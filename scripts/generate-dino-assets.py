#!/usr/bin/env python3
from PIL import Image, ImageDraw
from pathlib import Path
import argparse

S=4
def sc(v): return int(round(v*S))
def pts(seq): return [(sc(x),sc(y)) for x,y in seq]
def canvas(w,h): return Image.new("RGBA",(w*S,h*S),(0,0,0,0))
def poly(d,p,fill,outline=(34,37,28,255),width=2):
    d.polygon(pts(p),fill=fill)
    if outline: d.line(pts(p+[p[0]]),fill=outline,width=max(1,sc(width)),joint="curve")
def ell(d,b,fill,outline=(34,37,28,255),width=2):
    d.ellipse(tuple(sc(x) for x in b),fill=fill,outline=outline,width=max(1,sc(width)))
def line(d,p,fill,width=2): d.line(pts(p),fill=fill,width=max(1,sc(width)),joint="curve")
def down(im): return im.resize((im.width//S,im.height//S),Image.Resampling.LANCZOS)
def shadow(d,b,alpha=70): ell(d,b,(10,16,20,alpha),None)
def eye(d,x,y):
    ell(d,(x-3,y-3,x+3,y+3),(247,198,61,255),(38,29,18,255),1)
    ell(d,(x-.8,y-2,x+.8,y+2),(15,14,12,255),None)
def teeth(d,x,y,n=5,dx=4):
    for i in range(n): poly(d,[(x+i*dx,y),(x+2+i*dx,y),(x+1+i*dx,y+4)],(244,231,193,255),(100,81,61,255),.6)
def texture(d,spots,color):
    for x,y,rx,ry in spots: ell(d,(x-rx,y-ry,x+rx,y+ry),color,None)

P={
"raptor":((82,121,65,255),(42,67,37,255),(159,169,104,255),(191,88,48,255)),
"alpha":((132,66,52,255),(72,32,31,255),(186,104,75,255),(229,151,70,255)),
"ptero":((154,113,72,255),(79,57,43,255),(206,159,105,255),(221,177,116,255)),
"hunter":((91,81,101,255),(46,39,56,255),(142,121,145,255),(205,141,82,255)),
"trike":((101,116,68,255),(55,67,42,255),(160,159,98,255),(220,193,137,255)),
"ankylo":((112,96,70,255),(66,56,44,255),(154,133,94,255),(205,180,129,255)),
"plesio":((55,126,137,255),(29,72,80,255),(95,179,177,255),(179,217,190,255)),
"nestling":((145,148,73,255),(77,85,40,255),(194,196,111,255),(225,168,65,255)),
"pal":((61,80,53,255),(28,39,31,255),(100,118,78,255),(139,57,48,255))
}

def raptor(i,pal):
    W,H=160,88; im=canvas(W,H); d=ImageDraw.Draw(im,"RGBA")
    body,dark,light,accent=pal; bob=[0,1.5,3,1.5,0,-1.5][i%6]; a=[-4,0,5,3,-1,-5][i%6]; b=[4,2,-3,-5,-1,4][i%6]
    shadow(d,(30,71,138,79),55)
    poly(d,[(18,48+bob),(56,31+bob),(89,35+bob),(67,51+bob),(25,61+bob)],body)
    ell(d,(49,26+bob,105,61+bob),body); ell(d,(59,39+bob,101,60+bob),light,None)
    poly(d,[(92,30+bob),(112,17+bob),(143,22+bob),(151,32+bob),(139,42+bob),(106,40+bob)],body)
    poly(d,[(113,35+bob),(145,31+bob),(137,44+bob),(109,41+bob)],dark)
    for x,h in [(108,9),(116,13),(124,15),(132,11)]: poly(d,[(x,22+bob),(x+5,22-h+bob),(x+8,24+bob)],accent,(58,45,28,255),1)
    line(d,[(114,34+bob),(139,34+bob)],(53,34,28,255),2); teeth(d,116,34+bob,5,4); eye(d,129,25+bob)
    line(d,[(99,40+bob),(108,50+bob),(116,48+bob)],dark,5)
    line(d,[(68,56+bob),(62,71+a),(49,77+a)],dark,8); line(d,[(91,56+bob),(99,69+b),(115,75+b)],dark,8)
    line(d,[(49,77+a),(41,77+a)],accent,2); line(d,[(115,75+b),(124,75+b)],accent,2)
    for x in [49,58,69,80,91]: line(d,[(x,29+bob),(x+6,40+bob)],dark,2)
    texture(d,[(66,46,4,2),(80,47,5,2),(96,43,3,2)],(49,83,42,90))
    return down(im)

def ptero(i,pal):
    W,H=184,104; im=canvas(W,H); d=ImageDraw.Draw(im,"RGBA"); body,dark,light,accent=pal; flap=[-15,-7,2,10,2,-7][i%6]
    shadow(d,(42,84,145,91),40)
    poly(d,[(78,51),(31,22+flap),(9,34+flap),(55,68),(83,61)],body); poly(d,[(95,50),(143,18+flap),(176,31+flap),(123,68),(92,61)],body)
    poly(d,[(35,27+flap),(53,60),(71,57),(51,34+flap)],light,(73,57,46,255),1)
    poly(d,[(140,24+flap),(125,61),(108,58),(125,31+flap)],light,(73,57,46,255),1)
    ell(d,(70,46,105,69),body); poly(d,[(98,49),(121,40),(153,48),(124,58),(98,58)],body)
    poly(d,[(145,48),(177,51),(149,57)],accent); poly(d,[(119,42),(128,25),(133,45)],dark); eye(d,130,46)
    line(d,[(80,66),(75,79),(68,83)],dark,4); line(d,[(92,66),(98,78),(105,82)],dark,4)
    return down(im)

def trike(i,pal):
    W,H=206,116; im=canvas(W,H); d=ImageDraw.Draw(im,"RGBA"); body,dark,light,accent=pal
    bob=[0,1.5,2,0,-1.5,-1][i%6]; a=[-3,0,4,2,-2,-4][i%6]; b=[3,1,-3,-4,0,4][i%6]
    shadow(d,(28,94,188,104),65); ell(d,(31,39+bob,139,87+bob),body); ell(d,(47,60+bob,130,86+bob),light,None)
    poly(d,[(33,51+bob),(8,61+bob),(34,67+bob)],body)
    poly(d,[(130,31+bob),(159,28+bob),(184,48+bob),(176,78+bob),(139,79+bob),(121,57+bob)],dark)
    ell(d,(139,48+bob,188,79+bob),body)
    poly(d,[(164,50+bob),(199,34+bob),(176,57+bob)],accent,(92,74,54,255),1)
    poly(d,[(153,57+bob),(185,65+bob),(157,66+bob)],accent,(92,74,54,255),1)
    poly(d,[(149,48+bob),(153,23+bob),(160,51+bob)],accent,(92,74,54,255),1); eye(d,170,55+bob)
    for x,z in [(56,a),(86,b),(116,a),(139,b)]: line(d,[(x,81+bob),(x-2,100+z)],dark,10)
    return down(im)

def ankylo(i,pal):
    W,H=170,88; im=canvas(W,H); d=ImageDraw.Draw(im,"RGBA"); body,dark,light,accent=pal; bob=[0,1.5,0,-1.5][i%4]
    shadow(d,(22,72,150,80),55); ell(d,(37,35+bob,126,69+bob),body); ell(d,(50,50+bob,120,68+bob),light,None)
    for x,h in [(48,11),(62,14),(78,12),(95,15),(111,11)]: poly(d,[(x,39+bob),(x+5,39-h+bob),(x+11,41+bob)],dark)
    ell(d,(119,46+bob,151,68+bob),body); eye(d,140,51+bob); line(d,[(38,53+bob),(18,60+bob)],dark,8); ell(d,(5,53+bob,21,69+bob),dark)
    for x in [53,83,112,133]: line(d,[(x,65+bob),(x-2,78)],dark,7)
    return down(im)

def plesio(i,pal):
    W,H=178,94; im=canvas(W,H); d=ImageDraw.Draw(im,"RGBA"); body,dark,light,accent=pal; w=[0,2,4,2,0,-2][i%6]
    ell(d,(37,43+w,113,70+w),body); ell(d,(52,54+w,106,69+w),light,None)
    line(d,[(104,49+w),(126,31+w),(139,18+w)],body,14); ell(d,(132,12+w,158,30+w),body); eye(d,148,18+w)
    poly(d,[(60,63+w),(39,82+w),(71,70+w)],dark); poly(d,[(97,62+w),(120,81+w),(93,70+w)],dark); poly(d,[(39,49+w),(12,39+w),(27,61+w)],body)
    return down(im)

def nestling(i,pal):
    W,H=112,74; im=canvas(W,H); d=ImageDraw.Draw(im,"RGBA"); body,dark,light,accent=pal; b=[0,2,0,-2][i%4]
    shadow(d,(20,61,94,67),45); ell(d,(31,28+b,74,56+b),body); ell(d,(65,22+b,97,45+b),body); eye(d,86,28+b)
    poly(d,[(70,23+b),(77,10+b),(83,25+b)],accent); poly(d,[(32,37+b),(13,43+b),(33,50+b)],body)
    line(d,[(43,53+b),(39,66)],dark,6); line(d,[(66,53+b),(70,66)],dark,6)
    return down(im)

def pala(i,pal,roar=False,hurt=False):
    W,H=286,164; im=canvas(W,H); d=ImageDraw.Draw(im,"RGBA"); body,dark,light,accent=pal; b=[0,2,0,-2][i%4]
    shadow(d,(33,137,252,151),75); poly(d,[(27,88+b),(88,57+b),(141,63+b),(105,101+b),(35,112+b)],dark)
    ell(d,(82,53+b,195,116+b),body); ell(d,(104,83+b,181,115+b),light,None)
    poly(d,[(177,61+b),(208,34+b),(251,41+b),(274,67+b),(254,91+b),(198,84+b)],body)
    for x,h in [(106,20),(124,28),(144,24),(165,18),(190,14)]: poly(d,[(x,59+b),(x+7,59-h+b),(x+14,61+b)],accent,(55,40,34,255),1)
    if roar:
        poly(d,[(240,66+b),(282,72+b),(245,99+b),(217,82+b)],dark); poly(d,[(246,78+b),(276,75+b),(250,91+b)],(164,61,50,255),None); teeth(d,238,67+b,7,5)
    else:
        poly(d,[(239,66+b),(277,71+b),(249,82+b)],dark); teeth(d,241,68+b,6,5)
    eye(d,237,54+b); line(d,[(199,79+b),(212,96+b),(225,92+b)],dark,7)
    st=[-3,2,4,-2][i%4]
    for x,z in [(116,st),(164,-st)]: line(d,[(x,108+b),(x-5,140+z)],dark,15)
    if hurt: line(d,[(252,47),(268,33)],(255,113,72,255),5)
    return down(im)

def save(root,name,items):
    d=root/name; d.mkdir(parents=True,exist_ok=True)
    for fn,img in items: img.save(d/fn,optimize=True)

def generate(root):
    save(root,"raptor",[(f"raptor-run-{i}.png",raptor(i,P["raptor"])) for i in range(6)]+[(f"raptor-idle-{i}.png",raptor(i*3,P["raptor"])) for i in range(2)]+[("raptor-squished.png",raptor(0,P["raptor"]).resize((160,46),Image.Resampling.LANCZOS))])
    save(root,"alpha_raptor",[(f"alpha-run-{i}.png",raptor(i,P["alpha"])) for i in range(6)]+[(f"alpha-idle-{i}.png",raptor(i*3,P["alpha"])) for i in range(2)]+[("alpha-squished.png",raptor(0,P["alpha"]).resize((160,46),Image.Resampling.LANCZOS))])
    save(root,"ptero",[(f"ptero-fly-{i}.png",ptero(i,P["ptero"])) for i in range(6)]+[(f"ptero-glide-{i}.png",ptero(i*3+1,P["ptero"])) for i in range(2)])
    save(root,"hunter_ptero",[(f"hunter-fly-{i}.png",ptero(i,P["hunter"])) for i in range(6)])
    save(root,"trike",[(f"trike-walk-{i}.png",trike(i,P["trike"])) for i in range(6)]+[(f"trike-idle-{i}.png",trike(i*3,P["trike"])) for i in range(2)])
    save(root,"ankylo",[(f"ankylo-walk-{i}.png",ankylo(i,P["ankylo"])) for i in range(4)])
    save(root,"plesio",[(f"plesio-swim-{i}.png",plesio(i,P["plesio"])) for i in range(6)])
    save(root,"nestling",[(f"nestling-run-{i}.png",nestling(i,P["nestling"])) for i in range(4)])
    save(root,"palaszarusz",[(f"pal-walk-{i}.png",pala(i,P["pal"])) for i in range(4)]+[(f"pal-roar-{i}.png",pala(i,P["pal"],True)) for i in range(3)]+[(f"pal-hurt-{i}.png",pala(i*2+1,P["pal"],False,True)) for i in range(2)])

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--output",required=True); a=ap.parse_args(); generate(Path(a.output))
