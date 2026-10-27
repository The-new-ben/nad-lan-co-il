# -*- coding: utf-8 -*-
"""Side-by-side + edge overlay of a render and its AI pass.  python compare.py <orig> <ai> <out-side-by-side> <out-edges> "label A" "label B"
Edge overlay: original edges in teal, AI edges in orange; where they coincide they read dark. Prints the mean edge offset."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
a0, b0, out, out2, la, lb = sys.argv[1:7]
A = Image.open(a0).convert("RGB"); B = Image.open(b0).convert("RGB")
w = 1200; h = int(w * A.height / A.width)
A = A.resize((w, h), Image.LANCZOS); B = B.resize((w, h), Image.LANCZOS)
try:
    f = ImageFont.truetype("arial.ttf", 26)
except Exception:
    f = None
S = Image.new("RGB", (w * 2 + 30, h + 60), "white"); S.paste(A, (0, 60)); S.paste(B, (w + 30, 60))
d = ImageDraw.Draw(S); d.text((10, 16), la, fill=(20, 33, 43), font=f); d.text((w + 40, 16), lb, fill=(20, 33, 43), font=f)
S.save(out)
ea = np.asarray(A.convert("L").filter(ImageFilter.FIND_EDGES)) > 40
eb = np.asarray(B.convert("L").filter(ImageFilter.FIND_EDGES)) > 40
O = np.full((h, w, 3), 255, np.uint8)
O[ea] = (31, 120, 140); O[eb] = (230, 120, 30); O[ea & eb] = (20, 33, 43)
Image.fromarray(O).save(out2)
# distance from each AI edge pixel to the nearest original edge (chamfer, coarse)
from math import inf
ya, xa = np.nonzero(ea); yb, xb = np.nonzero(eb)
grid = np.full((h, w), 99, np.int32)
grid[ea] = 0
for _ in range(12):
    g = grid.copy()
    g[1:, :] = np.minimum(g[1:, :], grid[:-1, :] + 1); g[:-1, :] = np.minimum(g[:-1, :], grid[1:, :] + 1)
    g[:, 1:] = np.minimum(g[:, 1:], grid[:, :-1] + 1); g[:, :-1] = np.minimum(g[:, :-1], grid[:, 1:] + 1)
    grid = g
dist = grid[eb]
print("AI edge px within 3px of an original edge: %.1f%%, within 8px: %.1f%%, median %d px (image width %d)" % ((dist <= 3).mean() * 100, (dist <= 8).mean() * 100, np.median(dist), w))
