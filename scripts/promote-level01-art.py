#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAN = ROOT / "art" / "level01-production.json"

def png_size(path: pathlib.Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    return struct.unpack(">II", header[16:24])

def promote(asset: dict, dry_run: bool) -> tuple[bool, str]:
    source = ROOT / asset["incoming"]
    surface = ROOT / asset["surface"]
    if not source.is_file():
        return False, "incoming missing"

    width, height = png_size(source)
    logical_w, logical_h = asset["logical"]
    minimum_w, minimum_h = asset["minimum"]
    if width < minimum_w or height < minimum_h:
        return False, f"too small {width}x{height} < {minimum_w}x{minimum_h}"

    sx, sy = logical_w / width, logical_h / height
    if abs(sx - sy) > 0.000001:
        return False, f"aspect mismatch: scale {sx:.8f} vs {sy:.8f}"

    destination = surface.with_name(source.name)
    content = f"""(supertux-surface
  ; Promoted Level 01 UHD runtime binding.
  (scale {sx:.8f} {sy:.8f})
  (diffuse-texture
    (file "{destination.name}")
    (filter "linear")
  )
)
"""
    if dry_run:
        return True, f"would promote {width}x{height} scale={sx:.8f}"

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    surface.write_text(content, encoding="utf-8")
    return True, f"promoted {width}x{height} scale={sx:.8f}"

def main() -> int:
    parser = argparse.ArgumentParser(description="Batch-promote incoming Level 01 UHD exports.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--priority", type=int, choices=(1,2,3))
    args = parser.parse_args()

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    selected = [a for a in plan["assets"] if args.priority is None or a["priority"] <= args.priority]
    promoted = skipped = 0
    for asset in selected:
        ok, detail = promote(asset, args.dry_run)
        print(f"{'OK' if ok else 'SKIP':4} {asset['id']:24} {detail}")
        if ok: promoted += 1
        else: skipped += 1

    print()
    print(f"Promotable/promoted: {promoted}; skipped: {skipped}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
