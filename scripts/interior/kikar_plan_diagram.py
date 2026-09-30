# -*- coding: utf-8 -*-
"""Draws the prototype's floor diagram (tower C, floor 30): the plate as the world draws it, the core and its lobby ring
(illustration), the four quarters, apartment A's rooms on the west quarter, the balcony, the fins, and the cameras of the
renders. Output: docs/research/2026-09-30-kikar-hamedina/interiors-proto/plan-floor30-towerC.png (PIL only).
Labels in English (the diagram is a working document, not a sales surface)."""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(REPO, "docs", "research", "2026-09-30-kikar-hamedina", "interiors-proto", "plan-floor30-towerC.png")
N, HALF, AG, CORE, RING = 4.5, 16.3, 15.05, 5.2, 6.8
TH = 31.86 - 1.25 * 29          # floor 30's plate bearing
S = 26                          # px per metre
W, H = 1100, 1100
C = (W / 2, H / 2 + 20)


def P(u, v):
    """plate-local (u along the plate's bearing, v 90 degrees clockwise) -> image, north up"""
    b = math.radians(TH)
    eu = (math.sin(b), math.cos(b))
    ev = (math.sin(b + math.pi / 2), math.cos(b + math.pi / 2))
    x = u * eu[0] + v * ev[0]
    y = u * eu[1] + v * ev[1]
    return (C[0] + x * S, C[1] - y * S)


def outline(half, M=360):
    pts = []
    for k in range(M):
        t = k / M * 2 * math.pi
        c, s = math.cos(t), math.sin(t)
        pts.append((half * math.copysign(abs(c) ** (2 / N), c), half * math.copysign(abs(s) ** (2 / N), s)))
    return pts


def L(s, d):
    """the west apartment's frame (s to the right facing out = plate u; d inward) -> plate (u, v)"""
    return P(s, -(AG - d))


def font(sz):
    for f in ("arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(f, sz)
        except OSError:
            pass
    return ImageFont.load_default()


im = Image.new("RGB", (W, H), (250, 247, 241))
d = ImageDraw.Draw(im)
ink, gold, hair, terra, glass = (27, 26, 23), (156, 122, 60), (200, 192, 178), (194, 86, 58), (120, 160, 170)
d.polygon([P(u, v) for (u, v) in outline(HALF)], fill=(236, 232, 223), outline=hair)
d.line([P(u, v) for (u, v) in outline(AG)] + [P(*outline(AG)[0])], fill=glass, width=3)
d.ellipse([C[0] - RING * S, C[1] - RING * S, C[0] + RING * S, C[1] + RING * S], fill=(228, 222, 210), outline=hair)
d.ellipse([C[0] - CORE * S, C[1] - CORE * S, C[0] + CORE * S, C[1] + CORE * S], fill=(205, 198, 185), outline=ink)
for k in range(4):                      # the party walls on the diagonals
    a = math.radians(45 + 90 * k)
    r0, r1 = RING, 18.2
    d.line([P(r0 * math.cos(a), r0 * math.sin(a)), P(r1 * math.cos(a), r1 * math.sin(a))], fill=ink, width=3)
# apartment A (west quarter): rooms
f = font(15)
fs = font(12)
for (s0, d0, s1, d1) in ((-5.0, 0, -5.0, 7.4), (4.72, 0, 4.72, 7.4), (-5.0, 7.4, 4.72, 7.4), (4.72, 5.2, 9.85, 5.2)):
    d.line([L(s0, d0), L(s1, d1)], fill=ink, width=2)
# balcony
bal = [L(s, 0) for s in (-4.4, 4.4)] + [L(4.4, -1.25), L(-4.4, -1.25)]
d.polygon(bal, fill=(214, 200, 170), outline=gold)
for (txt, s, dd) in (("living · dining · kitchen", -2.3, 1.6), ("master bedroom", 8.3, 1.6), ("bedroom 2 · safe room", -8.4, 2.4),
                     ("hall · baths · storage", -2.0, 8.3), ("balcony 8.8 x 1.25 m", 0.0, -2.0), ("core (5.2 m, illustration)", 0, 15.05)):
    x, y = L(s, dd)
    tw = d.textlength(txt, font=fs)
    d.text((x - tw / 2, y - 7), txt, fill=ink, font=fs)
# fins every 1.5 m (the world's rhythm) on the whole plate
go = outline(AG, 144)
glen = [0.0]
for k in range(1, len(go) + 1):
    glen.append(glen[-1] + math.dist(go[k - 1], go[k % len(go)]))
per = glen[-1]
nfin = int(per / 1.5)
for q in range(nfin):
    sq = (q + 0.5) * per / nfin
    k = next(kk for kk in range(len(go)) if glen[kk + 1] >= sq)
    t = (sq - glen[k]) / (glen[k + 1] - glen[k])
    a, b2 = go[k], go[(k + 1) % len(go)]
    u, v = a[0] + (b2[0] - a[0]) * t, a[1] + (b2[1] - a[1]) * t
    r = math.hypot(u, v)
    d.line([P(u, v), P(u * (r + 0.3) / r, v * (r + 0.3) / r)], fill=ink, width=1)
# cameras
cams = {"living": (-0.35, 7.05, -2), "living (day)": (-4.5, 6.9, 22), "bedroom": (6.2, 4.5, 30), "balcony": (2.6, -0.3, -48),
        "360": (0.35, 3.9, None)}
for nm, (s, dd, yaw) in cams.items():
    x, y = L(s, dd)
    d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=terra)
    if yaw is not None:
        # the direction: out (toward -d) turned by yaw to the right (+s)
        ex, ey = L(s + math.sin(math.radians(yaw)) * 1.6, dd - math.cos(math.radians(yaw)) * 1.6)
        d.line([(x, y), (ex, ey)], fill=terra, width=3)
    d.text((x + 8, y + 4), nm, fill=terra, font=fs)
# north arrow and the facing
d.line([(W - 70, 120), (W - 70, 60)], fill=ink, width=3)
d.polygon([(W - 78, 70), (W - 62, 70), (W - 70, 52)], fill=ink)
d.text((W - 76, 126), "N", fill=ink, font=f)
wx, wy = L(0, -3.2)
d.text((wx - 70, wy - 60), "faces 265.6°", fill=gold, font=f)
title = "Tower C, floor 30 (plate turned to %.2f°): the example apartment's quarter. ILLUSTRATION, not a published plan." % (TH % 360)
d.text((24, 18), title, fill=ink, font=f)
d.text((24, 40), "Glass line = the world's plate (municipal footprint, superellipse n 4.5); fins every 1.5 m; core size not published.", fill=ink, font=fs)
d.text((24, H - 30), "Grid: 1 m = %d px. Party walls on the diagonals: 4 apartments a floor (453 / 117 floors = 3.9)." % S, fill=ink, font=fs)
im.save(OUT)
print("wrote", OUT)
