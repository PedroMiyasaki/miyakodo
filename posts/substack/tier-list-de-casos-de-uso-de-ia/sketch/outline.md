# Plano do artigo: IA no trabalho de especialistas

Status: revisão `v4.md` aprovada pelo usuário e fechada em `../final.md`, com capa e duas figuras produzidas e conferidas. O plano abaixo registra o planejamento inicial.

## Título e subtítulo propostos

**IA no trabalho de especialistas**

Como organizar as informações e orientar a IA para ajudar o profissional no trabalho que o cliente contratou.

## Recorte e tese

Artigo curto sobre o padrão do tier S da fala gravada. Não recontar a tier list nem comparar as outras categorias. Público: empresários, stakeholders e quem decide o orçamento de IA.

Em muitas empresas de serviços, o profissional precisa reunir informações, analisar um caso, aplicar critérios e entregar um trabalho ao cliente. A aposta do autor é que organizar os dados, permitir que a IA os consulte e registrar os procedimentos do especialista pode ajudar a equipe a produzir mais. O ganho é uma hipótese a avaliar na operação da empresa; depende do trabalho, dos dados e de como a IA é usada.

A explicação precisa valer para vários setores. Usar relatório, análise, recomendação ou plano como exemplos, sem enumerar profissões. Partir da rotina do profissional e explicar a tecnologia conforme ela participa do trabalho.

## Arco e tamanho

Estimativa: 700 a 850 palavras de corpo, cerca de quatro minutos de leitura. Os tamanhos abaixo orientam o ritmo; não são cotas. Duas figuras internas carregam a explicação visual, além da capa.

1. **Por onde começar** (90 a 110 palavras). Abrir com uma rotina reconhecível: reunir informações, analisar um caso, aplicar critérios e entregar um trabalho ao cliente. Mostrar por que eu considero esse uso interessante: a IA pode ajudar a fazer um trabalho pelo qual a empresa já recebe. Escrever como o autor explicaria isso numa conversa, sem resumir a abertura numa frase de efeito.

2. **O trabalho do especialista** (120 a 150 palavras). Explicar o que o profissional acrescenta às informações que recebe: contexto, conhecimento e método. Relatório, análise, recomendação ou plano bastam como exemplos. A figura `01.png` mostra a relação entre esses elementos; o texto explica por que ela interessa a quem paga pelo projeto de IA, sem narrar o desenho nem tratar o serviço como uma equação.

3. **Antes de usar a IA** (130 a 160 palavras). Mostrar o preparo necessário: reunir as informações relevantes, conferir se os registros se referem ao mesmo trabalho, corrigir inconsistências e manter os dados atualizados. A organização deve facilitar a consulta ao que o profissional precisa; reunir tudo em um único banco não é uma exigência. Explicar também quais critérios e procedimentos ele segue na análise.

4. **Consultar os dados e seguir o método** (180 a 210 palavras). Partir da IA que o profissional já usa. Introduzir MCP apenas para explicar como esse agente pode consultar os dados da empresa e usar as ferramentas que foram conectadas a ele. O preparo dos dados e as instruções de trabalho precisam ser feitos pela equipe responsável pelo projeto. Procedimentos e exemplos aprovados ajudam a orientar o agente. A figura `02.png` mostra como isso se organiza; o texto comenta as escolhas, sem repetir cada etapa do diagrama ou descrever a arquitetura do protocolo.

5. **Como avaliar se compensa** (150 a 180 palavras). Fechar com o que o empresário pode observar num trabalho recorrente: quanto tempo leva, quanto precisa ser refeito, se mantém a qualidade e se a equipe consegue atender mais clientes. O especialista confere e aprova o resultado. Organização dos dados, permissões e manutenção entram na conta. Retomar a opinião do autor sobre esse uso da IA sem prometer retorno ou inventar ganhos de produtividade. O artigo já é a continuação prometida no vídeo, portanto não precisa pedir que o leitor comente “especialista”.

## Forma editorial

- Abertura direta, em primeira pessoa quando houver julgamento do autor.
- No máximo dois intertítulos: “Antes de usar a IA” e “Como avaliar se compensa”. Os cinco movimentos acima não precisam virar cinco seções visíveis.
- Pelo menos dois ou três parágrafos entre as duas figuras. A leitura deve fazer sentido com e sem elas.
- Figuras conceituais autorais em preto e branco, no sistema Alvinegro de `design/identity.md`. A preferência explícita do usuário substitui a exigência de capturas reais do Passo 7a.
- Não apresentar MCP como garantia de qualidade, segurança, produtividade ou autonomia. O acesso depende das permissões e da implementação. Não afirmar que toda empresa de serviços cabe nessa abstração.
- Ler o texto como fala em português brasileiro. Preferir ações concretas a slogans, abstrações e nomes de arquitetura. Sem emojis, sem em dash, sem fórmulas de contraste e sem repetir a ideia de “transformar informação em informação”.

## Base e calibração

Fonte principal: [`posts/script/tier-list-de-casos-de-uso-de-ia/sketch/v2.md`](../../../script/tier-list-de-casos-de-uso-de-ia/sketch/v2.md), baseada no vídeo `video/inputs/tier_list/tier_list.MP4`. A fala gravada e a conversa prevalecem sobre a v1.

Ideia de origem lida no Notion: [Tier list de casos de uso de IA](https://app.notion.com/p/3f4ffe7442fd81188cebe721291c6881?pvs=204). A nota original menciona dados preparados, MCP e práticas compartilhadas pelo time; o artigo concentra esses elementos no trabalho do especialista.

Calibração pelos três slugs de Substack existentes: `ia-torna-dados-juridicos-estruturaveis-a-area-vai-ser-disruptada` (v1), `gpt-6-is-great-not-as-good-as-they-said` (v3) e `a-enter-e-a-tese-ai-as-a-service-da-sequoia` (v3). Manter raciocínio contínuo, opinião com premissas explícitas, referências junto à afirmação e legendas que acrescentem leitura. Adaptar a extensão e os visuais ao pedido atual, sem reproduzir as tabelas, a densidade de notícias ou o recorte jurídico desses artigos.

Fontes primárias consultadas para as afirmações técnicas:

- [MCP, Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture): arquitetura entre aplicativo e servidores, recursos, ferramentas e limites do protocolo quanto ao uso do modelo e à gestão do contexto.
- [MCP, Server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts): recursos como contexto e ferramentas como operações expostas ao aplicativo. Sustenta o funcionamento mostrado na segunda figura, não a tese de retorno financeiro.
- [MCP, Security best practices](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices): permissões e controles precisam fazer parte da implementação. Usar apenas se houver afirmação correspondente no corpo; não transformar o artigo em checklist de segurança.

Não foram buscados relatórios de ROI. Não haverá números de mercado ou ganhos percentuais para sustentar uma opinião sobre o padrão.

## Próxima revisão

Revisar `sketch/v1.md` com o usuário e travar o texto antes de produzir as figuras. O artigo permanece como rascunho; não criar `final.md`, publicar nem atualizar o Notion.
