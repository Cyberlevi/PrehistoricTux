#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="$ROOT/.engine/build-0.7.0-uhd/supertux2"
ADDON_ID="cyberlevi-prehistorictux"
USERDIR="$ROOT/.uhd-scale-test-userdir"
DEST="$USERDIR/addons/$ADDON_ID"
LEVEL="$DEST/levels/prehistoric_tux/dev/uhd_surface_scale_test.stl"

if [[ ! -x "$BIN" ]]; then
  echo "Patched UHD engine is not built yet." >&2
  echo "Run: bash scripts/setup-garuda-uhd-build.sh" >&2
  exit 1
fi

rm -rf "$USERDIR"
mkdir -p "$USERDIR"
cat > "$USERDIR/config" <<EOF
(supertux-config
  (developer #t)
  (addons
    (addon
      (id "$ADDON_ID")
      (enabled #t)
    )
  )
)
EOF

SUPERTUX2_USER_DIR="$USERDIR" bash "$ROOT/scripts/install-dev-addon.sh"
python "$ROOT/scripts/validate_levels.py"

exec "$BIN" \
  --userdir "$USERDIR" \
  --developer \
  --window \
  --geometry 1280x720 \
  "$LEVEL"
