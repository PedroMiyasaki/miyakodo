"""Timestamps palavra a palavra. Whisper em português, nunca modelo .en.

O contrato segue `.agents/skills/media-use/audio/references/transcribe.md`:
modelo sem sufixo `.en` e `--language pt`. Modelo `.en` traduz a fala.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from narrar.audio import probe_duration
from narrar.script import Chunk

WORD_KEYS = ("text", "start", "end")


def guard_whisper_model(model: str) -> str:
    name = (model or "").strip()
    if not name:
        raise ValueError("informe o modelo Whisper, por exemplo small")
    leaf = name.replace("\\", "/").split("/")[-1]
    if leaf.endswith(".en") or ".en." in leaf:
        raise ValueError(
            f"modelo {name} é inglês (.en) e traduz o português. "
            "Use small, medium ou large-v3 com --language pt."
        )
    return name


def canonical_language(value: str) -> str:
    key = (value or "").strip().lower().replace("_", "-")
    if key in {"pt", "pt-br", "portuguese", "português"}:
        return "pt"
    raise ValueError(f"idioma {value} não é português. Use --language pt.")


def whisper_cli_command(audio: Path | str, model: str, language: str, out_dir: Path | str) -> list[str]:
    return [
        "whisper",
        str(audio),
        "--model",
        guard_whisper_model(model),
        "--language",
        canonical_language(language),
        "--word_timestamps",
        "True",
        "--output_format",
        "json",
        "--output_dir",
        str(out_dir),
        "--verbose",
        "False",
    ]


def hyperframes_transcribe_command(audio: Path | str, model: str = "small", language: str = "pt") -> list[str]:
    """Mesma forma documentada em media-use: npx hyperframes transcribe --model --language."""
    return [
        "npx",
        "hyperframes",
        "transcribe",
        str(audio),
        "--model",
        guard_whisper_model(model),
        "--language",
        canonical_language(language),
    ]


def words_from_whisper_payload(payload) -> list[dict]:
    if isinstance(payload, list):
        if payload and isinstance(payload[0], dict) and "start" in payload[0] and "words" not in payload[0]:
            return normalize_words(payload, None)
        segments = payload
    elif isinstance(payload, dict):
        segments = payload.get("segments") or []
    else:
        raise ValueError("transcrição em formato desconhecido")
    raw = []
    for segment in segments:
        if not isinstance(segment, dict):
            continue
        for word in segment.get("words") or []:
            raw.append({
                "text": word.get("text", word.get("word", "")),
                "start": word.get("start", 0),
                "end": word.get("end", 0),
            })
    return normalize_words(raw, None)


def normalize_words(words: list[dict], duration: float | None) -> list[dict]:
    ordered = sorted(words, key=lambda word: (float(word.get("start", 0)), float(word.get("end", word.get("start", 0)))))
    cleaned = []
    last_end = 0.0
    for word in ordered:
        text = str(word.get("text") or word.get("word") or "").strip()
        if not text or text in {"♪", "[silêncio]"}:
            continue
        start = float(word["start"])
        end = float(word.get("end", start))
        if start < last_end:
            start = last_end
        if end <= start:
            end = start + 0.04
        if duration is not None:
            if start >= duration:
                continue
            end = min(end, max(start + 0.02, duration))
            if end > duration:
                end = duration
            if end <= start:
                continue
        item = {"text": text, "start": round(start, 3), "end": round(end, 3)}
        if item["end"] <= item["start"]:
            item["end"] = round(item["start"] + 0.02, 3)
        cleaned.append(item)
        last_end = item["end"]
    return cleaned


def align_chunks(chunks: list[Chunk] | tuple[Chunk, ...], spans: list[tuple[float, float]] | tuple, duration: float | None = None) -> list[dict]:
    raw = []
    for chunk, span in zip(chunks, spans):
        tokens = [token for token in chunk.text.split() if token]
        if not tokens:
            continue
        start, end = span
        width = max(end - start, 0.05 * len(tokens))
        step = width / len(tokens)
        for index, token in enumerate(tokens):
            word_start = start + index * step
            word_end = min(end, word_start + step * 0.92)
            raw.append({"text": token, "start": word_start, "end": word_end})
    return normalize_words(raw, duration)


def transcribe(path: Path | str, model: str = "small", language: str = "pt", runners=None) -> list[dict]:
    model = guard_whisper_model(model)
    language = canonical_language(language)
    attempts = runners or (try_faster_whisper, try_openai_whisper, try_whisper_cli)
    errors = []
    for run in attempts:
        try:
            words = run(Path(path), model, language)
        except ImportError as exc:
            errors.append(str(exc))
            continue
        except FileNotFoundError as exc:
            errors.append(str(exc))
            continue
        if not words:
            raise RuntimeError("Whisper não devolveu palavras. Confira se o áudio tem fala.")
        return normalize_words(words, probe_duration(Path(path)))
    detail = "; ".join(errors) or "nenhum backend de Whisper disponível"
    raise RuntimeError(
        "Não achei Whisper neste ambiente. Instale faster-whisper ou openai-whisper, "
        f"com modelo sem sufixo .en e --language pt. ({detail})"
    )


def try_faster_whisper(path: Path, model: str, language: str) -> list[dict]:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise ImportError("faster-whisper não instalado") from exc
    device = "cpu"
    compute = "int8"
    try:
        import torch

        if torch.cuda.is_available():
            device = "cuda"
            compute = "float16"
    except ImportError:
        pass
    whisper = WhisperModel(model, device=device, compute_type=compute)
    segments, _info = whisper.transcribe(str(path), language=language, word_timestamps=True)
    payload = []
    for segment in segments:
        words = []
        for word in segment.words or []:
            words.append({"word": word.word, "start": word.start, "end": word.end})
        payload.append({"words": words})
    return words_from_whisper_payload({"segments": payload})


def try_openai_whisper(path: Path, model: str, language: str) -> list[dict]:
    try:
        import whisper
    except ImportError as exc:
        raise ImportError("openai-whisper não instalado") from exc
    loaded = whisper.load_model(model)
    result = loaded.transcribe(str(path), language=language, word_timestamps=True, verbose=False)
    return words_from_whisper_payload(result)


def try_whisper_cli(path: Path, model: str, language: str) -> list[dict]:
    with tempfile.TemporaryDirectory() as tmp:
        command = whisper_cli_command(path, model, language, tmp)
        proc = subprocess.run(command, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            if proc.returncode == 127 or "not found" in (proc.stderr or "").lower():
                raise FileNotFoundError("whisper")
            raise RuntimeError((proc.stderr or proc.stdout or "whisper falhou")[-800:])
        json_path = Path(tmp) / f"{path.stem}.json"
        if not json_path.exists():
            found = list(Path(tmp).glob("*.json"))
            if not found:
                raise RuntimeError("o Whisper CLI não gravou o JSON")
            json_path = found[0]
        payload = json.loads(json_path.read_text(encoding="utf-8"))
    return words_from_whisper_payload(payload)


class WhisperAligner:
    def __init__(self, model: str = "small", language: str = "pt"):
        self.model = guard_whisper_model(model)
        self.language = canonical_language(language)

    def __call__(self, wav_path, chunks, spans) -> list[dict]:
        del chunks, spans
        return transcribe(wav_path, model=self.model, language=self.language)


class ProportionalAligner:
    """Reparte o texto falado dentro dos spans da costura. Só para teste, sem GPU."""

    def __init__(self, model: str = "small", language: str = "pt"):
        self.model = guard_whisper_model(model)
        self.language = canonical_language(language)

    def __call__(self, wav_path, chunks, spans) -> list[dict]:
        return align_chunks(chunks, spans, probe_duration(Path(wav_path)))
