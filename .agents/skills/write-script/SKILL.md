---
name: write-script
description: >
  Lê uma ideia do banco de Ideias e produz um roteiro de Reel completo,
  formatado para o teleprompter, na voz do usuário.
  Ative com comandos como "escreve o roteiro da última ideia".
---
## 1. Produção · Roteiro de Reel

**Propósito:** transformar uma ideia do banco de Ideias num roteiro de Reel que um curioso pararia para ver e assistiria até o fim, na voz do usuário, no formato híbrido do teleprompter.

**A ideia chega escrita como análise. O roteiro sai como história (story-telling).** A linha do Notion costuma trazer uma tese de analista e uma pilha de fatos. O trabalho não é resumir, é transformar a ideia numa boa história, com tom autoritativo e dando valor a quem assiste.

## Quando agir

Rode quando o usuário pedir, com qualquer frase, para transformar uma ideia crua em roteiro de Reel. Exemplos de gatilho:

- "escreve o roteiro da última ideia"
- "roteiro da ideia X"
- "escreve o roteiro"

## Entrada: a ideia

Banco **Ideas** · `e2970ca3-7724-4a81-8f12-7ea34c048c67` (ID do data source, via Notion MCP). Se o usuário não disse qual ideia: filtre por `Status = "Pending"`, ordene por `Date` decrescente (ou `createdTime` se `Date` estiver vazio), pegue a mais recente, mostre o título e confirme antes de seguir. Se ele indicou um título, ache essa ideia e use direto. Leia tudo da linha: título, notas, anexos, data.

## Quem assiste

O Reel existe para alcançar quem ainda não segue o usuário. O espectador padrão é o **entusiasta curioso de IA**: brasileiro, usa o ChatGPT, acha o assunto interessante e **não é da área**. Não existe documento de audiência nem de pilar: se a peça pedir outro leitor, ou um ângulo que você não consegue achar, pergunte ao usuário. Se o usuário nomear outro público, siga o dele.

O teste de ouro: ele entende tudo ouvindo uma vez, sai com uma ideia que não tinha, e um engenheiro assistindo ao mesmo vídeo não encontra nada errado. Simples não é raso: a ideia pode ser complexa, o que precisa ser simples são as palavras.

## O formato: literal & tópicos

O coração da skill. Parte do roteiro a retenção fica literal, e o que decide a naturalidade vira tópico:

- **Literal:** o texto é falado exatamente como está escrito. São o gancho, as viradas, a recompensa e o CTA.
- **Tópicos:** pistas curtas do que explicar, na ordem, para o usuário falar do jeito dele. São a promessa e o miolo de cada degrau.

Todo bloco declara o modo no cabeçalho (`[HOOK] · literal`, `[DEGRAU] · tópicos`), e cada bloco tem um modo só. Se o usuário pedir outro modo para um bloco, siga o pedido dele.

A espinha, nesta ordem: `[HOOK]` literal (até ~30 palavras) → `[PROMESSA]` tópicos (1 a 3) → `[VIRADA]` literal + `[DEGRAU]` tópicos, de um a quatro degraus → `[RECOMPENSA]` literal → `[CTA]` literal (um pedido só, e o roteiro acaba). Todo degrau vem logo depois de uma virada com referente concreto ("só que a margem vai cair" abre um degrau, "foi aí que tudo mudou" não abre nada), e as viradas variam de forma. A recompensa responde a pergunta do vídeo retomando o gancho. O arquivo começa direto no `[HOOK]`, sem cabeçalho, e termina num rodapé depois de uma linha `---` com a linha `Gravação: um take por bloco. Literal lido, tópicos falados olhando pra lente.` e, quando houver, as fontes dos inserts.

## Antes de escrever: traduzir a ideia

Esse planejamento fica nas suas notas de trabalho, não vai ao arquivo. Responda em uma ou duas linhas cada:

1. **O fato, contado para um amigo.** Como você contaria isso numa mesa de bar para alguém que não é da área? Sem sigla, sem valor de rodada, sem nome que ele não conhece.
2. **O que está em jogo para ele.** Onde o assunto encosta na vida do espectador: o dinheiro, o trabalho, as ferramentas que ele usa, medo ou segurança, ser enganado, curiosidade sobre como o mundo funciona.
3. **A pergunta do vídeo.** Uma pergunta, do jeito que o espectador faria, que o gancho cria e que só a recompensa responde. O título da ideia é o assunto; o gancho nasce da pergunta.

A **sacada é opcional**: o padrão por trás do fato, que o espectador não concluiria sozinho e que um engenheiro reconheceria como verdade. Se as notas trazem um ângulo escrito pelo usuário, esse ângulo manda e vira a sacada. Senão, só entra se ela for concreta e específica; sacada genérica é pior que nenhuma, e vídeo que explica bem uma notícia é legítimo. Quando existe, ela vira o último degrau e a recompensa responde no nível dela.

Se a pergunta 2 ficar sem resposta, diga isso ao usuário antes de escrever, junto com o ângulo mais próximo que passaria (ou a sugestão de outro formato), e espere a decisão dele.

## Como escrever

Roteiro de Reel é fala transcrita: escreva como o usuário fala — direto, sem inflação. Nos blocos literais as regras abaixo moldam a própria fala; nos tópicos, elas decidem o que vai na pista.

- **Tudo traduzido na primeira menção.** Todo termo ganha uma analogia do dia a dia ou uma explicação de uma frase ("chip, a peça que faz IA rodar"); todo número ganha o "ou seja" ("30%, 40% = não acertavam a maioria"). Números e nomes saem escritos exatamente como devem ser ditos. Termo de que a história não precisa sai do roteiro.
- **Tópico é pista, não frase.** Uma ideia por linha começando com `-`, telegráfica, até ~15 palavras, com a analogia, o exemplo ou o número escolhido dentro dela. Tópico que virou frase completa é roteiro literal disfarçado: corte até sobrar a pista.
- **Todo degrau carrega pelo menos um fato conferível:** um número traduzido, um nome, uma data, uma cena real. Explicação sem fato vira aula genérica. Um exemplo que dá para imaginar ganha de três dados.
- **Tudo ensina, prova ou abre a próxima pergunta.** Toda frase literal e todo tópico faz uma das três; o resto sai. Não existe teto de tamanho: se ficou longo, entregue longo com a duração estimada.
- **Gancho sem cumprimento.** A primeira frase já está dentro do assunto e sozinha segura o dedo. Escreva alguns candidatos, escolha o de aposta mais forte e guarde os dois melhores seguintes para mostrar como alternativas.
- **Marque o que é para mostrar na tela.** Quando o roteiro cita algo com artefato real (post, gráfico, página de preço, manchete), marque `[insert: o que mostrar]` logo depois da frase ou tópico, de zero a quatro por roteiro, e liste as fontes no rodapé.

## Leitura fria

Antes de apresentar, releia o roteiro como quem nunca viu a ideia — de preferência num contexto limpo (subagente, quando houver), passando só o texto do roteiro, sem as notas. Uma passada, na ordem, imaginando o vídeo: a primeira frase segura o dedo? Alguma palavra trava? Em que ponto você sairia? O final responde o que o começo prometeu? Algum tópico está vago demais para imaginar o que dizer? Alguma frase literal soa como texto escrito? Conserte traduzindo antes de cortar: o que confundiu muda a tradução, não some do roteiro.

## Apresentar, iterar e fechar

Derive o slug do título (minúsculas, sem acento, hífens) e salve o roteiro na hora como `posts/script/<slug>/sketch/v1.md`. Apresente nesta ordem: uma linha de contexto (`Pergunta do vídeo: <a pergunta> · ~M:SS estimados`), o roteiro completo, os dois ganchos alternativos e, quando houver, os pontos para conferir antes de gravar (fatos que não vieram da ideia). Feche perguntando "Pronto para finalizar, ou mais alguma correção?" e deixe o caminho do arquivo como última linha da mensagem.

Cada correção cria `posts/script/<slug>/sketch/v(N+1).md`: leia a versão anterior, copie os blocos que não mudaram verbatim e aplique só o diff. Repita até o usuário confirmar "pronto" explicitamente. Só então copie o `v<N>.md` de maior número para `posts/script/<slug>/final.md`, verbatim, antes de qualquer outra coisa — e depois atualize a ideia no banco Ideas: `Status` → `"Processed"` e `Format` → `"Reel"`. Essa é a única escrita no Notion; o conteúdo nunca sobe. Confirme com: "Roteiro pronto, salvo em `posts/script/<slug>/final.md`. Próximo passo: gravar o Reel com o teleprompter."

## Calibração

Roteiro da Harvey (`posts/script/vender-o-trabalho-juridico-agora-paga-um-modelo-proprio/sketch/v3.md`), no formato híbrido. Copie os movimentos, com palavras novas — o assunto e o formato do próximo roteiro saem do planejamento, não daqui.

```
[HOOK] · literal
Todo mundo achou que o robô ia pegar a fábrica.
Pegou o escritório de advocacia.

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

[RECOMPENSA] · literal
Caro, em texto, e conferível.
Quem bate nos três está na fila.

[CTA] · literal
Roda esses três no seu trabalho.
Se bateu nos três, me conta nos comentários qual é a profissão.
Eu quero ver quantas aparecem aqui.

---
Gravação: um take por bloco. Literal lido, tópicos falados olhando pra lente.
```

## Fora do escopo

Esta skill não faz: captura de ideias cruas (isso é a `registrar-ideia`); adaptação para LinkedIn ou Instagram, a menos que o usuário peça outro formato; publicação; análise de desempenho.
