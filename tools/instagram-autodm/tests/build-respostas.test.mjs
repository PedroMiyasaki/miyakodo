import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { DatabaseSync } from "node:sqlite";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { applySqlite, buildSyncSql, runBuild, toolRoot } from "../scripts/build-respostas.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

async function emptyRepo() {
  const root = await mkdtemp(path.join(tmpdir(), "respostas-"));
  await mkdir(path.join(root, "posts/script/evals"), { recursive: true });
  await mkdir(path.join(root, "posts/script/tier"), { recursive: true });
  await writeFile(path.join(root, "posts/script/evals/respostas-comentarios.md"), await readFile(path.join(here, "fixtures/evals.md")));
  await writeFile(path.join(root, "posts/script/tier/respostas-comentarios.md"), await readFile(path.join(here, "fixtures/especialista.md")));
  return root;
}

async function migratedDb() {
  const dir = await mkdtemp(path.join(tmpdir(), "autodm-db-"));
  const dbPath = path.join(dir, "local.sqlite");
  const db = new DatabaseSync(dbPath);
  const names = (await readdir(path.join(toolRoot, "migrations"))).filter((name) => name.endsWith(".sql")).sort();
  for (const name of names) db.exec(await readFile(path.join(toolRoot, "migrations", name), "utf8"));
  db.close();
  return dbPath;
}

test("sincroniza, atualiza e pausa pelo source key", async () => {
  const root = await emptyRepo();
  const dbPath = await migratedDb();
  const jsonPath = path.join(root, "automations.json");
  const first = await runBuild({ root, dbPath, jsonPath, dryRun: true });
  assert.equal(first.ok, true);
  assert.match(first.report, /criar DeU8X1fhF6a:evals/);
  assert.match(first.report, /criar DehPW4yCR7W:especialista/);
  assert.equal(first.applied, false);

  const applied = await runBuild({ root, dbPath, jsonPath });
  assert.equal(applied.applied, true);
  const db = new DatabaseSync(dbPath);
  const rows = db.prepare("SELECT source_key, active, match_mode, followers_only, reply_text FROM rules WHERE source_key IS NOT NULL ORDER BY source_key").all();
  assert.equal(rows.length, 2);
  assert.equal(rows[0].match_mode, "strict");
  assert.equal(rows[0].followers_only, 1);
  assert.match(rows[0].reply_text, /evals para agentes/);
  db.close();

  await rm(path.join(root, "posts/script/tier/respostas-comentarios.md"));
  const evalsPath = path.join(root, "posts/script/evals/respostas-comentarios.md");
  const evals = await readFile(evalsPath, "utf8");
  await writeFile(evalsPath, evals.replace("Enviei no direct.", "Mandei no direct."));
  const second = await runBuild({ root, dbPath, jsonPath: null });
  assert.equal(second.ok, true);
  const after = new DatabaseSync(dbPath);
  const left = after.prepare("SELECT source_key, active, public_reply_text, media_id FROM rules WHERE source_key IS NOT NULL ORDER BY source_key").all();
  assert.deepEqual(left.map((row) => [row.source_key, row.active, row.public_reply_text]), [
    ["DeU8X1fhF6a:evals", 1, "Mandei no direct."],
    ["DehPW4yCR7W:especialista", 0, "Enviei o artigo no direct."]
  ]);
  after.prepare("UPDATE rules SET media_id = '179' WHERE source_key = 'DeU8X1fhF6a:evals'").run();
  after.close();
  await applySqlite(dbPath, buildSyncSql([{
    sourceKey: "DeU8X1fhF6a:evals",
    label: "DeU8X1fhF6a evals",
    keyword: "evals",
    replyText: "texto",
    publicReplyText: "ok",
    followPromptText: "segue",
    followersOnly: true,
    shortcode: "DeU8X1fhF6a",
    mediaId: null
  }]));
  const kept = new DatabaseSync(dbPath);
  assert.equal(kept.prepare("SELECT media_id FROM rules WHERE source_key = 'DeU8X1fhF6a:evals'").get().media_id, "179");
  kept.close();
  await rm(root, { recursive: true, force: true });
  await rm(path.dirname(dbPath), { recursive: true, force: true });
});

test("não grava quando a validação falha", async () => {
  const root = await mkdtemp(path.join(tmpdir(), "respostas-ruins-"));
  await mkdir(path.join(root, "posts/a"), { recursive: true });
  await mkdir(path.join(root, "posts/b"), { recursive: true });
  const body = await readFile(path.join(here, "fixtures/evals.md"), "utf8");
  await writeFile(path.join(root, "posts/a/respostas-comentarios.md"), body);
  await writeFile(path.join(root, "posts/b/respostas-comentarios.md"), body.replaceAll("DeU8X1fhF6a", "OutroPost9"));
  const dbPath = await migratedDb();
  const result = await runBuild({ root, dbPath, jsonPath: null });
  assert.equal(result.ok, false);
  assert.match(result.report, /única/);
  const db = new DatabaseSync(dbPath);
  assert.equal(db.prepare("SELECT COUNT(*) AS n FROM rules WHERE source_key IS NOT NULL").get().n, 0);
  db.close();
  await rm(root, { recursive: true, force: true });
  await rm(path.dirname(dbPath), { recursive: true, force: true });
});
