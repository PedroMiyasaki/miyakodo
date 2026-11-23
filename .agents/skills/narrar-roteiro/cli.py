"""CLI da narração local.

  python cli.py texto ROTEIRO.md --mode auto
  python cli.py narrar ROTEIRO.md --ref video/inputs/voice-ref/pedro.wav --ref-text video/inputs/voice-ref/pedro.txt
  python cli.py extrair-referencia video/inputs/headless-software.MP4 --out video/inputs/voice-ref/pedro.wav
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from narrar.align import ProportionalAligner, WhisperAligner  # noqa: E402
from narrar.mock import MockVoice  # noqa: E402
from narrar.pipeline import find_repo, narrate  # noqa: E402
from narrar.reference import extract_reference  # noqa: E402
from narrar.script import prepare_speech, render_preview  # noqa: E402


def main(argv=None) -> int:
    _utf8_stdio()
    parser = argparse.ArgumentParser(description="Narra um roteiro com a voz clonada do Pedro, na GPU local.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    texto = sub.add_parser("texto", help="Mostra só o que seria falado, sem sintetizar.")
    _add_script_args(texto)

    narrar = sub.add_parser("narrar", help="Gera voice.wav e words.json.")
    _add_script_args(narrar)
    narrar.add_argument("--ref", required=True, help="WAV de referência, 10 a 30 segundos.")
    narrar.add_argument("--ref-text", help="Transcrição literal da referência, ou caminho de um .txt.")
    narrar.add_argument("--out", help="Pasta de saída. O padrão é video/outputs/narracao/<slug>.")
    narrar.add_argument("--device", default="auto", help="auto, cpu, cuda ou cuda:0.")
    narrar.add_argument("--dtype", default="auto", choices=("auto", "bfloat16", "float16", "float32"))
    narrar.add_argument("--attn", default="auto", choices=("auto", "sdpa", "flash_attention_2", "eager"))
    narrar.add_argument("--whisper-model", default="small", help="small, medium ou large-v3. Nunca .en.")
    narrar.add_argument("--language", default="pt")
    narrar.add_argument("--backend", default="qwen", choices=("qwen", "mock"))
    narrar.add_argument("--align", default=None, choices=("whisper", "mock"))
    narrar.add_argument("--no-loudnorm", action="store_true")
    narrar.add_argument("--no-snippet", action="store_true")
    narrar.add_argument("--x-vector-only", action="store_true", help="Ignora a transcrição e clona só pelo embedding.")
    narrar.add_argument("--sentence-pause", type=float, default=0.28)
    narrar.add_argument("--paragraph-pause", type=float, default=0.52)
    narrar.add_argument("--beat-pause", type=float, default=0.75)
    narrar.add_argument("--crossfade-ms", type=float, default=15.0)

    extrair = sub.add_parser("extrair-referencia", help="Recorta uma amostra limpa de um vídeo do Pedro.")
    extrair.add_argument("video")
    extrair.add_argument("--out", required=True)
    extrair.add_argument("--start", type=float, default=None, help="Segundos. Sem isso, a janela é escolhida pelo silêncio.")
    extrair.add_argument("--duration", type=float, default=None, help="Duração do corte. O padrão automático é 18 s.")
    extrair.add_argument("--target", type=float, default=18.0)
    extrair.add_argument("--transcribe", action="store_true", help="Gera a transcrição com Whisper, --language pt.")
    extrair.add_argument("--transcript-out")
    extrair.add_argument("--whisper-model", default="small")
    extrair.add_argument("--language", default="pt")

    args = parser.parse_args(argv)
    try:
        if args.cmd == "texto":
            return cmd_texto(args)
        if args.cmd == "narrar":
            return cmd_narrar(args)
        return cmd_extrair(args)
    except (ValueError, RuntimeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


def cmd_texto(args) -> int:
    speech = prepare_speech(Path(args.roteiro).read_text(encoding="utf-8"), mode=args.mode, max_chars=args.max_chars)
    sys.stdout.write(render_preview(speech.chunks))
    if speech.chunks:
        sys.stdout.write("\n")
    return 0


def cmd_narrar(args) -> int:
    roteiro = Path(args.roteiro)
    repo = find_repo(roteiro.resolve())
    out = Path(args.out) if args.out else _default_out(repo, roteiro)
    align_name = args.align or ("mock" if args.backend == "mock" else "whisper")
    backend = _backend(args)
    aligner = _aligner(align_name, args.whisper_model, args.language)
    narrate(
        roteiro,
        Path(args.ref),
        out,
        ref_text=resolve_ref_text(args.ref_text),
        mode=args.mode,
        backend=backend,
        aligner=aligner,
        repo=repo,
        max_chars=args.max_chars,
        sentence_pause=args.sentence_pause,
        paragraph_pause=args.paragraph_pause,
        beat_pause=args.beat_pause,
        crossfade_ms=args.crossfade_ms,
        loudnorm=not args.no_loudnorm,
        snippet=not args.no_snippet,
        x_vector_only=args.x_vector_only,
    )
    return 0


def cmd_extrair(args) -> int:
    transcript = Path(args.transcript_out) if args.transcript_out else None
    result = extract_reference(
        Path(args.video),
        Path(args.out),
        start=args.start,
        duration=args.duration,
        target=args.target,
        transcribe_ref=args.transcribe or transcript is not None,
        transcript_out=transcript,
        whisper_model=args.whisper_model,
        language=args.language,
    )
    print(
        f"inicio {result['start']:.3f}s, janela {result['duration']:.3f}s, "
        f"amostra {result['output_duration']:.3f}s, arquivo {result['path']}"
    )
    if result["output_duration"] < 8:
        print("amostra curta. O clone fica melhor entre 10 e 30 segundos de fala limpa.", file=sys.stderr)
    if "transcript" in result:
        print(f"transcrição {result['transcript']}")
    return 0


def resolve_ref_text(value: str | None) -> str | None:
    if value is None or not str(value).strip():
        return None
    raw = str(value).strip()
    path = Path(raw)
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    if raw.endswith(".txt") or "/" in raw or "\\" in raw:
        raise ValueError(f"não achei a transcrição em {raw}")
    return raw


def _add_script_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("roteiro")
    parser.add_argument("--mode", default="auto", choices=("auto", "literal", "all"))
    parser.add_argument("--max-chars", type=int, default=240)


def _backend(args):
    if args.backend == "mock":
        return MockVoice()
    from narrar.tts import QwenVoice

    return QwenVoice(device=args.device, dtype=args.dtype, attn=args.attn)


def _aligner(name: str, model: str, language: str):
    if name == "mock":
        return ProportionalAligner(model=model, language=language)
    if name == "whisper":
        return WhisperAligner(model=model, language=language)
    raise ValueError(f"alinhador desconhecido: {name}")


def _default_out(repo: Path | None, roteiro: Path) -> Path:
    slug = roteiro.stem
    if repo is not None:
        return repo / "video" / "outputs" / "narracao" / slug
    return roteiro.parent / "narracao" / slug


def _utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass


if __name__ == "__main__":
    raise SystemExit(main())
