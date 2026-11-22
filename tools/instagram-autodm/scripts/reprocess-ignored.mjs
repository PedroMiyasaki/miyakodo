import { spawnSync } from "node:child_process";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { buildModule } from "../tests/worker-harness.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const toolRoot = path.resolve(here, "..");
const WINDOW_MS = 7 * 24 * 60 * 60 * 1000;
const RECHECK_MS = 4000;

const args = new Set(process.argv.slice(2));
const send = args.has("--send") && !args.has("--dry-run");

const matcher = await buildModule(path.join(toolRoot, "src/keyword-match.ts"));
const { isStrictKeyword, isBasicallyKeyword } = matcher.module;

try {
  const plan = await planReplies();
  for (const line of plan.lines) console.log(line);
  console.log(plan.summary);
  if (!send) {
    console.log("Nada foi enviado. Use --send para enviar quem está dentro dos 7 dias.");
  } else {
    console.log(await deliver(plan.actions));
  }
} finally {
  await matcher.dispose();
}

async function planReplies() {
  const env = await readDevVars();
  const owner = await ownerUsername();
  const rules = (await d1("SELECT id, keywords, reply_text, public_reply_text, follow_prompt_text, media_id, match_mode, active, followers_only, label FROM rules WHERE active = 1"))
    .map(hydrateRule);
  const comments = await d1("SELECT comment_id, media_id, username, comment_text, author_id, received_at FROM comment_events WHERE status = 'ignored_no_keyword' ORDER BY received_at");
  const deliveries = await d1("SELECT rule_id, recipient_id, status FROM material_deliveries");
  const taken = new Set(deliveries.map((row) => `${row.rule_id}:${row.recipient_id}`));
  const now = Date.now();
  const lines = [];
  const actions = [];
  for (const comment of comments) {
    const rule = rules.find((item) => item.mediaId === comment.media_id && matchKeyword(comment.comment_text, item));
    if (!rule) continue;
    const username = comment.username || "(sem usuário)";
    const age = ageMs(comment.received_at, now);
    if (owner && username.toLowerCase().replace(/^@/, "") === owner) {
      lines.push(`pular @${username}  comentário do dono  "${comment.comment_text}"`);
      continue;
    }
    if (age == null || age > WINDOW_MS) {
      lines.push(`pular @${username}  fora da janela de 7 dias  "${comment.comment_text}"`);
      continue;
    }
    const recipientId = comment.author_id || (comment.username ? `username:${comment.username.toLowerCase()}` : "");
    if (!recipientId) {
      lines.push(`pular @${username}  sem autor  "${comment.comment_text}"`);
      continue;
    }
    if (taken.has(`${rule.id}:${recipientId}`)) {
      lines.push(`pular @${username}  já tem entrega nesta regra  "${comment.comment_text}"`);
      continue;
    }
    const decision = /^\d{1,40}$/.test(recipientId)
      ? await decideFollower(env, recipientId)
      : "unknown";
    const action = decision === "follower" ? "material" : decision === "not_follower" ? "pedido para seguir" : "botão para confirmar";
    lines.push(`enviar @${username}  ${action}  regra ${rule.label}  "${comment.comment_text}"`);
    actions.push({ comment, rule, recipientId, decision });
    taken.add(`${rule.id}:${recipientId}`);
  }
  const summary = actions.length
    ? `${actions.length} pessoa(s) receberiam mensagem.`
    : "Ninguém receberia mensagem.";
  return { lines, summary, actions, env, failed: false };
}

function matchKeyword(text, rule) {
  const matches = rule.matchMode === "strict" ? isStrictKeyword : isBasicallyKeyword;
  return rule.keywords.some((keyword) => matches(text, keyword));
}

function hydrateRule(row) {
  const parsed = JSON.parse(row.keywords);
  return {
    id: row.id,
    label: row.label,
    keywords: Array.isArray(parsed) ? parsed : [],
    replyText: row.reply_text,
    publicReplyText: row.public_reply_text,
    followPromptText: row.follow_prompt_text,
    mediaId: row.media_id,
    matchMode: row.match_mode || "loose"
  };
}

function ageMs(receivedAt, now) {
  if (!receivedAt) return null;
  const parsed = Date.parse(receivedAt.includes("T") ? receivedAt : receivedAt.replace(" ", "T") + "Z");
  return Number.isFinite(parsed) ? now - parsed : null;
}

async function decideFollower(env, recipientId) {
  const first = await followerStatus(env, recipientId);
  if (first === true) return "follower";
  await new Promise((resolve) => setTimeout(resolve, RECHECK_MS));
  const second = await followerStatus(env, recipientId);
  if (second === true) return "follower";
  if (second === false) return "not_follower";
  return "unknown";
}

async function followerStatus(env, recipientId) {
  const url = new URL(`https://graph.instagram.com/v25.0/${encodeURIComponent(recipientId)}`);
  url.searchParams.set("fields", "username,is_user_follow_business");
  url.searchParams.set("access_token", env.INSTAGRAM_ACCESS_TOKEN);
  const response = await fetch(url);
  if (!response.ok) return null;
  const data = await response.json();
  return typeof data.is_user_follow_business === "boolean" ? data.is_user_follow_business : null;
}

async function deliver(actions) {
  const env = await readDevVars();
  let sent = 0;
  for (const action of actions) {
    const message = messageFor(action);
    const privateReply = await graphPost(env, `${env.IG_USER_ID}/messages`, {
      recipient: { comment_id: action.comment.comment_id },
      message
    });
    if (!privateReply.ok) {
      console.log(`falhou @${action.comment.username}  ${privateReply.error}`);
      continue;
    }
    if (action.decision === "follower" && action.rule.publicReplyText) {
      const reply = await graphPost(env, `${action.comment.comment_id}/replies`, null, {
        message: action.rule.publicReplyText
      });
      if (!reply.ok) console.log(`direct saiu, comentário público falhou @${action.comment.username}  ${reply.error}`);
    }
    const status = action.decision === "follower" ? "sent" : action.decision === "not_follower" ? "awaiting_follow" : "prompted";
    const delivery = action.decision === "follower" ? "delivered" : action.decision === "not_follower" ? "awaiting_follow" : "prompted";
    const now = new Date().toISOString();
    await d1(`UPDATE comment_events SET matched = 1, status = '${status}', matched_rule_id = ${action.rule.id}, matched_keyword = ${sql(action.rule.keywords[0])}, rule_label = ${sql(action.rule.label)}, sent_at = ${sql(now)} WHERE comment_id = ${sql(action.comment.comment_id)}`);
    await d1(`INSERT OR IGNORE INTO material_deliveries (rule_id, recipient_id, comment_id, status, created_at, updated_at, material_sent_at) VALUES (${action.rule.id}, ${sql(action.recipientId)}, ${sql(action.comment.comment_id)}, ${sql(delivery)}, ${sql(now)}, ${sql(now)}, ${action.decision === "follower" ? sql(now) : "NULL"})`);
    sent += 1;
    console.log(`enviado @${action.comment.username}`);
  }
  return `${sent} envio(s).`;
}

function messageFor(action) {
  if (action.decision === "follower") return { text: action.rule.replyText };
  const title = action.decision === "not_follower" ? "Já segui" : "Quero o material";
  const text = action.decision === "not_follower"
    ? (action.rule.followPromptText || "Me segue por aqui para eu te enviar o material.")
    : "Toque no botão para receber o material.";
  const step = action.decision === "not_follower" ? "followed" : "material";
  return {
    attachment: {
      type: "template",
      payload: {
        template_type: "button",
        text,
        buttons: [{ type: "postback", title, payload: `GATE:v1:${action.rule.id}:${action.comment.comment_id}:${step}` }]
      }
    }
  };
}

async function graphPost(env, pathName, jsonBody, form) {
  const url = new URL(`https://graph.instagram.com/v25.0/${pathName}`);
  const headers = { authorization: `Bearer ${env.INSTAGRAM_ACCESS_TOKEN}` };
  let body;
  if (jsonBody) {
    headers["content-type"] = "application/json";
    body = JSON.stringify(jsonBody);
  } else {
    url.searchParams.set("access_token", env.INSTAGRAM_ACCESS_TOKEN);
    for (const [key, value] of Object.entries(form)) url.searchParams.set(key, value);
  }
  const response = await fetch(url, { method: "POST", headers, body });
  if (response.ok) return { ok: true };
  const payload = await response.json().catch(() => ({}));
  return { ok: false, error: payload.error?.message || `HTTP ${response.status}` };
}

function sql(value) {
  return `'${String(value).replaceAll("'", "''")}'`;
}

async function ownerUsername() {
  const source = await readFile(path.join(toolRoot, "wrangler.jsonc"), "utf8");
  const match = /"OWNER_IG_USERNAME"\s*:\s*"([^"]+)"/.exec(source);
  return match?.[1]?.trim().toLowerCase().replace(/^@/, "") || "";
}

async function readDevVars() {
  const values = {};
  for (const line of (await readFile(path.join(toolRoot, ".dev.vars"), "utf8")).split(/\r?\n/)) {
    if (!line || line.startsWith("#") || !line.includes("=")) continue;
    const index = line.indexOf("=");
    values[line.slice(0, index)] = line.slice(index + 1).trim();
  }
  if (!values.INSTAGRAM_ACCESS_TOKEN || !values.IG_USER_ID) {
    throw new Error("Faltam INSTAGRAM_ACCESS_TOKEN ou IG_USER_ID em .dev.vars.");
  }
  return values;
}

async function d1(command) {
  const bin = path.join(toolRoot, "node_modules", "wrangler", "bin", "wrangler.js");
  const result = spawnSync(process.execPath, [bin, "d1", "execute", "instagram-autodm", "--remote", "--json", "--command", command], {
    cwd: toolRoot,
    encoding: "utf8"
  });
  if (result.status !== 0) throw new Error((result.stderr || result.stdout || "wrangler falhou").trim());
  const parsed = JSON.parse(result.stdout);
  return Array.isArray(parsed) ? parsed.flatMap((item) => item.results ?? []) : parsed.results ?? [];
}
