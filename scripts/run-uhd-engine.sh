#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="$ROOT/.engine/build-0.7.0-uhd/supertux2"

if [[ ! -x "$BIN" ]]; then
  echo "Patched UHD engine is not built yet." >&2
  echo "Run: bash scripts/build-uhd-engine.sh" >&2
  exit 1
fi

export SUPERTUX_BIN="$BIN"
export PREHISTORICTUX_RENDERER="${PREHISTORICTUX_RENDERER:-opengl}"

# Keep current 1080p monitors safe by default. On a physical UHD display:
# PREHISTORICTUX_GEOMETRY=3840x2160 PREHISTORICTUX_VIDEO_MODE=fullscreen bash scripts/run-uhd-engine.sh
exec bash "$ROOT/scripts/run-garuda.sh"
