---
id: subtitles
phase: render
---

# Feature · Legendas do vídeo

## O que faz
Queima as legendas no vídeo (não depende da legenda automática do Instagram).
Três coisas definem o visual:

- **Sentence case**, como foi transcrito. Maiúscula só onde a língua pede:
  nomes, siglas, começo de frase. Nunca um `.upper()` geral.
- **Trechos curtos que se substituem**, como a legenda padrão do Instagram: até
  quatro palavras e duas linhas por vez, e o trecho seguinte entra no lugar do
  anterior.
- **A fonte do Alvinegro**: Bricolage Grotesque ExtraBold.

O arquivo é `<edit>/master.ass`, **ASS, não SRT**: o ASS carrega o próprio
estilo (fonte, sombra, margem) dimensionado para o canvas real, sem
`force_style`.

A timeline é a timeline de **output** (depois dos cortes de tempo morto).

Hard Rule 1 do `video-use`: as legendas entram por **último** no composite, e
nenhum overlay pode cobrir elas.

## Ligadas por padrão, só no render final

Todo modo sai com legendas queimadas. **Mas elas só são queimadas no render
final**, nunca num preview.

O motivo é custo, não gosto. Montar o `master.ass` é barato (ele lê as
transcrições cacheadas do disco), mas queimar pelo libass força um re-encode
completo do composite, e os previews existem para serem re-renderizados uma
dúzia de vezes enquanto o cut ainda está mudando. Legendas em toda iteração
encareceriam cada rodada por um output que ninguém está lendo ainda.

| Render | Legendas |
|---|---|
| `--preview` (iteração) | **nunca**: sem `--subtitles`, sem `master.ass` |
| `final.mp4` (depois do "pronto") | **sempre**, a não ser que o usuário tenha desligado |

O usuário desliga dizendo isso ("sem legenda", "sem legendas", "pula as
legendas"). Aí o final renderiza como um preview: sem `subtitles` no EDL, sem
`--subtitles`, sem `master.ass`.

As palavras queimadas são as que já foram aprovadas nos previews, então não tem
nada para revisar duas vezes: o cut fecha antes de as legendas existirem.

## O estilo

O `master.ass` sai com um bloco `[V4+ Styles]` com uma entrada só, `BODY`, usada
em toda cue. Todo tamanho é escrito como fração da altura real do output, e
`PlayResX/Y` é o canvas real, então os mesmos números valem seja qual for a
resolução que o celular gravou.

| Estilo | Fonte | Visual |
|---|---|---|
| `BODY` | Bricolage Grotesque ExtraBold | Branco, **sem contorno**: uma sombra projetada é a única separação da imagem. |

O `BODY` rodar sem contorno é uma escolha deliberada, e é o único ajuste que
depende da imagem: branco sobre uma parede estourada ou uma camisa branca
sobrevive só com a sombra, mas por pouco. Se um take for claro o bastante para
perder o texto, aumente `Shadow` antes de recorrer a `Outline`: a borda preta é
o que fazia as legendas antigas parecerem geradas automaticamente.

**Fonte.** A Bricolage não está instalada no Windows. O TTF fica em
`assets/fonts/` e o renderer copia ele para `<edit>/fonts/`, que é passado
como `fontsdir=fonts`, relativo, porque um caminho absoluto do Windows quebra o
argumento do filtro nos dois-pontos do drive. Se uma legenda sair numa sans de
fallback, foi essa cópia que falhou.

## Como rodar

No render final, não antes:

1. No `edl.json`, declare `"subtitles": "master.ass"` (caminho relativo a
   `<edit>/`).
2. Rode o renderer **com** `--subtitles`. Ele monta o `master.ass` a partir das
   transcrições + ranges e queima via libass:

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/render_vertical.py \
  "<edit>/edl.json" -o "<edit>/final.mp4" --subtitles
```

O gerador quebra a fala em trechos curtos (quebra na pontuação, a cada quatro
palavras ou antes de uma terceira linha). Use os trechos como vieram.

O renderer só monta o `master.ass` quando ele não existe. Um existente é
reaproveitado como está, então uma correção feita à mão sobrevive aos
re-renders. Para recomeçar do zero a partir das transcrições, apague o arquivo.

## Onde fica o limite
O assunto é sério, e as legendas carregam a seriedade. Sem pop de palavra estilo
karaokê, sem bounce, sem cor ciclando por palavra, sem emoji.

`\t` (transformações animadas) e `\fad` funcionam no ASS e não são usados de
propósito. Se algum Reel um dia precisar de movimento numa palavra, isso é uma
decisão sobre o sistema: entra neste arquivo primeiro, com orçamento, ou não é
usado.

## Autoavaliação
No final (os previews não têm legenda para conferir):

- **Caixa**: sentence case, não um paredão de maiúsculas.
- **Fonte**: a queima está em grotesca, não numa sans de fallback. Se parece
  Arial, `<edit>/fonts/` está vazia.
- **Hard Rule 1**: nenhum overlay esconde a faixa das legendas. Se algum
  esconder, reposicione o *overlay*, nunca as legendas.

**Elas dividem o terço inferior com os cards de notícia/referência.** O bloco de
legenda fica a 31.25% da altura do frame a partir de baixo e cresce para cima
quando o trecho quebra em duas linhas. O card fica centralizado no terço
inferior com ~70% da altura dele, então sobram uns dois por cento de ar: confira
os trechos de duas linhas. Se encostarem, suba o **card** (a geometria do
`news_insert.py`), nunca desça as legendas.

Uma janela de overlay que muda aqui exige re-renderizar o final, então confira
antes de entregar o arquivo.

## Autoteste
`assets/test_captions.py` verifica que os trechos são curtos e não acumulam, que
nenhuma cue sobrepõe a seguinte, os limites da segurada na pausa e a caixa
preservada, e depois queima um frame para provar que a fonte resolve no libass:

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/test_captions.py
```
