# Formatos de conteúdo

Este documento registra os formatos editoriais que o projeto produz hoje. A lista parte das skills de produção e separa três coisas que não são equivalentes:

- **formato** é a peça publicável;
- **modo** é uma variação narrativa, de densidade ou de edição dentro do formato;
- **derivado** reapresenta uma peça que já existe e não cria um novo formato canônico no banco Ideas.

## Reel — Canal Principal: Instagram

Vídeo curto de talking head. A ideia vira uma história guiada por uma pergunta, com roteiro híbrido de trechos literais e tópicos para preservar, ao mesmo tempo, retenção e naturalidade na fala.

O formato é escrito pela skill `write-script`. O vídeo é produzido com Hyperframes. A entrega completa mora em `posts/script/<slug>/`: roteiro (`final.md`), vídeo (`reels.mp4`), legenda (`caption.md`) e capa (`cover.png`). No banco Ideas, o valor de `Format` é `Reel`.

### Modos e variações atuais

**Formato da história no roteiro:**

- **Mistério:** parte de um fato que contradiz a expectativa e avança por pistas até a revelação.
- **Crença invertida:** derruba uma crença comum, prova a inversão e entrega uma regra prática.
- **Desmonte:** examina de perto uma promessa, anúncio ou alerta que está circulando e explicita a posição do autor.
- **Aula em camadas:** ensina as peças necessárias para entender um assunto e as conecta numa regra final.

**Modo de fala dos blocos:**

- **Literal:** hook, viradas, recompensa e CTA são falados exatamente como foram escritos.
- **Tópicos:** promessa e degraus funcionam como pistas para uma explicação natural.

Esses modos mudam a narrativa, mas a peça continua sendo um Reel.

## Carrossel editorial — Canal Principal: Instagram

Sequência visual nativa em que copy e arte são produzidas como uma entrega única. Cada slide sustenta uma conclusão, e a leitura das headlines em sequência deve formar um argumento coerente. A peça usa proporção 4:5, tem no máximo dez slides e inclui capa e CTA.

A skill `carousel` produz o formato completo em `posts/carousel/<slug>/`: `final.md` com a copy e a legenda, mais `01.png` a `10.png`. No banco Ideas, o valor de `Format` é `IG Carousel`.

### Modos atuais

- **Reconhecimento:** cerca de uma frase e 20 palavras por slide, tipografia grande e leitura rápida; busca identificação e compartilhamento.
- **Leitura:** até cerca de 60 palavras por slide, com informação suficiente para justificar o salvamento.

O modo de densidade vale para a peça inteira; misturar os dois enfraquece a hierarquia.

## Thread — Canal Principal: Threads

Sequência de textos encadeados para o Threads. Cada publicação precisa funcionar isoladamente e, ao mesmo tempo, mover o argumento da sequência. A faixa típica é de cinco a nove posts, com limite de 500 caracteres por post.

A skill `write-thread` salva a peça em `posts/thread/<slug>/final.md`. No banco Ideas, o valor de `Format` é `Thread`.

### Variações atuais

- **Sequência curta:** cinco ou seis posts para um ponto, uma provocação ou uma observação rápida.
- **Sequência média:** sete a nove posts para um argumento com exemplo, derrubada de mito ou framework simples.
- **Sequência longa:** dez ou mais posts quando existem vários exemplos ou camadas; é rara e, acima de doze, a ideia provavelmente pede Reel ou carrossel.

Essas variações regulam o tamanho. A estrutura permanece hook, desenvolvimento e fecho.

## Carrossel derivado de thread — Canal Principal: Instagram

Adaptação visual de uma thread já escrita. A copy pode ser reformatada para o espaço do slide, mas a origem continua sendo a thread. Por isso, este é um **derivado**, não um novo formato canônico no banco Ideas.

A skill `build-thread-carousel` grava a reescrita e o HTML em `posts/thread/<slug>/sketch/` e os PNGs publicáveis na raiz de `posts/thread/<slug>/`.

### Modos atuais

- **Default:** layout editorial inspirado no X, com paleta clara e neutra.
- **X:** dark mode que reproduz mais fielmente a aparência do Twitter/X.

Os dois modos mantêm o mesmo conteúdo, estrutura e proporção 4:5; muda apenas o tratamento visual.

## Post de LinkedIn — Canal Principal: LinkedIn

Post de texto longo nativo, acompanhado por uma imagem que interrompe o scroll. Defende uma tese com substância, evidência e posição clara, em até 3.000 caracteres. A primeira linha cria tensão antes do “ver mais”; o corpo desenvolve o argumento em parágrafos; o fecho comprime a posição ou faz uma pergunta genuína.

A skill `build-linkedin` entrega `final.md` e `image.png` em `posts/linkedin/<slug>/`. No banco Ideas, o valor de `Format` é `LinkedIn Post`.

A skill não declara modos formais para este formato. Extensão, blocos argumentativos e tipo de hook variam conforme o material, sem virar categorias separadas.

## Artigo ilustrado — Canal Principal: Substack

Artigo longo construído como uma história sequencial, apoiado por três a oito capturas reais de fontes primárias. Em vez de apenas publicar a conclusão, mostra o caminho até ela: hipóteses, documentos, testes, números, erros e decisões. O corpo costuma ter de 1.200 a 3.000 palavras, sem teto quando o material sustenta a extensão.

A skill `write-substack` entrega `final.md`, `cover.png` e as imagens numeradas em `posts/substack/<slug>/`. Quando nasce de uma ideia nova, o valor de `Format` no banco Ideas é `Substack`; quando aprofunda uma peça já processada, preserva o formato primário da ideia.

### Modos narrativos atuais

- **Investigação:** algo quebrou e o autor reconstrói como descobriu a causa.
- **Reconstrução:** confronta a cobertura com as fontes primárias para mostrar o que aconteceu de fato; é o modo de notícia.
- **Teste:** acompanha uma pergunta, o setup, a execução, os resultados e as falhas de um experimento real.
- **Decisão:** compara alternativas, registra a escolha, o custo pago e o que faria o autor voltar atrás.

Os caminhos de **reuso** e **standalone** são fluxos de entrada e fechamento no Notion, não modos editoriais.

## O que não conta como formato

- `capture-idea` e `content-research` alimentam o banco Ideas, mas não produzem uma peça publicável.
- `build-thread-carousel` cria uma apresentação derivada para Instagram, sem substituir o `Format` primário `Thread`.
