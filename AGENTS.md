# AGENTS.md

Este arquivo orienta agentes de código (Codex, Claude Code, Cursor, etc.) neste repositório.

## Links locais: onde editar

Há **uma cópia** no disco; os outros caminhos são espelhos para cada ferramenta achar o que espera:

| Caminho | Papel |
|---|---|
| `AGENTS.md` | **Canônico.** Instruções do repo - edite sempre aqui. |
| `CLAUDE.md` | Link local → `AGENTS.md` (não versionado). |
| `.agents/skills/` | **Única** árvore de skills no git. |
| `.claude/skills/`, `.cursor/skills/` | Links locais → `.agents/skills/` (não versionados). |

**Skills:** quando o usuário pedir criar, mudar ou refinar uma skill (`SKILL.md`, `assets/`, exemplos, scripts da skill), o trabalho é **sempre** em `.agents/skills/<nome-da-skill>/`. Não duplique em `.claude/skills` nem `.cursor/skills`. Se o arquivo apareceu aberto via `.claude/...` ou `.cursor/...`, é o **mesmo** arquivo - use o path `.agents/skills/...` ao salvar e no commit.

**Setup após clone:** `scripts/link-skills.cmd` (Windows) ou `scripts/link-skills.sh` (macOS/Linux) recria os links de skills e `CLAUDE.md`.

## O que é este repositório

Este repositório guarda a produção de conteúdo do usuário: roteiros de Reel, threads, carrosséis e posts de LinkedIn. Não é um projeto de software. Tudo que parece "código" aqui é conteúdo. A produção roda por skills mais o MCP do Notion.

Na prática, isso quer dizer que não existe build, não existe suíte de testes e não existe linter. O que sai daqui é texto e imagem, não software.

**Estado atual: o repositório está em transição.** A marca antiga foi removida (documentos de estratégia, sistema visual e logos foram embora) e a direção nova, uma marca pessoal, ainda está sendo montada.

Já reconstruído: o sistema visual (`design/identity.md`). Ausência deliberada, não pendência: não existe documento de audiência, de pilares de conteúdo nem de voz. Se uma peça precisa de um leitor-alvo ou de um ângulo, pergunte ao usuário.

**Idioma.** O repositório trabalha em português do Brasil: skills, docs, este arquivo e a conversa. As peças publicadas (roteiro, carrossel, thread, post de LinkedIn, artigo de Substack) saem em português do Brasil. O schema do Notion (nomes de propriedades e valores) fica em inglês: o banco de ideias é um só.

## Como o trabalho flui aqui

A razão de ser deste repositório é produzir conteúdo bom com pouco atrito. Quando o usuário pede um post, um roteiro, uma thread, um carrossel ou a captura de uma ideia, invoque a skill correspondente e entregue o melhor rascunho possível, em vez de forçar o pedido por um processo rígido.

O fluxo é direto, sem etapa de brief no meio: a ideia é capturada no banco **Ideas** → uma skill de conteúdo (`write-script`, `carousel`, `write-thread`, `build-linkedin`, `write-substack`) lê a ideia e refina a peça localmente em `posts/<type>/<slug>/sketch/` por quantas iterações forem necessárias → quando o usuário confirma "pronto", a versão aprovada é publicada na raiz do slug. Peças de texto viram `final.md`; o carrossel publica os PNGs aprovados. Não existe banco intermediário de publicação: a peça mora localmente, e a única escrita de volta no Notion acontece no "pronto" (`Status` → `Processed`, mais o `Format` que foi produzido).

Toda skill de produção de conteúdo carrega o mesmo passo de fechamento padronizado: **registrar `Status` → `Processed` e o `Format` da peça** no "pronto". São esses dois campos que acumulam a foto real do calendário no banco: normalmente uma ideia nasce sem formato, e o formato é decidido durante a produção. **Exceção na captura:** links de Reels do Instagram entram como `Pending`, com `Format` → `Reel` e canal Instagram (na propriedade de canal existente ou em `Notes`), conforme `registrar-ideia`. O fechamento da produção continua obrigatório. Essa lista de skills não é fechada: ao criar uma skill de produção nova, copie o passo de fechamento de uma existente.

**`write-substack` é a única exceção documentada, e só no caminho de reuso.** O artigo reescreve uma tese cuja ideia já foi fechada pelo Reel, e uma ideia carrega um único `Format`. Escrever `Substack` por cima apagaria o formato primário e corromperia a foto do calendário que o banco acumula, então o caminho de reuso não escreve nada no Notion. Rodando sozinha numa ideia `Pending` nova, a skill fecha a ideia normalmente com `Format` → `Substack`. Não "conserte" o caminho de reuso para ficar igual às outras skills.

**`carousel` é a exceção à divisão escrever-depois-montar.** Copy e composição nascem juntas no HTML e a primeira versão apresentada já é renderizada. Cada rodada ocupa uma pasta `sketch/v<N>/` completa. Threads mantêm a divisão (`write-thread` → `build-thread-carousel`), porque uma thread sai como texto e o carrossel é um derivado opcional.

As skills são invocadas por comandos naturais em português (por exemplo "escreve o roteiro da última ideia", "faz um carrossel", "escreve um post pro LinkedIn"), **não** por slash commands. Leia `.agents/skills/<skill-name>/SKILL.md` (ver **Links locais** acima). Claude Code pode invocar pela ferramenta Skill.

## Voz

Deliberadamente **não existe documento de voz, de audiência nem de pilares de conteúdo**. Os três foram cortados para simplificar o processo e devolver heurística aos agentes: escreva como o usuário fala e pensa, sem tentar encaixar a peça num molde. Se uma peça precisa de um leitor-alvo ou de um ângulo, pergunte ao usuário. Não reconstrua um perfil de audiência a partir de conteúdo antigo.

## MCP do Notion: IDs críticos

O banco de ideias é o único objeto canônico no Notion. Trate o ID como canônico:

| Objeto | ID |
|---|---|
| **Ideas** (data source) | `e2970ca3-7724-4a81-8f12-7ea34c048c67` |

O schema dele está em inglês: propriedades `Idea`, `Notes`, `Date`, `Status`, `Format`, `ACP Phase`. Valores de Status: `Pending` / `Processing` / `Processed` / `Discarded`. Valores de Format: `Reel` / `IG Carousel` / `Thread` / `LinkedIn Post`, mais `Substack`, **ainda não criado** (veja abaixo). Valores de ACP Phase: `A · Audience` / `C · Community` / `P · Product`.

A propriedade `Pillar` foi apagada junto com o documento de pilares de conteúdo. Não recrie.

O Notion tem dois papéis. É a **fonte de leitura** das skills de produção (`write-script`, `carousel`, `write-thread`, `build-linkedin`, `write-substack`): elas leem a ideia daqui, salvam o conteúdo localmente em `posts/`, e a única escrita de volta é marcar `Status` como `Processed` e registrar o `Format` no fim (o conteúdo em si nunca sobe). E é o **alvo de escrita** da captura de ideias (`registrar-ideia`, `brainstorm-ideas`, `content-research`), que registram ideias novas no banco. Leituras (`notion-search`, `notion-fetch`) são pré-aprovadas. Escrever no banco de ideias (`create-database-row`) pede confirmação, e isso é de propósito, não é configuração errada.

**Cuidado ao mudar o schema:** renomear as opções de uma propriedade select pelo MCP substitui o conjunto de opções inteiro e apaga em silêncio o valor guardado em toda linha. Tire um snapshot das linhas antes e restaure depois da mudança.

É por isso que a opção `Substack` em `Format` é adicionada **na mão, pela interface do Notion**: um clique, risco zero. Até 2026-09-05 ela não tinha sido adicionada. `write-substack` só precisa dela no caminho standalone. Se a opção não existir ali, a skill para e pergunta, em vez de criar pelo MCP.

## Convenção de rascunho local

As skills textuais de produção (script, thread, linkedin, substack) seguem um protocolo estrito de rascunho:

1. Slug = título → minúsculas, sem acento, hífen no lugar de espaço e pontuação.
2. O primeiro rascunho é salvo em `posts/<type>/<slug>/sketch/v1.md` no momento em que é apresentado, onde `<type>` é `script`, `thread`, `linkedin` ou `substack`, conforme a skill que produziu.
3. Toda correção do usuário cria `posts/<type>/<slug>/sketch/v(N+1).md` na mesma pasta. Leia v(N), copie os blocos que não mudaram **verbatim** e aplique só o diff. Nunca regenere conteúdo que não mudou.
4. Quando o usuário confirma "pronto" explicitamente, o `sketch/v<N>.md` de número mais alto é copiado para `posts/<type>/<slug>/final.md`. Essa cópia é a peça publicável, e o histórico `sketch/v<N>` fica onde está como trilha de auditoria. A skill então atualiza a ideia de origem no Notion (`Status` → `Processed` e o `Format` da peça, e nada do conteúdo sobe).

Esse versionamento é deliberado: os arquivos locais são a trilha de auditoria e a fonte única da peça. A publicação é manual, feita pelo usuário na plataforma de destino a partir do arquivo final.

**Exceção visual:** `carousel` não cria rascunho de copy em Markdown. Cada iteração fica em `posts/carousel/<slug>/sketch/v<N>/`, com `carousel.html` e todos os PNGs daquela versão. No "pronto", apenas os PNGs aprovados são copiados para a raiz do slug; não existe `final.md`.

**Tudo de uma peça mora em `posts/<type>/<slug>/`, assets visuais incluídos.** `sketch/` guarda o material de trabalho e a raiz do slug guarda só o que é publicado:

| Tipo | Raiz do slug | `sketch/` |
|---|---|---|
| `script` | `final.md`, `reels.mp4`, `caption.md`, `cover.png` | `v<N>.md`, `cover.html` |
| `carousel` | PNGs da versão aprovada | `v<N>/carousel.html` + PNGs da versão |
| `thread` | `final.md` (o texto da thread), `01.png` … `10.png` quando `build-thread-carousel` roda | `v<N>.md`, `carousel-v<N>.md` (a reescrita da copy para slide), `carousel.html`, `images/` |
| `linkedin` | `final.md`, `image.png` (URL de origem registrada no rodapé do `final.md`) | `v<N>.md` |
| `substack` | `final.md` (título + subtítulo + artigo com marcadores de imagem inline + rodapé de metadados), `cover.png`, `01.png` … `NN.png` | `v<N>.md`, `shotlist.md` |

Os PNGs publicados ficam soltos na raiz do slug, sem subpasta `render/` nem `editorial/`, e as composições HTML ficam em `sketch/`. `output/` sumiu por completo: toda skill escreve em `posts/<type>/<slug>/`. Um Reel não é um objeto próprio. Ele é a entrega do roteiro, então o vídeo, a legenda do post e a capa caem na pasta do próprio roteiro.

## Vídeo: Reels

Vídeo de Reel é produzido com Hyperframes, pela skill `hyperframes`. No "pronto", as entregas ficam na pasta do roteiro, `posts/script/<slug>/`: `reels.mp4`, `caption.md` e `cover.png`. A capa segue o Alvinegro e o arquétipo `01 COVER`. Os nomes são fixos; o slug identifica a pasta.

## Sistema visual: Alvinegro

`design/identity.md` é o sistema visual de toda entrega com layout próprio: preto e branco estrito, display grotesca pesada, line art com wobble de traço à mão e preenchimento em halftone. `design/proof/` guarda uma prova renderizada de três slides: copie o `<style>` e o `<defs>` dela para começar uma peça nova. **Não improvise paleta nem fonte**, e não traga a marca antiga de volta.

O brand book completo é `design/brandbook/book.html` (17 páginas, renderizadas em `render/`). Ele é o sistema *mostrado*. `identity.md` é o sistema *enunciado*, e o markdown é canônico se os dois algum dia discordarem. Ao lado dele: `design/logotype/` (o stamp mark, o badge e o masthead, mais as rotas que foram exploradas), `design/templates/slides.html` (oito arquétipos de slide) e `design/stationery/stationery.html` (cartão de visita e papel timbrado A4, só digital). Todos renderizam por `scripts/render_html_to_pngs.py`: nada aqui precisa de ferramenta de design.

A arte é gerada, não buscada: geometria SVG limpa rasgada por um filtro `feTurbulence` + `feDisplacementMap` na hora do render, com preenchimento de pontos de halftone deslocado do contorno. O vocabulário de desenho é deliberadamente geométrico (caixas, setas, fluxos, gráficos, terminais). Assunto figurativo está fora do alcance dessa técnica e pertence a `design/art/`, como arquivo escaneado de verdade.

As duas skills de carrossel usam o mesmo sistema visual por caminhos diferentes:

- `build-thread-carousel` usa arquétipos em `.agents/skills/build-thread-carousel/assets/` (`hook-display`, `body-paragraph` e `_carousel.css`, nos modes `default` e `x`). O CSS é autocontido: valores inline, sem import externo. A identidade já está fixa nos arquétipos: Pedro Miyasaki, `@pedro.miyasaki.ia`, sem avatar.
- `carousel` cria cada versão diretamente em HTML a partir de `design/identity.md` e `design/proof/proof.html`, renderiza dentro da própria pasta de versão e itera sobre o resultado visual.

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
- As instruções de usuário em `~/.Codex/AGENTS.md` ou `~/.claude/CLAUDE.md` (Karpathy guidelines) valem aqui: simplicidade primeiro, mudanças cirúrgicas, expor tradeoffs, definir critérios de sucesso verificáveis.
