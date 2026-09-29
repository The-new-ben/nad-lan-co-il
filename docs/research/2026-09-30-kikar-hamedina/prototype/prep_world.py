# -*- coding: utf-8 -*-
"""Kikar Hamedina world prototype (P4 design reference, LOCAL ONLY): builds world-data.js for kikar-world.html.

  python docs/research/2026-09-30-kikar-hamedina/prototype/prep_world.py

Inputs (all real, all read-only):
  ../city-blocks.json            buildings within 700 m (GIS 513), towers, plot lots, street axes, green areas
  ../places.json                 1,245 places (findplace + OSM + city layers), for the 25 pins
  ../sight-landmarks.json        far landmarks (sea, port, Reading, Azrieli...) for the window views
  ../kikar-stage/quarter.json    the square's two public buildings (school N, community centre S)
  scripts/project-stage/_cache/kikar-area/gis-513-*.json   the same GIS 513 fetch out to 2 km (context ring 700-2000 m)
  scripts/project-stage/_cache/kikar-area/gis-507/508-*    street axes to 1.6 km
  Tel Aviv-Yafo GIS IView2, fetched once (GET, cached in the same git-ignored folder):
    503 green areas to 2.2 km, 504 water bodies (the sea, the Yarkon, the park lake), 574 tree canopies 2024 to 900 m
Frame: x = metres east of the plot centre, z = metres south (three.js: north = -z), the frame of city-blocks.json.
"""
import glob, hashlib, io, json, math, os, sys, time, urllib.parse, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(RES)))
CACHE = os.path.join(REPO, "scripts", "project-stage", "_cache", "kikar-area")
os.makedirs(CACHE, exist_ok=True)
BASE = "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/%d/query"
UA = {"User-Agent": "Mozilla/5.0 NadLan-CITY/1.0 (nad-lan.co.il; research, read-only)"}
SKIP_TYPES = {"אנטנה", "תחנת אוטובוס", "מבנה ארעי"}
TOWER_OIDS = {45535: "A", 45534: "B", 44219: "C"}

cb = json.load(io.open(os.path.join(RES, "city-blocks.json"), encoding="utf-8"))
O = (cb["origin"]["lat"], cb["origin"]["lng"])
KX = math.cos(math.radians(O[0])) * 111320.0
KZ = 111320.0


def xz(lat, lng):
    return ((lng - O[1]) * KX, -(lat - O[0]) * KZ)


def r1(v):
    return round(v, 1)


def flat(P):
    return [v for x, z in P for v in (r1(x), r1(z))]


def ring_area(P):
    A = 0.0
    for i in range(len(P)):
        x0, z0 = P[i]
        x1, z1 = P[(i + 1) % len(P)]
        A += x0 * z1 - x1 * z0
    return A / 2.0


def centroid(P):
    A = cx = cz = 0.0
    for i in range(len(P)):
        x0, z0 = P[i]
        x1, z1 = P[(i + 1) % len(P)]
        c = x0 * z1 - x1 * z0
        A += c
        cx += (x0 + x1) * c
        cz += (z0 + z1) * c
    if abs(A) < 1e-9:
        return sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P)
    return cx / (3 * A), cz / (3 * A)


def seg_dist(p, a, b):
    ax, az = b[0] - a[0], b[1] - a[1]
    L = ax * ax + az * az
    t = 0 if L == 0 else max(0, min(1, ((p[0] - a[0]) * ax + (p[1] - a[1]) * az) / L))
    return math.hypot(p[0] - a[0] - t * ax, p[1] - a[1] - t * az)


def dp_open(pts, tol):
    if len(pts) < 3:
        return pts
    stack, keep = [(0, len(pts) - 1)], {0, len(pts) - 1}
    while stack:
        i0, i1 = stack.pop()
        best, bi = -1, -1
        for i in range(i0 + 1, i1):
            d = seg_dist(pts[i], pts[i0], pts[i1])
            if d > best:
                best, bi = d, i
        if best > tol:
            keep.add(bi)
            stack += [(i0, bi), (bi, i1)]
    return [pts[i] for i in sorted(keep)]


def simplify_ring(P, tol):
    if len(P) <= 4:
        return P
    far = max(range(len(P)), key=lambda i: math.hypot(P[i][0] - P[0][0], P[i][1] - P[0][1]))
    a = dp_open(P[: far + 1], tol)
    b = dp_open(P[far:] + [P[0]], tol)
    out = a[:-1] + b[:-1]
    return out if len(out) >= 3 else P


def envelope(radius):
    dlat = radius / 110574.0
    dlng = radius / (math.cos(math.radians(O[0])) * 111320.0)
    return "%.6f,%.6f,%.6f,%.6f" % (O[1] - dlng, O[0] - dlat, O[1] + dlng, O[0] + dlat)


def get(layer, **kw):
    p = {"f": "json"}
    p.update(kw)
    url = BASE % layer + "?" + urllib.parse.urlencode(p)
    key = os.path.join(CACHE, "proto-%d-%s.json" % (layer, hashlib.md5(url.encode("utf-8")).hexdigest()[:16]))
    if os.path.exists(key):
        return json.load(io.open(key, encoding="utf-8"))
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                d = json.loads(r.read().decode("utf-8"))
            io.open(key, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False))
            time.sleep(0.4)
            return d
        except Exception:
            if attempt == 2:
                raise
            time.sleep(3)


def fetch_all(layer, radius, fields, **extra):
    out, off = [], 0
    while True:
        d = get(layer, where="1=1", geometry=envelope(radius), geometryType="esriGeometryEnvelope", inSR=4326,
                spatialRel="esriSpatialRelIntersects", outFields=fields, returnGeometry="true", outSR=4326,
                resultOffset=off, resultRecordCount=1000, **extra)
        feats = d.get("features") or []
        out += feats
        if not feats or not d.get("exceededTransferLimit"):
            break
        off += len(feats)
    return out


def height_of(a):
    floors = int(a.get("ms_komot") or 0) or None
    if a.get("gova_simplex_2019"):
        return float(a["gova_simplex_2019"]), "survey"
    if a.get("max_height") and a.get("min_height") and a["max_height"] > a["min_height"]:
        return float(a["max_height"] - a["min_height"]), "roof-base"
    if a.get("dsm_mean"):
        return float(a["dsm_mean"]), "dsm"
    if floors:
        return floors * 3.2, "floors"
    return None, None


# ---------------- 1. buildings: near (city-blocks.json, 700 m) + context ring from the same GIS 513 fetch ----------------
near, near_oids = [], set()
for b in cb["buildings"]:
    near_oids.add(b["oid"])
    if b.get("kikar_tower") or b["oid"] in TOWER_OIDS:
        continue
    if not b.get("h") or b["h"] < 1.5:
        continue
    P = [xz(la, ln) for la, ln in b["fp"]]
    if ring_area(P) < 0:
        P = P[::-1]
    near.append([r1(b["h"]), 1 if b.get("type") == "מבנה ציבור" else 0] + flat(P))

far, seen = [], set()
for f in sorted(glob.glob(os.path.join(CACHE, "gis-513-*.json"))):
    d = json.load(io.open(f, encoding="utf-8"))
    for ft in d.get("features") or []:
        a = ft.get("attributes") or {}
        oid = a.get("oid_mivne")
        if oid in seen or oid in near_oids or oid in TOWER_OIDS:
            continue
        seen.add(oid)
        typ = (a.get("t_sug_mivne") or "").strip()
        if typ in SKIP_TYPES:
            continue
        rings = (ft.get("geometry") or {}).get("rings") or []
        if not rings:
            continue
        ring = rings[0][:-1] if rings[0][0] == rings[0][-1] else rings[0]
        P = [xz(lat, lng) for lng, lat in ring]
        if len(P) < 3:
            continue
        A = ring_area(P)
        if abs(A) < 30:
            continue
        cx, cz = centroid(P)
        if math.hypot(cx, cz) <= 690:
            continue
        h, _ = height_of(a)
        if not h or h < 2:
            continue
        P = simplify_ring(P, 1.0)
        if ring_area(P) < 0:
            P = P[::-1]
        far.append([r1(h), 0] + flat(P))
print("buildings: near %d, context %d" % (len(near), len(far)))

# ---------------- 2. street axes to 1.6 km (cached GIS 507/508, the width classes of build_area_kikar.py) ----------------
mains = set()
for f in glob.glob(os.path.join(CACHE, "gis-508-*.json")):
    for ft in json.load(io.open(f, encoding="utf-8")).get("features") or []:
        mains.add((ft["attributes"].get("t_rechov") or "").strip())
streets, ring_axes, seen_s = [], [], set()
for f in sorted(glob.glob(os.path.join(CACHE, "gis-507-*.json"))):
    for ft in json.load(io.open(f, encoding="utf-8")).get("features") or []:
        a = ft["attributes"]
        name = (a.get("t_rechov") or "").strip()
        sug = (a.get("t_sug") or "").strip()
        k = int(a.get("k_reka") or 0)
        w = 5 if (sug in ("שביל", "סמטת") or k in (0, 50)) else (24 if sug == "שדרות" else (20 if (k == 200 or name in mains) else 10))
        for path in (ft["geometry"].get("paths") or []):
            key = json.dumps(path[:2])
            if key in seen_s:
                continue
            seen_s.add(key)
            P = dp_open([xz(lat, lng) for lng, lat in path], 0.6)
            if min(max(abs(x), abs(z)) for x, z in P) > 1650:
                continue
            rec = [w, 1 if name in ("הא באייר",) else 0] + flat(P)
            streets.append(rec)
            if name == "הא באייר":
                ring_axes.append(flat(P))
print("streets", len(streets), "ring pieces", len(ring_axes))

# ---------------- 3. green areas (GIS 503) to 2.2 km; the square's park at full detail ----------------
greens, park = [], None
for ft in fetch_all(503, 2200, "shem_gan,sug_gan"):
    a = ft["attributes"]
    name = (a.get("shem_gan") or "").strip()
    for ring in (ft["geometry"].get("rings") or []):
        P = [xz(lat, lng) for lng, lat in ring[:-1]]
        if len(P) < 3 or abs(ring_area(P)) < 60:
            continue
        if name == "ככר המדינה" and abs(ring_area(P)) > 5000:
            park = flat(simplify_ring(P, 0.25))
        P = simplify_ring(P, 0.8 if max(abs(p[0]) for p in P) < 800 else 1.8)
        greens.append(flat(P))
print("greens", len(greens), "park pts", len(park or []) // 2)

# ---------------- 4. water (GIS 504): the sea, the Yarkon, the Yarkon park lake ----------------
water = []
for ft in fetch_all(504, 6000, "teur"):
    name = (ft["attributes"].get("teur") or "").strip()
    rings = ft["geometry"].get("rings") or []
    for i, ring in enumerate(rings):
        P = [xz(lat, lng) for lng, lat in ring[:-1]]
        if len(P) < 3:
            continue
        P = simplify_ring(P, 1.5)
        A = ring_area(P)
        water.append({"name": name, "outer": i == 0, "area": round(abs(A)), "pts": flat(P)})
print("water rings", [(w["name"], w["outer"], w["area"], len(w["pts"]) // 2) for w in water])

# ---------------- 5. tree canopies 2024 (GIS 574) to 900 m: centroid + equivalent radius ----------------
def inside(P, x, z):
    c = False
    j = len(P) - 1
    for i in range(len(P)):
        xi, zi = P[i]
        xj, zj = P[j]
        if (zi > z) != (zj > z) and x < (xj - xi) * (z - zi) / (zj - zi + 1e-12) + xi:
            c = not c
        j = i
    return c


# a canopy polygon is often a whole row of street trees merged into one shape: small polygons become one tree at the
# centroid, large ones are filled with trees on a jittered 7 m grid (deterministic). Canopy footprints are the city's;
# the individual crowns and the heights are an illustration.
import random
rng = random.Random(20260930)
trees, n_poly = [], 0
for ft in fetch_all(574, 900, "Shape_Area", maxAllowableOffset=0.00001, geometryPrecision=7):
    rings = ft["geometry"].get("rings") or []
    if not rings:
        continue
    P = [xz(lat, lng) for lng, lat in rings[0][:-1]]
    if len(P) < 3:
        continue
    A = abs(ring_area(P))
    if A < 6:
        continue
    cx, cz = centroid(P)
    if math.hypot(cx, cz) > 900:
        continue
    n_poly += 1
    if A < 75:
        trees.append([r1(cx), r1(cz), round(max(1.4, min(math.sqrt(A / math.pi), 4.6)), 1)])
        continue
    S = 7.0
    xs = [p[0] for p in P]
    zs = [p[1] for p in P]
    got = 0
    x = math.floor(min(xs) / S) * S
    while x <= max(xs):
        z = math.floor(min(zs) / S) * S
        while z <= max(zs):
            jx, jz = x + rng.uniform(-1.3, 1.3), z + rng.uniform(-1.3, 1.3)
            if inside(P, jx, jz):
                trees.append([r1(jx), r1(jz), round(rng.uniform(3.2, 4.3), 1)])
                got += 1
            z += S
        x += S
    if not got:
        trees.append([r1(cx), r1(cz), 3.8])
print("tree canopy polygons", n_poly, "-> trees", len(trees))

# ---------------- 6. the plot: lots of plan 2500ב and the three towers (municipal footprints) ----------------
lots = []
for l in cb["plot"]["lots"]:
    P = [xz(la, ln) for la, ln in l["ring"]]
    lots.append({"lot": l["lot"], "use": l["use"], "pts": flat(P)})
towers = []
PUB = {"A": {"floors": 40, "h": 160.0, "src": "Hebrew Wikipedia / Ashtrom: 40 floors, 160 m"},
       "B": {"floors": 37, "h": 157.0, "src": "Hebrew Wikipedia / Ashtrom: 37 floors, 157 m (the city's GIS 513: 40 floors, 158.2 m)"},
       "C": {"floors": 40, "h": 160.0, "src": "Hebrew Wikipedia / Ashtrom: 40 floors, 160 m"}}
for t in cb["plot"]["towers"]:
    k = t["name"][-1]
    P = [xz(la, ln) for la, ln in t["fp"]]
    if ring_area(P) < 0:
        P = P[::-1]
    cx, cz = centroid(P)
    # the footprint's orientation: the bearing of its first long edge, folded into 0-90
    ang = []
    for i in range(len(P)):
        (x0, z0), (x1, z1) = P[i], P[(i + 1) % len(P)]
        ang.append(math.degrees(math.atan2(x1 - x0, -(z1 - z0))) % 90)
    base = sum(ang) / len(ang)
    side = math.sqrt(abs(ring_area(P)))
    towers.append({"key": k, "name": t["name"], "cx": r1(cx), "cz": r1(cz), "fp": flat(P), "area": round(abs(ring_area(P))),
                   "side": round(side, 1), "base_bearing": round(base, 1), "gis_floors": t["floors"], "gis_h": t["h"],
                   "floors": PUB[k]["floors"], "h": PUB[k]["h"], "src": PUB[k]["src"]})
print("towers", [(t["key"], t["cx"], t["cz"], t["side"], t["base_bearing"]) for t in towers])

# ---------------- 7. the 25 pins ----------------
places = json.load(io.open(os.path.join(RES, "places.json"), encoding="utf-8"))["places"]
quarter = json.load(io.open(os.path.join(RES, "kikar-stage", "quarter.json"), encoding="utf-8"))
PICK = [  # (name as in places.json, kind shown, English, tier) tier 1 = always shown in the aerial
    ("תחנת איכילוב, הקו הסגול", "transport", "Ichilov station, Purple Line (planned 2028)", 1),
    ("תחנת ארלוזרוב, הקו האדום", "transport", "Arlozorov station, Red Line", 1),
    ("תל אביב סבידור מרכז", "transport", "Tel Aviv Savidor Center railway", 2),
    ("תחנת ארלוזורוב, הקו הירוק", "transport", "Arlozorov West, Green Line (planned)", 2),
    ("בי\"ח איכילוב", "health", "Ichilov Hospital", 1),
    ("פארק הירקון (גני יהושע), ליד בני דן", "outdoors", "Park HaYarkon (Ganei Yehoshua)", 1),
    ("גן אברהם", "outdoors", "Abraham Park", 2),
    ("ZEST", "food", "ZEST supermarket", 1),
    ("בייקרי כיכר המדינה", "food", "Kikar HaMedina Bakery (café)", 1),
    ("City Market", "food", "City Market", 2),
    ("Gucci", "shop", "Gucci", 1),
    ("Open", "food", "Open (restaurant)", 2),
    ("לחם ארז", "food", "Lehem Erez (café)", 1),
    ("הקערה", "food", "HaKe'ara (grocery)", 2),
    ("Miele", "shop", "Miele", 2),
    ("TOLLMAN'S", "shop", "Tollman's", 2),
    ("מרינדו", "shop", "Marinado", 2),
    ("ויקטורי", "food", "Victory supermarket", 2),
    ("הגימנסיה העברית הרצליה", "education", "Herzliya Hebrew Gymnasium", 1),
    ("תיאטרון תל אביב", "culture", "Tel Aviv Theatre", 2),
    ("מרכז ויצמן", "shop", "Weizman Centre", 2),
    ("ארלוזורוב 97 - הקאנטרי הקהילתי במרכז", "outdoors", "Arlozorov 97 Sports Center", 2),
    ("ענן", "education", "Anan kindergarten", 2),
]
KIND_HE = {"transport": "תחבורה", "health": "בריאות", "outdoors": "פארק", "food": "מזון", "shop": "קניות",
           "education": "חינוך", "culture": "תרבות", "civic": "מבנה ציבור"}
pins = []
for qp, en in ((quarter["places"][0], "Kikar HaMedina school"), (quarter["places"][1], "Community centre")):
    pins.append({"name": qp["name"], "en": en, "kind": "civic" if "קהילתי" in qp["name"] else "education", "x": qp["x"], "z": qp["z"],
                 "dist": qp["dist"], "walk": 1, "tier": 1, "src": qp["src"][:160]})
for name, kind, en, tier in PICK:
    c = [p for p in places if p["name"] == name]
    if not c:
        print("MISSING pin", name)
        continue
    p = min(c, key=lambda p: p["dist"])
    extra = p.get("opens") or ""
    pins.append({"name": name, "en": en, "kind": kind, "x": p["x"], "z": p["z"], "dist": p["dist"], "walk": p.get("walk"),
                 "tier": tier, "line": p.get("line"), "note": extra, "src": p.get("src")})
print("pins", len(pins))
for p in pins:
    p["kind_he"] = KIND_HE.get(p["kind"], "")

# ---------------- 8. far landmarks for the window views (sight-landmarks.json) ----------------
sl = json.load(io.open(os.path.join(RES, "sight-landmarks.json"), encoding="utf-8"))
marks = []
for l in sl["landmarks"]:
    if l["key"] in ("sea", "port", "reading_lighthouse", "reading", "sportek", "ramat_aviv", "tau", "azrieli_center", "ichilov",
                    "city_hall", "savidor", "moshe_aviv", "azrieli_sarona", "habima"):
        x, z = xz(l["lat"], l["lng"])
        marks.append({"key": l["key"], "name": l["name"].split(" (")[0], "en": l["name_en"], "x": r1(x), "z": r1(z), "h": l.get("h"),
                      "dist": l["dist_m"]})

eye = json.load(io.open(os.path.join(RES, "eye-kikar-provisional.json"), encoding="utf-8"))
out = {"v": 1, "generated_at": time.strftime("%Y-%m-%d"), "origin": {"lat": O[0], "lng": O[1]},
       "frame": "x metres east, z metres south of the plot centre (three.js north = -z)",
       "near": near, "far": far, "streets": streets, "ring": ring_axes, "greens": greens, "park": park, "water": water,
       "trees": trees, "lots": lots, "towers": towers, "pins": pins, "marks": marks, "eye_rule": eye["source"],
       "src": {"buildings": cb["source"], "streets": "GIS 507/508", "greens": "GIS 503", "water": "GIS 504",
               "trees": "GIS 574 (tree canopies 2024)", "pins": "places.json (findplace + OSM + city layers)"}}
js = "window.KIKAR_WORLD = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n"
p = os.path.join(HERE, "world-data.js")
io.open(p, "w", encoding="utf-8", newline="\n").write(js)
print("wrote", p, os.path.getsize(p), "bytes")
