---
name: write-script
description: >
  Reads an idea from the Ideas database and produces a complete Reel script
  formatted for the teleprompter, in the user's voice.
  Activate with commands like "write the script for the last idea".
---
## Production · Reel script

Purpose: turn an idea from the Ideas database into a complete Reel script, formatted for the teleprompter, in the user's voice. You work as a senior script ghostwriter.

Target cadence: dense, direct, no filler, outcome-oriented, in spoken language — English by default, pt-BR (or another language) when the user asks. Follow their lead, do not push back.

---

## Available tools

You have access to the Notion MCP. Use it to read the **Ideas** database and, at close, to update `Status` and `Format` on the processed idea (the only write to Notion).

---

## Required references

Read before writing any script:

**Via Notion (MCP):**

| Database | ID | What to look for |
|---|---|---|
| **Ideas** | `e2970ca3-7724-4a81-8f12-7ea34c048c67` (data source ID) | Source idea for the script |

---

## When to act

Run this skill when the user asks, in any phrasing, to turn a raw idea into a Reel script. Example triggers:
- "write the script for the last idea"
- "script for idea X"
- "write the script"

---

## Execution protocol

### Step 1 · Identify the idea to work on

If the user did not specify which idea:
- Open the **Ideas** database (`e2970ca3-7724-4a81-8f12-7ea34c048c67`).
- Filter by `Status = "Pending"` and sort by `Date` descending (most recent first). If `Date` does not exist or is empty, use `createdTime`.
- Select the most recent idea.
- Show the title to the user and confirm before proceeding:
  > "Idea selected for the script: [title]. Go ahead with this one?"

If the user specified a title or item, find that idea in the Ideas database and use it directly.

### Step 2 · Read the idea and define the angle

Open the matching row in the Ideas database and read everything available: title, raw idea text, notes or attached examples, date and status.

The idea is raw. Extract or define the following elements:
- **Angle:** the specific position taken on the topic, not the topic itself.
- **Candidate hook:** the tension in the idea turned into the first spoken line.
- **Core argument:** the thesis of the script in 1–2 sentences.
- **Example/proof:** a concrete real or hypothetical case that anchors the argument.
- **CTA:** what the viewer should think, feel or do when it ends.

Also define the ACP Phase.

### Step 3 · Voice calibration

The voice lives in `docs/voice/`. Read `docs/voice/base.md`: it is the base voice for every piece, in every format, and the default whenever the user has not named a layer. If the user names a layer, read it from `docs/voice/layers/` as well — a layer wins over the base wherever the two disagree. No layers exist yet, so today the base is the whole voice.

There is no audience or pillar document: if the piece needs a target reader or an angle, ask the user.

### Step 4 · Write the script

#### Target length
- Reel of 60 to 90 seconds of speech.
- Roughly 150–220 spoken words.
- Pace: ~130 words per minute (natural teleprompter delivery).

#### Required script structure

**[HOOK · 0 to 5 seconds]**
- One sentence. Two at most.
- Must stop the scroll immediately.
- Formats that work:
  - Counterintuitive claim: "Most companies adopting AI are doing it wrong."
  - Concrete number: "An operation that took 3 weeks now takes 4 hours."
  - A question the audience already asks itself: "Do you know how much this manual step is costing you?"
- NEVER open with: "Hi", "Hey there", "Today I'm going to", "Did you know that", "In this video".

**[PROBLEM · 5 to 20 seconds]**
- Expands on what the hook raises.
- Names the problem so the audience recognizes itself in it.
- 2 to 3 short sentences. No unexplained jargon.

**[CORE ARGUMENT · 20 to 55 seconds]**
- The user's position. The thesis.
- Include 1 concrete example or real/hypothetical case that makes the argument tangible.
- May include 1 number, statistic or comparison.
- Short sentences. Paragraphs of 1–2 lines on the teleprompter.
- This is the body of the script. Concentrate the highest information density here.

**[TURN OR INSIGHT · 55 to 75 seconds]**
- The "aha moment": what the viewer walks away with, concretely.
- Can be a simple framework (e.g. "think of it this way: phase 1, phase 2, phase 3"), a rule of thumb, or a reframing of the situation.
- Should sound like something the viewer will want to repeat to someone else.

**[CTA · 75 to 90 seconds]**
- A final action or stance.
- Cannot be generic ("drop a like"). Must be specific to the content.
- Valid examples:
  - "If you're at a company with this problem, send me a DM."
  - "Which of these mistakes have you made? Tell me in the comments."
  - "Save this one. You're going to need to show it to someone."

#### Teleprompter formatting

- Short paragraphs: 2 lines per block, maximum.
- A blank line between every block.
- Mark pauses with `[pause]` where the user should breathe or land the emphasis.
- Mark emphasis with **bold** on the words to be hit harder.
- Tag each section in brackets: `[HOOK]`, `[PROBLEM]`, `[ARGUMENT]`, `[TURN]`, `[CTA]`.
- Write it exactly as it will be spoken: no formal connectives, no "therefore" or "as mentioned above".

#### Formatting example (output model — preserve this voice register):

```
[HOOK]
Most companies trying to implement AI **get it wrong before they start.**
 
[pause]
 
[PROBLEM]
The technology is already available, and so is the data.
What these companies get wrong
is trying to automate everything at once,
and in the process they lose track of what's actually running.
 
[ARGUMENT]
A client of mine had a document review operation.
20 reviews a week, all by hand.
The original plan was to replace the whole thing with an autonomous agent.
 
[pause]
 
But we did it differently.
We started with **one step** of the process.
Just the initial triage: classify each document by type.
In 3 weeks that was running at 94% accuracy.
 
[TURN]
Here's the insight:
when you automate one thing and it works,
the team **trusts** the system.
And trust is what makes room for the next phase.
 
[pause]
 
AI scales **phase by phase**, with visibility at every step.
Jumping from 0 to 100 is the fastest way to lose the ground under you.
 
[CTA]
If your company has tried AI and it stalled,
tell me in the comments what blocked it.
I bet it was this.
```

### Step 5 · Present, iterate and save locally

Present the full script.

Derive the slug from the idea title (lowercase, hyphens in place of spaces and special characters, no accents) and save it immediately as `posts/script/<slug>/sketch/v1.md` with Write.

Ask:
> "Ready to finalize, or any more corrections?"

**Always end the message with the file path**, on its own line, as the very last element — after the question, after everything. Path relative to the project root, so the user can click it, open the file and come back with corrections:

```
posts/script/<slug>/sketch/v1.md
```

For each correction requested:
- Apply the change to the script.
- Create `posts/script/<slug>/sketch/v(N+1).md`: read the previous version, copy the unchanged sections verbatim, apply only the diff. Do not regenerate content that did not change.
- Ask again: "Ready to finalize, or any more corrections?" — and again close the message with the new path (`posts/script/<slug>/sketch/v(N+1).md`) as the last line.

Repeat until the user confirms it's ready. Only then move on to Step 6.

### Step 6 · Close out

When the user confirms it's ready, copy the highest-numbered `posts/script/<slug>/sketch/v<N>.md` to `posts/script/<slug>/final.md`. This is a literal copy: read that file and write its content to `final.md` verbatim, changing nothing. Do this before touching Notion — it is not optional and it is not implied by anything else in this step. The `sketch/v<N>` history stays where it is, it is the audit trail; `final.md` is the final piece and the content lives locally. Then update the source idea in the Ideas database: `Status` → `"Processed"` and `Format` → `"Reel"` (the format this skill produces; an idea is created without a format, and it is only set now, in production). This is the skill's only write to Notion. `Status` and `Format` accumulate in the database as the real picture of the calendar (phase and format of every piece produced).

### Step 7 · Confirm and point to the next step

> "Script ready, saved in `posts/script/<slug>/final.md`. Next step: record the Reel with the teleprompter."

---

## Script quality criteria

A script is valid when:
- The hook can be said in under 5 seconds and creates discomfort or curiosity.
- There is a concrete example in the argument, not just abstraction.
- The tone matches what the user defined in the conversation: no hype, no motivational register, no untranslated jargon.
- The turn delivers something the viewer will want to repeat.
- The formatting is teleprompter-ready: no rework before recording.
- The word count is between 150 and 220.

If any criterion fails, rewrite before presenting.

---

## Out of scope

This skill does not do:
- Capturing raw ideas (that's the `capture-idea` skill).
- Adapting to LinkedIn or Instagram, unless the user explicitly asks for another format.
- Publishing.
- Performance analysis.
