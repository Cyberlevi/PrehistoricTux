#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="${SUPERTUX_BIN:-supertux2}"
ADDON_ID="cyberlevi-prehistorictux"
DEST="${XDG_DATA_HOME:-$HOME/.local/share}/supertux2/addons/$ADDON_ID"
LEVEL="$DEST/levels/prehistoric_tux/01_lost_egg_valley.stl"

if ! command -v "$BIN" >/dev/null 2>&1; then
  echo "SuperTux executable not found: $BIN" >&2
  exit 1
fi

"$ROOT/scripts/install-dev-addon.sh"
python "$ROOT/scripts/validate_levels.py"

exec "$BIN" --developer --edit-level "$LEVEL"
