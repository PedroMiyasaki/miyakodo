# Craft de carrossel

Referência de trabalho para carrosséis. Derivada de um corpus de cinco carrosséis virais em
`examples/carousels/` (`calebraalston`, `habitosqueabracam`, `okaashish`, `souantisocialmedia`,
`yasminkbs`): toda regra abaixo é uma prática observada nos **cinco**, em dois idiomas e cinco
nichos sem relação entre si, mais o craft de composição que sobreviveu ao contato com esse corpus.

**Leia antes de escrever copy e antes de escrever HTML.** A skill `carousel` lê este arquivo a cada
execução e aplica ele às duas metades da peça. Os princípios são um sistema só: um template travado
não salva uma copy que enterra a conclusão, e uma boa headline não sobrevive a um slide que tem
outras quatro coisas em cima.

---

## 0 · Os slots de identidade

O sistema visual ainda não está definido. Ele não precisa estar para este documento funcionar, só
que não dá para compor um carrossel enquanto esses slots não tiverem valor. **Pergunte ao usuário,
ou leia do documento de identidade quando ele existir, antes de escrever qualquer HTML.** Declare
os slots uma vez no `<style>` da peça e nunca desvie de um slide para outro.

| Slot | O que é | Faixa no corpus |
|---|---|---|
| `GROUND` | O fundo. Uma cor chapada, em todo slide. | teal escuro / papel quente / branco / lima / creme |
| `INK` | A cor do texto. | creme / marrom / preto / azul-marinho / azul klein |
| `ACCENT` | **Exatamente um.** Marca um significado consistente do começo ao fim. | sálvia claro / teal / um azul / nenhum |
| `DISPLAY` | Fonte da headline. | serifada, slab, manuscrita, grotesca |
| `BODY` | Fonte do body. Pode ser a mesma do DISPLAY. | sans, serifada, a mesma do display |
| `MARK` | Mobília de marca: masthead, handle ou marca de canto. Mesmo lugar, mesmo tamanho, em todo slide. | lockup do logo / linha tracejada + ponto / handle / asterisco + rótulo |
| `ART` | A linguagem de ilustração. Um estilo, usado em tudo. Pode ser `none`. | line art / colagem ukiyo-e / doodle + mascote / desenho a caneta / nenhum |
| `TEXTURE` | Tratamento opcional do fundo. Sutil ou ausente. | grão de papel / ruído / chapado |

Regras que valem independentemente do que preenche os slots:

- **No máximo duas famílias tipográficas.** Três das cinco contas do corpus usam uma. O tamanho é a
  hierarquia. Não existe uma terceira família para "meta".
- **Um accent, um significado.** No `okaashish`, azul quer dizer *isto é o número ou a palavra do
  ganho*, toda vez, sem exceção. No `habitosqueabracam`, teal quer dizer *isto é o fato que você
  não sabia*. Um accent que marca três coisas diferentes é decoração, não sinal.
- **`ART: none` é viável, mas é o modo difícil.** O `yasminkbs` roda 15 slides só com tipografia e
  funciona, porque o bloco de texto é enorme e cada frase é uma cena que o leitor reconhece. Quatro
  das cinco contas usam uma linguagem de ilustração, e ela é o principal ativo de reconhecimento no
  thumbnail.
- **A identidade tem que sobreviver ao teste do thumbnail:** encolha um slide para 20% e corte o
  handle. Se não dá para identificar que é esta conta, os slots estão fracos demais.

---

## P1 · A capa vende uma unidade contável, não um tema

A capa diz duas coisas ao leitor antes do primeiro swipe: **qual é a unidade** e **mais ou menos
quantas tem.** Não o assunto: a forma da coisa que ele vai consumir.

> "Hábitos japoneses que você vai querer copiar" → uma lista de hábitos para roubar
> "I researched **1540** Reddit posts… here's what I found" → achados de um dataset real
> "Quantity **or** Quality content" → um binário, resolvido por um método

Um tema é um convite para *talvez* deslizar. Uma unidade contável é um contrato: o leitor sabe que
o slide 2 traz um hábito / uma estatística / um momento, e que existe um fim. Promessa finita é
promessa que o leitor termina.

- **Um número faz o trabalho de um parágrafo.** `1540 Reddit posts` é o argumento de credibilidade
  inteiro de um carrossel de 13 slides, em três palavras. Neste nicho: o nome de um modelo, um
  preço, um número de benchmark, um lançamento com data, uma contagem de coisas testadas.
- **Diga o ganho, não o processo.** "que você vai querer copiar", "Here's what I found", "hoje
  mesmo". O leitor fica sabendo o que leva embora.
- A capa é o maior gesto tipográfico da peça. Display no topo da escala.

**Cheque:** a capa nomeia uma unidade e sugere uma contagem? Se ela nomeia um assunto, reescreva.

---

## P2 · Uma ideia por slide, headline primeiro: as headlines sozinhas são o artigo

Todo slide segue a mesma gramática interna:

```
HEADLINE   ← a conclusão, uma frase completa que se sustenta sozinha, legível em ~1,5s
body       ← o apoio: por quê, como, a ressalva, o exemplo              (opcional)
proof      ← o print, o diagrama, a ilustração                          (opcional)
```

A headline **nunca é um rótulo e nunca é um teaser**: ela é o achado em si. Não "Automation", mas
"**More than 60% are adding AI to traditional services.**" O body então dá contexto e ressalva.
Isso é pirâmide invertida: **conclusão primeiro, preparação depois.**

> Isso inverte a regra antiga de "estabelecer → evidência → efeito". O corpus não gasta um slide,
> nem o topo de um slide, com preparação. O que ele faz é deixar a headline autossuficiente: o
> número chega sempre com o sujeito grudado, nunca como um número pelado.

**O teste de leitura corrida, o cheque mais útil deste documento inteiro.** Leia só as headlines,
de cima a baixo. Se isso sozinho for um artigo coerente, o carrossel funciona. Se ler como
fragmentos, as headlines são rótulos e a peça vai perder todo mundo que passa o olho.

O leitor consome carrossel em duas velocidades ao mesmo tempo: uma passada rápida pela camada das
headlines e uma leitura lenta dos dois ou três slides que pegaram. O mesmo arquivo atende as duas
audiências. Um slide que precisa do anterior para fazer sentido quebra a camada rápida e perde quem
passa o olho para sempre.

**Uma ideia por slide, sem exceção.** Não um tema: uma ideia. Três passos são três slides. Uma
fórmula de quatro partes é uma ideia e pode dividir um slide, separada em quatro linhas visualmente
distintas.

---

## P3 · Trave um template e gaste a novidade no conteúdo, nunca no layout

A coisa mais disciplinada que o corpus faz, e a mais fácil de errar.

**O template nunca muda.** Mesmos slots, mesma hierarquia, mesmas posições, slide após slide.
`yasminkbs`: 15 slides, header idêntico, tamanho de tipo idêntico, margem idêntica, só a frase
muda. `habitosqueabracam`: um masthead fixo (linha tracejada, ponto da marca, termo em display,
tradução em caixa alta condensada, body serifado, pull-quote no accent), cinco vezes sem desvio.

> Isso inverte a restrição antiga de "sem template, cada slide composto na hora". Aquela regra
> produzia uma variedade que o leitor sente como atrito. O olho reaprende um layout novo em mais ou
> menos meio segundo. Em 12 slides são seis segundos de atenção gastos em navegação.

O que pode se mover: `souantisocialmedia` e `calebraalston` deslocam o bloco de texto e a
ilustração pelo canvas entre um slide e outro, para a sequência não parecer copiar e colar. Os
**elementos e a hierarquia deles ficam congelados**. Só a posição no canvas respira.

**Layout, consistente nos cinco:**

- **4:5, 1080×1350.** O máximo de espaço vertical no feed.
- **A headline é dona do terço de cima.** Todo slide, toda conta. O terço de baixo é ilustração ou
  ar de propósito: é ali que moram a interface do Instagram, a prévia da legenda do post e o dedão
  do leitor.
- **Margem de segurança ≈ 88px (8%).** O corpus roda entre 8 e 9%, não os 4% que uma margem de
  48px dá.
- **Escala tipográfica, medida no corpus a 1080 de largura:**

  | Nível | Tamanho | Notas |
  |---|---|---|
  | Hook da capa | 90–130px | O maior gesto da peça |
  | Headline do slide | 70–110px | Entrelinha apertada: um bloco, não um parágrafo |
  | Body | 40–56px | Abaixo de ~36px fica ilegível no feed |
  | Body de carrossel de leitura | 38–44px | Só nesse modo de densidade, veja a divisão abaixo |

- **Espaço em branco é um nível de hierarquia.** O `yasminkbs` deixa uns 40% da maioria dos slides
  vazios e isso passa confiança. Funciona porque o bloco de texto é enorme, veja a seção sobre
  espaço morto.
- **Sem indicador de página.** Nenhuma das cinco tem. O Instagram já desenha as bolinhas.

**Duas densidades. Escolha uma por peça, de propósito.**

- **Carrossel de leitura** (`habitosqueabracam`): 6 a 8 linhas de body por slide, serifada em
  tamanho grande. Troca alcance por profundidade. Use quando o valor *é* a informação.
- **Carrossel de reconhecimento** (`yasminkbs`): uma frase por slide. Troca profundidade por
  velocidade de swipe e por marcação. Use quando o valor é "isso é literalmente o meu time".

Um carrossel que fica no meio do caminho entre os dois funciona pior que qualquer um deles.

---

## P4 · Toda afirmação ancora em algo que o leitor consegue visualizar

Nenhum slide do corpus argumenta com adjetivos. Cada afirmação se resolve numa de quatro formas:

1. **Um número.** `1540 posts`, `60%`, `<5%`, `$3k–$5k`, `£250`, `20–30 minutes`.
2. **Um artefato.** O `okaashish` prega um print real em quase todo slide. Muitas vezes é ilegível
   no tamanho do feed, e tudo bem: ele não está ali para ser lido, está ali para provar que a
   afirmação veio de algum lugar. *Neste nicho: uma thread, um repo, uma página de preços, uma
   tabela de benchmark, um dashboard.*
3. **Uma coisa com nome.** `Tsundoku`, `Ichigo ichie`, "the Accordion Method". Um conceito com
   nome viaja: o leitor consegue repetir para outra pessoa, e é esse o mecanismo por trás do
   compartilhamento.
4. **Uma cena exata.** A forma mais afiada, e a que o corpus mais usa:

   > "sem um áudio de 7 minutos antes", e não *comunicação ruim*
   > "a única coisa nova que entra na sua cabeça é notificação do Teams", e não *você está estagnado*
   > "não conta ir num restaurante diferente ou cortar a franja", antecipando a desculpa do leitor

Especificidade produz reconhecimento, e reconhecimento é o que gera comentário e compartilhamento.
"Seja um líder melhor" ganha um like. "Quando alguém manda 'resolvido' sem um áudio de 7 minutos
antes" vira marcação para um colega. Ninguém marca alguém numa abstração.

**Faça a ressalva às claras.** O `okaashish` escreve "**I did not verify, though**" e "**Not
verified**" direto nos slides. A honestidade dá autoridade: soa como alguém que foi mesmo até a
fonte, não como alguém vendendo a conclusão. Nomeie a fonte, dê a data, ou derrube a afirmação.

---

## P5 · Os dois últimos slides: a virada, depois um pedido de baixo esforço

**O penúltimo slide é o ganho, nunca o item mais fraco da lista.** É onde a sequência para de
listar e começa a significar alguma coisa:

> `okaashish` s12: "The real AI money formula", a resposta que os dez slides anteriores mereceram.
> `habitosqueabracam` s7: "cada um deles resolve uma necessidade que a gente também tem, só nunca
> ganhou nome aqui."
> `calebraalston` s5: "Repeat the cycle", fecha o ciclo que a metáfora abriu.

**O último slide pede exatamente uma coisa que o leitor já sabe responder.** Duas formas:

*Comentário com palavra-chave*: uma palavra, entre aspas, com uma recompensa dita maior que o que
acabou de ser entregue:
> "Comment **'Select'** - if you want the full system for how to make content that gets you customers."
> "Comment **'REDDIT'** - and I'll share the full breakdown."

*Pergunta com resposta pronta*: sem trabalho cognitivo nenhum:
> "Se você pudesse roubar só um desses hábitos este mês, qual seria?"

Nunca "o que você acha?". As duas formas estreitam a resposta para uma escolha que o leitor já fez
enquanto lia. O pedido de follow, se existir, vem depois e é jogado como piada, nunca como o CTA
principal.

**O slide de CTA pode quebrar o registro visual.** O `calebraalston` vira de teal escuro para
dourado no último slide. O `calebraalston` também roda o CTA no **rodapé de todo slide**, então o
pedido nunca depende de chegar ao fim. Vale roubar. Os dois slides de CTA do corpus estão
centralizados no meio, com o maior tipo do deck: o CTA é o slide que mais grita, não o mais sóbrio.

*Exceção, anotada para não ser copiada sem querer:* o `yasminkbs` não tem CTA. Termina no 15º item
e para. Só é viável quando o conteúdo é identificação pura e o compartilhamento **é** o CTA. Quatro
de cinco têm um pedido explícito. Trate "sem CTA" como a exceção que é.

---

## Camada de craft · espaço morto, peso óptico, feedback

**"Muito espaço vazio" quase sempre quer dizer espaço morto, não espaço negativo demais.**

| | Espaço negativo intencional | Espaço morto (falha) |
|---|---|---|
| Função | Emoldura o conteúdo, força o foco | Tela que sobrou porque o conteúdo é leve demais |
| Sensação | Deliberado, respira | Inacabado, "só texto lá em cima" |
| Peso óptico | O bloco principal é denso e grande | Título minúsculo + body minúsculo + vazio enorme embaixo |
| Thumbnail | O hook ainda domina | Parece uma página em branco com uma linha |

Corrija espaço morto com **escala, massa tipográfica e agrupamento**, nunca espalhando
micro-elementos pelos cantos. O `yasminkbs` é a prova: 40% vazio, e passa confiança porque o bloco
de texto carrega todo o peso.

**Termos para usar ao planejar e ao explicar uma correção:**

- **Âncora visual**: o elemento que carrega o slide. Todo slide precisa de exatamente uma.
- **Peso óptico**: quanto um elemento pesa na composição.
- **Massa tipográfica**: texto como bloco sólido, escala alta mais entrelinha apertada, não
  parágrafo de blog.
- **Agrupamento (proximidade)**: a mesma ideia fica junta. Ideias diferentes ganham um intervalo
  claro.
- **Equilíbrio assimétrico**: peso num canto compensado por peso em outro.
- **Contraste figura-fundo**: o texto tem que saltar do fundo no thumbnail.

**Convertendo feedback subjetivo em ajuste:**

| O usuário diz | Diagnostique |
|---|---|
| "vazio" | Espaço morto ou espaço negativo? Falta âncora? Escala tipográfica tímida demais? |
| "sem impacto" | Hierarquia fraca, contraste baixo, massa tipográfica insuficiente |
| "não entendi" | Headline é rótulo em vez de conclusão, ou jargão sem efeito na mesma tela |
| "sem graça" | Template travado certo, mas a copy falhou no P4: sem número, artefato, nome ou cena |

---

## Contrato de frame (rígido)

1. Cada slide é um `<section class="slide">`, exatamente `width: 1080px; height: 1350px; overflow: hidden`.
   O renderizador lê o seletor `.slide`.
2. Padding interno mínimo de **88px** em todos os lados.
3. `GROUND` chapado. Nunca degradê. Inverter para escuro é decisão da peça inteira, nunca de um
   slide.
4. `data-theme="light"` na raiz, para o render não herdar o modo escuro do sistema.
5. Fontes: só as famílias `DISPLAY` / `BODY`. Declaradas uma vez, no topo.
6. Seguro para render: estado final estático. Sem `:hover`, sem animação, sem JS para conteúdo que
   precisa aparecer.
7. `MARK` no mesmo canto, no mesmo tamanho, em todo slide.

```bash
uv run python scripts/render_html_to_pngs.py \
  --html "posts/carousel/<slug>/sketch/carousel.html" \
  --out "posts/carousel/<slug>" \
  --selector ".slide" --width 1080 --height 1350
```

---

## Proibido

Foto de stock. Degradê. Emoji. Biblioteca de ícones. Travessão (-). Card com sombra + borda no
accent. Ênfase misturada (negrito + cor + sublinhado + caixa na mesma frase). Uma terceira família
tipográfica. Mais de uma cor de accent. Slide decorativo sem frase: todo slide do corpus, os 51,
carrega uma. Encher a lista para bater um número de slides. Headline com ressalva: a ressalva mora
no body.

---

## Teto rígido: 10 slides

**Carrossel de Instagram nesta conta para em 10 imagens. Isso é restrição da plataforma, não
preferência editorial: o 11º slide não sobe.** Capa e CTA são dois dos dez, então o argumento tem
**oito slides** para trabalhar.

Isso passa por cima do "o tamanho segue a contagem de unidades" do corpus. Quando a contagem passa
de oito, truncar a lista é o conserto errado: cortar o item 9 deixa uma promessa que a capa já fez.
Faça uma destas coisas no lugar:

1. **Junte irmãos.** Três exemplos que provam o mesmo ponto são um slide com três linhas, não três
   slides. Procure slides vizinhos cujas headlines poderiam ser uma frase só.
2. **Corte a preparação.** Slides de contexto, de definição e de "por que agora" são a gordura de
   sempre. Se a headline de um slide é uma premissa em vez de um achado, ele é candidato.
3. **Estreite a promessa da capa.** "Os 5 que importam" é um carrossel melhor que uma lista de 9
   truncada. Mude a contagem na capa. Não derrube o rabo da lista em silêncio.
4. **Mude de formato.** Uma lista que precisa mesmo de 14 unidades é uma thread ou um Reel, não um
   carrossel. Diga isso em vez de mutilar a lista.

Nunca corte: a capa, a virada, o CTA, nem o slide que carrega a prova mais forte da peça.

---

## Checklist antes de publicar

**Copy**
- [ ] A capa nomeia uma unidade contável e o ganho dela, não um tema
- [ ] Um número na capa, se existir um de verdade
- [ ] Uma ideia por slide
- [ ] Toda headline é a conclusão, frase completa que se sustenta sozinha
- [ ] **As headlines lidas sozinhas, do começo ao fim, formam um artigo coerente**
- [ ] Toda afirmação se resolve num número, artefato, coisa com nome ou cena exata
- [ ] Afirmação não verificada está marcada como não verificada
- [ ] O penúltimo slide faz a virada da peça
- [ ] Último slide: uma palavra para comentar, ou uma pergunta com resposta óbvia
- [ ] Sem inflação nem jargão sem tradução; soa como o usuário falando

**Design**
- [ ] Todos os slots de identidade preenchidos e declarados uma vez
- [ ] Um template travado: mesmos slots, mesma hierarquia, em todo slide
- [ ] Headline no terço de cima, e o terço de baixo é arte ou ar
- [ ] `GROUND` + `INK` + no máximo um `ACCENT`, e o accent significa uma coisa só
- [ ] No máximo duas famílias tipográficas
- [ ] Uma linguagem de ilustração, ou nenhuma, com consistência
- [ ] 4:5 1080×1350, margens de 88px
- [ ] Todo slide tem exatamente uma âncora com peso óptico dominante
- [ ] Modo de densidade escolhido de propósito: leitura ou reconhecimento
- [ ] Teste do thumbnail a 20%: ainda dá para ler, e ainda dá para identificar a conta com o handle cortado
