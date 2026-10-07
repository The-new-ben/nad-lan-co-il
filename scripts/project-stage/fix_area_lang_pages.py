# -*- coding: utf-8 -*-
"""HAD-439/HAD-460 close-out of the area language pages (8.10.2026):
1. a name: the Hebrew Sde Dov hub says נופי ים (Nofei Yam); the en/fr/ar hubs wrote "Neve Yam" / "نافيه يام" (from the packet's
   name list); Russian already wrote Нофей-Ям;
2. links: every link from a language page to a HEBREW page that now has a same-language page (the New North hub, Rova 4, the
   Sde Dov hub, the Sde Dov prices page) points to the same-language page and loses its "(in Hebrew)" marker.
Backup before, read-back after, every target checked 200 first.   python fix_area_lang_pages.py [--dry]"""
import glob
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BK = os.path.join(REPO, "docs", "qa", "had-460", "lang-pages-backup")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "fixarea"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
S = "https://nad-lan.co.il"
MARK = {"en": " (in Hebrew)", "fr": " (en hébreu)", "ru": " (на иврите)", "ar": " (بالعبرية)"}
PATHS = ["/north-tel-aviv/rova-4/", "/north-tel-aviv/", "/sde-dov/prices/", "/sde-dov/"]
NAME = {"en": ("Neve Yam", "Nofei Yam"), "fr": ("Neve Yam", "Nofei Yam"), "ar": ("نافيه يام", "نوفي يام")}
pubs = []
for f in glob.glob(os.path.join(REPO, "docs", "content", "*", "out", "published-*-*.json")):
    lang = os.path.basename(f)[:-5].rsplit("-", 1)[1]
    pubs.append((lang, json.load(io.open(f, encoding="utf-8"))))
alive = {}
for lang in MARK:
    for p in PATHS:
        u = S + "/" + lang + p
        try:
            alive[(lang, p)] = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).status == 200
        except Exception:
            alive[(lang, p)] = False
os.makedirs(BK, exist_ok=True)
tot = 0
for lang, pub in sorted(pubs, key=lambda x: (x[0], x[1]["id"])):
    pid = pub["id"]
    s, b, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=content,modified,link")
    raw = b["content"]["raw"]
    new, notes = raw, []
    for p in PATHS:
        if not alive[(lang, p)]:
            continue
        pat = re.compile(r'(<a [^>]*href=")' + re.escape(S + p) + r'("[^>]*>[^<]*</a>)' + re.escape(MARK[lang]))
        n = len(pat.findall(new))
        if n:
            new = pat.sub(lambda m: m.group(1) + S + "/" + lang + p + m.group(2), new); notes.append(f"{p} x{n}")
    if lang in NAME and "/sde-dov/" in b["link"]:
        a, z = NAME[lang]
        n = new.count(a)
        if n:
            new = new.replace(a, z); notes.append(f"name x{n}")
    print(f"[{lang}] page {pid} {b['link']}: {', '.join(notes) or 'nothing to change'}")
    if new == raw or "--dry" in sys.argv:
        continue
    io.open(os.path.join(BK, f"page-{pid}-{time.strftime('%Y%m%dT%H%M%S')}.json"), "w", encoding="utf-8").write(json.dumps({"id": pid, "content": raw, "modified": b["modified"]}, ensure_ascii=False))
    s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": new})
    ok = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=content")[1]["content"]["raw"] == new
    print(f"   written {s}, read-back identical {ok}")
    tot += 1
print("[done] pages changed:", tot)
