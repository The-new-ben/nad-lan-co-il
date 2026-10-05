# -*- coding: utf-8 -*-
"""Read-only: back up page 5154 (/en/buy-property-in-israel/) exactly as stored (context=edit) before HAD-429 replaces its body.
Uses the app password in-process (never printed). Writes docs/qa/page-5154/backup-<UTC>.json."""
import json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "upload_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req = _ns["req"]
s, page, _ = req("GET", "/wp-json/wp/v2/pages/5154?context=edit")
if s != 200 or not isinstance(page, dict):
    raise SystemExit(f"FATAL read: {s}")
keep = {k: page.get(k) for k in ("id", "slug", "status", "parent", "template", "modified", "link", "title", "excerpt", "content", "meta")}
out = os.path.join(REPO, "docs", "qa", "page-5154", "backup-%s.json" % time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()))
open(out, "w", encoding="utf-8").write(json.dumps(keep, ensure_ascii=False, indent=1))
raw = (page.get("content") or {}).get("raw", "")
print("saved", out)
print("raw bytes", len(raw), "| blocks", raw.count("<!-- wp:"), "| h1 in raw", raw.count("<h1"), "| template", page.get("template"))
print("meta keys", sorted((page.get("meta") or {}).keys())[:40])
print("raw head:", raw[:700].replace("\n", " "))
