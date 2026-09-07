# Carousel craft

Working reference for carousels. Derived from a corpus of five viral carousels in
`examples/carousels/` (`calebraalston`, `habitosqueabracam`, `okaashish`, `souantisocialmedia`,
`yasminkbs`) — every rule below is a practice observed in **all five**, across two languages and
five unrelated niches, plus the composition craft that survived contact with that corpus.

**Read before writing copy and before writing HTML.** The `carousel` skill reads this file on every
run and applies it to both halves of the piece. The principles are one system: a locked template
can't rescue copy that buries its conclusion, and a good headline can't survive a slide that has
four other things on it.

---

## 0 · The identity slots

The visual system is not defined yet. It doesn't need to be for this document to work — but a
carousel cannot be composed until these slots have values. **Ask the user, or read them from the
identity doc once it exists, before writing any HTML.** Declare them once in the piece's `<style>`
and never deviate slide to slide.

| Slot | What it is | Corpus range |
|---|---|---|
| `GROUND` | The background. One flat color, every slide. | dark teal / warm paper / white / lime / cream |
| `INK` | The text color. | cream / brown / black / navy / klein blue |
| `ACCENT` | **Exactly one.** Marks one consistent meaning throughout. | pale sage / teal / one blue / none |
| `DISPLAY` | Headline face. | serif, slab, handwriting, grotesque |
| `BODY` | Body face. May be the same as DISPLAY. | sans, serif, same-as-display |
| `MARK` | Brand furniture: masthead, handle, or corner mark. Same place, same size, every slide. | logo lockup / dashed rule + dot / handle / asterisk + label |
| `ART` | The illustration language. One style, used everywhere. May be `none`. | line art / ukiyo-e collage / doodle + mascot / pen drawing / none |
| `TEXTURE` | Optional ground treatment. Subtle or absent. | paper grain / noise / flat |

Rules that bind regardless of what fills the slots:

- **Two type families maximum.** Three of the five corpus accounts use one. Size is the hierarchy;
  there is no third family for "meta".
- **One accent, one meaning.** In `okaashish`, blue means *this is the number or the payoff word* —
  every time, no exceptions. In `habitosqueabracam`, teal means *this is the fact you didn't know*.
  An accent that marks three different things is decoration, not a signal.
- **`ART: none` is viable but is the hard mode.** `yasminkbs` runs 15 type-only slides and works,
  because the type block is enormous and every sentence is a scene the reader recognizes. Four of
  five accounts use an illustration language, and it is their primary thumbnail-recognition asset.
- **The identity must survive the thumbnail test:** shrink a slide to 20% and crop the handle. If it
  isn't identifiable as this account, the slots are set too weakly.

---

## P1 · The cover sells a countable unit, not a topic

The cover tells the reader two things before the first swipe: **what the unit is** and **roughly how
many there are.** Not the subject — the shape of the thing they're about to consume.

> "Hábitos japoneses que você vai querer copiar" → a list of habits you can steal
> "I researched **1540** Reddit posts… here's what I found" → findings from a real dataset
> "Quantity **or** Quality content" → one binary, resolved by a method

A topic is an invitation to *maybe* swipe. A countable unit is a contract: the reader knows slide 2
holds one habit / one stat / one moment, and that there's an end. Finite promises get finished.

- **A number does the work of a paragraph.** `1540 Reddit posts` is the entire credibility argument
  for a 13-slide carousel, in three words. In this niche: a model name, a price, a benchmark
  number, a dated release, a count of things tested.
- **State the payoff, not the process.** "que você vai querer copiar", "Here's what I found",
  "hoje mesmo". The reader is told what they walk away with.
- The cover is the piece's largest typographic gesture. Display at the top of the scale.

**Check:** does the cover name a unit and imply a count? If it names a subject, rewrite it.

---

## P2 · One idea per slide, headline-first — the headlines alone are the article

Every slide follows the same internal grammar:

```
HEADLINE   ← the conclusion, a complete self-contained sentence, readable in ~1.5s
body       ← the support: why, how, the caveat, the example        (optional)
proof      ← the screenshot, the diagram, the illustration          (optional)
```

The headline is **never a label and never a teaser** — it is the finding itself. Not "Automation"
but "**More than 60% are adding AI to traditional services.**" The body then gives context and
caveat. This is inverted pyramid: **conclusion first, setup after.**

> This reverses the old "establish → evidence → effect" rule. The corpus does not spend a slide, or
> the top of a slide, on setup. What it does instead is make the headline self-sufficient: the
> number always arrives with its subject attached, never as a naked figure.

**The readthrough test — the single most useful check in this document.** Read only the headlines,
top to bottom. If that alone is a coherent article, the carousel works. If it reads as fragments,
the headlines are labels and the piece will lose every skimmer.

Carousels are consumed at two speeds at once: a fast skim down the headline layer, and a slow read
of the two or three slides that landed. Both audiences are served by the same file. A slide that
needs the previous slide to make sense breaks the skim layer and loses the skimmer permanently.

**One idea per slide, no exceptions.** Not one topic — one idea. Three steps means three slides. A
four-part formula is one idea and may share a slide, split into four visually separated rows.

---

## P3 · Lock one template; spend novelty on content, never on layout

The most disciplined thing the corpus does, and the easiest to get wrong.

**The template never changes.** Same slots, same hierarchy, same positions, slide after slide.
`yasminkbs`: 15 slides, identical header, identical type size, identical margin, only the sentence
changes. `habitosqueabracam`: a fixed masthead — dashed rule, brand dot, term in display, translation
in condensed caps, serif body, accent pull-quote — five times without deviation.

> This reverses the old "no template, every slide composed on the spot" constraint. That rule was
> producing variety the reader experiences as friction. The eye re-learns a new layout in about half
> a second; across 12 slides that is six seconds of attention spent on navigation.

What is allowed to move: `souantisocialmedia` and `calebraalston` shift the text block and the
illustration around the canvas between slides so the sequence doesn't read as copy-paste. The
**elements and their hierarchy stay frozen**; only their position on the canvas breathes.

**Layout, consistent across all five:**

- **4:5 — 1080×1350.** Maximum vertical real estate in the feed.
- **The headline owns the top third.** Every slide, every account. The bottom third is illustration
  or deliberate air — that's where the IG chrome, the caption preview and the reader's thumb live.
- **Safe margin ≈ 88px (8%).** The corpus runs 8–9%, not the 4% a 48px margin gives.
- **Type scale, measured off the corpus at 1080 width:**

  | Level | Size | Notes |
  |---|---|---|
  | Cover hook | 90–130px | The piece's largest gesture |
  | Slide headline | 70–110px | Tight leading — a block, not a paragraph |
  | Body | 40–56px | Below ~36px is illegible in the feed |
  | Reading-carousel body | 38–44px | Density mode only — see the split below |

- **Whitespace is a level of hierarchy.** `yasminkbs` leaves ~40% of most slides empty and it reads
  as confidence. That works because the type block is enormous — see the dead-air section.
- **No page indicator.** Zero of the five have one; Instagram already draws the dots.

**Two densities. Pick one per piece, deliberately.**

- **Reading carousel** (`habitosqueabracam`): 6–8 lines of body per slide, serif at large size.
  Trades reach for depth. Use when the value *is* the information.
- **Recognition carousel** (`yasminkbs`): one sentence per slide. Trades depth for swipe speed and
  taggability. Use when the value is "this is literally my team."

A carousel that lands halfway between them works less well than either.

---

## P4 · Every claim anchors to something the reader can picture

Not one slide in the corpus argues with adjectives. Each claim resolves to one of four forms:

1. **A number.** `1540 posts`, `60%`, `<5%`, `$3k–$5k`, `£250`, `20–30 minutes`.
2. **An artifact.** `okaashish` pins a real screenshot to nearly every slide. It is often unreadable
   at feed size and that is fine — it isn't there to be read, it's there to prove the claim came
   from somewhere. *In this niche: a thread, a repo, a pricing page, a benchmark table, a dashboard.*
3. **A named thing.** `Tsundoku`, `Ichigo ichie`, "the Accordion Method". A named concept is
   portable — the reader can repeat it to someone else, which is the mechanism behind a share.
4. **An exact scene.** The sharpest form, and the one the corpus leans on hardest:

   > "sem um áudio de 7 minutos antes" — not *bad communication*
   > "a única coisa nova que entra na sua cabeça é notificação do Teams" — not *you're in a rut*
   > "não conta ir num restaurante diferente ou cortar a franja" — pre-empting the reader's excuse

Specificity produces recognition, and recognition is what gets commented and shared. "Be a better
leader" gets a like; "when someone sends 'resolved' without a 7-minute voice note first" gets tagged
to a colleague. You cannot tag someone into an abstraction.

**Hedge in the open.** `okaashish` writes "**I did not verify, though**" and "**Not verified**"
directly on the slides. The honesty adds authority — it reads as someone who actually went to the
source rather than someone selling the conclusion. This aligns with `docs/voice/base.md` §6: name
the source, give the date, or drop the claim.

---

## P5 · The last two slides: reframe, then one low-effort ask

**The penultimate slide is the payoff, never the weakest list item.** It's where the sequence stops
listing and starts meaning something:

> `okaashish` s12: "The real AI money formula" — the answer the previous ten slides earned.
> `habitosqueabracam` s7: "each of these solves a need we have too, it just never got a name here."
> `calebraalston` s5: "Repeat the cycle" — closes the loop the metaphor opened.

**The final slide asks for exactly one thing the reader already has the answer to.** Two shapes:

*Comment gate* — one word, in quotes, with a stated reward bigger than what was just delivered:
> "Comment **'Select'** — if you want the full system for how to make content that gets you customers."
> "Comment **'REDDIT'** — and I'll share the full breakdown."

*Answerable question* — no cognitive work required:
> "If you could steal just one of these habits this month, which one?"

Never "what do you think?" Both shapes narrow the answer to a choice the reader already made while
reading. The follow-ask, if present, comes after and is thrown away as a joke — never the primary CTA.

**The CTA slide may break visual register.** `calebraalston` flips from dark teal to gold for the
final slide. `calebraalston` also runs the CTA in the **footer of every slide**, so the ask never
depends on reaching the end — worth stealing. Both CTA slides in the corpus are dead-centered with
the largest type in the deck; the CTA is the loudest slide, not the soberest.

*Exception, noted so it isn't copied by accident:* `yasminkbs` has no CTA — it ends on the 15th item
and stops. Viable only when the content is pure identification and the share **is** the CTA. Four of
five have an explicit ask; treat "no CTA" as the exception it is.

---

## Craft layer · dead air, optical weight, feedback

**"Too much empty space" almost always means dead air, not too much negative space.**

| | Intentional negative space | Dead air (failure) |
|---|---|---|
| Function | Frames the content, forces focus | Screen left over because the content is too light |
| Feel | Deliberate, it breathes | Unfinished, "text-only-at-the-top" |
| Optical weight | The main block is dense and large | Tiny title + tiny body + huge void underneath |
| Thumbnail | The hook still dominates | Looks like a blank page with one line |

Fix dead air with **scale, typographic mass and grouping** — never by scattering micro-elements into
the corners. `yasminkbs` is the proof: 40% empty, and it reads as confidence because the type block
carries all the weight.

**Terms to use when planning and when explaining a correction:**

- **Visual anchor** — the element carrying the slide. Every slide needs exactly one.
- **Optical weight** — how much an element weighs in the composition.
- **Typographic mass** — text as a solid block: high scale plus tight leading, not a blog paragraph.
- **Grouping (proximity)** — same idea sits close; different ideas get a clear interval.
- **Asymmetrical balance** — weight in one corner offset by weight in another.
- **Figure-ground contrast** — the text has to jump off the ground in the thumbnail.

**Translating subjective feedback:**

| User says | Diagnose |
|---|---|
| "empty" | Dead air or negative space? Missing anchor? Type scale too timid? |
| "no impact" | Weak hierarchy, low contrast, insufficient typographic mass |
| "I didn't get it" | Headline is a label instead of the conclusion, or jargon with no effect on the same screen |
| "boring" | Template locked correctly but the copy failed P4 — no number, artifact, name or scene |

---

## Frame contract (rigid)

1. Each slide is `<section class="slide">`, exactly `width: 1080px; height: 1350px; overflow: hidden`.
   The renderer reads the `.slide` selector.
2. Minimum inner padding **88px** on all sides.
3. Flat `GROUND`. Never a gradient. Inverting to dark is a whole-piece decision, never per-slide.
4. `data-theme="light"` on the root so the render doesn't inherit OS dark mode.
5. Fonts: only the `DISPLAY` / `BODY` families. Declared once, at the top.
6. Render-safe: static final state. No `:hover`, no animation, no JS for content that must appear.
7. `MARK` in the same corner, same size, every slide.

```bash
uv run python scripts/render_html_to_pngs.py \
  --html "posts/carousel/<slug>/sketch/carousel.html" \
  --out "posts/carousel/<slug>" \
  --selector ".slide" --width 1080 --height 1350
```

---

## Forbidden

Stock photography. Gradient. Emoji. Icon libraries. Em dash (—). Cards with shadow + accent border.
Mixed emphasis (bold + color + underline + box on the same phrase). A third type family. More than
one accent color. A decorative slide that carries no sentence — every slide in the corpus, all 51,
carries one. Padding a list to hit a slide count. Hedged headlines — caveats live in the body.

---

## Hard ceiling: 10 slides

**Instagram carousels on this account cap at 10 images. This is a platform constraint, not an
editorial preference — an 11th slide does not get posted.** Cover and CTA are two of the ten, so the
argument has **eight slides** to work with.

This overrides the corpus's "length follows the unit count." When the unit count exceeds eight,
truncating the list is the wrong fix — cutting item 9 leaves a promise the cover already made. Do
one of these instead:

1. **Merge siblings.** Three examples that make the same point are one slide with three lines, not
   three slides. Look for adjacent slides whose headlines could be one sentence.
2. **Cut the setup.** Context, definition and "why now" slides are the usual fat. If the headline of
   a slide is a premise rather than a finding, it is a candidate.
3. **Narrow the promise on the cover.** "The 5 that matter" is a better carousel than a truncated
   list of 9. Change the count on the cover; do not silently drop the tail.
4. **Change format.** A list that genuinely needs 14 units is a thread or a Reel, not a carousel.
   Say so rather than mutilating it.

Never cut: the cover, the reframe, the CTA, or the slide carrying the piece's strongest proof.

---

## Pre-ship checklist

**Copy**
- [ ] Cover names a countable unit and its payoff, not a topic
- [ ] A number on the cover if one honestly exists
- [ ] One idea per slide
- [ ] Every headline is the conclusion, self-contained, complete sentence
- [ ] **Headlines read alone, end to end, as a coherent article**
- [ ] Every claim resolves to a number, artifact, named thing or exact scene
- [ ] Unverified claims are labelled as unverified
- [ ] Penultimate slide reframes the piece
- [ ] Final slide: one word to comment, or one question with an obvious answer
- [ ] Passes `docs/voice/base.md`

**Design**
- [ ] All identity slots filled and declared once
- [ ] One locked template: same slots, same hierarchy, every slide
- [ ] Headline in the top third; bottom third is art or air
- [ ] Ground + ink + at most one accent, and the accent means one thing
- [ ] Two type families maximum
- [ ] One illustration language, or none, consistently
- [ ] 4:5 1080×1350, 88px margins
- [ ] Every slide has exactly one anchor with dominant optical weight
- [ ] Density mode chosen deliberately: reading or recognition
- [ ] Thumbnail test at 20%: still reads, and still identifiable as this account with the handle cropped
