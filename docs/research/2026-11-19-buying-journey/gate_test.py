# -*- coding: utf-8 -*-
"""Package 4 (HAD-796): the lawyer gate on the LIVE site. usage: gate_test.py <token>
Creates a test lawyer user (role nadlan_lawyer) with an application password held only in memory, proves: anonymous deposit refused
(409), administrator approve refused (403), lawyer without the tick refused (400), lawyer with the tick approves (200). Prints the
lawyer user id for the clean-up step. No personal data; the password is never printed or written."""
import os, sys, json, base64, secrets, urllib.request, urllib.error
sys.path.insert(0, r"C:\Users\777\AppData\Local\Temp\claude\231dc6a3026aa599\61826a5c-4e31-47cc-8b2a-ac3ac94180f1\scratchpad")
from restlib_p4 import req, SITE  # noqa: E402
sys.stdout.reconfigure(encoding="utf-8")
tok = sys.argv[1]
O = "/wp-json/nadlan/v1/cart/order/" + tok
out = {}
def anon(method, path, body=None, auth=None):
    r = urllib.request.Request(SITE + path, data=json.dumps(body).encode() if body is not None else None, method=method, headers={"Content-Type": "application/json", "User-Agent": "NadLanPackage4Test/1.0"})
    if auth: r.add_header("Authorization", "Basic " + base64.b64encode(auth.encode()).decode())
    try:
        with urllib.request.urlopen(r, timeout=60) as f: return f.status, json.loads(f.read().decode())
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read().decode())
        except Exception: return e.code, None
s, j = anon("GET", O); out["state_before"] = (s, j and j.get("status"))
s, j = anon("POST", O + "/deposit", {"simulate": True}); out["anon_deposit"] = (s, j and (j.get("code") or j.get("status")))
s, j = req("POST", O + "/approve", body={"confirm": True, "licence": "00000"}); out["admin_approve"] = (s, isinstance(j, dict) and (j.get("code") or j.get("status")))
name = "nl-lawyer-test-" + secrets.token_hex(3)
s, u = req("POST", "/wp-json/wp/v2/users", body={"username": name, "email": name + "@example.invalid", "password": secrets.token_urlsafe(24), "roles": ["nadlan_lawyer"], "name": "עו״ד בדיקה (חבילה 4)"})
assert s in (200, 201), (s, str(u)[:300])
uid = u["id"]; out["lawyer_user"] = uid
s, ap = req("POST", "/wp-json/wp/v2/users/%d/application-passwords" % uid, body={"name": "package4-test"})
assert s in (200, 201), (s, str(ap)[:200])
cred = name + ":" + ap["password"]
s, j = anon("POST", O + "/approve", {"licence": "00000"}, auth=cred); out["lawyer_no_tick"] = (s, j and j.get("code"))
s, j = anon("POST", O + "/approve", {"confirm": True, "licence": "00000", "note": "בדיקת מערכת: אושר לצורך הדגמה בלבד"}, auth=cred); out["lawyer_approve"] = (s, j and j.get("status"))
s, j = anon("GET", O); out["state_after"] = (s, j and j.get("status"), j and j.get("lawyer") and j["lawyer"].get("name"))
print(json.dumps(out, ensure_ascii=False))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "live", "gate-%s.json" % tok[:6]), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
