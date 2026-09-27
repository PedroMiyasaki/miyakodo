# assets/ — arquétipos do carrossel de IG derivado de thread (skill build-thread-carousel)

Pasta de referência executável dos arquétipos do carrossel de Instagram **derivado de uma thread** (skill `build-thread-carousel`). Cada arquétipo é um arquivo HTML completo e independente: abra no navegador e ele renderiza um slide de demonstração com placeholders.

A skill tem dois modos, cada um com sua subpasta de arquétipos, com a mesma estrutura de arquivos (`_carousel.css`, `hook-display.html`, `body-paragraph.html`) e conteúdo diferente:

- **`default/`**: o modo padrão. Layout X-cosplay em paleta clara e neutra. Documentado abaixo.
- **`x/`**: o modo X. Dark mode, clone fiel do Twitter/X (herdado da skill aposentada `gerar-prints-reel`, usada historicamente para gerar imagem de fundo de Reel).

Qual usar em cada caso está no `SKILL.md` da skill, seção "Modos".

**Placeholders de identidade:** os arquétipos carregam `{{NAME}}`, `{{HANDLE}}` e `{{AVATAR_URL}}` no cabeçalho (e `{{IMAGE_URL}}` no slot de mídia de exemplo). A identidade da marca pessoal ainda não foi definida, então a skill **pergunta ao usuário** o nome, o handle e o caminho do avatar antes de gerar o HTML.

## Layout X-cosplay, paleta clara (modo default)

Estes arquétipos usam o **layout X-cosplay editorial** (referência: Adriano Couto / "Gestão com IA"), em paleta clara e neutra:

- Cabeçalho compacto do X (avatar circular + nome em negrito + selo azul `#1d9bf0` de verificado + handle). **É o layout, não a cor, que faz parecer um tweet**
- Fundo neutro `oklch(0.96 0 0)` (off-white sem tom quente)
- Texto em preto puro `oklch(0 0 0)`, cinzas neutros (chroma 0)
- Inter no body (via `@import` do Google Fonts), JetBrains Mono em `code`, com fallback para as fontes do sistema
- Acento vermelho-tijolo `--seal` nos links, no chip de `code` e na borda da citação
- Conteúdo centralizado na vertical no slide: pouco texto flutua no meio com bastante ar, muito texto ocupa mais

O **único traço nativo do X que ficou** é o azul `#1d9bf0` do selo de verificado: um check recolorido pareceria selo falso. O stylesheet é autossuficiente: todos os valores estão inline nele. Não generalize estes arquétipos para outros contextos.

## O sistema (dentro de cada subpasta)

- **`_carousel.css`**: o chrome compartilhado. Dimensões 1080×1350, `.slide` como coluna flex centralizada, `.profile-row`, `.tweet-text` com render de markdown inline, slot opcional `.tweet-media`. Mudou aqui, mudou em todo carrossel daquele modo.
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

Exemplo de bom uso da seta (slide 6 do Adriano):
```
A regra é simples e vale para qualquer IA do mercado:

→ Suas bases de conhecimento ficam num lugar que é seu.

→ As instruções dos seus agentes estão documentadas num arquivo.

→ A IA é só o motor que roda em cima disso.
```

## Slot de imagem (`.tweet-media`)

Slot opcional embaixo do texto. Quando presente, preenche espaço em slide curto. Cantos arredondados de 18px, altura fixa de 360px, `object-fit: cover` cuida do corte.

**Quando um slide ganha imagem** (detalhe em `.claude/skills/build-thread-carousel/SKILL.md` § "Busca proativa de imagem"). Três regras, em ordem:

1. **Imagem manual sempre ganha.** Se `posts/thread/<slug>/sketch/images/0N.<ext>` (ou `N.<ext>` sem zero) existe para o slide N, ela é usada, sem exceção: a heurística nem roda.
2. **T1 sempre tem imagem**, manual ou buscada, mas nunca ausente. É o que para o scroll.
3. **T2+ sem imagem manual:** heurística. `body < 250 caracteres sem setas` = busca. Senão, só texto.

Quando a skill sai para buscar, o Claude:
   - Deriva uma query semântica do conteúdo **daquele tweet específico**, não do tema geral da thread (em inglês, que funciona melhor em banco de imagens)
   - `WebSearch` com `<query> unsplash photo` ou `<query> stock free`
   - `WebFetch` na página candidata para extrair a URL direta da imagem
   - `bash curl -L -o posts/thread/<slug>/sketch/images/0N.<ext> <url>` para baixar
   - `Read` na imagem baixada (o Claude é multimodal) para julgar se ela bate com o texto **daquele slide**, e não só com o tema da thread. Imagem que ilustra o assunto geral mas briga com o slide é descartada.
   - Se funciona, inclui no HTML. Se não, tenta a próxima candidata ou pula (T1 nunca pula)

As imagens ficam em `posts/thread/<slug>/sketch/images/0N.<ext>`: material de trabalho, ao lado da reescrita do carrossel (`sketch/carousel-v<N>.md`) e da composição (`sketch/carousel.html`) que elas alimentam. Ao re-renderizar, a skill confere se a imagem do slide já existe antes de buscar. Se existe, reaproveita.

## Identidade do cabeçalho (X-cosplay)

Nenhuma identidade está fixa: os três campos são placeholders, preenchidos com o que o usuário informar.

- Avatar: `{{AVATAR_URL}}`, caminho do arquivo, relativo ao `carousel.html` gerado
- Nome de exibição: `{{NAME}}`
- Handle / segunda linha: `{{HANDLE}}`
- Selo de verificado: SVG inline no estilo do X (azul `#1d9bf0`). É layout, não identidade, e fica fixo

## Limites do sistema

- Tudo é otimizado para **1080×1350**. Outras dimensões exigem revisar a escala tipográfica.
- Cor de fundo: off-white neutro fixo no modo default, quase preto (`oklch(0.06)`) no modo X. Não é configurável por slide dentro do mesmo modo.
- Imagens em `.tweet-media`: proporção 3:1 (1080×360 visualmente). Imagem mais alta ou mais baixa é cortada pelo `object-fit`. Escolher imagens razoáveis é responsabilidade da skill.
- `--seal` (o acento vermelho-tijolo) aparece nos links, no chip de code e na borda da citação. O único azul do X que sobrou é o do selo de verificado.
