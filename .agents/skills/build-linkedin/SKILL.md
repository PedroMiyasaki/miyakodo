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

Propósito: produzir um post de LinkedIn completo e pronto para publicar: o texto longo **e** a imagem que vai com ele. O trabalho é transformar ideias cruas em posts de LinkedIn que defendem uma tese, carregam densidade e tomam uma posição clara, na voz do usuário, e depois encontrar a única imagem que faz o leitor-alvo parar o scroll por tempo suficiente para ler.

O formato pede um argumento com mais camadas que os outros formatos, sem teto de caracteres como no X e sem visual para se apoiar. Entregue substância.

---

## Ferramentas disponíveis

Use o Notion MCP para ler o banco **Ideas** e, no fechamento, atualizar `Status` e `Format` na ideia processada (a única escrita no Notion).

Use as ferramentas de **automação do navegador Chrome** (`mcp__claude-in-chrome__*`) no Passo 7 para encontrar e capturar a imagem do post. Elas são deferred: invoque a skill `Codex-in-chrome` antes de chamar qualquer uma delas.

---

## Referências obrigatórias

Leia antes de escrever qualquer post de LinkedIn:

**Via Notion (MCP):**

| Banco | ID | O que procurar |
|---|---|---|
| **Ideas** | `e2970ca3-7724-4a81-8f12-7ea34c048c67` (ID do data source) | A ideia de origem do post de LinkedIn |

**Localmente, leia os dois em toda rodada:**

`examples/` guarda dois posts reais de LinkedIn que funcionaram: `assinatura_cc.md` e `hype_ia.md`. **O assunto deles é irrelevante** e nenhum dos dois é sobre a ideia que você está escrevendo. Eles estão ali para uma coisa só: calibrar como um post de LinkedIn humano, com autoridade e compartilhável fica na página. Leia os dois.

O que eles mostram em conjunto, e onde cada regra está escrita hoje:

| O que os exemplos fazem | Escrito em |
|---|---|
| Parágrafos de 3 a 6 frases encadeadas, parágrafo de uma frase usado como beat raro | `base.md` § 5, *Densidade de parágrafo* |
| Frases dentro do parágrafo ligadas por conectivos de verdade | `base.md` § 7 |
| Repetição usada como figura audível que cresce e para | `base.md` § 5, *Repetição deliberada* |
| Um nome próprio ou um número a cada duas ou três frases | `sincere-senior.md`, *Concretude* |
| A decisão, o preço ou o dado próprio do autor em jogo | `sincere-senior.md`, *Skin in the game* |
| Sem hashtag, sem CTA de engajamento | Passo 5 abaixo |

---

## Quando agir

Rode quando o usuário disser algo como:
- "monta o post do LinkedIn da última ideia"
- "escreve o post do LinkedIn da próxima ideia"
- "LinkedIn do item X"
- "gera o texto do LinkedIn"
- ou qualquer variação que signifique transformar uma ideia crua num post longo de LinkedIn

A entrega é sempre texto **mais** imagem. Se o usuário pedir só o texto, pule o Passo 7 e diga isso.

---

## Protocolo de execução, passo a passo

### Passo 1 · Identificar a ideia a trabalhar

Se o usuário não especificou qual:
- Abra o banco **Ideas** (`e2970ca3-7724-4a81-8f12-7ea34c048c67`)
- Filtre por `Status = "Pending"` e ordene por `Date` decrescente (mais recente primeiro). Se `Date` não existir ou estiver vazio, use `createdTime`
- Pegue a ideia mais recente
- Mostre o título ao usuário e confirme antes de seguir:
  > "Ideia selecionada para o LinkedIn: [título]. Sigo com essa?"

Se o usuário especificou um título ou item: encontre essa ideia no banco Ideas e use direto.

### Passo 2 · Ler a ideia inteira

Abra a linha correspondente no banco Ideas e leia tudo que estiver disponível:
- Título
- Texto cru da ideia
- Notas, contexto ou exemplos anexados
- Data e status

Extraia da ideia os seguintes elementos:
- Ângulo principal
- Tese possível
- Exemplo/prova disponível, ou uma hipótese concreta
- A tensão que pode virar o hook

Defina também a ACP Phase.

### Passo 3 · Calibração de voz

A voz mora em `docs/voice/`. Leia `docs/voice/base.md`: é a voz base de toda peça, em todo formato.

Depois leia `docs/voice/layers/sincere-senior.md`. É a **layer padrão de todo post de LinkedIn**: o registro de engenheiro sênior, o formato do argumento e as regras de honestidade que fazem o post soar como o usuário. Leia em toda rodada, sem que peçam. Onde ela discorda da base em registro, a layer ganha. As regras anti-slop da base continuam valendo.

Se o usuário nomear outra layer, leia essa também em `docs/voice/layers/`: ela ganha das outras duas.

Depois leia os posts em `examples/`. Os dois documentos de voz enunciam as regras. Os exemplos são o que as regras produzem numa página, e a distância entre ler uma regra sobre densidade de parágrafo e ver uma aplicada é a maior parte da calibração. Ignore o assunto deles.

Não existe documento de audiência nem de pilar: se a peça precisar de um leitor-alvo ou de um ângulo, pergunte ao usuário.

### Passo 4 · Decidir estrutura e tamanho

Um post de texto no LinkedIn tem um teto técnico de 3.000 caracteres. Deixe a necessidade do argumento definir o tamanho: sem enchimento, sem corte prematuro.

**Faixas de referência:**
- **Post curto (600–900 caracteres)**: uma observação só, um dado com interpretação, uma posição direta. Para a fase A do ACP, em que alcance importa mais que profundidade.
- **Post médio (900–1.800 caracteres)**: um argumento com exemplo, derrubada de mito, um framework em 2 ou 3 pontos. O mais comum para ACP=A→C.
- **Post longo (1.800–2.800 caracteres)**: análise aprofundada, cadeia causal com várias camadas, argumento que precisaria de carrossel se fosse visual. Para ACP=C, em que autoridade é o objetivo.

Se a ideia cabe bem num post curto, não estique. Se a ideia precisa de um desenvolvimento que passa de 2.800 caracteres para manter a qualidade, use o formato carrossel.

**Calibre contra `examples/` antes de assumir que precisa do formato longo.** Ali, o post que anuncia uma decisão fica em 1.600 caracteres, e só o que é pura polêmica passa de 3.000. O tamanho acompanha quanto material verificável o autor tem de verdade (nomes, números, uma decisão que ele tomou), não quanto argumento ele conseguiria construir. Um post de 2.900 caracteres feito só de raciocínio é longo porque está inchado, e vai parecer isso ao lado do post de 1.600 que anuncia uma decisão com preço e para.

### Passo 5 · Escrever o post

#### Formatação nativa do LinkedIn

O LinkedIn renderiza quebra de linha como espaço visual, e a tentação é usar esse espaço em toda frase. Não use. **Aqui, parágrafo é unidade de pensamento, não unidade de exibição.** A maioria tem de três a seis frases que desenvolvem uma ideia, ligadas por conectivos de verdade, conforme `base.md` § 5 e § 7. O parágrafo de uma frase é um beat: funciona porque é raro, e dois ou três deles num post é o teto.

O defeito que isso substitui é específico e é o mais comum do formato: frases corretas empilhadas uma por linha, todas com o mesmo peso, nada construindo, nenhum sinal de qual ideia sustenta o resto. Lê como feed de teleprompter. Os dois posts em `examples/` evitam isso, inclusive o que é pura polêmica.

Varie o tamanho dos parágrafos de propósito. Um que tem seis frases, depois um que tem duas, depois um fragmento: isso é a cara de gente escrevendo.

**Uma lista curta com hífen é permitida** quando os itens são de fato paralelos e curtos (três famílias de solver, três motivos). Um dos posts de referência usa uma. O que fica de fora é a lista de cabeçalho inline que `base.md` § 5 proíbe, `- **Velocidade:** o sistema é mais rápido`: decoração fingindo ser estrutura.

**Sem markdown**: o LinkedIn não renderiza `**negrito**`, `_itálico_` nem `# headings`. Use quebras de linha e estrutura verbal para criar hierarquia visual. Símbolos funcionais (→, •) são aceitáveis como marcadores de lista. Emojis decorativos (🚀, 🔥, 💡) são proibidos.

#### Estrutura obrigatória

**Primeira linha: hook**
- É o único texto visível antes do botão "ver mais" no feed
- Função: criar tensão suficiente para o leitor clicar em "ver mais"
- Formatos válidos (exemplos de saída):
  - Afirmação contraintuitiva: "A maioria dos projetos de IA não falha na tecnologia."
  - Um dado com interpretação implícita: "80% dos casos de uso de IA que chegam até a gente já foram tentados internamente uma vez."
  - Uma pergunta que nomeia uma dor real da audiência: "Por que a automação que funcionou no piloto trava na escala?"
  - **O fato em si, dito seco**, quando o fato é notícia de verdade: "Hoje é um dia grande para a DuckLabs: estamos entrando na Amazon Web Services." Sem preparação, porque o anúncio é a tensão.
  - **Um fragmento**, quando a história é uma decisão: "Parei." Uma palavra, e o motivo na linha seguinte. Isso só funciona quando o que vem depois é uma decisão real com um preço anexado. Como recurso de estilo num post comum, é teatro.
- **Nunca abra com:** "Olá, LinkedIn", apresentação da empresa, ou pergunta genérica ("Você sabia que...")
- A primeira linha não deve entregar a resposta. Ela deve tornar a resposta irresistível

**Não fabrique uma tensão que a ideia não tem.** Os dois posts de referência abrem sem truque: um com uma decisão que custou dinheiro de verdade, o outro só dizendo a tese. Os dois seguram porque o material é real. Uma afirmação contraintuitiva inventada e parafusada em cima de material comum é pior do que a afirmação seca desse material.

**Desenvolvimento (corpo)**

Organize o argumento em blocos curtos com função clara:

- **Bloco de problema**: nomeia o que está errado no entendimento convencional ou na prática comum
- **Bloco de causa**: explica *por que* o problema existe, a camada que a maioria não vê
- **Bloco de evidência**: um dado, um caso real (sem nomear o cliente), uma observação mensurável, uma comparação concreta
- **Bloco de contraste**: o que a maioria faz vs. o que funciona, com especificidade, não generalidades
- **Bloco de framework**: uma lógica em 2 a 4 pontos que o leitor consegue aplicar ou usar como critério
- **Bloco de nuance**: antecipa a objeção óbvia e responde, mostra profundidade, evita a simplificação excessiva

Não use todo bloco em todo post. Escolha os que a ideia exige. Um post médio tem 3 ou 4 blocos bem desenvolvidos. Um post longo pode ter 5 ou 6.

**Isso são funções, não uma ordem de execução, e elas ficam invisíveis na saída.** Os posts de referência não percorrem problema → causa → evidência → nuance: um é decisão e número do começo ao fim, o outro vai direto da posição ao contraste e não concede nada. O bloco de nuance, em particular, é opcional. Um post que toma uma posição e segura é mais forte que um que se amacia na hora marcada. Se um leitor consegue reconstruir a lista de blocos a partir do post pronto, os blocos estão aparecendo.

**Fechamento / CTA**

CTA no LinkedIn não é pedido vazio de engajamento. Formatos válidos (exemplos de saída):

- Uma posição clara que consolida o argumento: "O ponto é controle de processo antes de automação, e a tecnologia vem como consequência disso, não como ponto de partida."
- Uma pergunta que o autor genuinamente não consegue responder, dirigida a leitores que conseguem: "Que outros domínios ainda têm algoritmo correndo na frente da escala?"
- O link para a coisa que o post anuncia, quando o post é um anúncio: "Leia o anúncio completo aqui:"

O fechamento é onde os posts de referência são mais consistentes, e é o oposto do que o formato ensina. **Nenhum dos dois pede nada.** Um termina na posição, o outro termina numa acusação. O post ganha o comentário por valer uma resposta, não por pedir a resposta.

Então: termine na compressão final do argumento, ou numa pergunta cuja resposta você de fato não sabe e um leitor qualificado talvez saiba. Nunca em "o que você acha?".

**Hashtags: o padrão é nenhuma.**

Os dois posts de referência têm zero, e o formato não precisa delas para alcance há anos. Acrescente só quando o usuário pedir, ou quando o post mira de verdade uma tag que as pessoas seguem. Nesse caso, no máximo três, técnicas e específicas, numa linha própria no fim. `#inovação`, `#tecnologia`, `#IA` são ruído e marcam o post como saída de marketing.

#### Formatação da saída

Entregue o post completo na forma final de publicação, quebras de linha incluídas, sem rótulos estruturais (sem "BLOCO DE PROBLEMA:", sem "HOOK:"). A saída tem que dar para colar direto no LinkedIn sem edição de formatação.

```
[primeira linha: hook]

[desenvolvimento, em parágrafos de tamanho variado]

[fechamento]
```

Hashtags não fazem parte da forma padrão. Quando o usuário pedir, elas vão numa linha própria depois do fechamento.

Junto com o post, entregue também:
- Contagem de caracteres
- A ACP Phase identificada

### Passo 6 · Apresentar, iterar e salvar localmente

Apresente o post completo com a contagem de caracteres e a ACP.

Derive o slug do título da ideia (minúsculas, hífens no lugar de espaços e caracteres especiais, sem acentos) e salve na hora como `posts/linkedin/<slug>/sketch/v1.md` com Write, com o post na forma final de publicação seguido da linha com a contagem de caracteres e a ACP.

Pergunte:
> "Pronto para finalizar, ou mais alguma correção?"

Para cada correção pedida:
- Aplique a mudança, recalculando a contagem de caracteres quando precisar.
- Crie `posts/linkedin/<slug>/sketch/v(N+1).md`: leia a versão anterior, copie verbatim os blocos que não mudaram, aplique só o que mudou. Não regenere o que não mudou.
- Pergunte de novo: "Pronto para finalizar, ou mais alguma correção?"

Repita até o usuário confirmar que está pronto. Só então siga para o Passo 7.

### Passo 7 · Encontrar e capturar a imagem

O texto está travado. Agora encontre a única imagem que merece a parada.

A audiência é gente que trabalha com IA e dono de negócio rolando o feed em velocidade. A imagem tem um trabalho só: fazer esse leitor específico parar por tempo suficiente para ler a primeira linha. Ela faz isso mostrando **algo que ele reconhece do próprio trabalho**, não sendo bonita.

#### 7a · Decidir o que a imagem tem que carregar

Antes de buscar, escreva uma frase: *o que essa imagem tem que mostrar?* Responda a partir do post, não de uma noção vaga do tema.

A resposta mais forte é quase sempre **o mecanismo que o post discute, desenhado**. O leitor reconhece o próprio sistema na figura antes de ler uma palavra, e o argumento já começou.

> **Caso de referência.** O post contra agentes totalmente autônomos saiu com o diagrama canônico do loop ReAct: `Task → LLM (Reasoning self-loop) → Tools → Environment`, com as setas `Action` e `Result`. Preto e branco, sem marca. É exatamente a arquitetura que o post desmonta. Quem já construiu um viu o próprio sistema e parou.

Classes de imagem que funcionam, da melhor para a pior:

1. **O diagrama de arquitetura da coisa em discussão.** Torna o argumento visível antes de o texto ser lido.
2. **Um gráfico com forma surpreendente**: um benchmark, uma curva de custo, uma distribuição de latência. Use quando a espinha do post é um número.
3. **Um print do artefato real**: um trace, um log, um system prompt de 400 linhas, um dashboard, a UI de uma ferramenta. Lê como prova de que a coisa foi vista, não teorizada.
4. **Uma figura do paper que o post cita.** Crível e específica. Dê o crédito.

Nunca: foto de banco de imagem de gente no laptop, cérebro brilhando, mão de robô, rede neural azul abstrata, arte gerada por IA, ou um card com o hook digitado em cima de um gradiente. Isso sinaliza "conteúdo" e é ignorado exatamente pelo leitor para quem o post existe.

#### 7b · Julgar no tamanho do feed

A imagem vai ser vista pequena, primeiro, num celular. Antes de capturar, confira:

- **Legível como thumbnail.** Rótulos legíveis em mais ou menos 40% da largura. Se precisa de zoom, falhou.
- **Poucos elementos.** Cinco ou seis caixas, não um mapa de sistema com 30 nós.
- **Alto contraste**, e sobrevive tanto ao modo claro quanto ao escuro do LinkedIn. Fundo branco liso ou escuro liso funcionam. Cinza médio não.
- **Paisagem ou quadrada.** Imagem alta é cortada no feed.
- **Sem marca alheia**, sem marca d'água, sem banner de cookie nem chrome de navegação visível na captura.

#### 7c · Buscar e capturar

Invoque a skill `Codex-in-chrome`, depois trabalhe numa **aba nova** (`tabs_create_mcp`).

Vá na fonte antes de ir na busca de imagens. Ordem das fontes: o paper no arXiv, a página de docs do framework, o post original do blog, e a busca de imagens como último recurso. Uma página de origem dá resolução de verdade e uma URL que dá para verificar e creditar. Um thumbnail de busca de imagens não dá nenhum dos dois.

Monte a query a partir do termo canônico, não da frase do post, e em inglês (é assim que docs e busca indexam): `react agent loop diagram`, `langgraph state graph architecture`, `<paper name> figure 2`. Se o post discute uma coisa com nome, a coisa com nome tem uma figura canônica. Encontre essa.

Capture com um screenshot do elemento na página. Recorte na figura: sem a mobília da página em volta.

Não fabrique uma imagem e não monte uma em HTML. Este passo encontra um artefato que já existe. Se nada bom aparecer depois de duas ou três buscas, pare e diga isso, em vez de se contentar com foto de banco de imagem. Um post sem imagem ganha de um post com cérebro brilhando.

#### 7d · Salvar junto com o post

Salve a captura como `posts/linkedin/<slug>/image.png`: na raiz da pasta, ao lado do `final.md` com que ela sai, não em `sketch/`.

Depois acrescente uma linha ao rodapé de metadados do `posts/linkedin/<slug>/sketch/v<N>.md` final (o rodapé que já carrega a contagem de caracteres e a ACP, não o corpo publicável), para o arquivo de texto apontar para a imagem dele:

```
Imagem: posts/linkedin/<slug>/image.png — <URL de origem>
```

O rodapé fica em `sketch/v<N>.md`, então ele vai junto para o `final.md` quando essa cópia for feita no Passo 8.

Se a imagem é figura de um paper ou de um post de blog identificável, diga ao usuário para creditar a fonte no post ou no primeiro comentário. Diagrama genérico de livro didático não precisa.

#### 7e · Apresentar

Mostre a imagem ao usuário, uma linha sobre por que ela foi escolhida, e a URL de origem. Pergunte:

> "Essa imagem funciona, ou procuro outra?"

Se ele quiser outra, volte ao 7a e responda de novo *o que essa imagem tem que mostrar?* antes de buscar de novo. Uma segunda busca com a mesma premissa costuma devolver os mesmos erros.

### Passo 8 · Fechar

Com o texto confirmado e a imagem aprovada, monte a entrega. Tudo da peça mora em **uma** pasta, `posts/linkedin/<slug>/`: `sketch/` é o material de trabalho, e a raiz da pasta guarda exatamente o que é publicado:

| Arquivo | O que é | Escrito por |
|---|---|---|
| `final.md` | cópia do `sketch/v<N>.md` de maior número | esta skill, agora |
| `image.png` | a captura do Passo 7 | esta skill, no 7d |

Então neste passo você copia o `sketch/v<N>.md` final para `posts/linkedin/<slug>/final.md`. A imagem já está no lugar desde o 7d.

O histórico `sketch/v<N>` nunca é apagado: é a trilha de auditoria, e `final.md` é uma cópia da versão mais alta tirada no "pronto". Então, se o usuário editar um `sketch/v<N>.md` depois disso, copie de novo para `final.md`.

Depois atualize a ideia de origem no banco Ideas: `Status` → `"Processed"` e `Format` → `"LinkedIn Post"` (o formato que esta skill produz: a ideia é criada sem formato, e ele só é definido agora, na produção). Essa é a única escrita desta skill no Notion. `Status` e `Format` se acumulam no banco como o retrato real do calendário (fase e formato de toda peça produzida).

### Passo 9 · Apontar o próximo passo

> "Post pronto. Tudo sai de `posts/linkedin/<slug>/`: `final.md` e `image.png`. O histórico de versões fica em `sketch/`. Próximo passo: publicar manualmente no LinkedIn."

---

## Critérios de qualidade do post de LinkedIn

Um post é válido quando todo critério abaixo é atendido:
- A primeira linha cria tensão suficiente para o clique em "ver mais" sem revelar a resposta
- O argumento é desenvolvido de verdade: tirar qualquer bloco piora o post
- O tom bate com o que o usuário definiu na conversa: sem hype, sem registro motivacional, sem jargão sem explicação
- O tamanho dos parágrafos varia, e o parágrafo de uma frase aparece no máximo duas ou três vezes, como beat
- Dentro de cada parágrafo, as frases estão ligadas por conectivos de verdade em vez de empilhadas lado a lado
- Todo parágrafo carrega pelo menos um nome próprio ou um número que o leitor poderia ir verificar
- O autor está exposto em algum lugar: uma decisão que tomou, um preço que pagou, um dado que só ele tem
- Não há markdown (`**`, `_`, `#`), só texto puro com quebras de linha
- O fechamento toma uma posição ou pergunta algo que o autor de fato não consegue responder, e não pede nada
- Não há hashtags, a menos que o usuário tenha pedido
- A contagem de caracteres não passa de 3.000
- Lendo só a primeira linha e o CTA, o leitor pega a tese central do post
- A imagem mostra algo do assunto real do post, é legível como thumbnail e não é foto de banco de imagem
- A imagem está salva em `posts/linkedin/<slug>/image.png` e o rodapé do `sketch/v<N>.md` final registra o caminho e a URL de origem
- A raiz de `posts/linkedin/<slug>/` guarda o conjunto publicável: `final.md` (cópia do `sketch/v<N>.md` final) ao lado de `image.png`, com o histórico `v<N>` intacto em `sketch/`

Se qualquer critério falhar, refaça antes de apresentar.

---

## Fora do escopo

- Não captura ideias cruas (isso é a skill de captura de ideias)
- Não escreve roteiros de Reel (isso é a skill de roteiro)
- Não escreve carrosséis (isso é a skill de carrossel)
- Não escreve threads (isso é a skill de thread)
- Não adapta um carrossel para o LinkedIn: quando o usuário quiser publicar um carrossel no LinkedIn, vai direto para a publicação ou para o design, sem passar por esta skill de texto
- Não publica nada: publicar no LinkedIn é manual
