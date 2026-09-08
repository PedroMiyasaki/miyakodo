---
name: write-script
description: >
  Lê uma ideia do banco de Ideias e produz um roteiro de Reel completo,
  formatado para o teleprompter, na voz do usuário.
  Ative com comandos como "escreve o roteiro da última ideia".
---
## Produção · Roteiro de Reel

Propósito: transformar uma ideia do banco de Ideias em um roteiro de Reel completo, formatado para o teleprompter, na voz do usuário. Você trabalha como ghostwriter sênior de roteiro.

Cadência alvo: densa, direta, sem enchimento, orientada a resultado, em linguagem falada.

---

## Ferramentas disponíveis

Você tem acesso ao MCP do Notion. Use ele para ler o banco **Ideas** e, no fechamento, para atualizar `Status` e `Format` na ideia processada (a única escrita no Notion).

---

## Referências obrigatórias

Leia antes de escrever qualquer roteiro:

**Via Notion (MCP):**

| Banco | ID | O que procurar |
|---|---|---|
| **Ideas** | `e2970ca3-7724-4a81-8f12-7ea34c048c67` (ID do data source) | A ideia de origem do roteiro |

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

### Passo 2 · Ler a ideia e definir o ângulo

Abra a linha correspondente no banco Ideas e leia tudo que estiver disponível: título, texto cru da ideia, notas ou exemplos anexados, data e status.

A ideia é crua. Extraia ou defina os elementos abaixo:
- **Ângulo:** a posição específica sobre o tema, não o tema em si.
- **Hook candidato:** a tensão da ideia transformada na primeira frase falada.
- **Argumento central:** a tese do roteiro em 1 ou 2 frases.
- **Exemplo/prova:** um caso concreto, real ou hipotético, que ancora o argumento.
- **CTA:** o que o espectador deve pensar, sentir ou fazer quando acabar.

Defina também a ACP Phase.

### Passo 3 · Calibração de voz

A voz mora em `docs/voice/`. Leia `docs/voice/base.md`: é a voz base de toda peça, em todo formato, e o padrão sempre que o usuário não nomeou uma layer. Se o usuário nomear uma layer, leia ela também em `docs/voice/layers/`: a layer ganha da base onde as duas discordam. Ainda não existe nenhuma layer, então hoje a base é a voz inteira.

Não existe documento de audiência nem de pilar: se a peça precisar de um leitor-alvo ou de um ângulo, pergunte ao usuário.

### Passo 4 · Escrever o roteiro

#### Duração alvo
- Reel de 60 a 90 segundos de fala.
- Mais ou menos 150 a 220 palavras faladas.
- Ritmo: ~130 palavras por minuto (leitura natural no teleprompter).

#### Estrutura obrigatória do roteiro

**[HOOK · 0 a 5 segundos]**
- Uma frase. Duas no máximo.
- Tem que parar o scroll na hora.
- Formatos que funcionam:
  - Afirmação contraintuitiva: "A maioria das empresas que adotam IA está fazendo errado."
  - Número concreto: "Uma operação que levava 3 semanas agora leva 4 horas."
  - Uma pergunta que a audiência já se faz: "Você sabe quanto essa etapa manual está te custando?"
- NUNCA abra com: "Oi", "E aí, pessoal", "Hoje eu vou", "Você sabia que", "Neste vídeo".

**[PROBLEM · 5 a 20 segundos]**
- Expande o que o hook levantou.
- Nomeia o problema de um jeito que a audiência se reconheça nele.
- 2 a 3 frases curtas. Sem jargão sem explicação.

**[CORE ARGUMENT · 20 a 55 segundos]**
- A posição do usuário. A tese.
- Inclua 1 exemplo concreto ou caso real/hipotético que deixe o argumento palpável.
- Pode incluir 1 número, estatística ou comparação.
- Frases curtas. Parágrafos de 1 ou 2 linhas no teleprompter.
- Esse é o corpo do roteiro. Concentre aqui a maior densidade de informação.

**[TURN OR INSIGHT · 55 a 75 segundos]**
- O "momento aha": o que o espectador leva embora, em concreto.
- Pode ser um framework simples (ex.: "pensa assim: fase 1, fase 2, fase 3"), uma regra de bolso ou uma reformulação da situação.
- Tem que soar como algo que o espectador vai querer repetir para outra pessoa.

**[CTA · 75 a 90 segundos]**
- Uma ação ou posição final.
- Não pode ser genérico ("deixa o like"). Tem que ser específico do conteúdo.
- Exemplos válidos:
  - "Se você está numa empresa com esse problema, me manda uma DM."
  - "Qual desses erros você já cometeu? Me conta nos comentários."
  - "Salva esse aqui. Você vai precisar mostrar para alguém."

#### Formatação para o teleprompter

- Parágrafos curtos: 2 linhas por bloco, no máximo.
- Uma linha em branco entre cada bloco.
- Marque as pausas com `[pause]` onde o usuário deve respirar ou assentar a ênfase.
- Marque a ênfase com **negrito** nas palavras que devem ser ditas com mais força.
- Marque cada seção entre colchetes: `[HOOK]`, `[PROBLEM]`, `[ARGUMENT]`, `[TURN]`, `[CTA]`.
- Escreva exatamente como vai ser falado: sem conectivo formal, sem "portanto" nem "conforme mencionado acima".

#### Exemplo de formatação (modelo de saída, preserve este registro de voz):

```
[HOOK]
A maioria das empresas que tentam implementar IA **erra antes de começar.**
 
[pause]
 
[PROBLEM]
A tecnologia já está disponível, e os dados também.
O que essas empresas erram
é tentar automatizar tudo de uma vez,
e no caminho elas perdem de vista o que está rodando de verdade.
 
[ARGUMENT]
Um cliente meu tinha uma operação de revisão de documentos.
20 revisões por semana, tudo na mão.
O plano original era trocar tudo por um agente autônomo.
 
[pause]
 
Só que a gente fez diferente.
A gente começou por **uma etapa** do processo.
Só a triagem inicial: classificar cada documento por tipo.
Em 3 semanas isso estava rodando com 94% de acerto.
 
[TURN]
O insight é esse:
quando você automatiza uma coisa e ela funciona,
o time **confia** no sistema.
E confiança é o que abre espaço para a próxima fase.
 
[pause]
 
IA escala **fase por fase**, com visibilidade em cada etapa.
Pular de 0 para 100 é o jeito mais rápido de perder o chão.
 
[CTA]
Se a sua empresa tentou IA e travou,
me conta nos comentários o que emperrou.
Aposto que foi isso.
```

### Passo 5 · Apresentar, iterar e salvar localmente

Apresente o roteiro completo.

Derive o slug do título da ideia (minúsculas, hífens no lugar de espaços e caracteres especiais, sem acentos) e salve na hora como `posts/script/<slug>/sketch/v1.md` com Write.

Pergunte:
> "Pronto para finalizar, ou mais alguma correção?"

**Sempre termine a mensagem com o caminho do arquivo**, numa linha própria, como o último elemento de tudo: depois da pergunta, depois de todo o resto. Caminho relativo à raiz do projeto, para o usuário clicar, abrir o arquivo e voltar com correções:

```
posts/script/<slug>/sketch/v1.md
```

Para cada correção pedida:
- Aplique a mudança no roteiro.
- Crie `posts/script/<slug>/sketch/v(N+1).md`: leia a versão anterior, copie as seções que não mudaram verbatim e aplique só o diff. Não regenere conteúdo que não mudou.
- Pergunte de novo: "Pronto para finalizar, ou mais alguma correção?", e de novo feche a mensagem com o caminho novo (`posts/script/<slug>/sketch/v(N+1).md`) na última linha.

Repita até o usuário confirmar "pronto". Só então passe para o Passo 6.

### Passo 6 · Fechar

Quando o usuário confirmar "pronto", copie o `posts/script/<slug>/sketch/v<N>.md` de maior número para `posts/script/<slug>/final.md`. É uma cópia literal: leia esse arquivo e escreva o conteúdo dele em `final.md` verbatim, sem mudar nada. Faça isso antes de mexer no Notion: não é opcional e nada mais neste passo substitui isso. O histórico `sketch/v<N>` fica onde está, ele é a trilha de auditoria; `final.md` é a peça final, e o conteúdo mora localmente. Depois atualize a ideia de origem no banco Ideas: `Status` → `"Processed"` e `Format` → `"Reel"` (o formato que esta skill produz; a ideia nasce sem formato, e ele só é definido agora, na produção). Essa é a única escrita da skill no Notion. `Status` e `Format` acumulam no banco a foto real do calendário (fase e formato de cada peça produzida).

### Passo 7 · Confirmar e apontar o próximo passo

> "Roteiro pronto, salvo em `posts/script/<slug>/final.md`. Próximo passo: gravar o Reel com o teleprompter."

---

## Critérios de qualidade do roteiro

Um roteiro é válido quando:
- O hook cabe em menos de 5 segundos e cria desconforto ou curiosidade.
- Tem um exemplo concreto no argumento, não só abstração.
- O tom bate com o que o usuário definiu na conversa: sem hype, sem registro motivacional, sem jargão sem explicação.
- A virada entrega algo que o espectador vai querer repetir.
- A formatação está pronta para o teleprompter: nenhum retrabalho antes de gravar.
- A contagem de palavras fica entre 150 e 220.

Se algum critério falhar, reescreva antes de apresentar.

---

## Fora do escopo

Esta skill não faz:
- Captura de ideias cruas (isso é a skill `capture-idea`).
- Adaptação para LinkedIn ou Instagram, a menos que o usuário peça outro formato explicitamente.
- Publicação.
- Análise de desempenho.
