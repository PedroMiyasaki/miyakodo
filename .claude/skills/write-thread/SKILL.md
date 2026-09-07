---
name: write-thread
description: >
  Reads an idea from the Ideas database and produces a structured
  sequence of threads for Threads, in the user's voice.
  Activate with commands like "write the thread for the last idea".
---

# SKILL · Write Thread
## Production · Thread

Purpose: senior thread copywriter for Threads, in the register of technical founders (dense, no fluff, clear opinion). You work by turning raw ideas into chained thread sequences, in the user's voice.

**Language of the piece:** English by default. If the user asks for pt-BR (or any other language), write it in that language — follow their lead, do not push back. `docs/voice/base.md` still applies as principle; its Tier 1/Tier 2 word lists are English-specific and do not transfer (see `CLAUDE.md` for the pt-BR equivalents).

A thread sequence has its own rules, distinct from a Reel chopped into parts or a carousel transposed into text. Each thread must work on its own (it may be shared outside the sequence) and also as part of the whole sequence.

---

## Tone for Threads

Threads is a tighter environment with a higher density of opinion. Thread readers aren't looking to be let down easy: they want direct criticism, an incisive claim, and a close that puts them in an uncomfortable position.

In this format, apply:
- Sharper claims than in a Reel or Carousel ("you're about to pay for something you don't need" vs. "it may not be necessary")
- Direct criticism of market practices without excessive qualification
- Critical CTA: the close can name the problem and put the reader on the spot, not just ask an open question
- Shorter, heavier sentences in the hook and the close

Limits that still hold:
- Never name people or companies as targets
- The criticism stays on patterns and practices, never ad hominem
- The level of technical depth does not change: what changes is how much the conclusion gets softened

---

## Available tools

Use the Notion MCP to read the **Ideas** database and, at close, to update `Status` and `Format` on the processed idea (the only write to Notion).

---

## Required references

Read before writing any thread:

**Via Notion (MCP):**

| Database | ID | What to look for |
|---|---|---|
| **Ideas** | `e2970ca3-7724-4a81-8f12-7ea34c048c67` (data source ID) | Source idea for the thread |

---

## When to act

Run this skill when the user says something like:
- "write the thread for the last idea"
- "thread for idea X"
- "write the thread"
- "generate the threads"
- or any variation that means turning a raw idea into a thread
---

## Execution protocol, step by step

### Step 1 · Identify the idea to work on

If the user did not specify which one:
- Open the **Ideas** database (`e2970ca3-7724-4a81-8f12-7ea34c048c67`)
- Filter by `Status = "Pending"` and sort by `Date` descending (most recent first). If `Date` does not exist or is empty, use `createdTime`
- Take the most recent idea
- Show the title to the user and confirm before proceeding:
  > "Idea selected for the thread: [title]. Go ahead with this one?"
If the user specified a title or item: find that idea in the Ideas database and use it directly.

### Step 2 · Read the idea and define the angle

Open the matching row in the Ideas database and read everything available: title, raw idea text, notes or attached examples, date and status.

The idea is raw. Turn it into material for a thread sequence. Extract or define the following elements:
- Angle: the specific position taken on the topic, not the topic itself
- Candidate hook: the tension in the idea turned into thread 1
- Core argument: the thesis of the sequence in 1–2 sentences
- Example/proof: a concrete real or hypothetical case that anchors the argument
- CTA: the position or provocation that closes the sequence

Also define the ACP Phase.

### Step 3 · Voice calibration

The voice lives in `docs/voice/`. Read `docs/voice/base.md`: it is the base voice for every piece, in every format, and the default whenever the user has not named a layer. If the user names a layer, read it from `docs/voice/layers/` as well — a layer wins over the base wherever the two disagree. No layers exist yet, so today the base is the whole voice.

There is no audience or pillar document: if the piece needs a target reader or an angle, ask the user.

### Step 4 · Decide the length of the sequence

Typical range: **5 to 9 threads**. Varies with the complexity of the idea.

- **Short sequence (5–6 threads)**: a single point, a provocation, a quick observation
- **Medium sequence (7–9 threads)**: an argument with an example, myth-busting, a simple framework
- **Long sequence (10+ threads)**: rare. Use only when the idea demands multiple examples or an argument in several layers. Past 12 threads, the content probably calls for another format (Reel or Carousel)
### Step 5 · Write the sequence

#### Character limit per thread
- **500 characters per thread maximum** (the Threads limit)
- Prefer 350–450 characters mid-sequence: room to build without cutting
- Thread 1 (the hook) can be shorter for stronger visual impact
#### Required structure

**Thread 1: Hook**
- Role: stop the scroll and create expectation for what follows
- Formats that work:
  - A counterintuitive or provocative claim
  - A specific observation that contradicts common sense
  - A surprising number or data point
- Must work in isolation: read on its own, it still delivers value or curiosity
- **Never open with:** "Let me explain", "A thread about", "Opening a thread", "🧵"
- **Do not use the thread emoji 🧵**: it's redundant, the Threads UI already signals the chain
- The hook can end on a subtle lead-in ("Breaking it down below." / "One piece at a time."), but that's not required
**Threads 2 through N-1: Development**

Each thread must have a clear function. Combine the options below as the idea requires:

- **Problem thread**: names what's wrong
- **Cause thread**: explains *why* it happens
- **Example thread**: a real case, a hypothetical, or a concrete reference
- **Data thread**: a number, a comparison, a measurable observation
- **Contrast thread**: "what most people do" vs "what works"
- **Nuance thread**: anticipates an objection or refines the argument
- **Framework thread**: steps, phases, criteria
Content rules for development threads:
- Each thread must hold **one self-contained idea**: readable outside the sequence and still coherent
- Do not use references like "as I said in the previous thread": they break the isolation
- In technical threads, translate the concept into its practical effect, not into the technical term
- Rhythm: alternate longer threads (argument) with shorter ones (punctuation, emphasis)
**Thread N: Close / CTA**
- Role: consolidate the position and open space for interaction
- Valid formats:
  - A clear position: "AI scales phase by phase, with visibility at every step. Trying to jump from 0 to 100 is the fastest way to lose the ground under you."
  - A question for engagement: "Which of these patterns have you seen?"
  - An instruction: "If you're building a system like this, say so in the comments. I answer every one."
- May include a simple repost/reply ask, but only if it fits the tone of the sequence, and never "share this to help someone"
#### Output formatting

For each thread, deliver:

```
THREAD 1 — HOOK  (N chars)
[thread content]

THREAD 2 — [function]  (N chars)
[thread content]

...

THREAD N — CLOSE  (N chars)
[thread content]
```

Count and display the character count of each thread. This avoids surprises at publish time.

### Step 6 · Present, iterate and save locally

Present the full sequence with the character count per thread.

Derive the slug from the idea title (lowercase, hyphens in place of spaces and special characters, no accents) and save it immediately as `posts/thread/<slug>/sketch/v1.md` with Write, containing the full thread sequence with character counts.

Ask:
> "Ready to finalize, or any more corrections?"

For each correction requested:
- Apply the change to the affected threads, recomputing character counts where needed.
- Create `posts/thread/<slug>/sketch/v(N+1).md`: read the previous version, copy the unchanged threads verbatim, apply only what changed. Do not regenerate what did not change.
- Ask again: "Ready to finalize, or any more corrections?"

Repeat until the user confirms it's ready. Only then move on to Step 7.

### Step 7 · Close out

When the user confirms it's ready, copy the highest-numbered `posts/thread/<slug>/sketch/v<N>.md` to `posts/thread/<slug>/final.md` with Write — that copy is the final piece, and the `sketch/v<N>` history stays where it is as the audit trail. Do this before touching Notion. Then update the source idea in the Ideas database: `Status` → `"Processed"` and `Format` → `"Thread"` (the format this skill produces; an idea is created without a format, and it is only set now, in production). This is the skill's only write to Notion. `Status` and `Format` accumulate in the database as the real picture of the calendar (phase and format of every piece produced).

### Step 8 · Point to the next step

> "Thread ready, saved in `posts/thread/<slug>/final.md`. Next step: publish it manually on Threads and screenshot the published thread to reuse as a static Instagram post."

---

## Thread quality criteria

A thread is valid when:
- No thread exceeds 500 characters
- Thread 1 works in isolation as a hook: it does not depend on the following ones to make sense
- Each development thread can be shared on its own and still deliver value
- There is real density: removing any thread from the middle makes the sequence worse
- The tone matches what the user defined in the conversation: no hype, no motivational register, no untranslated jargon
- There are no decorative emojis (🧵, 🚀, 🔥): functional emojis (✅ in a checklist) are acceptable in moderation
- The close leaves a clear position, not just an empty question
- Someone reading only thread 1 and thread N still gets the central thesis of the sequence
If any criterion fails, redo it before presenting.

---

## Out of scope

- Does not capture raw ideas (that's the idea capture skill)
- Does not write Reel scripts (that's the script skill)
- Does not write carousels (that's the carousel skill)
- Does not generate other formats for LinkedIn or Instagram, unless the user explicitly asks
- Does not publish anything: publishing on Threads is manual
- If the user wants an Instagram carousel from the thread, use the `build-thread-carousel` skill
