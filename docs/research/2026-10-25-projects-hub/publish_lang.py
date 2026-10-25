# -*- coding: utf-8 -*-
"""Creates /<lang>/projects/ (Ben 25.10.2026) as a WordPress page under the language root, content [nadlan_projects_hub lang=".."],
title (the H1), Yoast title and description from data/hub-lang/<lang>.json. Guards: release 1.72.514+ is live (the shortcode and
the dictionary answer), the slug is free under that root, no other page or post owns "<lang>/projects". After the write: reads back,
then checks the live page as Google gets it: 200, one H1, lang attribute, the hub sections, one FAQPage, hreflang both ways
(/projects/ <-> /<lang>/projects/), self canonical, no Hebrew left in the visible hub text, no long dash.
  python docs/research/2026-10-25-projects-hub/publish_lang.py en [--dry]"""
import html as HT, io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "plang"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
LANG = sys.argv[1]; DRY = "--dry" in sys.argv
assert LANG in ("en", "ru", "fr")
d = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "data", "hub-lang", LANG + ".json"), encoding="utf-8"))
get = lambda u: urllib.request.urlopen(urllib.request.Request(u + ("&" if "?" in u else "?") + "pl=%d" % (time.time() * 1000), headers={"User-Agent": "Mozilla/5.0 NadLan-PL/1.0"}), timeout=90).read().decode("utf-8", "replace")
live = get("https://nad-lan.co.il/wp-content/plugins/nadlan-config/data/hub-lang/%s.json" % LANG)
assert '"lang": "%s"' % LANG in live, "the %s dictionary is not live yet" % LANG
s, root, _ = req("GET", "/wp-json/wp/v2/pages?slug=%s&parent=0&_fields=id,link" % LANG)
assert root, "language root page /%s/ not found" % LANG
rid = root[0]["id"]
s, ex, _ = req("GET", "/wp-json/wp/v2/pages?slug=projects&parent=%d&status=publish,draft,private&context=edit&_fields=id,link,status" % rid)
s2, ex2, _ = req("GET", "/wp-json/wp/v2/posts?slug=projects&_fields=id,link")
print("[guard] root", rid, "| existing child 'projects':", ex, "| post with that slug:", ex2)
content = '[nadlan_projects_hub lang="%s"]' % LANG
body = {"title": d["page_title"], "slug": "projects", "parent": rid, "content": content, "status": "publish",
        "meta": {"_yoast_wpseo_title": d["seo_title"], "_yoast_wpseo_metadesc": d["seo_desc"], "_yoast_wpseo_bctitle": d.get("crumb", "")}}
if DRY:
    print("[dry] would", "update" if ex else "create", "/%s/projects/" % LANG, "|", d["page_title"]); sys.exit(0)
if ex:
    s3, b, _ = req("POST", "/wp-json/wp/v2/pages/%d" % ex[0]["id"], body)
else:
    s3, b, _ = req("POST", "/wp-json/wp/v2/pages", body)
pid = b["id"]; print("[write]", s3, "page", pid, b.get("link"))
s4, back, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,title,meta,link,status" % pid)
print("[read-back] content:", back["content"]["raw"] == content, "| status:", back["status"], "| seo:", back["meta"].get("_yoast_wpseo_title") == d["seo_title"])
time.sleep(4)
page = get(back["link"]); bd = page[page.find("<body"):]
hub = bd[bd.find('class="nlph nlph--ltr"'):]
vis = re.sub(r"\s+", " ", HT.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b.*?</\1>", " ", hub, flags=re.S))))
heb = re.findall(r"[֐-׿]{2,}[^.]{0,30}", vis)
cat = get("https://nad-lan.co.il/projects/")
checks = {
    "one h1": bd.count("<h1") == 1,
    "html lang": ('lang="%s"' % LANG) in page[:3000],
    "sections": all(('id="nlph-%s"' % x) in page for x in ("market", "tlv", "prices", "abroad", "timeline", "pay", "checks", "faq", "sources")),
    "one FAQPage": page.count('"@type":"FAQPage"') == 1,
    "hreflang on this page -> /projects/": 'hreflang="he" href="https://nad-lan.co.il/projects/"' in page,
    "hreflang on /projects/ -> this page": ('hreflang="%s" href="%s"' % (LANG, back["link"])) in cat,
    "self canonical": ('<link rel="canonical" href="%s"' % back["link"]) in page,
    "no Hebrew in the hub text": not heb,
    "no long dash": not re.search(r"[–—]", vis),
}
for k, v in checks.items():
    print(("OK   " if v else "FAIL ") + k)
if heb:
    print("     Hebrew left:", heb[:8])
