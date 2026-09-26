#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="${SUPERTUX_BIN:-supertux2}"
ADDON_ID="cyberlevi-prehistorictux"
DEST="${XDG_DATA_HOME:-$HOME/.local/share}/supertux2/addons/$ADDON_ID"

if ! command -v "$BIN" >/dev/null 2>&1; then
  echo "SuperTux executable not found: $BIN" >&2
  exit 1
fi

bash "$ROOT/scripts/install-dev-addon.sh"
python "$ROOT/scripts/validate_levels.py"

mapfile -t FILES < <(find "$DEST/levels/prehistoric_tux" -maxdepth 1 \
  \( -name '*.stl' -o -name '*.stwm' \) -type f | sort)

for file in "${FILES[@]}"; do
  echo "SuperTux parser smoke test: ${file##*/}"
  "$BIN" --resave "$file"
done

echo "Static and SuperTux parser smoke tests completed for ${#FILES[@]} files."
