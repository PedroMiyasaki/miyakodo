# Sunday — review the cuts, write LinkedIn and the article, schedule the week

**Ends with:** 5 reels in `posts/script/<slug>/` (each script folder holding `reels.mp4`, `caption.md` and `cover.png`), 3 LinkedIn posts, 1 Substack article, 9 posts scheduled.
**Sessions at peak:** default — 9 (1 Substack + 5 resumed + 3 LinkedIn) · multitask — 5 (1 Substack + 1 resumed + 3 LinkedIn). Context: [README](README.md).

## Substack — fire it first, it runs all day

The article is the longest piece of the week and it publishes today. Start it before you watch a single cut, then check in on it between reviews.

- [ ] **Pick the subject.** Either the deepest of the 5 ideas you recorded, or **news from this week** — the article publishes today, so nothing here is too perishable.
  Pick for material, not for hook: the right subject is the one where you can already name three things you could go capture.
  ⚠️ News only works if you can reach a primary source — the paper, the model card, the pricing page. Without one there is no article, only the fifth summary of the same announcement.

- [ ] **Open 1 agent session, run** `write-substack` on it. Then leave it and go watch the cuts.

- [ ] **Approve the plan when it comes back** — spine, outline, shot list. Do this between two cut reviews; it takes two minutes.
  🖋 This is the cheapest place all day to change direction. Read the shot list: if you can't picture the image, the agent can't capture it.

- [ ] **Iterate the text to locked, then let it run the capture session.** 3 to 8 real browser captures plus a cover.
  ⚠️ Every image is a real capture from a primary source. If the agent offers a stock photo or a diagram it built, that's a bug — send it back.

- [ ] **Review the article with the images in place**, not the text alone. Each image needs runway before it and a takeaway after.

- [ ] **Spend one round on the title alone.** It's the email subject line and the only thing most of the list will ever read.



## Review the 5 cuts

- [ ] **Resume yesterday's layout.** Reopen everything you need before reviewing any cut.
  - **default:** yesterday's 5 agent sessions, one per slug.
  - **multitask:** yesterday's coordinating session. It already knows the five slugs — don't open five new ones.

- [ ] **Watch each cut, hand back notes in plain language** — dragging opening, repeated point, dead pause, cut landing on the wrong word. The session that wrote the script knows it, so refer to content, not timestamps. Iterate until postable.
  🔥 First two seconds: hard cut, zero intro. If the opening drags, that's the first note.
  A cut that needs nothing is finished. Accept it and move on.

- [ ] **Check:** `video/inputs/` empty, this week's 5 script folders in `posts/script/` each holding its video, caption and cover.



## LinkedIn (3 new agent sessions, in parallel)

- [ ] **Pick the 3 most technical of the 5 ideas you recorded.** Reuse beats a fresh idea from the bank.

- [ ] **Open 3 agent sessions, run** `build-linkedin` on each. Iterate to "done" (text + image).
  Presence, not reach. Don't force a hook onto them.

- [ ] **If one of the 3 shares the article's thesis, hand that agent the article.** Give it `posts/substack/<slug>/final.md` so it doesn't repeat the piece, and have it close on the link.
  🖋 That post is the subscription engine: cold LinkedIn readers, one click from the list.



## Schedule

- [ ] **Build the grid before opening any app.** The window starts today.

  | Day             | Instagram          | LinkedIn   | Substack  |
  | --------------- | ------------------ | ---------- | --------- |
  | **Sun (today)** | reel 1 🔥          | —          | article 🖋 |
  | Mon             | reel 2 🔥          | LinkedIn 1 | —         |
  | Tue             | reel 3 🔥          | —          | —         |
  | Wed             | reel 4 🔥          | LinkedIn 2 | —         |
  | Thu             | reel 5 🔥          | —          | —         |
  | Fri             | stock reel, if any | LinkedIn 3 | —         |
  | Sat             | —                  | —          | —         |

  Most perishable reel first. News today or Monday; a timeless thesis survives to Thursday.
  ⏱️ Reel 1 goes out today — if the slot has passed, publish it now instead of scheduling.
  🖋 The article goes out today too, written today. That zero lag is what lets it be news.

- [ ] **Publish the Substack article.** Everything is in `posts/substack/<slug>/`: paste `final.md`, drag each PNG onto its `![NN — …]` marker, paste the captions, set `cover.png` as the cover.
  ⚠️ Substack sends an email. A typo reaches the whole list and can't be edited after send — read the title and the first paragraph once more before you hit publish.

- [ ] **Schedule the 5 reels** on Instagram, each with its script's caption.

- [ ] **Schedule the 3 LinkedIn posts.** If one links the article, put that one on Monday, right behind it.

- [ ] **Re-check the whole grid before closing.** A post on the wrong day only surfaces Thursday, too late to fix.

- [ ] **Close the ideas in Notion:** `Status` → `Processed`.
  ⚠️ A reused idea can only carry one `Format` — record `Reel`. The article adds nothing here; `write-substack` deliberately skips the Notion write when it reuses a thesis. If the article came from fresh news instead, that idea closes on its own as `Substack`.

Next: **[Saturday](saturday.md)**
