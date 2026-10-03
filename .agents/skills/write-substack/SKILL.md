---
name: write-substack
description: >
  Produz um artigo ilustrado completo para o Substack: uma história sequencial com
  espinha narrativa de verdade, 3 a 8 imagens capturadas ao vivo de fontes primárias
  no navegador, e um título feito para ser aberto. Parte de uma tese que já saiu como
  Reel, de uma notícia recém-saída ou de uma ideia crua. Ative com comandos como
  "escreve o Substack da semana", "transforma <slug> em artigo",
  "escreve o artigo do Substack sobre <notícia>".
---

# SKILL · write-substack
## Produção · Artigo de Substack (texto longo + imagens capturadas)

Propósito: produzir um **artigo acabado**, daqueles que um leitor com base técnica escolhe gastar vinte minutos lendo e encaminha para alguém. Não é um post longo. É um artigo: uma história que anda em sequência, sustentada por imagens capturadas da coisa real.

Três propriedades separam o que esta skill publica de tudo o mais que sai deste repositório:

1. **Roda numa espinha narrativa, não numa estrutura de argumento.** O leitor acompanha alguém descobrindo alguma coisa, na ordem.
2. **É ilustrado com capturas reais.** De três a oito imagens, cada uma printada de uma fonte primária no navegador, cada uma colocada onde o texto acabou de levantar a pergunta que ela responde.
3. **Não tem teto de tamanho.** Acaba quando o material acaba.

---

## Para que serve este canal

Instagram e LinkedIn são audiência alugada. O Substack é a **lista própria**: o único canal aqui em que o leitor entrega um endereço e pode responder direto para você.

| | Instagram / LinkedIn | Substack |
|---|---|---|
| Métrica que importa | alcance, reações | **taxa de abertura e respostas** |
| Estado do leitor | rolando o feed, frio | optou por entrar, com vinte minutos disponíveis |
| O que ganha o clique | um hook que cria tensão | um **título que vale uma noite** |
| O que a peça carrega | a conclusão | **o caminho inteiro até ela, mostrado** |
| Papel no ACP | A · Audience → C · Community | **C · Community → P · Product** |

As respostas são o produto deste canal. O mesmo problema nomeado em trinta respostas é o próximo workshop, a próxima oferta, a próxima coisa que vale construir. Escreva mirando a resposta.

## A regra que impede isso de virar um post longo

**O LinkedIn publica a conclusão. Aqui sai o caminho.**

Um artigo que chega à mesma conclusão pela mesma estrada, com mais parágrafos, falhou. O que os formatos curtos não conseguiram carregar é a sequência: o primeiro palpite errado, o número que quebrou ele, a página que você foi ler de verdade, a coisa que você tentou e não funcionou.

Dois testes concretos, aplicados no Passo 5 e de novo no fim:

- **O teste do artefato.** O artigo carrega pelo menos uma coisa que não caberia num post de LinkedIn: uma figura capturada, um bloco de código, um log ou trace real, uma tabela, uma série de números.
- **O teste da sequência.** Leia só os headings das seções, na ordem. Se eles não soam como uma coisa acontecendo depois da outra, a peça é um argumento vestido de artigo. Reescreva a espinha.

---

## Notícia é assunto legítimo

Material perecível é bem-vindo aqui, e muitas vezes é o melhor assunto disponível. Nada neste formato exige tese perene.

**Mas notícia só vira artigo por reconstrução.** Um resumo do que foi anunciado não é artigo, e o leitor já viu quatro desses. O que torna o texto seu é a distância entre o que a cobertura disse e o que o documento primário diz de fato, lido na página 14, capturado e colocado ao lado da manchete. Essa é a espinha de **reconstrução** do Passo 4, e é a que mais depende de imagem entre as quatro. Se você não consegue chegar a uma fonte primária, não existe artigo: diga isso em vez de escrever o quinto resumo.

---

## Ferramentas disponíveis

**MCP do Notion**: para ler o banco **Ideas** e, no caminho standalone, para atualizar `Status` e `Format` no fechamento.

**Automação do navegador Chrome** (`mcp__claude-in-chrome__*`): o motor de captura, usado ao longo de uma sessão inteira no Passo 7. Essas ferramentas são carregadas sob demanda (deferred): invoque a skill `claude-in-chrome` antes de chamar qualquer uma delas.

---

## Referências obrigatórias

**A voz, em toda rodada:** escreva como o usuário fala e pensa - posição primeiro, autor exposto, opinião com referente concreto. Sem jargão sem tradução, sem inflação.

**O que já existe sobre esta tese, quando existe:**

| Arquivo | Por quê |
|---|---|
| `posts/script/<slug>/final.md` | O Reel que carregou a ideia. Leia para o artigo não repetir o enquadramento dele, e para achar o que a versão de 60 segundos teve que jogar fora. |
| `posts/linkedin/<slug>/final.md` | Só se já existir. Leia para saber o que evitar: nenhuma frase passa verbatim. |

**Calibração, em toda rodada:**

| Fonte | O que você está lendo ali |
|---|---|
| `posts/substack/*/final.md`, os artigos já publicados aqui | O estilo da casa como ele está de fato, inclusive como as imagens são colocadas e legendadas. Leia os dois mais recentes. Na primeira rodada não existe nenhum; pule em vez de inventar um. |
| `.agents/skills/build-linkedin/examples/` | Registro da prosa no nível da frase: densidade de parágrafo, conectivos reais, um nome próprio ou número a cada duas ou três frases, o autor exposto. **O assunto deles é irrelevante.** |

Não existe documento de audiência nem de pilar de conteúdo, de propósito. Se a peça precisar de um leitor-alvo ou de um ângulo, pergunte ao usuário.

---

## Quando agir

- "escreve o Substack da semana"
- "transforma `<slug>` em artigo"
- "escreve o artigo do Substack sobre [algo que aconteceu esta semana]"
- "escreve a versão em artigo do reel sobre X"
- qualquer variação que signifique uma peça longa e ilustrada de newsletter

---

## Dois caminhos de entrada

Eles só diferem no Passo 1 e no Passo 9.

**Caminho de reuso.** Uma tese que já saiu em outro formato, geralmente um Reel, às vezes um post de LinkedIn, levada a fundo. O `final.md` irmão existe em `posts/`, e a ideia de origem já está `Processed` no Notion, carregando aquele formato. **Este caminho não escreve nada no Notion.**

**Caminho standalone.** Uma ideia nova do banco Ideas, ou uma notícia que o usuário traz direto. Sem irmãos. Este caminho fecha a ideia no Notion no Passo 9.

---

# Protocolo de execução

## Passo 1 · Identificar o assunto

**Caminho de reuso.** O usuário nomeia um slug. Se não nomeou, liste os slugs mais recentes em `posts/script/` e `posts/linkedin/` por mtime, mostre e pergunte qual vai virar artigo.

Escolha pela **profundidade do material disponível**, nunca pela força do hook. O assunto certo é aquele em que você consegue nomear, antes de escrever uma palavra, pelo menos três coisas que daria para ir capturar.

**Caminho standalone.** Se for notícia que o usuário trouxe, pegue direto. Senão, abra o banco **Ideas** (`e2970ca3-7724-4a81-8f12-7ea34c048c67`), filtre `Status = "Pending"`, ordene por `Date` decrescente (na falta, `createdTime`) e confirme a mais recente:

> "Ideia selecionada para o artigo: [título]. Sigo com essa?"

## Passo 2 · Ler tudo, e separar

**Caminho de reuso.** Leia `posts/script/<slug>/final.md` inteiro, mais a linha da ideia no Notion. Depois monte duas listas explícitas, nas suas notas de trabalho:

- **Queimado**: toda afirmação, exemplo e virada de frase que a audiência já viu no Reel. O artigo pode chegar à mesma conclusão, nunca pelas mesmas frases.
- **Cortado por tempo**: a ressalva que não coube em 60 segundos, o segundo exemplo, o número que precisava de um gráfico, a coisa que você tentou primeiro e falhou, a fonte que você leu mas não dava para citar falando. **Isso é o artigo.**

Se o "cortado por tempo" for magro, o assunto é magro. Diga isso e proponha outro slug em vez de encher linguiça.

**Caminho standalone.** Leia a ideia inteira. Depois, antes de qualquer outra coisa, **vá atrás das fontes primárias**. Para notícia, isso quer dizer o post do anúncio, o model card, o paper, a página de preços, o changelog, o repositório, não a cobertura. Você não consegue planejar o artigo sem saber o que esses documentos dizem de fato, e na espinha de reconstrução a distância entre eles e a cobertura *é* o artigo.

## Passo 3 · Calibração de voz

Leia as fontes de calibração em **Referências obrigatórias**: os exemplos mostram como a voz fica numa página.

## Passo 4 · Planejar: espinha, depois outline, depois shot list

**Este passo acontece antes de qualquer frase do artigo ser escrita, e é apresentado ao usuário antes de escrever.** As imagens não são decoração acrescentada no fim: o texto é escrito para preparar cada uma delas, então a shot list precisa existir primeiro.

### 4a · Escolher uma espinha narrativa

Toda espinha abaixo é **sequencial**: é uma coisa acontecendo depois da outra, não um conjunto de pontos. É essa a diferença entre um artigo e um post longo.

---

**1 · A investigação** - *alguma coisa quebrou e você descobriu por quê*

1. Uma cena concreta, datada, com um número dentro. Não uma tese.
2. A primeira leitura errada, e por que ela era razoável: é aqui que o leitor se reconhece.
3. A evidência que não encaixou. **A primeira imagem costuma cair aqui.**
4. A descida: um passo por seção curta, cada uma com a própria captura.
5. A virada: o que estava acontecendo de verdade.
6. O que isso significa fora do seu caso, e onde deixa de ser verdade.
7. A objeção real, respondida.
8. A pergunta.

Use quando você viu algo falhar de perto o bastante para reconstruir.

---

**2 · A reconstrução** - *isto é o que aconteceu de fato* · **a espinha de notícia**

1. O que foi anunciado, em uma frase, sem adjetivo.
2. O que a cobertura disse que aquilo significava. **Imagem: a manchete, o gráfico do post de anúncio.**
3. O que o documento primário diz de fato. **Imagens: a página do paper, o model card, a tabela de preços, o default da config.** Esse é o centro de gravidade da espinha: espere três ou quatro capturas aqui.
4. A distância entre 2 e 3, nomeada sem rodeio.
5. O que muda na prática, com números.
6. O que ainda não dá para saber, dito com honestidade.
7. A pergunta.

Use quando alguma coisa aconteceu esta semana. **Exige fontes primárias.** Sem elas, não escreva.

---

**3 · O teste** - *você rodou, e foi isto que aconteceu*

1. A pergunta que você queria responder, e por que ela importa para quem faz esse trabalho.
2. O setup, com as limitações admitidas logo de cara. **Imagem: o ambiente, a config, o prompt.**
3. O que aconteceu, na ordem em que aconteceu. **Imagens: os resultados, e os erros. As falhas são mais interessantes que os acertos e também são capturadas.**
4. O resultado que você não esperava.
5. O que você mudaria no próprio teste.
6. A pergunta.

Use quando você tem acesso à coisa e consegue rodar de verdade.

---

**4 · A decisão** - *A ou B, e o que custou*

1. O que estava em jogo, e o prazo que forçou a escolha.
2. As opções, com honestidade, com o preço de cada uma. **Imagens: a comparação, a documentação, os preços.**
3. O que você quase escolheu, e por que era tentador.
4. O que você escolheu, e o que te custou.
5. O que faria você voltar atrás.
6. A pergunta.

Use quando você pagou por uma escolha. É a espinha em que o autor mais se expõe.

---

**A regra do encadeamento, seja qual for a espinha:** toda seção termina abrindo a pergunta que a próxima responde. Leia seus headings na ordem: se você não quiser ler o próximo, a sequência está frouxa.

### 4b · Fazer o outline

De cinco a nove seções. **Headings são frases, não rótulos**: "O retrieval nunca foi o problema", não "Análise". Um leitor que escaneia só os headings tem que sair com a história.

Escreva uma linha por seção dizendo o que acontece nela. Se duas seções vizinhas dizem o mesmo tipo de coisa, junte as duas.

### 4c · Montar a shot list

Antes de abrir o navegador, escreva a shot list como tabela em `posts/substack/<slug>/sketch/shotlist.md`:

| # | Âncora - a frase depois da qual ela entra | O que precisa mostrar | Onde capturar | Status |
|---|---|---|---|---|
| cover | - | o mecanismo de que o artigo trata | arXiv fig. 2 | planejada |
| 01 | "o custo triplicou sem o tráfego se mexer" | a curva de custo, com o eixo log visível | a página de status do provedor | planejada |

Regras para a lista:

- **De três a oito imagens**, mais a capa. Uma imagem a cada 250 a 400 palavras é o ritmo certo. Menos de três num artigo longo vira paredão de texto; mais de oito vira apresentação de slides.
- **Toda imagem responde a uma pergunta que o texto acabou de fazer.** Se você não consegue escrever a frase-âncora, você não precisa da imagem.
- **Toda imagem tem uma fonte real, com link.** Se você não consegue dizer onde iria capturar, ela não entra na lista.
- **Capture as falhas também**, na espinha de teste: uma mensagem de erro é mais crível que um print de sucesso.

### 4d · Apresentar o plano

Mostre ao usuário a espinha, o outline e a shot list antes de escrever:

> "Espinha: [nome]. Outline: [headings]. Shot list: [N imagens, fontes]. Quer mudar alguma coisa antes de eu escrever?"

É o lugar mais barato da rodada inteira para mudar de direção. Não pule.

## Passo 5 · Escrever o artigo

### O título

**O título é o produto**: a linha de assunto do email, o card do feed, a única coisa que a maior parte da lista chega a ver.

O título declara a **tese ou a descoberta**, nunca o tema:

- **O reenquadramento:** "Compliance é um problema de dados fantasiado de jurídico"
- **A negação:** "Por que a sua primeira contratação em IA não deveria ser um engenheiro de ML"
- **O custo nomeado:** "Quanto custa de verdade o humano no loop a 40.000 documentos por mês"
- **A reconstrução:** "O que o model card do GPT-5 diz na página 14"
- **O fato seco**, quando o fato é notícia de verdade e é seu de verdade

**Nunca:** o formato tema-dois-pontos-promessa ("RAG em escala: um guia prático"), que é blog corporativo e soa como um. Número de listicle. Pergunta que o artigo não responde. Qualquer coisa que o leitor não consiga entender sem abrir o email.

### O subtítulo

O Substack mostra ele embaixo do título e no preview do email. **Ele não repete o título**: acrescenta a consequência, o custo ou o escopo que o título deixou implícito. Uma frase. Se apagar ele não perde informação, reescreva.

### A abertura

**Abertura fria, numa cena.** O primeiro parágrafo é um momento específico com um número específico dentro, não uma afirmação geral com exemplos embaixo.

Proibidos, todos: "Na edição desta semana", "Bem-vindo de volta", qualquer saudação, qualquer resumo do que vem, qualquer pigarro, qualquer definição de termo que o leitor já conhece.

### O corpo

Escreva seguindo o outline, e **prepare o terreno para cada imagem**. As duas ou três frases antes de uma imagem dizem ao leitor o que ele vai olhar e por que importa; a frase depois diz o que ele leva. Imagem jogada sem preparação é decoração, e o leitor rola por cima.

Marque a posição das imagens inline enquanto escreve:

```
![01 - <caption placeholder>](01.png)
```

O Substack renderiza markdown, que é o oposto da restrição do LinkedIn. Use, e use para o que o LinkedIn não conseguia segurar:

- `##` para heading de seção
- Blocos de código com fence: reais, curtos, executáveis ou coláveis. Não pseudocódigo fazendo as vezes de uma ideia.
- Tabelas, quando duas coisas ficam no mesmo eixo e a comparação é o ponto
- Blockquote para uma linha de log real, trecho de trace, mensagem de erro ou fonte citada
- Links inline, **pelo menos três verificáveis**: o paper, o repositório, a página da documentação, o benchmark
- `**negrito**` com parcimônia: para um termo sendo definido, não para uma frase de que você gostou

Parágrafos desenvolvem uma ideia em algumas frases ligadas por conectivos reais; o parágrafo de uma frase só é beat raro. A rolagem de uma frase por linha é artefato de feed; num email, soa como alguém sem nada para dizer.

**Antecipe uma objeção real e responda.** Neste tamanho, um leitor que discorda tem tempo de montar o contra-argumento. Chegue antes, formule com justiça e diga o que mudaria a sua opinião.

### Tamanho

**De 1.200 a 3.000 palavras é o corpo normal de um artigo aqui, e não existe teto quando o material aguenta.** Uma peça de 4.000 palavras sustentada por seis capturas, uma tabela e uma decisão pela qual você pagou é um bom artigo. Uma peça de 1.400 palavras feita só de raciocínio está enchendo linguiça já nas 1.400.

A regra de trabalho: **a cada 400 palavras entra alguma coisa nova e checável**: um número, um nome, uma captura, uma citação, um link. Trecho que não entrega isso é cortado, por mais bem escrito que esteja.

### O fecho

**O fecho pede a resposta.** Numa lista própria, a resposta é o objetivo inteiro, e quarenta respostas valem mais que três mil reações. É o único lugar em que o formato quebra de propósito a regra do LinkedIn de não pedir nada.

A pergunta tem que merecer:

- Uma que **você de verdade não consegue responder** e um leitor qualificado consegue.
- Que peça **o material dele, não a opinião dele**: "O que o seu time faz quando a suíte de evals discorda do cliente?", não "O que você acha?".
- Depois que a história assentou, não no lugar dela.

**Sem CTA de assinatura no corpo**: o Substack injeta o dele. **Sem bloco de despedida**, sem "até semana que vem", sem despejo de links. Termine na pergunta.

### Formato da saída

```
# <título>
### <subtítulo>

<o artigo, com os marcadores ![NN - caption](NN.png) no lugar>
```

Depois, um rodapé de metadados: não é texto publicável, é o registro da peça, e vai junto para o `final.md`:

```
---
Palavras: <contagem>
ACP: <fase>
Espinha: <investigação | reconstrução | teste | decisão>
Artefato: <a coisa que não caberia num post de LinkedIn>
Imagens: <N>, ver shotlist.md
Fontes: <as fontes primárias usadas, como URLs>
Reuso de: <slug>   <- só no caminho de reuso
```

## Passo 6 · Apresentar, iterar, salvar

Apresente o artigo completo com título, subtítulo, contagem de palavras e os marcadores de imagem no lugar.

Derive o slug do título (minúsculas, hífens no lugar de espaços e pontuação, sem acentos). No caminho de reuso, **reaproveite o slug do irmão**, para a tese morar sob um nome só em `posts/script/`, `posts/linkedin/` e `posts/substack/`.

Salve na hora como `posts/substack/<slug>/sketch/v1.md`.

Pergunte:

> "Pronto para travar o texto e ir capturar as imagens, ou correções antes?"

Para cada correção: aplique, recalcule a contagem de palavras e crie `posts/substack/<slug>/sketch/v(N+1).md`: leia a versão anterior, copie os blocos que não mudaram **verbatim** e aplique só o diff. Nunca regenere o que não mudou.

**Ofereça uma passada no título explicitamente, uma vez, antes de travar.** O título carrega mais do resultado desta peça do que qualquer parágrafo, e é o que o usuário tem mais chance de aceitar sem pensar:

> "Três alternativas antes de travar: [A] / [B] / [C]. Fica com o atual?"

Trave o texto antes do Passo 7. Capturar contra um rascunho em movimento desperdiça a sessão.

## Passo 7 · A sessão de captura

Invoque a skill `claude-in-chrome`. Trabalhe numa **aba nova** (`tabs_create_mcp`). Percorra a shot list de cima a baixo numa sentada só.

### 7a · Inegociáveis

- **Toda imagem é uma captura real de uma página ao vivo.** Nunca fabrique uma, nunca monte uma em HTML, nunca use imagem gerada por IA, nunca use stock. É nessa regra que a credibilidade do canal se apoia.
- **Fonte primária, sempre.** O paper no arXiv em vez de um blog citando ele. A página de preços em vez de um print da página de preços. O repositório em vez do tweet sobre o repositório. Print de tweet nunca é evidência de um fato: vá até o que o tweet cita.
- **Nada atrás de paywall, nada privado.** Sem dado de cliente, sem dashboard interno, sem tela logada com informação de alguém.
- **A URL da fonte é registrada em toda captura**, na shot list, no momento da captura. Captura sem URL não tem crédito e não sai.

### 7b · Técnica de captura

- **Dê zoom antes de capturar**, não capture aberto para cortar depois: cortar joga fora a resolução que deixa os rótulos legíveis.
- **Enquadre o elemento, não a página.** Sem interface do navegador, sem barra de navegação, sem sidebar, sem banner de cookie, sem scrollbar, sem seção vizinha aparecendo pela metade.
- **Feche os banners primeiro**, depois capture. Aviso de cookie no canto passa descuido.
- **Escolha o tema de maior contraste** quando a página oferece os dois: em geral o claro, para texto e figuras.
- **Zoom do navegador em 125 a 150% para capturas cheias de texto** (um parágrafo de paper, uma config, um log). No zoom padrão sai um texto que ninguém lê num email.

### 7c · Checagem por imagem, antes de seguir

Cada captura passa nas cinco ou é refeita:

1. **Legível a 50% da largura**: é mais ou menos assim que ela aparece no cliente de email do celular.
2. **Uma ideia visível.** Se o leitor precisa caçar o que você quis dizer, corte mais apertado.
3. **Nada sobrando**: sem interface de navegador, sem marca d'água, sem marca de terceiros sem relação.
4. **Ela responde à frase-âncora.** Leia a âncora, olhe a imagem. Se não encaixa, o take estava errado, não o corte.
5. **A URL está registrada.**

### 7d · A capa

A capa aparece no topo do email, no card do feed e no card de compartilhamento social, cortada em mais ou menos 2:1. Então: **paisagem, larga, nada essencial no sexto externo, legível pequena, alto contraste, poucos elementos.**

A capa mais forte é quase sempre **o mecanismo de que o artigo trata, desenhado**: o leitor reconhece o próprio sistema antes de ler uma palavra. Senão: o gráfico com a forma surpreendente, o print do artefato real, a figura do paper citado.

Muitas vezes a melhor capa é um take que já está na sua lista. Reaproveitar um é bom, e melhor que uma capa dedicada fraca.

Se já existe um post de LinkedIn sobre esta tese e `posts/linkedin/<slug>/image.png` está lá, mostre e pergunte se reaproveita. **Nunca reaproveite em silêncio.**

### 7e · Quando um take não existe

Se uma captura planejada não tem fonte real depois de algumas tentativas honestas, **muda o texto, não a imagem**. Reescreva aquela passagem para ela não depender da figura, e risque a linha da shot list. Nunca coloque uma imagem decorativa para preencher a vaga. Diga o que caiu e por quê.

### 7f · Salvar e registrar

Salve na raiz do slug, ao lado do `final.md` com que elas saem, não em `sketch/`:

- `posts/substack/<slug>/cover.png`
- `posts/substack/<slug>/01.png` … `NN.png`, numeradas na ordem de leitura

Atualize `sketch/shotlist.md`: toda linha recebe o status final e a **URL da fonte**.

## Passo 8 · Legendar, posicionar e revisar os pares

Agora o artigo e as imagens existem. É neste passo que uma peça boa vira uma peça acabada: não pule.

### 8a · Escrever as legendas

Toda imagem ganha uma legenda com dois trabalhos:

1. **O que olhar**, em uma oração. Não uma descrição da imagem, uma direção. "O eixo Y é log; a queda entre 8k e 32k tokens é a parte que o gráfico do anúncio deixa de fora."
2. **A fonte, com link.** "- [OpenAI, GPT-5 model card, p.14](url)"

Legenda que só nomeia a imagem ("Figura 2: a arquitetura") é espaço jogado fora. Se a imagem precisa creditar a figura de um paper, credite aqui; o Substack tem o espaço que o LinkedIn não tem.

### 8b · Ler o artigo com as imagens no lugar

Leia de ponta a ponta como um leitor leria, e cheque três coisas:

- **Toda imagem tem preparação**: as frases antes montam a cena, a frase depois diz o que levar.
- **O ritmo segura.** Nenhuma dupla de imagens coladas com uma frase entre elas. Nenhum trecho de 900 palavras sem nada para olhar.
- **Nada redundante.** Se a legenda diz o que o parágrafo já disse, corte um dos dois.

Escreva as correções num novo `sketch/v(N+1).md`, com as legendas reais no lugar dos placeholders.

### 8c · Apresentar o conjunto

Mostre ao usuário o artigo e cada imagem com a legenda. Pergunte:

> "Artigo e [N] imagens. Alguma coisa para refazer ou reescrever?"

Se uma imagem for rejeitada, volte ao 4c e responda de novo *o que esta imagem precisa mostrar?* antes de recapturar: uma segunda tentativa com a mesma premissa erra do mesmo jeito.

## Passo 9 · Fechar

Tudo mora em `posts/substack/<slug>/`. `sketch/` é material de trabalho; a raiz é exatamente o que sai:

| Arquivo | O que é | Escrito por |
|---|---|---|
| `final.md` | cópia do `sketch/v<N>.md` de maior número | esta skill, agora |
| `cover.png` | a capa do Passo 7d | esta skill, no 7f |
| `01.png` … `NN.png` | as capturas do corpo, na ordem de leitura | esta skill, no 7f |

`sketch/` guarda `v<N>.md` e `shotlist.md` como trilha de auditoria. Se o usuário editar um `sketch/v<N>.md` depois, copie de novo para `final.md`.

**Notion, por caminho:**

- **Caminho de reuso: não escreva nada.** A ideia foi fechada pelo Reel e carrega um único `Format`. Escrever `Substack` por cima apagaria o formato primário e corromperia a foto do calendário que o banco acumula. Diga que está pulando a escrita, e por quê.
- **Caminho standalone:** `Status` → `"Processed"` e `Format` → `"Substack"`. Se `Format` não tiver a opção `Substack`, **pare e peça ao usuário para adicionar na interface do Notion**. Não adicione pelo MCP: editar o conjunto de opções de uma propriedade select por ali substitui o conjunto inteiro e apaga em silêncio o valor de toda linha (veja o `AGENTS.md`).

## Passo 10 · Entregar

> "Artigo pronto: [título], [N] palavras, [N] imagens. Está tudo em `posts/substack/<slug>/`.
> Para publicar: cole o `final.md` no editor do Substack, depois arraste cada PNG para cima do marcador `![NN - …]` dele e cole a legenda embaixo. Defina `cover.png` como capa do post."

---

## Critérios de qualidade

**A história**
- O título declara uma tese ou uma descoberta, sem promessa depois de dois-pontos e sem número de listicle
- O subtítulo acrescenta a consequência ou o custo em vez de repetir o título
- Abre frio, numa cena específica com um número, não numa afirmação geral
- Uma espinha foi escolhida, e os headings das seções, lidos na ordem, contam essa história
- Toda seção termina abrindo a pergunta que a próxima responde
- Uma objeção real é nomeada com justiça e respondida, com o que mudaria a opinião do autor
- O fecho faz uma pergunta que o autor de verdade não consegue responder, pedindo o material do leitor em vez da opinião dele
- Sem CTA de assinatura e sem bloco de despedida no corpo

**As imagens**
- De três a oito imagens no corpo mais uma capa, mais ou menos uma a cada 250 a 400 palavras
- **Toda imagem é uma captura real do navegador, de fonte primária.** Sem stock, sem arte gerada por IA, sem diagrama montado em HTML, sem print de tweet no lugar de um fato
- Toda imagem cai onde o texto acabou de levantar a pergunta que ela responde, com preparação antes e conclusão depois
- Toda imagem é legível a 50% da largura, enquadrada no elemento, sem interface de navegador, banner ou marca d'água
- Toda imagem tem uma legenda que dirige o olhar e linka a fonte
- A capa é paisagem, sobrevive ao corte 2:1 e mostra o assunto real do artigo
- Toda URL de fonte está registrada em `sketch/shotlist.md`

**O que faz disso um artigo**
- Carrega pelo menos um artefato que não caberia num post de LinkedIn
- Pelo menos três links inline que o leitor pode ir verificar
- A cada 400 palavras entra alguma coisa checável: um número, um nome, uma captura, uma citação
- No caminho de reuso, nenhuma frase passa verbatim do Reel, e o material é o que a versão de 60 segundos teve que cortar

**A voz**
- O tamanho dos parágrafos varia; o parágrafo de uma frase só é um beat raro, não o padrão
- As frases dentro de um parágrafo são ligadas por conectivos reais, não empilhadas
- Toda seção carrega um nome próprio ou um número que o leitor pode verificar
- O autor está exposto em algum lugar: uma decisão tomada, um preço pago, um primeiro palpite errado admitido
- Sem hype, sem registro motivacional, sem jargão sem explicação

**Os arquivos**
- A raiz de `posts/substack/<slug>/` tem `final.md`, `cover.png` e `01.png`…`NN.png`
- `sketch/` tem o histórico `v<N>.md` e o `shotlist.md` com toda URL de fonte
- O Notion só foi escrito no caminho standalone

Se algum critério falhar, conserte antes de apresentar.

---

## Fora do escopo

- Não captura ideias cruas (isso é `registrar-ideia`)
- Não escreve roteiro de Reel, carrossel, thread nem post de LinkedIn: cada um tem a própria skill
- Não desenha nem gera arte. Toda imagem é capturada de algo que já existe. Uma peça que precisa de arte composta no sistema Alvinegro é um carrossel, não um artigo
- Não publica: colar no Substack é manual
