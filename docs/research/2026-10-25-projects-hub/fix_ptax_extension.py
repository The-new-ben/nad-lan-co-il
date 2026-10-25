# -*- coding: utf-8 -*-
"""The foreign-resident / additional-home purchase-tax order was extended to purchases up to 10.2.2027 inclusive (Tax Authority
notice of 12.10.2026, https://www.gov.il/he/pages/pa121026-2, found while building the language hubs, 25.10.2026). Corrects the two
Hebrew pages that still said it ends 31.12.2026: /purchase-tax-calculator/ (page 6, text + Yoast description) and
/real-estate-tax-advisor/purchase-tax-investor/ (page 532). Exact sentence replacements on the live content (each must match once),
a backup of the live content first, read-back, then the live page is checked. Run after release 1.72.515 (the calculator itself).
  python docs/research/2026-10-25-projects-hub/fix_ptax_extension.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "ptxfix"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
N = '<a href="https://www.gov.il/he/pages/pa121026-2" rel="noopener">הודעת רשות המסים מ־12.10.2026</a>'
FIX = {
    6: [
        ("השיעור על דירה נוספת הוא הוראת שעה עד 31.12.2026. מדווחים", "השיעור על דירה נוספת הוא הוראת שעה, שהוארכה לרכישות עד 10.2.2027. מדווחים"),
        ("<small>עד ₪6,055,070 · הוראת שעה עד 31.12.2026</small>", "<small>עד ₪6,055,070 · הוראת שעה עד 10.2.2027</small>"),
        ("הוא הוראת שעה שמסתיימת ב־31.12.2026.</p>", "הוא הוראת שעה, שהוארכה לרכישות עד 10.2.2027.</p>"),
        ('<span class="l">בתוקף:</span> הוראת שעה עד 31.12.2026</td>', '<span class="l">בתוקף:</span> הוראת שעה עד 10.2.2027</td>'),
        ("נקבע בהוראת שעה לרכישות מ־16.1.2025 עד 31.12.2026. רשות המסים לא פרסמה עד היום מה יחול מ־1.1.2027. בתקשורת דווח שההוראה עשויה להמשיך לחול עד אחרי הבחירות, אבל לא מצאנו לכך טקסט רשמי, ולכן אין כאן מספרים ל־2027. מי שחותם על דירה להשקעה סביב סוף השנה בודק את השיעור ביום החתימה. המחשבון מזהיר כשמועד העסקה אחרי 31.12.2026.",
         "נקבע בהוראת שעה לרכישות מ־16.1.2025 עד 31.12.2026. בעקבות פיזור הכנסת הוארכה הוראת השעה לרכישות עד 10.2.2027, כולל (" + N + "). מה יחול על רכישות מ־11.2.2027 עוד לא פורסם, ולכן אין כאן מספרים לתקופה שאחרי. מי שחותם על דירה להשקעה בתחילת 2027 בודק את השיעור ביום החתימה. המחשבון מזהיר כשמועד העסקה אחרי 10.2.2027."),
        ("לפי הוראת השעה עד 31.12.2026. מי שיהפוך", "לפי הוראת השעה, שהוארכה לרכישות עד 10.2.2027. מי שיהפוך"),
        ("<h3>מה יקרה למס הרכישה על דירה נוספת אחרי 31.12.2026?</h3><p>השיעור של 8% ו־10% הוא הוראת שעה עד 31.12.2026. רשות המסים לא פרסמה עדיין מה יחול מ־1.1.2027.</p>",
         "<h3>מה יקרה למס הרכישה על דירה נוספת אחרי 10.2.2027?</h3><p>השיעור של 8% ו־10% הוא הוראת שעה. היא נקבעה עד 31.12.2026, ובעקבות פיזור הכנסת הוארכה לרכישות עד 10.2.2027 (הודעת רשות המסים מ־12.10.2026). מה יחול על רכישות מ־11.2.2027 עוד לא פורסם.</p>"),
        ("ו־10% מעל, לפי הוראת השעה עד 31.12.2026.</p><h3>כמה מס רכישה", "ו־10% מעל, לפי הוראת השעה, שהוארכה לרכישות עד 10.2.2027.</p><h3>כמה מס רכישה"),
    ],
    532: [
        ('<h2 dir="rtl">השיעור על דירה נוספת: הוראת שעה עד 31.12.2026</h2>', '<h2 dir="rtl">השיעור על דירה נוספת: הוראת שעה עד 10.2.2027</h2>'),
        ("נקבע בהוראת שעה לרכישות מ־16.1.2025 עד 31.12.2026 (הוראת ביצוע 1/2026 של רשות המסים). רשות המסים לא פרסמה עדיין מה יחול מ־1.1.2027. מי שמתכנן לחתום על דירה להשקעה סביב סוף השנה בודק את השיעור ביום החתימה.",
         "נקבע בהוראת שעה לרכישות מ־16.1.2025 עד 31.12.2026 (הוראת ביצוע 1/2026 של רשות המסים), ובעקבות פיזור הכנסת הוארך לרכישות עד 10.2.2027, כולל (" + N + "). מה יחול על רכישות מ־11.2.2027 עוד לא פורסם. מי שמתכנן לחתום על דירה להשקעה בתחילת 2027 בודק את השיעור ביום החתימה."),
    ],
}
META = {6: ("(הוראת שעה עד 31.12.2026)", "(הוראת שעה עד 10.2.2027)")}
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
for pid, reps in FIX.items():
    s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,meta,link" % pid)
    raw = r["content"]["raw"]; new = raw
    for a, b in reps:
        assert new.count(a) == 1, (pid, new.count(a), a[:70])
        new = new.replace(a, b)
    left = new.count("31.12.2026")
    body = {"content": new}
    if pid in META:
        md = r["meta"].get("_yoast_wpseo_metadesc") or ""
        assert md.count(META[pid][0]) == 1, (pid, "metadesc")
        body["meta"] = {"_yoast_wpseo_metadesc": md.replace(*META[pid])}
    print("[page %d] %d replacements, '31.12.2026' left in text: %d (the original end date, named once as history)" % (pid, len(reps), left))
    if DRY:
        continue
    io.open(os.path.join(bk, "page-%d-%s.html" % (pid, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
    req("POST", "/wp-json/wp/v2/pages/%d" % pid, body)
    back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % pid)[1]["content"]["raw"]
    time.sleep(2)
    page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?nlx=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    ok = {"read-back": back == new, "10.2.2027 on the page": page.count("10.2.2027") >= 2, "notice link": "pa121026-2" in page,
          "one h1": page[page.find("<body"):].count("<h1") == 1, "old end-date sentence gone": "הוראת שעה עד 31.12.2026" not in page}
    for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
