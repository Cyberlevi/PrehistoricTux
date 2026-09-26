#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="${SUPERTUX_BIN:-supertux2}"
ADDON_ID="cyberlevi-prehistorictux"
DEV_USERDIR="$ROOT/.dev-userdir"
DEST="$DEV_USERDIR/addons/$ADDON_ID"
WORLDMAP="$DEST/levels/prehistoric_tux/worldmap.stwm"

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

echo "Launching PrehistoricTux in UHD developer mode..."
exec "$BIN" \
  --userdir "$DEV_USERDIR" \
  --developer \
  --show-fps \
  --renderer opengl \
  --fullscreen \
  --geometry 3840x2160 \
  "$WORLDMAP"
