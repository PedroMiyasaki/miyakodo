---
name: write-substack
description: >
  Produces a full illustrated Substack article — a sequential story with a real narrative
  spine, 3 to 8 images captured live from primary sources in the browser, and a title
  built to be opened. Works from a thesis that already shipped as a Reel, from breaking
  news, or from a raw idea. Activate with commands like "write this week's Substack",
  "turn <slug> into an article", "write the Substack piece about <news>".
---

# SKILL · write-substack
## Production · Substack article (long-form + captured images)

Purpose: produce a **finished article** — one a technically literate reader chooses to spend twenty minutes on and forwards to somebody. Not a long post. An article: a story that moves in sequence, carried by images captured from the real thing.

Three properties separate what this skill ships from what everything else in this repo ships:

1. **It runs on a narrative spine, not an argument structure.** The reader follows someone finding something out, in order.
2. **It is illustrated with real captures.** Three to eight images, every one screenshotted from a primary source in the browser, every one placed where the text just raised the question it answers.
3. **It has no length ceiling.** It ends when the material ends.

**Language of the piece:** English by default. If the user asks for pt-BR (or any other language), write it in that language — follow their lead, do not push back. `docs/voice/base.md` still applies as principle; its Tier 1/Tier 2 word lists are English-specific and do not transfer (see `CLAUDE.md`). A finished English article can be adapted later with `traduzir`.

---

## What this channel is for

Instagram and LinkedIn are rented audience. Substack is the **owned list** — the only channel here where the reader hands over an address and can answer you directly.

| | Instagram / LinkedIn | Substack |
|---|---|---|
| Metric that matters | reach, reactions | **open rate and replies** |
| Reader's state | scrolling, cold | opted in, twenty minutes available |
| What earns the click | a hook that creates tension | a **title worth an evening** |
| What the piece carries | the conclusion | **the whole route to it, shown** |
| Role in ACP | A · Audience → C · Community | **C · Community → P · Product** |

Replies are the product of this channel. The same problem named in thirty replies is the next workshop, the next offer, the next thing worth building. Write toward the reply.

## The rule that keeps this from being a long post

**LinkedIn ships the conclusion. This ships the route.**

An article that reaches the same conclusion by the same road, with more paragraphs, has failed. What the shorter formats could not carry is the sequence: the wrong first guess, the number that broke it, the page you actually went and read, the thing you tried that did not work.

Two concrete tests, applied at Step 5 and again at the end:

- **The artifact test.** The article carries at least one thing that could not have been posted on LinkedIn: a captured figure, a code block, a real log or trace, a table, a number series.
- **The sequence test.** Read only the section headings, in order. If they do not read as one thing happening after another, the piece is an argument wearing an article's clothes. Rewrite the spine.

---

## News is a legitimate subject

Perishable material is welcome here, and often the best subject available. Nothing about this format requires an evergreen thesis.

**But news becomes an article only through reconstruction.** A summary of what was announced is not an article, and the reader has already seen four of those. What makes it yours is the gap between what the coverage said and what the primary document actually says — read on page 14, captured, and put next to the headline. That is the **reconstruction** spine in Step 4, and it is the most image-dependent of the four. If you cannot get to a primary source, there is no article; say so rather than writing the fifth summary.

---

## Available tools

**Notion MCP** — to read the **Ideas** database, and on the standalone path to update `Status` and `Format` at close.

**Chrome browser automation** (`mcp__claude-in-chrome__*`) — the capture engine, used across a whole session in Step 7. They are deferred: invoke the `claude-in-chrome` skill before calling any of them.

---

## Required references

**The voice, every run:**

| Document | Why |
|---|---|
| `docs/voice/base.md` | The base voice for every piece, in every format. Non-negotiable floor. |
| `docs/voice/layers/sincere-senior.md` | The register — senior engineer, position first, skin in the game. Default layer for Substack articles as well as LinkedIn posts. Where it disagrees with the base on register, the layer wins; the base's anti-slop rules still hold. |

If the user names a different layer, read it from `docs/voice/layers/` too and let it win over both.

**Prior art on this thesis, when it exists:**

| File | Why |
|---|---|
| `posts/script/<slug>/final.md` | The Reel that carried the idea. Read it so the article does not repeat its framing — and to find what the 60-second version had to throw away. |
| `posts/linkedin/<slug>/final.md` | Only if it already exists. Read it for what to avoid: not one sentence carries over verbatim. |

**Calibration, every run:**

| Source | What you are reading for |
|---|---|
| `posts/substack/*/final.md` — the articles already published here | House style as it actually stands, including how images are placed and captioned. Read the two most recent. On the first run there are none; skip this rather than inventing one. |
| `.claude/skills/build-linkedin/examples/` (`english/` and `pt-br/`) | Prose register at the sentence level: paragraph density, real connectives, a proper noun or number every two or three sentences, the writer exposed. **Their subject matter is irrelevant.** Read the pair matching the language you are writing in. |

There is no audience document and no content-pillar document, by design. If the piece needs a target reader or an angle, ask the user.

---

## When to act

- "write this week's Substack"
- "turn `<slug>` into an article"
- "write the Substack piece about [something that happened this week]"
- "write the article version of the reel about X"
- any variation meaning a long-form illustrated newsletter piece

---

## Two entry paths

They differ only in Step 1 and Step 9.

**Reuse path.** A thesis that already shipped in another format — usually a Reel, sometimes a LinkedIn post — taken deep. The sibling `final.md` exists in `posts/`, and the source idea is already `Processed` in Notion carrying that format. **This path writes nothing to Notion.**

**Standalone path.** A fresh idea from the Ideas database, or news the user brings in directly. No siblings. This path closes the idea in Notion at Step 9.

---

# Execution protocol

## Step 1 · Identify the subject

**Reuse path.** The user names a slug. If they did not, list the most recent slugs in `posts/script/` and `posts/linkedin/` by mtime, show them, and ask which one goes long.

Choose for **depth of available material**, never for hook strength. The right subject is the one where you can name, before writing a word, at least three things you could go capture.

**Standalone path.** For news the user brings in, take it directly. Otherwise open the **Ideas** database (`e2970ca3-7724-4a81-8f12-7ea34c048c67`), filter `Status = "Pending"`, sort by `Date` descending (fall back to `createdTime`), and confirm the most recent:

> "Idea selected for the article: [title]. Go ahead with this one?"

## Step 2 · Read everything, and separate it

**Reuse path.** Read `posts/script/<slug>/final.md` in full, plus the idea row in Notion. Then build two lists explicitly, in your own working notes:

- **Burned** — every claim, example and turn of phrase the audience already saw in the Reel. The article may land on the same conclusion, never by the same sentences.
- **Cut for time** — the caveat that did not fit in 60 seconds, the second example, the number that needed a chart, the thing you tried first that failed, the source you read but could not cite out loud. **This is the article.**

If "cut for time" is thin, the subject is thin. Say so and propose a different slug rather than padding.

**Standalone path.** Read the idea in full. Then, before anything else, **go find the primary sources**. For news, that means the announcement post, the model card, the paper, the pricing page, the changelog, the repo — not the coverage. You cannot plan the article until you know what those documents actually say, and on the reconstruction spine the gap between them and the coverage *is* the article.

## Step 3 · Voice calibration

Read the two voice documents and the calibration sources under **Required references**. The documents state the rules; the examples are what those rules look like on a page.

## Step 4 · Plan: spine, then outline, then shot list

**This step is done before a sentence of the article is written, and it is presented to the user before writing.** The images are not decoration added at the end — the text is written to set each one up, so the shot list has to exist first.

### 4a · Choose one narrative spine

Every spine below is **sequential**: it is one thing happening after another, not a set of points. That is the difference between an article and a long post.

---

**1 · The investigation** — *something broke and you found out why*

1. A dated, concrete scene with a number in it. Not a thesis.
2. The wrong first reading, and why it was reasonable — this is where the reader recognizes themselves.
3. The evidence that did not fit. **First image usually lands here.**
4. The descent: one step per short section, each with its own capture.
5. The turn — what was actually happening.
6. What it means outside your case, and where it stops being true.
7. The real objection, answered.
8. The question.

Use when you watched something fail closely enough to reconstruct it.

---

**2 · The reconstruction** — *this is what actually happened* · **the news spine**

1. What was announced, in one sentence, with no adjective.
2. What the coverage said it meant. **Image: the headline, the chart from the announcement post.**
3. What the primary document actually says. **Images: the page of the paper, the model card, the pricing table, the config default.** This is the spine's center of gravity — expect three or four captures here.
4. The distance between 2 and 3, named plainly.
5. What changes in practice, with numbers.
6. What still cannot be known, said honestly.
7. The question.

Use when something landed this week. **Requires primary sources.** Without them, do not write it.

---

**3 · The test** — *you ran it, here is what happened*

1. The question you wanted answered, and why it matters to someone doing this work.
2. The setup, with its limitations admitted up front. **Image: the environment, the config, the prompt.**
3. What happened, in the order it happened. **Images: the results, and the errors — the failures are more interesting than the successes and get captured too.**
4. The result you did not expect.
5. What you would change about the test itself.
6. The question.

Use when you have access to the thing and can actually run it.

---

**4 · The decision** — *A or B, and what it cost*

1. What was at stake, and the deadline that forced it.
2. The options, honestly, with the price of each. **Images: the comparison, the docs, the pricing.**
3. What you almost chose, and why it was tempting.
4. What you chose, and what it cost you.
5. What would make you switch back.
6. The question.

Use when you paid for a choice. Maximum skin in the game.

---

**The pull rule, whichever spine you pick:** every section ends by opening the question the next section answers. Read your headings in order — if you would not want to read the next one, the sequence is slack.

### 4b · Outline it

Five to nine sections. **Headings are sentences, not labels** — "Retrieval was never the problem", not "Analysis". A reader who scans only the headings should come away with the story.

Write one line per section saying what happens in it. If two adjacent sections say the same kind of thing, merge them.

### 4c · Build the shot list

Before opening a browser, write the shot list as a table in `posts/substack/<slug>/sketch/shotlist.md`:

| # | Anchor — the sentence it lands after | What it must show | Where to capture it | Status |
|---|---|---|---|---|
| cover | — | the mechanism the article is about | arXiv fig. 2 | planned |
| 01 | "the cost tripled without the traffic moving" | the cost curve, with the log axis visible | the provider's status page | planned |

Rules for the list:

- **Three to eight images**, plus the cover. One image per 250–400 words is the right rhythm. Under three in a long article reads as a wall; over eight reads as a deck.
- **Every image answers a question the text just asked.** If you cannot write the anchor sentence, you do not need the image.
- **Every image has a real, linkable source.** If you cannot name where you would capture it, it does not go on the list.
- **Capture failures too**, on the test spine — an error message is more credible than a success screenshot.

### 4d · Present the plan

Show the user the spine, the outline and the shot list before writing:

> "Spine: [name]. Outline: [headings]. Shot list: [N images, sources]. Want changes before I write it?"

This is the cheapest place in the whole run to change direction. Do not skip it.

## Step 5 · Write the article

### The title

**The title is the product** — the email subject line, the feed card, the only thing most of the list ever sees.

A title states the **thesis or the finding**, never the topic:

- **The reframe:** "Compliance is a data problem wearing a legal costume"
- **The negation:** "Why your first AI hire should not be an ML engineer"
- **The named cost:** "What human-in-the-loop actually costs at 40,000 documents a month"
- **The reconstruction:** "What the GPT-5 model card says on page 14"
- **The flat fact**, when the fact is genuinely news and genuinely yours

**Never:** the topic-colon-promise shape ("RAG at scale: a practical guide") — that is a corporate blog and reads like one. A listicle number. A question the article does not answer. Anything the reader cannot parse without opening the email.

### The subtitle

Substack renders it under the title and in the email preview. **It does not restate the title** — it adds the consequence, the cost or the scope the title leaves implicit. One sentence. If deleting it loses no information, rewrite it.

### The opening

**Cold open, on a scene.** The first paragraph is a specific moment with a specific number in it, not a general claim with examples underneath.

Banned, all of them: "In this week's issue", "Welcome back", any greeting, any summary of what is coming, any throat-clearing, any definition of a term the reader knows.

### The body

Write to the outline, and **write each image its runway**. The two or three sentences before an image tell the reader what they are about to look at and why it matters; the sentence after it tells them what to take away. An image dropped in without runway is decoration, and the reader scrolls past it.

Mark image positions inline as you write:

```
![01 — <caption placeholder>](01.png)
```

Substack renders markdown, which is the opposite of LinkedIn's constraint. Use it, and use it for what LinkedIn could not hold:

- `##` for section headings
- Fenced code blocks — real, short, runnable or pasteable. Not pseudocode standing in for an idea.
- Tables, when two things sit on the same axis and the comparison is the point
- Blockquotes for a real log line, trace excerpt, error message or quoted source
- Inline links — **at least three verifiable ones**: the paper, the repo, the doc page, the benchmark
- `**bold**` sparingly, per `base.md` § 5 — for a term being defined, not for a sentence you liked

Paragraph rules from `base.md` § 5 and § 7 hold and matter more at this length: three to six sentences joined by real connectives, the single-sentence paragraph kept as a rare beat. The one-line-per-sentence scroll is a feed artifact; in an email it reads as someone with nothing to say.

**Anticipate one real objection and answer it.** At this length a reader who disagrees has time to compose the counterargument. Get there first, state it fairly, and say what would change your mind.

### Length

**1,200 to 3,000 words is the normal body of an article here, and there is no ceiling when the material holds.** A 4,000-word piece backed by six captures, a table and a decision you paid for is a good article. A 1,400-word piece built out of reasoning alone is padded at 1,400.

The working rule: **every 400 words must introduce something new that is checkable** — a number, a name, a capture, a quote, a link. Stretches that do not, get cut, however well written.

### The close

**The close asks for the reply.** On an owned list a reply is the whole point, and forty replies beat three thousand reactions. This is the one place the format deliberately breaks the LinkedIn rule against asking for anything.

The question has to earn it:

- One **you genuinely cannot answer** and a qualified reader can.
- Asking for **their material, not their opinion** — "What does your team do when the eval suite disagrees with the customer?" not "What do you think?"
- After the story has landed, not instead of landing it.

**No subscribe CTA in the body** — Substack injects its own. **No sign-off block**, no "until next week", no link dump. End on the question.

### Output shape

```
# <title>
### <subtitle>

<the article, with ![NN — caption](NN.png) markers in place>
```

Then a metadata footer — not publishable text, but the piece's record, carried into `final.md`:

```
---
Words: <count>
ACP: <phase>
Spine: <investigation | reconstruction | test | decision>
Artifact: <the thing that could not have been a LinkedIn post>
Images: <N> — see shotlist.md
Sources: <the primary sources used, as URLs>
Reuse of: <slug>   <- reuse path only
```

## Step 6 · Present, iterate, save

Present the full article with title, subtitle, word count and the image markers in place.

Derive the slug from the title (lowercase, hyphens for spaces and punctuation, no accents). On the reuse path, **reuse the sibling's slug** so the thesis lives under one name across `posts/script/`, `posts/linkedin/` and `posts/substack/`.

Save immediately as `posts/substack/<slug>/sketch/v1.md`.

Ask:

> "Ready to lock the text and go capture the images, or corrections first?"

For each correction: apply it, recompute the word count, and create `posts/substack/<slug>/sketch/v(N+1).md` — read the previous version, copy unchanged blocks **verbatim**, apply only the diff. Never regenerate what did not change.

**Offer a title pass explicitly, once, before locking.** The title carries more of this piece's outcome than any paragraph, and it is what the user is most likely to accept passively:

> "Three alternates before we lock it: [A] / [B] / [C]. Keep the current one?"

Lock the text before Step 7. Capturing against a moving draft wastes the session.

## Step 7 · The capture session

Invoke the `claude-in-chrome` skill. Work in a **new tab** (`tabs_create_mcp`). Work the shot list top to bottom in one sitting.

### 7a · Non-negotiables

- **Every image is a real capture from a live page.** Never fabricate one, never build one in HTML, never use an AI-generated image, never use stock. This is the rule the channel's credibility rests on.
- **Primary source, always.** The paper on arXiv over a blog quoting it. The pricing page over a screenshot of the pricing page. The repo over the tweet about the repo. A screenshot of a tweet is never evidence of a fact — go to what the tweet cites.
- **Nothing paywalled, nothing private.** No customer data, no internal dashboards, no logged-in views containing anyone's information.
- **The source URL is recorded for every capture**, in the shot list, at the moment of capture. A capture without a URL cannot be credited and does not ship.

### 7b · Capture craft

- **Zoom in before capturing**, do not capture wide and crop down — cropping throws away the resolution that makes labels readable.
- **Frame the element, not the page.** No browser chrome, no nav bar, no sidebar, no cookie banner, no scrollbar, no half-visible neighboring section.
- **Dismiss the banners first**, then capture. A cookie notice in the corner reads as carelessness.
- **Pick the higher-contrast theme** when the page offers both — usually light, for text and figures.
- **Zoom the browser to 125–150% for text-heavy captures** (a paper paragraph, a config, a log). Default zoom produces text nobody reads in an email.

### 7c · Per-image check, before moving on

Each capture passes all five or gets retaken:

1. **Legible at 50% width** — that is roughly how it renders in a phone email client.
2. **One idea visible.** If the reader has to hunt for what you meant, crop tighter.
3. **Nothing extraneous** — no chrome, no watermark, no unrelated branding.
4. **It answers its anchor sentence.** Read the anchor, look at the image. If it does not land, the shot was wrong, not the crop.
5. **The URL is recorded.**

### 7d · The cover

The cover is seen at the top of the email, on the feed card, and on the social share card cropped to roughly 2:1. So: **landscape, wide, nothing load-bearing in the outer sixth, legible small, high contrast, few elements.**

The strongest cover is almost always **the mechanism the article is about, drawn** — the reader recognizes their own system before reading a word. Otherwise: the chart with the surprising shape, the screenshot of the real artifact, the figure from the cited paper.

Often the best cover is a shot already on your list. Reusing one is fine and better than a weak dedicated cover.

If a LinkedIn post on this thesis already exists and `posts/linkedin/<slug>/image.png` is there, show it and ask whether to reuse it. **Never reuse it silently.**

### 7e · When a shot does not exist

If a planned capture has no real source after a couple of honest attempts, **the text changes, not the image**. Rewrite that passage so it does not depend on the picture, and strike the row from the shot list. Never substitute a decorative image to fill the slot. Say what you dropped and why.

### 7f · Save and record

Save to the slug root, beside the `final.md` they ship with — not in `sketch/`:

- `posts/substack/<slug>/cover.png`
- `posts/substack/<slug>/01.png` … `NN.png`, numbered in reading order

Update `sketch/shotlist.md`: every row gets its final status and its **source URL**.

## Step 8 · Caption, place, and review the pairs

Now the article and the images exist. This step is where a good piece becomes a finished one — do not skip it.

### 8a · Write the captions

Every image gets a caption doing two jobs:

1. **What to look at**, in one clause. Not a description of the image — a direction. "The Y axis is log; the drop between 8k and 32k tokens is the part the announcement chart leaves out."
2. **The source, linked.** "— [OpenAI, GPT-5 model card, p.14](url)"

A caption that only names the image ("Figure 2: the architecture") is wasted space. If the image needs a paper's figure credited, credit it here; Substack has the room LinkedIn does not.

### 8b · Read the article with the images in place

Read it end to end as a reader would, and check three things:

- **Every image has runway** — the sentences before it set it up, the sentence after it says what to take.
- **The rhythm holds.** No two images back to back with a sentence between them. No 900-word stretch with nothing to look at.
- **Nothing is redundant.** If the caption says what the paragraph already said, cut one.

Write the corrections into a new `sketch/v(N+1).md` with the real captions replacing the placeholders.

### 8c · Present the whole thing

Show the user the article and every image with its caption. Ask:

> "Article and [N] images. Anything to reshoot or rewrite?"

If an image gets rejected, go back to 4c and re-answer *what does this image have to show?* before recapturing — a second attempt on the same premise returns the same miss.

## Step 9 · Close out

Everything lives in `posts/substack/<slug>/`. `sketch/` is working material; the root is exactly what ships:

| File | What it is | Written by |
|---|---|---|
| `final.md` | copy of the highest-numbered `sketch/v<N>.md` | this skill, now |
| `cover.png` | the cover from Step 7d | this skill, in 7f |
| `01.png` … `NN.png` | the body captures, in reading order | this skill, in 7f |
| `pt-br.md` | copy of the highest `sketch/pt-br-v<N>.md` | `traduzir`, later, only if asked |

`sketch/` keeps `v<N>.md` and `shotlist.md` as the audit trail. If the user edits a `sketch/v<N>.md` afterwards, re-copy it to `final.md`.

**Notion, by path:**

- **Reuse path: write nothing.** The idea is closed by the Reel and carries a single `Format`. Writing `Substack` over it would erase the primary format and corrupt the calendar picture the database accumulates. Say you are skipping the write, and why.
- **Standalone path:** `Status` → `"Processed"` and `Format` → `"Substack"`. If `Format` has no `Substack` option, **stop and ask the user to add it in the Notion UI**. Do not add it through the MCP: editing a select property's option set there replaces it wholesale and silently clears the value on every row (see `CLAUDE.md`).

## Step 10 · Hand it off

> "Article ready: [title], [N] words, [N] images. Everything is in `posts/substack/<slug>/`.
> To publish: paste `final.md` into the Substack editor, then drag each PNG onto its `![NN — …]` marker and paste the caption underneath. Set `cover.png` as the post cover."

---

## Quality criteria

**The story**
- The title states a thesis or a finding, with no colon-promise and no listicle number
- The subtitle adds the consequence or cost rather than restating the title
- It opens cold, on a specific scene with a number, not on a general claim
- One spine is chosen and the section headings, read in order, tell that story
- Every section ends by opening the question the next one answers
- One real objection is named fairly and answered, with what would change the writer's mind
- The close asks a question the writer genuinely cannot answer, for the reader's material rather than their opinion
- No subscribe CTA and no sign-off block in the body

**The images**
- Three to eight body images plus a cover, roughly one per 250–400 words
- **Every one is a real browser capture from a primary source.** No stock, no AI-generated art, no HTML-built diagram, no screenshot of a tweet standing in for a fact
- Every one lands where the text just raised the question it answers, with runway before and a takeaway after
- Every one is legible at 50% width, framed on the element, free of chrome, banners and watermarks
- Every one has a caption that directs the eye and links its source
- The cover is landscape, survives a 2:1 crop, and shows the article's actual subject
- Every source URL is recorded in `sketch/shotlist.md`

**What makes it an article**
- It carries at least one artifact that could not have been a LinkedIn post
- At least three inline links a reader could go verify
- Every 400 words introduces something checkable — a number, a name, a capture, a quote
- On the reuse path, not one sentence carries over verbatim from the Reel, and the material is what the 60-second version had to cut

**The voice**
- Paragraph length varies; the single-sentence paragraph is a rare beat, not the default
- Sentences inside a paragraph are joined by real connectives, not stacked
- Every section carries a proper noun or number a reader could verify
- The writer is exposed somewhere: a decision made, a price paid, a wrong first guess admitted
- No hype, no motivational register, no untranslated jargon

**The files**
- `posts/substack/<slug>/` root holds `final.md`, `cover.png` and `01.png`…`NN.png`
- `sketch/` holds the `v<N>.md` history and `shotlist.md` with every source URL
- Notion was written to on the standalone path only

If any criterion fails, fix it before presenting.

---

## Out of scope

- Does not capture raw ideas (that is `capture-idea`)
- Does not write Reel scripts, carousels, threads or LinkedIn posts — their own skills
- Does not translate: `traduzir` adapts the finished `final.md` on its own parallel sequence
- Does not design or generate artwork. Every image is captured from something that already exists. A piece needing composed art in the Alvinegro system is a carousel, not an article
- Does not publish: pasting into Substack is manual
