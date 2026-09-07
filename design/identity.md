# Visual identity — Alvinegro

The visual system for every deliverable with its own layout. Fills the identity slots the
carousel craft doc (`.claude/skills/carousel/assets/carousel-craft.md`, §0) requires.

Proof of the system rendered: `design/proof/` (HTML + PNGs). Copy its `<style>` and `<defs>` as
the starting point for any new piece.

---

## The slots

| Slot | Value |
|---|---|
| `GROUND` | `#FFFFFF` paper. Inverted slides: `#0A0A0A`. |
| `INK` | `#0A0A0A` on paper; `#FFFFFF` on inverted. |
| `ACCENT` | **None — inversion is the accent.** See below. |
| `DISPLAY` | Bricolage Grotesque 800 · `letter-spacing:-.025em` · `line-height:.94` |
| `BODY` | Inter 400/500 |
| `READ` | **Newsreader 400 + italic** — reading mode only, white ground only. See below. |
| `MARK` | **`@pedro.miyasaki.ia`** — Inter 500, 22px, uppercase, `letter-spacing:.18em`, `opacity:.55`, top-left, every slide. This is the real handle; never render a placeholder. |
| `ART` | Hand-drawn wobble line + halftone fill. Technique below. |
| `TEXTURE` | Paper grain: `radial-gradient(currentColor .5px, transparent .6px)`, `4px` grid, `opacity:.05` |

Two families, two values, no third of anything. Strictly black and white — the halftone dot screen
is what produces every intermediate tone, exactly like newspaper printing.

**Inversion is the only accent, and it means one thing: the frame of the piece.** The cover and the
CTA are black; everything between is white. Nothing else inverts. That satisfies the craft doc's
"one accent, one consistent meaning" rule without spending a color, and it makes the cover a black
rectangle in a feed of white ones.

**Type scale** (1080×1350 canvas, 88px margin):

| Level | Size |
|---|---|
| Cover hook | 104px |
| Slide headline | 86px |
| CTA | 118px, centered |
| Body | 46px / 1.32, max 30ch |
| Mark | 22px |

---

## Typography — three voices

| Voice | Face | Job |
|---|---|---|
| Recognition | Bricolage Grotesque 800 | Hooks, headlines, the logotype. Never below 40px. |
| Support | Inter 400/500 | Body under a headline, the handle mark, labels, captions. |
| Reading | Newsreader 400 + italic | Anything over four lines. **White ground only.** |

Newsreader carries an optical-size axis, so it is set for its size rather than scaled to it — the
same argument as the roughness bands. On ink grounds it goes thin and dirty at every size, which is
why reading mode is white-only and not a preference.

Scale on the 1080 × 1350 canvas at an 88px margin: cover hook 104 · slide headline 86 · CTA 118
centred · body Inter 46/1.32 at 30ch · **reading Newsreader 40/1.42 at 38ch** · eyebrow and handle
mark 22 at `.18em`.

**Two sizes on a slide, never three.** If a slide seems to need a third level, it is two slides.

---

## Colour — the halftone ramp

Grey is a screen, never a tint. Four densities on the same 11px grid; pick one, do not interpolate,
and never reach for `opacity` or a hex grey to get there.

| Name | Radius | Coverage | Use |
|---|---|---|---|
| Whisper | 1.4 | 5.6% | Grain over a full bleed |
| Screen | 2.1 | 11.4% | The default — artwork fill |
| Shadow | 3.0 | 23.3% | Weight inside a drawing |
| Solid-ish | 3.9 | 39.4% | Reads dark, still dots |
| Ink | — | 100% | Flat. No screen. |

The dot inverts to white on ink grounds — same radii, same grid. **Never place a screen on a
screen:** two overlapping grids moiré on export, and the artefact survives compression better than
the artwork does.

`#0A0A0A` rather than `#000000` because true black smears on OLED during scroll and bands under
H.264. Contrast against paper is 19.8:1. Use the same `#0A0A0A` for Reel grounds, and keep the
paper grain on in exported frames — it doubles as dither.

---

## Patterns — six devices

The filter and the screen are technique. These are the things you place on a page:

1. **Field** — the screen at full bleed.
2. **Rule set** — heavy over thin, from the masthead. Every divider in the system.
3. **Tally** — counting marks, for anything measured in weeks or reps.
4. **Grain** — 4px radial at `.05` in `currentColor`, so it survives inversion. Always on.
5. **Torn band** — a rectangle through `#rough-lg`. Section breaks and pull quotes.
6. **Block label** — the logotype's block at label scale. Eyebrows and tags only.

Six is the whole vocabulary. A seventh is a decision about the system, so it goes in this file or it
does not get used. None of them may sit on a screen.

---

## Templates and stationery

| What | Source | Render at |
|---|---|---|
| Eight slide archetypes | `design/templates/slides.html` | `--selector .slide --width 1080 --height 1350` |
| Business card, two faces | `design/stationery/stationery.html` | `--selector .card --width 1050 --height 600` |
| Letterhead, A4 | `design/stationery/stationery.html` | `--selector .letter --width 1240 --height 1800` |
| The brand book | `design/brandbook/book.html` | `--selector .page --width 1600 --height 880` |

Archetypes: **cover · statement · quote · data · list · split · reading · CTA**. The handle mark is
on every one of them; the logotype is on none. Reach for *quote* when the line is the whole point,
*data* when one number persuades (never two), *list* for something the reader will screenshot (max
five), *split* when inversion carries the turn, *reading* when the argument runs past four lines.

Stationery is **digital only** — no bleed, no trim marks, no crop allowance. Card front carries the
stamp, back carries the badge: two surfaces, never in the same field of view. Contact details are
slots on purpose.

---

## The logotype

`design/logotype/` — `spec.html` is the source, `spec-render/` the four rendered pages.

**The mark is the name knocked out of an inked block.** Block and letterforms are roughened as one
impression, so the edge chews while the counters stay open. It is not a wordmark placed inside a
rectangle.

| Asset | What it is | Where it goes |
|---|---|---|
| **Stamp** | `PEDRO MIYASAKI` reversed out of the inked block | Letterhead, card, deck covers, sign-off |
| **Badge** | The same block cut down to `PM` | Avatar, favicon, video bug |
| **Masthead** | Name between two rules, descriptor slot beneath | Page headers, Substack, LinkedIn banner |

```
Block padding   .30em top · .38em sides · .34em bottom
Wordmark        Bricolage Grotesque 800, uppercase, -.03em
Clear space     .30em on every side, in em of the wordmark
Minimum         stamp 96px wide · badge 24px
```

**Roughness is a function of size.** The displacement is in absolute pixels, so one filter cannot
serve every size — `scale="7"` reads as ink at 900px and as mud at 120px.

| Mark width | Filter | scale | baseFrequency |
|---|---|---|---|
| ≥ 600px | `#rough-lg` | 7 | .018 |
| 300–600px | `#rough-md` | 4 | .026 |
| 120–300px | `#rough-sm` | 2 | .042 |
| < 120px | none | — | — |

The impression is **baked at render size**. Never scale an exported PNG of the mark — re-render it
at the target size so the band is right.

**The masthead is set, never filtered.** Its rules and descriptor are em-based off the wordmark:
top rule `.048em`, bottom rule `.014em`, descriptor `.115em` at `.34em` tracking. The descriptor
drops below a 96px wordmark, where it would render under 11px.

**Five ways to break it:** stretching (shears the grain), re-setting in Inter, filtering twice
(collapses the counters), placing it on a mid-tone, and using badge and stamp in the same field of
view — they are one mark at two altitudes.

**The logotype is not the slide mark.** Carousel slides keep the `MARK` slot above — the handle in
Inter, top-left, quiet. The stamp is a brand asset for stationery and headers; it never appears on
a carousel slide, where it would fight the display headline.

---

## How the drawings get made

No plugin, no image generation, no stock. Clean SVG geometry, torn up by a displacement filter at
render time. Playwright's Chromium applies it, so it lands in the PNG.

```html
<filter id="rough" x="-25%" y="-25%" width="150%" height="150%">
  <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="3" seed="11" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="rough2" x="-25%" y="-25%" width="150%" height="150%">
  <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="3" seed="4" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="6" xChannelSelector="R" yChannelSelector="G"/>
</filter>

<pattern id="ht-dark" width="11" height="11" patternUnits="userSpaceOnUse">
  <circle cx="5.5" cy="5.5" r="2.1" fill="#0A0A0A"/>
</pattern>
<pattern id="ht-light" width="11" height="11" patternUnits="userSpaceOnUse">
  <circle cx="5.5" cy="5.5" r="2.1" fill="#FFFFFF"/>
</pattern>
```

**The construction, every time:**

1. Draw the shape twice — once as a halftone-filled solid, once as a stroked outline.
2. The fill sits **offset by 8–9px** from the outline (`transform="translate(-9,7)"`). That
   misregistration is the whole trick: it reads as a two-pass print that didn't line up.
3. Fill gets `#rough2`, outline gets `#rough` — different seeds, so the two passes wobble
   independently, like two separate hand passes.
4. Stroke: `stroke-width:7`, `stroke-linecap:round`, `stroke-linejoin:round`. Never thinner — the
   filter eats thin strokes.
5. Art occupies the bottom ~40% of the slide, 600–900px wide. Undersized art reads as dead air —
   scale is the fix, always.

**Draw only what survives the treatment.** The vocabulary is geometric and diagrammatic: boxes,
windows, terminals, arrows, flows, bars, charts, checkmarks, crosses, cursors, nodes, speech
bubbles, stacks, sliders. That covers the whole AI-for-builders subject.

Do **not** attempt figurative subjects — faces, animals, hands, objects with organic contours. Clean
geometry plus a wobble filter reads as authored; a generated apple reads as clipart with a tremor.
If a piece genuinely needs a figurative drawing, draw it by hand, scan it, and drop it in
`design/art/` — the system accepts a real `<img>` there.

---

## Why this is not the Anthropic look

The screenshot that started this uses the same *structure*: hand-drawn irregular outline plus a
flat fill in slight misregistration. That structure is a printing idiom, not a proprietary asset,
and it's the same idea `habitosqueabracam` uses with ukiyo-e in `examples/carousels/`.

Every material choice underneath it is different:

| | Anthropic | Alvinegro |
|---|---|---|
| Ground | warm cream | pure white, and black half the time |
| Fill | flat warm grey | halftone dot screen, pure black or white |
| Type | soft serif | heavy grotesque |
| Register | gentle, editorial | high contrast, poster |
| Accent | a color (coral) | inversion |

Soft type + soft drawing reads as the Anthropic register. Crude drawing against a hard, heavy
grotesque is a different tension — and it's what makes `souantisocialmedia` and `okaashish` feel
authored rather than templated.

---

## Open items

- **Figurative art library.** `design/art/` doesn't exist yet. Create it when a piece needs a drawn
  subject the geometric vocabulary can't carry.
- ~~**Reading mode.**~~ Closed 2026-08-20 — Newsreader, white ground only. See Typography above.
- ~~**Brand book.**~~ Closed 2026-08-20 — 17 pages in `design/brandbook/`. Logotype route decided:
  stamp as the mark, masthead as the header structure.
- **Visual tone reference.** The book's tone page (13) states the register in words. A real reference
  board — scanned newsprint, actual broadsheets — would pin it harder than adjectives do.
