import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { after, before, test } from "node:test";
import { buildModule, buildWorker, createHarness } from "./worker-harness.mjs";
import { parseRespostasMarkdown } from "../scripts/parse-respostas.mjs";

let built;
let gate;
before(async () => {
  built = await buildWorker();
  gate = await buildModule("src/follower-gate.ts");
});
after(async () => {
  await built?.dispose();
  await gate?.dispose();
});

const MEDIA = "17900011110000001";
const OTHER_MEDIA = "17900011110000099";
const AUTHOR = "17895551212000001";
const GRAPH = "https://graph.instagram.com/v25.0";

async function draft() {
  const markdown = await readFile("tests/fixtures/evals.md", "utf8");
  return parseRespostasMarkdown(markdown, "fixtures/evals.md").drafts[0];
}

async function install(t, overrides = {}) {
  const h = await createHarness(built.worker, {
    GRAPH_API_BASE: GRAPH,
    FOLLOWER_RECHECK_MS: "0",
    OWNER_IG_USERNAME: "pedro.miyasaki.ia",
    DRY_RUN: "false",
    ...overrides
  });
  t.after(() => h.dispose());
  const rule = await draft();
  const inserted = await h.db.prepare(
    `INSERT INTO rules (
      label, channels, keywords, reply_text, public_reply_text, active, created_at, updated_at,
      media_id, shortcode, source_key, followers_only, follow_prompt_text, match_mode
    ) VALUES (?, '["comments"]', ?, ?, ?, 1, 'now', 'now', ?, ?, ?, 1, ?, 'strict')`
  ).bind(
    rule.label,
    JSON.stringify([rule.keyword]),
    rule.replyText,
    rule.publicReplyText,
    MEDIA,
    rule.shortcode,
    rule.sourceKey,
    rule.followPromptText
  ).run();
  return { h, rule, ruleId: Number(inserted.meta.last_row_id) };
}

function comment(id, text, media = MEDIA, username = "reader", authorId = AUTHOR) {
  return {
    object: "instagram",
    entry: [{
      id: "test-instagram-account",
      changes: [{ field: "comments", value: { id, text, from: { id: authorId, username }, media: { id: media } } }]
    }]
  };
}

function postback(ruleId, commentId, authorId = AUTHOR, step = "material") {
  return {
    object: "instagram",
    entry: [{
      id: "test-instagram-account",
      messaging: [{
        sender: { id: authorId },
        recipient: { id: "test-instagram-account" },
        timestamp: Date.now(),
        postback: { title: "Quero o material", payload: `GATE:v1:${ruleId}:${commentId}:${step}` }
      }]
    }]
  };
}

function profiles(h, values) {
  const queue = [...values];
  h.setResponder((call) => {
    if (call.method === "GET") {
      const value = queue.shift();
      if (typeof value !== "boolean") return Response.json({});
      return Response.json({ username: "reader", is_user_follow_business: value });
    }
    return Response.json({ id: "reply-id", message_id: "dm-id" });
  });
}

const messagePosts = (h) => h.calls.filter((call) => call.method === "POST" && call.url.pathname.endsWith("/messages"));
const publicReplies = (h) => h.calls.filter((call) => call.method === "POST" && call.url.pathname.endsWith("/replies"));

test("a decisão espera uma segunda checagem antes de negar", async () => {
  const { decideFollower } = gate.module;
  const calls = [];
  const follower = await decideFollower(async () => {
    calls.push("check");
    return calls.length === 1 ? false : true;
  }, async () => { calls.push("wait"); });
  assert.deepEqual(calls, ["check", "wait", "check"]);
  assert.equal(follower, "follower");
  assert.equal(await decideFollower(async () => false, async () => {}), "not_follower");
  assert.equal(await decideFollower(async () => null, async () => {}), "unknown");
  assert.equal(await decideFollower(async () => true, async () => { throw new Error("não deveria esperar"); }), "follower");
});

test("comentário de uma palavra entrega o texto do arquivo para quem já segue", async (t) => {
  const { h, rule, ruleId } = await install(t);
  profiles(h, [true]);
  await h.webhook(comment("c-owner", "EVALS!", MEDIA, "pedro.miyasaki.ia", "17895550000000002"));
  await h.webhook(comment("c-phrase", "quero evals"));
  await h.webhook(comment("c-other", "EVALS!", OTHER_MEDIA));
  await h.webhook(comment("c-yes", "EVALS!"));
  assert.equal(h.query("SELECT status FROM comment_events WHERE comment_id = 'c-owner'").status, "ignored_owner");
  assert.equal(h.query("SELECT status FROM comment_events WHERE comment_id = 'c-phrase'").status, "ignored_no_keyword");
  assert.equal(h.query("SELECT status FROM comment_events WHERE comment_id = 'c-other'").status, "ignored_no_keyword");
  assert.equal(messagePosts(h).length, 1);
  assert.equal(messagePosts(h)[0].body.recipient.comment_id, "c-yes");
  assert.equal(messagePosts(h)[0].body.message.text, rule.replyText);
  assert.equal(publicReplies(h).length, 1);
  assert.equal(publicReplies(h)[0].url.searchParams.get("message"), rule.publicReplyText);
  assert.equal(h.query("SELECT status FROM material_deliveries WHERE rule_id = ?", ruleId).status, "delivered");
  assert.equal(h.query("SELECT status FROM comment_events WHERE comment_id = 'c-yes'").status, "sent");

  const before = h.calls.length;
  await h.webhook(comment("c-again", "evals", MEDIA, "reader", AUTHOR));
  assert.equal(h.query("SELECT status FROM comment_events WHERE comment_id = 'c-again'").status, "ignored_already_delivered");
  assert.equal(h.calls.length, before);
});

test("quem não segue recebe o pedido e o botão Já segui, sem o material", async (t) => {
  const { h, rule, ruleId } = await install(t);
  profiles(h, [false, false, true]);
  await h.webhook(comment("c-no", "evals"));
  assert.equal(publicReplies(h).length, 0);
  assert.equal(messagePosts(h).length, 1);
  const follow = messagePosts(h)[0].body.message.attachment.payload;
  assert.equal(follow.text, rule.followPromptText);
  assert.equal(follow.buttons[0].title, "Já segui");
  assert.equal(follow.buttons[0].payload, `GATE:v1:${ruleId}:c-no:followed`);
  assert.equal(JSON.stringify(messagePosts(h)[0].body).includes(rule.link), false);
  assert.equal(h.query("SELECT status FROM material_deliveries WHERE comment_id = 'c-no'").status, "awaiting_follow");

  await h.webhook(postback(ruleId, "c-no", AUTHOR, "followed"));
  assert.equal(messagePosts(h).at(-1).body.message.text, rule.replyText);
  assert.equal(publicReplies(h).length, 1);
  assert.equal(h.query("SELECT status FROM material_deliveries WHERE comment_id = 'c-no'").status, "delivered");
});

test("uma checagem negativa seguida de positiva entrega o material", async (t) => {
  const { h, rule } = await install(t);
  profiles(h, [false, true]);
  await h.webhook(comment("c-lag", "evals"));
  const lookups = h.calls.filter((call) => call.method === "GET" && call.url.pathname.endsWith(`/${AUTHOR}`));
  assert.equal(lookups.length, 2);
  assert.equal(messagePosts(h).at(-1).body.message.text, rule.replyText);
  assert.equal(publicReplies(h).length, 1);
  assert.equal(h.query("SELECT status FROM material_deliveries WHERE comment_id = 'c-lag'").status, "delivered");
});

test("falha da API não trata a pessoa como quem não segue", async (t) => {
  const { h, rule, ruleId } = await install(t);
  profiles(h, [null, null, null, null]);
  await h.webhook(comment("c-unknown", "evals"));
  await h.webhook(postback(ruleId, "c-unknown"));
  assert.equal(publicReplies(h).length, 0);
  const follow = messagePosts(h).at(-1).body.message.attachment.payload;
  assert.match(follow.text, /Não consegui confirmar/);
  assert.equal(JSON.stringify(follow).includes(rule.link), false);
  assert.equal(h.query("SELECT status FROM material_deliveries WHERE comment_id = 'c-unknown'").status, "prompted");
});
