# -*- coding: utf-8 -*-
"""Cuts a Cycles 360° panorama for the web (design system ApartmentTour): the full picture as JPG (4096 and 2048 wide),
and the card's picture, a straight (rectilinear) view through the window, 1200 x 675.
PIL only, no numpy (the card is reprojected pixel by pixel from the panorama, with bilinear sampling).
  python scripts/interior/cut_tour.py <panorama.png> <out folder> <name> [yaw_deg pitch_deg hfov_deg]"""
import math, os, sys

from PIL import Image

src, out_dir, name = sys.argv[1], sys.argv[2], sys.argv[3]
YAW = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0      # 0 = the panorama's centre (the window)
PITCH = float(sys.argv[5]) if len(sys.argv) > 5 else -4.0   # a little down: the horizon sits in the upper half
HFOV = float(sys.argv[6]) if len(sys.argv) > 6 else 84.0
os.makedirs(out_dir, exist_ok=True)

pano = Image.open(src).convert("RGB")
W, H = pano.size
pano.save(os.path.join(out_dir, name + ".jpg"), "JPEG", quality=82, optimize=True, progressive=True)
pano.resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(out_dir, name + "-2k.jpg"), "JPEG", quality=82, optimize=True, progressive=True)

# the card: a pinhole view out of the panorama
CW, CH = 1200, 675
f = (CW / 2) / math.tan(math.radians(HFOV) / 2)
yaw, pitch = math.radians(YAW), math.radians(PITCH)
cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)
px = pano.load()
card = Image.new("RGB", (CW, CH))
cd = card.load()


def sample(u, v):
    x = u * W - 0.5
    y = v * H - 0.5
    x0 = int(math.floor(x))
    y0 = int(math.floor(y))
    fx, fy = x - x0, y - y0
    y0 = min(max(y0, 0), H - 1)
    y1 = min(y0 + 1, H - 1)
    x0m, x1m = x0 % W, (x0 + 1) % W
    a, b, c, d = px[x0m, y0], px[x1m, y0], px[x0m, y1], px[x1m, y1]
    return tuple(int(a[k] * (1 - fx) * (1 - fy) + b[k] * fx * (1 - fy) + c[k] * (1 - fx) * fy + d[k] * fx * fy + 0.5) for k in range(3))


for j in range(CH):
    yv = (CH / 2 - j - 0.5)
    for i in range(CW):
        xv = (i + 0.5 - CW / 2)
        # camera ray: forward = the panorama's centre, right = +x, up = +y; pitch about the right axis, then yaw
        dx, dy, dz = xv, yv, f
        dy, dz = dy * cp + dz * sp, -dy * sp + dz * cp
        dx, dz = dx * cy + dz * sy, -dx * sy + dz * cy
        lon = math.atan2(dx, dz)                       # 0 at the centre, positive to the right
        lat = math.atan2(dy, math.hypot(dx, dz))
        cd[i, j] = sample(0.5 + lon / (2 * math.pi), 0.5 - lat / math.pi)
card.save(os.path.join(out_dir, name + "-card.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
for fn in (name + ".jpg", name + "-2k.jpg", name + "-card.jpg"):
    p = os.path.join(out_dir, fn)
    print(fn, os.path.getsize(p), "bytes")
