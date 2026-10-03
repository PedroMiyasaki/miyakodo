---
name: registrar-aprendizado
description: >
  Registra o que deu errado numa sessão de gravação em content-routines/aprendizados.md,
  agrupado sob a data do último sábado (inclusive: se rodar num sábado, é aquele sábado
  mesmo). O primeiro passo do sábado lê esse arquivo de volta, então o lote seguinte não
  repete o erro.
  Ative com "/registrar-aprendizado", "registrar aprendizado", "anota esse aprendizado",
  ou sempre que o usuário contar algo que deu errado numa sessão de gravação ou de edição.
---
## Registrar um aprendizado de sessão de gravação

Objetivo: pegar o que o usuário observou de errado na sessão e guardar em
`content-routines/aprendizados.md` sob o sábado daquela sessão, para que o primeiro passo do
[saturday.md](../../../content-routines/default/saturday.md) mostre isso antes do lote seguinte.

Atrito zero: o usuário despeja a observação, esta skill data, transforma em regra e guarda.
Não faça perguntas antes de salvar.

---

## Passo 1 · Pegar as observações

Elas costumam vir junto com a invocação ("/registrar-aprendizado o teleprompter estava longe demais").
Se a invocação vier sem nada, pergunte uma vez: *"O que deu errado nessa sessão?"* - e siga.

## Passo 2 · Calcular o sábado da sessão

Inclusive: rodando num sábado, guarda naquele mesmo sábado.

```bash
date -d "-$(( ($(date +%u) + 1) % 7 )) days" +%F
```

## Passo 3 · Escrever a entrada

Um bullet por erro distinto, em português. Cada bullet é
**o que aconteceu → a regra que evita**, uma linha, no imperativo. Sem preâmbulo, sem consolo.

- ❌ "O áudio ficou ruim porque o microfone estava longe e isso atrapalhou a edição."
- ✅ "O lapela acabou por baixo da gola: prenda ele por fora da camisa e ouça 10s de áudio antes de gravar os 5."

## Passo 4 · Guardar em `content-routines/aprendizados.md`

Sábado mais recente primeiro, logo abaixo do marcador `<!-- entradas novas entram logo abaixo desta linha -->`.

- Já existe o heading daquele sábado → acrescente os bullets nele.
- Não existe → crie `## YYYY-MM-DD (sábado)` logo abaixo do marcador, com os bullets embaixo.

Não mexa em mais nada do arquivo.

## Passo 5 · Confirmar em uma linha

> Registrado em 2026-08-29: 2 aprendizados.

---

## Fora do escopo

- Não toca no Notion, nos roteiros nem nos vídeos.
- Não edita nem reescreve entrada antiga.
- Não avalia a sessão nem dá incentivo: guarda a regra e para.
