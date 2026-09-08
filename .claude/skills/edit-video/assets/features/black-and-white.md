---
id: black-and-white
phase: plate
industry: B&W grade window / desaturate pass
---

# Feature · Preto e branco (janela de grade P&B)

## Nome na indústria
Uma janela temporal de **dessaturação** (saturação → 0) no plano. Na ilha de
edição costuma aparecer como **B&W grade**, **flashback grade** ou, quando marca
a fala de outra pessoa / ironia, **diegetic imitation grade**: a colorização muda
para sinalizar "agora estou citando / imitando outra voz", não um flashback
literal.

## O que faz
Por um trecho curto, o talking-head (o **plate**) fica em preto e branco. Fora
da janela, cor normal. Serve para:

- imitar o interlocutor cético
- marcar crítica / "a voz do mercado"
- destacar um argumento que você está rebatendo

## Exemplo em contexto
Você explica que um guardrail é um mecanismo **externo**. Aí você imita a
objeção:

> "Tá, mas não dá para só colocar a regra no prompt?"

Nesse trecho: **P&B** (e, para dar mais peso, `zoom-emphasis` `fast` sobre o
mesmo intervalo: o combo clássico de "entrar na cabeça da objeção").

Quando você volta para a sua própria voz / resposta, a cor volta (fim da
janela).

Instrução explícita durante a gravação (uma nota de editor) também conta, e
prevalece:

> …"Ah, eu posso só colocar uma regra no prompt" **"nessa parte da imitação,
> vai para preto e branco"** E na verdade você poderia…

Aplique o P&B na imitação e **corte** a instrução falada em si do vídeo e das
legendas (ver a seção de notas de editor da `SKILL.md`).

## Parâmetros (padrões)

| Parâmetro | Padrão | Notas |
|---|---|---|
| `start_in_output` / `end_in_output` | a janela da imitação | tipicamente 1.5–4s |
| Fade in/out da dessaturação | 80–120ms | evita um "corte seco" de cor |
| Escopo | **só o plate** | overlays de terço (motion / news) e legendas **não** herdam o P&B: ficam coloridos por cima, a não ser que o beat peça o contrário |

## Como rodar

1. Marque na timeline de output o intervalo em que a voz é "a outra pessoa"
   (imitação) ou a crítica encenada.
2. EDL:

```json
"plate_effects": [
  {
    "type": "preto_e_branco",
    "start_in_output": 18.20,
    "end_in_output": 21.00
  }
]
```

> A string `type` é o literal que o renderer compara. Mantenha exatamente como
> está escrito acima.

3. No render do plate: `hue=s=0` (ou equivalente) ligado entre start/end, com
   fades curtos nas bordas.

## Combos
- **Com `zoom-emphasis`:** permitido e desejável em imitações ("punch-in +
  P&B").
- **Com `pop-it`:** evite na mesma janela: o pop-it é lista afirmativa, o P&B é
  voz de outra pessoa / crítica.
- **Com `motion-third`:** tranquilo: o diagrama no terço superior fica em cor, o
  rosto embaixo vai para P&B.

## Regras duras
- Janela curta. P&B que dura demais vira estética, não sinal.
- De volta à cor **antes** do CTA final (o fecho da peça fica em cor, a não ser
  que o usuário peça explicitamente o contrário).

## Status
Implementada. O `render_vertical.py` lê `plate_effects` e aplica `hue=s=` com
rampas nas bordas (`fade`, padrão 100ms) no plate, antes dos overlays, então os
cards de terço e as legendas ficam coloridos por cima.
Autoteste: `assets/test_plate_effects.py`.
