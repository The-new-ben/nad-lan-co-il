# -*- coding: utf-8 -*-
"""The data of Kikar's showroom stage (HAD-712, 11.11.2026): each tower turned through a circle, and the map under the model.
  1. scripts/interior/_renders/kikar/turn/t-<T>-<nn>.png (kikar_turntable.py) -> assets/project-stage/hamedina/turn/<T>-<nn>.webp
  2. the three t-<T>.json files -> turn/turn.json: per tower and frame the camera's bearing and each floor's band on the picture
     [left x, left y, right x, right y] in thousandths of the picture (x right, y down)
  3. turn/map.webp: the square and its surroundings from world.json (the municipality's open data, as the world draws it), north up,
     from 2,150 m west of the plot's centre (the sea) to 650 m east; turn/turn.json carries its extent, so the page draws the towers
     and the beam over it.
  python scripts/kikar/build_showroom_data.py"""
import base64
import json
import os
import struct

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
HAM = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "hamedina")
SRC = os.path.join(REPO, "scripts", "interior", "_renders", "kikar", "turn")
OUT = os.path.join(HAM, "turn")
os.makedirs(OUT, exist_ok=True)
W = json.load(open(os.path.join(HAM, "world.json"), encoding="utf-8"))


def ints(x):
    if isinstance(x, str):
        raw = base64.b64decode(x)
        return struct.unpack("<%dh" % (len(raw) // 2), raw)
    return x


def unpack(arr, off, n, q):
    x = z = 0
    P = []
    for i in range(n):
        x += arr[off + 2 * i]
        z += arr[off + 2 * i + 1]
        P.append((x * q, -z * q))  # X east, Y north, metres from the plot's centre
    return P


# ------------------------------------------------------------------ 1 + 2: the frames and their floor bands
towers = {}
total = 0
for k in "ABC":
    jp = os.path.join(SRC, "t-%s.json" % k)
    if not os.path.exists(jp):
        continue
    d = json.load(open(jp))
    frames, have = [], 0
    for f in d["frames"]:
        png = os.path.join(SRC, f["file"])
        webp = os.path.join(OUT, "%s-%02d.webp" % (k, f["i"]))
        if os.path.exists(png) and (not os.path.exists(webp) or os.path.getmtime(webp) < os.path.getmtime(png)):
            Image.open(png).convert("RGB").save(webp, "WEBP", quality=78, method=6)
        if os.path.exists(webp):
            have += 1
            total += os.path.getsize(webp)
        frames.append({"b": f["bearing"], "ok": 1 if os.path.exists(webp) else 0,
                       "f": [[round(v * 1000) for v in row[:4]] for row in f["floors"]]})
    towers[k] = {"floors": d["floors"], "base": d["base_bearing"], "frames": frames, "have": have}
    size, twist, tdir = d["size"], d["twist"], d["twist_dir"]
    print("tower %s: %d of %d frames" % (k, have, len(frames)))

# ------------------------------------------------------------------ 3: the map under the model
X0, X1, Y0, Y1, S = -2150.0, 650.0, -474.0, 474.0, 2  # metres; 2 picture pixels per CSS pixel at 390 wide
PW, PH = 390 * S, 132 * S
kx, ky = PW / (X1 - X0), PH / (Y1 - Y0)


def px(p):
    return ((p[0] - X0) * kx, (Y1 - p[1]) * ky)


im = Image.new("RGB", (PW, PH), (230, 237, 240))
dr = ImageDraw.Draw(im)
for w in W["water"]["rings"]:
    P = unpack(w["p"], 0, len(w["p"]) // 2, W["water"]["q"])
    if len(P) > 2:
        dr.polygon([px(p) for p in P], fill=(159, 198, 214))
G = ints(W["greens"]["data"])
o = 0
while o < len(G):
    n = G[o]
    P = unpack(G, o + 3, n, W["greens"]["q"])
    o += 3 + 2 * n
    if len(P) > 2:
        dr.polygon([px(p) for p in P], fill=(207, 224, 201))
A = ints(W["blocks"]["data"])
bq, bqf = W["blocks"]["q"], W["blocks"].get("q_far", W["blocks"]["q"])
o = 0
while o < len(A):
    n, flags = A[o], A[o + 4] & 0xFFFF
    P = unpack(A, o + 5, n, bqf if flags & 256 else bq)
    o += 5 + 2 * n
    if len(P) > 2 and X0 - 50 < P[0][0] < X1 + 50 and Y0 - 50 < P[0][1] < Y1 + 50:
        dr.polygon([px(p) for p in P], fill=(205, 214, 220))
Sx = ints(W["streets"]["data"])
o = 0
while o < len(Sx):
    n, w = Sx[o], Sx[o + 1]
    P = unpack(Sx, o + 4, n, W["streets"]["q"])
    o += 4 + 2 * n
    if len(P) > 1:
        dr.line([px(p) for p in P], fill=(255, 255, 255), width=max(2, int(round(w * kx * 0.9))))
if W.get("park"):
    P = unpack(W["park"]["p"], 0, len(W["park"]["p"]) // 2, W["park"]["q"])
    dr.polygon([px(p) for p in P], fill=(190, 219, 184))
if W.get("pond"):
    P = unpack(W["pond"]["p"], 0, len(W["pond"]["p"]) // 2, W["pond"]["q"])
    dr.polygon([px(p) for p in P], fill=(159, 198, 214))
im.save(os.path.join(OUT, "map.webp"), "WEBP", quality=82, method=6)

json.dump({"about": "Kikar's showroom stage: per tower and frame the camera's bearing (b) and each floor's band [left x, left y, right x, "
                    "right y] in thousandths of the picture; map = the extent of map.webp in metres from the plot's centre (X east, Y north) "
                    "(scripts/kikar/build_showroom_data.py)",
           "size": size, "twist": twist, "twist_dir": tdir, "fh": W["model"]["fh"],
           "map": {"x0": X0, "x1": X1, "y0": Y0, "y1": Y1, "towers": {t["key"]: [t["cx"], -t["cz"], t["side"]] for t in W["towers"]}},
           "towers": towers},
          open(os.path.join(OUT, "turn.json"), "w", encoding="utf-8", newline="\n"), separators=(",", ":"))
print("turn.json", os.path.getsize(os.path.join(OUT, "turn.json")) // 1024, "KB | map.webp", os.path.getsize(os.path.join(OUT, "map.webp")) // 1024,
      "KB | frames", total // 1024, "KB")
