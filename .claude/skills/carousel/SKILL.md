---
name: carousel
description: >
  Produces a complete Instagram carousel end to end: reads an idea from the
  Ideas database, writes the slide copy and caption in the user's voice, then
  composes and renders the slide art as 4:5 PNGs. Activate with commands like
  "write the carousel for the last idea", "make a carousel", "render the
  carousel <slug>", "redraw the carousel art", or when feedback is about empty
  space, weak hierarchy or storytelling in carousel slides. Not for thread
  X-cosplay carousels (that is build-thread-carousel).
---

# SKILL · Carousel

Turn a raw idea into a finished carousel: copy **and** art, in one pass. Copy and composition are
one deliverable here — the headline is the anchor, the template only locks if the copy has a
repeating shape, and a copy fix is often the right answer to a visual problem.

Act as a senior copywriter and art director on the same piece.

---

## Required reading — before writing anything

1. **`assets/carousel-craft.md`** — the craft standard. Identity slots, the five principles derived
   from the viral corpus in `examples/carousels/`, the frame contract, the type scale, the forbidden
   list and the pre-ship checklist. **Read it in full on every run.** Where this file and the craft
   doc appear to disagree, the craft doc wins.
2. **`docs/voice/base.md`** — the base voice for every piece. If the user names a layer, read it
   from `docs/voice/layers/` too; a layer beats the base where they disagree.
3. **`design/identity.md`** — the visual system (Alvinegro). It fills every identity slot the craft
   doc requires, carries the type scale, and specifies how the artwork is drawn: clean SVG geometry
   torn up by an `feTurbulence` + `feDisplacementMap` filter, with a halftone fill offset from the
   outline. Copy the `<style>` and `<defs>` from `design/proof/proof.html` as the starting point.
   Do not invent a palette or typeface — the system is defined. Only ask the user when a piece needs
   something the system has no value for.
4. On the first run of a session, or when feedback is about composition: read 3–4 PNGs from
   `examples/carousels/<account>/`. Extract the principles; copy no account's aesthetic.

There is no audience or pillar document. If the piece needs a target reader or an angle, ask.

**Language of the piece:** English by default. If the user asks for pt-BR (or any other language), write it in that language — follow their lead, do not push back. `docs/voice/base.md` still applies as principle; its Tier 1/Tier 2 word lists are English-specific and do not transfer (see `CLAUDE.md` for the pt-BR equivalents).

---

## Notion

| Object | ID |
|---|---|
| **Ideas** (data source) | `e2970ca3-7724-4a81-8f12-7ea34c048c67` |

Read the idea at the start; write `Status` and `Format` at the end. That is the only write.

---

## When to activate

Any request that means "turn an idea into a carousel" — "write the carousel for the last idea",
"carousel for idea X", "make a carousel" — **and** any request about carousel art: "render the
carousel `<slug>`", "redraw the art", "too much empty space", "no impact", "weak hierarchy".

**Entering mid-flow:** if `posts/carousel/<slug>/sketch/v<N>.md` already exists and the request is
about art, skip to Step 7 and work from the highest version. If the request is a copy change on a
piece already rendered, edit the copy (new `v<N+1>`), then re-render.

---

## Part 1 · Copy

### Step 1 · Pick the idea

If the user did not name one: open **Ideas**, filter `Status = "Pending"`, sort by `Date`
descending (fall back to `createdTime`), take the most recent, and confirm:

> "Idea selected for the carousel: [title]. Go ahead with this one?"

If they named one, find it and use it directly.

### Step 2 · Define the angle

Read the whole row — title, raw text, notes, date, status. The idea is raw. Extract:

- **Angle** — the position taken on the topic, not the topic
- **Unit** — what the carousel is a list of: steps, findings, habits, moments, mistakes (P1)
- **Core argument** — the thesis in 1–2 sentences
- **Proof** — the numbers, artifacts, named things or exact scenes that will anchor the claims (P4)
- **The reframe** — what the penultimate slide says that the list alone doesn't (P5)
- **The ask** — one word to comment, or one question with an obvious answer (P5)
- **ACP Phase**

### Step 3 · Choose the density mode

Per the craft doc, pick one deliberately and hold it for the whole piece:

- **Recognition** — one sentence per slide, big type, high swipe speed, built to be tagged.
- **Reading** — 6–8 lines of body per slide, built to be saved. Use when the value *is* the
  information.

Halfway between them works less well than either.

### Step 4 · Decide the slide count

**Hard ceiling: 10 slides.** Instagram caps the carousel at 10 images — an 11th does not get posted.
Cover and CTA take two, so the argument has **eight**. Never ship more than 10.

Do not pad to hit a number. If the unit count exceeds eight, do not truncate the list — merge
siblings, cut the setup slides, narrow the promise on the cover, or send the idea to another format.
The full rule is in the craft doc under **Hard ceiling: 10 slides**; read it before cutting.

Two slides are mandatory: **slide 1 is the cover**, **the last slide is the CTA**. The penultimate
slide is the reframe, never the weakest list item.

### Step 5 · Write the slides

Every slide follows the craft doc's grammar: **headline = the conclusion, stated as a complete
self-contained sentence**, then optional body (the why, the caveat, the example), then optional
proof. The headline is never a label and never a teaser.

**Cover:** names the countable unit and the payoff. A number if one honestly exists. Not a topic.

> Good: "I researched 1540 Reddit posts to see how people are making money with AI"
> Bad: "Everything about AI for business"

**Development slides:** one idea each. Useful functions to combine as the idea requires — problem,
data, contrast, example, framework, insight, objection — but whichever function a slide serves, its
headline still states the conclusion.

Every claim resolves to a number, an artifact, a named thing or an exact scene. Label unverified
claims as unverified; the hedge adds authority.

**Word budget:** recognition mode ~20 words per slide; reading mode up to ~60. If a slide carries
two ideas, split it.

**CTA:** one word to comment, in quotes, with a stated reward — or one question the reader already
has the answer to. Never "what do you think?", never a bare follow-ask.

> "Comment 'SYSTEM' and I'll send the full breakdown."
> "If you could steal one of these this month, which one?"

**Before moving on, run the readthrough test:** read only the headlines, top to bottom. If that
alone is not a coherent article, the headlines are labels — rewrite them.

**Output format:**

```
SLIDE 1 — COVER
Headline: [the unit + the payoff]
Sub: [optional, 1 line]

SLIDE 2 — [function]
Headline: [the conclusion, complete sentence]
Body: [support]
Proof: [number / artifact / named thing / scene, if any]

...

SLIDE N-1 — REFRAME
Headline: [what the list adds up to]

SLIDE N — CTA
Headline: [the ask]
Action: [the one word, or the question]
```

### Step 6 · Caption, then save and iterate

The caption carries the context around the post, not a prose restatement of the slides. First line
must stop the scroll on its own. 2–4 short paragraphs expanding the argument or adding a nuance
that didn't fit. A specific CTA. 3–5 hashtags. 80–180 words, never past 250.

Present slides and caption separately. Derive the slug from the idea title (lowercase, no accents,
hyphens for spaces and punctuation) and save immediately to `posts/carousel/<slug>/sketch/v1.md` —
slides, then `---`, then the caption.

Ask: *"Ready to move to the art, or any more corrections?"*

Each correction creates `posts/carousel/<slug>/sketch/v(N+1).md`: read `v(N)`, copy unchanged blocks
**verbatim**, apply only the diff. Never regenerate what did not change.

---

## Part 2 · Art

Prerequisites, once per machine:

```bash
uv sync
uv run playwright install chromium
```

### Step 7 · Lock the template

The identity is fixed by `design/identity.md` — do not re-decide it. What varies per piece is the
template. State in 3–6 lines and present to the user:

- **The one template**: which slots each slide carries, in what hierarchy, in what position.
- Which slides invert (cover and CTA by default — inversion marks the frame of the piece).
- The drawing per slide, from the geometric vocabulary in `design/identity.md`.
- Where the optical mass sits on each slide, so none falls into dead air.

The locked template is what produces coherence. Position may breathe across slides; elements and
hierarchy do not change. Do not compose slide-by-slide inventions.

### Step 8 · Compose `posts/carousel/<slug>/sketch/carousel.html`

One self-sufficient file, N × `<section class="slide">`, with a `<style>` in the `<head>` carrying
the frame contract, the identity slots and the type scale — all per the craft doc. No external
stylesheet.

**Anti-patterns this skill has produced before:**

1. A tiny mono kicker standing in as the slide title — nobody reads it, and the body then lands with
   no context.
2. `justify-content: space-between` pushing a sliver of text to the top and another to the bottom,
   with a hole in the middle serving no narrative function.
3. Jargon with no effect on the same screen ("16 out of 896 specialists", unexplained).
4. Treating negative space as an excuse for timid typography.

### Step 9 · Render

```bash
uv run python scripts/render_html_to_pngs.py \
  --html "posts/carousel/<slug>/sketch/carousel.html" \
  --out "posts/carousel/<slug>" \
  --selector ".slide" \
  --width 1080 --height 1350
```

PNGs land loose in `posts/carousel/<slug>/` at 3240×4050 (3× device scale). The renderer zero-pads
the filename to the width of the slide count: ten slides give `01.png`–`10.png`, a shorter deck
gives `1.png`–`8.png`. Both sort in slide order; leave the names as they come out.

### Step 10 · QA before presenting

Open the cover, one development slide and the CTA with the Read tool and run the **pre-ship
checklist** at the end of the craft doc — both halves, copy and design. Any failure: fix and
re-render **before** delivering.

### Step 11 · Present and iterate

Present the renders. Use the craft doc's feedback translation table to turn subjective feedback into
a diagnosis before acting.

**A visual problem is often a copy problem.** A headline that overflows the type scale, a slide with
no anchor because the sentence has no conclusion in it, a "boring" slide that carries no number or
scene — fix the copy. That means a new `posts/carousel/<slug>/sketch/v(N+1).md`, then re-render. Do
not shrink the type to fit bad copy.

`sketch/` is the working material — the `v<N>` audit trail and the HTML composition — and it stays
there. The slug root carries only what gets published: the PNGs, and `final.md` at close-out.

### Step 12 · Close out

When the user confirms "done", copy the highest `posts/carousel/<slug>/sketch/v<N>.md` **verbatim**
to `posts/carousel/<slug>/final.md` — slides and caption, nothing rewritten. That file plus the PNGs
is the deliverable; the `sketch/v<N>` history stays where it is. Then update the source idea in
**Ideas**: `Status` → `"Processed"` and `Format` → `"IG Carousel"`. This is the only write to Notion.

If the user stops at the copy stage and explicitly calls it done there, write `final.md` and the
Notion update then.

Deliver the paths to `final.md` and the PNGs, and report the slide count.

---

## Out of scope

- Capturing raw ideas (`capture-idea`), Reel scripts (`write-script`), threads (`write-thread`),
  LinkedIn posts (`build-linkedin`).
- The X-cosplay thread aesthetic (`build-thread-carousel`).
- Adapting the piece to another platform unless asked.
- Publishing — that is manual, by the user, from the final files.

## Known limitations

- Fixed 1080×1350. Another format means revisiting the frame contract in the craft doc.
- Overflow is not checked automatically; a slide with long text may clip. Review renders before
  approving.
- Webfonts via `@import` in the piece's `<style>`; the renderer waits for `document.fonts.ready`.
  With no network it falls back to system fonts.
- The `ART` slot is only as good as what the identity provides. With `ART: none` the piece runs
  type-only — viable, but the hardest mode to make land (craft doc, §0).
