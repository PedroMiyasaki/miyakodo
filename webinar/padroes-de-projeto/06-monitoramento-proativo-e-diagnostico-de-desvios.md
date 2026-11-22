# Padrão de projeto 6: Monitoramento proativo e diagnóstico de desvios

## Objetivo de negócio

Tirar o dono e a diretoria do modo reativo (descobrir problemas só no fechamento do mês, quando a margem já caiu, o estoque rompeu ou o cliente importante já cancelou) e colocar uma camada contínua de vigilância inteligente rodando em background sobre a operação.

Este padrão funciona como o **espelho proativo do Talk to your data** (Padrão 3): enquanto no Talk to your data o gestor precisa lembrar de abrir a ferramenta e fazer a pergunta certa, aqui o sistema monitora a empresa periodicamente, detecta anomalias relevantes, investiga o porquê cruzando números com textos operacionais e aciona o responsável certo com um diagnóstico curto e acionável.

---

## Visão geral do fluxo

```text
[Operação viva da empresa]  (ERP, financeiro, estoque, CRM, logística, e-mails, chamados)
          |
          |  execução agendada / contínua em background
          v
+-------------------------------------------------------------------+
|  APLICAÇÃO DE MONITORAMENTO EM NUVEM (Harness próprio)            |
|                                                                   |
|  1. Detecção de desvio (regras determinísticas + Workflow)        |
|     (queda de margem, ruptura, atraso, despesa fora da curva,     |
|      cliente-chave sem comprar)                                   |
|          |                                                        |
|          | só aciona IA profunda quando há desvio real            |
|          v                                                        |
|  2. Investigação de causa (Agente + Model Routing)                |
|        |                                      |                   |
|        | cruza números + textos               | segue critérios   |
|        v                                      v                   |
|  [Camada de dados e ações]            [Repositório de Skills]     |
|  (views do ERP/CRM/financeiro         (roteiros de diagnóstico    |
|   + ocorrências, chamados,             por área: margem, estoque, |
|   e-mails via MCP / Tools / RAG)       inadimplência, churn)      |
|        |                                                          |
|        v                                                          |
|  3. Alerta estruturado (Saída estruturada: severidade, causa      |
|     provável, impacto financeiro, dono da área, ação sugerida)    |
+----------------------------------|--------------------------------+
                                   |
          envio proativo           |  (WhatsApp, Slack, Teams, e-mail)
                                   v
                   [Human-in-the-loop]
                   (sócio ou gestor recebe apenas o que importa,
                    decide e aprova a ação corretiva na hora)
```

---

## Arquitetura passo a passo (conectada aos conceitos da Parte 2)

### 1. Vigilância em background: detecção determinística antes de acionar IA
- **Como funciona:** em ciclos definidos pela empresa (de hora em hora, diariamente ou por evento), uma aplicação em nuvem verifica indicadores críticos do negócio: margem abaixo do piso, despesa fora da curva, atraso recorrente em transportadora, estoque caminhando para ruptura, cliente relevante que parou de comprar ou aumento súbito de reclamações.
- **Economia e rigor pelo Princípio 1:** a primeira camada de disparo usa **regras determinísticas e cálculos diretos no banco** (não gasta IA procurando agulha no palheiro sem necessidade). A IA só é acionada quando existe um desvio concreto que precisa ser investigado e explicado.
- **Conceitos da Parte 2:**
  - **Superfície de entrega (onde a IA vive na empresa):** roda em uma **camada de aplicação customizada na nuvem da própria empresa** em background (sem depender de ninguém lembrar de abrir um chat), entregando os alertas diretamente nos canais onde os decisores já olham (WhatsApp, Slack, Teams ou e-mail).
  - **One-off LLM call vs Workflow vs Agente:** arquitetura híbrida em duas etapas: **Workflow** agendado com checagens determinísticas para levantar sinais -> **Agente** investigador acionado apenas para diagnosticar os desvios relevantes.

### 2. Investigação da causa cruzando dado estruturado e contexto textual
- **Como funciona:** saber que "a margem da linha X caiu 4 pontos nesta semana" um alerta tradicional de BI já avisa. O diferencial da IA entra no passo seguinte: o **Agente** investiga **por que** aquilo aconteceu, cruzando os números do ERP/financeiro com informações não estruturadas (e-mails comerciais, justificativas de desconto, ocorrências logísticas, chamados de suporte, atas de reunião ou notas de compras).
- **Exemplo prático:** em vez de mandar só "cliente Alfa reduziu pedidos em 60%", o agente cruza ERP + CRM + suporte e devolve: "cliente Alfa reduziu pedidos após três entregas atrasadas pela transportadora Y nas últimas duas semanas e um chamado de avaria ainda aberto no pós-venda".
- **Conceitos da Parte 2:**
  - **Camada de dados e ações:** combina consultas somente leitura a dados estruturados do ERP, CRM e financeiro (via **MCP / Tools**) com busca sobre histórico textual de ocorrências, chamados e comunicações (via **RAG / Tools**).
  - **Skills:** roteiros oficiais de investigação por tipo de alerta (ex.: "como diagnosticar queda de margem", "como investigar risco de churn em conta B2B", "como apurar desvio de frete"), mantidos pelos líderes das áreas para que a IA sempre cheque as hipóteses certas.

### 3. Harness próprio com memória histórica para evitar "fadiga de alerta"
- **Como funciona:** o maior risco de qualquer sistema de alertas é mandar notificações repetitivas, rasas ou irrelevantes até o gestor parar de ler. Por isso, a empresa controla o harness completo:
  - **System Prompt customizado:** exige síntese executiva curta, citação obrigatória das evidências consultadas (números e registros) e proibição de especular causa sem lastro nos dados.
  - **Toolset customizado (somente leitura + notificação):** ferramentas para consultar indicadores, investigar registros relacionados e enviar alertas ao responsável correto, sem autonomia para executar mudanças financeiras ou operacionais sozinho.
  - **Memória e estado:** registra quais desvios já foram alertados, quais o gestor já marcou como conhecidos/justificados (por exemplo, uma campanha promocional planejada) e acompanha se o problema está melhorando ou piorando ao longo dos dias. Isso evita repetir o mesmo alerta toda manhã.
- **Conceito da Parte 2:** **Anatomia de agente, Harness e Memória/Estado** (memória/estado como peça central para diferenciar desvio novo de problema já tratado e evitar ruído).

### 4. Alerta padronizado e decisão humana imediata
- **Saída pronta para ação:** cada alerta gerado segue uma **Saída estruturada** contendo categoria do desvio, severidade (`baixo`, `médio`, `crítico`), impacto financeiro estimado, causa provável com evidências, área/dono responsável e sugestões objetivas de ação corretiva. Essa estrutura permite tanto enviar uma mensagem limpa no canal do gestor quanto abrir tarefa automática no sistema de gestão.
- **Humano no comando da ação:** a IA detecta, investiga e resume; quem decide segurar um pagamento, ligar para o cliente, trocar transportadora ou ajustar preço é o gestor ou sócio.
- **Conceitos da Parte 2:** **Saída estruturada (Structured Outputs)** e **Human-in-the-loop** (IA faz a vigilância e a investigação; humano valida o diagnóstico e executa ou aprova a ação corretiva).

### 5. Roteamento de modelos e calibração de sinal vs ruído
- **Custo sob controle no monitoramento contínuo:** modelos rápidos e baratos fazem a triagem de textos/ocorrências e classificam se um sinal merece atenção; modelos mais capazes entram apenas para montar o diagnóstico cruzado de desvios críticos.
- **Calibração contínua (sinal vs ruído):** a empresa avalia periodicamente o histórico de alertas enviados com uma métrica simples de negócio: quantos alertas foram de fato úteis/acionáveis para os gestores, quantos foram ruído irrelevante e se algum desvio relevante passou sem alerta.
- **Conceitos da Parte 2:** **Roteamento de modelos (Model Routing)** e **Evals (verificação de resposta)**.

---

## Resumo do mapeamento com os conceitos da Parte 2

| Conceito (Parte 2) | Como aparece neste padrão |
| --- | --- |
| **One-off LLM call vs Workflow vs Agente** | **Workflow** agendado com regras determinísticas detecta o desvio; **Agente** investigador entra sob demanda para cruzar fontes e diagnosticar a causa. |
| **Anatomia de agente, Harness e Memória/Estado** | **Harness customizado** com System Prompt executivo baseado em evidências, Toolset somente leitura + envio de alerta, e **memória/estado** rastreando desvios já notificados ou justificados para evitar fadiga de alerta. |
| **Evals (verificação de resposta)** | Acompanhamento objetivo de sinal vs ruído (proporção de alertas úteis/acionáveis, falsos alarmes e desvios reais que passaram batido) para calibrar skills e limiares. |
| **Saída estruturada (Structured Outputs)** | Gera alerta padronizado com severidade, impacto estimado, causa com evidências, responsável e ação sugerida, alimentando canais de aviso ou tarefas internas. |
| **Human-in-the-loop** | Sócio ou gestor recebe o diagnóstico pronto no canal que já usa, decide a correção e pode marcar exceções conhecidas que retroalimentam a memória do sistema. |
| **Skills** | Roteiros de diagnóstico por tipo de desvio (margem, estoque, frete, inadimplência, churn) escritos pelos gestores de cada área. |
| **Camada de dados e ações** | Combina consultas a dados estruturados (ERP, financeiro, CRM via **MCP / Tools**) com busca sobre textos operacionais (e-mails, chamados, ocorrências via **RAG / Tools**). |
| **Superfície de entrega (onde a IA vive na empresa)** | **Camada de aplicação customizada na nuvem da própria empresa** rodando em background, com entrega proativa em canais já usados (WhatsApp, Slack, Teams, e-mail). |
| **Roteamento de modelos (Model Routing)** | Modelos rápidos e baratos na triagem contínua de sinais; modelos mais capazes reservados para investigação cruzada de desvios relevantes. |
| **Governança e centralização (transversal)** | Regras oficiais de alerta e limiares centralizados, acesso somente leitura por escopo de área e trilha histórica de cada desvio detectado e tratado. |

---

## Conexão com os Princípios básicos (Parte 1)

- **Princípio 1 (Natureza probabilística da IA):** usa código e cálculo determinístico para detectar desvios numéricos com precisão e custo mínimo, acionando a IA probabilística exatamente onde ela brilha: cruzar números com textos soltos para explicar a causa do problema.
- **Princípio 2 (Engenharia de contexto):** o diagnóstico só acerta porque o agente recebe contexto completo (dados do ERP/CRM, histórico de ocorrências, skills de diagnóstico da área e memória do que já foi justificado).
- **Princípio 3 (A IA é uma ferramenta, não um objetivo final):** protege margem, caixa, operação e carteira de clientes antes que pequenos desvios virem prejuízo grande no fechamento do mês.
