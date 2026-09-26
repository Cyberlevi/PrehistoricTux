#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="${SUPERTUX_BIN:-supertux2}"
ADDON_ID="cyberlevi-prehistorictux"
DIAG_USERDIR="$ROOT/.diag-userdir"
DEST="$DIAG_USERDIR/addons/$ADDON_ID"
WORLDMAP="$DEST/levels/prehistoric_tux/worldmap.stwm"
OUTDIR="$ROOT/diagnostics"
LOG="$OUTDIR/supertux-debug.log"
CORE="$OUTDIR/coredump.txt"

mkdir -p "$OUTDIR"
rm -rf "$DIAG_USERDIR"
mkdir -p "$DIAG_USERDIR"

cat > "$DIAG_USERDIR/config" <<EOF
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

{
  echo "=== PrehistoricTux crash diagnostic ==="
  date
  echo
  echo "=== SuperTux ==="
  "$BIN" --version || true
  echo
  echo "=== Session ==="
  echo "XDG_SESSION_TYPE=${XDG_SESSION_TYPE:-unknown}"
  echo "WAYLAND_DISPLAY=${WAYLAND_DISPLAY:-unset}"
  echo "DISPLAY=${DISPLAY:-unset}"
  echo
  echo "=== Kernel ==="
  uname -a
  echo
  echo "=== GPU ==="
  if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi --query-gpu=name,driver_version --format=csv,noheader || true
  fi
  echo
  echo "=== Install + static validation ==="
} | tee "$LOG"

SUPERTUX2_USER_DIR="$DIAG_USERDIR" bash "$ROOT/scripts/install-dev-addon.sh" 2>&1 | tee -a "$LOG"
python "$ROOT/scripts/validate_levels.py" 2>&1 | tee -a "$LOG"

echo | tee -a "$LOG"
echo "=== Launch: 1280x720 window, renderer auto, debug logging ===" | tee -a "$LOG"

set +e
"$BIN" \
  --userdir "$DIAG_USERDIR" \
  --debug \
  --developer \
  --show-fps \
  --renderer auto \
  --window \
  --geometry 1280x720 \
  "$WORLDMAP" 2>&1 | tee -a "$LOG"
STATUS=${PIPESTATUS[0]}
set -e

echo | tee -a "$LOG"
echo "SuperTux exit code: $STATUS" | tee -a "$LOG"

if [[ "$STATUS" -ne 0 ]] && command -v coredumpctl >/dev/null 2>&1; then
  {
    echo "=== Latest coredump info ==="
    coredumpctl --no-pager info supertux2 2>&1 | tail -n 220
  } | tee "$CORE" | tee -a "$LOG"
fi

echo
echo "Diagnostic log: $LOG"
if [[ -f "$CORE" ]]; then
  echo "Coredump info:  $CORE"
fi

exit "$STATUS"
