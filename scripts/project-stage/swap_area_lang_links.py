# -*- coding: utf-8 -*-
"""HAD-460: once /<lang>/north-tel-aviv/ and /<lang>/north-tel-aviv/rova-4/ are both live, their links to each other's HEBREW page
(written with a "(in Hebrew)" marker because the language page did not exist yet) point to the same-language page and lose the
marker (docs/content/north-tel-aviv-2026-10/links.json "swap_after_publish"). Backup before, read-back after, the link checked 200.
python swap_area_lang_links.py [--dry]"""
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(REPO, "docs", "content", "north-tel-aviv-2026-10", "out")
BK = os.path.join(REPO, "docs", "qa", "had-460", "lang-pages-backup")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "swaplinks"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
MARK = {"en": " (in Hebrew)", "fr": " (en hébreu)", "ru": " (на иврите)", "ar": " (بالعبرية)"}
HE = {"hub": "https://nad-lan.co.il/north-tel-aviv/rova-4/", "rova-4": "https://nad-lan.co.il/north-tel-aviv/"}
TO = {"hub": "https://nad-lan.co.il/{l}/north-tel-aviv/rova-4/", "rova-4": "https://nad-lan.co.il/{l}/north-tel-aviv/"}
os.makedirs(BK, exist_ok=True)
for lang in ("en", "fr", "ru", "ar"):
    for pg in ("hub", "rova-4"):
        pub = json.load(io.open(os.path.join(OUT, f"published-{pg}-{lang}.json"), encoding="utf-8"))
        pid, target = pub["id"], TO[pg].format(l=lang)
        st = urllib.request.urlopen(urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).status
        s, b, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=content,modified")
        raw = b["content"]["raw"]
        pat = re.compile(r'(<a [^>]*href=")' + re.escape(HE[pg]) + r'("[^>]*>[^<]*</a>)' + re.escape(MARK[lang]))
        n = len(pat.findall(raw))
        new = pat.sub(lambda m: m.group(1) + target + m.group(2), raw)
        print(f"[{lang} {pg}] page {pid}: {n} link(s) -> {target} ({st})")
        if not n or st != 200 or "--dry" in sys.argv:
            continue
        io.open(os.path.join(BK, f"page-{pid}-{time.strftime('%Y%m%dT%H%M%S')}.json"), "w", encoding="utf-8").write(json.dumps({"id": pid, "content": raw, "modified": b["modified"]}, ensure_ascii=False))
        s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": new})
        ok = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=content")[1]["content"]["raw"] == new
        print(f"   written {s}, read-back identical {ok}")
