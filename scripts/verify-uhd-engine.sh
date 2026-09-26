#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="$ROOT/.engine/build-0.7.0-uhd/supertux2"

if [[ ! -x "$BIN" ]]; then
  echo "Patched UHD engine is not built yet." >&2
  echo "Run: bash scripts/setup-garuda-uhd-build.sh" >&2
  exit 1
fi

echo "=== Patched engine ==="
"$BIN" --version || true
echo

echo "=== Static + parser smoke tests ==="
SUPERTUX_BIN="$BIN" bash "$ROOT/scripts/smoke-test-supertux.sh"
echo

echo "=== Active UHD bindings ==="
python "$ROOT/scripts/uhd-audit.py"
echo

echo "UHD engine verification passed."
echo "Visual logical-scale check:"
echo "  bash scripts/test-uhd-surface-scale.sh"
