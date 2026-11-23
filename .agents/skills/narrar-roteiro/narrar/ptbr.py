"""Fala em português do Brasil: abreviação, número e sigla viram texto pronunciável."""

from __future__ import annotations

import re

_UNITS = [
    "zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove",
    "dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete",
    "dezoito", "dezenove",
]
_TENS = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
_HUNDREDS = [
    "", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos",
    "seiscentos", "setecentos", "oitocentos", "novecentos",
]
_ORD_M = {
    1: "primeiro", 2: "segundo", 3: "terceiro", 4: "quarto", 5: "quinto",
    6: "sexto", 7: "sétimo", 8: "oitavo", 9: "nono", 10: "décimo",
}
_ORD_F = {
    1: "primeira", 2: "segunda", 3: "terceira", 4: "quarta", 5: "quinta",
    6: "sexta", 7: "sétima", 8: "oitava", 9: "nona", 10: "décima",
}
_LETTER = {
    "A": "a", "B": "bê", "C": "cê", "D": "dê", "E": "é", "F": "éfe", "G": "gê",
    "H": "agá", "I": "i", "J": "jota", "K": "cá", "L": "ele", "M": "eme", "N": "ene",
    "O": "ó", "P": "pê", "Q": "quê", "R": "erre", "S": "esse", "T": "tê", "U": "u",
    "V": "vê", "W": "dáblio", "X": "xis", "Y": "ípsilon", "Z": "zê",
}
ACRONYMS = {
    "IA", "RAG", "MCP", "API", "PDF", "NDA", "GPU", "CPU", "LLM", "SDK", "CLI",
    "SQL", "HTML", "CSS", "JSON", "URL", "CTA", "UX", "UI", "CRM", "MIT", "SFX",
    "TTS", "WAV", "HTTP", "CEO", "CFO", "ROI", "KPI", "FAQ", "OKR", "GPT",
}
_MEDIA = {
    "MP3": "eme pê três",
    "MP4": "eme pê quatro",
    "B2B": "bê dois bê",
    "B2C": "bê dois cê",
}

_ABBR = [
    (re.compile(r"\bp\.\s*ex\.", re.I), "por exemplo"),
    (re.compile(r"\bex\.:", re.I), "por exemplo:"),
    (re.compile(r"\bi\.e\.", re.I), "isto é"),
    (re.compile(r"\be\.g\.", re.I), "por exemplo"),
    (re.compile(r"\betc\.", re.I), "etcétera."),
    (re.compile(r"\bDra\.", re.I), "doutora"),
    (re.compile(r"\bDr\.", re.I), "doutor"),
    (re.compile(r"\bSra\.", re.I), "senhora"),
    (re.compile(r"\bSr\.", re.I), "senhor"),
    (re.compile(r"\bProfa\.", re.I), "professora"),
    (re.compile(r"\bProf\.", re.I), "professor"),
    (re.compile(r"\bart\.", re.I), "artigo"),
    (re.compile(r"\bpágs?\.", re.I), "página"),
    (re.compile(r"\bpags?\.", re.I), "página"),
    (re.compile(r"\bobs\.", re.I), "observação"),
    (re.compile(r"\baprox\.", re.I), "aproximadamente"),
    (re.compile(r"\bvs\.", re.I), "versus"),
    (re.compile(r"\bn\.º|\bnº|\bn°", re.I), "número"),
]
_CURRENCY = re.compile(
    r"(US\$|R\$)\s*(\d{1,3}(?:\.\d{3})+(?:,\d{1,2})?|\d+(?:,\d{1,2})?)"
)
_PERCENT = re.compile(r"(\d{1,3}(?:\.\d{3})+|\d+)(?:,(\d+))?\s*%")
_HOURS = re.compile(r"(?<![\w])(\d+)\s*h\b", re.I)
_UNIT = re.compile(r"(?<![\w])(\d+(?:,\d+)?)\s*(km|kg)\b", re.I)
_GPT = re.compile(r"\bGPT-(\d+)\b")
_ORDINAL = re.compile(r"(?<![\w])(\d{1,2})([ºª])")
_NUMBER = re.compile(
    r"(?<![\w])(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+,\d+|\d+\.\d+|\d+)(?![\w])"
)
_ACRONYM = re.compile(r"\b([A-Z]{2,5})(s)?\b")


def cardinal(number: int) -> str:
    if number < 0:
        return "menos " + cardinal(-number)
    if number < 20:
        return _UNITS[number]
    if number < 100:
        ten, unit = divmod(number, 10)
        if unit == 0:
            return _TENS[ten]
        return f"{_TENS[ten]} e {_UNITS[unit]}"
    if number == 100:
        return "cem"
    if number < 1000:
        hundred, rest = divmod(number, 100)
        if rest == 0:
            return _HUNDREDS[hundred]
        return f"{_HUNDREDS[hundred]} e {cardinal(rest)}"
    if number < 1_000_000:
        thousand, rest = divmod(number, 1000)
        head = "mil" if thousand == 1 else f"{cardinal(thousand)} mil"
        return _join_big(head, rest)
    if number < 1_000_000_000:
        million, rest = divmod(number, 1_000_000)
        head = "um milhão" if million == 1 else f"{cardinal(million)} milhões"
        return _join_big(head, rest)
    billion, rest = divmod(number, 1_000_000_000)
    head = "um bilhão" if billion == 1 else f"{cardinal(billion)} bilhões"
    return _join_big(head, rest)


def _join_big(head: str, rest: int) -> str:
    if rest == 0:
        return head
    if rest < 100 or rest % 100 == 0:
        return f"{head} e {cardinal(rest)}"
    return f"{head} {cardinal(rest)}"


def feminine_cardinal(number: int) -> str:
    word = cardinal(number)
    if word == "um":
        return "uma"
    if word == "dois":
        return "duas"
    if word.endswith(" e um"):
        return word[:-2] + "uma"
    if word.endswith(" e dois"):
        return word[:-4] + "duas"
    return word


def ordinal(number: int, feminine: bool) -> str:
    table = _ORD_F if feminine else _ORD_M
    if number in table:
        return table[number]
    if 11 <= number <= 19:
        base = "décima" if feminine else "décimo"
        return f"{base} {table[number - 10]}"
    return cardinal(number)


def number_to_words(token: str) -> str:
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", token):
        return cardinal(int(token.replace(".", "")))
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+,\d+|\d+,\d+", token):
        whole, frac = token.replace(".", "").split(",")
        spoken = cardinal(int(whole))
        if int(frac) == 0:
            return spoken
        return f"{spoken} vírgula {' '.join(cardinal(int(digit)) for digit in frac)}"
    if re.fullmatch(r"\d+\.\d+", token):
        whole, frac = token.split(".")
        return f"{cardinal(int(whole))} ponto {' '.join(cardinal(int(digit)) for digit in frac)}"
    return cardinal(int(token))


def _money(symbol: str, token: str) -> str:
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+(?:,\d{1,2})?", token):
        body = token.replace(".", "")
    else:
        body = token
    if "," in body:
        whole, frac = body.split(",")
        amount = int(whole or "0")
        cents = int((frac + "0")[:2])
    else:
        amount = int(body or "0")
        cents = 0
    if symbol == "US$":
        unit = "dólar" if amount == 1 else "dólares"
        spoken = f"{cardinal(amount)} {unit}"
        if cents:
            cent_unit = "centavo" if cents == 1 else "centavos"
            spoken = f"{spoken} e {cardinal(cents)} {cent_unit}"
        return spoken
    parts = []
    if amount or not cents:
        parts.append(f"{cardinal(amount)} {'real' if amount == 1 else 'reais'}")
    if cents:
        parts.append(f"{cardinal(cents)} {'centavo' if cents == 1 else 'centavos'}")
    return " e ".join(parts)


def _spell(token: str, plural: bool) -> str:
    parts = [_LETTER[letter] for letter in token]
    if plural and parts:
        parts[-1] = parts[-1] + "s"
    return " ".join(parts)


def normalize_ptbr(text: str) -> str:
    """Prepara um parágrafo já sem marcação para o TTS ler em voz alta."""
    if not text or not text.strip():
        return ""
    cleaned = text.replace("…", ",").replace("...", ",")
    cleaned = cleaned.replace("—", ", ").replace("–", ", ")
    cleaned = cleaned.replace("→", ". ").replace("->", ". ")
    cleaned = cleaned.replace("≠", " não é ")
    cleaned = cleaned.replace("×", " por ")
    cleaned = re.sub(r"\s=\s", ", ", cleaned)
    for pattern, replacement in _ABBR:
        cleaned = pattern.sub(replacement, cleaned)
    cleaned = _CURRENCY.sub(lambda match: _money(match.group(1), match.group(2)), cleaned)
    cleaned = _PERCENT.sub(_percent, cleaned)
    cleaned = _HOURS.sub(lambda match: _hours(int(match.group(1))), cleaned)
    cleaned = _UNIT.sub(_unit, cleaned)
    for token, spoken in _MEDIA.items():
        cleaned = re.sub(rf"\b{token}\b", spoken, cleaned)
    cleaned = _GPT.sub(lambda match: f"gê pê tê {match.group(1)}", cleaned)
    cleaned = _ORDINAL.sub(
        lambda match: ordinal(int(match.group(1)), match.group(2) == "ª"),
        cleaned,
    )
    cleaned = _NUMBER.sub(lambda match: number_to_words(match.group(1)), cleaned)
    cleaned = _ACRONYM.sub(_acronym, cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"\s+([,.!?;:])", r"\1", cleaned)
    cleaned = re.sub(r"\.{2,}", ".", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _percent(match: re.Match) -> str:
    whole = number_to_words(match.group(1))
    frac = match.group(2)
    if frac:
        digits = " ".join(cardinal(int(digit)) for digit in frac)
        whole = f"{whole} vírgula {digits}"
    return f"{whole} por cento"


def _hours(number: int) -> str:
    if number == 1:
        return "uma hora"
    return f"{feminine_cardinal(number)} horas"


def _unit(match: re.Match) -> str:
    token = match.group(1)
    kind = match.group(2).lower()
    if "," in token:
        whole, frac = token.split(",")
        spoken = f"{cardinal(int(whole))} vírgula {' '.join(cardinal(int(digit)) for digit in frac)}"
        amount = float(token.replace(",", "."))
    else:
        spoken = cardinal(int(token))
        amount = int(token)
    if kind == "km":
        unit = "quilômetro" if amount == 1 else "quilômetros"
    else:
        unit = "quilo" if amount == 1 else "quilos"
    return f"{spoken} {unit}"


def _acronym(match: re.Match) -> str:
    token = match.group(1)
    if token not in ACRONYMS:
        return match.group(0)
    return _spell(token, match.group(2) == "s")
