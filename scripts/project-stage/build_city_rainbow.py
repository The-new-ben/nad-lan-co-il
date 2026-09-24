# -*- coding: utf-8 -*-
"""The real city around Rainbow for the stage (the site loop, R4b part B): the existing buildings from the Tel Aviv-Yafo
GIS layer 513 "מבנים" (footprint, height, floors, year), in place of the generic volumes the stage drew until 1.72.267.

Output: plugins/nadlan-config/assets/project-stage/rainbow/city.json, read by stage.js at load (nothing is fetched from
the city at page time):
  {"v": 1, "generated_at", "source", "note", "b": [[height_m, floors, year, x1, z1, x2, z2, ...], ...]}
x and z are metres in the stage's frame (from the lot's centre 32.103168, 34.784441, turned with the grid by -10°:
x = grid east, z = grid south), the ring wound like the stage's own plates. Left out, so the model shows the city and not
its noise: antennas, bus shelters and temporary structures (site offices), footprints under 25 m², anything lower than
2.5 m, and whatever stands on Rainbow's own lot or on one of our projects' lots (those are being built again; the stage
draws the new building there). Heights: the city's 2019 survey height, else roof minus base, else floors x 3.2 m.
With them, the Sde Dov plan's lots that have an approved design plan (the micro-atlas snapshot of the city's plan layer,
27.8.2026), as flat plates, and the planned linear park, so the quarter being built reads as a planned quarter and not as
an empty field: "lots": [["lot" | "park", "105", x1, z1, ...], ...]. Rainbow's own lot is drawn by the stage itself.
  python scripts/project-stage/build_city_rainbow.py [--raw saved.geojson]"""
import io, json, math, os, sys, time, urllib.parse, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "rainbow")
OUT = os.path.join(DIR, "city.json")
ORIGIN = (32.103168, 34.784441)
GRID = math.radians(-10)
BOX = (34.7740, 32.0950, 34.7950, 32.1115)   # about 1 km around the lot on every side
LAYER = "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/513/query"
SKIP_TYPES = {"אנטנה", "תחנת אוטובוס", "מבנה ארעי"}
PLANS = os.path.join(os.path.expanduser("~"), "Documents", "Codex", "2026-08-27", "https-www-nadlan-gov-il-https", "outputs",
                     "sde-dov-micro-atlas", "plans-and-parcels.geojson")
LOT = [[-30.7, 68.7], [-29.5, -71.7], [19.3, -71.1], [30.7, -61.4], [30.3, 46.6], [22.6, 65.3], [10.1, 75.8]]


def fetch():
    q = {"where": "1=1", "geometry": ",".join(map(str, BOX)), "geometryType": "esriGeometryEnvelope", "inSR": 4326,
         "spatialRel": "esriSpatialRelIntersects", "outFields": "oid_mivne,ms_komot,t_sug_mivne,gova_simplex_2019,min_height,max_height,year",
         "returnGeometry": "true", "outSR": 4326, "f": "geojson", "resultRecordCount": 2000}
    r = urllib.request.Request(LAYER + "?" + urllib.parse.urlencode(q), headers={"User-Agent": "Mozilla/5.0 NadLan-CITY/1.0"})
    with urllib.request.urlopen(r, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def local(lng, lat):
    e = (lng - ORIGIN[1]) * math.cos(math.radians(ORIGIN[0])) * 111320.0
    n = (lat - ORIGIN[0]) * 110574.0
    X, Z = e, -n
    c, s = math.cos(GRID), math.sin(GRID)
    return (X * c - Z * s, X * s + Z * c)


def area(P):
    return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))) / 2


def inside(p, P):
    x, z = p; c = False
    for i in range(len(P)):
        a, b = P[i], P[i - 1]
        if (a[1] > z) != (b[1] > z) and x < (b[0] - a[0]) * (z - a[1]) / (b[1] - a[1]) + a[0]:
            c = not c
    return c


def seg_dist(p, a, b):
    ax, az = b[0] - a[0], b[1] - a[1]
    L = ax * ax + az * az
    t = 0 if L == 0 else max(0, min(1, ((p[0] - a[0]) * ax + (p[1] - a[1]) * az) / L))
    return math.hypot(p[0] - a[0] - t * ax, p[1] - a[1] - t * az)


def simplify(P, tol):
    """Douglas-Peucker on a closed ring (split at the point farthest from the first)."""
    if len(P) <= 4:
        return P
    far = max(range(len(P)), key=lambda i: math.hypot(P[i][0] - P[0][0], P[i][1] - P[0][1]))

    def dp(pts):
        if len(pts) < 3:
            return pts
        i, d = max(((i, seg_dist(pts[i], pts[0], pts[-1])) for i in range(1, len(pts) - 1)), key=lambda t: t[1])
        if d <= tol:
            return [pts[0], pts[-1]]
        return dp(pts[: i + 1])[:-1] + dp(pts[i:])

    a = dp(P[: far + 1]); b = dp(P[far:] + [P[0]])
    out = a[:-1] + b[:-1]
    return out if len(out) >= 3 else P


def main():
    raw = None
    if "--raw" in sys.argv:
        raw = json.load(io.open(sys.argv[sys.argv.index("--raw") + 1], encoding="utf-8"))
    else:
        raw = fetch()
    feats = raw.get("features") or []
    # our projects' lots (quarter.json): the plate the stage draws there, 64 x 52 m, turned with the grid
    q = json.load(io.open(os.path.join(DIR, "quarter.json"), encoding="utf-8"))
    c, s = math.cos(GRID), math.sin(GRID)
    ours = [(p["x"] * c - p["z"] * s, p["x"] * s + p["z"] * c) for p in q.get("projects", [])]
    kept, why = [], {"type": 0, "small": 0, "low": 0, "rainbow": 0, "ours": 0, "shape": 0}
    for f in feats:
        pr = f.get("properties") or {}
        if (pr.get("t_sug_mivne") or "").strip() in SKIP_TYPES:
            why["type"] += 1; continue
        h = pr.get("gova_simplex_2019") or 0
        if not h and pr.get("max_height") and pr.get("min_height"):
            h = pr["max_height"] - pr["min_height"]
        if not h and pr.get("ms_komot"):
            h = pr["ms_komot"] * 3.2
        if h < 2.5:
            why["low"] += 1; continue
        g = f.get("geometry") or {}
        polys = [g["coordinates"]] if g.get("type") == "Polygon" else (g.get("coordinates") or [])
        for poly in polys:
            ring = poly[0]
            if len(ring) > 1 and ring[0] == ring[-1]:
                ring = ring[:-1]
            P = [local(lng, lat) for lng, lat in ring]
            if len(P) < 3:
                why["shape"] += 1; continue
            if abs(area(P)) < 25:
                why["small"] += 1; continue
            cx = sum(p[0] for p in P) / len(P); cz = sum(p[1] for p in P) / len(P)
            if inside((cx, cz), LOT) or any(inside(p, LOT) for p in P):
                why["rainbow"] += 1; continue
            if any(abs(cx - ox) < 32 and abs(cz - oz) < 26 for ox, oz in ours):
                why["ours"] += 1; continue
            P = simplify(P, 0.6)
            if area(P) < 0:        # wound like the stage's plates (roundRectPoly): positive in (x, z)
                P = P[::-1]
            flat = []
            for x, z in P:
                flat += [round(x, 1), round(z, 1)]
            kept.append([round(h * 2) / 2, int(pr.get("ms_komot") or 0), int(pr.get("year") or 0)] + flat)
    kept.sort(key=lambda b: (b[3], b[4]))
    # the plan's lots (design plans approved lot by lot) and the linear park, within 1.3 km; Rainbow's lot 111 left to the stage
    lots = []
    for f in json.load(io.open(PLANS, encoding="utf-8"))["features"]:
        pr = f["properties"]; name = pr.get("name") or ""
        if pr.get("plan_level") != "תכנית עיצוב/מגרש":
            continue
        kind = "park" if "פארק" in name else ("lot" if name.startswith(("מגרש", "יחידת תכנון")) else None)
        if not kind or name.startswith("מגרש 111,"):
            continue
        g = f["geometry"]
        rings = [g["coordinates"][0]] if g["type"] == "Polygon" else [pp[0] for pp in g["coordinates"]]
        for ring in rings:
            if len(ring) > 1 and ring[0] == ring[-1]:
                ring = ring[:-1]
            P = [local(lng, lat) for lng, lat in ring]
            if min(math.hypot(x, z) for x, z in P) > 1300:
                continue
            if area(P) < 0:
                P = P[::-1]
            num = "".join(ch for ch in name.split(",")[0] if ch.isdigit())
            flat = []
            for x, z in P:
                flat += [round(x, 1), round(z, 1)]
            lots.append([kind, num] + flat)
    out = {"v": 1, "generated_at": time.strftime("%Y-%m-%d"),
           "source": "עיריית תל אביב-יפו, שכבת המבנים (GIS 513), " + time.strftime("%-m.%Y" if os.name != "nt" else "%#m.%Y"),
           "note": "הבניינים הקיימים היום, לפי שכבת המבנים של העירייה: קו הבניין, הגובה, הקומות ושנת הבנייה.",
           "lots_source": "עיריית תל אביב-יפו, שכבת התוכניות: מגרשים עם תכנית עיצוב מאושרת (27.8.2026)",
           "b": kept, "lots": lots}
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    hs = sorted(b[0] for b in kept)
    print("features", len(feats), "| kept", len(kept), "| left out", why)
    print("heights: median %.1f m, max %.1f m | points %d" % (hs[len(hs) // 2], hs[-1], sum((len(b) - 3) // 2 for b in kept)))
    print("plan lots", sum(1 for l in lots if l[0] == "lot"), "| park parts", sum(1 for l in lots if l[0] == "park"))
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
