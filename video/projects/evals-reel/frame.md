---
colors:
  ground: "#FFFFFF"
  ink: "#0A0A0A"
  inverted_ground: "#0A0A0A"
  inverted_ink: "#FFFFFF"
  semantic_correct: "#5BD6A2"
  semantic_error: "#FF6B6B"
typography:
  display:
    family: "Bricolage Grotesque"
    weight: 800
    letter_spacing: "-0.025em"
    line_height: 0.94
  body:
    family: "Inter"
    weight: 500
  reading:
    family: "Newsreader"
    weight: 400
    style: "italic"
spacing:
  safe_x: 72
  safe_top: 72
  caption_keepout_bottom: 300
components:
  mark: "@pedro.miyasaki.ia"
  grain: "radial-gradient(currentColor .5px, transparent .6px), 4px grid, opacity .05"
  halftone_grid: 11
  rough_outline_width: 7
  corner_radius: 0
---

## Overview

Alvinegro is a black-and-white editorial print system. The talking head remains untouched whenever
there is no explanatory insert. Concept graphics take over the whole frame on a black background;
they never sit over the speaker's face. Inversion is the main accent. In this revision, green
marks relevant clauses or correct answers; red marks highlighted output, excess, omissions or regressions.

## Frame

- Canvas: 1080 by 1920.
- Default footage fills the frame.
- Captions stay inside the lower safe zone and never cover the speaker's mouth.
- Talking-head passages contain footage and captions. The requested business disclaimer and quoted `"EVALS"` callout sit above the face.
- Full-frame inserts are reserved for concepts that are difficult for a non-technical viewer.
- Keep the handle in the upper-left corner only when a full-frame graphic takes over.

## Typography

- Display: Bricolage Grotesque 800. Never below 40 px.
- Body and captions: Inter 400 or 500.
- Long reading copy: Newsreader 400 italic, only on white.
- Use no more than two type sizes in one graphic state.

## Color and texture

- Use `#FFFFFF` and `#0A0A0A`, with `#5BD6A2` and `#FF6B6B` only for the semantic signals requested in this revision.
- Gray must come from black or white halftone, never a gray hex.
- Keep the paper grain active on graphic surfaces.
- Do not place halftone over halftone.

## Graphic vocabulary

- Field, paired rules, tally marks, rough tape, block labels and paper grain.
- Diagrammatic SVG only: contracts, boxes, arrows, checkmarks, crosses, bars and counters.
- Rough outlines use 7 px strokes with rounded caps and joins.
- Halftone fills sit 8 to 9 px off-register from their outlines.

## Motion

- Editorial, controlled and readable.
- Hard cuts follow speech edits.
- Punch-ins are short and sparse.
- Graphic callouts stamp, draw or assemble. They do not float without purpose.
- No glow, gradients, rounded UI cards, neon, fake interfaces or decorative color.

## Brand constraints

- `@pedro.miyasaki.ia` is the only persistent text mark.
- Do not use the full stamp or badge over talking-head footage.
- Every explanatory graphic uses a full black frame. Never layer it over the talking head.
