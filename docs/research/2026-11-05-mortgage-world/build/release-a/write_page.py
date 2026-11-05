# -*- coding: utf-8 -*-
"""MortgageWorld A, page 121 /mortgage-calculator/ (HAD-675, Ben 5.11.2026). Runs AFTER release 1.72.587 is live (mquick tool,
[nadlan_mortgage_market], boi-mortgage.json v2).

ADDITIVE (Ben 5.11: "don't remove content"): every original line stays. The only edits inside old text are listed in EDITS and checked
one by one: the H1 text (keywords.md section 8), the lead paragraph (a superset of the old one: every old clause kept, the monthly
number and the payment-first and schedule signals added), three headings renamed so the main page stops taking words its child pages
own (keywords.md section 4 and 8), and the U1 "עודכן" date.
What it adds:
  1. [nadlan_crumbs label="מחשבון משכנתא"] at the top (visible trail + BreadcrumbList; inc/breadcrumbs.php);
  2. the quick calculator [nadlan_tool id="mquick"] right after the CTA row, before the full tool;
  3. the full Mortgage 2.0 inside <details id="mortgage-full" open> (folded on phones after it has drawn; the page CTAs open it);
  4. the two old calculators each inside a <details> (kept, folded);
  5. [nadlan_mortgage_market] (this month's BoI numbers by bank and by city, Dataset JSON-LD) before the U1 block;
  6. a crawlable yearly amortization table (לוח סילוקין) for 1,000,000 ILS over 25 years at the system-average mix, in the
     Spitzer section;
  7. a section that states the current rules where AI answers repeat outdated ones (directive 329 ss.5, 7, 8, definitions);
  8. 8 new FAQ questions (30 to 38), no duplicate of the 30;
  9. Yoast title and meta description (keywords.md section 8).
  python write_page.py --dry   (GET only; writes preview-content.html here)
  python write_page.py         (backup, POST, read-back, live checks)"""
import io, json, math, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 121
D = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "boi-mortgage.json"), encoding="utf-8"))
BB = D["by_bank"]; I = len(BB["months"]) - 1; YM = BB["months"][I]
HEM = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]
def month(ym): y, m = ym.split("-"); return HEM[int(m) - 1] + " " + y
MON = month(YM)
UPDATED = "5.11.2026"
TR = ["fixed_nl", "prime", "var_nl_other", "var_cpi", "fixed_cpi"]
def ils(x): return "{:,.0f} ₪".format(round(x))
def eff(e): return (1 + e / 100) ** (1 / 12) - 1
def pmt(P, r, n): return P * r / (1 - (1 + r) ** -n) if r else P / n
def pay(bank, loan=1e6, years=25, i=I):
    mix = BB["mix"][bank]; rate = BB["rate"][bank]; tot = sum(mix[t][i] for t in TR)
    return sum(pmt(loan * mix[t][i] / tot, eff(rate[t][i]), years * 12) for t in TR)
P25 = pay("system"); P30 = pay("system", years=30); P20 = pay("system", years=20)
assert round(P25) == 5428, round(P25)
IRR = BB["rate"]["system"]["irr"][I]
names = {b["k"]: b["he"] for b in BB["banks"]}
big5 = ["hapoalim", "leumi", "discount", "mizrahi", "fibi"]
LO = min(big5, key=lambda b: BB["rate"][b]["irr"][I]); HI = max(big5, key=lambda b: BB["rate"][b]["irr"][I])
med = D["homes"]["medians"]; TLV = med["city"]["תל אביב יפו"]["r4"]
FM = D["flows"]["months"][-1]; LOANS = D["flows"]["series"]["loans"]["v"][-1]; VOL = D["flows"]["series"]["volume_k"]["v"][-1] * 1000

def schedule():
    """Yearly Spitzer schedule of 1,000,000 ILS over 25 years, each track amortized on its own at its average effective rate."""
    tot = sum(BB["mix"]["system"][t][I] for t in TR); rows = []
    bal = {t: 1e6 * BB["mix"]["system"][t][I] / tot for t in TR}
    r = {t: eff(BB["rate"]["system"][t][I]) for t in TR}
    m = {t: pmt(bal[t], r[t], 300) for t in TR}
    for y in range(1, 26):
        pi = pr = 0.0
        for _ in range(12):
            for t in TR:
                it = bal[t] * r[t]; p = m[t] - it; bal[t] -= p; pi += it; pr += p
        rows.append((y, pi + pr, pi, pr, max(0.0, sum(bal.values()))))
    return rows
SCH = schedule()
assert abs(SCH[-1][4]) < 1, SCH[-1][4]

# ------------------------------------------------------------------------------------------------ the new text
LEAD_OLD = ('<p class="nlu1-lead">מחשבון משכנתא מחשב את ההחזר החודשי, הריבית וסך התשלומים לפי הסכום, המסלולים והתקופה. הקלידו סכום, בחרו תמהיל או אחד משלושת הסלים האחידים של בנק ישראל, '
            'וראו את ההחזר הראשון, את ההחזר הגבוה הצפוי, והאם הריבית שהבנק הציע לכם גבוהה מהממוצע שבנק ישראל פרסם החודש. כל הנתונים ממקורות רשמיים, עם תאריך.</p>')
LEAD_NEW = ('<p class="nlu1-lead">מחשבון משכנתא מחשב את ההחזר החודשי, הריבית וסך התשלומים לפי הסכום, המסלולים והתקופה, וגם הפוך: לפי ההחזר החודשי שמתאים לכם. '
            'משכנתא של <bdi>1,000,000 ₪</bdi> ל־25 שנה בתמהיל הממוצע של ' + MON + ' עולה <bdi>' + ils(P25) + '</bdi> בחודש הראשון. הקלידו סכום, בחרו תמהיל או אחד משלושת הסלים האחידים של בנק ישראל, '
            'וראו את ההחזר הראשון, את ההחזר הגבוה הצפוי, את לוח הסילוקין, והאם הריבית שהבנק הציע לכם גבוהה מהממוצע שבנק ישראל פרסם החודש. כל הנתונים ממקורות רשמיים, עם תאריך.</p>')
H1_OLD = '<h1 class="wp-block-heading nlseo-h1-v1">מחשבון משכנתא 2026: החזר חודשי ועלות כוללת</h1>'
H1_NEW = '<h1 class="wp-block-heading nlseo-h1-v1">מחשבון משכנתא: חישוב החזר חודשי ועלות כוללת לפי מסלולים</h1>'
EDITS = [  # (old, new): each old string once in the live content, replaced once
    (H1_OLD, H1_NEW),
    (LEAD_OLD, LEAD_NEW),
    ("<h2>ריבית משכנתא ממוצעת לפי מסלול ולפי תקופה</h2>", "<h2>הממוצע החודשי של בנק ישראל לפי מסלול ותקופה</h2>"),
    ("<h2>משכנתא לדירה להשקעה</h2>", "<h2>גם למשקיעים: מה משתנה בחישוב</h2>"),
    ("<h2>שפיצר, קרן שווה, בלון וגרייס</h2>", "<h2>לוח סילוקין למשכנתא: שפיצר, קרן שווה, בלון וגרייס</h2>"),
]

CRUMBS = '[nadlan_crumbs label="מחשבון משכנתא"]\n'
QUICK = '<div id="quick" class="nlu1-anchor"></div>[nadlan_tool id="mquick"]\n'
FULL_OPEN = ('<style id="nlmx-css">.nlmx-fold{margin:12px 0 18px;border:1px solid #D3DCE2;border-radius:6px;background:#fff}'
             '.nlmx-fold>summary{list-style:none;cursor:pointer;min-height:52px;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px;font:600 17px/1.4 "IBM Plex Sans Hebrew",system-ui,sans-serif;color:#1F4B5C}'
             '.nlmx-fold>summary::-webkit-details-marker{display:none}.nlmx-fold>summary::after{content:"";width:10px;height:10px;border-inline-end:2px solid #2F6F86;border-bottom:2px solid #2F6F86;transform:rotate(45deg);flex:0 0 auto;margin-top:-4px}'
             '.nlmx-fold[open]>summary::after{transform:rotate(-135deg);margin-top:4px}.nlmx-fold>summary:focus-visible{outline:2px solid #2F6F86;outline-offset:2px}'
             '.nlmx-fold>summary small{display:block;font-weight:400;font-size:13px;color:#5E6A75}.nlmx-fold[open]{padding-bottom:8px}</style>\n'
             '<details id="mortgage-full" class="nlmx-fold" open><summary><span>המחשבון המלא: מסלולים, תמהילים ולוח סילוקין<small>שלושת הסלים האחידים, ארבעה תמהילים זה לצד זה, פירעון מוקדם והשוואת ההצעה מהבנק</small></span></summary>\n')
FULL_CLOSE = ('</details>\n<script>(function(){var d=document.getElementById("mortgage-full");if(!d)return;var re=/^#(mortgage-tool|bank-offer-check)$/;'
              'document.addEventListener("click",function(e){var a=e.target&&e.target.closest?e.target.closest("a[href]"):null;if(a&&re.test(a.getAttribute("href")))d.open=true;},true);'
              'if(re.test(location.hash))d.open=true;window.addEventListener("load",function(){if(window.matchMedia("(max-width: 899px)").matches&&!re.test(location.hash)){setTimeout(function(){d.open=false;},1500);}});})();</script>\n')
CLASSIC1 = ('<details class="nlmx-fold"><summary><span>המחשבון הקלאסי לפי שלושה מסלולים<small>סכום, ריבית ותקופה לכל מסלול, עם בדיקת עלייה בריבית</small></span></summary>\n', '</details>\n')
CLASSIC2 = ('<details class="nlmx-fold"><summary><span>מחשבון החזר חודשי פשוט<small>סכום, ריבית, תקופה והכנסה: ההחזר, סך הריבית ויחס ההחזר</small></span></summary>\n', '</details>\n')
MARKET = '[nadlan_mortgage_market]\n'

def t_row(r): return ("<tr><th scope=\"row\">" + str(r[0]) + "</th><td class=\"n\">" + ils(r[1]) + "</td><td class=\"n\">" + ils(r[2]) + "</td><td class=\"n\">" + ils(r[3]) + "</td><td class=\"n\">" + ils(r[4]) + "</td></tr>")
SCHED = ('<p>לוח סילוקין של משכנתא של <bdi>1,000,000 ₪</bdi> ל־25 שנה, בתמהיל ובריביות הממוצעים של כל הבנקים ב' + MON + ', בלוח שפיצר: כל מסלול נפרע בהחזר קבוע משלו, ובמסלולים הצמודים בלי שינוי במדד. '
         'בשנה הראשונה משלמים <bdi>' + ils(SCH[0][1]) + '</bdi>, מהם <bdi>' + ils(SCH[0][2]) + '</bdi> ריבית ורק <bdi>' + ils(SCH[0][3]) + '</bdi> קרן; בשנה האחרונה כמעט כל ההחזר הוא קרן. '
         'סך הריבית לאורך כל התקופה: <bdi>' + ils(sum(r[2] for r in SCH)) + '</bdi>.</p>\n'
         '<div class="nlu1-t nlu1-x"><table><caption>לוח סילוקין שנתי: 1,000,000 ₪ ל־25 שנה, תמהיל ממוצע ' + MON + '</caption><thead><tr><th scope="col">שנה</th><th scope="col">החזרים בשנה</th><th scope="col">מזה ריבית</th><th scope="col">מזה קרן</th><th scope="col">יתרה בסוף השנה</th></tr></thead><tbody>'
         + "".join(t_row(r) for r in SCH) + '</tbody></table></div>\n'
         '<p class="nlu1-meta">מקור הריביות והתמהיל: בנק ישראל, השוואת ריביות בהלוואות לדיור (' + MON + '). החישוב שלנו; ההחזר בפועל תלוי בריבית שתקבלו, במדד ובשינויים בפריים. את הלוח החודשי המלא למשכנתא שלכם מציג המחשבון המלא בראש הדף.</p>\n')

MYTHS = ('<section id="mortgage-rules-facts">\n<h2>ארבע טעויות שחוזרות בתשובות על משכנתאות, ומה הכללים אומרים</h2>\n'
         '<p>חלק מהתשובות שרצות ברשת על משכנתאות בישראל מבוססות על כללים שהשתנו. אלה הכללים של הוראה 329 של הפיקוח על הבנקים, בנוסח המעודכן:</p>\n'
         '<h3>שליש בפריים? אין מגבלה כזאת היום</h3>\n<p>אין היום כלל שמגביל את הפריים לשליש מהמשכנתא. הכלל הוא שהחלק בריבית משתנה, הפריים יחד עם שאר המסלולים המשתנים, לא יעלה על <bdi>66.66%</bdi> מההלוואה, כלומר לפחות שליש בריבית קבועה (הוראה 329, סעיף 7).</p>\n'
         '<h3>ההחזר עד 40% מההכנסה? המגבלה היא 50%</h3>\n<p>ההחזר החודשי לא יעלה על <bdi>50%</bdi> מההכנסה הפנויה. מעל <bdi>40%</bdi> הבנק מחזיק יותר הון כנגד ההלוואה, ולכן בפועל רוב המשכנתאות נשארות מתחת: באוגוסט 2026 יחס ההחזר הממוצע במשכנתאות החדשות היה <bdi>29.23%</bdi> (הוראה 329, סעיף 5; בנק ישראל).</p>\n'
         '<h3>משכנתא ל־40 שנה? בבנקים עד 30 שנה</h3>\n<p>התקופה המרבית של הלוואה לדיור בבנק היא <bdi>30</bdi> שנה (הוראה 329, סעיף 8). מי שמחפש החזר נמוך יותר בוחר בתקופה ארוכה עד התקרה הזאת, ומשלם יותר ריבית לאורך הדרך: משכנתא של <bdi>1,000,000 ₪</bdi> ל־30 שנה עולה <bdi>' + ils(P30) + '</bdi> בחודש הראשון, מול <bdi>' + ils(P25) + '</bdi> ל־25 שנה.</p>\n'
         '<h3>תושבי חוץ מקבלים 60%? המימון המרבי הוא 50%</h3>\n<p>מי שאינו תושב ישראל אינו יכול להיחשב רוכש דירה יחידה, ולכן שיעור המימון המרבי שלו הוא <bdi>50%</bdi>, כמו בדירה נוספת. דירה יחידה: עד <bdi>75%</bdi>; דירה חלופית: עד <bdi>70%</bdi> (הוראה 329, סעיף 2 וההגדרות).</p>\n'
         '<p class="nlu1-meta">המקור: הוראת ניהול בנקאי תקין 329, מגבלות למתן הלוואות לדיור, בנק ישראל (נוסח 8.2.2026, עדכון 30.6.2026). נתוני יחס ההחזר: בנק ישראל, סדרות המשכנתאות החדשות.</p>\n</section>\n')

def qa(q, a): return '<h3>' + q + '</h3>\n<p>' + a + '</p>\n'
LO_N, HI_N = names[LO], names[HI]
FAQ_ADD = (
    qa("מה זה לוח סילוקין למשכנתא?", "לוח סילוקין הוא הטבלה של כל ההחזרים לאורך המשכנתא: בכל חודש כמה מההחזר הולך לריבית, כמה לקרן, ומה היתרה שנשארה. בלוח שפיצר ההחזר קבוע והחלק של הקרן גדל עם הזמן. בעמוד הזה יש לוח סילוקין שנתי של משכנתא של 1,000,000 ₪ ל־25 שנה, והמחשבון המלא מציג לוח חודשי למשכנתא שלכם.")
    + qa("איך מחשבים לוח שפיצר?", "ההחזר החודשי בלוח שפיצר הוא הקרן כפול הריבית החודשית, חלקי אחת פחות אחת חלקי אחת ועוד הריבית החודשית בחזקת מספר החודשים. בכל חודש מחשבים את הריבית על היתרה, ומה שנשאר מההחזר מקטין את הקרן. במשכנתא של כמה מסלולים מחשבים כך כל מסלול לבד ומחברים.")
    + qa("מה ההבדל בין הלוואת גרייס להלוואת בלון?", "בגרייס דוחים לתקופה קצרה בתחילת ההלוואה את תשלום הקרן (גרייס חלקי, משלמים רק ריבית) או גם את הריבית (גרייס מלא, הריבית נצברת לקרן), ואחר כך ההלוואה נפרעת בהחזרים רגילים. בבלון לא משלמים קרן לאורך כל התקופה, ולפעמים גם לא ריבית, והכול נפרע בתשלום אחד בסוף.")
    + qa("האם ניתן לקבל משכנתא ל־40 שנה?", "לא בבנק. לפי הוראה 329 התקופה המרבית של הלוואה לדיור היא 30 שנה. משכנתא של 1,000,000 ₪ ל־30 שנה בתמהיל הממוצע של " + MON + " עולה " + ils(P30) + " בחודש הראשון.")
    + qa("האם מותר לקחת יותר משליש מהמשכנתא בפריים?", "כן. אין היום מגבלה של שליש על הפריים. המגבלה היא על כל החלק בריבית משתנה יחד: עד 66.66% מההלוואה, כך שלפחות שליש יהיה בריבית קבועה (הוראה 329, סעיף 7).")
    + qa("באיזה בנק הכי כדאי לקחת משכנתא?", "אין תשובה אחת, כי הריבית נקבעת לכל לקוח לפי הפרופיל שלו. לפי נתוני בנק ישראל ל" + MON + ", הריבית הכוללת החזויה הממוצעת במשכנתאות החדשות הייתה הנמוכה ביותר מבין חמשת הבנקים הגדולים ב" + LO_N + " (" + "{:.2f}%".format(BB["rate"][LO]["irr"][I]) + ") והגבוהה ב" + HI_N + " (" + "{:.2f}%".format(BB["rate"][HI]["irr"][I]) + "). ממוצע של בנק אינו הצעה; הדרך לדעת היא לקבל אישור עקרוני מכמה בנקים ולהשוות את שלושת הסלים האחידים.")
    + qa("כמה עולה משכנתא על דירת 4 חדרים בתל אביב?", "מחיר החציון של דירת 4 חדרים שנמכרה בתל אביב יפו ברבעון " + TLV["quarter"] + " היה " + ils(TLV["median"]) + ". משכנתא של 75% ממנו, " + ils(TLV["median"] * 0.75) + ", ל־25 שנה בתמהיל הממוצע של " + MON + " עולה כ־" + ils(TLV["median"] * 0.75 / 1e6 * P25) + " בחודש הראשון. הטבלה לפי עיר נמצאת בפרק שוק המשכנתאות.")
    + qa("כמה משכנתאות חדשות ניתנו בחודש האחרון בישראל?", "ב" + month(FM) + " הבנקים העמידו " + "{:,.0f}".format(LOANS) + " משכנתאות חדשות בהיקף של " + "{:.2f}".format(VOL / 1e9) + " מיליארד ₪, הלוואה ממוצעת של כ־" + ils(VOL / LOANS) + " (בנק ישראל). הנתונים המלאים מתעדכנים בכל חודש בפרק שוק המשכנתאות.")
)
SEO_TITLE = "מחשבון משכנתא 2026: חישוב החזר חודשי, תמהיל ולוח סילוקין"
SEO_DESC = "מחשבון משכנתא לפי מסלולים: חישוב החזר חודשי, ההחזר הגבוה הצפוי ולוח סילוקין שפיצר, שלושת הסלים של בנק ישראל ובדיקה אם הריבית שהציעו לכם גבוהה מהממוצע החודשי."
INVEST_LINK = '<p>לחישוב המלא של משקיעים, עם מימון של עד 50% ושכר הדירה, יש עמוד נפרד: <a href="/investment-property-mortgage/">משכנתא לדירה להשקעה</a>.</p>\n'

# ------------------------------------------------------------------------------------------------ read the live content
sys.stdout.flush()
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_page"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,title,modified,meta" % PID)
assert s == 200, s
raw = r["content"]["raw"]
new = raw
assert "[nadlan_tool id=\"mquick\"]" not in raw and "[nadlan_mortgage_market]" not in raw, "already written"
for o, n_ in EDITS:
    assert new.count(o) == 1, ("edit anchor", o[:70], new.count(o)); new = new.replace(o, n_)
def ins_before(anchor, text, what):
    global new
    assert new.count(anchor) == 1, (what, new.count(anchor)); new = new.replace(anchor, text + anchor)
def ins_after(anchor, text, what):
    global new
    assert new.count(anchor) == 1, (what, new.count(anchor)); new = new.replace(anchor, anchor + text)
# 1. crumbs at the very top
assert new.startswith("<!-- wp:heading"), new[:60]
new = CRUMBS + new
# 2 + 3. quick tool, then the full tool folded on phones
M_ANCH = '<div id="mortgage-tool" class="nlu1-anchor"></div>[nadlan_tool id="mortgage"]\n'
assert new.count(M_ANCH) == 1, new.count(M_ANCH)
new = new.replace(M_ANCH, QUICK + FULL_OPEN + M_ANCH + FULL_CLOSE)
# 4. the two old calculators, each folded
a = new.index(FULL_CLOSE) + len(FULL_CLOSE)
c1_start = new.index("<style>\n.nlc-calc{", a); c1_end = new.index("</script>", new.index('id="nlc-mortgage"', c1_start)) + len("</script>")
new = new[:c1_start] + CLASSIC1[0] + new[c1_start:c1_end] + "\n" + CLASSIC1[1] + new[c1_end:]
c2_start = new.index('<section class="calc-shell wrap" aria-label="חישוב החזר משכנתא">'); c2_end = new.index("</section>", new.index('id="nmc-stressed"', c2_start)) + len("</section>")
new = new[:c2_start] + CLASSIC2[0] + new[c2_start:c2_end] + "\n" + CLASSIC2[1] + new[c2_end:]
# 5. the market block before the U1 block
ins_before('<div class="wrap nlu1">', MARKET, "U1 block")
# 6. the schedule at the end of the Spitzer section
sp = new.index("<h2>לוח סילוקין למשכנתא: שפיצר, קרן שווה, בלון וגרייס</h2>"); sp_end = new.index("</section>", sp)
new = new[:sp_end] + SCHED + new[sp_end:]
# 7. the rules facts after the section on what the BoI allows
rl = new.index("<h2>מה בנק ישראל מתיר: מימון, החזר מהכנסה, תמהיל ותקופה</h2>"); rl_end = new.index("</section>", rl) + len("</section>")
new = new[:rl_end] + "\n" + MYTHS + new[rl_end:]
# the investors note links the owner page with its exact words
iv = new.index("<h2>גם למשקיעים: מה משתנה בחישוב</h2>"); iv_end = new.index("</section>", iv)
new = new[:iv_end] + INVEST_LINK + new[iv_end:]
# 8. FAQ
fq = new.index('<section id="faq">'); fq_end = new.index("</section>", fq)
old_q = set(re.sub(r"<[^>]+>", "", q).strip() for q in re.findall(r"<h3[^>]*>(.*?)</h3>", new[fq:fq_end]))
new_q = [re.sub(r"<[^>]+>", "", q).strip() for q in re.findall(r"<h3>(.*?)</h3>", FAQ_ADD)]
assert not (set(new_q) & old_q), set(new_q) & old_q
new = new[:fq_end] + FAQ_ADD + new[fq_end:]
# the U1 "updated" date
n_upd = new.count("עודכן 26.10.2026")
new = new.replace("עודכן 26.10.2026", "עודכן " + UPDATED)

# ------------------------------------------------------------------------------------------------ checks
EDIT_OLD = [o for o, _ in EDITS]
for line in raw.split("\n"):  # additive: every original line survives (the edited ones in their edited form)
    if not line.strip():
        continue
    ln = line
    for o, n_ in EDITS:
        ln = ln.replace(o, n_)
    ln = ln.replace("עודכן 26.10.2026", "עודכן " + UPDATED)
    assert ln in new, ("an original line is missing", line[:90])
assert new.count("<h1") == 1
order = [new.index(x) for x in ("[nadlan_crumbs", "<h1 ", 'class="nlu1-lead"', 'class="nlu1-cta"', '[nadlan_tool id="mquick"]', 'id="mortgage-full"', '[nadlan_tool id="mortgage"]',
                                'id="nlc-mortgage"', 'id="nmc-loan"', "[nadlan_mortgage_market]", '<div class="wrap nlu1">', 'id="mortgage-rules-facts"', '<section id="faq">')]
assert order == sorted(order), ("content order", order)
def visible(h):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", h, flags=re.S); h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    h = re.sub(r"\[[a-z_]+[^\]]*\]", " ", h); h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", h.replace("&nbsp;", " "))
ADDED = LEAD_NEW + H1_NEW + FULL_OPEN + CLASSIC1[0] + CLASSIC2[0] + SCHED + MYTHS + FAQ_ADD + INVEST_LINK + "".join(n_ for _, n_ in EDITS)
v = visible(ADDED)
BANNED = r"ממשק|מערכת|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה|נדלן חכם|Nadlan|מנגנון|מודל|הדגמה|טכנולוגי|אלגוריתם|PMT|אטלס|Atlas|\bדמו\b"
assert not re.search(r"[–—]", v), "long dash"
assert not re.search(r"(?:^|\s)-{1,3}(?:\s|$)|--", v), "spaced hyphen"
m_ = re.search(BANNED, v); assert not m_, ("banned word", m_.group(0) if m_ else "")
assert '"' not in v and "..." not in v, "ASCII quote or ellipsis in new visible text"
faq_n = len(re.findall(r"<h3[^>]*>.*?</h3>\s*<p", new[new.index('<section id="faq">'):new.index("</section>", new.index('<section id="faq">'))], flags=re.S))
assert faq_n == 38, faq_n
print("[page %d] %s | modified %s | edits %d + U1 date x%d | FAQ %d | new visible words %d | schedule rows %d | first-year payment %s"
      % (PID, r["link"], r["modified"], len(EDITS), n_upd, faq_n, len(v.split()), len(SCH), ils(SCH[0][1])))
print("[seo] title", len(SEO_TITLE), SEO_TITLE, "| desc", len(SEO_DESC))
if DRY:
    io.open(os.path.join(H, "preview-content.html"), "w", encoding="utf-8", newline="").write(new)
    print("[dry] nothing written; preview-content.html")
    sys.exit(0)

# ------------------------------------------------------------------------------------------------ live write
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
stamp = time.strftime("%Y%m%d-%H%M%S")
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, stamp)), "w", encoding="utf-8", newline="").write(raw)
meta = r.get("meta") or {}
io.open(os.path.join(bk, "page-%d-meta-%s.json" % (PID, stamp)), "w", encoding="utf-8").write(json.dumps({k: meta.get(k) for k in ("_yoast_wpseo_title", "_yoast_wpseo_metadesc")}, ensure_ascii=False))
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new, "meta": {"_yoast_wpseo_title": SEO_TITLE, "_yoast_wpseo_metadesc": SEO_DESC}})
assert s2 in (200, 201), s2
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,meta" % PID)[1]
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
ok = {"read-back": back["content"]["raw"].strip() == new.strip(), "yoast title saved": (back.get("meta") or {}).get("_yoast_wpseo_title") == SEO_TITLE,
      "<title>": "<title>" + SEO_TITLE in page, "one h1": bd.count("<h1") == 1, "h1 text": "מחשבון משכנתא: חישוב החזר חודשי ועלות כוללת לפי מסלולים" in bd,
      "crumbs visible": 'class="nlbc nlbc--page"' in bd, "BreadcrumbList": '"@type":"BreadcrumbList"' in page, "mquick mounted": 'data-nli="mquick"' in bd,
      "mquick.js enqueued": "tools/mquick.js" in page, "mortgage tool kept": 'data-nli="mortgage"' in bd, "market block": 'id="mortgage-market"' in bd,
      "Dataset": '"@type":"Dataset"' in page, "one FAQPage": page.count('"@type":"FAQPage"') == 1, "38 questions": page.count('"@type":"Question"') == 38,
      "old calculators kept": 'id="nlc-mortgage"' in bd and 'id="nmc-loan"' in bd, "schedule": "לוח סילוקין שנתי" in bd, "rules facts": 'id="mortgage-rules-facts"' in bd}
for k, v_ in ok.items(): print("   ", "OK " if v_ else "BAD", k)
print("ALL OK" if all(ok.values()) else "SOME CHECKS FAILED: the backup is in page-backup/")
