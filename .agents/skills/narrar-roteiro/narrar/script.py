"""Lê o roteiro híbrido do teleprompter, ou um Markdown corrido, e corta em chunks."""

from __future__ import annotations

import re
from dataclasses import dataclass

from narrar.ptbr import normalize_ptbr

MODES = ("auto", "literal", "all")
DEFAULT_MAX_CHARS = 240

_COMMENT = re.compile(r"<!--.*?-->", re.S)
_HEADER = re.compile(
    r"^\[([^\]\n]+)\]\s*(?:[·•|]\s*(literal|tópicos|topicos))?\s*$",
    re.IGNORECASE,
)
_FENCE = re.compile(r"^```")
_HEADING = re.compile(r"^#{1,6}\s+")
_BULLET = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
_QUOTE = re.compile(r"^\s*>\s?")
_RULES = {"---", "***", "___"}
_SKIP_PREFIXES = (
    "insert", "inserir", "cena", "b-roll", "broll", "nota", "sfx",
    "corte", "cut", "gravação", "gravacao", "fonte", "fontes", "overlay",
)


@dataclass(frozen=True)
class Paragraph:
    text: str
    break_after: str


@dataclass(frozen=True)
class Chunk:
    text: str
    break_after: str


@dataclass(frozen=True)
class Speech:
    paragraphs: tuple[Paragraph, ...]
    chunks: tuple[Chunk, ...]
    text: str


def prepare_speech(text: str, mode: str = "auto", max_chars: int = DEFAULT_MAX_CHARS) -> Speech:
    if mode not in MODES:
        raise ValueError(f"mode inválido: {mode}. Use auto, literal ou all.")
    if max_chars < 20:
        raise ValueError("max_chars pequeno demais para uma frase")
    paragraphs = tuple(parse_paragraphs(text, mode))
    chunks = tuple(chunk_paragraphs(paragraphs, max_chars))
    spoken = " ".join(chunk.text for chunk in chunks)
    return Speech(paragraphs=paragraphs, chunks=chunks, text=spoken)


def render_preview(chunks: list[Chunk] | tuple[Chunk, ...]) -> str:
    blocks: list[str] = []
    current: list[str] = []
    for chunk in chunks:
        current.append(chunk.text)
        if chunk.break_after in {"paragraph", "beat", "end"}:
            blocks.append(" ".join(current))
            current = []
    if current:
        blocks.append(" ".join(current))
    return "\n\n".join(blocks)


def looks_hybrid(text: str) -> bool:
    for line in text.splitlines():
        header = _HEADER.match(line.strip())
        if header and classify_bracket(header.group(1)) == "section":
            return True
    return False


def classify_bracket(label: str) -> str:
    raw = label.strip()
    low = raw.lower()
    if low in {"pause", "pausa", "respiro"}:
        return "pause"
    if low.startswith(_SKIP_PREFIXES) or ":" in raw:
        return "skip"
    return "section"


def parse_paragraphs(text: str, mode: str) -> list[Paragraph]:
    if mode not in MODES:
        raise ValueError(f"mode inválido: {mode}. Use auto, literal ou all.")
    raw = _COMMENT.sub("", text)
    hybrid = looks_hybrid(raw)
    effective = "literal" if (mode == "auto" and hybrid) or mode == "literal" else "all"
    paragraphs: list[Paragraph] = []
    buf: list[str] = []
    section_mode: str | None = None
    include = _include(effective, section_mode, hybrid)
    in_fence = False

    def flush(kind: str = "paragraph") -> None:
        nonlocal buf
        if include:
            joined = normalize_ptbr(_join(buf))
            if joined:
                paragraphs.append(Paragraph(joined, kind))
        buf = []

    for line in raw.splitlines():
        stripped = line.strip()
        if _FENCE.match(stripped):
            flush("paragraph")
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped in _RULES:
            flush("paragraph")
            if hybrid:
                break
            continue
        header = _HEADER.match(stripped)
        if header:
            kind = classify_bracket(header.group(1))
            if kind == "skip":
                continue
            if kind == "pause":
                if include and buf:
                    flush("beat")
                else:
                    buf = []
                    if paragraphs and paragraphs[-1].break_after != "beat":
                        paragraphs[-1] = Paragraph(paragraphs[-1].text, "beat")
                continue
            flush("paragraph")
            section_mode = _mode_name(header.group(2))
            include = _include(effective, section_mode, hybrid)
            continue
        if not stripped:
            flush("paragraph")
            continue
        if hybrid and _HEADING.match(stripped):
            continue
        cleaned = clean_line(stripped)
        if cleaned:
            buf.append(cleaned)
    flush("paragraph")
    return paragraphs


def chunk_paragraphs(paragraphs: list[Paragraph] | tuple[Paragraph, ...], max_chars: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    last_index = len(paragraphs) - 1
    for index, paragraph in enumerate(paragraphs):
        packed = pack_sentences(split_sentences(paragraph.text), max_chars)
        last_paragraph = index == last_index
        for piece_index, piece in enumerate(packed):
            last_piece = piece_index == len(packed) - 1
            if last_piece and paragraph.break_after == "beat":
                kind = "beat"
            elif last_piece and last_paragraph:
                kind = "end"
            elif last_piece:
                kind = "paragraph"
            else:
                kind = "sentence"
            chunks.append(Chunk(piece, kind))
    return chunks


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part.strip() for part in parts if part.strip()]


def pack_sentences(sentences: list[str], max_chars: int) -> list[str]:
    packed: list[str] = []
    buf = ""
    for sentence in sentences:
        for piece in split_long(sentence, max_chars):
            if not buf:
                buf = piece
                continue
            if len(buf) + 1 + len(piece) <= max_chars:
                buf = f"{buf} {piece}"
            else:
                packed.append(buf)
                buf = piece
    if buf:
        packed.append(buf)
    return packed


def split_long(text: str, max_chars: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars or " " not in text:
        return [text]
    window = text[: max_chars + 1]
    for sep in ("; ", ": ", ", ", " "):
        idx = window.rfind(sep)
        if idx < 8:
            continue
        if sep == " ":
            head = text[:idx].strip()
            tail = text[idx + 1 :].strip()
        else:
            head = (text[:idx] + sep.strip()).strip()
            tail = text[idx + len(sep) :].strip()
        if head and tail and head != text:
            return split_long(head, max_chars) + split_long(tail, max_chars)
    return [text]


def clean_line(line: str) -> str:
    text = _HEADING.sub("", line.strip())
    text = _QUOTE.sub("", text)
    text = _BULLET.sub("", text)
    return clean_inline(text)


def clean_inline(text: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.replace("**", "").replace("__", "")
    text = text.replace("`", "")
    text = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def _include(mode: str, section_mode: str | None, hybrid: bool) -> bool:
    if not hybrid or mode == "all":
        return True
    return section_mode != "topicos"


def _mode_name(value: str | None) -> str | None:
    if not value:
        return None
    key = value.strip().lower()
    if key in {"tópicos", "topicos"}:
        return "topicos"
    if key == "literal":
        return "literal"
    return None


def _join(lines: list[str]) -> str:
    return re.sub(r"\s+", " ", " ".join(part.strip() for part in lines if part.strip())).strip()
