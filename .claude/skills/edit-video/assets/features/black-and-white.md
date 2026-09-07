---
id: black-and-white
phase: plate
industry: B&W grade window / desaturate pass
---

# Feature · Black and white (B&W grade window)

## Industry name
A temporal **desaturation** window (saturation → 0) on the shot. In cutting
rooms it usually shows up as a **B&W grade**, a **flashback grade** or, when it
marks someone else's speech / irony, a **diegetic imitation grade** — the grade
changes to signal “I am quoting / impersonating another voice now”, not a
literal flashback.

## What it does
For a short stretch, the talking-head (the **plate**) goes black and white.
Outside the window, normal colour. It serves to:

- impersonate the sceptical counterpart
- mark criticism / “the voice of the market”
- highlight an argument you are rebutting

## Contextual example
You explain that a guardrail is an **external** mechanism. Then you impersonate
the objection:

> “Yeah, but can't you just put the rule in the prompt?”

On that stretch: **B&W** (and, for extra weight, `zoom-emphasis` `fast` over the
same range — the classic “get inside the objection's head” combo).

When you go back to your own voice / answer, the colour returns (end of the
window).

Explicit direction during the recording (an editor note) also counts — and
prevails:

> …“Well, I can just put a rule in the prompt” **“on that impression bit, go
> black and white”** And you could actually…

Apply B&W to the impression; **cut** the spoken direction itself from the
video/subtitles (`SKILL.md` § Editor notes).

## Parameters (defaults)

| Param | Default | Notes |
|---|---|---|
| `start_in_output` / `end_in_output` | the impression's window | typically 1.5–4s |
| Desaturation fade in/out | 80–120ms | avoids a “hard cut” of colour |
| Scope | **the plate only** | third-band overlays (motion / news) and subtitles do **not** inherit the B&W — they stay coloured on top, unless the beat calls for the opposite |

## How to run it

1. Mark on the output timeline the range where the voice is “the other person”
   (impression) or the staged criticism.
2. EDL:

```json
"plate_effects": [
  {
    "type": "preto_e_branco",
    "start_in_output": 18.20,
    "end_in_output": 21.00
  }
]
```

> The `type` string is the literal the renderer matches on — keep it exactly as
> written above.

3. In the plate render: `hue=s=0` (or equivalent) enabled between start/end,
   with short fades at the edges.

## Combos
- **With `zoom-emphasis`:** allowed and desirable on impressions (“punch-in +
  B&W”).
- **With `pop-it`:** avoid it in the same window — pop-it is an affirmative
  list; B&W is someone else's voice / criticism.
- **With `motion-third`:** fine; the diagram in the upper third stays in colour,
  the face below goes B&W.

## Hard rules
- Short window. B&W that runs too long becomes an aesthetic, not a signal.
- Back to colour **before** the final CTA (the close of the piece stays in
  colour, unless the user explicitly asks otherwise).

## Status
Implemented. `render_vertical.py` reads `plate_effects` and applies `hue=s=`
with edge ramps (`fade`, default 100ms) on the plate, before the overlays — so
third-band cards and subtitles stay coloured on top.
Self-check: `assets/test_plate_effects.py`.
