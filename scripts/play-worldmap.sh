#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="${SUPERTUX_BIN:-supertux2}"
DEV_USERDIR="$ROOT/.dev-userdir"
ADDON_ID="cyberlevi-prehistorictux"
DEST="$DEV_USERDIR/addons/$ADDON_ID"
mkdir -p "$DEV_USERDIR"
SUPERTUX2_USER_DIR="$DEV_USERDIR" bash "$ROOT/scripts/install-dev-addon.sh"
"$BIN" --userdir "$DEV_USERDIR" --developer --show-fps --window --geometry "${SUPERTUX_GEOMETRY:-1920x1080}" "$DEST/levels/prehistoric_tux/worldmap.stwm"
