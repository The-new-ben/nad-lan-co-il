# -*- coding: utf-8 -*-
"""Builds plugins/nadlan-config/assets/instruments/data/asbestos.json for the asbestos page tools (HAD-668, R11e).

Sites: the 348 points of the Western Galilee friable-asbestos soil project (MoEP ArcGIS layer, saved in
docs/research/2026-11-03-asbestos/wg-sites.geojson), with the three official statuses as MoEP words them.
Registry: the MoEP registry of asbestos licence holders, live from the data.gov.il datastore, COUNTED by licence type,
district and locality only (no names, no phones: the page links out to the gov.il search).
Landfills and labs: data.gov.il datastore, site name, type and area only.
Units: the MoEP spreadsheet of local authorities and their environmental unit (gov.il, the hotline page), the unit's
name, district, office phone, website and address; never the managers' names or mobile numbers.
  python -I build_asbestos_data.py <units.xlsx> [--out <path>]"""
import json
import os
import re
import sys
import time
import urllib.request
from collections import Counter

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RES = os.path.join(REPO, "docs", "research", "2026-11-03-asbestos")
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "asbestos.json")
if "--out" in sys.argv:
    OUT = sys.argv[sys.argv.index("--out") + 1]
CKAN = "https://data.gov.il/api/3/action/"
REGISTRY = "512d916e-07f0-4774-b84a-3a989e45e7eb"
STATUS = ["אתר שנוקה ולא ידוע על אסבסט שנותר בקרקע", "אתר שנוקה אך ידוע שנותר אסבסט תחת התשתיות", "אתר שידוע שיש בו אסבסט, טרם בוצע ניקוי"]
FIX_PLACE = {"נהריה": "נהרייה"}


def get(url):
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (nad-lan.co.il data build)"})
    return json.load(urllib.request.urlopen(r, timeout=90))


def rows(resource):
    out, off = [], 0
    while True:
        d = get(CKAN + "datastore_search?resource_id=%s&limit=500&offset=%d" % (resource, off))["result"]
        out += d["records"]; off += 500
        if off >= d["total"]:
            return out


def resource_of(dataset):
    for r in get(CKAN + "package_show?id=" + dataset)["result"]["resources"]:
        if r.get("datastore_active"):
            return r["id"]
    raise SystemExit("no datastore resource in " + dataset)


def clean(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()


# 1. The Western Galilee sites
g = json.load(open(os.path.join(RES, "wg-sites.geojson"), encoding="utf-8"))
sites, by_place = [], Counter()
for f in g["features"]:
    p = f["properties"]; lon, lat = f["geometry"]["coordinates"]
    place = FIX_PLACE.get(clean(p.get("yishuv")), clean(p.get("yishuv")))
    st = STATUS.index(clean(p.get("legend")))
    sites.append([round(lon, 5), round(lat, 5), st, place])
    by_place[(place, st)] += 1
assert len(sites) == 348, len(sites)
places = {}
for (pl, st), n in by_place.items():
    places.setdefault(pl, [0, 0, 0])[st] += n

# 2. The registry, counted
reg = rows(REGISTRY)
by_type = Counter(clean(r.get("LicenseType")) for r in reg)
by_dist = Counter(clean(r.get("District")) or "לא צוין" for r in reg)
by_td = Counter((clean(r.get("LicenseType")), clean(r.get("District")) or "לא צוין") for r in reg)
by_loc = Counter(clean(r.get("Settlement")) for r in reg if clean(r.get("Settlement")))
disc = sum(1 for r in reg if clean(r.get("DisciplinaryAspects")))

# 3. Landfills and labs (site, type, area; no person names)
# the operators are companies: the page names the place only (the no-names rule), matched from the address or the site name
PLACE = [("מילואות", "מילואות דרום, הגליל המערבי"), ("תמר", "אפעה, אזור תמר"), ("אילות", "נימרה, אזור אילות"),
         ("תות", "מחצבות תות, ליד זכרון יעקב"), ("383", "חרובית, ליד שדות מיכה"), ("נאות חובב", "נאות חובב")]
lf = []
for r in rows(resource_of("asbestoslandfills")):
    txt = clean(r.get("Address")) + " " + clean(r.get("EnvironmentalSite"))
    place = next((v for k, v in PLACE if k in txt), None)
    if not place:
        raise SystemExit("FATAL: a landfill site with no place label: " + txt)
    lf.append({"place": place, "type": clean(r.get("SiteType")).replace("+", ", ")})
labs = Counter(clean(r.get("LabType")) for r in rows(resource_of("asbestos-lab")))

# 4. Local authorities and their environmental unit
wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
ws = wb.worksheets[0]; hdr = None; units = []
for r in ws.iter_rows(values_only=True):
    r = [clean(c) for c in r]
    if hdr is None:
        hdr = r; continue
    row = dict(zip(hdr, r))
    if not row.get("רשות") or not row.get("שם יחידה"):
        continue
    site = row.get("אתר היחידה", "")
    if site and not site.startswith("http"):
        site = "https://" + site
    units.append([row["רשות"], row.get("מחוז", ""), row["שם יחידה"], row.get("טלפון יחידה", ""), site, row.get("כתובת היחידה", "")])
units.sort(key=lambda u: u[0])

data = {
    "key": "asb", "built": time.strftime("%Y-%m-%d"),
    "sources": {
        "sites": "המשרד להגנת הסביבה, שכבת פרויקט ניקוי הקרקעות מאסבסט פריך בגליל המערבי (data.gov.il)",
        "registry": "המשרד להגנת הסביבה, מרשם העוסקים באסבסט (data.gov.il)",
        "units": "המשרד להגנת הסביבה, רשימת היחידות הסביבתיות ואיגודי הערים לאיכות הסביבה",
        "prices": "מרכז המחקר והמידע של הכנסת, 17.7.2023, לפי מכרז קבלן הבית של המשרד להגנת הסביבה",
    },
    "status": STATUS, "sites": sites,
    "places": dict(sorted(places.items(), key=lambda kv: -sum(kv[1]))),
    "registry": {"total": len(reg), "byType": dict(by_type.most_common()), "byDistrict": dict(by_dist.most_common()),
                 "byTypeDistrict": {"%s|%s" % k: v for k, v in sorted(by_td.items())}, "localities": len(by_loc),
                 "disciplinary": disc, "search": "https://www.gov.il/he/Departments/DynamicCollectors/asbest_list"},
    "landfills": lf, "labs": dict(labs.most_common()),
    "units": units,
    "prices": {"brokenM2": 50, "friableM3": 1600, "date": "2023-07-17"},
    "hotline": {"moep": "*6911", "moepLine": "073-2733200", "city": "106"},
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("sites", len(sites), "| places", len(places), "| registry", len(reg), dict(by_type), "| landfills", len(lf), "| labs", dict(labs),
      "| units", len(units), "| disciplinary", disc, "|", os.path.getsize(OUT), "bytes ->", OUT)
