#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/addon"
ADDON_ID="cyberlevi-prehistorictux"
DEST="${XDG_DATA_HOME:-$HOME/.local/share}/supertux2/addons/$ADDON_ID"

rm -rf "$DEST"
mkdir -p "$DEST"
cp -a "$SRC"/. "$DEST"/

printf 'Installed PrehistoricTux development add-on to %s\n' "$DEST"
printf 'Worldmap: levels/prehistoric_tux/worldmap.stwm\n'
printf 'Level 01: levels/prehistoric_tux/01_lost_egg_valley.stl\n'
