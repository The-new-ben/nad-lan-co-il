# -*- coding: utf-8 -*-
"""Ben 15.11.2026: "פייל מנג'ר, תחבא אותו" - deactivate the File Manager Advanced plugin (its Adminer screen throws a fatal error
because templates/adminer.php is missing). Deactivate only: files and settings stay, one click in Plugins turns it back on.
python scripts/project-stage/fma_off.py [--check]"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "fmaoff"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
P = "/wp-json/wp/v2/plugins/file-manager-advanced/file_manager_advanced"
s, b, _ = req("GET", P)
print("before:", s, b.get("status") if isinstance(b, dict) else b, b.get("version") if isinstance(b, dict) else "")
if "--check" in sys.argv or not isinstance(b, dict) or b.get("status") != "active":
    sys.exit(0)
s, b, _ = req("POST", P, {"status": "inactive"})
print("deactivate:", s, b.get("status") if isinstance(b, dict) else b)
s, b, _ = req("GET", P)
print("after:", s, b.get("status") if isinstance(b, dict) else b)
s, h, _ = req("GET", "/wp-json/nadlan/v1/health")
print("health:", s, (h or {}).get("version") if isinstance(h, dict) else h)
