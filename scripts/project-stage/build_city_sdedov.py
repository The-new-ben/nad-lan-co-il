# -*- coding: utf-8 -*-
"""The real city around a Sde Dov project for its 3D stage (prototypes, 28.9.2026): Dimri Yama (lot 107) and Ashira
(lot 101), next to Rainbow. The same approach as build_city_rainbow.py and build_city_duo.py: public, read-only GET
queries to the Tel Aviv-Yafo GIS (ArcGIS REST, IView2) and to our own pages' public REST; nothing is fetched at page time.

Frame (docs/research/2026-09-28-stages/stage-geometry.md, section 0.2): origin = the lot's centroid (GIS 837); e = (lng -
lng0) * cos(lat0) * 111320, n = (lat - lat0) * 110574; X = e, Z = -n; turned with the lots' grid, g = -11 degrees:
x = X cos g - Z sin g, z = X sin g + Z cos g (x = grid east, z = grid south).

Writes, next to the stage (plugins/nadlan-config/assets/project-stage/<dimri|ashira>/):
  city.json
    b      [[height_m, floors, year, x1, z1, ...], ...]  buildings standing today (GIS 513) within 750 m; left out:
           antennas, bus shelters, temporary structures, footprints under 25 m2, anything under 2.5 m, and whatever stands
           on the project's own lot or on one of our projects' lots (those are being built; the stage draws them).
    f      [cx, cz, w, d, angle_deg, h, ...]  the far city, 750 m to 1.5 km: each building of 6 m or more as its box.
    lots   [["lot" | "park", "105", x1, z1, ...], ...]  the lots of the Sde Dov plans (GIS 837: תמ"ל/3001, 4444) within
           900 m, the project's own lot left to the stage; open space and parks as "park", roads left out.
    g      [["name", x1, z1, ...], ...]  public green areas (GIS 503).
    s      [[width_m, "name", x1, z1, ...], ...]  street axes (GIS 507; the width a drawing class, as for DUO).
    t      [x1, z1, ...]  street and park trees (GIS 628) within 420 m.
    labels [["name", x, z], ...]  the named streets along the lot's edges (the nearest axis to each edge's middle).
    coast  {"x0", "k", "line"}  the waterline: "line" is the shore from OpenStreetMap's coastline (natural=coastline, a
           public read-only Overpass query), as its most landward point every 40 m along the grid (breakwaters and jetties
           left out), within 3 km north and south; x0/k a straight fit of it for the sea's shading. Without OSM, a fit
           through the sea edge of the city's beaches (GIS 579).
  quarter.json  our other project pages around it (public REST: developer, status, floors, units, position) and the
           places Rainbow's quarter already names (find-place: TLV OpenData + OSM, 8.2026), with the distance and the
           bearing from the project's main tower.

  python scripts/project-stage/build_city_sdedov.py dimri|ashira [--coast-json saved-coastline.json]"""
import io, json, math, os, re, sys, time, urllib.parse, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/%d/query"
UA = {"User-Agent": "Mozilla/5.0 NadLan-CITY/1.0"}
GRID = math.radians(-11)
R_B, R_F, R_T, R_L = 750.0, 1500.0, 420.0, 900.0
SKIP_TYPES = {"אנטנה", "תחנת אוטובוס", "מבנה ארעי"}

PROJECTS = {
    # research sections 1 and 2: the lot's centroid (GIS 837), its outline in the stage frame, the plan's lot number, and
    # the main tower's centre (the view, the beam and every distance start there)
    "dimri": {"id": 4745, "dir": "dimri", "origin": (32.104441, 34.784472), "lot": "107",
              "outline": [[53.5, -35.6], [53.9, 22.6], [51.7, 28.6], [48.4, 32.3], [44.0, 34.8], [39.1, 35.6], [-53.1, 35.9], [-53.3, -35.2]],
              "tower": (-30.9, 18.2),
              # the design decision (10.5.2023) names the streets the city's axis layer still numbers: Israel Galili on the
              # east (axis 2438), Yaakov Apter on the south (axis 2436); by the lot's edge index
              "edge_names": {0: "ישראל גלילי", 5: "יעקב אפטר"}},
    "ashira": {"id": 4744, "dir": "ashira", "origin": (32.105643, 34.787673), "lot": "101",
               "outline": [[57.9, 43.6], [-26.5, 44.0], [-51.8, -25.2], [-56.3, -43.2], [29.8, -43.7], [33.7, -27.0], [42.5, 2.9]],
               "tower": (-15.7, 21.5),
               # the committee agenda (3.5.2023): Levi Eshkol on the east; road no. 14, a new street, on the west (no name yet)
               "edge_names": {4: "לוי אשכול", 5: "לוי אשכול", 6: "לוי אשכול"}},
}
# our pages in and around the quarter (the same list as build_quarter_rainbow.py, with Rainbow itself); the short name a
# buyer says. Rainbow's page meta holds no floor count: its own facts give the tower's 39 floors and 459 homes (the
# developer's reports), and its tower point (the stage's view point) is used instead of the lot's centre.
QPROJ = [
    (4464, "ריינבו", "RAINBOW"), (4745, "דמרי ימה", "DIMRI YAMA"), (4747, "זוהי", "ZOHI"), (4750, "שיכון ובינוי, מגרש 109", ""),
    (4749, "אוטופיה", "UTOPIA"), (4744, "אשירה", "ASHIRA"), (4748, "גינדי ווג", "GINDI VOGUE"), (4867, "מגדל איינשטיין", "EINSTEIN TOWER"),
    (4743, "פירסט", "FIRST"),
]
RAINBOW_FIX = {"lat": 32.10354, "lng": 34.78466, "floors": 39, "units": 459}
STATUS = {"permits": "בהליכי היתר", "construction": "בבנייה", "marketing": "בשיווק", "planning": "בתכנון", "presale": "בשיווק מוקדם"}
PHASE = {"בבנייה": "building", "בשיווק": "selling", "בשיווק מוקדם": "selling", "בהיתר בנייה": "permit", "בהליכי היתר": "permit", "בתכנון": "permit"}
SRC_ATLAS = "find-place, נתוני עיריית תל אביב-יפו ו-OpenStreetMap, 8.2026"
PLACES = [  # Rainbow's quarter.json places (build_quarter_rainbow.py), the same points and words
    ("rail", "תחנת רידינג, הרכבת הקלה", 32.0994035, 34.7822364, "מאושרת, עוד לא פועלת", SRC_ATLAS),
    ("school", "בית הספר כוכב הצפון", 32.101408, 34.786443, "קיים", SRC_ATLAS),
    ("park", "גן כוכב הצפון", 32.102028, 34.785529, "קיים", SRC_ATLAS),
    ("beach", "חוף רידינג", 32.10711, 34.77681, "קיים", SRC_ATLAS),
    ("nature", "שפך נחל הירקון", 32.098806, 34.778214, "קיים", SRC_ATLAS),
]
# the city layer writes a street "surname first name"; the stage writes it the way it is said
SAY = {"אפטר יעקב": "יעקב אפטר", "גלילי ישראל": "ישראל גלילי", "אשכול לוי": "לוי אשכול", "לביטוב זהרה": "זהרה לביטוב",
       "עגנון ש\"י": "ש\"י עגנון", "קובנר אבא": "אבא קובנר", "זאבי רחבעם (גנדי)": "רחבעם זאבי", "שטרן אייזק": "אייזק שטרן"}


def get(layer, **kw):
    p = {"f": "json"}
    p.update(kw)
    url = BASE % layer + "?" + urllib.parse.urlencode(p)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if attempt == 3:
                raise
            time.sleep(4)


def main():
    key = sys.argv[1] if len(sys.argv) > 1 else ""
    if key not in PROJECTS:
        sys.exit("usage: build_city_sdedov.py " + "|".join(PROJECTS))
    P = PROJECTS[key]
    O = P["origin"]
    LOT = P["outline"]
    DIR = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", P["dir"])
    os.makedirs(DIR, exist_ok=True)

    def envelope(radius):
        dlat = radius / 110574.0
        dlng = radius / (math.cos(math.radians(O[0])) * 111320.0)
        return "%.6f,%.6f,%.6f,%.6f" % (O[1] - dlng, O[0] - dlat, O[1] + dlng, O[0] + dlat)

    def fetch_all(layer, radius, fields, where="1=1"):
        out, off = [], 0
        while True:
            d = get(layer, where=where, geometry=envelope(radius), geometryType="esriGeometryEnvelope", inSR=4326,
                    spatialRel="esriSpatialRelIntersects", outFields=fields, returnGeometry="true", outSR=4326,
                    resultOffset=off, resultRecordCount=1000)
            feats = d.get("features") or []
            out += feats
            if not feats or not d.get("exceededTransferLimit"):
                break
            off += len(feats)
        return out

    def local(lng, lat):
        e = (lng - O[1]) * math.cos(math.radians(O[0])) * 111320.0
        n = (lat - O[0]) * 110574.0
        X, Z = e, -n
        c, s = math.cos(GRID), math.sin(GRID)
        return (X * c - Z * s, X * s + Z * c)

    def to_latlng(x, z):
        c, s = math.cos(-GRID), math.sin(-GRID)
        X, Z = x * c - z * s, x * s + z * c
        return (O[0] + (-Z) / 110574.0, O[1] + X / (math.cos(math.radians(O[0])) * 111320.0))

    def world(x, z):
        c, s = math.cos(-GRID), math.sin(-GRID)
        return round(x * c - z * s, 1), round(x * s + z * c, 1)

    def from_tower(x, z):
        tx, tz = P["tower"]
        c, s = math.cos(-GRID), math.sin(-GRID)
        X, Z = (x - tx) * c - (z - tz) * s, (x - tx) * s + (z - tz) * c
        return round(math.hypot(X, Z)), round((math.degrees(math.atan2(X, -Z)) + 360) % 360, 1)

    # ---------------- our projects (REST, read only) ----------------
    ours = []
    for pid, short, brand in QPROJ:
        u = "https://nad-lan.co.il/wp-json/wp/v2/nadlan_project/%d?_fields=id,link,meta&nlq=%d" % (pid, int(time.time()))
        with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
            d = json.loads(r.read().decode("utf-8"))
        m = d.get("meta") or {}
        lat, lng = float(m.get("lat") or 0), float(m.get("lng") or 0)
        floors, units = int(m.get("num_floors") or 0), int(m.get("num_units") or 0)
        if pid == 4464:
            lat, lng, floors, units = RAINBOW_FIX["lat"], RAINBOW_FIX["lng"], RAINBOW_FIX["floors"], RAINBOW_FIX["units"]
        if not (lat and lng):
            continue
        x, z = local(lng, lat)
        st = (m.get("project_status") or "").strip()
        st = STATUS.get(st.lower(), st)
        ours.append({"pid": pid, "short": short, "brand": brand, "x": x, "z": z, "floors": floors, "units": units, "status": st,
                     "developer": re.sub(r"\bנדלן\b", "נדל״ן", (m.get("developer_name") or "").strip().replace("׳", "'")),
                     "url": d.get("link"), "year": int(m.get("completion_year") or 0)})

    def inside(p, poly):
        x, z = p
        c = False
        for i in range(len(poly)):
            a, b = poly[i], poly[i - 1]
            if (a[1] > z) != (b[1] > z) and x < (b[0] - a[0]) * (z - a[1]) / (b[1] - a[1]) + a[0]:
                c = not c
        return c

    def area(Q):
        return sum(Q[i][0] * Q[(i + 1) % len(Q)][1] - Q[(i + 1) % len(Q)][0] * Q[i][1] for i in range(len(Q))) / 2

    def seg_dist(p, a, b):
        ax, az = b[0] - a[0], b[1] - a[1]
        L = ax * ax + az * az
        t = 0 if L == 0 else max(0, min(1, ((p[0] - a[0]) * ax + (p[1] - a[1]) * az) / L))
        return math.hypot(p[0] - a[0] - t * ax, p[1] - a[1] - t * az), (a[0] + t * ax, a[1] + t * az)

    def dp_open(pts, tol):
        if len(pts) < 3:
            return pts
        i, d = max(((i, seg_dist(pts[i], pts[0], pts[-1])[0]) for i in range(1, len(pts) - 1)), key=lambda t: t[1])
        if d <= tol:
            return [pts[0], pts[-1]]
        return dp_open(pts[: i + 1], tol)[:-1] + dp_open(pts[i:], tol)

    def simplify(Q, tol):
        if len(Q) <= 4:
            return Q
        far = max(range(len(Q)), key=lambda i: math.hypot(Q[i][0] - Q[0][0], Q[i][1] - Q[0][1]))
        a = dp_open(Q[: far + 1], tol)
        b = dp_open(Q[far:] + [Q[0]], tol)
        out = a[:-1] + b[:-1]
        return out if len(out) >= 3 else Q

    def flat(Q):
        f = []
        for x, z in Q:
            f += [round(x, 1), round(z, 1)]
        return f

    def obb(Q):
        best = None
        for i in range(len(Q)):
            a, b = Q[i], Q[(i + 1) % len(Q)]
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            c, s = math.cos(-ang), math.sin(-ang)
            us = [x * c - z * s for x, z in Q]
            vs = [x * s + z * c for x, z in Q]
            ar = (max(us) - min(us)) * (max(vs) - min(vs))
            if best is None or ar < best[0]:
                u0, v0 = (max(us) + min(us)) / 2, (max(vs) + min(vs)) / 2
                c2, s2 = math.cos(ang), math.sin(ang)
                best = (ar, u0 * c2 - v0 * s2, u0 * s2 + v0 * c2, max(us) - min(us), max(vs) - min(vs), ang)
        _, cx, cz, w, d, ang = best
        return [round(cx), round(cz), round(w, 1), round(d, 1), round(math.degrees(ang) % 180)]

    # ---------------- the Sde Dov plans' lots (GIS 837) ----------------
    lots, lotpolys, own = [], [], None
    for f in fetch_all(837, R_L, "st_mispar_migrash_betaba,st_taba,t_yeud_karka"):
        a = f["attributes"]
        plan = (a.get("st_taba") or "").strip()
        use = a.get("t_yeud_karka") or ""
        if not ("3001" in plan or "4444" in plan):
            continue
        num = (a.get("st_mispar_migrash_betaba") or "").strip()
        rings = (f.get("geometry") or {}).get("rings") or []
        if not rings:
            continue
        Q = [local(lng, lat) for lng, lat in rings[0][:-1]]
        if len(Q) < 3:
            continue
        Q = simplify(Q, 0.35)
        if area(Q) < 0:
            Q = Q[::-1]
        cx, cz = sum(p[0] for p in Q) / len(Q), sum(p[1] for p in Q) / len(Q)
        if "3001" in plan and num == P["lot"] and inside((0, 0), Q):
            own = Q
            continue
        if "דרך" in use or "מסילה" in use:
            continue
        kind = "park" if (("פתוח" in use or "פארק" in use or "גן" in use or "כיכר" in use) and "מבנים" not in use) else "lot"
        lots.append([kind, num] + flat(Q))
        lotpolys.append(Q)
    # the lots our other projects stand on: their buildings are drawn as schematic masses, not the city's layer
    our_lots = []
    for q in ours:
        for Q in lotpolys:
            if inside((q["x"], q["z"]), Q):
                our_lots.append(Q)
                break

    # ---------------- buildings (GIS 513) ----------------
    feats = fetch_all(513, R_F, "oid_mivne,ms_komot,t_sug_mivne,gova_simplex_2019,min_height,max_height,year")
    kept, far, why, seen = [], [], {"type": 0, "small": 0, "low": 0, "own": 0, "ours": 0, "far": 0}, set()
    for f in feats:
        a = f.get("attributes") or {}
        if a.get("oid_mivne") in seen:
            continue
        seen.add(a.get("oid_mivne"))
        if (a.get("t_sug_mivne") or "").strip() in SKIP_TYPES:
            why["type"] += 1
            continue
        h = a.get("gova_simplex_2019") or 0
        if not h and a.get("max_height") and a.get("min_height"):
            h = a["max_height"] - a["min_height"]
        if not h and a.get("ms_komot"):
            h = a["ms_komot"] * 3.2
        if h < 2.5:
            why["low"] += 1
            continue
        rings = (f.get("geometry") or {}).get("rings") or []
        if not rings:
            continue
        ring = rings[0][:-1] if rings[0][0] == rings[0][-1] else rings[0]
        Q = [local(lng, lat) for lng, lat in ring]
        if len(Q) < 3 or abs(area(Q)) < 25:
            why["small"] += 1
            continue
        cx, cz = sum(p[0] for p in Q) / len(Q), sum(p[1] for p in Q) / len(Q)
        dc = math.hypot(cx, cz)
        if dc > R_F:
            continue
        if inside((cx, cz), LOT):
            why["own"] += 1
            continue
        if any(inside((cx, cz), L) for L in our_lots):
            why["ours"] += 1
            continue
        if dc > R_B:
            if h >= 6:
                far.append(obb(Q) + [round(h)])
            why["far"] += 1
            continue
        Q = simplify(Q, 0.6)
        if area(Q) < 0:
            Q = Q[::-1]
        kept.append([round(h * 2) / 2, int(a.get("ms_komot") or 0), int(a.get("year") or 0)] + flat(Q))
    kept.sort(key=lambda b: (b[3], b[4]))

    # ---------------- green areas, streets, trees ----------------
    greens = []
    for f in fetch_all(503, R_B, "shem_gan"):
        rings = (f.get("geometry") or {}).get("rings") or []
        if not rings:
            continue
        Q = [local(lng, lat) for lng, lat in rings[0][:-1]]
        if len(Q) < 3 or abs(area(Q)) < 40 or min(math.hypot(x, z) for x, z in Q) > R_B:
            continue
        Q = simplify(Q, 0.8)
        if area(Q) < 0:
            Q = Q[::-1]
        greens.append([(f["attributes"].get("shem_gan") or "").strip()] + flat(Q))
    mains = set((f["attributes"].get("t_rechov") or "").strip() for f in fetch_all(508, R_B + 200, "t_rechov"))
    streets, axes = [], {}
    for f in fetch_all(507, R_B + 150, "t_rechov,t_sug,k_reka"):
        a = f["attributes"]
        name = (a.get("t_rechov") or "").strip()
        sug = (a.get("t_sug") or "").strip()
        k = int(a.get("k_reka") or 0)
        w = 5 if (sug in ("שביל", "סמטת") or k in (0, 50)) else (24 if sug == "שדרות" else (20 if (k == 200 or name in mains) else 10))
        for path in ((f.get("geometry") or {}).get("paths") or []):
            Q = [local(lng, lat) for lng, lat in path]
            if min(math.hypot(x, z) for x, z in Q) > R_B + 100:
                continue
            Q = dp_open(Q, 0.5)
            streets.append([w, name] + flat(Q))
            axes.setdefault(name, []).append(Q)
    trees = []
    for f in fetch_all(628, R_T, "oid"):
        g = f.get("geometry") or {}
        if "x" not in g:
            continue
        x, z = local(g["x"], g["y"])
        if math.hypot(x, z) > R_T or inside((x, z), LOT) or any(inside((x, z), L) for L in our_lots):
            continue
        trees += [round(x, 1), round(z, 1)]

    # ---------------- the coast (the sea edge of the city's beaches) ----------------
    d = get(579, where="1=1", geometry="%.4f,%.4f,%.4f,%.4f" % (O[1] - 0.05, O[0] - 0.035, O[1] + 0.005, O[0] + 0.035),
            geometryType="esriGeometryEnvelope", inSR=4326, spatialRel="esriSpatialRelIntersects", outFields="beach_name",
            returnGeometry="true", outSR=4326)
    edge = []
    for f in d.get("features") or []:
        Q = [local(lng, lat) for lng, lat in f["geometry"]["rings"][0]]
        w = min(Q, key=lambda p: p[0])
        if -2600 <= w[1] <= 2600:
            edge.append((w[1], w[0], f["attributes"].get("beach_name")))
    n = len(edge)
    mz = sum(e[0] for e in edge) / n
    mx = sum(e[1] for e in edge) / n
    k = sum((e[0] - mz) * (e[1] - mx) for e in edge) / sum((e[0] - mz) ** 2 for e in edge)
    coast = {"x0": round(mx - k * mz, 1), "k": round(k, 4), "beaches": [e[2] for e in edge]}

    # the shore itself, from OpenStreetMap's coastline (read only), where the mirror answers
    osm = []
    if "--coast-json" in sys.argv:  # a saved answer of the same query: [[lat, lng], ...]
        osm = [local(lng, lat) for lat, lng in json.load(io.open(sys.argv[sys.argv.index("--coast-json") + 1], encoding="utf-8"))]
    q = '[out:json][timeout:50];way["natural"="coastline"](%.4f,%.4f,%.4f,%.4f);out geom;' % (O[0] - 0.03, O[1] - 0.04, O[0] + 0.03, O[1] + 0.005)
    for host in (() if osm else ("https://maps.mail.ru/osm/tools/overpass/api/interpreter", "https://overpass-api.de/api/interpreter")):
        try:
            with urllib.request.urlopen(urllib.request.Request(host + "?data=" + urllib.parse.quote(q), headers=UA), timeout=90) as r:
                osm = [local(nd["lon"], nd["lat"]) for w in json.loads(r.read().decode("utf-8"))["elements"] for nd in w.get("geometry", [])]
            if osm:
                break
        except Exception as e:
            print("  overpass", host, e)
    if osm:
        prof = {}
        for x, z in osm:
            b = int(round(z / 40.0))
            if abs(b * 40) <= 3000:
                prof[b] = max(prof.get(b, -1e9), x)
        bins = sorted(prof)
        line = []
        for b in range(bins[0], bins[-1] + 1):
            if b in prof:
                line.append([round(prof[b], 1), b * 40])
            else:  # a bin without a coastline node: between its neighbours
                lo = max(c for c in bins if c < b); hi = min(c for c in bins if c > b)
                t = (b - lo) / (hi - lo)
                line.append([round(prof[lo] + (prof[hi] - prof[lo]) * t, 1), b * 40])
        nz = [p for p in line if abs(p[1]) <= 1400]
        mzz = sum(p[1] for p in nz) / len(nz); mxx = sum(p[0] for p in nz) / len(nz)
        kk = sum((p[1] - mzz) * (p[0] - mxx) for p in nz) / sum((p[1] - mzz) ** 2 for p in nz)
        near = min(osm, key=lambda p: math.hypot(*p))
        coast = {"x0": round(mxx - kk * mzz, 1), "k": round(kk, 4), "line": line, "nearest_m": round(math.hypot(*near)),
                 "src": "OpenStreetMap, natural=coastline, " + time.strftime("%#d.%#m.%Y" if os.name == "nt" else "%-d.%-m.%Y")}

    # ---------------- labels: the named streets along the lot's edges ----------------
    labels, named = [], set()
    for i in range(len(LOT)):
        a, b = LOT[i], LOT[(i + 1) % len(LOT)]
        if math.hypot(b[0] - a[0], b[1] - a[1]) < 25:
            continue
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        best = (1e9, None, None)
        for name, paths in axes.items():
            if not name or re.fullmatch(r"[\d\s]+", name):
                continue
            for Q in paths:
                for j in range(len(Q) - 1):
                    dd, qp = seg_dist(mid, Q[j], Q[j + 1])
                    if dd < best[0]:
                        best = (dd, name, qp)
        # the nearest axis of any name (a new street may still carry a number in the city's layer)
        anyb = (1e9, None, None)
        for name, paths in axes.items():
            for Q in paths:
                for j in range(len(Q) - 1):
                    dd, qp = seg_dist(mid, Q[j], Q[j + 1])
                    if dd < anyb[0]:
                        anyb = (dd, name, qp)
        plan_name = P.get("edge_names", {}).get(i)
        if anyb[0] < 32 and re.fullmatch(r"[\d\s]+", anyb[1] or "") and plan_name and plan_name not in named:
            named.add(plan_name)
            labels.append([plan_name, round(anyb[2][0], 1), round(anyb[2][1], 1)])
        elif best[0] < 32 and SAY.get(best[1], best[1]) not in named:
            named.add(SAY.get(best[1], best[1]))
            labels.append([SAY.get(best[1], best[1]), round(best[2][0], 1), round(best[2][1], 1)])

    out = {"v": 1, "generated_at": time.strftime("%Y-%m-%d"),
           "source": "עיריית תל אביב-יפו: שכבות המבנים (513), המגרשים (837), הרחובות (507, 508), השטחים הירוקים (503), העצים (628) והחופים (579), " + time.strftime("%#m.%Y" if os.name == "nt" else "%-m.%Y"),
           "note": "הבניינים הקיימים היום לפי שכבת המבנים של העירייה; מגרשי תכנית רובע שדה דב לפי שכבת המגרשים. רוחב הרחובות בציור להמחשה; הצירים לפי העירייה.",
           "origin": {"lat": O[0], "lng": O[1], "grid_deg": 11},
           "b": kept, "f": [v for b in far for v in b], "lots": lots, "g": greens, "s": streets, "t": trees, "labels": labels, "coast": coast}
    io.open(os.path.join(DIR, "city.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print(key, "| buildings", len(kept), "| far", len(far), "| left out", why)
    print("  lots", len(lots), "| own lot found", own is not None, "| greens", len(greens), "| streets", len(streets), "| trees", len(trees) // 2)
    print("  coast x = %.1f + %.4f z" % (coast["x0"], coast["k"]), "| OSM line points", len(coast.get("line") or []), "| nearest", coast.get("nearest_m"), "| beaches fit", n)
    print("  labels", labels)
    print("  city.json", os.path.getsize(os.path.join(DIR, "city.json")), "bytes")

    # ---------------- quarter.json ----------------
    tlat, tlng = to_latlng(*P["tower"])
    q = {"generated_at": time.strftime("%Y-%m-%d"), "origin": {"lat": O[0], "lng": O[1]},
         "tower": {"lat": round(tlat, 6), "lng": round(tlng, 6), "note": "the main tower's centre (research file, DRAWING grade)"},
         "note": "מסה סכמטית לפי מספר הקומות בעמוד הפרויקט; המיקום לפי המגרש. הדמיה להמחשה בלבד.", "projects": [], "places": []}
    for o in ours:
        if o["pid"] == P["id"]:
            continue
        dist, brg = from_tower(o["x"], o["z"])
        wx, wz = world(o["x"], o["z"])
        item = {"id": o["pid"], "kind": "project", "name": o["short"], "pin": o["short"].split(",")[0].strip(), "brand": o["brand"],
                "developer": o["developer"], "status": o["status"], "floors": o["floors"] or None, "units": o["units"] or None,
                "url": o["url"], "x": wx, "z": wz, "dist": dist, "bearing": brg, "source": "עמוד הפרויקט באתר",
                "phase": PHASE.get(o["status"], "permit")}
        if o["year"] > 2000:
            item["occupancy"] = o["year"]
        q["projects"].append(item)
    for kind, name, lat, lng, status, src in PLACES:
        x, z = local(lng, lat)
        dist, brg = from_tower(x, z)
        wx, wz = world(x, z)
        q["places"].append({"kind": kind, "name": name, "pin": name.split(",")[0].strip(), "status": status, "x": wx, "z": wz,
                            "dist": dist, "bearing": brg, "walk": max(1, round(dist * 1.25 / 80)), "source": src})
    io.open(os.path.join(DIR, "quarter.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(q, ensure_ascii=False, indent=1))
    print("  quarter:", [(p["name"], p["dist"], p["bearing"], p["floors"], p["phase"]) for p in q["projects"]])
    print("  places:", [(p["name"], p["dist"], p["bearing"]) for p in q["places"]])
    print("  the tower's point", round(tlat, 6), round(tlng, 6))


if __name__ == "__main__":
    main()
