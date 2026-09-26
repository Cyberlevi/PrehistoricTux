#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ADDON_ID="cyberlevi-prehistorictux"
OUT="$ROOT/dist/$ADDON_ID.zip"

mkdir -p "$ROOT/dist"
rm -f "$OUT"

ROOT="$ROOT" OUT="$OUT" python - <<'PY'
import os
import pathlib
import zipfile

root = pathlib.Path(os.environ["ROOT"])
src = root / "addon"
out = pathlib.Path(os.environ["OUT"])

with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for path in sorted(src.rglob("*")):
        if path.is_file():
            zf.write(path, path.relative_to(src).as_posix())

print(out)
PY

printf 'Packaged add-on: %s\n' "$OUT"
