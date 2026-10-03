# -*- coding: utf-8 -*-
"""HAD-396 data patch, REPORT ONLY (Maya's urban-data-report-conditions.md; urban commit 30262c76). Installs urban's
had396_data_patch.php (md5-pinned) as a temporary inactive snippet, activates it, POSTs {} (the report path, which writes
nothing), saves the full response under docs/qa/had-396/, then deactivates and deletes the snippet. Never sends "apply".
The app password is decrypted in-process (DPAPI) and never printed.   python scripts/project-stage/had396_report.py"""
import hashlib, json, os, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "had396_report_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
COMMIT, WANT = "30262c76", "74cd59dba9345c95125a6f4f169ff6d6"
code_b = subprocess.run(["git", "-C", REPO, "show", f"{COMMIT}:scripts/urban-renewal/had396_data_patch.php"], capture_output=True, check=True).stdout
if hashlib.md5(code_b).hexdigest() != WANT:
    raise SystemExit("FATAL: the script at " + COMMIT + " is not " + WANT[:10])
code = code_b.decode("utf-8")
if not code.startswith("<?php"):
    raise SystemExit("FATAL: the script does not start with <?php")
code = code.split("\n", 1)[1]  # Code Snippets stores the body without the opening tag
s, c = snip("POST", "", {"name": f"tmp-had396-report-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "snippet create")
sid = c["id"]
try:
    s, u = snip("PUT", f"/{sid}", {"name": c["name"], "code": code, "scope": "global", "active": False}); must(s, u, "snippet update")
    s, a = snip("PUT", f"/{sid}/activate", {}); must(s, a, "snippet activate")
    s, r, _ = req("POST", "/wp-json/nadlanfix/v1/had396-data", {}, timeout=120); must(s, r, "report")
finally:
    s1, _ = snip("PUT", f"/{sid}/deactivate", {}); s2, _ = snip("DELETE", f"/{sid}", None)
    print("[snippet] cleanup", s1, s2)
    s3, _, _ = req("POST", "/wp-json/nadlanfix/v1/had396-data", {}, timeout=60)
    print("[route] after cleanup http", s3, "(want 404)")
stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
out = os.path.join(REPO, "docs", "qa", "had-396", f"data-report-live-{stamp}.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "w", encoding="utf-8").write(json.dumps(r, ensure_ascii=False, indent=1))
print("[report] mode:", r.get("mode"), "| ok:", r.get("ok"), "| errors:", r.get("errors"), "| apply:", r.get("apply"))
print("[report] before_md5:", r.get("before_md5"), "| planned writes:", len(r.get("planned_writes") or []))
print("[report] saved", os.path.relpath(out, REPO), hashlib.md5(open(out, "rb").read()).hexdigest()[:10])
