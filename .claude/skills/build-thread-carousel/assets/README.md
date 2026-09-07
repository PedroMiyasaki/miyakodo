# assets/ — archetypes for a thread-derived IG carousel (build-thread-carousel skill)

Runnable reference folder for the archetypes of the Instagram carousel **derived from a thread** (`build-thread-carousel` skill). Each archetype is a complete, standalone HTML file — open it in a browser and it renders a demo slide with placeholders.

The skill has two modes, each with its own archetype subfolder — same file structure (`_carousel.css`, `hook-display.html`, `body-paragraph.html`), different content:

- **`default/`** — the default mode. X-cosplay layout in a light, neutral palette. Documented below.
- **`x/`** — X mode. Dark mode, a faithful Twitter/X clone (inherited from the retired `gerar-prints-reel` skill, historically used to generate Reel background images).

Which one to use in each case is in the skill's `SKILL.md`, "Modes" section.

**Identity placeholders:** the archetypes carry `{{NAME}}`, `{{HANDLE}}` and `{{AVATAR_URL}}` in the header (and `{{IMAGE_URL}}` in the sample media slot) — the personal brand identity has not been defined yet, so the skill **asks the user** for the name, handle and avatar path before generating the HTML.

## X-cosplay layout, light palette (default mode)

These archetypes use the **editorial X-cosplay layout** (reference: Adriano Couto / "Gestão com IA"), in a light, neutral palette:

- Compact X header (circular avatar + bold name + blue `#1d9bf0` verified badge + handle) — **it is the layout, not the color, that makes it look like a tweet**
- Neutral bg `oklch(0.96 0 0)` (off-white with no warm cast)
- Text in pure black `oklch(0 0 0)`, neutral grays (chroma 0)
- Inter for the body (via Google Fonts `@import`), JetBrains Mono for `code`, with a fallback to system fonts
- `--seal` brick-red accent on links, the `code` chip and the quote border
- Content vertically centered on the slide — a little text floats in the middle with generous air, a lot of text takes up more

The **only X-native trait retained** is the `#1d9bf0` blue of the verified badge: a recolored check would read as a fake seal. The stylesheet is self-sufficient: all the values live inline in it. Do not generalize these archetypes to other contexts.

## The system (inside each subfolder)

- **`_carousel.css`** — shared chrome: 1080×1350 dimensions, `.slide` as a centered flex column, `.profile-row`, `.tweet-text` with inline markdown rendering, optional `.tweet-media` slot. Changed here = changed in every carousel of that mode.
- **`hook-display.html`** — the first slide. The first paragraph becomes a larger bold headline (40px), the rest regular body (30px). Everything vertically centered.
- **`body-paragraph.html`** — the middle and last slides. Tweet-text at 30px with paragraphs. Supports markdown and `→ ` markers.

## Which to use when

| Position | Default | When to swap |
|---|---|---|
| T1 | `hook-display` | Short hook (up to ~250 chars). Above that it becomes `body-paragraph`. |
| T2 through T(N) | `body-paragraph` | No variants. Use markdown bold/italics/arrows inside the body to give it rhythm. |

There is no separate archetype for the closer — to give weight to the last tweet's test sentence, wrap it in `**bold**` or `> blockquote` inside `body-paragraph`.

## Formatting in the carousel .md

The carousel .md **can be more formatted than the original thread**. There is no character limit on IG, so use the space:

- `**bold**` on one key sentence per slide
- `*italics*` on highlighted terms
- `` `code` `` on technical terms (`RAG`, `eval`, etc.)
- `> quote` to pull out an important sentence
- **`→ ` as an inline list marker** — write `→ ` at the start of each item, with a paragraph break between items. Do not use markdown `*` or `-` (they render as a `<ul>`, which looks visually different). The arrow is literal text.

Example of good arrow use (Adriano slide 6):
```
The rule is simple and holds for any AI on the market:

→ Your knowledge bases live somewhere that belongs to you.

→ Your agents' instructions are documented in a file.

→ The AI is just the engine running on top of that.
```

## Image slot (`.tweet-media`)

Optional slot below the text. When present, it fills space on short slides. 18px rounded corners, fixed height of 360px, `object-fit: cover` handles the crop.

**When a slide gets an image** (detail in `.claude/skills/build-thread-carousel/SKILL.md` § "Proactive image sourcing"). Three rules, in order:

1. **A manual image always wins.** If `posts/thread/<slug>/sketch/images/0N.<ext>` (or unpadded `N.<ext>`) exists for slide N, it gets used, no exceptions — the heuristic does not even run.
2. **T1 always has an image** — manual, or searched, but never absent. It is what stops the scroll.
3. **T2+ with no manual image:** heuristic — `body < 250 chars with no arrows` = search; otherwise, text only.

When the skill goes searching, Claude:
   - Derives a semantic query from the content of **that specific tweet**, not from the thread's general theme (in English, better for stock photo sites)
   - `WebSearch` for `<query> unsplash photo` or `<query> stock free`
   - `WebFetch` on the candidate page to extract the direct image URL
   - `bash curl -L -o posts/thread/<slug>/sketch/images/0N.<ext> <url>` to download it
   - `Read` on the downloaded image (Claude is multimodal) to judge whether it matches the text of **that slide** — not just the thread's theme. An image that illustrates the general subject but clashes with the slide gets discarded.
   - If it works, includes it in the HTML; if not, tries the next candidate or skips (T1 never skips)

Images live in `posts/thread/<slug>/sketch/images/0N.<ext>` — working material, alongside the carousel rewrite (`sketch/carousel-v<N>.md`) and the composition (`sketch/carousel.html`) they feed. On re-render: the skill checks whether the slide's image already exists before searching; if so, it reuses it.

## Header identity (X-cosplay)

No identity is hardcoded: the three fields are placeholders, filled with whatever the user provides.

- Avatar: `{{AVATAR_URL}}` — path to the file, relative to the generated `carousel.html`
- Display name: `{{NAME}}`
- Handle / second line: `{{HANDLE}}`
- Verified badge: inline X-style SVG (blue `#1d9bf0`) — it is layout, not identity, and stays fixed

## System limits

- Everything is optimized for **1080×1350**. Other dimensions require revising the type scale.
- Background color: fixed neutral off-white in the default mode, near-black (`oklch(0.06)`) in X mode. It is not configurable per slide within the same mode.
- Images in `.tweet-media`: 3:1 aspect ratio (1080×360 visually). Taller/shorter images get cropped by `object-fit`. The skill is responsible for picking reasonable images.
- `--seal` (the brick-red accent) shows up on links, the code chip and the quote border. The only X blue left is the verified badge's.
