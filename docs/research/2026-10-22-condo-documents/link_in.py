# -*- coding: utf-8 -*-
"""Three contextual links INTO /real-estate-lawyer/condo-documents/ (HAD-592, C12), one plain sentence each, right after a named
paragraph of a related page (the owner's pace rule: a few pages a day). Each page keeps its own intent: the land-extract page keeps
"נסח טאבו", the checklist keeps "רשימת בדיקות", the parking guide keeps "חניה בפרויקט חדש"; the sentence only sends the reader who
needs the condo file onward. Backup before, read-back after, the live page checked for the link and one h1.
  python docs/research/2026-10-22-condo-documents/link_in.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "linkin"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
BK = os.path.join(H, "page-backup"); os.makedirs(BK, exist_ok=True)
L = '<a href="/real-estate-lawyer/condo-documents/">%s</a>'
PLAN = [
 (18, "בנסח אפשר לראות פרטים כמו גוש, חלקה ותת חלקה",
  "הנסח מראה שיש הצמדה, אבל איפה בדיוק החניה או המחסן רואים רק בתיק הבית המשותף: " + L % "כך מזמינים את הצו, התקנון והתשריט וקוראים אותם" + "."),
 (8, "לפני חתימה צריך להבין מי בעל הזכויות ומה בדיוק נמכר",
  "בדירה בבית משותף כדאי להזמין גם את תיק הבית המשותף, ב־39 ₪ באתר הממשלתי, ולבדוק בתשריט את החניה, המחסן והגג: " + L % "מסמכי בית משותף ומה בודקים בהם" + "."),
 (6125, "בפרויקט שטרם נרשם כבית משותף עדיין אין תמיד נסח",
  "אחרי שהבניין נרשם, החניה מופיעה בתשריט הבית המשותף באות ובצבע של הדירה, וכך בודקים שהיא אכן שלכם: " + L % "איך קוראים תשריט בית משותף" + "."),
]
plain = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()
for pid, start, sent in PLAN:
    s, b, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % pid)
    raw = b["content"]["raw"]
    if "/real-estate-lawyer/condo-documents/" in raw:
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
    ok = back == new and body.count("<h1") == 1 and 'href="/real-estate-lawyer/condo-documents/"' in body
    print("   ", "LIVE OK" if ok else "LIVE CHECK FAILED")
