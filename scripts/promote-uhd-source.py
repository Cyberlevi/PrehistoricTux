#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import struct
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]


def png_size(path: pathlib.Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    return struct.unpack(">II", header[16:24])


def parse_logical(value: str) -> tuple[int, int]:
    m = re.fullmatch(r"(\d+)[xX](\d+)", value)
    if not m:
        raise argparse.ArgumentTypeError("logical size must look like 64x48")
    return int(m.group(1)), int(m.group(2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote a genuine UHD PNG into an active .surface binding.")
    parser.add_argument("--surface", required=True, type=pathlib.Path)
    parser.add_argument("--source", required=True, type=pathlib.Path)
    parser.add_argument("--logical", required=True, type=parse_logical)
    parser.add_argument("--minimum-scale", type=int, default=4)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    surface = args.surface if args.surface.is_absolute() else ROOT / args.surface
    source = args.source.expanduser().resolve()

    if not surface.is_file():
        print(f"Surface binding not found: {surface}", file=sys.stderr)
        return 2
    if not source.is_file():
        print(f"Source image not found: {source}", file=sys.stderr)
        return 2

    width, height = png_size(source)
    logical_w, logical_h = args.logical

    minimum_w = logical_w * args.minimum_scale
    minimum_h = logical_h * args.minimum_scale
    if width < minimum_w or height < minimum_h:
        print(
            f"Source is only {width}x{height}; expected at least "
            f"{minimum_w}x{minimum_h} for {args.minimum_scale}x UHD.",
            file=sys.stderr,
        )
        return 3

    sx = logical_w / width
    sy = logical_h / height
    if abs(sx - sy) > 0.000001:
        print(
            f"Non-uniform logical scale would be required: {sx:.8f} x {sy:.8f}. "
            "Crop/export the art at the correct aspect ratio first.",
            file=sys.stderr,
        )
        return 4

    suffix = f"@{args.minimum_scale}x"
    destination = surface.with_name(surface.stem + suffix + ".png")
    surface_text = f"""(supertux-surface
  ; Promoted UHD runtime binding.
  (scale {sx:.8f} {sy:.8f})
  (diffuse-texture
    (file "{destination.name}")
    (filter "linear")
  )
)
"""

    print(f"Surface:     {surface.relative_to(ROOT)}")
    print(f"Source:      {source} ({width}x{height})")
    print(f"Destination: {destination.relative_to(ROOT)}")
    print(f"Logical:     {logical_w}x{logical_h}")
    print(f"Scale:       {sx:.8f}")

    if args.dry_run:
        print("Dry run: no files changed.")
        return 0

    shutil.copy2(source, destination)
    surface.write_text(surface_text, encoding="utf-8")
    print("Promoted UHD source and updated runtime binding.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
