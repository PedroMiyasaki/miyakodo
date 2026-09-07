# CLAUDE.md

This file guides Claude Code (claude.ai/code) when working in this repository.

## What this repo is

This repo holds the user's content production: Reel scripts, threads, carousels and LinkedIn posts. It is not a software project. Everything that looks like "code" here is really content. Production runs through skills plus the Notion MCP.

Practically, that means there is no build, no test suite and no linter. The deliverable is text and image assets, not software.

**Current state: the repo is in transition.** The former brand was removed — strategy documents, visual system and logos are gone — and the new direction, a personal brand, is still being built out.

Rebuilt so far: the base voice (`docs/voice/base.md`), the weekend cadence (`content-routines/default/`) and the visual system (`design/identity.md`). Deliberately absent, not pending: there is no audience document and no content-pillar document — both were dropped to simplify the process. If a piece needs a target reader or an angle, ask the user.

**Language.** The repo works in English: skills, docs, this file, the Notion schema and the conversation. **Published pieces are a separate call** — a script, carousel, thread, LinkedIn post or Substack article ships in whatever language the user asks for, pt-BR included. Default to English when they do not say; follow their lead when they do, and do not push back on it.
## How work flows here

The point of this repo is producing good content with little friction. When the user asks for a post, script, thread, carousel or idea capture, invoke the matching skill and deliver the best possible draft instead of forcing the request through a rigid process.

The flow is direct, with no intermediate brief step: an idea is captured in the **Ideas** database → a content skill (`write-script`, `carousel`, `write-thread`, `build-linkedin`, `write-substack`) reads the idea, then writes and refines the draft locally in `posts/<type>/<slug>/sketch/` for as many iterations as it takes → once the user confirms "done", the final version is copied to `posts/<type>/<slug>/final.md`. There is no intermediate publishing database: the piece lives locally, and the only write back to Notion happens at "done" (`Status` → `Processed`, plus the `Format` that was produced).

Every content production skill carries the same standardized closing step: **record `Status` → `Processed` and the piece's `Format`** at "done". Those two fields are what accumulate the real picture of the calendar in the database — an idea is born without a format, and the format is decided during production. This list of skills is not closed: when creating a new production skill, copy the closing step from an existing one.

**`write-substack` is the one documented exception, and only on its reuse path.** The article rewrites a thesis whose idea was already closed by the Reel, and an idea carries a single `Format`. Writing `Substack` over it would erase the primary format and corrupt the calendar picture the database accumulates, so the reuse path writes nothing to Notion at all. Run standalone on a fresh `Pending` idea, the skill closes it normally with `Format` → `Substack`. Do not "fix" the reuse path to match the other skills.

**`carousel` is the exception to the write-then-build split.** It produces copy *and* art in one skill, because for a carousel the two are one deliverable: the headline is the visual anchor, a locked template only holds if the copy has a repeating shape, and a copy edit is often the right fix for a visual problem. Its craft standard lives in `.claude/skills/carousel/assets/carousel-craft.md`, reverse-engineered from the viral corpus in `examples/carousels/`, and it governs both halves. Threads keep the split (`write-thread` → `build-thread-carousel`), because a thread ships as text and the carousel is an optional derivative.

Skills are invoked through natural English commands (e.g. "write the script for the last idea", "make a carousel", "write a LinkedIn post"), **not** slash commands. They live in `.claude/skills/<skill-name>/SKILL.md` and are discovered automatically. When a request matches one, invoke it via the Skill tool.

`writing-feedback` is the meta-skill: at the end of a production session the user invokes it to consolidate every tone and writing correction made during the conversation into permanent rules in the voice folder — `docs/voice/base.md` by default, or a named layer in `docs/voice/layers/`.

## Content routines

`content-routines/` holds the operating cadence — when the work happens, as opposed to how a single piece is made. `default/` is the normal weekend; `maintainance/` is the travel mode, where nothing is recorded and the week runs on 7 carousels instead of 5 reels. Another cadence (a weekday mode, a launch week) becomes a sibling folder. **A change to the cadence lands in both modes** — the weekly Substack article, for instance, is fired first thing on Sunday and published that same Sunday in each.

The default mode produces and schedules the whole week across two days. Monday to Friday nothing is produced.

| File | What it is |
|---|---|
| `default/README.md` | What the week produces, the 🔥 definition, why the setup is what it is, stock rules |
| `default/saturday.md` | 5 scripts → batch recording → move files → fire the first edit pass |
| `default/sunday.md` | Fire the article → review the 5 cuts → 3 LinkedIn posts → publish and schedule the week |

Output per week: **5 reels (Instagram) + 3 technical LinkedIn posts + 1 illustrated Substack article = 9 posts from 5 recordings.** The LinkedIn posts reuse ideas the reels came from, and the article usually takes one of those deeper still, so one idea works up to three times. The article is the exception that may come from outside the five: it is written and published on the same Sunday, and that zero lag is what makes it the only slot where perishable news is allowed. Its LinkedIn sibling goes out Monday and links back to it, which is where cold reach turns into subscribers. The same 5 Claude Code sessions carry both days: session N writes script N on Saturday, edits video N, and is resumed on Sunday to review that cut.

**When editing these files, keep the split:** the two day files are checklists worked top to bottom with hands busy, so reasoning belongs in the README and only decisions made in the moment stay inline.

## Voice calibration

The base voice for every piece, in every format, is `docs/voice/base.md`. Read it before writing. Layers that stack on top live in `docs/voice/layers/`; when a layer applies, it wins over the base for that piece.

There is deliberately **no audience document and no content-pillar document**. Both were dropped to simplify the process. If a piece needs a target reader or an angle, ask the user — do not reconstruct an audience profile from old content.

## Notion MCP: critical IDs

The idea bank is the only canonical object in Notion. Treat the ID as canonical:

| Object | ID |
|---|---|
| **Ideas** (data source) | `e2970ca3-7724-4a81-8f12-7ea34c048c67` |

Its schema is in English: properties `Idea`, `Notes`, `Date`, `Status`, `Format`, `ACP Phase`. Values — Status: `Pending` / `Processing` / `Processed` / `Discarded`. Format: `Reel` / `IG Carousel` / `Thread` / `LinkedIn Post` — plus `Substack`, **not created yet** (see below). ACP Phase: `A · Audience` / `C · Community` / `P · Product`.

The `Pillar` property was deleted along with the content-pillar document. Do not recreate it.

Notion plays two roles. It is the **read source** for the production skills (`write-script`, `carousel`, `write-thread`, `build-linkedin`, `write-substack`): they read the idea from here, save the content locally in `posts/`, and the only write back is marking `Status` as `Processed` and recording the `Format` at the end (the content itself never goes up). It is the **write target** for idea capture (`capture-idea`, `brainstorm-ideas`, `news-ideas`), which record new ideas in the database. Reads (`notion-search`, `notion-fetch`) are pre-approved; writing to the idea bank (`create-database-row`) asks for confirmation, and that is by design, not a misconfiguration.

**Caution when changing the schema:** renaming a select property's options through the MCP replaces the option set wholesale and silently clears the stored value on every row. Snapshot the rows first, then restore them after the change.

That is why the `Substack` option on `Format` is added **by hand, in the Notion UI** — one click, no risk. As of 2026-09-05 it has not been added. `write-substack` only needs it on its standalone path; if the option is missing there, the skill stops and asks rather than creating it through the MCP.

## Local draft convention

The production skills (script, carousel, thread, linkedin, substack) follow a strict drafting protocol:

1. Slug = title → lowercase, no accents, hyphens replacing spaces and punctuation.
2. The first draft is saved to `posts/<type>/<slug>/sketch/v1.md` at the moment it is presented, where `<type>` is `script`, `carousel`, `thread`, `linkedin` or `substack`, depending on which skill produced it.
3. Every user correction creates `posts/<type>/<slug>/sketch/v(N+1).md` in the same folder. Read v(N), copy unchanged blocks **verbatim**, and apply only the diff. Never regenerate content that did not change.
4. When the user explicitly confirms "done", the highest-numbered `sketch/v<N>.md` is copied to `posts/<type>/<slug>/final.md` — that copy is the publishable piece, and the `sketch/v<N>` history stays put as the audit trail. The skill then updates the source idea in Notion (`Status` → `Processed` and the piece's `Format`; none of the content goes up).

This versioning is deliberate: the local files are the audit trail and the single source of the piece. Publishing is manual, done by the user on the target platform from the final file.

**Translations run on a parallel sequence.** The `traduzir` skill adapts a finished piece into pt-BR and saves it as `posts/<type>/<slug>/sketch/pt-br-v<N>.md`, beside the original's own iterations, with the same diff protocol; at "done" the highest one is copied to `posts/<type>/<slug>/pt-br.md`, next to `final.md`. The sequence is kept separate from `v<N>.md` so the original stays canonical and `final.md` stays the final piece. The layout is the same for every type — there is no LinkedIn special case. `traduzir` runs after "done" and writes nothing to Notion — the `Status` and `Format` update already happened when the original shipped. Its rules live in `docs/voice/base.md` § 9, the only section of the voice guide written in Portuguese.

**Everything for a piece lives in `posts/<type>/<slug>/`, visual assets included.** The folder has two levels. `sketch/` is the working material — `v<N>.md`, the HTML compositions, source images the user drops in — and the slug root holds only what gets published, nothing else:

| Type | Slug root | `sketch/` |
|---|---|---|
| `script` | `final.md`, `reels.mp4`, `caption.md`, `cover.png` | `v<N>.md`, `cover.html` |
| `carousel` | `final.md` (slide copy + caption), `01.png` … `10.png` | `v<N>.md`, `carousel.html` |
| `thread` | `final.md` (the thread text), `01.png` … `10.png` when `build-thread-carousel` runs | `v<N>.md`, `carousel-v<N>.md` (the slide-copy rewrite), `carousel.html`, `images/` |
| `linkedin` | `final.md`, `image.png` (source URL recorded in the `final.md` footer) | `v<N>.md` |
| `substack` | `final.md` (title + subtitle + article with inline image markers + metadata footer), `cover.png`, `01.png` … `NN.png` | `v<N>.md`, `shotlist.md` |

Rendered PNGs sit loose at the slug root — no `render/` and no `editorial/` subfolder — and the HTML composition is a build intermediate, so it stays in `sketch/`. `output/` is gone entirely: every skill writes into `posts/<type>/<slug>/`, `edit-video` included. A Reel is not its own object — it is the script's deliverable, so its video, caption and cover land in that script's own folder.

## Video editing: Reels

The `edit-video` skill turns a talking-head video into a finished Reel. It is a layer over the generic `video-use` skill (which lives in `~/.claude/skills/video-use/` and carries the production-correctness rules): `edit-video` does not rebuild the engine — it picks a **mode** (a collection of **features** in `.claude/skills/edit-video/assets/features/` and `assets/modes/`) and runs each one. Invoked by natural command ("edit this video", "turn this into a Reel", "edit it in news mode"). While recording, the user can speak **editor notes** between `open editor note` and `close editor note`: the skill obeys the instruction during assembly and **cuts** the whole block from the deliverable, so it reaches neither the audio nor the captions.

Current features: `cut-dead-air`, `loudnorm`, `news-inserts`, `subtitles` (**on by default, burned only on the final render** — previews never carry them, so iterating on the cut stays cheap), plus specs for `zoom-emphasis`, `black-and-white`, `pop-it` and `motion-third`. Modes: `baseline` and `news` (implemented) and `authority` (features defined, helpers pending). Invariant: never force 9:16. Input in `video/inputs/` (default = most recent), scratch in `edit/<slug>/` at the root (outside the `video/` git repo), and at "done" the three deliverables land together in the script's own folder, `posts/script/<slug>/`, beside the script that produced them rather than in a separate tree: `reels.mp4` (the cut), `caption.md` (the Instagram caption) and `cover.png` (the cover, composed in the Alvinegro system from the `01 COVER` archetype). The filenames are fixed and generic in every Reel folder — the slug is the folder, never part of the filename. Nothing ships to `video/outputs/` anymore.

## Visual system: Alvinegro

`design/identity.md` is the visual system for every deliverable with its own layout: strictly black
and white, heavy grotesque display, hand-drawn wobble line art with a halftone fill. `design/proof/`
holds a rendered three-slide proof — copy its `<style>` and `<defs>` to start a new piece. **Do not
improvise a palette or typeface**, and do not reintroduce the old brand.

The full brand book is `design/brandbook/book.html` (17 pages, rendered to `render/`). It is the
system *shown*; `identity.md` is the system *stated*, and the markdown is canonical if the two ever
disagree. Alongside it: `design/logotype/` (the stamp mark, badge and masthead, plus the routes that
were explored), `design/templates/slides.html` (eight slide archetypes) and
`design/stationery/stationery.html` (business card and A4 letterhead, digital only). All of them
render through `scripts/render_html_to_pngs.py` — nothing here needs a design tool.

The artwork is generated, not sourced: clean SVG geometry torn up by an `feTurbulence` +
`feDisplacementMap` filter at render time, with a halftone-dot fill offset from the outline. The
drawing vocabulary is deliberately geometric (boxes, arrows, flows, charts, terminals) — figurative
subjects are out of reach for that technique and belong in `design/art/` as real scanned files.

The two carousel skills still work, using their own assets, which live next to them rather than in `design/`:

- `build-thread-carousel` uses archetypes in `.claude/skills/build-thread-carousel/assets/` (`hook-display`, `body-paragraph` and `_carousel.css`, in `default` and `x` modes). The CSS is self-contained: values are inline, with no external import. Name, handle and avatar are placeholders — ask the user before rendering.
- `carousel` keeps its craft standard in `.claude/skills/carousel/assets/carousel-craft.md`: identity slots, five principles reverse-engineered from `examples/carousels/`, frame contract, type scale and pre-ship checklist. It covers copy and design together and survives a change of identity — the visual system plugs into its slot table (`GROUND / INK / ACCENT / DISPLAY / BODY / MARK / ART / TEXTURE`) rather than being written into the doc. **`design/identity.md` fills those slots — that is what connects the identity to production.**

Tone and vocabulary critique still goes through the `writing-feedback` skill.

## Twitter print template (legacy)

`templates/twitter-print/` renders thread tweets as PNGs with a Twitter-clone look (round avatar, handle, date). **It is not the default path for Instagram carousels** — `build-thread-carousel` uses an editorial pipeline (archetypes plus a generic HTML renderer). The template stays available for the occasional case where the Twitter-clone register is exactly what you want.

To use it manually:

```bash
python -m http.server 8000   # from inside templates/twitter-print/
```

Open `http://localhost:8000` in **Chrome or Edge** (Firefox and Safari do not support the directory picker the API requires). Opening `index.html` directly over `file://` makes the "Export PNG" button fail, and that is deliberate, not a bug to fix.

## Automation scripts

Some skills delegate mechanical work (rendering, parsing, exporting) to Python scripts in `scripts/`. Dependencies live in `pyproject.toml` at the root and are managed with **uv**.

First-time setup per machine:

```bash
uv sync
uv run playwright install chromium   # only if the script needs a browser
```

To run a script: `uv run python scripts/<name>.py [args]`. The skills that depend on these routines call the script via Bash, so there is no command to memorize: just follow the skill that invokes it.

Current scripts:

| Script | Invoked by | What it does |
|---|---|---|
| `scripts/render_html_to_pngs.py` | `build-thread-carousel` (and any future skill needing HTML→PNG) | Generic renderer: takes `--html` and `--selector` and screenshots every element matching the selector via headless Playwright. It knows nothing about content type. Output at `device_scale_factor=3` by default. |

Adding a new script: declare the dependency in `pyproject.toml`, run `uv sync`, and reference it from `scripts/`. If the skill invoking the script is a production routine, document it here too.

## Platform notes

- Windows plus a bash shell. Use `/dev/null` and forward slashes, but absolute paths need the Windows drive letter (`C:/Users/Pedro Miyasaki/...`).
- This is a personal, local-only repo with no remote and no collaborators. Commit messages can be short and plain — a one-line summary of what changed and why is enough, no conventional-commit format, no body sections, no PR-style detail.
- The user instructions in `~/.claude/CLAUDE.md` (Karpathy guidelines) apply here: simplicity first, surgical changes, surface tradeoffs, define verifiable success criteria.
