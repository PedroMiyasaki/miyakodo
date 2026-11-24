"""Liga parser, clonagem, costura, loudness e words.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from narrar.align import normalize_words
from narrar.audio import apply_loudnorm, probe_duration, stitch, write_wav
from narrar.script import prepare_speech


def find_repo(start: Path) -> Path | None:
    for candidate in [start, *start.parents]:
        if (candidate / "AGENTS.md").exists() and (candidate / "design").is_dir():
            return candidate
    return None


def relative_to_repo(path: Path, repo: Path | None) -> str:
    resolved = path.resolve()
    if repo is not None:
        try:
            return resolved.relative_to(repo.resolve()).as_posix()
        except ValueError:
            pass
    return resolved.as_posix()


def narrate(
    roteiro: Path,
    ref_audio: Path,
    out_dir: Path,
    *,
    ref_text: str | None,
    mode: str,
    backend,
    aligner,
    repo: Path | None = None,
    max_chars: int = 240,
    sentence_pause: float = 0.28,
    paragraph_pause: float = 0.52,
    beat_pause: float = 0.75,
    crossfade_ms: float = 15.0,
    loudnorm: bool = True,
    snippet: bool = True,
    x_vector_only: bool = False,
    log=None,
) -> dict:
    if not roteiro.is_file():
        raise ValueError(f"não achei o roteiro {roteiro}")
    if not ref_audio.is_file():
        raise ValueError(f"não achei a referência de voz {ref_audio}")
    speech = prepare_speech(roteiro.read_text(encoding="utf-8"), mode=mode, max_chars=max_chars)
    if not speech.chunks:
        raise ValueError("nada para narrar. O modo literal ignora blocos de tópicos.")
    use_vector = x_vector_only or not (ref_text and ref_text.strip())
    if use_vector:
        _say(
            "sem transcrição da referência: clonagem só pelo embedding (x_vector_only). "
            "Com o texto literal da amostra o timbre fica mais estável.",
            log,
        )
    runtime = getattr(backend, "runtime", None)
    if runtime:
        _say(f"runtime: {runtime[0]}, {runtime[1]}, {runtime[2]}", log)
    _say(f"chunks: {len(speech.chunks)}", log)
    pieces = []
    sample_rate = None
    try:
        backend.prepare(str(ref_audio.resolve()), None if use_vector else ref_text.strip(), use_vector)
        for chunk in speech.chunks:
            samples, this_rate = backend.synthesize(chunk.text)
            if sample_rate is None:
                sample_rate = this_rate
            elif this_rate != sample_rate:
                raise RuntimeError("o sample rate mudou entre chunks")
            pieces.append((samples, chunk.break_after))
    finally:
        closer = getattr(backend, "close", None)
        if closer:
            closer()
    if sample_rate is None:
        raise RuntimeError("nenhum chunk foi sintetizado")
    stitched = stitch(
        pieces,
        sample_rate,
        sentence_pause=sentence_pause,
        paragraph_pause=paragraph_pause,
        beat_pause=beat_pause,
        crossfade_ms=crossfade_ms,
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    voice_path = out_dir / "voice.wav"
    write_wav(voice_path, stitched.samples, stitched.sample_rate)
    if loudnorm:
        apply_loudnorm(voice_path)
    duration = probe_duration(voice_path)
    words = aligner(voice_path, speech.chunks, stitched.spans)
    words = normalize_words(words, duration)
    if not words:
        raise RuntimeError("a narração saiu sem timestamps")
    words_path = out_dir / "words.json"
    words_path.write_text(json.dumps(words, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    snippet_path = None
    if snippet:
        payload = {
            "mode": "sem-gravacao",
            "voice": {
                "src": relative_to_repo(voice_path, repo),
                "in": 0,
                "out": round(duration, 3),
            },
            "words": words,
        }
        snippet_path = out_dir / "produzir-video.snippet.json"
        snippet_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _say(f"voz: {voice_path}", log)
    _say(f"words: {words_path}", log)
    return {
        "out_dir": out_dir,
        "voice": voice_path,
        "words": words_path,
        "snippet": snippet_path,
        "chunks": len(speech.chunks),
        "duration": duration,
        "sample_rate": probe_wav_rate(voice_path),
        "x_vector_only": use_vector,
        "speech": speech,
    }


def probe_wav_rate(path: Path) -> int:
    import wave

    with wave.open(str(path), "r") as handle:
        return handle.getframerate()


def _say(message: str, log) -> None:
    if log is None:
        print(message, file=sys.stderr)
    else:
        log(message)
