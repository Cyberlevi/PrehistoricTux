#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/PrehistoricTux-The-Lost-Egg.zip"
cd "$ROOT/addon"
rm -f "$OUT"
zip -r "$OUT" . -x "*.DS_Store"
echo "$OUT"
