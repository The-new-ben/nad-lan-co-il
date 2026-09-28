# -*- coding: utf-8 -*-
"""Dimri Yama's page without "קו ראשון לחוף" (28.9.2026; design system StageSdeDov v82). The research of 28.9
(docs/research/2026-09-28-stages/stage-geometry.md, section 1; OpenStreetMap's coastline) puts lot 107 about 0.7 km from
the water (680 m from the lot's centre, 650 m from the tower's); the first line of the Sde Dov quarter lies further west.
Eight places in the page's text said "first line"; each becomes the measured distance. Same mechanism as
rainbow_content4.py: raw content over REST (the app password decrypted in-process, never printed), each fix must match
exactly once, guarded by the md5 of the content read just before; the old raw content is saved first.
  python scripts/project-stage/dimri_first_line.py            # show
  python scripts/project-stage/dimri_first_line.py --apply    # write"""
import io, os, sys, hashlib, time
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = io.open(os.path.join(REPO, "scripts", "project-stage", "rainbow_content4.py"), encoding="utf-8").read()
exec(compile(src[src.index("import base64, ctypes"):src.index("FIXES = [")].replace("PID = 4464", "PID = 4745")
             .replace('QA = os.path.join(REPO, "docs", "qa", "rainbow-content-2026-09-24")', 'QA = os.path.join(REPO, "docs", "qa", "dimri-content-2026-09-28")'), "head", "exec"))
FIXES = [
    ("הן בגלל המיקום בקו ראשון לחוף הים והן בגלל מבנה העסקה",
     "הן בגלל המיקום, כ-700 מטר מקו המים בין החוף לפארק הירקון, והן בגלל מבנה העסקה"),
    ('<td dir="rtl">קו ראשון לחוף ובקרבת פארק הירקון</td>',
     '<td dir="rtl">כ-700 מטר מקו המים, בקרבת פארק הירקון</td>'),
    ('<h2 dir="rtl">מיקום: קו ראשון לחוף, מתחם אשכול ואבן גבירול 220</h2>',
     '<h2 dir="rtl">מיקום: מתחם אשכול ואבן גבירול 220, כ-700 מטר מהים</h2>'),
    ('קו ראשון לחוף אינו רק ביטוי שיווקי. במונחי נדל"ן, קרבה ישירה לים משפיעה על תפיסת היוקרה,',
     'הקרבה לים אינה רק ביטוי שיווקי. במונחי נדל"ן, מרחק של כ-700 מטר מקו המים, בין החוף לפארק הירקון, משפיע על תפיסת היוקרה,'),
    ("או רק מהשתייכות כללית לפרויקט בקו ראשון.",
     "או רק מהשתייכות כללית לפרויקט קרוב לים."),
    ("ובמיוחד בקו ראשון לחוף, התמהיל",
     "ובמיוחד בפרויקט קרוב לים, התמהיל"),
    ('<td dir="rtl">קו ראשון לחוף, מתחם אשכול</td>',
     '<td dir="rtl">מתחם אשכול, כ-700 מטר מהים</td>'),
    ("בקו ראשון לחוף הים של תל אביב, בין החוף לפארק הירקון.",
     "כ-700 מטר מקו המים של תל אביב, בין החוף לפארק הירקון."),
]
d = read()
raw = d["content"]["raw"]
md5 = hashlib.md5(raw.encode("utf-8")).hexdigest()
new, bad = raw, []
for a, b in FIXES:
    n = new.count(a)
    print("[fix] x%d  %s..." % (n, a[:50]))
    if n != 1:
        bad.append(a[:50]); continue
    new = new.replace(a, b)
print("[check] 'קו ראשון' left:", new.count("קו ראשון"))
if "--apply" not in sys.argv:
    raise SystemExit(0)
if bad or new.count("קו ראשון"):
    raise SystemExit("FATAL: %s; nothing written" % bad)
os.makedirs(QA, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(QA, "post-4745.raw.%s.before.html" % stamp), "w", encoding="utf-8").write(raw)
if hashlib.md5(read()["content"]["raw"].encode("utf-8")).hexdigest() != md5:
    raise SystemExit("FATAL: the content changed while we read it; nothing written")
s, r = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
print("[write]", s, "| verified", read()["content"]["raw"] == new)
