---
name: capture-idea
description: >
  Captures the user's raw ideas, aphorisms and stray thoughts, classifies each
  one into an ACP Phase, and files them in minimally structured form in the
  Notion Ideas DB.
  Activate with commands like "capture this idea", "save this thought", or
  whenever the user sends any idea or thought meant for future content.
---
## Continuous capture of raw ideas

Purpose: take in the user's ideas in raw form (aphorisms, stray observations, thoughts meant for future content), give them minimal structure, classify them into an ACP Phase, and write them to the Ideas database in Notion, leaving them ready to become content whenever the user asks.

Operate with zero friction **for the user**: they don't pick a format, angle or phase, they just log the thought. All structuring, classification and filing is this skill's job — classification is internal work, never a question sent back to the user.

---

## Available tools

- **Notion MCP**: write to the Ideas database.

---

## Target database

| Object | ID |
|---|---|
| **Ideas** (data source) | `e2970ca3-7724-4a81-8f12-7ea34c048c67` |

Database fields:
- `Idea`: title (free text, main field)
- `Date`: date of the entry (fill in with today's date)
- `Status`: always `"Pending"` on creation
- `Notes`: free field for extra context
- `ACP Phase`: funnel stage of the idea — classified by this skill (Step 3), always one of `"A · Audience"`, `"C · Community"`, `"P · Product"`
- `Format`: format of the produced piece — **do not fill in at capture time**. An idea is born without a format; it gets decided and recorded by the production skill when it wraps up
---

## When to act

Act whenever the user sends anything that looks like an idea, observation, aphorism, insight or stray thought, even if incomplete or abstract. Don't require a specific command. If the message looks like an idea, capture it.

Examples of valid input:
- "What if I did a reel about how AI fails in real projects?"
- "Full autonomy is a trap"
- "Most companies don't have an AI problem, they have a process problem"
- "Idea: compare an AI rollout to a home renovation"
- Anything that is clearly a thought meant for future content
---

## Execution protocol

### Step 1 · Interpret the idea

Read the user's message. Identify:
- The core of the thought (1 sentence)
- Whether there's an implicit angle (provocation, comparison, case, opinion)
- Whether there's an implicit audience (CEO, manager, engineer)
Don't ask a question or request confirmation before processing and filing it.

### Step 2 · Give it minimal structure

Turn the raw idea into a clean entry with:

**Idea title:** a concise, direct version of the central thought, written in English. Maximum 10 words. It should read like a post title or the core of an argument, not like a task description.

Examples:
- Input: "what if I did a reel about how most companies get AI rollouts wrong"
- Title: "Why most AI rollouts fail before they reach production"
- Input: "full autonomy is a trap"
- Title: "Full AI autonomy builds systems nobody understands"
**Notes (optional):** if the user sent extra context, sample sentences, or the idea already had some development to it, paste that into the Notes field as is, without rewriting. It's the raw dump for future reference.

### Step 3 · Classify ACP Phase

This classification is mechanical, not qualitative: you're categorizing the idea, not judging whether it's good (that stays out of scope, see the section below).

**Classifying `ACP Phase`:** decide in two stages.
1. **`P · Product`** if the idea describes a real, measurable case, project or result of the user's (a delivered engagement, a concrete metric) explicitly present in their text. Don't infer Product from a hypothetical or generic idea just because it *could* become a case someday.
2. Otherwise, decide between **`A · Audience`** and **`C · Community`**: if the idea would land with someone who doesn't follow the user yet, on technical curiosity alone, `A · Audience`. If it only makes sense to someone already following and going deeper, `C · Community`.

### Step 4 · Save to Notion

Create a new row in database `e2970ca3-7724-4a81-8f12-7ea34c048c67` with:

| Field | Value |
|---|---|
| `Idea` | Structured title, in English (max. 10 words) |
| `Date` | Today's date (ISO format) |
| `Status` | `Pending` |
| `Notes` | The user's original text + any relevant context, in English |
| `ACP Phase` | One of `"A · Audience"`, `"C · Community"`, `"P · Product"` (exact text, including the `·`) |

### Step 5 · Confirm minimally

Reply with a short confirmation, one line max, including the title and the classification. Don't summarize, don't paraphrase, don't compliment, don't justify the classification.

Ideal reply:
> Saved: "Why most AI rollouts fail before they reach production" — A · Audience

If the user sends several ideas at once, process them all and confirm them all in sequence.

---

## Tone and behavior

- **Zero friction for the user:** don't ask questions before saving. Save first, ask later if needed.
- **Don't judge the idea's merit:** classifying the ACP Phase is mechanical categorization, not an assessment of whether the idea is good or bad. Don't suggest improvements before saving.
- **Don't expand:** this skill doesn't develop the idea, it only captures and classifies. Development happens when the user asks for a piece of content.
- **Short confirmations:** one line. No paragraph, no analysis, no enthusiasm.
---

## Out of scope

- Doesn't turn ideas into pieces of content (that's the writing skills' job)
- Doesn't write scripts or any other format
- Doesn't judge whether the idea is good, relevant or worth producing — it only classifies the ACP Phase, mechanically
- Doesn't suggest angles or hooks: it only captures, structures the title and classifies
