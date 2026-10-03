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
echo "OK: $root/.claude/skills e $root/.cursor/skills -> .agents/skills"
