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
printf 'Installed Stock Adventure add-on to %s\n' "$DEST"
