# -*- coding: utf-8 -*-
"""The map of Greece for the price-list tools (HAD-592, Ben 22.10.2026: "the most comprehensive Greece price list ... infographics,
tools, something new"). Source: Natural Earth 1:10m country shapes, public domain, via world-atlas@2.0.2 (countries-10m.json,
TopoJSON). Decodes Greece and its neighbours (Albania, North Macedonia, Bulgaria, Turkey), projects them (equirectangular with
cos(38.5°)), simplifies (Douglas-Peucker) and writes plugins/nadlan-config/assets/instruments/data/greece-map.json:
{"vb": [w, h], "proj": {...}, "gr": "<svg path>", "nb": "<svg path>"}. The tools place each priced place with the same projection.
  python docs/research/2026-10-22-greece-prices/geo/build_map.py"""
import io, json, math, os
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
T = json.load(io.open(os.path.join(H, "countries-10m.json"), encoding="utf-8"))
sc, tr = T["transform"]["scale"], T["transform"]["translate"]
arcs = []
for a in T["arcs"]:
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy; pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
    arcs.append(pts)
LON0, LAT0, LAT1, LON1 = 19.2, 34.7, 41.9, 29.9
COS = math.cos(math.radians(38.5)); W = 800
K = W / ((LON1 - LON0) * COS); Hh = round((LAT1 - LAT0) * K)
proj = lambda lon, lat: ((lon - LON0) * COS * K, (LAT1 - lat) * K)


def ring(idx):
    pts = []
    for i in idx:
        a = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(a if not pts else a[1:])
    return pts


def dp(pts, eps):
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1e-9
    i, dmax = 0, 0
    for k in range(1, len(pts) - 1):
        d = abs(dy * pts[k][0] - dx * pts[k][1] + x2 * y1 - y2 * x1) / L
        if d > dmax: i, dmax = k, d
    if dmax <= eps: return [pts[0], pts[-1]]
    return dp(pts[:i + 1], eps)[:-1] + dp(pts[i:], eps)


def path(geom, eps, clip=False):
    polys = geom["arcs"] if geom["type"] == "MultiPolygon" else [geom["arcs"]]
    out = []
    for poly in polys:
        for r in poly:
            pts = [proj(lon, lat) for lon, lat in ring(r)]
            if clip and not any(-40 <= x <= W + 40 and -40 <= y <= Hh + 40 for x, y in pts): continue
            mid = len(pts) // 2
            s = dp(pts[:mid + 1], eps)[:-1] + dp(pts[mid:], eps)  # a closed ring: simplify the two halves, or it collapses
            if len(s) < 3: continue
            xs = [p[0] for p in s]; ys = [p[1] for p in s]
            if (max(xs) - min(xs)) < 1.2 and (max(ys) - min(ys)) < 1.2: continue
            out.append("M" + "L".join("%.1f,%.1f" % p for p in s) + "Z")
    return "".join(out)


G = {g["properties"]["name"]: g for g in T["objects"]["countries"]["geometries"] if "properties" in g}
gr = path(G["Greece"], 0.35)
nb = "".join(path(G[n], 0.8, clip=True) for n in ("Albania", "North Macedonia", "Macedonia", "Bulgaria", "Turkey") if n in G)
out = {"key": "gmap", "source": "Natural Earth 1:10m (public domain), world-atlas@2.0.2", "vb": [W, Hh],
       "proj": {"lon0": LON0, "lat1": LAT1, "cos": round(COS, 6), "k": round(K, 4)}, "gr": gr, "nb": nb}
dst = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "greece-map.json")
io.open(dst, "w", encoding="utf-8").write(json.dumps(out, separators=(",", ":")))
print("greece-map.json", os.path.getsize(dst), "bytes | viewBox", W, Hh, "| greece path", len(gr), "| neighbours", len(nb))
io.open(os.path.join(H, "preview.svg"), "w", encoding="utf-8").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"><rect width="100%%" height="100%%" fill="#E6F0F3"/><path d="%s" fill="#D3DCE2"/><path d="%s" fill="#fff" stroke="#1F4B5C" stroke-width=".8"/></svg>' % (W, Hh, nb, gr))
