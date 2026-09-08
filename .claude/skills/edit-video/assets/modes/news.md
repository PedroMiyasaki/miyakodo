---
id: news
aliases: [news mode, breaking news]
---

# Modo · news

Baseline (corte + loudnorm) + imagens de referência como **card flutuante** no
terço inferior, sincronizadas com a fala. A regra deste modo: cada card aparece
por alguns segundos enquanto a fala trata daquele assunto específico e depois
some. Ele não precisa segurar até o assunto seguinte, não precisa cobrir a peça
inteira, e o talking head nunca é redimensionado (o card só compõe por cima,
nunca reserva espaço). Todo pop de card vem com um click (`pop-it`). Veja
`news-inserts.md` para o mecanismo. Legendas do vídeo queimadas como em todo
modo, só no render final. Os cards ficam no terço inferior, então confira que
eles não invadem a faixa das legendas (`assets/features/subtitles.md`).

## Features (ordem)

1. `cut-dead-air` → `assets/features/cut-dead-air.md`
2. `news-inserts` → `assets/features/news-inserts.md`
3. `pop-it` → `assets/features/pop-it.md` (só o click de áudio em cada pop de
   imagem, `render_vertical.py --pop-it`. O micro punch-in do plate nas
   palavras faladas ainda é spec, não entra aqui)
4. `loudnorm` → `assets/features/loudnorm.md`

## Quando usar
Reel de notícia: modelo novo, rodada de investimento, aquisição, pesquisa.
Também sempre que o usuário pedir o modo `news` explicitamente.
