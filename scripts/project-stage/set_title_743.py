# -*- coding: utf-8 -*-
"""HAD-743, Ben 15.11.2026 approved the H1 "מבצעי קבלנים 2026: מפת כל המבצעים בישראל" for /developer-deals/ (Hebrew page).
Changes the page title only (the H1); the Yoast SEO title, the slug and the publish date stay. Saves before/after to the research folder.
python scripts/project-stage/set_title_743.py [--check]"""
import io, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "title743"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
NEW = "מבצעי קבלנים 2026: מפת כל המבצעים בישראל"
s, r, _ = req("GET", "/wp-json/wp/v2/pages?slug=developer-deals&context=edit&_fields=id,title,date,modified,link,yoast_head_json,meta")
pages = [p for p in r if "/en/" not in p.get("link", "")] if isinstance(r, list) else []
assert len(pages) == 1, (s, [p.get("link") for p in (r if isinstance(r, list) else [])])
p = pages[0]
before = {"id": p["id"], "title": p["title"]["raw"], "date": p["date"], "modified": p["modified"], "seo_title": (p.get("yoast_head_json") or {}).get("title")}
print("before:", json.dumps(before, ensure_ascii=False))
out = os.path.join(REPO, "docs", "research", "2026-11-15-deals-board", "h1-change-%s.json" % time.strftime("%Y%m%dT%H%M%S"))
if "--check" in sys.argv or before["title"] == NEW:
    sys.exit(0)
s, r2, _ = req("POST", "/wp-json/wp/v2/pages/%d" % p["id"], {"title": NEW})
after = {"http": s, "title": r2.get("title", {}).get("raw") if isinstance(r2, dict) else r2, "date": r2.get("date") if isinstance(r2, dict) else None}
print("after:", json.dumps(after, ensure_ascii=False))
assert after["title"] == NEW and after["date"] == before["date"], after
io.open(out, "w", encoding="utf-8").write(json.dumps({"before": before, "after": after}, ensure_ascii=False, indent=1))
