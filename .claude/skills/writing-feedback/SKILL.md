---
name: writing-feedback
description: >
  Use when the user explicitly asks to consolidate a content session's
  accumulated writing feedback into the voice guide. Triggers: "consolidate
  this session's writing feedback", "turn this conversation's corrections into
  rules", "update the voice guide". Applies to content sessions (script,
  carousel, thread, LinkedIn) after several corrections to tone, vocabulary,
  rhythm or register. Do NOT invoke on a single mid-session correction: it runs
  once, on demand, over all corrections in the chat.
---

# Writing Feedback · Voice Guide Consolidation

## Purpose

Function: consolidate, in a single batch, the writing corrections the user made over a production session into permanent rules in the Voice Guide. Goal: keep the same mistake from coming back in future sessions.

Central constraint: run this skill **once, on demand, at the end of the conversation**, sweeping the whole session. Do not react to individual corrections during production.

## When to use

Activation condition: the user invokes it explicitly, at the end of a content production session (script, carousel, thread, LinkedIn, caption) in which they corrected tone, vocabulary, rhythm, register or structure more than once. Triggers: "consolidate this session's writing feedback", "turn this conversation's corrections into rules", "update the voice guide".

**When NOT to use:**

- Do not run it during the session, on every correction. The individual correction is already applied on the spot, inside the production skill. This skill only comes in when the user asks for the consolidation.
- Do not run it on corrections to code, analysis or internal documents. Publishable content only.

## Protocol

### Step 1 · Sweep the conversation

Reread the entire conversation. Collect every moment where the user corrected, rejected or redirected *how* something was written: tone, word choice, vocabulary, rhythm, register, sentence structure, punctuation, format.

For each correction, record:

- **✗ rejected**: what the model had written.
- **✓ accepted**: what the user asked for instead, or the rewrite they approved.
- **reason**: the reason they gave, if they gave one.

The conversation holds the real ✗/✓ pairs that feed Step 4. Do not invent examples in Step 4 when the real pair is recorded here.

If the sweep finds zero writing corrections, say so and stop. If it finds only one, go ahead anyway.

### Step 2 · Assess generalization

A correction only becomes a rule if it is **generalizable**: if the same choice would be wrong in a future piece, on another subject. Classify each one:

- **Generalizable**: points at a pattern ("you always do X", "stop using Y"). The same word or structure would be wrong in any piece.
- **One-off**: tied to this piece's subject, to a fact, or to a choice that only holds here. Or the user said "just here".
- **Borderline**: when in doubt, mark it this way and leave the decision to the user in Step 5.

Do not silently discard one-off corrections. Include them in the Step 5 proposal with the reason, so the user can promote any of them.

### Step 3 · Deduplicate and reconcile with the guide

The voice lives in `docs/voice/`. Read the target file: `docs/voice/base.md` by default, or the layer in `docs/voice/layers/` if the user named one. No layers exist yet, so today the target is always the base. Then run two passes:

**(a) Deduplicate against each other.** If the user corrected the same pattern at different points in the conversation, treat it as one rule, not several. Merge the occurrences and keep the examples.

**(b) Reconcile with the guide.** For each remaining rule, apply the table below:

| Situation | Action |
|---|---|
| Already covered by an existing rule, nothing new | Discard. Do not duplicate. |
| Covered by an existing rule, but the session produced a sharper example or a broader pattern | Propose **sharpening the existing rule**: rewrite it to absorb the better example. |
| Contradicts an existing rule | **Do not overwrite.** Flag the contradiction in the proposal and leave the decision to the user. |
| New, not covered | Becomes a new rule in the most fitting section of the guide. |

### Step 4 · Write the rules with sharp examples

For each new rule and each entry to sharpen, write the item in the style of the guide's rules:

- **Bold** at the opening, naming the pattern to avoid or the calibration.
- One diagnostic sentence: why it sounds wrong, or why the calibration matters.
- A concrete example, preferably the ✗/✓ contrast pulled from the real session: the sentence the model wrote and the one the user accepted. A generic example ("avoid formal words") is precisely what the rule should eliminate.
- Timeless: no date, no "in this session", no reference to the episode.

Place each rule in the most fitting section of the target file. `docs/voice/base.md` is organized as: **Structure**, **Significance inflation and promotional language**, **Vocabulary**, **Grammar-level tics**, **Rhythm and style**, **Hedging, filler, vague attribution**, **Connective tissue**, **Voice and texture**. If a group of rules fits none of them, propose a new section, with a title.

### Step 5 · Propose the batch to the user

Before touching the file, present the whole proposal in one message:

- **New rules**: each one as the literal markdown item that will be inserted, under its target subsection.
- **Entries to sharpen**: the current item and the proposed one, side by side.
- **One-offs**: listed, each with a line saying "treating as one-off because X".
- **Conflicts**: "correction Z contradicts rule N in the guide; pick which of the two holds, the skill does not decide on its own."

The user can approve everything, approve a subset, edit the text, or promote and demote items. Do not write anything without explicit approval.

### Step 6 · Apply in batch

After approval, apply all approved changes at once, to the target file identified in Step 3: `docs/voice/base.md` by default, or the named layer in `docs/voice/layers/`.

Preserve the target file's existing structure. Insert each rule inside the section it belongs to, in the voice the file already uses. Do not append a "session corrections" block at the end and do not restructure the document to accommodate a rule.

Then confirm to the user what was inserted, and where.

The skill does not re-correct the session's outputs. The corrections were already applied on the spot, during production.

## What this skill does not do

- Does not run on its own during the session. Only when the user asks, once, at the end.
- Does not settle a contradiction between a new correction and an existing rule on its own: it flags it and leaves the decision to the user.
- Does not invent examples. It uses the real ✗/✓ pairs from the conversation.
- Does not re-correct the session's outputs.
- Does not promote a correction to a rule without the user's approval.
- Does not record feedback about code, analysis or internal documents.

## Rule quality bar

A rule is good enough when:

- A senior AI engineer can apply it without ambiguity.
- It prevents the specific mistake that was corrected, without banning what was never a problem.
- The example is real (from the session) and sharp (a ✗/✓ contrast, not a generic illustration).

If the rule comes out vague ("don't use formal words"), refine it until it can be applied mechanically.
