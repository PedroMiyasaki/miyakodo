---
id: subtitles
phase: render
---

# Feature · Legendas do vídeo

## O que faz
Queima as legendas no vídeo (não depende da legenda automática do Instagram).
Três coisas definem o visual, e só a primeira é mecânica:

- **Sentence case**, como foi transcrito. Maiúscula só onde a língua pede:
  nomes, siglas, começo de frase. Nunca um `.upper()` geral.
- **As palavras se acumulam de duas em duas dentro de um bloco**, aí o bloco
  limpa e o próximo começa. Não é um par novo piscando a cada 400ms.
- **As fontes do Alvinegro**: Bricolage Grotesque ExtraBold para a linha,
  Newsreader itálico para a palavra em ênfase, que também inverte.

O arquivo é `<edit>/master.ass`, **ASS, não SRT**. O SRT carrega exatamente um
estilo para o arquivo inteiro, e o parser de SRT do ffmpeg descarta as tags de
override `{\...}` *em silêncio*, então a ênfase por palavra renderiza como texto
comum e você acha que funcionou. O ASS era o caminho de upgrade para onde esta
feature sempre apontou. Agora é o único caminho.

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

## Os dois estilos

O `master.ass` sai com um bloco `[V4+ Styles]` com exatamente duas entradas.
Todo tamanho é escrito como fração da altura real do output, e `PlayResX/Y` é o
canvas real, então os mesmos números valem seja qual for a resolução que o
celular gravou.

| Estilo | Fonte | Visual |
|---|---|---|
| `BODY` | Bricolage Grotesque ExtraBold | Branco, **sem contorno**: uma sombra projetada é a única separação da imagem. O padrão de toda cue. |
| `EMPH` | Newsreader itálico, 2pt maior | **Invertido**: glifo quase preto dentro de um contorno branco grosso. Lê como marca-texto sobre a imagem. |

O `BODY` rodar sem contorno é uma escolha deliberada, e é o único ajuste que
depende da imagem: branco sobre uma parede estourada ou uma camisa branca
sobrevive só com a sombra, mas por pouco. Se um take for claro o bastante para
perder o texto, aumente `Shadow` antes de recorrer a `Outline`: a borda preta é
o que fazia as legendas antigas parecerem geradas automaticamente.

O `EMPH` é o acento da marca, e a marca não tem *cor* de acento: o
`design/identity.md` diz que a inversão é o acento, e isto é inversão. Não
introduza um matiz para destacar uma palavra. O itálico serifado contra a
grotesca já é uma quebra tonal dura. Isso mais a inversão é o dispositivo
inteiro.

Troque no meio da cue com `\r<style>`:

```
Dialogue: 0,0:00:03.10,0:00:04.40,BODY,,0,0,0,,não vai\h\h{\rEMPH}substituir{\r}
```

`\rEMPH` restaura *todas* as propriedades daquele estilo, `BorderStyle`
inclusive. Nenhuma outra tag muda border style inline. `\r` sozinho volta ao
estilo da própria cue. O `\h\h` antes dele é estrutural: o contorno do `EMPH` é
grosso o bastante para engolir um espaço normal e colar as palavras.

**Fontes.** Nenhuma das duas está instalada no Windows. Os TTFs ficam em
`assets/fonts/` e o renderer copia eles para `<edit>/fonts/`, que é passado
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

3. **Passe o `master.ass` gerado pela edição abaixo**, depois rode o mesmo
   comando de novo para queimar o arquivo editado.

O renderer só monta o `master.ass` quando ele não existe. Um existente é
reaproveitado como está, então a sua edição sobrevive aos re-renders. Para
recomeçar do zero a partir das transcrições, apague o arquivo.

## A edição — a parte que tira a cara de legenda automática

O gerador é burro de propósito. Ele agrupa por pontuação, limita os blocos a
seis palavras, revela de duas em duas e quebra a linha em dezoito caracteres.
Isso é um esqueleto com o pulso certo, não uma trilha de legenda pronta. **Leia
contra o áudio e edite.** Três movimentos, em ordem de quanto cada um rende.

### 1. Reagrupe por respiração, não por contagem

Um bloco tem que ser uma unidade que alguém diria de uma vez só. Junte ou divida
os blocos do gerador até ficarem assim, e aí varie o tamanho de propósito.

| A linha faz isso | Bloco |
|---|---|
| Corre, conecta, prepara | 5–6 palavras, reveladas em três passos |
| Aterrissa, vira, contradiz | 2–3 palavras, um ou dois passos |
| **A punchline** | 1–2 palavras, sozinha, nada antes dela na tela |

A variação *é* o efeito. Um bloco de seis palavras seguido de um bloco de duas
lê como aceleração mesmo sem nada ter se movido.

### 2. Varie como o bloco se monta

Duas palavras por vez é o padrão, não uma regra, e o gerador aplica isso
uniformemente porque não consegue ouvir o take. Você consegue.

- Uma linha dita rápido pode chegar **inteira**: uma cue, sem revelar aos
  poucos.
- Uma lista pode chegar **uma palavra por passo**, cada item caindo no próprio
  beat.
- Uma virada pode **segurar a preparação e aí soltar a última palavra sozinha**,
  depois de um intervalo maior do que a fala exige.
- Uma linha pode quebrar onde a *voz* quebra, não onde os dezoito caracteres
  acabaram. Mova o `\N`.

Nada aqui é um comportamento fixo para reproduzir. Veja o que a entrega faz e
monte o bloco que combina com ela.

### 3. Dê ênfase às palavras que a entrega já acerta

Dois dispositivos, e eles se somam:

**Isolamento**: deixe a palavra sozinha no frame e segure um beat a mais do que
a fala precisa. De graça, e funciona com qualquer palavra.

**`\rEMPH`**: a inversão em itálico serifado, para a palavra que a linha inteira
existe para entregar. Orçamento: **2–4 num Reel de 45 segundos, no máximo uma
por bloco.** Mais que isso e toda palavra fica enfatizada, o que é o mesmo que
nenhuma. Uma palavra marcada `EMPH` tem que ser uma em que você se apoiaria se
lesse a linha em voz alta. Se você está procurando a segunda num bloco, a
primeira foi a escolha errada.

### 4. Segure na pausa

O gerador já estende a última cue de um bloco até 0.6s dentro do silêncio
seguinte, parando antes do próximo bloco e nunca cruzando o corte seco de um
segmento. Alongue essas seguradas onde a entrega realmente descansa, e encurte
onde a linha seguinte entra em cima. Nunca atravesse um corte.

### Onde fica o limite
O assunto é sério, e as legendas carregam a seriedade. Sem pop de palavra estilo
karaokê, sem bounce, sem cor ciclando por palavra, sem emoji. O que a gente pega
emprestado da edição viral é **ritmo e um único dispositivo de ênfase**: a
sensação de que o texto está reagindo à fala em vez de correr do lado dela.

`\t` (transformações animadas) e `\fad` funcionam no ASS e não são usados de
propósito. Se algum Reel um dia precisar de movimento numa palavra, isso é uma
decisão sobre o sistema: entra neste arquivo primeiro, com orçamento, ou não é
usado.

## Autoavaliação
No final (os previews não têm legenda para conferir):

- **Caixa**: sentence case, não um paredão de maiúsculas.
- **Ritmo**: passe o olho nos tamanhos de bloco ao longo do arquivo. **Se todo
  bloco tem seis palavras reveladas em três passos iguais, a edição não
  aconteceu.**
- **Ênfase**: conte os `\rEMPH`. Mais de ~4 num Reel de 45s é sinal de recuar.
  Zero também é um achado: um Reel sem nenhuma linha em que valha se apoiar
  costuma ser problema de roteiro, não de legenda.
- **Fontes**: a queima está em grotesca, não numa sans de fallback. Se parece
  Arial, `<edit>/fonts/` está vazia.
- **Hard Rule 1**: nenhum overlay esconde a faixa das legendas. Se algum
  esconder, reposicione o *overlay*, nunca as legendas.

**Elas dividem o terço inferior com os cards de notícia/referência.** O bloco de
legenda fica a 31.25% da altura do frame a partir de baixo e **cresce para
cima** conforme as palavras se acumulam, então um bloco de três linhas chega
mais alto que um de uma linha. O card fica centralizado no terço inferior com
~70% da altura dele. Com cues de SRT de altura fixa isso já era uns dois por
cento de ar. Com um bloco que cresce, o que você tem que conferir são as cues
acumuladas, não a primeira. Se encostarem, suba o **card** (a geometria do
`news_insert.py`), nunca desça as legendas.

Uma janela de overlay que muda aqui exige re-renderizar o final, então confira
antes de entregar o arquivo.

## Autoteste
`assets/test_captions.py` verifica a acumulação, os passos de revelação
contíguos, os limites da segurada na pausa e a caixa preservada, e depois queima
um frame para provar que as fontes resolvem e que o `\rEMPH` sobrevive ao
libass:

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/test_captions.py
```
