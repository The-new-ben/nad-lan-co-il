import sys
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS=None
src=r"C:/Users/777/nad-lan/nad-lan-co-il/docs/sales/kochav-ph/plan/plan-raw-0.jpeg"
x0,y0,x1,y1=map(int,sys.argv[1:5]); sc=float(sys.argv[5]); step=int(sys.argv[6]); out=sys.argv[7]
im=Image.open(src).convert("RGB").crop((x0,y0,x1,y1))
im=im.resize((int((x1-x0)*sc),int((y1-y0)*sc)),Image.LANCZOS)
d=ImageDraw.Draw(im,"RGBA")
try: f=ImageFont.truetype("arial.ttf",11)
except: f=None
for gx in range((x0//step+1)*step,x1,step):
    X=(gx-x0)*sc; d.line([(X,0),(X,im.height)],fill=(255,0,0,70) if gx%(step*5) else (255,0,0,150),width=1)
    d.text((X+2,2),str(gx),fill=(200,0,0),font=f)
for gy in range((y0//step+1)*step,y1,step):
    Y=(gy-y0)*sc; d.line([(0,Y),(im.width,Y)],fill=(0,0,255,70) if gy%(step*5) else (0,0,255,150),width=1)
    d.text((2,Y+2),str(gy),fill=(0,0,200),font=f)
im.save(out); print(im.size)
