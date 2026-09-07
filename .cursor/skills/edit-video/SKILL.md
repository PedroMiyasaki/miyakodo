---
name: edit-video
description: >
  Use when editing a talking-head video into a finished Reel — "edit this
  video", "turn this into a Reel", "edit it in news mode", or when a file in
  video/inputs/ needs editing.
---

# SKILL · Edit video (Reel)

Project layer on top of the `video-use` skill. `video-use` is the generic engine
(transcription, cutting, concat, loudnorm, compositing) and carries the
production-correctness rules. This skill does not reimplement the engine: it
picks a **mode** (a collection of **features**) and runs each feature.

## Architecture

| Layer | Where | Role |
|---|---|---|
| **Feature** | `assets/features/<id>.md` | One editing capability (what + how) |
| **Mode** | `assets/modes/<id>.md` | Ordered list of feature ids |
| **Orchestrator** | this `SKILL.md` | I/O, invariants, mode choice, protocol |

Current features: `cut-dead-air`, `subtitles`, `loudnorm`, `news-inserts`,
`zoom-emphasis`, `black-and-white`, `pop-it`, `motion-third`.
Current modes: `baseline`, `news`, `authority`. Only the `motion-third` helper
(opt-in, blocks no mode) and the visual micro-zoom of `pop-it` are still
missing — see `assets/modes/authority.md`.

To add a new capability: write `assets/features/<id>.md`, then reference it from
an existing mode or create `assets/modes/<id>.md`. Do not embed new feature
logic in this file.

Every feature declares a `phase` in its frontmatter — run them in the mode's
order, grouped by the pipeline's natural phases:

1. `edl` — builds `ranges` (and whatever else the feature changes in the EDL)
2. `plate` — effects on the talking-head (`plate_effects`: zoom, B&W, pop-it)
3. `overlays` — generates clips and fills `edl.overlays` (news, motion)
4. `render` — calls `render_vertical.py` with the feature's flags (loudnorm;
   `subtitles` on the final render only — `assets/features/subtitles.md`)

## Invariants (every mode)

- **No 9:16 conversion.** Preserve the source framing/resolution.
- **The talking-head is never resized or cropped.** Reference images
  (`news-inserts`) are a **floating card** composited over the video, always
  — they never reserve space nor force a crop/pillarbox. In `news` each card
  is brief (a few seconds, synced to the subject being spoken about) and goes
  away; it does not have to cover the whole piece nor hold until the next
  subject. See `news-inserts.md`. In `authority` / pedagogical content the
  editor **judges beat by beat** where the emphasis has to land (face
  vs diagram); when in doubt, empty third. See `motion-third.md` § Editorial
  judgement.
- **Editor notes:** directions the user speaks to the editor mid-take, in
  whatever words come out — **obey** them in the edit and **cut** them from the
  deliverable (audio, image and subtitles). They are never announced, follow no
  format, and are **not bounded by the feature list below** — the user is
  briefing an editor, not filling in a form. Watch for them on every take. See
  § Editor notes.
- Follow `video-use`'s Hard Rules (per-segment extract + concat `-c copy`,
  30ms fade, overlay with `setpts`, never cut inside a word, word-level ASR,
  transcript cache, confirm the strategy before executing, outputs in
  `<edit>/`).
- **Subtitles ship by default, on the final render only.** Every mode gets
  burned-in captions, but never on a preview: they are burned once the cut is
  locked, so iterating on the edit never pays for the re-encode. The user turns
  them off by saying so. Sentence case, the Alvinegro faces, words accumulating
  two at a time, one serif-italic inversion for a word under emphasis — and the
  generated file is a skeleton you edit by hand before burning. See
  `assets/features/subtitles.md`.

## Editor notes
Mid-take, the user stops narrating and talks to **you** instead. There is no
required phrasing and there are no markers to look for — recording is already
enough work without remembering a syntax. Notes come out however they come out,
in English or pt-BR:

> “Editor, corta essa parte, vou falar o final de novo.”
> “corta, vou falar de novo”
> “open editor note, on that impression bit go black and white, close editor
> note” — the old marker form still reads as a note, it is just no longer
> required

**Assume every recording has them.** Read the packed transcript the way a person
would, not as a pattern match: a note is any stretch aimed at whoever is cutting
the video rather than at the audience. The tells are addressing the editor,
talking *about* the video instead of *inside* it, abandoning a sentence to
restart it, or narrating an intention (“vou falar de novo”, “deixa eu refazer”)
instead of an idea. If a line only makes sense to the person editing, it is a
note.

**The boundaries are yours to judge.** A note usually runs from where the
delivery breaks to where the next real take starts, with a pause on either side.
When the edge is ambiguous, cut slightly wide rather than leave a fragment of the
note in the deliverable — and say what you cut.

### What to do with the note
1. **Read and apply it.** The note governs the edit of the stretch it comments
   on (usually the VO right before or right after the note block).

   **Do not start by asking which feature it is.** Ask what the user wants the
   video to do, then reach for the cheapest thing that does it, in this order:
   a feature in the mode → a feature outside it → a knob in the render that no
   feature wraps (a range boundary, the order of two ranges, a level, a caption
   style or position, a margin, a duration) → something that would have to be
   built. Only the last one is a conversation; the first three you do and
   report.

   **A note is not required to name anything this skill has a word for.** The
   feature list is the implementation's vocabulary, not the vocabulary of
   someone talking while filming, and the two will not line up. Treat every
   note as a direction to an editor who is expected to figure out how — because
   that is what it is.
2. **Cut it from the final video.** Remove the whole note — the direction plus
   whatever botched take it belongs to — from the output timeline, on a word
   boundary. The note does **not** go into the audio, does **not** go into the
   subtitles, and does **not** produce an effect over the words of the note
   itself.
3. **Log it** in `<edit>/project.md` (note text → effect applied → `start/end`
   cut from the source).

### Examples — shapes, not a menu

Eight notes that came up early. They are here to show the **range** a note can
have, not to be the set of notes that exist. A note resembling none of these is
not an unrecognised note — it is the ordinary case, and answering it by hunting
for its nearest row below is how you end up doing something adjacent to what was
asked instead of the thing itself.

| Spoken note | Typical effect |
|---|---|
| “on that impression bit, go black and white” | `black-and-white` on the adjacent impression |
| “do a quick punch-in on ‘you’re wrong’” | `zoom-emphasis` `fast` on the payoff |
| “pop-it on safe, reliable and auditable” | `pop-it` on those three onsets |
| “show the screenshot of the paper here” | `news-inserts` in the third (image from the folder / search) |
| “animate the retrieve → rank → generate flow” | `motion-third` on that beat |
| “don't put anything in the third on this part” | empty third; clean plate |
| “cut this bit, I messed up” / “corta, vou falar de novo” | drop the abandoned take and the note |
| “corta todo esse final que eu falei de X” | drop **every** take covering X, back to where that stretch begins |

Full example, from a real take:

> …“Nesse contexto, se você pagar, por exemplo, a assinatura da OpenAI…”
> **“Editor, corta essa parte, vou falar o final de novo.”**
> “Mas você vai ver que os da Anthropic tão muito altos na coluna de custo…”

Deliverable: the abandoned OpenAI sentence **and** the direction are both gone,
and the piece continues on the retake. Nothing signals that a note was there.

A note can also reach backwards well past its own take:

> **“Corta todo esse final que eu falei dos modelos da Anthropic serem bons,
> corta tudo isso. Eu vou falar só o finalzinho agora.”**

That one scopes by **subject**, not by proximity — find where the Anthropic
stretch begins and cut from there, not just from the sentence before the note.
(The subtitles are built from the output timeline, so a note cut in the EDL can
never surface in them.)

### Hard rules
- **Never leave a note in the deliverable.** When you cannot tell whether a line
  is a note or content, treat it as a note: cut it and tell the user. Shipping a
  Reel where he is heard talking to his editor is the one unrecoverable failure
  here.
- **Report every note before rendering** — what was said, how you read its
  scope, what you cut, and what you did about it. That is the user's only chance
  to catch a note you scoped too wide or too narrow. A note you decided *not* to
  act on gets reported too: saying nothing reads as "handled", and the user
  finds out on the deliverable.
- Note contradicts the mode's default judgement → **the note wins** (it is the
  user's direction).
- **A note you cannot act on is answered, never quietly dropped.** If nothing in
  the pipeline does what it asks, say so plainly, name the closest thing that is
  reachable, and let the user choose. Building something new mid-edit is a
  conversation rather than a decision you make alone — but "no feature covers
  this" is never a reason to leave a note unmentioned.

## Prerequisites

- `video-use` installed (`~/.claude/skills/video-use/`) with `ffmpeg`/`ffprobe`
  on the PATH and `ELEVENLABS_API_KEY` resolving (in the environment or in
  `video-use`'s `.env`, **never** in the content repo).
- Scripts: `assets/news_insert.py`, `assets/render_vertical.py`,
  `assets/fonts/`.

## Input and output

- **Input:** `video/inputs/`. No file named → the **most recent** one (highest
  mtime). Only disambiguate if the request names a file that does not exist.
- **Scratch:** `edit/<slug>/` at the repo root (= `<edit>`). Outside `video/`'s
  git.
- **Output:** on "done", **one folder** — `posts/script/<slug>/`, the script's
  own folder, where its `sketch/v<N>.md` history and its `final.md` already
  live — holding all three artifacts side by side:

  | File | What |
  |---|---|
  | `reels.mp4` | the cut, with burned-in subtitles |
  | `caption.md` | the Instagram caption |
  | `cover.png` | the cover (its `cover.html` source stays in `sketch/`) |

  They ship together and they live together: posting a Reel means opening one
  folder and finding everything it needs there. The video is not delivered
  without its caption and its cover, and none of the three goes anywhere else.

  **The filenames are fixed and generic — never build them from the slug.** The
  folder is already named for the piece, so repeating it inside would say the
  same thing twice; every Reel folder holds the same three names, which is what
  makes them scannable side by side. `reels.mp4` / `caption.md` / `cover.png`,
  in every folder, always.

## Protocol

### 1. Source + inventory + transcription
Source = the named file or the most recent one in `video/inputs/`. `video-use`
helpers: `ffprobe`, `transcribe.py` (cached), `pack_transcripts.py`. Define the
**slug** (title → lowercase, no accents, hyphens). Scratch in `edit/<slug>/`.

**That slug is the script's slug.** A Reel starts life as a script, so the
deliverables land in that script's existing folder, `posts/script/<slug>/`,
beside its `sketch/` history and its `final.md` — which is the script; there is
no separate copy of it in the folder. If `posts/script/<slug>/` does not exist
(a video with no script behind it), create it and write the deliverables in;
there is simply no `sketch/` and no `final.md`.

Right after packing the transcript: read it end to end hunting for **editor
notes** (§ Editor notes) — assume there are some. Extract each one, plan its
effect, and mark the whole span for cutting in the EDL — **before** picking
feature beats “on autopilot”.

### 2. Pick the mode
1. If the user names a mode (or an alias), use it.
2. Otherwise, if the transcript cites a concrete news item (new model, funding
   round, acquisition, research) → `news`.
3. Otherwise → `baseline`.

Read `assets/modes/<id>.md` with the Read tool. Confirm the strategy (mode +
features) with the user before executing. `subtitles` rides on every mode
without being listed in one — drop it only if the user says so.

### 3. Load and run the features
For each feature listed in the mode (+ explicit opt-ins), **in this order**:

1. `Read` `assets/features/<id>.md`
2. Do what the file says, in its `phase`

Before the render, `edl.json` must exist (`video-use` format: `sources`,
`ranges` on word boundaries, `grade`, `overlays`). No overlay features →
`overlays: []`. **No** `subtitles` key in the EDL while you are previewing —
it goes in at the final render (§ 5), or never, if the user turned them off.

Iterate on previews (loudnorm = without `--no-loudnorm`; **no** `--subtitles`):

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/render_vertical.py \
  "<edit>/edl.json" -o "<edit>/preview.mp4" --preview
```

Re-render the preview as many times as the cut needs. Subtitles stay out of
every one of them — see § 5 for the final.

### 4. Self-eval (step 7 of video-use)
`timeline_view` on the output at every cut boundary and overlay window. Check
for discontinuity, audio pops and misaligned overlays (Hard Rule 4). `ffprobe`
the duration. Up to 3 passes; if it persists, flag it. **Ask the user to listen
to the cut junctions** (you do not hear audio).

The subtitle check (Hard Rule 1 — no overlay covering the bottom band) belongs
to the final, since the previews carry no subtitles. Overlays that already sit
low in the frame are the ones to watch.

### 5. Delivery
"Done" is the signal that the cut is locked — and the only moment the final
render happens. Add `"subtitles": "master.ass"` to `edl.json` and render with
`--subtitles` (drop both if the user turned subtitles off):

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/render_vertical.py \
  "<edit>/edl.json" -o "<edit>/final.mp4" --subtitles
```

Say the subtitles are being burned before you start — this render is slower than
the previews, and it is the first one that has them.

**The first pass generates `master.ass` from a dumb rule — six-word blocks,
two words revealed per step. Do not ship that.** Regroup by breath, vary how
each block assembles, mark the payoff words `\rEMPH`, adjust the holds — § The
edit in `assets/features/subtitles.md` — then run the same command again to burn
the edited file (an existing `master.ass` is reused, never regenerated over).
That edit is where the captions stop looking auto-generated; it is a listening
pass, not a formatting pass.

Then check the subtitles (§ 4) and ship the three artifacts into the piece's
own folder — the cut, its caption and its cover, all in `posts/script/<slug>/`.
The folder almost always exists already (the script was written there), so the
`mkdir -p` is a no-op safeguard for the scriptless case, not what creates the
piece.

```bash
mkdir -p "posts/script/<slug>" && mv "<edit>/final.mp4" "posts/script/<slug>/reels.mp4"
```

If the user reopens the cut after this, go back to previews — a further edit
re-renders the final from scratch.

Then write `posts/script/<slug>/caption.md` — the Instagram caption for that
Reel, in the language actually spoken in the video. It lands next to the video
it belongs to, not in a folder of its own.

**The caption is two lines, not a rewrite of the Reel.** The video already said
everything; the caption's whole job is to land after it and ask for the follow.

```
<one short line that hooks off what the Reel just said>
siga @pedro.miyasaki.ia
```

The first line is a **single sentence** that only makes sense to someone who
just watched. It names the Reel's subject and turns back to the viewer — check
the surprise, open the comments, or ask where they stand. It does not summarize
the video, does not repeat the hook, and does not teach anything new.

The follow line is always the second line. The handle is verbatim; the verb
follows the language spoken in the video (`siga` / `follow`).

Each block below is one whole caption, for a different kind of Reel:

```
# Reel: what the terminal bench is (baseline · explanatory)
E aí? Sabia que o terminal bench era assim?
siga @pedro.miyasaki.ia

# Reel: a new model announcement (news)
Esse lançamento me pegou de surpresa. Você já tinha visto?
siga @pedro.miyasaki.ia

# Reel: how guardrails actually work (authority · pedagogical)
Ficou com alguma dúvida? Coloca nos comentários
siga @pedro.miyasaki.ia

# Reel: "RAG is a crutch" (baseline · thesis)
Concorda ou acha que eu tô viajando?
siga @pedro.miyasaki.ia

# Reel: the mistake everyone makes when writing evals (authority)
Já perdeu tempo com isso também?
siga @pedro.miyasaki.ia

# Reel recorded in English: why your agent keeps looping
Wait — did you know it worked like that?
follow @pedro.miyasaki.ia
```

What it must never look like — the Reel rewritten as text:

```
# ✗ wrong
O terminal bench é um benchmark que mede a capacidade de agentes de IA
resolverem tarefas reais em um terminal. Nesse Reel eu explico como ele
funciona, por que ele é difícil e o que os resultados dizem sobre...
```

Present the caption in the chat too, so the user can correct it before posting.
Corrections rewrite `posts/script/<slug>/caption.md` in place — it is a build
artifact next to the render, not versioned as `v<N>`.

#### The cover
The Reel also ships a cover — the frame that holds the grid, so it is composed,
never a grabbed still. Its render lands in the same `posts/script/<slug>/`
folder the cut and the caption ship to; the HTML source is a build intermediate,
so it stays in `sketch/`. Build it in the **Alvinegro** system, not improvised:
read `design/identity.md` and copy the `01 COVER` archetype from
`design/templates/slides.html` (`<style>` and `<defs>` included) into
`posts/script/<slug>/sketch/cover.html`.

- **Frame 1080×1920 — 9:16, the Reel's own aspect**, so the cover fills the
  Reels tab instead of sitting letterboxed inside it.
- **The archetype is 1080×1350, so the copied CSS has to be overridden.** Add
  `.slide{height:1920px}` in `cover.html` after the `<style>` you copied in.
  The renderer's `--width/--height` only size the *viewport*: the PNG comes from
  the element's own CSS box, so without that override the cover renders 4:5 no
  matter what the command line says. Check the rendered pixel size before
  shipping — 3240×5760 at the default `--scale 3`.
- **The grid crops it back to 4:5, from the middle.** Anything that has to be
  read at thumbnail size — the hook above all — belongs inside the central
  1080×1350. The ~285px above and below are bleed: the mark and the line art can
  live out there, and the extra height is air, not a licence for a third size.
- Inverted slide (`.slide.inv`), the `@handle` mark, `.hook` display line,
  optional `.bd` support line, optional line art from the drawing vocabulary
  (boxes, arrows, flows, terminals — nothing figurative).
- The hook is the Reel's own opening line, tightened to fit — not a new claim
  and not the caption's first line.
- Strictly black and white. No palette, no typeface, no logo outside the system.

```bash
uv run python scripts/render_html_to_pngs.py \
  --html "posts/script/<slug>/sketch/cover.html" \
  --out "posts/script/<slug>/sketch" \
  --selector ".slide" \
  --width 1080 --height 1920
mv "posts/script/<slug>/sketch/1.png" "posts/script/<slug>/cover.png"
```

The renderer names by sequence, and one `.slide` renders as `1.png` — hence
the rename. It renders into `sketch/` and the finished cover is moved out, so a
failed rename leaves a stray `1.png` in the working material rather than beside
the deliverables.

Show the render to the user. Corrections edit the HTML and re-render — `sketch/`
is working material and the slug root holds only what gets published; the
deliverables are regenerable, never versioned as `v<N>`.

The scratch in `edit/<slug>/` can be discarded.

## Wiring

| Piece | Where |
|---|---|
| Features | `assets/features/*.md` |
| Modes | `assets/modes/*.md` |
| News insert CLI | `assets/news_insert.py` + `assets/README.md` |
| Render | `assets/render_vertical.py` (legacy name; does not force 9:16) |
| News images | `video/inputs/<slug>-imagens/` (manual wins) |
| Engine | `~/.claude/skills/video-use/` |

Session memory: `<edit>/project.md` (`video-use` format).
