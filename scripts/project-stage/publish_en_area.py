# -*- coding: utf-8 -*-
"""HAD-460 / HAD-439: publish a language version of an area page in the site's EXISTING page-language pattern (the CEO's decision
B, corrected 7.10.2026): /<lang>/<path>/ as a child of the language root page (inc/page-lang.php gives lang/dir, the hreflang
cluster and x-default to Hebrew automatically). Gates (the CEO's quality terms): check_translation.py PASSES on the article and
its meta; the URL is free; after publishing the live page must answer 200 with <html lang> = the language, exactly one H1, the
hreflang cluster on BOTH the language page and its Hebrew source, and the page's components (price list / map) in that language.
Any failed check moves the new page to draft (never deleted).
Pages: hub, rova-4 (docs/content/north-tel-aviv-2026-10), sde-dov-hub, sde-dov-prices (docs/content/sde-dov-i18n-2026-10).
python publish_en_area.py <page> [--lang en] [--dry]      python publish_en_area.py --draft <page id>"""
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
ARGS = sys.argv[1:]
LANG = ARGS[ARGS.index("--lang") + 1] if "--lang" in ARGS else "en"
ROOTS = {"en": 5011, "fr": 5055, "ru": 5056, "ar": 5057}
S = "https://nad-lan.co.il"
PAGES = {
    "hub": {"work": "north-tel-aviv-2026-10", "under": None, "slug": "north-tel-aviv", "he": S + "/north-tel-aviv/", "markers": {}},
    "rova-4": {"work": "north-tel-aviv-2026-10", "under": "north-tel-aviv", "slug": "rova-4", "he": S + "/north-tel-aviv/rova-4/",
               "markers": {"<!-- NLPG -->": '[nadlan_price_guide key="rova-4"]', "<!-- NLAM -->": '[nadlan_area_map key="rova-4"]'}},
    "sde-dov-hub": {"work": "sde-dov-i18n-2026-10", "under": None, "slug": "sde-dov", "he": S + "/sde-dov/",
                    "markers": {"<!-- NLAM -->": '[nadlan_area_map key="sde-dov"]'}},
    "sde-dov-prices": {"work": "sde-dov-i18n-2026-10", "under": "sde-dov", "slug": "prices", "he": S + "/sde-dov/prices/",
                       "markers": {"<!-- NLPG -->": '[nadlan_price_guide key="sde-dov-prices"]'}},
}
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
P = PAGES[which]
WORK = os.path.join(REPO, "docs", "content", P["work"])
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
parent = ROOTS[LANG]
if P["under"]:
    up = child(ROOTS[LANG], P["under"])
    if not up or up["status"] != "publish":
        raise SystemExit("FATAL: the language parent /%s/%s/ is not live yet" % (LANG, P["under"]))
    parent = up["id"]
for mk, sc in P["markers"].items():
    if html.count(mk) != 1:
        raise SystemExit(f"FATAL: the article needs exactly one {mk} marker")
    html = html.replace(mk, "\n" + sc + "\n")
# gate 2: the URL is free
ex = child(parent, P["slug"])
if ex:
    raise SystemExit(f"FATAL: a page already sits at that path (id {ex['id']}, {ex['status']}): {ex['link']}")
print(f"[plan] /{LANG}/... slug {P['slug']} under parent {parent}; H1 '{title[:70]}'; SEO title {len(seo_title.group(1).strip())} chars, description {len(seo_desc.group(1).strip())} chars; {len(html):,} chars")
if "--dry" in ARGS:
    raise SystemExit(0)
s, b, _ = req("POST", "/wp-json/wp/v2/pages", {"title": title, "slug": P["slug"], "parent": parent, "status": "publish", "content": html,
                                               "meta": {"_yoast_wpseo_title": seo_title.group(1).strip(), "_yoast_wpseo_metadesc": seo_desc.group(1).strip()}})
if s not in (200, 201) or not isinstance(b, dict) or not b.get("id"):
    raise SystemExit(f"FATAL: create failed {s}")
pid, link = b["id"], b["link"]
print(f"[created] page {pid}: {link}")
io.open(os.path.join(WORK, "out", f"published-{which}-{LANG}.json"), "w", encoding="utf-8").write(json.dumps({"id": pid, "link": link, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}, ensure_ascii=False))
time.sleep(3)
st, live = page(link)
_, he = page(P["he"])
body = live[live.find("<body"):]
checks = {
    "200": st == 200,
    "html lang": bool(re.search(r'<html[^>]*lang="%s' % LANG, live)),
    "one h1": body.count("<h1") == 1,
    "hreflang on the new page": ('hreflang="%s"' % LANG) in live and 'hreflang="he"' in live and 'hreflang="x-default"' in live,
    "hreflang back on the Hebrew page": (link in he) and ('hreflang="%s"' % LANG) in he,
    "no raw shortcode": "[nadlan_" not in body,
}
if "<!-- NLPG -->" in P["markers"]:
    i = body.find('id="nlpg"')
    checks["price list in the language"] = i > 0 and ('lang="%s"' % LANG) in body[max(0, i - 400):i + 400]
if "<!-- NLAM -->" in P["markers"]:
    i = body.find('class="nlds nlam"')
    checks["map in the language"] = i > 0 and ('lang="%s"' % LANG) in body[i:i + 600]
for k, v in checks.items():
    print(f"   {'OK ' if v else 'BAD'} {k}")
if not all(checks.values()):
    print("[draft] a check failed:", req("POST", f"/wp-json/wp/v2/pages/{pid}", {"status": "draft"})[0]); raise SystemExit(1)
print(f"[done] {link}")
