# assets/ - arquétipos do carrossel de IG derivado de thread (skill build-thread-carousel)

Pasta dos arquétipos do carrossel de Instagram **derivado de uma thread** (skill `build-thread-carousel`). Cada arquétipo é um arquivo HTML completo e independente: abra no navegador e ele renderiza um slide de demonstração.

A skill tem dois modos, cada um com sua subpasta de arquétipos, com a mesma estrutura de arquivos (`_carousel.css`, `hook-display.html`, `body-paragraph.html`) e conteúdo diferente:

- **`default/`**: o modo padrão. Layout X-cosplay em paleta clara e neutra. Documentado abaixo.
- **`x/`**: o modo X. Dark mode, clone fiel do Twitter/X (herdado da skill aposentada `gerar-prints-reel`, usada historicamente para gerar imagem de fundo de Reel).

Qual usar em cada caso está no `SKILL.md` da skill, seção "Modos".

## Layout X-cosplay, paleta clara (modo default)

Estes arquétipos usam um **layout X-cosplay editorial** em paleta clara e neutra:

- Cabeçalho compacto com nome, selo azul `#1d9bf0` de verificado e handle
- Fundo neutro `oklch(0.96 0 0)` (off-white sem tom quente)
- Texto em preto puro `oklch(0 0 0)`, cinzas neutros (chroma 0)
- Inter no body (via `@import` do Google Fonts), JetBrains Mono em `code`, com fallback para as fontes do sistema
- Acento vermelho-tijolo `--seal` nos links, no chip de `code` e na borda da citação
- Conteúdo centralizado na vertical no slide: pouco texto flutua no meio com bastante ar, muito texto ocupa mais

O **único traço nativo do X que ficou** é o azul `#1d9bf0` do selo de verificado: um check recolorido pareceria selo falso. O stylesheet é autossuficiente: todos os valores estão inline nele. Não generalize estes arquétipos para outros contextos.

## O sistema (dentro de cada subpasta)

- **`_carousel.css`**: o chrome compartilhado. Dimensões 1080×1350, `.slide` como coluna flex centralizada, `.profile-row`, `.tweet-text` com render de markdown inline e slot opcional `.tweet-media`. Mudou aqui, mudou em todo carrossel daquele modo.
- **`hook-display.html`**: o primeiro slide. O primeiro parágrafo vira uma headline maior em negrito (40px), o resto body regular (30px). Tudo centralizado na vertical.
- **`body-paragraph.html`**: os slides do meio e o último. Tweet-text a 30px com parágrafos. Aceita markdown e marcadores `→ `.

## Qual usar quando

| Posição | Padrão | Quando trocar |
|---|---|---|
| T1 | `hook-display` | Hook curto (até ~250 caracteres). Acima disso vira `body-paragraph`. |
| T2 até T(N) | `body-paragraph` | Sem variantes. Use negrito/itálico/setas de markdown dentro do body para dar ritmo. |

Não tem arquétipo separado para o fechamento: para dar peso à frase de teste do último tweet, envolva ela em `**negrito**` ou `> blockquote` dentro do `body-paragraph`.

## Formatação no .md do carrossel

O .md do carrossel **pode ser mais formatado que a thread original**. Não tem limite de caracteres no IG, então use o espaço:

- `**negrito**` em uma frase-chave por slide
- `*itálico*` em termos destacados
- `` `code` `` em termos técnicos (`RAG`, `eval` etc.)
- `> citação` para destacar uma frase importante
- **`→ ` como marcador de lista inline**: escreva `→ ` no começo de cada item, com quebra de parágrafo entre os itens. Não use `*` nem `-` do markdown (eles renderizam como `<ul>`, que fica visualmente diferente). A seta é texto literal.

## Slot de imagem (`.tweet-media`)

Slot opcional embaixo do texto. Quando presente, preenche espaço em slide curto. Cantos arredondados de 18px, altura fixa de 360px, `object-fit: cover` cuida do corte.

**Quando um slide ganha imagem** (detalhe em `.agents/skills/build-thread-carousel/SKILL.md` § "Busca proativa de imagem"). Três regras, em ordem:

1. **Imagem manual sempre ganha.** Se `posts/thread/<slug>/sketch/images/0N.<ext>` (ou `N.<ext>` sem zero) existe para o slide N, ela é usada, sem exceção: a heurística nem roda.
2. **T1 sempre tem imagem**, manual ou buscada, mas nunca ausente. É o que para o scroll.
3. **T2+ sem imagem manual:** heurística. `body < 250 caracteres sem setas` = busca. Senão, só texto.

Quando a skill sai para buscar, o Claude:
   - Deriva uma query semântica do conteúdo **daquele tweet específico**, não do tema geral da thread (em inglês, que funciona melhor em banco de imagens)
   - `WebSearch` com uma query semântica
   - `WebFetch` na página candidata para extrair a URL direta da imagem
   - `bash curl -L -o posts/thread/<slug>/sketch/images/0N.<ext> <url>` para baixar
   - `Read` na imagem baixada (o Claude é multimodal) para julgar se ela bate com o texto **daquele slide**, e não só com o tema da thread. Imagem que ilustra o assunto geral mas briga com o slide é descartada.
   - Se funciona, inclui no HTML. Se não, tenta a próxima candidata ou pula (T1 nunca pula)

As imagens ficam em `posts/thread/<slug>/sketch/images/0N.<ext>`: material de trabalho, ao lado da reescrita do carrossel (`sketch/carousel-v<N>.md`) e da composição (`sketch/carousel.html`) que elas alimentam. Ao re-renderizar, a skill confere se a imagem do slide já existe antes de buscar. Se existe, reaproveita.
