# Registrar um modo

Este arquivo é o contrato para transformar um estudo de Reel, Short ou TikTok num modo novo do pipeline. O estudo chega pronto, numa pasta. Quem assiste o vídeo e separa os cortes é a skill externa (assistente miya, fora deste repositório). Aqui o trabalho é ler essa pasta e registrar a gramática no nosso formato.

Não registre o estudo como cópia do vídeo. O modo descreve como editar. A peça continua sendo do Pedro, na identidade Miyakodo.

Antes de escrever, leia `modos/sem-gravacao/MODE.md` e `modos/gravacao/MODE.md`. Os dois são o formato. Um modo novo é outra pasta no mesmo lugar.

## Contrato da pasta de estudo

A pasta não entra em `modos/` e não entra no git. O vídeo de referência, se ficar na máquina, vai para `video/inputs/`. MP4 nesse caminho já está no `.gitignore`.

```text
estudo/<nome>/
  STUDY.md
  frames/
  transcricao.json
```

`STUDY.md` descreve o vídeo edição por edição, no relógio da transcrição, em segundos.

```markdown
# Estudo

Fonte: plataforma e URL, ou o nome do arquivo local
Criador: nome de quem publicou o vídeo de referência
Duração: segundos
Formato: 9:16 ou o que for

## Edições

### 1. 0.00 a 1.40

Quadro: o que está na tela (pessoa, texto, tela, split)
Corte: seco, zoom, punch-in, ou o que o frame mostrar
Legenda: onde senta e quantas palavras cabem
Motion: o que entra e como
Função: gancho, prova, lista, história, CTA, ou outra função do plano
Frame: frames/001.jpg
```

Cada edição aponta um frame em `frames/`. O nome do arquivo carrega a ordem ou o timestamp (`001.jpg`, `001-0.00.jpg`). O frame serve para ver o corte. Ele não vira asset do modo.

`transcricao.json` é uma lista no mesmo relógio:

```json
[{"text": "palavra", "start": 0.0, "end": 0.32}]
```

`start` e `end` em segundos. Sem esse arquivo, sem os frames ou sem o `STUDY.md`, o estudo está incompleto. Não invente o corte que falta.

## Passo a passo

1. Leia o `STUDY.md`, os frames e a transcrição inteiros. Separe a gramática (ritmo, duração dos planos, troca entre pessoa e motion, lugar da legenda, função de cada edição) do que é do outro criador (cor, fonte, logo, música, figurino gráfico, texto, rosto).
2. Escolha o slug em kebab-case, sem acento, diferente dos modos já registrados.
3. Para cada edição, escolha um layout que já existe e um `scene.type` que já existe. Anote a escolha ao lado da edição. A lista está no fim deste arquivo.
4. Se nenhuma combinação conta o plano, escreva qual edição não coube e por quê. Só então crie layout ou `scene.type` novo. Preferir o que já existe é a regra. Criar é a exceção, com o motivo no `MODE.md`.
5. Crie `modos/<slug>/MODE.md`. O frontmatter é o que `pipeline/registry.py` lê. `cli.py` e `compile.py` despacham o `mode` do roteiro por esses campos. Não há segunda lista no código. A pasta com `MODE.md` válido passa a ser um modo.
6. No corpo, use as seções `Quando usar`, `Entradas`, `Layouts`, `Legenda`, `Ritmo de corte`, `Motion` e `O que reaproveita`. O registro recusa o arquivo se uma delas faltar.
7. Escreva `examples/<slug>.json` com conteúdo do Pedro. O texto do criador de referência não entra no exemplo. Se o modo for `media: bruto` e não houver talking head do Pedro, use `footage.still` em `assets/pedro-frame.jpg` para o exemplo fechar sem o MP4 de outra pessoa.
8. Rode o checklist de validação abaixo.

### Frontmatter

`true` e `false` em minúsculo. Listas com `- `. O `slug` tem de ser o nome da pasta.

| Campo | Valores | O que despacha |
|---|---|---|
| `layouts` | lista | layouts aceitos no beat |
| `default_layout` | um item de `layouts` | beat sem layout |
| `validate_tone` | `true` ou `false` | se `tone` tem de estar na paleta |
| `caption_profile` | `faixa`, `gravada` ou `duas-vozes` | tamanho do grupo e a classe da legenda |
| `caption_max_words` | inteiro | teto de palavras |
| `caption_max_chars` | inteiro | teto de caracteres |
| `caption_max_duration` | número, em segundos | teto de duração do grupo |
| `caption_merge_orphans` | `true` ou `false` | palavra solta volta para o grupo vizinho |
| `caption_anchor` | `faixa` ou `layout` | posição da placa |
| `caption_top` | inteiro, só com `faixa` | `top` fixo, em px |
| `caption_tops` | mapa layout para px, só com `layout` | um `top` por layout do modo |
| `media` | `voz` ou `bruto` | como a faixa entra |
| `whoosh_on_change` | `true` ou `false` | whoosh a partir do segundo beat |
| `avatar` | `true` ou `false` | avatar do Pedro e o movimento dele |
| `grain` | `true` ou `false` | grão de papel |
| `scene_wrapper` | `wash` ou `plain` | cena com tom e fade, ou corte seco |
| `boxes` | `faceless`, `recorded` ou `studio` | qual catálogo de caixas o layout usa |

`media: voz` copia a faixa, mede a boca e não pede footage. `media: bruto` corta silêncio interno acima de cerca de 0,28 s, com respiro de 0,05 s nas bordas, e exige `footage.src` ou `footage.still`.

`scene_wrapper: wash` pinta o tom e faz a cena entrar em 0,16 s. `plain` é o corte seco, sem wash.

`caption_profile: faixa` agrupa curto e marca ênfase, strong e CTA em itálico Instrument Serif. `gravada` agrupa um pouco maior, manda ênfase para o verde, strong para a pílula dark brown e CTA para a pílula laranja. `duas-vozes` fica numa linha, com itálico na ênfase, logo inline e a palavra seguinte borrada.

Campo que o registro não conhece, ou valor fora dessas listas, faz o modo inteiro falhar ao carregar. Para um perfil, um wrapper ou uma caixa que ainda não existem, altere `pipeline/registry.py` e o ponto do pipeline que desenha isso (`compile.py`, `compose.py`, `captions.py` ou `cli.py`). Escreva no `MODE.md` qual edição do estudo exigiu a extensão.

## Regras fixas

- Remapeie sempre para `design/identity.md`. Cores: off-white `#f6f4ee`, cinza `#aba199`, dark brown `#280e03`, verde `#1a3010`, e as de apoio `#b6cadb`, `#c1c167`, `#d39ca7`, `#db3c05`. Fontes: Instrument Serif no título, Poppins na interface. Logo: o horizontal dark brown.
- A pessoa na tela é o Pedro. No modo sem bruto, o avatar de `pipeline/avatar.py`. No modo com bruto, o talking head dele, ou o still `assets/pedro-frame.jpg`. Carlos só entra como público, pelo `scene.type` `carlos` ou `versus`.
- Copie a gramática de edição. Ritmo de corte, duração dos planos, alternância entre pessoa e motion, lugar da legenda, punch-in e a função de cada beat.
- Não copie a arte gráfica, a música nem o conteúdo de outro criador. A cama sonora continua `assets/bed.wav`, ou uma faixa que o Pedro tenha. O roteiro do exemplo é texto dele.
- Prefira layouts e `scene.type` existentes. Crie um novo só quando o estudo não couber nos de baixo, e registre o motivo.
- MP4, render e cache ficam de fora do git. O `.gitignore` já cobre `video/inputs/**/*.mp4`, `video/outputs/`, `video/projects/**/*.mp4`, `video/projects/**/.hyperframes/`, `video/projects/**/.transcode-cache/`, `video/projects/**/renders/` e `video/projects/**/snapshots/`. Não coloque MP4, frame de terceiro nem cache dentro de `modos/`.

## Layouts e cenas que já existem

`boxes: faceless`, caixas em `LAYOUT_SPOTS`: `guide`, `center`, `corner`, `hero`, `pip`, `full`.

`boxes: recorded`, caixas em `RECORDED_BOXES`: `split`, `motion`, `creator`.

`boxes: studio`, caixas em `STUDIO_SPOTS`: `painel` (poço arredondado, cabeça do avatar vazando), `full`, `hero`.

`scene.type`: `timeline`, `mockup`, `counter`, `diagram`, `chat`, `code`, `phone`, `grid`, `scanline`, `folders`, `bullets`, `quote`, `badge`, `stack`, `statement`, `carlos`, `versus`, `vidro`, `alca`.

`vidro` é o card translúcido com rótulo em serif itálico. `alca` é o card com alças de seleção. `duas-vozes` é a legenda de uma linha, com itálico na ênfase, logo inline na lista `logos` e a palavra seguinte borrada. `chapter: true` pede um flash, no teto de quatro a cada 69 s.

`stack` recebe `children`. Os outros leem `title`, `items`, `lines`, `messages`, `value`, `label`, `text`, `filename`, `handle`, `comment`, `dm`, `center`, `root`, `kicker`, `kind` ou `scan`, conforme o tipo. O que não vier usa um miolo pequeno.

## Checklist de validação

Na raiz do repo, com `<slug>` no lugar do modo novo:

```bash
python3 -m unittest discover -s .agents/skills/produzir-video/tests -v
python3 .agents/skills/produzir-video/pipeline/cli.py build .agents/skills/produzir-video/examples/<slug>.json
python3 .agents/skills/produzir-video/pipeline/cli.py render video/projects/<slug> --output video/outputs/<slug>.mp4 --quality draft
```

O `unittest` tem de passar, inclusive o erro de modo desconhecido e a estabilidade de `sem-gravacao` e `gravacao`.

O `build` grava `video/projects/<slug>/` com `index.html` e `meta.json`. O `render` grava o MP4 em `video/outputs/`. Abra um frame do render e confira paleta, fonte, logo e o Pedro (avatar ou rosto). Arte, música e texto do criador de referência não aparecem.

`git status` não lista MP4, render nem cache. Não publique o vídeo.
