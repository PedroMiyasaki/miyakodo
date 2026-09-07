---
name: build-thread-carousel
description: >
  Builds an Instagram carousel from an already-written thread (in
  posts/thread/<slug>/sketch/v<N>.md), generating a carousel.html in
  posts/thread/<slug>/sketch/ with an editorial X-cosplay aesthetic
  (header with avatar + name + blue verified badge, vertically
  centered content, optional image slot). It has two visual modes:
  default (light, neutral palette) and X (dark mode, a faithful X
  clone — also used as Reel background images). Name, handle and
  avatar are placeholders: ask the user before generating.
  Renders each slide as a PNG via Playwright. Activate with
  commands like "build the carousel for thread <slug>", "render
  the PNGs for <slug>", "build the X-mode carousel for <slug>",
  "generate the reel stills for thread <slug>", "make the stills
  for <slug>" or "use the build-thread-carousel skill on the
  <slug> post".
---

# SKILL · Build thread carousel
## Build Thread Carousel

Purpose: build the IG carousel from an already-written thread. Each slide reproduces the X header (avatar + name + blue verified badge + handle on the second line), with the content **vertically centered**. Optional image slot below the text, to fill out short slides.

> **The header identity is a placeholder.** The archetypes carry `{{NAME}}`, `{{HANDLE}}` and `{{AVATAR_URL}}` — the personal brand has not been defined yet. **Ask the user for the name, handle and avatar file path before generating the HTML**, and substitute all three while composing. Do not invent any of them.

The skill has **two visual modes** — same content, same structure, different art. See the "Modes" section below to choose which to use and how to activate each one.

Visual reference for the default mode: Adriano Couto / "Gestão com IA". The **layout** is editorial X-cosplay — it emulates the look of a tweet, since the content originates from X threads.

---

## Modes

| | **default** | **X** |
|---|---|---|
| When to use it | IG feed carousel | Background images for a Reel (a sequence of stills), or when the request is explicitly for an X/Twitter clone |
| Palette | Light and neutral: off-white bg, pure black text, `--seal` brick-red accent | X's native dark mode: near-black bg (`oklch(0.06)`), near-white text |
| Avatar | `{{AVATAR_URL}}` — provided by the user | `{{AVATAR_URL}}` — provided by the user |
| Archetypes | `assets/default/` | `assets/x/` |
| Slide dimensions | 1080×1350 (4:5) — the same in both modes | |
| Output | `posts/thread/<slug>/sketch/carousel.html` + `sketch/carousel-v<N>.md` + PNGs loose at `posts/thread/<slug>/` — **same convention in both modes**, do not split by mode | |

Activating X mode: commands mentioning "X mode", "X style", "dark mode", or the legacy commands of the retired `gerar-prints-reel` skill ("generate the reel stills for thread `<slug>`", "make the stills for `<slug>`", "use the gerar-prints-reel skill on the `<slug>` post"). Any other command activates the default mode.

The rest of this protocol is **identical in both modes**, except where explicitly marked — the only real difference is which `assets/` subfolder to import.

---

## Prerequisites (once per machine)

```bash
uv sync
uv run playwright install chromium
```

---

## Required reading before generating

The archetypes live in `assets/`, packaged with this skill (path relative to this SKILL.md), organized by mode:

1. `assets/README.md` — documents the X-cosplay exception, the two modes and when to use each archetype
2. `assets/<mode>/_carousel.css` — shared chrome of the chosen mode (X header, vertical centering, media slot, markdown rendering)
3. `assets/<mode>/hook-display.html` — archetype for the first slide, in the chosen mode
4. `assets/<mode>/body-paragraph.html` — archetype for the remaining slides, in the chosen mode

Where `<mode>` is `default` or `x`, per the "Modes" section above.

Each `_carousel.css` is self-sufficient: color and typography are already embedded in it, there is no external stylesheet to load.

---

## When to activate

Commands like:

- "Use the `build-thread-carousel` skill on the `<slug>` post"
- "Build the carousel for thread `<slug>`"
- "Render the PNGs for `<slug>`"
- "Build the X-mode carousel for `<slug>`" / "generate the reel stills for thread `<slug>`" / "make the stills for `<slug>`" (X mode)

Do not activate if the thread does not yet exist in `posts/thread/<slug>/sketch/v<N>.md`. Point the user to `write-thread`.

---

## Protocol

### 1. Identify the slug

Subfolder in `posts/thread/`. If ambiguous, check with Glob `posts/thread/<input>*`.

### 2. Adapt the text for a carousel

The carousel **can be more formatted and longer than the original thread** — IG has no character limit, and the slides look better with more spacing and structure.

- Read `posts/thread/<slug>/sketch/v<N>.md` (the most recent version of the thread).
- Save the rewrite to `posts/thread/<slug>/sketch/carousel-v1.md`. Do **not** create a `v<N+1>.md`: the `v<N>` sequence is the thread (what goes to X), and its highest-numbered version must remain the latest version *of the thread*, not a carousel adaptation. `sketch/` therefore holds two parallel sequences — `v<N>.md` for the thread, `carousel-v<N>.md` for the carousel — each iterated on its own, next to the `carousel.html` that will be generated from the second.
- In the rewrite, keep the **core of the argument**. You may:
  - Add connectors ("Think about it:", "Two paths:", "In practice:") that give it rhythm
  - Reformat as an arrow list `→ ` when the content has parallel items
  - Add transition paragraphs that existed only implicitly in the thread
  - Use rich markdown:
    - `**bold**` on one key sentence per slide
    - `*italics*` on a highlighted term
    - `` `code` `` on technical terms (`RAG`, `eval`, etc.)
    - `> quote` to highlight an important sentence
    - `→ ` as an inline list marker (literal text, paragraph break between items — do NOT use markdown `*` or `-`)
- Copy the thread's YAML header/metadata to the top of `carousel-v1.md`. Record what changed from thread `v<N>.md` to this adaptation.
- Tradeoff: the expanded version diverges from the one going to X. That is expected — the carousel .md is a deliverable of its own.

### 3. Map each tweet to an archetype

- T1 → `slide-hook` (the first paragraph becomes a **bold 40px headline**, the rest in regular 30px body).
- T2 through T(N) → `slide-body` (regular 30px text with markdown).

Do not create a new archetype without approval.

### 4. Proactive image sourcing

Whether a slide gets an image follows three rules, in priority order:

**Rule 1 — a manual image always wins (any slide).**
For every slide N, check whether a matching image file already exists in `posts/thread/<slug>/sketch/images/`. Accept both the zero-padded and unpadded form (`01.jpg` or `1.jpg`), in `.png`, `.jpg`, `.jpeg` or `.webp`. If it exists, **use that image, no exceptions** — do not run the heuristic, do not search, do not evaluate. The user put it there deliberately.

**Rule 2 — slide 1 always has an image.**
The first slide (T1, the hook) always gets an image, regardless of the heuristic — it is what makes the carousel stop the scroll. If there is no manual image for it (rule 1), search proactively. Never deliver T1 without an image.

**Rule 3 — remaining slides: size heuristic.**
For slides from T2 onward with no manual image, identify the short ones that would benefit from an image. Heuristic: **body < 250 chars with no arrow lists** = candidate; in that case, search proactively. A long slide stays text-only.

**Proactive search procedure** (applied when rule 2 or 3 calls for a search):

- Derive a semantic query from the content of **that specific slide**, not from the thread's general theme (in English, more effective for stock photo sites). E.g.: for "AI is producing inefficient professionals", the query would be `frustrated professional computer screen stock photo`.
- Run `WebSearch` for `<query> unsplash` or `<query> pexels free`.
- Select 2–3 candidate URLs (prioritize unsplash.com, pexels.com, pixabay.com).
- Run `WebFetch` on the candidate page to extract the direct URL of the image file. If the URL comes back as `plus.unsplash.com/premium_photo-...`, it is paid Unsplash+: discard it and try the next candidate.
- Create the folder: `mkdir -p posts/thread/<slug>/sketch/images` (if it does not exist).
- Download via Bash: `curl -L -o "posts/thread/<slug>/sketch/images/0N.jpg" "<direct-url>"` (an image downloaded by the skill is always saved zero-padded, `0N.jpg`).
- **Inspect the image with `Read`** (Claude is multimodal). Judge it rigorously:
  - **Does the image match the text of THAT specific slide, not just the thread's general theme?** This is the most common mistake: using an image that illustrates the thread's subject but clashes with the slide it gets inserted into. A real example: putting a photo of a trash can full of crumpled paper on a hook slide that is about *overconfidence* — it fits the thread ("AI produces bad work"), but not the hook's point. An image like that should be discarded, however good a photo it is.
  - Is the quality adequate? Is it free of overlaid text that would clash?
- If it works, keep it. Otherwise: for slides T2+, delete it and try the next candidate, or skip the slide (no image beats an off-topic image). **For T1, do not skip** — broaden or reformulate the query and search more; if nothing still works, tell the user and ask for a manual image.

**Report to the user** which slides got an image and where from (manual or searched), before generating the HTML.

Cropping is not necessary — the CSS `.tweet-media` uses `object-fit: cover` with a fixed height of 360px, and the browser crops automatically in the Playwright render.

### 5. Present the plan to the user

Before generating the HTML, list for the user:
- The slide mapping (T1 → hook, T2-T(N) → body)
- Which slides got an image and the source (link to the original image)
- Markdown emphases added (sentences that became bold/italic)

Ask for confirmation or adjustments.

### 6. Generate `posts/thread/<slug>/sketch/carousel.html`

After approval:

- Import **only** the `_carousel.css` of the chosen mode via `<link>` (self-sufficient stylesheet). Path relative to `posts/thread/<slug>/sketch/`:
  - `../../../../.claude/skills/build-thread-carousel/assets/<mode>/_carousel.css`
- Include a `<style>` in the `<head>` copying, from the chosen mode's archetypes, the blocks for the `.slide-hook` and `.slide-body` classes.
- Each tweet becomes `<section class="slide slide-<archetype>" data-slide="NN">`, with:
  - a complete `<header class="profile-row">` (avatar + name + verified SVG + handle), with `{{NAME}}`, `{{HANDLE}}` and `{{AVATAR_URL}}` already substituted by what the user provided. If they have not provided it yet, **ask before generating**
  - `<div class="tweet-text">` with markdown already converted to inline HTML (`**` → `<strong>`, `*` → `<em>`, `` ` `` → `<code>`, `>` → `<blockquote>`)
  - `<div class="tweet-media"><img src="images/<file>" alt="..."></div>` **only if** the slide has an associated image. The images sit in `sketch/images/`, a sibling of the HTML, so the reference is just the folder and the filename — no `../` at all. `<file>` is the real filename: `0N.jpg` when the skill downloaded it, or `0N`/`N` in any extension (`.png`/`.jpg`/`.jpeg`/`.webp`) if it was a manual image
- `<body class="carrossel-preview">` to give a neutral (or dark, in X mode) background when opened in the browser.

### 7. Present the HTML for the user to review

The user can open the file directly in the browser (`file://` in Chrome/Edge). When they ask for an adjustment:
- Copy change → create `posts/thread/<slug>/sketch/carousel-v<N+1>.md` (copy the unchanged blocks from `carousel-v<N>.md` literally, apply only the diff) and regenerate the HTML.
- Image change on a slide → replace the file in `posts/thread/<slug>/sketch/images/` or run image sourcing again.
- Systemic visual change → adjust the archetype in `assets/<mode>/`.

### 8. Render the PNGs

```bash
uv run python scripts/render_html_to_pngs.py \
  --html "posts/thread/<slug>/sketch/carousel.html" \
  --out "posts/thread/<slug>" \
  --selector ".slide" \
  --width 1080 --height 1350
```

PNGs generated loose in `posts/thread/<slug>/`, 3240×4050 (3× device scale). The script numbers them sequentially, zero-padded to the width of the slide count: a carousel of 10 or more slides comes out `01.png … 10.png`, one of 9 or fewer comes out `1.png … 9.png`.

### 9. Report

State how many PNGs were generated, the output folder, and which slides got an image and where from. If any slide still shows a lot of empty space, suggest the user consider adding a manual image.

---

## Identity on the slides (placeholders)

No identity is hardcoded in the archetypes. The fields below are filled with whatever the user provides, on every piece:

- Avatar: `{{AVATAR_URL}}` — path to the image file, relative to the generated `carousel.html`
- Display name: `{{NAME}}`
- Handle / second line of the header: `{{HANDLE}}`
- Verified badge: inline X-style SVG (blue `#1d9bf0`) — it is layout, not identity, and stays fixed

When the user settles on a name, handle and avatar for good, write the values into the 2 archetypes of the affected mode AND into the already-generated `carousel.html`.

---

## Image sourcing — preferred sites

In order of preference:

1. **Unsplash** (`unsplash.com`) — high-quality editorial photos. **Careful:** the search mixes free and paid results. Only the direct `images.unsplash.com/photo-<id>?...` URLs work (free); the `plus.unsplash.com/premium_photo-<id>?...` ones are **paid Unsplash+** and must be discarded immediately — in the demo, 2 of the first 4 candidates were premium.
2. **Pexels** (`pexels.com`) — an equivalent alternative. 100% free, no paid tier: the recommended default to avoid Unsplash's premium triage.
3. **Pixabay** (`pixabay.com`) — backup
4. **Wikipedia / Wikimedia Commons** — for images of events, places, well-known people. Mind the license.

Avoid:
- Google Images directly (uncertain copyright)
- Sites with watermarks (Getty, Shutterstock thumbnails)
- Images with overlaid text (English labels, other brands' logos)

## Known limitations

- Fixed size: 1080×1350. Changing the dimensions requires revising the archetypes.
- Image slot with a 3:1 aspect ratio (1080×360 visually). Very square or very tall images lose information in the crop. Review before approving.
- Overflow is not checked automatically. Slides with very long text + an image can clip at the bottom. Review the HTML before rendering.
- The text uses Inter (and JetBrains Mono in `code`), loaded via a Google Fonts `@import` in `_carousel.css`. The renderer waits for `document.fonts.ready` before the screenshot, so the webfont makes it into the PNG. With no network, it falls back to system fonts (`-apple-system`, etc.) — visually near-identical.
- Image search depends on `WebSearch` returning Unsplash/Pexels links. If it does not, use a more generic query or Wikimedia.
