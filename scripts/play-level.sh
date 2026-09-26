#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="${SUPERTUX_BIN:-supertux2}"
ADDON_ID="cyberlevi-prehistorictux"
DEV_USERDIR="$ROOT/.dev-userdir"
DEST="$DEV_USERDIR/addons/$ADDON_ID"
LEVEL_NO="${1:-1}"
case "$LEVEL_NO" in
  1) LEVEL_FILE="01_frostline_ascent.stl" ;;
  2) LEVEL_FILE="02_frozen_outpost.stl" ;;
  *) echo "Currently available: 1-2" >&2; exit 2 ;;
esac
GEOMETRY="${SUPERTUX_GEOMETRY:-1920x1080}"
mkdir -p "$DEV_USERDIR"
cat > "$DEV_USERDIR/config" <<EOF
(supertux-config
  (show_fps #t)
  (developer #t)
  (addons
    (addon
      (id "$ADDON_ID")
      (enabled #t)
    )
  )
)
EOF
SUPERTUX2_USER_DIR="$DEV_USERDIR" bash "$ROOT/scripts/install-dev-addon.sh"
LEVEL="$DEST/levels/prehistoric_tux/$LEVEL_FILE"
echo "Launching $LEVEL_FILE"
"$BIN" --userdir "$DEV_USERDIR" --developer --show-fps --window --geometry "$GEOMETRY" "$LEVEL"
