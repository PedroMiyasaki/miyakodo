# Modo Notícias

Use este documento quando o usuário selecionar o modo **Notícias** ou quando a edição for claramente uma cobertura de notícia, acontecimento recente ou atualidade. Se a categoria não estiver clara e ativar este modo mudar os overlays, pergunte qual modo usar antes de preparar o plano.

Este modo define somente as intervenções específicas de notícias. Os comportamentos gerais de `editar-video` continuam valendo. Não acrescente outros tratamentos visuais além dos overlays descritos aqui e dos comportamentos gerais.

## Padrões opcionais ativados neste modo

Neste modo, ativar ambos, mesmo sem um pedido separado para cada um:

- `perfil-pb` durante o vídeo, conforme [`Perfil PB`](../video-patterns.md#perfil-pb).
- `aviso-2x` uma vez, conforme [`Aviso 2x`](../video-patterns.md#aviso-2x). Propor no plano um trecho de 3,4 s, de preferência junto a um gesto apontando para baixo. Se não houver gesto, escolher um trecho visualmente livre, sem cobrir rosto, legenda, gráfico ou captura de notícia. Registrar o trecho e a posição no plano.

Um pedido explícito do usuário para desligar um deles neste vídeo prevalece. A ativação vale somente para esta edição no modo Notícias; fora dele, ambos continuam desligados por padrão.

## Overlays editoriais do modo

A fala do vídeo é a fonte dos gatilhos. Identifique as entidades e os eventos na transcrição e prepare os overlays correspondentes. Cada overlay entra no trecho em que a fala trata daquele assunto, não permanece na tela durante o vídeo todo. Reutilize a mesma captura se a entidade ou notícia voltar a ser mencionada; não crie uma cópia por repetição da palavra.

### 1. Empresas: logo original

Quando o usuário falar o nome de uma empresa, incluir a logo original dessa empresa como overlay durante o trecho correspondente.

- Localizar a marca com automação do navegador. Preferir a página oficial da empresa ou seus materiais oficiais de marca. Usar a imagem real da logo, sem redesenhar, gerar ou substituir por um ícone aproximado.
- Fazer uma captura de tela no navegador que preserve a logo encontrada. Recortar para o overlay somente a área necessária, mantendo a identidade e a proporção da marca.
- Verificar que o resultado é a empresa citada, não outra empresa com nome semelhante. Registrar a URL de origem no plano.
- Uma captura por empresa é suficiente; reaproveitá-la em menções seguintes e sincronizar sua exibição com cada trecho relevante.

### 2. Pessoas famosas: fotografia da pessoa

Quando o vídeo mencionar pelo nome uma pessoa famosa ou figura pública, incluir uma fotografia real e reconhecível dessa pessoa no trecho correspondente.

- Encontrar a fotografia com automação do navegador e fazer uma captura de tela da imagem original. Preferir uma página oficial ou uma fonte editorial confiável que identifique corretamente a pessoa.
- Não gerar, ilustrar, substituir por outra pessoa nem usar uma imagem cuja identidade seja incerta. Verificar o nome e a imagem na fonte; registrar a URL no plano.
- Preparar uma captura por pessoa e reutilizá-la nas menções seguintes. Sincronizar o overlay com os trechos em que a pessoa é mencionada.
- Se o nome for ambíguo ou a fonte não confirmar quem aparece na imagem, deixar como pendência e perguntar; não adivinhar.

### 3. Ações: gráfico real do período mencionado

Quando a fala disser que ações/cotações de uma empresa subiram, caíram ou ficaram estáveis, incluir uma captura do gráfico real daquela ação cobrindo o período citado.

- Identificar a empresa, o ticker e o período exato a partir da fala e do contexto do vídeo. Preferir o Google Finance: pesquisar a ação e ajustar o gráfico ao intervalo mencionado.
- A captura precisa corresponder ao ticker e ao período corretos. Registrar ticker, intervalo, URL e data da captura no plano. Não usar um gráfico genérico, inventado, de outra ação ou que mostre um período diferente como se fosse o citado.
- Se o ticker não puder ser determinado com segurança, registrar a pendência e pedir esclarecimento antes de fechar o plano. Se a expressão do período for ambígua, propor no plano a leitura escolhida e marcar a confirmação do usuário como pendência. Não preencher uma lacuna com um intervalo arbitrário nem apresentar um período inferido como fato confirmado.
- Mostrar o gráfico enquanto a fala explica esse movimento. O gráfico não deve encobrir a pessoa falando ou as legendas.

### 4. Notícias: captura da notícia mencionada

Quando o usuário disser explicitamente que uma notícia foi publicada ou que um acontecimento foi noticiado, incluir uma captura da página da notícia que corresponde ao que está sendo dito.

- Encontrar a notícia com automação do navegador. Se a fala nomear publicação ou URL, abrir essa fonte. Caso contrário, localizar uma notícia confiável sobre o acontecimento exato, preferindo a fonte primária quando existir.
- Capturar a página original e enquadrar título, publicação e data de forma legível. Não substituir a notícia por um artigo apenas relacionado ou por um resumo inventado.
- Registrar no plano a manchete, o veículo, a URL e a data da captura. Mostrar a captura durante a fala sobre aquela notícia.
- Se não for possível confirmar que a página corresponde ao acontecimento narrado, deixar a captura como pendência e perguntar; não fabricar uma manchete nem alegar que foi a fonte citada.

## Pesquisa, captura e arquivos

- Fazer a pesquisa e as capturas usando automação do navegador, conforme as instruções globais para o Google Chrome. Inspecionar a aba e o endereço antes de interagir; depois da navegação, confirmar a página e verificar a captura. Se a página pedir login, apresentar CAPTCHA ou depender de confirmação manual, parar e pedir ajuda ao usuário.
- Guardar as capturas específicas deste vídeo nos assets do projeto de edição, por exemplo `video/projects/<slug>/assets/`. Não guardá-las na pasta permanente desta skill nem depender dos assets de outros projetos.
- Usar arquivos reais e preservar sua proveniência. Para cada captura usada, registrar fonte e URL no plano. Não confundir o screenshot de referência da skill com a imagem a pesquisar para uma nova edição.
- Depois de preparar as imagens, encaminhar a composição, a camada, o posicionamento e o timing dos overlays às skills técnicas indicadas pelo roteador HyperFrames. Este modo determina **o que** procurar, **quando** inserir e a fonte que comprova a imagem; o HyperFrames determina **como** compor e renderizar.

## Plano de sequência

Antes de montar a composição, apresentar os overlays e sua intenção no plano e aguardar a aprovação normal de `editar-video`. O plano de Notícias inclui:

- Modo ativo: Notícias.
- `perfil-pb`: ligado pelo modo ou desligado por instrução explícita do usuário.
- `aviso-2x`: ligado pelo modo ou desligado por instrução explícita; trecho proposto e posição.
- Uma linha por empresa, pessoa, notícia ou movimento de ação: gatilho/trecho falado, tempo de origem, tempo previsto na edição, captura preparada, URL e, para ações, ticker e intervalo do gráfico. Preparar/consultar as capturas de navegação para revisão visual; não confundir a proposta com a composição/render final.
- Pendências de identificação, período ou fonte que precisem de resposta do usuário.

Capturas de navegador são assets e provas baratas para revisar no plano. Não renderizar o vídeo completo antes de o usuário aprovar o plano e dizer “pronto”, conforme a skill `editar-video`.
