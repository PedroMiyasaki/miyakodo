Você ainda define as regras dos seus agentes no system prompt?

Não tem nada implicitamente errado nisso, mas vale entender o que você está comprando: o system prompt é um jeito estatisticamente provável de impor uma regra a um agente, e não um jeito certeiro. Ele tira o modelo de não ter formato de saída para ter com 99% de acerto, o que é muito. O problema é, 99% basta enquanto você é o usuário, esse 1% restante é imperceptível, você lê a resposta, percebe o erro, e envia novamente. É um "agentic loop" direto entre você o LLM, e na maioria das aplicações agênticas, não temos o luxo de ter o usuário dando feedback em todas as saídas erradas.

E essa ainda é a conta otimista, não estamos falando de uma chamada só, é uma cadeia. Seis passos a 99% cada dão 94% de ponta a ponta, o que significa quase certamente 1 erro a cada 17 execuções. E em aplicações agênticas erros são partircurlamente omissos, podem não dar erro na hora e sim três passos depois, às três da manhã, como uma data de agendamento inválida ou um id inexistente.

Repetir a chamada também não resolve, tentar novamente sem dizer o que quebrou é sortear na mesma distribuição outra vez. O que conserta não é a tentativa, e sim um bom feedback loop.

Essa é uma das coisas que eu mais notei estudando para a certificação de Claude Architect, e que venho percebendo como tendência na indústria inteira, a necessidade crescente de tornar o comportamento dos agentes controlável, principalmente em sistemas grandes com muitas execuções.

E é exatamente para isso que os hooks existem.

Na prática, os hooks são rotinas de código entre a saída do modelo e quem a consome. É um wrapper propositalmente abstrato, que te dá espaço para vários tipos de validação, e a boa prática não é validar tipo de dado nem formatação, e sim aspectos semânticos, lógicos e taxonômicos, o que normalmente exige uma função específica no seu backend ou até um LLM as a judge.

E o mais interessante do mecanismo é que você não está fazendo uma segunda chamada, que precisaria receber todo o contexto da primeira de novo. Você está literalmente refazendo a primeira, informando o modelo do problema, sem reinjetar contexto nem dependência. Ele já sabe tudo o que fez, agora sabe também onde errou, e refaz a inferência com as duas coisas na mão.

E é aí que a conta vira, porque você multiplica a chance inicial de 1% de erro por outra de no mínimo 1%, e o patamar cai para um valor estatisticamente seguro para aplicação enterprise.

O preço é que você vai precisar imaginar vários cenários de erro, e dependendo da maturidade da aplicação você talvez ainda não tenha acervo real para isso, então sobra brainstorming para levantar esses cenários na mão. No fim, o hook é tão bom quanto o erro real que ele pega.

Tem outro custo, e esse é literal: hook precisa de limitação. O modelo pode entrar num loop vicioso de execuções, e sem teto aquilo roda indefinidamente, o que não é nada bom para a sua conta no Bedrock.

Dá uma olhada no system prompt do seu agente e conta as regras. Depois observa quantas são sobre saída, validação e coisas que poderiam ser objetivamente verificadas. Cada uma dessas é espaço para um hook.

---

Caracteres: 3176
ACP Phase: C · Community
Image: posts/linkedin/hooks-are-the-only-reliable-guardrail-against-ai-errors/image.png - https://www.anthropic.com/engineering/building-effective-agents
