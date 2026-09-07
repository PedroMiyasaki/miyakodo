# Assets · edit-video

## Features and modes

- **Features** (one capability each): `features/<id>.md`
- **Modes** (ordered collections of features): `modes/<id>.md`

The orchestrator is `../SKILL.md`: it picks the mode, reads each feature, runs
them.

| Feature | Phase | Script / mechanism |
|---|---|---|
| `cut-dead-air` | `edl` | ranges in `edl.json` (`video-use` helpers) |
| `zoom-emphasis` | `plate` | `plate_effects` → `zoompan` with a smoothstep curve |
| `black-and-white` | `plate` | `plate_effects` → `hue=s=` window with ramps |
| `pop-it` | `plate` | micro punch-ins + `assets/sfx/click.wav` *(spec)* |
| `news-inserts` | `overlays` | `news_insert.py` |
| `motion-third` | `overlays` | HTML/CSS → `motion_terco.py` *(spec)* |
| `subtitles` | `render` | **every mode, final render only** — `render_vertical.py --subtitles` |
| `loudnorm` | `render` | `render_vertical.py` (without `--no-loudnorm`) |

| Mode | Features |
|---|---|
| `baseline` | cut-dead-air → loudnorm |
| `news` | cut-dead-air → news-inserts → loudnorm |
| `authority` | baseline + zoom-emphasis + black-and-white + motion-third *(spec)* + news-inserts *(opt-in)* |

`subtitles` is in no mode's list because it rides on all of them — burned at the
final render, never on a preview.

---

# `news_insert.py` — the news insert CLI (upper third)

Used by the `news-inserts` feature. Turns **one image** into a 1080×1920
overlay: the image in the **upper third**, the rest transparent (face visible
below). Ken Burns (zoom 1.0→1.06) inside the band + alpha fades + minimal
chrome. Output ProRes 4444 alpha → `edl.json` `overlays`.

Each call writes `<out>/frames/*.png` and `<out>/render.mov`.

| Flag | Default | What it does |
|---|---|---|
| `--image` | required | path to the image (screenshot, chart, logo, photo) |
| `--out` | required | the slot's folder (e.g. `<edit>/animations/slot_news_01`) |
| `--duration` | required | seconds = the size of the beat's window |
| `--fit` | `contain` | `contain` = the whole image fits in the band. `cover` = fills the band and crops |
| `--source` | `""` | mono chyron at the top of the band ("FONTE: …"); omit for a clean insert |

The card's colours (ink/paper/seal) are constants in the script itself; the
chyron's font is `fonts/JetBrainsMono.ttf`.

## `fonts/`

| File | Used by | Voice |
|---|---|---|
| `JetBrainsMono.ttf` | `news_insert.py` | the card's source chyron |
| `BricolageGrotesque-ExtraBold.ttf` | captions (`BODY`) | Alvinegro DISPLAY |
| `Newsreader-Italic.ttf` | captions (`EMPH`) | Alvinegro READ |

The two caption faces are copied into `<edit>/fonts/` at render time and reached
via libass's `fontsdir` — they are not installed system-wide, so nothing outside
this skill can resolve them by name.
