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

printf 'Installed PrehistoricTux development add-on to %s\n' "$DEST"
printf 'Worldmap: levels/prehistoric_tux/worldmap.stwm\n'
printf 'Level 01: levels/prehistoric_tux/01_lost_egg_valley.stl\n'
