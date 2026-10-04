# [AGENTS.md](http://AGENTS.md)

## O repositório

Este repositório é o sistema de produção de conteúdo de Pedro Miyasaki. Ele reúne as skills que transformam ideias em roteiros de Reel, carrosséis, threads, posts de LinkedIn e artigos de Substack, além dos arquivos de trabalho e assets de cada peça.

O fluxo começa no banco **Ideas**, no Notion. Uma skill lê a ideia, produz o formato pedido e salva as iterações localmente em `posts/`. O usuário revisa a peça até dizer "pronto"; só então a versão aprovada vira a entrega final e o estado da ideia é atualizado no Notion. A publicação na plataforma de destino é manual.

Este não é um projeto de software tradicional. Não há aplicação para executar nem suíte de testes como etapa padrão. Scripts existem apenas para tarefas mecânicas, como renderização e manutenção de links. A prioridade é reduzir o atrito da produção sem transformar preferências acumuladas em regras rígidas. Cada skill deve preservar espaço para julgamento, linguagem e estrutura adequados ao formato e à ideia.

## Estrutura de pastas

```text
.
├── .agents/
│   └── skills/             # fonte canônica de todas as skills
├── .claude/
│   └── skills -> .agents/skills
├── .cursor/
│   └── skills -> .agents/skills
├── CLAUDE.md -> AGENTS.md  # espelho local destas instruções
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

`AGENTS.md` também é canônico. `CLAUDE.md` aponta para ele e não deve receber uma cópia independente.

Dentro de `posts/`, cada peça mora em `posts/<formato>/<slug>/`. Em geral, `sketch/` guarda as versões de trabalho e a raiz do slug guarda somente os arquivos aprovados para publicação. Os detalhes variam entre formatos, então consulte o `SKILL.md` correspondente antes de produzir, revisar ou finalizar uma peça.

`design/` é a fonte do sistema visual. `examples/` oferece material de referência, não templates obrigatórios. `scripts/` automatiza trabalho mecânico e não deve concentrar decisões editoriais.

## Voz

Esta não é uma definição completa da voz do usuário. Ela reúne apenas os poucos princípios que considero válidos em qualquer produção de conteúdo. Os pontos são propositalmente curtos: regras globais demais fazem os canais soarem iguais e induzem overfitting. As nuances de ritmo, densidade, estrutura e posicionamento devem vir da ideia, da skill do formato e da calibração pelos conteúdos recentes.

- **Nunca utilizar em dash.** Reestruture a frase com ponto, vírgula, dois-pontos ou parênteses. O hífen continua válido quando sua função gramatical exigir.
- **Nunca utilizar emojis.** Não use emojis em títulos, corpo, listas, CTAs ou como decoração visual.
- **Evitar "LLM tone".** Escreva diretamente em português do Brasil, em vez de montar a frase em inglês e traduzi-la. Modelos tendem a transportar sintaxe, ritmo e fórmulas retóricas do inglês para o português, produzindo um texto correto, mas artificial. Leia a frase como fala e prefira construções que um brasileiro usaria naturalmente.
  - `VICIOS.md` será o inventário desses padrões. Por enquanto, é apenas um placeholder.

## Ferramentas globais

### Notion

O MCP do Notion conecta o repositório ao banco de ideias. O banco canônico é **Ideas**, data source `e2970ca3-7724-4a81-8f12-7ea34c048c67`.

Skills de produção usam o Notion para localizar e ler a ideia de origem. A escrita normalmente acontece apenas no fechamento, para registrar o status e o formato produzidos. O conteúdo da peça permanece nos arquivos locais. Siga sempre a regra da skill ativa, especialmente quando ela definir uma exceção.

### Google Chrome

A automação de navegador via MCP permite operar o Google Chrome como uma ferramenta de trabalho. Use-a quando a tarefa exigir pesquisa na web, interação com páginas, inspeção de conteúdo ao vivo, verificação visual ou captura de imagens.

Antes de agir numa página, confira o estado atual da aba. Depois de uma interação importante, verifique o resultado em vez de presumir que ela funcionou. Captchas, logins, permissões e confirmações sensíveis devem ser deixados para o usuário.