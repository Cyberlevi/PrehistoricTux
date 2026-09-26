#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/PrehistoricTux-The-Lost-Egg.zip"
STAGE="$ROOT/.package-stage"
rm -rf "$STAGE"
mkdir -p "$STAGE"
cp -a "$ROOT/addon"/. "$STAGE"/
PYTHON_BIN="python3"
if ! "$PYTHON_BIN" -c 'import PIL' >/dev/null 2>&1; then
  VENV="$ROOT/.dino-venv"
  if [ ! -x "$VENV/bin/python" ]; then
    python3 -m venv "$VENV"
    "$VENV/bin/python" -m pip install -q -r "$ROOT/requirements-dev.txt"
  fi
  PYTHON_BIN="$VENV/bin/python"
fi
"$PYTHON_BIN" "$ROOT/scripts/generate-dino-assets.py" --output "$STAGE/images/dino"
(
  cd "$STAGE"
  rm -f "$OUT"
  zip -r "$OUT" . -x "*.DS_Store"
)
rm -rf "$STAGE"
echo "$OUT"
