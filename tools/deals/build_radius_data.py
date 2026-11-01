# -*- coding: utf-8 -*-
"""The data file of the RadiusPrices block (HAD-654, Claude Design v105.5): radius-prices-v1.json (the deals within 500 m,
build_radius_prices.py) plus, per project, the official neighbourhood median that nadlan.gov.il publishes (the public
neighbourhood files the government site itself loads, no token). The project is placed in its municipal neighbourhood
(neighborhoods.geojson, point in polygon) and matched to the official list by name. When the official file has no median
(the new Sde Dov quarter), the nearest neighbourhood that has one is used and marked "near".
Usage: build_radius_data.py <projects.json> <radius-prices-v1.json> <gov dir> <out>  (out: plugins/nadlan-config/data/radius-prices.json)"""
import json, math, os, re, sys, time, urllib.request
PJ, RP, GOV, OUT = sys.argv[1:5]
SRC = r"C:\Users\777\Documents\Codex\2026-08-27\https-www-nadlan-gov-il-https\platform\data\raw\tlv-citywide"
S5000 = os.path.join(GOV, "s5000.json")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130"}


def fetch(url, path):
    if not os.path.exists(path):
        open(path, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read())
        time.sleep(1.2)
    return json.load(open(path, encoding="utf-8-sig"))


def norm(s):
    s = re.sub(r"[\"'׳״()]", "", str(s)).replace("-", " ").replace("ככר", "כיכר")
    s = re.sub(r"\bנוה\b", "נווה", s)
    return re.sub(r"\s+", " ", s).strip()


def inside(pt, ring):
    x, y, c = pt[1], pt[0], False
    for i in range(len(ring)):
        x1, y1 = ring[i - 1]; x2, y2 = ring[i]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def label(name):
    """The municipal spelling as a reader writes it: "'תכנית ל" -> "תכנית ל׳", "נוה" -> "נווה", "ככר" -> "כיכר"."""
    n = name.strip()
    if n.startswith("'"):
        n = n[1:].strip() + "׳"
    n = re.sub(r"\bנוה\b", "נווה", n).replace("ככר", "כיכר").replace("רמת-אביב", "רמת אביב").replace("הדר-יוסף", "הדר יוסף")
    return re.sub(r"\s*-\s*", ", ", n)


def centroid(ring):
    return (sum(p[1] for p in ring) / len(ring), sum(p[0] for p in ring) / len(ring))


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 2 * 6371 * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))


city = fetch("https://data.nadlan.gov.il/api/pages/settlement/buy/5000.json", S5000)
official = {norm(o["title"]): o for o in city["otherNeighborhoods"]}
hoods = []
for f in json.load(open(os.path.join(SRC, "neighborhoods.geojson"), encoding="utf-8"))["features"]:
    g = f["geometry"]
    rings = [g["coordinates"][0]] if g["type"] == "Polygon" else [p[0] for p in g["coordinates"]]
    name = f["properties"]["shem_shchuna"].strip()
    n = norm(name)
    o = official.get(n) or next((v for k, v in official.items() if n.startswith(k) or k.startswith(n)), None)
    hoods.append({"name": name, "rings": rings, "c": centroid(rings[0]), "off": o})


def latest(series, key):
    pts = [g for g in series if g.get(key)]
    if not pts:
        return None
    g = pts[0]
    return {"ils": int(g[key]), "q": (int(g["month"]) + 2) // 3, "y": int(g["year"])}


# outside Tel Aviv-Yafo there are no municipal polygons here: a project is tied by hand to the official neighbourhood next to it
# (R6b, 2.11.2026: the Herzliya marina has no official neighbourhood of its own; Herzliya Pituach is the one beside it)
OUTSIDE = {"marina-towers-herzliya": ("6400", "הרצליה פיתוח")}


def official_of(h, min_points=1):
    o = h["off"]
    if not o:
        return None
    d = fetch(f"https://data.nadlan.gov.il/api/pages/neighborhood/buy/{o['id']}.json", os.path.join(GOV, f"n{o['id']}.json"))
    by = {str(r.get("numRooms", r.get("rooms", r.get("title")))): r["graphData"] for r in d["trends"]["rooms"]}
    allr = latest(by.get("all", []), "neighborhoodPrice")
    if not allr or sum(1 for g in by.get("all", []) if g.get("neighborhoodPrice")) < min_points:
        return None
    return {"id": o["id"], "name": label(h["name"]), "version": d.get("version", ""), "all": allr,
            "rooms": {k: latest(by.get(k, []), "neighborhoodPrice") for k in ("3", "4", "5")}}


rp = json.load(open(RP, encoding="utf-8"))
out = {"source": rp["source"], "official_source": "רשות המסים, כפי שמפורסם באתר nadlan.gov.il", "projects": {}}
for p in json.load(open(PJ, encoding="utf-8")):
    if not p.get("lat"):
        continue
    me = (float(p["lat"]), float(p["lng"]))
    home = next((h for h in hoods if any(inside(me, r) for r in h["rings"])), None)
    rec = dict(rp["projects"].get(str(p["id"]), {"n": 0}))
    rec.pop("pt", None)
    # the new Sde Dov quarter has no official median of its own: a neighbourhood's figure is shown as the NEIGHBOURING one
    sde = "sde-dov" in p["slug"] or p["slug"] == "rainbow-tel-aviv"
    off = official_of(home) if home else None
    near = bool(off) and sde
    if not home and p["slug"] in OUTSIDE:
        sid, title = OUTSIDE[p["slug"]]
        st = fetch(f"https://data.nadlan.gov.il/api/pages/settlement/buy/{sid}.json", os.path.join(GOV, f"s{sid}.json"))
        o = next((v for v in st["otherNeighborhoods"] if norm(v["title"]) == norm(title)), None)
        off = official_of({"off": o, "name": title}, min_points=8) if o else None
        near = bool(off)
    if home and not off:  # outside Tel Aviv-Yafo (Herzliya) nothing is borrowed
        for h in sorted(hoods, key=lambda h: km(me, h["c"])):
            if h is home or km(me, h["c"]) > 1.5:
                continue
            off = official_of(h, min_points=8)
            if off:
                near = True
                break
    rec["hood"] = label(home["name"]) if home else ""
    if off:
        rec["official"] = dict(off, near=near)
    out["projects"][str(p["id"])] = rec
    print(p["slug"], "|", rec["hood"], "|", off and off["name"], "near" if near else "", off and off["all"])
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("written", OUT, os.path.getsize(OUT), "bytes")
