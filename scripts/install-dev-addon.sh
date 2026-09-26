#!/usr/bin/env bash
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/addon"
DEST="${XDG_DATA_HOME:-$HOME/.local/share}/supertux2/addons/prehistoric-tux"

mkdir -p "$DEST"
cp -a "$SRC"/. "$DEST"/
printf 'Installed PrehistoricTux development add-on to %s\n' "$DEST"
printf 'Open SuperTux and use the editor to smoke-test 01_lost_egg_valley.stl.\n'
