---
name: build-linkedin
description: >
  Lê uma ideia do banco Ideas, produz um post de texto longo nativo do LinkedIn na
  voz do usuário e depois encontra e captura a imagem que para o scroll e sai junto
  com ele. Ative com comandos como "monta o post do LinkedIn da última ideia" ou
  "escreve o post do LinkedIn da última ideia".
---

# SKILL · build-linkedin

## Produção · Post de LinkedIn (texto + imagem)

Propósito: transformar uma ideia crua do banco **Ideas** num post de LinkedIn pronto para publicar — texto longo com tese, densidade e posição clara, na voz do usuário, mais a imagem que faz o leitor parar o scroll. A entrega é sempre texto **mais** imagem; se o usuário pedir só o texto, pule a imagem e diga isso.

## Quando agir

Rode quando o usuário disser algo como "monta o post do LinkedIn da última ideia", "escreve o post do LinkedIn da próxima ideia", "LinkedIn do item X", "gera o texto do LinkedIn", ou qualquer variação que signifique transformar uma ideia crua num post longo de LinkedIn.

## Entrada: a ideia

- Banco **Ideas** ID `e2970ca3-7724-4a81-8f12-7ea34c048c67`. Se o usuário não especificou qual ideia: filtre `Status = "Pending"`, ordene por `Date` decrescente (ou `createdTime` se `Date` estiver vazio), pegue a mais recente e confirme o título antes de seguir.
- Leia a linha inteira: título, texto cru, notas, data e status. Extraia o ângulo, a tese, a prova disponível (ou hipótese concreta) e a tensão que pode virar o hook. Identifique também a ACP Phase.
- Não existe documento de audiência nem de pilar: se a peça precisar de um leitor-alvo ou de um ângulo, pergunte ao usuário.

## Voz: calibração por exemplos reais

Escreva como o usuário fala e pensa: posição primeiro, autor exposto, opinião com referente concreto. Sem jargão sem tradução, sem inflação.

Antes de escrever, leia sempre os dois posts reais em `examples/` (`assinatura_cc.md` e `hype_ia.md`). **O assunto deles é irrelevante** — eles calibram como um post humano, com autoridade e compartilhável fica na página: parágrafos de pensamento encadeado com beats curtos raros, frases ligadas por conectivos de verdade, nomes e números verificáveis, o autor em jogo, e fechamento que toma posição em vez de pedir engajamento.

## O post

Deixe a necessidade do argumento definir o tamanho: sem enchimento, sem corte prematuro. O teto técnico do LinkedIn é 3.000 caracteres. Se a ideia precisa de mais que isso para manter a qualidade, considere o formato carrossel.

Escreva o post na forma final de publicação — quebras de linha incluídas, sem rótulos estruturais, pronto para colar. Junto, entregue a contagem de caracteres e a ACP Phase. Regras do formato:

- **Parágrafo é unidade de pensamento, não de exibição.** A maioria desenvolve uma ideia em várias frases; o parágrafo de uma frase é um beat raro (dois ou três por post, no máximo).
- **Sem markdown** (o LinkedIn não renderiza `**`, `_`, `#`), **sem emojis decorativos** e **sem hashtags** — a menos que o usuário peça, e aí no máximo três, específicas, em linha própria no fim.
- **Primeira linha cria a tensão do "ver mais" sem entregar a resposta.** Não fabrique uma tensão que a ideia não tem: material real segura sem truque.
- **Fechamento toma posição ou pergunta algo que o autor de fato não sabe** e um leitor qualificado talvez saiba. Nunca "o que você acha?".

## Iteração e rascunho local

Derive o slug do título da ideia (minúsculas, sem acento, hífens no lugar de espaços e pontuação) e salve o post na hora como `posts/linkedin/<slug>/sketch/v1.md`. Cada correção pedida vira `v(N+1).md`: leia a versão anterior, copie os blocos imutados **verbatim**, aplique só o diff, nunca regenere o que não mudou. Repita até o usuário confirmar que está pronto.

## A imagem

Com o texto travado, encontre a única imagem que merece a parada. Antes de buscar, escreva uma frase: *o que essa imagem tem que mostrar?* — respondida a partir do post. Prefira o artefato real que o leitor reconhece do próprio trabalho (o diagrama da arquitetura em discussão, um gráfico com forma surpreendente, um print do artefato, uma figura do paper citado com crédito) a qualquer coisa decorativa. Nunca foto de banco de imagem, arte gerada por IA ou card com o hook sobre gradiente — e não fabrique imagem em HTML. A imagem tem que ser legível pequena, no celular, e sobreviver aos modos claro e escuro.

Busque com as ferramentas de automação do navegador (invoque a skill `claude-in-chrome` antes de usá-las): vá à fonte (paper, docs, post original) antes da busca de imagens, capture por screenshot recortado na figura, sem mobília da página. Se nada bom aparecer em duas ou três buscas, diga isso — um post sem imagem ganha de um post com imagem ruim.

Salve como `posts/linkedin/<slug>/image.png` e registre no rodapé do `sketch/v<N>.md` final: `Imagem: posts/linkedin/<slug>/image.png — <URL de origem>`. Mostre a imagem, diga por que a escolheu e pergunte se funciona ou se procura outra.

## Fechamento ("pronto")

Só no "pronto" explícito do usuário: copie o `sketch/v<N>.md` de maior número para `posts/linkedin/<slug>/final.md` (o histórico `sketch/` fica intacto como trilha de auditoria) e atualize a ideia no banco Ideas: `Status` → `Processed`, `Format` → `LinkedIn Post`. Essa é a única escrita no Notion — o conteúdo nunca sobe. Feche com: "Post pronto. Tudo sai de `posts/linkedin/<slug>/`: `final.md` e `image.png`. Próximo passo: publicar manualmente no LinkedIn."

## Fora do escopo

Não captura ideias cruas, não escreve roteiros, carrosséis nem threads, não adapta carrossel para o LinkedIn e não publica nada — publicar é manual.
