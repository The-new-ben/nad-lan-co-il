# render the raster in rotated (s=x+y, d=x-y) space: horizontal axis = s (D1 lines x+y=c are vertical), vertical axis = d increasing DOWN? we put d increasing upward? -> keep d increasing downward.
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS=None
src=r"C:/Users/777/nad-lan/nad-lan-co-il/docs/sales/kochav-ph/plan/plan-raw-0.jpeg"
s0,s1,d0,d1=map(float,sys.argv[1:5]); sc=float(sys.argv[5]); step=int(sys.argv[6]); out=sys.argv[7]
A=np.asarray(Image.open(src).convert("L"),dtype=np.float32)
H,W=A.shape
# output pixel spacing in s-units: 1 orig px perpendicular = sqrt2 s-units; out px = 1/sc orig px
ds=np.sqrt(2)/sc
ns=int((s1-s0)/ds); nd=int((d1-d0)/ds)
S=s0+np.arange(ns)*ds; D=d1-np.arange(nd)*ds
SS,DD=np.meshgrid(S,D)
X=(SS+DD)/2; Y=(SS-DD)/2
xi=np.clip(np.round(X).astype(int),0,W-1); yi=np.clip(np.round(Y).astype(int),0,H-1)
O=A[yi,xi]; O[(X<0)|(X>=W)|(Y<0)|(Y>=H)]=200
im=Image.fromarray(O.astype(np.uint8)).convert("RGB"); d=ImageDraw.Draw(im,"RGBA")
try: f=ImageFont.truetype("arial.ttf",11)
except: f=None
for g in range(int(s0//step+1)*step,int(s1),step):
    P=(g-s0)/ds; d.line([(P,0),(P,nd)],fill=(255,0,0,80 if g%(step*5) else 160)); d.text((P+2,2),str(g),fill=(200,0,0),font=f)
for g in range(int(d0//step+1)*step,int(d1),step):
    P=(d1-g)/ds; d.line([(0,P),(ns,P)],fill=(0,0,255,80 if g%(step*5) else 160)); d.text((2,P+2),str(g),fill=(0,0,200),font=f)
im.save(out); print(im.size)
