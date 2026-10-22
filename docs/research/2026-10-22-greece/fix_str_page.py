# -*- coding: utf-8 -*-
"""Our own defects on /short-term-rentals-abroad/short-term-rentals-greece/ (page 398), found by the SERP research 22.10.2026
(serp-dna.md section 8; HAD-592, the no-silent-gaps law): editor leftovers on the page ("מאמר מוכן להדבקה", a second "עודכן ונבדק"
line, a visible "תגיות מוצעות" block, a dead "חזרה למדריך המקיף" line), three cut-off sentences, one sentence that implied a
buyer can keep an existing Airbnb registration in central Athens (the AMA is deleted on sale in districts 1-3), and a meta
description that promised a golden visa "from 250 thousand" (outdated since 2024). Nothing else changes. Backup, read-back, live check.
  python docs/research/2026-10-22-greece/fix_str_page.py [--dry]"""
import io, os, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "strfix"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 398
CLUSTER = ('<p>המדריכים המלאים ליוון: <a href="/global/greece/">נדל״ן ביוון</a> · <a href="/athens-apartments/">דירה באתונה</a> · '
           '<a href="/acquisition-greece/">קניית דירה ביוון, השלבים והעלויות</a> · <a href="/taxation-greece-israel/">מיסוי דירה ביוון לישראלים</a></p>')
R = [
    ("<p>מאמר מוכן להדבקה</p>", ""),
    ("<p>עודכן ונבדק: 28.5.2026</p>", ""),
    ("<p>הבדיקה הנכונה היא לא “כמה הדירה יכולה להכניס ב-Airbnb” </p>",
     "<p>הבדיקה הנכונה היא לא “כמה הדירה יכולה להכניס ב-Airbnb”, אלא האם מותר לרשום אותה, כמה נשאר אחרי כל ההוצאות והמסים, ומה החלופה בהשכרה לטווח ארוך.</p>"),
    ("ו-4 אירו ליום בבית פרטי מעל 80 </p>", "ו-4 אירו ליום בבית פרטי מעל 80 מ״ר.</p>"),
    ("ולכן נכס באתונה בלי AMA פעיל או בלי בדיקת רובע מדויקת אינו מתאים להנחת עבודה אוטומטית של</p>",
     "ולכן לפני קנייה באתונה בודקים באיזה מחוז הנכס נמצא: במחוזות 1 עד 3 גם רישום AMA קיים נמחק כשהדירה נמכרת, ואי אפשר להניח הכנסה מהשכרה קצרה.</p>"),
    ("<p>חזרה למדריך המקיף: חזרה למדריך המקיף</p>", CLUSTER),
]
s, b, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,meta" % PID)
raw = b["content"]["raw"]; new = raw
for a, c in R:
    if new.count(a) != 1:
        raise SystemExit("anchor x%d: %s" % (new.count(a), a[:60]))
    new = new.replace(a, c)
i = new.find("<h2>תגיות מוצעות</h2>"); j = new.find("<h2>", i + 5)
if i < 0 or j < 0: raise SystemExit("tags block not found")
new = new[:i] + new[j:]
DESC = "מדריך 2026 למשקיע ישראלי: רישום AMA, הקפאת רישום חדש במרכז אתונה ובמרכז סלוניקי, אגרת האקלים, מס על שכירות במדרגות 2026, מחירים ותשואה נטו."
print("before", len(raw), "after", len(new), "| old desc:", b["meta"].get("_yoast_wpseo_metadesc"))
if DRY: raise SystemExit("[dry]")
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new, "meta": {"_yoast_wpseo_metadesc": DESC}})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,meta" % PID)[1]
time.sleep(2)
html = urllib.request.urlopen(urllib.request.Request(b["link"] + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
body = html[html.find("<body"):]
ok = {"read-back": back["content"]["raw"] == new, "desc": back["meta"].get("_yoast_wpseo_metadesc") == DESC, "no leftovers": "מאמר מוכן להדבקה" not in body and "תגיות מוצעות" not in body,
      "cluster links": "/acquisition-greece/" in body, "no 250 in desc": "250 אלף" not in html[:html.find("<body")], "one h1": body.count("<h1") == 1}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
