---
id: cut-dead-air
phase: edl
---

# Feature · Cut dead air

## What it does
Removes long silences and verbal slips from the talking-head. The deliverable
gets denser; the speech stays in the same order, just without the dead air.

## How to run it
With the word-level transcript (`takes_packed.md` / `video-use` helpers):

1. **First:** find and cut every **editor note** — the direction plus the
   botched take it belongs to. They follow no fixed phrasing, so read for
   intent, not for a marker. The notes drive other features, but they do **not**
   stay in the deliverable — see `SKILL.md` § Editor notes.
2. Mark silences ≥ ~1.0s and verbal slips.
3. Cut on a **word boundary**, with padding in the 30–200ms window.
4. Preserve dramatic pauses when they are intentional (do not cut everything
   that happens to be silence).
5. Materialize the cuts as `ranges` in `edl.json` (`video-use` format).

Never cut inside a word (`video-use` Hard Rule).
