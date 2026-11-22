# assets/ - arquétipos do carrossel de IG derivado de thread (skill build-thread-carousel)

Pasta dos arquétipos do carrossel de Instagram derivado de uma thread (skill `build-thread-carousel`). Cada arquétipo é um arquivo HTML completo e independente: abra no navegador e ele renderiza um slide de demonstração.

A marca visual é a da escola Miyakodo. Antes de produzir, leia `design/identity.md`. Ele é a fonte canônica de cor, tipografia, logo, mascote e textura. Os CSS embutem os valores registrados lá. Se divergir, vale o `identity.md`.

- Logos: `design/logo/`. No modo default, o PNG horizontal dark brown é `design/logo/png/horizontal/MIYAKODO_HORIZONTAL2.png` (`#280e03`). No modo X, o PNG horizontal off-white é `design/logo/png/horizontal/MIYAKODO_HORIZONTAL3.png` (`#f6f4ee`). O número não é a mesma cor no PNG e no PDF. Use a tabela de `identity.md`.
- Fontes: `design/fontes/instrument-serif.zip` (títulos, Instrument Serif, Regular e Italic) e `design/fontes/poppins.zip` (corpo, Poppins). Não copie as fontes para fora de `design/fontes/`.
- Mascote Carlos e textura: `design/mascote-e-textura/`. O índice do PNG não coincide com o do PDF, salvo o corpo agachado. A tabela de expressões está em `identity.md`. Entram na composição quando a peça pedir. Não são cabeçalho obrigatório.
- Guia: `design/apresentacao-idv-pedro-miyakodo.pdf`.

A skill tem dois modos, cada um com sua subpasta de arquétipos, com a mesma estrutura de arquivos (`_carousel.css`, `hook-display.html`, `body-paragraph.html`):

- **`default/`**: carrossel para o feed. Fundo off-white `#f6f4ee`, texto dark brown `#280e03`.
- **`x/`**: variante escura. Fundo dark brown `#280e03`, texto off-white `#f6f4ee`. Também serve de still para Reel. A pasta continua se chamando `x` porque os comandos da skill usam esse nome.

Qual usar em cada caso está no `SKILL.md` da skill, seção "Modos".

## Layout do modo default

O cabeçalho traz o logo Miyakodo, o nome Pedro Miyasaki e o handle `@pedro.miyasaki.ia`, porque a peça sai no perfil do fundador. O conteúdo fica centralizado na vertical.

- Fundo off-white `#f6f4ee`
- Texto dark brown `#280e03`, meta em cinza `#aba199`
- Títulos em Instrument Serif, peso regular (a entrega não tem negrito). Corpo em Poppins
- Acento `#db3c05` (apoio) em link e borda de citação. Chip de `code` em `#b6cadb` (apoio), com texto dark brown
- `code` usa a mono do sistema. `identity.md` não registra uma família mono
- Pouco texto flutua no meio com bastante ar, muito texto ocupa mais

O stylesheet é autossuficiente: os valores usados no chrome estão nele, tirados de `design/identity.md`. O `@import` carrega Instrument Serif e Poppins para o navegador. Os arquivos canônicos continuam nos zips de `design/fontes/`.

## O sistema (dentro de cada subpasta)

- **`_carousel.css`**: o chrome compartilhado. Dimensões 1080×1350, `.slide` como coluna flex centralizada, `.profile-row`, `.tweet-text` com render de markdown inline e slot opcional `.tweet-media`. Mudou aqui, mudou em todo carrossel daquele modo.
- **`hook-display.html`**: o primeiro slide. O primeiro parágrafo vira headline em Instrument Serif, 40px, peso regular. O resto fica em Poppins, 30px. Tudo centralizado na vertical.
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
