# AGENTS.md

## O repositório

Este repositório organiza a produção de conteúdo de Pedro Miyasaki. As ideias vêm do Notion e são transformadas por skills em roteiros de Reel, carrosséis, threads, posts de LinkedIn, artigos de Substack e seus assets.

Não é uma aplicação de software. O objetivo é produzir, revisar e guardar conteúdo com pouco atrito, deixando decisões de linguagem e estrutura para a skill de cada formato.

## Estrutura de pastas

```text
.
├── .agents/
│   └── skills/             # fonte canônica de todas as skills
├── .claude/
│   └── skills -> .agents/skills
├── .cursor/
│   └── skills -> .agents/skills
├── posts/                  # peças produzidas, organizadas por formato e slug
│   ├── script/
│   ├── carousel/
│   ├── thread/
│   ├── linkedin/
│   └── substack/
├── design/                 # identidade visual, templates e provas
├── docs/                   # documentação e pesquisa
├── examples/               # referências de conteúdo
├── scripts/                # automações de render e manutenção
├── templates/              # templates auxiliares
├── video/                  # recursos de produção de vídeo
├── objectives/             # objetivos do projeto
├── TODO.md
├── pyproject.toml
└── uv.lock
```

Edite skills somente em `.agents/skills/`. As pastas `.claude/skills` e `.cursor/skills` são links simbólicos para a mesma árvore.

Cada skill define seu próprio fluxo e sua convenção dentro de `posts/<formato>/<slug>/`. Consulte o `SKILL.md` correspondente antes de produzir ou alterar uma peça.

## Voz

Esta seção reúne os poucos pontos que considero válidos para qualquer produção de conteúdo. Eles são propositalmente curtos para evitar overfitting sem apagar as nuances necessárias de cada canal e tipo de conteúdo.

- Nunca utilizar em dash.
- Nunca utilizar emojis.
- Atentar-se ao "LLM tone", especialmente ao problema inglês para português: modelos tendem a escrever em português apenas traduzindo estruturas do inglês, o que gera vícios de linguagem.
  - `VICIOS.md` (placeholder por enquanto).

## Ferramentas globais

### Notion

O MCP do Notion é a fonte das ideias e o local de atualização do estado delas. O banco canônico é **Ideas**, data source `e2970ca3-7724-4a81-8f12-7ea34c048c67`. Cada skill explica quando deve apenas ler e quando pode escrever.

### Google Chrome

A automação de navegador via MCP permite operar o Google Chrome para pesquisar, abrir páginas, interagir com sites, inspecionar conteúdo e capturar imagens quando a tarefa exigir.
