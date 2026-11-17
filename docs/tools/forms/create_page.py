# -*- coding: utf-8 -*-
"""HAD-768: publishes /forms/ (page.html + meta.json) after release 1.72.694 put [nadlan_forms] on the site. The pattern of
docs/tools/asbestos/create_pages.py. Gates: the slug is free, no page with the same title, exactly one [nadlan_forms], no forbidden
word. After publishing: 200, exactly one H1, the hub section, the hub script and CSS, the JSON-LD with CollectionPage and FAQPage,
no raw shortcode, the Yoast title. Any failed check moves the page to draft (never deleted).
  python docs/tools/forms/create_page.py [--dry]"""
import io, json, os, re, sys, time, urllib.parse, urllib.request

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "formspage"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
html = io.open(os.path.join(H, "page.html"), encoding="utf-8").read()
meta = json.load(io.open(os.path.join(H, "meta.json"), encoding="utf-8"))
if html.count("[nadlan_forms]") != 1:
    raise SystemExit("FATAL: the content needs exactly one [nadlan_forms]")
bad = [w for w in meta.get("forbid", []) if w in html or w in meta["title"] or w in meta["seo_title"] or w in meta["seo_desc"]]
if bad:
    raise SystemExit(f"FATAL: forbidden text in the page: {bad}")
s, b, _ = req("GET", f"/wp-json/wp/v2/pages?slug={meta['slug']}&status=publish,draft,private,pending&context=edit&_fields=id,status,link")
if isinstance(b, list) and b:
    raise SystemExit(f"FATAL: the slug is taken: {b[0]}")
s, hits, _ = req("GET", f"/wp-json/wp/v2/pages?search={urllib.parse.quote(meta['title'][:30])}&_fields=id,title,link&per_page=20")
same = [x for x in (hits or []) if re.sub(r"<[^>]+>", "", x["title"]["rendered"]).strip() == meta["title"]]
if same:
    raise SystemExit(f"FATAL: the same title exists: {same}")
print(f"[plan] slug {meta['slug']} · H1 '{meta['title']}' · SEO {len(meta['seo_title'])}/{len(meta['seo_desc'])} chars · {len(html):,} chars")
if "--dry" in sys.argv:
    raise SystemExit(0)
s, b, _ = req("POST", "/wp-json/wp/v2/pages", {"title": meta["title"], "slug": meta["slug"], "status": "publish", "content": html, "parent": 0,
                                               "meta": {"_yoast_wpseo_title": meta["seo_title"], "_yoast_wpseo_metadesc": meta["seo_desc"]}})
if s not in (200, 201) or not b.get("id"):
    raise SystemExit(f"FATAL create {s}: {json.dumps(b, ensure_ascii=False)[:300]}")
pid, link = b["id"], b["link"]
json.dump({"id": pid, "link": link, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}, io.open(os.path.join(H, "published.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("[created]", pid, link)
time.sleep(4)
live = urllib.request.urlopen(urllib.request.Request(link + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=120).read().decode("utf-8", "replace")
body = live[live.find("<body"):]
ld = re.search(r'<script type="application/ld\+json" id="nadlan-forms-ld">(.*?)</script>', live, re.S)
checks = {"one h1": body.count("<h1") == 1, "hub": 'id="nlfm"' in body, "data": 'id="nlfm-data"' in body,
          "script": "/plugins/nadlan-config/assets/forms/forms.js" in live, "css": "/plugins/nadlan-config/assets/forms/forms.css" in live,
          "schema": bool(ld) and '"CollectionPage"' in ld.group(1) and '"FAQPage"' in ld.group(1), "no raw shortcode": "[nadlan_forms" not in body,
          "yoast title": meta["seo_title"].split(":")[0] in live[:40000], "lang": 'lang="he' in live[:3000]}
for k, v in checks.items():
    print("  ", "OK " if v else "BAD", k)
if not all(checks.values()):
    print("[draft]", req("POST", f"/wp-json/wp/v2/pages/{pid}", {"status": "draft"})[0])
    raise SystemExit(1)
print("[done]", link)
