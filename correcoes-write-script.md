# Correções da skill write-script

O que mudou na skill de roteiro de Reel, comparando a versão anterior (`2bca86d`) com a reescrita (`e8d77ee`) e o ajuste feito depois (`ad82bc8`), na branch `pt-br`. As mesmas mudanças foram replicadas na `main` (`0ee50f5` e `d0e03af`).

O documento tem três partes:
1. as correções no processo da skill;
2. as correções reais que o usuário fez em primeiras versões e que viraram calibração;
3. os ajustes feitos depois da replicação.

---

## 1. Correções no processo da skill

### 1.1 O objetivo do roteiro

- **Antes:** resumir a ideia num roteiro "denso, direto, sem enchimento, orientado a resultado". O papel era de ghostwriter sênior de roteiro.
- **Agora:** fazer um roteiro que um curioso pararia para ver e assistiria até o fim. O papel é de roteirista sênior de vídeo curto. A regra-mãe: **a ideia chega escrita como análise e o roteiro sai como história.**
- **Por quê:** a linha do Notion traz uma tese de analista e uma pilha de fatos. Resumir essa pilha dá um vídeo que ninguém assiste. O roteiro bom não é o que diz mais coisas por minuto. É o que o espectador entende de primeira e não consegue parar de assistir.

### 1.2 O formato do texto

- **Antes:** roteiro 100% literal, lido palavra por palavra no teleprompter.
- **Agora:** formato híbrido. **Literal** (falado exatamente como está escrito) no gancho, nas viradas, na recompensa e no CTA. **Tópicos** (pistas para o usuário falar do jeito dele) na promessa e no miolo de cada degrau. Todo bloco declara o modo no cabeçalho (`[HOOK] · literal`, `[DEGRAU] · tópicos`) e tem um modo só.
- **Por quê:** explicando com as próprias palavras, o usuário soa como gente e acrescenta o "ou seja", o exemplo e o porquê. Mas o improviso estraga o que precisa ser exato: o gancho, a virada e o número.

### 1.3 Para quem o roteiro é escrito

- **Antes:** não havia espectador definido. Quando a peça precisava de um leitor-alvo, a instrução era perguntar ao usuário.
- **Agora:** o espectador padrão, definido pelo usuário em 2026-09-12, é o **entusiasta curioso de IA** (brasileiro, usa o ChatGPT, vê manchete de IA no feed, **não é da área**). A skill lista o que ele reconhece (ChatGPT, Nvidia, chip…) e o que ele não sabe (harness, token, benchmark, valuation…).
- **Teste de ouro:** ele entende tudo ouvindo uma vez, sai com uma ideia que não tinha, e um engenheiro não acha nada errado. Simples não é raso: a ideia pode ser complexa, as palavras é que precisam ser simples.

### 1.4 Planejar antes de escrever

- **Antes:** na leitura da ideia, a skill extraía ângulo, hook, argumento, exemplo e CTA, e já partia para a escrita.
- **Agora:** existe um passo de planejamento (Passo 4), que fica nas notas de trabalho e não vai para o arquivo. Ele traduz a ideia para quem assiste em sete itens:
  1. o fato contado para um amigo, sem sigla e sem valor de rodada;
  2. o que está em jogo para o espectador: dinheiro, trabalho, ferramentas, medo, ser enganado ou curiosidade;
  3. a pergunta do vídeo, que o gancho cria e só a recompensa responde;
  4. o dicionário de termos, cada um com a sua tradução;
  5. o material mais forte, já em escala humana;
  6. o que fica de fora;
  7. a sacada, quando existe uma boa.
- **Regra:** o título da ideia é o assunto, e o gancho nasce da pergunta do vídeo, não do título.

### 1.5 Jargão

- **Antes:** uma regra genérica, "sem jargão sem explicação".
- **Agora:**
  - **Tradução obrigatória:** todo termo sem o qual a história não fecha entra traduzido na primeira menção, com uma analogia do dia a dia ou uma explicação de uma frase ("o modelo é o cérebro, o harness é a mão").
  - **Corte:** termo de que a história não precisa sai do roteiro.
  - **Aposto:** empresa ou produto desconhecido ganha um aposto curto ("a Harvey, uma IA feita para advogados").
  - **Nome conhecido primeiro:** "ChatGPT" antes de "GPT-6 Astra".
  - **Sem bordão:** a mesma analogia pode voltar em outro Reel, mas com palavras novas.

### 1.6 Fatos e números

- **Antes:** "número concreto" era um formato de gancho, e o argumento "pode incluir 1 número, estatística ou comparação".
- **Agora:**
  - **Filtro de fatos:** só entra o fato que ajuda a responder a pergunta. Nome de fundo, valor de rodada, versão e detalhe de arquitetura ficam de fora, a menos que a história precise deles.
  - **Escala humana:** "menos da metade do preço" no lugar de "57% mais barato".
  - **"Ou seja":** todo número vem explicado ("30%, 40%. Ou seja, não acertavam a maioria").
  - **Número no gancho:** só quando é sentido sem fazer conta ("o maior faturamento da história"). Rodada e porcentagem de benchmark ficam no miolo, já traduzidas.
  - **Fato por degrau:** todo degrau carrega pelo menos um fato conferível (número traduzido, nome, data ou cena real). É o fato que faz o engenheiro confiar e o curioso contar para alguém.

### 1.7 A sacada deixou de ser obrigatória

- **Antes:** todo roteiro tinha um bloco `[TURN OR INSIGHT]` com um "momento aha" (um framework, uma regra de bolso ou uma reformulação).
- **Agora:** a sacada é **opcional**. Um vídeo que explica bem uma notícia é legítimo, e sacada genérica é pior que nenhuma.
  - **Ângulo do usuário:** se as notas ou a conversa trazem um ângulo escrito por ele, esse ângulo é a sacada, e ela entra sem marca.
  - **Só resumo da notícia:** se as notas só resumem o fato (o formato da `content-research`), a skill procura uma sacada com três perguntas: o mecanismo, o que só existia por causa do contrário, e onde mais isso bate.
  - **Teste de sacada boa:** tem mecanismo concreto, diz algo que o espectador não tiraria sozinho, traz um segundo exemplo ou uma consequência com nome, e não serve igual para qualquer outra notícia. Falhou num item, fica de fora.
  - **Marca de proposta:** a sacada proposta pela skill entra marcada com `· sacada proposta`. Quando existe, ela é sempre o último degrau.

### 1.8 Portão 🔥

- **Antes:** a skill não checava se a ideia servia para Reel.
- **Agora:** se ninguém consegue dizer o que está em jogo para o espectador (item 2 do planejamento), a ideia não passa no teste 🔥. A skill avisa o usuário antes de escrever, sugere o ângulo mais próximo que passaria ou outro formato (post de LinkedIn, por exemplo), e espera a decisão.

### 1.9 A estrutura

- **Antes:** uma estrutura fixa, cronometrada: HOOK (0–5s), PROBLEM (5–20s), CORE ARGUMENT (20–55s), TURN OR INSIGHT (55–75s), CTA (75–90s).
- **Agora:** duas camadas.
  - **Quatro formatos de história,** escolhidos pela pergunta do vídeo: o mistério, a crença invertida, o desmonte e a aula em camadas. Cada um diz o que vai em cada degrau.
  - **Uma espinha comum,** em que cada bloco tem um trabalho na curva de retenção, e não um tempo:

| Bloco | Modo | Trabalho |
|---|---|---|
| `[HOOK]` | literal | parar o dedo, em até ~30 palavras |
| `[PROMESSA]` | tópicos | confirmar que a pergunta vale a pena |
| `[VIRADA]` | literal | abrir o degrau seguinte |
| `[DEGRAU]` | tópicos | ensinar ou provar uma coisa (um a quatro degraus) |
| `[RECOMPENSA]` | literal | responder a pergunta, retomando o gancho |
| `[CTA]` | literal | um pedido só |

### 1.10 O encadeamento (história, não lista)

- **Antes:** não havia regra de ligação entre as partes.
- **Agora:**
  - **Virada antes de degrau:** todo `[DEGRAU]` vem logo depois de uma `[VIRADA]` ("mas", "então" ou uma pergunta), sempre com referente concreto.
  - **Sem frase de guru:** "E foi aí que tudo mudou" não abre nada.
  - **"E também" é lista:** se a ligação natural entre dois degraus é "e também", o segundo é item de lista, e os dois viram um degrau só. A regra é dos criadores de South Park, e é ela que separa história de lista de fatos.
  - **Formas variadas:** as viradas mudam de forma. Três "só que" seguidos viram tique.
  - **Tópico que repete o anterior sai.**

### 1.11 O gancho

- **Antes:** três formatos genéricos (afirmação contraintuitiva, número concreto, pergunta), com exemplos inventados ("A maioria das empresas que adotam IA está fazendo errado").
- **Agora:**
  - **Volume:** a skill escreve pelo menos **8 ganchos de pelo menos 5 tipos**, a partir de uma tabela de 10 tipos, cada um com um exemplo que o usuário escreveu ou aprovou.
  - **Regras de forma:** a primeira frase já está dentro do assunto e segura o dedo sozinha, e o gancho inteiro cabe em ~30 palavras.
  - **Teste de seis perguntas:** reconhecimento, aposta, pergunta aberta, primeira escuta, boca do usuário e promessa cumprida. Falhou numa, o gancho sai.
  - **Escolha:** vence o gancho de aposta mais forte. Os dois seguintes, de tipos diferentes, vão para a apresentação como alternativos.
  - **Promessa cumprida:** gancho que o vídeo não paga é clickbait, e o README proíbe.

### 1.12 O tamanho

- **Antes:** Reel de 60 a 90 segundos, 150 a 220 palavras, a ~130 palavras por minuto. A contagem de palavras era critério de qualidade.
- **Agora:** **não existe teto.**
  - **O que controla o tamanho:** toda frase e todo tópico ensina, prova ou abre a próxima pergunta, e o que não faz nenhuma das três sai.
  - **Referência, não meta:** a maioria dos Reels fica entre 1:15 e 2:00, e uma aula em camadas pode chegar a 3 minutos.
  - **Estimativa:** palavras literais divididas por 200 por minuto (a velocidade do usuário depois do corte), mais ~8 segundos por tópico.
  - **Frase ditada pelo usuário não é cortada para caber.** Se o roteiro ficou longo, ele sai longo, com a duração estimada.

### 1.13 O final do roteiro

- **Antes:** o "momento aha", algo "que o espectador vai querer repetir para outra pessoa".
- **Agora:** a `[RECOMPENSA]` responde a pergunta do vídeo, retoma o gancho com a mesma palavra ou o mesmo número, e usa uma de **quatro formas**: um teste de bolso, a revelação que fecha o gancho, uma posição honesta ou a consequência.
- **Teste de referente:** tente dizer a mesma coisa com outras palavras. Se não der, é frase de efeito.

### 1.14 O CTA

- **Antes:** exemplos genéricos ("me manda uma DM", "salva esse aqui").
- **Agora:** um pedido só, em até três linhas, e o roteiro acaba nele. O pedido é escolhido pelo tipo de recompensa:
  - **teste ou regra prática:** mandar o vídeo para alguém específico (compartilhamento por DM é um dos sinais que mais levam o Reel a quem não segue);
  - **posição ou polêmica:** a opinião dele nos comentários;
  - **notícia explicada:** seguir a conta, com o motivo;
  - **tema que já tem artigo no Substack:** palavra-chave nos comentários.

### 1.15 O registro da fala

- **Antes:** "escreva exatamente como vai ser falado: sem conectivo formal".
- **Agora:** o usuário explicando para um amigo curioso, e não um analista resumindo para um colega.
  - **Porquê:** toda afirmação que sustenta a história ganha o porquê, numa frase.
  - **Exemplo:** um exemplo que dá para imaginar (uma cena, um experimento mental) ganha de três dados.
  - **Opinião:** vem em primeira pessoa, com o limite dito.
  - **Marcas de fala:** nos blocos literais entram "Sabe aqueles…?", "Então…", "tá", "pra".
  - **Muletas:** as que o usuário já pediu para cortar ("basicamente", "meio que") ficam fora.
- **Como escrever um tópico (regra nova):** uma ideia por linha, até ~15 palavras, telegráfico (`→`, `=`, `:`). A analogia e o número já escolhidos vão escritos na pista. Tópico que virou frase completa é roteiro literal disfarçado.

### 1.16 Formatação para o teleprompter

- **Quebra de linha:**
  - **Antes:** parágrafos de até 2 linhas.
  - **Agora:** uma frase ou um fôlego por linha nos blocos literais (a quebra marca respiração) e um tópico por linha.
- **`[pause]`:**
  - **Antes:** onde o usuário devesse respirar ou assentar a ênfase.
  - **Agora:** só depois do gancho e antes de uma revelação.
- **Negrito:**
  - **Antes:** livre, em toda palavra de ênfase.
  - **Agora:** no máximo **três** no roteiro inteiro, só em bloco literal, na palavra cuja ênfase muda o sentido.
  - **Por quê:** negrito em toda frase de efeito empurra a leitura para o "modo YouTuber" que `content-routines/aprendizados.md` (2026-08-29) pede para evitar.
- **Provas na tela (regra nova):** `[insert: o que mostrar]` numa linha própria, de zero a quatro por roteiro, só com artefato real.
- **Rodapé (regra nova):** o arquivo começa direto no `[HOOK]` e termina num rodapé com a linha de gravação ("um take por bloco. Literal lido, tópicos falados olhando pra lente.") e as fontes dos inserts.

### 1.17 Leitura fria antes de apresentar

- **Antes:** a própria skill conferia os critérios e reescrevia se algo falhasse.
- **Agora:** existe um passo de leitura fria (Passo 6). Um subagente recebe **só o texto do roteiro**, sem a ideia e sem as notas, faz o papel do espectador e responde oito perguntas: se continuaria assistindo, que palavras não entendeu, onde arrastaria o dedo, se o final respondeu, e assim por diante. Sem subagente, a skill responde ela mesma, fingindo nunca ter visto a ideia.
- **Por quê:** quem acabou de ler as notas do Notion não enxerga o próprio jargão.
- **Regras do conserto:**
  - **Traduzir antes de cortar:** o material mais forte fica, e o que muda é a tradução dele.
  - **Tabela de consertos:** cada problema apontado tem um conserto definido.
  - **No máximo duas rodadas:** um leitor novo sempre acha algo novo, e rodada demais tira do roteiro justamente o que ele tem de concreto.

### 1.18 A apresentação

- **Antes:** o roteiro, a pergunta "Pronto para finalizar?" e o caminho do arquivo.
- **Agora**, nesta ordem:
  1. uma linha de contexto (formato da história · pergunta do vídeo · duração estimada);
  2. o roteiro;
  3. os dois ganchos alternativos, numerados;
  4. os **pontos para conferir antes de gravar**, perguntados na AskUserQuestion (manter, cortar ou alternativa, com recomendação): todo fato que não veio da ideia e o que a leitura fria apontou e foi mantido;
  5. a pergunta;
  6. o caminho do arquivo, sempre na última linha.

### 1.19 A iteração e o fechamento

- **Gancho alternativo:** "usa o 2" troca o `[HOOK]`, e a `[PROMESSA]` só muda se deixou de conversar com o gancho novo.
- **Sacada proposta, quatro casos:**
  - o usuário pediu para tirar: saem os blocos marcados, e a recompensa volta para o nível da notícia;
  - o usuário deu outro ângulo: a sacada é reescrita em cima dele, sem marca;
  - o usuário pediu outra tentativa: a skill propõe outra sacada, marcada;
  - o usuário corrigiu outra parte e não mexeu na sacada: ela foi aceita, e a marca sai.
- **No "pronto":** se ainda houver marca `· sacada proposta`, a skill cria antes uma versão sem as marcas e só depois copia para o `final.md`.

### 1.20 O modelo de saída

- **Antes:** um roteiro inventado, em registro corporativo ("Um cliente meu tinha uma operação de revisão de documentos… 94% de acerto").
- **Agora:** uma seção de **Calibração** com um roteiro aprovado do usuário (Harvey), anotado bloco a bloco, e os pares antes/depois da parte 2 deste documento.
- **Uso:** copiar os movimentos das frases, com palavras novas.

### 1.21 Os critérios de qualidade

- **Antes:** seis critérios, incluindo "hook em menos de 5 segundos" e "entre 150 e 220 palavras".
- **Agora:** um checklist de 16 itens que espelha as regras acima, entre eles:
  - modo declarado em todo bloco;
  - pergunta do vídeo respondida na recompensa;
  - gancho aprovado nas seis perguntas;
  - toda virada antes de degrau;
  - nenhum termo sem tradução;
  - fato conferível em todo degrau;
  - sacada testada e marcada;
  - leitura fria feita;
  - fatos externos levados ao usuário;
  - negrito em no máximo três lugares;
  - rodapé presente.

---

## 2. Correções reais do usuário em primeiras versões

Cada par abaixo está na seção Calibração da skill: a primeira versão entregue e o que o usuário gravou ou aprovou no lugar.

### Gancho

1. **Nomes conhecidos, não abstração.**
   - v1: "O mesmo teste deu dois vencedores em três dias. E nenhum dos dois modelos mudou."
   - Usuário: "Três dias atrás o GPT-6 era a melhor IA do mundo. Hoje ele empata com o Claude. E nada no GPT-6 mudou."
   - Padrão: o título da ideia virou uma reviravolta com nomes que o espectador conhece.
2. **Algo em jogo para o espectador, não notícia de mercado.**
   - v1: "A Sequoia acabou de colocar cinco milhões e meio de dólares numa startup jurídica brasileira. E a tese por trás do cheque contraria vinte anos de Vale do Silício."
   - Usuário: "Se você quer construir uma empresa de bilhões com IA, para de vender software. E quem está dizendo isso não sou eu."
   - Padrão: a notícia virou um conselho com aposta e pergunta aberta (quem está dizendo?).
3. **O que está em jogo vem antes da opinião.**
   - v1: "Um pesquisador saiu da Anthropic dizendo que a IA pode matar todo mundo até o fim da década. E eu não comprei."
   - Usuário: "A inteligência artificial pode acabar com a humanidade até o fim dessa década. [pause] Bom. Pelo menos é isso que diz um pesquisador que saiu da Anthropic essa semana."
   - Padrão: a afirmação com todo o peso primeiro, e a fonte que desinfla depois.

### Explicação

4. **Analogia que ensina, não afirmação de especialista.**
   - v1: "Primeiro: uma linha não é um modelo. É um modelo mais o harness que pilota ele."
   - Usuário: "O modelo é o cérebro. Entra texto, sai texto. […] Ele não tem mãos. […] O harness é a mão."
   - Padrão: o conceito virou uma analogia que ensina o objeto.
5. **Currículo é contexto de que a história não precisa.**
   - v1: "Jacob Coxon, matemático de Cambridge, trabalhou no GPT-4o na OpenAI e em pretraining na Anthropic."
   - Usuário: cortou. "Um pesquisador que saiu da Anthropic" basta.
   - Padrão: corte o que não ajuda a responder a pergunta.
6. **O mecanismo vem antes da frase esperta.**
   - v1: "Chip que vende sozinho não precisa de banco montando o crediário do cliente."
   - Usuário: primeiro explicou o mecanismo (o dinheiro financia os data centers que compram o chip, e a GPU vira garantia de empréstimo, que nem imóvel). Só depois veio a frase, agora como pergunta: "Se o chip é tão bom assim, por que ela precisa montar o crediário do cliente pra vender?"
   - Padrão: explicação primeiro, e a frase de efeito vira pergunta.

### Recompensa

7. **Teste aplicável, não aforismo de estrategista.**
   - v1: "Quem entrega o trabalho consegue descer e fazer o modelo. Quem faz o modelo não consegue subir e chegar no cliente."
   - Usuário: "Caro, em texto, e conferível. Quem bate nos três está na fila."
   - Padrão: a conclusão virou um teste que o espectador aplica no próprio trabalho.
8. **Posição honesta, não frase de efeito.**
   - v1: "Eu não acho que ele mentiu. Acho que ele foi útil."
   - Usuário: "Eu não estou dizendo que ele está de má-fé, nem que isso é premeditado. Mas eu não gosto de sentir medo por causa de declaração solta, sem apontamento direto."
   - Padrão: opinião em primeira pessoa, com o limite dito.

### Sacada

9. **A sacada sai do caso e mostra o mecanismo.**
   - v1: "Com a IA fazendo essa parte, o atalho perdeu o motivo, e voltou a valer a pena fazer um app sob medida pra cada celular."
   - Usuário (na revisão): o vídeo devia mostrar que a IA muda o que vale a pena fazer. Ganho pequeno que antes não compensava passa a compensar, e atalho e framework que só existiam porque escrever código era caro perdem o motivo.
   - Padrão: a conclusão da v1 ficou presa ao caso da Shopify. A do usuário diz o mecanismo (escrever código ficou barato) e onde mais ele bate.

### CTA

10. **Algo que qualquer um faz, não tarefa de profissional.**
    - v1: "Antes de trocar de modelo por causa de ranking, abre o índice e olha só o sub-teste mais parecido com o que você faz no dia a dia."
    - Usuário: "Pega a tarefa que você mais faz e roda nas duas. Em dez minutos você tem o único ranking que importa: o seu."
    - Padrão: o pedido virou algo que o espectador consegue fazer em dez minutos.

---

## 3. Ajustes feitos depois da replicação

1. **Número de formas da recompensa.** A seção da recompensa lista quatro formas, mas a tabela de consertos da leitura fria dizia "reescreva a recompensa numa das **três** formas". Agora diz "quatro" (`ad82bc8` na `pt-br`, `d0e03af` na `main`).
2. **`traduzir` com os blocos antigos (só na `main`).** A skill `traduzir` mandava preservar os marcadores `[HOOK]` e `[PROBLEM]`, da estrutura antiga. Agora cita os cabeçalhos novos com o modo, `[pause]`, `[insert: …]` e o rodapé.
3. **Adaptações da versão em inglês (`main`).**
   - **Espectador:** perdeu o "brasileiro", porque na `main` o roteiro sai em inglês por padrão.
   - **Idioma:** ganhou a linha da `main` (inglês por padrão, pt-BR quando o usuário pedir).
   - **Referência da voz:** a regra da frase de guru aponta para o § 9.8 do `base.md`, que é onde ela mora lá.
