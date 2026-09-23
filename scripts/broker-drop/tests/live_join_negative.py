# -*- coding: utf-8 -*-
"""Safe tests of the public join door: nothing here creates a broker."""
import json, sys, time, urllib.request, urllib.error, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")
API = "https://nad-lan.co.il/wp-json/nadlan/v1/brokers"
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128 Safari/537.36", "Content-Type": "application/json"}
def post(path, body):
    r = urllib.request.Request(API + path, data=json.dumps(body, ensure_ascii=False).encode(), headers=H, method="POST")
    try:
        with urllib.request.urlopen(r, timeout=90) as x:
            return x.status, json.loads(x.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")
# a real licence from the public register, used only with a WRONG name (nothing is created)
q = urllib.parse.urlencode({"resource_id": "a0f56034-88db-4132-8803-854bcdb01ca1", "limit": 1, "offset": 5000})
rec = json.loads(urllib.request.urlopen(urllib.request.Request("https://data.gov.il/api/3/action/datastore_search?" + q, headers={"User-Agent": H["User-Agent"]}), timeout=60).read().decode())["result"]["records"][0]
other_lic = str(rec["מס רשיון"])
base = {"lang": "he", "licence": "", "name_he": "בדיקת מערכת", "name_en": "System Check", "brand": "", "phone": "052-0000000", "email": "check@example.com",
        "areas": "נווה צדק, יפו", "bio": "", "gender": "m", "decl": "1", "agree": "1", "website": ""}
tests = [
    ("honeypot", dict(base, licence="12345", website="http://spam")),
    ("missing areas", dict(base, licence="12345", areas="")),
    ("bad phone", dict(base, licence="12345", phone="03-1234567")),
    ("english name in Hebrew", dict(base, licence="12345", name_en="בדיקה")),
    ("no declaration", dict(base, licence="12345", decl="")),
    ("licence not in register", dict(base, licence="99999999")),
    ("real licence, wrong name", dict(base, licence=other_lic)),
    ("Meital's licence (already has a site)", dict(base, licence="3131540", name_he="מיטל קציר")),
]
for name, body in tests:
    s, j = post("/join", body)
    print(f"{name:40s} {s} {j.get('code', '')} | {j.get('message', j)}")
s, j = post("/relink", {"licence": "3131540", "email": "someone@example.com", "lang": "he"})
print(f"{'relink, wrong email':40s} {s} | {j.get('message')}")
