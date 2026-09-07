---
id: news-inserts
phase: overlays
---

# Feature · News / reference inserts

## What it does
A reference image appears as a **floating card**, composited straight over the
video — it does **not** resize or crop the talking-head, the whole frame stays
exactly as it was shot. The card sits **centered in the lower-third zone**
(not glued to the bottom edge) for **a few seconds, while the VO talks about
that subject**, and then goes away — it does not have to stay until the next
subject starts, and stretches with no card between one insert and the next are
normal. Scale pop (slight overshoot) + quick fade on entry, synced with the
`pop-it` click (§3); soft fade on exit. Gentle Ken Burns inside the card while
it holds. Optional: a `FONTE: …` chyron in the card's corner.

Uses:

- `news` mode — 2–5 specific images across the piece (announcement, benchmark,
  specs, platform mentioned), each one a brief card at the moment the VO
  mentions it.
- `authority` mode (opt-in) — visual evidence for the thesis: a screenshot of a
  **paper**, an article, a model/library launch, a figure from a study.

Script: `assets/news_insert.py` (ProRes 4444 alpha, full canvas, transparent
except for the card). The canvas is passed via `--width`/`--height` — **always
the source's real output** (rotation applied, not the stream's raw
`width`/`height`; `render_vertical.py` prints `canvas: WxH` at the start of the
render — use that value), never a fixed value. CLI in `assets/README.md`.

## How to run it

### 1. Beats + windows
Reading `takes_packed.md`, locate every mention of something worth visual proof
(product name, benchmark claim, platform mentioned, etc.) and the word range in
which it is said. Map the **start** of that range onto the output timeline —
that is where the card is born. **Short duration: 4–7s per card**, not the whole
beat. It does not have to cover 100% of the piece; gaps with no card are normal
and expected. Also locate the **CTA** — no card enters from there on (clean
frame for the close).

### 2. Image for each card
- **Manual wins.** Check `video/inputs/<slug>-imagens/` for `01.<ext>`,
  `02.<ext>`… (`.png/.jpg/.jpeg/.webp`, with or without the leading zero). If
  they exist, use them without second-guessing.
- **Otherwise, search proactively.** One image per card, specific to what is
  being said right there — do not repeat the same generic cover image for the
  whole piece. A screenshot of the announcement, a model card, a benchmark
  chart, the page of the platform mentioned: each technical section gets its own
  visual evidence when the primary source offers one. A real screenshot of the
  official site (via browser, cropped to the relevant section) beats any generic
  cover image on specificity. Query in English → `WebSearch`/browser → crop with
  `zoom` (`save_to_disk: true`) → copy into the folder (`0N.png`) → inspect with
  `Read`. Criteria: does it match *that* moment? legible in the card? no
  watermark? No image > wrong image. Avoid generic stock.
- **Report** to the user, before rendering, which image covers which moment and
  where each one came from.

### 3. Generate the cards + pop-it
One clip per card:

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/news_insert.py \
  --image "video/inputs/<slug>-imagens/01.png" \
  --out "<edit>/animations/slot_news_01" \
  --duration 6 --source "openai.com" --fit contain \
  --width 2160 --height 3840
```

- `--width`/`--height`: the source's real output, from the `canvas:` line
  `render_vertical.py` prints — not a fixed value.
- `--fit contain` (the default, and preferred almost always): the whole image
  fits inside the card, cropping no content. The card's background is white —
  most site screenshots already have a white/light background, so `contain`'s
  letterbox usually stays invisible rather than reading as empty filler.
- `--fit cover`: only when the excess cropped at the edges is guaranteed to be
  empty (an isolated logo, a photo with plenty of air around it). Test first: if
  the image has text running all the way to the edge (e.g. a very wide page
  title), `cover` cuts the text — use `contain`.
- `--source`: mono chyron in the card's corner; omit it for a clean insert.

**Pop-it (audio click on the pop):** when rendering (`render_vertical.py`),
pass `--pop-it` — it mixes a click (`assets/sfx/click.wav`) at each overlay's
`start_in_output`, synced with the scale pop that `news_insert.py` already draws
in the clip's first ~150ms. Nothing separate needs to be generated for it; it is
a render flag. See `pop-it.md` for the SFX itself.

### 4. Position them in the EDL
Each card goes into `overlays` with `start_in_output` = the start of the moment
and `duration` = 4–7s (it does not have to be contiguous with the next one; gaps
are expected). There is no `band` field in `ranges` anymore — the talking-head
is never resized, so the EDL's `ranges` need nothing special for this feature.

> Third-party screenshot: the chyron credits the source; the user decides what
> to publish. Flag any doubt about usage rights.

## Calibration
Canvas = the source's real output, always recomputed (never hardcoded — this was
a bug: an overlay generated at a fixed 1080×1920 and composited over a 4K source
showed up at 1/4 of the size, covering only the corner). Card: side margin ~8%
of the canvas on each side, max height ~70% of the lower third (so it keeps air
above/below and never sticks to the bottom edge), rounded corners + a soft
shadow to separate it from the video behind it (there is never an opaque band
covering the video — the rest of the frame stays visible the whole time,
including behind/around the card).

## History
There were two earlier versions of this feature: (1) an opt-in per-beat burst
with no canvas control (the tiny-image bug); (2) a full band in the upper third,
persistent until the CTA, with the talking-head resized to fit below it. Both
were abandoned — with v2 the user found resizing the video for no reason
annoying, and the persistent band stayed on screen far too long without the
matching subject. The current version (floating card, brief, resizing nothing)
is the definitive one until new feedback.
