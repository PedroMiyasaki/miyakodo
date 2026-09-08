---
id: cut-dead-air
phase: edl
---

# Feature · Cortar tempo morto

## O que faz
Tira os silêncios longos e os tropeços de fala do talking-head. O vídeo final
fica mais denso, e a fala continua na mesma ordem, só sem o tempo morto.

## Como rodar
Com a transcrição por palavra (`takes_packed.md` / helpers do `video-use`):

1. **Primeiro:** ache e corte todas as **notas de editor**: a instrução mais o
   take errado ao qual ela pertence. Elas não seguem uma frase fixa, então leia
   procurando a intenção, não um marcador. As notas orientam outras features,
   mas **não** ficam no vídeo final (ver a seção de notas de editor da
   `SKILL.md`).
2. Marque os silêncios ≥ ~1.0s e os tropeços de fala.
3. Corte em **fronteira de palavra**, com padding na janela de 30–200ms.
4. Preserve as pausas dramáticas quando forem intencionais (não corte tudo que
   por acaso é silêncio).
5. Materialize os cortes como `ranges` no `edl.json` (formato do `video-use`).

Nunca corte dentro de uma palavra (Hard Rule do `video-use`).
