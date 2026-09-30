# -*- coding: utf-8 -*-
"""Kikar Hamedina, P2 (the area), step 1 of 3: the plot, the blocks around it and the inputs build_places.py needs.
Research only (30.9.2026): nothing here writes into plugins/nadlan-config/assets/ (that happens at release, P7).

  python docs/research/2026-09-30-kikar-hamedina/build_area_kikar.py
  python scripts/project-stage/build_places.py kikar            (step 2: findplace + OSM + Mapbox walking)
  python docs/research/2026-09-30-kikar-hamedina/enrich_places_kikar.py   (step 3: city layers, bus lines, rail, landmarks)

Sources, all public and read-only (GET):
  Tel Aviv-Yafo municipality GIS, ArcGIS REST IView2 (https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer):
    837 lots of plan 2500ב (the square), 528 the plans, 513 buildings (floors, heights, year, name), 499 construction sites.
The plot centre is the area-weighted centroid of plan 2500ב's lots that are not roads (lot 101 residential, lot 303 public
buildings + open space, lots 201-208 private open space). OpenStreetMap's construction area "פרויקט כיכר המדינה"
(way 727196846) is the cross-check.

Frame of the "b" array (so build_places.py's sight lines read it as they read city.json): x = metres east of the plot
centre = (lng - lng0) * 111320 * cos(lat0); z = metres south = -(lat - lat0) * 111320; no grid turn (grid_deg 0).
Every building also keeps its lat/lng footprint, so the P5 stage can re-project it into any frame.

Outputs (docs/research/2026-09-30-kikar-hamedina/):
  city-blocks.json            every building of GIS 513 within 700 m (footprint, floors, year, height and its source), the
                              notable towers within 2 km, the plot (plan lots + the three towers), "b" for the sight lines,
                              the street axes (507/508) and green areas (503) for the P5 world, and the distance to each road
  kikar-stage/quarter.json    origin + view point (the plot centre) + the square's own landmarks, for build_places.py
  kikar-stage/city.json       the "b" array alone, in the file name build_places.py expects
  eye-kikar-provisional.json  PROVISIONAL eye heights on floors 10/25/37 (formula, see EYE below), replaced in P5
"""
import hashlib, io, json, math, os, sys, time, urllib.parse, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.join(HERE, "kikar-stage")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
CACHE = os.path.join(REPO, "scripts", "project-stage", "_cache", "kikar-area")     # git-ignored
os.makedirs(STAGE, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)
BASE = "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/%d/query"
UA = {"User-Agent": "Mozilla/5.0 NadLan-CITY/1.0 (nad-lan.co.il; research, read-only)"}
R_B = 700.0          # every building within this distance of the plot centre (footprint centroid)
R_N = 2000.0         # notable towers: 70 m and higher within this distance
N_H = 70.0
SKIP_TYPES = {"אנטנה", "תחנת אוטובוס", "מבנה ארעי"}
TODAY = time.strftime("%Y-%m-%d")


def get(layer, **kw):
    p = {"f": "json"}
    p.update(kw)
    url = BASE % layer + "?" + urllib.parse.urlencode(p)
    key = os.path.join(CACHE, "gis-%d-%s.json" % (layer, hashlib.md5(url.encode("utf-8")).hexdigest()[:16]))
    if os.path.exists(key):
        return json.load(io.open(key, encoding="utf-8"))
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                d = json.loads(r.read().decode("utf-8"))
            io.open(key, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False))
            time.sleep(0.5)
            return d
        except Exception:
            if attempt == 2:
                raise
            time.sleep(3)


def envelope(c, radius):
    dlat = radius / 110574.0
    dlng = radius / (math.cos(math.radians(c[0])) * 111320.0)
    return "%.6f,%.6f,%.6f,%.6f" % (c[1] - dlng, c[0] - dlat, c[1] + dlng, c[0] + dlat)


def fetch_all(layer, c, radius, fields, where="1=1"):
    out, off = [], 0
    while True:
        d = get(layer, where=where, geometry=envelope(c, radius), geometryType="esriGeometryEnvelope", inSR=4326,
                spatialRel="esriSpatialRelIntersects", outFields=fields, returnGeometry="true", outSR=4326,
                resultOffset=off, resultRecordCount=1000)
        feats = d.get("features") or []
        out += feats
        if not feats or not d.get("exceededTransferLimit"):
            break
        off += len(feats)
    return out


def ring_centroid(P):
    """area-weighted centroid and signed area of a ring of (x, y)"""
    A = cx = cy = 0.0
    for i in range(len(P)):
        x0, y0 = P[i]
        x1, y1 = P[(i + 1) % len(P)]
        c = x0 * y1 - x1 * y0
        A += c
        cx += (x0 + x1) * c
        cy += (y0 + y1) * c
    A /= 2.0
    if abs(A) < 1e-9:
        return 0.0, sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P)
    return A, cx / (6 * A), cy / (6 * A)


def seg_dist(p, a, b):
    ax, az = b[0] - a[0], b[1] - a[1]
    L = ax * ax + az * az
    t = 0 if L == 0 else max(0, min(1, ((p[0] - a[0]) * ax + (p[1] - a[1]) * az) / L))
    return math.hypot(p[0] - a[0] - t * ax, p[1] - a[1] - t * az)


def dp_open(pts, tol):
    if len(pts) < 3:
        return pts
    i, d = max(((i, seg_dist(pts[i], pts[0], pts[-1])) for i in range(1, len(pts) - 1)), key=lambda t: t[1])
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


def main():
    # ---------------- 1. the plot: plan 2500ב's lots (GIS 837) and the plans (GIS 528) ----------------
    probe = (32.0868637, 34.7898471)       # OSM's point of the square (way 26260278), only to find the lots
    lots = get(837, where="st_taba LIKE '2500%'", geometry=envelope(probe, 250), geometryType="esriGeometryEnvelope",
               inSR=4326, spatialRel="esriSpatialRelIntersects", outFields="*", returnGeometry="true", outSR=4326)["features"]
    k0 = math.cos(math.radians(probe[0])) * 111320.0
    tot = [0.0, 0.0, 0.0]
    lot_out = []
    for f in lots:
        a = f["attributes"]
        use = (a.get("t_yeud_karka") or "").strip()
        num = (a.get("st_mispar_migrash_betaba") or "").strip()
        ring = f["geometry"]["rings"][0][:-1]
        P = [((lng - probe[1]) * k0, (lat - probe[0]) * 110574.0) for lng, lat in ring]
        A, cx, cy = ring_centroid(P)
        lot_out.append({"lot": num or None, "use": use, "plan": (a.get("st_taba") or "").strip(), "gush": a.get("ms_gush"),
                        "area_registered_m2": a.get("ms_shetach_rashum"), "area_gis_m2": round(abs(A)),
                        "ring": [[round(lat, 7), round(lng, 7)] for lng, lat in ring]})
        if num and not use.startswith("דרך"):
            tot[0] += abs(A)
            tot[1] += cx * abs(A)
            tot[2] += cy * abs(A)
    c_e, c_n = tot[1] / tot[0], tot[2] / tot[0]
    O = (round(probe[0] + c_n / 110574.0, 6), round(probe[1] + c_e / k0, 6))
    print("plot centre (plan 2500ב lots, not roads): %.6f, %.6f  area %.0f m2" % (O[0], O[1], tot[0]))
    plans = []
    for f in get(528, where="taba LIKE '2500%'", outFields="taba,shem_taba,t_status,tr_matan_tokef,megurim_yechidot,megurim_shetach,mivney_tzibur_shetach,url_documents,url_iplan,mispar_tochnit_mavat",
                 returnGeometry="false")["features"]:
        a = f["attributes"]
        eff = a.get("tr_matan_tokef")
        plans.append({"plan": (a.get("taba") or "").strip(), "name": a.get("shem_taba"), "status": a.get("t_status"),
                      "in_force_from": time.strftime("%Y-%m-%d", time.gmtime(eff / 1000)) if eff and eff > 0 else None,
                      "housing_units": a.get("megurim_yechidot") or None, "housing_m2": a.get("megurim_shetach") or None,
                      "public_buildings_m2": a.get("mivney_tzibur_shetach") or None, "mavat": a.get("mispar_tochnit_mavat"),
                      "docs": a.get("url_documents"), "iplan": a.get("url_iplan")})

    KX = math.cos(math.radians(O[0])) * 111320.0
    KZ = 111320.0                          # build_places.py's xz(): the same metres for lat, so its sight lines line up

    def xz(lng, lat):
        return ((lng - O[1]) * KX, -(lat - O[0]) * KZ)

    def dist_bearing(lat, lng):
        dx = (lng - O[1]) * KX
        dy = (lat - O[0]) * KZ
        return round(math.hypot(dx, dy)), round((math.degrees(math.atan2(dx, dy)) + 360) % 360, 1)

    # ---------------- 2. buildings (GIS 513) ----------------
    feats = fetch_all(513, O, R_N, "oid_mivne,id_binyan,t_sug_mivne,ms_komot,shem_mivne,gova_simplex_2019,min_height,max_height,year,dsm_mean,dsm_max")
    blds, notable, towers, why, seen = [], [], [], {"type": 0, "tiny": 0, "no_height": 0, "dup": 0}, set()
    for f in feats:
        a = f.get("attributes") or {}
        oid = a.get("oid_mivne")
        if oid in seen:
            why["dup"] += 1
            continue
        seen.add(oid)
        rings = (f.get("geometry") or {}).get("rings") or []
        if not rings:
            continue
        ring = rings[0][:-1] if rings[0][0] == rings[0][-1] else rings[0]
        P = [xz(lng, lat) for lng, lat in ring]
        if len(P) < 3:
            continue
        A, cx, cz = ring_centroid(P)
        dist = math.hypot(cx, cz)
        typ = (a.get("t_sug_mivne") or "").strip()
        name = (a.get("shem_mivne") or "").strip() or None
        floors = int(a.get("ms_komot") or 0) or None
        # the height and its source, best first: the city's 2019 survey, roof minus base, the DSM mean, floors x 3.2 m
        h, hs = None, "not found"
        if a.get("gova_simplex_2019"):
            h, hs = float(a["gova_simplex_2019"]), "survey 2019 (gova_simplex_2019)"
        elif a.get("max_height") and a.get("min_height") and a["max_height"] > a["min_height"]:
            h, hs = float(a["max_height"] - a["min_height"]), "roof minus base (max_height - min_height)"
        elif a.get("dsm_mean"):
            h, hs = float(a["dsm_mean"]), "DSM mean (dsm_mean)"
        elif floors:
            h, hs = floors * 3.2, "ESTIMATED: floors x 3.2 m"
        lat_c = O[0] - cz / KZ
        lng_c = O[1] + cx / KX
        d, br = dist_bearing(lat_c, lng_c)
        rec = {"oid": oid, "id": a.get("id_binyan"), "type": typ or None, "name": name, "floors": floors,
               "year": int(a.get("year") or 0) or None, "h": round(h, 1) if h else None, "h_src": hs,
               "dsm_max": round(a["dsm_max"], 1) if a.get("dsm_max") else None,
               "lat": round(lat_c, 6), "lng": round(lng_c, 6), "dist": d, "bearing": br, "area_m2": round(abs(A))}
        is_tower = name in ("מגדל A", "מגדל B", "מגדל C") and d < 150
        if is_tower:
            rec["fp"] = [[round(lat, 7), round(lng, 7)] for lng, lat in ring]
            towers.append(rec)
        if h and h >= N_H and d <= R_N and not is_tower:
            notable.append(dict(rec))
        if dist > R_B:
            continue
        if typ in SKIP_TYPES:
            why["type"] += 1
            continue
        if abs(A) < 10:
            why["tiny"] += 1
            continue
        Ps = simplify_ring(P, 0.3)
        if ring_centroid(Ps)[0] < 0:
            Ps = Ps[::-1]
        rec["fp"] = [[round(O[0] - z / KZ, 7), round(O[1] + x / KX, 7)] for x, z in Ps]
        rec["xz"] = [v for x, z in Ps for v in (round(x, 1), round(z, 1))]
        rec["kikar_tower"] = name[-1] if is_tower else None
        if not h:
            why["no_height"] += 1
        blds.append(rec)
    blds.sort(key=lambda r: r["dist"])
    notable.sort(key=lambda r: -r["h"])
    towers.sort(key=lambda r: r["name"])
    # the "b" array for the sight lines: the three towers stay out (the eye stands in them; per-tower lines are P5)
    b = [[round(r["h"] * 2) / 2, r["floors"] or 0, r["year"] or 0] + r["xz"] for r in blds
         if r["h"] and r["h"] >= 2.5 and not r["kikar_tower"]]

    # ---------------- 3. the construction-site records on the plot (GIS 499) ----------------
    sites = []
    for f in fetch_all(499, O, 150, "*"):
        a = f["attributes"]
        ring = f["geometry"]["rings"][0][:-1]
        P = [xz(lng, lat) for lng, lat in ring]
        A, cx, cz = ring_centroid(P)
        if math.hypot(cx, cz) > 120:
            continue
        ts = lambda v: time.strftime("%Y-%m-%d", time.gmtime(v / 1000)) if v and v > 0 else None
        sites.append({"file": a.get("tik_tipul"), "status": a.get("status_pikuach"), "status_date": ts(a.get("tr_status_pikuach")),
                      "stage": a.get("matzav_bniya"), "works_started": ts(a.get("tr_tchilat_avoda")), "permits": a.get("heterim"),
                      "address": (a.get("ktovet") or "").strip() or None, "lat": round(O[0] - cz / KZ, 6), "lng": round(O[1] + cx / KX, 6)})

    # ---------------- 3b. streets (GIS 507 axes, 508 main streets) and green areas (GIS 503) ----------------
    mains = set((f["attributes"].get("t_rechov") or "").strip() for f in fetch_all(508, O, 1600, "t_rechov"))
    streets, near = [], {}
    for f in fetch_all(507, O, 1600, "t_rechov,t_sug,k_reka"):
        a = f["attributes"]
        name = (a.get("t_rechov") or "").strip()
        sug = (a.get("t_sug") or "").strip()
        k = int(a.get("k_reka") or 0)
        w = 5 if (sug in ("שביל", "סמטת") or k in (0, 50)) else (24 if sug == "שדרות" else (20 if (k == 200 or name in mains) else 10))
        for path in (f["geometry"].get("paths") or []):
            P = [xz(lng, lat) for lng, lat in path]
            for i in range(len(P) - 1):
                (x1, z1), (x2, z2) = P[i], P[i + 1]
                dx, dz = x2 - x1, z2 - z1
                L = dx * dx + dz * dz
                t = 0 if L == 0 else max(0, min(1, -(x1 * dx + z1 * dz) / L))
                qx, qz = x1 + t * dx, z1 + t * dz
                dd = math.hypot(qx, qz)
                if name and (name not in near or dd < near[name][0]):
                    near[name] = (dd, qx, qz, w, sug)
            if min(math.hypot(x, z) for x, z in P) <= R_B + 100:
                P2 = dp_open(P, 0.5)
                streets.append([w, name] + [v for x, z in P2 for v in (round(x, 1), round(z, 1))])
    roads_near = []
    for name, (dd, qx, qz, w, sug) in sorted(near.items(), key=lambda kv: kv[1][0]):
        la, ln = O[0] - qz / KZ, O[1] + qx / KX
        if not name.isdigit() and dd <= 1600:            # every named street within 1.6 km, nearest point first
            roads_near.append({"name": name, "kind": sug or None, "main": name in mains, "dist_m": round(dd), "bearing": dist_bearing(la, ln)[1],
                               "nearest": [round(la, 6), round(ln, 6)]})
    greens = []
    for f in fetch_all(503, O, R_B, "shem_gan,sug_gan"):
        a = f["attributes"]
        for ring in (f["geometry"].get("rings") or [])[:1]:
            P = [xz(lng, lat) for lng, lat in ring[:-1]]
            if len(P) < 3 or abs(ring_centroid(P)[0]) < 40 or min(math.hypot(x, z) for x, z in P) > R_B:
                continue
            P = simplify_ring(P, 0.8)
            greens.append([(a.get("shem_gan") or "").strip()] + [v for x, z in P for v in (round(x, 1), round(z, 1))])

    # ---------------- 4. write city-blocks.json ----------------
    hs_count = {}
    for r in blds:
        hs_count[r["h_src"].split(" (")[0]] = hs_count.get(r["h_src"].split(" (")[0], 0) + 1
    out = {
        "v": 1, "generated_at": TODAY,
        "source": "עיריית תל אביב-יפו, GIS פתוח (ArcGIS REST IView2): שכבת המבנים 513, המגרשים 837, התכניות 528, אתרי הבנייה 499; נשלף %s" % TODAY,
        "source_url": "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/513",
        "origin": {"lat": O[0], "lng": O[1], "what": "the plot centre: area-weighted centroid of plan 2500ב's lots that are not roads (GIS 837)",
                   "cross_check": "OpenStreetMap construction area 'פרויקט כיכר המדינה' (way 727196846), vertex mean 32.086854, 34.789805 (~11 m away)"},
        "frame": {"x": "metres east of the origin = (lng - lng0) * 111320 * cos(lat0)", "z": "metres south = -(lat - lat0) * 111320",
                  "grid_deg": 0, "note": "the frame of scripts/project-stage/build_places.py xz(); the stage (P5) may turn it"},
        "radius_m": R_B,
        "height_rule": ["survey 2019 (gova_simplex_2019)", "roof minus base (max_height - min_height)", "DSM mean (dsm_mean)",
                        "ESTIMATED: floors x 3.2 m", "not found"],
        "left_out": {"types": sorted(SKIP_TYPES), "footprints_under_10_m2": why["tiny"], "by_type": why["type"]},
        "counts": {"buildings": len(blds), "with_height": sum(1 for r in blds if r["h"]), "height_sources": hs_count,
                   "b_for_sight": len(b), "notable_70m_within_2km": len(notable)},
        "plot": {"plans": plans, "lots": lot_out, "area_not_roads_m2": round(tot[0]), "towers": [{k: v for k, v in t.items() if k not in ("xz", "kikar_tower")} for t in towers], "construction_sites": sites,
                 "note": "the tower names A/B/C, floors and heights are the city's GIS 513 fields (shem_mivne, ms_komot, dsm_mean)"},
        "notable": [{k: r[k] for k in ("oid", "name", "type", "floors", "year", "h", "h_src", "dsm_max", "lat", "lng", "dist", "bearing")} for r in notable],
        "buildings": [{k: v for k, v in r.items() if k != "xz"} for r in blds],
        "b": b,
        "s": streets, "s_note": "street axes (GIS 507; width class: main streets 508 and k_reka 200 = 20 m, boulevards 24 m, streets 10 m, lanes and paths 5 m; widths are a drawing class, the axes are the city's), within %d m" % (R_B + 100),
        "g": greens, "g_note": "public green areas (GIS 503 'שטחים ירוקים') touching the %d m ring" % R_B,
        "roads_near": roads_near,
    }
    p = os.path.join(HERE, "city-blocks.json")
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n")
    io.open(os.path.join(STAGE, "city.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps({"v": 1, "generated_at": TODAY, "source": out["source"], "origin": {"lat": O[0], "lng": O[1], "grid_deg": 0, "m_lat": KZ},
                    "note": "only 'b', for build_places.py's sight lines (a copy of city-blocks.json's b)", "b": b},
                   ensure_ascii=False, separators=(",", ":")) + "\n")
    print("buildings within %d m: %d (with height %d) | b %d | notable %d | left out %s" % (R_B, len(blds), out["counts"]["with_height"], len(b), len(notable), why))
    print("height sources", hs_count, "| streets", len(streets), "| greens", len(greens))
    print("roads_near", len(roads_near))
    for t in towers:
        print("tower", t["name"], t["floors"], t["h"], t["h_src"], t["lat"], t["lng"], t["dist"], t["bearing"])
    for r in notable[:25]:
        print("notable", r["h"], r["floors"], r["name"], r["type"], r["dist"], r["bearing"], r["h_src"])
    print("wrote", p, os.path.getsize(p), "bytes")

    # ---------------- 5. quarter.json for build_places.py: origin, view point, the square's own landmarks ----------------
    # the two new public buildings on lot 303 (the west of the plot). Their names, checked 30.9.2026 against the city's point
    # layers and OpenStreetMap: the city's schools (769) and community (553) layers put the elementary school "כיכר המדינה",
    # the middle school "מאיר שלו - חט\"ב" (both ה' באייר 75) and "מרכז קהילתי כיכר המדינה" in the NORTH-WEST building
    # (oid 43143, no name in 513); OSM way 1560991906 names that building "בית הספר כיכר המדינה". The buildings layer names
    # the SOUTH-WEST building (oid 43109) "מרכז קהילתי", while OSM way 1560991907 calls it "תיכון עירוני כ\"ה ע\"ש מאיר שלו":
    # a conflict, kept in the source line.
    NAMES = {43143: ("בית הספר כיכר המדינה", "השם: שכבת בתי הספר של העירייה (769: כיכר המדינה, יסודי; מאיר שלו, חט\"ב; ה' באייר 75), "
                     "שכבת מוסדות הקהילה (553: מרכז קהילתי כיכר המדינה) ו-OSM (way 1560991906)"),
             43109: ("מרכז קהילתי", "השם: שכבת המבנים (513); סתירה: OSM (way 1560991907) קורא לו תיכון עירוני כ\"ה ע\"ש מאיר שלו, "
                     "ושכבת מוסדות הקהילה (553) מציבה את המרכז הקהילתי בבניין הצפון-מערבי")}
    marks = []
    for r in blds:
        if r["dist"] < 140 and r["type"] == "מבנה ציבור":
            nm, why_name = NAMES.get(r["oid"], (r["name"] or "מבנה ציבור בכיכר", ""))
            marks.append({"kind": "civic", "name": nm, "pin": nm, "status": "מבנה ציבור, %s קומות%s" % (r["floors"], ", %s" % r["year"] if r["year"] else ""),
                          "lat": r["lat"], "lng": r["lng"], "src": "שכבת המבנים של עיריית תל אביב-יפו (513), oid %s%s" % (r["oid"], "; " + why_name if why_name else "")})
    q = {"generated_at": TODAY, "origin": {"lat": O[0], "lng": O[1]},
         "tower": {"lat": O[0], "lng": O[1], "note": "the plot centre (PROVISIONAL view point): the three towers stand 67-90 m from it; per-tower view points come in P5"},
         "towers": [{k: t[k] for k in ("name", "floors", "h", "h_src", "lat", "lng", "dist", "bearing")} for t in towers],
         "note": "research copy for build_places.py (P2); the stage's own quarter.json is written in P5/P7", "projects": [], "places": []}
    for m in marks:
        x, z = xz(m["lng"], m["lat"])
        d, br = dist_bearing(m["lat"], m["lng"])
        q["places"].append({"kind": m["kind"], "name": m["name"], "pin": m["pin"], "status": m["status"], "x": round(x, 1), "z": round(z, 1),
                            "dist": d, "bearing": br, "src": m["src"]})
    io.open(os.path.join(STAGE, "quarter.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(q, ensure_ascii=False, indent=1))
    print("quarter places", [(p["name"], p["dist"], p["bearing"]) for p in q["places"]])

    # ---------------- 6. PROVISIONAL eye heights ----------------
    # EYE: (floor - 1) x 4.0 m + 1.6 m; 4.0 m = 160 m / 40 floors (GIS 513: towers A and C, 40 floors, 160 m). Bands 10/25/37:
    # 37 is the highest floor every tower has (tower B: 37 floors per Wikipedia/Ashtrom, 40 per GIS 513 - a conflict for P1).
    eye = {str(f): round((f - 1) * 4.0 + 1.6, 1) for f in (10, 25, 37)}
    io.open(os.path.join(HERE, "eye-kikar-provisional.json"), "w", encoding="utf-8").write(json.dumps(
        {"project": "kikar", "measured": None, "computed": TODAY, "provisional": True,
         "source": "CALC, provisional: (floor - 1) x 4.0 m + 1.6 m; 4.0 m = 160 m / 40 floors from the city's GIS 513 (towers A, C). Replace with the stage's floorHeight() in P5 (scripts/project-stage/measure_eyes.py).",
         "eye": eye}, indent=1))
    print("provisional eyes", eye)


if __name__ == "__main__":
    main()
