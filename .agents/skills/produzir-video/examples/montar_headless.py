"""Monta o roteiro sem-gravacao de Headless Software a partir da transcrição.

A transcrição palavra a palavra fica em headless-software-words.json depois
desta etapa. O JSON final é headless-software.json.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORDS_SRC = ROOT / "headless-software-words.json"

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
    (2.6, "hero", "ink", "Gancho", {"type": "peel", "kicker": "Talvez você não saiba", "text": "O futuro do software", "items": ["Botão", "Menu", "Tela", "Dashboard"], "lines": ["API", "MCP", "CLI"]}),
    (6.6, "full", "verde", "Sem interface", {"type": "peel", "text": "Sem nenhuma interface", "items": ["Botão", "Menu", "Dashboard"], "lines": ["API", "MCP", "CLI"]}),
    (10.1, "full", "paper", "Headless", {"type": "peel", "kicker": "Vale do Silício", "text": "Headless", "items": ["UI", "Clique", "Formulário"], "lines": ["API", "MCP", "CLI"]}),
    (14.1, "full", "azul", "Sem botão", {"type": "flow", "kicker": "Some tudo isso", "items": ["Interface", "Botão", "Tela", "Dashboard"]}),
    (17.8, "guide", "paper", "Usuário", {"type": "carlos", "pose": "boss", "line": "Sem usuário dentro", "props": ["sem tela", "sem clique", "sem formulário"]}),
    (21.7, "full", "paper", "Pergunta", {"type": "versus", "left": "Humano", "right": "Agente", "left_items": ["vê a tela", "clica", "preenche", "espera"], "right_items": ["chama API", "lê MCP", "executa", "não clica"], "pose": "boss"}),
    (26.2, "full", "oliva", "Outra ideia", {"type": "flow", "kicker": "Junto com isso", "items": ["Outra ideia", "Personal agents", "Fazem a tarefa", "Não só respondem"]}),
    (30.2, "full", "paper", "Agents", {"type": "statement", "kicker": "Em alta", "lines": ["Personal", "agents"], "chips": ["Instinct", "Grok Bot", "uso pessoal"]}),
    (34.8, "guide", "azul", "Quem usa", {"type": "carlos", "pose": "coffee", "line": "No dia a dia", "props": ["Instinct", "Grok Bot", "conta", "agenda"]}),
    (37.7, "full", "rosa", "O dia", {"type": "flow", "kicker": "O agente faz", "items": ["Pagar contas", "Marcar médico", "Lembrar", "Resolver o dia"]}),
    (41.1, "full", "verde", "Tarefas", {"type": "statement", "lines": ["Feito para", "o agente"], "chips": ["compra", "agenda", "contrata"]}),
    (43.6, "full", "paper", "O software", {"type": "peel", "kicker": "Headless", "text": "O software", "items": ["Tela", "Botão"], "lines": ["API", "MCP", "CLI"]}),
    (45.9, "hero", "verde", "Para o agente", {"type": "statement", "text": "Para o agente", "chips": ["não para você", "para a função"]}),
    (48.9, "full", "paper", "Não para você", {"type": "clutter", "pose": "boss", "line": "Não para você", "props": ["Nome", "Email", "Cargo", "Empresa", "Telefone", "CNPJ"]}),
    (52.9, "full", "azul", "Stripe", {"type": "flow", "kicker": "Stripe", "items": ["Pagamentos", "1% do PIB", "Agentes", "Sem clique"]}),
    (55.7, "pip", "paper", "Tempos", {"type": "statement", "lines": ["Nos últimos", "tempos"], "chips": ["volume", "agentes", "curva"]}),
    (58.2, "hero", "ink", "Pagamentos", {"type": "statement", "kicker": "Dentro da Stripe", "text": "Agentes pagando", "chips": ["sem tela", "sem botão"]}),
    (61.9, "full", "oliva", "Curva", {"type": "chart", "kicker": "Stripe", "text": "Crescendo"}),
    (66.2, "full", "verde", "Economia", {"type": "flow", "kicker": "Economia nova", "items": ["Software", "Serviço", "Para o agente", "Menos para a pessoa"]}),
    (69.0, "full", "paper", "Destino", {"type": "versus", "left": "Pessoas", "right": "Agentes", "left_items": ["vê a tela", "clica", "preenche", "menos peso"], "right_items": ["chama função", "lê API", "paga", "fecha"], "pose": "squat"}),
    (73.5, "guide", "rosa", "Empresário", {"type": "carlos", "pose": "squat", "line": "Se você é empresário", "props": ["alerta", "produto", "serviço"]}),
    (77.0, "full", "paper", "Alerta", {"type": "versus", "left": "Só pessoa", "right": "Também agente", "left_items": ["site", "anúncio", "formulário"], "right_items": ["API", "preço", "pedido"], "pose": "squat"}),
    (81.4, "full", "paper", "Vender", {"type": "flow", "kicker": "Não basta", "items": ["Vender o produto", "Vender o serviço", "Falar só com pessoas", "Ignorar o agente"]}),
    (85.0, "guide", "azul", "Cardápio", {"type": "carlos", "pose": "boss", "line": "Expõe o cardápio", "props": ["preço", "estoque", "pedido", "pagamento"]}),
    (89.6, "full", "paper", "Cotidiano", {"type": "versus", "left": "Pessoa", "right": "Agente", "left_items": ["vê a página", "lê o site", "preenche", "compara no olho"], "right_items": ["resolve o dia", "lê o endpoint", "chama a função", "fecha sozinho"], "pose": "coffee"}),
    (93.7, "full", "oliva", "Pessoas", {"type": "statement", "lines": ["Bom para", "pessoas"], "chips": ["página", "site", "formulário"]}),
    (97.7, "full", "rosa", "Agente cego", {"type": "maze", "pose": "stars", "line": "Ruim para o agente", "props": ["Modal", "Dropdown", "Popup", "Cookie", "Menu", "Alerta"]}),
    (101.9, "full", "ink", "Some", {"type": "statement", "text": "Não aparece", "chips": ["sumiu", "o agente passa", "o concorrente fica"]}),
    (104.1, "full", "paper", "Concorrente", {"type": "flow", "kicker": "O agente", "items": ["Não acha", "Não opera", "O concorrente leva", "Você perde o cliente"]}),
    (106.7, "full", "azul", "Futuro", {"type": "statement", "lines": ["No futuro"], "chips": ["bens", "serviços", "cardápio", "acesso"]}),
    (108.9, "full", "verde", "Quem cresce", {"type": "statement", "text": "Quem cresce", "chips": ["cardápio aberto", "agente entra", "cliente fica"]}),
    (113.8, "guide", "paper", "Cardápio do agente", {"type": "carlos", "pose": "money", "line": "Cardápio para o agente", "props": ["preço", "API", "endpoint", "pagamento"]}),
    (117.8, "full", "azul", "Direção", {"type": "versus", "left": "Pessoa", "right": "Agente", "left_items": ["a porta de sempre", "o site", "o atendimento"], "right_items": ["a porta nova", "a função", "o acesso"], "pose": "boss"}),
    (121.2, "full", "ink", "Perfil", {"type": "close", "text": "Headless", "handle": "@pedro.miyasaki.ia"}),
    (124.7, "hero", "verde", "CTA", {"type": "close", "text": "Me segue", "handle": "@pedro.miyasaki.ia"}),
]


def main() -> None:
    payload = json.loads(WORDS_SRC.read_text(encoding="utf-8"))
    raw = payload["words"] if isinstance(payload, dict) else payload
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
