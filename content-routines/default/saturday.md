# Saturday — 5 scripts, 5 recordings, first edit pass

**Ends with:** 5 scripts in `posts/script/`, 5 videos in `video/inputs/`, 5 first cuts rendering. What stays open depends on the mode.
**Publishes nothing.** Context and the 🔥 test: [README](README.md).

**Mode — pick before opening anything.** `default` unless you want speed.

| Mode | When | What you open |
|---|---|---|
| **default** | Isolation. One conversation per piece. | 5 agent sessions |
| **multitask** | Speed. One conversation running the day. | 1 session spanning 5 agents |

- [ ] **Read the latest [aprendizados](../aprendizados.md)** — top entries first, before anything else.
  ⚠️ Whatever broke last week repeats today unless you read it now. New mistake today → new entry there.

- [ ] **Pick 5 phase-A ideas** from the Ideas database (`ACP Phase` = `A · Audience`), all passing the 🔥 test.
  ⚠️ No perishable news — a reel recorded today may not air until Thursday.
  🖋 Try to leave at least one of the 5 with real depth under it — a number, a decision you made, code you can paste. Sunday's article usually comes from one of them. Not a hard rule: news from the week can take that slot instead.

- [ ] **Write the 5 scripts.** Iterate to "done" in all 5.
  🔥 Spend the iterations on the first two lines. A hook that doesn't stop the scroll invalidates the rest.
  - **default:** Open 5 agent sessions, one per script, and run `write-script` in each.
  - **multitask:** Open 1 coordinating session. It spans 5 agents, one per script, runs `write-script` in each, and owns the process — you talk to the session, not to the five agents. The agents coordinate through it (shared slugs, no colliding hooks, no two agents on the same piece).

- [ ] **Record all 5 on the teleprompter, in one batch** — same light, same clothes, same setup.
  💡 Record a 6th if the day allows. It skips the schedule and becomes stock.

- [ ] **Move the recordings off your phone** into `video/inputs/`, each file **named after its script slug**.
  ⚠️ Every step from here on is addressed by slug. Don't leave five unnamed exports.

- [ ] **Fire the first edit pass** in the same layout you wrote in. Run `edit-video` once per script, in the fitting mode:
  - news-driven → `news`
  - thesis / position → `baseline`
  - burned-in captions → only if you ask (`subtitles` is opt-in; Instagram makes its own)
  **Fire and leave.** Don't review tonight — that's tomorrow's first job.
  - **default:** fire it in those same 5 agent sessions.
  - **multitask:** fire it from the coordinating session — it dispatches `edit-video` to each of the 5 agents.

- [ ] **Leave a resume note for Sunday.**
  - **default:** which agent session owns which slug. Tomorrow resumes all 5.
  - **multitask:** that this weekend is multitask, and the coordinating session's name. Tomorrow resumes that one session.

Next: **[Sunday](sunday.md)**
