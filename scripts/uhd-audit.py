#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
import pathlib
import struct
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "art" / "uhd-manifest.json"


def png_size(path: pathlib.Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        signature = handle.read(24)
    if len(signature) < 24 or signature[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    width, height = struct.unpack(">II", signature[16:24])
    return width, height


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit PrehistoricTux art against UHD source targets.")
    parser.add_argument("--strict", action="store_true", help="exit non-zero when a prototype asset is below UHD target")
    args = parser.parse_args()

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    total = 0
    ready = 0
    short = 0

    print("PrehistoricTux UHD asset audit")
    print(f"Master scale target: {data['policy']['master_scale']}x")
    print()

    for group in data["assets"]:
        matches = sorted(pathlib.Path(p) for p in glob.glob(str(ROOT / group["glob"])))
        target_w, target_h = group["minimum_master_size"]

        if not matches:
            print(f"MISSING  {group['name']}: no assets matched {group['glob']}")
            short += 1
            continue

        group_ready = 0
        for path in matches:
            total += 1
            try:
                width, height = png_size(path)
            except ValueError as exc:
                print(f"INVALID  {path.relative_to(ROOT)}: {exc}")
                short += 1
                continue

            ok = width >= target_w and height >= target_h
            if ok:
                ready += 1
                group_ready += 1
                state = "UHD"
            else:
                short += 1
                state = "PROTO"

            print(
                f"{state:5}  {path.relative_to(ROOT)}  "
                f"{width}x{height}  target>={target_w}x{target_h}"
            )

        print(f"       {group['name']}: {group_ready}/{len(matches)} UHD-ready")
        print()

    print(f"Summary: {ready}/{total} checked PNGs meet current UHD source targets.")
    if short:
        print(f"{short} prototype/missing assets still need a genuine high-detail art pass.")

    return 1 if args.strict and short else 0


if __name__ == "__main__":
    raise SystemExit(main())
