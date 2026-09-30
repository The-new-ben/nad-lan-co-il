# -*- coding: utf-8 -*-
"""HAD-376 hand check: named places whose sight label changed, checked against the Tel Aviv-Yafo buildings layer itself (GIS 513,
a read-only point query at the place's own lat/lng, so no frame of ours is involved), then against city.json's footprints in
the old frame (north up, 111320) and in the layer's declared frame (build_places.py city_xz).

  python scripts/project-stage/sight_handcheck.py <before-dir> [--n 3]"""
import io, json, math, os, sys, time, urllib.parse, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BEFORE = sys.argv[1]
N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 3
GIS = "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/513/query"
PREF = {"health": 0, "education": 1, "food": 2, "community": 3, "essentials": 4, "outdoors": 5, "transport": 6}


def inside(poly, x, z):
    c = False; j = len(poly) - 1
    for i in range(len(poly)):
        xi, zi = poly[i]; xj, zj = poly[j]
        if (zi > z) != (zj > z) and x < (xj - xi) * (z - zi) / (zj - zi + 1e-12) + xi:
            c = not c
        j = i
    return c


def gis(lat, lng):
    q = {"geometry": "%.6f,%.6f" % (lng, lat), "geometryType": "esriGeometryPoint", "inSR": 4326, "spatialRel": "esriSpatialRelIntersects",
         "outFields": "oid_mivne,ms_komot,t_sug_mivne,gova_simplex_2019,min_height,max_height,year", "returnGeometry": "false", "f": "json"}
    r = urllib.request.Request(GIS + "?" + urllib.parse.urlencode(q), headers={"User-Agent": "Mozilla/5.0 NadLan-CITY/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(r, timeout=60) as resp:
                return [f["attributes"] for f in json.loads(resp.read().decode("utf-8")).get("features", [])]
        except Exception:
            time.sleep(2)
    return None


report = {}
for pk in ("rainbow", "duo", "dimri", "ashira"):
    d = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", pk)
    C = json.load(io.open(os.path.join(d, "city.json"), encoding="utf-8")); Q = json.load(io.open(os.path.join(d, "quarter.json"), encoding="utf-8"))
    A = json.load(io.open(os.path.join(BEFORE, pk + ".places.json"), encoding="utf-8"))
    B = json.load(io.open(os.path.join(d, "places.json"), encoding="utf-8"))
    o = C["origin"]; ke = 111320 * math.cos(math.radians(o["lat"])); kn = o.get("m_lat", 110574.0); g = math.radians(-o["grid_deg"])
    ol = (Q["origin"]["lat"], Q["origin"]["lng"])
    new_xz = lambda la, ln: (((ln - o["lng"]) * ke) * math.cos(g) - (-(la - o["lat"]) * kn) * math.sin(g), ((ln - o["lng"]) * ke) * math.sin(g) + (-(la - o["lat"]) * kn) * math.cos(g))
    old_xz = lambda la, ln: ((ln - ol[1]) * 111320 * math.cos(math.radians(ol[0])), -(la - ol[0]) * 111320)
    blds = []
    for b in C["b"]:
        pts = b[3:]; poly = [(pts[i], pts[i + 1]) for i in range(0, len(pts) - 1, 2)]
        blds.append((b[0], b[1], b[2], poly))
    def host(x, z):
        for h, fl, yr, poly in blds:
            if inside(poly, x, z):
                return {"h": h, "floors": fl, "year": yr}
        return None
    cands = []
    for p, q in zip(A["places"], B["places"]):
        if p["sight"] == q["sight"] or p.get("generic") or p.get("corp") or p["dist"] > 650:
            continue
        cands.append((PREF.get(p["g"], 9), p["dist"], p, q))
    cands.sort(key=lambda c: (c[0], c[1]))
    picked, groups = [], set()
    for pref, dist, p, q in cands:   # three different groups, the nearest of each
        if p["g"] in groups:
            continue
        real = gis(p["lat"], p["lng"])
        if not real:
            continue
        groups.add(p["g"]); picked.append((p, q, real))
        if len(picked) == N:
            break
    report[pk] = []
    print(f"== {pk} (city.json frame: grid {o['grid_deg']} deg, lat metres {kn})")
    for p, q, real in picked:
        r = real[0]
        rh = r.get("gova_simplex_2019") or ((r.get("max_height") or 0) - (r.get("min_height") or 0)) or (r.get("ms_komot") or 0) * 3.2
        hn, ho = host(*new_xz(p["lat"], p["lng"])), host(*old_xz(p["lat"], p["lng"]))
        match = bool(hn) and hn["floors"] == int(r.get("ms_komot") or 0) and hn["year"] == int(r.get("year") or 0) and abs(hn["h"] - round(rh * 2) / 2) < 0.6
        row = {"name": p["name"], "g": p["g"], "lat": p["lat"], "lng": p["lng"], "dist": p["dist"], "bearing": p["bearing"],
               "gis": {"oid": r.get("oid_mivne"), "floors": r.get("ms_komot"), "year": r.get("year"), "height": round(rh, 1), "type": r.get("t_sug_mivne")},
               "new_frame_building": hn, "old_frame_building": ho, "new_matches_gis": match,
               "sight_before": p["sight"], "sight_after": q["sight"]}
        report[pk].append(row)
        print(f"  {p['name']} ({p['g']}, {p['dist']} m, bearing {p['bearing']}) at {p['lat']},{p['lng']}")
        print(f"     the city's layer at that point: building {r.get('oid_mivne')}, {r.get('ms_komot')} floors, {r.get('year')}, {rh:.1f} m ({r.get('t_sug_mivne')})")
        print(f"     city.json, the declared frame: {hn}  -> {'SAME building' if match else 'NOT the same'}")
        print(f"     city.json, the old frame:      {ho}")
        print(f"     sight before {p['sight']}  after {q['sight']}")
json.dump(report, io.open(os.path.join(REPO, "docs", "qa", "had-376-sightlines", "handcheck.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
