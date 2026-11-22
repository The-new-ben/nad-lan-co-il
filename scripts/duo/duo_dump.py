# -*- coding: utf-8 -*-
"""Read-only: the raw content of the five DUO posts (he 4893, en 5194, fr 5195, ru 5196, ar 5197) into
docs/research/2026-11-22-duo-audit/raw/<id>.html with md5 and modified date. Writes nothing on the site."""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "duodump"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
OUT = os.path.join(REPO, "docs", "research", "2026-11-22-duo-audit", "raw"); os.makedirs(OUT, exist_ok=True)
info = {}
for pid in (4893, 5194, 5195, 5196, 5197):
    s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content,title" % pid)
    assert s == 200, (pid, s)
    raw = g["content"]["raw"]
    open(os.path.join(OUT, "%d.html" % pid), "w", encoding="utf-8", newline="").write(raw)
    info[pid] = {"slug": g["slug"], "modified": g["modified"], "md5": hashlib.md5(raw.encode("utf-8")).hexdigest(), "chars": len(raw), "title": g["title"]["raw"]}
    print(pid, info[pid]["slug"], info[pid]["modified"], info[pid]["md5"][:10], len(raw))
    time.sleep(1.5)
json.dump(info, open(os.path.join(OUT, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
