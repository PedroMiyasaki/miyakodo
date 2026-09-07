---
id: loudnorm
phase: render
---

# Feature · Loudnorm

## What it does
Normalizes the Reel's audio to **-14 LUFS / -1 dBTP / LRA 11** (two-pass), the
publishing standard.

## How to run it
Run this skill's renderer **without** `--no-loudnorm`:

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/render_vertical.py \
  "<edit>/edl.json" -o "<edit>/final.mp4"
```

Fast preview (still with loudnorm, lower quality ladder):

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/render_vertical.py \
  "<edit>/edl.json" -o "<edit>/preview.mp4" --preview
```

Only use `--no-loudnorm` if the user explicitly asks for a render without
normalization (debug). In this skill's production runs, loudnorm is mandatory
whenever this feature is in the mode.
