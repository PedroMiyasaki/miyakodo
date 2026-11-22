---
slug: 5-conceitos-de-ia-que-empreendedores-precisam-conhecer
entrada: https://app.notion.com/p/3fcffe7442fd81fa8bb2f8290b77bd7e
modo: lista-com-gancho
versao: v4
status: aprovado
etapa: arquivado-em-posts
estrutura_textual: v2-aprovada
gancho: video/hooks/cafe_cortado.mp4
duracao_original: 5
duracao_prevista: 37
---

## Pedido do usuário

> Agora eu quero que você utilize a skill de edição de vídeo no modo de edição lista com gancho nessa ideia que acabamos de registrar. E já deixo claro que... o conteúdo que nós vamos enviar para as pessoas... que comentarem a palavra do CTA final é esse aqui: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

### Revisão v2

> Certo, vamos trocar o nome do primeiro pra... tipos de arquitetura de sistemas de IA. Vamos trocar o segundo pra engenharia de contexto, e aí entre parênteses escrito context engineering. Sobre o quarto onde tá escrito LLM ops, eu queria AI ops. E aí, como saber a hora de trocar de modelo? E vamos trocar o CTA? Pra uma palavra chave "RECURSOS" E aí, na verdade, eu... a pessoa tem que comentar recursos pra eu enviar os artigos sobre todos os assuntos pra ela. Um dos artigos a gente já sabe, já tem a referência, mas aí eu vou precisar que você pesquise os artigos para os outros assuntos, mas deve ser fácil de achar um artigo oficial da Anthropic ou da OpenAI pra cada um desses itens, mas faz isso só depois. Agora foca em refazer essa estruturazinha aí com essas mudanças que eu pedi.

### Aprovação da estrutura textual

> De acordo, pode fazer

Aprovação recebida em 2026-10-17: autoriza a criação dos banners e do plano visual a partir da v2. Não é aprovação do plano visual ainda não apresentado nem autorização de render final.

### Revisão visual v4

> Na verdade, as imagens de cada um dos banners devem ocupar como se fosse um overlay, onde o fundo é branco e todas essas caixas com flechas e explicações técnicas ficam no preto. Numa ideia de que o título de cima faz referência a uma imagem como se ela fosse um overlay embaixo, como se ela viesse de um lugar diferente, um artigo, alguma coisa do tipo explicando, mesmo que seja uma imagem que você vai fazer, e aí embaixo uma legenda sobre essa imagem. Mude todos os banners pra que eles fiquem com esse aspecto.

Interpretação aplicada: manter o fundo externo da cena preto; separar título acima, painel-imagem branco independente no meio com diagramas/textos técnicos pretos, e legenda fora do painel abaixo. Manter textos e tempos da v2. Somente os cinco banners mudam.


### Respostas de 2026-10-17

- Gancho: sem fala (confirmado pelo usuário).
- Visual v4: aprovado para a montagem final, sem render.
- Som do gancho: sem som na versão final.
- Render: qualidade looks escolhida. Aguardando "pronto" ou "pode renderizar" para renderizar.

## Fonte

Ideia: [5 conceitos de IA que empreendedores precisam conhecer](https://app.notion.com/p/3fcffe7442fd81fa8bb2f8290b77bd7e).

Preservar os cinco itens e sua ordem. Evals deve aparecer explicitamente como o conceito mais importante. Notion consultado somente para leitura, sem alteração de Status ou Format.

## Comportamentos padrão

- Modo: Lista com gancho, vertical 1080 × 1920.
- Abertura: arquivo sorteado com secrets.choice entre os seis MP4 da raiz de video/hooks/. Resultado: cafe_cortado.mp4. Duração confirmada por ffprobe: 5 s; origem 2160 × 3840.
- Fala do gancho: não há, confirmado pelo usuário em 2026-10-17. A transcrição de teste falhou nesta máquina (motor de transcrição indisponível), então a informação vem do usuário, não de verificação técnica. Por isso, legenda-evals e corte de espaço morto de fala não se aplicam ao take 1.
- Áudio do gancho: sem som na versão final, decisão do usuário em 2026-10-17. A cópia assets/gancho-sdr.mp4 não tem faixa de áudio. O original tem som contínuo (média -32,1 dB), que não entra na edição.
- Textos deste modo: overlays próprios, não legenda-evals.
- Perfil-pb: desligado.
- Aviso-2x: desligado.
- Estrutura textual v2 aprovada. Banners e capturas estáticas gerados nas versões v3 e v4. Composição em plano/index.html usada somente para as capturas. A montagem final está na raiz do projeto (index.html), com o vídeo real na abertura. Nenhum MP4 renderizado.
- O take de abertura é HDR HLG/BT.2020. O frame de referência foi convertido tecnicamente para SDR/BT.709 para revisão junto dos banners alvinegros. A montagem usa assets/gancho-sdr.mp4 (SDR/BT.709, 1080 × 1920, sem áudio). O original não foi alterado.
- A identidade alvinegra é aplicada sem handle nem logotipo: o modo mantém perfil-pb desligado. Fundo #0A0A0A, texto branco, fontes locais Bricolage Grotesque e Inter, contornos com wobble e preenchimento em retícula deslocada, conforme design/proof/proof.html e design/templates/slides.html.

## Decisões e intenção

- Categoria das legendas dos banners: decisões de negócio que cada conceito ajuda a tomar. Cada legenda será uma pergunta curta, não uma repetição do nome técnico.
- A futura imagem de cada banner carrega a explicação do conceito. Fundo preto #0A0A0A, identidade do projeto, Bricolage Grotesque e Inter, a detalhar somente na etapa visual.
- Primeiro item: Tipos de arquitetura de sistemas de IA, conforme revisão do usuário. A futura imagem deve distinguir chamada isolada de LLM, workflow com sequência definida, agente que escolhe próximos passos/ferramentas e sistema multiagente. Não apresentar esses arranjos como uma escada de qualidade.
- Engenharia de contexto (context engineering): a futura imagem deve explicar a preparação e seleção de instruções, informações, histórico e ferramentas disponíveis ao modelo.
- Injeção de dependências: a futura imagem deve explicar o fornecimento de recursos e contexto de execução ao agente, como identidade, clientes e ferramentas com escopo. Não afirmar que injeção de dependências, sozinha, garante autorização ou governança.
- Quarto item: AI Ops, conforme nome solicitado pelo usuário, com a legenda "Como saber a hora de trocar de modelo?". Preservar o sentido de avaliar a hora de trocar modelos conforme o mercado evolui, sem substituir novamente o nome por LLMOps. Não altera a ideia no Notion.
- Evals fecha a lista com a marcação explícita "o mais importante". A futura imagem deve ligar casos reais, critérios de sucesso e comparação antes/depois.
- Palavra-chave: RECURSOS, definida pelo usuário em substituição a CRITERIO. Verificação local: os respostas-comentarios.md existentes registram apenas "especialista" (tier-list-de-casos-de-uso-de-ia) e "evals" (se-voce-desenvolve-qualquer-projeto-de-ia-precisa-de-evals). RECURSOS não aparece nos registros locais. A conta do Instagram não foi consultada, então ainda não há garantia de que a palavra esteja livre.
- Recursos do CTA: artigos sobre os cinco assuntos, não apenas Evals. Um artigo por item, buscando fontes oficiais da Anthropic ou OpenAI. O artigo de Evals já foi informado; os demais serão pesquisados depois, por orientação explícita do usuário. Não pesquisar nesta revisão e não prometer material autoral ou tradução.

## Cortes propostos

- Gancho: manter origem 00:00–00:05, mapeada para edição 00:00–00:05. Tempo removido: 0 s. Não repetir nem esticar.
- Demais takes: telas próprias. Durações provisórias para leitura das legendas e das futuras imagens, a conferir no plano visual.

## Estrutura textual v2

### Take 1 · 00:00–00:05 · 5 s · vídeo de gancho

Arquivo: video/hooks/cafe_cortado.mp4.

Legenda: "5 conceitos de IA que todo empreendedor precisa conhecer. O último é o mais importante."

### Take 2 · 00:05–00:12 · 7 s · banner

Item: 1. Tipos de arquitetura de sistemas de IA.

Legenda: "Você precisa de um agente ou de um fluxo bem definido?"

### Take 3 · 00:12–00:17 · 5 s · banner

Item: 2. Engenharia de contexto (context engineering).

Legenda: "Sua IA recebe o que precisa para decidir?"

### Take 4 · 00:17–00:22 · 5 s · banner

Item: 3. Injeção de dependências em agentes.

Legenda: "O agente pode acessar o quê, em nome de quem?"

### Take 5 · 00:22–00:27 · 5 s · banner

Item: 4. AI Ops.

Legenda: "Como saber a hora de trocar de modelo?"

### Take 6 · 00:27–00:33 · 6 s · banner

Item: 5. Evals: o mais importante.

Legenda: "A mudança melhorou ou só parece que melhorou?"

### Take 7 · 00:33–00:37 · 4 s · CTA

Fundo preto, sem imagem. Três linhas:

comenta:
"RECURSOS"
Te envio os artigos sobre esses 5 conceitos.

## Plano visual v4

Textos e durações da v2 preservados. Canvas 1080 × 1920. Prévias de cada take: 540 × 960. Cinco banners em resolução integral em assets/, com o painel branco também isolado em assets/*-overlay.png.

- 00:00–00:05 · Gancho · captura plano/01-gancho.png. Frame real em 1,5 s de cafe_cortado.mp4, com título em bloco preto e chamada do último conceito. Na montagem final, o vídeo real (cópia SDR) ocupa os 5 s, sem repetição.
- 00:05–00:12 · Tipos de arquitetura · captura plano/02-arquiteturas.png; banner assets/02-arquiteturas.png. Quatro linhas: chamada isolada entrada/LLM/saída, workflow ler/checar/enviar, agente em loop com ferramentas e coordenação de dois agentes. Tipos apresentados sem hierarquia de qualidade.
- 00:12–00:17 · Engenharia de contexto · captura plano/03-contexto.png; banner assets/03-contexto.png. Instruções, dados, histórico e ferramentas convergem para seleção do que importa e contexto entregue ao modelo.
- 00:17–00:22 · Injeção de dependências · captura plano/04-dependencias.png; banner assets/04-dependencias.png. Identidade do usuário, cliente de API e ferramentas com escopo são fornecidos pela aplicação ao agente. Serviços continuam responsáveis por validar permissões.
- 00:22–00:27 · AI Ops · captura plano/05-ai-ops.png; banner assets/05-ai-ops.png. Modelos atual/novo passam pelos mesmos casos reais; qualidade, custo e latência orientam uma troca gradual com possibilidade de voltar. Sem números de desempenho inventados.
- 00:27–00:33 · Evals: o mais importante · captura plano/06-evals.png; banner assets/06-evals.png. Mesmos casos reais e critérios de sucesso antes/depois para comparar e detectar regressões. O diagrama não traz números nem resultados de benchmark.
- 00:33–00:37 · CTA · captura plano/07-cta.png. Somente três blocos de texto sobre preto, sem imagem: comenta:, "RECURSOS" e a entrega de artigos dos cinco conceitos.

Visão geral: plano/sequencia.png. Fonte editável para capturas: plano/index.html. Script mecânico de preparação e exportação: preparar-previa.py. A montagem final está em index.html, na raiz do projeto.

Layout dos banners: fundo preto; título a partir de y=260; painel branco de 920 × 876 px em x=80, y=570, com diagrama em preto; legenda em y=1476, abaixo do painel. Gancho e CTA sem mudança de layout. Os textos de título e legenda seguem a v2. Dentro dos diagramas, alguns rótulos foram reescritos para caber nas caixas (por exemplo, "Antes da mudança" e "com possibilidade de voltar"). Dois são novos: "repete até concluir" (arquiteturas) e "dentro do limite de tokens" (contexto).

## Recurso e resposta automática

- Palavra-chave definida: RECURSOS.
- Entrega: artigos sobre todos os cinco assuntos.
- Artigo de Evals já informado: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Título verificado: Demystifying evals for AI agents. Idioma: inglês.
- Artigos dos outros quatro assuntos: pendentes de pesquisa posterior, preferindo um artigo oficial da Anthropic ou OpenAI por item. Não pesquisar agora.
- Não é necessário perguntar novamente o escopo dos recursos nem o link de Evals.
- Cadastro de resposta automática somente na etapa correspondente, com a skill registrar-resposta-automatica. Exige link do post do Instagram e pasta de peça existente em posts/, ainda não informados, além dos links dos demais artigos. Não criar cadastro, inventar link nem executar atendimentos agora.

## Pendências e dúvidas

- Visual v4 aprovado e renderizado em qualidade looks. A pedido do usuário, o Reel final foi movido para `posts/script/5-conceitos-de-ia-que-empreendedores-precisam-conhecer/reels.mp4` para indicar que está postado.
- Em etapa posterior: pesquisar e verificar os artigos oficiais dos quatro assuntos ainda sem referência, conforme pedido do usuário. Nenhuma pesquisa de artigos adicionais nesta etapa.
- Montagem final feita e validada (ver Histórico, v4 · montagem). Ajustar tempos de leitura se a revisão visual do usuário pedir.
- Render somente após "pronto" ou "pode renderizar".

## Conferência da prévia

- HyperFrames 0.8.169: check executado nos tempos 2, 8.5, 14.5, 19.5, 24.5, 30 e 35 s. Na revisão v4: ok, 0 erros; contraste 46/46.
- O check mantém oito avisos de organização: sete takes no mesmo arquivo estático e recomendação de cenas em subcomposições. Aceitos somente na fonte de capturas; a composição final terá cenas separadas. Avisos restantes, sem erros: 8 de lint (estrutura de sub-composições, aceitos para esta prévia), 13 de layout (conectores de SVG) e 4 informativos. Medi por script: as pontas das setas tocam as caixas, exceto nas saídas de barramento, que partem de uma linha de propósito.
- Sete capturas 1080 × 1920 exportadas com snapshot (não render), cinco banners salvos em assets/, sete versões 540 × 960 em plano/ e folha geral em plano/sequencia.png. Duas fontes locais carregadas nas capturas.
- A conversão do frame HDR para SDR removeu a promoção automática indevida para BT.2020/HEVC da prévia. Nenhum original alterado.
- Nenhum arquivo MP4 final gerado. Falta aprovação visual.

## Histórico

- v1: proposta textual com cinco conceitos, gancho sorteado de 5 s, Evals destacado como o mais importante e recurso do CTA definido pelo usuário. Nenhuma imagem ou composição gerada.
- v2: nomes dos itens 1 e 2 atualizados; quarto item renomeado para AI Ops com a pergunta solicitada; CTA alterado para RECURSOS e entrega ampliada para artigos sobre os cinco conceitos. Pesquisa dos demais artigos adiada a pedido do usuário. Gancho, durações e demais textos preservados.
- v3: estrutura textual aprovada. Criados cinco banners pedagógicos e sete capturas estáticas com a identidade alvinegra; mantidos os 37 s e os textos da v2. Plano visual submetido para aprovação antes da composição e render finais. Pesquisa dos artigos ainda pendente para etapa posterior.
- v4: painéis brancos com diagramas pretos nos cinco banners, título acima e legenda abaixo, sobre fundo preto. Gancho e CTA sem alteração; mesmos 37 s e mesmos textos da v2. Dois rótulos novos nos diagramas e alguns reescritos para caber nas caixas.
- v4 · montagem: composição final em `index.html` na raiz do projeto, com o take de abertura real (`assets/gancho-sdr.mp4`, cópia SDR sem som; o original não foi alterado). Check sem erros, contraste 46/46, capturas em `plano/capturas-final/`. Render não executado.
- Final: "pronto" do usuário em 2026-10-18. Renderizado em qualidade looks (1080 × 1920, H.264, 30 fps, 37 s, 7 MB, sem áudio). Depois, a pedido do usuário, movido para `posts/script/5-conceitos-de-ia-que-empreendedores-precisam-conhecer/reels.mp4` para indicar que está postado. A ideia no Notion foi atualizada para `Processed` e `Reel`. Falta registrar a resposta automática (palavra RECURSOS) com os artigos dos cinco conceitos.
- Montagem final (sem render): composição em `index.html` na raiz do projeto, com o take de abertura real em `assets/gancho-sdr.mp4` (cópia SDR 1080 × 1920, sem áudio) e os mesmos painéis da v4. Linha do tempo de 37 s conferida. Check sem erros; contraste 46/46. Capturas em `plano/capturas-final/`. Aguardando decisão sobre o som original e o "pronto".
