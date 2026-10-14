# -*- coding: utf-8 -*-
"""HAD-527: official index series for the Instruments (CBS public API, no key). Chains every base into the latest base so any
two months compare directly, and checks the chain against the CBS's own linkage calculator.
python build_index_data.py   -> plugins/nadlan-config/assets/instruments/data/cbs-<id>.json"""
import json
import os
import time
import urllib.request

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "assets", "instruments", "data")
SERIES = {200010: "מדד מחירי תשומה בבנייה למגורים", 120010: "מדד המחירים לצרכן"}
UA = {"User-Agent": "Mozilla/5.0 NadLan-instruments"}


def get(url):
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except Exception as e:
            time.sleep(2 + 3 * i); last = e
    raise last


for sid, name in SERIES.items():
    rows, page = [], 1
    while True:
        d = get(f"https://api.cbs.gov.il/index/data/price?id={sid}&format=json&download=false&lang=he&startPeriod=01-2010&PageSize=500&Page={page}")
        m = d["month"][0]["date"]
        rows += m
        if d["paging"]["current_page"] >= d["paging"]["last_page"]:
            break
        page += 1
    rows.sort(key=lambda r: (r["year"], r["month"]))
    # chain: walk back from the newest; a month whose base differs from its successor's is converted by the ratio at the
    # successor (its prevBase value = the same month in the older base)
    out, factor = {}, 1.0
    newest_base = rows[-1]["currBase"]["baseDesc"]
    for i in range(len(rows) - 1, -1, -1):
        r = rows[i]
        key = f"{r['year']}-{r['month']:02d}"
        if r["currBase"]["baseDesc"] != newest_base and i + 1 < len(rows):
            nxt = rows[i + 1]
            if nxt["currBase"]["baseDesc"] != r["currBase"]["baseDesc"]:
                # the newer base names its base period: "2025 יולי" (that month = 100) or "2024 ממוצע" (that year's average = 100)
                yb, per = nxt["currBase"]["baseDesc"].split(" ", 1)
                old_base = r["currBase"]["baseDesc"]
                if "ממוצע" in per:
                    olds = [x["currBase"]["value"] for x in rows if x["year"] == int(yb) and x["currBase"]["baseDesc"] == old_base]
                    if len(olds) != 12:
                        raise SystemExit(f"cannot chain {sid} at {key}: {len(olds)} months of {yb} in the old base")
                    ref = sum(olds) / 12
                else:
                    MON = {"ינואר": 1, "פברואר": 2, "מרץ": 3, "אפריל": 4, "מאי": 5, "יוני": 6, "יולי": 7, "אוגוסט": 8, "ספטמבר": 9, "אוקטובר": 10, "נובמבר": 11, "דצמבר": 12}
                    mm = MON[per.strip()]
                    ref = [x["currBase"]["value"] for x in rows if x["year"] == int(yb) and x["month"] == mm and x["currBase"]["baseDesc"] == old_base]
                    if not ref:
                        raise SystemExit(f"cannot chain {sid} at {key}: base month not in the old base")
                    ref = ref[0]
                factor *= 100.0 / ref
                newest_base = old_base
        out[key] = round(r["currBase"]["value"] * factor, 4)
    months = dict(sorted(out.items()))
    # align every base boundary to the CBS calculator's own chaining (its coefficient is rounded; ours came from averages)
    ks = list(months)
    bases = {f"{r['year']}-{r['month']:02d}": r["currBase"]["baseDesc"] for r in rows}
    for i in range(1, len(ks)):
        a, b = ks[i - 1], ks[i]
        if bases[a] == bases[b]:
            continue
        def nxt(k):
            y, m = int(k[:4]), int(k[5:]) + 1
            return (y + (m > 12), (m - 1) % 12 + 1)
        (ya, ma), (yb, mb) = nxt(a), nxt(b)
        c = get(f"https://api.cbs.gov.il/index/data/calculator/{sid}?value=1000000&date={ma:02d}-20-{ya}&toDate={mb:02d}-20-{yb}&format=json&download=false")
        r_cbs = float(c["answer"]["to_value"]) / 1000000
        r_ours = months[b] / months[a]
        f = r_ours / r_cbs
        for k in ks[:i]:
            months[k] = round(months[k] * f, 6)
        print(f"   {sid} boundary {a}->{b}: ours {r_ours:.5f} cbs {r_cbs:.5f} scale {f:.6f}")
    last = list(months)[-1]
    # check two spans against the CBS linkage calculator
    checks = []
    for a, b in (("2022-07", last), ("2019-01", last)):
        if a not in months:
            continue
        ya, ma = a.split("-"); yb, mb = b.split("-")
        c = get(f"https://api.cbs.gov.il/index/data/calculator/{sid}?value=100&date={int(ma) % 12 + 1:02d}-20-{int(ya) + (1 if ma == '12' else 0)}&toDate={int(mb) % 12 + 1:02d}-20-{int(yb) + (1 if mb == '12' else 0)}&format=json&download=false")  # the 20th of the next month: that month's index is the known one
        cbs = c.get("answer", {}).get("to_value") if isinstance(c.get("answer"), dict) else None
        ours = 100 * months[b] / months[a]
        checks.append({"from": a, "to": b, "ours": round(ours, 3), "cbs": cbs})
    data = {"id": sid, "name": name, "unit": "points, chained to the latest base", "base": rows[-1]["currBase"]["baseDesc"], "latest": last,
            "source": f"הלשכה המרכזית לסטטיסטיקה, סדרה {sid}", "fetched": time.strftime("%Y-%m-%d"), "check": checks, "months": months}
    json.dump(data, open(os.path.join(OUT, f"cbs-{sid}.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(sid, name, len(months), "months, latest", last, "checks", checks)
