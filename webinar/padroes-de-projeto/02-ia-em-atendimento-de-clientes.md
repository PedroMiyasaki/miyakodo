# Padrão de projeto 2: IA em atendimento de clientes (vendas e afins)

## Objetivo de negócio

Escalar atendimento comercial, relacionamento e **venda ativa** com consistência e memória de longo prazo sobre cada cliente, sem perder controle sobre políticas comerciais nem expor a empresa a decisões financeiras indevidas.

Diferente de chatbots antigos de menu fixo (que travam fora de meia dúzia de opções) e diferente de dar um chat solto para cada vendedor, este padrão coloca uma instância controlada de IA conversando diretamente com os clientes nos canais da empresa, lembrando o histórico de cada pessoa, seguindo regras centralizadas e escalando decisões sensíveis para validação humana.

---

## Visão geral do fluxo

```text
[Canais de atendimento]  (WhatsApp, chat do site, Instagram, e-mail etc.)
          ^
          |  conversa reativa + abordagens de venda ativa
          v
+-------------------------------------------------------------------+
|  APLICAÇÃO CUSTOMIZADA NA NUVEM DA EMPRESA (Harness próprio)      |
|                                                                   |
|  System Prompt customizado + Workflows críticos + Model Routing   |
|                              |                                    |
|                     [Agente de Atendimento]                       |
|                   /       |            \                          |
|        Toolset   /        | lê/grava    \  usa                    |
|     customizado /         v              \                        |
|                /  [Camada de Persistência] \                      |
|               /   (histórico de conversas,  \                     |
|              /     compras, preferências)    \                    |
|             v                                 v                   |
|   [Regras, Políticas e Dados]          [Repositório de Skills]    |
|   (catálogo, preços, ERP, CRM)         (qualificação, venda ativa,|
|                                         objeções, trocas)         |
+---------------------------|-----------------------|---------------+
                            |                       |
          saída estruturada |                       | decisão crítica
          (CRM, ERP,        |                       | (reembolso, desconto
           pedidos)         v                       v  fora da regra etc.)
                 [Sistemas da empresa]      [Human-in-the-loop]
                                            (validação e aprovação
                                             humana antes de agir)
```

---

## Arquitetura passo a passo (conectada aos conceitos da Parte 2)

### 1. Aplicação customizada na nuvem conectada aos canais do cliente
- **Como funciona:** a IA roda em uma aplicação própria hospedada na nuvem da empresa, integrada aos canais onde o cliente já fala com o negócio (WhatsApp, chat, e-mail, redes sociais). Essa mesma instância consegue responder demandas que chegam (atendimento receptivo) e iniciar contatos relevantes no momento certo (venda ativa).
- **Por que muda o jogo frente ao Padrão 1:** como aqui a IA conversa direto com o cliente final e opera em escala, ela não pode depender da máquina de um funcionário. Precisa rodar de forma centralizada, contínua e auditável.
- **Conceitos da Parte 2:**
  - **Superfície de entrega (onde a IA vive na empresa):** aqui a IA vive em uma **camada de aplicação customizada na nuvem da própria empresa**, trazendo o maior nível de controle, rastreabilidade e governança sobre o que entra e sai das conversas.
  - **One-off LLM call vs Workflow vs Agente:** combina um **Agente** (para conduzir a conversa natural, tirar dúvidas e personalizar a oferta) com **Workflows** previsíveis para etapas obrigatórias e sensíveis (como fechamento de pedido, emissão de cobrança ou solicitação de devolução).

### 2. Harness próprio: System Prompt, Toolset customizado e Memória persistida
- **Como funciona:** como a empresa constrói a aplicação, ela controla todo o ambiente em volta do modelo:
  - **System Prompt customizado:** define a identidade da empresa, o tom da conversa, o objetivo comercial e os limites rígidos do que o agente pode ou não fazer (por exemplo, nunca inventar condição fora da tabela nem prometer reembolso sem aprovação).
  - **Toolset customizado:** delimita exatamente quais ações a IA tem permissão para executar (consultar catálogo e preço, checar status de entrega, consultar histórico de pedidos, registrar oportunidade no CRM, disparar pedido de aprovação humana).
  - **Camada de persistência (memória por cliente):** grava e recupera o histórico de conversas, compras anteriores, preferências e momento de cada cliente. É isso que permite que a IA atenda sem fazer o cliente repetir tudo e viabiliza a **venda ativa** inteligente (por exemplo, lembrar o que o cliente já comprou para sugerir reposição, complemento ou retomada de orçamento aberto).
- **Conceito da Parte 2:** **Anatomia de agente, Harness e Memória/Estado** (aqui a empresa assume o **controle do próprio harness**, aceitando mais investimento inicial de engenharia em troca de controle fino sobre comportamento, ferramentas e memória persistida por cliente).

### 3. Regras, políticas centralizadas, dados e método comercial
- **Como funciona:** em vez de deixar políticas de preço, prazos, trocas e abordagens de venda espalhadas na cabeça de cada atendente, a instância lê uma base centralizada e atualizada pela empresa:
  - **Regras, políticas e catálogo centralizados:** documentos de política comercial, tabela de preços, condições de entrega/troca e dados operacionais do ERP e CRM, acessados por **RAG** (quando há catálogos ou bases extensas de informação) e por **MCP / Tools** (para consultas em tempo real a pedidos, estoque e cadastro do cliente).
  - **Skills comerciais:** os procedimentos recorrentes de atendimento e vendas (qualificar um lead, contornar objeções comuns, conduzir recompra ou venda ativa, coletar dados de uma solicitação de troca) ficam registrados como métodos reutilizáveis. Quando a empresa altera uma campanha ou política comercial, basta atualizar a base central e a skill correspondente.
- **Conceitos da Parte 2:** **Camada de dados e ações** (RAG, MCP e Tools ligando a IA às políticas e sistemas reais), **Skills** (roteiros e métodos comerciais registrados como ativo da empresa) e o fio transversal de **governança e centralização**.

### 4. Validação humana em decisões críticas
- **Como funciona:** a IA resolve com autonomia o que está dentro das regras claras da empresa (tirar dúvidas, qualificar, apresentar produtos, acompanhar pedido, propor recompra). Porém, antes de qualquer decisão importante ou de risco financeiro/reputacional, o fluxo trava e pede aprovação de uma pessoa responsável.
- **Exemplos de gatilhos típicos:** devolução de dinheiro ou estorno, concessão de desconto fora da política padrão, cancelamento de contrato relevante, reclamação crítica ou qualquer exceção que o agente não consiga enquadrar com segurança. O agente entrega o resumo da conversa e a ação sugerida para o humano aprovar, ajustar ou assumir o atendimento.
- **Conceito da Parte 2:** **Human-in-the-loop**, atuando como barreira prática de segurança, validação e governança comercial antes de decisões irreversíveis ou caras.

### 5. Integração com sistemas, controle de custo e evolução contínua
- **Saída estruturada para movimentar a empresa:** enquanto conversa em linguagem natural com o cliente, a aplicação extrai e envia **saídas estruturadas** para os sistemas internos (atualiza o funil no CRM, registra intenção de compra, cria pedido ou ticket de reembolso no ERP e atualiza os campos de memória do cliente na camada de persistência).
- **Otimização de custo e velocidade em volume:** como atendimento envolve muitas mensagens curtas e repetitivas, o sistema não usa o modelo mais caro para tudo. Mensagens triviais (saudação, classificação de intenção, consulta simples de status, extração de dados) rodam em modelos mais rápidos e baratos; negociações complexas, recomendações consultivas e casos delicados são roteados para modelos mais capazes.
- **Verificação de qualidade antes e depois de ir ao ar:** como o agente fala em nome da marca, a empresa mantém uma rotina objetiva de checagem sobre conversas reais e cenários sensíveis (por exemplo, verificar se o agente respeita limites de preço, não promete o que não existe e realmente converte).
- **Conceitos da Parte 2:** **Saída estruturada (Structured Outputs)**, **Roteamento de modelos (Model Routing)** e **Evals (verificação de resposta)**.

---

## Resumo do mapeamento com os conceitos da Parte 2

| Conceito (Parte 2) | Como aparece neste padrão |
| --- | --- |
| **One-off LLM call vs Workflow vs Agente** | **Agente** para conduzir a conversa aberta e a venda ativa, combinado com **Workflows** previsíveis para passos críticos (fechamento, cobrança, estorno). |
| **Anatomia de agente, Harness e Memória/Estado** | **Harness customizado** com System Prompt próprio, Toolset controlado e **camada de persistência de memória/estado** por cliente (histórico de conversas e compras que viabiliza atendimento contínuo e venda ativa). |
| **Evals (verificação de resposta)** | Verificação objetiva em conversas reais e cenários críticos (regras de preço, política de reembolso, qualidade comercial) para guiar a evolução do agente sem degradar atendimento. |
| **Saída estruturada (Structured Outputs)** | Converte o que aconteceu na conversa em registros padronizados para atualizar CRM, ERP, pedidos e memória persistida do cliente automaticamente. |
| **Human-in-the-loop** | Trava obrigatória de validação humana antes de decisões importantes ou sensíveis (como devolução de dinheiro, descontos excepcionais ou casos críticos). |
| **Skills** | Métodos comerciais e de atendimento registrados de forma reutilizável (qualificação, contorno de objeção, venda ativa/recompra, triagem de troca). |
| **Camada de dados e ações** | Leitura centralizada de regras, políticas e catálogo (via **RAG** quando volumoso) e conexão em tempo real a pedidos, estoque e CRM (via **MCP / Tools**). |
| **Superfície de entrega (onde a IA vive na empresa)** | **Camada de aplicação customizada na nuvem da própria empresa**, conectada aos canais de atendimento e controlada centralmente. |
| **Roteamento de modelos (Model Routing)** | Modelos mais baratos e rápidos para interações e classificações simples; modelos mais capazes para negociação, venda consultiva e casos complexos. |
| **Governança e centralização (transversal)** | Políticas comerciais em fonte única, histórico rastreável por cliente, permissões restritas no toolset e aprovação humana nas decisões de risco. |

---

## Conexão com os Princípios básicos (Parte 1)

- **Princípio 1 (Natureza probabilística da IA):** a IA lida com a parte probabilística (entender o que o cliente quer em linguagem natural, relacionar histórico e propor oferta), enquanto workflows, regras de preço e sistemas determinísticos (CRM/ERP) garantem cálculo exato e execução controlada.
- **Princípio 2 (Engenharia de contexto):** o atendimento só fica bom e comercialmente útil porque o agente recebe contexto rico e atualizado (memória persistida do cliente, compras passadas, regras centralizadas e skills comerciais), não por causa de um prompt genérico.
- **Princípio 3 (A IA é uma ferramenta, não um objetivo final):** o projeto ataca diretamente receita, conversão, retenção e velocidade de resposta no funil comercial, onde o ganho aparece no resultado do negócio.
