# Modo Lista com gancho

Vídeo vertical montado a partir de uma lista: um vídeo de gancho com texto por cima, um banner por item da lista e uma tela final de CTA. Este modo não parte de um vídeo de `video/inputs/`. O material de abertura vem de `video/hooks/`.

Estrutura fixa:

1. **Take 1:** vídeo de gancho com uma legenda de impacto por cima.
2. **Um take por item da lista:** tela em dark brown `#280e03`, imagem explicativa e uma legenda pequena.
3. **Take final:** tela em dark brown `#280e03` de CTA, sem imagem.

Os comportamentos gerais de `editar-video` continuam valendo. O plano de sequência e a aprovação antes do render final também. Neste modo os ganchos não têm som para a edição: não há fala a transcrever nem silêncio de fala a cortar; registre `legenda-evals` e corte de espaço morto como "não se aplica". As legendas deste modo são overlays de texto próprios, não `legenda-evals`. `perfil-pb` e `aviso-2x` ficam desligados, salvo pedido explícito.

## Áudio: fora do escopo

O vídeo final deste modo é **sem áudio**. O usuário adiciona a música diretamente no Instagram. Mesmo que o arquivo do gancho contenha uma track de áudio, ignore-a e mantenha o gancho mudo na composição e na exportação. Não investigar volume, fala ou silêncios, não transcrever, não buscar música, não criar narração, efeitos, mixagem ou sincronização com batidas. Não perguntar sobre trilha nem deixar o som como pendência: a aprovação é visual.

## Entrada

A lista vem de uma destas fontes:

- **Ideia do Notion:** banco **Ideas**, data source `e2970ca3-7724-4a81-8f12-7ea34c048c67`. Leia a linha indicada pelo usuário, com título, notas e itens. Use o Notion somente para leitura: não altere `Status` nem `Format`, a menos que o usuário peça.
- **Descrição na chamada:** os itens ditos pelo usuário na própria mensagem.

Se não houver ideia identificável nem lista na mensagem, peça uma das duas. Cada item da lista vira um take. Não funda, descarte nem acrescente itens sem avisar. Se a lista estiver ambígua, pergunte antes de propor.

## Caminho rápido até o pré-plano

Nesta fase a entrega é editorial, não técnica. Depois de ler `SKILL.md` e este modo, faça somente:

1. **Ler a fonte mínima.** Se a lista já está na conversa, use-a sem consultar o Notion de novo. Se o usuário indicou uma ideia, leia essa ideia. Se indicou um roteiro local, localize e leia o roteiro final, sem abrir o vídeo, transcrições ou o projeto antigo. Pesquise apenas o necessário para encontrar a fonte indicada, não o histórico inteiro de conteúdo.
2. **Escolher o gancho uma vez.** Liste os MP4 da raiz de `video/hooks/` uma vez, sorteie um e consulte somente a duração desse arquivo, se necessário. Não analise os demais arquivos. Se houver erro ou bloqueio de acesso, apresente o pré-plano com gancho a confirmar e duração estimada, em vez de interromper a proposta por investigação técnica.
3. **Escrever e apresentar.** Proponha gancho textual, categoria, legendas, durações estimadas e CTA inline no chat. Registre a estrutura em `plano.md`, sem construir composição ou imagens. Pare para a revisão do usuário.

**Só depois do ok textual:** leia `design/identity.md`, os catálogos visuais e as skills técnicas exigidas para produzir as imagens e montar a sequência. Antes disso, não carregue o roteador HyperFrames nem suas skills de domínio, não execute instalação, atualização, catálogo, preview, validação ou captura. A leitura desses documentos não é necessária para aprovar os textos.

A pesquisa dos recursos prometidos no CTA, a localização da publicação no Instagram, o cadastro da resposta automática e a consulta ao estado de atendimento de comentários ficam para suas etapas posteriores. Material já informado deve ser anotado, não pesquisado ou verificado novamente como condição para apresentar o pré-plano. Não prometa uma entrega específica que ainda não foi definida; proponha uma frase coerente e sinalize o recurso a confirmar.

Dúvidas que não impedem escrever os textos entram como observações na proposta, não como uma sequência de perguntas preliminares. Pergunte antes somente se faltar a lista ou houver uma ambiguidade que impeça identificar o conteúdo. Não delegue a proposta simples a subagentes nem crie documentos extras de planejamento.

## Vídeo de gancho

Escolha **aleatoriamente** um arquivo `.mp4` na raiz de `video/hooks/`. Há versões normais e espelhadas, todas verticais; todas valem. Não use a subpasta `originais/`. Sorteie de verdade, sem favorecer o primeiro da lista, e registre no plano o arquivo escolhido. Se o usuário pedir um gancho específico, use esse. A duração do take 1 é a duração do vídeo escolhido: não estique nem repita o vídeo sem pedido.

Canvas final: vertical, 1080 × 1920.

## Proposta de estrutura (antes de gerar qualquer coisa)

Antes de criar imagens ou montar a composição, envie a estrutura **inline na própria resposta do chat**, em Markdown legível, take a take. Não substitua a proposta por um link para `plano.md`, tabela, bloco de código, HTML, Canvas ou anexo. Salve `plano.md` como registro, mas o usuário precisa conseguir revisar todos os textos sem sair da conversa. Não gere nem mostre imagens nesta etapa.

Apresente o pré-plano assim, seguindo a organização usada na sessão dos cinco conceitos:

- Abra com **Lista com gancho · Estrutura v<N>**.
- Informe o arquivo de gancho, sua duração, a duração total prevista e a categoria escolhida para as legendas.
- Use um subtítulo por take: **Take 1 · <duração> s · Vídeo de gancho**, **Take 2 · <duração> s · Banner** e assim por diante.
- No gancho, escreva **Texto sobre o vídeo:** e a chamada em uma citação Markdown (`>`).
- Em cada banner, escreva o número e o nome do item em negrito, depois **Legenda:** e o texto proposto em uma citação Markdown. Uma frase breve sobre o que a imagem explicará é permitida quando ajudar a entender o item, mas não desenhe, gere nem detalhe a execução da imagem agora.
- Termine com **Take final · <duração> s · CTA**, indique tela em dark brown `#280e03` sem imagem e apresente as três linhas do CTA em uma citação, com a palavra-chave em negrito e entre aspas.
- Feche pedindo aprovação dos textos para preparar as imagens e a sequência visual. Ainda não é aprovação de render final.

Não faça uma rodada de pesquisa visual, setup de HyperFrames ou análise do áudio antes de entregar o pré-plano. Use a ideia/lista e os recursos já disponíveis; esclareça apenas dúvidas indispensáveis para os textos. A imagem de cada banner só é criada depois da aprovação.

Cada texto é escrito em português natural do Brasil, seguindo as regras de voz do `AGENTS.md`.

### O texto do gancho (take 1)

É o texto que decide se a pessoa continua assistindo. Escreva uma chamada que prenda a atenção com curiosidade e faça a pessoa sentir que aquilo é importante para ela. O que a chamada promete tem de ser entregue pela lista: um gancho que a lista não cumpre quebra a confiança do público.

### As legendas dos banners (takes do meio)

Cada banner leva uma imagem e uma legenda pequena, e a legenda também tem de manter a pessoa engajada. Não repita só o nome do item. Escolha a categoria de informação que, para esta lista, mais prende a atenção, por exemplo áreas afetadas (logística, financeira, jurídica e assim por diante) ou tipos de profissionais mais afetados. Declare a categoria na proposta e escreva cada legenda dentro dela, de modo que os banners soem como uma série.

A imagem carrega a explicação do item. A legenda acrescenta o ângulo da categoria.

Ponto de partida para a duração: cerca de 3 s por banner, ajustando ao tempo de leitura da legenda e de entendimento da imagem.

### O CTA (take final)

Pense numa boa palavra-chave para o público comentar e proponha-a na estrutura. Requisitos:

- Uma única palavra, porque o atendimento dos comentários só aceita comentários de uma palavra.
- Coerente com o conteúdo da lista.
- Use a palavra definida pelo usuário ou proponha uma palavra coerente. Não é necessário que seja inédita entre todos os posts: o atendimento associa a palavra à publicação. Não pesquise palavras-chave anteriores nem pendências de atendimento para apresentar o pré-plano. A associação com o post correto é conferida depois, em `registrar-resposta-automatica`.

O take final tem fundo dark brown `#280e03` e **nunca leva imagem**. Compõe-se de três linhas, de cima para baixo:

1. `comenta:` (com dois pontos).
2. A palavra-chave em tamanho grande, entre aspas.
3. Uma frase curta dizendo que você envia os materiais ou recursos para quem comentar, coerente com o assunto do vídeo, para quem quiser saber mais.

### Iteração

Reenvie a estrutura completa a cada rodada de feedback, alterando só o que foi pedido, e registre a versão no `plano.md`. Reutilize a fonte, o gancho sorteado, a categoria e os textos não afetados: não releia todas as skills, não sorteie outro gancho e não reabra pesquisa a cada correção. Se o usuário mudar a fonte ou pedir informação nova, consulte apenas o necessário para essa alteração. Repita até o usuário dizer que está ok. Só então avance para a geração.

## Depois do ok da estrutura

### 1. Gerar as imagens dos banners

Crie uma imagem por item com a identidade Miyakodo. Leia `design/identity.md` e use o logo, as fontes e o mascote destas pastas:

- **Logo:** `design/logo/png/` e `design/logo/pdf/`, horizontal e vertical. A tabela de arquivo e cor está em `design/identity.md`. No fundo dark brown, use a versão off-white. No painel off-white, use a versão dark brown.
- **Fontes:** títulos em Instrument Serif, corpo em Poppins. A origem é `design/fontes/instrument-serif.zip` e `design/fontes/poppins.zip`. Para renderizar, use as cópias em `assets/fonts/` desta skill e copie os arquivos da peça para os assets do projeto em curso. Licenças: `InstrumentSerif-OFL.txt` e `Poppins-OFL.txt`.
- **Mascote:** Carlos, em `design/mascote-e-textura/`. Escolha a expressão que combina com o item, pela tabela de `design/identity.md`. A textura de anéis está em `design/mascote-e-textura/textura.pdf`.

Paleta, como em `design/identity.md`: off-white `#f6f4ee`, cinza `#aba199`, dark brown `#280e03`, verde `#1a3010`. Cores de apoio: `#b6cadb`, `#c1c167`, `#d39ca7`, `#db3c05`.

Neste modo, distinga duas superfícies:

- **Tela do vídeo:** fundo dark brown `#280e03`.
- **Imagem explicativa:** painel de fundo off-white `#f6f4ee`, com título, textos, desenhos e diagramas em dark brown `#280e03`. A imagem deve parecer uma referência externa, como um recorte de um recurso que está sendo mostrado no vídeo, mesmo sendo produzida para esta peça.

Dentro do painel off-white, o título identifica o assunto e a imagem explica o item. Fora dele, na área dark brown, a legenda em off-white `#f6f4ee` comenta a imagem. A legenda fica fora do painel, e o banner mantém as duas superfícies. Não inventar fonte, autoria, logo, citação ou atribuição externa para simular a referência. O logo da peça é o da Miyakodo, nas pastas acima.

Verde, cinza e as cores de apoio entram no painel para contraste e ponto de atenção.

Títulos em Instrument Serif: `InstrumentSerif-Regular.ttf` e, no itálico, `InstrumentSerif-Italic.ttf` (`font-family: "Instrument Serif"`, peso 400). Corpo e legendas em Poppins: `Poppins-Regular.ttf` (400), `Poppins-SemiBold.ttf` (600), `Poppins-Bold.ttf` (700), `Poppins-ExtraBold.ttf` (800). Declare cada TTF de Poppins com `format("truetype")` e `font-family: "Poppins"`, com o peso do arquivo. SemiBold e ExtraBold trazem o peso no nome interno da família; o `font-weight` do `@font-face` é o que vale.

As imagens devem ser pedagógicas e chamar bastante atenção: fluxos, workflows, setas, caixas, o que fizer a pessoa parar para olhar e entender o item. Escolha o que explica melhor cada item, com a paleta, o logo e o mascote da identidade. O enquadramento de referência está em [assets/lista-com-gancho-sequencia.png](../assets/lista-com-gancho-sequencia.png). O print é da identidade anterior. As cores e as fontes vigentes são as desta spec (Miyakodo).

Guarde as imagens em `video/projects/<slug>/assets/`, onde `<slug>` deriva do título da ideia.

### 2. Plano de sequência com as imagens reais

Siga a regra de `editar-video`: monte o `plano.md` e uma **prancha única `plano/sequencia.png`**, com as imagens reais. Use como padrão de enquadramento a referência permanente [lista-com-gancho-sequencia.png](../assets/lista-com-gancho-sequencia.png), já preservada dentro desta skill. O print é da identidade anterior. As cores e as fontes vigentes são as desta spec (Miyakodo). Não é necessário consultar o projeto antigo.

A prancha tem fundo off-white `#f6f4ee` e miniaturas verticais de todos os takes, em ordem de leitura da esquerda para a direita e de cima para baixo. Acima de cada miniatura, mostre número do take e duração, fora do conteúdo do vídeo. Use até quatro takes por linha e acrescente linhas conforme a quantidade de itens, sem obrigar a lista a ter cinco itens. Preserve as proporções e mantenha a resolução suficiente para inspecionar textos e diagramas.

- Primeira miniatura: frame real do gancho com o texto aprovado por cima.
- Miniaturas intermediárias: tela em dark brown `#280e03`, painel explicativo off-white `#f6f4ee` com arte em dark brown e legenda off-white abaixo, exatamente como aparecerão no vídeo.
- Última miniatura: CTA em dark brown `#280e03`, somente os três textos, sem imagem.

Mostre `sequencia.png` **inline no chat**, não apenas seu caminho. Gere a prancha a partir dos PNGs dos banners, do CTA e de um frame do gancho, sem renderizar um MP4 completo, criar animações ou inicializar um projeto HyperFrames separado só para a prancha. Reaproveite os assets e refaça apenas os takes alterados, remontando a prancha a cada revisão. Se uma miniatura estiver pequena demais para conferir, forneça também a captura daquele take em tamanho maior.

Itere com o usuário até aprovar a sequência visual. O ok do pré-plano textual autoriza criar as imagens, não pular esta revisão.

### 3. Render final

Só depois do "pronto" do usuário, monte e renderize pelas skills do HyperFrames, conforme o roteador. O render vai para `video/outputs/`.

## Último passo: recursos e resposta automática

Quando o usuário aprovar a versão final do vídeo, a última etapa da skill é **sempre** perguntar quais recursos ele vai enviar para quem comentar a palavra-chave. Pergunte quais são e peça o link ou arquivo de cada um. Não invente nem presuma recursos.

Com a resposta, execute a skill [registrar-resposta-automatica](../../registrar-resposta-automatica/SKILL.md), passando a palavra-chave do CTA e os recursos informados, para registrar a resposta automática na pasta da peça. Siga as regras daquela skill. Em particular, ela exige o link do post do Instagram e uma pasta de peça existente em `posts/`; se faltar algum dos dois, peça ao usuário, sem criar pasta nem inventar link.
