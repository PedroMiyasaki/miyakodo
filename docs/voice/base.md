# Voz base

Esta é a voz base de tudo que sai deste projeto: roteiros de Reel, threads, carrosséis, posts de LinkedIn, legendas. Vale para toda peça, em todo formato, sem exceção.

É uma **base**, não a voz inteira. Regras de formato e de situação empilham em cima dela como layers em `docs/voice/layers/`. Quando uma layer contradiz a base, a layer vence naquela peça. Mas a base é o piso: nada sai abaixo dela.

**Leia isto antes de escrever, não depois.** Isto não é conserto aplicado num rascunho pronto. É o jeito como o rascunho sai da primeira vez. Revisar contra esta lista no fim é a rede de segurança, não o método.

---

## A ideia central

Texto gerado por máquina tem cheiro. Nunca é uma palavra ou um truque isolado: é a combinação. Estrutura previsível, frase que hesita e depois afirma, paralelismo sem descanso, importância inflada, e tudo embrulhado com um laço no fim. Texto humano é mais bagunçado, tem mais opinião e varia de ritmo.

**Isso não é pedir texto mais simples.** É soar como alguém que conhece o assunto de verdade e tem opinião sobre ele. Densidade é bem-vinda. Polimento que apaga a pessoa, não.

**O ponto de partida.** O português que sai por padrão vem de um lugar específico: petição, artigo acadêmico e redação de vestibular. Esse é o registro que domina o texto formal em português na internet, então é ele que aparece quando ninguém pede outra coisa. O problema não é a formalidade em si. É que esse registro pertence a documento, e a gente escreve para vídeo, carrossel e post.

**Nada aqui pede texto errado.** Toda regra deste guia escolhe, entre duas formas corretas, a que alguém usaria falando.

**Empilhamento de padrões:** quando vários sinais fracos caem na mesma frase (negrito, mais aspas de ironia, mais um aparte dramático, tudo em cima de um termo inventado), isso é um sinal forte, não três fracos. Conserte uma vez. Não conte três vezes. O inverso também vale: um caso isolado não é sinal, o empilhamento é.

---

## 1. Estrutura

Fórmula é o sinal mais visível. O mesmo desenho de seção repetido dez vezes. Todo parágrafo montado igual.

**Evite:**
- Toda seção terminando numa lição arrumada ou numa conclusão
- Chamada repetida: "O que isso significa para você:", "A lição:", "Por que isso importa:"
- O mesmo número de parágrafos por seção, o mesmo número de itens por lista
- "Contexto, explicação, conclusão" repetido ao pé da letra em cada seção
- Fecho de fórmula: "Desafios e perspectivas", "O que vem pela frente"
- O loop "Apesar do seu [ponto forte]… enfrenta desafios… Apesar desses desafios…"

**No lugar:**
- Varie o tamanho das seções. Uma tem dois parágrafos. Outra tem cinco.
- Deixe uma seção acabar de repente. Nem tudo precisa de laço.
- Quebre o padrão de propósito: se três seções são lista, a quarta é prosa.
- Dilua o "o que isso significa" no texto em vez de anunciar.
- Troque o enchimento de desafio e perspectiva por fato específico.

> **Fraco:** Apesar do desempenho impressionante nos benchmarks, o modelo enfrenta desafios típicos de um lançamento open-weight, como custo de inferência e requisitos de hardware. Apesar desses desafios, com sua licença permissiva e comunidade crescente, ele continua ganhando adoção.
>
> **Melhor:** A inferência custa cerca de 3× mais que a alternativa por API no mesmo throughput. Dois provedores de inferência adicionaram suporte na primeira semana, e foi isso que puxou a adoção de verdade.

**A capa fala para o entusiasta médio, não para o especialista.** O leitor brasileiro médio de IA reconhece ChatGPT, OpenAI, SpaceX, Torvalds. Não reconhece harness, page table, change of control, nem “N fatos mostram onde X termina”. A capa precisa de uma frase que alguém falaria, e de um nome ou logo que a pessoa já conhece. A tese técnica entra depois, quando o scroll já aconteceu.

> **Fraco:** 6 fatos mostram onde o GPT-6 termina e o discurso de AGI começa.
>
> **Melhor:** O ChatGPT-6 é ótimo. Mas se acalmem, a AGI ainda não está entre nós.

> **Fraco:** 4 elos mostram quem decide quais modelos chegam ao seu IDE
>
> **Melhor:** A SpaceX comprou o Cursor. E a OpenAI não gostou nada disso.

**Conte o caso até o leitor conseguir repetir o que aconteceu.** Se alguém técnico lê o post e ainda não entende o conflito, o bug ou o teste, o texto falhou. Ensina o objeto primeiro, em analogia ou cena cotidiana; o caveat, o número e a tese vêm depois. Abrir no jargão ou no “mas” é inverter a aula.

> **Fraco:** O 99,9% mais chamativo veio com o harness da própria OpenAI.
>
> **Melhor:** O ARC-AGI-3 é um teste que mede a capacidade de um modelo no eixo AGI. Ele gera um mini-game nunca visto pela IA, o que teoricamente testa a capacidade dela de generalizar inteligência em tarefas novas. Nesse contexto, o ChatGPT-6 foi muito bem, com 99,9% de acerto.
> Mas tem um detalhe importante...

> **Fraco:** Numa Battlemage G21 de 16 GiB, o driver Intel Xe entregava parte do armazenamento de compressão como VRAM livre.
>
> **Melhor:** O computador ligava. Mas a tela de login não parava de reiniciar.

**Não reabra o slide seguinte com a prova do slide anterior.** Se o slide 4 já gastou “24 patches e 18 reinicializações”, o 5 começa no próximo fato. Repetir a contagem no gancho é feio e parece que a história não andou.

> **Fraco:** Depois de 24 patches e 18 reinicializações, surgiu uma correção de uma linha.
>
> **Melhor:** Em determinado momento, o sistema arredondava a memória para cima e liberava 2 KiB que deveriam continuar reservados.

**CTA de carrossel pede um comentário-chave, não uma bifurcação retórica.** O fecho oferece o ativo (artigo, commit, link) em troca de uma palavra no comentário. A pergunta “A ou B?” no último slide parece exercício, não conversa.

> **Fraco:** Agora escolha: AGI ou ótimo upgrade?
>
> **Melhor:** Eu escrevi um artigo detalhando melhor esse comparativo. Comenta “COMPARATIVO” e eu te envio!

> **Fraco:** Quando a IA disser “impossível”, você fecha o relatório ou pede outro diagnóstico?
>
> **Melhor:** Ficou curioso para ver esse processo em detalhes? Comente “COMMIT” que eu te envio o link do commit que exploramos aqui.

---

## 2. Inflação de importância e linguagem promocional

O defeito padrão é inflar importância. Tudo vira fundamental, revolucionário, vibrante. Lê como release de assessoria.

**Inflação de importância:** serve como, atua como, é um testemunho de, é um lembrete de, papel fundamental / vital / crucial / central, momento-chave, marco, ressalta a importância, destaca a relevância, reflete uma tendência mais ampla, simbolizando seu legado duradouro, abre caminho para, prepara o terreno para, marca uma virada, representa uma mudança, ponto de inflexão, cenário em constante evolução, marca indelével, profundamente enraizado

**Linguagem promocional:** conta com, vibrante, rico (no sentido figurado), profundo, aprimorando, exibindo, exemplifica, compromisso com, revolucionário (no sentido figurado), renomado, deslumbrante, imperdível, impressionante, aninhado, no coração de

**O conserto raramente é um sinônimo.** Quase sempre você apaga a inflação e põe um fato específico no lugar.

> **Fraco:** O laboratório foi fundado em 2023, marcando um momento fundamental na evolução da pesquisa em modelos abertos.
>
> **Melhor:** O laboratório foi fundado em 2023 para publicar modelos open-weight, depois que os fundadores saíram de um laboratório fechado por discordar da política de lançamento.

### Adjetivo que ninguém falaria

*Realidade brutal*, *impacto real*, *tentativa bonita*, *verdade crua*, *escolha corajosa*. O adjetivo foi escolhido pelo peso, não pelo encaixe, e o par só existe no papel.

O teste: você já disse essa combinação em voz alta para alguém? Se a resposta for não, troque o adjetivo ou corte ele.

**Isso não é um pedido para tirar adjetivo forte.** *Erro caro*, *decisão idiota*, *resultado ridículo* são fortes e são falados. Repare que o problema também não é o adjetivo vazio do topo desta seção, que é outro defeito: ali a palavra não diz nada, aqui ela diz, só que na combinação errada.

### O que não é inflação

**Tirar *muito*, *bem*, *bastante*, *realmente*, *ainda*, *tão* para “soar técnico” deixa o texto estéril.** Isso não é o adjetivo inflado do topo da seção. É o jeito normal de uma pessoa pesar o que está dizendo.

> **Fraco:** O GPT-6 é excelente. O 99,9% não prova AGI.
>
> **Melhor:** O GPT-6 melhorou muito. Só não virou AGI.

> **Fraco:** Era uma boa história. Também estava errada num detalhe que muda quase tudo.
>
> **Melhor:** Só que eu estava simplificando demais. […] A nota é real, o resultado é realmente impressionante…

A regra de inflação continua valendo para *papel fundamental*, *revolucionário*, *impacto real*, *escolha corajosa*. Não use ela para limpar o português falado.

---

## 3. Vocabulário

Certas palavras entregam na hora.

**Nível 1, sinal vermelho, não use:** mergulhar fundo, mergulhar em, cenário (metafórico), tapeçaria, mudança de paradigma, alavancar (como verbo), navegar (metafórico), universo (metafórico), embarcar numa jornada, jornada, miríade, uma infinidade de, multifacetado, revolucionar, sinergia, ecossistema (fora de contexto técnico), ressoar, desbloquear, potencializar

**Nível 2, suspeito em grupo, três ou mais na mesma peça é sinal:** robusto, fluido, de ponta, inovador, abrangente, fundamental, cheio de nuances, convincente, transformador, reforçar, ressaltar, em constante evolução, fomentar, imperativo, intrincado, holístico, disruptivo, sem precedentes, otimizar

Repare que várias palavras do nível 2 são termos técnicos legítimos neste assunto. `ecossistema` descrevendo um registro de pacotes está certo. `ecossistema` descrevendo um mercado, não. `robusto` como propriedade de um sistema sob carga está certo. `robusto` como elogio, não. Julgue pelo que a palavra está fazendo: trabalho técnico ou decoração.

**O conserto costuma ser estrutural, não lexical.** A frase em geral precisa ser remontada, não ter uma palavra trocada.

> **Fraco:** Uma característica distintiva do framework é a incorporação de streaming. Um testemunho duradouro da sua origem na pesquisa é a ampla adoção de primitivas assíncronas em todo o ecossistema, evidenciando como esses padrões se integraram aos fluxos de produção.
>
> **Melhor:** O framework faz streaming por padrão. As primitivas assíncronas vieram do protótipo de pesquisa e ficaram, e é por isso que o código de produção ainda carrega elas.

### Palavra comprida onde cabe palavra curta

| Sai | Entra |
|---|---|
| realizar, efetuar | fazer |
| possuir | ter |
| utilizar | usar |
| necessitar | precisar |
| auxiliar | ajudar |
| demonstrar | mostrar |
| proporcionar, propiciar | dar |
| aprimorar, otimizar, potencializar | melhorar |
| iniciar, finalizar | começar, acabar |
| elaborar | escrever, montar |

**Nenhuma dessas palavras está proibida.** O teste é se existe uma palavra curta que diz a mesma coisa *naquela frase*. "Realizar um sonho" fica, porque "fazer um sonho" não é a mesma coisa. "Realizar uma análise" vira "analisar". E em peça técnica algumas delas carregam sentido de verdade: *otimizar* uma query é trabalho técnico, *otimizar* o seu dia é enfeite. Julgue pela função, igual ao critério do topo desta seção.

### Decalque do inglês

Construções que passam na gramática e não passam no ouvido, porque foram pensadas em inglês. Saber de onde cada uma vem ajuda a reconhecer:

| Decalque | Origem |
|---|---|
| mergulhar fundo em, vamos mergulhar | *dive into, delve* |
| desbloquear o potencial | *unlock the potential* |
| alavancar (como verbo genérico) | *leverage* |
| no cenário atual, no mundo de hoje | *in today's landscape* |
| quando se trata de | *when it comes to* |
| no final do dia | *at the end of the day* |
| tenha em mente | *keep in mind* |
| dar um passo atrás | *take a step back* |
| abraçar a mudança | *embrace change* |
| elevar seu conteúdo | *elevate* |
| Aqui está o porquê | *Here's why* |
| Espero que este email o encontre bem | *I hope this email finds you well* |

**Algumas dessas expressões já são português de verdade.** "Divisor de águas" existia muito antes do ChatGPT, e "no final do dia" está na boca de qualquer pessoa que trabalha em empresa. Sozinha, nenhuma delas prova nada. Elas contam quando aparecem em cima das outras coisas deste guia.

O decalque também mora no heading e no fecho aforístico: a frase foi pensada como título de newsletter em inglês e só depois traduzida.

> **Fraco:** O mesmo benchmark produziu dois GPT-6. / O ganho mais útil aparece quando o modelo admite que não sabe.
>
> **Melhor:** O mesmo GPT-6 tirou 62,7% e 99,9% na mesma prova. / O GPT-6 ainda alucina muito, só que quase a metade.

---

## 4. Tiques de gramática

Esses entregam o texto mesmo quando o vocabulário está limpo.

### Fuga do verbo "ser"

Construção rebuscada no lugar de "é", "são", "tem". O sinal é o acúmulo: a peça que nunca diz "é" e fica alternando entre "serve como", "atua como", "representa", "funciona como". Um "serve como" num parágrafo normal não é nada.

- "serve como" / "atua como" / "representa" → "é"
- "conta com" / "apresenta" / "oferece" / "dispõe de" → "tem"

> **Fraco:** O roteador atua como ponto de entrada. Ele conta com quatro backends e apresenta um overhead abaixo de um milissegundo.
>
> **Melhor:** O roteador é o ponto de entrada. Tem quatro backends e adiciona menos de um milissegundo.

Não é sinal: "o eval serve de teste de regressão e de benchmark ao mesmo tempo". Frase normal.

### Gerúndio de análise rasa

Gerúndio pendurado no fim da frase para fingir profundidade: "destacando…", "ressaltando…", "enfatizando…", "refletindo…", "simbolizando…", "evidenciando…", "contribuindo para…", "fomentando…"

Apague o trecho, ou promova ele a frase própria com uma fonte real por trás.

### Paralelismo negativo

"Não só… mas também…" e "Não é só sobre X, é sobre Y". Uma vez, tudo bem. O sinal é a densidade: numa peça curta, uma vez já basta. Duas numa longa. Vira muleta rápido, e tenta muito no gancho, então olhe ali primeiro.

### Regra de três

Tríade forçada onde o terceiro item é enchimento: "inovação, inspiração e insights". Tricólon é figura antiga e legítima, então não marque todo grupo de três. Marque os que têm um terceiro item que não acrescenta nada ou quase repete os dois primeiros. Se ele carrega peso, fica. Se não, corte para dois.

### Rodízio de sinônimos

Variação elegante demais: "o modelo… o sistema… a rede… a arquitetura", tudo no mesmo parágrafo, tudo para a mesma coisa. Escolha um termo e repita. Repetir é normal quando é a palavra mais clara. Em texto técnico é quase obrigatório.

### Intervalo falso

"De X a Y" onde X e Y não estão numa escala que faça sentido.

> **Fraco:** A virada nos levou do primeiro paper do transformer ao zoológico de modelos de hoje, de uma GPU só à dança enigmática do treinamento distribuído.
>
> **Melhor:** A peça cobre o paper original do transformer, os resultados de escala que vieram depois e onde o treinamento distribuído está agora.

### Verbo com "-se" no lugar de sujeito

O alvo é o `-se` que apaga quem fez a ação: *trata-se de*, *faz-se necessário*, *nota-se*, *observa-se*, *pode-se dizer*, *torna-se*, *encontra-se*, *percebe-se*. Junto com ele vem a passiva sem agente e o *é recomendado que*.

> **Fraco:** Trata-se de um erro comum, e nota-se que ele aparece mais em carrossel.
>
> **Melhor:** Esse erro é comum, e aparece mais em carrossel.

> **Fraco:** É recomendado que o roteiro seja lido em voz alta antes da gravação.
>
> **Melhor:** Leia o roteiro em voz alta antes de gravar.

**Não confunda com pronome reflexivo ou verbo pronominal.** *Ela se conecta*, *o post se espalhou*, *a gente se acostuma*, *não se sente bem*: todos normais, todos ficam. O critério é outro: pergunte "quem?" para a frase. Se a frase se recusa a responder, o `-se` está escondendo o sujeito.

A mesóclise (*far-se-á*, *dir-se-ia*) não tem uso nenhum em nenhum formato daqui.

### Substantivo sem artigo e sem plural

O substantivo contável em posição de objeto pede artigo ou plural. O hábito de largar ele pelado vem do inglês, onde *avoid bad posts* dispensa artigo, e atravessa junto com a estrutura da frase. O resultado passa na gramática e trava no ouvido, geralmente sem que o leitor consiga apontar o motivo.

> **Fraco:** É melhor escrever tudo na mão para evitar post ruim.
>
> **Melhor:** …para evitar um post ruim. / …para evitar posts ruins.

**Isso não quer dizer que todo substantivo pede artigo.** *Eu gosto de música*, *ele vive de conteúdo*, *sem medo*: aí o substantivo é genérico e não conta unidade, então está certo do jeito que está. O alvo é o substantivo contável na posição de objeto, do tipo que dá para contar: um post, dois posts.

### Quem está falando

Três hábitos que empurram o texto para longe da fala, agrupados porque aparecem juntos.

**Pronome oblíquo antes do verbo:** *isso lhe permite*, *conferindo-lhe*, *ao fazê-lo*, *eu o vi*. Nenhum formato daqui aguenta essa fileira. Na fala o pronome vira tônico ("eu vi ele") ou some ("Viu o vídeo?" "Vi.").

**Futuro em -rá:** *você notará*, *isso trará*, *poderá*. Vira "você vai notar", "isso vai trazer". Cuidado com o exagero: *será* e *vai ser* convivem sem problema, e o alvo é a forma empilhada, não uma ocorrência.

**Primeira pessoa do plural:** *precisamos*, *fizemos*, *observamos*. Em roteiro e legenda isso quase sempre é "a gente precisa", "a gente fez".

**O formato move o limite.** Roteiro de Reel é fala transcrita e aguenta o registro mais solto que existe neste guia. Post técnico de LinkedIn aguenta menos, e "nós" ali pode ser a escolha certa. O que nenhum dos dois aguenta é o clítico culto.

---

## 5. Ritmo e estilo

A cadência padrão é metronômica. Frase média. Frase média. Frase média. Gente de verdade varia muito.

**Evite:** toda frase com 15 a 25 palavras, nenhuma frase curta de impacto, nenhuma que corre longa e vai construindo, toda frase começando por substantivo ou por artigo.

**No lugar:** jogue frases curtas. "Isso é novo." "Funciona." "Não mais." Deixe uma frase correr quando a ideia precisa de espaço. Comece algumas com "Mas", "E", "Aí", "Então". Fragmento é normal fora de registro acadêmico.

**A frase curta é um beat, não o padrão.** Ela fecha um parágrafo, abre outro, cai uma vez para marcar o ponto. Dentro do parágrafo, frase que desenvolve a mesma ideia fica ligada à vizinha, e a seção 7 diz como. Empilhar frase curta dentro do parágrafo não é ritmo, é o staccato que denuncia a máquina.

### Densidade de parágrafo

O ritmo da frase tem um gêmeo um nível acima, e ele falha do mesmo jeito. O sinal é a peça onde todo parágrafo tem uma frase só, separado por linha em branco, até o fim. Lê como feed de teleprompter, não como alguém escrevendo: toda linha cai com o mesmo peso, nada acumula, e o leitor não recebe nenhum sinal de qual ideia sustenta o resto.

**Parágrafo é unidade de pensamento, não de exibição.** A maioria tem de três a seis frases que pertencem uma à outra, porque estão desenvolvendo uma coisa só. O parágrafo de uma frase é um beat, e funciona justamente porque é raro. Para de funcionar na hora em que vira o padrão.

> **Fraco:**
> O sistema erra uma vez a cada cem execuções.
>
> Parece bom.
>
> Só que a aplicação roda mil vezes por dia.
>
> São dez saídas quebradas que ninguém vê.
>
> **Melhor:** O sistema erra uma vez a cada cem execuções, o que parece bom até você olhar o volume: a aplicação roda mil vezes por dia, então são dez saídas quebradas por dia e ninguém está lendo.

Varie de propósito. Uma peça onde um parágrafo tem seis frases, o seguinte tem duas e o outro é um fragmento de quatro palavras é uma peça escrita por uma pessoa.

### Frase pensada em inglês

**A frase inteira foi pensada em inglês e só depois vestida de português.** A lista de decalques da seção 3 pega a expressão. Este item pega a arquitetura: título em caixa alta, “N fatos mostram X”, heading de tese, metáfora importada, sentença curta + ponto + sentença curta, sem o continuísmo que o ouvido brasileiro espera. O teste é o mesmo do guia inteiro: você falaria isso assim? Se a resposta for “só se eu estivesse traduzindo um headline”, reescreve. Não basta trocar o vocabulário.

> **Fraco:** Ele não esperou um palpite genial. Cada dúvida virava mais código de diagnóstico, uma nova reinicialização e outra rodada de análise. A IA fazia o trabalho repetitivo. Ele decidia o próximo teste.
>
> **Melhor:** Ele não esperou um palpite genial: cada dúvida virava mais código de diagnóstico, que levava a uma nova reinicialização e gerava outra rodada de análise, enquanto a IA fazia o trabalho repetitivo e ele decidia o próximo teste.

### Repetição deliberada

A seção 1 mata o paralelismo que fica no fundo: toda seção montada igual, toda lista do mesmo tamanho. Isso é diferente de repetição usada como figura: de propósito, num lugar só, construindo até alguma coisa.

> Quem já construiu coisa de verdade com IA sabe reconhecer esse teatro de longe.
> Sabe a diferença entre protótipo de palco e sistema em produção.
> Sabe que empresa não se sustenta com thread viral e print bonito.
> Sabe também que arquitetura séria exige engenharia, avaliação, contexto, governança.

Quatro frases abrindo no mesmo verbo, e funciona, porque está fazendo trabalho retórico e depois para. O teste é se a repetição é *ouvida*. Paralelismo de fundo é invisível e uniforme. Figura é audível e acaba.

### Travessão e ponto e vírgula

O travessão entra para injetar aparte dramático. O sinal é frequência e função ao mesmo tempo.

- **Frequência:** mais de um a cada três ou quatro parágrafos está acima do que uma pessoa escreve.
- **Função:** um só já é sinal quando faz o movimento clássico: o aparte explicativo largado no meio da frase para soar afiado.

A regra é uma: o aparte no meio da frase pede vírgula, dois-pontos ou parênteses. Ou vira frase nova. O travessão dramático é hábito tipográfico importado do inglês, e a essa altura virou piada pronta. Conte antes de dizer que tem demais.

**Ponto e vírgula** não aparece em post nem em legenda. Ele engessa a frase e denuncia na hora.

### Negrito

Ênfase mecânica, principalmente dentro de lista. Tire a maior parte. Guarde para termo importante de verdade na primeira vez que aparece.

Em carrossel, o negrito também vai na virada (“Mas tem um detalhe importante...”, “Modelo melhor? / AGI?”) e no nome do objeto que o slide está ensinando (ARC-AGI-3). Negrito mecânico dentro de lista continua proibido.

### Lista com cabeçalho inline

> **Fraco:**
> - **Velocidade:** O sistema está mais rápido.
> - **Qualidade:** A qualidade da saída melhorou.
> - **Segurança:** A segurança foi reforçada.
>
> **Melhor:** A atualização corta a latência p99 mais ou menos pela metade, corrige o bug de truncamento em contexto longo e tira o token store do disco.

### Emojis

Nenhum, em nenhuma peça.

### Título em caixa alta

Inicial maiúscula em cada palavra do título é sinal fraco sozinho: vários manuais de estilo pedem isso. Só conta junto com outros padrões, então não marque isolado.

Título inteiro em caixa alta é outra coisa. Não é estilo, é cartaz. Título de carrossel vai em caixa normal, como se fosse falado.

> **Fraco:** 4 ELOS MOSTRAM QUEM DECIDE QUAIS MODELOS CHEGAM AO SEU IDE
>
> **Melhor:** A SpaceX comprou o Cursor. E a OpenAI não gostou nada disso.

### Aspas curvas

Tipograficamente corretas e esperadas em conteúdo formatado. Só são sinal em texto puro ou em contexto de código, onde a aspa reta é a norma.

---

## 6. Hedge, enchimento e atribuição vaga

Hedge vem da tentativa de soar equilibrado. Quem entende do assunto é mais direto.

**Hedge para cortar:** "É importante notar que…", "Vale mencionar que…", "Embora certamente existam desafios…", "Isso não é isento de desvantagens…", "Para ser justo…", "Sem dúvida…", abrir com "Certamente," ou "Com certeza,", e qualificador empilhado como "poderia talvez se argumentar que… pode ter algum".

Diga a coisa. Fique do lado para onde a peça obviamente pende. Um hedge por peça é normal. Cinco é o sinal.

**Enchimento:**
- "a fim de" → "para"
- "devido ao fato de que" → "porque"
- "neste momento" → "agora"
- "o sistema tem a capacidade de" → "o sistema pode"
- "é importante notar que os dados mostram" → "os dados mostram"

**Atribuição vaga:** "Relatórios do setor", "Especialistas afirmam", "Observadores apontam". Nomeie a fonte, dê a data, ou tire a afirmação.

> **Fraco:** Especialistas acreditam que a técnica tem papel fundamental na confiabilidade em produção.
>
> **Melhor:** A técnica cortou a taxa de alucinação em 40% no conjunto de teste, segundo o paper de 2026 que apresentou ela.

**Resto de chatbot:** "Espero ter ajudado!", "Me avise se quiser que eu detalhe alguma seção!", "Ótima pergunta!", "Claro!" Apague inteiro. Isso nunca deveria chegar a um rascunho.

**Aviso de data de corte:** "Embora os detalhes sejam limitados…", "Com base nas informações disponíveis…" Ache a fonte ou tire a afirmação. ("Até [data]" é outra coisa: é prática normal para dado que envelhece e cabe neste assunto.)

**Bajulação:** nada de elogio, nada de "você está absolutamente certo". Responda ao conteúdo.

**Fecho positivo genérico:** "O futuro é promissor", "Vêm tempos empolgantes por aí", "Só o tempo dirá." Termine num fato específico, numa posição, ou só pare.

---

## 7. Tecido conectivo

As mesmas transições, sem parar. O repertório vem inteiro da redação escolar:

*Ademais* · *Outrossim* · *Além disso* · *Adicionalmente* · *Por conseguinte* · *Dessa forma* · *Sendo assim* · *Nesse sentido* · *Diante do exposto* · *Em suma* · *Em conclusão* · *Dito isso* · *Com isso em mente* · *Quando se trata de* · *Vale ressaltar que* · *Cabe destacar* · *É importante frisar* · *Convém salientar* · *Em contrapartida*

Some a família inteira do *É importante...*: *é importante lembrar que*, *é fundamental entender*, *vale lembrar que*.

Na maior parte dos casos o conector não precisa existir, e a frase seguinte começa sozinha. Quando precisa, use a ligação real: mas, só que, porque, aí, então. Faça referência direta à ideia anterior em vez de pegar um conector genérico. Deixe a quebra de parágrafo carregar o peso. *No entanto* uma vez num texto longo não é crime.

**Essa regra é sobre passar de um parágrafo para outro. Dentro do parágrafo, vale o contrário.** Frase que desenvolve a mesma ideia fica ligada à vizinha: vírgula e "porque", dois-pontos, "só que", "aí", "então", "mesmo assim", "ainda assim", oração relativa. Isso não é enfeite. É o tecido. Tirar essas ligações é o que produz o metrônomo da seção 5: quatro frases corretas lado a lado, nenhuma encostando na outra. A frase curta é beat entre parágrafos ou como fecho, não o padrão dentro do parágrafo.

> **Fraco:** O prompt é estatístico. Ele acerta 99% das vezes. Uma aplicação roda mil vezes por dia. São dez erros.
>
> **Melhor:** O prompt é estatístico, e 99% de acerto vira dez erros por dia numa aplicação que roda mil vezes.

> **Fraco:** As duas notas são verdadeiras. Elas só respondem a perguntas diferentes.
>
> **Melhor:** Portanto, não existe um resultado verdadeiro e outro falso. Existem dois resultados verdadeiros medindo coisas diferentes, embora apenas um deles tenha ido parar no centro do lançamento.

Cortar um conector de redação é melhoria. Cortar a ligação lógica é estrago, e o resultado é o português de IA: declaração, ponto, declaração, ponto.

---

## 8. Voz e textura

Evitar os padrões acima é metade do trabalho. Texto estéril, sem voz, é tão reconhecível quanto o slop.

**Sinais de texto sem alma, mesmo tecnicamente limpo:** frase sempre do mesmo tamanho, nenhuma opinião, nenhuma dúvida admitida, nenhuma primeira pessoa onde ela caberia, nenhum humor ou aresta, lê como verbete de enciclopédia.

**Como colocar uma pessoa no texto:**

- **Tenha opinião.** Reaja aos fatos, não só relate. "Eu sinceramente não sei o que sentir sobre isso" é mais humano que uma lista neutra de prós e contras.
- **Admita a complexidade.** "Isso é impressionante e também meio inquietante" ganha de "Isso é impressionante."
- **Use "eu" quando cabe.** Primeira pessoa é honesta, não é falta de profissionalismo. "O que me pega é…" sinaliza uma pessoa de verdade pensando.
- **Deixe entrar um pouco de bagunça.** Estrutura perfeita parece algoritmo. Aparte e pensamento pela metade são humanos.
- **Seja específico sobre o que sente.** Não "isso é preocupante", mas "tem algo inquietante em agente moendo código às 3 da manhã sem ninguém olhando".
- **Mostre experiência vivida.** "era projeto de feira de ciências", "isso já soa antigo", "quem já debugou um…"
- **Deixe o entusiasmo de verdade pontuar.** Um ponto de exclamação no fato que te surpreendeu de verdade ("o maior salto da década veio do pré-processamento!") lê como alguém que se importa com o assunto. Um ou dois por peça. Só vira slop quando a empolgação é fabricada para o leitor em vez de sentida pela coisa.

**Limites:** um ou dois apartes casuais por seção, no máximo. Sem gíria colocada de propósito, sem tentar ser descolado: soa forçado. Não enfie "eu" se a peça não é em primeira pessoa. Nenhum humor que não sirva ao ponto.

> **Limpo mas morto:** O experimento produziu resultados interessantes. Os agentes geraram 3 milhões de linhas de código. Alguns desenvolvedores ficaram impressionados, outros céticos. As implicações ainda não estão claras.
>
> **Vivo:** Eu sinceramente não sei o que sentir sobre esse. 3 milhões de linhas de código, geradas enquanto os humanos supostamente dormiam. Metade da comunidade dev está surtando, a outra metade está explicando por que não conta. A verdade provavelmente está em algum lugar chato no meio, mas eu não paro de pensar naqueles agentes trabalhando a noite inteira.

### Frase de guru e frase sem referente

**O repertório de guru** já vem gasto de fábrica: "a parte que ninguém vê", "não é sobre X, é sobre Y", "o resultado? [lista]", "no fim, fulano não fez X, ele percebeu Y", "e foi aí que tudo mudou", "ninguém te conta isso", "spoiler:".

**A frase sem referente** é pior, porque imita o formato de aforismo sem carregar conteúdo:

> "Não é a semana ruim, é o fio que não some quando o resto melhora."

O teste: tente dizer a frase com outras palavras. Se não dá, ela não significa nada, e quem lê também não entende.

**Frase curta de efeito continua liberada.** Esta seção pede exatamente isso. A diferença é que a boa fala de alguma coisa concreta: "Inferência custa 3× mais" é curta, é forte, e tem referente.

**Provérbio de verdade também não é frase de guru.** "Em casa de ferreiro, o espeto de pau", "a conta vem", "quem paga mal paga duas vezes": essas existem na boca das pessoas há décadas e chegam com o significado pronto, sem precisar de explicação. A frase de guru imita esse formato sem ter nem a idade nem o referente. O teste é a origem, não o formato: se a sua avó reconheceria a frase, é provérbio; se ela parece ter sido inventada para o post, é guru.

---

## O teste de ler em voz alta

Antes de dar a peça por pronta, leia em voz alta, ou imagine lendo para um colega. Marque tudo que:

- Soa como release de assessoria
- Ninguém diria em voz alta numa conversa
- Dá uma leve vergonha
- Está se esforçando demais para parecer inteligente
- Poderia ter sido escrito sobre qualquer assunto trocando meia dúzia de substantivos

O último é o teste mais afiado. Se a peça sobrevive à troca de assunto, nunca foi sobre o assunto.

---

## O que não sacrificar

Voz não passa por cima de precisão. Mantenha:

- Precisão técnica e números específicos
- Nomes próprios, nomes de produto, versões, atribuições
- O argumento central
- Formatação que está fazendo trabalho de verdade, não decoração

Se uma regra daqui forçar uma afirmação factual a ficar vaga, o fato vence. Ficar vago para soar casual é a mesma falha que inflar para soar importante.

E o que este guia não está pedindo:

- **Não é para escrever errado.** Nada aqui pede crase trocada, concordância quebrada ou erro de digitação plantado. Isso aparece em lista de detector porque detector procura sinal, e o objetivo aqui é escrever, não caçar. Texto correto e falado é o alvo.
- **Não é para forçar gíria.** "Mano", "tipo assim" e "sério mesmo" entram quando saem sozinhos. Gíria colocada de propósito soa pior que a formalidade que ela veio consertar.
- **Não é lista de palavra proibida.** Cada bloco tem um critério, e o critério vale mais que a lista. Palavra da lista com trabalho para fazer, fica.
- **Não vale igual para todo formato.** Roteiro de Reel, legenda, thread e post de LinkedIn ocupam pontos diferentes da mesma escala.

---

## Fontes

Os padrões vêm da página [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) da Wikipedia, mantida pelo WikiProject AI Cleanup, mais prática editorial comum. Adaptados aqui como padrão de produção, não como checklist de limpeza.

Os blocos sobre substantivo sem artigo, adjetivo que ninguém falaria e frase de guru vêm do carrossel de [@souantisocialmedia](https://www.instagram.com/souantisocialmedia/) sobre vícios de linguagem de IA em português. O resto é observação de corpus.
