# -*- coding: utf-8 -*-
"""Three contextual links INTO /pinkas-hakablanim/ (HAD-592), one plain sentence each, right after a named paragraph of a related page
(the owner's pace rule: a few pages a day). Each page keeps its own intent: the renovation page keeps "קבלן שיפוצים", the buying
guide keeps "קניית דירה", the supervisor page keeps "מפקח בנייה"; the sentence only sends the reader who wants to check a contractor.
Backup before, read-back after, the live page checked for the link and one h1. Skips a page that already links.
  python docs/research/2026-10-22-contractor-register/link_in.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "linkin"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
BK = os.path.join(H, "page-backup"); os.makedirs(BK, exist_ok=True)
L = '<a href="/pinkas-hakablanim/">%s</a>'
PLAN = [
 (109, "בישראל קיים רשם הקבלנים ופנקס קבלנים רשומים",
  "לפני שחותמים עם קבלן שיפוצים, מקלידים את השם או את מספר הקבלן ב" + L % "בדיקת קבלן רשום" + " ורואים אם הוא רשום בענף השיפוצים, באיזה סיווג ועד איזה סכום מותר לו לעבוד."),
 (9, "בדירה מקבלן, בדיקת המסמכים שונה",
  "את הקבלן עצמו בודקים ב" + L % "פנקס הקבלנים" + ": האם הוא רשום בענף הבנייה, מה הסיווג שלו, והאם יש הגבלה על הרישיון."),
 (94, "כדאי לבדוק גם ניגוד עניינים",
  "ואת הקבלן שהמפקח ילווה כדאי לבדוק כבר לפני החתימה, ב" + L % "חיפוש בפנקס הקבלנים" + ": באיזה ענף הוא רשום ועד איזה סכום מותר לו לבנות באתר אחד."),
]
plain = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()
for pid, start, sent in PLAN:
    s, b, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % pid)
    raw = b["content"]["raw"]
    if "/pinkas-hakablanim/" in raw:
        print(pid, "already links"); continue
    hit = next((m for m in re.finditer(r"<p\b[^>]*>(.*?)</p>", raw, re.S) if start in plain(m.group(1))), None)
    if not hit:
        print(pid, "PARAGRAPH NOT FOUND:", start[:40]); continue
    new = raw[:hit.end()] + "\n<p>" + sent + "</p>" + raw[hit.end():]
    print(pid, b["link"], "| after:", plain(hit.group(1))[:60])
    if DRY:
        continue
    io.open(os.path.join(BK, "page-%d-%s.html" % (pid, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
    req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"content": new})
    back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % pid)[1]["content"]["raw"]
    time.sleep(1.5)
    html = urllib.request.urlopen(urllib.request.Request(b["link"] + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    body = html[html.find("<body"):]
    ok = back == new and body.count("<h1") == 1 and 'href="/pinkas-hakablanim/"' in body
    print("   ", "LIVE OK" if ok else "LIVE CHECK FAILED")
