---
name: write-thread
description: >
  Lê uma ideia do banco Ideas e atua como copywriter sênior para transformá-la
  numa sequência encadeada para o Threads, em registro técnico, denso, direto e
  opinativo. Cada thread funciona sozinha e também como parte do todo. Ative
  com pedidos como "escreve a thread da última ideia", "thread da ideia X" ou
  "gera as threads".
---

# Thread para o Threads

## Ferramentas disponíveis

Use o MCP do Notion para ler o banco **Ideas** e, no fechamento, para atualizar `Status` e `Format` na ideia processada (a única escrita no Notion).

---

## Referências obrigatórias

Leia antes de escrever qualquer thread:

**Via Notion (MCP):**

| Banco | ID | O que procurar |
|---|---|---|
| **Ideas** | `e2970ca3-7724-4a81-8f12-7ea34c048c67` (ID do data source) | A ideia de origem da thread |

---

## Quando agir

Rode esta skill quando o usuário disser algo como:
- "escreve a thread da última ideia"
- "thread da ideia X"
- "escreve a thread"
- "gera as threads"
- ou qualquer variação que signifique transformar uma ideia crua em thread
---

## Protocolo de execução, passo a passo

### Passo 1 · Identificar a ideia

Se o usuário não disse qual:
- Abra o banco **Ideas** (`e2970ca3-7724-4a81-8f12-7ea34c048c67`)
- Filtre por `Status = "Pending"` e ordene por `Date` decrescente (a mais recente primeiro). Se `Date` não existir ou estiver vazio, use `createdTime`
- Pegue a ideia mais recente
- Mostre o título ao usuário e confirme antes de seguir:
  > "Ideia selecionada para a thread: [título]. Sigo com essa?"
Se o usuário indicou um título ou item: ache essa ideia no banco Ideas e use ela direto.

### Passo 2 · Ler a ideia e definir o ângulo

Abra a linha correspondente no banco Ideas e leia tudo que estiver disponível: título, texto cru da ideia, notas ou exemplos anexados, data e status.

A ideia é crua. Transforme ela em material para uma sequência de threads. Extraia ou defina os elementos abaixo:
- Ângulo: a posição específica sobre o tema, não o tema em si
- Hook candidato: a tensão da ideia transformada na thread 1
- Argumento central: a tese da sequência em 1 ou 2 frases
- Exemplo/prova: um caso concreto, real ou hipotético, que ancora o argumento
- CTA: a posição ou provocação que fecha a sequência

Defina também a ACP Phase.

### Passo 3 · Calibrar pelo histórico

Liste os slugs mais recentes em `posts/thread/` e leia a última versão de até cinco sequências: `final.md` quando existir ou o `sketch/v<N>.md` de maior número, nunca `carousel-v<N>.md`.

Use o histórico como few-shot, não como checklist. Observe registro, vocabulário, ritmo, densidade técnica, hooks, fechos, uso de primeira pessoa, opinião, humor, tamanho e formatação. Imite os padrões recorrentes sem copiar frases e dê mais peso aos exemplos recentes. Se houver menos de cinco, use o que existir; se não houver nenhum, siga sem calibração.

Atente-se ao tom mais crítico e opinativo do Threads: seja incisivo sobre práticas e ideias, sem transformar a crítica em ataque pessoal.

### Passo 4 · Escrever a sequência

#### Limite de caracteres por thread
- **500 caracteres por thread, no máximo** (o limite do Threads)

A primeira thread precisa ser um gancho forte e funcionar sozinha. Defina heuristicamente o tamanho, o desenvolvimento e o fecho que melhor servem à ideia, mantendo cada thread compreensível isoladamente e a sequência coerente como um todo.

#### Formatação da saída

Para cada thread, entregue:

```
THREAD 1 - HOOK  (N chars)
[conteúdo da thread]

THREAD 2 - [função]  (N chars)
[conteúdo da thread]

...

THREAD N - CLOSE  (N chars)
[conteúdo da thread]
```

Conte e mostre a quantidade de caracteres de cada thread. Isso evita surpresa na hora de publicar.

### Passo 5 · Apresentar, iterar e salvar localmente

Apresente a sequência completa com a contagem de caracteres por thread.

Derive o slug do título da ideia (minúsculas, hífens no lugar de espaços e caracteres especiais, sem acentos) e salve na hora como `posts/thread/<slug>/sketch/v1.md` com Write, com a sequência completa de threads e as contagens de caracteres.

Pergunte:
> "Pronto para finalizar, ou mais alguma correção?"

Para cada correção pedida:
- Aplique a mudança nas threads afetadas, recalculando a contagem de caracteres onde for preciso.
- Crie `posts/thread/<slug>/sketch/v(N+1).md`: leia a versão anterior, copie as threads que não mudaram verbatim e aplique só o que mudou. Não regenere o que não mudou.
- Pergunte de novo: "Pronto para finalizar, ou mais alguma correção?"

Repita até o usuário confirmar "pronto". Só então passe para o Passo 6.

### Passo 6 · Fechar

Quando o usuário confirmar "pronto", copie o `posts/thread/<slug>/sketch/v<N>.md` de maior número para `posts/thread/<slug>/final.md` com Write: essa cópia é a peça final, e o histórico `sketch/v<N>` fica onde está, como trilha de auditoria. Faça isso antes de mexer no Notion. Depois atualize a ideia de origem no banco Ideas: `Status` → `"Processed"` e `Format` → `"Thread"` (o formato que esta skill produz; a ideia nasce sem formato, e ele só é definido agora, na produção). Essa é a única escrita da skill no Notion. `Status` e `Format` acumulam no banco a foto real do calendário (fase e formato de cada peça produzida).

### Passo 7 · Apontar o próximo passo

> "Thread pronta, salva em `posts/thread/<slug>/final.md`. Próximo passo: publicar manualmente no Threads e tirar print da thread publicada para reaproveitar como post estático no Instagram."
