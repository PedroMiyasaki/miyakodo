"""Costura PCM, WAV e loudness de Reel (-16 LUFS, -1 dBTP)."""

from __future__ import annotations

import array
import json
import subprocess
import sys
import wave
from dataclasses import dataclass
from pathlib import Path

TARGET_I = -16.0
TARGET_TP = -1.0
TARGET_LRA = 11.0
DELIVERY_RATE = 48000


@dataclass(frozen=True)
class StitchResult:
    samples: array.array
    sample_rate: int
    spans: tuple[tuple[float, float], ...]

    @property
    def duration(self) -> float:
        if self.sample_rate <= 0:
            return 0.0
        return len(self.samples) / self.sample_rate


def stitch(
    pieces: list[tuple[array.array, str]],
    sample_rate: int,
    *,
    sentence_pause: float = 0.28,
    paragraph_pause: float = 0.52,
    beat_pause: float = 0.75,
    crossfade_ms: float = 15.0,
    tail_s: float = 0.12,
) -> StitchResult:
    """Junta os chunks. A borda de cada um desce até o silêncio da pausa, sem clique."""
    if sample_rate <= 0:
        raise ValueError("sample rate inválido")
    pauses = {
        "sentence": sentence_pause,
        "paragraph": paragraph_pause,
        "beat": beat_pause,
        "end": 0.0,
    }
    fade_n = max(0, int(round(sample_rate * (crossfade_ms / 1000.0))))
    out: array.array = array.array("h")
    spans: list[tuple[float, float]] = []
    last = len(pieces) - 1
    for index, (samples, kind) in enumerate(pieces):
        chunk = array.array("h", samples)
        fade_edges(chunk, min(fade_n, len(chunk) // 2))
        start = len(out) / sample_rate
        out.extend(chunk)
        spans.append((start, len(out) / sample_rate))
        if index < last:
            gap_n = int(round(sample_rate * pauses.get(kind, sentence_pause)))
            if gap_n > 0:
                out.extend(array.array("h", [0]) * gap_n)
    tail_n = int(round(sample_rate * tail_s))
    if tail_n > 0:
        out.extend(array.array("h", [0]) * tail_n)
    return StitchResult(out, sample_rate, tuple(spans))


def fade_edges(samples: array.array, fade: int) -> None:
    if fade <= 0:
        return
    last = len(samples) - 1
    for index in range(fade):
        gain = index / fade
        samples[index] = int(samples[index] * gain)
        samples[last - index] = int(samples[last - index] * gain)


def pcm_from_sequence(samples) -> array.array:
    flat: list[float] = []

    def walk(node) -> None:
        if hasattr(node, "detach"):
            node = node.detach().cpu().numpy()
        if hasattr(node, "reshape") and not isinstance(node, (str, bytes)):
            node = node.reshape(-1).tolist()
        if isinstance(node, (list, tuple)):
            for item in node:
                walk(item)
            return
        flat.append(float(node))

    walk(samples)
    out: array.array = array.array("h")
    for value in flat:
        clamped = max(-1.0, min(1.0, value))
        out.append(int(round(clamped * 32767.0)))
    return out


def write_wav(path: Path, samples: array.array, sample_rate: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = samples
    if sys.byteorder != "little":
        payload = array.array("h", samples)
        payload.byteswap()
    with wave.open(str(path), "w") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(payload.tobytes())


def read_wav(path: Path) -> tuple[array.array, int]:
    with wave.open(str(path), "r") as handle:
        if handle.getnchannels() != 1 or handle.getsampwidth() != 2:
            raise RuntimeError(f"{path} precisa ser WAV mono de 16 bits")
        data: array.array = array.array("h")
        data.frombytes(handle.readframes(handle.getnframes()))
        if sys.byteorder != "little":
            data.byteswap()
        return data, handle.getframerate()


def probe_duration(path: Path) -> float:
    try:
        _samples, rate = read_wav(path)
        return len(_samples) / rate
    except (wave.Error, EOFError, RuntimeError):
        pass
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        raise RuntimeError(f"não medi a duração de {path}")
    return float(proc.stdout.strip())


def loudnorm_filter(stats: dict | None = None) -> str:
    base = f"loudnorm=I={TARGET_I:g}:TP={TARGET_TP:g}:LRA={TARGET_LRA:g}"
    if not stats:
        return base
    return (
        f"{base}:measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
        f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:"
        f"offset={stats['target_offset']}:linear=true"
    )


def parse_loudnorm_stats(stderr: str) -> dict:
    start = stderr.rfind("{")
    end = stderr.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("loudnorm não devolveu medição")
    return json.loads(stderr[start : end + 1])


def apply_loudnorm(path: Path, sample_rate: int = DELIVERY_RATE) -> Path:
    """Duas passadas. O arquivo final fica mono, 48 kHz, -16 LUFS, teto de -1 dBTP."""
    measure = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(path),
            "-af", loudnorm_filter() + ":print_format=json",
            "-f", "null", "-",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if measure.returncode != 0:
        raise RuntimeError(measure.stderr[-800:] or "ffmpeg não mediu o loudness")
    try:
        stats = parse_loudnorm_stats(measure.stderr)
        audio_filter = loudnorm_filter(stats)
    except (ValueError, KeyError, json.JSONDecodeError):
        audio_filter = loudnorm_filter()
    destination = path.with_suffix(".norm.wav")
    rendered = subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(path),
            "-af", audio_filter,
            "-ar", str(sample_rate),
            "-ac", "1",
            "-c:a", "pcm_s16le",
            str(destination),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if rendered.returncode != 0:
        raise RuntimeError(rendered.stderr[-800:] or "ffmpeg não normalizou o áudio")
    destination.replace(path)
    return path


def measure_loudness(path: Path) -> dict:
    proc = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(path),
            "-af", loudnorm_filter() + ":print_format=json",
            "-f", "null", "-",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[-800:] or "ffmpeg não mediu o loudness")
    return parse_loudnorm_stats(proc.stderr)
