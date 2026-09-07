---
id: motion-third
phase: overlays
industry: upper-third motion graphics / explainer MOTION
---

# Feature · Motion in the upper third (upper-third MOTION)

## Industry name
**Upper-third motion graphics** (sometimes *explainer MOTION* / *diagram
insert*): a programmatic animation occupying the top band of the frame, while
the VO and the face carry on in the bottom two thirds. Same spatial “slot” as
the news inserts — different vocabulary (animated diagram, not a static
screenshot).

## What it does
On pedagogical beats (flow, pipeline, guardrail, eval, harness, branching), it
generates a ProRes 4444 alpha clip with an animation in the **upper third**; the
rest of the canvas is transparent. It composites as `overlays` in the EDL (same
as `news-inserts`).

**The upper third is not on by default.** Having the feature in the mode only
authorizes the vocabulary — it does not oblige you to fill the band. See the
editorial judgement below.

## Editorial judgement (mandatory)

Unlike `news` mode (where the rule is more predictable: insert when the news is
cited, gone at the CTA), in pedagogical/authority content you **cannot decide in
advance** on a fixed grid of “always animate here”. The editor has to be
**critical beat by beat**.

Ask, for each stretch of the VO:

1. **Where does the emphasis need to land right now?** On the face/spoken
   argument, or on a diagram the speech alone cannot carry?
2. **Does the motion clarify or compete?** If the moment is a vocal punch, an
   impression (B&W), a pop-it list, or the CTA — the upper third **goes away**
   (or never enters).
3. **Is there real visual structure?** A flow, a branch, layers, a checklist.
   Without that, do not force decorative animation.

Common-sense defaults (not blind rules):

| Moment | Upper third |
|---|---|
| Explaining a mechanism / pipeline / conditional | Strong candidate for motion |
| Thesis, opinion, provocation, “you're wrong” | Prefer a clean plate (`zoom-emphasis` / the face) |
| Impression / someone else's voice | Prefer `black-and-white`; motion off |
| Spoken list (names, adjectives) | Prefer `pop-it`; motion off |
| CTA / close | **Always off** (clean frame on the face) |
| There was already motion in the last ~4s | Default off — let it breathe |

The absence of motion is a valid and frequent decision. A good pedagogical Reel
has long stretches of just talking-head + subtitles. When in doubt, **do not
expose** the third.

## Programmatic approach (decision — confirmed)

**Official path:** HTML + CSS → Playwright frame by frame → ProRes alpha. Not a
manual timeline in CapCut.

### Visual system

The visual system (tokens, typography, components) was removed when the old
brand was retired and has no replacement yet. Until one exists, ask the user for
the palette and the typography before writing the beat's HTML, and reuse the
same decision across every beat of the piece — one palette per Reel.

**Forbidden in motion:** new fonts on every beat, neon gradients, multi-layer
shadows, “AI purple”, stock Lottie.

Why this stack:

- the HTML→PNG pipeline (`scripts/render_html_to_pngs.py` / Playwright) —
  motion = the same idea with N frames over time
- the agent writes the animation from the beat and re-renders it

**Escape hatch:** Manim only if the beat is a heavy mathematical
equation/derivation — and even then the palette must be the same as the rest of
the piece. It is not this feature's default.

### Contract for one motion beat

1. **A 1-line storyboard** (what appears, in what order) aligned to the VO's
   words.
2. **File** `<edit>/motion/<beat_id>/index.html` — a 1080×640 composition (the
   upper third). No site UI chrome; the diagram only.
3. **Duration** = the beat's window on the output timeline (typically 3–6s).
4. **Render** → a PNG sequence @ 24fps → `render.mov` ProRes 4444, full
   1080×1920 canvas with the top band as the animation and the rest transparent
   (same spatial envelope as `news_insert.py`).
5. **EDL** `overlays[]` with `start_in_output` / `duration`.

Target helper (to be implemented): `assets/motion_terco.py` — takes `--html`,
`--duration`, `--out`; uses headless Playwright frame by frame (or CSS
animations scrubbed via `currentTime`) and packages the `.mov`.

### What to animate (permitted vocabulary)

| Type | Example use |
|---|---|
| Linear flow | pipeline retrieve → rank → generate |
| Branching / conditional | “if score < threshold → block” |
| Layers | prompt vs external guardrail vs eval |
| A checklist ticking off | 3 harness criteria |
| Counter / state | pass → fail in an eval |

Anti-patterns: abstract wallpaper, generic Lottie with no thesis, long text in
the third (that is subtitling — it goes at the bottom via the `subtitles`
feature).

## Contextual example
You explain a layered guardrail. While you say “first the policy, then the
classifier, then the block”, the upper third animates three nodes lighting up in
sequence, with arrows, in the piece's palette. At the CTA (“study the mechanism,
not the slogan”), the overlay goes away — clean frame on the face (the same
CTA-wall rule as news mode).

## How to run it

1. Find the pedagogical beats in the VO (diagram > loose sentence).
2. For each beat: 1-line storyboard → write the `index.html` → render with the
   helper → position it in the EDL.
3. **CTA wall:** `start + duration ≤ cta_start`. At the close, the third is
   free.
4. Report the beat, the duration and a preview frame to the user before the
   Reel's final render.

```json
"overlays": [
  {
    "file": "animations/motion_01/render.mov",
    "start_in_output": 22.0,
    "duration": 4.5
  }
]
```

## Hard rules
- Upper third only. Never full-frame (that would erase the teacher).
- Subtitles (the `subtitles` feature) still go underneath — Hard Rule 1.
- **Opt-in by judgement**, not by checklist. Do not animate “because the mode
  allows it”.
- Density: at most **1 motion active** at a time; a loose ceiling of 2–4 beats
  per short Reel — and only if each one passes the judgement above. Zero motions
  is fine too.
- One palette for the whole piece. No parallel palette per beat.
- If the diagram does not clarify the sentence within a <2s glance, redo the
  HTML or **cut the beat** — do not “save” it with more text.

## Relationship to other features
- Vs `news-inserts`: same spatial slot. Static (paper / article / launch / news)
  = `news-inserts`; animated diagram = `motion-third`. Do not use both at the
  same instant. In `authority`, both are opt-in.
- With `black-and-white` / `zoom-emphasis`: fine — the plate below changes; the
  motion stays coloured in the band.
- With `pop-it`: avoid it in the same second (click + diagram compete for
  attention).

## Status
Spec + file contract are ready. Implementation pending:
`assets/motion_terco.py` + a folder of canonical examples in
`assets/motion-examples/` (one flow, one branch, one checklist).
