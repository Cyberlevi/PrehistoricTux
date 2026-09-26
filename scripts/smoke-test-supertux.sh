#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="${SUPERTUX_BIN:-supertux2}"
ADDON_ID="cyberlevi-prehistorictux"
TEST_USERDIR="$ROOT/.smoke-userdir"
DEST="$TEST_USERDIR/addons/$ADDON_ID"

if ! command -v "$BIN" >/dev/null 2>&1; then
  echo "SuperTux executable not found: $BIN" >&2
  exit 1
fi

rm -rf "$TEST_USERDIR"
mkdir -p "$TEST_USERDIR"

cat > "$TEST_USERDIR/config" <<EOF
(supertux-config
  (addons
    (addon
      (id "$ADDON_ID")
      (enabled #t)
    )
  )
)
EOF

SUPERTUX2_USER_DIR="$TEST_USERDIR" bash "$ROOT/scripts/install-dev-addon.sh"
python "$ROOT/scripts/validate_levels.py"

mapfile -t FILES < <(find "$DEST/levels/prehistoric_tux" \
  \( -name '*.stl' -o -name '*.stwm' \) -type f | sort)

for file in "${FILES[@]}"; do
  echo "SuperTux parser smoke test: ${file##*/}"
  "$BIN" --userdir "$TEST_USERDIR" --resave "$file"
done

echo "Static and SuperTux parser smoke tests completed for ${#FILES[@]} files."
