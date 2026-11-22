# Webinar 1 (Miyakodo): assuntos definidos

Documento de trabalho com os assuntos já aprovados para o primeiro webinar ao vivo de 2 horas (com pelo menos 30 minutos reservados para perguntas no final). A ementa parte de três princípios básicos guiantes e, a partir deles, evolui para as seções mais específicas de padrão de projeto, tecnologia e governança.

## Requisitos do produto

- **Entregável concreto:** o webinar tem cara de produto e entrega algo referenciável (playbook / roadmap) que dá clareza prática para o empresário agir depois.
- **Clareza para decidir:** donos, sócios e líderes de empresas médias brasileiras pagam por clareza, não por aula de ferramenta. Os temas precisam tirar a pessoa do estado de confusão e ajudá-la a enxergar casos de uso reais no próprio negócio.
- **Conexão com o momento do mercado:** a proposta conversa com o FOMO e a sensação de psicose com IA no mercado, respondendo com calma, critério e método.

## Parte 1: Princípios básicos (guiam todo o resto da ementa)

A ementa abre apresentando estes três princípios, que formam a base conceitual para todas as seções seguintes.

### Princípio 1: A natureza probabilística da IA
- Como a IA funciona na essência: um pouco da estrutura de embeddings e do raciocínio por trás de como a ferramenta é feita.
- Por que a inteligência artificial é uma solução muito cara para casos em que ela não é necessária (contraste entre problemas probabilísticos e problemas determinísticos, nos quais software tradicional, regra fixa ou ajuste de processo resolve melhor e mais barato).

### Princípio 2: Engenharia de contexto
- Como a necessidade de técnicas como engenharia de prompting, role prompting e similares veio decrescendo em importância nos últimos anos, enquanto a engenharia de contexto veio crescendo em importância.
- Como todo o ecossistema de plugins, skills, conexões e MCPs é, na verdade, uma abstração sobre a mesma coisa: fornecer o contexto necessário para que a IA consiga trabalhar.

### Princípio 3: A IA é uma ferramenta, não um objetivo final
- A diagramação do negócio, o entendimento do core business da empresa (onde estão os gastos, onde estão os lucros) e o desenho e a clareza mental disso, como primeiro princípio, são muito mais importantes para identificar onde a IA como ferramenta faz diferença do que usar IA apenas pelo objetivo final de "usar IA".
- Inteligência artificial nenhuma salva um projeto ruim que não tem relação com o core business da empresa.

## Parte 2: Conceitualização

Cada conceito desta seção segue a mesma didática: primeiro a explicação do conceito, depois um exemplo prático ou situação real de aplicação.

**Nota transversal (governança e centralização):** centralização e camada de governança não entram como tópico isolado. Aparecem como fio condutor dentro de Human-in-the-loop, Skills, Camada de dados e ações e Superfície de entrega, mostrando que a governança empresarial de IA nasce da combinação dessas peças.

### 1. One-off LLM call vs Workflow vs Agente
- Diferencia os três níveis de complexidade, previsibilidade e controle no uso de LLMs: uma chamada pontual (one-off), um workflow estruturado e um agente autônomo.

### 2. Anatomia de agente, Harness e Memória/Estado
- Explica os componentes de um agente: system prompt, tools e **memória/estado** (absorvido aqui, sem ser um tema isolado, para mostrar o que a IA retém entre interações e ao longo de um caso).
- Conceitualiza todo esse conjunto em volta do modelo como **harness**.
- Trade-off de controle do harness: usar uma solução pronta (como Claude Code ou Codex) acelera e simplifica, mas abre mão do controle sobre o harness; construir ou controlar o próprio harness dá controle fino, porém exige mais engenharia.

### 3. Evals (verificação de resposta)
- **Profundidade:** propositalmente rasa e direta, para não consumir tempo excessivo do webinar.
- **Mensagem central:** verificação estruturada de resposta é o que dá uma direção real de evolução ao projeto de IA (sem eval, mudanças acontecem no escuro).

### 4. Saída estruturada (Structured Outputs)
- Foco em controle de saída e na ponte com o resto da empresa: como transformar a saída probabilística da IA em dado padronizado que pode ser integrado depois em sistemas automáticos e determinísticos para movimentar a operação.

### 5. Human-in-the-loop
- Um dos conceitos mais importantes na gestão de projetos de IA no contexto empresarial.
- Garante segurança operacional e atua diretamente como camada de validação e governança (onde o humano aprova, corrige ou intervém no fluxo).

### 6. Skills
- **Analogia didática:** igual a funções em programação. Se você escreve o mesmo snippet de código mais de uma vez, deveria criar uma função; se você escreve o mesmo prompt mais de uma vez, deveria criar uma skill.
- **Visão empresarial:** skills são registros de métodos para a IA executar uma tarefa específica. Empresas têm workflows, métodos e passos repetidos, e isso deve virar skill em projetos de IA.
- **Posicionamento:** skill é o formato mais estabelecido no mercado para registrar um processo para uma IA executar qualquer atividade, funcionando como ativo compartilhado e parte da governança centralizada da empresa.

### 7. Camada de dados e ações
- Explica por que dar à IA acesso organizado à camada de dados (e centralizar essa camada com governança) é decisivo para o projeto funcionar.
- Três formas de conectar dados conforme o caso:
  - **RAG:** quando há volumes ou documentos muito grandes.
  - **MCP:** conexão padronizada com fontes de dados e ferramentas corporativas.
  - **Tools:** para processos mais simples, como navegar dados em uma máquina local ou executar consultas diretas.

### 8. Superfície de entrega (onde a IA vive na empresa)
- Mapeia os lugares onde uma IA pode viver do ponto de vista empresarial, com níveis crescentes de controle, centralização e governança:
  - **Na máquina de cada funcionário:** por exemplo, instalação local de ferramentas como Codex (ou similares) por estação.
  - **Em assinaturas Enterprise:** como ChatGPT Enterprise ou Gemini Enterprise, já trazendo algum nível de centralização e governança.
  - **Em camada de aplicação customizada na nuvem da própria empresa:** usando plataformas como AWS Bedrock, Azure AI Foundry e similares.
  - *(Em aberto para expandir depois com outras superfícies possíveis.)*

### 9. Roteamento de modelos (Model Routing)
- Explica o trade-off entre modelos mais baratos para tarefas mais simples e modelos mais caros para tarefas mais complexas.
- Apresenta a lógica por trás de model routing e cita provedores e camadas agnósticas que permitem chamar vários modelos diferentes, como OpenRouter, Cursor e similares.

## Parte 3: Padrões de projeto

### 1. Especialista aumentado com IA

### 2. IA em atendimento de clientes (vendas e afins)

### 3. Talk to your data

### 4. IA para compliance

### 5. Processamento inteligente de documentos para o ERP

### 6. Monitoramento proativo e diagnóstico de desvios

## Parte 4: Finalização

## Fora da ementa (vai para o entregável separado)

- **Critério de priorização para o primeiro passo (filtro usar / aumentar / não tocar):** entra no webinar, mas como parte do produto separado de roadmap, não como assunto da ementa.
