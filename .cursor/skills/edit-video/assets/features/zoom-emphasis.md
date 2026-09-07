---
id: zoom-emphasis
phase: plate
industry: punch-in / push-in (with reset / punch-out)
---

# Feature · Zoom for emphasis (punch-in / push-in)

## Industry name
In editing, tightening the framing without cutting the shot is called a
**push-in** (when it is slow, the camera “pushes”) or a **punch-in** (when it is
fast, it “punches” the frame). The return to 100% is called a **reset** /
**punch-out**. It is not a cut to another take: it is a **scale + crop
transform** on the same talking-head.

## What it does
On emphasis beats, the frame moves closer to the face/thesis and
**mandatorily returns to 1.0×** before the next beat. Never leave the video
“stuck” in the zoom.

Two modes (pick one per beat):

| Mode | Industry name | When to use it | Behaviour |
|---|---|---|---|
| `slow` | **slow push-in** | Long line of reasoning, thesis, CTA | Scale rises very subtly across the sentence |
| `fast` | **crash / punch-in** | Short payoff (“…you're wrong”) | Fast zoom **right before** the key word/phrase, holds a moment, resets |

## Contextual example

**Slow** — opening:
> “You need protections on your artificial intelligence applications.”
Push-in from ~1.00 → ~1.06 across the whole sentence; at the full stop, ease-out
back to 1.00.

**Fast** — the blow:
> “You could put negative instructions in the system prompt, but if you do
> that, **you're wrong**.”
Punch-in (~180–250ms) landing on the onset of “you're wrong” (peak scale
~1.12–1.15), holds ~200–400ms, resets in ~200ms.

## Parameters (defaults)

| Param | `slow` | `fast` |
|---|---|---|
| `scale_peak` | 1.06–1.08 | 1.12–1.15 |
| Rise | length of the beat's window (ease-in-out) | 180–250ms (ease-out) |
| Hold at peak | optional, short | 200–400ms |
| Reset → 1.0 | last ~20–30% of the window, or 200–300ms after the hold | 150–250ms after the hold |
| Crop anchor | centre of the face (or centre of the frame if there is no face track) | same |

## How to run it

1. On the output transcript, mark the emphasis beats. Classify each one `slow`
   or `fast`. For `fast`, note the payoff word and the **start** timestamp of
   that word (`land_at` on the output timeline).
2. Write it into the EDL (a plate extension), with no overlapping zooms:

```json
"plate_effects": [
  {
    "type": "zoom_enfase",
    "mode": "fast",
    "start_in_output": 12.40,
    "end_in_output": 14.10,
    "land_at": 12.85,
    "scale_peak": 1.14
  }
]
```

> The `type` string is the literal the renderer matches on — keep it exactly as
> written above.

3. In the plate render (before the overlays), apply a centred `scale` + `crop`
   with keyframes; at `end_in_output` the scale **must** be 1.0.

## Hard rules
- Every zoom has a reset. If `end` arrives and the scale ≠ 1.0, the effect is
  wrong.
- Do not stack it with `pop-it` in the same window (pop-it's micro-zooms are a
  different vocabulary).
- It can be combined with `black-and-white` on the same beat (impression /
  criticism).
- Do not zoom over an upper-third insert in a way that “eats” the band: the zoom
  is on the **plate** (the face); third-band overlays go on top afterwards.

## Status
Implemented. `render_vertical.py` reads `plate_effects` and applies them to the
plate (after the concat, before the overlays) via `zoompan` with a smoothstep
curve. The reset to 1.0× is guaranteed by construction, and overlapping zoom
windows are rejected with an error. Self-check: `assets/test_plate_effects.py`.
