# -*- coding: utf-8 -*-
"""MortgageWorld Q (loop round, HAD-675, 6.11.2026 evening): two comparison tables from the lenders' own pages, read by hand in the
owner's Chrome on 6.11.2026, plus two FAQ answers. Additive; nothing removed.
  1. payment-trouble: "דחיית תשלומי משכנתא בבנקים" (Mizrahi-Tefahot, Leumi Mortgages, Discount, Bank of Jerusalem; Hapoalim's
     page did not render its text and is left out), with the law's baseline (s.9ח1);
  2. existing-property: what banks may lend (directive 329) next to what two insurers publish (Menora Mivtachim, Clal); Harel's
     page refused access and is left out;
  3. FAQ +2. python write_page_q.py --dry, then without --dry."""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, H)
from chapters_n import table, L  # noqa: E402
LTR = lambda s: '<bdi dir="ltr">%s</bdi>' % s

MZ = "https://www.mizrahi-tefahot.co.il/mortgages/updatemortgage/mortgage-break/"
LM = "https://mortgage.leumi.co.il/all-about-mortgage/category/about/deferment-payments"
DS = "https://mortgage.discountbank.co.il/your-mortgage/mortgage-changes"
BJ = "https://www.bankjerusalem.co.il/mortgage/mortgage_freeze_questions"
MN = "https://www.menoramivt.co.il/product/mortgage-loan"
CL = "https://www.clalbit.co.il/loansandmortgage/mortgagenew/"

DEFER = (table("דחיית תשלומי משכנתא בבנקים: מה כל בנק מפרסם",
               "מתוך דף הדחייה באתר של כל בנק, נקרא ב־6.11.2026. מה שלא כתוב בדף מסומן כך. הזכות שבחוק חלה בכל בנק.",
               ["בנק", "איך דוחים", "לכמה זמן", "עלות", "איך מבקשים"],
               [["החוק, בכל בנק", "דחייה בנסיבות מיוחדות (אבטלה, מחלה, לידה), אם בחרתם בה בהסכם", "עד 3 חודשים בכל פעם, עד 3 פעמים", "לפי ההסכם", "בכתב, עם אישורים"],
                [L(MZ, "מזרחי־טפחות"), "דחייה מלאה (קרן וריבית) או חלקית (ריבית בלבד), בלי להאריך את תקופת המשכנתא", "לא צוין בדף", "320 ₪ לכל הלוואה על שינוי לוח התשלומים", LTR("*8860") + ", שלוחה 4 ואז 5; בקשה אחת לכל הרכב לווים"],
                [L(LM, "לאומי למשכנתאות"), "בנסיבות מיוחדות לפי ההסכם, וגם דחייה לפי שיקול הבנק בהלוואות מכספי הבנק, בלי לדחות את מועד הפירעון הסופי", "בנסיבות מיוחדות עד 3 חודשים בכל פעם ועד 3 פעמים", "לפי תעריפון הבנק", LTR("*6062")],
                [L(DS, "דיסקונט"), "קרן וריבית או קרן בלבד, עם הארכת תקופה או בלעדיה; בהלוואה צמודה גם הפרשי ההצמדה נדחים", "עד 6 חודשים", "לפי הבנק; בביטול תוך 60 ימים העמלה לא מוחזרת", "באפליקציה (בהלוואות בלי ערבים) או " + LTR("*2009")],
                [L(BJ, "בנק ירושלים"), "הריבית על תקופת ההקפאה מתווספת והיתרה נפרסת על החודשים שנותרו; ההקפאה לא מונעת מחזור", "לא צוין בדף", "לא צוין בדף", "דרך הבנק"]],
               numcols=[])
         + '<p>בכל הבנקים התשלומים נגבים כרגיל עד שהבנק מאשר את הדחייה, וכל דחייה מייקרת את ההלוואה. כמה זה יעלה במשכנתא שלכם, בשלוש הדרכים: '
           '<a href="#tool-kashe">כשקשה לשלם</a>. הדף של בנק הפועלים לא הציג את תוכנו בבדיקה שלנו, ולכן הוא לא בטבלה.</p>\n')

NONBANK = (table("משכנתא על דירה קיימת: מה מותר לבנק, ומה חברות ביטוח מפרסמות",
                 "הבנקים: הוראה 329 של בנק ישראל, שחלה על תאגידים בנקאיים. חברות הביטוח: מהדף של כל חברה, נקרא ב־6.11.2026. זה מה שהן מפרסמות, לא הצעה.",
                 ["מי מלווה", "הלוואה לכל מטרה על הדירה", "קניית דירה להשקעה", "המקור"],
                 [["בנק", "עד 50% משווי הדירה; עד 70% כשהחלק מעל 50% לא עולה על 200,000 ₪", "עד 50%", "הוראה 329 של בנק ישראל"],
                  ["מנורה מבטחים", "עד 70%", "עד 75%", L(MN, "משכנתא לכל מטרה, מנורה מבטחים")],
                  ["כלל ביטוח ופיננסים", "עד 60%, גם באיחוד הלוואות", "עד 60%, ובשעבוד כל הנכסים יחד עד 60% משוויים", L(CL, "משכנתא בכלל ביטוח ופיננסים")]],
                 numcols=[])
           + '<p>ההבדל נובע מכך שהוראה 329 חלה על הבנקים, ומנורה מבטחים כותבת בדף שלה שהיא לא כפופה לכללי החיתום של בנק ישראל. אחוז מימון '
             'גבוה יותר הוא גם חוב גדול יותר על הדירה; משווים את הריבית ואת סך ההחזרים, לא רק את אחוז המימון. הדף של הראל דחה את הגישה בבדיקה '
             'שלנו, ולכן הוא לא בטבלה.</p>\n')

FAQ = [
    ("כמה חודשים אפשר להקפיא משכנתא?",
     'לפי החוק, מי שבחר בהסכם בדחייה בנסיבות מיוחדות זכאי לעד 3 חודשים בכל פעם ועד 3 פעמים. מעבר לזה זה תלוי בבנק: דיסקונט מפרסם דחייה של עד '
     '6 חודשים, ומזרחי־טפחות גובה 320 ₪ לכל הלוואה על שינוי לוח התשלומים. בכל דחייה ההלוואה מתייקרת.'),
    ("חברת ביטוח נותנת יותר מימון על דירה קיימת?",
     'כן, לפי מה שהן מפרסמות: מנורה מבטחים עד 70% בהלוואה לכל מטרה ועד 75% לדירה להשקעה, וכלל ביטוח ופיננסים עד 60%. בבנק התקרה היא 50%, ועד '
     '70% כשהחלק מעל 50% לא עולה על 200,000 ₪, כי הוראה 329 של בנק ישראל חלה על הבנקים.'),
]

src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_q"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/121?context=edit&_fields=content,link"); assert s == 200, s
raw = r["content"]["raw"]; assert "דחיית תשלומי משכנתא בבנקים: מה כל בנק מפרסם" not in raw, "already written"


def sec_bounds(txt, sid):
    m0 = re.search(r'<section\b[^>]*\bid="%s"' % re.escape(sid), txt); i = m0.start(); depth = 0
    for m in re.finditer(r'<section\b|</section>', txt[i:]):
        depth += 1 if m.group(0) == '<section' else -1
        if depth == 0:
            return i, i + m.start(), i + m.end()


def before_back(txt, sid, html):
    i, c, e = sec_bounds(txt, sid); k = txt.rfind('<p class="nlmap-back">', i, c); assert k > i, sid
    return txt[:k] + html + txt[k:]


new = before_back(raw, "payment-trouble", DEFER)
new = before_back(new, "existing-property", NONBANK)
i, c, e = sec_bounds(new, "faq"); new = new[:c] + "".join("<h3>%s</h3>\n<p>%s</p>\n" % qa for qa in FAQ) + new[c:]
for line in raw.split("\n"):
    assert not line.strip() or line in new, ("missing", line[:80])
vis = re.sub(r"<[^>]+>", " ", DEFER + NONBANK + "".join(q + a for q, a in FAQ))
assert not re.search(r"[–—]", vis), "long dash"
for bad in ("סימולציה", "ממשק", "דמו", "המערכת", "הפלטפורמה", "עולם המשכנתא"):
    assert not re.search(r"(?<![֐-׿])%s(?![֐-׿])" % bad, vis), bad
print("[page 121] round Q; content %d -> %d bytes; FAQ +%d" % (len(raw), len(new), len(FAQ)))
if DRY:
    io.open(os.path.join(H, "preview-content-q.html"), "w", encoding="utf-8", newline="").write(new); print("[dry] ok"); sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-121-%s.html" % time.strftime("%Y%m%d-%H%M%S")), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/121", {"content": new}); assert s2 in (200, 201), s2
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print("live:", "מה כל בנק מפרסם" in page, "מנורה מבטחים" in page, page.count('"@type":"Question"'), "questions")
