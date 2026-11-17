# -*- coding: utf-8 -*-
"""Read-only inventory of every published item that belongs to Meital Katsir (broker card 7833): properties linked by nl_broker_id,
the broker pages under /brokers/meital-katzir/ in every language, the professional card. Writes inventory.json (id, type, status, link)."""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "inv"}; exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
out = []
def pages(t, q):
    res, p = [], 1
    while True:
        s, b, _ = req("GET", f"/wp-json/wp/v2/{t}?{q}&per_page=100&page={p}&context=edit&status=publish,draft,private,pending&_fields=id,link,status,slug,parent,meta,title")
        if s != 200 or not b: break
        res += b; p += 1
        if len(b) < 100: break
    return res
for x in pages("nadlan_property", "orderby=id"):
    m = x.get("meta") or {}
    if str(m.get("nl_broker_id", "")) == "7833":
        out.append({"id": x["id"], "type": "nadlan_property", "status": x["status"], "link": x["link"], "title": x["title"]["raw"][:80]})
for x in pages("nadlan_professional", "slug=meital-katzir"):
    out.append({"id": x["id"], "type": "nadlan_professional", "status": x["status"], "link": x["link"], "title": x["title"]["raw"][:80]})
allp = pages("pages", "orderby=id")
ids = {x["id"] for x in allp if "meital" in x["slug"] or "meital-katzir" in x["link"]}
changed = True
while changed:
    changed = False
    for x in allp:
        if x["parent"] in ids and x["id"] not in ids: ids.add(x["id"]); changed = True
for x in allp:
    if x["id"] in ids:
        out.append({"id": x["id"], "type": "page", "status": x["status"], "link": x["link"], "title": x["title"]["raw"][:80]})
json.dump(out, open(os.path.join(H, "inventory.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for o in out: print(o["type"], o["id"], o["status"], o["link"])
print(len(out), "items")
