# Base voice

This is the base voice for everything produced in this project: Reel scripts, threads, carousels, LinkedIn posts, captions. It applies to every piece, in every format, with no exceptions.

It is a **base**, not the whole voice. Format-specific and situational rules stack on top of it as layers in `docs/voice/layers/`. When a layer contradicts the base, the layer wins for that piece — but the base is the floor: nothing ships below it.

**Read this before writing, not after.** These are not repairs applied to a finished draft. They are how the draft comes out the first time. Reviewing against this list afterwards is the backstop, not the method.

---

## The core idea

Machine-generated writing has a smell. It is never a single word or trick — it is the combination: predictable structure, hedge-then-assert phrasing, relentless parallelism, inflated significance, and everything wrapped in a tidy bow. Human writing is messier, more opinionated, and varies in rhythm.

**This is not about dumbing the writing down.** It is about sounding like someone who actually knows the subject and has opinions about it. Density is welcome. Polish that erases the person is not.

**Pattern stacking:** when several weak signals land on the same sentence — boldface plus scare quotes plus an em-dash aside on one coined term — that is one strong tell, not three weak ones. Fix it once. Do not count it three times.

---

## 1. Structure

Formulas are the most visible tell. The same section shape repeated ten times. Every paragraph built identically.

**Avoid:**
- Every section ending in a neat takeaway or bottom line
- Repeated callouts: "What this means for you:", "The takeaway:", "Why it matters:"
- Identical paragraph counts per section, identical item counts per list
- "Setup, explanation, conclusion" repeated verbatim across sections
- Formulaic closers: "Challenges and Future Prospects", "Future Outlook"
- "Despite its [strength]… faces challenges… Despite these challenges…" loops

**Instead:**
- Vary section length. Some get two paragraphs. Some get five.
- Let sections end abruptly. Not everything needs a bow.
- Break the pattern deliberately: if three sections are lists, make the fourth prose.
- Fold the "what this means" into the text instead of announcing it.
- Replace challenge/outlook filler with specific facts.

> **Weak:** Despite its impressive benchmark performance, the model faces challenges typical of open-weight releases, including inference cost and hardware requirements. Despite these challenges, with its permissive license and growing community, it continues to gain adoption.
>
> **Better:** Inference costs about 3× more than the API alternative at equivalent throughput. Two inference providers added support in the first week, which is what actually drove adoption.

**A capa fala para o entusiasta médio, não para o especialista.** O leitor brasileiro médio de IA reconhece ChatGPT, OpenAI, SpaceX, Torvalds. Não reconhece harness, page table, change of control, nem “N fatos mostram onde X termina”. A capa precisa de uma frase que alguém falaria, e de um nome ou logo que a pessoa já conhece. A tese técnica entra depois, quando o scroll já aconteceu.

> **Weak:** 6 fatos mostram onde o GPT-6 termina e o discurso de AGI começa.
>
> **Better:** O ChatGPT-6 é ótimo. Mas se acalmem, a AGI ainda não está entre nós.

> **Weak:** 4 elos mostram quem decide quais modelos chegam ao seu IDE
>
> **Better:** A SpaceX comprou o Cursor. E a OpenAI não gostou nada disso.

**Conte o caso até o leitor conseguir repetir o que aconteceu.** Se alguém técnico lê o post e ainda não entende o conflito, o bug ou o teste, o texto falhou. Ensina o objeto primeiro, em analogia ou cena cotidiana; o caveat, o número e a tese vêm depois. Abrir no jargão ou no “mas” é inverter a aula.

> **Weak:** O 99,9% mais chamativo veio com o harness da própria OpenAI.
>
> **Better:** O ARC-AGI-3 é um teste que mede a capacidade de um modelo no eixo AGI. Ele gera um mini-game nunca visto pela IA, o que teoricamente testa a capacidade dela de generalizar inteligência em tarefas novas. Nesse contexto, o ChatGPT-6 foi muito bem, com 99,9% de acerto.
> Mas tem um detalhe importante...

> **Weak:** Numa Battlemage G21 de 16 GiB, o driver Intel Xe entregava parte do armazenamento de compressão como VRAM livre.
>
> **Better:** O computador ligava. Mas a tela de login não parava de reiniciar.

**Não reabra o slide seguinte com a prova do slide anterior.** Se o slide 4 já gastou “24 patches e 18 reinicializações”, o 5 começa no próximo fato. Repetir a contagem no gancho é feio e parece que a história não andou.

> **Weak:** Depois de 24 patches e 18 reinicializações, surgiu uma correção de uma linha.
>
> **Better:** Em determinado momento, o sistema arredondava a memória para cima e liberava 2 KiB que deveriam continuar reservados.

**CTA de carrossel pede um comentário-chave, não uma bifurcação retórica.** O fecho oferece o ativo (artigo, commit, link) em troca de uma palavra no comentário. A pergunta “A ou B?” no último slide parece exercício, não conversa.

> **Weak:** Agora escolha: AGI ou ótimo upgrade?
>
> **Better:** Eu escrevi um artigo detalhando melhor esse comparativo. Comenta “COMPARATIVO” e eu te envio!

> **Weak:** Quando a IA disser “impossível”, você fecha o relatório ou pede outro diagnóstico?
>
> **Better:** Ficou curioso para ver esse processo em detalhes? Comente “COMMIT” que eu te envio o link do commit que exploramos aqui.

---

## 2. Significance inflation and promotional language

The default failure mode is puffing up importance. Everything becomes pivotal, groundbreaking, vibrant. It reads like a press release.

**Significance inflation:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal role, key moment, underscores/highlights its importance, reflects broader, symbolizing its ongoing/enduring/lasting, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, indelible mark, deeply rooted

**Promotional language:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning, nestled, in the heart of

**The fix is rarely a synonym.** Usually you delete the inflation and put a specific fact in its place.

> **Weak:** The lab was founded in 2023, marking a pivotal moment in the evolution of open model research.
>
> **Better:** The lab was founded in 2023 to publish open-weight models, after its founders left a closed lab over release policy.

---

## 3. Vocabulary

Certain words are immediate giveaways.

**Tier 1 — red flags, avoid outright:** delve, landscape (metaphorical), tapestry, paradigm shift, leverage (verb), harness, navigate (metaphorical), realm, embark on a journey, myriad, plethora, multifaceted, groundbreaking, revolutionize, synergy, ecosystem (non-technical), resonate, streamline

**Tier 2 — suspicious in clusters, three or more in one piece is a tell:** robust, seamless, cutting-edge, innovative, comprehensive, pivotal, nuanced, compelling, transformative, bolster, underscore, evolving, fostering, imperative, intricate, overarching, unprecedented

Note that several Tier 2 words are legitimate technical terms in this subject matter. `ecosystem` describing a package registry is fine; `ecosystem` describing a market is not. `robust` as a property of a system under load is fine; `robust` as a compliment is not. Judge by whether the word is doing technical work or decorative work.

**The fix is often structural, not lexical.** The sentence usually needs rebuilding, not a word swap.

> **Weak:** A distinctive feature of the framework is the incorporation of streaming. An enduring testament to its research origins is the widespread adoption of async primitives across the ecosystem, showcasing how these patterns have integrated into production workflows.
>
> **Better:** The framework streams by default. Its async primitives came out of the research prototype and stayed, which is why production code still carries them.

---

## 4. Grammar-level tics

These give the writing away even when the vocabulary is clean.

### Copula avoidance

Elaborate constructions substituted for plain "is", "are", "has". The tell is clustering — a piece that never says "is" and rotates through "serves as", "stands as", "represents", "functions as". One "serves as" in an otherwise normal paragraph is fine.

- "serves as" / "stands as" / "represents" → "is"
- "boasts" / "features" / "offers" → "has"

> **Weak:** The router serves as the entry point. It features four backends and boasts sub-millisecond overhead.
>
> **Better:** The router is the entry point. It has four backends and adds under a millisecond.

Not a tell: "the eval serves as both regression test and benchmark" — that is a normal sentence.

### Superficial -ing analyses

Present participles tacked on to fake depth: "highlighting…", "underscoring…", "emphasizing…", "reflecting…", "symbolizing…", "showcasing…", "contributing to…", "fostering…"

Delete the phrase, or promote it into its own sentence with an actual source behind it.

### Negative parallelism

"Not only… but…" and "It's not just about X, it's about Y". Fine once. The tell is density: in a short piece, once is plenty; twice in a long one. It becomes a crutch fast, and it is especially tempting in hooks — watch for it there.

### Rule of three

Forced triads where the third item is padding: "innovation, inspiration, and insights." Tricolons are ancient and legitimate, so do not flag every group of three. Flag the ones where the third item adds nothing or near-repeats the first two. If it pulls its weight, keep it. If not, cut to two.

### Synonym cycling

Excessive elegant variation: "the model… the system… the network… the architecture" all in one paragraph for the same thing. Pick one term and repeat it. Repetition is fine when it is the clearest word — in technical writing it is usually mandatory.

### False ranges

"From X to Y" where X and Y are not on a meaningful scale.

> **Weak:** The shift has taken us from the first transformer paper to the sprawling model zoo, from single GPUs to the enigmatic dance of distributed training.
>
> **Better:** The piece covers the original transformer paper, the scaling results that followed, and where distributed training stands now.

---

## 5. Rhythm and style

The default cadence is metronomic. Medium sentence. Medium sentence. Medium sentence. Humans vary wildly.

**Avoid:** every sentence 15–25 words, no short punchy lines, nothing that runs long and builds, every sentence opening on a noun or "The".

**Instead:** throw in short ones. "That's new." "It works." "Not anymore." Let a sentence run when the idea needs room. Start some with "But", "And", "So". Fragments are fine outside academic registers.

### Paragraph density

Sentence rhythm has a twin one level up, and it fails the same way. The tell is the piece where every paragraph is one sentence, separated by a blank line, all the way down. It reads as a teleprompter feed rather than as someone writing: every line lands with the same weight, nothing accumulates, and the reader gets no signal about which idea is load-bearing.

**A paragraph is a unit of thought, not a unit of display.** Most of them run three to six sentences that belong together, because they are developing one thing. The one-sentence paragraph is a beat, and it works precisely because it is rare — it stops working the moment it becomes the default.

> **Weak:**
> The system gets it wrong once in a hundred runs.
>
> That sounds fine.
>
> But the application runs a thousand times a day.
>
> That's ten broken outputs nobody sees.
>
> **Better:** The system gets it wrong once in a hundred runs, which sounds fine until you look at the volume: the application runs a thousand times a day, so that is ten broken outputs a day and nobody is reading them.

Vary it on purpose. A piece where one paragraph runs six sentences, the next runs two, and the one after is a four-word fragment is a piece written by a person.

### Deliberate repetition

Section 1 kills parallelism that sits in the background — every section built the same, every list the same length. That is a different thing from repetition used as a figure: on purpose, in one place, building to something.

> Quem já construiu coisa de verdade com IA sabe reconhecer esse teatro de longe.
> Sabe a diferença entre protótipo de palco e sistema em produção.
> Sabe que empresa não se sustenta com thread viral e print bonito.
> Sabe também que arquitetura séria exige engenharia, avaliação, contexto, governança.

Four sentences opening on the same verb, and it works, because it is doing rhetorical work and then it stops. The test is whether the repetition is *heard*. Background parallelism is invisible and uniform; a figure is audible and it ends.

### Em dashes

Used to inject dramatic asides. The tell is frequency and function both.

- **Frequency:** more than one per three or four paragraphs is above human baseline.
- **Function:** even one is a tell when it does the classic move — a dramatic explanatory aside dropped mid-sentence to sound punchy.

Use commas or periods. Restructure. Count them before claiming there are too many.

### Boldface

Mechanical emphasis, especially inside lists. Remove most of it. Save it for genuinely important terms on first mention.

In a carousel, bold also belongs on the turn (“Mas tem um detalhe importante...”, “Modelo melhor? / AGI?”) and on the name of the object the slide is teaching (ARC-AGI-3). Mechanical bold inside a list stays forbidden.

### Inline-header lists

> **Weak:**
> - **Speed:** The system is faster.
> - **Quality:** Output quality has improved.
> - **Security:** Security has been strengthened.
>
> **Better:** The update cuts p99 latency roughly in half, fixes the truncation bug in long contexts, and moves the token store off disk.

### Emojis

None, in any deliverable.

### Title case in headings

Weak signal on its own — title case is standard in several style guides. Only a tell alongside other patterns. Do not flag it in isolation.

In a pt-BR piece, a headline set entirely in caps is not title case: it is a poster. Carousel headlines go in sentence case, as if spoken.

> **Weak:** 4 ELOS MOSTRAM QUEM DECIDE QUAIS MODELOS CHEGAM AO SEU IDE
>
> **Better:** A SpaceX comprou o Cursor. E a OpenAI não gostou nada disso.

### Curly quotes

Typographically correct and expected in formatted content. Only a tell in plain-text or code contexts where straight quotes are the norm.

---

## 6. Hedging, filler, vague attribution

Hedging comes from trying to sound balanced. People with expertise are more direct.

**Hedging to cut:** "It's important to note that…", "It's worth mentioning…", "While there are certainly challenges…", "This is not without its drawbacks…", "To be sure…", "To be fair…", opening with "Certainly," or "Absolutely," and stacked qualifiers like "could potentially possibly be argued that… might have some".

Say the thing. Take the side the piece obviously leans toward. One hedge per piece is fine. Five is the tell.

**Filler:**
- "In order to achieve this" → "To do this"
- "Due to the fact that" → "Because"
- "At this point in time" → "Now"
- "The system has the ability to" → "The system can"
- "It is important to note that the data shows" → "The data shows"

**Vague attribution:** "Industry reports", "Experts argue", "Observers have cited". Name the source, give the date, or drop the claim.

> **Weak:** Experts believe the technique plays a crucial role in production reliability.
>
> **Better:** The technique cut hallucination rate by 40% on the held-out set, according to the 2026 paper that introduced it.

**Chatbot artifacts:** "I hope this helps!", "Let me know if you'd like me to expand on any section!", "Great question!", "Certainly!" Delete entirely — these should never survive into a draft.

**Knowledge-cutoff disclaimers:** "While specific details are limited…", "Based on available information…" Find the source or drop the claim. ("As of [date]" is different — it is standard practice for time-sensitive data and belongs in this subject matter.)

**Sycophancy:** no flattery, no "you're absolutely right". Respond to the substance.

**Generic positive endings:** "The future looks bright", "Exciting times lie ahead", "Only time will tell." End on a specific fact, a position, or just stop.

---

## 7. Connective tissue

The same transitions, over and over.

**Overused:** "Moreover", "Furthermore", "Additionally", "In conclusion", "To sum up", "That said", "That being said", "With that in mind", "Moving forward", "When it comes to".

Usually no transition is needed at all — start the next thought. When one is needed, use the real logical connection: because, so, but, and. Reference the previous idea directly instead of reaching for a generic connector. Let paragraph breaks carry the weight.

**That rule is about moving between paragraphs. Inside one, the opposite applies.** Sentences developing the same idea get joined: a comma and a "because", a colon, a "so", a "but", a relative clause. Stripping those out is what produces the metronome from section 5 — four correct sentences standing side by side, none of them touching.

> **Weak:** O prompt é estatístico. Ele acerta 99% das vezes. Uma aplicação roda mil vezes por dia. São dez erros.
>
> **Better:** O prompt é estatístico, e 99% de acerto vira dez erros por dia numa aplicação que roda mil vezes.

Cutting a generic connector is an improvement. Cutting the logical connection is damage.

---

## 8. Voice and texture

Avoiding the patterns above is half the job. Sterile, voiceless writing is just as recognizable as slop.

**Signs of soulless writing, even when technically clean:** uniform sentence length, no opinions, no acknowledged uncertainty, no first person where it fits, no humor or edge, reads like an encyclopedia entry.

**How to put a person in it:**

- **Have opinions.** React to the facts, do not just report them. "I genuinely don't know how to feel about this" is more human than a neutral pro/con list.
- **Acknowledge complexity.** "This is impressive and also kind of unsettling" beats "This is impressive."
- **Use "I" when it fits.** First person is honest, not unprofessional. "Here's what gets me…" signals a real person thinking.
- **Let some mess in.** Perfect structure feels algorithmic. Asides and half-formed thoughts are human.
- **Be specific about feelings.** Not "this is concerning" but "there's something unsettling about agents grinding away at 3am with nobody watching."
- **Show lived experience.** "used to be a science project", "that already sounds quaint", "anyone who's debugged a…"
- **Let real enthusiasm punctuate.** An exclamation mark on the fact that genuinely surprised you — "the biggest jump of the decade came from preprocessing!" — reads as someone who cares about the subject. One or two in a piece. It is only slop when the excitement is manufactured for the reader instead of felt about the thing.

**Limits:** one or two casual asides per section, maximum. No slang, no trying to be hip — it reads as forced. Do not insert "I" if the piece is not already first person. No humor that does not serve the point.

> **Clean but dead:** The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were skeptical. The implications remain unclear.
>
> **Alive:** I genuinely don't know how to feel about this one. 3 million lines of code, generated while the humans presumably slept. Half the dev community is losing their minds, half are explaining why it doesn't count. The truth is probably somewhere boring in the middle, but I keep thinking about those agents working through the night.

---

## 9. Brazilian Portuguese

Sections 1–8 are written against English drafts. When a piece ships in pt-BR, this section stacks on top of them, and it is deliberately written in Portuguese: the prose here doubles as a working sample of the register it describes. Reading rules about spoken Portuguese in English calibrates nothing.

### O ponto de partida

O português que sai por padrão vem de um lugar específico: petição, artigo acadêmico e redação de vestibular. Esse é o registro que domina o texto formal em português na internet, então é ele que aparece quando ninguém pede outra coisa. O problema não é a formalidade em si. É que esse registro pertence a documento, e a gente escreve para vídeo, carrossel e post.

**Nada aqui pede texto errado.** Toda regra abaixo escolhe, entre duas formas corretas, a que alguém usaria falando. Vale a mesma lógica do topo do documento: um caso isolado não é sinal, o empilhamento é.

### 9.1 Verbo com "-se" no lugar de sujeito

O alvo é o `-se` que apaga quem fez a ação: *trata-se de*, *faz-se necessário*, *nota-se*, *observa-se*, *pode-se dizer*, *torna-se*, *encontra-se*, *percebe-se*. Junto com ele vem a passiva sem agente e o *é recomendado que*.

> **Fraco:** Trata-se de um erro comum, e nota-se que ele aparece mais em carrossel.
>
> **Melhor:** Esse erro é comum, e aparece mais em carrossel.

> **Fraco:** É recomendado que o roteiro seja lido em voz alta antes da gravação.
>
> **Melhor:** Leia o roteiro em voz alta antes de gravar.

**Não confunda com pronome reflexivo ou verbo pronominal.** *Ela se conecta*, *o post se espalhou*, *a gente se acostuma*, *não se sente bem*: todos normais, todos ficam. O critério é outro: pergunte "quem?" para a frase. Se a frase se recusa a responder, o `-se` está escondendo o sujeito.

A mesóclise (*far-se-á*, *dir-se-ia*) não tem uso nenhum em nenhum formato daqui.

### 9.2 Substantivo sem artigo e sem plural

Em inglês, o substantivo contável dispensa artigo no plural: *avoid bad posts*. Em português não dispensa, e a estrutura do inglês atravessa junto com a tradução. O resultado passa na gramática e trava no ouvido, geralmente sem que o leitor consiga apontar o motivo.

> **Fraco:** É melhor escrever tudo na mão para evitar post ruim.
>
> **Melhor:** …para evitar um post ruim. / …para evitar posts ruins.

**Isso não quer dizer que todo substantivo pede artigo.** *Eu gosto de música*, *ele vive de conteúdo*, *sem medo*: aí o substantivo é genérico e não conta unidade, então está certo do jeito que está. O alvo é o substantivo contável na posição de objeto, do tipo que dá para contar: um post, dois posts.

### 9.3 Palavra comprida onde cabe palavra curta

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

**Nenhuma dessas palavras está proibida.** O teste é se existe uma palavra curta que diz a mesma coisa *naquela frase*. "Realizar um sonho" fica, porque "fazer um sonho" não é a mesma coisa. "Realizar uma análise" vira "analisar". E em peça técnica algumas delas carregam sentido de verdade: *otimizar* uma query é trabalho técnico, *otimizar* o seu dia é enfeite. Julgue pela função, igual à seção 3.

### 9.4 Quem está falando

Três hábitos que empurram o texto para longe da fala, agrupados porque aparecem juntos.

**Pronome oblíquo antes do verbo:** *isso lhe permite*, *conferindo-lhe*, *ao fazê-lo*, *eu o vi*. Nenhum formato daqui aguenta essa fileira. Na fala o pronome vira tônico ("eu vi ele") ou some ("Viu o vídeo?" "Vi.").

**Futuro em -rá:** *você notará*, *isso trará*, *poderá*. Vira "você vai notar", "isso vai trazer". Cuidado com o exagero: *será* e *vai ser* convivem sem problema, e o alvo é a forma empilhada, não uma ocorrência.

**Primeira pessoa do plural:** *precisamos*, *fizemos*, *observamos*. Em roteiro e legenda isso quase sempre é "a gente precisa", "a gente fez".

**O formato move o limite.** Roteiro de Reel é fala transcrita e aguenta o registro mais solto que existe nesta seção. Post técnico de LinkedIn aguenta menos, e "nós" ali pode ser a escolha certa. O que nenhum dos dois aguenta é o clítico culto.

### 9.5 Conectores de redação

A seção 7 já trata de conector genérico, mas o repertório em português é outro, e vem inteiro da redação escolar:

*Ademais* · *Outrossim* · *Por conseguinte* · *Dessa forma* · *Sendo assim* · *Nesse sentido* · *Diante do exposto* · *Em suma* · *Vale ressaltar que* · *Cabe destacar* · *É importante frisar* · *Convém salientar* · *Em contrapartida*

Some a família inteira do *É importante...*: *é importante lembrar que*, *é fundamental entender*, *vale lembrar que*.

Na maior parte dos casos o conector escolar não precisa existir, e a frase seguinte começa sozinha. Quando precisa, use a ligação real: mas, só que, porque, aí, então. *No entanto* uma vez num texto longo não é crime.

**O outro lado do mesmo defeito:** cortar o conector de redação e não recolocar a ligação falada. O resultado é o português de IA: declaração, ponto, declaração, ponto.

> **Fraco:** As duas notas são verdadeiras. Elas só respondem a perguntas diferentes.
>
> **Melhor:** Portanto, não existe um resultado verdadeiro e outro falso. Existem dois resultados verdadeiros medindo coisas diferentes, embora apenas um deles tenha ido parar no centro do lançamento.

Em parágrafo de peça em pt-BR, *só que*, *porque*, *aí*, *então*, *mesmo assim*, *ainda assim* não são enfeite. São o tecido. A seção 5 pede frase curta como beat em inglês; aplicada dentro do parágrafo em português, vira o empilhamento que denuncia a máquina. Aqui esta seção ganha da 5.

### 9.6 Decalque do inglês

Construções que passam na gramática e não passam no ouvido, porque foram pensadas em inglês:

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

A lista Tier 1 da seção 3 traduz quase inteira e continua valendo: *delve* vira "mergulhar", *landscape* vira "cenário", *journey* vira "jornada", *tapestry* vira "tapeçaria".

**Algumas dessas expressões já são português de verdade.** "Divisor de águas" existia muito antes do ChatGPT, e "no final do dia" está na boca de qualquer pessoa que trabalha em empresa. Sozinha, nenhuma delas prova nada. Elas contam quando aparecem em cima das outras coisas desta seção.

O decalque também mora no heading e no fecho aforístico: a frase foi pensada como título de newsletter em inglês e só depois traduzida.

> **Fraco:** O mesmo benchmark produziu dois GPT-6. / O ganho mais útil aparece quando o modelo admite que não sabe.
>
> **Melhor:** O mesmo GPT-6 tirou 62,7% e 99,9% na mesma prova. / O GPT-6 ainda alucina muito, só que quase a metade.

### 9.7 Adjetivo que ninguém falaria

*Realidade brutal*, *impacto real*, *tentativa bonita*, *verdade crua*, *escolha corajosa*. O adjetivo foi escolhido pelo peso, não pelo encaixe, e o par só existe no papel.

O teste: você já disse essa combinação em voz alta para alguém? Se a resposta for não, troque o adjetivo ou corte ele.

**Isso não é um pedido para tirar adjetivo forte.** *Erro caro*, *decisão idiota*, *resultado ridículo* são fortes e são falados. Repare que o problema também não é o adjetivo vazio da seção 2, que é outro defeito: ali a palavra não diz nada, aqui ela diz, só que na combinação errada.

### 9.8 Frase de guru e frase sem referente

**O repertório de guru** já vem gasto de fábrica: "a parte que ninguém vê", "não é sobre X, é sobre Y", "o resultado? [lista]", "no fim, fulano não fez X, ele percebeu Y", "e foi aí que tudo mudou", "ninguém te conta isso", "spoiler:".

**A frase sem referente** é pior, porque imita o formato de aforismo sem carregar conteúdo:

> "Não é a semana ruim, é o fio que não some quando o resto melhora."

O teste: tente dizer a frase com outras palavras. Se não dá, ela não significa nada, e quem lê também não entende.

**Frase curta de efeito continua liberada.** A seção 8 pede exatamente isso. A diferença é que a boa fala de alguma coisa concreta: "Inferência custa 3× mais" é curta, é forte, e tem referente.

**Provérbio de verdade também não é frase de guru.** "Em casa de ferreiro, o espeto de pau", "a conta vem", "quem paga mal paga duas vezes": essas existem na boca das pessoas há décadas e chegam com o significado pronto, sem precisar de explicação. A frase de guru imita esse formato sem ter nem a idade nem o referente. O teste é a origem, não o formato: se a sua avó reconheceria a frase, é provérbio; se ela parece ter sido inventada para o post, é guru.

### 9.9 Pontuação

**Travessão.** A seção 5 já limita a frequência, e em português o limite aperta mais, porque a alternativa é melhor: o aparte no meio da frase pede vírgula, dois-pontos ou parênteses. O travessão dramático é hábito tipográfico importado do inglês, e a essa altura virou piada pronta.

**Ponto e vírgula.** Não aparece em post nem em legenda. Ele engessa a frase e denuncia na hora.

### 9.10 Português pensado em inglês

**A frase inteira foi pensada em inglês e só depois vestida de português.** A lista da 9.6 pega o decalque de expressão. Este item pega a arquitetura: título em caixa alta, “N fatos mostram X”, heading de tese, metáfora importada, sentença curta + ponto + sentença curta, sem o continuísmo que o ouvido brasileiro espera. O teste é o mesmo da 9: você falaria isso assim? Se a resposta for “só se eu estivesse traduzindo um headline”, reescreve. Não basta trocar o vocabulário.

> **Fraco:** 4 ELOS MOSTRAM QUEM DECIDE QUAIS MODELOS CHEGAM AO SEU IDE
>
> **Melhor:** A SpaceX comprou o Cursor. E a OpenAI não gostou nada disso.

> **Fraco:** Ele não esperou um palpite genial. Cada dúvida virava mais código de diagnóstico, uma nova reinicialização e outra rodada de análise. A IA fazia o trabalho repetitivo. Ele decidia o próximo teste.
>
> **Melhor:** Ele não esperou um palpite genial: cada dúvida virava mais código de diagnóstico, que levava a uma nova reinicialização e gerava outra rodada de análise, enquanto a IA fazia o trabalho repetitivo e ele decidia o próximo teste.

### 9.11 Advérbio de intensidade da fala

**Em pt-BR, tirar *muito*, *bem*, *bastante*, *realmente*, *ainda*, *tão* para “soar técnico” deixa o texto estéril.** Isso não é o adjetivo inflado da seção 2. É o jeito normal de uma pessoa pesar o que está dizendo.

> **Fraco:** O GPT-6 é excelente. O 99,9% não prova AGI.
>
> **Melhor:** O GPT-6 melhorou muito. Só não virou AGI.

> **Fraco:** Era uma boa história. Também estava errada num detalhe que muda quase tudo.
>
> **Melhor:** Só que eu estava simplificando demais. […] A nota é real, o resultado é realmente impressionante…

A seção 2 continua valendo para *impacto real*, *escolha corajosa*, *groundbreaking*. Não use ela para limpar o português falado.

### O que esta seção não está pedindo

- **Não é para escrever errado.** Nada aqui pede crase trocada, concordância quebrada ou erro de digitação plantado. Isso aparece em lista de detector porque detector procura sinal, e o objetivo aqui é escrever, não caçar. Texto correto e falado é o alvo.
- **Não é para forçar gíria.** "Mano", "tipo assim" e "sério mesmo" entram quando saem sozinhos. Gíria colocada de propósito soa pior que a formalidade que ela veio consertar.
- **Não é lista de palavra proibida.** Cada bloco tem um critério, e o critério vale mais que a lista. Palavra da lista com trabalho para fazer, fica.
- **Não vale para peça em inglês.** Ali as seções 1 a 8 já bastam.
- **Não vale igual para todo formato.** Roteiro de Reel, legenda, thread e post de LinkedIn ocupam pontos diferentes da mesma escala.

**Fonte:** os itens 9.2, 9.7 e 9.8 vêm do carrossel de [@souantisocialmedia](https://www.instagram.com/souantisocialmedia/) sobre vícios de linguagem de IA em português. O resto é observação de corpus.

---

## The read-it-out-loud test

Before a piece is done, read it out loud, or imagine reading it to a colleague. Flag anything that:

- Sounds like a press release
- No one would say out loud in conversation
- Makes you cringe slightly
- Is trying too hard to sound smart
- Could have been written about any topic by swapping a few nouns

That last one is the sharpest test. If the piece survives having its subject swapped, it was never about the subject.

---

## What not to sacrifice

Voice does not override accuracy. Keep:

- Technical accuracy and specific numbers
- Proper nouns, product names, versions, attributions
- The core argument
- Formatting that is doing real work, not decoration

If a rule here would force a factual claim to become vague, the fact wins. Being vague to sound casual is the same failure as being inflated to sound important.

---

## Source

The patterns come from Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup, plus standard editorial practice. Adapted here as a production standard rather than a cleanup checklist.
