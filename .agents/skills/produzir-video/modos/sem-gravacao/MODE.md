---
slug: sem-gravacao
layouts:
  - guide
  - center
  - corner
  - hero
  - pip
  - full
default_layout: guide
validate_tone: true
caption_profile: faixa
caption_max_words: 4
caption_max_chars: 26
caption_max_duration: 1.2
caption_merge_orphans: false
caption_anchor: faixa
caption_top: 224
media: voz
whoosh_on_change: false
avatar: true
grain: true
scene_wrapper: wash
boxes: faceless
---

# sem-gravacao

## Quando usar

Não há gravação nova. A voz e o desenho carregam a peça.

## Entradas

Roteiro JSON com `mode: sem-gravacao`, `voice.src` e a janela `voice.in` / `voice.out`. `words` é opcional. Sem `footage`.

## Layouts

Todos na área segura do Reels: abaixo da faixa de legenda, acima do rodapé da legenda do post, longe da coluna de botões.

- `hero` e `center`: frase curta em cima, busto grande embaixo.
- `guide`: Pedro à esquerda, cena à direita. É o padrão quando o beat não declara layout.
- `pip` e `corner`: a cena ocupa o miolo e o busto fica pequeno, acima do rodapé.
- `full`: a cena toma a área segura e o avatar sai.

A troca entre layouts é corte.

## Legenda

Placa off-white (`face`), entre o topo da interface e o começo da cena, em `top: 224`. Não cobre avatar nem texto de cena. No máximo 4 palavras, 26 caracteres ou 1,2 s. `emphasis`, `strong` e `cta` saem em itálico, Instrument Serif. A palavra falada ganha o realce escuro com sombra.

## Ritmo de corte

Corte seco de um beat para o outro. A voz não perde silêncio. A cena entra com um fade de 0,16 s. Sem whoosh entre beats.

## Motion

O avatar do Pedro muda de enquadramento com o layout (0,38 s, fora o primeiro beat). Piscar, sobrancelha na ênfase e visema pela faixa de voz. Grão de papel por cima do quadro. Cada cena entra com o pop elástico do `scene.type`.

## O que reaproveita

O pipeline comum: `scene.type` de `pipeline/scenes.py`, paleta e fontes de `design/identity.md`, logo horizontal, avatar em `pipeline/avatar.py`, cama `assets/bed.wav` e os sfx já mapeados. Este modo não traz arte, música nem texto de outro criador.
