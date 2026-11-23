"""Silêncio, remap de tempo e envelope da boca. Sem dependência de rede."""

import re
import struct
import subprocess
import wave
from pathlib import Path


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


def keep_ranges(duration: float, silences: list[tuple[float, float]], pad: float = 0.05) -> list[tuple[float, float]]:
    """Inverte silêncios e guarda um respiro curto nas bordas de cada corte."""
    if duration <= 0:
        return []
    spans: list[list[float]] = []
    cursor = 0.0
    for start, end in silences:
        start = max(0.0, min(duration, start))
        end = max(0.0, min(duration, end))
        if end <= start:
            continue
        if start > cursor + 0.02:
            speech_end = min(duration, start + pad)
            spans.append([cursor, speech_end])
        cursor = max(cursor, end - pad)
    if duration > cursor + 0.02:
        spans.append([cursor, duration])
    merged: list[list[float]] = []
    for start, end in spans:
        if merged and start <= merged[-1][1] + 0.01:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [(round(a, 4), round(b, 4)) for a, b in merged if b - a > 0.04]


def range_duration(ranges: list[tuple[float, float]]) -> float:
    return round(sum(end - start for start, end in ranges), 4)


def remap_time(moment: float, ranges: list[tuple[float, float]]) -> float:
    acc = 0.0
    for start, end in ranges:
        if moment < start:
            return round(acc, 4)
        if moment <= end:
            return round(acc + (moment - start), 4)
        acc += end - start
    return round(acc, 4)


def detect_silences(path: Path, noise: str = "-32dB", minimum: float = 0.28) -> list[tuple[float, float]]:
    result = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(path),
            "-af", f"silencedetect=noise={noise}:d={minimum}",
            "-f", "null", "-",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return parse_silences(result.stderr)


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def mouth_envelope(path: Path, hz: int = 40) -> list[float]:
    raw = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", str(hz), "-f", "s16le", "-"],
        capture_output=True,
        check=True,
    ).stdout
    if not raw:
        return []
    samples = struct.unpack("<" + "h" * (len(raw) // 2), raw[: len(raw) // 2 * 2])
    peak = max(1, max(abs(sample) for sample in samples))
    envelope = []
    for sample in samples:
        level = abs(sample) / peak
        envelope.append(round(min(1.0, level * 1.35), 3))
    return envelope


def write_wav(path: Path, seconds: float, freq: float = 220.0, rate: int = 8000) -> None:
    """Tom curto para testes. Não é a voz de Pedro."""
    import math

    path.parent.mkdir(parents=True, exist_ok=True)
    frames = bytearray()
    total = int(seconds * rate)
    for i in range(total):
        value = int(12000 * math.sin(2 * math.pi * freq * (i / rate)))
        frames += struct.pack("<h", value)
    with wave.open(str(path), "w") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(frames)
