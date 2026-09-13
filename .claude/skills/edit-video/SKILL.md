---
name: edit-video
description: >
  Use quando for editar um vídeo de talking head até virar um Reel pronto: "edita
  esse vídeo", "transforma isso num Reel", "edita no modo news", ou quando um
  arquivo em video/inputs/ precisa de edição.
---

# SKILL · Editar vídeo (Reel)

Camada do projeto em cima da skill `video-use`. A `video-use` é a engine genérica
(transcrição, corte, concat, loudnorm, composição) e carrega as regras de correção
de produção. Esta skill não reimplementa a engine: ela escolhe um **modo** (uma
coleção de **features**) e roda cada feature.

## Arquitetura

| Camada | Onde | Papel |
|---|---|---|
| **Feature** | `assets/features/<id>.md` | Uma capacidade de edição (o quê + como) |
| **Modo** | `assets/modes/<id>.md` | Lista ordenada de ids de feature |
| **Orquestrador** | este `SKILL.md` | Entrada e saída, invariantes, escolha do modo, protocolo |

Features atuais: `cut-dead-air`, `subtitles`, `loudnorm`, `news-inserts`,
`zoom-emphasis`, `black-and-white`, `pop-it`, `motion-third`.
Modos atuais: `baseline`, `news`, `authority`. Só faltam o helper do
`motion-third` (opt-in, não trava nenhum modo) e o micro-zoom visual do `pop-it`.
Veja `assets/modes/authority.md`.

Para adicionar uma capacidade nova: escreva `assets/features/<id>.md` e depois
referencie de um modo que já existe, ou crie `assets/modes/<id>.md`. Não embuta
lógica de feature nova neste arquivo.

Toda feature declara uma `phase` no frontmatter. Rode as features na ordem do
modo, agrupadas pelas fases naturais do pipeline:

1. `edl`: monta os `ranges` (e o que mais a feature mudar na EDL)
2. `plate`: efeitos sobre o talking head (`plate_effects`: zoom, P&B, pop-it)
3. `overlays`: gera os clipes e preenche `edl.overlays` (news, motion)
4. `render`: chama o `render_vertical.py` com as flags da feature (loudnorm,
   e `subtitles` só no render final, veja `assets/features/subtitles.md`)

## Invariantes (todo modo)

- **Nada de conversão para 9:16.** Preserve o enquadramento, a resolução e o
  frame rate da fonte (60fps gravado sai 60fps, preview incluído, e os cards do
  `news_insert.py` recebem o mesmo `--fps`).
- **O talking head nunca é redimensionado nem cortado.** Imagem de referência
  (`news-inserts`) é sempre um **card flutuante** composto por cima do vídeo:
  ela nunca reserva espaço nem força crop ou pillarbox. No `news` cada card é
  breve (alguns segundos, sincronizado com o assunto que está sendo falado) e
  some. Ele não precisa cobrir a peça inteira nem segurar até o assunto
  seguinte. Veja `news-inserts.md`. Em `authority` e em conteúdo pedagógico o
  editor **julga beat a beat** onde a ênfase tem que cair (rosto ou diagrama).
  Na dúvida, terço vazio. Veja `motion-third.md` § Julgamento editorial.
- **Notas de editor:** instruções que o usuário fala para o editor no meio do
  take, com as palavras que saírem. **Obedeça** na edição e **corte** da
  entrega (áudio, imagem e legendas do vídeo). Elas nunca são anunciadas, não
  seguem formato e **não ficam presas à lista de features abaixo**: o usuário
  está passando um briefing para um editor, não preenchendo um formulário.
  Fique atento a elas em todo take. Veja § Notas de editor.
- Siga as Hard Rules da `video-use` (extração por segmento + concat `-c copy`,
  fade de 30ms, overlay com `setpts`, nunca cortar no meio de uma palavra, ASR
  com timestamp por palavra, cache de transcrição, confirmar a estratégia antes
  de executar, outputs em `<edit>/`).
- **As legendas do vídeo saem por padrão, e só no render final.** Todo modo
  recebe legendas queimadas, mas nunca num preview: elas são queimadas quando o
  corte já travou, então iterar na edição nunca paga o re-encode. O usuário
  desliga só pedindo. Só a inicial da frase em maiúscula, a fonte do
  Alvinegro, trechos curtos que se substituem como a legenda padrão do
  Instagram. Veja `assets/features/subtitles.md`.

## Notas de editor
No meio do take, o usuário para de narrar e fala com **você**. Não existe frase
obrigatória nem marcador para procurar: gravar já dá trabalho demais sem ter
que lembrar de uma sintaxe. A nota sai do jeito que sair:

> “Editor, corta essa parte, vou falar o final de novo.”
> “corta, vou falar de novo”
> “open editor note, on that impression bit go black and white, close editor
> note”: a forma antiga, com marcador, ainda conta como nota, só não é mais
> obrigatória

**Parta do princípio de que toda gravação tem notas.** Leia a transcrição
empacotada como uma pessoa leria, não como um match de padrão: nota é qualquer
trecho dirigido a quem está cortando o vídeo, e não ao público. Os sinais são
falar com o editor, falar *sobre* o vídeo em vez de *dentro* dele, abandonar
uma frase para recomeçar, ou narrar uma intenção (“vou falar de novo”, “deixa
eu refazer”) em vez de uma ideia. Se uma linha só faz sentido para quem está
editando, é nota.

**Os limites são você quem julga.** Uma nota normalmente vai de onde a fala
quebra até onde o próximo take de verdade começa, com uma pausa de cada lado.
Quando a borda é ambígua, corte um pouco mais largo em vez de deixar um pedaço
da nota na entrega, e diga o que cortou.

### O que fazer com a nota
1. **Leia e aplique.** A nota manda na edição do trecho que ela comenta
   (normalmente a fala logo antes ou logo depois do bloco da nota).

   **Não comece perguntando qual feature é.** Pergunte o que o usuário quer que
   o vídeo faça, aí pegue a coisa mais barata que faz isso, nesta ordem: uma
   feature do modo → uma feature fora dele → um ajuste do render que nenhuma
   feature embrulha (o limite de um range, a ordem de dois ranges, um nível, o
   estilo ou a posição das legendas do vídeo, uma margem, uma duração) → algo
   que teria que ser construído. Só o último vira conversa. Os três primeiros
   você faz e reporta.

   **A nota não precisa nomear nada que esta skill tenha palavra para.** A lista
   de features é o vocabulário da implementação, não o vocabulário de quem fala
   enquanto grava, e os dois não vão bater. Trate toda nota como uma instrução
   para um editor que tem a obrigação de descobrir o como, porque é exatamente
   isso que ela é.
2. **Corte do vídeo final.** Tire a nota inteira, a instrução mais o take
   estragado a que ela pertence, da timeline de saída, num limite de palavra. A
   nota **não** vai para o áudio, **não** vai para as legendas do vídeo e
   **não** gera efeito sobre as palavras da própria nota.
3. **Registre** em `<edit>/project.md` (texto da nota → efeito aplicado →
   `start/end` cortados da fonte).

### Exemplos: formas, não um menu

Oito notas que apareceram nas primeiras edições. Estão aqui para mostrar o
**alcance** que uma nota pode ter, não para ser o conjunto das notas que
existem. Uma nota que não parece com nenhuma destas não é uma nota
desconhecida: é o caso comum, e responder a ela caçando a linha mais parecida
abaixo é o jeito de acabar fazendo algo parecido com o que foi pedido em vez da
coisa em si.

| Nota falada | Efeito típico |
|---|---|
| “nessa parte da imitação, vai pra preto e branco” | `black-and-white` na imitação adjacente |
| “dá um punch-in rápido no ‘você tá errado’” | `zoom-emphasis` `fast` no fecho da frase |
| “pop-it em seguro, confiável e auditável” | `pop-it` no início dessas três palavras |
| “mostra o print do paper aqui” | `news-inserts` no terço (imagem da pasta / busca) |
| “anima o fluxo retrieve → rank → generate” | `motion-third` nesse beat |
| “não bota nada no terço nessa parte” | terço vazio, plate limpo |
| “corta essa parte, eu errei” / “corta, vou falar de novo” | descartar o take abandonado e a nota |
| “corta todo esse final que eu falei de X” | descartar **todos** os takes que cobrem X, voltando até onde esse trecho começa |

Exemplo completo, de um take real:

> …“Nesse contexto, se você pagar, por exemplo, a assinatura da OpenAI…”
> **“Editor, corta essa parte, vou falar o final de novo.”**
> “Mas você vai ver que os da Anthropic tão muito altos na coluna de custo…”

Entrega: a frase abandonada sobre a OpenAI **e** a instrução somem as duas, e a
peça continua no retake. Nada sinaliza que havia uma nota ali.

A nota também pode alcançar bem para trás, além do próprio take:

> **“Corta todo esse final que eu falei dos modelos da Anthropic serem bons,
> corta tudo isso. Eu vou falar só o finalzinho agora.”**

Essa delimita por **assunto**, não por proximidade: ache onde o trecho da
Anthropic começa e corte dali, não só da frase anterior à nota. (As legendas do
vídeo são montadas a partir da timeline de saída, então uma nota cortada na EDL
nunca aparece nelas.)

### Regras duras
- **Nunca deixe uma nota na entrega.** Quando não der para saber se uma linha é
  nota ou conteúdo, trate como nota: corte e avise o usuário. Publicar um Reel
  em que dá para ouvir o usuário falando com o editor é a única falha
  irrecuperável aqui.
- **Reporte toda nota antes de renderizar**: o que foi dito, como você leu o
  alcance, o que cortou e o que fez a respeito. Essa é a única chance do
  usuário pegar uma nota que você delimitou larga ou estreita demais. Nota que
  você decidiu *não* aplicar também entra no relato: ficar em silêncio soa como
  "resolvido", e o usuário só descobre na entrega.
- Nota contradiz o julgamento padrão do modo → **a nota ganha** (é a instrução
  do usuário).
- **Nota que você não consegue aplicar é respondida, nunca descartada em
  silêncio.** Se nada no pipeline faz o que ela pede, diga isso na lata, aponte
  a coisa mais próxima que está ao alcance e deixe o usuário escolher.
  Construir algo novo no meio da edição é uma conversa, não uma decisão sua
  sozinho. Só que "nenhuma feature cobre isso" nunca é motivo para deixar uma
  nota sem menção.

## Pré-requisitos

- `video-use` instalada (`~/.claude/skills/video-use/`) com `ffmpeg`/`ffprobe`
  no PATH e `ELEVENLABS_API_KEY` resolvendo (no ambiente ou no `.env` da
  `video-use`, **nunca** no repositório de conteúdo).
- Scripts: `assets/news_insert.py`, `assets/render_vertical.py`,
  `assets/fonts/`.

## Entrada e saída

- **Entrada:** `video/inputs/`. Sem arquivo nomeado → o **mais recente** (maior
  mtime). Só desambigue se o pedido nomear um arquivo que não existe.
- **Rascunho:** `edit/<slug>/` na raiz do repositório (= `<edit>`). Fora do git
  de `video/`.
- **Saída:** no "pronto", **uma pasta só**, `posts/script/<slug>/`, a pasta do
  próprio roteiro, onde o histórico `sketch/v<N>.md` e o `final.md` já moram,
  com os três artefatos lado a lado:

  | Arquivo | O que é |
  |---|---|
  | `reels.mp4` | o corte, com as legendas do vídeo queimadas |
  | `caption.md` | a legenda do post no Instagram |
  | `cover.png` | a capa (a fonte `cover.html` fica em `sketch/`) |

  Eles saem juntos e moram juntos: postar um Reel é abrir uma pasta e encontrar
  ali tudo que ele precisa. O vídeo não é entregue sem a legenda do post e sem
  a capa, e nenhum dos três vai para outro lugar.

  **Os nomes de arquivo são fixos e genéricos. Nunca monte a partir do slug.**
  A pasta já tem o nome da peça, então repetir dentro dela seria dizer a mesma
  coisa duas vezes. Toda pasta de Reel tem os mesmos três nomes, e é isso que
  deixa as pastas comparáveis lado a lado. `reels.mp4` / `caption.md` /
  `cover.png`, em toda pasta, sempre.

## Protocolo

### 1. Fonte + inventário + transcrição
Fonte = o arquivo nomeado ou o mais recente em `video/inputs/`. Helpers da
`video-use`: `ffprobe`, `transcribe.py` (com cache), `pack_transcripts.py`.
Defina o **slug** (título → minúsculas, sem acento, hífens). Rascunho em
`edit/<slug>/`.

**Esse slug é o slug do roteiro.** Um Reel nasce como roteiro, então as
entregas caem na pasta que esse roteiro já tem, `posts/script/<slug>/`, ao lado
do histórico em `sketch/` e do `final.md`, que é o roteiro. Não existe cópia
separada dele na pasta. Se `posts/script/<slug>/` não existe (um vídeo sem
roteiro por trás), crie a pasta e escreva as entregas nela. Só não vai ter
`sketch/` nem `final.md`.

Logo depois de empacotar a transcrição: leia do começo ao fim caçando **notas
de editor** (§ Notas de editor), partindo do princípio de que existem. Extraia
cada uma, planeje o efeito e marque o trecho inteiro para corte na EDL,
**antes** de escolher os beats das features "no automático".

### 2. Escolher o modo
1. Se o usuário nomear um modo (ou um alias), use esse.
2. Senão, se a transcrição cita uma notícia concreta (modelo novo, rodada de
   investimento, aquisição, pesquisa) → `news`.
3. Senão → `baseline`.

Leia `assets/modes/<id>.md` com a ferramenta Read. Confirme a estratégia (modo +
features) com o usuário antes de executar. `subtitles` vai junto em todo modo
sem estar listada em nenhum. Só tire se o usuário pedir.

### 3. Carregar e rodar as features
Para cada feature listada no modo (+ opt-ins explícitos), **nesta ordem**:

1. `Read` em `assets/features/<id>.md`
2. Faça o que o arquivo diz, na `phase` dele

Antes do render, o `edl.json` precisa existir (formato da `video-use`:
`sources`, `ranges` em limites de palavra, `grade`, `overlays`). Sem feature de
overlay → `overlays: []`. **Nenhuma** chave `subtitles` na EDL enquanto você
está no preview: ela entra no render final (§ 5), ou nunca, se o usuário
desligou as legendas.

Itere nos previews (loudnorm = sem `--no-loudnorm`, e **sem** `--subtitles`):

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/render_vertical.py \
  "<edit>/edl.json" -o "<edit>/preview.mp4" --preview
```

Renderize o preview quantas vezes o corte precisar. As legendas do vídeo ficam
fora de todos eles. Veja § 5 para o final.

### 4. Autoavaliação (passo 7 da video-use)
`timeline_view` na saída em toda borda de corte e janela de overlay. Procure
descontinuidades, estalos no áudio e overlays desalinhados (Hard Rule 4). `ffprobe`
na duração. Até 3 passadas. Se persistir, sinalize. **Peça para o usuário ouvir
as emendas do corte** (você não ouve áudio).

A checagem das legendas do vídeo (Hard Rule 1: nenhum overlay cobrindo a faixa
de baixo) é do final, porque os previews não têm legenda. Os overlays que já
ficam baixos no quadro são os que merecem atenção.

### 5. Entrega
"Pronto" é o sinal de que o corte travou, e o único momento em que o render
final acontece. Adicione `"subtitles": "master.ass"` ao `edl.json` e renderize
com `--subtitles` (tire os dois se o usuário desligou as legendas):

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/render_vertical.py \
  "<edit>/edl.json" -o "<edit>/final.mp4" --subtitles
```

Avise que as legendas estão sendo queimadas antes de começar: esse render é
mais lento que os previews, e é o primeiro que tem legenda.

Aí cheque as legendas (§ 4) e leve os três artefatos para a pasta da própria
peça: o corte, a legenda do post e a capa, tudo em `posts/script/<slug>/`. A
pasta quase sempre já existe (o roteiro foi escrito lá), então o `mkdir -p` é
uma proteção para o caso sem roteiro, não o que cria a peça.

```bash
mkdir -p "posts/script/<slug>" && mv "<edit>/final.mp4" "posts/script/<slug>/reels.mp4"
```

Se o usuário reabrir o corte depois disso, volte para os previews: uma edição a
mais renderiza o final do zero de novo.

Depois escreva `posts/script/<slug>/caption.md`, a legenda do post no Instagram
para esse Reel. Ela fica ao lado do vídeo a que pertence, não numa pasta
própria.

**A legenda do post tem duas linhas, não é uma reescrita do Reel.** O vídeo já
disse tudo. O trabalho inteiro da legenda é cair depois dele e pedir o follow.

```
<uma linha curta que engancha no que o Reel acabou de dizer>
siga @pedro.miyasaki.ia
```

A primeira linha é **uma frase só**, que só faz sentido para quem acabou de
assistir. Ela nomeia o assunto do Reel e vira para quem está vendo: confere a
surpresa, abre os comentários ou pergunta de que lado a pessoa está. Não resume
o vídeo, não repete o hook e não ensina nada novo.

A linha do follow é sempre a segunda. O handle é verbatim e o verbo é `siga`.

Cada bloco abaixo é uma legenda inteira, para um tipo diferente de Reel:

```
# Reel: o que é o terminal bench (baseline · explicativo)
E aí? Sabia que o terminal bench era assim?
siga @pedro.miyasaki.ia

# Reel: anúncio de um modelo novo (news)
Esse lançamento me pegou de surpresa. Você já tinha visto?
siga @pedro.miyasaki.ia

# Reel: como guardrails funcionam de verdade (authority · pedagógico)
Ficou com alguma dúvida? Coloca nos comentários
siga @pedro.miyasaki.ia

# Reel: "RAG é muleta" (baseline · tese)
Concorda ou acha que eu tô viajando?
siga @pedro.miyasaki.ia

# Reel: o erro que todo mundo comete escrevendo evals (authority)
Já perdeu tempo com isso também?
siga @pedro.miyasaki.ia

# Reel: por que o seu agente fica em loop (baseline · explicativo)
Espera, você sabia que funcionava assim?
siga @pedro.miyasaki.ia
```

Como ela nunca pode ficar, o Reel reescrito em texto:

```
# ✗ errado
O terminal bench é um benchmark que mede a capacidade de agentes de IA
resolverem tarefas reais em um terminal. Nesse Reel eu explico como ele
funciona, por que ele é difícil e o que os resultados dizem sobre...
```

Mostre a legenda do post no chat também, para o usuário corrigir antes de
postar. Correção reescreve `posts/script/<slug>/caption.md` no lugar: é um
artefato de build ao lado do render, não versionado como `v<N>`.

#### A capa
O Reel também sai com capa: o quadro que segura o feed, então ela é composta,
nunca um frame capturado. O render dela cai na mesma pasta
`posts/script/<slug>/` para onde vão o corte e a legenda do post. A fonte HTML
é um intermediário de build, então fica em `sketch/`. Monte no sistema
**Alvinegro**, sem improviso: leia `design/identity.md` e copie o arquétipo
`01 COVER` de `design/templates/slides.html` (`<style>` e `<defs>` incluídos)
para `posts/script/<slug>/sketch/cover.html`.

- **Quadro 1080×1920, 9:16, a proporção do próprio Reel**, para a capa
  preencher a aba de Reels em vez de ficar com barra em cima e embaixo.
- **O arquétipo é 1080×1350, então o CSS copiado precisa de override.**
  Adicione `.slide{height:1920px}` no `cover.html` depois do `<style>` que você
  copiou. O `--width/--height` do renderizador só dimensiona o *viewport*: o
  PNG sai da caixa CSS do próprio elemento, então sem esse override a capa
  renderiza em 4:5 independente do que a linha de comando diz. Confira o
  tamanho em pixels do render antes de publicar: 3240×5760 no `--scale 3`
  padrão.
- **O feed corta de volta para 4:5, a partir do meio.** Tudo que precisa ser
  lido em tamanho de miniatura, o hook acima de tudo, mora dentro do
  1080×1350 central. Os ~285px acima e abaixo são sangria: a marca e o line art
  podem morar ali, e a altura extra é ar, não licença para um terceiro tamanho.
- Slide invertido (`.slide.inv`), a marca `@handle`, linha display `.hook`,
  linha de apoio `.bd` opcional, line art opcional do vocabulário de desenho
  (caixas, setas, fluxos, terminais, nada figurativo).
- O hook é a própria linha de abertura do Reel, apertada para caber: não é uma
  afirmação nova nem a primeira linha da legenda do post.
- Estritamente preto e branco. Nada de paleta, tipografia ou logo fora do
  sistema.

```bash
uv run python scripts/render_html_to_pngs.py \
  --html "posts/script/<slug>/sketch/cover.html" \
  --out "posts/script/<slug>/sketch" \
  --selector ".slide" \
  --width 1080 --height 1920
mv "posts/script/<slug>/sketch/1.png" "posts/script/<slug>/cover.png"
```

O renderizador nomeia por sequência, e um `.slide` só renderiza como `1.png`,
daí o rename. Ele renderiza em `sketch/` e a capa pronta é movida para fora,
então um rename que falha deixa um `1.png` perdido no material de trabalho, e
não ao lado das entregas.

Mostre o render para o usuário. Correção edita o HTML e renderiza de novo:
`sketch/` é material de trabalho e a raiz do slug só guarda o que é publicado.
As entregas dá para gerar de novo, nunca são versionadas como `v<N>`.

O rascunho em `edit/<slug>/` pode ser descartado.

## Mapa

| Peça | Onde |
|---|---|
| Features | `assets/features/*.md` |
| Modos | `assets/modes/*.md` |
| CLI do insert de notícia | `assets/news_insert.py` + `assets/README.md` |
| Render | `assets/render_vertical.py` (nome legado, não força 9:16) |
| Imagens de notícia | `video/inputs/<slug>-imagens/` (manual ganha) |
| Engine | `~/.claude/skills/video-use/` |

Memória da sessão: `<edit>/project.md` (formato da `video-use`).
