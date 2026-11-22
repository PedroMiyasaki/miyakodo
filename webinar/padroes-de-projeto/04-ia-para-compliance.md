# Padrão de projeto 4: IA para compliance

## Objetivo de negócio

Centralizar todas as legislações, normas e exigências de compliance aplicáveis à empresa em uma fonte única, viva e validada por humanos, e transformar essa base em um serviço ativo que tanto **permite às equipes consultar e validar materiais no dia a dia** quanto **verifica automaticamente textos e assets via API** para dizer se estão em conformidade ou não.

Em vez de depender de planilhas desatualizadas, consultas manuais demoradas ao jurídico ou cada área interpretando regras regulatórias do próprio jeito, este padrão cria uma camada central de inteligência regulatória que alimenta tanto as pessoas quanto os sistemas da empresa.

---

## Visão geral do fluxo

```text
[Fontes externas na internet]  (leis, normas setoriais, órgãos reguladores, portarias)
          |
          v
+-------------------------------------------------------------------+
|  INSTÂNCIA CUSTOMIZADA NA NUVEM (spawna múltiplos agentes)        |
|                                                                   |
|  [Agente 1]   [Agente 2]   [Agente N]   (coleta de conceitos,     |
|                                          leis e atualizações)     |
+--------------------------------|----------------------------------+
                                 |
                                 v
                     [Human-in-the-loop]
                     (jurídico / compliance valida o que
                      se aplica ao contexto da empresa)
                                 |
                                 v
            +-----------------------------------------+
            |  DATABASE CENTRALIZADO / KNOWLEDGE BASE |
            |  (legislações, regras e requisitos de   |
            |   compliance oficiais da empresa)       |
            +--------------|------------|-------------+
                           |            |
        exposição via      |            |  conexão direta
        RAG + MCP          |            |  (RAG / MCP / Tools)
                           v            v
  +-----------------------------+  +----------------------------------+
  |  INSTÂNCIAS LOCAIS DAS      |  |  INSTÂNCIA CUSTOMIZADA DE        |
  |  PESSOAS DA EMPRESA         |  |  VALIDAÇÃO VIA API               |
  |  (Claude, Codex, Cursor,    |  |                                  |
  |   assinatura Enterprise)    |  |  Recebe texto / asset via API    |
  |                             |  |  de outros sistemas da empresa   |
  |  Lê regras + usa Skills     |  |              |                   |
  |  para consultar dúvidas e   |  |              v                   |
  |  validar assets internos    |  |  Devolve Saída estruturada:      |
  |                             |  |  em conformidade ou não +        |
  |                             |  |  norma/motivo (+ alerta humano   |
  |                             |  |  se necessário)                  |
  +-----------------------------+  +----------------------------------+
```

---

## Arquitetura passo a passo (conectada aos conceitos da Parte 2)

### 1. Coleta automatizada com múltiplos agentes em nuvem
- **Como funciona:** uma instância customizada na nuvem consegue **spawnar vários agentes** conforme a necessidade da empresa (por exemplo, um agente por frente regulatória, órgão fiscalizador ou tema legal). Esses agentes monitoram e coletam na internet as documentações, legislações, conceitos e atualizações de compliance relevantes para o contexto do negócio, consolidando tudo em um único lugar.
- **Por que usar múltiplos agentes aqui:** acompanhar mudanças regulatórias em várias frentes manualmente é caro e lento. Spawnar agentes especializados em coleta permite cobrir várias fontes em paralelo sem depender de acompanhamento manual constante.
- **Conceitos da Parte 2:**
  - **Superfície de entrega (onde a IA vive na empresa):** esta primeira camada vive em uma **camada de aplicação customizada na nuvem da própria empresa**, preparada para orquestrar e spawnar múltiplos agentes de forma contínua e controlada.
  - **One-off LLM call vs Workflow vs Agente:** usa **Agentes** para buscar, navegar e extrair conceitos e normas em fontes abertas na internet, orquestrados dentro de um **Workflow** recorrente de ingestão e revisão.
  - **Anatomia de agente, Harness e Memória/Estado:** **harness próprio** definindo o System Prompt de cada agente coletor (foco no contexto da empresa e no que filtrar), o Toolset de busca e leitura documental, e a **memória/estado** para controlar o que já foi capturado e destacar apenas novidades ou alterações de norma.

### 2. Curadoria e validação humana (Human-in-the-loop)
- **Como funciona:** nada do que os agentes coletaram na internet entra direto como verdade oficial da empresa. Tudo passa primeiro por uma **camada de validação com Human-in-the-loop** conduzida pelo time jurídico ou de compliance, que revisa os conceitos e legislações trazidos pelos agentes, confirma o que realmente se aplica ao negócio, ajusta interpretações e aprova a publicação.
- **Por que essa etapa é inegociável:** em compliance, erro de interpretação ou fonte desatualizada gera risco legal e financeiro real. Os agentes eliminam o trabalho pesado de busca e consolidação; o especialista humano garante a validade jurídica da regra que a empresa vai seguir.
- **Conceito da Parte 2:** **Human-in-the-loop** (atuando como portão de governança e validação antes que qualquer norma passe a valer na base oficial) e o fio transversal de **governança e centralização**.

### 3. Database centralizado (Knowledge Base de Compliance)
- **Como funciona:** uma vez validados pelos humanos, todos os conceitos, legislações, obrigações e regras de compliance viram um **database centralizado (Knowledge Base)** oficial da empresa. Essa base passa a ser a fonte única da verdade regulatória para qualquer pessoa ou sistema dentro do negócio.
- **Exposição dupla dos dados:** essa Knowledge Base não fica trancada em um portal morto. Ela é disponibilizada tanto para consumo em ferramentas de IA corporativas quanto via **MCP**, permitindo acesso estruturado e governado sem duplicar arquivos.
- **Conceitos da Parte 2:** **Camada de dados e ações** (**RAG** sobre a Knowledge Base para lidar com grandes volumes de leis e regulamentos, combinada com **MCP** para expor esse conhecimento de forma padronizada a diferentes ferramentas e instâncias) e o fio transversal de **governança e centralização**.

### 4. Consumo pelas equipes nas instâncias locais (consulta e validação de assets)
- **Como funciona:** com a Knowledge Base exposta via **MCP**, diferentes pessoas da empresa (jurídico, marketing, comercial, produto, operações) conectam suas próprias **instâncias locais de IA** (como Claude, Codex, Cursor ou assinatura Enterprise) diretamente à base oficial de compliance. A partir dali, conseguem tirar dúvidas sobre legislações aplicáveis e validar diferentes assets da empresa (documentos, contratos, materiais de comunicação, procedimentos) no próprio fluxo de trabalho.
- **Padronização das revisões:** os roteiros recorrentes de checagem por tipo de material (ex.: validar uma peça comercial, revisar cláusulas de um contrato ou conferir um comunicado regulatório) ficam registrados como **Skills** compartilhadas, evitando que cada colaborador valide compliance de um jeito improvisado.
- **Conceitos da Parte 2:**
  - **Superfície de entrega (onde a IA vive na empresa):** este padrão mostra um desenho **híbrido**, combinando a aplicação customizada na nuvem (que alimenta e governa a base) com a **máquina de cada funcionário** ou **assinaturas Enterprise** na ponta de consumo das equipes.
  - **Skills:** métodos repetitivos de checagem e consulta de compliance viram skills reutilizáveis pela empresa inteira.

### 5. Camada de validação automatizada via API
- **Como funciona:** além do uso pelas pessoas, uma **instância customizada de validação** conectada à mesma Knowledge Base expõe uma **API** para outros sistemas da empresa. Qualquer fluxo interno (CRM, sistema de contratos, plataforma de atendimento, ferramenta de publicação de conteúdo ou aprovação comercial) envia um pedaço de texto ou asset via API e recebe de volta uma análise objetiva dizendo **se aquilo está em conformidade ou não** com as legislações e normas vigentes da base, junto com os apontamentos e a referência da norma correspondente.
- **Saída pronta para integração automática:** em vez de responder com um parecer longo em texto livre, essa camada devolve uma **saída estruturada** (por exemplo: status de conformidade, severidade, itens violados, trecho problemático e referência na Knowledge Base), permitindo que o sistema chamador libere o fluxo, bloqueie o envio ou acione revisão humana (**Human-in-the-loop** na ponta das exceções).
- **Conceitos da Parte 2:**
  - **Saída estruturada (Structured Outputs):** essencial na camada via API para transformar a avaliação de compliance em decisão padronizada e integrável em sistemas automáticos da empresa.
  - **One-off LLM call vs Workflow vs Agente:** a validação via API roda tipicamente como **Workflow / One-off LLM call** previsível e auditável sobre a Knowledge Base, garantindo consistência nas checagens.
  - **Roteamento de modelos (Model Routing):** modelos mais baratos e rápidos para triagens simples, extrações e validações rotineiras de alto volume via API; modelos mais capazes para interpretação de legislações complexas, coleta analítica e pareceres sensíveis.
  - **Evals (verificação de resposta):** bateria objetiva de testes com textos sabidamente conformes e sabidamente fora de conformidade para garantir que a camada de validação mantenha precisão (evitando deixar passar infrações reais ou gerar bloqueios indevidos) à medida que novas leis entram na base.

---

## Resumo do mapeamento com os conceitos da Parte 2

| Conceito (Parte 2) | Como aparece neste padrão |
| --- | --- |
| **One-off LLM call vs Workflow vs Agente** | **Múltiplos agentes** na coleta de leis e conceitos na internet; **Workflow** previsível na ingestão/revisão e na camada de validação de textos e assets via API. |
| **Anatomia de agente, Harness e Memória/Estado** | **Harness customizado** em nuvem controlando o spawning dos agentes coletores, o System Prompt regulatório, o Toolset de busca/consulta e a memória/estado do que já foi coletado e atualizado. |
| **Evals (verificação de resposta)** | Verificação em casos conhecidos (materiais conformes e não conformes) para dar direção de evolução à precisão da coleta e da camada de validação via API. |
| **Saída estruturada (Structured Outputs)** | Essencial na instância de validação via API: devolve veredito padronizado (em conformidade ou não, severidade, motivo e norma de referência) pronto para integração com outros sistemas. |
| **Human-in-the-loop** | **Portão central de validação:** humanos validam as legislações e conceitos coletados pelos agentes antes de entrarem na Knowledge Base oficial (e também revisam exceções/bloqueios apontados pela API). |
| **Skills** | Roteiros padronizados de checagem e validação de compliance por tipo de asset, reutilizados pelas pessoas nas instâncias locais e pela camada de validação. |
| **Camada de dados e ações** | **Database centralizado / Knowledge Base** de compliance acessado via **RAG** (grande volume de legislações) e disponibilizado via **MCP** para instâncias locais e para a API de validação. |
| **Superfície de entrega (onde a IA vive na empresa)** | **Desenho híbrido:** **camada de aplicação customizada na nuvem** (coleta multiagente, Knowledge Base e validação via API) combinada com **máquina de cada funcionário / assinaturas Enterprise** para consultas e validações locais via MCP. |
| **Roteamento de modelos (Model Routing)** | Modelos rápidos e baratos para triagens e checagens de alto volume; modelos mais capazes para interpretar legislação complexa e validar casos sensíveis. |
| **Governança e centralização (transversal)** | Todas as legislações que a empresa precisa seguir reunidas e validadas em uma única Knowledge Base oficial, consumida de forma controlada por pessoas e sistemas. |

---

## Conexão com os Princípios básicos (Parte 1)

- **Princípio 1 (Natureza probabilística da IA):** a IA resolve o trabalho probabilístico de localizar, sintetizar e confrontar textos contra legislações extensas; a validação humana da base oficial, a saída estruturada da API e as travas nos sistemas determinísticos garantem segurança regulatória.
- **Princípio 2 (Engenharia de contexto):** a validação só é confiável porque toda consulta (seja de um funcionário via MCP ou de um sistema via API) consome a mesma Knowledge Base centralizada, curada e atualizada, e não conhecimento genérico do modelo.
- **Princípio 3 (A IA é uma ferramenta, não um objetivo final):** o padrão resolve uma dor concreta de risco e escala em empresas médias: manter conformidade viva em toda a operação sem transformar o time jurídico ou de compliance em gargalo manual.
