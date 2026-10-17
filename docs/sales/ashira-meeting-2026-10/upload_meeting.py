# -*- coding: utf-8 -*-
"""HAD-495: put Meital's working files into the materials tab of her office (admin REST /nadlan/v1/sg/file, 1.72.444).
Each file is verified after upload (its own link answers 200 with the same MD5). The links go to private/kit-links.json.
python upload_kit.py"""
import base64
import hashlib
import json
import os
import time
import urllib.request

MEET = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.join(os.path.dirname(MEET), "meital-kit-2026-10")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(MEET)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "upkit"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
OFFICE = json.load(open(os.path.join(HERE, "private", "office-6b3536.json"), encoding="utf-8"))["token"]
G = "פגישת אשירה · יום שני 19.10"
KIT = [
    ("concept.pdf", "הקונספט העסקי · גרסה 3, 17.10 לילה", G, 69, "גרסה 3 מחליפה את הקודמות: מה עובד היום מול פיילוט, ניתוב פניות לא הוחלט, תנאי הרישום טעונים הסכם ובדיקת עו״ד, אין שיוך קונה למיטל לפי אזור."),
    ("meeting-deck.pdf", "מצגת הפגישה · גרסה 3, 17.10 לילה", G, 70, "גרסה 3 מחליפה את הקודמות. בלי הבטחות שלא קיימות היום."),
    ("playbook.pdf", "ספר המכירה · גרסה 3, 17.10 לילה", G, 71, "גרסה 3 מחליפה את הקודמות."),
    ("business.pdf", "הקרקע העסקית · גרסה 3, 17.10 לילה", G, 72, "גרסה 3 מחליפה את הקודמות. פנימי."),
]
links = {}
for name, title, group, order, desc in KIT:
    raw = open(os.path.join(MEET, name), "rb").read()
    s, b, _ = req("POST", "/wp-json/nadlan/v1/sg/file", {"office": OFFICE, "name": name, "title": title, "group": group, "order": order, "desc": desc,
                                                        "b64": base64.b64encode(raw).decode()})
    if s != 200 or not b.get("ok"):
        raise SystemExit(f"FATAL {name}: {s} {str(b)[:200]}")
    got = urllib.request.urlopen(urllib.request.Request(b["url"] + "&nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=120).read()
    ok = hashlib.md5(got).hexdigest() == hashlib.md5(raw).hexdigest()
    print(("OK " if ok else "BAD"), name, len(raw), "bytes")
    if not ok:
        raise SystemExit("FATAL: the served file differs")
    links[name] = {"title": title, "group": group, "desc": desc, "url": b["url"]}
json.dump(links, open(os.path.join(HERE, "private", "meeting-links.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done:", len(links), "files")
