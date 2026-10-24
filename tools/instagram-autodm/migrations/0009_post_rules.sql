-- Rules synced from posts/**/respostas-comentarios.md.
-- source_key is post + keyword. NULL source_key keeps dashboard-only rules.
-- match_mode strict: the comment is only the keyword. loose: the upstream matcher.
-- followers_only: private reply is a button, and the material waits for a follower check.

ALTER TABLE rules ADD COLUMN media_id TEXT;
ALTER TABLE rules ADD COLUMN shortcode TEXT;
ALTER TABLE rules ADD COLUMN source_key TEXT;
ALTER TABLE rules ADD COLUMN followers_only INTEGER NOT NULL DEFAULT 0;
ALTER TABLE rules ADD COLUMN follow_prompt_text TEXT;
ALTER TABLE rules ADD COLUMN match_mode TEXT NOT NULL DEFAULT 'loose';

CREATE UNIQUE INDEX IF NOT EXISTS idx_rules_source_key ON rules (source_key);

ALTER TABLE comment_events ADD COLUMN author_id TEXT;

CREATE TABLE IF NOT EXISTS material_deliveries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rule_id INTEGER NOT NULL,
  recipient_id TEXT NOT NULL,
  comment_id TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  material_sent_at TEXT,
  UNIQUE (rule_id, recipient_id)
);

CREATE INDEX IF NOT EXISTS idx_material_deliveries_comment
  ON material_deliveries (comment_id);
