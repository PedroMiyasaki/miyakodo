# Identidade visual — Alvinegro

O sistema visual de todo entregável que tem layout próprio. Preenche os slots de identidade que o
craft doc do carrossel (`.claude/skills/carousel/assets/carousel-craft.md`, §0) exige.

Prova do sistema renderizada: `design/proof/` (HTML + PNGs). Copie o `<style>` e o `<defs>` de lá
como ponto de partida de qualquer peça nova.

---

## Os slots

| Slot | Valor |
|---|---|
| `GROUND` | `#FFFFFF`, papel. Slides invertidos: `#0A0A0A`. |
| `INK` | `#0A0A0A` sobre papel, `#FFFFFF` nos invertidos. |
| `ACCENT` | **Nenhum: a inversão é o acento.** Veja abaixo. |
| `DISPLAY` | Bricolage Grotesque 800 · `letter-spacing:-.025em` · `line-height:.94` |
| `BODY` | Inter 400/500 |
| `READ` | **Newsreader 400 + itálico**: só em modo leitura, só sobre fundo branco. Veja abaixo. |
| `MARK` | **`@pedro.miyasaki.ia`**: Inter 500, 22px, caixa alta, `letter-spacing:.18em`, `opacity:.55`, canto superior esquerdo, em todo slide. Esse é o handle de verdade, nunca renderize um placeholder. |
| `ART` | Linha com wobble de mão + preenchimento em halftone. A técnica está abaixo. |
| `TEXTURE` | Grão de papel: `radial-gradient(currentColor .5px, transparent .6px)`, grade de `4px`, `opacity:.05` |

Duas famílias, dois valores, nenhum terceiro de nada. Estritamente preto e branco: a retícula de
halftone é o que produz todo tom intermediário, igual à impressão de jornal.

**A inversão é o único acento, e significa uma coisa só: a moldura da peça.** A capa e o CTA são
pretos, tudo entre os dois é branco. Nada mais inverte. Isso cumpre a regra do craft doc de "um
acento, um significado constante" sem gastar cor, e faz da capa um retângulo preto num feed de
retângulos brancos.

**Escala tipográfica** (canvas de 1080×1350, margem de 88px):

| Nível | Tamanho |
|---|---|
| Hook da capa | 104px |
| Headline do slide | 86px |
| CTA | 118px, centralizado |
| Body | 46px / 1.32, máx. 30ch |
| Marca | 22px |

---

## Tipografia — três vozes

| Voz | Fonte | Função |
|---|---|---|
| Reconhecimento | Bricolage Grotesque 800 | Hooks, headlines, o logotipo. Nunca abaixo de 40px. |
| Apoio | Inter 400/500 | Body embaixo de headline, a marca do handle, rótulos, legendas. |
| Leitura | Newsreader 400 + itálico | Qualquer coisa acima de quatro linhas. **Só sobre fundo branco.** |

A Newsreader tem eixo de tamanho óptico, então ela é composta para o tamanho em que vai aparecer, e
não escalada até ele: o mesmo argumento das faixas de rugosidade. Sobre fundo preto ela fica fina e
suja em qualquer tamanho, e é por isso que o modo leitura é só em branco, não por preferência.

Escala no canvas de 1080 × 1350 com margem de 88px: hook da capa 104 · headline do slide 86 · CTA
118 centralizado · body Inter 46/1.32 a 30ch · **leitura Newsreader 40/1.42 a 38ch** · chapéu e
marca do handle 22 a `.18em`.

**Dois tamanhos por slide, nunca três.** Se um slide parece precisar de um terceiro nível, ele é
dois slides.

---

## Cor — a rampa de halftone

Cinza é retícula, nunca cor chapada. São quatro densidades na mesma grade de 11px: escolha uma, não
interpole, e nunca use `opacity` nem um cinza em hex para chegar lá.

| Nome | Raio | Cobertura | Uso |
|---|---|---|---|
| Sussurro | 1.4 | 5.6% | Grão sobre fundo em sangria |
| Retícula | 2.1 | 11.4% | O padrão: preenchimento da arte |
| Sombra | 3.0 | 23.3% | Peso dentro de um desenho |
| Quase chapado | 3.9 | 39.4% | Parece escuro, mas ainda é ponto |
| Tinta | — | 100% | Chapado. Sem retícula. |

Sobre fundo preto o ponto inverte para branco: mesmos raios, mesma grade. **Nunca coloque retícula
sobre retícula:** duas grades sobrepostas geram moiré na exportação, e o artefato sobrevive à
compressão melhor que a arte.

`#0A0A0A` em vez de `#000000` porque o preto puro borra em tela OLED durante o scroll e cria banding
no H.264. O contraste contra o papel é de 19.8:1. Use o mesmo `#0A0A0A` como fundo de Reel, e deixe
o grão de papel ligado nos frames exportados: ele também funciona como dither.

---

## Padrões — seis recursos

O filtro e a retícula são técnica. Estes são os elementos que você coloca na página:

1. **Campo**: a retícula em sangria, cobrindo o slide inteiro.
2. **Par de fios**: grosso sobre fino, vindo do masthead. Todo divisor do sistema.
3. **Contagem**: tracinhos de contar, para qualquer coisa medida em semanas ou repetições.
4. **Grão**: radial de 4px a `.05` em `currentColor`, para sobreviver à inversão. Sempre ligado.
5. **Faixa rasgada**: um retângulo passado pelo `#rough-lg`. Quebras de seção e citações em destaque.
6. **Rótulo em bloco**: o bloco do logotipo em escala de rótulo. Só para chapéus e tags.

Seis é o vocabulário inteiro. Um sétimo é uma decisão sobre o sistema, então ou entra neste arquivo
ou não é usado. Nenhum deles pode ficar em cima de retícula.

---

## Templates e papelaria

| O quê | Fonte | Renderizar com |
|---|---|---|
| Oito arquétipos de slide | `design/templates/slides.html` | `--selector .slide --width 1080 --height 1350` |
| Cartão de visita, duas faces | `design/stationery/stationery.html` | `--selector .card --width 1050 --height 600` |
| Papel timbrado, A4 | `design/stationery/stationery.html` | `--selector .letter --width 1240 --height 1800` |
| O brand book | `design/brandbook/book.html` | `--selector .page --width 1600 --height 880` |

Arquétipos: **cover · statement · quote · data · list · split · reading · CTA**. A marca do handle
está em todos eles, o logotipo em nenhum. Use *quote* quando a frase é o ponto inteiro, *data*
quando um número convence (nunca dois), *list* para o que o leitor vai printar (no máximo cinco
itens), *split* quando a inversão carrega a virada, *reading* quando o argumento passa de quatro
linhas.

A papelaria é **só digital**: sem sangria, sem marcas de corte, sem margem de refile. A frente do
cartão leva o stamp, o verso leva o badge: duas superfícies, nunca no mesmo campo de visão. Os dados
de contato são slots de propósito.

---

## O logotipo

`design/logotype/`: `spec.html` é a fonte, `spec-render/` são as quatro páginas renderizadas.

**A marca é o nome vazado de um bloco entintado.** Bloco e letras são desgastados como uma impressão
só, então a borda fica mordida enquanto as contraformas continuam abertas. Não é um wordmark
colocado dentro de um retângulo.

| Peça | O que é | Onde entra |
|---|---|---|
| **Stamp** | `PEDRO MIYASAKI` vazado do bloco entintado | Papel timbrado, cartão, capa de deck, assinatura |
| **Badge** | O mesmo bloco reduzido a `PM` | Avatar, favicon, marca de canto no vídeo |
| **Masthead** | Nome entre dois fios, slot de descritor embaixo | Cabeçalho de página, Substack, banner do LinkedIn |

```
Padding do bloco    .30em em cima · .38em nos lados · .34em embaixo
Wordmark            Bricolage Grotesque 800, caixa alta, -.03em
Área de proteção    .30em de cada lado, em em do wordmark
Mínimo              stamp 96px de largura · badge 24px
```

**A rugosidade depende do tamanho.** O deslocamento é em pixels absolutos, então um filtro só não
serve para todo tamanho: `scale="7"` parece tinta a 900px e lama a 120px.

| Largura da marca | Filtro | scale | baseFrequency |
|---|---|---|---|
| ≥ 600px | `#rough-lg` | 7 | .018 |
| 300–600px | `#rough-md` | 4 | .026 |
| 120–300px | `#rough-sm` | 2 | .042 |
| < 120px | nenhum | — | — |

A impressão é **fixada no tamanho de render**. Nunca redimensione um PNG exportado da marca:
renderize de novo no tamanho de destino para a faixa ficar certa.

**O masthead é composto, nunca filtrado.** Os fios e o descritor são medidos em em, a partir do wordmark:
fio de cima `.048em`, fio de baixo `.014em`, descritor `.115em` com tracking de `.34em`. Abaixo de um
wordmark de 96px o descritor some, porque renderizaria com menos de 11px.

**Cinco jeitos de quebrar a marca:** esticar (cisalha o grão), recompor em Inter, filtrar duas vezes
(fecha as contraformas), colocar sobre meio-tom, e usar badge e stamp no mesmo campo de visão,
porque os dois são uma marca só em duas altitudes.

**O logotipo não é a marca do slide.** Os slides de carrossel usam o slot `MARK` lá de cima: o handle
em Inter, no canto superior esquerdo, discreto. O stamp é peça de marca para papelaria e cabeçalho,
e nunca aparece em slide de carrossel, onde ia brigar com a headline em display.

---

## Como os desenhos são feitos

Sem plugin, sem geração de imagem, sem stock. Geometria SVG limpa, rasgada por um filtro de
deslocamento na hora do render. O Chromium do Playwright aplica o filtro, então ele chega ao PNG.

```html
<filter id="rough" x="-25%" y="-25%" width="150%" height="150%">
  <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="3" seed="11" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="rough2" x="-25%" y="-25%" width="150%" height="150%">
  <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="3" seed="4" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="6" xChannelSelector="R" yChannelSelector="G"/>
</filter>

<pattern id="ht-dark" width="11" height="11" patternUnits="userSpaceOnUse">
  <circle cx="5.5" cy="5.5" r="2.1" fill="#0A0A0A"/>
</pattern>
<pattern id="ht-light" width="11" height="11" patternUnits="userSpaceOnUse">
  <circle cx="5.5" cy="5.5" r="2.1" fill="#FFFFFF"/>
</pattern>
```

**A construção, sempre a mesma:**

1. Desenhe a forma duas vezes: uma como sólido preenchido com halftone, outra como contorno traçado.
2. O preenchimento fica **deslocado 8–9px** do contorno (`transform="translate(-9,7)"`). Esse
   desregistro é o truque inteiro: parece uma impressão em duas passadas que não bateram.
3. O preenchimento recebe `#rough2`, o contorno recebe `#rough`: seeds diferentes, para as duas
   passadas tremerem de forma independente, como duas passadas de mão separadas.
4. Traço: `stroke-width:7`, `stroke-linecap:round`, `stroke-linejoin:round`. Nunca mais fino, porque
   o filtro come traço fino.
5. A arte ocupa os ~40% de baixo do slide, com 600–900px de largura. Arte pequena demais parece
   espaço morto: a correção é sempre escala.

**Desenhe só o que sobrevive ao tratamento.** O vocabulário é geométrico e diagramático: caixas,
janelas, terminais, setas, fluxos, barras, gráficos, checkmarks, cruzes, cursores, nós, balões de
fala, pilhas, sliders. Isso cobre o assunto inteiro de IA para quem constrói.

**Não** tente tema figurativo: rosto, animal, mão, objeto de contorno orgânico. Geometria limpa mais
filtro de wobble parece desenho de autor. Uma maçã gerada parece clipart com tremor. Se uma peça
precisa mesmo de um desenho figurativo, desenhe à mão, escaneie e coloque em `design/art/`: o
sistema aceita um `<img>` de verdade ali.

---

## Por que isso não é o visual da Anthropic

O screenshot que deu origem a isso usa a mesma *estrutura*: contorno irregular feito à mão mais
preenchimento chapado com um leve desregistro. Essa estrutura é um idioma de impressão, não um ativo
proprietário, e é a mesma ideia que o `habitosqueabracam` usa com ukiyo-e em `examples/carousels/`.

Toda escolha de material por baixo dela é diferente:

| | Anthropic | Alvinegro |
|---|---|---|
| Fundo | creme quente | branco puro, e preto metade do tempo |
| Preenchimento | cinza quente chapado | retícula de halftone, preto ou branco puro |
| Tipografia | serifa suave | grotesque pesada |
| Registro | suave, editorial | alto contraste, cartaz |
| Acento | uma cor (coral) | inversão |

Tipografia suave + desenho suave lê como o registro da Anthropic. Desenho tosco contra uma grotesque dura
e pesada é outra tensão, e é o que faz `souantisocialmedia` e `okaashish` parecerem de autor, e não
de template.

---

## Pendências

- **Biblioteca de arte figurativa.** `design/art/` ainda não existe. Crie quando uma peça precisar de
  um tema desenhado que o vocabulário geométrico não aguenta.
- ~~**Modo leitura.**~~ Fechado em 2026-08-20: Newsreader, só sobre fundo branco. Veja Tipografia
  acima.
- ~~**Brand book.**~~ Fechado em 2026-08-20: 17 páginas em `design/brandbook/`. Rota do logotipo
  decidida: stamp como marca, masthead como estrutura de cabeçalho.
- **Referência de tom visual.** A página de tom do book (13) descreve o registro em palavras. Um
  painel de referência de verdade (jornal escaneado, broadsheet real) ia fixar isso melhor que
  adjetivos.
