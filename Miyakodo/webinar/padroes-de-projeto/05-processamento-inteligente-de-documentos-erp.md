# Padrão de projeto 5: Processamento inteligente de documentos para o ERP

## Objetivo de negócio

Eliminar trabalho manual repetitivo de digitação, leitura e conferência de documentos desestruturados (ordens de compra, romaneios, CT-e, notas fiscais de serviço de prefeituras diferentes, comprovantes de entrega, medições de obra, guias e laudos) que precisam entrar nos sistemas transacionais da empresa (ERP, WMS, financeiro).

Este padrão tem um papel didático muito forte para o empresário: mostra que **nem todo projeto de alto ROI precisa de chat nem de agente autônomo**. Aqui a IA atua nos bastidores dentro de um pipeline previsível, lendo a bagunça dos documentos, entregando dados estruturados e acionando o humano apenas nas exceções.

---

## Visão geral do fluxo

```text
[Entrada de documentos]  (e-mail, portal de fornecedores, WhatsApp, pasta, scanner)
   (PDFs, notas, ordens de compra, romaneios, comprovantes em dezenas de layouts)
          |
          v
+-------------------------------------------------------------------+
|  PIPELINE EM NUVEM (Workflow previsível + Harness próprio)        |
|                                                                   |
|  1. Classificação do documento (Model Routing: modelo barato)     |
|  2. Extração de campos (One-off LLM call + Saída estruturada)     |
|        |                                      |                   |
|        | aplica regras                        | cruza cadastros   |
|        v                                      v                   |
|  [Repositório de Skills]             [Camada de dados e ações]    |
|  (regras de leitura e validação      (ERP / WMS / cadastro de     |
|   por tipo de documento)              fornecedores e pedidos)     |
|        |                                                          |
|        v                                                          |
|  3. Validação determinística (CNPJ, soma, pedido, alçada,         |
|     grau de confiança; escalona modelo mais forte se ambíguo)     |
+------------------------|------------------------|-----------------+
                         |                        |
        dados batem +    |                        | divergência de valor,
        alta confiança   |                        | item ou baixa confiança
                         v                        v
            [Lançamento automático       [Human-in-the-loop]
             no ERP / Financeiro]        (fila de exceções: analista
                                          confere apenas os 10% a 20%
                                          com divergência, lado a lado
                                          com o documento original)
```

---

## Arquitetura passo a passo (conectada aos conceitos da Parte 2)

### 1. Captura automática e pipeline previsível em background
- **Como funciona:** sempre que chega um documento (por e-mail, portal de fornecedor, pasta compartilhada ou canal operacional), uma aplicação em nuvem captura o arquivo automaticamente, identifica qual tipo de documento é (ordem de compra, nota de serviço, comprovante de entrega, medição) e inicia um fluxo fixo de leitura e validação.
- **Por que não usar agente autônomo aqui:** um processo de entrada fiscal ou operacional precisa ser previsível, rápido, barato e auditável. Um fluxo determinístico com etapas bem definidas entrega muito mais estabilidade e menor custo do que um agente decidindo sozinho o que fazer a cada documento.
- **Conceitos da Parte 2:**
  - **Superfície de entrega (onde a IA vive na empresa):** roda em uma **camada de aplicação customizada na nuvem da própria empresa**, operando silenciosamente em background conectada aos canais de entrada e ao ERP (sem criar uma tela de chat extra para a equipe).
  - **One-off LLM call vs Workflow vs Agente:** exemplo puro de **Workflow** estruturado combinado com **One-off LLM calls** especializadas por etapa (classificar -> extrair -> conferir), dispensando agente autônomo.

### 2. Extração controlada para integração direta (Saída estruturada)
- **Como funciona:** o trabalho da IA termina no ponto certo: ler layouts variados, cabeçalhos diferentes e textos soltos e devolver um conjunto fixo de campos padronizados (emissor, CNPJ, número do pedido, itens, quantidades, valores, vencimento, observações e nível de confiança por campo).
- **Onde entra a precisão determinística:** assim que os campos saem estruturados, regras tradicionais de software conferem automaticamente se a soma dos itens bate com o total, se o CNPJ existe no cadastro, se o valor corresponde ao pedido de compra no ERP e se está dentro da tolerância permitida. A IA lê o caos; código determinístico valida a conta.
- **Conceito da Parte 2:** **Saída estruturada (Structured Outputs)** como **protagonista absoluto** do padrão, garantindo controle rigoroso de formato para movimentar automaticamente os sistemas transacionais da empresa.

### 3. Regras por tipo de documento, conexão com o ERP e Harness enxuto
- **Como funciona:** cada tipo de documento da empresa tem suas particularidades (como interpretar retenção de imposto em nota de prefeitura, onde achar código do cliente numa ordem de compra, quais campos são obrigatórios em um romaneio). Essas instruções ficam centralizadas e versionadas, e o pipeline consulta o ERP em tempo real para cruzar o documento contra pedidos e cadastros existentes.
- **Ambiente de execução controlado:** o harness próprio define um System Prompt estritamente extrativo (nunca preencher campo por suposição; se estiver ilegível ou ausente, marcar como nulo/baixa confiança), um Toolset enxuto para consultar cadastros/pedidos e registrar lançamentos permitidos, e memória/estado do lote processado para evitar duplicidade de lançamento e manter trilha de auditoria.
- **Conceitos da Parte 2:**
  - **Skills:** regras de leitura, normalização e critérios de exceção por tipo de documento registradas como ativo reutilizável e atualizadas pelo time financeiro/operacional quando muda uma regra ou entra um fornecedor/layout novo.
  - **Camada de dados e ações:** conexão via **MCP / Tools** ao ERP, WMS ou banco cadastral para cruzar o documento extraído contra dados reais da empresa antes de liberar o lançamento (com eventual **RAG** apenas se houver catálogos enormes de códigos/produtos para mapear itens).
  - **Anatomia de agente, Harness e Memória/Estado:** harness customizado minimalista focado em extração fiel, prevenção de duplicidade e rastreabilidade por documento.

### 4. Human-in-the-loop por exceção
- **Como funciona:** em vez de obrigar um analista a conferir 100% dos documentos na mão, os documentos limpos, consistentes com o ERP e com alta confiança (tipicamente a grande maioria do volume) seguem automaticamente para lançamento. Somente as exceções (valor divergente do pedido, CNPJ novo, documento cortado/ilegível, imposto inesperado ou baixa confiança em algum campo) caem em uma **fila humana de validação**, já com os campos preenchidos e o documento original ao lado para correção e aprovação em segundos.
- **Conceito da Parte 2:** **Human-in-the-loop** operando no modelo de **gestão por exceção**, garantindo segurança contábil e operacional enquanto libera o time da digitação repetitiva.

### 5. Economia em alto volume e verificação objetiva de acurácia
- **Model Routing guiado por confiança:** empresas médias processam milhares de documentos por mês. O pipeline usa modelos rápidos e baratos para classificar e extrair documentos limpos e padronizados, e aciona um modelo mais capaz apenas quando o documento está muito bagunçado, escaneado em baixa qualidade ou retorna baixa confiança na primeira passagem.
- **Medição exata de desempenho:** neste padrão, medir qualidade é simples e inquestionável. O time separa uma amostra real de documentos já lançados corretamente no passado e mede a taxa de acerto campo a campo (valor, data, CNPJ, itens) sempre que ajusta uma skill ou troca o modelo.
- **Conceitos da Parte 2:** **Roteamento de modelos (Model Routing)** e **Evals (verificação de resposta)**.

---

## Resumo do mapeamento com os conceitos da Parte 2

| Conceito (Parte 2) | Como aparece neste padrão |
| --- | --- |
| **One-off LLM call vs Workflow vs Agente** | **Workflow previsível + One-off LLM calls** por etapa (classificação e extração), sem necessidade de agente autônomo. |
| **Anatomia de agente, Harness e Memória/Estado** | **Harness customizado** enxuto e rigoroso (proibido chutar campo faltante), Toolset de consulta/lançamento no ERP e estado controlando duplicidades e trilha do documento. |
| **Evals (verificação de resposta)** | Medição objetiva campo a campo sobre uma amostra real de documentos históricos já lançados para validar cada mudança de skill ou modelo. |
| **Saída estruturada (Structured Outputs)** | **Protagonista do padrão:** transforma documentos caóticos em campos padronizados prontos para validação determinística e lançamento no ERP. |
| **Human-in-the-loop** | **Validação por exceção:** documentos limpos passam direto; apenas divergências ou baixa confiança caem na fila humana com o original lado a lado. |
| **Skills** | Regras de extração, normalização e critérios de conferência por tipo de documento, mantidas pelo time operacional/financeiro. |
| **Camada de dados e ações** | Conexão via **MCP / Tools** ao ERP/WMS/financeiro para cruzar pedido, fornecedor e cadastro antes de lançar (e **RAG** opcional para de-para de grandes catálogos de produtos). |
| **Superfície de entrega (onde a IA vive na empresa)** | **Camada de aplicação customizada na nuvem da própria empresa**, operando em background integrada à entrada de documentos e ao ERP. |
| **Roteamento de modelos (Model Routing)** | Modelos rápidos e baratos para o grosso do volume de documentos limpos; modelos mais capazes acionados apenas em documentos difíceis ou de baixa confiança. |
| **Governança e centralização (transversal)** | Regras de lançamento únicas, checagem determinística antes de gravar no ERP, fila auditável de exceções e trilha completa ligando cada lançamento ao documento original. |

---

## Conexão com os Princípios básicos (Parte 1)

- **Princípio 1 (Natureza probabilística da IA):** divisão exemplar entre probabilístico e determinístico. A IA faz apenas o que código tradicional não consegue bem (ler layouts imprevisíveis e extrair campos); o software determinístico faz toda a conferência matemática, fiscal e de cadastro.
- **Princípio 2 (Engenharia de contexto):** a precisão não vem de um prompt genérico de "leia esse PDF", e sim das skills por tipo de documento e do cruzamento com cadastros e pedidos reais do ERP.
- **Princípio 3 (A IA é uma ferramenta, não um objetivo final):** ataca diretamente custo operacional de backoffice, velocidade de faturamento/recebimento e redução de erro humano de digitação no core operacional.
