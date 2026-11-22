import { readFile, readdir } from "node:fs/promises";
import path from "node:path";

const DM_BYTES = 1000;
const BUTTON_TEXT_CHARS = 640;
const PUBLIC_REPLY_CHARS = 2200;
const URL_PATTERN = /https?:\/\/(?:www\.)?instagram\.com\/(?:p|reel|tv)\/([A-Za-z0-9_-]+)/i;
const KEYWORD_LINE = /^[-*]?\s*palavra-chave\s*:\s*(.+?)\s*$/i;
const CODE_LINE = /^[-*]?\s*c[oó]digo do post\s*:\s*(\S+)\s*$/i;
const MEDIA_LINE = /^[-*]?\s*(?:id da m[ií]dia|media id)\s*:\s*(\d+)\s*$/i;
const FOLLOWERS_LINE = /^[-*]?\s*somente seguidores\s*:\s*(sim|n[aã]o|yes|no)\s*$/i;

export function parseRespostasMarkdown(markdown, filePath = "respostas-comentarios.md") {
  const errors = [];
  const lines = String(markdown).replace(/^\uFEFF/, "").split(/\r?\n/);
  let section = "meta";
  const seen = { dm: false, publicReply: false, follow: false };
  const bodies = { dm: [], publicReply: [], follow: [] };
  const meta = [];

  for (const line of lines) {
    const heading = /^##\s+(.+?)\s*$/.exec(line);
    if (heading) {
      const name = heading[1].normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();
      if (name.includes("mensagem no direct")) {
        section = "dm";
        seen.dm = true;
      } else if (name.includes("resposta no comentario")) {
        section = "publicReply";
        seen.publicReply = true;
      } else if (name.includes("pedido para seguir")) {
        section = "follow";
        seen.follow = true;
      } else {
        section = "meta";
      }
      continue;
    }
    if (section === "dm" || section === "publicReply" || section === "follow") bodies[section].push(line);
    else meta.push(line);
  }

  const keywords = [];
  let code = null;
  let mediaId = null;
  let followers = null;
  let url = null;
  let urlCode = null;
  for (const line of meta) {
    const keyword = KEYWORD_LINE.exec(line);
    if (keyword) {
      keywords.push(keyword[1].trim());
      continue;
    }
    const postCode = CODE_LINE.exec(line);
    if (postCode) {
      code = postCode[1];
      continue;
    }
    const media = MEDIA_LINE.exec(line);
    if (media) {
      mediaId = media[1];
      continue;
    }
    const follower = FOLLOWERS_LINE.exec(line);
    if (follower) {
      followers = /^sim$|^yes$/i.test(follower[1]);
      continue;
    }
    const found = URL_PATTERN.exec(line);
    if (found && !url) {
      url = found[0];
      urlCode = found[1];
    }
  }

  if (!code && urlCode) code = urlCode;
  if (code && urlCode && code !== urlCode) {
    errors.push(`${filePath}: o código do post (${code}) não é o da URL (${urlCode}).`);
  }
  if (!code && !mediaId) errors.push(`${filePath}: falta o código do post ou a URL.`);
  if (!keywords.length) errors.push(`${filePath}: falta a palavra-chave.`);
  if (followers === null) errors.push(`${filePath}: falta "Somente seguidores".`);
  if (!seen.dm) errors.push(`${filePath}: falta a seção "Mensagem no direct".`);
  if (!seen.publicReply) errors.push(`${filePath}: falta a seção "Resposta no comentário".`);

  const replyText = bodies.dm.join("\n").trim();
  const publicReplyText = bodies.publicReply.join("\n").trim();
  const followPromptText = bodies.follow.join("\n").trim();
  if (seen.dm && !replyText) errors.push(`${filePath}: a mensagem no direct está vazia.`);
  if (seen.publicReply && !publicReplyText) errors.push(`${filePath}: a resposta no comentário está vazia.`);
  if (followers !== false && !seen.follow) errors.push(`${filePath}: falta a seção "Pedido para seguir".`);
  if (followers !== false && seen.follow && !followPromptText) errors.push(`${filePath}: o pedido para seguir está vazio.`);

  if (replyText && byteLength(replyText) > DM_BYTES) {
    errors.push(`${filePath}: a mensagem no direct tem ${byteLength(replyText)} bytes. O limite do Instagram é ${DM_BYTES}.`);
  }
  if (publicReplyText && publicReplyText.length > PUBLIC_REPLY_CHARS) {
    errors.push(`${filePath}: a resposta no comentário tem ${publicReplyText.length} caracteres. O limite é ${PUBLIC_REPLY_CHARS}.`);
  }
  if (followers !== false && followPromptText && followPromptText.length > BUTTON_TEXT_CHARS) {
    errors.push(`${filePath}: o pedido para seguir tem ${followPromptText.length} caracteres. O limite do botão é ${BUTTON_TEXT_CHARS}.`);
  }

  const drafts = [];
  const seenKeywords = new Set();
  for (const keyword of keywords) {
    if (!keyword || /[^\p{L}\p{N}_]/u.test(keyword.normalize("NFKC"))) {
      errors.push(`${filePath}: a palavra-chave "${keyword}" precisa ser uma única palavra.`);
      continue;
    }
    const normalized = foldKeyword(keyword);
    if (seenKeywords.has(normalized)) {
      errors.push(`${filePath}: a palavra-chave "${keyword}" está repetida.`);
      continue;
    }
    seenKeywords.add(normalized);
    const postKey = code || `media-${mediaId}`;
    drafts.push({
      sourceKey: `${postKey}:${normalized}`,
      label: `${postKey} ${keyword}`,
      shortcode: code,
      mediaId,
      url,
      keyword,
      replyText,
      publicReplyText,
      followPromptText: followers === false ? null : followPromptText,
      followersOnly: followers !== false,
      link: firstHttpsUrl(replyText),
      file: filePath
    });
  }

  if (errors.length) return { drafts: [], errors };
  return { drafts, errors };
}

export async function loadRespostas(root) {
  const postsDir = path.join(root, "posts");
  let files;
  try {
    files = await findMarkdowns(postsDir);
  } catch (error) {
    return { drafts: [], errors: [`Não consegui ler ${postsDir}: ${error.message}`] };
  }
  files.sort();
  const drafts = [];
  const errors = [];
  for (const file of files) {
    const markdown = await readFile(file, "utf8");
    const relative = path.relative(root, file).split(path.sep).join("/");
    const parsed = parseRespostasMarkdown(markdown, relative);
    errors.push(...parsed.errors);
    drafts.push(...parsed.drafts);
  }
  if (errors.length) return { drafts: [], errors };

  const byKeyword = new Map();
  for (const draft of drafts) {
    const key = foldKeyword(draft.keyword);
    const previous = byKeyword.get(key);
    if (previous) {
      errors.push(`A palavra-chave "${draft.keyword}" está em ${previous.file} e ${draft.file}. Cada palavra ativa precisa ser única.`);
    } else {
      byKeyword.set(key, draft);
    }
  }
  if (errors.length) return { drafts: [], errors };
  return { drafts, errors };
}

export function byteLength(text) {
  return new TextEncoder().encode(text).length;
}

export function foldKeyword(keyword) {
  return String(keyword).normalize("NFKC").normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();
}

function firstHttpsUrl(text) {
  const match = /https:\/\/[^\s<>]+/i.exec(text);
  return match ? match[0].replace(/[),.;]+$/, "") : null;
}

async function findMarkdowns(dir) {
  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch (error) {
    if (error.code === "ENOENT") return [];
    throw error;
  }
  const found = [];
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) found.push(...await findMarkdowns(full));
    else if (entry.isFile() && entry.name === "respostas-comentarios.md") found.push(full);
  }
  return found;
}
