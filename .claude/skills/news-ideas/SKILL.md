---
name: news-ideas
description: >
  Reads recent AI news from leading international sources, distills each
  relevant fact (new models, apps, funding rounds, startups, research,
  acquisitions, regulation) into a content idea and writes it straight to the
  Notion Ideas DB. Activate with commands like "update the ideas with today's AI
  news", "pull today's AI headlines" or "run the news radar".
---

## Ideas from the AI news cycle

Purpose: sweep the AI news cycle, identify what actually counts as news and convert each relevant fact into a content idea filed in the bank. The output is ideas ready to enter the queue.

Every idea generated carries the same underlying intent: to report a fact from the news cycle through content. The fact varies, the intent doesn't. A new model, a funding round, a freshly launched app, an acquisition, a paper or a regulatory shift — each case becomes "how the user tells this fact to their audience".

---

## Available tools

- **WebFetch**: pull the curated news digests
- **WebSearch**: catch recent breaking stories not yet in the digests
- **Notion MCP**: read ideas already on record (dedupe)
- **Bash**: read and write `last-run.txt`, the sweep window marker
- **`capture-idea` skill**: handles the filing in Notion. Don't duplicate that write.

---

## Required references

Before generating any idea, load everything below:

**Via Notion (MCP), `notion-fetch` with the ID below:**

| Object | ID | What to look for |
|---|---|---|
| **Ideas** | `e2970ca3-7724-4a81-8f12-7ea34c048c67` | Titles and Notes of the ideas already on record (so you don't repeat a story) |

---

## Voice calibration

The voice lives in `docs/voice/`. Read `docs/voice/base.md`: it is the base voice for every piece, in every format, and the default whenever the user has not named a layer. If the user names a layer, read it from `docs/voice/layers/` as well — a layer wins over the base wherever the two disagree. No layers exist yet, so today the base is the whole voice.

There is no audience or pillar document: if the piece needs a target reader or an angle, ask the user.

---

## The sweep window

`.claude/skills/news-ideas/last-run.txt` holds a single line: the UTC timestamp of the last sweep, ISO 8601 (`2026-08-26T14:03:11Z`). It defines the window this run covers — **from that timestamp up to now**.

Read it at Step 1, write it at Step 7, every run, whether or not anything was filed. The window was swept either way.

If the file is missing (first run ever, or it was deleted), fall back to **the last 7 days** and carry on — do not treat it as an error.

The window is a filter on *publication date*, not a promise the sources honor it. Digests reprint older items and search results drift; check each candidate's own date and drop anything published before the window opens. Dedupe against the bank still runs on top of this — a boundary story that already got filed does not get filed twice.

---

## News sources

### Must check — every run, no exceptions

| Source | URL |
|---|---|
| AI News (smol.ai daily digest) | `https://news.smol.ai/` |
| Anthropic News | `https://www.anthropic.com/news` |
| OpenAI News | `https://openai.com/news/` |
| Google Gemini News | `https://gemini.google/latest-news/` |

**The three provider blogs are owned media: most of what they publish is marketing, not news.** Judge each post before it becomes an idea. A shipped model, a real capability, a price change, a deprecation, a published benchmark or paper is news. A customer success story, a partnership announcement with no product behind it, a policy manifesto, a rebrand, an enterprise-tier pitch or a "we believe" essay is advertising — discard it. When the post is a launch wrapped in marketing, keep the shipped fact and throw away the framing.

### Also check

| Source | URL |
|---|---|
| TLDR AI | `https://tldr.tech/ai` |
| The Batch (DeepLearning.AI) | `https://www.deeplearning.ai/the-batch/` |
| Import AI | `https://importai.substack.com/` |
| Latent Space (essays, podcast) | `https://www.latent.space/` |
| Simon Willison | `https://simonwillison.net/` |
| Hacker News (front page) | `https://news.ycombinator.com/` |

The must-check list is a floor, not a ceiling: the sweep still covers the sources above **and** runs **one WebSearch pass** for breaking stories from the last 7 days not yet in the digests (e.g. `"AI" funding round`, `new LLM release`, `AI acquisition`, anchored on the sweep window). Everything worth reporting that week that no provider blog would ever publish — funding, acquisitions, regulation, rival labs, open source — comes from there. On Hacker News, consider AI items only.

---

## Execution protocol

### Step 1 · Load context (in parallel)

- `notion-fetch` on data source `e2970ca3-7724-4a81-8f12-7ea34c048c67` to read the ideas already on record (titles + Notes, which is where the source URL for dedupe comes from)
- Read the window marker and stamp this run in one shot:

  ```bash
  cat .claude/skills/news-ideas/last-run.txt 2>/dev/null || echo "(no marker — sweep the last 7 days)"
  date -u +%Y-%m-%dT%H:%M:%SZ
  ```

  The first line is where the window **opens**; the second is `NOW`, where it closes — hold on to that exact string, it is what Step 7 writes.
- Settle tone, audience and angle with the user (see § Voice calibration)

Don't skip this step: dedupe, the sweep window and relevance calibration depend entirely on what gets loaded here.

### Step 2 · Fetch the news

Run WebFetch on each curated source plus the WebSearch pass. Gather candidate facts published **inside the window** from Step 1 — since the last sweep, up to `NOW`. Don't include anything published before the window opens, even if it shows up in the search or sits on a digest's front page.

### Step 3 · Select what is actually news

Keep only a **concrete, datable, verifiable fact** from the AI space that touches a pain, decision or curiosity of the audience the user defined.

**Discard:**
- Warmed-over opinion, listicles, promotional content dressed up as news
- Rumors without a trustworthy source
- Any fact already represented in the bank (same story **or** same source URL) — dedupe is mandatory, because this skill writes without human review and may run again tomorrow

**Volume:** equal to the number of relevant stories that day. It might be 2, it might be 8. Don't force a number and **don't invent news to fill a quota**. If nothing new clears the bar, file nothing and say so.

### Step 4 · Frame each story as an idea

For each selected story, produce:

**Idea title:** maximum 10 words, in the user's voice, written in English. It must be the *content angle*, not the headline copied over. Concept by its effect, not by its name; anti-hype; no untranslated jargon; never open with "Did you know", "Today" or "Hi there".

- Headline: "OpenAI launches GPT-5.5 with a 2M token window"
- Bad title (copy): "GPT-5.5 arrives with 2M tokens of context"
- Good title (angle): "A giant context window won't fix your process problem"

**Notes:** a 1–2 sentence summary of the fact + `Source: <URL>` + `Suggested format: <Reel | Thread | IG Carousel | LinkedIn Post>`.

### Step 5 · File everything

For each idea, invoke the `capture-idea` skill via the Skill tool, passing the **framed title** and the **notes block** (summary + `Source: <URL>` + suggested format). `capture-idea` handles the write to Notion. The source URL **must be preserved in the Notes field**.

Don't ask for approval and don't present the ideas beforehand. File them all directly.

### Step 6 · Report

Close with a short list of what was filed: one line per idea, with the source. No intro and no commentary.

```
Filed in the bank:
1. [title] — [source]
2. [title] — [source]
```

If nothing cleared the bar: `Nothing new worth covering in today's news. Nothing filed.`

Say which window was swept in one line: `Window: <last-run> → <NOW>` (or `last 7 days → <NOW>` on a first run).

### Step 7 · Stamp the run

Last thing, always — even when nothing was filed, even when a fetch failed:

```bash
printf '%s
' '<NOW>' > .claude/skills/news-ideas/last-run.txt
```

`<NOW>` is the exact timestamp captured in Step 1, not a fresh `date` call: anything published while the sweep was running stays inside the next window instead of falling through the gap.

---

## Tone and behavior

- **No hype.** The angle is always what the fact changes in practice for the audience, not a reaction to the news.
- **Don't copy the headline.** The title is the content angle, not the press release.
- **Don't make things up.** If the source doesn't confirm the fact, it doesn't become an idea.
- **Dedupe first.** Before filing, confirm the story isn't already in the bank.
- **Always stamp.** Step 7 runs on every path, including the empty one. A skipped stamp makes the next run re-sweep ground already covered.

---

## Out of scope

- Doesn't write the final content (that's the `write-*` skills' job)
- Doesn't publish anything outside the Ideas DB
- Doesn't opine on the news or rank the ideas
- Doesn't ask for approval: it files whatever clears the bar
