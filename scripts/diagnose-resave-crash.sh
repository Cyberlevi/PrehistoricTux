#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PATCHED="$ROOT/.engine/build-0.7.0-uhd/supertux2"
STOCK="${SUPERTUX_STOCK_BIN:-$(command -v supertux2 || true)}"
ADDON_ID="cyberlevi-prehistorictux"
OUT="$ROOT/diagnostics/resave-compare"
PATCHED_USERDIR="$ROOT/.diag-resave-patched"
STOCK_USERDIR="$ROOT/.diag-resave-stock"

if [[ ! -x "$PATCHED" ]]; then
  echo "Patched UHD engine is not built: $PATCHED" >&2
  exit 1
fi

if [[ -z "$STOCK" || ! -x "$STOCK" ]]; then
  echo "System SuperTux binary not found; patched-engine diagnostics will still run." >&2
  STOCK=""
fi

rm -rf "$OUT" "$PATCHED_USERDIR" "$STOCK_USERDIR"
mkdir -p "$OUT" "$PATCHED_USERDIR" "$STOCK_USERDIR"

write_config() {
  local dir="$1"
  cat > "$dir/config" <<EOF
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
}

write_config "$PATCHED_USERDIR"
write_config "$STOCK_USERDIR"

SUPERTUX2_USER_DIR="$PATCHED_USERDIR" bash "$ROOT/scripts/install-dev-addon.sh" >/dev/null
SUPERTUX2_USER_DIR="$STOCK_USERDIR" bash "$ROOT/scripts/install-dev-addon.sh" >/dev/null
python "$ROOT/scripts/validate_levels.py" >"$OUT/static-validator.log"

PATCHED_LEVEL="$PATCHED_USERDIR/addons/$ADDON_ID/levels/prehistoric_tux/01_lost_egg_valley.stl"
STOCK_LEVEL="$STOCK_USERDIR/addons/$ADDON_ID/levels/prehistoric_tux/01_lost_egg_valley.stl"

run_case() {
  local label="$1"
  local bin="$2"
  local userdir="$3"
  local level="$4"
  local log="$OUT/$label.log"

  echo "=== $label ==="
  echo "binary: $bin"

  set +e
  "$bin" --userdir "$userdir" --debug --resave "$level" >"$log" 2>&1
  local status=$?
  set -e

  echo "exit: $status"
  if [[ "$status" -ne 0 ]]; then
    tail -n 45 "$log" || true

    local offset
    offset="$(grep -oE 'supertux2\(\+0x[0-9a-fA-F]+\)' "$log" | head -n 1 | sed -E 's/.*\(\+?(0x[0-9a-fA-F]+)\).*/\1/' || true)"
    if [[ -n "$offset" ]] && command -v addr2line >/dev/null 2>&1; then
      echo
      echo "addr2line for first anonymous frame ($offset):"
      addr2line -Cfipe "$bin" "$offset" || true
    fi
  fi
  echo

  return 0
}

if [[ -n "$STOCK" ]]; then
  run_case "stock-level01-resave" "$STOCK" "$STOCK_USERDIR" "$STOCK_LEVEL"
fi
run_case "patched-level01-resave" "$PATCHED" "$PATCHED_USERDIR" "$PATCHED_LEVEL"

echo "=== Minimal UHD test level through patched --resave ==="
PATCHED_MIN="$PATCHED_USERDIR/addons/$ADDON_ID/levels/prehistoric_tux/dev/uhd_surface_scale_test.stl"
set +e
"$PATCHED" --userdir "$PATCHED_USERDIR" --debug --resave "$PATCHED_MIN" >"$OUT/patched-minimal-resave.log" 2>&1
MIN_STATUS=$?
set -e
echo "exit: $MIN_STATUS"
if [[ "$MIN_STATUS" -ne 0 ]]; then
  tail -n 45 "$OUT/patched-minimal-resave.log" || true
fi
echo

echo "Diagnostic logs: $OUT"
echo
echo "Interpretation:"
echo "  stock PASS + patched FAIL   -> patched-engine regression"
echo "  stock FAIL + patched PASS   -> upstream/system SuperTux resave bug fixed in our engine"
echo "  stock FAIL + patched FAIL   -> remaining shared resave/content issue"
echo "  minimal PASS + Level01 FAIL -> Level01-specific object/content interaction"
