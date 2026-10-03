---
name: build-linkedin
description: >
  Lê uma ideia do banco Ideas, produz um post nativo do LinkedIn na voz do
  usuário e encontra uma imagem que acompanha o texto. Ative com comandos como
  "monta o post do LinkedIn da última ideia" ou "escreve o post do LinkedIn".
---

# Produção · Post de LinkedIn

Propósito: transformar uma ideia crua em um post de LinkedIn com argumento, opinião e substância, pronto para publicar junto com uma imagem relevante.

Use o Notion MCP para ler o banco **Ideas** e, no fechamento, atualizar `Status` e `Format`. Essa é a única escrita no Notion; o conteúdo nunca sobe.

Banco **Ideas** · `e2970ca3-7724-4a81-8f12-7ea34c048c67`

## Quando agir

Rode quando o usuário pedir, em linguagem natural, para transformar uma ideia em post de LinkedIn. A entrega padrão é texto e imagem. Se ele pedir só o texto, pule a imagem.

## Passo 1 · Identificar a ideia

Se o usuário não indicou qual:

- Abra o banco Ideas.
- Filtre por `Status = "Pending"` e ordene por `Date` decrescente; se necessário, use `createdTime`.
- Pegue a mais recente, mostre o título e confirme antes de seguir.

Se o usuário indicou uma ideia, encontre ela e use direto.

## Passo 2 · Ler a ideia e definir a fase ACP

Leia a linha inteira no Notion, incluindo título, notas, contexto e anexos. Entenda a ideia como um todo e defina a `ACP Phase`.

## Passo 3 · Calibrar a linguagem pelo histórico

Liste os slugs mais recentes em `posts/linkedin/` e leia a última versão de até cinco posts: `final.md` quando existir; senão, o `sketch/v<N>.md` de maior N. Nunca leia versões antigas como referência.

Observe como o usuário escreve nesse formato: registro e tratamento, ritmo das frases e parágrafos, densidade técnica, presença de números e nomes próprios, tipos de abertura e fecho, uso de primeira pessoa, opinião e humor, extensão e formatação.

Use o padrão observado como few-shot, sem copiar frases. Se os posts divergirem, dê mais peso ao mais recente. Com menos de cinco, leia o que houver. Sem nenhum, siga sem calibração e avise em uma linha.

Não existe documento de audiência nem de pilar. Se a ideia realmente exigir uma definição que ela própria não traz, pergunte ao usuário.

## Passo 4 · Escrever o post

Escreva o post completo na forma final de publicação, pronto para colar no LinkedIn. Respeite o teto técnico de 3.000 caracteres e use texto puro: o LinkedIn não renderiza markdown.

### Hook

A primeira linha é o que aparece antes de "ver mais". Ela deve colocar o leitor dentro do assunto e criar motivo para continuar, sem preâmbulo genérico nem tensão fabricada.

### Desenvolvimento

Desenvolva a ideia em parágrafos naturais. Dê ao argumento o espaço que ele pede, sustentando-o com fatos, mecanismos, exemplos ou experiência concreta. A estrutura deve nascer da ideia e da calibração do Passo 3, não de um molde fixo.

### Fecho

Termine quando o argumento estiver completo: numa posição, consequência, tradeoff ou pergunta honesta que a peça realmente abriu. Não acrescente um pedido vazio de engajamento.

Entregue o post sem rótulos como `HOOK` ou `DESENVOLVIMENTO`, seguido da contagem de caracteres e da fase ACP.

## Passo 5 · Apresentar, iterar e salvar

Derive o slug do título da ideia: minúsculas, sem acentos, hífens no lugar de espaços e pontuação.

Salve o primeiro rascunho em:

```text
posts/linkedin/<slug>/sketch/v1.md
```

O arquivo contém o post na forma final de publicação e um rodapé com a contagem de caracteres e a ACP.

Apresente o post e pergunte se está pronto ou se precisa de correção. Cada correção cria `sketch/v(N+1).md`: leia a versão anterior, copie verbatim os blocos que não mudaram e aplique apenas o diff. Não regenere o restante.

Só avance quando o usuário confirmar "pronto" explicitamente.

## Passo 6 · Encontrar a imagem

Com o texto confirmado, defina em uma frase o que a imagem precisa mostrar. Prefira um artefato real que torne o argumento visível: diagrama, gráfico, print, trace, interface ou figura de uma fonte citada. Evite imagem genérica ou meramente decorativa.

Use a automação de navegador disponível. Vá primeiro à fonte original (paper, documentação, blog ou repositório) e use busca de imagens apenas como fallback. Pesquise pelo nome canônico do objeto, de preferência em inglês. Capture o elemento na página, sem a interface do navegador ao redor.

A imagem precisa funcionar no tamanho do feed: legível no celular, com poucos elementos, bom contraste, sem marca d'água e sem texto acidental da página. Se nada adequado aparecer após duas ou três buscas, pare e diga isso; publicar sem imagem é melhor que usar uma imagem ruim.

Salve em:

```text
posts/linkedin/<slug>/image.png
```

Registre no rodapé da versão final do sketch:

```text
Imagem: posts/linkedin/<slug>/image.png - <URL de origem>
```

Mostre a imagem, explique em uma linha por que ela foi escolhida e peça aprovação. Se o usuário pedir outra, redefina primeiro o que ela precisa mostrar.

## Passo 7 · Fechar

Depois que o texto estiver confirmado e a imagem aprovada, copie a versão mais alta do sketch, verbatim, para:

```text
posts/linkedin/<slug>/final.md
```

A raiz da peça fica com `final.md` e, quando houver imagem, `image.png`. O histórico permanece em `sketch/`.

Atualize a ideia no Notion:

- `Status` → `Processed`
- `Format` → `LinkedIn Post`

Confirme o caminho dos arquivos. A publicação no LinkedIn é manual.
