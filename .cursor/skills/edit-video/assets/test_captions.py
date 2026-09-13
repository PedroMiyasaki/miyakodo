"""Self-check for the caption builder (build_master_ass).

Builds an ASS from a synthetic two-segment transcript and asserts the four
things the feature spec promises, then burns a frame to prove the font
resolves in libass:

  - short chunks that replace each other: no cue over CUE_WORDS or two
    lines, no word shown twice (nothing accumulates)
  - no cue outlives the next one's start
  - a cue holds through the pause but never into the next cue
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
    CAPTION_FONTS, CAPTION_TTFS, CUE_WORDS, build_master_ass,
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

        # Two sentences in one source. The gap after "código." is the pause its
        # cue should hold through.
        (edit / "transcripts" / "a.json").write_text(json.dumps({"words": _words([
            ("A", 0.0, 0.2), ("IA", 0.2, 0.6), ("escreve", 0.6, 1.1),
            ("o", 1.1, 1.2), ("código.", 1.2, 1.8),
            # four words that wrap to three lines at LINE_CHARS
            ("Ela", 3.0, 3.3), ("estuda", 3.3, 3.6), ("inteligência", 3.6, 4.2),
            ("artificial.", 4.2, 4.8),
        ])}), encoding="utf-8")
        edl = {"sources": {"a": "a.mp4"},
               "ranges": [{"source": "a", "start": 0.0, "end": 5.0}]}

        out = edit / "master.ass"
        build_master_ass(edl, edit, out, (W, H))
        ass = out.read_text(encoding="utf-8")
        cues = _cues(ass)

        # Short chunks, each word shown exactly once: nothing accumulates.
        chunks = [c[2].replace("\\N", " ").split() for c in cues]
        assert all(len(c) <= CUE_WORDS for c in chunks), f"chunk too long: {chunks}"
        assert all(c[2].count("\\N") <= 1 for c in cues), \
            f"cue over two lines: {[c[2] for c in cues]}"
        shown = " ".join(" ".join(c) for c in chunks)
        assert shown == "A IA escreve o código Ela estuda inteligência artificial", \
            f"words repeated or lost: {shown!r}"

        # No cue may outlive the next one's start, ever — two cues alive at
        # once draw stacked. The MIN_STEP floor is the thing that can cause this.
        for (_, end, _), (start, _, _) in zip(cues, cues[1:]):
            assert end <= start + 1e-6, f"overlapping cues: {end} > {start}"

        # The sentence's last cue holds past its last word (1.8) but stops
        # before the next cue starts (3.0).
        hold_end = max(c[1] for c in cues if c[0] < 2.0)
        assert 1.8 < hold_end <= 3.0, f"bad hold: {hold_end}"

        # Case is left as transcribed.
        assert any("Ela" in c[2] for c in cues), "sentence case was lost"
        assert any("escreve" in c[2] for c in cues), "text was uppercased"

        # The font survives an actual burn (the first cue is on screen at t=0).
        fonts = edit / "fonts"
        fonts.mkdir()
        for ttf in CAPTION_TTFS:
            shutil.copy2(CAPTION_FONTS / ttf, fonts / ttf)
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
