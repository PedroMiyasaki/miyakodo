---
name: carousel
description: >
  Produz um carrossel de Instagram completo a partir de uma ideia do banco
  Ideas. Copy e composição nascem juntas no asset visual, sem rascunho
  intermediário em Markdown. Use para criar, revisar ou finalizar um
  carrossel. Carrosséis derivados de threads usam build-thread-carousel.
---

# Carrossel

Transforme uma ideia em um carrossel pronto para publicar. Trabalhe como copywriter e diretor de arte ao mesmo tempo: texto, hierarquia e composição devem ser resolvidos juntos no slide.

Não escreva primeiro um roteiro de slides em Markdown. A primeira versão apresentada já deve ser visual e renderizada.

## Fonte e destino

O banco canônico é **Ideas**, data source `e2970ca3-7724-4a81-8f12-7ea34c048c67`.

Cada iteração é uma versão visual completa:

```text
posts/carousel/<slug>/
  sketch/
    v1/
      carousel.html
      <renders>.png
    v2/
      carousel.html
      <renders>.png
  <renders finais>.png
```

O slug vem do título da ideia: minúsculas, sem acento e com hífens no lugar de espaços e pontuação. `carousel.html` é a composição editável; os PNGs da mesma pasta são exatamente os renders daquela versão.

## Processo

### 1. Ler a ideia

Se o usuário indicar uma ideia, use essa. Caso contrário, leia a ideia `Pending` mais recente em **Ideas**. Entenda a ideia inteira e defina a fase ACP sem transformar essa leitura num formulário ou checklist.

Guarde no `<head>` do HTML o ID da ideia de origem e a fase ACP em metatags, para que a peça continue vinculada à origem durante as iterações.

### 2. Calibrar pelo histórico

Antes de criar, examine até os cinco carrosséis mais recentes em `posts/carousel/`. Para cada um, use os PNGs finais da raiz; se eles não existirem, use a pasta `sketch/v<N>/` de maior número. Leia também o `carousel.html` correspondente quando existir.

Use esse histórico como few-shot, não como checklist. Perceba:

- linguagem: vocabulário, registro, construção das frases, ritmo, pontuação, pessoa, humor, opinião, densidade técnica, hooks e CTAs;
- narrativa: quantidade de texto, progressão entre slides, alternância de ritmo e maneira de abrir e fechar;
- visual: hierarquia, escala tipográfica, composição, contraste, uso de espaço, repetição, ilustração e relação entre texto e imagem.

Imite os padrões recorrentes sem copiar frases ou layouts. Dê mais peso aos trabalhos recentes. Se houver menos de cinco, use o que existir; se não houver nenhum, siga sem calibração.

### 3. Criar a versão visual

Leia `design/identity.md` antes de compor. Ele é a regra da identidade Miyakodo e a fonte canônica de cor, tipografia, logo, mascote e textura. Se a peça precisar de um hex ou de uma família, use só o que esse arquivo registra.

A base técnica são os assets em `design/`:

- `design/logo/`: logo horizontal e vertical, PNG e PDF. A cor de cada arquivo está na tabela de `identity.md`. O número do logo horizontal não é a mesma cor no PNG e no PDF.
- `design/fontes/`: `instrument-serif.zip` (títulos, Instrument Serif, Regular e Italic) e `poppins.zip` (corpo, Poppins). Não copie as fontes para fora dessa pasta.
- `design/mascote-e-textura/`: mascote Carlos e `textura.pdf`. O número do mascote também diverge entre PNG e PDF. Use a tabela de `identity.md`.
- `design/apresentacao-idv-pedro-miyakodo.pdf`: guia visual.

A identidade é fixa. Narrativa e composição pertencem à peça. Hierarquia e tamanho de tipo saem da peça e do histórico recente.

Crie diretamente `posts/carousel/<slug>/sketch/v<N>/carousel.html`, onde N é o próximo número disponível. O arquivo deve ser autossuficiente e conter todos os slides como `<section class="slide">`.

Resolva a copy dentro da composição. Decida livremente o número de slides, o ritmo, a estrutura, os arquétipos e a densidade que melhor servem à ideia. Preserve coerência entre os slides sem forçar todos a terem a mesma composição.

Cada slide deve medir 1080x1350, o formato 4:5 do carrossel de Instagram. Não apresente uma etapa separada de copy, plano visual ou aprovação de template.

### 4. Renderizar e revisar

Renderize a própria pasta da versão:

```bash
uv run python scripts/render_html_to_pngs.py \
  --html "posts/carousel/<slug>/sketch/v<N>/carousel.html" \
  --out "posts/carousel/<slug>/sketch/v<N>" \
  --selector ".slide" \
  --width 1080 --height 1350
```

Abra todos os PNGs e revise o carrossel como sequência. Corrija na mesma versão qualquer overflow, falha de legibilidade, desequilíbrio evidente ou quebra de narrativa encontrada antes da apresentação e renderize novamente.

### 5. Apresentar e iterar

Apresente os renders e peça feedback. Cada rodada de feedback cria uma nova pasta `sketch/v<N+1>/` com um `carousel.html` completo e seus próprios PNGs.

Parta da versão anterior e mude apenas o que o feedback exigir, incluindo os ajustes de copy necessários para a composição funcionar. Não mantenha texto ruim apenas porque o problema foi descrito como visual, nem redesenhe o que já foi aprovado.

Continue criando versões até o usuário dizer explicitamente "pronto".

### 6. Fechar

Quando o usuário disser "pronto":

1. copie os PNGs da versão aprovada para `posts/carousel/<slug>/`;
2. remova da raiz renders antigos que não pertençam à versão aprovada;
3. mantenha todas as versões em `sketch/`;
4. atualize a ideia de origem em **Ideas** para `Status` = `Processed` e `Format` = `IG Carousel`.

Não crie `final.md`: os PNGs publicados são a entrega final. Informe a versão aprovada, a quantidade de slides e a pasta de saída.
