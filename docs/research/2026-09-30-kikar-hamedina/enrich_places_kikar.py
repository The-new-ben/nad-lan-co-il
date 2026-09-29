# -*- coding: utf-8 -*-
"""Kikar Hamedina, P2 (the area), step 3 of 3 (after build_area_kikar.py and build_places.py kikar), 30.9.2026.

  python docs/research/2026-09-30-kikar-hamedina/enrich_places_kikar.py

What it adds to places.json (same schema as assets/project-stage/duo/places.json; new fields are optional extras the
front end ignores: "info", "lines", "rides", "line", "opens", "layer"):
  1. The municipality's own layers (Tel Aviv-Yafo GIS, IView2, public GET) for daily life within 1.5 km: schools and
     kindergartens of the 2026-27 school year (769, 768), recognised daycares (624), health funds' clinics (563), medical
     institutions (565), pharmacies (564), mother-and-baby stations (561), Magen David Adom (560), community (553), culture
     (745), gyms / halls / pools / fields / stadiums (937, 938, 939, 943, 936), playgrounds (696), dog parks (586), public
     gardens (551) and synagogues (568). findplace.co.il's frozen file stops at lat 32.0845 (about 250 m south of the
     plot), so south of it these layers are the city's own record; north of it a place already in the registry is not
     added twice. Only the institution's name, kind and address are kept (never the staff names or phones in the layers).
  2. Bus lines at every stop in the registry: Open Bus Stride (the Public Knowledge Workshop's archive of the Ministry of
     Transport's GTFS), the lines that stopped there on Tuesday 8.9.2026 (a normal weekday, before the holidays), with the
     number of rides that day.
  3. Light rail: every station of the red, green and purple lines within 1.6 km, from the city's layers 423, 764, 766.
     The red line runs (opened 18.8.2023); the purple line is planned for 2028 and the green line's Ibn Gabirol section
     for 2030 (sources in area.md); a station not yet running is marked "future" (the page says "מתוכננת").
  4. Park HaYarkon (OSM relation 16022802, "גני יהושע"): its three nearest edge points, named by the street next to them
     (Nominatim reverse geocoding).
  5. Walking minutes (Mapbox walking profile, the same cache and function as build_places.py) and the provisional sight
     lines for everything added.
  6. sight-landmarks.json: the landmarks a high floor may see, by direction, with coordinates and heights where sourced.
     Visibility itself is NOT computed yet (the towers' model and eye heights come in P5).
"""
import hashlib, io, json, math, os, re, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.argv = [sys.argv[0], "kikar"] + [a for a in sys.argv[1:] if a.startswith("--")]
sys.path.insert(0, os.path.join(REPO, "scripts", "project-stage"))
import build_places as bp        # noqa: E402  (its module code loads kikar's quarter, city and eyes; it also sets utf-8 stdout)

GIS = "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/%d/query"
UA_GIS = {"User-Agent": "Mozilla/5.0 NadLan-CITY/1.0 (nad-lan.co.il; research, read-only)"}
UA_OSM = {"User-Agent": "NadLan-places/1.0 (nad-lan.co.il; research, read-only)"}
STRIDE = "https://open-bus-stride-api.hasadna.org.il"
BUS_DAY = "2026-09-08"
CACHE = os.path.join(REPO, "scripts", "project-stage", "_cache", "kikar-area")
os.makedirs(CACHE, exist_ok=True)
O = bp.TOWER                      # the plot centre (kikar-stage/quarter.json "tower")
R = 1500.0
OUT = bp.OUT
LM_OUT = os.path.join(HERE, "sight-landmarks.json")
TODAY = time.strftime("%Y-%m-%d")


def cached(name, fetch):
    p = os.path.join(CACHE, name)
    if os.path.exists(p):
        return json.load(io.open(p, encoding="utf-8"))
    d = fetch()
    if d is not None:
        io.open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False))
    return d


def http_json(url, headers, data=None, timeout=120, pause=0.6):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            d = json.load(urllib.request.urlopen(req, timeout=timeout))
            time.sleep(pause)
            return d
        except Exception as e:
            print("  retry", url[:90], str(e)[:80])
            time.sleep(3 + 3 * attempt)
    return None


def envelope(c, radius):
    dlat = radius / 110574.0
    dlng = radius / (math.cos(math.radians(c[0])) * 111320.0)
    return "%.6f,%.6f,%.6f,%.6f" % (c[1] - dlng, c[0] - dlat, c[1] + dlng, c[0] + dlat)


def gis_all(layer, radius, fields="*", where="1=1"):
    def fetch():
        out, off = [], 0
        while True:
            q = {"f": "json", "where": where, "geometry": envelope(O, radius), "geometryType": "esriGeometryEnvelope", "inSR": 4326,
                 "spatialRel": "esriSpatialRelIntersects", "outFields": fields, "returnGeometry": "true", "outSR": 4326,
                 "resultOffset": off, "resultRecordCount": 1000}
            d = http_json(GIS % layer + "?" + urllib.parse.urlencode(q), UA_GIS, pause=0.4)
            if not d or "error" in d:
                print("  GIS layer", layer, "error", (d or {}).get("error"))
                break
            f = d.get("features") or []
            out += f
            if not f or not d.get("exceededTransferLimit"):
                break
            off += len(f)
        return out
    return cached("layer-%d-%d.json" % (layer, radius), fetch)


def point_of(g):
    if not g:
        return None
    if "x" in g:
        return g["y"], g["x"]
    if g.get("rings"):
        ring = g["rings"][0][:-1]
        A = cx = cy = 0.0
        for i in range(len(ring)):
            x0, y0 = ring[i]
            x1, y1 = ring[(i + 1) % len(ring)]
            c = x0 * y1 - x1 * y0
            A += c; cx += (x0 + x1) * c; cy += (y0 + y1) * c
        if abs(A) < 1e-15:
            return sum(p[1] for p in ring) / len(ring), sum(p[0] for p in ring) / len(ring)
        return cy / (3 * A), cx / (3 * A)
    return None


def clean_name(s):
    s = re.sub(r"\s+", " ", (s or "").replace("‏", "").replace("‎", "")).strip(" -–,")
    return s


def addr_of(street, num):
    street = clean_name(street)
    if not street:
        return None
    if num in (None, "", 0, "0") or re.search(r"(^|\s)%s\W*$" % re.escape(str(num)), street):
        return street               # some layers already carry the number in the street field
    return street + " %s" % num


# ---------------------------------------------------------------- 1. the city's layers
def s_(a, k):
    v = a.get(k)
    return clean_name(str(v)) if v not in (None, "") else ""


LAYERS = [
    # layer, group, kind(fn), name(fn), info(fn), addr(fn)
    (769, "education", lambda a: "school", lambda a: s_(a, "shem_mosad"),
     lambda a: ", ".join(x for x in (s_(a, "t_shlav_chinuch"), s_(a, "t_zerem")) if x), lambda a: addr_of(a.get("shem_rechov"), a.get("ms_bait"))),
    (768, "education", lambda a: "kindergarten", lambda a: ("גן " + s_(a, "shem_mosad")) if s_(a, "shem_mosad") and not s_(a, "shem_mosad").startswith("גן") else s_(a, "shem_mosad"),
     lambda a: ", ".join(x for x in (s_(a, "t_shlav_chinuch"), s_(a, "t_zerem")) if x), lambda a: addr_of(a.get("shem_rechov"), a.get("ms_bait"))),
    (624, "education", lambda a: "daycare", lambda a: s_(a, "name"), lambda a: s_(a, "type"), lambda a: s_(a, "address") or None),
    (563, "health", lambda a: "clinic", lambda a: s_(a, "shem") or s_(a, "t_kupa"), lambda a: s_(a, "t_kupa"), lambda a: addr_of(a.get("shem_rechov"), a.get("ms_bait"))),
    (565, "health", lambda a: "hospital" if "בית חולים" in s_(a, "t_sug_mosad") else "clinic", lambda a: s_(a, "shem_mosad"), lambda a: s_(a, "t_sug_mosad"),
     lambda a: addr_of(a.get("shem_rechov"), a.get("ms_bait"))),
    (564, "essentials", lambda a: "pharmacy", lambda a: s_(a, "shem"), lambda a: "בית מרקחת", lambda a: addr_of(a.get("shem_rechov"), a.get("ms_bait"))),
    (561, "health", lambda a: "clinic", lambda a: ("טיפת חלב " + s_(a, "shem_thana")) if "טיפת חלב" not in s_(a, "shem_thana") else s_(a, "shem_thana"),
     lambda a: "טיפת חלב", lambda a: s_(a, "Full_Address") or addr_of(a.get("shem_rechov"), a.get("ms_bait"))),
    (560, "health", lambda a: "health", lambda a: "מגן דוד אדום, " + s_(a, "shem_tahana") if s_(a, "shem_tahana") else "", lambda a: "תחנת מד\"א",
     lambda a: addr_of(a.get("shem_rechov"), a.get("ms_bait"))),
    (553, "community", lambda a: "community", lambda a: s_(a, "shem"), lambda a: ", ".join(x for x in (s_(a, "t_sug_rashi"), s_(a, "t_sug_mishni")) if x),
     lambda a: s_(a, "Full_Address") or addr_of(a.get("shem_rechov"), a.get("ms_bait"))),
    (745, "community", lambda a: "culture", lambda a: s_(a, "NAME"), lambda a: s_(a, "MAIN_TARBOT"), lambda a: s_(a, "KTOVET") or None),
    (937, "outdoors", lambda a: "gym", lambda a: s_(a, "facility_name"), lambda a: s_(a, "facility_sport"), lambda a: addr_of(a.get("Street"), a.get("house_number"))),
    (938, "outdoors", lambda a: "sport", lambda a: s_(a, "facility_name"), lambda a: s_(a, "facility_sport"), lambda a: s_(a, "Full_Address") or None),
    (939, "outdoors", lambda a: "swimming_pool", lambda a: s_(a, "facility_name"), lambda a: s_(a, "facility_sport"), lambda a: s_(a, "Full_Address") or None),
    (943, "outdoors", lambda a: "pitch", lambda a: s_(a, "facility_name"), lambda a: s_(a, "facility_sport"), lambda a: s_(a, "Full_Address") or None),
    (936, "outdoors", lambda a: "sport", lambda a: s_(a, "facility_name"), lambda a: s_(a, "facility_sport"), lambda a: s_(a, "Full_Address") or None),
    (696, "outdoors", lambda a: "playground", lambda a: s_(a, "shem_atar"), lambda a: s_(a, "shem_sug_atar"), lambda a: s_(a, "address") or None),
    (586, "outdoors", lambda a: "dog_park", lambda a: s_(a, "shem_gina"), lambda a: "גינת כלבים", lambda a: s_(a, "Full_Address") or None),
    (551, "outdoors", lambda a: "park", lambda a: s_(a, "shem_gan"), lambda a: s_(a, "sug_gan"), lambda a: None),
    (568, "community", lambda a: "worship", lambda a: s_(a, "name_bet_cneset"), lambda a: ("נוסח " + s_(a, "nosah")) if s_(a, "nosah") else "בית כנסת",
     lambda a: s_(a, "ketovet") or addr_of(a.get("name_str"), a.get("bait"))),
]


def norm(n):
    return re.sub(r"[\s\"'׳״\-.,()]", "", (n or "").lower())


def same_name(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return False
    if a == b or (len(a) >= 3 and len(b) >= 3 and (a in b or b in a)):
        return True
    # Hebrew spelling with or without the vowel letters (ארלוזורוב / ארלוזרוב)
    a2, b2 = re.sub("[וי]", "", a), re.sub("[וי]", "", b)
    return len(a2) >= 3 and a2 == b2


def meters(p, lat, lng):
    return math.hypot((p["lat"] - lat) * 111320.0, (p["lng"] - lng) * bp.M_LNG)


def add_place(places, cand, stats):
    """merge into an existing place (same group, same name within 150 m; or the same kind within 12 m), else append"""
    for p in places:
        d = meters(p, cand["lat"], cand["lng"])
        if p["g"] != cand["g"]:
            # the same name at the same spot in another group (findplace files some pharmacies under health): one place
            if not (d <= 30 and norm(p["name"]) == norm(cand["name"])):
                continue
        if (d <= 150 and same_name(p["name"], cand["name"])) or (d <= 12 and (p["k"] == cand["k"] or p.get("generic"))) or p["g"] != cand["g"]:
            for k in ("info", "addr", "lines", "rides", "stop_code", "line", "opens"):
                if cand.get(k) and not p.get(k):
                    p[k] = cand[k]
            if p.get("generic") and not cand.get("generic"):
                p["name"] = cand["name"]
                p.pop("generic", None)
            tag = {"tlv-gis": "gis", "gtfs": "gtfs"}.get(cand["src"])
            if tag and tag not in p["src"]:
                p["src"] = p["src"] + "+" + tag
            stats["merged"] += 1
            return p
    d, br = bp.dist_bearing(cand["lat"], cand["lng"])
    if d > R:
        stats["far"] += 1
        return None
    x, z = bp.xz(cand["lat"], cand["lng"])
    cand.update({"x": round(x, 1), "z": round(z, 1), "dist": d, "bearing": br})
    cand["lat"], cand["lng"] = round(cand["lat"], 6), round(cand["lng"], 6)
    places.append(cand)
    stats["added"] += 1
    return cand


def city_layers(places):
    stats = {"merged": 0, "added": 0, "far": 0, "noname": 0}
    per = {}
    for layer, g, kf, nf, inf, af in LAYERS:
        feats = gis_all(layer, int(R))
        n0 = stats["added"]
        for f in feats:
            a = f.get("attributes") or {}
            pt = point_of(f.get("geometry"))
            if not pt:
                continue
            name = nf(a)
            if layer == 551:
                area = a.get("shetach_gan") or a.get("ms_area") or 0
                try:
                    area = float(area)
                except Exception:
                    area = 0
                if not name or area and area < 800:
                    continue
            if not name:
                stats["noname"] += 1
                continue
            if layer == 696 and s_(a, "shem_sug_atar") == "בית ספר":
                continue          # a school's own yard is not a public playground
            cand = {"id": "tlv:%d/%s" % (layer, a.get("oid_mosad") or a.get("OBJECTID") or a.get("oid") or a.get("oid_kupa") or a.get("oid_merkahat")
                                          or a.get("oid_tahana") or a.get("oid_gina") or a.get("oid_shetach") or a.get("oid_cneset") or len(places)),
                    "g": g, "k": kf(a), "name": name, "lat": pt[0], "lng": pt[1], "src": "tlv-gis", "layer": layer}
            info = inf(a)
            if info:
                cand["info"] = info
            ad = af(a)
            if ad:
                cand["addr"] = ad
            if layer == 745 and s_(a, "NAME_ENG"):
                cand["names"] = {"en": s_(a, "NAME_ENG")}
            add_place(places, cand, stats)
        per[layer] = (len(feats), stats["added"] - n0)
    print("city layers:", stats, per)
    return stats


# ---------------------------------------------------------------- 2. bus lines (Open Bus Stride, GTFS)
def stride_stops_near():
    """every GTFS stop within 700 m of the plot on BUS_DAY, with its lines that day"""
    def fetch():
        stops, off = [], 0          # the API filters by city, not by area: every Tel Aviv stop that day, then 700 m around the plot
        while True:
            r = http_json(STRIDE + "/gtfs_stops/list?" + urllib.parse.urlencode(
                {"date_from": BUS_DAY, "date_to": BUS_DAY, "city": "תל אביב יפו", "limit": 1000, "offset": off}), UA_OSM, timeout=180) or []
            stops += r
            if len(r) < 1000:
                break
            off += 1000
        print("  GTFS stops in Tel Aviv-Yafo on", BUS_DAY, len(stops))
        stops = [s for s in stops if s.get("lat") and bp.dist_bearing(s["lat"], s["lon"])[0] <= 700]
        out = []
        for s in stops:
            lines, off = {}, 0
            while True:
                r = http_json(STRIDE + "/gtfs_ride_stops/list?" + urllib.parse.urlencode(
                    {"gtfs_stop_ids": s["id"], "arrival_time_from": BUS_DAY + "T00:00:00+03:00", "arrival_time_to": BUS_DAY + "T23:59:59+03:00",
                     "limit": 1000, "offset": off}), UA_OSM, timeout=180)
                if not r:
                    break
                for x in r:
                    k = x["gtfs_route__route_short_name"]
                    e = lines.setdefault(k, {"ref": k, "agency": x["gtfs_route__agency_name"], "to": set(), "rides": 0})
                    e["rides"] += 1
                    e["to"].add((x["gtfs_route__route_long_name"] or "").split("<->")[-1].split("-")[0].strip())
                if len(r) < 1000:
                    break
                off += 1000
            out.append({"code": s["code"], "name": s["name"], "lat": s["lat"], "lon": s["lon"],
                        "lines": [{"ref": v["ref"], "agency": v["agency"], "rides": v["rides"], "to": sorted(t for t in v["to"] if t)}
                                  for v in sorted(lines.values(), key=lambda v: -v["rides"])]})
            print("  stop", s["code"], s["name"], len(lines))
        return out
    return cached("stride-%s-700m.json" % BUS_DAY, fetch)


def merge_codes(stops):
    """the archive can hold several stop records of one stop code on a day (platforms): one record per code, lines united"""
    by = {}
    for s in stops:
        e = by.setdefault(s["code"], {"code": s["code"], "name": s["name"], "lat": s["lat"], "lon": s["lon"], "lines": {}})
        for l in s["lines"]:
            x = e["lines"].setdefault(l["ref"], {"ref": l["ref"], "agency": l["agency"], "rides": 0, "to": set()})
            x["rides"] += l["rides"]
            x["to"].update(l.get("to") or [])
    out = []
    for e in by.values():
        e["lines"] = [dict(v, to=sorted(v["to"])) for v in sorted(e["lines"].values(), key=lambda v: -v["rides"])]
        out.append(e)
    return out


def line_key(r):
    m = re.match(r"(\d+)", r)
    return (int(m.group(1)) if m else 9999, r)


def bus_lines(places):
    stops = merge_codes(stride_stops_near())
    print("GTFS stop codes within 700 m:", len(stops))
    used = set()
    n = 0
    for p in places:
        if p["k"] != "bus_stop":
            continue
        best = min(stops, key=lambda s: meters(p, s["lat"], s["lon"]), default=None)
        if best and meters(p, best["lat"], best["lon"]) <= 30 and best["lines"]:
            p["lines"] = sorted({l["ref"] for l in best["lines"]}, key=line_key)
            p["rides"] = sum(l["rides"] for l in best["lines"])
            p["stop_code"] = best["code"]
            used.add(best["code"])
            n += 1
    # the stops the 14-nearest cut left out but that carry many lines (the Namir / Jabotinsky hub): add the busiest
    extra = sorted([s for s in stops if s["code"] not in used and s["lines"]], key=lambda s: -sum(l["rides"] for l in s["lines"]))
    added = 0
    for s in extra:
        rides = sum(l["rides"] for l in s["lines"])
        if rides < 300 or added >= 8:
            continue
        cand = {"id": "gtfs:%s" % s["code"], "g": "transport", "k": "bus_stop", "name": s["name"], "lat": s["lat"], "lng": s["lon"],
                "src": "gtfs", "lines": sorted({l["ref"] for l in s["lines"]}, key=line_key), "rides": rides, "stop_code": s["code"]}
        if add_place(places, cand, {"merged": 0, "added": 0, "far": 0}):
            added += 1
    print("bus stops with lines:", n, "| busy stops added:", added)
    return stops


# ---------------------------------------------------------------- 3. light rail (the city's layers 423, 764, 766)
RAIL = [(423, "red", "האדום", "Red", 0, "פועל מאז 18.8.2023"),
        (766, "purple", "הסגול", "Purple", 1, "מתוכנן להיפתח ב-2028"),
        (764, "green", "הירוק", "Green", 1, "מתוכנן להיפתח עד 2030 (הקטע בתל אביב)")]


def rail(places):
    n = 0
    for layer, key, he, en, future, opens in RAIL:
        for f in gis_all(layer, 1600):
            a, g = f["attributes"], f["geometry"]
            d, _ = bp.dist_bearing(g["y"], g["x"])
            if d > 1600:
                continue
            nm = clean_name(a.get("station_name_HEB"))
            cand = {"id": "tlv:%d/%s" % (layer, a.get("oid")), "g": "transport", "k": "tram_stop", "name": "תחנת %s, הקו %s" % (nm, he),
                    "lat": g["y"], "lng": g["x"], "src": "tlv-gis", "layer": layer, "line": key, "opens": opens,
                    "info": ("תחנה תת־קרקעית" if (a.get("type") or "").strip() == "תחתית" else "תחנה עילית"),
                    "names": {"en": "%s station, %s Line" % (clean_name(a.get("station_name_ENG")) or nm, en)}}
            if future:
                cand["future"] = 1
            # a findplace/OSM entry of the same station keeps its place; it gets the line, the date and the flag
            twin = None
            for p in places:
                if p["k"] in ("tram_stop", "station", "subway_entrance", "halt") and meters(p, g["y"], g["x"]) <= 120 and (same_name(p["name"], nm) or key in (p.get("line") or "")):
                    twin = p
                    break
            if twin is not None and not twin.get("line"):
                twin.update({"line": key, "opens": opens, "names": cand["names"], "name": cand["name"], "info": cand["info"]})
                twin.pop("generic", None)
                if "gis" not in twin["src"]:
                    twin["src"] += "+gis"
                if future:
                    twin["future"] = 1
                else:
                    twin.pop("future", None)
                continue
            if add_place(places, cand, {"merged": 0, "added": 0, "far": 0}):
                n += 1
    print("rail stations added:", n)


# ---------------------------------------------------------------- 4. Park HaYarkon's nearest edges
def reverse(lat, lng):
    def fetch():
        return http_json("https://nominatim.openstreetmap.org/reverse?" + urllib.parse.urlencode(
            {"lat": lat, "lon": lng, "format": "jsonv2", "zoom": 17, "accept-language": "he"}), UA_OSM, pause=1.2)
    return cached("rev-%.6f-%.6f.json" % (lat, lng), fetch)


def yarkon(places):
    d = cached("nominatim-yarkon.json", lambda: http_json("https://nominatim.openstreetmap.org/lookup?" + urllib.parse.urlencode(
        {"osm_ids": "R16022802", "format": "jsonv2", "polygon_geojson": 1, "extratags": 1}), UA_OSM, pause=1.2))
    if not d:
        print("Park HaYarkon: not found")
        return []
    g = d[0]["geojson"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    pts = [(p[1], p[0]) for poly in polys for p in poly[0]]
    # the nearest edge point in each of three directions: north-west, north, north-east
    picks = {}
    for la, ln in pts:
        dd, br = bp.dist_bearing(la, ln)
        sector = "nw" if 300 <= br < 345 else ("n" if br >= 345 or br < 15 else ("ne" if 15 <= br < 75 else None))
        if sector and (sector not in picks or dd < picks[sector][0]):
            picks[sector] = (dd, la, ln)
    out = []
    for sector in ("n", "nw", "ne"):
        if sector not in picks:
            continue
        if out and picks[sector][0] > out[0]["dist"] + 150:
            continue          # only the nearest edge and any other edge about as near (three points on one street read as noise)
        dd, la, ln = picks[sector]
        rv = reverse(la, ln) or {}
        ad = rv.get("address") or {}
        road = ad.get("road") or ad.get("pedestrian") or ad.get("footway") or ""
        name = "פארק הירקון (גני יהושע)" + (", ליד %s" % road if road else "")
        cand = {"id": "osm:relation/16022802#%s" % sector, "g": "outdoors", "k": "park", "name": name, "lat": la, "lng": ln, "src": "osm",
                "info": "הנקודה הקרובה בשולי הפארק (לא בהכרח שער)", "names": {"en": "Park HaYarkon (Ganei Yehoshua)" + (", by %s" % road if road and re.search(r"[A-Za-z]", road) else "")}}
        # the edge is about 1 km away, inside the 1.5 km ring
        x, z = bp.xz(la, ln)
        dist, br = bp.dist_bearing(la, ln)
        cand.update({"x": round(x, 1), "z": round(z, 1), "dist": dist, "bearing": br, "lat": round(la, 6), "lng": round(ln, 6)})
        if any(o["name"] == name for o in out):
            continue
        places.append(cand)
        out.append(cand)
    print("Park HaYarkon edges:", [(c["name"], c["dist"], c["bearing"]) for c in out])
    return out


# ---------------------------------------------------------------- 5. walking from the square's ring road
# The plot is a closed building site inside the ring road ה' באייר (128-147 m from the centre, OSM way 5118376). Mapbox
# snaps the plot centre to the ring's south side (32.08568, 34.789541: 122 m south, checked 30.9.2026), which would add
# about two minutes to every walk north. So each walk starts on the ring, on the side facing the place (the point 138 m
# from the centre on the place's bearing; Mapbox snaps it to the ring road), and the 5/10/15-minute areas are the union of
# four Mapbox walking areas started at the ring's north, east, south and west points. PROVISIONAL until the lobbies'
# doors are known (P5): the towers' permit addresses are ה' באייר 25, 45 and 65 (GIS 499).
RING_R = 138.0


def ring_point(bearing):
    a = math.radians(bearing)
    return O[0] + RING_R * math.cos(a) / 111320.0, O[1] + RING_R * math.sin(a) / bp.M_LNG


def walk_from_ring(tok, lat, lng):
    _, br = bp.dist_bearing(lat, lng)
    s = ring_point(br)

    def fetch():
        url = ("https://api.mapbox.com/directions/v5/mapbox/walking/%.6f,%.6f;%.6f,%.6f?overview=false&access_token=%s"
               % (s[1], s[0], lng, lat, tok))
        try:
            d = json.load(urllib.request.urlopen(url, timeout=30))
            r = (d.get("routes") or [None])[0]
            return {"s": r["duration"], "m": r["distance"]} if r else {"s": None, "m": None}
        except Exception as e:
            print("  walk failed", str(e)[:60])
            return None
    d = bp.cached_json("walkring-%.5f-%.5f-%.5f-%.5f.json" % (s[0], s[1], lat, lng), fetch)
    time.sleep(0.05)
    return (max(1, round(d["s"] / 60)), round(d["m"])) if d and d.get("s") else (None, None)


def inside_ll(ring, lng, lat):
    c = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > lat) != (yj > lat) and lng < (xj - xi) * (lat - yi) / (yj - yi + 1e-15) + xi:
            c = not c
        j = i
    return c


def iso_union(tok):
    rings = {}
    for b in (0, 90, 180, 270):
        s = ring_point(b)

        def fetch(s=s):
            url = ("https://api.mapbox.com/isochrone/v1/mapbox/walking/%.6f,%.6f?contours_minutes=5,10,15&polygons=true&denoise=1&generalize=10&access_token=%s"
                   % (s[1], s[0], tok))
            return json.load(urllib.request.urlopen(url, timeout=30))
        d = bp.cached_json("isoring-%d.json" % b, fetch)
        for f in (d or {}).get("features", []):
            rings.setdefault(f["properties"]["contour"], []).append(f["geometry"]["coordinates"][0])
    out = []
    for m in sorted(rings):
        pts = []
        for a in range(0, 360, 3):
            ar = math.radians(a)
            far = 0
            for r in range(0, 2600, 10):
                la = O[0] + r * math.cos(ar) / 111320.0
                ln = O[1] + r * math.sin(ar) / bp.M_LNG
                if any(inside_ll(rg, ln, la) for rg in rings[m]):
                    far = r
            la = O[0] + far * math.cos(ar) / 111320.0
            ln = O[1] + far * math.sin(ar) / bp.M_LNG
            pts.append([round(ln, 6), round(la, 6)])
        pts.append(pts[0])
        out.append({"min": m, "ring": pts})
    return out


# ---------------------------------------------------------------- 6. landmarks for the sight lines (P5)
def nominatim_search(q):
    return cached("nomb-%s.json" % hashlib.md5(q.encode("utf-8")).hexdigest()[:12], lambda: http_json(
        "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
            {"q": q, "format": "jsonv2", "limit": 5, "viewbox": "34.74,32.13,34.84,32.04", "bounded": 1}), UA_OSM, pause=1.2))


def compass(br):
    return ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][int(((br + 22.5) % 360) // 45)]


def landmarks(city_blocks):
    items = []

    def add(key, name_he, name_en, lat, lng, kind, src, h=None, h_src=None, note=None, osm=None):
        d, br = bp.dist_bearing(lat, lng)
        items.append({"key": key, "name": name_he, "name_en": name_en, "kind": kind, "lat": round(lat, 6), "lng": round(lng, 6),
                      "dist_m": d, "bearing": br, "dir": compass(br), "h": h, "h_src": h_src, "src": src, "osm": osm, "note": note,
                      "visible": None})

    # the sea: the sea edge of the city's beach polygons (GIS 579), the nearest one and the band of bearings the coast spans
    beaches = gis_all(579, 4500, "beach_name")
    edge = []
    for f in beaches:
        ring = f["geometry"]["rings"][0]
        w = min(ring, key=lambda p: p[0])          # the westmost vertex = the waterline side
        d, br = bp.dist_bearing(w[1], w[0])
        edge.append((d, br, w[1], w[0], clean_name(f["attributes"].get("beach_name"))))
    edge.sort()
    if edge:
        d, br, la, ln, nm = edge[0]
        add("sea", "הים התיכון (%s, קו המים)" % (nm if nm.startswith("חוף") else "חוף " + nm) if nm else "הים התיכון", "Mediterranean Sea (%s beach, waterline)" % nm, la, ln, "sea",
            "עיריית תל אביב-יפו, שכבת החופים 579 (הקודקוד המערבי של פוליגון החוף)",
            note="the nearest beach's sea edge; the coast in the city's layer spans bearings %.0f-%.0f within 4.5 km" % (min(e[1] for e in edge), max(e[1] for e in edge)))
    # Park HaYarkon and its lake
    ypk = cached("nominatim-yarkon.json", lambda: None)
    if ypk:
        c = ypk[0]
        add("yarkon_park", "פארק הירקון (גני יהושע), מרכז", "Park HaYarkon (Ganei Yehoshua), centre", float(c["lat"]), float(c["lon"]), "park",
            "OpenStreetMap relation 16022802 (Nominatim)", osm="relation/16022802",
            note="the park spans from about 1 km north of the plot; its nearest edge points are in places.json (outdoors)")
    # named landmarks from OpenStreetMap (Nominatim), heights from the city's buildings layer when a building of GIS 513 stands there
    # (key, Hebrew, English, bounded Nominatim query, the OSM object expected: type/id)
    Q = [("azrieli_center", "מרכז עזריאלי (שלושת המגדלים)", "Azrieli Center (the three towers)", "מרכז עזריאלי", "way/32635200"),
         ("azrieli_sarona", "מגדל עזריאלי שרונה", "Azrieli Sarona Tower", "עזריאלי שרונה", "way/509799257"),
         ("marganit", "מגדל מרגנית (הקריה)", "Marganit Tower (HaKirya)", "מגדל מרגנית", "way/149520805"),
         ("reading", "תחנת הכוח רידינג", "Reading power station", "רידינג", "way/97714590"),
         ("reading_lighthouse", "מגדלור רידינג", "Reading lighthouse", "רידינג", "way/560065218"),
         ("port", "נמל תל אביב", "Tel Aviv Port", "נמל תל אביב", "way/803404214"),
         ("ramat_aviv", "רמת אביב", "Ramat Aviv", "רמת אביב", None),
         ("tau", "אוניברסיטת תל אביב", "Tel Aviv University", "אוניברסיטת תל אביב", "relation/17483735"),
         ("city_hall", "בניין עיריית תל אביב-יפו (כיכר רבין)", "Tel Aviv-Yafo City Hall (Rabin Square)", "עיריית תל אביב", "way/31786632"),
         ("habima", "תיאטרון הבימה", "Habima Theatre", "הבימה", "way/149522836"),
         ("ichilov", "בית החולים איכילוב (המרכז הרפואי תל אביב)", "Ichilov (Tel Aviv Sourasky Medical Center)", "איכילוב", "way/26599740"),
         ("savidor", "תחנת רכבת תל אביב סבידור מרכז", "Tel Aviv Savidor Center railway station", "Azrieli Center", None),
         ("moshe_aviv", "מגדל משה אביב (רמת גן)", "Moshe Aviv Tower (Ramat Gan)", "מגדל משה אביב", None),
         ("sportek", "ספורטק", "Sportek", "ספורטק", "way/34333834"),
         ]
    fixed = {"savidor": ("תל אביב סבידור מרכז", "node", 2930618402, 32.0842437, 34.7983117, "station"),
             "moshe_aviv": ("מגדל משה אביב", "way", 503512749, 32.0834265, 34.8037412, "building"),
             "ramat_aviv": ("רמת-אביב", "way", 819845420, 32.1088611, 34.7950946, "suburb")}
    blds = city_blocks.get("notable", []) + city_blocks.get("buildings", [])
    for key, he, en, q, want in Q:
        if key in fixed:
            nm, ot, oi, la, ln, typ = fixed[key]
            r = {"name": nm, "osm_type": ot, "osm_id": oi, "lat": la, "lon": ln, "type": typ}
        else:
            rs = nominatim_search(q) or []
            r = next((x for x in rs if want and "%s/%s" % (x["osm_type"], x["osm_id"]) == want), rs[0] if rs and not want else None)
        if not r:
            items.append({"key": key, "name": he, "name_en": en, "note": "not found (Nominatim, bounded to Tel Aviv: %s)" % q})
            continue
        la, ln = float(r["lat"]), float(r["lon"])
        h = hs = None
        near = [b for b in blds if b.get("h") and math.hypot((b["lat"] - la) * 111320, (b["lng"] - ln) * bp.M_LNG) < 45]
        if near and key not in ("ramat_aviv", "tau", "port", "sportek", "reading", "azrieli_center"):
            b = max(near, key=lambda b: b["h"])
            h, hs = b["h"], "עיריית תל אביב-יפו, שכבת המבנים 513, oid %s, %s קומות (%s)" % (b["oid"], b.get("floors"), b["h_src"])
        add(key, he, en, la, ln, r.get("type") or r.get("category"), "OpenStreetMap (Nominatim), %s/%s (%s)" % (r["osm_type"], r["osm_id"], r.get("name")),
            h=h, h_src=hs, osm="%s/%s" % (r["osm_type"], r["osm_id"]),
            note=("outside Tel Aviv-Yafo: no height in the city's layer" if key == "moshe_aviv" else None))
    # the Azrieli towers themselves, as the city's buildings layer names and measures them
    for b in city_blocks.get("notable", []):
        if b.get("name") == "מגדלי עזריאלי":
            add("azrieli_tower_%s" % b["oid"], "מגדלי עזריאלי (%s קומות)" % b.get("floors"), "Azrieli Center tower (%s floors)" % b.get("floors"),
                b["lat"], b["lng"], "tower", "עיריית תל אביב-יפו, שכבת המבנים 513, oid %s" % b["oid"], h=b["h"], h_src=b["h_src"])
    # the Ayalon (Highway 20): the nearest point of its motorway ways (Overpass)
    ay = cached("overpass-ayalon.json", lambda: http_json("https://overpass-api.de/api/interpreter", UA_OSM, data=urllib.parse.urlencode(
        {"data": "[out:json][timeout:60];way(around:3000,%.6f,%.6f)[highway=motorway][ref~\"^20$\"];out geom;" % O}).encode(), timeout=120, pause=1.2))
    if ay and ay.get("elements"):
        best = None
        for e in ay["elements"]:
            for p in e.get("geometry") or []:
                d, _ = bp.dist_bearing(p["lat"], p["lon"])
                if best is None or d < best[0]:
                    best = (d, p["lat"], p["lon"], e["id"])
        add("ayalon", "נתיבי איילון (כביש 20), הנקודה הקרובה", "Ayalon Highway (Route 20), nearest point", best[1], best[2], "motorway",
            "OpenStreetMap way %s (Overpass)" % best[3], osm="way/%s" % best[3])
    else:
        items.append({"key": "ayalon", "name": "נתיבי איילון", "name_en": "Ayalon Highway", "note": "not found (Overpass)"})
    # the notable towers of the city's layer within 2 km (heights sourced), for the skyline
    tall = [{"name": b.get("name"), "h": b["h"], "h_src": b["h_src"], "floors": b.get("floors"), "lat": b["lat"], "lng": b["lng"],
             "dist_m": b["dist"], "bearing": b["bearing"], "dir": compass(b["bearing"]), "oid": b["oid"]}
            for b in city_blocks.get("notable", []) if b["h"] >= 100]
    # the city's layer seldom names a tower: OpenStreetMap's name of the building there (reverse geocoding, building level)
    for t in tall:
        if t["h"] < 120:
            continue
        rv = cached("revb-%.6f-%.6f.json" % (t["lat"], t["lng"]), lambda t=t: http_json("https://nominatim.openstreetmap.org/reverse?" + urllib.parse.urlencode(
            {"lat": t["lat"], "lon": t["lng"], "format": "jsonv2", "zoom": 18, "accept-language": "he"}), UA_OSM, pause=1.2)) or {}
        if rv.get("name") and rv.get("category") == "building":            # a shop or office inside the tower is not its name
            t["osm_name"] = rv["name"]
            t["osm"] = "%s/%s" % (rv.get("osm_type"), rv.get("osm_id"))
        rd = (rv.get("address") or {})
        t["osm_address"] = " ".join(x for x in (rd.get("road"), rd.get("house_number")) if x) or None
    out = {"v": 1, "generated_at": TODAY, "status": "PREPARATION ONLY: visibility is not computed; the towers' model and eye heights come in P5",
           "origin": {"lat": O[0], "lng": O[1], "what": "the plot centre (plan 2500ב lots); the three towers stand 75-78 m from it"},
           "towers": json.load(io.open(os.path.join(HERE, "kikar-stage", "quarter.json"), encoding="utf-8")).get("towers"),
           "bearing_rule": "true bearing from the plot centre, degrees clockwise from north; dir = 8-point compass",
           "landmarks": sorted(items, key=lambda i: i.get("bearing", 999)),
           "by_direction": {}, "skyline_100m_within_2km": sorted(tall, key=lambda t: t["bearing"])}
    for i in items:
        if i.get("dir"):
            out["by_direction"].setdefault(i["dir"], []).append(i["key"])
    io.open(LM_OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, indent=1))
    print("landmarks", len(items), {k: v for k, v in out["by_direction"].items()}, "| skyline >=100 m:", len(tall))


def main():
    reg = json.load(io.open(OUT, encoding="utf-8"))
    if reg.get("provisional"):
        sys.exit("places.json is already enriched: run  python scripts/project-stage/build_places.py kikar  first (it rebuilds from cache)")
    places = reg["places"]
    n0 = len(places)
    city_layers(places)
    bus_lines(places)
    rail(places)
    yarkon(places)
    tok = None if "--no-walk" in sys.argv else bp.token()
    for p in places:
        if "sight" not in p:
            p["sight"] = bp.sight(p["x"], p["z"])
        if tok:
            p["walk"], p["route_m"] = walk_from_ring(tok, p["lat"], p["lng"])
    for lm in reg.get("landmarks", []):
        if tok:
            la = O[0] - lm["z"] / 111320.0
            ln = O[1] + lm["x"] / bp.M_LNG
            lm["walk"] = walk_from_ring(tok, la, ln)[0]
    if tok:
        reg["iso"] = iso_union(tok)
    places.sort(key=lambda p: p["dist"])
    reg["places"] = places
    reg["generated_at"] = TODAY
    reg["note"] += (" Kikar Hamedina additions (enrich_places_kikar.py, %s): the Tel Aviv-Yafo municipality's GIS layers for daily life "
                    "(schools and kindergartens 2026-27, daycares, clinics, pharmacies, community, culture, sport, playgrounds, gardens, "
                    "synagogues); bus lines per stop from Open Bus Stride (GTFS of the Ministry of Transport, %s); the light-rail stations of "
                    "the city's layers (red running; purple and green planned); Park HaYarkon's nearest edges (OpenStreetMap). The view point "
                    "and the sight lines are PROVISIONAL: from the plot centre, eye heights by formula (eye-kikar-provisional.json), the "
                    "three towers left out of the obstacles; per-tower sight lines are P5. Walking minutes start on the ring road ה' באייר "
                    "on the side facing each place (the plot is a closed building site; Mapbox would snap its centre 122 m south); the "
                    "5/10/15-minute areas are the union of four Mapbox walking areas from the ring's N/E/S/W points, outlined every 3 degrees."
                    % (TODAY, BUS_DAY))
    reg["src"].update({"gis": "עיריית תל אביב-יפו, GIS פתוח (IView2), %s" % time.strftime("%#m.%Y" if os.name == "nt" else "%-m.%Y"),
                       "lines": "Open Bus Stride (הסדנא לידע ציבורי), GTFS משרד התחבורה, %s" % BUS_DAY,
                       "rail": "עיריית תל אביב-יפו, שכבות הרכבת הקלה (423, 764, 766)"})
    reg["provisional"] = {"view_point": "the plot centre", "eye_src": "eye-kikar-provisional.json (CALC: (floor - 1) x 4.0 m + 1.6 m)",
                          "towers_left_out_of_obstacles": True,
                          "walk_start": "the ring road ה' באייר, 138 m from the centre on the place's bearing (Mapbox snaps it to the road)",
                          "iso": "union of four Mapbox walking isochrones (ring N/E/S/W), radial outline every 3 degrees"}
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(reg, ensure_ascii=False, separators=(",", ":")) + "\n")
    from collections import Counter
    print("places %d -> %d" % (n0, len(places)), dict(Counter(p["g"] for p in places)), dict(Counter(p["src"] for p in places)))
    print("walk known", sum(1 for p in places if p.get("walk")), "bytes", os.path.getsize(OUT))
    landmarks(json.load(io.open(os.path.join(HERE, "city-blocks.json"), encoding="utf-8")))


if __name__ == "__main__":
    main()
