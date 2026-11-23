---
name: produzir-video
description: Produz um Reel 9:16 da Miyakodo em um de dois modos. sem-gravacao monta avatar do Pedro, a voz dele e motion graphics. gravacao parte de um talking head gravado, corta silêncio e anima por cima. Ative com "produz o vídeo", "modo sem gravação", "modo gravação", "monta o reel" ou "usa produzir-video".
---

# Produzir vídeo

Um único pipeline. O roteiro JSON escolhe o modo, a voz, os beats e as cenas. O código em `pipeline/` gera uma composição HyperFrames 1080×1920. As skills `hyperframes*` continuam sendo o motor de render. Não há segundo gerador, nem Remotion, nem o fluxo antigo de `editar-video`.

Peças antigas em `video/projects/` (anteriores a este pipeline) são arquivo do que já foi editado. Vídeo novo sai daqui.

A identidade é a de `design/identity.md`: off-white `#f6f4ee`, cinza `#aba199`, dark brown `#280e03`, verde `#1a3010`, e as cores de apoio `#b6cadb`, `#c1c167`, `#d39ca7`, `#db3c05`. Título em Instrument Serif, texto de interface em Poppins. O logo usado nas cenas é o horizontal dark brown.

Os modos não copiam o visual dos reels de referência. Eles emprestam só a lógica: no sem gravação, o avatar do Pedro conduz um quadro que corta a cada poucos segundos; na gravação, o talking head alterna com motion e leva um punch-in no CTA. As cenas servem opinião, notícia, lista, história, tutorial ou CTA. O campo `purpose` registra a intenção e não trava o visual.

## Quando usar cada modo

| Modo | Pedro grava? | O que entra | O que sai |
|---|---|---|---|
| `sem-gravacao` | Não | Roteiro + faixa de voz | Avatar do Pedro, legendas numa faixa própria, cortes entre layouts |
| `gravacao` | Sim | Roteiro + vídeo bruto + voz (a do bruto, ou a mesma janela) | Talking head com jump cut de silêncio, overlays em split, tela cheia ou punch-in |

`sem-gravacao` quando não há gravação nova e a peça pode ser carregada pela voz e pelo desenho. `gravacao` quando existe talking head e as animações entram por cima da pessoa.

## Entradas

Arquivo JSON. Tempos do `voice`, dos `beats` e das `words` usam o relógio do arquivo de voz, em segundos.

- `mode`: `sem-gravacao` ou `gravacao`.
- `slug`, `title`.
- `purpose`: `tutorial`, `opiniao`, `noticia`, `lista`, `historia` ou `cta`.
- `voice.src`: caminho a partir da raiz do repo. `voice.in` e `voice.out` recortam a janela.
- `words`: opcional. Lista `{text, start, end}` alinhada à voz. Sem isso, o pipeline reparte `lines` de cada beat pela duração.
- `emphasis`, `strong`, `cta`: listas de palavras. No sem gravação, as três viram itálico em Instrument Serif. Na gravação, `emphasis` vai para o verde, `strong` para uma pílula dark brown e `cta` para uma pílula laranja.
- `beats`: `{start, end, layout, label, scene, tone}`. `tone` vale `paper`, `ink`, `verde`, `azul`, `rosa` ou `oliva`. No sem gravação o padrão é `paper`.
- `footage` (só `gravacao`): `src` de um mp4 no mesmo relógio da voz, ou `still` para o pipeline fabricar um plano a partir de uma foto. O mp4 e a voz são fatiados com o mesmo `in`/`out`.

Layouts de `sem-gravacao`, todos dentro da área segura do Reels (abaixo da faixa de legenda, acima do rodapé da legenda do post, longe da coluna de botões à direita):

- `hero` e `center`: frase curta em cima, busto grande embaixo.
- `guide`: Pedro à esquerda, cena à direita.
- `pip` e `corner`: a cena ocupa o miolo e o busto fica pequeno, acima do rodapé.
- `full`: a cena toma a área segura e o avatar sai.

A troca é corte. A legenda fica numa placa off-white, entre o topo da interface e o começo da cena, e não cobre avatar nem texto de cena.

Layouts de `gravacao`: `split` (pessoa embaixo, cena em cima), `motion` (pessoa some, a cena ocupa o quadro), `creator` (pessoa em tela cheia, com punch-in se `punch` não for false). A troca é corte seco. Silêncios internos acima de cerca de 0,28 s saem, com um respiro curto nas bordas para não comer consoante.

### Cenas

O campo `scene.type` aceita: `timeline`, `mockup`, `counter`, `diagram`, `chat`, `code`, `phone`, `grid`, `scanline`, `folders`, `bullets`, `quote`, `badge`, `stack`, `statement`, `carlos`, `versus`.

`statement` é o letreiro grande (`text` ou `lines`, `kicker` opcional). `carlos` coloca o mascote de `design/mascote-e-textura/` (`pose`: `squat`, `boss`, `money`, `coffee`, `stars`) sempre que a cena for o público, o empresário ou a pessoa com quem o Pedro fala. `versus` divide pessoa e agente. Se `pose` vier, o Carlos entra na coluna da pessoa.

`stack` recebe `children`, cada um com o próprio `type`. Os outros tipos leem `title`, `items`, `lines`, `messages`, `value`, `label`, `text`, `filename`, `handle`, `comment`, `dm`, `center`, `root`, `kicker`, `kind` ou `scan`, conforme o caso. O que não vier usa um miolo pequeno, para o componente não quebrar.

Cada cena entra com pop elástico e dispara um efeito (pop, whoosh, click, typing, notification, chime, impact, key). A cama sonora é `assets/bed.wav`, um tom baixo gerado, trocável por uma faixa real no mesmo caminho do projeto.

## Saídas

`pipeline/cli.py build` grava `video/projects/<slug>/`:

- `index.html`, `hyperframes.json`, `package.json`, `meta.json`
- `assets/voice.wav`, `assets/bed.wav`, fontes, logo, gsap e os sfx usados
- no modo gravação, `assets/footage.mp4` já com os jump cuts

O render não entra no build. Ele é um comando separado e grava o mp4 no caminho pedido. A pasta `video/outputs/` segue no gitignore.

## Gravação longa e o bruto de evals

O pipeline transcodifica o bruto para H.264, 1080×1920, 30 fps, antes dos cortes. HEVC e 60 fps entram do mesmo jeito. Se o arquivo vier em HLG ou BT.2020, como o iPhone, a imagem é convertida para SDR BT.709. O render usa `--sdr` para não cair no caminho HDR. A cama sonora é repetida até cobrir a duração. O teto de efeitos sobe com o tamanho da peça, até 80.

O mp4 original de evals não entra no git (passa de 100 MB). Ele está no release `footage-evals`:

```bash
mkdir -p video/inputs/evals
gh release download footage-evals --repo PedroMiyasaki/miyakodo -p evals.MP4 -D video/inputs/evals
```

O arquivo esperado é `video/inputs/evals/evals.MP4` (sha256 `bd6cdc1abcca5e8d672476c7bd86ae4f10918c9ac316c8eba330ed43b1d222fe`). `video/inputs/` já está no gitignore. O `footage.mp4` gerado em `video/projects/` também, pela regra `video/projects/**/*.mp4`.

O roteiro da peça inteira é `examples/evals-gravacao.json`. Voz e imagem são o mesmo arquivo, janela 0 até 209,533 s.

```bash
python3 .agents/skills/produzir-video/pipeline/cli.py build .agents/skills/produzir-video/examples/evals-gravacao.json --out video/projects/evals-gravacao
python3 .agents/skills/produzir-video/pipeline/cli.py render video/projects/evals-gravacao --output video/outputs/evals-gravacao.mp4 --quality looks
```

`video/projects/evals-gravacao/cortes.json` lista os silêncios removidos e as cenas na timeline já cortada.

## Comandos

Na raiz do repo:

```bash
python3 .agents/skills/produzir-video/pipeline/cli.py build .agents/skills/produzir-video/examples/sem-gravacao.json
python3 .agents/skills/produzir-video/pipeline/cli.py build .agents/skills/produzir-video/examples/gravacao.json

python3 .agents/skills/produzir-video/pipeline/cli.py check video/projects/exemplo-sem-gravacao
python3 .agents/skills/produzir-video/pipeline/cli.py render video/projects/exemplo-sem-gravacao --output video/outputs/exemplo-sem-gravacao.mp4 --quality looks

python3 .agents/skills/produzir-video/pipeline/cli.py check video/projects/exemplo-gravacao
python3 .agents/skills/produzir-video/pipeline/cli.py render video/projects/exemplo-gravacao --output video/outputs/exemplo-gravacao.mp4 --quality looks
```

Testes do compilador, das legendas, dos cortes e de um build curto:

```bash
python3 -m unittest discover -s .agents/skills/produzir-video/tests -v
```

## Exemplos

Os dois JSON em `examples/` usam a narração real de `evals-cut-audio.m4a` e a transcrição já versionada. O sem gravação cobre o gancho (use case, evals, negócio, CTA). A gravação cobre o trecho da empresa com fornecedores e cláusulas.

O bruto `evals-cut-sdr.mp4`, citado pelo projeto antigo, não está no checkout. O exemplo de gravação gera o plano a partir de `assets/pedro-frame.jpg` (o frame do rosto que estava em `evals-reel/snapshots/final-113/face.jpg`), com a voz real na mesma janela. Um talking head novo entra em `footage.src` sem mudar o pipeline.

O avatar não é o mascote Carlos. É o Pedro desenhado no mesmo sistema do Carlos: contorno dark brown, chapado, grão de papel e a paleta de `design/identity.md`. O rosto sai do vídeo de referência (cabelo escuro com mecha cinza, sobrancelha grossa, barba curta, pinta, camiseta e lapela). A boca troca de visema pelo volume da faixa. Carlos só entra quando a cena representa o público.

A narração de Headless Software está no release `footage-headless-software`, arquivo `headless-software.MP4` (sha256 `7da8c5295e52addbf88c5bc741fbf2b28418c00fe4b52ebc63ee6eba3867304d`). O mp4 não entra no git.

```bash
mkdir -p video/inputs/headless-software
gh release download footage-headless-software --repo PedroMiyasaki/miyakodo -p headless-software.MP4 -D video/inputs/headless-software
python3 .agents/skills/produzir-video/pipeline/cli.py build .agents/skills/produzir-video/examples/headless-software.json --out video/projects/headless-software-sem-gravacao
python3 .agents/skills/produzir-video/pipeline/cli.py render video/projects/headless-software-sem-gravacao --output video/outputs/headless-software-sem-gravacao.mp4 --quality looks
```

## O que este pipeline não faz

Não publica no Instagram. Não pede aprovação num plano de stills antes do render: o roteiro JSON é a direção. Não remove fundo de um vídeo arbitrário. Não clona voz. A faixa entra pronta em `voice.src`. A skill `narrar-roteiro` gera essa faixa na GPU local e entrega `words` no formato `{text, start, end}`. Se a faixa não for a do Pedro, o resultado não é a voz dele.
