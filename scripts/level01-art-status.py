#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import re
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAN = ROOT / "art" / "level01-production.json"

def png_size(path: pathlib.Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    return struct.unpack(">II", header[16:24])

def parse_surface(path: pathlib.Path) -> tuple[pathlib.Path, float, float]:
    text = path.read_text(encoding="utf-8")
    file_match = re.search(r'\(file\s+"([^"]+)"\)', text)
    if not file_match:
        raise ValueError("surface has no source file")
    scale_match = re.search(r'\(scale\s+([0-9.]+)\s+([0-9.]+)\)', text)
    sx = float(scale_match.group(1)) if scale_match else 1.0
    sy = float(scale_match.group(2)) if scale_match else 1.0
    return (path.parent / file_match.group(1)).resolve(), sx, sy

def main() -> int:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    rows = []
    ready = 0
    for asset in plan["assets"]:
        surface = ROOT / asset["surface"]
        state = "MISSING"
        detail = ""
        if surface.is_file():
            try:
                source, sx, sy = parse_surface(surface)
                if source.is_file():
                    w, h = png_size(source)
                    lw, lh = asset["logical"]
                    mw, mh = asset["minimum"]
                    logical_ok = abs(w * sx - lw) <= 0.51 and abs(h * sy - lh) <= 0.51
                    master_ok = w >= mw and h >= mh
                    state = "UHD" if logical_ok and master_ok else "PROTO"
                    if state == "UHD":
                        ready += 1
                    detail = f"{w}x{h}, scale={sx:g}x{sy:g}"
                else:
                    detail = f"source missing: {source.name}"
            except Exception as exc:
                detail = str(exc)
        rows.append((asset["priority"], asset["id"], state, detail))

    print("Level 01 UHD production status")
    print("==============================")
    for priority, asset_id, state, detail in sorted(rows):
        print(f"P{priority}  {state:7}  {asset_id:24} {detail}")
    print()
    print(f"Ready: {ready}/{len(rows)} ({ready / len(rows) * 100:.1f}%)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
