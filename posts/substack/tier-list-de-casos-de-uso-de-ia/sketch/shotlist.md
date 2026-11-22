# Shot list: IA no trabalho de especialistas

Revisão editorial `v4.md` aprovada pelo usuário e copiada para `../final.md`, substituindo a versão anterior. Capa e duas figuras conceituais produzidas no sistema Alvinegro, com fontes locais, e verificadas visualmente inclusive a 50% da largura. A revisão mantém as artes e suas legendas. Publicação manual no Substack.

## Artes entregues

| # | Âncora no texto | O que mostra | Fonte e arquivo | Status |
|---|---|---|---|---|
| cover | Título do artigo | Dados, especialista e entrega | Autoral, `sketch/figures.html#cover`; `cover.png` | Renderizada e conferida |
| 01 | “Essa combinação permite reaproveitar uma mesma estrutura técnica de IA em diferentes serviços, desde que os dados e o método de cada negócio estejam bem definidos.” | Dados de entrada, trabalho do especialista e entrega, com contexto, conhecimento e método | Autoral, `sketch/figures.html#figure01`; `01.png` | Renderizada e conferida |
| 02 | “A cada novo cliente, o time reaproveita essa estrutura e trabalha sobre o contexto específico daquela entrega.” | Dados organizados acessíveis por MCP, método orientando a IA e revisão pelo especialista | Autoral, `sketch/figures.html#figure02`; `02.png` | Renderizada e conferida |

Os PNGs têm 2000 px de largura. Capa: 2000 × 1000; figura 01: 2000 × 1100; figura 02: 2000 × 1120. As fontes Bricolage Grotesque 800 e Inter foram reutilizadas de assets locais do projeto. Provas de leitura a 50% em `sketch/qa/`. Fonte técnica do trecho MCP: https://modelcontextprotocol.io/docs/learn/architecture e https://modelcontextprotocol.io/docs/learn/server-concepts.

## Sistema visual

Fonte: `design/identity.md`. Alvinegro: preto `#0A0A0A`, branco `#FFFFFF`, Bricolage Grotesque 800 nos títulos e Inter nos rótulos. SVG geométrico, contorno irregular e halftone desregistrado. As texturas não devem prejudicar rótulos, setas ou leitura em tela pequena.

A capa é preta, perto de 2:1. Figuras internas brancas, horizontais, com hierarquia clara. Textos e medidas abaixo são especificações do plano; ajustes de composição podem preservar o mesmo significado.

## `cover.png`: IA no trabalho de especialistas

- **Formato:** 2000 × 1000 px, fundo preto; composição central legível também no recorte do Substack.
- **Título:** `IA NO TRABALHO DE ESPECIALISTAS`, com quebra entre `IA NO TRABALHO` e `DE ESPECIALISTAS`, ajustável conforme a composição.
- **Composição:** elementos geométricos representam informações à esquerda, o especialista ao centro e o trabalho concluído à direita. Manter uma direção de leitura, com o centro identificado como `ESPECIALISTA`.
- **Rótulos:** `DADOS` e `ENTREGA`. A capa apresenta o assunto sem acrescentar MCP nem uma frase de efeito.
- **Função:** representar a tese do artigo sem repetir o diagrama didático completo da primeira figura.

## `01.png`: o trabalho do especialista

- **Formato:** 2000 × 1100 px, fundo branco.
- **Título:** `O TRABALHO DO ESPECIALISTA`.
- **Fluxo principal horizontal:** `DADOS DE ENTRADA` → `TRABALHO DO ESPECIALISTA` → `ENTREGA AO CLIENTE`.
- **Rótulos secundários:** na entrada, `documentos e registros`; no especialista, `analisar o caso e aplicar critérios`; na entrega, `relatório · análise · recomendação · plano`.
- **Três insumos distintos ao núcleo central:** `CONTEXTO`, `CONHECIMENTO` e `MÉTODO`. Podem ficar como blocos acima do núcleo, cada um com uma ligação explícita ao trabalho do especialista. Não apresentar método como etapa posterior à entrega.
- **Limite da representação:** retrata uma abstração aplicável a muitas empresas de serviços, sem afirmar que explica toda empresa ou toda entrega.
- **Ponto de inserção:** depois de explicar o trabalho do especialista, aproximadamente no primeiro terço do texto.
- **Legenda proposta:** `O profissional analisa as informações e aplica seu conhecimento e método para produzir o trabalho contratado.`
- **O que explica:** a relação entre os dados recebidos, o que o especialista sabe e o trabalho que ele entrega ao cliente.

## `02.png`: dados e método no ambiente do especialista

- **Formato:** 2000 × 1120 px, fundo branco.
- **Título:** `COMO A IA PARTICIPA DO TRABALHO`.
- **Fluxo principal com cinco blocos:** `FONTES DA EMPRESA` → `DADOS ORGANIZADOS` → `MCP` → `IA DO ESPECIALISTA` → `REVISÃO E ENTREGA`.
- **Rótulos secundários:** fontes, `arquivos · sistemas · registros`; dados, `organizar · conferir · atualizar`; MCP, `consultar dados e usar ferramentas`; IA, `a que o profissional já usa`; revisão, `especialista confere e aprova`.
- **Método separado acima da IA:** bloco `MÉTODO DE TRABALHO`, com `instruções · procedimentos · exemplos aprovados` e seta entrando diretamente em `IA DO ESPECIALISTA`. Essa ligação não passa pelo bloco de dados nem exige que o método seja entregue pelo MCP.
- **Nota curta fora do fluxo:** `A equipe mantém os dados atualizados e confere o resultado.`
- **Limite da representação:** MCP é a conexão. Não desenhar um efeito automático de limpeza de dados, garantia de qualidade, aquisição de conhecimento ou eliminação da revisão humana.
- **Ponto de inserção:** depois de explicar como a IA consulta os dados e segue os procedimentos do trabalho, perto do fim do segundo terço. Manter dois ou três parágrafos entre esta figura e `01.png`.
- **Legenda proposta:** `Com os dados organizados, a IA pode consultar o que precisa e seguir os procedimentos do trabalho. O especialista confere o resultado antes de entregá-lo.`
- **O que explica:** como os dados e o método chegam à IA e em que momento o profissional confere o trabalho.

## Validação concluída

Conferidos contraste, margens, rótulos, setas e relação entre os elementos das três artes. As fontes locais carregaram corretamente no Chromium. As duas figuras estão ligadas às legendas do artigo. A documentação oficial do MCP sustenta o trecho técnico da segunda figura; os diagramas são conceituais e autorais.
