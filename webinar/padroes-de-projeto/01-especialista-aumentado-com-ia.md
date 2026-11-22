# Padrão de projeto 1: Especialista aumentado com IA

## Objetivo de negócio

Aumentar o ritmo de produção e a capacidade de entrega de um profissional especialista dentro da empresa, sem tentar substituí-lo por um agente autônomo.

Esse padrão resolve o caso típico de serviços e áreas especializadas (engenharia, jurídico, logística, medicina, consultoria, finanças, operações técnicas) em que o trabalho segue a estrutura **dados -> especialista -> saída**. Em vez de obrigar a IA a acertar todas as exceções e regras de bolso sozinha, o padrão equipa o especialista com dados organizados, método padronizado e uma IA operando como copiloto sob validação humana.

---

## Visão geral do fluxo

```text
[Fontes brutas da empresa]
          |
          v
[Camada de pré-processamento]
          |
          v
[Camada centralizada de dados]  (Database vetorial / RAG  OU  Pastas compartilháveis: OneDrive, SharePoint)
          |
          |  MCP interno (RAG)  ou  MCP nativo / Tools (pastas)
          v
+-------------------------------------------------------------+
|  AMBIENTE DO ESPECIALISTA (Claude, Codex, Cursor etc.)      |
|                                                             |
|  Especialista (opera, revisa, aprova)  <-->  IA (copiloto)  |
|                                                ^            |
+------------------------------------------------|------------+
                                                 |  usa
                                                 |
[Especialistas de validação] --(escrevem e validam)--> [Repositório centralizado de Skills]
                                                       (regras, métodos, resources | pasta governada, GitHub ou solução customizada)
          |
          v
[Saída(s) aprovada(s)]  (um tipo específico ou vários tipos de entrega)
```

---

## Arquitetura passo a passo (conectada aos conceitos da Parte 2)

### 1. Pré-processamento e camada centralizada de dados
- **Como funciona:** uma camada de pré-processamento coleta dados brutos e desorganizados que hoje estão espalhados por várias fontes da empresa (ERPs, planilhas, PDFs, e-mails, registros de sistemas) e consolida esse material em uma camada centralizada, estruturada e compartilhável.
- **Dois caminhos de implementação conforme a complexidade da empresa:**
  - **Base vetorial (RAG):** indicada quando há volumes grandes ou documentos extensos que precisam ser indexados e recuperados por busca estruturada/semântica.
  - **Navegação de pastas compartilháveis:** caminho mais simples e direto, organizando documentos e registros em uma estrutura limpa no OneDrive, SharePoint ou ferramenta equivalente, acessível por natureza para toda a empresa.
- **Conceito da Parte 2:** **Camada de dados e ações** (decidindo entre **RAG** para grandes volumes de documentos, **MCP** para conexão padronizada e **Tools** para navegação mais simples) e o fio condutor transversal de **governança e centralização** (permissões, versão única da verdade e fim dos arquivos soltos no computador de cada funcionário).

### 2. Conexão da IA do especialista com os dados
- **Como funciona:** o especialista usa uma IA no dia a dia (como Claude, Codex, Cursor ou equivalente) conectada diretamente à camada centralizada de dados da empresa, sem precisar ficar copiando e colando arquivos manualmente em chats soltos.
- **Como essa conexão acontece em cada caminho:**
  - Quando a empresa usa uma camada de **RAG / database vetorial**, a IA do especialista se conecta por meio de um **MCP interno** desenvolvido ou mantido pela empresa.
  - Quando a empresa usa a estrutura mais simples de **OneDrive ou SharePoint**, a IA se conecta por meio do **MCP nativo** dessas plataformas (ou via **Tools** de navegação de arquivos, conforme o ambiente).
- **Conceitos da Parte 2:** **Camada de dados e ações** (MCP interno, MCP nativo e Tools) e **Anatomia de agente, Harness e Memória/Estado** (as conexões entram como tools do agente e abastecem o contexto e o estado do caso atual).

### 3. Ambiente de operação do especialista (Harness e Superfície de entrega)
- **Como funciona:** o especialista interage com a IA diretamente na ferramenta que roda no seu ambiente de trabalho (Claude, Codex, Cursor ou similar), operando um **agente assistido** capaz de consultar a camada de dados, acionar skills e produzir rascunhos, análises e artefatos completos.
- **Por que começar por aqui:** usar um harness pronto acelera muito a adoção e reduz custo de engenharia, já que a empresa não precisa construir interface nem orquestração própria do zero. Em contrapartida, abre-se mão de controle fino sobre o harness.
- **Conceitos da Parte 2:**
  - **Superfície de entrega (onde a IA vive na empresa):** neste padrão, a IA vive principalmente **na máquina de cada funcionário** (instalação local de Codex, Claude, Cursor etc.), podendo também operar em **assinaturas Enterprise** (como ChatGPT Enterprise ou Gemini Enterprise) quando a empresa quer uma camada administrativa adicional de governança e controle de acesso sem construir software próprio.
  - **Anatomia de agente, Harness e Memória/Estado:** uso de um harness pronto (trade-off entre velocidade/custo e controle), com system prompt, tools conectadas aos dados e memória/estado ancorados na sessão e nos arquivos do caso.
  - **One-off LLM call vs Workflow vs Agente:** sai do uso solto de chamadas pontuais (one-off) para um **agente assistido** operando sobre workflows e métodos codificados, sem pular para um agente totalmente autônomo fora de controle.
  - **Roteamento de modelos (Model Routing):** quando operado em superfícies agnósticas (como Cursor ou integrações via OpenRouter), o especialista ou o time pode usar modelos mais rápidos e baratos para leituras, extrações e formatações rotineiras e modelos mais capazes para análises e decisões complexas.

### 4. Repositório centralizado de skills e governança de método
- **Como funciona:** a IA do especialista conversa com um **repositório centralizado de skills**, que concentra o jeito de trabalhar da empresa: instruções passo a passo, regras de negócio, critérios de qualidade, formatos esperados e resources de apoio.
- **Onde esse repositório pode viver:**
  - Uma solução customizada interna.
  - Uma pasta compartilhada com governança e controle de acesso (ex.: SharePoint / OneDrive).
  - Um repositório no **GitHub** (trazendo versionamento, histórico de alterações e fluxo formal de revisão).
- **Separação de papéis (governança viva):**
  - **Especialistas de validação:** escrevem, revisam, validam e versionam as skills oficiais do repositório.
  - **Especialistas da operação:** consomem e operam essas skills no dia a dia junto com a camada de dados para gerar as entregas, sem precisar reinventar prompts nem depender da TI toda vez que uma política ou critério muda.
- **Conceitos da Parte 2:** **Skills** (métodos repetidos viram ativo centralizado e reutilizável da empresa, análogo a funções em programação), **Evals (verificação de resposta)** (especialistas de validação podem testar alterações nas skills em casos reais anteriores para garantir que mudanças melhorem as entregas de fato) e o fio transversal de **governança e centralização**.

### 5. Operação humana e geração de saídas
- **Como funciona:** combinando os dados lidos da camada centralizada com as skills, regras e resources do repositório, o especialista usa a IA para produzir **tanto um único tipo de saída recorrente quanto vários tipos de saída** (por exemplo: relatório técnico, parecer jurídico, análise de logística, proposta comercial, diagnóstico operacional ou documento estruturado).
- **Papel central do humano:** o especialista não é um espectador passivo. Ele direciona o caso, julga exceções que não cabem em regra escrita, confere se a IA respeitou os dados e as fontes, corrige desvios e assina a entrega final.
- **Integração com o resto da empresa:** quando a saída precisa não apenas ser lida por uma pessoa, mas também alimentar sistemas internos (atualizar ERP, CRM, planilha de controle ou disparar outra etapa automática), o formato da entrega é restringido e padronizado.
- **Conceitos da Parte 2:**
  - **Human-in-the-loop:** é o **coração** deste padrão. Atua em dois níveis: na operação diária (o especialista conduz, valida e aprova cada entrega) e na governança do método (especialistas de validação escrevem e aprovam as skills do repositório).
  - **Saída estruturada (Structured Outputs):** aplicada sempre que uma ou mais saídas do especialista precisarem seguir um esquema fixo para integração automática em sistemas determinísticos da empresa.

---

## Resumo do mapeamento com os conceitos da Parte 2

| Conceito (Parte 2) | Como aparece neste padrão |
| --- | --- |
| **One-off LLM call vs Workflow vs Agente** | Opera como **Agente assistido** (copiloto) apoiado em workflows registrados em skills; evita tanto chamadas soltas sem padrão quanto agentes autônomos sem supervisão. |
| **Anatomia de agente, Harness e Memória/Estado** | Usa **harness pronto** (Claude, Codex, Cursor): alta velocidade de implantação com menor controle fino do harness; tools conectam dados e skills, e o estado do caso mora na sessão e nos arquivos. |
| **Evals (verificação de resposta)** | Usado pelos especialistas de validação para checar se novas skills ou ajustes de regras melhoram as entregas em casos reais antes de liberar para o time. |
| **Saída estruturada (Structured Outputs)** | Aplicada quando as saídas geradas pelo especialista (uma ou várias) precisam alimentar automaticamente sistemas determinísticos (ERP, CRM, bancos). |
| **Human-in-the-loop** | **Coração do padrão.** Presente na revisão e aprovação das entregas pelo especialista e na escrita/validação das skills no repositório central. |
| **Skills** | **Repositório centralizado de skills** (pasta governada, GitHub ou solução customizada) contendo métodos, regras e resources escritos por validadores e operados pelo time. |
| **Camada de dados e ações** | Pré-processamento de fontes brutas em camada centralizada (**RAG / base vetorial** via **MCP interno**, ou **pastas no OneDrive/SharePoint** via **MCP nativo / Tools**). |
| **Superfície de entrega (onde a IA vive na empresa)** | Principalmente **na máquina de cada funcionário** (Claude, Codex, Cursor), com caminho natural para **assinaturas Enterprise** (ChatGPT/Gemini Enterprise) conforme a necessidade de governança. |
| **Roteamento de modelos (Model Routing)** | Escolha de modelos mais baratos/rápidos para etapas simples e mais capazes para análises complexas (quando em superfícies ou provedores agnósticos como Cursor / OpenRouter). |
| **Governança e centralização (transversal)** | Nasce da junção entre camada de dados centralizada, repositório versionado de skills, validação humana em dois níveis e superfície controlada. |

---

## Conexão com os Princípios básicos (Parte 1)

- **Princípio 1 (Natureza probabilística da IA):** a IA atua onde há leitura, cruzamento e síntese probabilística; o especialista (e eventual saída estruturada ligada a sistemas determinísticos) segura precisão, exceções e responsabilidade final.
- **Princípio 2 (Engenharia de contexto):** todo o desenho (pré-processamento, camada de dados, MCP e repositório de skills) existe para entregar o contexto exato da empresa à IA sem depender de prompts manuais improvisados.
- **Princípio 3 (A IA é uma ferramenta, não um objetivo final):** o padrão só gera retorno quando aplicado a um trabalho de especialista diretamente ligado ao core business e ao ritmo de entrega que traz receita ou margem.
