# -*- coding: utf-8 -*-
"""HAD-460, the CEO's rule (7.10.2026): no hard price number in a city page's title, H1 or description (it ages and lies within a
quarter; the official figures live in the price list with their data date). The scan (docs/qa/had-460/city-titles/scan.json)
found 14 of 24 pages with numbers in the Yoast title or description, many stale against the official medians.
- title:       "מחירי דירות ב{X} 2026: חציון לפי חדרים, עסקאות ומגמה | נדלן"   (X = the city as the page's own H1 names it)
- description: "מחירי דירות ב{X} 2026 לפי מספר החדרים והשכונות: עסקאות, מגמת המחירים ומה לבדוק לפני שמחליטים."
Only fields that carry a number change; H1s carry none. Backup before, read-back after, rendered <title> checked.
python city_titles_fix.py [--dry | --rollback <backup.json>]"""
import html
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SCAN = os.path.join(REPO, "docs", "qa", "had-460", "city-titles", "scan.json")
BK = os.path.join(REPO, "docs", "qa", "had-460", "city-titles")
ARGS = sys.argv[1:]
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "ct"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
NUM = re.compile(r'(\d[\d,.]*\s*(?:מיליון|מ׳|מ\'|אלף|K|₪|ש"ח|שח))|(₪\s*\d)')

if "--rollback" in ARGS:
    bk = json.load(io.open(ARGS[ARGS.index("--rollback") + 1], encoding="utf-8"))
    for p in bk:
        s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{p['id']}", {"meta": {"_yoast_wpseo_title": p["yoast_title"], "_yoast_wpseo_metadesc": p["yoast_desc"]}})
        print("[rollback]", p["slug"], s)
    raise SystemExit(0)

rows = json.load(io.open(SCAN, encoding="utf-8"))
plan, backup = [], []
for r in rows:
    if not r.get("num_in"):
        continue
    m = re.match(r"מחירי דירות ב(.+?)(?: לפי|:|$)", r["h1"])
    if not m:
        print("[skip] no city name in the H1:", r["slug"], r["h1"]); continue
    x = m.group(1).strip()
    new = {}
    if "yoast_title" in r["num_in"] or "wp_title" in r["num_in"]:
        new["_yoast_wpseo_title"] = f"מחירי דירות ב{x} 2026: חציון לפי חדרים, עסקאות ומגמה | נדלן"
    if "yoast_desc" in r["num_in"]:
        new["_yoast_wpseo_metadesc"] = f"מחירי דירות ב{x} 2026 לפי מספר החדרים והשכונות: עסקאות, מגמת המחירים ומה לבדוק לפני שמחליטים."
    for k, v in new.items():
        if NUM.search(v) or len(v) > (70 if k == "_yoast_wpseo_title" else 160):
            raise SystemExit(f"FATAL: {r['slug']} {k} breaks the rule: {v}")
    plan.append((r, new))
    print(f"[plan] {r['slug']}: " + " | ".join(f"{k[13:]}: {v}" for k, v in new.items()))
if "--dry" in ARGS:
    raise SystemExit(0)
stamp = time.strftime("%Y%m%dT%H%M%S")
for r, new in plan:
    s, b, _ = req("GET", f"/wp-json/wp/v2/pages/{r['id']}?context=edit&_fields=meta")
    m = b.get("meta") or {}
    backup.append({"id": r["id"], "slug": r["slug"], "yoast_title": m.get("_yoast_wpseo_title", ""), "yoast_desc": m.get("_yoast_wpseo_metadesc", "")})
bkp = os.path.join(BK, f"backup-{stamp}.json")
io.open(bkp, "w", encoding="utf-8").write(json.dumps(backup, ensure_ascii=False, indent=1))
print("[backup]", os.path.relpath(bkp, REPO))
bad = []
for r, new in plan:
    s, w, _ = req("POST", f"/wp-json/wp/v2/pages/{r['id']}", {"meta": new})
    s2, b, _ = req("GET", f"/wp-json/wp/v2/pages/{r['id']}?context=edit&_fields=meta")
    ok = s == 200 and all((b.get("meta") or {}).get(k) == v for k, v in new.items())
    u = "https://nad-lan.co.il/" + r["slug"] + "/?nlct=%d" % time.time()
    h = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-ct"}), timeout=90).read().decode("utf-8", "replace")
    t = html.unescape((re.search(r"<title>(.*?)</title>", h, re.S) or [None, ""])[1] if re.search(r"<title>(.*?)</title>", h, re.S) else "")
    rendered_ok = "_yoast_wpseo_title" not in new or t == new["_yoast_wpseo_title"]
    print(f"[write] {r['slug']}: {s}, meta read-back {ok}, rendered title {'OK' if rendered_ok else 'DIFFERENT: ' + t}")
    if not (ok and rendered_ok):
        bad.append(r["slug"])
print("[done] bad:", bad, "| rollback with: python city_titles_fix.py --rollback", os.path.relpath(bkp, REPO))
