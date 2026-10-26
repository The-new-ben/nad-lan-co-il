# -*- coding: utf-8 -*-
"""Renewal map data (Q1 of docs/loop/UPGRADE-LOOP.md, Ben 25.10.2026): one dated JSON for /urban-renewal/map/ built only from
official public sources, so every number on the page carries its source and date.
  1. The Ministry of Construction and Housing open file "מתחמי התחדשות עירונית" (data.gov.il, resource f65a0daf-...): every complex,
     stage, track, units today and after building, permits, declaration date. Licence: data.gov.il terms (commercial use with credit).
  2. The localities list (data.gov.il resource 5c78e9fa-...) for the sub-district of each city; CBS sub-district -> district map below.
  3. The authority's live map layer (ArcGIS GIS_UrbanRenewal layer 1, which feeds the gov.il map): COUNTS ONLY (total, localities,
     units, stage and track counts, last edit date). Its geometry is not republished (licence field empty, research F9).
Writes plugins/nadlan-config/data/renewal-stats.json.   python tools/urban/build_renewal_stats.py"""
import collections, datetime, io, json, os, re, sys, urllib.parse, urllib.request
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
OUT = os.path.join(REPO, "plugins", "nadlan-config", "data", "renewal-stats.json")
UA = {"User-Agent": "Mozilla/5.0 NadLan-RenewalStats/1.0"}
FILE_RES = "f65a0daf-f737-49c5-9424-d378d52104f5"
LOC_RES = "5c78e9fa-c2e2-4771-93ff-7f400a12f7ba"
LAYER = "https://services6.arcgis.com/I08Ekaykft5ELucH/arcgis/rest/services/GIS_UrbanRenewal/FeatureServer/1"
# CBS: sub-district (נפה) -> district (מחוז)
NAFA = {"ירושלים": "ירושלים", "צפת": "הצפון", "כנרת": "הצפון", "יזרעאל": "הצפון", "עכו": "הצפון", "גולן": "הצפון",
        "חיפה": "חיפה", "חדרה": "חיפה", "השרון": "המרכז", "פתח תקווה": "המרכז", "פתח תקוה": "המרכז", "רמלה": "המרכז", "רחובות": "המרכז",
        "תל אביב": "תל אביב", "רמת גן": "תל אביב", "חולון": "תל אביב", "עפולה": "הצפון", "נצרת": "הצפון", "אשקלון": "הדרום", "באר שבע": "הדרום",
        "ג'נין": "יהודה ושומרון", "שכם": "יהודה ושומרון", "טול כרם": "יהודה ושומרון", "ראמאללה": "יהודה ושומרון",
        "ירדן (יריחו)": "יהודה ושומרון", "בית לחם": "יהודה ושומרון", "חברון": "יהודה ושומרון"}
CITY_DISTRICT = {"טירה": "המרכז", "סחנין": "הצפון"}  # their codes are missing from the localities list (CBS districts)
STAGE = {1: "תכנון ראשוני", 2: "תכנון סטטוטורי", 3: "תכנית מאושרת לפני מימוש", 4: "תכנית מאושרת במימוש"}  # codeStatusHarashut domain


def get(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read().decode("utf-8"))


def num(x):
    try:
        return int(float(str(x).strip().replace(",", "")))
    except Exception:
        return 0


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"\s*[–—]\s*", " - ", str(s or ""))).strip()  # names in the file use long dashes; the site prints none


def ckan_all(res):
    out, off = [], 0
    while True:
        d = get("https://data.gov.il/api/3/action/datastore_search?resource_id=%s&limit=1000&offset=%d" % (res, off))
        rows = d["result"]["records"]; out += rows; off += len(rows)
        if not rows or off >= d["result"]["total"]:
            return out


meta = get("https://data.gov.il/api/3/action/resource_show?id=" + FILE_RES)["result"]
rows = ckan_all(FILE_RES)
locs = {num(r["סמל_ישוב"]): clean(r["שם_נפה"]) for r in ckan_all(LOC_RES)}
recs = []
for r in rows:
    st = clean(r["Status"]).replace(" - ", " ")  # "תכנית מאושרת - אחרי רישוי" as written in the file
    if not st or re.fullmatch(r"\d{4}", st):
        st = "סטטוס לא תקין בקובץ"  # one row in the 15.8.2026 file carries "2025" as its status; counted, labelled
    recs.append({"n": num(r["MisparMitham"]), "city": clean(r["Yeshuv"]), "code": num(r["SemelYeshuv"]), "name": clean(r["ShemMitcham"]),
                 "ex": num(r["YachadKayam"]), "add": num(r["YachadTosafti"]), "prop": num(r["YachadMutza"]), "decl": clean(r["TaarichHachraza"]),
                 "plan": clean(r["MisparTochnit"]), "link": clean(r["KishurLatar"]), "permits": num(r["SachHeterim"]),
                 "track": clean(r["Maslul"]), "exec": clean(r["Bebitzua"]) == "כן", "status": st})
by_status = collections.OrderedDict()
for s in ("תכנון ראשוני", "תכנון סטטוטורי", "תכנית מאושרת לפני מימוש", "תכנית מאושרת במימוש", "תכנית מאושרת אחרי רישוי", "סטטוס לא תקין בקובץ"):
    rs = [x for x in recs if x["status"] == s]
    by_status[s] = {"n": len(rs), "existing": sum(x["ex"] for x in rs), "proposed": sum(x["prop"] for x in rs)}
others = [x for x in recs if x["status"] not in by_status]
tracks = collections.Counter(x["track"] or "ללא מסלול בקובץ" for x in recs)
years = collections.Counter()
for x in recs:
    m = re.search(r"(\d{4})$", x["decl"])
    if m:
        years[m.group(1)] += 1
last_decl = max((datetime.datetime.strptime(x["decl"], "%d/%m/%Y") for x in recs if re.fullmatch(r"\d{2}/\d{2}/\d{4}", x["decl"])), default=None)
cities = collections.OrderedDict()
for x in sorted(recs, key=lambda x: x["city"]):
    c = cities.setdefault(x["city"], {"city": x["city"], "district": NAFA.get(locs.get(x["code"], ""), CITY_DISTRICT.get(x["city"], "אחר")), "n": 0, "approved": 0, "exec": 0,
                                       "tax": 0, "auth": 0, "undeclared": 0, "existing": 0, "proposed": 0, "permits": 0, "last_decl": ""})
    c["n"] += 1; c["existing"] += x["ex"]; c["proposed"] += x["prop"]; c["permits"] += x["permits"]
    c["approved"] += x["status"].startswith("תכנית מאושרת")
    c["exec"] += x["exec"] or x["status"] == "תכנית מאושרת במימוש"
    c["tax"] += x["track"] == "מיסוי"; c["auth"] += x["track"] == "רשויות"; c["undeclared"] += x["track"] in ("טרם הוכרז", "")
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", x["decl"]):
        d = datetime.datetime.strptime(x["decl"], "%d/%m/%Y")
        if not c["last_decl"] or d > datetime.datetime.strptime(c["last_decl"], "%d/%m/%Y"):
            c["last_decl"] = x["decl"]
for c in cities.values():
    c["mult"] = round(c["proposed"] / c["existing"], 2) if c["existing"] else None
approved = sorted([x for x in recs if x["status"].startswith("תכנית מאושרת")], key=lambda x: (x["city"], -x["prop"]))
execution = sorted([x for x in recs if x["exec"] or x["permits"] > 0], key=lambda x: -x["permits"])
# the authority's live map: counts only
lay = get(LAYER + "?f=json")
feats = []
off = 0
while True:
    q = get(LAYER + "/query?" + urllib.parse.urlencode({"where": "1=1", "outFields": "MisparProject,Yeshuv,codeStatusHarashut,TeurSugMaslul,yachadKayamRashut,yachadMutzaRashut",
                                                         "returnGeometry": "false", "f": "json", "resultOffset": off, "resultRecordCount": 1000}))
    fs = q.get("features", []); feats += fs; off += len(fs)
    if not fs or not q.get("exceededTransferLimit"):
        break
# 26.10.2026: a complex drawn as several polygons is several identical rows on the layer (999 rows, 992 complexes on 20.10.2026);
# count each complex number once, so the tiles, the stage counts and the units are per complex (rows kept for reference)
rows_n = len(feats)
_seen = {}
for f in feats:
    _k = f["attributes"].get("MisparProject") or ("row", f["attributes"].get("OBJECTID"), len(_seen))
    _seen.setdefault(_k, f)
feats = list(_seen.values())
mstage = collections.Counter(STAGE.get(f["attributes"].get("codeStatusHarashut"), "ללא שלב במפה") for f in feats)
mtrack = collections.Counter(clean(f["attributes"].get("TeurSugMaslul")) or "ללא מסלול" for f in feats)
edit = (lay.get("editingInfo") or {}).get("dataLastEditDate")
out = {
    "built": datetime.date.today().isoformat(),
    "file": {"source": "משרד הבינוי והשיכון, הרשות הממשלתית להתחדשות עירונית: מתחמי התחדשות עירונית (data.gov.il)",
             "url": "https://data.gov.il/dataset/urban_renewal", "resource": FILE_RES,
             "last_modified": (meta.get("last_modified") or meta.get("metadata_modified") or "")[:10],
             "total": len(recs), "localities": len(cities), "existing": sum(x["ex"] for x in recs), "proposed": sum(x["prop"] for x in recs),
             "additional": sum(x["add"] for x in recs), "by_status": by_status, "other_status": len(others), "tracks": dict(tracks),
             "in_execution": sum(1 for x in recs if x["exec"]), "permits_units": sum(x["permits"] for x in recs),
             "permits_complexes": sum(1 for x in recs if x["permits"] > 0), "by_year": dict(sorted(years.items())),
             "last_declaration": last_decl.strftime("%d/%m/%Y") if last_decl else "", "cities": list(cities.values()),
             "approved": [{k: x[k] for k in ("name", "city", "status", "plan", "link", "ex", "prop")} for x in approved],
             "execution": [{k: x[k] for k in ("name", "city", "status", "permits", "prop")} for x in execution]},
    "map": {"source": "הרשות הממשלתית להתחדשות עירונית: מפת מתחמי פינוי בינוי מוכרזים (gov.il)", "url": "https://www.gov.il/he/departments/topics/mapa-renewal",
            "last_edit": datetime.datetime.utcfromtimestamp(edit / 1000).date().isoformat() if edit else "", "total": len(feats), "rows": rows_n,
            "localities": len({clean(f["attributes"].get("Yeshuv")) for f in feats}),
            "existing": sum(num(f["attributes"].get("yachadKayamRashut")) for f in feats),
            "proposed": sum(num(f["attributes"].get("yachadMutzaRashut")) for f in feats),
            "by_stage": dict(mstage), "tracks": dict(mtrack)},
}
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
f, m = out["file"], out["map"]
print("file: %d complexes, %d localities, %d -> %d units, modified %s, last declaration %s" % (f["total"], f["localities"], f["existing"], f["proposed"], f["last_modified"], f["last_declaration"]))
print("  by status:", {k: v["n"] for k, v in f["by_status"].items()}, "other", f["other_status"], "| tracks", f["tracks"])
print("  execution", f["in_execution"], "| permits", f["permits_units"], "in", f["permits_complexes"], "| years", f["by_year"])
print("  districts:", collections.Counter(c["district"] for c in f["cities"]), "| unmapped:", [c["city"] for c in f["cities"] if c["district"] == "אחר"])
print("map: %d complexes, %d localities, %d -> %d units, last edit %s | stages %s | tracks %s" % (m["total"], m["localities"], m["existing"], m["proposed"], m["last_edit"], m["by_stage"], m["tracks"]))
print("wrote", OUT)
