#!/usr/bin/env python3
from PIL import Image, ImageDraw
from pathlib import Path
import argparse

def poly(d,p,f,o=(28,35,24,255),w=2):
    d.polygon(p,fill=f)
    if o: d.line(p+[p[0]],fill=o,width=w,joint="curve")
def ell(d,b,f,o=(28,35,24,255),w=2): d.ellipse(b,fill=f,outline=o,width=w)
def line(d,p,f,w=3): d.line(p,fill=f,width=w,joint="curve")
def cv(w,h): return Image.new("RGBA",(w,h),(0,0,0,0))

P={
"raptor":((83,135,72,255),(47,80,45,255),(130,171,102,255),(219,193,126,255)),
"alpha":((149,72,60,255),(84,39,40,255),(190,105,82,255),(230,192,126,255)),
"ptero":((160,127,83,255),(91,69,54,255),(199,166,117,255),(224,197,133,255)),
"hunter":((104,88,102,255),(54,48,62,255),(145,123,140,255),(212,179,120,255)),
"trike":((102,125,75,255),(60,75,48,255),(151,160,103,255),(218,199,140,255)),
"ankylo":((116,102,77,255),(69,62,50,255),(158,140,103,255),(205,187,134,255)),
"plesio":((59,131,138,255),(35,80,87,255),(92,170,169,255),(199,207,145,255)),
"nestling":((147,154,76,255),(83,91,44,255),(190,194,111,255),(226,177,76,255)),
"pal":((60,86,55,255),(31,45,35,255),(91,116,75,255),(145,72,55,255))
}

def raptor(i,pal):
    im=cv(96,64);d=ImageDraw.Draw(im);body,dark,light,accent=pal
    b=[0,1,0,-1,0,1][i%6];a=[0,3,5,3,0,-3][i%6];c=[4,1,-3,-5,-2,2][i%6]
    poly(d,[(12,34+b),(39,25+b),(47,34+b),(18,44+b)],body);ell(d,(32,22+b,67,45+b),body);ell(d,(40,31+b,63,43+b),light,None)
    poly(d,[(60,24+b),(72,18+b),(88,22+b),(86,32+b),(69,33+b)],body);poly(d,[(72,27+b),(87,27+b),(82,34+b),(70,33+b)],dark)
    ell(d,(78,21+b,82,25+b),(245,230,120,255),None);ell(d,(80,22+b,82,24+b),(15,15,15,255),None)
    line(d,[(57,30+b),(66,37+b),(72,36+b)],dark,3);line(d,[(48,41+b),(45,52+a),(38,56+a)],dark,5);line(d,[(60,41+b),(65,51+c),(73,55+c)],dark,5)
    line(d,[(38,56+a),(34,56+a)],accent,2);line(d,[(73,55+c),(78,55+c)],accent,2);line(d,[(37,25+b),(42,31+b)],dark,2);line(d,[(45,24+b),(49,31+b)],dark,2)
    return im

def ptero(i,pal,hunter=False):
    im=cv(112,72);d=ImageDraw.Draw(im);body,dark,light,accent=pal;f=[-8,-2,6,10,6,-2][i%6]
    poly(d,[(48,34),(18,20+f),(6,31+f),(36,44),(50,40)],body);poly(d,[(58,34),(92,18+f),(107,29+f),(72,45),(56,40)],body)
    poly(d,[(18,20+f),(26,38),(36,44),(30,25+f)],light,None);poly(d,[(92,18+f),(83,39),(72,45),(79,24+f)],light,None)
    ell(d,(42,30,69,49),body);poly(d,[(62,32),(78,29),(98,34),(78,40),(61,39)],body);poly(d,[(91,34),(106,37),(92,40)],accent);poly(d,[(76,30),(83,19),(87,32)],dark)
    ell(d,(79,31,83,35),(245,230,120,255),None);line(d,[(52,45),(49,53),(45,56)],dark,3);line(d,[(60,45),(63,53),(67,56)],dark,3)
    if hunter: line(d,[(44,34),(36,30)],accent,2)
    return im

def trike(i,pal):
    im=cv(128,80);d=ImageDraw.Draw(im);body,dark,light,accent=pal;b=[0,1,0,-1,0,1][i%6];a=[1,3,4,2,0,-2][i%6];c=[3,1,-2,-4,-1,2][i%6]
    ell(d,(22,24+b,91,58+b),body);ell(d,(34,39+b,85,58+b),light,None);poly(d,[(24,31+b),(7,36+b),(24,43+b)],body);poly(d,[(83,19+b),(101,18+b),(113,29+b),(108,48+b),(87,50+b),(78,35+b)],dark);ell(d,(87,29+b,116,51+b),body)
    poly(d,[(101,30+b),(120,20+b),(108,35+b)],accent);poly(d,[(96,33+b),(113,38+b),(98,39+b)],accent);poly(d,[(92,29+b),(96,15+b),(100,31+b)],accent);ell(d,(101,32+b,105,36+b),(245,230,120,255),None)
    for x,z in [(38,a),(58,c),(78,a),(90,c)]: line(d,[(x,53+b),(x-2,67+z)],dark,6);line(d,[(x-2,67+z),(x+5,68+z)],accent,2)
    return im

def ankylo(i,pal):
    im=cv(112,64);d=ImageDraw.Draw(im);body,dark,light,accent=pal;b=[0,1,0,-1][i%4];ell(d,(25,27+b,82,51+b),body)
    for x,h in [(33,10),(45,7),(57,9),(69,6)]: poly(d,[(x,29+b),(x+5,18+b-h//2),(x+10,30+b)],dark)
    ell(d,(76,32+b,99,49+b),body);ell(d,(88,35+b,92,39+b),(240,225,120,255),None);line(d,[(28,39+b),(12,43+b)],dark,6);ell(d,(3,38+b,15,49+b),dark)
    for x in [35,58,78]: line(d,[(x,48+b),(x-1,59)],dark,5)
    return im

def plesio(i,pal):
    im=cv(112,64);d=ImageDraw.Draw(im);body,dark,light,accent=pal;w=[0,2,4,2,0,-2][i%6]
    ell(d,(27,28+w,73,49+w),body);line(d,[(65,33+w),(79,22+w),(88,15+w)],body,9);ell(d,(84,10+w,102,24+w),body);ell(d,(93,13+w,97,17+w),(240,225,120,255),None)
    poly(d,[(42,42+w),(28,56+w),(48,49+w)],dark);poly(d,[(63,43+w),(78,56+w),(60,49+w)],dark);poly(d,[(29,34+w),(10,27+w),(21,42+w)],body)
    return im

def nestling(i,pal):
    im=cv(72,56);d=ImageDraw.Draw(im);body,dark,light,accent=pal;b=[0,2,0,-2][i%4]
    ell(d,(22,22+b,52,44+b),body);ell(d,(41,16+b,63,34+b),body);ell(d,(51,20+b,55,24+b),(250,235,120,255),None);poly(d,[(44,18+b),(48,8+b),(52,19+b)],accent)
    line(d,[(30,41+b),(27,51)],dark,4);line(d,[(44,41+b),(47,51)],dark,4)
    return im

def pala(i,pal,roar=False,hurt=False):
    im=cv(192,128);d=ImageDraw.Draw(im);body,dark,light,accent=pal;b=[0,1,0,-1][i%4]
    poly(d,[(18,72+b),(58,50+b),(87,54+b),(64,82+b),(22,89+b)],dark);ell(d,(52,42+b,131,91+b),body);ell(d,(68,62+b,121,90+b),light,None);poly(d,[(118,48+b),(138,31+b),(165,35+b),(180,51+b),(169,69+b),(132,65+b)],body)
    if roar: poly(d,[(157,52+b),(187,56+b),(163,73+b),(145,62+b)],dark);poly(d,[(163,60+b),(182,59+b),(166,68+b)],(165,56,48,255),None)
    else: poly(d,[(158,51+b),(181,55+b),(165,62+b)],dark)
    line(d,[(143,38+b),(158,42+b)],dark,5);ell(d,(153,43+b,159,49+b),(255,203,80,255),None);ell(d,(156,44+b,159,47+b),(20,15,10,255),None)
    for x,h in [(70,16),(84,21),(99,18),(114,15)]: poly(d,[(x,47+b),(x+6,47+b-h),(x+12,48+b)],accent)
    s=[0,4,0,-4][i%4]
    for x,z in [(76,s),(109,-s)]: line(d,[(x,83+b),(x-3,108+z)],dark,10);line(d,[(x-3,108+z),(x+10,111+z)],accent,3)
    line(d,[(128,59+b),(137,71+b),(145,69+b)],dark,5)
    if hurt: line(d,[(160,40),(172,31)],(255,110,70,255),4)
    return im

def save(root,name,items):
    d=root/name;d.mkdir(parents=True,exist_ok=True)
    for fn,img in items: img.save(d/fn)

def generate(root):
    save(root,"raptor",[(f"raptor-run-{i}.png",raptor(i,P["raptor"])) for i in range(6)]+[(f"raptor-idle-{i}.png",raptor(i*3,P["raptor"])) for i in range(2)]+[("raptor-squished.png",raptor(0,P["raptor"]).resize((96,42)))])
    save(root,"alpha_raptor",[(f"alpha-run-{i}.png",raptor(i,P["alpha"])) for i in range(6)]+[(f"alpha-idle-{i}.png",raptor(i*3,P["alpha"])) for i in range(2)]+[("alpha-squished.png",raptor(0,P["alpha"]).resize((96,42)))])
    save(root,"ptero",[(f"ptero-fly-{i}.png",ptero(i,P["ptero"])) for i in range(6)]+[(f"ptero-glide-{i}.png",ptero(i*3+1,P["ptero"])) for i in range(2)])
    save(root,"hunter_ptero",[(f"hunter-fly-{i}.png",ptero(i,P["hunter"],True)) for i in range(6)])
    save(root,"trike",[(f"trike-walk-{i}.png",trike(i,P["trike"])) for i in range(6)]+[(f"trike-idle-{i}.png",trike(i*3,P["trike"])) for i in range(2)])
    save(root,"ankylo",[(f"ankylo-walk-{i}.png",ankylo(i,P["ankylo"])) for i in range(4)])
    save(root,"plesio",[(f"plesio-swim-{i}.png",plesio(i,P["plesio"])) for i in range(6)])
    save(root,"nestling",[(f"nestling-run-{i}.png",nestling(i,P["nestling"])) for i in range(4)])
    save(root,"palaszarusz",[(f"pal-walk-{i}.png",pala(i,P["pal"])) for i in range(4)]+[(f"pal-roar-{i}.png",pala(i,P["pal"],True)) for i in range(3)]+[(f"pal-hurt-{i}.png",pala(i*2+1,P["pal"],hurt=True)) for i in range(2)])

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--output",required=True);a=ap.parse_args();generate(Path(a.output))
