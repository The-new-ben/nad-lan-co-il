# -*- coding: utf-8 -*-
"""MortgageWorld O (loop round, HAD-675, 6.11.2026 evening): additive content on page 121 from a manual pass in the owner's Chrome.
  1. eligibility-loan: the ministry guide's terms (read by hand on gov.il, updated 25.9.2024) and the eligibility rate by term,
     worked from the formula (BoI average CPI-linked mortgage rate minus 0.5%, at most 3%) and the BoI series the guide links
     (in force from 19.10.2026, file updated 18.10.2026), labelled as our computation;
  2. rules-2026: the government relief plan, memo 13.1.2026, approved by the government 31.3.2026 (ynet), legislation stopped
     20.5.2026 (Globes);
  3. a new chapter "משכנתא לפי המצב שלכם" (renovation, no equity, age, self-employed, young couples, a refund from the state),
     only official facts: directive 329 s.2 and s.4א, Q&A 2.2 and 2.7, Annex A 1.3; no age limit in directive 329 (text searched);
  4. the map: one more link in stage 1; 5. FAQ +5.
Nothing removed. python write_page_o.py --dry, then without --dry."""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, H)
from chapters_n import table, L  # noqa: E402
BACK = '<p class="nlmap-back"><a href="#mortgage-map">↑ לכל נושאי המשכנתא</a></p>\n'
GUIDE = "https://www.gov.il/he/pages/mortgage_guide"
BOIAVG = "https://www.boi.org.il/information/interestrates/mortgage/"
GLOBES = "https://www.globes.co.il/news/article.aspx?did=1001543473"
QA = "https://www.boi.org.il/media/emunmobp/202601.pdf"
H2852 = "https://boi.org.il/media/hjrlkrse/h2852.pdf"
KZ = "https://www.kolzchut.org.il/he/"

# 1. eligibility: terms + the rate by term (pribmash in force 19.10.2026: 10-15 3.2417, 15-20 3.4552, 20-25 3.3652, >25 3.5272)
def elig_rate(avg):
    return min(3.0, round(avg - 0.5, 2))
ROWS = [("10 עד 15 שנה", 3.2417), ("15 עד 20 שנה", 3.4552), ("20 עד 25 שנה", 3.3652), ("מעל 25 שנה", 3.5272)]
ELIG_ADD = ('<p><b>תנאי ההלוואה לפי המדריך של משרד הבינוי והשיכון:</b> בדירה חדשה מקבלן הסיוע ניתן אם לא עברו 36 חודשים מהחתימה על חוזה '
  'הרכישה, ובדירה יד שנייה אם לא עברה שנה, ובשני המקרים רק כל עוד התמורה לא שולמה במלואה. מי שבונה את ביתו מתחיל לממש תוך 36 חודשים '
  'מהיתר הבנייה. ככלל, כל המשכנתא יחד, כולל המשכנתא הבנקאית המשלימה, לא עולה על 75% ממחיר הדירה; ההחזר צמוד למדד, התקופה עד 30 שנה '
  '(אפשר גם 5, 6, 7, 8, 9, 10, 15, 20 או 25), ואת הסיוע מקבלים בכל בנק למשכנתאות, לא רק בבנק שהנפיק את התעודה (' + L(GUIDE, "המדריך באתר הממשלה") + ').</p>\n'
  + table("ריבית הלוואת הזכאות לפי התקופה, בחישוב לפי הנוסחה",
          "הנוסחה: הריבית הממוצעת על משכנתאות צמודות למדד שבנק ישראל מפרסם, פחות 0.5%, ולא יותר מ־3%. הממוצעים בתוקף מ־19.10.2026. חישוב שלנו; הריבית המחייבת היא זו שבאישור הבנק.",
          ["תקופת ההלוואה", "הממוצע של בנק ישראל", "ריבית הזכאות"],
          [[t, "%.2f%%" % a, "%.2f%%" % elig_rate(a)] for t, a in ROWS])
  + '<p>חוק התוכנית הכלכלית לשנת 2026 עדכן את נוסח הבסיס לריבית הממוצעת של הבנקים באשראי לדיור, פחות 0.5% ועד 3%, או הריבית של הבנק המלווה אם '
  'היא נמוכה יותר. הממוצעים: ' + L(BOIAVG, "הריבית הממוצעת על משכנתאות, בנק ישראל") + '.</p>\n')

# 2. rules-2026 rows
ROW = lambda d, w, s: '<tr><th scope="row">%s</th><td>%s</td><td>%s</td></tr>' % (d, w, s)
R13 = ROW("13.1.2026", "תזכיר חוק ממשלתי: סיוע לנוטלי הלוואות לדיור עקב עליית הריבית (הוראת שעה), למי שלקחו משכנתא לפני העלאות הריבית של מרץ 2022", "הופץ להערות הציבור")
R31 = ROW("31.3.2026", "הממשלה אישרה את תוכנית הסיוע: מענק חודשי של עד 75% מהעלייה הריאלית בהחזר, לבעלי דירה יחידה", "אושרה בממשלה (ynet)")
R20 = ROW("20.5.2026", "חקיקת תוכנית הסיוע נעצרה, והיא ירדה מהפרק", "נעצרה (גלובס)")

# 3. situations chapter
SIT = ('<section id="mortgage-situations">\n<h2>משכנתא לפי המצב שלכם: שיפוץ, בלי הון עצמי, גיל, עצמאים וזוגות צעירים</h2>\n'
  '<p class="nlx-ans">הכללים של בנק ישראל זהים לכולם, אבל כל מצב פוגש מגבלה אחרת: בשיפוץ זו מטרת ההלוואה, בלי הון עצמי זה אחוז המימון, '
  'בגיל מבוגר זו תקופת ההלוואה, ובעצמאים זו ההוכחה של ההכנסה. הנה מה שקובעים המקורות הרשמיים, מצב אחרי מצב.</p>\n<ul>\n'
  '<li><b>משכנתא לשיפוץ:</b> הלוואה לשיפוץ או להרחבה של דירת מגורים לא נחשבת הלוואה לכל מטרה (שאלות ותשובות של הפיקוח על הבנקים, 2.2), '
  'ולכן לא חלה עליה התקרה של 50% של הלוואה לכל מטרה. מגבלת ההחזר, עד 50% מההכנסה הפנויה, חלה כרגיל. כמה אפשר לקבל על הדירה: '
  '<a href="#tool-neches">דירה קיימת</a>.</li>\n'
  '<li><b>משכנתא בלי הון עצמי:</b> בבנק לא. המימון המרבי הוא 75% בדירה יחידה, 70% בדירה חליפית ו־50% בדירה להשקעה (הוראה 329, סעיף 2). '
  'בדירה במחיר מופחת משלמים מכספכם לפחות 100,000 ₪, או 60,000 ₪ בדירה שניתן עליה מענק (סעיף 4א). הורים יכולים לעזור בהלוואה על הדירה '
  'שלהם, עד 50% משוויה (שו״ת 2.7), והבנק סופר לכל היותר מחצית מההכנסה של קרוב שאינו קונה (נספח א, 1.3). עוד: '
  '<a href="/mortgage-calculator/mortgage-ltv-ratio/">אחוז מימון משכנתא</a>.</li>\n'
  '<li><b>עד איזה גיל אפשר לקחת משכנתא:</b> בהוראה 329 של בנק ישראל אין גיל מרבי ללווה. המגבלה היא תקופה של עד 30 שנה (סעיף 8), ועד '
  'איזה גיל ההלוואה צריכה להסתיים קובע כל בנק לפי המדיניות שלו. לבני הגיל השלישי יש גם <a href="/mortgage-calculator/reverse-mortgage/">משכנתא הפוכה</a>.</li>\n'
  '<li><b>משכנתא לעצמאים:</b> אותם כללים בדיוק; ההבדל הוא במסמכים שמוכיחים את ההכנסה. רשימת המסמכים לכל סוג לווה, כולל עצמאים: '
  '<a href="#tool-ready">מוכנים לאישור עקרוני?</a></li>\n'
  '<li><b>משכנתא לזוגות צעירים:</b> בודקים קודם זכאות להלוואה מהמדינה, לפני החתימה על חוזה הרכישה (<a href="#tool-zakaut">מחשבון זכאות</a>), '
  'ואת <a href="/dira-behanacha/">דירה בהנחה</a>, ואחר כך כמה דירה ההכנסה וההון העצמי קונים (<a href="#tool-budget">כמה דירה זה קונה</a>).</li>\n'
  '<li><b>החזר משכנתא מהמדינה:</b> אין היום החזר כללי. תוכנית הסיוע הממשלתית למי שלקחו משכנתא לפני עליית הריבית אושרה בממשלה ב־31.3.2026, '
  'והחקיקה שלה נעצרה במאי 2026 (' + L(GLOBES, "גלובס, 20.5.2026") + '). מה שקיים: הלוואת זכאות, השתתפות חודשית לבני 70 ומעלה עם השלמת '
  'הכנסה, 340 ₪ לחודש לאדם עם מוגבלות מקצרת חיים, עד 2,500 ₪ לחודש למגדלי יתומים של חללים, ו־25% מתשלומי ביטוח החיים חוזרים בדוח '
  'למס (<a href="#mortgage-rights">זכויות במשכנתא</a>).</li>\n</ul>\n'
  '<p>המקורות: ' + L(H2852, "הוראה 329, גרסה 13") + ' · ' + L(QA, "שאלות ותשובות של הפיקוח, 8.2.2026") + '.</p>\n' + BACK + '</section>\n')

FAQ = [
    ("יש החזר משכנתא מהמדינה?",
     'אין היום החזר כללי. תוכנית ממשלתית למענק חודשי לבעלי דירה יחידה שלקחו משכנתא לפני עליית הריבית אושרה בממשלה ב־31.3.2026, והחקיקה שלה '
     'נעצרה במאי 2026. קיימים סיוע לזכאים, השתתפות בהחזר לבני 70 ומעלה עם השלמת הכנסה, וזיכוי מס של 25% מתשלומי ביטוח החיים.'),
    ("מה הריבית בהלוואת זכאות היום?",
     'לפי הנוסחה, הריבית הממוצעת על משכנתאות צמודות למדד של בנק ישראל פחות 0.5%, ולא יותר מ־3%. בממוצעים שבתוקף מ־19.10.2026 זה יוצא כ־2.74% '
     'ל־10 עד 15 שנה, 2.96% ל־15 עד 20, 2.87% ל־20 עד 25 ו־3% מעל 25 שנה. הריבית המחייבת מופיעה באישור הבנק.'),
    ("עד איזה גיל אפשר לקחת משכנתא?",
     'בהוראה 329 של בנק ישראל אין גיל מרבי ללווה. ההגבלה היא תקופה של עד 30 שנה, וכל בנק קובע לפי המדיניות שלו עד איזה גיל ההלוואה צריכה להסתיים.'),
    ("אפשר לקחת משכנתא בלי הון עצמי?",
     'בבנק לא: המימון המרבי הוא 75% בדירה יחידה, 70% בדירה חליפית ו־50% בדירה להשקעה. הורים יכולים לעזור בהלוואה על הדירה שלהם, עד 50% משוויה, '
     'ובדירה במחיר מופחת משלמים מכספכם לפחות 100,000 ₪.'),
    ("משכנתא לשיפוץ נחשבת הלוואה לכל מטרה?",
     'לא. לפי הפיקוח על הבנקים, הלוואה לשיפוץ או להרחבה של דירת מגורים לא נחשבת הלוואה לכל מטרה, ולכן התקרה של 50% של הלוואה לכל מטרה לא חלה '
     'עליה. מגבלת ההחזר, עד 50% מההכנסה הפנויה, חלה כרגיל.'),
]

src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_o"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/121?context=edit&_fields=content,link"); assert s == 200, s
raw = r["content"]["raw"]; assert 'id="mortgage-situations"' not in raw, "already written"
new = raw


def sec_bounds(txt, sid):
    m0 = re.search(r'<section\b[^>]*\bid="%s"' % re.escape(sid), txt); i = m0.start(); depth = 0
    for m in re.finditer(r'<section\b|</section>', txt[i:]):
        depth += 1 if m.group(0) == '<section' else -1
        if depth == 0:
            return i, i + m.start(), i + m.end()


def before_back(txt, sid, html):
    i, c, e = sec_bounds(txt, sid); k = txt.rfind('<p class="nlmap-back">', i, c); assert k > i, sid
    return txt[:k] + html + txt[k:]


def one(txt, a, b):
    assert txt.count(a) == 1, ("anchor", a[:70], txt.count(a)); return txt.replace(a, b)


new = before_back(new, "eligibility-loan", ELIG_ADD)
new = one(new, '<tr><th scope="row">8.2.2026</th>', R13 + '<tr><th scope="row">8.2.2026</th>')
new = one(new, '<tr><th scope="row">8.6.2026</th>', R31 + R20 + '<tr><th scope="row">8.6.2026</th>')
i, c, e = sec_bounds(new, "existing-property"); new = new[:e] + "\n" + SIT + new[e:].lstrip("\n")
new = one(new, '<li><a href="#bank-of-israel-rules">מה בנק ישראל מתיר</a></li>',
          '<li><a href="#bank-of-israel-rules">מה בנק ישראל מתיר</a></li><li><a href="#mortgage-situations">שיפוץ, בלי הון עצמי, גיל ועצמאים</a></li>')
new = one(new, '<span>1 · לפני שלוקחים משכנתא</span><small>7</small>', '<span>1 · לפני שלוקחים משכנתא</span><small>8</small>')
i, c, e = sec_bounds(new, "faq"); new = new[:c] + "".join("<h3>%s</h3>\n<p>%s</p>\n" % qa for qa in FAQ) + new[c:]
for line in raw.split("\n"):
    if line.strip():
        ln = line.replace('<span>1 · לפני שלוקחים משכנתא</span><small>7</small>', '<span>1 · לפני שלוקחים משכנתא</span><small>8</small>')
        assert ln in new or line in new or '<tr><th scope="row">8.2.2026</th>' in line or '<tr><th scope="row">8.6.2026</th>' in line or 'מה בנק ישראל מתיר</a></li>' in line, ("missing", line[:80])
vis = re.sub(r"<[^>]+>", " ", ELIG_ADD + R13 + R31 + R20 + SIT + "".join(q + a for q, a in FAQ))
assert not re.search(r"[–—]", vis), "long dash"
for bad in ("סימולציה", "ממשק", "דמו", "המערכת", "הפלטפורמה", "עולם המשכנתא"):
    assert not re.search(r"(?<![֐-׿])%s(?![֐-׿])" % bad, vis), bad
for href in sorted(set(re.findall(r'<a href="(/[^"#]*)"', SIT))):
    assert urllib.request.urlopen(urllib.request.Request("https://nad-lan.co.il" + href, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).status == 200, href
print("[page 121] round O; content %d -> %d bytes; FAQ +%d; rates %s" % (len(raw), len(new), len(FAQ), [elig_rate(a) for _, a in ROWS]))
if DRY:
    io.open(os.path.join(H, "preview-content-o.html"), "w", encoding="utf-8", newline="").write(new); print("[dry] ok"); sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-121-%s.html" % time.strftime("%Y%m%d-%H%M%S")), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/121", {"content": new}); assert s2 in (200, 201), s2
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print("live:", 'id="mortgage-situations"' in page, page.count('"@type":"Question"'), "questions", "2.74%" in page)
