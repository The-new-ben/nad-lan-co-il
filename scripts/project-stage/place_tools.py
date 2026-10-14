# -*- coding: utf-8 -*-
"""HAD-527: place an Instruments tool on an EXISTING page (no new URL, no cannibalisation): the shortcode goes right after
the page's first paragraph (the content-first law: H1, the answer paragraph, then the tool). Backup before, read-back after,
the live page checked for the instrument host and the tool script.  python place_tools.py <page id>=<tool id> ... [--dry]"""
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BK = os.path.join(REPO, "docs", "qa", "had-527", "page-backup")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "placetools"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
os.makedirs(BK, exist_ok=True)
for arg in [a for a in sys.argv[1:] if "=" in a]:
    pid, tool = arg.split("=")
    s, b, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=content,link,modified")
    raw = b["content"]["raw"]
    sc = f'[nadlan_tool id="{tool}"]'
    if sc in raw:
        print(pid, "already has", sc); continue
    m = re.search(r"</p>", raw)
    if not m:
        raise SystemExit(f"FATAL {pid}: no first paragraph")
    new = raw[:m.end()] + "\n\n<!-- wp:shortcode -->\n" + sc + "\n<!-- /wp:shortcode -->\n\n" + raw[m.end():]
    print(f"[{pid}] {b['link']}: {sc} after the first paragraph ({m.end()} chars in)")
    if "--dry" in sys.argv:
        continue
    io.open(os.path.join(BK, f"page-{pid}-{time.strftime('%Y%m%dT%H%M%S')}.json"), "w", encoding="utf-8").write(json.dumps({"id": pid, "content": raw, "modified": b["modified"]}, ensure_ascii=False))
    s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": new})
    ok = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=content")[1]["content"]["raw"] == new
    time.sleep(2)
    html = urllib.request.urlopen(urllib.request.Request(b["link"] + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    body = html[html.find("<body"):]
    checks = {"read-back": ok, "host": f'data-nli="{tool}"' in body, "script": f"instruments/tools/{tool}.js" in html, "json-ld": 'id="nadlan-nli-ld"' in html,
              "no raw shortcode": "[nadlan_tool" not in body, "one h1": body.count("<h1") == 1}
    print("   ", "  ".join(("OK " if v else "BAD ") + k for k, v in checks.items()))
