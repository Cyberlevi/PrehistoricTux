#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
ADDON=ROOT/"addon"
LEVELS=ADDON/"levels"/"prehistoric_tux"
errors=[]

def count_tile_rle(payload):
    nums=[int(x) for x in re.findall(r'-?\d+', payload)]
    total=0
    i=0
    while i < len(nums):
        if nums[i] < 0:
            total += -nums[i]
            i += 2
        else:
            total += 1
            i += 1
    return total

def balanced(text, path):
    depth=0; quote=False; esc=False
    for ch in text:
        if quote:
            if esc: esc=False
            elif ch=="\\": esc=True
            elif ch=='"': quote=False
            continue
        if ch=='"': quote=True
        elif ch=='(': depth+=1
        elif ch==')':
            depth-=1
            if depth<0:
                errors.append(f"{path}: unexpected )"); return
    if quote: errors.append(f"{path}: unterminated string")
    if depth: errors.append(f"{path}: parenthesis depth {depth}")
for p in list(LEVELS.glob("*.stl"))+[LEVELS/"worldmap.stwm"]+list((ADDON/"images"/"dino").rglob("*.sprite")):
    if not p.exists():
        errors.append(f"missing: {p}"); continue
    balanced(p.read_text(encoding="utf-8"), p.relative_to(ROOT))
levels=sorted(LEVELS.glob("[0-9][0-9]_*.stl"))
playable=[p for p in levels if p.name!="00_prologue.stl"]
if len(playable)!=8:
    errors.append(f"expected 8 playable campaign levels, found {len(playable)}")
if not (LEVELS/"00_prologue.stl").is_file():
    errors.append("missing prologue: 00_prologue.stl")
wm=(LEVELS/"worldmap.stwm").read_text(encoding="utf-8")
for m in re.finditer(r'\(tilemap[\s\S]*?\(width\s+(\d+)\)[\s\S]*?\(height\s+(\d+)\)[\s\S]*?\(tiles\s+([\s\S]*?)\)\s*\)', wm):
    width=int(m.group(1)); height=int(m.group(2))
    actual=count_tile_rle(m.group(3))
    expected=width*height
    if actual != expected:
        errors.append(f"worldmap tilemap has {actual} tiles, expected {expected} ({width}x{height})")
for ref in re.findall(r'\(level "([^"]+\.stl)"\)', wm):
    if not (LEVELS/ref).is_file():
        errors.append(f"worldmap missing level: {ref}")
for p in playable:
    t=p.read_text(encoding="utf-8")
    for ref in re.findall(r'"/images/dino/([^"]+\.sprite)"', t):
        if not (ADDON/"images"/"dino"/ref).is_file():
            errors.append(f"{p.name}: missing dino sprite {ref}")
for p in (ADDON/"images"/"dino").rglob("*.sprite"):
    t=p.read_text(encoding="utf-8")
    for fn in re.findall(r'"([^"]+\.png)"', t):
        if not (p.parent/fn).is_file():
            errors.append(f"{p.relative_to(ROOT)}: missing frame {fn}")
if errors:
    print("\n".join("ERROR: "+x for x in errors)); sys.exit(1)
print("PrehistoricTux static validation: OK")
print("8 playable levels + prologue + worldmap + dinosaur sprite references present")
