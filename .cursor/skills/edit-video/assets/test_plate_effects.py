"""Self-check for plate effects (zoom-emphasis / black-and-white).

Renders synthetic clips through the real filter chain and asserts the two hard
rules the feature specs state:

  - a zoom always lands back at 1.0x by its end_in_output
  - a B&W window is grey inside and coloured outside

Run:
  PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
    python .claude/skills/edit-video/assets/test_plate_effects.py
"""
from __future__ import annotations

import subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from render_vertical import apply_plate_effects, build_plate_filter  # noqa: E402

W, H = 320, 240


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def _make_source(path: Path, kind: str, seconds: float = 3.0) -> None:
    """A frozen frame: every timestamp holds the same image, so any difference
    downstream is the effect and nothing else."""
    src = (f"color=c=orange:s={W}x{H}" if kind == "solid"
           else f"testsrc=size={W}x{H}")
    with tempfile.TemporaryDirectory() as td:
        frame = Path(td) / "f.png"
        _run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"{src}:rate=24",
              "-frames:v", "1", str(frame)])
        _run(["ffmpeg", "-y", "-v", "error",
              "-loop", "1", "-i", str(frame),
              "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
              "-t", f"{seconds}", "-r", "24", "-pix_fmt", "yuv420p",
              "-c:v", "libx264", "-crf", "12", "-c:a", "aac", str(path)])


def _frame(video: Path, t: float, out: Path, scale: str | None = None) -> Path:
    cmd = ["ffmpeg", "-y", "-v", "error", "-ss", f"{t}", "-i", str(video), "-frames:v", "1"]
    if scale:
        cmd += ["-vf", scale]
    _run(cmd + [str(out)])
    return out


def _rgb(video: Path, t: float, td: Path) -> tuple[int, int, int]:
    """Average colour of the whole frame, as one pixel."""
    png = _frame(video, t, td / f"c{t}.png", scale="scale=1:1")
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(png), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        check=True, capture_output=True).stdout
    return raw[0], raw[1], raw[2]


def _psnr(a: Path, b: Path) -> float:
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(a), "-i", str(b), "-lavfi", "psnr", "-f", "null", "-"],
        check=True, capture_output=True, text=True).stderr
    tag = out.rsplit("average:", 1)[1].split()[0]
    return float("inf") if tag.startswith("inf") else float(tag)


def test_bw_window(td: Path) -> None:
    src, out = td / "solid.mp4", td / "solid_bw.mp4"
    _make_source(src, "solid")
    apply_plate_effects(
        src, [{"type": "preto_e_branco", "start_in_output": 1.0, "end_in_output": 2.0}],
        W, H, out, preview=True)

    r, g, b = _rgb(out, 0.3, td)
    assert max(r, g, b) - min(r, g, b) > 40, f"outside the window should stay coloured, got {(r,g,b)}"
    r, g, b = _rgb(out, 1.5, td)
    assert max(r, g, b) - min(r, g, b) <= 8, f"inside the window should be grey, got {(r,g,b)}"
    print("  ok  B&W: coloured outside, grey inside")


def _assert_zoom_resets(td: Path, effect: dict, peak_t: float, label: str) -> None:
    src, out = td / f"p_{label}.mp4", td / f"p_{label}_z.mp4"
    _make_source(src, "pattern")
    apply_plate_effects(src, [effect], W, H, out, preview=True)

    ref = _frame(src, 0.5, td / f"ref_{label}.png")
    at_peak = _psnr(_frame(out, peak_t, td / f"pk_{label}.png"), ref)
    end = float(effect["end_in_output"])
    at_end = _psnr(_frame(out, end - 0.02, td / f"en_{label}.png"), ref)

    assert at_peak < 30, f"{label}: no visible zoom at peak (psnr {at_peak:.1f} dB)"
    assert at_end > 38, f"{label}: did not reset to 1.0x by end_in_output (psnr {at_end:.1f} dB)"
    print(f"  ok  zoom {label}: peak {at_peak:.1f} dB, back to 1.0x at end {at_end:.1f} dB")


def test_zoom_resets(td: Path) -> None:
    _assert_zoom_resets(
        td, {"type": "zoom_enfase", "mode": "fast", "start_in_output": 1.0,
             "end_in_output": 2.2, "land_at": 1.5}, peak_t=1.6, label="fast")
    _assert_zoom_resets(
        td, {"type": "zoom_enfase", "mode": "slow", "start_in_output": 0.5,
             "end_in_output": 2.5, "scale_peak": 1.10}, peak_t=1.9, label="slow")


def test_guards() -> None:
    try:
        build_plate_filter([{"type": "flip_it", "start_in_output": 0, "end_in_output": 1}], W, H)
    except SystemExit:
        print("  ok  unknown effect type rejected")
    else:
        raise AssertionError("unknown plate_effect type should be rejected")

    overlapping = [
        {"type": "zoom_enfase", "mode": "slow", "start_in_output": 1.0, "end_in_output": 3.0},
        {"type": "zoom_enfase", "mode": "slow", "start_in_output": 2.0, "end_in_output": 4.0},
    ]
    try:
        build_plate_filter(overlapping, W, H)
    except SystemExit:
        print("  ok  overlapping zooms rejected")
    else:
        raise AssertionError("overlapping zoom windows should be rejected")

    assert build_plate_filter([], W, H) == "", "no effects should mean no filter"
    print("  ok  empty effect list yields no filter")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        td = Path(tmp)
        test_guards()
        test_bw_window(td)
        test_zoom_resets(td)
    print("plate effects: all checks passed")
