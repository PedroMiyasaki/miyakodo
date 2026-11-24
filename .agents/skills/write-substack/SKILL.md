---
name: write-substack
description: >
  Produz um artigo ilustrado para o Substack a partir de uma ideia nova, uma
  notícia ou uma tese já publicada em outro formato. Pesquisa fontes primárias,
  planeja a narrativa, escreve o artigo e captura as imagens que sustentam o
  texto. Ative com pedidos como "escreve o Substack da semana", "transforma
  <slug> em artigo" ou "escreve um artigo sobre <tema>".
---

# Artigo de Substack

## Git

Peça desta skill entra por commit direto na `main`. Não abra pull request e não crie branch para o conteúdo. Rascunho e versão final são conteúdo. Saída intermediária ou que dá para gerar de novo fica de fora do git, no caminho coberto pelo `.gitignore`.

## Quando agir

Use esta skill quando o usuário pedir uma peça longa e ilustrada para o Substack, seja a partir de uma ideia nova, uma notícia ou um conteúdo já produzido.

## Protocolo de execução

### Passo 1 · Identificar o assunto e o caminho

**Reuso:** o usuário indica um slug já produzido em `posts/script/` ou `posts/linkedin/`. Se não indicar, liste os mais recentes e pergunte qual deve virar artigo. Reaproveite o slug no Substack. A ideia já foi fechada no formato original, portanto este caminho não escreve nada no Notion.

**Standalone:** use a notícia trazida pelo usuário ou selecione a ideia `Pending` mais recente em **Ideas**, data source `e2970ca3-7724-4a81-8f12-7ea34c048c67`, e confirme o título. No fechamento, este caminho atualiza a ideia para `Status` = `Processed` e `Format` = `Substack`. Se essa opção de formato não existir, pare e peça ao usuário para criá-la pela interface do Notion.

### Passo 2 · Entender e pesquisar

No caminho de reuso, leia o `final.md` de origem e a ideia no Notion. Descubra o que o artigo pode aprofundar sem repetir as mesmas frases ou apenas alongar o conteúdo anterior.

No standalone, leia todo o material disponível e consulte as fontes primárias antes de planejar: anúncio, paper, model card, documentação, página de preços, changelog ou repositório. Se não houver material suficiente para sustentar um artigo, diga isso em vez de preencher espaço.

### Passo 3 · Calibrar pelo histórico

Leia a última versão de até cinco artigos recentes em `posts/substack/`: `final.md` quando existir ou o `sketch/v<N>.md` de maior número. Observe também as imagens, sua posição e suas legendas.

Use o histórico como few-shot, não como checklist. Perceba vocabulário, registro, construção das frases, ritmo, tamanho dos parágrafos, densidade técnica, uso de primeira pessoa, opinião, humor, aberturas, encerramentos, headings, recursos de Markdown e relação entre texto e imagem. Imite os padrões recorrentes sem copiar frases e dê mais peso aos exemplos recentes.

Se houver menos de cinco, use o que existir. Se não houver nenhum, siga sem calibração.

### Passo 4 · Planejar o artigo e a shot list

Assuma o papel de um escritor experiente de Substack. Defina heuristicamente a estrutura narrativa que melhor serve ao material, com a profundidade que ele sustenta. Planeje o arco do artigo e um outline de seções antes de escrever.

Monte também a shot list em `posts/substack/<slug>/sketch/shotlist.md`:

| # | Âncora | O que precisa mostrar | Onde capturar | Status |
|---|---|---|---|---|
| cover | - | mecanismo ou artefato central | fonte | planejada |
| 01 | frase depois da qual entra | evidência que responde à passagem | fonte | planejada |

Planeje de três a oito imagens, além da capa. Cada imagem precisa responder a uma passagem do texto e ter uma fonte real. Capture falhas também quando elas fizerem parte da história.

Apresente ao usuário o arco narrativo, o outline e a shot list. Espere a aprovação antes de escrever.

### Passo 5 · Escrever o artigo

Depois da aprovação, escreva seguindo o plano. O título declara a descoberta ou a tese; o subtítulo acrescenta consequência ou escopo. O corpo prepara cada imagem antes do marcador e explica depois o que ela demonstra. Use headings, links, tabelas, código e blockquotes quando ajudarem o artigo.

Formato obrigatório:

```markdown
# <título>
### <subtítulo>

<artigo com headings e marcadores de imagem>

![01 - <legenda provisória>](01.png)

---
Palavras: <contagem>
ACP: <fase>
Estrutura: <descrição curta do arco narrativo>
Imagens: <N>, ver shotlist.md
Fontes: <URLs das fontes primárias>
Reuso de: <slug> <!-- somente no caminho de reuso -->
```

### Passo 6 · Apresentar, salvar e iterar

Derive o slug do título, salvo quando o caminho de reuso já tiver um. Salve a primeira versão em `posts/substack/<slug>/sketch/v1.md`.

Apresente o artigo completo com título, subtítulo, contagem de palavras e marcadores de imagem. Para cada correção, crie `sketch/v<N+1>.md`, preservando verbatim tudo que não precisa mudar. Trave o texto com o usuário antes da captura.

### Passo 7 · Capturar as imagens

Use a automação de navegador disponível, abra uma aba nova e percorra a shot list de cima a baixo numa única sessão.

#### 7a · Inegociáveis

- Capture páginas reais ao vivo. Não fabrique, gere por IA, monte em HTML ou use stock.
- Prefira sempre a fonte primária ao conteúdo que comenta sobre ela.
- Não use paywall, informação privada, dashboard interno ou tela logada com dados de terceiros.
- Registre a URL de toda captura na shot list no momento em que ela for feita.

#### 7b · Técnica de captura

- Ajuste o zoom antes de capturar; não dependa de corte posterior.
- Enquadre o elemento, sem interface do navegador, navegação, sidebar, banners ou scrollbar.
- Feche banners e escolha o tema de maior contraste.
- Para texto, configuração ou log, use zoom de 125% a 150%.

#### 7c · Checagem por imagem

Antes de seguir, confirme:

1. continua legível a 50% da largura;
2. mostra uma ideia clara;
3. não contém elementos estranhos ao assunto;
4. responde à frase-âncora;
5. tem a URL registrada.

Refaça a captura se algum item falhar.

#### 7d · Capa

A capa deve funcionar em corte horizontal próximo de 2:1, com alto contraste, poucos elementos e nada essencial nas bordas. Prefira o mecanismo central, um gráfico forte ou o artefato real do artigo.

Se existir `posts/linkedin/<slug>/image.png`, mostre ao usuário e pergunte antes de reaproveitar.

#### 7e · Quando um take não existe

Se a fonte real não existir depois de tentativas honestas, ajuste o texto e retire a captura da shot list. Não use imagem decorativa para preencher a vaga. Informe ao usuário o que caiu e por quê.

#### 7f · Salvar e registrar

Salve os arquivos publicados na raiz do slug:

```text
posts/substack/<slug>/cover.png
posts/substack/<slug>/01.png ... NN.png
```

Atualize cada linha de `sketch/shotlist.md` com o status final e a URL da fonte.

### Passo 8 · Legendar, posicionar e revisar

Cada imagem recebe uma legenda que indica o que observar e credita a fonte com link. Substitua os marcadores provisórios pelas legendas reais.

Leia o artigo com as imagens no lugar. Verifique se cada uma foi preparada pelo texto, se o ritmo visual funciona e se legenda e parágrafo não repetem a mesma coisa. Salve correções em uma nova versão.

Apresente o conjunto ao usuário e pergunte se alguma imagem ou passagem precisa ser refeita.

### Passo 9 · Fechar

Quando o usuário disser "pronto", copie o `sketch/v<N>.md` mais alto verbatim para `posts/substack/<slug>/final.md`. Mantenha o histórico e a shot list em `sketch/`; a raiz contém `final.md`, `cover.png` e as imagens numeradas.

Execute o fechamento do Notion definido no Passo 1: nenhuma escrita no caminho de reuso; `Status` e `Format` no standalone.

### Passo 10 · Entregar

Informe o título, a contagem de palavras e imagens e o caminho `posts/substack/<slug>/`. Para publicar, o usuário cola `final.md` no Substack, substitui os marcadores pelos PNGs correspondentes e define `cover.png` como capa.
