#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import struct
import sys
import zlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "art" / "level01-p1-spec.json"

def read_png_rgba(path: pathlib.Path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("input is not a PNG")
    pos=8; width=height=None; color_type=None; bit_depth=None; chunks=[]
    while pos < len(data):
        length=struct.unpack(">I",data[pos:pos+4])[0]
        typ=data[pos+4:pos+8]; payload=data[pos+8:pos+8+length]
        pos += 12+length
        if typ==b"IHDR":
            width,height,bit_depth,color_type,_,_,_=struct.unpack(">IIBBBBB",payload)
        elif typ==b"IDAT":
            chunks.append(payload)
        elif typ==b"IEND":
            break
    if bit_depth!=8 or color_type!=6:
        raise ValueError("sprite sheet must be 8-bit RGBA PNG")
    raw=zlib.decompress(b"".join(chunks))
    stride=width*4
    rows=[]; prev=bytearray(stride); p=0
    for _ in range(height):
        f=raw[p]; p+=1
        scan=bytearray(raw[p:p+stride]); p+=stride
        bpp=4
        for x in range(stride):
            a=scan[x-bpp] if x>=bpp else 0
            b=prev[x]
            c=prev[x-bpp] if x>=bpp else 0
            if f==1: scan[x]=(scan[x]+a)&255
            elif f==2: scan[x]=(scan[x]+b)&255
            elif f==3: scan[x]=(scan[x]+((a+b)//2))&255
            elif f==4:
                q=a+b-c; pa=abs(q-a); pb=abs(q-b); pc=abs(q-c)
                pr=a if pa<=pb and pa<=pc else (b if pb<=pc else c)
                scan[x]=(scan[x]+pr)&255
            elif f!=0: raise ValueError(f"unsupported PNG filter {f}")
        rows.append(bytes(scan)); prev=scan
    return width,height,rows

def png_chunk(kind: bytes, payload: bytes)->bytes:
    return struct.pack(">I",len(payload))+kind+payload+struct.pack(">I",zlib.crc32(kind+payload)&0xffffffff)

def write_png(path: pathlib.Path, width:int, height:int, rows:list[bytes]):
    raw=b"".join(b"\x00"+row for row in rows)
    ihdr=struct.pack(">IIBBBBB",width,height,8,6,0,0,0)
    data=b"\x89PNG\r\n\x1a\n"+png_chunk(b"IHDR",ihdr)+png_chunk(b"IDAT",zlib.compress(raw,9))+png_chunk(b"IEND",b"")
    path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data)

def main()->int:
    parser=argparse.ArgumentParser(description="Slice a horizontal five-frame RGBA raptor sheet into Level 01 incoming UHD frames.")
    parser.add_argument("sheet",type=pathlib.Path)
    args=parser.parse_args()
    spec=json.loads(SPEC.read_text(encoding="utf-8"))["raptor"]
    width,height,rows=read_png_rgba(args.sheet.expanduser().resolve())
    cols=spec["sheet_columns"]
    if width%cols:
        print(f"sheet width {width} is not divisible by {cols}",file=sys.stderr); return 2
    fw=width//cols; fh=height
    mw,mh=spec["minimum_frame_size"]
    if fw<mw or fh<mh:
        print(f"cells are only {fw}x{fh}; minimum is {mw}x{mh}",file=sys.stderr); return 3
    if abs((fw/fh)-(4/3))>0.01:
        print(f"cell aspect must be 4:3; got {fw}x{fh}",file=sys.stderr); return 4

    for idx,asset_id in enumerate(spec["frame_ids"]):
        x0=idx*fw
        sliced=[row[x0*4:(x0+fw)*4] for row in rows]
        out=ROOT/"art/incoming/level01/raptor"/f"{asset_id}@4x.png"
        write_png(out,fw,fh,sliced)
        print(f"WROTE {out.relative_to(ROOT)} {fw}x{fh}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
