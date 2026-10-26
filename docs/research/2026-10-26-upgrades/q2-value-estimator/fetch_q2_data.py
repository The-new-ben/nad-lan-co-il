# -*- coding: utf-8 -*-
"""Q2 stage 2 data pull (GET only, public official sources, no keys):
1. data.nadlan.gov.il settlement buy files for the tool's 23 cities (codes from plugins/nadlan-config/assets/instruments/data/value.json)
   plus Yavne (2660): the median closed-deal price for 3, 4, 5 rooms and all apartments, 22 quarters, the city line and the Israel line
   (dna.md V1, V2). Polite: one request a second.
2. CBS dwelling price index, monthly, series 40010 (national, base 1993 average) and 60000 to 60500 (the six districts) from 01-2018
   (V7, V8, V9).
3. The Ministry of Justice register of real estate appraisers on data.gov.il (dataset shamaim, resource 8540534a-...): the row count
   and the resource's last-modified date only (no names are saved) (V11).
Writes data/q2-official.json (compact, what write_q2_stage2.py needs) and data/q2-fetch-log.json (URL, status, Last-Modified, UTC).
  python docs/research/2026-10-26-upgrades/q2-value-estimator/fetch_q2_data.py"""
import datetime, io, json, os, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
OUT = os.path.join(H, "data"); os.makedirs(OUT, exist_ok=True)
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
UA = {"User-Agent": "Mozilla/5.0 (nad-lan.co.il research; official public files; 1 req/s)"}
LOG = []


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def get(url, tries=3):
    for i in range(tries):
        t = now()
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60); b = r.read()
            LOG.append({"url": url, "status": r.status, "last_modified": r.headers.get("Last-Modified"), "utc": t, "bytes": len(b)})
            return json.loads(b.decode("utf-8-sig"))
        except Exception as e:
            LOG.append({"url": url, "status": getattr(e, "code", None), "error": str(e)[:160], "utc": t})
            time.sleep(2 + 2 * i)
    raise SystemExit("FAILED " + url)


VALUE = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "value.json"), encoding="utf-8"))
CITIES = [(n, c["code"], c.get("page")) for n, c in VALUE["cities"].items()] + [("יבנה", 2660, None)]
data = {"read_utc": now(), "settlements": [], "cbs": {}, "register": {}}

# 1. settlement files
for name, code, page in CITIES:
    d = get("https://data.nadlan.gov.il/api/pages/settlement/buy/%d.json" % code)
    rooms = {}
    for r in d["trends"]["rooms"]:
        pts = sorted(r["graphData"], key=lambda g: (g["year"], g["month"]))
        rooms[str(r["numRooms"])] = [[g["year"], g["month"], g["settlementPrice"], g["countryPrice"]] for g in pts]
    data["settlements"].append({"name": name, "official_name": d.get("settlementName"), "code": code, "page": page,
                                "version": d.get("version"), "last_modified": LOG[-1].get("last_modified"),
                                "neighbourhoods": len(d.get("otherNeighborhoods") or []), "rooms": rooms})
    print("settlement", code, name, d.get("version"), LOG[-1].get("last_modified"))
    time.sleep(1)

# 2. CBS series, monthly from 01-2018
for sid in (40010, 60000, 60100, 60200, 60300, 60400, 60500):
    rows, page = [], 1
    while True:
        d = get("https://api.cbs.gov.il/index/data/price?id=%d&format=json&download=false&lang=he&startPeriod=01-2018&PageSize=500&Page=%d" % (sid, page))
        m = d["month"][0]
        for x in m["date"]:
            rows.append([x["year"], x["month"], x["currBase"]["value"], x["currBase"]["baseDesc"], x.get("percent"), x.get("percentYear")])
        if d["paging"]["current_page"] >= d["paging"]["last_page"]:
            break
        page += 1
    rows.sort(key=lambda r: (r[0], r[1]))
    data["cbs"][str(sid)] = {"name": m["name"], "rows": rows}
    print("cbs", sid, m["name"], len(rows), "months, last", rows[-1][:3], "bases", sorted(set(r[3] for r in rows)))
    time.sleep(1)

# 3. the appraisers register: count + dates (no records kept)
RID = "8540534a-eccd-4568-a677-652d589ed172"
cnt = get("https://data.gov.il/api/3/action/datastore_search?resource_id=%s&limit=0" % RID)
res = get("https://data.gov.il/api/3/action/resource_show?id=%s" % RID)
data["register"] = {"resource_id": RID, "dataset": "shamaim", "total": cnt["result"]["total"],
                    "last_modified": res["result"].get("last_modified"), "metadata_modified": res["result"].get("metadata_modified"),
                    "name": res["result"].get("name"), "read_utc": now()}
print("register", data["register"]["total"], data["register"]["last_modified"])

json.dump(data, io.open(os.path.join(OUT, "q2-official.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
json.dump(LOG, io.open(os.path.join(OUT, "q2-fetch-log.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", sum(1 for l in LOG if l.get("status") == 200), "of", len(LOG), "requests")
