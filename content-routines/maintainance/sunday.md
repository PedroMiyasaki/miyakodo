# Sunday — the article, 3 carousels, 2 LinkedIn posts, schedule the week

**Ends with:** 7 Instagram carousels, 3 LinkedIn posts, 1 Substack article and all 11 posts scheduled.
**No recording and no video editing.**
**Agent teams are mandatory.** Resume Saturday's coordinator so assignments and slugs stay consistent.

- [ ] **Resume Saturday's coordinating session.**
  Confirm the 3 carousel drafts awaiting correction, their original agents, the 2 LinkedIn reuse assignments, yesterday's 5 finished slugs and the article subject you left picked.

## Substack — fire it first, it runs all day

The article is the longest piece of the week and it publishes today. Start it before the first carousel review, then check in between reviews.

- [ ] **Confirm the subject** from yesterday's note — one of the week's theses, or **news from this week**. The article publishes today, so nothing here is too perishable.
  Pick for material, not for hook: the right subject is the one where you can already name three things you could go capture.
  ⚠️ News only works if you can reach a primary source — the paper, the model card, the pricing page. Without one there is no article, only the fifth summary of the same announcement.

- [ ] **Open 1 agent session, run** `write-substack` on it. Then leave it and start the carousel reviews.

- [ ] **Approve the plan when it comes back** — spine, outline, shot list. Do this between two reviews; it takes two minutes.
  🖋 This is the cheapest place all day to change direction. Read the shot list: if you can't picture the image, the agent can't capture it.

- [ ] **Iterate the text to locked, then let it run the capture session.** 3 to 8 real browser captures plus a cover.
  ⚠️ Every image is a real capture from a primary source. If the agent offers a stock photo or a diagram it built, that's a bug — send it back.

- [ ] **Review the article with the images in place**, not the text alone. Each image needs runway before it and a takeaway after.

- [ ] **Spend one round on the title alone.** It's the email subject line and the only thing most of the list will ever read.

## Review and correction — 3 carousels

The first drafts already exist. Resume their original agents so each correction becomes a new local version instead of a rewrite.

- [ ] **Put the 3 remaining carousels through the full correction loop, one review at a time:**
  1. Read the complete slide copy and caption.
  2. Give concrete notes to that piece's agent.
  3. Review the revised version; repeat until the text is approved.
  4. Inspect every rendered slide for hierarchy, overflow, awkward breaks, repetition and weak visual composition.
  5. Send visual or copy corrections back to the same agent and re-render.
  6. Say "done" only when both copy and rendered slides are publishable.

  While you review the next piece, agents revise the ones already returned. Never use two agents on the same piece.

## LinkedIn — 2 agents in parallel

- [ ] **Dispatch 2 LinkedIn agents**, one reserved reuse idea per agent. Each runs `build-linkedin`.
  Reuse the thesis, not the carousel wording.

- [ ] **Put both LinkedIn posts through the full correction loop:**
  1. Review each complete text and return notes.
  2. Review the revised version; repeat until the writing is approved.
  3. Review each chosen image with its post.
  4. Request replacements or text corrections until each pair is publishable.

  A first draft does not count as finished. Use the agents' revision time to review the other post or finish a carousel.

- [ ] **If one of the 3 LinkedIn posts shares the article's thesis, hand that agent the article.** Give it `posts/substack/<slug>/final.md` so it doesn't repeat the piece, and have it close on the link.
  🖋 That post is the subscription engine: cold LinkedIn readers, one click from the list.

- [ ] **Check the complete week's output:**
  - 7 carousel folders in `posts/carousel/`, each with `final.md` and rendered slides
  - 3 LinkedIn folders in `posts/linkedin/`, each with `final.md` and `image.png`
  - 1 Substack folder in `posts/substack/`, with `final.md`, `cover.png` and the numbered captures
  - no piece still awaiting your review or an agent revision

## Schedule

- [ ] **Start scheduling only after all 11 pieces are approved.**
  Scheduling is protected work, not the place to discover unfinished copy or broken slides.

- [ ] **Build the grid before opening any app.** The window starts today.

  | Day             | Instagram  | LinkedIn   | Substack  |
  | --------------- | ---------- | ---------- | --------- |
  | **Sun (today)** | carousel 1 | —          | article 🖋 |
  | Mon             | carousel 2 | LinkedIn 1 | —         |
  | Tue             | carousel 3 | —          | —         |
  | Wed             | carousel 4 | LinkedIn 2 | —         |
  | Thu             | carousel 5 | —          | —         |
  | Fri             | carousel 6 | LinkedIn 3 | —         |
  | Sat             | carousel 7 | —          | —         |

  Put the most timely carousel first. Keep the strongest evergreen piece for the end of the window.
  ⏱️ Carousel 1 goes out today — if the slot has passed, publish it now instead of scheduling it.
  🖋 The article goes out today too, written today. That zero lag is what lets it be news.

- [ ] **Publish the Substack article.** Everything is in `posts/substack/<slug>/`: paste `final.md`, drag each PNG onto its `![NN — …]` marker, paste the captions, set `cover.png` as the cover.
  ⚠️ Substack sends an email. A typo reaches the whole list and can't be edited after send — read the title and the first paragraph once more before you hit publish.

- [ ] **Schedule the 7 carousels** on Instagram with their captions.

- [ ] **Schedule the 3 LinkedIn posts.** If one links the article, put that one on Monday, right behind it.

- [ ] **Re-check the whole grid before closing.**
  Confirm dates, channels, captions, slide order, LinkedIn images and the article's captures.

- [ ] **Close the 7 ideas in Notion:** `Status` → `Processed`, `Format` → `IG Carousel`.
  ⚠️ The 3 reused ideas can carry only one `Format`; keep the primary Instagram format. The article adds nothing here; `write-substack` deliberately skips the Notion write when it reuses a thesis. If the article came from fresh news instead, that idea closes on its own as `Substack`.

Next: **[Saturday](saturday.md)**
