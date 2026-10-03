#!/usr/bin/env bash
# Aponta .claude/skills e .cursor/skills para .agents/skills (uma cópia no disco).
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
target="../.agents/skills"
for parent in .claude .cursor; do
  link="$parent/skills"
  rm -rf "$link"
  ln -s "$target" "$link"
done
rm -f CLAUDE.md
ln -sf AGENTS.md CLAUDE.md
echo "OK: .claude/skills e .cursor/skills -> .agents/skills; CLAUDE.md -> AGENTS.md"
