# -*- coding: utf-8 -*-
"""Read-only: save the code of one Code Snippets snippet (GET /code-snippets/v1/snippets/<id>) under docs/qa/live-read/<stamp>/.
No bridge, no write. The app password is decrypted in-process (DPAPI) and never printed.

  python scripts/project-stage/snippet_read.py 661"""
import hashlib, io, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "snippet_read_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
snip, must = _ns["snip"], _ns["must"]
sid = sys.argv[1]
s, c = snip("GET", f"/{sid}", None); must(s, c, "snippet read")
code = (c.get("code") or "").encode("utf-8")
stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
out = os.path.join(REPO, "docs", "qa", "live-read", stamp); os.makedirs(out, exist_ok=True)
p = os.path.join(out, f"snippet-{sid}.php"); open(p, "wb").write(code)
print(f"[snippet] {sid} '{c.get('name')}' active={c.get('active')} scope={c.get('scope')} {len(code)} B md5 {hashlib.md5(code).hexdigest()[:10]} -> {os.path.relpath(p, REPO)}")
