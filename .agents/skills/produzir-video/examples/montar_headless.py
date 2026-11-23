"""Monta o roteiro sem-gravacao de Headless Software a partir da transcrição.

A transcrição palavra a palavra fica em headless-software-words.json depois
desta etapa. O JSON final é headless-software.json.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORDS_SRC = Path("/tmp/headless-audio/transcript.json")

SWAPS = [
    (["muito", "alta", "do"], ["muito", "em", "alta", "no"]),
    (["em", "muito", "envolgo"], ["muito", "em", "voga"]),
    (["solt"], ["soltou"]),
    (["gente", "de", "a"], ["agente", "de", "IA"]),
    (["de", "a"], ["de", "IA"]),
    (["e", "a", "pessoais"], ["pessoais"]),
    (["e", "pessoais"], ["pessoais"]),
    (["uma", "alerta"], ["um", "alerta"]),
    (["feito", "por", "seus"], ["feito", "para", "os"]),
    (["ai"], ["IA"]),
]


def key(token: str) -> str:
    return "".join(ch for ch in token.lower() if ch.isalnum())


def apply_swaps(words: list[dict]) -> list[dict]:
    current = words
    for old, new in SWAPS:
        keys = [key(word["text"]) for word in current]
        size = len(old)
        rebuilt = []
        index = 0
        while index < len(current):
            if keys[index:index + size] == old:
                start = current[index]["start"]
                end = current[index + size - 1]["end"]
                step = max(0.08, (end - start) / len(new))
                for offset, text in enumerate(new):
                    rebuilt.append({
                        "text": text,
                        "start": round(start + step * offset, 3),
                        "end": round(min(end, start + step * (offset + 1)), 3),
                    })
                index += size
            else:
                rebuilt.append(current[index])
                index += 1
        current = rebuilt
    return current


def snap(words: list[dict], moment: float) -> float:
    for word in words:
        if word["end"] >= moment - 0.04:
            return word["end"]
    return words[-1]["end"]


PLAN = [
    (2.6, "hero", "ink", "Gancho", {"type": "statement", "kicker": "Talvez você não saiba", "text": "O futuro"}),
    (6.6, "full", "verde", "Sem interface", {"type": "statement", "text": "Sem nenhuma interface"}),
    (10.1, "pip", "paper", "Headless", {"type": "statement", "kicker": "Vale do Silício", "text": "Headless"}),
    (14.1, "full", "azul", "Sem botão", {"type": "bullets", "kicker": "Sem nada disso", "items": ["Interface", "Botão", "Tela"]}),
    (17.8, "guide", "paper", "Usuário", {"type": "mockup", "title": "Software", "kind": "produto", "lines": ["sem tela", "sem clique", "sem usuário dentro"]}),
    (21.7, "hero", "rosa", "Pergunta", {"type": "statement", "text": "Como funciona?"}),
    (26.2, "full", "oliva", "Outra ideia", {"type": "statement", "kicker": "Junto com isso", "text": "Outra ideia"}),
    (30.2, "pip", "paper", "Agents", {"type": "statement", "kicker": "Em alta", "text": "Personal agents"}),
    (34.8, "full", "azul", "Quem usa", {"type": "grid", "items": ["Instinct", "Grok Bot", "Uso pessoal"]}),
    (37.7, "guide", "paper", "O dia", {"type": "carlos", "pose": "coffee", "line": "O dia a dia dele"}),
    (41.1, "full", "rosa", "Tarefas", {"type": "bullets", "kicker": "O agente faz", "items": ["Pagar contas", "Marcar médico", "Resolver o dia"]}),
    (43.6, "pip", "paper", "O software", {"type": "statement", "kicker": "Headless", "text": "O software"}),
    (45.9, "hero", "verde", "Para o agente", {"type": "statement", "text": "Para o agente"}),
    (48.9, "guide", "paper", "Não para você", {"type": "carlos", "pose": "boss", "line": "Não para você"}),
    (52.9, "pip", "azul", "Stripe", {"type": "mockup", "title": "Stripe", "kind": "pagamento", "lines": ["empresa de pagamento", "1% do PIB mundial"]}),
    (55.7, "full", "paper", "Tempos", {"type": "statement", "text": "Nos últimos tempos"}),
    (58.2, "hero", "ink", "Pagamentos", {"type": "statement", "kicker": "Dentro da Stripe", "text": "Agentes pagando"}),
    (61.9, "pip", "oliva", "Curva", {"type": "statement", "text": "Crescendo"}),
    (66.2, "full", "verde", "Economia", {"type": "statement", "text": "Economia nova"}),
    (69.0, "guide", "paper", "Destino", {"type": "versus", "left": "Pessoas", "right": "Agentes", "left_items": ["menos"], "right_items": ["o software", "o serviço"], "pose": "squat"}),
    (73.5, "guide", "rosa", "Empresário", {"type": "carlos", "pose": "squat", "line": "Se você é empresário"}),
    (77.0, "full", "ink", "Alerta", {"type": "statement", "text": "Um alerta"}),
    (81.4, "pip", "paper", "Vender", {"type": "bullets", "kicker": "Não basta", "items": ["Vender o produto", "Vender o serviço", "Falar só com pessoas"]}),
    (85.0, "guide", "azul", "Cardápio", {"type": "carlos", "pose": "boss", "line": "Expõe o cardápio"}),
    (89.6, "full", "paper", "Cotidiano", {"type": "versus", "left": "Pessoa", "right": "Agente", "left_items": ["vê a página"], "right_items": ["resolve o dia"], "pose": "coffee"}),
    (93.7, "pip", "oliva", "Pessoas", {"type": "statement", "text": "Bom para pessoas"}),
    (97.7, "guide", "rosa", "Agente cego", {"type": "carlos", "pose": "stars", "line": "Ruim para o agente"}),
    (101.9, "full", "ink", "Some", {"type": "statement", "text": "Não aparece"}),
    (104.1, "pip", "paper", "Concorrente", {"type": "bullets", "kicker": "O agente", "items": ["Não acha", "Não opera", "O concorrente leva"]}),
    (106.7, "pip", "azul", "Futuro", {"type": "statement", "text": "No futuro"}),
    (108.9, "full", "verde", "Quem cresce", {"type": "statement", "text": "Quem cresce"}),
    (113.8, "guide", "paper", "Cardápio do agente", {"type": "carlos", "pose": "money", "line": "Cardápio para o agente"}),
    (117.8, "full", "azul", "Direção", {"type": "statement", "text": "Não só para pessoas"}),
    (121.2, "pip", "paper", "Perfil", {"type": "quote", "text": "Perspectiva de mercado, sem ruído.", "by": "Pedro Miyasaki"}),
    (124.7, "hero", "verde", "CTA", {"type": "badge", "text": "Me segue"}),
]


def main() -> None:
    raw = json.loads(WORDS_SRC.read_text(encoding="utf-8"))["words"]
    words = apply_swaps(raw)
    beats = []
    cursor = 0.0
    for until, layout, tone, label, scene in PLAN:
        end = snap(words, until)
        end = max(end, round(cursor + 1.8, 3))
        if beats and end <= cursor + 0.4:
            continue
        beats.append({
            "start": round(cursor, 3),
            "end": round(end, 3),
            "layout": layout,
            "tone": tone,
            "label": label,
            "scene": scene,
        })
        cursor = end
    beats[-1]["end"] = round(max(beats[-1]["end"], words[-1]["end"] + 0.15), 3)
    roteiro = {
        "mode": "sem-gravacao",
        "slug": "headless-software-sem-gravacao",
        "title": "Headless Software",
        "purpose": "opiniao",
        "voice": {
            "src": "video/inputs/headless-software/headless-software.MP4",
            "in": 0,
            "out": 124.68,
        },
        "emphasis": ["interface", "Headless", "agentes", "empresário", "cardápio", "Stripe", "IA"],
        "strong": ["agente"],
        "cta": ["segue", "like"],
        "words": words,
        "beats": beats,
    }
    (ROOT / "headless-software-words.json").write_text(
        json.dumps(words, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / "headless-software.json").write_text(
        json.dumps(roteiro, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"palavras {len(words)} beats {len(beats)} fim {beats[-1]['end']}")
    for beat in beats:
        print(f"{beat['start']:7.2f}-{beat['end']:7.2f} {beat['end']-beat['start']:4.1f}s {beat['layout']:6} {beat['tone']:6} {beat['label']}")


if __name__ == "__main__":
    main()
