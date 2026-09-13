# SFX · edit-video

| Arquivo | Feature | Spec |
|---|---|---|
| `click.wav` | `pop-it` | mono 44.1kHz, ~278ms, click gravado de dois toques (press + release, 140ms entre eles), escolhido de ouvido pelo usuário. Pico -7.5dBFS, ataque em 2ms. Já versionado. |

Para trocar o click: substitua o `click.wav` mantendo o nome. Antes, corte o
silêncio do começo (o som toca no início exato do card, então silêncio inicial
vira atraso) e normalize o pico para -7.5dBFS, que é o nível em que o ganho e o
limitador do `render_vertical.py` foram calibrados. Sem o arquivo, o `pop-it`
não inventa SFX na hora do render.
