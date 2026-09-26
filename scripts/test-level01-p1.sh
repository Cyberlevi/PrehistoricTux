#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! python - <<'PY' >/dev/null 2>&1
from PIL import Image
PY
then
  echo "Python Pillow is missing." >&2
  if command -v pacman >/dev/null 2>&1; then
    echo "Install it with:" >&2
    echo "  bash scripts/setup-garuda-art-tools.sh" >&2
  fi
  exit 1
fi

echo "=== Generate Level 01 P1 UHD candidate ==="
python scripts/generate-level01-p1-candidate.py --promote

echo
echo "=== Re-run structural validation ==="
python scripts/validate_levels.py

echo
echo "=== Verify active P1 runtime bindings ==="
python scripts/level01-art-status.py

echo
echo "=== Launch Level 01 through patched UHD engine ==="
echo "Close the game window when you have finished the visual check."
exec bash scripts/play-uhd-level.sh 1
