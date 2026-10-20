# -*- coding: utf-8 -*-
"""Kochav HaTzafon world extras (20.10.2026): what build_city_sdedov.py does not draw, added to
docs/sales/kochav-ph/world/city.json in the same grid frame (origin 32.100006, 34.788333, grid -11 degrees).
Public read-only GET queries to the Tel Aviv-Yafo GIS (IView2):
  w   [["name", x1, z1, ...], ...]   water: the Yarkon (layer 504), clipped to a 1.6 km box
  br  [["name", "use", x1, z1, ...]]  bridges standing today (layer 550)
  bk  [["name", x1, z1, ...], ...]   bicycle paths (layer 577), the park's paths among them
  sp  [["sport", "name", x, z], ...]  sports facilities (layer 943)
and the shore: Ashira's OSM coastline (28.9.2026) moved to this origin (the same grid; origin = Ashira grid (180, 600)).
  python scripts/project-stage/kochav_extras.py"""
import io, json, math, os, sys, urllib.parse, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "docs", "sales", "kochav-ph", "world", "city.json")
ASH = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "ashira", "city.json")
O = (32.100006, 34.788333); G = math.radians(-11); SHIFT = (180.0, 600.0); BOX = 1600.0
UA = {"User-Agent": "Mozilla/5.0 NadLan-CITY/1.0"}


def get(layer, **kw):
    p = {"f": "json"}; p.update(kw)
    u = "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/%d/query?" % layer + urllib.parse.urlencode(p)
    return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=180).read().decode("utf-8"))


def local(lng, lat):
    X = (lng - O[1]) * math.cos(math.radians(O[0])) * 111320.0
    Z = -(lat - O[0]) * 110574.0
    c, s = math.cos(G), math.sin(G)
    return (X * c - Z * s, X * s + Z * c)


def env(r):
    dlat = r / 110574.0; dlng = r / (math.cos(math.radians(O[0])) * 111320.0)
    return "%.6f,%.6f,%.6f,%.6f" % (O[1] - dlng, O[0] - dlat, O[1] + dlng, O[0] + dlat)


def feats(layer, r=BOX * 1.42):
    return get(layer, where="1=1", geometry=env(r), geometryType="esriGeometryEnvelope", inSR=4326, spatialRel="esriSpatialRelIntersects",
               outFields="*", returnGeometry="true", outSR=4326, resultRecordCount=2000).get("features") or []


def clip(poly, b=BOX):  # Sutherland-Hodgman against the square [-b, b]
    for axis, sign in ((0, 1), (0, -1), (1, 1), (1, -1)):
        if not poly:
            break
        inside = lambda p: sign * p[axis] <= b
        out = []
        for i in range(len(poly)):
            a, c = poly[i - 1], poly[i]
            ia, ic = inside(a), inside(c)
            if ia != ic:
                t = (sign * b - a[axis]) / (c[axis] - a[axis])
                out.append((a[0] + t * (c[0] - a[0]), a[1] + t * (c[1] - a[1])))
            if ic:
                out.append(c)
        poly = out
    return poly


def thin(Q, d=2.0):
    out = [Q[0]]
    for p in Q[1:]:
        if math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) >= d:
            out.append(p)
    return out


def flat(Q):
    f = []
    for x, z in Q:
        f += [round(x, 1), round(z, 1)]
    return f


c = json.load(io.open(OUT, encoding="utf-8"))
w = []
for f in feats(504, BOX * 2):
    name = (f["attributes"].get("teur") or "").strip()
    if "הים" in name:
        continue
    for ring in (f.get("geometry") or {}).get("rings") or []:
        Q = clip([local(lng, lat) for lng, lat in ring])
        if len(Q) >= 3:
            w.append([name] + flat(thin(Q)))
br = []
for f in feats(550):
    a = f["attributes"]
    for path in (f.get("geometry") or {}).get("paths") or []:
        Q = [local(lng, lat) for lng, lat in path]
        if min(abs(x) for x, z in Q) < BOX and min(abs(z) for x, z in Q) < BOX:
            br.append([(a.get("shem") or "").strip(), (a.get("t_yeud") or "").strip()] + flat(Q))
bk = []
for f in feats(577):
    a = f["attributes"]
    for path in (f.get("geometry") or {}).get("paths") or []:
        Q = [local(lng, lat) for lng, lat in path]
        if any(abs(x) < BOX and abs(z) < BOX for x, z in Q):
            bk.append([(a.get("shem_mikta") or "").strip()] + flat(thin(Q, 3)))
sp = []
for f in feats(943):
    a = f["attributes"]; g = f.get("geometry") or {}
    if "x" in g:
        x, z = local(g["x"], g["y"])
        if abs(x) < BOX and abs(z) < BOX:
            sp.append([(a.get("facility_sport") or "").strip(), (a.get("facility_name") or "").strip(), round(x, 1), round(z, 1)])
ash = json.load(io.open(ASH, encoding="utf-8"))["coast"]
line = [[round(x - SHIFT[0], 1), z - int(SHIFT[1])] for x, z in ash["line"]]
c["coast"] = {"x0": round(ash["x0"] - SHIFT[0] + ash["k"] * SHIFT[1], 1), "k": ash["k"], "line": line, "src": ash.get("src", "") + " (moved to this origin)"}
c.update({"w": w, "br": br, "bk": bk, "sp": sp})
c["source"] += "; הירקון (504), גשרים (550), שבילי אופניים (577), מתקני ספורט (943)"
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(c, ensure_ascii=False, separators=(",", ":")))
print("water", len(w), [(r[0], len(r) // 2) for r in w], "| bridges", len(br), "| bike", len(bk), "| sports", len(sp), "| bytes", os.path.getsize(OUT))
for b in br:
    print("  bridge", b[0], b[1], b[2:4])
