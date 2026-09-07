---
id: authority
aliases: [pedagogical, teaching, thesis, teach]
status: ready
---

# Mode · authority

Pedagogical + authoritative tone: teaching guardrails, harnesses, evals,
mechanisms.

Implementation state: `plate_effects` exists in `render_vertical.py` (it covers
`zoom-emphasis` and `black-and-white`, with a self-check in
`assets/test_plate_effects.py`), and so do `news-inserts` / `news_insert.py`.
Only `motion_terco.py` is missing, and it is **opt-in** and does not block the
mode: without it, the diagram beat falls back to the third's default judgement
(empty, or a reference insert).

`pop-it` today is only the click SFX (`--pop-it`, tied to the start of each
overlay); the spec's visual micro-zoom does not exist yet.

## Features (order)

1. `cut-dead-air` → `assets/features/cut-dead-air.md`
2. `zoom-emphasis` → `assets/features/zoom-emphasis.md`        *(plate)*
3. `black-and-white` → `assets/features/black-and-white.md`    *(plate)*
4. `pop-it` → `assets/features/pop-it.md`                      *(plate + SFX)*
5. `motion-third` → `assets/features/motion-third.md`          *(overlays · opt-in)*
6. `news-inserts` → `assets/features/news-inserts.md`          *(overlays · opt-in)*
7. `loudnorm` → `assets/features/loudnorm.md`

`subtitles` is not listed because it rides on every mode — burned at the final
render only (`assets/features/subtitles.md`).

Not every beat uses every feature: the mode **enables** the vocabulary; the
editor picks per beat (slow push on the thesis, B&W on the impression, pop-it on
the list, motion on the diagram, a paper screenshot on the citation). No beat =
no effect emitted.

### Upper third — judgement, not a fixed grid
In `news`, the third's exposure is relatively predictable (insert when the news
is cited → gone at the CTA). Here it is **not**: the editor decides **at each
moment** whether the emphasis goes on the diagram (`motion-third`), on a
**reference image** (`news-inserts`), or on the face/plate (zoom, B&W, pop-it,
or nothing). When in doubt, leave the third empty. See “Editorial judgement” in
`motion-third.md`.

Two kinds of content in the same slot (never at the same time):

| Type | Feature | When |
|---|---|---|
| Animated diagram / flow | `motion-third` | The speech teaches a mechanism that gains from a structured visual |
| Static screenshot (paper, article, launch) | `news-inserts` | The speech **cites** a concrete source and the screenshot anchors the claim |

**Reference inserts (optional, same engine as news mode).** Typically: a
screenshot of a paper, an article, a model/library announcement, a figure from a
study. Same pipeline: `news_insert.py`, the `video/inputs/<slug>-imagens/`
folder, a `FONTE:` chyron where it makes sense. Gone at the CTA.

Example: in the middle of a Reel about guardrails you say

> “Making negative statements pollutes the AI's global workspace, as this paper
> from university X showed”

→ the upper third with the paper's screenshot (title/authors/figure legible),
while the VO carries on. It is not breaking news; it is **visual evidence** for
the pedagogical thesis.

## When to use it
Content that teaches a mechanism (guardrails, evals, harnesses, pipelines) in an
authoritative voice — not pure breaking news (that is `news`). Citing a paper or
a launch inside the lesson is still `authority` + `news-inserts`.
