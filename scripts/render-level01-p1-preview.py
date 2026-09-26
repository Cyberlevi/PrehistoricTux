#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Pillow is required. Run: bash scripts/setup-garuda-art-tools.sh", file=sys.stderr)
    raise SystemExit(2)

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "art" / "incoming" / "level01"
OUT = BASE / "P1_PREVIEW.png"

RAPTORS = [
    BASE / "raptor" / "raptor-walk-0@4x.png",
    BASE / "raptor" / "raptor-walk-1@4x.png",
    BASE / "raptor" / "raptor-walk-2@4x.png",
    BASE / "raptor" / "raptor-walk-3@4x.png",
    BASE / "raptor" / "raptor-squished@4x.png",
]
TILES = [
    BASE / "terrain" / "jungle-fill@4x.png",
    BASE / "terrain" / "jungle-top@4x.png",
]

missing = [p for p in RAPTORS + TILES if not p.is_file()]
if missing:
    for p in missing:
        print(f"Missing: {p.relative_to(ROOT)}", file=sys.stderr)
    raise SystemExit(1)

W, H = 1480, 640
sheet = Image.new("RGB", (W, H), (27, 30, 31))
d = ImageDraw.Draw(sheet)

d.text((28, 20), "PrehistoricTux — Level 01 P1 actual generated assets", fill=(240, 231, 202))
d.text((28, 48), "Raptor runtime source: 256×192  |  Jungle tiles: 128×128", fill=(190, 199, 198))

x = 28
for idx, path in enumerate(RAPTORS):
    src = Image.open(path).convert("RGBA")
    # checkerboard makes transparency obvious without modifying the source.
    box = Image.new("RGB", src.size, (200, 200, 200))
    bd = ImageDraw.Draw(box)
    cell = 16
    for yy in range(0, src.height, cell):
        for xx in range(0, src.width, cell):
            if ((xx // cell) + (yy // cell)) % 2:
                bd.rectangle((xx, yy, xx + cell - 1, yy + cell - 1), fill=(228, 228, 228))
    box.paste(src, (0, 0), src)
    sheet.paste(box, (x, 92))
    d.rectangle((x, 92, x + src.width - 1, 92 + src.height - 1), outline=(82, 91, 91))
    d.text((x, 292), path.stem.replace("@4x", ""), fill=(220, 220, 214))
    x += 282

d.text((28, 346), "Jungle terrain", fill=(240, 231, 202))
x = 28
for path in TILES:
    src = Image.open(path).convert("RGB")
    shown = src.resize((256, 256), Image.Resampling.NEAREST)
    sheet.paste(shown, (x, 378))
    d.rectangle((x, 378, x + 255, 633), outline=(82, 91, 91))
    d.text((x + 270, 398), path.stem.replace("@4x", ""), fill=(220, 220, 214))
    d.text((x + 270, 424), "128×128 source, shown 2×", fill=(164, 176, 174))
    x += 700

OUT.parent.mkdir(parents=True, exist_ok=True)
sheet.save(OUT, optimize=True)
print(OUT.relative_to(ROOT))
