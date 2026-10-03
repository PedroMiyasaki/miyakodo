---
name: carousel
description: >
  Produz um carrossel de Instagram completo, de ponta a ponta: lê uma ideia do
  banco Ideas, escreve a copy dos slides e a legenda do post na voz do usuário,
  depois compõe e renderiza a arte dos slides como PNGs 4:5. Ative com comandos
  como "escreve o carrossel da última ideia", "faz um carrossel", "renderiza o
  carrossel <slug>", "redesenha a arte do carrossel", ou quando o feedback é
  sobre espaço vazio, hierarquia fraca ou narrativa nos slides do carrossel.
  Não serve para carrossel de thread em X-cosplay (isso é build-thread-carousel).
---

# SKILL · Carrossel

Transforme uma ideia crua num carrossel pronto: copy **e** arte, numa passada só. Aqui copy e
composição são uma entrega única: a headline é a âncora, o template só trava se a copy tiver uma
forma que se repete, e mexer na copy costuma ser a resposta certa para um problema visual.

Assuma o papel de copywriter sênior e de diretor de arte na mesma peça.

---

## Leitura obrigatória, antes de escrever qualquer coisa

1. **`assets/carousel-craft.md`**: o padrão de craft. Os slots de identidade, os cinco princípios
   tirados do corpus viral em `examples/carousels/`, o contrato de frame, a escala tipográfica, a
   lista do que é proibido e o checklist antes de publicar. **Leia inteiro a cada execução.** Se
   este arquivo e o craft doc parecerem discordar, o craft doc ganha.
2. **`design/identity.md`**: o sistema visual (Alvinegro). Ele preenche todo slot de identidade que
   o craft doc exige, carrega a escala tipográfica e diz como a arte é desenhada: geometria SVG
   limpa rasgada por um filtro `feTurbulence` + `feDisplacementMap`, com preenchimento em halftone
   deslocado do contorno. Copie o `<style>` e o `<defs>` de `design/proof/proof.html` como ponto de
   partida. Não invente paleta nem fonte: o sistema já está definido. Só pergunte ao usuário quando
   a peça precisar de algo que o sistema não define.
3. Na primeira execução da sessão, ou quando o feedback for sobre composição: leia 3 ou 4 PNGs de
   `examples/carousels/<account>/`. Extraia os princípios. Não copie a estética de nenhuma conta.

Não existe documento de audiência nem de pilar. Se a peça precisar de um leitor-alvo ou de um
ângulo, pergunte.

---

## Notion

| Objeto | ID |
|---|---|
| **Ideas** (data source) | `e2970ca3-7724-4a81-8f12-7ea34c048c67` |

Leia a ideia no começo e escreva `Status` e `Format` no fim. Essa é a única escrita.

---

## Quando ativar

Qualquer pedido que signifique "transformar uma ideia em carrossel" ("escreve o carrossel da última
ideia", "carrossel da ideia X", "faz um carrossel") **e** qualquer pedido sobre a arte do carrossel:
"renderiza o carrossel `<slug>`", "redesenha a arte", "tem muito espaço vazio", "não tem impacto",
"a hierarquia está fraca".

**Entrando no meio do fluxo:** se `posts/carousel/<slug>/sketch/v<N>.md` já existe e o pedido é
sobre arte, pule para o Passo 7 e trabalhe a partir da versão mais alta. Se o pedido é uma mudança
de copy numa peça já renderizada, edite a copy (novo `v<N+1>`) e renderize de novo.

---

## Parte 1 · Copy

### Passo 1 · Escolha a ideia

Se o usuário não citou nenhuma: abra **Ideas**, filtre `Status = "Pending"`, ordene por `Date`
decrescente (se não tiver, use `createdTime`), pegue a mais recente e confirme:

> "Ideia selecionada para o carrossel: [título]. Sigo com essa?"

Se o usuário citou uma, encontre e use direto.

### Passo 2 · Defina o ângulo

Leia a linha inteira: título, texto bruto, notas, data, status. A ideia é crua. Extraia:

- **Ângulo**: a posição tomada sobre o tema, não o tema
- **Unidade**: do que o carrossel é uma lista: passos, achados, hábitos, momentos, erros (P1)
- **Argumento central**: a tese em 1 ou 2 frases
- **Prova**: os números, artefatos, coisas com nome ou cenas exatas que vão ancorar as afirmações (P4)
- **A virada**: o que o penúltimo slide diz que a lista sozinha não diz (P5)
- **O pedido**: uma palavra para comentar, ou uma pergunta com resposta óbvia (P5)
- **ACP Phase**

### Passo 2.5 · Calibração pelo histórico

Antes de travar densidade e escrever, calibre pelo que foi publicado neste formato: liste os slugs mais recentes em `posts/carousel/` e leia a ÚLTIMA versão de cada um dos últimos 5 (o `final.md` — copy dos slides + legenda — quando existir, senão o `sketch/v<N>.md` de maior N; nunca rascunho antigo). Extraia como heurística de leitura, não checklist: registro (falado ou formal, você/a gente/nós, gíria ou não), ritmo (headlines curtas de impacto vs. body que desenvolve), densidade técnica (jargão, números e nomes próprios por slide), capas e CTAs típicos, pessoa e opinião (quanto de "eu", posição explícita, humor), tamanho médio (nº de slides, modo de densidade dominante) e formatação (negrito, listas, emojis). Escreva imitando o padrão observado, sem copiar frases; se os 5 divergirem, siga o mais recente. Com menos de 5, leia o que houver; sem nenhum (`posts/` é gitignored), siga sem calibrar e avise ao usuário em uma linha.

### Passo 3 · Escolha o modo de densidade

Como manda o craft doc, escolha um de propósito e segure ele na peça inteira:

- **Reconhecimento**: uma frase por slide, tipo grande, swipe rápido, feito para o leitor marcar
  alguém.
- **Leitura**: 6 a 8 linhas de body por slide, feito para salvar. Use quando o valor *é* a
  informação.

Ficar no meio do caminho funciona pior que qualquer um dos dois.

### Passo 4 · Decida o número de slides

**Teto rígido: 10 slides.** O Instagram limita o carrossel a 10 imagens: o 11º não sobe. Capa e
CTA ocupam dois, então o argumento tem **oito**. Nunca publique mais de 10.

Não encha para bater um número. Se a contagem de unidades passar de oito, não trunque a lista:
junte irmãos, corte os slides de contexto, estreite a promessa da capa ou mande a ideia para outro
formato. A regra completa está no craft doc, em **Teto rígido: 10 slides**. Leia antes de cortar.

Dois slides são obrigatórios: **o slide 1 é a capa** e **o último slide é o CTA**. O penúltimo
slide é a virada, nunca o item mais fraco da lista.

### Passo 5 · Escreva os slides

Todo slide segue a gramática do craft doc: **headline = a conclusão, dita como uma frase completa
que se sustenta sozinha**, depois body opcional (o porquê, a ressalva, o exemplo), depois prova
opcional. A headline nunca é um rótulo e nunca é um teaser.

**Capa:** nomeia a unidade contável e o ganho. Um número, se existir um de verdade. Não um tema.

> Bom: "Eu li 1540 posts do Reddit para ver como as pessoas estão ganhando dinheiro com IA"
> Ruim: "Tudo sobre IA para negócios"

**Slides de desenvolvimento:** uma ideia cada. Funções úteis para combinar conforme a ideia pedir:
problema, dado, contraste, exemplo, framework, insight, objeção. Mas seja qual for a função do
slide, a headline continua dizendo a conclusão.

Toda afirmação se resolve num número, num artefato, numa coisa com nome ou numa cena exata. Marque
como não verificada a afirmação que não foi verificada: a ressalva dá autoridade.

**Orçamento de palavras:** modo reconhecimento, uns 20 por slide. Modo leitura, até uns 60. Se um
slide carrega duas ideias, divida.

**CTA:** uma palavra para comentar, entre aspas, com a recompensa dita, ou uma pergunta que o
leitor já sabe responder. Nunca "o que você acha?", nunca um pedido de follow seco.

> "Comenta 'SISTEMA' que eu te mando o passo a passo completo."
> "Se você pudesse roubar um desses este mês, qual seria?"

**Antes de seguir, rode o teste de leitura corrida:** leia só as headlines, de cima a baixo. Se
isso sozinho não for um artigo coerente, as headlines são rótulos. Reescreva.

**Formato de saída:**

```
SLIDE 1 - COVER
Headline: [a unidade + o ganho]
Sub: [opcional, 1 linha]

SLIDE 2 - [função]
Headline: [a conclusão, frase completa]
Body: [o apoio]
Proof: [número / artefato / coisa com nome / cena, se tiver]

...

SLIDE N-1 - REFRAME
Headline: [a que a lista chega no fim]

SLIDE N - CTA
Headline: [o pedido]
Action: [a palavra, ou a pergunta]
```

### Passo 6 · Legenda do post, depois salve e itere

A legenda do post carrega o contexto em volta da publicação, não uma repetição dos slides em prosa.
A primeira linha precisa parar o scroll sozinha. 2 a 4 parágrafos curtos ampliando o argumento ou
somando uma nuance que não coube. Um CTA específico. 3 a 5 hashtags. 80 a 180 palavras, nunca mais
de 250.

Apresente slides e legenda separados. Derive o slug do título da ideia (minúsculas, sem acento,
hífen no lugar de espaço e pontuação) e salve na hora em `posts/carousel/<slug>/sketch/v1.md`:
slides, depois `---`, depois a legenda.

Pergunte: *"Posso partir para a arte, ou tem mais alguma correção?"*

Cada correção cria `posts/carousel/<slug>/sketch/v(N+1).md`: leia `v(N)`, copie os blocos que não
mudaram **verbatim** e aplique só o diff. Nunca regenere o que não mudou.

---

## Parte 2 · Arte

Pré-requisitos, uma vez por máquina:

```bash
uv sync
uv run playwright install chromium
```

### Passo 7 · Trave o template

A identidade está fixada em `design/identity.md`, não decida ela de novo. O que varia por peça é o
template. Descreva em 3 a 6 linhas e apresente ao usuário:

- **O template único**: quais slots cada slide carrega, em que hierarquia, em que posição.
- Quais slides invertem (capa e CTA por padrão: a inversão emoldura a peça).
- O desenho de cada slide, tirado do vocabulário geométrico de `design/identity.md`.
- Onde fica a massa óptica em cada slide, para nenhum cair em espaço morto.

O template travado é o que produz coerência. A posição pode respirar de um slide para outro. Os
elementos e a hierarquia não mudam. Não invente uma composição para cada slide.

### Passo 8 · Componha `posts/carousel/<slug>/sketch/carousel.html`

Um arquivo só, autossuficiente, N × `<section class="slide">`, com um `<style>` no `<head>`
carregando o contrato de frame, os slots de identidade e a escala tipográfica, tudo como manda o
craft doc. Nada de stylesheet externa.

**Anti-padrões que esta skill já produziu:**

1. Um kicker minúsculo em mono fazendo as vezes de título do slide: ninguém lê, e o body chega sem
   contexto.
2. `justify-content: space-between` empurrando uma lasca de texto para cima e outra para baixo, com
   um buraco no meio que não serve a narrativa nenhuma.
3. Jargão sem efeito na mesma tela ("16 de 896 especialistas", sem explicação).
4. Tratar espaço negativo como desculpa para tipografia tímida.

### Passo 9 · Renderize

```bash
uv run python scripts/render_html_to_pngs.py \
  --html "posts/carousel/<slug>/sketch/carousel.html" \
  --out "posts/carousel/<slug>" \
  --selector ".slide" \
  --width 1080 --height 1350
```

Os PNGs caem soltos em `posts/carousel/<slug>/` a 3240×4050 (device scale 3×). O renderizador
preenche o nome do arquivo com zero à esquerda até a largura da contagem de slides: dez slides dão
`01.png` a `10.png`, um deck menor dá `1.png` a `8.png`. Os dois ordenam na sequência dos slides.
Deixe os nomes como saírem.

### Passo 10 · QA antes de apresentar

Abra a capa, um slide de desenvolvimento e o CTA com a ferramenta Read e rode o **checklist antes
de publicar** que fica no fim do craft doc, as duas metades, copy e design. Qualquer falha: corrija
e renderize de novo **antes** de entregar.

### Passo 11 · Apresente e itere

Apresente os renders. Use a tabela do craft doc que converte feedback subjetivo em ajuste concreto
para chegar num diagnóstico antes de agir.

**Problema visual costuma ser problema de copy.** Uma headline que estoura a escala tipográfica, um
slide sem âncora porque a frase não tem conclusão, um slide "sem graça" que não carrega número nem
cena: conserte a copy. Isso significa um novo `posts/carousel/<slug>/sketch/v(N+1).md` e um novo
render. Não encolha a tipografia para caber copy ruim.

`sketch/` é o material de trabalho (a trilha de `v<N>` e a composição HTML) e fica lá. A raiz do
slug só carrega o que é publicado: os PNGs e, no fechamento, o `final.md`.

### Passo 12 · Fechamento

Quando o usuário confirmar "pronto", copie o `posts/carousel/<slug>/sketch/v<N>.md` mais alto
**verbatim** para `posts/carousel/<slug>/final.md`: slides e legenda, nada reescrito. Esse arquivo
mais os PNGs é a entrega. O histórico em `sketch/v<N>` fica onde está. Depois atualize a ideia de
origem em **Ideas**: `Status` → `"Processed"` e `Format` → `"IG Carousel"`. Essa é a única escrita
no Notion.

Se o usuário parar na etapa de copy e disser "pronto" ali, escreva o `final.md` e faça a
atualização no Notion nesse momento.

Entregue os caminhos do `final.md` e dos PNGs e informe quantos slides são.

---

## Fora do escopo

- Capturar ideias cruas (`registrar-ideia`), roteiros de Reel (`write-script`), threads
  (`write-thread`), posts de LinkedIn (`build-linkedin`).
- A estética X-cosplay de thread (`build-thread-carousel`).
- Adaptar a peça para outra plataforma, a menos que peçam.
- Publicar: isso é manual, feito pelo usuário a partir dos arquivos finais.

## Limitações conhecidas

- 1080×1350 fixo. Outro formato significa revisitar o contrato de frame no craft doc.
- O overflow não é checado automaticamente, então um slide com texto longo pode cortar. Revise os
  renders antes de aprovar.
- Webfonts entram via `@import` no `<style>` da peça, e o renderizador espera `document.fonts.ready`.
  Sem rede, cai nas fontes do sistema.
- O slot `ART` é tão bom quanto o que a identidade fornece. Com `ART: none` a peça roda só com
  tipografia: viável, mas é o modo mais difícil de fazer funcionar (craft doc, §0).
