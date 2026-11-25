#!/usr/bin/env python3
"""Coleta pública para a estratégia viral. Sem chave e sem login.

Cada fonte que falha vira uma lacuna. As outras continuam.
Saída: um JSON na saída padrão.

Uso:
  python3 .agents/skills/content-research/scripts/fontes_virais.py --horas 24
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import urllib.parse
import urllib.request
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, timezone

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# Canais cujo RSS devolve data e views sem chave.
# A busca livre do YouTube não devolve lista neste ambiente.
CANAIS_YOUTUBE = (
    ("Fireship", "UCsBjURrPoezykLs9EqgamOA"),
    ("Y Combinator", "UCcefcZRL2oaA_uBNeo5UOWg"),
    ("a16z", "UC9cn0TuPq4dnbTY-CBsm8XA"),
)

CONSULTAS_HN = ("agents", "AI", "ChatGPT")
PONTOS_MINIMOS_HN = 40
VIEWS_MINIMAS_YOUTUBE = 100_000
TERMO_IA = re.compile(
    r"\b(ia|ai|intelig[eê]ncia artificial|chatgpt|gemini|claude|agente|agentes)\b",
    re.IGNORECASE,
)


def buscar(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "*/*", "Accept-Language": "pt-BR,en;q=0.8"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read(500_000)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def dentro(publicado: datetime, inicio: datetime, agora: datetime) -> bool:
    if publicado.tzinfo is None:
        publicado = publicado.replace(tzinfo=timezone.utc)
    return inicio <= publicado.astimezone(timezone.utc) <= agora


def hacker_news(inicio: datetime, agora: datetime) -> dict:
    ts = int(inicio.timestamp())
    vistos: set[str] = set()
    itens = []
    for consulta in CONSULTAS_HN:
        filtro = urllib.parse.quote(f"created_at_i>{ts},points>={PONTOS_MINIMOS_HN}")
        url = (
            "https://hn.algolia.com/api/v1/search?"
            f"query={urllib.parse.quote(consulta)}&tags=story"
            f"&numericFilters={filtro}&hitsPerPage=15"
        )
        bruto = json.loads(buscar(url))
        for hit in bruto.get("hits") or []:
            oid = str(hit.get("objectID") or "")
            if not oid or oid in vistos:
                continue
            vistos.add(oid)
            criado = hit.get("created_at")
            if not criado:
                continue
            publicado = datetime.fromisoformat(criado.replace("Z", "+00:00"))
            if not dentro(publicado, inicio, agora):
                continue
            pontos = int(hit.get("points") or 0)
            if pontos < PONTOS_MINIMOS_HN:
                continue
            itens.append(
                {
                    "titulo": hit.get("title") or "",
                    "url": hit.get("url") or f"https://news.ycombinator.com/item?id={oid}",
                    "discussao": f"https://news.ycombinator.com/item?id={oid}",
                    "publicado_em": iso(publicado),
                    "engajamento": {
                        "pontos": pontos,
                        "comentarios": int(hit.get("num_comments") or 0),
                    },
                    "data_vem_de": "created_at da API do Algolia",
                }
            )
    itens.sort(key=lambda item: item["engajamento"]["pontos"], reverse=True)
    return {"nome": "hacker news", "ok": True, "erro": None, "itens": itens[:8]}


def youtube(inicio: datetime, agora: datetime) -> dict:
    itens = []
    erros = []
    for nome, canal in CANAIS_YOUTUBE:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={canal}"
        try:
            texto = buscar(url).decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001 - uma falha de canal não para o resto
            erros.append(f"{nome}: {exc}")
            continue
        entradas = re.findall(r"<entry>.*?</entry>", texto, re.S)
        views_feed = [int(v) for v in re.findall(r'views="(\d+)"', texto)]
        mediana = int(statistics.median(views_feed)) if views_feed else None
        for entrada in entradas:
            pub = re.search(r"<published>([^<]+)</published>", entrada)
            titulo = re.search(r"<title>([^<]+)</title>", entrada)
            video = re.search(r"<yt:videoId>([^<]+)</yt:videoId>", entrada)
            views = re.search(r'views="(\d+)"', entrada)
            if not (pub and titulo and video and views):
                continue
            publicado = datetime.fromisoformat(pub.group(1).replace("Z", "+00:00"))
            if not dentro(publicado, inicio, agora):
                continue
            contagem = int(views.group(1))
            acima = mediana is not None and contagem >= mediana
            if contagem < VIEWS_MINIMAS_YOUTUBE and not acima:
                continue
            itens.append(
                {
                    "titulo": titulo.group(1),
                    "url": f"https://www.youtube.com/watch?v={video.group(1)}",
                    "canal": nome,
                    "publicado_em": iso(publicado),
                    "engajamento": {"views": contagem, "mediana_do_canal": mediana},
                    "data_vem_de": "published do RSS do canal",
                }
            )
    return {
        "nome": "youtube rss",
        "ok": bool(itens) or not erros,
        "erro": "; ".join(erros) or None,
        "itens": itens[:8],
    }


def product_hunt(inicio: datetime, agora: datetime) -> dict:
    texto = buscar("https://www.producthunt.com/feed").decode("utf-8", "replace")
    itens = []
    for entrada in re.findall(r"<entry>.*?</entry>", texto, re.S):
        pub = re.search(r"<published>([^<]+)</published>", entrada)
        titulo = re.search(r"<title>([^<]+)</title>", entrada)
        link = re.search(r'href="([^"]+)"', entrada)
        if not (pub and titulo and link):
            continue
        publicado = datetime.fromisoformat(pub.group(1))
        if not dentro(publicado, inicio, agora):
            continue
        itens.append(
            {
                "titulo": titulo.group(1),
                "url": link.group(1).split("?")[0],
                "publicado_em": iso(publicado),
                "engajamento": None,
                "data_vem_de": "published do feed Atom",
                "limite": "sem contagem de votos. Não sustenta viral sozinho.",
            }
        )
    return {"nome": "product hunt", "ok": True, "erro": None, "itens": itens[:8]}


def trends_brasil(inicio: datetime, agora: datetime) -> dict:
    texto = buscar("https://trends.google.com/trending/rss?geo=BR").decode("utf-8", "replace")
    itens = []
    for item in re.findall(r"<item>.*?</item>", texto, re.S):
        titulo = re.search(r"<title>([^<]+)</title>", item)
        trafego = re.search(r"<ht:approx_traffic>([^<]+)</ht:approx_traffic>", item)
        quando = re.search(r"<pubDate>([^<]+)</pubDate>", item)
        if not (titulo and trafego and quando):
            continue
        if not TERMO_IA.search(titulo.group(1)):
            continue
        publicado = parsedate_to_datetime(quando.group(1))
        if not dentro(publicado, inicio, agora):
            continue
        itens.append(
            {
                "titulo": titulo.group(1),
                "url": None,
                "publicado_em": iso(publicado),
                "engajamento": {"trafego_aproximado": trafego.group(1)},
                "data_vem_de": "pubDate da lista diária. Não é a data de uma peça.",
                "limite": "sinal de busca, não um post. Não vira ideia sozinho.",
            }
        )
    return {"nome": "google trends br", "ok": True, "erro": None, "itens": itens}


def reddit(inicio: datetime, agora: datetime) -> dict:
    url = "https://www.reddit.com/r/LocalLLaMA/top.json?t=day&limit=10&raw_json=1"
    try:
        bruto = json.loads(buscar(url))
    except Exception as exc:  # noqa: BLE001
        return {
            "nome": "reddit",
            "ok": False,
            "erro": f"sem acesso ({exc}). r/LocalLLaMA, r/ChatGPT e r/artificial ficam de fora nesta máquina.",
            "itens": [],
        }
    itens = []
    for filho in bruto.get("data", {}).get("children", []):
        dado = filho.get("data") or {}
        if "created_utc" not in dado:
            continue
        publicado = datetime.fromtimestamp(dado["created_utc"], timezone.utc)
        if not dentro(publicado, inicio, agora):
            continue
        itens.append(
            {
                "titulo": dado.get("title") or "",
                "url": "https://www.reddit.com" + dado.get("permalink", ""),
                "publicado_em": iso(publicado),
                "engajamento": {
                    "pontos": int(dado.get("score") or 0),
                    "comentarios": int(dado.get("num_comments") or 0),
                },
                "data_vem_de": "created_utc do JSON",
            }
        )
    return {"nome": "reddit", "ok": True, "erro": None, "itens": itens[:8]}


def main() -> None:
    parser = argparse.ArgumentParser(description="Fontes públicas da estratégia viral.")
    parser.add_argument("--horas", type=int, default=24, help="Janela em horas, a partir de agora.")
    args = parser.parse_args()
    agora = datetime.now(timezone.utc)
    inicio = agora - timedelta(hours=args.horas)
    fontes = []
    for coletor in (
        lambda: hacker_news(inicio, agora),
        lambda: youtube(inicio, agora),
        lambda: product_hunt(inicio, agora),
        lambda: trends_brasil(inicio, agora),
        lambda: reddit(inicio, agora),
    ):
        try:
            fontes.append(coletor())
        except Exception as exc:  # noqa: BLE001
            fontes.append({"nome": getattr(coletor, "__name__", "fonte"), "ok": False, "erro": str(exc), "itens": []})
    print(
        json.dumps(
            {
                "agora": iso(agora),
                "inicio": iso(inicio),
                "horas": args.horas,
                "fontes": fontes,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
