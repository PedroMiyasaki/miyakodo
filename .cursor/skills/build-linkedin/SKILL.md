---
name: build-linkedin
description: >
  Reads an idea from the Ideas database, produces a native long-form text post for
  LinkedIn in the user's voice, and then finds and captures the scroll-stopping image
  that ships with it. Activate with commands like "build the LinkedIn post for the
  last idea" or "write the LinkedIn post for the last idea".
---

# SKILL · build-linkedin
## Production · LinkedIn post (text + image)

Purpose: produce a complete, ready-to-publish LinkedIn post — the long-form text **and** the image that goes with it. You work by turning raw ideas into LinkedIn posts that argue a case, carry density and take a clear position, in the user's voice, then finding the one image that makes the target reader stop scrolling long enough to read it.

**Language of the piece:** English by default. If the user asks for pt-BR (or any other language), write it in that language — follow their lead, do not push back. `docs/voice/base.md` still applies as principle; its Tier 1/Tier 2 word lists are English-specific and do not transfer (see `CLAUDE.md` for the pt-BR equivalents).

The format calls for an argument with more layers than the other formats, with no character ceiling like X and no visual to lean on. Deliver substance.

---

## Available tools

Use the Notion MCP to read the **Ideas** database and, at close, to update `Status` and `Format` on the processed idea (the only write to Notion).

Use the **Chrome browser automation** tools (`mcp__claude-in-chrome__*`) in Step 7 to find and capture the post's image. They are deferred: invoke the `claude-in-chrome` skill before calling any of them.

---

## Required references

Read before writing any LinkedIn post:

**Via Notion (MCP):**

| Database | ID | What to look for |
|---|---|---|
| **Ideas** | `e2970ca3-7724-4a81-8f12-7ea34c048c67` (data source ID) | Source idea for the LinkedIn post |

**Locally — read at least two of these on every run:**

`examples/` holds real LinkedIn posts that worked, split into `english/` and `pt-br/`. **Their
subject matter is irrelevant** and none of them is about the idea you are writing. They are there
for one thing: calibrating what a human, authoritative, shareable LinkedIn post looks like on the
page. Read the pair matching the language you are writing in, plus one from the other folder.

What they are collectively showing, and where each rule now lives:

| What the examples do | Written down in |
|---|---|
| Paragraphs of 3–6 joined sentences, single-sentence paragraphs used as rare beats | `base.md` § 5, *Paragraph density* |
| Sentences inside a paragraph joined by real connectives | `base.md` § 7 |
| Repetition used as an audible figure that builds and stops | `base.md` § 5, *Deliberate repetition* |
| A proper noun or a number every two or three sentences | `sincere-senior.md`, *Concreteness* |
| The writer's own decision, price, or first-party data on the line | `sincere-senior.md`, *Skin in the game* |
| No hashtags, no engagement CTA | Step 5 below |

---

## When to act

Run this when the user says something like:
- "build the LinkedIn post for the last idea"
- "write the LinkedIn post for the next idea"
- "LinkedIn for item X"
- "generate the LinkedIn copy"
- or any variation that means turning a raw idea into a long-form LinkedIn post

The deliverable is always text **plus** image. If the user asks for text only, skip Step 7 and say so.

---

## Execution protocol, step by step

### Step 1 · Identify the idea to work on

If the user did not specify which one:
- Open the **Ideas** database (`e2970ca3-7724-4a81-8f12-7ea34c048c67`)
- Filter by `Status = "Pending"` and sort by `Date` descending (most recent first). If `Date` does not exist or is empty, use `createdTime`
- Take the most recent idea
- Show the title to the user and confirm before proceeding:
  > "Idea selected for LinkedIn: [title]. Go ahead with this one?"

If the user specified a title or item: find that idea in the Ideas database and use it directly.

### Step 2 · Read the full idea

Open the matching row in the Ideas database and read everything available:
- Title
- Raw idea text
- Notes, context or attached examples
- Date and status

Extract the following elements from the idea:
- Main angle
- Possible thesis
- Available example/proof, or a concrete hypothesis
- The tension that can become the hook

Also define the ACP Phase.

### Step 3 · Voice calibration

The voice lives in `docs/voice/`. Read `docs/voice/base.md`: it is the base voice for every piece, in every format.

Then read `docs/voice/layers/sincere-senior.md`. It is the **default layer for every LinkedIn post** — the senior-engineer register, the argument shape and the honesty rules that make the post sound like the user. Read it on every run, without being asked. Where it disagrees with the base on register, the layer wins; the base's anti-slop rules still hold.

If the user names a different layer, read it from `docs/voice/layers/` as well and let it win over both.

Then read the posts in `examples/` for the language you are writing in, plus one from the other folder. The two voice documents state the rules; the examples are what the rules produce on a page, and the gap between reading a rule about paragraph density and seeing one is most of the calibration. Ignore what they are about.

There is no audience or pillar document: if the piece needs a target reader or an angle, ask the user.

### Step 4 · Decide structure and length

LinkedIn text posts have a technical ceiling of 3,000 characters. Let the needs of the argument set the length: no padding, no premature cutoff.

**Guiding ranges:**
- **Short post (600–900 chars)**: a single observation, a data point with an interpretation, a direct position. For ACP phase A, where reach matters more than depth.
- **Medium post (900–1,800 chars)**: an argument with an example, myth-busting, a framework in 2–3 points. Most common for ACP=A→C.
- **Long post (1,800–2,800 chars)**: in-depth analysis, a causal chain with multiple layers, an argument that would need a carousel if it were visual. For ACP=C, where authority is the goal.

If the idea fits well in a short post, don't stretch it. If the idea needs development that goes past 2,800 chars to hold quality, use the carousel format instead.

**Calibrate against `examples/` before assuming you need the long form.** Those posts run 1,200 to 1,900 characters, and only the most polemical one goes past 3,000. Length there tracks how much verifiable material the writer actually has — names, numbers, a decision they made — not how much argument they could construct. A 2,900-character post built from reasoning alone is long because it is padded, and it will read that way next to the 1,231-character one that announces a fact and stops.

### Step 5 · Write the post

#### Native LinkedIn formatting

LinkedIn renders line breaks as visual space, and the temptation is to use that space on every sentence. Don't. **A paragraph here is a unit of thought, not a unit of display** — most run three to six sentences that develop one idea, joined by real connectives, per `base.md` § 5 and § 7. The single-sentence paragraph is a beat: it works because it is rare, and two or three of them in a post is the ceiling.

The failure this replaces is specific and it is the most common one in the format: correct sentences stacked one per line, each with the same weight, nothing building, no signal about which idea is load-bearing. It scans as a teleprompter feed. Every post in `examples/` avoids it, including the one that is pure polemic.

Vary paragraph length deliberately. One that runs six sentences, then one that runs two, then a fragment — that is what a person writing looks like.

**A short hyphen list is allowed** when the items are genuinely parallel and short (three solver families, three reasons). Two of the reference posts use one. What is banned is the inline-header list from `base.md` § 5 — `- **Speed:** the system is faster` — which is decoration pretending to be structure.

**No markdown**: LinkedIn does not render `**bold**`, `_italic_` or `# headings`. Use line breaks and verbal structure to create visual hierarchy. Functional symbols (→, •) are acceptable as list markers. Decorative emojis (🚀, 🔥, 💡) are forbidden.

#### Required structure

**First line: hook**
- It's the only text visible before the "see more" button in the feed
- Function: create enough tension for the reader to click "see more"
- Valid formats (output examples):
  - Counterintuitive claim: "Most AI projects don't fail on the technology."
  - A data point with an implicit interpretation: "80% of the AI use cases that reach us have already been attempted in-house once."
  - A question that names a real pain in the audience: "Why does the automation that worked in the pilot stall at scale?"
  - **The fact itself, stated flat**, when the fact is genuinely news: "Today marks a big moment for DuckLabs: we are joining Amazon Web Services." No windup, because the announcement is the tension.
  - **A fragment**, when a decision is the story: "Parei." One word, then the reason on the next line. This only works when what follows is a real decision with a price attached — as a stylistic move on an ordinary post it is theater.
- **Never open with:** "Hello, LinkedIn", a company introduction, or a generic question ("Did you know that...")
- The first line should not deliver the answer; it should make the answer irresistible

**Do not manufacture tension the idea does not have.** Two of the four reference posts open by simply saying the thing — an acquisition, a benchmark number — and they hold because the material is real. A fabricated counterintuitive claim bolted onto ordinary material is worse than the flat statement of that material.

**Development (body)**

Organize the argument into short blocks with a clear function:

- **Problem block**: names what's wrong in the conventional understanding or the common practice
- **Cause block**: explains *why* the problem exists, the layer most people don't see
- **Evidence block**: a data point, a real case (without naming the client), a measurable observation, a concrete comparison
- **Contrast block**: what most people do vs. what works, with specificity, not generalities
- **Framework block**: a logic in 2–4 points the reader can apply or use as criteria
- **Nuance block**: anticipates the obvious objection and answers it, shows depth, avoids oversimplification

Don't use every block in every post. Pick the ones the idea requires. A medium post has 3–4 well-developed blocks; a long post can have 5–6.

**These are functions, not a running order, and they are invisible in the output.** The reference posts do not walk problem → cause → evidence → nuance; one is evidence the whole way down, another goes straight from position to contrast and never concedes anything. The nuance block in particular is optional — a post that takes a position and holds it is stronger than one that softens itself on schedule. If a reader could reconstruct the block list from the finished post, the blocks are showing.

**Close / CTA**

A CTA on LinkedIn is not an empty ask for engagement. Valid formats (output examples):

- A clear position that consolidates the argument: "The point is process control before automation, and the technology comes as a consequence of that, not as the starting point."
- A question the writer genuinely cannot answer, aimed at readers who can: "What other domains have algorithms still outrunning scaling?"
- The link to the thing the post is announcing, when the post is an announcement: "Read the full announcement here:"

The close is where the reference posts are most consistent, and it is the opposite of what the format teaches. **None of the four asks for anything.** One ends on the tradeoff, one ends on an accusation, one ends on a link, and one ends on a question its own author cannot answer. The post earns the comment by being worth answering, not by requesting the answer.

So: end on the argument's final compression, or on a question you genuinely don't know the answer to and a qualified reader might. Never on "what do you think?".

**Hashtags — default to none.**

All four reference posts carry zero, and the format has not needed them for reach in years. Add them only when the user asks, or when a post is genuinely aimed at a tag people follow — and then three at most, technical and specific, on their own line at the end. `#innovation`, `#technology`, `#AI` are noise and mark the post as marketing output.

#### Output formatting

Deliver the complete post in its final publishing form, line breaks included, with no structural labels (no "PROBLEM BLOCK:", no "HOOK:"). The output must be pasteable straight into LinkedIn with no formatting edits.

```
[first line: hook]

[development, in paragraphs of varying length]

[close]
```

Hashtags are not part of the default shape. When the user asks for them, they go on their own line after the close.

Alongside the post, also deliver:
- Character count
- The ACP Phase identified

### Step 6 · Present, iterate and save locally

Present the complete post with the character count and ACP.

Derive the slug from the idea title (lowercase, hyphens in place of spaces and special characters, no accents) and save it immediately as `posts/linkedin/<slug>/sketch/v1.md` with Write, containing the post in its final publishing form followed by the line with the character count and ACP.

Ask:
> "Ready to finalize, or any more corrections?"

For each correction requested:
- Apply the change, recomputing the character count where needed.
- Create `posts/linkedin/<slug>/sketch/v(N+1).md`: read the previous version, copy the unchanged blocks verbatim, apply only what changed. Do not regenerate what did not change.
- Ask again: "Ready to finalize, or any more corrections?"

Repeat until the user confirms it's ready. Only then move on to Step 7.

### Step 7 · Find and capture the image

The text is locked. Now find the one image that earns the stop.

The audience is AI practitioners and business owners scrolling a feed at speed. The image has one job: make that specific reader pause long enough to read the first line. It does that by showing them **something they recognize from their own work** — not by being pretty.

#### 7a · Decide what the image has to carry

Before searching, write one sentence: *what does this image have to show?* Answer it from the post, not from a vague sense of the topic.

The strongest answer is almost always **the mechanism the post argues about, drawn**. The reader recognizes their own system in the picture before reading a word, and the argument has already started.

> **Reference case.** The post arguing against fully autonomous agents shipped with the canonical ReAct loop diagram: `Task → LLM (Reasoning self-loop) → Tools → Environment`, with `Action` and `Result` arrows. Plain black and white, no branding. It is the exact architecture the post takes apart. Anyone who has built one saw their own system and stopped.

Image classes that work, best first:

1. **The architecture diagram of the thing being argued about.** Makes the argument visible before the text is read.
2. **A chart with a surprising shape** — a benchmark, a cost curve, a latency distribution. Use when the post's spine is a number.
3. **A screenshot of the real artifact** — a trace, a log, a 400-line system prompt, a dashboard, a tool UI. Reads as proof the thing was seen, not theorized.
4. **A figure from the paper the post cites.** Credible and specific; credit it.

Never: stock photos of people at laptops, glowing brains, robot hands, abstract blue neural networks, AI-generated art, or a quote card with the hook typed over a gradient. Those signal "content" and get scrolled past by exactly the reader the post is for.

#### 7b · Judge it at feed size

The image will be seen small, first, on a phone. Before capturing, check:

- **Legible as a thumbnail.** Labels readable at roughly 40% width. If it needs zooming, it fails.
- **Few elements.** Five or six boxes, not a 30-node system map.
- **High contrast**, and survives both LinkedIn light and dark mode. Plain white or plain dark backgrounds both work; mid-grey does not.
- **Landscape or square.** Tall images get cropped in the feed.
- **No unrelated branding**, no watermark, no visible cookie banner or nav chrome in the capture.

#### 7c · Search and capture

Invoke the `claude-in-chrome` skill, then work in a **new tab** (`tabs_create_mcp`).

Go to the source before going to image search. Sources rank: the paper on arXiv, the framework's docs page, the original blog post, then image search as the fallback. A source page gives real resolution and a URL that can be verified and credited; an image-search thumbnail gives neither.

Build the query from the canonical term, not from the post's phrasing: `react agent loop diagram`, `langgraph state graph architecture`, `<paper name> figure 2`. If the post argues about a named thing, the named thing has a canonical picture — find that one.

Capture with a screenshot of the element on the page. Crop to the figure: no surrounding page furniture.

Do not fabricate an image, and do not build one in HTML — this step finds an existing artifact. If nothing good exists after a couple of searches, stop and say so rather than settling for a stock photo. A post with no image beats a post with a glowing brain.

#### 7d · Save it with the post

Save the capture as `posts/linkedin/<slug>/image.png` — at the folder root, beside the `final.md` it ships with, not in `sketch/`.

Then append one line to the metadata footer of the final `posts/linkedin/<slug>/sketch/v<N>.md` (the footer that already carries the character count and ACP — not the publishable body), so the text file points at its image:

```
Image: posts/linkedin/<slug>/image.png — <source URL>
```

The footer belongs in `sketch/v<N>.md`, so it rides along into `final.md` when that copy is made in Step 8.

If the image is a figure from a paper or an identifiable blog post, tell the user to credit the source in the post or in the first comment. Generic textbook diagrams don't need it.

#### 7e · Present it

Show the user the image, one line on why it was chosen, and the source URL. Ask:

> "Does this image work, or should I look for another?"

If they want another, go back to 7a and re-answer *what does this image have to show?* before searching again — a second search on the same premise usually returns the same misses.

### Step 8 · Close out

With the text confirmed and the image approved, assemble the deliverable. Everything for the piece lives in **one** folder, `posts/linkedin/<slug>/`: `sketch/` is the working material, and the folder root holds exactly what gets published:

| File | What it is | Written by |
|---|---|---|
| `final.md` | copy of the highest-numbered `sketch/v<N>.md` | this skill, now |
| `image.png` | the capture from Step 7 | this skill, in 7d |
| `pt-br.md` | copy of the highest-numbered `sketch/pt-br-v<N>.md` | `traduzir`, later, only if a translation is asked for |

So at this step you copy the final `sketch/v<N>.md` to `posts/linkedin/<slug>/final.md`. The image is already in place from 7d. The `pt-br.md` slot stays empty unless the user asks for a translation.

The `sketch/v<N>` history is never deleted — it is the audit trail, and `final.md` is a copy of its highest version taken at "done". So if the user edits a `sketch/v<N>.md` after that, re-copy it to `final.md`.

Then update the source idea in the Ideas database: `Status` → `"Processed"` and `Format` → `"LinkedIn Post"` (the format this skill produces; an idea is created without a format, and it is only set now, in production). This is the skill's only write to Notion. `Status` and `Format` accumulate in the database as the real picture of the calendar (phase and format of every piece produced).

### Step 9 · Point to the next step

> "Post ready. Everything ships from `posts/linkedin/<slug>/` — `final.md` and `image.png`. Version history stays in `sketch/`. Next step: publish it manually on LinkedIn."

---

## LinkedIn post quality criteria

A post is valid when every criterion below is satisfied:
- The first line creates enough tension for the "see more" click without revealing the answer
- The argument is genuinely developed: removing any block makes the post worse
- The tone matches what the user defined in the conversation: no hype, no motivational register, no untranslated jargon
- Paragraph length varies, and the single-sentence paragraph appears two or three times at most, as a beat
- Inside each paragraph, the sentences are joined by real connectives instead of stacked side by side
- Every paragraph carries at least one proper noun or number a reader could go verify
- The writer is exposed somewhere: a decision they made, a price they paid, data only they have
- There is no markdown (`**`, `_`, `#`), only plain text with line breaks
- The close takes a position or asks something the writer genuinely can't answer, and asks for nothing
- There are no hashtags, unless the user asked for them
- The character count does not exceed 3,000
- Reading only the first line and the CTA, the reader gets the central thesis of the post
- The image shows something from the post's actual subject, is legible as a thumbnail, and is not a stock photo
- The image is saved at `posts/linkedin/<slug>/image.png` and the final `sketch/v<N>.md` footer records its path and source URL
- The root of `posts/linkedin/<slug>/` holds the publishable set: `final.md` (copy of the final `sketch/v<N>.md`) alongside `image.png`, with the `v<N>` history left intact in `sketch/`

If any criterion fails, redo it before presenting.

---

## Out of scope

- Does not capture raw ideas (that's the idea capture skill)
- Does not write Reel scripts (that's the script skill)
- Does not write carousels (that's the carousel skill)
- Does not write threads (that's the thread skill)
- Does not adapt a carousel for LinkedIn: when the user wants to publish a carousel on LinkedIn, they should go straight to publishing or design, without passing through this text skill
- Does not publish anything: publishing on LinkedIn is manual
