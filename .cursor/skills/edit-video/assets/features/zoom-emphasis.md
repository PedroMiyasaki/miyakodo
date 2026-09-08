---
id: zoom-emphasis
phase: plate
industry: punch-in / push-in (with reset / punch-out)
---

# Feature · Zoom de ênfase (punch-in / push-in)

## Nome na indústria
Na edição, fechar o enquadramento sem cortar o plano se chama **push-in** (quando
é lento, a câmera "empurra") ou **punch-in** (quando é rápido, "soca" o frame). A
volta para 100% se chama **reset** / **punch-out**. Não é um corte para outro
take: é uma **transformação de scale + crop** no mesmo talking-head.

## O que faz
Nos beats de ênfase, o frame se aproxima do rosto/tese e **obrigatoriamente
volta para 1.0×** antes do próximo beat. Nunca deixe o vídeo "preso" no zoom.

Dois modos (escolha um por beat):

| Modo | Nome na indústria | Quando usar | Comportamento |
|---|---|---|---|
| `slow` | **slow push-in** | Linha de raciocínio longa, tese, CTA | A escala sobe bem sutil ao longo da frase |
| `fast` | **crash / punch-in** | Payoff curto ("…você está errado") | Zoom rápido **logo antes** da palavra/frase-chave, segura um instante, reseta |

## Exemplo em contexto

**Slow**, na abertura:
> "Você precisa de proteções nas suas aplicações de inteligência artificial."
Push-in de ~1.00 → ~1.06 ao longo da frase inteira. No ponto final, ease-out de
volta para 1.00.

**Fast**, o golpe:
> "Você poderia colocar instruções negativas no system prompt, mas se fizer
> isso, **você está errado**."
Punch-in (~180–250ms) caindo no onset de "você está errado" (escala de pico
~1.12–1.15), segura ~200–400ms, reseta em ~200ms.

## Parâmetros (padrões)

| Parâmetro | `slow` | `fast` |
|---|---|---|
| `scale_peak` | 1.06–1.08 | 1.12–1.15 |
| Subida | duração da janela do beat (ease-in-out) | 180–250ms (ease-out) |
| Segurada no pico | opcional, curta | 200–400ms |
| Reset → 1.0 | últimos ~20–30% da janela, ou 200–300ms depois da segurada | 150–250ms depois da segurada |
| Âncora do crop | centro do rosto (ou centro do frame se não houver face track) | igual |

## Como rodar

1. Na transcrição de output, marque os beats de ênfase. Classifique cada um como
   `slow` ou `fast`. Para `fast`, anote a palavra de payoff e o timestamp de
   **início** dessa palavra (`land_at` na timeline de output).
2. Escreva no EDL (uma extensão de plate), sem zooms sobrepostos:

```json
"plate_effects": [
  {
    "type": "zoom_enfase",
    "mode": "fast",
    "start_in_output": 12.40,
    "end_in_output": 14.10,
    "land_at": 12.85,
    "scale_peak": 1.14
  }
]
```

> A string `type` é o literal que o renderer compara. Mantenha exatamente como
> está escrito acima.

3. No render do plate (antes dos overlays), aplique um `scale` + `crop`
   centralizado com keyframes. Em `end_in_output` a escala **tem** que ser 1.0.

## Regras duras
- Todo zoom tem reset. Se `end` chega e a escala ≠ 1.0, o efeito está errado.
- Não empilhe com `pop-it` na mesma janela (os micro-zooms do pop-it são outro
  vocabulário).
- Pode combinar com `black-and-white` no mesmo beat (imitação / crítica).
- Não dê zoom sobre um insert do terço superior de um jeito que "coma" a faixa:
  o zoom é no **plate** (o rosto), e os overlays de terço entram por cima
  depois.

## Status
Implementada. O `render_vertical.py` lê `plate_effects` e aplica no plate
(depois do concat, antes dos overlays) via `zoompan` com curva smoothstep. O
reset para 1.0× é garantido por construção, e janelas de zoom sobrepostas são
rejeitadas com erro. Autoteste: `assets/test_plate_effects.py`.
