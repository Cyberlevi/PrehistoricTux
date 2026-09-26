#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="$ROOT/.engine/build-0.7.0-uhd/supertux2"

echo "PrehistoricTux UHD status"
echo "========================"
if [[ -x "$BIN" ]]; then
  echo "Engine: BUILT"
  "$BIN" --version 2>/dev/null | head -n 1 || true
else
  echo "Engine: NOT BUILT"
fi
echo

python "$ROOT/scripts/uhd-audit.py"
