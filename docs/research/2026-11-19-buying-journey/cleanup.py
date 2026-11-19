# -*- coding: utf-8 -*-
"""Package 4: remove the test orders (and their leads) by reference, the test lawyer users, and put the gate back on. usage: cleanup.py REF[,REF] [UID,UID]"""
import sys, json
sys.path.insert(0, r"C:\Users\777\AppData\Local\Temp\claude\231dc6a3026aa599\61826a5c-4e31-47cc-8b2a-ac3ac94180f1\scratchpad")
from restlib_p4 import req  # noqa: E402
sys.stdout.reconfigure(encoding="utf-8")
refs = [r for r in sys.argv[1].split(",") if r]
uids = [int(u) for u in (sys.argv[2].split(",") if len(sys.argv) > 2 and sys.argv[2] else [])]
print("purge", req("POST", "/wp-json/nadlan/v1/cart/admin/purge", body={"refs": refs}))
s, me = req("GET", "/wp-json/wp/v2/users/me?context=edit&_fields=id")
for u in uids:
    s, r = req("GET", "/wp-json/wp/v2/users/%d?context=edit&_fields=id,roles,username" % u)
    assert s == 200 and r.get("roles") == ["nadlan_lawyer"] and str(r.get("username", "")).startswith("nl-lawyer-test-"), (s, r)
    print("delete user", u, req("DELETE", "/wp-json/wp/v2/users/%d?force=true&reassign=%d" % (u, me["id"]))[0])
print("gate on", req("POST", "/wp-json/wp/v2/settings", body={"nadlan_cart_gate": "1"}))
