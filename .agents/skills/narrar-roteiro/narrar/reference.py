"""Recorta 10 a 30 segundos limpos de um vídeo do Pedro para servir de referência."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from narrar.audio import probe_duration

_START = re.compile(r"silence_start:\s*([0-9.]+)")
_END = re.compile(r"silence_end:\s*([0-9.]+)")


def parse_silences(ffmpeg_log: str) -> list[tuple[float, float]]:
    pending = None
    found = []
    for line in ffmpeg_log.splitlines():
        start = _START.search(line)
        if start:
            pending = float(start.group(1))
            continue
        end = _END.search(line)
        if end and pending is not None:
            stop = float(end.group(1))
            if stop > pending:
                found.append((pending, stop))
            pending = None
    return found


def speech_spans(duration: float, silences: list[tuple[float, float]]) -> list[tuple[float, float]]:
    spans = []
    cursor = 0.0
    for start, end in silences:
        start = max(0.0, min(duration, start))
        end = max(start, min(duration, end))
        if start > cursor + 0.05:
            spans.append((cursor, start))
        cursor = max(cursor, end)
    if duration > cursor + 0.05:
        spans.append((cursor, duration))
    return spans


def pick_window(
    duration: float,
    silences: list[tuple[float, float]],
    target: float = 18.0,
    minimum: float = 10.0,
    maximum: float = 30.0,
) -> tuple[float, float]:
    """Escolhe um trecho contínuo de fala, de preferência perto de `target` segundos."""
    if duration <= 0:
        raise ValueError("duração inválida")
    goal = min(maximum, max(min(minimum, duration), min(target, duration)))
    spans = speech_spans(duration, silences)
    if not spans:
        return 0.0, round(min(duration, goal), 3)
    usable = [span for span in spans if span[1] - span[0] >= minimum - 0.05]
    pool = usable or spans

    def score(span: tuple[float, float]) -> tuple[float, float]:
        length = span[1] - span[0]
        return (abs(length - target), -length)

    start, end = min(pool, key=score)
    take = min(end - start, target, maximum)
    return round(start, 3), round(take, 3)


def reference_audio_filter() -> str:
    trim = "silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.05"
    return (
        "highpass=f=80,"
        f"areverse,{trim},"
        f"areverse,{trim},"
        "loudnorm=I=-16:TP=-1.5:LRA=11"
    )


def silencedetect_command(src: Path) -> list[str]:
    return [
        "ffmpeg", "-hide_banner", "-i", str(src),
        "-af", "silencedetect=noise=-35dB:d=0.3",
        "-f", "null", "-",
    ]


def ffmpeg_extract_command(src: Path, dst: Path, start: float, duration: float, sample_rate: int = 24000) -> list[str]:
    return [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src),
        "-ss", f"{start:.3f}",
        "-t", f"{duration:.3f}",
        "-vn", "-ac", "1", "-ar", str(sample_rate),
        "-af", reference_audio_filter(),
        str(dst),
    ]


def extract_reference(
    src: Path,
    dst: Path,
    *,
    start: float | None = None,
    duration: float | None = None,
    target: float = 18.0,
    minimum: float = 10.0,
    maximum: float = 30.0,
    transcribe_ref: bool = False,
    transcript_out: Path | None = None,
    whisper_model: str = "small",
    language: str = "pt",
) -> dict:
    if not src.is_file():
        raise ValueError(f"não achei o vídeo {src}")
    total = probe_duration(src)
    chosen_start = start
    chosen_duration = duration
    if chosen_start is None:
        log = subprocess.run(silencedetect_command(src), capture_output=True, text=True, check=False)
        silences = parse_silences(log.stderr or "")
        chosen_start, chosen_duration = pick_window(
            total, silences, target=target, minimum=minimum, maximum=maximum,
        )
    elif chosen_duration is None:
        chosen_duration = min(target, max(0.5, total - chosen_start))
    if chosen_duration <= 0:
        raise ValueError("a janela de referência ficou vazia")
    dst.parent.mkdir(parents=True, exist_ok=True)
    command = ffmpeg_extract_command(src, dst, chosen_start, chosen_duration)
    rendered = subprocess.run(command, capture_output=True, text=True, check=False)
    if rendered.returncode != 0:
        raise RuntimeError(rendered.stderr.strip() or "ffmpeg falhou ao extrair a referência")
    output_duration = probe_duration(dst)
    result = {
        "start": chosen_start,
        "duration": chosen_duration,
        "path": dst,
        "output_duration": output_duration,
        "source_duration": total,
    }
    if transcribe_ref or transcript_out:
        from narrar.align import transcribe

        words = transcribe(dst, model=whisper_model, language=language)
        text = " ".join(word["text"] for word in words).strip()
        target_path = transcript_out or dst.with_suffix(".txt")
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(text + "\n", encoding="utf-8")
        result["transcript"] = target_path
    return result
