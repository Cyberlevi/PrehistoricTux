#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD="$ROOT/.engine/build-0.7.0-uhd"
BIN="$BUILD/supertux2"
PATCHER="$ROOT/scripts/apply-uhd-engine-patch.py"
PATCH_MARKER="$BUILD/.prehistorictux-uhd-patch.sha256"

if [[ ! -x "$BIN" ]]; then
  echo "Patched UHD engine is not built yet." >&2
  echo "Run: bash scripts/setup-garuda-uhd-build.sh" >&2
  exit 1
fi

CURRENT_PATCH_SHA="$(sha256sum "$PATCHER" | awk '{print $1}')"
BUILT_PATCH_SHA="$(cat "$PATCH_MARKER" 2>/dev/null || true)"
if [[ "$CURRENT_PATCH_SHA" != "$BUILT_PATCH_SHA" ]]; then
  echo "The UHD engine binary was built with an older/missing patch revision." >&2
  echo "Rebuild it with: bash scripts/build-uhd-engine.sh" >&2
  exit 1
fi

export SUPERTUX_BIN="$BIN"
export PREHISTORICTUX_RENDERER="${PREHISTORICTUX_RENDERER:-opengl}"

# Keep current 1080p monitors safe by default. On a physical UHD display:
# PREHISTORICTUX_GEOMETRY=3840x2160 PREHISTORICTUX_VIDEO_MODE=fullscreen bash scripts/run-uhd-engine.sh
exec bash "$ROOT/scripts/run-garuda.sh"
