---
id: news
aliases: [news mode, breaking news]
---

# Mode · news

Baseline (cutting + loudnorm) + reference images as a **floating card** in the
lower third, synced to the speech. This mode's rule: each card appears for a few
seconds while the VO talks about that specific subject and then goes away — it
does not have to hold until the next subject, it does not have to cover the
whole piece, and the talking-head is never resized (the card only composites on
top, it never reserves space). Every card pop comes with a click (`pop-it`). See
`news-inserts.md` for the mechanism. Burned-in subtitles like every mode, at the
final render only — the cards sit in the lower third, so check they clear the
subtitle band (`assets/features/subtitles.md`).

## Features (order)

1. `cut-dead-air` → `assets/features/cut-dead-air.md`
2. `news-inserts` → `assets/features/news-inserts.md`
3. `pop-it` → `assets/features/pop-it.md` (only the audio click on each image
   pop — `render_vertical.py --pop-it`; the plate's micro punch-in on spoken
   words is still spec, not used here)
4. `loudnorm` → `assets/features/loudnorm.md`

## When to use it
A news Reel: new model, funding round, acquisition, research. Also whenever the
user explicitly asks for `news mode`.
