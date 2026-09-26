#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/addon"
ADDON_ID="cyberlevi-prehistorictux"
USERDIR="${SUPERTUX2_USER_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/supertux2}"
DEST="$USERDIR/addons/$ADDON_ID"
rm -rf "$DEST"
mkdir -p "$DEST"
cp -a "$SRC"/. "$DEST"/
PYTHON_BIN="python3"
if ! "$PYTHON_BIN" -c 'import PIL' >/dev/null 2>&1; then
  VENV="$ROOT/.dino-venv"
  if [ ! -x "$VENV/bin/python" ]; then
    python3 -m venv "$VENV"
    "$VENV/bin/python" -m pip install -q -r "$ROOT/requirements-dev.txt"
  fi
  PYTHON_BIN="$VENV/bin/python"
fi
"$PYTHON_BIN" "$ROOT/scripts/generate-dino-assets.py" --output "$DEST/images/dino"
echo "Installed PrehistoricTux to $DEST"
echo "Worldmap: levels/prehistoric_tux/worldmap.stwm"
