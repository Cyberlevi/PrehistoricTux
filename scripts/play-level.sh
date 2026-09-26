#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="${SUPERTUX_BIN:-supertux2}"
ADDON_ID="cyberlevi-prehistorictux"
DEV_USERDIR="$ROOT/.dev-userdir"
DEST="$DEV_USERDIR/addons/$ADDON_ID"

LEVEL_NO="${1:-1}"
case "$LEVEL_NO" in
  1) LEVEL_FILE="01_lost_egg_valley.stl" ;;
  2) LEVEL_FILE="02_fernwood_canopy.stl" ;;
  3) LEVEL_FILE="03_serpent_caves.stl" ;;
  4) LEVEL_FILE="04_pterosaur_cliffs.stl" ;;
  5) LEVEL_FILE="05_obsidian_river.stl" ;;
  6) LEVEL_FILE="06_bonefield_at_dusk.stl" ;;
  7) LEVEL_FILE="07_nesting_grounds.stl" ;;
  8) LEVEL_FILE="08_palaszarusz_crater.stl" ;;
  *)
    echo "Usage: bash scripts/play-level.sh [1-8]" >&2
    exit 2
    ;;
esac

GEOMETRY="${PREHISTORICTUX_GEOMETRY:-1920x1080}"
VIDEO_MODE="${PREHISTORICTUX_VIDEO_MODE:-window}"
RENDERER="${PREHISTORICTUX_RENDERER:-auto}"

if ! command -v "$BIN" >/dev/null 2>&1; then
  echo "SuperTux executable not found: $BIN" >&2
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

LEVEL="$DEST/levels/prehistoric_tux/$LEVEL_FILE"
LOGDIR="$ROOT/diagnostics"
mkdir -p "$LOGDIR"
LOG="$LOGDIR/level-${LEVEL_NO}.log"

echo "Launching PrehistoricTux Level $LEVEL_NO: $LEVEL_FILE"
echo "Runtime log: $LOG"

set +e
"$BIN" \
  --userdir "$DEV_USERDIR" \
  --developer \
  --show-fps \
  --renderer "$RENDERER" \
  "$VIDEO_ARG" \
  --geometry "$GEOMETRY" \
  "$LEVEL" 2>&1 | tee "$LOG"
STATUS=${PIPESTATUS[0]}
set -e
exit "$STATUS"
