#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/PrehistoricTux-The-Lost-Egg.zip"
STAGE="$ROOT/.package-stage"
rm -rf "$STAGE"
mkdir -p "$STAGE"
cp -a "$ROOT/addon"/. "$STAGE"/
python3 "$ROOT/scripts/generate-dino-assets.py" --output "$STAGE/images/dino"
(
  cd "$STAGE"
  rm -f "$OUT"
  zip -r "$OUT" . -x "*.DS_Store"
)
rm -rf "$STAGE"
echo "$OUT"
