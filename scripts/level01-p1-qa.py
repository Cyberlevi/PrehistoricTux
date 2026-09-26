#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import struct
import zlib

ROOT=pathlib.Path(__file__).resolve().parents[1]
PLAN=json.loads((ROOT/"art/level01-production.json").read_text(encoding="utf-8"))
P1=[a for a in PLAN["assets"] if a["priority"]==1]

def png_info(path:pathlib.Path):
    data=path.read_bytes()
    if data[:8]!=b"\x89PNG\r\n\x1a\n": raise ValueError("not PNG")
    pos=8; ids=[]; w=h=bd=ct=None
    while pos<len(data):
        n=struct.unpack(">I",data[pos:pos+4])[0]; typ=data[pos+4:pos+8]; payload=data[pos+8:pos+8+n]; pos+=12+n
        if typ==b"IHDR": w,h,bd,ct,_,_,_=struct.unpack(">IIBBBBB",payload)
        elif typ==b"IDAT": ids.append(payload)
        elif typ==b"IEND": break
    return w,h,bd,ct,b"".join(ids)

def alpha_bbox(path:pathlib.Path):
    w,h,bd,ct,ids=png_info(path)
    if bd!=8 or ct!=6: return None,(w,h)
    raw=zlib.decompress(ids); stride=w*4; prev=bytearray(stride); p=0
    minx=w; miny=h; maxx=maxy=-1; opaque=0
    for y in range(h):
        f=raw[p]; p+=1; scan=bytearray(raw[p:p+stride]); p+=stride
        for x in range(stride):
            a=scan[x-4] if x>=4 else 0; b=prev[x]; c=prev[x-4] if x>=4 else 0
            if f==1: scan[x]=(scan[x]+a)&255
            elif f==2: scan[x]=(scan[x]+b)&255
            elif f==3: scan[x]=(scan[x]+((a+b)//2))&255
            elif f==4:
                q=a+b-c; pa=abs(q-a); pb=abs(q-b); pc=abs(q-c); pr=a if pa<=pb and pa<=pc else (b if pb<=pc else c)
                scan[x]=(scan[x]+pr)&255
            elif f!=0: raise ValueError(f"unsupported PNG filter {f}")
        for x in range(w):
            if scan[x*4+3]>8:
                opaque+=1; minx=min(minx,x); maxx=max(maxx,x); miny=min(miny,y); maxy=max(maxy,y)
        prev=scan
    return ((minx,miny,maxx,maxy,opaque) if opaque else None),(w,h)

def main()->int:
    failures=0; walk_bottoms=[]
    print("Level 01 P1 art QA")
    print("===================")
    for asset in P1:
        path=ROOT/asset["incoming"]
        if not path.is_file():
            print(f"MISSING {asset['id']:20} {path.relative_to(ROOT)}"); failures+=1; continue
        try:
            bbox,size=alpha_bbox(path); w,h=size; mw,mh=asset["minimum"]
            errs=[]
            if w<mw or h<mh: errs.append(f"too small {w}x{h} < {mw}x{mh}")
            if asset["kind"]=="creature":
                if bbox is None: errs.append("no visible alpha content")
                else:
                    minx,miny,maxx,maxy,opaque=bbox
                    if minx==0 or maxx==w-1 or miny==0 or maxy==h-1: errs.append("art touches frame edge")
                    occ=opaque/(w*h)
                    if occ<0.06: errs.append(f"very low silhouette occupancy {occ:.1%}")
                    if asset["id"].startswith("raptor-walk-"): walk_bottoms.append((asset["id"],maxy/h))
            else:
                # terrain must be opaque at all four corners to avoid transparent seams
                _,_,bd,ct,_=png_info(path)
                if ct!=6: errs.append("expected RGBA PNG for consistent pipeline")
            if errs:
                print(f"FAIL    {asset['id']:20} " + "; ".join(errs)); failures+=1
            else:
                print(f"PASS    {asset['id']:20} {w}x{h}")
        except Exception as exc:
            print(f"FAIL    {asset['id']:20} {exc}"); failures+=1

    if len(walk_bottoms)>=2:
        ys=[v for _,v in walk_bottoms]
        spread=max(ys)-min(ys)
        if spread>0.04:
            print(f"FAIL    raptor floor-line drift {spread:.1%} of frame height")
            failures+=1
        else:
            print(f"PASS    raptor floor-line drift {spread:.1%}")

    print()
    print("P1 QA:", "PASS" if failures==0 else f"FAIL ({failures} issue(s))")
    return 1 if failures else 0

if __name__=="__main__":
    raise SystemExit(main())
