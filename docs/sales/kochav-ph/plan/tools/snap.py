# usage: snap.py ORIENT c t0 t1 [R]
# ORIENT: H (y=c, t=x), V (x=c, t=y), D1 (x+y=c, t=d=x-y), D2 (x-y=c, t=s=x+y)
import sys, numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
A=255-np.asarray(Image.open(r"C:/Users/777/nad-lan/nad-lan-co-il/docs/sales/kochav-ph/plan/plan-raw-0.jpeg").convert("L"),dtype=np.float32)
H,W=A.shape
def samp(xs,ys):
    xi=np.clip(np.round(xs).astype(int),0,W-1); yi=np.clip(np.round(ys).astype(int),0,H-1); return A[yi,xi]
def prof(o,c,t0,t1,R=40):
    out=[]
    for off in np.arange(-R,R+0.5,1 if o in("H","V") else 1):
        cc=c+off
        t=np.arange(t0,t1,1.0)
        if o=="H": xs,ys=t,np.full_like(t,cc)
        elif o=="V": xs,ys=np.full_like(t,cc),t
        elif o=="D1": xs,ys=(cc+t)/2,(cc-t)/2
        else: xs,ys=(t+cc)/2,(t-cc)/2
        v=samp(xs,ys); out.append((cc,(v>110).mean()))
    return out
o=sys.argv[1]; c=float(sys.argv[2]); t0=float(sys.argv[3]); t1=float(sys.argv[4]); R=float(sys.argv[5]) if len(sys.argv)>5 else 40
p=prof(o,c,t0,t1,R)
vals=[v for _,v in p]
peaks=[(cc,round(v,2)) for i,(cc,v) in enumerate(p) if v>0.35 and (i==0 or v>=vals[i-1]) and (i==len(p)-1 or v>=vals[i+1])]
print(o,c,"[",t0,t1,"] peaks:",peaks)
