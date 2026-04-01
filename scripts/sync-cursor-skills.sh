#!/usr/bin/env bash
# Sync canonical skill/* into .cursor/skills/* for Cursor project skills.
# Usage: bash scripts/sync-cursor-skills.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_ROOT="$ROOT/skill"
DEST_ROOT="$ROOT/.cursor/skills"

LEAF_SKILLS=(
  run-init
  design-intake
  design-normalize
  design-to-plan
  plan-to-slices
  slice-implement
  slice-verify
  integration-verify
  result-curate
  run-status
)

mkdir -p "$DEST_ROOT"
for name in "${LEAF_SKILLS[@]}"; do
  src="$SKILL_ROOT/$name/SKILL.md"
  if [[ ! -f "$src" ]]; then
    echo "Missing: $src" >&2
    exit 1
  fi
  mkdir -p "$DEST_ROOT/$name"
  cp -f "$src" "$DEST_ROOT/$name/SKILL.md"
  echo "Synced $name -> .cursor/skills/$name"
done
echo "Done. ${#LEAF_SKILLS[@]} Cursor project skills -> $DEST_ROOT"
