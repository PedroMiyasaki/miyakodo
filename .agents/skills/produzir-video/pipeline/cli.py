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
    _copy_static(assets, model["sfx"])
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
            "-an", "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-r", "30", "-pix_fmt", "yuv420p", str(window),
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


def _concat_video(src: Path, ranges, dest: Path) -> None:
    filters, labels = [], []
    for index, (start, end) in enumerate(ranges):
        filters.append(f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{index}]")
        labels.append(f"[v{index}]")
    graph = ";".join(filters) + f";{''.join(labels)}concat=n={len(ranges)}:v=1:a=0[out]"
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
        "-filter_complex", graph, "-map", "[out]", "-pix_fmt", "yuv420p", "-r", "30", str(dest),
    ])


def _copy_static(assets: Path, sfx: list[dict]) -> None:
    for font in (SKILL_DIR / "assets" / "fonts").iterdir():
        if font.suffix.lower() in {".ttf", ".txt"}:
            shutil.copy2(font, assets / "fonts" / font.name)
    shutil.copy2(SKILL_DIR / "assets" / "gsap.min.js", assets / "gsap.min.js")
    shutil.copy2(SKILL_DIR / "assets" / "bed.wav", assets / "bed.wav")
    names = {SFX_FILES[event["name"]] for event in sfx if event["name"] in SFX_FILES}
    for name in names:
        shutil.copy2(SKILL_DIR / "assets" / "sfx" / name, assets / "sfx" / name)
    repo = find_repo(SKILL_DIR)
    logo = repo / "design/logo/png/horizontal/MIYAKODO_HORIZONTAL2.png"
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(logo),
        "-vf", "scale=420:-1", str(assets / "logo.png"),
    ])


def _run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(result.stderr[-2000:] or f"falhou: {' '.join(cmd)}")


def _hyperframes(project: Path, args: list[str]) -> int:
    cmd = ["npx", "--yes", f"hyperframes@{HF}", *args]
    result = subprocess.run(cmd, cwd=project)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
