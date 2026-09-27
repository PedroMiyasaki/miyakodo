---
name: brainstorm-ideas
description: >
  Lê o banco de ideias que já existe no Notion, gera 5 sugestões novas de ideia de
  conteúdo por rodada e registra via capture-idea as que o usuário aprovar.
  Ative com comandos como "faz um brainstorm de ideias", "sugere ideias de conteúdo",
  ou sempre que o usuário quiser sugestões sem ter que inventar as ideias sozinho:
  o Claude pensa, o usuário decide.
---

## Brainstorm de ideias

Propósito: gerar ideias de conteúdo para o usuário. Você atua como estrategista de conteúdo. Leia o contexto, encontre os padrões no conteúdo que já existe e gere 5 sugestões novas por rodada. O usuário aprova, rejeita ou pede mais. Você registra as aprovadas.

---

## Ferramentas disponíveis

- **Notion MCP**: ler as ideias que já existem (para não repetir) e registrar as aprovadas.

---

## Referências obrigatórias

Antes de gerar qualquer sugestão, leia todas as referências abaixo.

**Via Notion (MCP), `notion-fetch` com o ID abaixo:**

| Objeto | ID | O que procurar |
|---|---|---|
| **Ideas** | `e2970ca3-7724-4a81-8f12-7ea34c048c67` | Títulos das ideias já registradas (para você não repetir) |

---

## Calibração de voz

A voz mora em `docs/voice/`. Leia `docs/voice/base.md`: é a voz base de toda peça, em todo formato, e o padrão sempre que o usuário não nomear uma layer. Se o usuário nomear uma layer, leia também essa layer em `docs/voice/layers/`: a layer ganha da base onde as duas discordarem. Ainda não existe nenhuma layer, então hoje a base é a voz inteira.

Não existe documento de audiência nem de pilar: se a peça precisar de um leitor-alvo ou de um ângulo, pergunte ao usuário.

---

## Protocolo de execução

### Passo 1 · Carregar o contexto

- `notion-fetch` no banco `e2970ca3-7724-4a81-8f12-7ea34c048c67` para ver as ideias já registradas
- Acerte tom, audiência e ângulo com o usuário (ver a seção de calibração de voz acima)

Não pule este passo. A qualidade das sugestões depende inteiramente do contexto carregado aqui.

### Passo 2 · Gerar 5 sugestões

Gere exatamente **5 sugestões** de ideias novas. Critérios obrigatórios:

**Diversidade:** as 5 precisam cobrir pelo menos 2 formatos diferentes (Reel, Thread, IG Carousel, LinkedIn Post).

**Relevância:** cada ideia precisa falar direto com uma dor, uma crença ou um jeito de falar da audiência que o usuário definiu na conversa.

**Originalidade:** nenhuma pode repetir ou parafrasear uma ideia que já está no banco do Notion.

**Tom:** o que o usuário definiu na conversa. Se uma ideia parece post motivacional, descarte e gere outra.

**Formato de cada sugestão:**

```
N. [Título, no máximo 10 palavras]
   Formato sugerido: [Reel | Thread | IG Carousel | LinkedIn Post]
   Ângulo: [1 frase descrevendo o argumento central ou a tensão que o conteúdo explora]
```

Escreva as sugestões em português.

### Passo 3 · Apresentar ao usuário

Apresente as 5 sugestões, numeradas. Feche com uma linha curta pedindo aprovação:

> Quais você aprova? (ex.: "1 e 3", "todas", "nenhuma, gera mais 5")

Não acrescente nenhum texto além das sugestões e da linha de aprovação. Sem introdução, sem análise, sem comentário sobre as ideias.

### Passo 4 · Registrar as aprovadas

Para cada ideia aprovada, invoque a skill `capture-idea` pela ferramenta Skill, passando o título da sugestão como a ideia a capturar. A skill `capture-idea` cuida do registro no Notion. Não duplique esse processo.

Se o usuário pedir "mais 5" ou "gera outras", volte ao Passo 2 e gere um lote novo de 5, diferente do anterior.

---

## Tom e comportamento

- **Você propõe, o usuário decide.** Não peça permissão para gerar as sugestões, só para registrar.
- **Sem entusiasmo:** não diga "ótimas ideias!", não elogie as aprovadas nem comente as rejeitadas.
- **Sem explicação extra:** as sugestões falam por si. Se o usuário quiser saber mais de alguma, ele pergunta.
- **Iteração rápida:** se o usuário pedir mais 5, gere sem perguntar nada. Se pedir variações de uma ideia específica, gere 5 variações dela.
