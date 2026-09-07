"""Self-check for the caption builder (build_master_ass).

Builds an ASS from a synthetic two-segment transcript and asserts the four
things the feature spec promises, then burns a frame to prove the fonts and
the mid-cue style switch survive libass:

  - words accumulate inside a block instead of flashing a fresh pair
  - a block's cues are contiguous (no blink between reveal steps)
  - the block's last cue holds through the pause but never past the hard cut
  - sentence case is preserved, not uppercased

Run:
  PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
    python .claude/skills/edit-video/assets/test_captions.py
"""
from __future__ import annotations

import json, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from render_vertical import (  # noqa: E402
    CAPTION_FONTS, CAPTION_TTFS, build_master_ass,
)

W, H = 1080, 1920


def _words(spec: list[tuple[str, float, float]]) -> list[dict]:
    return [{"type": "word", "text": t, "start": s, "end": e}
            for t, s, e in spec]


def _cues(ass: str) -> list[tuple[float, float, str]]:
    out = []
    for line in ass.splitlines():
        if not line.startswith("Dialogue:"):
            continue
        f = line.split(",", 9)
        out.append((_secs(f[1]), _secs(f[2]), f[9]))
    return out


def _secs(stamp: str) -> float:
    h, m, s = stamp.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        edit = Path(td)
        (edit / "transcripts").mkdir()

        # Two sentences in one source. The gap after "código." is the pause the
        # last cue of block 1 should hold through.
        (edit / "transcripts" / "a.json").write_text(json.dumps({"words": _words([
            ("A", 0.0, 0.2), ("IA", 0.2, 0.6), ("escreve", 0.6, 1.1),
            ("o", 1.1, 1.2), ("código.", 1.2, 1.8),
            ("Ela", 3.0, 3.3), ("não", 3.3, 3.6), ("entende", 3.6, 4.2),
        ])}), encoding="utf-8")
        edl = {"sources": {"a": "a.mp4"},
               "ranges": [{"source": "a", "start": 0.0, "end": 5.0}]}

        out = edit / "master.ass"
        build_master_ass(edl, edit, out, (W, H))
        ass = out.read_text(encoding="utf-8")
        cues = _cues(ass)

        assert len(cues) >= 4, f"expected several reveal steps, got {len(cues)}"

        # Accumulation: inside a block each cue contains the previous one.
        first = [c[2] for c in cues if c[0] < 2.0]
        assert len(first) >= 3, f"block 1 should reveal in steps: {first}"
        for prev, nxt in zip(first, first[1:]):
            stripped = prev.rstrip(",;:.").replace("\\N", " ")
            assert stripped in nxt.replace("\\N", " "), \
                f"not accumulating: {prev!r} -> {nxt!r}"

        # Contiguous inside the block: no gap between reveal steps.
        for (_, end, _), (start, _, _) in zip(cues, cues[1:]):
            if start < 2.0:
                assert abs(end - start) < 0.01, \
                    f"blink between steps: {end} -> {start}"

        # No cue may outlive the next one's start, ever — two cues alive at
        # once draw stacked. Real transcripts put reveal steps 90ms apart, so
        # the MIN_STEP floor is the thing that can cause this.
        for (_, end, _), (start, _, _) in zip(cues, cues[1:]):
            assert end <= start + 1e-6, f"overlapping cues: {end} > {start}"

        # The block's last cue holds past the last word (1.8) but stops before
        # the next block starts (3.0).
        block1_end = max(c[1] for c in cues if c[0] < 2.0)
        assert 1.8 < block1_end <= 3.0, f"bad hold: {block1_end}"

        # Case is left as transcribed.
        assert any("Ela" in c[2] for c in cues), "sentence case was lost"
        assert any("escreve" in c[2] for c in cues), "text was uppercased"

        # The fonts and the mid-cue style switch survive an actual burn.
        fonts = edit / "fonts"
        fonts.mkdir()
        for ttf in CAPTION_TTFS:
            shutil.copy2(CAPTION_FONTS / ttf, fonts / ttf)
        out.write_text(ass.rstrip("\n") + "\n" + "Dialogue: 0,0:00:00.00,"
                       "0:00:01.00,BODY,,0,0,0,,teste\\h\\h"
                       "{\\rEMPH}ênfase{\\r}\n", encoding="utf-8")
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
             "-i", f"color=c=black:s={W}x{H}:d=1",
             "-vf", "subtitles=master.ass:fontsdir=fonts",
             "-frames:v", "1", "burn.png", "-nostdin"],
            check=True, cwd=str(edit), stderr=subprocess.PIPE,
        )
        assert (edit / "burn.png").stat().st_size > 10_000, "burn produced nothing"

    print("captions self-check: OK")


if __name__ == "__main__":
    main()
