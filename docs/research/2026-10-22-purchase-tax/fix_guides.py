# -*- coding: utf-8 -*-
"""The 18-month rule on our two purchase-tax guides (HAD-592 C14; brief.md section 8.7; facts F2, F5, F5a). Both guides said an
upgrader must sell the previous home within 18 months. For purchases from 1.6.2025 the period is 24 months (18 months for
purchases 1.6.2023-31.5.2025, or 12 months from receiving a contractor home, the later), and the war extension of instruction
2/2026 moved most deadlines. The investor guide also never said that the 8%/10% rate is a temporary order to 31.12.2026.
Only those sentences change; every section stays. Backup, read-back, live check.
  python docs/research/2026-10-22-purchase-tax/fix_guides.py [--dry]"""
import io, os, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "fixguides"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
CALC = '<a href="/purchase-tax-calculator/">מחשבון מס הרכישה</a>'
PERIOD = ("לרכישה מ־1.6.2025 יש למכור את הדירה הקודמת תוך 24 חודשים מרכישת החדשה; לרכישה מ־1.6.2023 עד 31.5.2025 התקופה 18 חודשים; ובדירה מקבלן "
          "12 חודשים מקבלת הדירה, המאוחר מביניהם. בגלל המלחמה, מועד שהתקופה שלו נוגעת בתקופה 28.2.2026 עד 31.5.2026 נדחה למאוחר מבין 31.8.2026 לבין המועד המקורי "
          "ועוד שלושה חודשים (הוראת ביצוע 2/2026)")
FIRST = [
    ('<h2 dir="rtl">מי נחשב בעל דירה יחידה וכלל 18 החודשים</h2>', '<h2 dir="rtl">מי נחשב בעל דירה יחידה, ותוך כמה זמן למכור דירה קודמת</h2>'),
    ('בהחלפת דירה, הכלל שהרוכשים נוטים לכנות "כלל 18 החודשים" מתייחס', 'בהחלפת דירה, הכלל שרבים עדיין מכנים "כלל 18 החודשים" מתייחס'),
    ('לפי הנתון המחייב בחוק מיסוי מקרקעין, יש למכור את הדירה הקודמת תוך 18 חודשים מרכישת החדשה, כאשר יש לבדוק בכל עסקה את הוראות המעבר והמועד המדויק של הרכישה.',
     PERIOD + ". את התאריך שלכם מחשבים ב" + CALC + "."),
    ('בהקשר של כלל 18 החודשים, איחור במכירה עלול להפוך את העסקה לעסקת דירה נוספת לצורכי מס.',
     'איחור במכירה מעבר לתקופה, 24 חודשים לרכישה מ־1.6.2025, עלול להפוך את העסקה לעסקת דירה נוספת לצורכי מס.'),
    ('לפי כלל 18 החודשים, יש למכור את הדירה הקודמת תוך 18 חודשים מרכישת הדירה החדשה כדי ליהנות ממדרגות דירה יחידה, בכפוף להוראות הדין החלות על מועד העסקה.',
     'לרכישה מ־1.6.2025 יש למכור את הדירה הקודמת תוך 24 חודשים מרכישת הדירה החדשה כדי ליהנות ממדרגות דירה יחידה (18 חודשים לרכישה מ־1.6.2023 עד 31.5.2025, ו־12 חודשים מקבלת דירה מקבלן, המאוחר מביניהם).'),
]
INV_SECTION = ('<h2 dir="rtl">דירה חלופית: מתי משקיע משלם כמו דירה יחידה</h2> '
    '<p dir="rtl">משפחות רבות קונות דירה גדולה יותר עוד לפני שמכרו את הישנה. החוק לא מחייב אותן במס של משקיע אם ימכרו את הדירה הקודמת בזמן. ' + PERIOD + '. '
    'מי שמוכר בזמן נחשב קונה של דירה יחידה לצורך מס הרכישה על הדירה החדשה.</p> '
    '<p dir="rtl">בדיווח על רכישת הדירה החדשה מצהירים שהדירה הקודמת תימכר בתוך התקופה, ומשלמים לפי מדרגות הדירה היחידה. אם הדירה הישנה לא נמכרה עד תום התקופה, '
    'רשות המסים דורשת את ההפרש לשיעור של דירה נוספת, עם הפרשי הצמדה וריבית מיום הרכישה. מי ששילם כדירה נוספת ומכר בזמן מקבל החזר.</p> '
    '<p dir="rtl">בדירה מקבלן התקופה נספרת גם מיום קבלת החזקה בדירה החדשה, 12 חודשים, ונבחר המועד המאוחר. את התאריך המדויק שלכם, כולל הארכת המלחמה, מחשבים ב' + CALC + '.</p> '
    '<div class="note" dir="rtl">לא כדאי לחכות לחודשים האחרונים כדי להתחיל למכור: עיכוב בעסקת המכירה עלול לגרור את מלוא המס של דירה נוספת.</div> '
    '<h2 dir="rtl">השיעור על דירה נוספת: הוראת שעה עד 31.12.2026</h2> '
    '<p dir="rtl">השיעור של 8% עד 6,055,070 ₪ ו־10% מעל, על דירה נוספת, לתושב חוץ ולחברה, נקבע בהוראת שעה לרכישות מ־16.1.2025 עד 31.12.2026 (הוראת ביצוע 1/2026 של רשות המסים). '
    'רשות המסים לא פרסמה עדיין מה יחול מ־1.1.2027. מי שמתכנן לחתום על דירה להשקעה סביב סוף השנה בודק את השיעור ביום החתימה.</p> ')
s, b, _ = req("GET", "/wp-json/wp/v2/pages/529?context=edit&_fields=content,link")
raw1 = b["content"]["raw"]; new1 = raw1; link1 = b["link"]
for a, c in FIRST:
    if new1.count(a) != 1: raise SystemExit("first-home anchor x%d: %s" % (new1.count(a), a[:60]))
    new1 = new1.replace(a, c)
s, b2, _ = req("GET", "/wp-json/wp/v2/pages/532?context=edit&_fields=content,link")
raw2 = b2["content"]["raw"]; link2 = b2["link"]
i = raw2.index('<h2 dir="rtl">כלל 18 החודשים: מתי משקיע משלם כמו דירה יחידה</h2>'); j = raw2.index("<h2", i + 10)
new2 = raw2[:i] + INV_SECTION + raw2[j:]
print("first-home", len(raw1), "->", len(new1), "| investor", len(raw2), "->", len(new2))
if DRY: raise SystemExit("[dry]")
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
for pid, raw, new, link in ((529, raw1, new1, link1), (532, raw2, new2, link2)):
    io.open(os.path.join(bk, "page-%d-%s.html" % (pid, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
    req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"content": new})
    back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % pid)[1]["content"]["raw"]
    time.sleep(1.5)
    page = urllib.request.urlopen(urllib.request.Request(link + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    bd = page[page.find("<body"):]
    ok = back == new and bd.count("<h1") == 1 and "24 חודשים" in bd and "תוך 18 חודשים מרכישת החדשה" not in bd and "/purchase-tax-calculator/" in bd
    print(pid, link, "LIVE OK" if ok else "LIVE CHECK FAILED")
