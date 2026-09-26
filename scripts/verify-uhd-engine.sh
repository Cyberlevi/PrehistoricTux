#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD="$ROOT/.engine/build-0.7.0-uhd"
BIN="$BUILD/supertux2"
PATCH="$ROOT/engine-patches/0001-uhd-logical-surface-scale.patch"
PATCH_MARKER="$BUILD/.prehistorictux-uhd-patch.sha256"

if [[ ! -x "$BIN" ]]; then
  echo "Patched UHD engine is not built yet." >&2
  echo "Run: bash scripts/setup-garuda-uhd-build.sh" >&2
  exit 1
fi

CURRENT_PATCH_SHA="$(sha256sum "$PATCH" | awk '{print $1}')"
BUILT_PATCH_SHA="$(cat "$PATCH_MARKER" 2>/dev/null || true)"
if [[ "$CURRENT_PATCH_SHA" != "$BUILT_PATCH_SHA" ]]; then
  echo "UHD engine patch fingerprint mismatch." >&2
  echo "Rebuild with: bash scripts/build-uhd-engine.sh" >&2
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
