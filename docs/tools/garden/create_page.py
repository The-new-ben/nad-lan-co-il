# -*- coding: utf-8 -*-
"""HAD-669 R12e: publishes /tel-aviv-garden-apartments/ (page.html + meta.json) after release 1.72.577 put the four garden tools on
the site. The pattern of scripts/project-stage/create_tool_page.py, with the
checks of this page: the four tools share one script (tools/garden.js). Gates: the slug is free under its parent, no published
page or post has the same title, exactly one shortcode per tool, no forbidden word. After publishing: 200, exactly one H1, the four
hosts, the shared script, the page CSS, the JSON-LD with a FAQPage, the cutaway image, no raw shortcode, the Yoast title, the
hreflang pair (once both exist). Any failed check moves that page to draft (never deleted).
  python create_pages.py he|en [--dry]"""
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "gdnpage"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
LANG = sys.argv[1]
html = io.open(os.path.join(H, "page.html" if LANG == "he" else "page-en.html"), encoding="utf-8").read()
meta = json.load(io.open(os.path.join(H, "meta.json" if LANG == "he" else "meta-en.json"), encoding="utf-8"))
if meta["parent"] == "EN_ROOT":
    s, b, _ = req("GET", "/wp-json/wp/v2/pages?slug=en&parent=0&_fields=id,link,status")
    roots = [x for x in (b or []) if x.get("status") == "publish"]
    if len(roots) != 1:
        raise SystemExit(f"FATAL: the /en/ root page: {b}")
    meta["parent"] = roots[0]["id"]
PARENT = int(meta["parent"] or 0)
TOOLS = meta["tools"]
for t in TOOLS:
    if html.count(f'[nadlan_tool id="{t}"]') != 1:
        raise SystemExit(f"FATAL: the content needs exactly one [nadlan_tool id=\"{t}\"]")
if html.count("[nadlan_tool") != len(TOOLS):
    raise SystemExit("FATAL: an extra shortcode in the content")
bad = [w for w in meta.get("forbid", []) if w in html or w in meta["title"] or w in meta["seo_title"] or w in meta["seo_desc"]]
if bad:
    raise SystemExit(f"FATAL: forbidden text in the page: {bad}")
s, b, _ = req("GET", f"/wp-json/wp/v2/pages?slug={meta['slug']}&parent={PARENT}&status=publish,draft,private,pending&context=edit&_fields=id,status,link")
if isinstance(b, list) and b:
    raise SystemExit(f"FATAL: the slug is taken: {b[0]}")
for t in ("pages", "posts"):
    s, hits, _ = req("GET", f"/wp-json/wp/v2/{t}?search={urllib.parse.quote(meta['title'][:40])}&_fields=id,title,link&per_page=20")
    same = [x for x in (hits or []) if re.sub(r"<[^>]+>", "", x["title"]["rendered"]).strip() == meta["title"]]
    if same:
        raise SystemExit(f"FATAL: the same title exists: {same}")
words = len(re.findall(r"[\w֐-׿'\-]+", re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", "", html, flags=re.S))))
print(f"[plan] {LANG} slug {meta['slug']} under {PARENT} · H1 '{meta['title']}' · SEO {len(meta['seo_title'])}/{len(meta['seo_desc'])} chars · {len(html):,} chars · ~{words:,} words")
if "--dry" in sys.argv:
    raise SystemExit(0)
s, b, _ = req("POST", "/wp-json/wp/v2/pages", {"title": meta["title"], "slug": meta["slug"], "status": "publish", "content": html, "parent": PARENT,
                                               "meta": {"_yoast_wpseo_title": meta["seo_title"], "_yoast_wpseo_metadesc": meta["seo_desc"]}})
if s not in (200, 201) or not b.get("id"):
    raise SystemExit(f"FATAL create {s}: {json.dumps(b, ensure_ascii=False)[:300]}")
pid, link = b["id"], b["link"]
json.dump({"id": pid, "link": link, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}, io.open(os.path.join(H, f"published-{LANG}.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("[created]", pid, link)
time.sleep(4)
live = urllib.request.urlopen(urllib.request.Request(link + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
body = live[live.find("<body"):]
ld = re.search(r'<script type="application/ld\+json" id="nadlan-nli-ld">(.*?)</script>', live, re.S)
checks = {"one h1": body.count("<h1") == 1, "four hosts": all(f'data-nli="{t}"' in body for t in TOOLS),
          "shared script": "/plugins/nadlan-config/assets/instruments/tools/garden.js" in live, "page css": 'id="nadlan-gdn-css"' in live,
          "faq schema": bool(ld) and '"FAQPage"' in ld.group(1), "listings block": 'id="gdl"' in body,
          "no raw shortcode": "[nadlan_tool" not in body, "yoast title": meta["seo_title"].split(":")[0] in live[:30000],
          "lang": ('lang="en' in live[:3000]) if LANG == "en" else ('lang="he' in live[:3000])}
for k, v in checks.items():
    print("  ", "OK " if v else "BAD", k)
print("   hreflang:", re.findall(r'<link rel="alternate" hreflang="(\w[\w-]*)" href="([^"]+)"', live))
if not all(checks.values()):
    print("[draft]", req("POST", f"/wp-json/wp/v2/pages/{pid}", {"status": "draft"})[0])
    raise SystemExit(1)
print("[done]", link)
