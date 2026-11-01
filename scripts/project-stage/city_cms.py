# -*- coding: utf-8 -*-
"""HAD-642 loop L3a: append [nadlan_city_projects city="..."] to the end of the pages that own the cities (their price
pages), so each owns "פרויקטים חדשים ב<city>" without a new URL. Additive: the page's content stays, the block goes after it.
Backup docs/qa/compound-wave/city-backup.json; --undo restores."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
RUNNER = sorted([f for f in os.listdir(H) if f.startswith("deploy5") and f.endswith(".py") and f[6:9].isdigit()])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read(); sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "city", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
BK = os.path.join(REPO, "docs", "qa", "compound-wave", "city-backup.json")
PAGES = {4570: "רמת גן", 4573: "פתח תקוה", 4581: "ראשון לציון", 4891: "בת ים", 4585: "חולון", 4571: "גבעתים", 4597: "אילת"}
if "--undo" in ARGV:
    for pid, c in json.load(open(BK, encoding="utf-8")).items():
        print("[undo]", pid, req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": c})[0])
    raise SystemExit(0)
bk = json.load(open(BK, encoding="utf-8")) if os.path.exists(BK) else {}
for pid, city in PAGES.items():
    cur = must(*req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=slug,content"), f"read {pid}")
    c = cur["content"]["raw"]
    if "[nadlan_city_projects" in c:
        print("[has]", pid); continue
    if str(pid) not in bk:
        bk[str(pid)] = c; json.dump(bk, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    body = c.rstrip() + '\n\n[nadlan_city_projects city="' + city + '"]'
    st, d = req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": body})
    print(f"[city] {pid} {cur['slug']}: {'OK' if st in (200, 201) and d.get('content', {}).get('raw') == body else 'CHECK ' + str(st)}")
