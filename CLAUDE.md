# CLAUDE.md

Este arquivo orienta o Claude Code (claude.ai/code) quando ele trabalha neste repositório.

## O que é este repositório

Este repositório guarda a produção de conteúdo do usuário: roteiros de Reel, threads, carrosséis e posts de LinkedIn. Não é um projeto de software. Tudo que parece "código" aqui é conteúdo. A produção roda por skills mais o MCP do Notion.

Na prática, isso quer dizer que não existe build, não existe suíte de testes e não existe linter. O que sai daqui é texto e imagem, não software.

**Estado atual: o repositório está em transição.** A marca antiga foi removida (documentos de estratégia, sistema visual e logos foram embora) e a direção nova, uma marca pessoal, ainda está sendo montada.

Já reconstruído: a voz base (`docs/voice/base.md`), a cadência de fim de semana (`content-routines/default/`) e o sistema visual (`design/identity.md`). Ausência deliberada, não pendência: não existe documento de audiência nem documento de pilares de conteúdo. Os dois foram cortados para simplificar o processo. Se uma peça precisa de um leitor-alvo ou de um ângulo, pergunte ao usuário.

**Idioma.** O repositório trabalha em português do Brasil: skills, docs, este arquivo e a conversa. As peças publicadas (roteiro, carrossel, thread, post de LinkedIn, artigo de Substack) saem em português do Brasil. O schema do Notion (nomes de propriedades e valores) fica em inglês: o banco de ideias é um só.

## Como o trabalho flui aqui

A razão de ser deste repositório é produzir conteúdo bom com pouco atrito. Quando o usuário pede um post, um roteiro, uma thread, um carrossel ou a captura de uma ideia, invoque a skill correspondente e entregue o melhor rascunho possível, em vez de forçar o pedido por um processo rígido.

O fluxo é direto, sem etapa de brief no meio: a ideia é capturada no banco **Ideas** → uma skill de conteúdo (`write-script`, `carousel`, `write-thread`, `build-linkedin`, `write-substack`) lê a ideia, escreve e refina o rascunho localmente em `posts/<type>/<slug>/sketch/` por quantas iterações forem necessárias → quando o usuário confirma "pronto", a versão final é copiada para `posts/<type>/<slug>/final.md`. Não existe banco intermediário de publicação: a peça mora localmente, e a única escrita de volta no Notion acontece no "pronto" (`Status` → `Processed`, mais o `Format` que foi produzido).

Toda skill de produção de conteúdo carrega o mesmo passo de fechamento padronizado: **registrar `Status` → `Processed` e o `Format` da peça** no "pronto". São esses dois campos que acumulam a foto real do calendário no banco: uma ideia nasce sem formato, e o formato é decidido durante a produção. Essa lista de skills não é fechada: ao criar uma skill de produção nova, copie o passo de fechamento de uma existente.

**`write-substack` é a única exceção documentada, e só no caminho de reuso.** O artigo reescreve uma tese cuja ideia já foi fechada pelo Reel, e uma ideia carrega um único `Format`. Escrever `Substack` por cima apagaria o formato primário e corromperia a foto do calendário que o banco acumula, então o caminho de reuso não escreve nada no Notion. Rodando sozinha numa ideia `Pending` nova, a skill fecha a ideia normalmente com `Format` → `Substack`. Não "conserte" o caminho de reuso para ficar igual às outras skills.

**`carousel` é a exceção à divisão escrever-depois-montar.** Ela produz copy *e* arte numa skill só, porque num carrossel os dois são uma entrega só: a headline é a âncora visual, um template travado só se sustenta se a copy tem uma forma que se repete, e mexer na copy costuma ser a correção certa para um problema visual. O padrão de craft dela mora em `.claude/skills/carousel/assets/carousel-craft.md`, extraído por engenharia reversa do corpus viral em `examples/carousels/`, e governa as duas metades. Threads mantêm a divisão (`write-thread` → `build-thread-carousel`), porque uma thread sai como texto e o carrossel é um derivado opcional.

As skills são invocadas por comandos naturais em português (por exemplo "escreve o roteiro da última ideia", "faz um carrossel", "escreve um post pro LinkedIn"), **não** por slash commands. Elas moram em `.claude/skills/<skill-name>/SKILL.md` e são descobertas automaticamente. Quando um pedido bate com uma delas, invoque pela ferramenta Skill.

`writing-feedback` é a meta-skill: no fim de uma sessão de produção o usuário invoca ela para consolidar toda correção de tom e de escrita feita na conversa em regras permanentes na pasta de voz, `docs/voice/base.md` por padrão, ou uma layer nomeada em `docs/voice/layers/`.

## Rotinas de conteúdo

`content-routines/` guarda a cadência de operação: quando o trabalho acontece, em oposição a como uma peça é feita. `default/` é o fim de semana normal. `maintainance/` é o modo viagem, em que nada é gravado e a semana roda com 7 carrosséis em vez de 5 reels. Outra cadência (um modo de dia de semana, uma semana de lançamento) vira uma pasta irmã. **Uma mudança na cadência entra nos dois modos.** O artigo semanal do Substack, por exemplo, é disparado logo cedo no domingo e publicado nesse mesmo domingo em cada um.

O modo default produz e agenda a semana inteira em dois dias. De segunda a sexta nada é produzido.

| Arquivo | O que é |
|---|---|
| `default/README.md` | O que a semana produz, a definição de 🔥, por que o setup é o que é, regras de stock |
| `default/saturday.md` | 5 roteiros → gravação em lote → mover os arquivos → disparar a primeira passada de edição |
| `default/sunday.md` | Disparar o artigo → revisar os 5 cortes → 3 posts de LinkedIn → publicar e agendar a semana |

Saída por semana: **5 reels (Instagram) + 3 posts técnicos de LinkedIn + 1 artigo ilustrado no Substack = 9 posts a partir de 5 gravações.** Os posts de LinkedIn reaproveitam as ideias de onde os reels saíram, e o artigo normalmente aprofunda uma delas ainda mais, então uma ideia rende até três vezes. O artigo é a exceção que pode vir de fora das cinco: ele é escrito e publicado no mesmo domingo, e esse lag zero é o que faz dele o único slot em que notícia perecível é permitida. O irmão dele no LinkedIn sai na segunda e linka de volta para o artigo, que é onde alcance frio vira assinante. As mesmas 5 sessões de Claude Code carregam os dois dias: a sessão N escreve o roteiro N no sábado, edita o vídeo N e é retomada no domingo para revisar aquele corte.

**Ao editar esses arquivos, mantenha a divisão:** os dois arquivos de dia são checklists trabalhados de cima para baixo com as mãos ocupadas, então o raciocínio fica no README e só as decisões tomadas na hora ficam inline.

## Calibração de voz

A voz base de toda peça, em todo formato, é `docs/voice/base.md`. Leia antes de escrever. As layers que empilham por cima moram em `docs/voice/layers/`. Quando uma layer se aplica, ela ganha da base naquela peça.

Deliberadamente **não existe documento de audiência nem documento de pilares de conteúdo**. Os dois foram cortados para simplificar o processo. Se uma peça precisa de um leitor-alvo ou de um ângulo, pergunte ao usuário. Não reconstrua um perfil de audiência a partir de conteúdo antigo.

## MCP do Notion: IDs críticos

O banco de ideias é o único objeto canônico no Notion. Trate o ID como canônico:

| Objeto | ID |
|---|---|
| **Ideas** (data source) | `e2970ca3-7724-4a81-8f12-7ea34c048c67` |

O schema dele está em inglês: propriedades `Idea`, `Notes`, `Date`, `Status`, `Format`, `ACP Phase`. Valores de Status: `Pending` / `Processing` / `Processed` / `Discarded`. Valores de Format: `Reel` / `IG Carousel` / `Thread` / `LinkedIn Post`, mais `Substack`, **ainda não criado** (veja abaixo). Valores de ACP Phase: `A · Audience` / `C · Community` / `P · Product`.

A propriedade `Pillar` foi apagada junto com o documento de pilares de conteúdo. Não recrie.

O Notion tem dois papéis. É a **fonte de leitura** das skills de produção (`write-script`, `carousel`, `write-thread`, `build-linkedin`, `write-substack`): elas leem a ideia daqui, salvam o conteúdo localmente em `posts/`, e a única escrita de volta é marcar `Status` como `Processed` e registrar o `Format` no fim (o conteúdo em si nunca sobe). E é o **alvo de escrita** da captura de ideias (`capture-idea`, `brainstorm-ideas`, `content-research`), que registram ideias novas no banco. Leituras (`notion-search`, `notion-fetch`) são pré-aprovadas. Escrever no banco de ideias (`create-database-row`) pede confirmação, e isso é de propósito, não é configuração errada.

**Cuidado ao mudar o schema:** renomear as opções de uma propriedade select pelo MCP substitui o conjunto de opções inteiro e apaga em silêncio o valor guardado em toda linha. Tire um snapshot das linhas antes e restaure depois da mudança.

É por isso que a opção `Substack` em `Format` é adicionada **na mão, pela interface do Notion**: um clique, risco zero. Até 2026-09-05 ela não tinha sido adicionada. `write-substack` só precisa dela no caminho standalone. Se a opção não existir ali, a skill para e pergunta, em vez de criar pelo MCP.

## Convenção de rascunho local

As skills de produção (script, carousel, thread, linkedin, substack) seguem um protocolo estrito de rascunho:

1. Slug = título → minúsculas, sem acento, hífen no lugar de espaço e pontuação.
2. O primeiro rascunho é salvo em `posts/<type>/<slug>/sketch/v1.md` no momento em que é apresentado, onde `<type>` é `script`, `carousel`, `thread`, `linkedin` ou `substack`, conforme a skill que produziu.
3. Toda correção do usuário cria `posts/<type>/<slug>/sketch/v(N+1).md` na mesma pasta. Leia v(N), copie os blocos que não mudaram **verbatim** e aplique só o diff. Nunca regenere conteúdo que não mudou.
4. Quando o usuário confirma "pronto" explicitamente, o `sketch/v<N>.md` de número mais alto é copiado para `posts/<type>/<slug>/final.md`. Essa cópia é a peça publicável, e o histórico `sketch/v<N>` fica onde está como trilha de auditoria. A skill então atualiza a ideia de origem no Notion (`Status` → `Processed` e o `Format` da peça, e nada do conteúdo sobe).

Esse versionamento é deliberado: os arquivos locais são a trilha de auditoria e a fonte única da peça. A publicação é manual, feita pelo usuário na plataforma de destino a partir do arquivo final.

**Tudo de uma peça mora em `posts/<type>/<slug>/`, assets visuais incluídos.** A pasta tem dois níveis. `sketch/` é o material de trabalho (`v<N>.md`, as composições HTML, imagens de origem que o usuário solta lá) e a raiz do slug guarda só o que é publicado, nada mais:

| Tipo | Raiz do slug | `sketch/` |
|---|---|---|
| `script` | `final.md`, `reels.mp4`, `caption.md`, `cover.png` | `v<N>.md`, `cover.html` |
| `carousel` | `final.md` (copy dos slides + legenda do post), `01.png` … `10.png` | `v<N>.md`, `carousel.html` |
| `thread` | `final.md` (o texto da thread), `01.png` … `10.png` quando `build-thread-carousel` roda | `v<N>.md`, `carousel-v<N>.md` (a reescrita da copy para slide), `carousel.html`, `images/` |
| `linkedin` | `final.md`, `image.png` (URL de origem registrada no rodapé do `final.md`) | `v<N>.md` |
| `substack` | `final.md` (título + subtítulo + artigo com marcadores de imagem inline + rodapé de metadados), `cover.png`, `01.png` … `NN.png` | `v<N>.md`, `shotlist.md` |

Os PNGs renderizados ficam soltos na raiz do slug, sem subpasta `render/` nem `editorial/`, e a composição HTML é um intermediário de build, então fica em `sketch/`. `output/` sumiu por completo: toda skill escreve em `posts/<type>/<slug>/`. Um Reel não é um objeto próprio. Ele é a entrega do roteiro, então o vídeo, a legenda do post e a capa caem na pasta do próprio roteiro.

## Vídeo: Reels

Vídeo de Reel é produzido com Hyperframes, pela skill `hyperframes`. No "pronto", as entregas ficam na pasta do roteiro, `posts/script/<slug>/`: `reels.mp4`, `caption.md` e `cover.png`. A capa segue o Alvinegro e o arquétipo `01 COVER`. Os nomes são fixos; o slug identifica a pasta.

## Sistema visual: Alvinegro

`design/identity.md` é o sistema visual de toda entrega com layout próprio: preto e branco estrito, display grotesca pesada, line art com wobble de traço à mão e preenchimento em halftone. `design/proof/` guarda uma prova renderizada de três slides: copie o `<style>` e o `<defs>` dela para começar uma peça nova. **Não improvise paleta nem fonte**, e não traga a marca antiga de volta.

O brand book completo é `design/brandbook/book.html` (17 páginas, renderizadas em `render/`). Ele é o sistema *mostrado*. `identity.md` é o sistema *enunciado*, e o markdown é canônico se os dois algum dia discordarem. Ao lado dele: `design/logotype/` (o stamp mark, o badge e o masthead, mais as rotas que foram exploradas), `design/templates/slides.html` (oito arquétipos de slide) e `design/stationery/stationery.html` (cartão de visita e papel timbrado A4, só digital). Todos renderizam por `scripts/render_html_to_pngs.py`: nada aqui precisa de ferramenta de design.

A arte é gerada, não buscada: geometria SVG limpa rasgada por um filtro `feTurbulence` + `feDisplacementMap` na hora do render, com preenchimento de pontos de halftone deslocado do contorno. O vocabulário de desenho é deliberadamente geométrico (caixas, setas, fluxos, gráficos, terminais). Assunto figurativo está fora do alcance dessa técnica e pertence a `design/art/`, como arquivo escaneado de verdade.

As duas skills de carrossel continuam funcionando, com assets próprios, que moram ao lado delas e não em `design/`:

- `build-thread-carousel` usa arquétipos em `.claude/skills/build-thread-carousel/assets/` (`hook-display`, `body-paragraph` e `_carousel.css`, nos modes `default` e `x`). O CSS é autocontido: valores inline, sem import externo. Nome, handle e avatar são placeholders: pergunte ao usuário antes de renderizar.
- `carousel` mantém o padrão de craft em `.claude/skills/carousel/assets/carousel-craft.md`: slots de identidade, cinco princípios extraídos por engenharia reversa de `examples/carousels/`, contrato de frame, escala tipográfica e checklist de pré-publicação. Ele cobre copy e design juntos e sobrevive a uma troca de identidade: o sistema visual encaixa na tabela de slots (`GROUND / INK / ACCENT / DISPLAY / BODY / MARK / ART / TEXTURE`) em vez de ser escrito no doc. **`design/identity.md` preenche esses slots. É isso que liga a identidade à produção.**

Crítica de tom e vocabulário continua passando pela skill `writing-feedback`.

## Template de print do Twitter (legado)

`templates/twitter-print/` renderiza os tweets de uma thread como PNGs com cara de clone do Twitter (avatar redondo, handle, data). **Não é o caminho padrão para carrossel de Instagram**: `build-thread-carousel` usa um pipeline editorial (arquétipos mais um renderizador HTML genérico). O template fica disponível para o caso ocasional em que o registro de clone do Twitter é exatamente o que você quer.

Para usar na mão:

```bash
python -m http.server 8000   # de dentro de templates/twitter-print/
```

Abra `http://localhost:8000` no **Chrome ou no Edge** (Firefox e Safari não suportam o seletor de diretório que a API exige). Abrir `index.html` direto por `file://` faz o botão "Export PNG" falhar, e isso é de propósito, não é bug para consertar.

## Scripts de automação

Algumas skills delegam trabalho mecânico (render, parsing, export) a scripts Python em `scripts/`. As dependências moram no `pyproject.toml` da raiz e são gerenciadas com **uv**.

Setup inicial por máquina:

```bash
uv sync
uv run playwright install chromium   # só se o script precisar de navegador
```

Para rodar um script: `uv run python scripts/<name>.py [args]`. As skills que dependem dessas rotinas chamam o script via Bash, então não tem comando para decorar: siga a skill que invoca.

Scripts atuais:

| Script | Invocado por | O que faz |
|---|---|---|
| `scripts/render_html_to_pngs.py` | `build-thread-carousel` (e qualquer skill futura que precise de HTML→PNG) | Renderizador genérico: recebe `--html` e `--selector` e tira screenshot de cada elemento que bate com o seletor via Playwright headless. Não sabe nada sobre tipo de conteúdo. Saída em `device_scale_factor=3` por padrão. |

Para adicionar um script novo: declare a dependência no `pyproject.toml`, rode `uv sync` e referencie a partir de `scripts/`. Se a skill que invoca o script é uma rotina de produção, documente aqui também.

## Notas de plataforma

- Windows com shell bash. Use `/dev/null` e barras normais, mas caminho absoluto precisa da letra do drive do Windows (`C:/Users/Pedro Miyasaki/...`).
- Este é um repositório pessoal, só local, sem remote e sem colaboradores. Mensagem de commit pode ser curta e simples: uma linha resumindo o que mudou e por quê basta, sem formato de conventional commit, sem seções de corpo, sem detalhe de PR.
- As instruções de usuário em `~/.claude/CLAUDE.md` (Karpathy guidelines) valem aqui: simplicidade primeiro, mudanças cirúrgicas, expor tradeoffs, definir critérios de sucesso verificáveis.
