"""Build data.json for the Rova 4 area map prototype and embed a copy into preview.html.

Inputs (all inside this folder unless noted):
  raw/nominatim.json  from geocode.py   (renewal addresses, OSM Nominatim)
  raw/overpass.json   from fetch_osm.py (daily-life places + boundary streets, OSM Overpass)
  raw/projects.json   fetched here on first run (nad-lan.co.il /wp-json/nadlan/v1/project-map
                      + each candidate project page, JSON-LD geo and the stage lat/lng)
Facts for the renewal cards: docs/content/rova-4-2026-10/facts.md (R41-R51) and
docs/research/2026-10-07-kikar-prices/press-facts.md (U1-U12, D1). Wording of the stage column
follows the live table on /north-tel-aviv/rova-4/ (read 7.10.2026).

Stdlib only. Run: python build_data.py
"""
import html as htmllib
import json
import math
import os
import re
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "nad-lan.co.il-area-map-prototype/1.0 (design preview; reads own public pages)"
TODAY = "2026-10-07"
FALLBACK_TA = (32.0853, 34.781806)  # catalogue's city-centre fallback: shared by dozens of pages, never a real position


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


# ---------------------------------------------------------------- geometry helpers
def interp(seq, x):
    """seq: list of (x, y) sorted by x. Linear interpolation, clamped (constant) beyond the ends."""
    if x <= seq[0][0]:
        return seq[0][1]
    if x >= seq[-1][0]:
        return seq[-1][1]
    for (x0, y0), (x1, y1) in zip(seq, seq[1:]):
        if x0 <= x <= x1:
            t = 0 if x1 == x0 else (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return seq[-1][1]


def centreline(points, axis, step):
    """Collapse all nodes of a street (both carriageways, many ways) into one line.
    axis='lat' -> bins along latitude, value = mean longitude (north-south street); 'lng' the other way."""
    bins = {}
    for lat, lng in points:
        k = round((lat if axis == "lat" else lng) / step)
        bins.setdefault(k, []).append((lat, lng))
    out = []
    for k in sorted(bins):
        pts = bins[k]
        out.append((sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)))
    return out  # list of (lat, lng)


def corner(ns_line, ew_line):
    """Meeting point of a north-south line (lng as a function of lat) and an east-west line (lat of lng)."""
    ns = sorted((p[0], p[1]) for p in ns_line)            # (lat, lng)
    ew = sorted((p[1], p[0]) for p in ew_line)            # (lng, lat)
    lat = sum(p[0] for p in ew_line) / len(ew_line)
    for _ in range(30):
        lng = interp(ns, lat)
        lat = interp(ew, lng)
    return lat, interp(ns, lat)


def point_in_poly(lat, lng, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        yi, xi = ring[i][1], ring[i][0]
        yj, xj = ring[j][1], ring[j][0]
        if (yi > lat) != (yj > lat) and lng < (xj - xi) * (lat - yi) / (yj - yi + 1e-15) + xi:
            inside = not inside
        j = i
    return inside


def metres(a_lat, a_lng, b_lat, b_lng):
    dy = (a_lat - b_lat) * 110900
    dx = (a_lng - b_lng) * 110900 * math.cos(math.radians((a_lat + b_lat) / 2))
    return math.hypot(dx, dy)


def dist_to_ring(lat, lng, ring):
    best = 1e12
    for (x0, y0), (x1, y1) in zip(ring, ring[1:]):
        for t in [i / 20 for i in range(21)]:
            best = min(best, metres(lat, lng, y0 + t * (y1 - y0), x0 + t * (x1 - x0)))
    return best


# ---------------------------------------------------------------- boundary
def build_boundary(ov):
    west, south, east, north = [], [], [], []
    for e in ov["elements"]:
        if e["type"] != "way" or "geometry" not in e:
            continue
        t = e.get("tags", {})
        pts = [(g["lat"], g["lon"]) for g in e["geometry"]]
        name = t.get("name", "")
        if t.get("highway") and name == "אבן גבירול":
            west += pts
        elif t.get("highway") and "שאול המלך" in name:
            south += pts
        elif t.get("highway") == "motorway" and ("איילון" in name or t.get("ref") == "20"):
            east += pts
        elif t.get("waterway") == "river" and "ירקון" in name:
            north += pts
    W = centreline(west, "lat", 0.0006)
    S = centreline(south, "lng", 0.0006)
    E = centreline(east, "lat", 0.0006)
    N = centreline(north, "lng", 0.0006)
    sw, nw = corner(W, S), corner(W, N)
    se, ne = corner(E, S), corner(E, N)
    ring = [sw]
    ring += [p for p in sorted(W) if sw[0] < p[0] < nw[0]]
    ring += [nw]
    ring += [p for p in sorted(N, key=lambda p: p[1]) if nw[1] < p[1] < ne[1]]
    ring += [ne]
    ring += [p for p in sorted(E, reverse=True) if se[0] < p[0] < ne[0]]
    ring += [se]
    ring += [p for p in sorted(S, key=lambda p: -p[1]) if sw[1] < p[1] < se[1]]
    ring += [sw]
    coords = [[round(p[1], 6), round(p[0], 6)] for p in ring]
    counts = {"west_nodes": len(west), "south_nodes": len(south), "east_nodes": len(east), "north_nodes": len(north)}
    return coords, counts, {"sw": sw, "nw": nw, "ne": ne, "se": se}


# ---------------------------------------------------------------- projects
PROJECT_FACTS = {
    # url -> (short name shown on the pin, one fact line in the page's own words, developer line or None)
    "https://nad-lan.co.il/projects/hamedina/": ("מגדלי כיכר המדינה", "3 מגדלים בני 40, 40 ו-37 קומות · 453 דירות", None),
    "https://nad-lan.co.il/projects/duo-tel-aviv/": ("DUO", "2 מגדלים בני 54 קומות · 668 דירות", "אפריקה ישראל מגורים"),
    "https://nad-lan.co.il/projects/h-infinity-somail-tel-aviv/": ("H Infinity", "מגדל מגורים ובניין בוטיק · כ-278 דירות", "קבוצת חג'ג'"),
    "https://nad-lan.co.il/projects/yoo-tel-aviv/": ("מגדלי YOO", "2 מגדלים בני 37 ו-41 קומות · כ-300 דירות", "קבוצת חבס"),
    "https://nad-lan.co.il/projects/akirov-towers/": ("מגדלי אקירוב", "3 מגדלים בני 32 קומות · כ-350 דירות", "אלרוב"),
    "https://nad-lan.co.il/projects/park-bavli/": ("פארק בבלי", "4 מגדלים בני 46 קומות · כ-800 דירות", "קבוצת תשובה ואלעד מגורים"),
}
RENEWAL_PAGES = {
    # our own renewal-compound pages inside the quarter (data.gov.il urban-renewal register, via the page)
    "https://nad-lan.co.il/projects/%d7%90%d7%a8%d7%9c%d7%95%d7%96%d7%95%d7%a8%d7%95%d7%91/": {
        "id": "page-arlozorov", "address": "מתחם ארלוזורוב", "before": "57 דירות", "after": "248 דירות",
        "developer": None, "stage": "תכנית מאושרת לפני מימוש, 2023",
        "note": "תכנית 507-0634923 · המיקום בקירוב",
    },
    "https://nad-lan.co.il/projects/%d7%93%d7%a4%d7%a0%d7%94/": {
        "id": "page-dafna", "address": "מתחם דפנה", "before": None, "after": None,
        "developer": None, "stage": "תכנית מאושרת במימוש, 2015",
        "note": "תכנית תא/3885 · המיקום בקירוב",
        # the page prints 1,434 units total, 471 existing, 517 added: they do not add up, so no unit line here
    },
}


def fetch_projects():
    path = os.path.join(RAW, "projects.json")
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))
    out = {"retrieved": now(), "catalogue_url": "https://nad-lan.co.il/wp-json/nadlan/v1/project-map", "pages": {}}
    cat = json.loads(get(out["catalogue_url"]))
    out["catalogue"] = [it for it in cat["items"] if 32.06 <= it["lat"] <= 32.11 and 34.77 <= it["lng"] <= 34.81]
    for it in out["catalogue"]:
        if (it["lat"], it["lng"]) == FALLBACK_TA:
            continue
        s = get(it["url"])
        geo = re.findall(r'"geo":\{"@type":"GeoCoordinates","latitude":([\d.]+),"longitude":([\d.]+)\}', s)
        stage = re.findall(r'&quot;lat&quot;:([\d.]+),&quot;lng&quot;:([\d.]+)', s)
        title = re.search(r"<title>(.*?)</title>", s, re.S)
        out["pages"][it["url"]] = {
            "retrieved": now(), "jsonld_geo": geo[:1], "stage_latlng": stage[:1],
            "title": htmllib.unescape(title.group(1)).strip() if title else "",
        }
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return out


# ---------------------------------------------------------------- renewal rows
ICE28 = "https://www.ice.co.il/realestate/news/article/1110810"
BIZ5 = "https://www.bizportal.co.il/realestates/news/article/20044073"
RENEWAL = [
    {"id": "zlotisti-4", "address": "זלוציסטי 4", "geo": ["zlotisti-4"], "before": "4 קומות, 12 דירות",
     "after": "8 קומות, 22 דירות", "developer": None, "stage": "נהרס, 2.2026",
     "facts": ["R41", "U1"], "sources": [ICE28, BIZ5], "source_date": "28.4.2026; 5.10.2026"},
    {"id": "remez-27", "address": "רמז 27", "geo": ["remez-27"], "before": "4 קומות, 14 דירות",
     "after": "9 קומות, 24 דירות", "developer": None, "stage": "נהרס, 2.2026",
     "facts": ["R42", "U2"], "sources": [ICE28, BIZ5], "source_date": "28.4.2026; 5.10.2026"},
    {"id": "jabotinsky-152", "address": "ז'בוטינסקי 152", "geo": ["jabotinsky-152"], "before": "4 קומות, 20 דירות",
     "after": "8 קומות, 38 דירות", "developer": "בית וגג", "stage": "סיום צפוי ברבעון האחרון של 2028",
     "facts": ["R43", "U3"], "sources": ["https://www.bizportal.co.il/realestates/news/article/20030456"], "source_date": "16.4.2026"},
    {"id": "beeri-36-56", "address": "בארי 36 עד 56, הצד הזוגי", "geo": ["beeri-36", "beeri-56"],
     "before": "11 בניינים, כ-190 דירות", "after": "עד כ-500 דירות, לפי הערכת החברה", "developer": "אדם שוסטר",
     "stage": "נבחרה במכרז הדיירים, 3.2026", "facts": ["R44", "U4"],
     "sources": ["https://www.nadlancenter.co.il/article/14246", BIZ5], "source_date": "31.3.2026; 5.10.2026"},
    {"id": "jabotinsky-135-137", "address": "ז'בוטינסקי 135 עד 137", "geo": ["jabotinsky-135", "jabotinsky-137"],
     "before": "32 דירות", "after": "9 קומות, 68 דירות", "developer": "אפריקה התחדשות ובית וגג",
     "stage": "נחתם חוזה ביצוע, 8.2024", "facts": ["R45", "U5"],
     "sources": ["https://www.nadlancenter.co.il/article/10453"], "source_date": "18.8.2024"},
    {"id": "jabotinsky-133", "address": "ז'בוטינסקי 133", "geo": ["jabotinsky-133"], "before": "16 דירות",
     "after": "9 קומות, 33 דירות", "developer": "בית וגג", "stage": "הבניין הישן נהרס, 11.2025",
     "facts": ["R46", "U6"], "sources": ["https://www.nadlancenter.co.il/article/13382"], "source_date": "3.12.2025"},
    {"id": "remez-44", "address": "רמז 44", "geo": ["remez-44"], "before": None, "after": "7 קומות, 25 דירות",
     "developer": "אנשי העיר", "stage": "היתר בנייה, 9.12.2025", "facts": ["R47", "U7"],
     "sources": ["https://www.nadlancenter.co.il/article/13436"], "source_date": "10.12.2025"},
    {"id": "remez-42", "address": "רמז 42", "geo": ["remez-42"], "before": None, "after": "20 דירות",
     "developer": "אנשי העיר", "stage": "בקשה להיתר", "facts": ["R47", "U8"],
     "sources": ["https://www.nadlancenter.co.il/article/13436"], "source_date": "10.12.2025"},
    {"id": "remez-25", "address": "רמז 25", "geo": ["remez-25"], "before": None, "after": "26 דירות",
     "developer": "אנשי העיר", "stage": "הדיירים פונו", "facts": ["R47", "U8"],
     "sources": ["https://www.nadlancenter.co.il/article/13436"], "source_date": "10.12.2025"},
    {"id": "remez-22", "address": "רמז 22", "geo": ["remez-22"], "before": None, "after": "32 דירות",
     "developer": "אנשי העיר", "stage": "אישור ועדה", "facts": ["R47", "U8"],
     "sources": ["https://www.nadlancenter.co.il/article/13436"], "source_date": "10.12.2025"},
    {"id": "lissin-27", "address": "ליסין 27", "geo": ["lissin-27"], "before": "4 קומות, 12 דירות",
     "after": "7 קומות, 21 דירות", "developer": "יעז יזמות", "stage": "היתר בנייה, 7.2026",
     "facts": ["R48", "U9"], "sources": ["https://www.nadlancenter.co.il/article/15116"], "source_date": "5.8.2026"},
    {"id": "sharet-30", "address": "שרת 30", "geo": ["sharet-30"], "before": "4 קומות, 11 דירות",
     "after": "8 קומות, 24 דירות", "developer": "יעז יזמות", "stage": "היתר בנייה, 7.2026",
     "facts": ["R49", "U10"], "sources": ["https://www.nadlancenter.co.il/article/15116"], "source_date": "5.8.2026"},
    {"id": "zichron-yaakov-16", "address": "זכרון יעקב 16", "geo": ["zichron-yaakov-16"],
     "before": "3 קומות על עמודים, 12 דירות", "after": "7 קומות, 26 דירות", "developer": "קבוצת לוינשטיין",
     "stage": "ההריסה החלה 24.11.2024, אכלוס צפוי במחצית השנייה של 2028", "facts": ["R50", "U11"],
     "sources": ["https://www.ice.co.il/realestate/news/article/1039645"], "source_date": "25.11.2024"},
    {"id": "henkin-3", "address": "חנקין 3", "geo": ["henkin-3"], "before": None, "after": None,
     "developer": "נוגה", "stage": "פרויקט הריסה ובנייה", "facts": ["R51", "U12", "D1"],
     "sources": [ICE28, BIZ5], "source_date": "28.4.2026; 5.10.2026"},
]

# ---------------------------------------------------------------- daily life
def classify(t):
    a, shop, leis, rw, pt = t.get("amenity"), t.get("shop"), t.get("leisure"), t.get("railway"), t.get("public_transport")
    if a == "school":
        return "edu", "בית ספר"
    if a == "kindergarten":
        return "edu", "גן ילדים"
    if leis == "park":
        return "parks", "פארק"
    if shop == "supermarket":
        return "shop", "סופרמרקט"
    if a == "cafe":
        return "shop", "בית קפה"
    if a == "pharmacy":
        return "shop", "בית מרקחת"
    if rw in ("station", "halt", "stop", "tram_stop") or pt == "station":
        if t.get("light_rail") == "yes" or t.get("station") == "light_rail" or t.get("subway") == "yes" or rw == "tram_stop":
            return "transit", "תחנת הרכבת הקלה"
        if t.get("train") == "yes" or rw in ("station", "halt"):
            return "transit", "תחנת רכבת"
        if t.get("bus") == "yes":
            return "transit", "מסוף אוטובוסים"
        return None
    return None


def build_places(ov, ring):
    retrieved = ov["_retrieved"]
    places, dropped = [], {"unnamed": 0, "outside": 0, "duplicate": 0, "other": 0, "stop_position": 0}
    for e in ov["elements"]:
        t = e.get("tags", {})
        if e["type"] == "way" and "geometry" in e:
            continue  # boundary lines
        if e["type"] == "relation" and t.get("boundary"):
            continue
        c = classify(t)
        if not c:
            dropped["other"] += 1
            continue
        if t.get("railway") == "stop" or t.get("public_transport") == "stop_position":
            dropped["stop_position"] += 1
            continue
        name = t.get("name:he") or t.get("name")
        if not name:
            dropped["unnamed"] += 1
            continue
        lat = e.get("lat", e.get("center", {}).get("lat"))
        lng = e.get("lon", e.get("center", {}).get("lon"))
        if lat is None:
            dropped["other"] += 1
            continue
        inside = point_in_poly(lat, lng, ring)
        edge = None
        if not inside:
            d = dist_to_ring(lat, lng, ring)
            if c[0] == "transit" and d <= 250:
                edge = round(d)
            else:
                dropped["outside"] += 1
                continue
        addr = " ".join(x for x in [t.get("addr:street"), t.get("addr:housenumber")] if x)
        places.append({
            "id": f"osm-{e['type']}-{e['id']}", "cat": c[0], "type": c[1], "name": name.strip(),
            "lat": round(lat, 6), "lng": round(lng, 6), "addr": addr or None,
            "edge_m": edge,
            "source": "OpenStreetMap (Overpass API)",
            "source_url": f"https://www.openstreetmap.org/{e['type']}/{e['id']}",
            "retrieved": retrieved,
        })
    # one pin per name and category within 120 m (a school mapped as both a point and an area, a station's parts)
    keep = []
    for p in places:
        dup = next((k for k in keep if k["cat"] == p["cat"] and k["name"] == p["name"]
                    and metres(k["lat"], k["lng"], p["lat"], p["lng"]) < 120), None)
        if dup:
            dropped["duplicate"] += 1
            continue
        keep.append(p)
    keep.sort(key=lambda p: (p["cat"], p["type"], p["name"]))
    return keep, dropped


# ---------------------------------------------------------------- main
def main():
    nom = json.load(open(os.path.join(RAW, "nominatim.json"), encoding="utf-8"))
    ov = json.load(open(os.path.join(RAW, "overpass.json"), encoding="utf-8"))
    pj = fetch_projects()

    ring, bcounts, corners = build_boundary(ov)
    rels = [e for e in ov["elements"] if e["type"] == "relation" and e.get("tags", {}).get("boundary")]
    boundary = {
        "type": "Feature",
        "properties": {
            "label": "גבולות הרובע, בקירוב",
            "method": "No OSM boundary relation for Rova 4 in the box (relations seen: %d). Line built from the OSM "
                      "geometry of the four boundary lines named in facts.md R1: אבן גבירול (west), נתיבי איילון "
                      "(east), נחל הירקון (north), שדרות שאול המלך (south); carriageways averaged, corners where "
                      "the lines meet (extended straight where a street stops short)." % len(rels),
            "nodes_used": bcounts,
            "corners": {k: [round(v[0], 6), round(v[1], 6)] for k, v in corners.items()},
            "source": "OpenStreetMap (Overpass API); boundary text: he.wikipedia רובעי תל אביב-יפו (facts.md R1)",
            "retrieved": ov["_retrieved"],
        },
        "geometry": {"type": "Polygon", "coordinates": [ring]},
    }

    # projects
    projects, projects_out = [], []
    for it in pj["catalogue"]:
        url = it["url"]
        if (it["lat"], it["lng"]) == FALLBACK_TA:
            projects_out.append({"url": url, "title": it["title"], "why": "catalogue city-centre fallback position, no real coordinate"})
            continue
        if url in RENEWAL_PAGES:
            continue
        inside = point_in_poly(it["lat"], it["lng"], ring)
        if not inside:
            projects_out.append({"url": url, "title": it["title"], "why": "outside the quarter line",
                                 "lat": it["lat"], "lng": it["lng"]})
            continue
        if url not in PROJECT_FACTS:
            projects_out.append({"url": url, "title": it["title"], "why": "inside, but no fact line prepared (review)"})
            continue
        page = pj["pages"].get(url, {})
        short, fact, dev = PROJECT_FACTS[url]
        lat, lng, how = it["lat"], it["lng"], "page JSON-LD geo (same as the catalogue)"
        alt = None
        if url.endswith("/duo-tel-aviv/") and page.get("stage_latlng"):
            # the brief's DUO point is the stage position printed on the page; JSON-LD sits ~17 m away
            lat, lng = float(page["stage_latlng"][0][0]), float(page["stage_latlng"][0][1])
            how = "stage lat/lng printed in the page HTML"
            alt = {"jsonld_geo": [float(x) for x in page["jsonld_geo"][0]]}
        projects.append({
            "id": url.rstrip("/").split("/")[-1], "name": short, "title": page.get("title") or it["title"],
            "fact": fact, "developer": dev, "url": url, "lat": lat, "lng": lng,
            "hero": url.endswith("/hamedina/"),
            "source": "nad-lan.co.il project page", "source_url": url, "position_from": how,
            "alt_position": alt, "retrieved": page.get("retrieved", pj["retrieved"]),
        })
    projects.sort(key=lambda p: (not p["hero"], p["name"]))

    # renewal (press rows geocoded + our own compound pages)
    renewal, unplaced = [], []
    for row in RENEWAL:
        hits = []
        for key in row["geo"]:
            entry = nom.get(key, {})
            res = [x for x in entry.get("results", []) if x.get("address", {}).get("house_number")]
            if res:
                att = entry["attempts"][entry["chosen_attempt"]]
                hits.append({"query": att["q"], "url": att["url"], "retrieved": att["retrieved"],
                             "lat": float(res[0]["lat"]), "lng": float(res[0]["lon"]),
                             "osm": f"{res[0]['osm_type']}/{res[0]['osm_id']}",
                             "osm_display_name": res[0]["display_name"], "addresstype": res[0].get("addresstype")})
        base = {k: row[k] for k in ("id", "address", "before", "after", "developer", "stage", "facts", "sources", "source_date")}
        if len(hits) != len(row["geo"]):
            base["why_unplaced"] = "Nominatim matched the street only, no house number"
            base["nominatim_tried"] = [a["q"] for k in row["geo"] for a in nom.get(k, {}).get("attempts", [])]
            unplaced.append(base)
            continue
        lat = sum(h["lat"] for h in hits) / len(hits)
        lng = sum(h["lng"] for h in hits) / len(hits)
        if not point_in_poly(lat, lng, ring):
            base["why_unplaced"] = "geocoded outside the quarter line"
            base["geocode"] = hits
            unplaced.append(base)
            continue
        base.update({"lat": round(lat, 6), "lng": round(lng, 6), "geocode": hits,
                     "position_from": "OSM Nominatim" + (" (midpoint of %d addresses)" % len(hits) if len(hits) > 1 else ""),
                     "url": None})
        renewal.append(base)
    for url, meta in RENEWAL_PAGES.items():
        it = next((x for x in pj["catalogue"] if x["url"] == url), None)
        if not it:
            continue
        page = pj["pages"].get(url, {})
        lat, lng = it["lat"], it["lng"]
        row = dict(meta)
        row.update({"facts": [], "sources": [url, "https://data.gov.il (מאגר התחדשות עירונית, via the page)"],
                    "source_date": "page read 7.10.2026", "url": url, "lat": lat, "lng": lng,
                    "position_from": "page JSON-LD geo; precision not stated, shown as approximate",
                    "retrieved": page.get("retrieved", pj["retrieved"])})
        if point_in_poly(lat, lng, ring):
            renewal.append(row)
        else:
            row["why_unplaced"] = "outside the quarter line"
            unplaced.append(row)

    places, dropped = build_places(ov, ring)
    counts = {
        "projects": len(projects), "renewal": len(renewal),
        "edu": sum(p["cat"] == "edu" for p in places), "parks": sum(p["cat"] == "parks" for p in places),
        "shop": sum(p["cat"] == "shop" for p in places), "transit": sum(p["cat"] == "transit" for p in places),
    }
    data = {
        "key": "rova-4",
        "updated": TODAY,
        "page": "https://nad-lan.co.il/north-tel-aviv/rova-4/",
        "view": {"center": [34.789776, 32.086758], "zoom": 15, "pitch": 55, "bearing": -18,
                 "phone": {"center": [34.7900, 32.0868], "zoom": 14.2, "pitch": 55}},
        "counts": counts,
        "sources": {
            "osm": {"name": "OpenStreetMap contributors", "licence": "ODbL 1.0",
                    "url": "https://www.openstreetmap.org/copyright"},
            "overpass": {"endpoint": ov.get("_endpoint"), "retrieved": ov["_retrieved"]},
            "nominatim": {"endpoint": "https://nominatim.openstreetmap.org/search", "policy": "1 request per second, cached"},
            "catalogue": {"url": pj["catalogue_url"], "retrieved": pj["retrieved"]},
            "facts": ["docs/content/rova-4-2026-10/facts.md", "docs/research/2026-10-07-kikar-prices/press-facts.md"],
        },
        "boundary": boundary,
        "projects": projects,
        "renewal": renewal,
        "places": places,
        "not_placed": {"renewal": unplaced, "projects": projects_out, "places_dropped": dropped},
    }
    json.dump(data, open(os.path.join(HERE, "data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # embed a compact copy in preview.html (between the data script tags)
    prev = os.path.join(HERE, "preview.html")
    if os.path.exists(prev):
        page = open(prev, encoding="utf-8").read()
        lite = {k: data[k] for k in ("key", "updated", "view", "counts", "boundary", "places")}
        lite["projects"] = [{k: v for k, v in p.items() if k not in ("title", "alt_position")} for p in data["projects"]]
        # the page needs the card fields and the position; the geocoding evidence stays in data.json
        lite["renewal"] = [{k: v for k, v in r.items() if k not in ("geocode", "sources", "facts")} for r in data["renewal"]]
        blob = json.dumps(lite, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        page2, n = re.subn(r'(<script id="nlam-data" type="application/json">)(.*?)(</script>)',
                           lambda m: m.group(1) + blob + m.group(3), page, flags=re.S)
        if n == 1:
            open(prev, "w", encoding="utf-8").write(page2)
            print("embedded data into preview.html")
    print(json.dumps(counts, ensure_ascii=False), "unplaced renewal:", [u["id"] for u in unplaced],
          "dropped places:", dropped)
    print("projects outside / skipped:", [(p["title"][:30], p["why"]) for p in projects_out])


if __name__ == "__main__":
    main()
