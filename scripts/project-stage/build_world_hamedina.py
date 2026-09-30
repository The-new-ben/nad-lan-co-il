# -*- coding: utf-8 -*-
"""Kikar Hamedina towers: the WORLD data for the shared world module (P5, LOCAL build, no network unless a cache is missing).

    python scripts/project-stage/build_world_hamedina.py

Writes
    plugins/nadlan-config/assets/project-stage/hamedina/world.json    the core world (quantized, compact; budget ~1.5 MB)
    plugins/nadlan-config/assets/project-stage/hamedina/places.json   a copy of the P2 place registry (loaded on intent)

Reads (all real, all read-only; nothing is invented, every fact line carries its source)
    docs/research/2026-09-30-kikar-hamedina/city-blocks.json      buildings within 700 m (TLV GIS 513) with heights,
                                                                  floors, year; the plot (lots of plan 2500ב, GIS 837);
                                                                  the three towers' municipal footprints
    docs/research/2026-09-30-kikar-hamedina/places.json           1,245 places (findplace + OSM + city layers + Mapbox walk)
    docs/research/2026-09-30-kikar-hamedina/sight-landmarks.json  far landmarks (sea, port, Reading, Azrieli ...)
    docs/research/2026-09-30-kikar-hamedina/kikar-stage/quarter.json   the square's two public buildings (4.8.2021 decision)
    scripts/project-stage/_cache/kikar-area/gis-513-*.json        GIS 513 out to 2 km (context ring 700 m - 2 km)
    scripts/project-stage/_cache/kikar-area/gis-507/508-*.json    street axes (GIS 507) and main streets (508)
    scripts/project-stage/_cache/kikar-area/proto-503/504/574-*   green areas, water, tree canopies 2024 (fetched by the
                                                                  P4 prototype with plain GET; fetched again if missing)

Frame: x = metres east of the plot centre 32.086758, 34.789776, z = metres south (three.js north = -z); the frame of
city-blocks.json and places.json (111,320 m per degree, x scaled by cos(lat)).

Encoding (world.json "enc": "nlw2"): the heavy layers are flat integer arrays (JSON; the trees as little-endian Int16 in
base64). Each record starts with a small header, then the first vertex absolute and the rest as deltas, in the layer's unit
("q", metres per step). Integers with deltas compress well with the server's gzip/brotli.
    blocks  q=0.1   [n, h_dm, floors, year, flags, x0, z0, dx1, dz1, ...]   flags: 1 public, 2 near (<700 m), 4 ring
                    building of the square, 8 school, 16 community centre, 32 under construction, 64-192 height source
                    (0 survey 2019, 1 roof-base, 2 DSM, 3 estimated floors x 3.2 m), 256 coordinates in 0.5 m steps
    streets q=0.1   [n, width_m, flags, name_index, x0, z0, dx, dz, ...]    flags: 1 the ring road ה' באייר
    greens  q=0.5   [n, name_index, flags, x0, z0, dx, dz, ...]             flags: 1 the square's own park
    trees   q=0.1   [x, z, r] per tree (the city's 2024 canopy layer; crown sizes and heights are an illustration)
    water   q=1     JSON: [{"n": name_index, "o": 1 outer / 0 hole, "p": [x0, z0, dx, dz, ...]}]
"""
import base64, glob, hashlib, io, json, math, os, random, re, shutil, struct, sys, time, urllib.parse, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RES = os.path.join(REPO, "docs", "research", "2026-09-30-kikar-hamedina")
CACHE = os.path.join(HERE, "_cache", "kikar-area")
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "hamedina")
os.makedirs(CACHE, exist_ok=True)
os.makedirs(OUT, exist_ok=True)
BASE = "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/%d/query"
UA = {"User-Agent": "Mozilla/5.0 NadLan-CITY/1.0 (nad-lan.co.il; research, read-only)"}
SKIP_TYPES = {"אנטנה", "תחנת אוטובוס", "מבנה ארעי"}
TOWER_OIDS = {45535: "A", 45534: "B", 44219: "C"}
SCHOOL_OID, CENTRE_OID = 43143, 43109

cb = json.load(io.open(os.path.join(RES, "city-blocks.json"), encoding="utf-8"))
O = (cb["origin"]["lat"], cb["origin"]["lng"])
KX = math.cos(math.radians(O[0])) * 111320.0
KZ = 111320.0


def xz(lat, lng):
    return ((lng - O[1]) * KX, -(lat - O[0]) * KZ)


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


def get(layer, prefix="proto", **kw):
    p = {"f": "json"}
    p.update(kw)
    url = BASE % layer + "?" + urllib.parse.urlencode(p)
    key = os.path.join(CACHE, "%s-%d-%s.json" % (prefix, layer, hashlib.md5(url.encode("utf-8")).hexdigest()[:16]))
    if os.path.exists(key):
        return json.load(io.open(key, encoding="utf-8"))
    print("  fetching GIS layer", layer, "(public, GET)")
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


def fetch_all(layer, radius, fields, prefix="proto", **extra):
    out, off = [], 0
    while True:
        d = get(layer, prefix=prefix, where="1=1", geometry=envelope(radius), geometryType="esriGeometryEnvelope", inSR=4326,
                spatialRel="esriSpatialRelIntersects", outFields=fields, returnGeometry="true", outSR=4326,
                resultOffset=off, resultRecordCount=1000, **extra)
        feats = d.get("features") or []
        out += feats
        if not feats or not d.get("exceededTransferLimit"):
            break
        off += len(feats)
    return out


# ------------------------------------------------------------------------------------------------ encoding helpers
def q(v, unit):
    return int(round(v / unit))


def enc_ring(P, unit):
    """first vertex absolute, the rest as deltas, in steps of `unit` metres"""
    out, px, pz = [], 0, 0
    for i, (x, z) in enumerate(P):
        qx, qz = q(x, unit), q(z, unit)
        if i == 0:
            out += [qx, qz]
        else:
            out += [qx - px, qz - pz]
        px, pz = qx, qz
    return out


def b64_i16(vals):
    for v in vals:
        if v < -32768 or v > 32767:
            raise ValueError("Int16 overflow %r" % v)
    return base64.b64encode(struct.pack("<%dh" % len(vals), *vals)).decode("ascii")


def height_of(a):
    floors = int(a.get("ms_komot") or 0) or None
    if a.get("gova_simplex_2019"):
        return float(a["gova_simplex_2019"]), 0
    if a.get("max_height") and a.get("min_height") and a["max_height"] > a["min_height"]:
        return float(a["max_height"] - a["min_height"]), 1
    if a.get("dsm_mean"):
        return float(a["dsm_mean"]), 2
    if floors:
        return floors * 3.2, 3
    return None, None


HSRC = {"survey 2019 (gova_simplex_2019)": 0, "roof minus base (max_height - min_height)": 1, "DSM mean (dsm_mean)": 2,
        "ESTIMATED: floors x 3.2 m": 3}
names = []


def name_index(s):
    s = (s or "").strip()
    if not s:
        return -1
    if s not in names:
        names.append(s)
    return names.index(s)


# ------------------------------------------------------------------------------------------------ 1. buildings
blocks, near_oids, block_names, civic_idx = [], set(), {}, {}
ring_count = 0
for b in cb["buildings"]:
    near_oids.add(b["oid"])
    if b.get("kikar_tower") or b["oid"] in TOWER_OIDS:
        continue
    if not b.get("h") or b["h"] < 1.5:
        continue
    P = [xz(la, ln) for la, ln in b["fp"]]
    if ring_area(P) < 0:
        P = P[::-1]
    cx, cz = centroid(P)
    d = math.hypot(cx, cz)
    flags = 2
    if b.get("type") == "מבנה ציבור":
        flags |= 1
    if b.get("type") == "מבנה בבנייה":
        flags |= 32
    # the square's ring of 1970s buildings (outside the ring road ה' באייר, 128-147 m from the centre)
    if 146 < d < 163 and b["h"] >= 15:
        flags |= 4
        ring_count += 1
    if b["oid"] == SCHOOL_OID:
        flags |= 8
    if b["oid"] == CENTRE_OID:
        flags |= 16
    flags |= HSRC.get(b.get("h_src"), 3) << 6
    rec = [len(P), q(b["h"], 0.1), int(b.get("floors") or 0), int(b.get("year") or 0), flags] + enc_ring(P, 0.1)
    if b.get("name") and b["oid"] not in (SCHOOL_OID, CENTRE_OID):
        block_names[len(blocks)] = b["name"]
    if b["oid"] == SCHOOL_OID:
        civic_idx["school"] = len(blocks)
    if b["oid"] == CENTRE_OID:
        civic_idx["centre"] = len(blocks)
    blocks.append(rec)
n_near = len(blocks)

seen = set()
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
        h, hs = height_of(a)
        if not h or h < 2:
            continue
        P = simplify_ring(P, 1.0)
        if len(P) < 3:
            continue
        if ring_area(P) < 0:
            P = P[::-1]
        flags = (1 if typ == "מבנה ציבור" else 0) | (hs << 6) | 256  # 256: coordinates in 0.5 m steps (the far ring is simplified to 1 m)
        blocks.append([len(P), q(h, 0.1), int(a.get("ms_komot") or 0), 0, flags] + enc_ring(P, 0.5))
if not seen:
    print("WARNING: no GIS 513 context cache (run build_area_kikar.py first); the world has the 700 m ring only")
print("buildings: near %d (ring of the square %d), context %d" % (n_near, ring_count, len(blocks) - n_near))

# ------------------------------------------------------------------------------------------------ 2. streets
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
            if max(max(abs(x), abs(z)) for x, z in P) > 3200:
                continue
            is_ring = name == "הא באייר"
            streets.append([len(P), w, 1 if is_ring else 0, name_index(name)] + enc_ring(P, 0.1))
            if is_ring:
                ring_axes.append(enc_ring(P, 0.1))
print("streets", len(streets), "ring pieces", len(ring_axes))

# ------------------------------------------------------------------------------------------------ 3. greens (GIS 503)
greens, park = [], None
for ft in fetch_all(503, 2200, "shem_gan,sug_gan"):
    a = ft["attributes"]
    name = (a.get("shem_gan") or "").strip()
    for ring in (ft["geometry"].get("rings") or []):
        P = [xz(lat, lng) for lng, lat in ring[:-1]]
        if len(P) < 3 or abs(ring_area(P)) < 60:
            continue
        flags = 0
        if name == "ככר המדינה" and abs(ring_area(P)) > 5000:
            park = enc_ring(simplify_ring(P, 0.25), 0.1)
            flags = 1
        P = simplify_ring(P, 0.8 if max(abs(p[0]) for p in P) < 800 else 1.8)
        if ring_area(P) < 0:
            P = P[::-1]
        greens.append([len(P), name_index(name), flags] + enc_ring(P, 0.5))
print("greens", len(greens), "park", bool(park))

# ------------------------------------------------------------------------------------------------ 4. water (GIS 504)
water = []
for ft in fetch_all(504, 6000, "teur"):
    name = (ft["attributes"].get("teur") or "").strip()
    rings = ft["geometry"].get("rings") or []
    for i, ring in enumerate(rings):
        P = [xz(lat, lng) for lng, lat in ring[:-1]]
        if len(P) < 3:
            continue
        P = simplify_ring(P, 1.5)
        water.append({"n": name_index(name), "o": 1 if i == 0 else 0, "p": enc_ring(P, 1.0)})
print("water rings", len(water))


# ------------------------------------------------------------------------------------------------ 5. trees (GIS 574, 2024)
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


rng = random.Random(20260930)
trees = []
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
    if A < 75:
        trees.append((cx, cz, max(1.4, min(math.sqrt(A / math.pi), 4.6))))
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
                trees.append((jx, jz, rng.uniform(3.2, 4.3)))
                got += 1
            z += S
        x += S
    if not got:
        trees.append((cx, cz, 3.8))
tree_vals = []
for x, z, r in trees:
    tree_vals += [q(x, 0.1), q(z, 0.1), q(r, 0.1)]
print("trees", len(trees))

# ------------------------------------------------------------------------------------------------ 6. the plot and the towers
lots = []
for l in cb["plot"]["lots"]:
    P = [xz(la, ln) for la, ln in l["ring"]]
    lots.append({"lot": l["lot"], "use": l["use"], "p": enc_ring(P, 0.1)})

PUB = {"A": (40, 160.0), "B": (37, 157.0), "C": (40, 160.0)}
towers = []
for t in cb["plot"]["towers"]:
    k = t["name"][-1]
    P = [xz(la, ln) for la, ln in t["fp"]]
    if ring_area(P) < 0:
        P = P[::-1]
    cx, cz = centroid(P)
    ang = []
    for i in range(len(P)):
        (x0, z0), (x1, z1) = P[i], P[(i + 1) % len(P)]
        ang.append(math.degrees(math.atan2(x1 - x0, -(z1 - z0))) % 90)
    base = sum(ang) / len(ang)
    side = math.sqrt(abs(ring_area(P)))
    towers.append({"key": k, "cx": round(cx, 2), "cz": round(cz, 2), "fp": enc_ring(P, 0.1), "area": round(abs(ring_area(P))),
                   "side": round(side, 2), "base_bearing": round(base, 2), "gis_floors": t["floors"], "gis_h": t["h"],
                   "floors": PUB[k][0], "h": PUB[k][1]})
towers.sort(key=lambda t: t["key"])
print("towers", [(t["key"], t["cx"], t["cz"], t["side"], t["base_bearing"]) for t in towers])

# ------------------------------------------------------------------------------------------------ 7. the pond (ILLUSTRATION)
# No outline of the ecological pond has been published (area.md, 30.9.2026). The design (v104) shows it, so it is drawn as an
# amorphous 2,500 m2 shape in the middle of the park with a dashed outline and the label "location and shape for illustration".
def signed(P):
    return ring_area(P)


raw, n = [], 64
rr = lambda t: 1 + 0.16 * math.sin(2 * t + 0.6) + 0.1 * math.sin(3 * t + 2.1) + 0.05 * math.sin(5 * t + 0.3)
for i in range(n):
    t = i / n * math.pi * 2
    raw.append((math.cos(t) * rr(t) * 1.25, math.sin(t) * rr(t) * 0.85))
kk = math.sqrt(2500.0 / abs(signed(raw)))
rot = math.radians(-18)
pond = [(6 + (u * math.cos(rot) - v * math.sin(rot)) * kk, 2 + (u * math.sin(rot) + v * math.cos(rot)) * kk) for u, v in raw]
pond_area = round(abs(signed(pond)))

# ------------------------------------------------------------------------------------------------ 8. featured pins and far marks
places_doc = json.load(io.open(os.path.join(RES, "places.json"), encoding="utf-8"))
places = places_doc["places"]
quarter = json.load(io.open(os.path.join(RES, "kikar-stage", "quarter.json"), encoding="utf-8"))
PICK = [  # (name in places.json, English, tier) tier 1 = named in the aerial view
    ("תחנת איכילוב, הקו הסגול", "Ichilov station, Purple Line", 1),
    ("תחנת ארלוזרוב, הקו האדום", "Arlozorov station, Red Line", 1),
    ("תל אביב סבידור מרכז", "Tel Aviv Savidor Center railway", 2),
    ("תחנת ארלוזורוב, הקו הירוק", "Arlozorov station, Green Line", 2),
    ("בי\"ח איכילוב", "Ichilov Hospital", 1),
    ("פארק הירקון (גני יהושע), ליד בני דן", "Park HaYarkon (Ganei Yehoshua)", 1),
    ("גן אברהם", "Abraham Park", 2),
    ("ZEST", "ZEST", 2),
    ("בייקרי כיכר המדינה", "Kikar HaMedina Bakery", 2),
    ("Gucci", "Gucci", 2),
    ("לחם ארז", "Lehem Erez", 2),
    ("הגימנסיה העברית הרצליה", "Herzliya Hebrew Gymnasium", 1),
    ("תיאטרון תל אביב", "Tel Aviv Theatre", 2),
    ("ארלוזורוב 97 - הקאנטרי הקהילתי במרכז", "Arlozorov 97 sports centre", 2),
]
pins = []
for name, en, tier in PICK:
    c = [p for p in places if p["name"] == name]
    if not c:
        print("MISSING pin", name)
        continue
    p = min(c, key=lambda p: p["dist"])
    pins.append({"id": p["id"], "tier": tier, "en": en})

sl = json.load(io.open(os.path.join(RES, "sight-landmarks.json"), encoding="utf-8"))
marks = []
for l in sl["landmarks"]:
    if l["key"] in ("sea", "port", "reading_lighthouse", "reading", "sportek", "ramat_aviv", "tau", "azrieli_center", "ichilov",
                    "city_hall", "savidor", "moshe_aviv", "azrieli_sarona", "habima"):
        x, z = xz(l["lat"], l["lng"])
        en = re.sub(r"\s*\([^)]*[֐-׿][^)]*\)", "", l["name_en"]).strip()
        marks.append({"key": l["key"], "he": l["name"].split(" (")[0], "en": en, "x": round(x), "z": round(z),
                      "h": l.get("h"), "dist": l["dist_m"]})

# ------------------------------------------------------------------------------------------------ 9. the facts (sourced)
S = {
    "wiki_he": {"he": "ויקיפדיה, מגדלי כיכר המדינה", "en": "Hebrew Wikipedia, Kikar HaMedina Towers",
                "url": "https://he.wikipedia.org/wiki/מגדלי_כיכר_המדינה"},
    "ashtrom": {"he": "אשטרום, עמוד הפרויקט", "en": "Ashtrom, project page", "url": "https://www.ashtrom.co.il/projects/kikar-hamedina"},
    "electra": {"he": "אלקטרה בנייה, עמוד הפרויקט", "en": "Electra Construction, project page",
                "url": "https://www.electra.co.il/en/electra_building/projects/kikar_hamedina_towers"},
    "mys": {"he": "יסקי מור סיון אדריכלים", "en": "Yaski Mor Sivan Architects", "url": "https://m-y-s.com/Kikar-Hamedina"},
    "mako_0926": {"he": "מאקו, 24.9.2026", "en": "Mako, 24.9.2026",
                  "url": "https://www.mako.co.il/living-architecture/local/Article-1b24331b3cec0a1026.htm"},
    "mako_1125": {"he": "מאקו, 11.11.2025", "en": "Mako, 11.11.2025",
                  "url": "https://www.mako.co.il/finances-real-estate/Article-cdd2b05daf37a91026.htm"},
    "globes_0925": {"he": "גלובס, 25.9.2025", "en": "Globes, 25.9.2025",
                    "url": "https://en.globes.co.il/en/article-tel-avivs-kikar-hamedina-undergoes-transformation-1001522524"},
    "globes_1222": {"he": "גלובס, 14.12.2022", "en": "Globes, 14.12.2022", "url": "https://en.globes.co.il/en/article-1001432722"},
    "alum": {"he": "אלום אשת", "en": "Alum Eshet",
             "url": "https://www.alumeshet.co.il/en/projects/%D7%9B%D7%99%D7%9B%D7%A8-%D7%94%D7%9E%D7%93%D7%99%D7%A0%D7%94/"},
    "tlv_site": {"he": "עיריית תל אביב-יפו, אתרי בנייה (תיק 61-1-2018-0391)", "en": "Tel Aviv-Yafo municipality, building sites (file 61-1-2018-0391)",
                 "url": "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/499"},
    "tlv_513": {"he": "מאגר המבנים של עיריית תל אביב-יפו", "en": "Tel Aviv-Yafo municipality buildings data",
                "url": "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/513"},
    "tlv_0821": {"he": "החלטת הוועדה המקומית, 4.8.2021", "en": "Local planning committee decision, 4.8.2021",
                 "url": "https://www.tel-aviv.gov.il/Residents/Development/DocLib/2500%D7%91-%D7%9B%D7%99%D7%9B%D7%A8%20%D7%94%D7%9E%D7%93%D7%99%D7%A0%D7%94%20%D7%9E%D7%91%D7%A0%D7%99%20%D7%A6%D7%99%D7%91%D7%95%D7%A8%20%D7%A2%D7%99%D7%A6%D7%95%D7%91.pdf"},
    "wiki_en_sq": {"he": "ויקיפדיה (אנגלית), כיכר המדינה", "en": "Wikipedia, Kikar Hamedina", "url": "https://en.wikipedia.org/wiki/Kikar_Hamedina"},
    "wiki_he_sq": {"he": "ויקיפדיה, כיכר המדינה", "en": "Hebrew Wikipedia, Kikar HaMedina", "url": "https://he.wikipedia.org/wiki/כיכר_המדינה"},
    "ynetnews": {"he": "ynetnews", "en": "ynetnews", "url": "https://www.ynetnews.com/real-estate/article/r1w0etf111e"},
    "tlv_503": {"he": "השטחים הירוקים של עיריית תל אביב-יפו", "en": "Tel Aviv-Yafo municipality green areas",
                "url": "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/503"},
    "tlv_574": {"he": "חופות העצים של עיריית תל אביב-יפו, 2024", "en": "Tel Aviv-Yafo municipality tree canopies, 2024",
                "url": "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/574"},
    "tlv_507": {"he": "צירי הרחובות של עיריית תל אביב-יפו", "en": "Tel Aviv-Yafo municipality street axes",
                "url": "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/507"},
    "tlv_837": {"he": "מגרשי תכנית 2500ב, עיריית תל אביב-יפו", "en": "Plan 2500B lots, Tel Aviv-Yafo municipality",
                "url": "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/837"},
    "tlv_504": {"he": "גופי המים של עיריית תל אביב-יפו", "en": "Tel Aviv-Yafo municipality water bodies",
                "url": "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/504"},
    "tlvonline": {"he": "tlvonline, 2.11.2025", "en": "tlvonline, 2.11.2025",
                  "url": "https://tlvonline.co.il/%D7%A9%D7%93%D7%A8%D7%95%D7%92-%D7%9B%D7%99%D7%9B%D7%A8-%D7%94%D7%9E%D7%93%D7%99%D7%A0%D7%94-%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91/"},
}


def L(he, en, *src):
    return {"he": he, "en": en, "src": list(src)}


facts = {
    "towers": [
        L("שלושה מגדלי מגורים: מגדל A ומגדל C בני 40 קומות ו-160 מ׳, מגדל B בן 37 קומות ו-157 מ׳", "Three residential towers: towers A and C of 40 floors and 160 m, tower B of 37 floors and 157 m", "wiki_he", "ashtrom"),
        L("כל קומה מסתובבת 1.25° ביחס לקומה שמתחתיה", "Every floor turns 1.25° against the floor below", "wiki_he", "mako_0926", "alum"),
        L("453 דירות בשלושת המגדלים", "453 apartments in the three towers", "ashtrom", "wiki_he", "globes_1222"),
        L("אדריכלים: יסקי מור סיון · ביצוע: אלקטרה בנייה ואשטרום", "Architects: Yaski Mor Sivan · Built by Electra Construction and Ashtrom", "mys", "electra", "ashtrom"),
        L("חזית של תקרות וקירות מסך לבנים שחוזרים קומה אחר קומה", "A façade of floor slabs and white curtain walls repeated floor after floor", "mys", "mako_0926"),
        L("בריכה, חדר כושר, ספא, חדרי טיפולים ואולמות רב-תכליתיים באחת מקומות המרתף", "Pool, gym, spa, treatment rooms and multi-purpose halls on one of the basement levels", "ashtrom"),
        L("גמר שלד: 23.4.2026, לפי רישום אתר הבנייה בעירייה", "Frame completed on 23.4.2026, per the municipality's building-site record", "tlv_site"),
    ],
    "tower": {
        "A": [L("40 קומות · 160 מ׳", "40 floors · 160 m", "wiki_he", "ashtrom", "tlv_513"),
              L("בדרום-מערב המתחם", "In the south-west of the compound", "tlv_513")],
        "B": [L("37 קומות · 157 מ׳", "37 floors · 157 m", "wiki_he", "ashtrom"),
              L("במאגר המבנים של העירייה: 40 קומות · 158.2 מ׳", "In the municipality's buildings data: 40 floors · 158.2 m", "tlv_513"),
              L("בדרום-מזרח המתחם", "In the south-east of the compound", "tlv_513")],
        "C": [L("40 קומות · 160 מ׳", "40 floors · 160 m", "wiki_he", "ashtrom", "tlv_513"),
              L("בצפון-מזרח המתחם", "In the north-east of the compound", "tlv_513")],
    },
    "park": [
        L("פארק ציבורי של כ-40 דונם במרכז הכיכר", "A public park of about 40 dunams in the heart of the square", "globes_0925", "mako_0926"),
        L("אגם אקולוגי בעומק 1 מ׳, מדשאות, גינת כלבים ומתקני משחק", "An ecological pond 1 m deep, lawns, a dog park and playgrounds", "mako_0926", "mako_1125"),
        L("560 עצים חדשים ו-36 עצים ותיקים שנשמרו", "560 new trees and 36 mature trees kept", "mako_1125", "mako_0926"),
        L("מסלול ריצה של 750 מ׳ ושדרה היקפית עם שביל אופניים", "A 750 m running track and a perimeter boulevard with a bike path", "mako_0926", "mako_1125"),
        L("העבודות בכיכר ובטבעת ה׳ באייר צפויות להסתיים עד סוף 2027 (העירייה)", "The works in the square and on the ה' באייר ring are due by the end of 2027 (the municipality)", "mako_0926"),
    ],
    "pond": [
        L("אגם אקולוגי בעומק 1 מ׳", "An ecological pond 1 m deep", "mako_0926"),
        L("מוקף צמחייה רב-שנתית, עם תעלות זרימה, גשרים ושבילים", "Surrounded by perennial planting, with flow channels, bridges and paths", "mako_1125", "tlvonline"),
        L("המיקום והצורה בתמונה להמחשה בלבד: תוכנית האגם לא פורסמה", "Location and shape shown for illustration only: the pond's plan is not published"),
    ],
    "school": [
        L("בית ספר יסודי בחלק הצפוני של הכיכר, נפתח עם תחילת שנת הלימודים", "A primary school in the north of the square, opened with the start of the school year", "mako_0926"),
        L("מבנה בצורת מניפה עם שלוש קומות עליונות וגג ירוק פעיל", "A fan-shaped building with three upper floors and an active green roof", "tlvonline", "tlv_0821"),
        L("אולם ספורט תת-קרקעי, חצר פעילה ומגרש פתוח לציבור בשעות אחר הצהריים", "An underground sports hall, an active courtyard and a field open to the public in the afternoons", "tlvonline", "mako_1125"),
        L("18 כיתות ועוד 6 כיתות חינוך מיוחד · ה׳ באייר 75", "18 classes plus 6 special-education classes · 75 ה' באייר", "tlv_0821"),
    ],
    "centre": [
        L("מרכז קהילתי בחלק הדרומי של הכיכר: חמש קומות עם חדרי פעילות, אולמות הרצאות, סטודיו למחול, חדרי אמנות ואולם רב-תכליתי", "The community centre in the south of the square: five floors of activity rooms, lecture halls, a dance studio, art rooms and a multi-purpose hall", "mako_1125", "tlvonline"),
        L("בתכנון של 2021: 4 קומות (עד 7 בעתיד), משרד ניהול הפארק, שירותים ציבוריים ובית קפה של כ-60 מ״ר", "In the 2021 design: 4 floors (up to 7 later), the park's management office, public toilets and a café of about 60 m²", "tlv_0821"),
    ],
    "ring": [
        L("טבעת הבניינים של הכיכר נבנתה ברובה בתחילת שנות ה-70", "The square's ring of buildings was built mostly in the early 1970s", "wiki_en_sq"),
        L("בקומות הקרקע: חנויות אופנה ויוקרה", "On the ground floors: fashion and luxury shops", "wiki_en_sq"),
        L("תכנון: ישראל לוטן ואבא אלחנני, עם אוסקר נימאייר", "Designed by Israel Lotan and Abba Elhanani, with Oscar Niemeyer", "wiki_he_sq"),
    ],
    "road": [
        L("רחוב הטבעת ה׳ באייר מקיף את הכיכר", "The ring street ה' באייר circles the square", "wiki_he_sq"),
        L("שביל אופניים היקפי, מדרכות רחבות וארבעה מעברי חצייה חדשים", "A circular bike path, wider sidewalks and four new crossings", "ynetnews"),
    ],
    "square": [
        L("הכיכר הגדולה בישראל", "The largest square in Israel", "wiki_he_sq"),
        L("מגרש המגורים 101 (מגורים ד׳) ומגרש 303 לשטחים פתוחים ומבני ציבור", "Residential lot 101 and lot 303 for open space and public buildings", "tlv_837"),
    ],
}

model = {
    "fh": 4.0, "twist": 1.25, "twist_dir": -1, "slab_t": 0.45, "slab_out": 1.25, "plate": "superellipse", "plate_n": 4.5,
    "eye": "(floor - 1) x 4.0 m + 1.6 m",
    "notes": [
        L("גובה קומה 4.0 מ׳: הנחה זמנית (160 מ׳ חלקי 40 קומות); גובה הקומות לא פורסם", "Floor height 4.0 m: provisional (160 m / 40 floors); floor heights are not published", "tlv_513"),
        L("כיוון הסיבוב לא פורסם: כאן נגד כיוון השעון במבט מלמעלה", "The turn's direction is not published: shown counter-clockwise from above"),
        L("צורת הקומה להמחשה, בהשראת העיגול, בגודל קונטור הבניין במאגר העירייה; אין תוכנית קומה רשמית", "Floor-plate shape is an illustration, circle-inspired, sized to the municipal footprint; no official plan is public", "tlv_513", "mys"),
        L("הנסיגה בין הקומות לא פורסמה בכמות, ולכן אינה מוצגת", "The set-back between floors is not quantified, so it is not shown", "mys"),
        L("כתר הגג של מגדל B (מ-148 ל-157 מ׳) להמחשה", "Tower B's roof crown (148 to 157 m) is an illustration"),
    ],
}

# the park's features (coordinator, 30.9.2026, from Mako 24.9.2026 / 11.11.2025 and tlvonline 2.11.2025). No municipal layer
# places them inside the square, so every pin stands where it reads well and says "location for illustration".
def at(bearing, r):
    return round(math.sin(math.radians(bearing)) * r, 1), round(-math.cos(math.radians(bearing)) * r, 1)


PF = [
    ("dog", "גינת כלבים", "Dog garden", at(96, 102), [L("גינת כלבים בפארק החדש של הכיכר", "A dog garden in the square's new park", "mako_1125", "tlvonline", "ashtrom")]),
    ("play", "גן משחקים", "Playground", at(172, 100), [L("גן משחקים ומתקני משחק לילדים", "A playground with play equipment for children", "mako_1125", "tlvonline", "globes_1222")]),
    ("lawns", "מדשאות ושולחנות", "Lawns and tables", at(352, 100), [L("מדשאות, שולחנות משחק ופינות ישיבה", "Lawns, game tables and seating", "mako_1125", "tlvonline")]),
    ("bridges", "גשרים ושבילים", "Bridges and paths", at(70, 38), [L("שבילים, תעלות זרימה וגשרים סביב האגם", "Paths, flow channels and bridges around the pond", "mako_1125", "tlvonline")]),
    ("boulevard", "שדרה ושביל אופניים", "Boulevard and bike path", at(20, 121), [L("שדרה עירונית חדשה סביב הכיכר, עם שביל אופניים", "A new urban boulevard around the square, with a bike path", "mako_1125", "tlvonline")]),
    ("trees", "שלוש שורות עצים", "Three rows of trees", at(140, 121), [L("שלוש שורות עצים לאורך השדרה, כולל עצים ותיקים לשימור", "Three rows of trees along the boulevard, including heritage trees", "mako_1125", "globes_1222"),
                                                                      L("560 עצים חדשים ו-36 עצים ותיקים שנשמרו", "560 new trees and 36 mature trees kept", "mako_1125", "mako_0926")]),
    ("track", "מסלול ריצה 750 מ׳", "Running track, 750 m", at(248, 119), [L("מסלול ריצה באורך 750 מ׳", "A 750 m running track", "mako_0926")]),
    ("kiosks", "קיוסקים ופינות ישיבה", "Kiosks and seating", at(200, 112), [L("קיוסקים ופינות ישיבה מוצלות בפארק", "Kiosks and shaded seating in the park", "mako_1125", "tlvonline"),
                                                                           L("שלושה קיוסקים (2022) או ארבעה בתי קפה קטנים בתצורת קיוסק (2025)", "Three kiosks (2022) or four small cafés in kiosk form (2025)", "globes_1222", "globes_0925")]),
]
park_features = [{"key": k, "he": he, "en": en, "x": xy[0], "z": xy[1], "lines": lines, "illus": True} for k, he, en, xy, lines in PF]

civic = [
    {"key": "school", "block": civic_idx.get("school"), "he": "בית הספר כיכר המדינה", "en": "Kikar HaMedina school",
     "x": quarter["places"][0]["x"], "z": quarter["places"][0]["z"]},
    {"key": "centre", "block": civic_idx.get("centre"), "he": "המרכז הקהילתי", "en": "Community centre",
     "x": quarter["places"][1]["x"], "z": quarter["places"][1]["z"]},
]

block_vals = [v for rec in blocks for v in rec]
street_vals = [v for rec in streets for v in rec]
green_vals = [v for rec in greens for v in rec]
out = {
    "v": 2, "enc": "nlw2", "id": "hamedina", "generated_at": time.strftime("%Y-%m-%d"),
    "origin": {"lat": O[0], "lng": O[1]}, "frame": "x metres east, z metres south of the plot centre (three.js north = -z)",
    "radius": {"near": 700, "far": 2000},
    "names": names,
    "blocks": {"q": 0.1, "q_far": 0.5, "n": len(blocks), "near": n_near, "data": block_vals, "names": {str(k): v for k, v in block_names.items()}},
    "streets": {"q": 0.1, "n": len(streets), "data": street_vals},
    "greens": {"q": 0.5, "n": len(greens), "data": green_vals},
    "water": {"q": 1.0, "rings": water},
    "trees": {"q": 0.1, "n": len(trees), "data": b64_i16(tree_vals)},
    "ring": {"q": 0.1, "parts": ring_axes},
    "park": {"q": 0.1, "p": park},
    "pond": {"q": 0.1, "p": enc_ring(pond, 0.1), "area": pond_area, "illustration": True},
    "lots": {"q": 0.1, "list": lots},
    "towers": towers,
    "civic": civic,
    "park_features": park_features,
    "pins": pins,
    "marks": marks,
    "model": model,
    "facts": facts,
    "sources": S,
    "places_src": places_doc.get("src"),
    "src": {"buildings": cb["source"], "streets": "GIS 507/508", "greens": "GIS 503", "water": "GIS 504",
            "trees": "GIS 574 (tree canopies 2024)", "places": "places.json (findplace + OSM + city layers; Mapbox walking)"},
}
p = os.path.join(OUT, "world.json")
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print("wrote", p, os.path.getsize(p), "bytes")
shutil.copyfile(os.path.join(RES, "places.json"), os.path.join(OUT, "places.json"))
print("copied places.json", os.path.getsize(os.path.join(OUT, "places.json")), "bytes")
