# -*- coding: utf-8 -*-
"""HAD-681 (Ben 7.11.2026): the data of the three /apartment-prices/ tools (pmarket, pcity, panatomy) in one small file.

    python tools/instruments/build_prices_hub.py      -> plugins/nadlan-config/assets/instruments/data/prices-hub.json

Everything comes from files the site already ships, plus one public call:
  - value-series.json: the CBS dwelling price index 40010 (1993 = 100, from 1994-01) and the district series 60000-60500
    (from 2017-10); the 24 cities and the national medians of closed deals by rooms, 22 quarters (nadlan.gov.il / Tax Authority).
  - cbs-120010.json: the CPI from 2010-01 (chained to the latest base, checked against the CBS calculator).
  - the CBS public API (no key): the CPI 1994-01..2011-12, chained by the "<year> average = 100" rule and scaled onto
    cbs-120010.json over the 2010-2011 overlap (the overlap ratio is printed; it must be flat). Needed for the real
    (CPI-adjusted) change since 1994. The other tools' cbs-120010.json is NOT touched.
  - rent.json: the government median rent by city and rooms, per quarter (same quarter as the price, never mixed).
  - boi-mortgage.json: the Bank of Israel average fixed not-linked rate of the latest month and the 75% cap of directive 329.
Label of the dwelling index: CBS publishes it for two-month periods; the API month M is the deals of M and M+1, published about
the 15th of M+3 (checked: 2026-07 = -0.6% = "July and August 2026", published 15.10.2026; our post /cbs-dwelling-july-august-2026/).
"""
import io
import json
import os
import sys
import time
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")
UA = {"User-Agent": "Mozilla/5.0 NadLan-instruments"}

# city (as in value-series.json) -> its owner price page slug on nad-lan.co.il (live sitemap, 7.11.2026); None = no page
SLUG = {
    "תל אביב יפו": "tel-aviv", "רמת גן": "ramat-gan", "גבעתיים": "givatayim", "בני ברק": "bnei-brak", "פתח תקווה": "petah-tikva",
    "חולון": "holon", "בת ים": "bat-yam", "ראשון לציון": "rishon-lezion", "קריית אונו": "kiryat-ono", "הרצליה": "herzliya",
    "רעננה": "raanana", "כפר סבא": "kfar-saba", "הוד השרון": "hod-hasharon", "רמת השרון": "ramat-hasharon", "נתניה": "netanya",
    "ירושלים": "jerusalem", "מודיעין מכבים רעות": "modiin", "חיפה": "haifa", "רחובות": "rehovot", "אשדוד": "ashdod",
    "אשקלון": "ashkelon", "באר שבע": "beer-sheva", "אילת": "eilat", "יבנה": None,
}
DIST = {"60000": "ירושלים", "60100": "הצפון", "60200": "חיפה", "60300": "המרכז", "60400": "תל אביב", "60500": "הדרום"}


def load(name):
    return json.load(io.open(os.path.join(DATA, name), encoding="utf-8"))


def get(url):
    last = None
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 + 3 * i)
    raise last


def months_from(start, n):
    y, m = int(start[:4]), int(start[5:7])
    out = []
    for _ in range(n):
        out.append(f"{y}-{m:02d}")
        m += 1
        if m > 12:
            y, m = y + 1, 1
    return out


def cpi_since_1994(cpi10):
    """CPI 1994-01.. on the scale of cbs-120010.json: the file from 2010-01, the API chain before it."""
    d = get("https://api.cbs.gov.il/index/data/price?id=120010&format=json&download=false&lang=he&startPeriod=01-1994&endPeriod=12-2011&PageSize=500")
    rows = sorted(d["month"][0]["date"], key=lambda r: (r["year"], r["month"]))
    out, factor = {}, 1.0
    newest = rows[-1]["currBase"]["baseDesc"]
    for i in range(len(rows) - 1, -1, -1):
        r = rows[i]
        base = r["currBase"]["baseDesc"]
        if base != newest:
            # the newer base is "<year> ממוצע": that year's average in the older base = 100
            yb = int(newest.split(" ")[0])
            olds = [x["currBase"]["value"] for x in rows if x["year"] == yb and x["currBase"]["baseDesc"] == base]
            if len(olds) != 12:
                raise SystemExit(f"cannot chain the CPI at {r['year']}-{r['month']}: {len(olds)} months of {yb} in base {base}")
            factor *= 100.0 / (sum(olds) / 12)
            newest = base
        out[f"{r['year']}-{r['month']:02d}"] = r["currBase"]["value"] * factor
    ov = [k for k in out if k >= "2010-01" and k in cpi10]
    ratios = [cpi10[k] / out[k] for k in ov]
    s = sum(ratios) / len(ratios)
    spread = (max(ratios) - min(ratios)) / s
    print(f"CPI overlap 2010-2011: {len(ov)} months, ratio {s:.6f}, spread {100 * spread:.3f}%")
    if spread > 0.002:
        raise SystemExit("the CPI chain does not sit flat on cbs-120010.json")
    keys = sorted(set(k for k in out if k < "2010-01") | set(cpi10))
    return [round(cpi10[k] if k in cpi10 else out[k] * s, 4) for k in keys], keys[0], keys[-1], round(100 * spread, 4)


def qend(q):
    """'1-3.2026' -> '2026-03' (the quarter as rent.json names it)."""
    a, y = q.split(".")
    return f"{y}-{int(a.split('-')[1]):02d}"


def main():
    vs = load("value-series.json")
    c10 = load("cbs-120010.json")
    rent = load("rent.json")
    boim = load("boi-mortgage.json")
    s = vs["cbs"]["s"]
    hpi = s["40010"]
    if hpi["from"] != "1994-01":
        raise SystemExit("40010 does not start in 1994-01")
    latest = months_from(hpi["from"], len(hpi["v"]))[-1]
    if latest != vs["cbs"]["latest"]:
        raise SystemExit(f"40010 ends {latest}, value-series says {vs['cbs']['latest']}")
    cpi, cfrom, clast, spread = cpi_since_1994(c10["months"])
    span = (int(clast[:4]) - 1994) * 12 + int(clast[5:7])
    if cfrom != "1994-01" or len(cpi) != span:
        raise SystemExit("the CPI months are not continuous")
    qs = vs["q"]
    rq = [qend(q) for q in qs]
    rent_by_code = {c["code"]: c for c in rent["cities"]}

    def rent_of(row):
        o = {}
        for k in ("3", "4", "5"):
            x = row.get("r", {}).get(k)
            if not x:
                continue
            m = {a: b for a, b in x.get("s", [])}
            o["r" + k] = {q: m[q] for q in rq if q in m}
        return o

    cities = []
    for n, c in vs["city"].items():
        if n not in SLUG:
            raise SystemExit(f"no slug decision for {n}")
        rr = rent_by_code.get(c["code"])
        cities.append({"n": n, "slug": SLUG[n], "dist": c["dist"], "cbs": c["cbs"], "code": c["code"],
                       "r3": c["r3"], "r4": c["r4"], "r5": c["r5"], "ra": c["ra"], "rent": rent_of(rr) if rr else {}})
    # the whole span against the CBS linkage calculator (the 20th of the next month: that month's index is the known one)
    y, m = int(clast[:4]), int(clast[5:7]) + 1
    if m > 12:
        y, m = y + 1, 1
    check = None
    try:
        calc = get(f"https://api.cbs.gov.il/index/data/calculator/120010?value=100&date=02-20-1994&toDate={m:02d}-20-{y}&format=json&download=false")
        check = {"from": "1994-01", "to": clast, "ours": round(100 * cpi[-1] / cpi[0], 3), "cbs": calc["answer"]["to_value"]}
        print("CPI check vs the CBS calculator:", check)
        if abs(check["ours"] / float(check["cbs"]) - 1) > 0.001:
            raise SystemExit("the CPI chain is off the CBS calculator by more than 0.1%")
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 (the calculator is a check, not a source)
        print("CPI calculator check skipped:", e)
    fx = boim["rates"]["fixed_nl"]
    src0 = boim["sources"][0]
    out = {
        "key": "phub",
        "built": time.strftime("%Y-%m-%d"),
        "note": "HAD-681: built by tools/instruments/build_prices_hub.py from value-series.json, cbs-120010.json, rent.json, boi-mortgage.json and the CBS API (CPI 1994-2009).",
        "hpi": {"from": hpi["from"], "v": hpi["v"], "latest": latest, "base": hpi["base"],
                "deals": "the API month M is the deals of M and M+1, published about the 15th of M+3",
                "src": {"he": "הלשכה המרכזית לסטטיסטיקה, מדד מחירי הדירות (סדרה 40010, ממוצע 1993 = 100) והמדדים לפי מחוז (60000 עד 60500)", "url": "https://www.cbs.gov.il/he/subjects/Pages/%D7%9E%D7%93%D7%93-%D7%9E%D7%97%D7%99%D7%A8%D7%99-%D7%93%D7%99%D7%A8%D7%95%D7%AA.aspx", "read": vs["cbs"]["read"]}},
        "dist": [{"id": k, "n": DIST[k], "from": s[k]["from"], "v": s[k]["v"]} for k in ("60400", "60300", "60000", "60200", "60100", "60500")],
        "cpi": {"from": cfrom, "v": cpi, "latest": clast, "spread_pct": spread, "check": check,
                "src": {"he": "הלשכה המרכזית לסטטיסטיקה, מדד המחירים לצרכן (סדרה 120010)", "url": "https://www.cbs.gov.il/he/subjects/Pages/%D7%9E%D7%93%D7%93-%D7%94%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D-%D7%9C%D7%A6%D7%A8%D7%9B%D7%9F.aspx", "read": time.strftime("%Y-%m-%d")}},
        "q": qs,
        "il": {"r3": vs["il"]["r3"], "r4": vs["il"]["r4"], "r5": vs["il"]["r5"], "ra": vs["il"]["ra"], "rent": rent_of(rent["nat"])},
        "city": cities,
        "vsrc": {"he": "רשות המסים, עסקאות שנסגרו, דרך אתר הנדל״ן הממשלתי: חציון לפי מספר חדרים", "url": vs["url"], "version": vs["file"], "read": vs["read"]},
        "rsrc": {"he": "אתר הנדל״ן הממשלתי, שכר דירה חציוני לפי עיר וחדרים", "url": rent["src"]["gov"]["url"], "read": rent["src"]["gov"]["read"]},
        "mort": {"eff": fx["rate"], "month": fx["hist"][-1][0], "label": fx["label"], "ltv": boim["rules"]["ltv"]["single"], "years": 25,
                 "src": {"he": "בנק ישראל, הריבית הממוצעת על הלוואות חדשות לדיור", "url": src0["url"]},
                 "ltvSrc": {"he": boim["rules"]["src"]["label"], "url": boim["rules"]["src"]["url"]}},
    }
    path = os.path.join(DATA, "prices-hub.json")
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print("wrote", path, os.path.getsize(path), "bytes; hpi", out["hpi"]["latest"], "cpi", clast, "cities", len(cities))


if __name__ == "__main__":
    main()
