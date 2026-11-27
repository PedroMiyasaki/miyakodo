---
slug: jason-cooperson
layouts:
  - painel
  - full
  - hero
default_layout: painel
validate_tone: true
caption_profile: duas-vozes
caption_max_words: 3
caption_max_chars: 28
caption_max_duration: 1.1
caption_merge_orphans: false
caption_anchor: layout
caption_tops:
  painel: 760
  full: 1188
  hero: 1200
media: voz
whoosh_on_change: false
avatar: true
grain: true
scene_wrapper: wash
boxes: studio
---

# jason-cooperson

Gramática de um Reel de referência (painel com o falante, motion sem ele, legenda de duas vozes, troca a cada poucos segundos). A identidade é a de `design/identity.md`. Sem talking head: o falante é o avatar do Pedro. Sem a trilha, as cores, as fontes e o CTA do vídeo estudado.

O teto de glitch é quatro flashes a cada 69 s (`int(duração * 4 / 69)`). Abaixo de 17,25 s o teto é zero. O exemplo curto não gasta esse orçamento.

## Quando usar

A peça é voz e desenho, no ritmo de ferramenta: card em cima, pessoa embaixo, e de vez em quando o card sozinho ou o busto grande para opinião e CTA. Não usar quando já existe talking head novo. Esse caso continua em `gravacao`.

## Entradas

Roteiro JSON com `mode: jason-cooperson` e `voice`. Sem `footage`.

`logos`: lista opcional de palavras que saem como o logo horizontal, no lugar do texto. Só marca que a frase realmente diz.

`chapter: true` num beat pede um flash curto (off-white e uma linha laranja). O compilador recusa se passar do teto.

## Layouts

Três, e só o primeiro é novo.

- `painel` (padrão). Card na área de cima. Embaixo, um poço arredondado off-white. O avatar entra com a cabeça vazando acima da borda. É o layout âncora do estudo (falante no painel, legenda no vão). `guide`, `pip` e `hero` não fazem esse recorte: um é lado a lado, outro é miniatura, o outro é busto solto.
- `full`: o card ocupa o quadro e o avatar sai. Cobre o motion sem falante (janela, lista, terminal).
- `hero`: frase curta em cima e busto grande. Cobre opinião e CTA, no lugar da câmera cheia. A legenda senta na altura do peito.

A troca é corte. O fade de 0,16 s do wash entra no lugar do blur de chegada. Sem whoosh entre beats.

## Legenda

Perfil `duas-vozes`, uma linha, no máximo 3 palavras, 28 caracteres ou 1,1 s. A placa é off-white com borda dark brown.

- Corpo em Poppins bold.
- `emphasis` e `strong` em Instrument Serif itálico. É a segunda voz. Não é a script do vídeo de referência.
- `cta` em laranja `#db3c05`, com um glow curto. Não é ciano.
- Palavra listada em `logos` vira `assets/logo.png` dentro da linha.
- A palavra seguinte da mesma linha entra borrada e some o blur quando chega a vez dela.

Posição: `painel` em 760, `full` em 1188, `hero` em 1200, na camisa, abaixo do rosto.

## Ritmo de corte

Um plano a cada poucos segundos, e o miolo do card troca com a cláusula. Média do estudo: um corte a cada 3,85 s, com troca interna mais curta. Não copiar os 18 planos nem os tempos.

Flash de capítulo só com `chapter: true`, e nunca acima de quatro em 69 s. O resto é corte seco. Não há scanline ciano, não há glitch repetido.

## Motion

Avatar do Pedro no `painel` e no `hero`, com a boca na faixa. No `painel` a cabeça passa da borda do poço. Grão de papel. Pop elástico do `scene.type`. Sem footage.

## O que reaproveita

Paleta, Instrument Serif, Poppins, logo horizontal, avatar, grão, cama `assets/bed.wav`, sfx já mapeados, wash e os tons (`paper`, `ink`, `verde`, `azul`, `rosa`, `oliva`).

`scene.type` que já cobrem o estudo: `statement`, `badge`, `counter`, `code`, `mockup`, `bullets`, `phone`. Terminal vira `code`. Janela vira `mockup`. Número de prova vira `counter`, com número nosso, nunca o do vídeo estudado.

Dois tipos novos, porque nenhum existente fazia a peça:

- `vidro`: card translúcido com rótulo em serif itálico caixa-alta. O estudo repete esse rótulo em cima de cada card. `quote` é citação, `statement` é letreiro, nenhum é esse rótulo.
- `alca`: card com oito alças de seleção e um aro oliva. A gramática é a da ferramenta de design. As alças são quadrados nossos, não um asset de terceiro.

Não entram a trilha, os prints, os Reels de exemplo, o rosto, a paleta exata nem o CTA "comment style".
