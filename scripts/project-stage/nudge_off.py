# -*- coding: utf-8 -*-
"""Ben 1.11.2026: take the price slip down now. Every project whose box says "on" goes to "off" (backup first)."""
import json, os, sys
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"; os.chdir(REPO)
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "nu", "__file__": os.path.join(REPO, "scripts", "skin-a", "deployskin.py")}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin", "exec"), ns)
req = ns["req"]
on = []; page = 1
while True:
    s, d, _ = req("GET", f"/wp-json/wp/v2/nadlan_project?context=edit&per_page=100&page={page}&status=publish&_fields=id,slug,meta")
    if s != 200 or not isinstance(d, list) or not d: break
    on += [(p["id"], p["slug"]) for p in d if (p.get("meta") or {}).get("nadlan_nudge") == "on"]
    page += 1
print("on:", on)
bk = os.path.join(REPO, "docs", "qa", "compound-wave", "nudge-off-20261101.json")
json.dump({str(i): "on" for i, _ in on}, open(bk, "w", encoding="utf-8"))
for i, slug in on:
    s, d, _ = req("POST", f"/wp-json/wp/v2/nadlan_project/{i}", {"meta": {"nadlan_nudge": "off"}})
    print("[off]", i, slug, s, (d.get("meta") or {}).get("nadlan_nudge"))
s, o, _ = req("GET", "/wp-json/wp/v2/settings")
