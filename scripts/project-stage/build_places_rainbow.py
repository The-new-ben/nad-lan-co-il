# -*- coding: utf-8 -*-
"""AreaLife (design system AreaLife v97, 28.9.2026): the one place registry around Rainbow, for the area map, the view from
the floor and the 360 windows (Codex consult 28.9: one layer for all three, every place with its source).

The owner, 28.9: "the maps are not rich enough ... people want to know what's around ... they don't want to see white
buildings, they want to know what's in the neighbourhood".

Output: plugins/nadlan-config/assets/project-stage/rainbow/places.json
  places     every place within RADIUS of the tower: first findplace's frozen discovery file (the owner's findplace.co.il,
             north Tel Aviv: Tel Aviv-Yafo municipality open data + OpenStreetMap, 27.8.2026; scripts/project-stage/data/
             findplace-north-tlv-discovery-v2.geojson, sha256 in its manifest), then OpenStreetMap (Overpass) for what it lacks
             and for the names in other languages (a place found in both is one, matched by group, name and 40 m), with its
             id (fp:<id> or osm:<type>/<id>), its source ('tlv', 'osm', 'tlv+osm'), its findplace page when it has one, one of
             seven groups (education, outdoors, transport, food, essentials, health, community),
             its position (x east, z south, metres from the lot's centre, as the stage), the distance and the bearing from
             the tower, the walking minutes (Mapbox Directions, walking profile, from the tower's entrance side; null when
             the router gave none), and what is visible of it from floors 10, 25 and 36 ('street': the place itself, 'roof':
             only the building it stands in, null: hidden), by the city's buildings layer (city.json).
  landmarks  the quarter's places (quarter.json: the light rail, the beach, the river mouth, the park, the school), kept
             with their own source.
  iso        5, 10 and 15 walking minutes around the tower (Mapbox Isochrone, walking): approximate reachability areas.
Nothing is invented: a place without a name in OSM keeps OSM's kind in Hebrew and is marked so ('generic'); a missing
walk time stays null. OSM data (c) OpenStreetMap contributors, ODbL: the page says so wherever it shows them.
  python scripts/project-stage/build_places_rainbow.py [--no-walk]"""
import io, json, math, os, re, sys, time, urllib.parse, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RB = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "rainbow")
OUT = os.path.join(RB, "places.json")
CACHE = os.path.join(REPO, "scripts", "project-stage", "_cache", "places-rainbow")
os.makedirs(CACHE, exist_ok=True)
LOT = (32.103168, 34.784441)     # the scene's origin (build_quarter_rainbow.py)
TOWER = (32.10354, 34.78466)     # the tower
RADIUS = 1500
FLOORS = {10: 7.2 + 9 * 3.75 + 1.6, 25: 7.2 + 24 * 3.75 + 1.6, 36: 7.2 + 35 * 3.75 + 1.6}   # the eye, metres above the street
M_LAT = 111320.0
M_LNG = 111320.0 * math.cos(math.radians(LOT[0]))


def xz(lat, lng):
    return ((lng - LOT[1]) * M_LNG, -(lat - LOT[0]) * M_LAT)


def dist_bearing(lat, lng):
    dx = (lng - TOWER[1]) * M_LNG
    dy = (lat - TOWER[0]) * M_LAT
    return round(math.hypot(dx, dy)), round((math.degrees(math.atan2(dx, dy)) + 360) % 360, 1)


def token():
    """the site's public Mapbox token (pk.), as every project page prints it; read from the page, never stored"""
    html = urllib.request.urlopen(urllib.request.Request("https://nad-lan.co.il/projects/rainbow-tel-aviv/?pl=1", headers={"User-Agent": "NadLan-places/1.0"}), timeout=60).read().decode("utf-8", "replace")
    m = re.search(r"pk\.[A-Za-z0-9._-]{40,}", html)
    return m.group(0) if m else None


def cached_json(name, fetch):
    p = os.path.join(CACHE, name)
    if os.path.exists(p):
        return json.load(io.open(p, encoding="utf-8"))
    d = fetch()
    if d is not None:
        io.open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False))
    return d


# ---------------------------------------------------------------- 1. OpenStreetMap
Q = """[out:json][timeout:60];(
nwr(around:{r},{la},{ln})[amenity~"^(school|kindergarten|library|college|university|childcare)$"];
nwr(around:{r},{la},{ln})[leisure~"^(park|playground|garden|sports_centre|fitness_centre|pitch|dog_park|swimming_pool)$"][name];
nwr(around:{r},{la},{ln})[leisure~"^(park|playground|garden|dog_park)$"];
nwr(around:{r},{la},{ln})[natural="beach"];
nwr(around:{r},{la},{ln})[railway~"^(station|halt|tram_stop|subway_entrance)$"];
node(around:{r},{la},{ln})[highway=bus_stop];
nwr(around:{r},{la},{ln})[amenity~"^(cafe|restaurant|ice_cream|fast_food|bar|pub)$"];
nwr(around:{r},{la},{ln})[shop~"^(supermarket|convenience|greengrocer|bakery|mall|department_store|butcher|deli|chemist)$"];
nwr(around:{r},{la},{ln})[amenity~"^(pharmacy|post_office|bank|atm)$"];
nwr(around:{r},{la},{ln})[amenity~"^(clinic|doctors|hospital|dentist)$"];
nwr(around:{r},{la},{ln})[healthcare];
);out tags center;"""
ENDPOINTS = ["https://overpass-api.de/api/interpreter", "https://overpass.openstreetmap.fr/api/interpreter",
             "https://overpass.kumi.systems/api/interpreter"]


def overpass():
    q = Q.format(r=RADIUS, la=TOWER[0], ln=TOWER[1])
    for ep in ENDPOINTS:
        try:
            req = urllib.request.Request(ep, data=urllib.parse.urlencode({"data": q}).encode(), headers={"User-Agent": "NadLan-places/1.0 (nad-lan.co.il)"})
            d = json.load(urllib.request.urlopen(req, timeout=90))
            if isinstance(d, dict) and d.get("elements") is not None:
                print("overpass", ep, len(d["elements"]))
                return d
        except Exception as e:
            print("overpass", ep, "failed:", str(e)[:100])
    return None


GENERIC = {"bus_stop": "תחנת אוטובוס", "park": "פארק", "playground": "גן משחקים", "garden": "גינה ציבורית", "pitch": "מגרש ספורט",
           "kindergarten": "גן ילדים", "childcare": "מעון יום", "school": "בית ספר", "supermarket": "סופרמרקט", "convenience": "מכולת",
           "pharmacy": "בית מרקחת", "clinic": "מרפאה", "doctors": "מרפאה", "dentist": "מרפאת שיניים", "tram_stop": "תחנת רכבת קלה",
           "station": "תחנת רכבת", "dog_park": "גינת כלבים", "beach": "חוף", "atm": "כספומט", "bank": "בנק", "post_office": "סניף דואר",
           "cafe": "בית קפה", "restaurant": "מסעדה", "bakery": "מאפייה", "greengrocer": "ירקן", "fitness_centre": "חדר כושר",
           "sports_centre": "מרכז ספורט", "library": "ספרייה", "swimming_pool": "בריכה", "ice_cream": "גלידרייה", "fast_food": "אוכל מהיר",
           "subway_entrance": "כניסה לתחנה", "halt": "תחנת רכבת", "hospital": "בית חולים", "mall": "קניון", "chemist": "פארם"}


# findplace's categories into the seven groups (hotels, parking, bike docks, wellness salons and construction stay out:
# construction is its own layer later); a light-rail station marked future is a planned station, never a running one
FP_GROUP = {"school": "education", "kindergarten": "education", "daycare": "education", "library": "education",
            "park": "outdoors", "dog_park": "outdoors", "playground": "outdoors", "beach": "outdoors", "sport": "outdoors", "gym": "outdoors",
            "lrt_station": "transport", "transit_stop": "transport",
            "cafe": "food", "restaurant": "food", "bar": "food", "bakery": "food",
            "supermarket": "essentials", "shopping": "essentials", "pharmacy": "essentials", "bank": "essentials",
            "health": "health", "community": "community", "culture": "community", "worship": "community"}
FP_KIND = {"lrt_station": "tram_stop", "transit_stop": "bus_stop"}
FP = os.path.join(REPO, "scripts", "project-stage", "data", "findplace-north-tlv-discovery-v2.geojson")


def findplace():
    d = json.load(io.open(FP, encoding="utf-8"))
    out = []
    for f in d["features"]:
        pr = f.get("properties", {}); c = pr.get("c")
        g = FP_GROUP.get(c)
        if not g or not pr.get("n"):
            continue
        ln, la = f["geometry"]["coordinates"][:2]
        out.append({"src_id": "fp:" + str(f.get("id", "")).strip(), "g": g, "k": FP_KIND.get(c, c), "name": pr["n"].strip(), "lat": la, "lng": ln,
                    "src": pr.get("s", "tlv"), "addr": pr.get("a"), "web": pr.get("w"), "page": pr.get("p"), "future": 1 if pr.get("f") else 0})
    return out


# the municipal licence layer sometimes names the licence holder, not the place a buyer knows: the company suffix goes, a
# name that is only a company drops to the end of every list ('corp'); a few kinds sit in the wrong group of the source
CORP = re.compile(r"\s*(בע[\"״”]?מ|בע\"מ|\(\d+\)|ע\.ר\.?|ltd\.?|inc\.?)\s*$", re.I)
NOT_IN = {"education": re.compile(r"אקדמיה ל|academy|סטודיו|studio|קורס", re.I),
          "outdoors": re.compile(r"כיבוי אש|משטרה|תחנת דלק|חניון", re.I)}


def clean(p):
    n = p["name"]
    if re.search(r"בע[\"״”]?מ|ltd|inc", n, re.I):
        p["corp"] = 1
    n = CORP.sub("", n).strip(" -–,")
    p["name"] = n
    rx = NOT_IN.get(p["g"])
    return bool(n) and not (rx and rx.search(n))


def norm_name(n):
    return re.sub(r"[\s\"'׳״\-.,()]", "", (n or "").lower())


def group_of(t):
    am, sh, le, rw, hw = t.get("amenity", ""), t.get("shop", ""), t.get("leisure", ""), t.get("railway", ""), t.get("highway", "")
    if am in ("school", "kindergarten", "library", "college", "university", "childcare"):
        return "education", am
    if le in ("park", "playground", "garden", "sports_centre", "fitness_centre", "pitch", "dog_park", "swimming_pool") or t.get("natural") == "beach":
        return "outdoors", le or "beach"
    if rw or hw == "bus_stop":
        return "transport", rw or "bus_stop"
    if am in ("cafe", "restaurant", "ice_cream", "fast_food", "bar", "pub"):
        return "food", am
    if sh or am in ("pharmacy", "post_office", "bank", "atm"):
        return "essentials", sh or am
    if am in ("clinic", "doctors", "hospital", "dentist") or t.get("healthcare"):
        return "health", am or t.get("healthcare")
    if am in ("community_centre", "place_of_worship", "theatre", "arts_centre", "cinema"):
        return "community", am
    return None, None


# ---------------------------------------------------------------- 2. what the windows see (city.json)
CITY = json.load(io.open(os.path.join(RB, "city.json"), encoding="utf-8"))
BLD = []
for b in CITY["b"]:
    h, pts = float(b[0]), b[3:]
    poly = [(pts[i], pts[i + 1]) for i in range(0, len(pts) - 1, 2)]
    xs, zs = [p[0] for p in poly], [p[1] for p in poly]
    BLD.append((h, poly, (min(xs), min(zs), max(xs), max(zs))))


def inside(poly, x, z):
    c = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, zi = poly[i]; xj, zj = poly[j]
        if (zi > z) != (zj > z) and x < (xj - xi) * (z - zi) / (zj - zi + 1e-12) + xi:
            c = not c
        j = i
    return c


def host(x, z):
    """the building a place stands in (its height), or None"""
    for h, poly, bb in BLD:
        if bb[0] <= x <= bb[2] and bb[1] <= z <= bb[3] and inside(poly, x, z):
            return h, poly
    return None


def seg_hits(poly, ax, az, bx, bz):
    """the parameters t along a->b where it crosses the polygon's edges"""
    out = []
    dx, dz = bx - ax, bz - az
    for i in range(len(poly)):
        x1, z1 = poly[i]; x2, z2 = poly[(i + 1) % len(poly)]
        ex, ez = x2 - x1, z2 - z1
        den = dx * ez - dz * ex
        if abs(den) < 1e-9:
            continue
        t = ((x1 - ax) * ez - (z1 - az) * ex) / den
        u = ((x1 - ax) * dz - (z1 - az) * dx) / den
        if 0 <= t <= 1 and 0 <= u <= 1:
            out.append(t)
    return out


def visible(eye, target, skip=None):
    """a straight sight line from eye (x, z, h) to target (x, z, h) passes over or beside every building of the layer"""
    ax, az, ah = eye; bx, bz, bh = target
    mnx, mxx, mnz, mxz = min(ax, bx), max(ax, bx), min(az, bz), max(az, bz)
    for h, poly, bb in BLD:
        if poly is skip or bb[2] < mnx or bb[0] > mxx or bb[3] < mnz or bb[1] > mxz:
            continue
        ts = seg_hits(poly, ax, az, bx, bz)
        if inside(poly, ax, az):
            ts.append(0.0)
        for t in ts:
            if t > 0.999:
                continue
            if ah + (bh - ah) * t < h:        # the line passes below the roof where it meets the building
                return False
    return True


def sight(x, z):
    """per floor: 'street' (the place itself), 'roof' (only its building's top), or None (hidden)"""
    hb = host(x, z)
    tx, tz = xz(*TOWER)
    out = {}
    for fl, eh in FLOORS.items():
        # the eye stands at the tower's glass on the side facing the place (half the tower's width out, about 12 m)
        d = math.hypot(x - tx, z - tz) or 1.0
        ex, ez = tx + (x - tx) / d * 12.0, tz + (z - tz) / d * 12.0
        if hb is None:
            out[str(fl)] = "street" if visible((ex, ez, eh), (x, z, 2.0)) else None
        else:
            h, poly = hb
            out[str(fl)] = "roof" if visible((ex, ez, eh), (x, z, h + 0.5), skip=poly) else None
    return out


# ---------------------------------------------------------------- 3. walking (Mapbox)
def walk_minutes(tok, lat, lng):
    def fetch():
        url = ("https://api.mapbox.com/directions/v5/mapbox/walking/%.6f,%.6f;%.6f,%.6f?overview=false&access_token=%s"
               % (TOWER[1], TOWER[0], lng, lat, tok))
        try:
            d = json.load(urllib.request.urlopen(url, timeout=30))
            r = (d.get("routes") or [None])[0]
            return {"s": r["duration"], "m": r["distance"]} if r else {"s": None, "m": None}
        except Exception as e:
            print("walk failed", str(e)[:80]); return None
    d = cached_json("walk-%.5f-%.5f.json" % (lat, lng), fetch)
    time.sleep(0.05)
    return (max(1, round(d["s"] / 60)), round(d["m"])) if d and d.get("s") else (None, None)


def isochrones(tok):
    def fetch():
        url = ("https://api.mapbox.com/isochrone/v1/mapbox/walking/%.6f,%.6f?contours_minutes=5,10,15&polygons=true&denoise=1&generalize=10&access_token=%s"
               % (TOWER[1], TOWER[0], tok))
        return json.load(urllib.request.urlopen(url, timeout=30))
    d = cached_json("isochrone.json", fetch)
    out = []
    for f in (d or {}).get("features", []):
        ring = f["geometry"]["coordinates"][0]
        out.append({"min": f["properties"]["contour"], "ring": [[round(p[0], 6), round(p[1], 6)] for p in ring]})
    return sorted(out, key=lambda r: r["min"])


def main():
    no_walk = "--no-walk" in sys.argv
    tok = None if no_walk else token()
    raw = cached_json("overpass.json", overpass)
    if not raw:
        sys.exit("Overpass gave nothing")
    places, seen = [], set()
    # 1. findplace first
    for f in findplace():
        d, br = dist_bearing(f["lat"], f["lng"])
        if d > RADIUS:
            continue
        x, z = xz(f["lat"], f["lng"])
        p = {"id": f["src_id"], "g": f["g"], "k": f["k"], "name": f["name"], "lat": round(f["lat"], 6), "lng": round(f["lng"], 6),
             "x": round(x, 1), "z": round(z, 1), "dist": d, "bearing": br, "src": f["src"]}
        if f.get("addr"): p["addr"] = f["addr"]
        if f.get("page"): p["fp"] = "https://findplace.co.il/he/" + f["page"].lstrip("/")
        if f.get("future"): p["future"] = 1
        places.append(p)
    fp_count = len(places)
    # 2. OpenStreetMap: what findplace lacks, and other-language names for what it has
    for e in raw["elements"]:
        t = e.get("tags", {})
        la = e.get("lat", (e.get("center") or {}).get("lat")); ln = e.get("lon", (e.get("center") or {}).get("lon"))
        if la is None or ln is None:
            continue
        g, kind = group_of(t)
        if not g:
            continue
        pid = "osm:%s/%s" % (e["type"], e["id"])
        if pid in seen:
            continue
        seen.add(pid)
        d, br = dist_bearing(la, ln)
        if d > RADIUS:
            continue
        name = t.get("name:he") or t.get("name") or ""
        generic = not name
        if generic:
            name = GENERIC.get(kind, "")
            if not name:
                continue
        x, z = xz(la, ln)
        p = {"id": pid, "g": g, "k": kind, "name": name, "lat": round(la, 6), "lng": round(ln, 6), "x": round(x, 1), "z": round(z, 1),
             "dist": d, "bearing": br}
        names = {l: t["name:" + l] for l in ("en", "ru", "fr", "ar") if t.get("name:" + l)}
        if t.get("name") and not t.get("name:he") and re.search(r"[A-Za-z]", t["name"]):
            names.setdefault("en", t["name"])
        if names:
            p["names"] = names
        if generic:
            p["generic"] = 1
        p["src"] = "osm"
        twin = None
        for q in places[:fp_count]:
            if q["g"] != g or abs(q["lat"] - p["lat"]) > 0.0006 or abs(q["lng"] - p["lng"]) > 0.0007:
                continue
            if math.hypot((q["lat"] - p["lat"]) * M_LAT, (q["lng"] - p["lng"]) * M_LNG) > 40:
                continue
            a, b = norm_name(q["name"]), norm_name(p["name"])
            if generic or a == b or (a and b and (a in b or b in a)):
                twin = q
                break
        if twin is not None:
            if names:
                twin.setdefault("names", {}).update({k: v for k, v in names.items() if k not in twin.get("names", {})})
            if twin["src"] == "tlv":
                twin["src"] = "tlv+osm"
            continue
        places.append(p)
    # bus stops: the nearest 14 (a map of every stop reads as noise); every other kind in full
    bus = sorted([p for p in places if p["k"] == "bus_stop"], key=lambda p: p["dist"])
    print("findplace", fp_count, "osm added", len(places) - fp_count)
    drop = set(p["id"] for p in bus[14:])
    places = [p for p in places if p["id"] not in drop]
    # generic duplicates at the same spot (two 'פארק' ways of one park): keep one
    keep, spots = [], set()
    for p in sorted(places, key=lambda p: (p.get("generic", 0), p["dist"])):
        key = (p["name"], round(p["lat"], 4), round(p["lng"], 4))
        if key in spots:
            continue
        spots.add(key); keep.append(p)
    places = sorted([p for p in keep if clean(p)], key=lambda p: p["dist"])
    for p in places:
        p["sight"] = sight(p["x"], p["z"])
        if tok:
            p["walk"], p["route_m"] = walk_minutes(tok, p["lat"], p["lng"])
    q = json.load(io.open(os.path.join(RB, "quarter.json"), encoding="utf-8"))
    landmarks = []
    for it in q.get("places", []):
        lm = {k: it[k] for k in ("kind", "name", "pin", "status", "x", "z", "dist", "bearing", "walk", "src") if k in it}
        lm["sight"] = sight(it["x"], it["z"])
        landmarks.append(lm)
    out = {
        "v": 1, "generated_at": time.strftime("%Y-%m-%d"),
        "note": "AreaLife v97: the places around Rainbow. findplace.co.il's frozen discovery file (Tel Aviv-Yafo municipality open "
                "data + OpenStreetMap, 27.8.2026, sha256 2909a0c2...), then OpenStreetMap (ODbL, (c) OpenStreetMap contributors) via Overpass, "
                "%s; walking minutes: Mapbox Directions, walking profile, from the tower; what the windows see: the city's buildings "
                "layer (GIS 513) with a straight sight line, the new projects around not included. Landmarks: quarter.json (find-place: "
                "TLV OpenData + OSM)." % time.strftime("%d.%m.%Y"),
        "src": {"osm": "OpenStreetMap, %s" % (time.strftime("%-m.%Y") if os.name != "nt" else time.strftime("%#m.%Y")),
                "tlv": "עיריית תל אביב-יפו, מידע פתוח, 8.2026", "fp": "findplace.co.il",
                "walk": "Mapbox, מסלול הליכה", "sight": "שכבת המבנים של עיריית תל אביב-יפו"},
        "tower": {"lat": TOWER[0], "lng": TOWER[1]},
        "groups": ["education", "outdoors", "transport", "food", "essentials", "health", "community"],
        "places": places, "landmarks": landmarks,
        "iso": isochrones(tok) if tok else [],
    }
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n")
    from collections import Counter
    print("places", len(places), dict(Counter(p["g"] for p in places)))
    for fl in ("10", "25", "36"):
        print("floor", fl, "street", sum(1 for p in places if p["sight"][fl] == "street"), "roof", sum(1 for p in places if p["sight"][fl] == "roof"))
    print("walk known", sum(1 for p in places if p.get("walk")), "iso", [r["min"] for r in out["iso"]], "bytes", os.path.getsize(OUT))


if __name__ == "__main__":
    main()
