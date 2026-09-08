---
id: authority
aliases: [pedagogical, teaching, thesis, teach]
status: ready
---

# Modo · authority

Tom pedagógico + de autoridade: ensinar guardrails, harnesses, evals,
mecanismos.

Estado da implementação: `plate_effects` existe no `render_vertical.py` (cobre
`zoom-emphasis` e `black-and-white`, com autoteste em
`assets/test_plate_effects.py`), e `news-inserts` / `news_insert.py` também.
Só falta o `motion_terco.py`, que é **opt-in** e não trava o modo: sem ele, o
beat de diagrama cai no julgamento padrão do terço (vazio, ou um insert de
referência).

`pop-it` hoje é só o SFX de click (`--pop-it`, amarrado ao início de cada
overlay). O micro-zoom visual da spec ainda não existe.

## Features (ordem)

1. `cut-dead-air` → `assets/features/cut-dead-air.md`
2. `zoom-emphasis` → `assets/features/zoom-emphasis.md`        *(plate)*
3. `black-and-white` → `assets/features/black-and-white.md`    *(plate)*
4. `pop-it` → `assets/features/pop-it.md`                      *(plate + SFX)*
5. `motion-third` → `assets/features/motion-third.md`          *(overlays · opt-in)*
6. `news-inserts` → `assets/features/news-inserts.md`          *(overlays · opt-in)*
7. `loudnorm` → `assets/features/loudnorm.md`

`subtitles` não está listada porque vai junto em todo modo: queimada só no
render final (`assets/features/subtitles.md`).

Nem todo beat usa toda feature: o modo **habilita** o vocabulário, e o editor
escolhe por beat (push lento na tese, P&B na imitação, pop-it na lista, motion
no diagrama, print de paper na citação). Sem beat = nenhum efeito emitido.

### Terço superior: julgamento, não grade fixa
No `news`, a exposição do terço é relativamente previsível (insert quando a
notícia é citada → some no CTA). Aqui **não**: o editor decide **a cada
momento** se a ênfase vai para o diagrama (`motion-third`), para uma **imagem
de referência** (`news-inserts`) ou para o rosto/plate (zoom, P&B, pop-it, ou
nada). Na dúvida, deixe o terço vazio. Veja “Julgamento editorial” em
`motion-third.md`.

Dois tipos de conteúdo no mesmo slot (nunca ao mesmo tempo):

| Tipo | Feature | Quando |
|---|---|---|
| Diagrama / fluxo animado | `motion-third` | A fala ensina um mecanismo que ganha com um visual estruturado |
| Print estático (paper, artigo, lançamento) | `news-inserts` | A fala **cita** uma fonte concreta e o print ancora a afirmação |

**Inserts de referência (opcional, mesma engine do modo news).** Normalmente: o
print de um paper, de um artigo, do anúncio de um modelo ou biblioteca, uma
figura de um estudo. Mesmo pipeline: `news_insert.py`, a pasta
`video/inputs/<slug>-imagens/`, um chyron `FONTE:` onde fizer sentido. Some no
CTA.

Exemplo: no meio de um Reel sobre guardrails você diz

> “Fazer afirmações negativas polui o workspace global da IA, como esse paper
> da universidade X mostrou”

→ o terço superior com o print do paper (título/autores/figura legíveis),
enquanto a fala segue. Não é notícia quente, é **evidência visual** para a tese
pedagógica.

## Quando usar
Conteúdo que ensina um mecanismo (guardrails, evals, harnesses, pipelines) com
voz de autoridade, e não notícia pura (isso é `news`). Citar um paper ou um
lançamento dentro da aula continua sendo `authority` + `news-inserts`.
