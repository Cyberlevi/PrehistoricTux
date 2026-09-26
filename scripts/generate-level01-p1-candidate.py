#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import pathlib
import random
import subprocess
import sys

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    print(
        "Pillow is required for production-art generation.\n"
        "Garuda/Arch: sudo pacman -S --needed python-pillow",
        file=sys.stderr,
    )
    raise SystemExit(2)

ROOT = pathlib.Path(__file__).resolve().parents[1]
INCOMING = ROOT / "art" / "incoming" / "level01"

RAPTOR_SIZE = (256, 192)
TILE_SIZE = (128, 128)
SCALE = 4


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def poly(draw: ImageDraw.ImageDraw, pts, fill, outline=None, width=1):
    draw.polygon([(int(x), int(y)) for x, y in pts], fill=fill)
    if outline:
        draw.line(
            [(int(x), int(y)) for x, y in pts] + [(int(pts[0][0]), int(pts[0][1]))],
            fill=outline,
            width=width,
            joint="curve",
        )


def ellipse(draw, box, fill, outline=None, width=1):
    box = tuple(int(v) for v in box)
    draw.ellipse(box, fill=fill, outline=outline, width=width)


def line(draw, pts, fill, width):
    draw.line([(int(x), int(y)) for x, y in pts], fill=fill, width=width, joint="curve")


def raptor_frame(frame: int, squished: bool = False) -> Image.Image:
    # Author at 4x output resolution, then supersample internally another 2x
    # so curves and feather edges remain clean when exported to 256x192.
    W, H = 512, 384
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(4100 + frame + (100 if squished else 0))

    outline = (43, 28, 20, 255)
    shadow = (92, 49, 27, 255)
    mid = (169, 84, 38, 255)
    light = (215, 124, 55, 255)
    cream = (223, 202, 158, 255)
    dark = (66, 42, 30, 255)
    feather = (85, 47, 31, 255)

    if squished:
        # Defeated pose intentionally keeps the same world-space baseline.
        body_y = 267
        # tail
        poly(d, [(232,260),(163,244),(91,238),(34,250),(92,269),(169,279),(244,286)],
             outline)
        poly(d, [(226,261),(161,250),(93,246),(45,252),(98,263),(167,272),(239,280)],
             mid)
        # body and chest
        ellipse(d, (205,221,382,314), outline)
        ellipse(d, (214,229,374,304), mid)
        ellipse(d, (276,250,382,309), cream)
        # neck/head low to ground
        poly(d, [(335,242),(386,239),(422,251),(433,272),(390,277),(350,268)], outline)
        poly(d, [(340,247),(383,244),(415,253),(424,268),(389,271),(352,264)], light)
        poly(d, [(401,254),(472,257),(484,273),(468,286),(400,282)], outline)
        poly(d, [(404,258),(467,261),(477,272),(463,280),(402,277)], light)
        ellipse(d, (438,260,450,272), (255,196,32,255), outline, 2)
        ellipse(d, (443,263,447,268), (10,10,8,255))
        # folded legs
        for x in (238, 310):
            line(d, [(x,287),(x-24,314),(x+25,320)], outline, 18)
            line(d, [(x,287),(x-22,311),(x+23,316)], shadow, 10)
        # feathers
        for x in range(228, 354, 18):
            poly(d, [(x,229),(x+10,211-rng.randint(0,8)),(x+18,234)], feather)
        # freckles
        for _ in range(34):
            x=rng.randint(225,365); y=rng.randint(238,298)
            ellipse(d,(x-3,y-2,x+3,y+2),(73,44,28,110))
    else:
        gait = [
            (-34, 28, 42, -6),
            (28, -6, -38, 30),
            (42, 8, -20, 24),
            (-18, 30, 36, -4),
        ][frame % 4]
        rear_dx, rear_dy, front_dx, front_dy = gait
        bob = [0, 7, -4, 5][frame % 4]
        body_y = 205 + bob

        # tail: broad base, thin tip, slight counter-swing
        tail_tip_y = 205 - frame * 3
        poly(d, [
            (270,205+bob),(198,184+bob),(121,183+bob),(39,209+tail_tip_y-205),
            (117,220+bob),(198,226+bob),(281,229+bob)
        ], outline)
        poly(d, [
            (267,207+bob),(198,191+bob),(124,191+bob),(52,208+tail_tip_y-205),
            (122,213+bob),(199,218+bob),(277,223+bob)
        ], mid)

        # body
        ellipse(d, (234,155+bob,386,266+bob), outline)
        ellipse(d, (243,163+bob,379,257+bob), mid)
        ellipse(d, (292,190+bob,378,254+bob), cream)

        # neck
        poly(d, [(332,181+bob),(350,120+bob),(385,83+bob),(424,101+bob),
                 (395,147+bob),(382,207+bob)], outline)
        poly(d, [(341,183+bob),(357,126+bob),(388,93+bob),(414,104+bob),
                 (389,148+bob),(374,202+bob)], light)
        # throat
        poly(d, [(381,109+bob),(407,120+bob),(388,183+bob),(365,190+bob)], cream)

        # head + snout
        ellipse(d, (374,72+bob,458,130+bob), outline)
        ellipse(d, (381,78+bob,452,124+bob), light)
        poly(d, [(424,91+bob),(492,96+bob),(502,111+bob),(485,127+bob),
                 (423,124+bob)], outline)
        poly(d, [(427,96+bob),(486,100+bob),(495,110+bob),(481,120+bob),
                 (425,119+bob)], light)
        # mouth
        line(d, [(433,115+bob),(483,116+bob)], dark, 3)
        for tx in (445,458,471):
            poly(d, [(tx,116+bob),(tx+4,116+bob),(tx+2,122+bob)], (240,230,196,255))
        # eye
        ellipse(d,(416,88+bob,431,103+bob),(255,193,29,255),outline,2)
        ellipse(d,(422,92+bob,427,99+bob),(8,8,5,255))

        # hind legs - two articulated limbs
        baseline = 337
        hip1=(285,235+bob); knee1=(274+rear_dx,278+rear_dy//3); foot1=(248+rear_dx,baseline)
        hip2=(334,236+bob); knee2=(347+front_dx,279+front_dy//3); foot2=(372+front_dx,baseline-2)
        for hip,knee,foot,c in [
            (hip1,knee1,foot1,shadow),
            (hip2,knee2,foot2,mid),
        ]:
            line(d,[hip,knee,foot],outline,28)
            line(d,[hip,knee,foot],c,18)
            # foot and claws
            line(d,[foot,(foot[0]+30,foot[1]+2)],outline,12)
            line(d,[foot,(foot[0]+27,foot[1])],c,7)
            for cx in (foot[0]+17,foot[0]+27):
                line(d,[(cx,foot[1]),(cx+9,foot[1]+5)],(32,28,25,255),3)

        # small arms
        shoulder=(370,186+bob)
        for off in (0,18):
            elbow=(388+off,215+bob)
            hand=(405+off,235+bob)
            line(d,[shoulder,elbow,hand],outline,13)
            line(d,[shoulder,elbow,hand],mid,7)
            for k in range(2):
                line(d,[hand,(hand[0]+10,hand[1]-2+k*5)],(35,29,25,255),2)

        # dorsal feather/scale ridge
        for x in range(262,410,15):
            center_bias=1.0-abs(x-340)/100
            hh=10+int(max(0,center_bias)*12)+rng.randint(-2,3)
            y=int(163+bob - max(0,center_bias)*28)
            poly(d,[(x-5,y+6),(x,y-hh),(x+7,y+6)],feather)

        # tiger-like body markings
        for x in range(270,360,20):
            line(d,[(x,166+bob),(x+9,195+bob)],(73,42,27,160),7)
        # subtle body texture
        for _ in range(44):
            x=rng.randint(248,372); y=rng.randint(170+bob,246+bob)
            ellipse(d,(x-3,y-2,x+3,y+2),(238,151,75,rng.randint(30,85)))

    # Soft internal highlight, never a baked floor shadow.
    img = img.resize(RAPTOR_SIZE, Image.Resampling.LANCZOS)
    return img


def draw_leaf(draw, x, y, size, angle, color):
    # Tiny pointed leaf polygon.
    ca, sa = math.cos(angle), math.sin(angle)
    pts=[]
    for px,py in [(-size*.18,0),(0,-size),(size*.18,0),(0,size*.22)]:
        pts.append((x+px*ca-py*sa, y+px*sa+py*ca))
    poly(draw,pts,color)


def rock_field(seed: int, top_edge: bool) -> Image.Image:
    W=512
    rng=random.Random(seed)
    img=Image.new("RGBA",(W,W),(43,34,25,255))
    d=ImageDraw.Draw(img,"RGBA")

    # layered soil base
    for y in range(W):
        t=y/(W-1)
        col=(int(66-16*t),int(52-15*t),int(35-8*t),255)
        d.line((0,y,W,y),fill=col)

    # large overlapping rocks; wrap copies near side boundaries for repeatability
    rocks=[]
    for row in range(5):
        yy=70+row*98+rng.randint(-18,18)
        for col in range(5):
            xx=40+col*108+rng.randint(-22,22)
            rx=rng.randint(44,67); ry=rng.randint(38,60)
            rocks.append((xx,yy,rx,ry))
    for xx,yy,rx,ry in rocks:
        base=rng.choice([(92,70,48,255),(104,78,51,255),(82,65,46,255),(115,84,55,255)])
        for shift in (-W,0,W):
            box=(xx-rx+shift,yy-ry,xx+rx+shift,yy+ry)
            ellipse(d,box,(39,31,25,255))
            inset=8
            ellipse(d,(box[0]+inset,box[1]+inset,box[2]-inset,box[3]-inset),base)
            # highlight + crack
            ellipse(d,(xx-rx*.45+shift,yy-ry*.45,xx+rx*.08+shift,yy+ry*.02),(165,130,80,80))
            if rng.random()<.8:
                line(d,[(xx-12+shift,yy-12),(xx+4+shift,yy+3),(xx-6+shift,yy+20)],(45,34,28,180),4)

    # roots and vines
    for _ in range(22):
        x=rng.randint(-30,W+30); y=rng.randint(0,W)
        length=rng.randint(30,105)
        col=rng.choice([(48,91,30,220),(61,111,35,230),(77,121,39,210)])
        line(d,[(x,y),(x+rng.randint(-18,18),y+length//2),(x+rng.randint(-20,20),y+length)],col,rng.randint(3,7))

    # moss + small ferns
    for _ in range(120):
        x=rng.randrange(W); y=rng.randrange(W)
        if rng.random()<0.55 or y<100:
            color=rng.choice([(70,118,33,210),(90,143,42,220),(111,161,53,210),(45,98,30,210)])
            draw_leaf(d,x,y,rng.randint(5,13),rng.random()*math.tau,color)

    if top_edge:
        # clean, readable platform cap
        d.rectangle((0,0,W,34),fill=(50,43,28,255))
        for x in range(-20,W+30,18):
            size=rng.randint(18,34)
            draw_leaf(d,x+rng.randint(-4,4),36,size,rng.uniform(-.8,.8),
                      rng.choice([(78,135,35,255),(99,157,44,255),(124,177,56,255)]))
        # dangling vines only below the cap
        for x in range(18,W,62):
            ln=rng.randint(45,130)
            line(d,[(x,32),(x+rng.randint(-10,10),32+ln)],(54,112,31,240),6)
            for yy in range(52,32+ln,22):
                draw_leaf(d,x+rng.randint(-7,7),yy,10,rng.uniform(-1.1,1.1),(77,137,38,235))

    img=img.resize(TILE_SIZE,Image.Resampling.LANCZOS)
    # Runtime terrain should be fully opaque.
    if img.mode!="RGBA":
        img=img.convert("RGBA")
    alpha=Image.new("L",img.size,255)
    img.putalpha(alpha)
    return img


def save_assets() -> list[pathlib.Path]:
    out=[]
    rdir=INCOMING/"raptor"
    tdir=INCOMING/"terrain"
    rdir.mkdir(parents=True,exist_ok=True)
    tdir.mkdir(parents=True,exist_ok=True)

    for i in range(4):
        p=rdir/f"raptor-walk-{i}@4x.png"
        raptor_frame(i).save(p,optimize=True)
        out.append(p)
    p=rdir/"raptor-squished@4x.png"
    raptor_frame(0,squished=True).save(p,optimize=True)
    out.append(p)

    p=tdir/"jungle-fill@4x.png"
    rock_field(8141,False).save(p,optimize=True)
    out.append(p)
    p=tdir/"jungle-top@4x.png"
    rock_field(8141,True).save(p,optimize=True)
    out.append(p)
    return out


def run(cmd: list[str]) -> None:
    print("+"," ".join(cmd))
    subprocess.run(cmd,cwd=ROOT,check=True)


def main()->int:
    parser=argparse.ArgumentParser(
        description="Generate a deterministic high-detail Level 01 P1 art candidate."
    )
    parser.add_argument("--promote",action="store_true",
                        help="run QA and promote the generated P1 assets into runtime bindings")
    args=parser.parse_args()

    files=save_assets()
    print("Generated Level 01 P1 candidate assets:")
    for p in files:
        print(" ",p.relative_to(ROOT))

    run([sys.executable,"scripts/level01-p1-qa.py"])
    run([sys.executable,"scripts/promote-level01-art.py","--priority","1","--dry-run"])

    if args.promote:
        run([sys.executable,"scripts/promote-level01-art.py","--priority","1"])
        run([sys.executable,"scripts/level01-art-status.py"])
        run([sys.executable,"scripts/uhd-audit.py"])
        print()
        print("P1 runtime bindings promoted. Test with: bash scripts/play-level.sh 1")
    else:
        print()
        print("Candidate assets passed QA. Re-run with --promote to activate them.")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
