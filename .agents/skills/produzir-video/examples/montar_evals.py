"""Monta o roteiro de gravação do Reel de evals a partir da transcrição.

A transcrição usada aqui saiu do bruto do release footage-evals
(video/inputs/evals/evals.MP4), não do áudio já cortado do projeto antigo.
Rode de novo só se for refazer a transcrição. O JSON commitado é a peça.
"""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "evals-gravacao.json"
FOOTAGE = "video/inputs/evals/evals.MP4"
DURACAO = 209.533


def _fix(token: str) -> str:
    bare = token.strip(".,;:!?\"")
    low = bare.lower()
    if low in {"evals", "evols", "vols"}:
        return token.replace(bare, "evals")
    if low == "ai":
        return token.replace(bare, "IA")
    if low == "pegarei":
        return token.replace(bare, "pegaria")
    return token


def load_words() -> list[dict]:
    base = json.loads(Path("/tmp/evals-words.json").read_text(encoding="utf-8"))["words"]
    tail = json.loads(Path("/tmp/evals-tail-words.json").read_text(encoding="utf-8"))
    merged = [word for word in base if word["start"] < 190] + tail
    cleaned = []
    skip_set = False
    for word in merged:
        text = _fix(word["text"])
        if skip_set and text.lower().strip(".,") == "set":
            skip_set = False
            continue
        skip_set = text.lower().strip(".,") == "data" and True
        if text.lower().strip(".,") == "data":
            text = "dataset"
            skip_set = True
        cleaned.append({"text": text, "start": word["start"], "end": word["end"]})
    return cleaned


def main() -> None:
    words = load_words()
    roteiro = {
        "mode": "gravacao",
        "slug": "evals-gravacao",
        "title": "Evals no produto",
        "purpose": "opiniao",
        "voice": {"src": FOOTAGE, "in": 0, "out": DURACAO},
        "footage": {"src": FOOTAGE},
        "emphasis": ["evals", "IA", "contratos", "cláusulas", "prompt", "Anthropic", "dataset"],
        "strong": ["problema", "quebrando"],
        "cta": ["comenta"],
        "words": words,
        "beats": [
            {"start": 0.0, "end": 20.06, "layout": "split", "label": "Gancho", "scene": {
                "type": "stack",
                "children": [
                    {"type": "timeline", "title": "O argumento", "items": ["Use case", "Evals", "Negócio"]},
                    {"type": "mockup", "title": "Produto", "kind": "app", "lines": ["cliente", "promessa", "IA"]},
                ],
            }},
            {"start": 20.06, "end": 36.14, "layout": "split", "label": "Fornecedores", "scene": {
                "type": "stack",
                "children": [
                    {"type": "folders", "root": "Empresa", "items": [
                        {"name": "Fornecedor A", "depth": 1},
                        {"name": "Fornecedor B", "depth": 1},
                        {"name": "Contratos", "depth": 1},
                    ]},
                    {"type": "chat", "title": "Contratos", "messages": [
                        {"from": "Empresa", "text": "cada contrato é diferente"},
                        {"from": "Pedro", "text": "lê as cláusulas"},
                    ]},
                ],
            }},
            {"start": 36.14, "end": 52.84, "layout": "motion", "label": "Sem evals", "scene": {
                "type": "code", "filename": "agente.ts",
                "lines": ["const resposta = agente(contrato)", "return resposta"],
            }},
            {"start": 52.84, "end": 78.26, "layout": "split", "label": "O problema", "scene": {
                "type": "bullets", "kicker": "Dois erros",
                "items": ["Aponta cláusula demais", "Esquece a cláusula crítica"],
            }},
            {"start": 78.26, "end": 93.10, "layout": "motion", "label": "O prompt", "scene": {
                "type": "quote", "text": "Mudou o prompt. Quebrou o resto.", "by": "Pedro",
            }},
            {"start": 93.10, "end": 106.80, "layout": "split", "label": "Dataset", "scene": {
                "type": "diagram", "center": "Evals", "items": ["Contratos", "Resposta", "Agente"],
            }},
            {"start": 106.80, "end": 122.00, "layout": "motion", "label": "50 contratos", "scene": {
                "type": "counter", "label": "contratos", "value": 50,
            }},
            {"start": 122.00, "end": 139.32, "layout": "split", "label": "Rodar de novo", "scene": {
                "type": "mockup", "title": "Produção", "kind": "evals", "scan": True,
                "lines": ["mudou o prompt", "roda o dataset", "confere a nota"],
            }},
            {"start": 139.32, "end": 153.00, "layout": "motion", "label": "Métrica", "scene": {
                "type": "diagram", "center": "Direção", "items": ["Métrica", "Nota", "Estabilidade"],
            }},
            {"start": 153.00, "end": 169.52, "layout": "split", "label": "Nota", "scene": {
                "type": "bullets", "kicker": "A regra",
                "items": ["Nota mais alta que a anterior", "Regra subjetiva quebra o resto"],
            }},
            {"start": 169.52, "end": 182.12, "layout": "motion", "label": "Jurídico", "scene": {
                "type": "chat", "title": "O caso", "messages": [
                    {"from": "Produto", "text": "essa regra quebra o caso"},
                    {"from": "Jurídico", "text": "deixa eu reescrever"},
                ],
            }},
            {"start": 182.12, "end": 199.56, "layout": "creator", "label": "Direção", "punch": False, "scene": {
                "type": "quote", "text": "O time deixa de ser reativo.", "by": "Pedro",
            }},
            {"start": 199.56, "end": 206.56, "layout": "split", "label": "Anthropic", "scene": {
                "type": "mockup", "title": "Anthropic", "kind": "material",
                "lines": ["material oficial", "sobre evals"],
            }},
            {"start": 206.56, "end": DURACAO, "layout": "creator", "label": "CTA", "punch": True, "scene": {
                "type": "phone", "handle": "@MIYAKODO", "comment": "evals", "dm": "te mando o material",
            }},
        ],
    }
    OUT.write_text(json.dumps(roteiro, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT, "words", len(words), "beats", len(roteiro["beats"]))


if __name__ == "__main__":
    main()
