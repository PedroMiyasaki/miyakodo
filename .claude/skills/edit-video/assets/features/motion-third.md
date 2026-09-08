---
id: motion-third
phase: overlays
industry: upper-third motion graphics / explainer MOTION
---

# Feature · Motion no terço superior (upper-third MOTION)

## Nome na indústria
**Upper-third motion graphics** (às vezes *explainer MOTION* / *diagram
insert*): uma animação programática ocupando a faixa de cima do frame, enquanto
a VO e o rosto seguem nos dois terços de baixo. Mesmo "slot" espacial dos
inserts de notícia, vocabulário diferente (diagrama animado, não screenshot
estático).

## O que faz
Em beats pedagógicos (fluxo, pipeline, guardrail, eval, harness, ramificação),
gera um clipe ProRes 4444 com alpha com uma animação no **terço superior**, e o
resto do canvas fica transparente. Entra no composite como `overlays` no EDL
(igual ao `news-inserts`).

**O terço superior não é ligado por padrão.** Ter a feature no modo só autoriza
o vocabulário, não obriga a preencher a faixa. Ver o julgamento editorial
abaixo.

## Julgamento editorial (obrigatório)

Diferente do modo `news` (onde a regra é mais previsível: insert quando a
notícia é citada, some no CTA), em conteúdo pedagógico/de autoridade **não dá
para decidir de antemão** numa grade fixa de "sempre anima aqui". O editor tem
que ser **crítico beat a beat**.

Pergunte, para cada trecho da VO:

1. **Onde a ênfase precisa cair agora?** No rosto/argumento falado, ou num
   diagrama que a fala sozinha não consegue carregar?
2. **O motion esclarece ou compete?** Se o momento é um soco vocal, uma
   imitação (P&B), uma lista de pop-it ou o CTA, o terço superior **some** (ou
   nem entra).
3. **Existe estrutura visual de verdade?** Um fluxo, uma ramificação, camadas,
   um checklist. Sem isso, não force animação decorativa.

Padrões de bom senso (não regras cegas):

| Momento | Terço superior |
|---|---|
| Explicando um mecanismo / pipeline / condicional | Forte candidato a motion |
| Tese, opinião, provocação, "você está errado" | Prefira plate limpo (`zoom-emphasis` / o rosto) |
| Imitação / voz de outra pessoa | Prefira `black-and-white`, motion desligado |
| Lista falada (nomes, adjetivos) | Prefira `pop-it`, motion desligado |
| CTA / fecho | **Sempre desligado** (frame limpo no rosto) |
| Já teve motion nos últimos ~4s | Desligado por padrão, deixe respirar |

A ausência de motion é uma decisão válida e frequente. Um bom Reel pedagógico
tem trechos longos só de talking-head + legendas. Na dúvida, **não exponha** o
terço.

## Abordagem programática (decisão confirmada)

**Caminho oficial:** HTML + CSS → Playwright frame a frame → ProRes com alpha.
Não uma timeline manual no CapCut.

### Sistema visual

O sistema visual (tokens, tipografia, componentes) foi removido quando a marca
antiga foi aposentada e ainda não tem substituto. Até existir um, pergunte ao
usuário a paleta e a tipografia antes de escrever o HTML do beat, e reaproveite
a mesma decisão em todos os beats da peça: uma paleta por Reel.

**Proibido em motion:** fonte nova a cada beat, gradiente neon, sombra em várias
camadas, "roxo de IA", Lottie de stock.

Por que esta stack:

- o pipeline HTML→PNG (`scripts/render_html_to_pngs.py` / Playwright): motion
  = a mesma ideia com N frames ao longo do tempo
- o agente escreve a animação a partir do beat e re-renderiza

**Válvula de escape:** Manim só se o beat for uma equação/derivação matemática
pesada, e mesmo assim a paleta tem que ser a mesma do resto da peça. Não é o
padrão desta feature.

### Contrato de um beat de motion

1. **Um storyboard de 1 linha** (o que aparece, em que ordem) alinhado às
   palavras da VO.
2. **Arquivo** `<edit>/motion/<beat_id>/index.html`: uma composição 1080×640 (o
   terço superior). Sem chrome de UI de site, só o diagrama.
3. **Duração** = a janela do beat na timeline de output (tipicamente 3–6s).
4. **Render** → sequência de PNG @ 24fps → `render.mov` ProRes 4444, canvas
   1080×1920 inteiro com a faixa de cima como animação e o resto transparente
   (mesmo envelope espacial do `news_insert.py`).
5. **EDL** `overlays[]` com `start_in_output` / `duration`.

Helper alvo (a implementar): `assets/motion_terco.py`, recebe `--html`,
`--duration` e `--out`. Usa Playwright headless frame a frame (ou animações CSS
com o tempo controlado via `currentTime`) e empacota o `.mov`.

### O que animar (vocabulário permitido)

| Tipo | Exemplo de uso |
|---|---|
| Fluxo linear | pipeline retrieve → rank → generate |
| Ramificação / condicional | "se score < threshold → block" |
| Camadas | prompt vs guardrail externo vs eval |
| Checklist sendo marcado | 3 critérios de harness |
| Contador / estado | pass → fail num eval |

Antipadrões: papel de parede abstrato, Lottie genérico sem tese, texto longo no
terço (isso é legenda, e vai embaixo pela feature `subtitles`).

## Exemplo em contexto
Você explica um guardrail em camadas. Enquanto diz "primeiro a policy, depois o
classificador, depois o bloqueio", o terço superior anima três nós acendendo em
sequência, com setas, na paleta da peça. No CTA ("estude o mecanismo, não o
slogan"), o overlay some: frame limpo no rosto (a mesma regra de muro do CTA do
modo news).

## Como rodar

1. Ache os beats pedagógicos na VO (diagrama > frase solta).
2. Para cada beat: storyboard de 1 linha → escreva o `index.html` → renderize
   com o helper → posicione no EDL.
3. **Muro do CTA:** `start + duration ≤ cta_start`. No fecho, o terço fica
   livre.
4. Reporte ao usuário o beat, a duração e um frame de preview antes do render
   final do Reel.

```json
"overlays": [
  {
    "file": "animations/motion_01/render.mov",
    "start_in_output": 22.0,
    "duration": 4.5
  }
]
```

## Regras duras
- Só terço superior. Nunca frame inteiro (isso apagaria o professor).
- As legendas (feature `subtitles`) continuam embaixo: Hard Rule 1.
- **Opt-in por julgamento**, não por checklist. Não anime "porque o modo
  permite".
- Densidade: no máximo **1 motion ativo** por vez, e um teto frouxo de 2–4
  beats por Reel curto, só se cada um passar no julgamento acima. Zero motions
  também está bom.
- Uma paleta para a peça inteira. Sem paleta paralela por beat.
- Se o diagrama não esclarece a frase numa olhada de <2s, refaça o HTML ou
  **corte o beat**. Não "salve" com mais texto.

## Relação com as outras features
- Vs `news-inserts`: mesmo slot espacial. Estático (paper / artigo / lançamento
  / notícia) = `news-inserts`, diagrama animado = `motion-third`. Não use os
  dois no mesmo instante. Em `authority`, os dois são opt-in.
- Com `black-and-white` / `zoom-emphasis`: tranquilo, o plate embaixo muda e o
  motion fica colorido na faixa.
- Com `pop-it`: evite no mesmo segundo (click e diagrama competem pela
  atenção).

## Status
Spec + contrato de arquivo prontos. Implementação pendente:
`assets/motion_terco.py` + uma pasta de exemplos canônicos em
`assets/motion-examples/` (um fluxo, uma ramificação, um checklist).
