# -*- coding: utf-8 -*-
"""HAD-543: pull the raw CMS content of the five Ashira posts (backup + work copy). Read-only."""
import os, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "pull"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
for lang, pid in (("he", 4744), ("en", 4927), ("fr", 4926), ("ru", 4924), ("ar", 4925)):
    s, d, _ = req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit")
    raw = d["content"]["raw"]
    open(os.path.join(HERE, f"before-{lang}-{pid}.html"), "w", encoding="utf-8").write(raw)
    print(lang, pid, s, len(raw), "modified", d.get("modified"))
