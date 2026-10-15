# -*- coding: utf-8 -*-
"""HAD-534: update an EXISTING tool page from docs/tools/<id>/page.html + meta.json (title, content, Yoast title/description),
page id from docs/tools/<id>/published.json. Backup before, read-back after, the rendered content checked for one H1, every
tool host, and words that must NOT appear (meta "forbid": e.g. company and project names). Any failed check restores the
backup.   python update_tool_page.py <id> [--dry]"""
import io
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "updatetoolpage"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
tool = sys.argv[1]
W = os.path.join(REPO, "docs", "tools", tool)
html = io.open(os.path.join(W, "page.html"), encoding="utf-8").read()
meta = json.load(io.open(os.path.join(W, "meta.json"), encoding="utf-8"))
pid = json.load(io.open(os.path.join(W, "published.json"), encoding="utf-8"))["id"]
TOOLS = meta.get("tools") or [tool]
FORBID = meta.get("forbid") or []
if html.count("[nadlan_tool") != len(TOOLS) or any(f'[nadlan_tool id="{t}"]' not in html for t in TOOLS):
    raise SystemExit("FATAL: the content needs exactly the shortcodes %s" % TOOLS)
bad = [w for w in FORBID if w in html or w in meta["title"] or w in meta["seo_title"] or w in meta["seo_desc"]]
if bad:
    raise SystemExit(f"FATAL: forbidden words in the source: {bad}")
s, b, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=title,content,link,modified,meta")
print(f"[plan] page {pid} {b['link']}: H1 '{meta['title']}' · {len(html):,} chars")
if "--dry" in sys.argv:
    raise SystemExit(0)
BK = os.path.join(REPO, "docs", "qa", "had-534", "page-backup"); os.makedirs(BK, exist_ok=True)
bk = os.path.join(BK, f"page-{pid}-{time.strftime('%Y%m%dT%H%M%S')}.json")
json.dump({"id": pid, "title": b["title"]["raw"], "raw": b["content"]["raw"], "meta": {k: (b.get("meta") or {}).get(k) for k in ("_yoast_wpseo_title", "_yoast_wpseo_metadesc")}},
          io.open(bk, "w", encoding="utf-8"), ensure_ascii=False)
print("[backup]", bk)
s, _, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}", {"title": meta["title"], "content": html, "meta": {"_yoast_wpseo_title": meta["seo_title"], "_yoast_wpseo_metadesc": meta["seo_desc"]}})
if s not in (200, 201):
    raise SystemExit(f"FATAL update {s}")
s, b2, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=title,content")
assert b2["content"]["raw"] == html and b2["title"]["raw"] == meta["title"], "read-back differs"
print("[read-back] OK")
time.sleep(3)
s, r, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?_fields=content,link")
rendered = r["content"]["rendered"]
live = urllib.request.urlopen(urllib.request.Request(r["link"] + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
body = live[live.find("<body"):]
checks = {"one h1": body.count("<h1") == 1, "h1 text": meta["title"].split(":")[0] in body, "hosts": all(f'data-nli="{t}"' in body for t in TOOLS),
          "no forbidden word in the content": not [w for w in FORBID if w in rendered], "yoast title": meta["seo_title"].split(":")[0] in live[:20000]}
for k, v in checks.items():
    print("  ", "OK " if v else "BAD", k)
if not all(checks.values()):
    old = json.load(io.open(bk, encoding="utf-8"))
    print("[restore]", req("POST", f"/wp-json/wp/v2/pages/{pid}", {"title": old["title"], "content": old["raw"], "meta": old["meta"]})[0]); raise SystemExit(1)
print("[done]", r["link"])
