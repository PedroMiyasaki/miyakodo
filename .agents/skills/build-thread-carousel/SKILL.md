---
name: build-thread-carousel
description: >
  Monta um carrossel de Instagram a partir de uma thread já escrita (em
  posts/thread/<slug>/sketch/v<N>.md), gerando um carousel.html em
  posts/thread/<slug>/sketch/ com estética editorial de X-cosplay
  (cabeçalho com nome + selo azul de verificado, conteúdo
  centralizado na vertical, slot de imagem opcional). Tem dois modos
  visuais: default (claro, paleta neutra) e X (dark mode, clone fiel
  do X, usado também como imagem de fundo de Reel).
  Renderiza cada slide como PNG via Playwright. Ative com comandos
  como "monta o carrossel da thread <slug>", "renderiza os PNGs de
  <slug>", "monta o carrossel em modo X de <slug>", "gera as stills
  do reel da thread <slug>", "faz as stills de <slug>" ou "usa a
  skill build-thread-carousel no post <slug>".
---

# SKILL · Montar carrossel de thread
## Montar carrossel de thread

Objetivo: montar o carrossel de IG a partir de uma thread já escrita. Cada slide reproduz um cabeçalho editorial inspirado no X, com a identidade fixa de Pedro Miyasaki e o conteúdo **centralizado na vertical**. Slot de imagem opcional embaixo do texto, para preencher slides curtos.

A skill tem **dois modos visuais**: mesmo conteúdo, mesma estrutura, arte diferente. Veja a seção "Modos" abaixo para escolher qual usar e como ativar cada um.

---

## Modos

| | **default** | **X** |
|---|---|---|
| Quando usar | Carrossel para o feed do IG | Imagens de fundo para um Reel (uma sequência de stills), ou quando o pedido é explicitamente um clone do X/Twitter |
| Paleta | Clara e neutra: fundo off-white, texto preto puro, acento vermelho-tijolo `--seal` | Dark mode nativo do X: fundo quase preto (`oklch(0.06)`), texto quase branco |
| Arquétipos | `assets/default/` | `assets/x/` |
| Dimensões do slide | 1080×1350 (4:5), iguais nos dois modos | |
| Output | `posts/thread/<slug>/sketch/carousel.html` + `sketch/carousel-v<N>.md` + PNGs soltos em `posts/thread/<slug>/`. **Mesma convenção nos dois modos**, não separe por modo | |

Ativar o modo X: comandos que mencionem "modo X", "estilo X", "dark mode", ou os comandos legados da skill aposentada `gerar-prints-reel` ("gera as stills do reel da thread `<slug>`", "faz as stills de `<slug>`", "usa a skill gerar-prints-reel no post `<slug>`"). Qualquer outro comando ativa o modo default.

O resto deste protocolo é **idêntico nos dois modos**, exceto onde estiver marcado: a única diferença real é qual subpasta de `assets/` importar.

---

## Leitura obrigatória antes de gerar

Os arquétipos ficam em `assets/`, empacotados com esta skill (caminho relativo a este SKILL.md), organizados por modo:

1. `assets/README.md`: documenta a exceção do X-cosplay, os dois modos e quando usar cada arquétipo
2. `assets/<mode>/_carousel.css`: chrome compartilhado do modo escolhido (cabeçalho do X, centralização vertical, slot de mídia, render de markdown)
3. `assets/<mode>/hook-display.html`: arquétipo do primeiro slide, no modo escolhido
4. `assets/<mode>/body-paragraph.html`: arquétipo dos demais slides, no modo escolhido

Onde `<mode>` é `default` ou `x`, conforme a seção "Modos" acima.

Cada `_carousel.css` é autossuficiente: cor e tipografia já estão embutidas nele, não tem stylesheet externo para carregar.

---

## Quando ativar

Comandos como:

- "Usa a skill `build-thread-carousel` no post `<slug>`"
- "Monta o carrossel da thread `<slug>`"
- "Renderiza os PNGs de `<slug>`"
- "Monta o carrossel em modo X de `<slug>`" / "gera as stills do reel da thread `<slug>`" / "faz as stills de `<slug>`" (modo X)

Não ative se a thread ainda não existe em `posts/thread/<slug>/sketch/v<N>.md`. Aponte o usuário para a `write-thread`.

---

## Protocolo

### 1. Identificar o slug

Subpasta em `posts/thread/`. Se estiver ambíguo, confira com Glob `posts/thread/<input>*`.

### 2. Calibração pelo histórico

Antes de adaptar o texto, calibre pelo que foi publicado neste derivado: liste os slugs mais recentes em `posts/thread/` e, de cada um dos últimos 5, leia a copy de carrossel mais recente (o `sketch/carousel-v<N>.md` de maior N) e abra os PNGs finais soltos na raiz do slug. Observe como heurística de leitura, não checklist: registro (falado ou formal, conectores de ritmo, gíria ou não), ritmo (headline curta vs. body, uso de listas de setas), densidade técnica (jargão, números e nomes por slide), hooks e CTAs típicos, pessoa e opinião (quanto de "eu", humor), tamanho médio (nº de slides), formatação (negrito/itálico/code/blockquote) e o que as imagens escolhidas têm em comum. Reescreva imitando o padrão observado, sem copiar frases; se os 5 divergirem, siga o mais recente. Com menos de 5 (ou sem nenhum `carousel-v<N>.md` - `posts/` é gitignored), use o que houver ou siga sem calibrar, avisando ao usuário em uma linha.

### 3. Adaptar o texto para carrossel

O carrossel **pode ser mais formatado e mais longo que a thread original**: o IG não tem limite de caracteres, e os slides ficam melhores com mais espaçamento e estrutura.

- Leia `posts/thread/<slug>/sketch/v<N>.md` (a versão mais recente da thread).
- Salve a reescrita em `posts/thread/<slug>/sketch/carousel-v1.md`. **Não** crie um `v<N+1>.md`: a sequência `v<N>` é a thread (o que vai para o X), e a versão de número mais alto dela tem que continuar sendo a versão mais recente *da thread*, não uma adaptação para carrossel. Então `sketch/` guarda duas sequências paralelas, `v<N>.md` para a thread e `carousel-v<N>.md` para o carrossel, cada uma iterada por conta própria, ao lado do `carousel.html` que vai ser gerado a partir da segunda.
- Na reescrita, mantenha o **núcleo do argumento**. Você pode:
  - Adicionar conectores ("Pensa comigo:", "Dois caminhos:", "Na prática:") que dão ritmo
  - Reformatar como lista de setas `→ ` quando o conteúdo tem itens paralelos
  - Adicionar parágrafos de transição que na thread só existiam implícitos
  - Usar markdown rico:
    - `**negrito**` em uma frase-chave por slide
    - `*itálico*` em um termo destacado
    - `` `code` `` em termos técnicos (`RAG`, `eval` etc.)
    - `> citação` para destacar uma frase importante
    - `→ ` como marcador de lista inline (texto literal, quebra de parágrafo entre itens; **não** use `*` nem `-` do markdown)
- Copie o cabeçalho/metadados YAML da thread para o topo do `carousel-v1.md`. Registre o que mudou da thread `v<N>.md` para esta adaptação.
- Tradeoff: a versão expandida diverge da que vai para o X. Isso é esperado: o .md do carrossel é um entregável próprio.

### 4. Mapear cada tweet para um arquétipo

- T1 → `slide-hook` (o primeiro parágrafo vira uma **headline em negrito de 40px**, o resto em body regular de 30px).
- T2 até T(N) → `slide-body` (texto regular de 30px com markdown).

Não crie arquétipo novo sem aprovação.

### 5. Busca proativa de imagem

Se um slide ganha imagem ou não é decidido por três regras, em ordem de prioridade:

**Regra 1: imagem manual sempre ganha (qualquer slide).**
Para cada slide N, confira se já existe um arquivo de imagem correspondente em `posts/thread/<slug>/sketch/images/`. Aceite as duas formas, com zero à esquerda ou sem (`01.jpg` ou `1.jpg`), em `.png`, `.jpg`, `.jpeg` ou `.webp`. Se existir, **use essa imagem, sem exceção**: não rode a heurística, não busque, não avalie. O usuário colocou ela ali de propósito.

**Regra 2: o slide 1 sempre tem imagem.**
O primeiro slide (T1, o hook) sempre ganha imagem, independente da heurística: é o que faz o carrossel parar o scroll. Se não tem imagem manual para ele (regra 1), busque proativamente. Nunca entregue o T1 sem imagem.

**Regra 3: demais slides, heurística de tamanho.**
Para os slides do T2 em diante sem imagem manual, identifique os curtos que se beneficiariam de uma imagem. Heurística: **body < 250 caracteres sem lista de setas** = candidato, e nesse caso busque proativamente. Slide longo fica só com texto.

**Procedimento de busca proativa** (quando a regra 2 ou a 3 pede busca):

- Derive uma query semântica do conteúdo **daquele slide específico**, não do tema geral da thread (em inglês, que funciona melhor em banco de imagens). Ex.: para "a IA está produzindo profissionais ineficientes", a query seria `frustrated professional computer screen stock photo`.
- Rode `WebSearch` e selecione 2–3 candidatas de fontes confiáveis que permitam reutilização.
- Rode `WebFetch` na página candidata para extrair a URL direta do arquivo de imagem.
- Crie a pasta: `mkdir -p posts/thread/<slug>/sketch/images` (se não existir).
- Baixe via Bash: `curl -L -o "posts/thread/<slug>/sketch/images/0N.jpg" "<direct-url>"` (imagem baixada pela skill é sempre salva com zero à esquerda, `0N.jpg`).
- **Inspecione a imagem com `Read`** (o Claude é multimodal). Julgue com rigor:
  - **A imagem bate com o texto DAQUELE slide específico, e não só com o tema geral da thread?** Imagem que ilustra o assunto geral mas briga com o ponto do slide deve ser descartada.
  - A qualidade está adequada? Está livre de texto sobreposto que ia brigar com o slide?
- Se funciona, mantenha. Senão: para slides T2+, apague e tente a próxima candidata, ou pule o slide (sem imagem é melhor que imagem fora do assunto). **No T1, não pule**: amplie ou reformule a query e busque mais. Se mesmo assim nada funcionar, avise o usuário e peça uma imagem manual.

**Informe ao usuário** quais slides ganharam imagem e de onde (manual ou buscada), antes de gerar o HTML.

Não precisa cortar: o CSS de `.tweet-media` usa `object-fit: cover` com altura fixa de 360px, e o navegador corta sozinho no render do Playwright.

### 6. Apresentar o plano ao usuário

Antes de gerar o HTML, liste para o usuário:
- O mapeamento dos slides (T1 → hook, T2-T(N) → body)
- Quais slides ganharam imagem e a fonte (link da imagem original)
- Ênfases de markdown adicionadas (frases que viraram negrito/itálico)

Peça confirmação ou ajustes.

### 7. Gerar `posts/thread/<slug>/sketch/carousel.html`

Depois da aprovação:

- Importe **só** o `_carousel.css` do modo escolhido via `<link>` (stylesheet autossuficiente). Caminho relativo a `posts/thread/<slug>/sketch/`:
  - `../../../../.agents/skills/build-thread-carousel/assets/<mode>/_carousel.css`
- Inclua um `<style>` no `<head>` copiando, dos arquétipos do modo escolhido, os blocos das classes `.slide-hook` e `.slide-body`.
- Cada tweet vira `<section class="slide slide-<archetype>" data-slide="NN">`, com:
  - o `<header class="profile-row">` dos arquétipos, já com a identidade fixa
  - `<div class="tweet-text">` com o markdown já convertido em HTML inline (`**` → `<strong>`, `*` → `<em>`, `` ` `` → `<code>`, `>` → `<blockquote>`)
  - `<div class="tweet-media"><img src="images/<file>" alt="..."></div>` **só se** o slide tem imagem associada. As imagens ficam em `sketch/images/`, irmã do HTML, então a referência é só a pasta e o nome do arquivo, sem nenhum `../`. `<file>` é o nome real do arquivo: `0N.jpg` quando a skill baixou, ou `0N`/`N` em qualquer extensão (`.png`/`.jpg`/`.jpeg`/`.webp`) se foi imagem manual
- `<body class="carrossel-preview">` para dar um fundo neutro (ou escuro, no modo X) quando abrir no navegador.

### 8. Apresentar o HTML para o usuário revisar

O usuário pode abrir o arquivo direto no navegador (`file://` no Chrome/Edge). Quando pedir ajuste:
- Mudança de copy → crie `posts/thread/<slug>/sketch/carousel-v<N+1>.md` (copie literalmente os blocos que não mudaram do `carousel-v<N>.md`, aplique só o diff) e gere o HTML de novo.
- Mudança de imagem em um slide → troque o arquivo em `posts/thread/<slug>/sketch/images/` ou rode a busca de imagem de novo.
- Mudança visual sistêmica → ajuste o arquétipo em `assets/<mode>/`.

### 9. Renderizar os PNGs

```bash
uv run python scripts/render_html_to_pngs.py \
  --html "posts/thread/<slug>/sketch/carousel.html" \
  --out "posts/thread/<slug>" \
  --selector ".slide" \
  --width 1080 --height 1350
```

PNGs gerados soltos em `posts/thread/<slug>/`, 3240×4050 (device scale 3×). O script numera em sequência, com zero à esquerda até a largura da contagem de slides: carrossel com 10 slides ou mais sai `01.png … 10.png`, com 9 ou menos sai `1.png … 9.png`.

### 10. Relatar

Diga quantos PNGs foram gerados, a pasta de saída, e quais slides ganharam imagem e de onde. Se algum slide ainda mostra muito espaço vazio, sugira ao usuário adicionar uma imagem manual.
