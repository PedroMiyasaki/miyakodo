---
slug: gravacao
layouts:
  - split
  - motion
  - creator
default_layout: split
validate_tone: false
caption_profile: gravada
caption_max_words: 5
caption_max_chars: 32
caption_max_duration: 1.75
caption_merge_orphans: true
caption_anchor: layout
caption_tops:
  split: 900
  motion: 188
  creator: 220
media: bruto
whoosh_on_change: true
avatar: false
grain: false
scene_wrapper: plain
boxes: recorded
---

# gravacao

## Quando usar

Existe talking head. A animação entra por cima da pessoa, ou no lugar dela por um instante.

## Entradas

Roteiro JSON com `mode: gravacao`, `voice` e `footage`. `footage.src` é um mp4 no mesmo relógio da voz. `footage.still` fabrica o plano a partir de uma foto quando não há bruto. A janela `in` / `out` fatia os dois.

## Layouts

- `split`: pessoa embaixo, cena em cima. É o padrão.
- `motion`: a pessoa some e a cena ocupa o quadro.
- `creator`: pessoa em tela cheia. Punch-in quando `punch` não é false.

A troca é corte seco.

## Legenda

Placa off-white (`grav`). A posição depende do layout: `split` em 900, `motion` em 188, `creator` em 220. Até 5 palavras, 32 caracteres ou 1,75 s. Palavra órfã volta para o grupo vizinho. `emphasis` vai para o verde, `strong` para uma pílula dark brown, `cta` para uma pílula laranja. A palavra falada só sobe a opacidade.

## Ritmo de corte

Silêncio interno acima de cerca de 0,28 s sai da voz e do vídeo, com um respiro curto nas bordas (0,05 s) para não comer consoante. O primeiro beat não leva whoosh. Os seguintes levam.

## Motion

Sem avatar desenhado e sem grão. O talking head é o plano, com jump cut. No `creator`, o punch-in escala até 1,14 quando `punch` está ligado. A cena entra no corte, sem o fade do sem-gravacao. O pop de cada `scene.type` continua.

## O que reaproveita

Os mesmos `scene.type`, a mesma paleta, as mesmas fontes, o logo e a cama sonora do pipeline. O rosto é o do Pedro, no bruto ou no still `assets/pedro-frame.jpg`. Não entra a arte gráfica, a música nem o texto de outro criador.
