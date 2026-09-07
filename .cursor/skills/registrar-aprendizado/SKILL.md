---
name: registrar-aprendizado
description: >
  Records what went wrong in a recording session into content-routines/aprendizados.md,
  grouped under the date of the last Saturday (inclusive — if it runs on a Saturday,
  that Saturday counts). Saturday's first step reads that file back, so the next batch
  doesn't repeat the mistake.
  Activate with "/registrar-aprendizado", "registrar aprendizado", "log this learning",
  or whenever the user reports something that went wrong in a recording or editing session.
---
## Record a recording-session learning

Purpose: capture the user's observations about what went wrong in a session and file them in
`content-routines/aprendizados.md` under the session's Saturday, so the first step of
[saturday.md](../../../content-routines/default/saturday.md) surfaces them before the next batch.

Zero friction: the user dumps the observation, this skill dates it, phrases it as a rule and files it.
Don't ask questions before saving.

---

## Step 1 · Get the observations

They usually come with the invocation ("/registrar-aprendizado the teleprompter was too far away").
If the invocation is bare, ask once: *"O que deu errado nessa sessão?"* — then proceed.

## Step 2 · Compute the session's Saturday

Inclusive — running on a Saturday files under that same Saturday:

```bash
date -d "-$(( ($(date +%u) + 1) % 7 )) days" +%F
```

## Step 3 · Write the entry

One bullet per distinct mistake, in English (repo convention). Each bullet is
**what happened → the rule that prevents it**, one line, imperative. No preamble, no sympathy.

- ❌ "The audio was bad because the mic was far away and this hurt the edit."
- ✅ "Lav mic ended up under the collar — clip it outside the shirt, check 10s of audio before recording all 5."

## Step 4 · File it in `content-routines/aprendizados.md`

Newest Saturday first, directly below the `<!-- new entries go directly below this line -->` marker.

- Heading for that Saturday already there → append the bullets to it.
- Not there → create `## YYYY-MM-DD (sábado)` right below the marker, with the bullets under it.

Leave everything else in the file untouched.

## Step 5 · Confirm in one line

> Registrado em 2026-08-29: 2 aprendizados.

---

## Out of scope

- Doesn't touch Notion, the scripts, or the videos.
- Doesn't edit or reword past entries.
- Doesn't grade the session or offer encouragement — it files the rule and stops.
