---
id: pop-it
phase: plate
industry: staccato punch-ins + hit SFX (word pops)
---

# Feature · Pop-it (punch staccato + hit SFX)

## Nome na indústria
Uma sequência de **micro punch-ins** sincronizados com palavras-alvo da VO, cada
um acompanhado de um **hit SFX** (click / tick). Em motion/edição: *word pops*,
*staccato zooms*, *impact hits on VO*. Não é tipografia cinética na tela: é o
**plano** "piscando" em escala + um click no áudio, no onset de cada palavra da
lista.

## O que faz
Em listas faladas (nomes, adjetivos, pilares), para **cada** item da lista:

1. no onset da palavra → **click** no áudio
2. no mesmo instante → **mini-zoom** (~1.00 → ~1.04 → 1.00 em ~120–180ms)
3. o próximo item só dispara depois que o anterior resetou

Depois do último item, escala = 1.0 e silêncio de SFX.

## Exemplos em contexto

**Nomes próprios:**
> "empresas como **Google**, **Amazon** e **Microsoft**"
Três hits: Google / Amazon / Microsoft.

**Adjetivos de valor:**
> "com guardrails as suas aplicações ficam mais **seguras**, **confiáveis** e
> **auditáveis**"
Três hits: seguras / confiáveis / auditáveis.

Não marque conectores ("como", "e", "mais"): só os termos da lista.

## Parâmetros (padrões)

| Parâmetro | Padrão |
|---|---|
| `scale_peak` por hit | 1.04 (máx. 1.06) |
| Duração do micro-zoom | 120–180ms (subida + reset) |
| SFX | `assets/sfx/click.wav` (mono, dois toques, ~278ms) |
| Ganho do SFX | ~-18 a -12 dBFS abaixo da VO. Isso vale para um hit isolado num beat sem fala simultânea. Quando o click cai exatamente onde a VO está falando (o caso do pop de imagem em `news-inserts`: o click marca o início do overlay, que também é onde a fala do beat começa), essa faixa é baixa demais e o click some debaixo da voz. O `render_vertical.py --pop-it` usa `+6dB` sobre o `click.wav` (pico efetivo ~-1.5dBFS) para esse caso. Medido, não só ouvido: `-14dB` de atenuação deixou o pico do click em ~-25dBFS contra um RMS de voz de ~-15dB, inaudível. Confirme de ouvido antes de assumir "presente": pico medido não quer dizer perceptível debaixo da fala. |
| Máximo de hits por beat | 2–5 (mais que isso vira metrônomo, divida em dois beats) |

## Como rodar

1. Na timeline de output, liste os onsets por palavra das palavras-alvo
   (`takes_packed.md` / ASR).
2. EDL:

```json
"plate_effects": [
  {
    "type": "pop_it",
    "hits": [
      {"t": 8.12, "word": "Google"},
      {"t": 8.55, "word": "Amazon"},
      {"t": 9.10, "word": "Microsoft"}
    ],
    "sfx": "assets/sfx/click.wav",
    "scale_peak": 1.04
  }
]
```

3. Render do plate: para cada hit, um keyframe de escala centralizado em `t`.
4. Mix de áudio: `amix` / `adelay` do click em cada `t` (caminho relativo à
   raiz do repo ou à skill). O loudnorm (a feature `loudnorm`) roda **depois** e
   engole o mix final.

## Regras duras
- Reset entre hits. Sem micro-zooms sobrepostos.
- Não combine com `zoom-emphasis` na mesma janela (conflito de escala).
- Não use em imitação de cético: isso é território do `black-and-white`.
- Se o ASR errar o onset, ajuste o `t` na mão antes do render final (1 frame de
  erro já "descola" o click da boca).

## Dependência de asset
Click canônico: `.claude/skills/edit-video/assets/sfx/click.wav` (mono, ~278ms,
um click gravado de dois toques, versionado no repo; spec em `sfx/README.md`). Se o
arquivo sumir, não invente um SFX na hora do render: restaure o asset ou pule os
hits de áudio e avise. Para trocar o som, substitua o arquivo mantendo o nome.

## Status
**Implementado (parcialmente): o click de áudio.** O `render_vertical.py
--pop-it` mixa o `click.wav` (adelay + amix, `normalize=0`, antes do loudnorm)
no `start_in_output` de cada entrada em `overlays`. É isso que o `news-inserts`
usa para tocar um click a cada card que aparece. Esse caso não precisa de
`plate_effects` nem de hits manuais: um overlay = um click, automaticamente.

**Spec, não implementado: o micro punch-in em lista falada** (os
`hits`/`plate_effects` no EDL acima, para nomes próprios ou adjetivos em
sequência, com zoom na imagem do próprio talking-head). Isso continua sendo
transformação pura de plate, sem código. Fica para uma implementação futura, se
algum modo pedir.
