# -*- coding: utf-8 -*-
"""HAD-642 loop L3b: the luxury owner pages get data and tools at the end of their content (additive), with a backup
(docs/qa/compound-wave/lux-backup.json) and --undo. TLV luxury + TLV penthouse prices: the city's developer projects;
Herzliya Pituach luxury: Herzliya's developer projects; the penthouse glossary term: the purchase-cost instrument."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
RUNNER = sorted([f for f in os.listdir(H) if f.startswith("deploy5") and f.endswith(".py") and f[6:9].isdigit()])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read(); sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "lux", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
BK = os.path.join(REPO, "docs", "qa", "compound-wave", "lux-backup.json")
ITEMS = [("pages", 4768, '[nadlan_city_projects city="תל אביב יפו" only="dev" limit="20"]'),
         ("pages", 250, '[nadlan_city_projects city="תל אביב יפו" only="dev" limit="20"]'),
         ("pages", 4898, '[nadlan_city_projects city="הרצליה" only="dev"]'),
         ("nadlan_term", 4887, '[nadlan_tool id="pcost" kind="new"]')]
if "--undo" in ARGV:
    for k, c in json.load(open(BK, encoding="utf-8")).items():
        t, pid = k.split(":")
        print("[undo]", k, req("POST", f"/wp-json/wp/v2/{t}/{pid}", {"content": c})[0])
    raise SystemExit(0)
bk = json.load(open(BK, encoding="utf-8")) if os.path.exists(BK) else {}
for t, pid, sc in ITEMS:
    cur = must(*req("GET", f"/wp-json/wp/v2/{t}/{pid}?context=edit&_fields=slug,content"), f"read {t} {pid}")
    c = cur["content"]["raw"]
    if sc.split()[0] in c and (sc.split()[1] in c):
        print("[has]", pid); continue
    key = f"{t}:{pid}"
    if key not in bk:
        bk[key] = c; json.dump(bk, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    body = c.rstrip() + "\n\n" + sc
    st, d = req("POST", f"/wp-json/wp/v2/{t}/{pid}", {"content": body})
    print(f"[lux] {t} {pid} {cur['slug']}: {'OK' if st in (200, 201) and d.get('content', {}).get('raw') == body else 'CHECK ' + str(st)}")
