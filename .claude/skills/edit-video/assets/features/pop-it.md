---
id: pop-it
phase: plate
industry: staccato punch-ins + hit SFX (word pops)
---

# Feature · Pop-it (staccato punch + hit SFX)

## Industry name
A sequence of **micro punch-ins** synced to target words in the VO, each one
accompanied by a **hit SFX** (click / tick). In motion/edit: *word pops*,
*staccato zooms*, *impact hits on VO*. It is not kinetic on-screen typography —
it is the **shot** “blinking” in scale + a click in the audio, at the onset of
each word in the list.

## What it does
On spoken lists (names, adjectives, pillars), for **each** item in the list:

1. at the word's onset → **click** in the audio
2. at the same instant → **mini-zoom** (~1.00 → ~1.04 → 1.00 in ~120–180ms)
3. the next item only fires after the previous one has reset

After the last item, scale = 1.0 and SFX silence.

## Contextual examples

**Proper nouns:**
> “companies like **Google**, **Amazon** and **Microsoft**”
Three hits: Google / Amazon / Microsoft.

**Value adjectives:**
> “with guardrails your applications become more **secure**, **reliable** and
> **auditable**”
Three hits: secure / reliable / auditable.

Do not mark connectors (“like”, “and”, “more”) — only the list's terms.

## Parameters (defaults)

| Param | Default |
|---|---|
| `scale_peak` per hit | 1.04 (max 1.06) |
| Micro-zoom duration | 120–180ms (rise + reset) |
| SFX | `assets/sfx/click.wav` (mono, short, ~30–80ms) |
| SFX gain | ~-18 to -12 dBFS under the VO — that holds for an isolated hit on a beat with no simultaneous speech. When the click lands exactly where the VO is speaking (the image-pop case in `news-inserts`: the click marks the overlay's start, which is also where the beat's speech begins), that range is far too low and the click disappears under the voice. `render_vertical.py --pop-it` uses `+4dB` over `click.wav` (effective peak ~-3.5dBFS) for that case — measured, not just heard: `-14dB` of attenuation left the click's peak at ~-25dBFS against a voice RMS of ~-15dB, inaudible. Confirm by ear before assuming "present" — a measured peak does not imply perceptible under speech. |
| Max hits per beat | 2–5 (beyond that it turns into a metronome; split it into two beats) |

## How to run it

1. On the output timeline, list the word-level onsets of the target words
   (`takes_packed.md` / ASR).
2. EDL:

```json
"plate_effects": [
  {
    "type": "pop_it",
    "hits": [
      {"t": 8.12, "word": "Google"},
      {"t": 8.55, "word": "Amazon"},
      {"t": 9.10, "word": "Microsoft"}
    ],
    "sfx": "assets/sfx/click.wav",
    "scale_peak": 1.04
  }
]
```

3. Plate render: for each hit, a scale keyframe centred on `t`.
4. Audio mix: `amix` / `adelay` of the click at each `t` (path relative to the
   repo root or to the skill). Loudnorm (the `loudnorm` feature) runs
   **afterwards** and swallows the final mix.

## Hard rules
- Reset between hits. No overlapping micro-zooms.
- Do not combine it with `zoom-emphasis` in the same window (scale conflict).
- Do not use it on a sceptical impression — that is `black-and-white`'s
  territory.
- If the ASR gets the onset wrong, adjust `t` by hand before the final render (1
  frame of error already “detaches” the click from the mouth).

## Asset dependency
Canonical click: `.claude/skills/edit-video/assets/sfx/click.wav`
(mono, ~45ms, a dry tick of filtered white noise — generated and versioned in
the repo). If the file disappears, do not invent an SFX at render time: restore
the asset or skip the audio hits and report it. To change the sound, replace the
file keeping the name.

## Status
**Implemented (partially): the audio click.** `render_vertical.py --pop-it`
mixes `click.wav` (adelay + amix, `normalize=0`, before loudnorm) at the
`start_in_output` of each entry in `overlays` — this is what `news-inserts` uses
to play a click for every card that appears. That case needs neither
`plate_effects` nor manual hits: one overlay = one click, automatically.

**Spec, not implemented: the micro punch-in on a spoken list** (the `hits`/
`plate_effects` in the EDL above, for proper nouns or adjectives in sequence,
with a zoom on the talking-head image itself). That is still pure plate
transform, with no code — a future implementation if some mode calls for it.
