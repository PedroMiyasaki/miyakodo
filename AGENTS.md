# [AGENTS.md](http://AGENTS.md)

## O repositório

Este repositório produz o conteúdo da Miyakodo, a escola de inteligência artificial para empreendedores. Pedro Miyasaki é o CEO, o fundador e o único professor. A voz pública das peças é a dele, em primeira pessoa. O perfil `@pedro.miyasaki.ia` e o nome Pedro nas peças de vídeo continuam, porque o canal de publicação é o perfil do fundador. Isso é founder-led growth: publicar no perfil do fundador para a escola crescer. A instituição é a escola, não uma marca pessoal.

No longo prazo, a escola caminha para uma comunidade, algo mais complexo. O desenho dessa comunidade não está definido neste repositório.

Ele reúne as skills que transformam ideias em roteiros de Reel, carrosséis, threads, posts de LinkedIn e artigos de Substack, além dos arquivos de trabalho e assets de cada peça.

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
├── README.md               # o que é o repositório e a escola
├── posts/                  # peças produzidas, organizadas por formato e slug
│   ├── script/
│   ├── carousel/
│   ├── thread/
│   ├── linkedin/
│   └── substack/
├── design/                 # identidade visual da escola Miyakodo: identity.md, apresentação, fontes, logo, mascote e textura
├── docs/                   # documentação e pesquisa
├── examples/               # referências de conteúdo
├── scripts/                # automações de render e manutenção
├── templates/              # templates auxiliares
├── video/                  # recursos de produção de vídeo
├── objectives/             # objetivos do projeto
├── tools/
│   └── instagram-autodm/   # Worker de comentários; a skill de deploy mora aqui
├── TODO.md
├── pyproject.toml
└── uv.lock
```

Edite skills somente em `.agents/skills/`. As pastas `.claude/skills` e `.cursor/skills` são links simbólicos para a mesma árvore. Exceção: a skill `deploy-instagram-autodm` mora em `tools/instagram-autodm/.agents/skills/deploy-instagram-autodm/SKILL.md`. A entrada `.agents/skills/deploy-instagram-autodm/` na raiz só aponta para esse arquivo.

`AGENTS.md` também é canônico. `CLAUDE.md` aponta para ele e não deve receber uma cópia independente.

Dentro de `posts/`, cada peça mora em `posts/<formato>/<slug>/`. Em geral, `sketch/` guarda as versões de trabalho e a raiz do slug guarda somente os arquivos aprovados para publicação. Os detalhes variam entre formatos, então consulte o `SKILL.md` correspondente antes de produzir, revisar ou finalizar uma peça.

`design/` é a fonte do sistema visual da escola Miyakodo. O índice está em `design/identity.md`. Na mesma pasta ficam a apresentação em PDF, as fontes, o logo e o mascote com textura. A produção de vídeo novo mora na skill `produzir-video`, não em `design/` nem nas pastas de peças antigas. `examples/` oferece material de referência, não templates obrigatórios. `scripts/` automatiza trabalho mecânico e não deve concentrar decisões editoriais.

## Edição de vídeo

Vídeo novo passa pela skill `produzir-video` ([SKILL.md](.agents/skills/produzir-video/SKILL.md)). Há um pipeline só: um roteiro JSON vira uma composição HyperFrames 1080×1920. As skills do HyperFrames renderizam. Não há caminho paralelo.

Dois modos:

- **`sem-gravacao`**: Pedro não grava. Entram o roteiro e a faixa de voz. Saem o avatar 2D do rosto dele, legendas no terço superior e motion graphics na paleta de `design/identity.md`. A faixa e o `words` podem sair da skill `narrar-roteiro`: ela clona a voz do Pedro na GPU da máquina dele e grava `voice.wav` mais `words.json`. A amostra fica em `video/inputs/voice-ref/` e não entra no git.
- **`gravacao`**: Pedro grava um talking head. Entram o roteiro, o bruto e a voz na mesma janela de tempo. O pipeline tira silêncio entre frases e monta as cenas por cima: split, motion em tela cheia ou o criador em tela cheia com punch-in.

O roteiro escolhe cenas combináveis (legenda, avatar, timeline, mockup, contador, diagrama, chat, código, telefone, grade, scanline, pastas, lista, citação, badge). `purpose` pode ser tutorial, opinião, notícia, lista, história ou CTA. Isso não troca o motor.

Peças já feitas em `video/projects/` antes deste pipeline ficam como arquivo. Não são o modo de produzir a próxima.

## Voz

A voz pública é a de Pedro Miyasaki, fundador e único professor da Miyakodo. As peças continuam em primeira pessoa, no perfil dele.

Esta não é uma definição completa dessa voz. Ela reúne apenas os poucos princípios que considero válidos em qualquer produção de conteúdo. Os pontos são propositalmente curtos: regras globais demais fazem os canais soarem iguais e induzem overfitting. As nuances de ritmo, densidade, estrutura e posicionamento devem vir da ideia, da skill do formato e da calibração pelos conteúdos recentes.

- **Nunca utilizar em dash.** Reestruture a frase com ponto, vírgula, dois-pontos ou parênteses. O hífen continua válido quando sua função gramatical exigir.
- **Nunca utilizar emojis.** Não use emojis em títulos, corpo, listas, CTAs ou como decoração visual.
- **Evitar "LLM tone".** Escreva diretamente em português do Brasil, em vez de montar a frase em inglês e traduzi-la. Modelos tendem a transportar sintaxe, ritmo e fórmulas retóricas do inglês para o português, produzindo um texto correto, mas artificial. Leia a frase como fala e prefira construções que um brasileiro usaria naturalmente.
  - `VICIOS.md` será o inventário desses padrões. Por enquanto, é apenas um placeholder.

## Git

Peça de conteúdo não abre pull request. Roteiro, post, rascunho, carrossel, artigo e saída de pesquisa entram por commit direto na `main`. A publicação na rede continua manual.

Pull request é para código, skill e infraestrutura. Mudar uma skill, um script ou a configuração do repositório passa por branch e pull request. A skill `content-research` é infraestrutura quando o arquivo dela muda. A rodada diária dela não é: grava ideia no Notion e não abre pull request.

Saída intermediária ou que dá para gerar de novo não entra no git. O caminho está no `.gitignore`. Texto, HTML e imagem da peça continuam versionáveis. Vídeo publicado, áudio e render pesado ficam de fora.

## Ferramentas globais

### Notion

O MCP do Notion conecta o repositório ao banco de ideias. O banco canônico é **Ideas**, data source `e2970ca3-7724-4a81-8f12-7ea34c048c67`.

Skills de produção usam o Notion para localizar e ler a ideia de origem. A escrita normalmente acontece apenas no fechamento, para registrar o status e o formato produzidos. O conteúdo da peça permanece nos arquivos locais. Siga sempre a regra da skill ativa, especialmente quando ela definir uma exceção.

A skill `content-research` é a exceção de entrada. Na rodada diária ela cria ideias novas com `Status` `Pending`. Não altera o status de uma ideia que já existe e não publica.

### Google Chrome

A automação de navegador via MCP permite operar o Google Chrome como uma ferramenta de trabalho. Use-a quando a tarefa exigir pesquisa na web, interação com páginas, inspeção de conteúdo ao vivo, verificação visual ou captura de imagens.

Antes de agir numa página, confira o estado atual da aba. Depois de uma interação importante, verifique o resultado em vez de presumir que ela funcionou. Captchas, logins, permissões e confirmações sensíveis devem ser deixados para o usuário.