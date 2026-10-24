import assert from "node:assert/strict";
import { after, before, test } from "node:test";
import { buildModule, buildWorker, createHarness } from "./worker-harness.mjs";

let built;
let poller;
before(async () => {
  built = await buildWorker();
  poller = await buildModule("src/comment-poll.ts");
});
after(async () => {
  await built?.dispose();
  await poller?.dispose();
});

test("o permalink devolve o código do post", () => {
  const { shortcodeFromPermalink } = poller.module;
  assert.equal(shortcodeFromPermalink("https://www.instagram.com/p/DeU8X1fhF6a/"), "DeU8X1fhF6a");
  assert.equal(shortcodeFromPermalink("https://www.instagram.com/reel/DehPW4yCR7W/?igsh=1"), "DehPW4yCR7W");
  assert.equal(shortcodeFromPermalink("https://example.com/p/DeU8X1fhF6a/"), null);
});

test("o cron de reserva fica desligado e, ligado, passa pelo mesmo pipeline", async (t) => {
  const off = await createHarness(built.worker, { COMMENT_POLL_ENABLED: "false", DRY_RUN: "true" });
  t.after(() => off.dispose());
  await built.worker.scheduled({ scheduledTime: Date.now(), cron: "*/5 * * * *" }, off.env);
  assert.equal(off.calls.length, 0);

  const h = await createHarness(built.worker, {
    COMMENT_POLL_ENABLED: "true",
    DRY_RUN: "true",
    GRAPH_API_BASE: "https://graph.instagram.com/v25.0",
    OWNER_IG_USERNAME: "pedro.miyasaki.ia"
  });
  t.after(() => h.dispose());
  await h.db.prepare(
    `INSERT INTO rules (
      label, channels, keywords, reply_text, public_reply_text, active, created_at, updated_at,
      media_id, shortcode, source_key, followers_only, follow_prompt_text, match_mode
    ) VALUES ('evals', '["comments"]', '["evals"]', 'material', 'Enviei no direct.', 1, 'now', 'now',
      '17900011110000001', 'DeU8X1fhF6a', 'DeU8X1fhF6a:evals', 1, 'segue', 'strict')`
  ).run();
  const recent = new Date().toISOString();
  const old = new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString();
  h.setResponder(() => Response.json({
    data: [
      { id: "poll-yes", text: "EVALS!", username: "reader", timestamp: recent, from: { id: "17895551212000001", username: "reader" } },
      { id: "poll-no", text: "quero evals", username: "reader", timestamp: recent, from: { id: "17895551212000009", username: "reader" } },
      { id: "poll-old", text: "evals", username: "reader", timestamp: old, from: { id: "17895551212000008", username: "reader" } },
      { id: "poll-owner", text: "evals", username: "pedro.miyasaki.ia", timestamp: recent, from: { id: "17895550000000002", username: "pedro.miyasaki.ia" } }
    ]
  }));
  await built.worker.scheduled({ scheduledTime: Date.now(), cron: "*/5 * * * *" }, h.env);
  assert.equal(h.query("SELECT status FROM comment_events WHERE comment_id = 'poll-yes'").status, "dry_run_matched");
  assert.equal(h.query("SELECT status FROM comment_events WHERE comment_id = 'poll-no'").status, "ignored_no_keyword");
  assert.equal(h.query("SELECT comment_id FROM comment_events WHERE comment_id = 'poll-old'"), null);
  assert.equal(h.query("SELECT status FROM comment_events WHERE comment_id = 'poll-owner'").status, "ignored_owner");
  assert.equal(h.calls.filter((call) => call.method === "POST").length, 0);
  await built.worker.scheduled({ scheduledTime: Date.now(), cron: "*/5 * * * *" }, h.env);
  assert.equal(h.queryAll("SELECT comment_id FROM comment_events WHERE comment_id = 'poll-yes'").length, 1);
});
