import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { parseRespostasMarkdown, loadRespostas, byteLength } from "../scripts/parse-respostas.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

test("os dois formatos reais viram uma regra cada", async () => {
  const evals = parseRespostasMarkdown(await readFile(path.join(here, "fixtures/evals.md"), "utf8"), "fixtures/evals.md");
  const tier = parseRespostasMarkdown(await readFile(path.join(here, "fixtures/especialista.md"), "utf8"), "fixtures/especialista.md");
  assert.deepEqual(evals.errors, []);
  assert.deepEqual(tier.errors, []);
  assert.equal(evals.drafts[0].sourceKey, "DeU8X1fhF6a:evals");
  assert.equal(evals.drafts[0].followersOnly, true);
  assert.equal(evals.drafts[0].publicReplyText, "Enviei no direct.");
  assert.equal(evals.drafts[0].followPromptText, "Me segue por aqui para eu te enviar o material.");
  assert.equal(evals.drafts[0].replyText, [
    "Aqui está o artigo da Anthropic sobre evals para agentes de IA que comentei no vídeo:",
    "",
    "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents"
  ].join("\n"));
  assert.equal(evals.drafts[0].link, "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents");
  assert.equal(tier.drafts[0].sourceKey, "DehPW4yCR7W:especialista");
  assert.equal(tier.drafts[0].publicReplyText, "Enviei o artigo no direct.");
  assert.equal(tier.drafts[0].followPromptText, "Me segue por aqui para eu te enviar o artigo.");
  assert.match(tier.drafts[0].replyText, /^Segue o artigo sobre o copiloto de IA para especialistas:\n\nhttps:\/\/pedromiyasaki\.substack\.com\/p\/ia-no-trabalho-de-especialistas$/);
});

test("os markdowns do repositório continuam válidos", async (t) => {
  const root = path.resolve(here, "../../..");
  const marker = path.join(root, "posts/script/se-voce-desenvolve-qualquer-projeto-de-ia-precisa-de-evals/respostas-comentarios.md");
  try {
    await readFile(marker, "utf8");
  } catch {
    t.skip("a pasta posts/ não está nesta cópia");
    return;
  }
  const loaded = await loadRespostas(root);
  assert.deepEqual(loaded.errors, []);
  const keys = loaded.drafts.map((draft) => draft.sourceKey).sort();
  assert.ok(keys.includes("DeU8X1fhF6a:evals"));
  assert.ok(keys.includes("DehPW4yCR7W:especialista"));
});

test("rejeita palavra repetida, direct longo e campo faltando", () => {
  const base = `# Respostas

- Código do post: Abc123
- Palavra-chave: evals
- Somente seguidores: sim

## Mensagem no direct

Olá

https://example.com/a

## Resposta no comentário

Enviei no direct.

## Pedido para seguir

Me segue.
`;
  const missing = parseRespostasMarkdown(base.replace("- Palavra-chave: evals\n", ""), "faltando.md");
  assert.match(missing.errors.join("\n"), /falta a palavra-chave/);

  const duplicated = parseRespostasMarkdown(base.replace("- Palavra-chave: evals\n", "- Palavra-chave: evals\n- Palavra-chave: evals\n"), "repetida.md");
  assert.match(duplicated.errors.join("\n"), /repetida/);

  const phrase = parseRespostasMarkdown(base.replace("Palavra-chave: evals", "Palavra-chave: quero evals"), "frase.md");
  assert.match(phrase.errors.join("\n"), /única palavra/);

  const long = `á`.repeat(1000);
  assert.ok(byteLength(long) > 1000);
  const heavy = parseRespostasMarkdown(base.replace("Olá", long), "longa.md");
  assert.match(heavy.errors.join("\n"), /1000/);

  const accented = parseRespostasMarkdown(base.replace("Palavra-chave: evals", "Palavra-chave: Padrão"), "acento.md");
  assert.deepEqual(accented.errors, []);
  assert.equal(accented.drafts[0].keyword, "Padrão");
  assert.equal(accented.drafts[0].sourceKey, "Abc123:padrao");

  const sameSound = parseRespostasMarkdown(base.replace("- Palavra-chave: evals\n", "- Palavra-chave: padrao\n- Palavra-chave: Padrão\n"), "acento-repetido.md");
  assert.match(sameSound.errors.join("\n"), /repetida/);

  const open = parseRespostasMarkdown(base.replace("Somente seguidores: sim", "Somente seguidores: não").replace("## Pedido para seguir\n\nMe segue.\n", ""), "aberta.md");
  assert.deepEqual(open.errors, []);
  assert.equal(open.drafts[0].followersOnly, false);
  assert.equal(open.drafts[0].followPromptText, null);
});

test("palavras que só diferem por acento não coexistem em arquivos ativos", async () => {
  const root = await mkdtemp(path.join(tmpdir(), "respostas-"));
  const piece = (slug) => path.join(root, "posts", slug);
  await mkdir(piece("a"), { recursive: true });
  await mkdir(piece("b"), { recursive: true });
  const body = (word, code) => `# Respostas

- Código do post: ${code}
- Palavra-chave: ${word}
- Somente seguidores: sim

## Mensagem no direct

Oi

## Resposta no comentário

Enviei.

## Pedido para seguir

Segue.
`;
  await writeFile(path.join(piece("a"), "respostas-comentarios.md"), body("padrao", "Aaa111"));
  await writeFile(path.join(piece("b"), "respostas-comentarios.md"), body("Padrão", "Bbb222"));
  try {
    const loaded = await loadRespostas(root);
    assert.match(loaded.errors.join("\n"), /Padrão/);
    assert.equal(loaded.drafts.length, 0);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
