# Assets · edit-video

## Features e modos

- **Features** (uma capacidade cada): `features/<id>.md`
- **Modos** (coleções ordenadas de features): `modes/<id>.md`

O orquestrador é o `../SKILL.md`: ele escolhe o modo, lê cada feature e roda
todas.

| Feature | Fase | Script / mecanismo |
|---|---|---|
| `cut-dead-air` | `edl` | ranges no `edl.json` (helpers da `video-use`) |
| `zoom-emphasis` | `plate` | `plate_effects` → `zoompan` com curva smoothstep |
| `black-and-white` | `plate` | `plate_effects` → janela `hue=s=` com rampas |
| `pop-it` | `plate` | micro punch-ins + `assets/sfx/click.wav` *(spec)* |
| `news-inserts` | `overlays` | `news_insert.py` |
| `motion-third` | `overlays` | HTML/CSS → `motion_terco.py` *(spec)* |
| `subtitles` | `render` | **todo modo, só no render final**: `render_vertical.py --subtitles` |
| `loudnorm` | `render` | `render_vertical.py` (sem `--no-loudnorm`) |

| Modo | Features |
|---|---|
| `baseline` | cut-dead-air → loudnorm |
| `news` | cut-dead-air → news-inserts → loudnorm |
| `authority` | baseline + zoom-emphasis + black-and-white + motion-third *(spec)* + news-inserts *(opt-in)* |

`subtitles` não está na lista de nenhum modo porque vai junto em todos:
queimada no render final, nunca num preview.

---

# `news_insert.py` — a CLI do insert de notícia (terço superior)

Usada pela feature `news-inserts`. Transforma **uma imagem** num overlay
1080×1920: a imagem no **terço superior**, o resto transparente (rosto visível
embaixo). Ken Burns (zoom 1.0→1.06) dentro da faixa + fades de alpha + chrome
mínimo. Saída em ProRes 4444 com alpha → `overlays` do `edl.json`.

Cada chamada escreve `<out>/frames/*.png` e `<out>/render.mov`.

| Flag | Padrão | O que faz |
|---|---|---|
| `--image` | obrigatória | caminho da imagem (print, gráfico, logo, foto) |
| `--out` | obrigatória | a pasta do slot (ex.: `<edit>/animations/slot_news_01`) |
| `--duration` | obrigatória | segundos = o tamanho da janela do beat |
| `--fit` | `contain` | `contain` = a imagem inteira cabe na faixa. `cover` = preenche a faixa e corta |
| `--source` | `""` | chyron mono no topo da faixa ("FONTE: …"). Omita para um insert limpo |

As cores do card (ink/paper/seal) são constantes no próprio script. A fonte do
chyron é `fonts/JetBrainsMono.ttf`.

## `fonts/`

| Arquivo | Usada por | Voz |
|---|---|---|
| `JetBrainsMono.ttf` | `news_insert.py` | o chyron de fonte do card |
| `BricolageGrotesque-ExtraBold.ttf` | legendas do vídeo (`BODY`) | DISPLAY do Alvinegro |

A fonte das legendas é copiada para `<edit>/fonts/` na hora do render e
alcançada pelo `fontsdir` do libass: ela não está instalada no sistema, então
nada fora desta skill consegue resolver ela pelo nome.
