#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD="$ROOT/.engine/build-0.7.0-uhd"
BIN="$BUILD/supertux2"
PATCHER="$ROOT/scripts/apply-uhd-engine-patch.py"
PATCH_MARKER="$BUILD/.prehistorictux-uhd-patch.sha256"
LEVEL_NO="${1:-1}"

if [[ ! -x "$BIN" ]]; then
  echo "Patched UHD engine is not built yet." >&2
  echo "Run: bash scripts/setup-garuda-uhd-build.sh" >&2
  exit 1
fi

CURRENT_PATCH_SHA="$(sha256sum "$PATCHER" | awk '{print $1}')"
BUILT_PATCH_SHA="$(cat "$PATCH_MARKER" 2>/dev/null || true)"
if [[ "$CURRENT_PATCH_SHA" != "$BUILT_PATCH_SHA" ]]; then
  echo "The UHD engine binary is stale relative to the current patcher." >&2
  echo "Rebuild with: bash scripts/build-uhd-engine.sh" >&2
  exit 1
fi

export SUPERTUX_BIN="$BIN"
export PREHISTORICTUX_RENDERER="${PREHISTORICTUX_RENDERER:-opengl}"

exec bash "$ROOT/scripts/play-level.sh" "$LEVEL_NO"
