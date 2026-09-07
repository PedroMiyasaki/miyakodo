---
id: subtitles
phase: render
---

# Feature · Subtitles

## What it does
Burns captions into the video (does not rely on Instagram's auto-caption).
Three things define the look, and only the first is mechanical:

- **Sentence case**, as transcribed. Uppercase only where the language wants it
  — names, acronyms, the start of a sentence. Never a blanket `.upper()`.
- **Words accumulate two at a time inside a block**, then the block clears and
  the next one starts. Not a fresh pair flashing every 400ms.
- **The Alvinegro faces**: Bricolage Grotesque ExtraBold for the line,
  Newsreader italic for a word under emphasis, which also inverts.

The file is `<edit>/master.ass` — **ASS, not SRT**. SRT carries exactly one
style for the whole file and ffmpeg's SRT parser strips `{\...}` override tags
*silently*, so per-word emphasis renders as plain text and you think it worked.
ASS was the upgrade path this feature was always pointing at; it is now the
only path.

The timeline is the **output** timeline (after the dead-air cuts).

`video-use` Hard Rule 1: subtitles go in **last** in the composite — no overlay
may cover them.

## On by default — final render only

Every mode ships burned-in captions. **But they are burned only on the final
render**, never on a preview.

The reason is cost, not taste. Building `master.ass` is cheap (it reads the
cached transcripts off disk), but burning through libass forces a full re-encode
of the composite, and previews exist to be re-rendered a dozen times while the
cut is still moving. Captions on every iteration would tax each round-trip for
an output nobody is reading yet.

| Render | Captions |
|---|---|
| `--preview` (iteration) | **never** — no `--subtitles`, no `master.ass` |
| `final.mp4` (after "done") | **always**, unless the user turned them off |

The user turns them off by saying so ("sem legenda", "no subtitles", "skip the
captions"). Then the final renders like a preview: no `subtitles` in the EDL, no
`--subtitles`, no `master.ass`.

The words being burned are the ones already approved in the previews, so there
is nothing to review twice — the cut is locked before the captions exist.

## The two styles

`master.ass` ships a `[V4+ Styles]` block with exactly two entries. Every size
is written as a fraction of the real output height, and `PlayResX/Y` is the real
canvas, so the same numbers hold whatever the phone shot.

| Style | Face | Look |
|---|---|---|
| `BODY` | Bricolage Grotesque ExtraBold | White, **no outline** — a drop shadow is the only separation from the footage. The default for every cue. |
| `EMPH` | Newsreader italic, 2pt up | **Inverted** — near-black glyph inside a fat white outline. Reads as a highlighter over footage. |

`BODY` running edge-free is a deliberate call, and it is the one setting that
depends on the footage: white on a blown-out wall or a white shirt survives on
the shadow alone, but only just. If a take is bright enough to lose the text,
raise `Shadow` before you reach for `Outline` — the black edge is what made the
old captions read as auto-generated.

`EMPH` is the brand's accent, and the brand has no accent *colour*:
`design/identity.md` says inversion is the accent, and this is inversion. Do not
introduce a hue to make a word pop. The serif italic against the grotesque is
already a hard tonal break — that plus the inversion is the whole device.

Switch mid-cue with `\r<style>`:

```
Dialogue: 0,0:00:03.10,0:00:04.40,BODY,,0,0,0,,não vai\h\h{\rEMPH}substituir{\r}
```

`\rEMPH` restores *every* property of that style, `BorderStyle` included — no
other tag can change border style inline. `\r` alone returns to the cue's own
style. The `\h\h` before it is load-bearing: `EMPH`'s outline is fat enough to
swallow a normal space and butt the words together.

**Fonts.** Neither face is installed on Windows. The TTFs live in
`assets/fonts/` and the renderer copies them into `<edit>/fonts/`, which is
passed as `fontsdir=fonts` — relative, because an absolute Windows path breaks
the filter arg on the drive colon. If a caption comes out in a fallback sans,
that copy is what failed.

## How to run it

At the final render — not before:

1. In `edl.json`, declare `"subtitles": "master.ass"` (path relative to
   `<edit>/`).
2. Run the renderer **with** `--subtitles`. It builds `master.ass` from the
   transcripts + ranges and burns it via libass:

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/render_vertical.py \
  "<edit>/edl.json" -o "<edit>/final.mp4" --subtitles
```

3. **Pass the generated `master.ass` through the edit below**, then run the same
   command again to burn the edited file.

The renderer only builds `master.ass` when it is missing — an existing one is
reused as-is, so your edit survives re-renders. To start over from the
transcripts, delete the file.

## The edit — the part that stops it looking auto-generated

The generator is deliberately dumb. It groups on punctuation, caps blocks at six
words, reveals two at a time and wraps at eighteen characters. That is a
skeleton with a correct pulse, not a finished caption track. **Read it against
the audio and edit it.** Three moves, in order of how much they buy.

### 1. Regroup by breath, not by count

A block should be a unit someone would actually say in one push. Merge or split
the generator's blocks until they are — then vary the length on purpose.

| Line does this | Block |
|---|---|
| Runs, connects, sets up | 5–6 words, revealed in three steps |
| Lands, turns, contradicts | 2–3 words, one or two steps |
| **The punchline** | 1–2 words, alone, nothing before it on screen |

The variation *is* the effect. A six-word block followed by a two-word block
reads as acceleration even though nothing moved.

### 2. Vary how a block assembles

Two words at a time is the default, not a rule, and the generator applies it
uniformly because it cannot hear the take. You can.

- A line delivered fast can arrive **whole** — one cue, no reveal.
- A list can arrive **one word per step**, each item landing on its own beat.
- A turn can **hold the setup, then drop the last word alone** after a longer
  gap than the speech strictly needs.
- A line can break where the *voice* breaks, not where eighteen characters ran
  out. Move the `\N`.

Nothing here is a fixed behaviour to reproduce. Watch what the delivery does and
build the block that matches it.

### 3. Emphasise the words the delivery already hits

Two devices, and they stack:

**Isolation** — give a word the frame to itself and hold it a beat longer than
the speech needs. Free, and it works on any word.

**`\rEMPH`** — the serif italic inversion, for the word the whole line exists to
deliver. Budget: **2–4 in a 45-second Reel, at most one per block.** More than
that and every word is emphasised, which is the same as none. A word marked
`EMPH` should be one you would lean on if you read the line out loud; if you are
reaching for the second one in a block, the first was the wrong choice.

### 4. Hold through the pause

The generator already extends a block's last cue up to 0.6s into the silence
after it, stopping before the next block and never across a segment's hard cut.
Lengthen those holds where the delivery actually rests, and shorten them where
the next line comes in hot. Never bridge a cut.

### Where the line is
The subject is serious; the captions carry the seriousness. No karaoke word-pop,
no bounce, no per-word colour cycling, no emoji. What is borrowed from viral
editing is **pacing and one emphasis device** — the sense that the text is
reacting to the speech instead of ticking alongside it.

`\t` (animated transforms) and `\fad` work in ASS and are deliberately not used.
If a Reel ever needs motion on a word, that is a decision about the system: it
goes in this file first, with a budget, or it does not get used.

## Self-eval
On the final (the previews have no captions to check):

- **Case** — sentence case, not a wall of caps.
- **Rhythm** — scan the block sizes down the file. **If every block is six words
  revealed in three even steps, the edit did not happen.**
- **Emphasis** — count the `\rEMPH` runs. More than ~4 in a 45s Reel means back
  off. Zero is also a finding: a Reel with no line worth leaning on is usually a
  script problem, not a caption one.
- **Fonts** — the burn is grotesque, not a fallback sans. If it looks like
  Arial, `<edit>/fonts/` is empty.
- **Hard Rule 1** — no overlay hides the captions' band. If one does, reposition
  the *overlay*, never the captions.

**They share the lower third with the news/reference cards.** The caption block
sits at 31.25% of the frame height from the bottom and **grows upward** as words
accumulate, so a three-line block reaches higher than a one-line block does. The
card is centred in the lower third at ~70% of its height. That was already a
couple of percent of air with fixed-height SRT cues; with a block that grows, it
is the accumulating cues you have to check, not the first one. If they touch,
move the **card** up (`news_insert.py`'s geometry), never the captions down.

An overlay window that moves here needs the final re-rendered, so check it
before handing the file over.

## Self-check
`assets/test_captions.py` asserts the accumulation, the contiguous reveal steps,
the hold-through-pause bounds and the preserved case, then burns a frame to
prove the fonts resolve and `\rEMPH` survives libass:

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/test_captions.py
```
