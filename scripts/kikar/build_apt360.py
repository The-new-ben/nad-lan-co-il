# -*- coding: utf-8 -*-
"""The living room in 360 from every Kikar apartment, for the web (HAD-710, 11.11.2026): reads the Blender renders of
scripts/interior/render_kikar_360s.py (docs/research/2026-11-10-kikar-showcase/living360/<T><f>-<s>.jpg, a day render whose
room is dark next to the bright window) and writes, per picture:
  assets/project-stage/hamedina/apt/<T><f>-<s>.webp       2048x1024 equirectangular, for the cockpit's 360 viewer
  assets/project-stage/hamedina/apt/<T><f>-<s>-card.webp  480x320, the middle of the room and its window, for the tile
The light: one exposure per picture in linear light (like opening the camera's aperture), chosen so the room band averages
the same brightness as the existing C30 living room 360, with a soft shoulder so the window keeps its view. No other edit.
Every picture stays "הדמיה להמחשה".
  python scripts/kikar/build_apt360.py
"""
import json
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(REPO, "docs", "research", "2026-11-10-kikar-showcase", "living360")
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "hamedina", "apt")
TARGET, KMAX, SHOULDER = 118.0, 4.0, 0.72
os.makedirs(OUT, exist_ok=True)


def s2l(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def l2s(x):
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * np.power(np.clip(x, 0, None), 1 / 2.4) - 0.055)


def tone(a, k):
    lin = s2l(a) * k
    lin = np.where(lin > SHOULDER, SHOULDER + (1 - SHOULDER) * (1 - np.exp(-(lin - SHOULDER) / (1 - SHOULDER))), lin)
    return np.clip(l2s(lin), 0, 1)


def exposure(a):
    band = a[300:1000]  # the room between the ceiling and the floor
    lo, hi = 1.0, KMAX
    for _ in range(18):
        k = (lo + hi) / 2
        m = float((tone(band, k) @ np.array([0.299, 0.587, 0.114], dtype=np.float32)).mean() * 255)
        lo, hi = (k, hi) if m < TARGET else (lo, k)
    return (lo + hi) / 2


idx = json.load(open(os.path.join(SRC, "index.json"), encoding="utf-8"))
log = {}
for name in sorted(idx):
    im = Image.open(os.path.join(SRC, name + ".jpg")).convert("RGB")
    assert im.size == (2048, 1024), (name, im.size)
    a = np.asarray(im, dtype=np.float32) / 255
    k = exposure(a)
    out = Image.fromarray((tone(a, k) * 255 + 0.5).astype(np.uint8))
    out.save(os.path.join(OUT, name + ".webp"), "WEBP", quality=80, method=6)
    out.crop((560, 300, 1488, 919)).resize((480, 320), Image.LANCZOS).save(os.path.join(OUT, name + "-card.webp"), "WEBP", quality=78, method=6)
    log[name] = round(k, 2)
    print(name, "exposure x%.2f" % k, os.path.getsize(os.path.join(OUT, name + ".webp")) // 1024, "KB")
tot = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
print("wrote", len(log), "pictures + cards into", OUT, "|", tot // 1024, "KB in all")
