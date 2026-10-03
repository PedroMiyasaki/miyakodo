---
name: build-thread-carousel
description: >
  Monta um carrossel de Instagram a partir de uma thread já escrita (em
  posts/thread/<slug>/sketch/v<N>.md), gerando um carousel.html em
  posts/thread/<slug>/sketch/ com estética editorial de X-cosplay
  (cabeçalho com avatar + nome + selo azul de verificado, conteúdo
  centralizado na vertical, slot de imagem opcional). Tem dois modos
  visuais: default (claro, paleta neutra) e X (dark mode, clone fiel
  do X, usado também como imagem de fundo de Reel). Nome, handle e
  avatar são placeholders: pergunte ao usuário antes de gerar.
  Renderiza cada slide como PNG via Playwright. Ative com comandos
  como "monta o carrossel da thread <slug>", "renderiza os PNGs de
  <slug>", "monta o carrossel em modo X de <slug>", "gera as stills
  do reel da thread <slug>", "faz as stills de <slug>" ou "usa a
  skill build-thread-carousel no post <slug>".
---

# SKILL · Montar carrossel de thread

**Propósito:** transformar uma thread pronta (texto da `write-thread`) num carrossel de Instagram. Entra texto, sai `carousel.html` + PNGs. É um derivado opcional: o fechamento no Notion já aconteceu na thread — **esta skill não escreve no Notion**.

## Quando ativar

Comandos como "monta o carrossel da thread `<slug>`", "renderiza os PNGs de `<slug>`", "monta o carrossel em modo X de `<slug>`" (e os legados "gera as stills do reel", "faz as stills de `<slug>`", que também ativam o modo X).

Não ative se a thread ainda não existe em `posts/thread/<slug>/sketch/v<N>.md` — aponte o usuário para a `write-thread`.

## Entrada e saída

Tudo mora em `posts/thread/<slug>/`, mesma convenção nos dois modos:

| Arquivo | Papel |
|---|---|
| `sketch/v<N>.md` (entrada) | Thread original, já escrita — só leitura |
| `sketch/carousel-v<N>.md` | Reescrita da copy para slides (sequência paralela à da thread: nunca crie um `v<N+1>.md` para o carrossel) |
| `sketch/carousel.html` | Composição dos slides |
| `sketch/images/` | Imagens manuais (colocadas pelo usuário) ou buscadas pela skill |
| `01.png` … `10.png` (raiz do slug) | PNGs renderizados |

## Modos

| | **default** | **X** |
|---|---|---|
| Quando usar | Carrossel para o feed do IG (padrão) | Stills de fundo para um Reel, ou clone explícito do X/Twitter |
| Paleta | Clara e neutra (off-white, texto preto) | Dark mode do X (fundo quase preto) |
| Arquétipos | `assets/default/` | `assets/x/` |

Qualquer menção a "modo X", "estilo X", "dark mode" ou aos comandos legados de stills ativa o modo X; o resto cai no default. Fora a subpasta de `assets/`, o protocolo é idêntico.

## Protocolo

### 1. Reescrever a copy para slides

Leia a `v<N>.md` mais recente e salve a adaptação em `sketch/carousel-v1.md` (copie o cabeçalho YAML da thread e registre o que mudou). O IG não tem limite de caracteres: pode expandir com conectores ("Pensa comigo:", "Na prática:"), listas e transições que na thread eram implícitas. Mantenha o núcleo do argumento.

Mapeamento: T1 → `slide-hook` (primeiro parágrafo vira headline em negrito de 40px, resto em body de 30px); T2–T(N) → `slide-body` (texto de 30px). Use markdown rico: `**negrito**` numa frase-chave por slide, `*itálico*`, `` `code` `` em termos técnicos, `> citação` para destaque, `→ ` como marcador de lista (ver exemplo em Calibração).

### 2. Resolver as imagens

Para cada slide, em ordem: (a) **imagem manual em `sketch/images/` sempre ganha**, sem exceção — o usuário pôs ali de propósito; (b) **o slide 1 sempre tem imagem** (é o que para o scroll): sem manual, busque; (c) nos demais, busque só para slides curtos que ficariam vazios (heurística: body abaixo de ~250 caracteres sem lista de setas).

Para buscar: derive a query **daquele slide específico** (em inglês), procure foto gratuita (`WebSearch` em Unsplash/Pexels — descarte resultado pago Unsplash+), baixe para `sketch/images/0N.jpg` e **inspecione com `Read`**: a imagem tem que bater com o ponto do slide, não só com o tema da thread. Se não bater, tente outra ou pule o slide (menos no T1, que nunca vai sem imagem — reformule a query ou peça uma manual ao usuário). Prefira Pexels quando o Unsplash devolver muito resultado pago; evite marca d'água e texto sobreposto.

### 3. Montar o HTML e revisar com o usuário

Mostre o mapeamento dos slides + quais ganharam imagem (e de onde) e peça ok antes de gerar. Depois:

- Importe **só** o `_carousel.css` do modo escolhido (`../../../../.agents/skills/build-thread-carousel/assets/<mode>/_carousel.css`) e copie os blocos `.slide-hook` / `.slide-body` dos arquétipos para um `<style>` no `<head>`.
- Cada tweet vira `<section class="slide slide-<archetype>">` com cabeçalho do X completo, `<div class="tweet-text">` (markdown convertido em HTML inline) e `<div class="tweet-media">` só se o slide tem imagem (`images/<arquivo>`, sem `../`).
- Nome, handle e avatar são placeholders (`{{NAME}}`, `{{HANDLE}}`, `{{AVATAR_URL}}`): **pergunte ao usuário antes de gerar** e substitua. Não invente nenhum.
- O usuário revisa abrindo o HTML no navegador. Ajuste de copy → novo `carousel-v<N+1>.md` (blocos intactos copiados verbatim, só o diff) + HTML refeito; ajuste de imagem → trocar o arquivo ou buscar de novo.

### 4. Renderizar

Setup (uma vez por máquina): `uv sync` + `uv run playwright install chromium`.

```bash
uv run python scripts/render_html_to_pngs.py \
  --html "posts/thread/<slug>/sketch/carousel.html" \
  --out "posts/thread/<slug>" \
  --selector ".slide" \
  --width 1080 --height 1350
```

Revise o HTML antes de renderizar: o tamanho é fixo em 1080×1350, o navegador corta a imagem sozinho (`object-fit: cover`, moldura 3:1) e texto longo demais + imagem pode estourar o slide. Ao final, diga quantos PNGs saíram e quais slides têm imagem.

## Restrições

- Não escreva no Notion; não crie arquétipo novo sem aprovação.
- Cada `_carousel.css` é autocontido (cor e tipografia inline, sem stylesheet externo).
- Detalhe dos arquétipos, do slot de imagem e dos placeholders: `assets/README.md`.

## Calibração

Lista com setas (texto literal, quebra de parágrafo entre itens — nunca `*`/`-` do markdown, que renderizam como `<ul>`):

```
A regra é simples e vale para qualquer IA do mercado:

→ Suas bases de conhecimento ficam num lugar que é seu.

→ As instruções dos seus agentes estão documentadas num arquivo.

→ A IA é só o motor que roda em cima disso.
```
