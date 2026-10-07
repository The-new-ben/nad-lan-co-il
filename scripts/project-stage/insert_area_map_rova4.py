# -*- coding: utf-8 -*-
"""HAD-460: the 3D map on the Rova 4 page (page 8218), right after its price list. Needs plugin 1.72.437+ (the map door).
Backup before, read-back after.   python insert_area_map_rova4.py [--dry | --rollback <backup.json>]"""
import io, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "am"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns); req = ns["req"]
PID, PG, AM = 8218, '[nadlan_price_guide key="rova-4"]', '[nadlan_area_map key="rova-4"]'
s, b, _ = req("GET", f"/wp-json/wp/v2/pages/{PID}?context=edit&_fields=content,modified")
raw = b["content"]["raw"]
if "--rollback" in sys.argv:
    bk = json.load(io.open(sys.argv[-1], encoding="utf-8")); s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{PID}", {"content": bk["content"]}); print("[rollback]", s); raise SystemExit(0)
if AM in raw: raise SystemExit("already there")
if raw.count(PG) != 1: raise SystemExit("FATAL: the price-list shortcode is not there once")
s, h, _ = req("GET", "/wp-json/nadlan/v1/health")
if tuple(int(x) for x in h["version"].split(".")) < (1, 72, 437): raise SystemExit("FATAL: needs 1.72.437, live is " + h["version"])
new = raw.replace(PG, PG + "\n" + AM + "\n")
if "--dry" in sys.argv: print("[dry] ok"); raise SystemExit(0)
os.makedirs(os.path.join(REPO, "docs", "qa", "had-460", "align-backup"), exist_ok=True)
bkp = os.path.join(REPO, "docs", "qa", "had-460", "align-backup", f"page-{PID}-map-{time.strftime('%Y%m%dT%H%M%S')}.json")
io.open(bkp, "w", encoding="utf-8").write(json.dumps({"id": PID, "content": raw}, ensure_ascii=False))
s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{PID}", {"content": new})
s2, a, _ = req("GET", f"/wp-json/wp/v2/pages/{PID}?context=edit&_fields=content")
print("[write]", s, "read-back identical:", a["content"]["raw"] == new, "| backup", os.path.relpath(bkp, REPO))
