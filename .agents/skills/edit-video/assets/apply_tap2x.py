"""Burn the 2X label onto an already-rendered video. Audio is copied."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from make_tap2x import OVERLAY, make_tap2x


def apply(src: Path, dest: Path, tap: Path | None = None) -> None:
    tap = tap or (src.parent / "tap2x.png")
    make_tap2x(tap)
    tmp = dest.with_suffix(".tap2x-tmp.mp4")
    cmd = [
        "ffmpeg", "-hide_banner", "-nostdin", "-y",
        "-i", str(src),
        "-i", str(tap),
        "-filter_complex",
        f"[1:v]format=rgba[tap];[0:v][tap]overlay={OVERLAY}",
        "-c:v", "h264_nvenc", "-preset", "p5", "-tune", "hq",
        "-rc", "vbr", "-cq", "19", "-b:v", "0",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart",
        str(tmp),
    ]
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)
    tmp.replace(dest)
    print(f"Wrote {dest}")


if __name__ == "__main__":
    apply(Path(sys.argv[1]), Path(sys.argv[2]))
