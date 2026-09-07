---
name: traduzir
description: >
  Adapts a finished piece (its final.md) into Brazilian Portuguese, following the
  pt-BR anti-pattern rules in the voice guide, and saves it alongside the
  original. Activate with commands like "traduzir", "traduz esse post",
  "translate this to pt-BR", "quero esse roteiro em português".
---

## Translation into pt-BR

Purpose: take a piece that is already finished — its `final.md` — and produce the Brazilian Portuguese version of it. The source piece is not touched.

This runs **after** a piece is done. It writes no ideas to Notion and changes no `Status` or `Format` there — that already happened when the original shipped.

---

## Required references

Read both before writing a single line:

| Reference | What to take from it |
|---|---|
| `docs/voice/base.md` § **9. Brazilian Portuguese** | The whole rule set. This is the point of the skill. |
| The source file itself | Structure, format markers, line breaks, emphasis. |

Sections 1–8 of the voice guide still apply. Section 9 stacks on top of them and wins wherever the two disagree in Portuguese.

---

## Execution protocol

### Step 1 · Find the source

Default: the piece the user just finished in this conversation.

Otherwise ask which one, or resolve from the slug they gave: **`posts/<type>/<slug>/final.md`**, where `<type>` is `script`, `carousel`, `thread`, `linkedin` or `substack`.

`final.md` is what "done" produces. If the folder holds only `sketch/v<N>.md` and no `final.md`, the piece is not finished: say so and send the user back to the skill that produces it (`write-script`, `carousel`, `write-thread`, `build-linkedin`, `write-substack`) instead of translating a draft.

### Step 2 · Adapt, don't translate

Read § 9 of the voice guide first. Then rewrite the piece in pt-BR.

**This skill carries the highest decalque risk in the repo**, because the source is English and the path of least resistance is word-for-word. § 9.6 is the section to hold in mind throughout: a sentence can be grammatically perfect and still land as English wearing Portuguese.

What that means in practice:

- A hook translated literally is a dead hook. Rebuild it so it works in Portuguese, even if the words end up different.
- Idioms get an equivalent, not a translation.
- Rhythm is part of the piece. If the English line was short and blunt, the Portuguese line is short and blunt.
- If a sentence resists adaptation, cut it and say the same thing another way.

**Keep unchanged:** proper nouns, product names, versions, numbers, technical terms that ship in English (prompt, harness, benchmark, deploy), quoted sources, links.

### Step 3 · Preserve the format

The pt-BR version is the same piece in another language, not a new piece. Whatever structure the source carries, carry it through:

- **script** — teleprompter markers (`[HOOK]`, `[PROBLEM]`, `[pause]`), line breaks, bold emphasis. The line breaks are breath marks; keep them where they fall.
- **carousel** / **thread** — slide and post boundaries, one for one.
- **linkedin** — paragraph breaks and the footer.
- **substack** — the title and subtitle at the top, the section headings, and every markdown structure the article carries: code blocks stay in the original language, tables and blockquotes keep their shape, inline links keep their targets. Translate the heading sentences; do not turn them back into labels. **Image markers keep their filenames and their positions** (`![01 — …](01.png)`) — the captures are shared with the original — but the caption text inside them is translated, source credit and all.

### Step 4 · Save

Write to `posts/<type>/<slug>/sketch/pt-br-v1.md`, in the same folder as the source.

Add a footer line recording where it came from:

```
---
pt-BR de final.md
```

The `sketch/pt-br-v<N>.md` sequence is separate from `sketch/v<N>.md` on purpose: the original stays the canonical piece, and its `final.md` stays the final one.

**Once the user confirms the translation is done, copy the highest `sketch/pt-br-v<N>.md` to `posts/<type>/<slug>/pt-br.md`.** Same rule for every type: `sketch/` holds the history, the slug root holds what gets published. A later correction to a `sketch/pt-br-v<N>.md` means re-copying it to `pt-br.md`.

### Step 5 · Iterate

Same protocol as the rest of the repo. Every user correction creates `sketch/pt-br-v<N+1>.md`: read the previous version, copy unchanged blocks **verbatim**, apply only the diff.

---

## Before handing it over

Read the pt-BR version out loud. The test in the voice guide works better in Portuguese than in English, and it catches in one pass what a checklist catches in five.

Then check the two things this skill gets wrong most often:

1. Any sentence that only makes sense if you know the English original (§ 9.6).
2. Any noun sitting there without an article or a plural (§ 9.2), which is what literal translation produces by default.
