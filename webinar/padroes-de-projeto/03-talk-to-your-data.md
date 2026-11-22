# Padrão de projeto 3: Talk to your data

## Objetivo de negócio

Permitir que sócios, diretores, gestores e analistas façam perguntas em linguagem natural diretamente sobre os dados da empresa (financeiro, comercial, estoque, operação, ERP, CRM) e recebam respostas confiáveis, tabelas e análises em segundos, sem depender de dashboards engessados nem esperar dias na fila do time de BI ou TI.

Um ponto central para o empresário entender aqui é que a IA **não calcula de cabeça**. Ela traduz a pergunta de negócio para consultas precisas em cima da base de dados da empresa, deixa o banco executar a conta exata e devolve a leitura organizada, com total transparência sobre os filtros e critérios usados.

---

## Visão geral do fluxo

```text
[Sócio / Gestor / Analista]
   ("Qual foi nossa margem por região no último trimestre e
     quais clientes puxaram a queda?")
          |
          v
+-------------------------------------------------------------------+
|  INTERFACE ANALÍTICA (Aplicação em nuvem OU Workspace via MCP)    |
|                                                                   |
|  System Prompt rigoroso + Model Routing + Memória da investigação |
|                              |                                    |
|                 [Workflow / Agente Analítico]                     |
|                   /         |            \                        |
|        consulta  /          | consulta    \  segue                |
|        regras   /           | somente      \                      |
|                v            | leitura       v                     |
|  [Camada semântica e        |        [Repositório de Skills]      |
|   dicionário de KPIs]       |        (análises recorrentes:       |
|  (o que é receita líquida,  |         margem, churn, inadimpl.)   |
|   cliente ativo, margem)    v                                     |
|               [Camada de Dados Governada (read-only)]             |
|               (views curadas de ERP, CRM, financeiro, BI          |
|                com permissão por cargo/área)                      |
|                              |                                    |
|                              | banco executa cálculo exato        |
|                              v                                    |
|  [Saída estruturada: números, tabela, gráfico + filtros usados]   |
+----------------------------------|--------------------------------+
                                   |
                                   v
                   [Human-in-the-loop]
                   (gestor confere critérios/filtros na resposta;
                    time de negócio/dados governa KPIs e views)
```

---

## Arquitetura passo a passo (conectada aos conceitos da Parte 2)

### 1. Camada de dados governada e dicionário de métricas (a base que evita número errado)
- **Como funciona:** o erro mais comum em projetos de "conversar com dados" é plugar uma IA diretamente nas tabelas brutas do banco de produção. Sem contexto de negócio, a IA erra nomes de colunas, mistura pedidos cancelados com faturados ou calcula margem diferente da do financeiro. Por isso, este padrão prepara primeiro uma **camada analítica curada (somente leitura)** sobre os dados de ERP, CRM, financeiro e operação, acompanhada de um **dicionário de negócio (camada semântica)** que define oficialmente cada indicador (receita líquida, margem de contribuição, cliente ativo, inadimplência, churn), com permissões de acesso por perfil de usuário.
- **Conceito da Parte 2:** **Camada de dados e ações** (**RAG** sobre o dicionário de dados, glossário de KPIs e documentação de tabelas quando o ambiente é grande; **MCP** ou **Tools** somente leitura para executar consultas sobre views governadas) e o fio transversal de **governança e centralização** (cada cargo só enxerga os dados a que tem permissão).

### 2. Tradução da pergunta em consultas determinísticas (Workflow e Agente)
- **Como funciona:** o usuário faz uma pergunta em português normal. O sistema entende a intenção, consulta o dicionário oficial de KPIs para usar a regra certa da empresa, gera a consulta exata contra a camada de dados (por exemplo, SQL ou consulta sobre views), executa essa consulta no banco de dados (que faz toda a matemática de forma 100% determinística) e interpreta o resultado retornado.
- **Do simples ao investigativo:** perguntas diretas ("quanto faturamos em outubro na região Sul?") seguem um **Workflow** enxuto e previsível. Perguntas exploratórias ("por que a margem caiu no último trimestre?") acionam um **Agente** que faz várias consultas encadeadas (quebra por região, depois por produto, depois por cliente) até montar o diagnóstico.
- **Conceitos da Parte 2:**
  - **One-off LLM call vs Workflow vs Agente:** **Workflow** previsível para perguntas diretas e padronizadas; **Agente** controlado quando a análise exige investigação em múltiplos passos sobre os dados.
  - **Skills:** análises gerenciais que a diretoria pede toda semana ou todo mês (fechamento de margem, curva ABC de clientes, aging de inadimplência, performance comercial por vendedor) viram **Skills** oficiais, garantindo que qualquer gestor receba a análise calculada exatamente sob o mesmo método da empresa.

### 3. Harness rigoroso, Toolset somente leitura e Memória da sessão
- **Como funciona:** o ambiente em volta do modelo é desenhado para impedir números inventados e proteger a integridade dos dados:
  - **System Prompt customizado:** instrui a IA a nunca estimar nem calcular números de cabeça, sempre consultar a base, respeitar as definições oficiais de KPIs, explicitar período e filtros aplicados na resposta e avisar quando não houver dado suficiente.
  - **Toolset customizado (estritamente read-only):** ferramentas para inspecionar o catálogo de tabelas/métricas, validar e rodar consultas somente leitura com limites de segurança (tempo e volume) e formatar tabelas ou gráficos. A IA nunca tem permissão de alterar ou apagar dados.
  - **Memória e estado:** mantém o fio da conversa analítica para perguntas de acompanhamento ("agora abre só os 10 maiores clientes", "tira as devoluções dessa conta", "compara com o mesmo período do ano passado") sem precisar recomeçar a pergunta do zero.
- **Conceito da Parte 2:** **Anatomia de agente, Harness e Memória/Estado** (controle do harness garantindo disciplina analítica, toolset somente leitura e estado contínuo da investigação).

### 4. Superfície de entrega e saída pronta para decisão
- **Onde o gestor conversa com os dados:** este padrão funciona bem em duas superfícies, conforme o estágio da empresa:
  - **Camada de aplicação customizada na nuvem da própria empresa:** um portal interno de análise ou bot corporativo (Slack, Teams, WhatsApp interno) quando a empresa quer controle rígido de permissões por cargo, renderização de gráficos/tabelas e trilha completa de auditoria.
  - **Na máquina de cada funcionário ou assinaturas Enterprise (via MCP):** analistas e líderes conectando sua IA (Claude, ChatGPT Enterprise, Gemini Enterprise, Cursor) diretamente ao **MCP interno** da camada analítica governada.
- **Controle de saída:** a resposta devolve não apenas um texto resumido, mas **saídas estruturadas** (consulta/parâmetros gerados para o banco, tabela de dados, especificação de gráfico e bloco de auditoria mostrando período, filtros e definição de KPI aplicados), permitindo conferência rápida ou exportação direta para relatórios e apresentações.
- **Conceitos da Parte 2:** **Superfície de entrega (onde a IA vive na empresa)** e **Saída estruturada (Structured Outputs)**.

### 5. Governança humana, custo sob controle e validação contra gabarito
- **Papel humano em duas frentes:** o time de negócio/financeiro/dados valida e mantém as definições de métricas, views e skills (evitando o "cada área tem um número diferente"), enquanto o gestor que consome a resposta consegue conferir os filtros e critérios exibidos antes de levar um número para uma decisão crítica.
- **Roteamento de modelos para equilibrar custo e precisão:** modelos rápidos e baratos classificam a pergunta, buscam quais tabelas/definições são relevantes e formatam respostas triviais; modelos mais capazes entram para traduzir perguntas de negócio complexas em consultas precisas de múltiplos passos e interpretar desvios.
- **Verificação contra números reais (gabarito):** em Talk to your data, errar um número destrói a confiança da diretoria no projeto inteiro. Por isso, o time mantém uma bateria de perguntas reais de negócio com os números já fechados pelo financeiro/BI para testar automaticamente se a IA continua batendo o valor exato a cada mudança de tabela, skill ou modelo.
- **Conceitos da Parte 2:** **Human-in-the-loop**, **Roteamento de modelos (Model Routing)** e **Evals (verificação de resposta)**.

---

## Resumo do mapeamento com os conceitos da Parte 2

| Conceito (Parte 2) | Como aparece neste padrão |
| --- | --- |
| **One-off LLM call vs Workflow vs Agente** | **Workflow** estruturado para consultas diretas e previsíveis; **Agente** controlado quando a pergunta exige várias consultas investigativas em sequência. |
| **Anatomia de agente, Harness e Memória/Estado** | **Harness rigoroso** com System Prompt antialucinação numérica, Toolset estritamente **somente leitura** e memória/estado preservando o fio das perguntas de aprofundamento na sessão. |
| **Evals (verificação de resposta)** | **Crítico no padrão:** bateria de perguntas reais de negócio com números já conferidos pelo financeiro/BI (gabarito) para garantir precisão antes e depois de qualquer alteração. |
| **Saída estruturada (Structured Outputs)** | Gera consultas/parâmetros válidos para o banco e entrega resultados padronizados (tabelas, dados de gráficos e metadados de filtros/critérios aplicados). |
| **Human-in-the-loop** | Time de negócio/dados governa o dicionário de KPIs, views e skills; o gestor valida os critérios e filtros exibidos em análises críticas de decisão. |
| **Skills** | Análises gerenciais recorrentes (margem, curva ABC, inadimplência, fechamento comercial) registradas como métodos oficiais para padronizar como a empresa lê seus números. |
| **Camada de dados e ações** | **Coração técnico do padrão:** views analíticas governadas (read-only) com permissão por perfil + camada semântica/dicionário de KPIs via **RAG**, acessados por **MCP** ou **Tools** de consulta segura. |
| **Superfície de entrega (onde a IA vive na empresa)** | **Camada de aplicação customizada na nuvem** (chat analítico interno, Slack/Teams) ou **instâncias locais / assinaturas Enterprise** conectadas via **MCP** à camada de dados. |
| **Roteamento de modelos (Model Routing)** | Modelos rápidos e baratos para triagem e consultas simples; modelos mais capazes para traduzir perguntas complexas em consultas encadeadas e análises de causa. |
| **Governança e centralização (transversal)** | Controle de acesso por cargo, definição única de indicadores da empresa, permissões somente leitura e transparência sobre filtros e origem de cada número. |

---

## Conexão com os Princípios básicos (Parte 1)

- **Princípio 1 (Natureza probabilística da IA):** exemplo clássico da divisão certa de papéis. A IA cuida da parte probabilística (entender a pergunta em linguagem natural e traduzir para consulta), enquanto o banco de dados faz a parte determinística (cálculo exato), sem deixar a LLM "chutar" números.
- **Princípio 2 (Engenharia de contexto):** sem a camada semântica, o dicionário de KPIs e views organizadas, o melhor modelo do mundo devolve o número errado; o valor do projeto está no contexto estruturado em volta dos dados.
- **Princípio 3 (A IA é uma ferramenta, não um objetivo final):** o foco não é ter um chat bonito em cima do banco, e sim dar velocidade e clareza para a liderança enxergar margem, receita, gargalos e desvios no core business sem ficar travada na fila de BI.
