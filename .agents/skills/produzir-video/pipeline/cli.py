"""Gera o projeto HyperFrames e dispara check/render.

Uso:
  python pipeline/cli.py build roteiro.json [--out DIR]
  python pipeline/cli.py check DIR
  python pipeline/cli.py render DIR --output arquivo.mp4 [--quality draft|looks]
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.audio import detect_silences, keep_ranges, mouth_envelope, probe_duration, range_duration
from pipeline.brand import SFX_FILES
from pipeline.compile import compile_script
from pipeline.compose import render_html

HF = "0.8.169"
SKILL_DIR = Path(__file__).resolve().parents[1]


def _scene_tipo(scene: dict) -> str:
    if scene.get("type") == "stack":
        kids = "+".join(str(child.get("type")) for child in scene.get("children") or [])
        return f"stack:{kids}"
    return str(scene.get("type"))


def find_repo(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "AGENTS.md").exists() and (candidate / "design").is_dir():
            return candidate
    raise SystemExit("não achei a raiz do repositório (AGENTS.md + design/)")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Pipeline de vídeo Miyakodo")
    sub = parser.add_subparsers(dest="cmd", required=True)
    build = sub.add_parser("build")
    build.add_argument("roteiro")
    build.add_argument("--out")
    check = sub.add_parser("check")
    check.add_argument("project")
    render = sub.add_parser("render")
    render.add_argument("project")
    render.add_argument("--output", required=True)
    render.add_argument("--quality", default="draft", choices=("draft", "looks", "delivery"))
    args = parser.parse_args(argv)
    repo = find_repo(SKILL_DIR)
    if args.cmd == "build":
        out = build_project(Path(args.roteiro), Path(args.out) if args.out else None, repo)
        print(out)
        return 0
    project = Path(args.project).resolve()
    if args.cmd == "check":
        return _hyperframes(project, ["check"])
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    return _hyperframes(project, ["render", "--quality", args.quality, "--output", str(output)])


def build_project(roteiro_path: Path, out: Path | None, repo: Path) -> Path:
    data = json.loads(roteiro_path.resolve().read_text(encoding="utf-8"))
    slug = str(data.get("slug") or roteiro_path.stem)
    target = out or (repo / "video" / "projects" / slug)
    if target.exists():
        shutil.rmtree(target)
    assets = target / "assets"
    (assets / "fonts").mkdir(parents=True)
    (assets / "sfx").mkdir()
    cuts, mouth = _media(data, assets, repo)
    model = compile_script(data, cuts=cuts, mouth=mouth)
    _copy_static(assets, model["sfx"], model["duration"])
    origem = round(float(data["voice"]["out"]) - float(data["voice"]["in"]), 3)
    mantidos = [{"in": a, "out": b} for a, b in (cuts or [(0.0, origem)])]
    removidos = []
    cursor = 0.0
    for trecho in mantidos:
        if trecho["in"] > cursor + 0.02:
            removidos.append({"in": round(cursor, 3), "out": round(trecho["in"], 3)})
        cursor = trecho["out"]
    if origem > cursor + 0.02:
        removidos.append({"in": round(cursor, 3), "out": origem})
    (target / "cortes.json").write_text(json.dumps({
        "origem_segundos": origem,
        "duracao_segundos": model["duration"],
        "removido_segundos": round(origem - model["duration"], 3),
        "silencios_removidos": removidos,
        "cenas_na_timeline_editada": [
            {
                "inicio": beat["start"],
                "fim": beat["end"],
                "layout": beat["layout"],
                "label": beat["label"],
                "tipo": _scene_tipo(beat["scene"]),
            }
            for beat in model["beats"]
        ],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (target / "index.html").write_text(render_html(model), encoding="utf-8")
    (target / "hyperframes.json").write_text(json.dumps({
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
        "paths": {"assets": "assets"},
    }, indent=2) + "\n", encoding="utf-8")
    (target / "package.json").write_text(json.dumps({
        "name": model["slug"],
        "private": True,
        "type": "module",
        "scripts": {
            "check": f"npx --yes hyperframes@{HF} check",
            "render": f"npx --yes hyperframes@{HF} render",
        },
    }, indent=2) + "\n", encoding="utf-8")
    (target / "meta.json").write_text(json.dumps({
        "mode": model["mode"],
        "purpose": model["purpose"],
        "duration": model["duration"],
        "slug": model["slug"],
    }, indent=2) + "\n", encoding="utf-8")
    return target


def _media(data: dict, assets: Path, repo: Path):
    voice = data.get("voice") or {}
    src = repo / voice["src"]
    if not src.exists():
        raise SystemExit(f"voz não encontrada: {src}")
    start, end = float(voice["in"]), float(voice["out"])
    sliced = assets / "voice-window.wav"
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", str(start), "-to", str(end), "-i", str(src),
        "-ac", "1", "-ar", "44100", str(sliced),
    ])
    mode = data.get("mode")
    cuts = None
    voice_out = assets / "voice.wav"
    if mode == "gravacao":
        duration = probe_duration(sliced)
        silences = detect_silences(sliced)
        ranges = keep_ranges(duration, silences)
        removed = duration - range_duration(ranges)
        if ranges and removed > 0.12:
            cuts = ranges
            _concat_audio(sliced, ranges, voice_out)
        else:
            shutil.copy2(sliced, voice_out)
        footage = _footage(data, assets, repo, start, end, duration)
        if cuts:
            _concat_video(footage, cuts, assets / "footage.mp4")
            footage.unlink(missing_ok=True)
        elif footage.name != "footage.mp4":
            footage.replace(assets / "footage.mp4")
        mouth = []
    else:
        shutil.copy2(sliced, voice_out)
        mouth = mouth_envelope(voice_out)
    sliced.unlink(missing_ok=True)
    return cuts, mouth


def _footage(data, assets, repo, start, end, duration):
    spec = data.get("footage") or {}
    window = assets / "footage-window.mp4"
    if spec.get("src"):
        source = repo / spec["src"]
        if not source.exists():
            raise SystemExit(f"vídeo bruto não encontrado: {source}")
        _run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", str(start), "-to", str(end), "-i", str(source),
            "-an", "-vf", _video_filter(source),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            str(window),
        ])
        return window
    still = spec.get("still")
    if not still:
        raise SystemExit("modo gravacao precisa de footage.src ou footage.still")
    image = repo / still
    if not image.exists():
        raise SystemExit(f"still não encontrada: {image}")
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-framerate", "30", "-t", f"{duration:.3f}", "-i", str(image),
        "-vf", f"scale=1180:2098,crop=1080:1920:x='20+36*t/{duration:.3f}':y='24+28*t/{duration:.3f}'",
        "-r", "30", "-pix_fmt", "yuv420p", "-an", str(window),
    ])
    return window


def _concat_audio(src: Path, ranges, dest: Path) -> None:
    filters, labels = [], []
    for index, (start, end) in enumerate(ranges):
        filters.append(f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{index}]")
        labels.append(f"[a{index}]")
    graph = ";".join(filters) + f";{''.join(labels)}concat=n={len(ranges)}:v=0:a=1[out]"
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
        "-filter_complex", graph, "-map", "[out]", str(dest),
    ])


def _video_filter(source: Path) -> str:
    base = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30"
    if not _is_hdr(source):
        return base
    return (
        base
        + ",zscale=tin=arib-std-b67:t=linear:npl=100,format=gbrpf32le,"
        + "zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
    )


def _is_hdr(source: Path) -> bool:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=color_transfer,color_primaries",
            "-of", "default=nw=1", str(source),
        ],
        capture_output=True, text=True, check=False,
    )
    text = result.stdout.lower()
    return any(token in text for token in ("arib-std-b67", "smpte2084", "bt2020"))


def _concat_video(src: Path, ranges, dest: Path) -> None:
    """Corta em lotes. Um filtro com dezenas de trims estoura a memória."""
    if not ranges:
        raise SystemExit("sem trechos para montar o vídeo")
    work = dest.parent / "_segs"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    parts = []
    step = 4
    for offset in range(0, len(ranges), step):
        group = list(ranges[offset:offset + step])
        part = work / f"part-{offset:02d}.mp4"
        _concat_video_filter(src, group, part)
        parts.append(part)
    if len(parts) == 1:
        parts[0].replace(dest)
    else:
        listing = work / "list.txt"
        listing.write_text("".join(f"file '{part.as_posix()}'\n" for part in parts), encoding="utf-8")
        _run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(listing),
            "-c", "copy", str(dest),
        ])
    shutil.rmtree(work, ignore_errors=True)


def _concat_video_filter(src: Path, ranges, dest: Path) -> None:
    filters, labels = [], []
    for index, (start, end) in enumerate(ranges):
        filters.append(f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{index}]")
        labels.append(f"[v{index}]")
    graph = ";".join(filters) + f";{''.join(labels)}concat=n={len(ranges)}:v=1:a=0[out]"
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
        "-filter_complex", graph, "-map", "[out]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", "30", str(dest),
    ])


def _copy_static(assets: Path, sfx: list[dict], duration: float) -> None:
    for font in (SKILL_DIR / "assets" / "fonts").iterdir():
        if font.suffix.lower() in {".ttf", ".txt"}:
            shutil.copy2(font, assets / "fonts" / font.name)
    shutil.copy2(SKILL_DIR / "assets" / "gsap.min.js", assets / "gsap.min.js")
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-stream_loop", "-1", "-i", str(SKILL_DIR / "assets" / "bed.wav"),
        "-t", f"{max(duration, 0.5):.3f}",
        "-ac", "1", "-ar", "44100", str(assets / "bed.wav"),
    ])
    names = {SFX_FILES[event["name"]] for event in sfx if event["name"] in SFX_FILES}
    for name in names:
        shutil.copy2(SKILL_DIR / "assets" / "sfx" / name, assets / "sfx" / name)
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", "color=c=0x8a8178:s=96x96,noise=alls=24:allf=t",
        "-frames:v", "1", str(assets / "noise.png"),
    ])
    repo = find_repo(SKILL_DIR)
    pedro = assets / "pedro"
    pedro.mkdir(exist_ok=True)
    for png in (SKILL_DIR / "assets" / "pedro").glob("*.png"):
        shutil.copy2(png, pedro / png.name)
    carlos = assets / "carlos"
    carlos.mkdir(exist_ok=True)
    mascotes = repo / "design" / "mascote-e-textura" / "png"
    for png in sorted(mascotes.glob("MASCOTE_*.png")):
        _run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(png), "-vf", "scale=720:-1",
            str(carlos / png.name),
        ])
    logo = repo / "design/logo/png/horizontal/MIYAKODO_HORIZONTAL2.png"
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(logo),
        "-vf", "scale=420:-1", str(assets / "logo.png"),
    ])


def _run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise SystemExit(f"exit {result.returncode}: {detail[-1500:] or cmd[0]}")


def _hyperframes(project: Path, args: list[str]) -> int:
    extra = []
    if args and args[0] == "render":
        extra = ["--browser-timeout", "180", "--player-ready-timeout", "120000", "--workers", "2", "--sdr"]
    cmd = ["npx", "--yes", f"hyperframes@{HF}", *args, *extra]
    result = subprocess.run(cmd, cwd=project)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
