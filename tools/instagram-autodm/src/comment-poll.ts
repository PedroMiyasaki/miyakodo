import { getInstagramAccessToken } from "./instagram-token";

// Backup for comment webhooks. Off unless COMMENT_POLL_ENABLED=true.
// The read shape follows ig-autodm-worker: GET /{media-id}/comments, then the
// same comment pipeline and comment_id dedupe as a webhook delivery.
export type IncomingComment = {
  commentId: string;
  mediaId: string | null;
  authorId: string | null;
  username: string | null;
  text: string;
  timestamp?: string;
};

type GraphEnv = {
  DB: D1Database;
  INSTAGRAM_ACCESS_TOKEN: string;
  IG_USER_ID: string;
  GRAPH_API_BASE: string;
};

type MediaRow = { id: number; shortcode: string };
type MediaIdRow = { media_id: string };

const PRIVATE_REPLY_WINDOW_MS = 7 * 24 * 60 * 60 * 1000;
const MEDIA_PAGES = 5;
const COMMENT_PAGES = 3;
const COMMENT_LIMIT = 25;
const MEDIA_PER_RUN = 10;

export function commentPollEnabled(env: { COMMENT_POLL_ENABLED?: string }): boolean {
  return String(env.COMMENT_POLL_ENABLED ?? "false").toLowerCase() === "true";
}

export function shortcodeFromPermalink(permalink: string): string | null {
  const match = /instagram\.com\/(?:p|reel|tv)\/([A-Za-z0-9_-]+)/i.exec(permalink);
  return match?.[1] ?? null;
}

export function officialGraphBase(value: string): URL {
  const url = new URL(value);
  if (url.protocol !== "https:" || url.hostname !== "graph.instagram.com" || url.port ||
      url.username || url.password || url.search || url.hash || !/^\/v\d+\.\d+\/?$/.test(url.pathname)) {
    throw new Error("Comment polling requires the official Instagram Graph API address.");
  }
  return url;
}

/** Fills media_id for active markdown rules that only have a shortcode. Read-only. */
export async function refreshUnresolvedMediaIds(env: GraphEnv): Promise<void> {
  const pending = await env.DB.prepare(
    `SELECT id, shortcode FROM rules
     WHERE active = 1 AND shortcode IS NOT NULL AND shortcode != ''
       AND (media_id IS NULL OR media_id = '')`
  ).all<MediaRow>();
  if (!pending.results.length) return;
  if (!env.IG_USER_ID?.trim() || !env.INSTAGRAM_ACCESS_TOKEN?.trim()) return;

  const known = await listMediaShortcodes(env);
  const now = new Date().toISOString();
  for (const row of pending.results) {
    const mediaId = known.get(row.shortcode);
    if (!mediaId) continue;
    await env.DB.prepare(
      `UPDATE rules SET media_id = ?, updated_at = ? WHERE id = ? AND (media_id IS NULL OR media_id = '')`
    ).bind(mediaId, now, row.id).run();
  }
}

export async function pollActiveMediaComments(env: GraphEnv, now = Date.now()): Promise<IncomingComment[]> {
  const rows = await env.DB.prepare(
    `SELECT DISTINCT media_id AS media_id FROM rules
     WHERE active = 1 AND media_id IS NOT NULL AND media_id != ''
     ORDER BY media_id`
  ).all<MediaIdRow>();
  const mediaIds = rows.results.map((row) => row.media_id);
  if (!mediaIds.length) return [];

  const batches = Math.max(1, Math.ceil(mediaIds.length / MEDIA_PER_RUN));
  const batch = Math.floor(now / 60_000) % batches;
  const selected = mediaIds.slice(batch * MEDIA_PER_RUN, (batch + 1) * MEDIA_PER_RUN);
  const base = officialGraphBase(env.GRAPH_API_BASE);
  const comments: IncomingComment[] = [];
  for (const mediaId of selected) {
    try {
      comments.push(...await listMediaComments(env, base, mediaId, now));
    } catch (error) {
      console.warn(JSON.stringify({
        level: "warn",
        msg: "comment_poll_media_failed",
        mediaId,
        error: error instanceof Error ? error.message : String(error)
      }));
    }
  }
  return comments;
}

async function listMediaShortcodes(env: GraphEnv): Promise<Map<string, string>> {
  const found = new Map<string, string>();
  let next: URL | null = new URL(`${officialGraphBase(env.GRAPH_API_BASE).href.replace(/\/$/, "")}/${encodeURIComponent(env.IG_USER_ID)}/media`);
  next.searchParams.set("fields", "id,permalink");
  next.searchParams.set("limit", "50");
  for (let page = 0; page < MEDIA_PAGES && next; page += 1) {
    const data = await graphGet(env, next);
    const items = Array.isArray(data.data) ? data.data : [];
    for (const item of items) {
      if (!item || typeof item !== "object") continue;
      const row = item as Record<string, unknown>;
      const id = typeof row.id === "string" ? row.id : null;
      const permalink = typeof row.permalink === "string" ? row.permalink : null;
      const shortcode = permalink ? shortcodeFromPermalink(permalink) : null;
      if (id && shortcode) found.set(shortcode, id);
    }
    next = nextPage(data.paging);
  }
  return found;
}

async function listMediaComments(env: GraphEnv, base: URL, mediaId: string, now: number): Promise<IncomingComment[]> {
  const withAuthor = await fetchCommentPage(env, base, mediaId, "id,text,username,timestamp,from");
  const pages = withAuthor ?? await fetchCommentPage(env, base, mediaId, "id,text,username,timestamp");
  if (!pages) throw new Error("Instagram comments fetch failed");
  return pages.filter((comment) => insidePrivateReplyWindow(comment, now));
}

async function fetchCommentPage(env: GraphEnv, base: URL, mediaId: string, fields: string): Promise<IncomingComment[] | null> {
  let next: URL | null = new URL(`${base.href.replace(/\/$/, "")}/${encodeURIComponent(mediaId)}/comments`);
  next.searchParams.set("fields", fields);
  next.searchParams.set("limit", String(COMMENT_LIMIT));
  const comments: IncomingComment[] = [];
  for (let page = 0; page < COMMENT_PAGES && next; page += 1) {
    const response = await graphGetRaw(env, next);
    if (!response.ok || !Array.isArray(response.data.data)) return page === 0 ? null : comments;
    for (const item of response.data.data) {
      const comment = mapComment(item, mediaId);
      if (comment) comments.push(comment);
    }
    next = nextPage(response.data.paging);
  }
  return comments;
}

function mapComment(value: unknown, mediaId: string): IncomingComment | null {
  if (!value || typeof value !== "object") return null;
  const row = value as Record<string, unknown>;
  const commentId = typeof row.id === "string" || typeof row.id === "number" ? String(row.id) : null;
  const text = typeof row.text === "string" ? row.text : "";
  if (!commentId || !text) return null;
  const from = row.from && typeof row.from === "object" ? row.from as Record<string, unknown> : null;
  const username = typeof row.username === "string"
    ? row.username
    : typeof from?.username === "string" ? from.username : null;
  const authorId = typeof from?.id === "string" || typeof from?.id === "number" ? String(from.id) : null;
  const timestamp = typeof row.timestamp === "string" ? row.timestamp : undefined;
  return { commentId, mediaId, authorId, username, text, timestamp };
}

function insidePrivateReplyWindow(comment: IncomingComment, now: number): boolean {
  const timestamp = comment.timestamp;
  if (!timestamp) return true;
  const parsed = Date.parse(timestamp);
  if (!Number.isFinite(parsed)) return true;
  return now - parsed <= PRIVATE_REPLY_WINDOW_MS;
}

function nextPage(paging: unknown): URL | null {
  if (!paging || typeof paging !== "object") return null;
  const next = (paging as { next?: unknown }).next;
  if (typeof next !== "string" || !next.startsWith("https://graph.instagram.com/")) return null;
  return new URL(next);
}

async function graphGet(env: GraphEnv, url: URL): Promise<Record<string, unknown>> {
  const response = await graphGetRaw(env, url);
  if (!response.ok) {
    throw new Error(`Instagram media list failed (${response.status})`);
  }
  return response.data;
}

async function graphGetRaw(env: GraphEnv, url: URL): Promise<{ ok: boolean; status: number; data: Record<string, unknown> }> {
  const token = await getInstagramAccessToken(env);
  const response = await fetch(url, { headers: { authorization: `Bearer ${token}` } });
  const text = await response.text();
  let data: Record<string, unknown> = {};
  try {
    const parsed: unknown = JSON.parse(text);
    if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) data = parsed as Record<string, unknown>;
  } catch {
    data = {};
  }
  return { ok: response.ok, status: response.status, data };
}
