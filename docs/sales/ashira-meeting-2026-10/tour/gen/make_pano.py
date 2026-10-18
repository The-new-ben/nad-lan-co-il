# -*- coding: utf-8 -*-
"""HAD-543: turn a generated facility view (1536x1024, ~90 deg wide) into a seamless 2:1 panorama for the tour viewer.
The view is reprojected (perspective -> equirect) into four 90-degree tiles, every other one mirrored, so each seam meets
itself; ceiling and floor beyond the frame fade into a soft blur of the frame's edge rows.
python make_pano.py pool spa ...  -> out/fac-<name>.jpg (4096x2048), -2k (2048x1024), -card (1200x675, from the view itself)"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter
H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, "out"); os.makedirs(OUT, exist_ok=True)
HFOV = 90.0

def bilinear(img, x, y):
    h, w = img.shape[:2]
    x = np.clip(x, 0, w - 1.001); y = np.clip(y, 0, h - 1.001)
    x0 = np.floor(x).astype(np.int32); y0 = np.floor(y).astype(np.int32)
    fx = (x - x0)[..., None]; fy = (y - y0)[..., None]
    a = img[y0, x0]; b = img[y0, x0 + 1]; c = img[y0 + 1, x0]; d = img[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy

def pano(src, W=4096):
    im = Image.open(src).convert("RGB")
    sw, sh = im.size
    sharp = np.asarray(im, dtype=np.float32)
    soft = np.asarray(im.filter(ImageFilter.GaussianBlur(40)), dtype=np.float32)
    Hh = W // 2
    lon = (np.arange(W) + 0.5) / W * 2 * np.pi - np.pi          # u = 0.5 -> lon 0 (yaw 0 looks at the centre)
    lat = np.pi / 2 - (np.arange(Hh) + 0.5) / Hh * np.pi
    LON, LAT = np.meshgrid(lon, lat)
    t = np.radians(HFOV)
    k = np.floor((LON + t / 2) / t)
    l = LON - k * t
    l = np.where(np.mod(k, 2) == 1, -l, l)                       # mirror every other tile
    f = (sw / 2) / np.tan(t / 2)
    dz = np.cos(LAT) * np.cos(l)
    x = sw / 2 + f * np.cos(LAT) * np.sin(l) / dz
    y = sh / 2 - f * np.sin(LAT) / dz
    over = np.maximum(0, np.maximum(-y, y - (sh - 1)))           # pixels beyond the frame (ceiling / floor)
    w = np.clip(over / (sh * 0.35), 0, 1)[..., None]
    w = w * w * (3 - 2 * w)
    a = bilinear(sharp, x, y); b = bilinear(soft, x, y)
    edge_blend = np.clip(over / 24.0, 0, 1)[..., None]           # a short ramp so the frame edge is not a hard line
    out = a * (1 - edge_blend) + (a * (1 - w) + b * w) * edge_blend
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), im

for name in sys.argv[1:]:
    p, view = pano(os.path.join(H, name + ".png"))
    base = os.path.join(OUT, "fac-" + name)
    p.save(base + ".jpg", quality=86, optimize=True, progressive=True)
    p.resize((2048, 1024), Image.LANCZOS).save(base + "-2k.jpg", quality=84, optimize=True, progressive=True)
    vw, vh = view.size; ch = int(vw * 9 / 16); top = (vh - ch) // 2
    view.crop((0, top, vw, top + ch)).resize((1200, 675), Image.LANCZOS).save(base + "-card.jpg", quality=84, optimize=True, progressive=True)
    print(name, [os.path.getsize(base + s + ".jpg") for s in ("", "-2k", "-card")])
