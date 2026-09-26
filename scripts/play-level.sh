#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="${SUPERTUX_BIN:-supertux2}"
DEV_USERDIR="$ROOT/.dev-userdir"
ADDON_ID="cyberlevi-prehistorictux"
DEST="$DEV_USERDIR/addons/$ADDON_ID"
N="${1:-1}"
case "$N" in
1) F="01_lost_egg_valley.stl";;
2) F="02_dinosaur_trail.stl";;
3) F="03_ancient_caves.stl";;
4) F="04_pterosaur_cliffs.stl";;
5) F="05_flooded_ruins.stl";;
6) F="06_bonefield.stl";;
7) F="07_nesting_grounds.stl";;
8) F="08_palaszarusz_crater.stl";;
*) echo "Usage: $0 [1-8]"; exit 2;;
esac
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
"$BIN" --userdir "$DEV_USERDIR" --developer --show-fps --window --geometry "${SUPERTUX_GEOMETRY:-1920x1080}" "$DEST/levels/prehistoric_tux/$F"
