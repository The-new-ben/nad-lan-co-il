# -*- coding: utf-8 -*-
"""HAD-543 (Ben 19.10: ChatGPT quality only): the floor-25 living-room 360s from pano-*.png -> the plugin's file set
(4096 master, -2k, -card 1200x675 and -thumb 240x135 rectilinear from the panorama's centre), seam blended."""
import os, numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(H, *[".."] * 6, "plugins", "nadlan-config", "assets", "project-stage", "ashira", "tour")
def seam(a):
    L, R = a[:, 0].copy(), a[:, -1].copy(); m = (L + R) / 2
    for i in range(32):
        w = (1 - i / 32) ** 2; a[:, i] += (m - L) * w; a[:, -1 - i] += (m - R) * w
    return a
def rect(eq, W, Hh, hfov=100.0):
    e = np.asarray(eq, dtype=np.float32); eh, ew = e.shape[:2]
    f = (W / 2) / np.tan(np.radians(hfov) / 2)
    x, y = np.meshgrid(np.arange(W) - W / 2 + 0.5, np.arange(Hh) - Hh / 2 + 0.5)
    lon = np.arctan2(x, f); lat = np.arctan2(-y, np.sqrt(x * x + f * f))
    u = ((lon / (2 * np.pi)) + 0.5) * ew; v = (0.5 - lat / np.pi) * eh
    u0 = np.clip(u.astype(int), 0, ew - 1); v0 = np.clip(v.astype(int), 0, eh - 1)
    return Image.fromarray(e[v0, u0].astype(np.uint8))
def save(im, o, thumb):
    big = im.resize((4096, 2048), Image.LANCZOS)
    card = rect(big, 2400, 1350, 110).resize((1200, 675), Image.LANCZOS)
    big.save(os.path.join(T, o + ".jpg"), quality=88, optimize=True, progressive=True)
    im.save(os.path.join(T, o + "-2k.jpg"), quality=85, optimize=True, progressive=True)
    card.save(os.path.join(T, o + "-card.jpg"), quality=85, optimize=True, progressive=True)
    if thumb:
        card.resize((240, 135), Image.LANCZOS).save(os.path.join(T, thumb), quality=85)
def load(name):
    a = seam(np.asarray(Image.open(os.path.join(H, name)).convert("RGB"), dtype=np.float32))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
# the base picture is the room AS DELIVERED (empty), the page's own words; the furnished look is the "warm" style
ROOMS = ["living-25w", "living-25n", "living-25e", "living-25s", "living-10w", "living-10n", "living-10e", "living-10s", "balcony-25w", "balcony-10w"]
for r in ROOMS:
    empty = load("pano-living-25w-bare-2048x1024.png" if r == "living-25w" else f"pano-{r}-src-2048x1024.png")
    save(empty, r, r + "-bare-thumb.jpg")
    save(load(f"pano-{r}-2048x1024.png"), r + "-warm", r + "-warm-thumb.jpg")
    print(r)
for st in ("light", "stone"):
    save(load(f"pano-living-25w-{st}-2048x1024.png"), "living-25w-" + st, "living-25w-" + st + "-thumb.jpg")
