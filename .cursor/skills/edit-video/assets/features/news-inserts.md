---
id: news-inserts
phase: overlays
---

# Feature · Inserts de notícia / referência

## O que faz
Uma imagem de referência aparece como um **card flutuante**, composto direto por
cima do vídeo: ele **não** redimensiona nem corta o talking-head, o frame inteiro
fica exatamente como foi gravado. O card fica **centralizado na zona do terço
inferior** (não colado na borda de baixo) por **alguns segundos, enquanto a VO
fala daquele assunto**, e depois some. Ele não precisa ficar até o próximo
assunto começar, e trechos sem card nenhum entre um insert e o outro são
normais. Pop de escala (leve overshoot) + fade rápido na entrada, sincronizado
com o click do `pop-it` (§3), e fade suave na saída. Um Ken Burns discreto
dentro do card enquanto ele segura. Opcional: um chyron `FONTE: …` no canto do card.

Usos:

- modo `news`: 2–5 imagens específicas ao longo da peça (anúncio, benchmark,
  specs, plataforma citada), cada uma um card curto no momento em que a VO
  menciona o assunto.
- modo `authority` (opt-in): prova visual da tese: o screenshot de um
  **paper**, um artigo, o lançamento de um modelo ou biblioteca, uma figura de um
  estudo.

Script: `assets/news_insert.py` (ProRes 4444 com alpha, canvas inteiro,
transparente fora do card). O canvas é passado por `--width`/`--height`,
**sempre o output real da fonte** (com a rotação aplicada, não o
`width`/`height` cru do stream. O `render_vertical.py` imprime `canvas: WxH` no
começo do render, use esse valor), nunca um valor fixo. A CLI está em
`assets/README.md`.

## Como rodar

### 1. Beats + janelas
Lendo o `takes_packed.md`, localize toda menção a algo que mereça prova visual
(nome de produto, afirmação de benchmark, plataforma citada etc.) e o intervalo
de palavras em que isso é dito. Mapeie o **início** desse intervalo na timeline
de output: é ali que o card nasce. **Duração curta: 4–7s por card**, não o beat
inteiro. Não precisa cobrir 100% da peça. Trechos sem card são normais e
esperados. Localize também o **CTA**: dali em diante nenhum card entra (frame
limpo para o fecho).

### 2. Imagem de cada card
- **Manual ganha.** Olhe em `video/inputs/<slug>-imagens/` por `01.<ext>`,
  `02.<ext>`… (`.png/.jpg/.jpeg/.webp`, com ou sem o zero na frente). Se
  existirem, use sem questionar.
- **Se não, procure por conta própria.** Uma imagem por card, específica do que
  está sendo dito naquele ponto. Não repita a mesma imagem de capa genérica na
  peça inteira. Um screenshot do anúncio, um model card, um gráfico de
  benchmark, a página da plataforma citada: cada trecho técnico ganha a própria
  prova visual quando a fonte primária oferece uma. Um screenshot real do site
  oficial (pelo browser, recortado na seção relevante) ganha de qualquer imagem
  de capa genérica em especificidade. Query em inglês → `WebSearch`/browser →
  recorte com `zoom` (`save_to_disk: true`) → copie para a pasta (`0N.png`) →
  inspecione com `Read`. Critérios: bate com *aquele* momento? Fica legível no
  card? Sem marca d'água? Nenhuma imagem > imagem errada. Evite stock genérico.
- **Reporte** ao usuário, antes de renderizar, qual imagem cobre qual momento e
  de onde cada uma veio.

### 3. Gerar os cards + pop-it
Um clipe por card:

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/news_insert.py \
  --image "video/inputs/<slug>-imagens/01.png" \
  --out "<edit>/animations/slot_news_01" \
  --duration 6 --source "openai.com" --fit contain \
  --width 2160 --height 3840
```

- `--width`/`--height`: o output real da fonte, tirado da linha `canvas:` que o
  `render_vertical.py` imprime, não um valor fixo.
- `--fit contain` (o padrão, e o preferido quase sempre): a imagem inteira cabe
  dentro do card, sem cortar nada. O fundo do card é branco, e a maioria dos
  screenshots de site já tem fundo branco ou claro, então o letterbox do
  `contain` costuma ficar invisível em vez de parecer espaço vazio.
- `--fit cover`: só quando a sobra cortada nas bordas é garantidamente vazia (um
  logo isolado, uma foto com bastante ar em volta). Teste antes: se a imagem tem
  texto indo até a borda (um título de página muito largo, por exemplo), o
  `cover` corta o texto. Use `contain`.
- `--source`: chyron mono no canto do card. Omita para um insert limpo.

**Pop-it (click de áudio no pop):** no render (`render_vertical.py`), passe
`--pop-it`: ele mixa um click (`assets/sfx/click.wav`) no `start_in_output` de
cada overlay, sincronizado com o pop de escala que o `news_insert.py` já desenha
nos primeiros ~150ms do clipe. Não precisa gerar nada separado para isso, é uma
flag de render. Ver `pop-it.md` para o SFX em si.

### 4. Posicionar no EDL
Cada card entra em `overlays` com `start_in_output` = o início do momento e
`duration` = 4–7s (não precisa ser contíguo com o próximo, trechos vazios são
esperados). Não existe mais o campo `band` em `ranges`: o talking-head nunca é
redimensionado, então os `ranges` do EDL não precisam de nada especial para esta
feature.

> Screenshot de terceiro: o chyron dá o crédito da fonte, e o usuário decide o
> que publicar. Aponte qualquer dúvida sobre direito de uso.

## Calibração
Canvas = o output real da fonte, sempre recalculado (nunca hardcoded, isso já
foi um bug: um overlay gerado em 1080×1920 fixo e composto sobre uma fonte 4K
apareceu com 1/4 do tamanho, cobrindo só o canto). Card: margem lateral de ~8%
do canvas de cada lado, altura máxima de ~70% do terço inferior (assim ele mantém
ar em cima e embaixo e nunca gruda na borda de baixo), cantos arredondados + uma
sombra suave para separar do vídeo atrás. **A imagem dentro do card também
entra com cantos levemente arredondados, nunca quadrada**: um print de canto
reto dentro do card arredondado fica com cara datada. O `news_insert.py` já faz
isso sozinho (mesmo raio do card, `RADIUS_FRAC`). Se algum dia uma imagem for
composta por outro caminho, arredonde os cantos do mesmo jeito (nunca existe uma faixa opaca cobrindo o
vídeo: o resto do frame fica visível o tempo todo, inclusive atrás e em volta do
card).

## Histórico
Esta feature teve duas versões anteriores: (1) um burst opt-in por beat sem
controle de canvas (o bug da imagem minúscula), e (2) uma faixa inteira no
terço superior, persistente até o CTA, com o talking-head redimensionado para
caber embaixo dela. As duas foram abandonadas: na v2 o usuário achou irritante
redimensionar o vídeo sem motivo, e a faixa persistente ficava na tela tempo
demais sem o assunto correspondente. A versão atual (card flutuante, curto, sem
redimensionar nada) é a definitiva até chegar feedback novo.
