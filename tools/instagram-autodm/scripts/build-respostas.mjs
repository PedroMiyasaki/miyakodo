import { spawnSync } from "node:child_process";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadRespostas } from "./parse-respostas.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
export const toolRoot = path.resolve(here, "..");
export const repoRoot = path.resolve(toolRoot, "../..");
const defaultJsonPath = path.join(toolRoot, "data", "automations.json");

export function sqlString(value) {
  if (value == null) return "NULL";
  return `'${String(value).replaceAll("'", "''")}'`;
}

export function buildSyncSql(drafts, now = new Date().toISOString()) {
  const statements = ["BEGIN;"];
  for (const draft of drafts) {
    statements.push(`INSERT INTO rules (
  label, channels, keywords, reply_text, public_reply_text, link_url, link_button_label,
  active, created_at, updated_at, media_id, shortcode, source_key, followers_only, follow_prompt_text, match_mode
) VALUES (
  ${sqlString(draft.label)},
  '["comments"]',
  ${sqlString(JSON.stringify([draft.keyword]))},
  ${sqlString(draft.replyText)},
  ${sqlString(draft.publicReplyText)},
  NULL,
  NULL,
  1,
  ${sqlString(now)},
  ${sqlString(now)},
  ${sqlString(draft.mediaId)},
  ${sqlString(draft.shortcode)},
  ${sqlString(draft.sourceKey)},
  ${draft.followersOnly ? 1 : 0},
  ${sqlString(draft.followPromptText)},
  'strict'
)
ON CONFLICT(source_key) DO UPDATE SET
  label = excluded.label,
  channels = excluded.channels,
  keywords = excluded.keywords,
  reply_text = excluded.reply_text,
  public_reply_text = excluded.public_reply_text,
  active = 1,
  updated_at = excluded.updated_at,
  media_id = COALESCE(excluded.media_id, rules.media_id),
  shortcode = excluded.shortcode,
  followers_only = excluded.followers_only,
  follow_prompt_text = excluded.follow_prompt_text,
  match_mode = excluded.match_mode;`);
  }
  if (drafts.length) {
    const keys = drafts.map((draft) => sqlString(draft.sourceKey)).join(", ");
    statements.push(`UPDATE rules SET active = 0, updated_at = ${sqlString(now)}
WHERE source_key IS NOT NULL AND source_key NOT IN (${keys}) AND active = 1;`);
  } else {
    statements.push(`UPDATE rules SET active = 0, updated_at = ${sqlString(now)}
WHERE source_key IS NOT NULL AND active = 1;`);
  }
  statements.push("COMMIT;");
  return `${statements.join("\n")}\n`;
}

export function diffRules(current, drafts) {
  const wanted = new Map(drafts.map((draft) => [draft.sourceKey, draft]));
  const lines = [];
  const seen = new Set();
  for (const draft of drafts) {
    const row = current.find((item) => item.source_key === draft.sourceKey);
    if (!row) {
      lines.push(`criar ${draft.sourceKey} (${draft.file})`);
      continue;
    }
    seen.add(draft.sourceKey);
    if (rowChanged(row, draft)) lines.push(`atualizar ${draft.sourceKey} (${draft.file})`);
    else lines.push(`igual ${draft.sourceKey}`);
  }
  for (const row of current) {
    if (!row.source_key || wanted.has(row.source_key) || seen.has(row.source_key)) continue;
    if (Number(row.active) === 1) lines.push(`pausar ${row.source_key}`);
  }
  return lines;
}

function rowChanged(row, draft) {
  const keywords = JSON.stringify([draft.keyword]);
  return Number(row.active) !== 1
    || row.reply_text !== draft.replyText
    || row.public_reply_text !== draft.publicReplyText
    || (row.follow_prompt_text ?? null) !== (draft.followPromptText ?? null)
    || Number(row.followers_only) !== (draft.followersOnly ? 1 : 0)
    || row.keywords !== keywords
    || (row.shortcode ?? null) !== (draft.shortcode ?? null)
    || row.match_mode !== "strict"
    || (draft.mediaId != null && row.media_id !== draft.mediaId);
}

export async function readSqliteRules(dbPath) {
  const { DatabaseSync } = await import("node:sqlite");
  const db = new DatabaseSync(dbPath);
  try {
    return db.prepare(
      `SELECT source_key, keywords, reply_text, public_reply_text, follow_prompt_text,
              followers_only, shortcode, media_id, active, match_mode
       FROM rules WHERE source_key IS NOT NULL`
    ).all();
  } finally {
    db.close();
  }
}

export async function applySqlite(dbPath, sql) {
  const { DatabaseSync } = await import("node:sqlite");
  const db = new DatabaseSync(dbPath);
  try {
    db.exec(sql);
  } finally {
    db.close();
  }
}

export async function runBuild(options = {}) {
  const root = options.root ?? repoRoot;
  const loaded = await loadRespostas(root);
  if (loaded.errors.length) return { ok: false, errors: loaded.errors, report: loaded.errors.join("\n") };

  const jsonPath = options.jsonPath === undefined ? defaultJsonPath : options.jsonPath;
  if (jsonPath) {
    await mkdir(path.dirname(jsonPath), { recursive: true });
    await writeFile(jsonPath, `${JSON.stringify({ generatedAt: new Date().toISOString(), rules: loaded.drafts }, null, 2)}\n`);
  }

  const lines = loaded.drafts.length
    ? loaded.drafts.map((draft) => `${draft.sourceKey}  ${draft.followersOnly ? "seguidores" : "todos"}  ${byteCount(draft.replyText)} bytes  ${draft.file}`)
    : ["Nenhum respostas-comentarios.md. As regras sincronizadas seriam pausadas."];
  const dryRun = Boolean(options.dryRun);
  const target = options.dbPath ? "db" : options.remote ? "remote" : null;
  if (!target) {
    return {
      ok: true,
      errors: [],
      applied: false,
      report: `${lines.join("\n")}\nNada foi gravado no D1. Use --dry-run --remote para ver o diff, ou --remote para sincronizar.`
    };
  }

  let current;
  try {
    current = target === "db" ? await readSqliteRules(options.dbPath) : await readRemoteRules();
  } catch (error) {
    return { ok: false, errors: [error.message], report: error.message };
  }
  const diff = diffRules(current, loaded.drafts);
  if (dryRun) {
    return { ok: true, errors: [], applied: false, report: `${lines.join("\n")}\n${diff.join("\n") || "Nada a mudar."}` };
  }
  const sql = buildSyncSql(loaded.drafts);
  try {
    if (target === "db") await applySqlite(options.dbPath, sql);
    else await applyRemote(sql);
  } catch (error) {
    return { ok: false, errors: [error.message], report: error.message };
  }
  return { ok: true, errors: [], applied: true, report: `${lines.join("\n")}\n${diff.join("\n")}\nSincronizado.` };
}

function byteCount(text) {
  return new TextEncoder().encode(text).length;
}

async function databaseName() {
  const source = await readFile(path.join(toolRoot, "wrangler.jsonc"), "utf8");
  const match = /"database_name"\s*:\s*"([^"]+)"/.exec(source);
  if (!match) throw new Error("Não encontrei database_name em wrangler.jsonc.");
  return match[1];
}

async function readRemoteRules() {
  const name = await databaseName();
  const result = wrangler([
    "d1", "execute", name, "--remote", "--json", "--command",
    "SELECT source_key, keywords, reply_text, public_reply_text, follow_prompt_text, followers_only, shortcode, media_id, active, match_mode FROM rules WHERE source_key IS NOT NULL"
  ]);
  const parsed = JSON.parse(result);
  const results = Array.isArray(parsed) ? parsed.flatMap((item) => item.results ?? []) : parsed.results ?? [];
  return results;
}

function remoteStatements(sql) {
  const statements = [];
  let current = "";
  let quoted = false;
  for (let i = 0; i < sql.length; i++) {
    const char = sql[i];
    if (char === "'") {
      if (quoted && sql[i + 1] === "'") {
        current += "''";
        i++;
        continue;
      }
      quoted = !quoted;
    }
    if (char === ";" && !quoted) {
      const statement = current.trim();
      if (statement && !/^(BEGIN|COMMIT)$/i.test(statement)) statements.push(statement);
      current = "";
      continue;
    }
    current += char;
  }
  const tail = current.trim();
  if (tail && !/^(BEGIN|COMMIT)$/i.test(tail)) statements.push(tail);
  return statements;
}

async function applyRemote(sql) {
  const name = await databaseName();
  // D1 rejects explicit BEGIN/COMMIT. Each statement is its own remote call.
  for (const statement of remoteStatements(sql)) {
    wrangler(["d1", "execute", name, "--remote", "--command", statement]);
  }
}

function wrangler(args) {
  const bin = path.join(toolRoot, "node_modules", "wrangler", "bin", "wrangler.js");
  const result = spawnSync(process.execPath, [bin, ...args], { cwd: toolRoot, encoding: "utf8" });
  if (result.error) throw new Error(`Não consegui rodar o wrangler: ${result.error.message}`);
  if (result.status !== 0) {
    throw new Error((result.stderr || result.stdout || "wrangler falhou").trim());
  }
  return result.stdout;
}

function printHelp() {
  console.log(`Uso: node scripts/build-respostas.mjs [--root pasta] [--dry-run] [--remote | --db arquivo.sqlite]

Lê posts/**/respostas-comentarios.md, valida e grava data/automations.json.
Sem --remote e sem --db, não escreve no D1.
--dry-run com --remote ou --db mostra o diff e não grava.`);
}

async function main() {
  const args = process.argv.slice(2);
  if (args.includes("--help") || args.includes("-h")) {
    printHelp();
    return;
  }
  const options = { dryRun: args.includes("--dry-run"), remote: args.includes("--remote") };
  const rootIndex = args.indexOf("--root");
  if (rootIndex !== -1) options.root = path.resolve(args[rootIndex + 1] ?? "");
  const dbIndex = args.indexOf("--db");
  if (dbIndex !== -1) options.dbPath = path.resolve(args[dbIndex + 1] ?? "");
  if (options.remote && options.dbPath) {
    console.error("Use só um destino: --remote ou --db.");
    process.exitCode = 1;
    return;
  }
  const result = await runBuild(options);
  if (result.report) console.log(result.report);
  if (!result.ok) process.exitCode = 1;
}

const invoked = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invoked) main();
