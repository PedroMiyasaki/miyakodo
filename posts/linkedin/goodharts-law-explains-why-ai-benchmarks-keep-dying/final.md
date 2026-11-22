A primeira coisa que eu olho num gráfico de benchmark de uma IA nova não é a com certeza enorme taxa de assertividade, é a data do benchmark que eles escolheram usar.

Vejo isso como um caso clássico da Lei de Goodhart: quando uma métrica vira meta, ela deixa de ser uma métrica eficiente, e a IA generativa talvez seja um dos piores exemplos disso que existem, porque pela própria natureza de treinamento e inferência o modelo não só mira no alvo, ele pode treinar nele.

São três mecanismos se empilhando:
1 - Contaminação: o benchmark é público, portanto, as tarefas, soluções e discussões sobre elas entram no corpus do próximo pré-treino.
2 - Harness: a nota não é só do modelo, é do modelo + scaffold em volta dele, loop do agente, número de tentativas, parser da saída, e esse scaffold fica sendo ajustado contra o benchmark durante vários meses.
3 - Seleção de checkpoint: quando o time roda a mesma avaliação a cada checkpoint e promove o que pontuou melhor, a avaliação já virou parte do treino, mesmo que aquele dado nunca tenha encostado no otimizador, é um RF indireto.

O Terminal-Bench é um dos exemplos mais limpos que a gente tem disso. As primeiras versões mediam de verdade o que um agente de terminal conseguia fazer, e com o tempo os labs foram otimizando em cima dessa primeira versão, com as notas subindo sem parar. Depois veio a versão 2, com o mesmo tipo de trabalho mas com tarefas novas, e os modelos que iam muito bem no Terminal-Bench 1 passaram a ir muito mal no 2. E aqui estamos de novo, com quase todo mundo indo extremamente bem no Terminal-Bench 2 (e 2.1) e mal na versão nova, o 3.

E essa queda toda é justamente a parte que vale lembrar: a distância entre a nota velha e a nota nova é o que expõe quanto daquela pontuação antiga era capacidade de verdade e quanto era ajuste fino em cima do teste.

Esse ciclo também não tem nada de novo, ele só vem acontecendo cada vez mais rápido. O ImageNet saturou e foi aposentado, o GLUE saturou e precisou virar SuperGLUE, e o Terminal-Bench está apenas dando mais uma volta na mesma roda, com o intervalo entre uma volta e outra encurtando cada vez mais (aliás, meio assustador)

Eu entendo perfeitamente a necessidade de existirem benchmarks, porque a alternativa é total desconhecimento de qual modelo é melhor. Mas eles servem muito mais para você descartar modelo do que para escolher entre os cinco primeiros do ranking, que geralmente estão disputando pontuações na segunda casa decimal. A realidade é que a especificidade do seu dia a dia de trabalho, testada contra os modelos que sobraram ainda vai ser a melhor medição que você vai conseguir.

#benchmarks #evals #llm

---

Caracteres: 2659
ACP Phase: A · Audience
Image: posts/linkedin/goodharts-law-explains-why-ai-benchmarks-keep-dying/image.png - https://www.frontierbench.ai/announcement
