# -*- coding: utf-8 -*-
"""HAD-460: publish a language version of an area page in the site's EXISTING page-language pattern (the CEO's decision B,
corrected 7.10.2026): /<lang>/<path>/ as a child of the language root page (inc/page-lang.php gives lang/dir, the hreflang
cluster and x-default to Hebrew automatically). Gates (the CEO's quality terms): check_translation.py PASSES on the article and
its meta; the URL is free; after publishing the live page must answer 200 with <html lang> = the language, exactly one H1, the
hreflang cluster on BOTH the language page and its Hebrew source, and (Rova 4) the price list and the map in that language.
Any failed check moves the new page to draft (never deleted).
python publish_en_area.py hub|rova-4 [--lang en] [--dry]      python publish_en_area.py --draft <page id>"""
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
WORK = os.path.join(REPO, "docs", "content", "north-tel-aviv-2026-10")
ARGS = sys.argv[1:]
LANG = ARGS[ARGS.index("--lang") + 1] if "--lang" in ARGS else "en"
ROOTS = {"en": 5011, "fr": 5055, "ru": 5056, "ar": 5057}
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "pubarea"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]


def page(url):
    r = urllib.request.urlopen(urllib.request.Request(url + ("&" if "?" in url else "?") + "nlpub=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0 NadLan-pub"}), timeout=90)
    return r.status, r.read().decode("utf-8", "replace")


def child(parent, slug):
    s, b, _ = req("GET", f"/wp-json/wp/v2/pages?slug={slug}&parent={parent}&status=publish,draft,private,pending&context=edit&_fields=id,status,link")
    return b[0] if isinstance(b, list) and b else None


if "--draft" in ARGS:
    pid = int(ARGS[ARGS.index("--draft") + 1])
    print("[draft]", req("POST", f"/wp-json/wp/v2/pages/{pid}", {"status": "draft"})[0]); raise SystemExit(0)

which = [a for a in ARGS if not a.startswith("--") and a not in ROOTS][0]
art = os.path.join(WORK, "out", f"{which}-{LANG}.html")
meta = os.path.join(WORK, "out", f"{which}-{LANG}.meta.txt")
# gate 1: the checker
chk = subprocess.run([sys.executable, os.path.join(WORK, "check_translation.py"), art, "--page", which, "--lang", LANG, "--meta", meta],
                     capture_output=True, text=True, encoding="utf-8", cwd=WORK, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
last = (chk.stdout.strip().splitlines() or [""])[-1]
print("[check]", chk.returncode, last[:160])
if chk.returncode != 0:
    raise SystemExit("FATAL: check_translation.py does not pass; nothing published")
html = io.open(art, encoding="utf-8").read()
mt = io.open(meta, encoding="utf-8").read()
seo_title = re.search(r"(?im)^\s*(?:seo[ _-]?)?title\s*:\s*(.+)$", mt)
seo_desc = re.search(r"(?im)^\s*(?:meta[ _-]?)?description\s*:\s*(.+)$", mt)
if not (seo_title and seo_desc):
    raise SystemExit("FATAL: the meta file has no title/description lines")
h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", html, re.S)
if html.count("<h1") != 1 or not h1:
    raise SystemExit("FATAL: the article must hold exactly one H1")
title = re.sub(r"<[^>]+>", "", h1.group(1)).strip()
if which == "hub":
    parent, slug, he_url = ROOTS[LANG], "north-tel-aviv", "https://nad-lan.co.il/north-tel-aviv/"
else:
    hub = child(ROOTS[LANG], "north-tel-aviv")
    if not hub or hub["status"] != "publish":
        raise SystemExit("FATAL: the language hub /%s/north-tel-aviv/ is not live yet (it is the parent page)" % LANG)
    parent, slug, he_url = hub["id"], "rova-4", "https://nad-lan.co.il/north-tel-aviv/rova-4/"
    if html.count("<!-- NLPG -->") != 1 or html.count("<!-- NLAM -->") != 1:
        raise SystemExit("FATAL: the Rova 4 article needs exactly one <!-- NLPG --> and one <!-- NLAM --> marker")
    html = html.replace("<!-- NLPG -->", '\n[nadlan_price_guide key="rova-4"]\n').replace("<!-- NLAM -->", '\n[nadlan_area_map key="rova-4"]\n')
# gate 2: the URL is free
ex = child(parent, slug)
if ex:
    raise SystemExit(f"FATAL: a page already sits at that path (id {ex['id']}, {ex['status']}): {ex['link']}")
print(f"[plan] /{LANG}/... slug {slug} under parent {parent}; H1 '{title[:70]}'; SEO title {len(seo_title.group(1).strip())} chars, description {len(seo_desc.group(1).strip())} chars; {len(html):,} chars")
if "--dry" in ARGS:
    raise SystemExit(0)
s, b, _ = req("POST", "/wp-json/wp/v2/pages", {"title": title, "slug": slug, "parent": parent, "status": "publish", "content": html,
                                               "meta": {"_yoast_wpseo_title": seo_title.group(1).strip(), "_yoast_wpseo_metadesc": seo_desc.group(1).strip()}})
if s not in (200, 201) or not isinstance(b, dict) or not b.get("id"):
    raise SystemExit(f"FATAL: create failed {s}")
pid, link = b["id"], b["link"]
print(f"[created] page {pid}: {link}")
io.open(os.path.join(WORK, "out", f"published-{which}-{LANG}.json"), "w", encoding="utf-8").write(json.dumps({"id": pid, "link": link, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}, ensure_ascii=False))
time.sleep(3)
st, live = page(link)
_, he = page(he_url)
body = live[live.find("<body"):]
checks = {
    "200": st == 200,
    "html lang": bool(re.search(r'<html[^>]*lang="%s' % LANG, live)),
    "one h1": body.count("<h1") == 1,
    "hreflang on the new page": ('hreflang="%s"' % LANG) in live and 'hreflang="he"' in live and 'hreflang="x-default"' in live,
    "hreflang back on the Hebrew page": (link in he) and ('hreflang="%s"' % LANG) in he,
    "no raw shortcode": "[nadlan_" not in body,
}
if which == "rova-4":
    checks["price list in the language"] = 'id="nlpg"' in body and ('lang="%s"' % LANG) in body[body.find('id="nlpg"') - 400:body.find('id="nlpg"') + 400]
    checks["map in the language"] = 'class="nlds nlam"' in body and ('lang="%s"' % LANG) in body[body.find('class="nlds nlam"'):body.find('class="nlds nlam"') + 600]
for k, v in checks.items():
    print(f"   {'OK ' if v else 'BAD'} {k}")
if not all(checks.values()):
    print("[draft] a check failed:", req("POST", f"/wp-json/wp/v2/pages/{pid}", {"status": "draft"})[0]); raise SystemExit(1)
print(f"[done] {link}")
