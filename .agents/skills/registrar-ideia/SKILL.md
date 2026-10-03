---
name: registrar-ideia
description: >
  Guarda ideias cruas do usuário no banco Ideas do Notion com estrutura mínima.
  Ative com "registra essa ideia", "guarda esse pensamento", ou sempre que a
  mensagem parecer uma ideia guardada para virar conteúdo depois.
---
## registrar-ideia

**Propósito:** tirar a ideia da cabeça do usuário e deixá-la pronta para virar conteúdo depois. Ele só despeja o pensamento; estrutura, classificação e registro são trabalho seu.

**Quando agir:** qualquer mensagem que pareça ideia, observação, aforismo ou insight — mesmo incompleta ou abstrata. Não exija comando específico. Não pergunte nada antes de salvar.

## O que gravar

Banco **Ideas** · `e2970ca3-7724-4a81-8f12-7ea34c048c67` (via Notion MCP):

| Campo | Valor |
|---|---|
| `Idea` | O pensamento central reescrito como título, em português, no máximo 10 palavras |
| `Date` | Hoje, formato ISO |
| `Status` | Sempre `Pending` |
| `Notes` | O texto original do usuário, como está, mais contexto se ele mandou |
| `ACP Phase` | Um de `A · Audience`, `C · Community`, `P · Product` (texto exato) |
| `Format` | **Vazio.** Formato se decide na produção, nunca na captura |

## Como classificar a ACP Phase

Classifique, não julgue — ideia boa ou ruim não é problema seu aqui:

- **`P · Product`** só se o texto menciona um caso, projeto ou resultado real e mensurável do próprio usuário. Hipótese genérica não é Product.
- Senão, pergunte-se: um desconhecido pararia por curiosidade técnica? **`A · Audience`**. Só faz sentido para quem já acompanha e quer ir fundo? **`C · Community`**.

## Comportamento

- **Salve primeiro, pergunte nunca** (antes de salvar). Não peça formato, ângulo ou fase.
- **Não desenvolva:** sem roteiro, sem hook, sem sugestão de melhoria. Só título limpo + despejo bruto.
- **Confirme em uma linha:** `Salvo: "<título>" — <fase>`. Várias ideias de uma vez, confirme em sequência.
