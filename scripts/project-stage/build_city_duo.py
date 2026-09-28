# -*- coding: utf-8 -*-
"""The real city around DUO Tel Aviv for its 3D stage (prototype, 28.9.2026), built the way build_city_rainbow.py builds
Rainbow's: public, read-only GET queries to the Tel Aviv-Yafo GIS (ArcGIS REST, IView2), nothing fetched at page time.

Frame (docs/research/2026-09-28-stages/stage-geometry.md, section 0.2 and 3): origin = the area-weighted centroid of lots
111 + 112 (GIS 837), 32.085698, 34.782856; e = (lng - lng0) * cos(lat0) * 111320, n = (lat - lat0) * 110574; X = e, Z = -n,
turned with the grid by g = -10 degrees: x = X cos g - Z sin g, z = X sin g + Z cos g. So x = grid east, z = grid south.

Outputs (next to the stage, plugins/nadlan-config/assets/project-stage/duo/):
  city.json
    f      [cx, cz, w, d, angle_deg, height_m, ...]  the far city, 750 m to 1.5 km (to the sea): each building of GIS 513 at
           least 6 m high as its smallest enclosing box, turned to its footprint, at its height (same height rule as b).
    b      [[height_m, floors, year, x1, z1, x2, z2, ...], ...]  buildings standing today (GIS 513 "מבנים"), within about
           750 m. Left out: antennas, bus shelters and temporary structures, footprints under 25 m2, anything lower than
           2.5 m, and whatever stands on DUO's own lots 111 + 112 (the stage draws DUO itself). Heights: the city's 2019
           survey height, else roof minus base, else floors x 3.2 m. The new municipality tower (oid 40141, 25 floors, 2024)
           has no surveyed height: floors x 3.2 m.
    lots   [["lot" | "park", "124", x1, z1, ...], ...]  the Somail plans' lots around DUO (GIS 837: plans 2988א, 2988ב, 4067),
           DUO's own 111 and 112 left to the stage; open space ("שטח ציבורי פתוח") as park.
    g      [["name", x1, z1, ...], ...]  public green areas (GIS 503 "שטחים ירוקים").
    s      [[width_m, "name", x1, z1, ...], ...]  street axes (GIS 507 "צירי רחוב"); the width is a drawing class by the
           layer's own road class (k_reka 200 and the main-street layer 508: 20 m; boulevards 24 m; other streets 10 m;
           lanes and paths 5 m). The widths are an illustration, the axes are the city's.
    t      [x1, z1, x2, z2, ...]  street and park trees (GIS 628 "עצים") within about 420 m: real positions, drawn as one
           generic crown (the species' size is not drawn).
    labels [["name", x, z], ...]  where the stage writes the streets around the lot: the nearest point of each street's
           axis to the lot, and the open space to the north (plan 4067).
    coast  {"x0", "k"}  the waterline in the stage frame, x = x0 + k * z, a straight fit through the west (sea) edge of the
           city's beach polygons (GIS 579 "חופים") from Metzitzim to Jerusalem beach.
  quarter.json   the quarter's pins (design system QuarterPins, like rainbow/quarter.json): our project page nearby
           (H Infinity, public REST read) and places from the city's layers, with x/z from the origin and the distance
           and bearing from the middle point between DUO's two towers.

  python scripts/project-stage/build_city_duo.py"""
import io, json, math, os, sys, time, urllib.parse, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "duo")
BASE = "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/%d/query"
UA = {"User-Agent": "Mozilla/5.0 NadLan-CITY/1.0"}
ORIGIN = (32.085698, 34.782856)          # lots 111 + 112, area-weighted centroid (research 3.1)
GRID = math.radians(-10)
R_B = 750.0                              # buildings radius (m): full footprints
R_F = 1500.0                             # the far city (m): each building as its oriented box, to the sea
R_T = 420.0                              # trees radius (m)
SKIP_TYPES = {"אנטנה", "תחנת אוטובוס", "מבנה ארעי"}
# DUO's lot outline in the stage frame (research 3.2): whatever stands inside is DUO itself
LOT = [[-42.3, -48.5], [44.5, -49.0], [44.6, -5.8], [40.0, -5.7], [40.0, 1.7], [39.7, 37.2], [39.3, 41.0], [37.9, 44.5],
       [34.6, 48.4], [32.6, 50.0], [28.1, 51.8], [25.7, 52.1], [-41.9, 48.6], [-42.1, 2.2]]
# the two towers' centres (GIS 513 oids 44499 and 42941, research 3.3): the view point for distances is between them
TOWERS_MID = (16.7, 1.6)


def get(layer, **kw):
    p = {"f": "json"}
    p.update(kw)
    url = BASE % layer + "?" + urllib.parse.urlencode(p)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # a slow city server: try again
            if attempt == 2:
                raise
            time.sleep(3)


def envelope(radius):
    dlat = radius / 110574.0
    dlng = radius / (math.cos(math.radians(ORIGIN[0])) * 111320.0)
    return "%.6f,%.6f,%.6f,%.6f" % (ORIGIN[1] - dlng, ORIGIN[0] - dlat, ORIGIN[1] + dlng, ORIGIN[0] + dlat)


def fetch_all(layer, radius, fields, where="1=1"):
    """Every feature in the envelope, page by page (resultOffset); the city's layers allow 2,000 per page."""
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
    e = (lng - ORIGIN[1]) * math.cos(math.radians(ORIGIN[0])) * 111320.0
    n = (lat - ORIGIN[0]) * 110574.0
    X, Z = e, -n
    c, s = math.cos(GRID), math.sin(GRID)
    return (X * c - Z * s, X * s + Z * c)


def to_latlng(x, z):
    c, s = math.cos(-GRID), math.sin(-GRID)
    X, Z = x * c - z * s, x * s + z * c
    return (ORIGIN[0] + (-Z) / 110574.0, ORIGIN[1] + X / (math.cos(math.radians(ORIGIN[0])) * 111320.0))


def area(P):
    return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))) / 2


def inside(p, P):
    x, z = p
    c = False
    for i in range(len(P)):
        a, b = P[i], P[i - 1]
        if (a[1] > z) != (b[1] > z) and x < (b[0] - a[0]) * (z - a[1]) / (b[1] - a[1]) + a[0]:
            c = not c
    return c


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


def simplify_ring(P, tol):
    if len(P) <= 4:
        return P
    far = max(range(len(P)), key=lambda i: math.hypot(P[i][0] - P[0][0], P[i][1] - P[0][1]))
    a = dp_open(P[: far + 1], tol)
    b = dp_open(P[far:] + [P[0]], tol)
    out = a[:-1] + b[:-1]
    return out if len(out) >= 3 else P


def obb(P):
    """The smallest rectangle around a footprint (its edges' directions tried in turn): [cx, cz, w, d, angle_deg]."""
    best = None
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        c, s = math.cos(-ang), math.sin(-ang)
        us = [x * c - z * s for x, z in P]
        vs = [x * s + z * c for x, z in P]
        ar = (max(us) - min(us)) * (max(vs) - min(vs))
        if best is None or ar < best[0]:
            u0, v0 = (max(us) + min(us)) / 2, (max(vs) + min(vs)) / 2
            c2, s2 = math.cos(ang), math.sin(ang)
            best = (ar, u0 * c2 - v0 * s2, u0 * s2 + v0 * c2, max(us) - min(us), max(vs) - min(vs), ang)
    _, cx, cz, w, d, ang = best
    return [round(cx), round(cz), round(w, 1), round(d, 1), round(math.degrees(ang) % 180)]


def flat(P):
    f = []
    for x, z in P:
        f += [round(x, 1), round(z, 1)]
    return f


def rings_of(g):
    if "rings" in g:
        return g["rings"]
    return []


def main():
    os.makedirs(DIR, exist_ok=True)
    # ---------------- buildings (GIS 513) ----------------
    feats = fetch_all(513, R_F, "oid_mivne,ms_komot,t_sug_mivne,gova_simplex_2019,min_height,max_height,year,shem_mivne")
    kept, far, why, seen = [], [], {"type": 0, "small": 0, "low": 0, "duo": 0, "far": 0, "dup": 0}, set()
    named = {}
    for f in feats:
        a = f.get("attributes") or {}
        oid = a.get("oid_mivne")
        if oid in seen:
            why["dup"] += 1
            continue
        seen.add(oid)
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
        for ring in rings_of(f.get("geometry") or {})[:1]:
            if len(ring) > 1 and ring[0] == ring[-1]:
                ring = ring[:-1]
            P = [local(lng, lat) for lng, lat in ring]
            if len(P) < 3 or abs(area(P)) < 25:
                why["small"] += 1
                continue
            cx = sum(p[0] for p in P) / len(P)
            cz = sum(p[1] for p in P) / len(P)
            dc = math.hypot(cx, cz)
            if dc > R_F:
                continue
            if dc > R_B:
                if h >= 6:
                    far.append(obb(P) + [round(h)])
                why["far"] += 1
                continue
            if inside((cx, cz), LOT) or sum(1 for p in P if inside(p, LOT)) > len(P) // 2:
                why["duo"] += 1
                continue
            P = simplify_ring(P, 0.6)
            if area(P) < 0:
                P = P[::-1]
            kept.append([round(h * 2) / 2, int(a.get("ms_komot") or 0), int(a.get("year") or 0)] + flat(P))
            if oid == 40141:
                named["municipality"] = (cx, cz, int(a.get("ms_komot") or 0), round(h, 1))
    kept.sort(key=lambda b: (b[3], b[4]))
    # ---------------- lots of the Somail plans (GIS 837) ----------------
    lots, lotc = [], {}
    d = get(837, where="st_taba LIKE '2988%' OR st_taba LIKE '4067%'", geometry=envelope(420), geometryType="esriGeometryEnvelope",
            inSR=4326, spatialRel="esriSpatialRelIntersects", outFields="st_mispar_migrash_betaba,st_taba,t_yeud_karka",
            returnGeometry="true", outSR=4326)
    for f in d.get("features") or []:
        a = f["attributes"]
        num = (a.get("st_mispar_migrash_betaba") or "").strip()
        plan = (a.get("st_taba") or "").strip()
        if plan.startswith("2988") and num in ("111", "112"):
            continue
        if "דרך" in (a.get("t_yeud_karka") or ""):   # the plans' road lots are streets: the street axes draw them
            continue
        for ring in rings_of(f["geometry"])[:1]:
            P = [local(lng, lat) for lng, lat in ring[:-1]]
            if len(P) < 3:
                continue
            P = simplify_ring(P, 0.35)
            if area(P) < 0:
                P = P[::-1]
            kind = "park" if "פתוח" in (a.get("t_yeud_karka") or "") and "מבנים" not in (a.get("t_yeud_karka") or "") else "lot"
            lots.append([kind, num] + flat(P))
            lotc[(plan, num)] = (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P), P)
    # ---------------- green areas (GIS 503) ----------------
    greens = []
    for f in fetch_all(503, R_B, "shem_gan,sug_gan"):
        a = f["attributes"]
        for ring in rings_of(f["geometry"])[:1]:
            P = [local(lng, lat) for lng, lat in ring[:-1]]
            if len(P) < 3 or abs(area(P)) < 40:
                continue
            if min(math.hypot(x, z) for x, z in P) > R_B:
                continue
            P = simplify_ring(P, 0.8)
            if area(P) < 0:
                P = P[::-1]
            greens.append([(a.get("shem_gan") or "").strip()] + flat(P))
    # ---------------- street axes (GIS 507, with the main-street layer 508) ----------------
    mains = set()
    for f in fetch_all(508, R_B + 200, "t_rechov"):
        mains.add((f["attributes"].get("t_rechov") or "").strip())
    streets, axes = [], {}
    for f in fetch_all(507, R_B + 150, "t_rechov,t_sug,k_reka"):
        a = f["attributes"]
        name = (a.get("t_rechov") or "").strip()
        sug = (a.get("t_sug") or "").strip()
        k = int(a.get("k_reka") or 0)
        if sug in ("שביל", "סמטת") or k in (0, 50):
            w = 5
        elif sug == "שדרות":
            w = 24
        elif k == 200 or name in mains:
            w = 20
        else:
            w = 10
        for path in (f["geometry"].get("paths") or []):
            P = [local(lng, lat) for lng, lat in path]
            if min(math.hypot(x, z) for x, z in P) > R_B + 100:
                continue
            P = dp_open(P, 0.5)
            streets.append([w, name] + flat(P))
            axes.setdefault(name, []).append(P)
    # ---------------- trees (GIS 628) ----------------
    trees = []
    for f in fetch_all(628, R_T, "oid"):
        g = f.get("geometry") or {}
        if "x" not in g:
            continue
        x, z = local(g["x"], g["y"])
        if math.hypot(x, z) > R_T or inside((x, z), LOT):
            continue
        trees += [round(x, 1), round(z, 1)]
    # ---------------- the coast (GIS 579 beaches: the sea edge of each) ----------------
    d = get(579, where="1=1", geometry="34.740,32.055,34.785,32.115", geometryType="esriGeometryEnvelope", inSR=4326,
            spatialRel="esriSpatialRelIntersects", outFields="beach_name", returnGeometry="true", outSR=4326)
    edge = []
    for f in d.get("features") or []:
        P = [local(lng, lat) for lng, lat in f["geometry"]["rings"][0]]
        w = min(P, key=lambda p: p[0])
        if -900 <= w[1] <= 2000:
            edge.append((w[1], w[0], f["attributes"].get("beach_name")))
    n = len(edge)
    mz = sum(e[0] for e in edge) / n
    mx = sum(e[1] for e in edge) / n
    k = sum((e[0] - mz) * (e[1] - mx) for e in edge) / sum((e[0] - mz) ** 2 for e in edge)
    coast = {"x0": round(mx - k * mz, 1), "k": round(k, 4), "beaches": [e[2] for e in edge]}
    # ---------------- labels: the streets around the lot and the open space to the north ----------------
    def nearest_on(name, p):
        best = (1e9, None)
        for P in axes.get(name, []):
            for i in range(len(P) - 1):
                dd, q = seg_dist(p, P[i], P[i + 1])
                if dd < best[0]:
                    best = (dd, q)
        return best[1]
    labels = []
    for name, probe in (("אבן גבירול", (-42.0, 10.0)), ("ארלוזורוב", (-5.0, 50.0)), ("בן סרוק", (44.5, 20.0))):
        q = nearest_on(name, probe)
        if q:
            labels.append([name, round(q[0], 1), round(q[1], 1)])
    pk = lotc.get(("4067", "2"))
    if pk:
        labels.append(["גבעת המורה", round(pk[0], 1), round(pk[1], 1)])
    out = {"v": 1, "generated_at": time.strftime("%Y-%m-%d"),
           "source": "עיריית תל אביב-יפו: שכבות המבנים (513), המגרשים (837), הרחובות (507, 508), השטחים הירוקים (503), העצים (628) והחופים (579), " + time.strftime("%#m.%Y" if os.name == "nt" else "%-m.%Y"),
           "note": "הבניינים הקיימים היום, לפי שכבת המבנים של העירייה: קו הבניין, הגובה, הקומות ושנת הבנייה. רוחב הרחובות בציור להמחשה; הצירים לפי העירייה.",
           "origin": {"lat": ORIGIN[0], "lng": ORIGIN[1], "grid_deg": 10},
           "b": kept, "f": [v for b in far for v in b], "lots": lots, "g": greens, "s": streets, "t": trees, "labels": labels, "coast": coast}
    io.open(os.path.join(DIR, "city.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    hs = sorted(b[0] for b in kept)
    print("buildings: features", len(feats), "| kept", len(kept), "| far boxes", len(far), "| left out", why)
    print("  heights: median %.1f m, max %.1f m" % (hs[len(hs) // 2], hs[-1]))
    print("  municipality tower (oid 40141):", named.get("municipality"))
    print("lots", len(lots), "| greens", len(greens), "| streets", len(streets), "| trees", len(trees) // 2)
    print("coast: x = %.1f + %.4f z, from %d beaches" % (coast["x0"], coast["k"], n))
    print("labels", labels)
    print("wrote city.json", os.path.getsize(os.path.join(DIR, "city.json")), "bytes")

    # ---------------- quarter.json ----------------
    mid_lat, mid_lng = to_latlng(*TOWERS_MID)

    def from_mid(x, z):
        # scene frame to true bearing: undo the grid turn, then atan2(east, north)
        c, s = math.cos(-GRID), math.sin(-GRID)
        X, Z = (x - TOWERS_MID[0]) * c - (z - TOWERS_MID[1]) * s, (x - TOWERS_MID[0]) * s + (z - TOWERS_MID[1]) * c
        return round(math.hypot(X, Z)), round((math.degrees(math.atan2(X, -Z)) + 360) % 360, 1)

    def world(x, z):
        # quarter.json's x/z are world metres (x east, z south) from the origin, as the stage's buildWorld turns them itself
        c, s = math.cos(-GRID), math.sin(-GRID)
        return round(x * c - z * s, 1), round(x * s + z * c, 1)
    q = {"generated_at": time.strftime("%Y-%m-%d"), "origin": {"lat": ORIGIN[0], "lng": ORIGIN[1]},
         "tower": {"lat": round(mid_lat, 6), "lng": round(mid_lng, 6), "note": "the middle point between the two towers"},
         "note": "מסה סכמטית לפי מספר הקומות בעמוד הפרויקט; המיקום לפי המגרש. הדמיה להמחשה בלבד.", "projects": [], "places": []}
    # H Infinity: our page (public REST, read only); its place is lot 124's centroid (GIS 837), which the page now holds
    try:
        u = "https://nad-lan.co.il/wp-json/wp/v2/nadlan_project/6548?_fields=id,link,meta&nlq=%d" % int(time.time())
        with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
            p = json.loads(r.read().decode("utf-8"))
        m = p.get("meta") or {}
        x, z = local(float(m["lng"]), float(m["lat"]))
        dist, brg = from_mid(x, z)
        wx, wz = world(x, z)
        st = {"construction": "בבנייה", "marketing": "בשיווק", "permits": "בהליכי היתר"}.get((m.get("project_status") or "").lower(), "")
        q["projects"].append({"id": 6548, "kind": "project", "name": "H Infinity", "pin": "H Infinity", "brand": "H INFINITY",
                              "developer": "קבוצת חג'ג'", "status": st, "floors": int(m.get("num_floors") or 0) or None,
                              "units": int(m.get("num_units") or 0) or None, "url": p.get("link"), "x": wx, "z": wz,
                              "dist": dist, "bearing": brg, "source": "עמוד הפרויקט באתר; המגרש לפי עיריית תל אביב-יפו (מגרש 124)",
                              "phase": "building" if st == "בבנייה" else ("selling" if st == "בשיווק" else "permit")})
    except Exception as e:
        print("H Infinity: skipped,", e)
    places = []
    if pk:
        places.append(("park", "גבעת המורה", "שטח ציבורי פתוח", pk[0], pk[1],
                       "גבול המגרש מצפון לפי החלטת רשות הרישוי (21.9.2025); השטח לפי שכבת המגרשים של העירייה (תכנית 4067)"))
    if "municipality" in named:
        mx_, mz_, fl, hh = named["municipality"]
        places.append(("civic", "בניין העירייה החדש", "מבנה ציבור, %d קומות" % fl, mx_, mz_,
                       "שכבת המבנים של עיריית תל אביב-יפו (מבנה ציבור, 25 קומות, 2024); החיבור אליו במרתף לפי החלטת רשות הרישוי (21.9.2025)"))
    st = get(764, where="1=1", geometry=envelope(400), geometryType="esriGeometryEnvelope", inSR=4326, spatialRel="esriSpatialRelIntersects",
             outFields="station_name_HEB,line,type", returnGeometry="true", outSR=4326)
    for f in st.get("features") or []:
        a, g = f["attributes"], f["geometry"]
        x, z = local(g["x"], g["y"])
        if math.hypot(x, z) < 300:
            places.append(("rail", "תחנת %s, הקו הירוק" % a["station_name_HEB"], "תחנה תת־קרקעית", x, z,
                           "שכבת הקו הירוק של עיריית תל אביב-יפו (תחנות)"))
    for kind, name, status, x, z, src in places:
        dist, brg = from_mid(x, z)
        wx, wz = world(x, z)
        q["places"].append({"kind": kind, "name": name, "pin": name.split(",")[0].strip(), "status": status, "x": wx, "z": wz,
                            "dist": dist, "bearing": brg, "walk": max(1, round(dist * 1.25 / 80)), "source": src})
    io.open(os.path.join(DIR, "quarter.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(q, ensure_ascii=False, indent=1))
    print("quarter: projects", [p["name"] for p in q["projects"]], "| places", [(p["name"], p["dist"], p["bearing"]) for p in q["places"]])
    print("  the towers' middle point", round(mid_lat, 6), round(mid_lng, 6))


if __name__ == "__main__":
    main()
