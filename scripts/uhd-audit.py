#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
import pathlib
import re
import struct


ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "art" / "uhd-manifest.json"


def png_size(path: pathlib.Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        signature = handle.read(24)
    if len(signature) < 24 or signature[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    return struct.unpack(">II", signature[16:24])


def parse_surface(path: pathlib.Path) -> tuple[pathlib.Path, float, float]:
    text = path.read_text(encoding="utf-8")
    file_match = re.search(r'\(file\s+"([^"]+)"\)', text)
    if not file_match:
        raise ValueError("surface has no diffuse texture file")

    scale_match = re.search(r'\(scale\s+([0-9.]+)\s+([0-9.]+)\)', text)
    if scale_match:
        sx, sy = float(scale_match.group(1)), float(scale_match.group(2))
    else:
        sx = sy = 1.0

    source = (path.parent / file_match.group(1)).resolve()
    return source, sx, sy


def close_enough(value: float, target: int, tolerance: float = 0.51) -> bool:
    return abs(value - float(target)) <= tolerance


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit active PrehistoricTux .surface bindings against UHD source targets."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero while any active runtime binding is below the UHD target",
    )
    args = parser.parse_args()

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    total = ready = short = 0

    print("PrehistoricTux UHD runtime-binding audit")
    print(f"Master scale target: {data['policy']['master_scale']}x")
    print()

    for group in data["assets"]:
        surfaces = sorted(
            pathlib.Path(p)
            for p in glob.glob(str(ROOT / group["surface_glob"]))
        )
        target_w, target_h = group["minimum_master_size"]
        logical_size = group.get("logical_size")
        logical_w, logical_h = logical_size if logical_size else (None, None)

        if not surfaces:
            print(f"MISSING  {group['name']}: {group['surface_glob']}")
            short += 1
            continue

        group_ready = 0
        for surface in surfaces:
            total += 1
            try:
                source, sx, sy = parse_surface(surface)
                if not source.is_file():
                    raise ValueError(f"source missing: {source}")
                width, height = png_size(source)
            except ValueError as exc:
                print(f"INVALID  {surface.relative_to(ROOT)}: {exc}")
                short += 1
                continue

            effective_w = width * sx
            effective_h = height * sy
            size_ok = width >= target_w and height >= target_h
            logical_ok = True
            if logical_size:
                logical_ok = (
                    close_enough(effective_w, logical_w)
                    and close_enough(effective_h, logical_h)
                )
            ok = size_ok and logical_ok

            if ok:
                ready += 1
                group_ready += 1
                state = "UHD"
            else:
                short += 1
                state = "PROTO"

            print(
                f"{state:5}  {surface.relative_to(ROOT)}\n"
                f"       source={source.relative_to(ROOT)} {width}x{height} "
                f"scale={sx:g}x{sy:g} logical≈{effective_w:g}x{effective_h:g} "
                f"target-source>={target_w}x{target_h} "
                + (f"target-logical={logical_w}x{logical_h}" if logical_size else "target-logical=fullscreen-fit")
            )

        print(f"       {group['name']}: {group_ready}/{len(surfaces)} UHD-ready")
        print()

    print(f"Summary: {ready}/{total} active bindings are genuinely UHD-ready.")
    if short:
        print(
            f"{short} bindings still use prototype-sized art, an incorrect logical scale, "
            "or a missing source."
        )

    return 1 if args.strict and short else 0


if __name__ == "__main__":
    raise SystemExit(main())
