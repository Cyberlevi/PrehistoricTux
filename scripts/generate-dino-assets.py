#!/usr/bin/env python3
from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "addon" / "images" / "dino" / "source" / "dino_strip.png"

# Crop boxes are relative to the 1798x165 source strip.
CROPS = {
    "raptor": (15, 45, 205, 155),
    "alpha_raptor": (220, 45, 405, 155),
    "ptero": (430, 20, 625, 155),
    "trike": (660, 20, 910, 155),
    "ankylo": (920, 45, 1130, 155),
    "plesio": (1110, 20, 1370, 155),
    "nestling": (1370, 50, 1495, 155),
    "palaszarusz": (1510, 15, 1765, 155),
}

CONFIG = {
    "raptor": ((192, 96), 6),
    "alpha_raptor": ((192, 96), 6),
    "ptero": ((224, 128), 6),
    "hunter_ptero": ((224, 128), 6),
    "trike": ((256, 128), 6),
    "ankylo": ((208, 96), 4),
    "plesio": ((224, 112), 6),
    "nestling": ((128, 80), 4),
    "palaszarusz": ((320, 176), 4),
}

def cut_dark_background(img):
    img = img.convert("RGBA")
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            hi = max(r, g, b)
            lo = min(r, g, b)
            sat = hi - lo
            lum = (r + g + b) / 3
            if (lum < 48 and sat < 38) or (r > 150 and g < 40 and b < 40) or (b > 145 and r < 55 and g < 90):
                px[x, y] = (r, g, b, 0)
            elif a:
                px[x, y] = (r, g, b, min(255, int(max(0, lum - 25) * 3.1)))
    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img

def fit_to_canvas(img, size, scale=0.90):
    w, h = size
    maxw, maxh = int(w * scale), int(h * 0.80)
    ratio = min(maxw / img.width, maxh / img.height)
    nw, nh = max(1, int(img.width * ratio)), max(1, int(img.height * ratio))
    return img.resize((nw, nh), Image.Resampling.LANCZOS)

def frame(base, size, bob=0, stretch=1.0, rotate=0, squash=1.0):
    w, h = size
    img = base
    if stretch != 1.0:
        img = img.resize((max(1, int(img.width * stretch)), img.height), Image.Resampling.LANCZOS)
    if squash != 1.0:
        img = img.resize((img.width, max(8, int(img.height * squash))), Image.Resampling.LANCZOS)
    if rotate:
        img = img.rotate(rotate, resample=Image.Resampling.BICUBIC, expand=True)
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    x = (w - img.width) // 2
    y = (h - img.height) // 2 + bob
    out.alpha_composite(img, (x, y))
    return out

def tint(img, factors):
    rfac, gfac, bfac = factors
    img = img.copy().convert("RGBA")
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a:
                px[x, y] = (min(255, int(r * rfac)), min(255, int(g * gfac)), min(255, int(b * bfac)), a)
    return img

def save(img, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, optimize=True)

def generate(output):
    strip = Image.open(SOURCE).convert("RGB")
    sx = strip.width / 1798.0
    sy = strip.height / 165.0
    bases = {}
    for name, box in CROPS.items():
        x1, y1, x2, y2 = box
        scaled_box = (
            max(0, int(round(x1 * sx))),
            max(0, int(round(y1 * sy))),
            min(strip.width, int(round(x2 * sx))),
            min(strip.height, int(round(y2 * sy))),
        )
        art = cut_dark_background(strip.crop(scaled_box))
        if name not in ("ptero",):
            art = ImageOps.mirror(art)
        bases[name] = art

    bases["hunter_ptero"] = tint(bases["ptero"], (0.72, 0.72, 0.86))

    # Ground predators
    for name, prefix in (("raptor", "raptor"), ("alpha_raptor", "alpha")):
        size, _ = CONFIG[name]
        base = fit_to_canvas(bases[name], size)
        for i, (bob, stretch) in enumerate([(0,1.00),(2,.985),(4,.965),(2,.985),(0,1.00),(-2,1.015)]):
            save(frame(base, size, bob=bob, stretch=stretch), output/name/f"{prefix}-run-{i}.png")
        save(frame(base, size, bob=0), output/name/f"{prefix}-idle-0.png")
        save(frame(base, size, bob=1, stretch=.995), output/name/f"{prefix}-idle-1.png")
        save(frame(base, size, bob=14, squash=.48), output/name/f"{prefix}-squished.png")

    # Pterosaurs
    for name, prefix in (("ptero","ptero"), ("hunter_ptero","hunter")):
        size, _ = CONFIG[name]
        base = fit_to_canvas(bases[name], size, .88)
        for i, (bob, squash) in enumerate([(0,1.0),(-4,.94),(-8,.88),(-4,.94),(0,1.0),(3,1.04)]):
            save(frame(base, size, bob=bob, squash=squash), output/name/f"{prefix}-fly-{i}.png")
        if name == "ptero":
            save(frame(base, size, bob=0), output/name/"ptero-glide-0.png")
            save(frame(base, size, bob=2, stretch=1.02), output/name/"ptero-glide-1.png")

    # Heavy dinosaurs
    size,_ = CONFIG["trike"]
    base = fit_to_canvas(bases["trike"], size, .92)
    for i,(bob,stretch) in enumerate([(0,1),(2,.99),(3,.98),(1,1),(0,1.01),(-2,1)]):
        save(frame(base,size,bob=bob,stretch=stretch), output/"trike"/f"trike-walk-{i}.png")
    save(frame(base,size), output/"trike"/"trike-idle-0.png")
    save(frame(base,size,bob=1), output/"trike"/"trike-idle-1.png")

    size,_ = CONFIG["ankylo"]
    base = fit_to_canvas(bases["ankylo"], size, .92)
    for i,bob in enumerate((0,2,0,-2)):
        save(frame(base,size,bob=bob,stretch=(.985 if i in (1,3) else 1.0)), output/"ankylo"/f"ankylo-walk-{i}.png")

    # Water creature
    size,_ = CONFIG["plesio"]
    base = fit_to_canvas(bases["plesio"], size, .90)
    for i,(bob,rot) in enumerate([(0,0),(2,1),(4,2),(2,1),(0,0),(-2,-1)]):
        save(frame(base,size,bob=bob,rotate=rot), output/"plesio"/f"plesio-swim-{i}.png")

    # Nestling
    size,_ = CONFIG["nestling"]
    base = fit_to_canvas(bases["nestling"], size, .88)
    for i,bob in enumerate((0,3,0,-3)):
        save(frame(base,size,bob=bob,stretch=(.96 if i in (1,3) else 1.0)), output/"nestling"/f"nestling-run-{i}.png")

    # Palaszarusz boss
    size,_ = CONFIG["palaszarusz"]
    base = fit_to_canvas(bases["palaszarusz"], size, .94)
    for i,(bob,stretch) in enumerate([(0,1),(3,.99),(0,1),(-3,1.01)]):
        save(frame(base,size,bob=bob,stretch=stretch), output/"palaszarusz"/f"pal-walk-{i}.png")
    for i,(scale,bob) in enumerate(((1.02,-2),(1.05,-3),(1.02,-1))):
        save(frame(base,size,bob=bob,stretch=scale), output/"palaszarusz"/f"pal-roar-{i}.png")
    save(frame(base,size,bob=2,rotate=-4), output/"palaszarusz"/"pal-hurt-0.png")
    save(frame(base,size,bob=4,rotate=4), output/"palaszarusz"/"pal-hurt-1.png")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    generate(Path(args.output))
