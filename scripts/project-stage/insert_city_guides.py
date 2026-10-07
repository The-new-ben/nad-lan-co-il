# -*- coding: utf-8 -*-
"""HAD-460: the city price list (PriceGuide, rooms variant) on the city price pages. Inserts [nadlan_price_guide key="<slug>"]
right after the page's first real paragraph (the first <p> after the H1 with at least 80 characters of text that is not the
"updated" line), never before it (Ben 7.10). Titles, H1s, descriptions and URLs are not touched (the CEO's terms, HAD-446).
Needs the plugin release that carries the city's data (pg_helper.CITIES). Backup before, read-back after, per page.
python insert_city_guides.py <slug> [<slug> ...] [--dry] [--project]      python insert_city_guides.py --rollback <backup.json>"""
import html
import io
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BK = os.path.join(REPO, "docs", "qa", "had-460", "city-backup")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
# --project: a project page (post type nadlan_project) with no stage block, e.g. H Infinity (the price list goes in its article)
BASE = "nadlan_project" if "--project" in sys.argv else "pages"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "cityguides"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]

if "--rollback" in sys.argv:
    bk = json.load(io.open(ARGS[0], encoding="utf-8"))
    s, r, _ = req("POST", f"/wp-json/wp/v2/{bk.get('base', 'pages')}/{bk['id']}", {"content": bk["content"]})
    print("[rollback]", bk["id"], s); raise SystemExit(0)

os.makedirs(BK, exist_ok=True)
for slug in ARGS:
    short = '[nadlan_price_guide key="%s"]' % slug
    s, lst, _ = req("GET", f"/wp-json/wp/v2/{BASE}?slug={slug}&_fields=id,link")
    if not (isinstance(lst, list) and len(lst) == 1):
        print(f"[skip] {slug}: {len(lst) if isinstance(lst, list) else lst} pages"); continue
    pid = lst[0]["id"]
    s, b, _ = req("GET", f"/wp-json/wp/v2/{BASE}/{pid}?context=edit&_fields=id,link,content,modified")
    raw = b["content"]["raw"]
    if short in raw:
        print(f"[skip] {slug}: already has the price list"); continue
    h1 = raw.find("<h1")
    start = raw.find("</h1>", h1) if h1 >= 0 else 0
    at = None
    for m in re.finditer(r"<p\b[^>]*>(.*?)</p>", raw[start:], re.S):
        text = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        if len(text) >= 80 and not text.startswith(("עודכן", "עדכון")):
            at = start + m.end(); break
    if at is None:
        print(f"[skip] {slug}: no opening paragraph found"); continue
    new = raw[:at] + "\n" + short + "\n" + raw[at:]
    print(f"[plan] {slug} (page {pid}): after the paragraph ending at {at}: ...{html.unescape(re.sub(r'<[^>]+>', '', raw[max(0, at - 160):at]))[-90:]}")
    if "--dry" in sys.argv:
        continue
    bkp = os.path.join(BK, f"page-{pid}-{time.strftime('%Y%m%dT%H%M%S')}.json")
    io.open(bkp, "w", encoding="utf-8").write(json.dumps({"base": BASE, "id": pid, "slug": slug, "content": raw, "modified": b["modified"]}, ensure_ascii=False))
    s, r, _ = req("POST", f"/wp-json/wp/v2/{BASE}/{pid}", {"content": new})
    s2, a, _ = req("GET", f"/wp-json/wp/v2/{BASE}/{pid}?context=edit&_fields=content")
    print(f"   written {s}, read-back identical: {a['content']['raw'] == new}; backup {os.path.relpath(bkp, REPO)}")
