#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="${SUPERTUX_BIN:-supertux2}"
ADDON_ID="cyberlevi-prehistorictux"
DEV_USERDIR="$ROOT/.dev-userdir"
DEST="$DEV_USERDIR/addons/$ADDON_ID"
WORLDMAP="$DEST/levels/prehistoric_tux/worldmap.stwm"

# Safe defaults for the current Garuda machine: all connected displays are 1920x1080.
# Keep UHD as an asset-production target; do not force a 3840x2160 fullscreen mode
# onto a 1080p monitor during runtime bring-up.
GEOMETRY="${PREHISTORICTUX_GEOMETRY:-1920x1080}"
VIDEO_MODE="${PREHISTORICTUX_VIDEO_MODE:-window}"
RENDERER="${PREHISTORICTUX_RENDERER:-auto}"

if ! command -v "$BIN" >/dev/null 2>&1; then
  echo "SuperTux executable not found: $BIN" >&2
  echo "Install SuperTux first or set SUPERTUX_BIN=/path/to/supertux2" >&2
  exit 1
fi

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
python "$ROOT/scripts/validate_levels.py"

VIDEO_ARG="--window"
if [[ "$VIDEO_MODE" == "fullscreen" ]]; then
  VIDEO_ARG="--fullscreen"
fi

echo "Launching PrehistoricTux in safe developer mode..."
echo "  geometry: $GEOMETRY"
echo "  video:    $VIDEO_MODE"
echo "  renderer: $RENDERER"

exec "$BIN" \
  --userdir "$DEV_USERDIR" \
  --developer \
  --show-fps \
  --renderer "$RENDERER" \
  "$VIDEO_ARG" \
  --geometry "$GEOMETRY" \
  "$WORLDMAP"
