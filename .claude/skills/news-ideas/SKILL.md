---
name: news-ideas
description: >
  Lê as notícias recentes de IA nas principais fontes internacionais, destila cada
  fato relevante (modelos novos, apps, rodadas de investimento, startups, pesquisa,
  aquisições, regulação) numa ideia de conteúdo e grava direto no banco Ideas do
  Notion. Ative com comandos como "atualiza as ideias com as notícias de IA de hoje",
  "puxa as manchetes de IA de hoje" ou "roda o radar de notícias".
---

## Ideias a partir do noticiário de IA

Propósito: varrer o noticiário de IA, identificar o que conta de verdade como notícia e converter cada fato relevante numa ideia de conteúdo registrada no banco. A saída são ideias prontas para entrar na fila.

Toda ideia gerada carrega a mesma intenção de fundo: reportar um fato do noticiário por meio de conteúdo. O fato varia, a intenção não. Um modelo novo, uma rodada de investimento, um app recém-lançado, uma aquisição, um paper ou uma mudança regulatória: cada caso vira "como o usuário conta esse fato para a audiência dele".

---

## Ferramentas disponíveis

- **WebFetch**: puxar os digests curados de notícias
- **WebSearch**: pegar as notícias quentes recentes que ainda não entraram nos digests
- **Notion MCP**: ler as ideias já registradas (dedupe)
- **Bash**: ler e escrever `last-run.txt`, o marcador da janela de varredura
- **Skill `capture-idea`**: cuida do registro no Notion. Não duplique essa escrita.

---

## Referências obrigatórias

Antes de gerar qualquer ideia, carregue tudo abaixo:

**Via Notion (MCP), `notion-fetch` com o ID abaixo:**

| Objeto | ID | O que procurar |
|---|---|---|
| **Ideas** | `e2970ca3-7724-4a81-8f12-7ea34c048c67` | Títulos e Notes das ideias já registradas (para você não repetir uma história) |

---

## Calibração de voz

A voz mora em `docs/voice/`. Leia `docs/voice/base.md`: é a voz base de toda peça, em todo formato, e o padrão sempre que o usuário não nomear uma layer. Se o usuário nomear uma layer, leia também essa layer em `docs/voice/layers/`: a layer ganha da base onde as duas discordarem. Ainda não existe nenhuma layer, então hoje a base é a voz inteira.

Não existe documento de audiência nem de pilar: se a peça precisar de um leitor-alvo ou de um ângulo, pergunte ao usuário.

---

## A janela de varredura

`.claude/skills/news-ideas/last-run.txt` guarda uma única linha: o timestamp UTC da última varredura, em ISO 8601 (`2026-08-26T14:03:11Z`). Ele define a janela que esta rodada cobre: **daquele timestamp até agora**.

Leia no Passo 1 e escreva no Passo 7, em toda rodada, tenha registrado alguma coisa ou não. A janela foi varrida de qualquer jeito.

Se o arquivo não existir (primeira rodada da vida, ou alguém apagou), use **os últimos 7 dias** e siga em frente. Não trate isso como erro.

A janela é um filtro de *data de publicação*, não uma promessa de que as fontes vão respeitar. Os digests reimprimem itens antigos e os resultados de busca escorregam: confira a data de cada candidato e descarte o que foi publicado antes de a janela abrir. O dedupe contra o banco continua rodando por cima disso: uma história na fronteira que já foi registrada não entra duas vezes.

---

## Fontes de notícia

### Obrigatórias, em toda rodada, sem exceção

| Fonte | URL |
|---|---|
| AI News (digest diário do smol.ai) | `https://news.smol.ai/` |
| Anthropic News | `https://www.anthropic.com/news` |
| OpenAI News | `https://openai.com/news/` |
| Google Gemini News | `https://gemini.google/latest-news/` |

**Os três blogs dos provedores são mídia própria: a maior parte do que eles publicam é marketing, não notícia.** Julgue cada post antes de ele virar ideia. Um modelo lançado, uma capacidade real, uma mudança de preço, uma depreciação, um benchmark ou um paper publicado é notícia. Um case de cliente, um anúncio de parceria sem produto por trás, um manifesto de política, um rebrand, um pitch de plano enterprise ou um ensaio do tipo "nós acreditamos" é propaganda: descarte. Quando o post é um lançamento embrulhado em marketing, fique com o fato lançado e jogue fora a embalagem.

### Também conferir

| Fonte | URL |
|---|---|
| TLDR AI | `https://tldr.tech/ai` |
| The Batch (DeepLearning.AI) | `https://www.deeplearning.ai/the-batch/` |
| Import AI | `https://importai.substack.com/` |
| Latent Space (ensaios, podcast) | `https://www.latent.space/` |
| Simon Willison | `https://simonwillison.net/` |
| Hacker News (página inicial) | `https://news.ycombinator.com/` |

A lista obrigatória é um piso, não um teto: a varredura ainda cobre as fontes acima **e** roda **uma passada de WebSearch** atrás de notícias quentes dos últimos 7 dias que ainda não entraram nos digests (ex.: `"AI" funding round`, `new LLM release`, `AI acquisition`, ancoradas na janela de varredura). Tudo que vale reportar naquela semana e que nenhum blog de provedor publicaria (investimento, aquisição, regulação, labs concorrentes, open source) vem daí. No Hacker News, considere só os itens de IA.

---

## Protocolo de execução

### Passo 1 · Carregar o contexto (em paralelo)

- `notion-fetch` no data source `e2970ca3-7724-4a81-8f12-7ea34c048c67` para ler as ideias já registradas (títulos + Notes, que é de onde sai a URL de origem para o dedupe)
- Leia o marcador da janela e carimbe esta rodada de uma vez só:

  ```bash
  cat .claude/skills/news-ideas/last-run.txt 2>/dev/null || echo "(no marker — sweep the last 7 days)"
  date -u +%Y-%m-%dT%H:%M:%SZ
  ```

  A primeira linha é onde a janela **abre**; a segunda é `NOW`, onde ela fecha. Guarde essa string exata: é o que o Passo 7 escreve.
- Acerte tom, audiência e ângulo com o usuário (ver a seção de calibração de voz acima)

Não pule este passo: o dedupe, a janela de varredura e a calibração de relevância dependem inteiramente do que é carregado aqui.

### Passo 2 · Buscar as notícias

Rode WebFetch em cada fonte curada, mais a passada de WebSearch. Reúna os fatos candidatos publicados **dentro da janela** do Passo 1: desde a última varredura, até `NOW`. Não inclua nada publicado antes de a janela abrir, mesmo que apareça na busca ou esteja na página inicial de um digest.

### Passo 3 · Selecionar o que é notícia de verdade

Fique só com fatos **concretos, datáveis e verificáveis** do espaço de IA que tocam numa dor, numa decisão ou numa curiosidade da audiência que o usuário definiu.

**Descarte:**
- Opinião requentada, listicles, conteúdo promocional vestido de notícia
- Boatos sem fonte confiável
- Qualquer fato que já está representado no banco (mesma história **ou** mesma URL de origem). O dedupe é obrigatório, porque esta skill escreve sem revisão humana e pode rodar de novo amanhã

**Volume:** igual ao número de histórias relevantes do dia. Pode ser 2, pode ser 8. Não force um número e **não invente notícia para bater cota**. Se nada novo passar na régua, não registre nada e diga isso.

### Passo 4 · Enquadrar cada história como ideia

Para cada história selecionada, produza:

**Título da ideia:** no máximo 10 palavras, na voz do usuário, escrito em português. Tem que ser o *ângulo de conteúdo*, não a manchete copiada. Conceito pelo efeito, não pelo nome, sem hype e sem jargão sem explicação. Nunca abra com "Você sabia", "Hoje" ou "Olá pessoal".

- Manchete: "OpenAI lança o GPT-5.5 com janela de 2M de tokens"
- Título ruim (cópia): "GPT-5.5 chega com 2M de tokens de contexto"
- Título bom (ângulo): "Janela de contexto gigante não conserta seu problema de processo"

**Notes:** um resumo do fato em 1 ou 2 frases + `Fonte: <URL>` + `Formato sugerido: <Reel | Thread | IG Carousel | LinkedIn Post>`.

### Passo 5 · Registrar tudo

Para cada ideia, invoque a skill `capture-idea` pela ferramenta Skill, passando o **título enquadrado** e o **bloco de notas** (resumo + `Fonte: <URL>` + formato sugerido). A `capture-idea` cuida da escrita no Notion. A URL de origem **precisa ser preservada no campo Notes**.

Não peça aprovação e não apresente as ideias antes. Registre todas direto.

### Passo 6 · Reportar

Feche com uma lista curta do que foi registrado: uma linha por ideia, com a fonte. Sem introdução e sem comentário.

```
Registrado no banco:
1. [título] — [fonte]
2. [título] — [fonte]
```

Se nada passou na régua: `Nada novo que valha cobrir nas notícias de hoje. Nada registrado.`

Diga em uma linha qual janela foi varrida: `Janela: <last-run> → <NOW>` (ou `últimos 7 dias → <NOW>` numa primeira rodada).

### Passo 7 · Carimbar a rodada

Última coisa, sempre, mesmo quando nada foi registrado, mesmo quando um fetch falhou:

```bash
printf '%s
' '<NOW>' > .claude/skills/news-ideas/last-run.txt
```

`<NOW>` é o timestamp exato capturado no Passo 1, não uma chamada nova de `date`: o que foi publicado enquanto a varredura rodava fica dentro da próxima janela em vez de cair no vão.

---

## Tom e comportamento

- **Sem hype.** O ângulo é sempre o que o fato muda na prática para a audiência, não uma reação à notícia.
- **Não copie a manchete.** O título é o ângulo de conteúdo, não o press release.
- **Não invente.** Se a fonte não confirma o fato, ele não vira ideia.
- **Dedupe primeiro.** Antes de registrar, confirme que a história ainda não está no banco.
- **Sempre carimbe.** O Passo 7 roda em todo caminho, inclusive o vazio. Um carimbo pulado faz a próxima rodada varrer de novo um terreno já coberto.

---

## Fora do escopo

- Não escreve o conteúdo final (isso é trabalho das skills `write-*`)
- Não publica nada fora do banco Ideas
- Não opina sobre a notícia nem ranqueia as ideias
- Não pede aprovação: registra o que passar na régua
