# -*- coding: utf-8 -*-
"""HAD-495 DealSign admin: create a broker's private office, or list every agreement and registration (the owner's ledger).
python sg_admin.py broker <name> <office> <licence> <phone> [<email>] [--token <32 hex to update>]
python sg_admin.py ledger
The office links are secrets of their owners: written to docs/sales/meital-kit-2026-10/private/ (git-ignored), never printed in full."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "sgadmin"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
PRIV = os.path.join(REPO, "docs", "sales", "meital-kit-2026-10", "private")
os.makedirs(PRIV, exist_ok=True)
a = sys.argv[1:]
if a[0] == "broker":
    body = {"name": a[1], "office": a[2], "lic": a[3], "phone": a[4], "email": a[5] if len(a) > 5 and not a[5].startswith("--") else ""}
    if "--token" in a:
        body["token"] = a[a.index("--token") + 1]
    s, b, _ = req("POST", "/wp-json/nadlan/v1/sg/broker", body)
    if s != 200 or not b.get("ok"):
        raise SystemExit(f"FATAL {s} {b}")
    f = os.path.join(PRIV, "office-" + b["token"][:6] + ".json")
    json.dump({"name": a[1], "office_url": b["office"], "token": b["token"]}, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("office created for", a[1], "->", b["office"][:48] + "...", "(full link in", f + ")")
else:
    s, b, _ = req("GET", "/wp-json/nadlan/v1/sg/admin")
    print(s, json.dumps(b, ensure_ascii=False, indent=1)[:6000])
