---
name: write-script
description: >
  Lê uma ideia do banco de Ideias e produz um roteiro de Reel completo,
  formatado para o teleprompter, na voz do usuário.
  Ative com comandos como "escreve o roteiro da última ideia".
---
## 1. Produção · Roteiro de Reel

Propósito: transformar uma ideia do banco de Ideias num roteiro de Reel que um curioso pararia para ver e assistiria até o fim, na voz do usuário, no formato híbrido do teleprompter. 

**A ideia chega escrita como análise. O roteiro sai como história (story-telling).** A linha do Notion costuma trazer uma tese de analista e uma pilha de fatos (rodada, versão, benchmark, sigla). O trabalho não é resumir, é transformar a idea em uma boa história, com tom autoritativo e dando valor ao espectador; Começe fazendo a história!

---

## 2. O formato: literal & tópicos

O usuário não lê roteiro palavra por palavra, **parte do trabalho aqui a retenção fica literal, e o que decide a naturalidade vira tópico.**

- **Literal:** o texto é falado exatamente como está escrito. São o gancho, as viradas, a recompensa e o CTA.
- **Tópicos:** pistas curtas do que explicar, na ordem, para o usuário falar do jeito dele. São a promessa e o miolo de cada degrau.

**Todo bloco declara o modo no cabeçalho, sempre** (`[HOOK] · literal`, `[DEGRAU] · tópicos`), e cada bloco tem um modo só. Se o usuário pedir outro modo para um bloco, siga o pedido dele.

---

## Quem assiste

O Reel existe para alcançar quem ainda não segue o usuário. O espectador padrão, definido pelo usuário em 2026-09-12, é o **entusiasta curioso de IA**: brasileiro, usa o ChatGPT, vê manchete de IA passando no feed, acha o assunto interessante e **não é da área**.

- **Ele reconhece:** ChatGPT, OpenAI, Google, Nvidia, Elon Musk, Apple, robô, algoritmo, assinatura, chip (de ouvir falar).
- **Ele não sabe o que é:** harness, token, benchmark, wrapper, pretraining, peso aberto, inferência, API, valuation, Series E.
- **O teste de ouro:** ele entende tudo ouvindo uma vez, sai com uma ideia que não tinha, e um engenheiro assistindo ao mesmo vídeo não encontra nada errado.
- **Simples não é raso.** A ideia pode ser complexa: o que precisa ser simples são as palavras.

Se o usuário nomear outro público para a peça, siga o público que ele nomeou.

---

## Ferramentas disponíveis

- **MCP do Notion:** ler o banco **Ideas** e, no fechamento, atualizar `Status` e `Format` na ideia processada (a única escrita no Notion).
- **Ferramenta de subagente (**`Agent`**),** quando existir nesta sessão: roda a leitura fria do Passo 6 num contexto limpo.

---

## Referências obrigatórias


| Fonte                                                                              | O que procurar                                                                                                                                |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ideas** · `e2970ca3-7724-4a81-8f12-7ea34c048c67` (ID do data source, via Notion) | A ideia de origem do roteiro |


Não existe documento de audiência nem de pilar. O espectador do Reel está definido acima. Se a peça pedir outro leitor, ou um ângulo que você não consegue achar, pergunte ao usuário.

---

## Quando agir

Rode esta skill quando o usuário pedir, com qualquer frase, para transformar uma ideia crua em roteiro de Reel. Exemplos de gatilho:

- "escreve o roteiro da última ideia"
- "roteiro da ideia X"
- "escreve o roteiro"

---

## Protocolo de execução

### Passo 1 · Identificar a ideia

Se o usuário não disse qual ideia:

- Abra o banco **Ideas** (`e2970ca3-7724-4a81-8f12-7ea34c048c67`).
- Filtre por `Status = "Pending"` e ordene por `Date` decrescente (a mais recente primeiro). Se `Date` não existir ou estiver vazio, use `createdTime`.
- Pegue a ideia mais recente.
- Mostre o título ao usuário e confirme antes de seguir:
  > "Ideia selecionada para o roteiro: [título]. Sigo com essa?"

Se o usuário indicou um título ou item, ache essa ideia no banco Ideas e use ela direto.

### Passo 2 · Ler a ideia

Abra a linha correspondente no banco Ideas e leia tudo que estiver disponível: título, notas, exemplos anexados, data e status. Defina também a ACP Phase.

### Passo 3 · Calibrar a voz

Roteiro de Reel é fala transcrita: escreva como o usuário fala - direto, sem inflação, sem jargão sem tradução. Leia também a seção **Calibração**, no fim desta skill: ela mostra um roteiro aprovado e as correções reais que o usuário fez em primeiras versões.

### Passo 4 · Planejar antes de escrever

Os três blocos abaixo ficam nas suas notas de trabalho, não no arquivo. É aqui que o roteiro fica bom ou ruim: um texto bem escrito em cima de um ângulo de analista continua sendo um vídeo que ninguém assiste.

#### 4a · Traduzir a ideia para quem assiste

Responda por escrito, em uma ou duas linhas cada:

1. **O fato, contado para um amigo.** Como você contaria isso numa mesa de bar para alguém que não é da área? Sem sigla, sem valor de rodada, sem nome que ele não conhece.
2. **O que está em jogo para ele.** Onde o assunto encosta na vida do espectador, e como:
  - o dinheiro dele (assinatura, preço, investimento)
  - o trabalho ou a carreira dele
  - as ferramentas que ele usa
  - medo ou segurança
  - ser enganado (hype, conflito de interesse, número maquiado)
  - curiosidade sobre como o mundo funciona (disputa entre países, dinheiro grande, bastidor)
3. **A pergunta do vídeo.** Uma pergunta, do jeito que o espectador faria, que o gancho cria e que só a recompensa responde. Exemplos: "por que a ação caiu se ela bateu recorde?", "qual profissão é a próxima?", "se nada mudou no modelo, o que mudou?".
4. **O dicionário.** Todo termo ou conceito sem o qual a história não fecha, cada um com a tradução que vai para o roteiro: uma analogia do dia a dia ("o modelo é o cérebro, o harness é a mão") ou uma explicação de uma frase ("chip, a peça que faz IA rodar"). Termo de que a história não precisa sai do roteiro. Empresa ou produto que ele não conhece ganha um aposto curto na primeira menção ("a Harvey, uma IA feita para advogados").
5. **O material mais forte.** O fato mais surpreendente, já em escala humana ("menos da metade do preço" no lugar de "57% mais barato"). Uma cena, um personagem ou um exemplo que dá para imaginar. Uma prova que dá para mostrar na tela (post, gráfico, página de preço, manchete).
6. **O que fica de fora.** Os fatos da ideia que não ajudam a responder a pergunta. A ideia é matéria-prima: nome de fundo, valor de rodada, versão e detalhe de arquitetura só entram quando a história precisa deles.
7. **A sacada, quando existe uma boa.** A sacada é o que a notícia revela além do próprio caso: o padrão por trás do fato, que o espectador não concluiria sozinho e que um engenheiro reconheceria como verdade. **Ela é opcional.** Vídeo que explica bem uma notícia é um vídeo legítimo, e sacada genérica é pior que nenhuma. Decida pelo que as notas e a conversa trazem:
  - **Existe um ângulo de raciocínio do usuário:** um texto dele dizendo o que o vídeo deve argumentar ou conectar, com ou sem o nome "sacada" ("conectar com a ideia de que…", "ângulo de vídeo: …", uma opinião dele sobre o fato). Esse ângulo é a sacada: escreva o roteiro em cima dele, sem marca nenhuma.
  - **As notas só resumem o fato:** é o formato da `content-research` (`O que aconteceu`, `Por que está em alta`, `Contexto` e `Fontes`), e esse contexto factual não conta como ângulo do usuário. Procure uma sacada com as três perguntas abaixo. Se ela passar no teste de sacada boa, entra no roteiro **marcada como proposta** (Passo 5, **Formatação**). Se não passar, o roteiro fica na notícia, sem sacada.
   As três perguntas, em sequência:
  - **O mecanismo:** o que mudou de verdade para esse fato acontecer? (Cognition: quem vende o modelo de IA passou a vender também o produto pronto.)
  - **O que só existia por causa do contrário:** o que fazia sentido enquanto o mecanismo era o oposto, e agora perde o chão? (Empresa que monta o produto em cima do modelo de um fornecedor que não concorria com ela.)
  - **Onde mais, e o que vem:** onde o mesmo mecanismo bate em seguida, e o que muda para quem usa ou constrói tecnologia? (Todo app feito em cima do modelo de outra empresa corre o mesmo risco, e quem pode vai querer um modelo próprio.)
   **Teste de sacada boa.** Falhou em um item, a sacada fica de fora:
  - Tem um mecanismo concreto, e não "a IA está mudando tudo".
  - Diz algo que o espectador não tiraria sozinho da notícia.
  - Traz um segundo exemplo, ou uma consequência com nome.
  - Não sobrevive à troca de assunto: se ela serviria igual para qualquer outra notícia de IA, é genérica (teste de ler em voz alta).
   Quando existe sacada, ela vira o último degrau do roteiro, e a recompensa responde a pergunta do vídeo no nível dela.

**O título da ideia é o assunto. O gancho nasce da pergunta do vídeo (item 3).**

Se as notas da ideia, ou a conversa, trazem um ângulo escrito pelo usuário, esse ângulo manda na tradução inteira, e é ele que vira a sacada (item 7).

**Portão 🔥.** Se o item 2 ficou sem resposta, a ideia não passa no portão 🔥. Diga isso ao usuário antes de escrever, junto com o ângulo mais próximo que passaria (ou a sugestão de outro formato, como post de LinkedIn), e espere a decisão dele.

#### 4b · Escolher o formato da história

Todo roteiro roda na mesma espinha (Passo 5). O formato decide o que vai em cada degrau dela. Escolha o formato que a pergunta do vídeo pede:

**1 · O mistério** · *aconteceu uma coisa que não faz sentido*
Use quando o fato contradiz o que se esperaria.

1. O paradoxo, com nomes que ele conhece.
2. A explicação óbvia, e por que ela não fecha.
3. A pista de verdade, ensinada do zero.
4. A revelação.
5. O que a revelação muda para ele e, se houver sacada, o padrão por trás dela.

**2 · A crença invertida** · *todo mundo acha uma coisa, e é outra*
Use quando o fato derruba uma crença ou um hábito comum.

1. A crença, dita como o espectador diria.
2. O fato que derruba ela.
3. Por que isso acontece, em degraus.
4. A prova: um caso concreto.
5. A regra ou o teste que ele leva embora e, se houver sacada, onde mais essa crença está caindo.

**3 · O desmonte** · *uma afirmação que está assustando ou empolgando todo mundo, olhada de perto*
Use quando o assunto é um anúncio, uma promessa ou um alerta que está circulando.

1. A afirmação, com todo o peso, como se fosse verdade.
2. Quem disse, com a prova de que disse.
3. O que não bate quando você olha de perto.
4. A evidência na outra direção, ou o interesse de quem disse.
5. A posição do usuário, em primeira pessoa, com o limite dela dito.

**4 · A aula em camadas** · *para entender isso, você precisa de duas ou três peças*
Use quando o assunto só faz sentido depois de ensinar conceitos: é o vídeo pedagógico.

1. Por que ele precisa entender isso (dinheiro, decisão, a notícia que ele vai ver).
2. A primeira peça, com analogia.
3. Uma demonstração concreta dela.
4. A virada: parecia resolvido, e a segunda peça complica.
5. A terceira peça, se existir.
6. A regra que junta tudo e, se houver sacada, onde mais ela vale.

Quando a pergunta é um mistério que só se resolve ensinando conceitos, use o mistério com os degraus da aula.

#### 4c · Gerar e testar o gancho

Escreva **pelo menos 8 ganchos, de pelo menos 5 tipos** da tabela. Os exemplos são ganchos que o usuário escreveu ou aprovou:


| Tipo                | Forma                                                   | Exemplo aprovado                                                                                                                                                  |
| ------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Crença invertida    | todo mundo achou X, aconteceu Y                         | "Todo mundo achou que o robô ia pegar a fábrica. Pegou o escritório de advocacia."                                                                                |
| Paradoxo            | um recorde e uma consequência que não combina com ele   | "Quarta, a Nvidia anunciou o maior faturamento da história dela. No mesmo dia, a China mostrou por que isso pode não durar."                                      |
| Reviravolta         | antes era X, agora é Y, e nada mudou                    | "Três dias atrás o GPT-6 era a melhor IA do mundo. Hoje ele empata com o Claude. E nada no GPT-6 mudou."                                                          |
| Aviso               | uma ordem direta que protege o espectador               | "Não assina plano anual de IA. Nenhum."                                                                                                                           |
| Pré-requisito       | antes de fazer X, entenda Y, senão…                     | "Antes de pagar por qualquer assinatura de IA pra programar, você precisa entender o Terminal-Bench. Senão você tá só chutando com o seu dinheiro."               |
| Conselho de fora    | um conselho contraintuitivo, e quem diz não é o usuário | "Se você quer construir uma empresa de bilhões com IA, para de vender software. E quem está dizendo isso não sou eu."                                             |
| Alarme e desinflada | a afirmação com todo o peso, depois a fonte             | "A inteligência artificial pode acabar com a humanidade até o fim dessa década. Bom. Pelo menos é isso que diz um pesquisador que saiu da Anthropic essa semana." |
| Mundo escondido     | está acontecendo algo grande que ele não viu            | "Talvez você não saiba, mas tem uma guerra fria entre Estados Unidos e China acontecendo agora. É por inteligência artificial."                                   |
| Reconhecimento      | algo que ele já viu, e o veredito                       | "Sabe aqueles gráficos de benchmark que todo modelo novo lança junto? Aqueles em que a barra está sempre mais alta que da última vez? Eles são quase inúteis."    |
| Os dois lados       | a mesma coisa é ótima para um e péssima para outro      | "Um prompt que acerta 99% das vezes é ótimo se você é o usuário. Péssimo se você está construindo um produto."                                                    |


Regras de forma que valem para todos:

- **A primeira frase já está dentro do assunto:** sem cumprimento e sem anunciar o vídeo ("oi, gente", "hoje eu vou falar", "neste vídeo").
- **A primeira frase sozinha segura o dedo.** Se o gancho só funciona a partir da segunda frase, a segunda vira a primeira.
- **O gancho inteiro cabe em até ~30 palavras.**
- **Número no gancho só quando ele é sentido sem fazer conta:** "o maior faturamento da história", "metade do preço", "a melhor IA do mundo". Valor de rodada e porcentagem de benchmark entram no miolo, já traduzidos.

Passe cada gancho pelo teste abaixo. **Gancho que falha em uma pergunta sai.**

1. **Reconhecimento.** Nas primeiras palavras aparece algo que o entusiasta já conhece: uma marca, uma experiência dele, uma crença comum.
2. **Aposta.** Dá para sentir o que está em jogo para ele.
3. **Pergunta aberta.** Quando o gancho termina, ele tem uma pergunta que só o vídeo responde.
4. **Primeira escuta.** Ele entende a frase ouvindo uma vez. Se aparece um termo técnico, a própria frase já deixa claro o que ele é.
5. **Boca do usuário.** O usuário diria essa frase assim, em voz alta, para um amigo.
6. **Promessa cumprida.** O roteiro entrega o que o gancho promete. Gancho que o vídeo não paga é clickbait, e o README proíbe.

Entre os que passaram, escolha o de aposta mais forte. Guarde os dois melhores seguintes, de tipos diferentes, para mostrar na apresentação.

### Passo 5 · Escrever o roteiro

#### A espinha

Todo roteiro tem estes blocos, nesta ordem. Cada um tem um trabalho na curva de retenção: quem arrasta o dedo quase sempre sai num bloco que não fez o trabalho dele.


| Bloco          | Modo    | Trabalho                                                                                                                 | Tamanho          |
| -------------- | ------- | ------------------------------------------------------------------------------------------------------------------------ | ---------------- |
| `[HOOK]`       | literal | Parar o dedo: algo que ele reconhece, algo em jogo, uma pergunta aberta                                                  | até ~30 palavras |
| `[PROMESSA]`   | tópicos | Confirmar que a pergunta vale a pena e que vai ser respondida. Só o contexto sem o qual o primeiro degrau não se entende | 1 a 3 tópicos    |
| `[VIRADA]`     | literal | Abrir o degrau seguinte com a pergunta dele                                                                              | 1 ou 2 frases    |
| `[DEGRAU]`     | tópicos | Ensinar ou provar uma coisa. De um a quatro degraus, cada um logo depois da sua virada                                   | 2 a 5 tópicos    |
| `[RECOMPENSA]` | literal | Responder a pergunta do vídeo de forma concreta, retomando o gancho                                                      | até ~6 linhas    |
| `[CTA]`        | literal | Um pedido só, e o roteiro acaba                                                                                          | até 3 linhas     |


Regras da espinha:

- **Todo** `[DEGRAU]` **vem logo depois de uma** `[VIRADA]`**.** A virada é uma mudança de direção ("mas", "só que", "aí"), uma consequência ("então", "por isso") ou uma pergunta direta, sempre com referente concreto: "Só que a Nvidia avisou que a margem vai cair" abre um degrau, "E foi aí que tudo mudou" não abre nada (frase de guru: soa como aforismo mas não diz nada concreto). Se a ligação natural entre dois degraus é "e também", o segundo é item de lista: junte os dois. A regra é dos criadores de South Park, e é ela que separa história de lista de fatos.
- **As viradas variam de forma:** uma é "mas", outra é pergunta, outra é "então". Três "só que" seguidos viram tique.
- **Todo degrau carrega pelo menos um fato conferível:** um número traduzido, um nome, uma data, uma cena real. Explicação sem fato vira aula genérica, e é o fato que faz o engenheiro confiar e o curioso contar para alguém.
- **Todo tópico acrescenta algo:** um fato, um porquê, uma analogia, um exemplo ou uma prova na tela. Tópico que repete o anterior sai.
- **Quando existe sacada (4a, item 7), o último degrau é o dela.** Ele sai do caso da notícia e mostra o padrão: o mecanismo, o que perde o chão e onde mais isso acontece. Fica em tópicos, porque é o raciocínio que o usuário faz melhor com as palavras dele. A virada que abre esse degrau avisa que o assunto é maior que o caso. Sem sacada, o último degrau fecha a notícia.
- **A resposta da pergunta do vídeo mora na** `[RECOMPENSA]`**.** A promessa e os degraus aproximam o espectador dela.
- **A recompensa retoma o gancho**, com a mesma palavra ou o mesmo número: "Então lembra que a qualidade tinha caído só 2%?"

#### Como escrever um tópico

O tópico é pista, não frase. Ele guarda as decisões de roteiro (o que explicar, com qual analogia, com qual número) e deixa as palavras para o usuário.

- **Uma ideia por linha,** começando com `-` , em poucas palavras (até ~15).
- **Telegráfico:** sem conectivo e sem frase completa. `→` para causa e consequência, `=` para tradução, `:` para detalhe. Exemplo: "contestar cobrança → olhar o extrato → demora → silêncio de linha caída".
- **A analogia e o exemplo escolhidos estão no tópico:** "robô de hoje = áudio de WhatsApp: fala, para, espera, torce".
- **Número e nome estão escritos exatamente como devem ser ditos:** "552 bilhões de números, usa menos de 3% por vez", "15 centavos de dólar = ler uns cinco livros".
- **Termo técnico vem com a tradução do lado:** "harness = a mão do modelo".
- **Tópico que virou frase completa é roteiro literal disfarçado:** corte até sobrar a pista.

#### Explicar como quem conversa

O registro é o do usuário explicando para um amigo curioso, e não o de um analista resumindo para um colega. Nos blocos literais, as regras abaixo moldam a própria fala. Nos tópicos, elas decidem o que vai na pista.

- **Todo número ganha o "ou seja".** Literal: "Eles tiravam 30%, 40%. Ou seja, não acertavam a maioria das questões." Tópico: "30%, 40% = não acertavam a maioria".
- **Toda afirmação que sustenta a história ganha o porquê,** numa frase.
- **Todo termo do dicionário (4a) entra traduzido na primeira vez que aparece.** Traduções que o usuário aprovou: "O modelo é o cérebro. Entra texto, sai texto. Ele não tem mãos." / "A briga é por chip, a peça que faz IA rodar." / "Ela pega um modelo de peso aberto e usa o modelo americano como professor." / "A GPU vira garantia de empréstimo, que nem imóvel." Elas mostram o tipo de tradução. Quando o conceito é o mesmo, a analogia pode voltar, mas a frase sai com palavras novas, porque frase repetida de um Reel para outro vira bordão.
- **O nome que ele conhece vem primeiro:** "ChatGPT" antes de "GPT-6 Astra", "uma empresa que aplica a mesma prova em todas as IAs" antes de "Artificial Analysis".
- **Um exemplo que dá para imaginar ganha de três dados.** Uma cena, um caso, um experimento mental: "Pega o Opus 5. Duas cópias. Mesmos pesos, mesma versão, tudo igual. A primeira tem uma ferramenta que edita arquivo trocando um trecho exato por outro. A segunda só tem uma ferramenta que reescreve o arquivo inteiro."
- **Opinião vem em primeira pessoa, com o limite dito.** "Eu não estou dizendo que ele está de má-fé. Mas eu não gosto de sentir medo por causa de declaração solta."
- **Fala, não texto, nos blocos literais:** "Sabe aqueles…?", "Então…", "Só que…", "tá", "pra". As muletas que o usuário já pediu para cortar na gravação ("basicamente", "meio que") ficam fora do roteiro.

#### Tamanho

O tamanho é o que a pergunta do vídeo precisa para ser respondida com clareza. Não existe teto.

- **A regra que controla o tamanho:** toda frase literal e todo tópico ensina, prova ou abre a próxima pergunta. O que não faz nenhuma das três sai. Explicação de que o espectador precisa para entender faz a primeira das três, e fica.
- **Referência, não meta:** a maioria dos Reels cabe entre 1:15 e 2:00 de fala, e uma aula em camadas pode chegar a 3 minutos. Para estimar: as palavras literais divididas por 200 por minuto (a velocidade do usuário depois do corte), mais uns 8 segundos por tópico.
- **Frase que o usuário ditou não é cortada para caber.** Se o roteiro ficou longo, entregue longo e diga a duração estimada.

#### A recompensa

A recompensa responde a pergunta do vídeo no nível da sacada, quando ela existe, ou no nível da notícia, quando não existe. Ela precisa de referente: tente dizer a mesma coisa com outras palavras, e se não der, é frase de efeito. Use uma destas quatro formas:

- **Um teste de bolso,** que o espectador aplica na própria vida: "Caro, em texto, e conferível. Quem bate nos três está na fila."
- **A revelação que fecha o gancho,** o número ou o fato que responde a pergunta: "A Sequoia entrou com cinco milhões e meio em 2024. Em maio a Enter valia um bilhão e duzentos."
- **Uma posição honesta:** "Eu não estou dizendo que ele está de má-fé, nem que isso é premeditado. Mas eu não gosto de sentir medo por causa de declaração solta, sem apontamento direto."
- **A consequência,** o que muda daqui pra frente por causa da sacada: "Se a dona do ChatGPT vende o mesmo produto que você, você não quer depender do cérebro dela."

#### O CTA

Um pedido só, em até três linhas, logo depois da recompensa. O roteiro acaba nele. Escolha o pedido pelo tipo de recompensa:


| A recompensa é…                                               | O CTA pede                                                                                                                             | Exemplo                                                                          |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| um teste ou uma regra prática                                 | que ele mande o vídeo para alguém específico (compartilhamento por DM é um dos sinais que mais levam um Reel a quem não segue a conta) | "Manda esse vídeo pra quem ainda paga plano anual de IA."                        |
| uma posição ou uma polêmica                                   | a resposta que ele já formou assistindo                                                                                                | "Você confia em benchmark que a própria empresa publica? Me conta aqui embaixo." |
| uma notícia explicada                                         | que ele siga a conta, com o motivo                                                                                                     | "Se você quer entender as notícias de IA sem o hype, me segue."                  |
| um tema que já tem artigo em `posts/substack/<slug>/final.md` | uma palavra-chave nos comentários                                                                                                      | "Comenta ARTIGO que eu te mando a versão completa."                              |


#### Provas na tela

Quando o roteiro cita algo que existe para ser mostrado (o post no X, o gráfico, a página de preço, a manchete), marque `[insert: o que mostrar]` numa linha própria, em qualquer bloco, logo depois da frase ou do tópico que aponta para ele. De zero a quatro por roteiro, só com artefato real. Quando a ideia traz o link da fonte, liste as fontes no rodapé do arquivo, uma por insert.

#### Formatação para o teleprompter

- Todo bloco abre com o cabeçalho e o modo numa linha própria: `[HOOK] · literal`, `[PROMESSA] · tópicos`, `[VIRADA] · literal`, `[DEGRAU] · tópicos`, `[RECOMPENSA] · literal`, `[CTA] · literal`.
- Bloco literal: uma frase ou um fôlego por linha. No teleprompter a quebra de linha marca respiração, não parágrafo.
- Bloco de tópicos: um tópico por linha, começando com `-` .
- Uma linha em branco entre blocos.
- **Sacada proposta pela skill** (4a, item 7, quando as notas só resumem o fato): todo bloco que só existe por causa dela, e a recompensa quando ela responde no nível da sacada, leva `· sacada proposta` no fim do cabeçalho. Exemplo: `[DEGRAU] · tópicos · sacada proposta`. Sacada que veio do usuário não leva marca.
- `[pause]` numa linha própria, só onde um beat precisa assentar: depois do gancho e antes de uma revelação.
- **Negrito em no máximo três lugares no roteiro inteiro, só em bloco literal,** na palavra cuja ênfase muda o sentido. Negrito em toda frase de efeito empurra a leitura para um "modo YouTuber" que afasta o espectador.
- O arquivo começa direto no `[HOOK] · literal`, sem cabeçalho, e termina num rodapé depois de uma linha `---`: a linha `Gravação: um take por bloco. Literal lido, tópicos falados olhando pra lente.` e, quando houver, as fontes dos inserts.

### Passo 6 · Leitura fria

Antes de apresentar, o roteiro passa pelos olhos de quem nunca viu a ideia. Quem acabou de ler as notas do Notion não enxerga o próprio jargão, então essa leitura não pode ser feita com as notas na cabeça.

- **Com a ferramenta de subagente disponível:** despache um subagente `general-purpose` passando **só o texto do roteiro**, sem a ideia e sem as suas notas, com o prompt abaixo.
- **Sem a ferramenta de subagente** (por exemplo, quando esta skill roda dentro de um agente do modo multitask): releia o arquivo do roteiro e responda você mesmo às mesmas perguntas, fazendo o papel de quem nunca viu a ideia.

```
Você é brasileiro, usa o ChatGPT de vez em quando e acha inteligência artificial um assunto
interessante, mas não trabalha com tecnologia. Você está rolando o Instagram e começa um Reel.
Abaixo está o roteiro do vídeo. Os blocos marcados "literal" são falados exatamente como estão
escritos. Os blocos marcados "tópicos" são as ideias que a pessoa vai explicar com as próprias
palavras, na ordem. Leia uma vez só, na ordem, imaginando o vídeo, sem voltar.

<roteiro>
[o roteiro como está no arquivo, sem as linhas [pause] e sem o rodapé, e com cada [insert: X]
trocado por (na tela: X)]
</roteiro>

Responda com franqueza. O objetivo é achar onde o vídeo perde gente, e também o que faz
ele valer a pena. Aponte só o que travou o seu entendimento ou te faria sair: o que você
entendeu não precisa ficar mais simples.
1. Depois da primeira frase, você continuaria assistindo? E depois do gancho inteiro? Que
   pergunta ficou na sua cabeça?
2. Liste cada palavra, sigla ou ideia que você não entendeu de primeira.
3. Em que ponto exato você arrastaria para o próximo vídeo, se arrastaria? Por quê?
4. O final respondeu a pergunta que o começo criou? Com o quê?
5. Conte o vídeo para um amigo em duas frases.
6. Algum tópico ficou vago demais para você imaginar o que a pessoa vai dizer? E alguma frase
   literal soa como texto escrito, e não como alguém falando?
7. Qual fato, número ou frase te fez querer continuar, ou você contaria para alguém?
8. Além do que aconteceu, o vídeo te deixou alguma ideia maior, que você não tinha antes? Qual?
```

A pergunta 8 só conta quando o roteiro tem sacada. Sem sacada, ignore a resposta dela.

Conserte o que a leitura apontar **traduzindo antes de cortar.** O material mais forte (4a, item 5) e o que o leitor citou na pergunta 7 ficam no roteiro: se confundiram, o que muda é a tradução deles.


| A leitura apontou                                  | Conserto                                                                                             |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| não continuaria, ou nenhuma pergunta ficou         | volte ao 4c: o gancho falhou em reconhecimento, aposta ou pergunta aberta                            |
| palavra que não entendeu                           | traduza na primeira menção (4a, item 4). Corte só o que não é material forte                         |
| arrastaria o dedo                                  | o trecho não abriu nada novo: reescreva a virada, ponha uma prova, ou corte o tópico                 |
| o final não respondeu                              | reescreva a recompensa numa das quatro formas                                                        |
| o resumo em duas frases saiu confuso               | a pergunta do vídeo não está clara: volte ao 4a, item 3                                              |
| o roteiro tem sacada, e nenhuma ideia maior chegou | reescreva o degrau da sacada. Se ela não se sustenta nem reescrita, tire a sacada e feche na notícia |
| tópico vago                                        | a pista não diz o que explicar: ponha nela a analogia, o exemplo ou o número escolhido               |
| frase literal de texto escrito                     | reescreva do jeito que o usuário falaria                                                             |


**A leitura fria roda no máximo duas vezes:** a primeira, e uma segunda só se o conserto trocou o gancho ou a recompensa. Depois disso, apresente. Um leitor novo sempre acha algo novo, e rodada demais vai tirando do roteiro justamente o que ele tem de concreto. O que a última leitura apontou e você decidiu manter vai para o usuário na apresentação.

### Passo 7 · Apresentar, iterar e salvar localmente

Derive o slug do título da ideia (minúsculas, hífens no lugar de espaços e caracteres especiais, sem acentos) e salve o roteiro na hora como `posts/script/<slug>/sketch/v1.md` com Write.

Apresente nesta ordem:

1. Uma linha de contexto: `Formato: <mistério | crença invertida | desmonte | aula em camadas> · Pergunta do vídeo: <a pergunta> · ~<M:SS> estimados` (a estimativa do Passo 5, em **Tamanho**).
2. O roteiro completo.
3. Os dois ganchos alternativos do 4c, numerados:
  > Ganchos alternativos:
  > 2) …
  > 3) …
4. Quando houver, os pontos **para conferir antes de gravar:** todo fato do roteiro que não veio da ideia (veio do seu conhecimento, e o usuário precisa checar), e o que a última leitura fria apontou e você decidiu manter. Cada ponto vira uma pergunta na ferramenta AskUserQuestion, feita depois da mensagem, com as opções manter, cortar e uma alternativa, e a sua recomendação marcada. São até quatro perguntas por chamada: se houver mais pontos, junte os do mesmo tipo. Sem essa ferramenta na sessão, liste os pontos em texto neste lugar da mensagem.
5. A pergunta:
  > "Pronto para finalizar, ou mais alguma correção?"
6. **O caminho do arquivo, numa linha própria, como o último elemento de toda a mensagem**: depois da pergunta, depois de todo o resto. Caminho relativo à raiz do projeto, para o usuário clicar, abrir o arquivo e voltar com correções:

```
posts/script/<slug>/sketch/v1.md
```

Para cada correção pedida:

- Aplique a mudança no roteiro.
- Crie `posts/script/<slug>/sketch/v(N+1).md`: leia a versão anterior, copie os blocos que não mudaram verbatim e aplique só o diff. Não regenere conteúdo que não mudou.
- Se o usuário escolher um gancho alternativo ("usa o 2"), troque o bloco `[HOOK]` na versão nova, e mexa na `[PROMESSA]` só se ela deixou de conversar com o gancho novo.
- Se o roteiro tem sacada proposta (blocos com `· sacada proposta`):
  - o usuário pediu para tirar: a versão nova remove os blocos marcados e reescreve a recompensa no nível da notícia;
  - o usuário deu outro ângulo: a sacada é reescrita em cima do ângulo dele, e sem marca, porque agora ela é dele;
  - o usuário só pediu outra tentativa: proponha outra sacada, com a marca;
  - o usuário corrigiu outra parte e não mexeu na sacada: ele aceitou, e a versão nova sai sem a marca.
- Pergunte de novo: "Pronto para finalizar, ou mais alguma correção?", e de novo feche a mensagem com o caminho novo (`posts/script/<slug>/sketch/v(N+1).md`) na última linha.

Repita até o usuário confirmar "pronto". Só então passe para o Passo 8.

### Passo 8 · Fechar

Se a versão de maior número ainda tem blocos marcados `· sacada proposta`, o "pronto" aceita a sacada: crie antes a versão seguinte, igual à anterior e só sem as marcas.

Quando o usuário confirmar "pronto", copie o `posts/script/<slug>/sketch/v<N>.md` de maior número para `posts/script/<slug>/final.md`. É uma cópia literal: leia esse arquivo e escreva o conteúdo dele em `final.md` verbatim, sem mudar nada. Faça isso antes de mexer no Notion: não é opcional e nada mais neste passo substitui isso. O histórico `sketch/v<N>` fica onde está, ele é a trilha de auditoria; `final.md` é a peça final, e o conteúdo mora localmente. Depois atualize a ideia de origem no banco Ideas: `Status` → `"Processed"` e `Format` → `"Reel"` (o formato que esta skill produz; a ideia nasce sem formato, e ele só é definido agora, na produção). Essa é a única escrita da skill no Notion. `Status` e `Format` acumulam no banco a foto real do calendário (fase e formato de cada peça produzida).

### Passo 9 · Confirmar e apontar o próximo passo

> "Roteiro pronto, salvo em `posts/script/<slug>/final.md`. Próximo passo: gravar o Reel com o teleprompter."

---

## Calibração

As frases desta seção já estão em roteiros do usuário. Copie os movimentos delas, com palavras novas.

### Um roteiro aprovado, bloco a bloco

Roteiro da Harvey (`posts/script/vender-o-trabalho-juridico-agora-paga-um-modelo-proprio/sketch/v3.md`), no formato híbrido: as frases literais são as do roteiro do usuário, e os tópicos resumem o que ele explicava no resto. Use para calibrar o registro, o trabalho de cada bloco e o tamanho de um tópico. O assunto e o formato do próximo roteiro saem do Passo 4, não daqui.

```
[HOOK] · literal
Todo mundo achou que o robô ia pegar a fábrica.
Pegou o **escritório de advocacia**.

[pause]

[PROMESSA] · tópicos
- 80% dos cem maiores escritórios de advocacia dos Estados Unidos já usam IA no trabalho
- e advogado era a profissão "blindada": diploma, anos de estudo

[VIRADA] · literal
A empresa chama Harvey.
Só que ela não vende um chatbot pro advogado escrever mais rápido, que é o que a gente imagina.

[DEGRAU] · tópicos
- ela pega a papelada inteira do caso, lê tudo, devolve a peça pronta
- o escritório compra o trabalho feito = igual compraria de um terceirizado
- setembro: levantou 550 milhões de dólares → treinou uma IA aberta só em direito

[VIRADA] · literal
Só que o direito não foi o primeiro porque é fácil.
Foi porque bate em três coisas.

[DEGRAU] · tópicos
- a hora de advogado é cara
- o trabalho todo é em cima de documento
- dá pra conferir se o resultado saiu certo

[pause]

[RECOMPENSA] · literal
Caro, em texto, e conferível.
Quem bate nos três **está na fila.**

[CTA] · literal
Roda esses três no seu trabalho.
Se bateu nos três, me conta nos comentários qual é a profissão.
Eu quero ver quantas aparecem aqui.

---
Gravação: um take por bloco. Literal lido, tópicos falados olhando pra lente.
```

O que cada bloco faz aqui:

- **HOOK · literal:** uma crença que todo mundo tem (robô toma a fábrica), virada ao contrário com uma profissão que ele conhece. Nenhum nome de empresa.
- **PROMESSA · tópicos:** o número que mostra que é sério e o que está em jogo (a profissão "blindada"). Ficam abertas as perguntas: por que advogado? E quem é o próximo?
- **VIRADA · literal:** o nome da empresa só aparece aqui, já desmontando a imagem que ele tem ("não vende um chatbot").
- **DEGRAU · tópicos:** o que ela faz, com a comparação que ele conhece (um terceirizado), e a rodada traduzida no que o dinheiro comprou. Uma ideia por linha, com os números escritos.
- **VIRADA · literal:** o segundo "só que" responde a pergunta que a promessa deixou (por que advogado?) e anuncia uma contagem, que prende até o terceiro item. Com dois "só que" ainda funciona. No terceiro, troque a forma.
- **DEGRAU · tópicos:** é o degrau da sacada. Os três critérios saem do caso da Harvey e viram um padrão que vale para qualquer profissão, um por linha, para o usuário explicar cada um do jeito dele. A sacada foi do usuário, então os blocos dela não levam marca.
- **RECOMPENSA · literal:** comprime os três critérios num teste de bolso que ele aplica no próprio trabalho.
- **CTA · literal:** pede exatamente o que a recompensa acabou de dar para ele fazer.

### Antes e depois: correções reais do usuário

Cada par é a primeira versão que esta skill entregou e o que o usuário gravou ou aprovou no lugar.

**Gancho**

> **v1:** "O mesmo teste deu dois vencedores em três dias. E nenhum dos dois modelos mudou."
> **Usuário:** "Três dias atrás o GPT-6 era a melhor IA do mundo. Hoje ele empata com o Claude. E nada no GPT-6 mudou."
> O título da ideia virou uma reviravolta com nomes que ele conhece.

> **v1:** "A Sequoia acabou de colocar cinco milhões e meio de dólares numa startup jurídica brasileira. E a tese por trás do cheque contraria vinte anos de Vale do Silício."
> **Usuário:** "Se você quer construir uma empresa de bilhões com IA, para de vender software. E quem está dizendo isso não sou eu."
> A notícia de mercado virou um conselho com algo em jogo e uma pergunta aberta (quem está dizendo?).

> **v1:** "Um pesquisador saiu da Anthropic dizendo que a IA pode matar todo mundo até o fim da década. E eu não comprei."
> **Usuário:** "A inteligência artificial pode acabar com a humanidade até o fim dessa década. [pause] Bom. Pelo menos é isso que diz um pesquisador que saiu da Anthropic essa semana."
> O que está em jogo vem antes da opinião de quem fala.

**Explicação**

> **v1 (traduzida do inglês):** "Primeiro: uma linha não é um modelo. É um modelo mais o harness que pilota ele."
> **Usuário:** "O modelo é o cérebro. Entra texto, sai texto. […] Ele não tem mãos. […] O harness é a mão. É o programa que envolve o modelo."
> A afirmação de especialista virou uma analogia que ensina o objeto.

> **v1:** "Jacob Coxon, matemático de Cambridge, trabalhou no GPT-4o na OpenAI e em pretraining na Anthropic."
> **Usuário:** cortou. "Um pesquisador que saiu da Anthropic" basta.
> Currículo é contexto de que a história não precisa.

> **v1:** "Chip que vende sozinho não precisa de banco montando o crediário do cliente."
> **Usuário:** "Não é dinheiro pra ela. É pra financiar os data centers que compram o chip dela e não têm caixa pra comprar nessa escala. A ideia é a GPU virar garantia de empréstimo, que nem imóvel." Só depois disso vem a frase, agora como pergunta: "Se o chip é tão bom assim, por que ela precisa montar o crediário do cliente pra vender?"
> O mecanismo explicado vem antes da frase esperta, e ela vira pergunta.

**Recompensa**

> **v1:** "Quem entrega o trabalho consegue descer e fazer o modelo. Quem faz o modelo não consegue subir e chegar no cliente."
> **Usuário:** "Caro, em texto, e conferível. Quem bate nos três está na fila."
> O aforismo de estrategista virou um teste que o espectador aplica no próprio trabalho.

> **v1:** "Eu não acho que ele mentiu. Acho que ele foi útil."
> **Usuário:** "Eu não estou dizendo que ele está de má-fé, nem que isso é premeditado. Mas eu não gosto de sentir medo por causa de declaração solta, sem apontamento direto."
> A frase de efeito virou uma posição honesta, com o limite dito.

**Sacada**

> **v1:** "Com a IA fazendo essa parte, o atalho perdeu o motivo, e voltou a valer a pena fazer um app sob medida pra cada celular."
> **Usuário (na revisão):** o vídeo devia mostrar que a IA está mudando o que vale a pena fazer: ganho pequeno que antes não compensava passa a compensar, e muito atalho e framework que só existia porque escrever código era caro perde o motivo.
> A conclusão ficou presa ao caso da Shopify. A do usuário sai do caso: diz o mecanismo (escrever código ficou barato) e onde mais ele bate.

**CTA**

> **v1:** "Antes de trocar de modelo por causa de ranking, abre o índice e olha só o sub-teste mais parecido com o que você faz no dia a dia."
> **Usuário:** "Pega a tarefa que você mais faz e roda nas duas. Em dez minutos você tem o único ranking que importa: o seu."
> A tarefa de profissional virou algo que qualquer um faz em dez minutos.

---

## Critérios de qualidade do roteiro

Confira antes de apresentar. Se algum item falhar, conserte antes.

- [ ] Todo bloco declara o modo no cabeçalho (`literal` ou `tópicos`), e cada bloco tem um modo só.
- [ ] A pergunta do vídeo cabe numa frase, e a `[RECOMPENSA]` responde ela.
- [ ] O `[HOOK]` passou nas seis perguntas do 4c, e a primeira frase sozinha segura o dedo.
- [ ] Todo `[DEGRAU]` vem logo depois de uma `[VIRADA]`, e as viradas variam de forma.
- [ ] Todo tópico é a pista de uma ideia, sem frase completa.
- [ ] Nenhum termo técnico chega sem tradução na primeira menção, nem dentro de tópico.
- [ ] Todo degrau carrega pelo menos um fato conferível, com número e nome escritos como devem ser ditos.
- [ ] Toda frase literal e todo tópico ensina, prova ou abre a próxima pergunta.
- [ ] Se tem sacada: ela está no último degrau, passou no teste de sacada boa e, se foi proposta pela skill, os blocos dela estão marcados. Se não tem, o roteiro fecha bem na notícia.
- [ ] A recompensa é um teste, uma revelação, uma posição ou uma consequência, e tem referente.
- [ ] Um CTA só, escolhido pela recompensa, e o roteiro acaba nele.
- [ ] A leitura fria rodou (no máximo duas vezes), e o que ela apontou foi consertado sem tirar o material mais forte.
- [ ] Todo fato que não veio da ideia foi levado ao usuário nos pontos para conferir antes de gravar.
- [ ] As frases literais soam como o usuário falando.
- [ ] Negrito em no máximo três lugares, só em bloco literal.
- [ ] O rodapé tem a linha de gravação e, quando houver, as fontes dos inserts.

---

## Fora do escopo

Esta skill não faz:

- Captura de ideias cruas (isso é a skill `registrar-ideia`).
- Adaptação para LinkedIn ou Instagram, a menos que o usuário peça outro formato explicitamente.
- Publicação.
- Análise de desempenho.

