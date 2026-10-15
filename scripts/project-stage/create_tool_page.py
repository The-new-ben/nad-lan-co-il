# -*- coding: utf-8 -*-
"""HAD-527: publish a NEW tool page from docs/tools/<id>/page.html + meta.json (title, slug, seo_title, seo_desc).
Gates: the slug is free at the root, no published page or post carries the same title, the content holds exactly one
[nadlan_tool] shortcode per tool in meta.tools (default: the id), under meta.parent if given. After publishing: 200, exactly one H1, the instrument host, the tool script, the JSON-LD, no raw
shortcode, the Yoast title. Any failed check moves the page to draft (never deleted).   python create_tool_page.py <id> [--dry]"""
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "toolpage"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
tool = sys.argv[1]
W = os.path.join(REPO, "docs", "tools", tool)
html = io.open(os.path.join(W, "page.html"), encoding="utf-8").read()
meta = json.load(io.open(os.path.join(W, "meta.json"), encoding="utf-8"))
TOOLS = meta.get("tools") or [tool]  # a page may hold several tools (HAD-534: the soil map + the PFAS calculator)
PARENT = int(meta.get("parent") or 0)  # a child page under an existing guide (e.g. /sde-dov/contamination/)
if html.count("[nadlan_tool") != len(TOOLS) or any(f'[nadlan_tool id="{t}"]' not in html for t in TOOLS):
    raise SystemExit("FATAL: the content needs exactly the shortcodes %s" % TOOLS)
s, b, _ = req("GET", f"/wp-json/wp/v2/pages?slug={meta['slug']}&parent={PARENT}&status=publish,draft,private,pending&context=edit&_fields=id,status,link")
if isinstance(b, list) and b:
    raise SystemExit(f"FATAL: the slug is taken: {b[0]}")
for t in ("pages", "posts"):
    s, hits, _ = req("GET", f"/wp-json/wp/v2/{t}?search={urllib.parse.quote(meta['title'])}&_fields=id,title,link&per_page=20")
    same = [h for h in (hits or []) if re.sub(r"<[^>]+>", "", h["title"]["rendered"]).strip() == meta["title"]]
    if same:
        raise SystemExit(f"FATAL: the same title exists: {same}")
print(f"[plan] /{meta['slug']}/ · H1 '{meta['title']}' · SEO {len(meta['seo_title'])}/{len(meta['seo_desc'])} chars · {len(html):,} chars")
if "--dry" in sys.argv:
    raise SystemExit(0)
s, b, _ = req("POST", "/wp-json/wp/v2/pages", {"title": meta["title"], "slug": meta["slug"], "status": "publish", "content": html, "parent": PARENT,
                                               "meta": {"_yoast_wpseo_title": meta["seo_title"], "_yoast_wpseo_metadesc": meta["seo_desc"]}})
if s not in (200, 201) or not b.get("id"):
    raise SystemExit(f"FATAL create {s}")
pid, link = b["id"], b["link"]
json.dump({"id": pid, "link": link, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}, io.open(os.path.join(W, "published.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("[created]", pid, link)
time.sleep(3)
live = urllib.request.urlopen(urllib.request.Request(link + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
body = live[live.find("<body"):]
checks = {"one h1": body.count("<h1") == 1, "host": all(f'data-nli="{t}"' in body for t in TOOLS), "script": all(f"/plugins/nadlan-config/assets/instruments/tools/{t}.js" in live for t in TOOLS),
          "json-ld": 'id="nadlan-nli-ld"' in live, "no raw shortcode": "[nadlan_tool" not in body, "yoast title": meta["seo_title"].split(":")[0] in live[:20000]}
for k, v in checks.items():
    print("  ", "OK " if v else "BAD", k)
if not all(checks.values()):
    print("[draft]", req("POST", f"/wp-json/wp/v2/pages/{pid}", {"status": "draft"})[0]); raise SystemExit(1)
print("[done]", link)
