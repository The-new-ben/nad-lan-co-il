# -*- coding: utf-8 -*-
"""Rainbow's quarter for the stage (the site loop, R4): our projects around it and the main places, at their true
positions, for pins and cards in the scene. Run offline; the page reads the file, nothing is fetched at page time.

Output: plugins/nadlan-config/assets/project-stage/rainbow/quarter.json
  projects: our project pages near Rainbow (public REST: developer, status, floors, units, the parcel point)
  places:   the places a buyer asks about, from the find-place data (TLV OpenData + OSM, 27.8.2026)
Every item carries x (metres east) and z (metres south, the scene's -north) from the lot's centre (the scene's origin),
the distance and the bearing from Rainbow's tower, and its source. Nothing is estimated: a project's height is its floors
from its own page (the scene draws a schematic mass and says so), and an item without a position is left out.
  python scripts/project-stage/build_quarter_rainbow.py"""
import io, json, math, os, re, sys, time, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "rainbow", "quarter.json")
LOT = (32.103168, 34.784441)     # the scene's origin: lot 111's centre
TOWER = (32.10354, 34.78466)     # Rainbow's tower (the view and the beam start here)

# our project pages near Rainbow (the Sde Dov quarter and the Einstein axis within about 1.3 km), with the short Hebrew
# name a buyer says; everything else comes from the page itself
PROJECTS = [
    (4745, "דמרי ימה", "DIMRI YAMA"),
    (4747, "זוהי", "ZOHI"),
    (4750, "שיכון ובינוי, מגרש 109", ""),
    (4749, "אוטופיה", "UTOPIA"),
    (4744, "אשירה", "ASHIRA"),
    (4748, "גינדי ווג", "GINDI VOGUE"),
    (4867, "מגדל איינשטיין", "EINSTEIN TOWER"),
    (4743, "פירסט", "FIRST"),
]
# a page's status as a buyer reads it (a few pages still hold a machine word)
STATUS = {"permits": "בהליכי היתר", "construction": "בבנייה", "marketing": "בשיווק", "planning": "בתכנון", "presale": "בשיווק מוקדם"}
# the legend's groups (design system QuarterPins): being built, selling, at the permit stage
PHASE = {"בבנייה": "building", "בשיווק": "selling", "בשיווק מוקדם": "selling", "בהיתר בנייה": "permit", "בהליכי היתר": "permit",
         "בתכנון": "permit"}
SRC_ATLAS = "find-place, נתוני עיריית תל אביב-יפו ו-OpenStreetMap, 8.2026"
PLACES = [
    # kind, name, lat, lng, status words, source
    ("rail", "תחנת רידינג, הרכבת הקלה", 32.0994035, 34.7822364, "מאושרת, עוד לא פועלת", SRC_ATLAS),
    ("school", "בית הספר כוכב הצפון", 32.101408, 34.786443, "קיים", SRC_ATLAS),
    ("park", "גן כוכב הצפון", 32.102028, 34.785529, "קיים", SRC_ATLAS),
    ("beach", "חוף רידינג", 32.10711, 34.77681, "קיים", SRC_ATLAS),
    ("nature", "שפך נחל הירקון", 32.098806, 34.778214, "קיים", SRC_ATLAS),
]


def enu(lat, lng, origin):
    e = (lng - origin[1]) * math.cos(math.radians(origin[0])) * 111320.0
    n = (lat - origin[0]) * 110574.0
    return e, n


def from_tower(lat, lng):
    e, n = enu(lat, lng, TOWER)
    return round(math.hypot(e, n)), round((math.degrees(math.atan2(e, n)) + 360) % 360, 1)


def rest(pid):
    url = "https://nad-lan.co.il/wp-json/wp/v2/nadlan_project/%d?_fields=id,slug,link,title,meta&nlq=%d" % (pid, int(time.time()))
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 NadLan-QUARTER/1.0"})
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


out = {"generated_at": time.strftime("%Y-%m-%d"), "origin": {"lat": LOT[0], "lng": LOT[1]}, "tower": {"lat": TOWER[0], "lng": TOWER[1]},
       "note": "מסה סכמטית לפי מספר הקומות בעמוד הפרויקט; המיקום לפי המגרש. הדמיה להמחשה בלבד.", "projects": [], "places": []}
for pid, short, brand in PROJECTS:
    d = rest(pid)
    m = d.get("meta") or {}
    lat, lng = float(m.get("lat") or 0), float(m.get("lng") or 0)
    if not (lat and lng):
        print("skip (no position):", pid, short)
        continue
    e, n = enu(lat, lng, LOT)
    dist, brg = from_tower(lat, lng)
    floors = int(m.get("num_floors") or 0)
    st = (m.get("project_status") or "").strip()
    item = {"id": pid, "kind": "project", "name": short, "pin": short.split(",")[0].strip(), "brand": brand,
            # the word is spelled with its gershayim on a sales surface, whatever the page's meta field holds
            "developer": re.sub(r"\bנדלן\b", "נדל״ן", (m.get("developer_name") or "").strip().replace("׳", "'")), "status": STATUS.get(st.lower(), st),
            "floors": floors or None, "units": int(m.get("num_units") or 0) or None, "url": d.get("link"),
            "x": round(e, 1), "z": round(-n, 1), "dist": dist, "bearing": brg,
            "source": "עמוד הפרויקט באתר"}
    item["phase"] = PHASE.get(item["status"], "permit")
    if int(m.get("completion_year") or 0) > 2000:   # a year only where the page gives one
        item["occupancy"] = int(m["completion_year"])
    out["projects"].append(item)
    print("project", pid, short, "| floors", floors, "| %d m at %.0f°" % (dist, brg))
for kind, name, lat, lng, status, src in PLACES:
    e, n = enu(lat, lng, LOT)
    dist, brg = from_tower(lat, lng)
    out["places"].append({"kind": kind, "name": name, "pin": name.split(",")[0].strip(), "status": status, "x": round(e, 1), "z": round(-n, 1), "dist": dist, "bearing": brg,
                          "walk": max(1, round(dist * 1.25 / 80)), "source": src})
    print("place", kind, name, "| %d m at %.0f°" % (dist, brg))
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, indent=1))
print("wrote", OUT, os.path.getsize(OUT), "bytes")
