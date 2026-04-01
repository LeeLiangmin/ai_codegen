#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
bash "$HERE/sync-opencode-skills.sh"
bash "$HERE/sync-cursor-skills.sh"
echo "All IDE skill mirrors updated."
