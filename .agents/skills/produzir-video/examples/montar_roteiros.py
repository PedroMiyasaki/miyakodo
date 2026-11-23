"""Recorta dois roteiros de exemplo da narração já versionada de evals.

A voz é video/projects/evals-reel/assets/evals-cut-audio.m4a.
O frame do rosto usado no exemplo de gravação fica em
.agents/skills/produzir-video/assets/pedro-frame.jpg. Ele veio do
snapshot final-113/face.jpg, tirado do repositório quando a limpeza de
cache apagou a pasta. O mp4 bruto evals-cut-sdr.mp4 não está no checkout.
"""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
TRANSCRIPT = REPO / "video/projects/evals-reel/transcript-edited.json"
OUT = Path(__file__).resolve().parent
VOICE = "video/projects/evals-reel/assets/evals-cut-audio.m4a"
STILL = ".agents/skills/produzir-video/assets/pedro-frame.jpg"


def slice_words(start: float, end: float) -> list[dict]:
    data = json.loads(TRANSCRIPT.read_text(encoding="utf-8"))
    words = []
    for word in data["words"]:
        if start <= float(word["start"]) < end:
            words.append({
                "text": word["text"],
                "start": round(float(word["start"]), 4),
                "end": round(float(word["end"]), 4),
            })
    return words


def main() -> None:
    sem = {
        "mode": "sem-gravacao",
        "slug": "exemplo-sem-gravacao",
        "title": "Evals, do use case ao negócio",
        "purpose": "opiniao",
        "voice": {"src": VOICE, "in": 0.10, "out": 16.90},
        "emphasis": ["evals", "IA", "negócios", "importantes"],
        "strong": ["técnica"],
        "cta": ["vídeo"],
        "words": slice_words(0.10, 16.90),
        "beats": [
            {
                "start": 0.10,
                "end": 5.70,
                "layout": "guide",
                "label": "Use case",
                "scene": {
                    "type": "stack",
                    "children": [
                        {"type": "timeline", "title": "O argumento", "items": ["Use case", "Evals", "Negócio"]},
                        {"type": "mockup", "title": "Produto", "kind": "app", "lines": ["cliente", "promessa", "IA"]},
                    ],
                },
            },
            {
                "start": 5.70,
                "end": 11.40,
                "layout": "center",
                "label": "Evals",
                "scene": {
                    "type": "code",
                    "filename": "evals.ts",
                    "lines": ["const nota = avaliar()", "return nota"],
                },
            },
            {
                "start": 11.40,
                "end": 14.20,
                "layout": "guide",
                "label": "Negócio",
                "scene": {
                    "type": "stack",
                    "children": [
                        {"type": "diagram", "center": "Negócio", "items": ["Produto", "Cliente", "Receita"]},
                        {"type": "quote", "text": "Eles tocam em negócio.", "by": "Pedro"},
                    ],
                },
            },
            {
                "start": 14.20,
                "end": 16.90,
                "layout": "corner",
                "label": "Fica",
                "scene": {
                    "type": "phone",
                    "handle": "@MIYAKODO",
                    "comment": "explica evals",
                    "dm": "te mando o mapa",
                },
            },
        ],
    }
    grav = {
        "mode": "gravacao",
        "slug": "exemplo-gravacao",
        "title": "Contratos e cláusulas",
        "purpose": "historia",
        "voice": {"src": VOICE, "in": 18.13, "out": 34.20},
        "footage": {"still": STILL},
        "emphasis": ["contratos", "cláusulas", "importantes", "IA"],
        "strong": ["críticas"],
        "cta": ["empresa"],
        "words": slice_words(18.13, 34.20),
        "beats": [
            {
                "start": 18.13,
                "end": 24.10,
                "layout": "split",
                "label": "Empresa",
                "scene": {
                    "type": "stack",
                    "children": [
                        {
                            "type": "folders",
                            "root": "Empresa",
                            "items": [
                                {"name": "Fornecedor A", "depth": 1},
                                {"name": "Fornecedor B", "depth": 1},
                                {"name": "Contratos", "depth": 1},
                            ],
                        },
                        {
                            "type": "chat",
                            "title": "Contratos",
                            "messages": [
                                {"from": "Empresa", "text": "chegou contrato novo"},
                                {"from": "Pedro", "text": "lê as cláusulas"},
                            ],
                        },
                    ],
                },
            },
            {
                "start": 24.10,
                "end": 29.20,
                "layout": "motion",
                "label": "Contrato",
                "scene": {
                    "type": "stack",
                    "children": [
                        {"type": "counter", "label": "fornecedores", "value": 4},
                        {"type": "grid", "items": ["prazo", "multa", "foro", "sigilo", "preço", "vigência", "anexo", "aviso", "rescisão"]},
                        {"type": "scanline", "label": "leitura do contrato"},
                    ],
                },
            },
            {
                "start": 29.20,
                "end": 34.20,
                "layout": "creator",
                "label": "Cláusulas",
                "punch": True,
                "scene": {"type": "badge", "text": "cláusulas críticas"},
            },
        ],
    }
    (OUT / "sem-gravacao.json").write_text(json.dumps(sem, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "gravacao.json").write_text(json.dumps(grav, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"sem-gravacao {len(sem['words'])} palavras")
    print(f"gravacao {len(grav['words'])} palavras")


if __name__ == "__main__":
    main()
