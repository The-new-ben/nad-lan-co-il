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

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "upkit"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
OFFICE = json.load(open(os.path.join(HERE, "private", "office-6b3536.json"), encoding="utf-8"))["token"]
G1, G2, G3, G4, G5 = "להתחלה", "מול היזם: הסכם ורישום", "מול הלקוח", "שלב 2: אולם התצוגה באתר", "בינך לבין nad-lan.co.il"
KIT = [
    ("guide.pdf", "שיתוף פעולה עם יזמים: איך עובדים", G1, 10, "שני השלבים, שיחת הפתיחה, השאלות ליזם, שכר התיווך בשוק, איך משתמשים במשרד הזה ומה לא אומרים. לקרוא ראשון."),
    ("agreement-template.pdf", "הסכם שיתוף פעולה והזמנת שירותי תיווך · נוסח כללי", G2, 20, "ההסכם מול כל יזם, עם טופס רישום לקוח. ממלאים חברה, פרויקט ושיעור שכר. אותו נוסח נחתם דיגיטלית בלשונית \"הסכמים\"."),
    ("agreement-ashira.pdf", "הסכם שיתוף פעולה · אשירה שדה דב (אביסרור משה ובניו)", G2, 21, "הנוסח עם פרטי הפרויקט, לעיון החברה או עורך הדין שלה לפני חתימה."),
    ("agreement-rainbow.pdf", "הסכם שיתוף פעולה · ריינבו תל אביב (ישראל קנדה)", G2, 22, "הנוסח עם פרטי הפרויקט, לעיון החברה או עורך הדין שלה לפני חתימה."),
    ("client-order.pdf", "הזמנת שירותי תיווך ללקוח", G3, 30, "הלקוח חותם לפני שמציגים אותו לחברה. כולל גילוי שהחברה משלמת לך והסכמה למסירת פרטים. הלקוח לא משלם."),
    ("deck-ashira.pdf", "מצגת · אשירה שדה דב", G4, 40, "12 עמודים: אולם התצוגה, חמש שפות, הליווי עד החתימה, התנאים ורישום הלקוח. אחרי שיש שיתוף פעולה."),
    ("film-ashira.mp4", "סרטון · אשירה שדה דב, 50 שניות", G4, 41, "בלי קול, לשליחה בוואטסאפ יחד עם המצגת."),
    ("terms-ashira.pdf", "עיקרי התנאים · אשירה שדה דב", G4, 42, "עיקרי השיתוף, ההסכם, הזמנת הפרסום באתר וטופס הרישום, במסמך אחד."),
    ("deck-rainbow.pdf", "מצגת · ריינבו תל אביב", G4, 43, "12 עמודים: אולם התצוגה, חמש שפות, הליווי עד החתימה, התנאים ורישום הלקוח. אחרי שיש שיתוף פעולה."),
    ("film-rainbow.mp4", "סרטון · ריינבו תל אביב, 50 שניות", G4, 44, "בלי קול, לשליחה בוואטסאפ יחד עם המצגת."),
    ("terms-rainbow.pdf", "עיקרי התנאים · ריינבו תל אביב", G4, 45, "עיקרי השיתוף, ההסכם, הזמנת הפרסום באתר וטופס הרישום, במסמך אחד."),
    ("meital-letter.pdf", "מכתב שיתוף פעולה עם nad-lan.co.il", G5, 60, "התנאים בינך לבין האתר: החלק שלך מתשלומי הפרסום של חברות שהבאת. לחתימה."),
]
links = {}
for name, title, group, order, desc in KIT:
    raw = open(os.path.join(HERE, name), "rb").read()
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
json.dump(links, open(os.path.join(HERE, "private", "kit-links.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done:", len(links), "files")
