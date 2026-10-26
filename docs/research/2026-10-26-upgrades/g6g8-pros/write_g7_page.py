# -*- coding: utf-8 -*-
"""G7 on /real-estate-appraiser/ (page 86): the owner page of "שמאי מקרקעין" (2,400 searches a month, KD 12, CPC $9.95; also
"שמאות מקרקעין" 2,400 and "שמאי" 2,400; not seen in Search Console in 90 days) and of the fee intents ("כמה עולה שמאי", "שמאי מקרקעין
מחיר"). Spec: dna.md (this folder). NOT RUN against the site by the research session (Ben, 26.10.2026: local only).

What it does (every number from data/shamai.json, built by tools/instruments/build_pros_data.py from the Appraisers Law, the
planning law, the 2009 fee regulations, the Ministry of Justice register and exam file on data.gov.il, Kol Zchut on bank appraisals
and the published price pages, all checked against the raw texts):
  1. the H1 (the hero h2, printed as the page's h1 by the theme) with the head term first, the WP title, Yoast title and description;
  2. inside the hero, right under the H1: the answer paragraph and three CTAs; after the hero: [nadlan_tool id="shamai"] and T1;
  3. new sections before named old headings: which appraisal (I1, T2), the bank's appraiser (T3), every published price (T4),
     the betterment levy, the decisive appraiser and section 197 (T5, I3, T6), how to check a licence with the live register
     search [nadlan_tool id="shamaireg"] and how to complain, the road to a licence (I2, T7);
  4. the FAQ heading becomes an h2 (so the FAQPage schema can be built), 20 new FAQ after the 4 old ones = 24, the next block's
     h3 becomes an h2 (so it is not read as a question), an English section and the method line;
Each anchor must match exactly once. Language law on the new visible text; internal links must answer 200 without a redirect.
  python write_g7_page.py --dry   public REST only: writes preview/g7-page-content.html, preview/g7-page-render.html, page-sources-g7.md
  python write_g7_page.py         backup, POST, read-back, live check (BLOCKED below until Ben's word)
  --style                          also the style-only reform of the old gold eyebrow and cream notice (Ben's word)"""
import io, json, os, re, sys, time, urllib.parse, urllib.request

H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from g6g8_common import *  # noqa: E402,F401
import infographics as ig  # noqa: E402

DRY = "--dry" in sys.argv; STYLE = "--style" in sys.argv
PID = 86; PFX = "nlsm"
H1_OLD = "שמאי מקרקעין עוזר להבין כמה הנכס באמת שווה, ומה עלול להשפיע על העסקה"
H1_NEW = "שמאי מקרקעין: מתי צריך, כמה זה עולה ואיך בודקים שהוא מורשה"
TITLE = H1_NEW
SEO_T = "שמאי מקרקעין: מחירים 2026, סוגי שומה ובדיקת רישיון"
SEO_D = "שמאי מקרקעין: איזו שומה צריך (בנק, לפני קנייה, היטל השבחה, ירושה), מי משלם, מחירים שפורסמו, המועדים בחוק, ובדיקה בפנקס של 3,182 שמאים מורשים."
assert len(SEO_T) <= 60 and len(SEO_D) <= 160, (len(SEO_T), len(SEO_D))
tbl = Tables(PFX)
WA_T = wa_link("שלום, הגעתי מהמדריך לשמאי מקרקעין באתר נדלן ואשמח לפרטים נוספים")
R_ = SH["register"]; EX = SH["exams"]; DC = SH["decisive"]
SRCN = {k: v["label"].split(" (")[0].split(",")[0] for k, v in SH["sources"].items()}


def env(keys):
    lo, hi = [], []
    for s in SH["prices"]:
        for r in s["rows"]:
            if r[0] in keys: lo.append(r[2]); hi.append(r[3])
    return min(lo), max(hi)


def dfee(a):
    f = sum((min(a, hi or 1e18) - lo) * r for lo, hi, r in DC["table"] if a > lo)
    return max(DC["min"], min(DC["max"], f))


APT = env(["apt"]); HOUSE = env(["house"]); FIN = [x for x in EX["rows"] if x[0] == EX["final"]][0]


def same(name, got, want): assert got == want, ("cross-check", name, got, want)
same("register", R_["count"], 3182); same("apartment", APT, (2000, 5400)); same("house", HOUSE, (2500, 7000)); same("final 2025", FIN[2], [674, 322])
same("decisive 800k", dfee(800000), 21000); same("decisive 1M", dfee(1000000), 25000); same("decisive 2M", dfee(2000000), 35000); same("decisive 5M", dfee(5000000), 50000)

# ------------------------------------------------------------------ TOP: answer + CTAs inside the hero; tool + T1 after it
ANSWER = ('<p class="%s-lead">שמאי מקרקעין הוא מי שרשום בפנקס שמאי המקרקעין: רק הוא רשאי לעשות שומת מקרקעין בשכר, ורק שומה שלו מוגשת לבית משפט. בפנקס רשומים היום %s שמאים. '
          'שומה לדירה בבניין פורסמה ב-%s עד %s ₪ ולבית פרטי ב-%s עד %s ₪; למשכנתא מזמינים שמאי מרשימת הבנק ומשלמים לפי תעריף הבנק, ועל דרישת היטל השבחה אפשר לערור בתוך 45 ימים.</p>\n'
          % (PFX, num(R_["count"]), num(APT[0]), num(APT[1]), num(HOUSE[0]), num(HOUSE[1])) +
          '<div class="%s-cta"><a class="%s-go" href="#shamai-tool">איזו שומה אתם צריכים</a><a href="%s" target="_blank" rel="noopener">לקבלת פרטים נוספים בוואטסאפ</a><a href="#shamai-check">בדיקת שמאי בפנקס</a></div>\n' % (PFX, PFX, WA_T))
T1 = tbl("שמאי מקרקעין במספרים (נבדק 26.10.2026)", ["מה", "המספר", "מקור"], [
    ["שמאים מורשים בפנקס", num(R_["count"]), "משרד המשפטים, data.gov.il, %s" % dmy(R_["updated"])],
    ["תנאי הרישום", "תואר אקדמי, בחינות, התמחות שנה במשרה מלאה או שנתיים בחצי משרה, בחינה מסכמת", "חוק שמאי מקרקעין, סעיף 7"],
    ["ציון עובר בבחינות", str(EX["pass"]), "תקנות שמאי מקרקעין (בחינות)"],
    ["הבחינה המסכמת ב-2025", "עברו %s מתוך %s נבחנים (%s)" % (num(FIN[2][1]), num(FIN[2][0]), pct(FIN[2][1] / FIN[2][0], 0)), "קובץ ציוני הבחינות, %s" % dmy(EX["updated"])],
    ["שומה בשכר בלי רישום", "אסורה; מי שמתחזה לשמאי: עד שנת מאסר", "סעיף 13"],
    ["שמאי הבנק למשכנתא", "מרשימת הבנק, לפי תעריף הבנק; העתק לכם; שימוש בבנק אחר בתוך 90 יום", "כל זכות, לפי נהלי בנק ישראל"],
    ["ערר על היטל השבחה", "45 ימים מהיום שהשומה הובאה לידיעתכם", "התוספת השלישית לחוק התכנון והבניה, סעיף 14"],
    ["תביעה על תכנית שפגעה בשווי", "3 שנים מתחילת תוקף התכנית", "חוק התכנון והבניה, סעיף 197"],
    ["שכר שמאי מכריע", "3% עד 500 אלף, 2% עד מיליון, 1% עד 2 מיליון, 0.5% מעל; מינימום " + num(DC["min"]) + ", תקרה " + num(DC["max"]) + ", ועוד מע״מ", "תקנות שכר שמאי מכריע, 2009"],
    ["שומה לדירה בבניין, מחירים שפורסמו", "%s עד %s ₪" % (num(APT[0]), num(APT[1])), "מידרג 2024, EC 2025, דפי זהב 2026"],
], minw=600)
TOOL = (css(PFX, guide=True) + (reform_css(PFX) if STYLE else "") +
        '<div class="%s-tool" id="shamai-tool">[nadlan_tool id="shamai"]</div>\n' % PFX + T1)

# ------------------------------------------------------------------ S_NEED (before "מתי כדאי להזמין שמאי לפני קניית דירה?"): which appraisal
rows2 = []
for p in SH["purposes"]:
    pr = None
    if p["price"]:
        pr = env(p["price"]) if any(r[0] in p["price"] for s in SH["prices"] for r in s["rows"]) else None
    d = p["deadline"]
    rows2.append([p["label"], p["who"], p["pay"], ("%d ימים" % d["days"]) if d and d.get("days") else ("%d שנים" % d["years"]) if d else "אין", ("%s עד %s ₪" % (num(pr[0]), num(pr[1]))) if pr else "לפי ההסכם או התעריף"])
T2 = tbl("איזו שומה צריך: מי מזמין, מי משלם, מה המועד", ["מטרה", "מי מזמין", "מי משלם", "מועד בחוק", "מחירים שפורסמו"], rows2, minw=760)
S_NEED = ('<h2>איזו שומה צריך: 8 מטרות, מי מזמין ומי משלם</h2>\n'
          '<p>"שמאי מקרקעין" הוא מקצוע אחד, אבל השומה משתנה לפי המטרה: שומה לבנק נועדה להגן על הבנק, שומה לפני חתימה נועדה להגן עליכם, ושומה נגדית להיטל השבחה היא מסמך במחלוקת מול הוועדה המקומית. '
          'מי שמזמין את השמאי, מי שמשלם לו והמועד שהחוק קובע שונים בכל מקרה. בכלי למעלה בוחרים את המטרה ורואים את המועד לפי התאריך שלכם.</p>\n' +
          fig(PFX, ig.g7_purposes(), "שמונה מטרות של שומה: מי מזמין, מי משלם, ומועד בחוק כשיש. המקורות: חוק שמאי מקרקעין, חוק התכנון והבניה, נהלי בנק ישראל כפי שמסכם כל זכות.") + T2)

# ------------------------------------------------------------------ S_BANK (before "שמאי ומשכנתא: למה לפעמים נוצרים פערים?"): the bank's appraiser
T3 = tbl("שמאי הבנק למשכנתא: מה הכללים", ["נושא", "הכלל"], [
    ["מי בוחר", "הבנק מוסר רשימת שמאים מאושרים עם האישור העקרוני; בוחרים אחד מהם ופונים אליו בעצמכם"],
    ["מי משלם", "אתם, ישירות לשמאי, לפי תעריפי הבנק"],
    ["לאן הולכת השומה", "השמאי מעביר אותה לבנק; מי ששילם זכאי לקבל העתק"],
    ["בנק אחר", "אפשר להגיש את אותה שומה לבנק אחר בתוך 90 יום מיום השומה"],
    ["שומה פרטית", "הבנק מקבל רק שומה של שמאי מהרשימה שלו"],
    ["ערעור", "ככלל אין; כשהשומה נמוכה באופן משמעותי מהמחיר או מדירות דומות, אפשר לבקש שומה נוספת מטעם הבנק"],
    ["פטור משומה", "הבנק רשאי לוותר, למשל בדירה חדשה מקבלן שעובד עם בנק מלווה או במימון נמוך"],
], minw=520)
S_BANK = ('<h2>שמאי הבנק למשכנתא: מי בוחר, מי משלם ומה עושים כשהשומה נמוכה</h2>\n'
          '<p>הבנק מממן לפי השווי שהשמאי שלו קובע, לא לפי המחיר שסיכמתם. כשהשומה נמוכה מהמחיר, ההפרש יוצא מההון העצמי שלכם. לכן מי שקונה עם משכנתא גבוהה מזמין לעיתים שומה פרטית לפני החתימה, '
          'ובמקביל מבקש מהבנק את רשימת השמאים מוקדם. הכללים לפי נהלי בנק ישראל, כפי שמסכם אותם אתר כל זכות:</p>\n' + T3 +
          '<p>שומת בנק נמוכה: בודקים את הסיבה (עסקאות השוואה, חריגת בנייה, רישום), משווים לעסקאות שנסגרו ב<a href="/property-value-estimator/">מחשבון שווי דירה</a>, ושוקלים בנק אחר בתוך 90 יום. '
          'כמה הבנק יממן לפי השווי: <a href="/mortgage-calculator/">מחשבון משכנתא</a>.</p>\n')

# ------------------------------------------------------------------ S_PRICE (before "כמה עולה שמאי מקרקעין ומה משפיע על המחיר?"): every published price
rows4 = []
for s in SH["prices"]:
    for r in s["rows"]:
        rows4.append([SRCN[s["src"]], r[1], "%s עד %s ₪" % (num(r[2]), num(r[3])) if r[3] > r[2] else "%s ₪" % num(r[2]), dmy(s["date"])])
T4 = tbl("כל המחירים שפורסמו לשמאי מקרקעין, מקור אחר מקור", ["מקור", "סוג השומה", "מחיר", "פורסם"], rows4, minw=600,
         note="אף אחד מהמקורות לא כתב אם המחיר כולל מע״מ. דפי זהב מפרסם טווחים שנראים כמחיר עגול כפול 1.08.")
S_PRICE = ('<h2>כמה עולה שמאי מקרקעין: כל המחירים שפורסמו</h2>\n'
           '<p>אין תעריף רשמי לשומה פרטית; יש מחירים שפורסמו. ריכזנו את כולם בטבלה אחת עם התאריך, וממנה נבנה הטווח בכלי: שומה לדירה בבניין %s עד %s ₪, לבית פרטי %s עד %s ₪, '
           'וחוות דעת לבית משפט מוסיפה לפי מידרג 1,500 עד 2,000 ₪ על השומה הרגילה. שומה נגדית להיטל השבחה מתומחרת לרוב כשכר קבוע ועוד 10%% מההפחתה שהשמאי השיג.</p>\n' % (num(APT[0]), num(APT[1]), num(HOUSE[0]), num(HOUSE[1])) + T4)

# ------------------------------------------------------------------ S_LEVY (before "שמאי בהתחדשות עירונית ובנכסים מורכבים"): levy, decisive appraiser, s.197
T5 = tbl("קיבלתם דרישת היטל השבחה: שלוש הדרכים", ["הדרך", "מתי", "מי מכריע", "מה עולה"], [
    ["בחינה חוזרת בוועדה", "חיוב עד 90,000 ₪, כשלא חולקים על עצם החיוב", "שמאי מטעם הוועדה, בתוך 14 ימים", "ללא שכר שמאי מכריע"],
    ["שמאי מכריע", "בתוך 45 ימים, כשלא חולקים על עצם החיוב אלא על הגובה", "שמאי מכריע מהרשימה; היושב ראש ממנה בתוך 15 ימים", "לפי התקנות, חצי לכל צד, ועוד מע״מ"],
    ["ערר לוועדת הערר", "בתוך 45 ימים, גם על עצם החיוב", "ועדת הערר לפיצויים ולהיטל השבחה, לעיתים עם שמאי מייעץ", "לפי ההליך; שכר שמאי מייעץ לפי אותן תקנות"],
    ["ערר על השמאי המכריע", "בתוך 45 ימים מההחלטה", "ועדת הערר", ""],
], minw=640, note="התוספת השלישית לחוק התכנון והבניה, סעיף 14. על לוח שומה: ערר בתוך שנה מהצגתו. יושבי הראש רשאים להאריך מועדים מטעמים מיוחדים.")
T6 = tbl("שכר שמאי מכריע לפי סכום ההשבחה שבבקשה", ["סכום ההשבחה", "השכר לפני מע״מ", "עם מע״מ 18%", "החלק שלכם, עם מע״מ"],
         [[ils(a), ils(dfee(a)), ils(dfee(a) * 1.18), ils(dfee(a) * 0.5 * 1.18)] for a in (50000, 500000, 1000000, 2000000, 5000000, 20000000)], minw=520, num_cols=True)
S_LEVY = ('<h2>היטל השבחה: 45 ימים, ערר או שמאי מכריע</h2>\n'
          '<p>היטל השבחה הוא מחצית מעליית השווי שתכנית, הקלה או שימוש חורג יצרו, והוועדה המקומית קובעת אותו לפי שומה של השמאי שלה. מי שחולק על הגובה מזמין שומה נגדית משמאי מטעמו, ואז יש לו 45 ימים מהיום שהשומה הובאה לידיעתו. '
          'הבחירה בין הדרכים תלויה בשאלה אם אתם חולקים על עצם החיוב או רק על הסכום.</p>\n' + T5 +
          '<h3>כמה עולה שמאי מכריע</h3>\n'
          '<p>שכר השמאי המכריע קבוע בתקנות ונגזר מסכום ההשבחה שבבקשה: 3%% על 500 אלף השקלים הראשונים, 2%% עד מיליון, 1%% עד 2 מיליון ו-0.5%% מעל, לא פחות מ-%s ₪ ולא יותר מ-%s ₪ למחלוקת, ועוד מע״מ. '
          'המבקש והוועדה המקומית משלמים כל אחד מחצית, והשמאי רשאי לדרוש רבע מהשכר עם המינוי. את הבקשה מגישים ל<a href="https://www.gov.il/he/departments/units/decisive_appraisal" target="_blank" rel="noopener">יחידת השמאות המכריעה במשרד המשפטים</a>. השמאי המכריע רשאי לחלק אחרת, למשל כשהתוצאה מובהקת לטובת צד. על המונח עצמו: <a href="/glossary/%%D7%%A9%%D7%%9E%%D7%%90%%D7%%99-%%D7%%9E%%D7%%9B%%D7%%A8%%D7%%99%%D7%%A2/">שמאי מכריע</a>.</p>\n'
          % (num(DC["min"]), num(DC["max"])) +
          fig(PFX, ig.g7_decisive(), "שכר שמאי מכריע לפי סכום ההשבחה שבבקשה, לפני מע״מ; הקו המקווקו הוא החלק של כל צד. לפי תקנות התכנון והבניה (שכרו של שמאי מכריע ושמאי מייעץ), התשס״ט-2009.") + T6 +
          '<h3>תכנית שפגעה בשווי: תביעה לפי סעיף 197</h3>\n'
          '<p>בעל זכות במקרקעין שנפגעו מתכנית, בתחומה או בגבולה, זכאי לפיצוי מהוועדה המקומית. התביעה מוגשת תוך 3 שנים מיום תחילת תוקף התכנית, ומצרפים אליה שומה של שמאי מקרקעין. '
          'כשהוועדה מחליטה על סכום אחר, אפשר לפנות בהסכמה לשמאי מכריע בתוך 45 ימים. מי שקיבל דרישה או רוצה לערור: <a href="/real-estate-tax-advisor/betterment-levy-appeal/">ערר על היטל השבחה</a>.</p>\n'
          '<p>בפינוי בינוי, כשבעלי יותר משתי חמישיות מהדירות בכל בניין מבקשים, הרשות להתחדשות עירונית ממנה שמאי לבדיקת הכדאיות בחינם; ושמאי בעלי הדירות משולם בדרך כלל בידי היזם. '
          'הפירוט: <a href="/glossary/shamai-pinui-binui/">שמאי פינוי בינוי</a> ו<a href="/urban-renewal/pinui-binui/">פינוי בינוי</a>.</p>\n')

# ------------------------------------------------------------------ S_CHECK (before "סימני אזהרה לפני שמזמינים שומה"): the register, complaints
S_CHECK = ('<h2 id="shamai-check">איך בודקים שהשמאי מורשה, ואיך מגישים תלונה</h2>\n'
           '<p>לפי החוק, "שמאי מקרקעין" הוא מי שרשום בפנקס. חברות בלשכת שמאי המקרקעין היא חברות בארגון מקצועי, ולא רישיון. החיפוש כאן נשלח ישירות ל<a href="' + R_["page"] + '" target="_blank" rel="noopener">מאגר שמאי המקרקעין של משרד המשפטים</a> ברגע שאתם מחפשים: '
           'שם, מספר רישיון, ועיר כשהיא רשומה.</p>\n' +
           '<div class="%s-tool">[nadlan_tool id="shamaireg"]</div>\n' % PFX +
           '<p>שמאי רשום אינו רשאי לעבוד במקרה שיש בו ניגוד בין העניין שלו לעניין שלכם (סעיף 14). תלונה על שמאי נבדקת בידי תובע שמונה לפי החוק, וקובלנה נדונה בוועדת משמעת שבראשה מי שכשיר להיות שופט; '
           'מי שתלונתו לא הובילה לקובלנה רשאי לערור למועצת שמאי המקרקעין בתוך 30 ימים (סעיפים 17, 22, 23).</p>\n')

# ------------------------------------------------------------------ S_EXAMS (before "שאלות שכדאי לשאול על הסביבה והעיר"): the road to a licence
EXN = {"מבוא לתורת השמאות": "מבוא לתורת השמאות", "דינים": "דינים", "יסודות הכלכלה חלק א - מיקרו כלכלה ומקרו כלכלה": "כלכלה: מיקרו ומאקרו", "יסודות הכלכלה חלק ב - כלכלה עירונית": "כלכלה עירונית",
       "יסודות בחשבונאות וניתוח דוחות כספיים": "חשבונאות וניתוח דוחות", "יסודות המימון ושימושם בשומת המקרקעין": "מימון בשומת מקרקעין", "סטטיסטיקה": "סטטיסטיקה", "יסודות הנדסת בנין והנדסה אזרחית": "הנדסת בניין",
       "יסודות מדידה ומיפוי": "מדידה ומיפוי", "תכנון ובניה חלק א - יסודות התכנון העירוני": "תכנון ובנייה א: יסודות", "תכנון ובניה חלק ב - דיני התכנון העירוני": "תכנון ובנייה ב: הדינים",
       "מיסוי מקרקעין ומסים אחרים": "מיסוי מקרקעין", "גישות ועקרונות בהערכת מקרקעין": "גישות בהערכת מקרקעין", "יישומים בשומת מקרקעין": "יישומים בשומת מקרקעין (מסכמת)"}
T7 = tbl("הבחינות של שמאי המקרקעין: נבחנים ועוברים (ציון 60 ומעלה)", ["בחינה", "2024: נבחנו", "עברו", "2025: נבחנו", "עברו"],
         [[EXN[e], num(a[0]), pct(a[1] / a[0], 0) if a[0] else "", num(b[0]), pct(b[1] / b[0], 0) if b[0] else ""] for e, a, b in EX["rows"]], minw=560, num_cols=True,
         note="כל ניסיון נספר, כולל נבחנים חוזרים. המקור: קובץ ציוני הבחינות של משרד המשפטים ב-data.gov.il, %s שורות, עודכן %s." % (num(EX["n_rows"]), dmy(EX["updated"])))
S_EXAMS = ('<h2>הדרך לרישיון: הבחינות, ההתמחות ומי עובר</h2>\n'
           '<p>כדי להירשם בפנקס צריך תואר אקדמי, לעבור את בחינות המועצה, להתמחות שנה במשרה של 40 שעות בשבוע או שנתיים בחצי משרה, ולעבור בחינה מסכמת. משרד המשפטים מפרסם את ציוני כל הבחינות, '
           'והם מראים כמה המסלול סלקטיבי: בבחינה המסכמת, "יישומים בשומת מקרקעין", עברו ב-2025 %s מהנבחנים.</p>\n' % pct(FIN[2][1] / FIN[2][0], 0) +
           fig(PFX, ig.g7_exams(), "שיעור העוברים בכל בחינה ב-2025, ציון 60 ומעלה. המקור: קובץ ציוני הבחינות של משרד המשפטים, data.gov.il.") + T7)

# ------------------------------------------------------------------ FAQ: 20 new after the 4 old
FAQ_NEW = [
    ("כמה עולה שמאי מקרקעין?", "לפי המחירים שפורסמו: שומה לדירה בבניין %s עד %s ₪, לבית פרטי %s עד %s ₪, לדמי שכירות 1,944 עד 4,320 ₪, ושעת ייעוץ 216 עד 540 ₪. אף מקור לא ציין אם המע״מ כלול." % (num(APT[0]), num(APT[1]), num(HOUSE[0]), num(HOUSE[1]))),
    ("כמה עולה שמאי לדירה לפני קנייה?", "שומה פרטית לדירה בבניין פורסמה ב-%s עד %s ₪, ודירה גדולה או פנטהאוז ב-2,500 עד 3,500 ₪. זו שומה שלכם, והיא לא מחליפה את שמאי הבנק אם לוקחים משכנתא." % (num(APT[0]), num(APT[1]))),
    ("כמה עולה שמאי מהבנק?", "לפי תעריף הבנק. מבקש המשכנתא משלם ישירות לשמאי שבחר מתוך רשימת הבנק, והתעריף נקבע לפי סוג הנכס, הגודל והמיקום."),
    ("מי בוחר את השמאי של הבנק?", "אתם, מתוך רשימת השמאים המאושרים שהבנק מוסר עם האישור העקרוני. הבנק מקבל רק שומה של שמאי מהרשימה שלו."),
    ("אפשר להשתמש בשומה של בנק אחד בבנק אחר?", "כן, אם לא עברו 90 יום מיום השומה. מי ששילם על השומה זכאי לקבל העתק שלה מהבנק."),
    ("אפשר לערער על שומת הבנק?", "ככלל לא. כשהשומה נמוכה באופן משמעותי ממחיר הקנייה או ממחירי דירות דומות, אפשר לבקש שומה נוספת מטעם הבנק."),
    ("מה עושים כששומת הבנק נמוכה ממחיר הקנייה?", "בודקים את הסיבה, משווים לעסקאות שנסגרו, מבקשים שומה נוספת כשהפער משמעותי, שוקלים בנק אחר בתוך 90 יום, ומתכננים הון עצמי גדול יותר. לפני החתימה, שומה פרטית מראה את הפער מראש."),
    ("איך בודקים שהשמאי מורשה?", "בפנקס שמאי המקרקעין של משרד המשפטים: בחיפוש בעמוד הזה לפי שם או מספר רישיון, או ישירות במאגר ב-data.gov.il. בפנקס %s שמאים." % num(R_["count"])),
    ("מה ההבדל בין מועצת שמאי המקרקעין ללשכת שמאי המקרקעין?", "המועצה הוקמה בחוק: היא עורכת את הבחינות, ויושב הראש שלה מנהל את הפנקס. הלשכה היא ארגון של שמאים. חברות בלשכה אינה רישיון; הרישום בפנקס הוא הרישיון."),
    ("כמה זמן יש לערער על היטל השבחה?", "45 ימים מהיום שהשומה הובאה לידיעתכם, לערר לוועדת הערר או לבקשה למינוי שמאי מכריע. על לוח שומה: שנה מהצגתו. יושבי הראש רשאים להאריך מטעמים מיוחדים."),
    ("כמה עולה שמאי מכריע?", "לפי התקנות: 3%% על 500 אלף השקלים הראשונים של ההשבחה, 2%% עד מיליון, 1%% עד 2 מיליון ו-0.5%% מעל, לפחות %s ₪ ולכל היותר %s ₪, ועוד מע״מ; כל צד משלם מחצית. על השבחה של מיליון: %s ₪." % (num(DC["min"]), num(DC["max"]), num(dfee(1000000)))),
    ("מה זה שמאי מייעץ?", "שמאי שוועדת הערר לפיצויים ולהיטל השבחה מבקשת למנות כדי שיגיש לה חוות דעת בכתב בערר. השכר שלו נקבע לפי אותן תקנות של השמאי המכריע."),
    ("מה זו תביעה לפי סעיף 197?", "תביעת פיצוי מהוועדה המקומית על מקרקעין שנפגעו מתכנית, בתחומה או בגבולה. מגישים תוך 3 שנים מתחילת תוקף התכנית, עם שומה של שמאי מקרקעין."),
    ("מי משלם לשמאי בפינוי בינוי?", "במבנה עסקה מקובל היזם משלם לאנשי המקצוע של בעלי הדירות. בנוסף, כשבעלי יותר משתי חמישיות מהדירות בכל בניין מבקשים, הרשות להתחדשות עירונית ממנה שמאי בחינם."),
    ("האם שומה פרטית לפני קנייה מחייבת את הבנק?", "לא. הבנק מקבל רק שומה של שמאי מהרשימה שלו. השומה הפרטית נועדה לכם: לבדוק את המחיר ואת הסיכונים לפני שחותמים."),
    ("איך שמאי מעריך דירה?", "בדירת מגורים בעיקר לפי השוואה לעסקאות שנסגרו באותו אזור, עם התאמות לקומה, לשטח, לחניה, למצב ולזכויות. בנכס מניב גם לפי ההכנסה, ובנכס חדש או ייחודי גם לפי העלות."),
    ("האם צריך שמאי רשום לבית משפט בירושה או בגירושין?", "כן. שומת מקרקעין מוגשת לבית משפט רק אם נערכה בידי שמאי מקרקעין רשום (סעיף 12 לחוק)."),
    ("כמה עוברים את בחינות השמאים?", "תלוי בבחינה: ב-2025 עברו %s בבחינה המסכמת, ובבחינות אחרות בין רבע לתשעה עשיריות מהנבחנים. ציון עובר: 60." % pct(FIN[2][1] / FIN[2][0], 0)),
    ("האם השמאי מייצג אותי או את הבנק?", "שמאי הבנק עובד בשביל הבנק, גם כשאתם משלמים לו. שמאי שהזמנתם עובד בשבילכם. החוק אוסר על שמאי לעבוד במקרה שיש בו ניגוד עניינים עם הלקוח."),
    ("האם מחיר השמאי כולל מע״מ?", "באף אחד מהמקורות שבדקנו לא נכתב. שאלו לפני ההזמנה, ובקשו הצעה כתובה שמפרטת מה כלול: ביקור בנכס, בדיקת מסמכים, דוח ושיחת הסבר."),
]
FAQ_NEW = [(q, a.replace("%%", "%")) for q, a in FAQ_NEW]
assert len(FAQ_NEW) == 20

# ------------------------------------------------------------------ English + method
EN = ('<section class="%s-en" lang="en" dir="ltr">\n<h2>Real estate appraiser in Israel (shamai mekarkein): fees, bank appraisals and licence checks</h2>\n'
      '<p>Only an appraiser registered in the Ministry of Justice register may value real estate for a fee, and only such an appraisal can be filed in court; %s appraisers are registered (25 Oct 2026). '
      'Published fees: %s to %s NIS for an apartment and %s to %s NIS for a house (none of the sources says whether VAT is included).</p>\n'
      '<p>For a mortgage, the bank gives you a list of approved appraisers; you pay the appraiser by the bank\'s tariff, you are entitled to a copy, and another bank may use it within 90 days. '
      'A betterment levy (hetel hashbacha) can be disputed within 45 days, before an appeals committee or a decisive appraiser whose fee is fixed by regulation (3%% of the first 500,000 NIS of the increase, down to 0.5%%, min 2,000 and max 100,000 NIS plus VAT, split between the sides). '
      'Check any appraiser by name or licence number in the official register search above.</p>\n</section>\n'
      % (PFX, num(R_["count"]), num(APT[0]), num(APT[1]), num(HOUSE[0]), num(HOUSE[1])))
METHOD = ('<p class="%s-note">עודכן %s. החוק והתקנות בנוסחם היום; הפנקס וציוני הבחינות מ-data.gov.il; כללי שמאות הבנק לפי כל זכות; המחירים כפי שפורסמו במידרג (7.2024), ב-EC שמאות (8.2025) ובדפי זהב (9.2026). '
          'המידע כללי ואינו חוות דעת שמאית או ייעוץ משפטי.</p>\n' % (PFX, UPDATED))

# ------------------------------------------------------------------ the live content, the anchors
req, raw, r = get_live(PID, DRY)
FAQ_LAST = "בנכס מסחרי, בית פרטי, קרקע או פרויקט התחדשות עירונית נדרש לעיתים זמן רב יותר.</p>"
R = [
    (H1_OLD + "</h2>", H1_NEW + "</h2>\n" + ANSWER),
    ('<section class="quick" aria-label="בדיקות מרכזיות">', TOOL + '<section class="quick" aria-label="בדיקות מרכזיות">'),
    (before_block(raw, "מתי כדאי להזמין שמאי לפני קניית דירה?"), None),
    (before_block(raw, "שמאי ומשכנתא: למה לפעמים נוצרים פערים?"), None),
    (before_block(raw, "כמה עולה שמאי מקרקעין ומה משפיע על המחיר?"), None),
    (before_block(raw, "שמאי בהתחדשות עירונית ובנכסים מורכבים"), None),
    (before_block(raw, "סימני אזהרה לפני שמזמינים שומה"), None),
    (before_block(raw, "שאלות שכדאי לשאול על הסביבה והעיר"), None),
    ("<h3>שאלות נפוצות</h3>", "<h2>שאלות נפוצות על שמאי מקרקעין</h2>"),
    (FAQ_LAST, FAQ_LAST + "\n" + faq(FAQ_NEW)),
    ("<h3>המשך בדיקה לפני החלטה</h3>", "<h2>המשך בדיקה לפני החלטה</h2>"),
]
for i, sec in zip(range(2, 8), (S_NEED, S_BANK, S_PRICE, S_LEVY, S_CHECK, S_EXAMS)): R[i] = (R[i][0], sec + R[i][0])
new = apply(raw, R) + "\n" + EN + METHOD
NEWS = [ANSWER, TOOL, S_NEED, S_BANK, S_PRICE, S_LEVY, S_CHECK, S_EXAMS, faq(FAQ_NEW), EN, METHOD]
print("[page %d] live content modified %s, %d chars; %d anchors matched once each (%s)" % (PID, r.get("modified"), len(raw), len(R), "public REST, rendered" if DRY else "raw"))
qs = gates("".join(NEWS), new, 4 + 20)
inner, bad, offi = check_links("".join(NEWS))
assert not bad, ("internal links must answer 200", bad)
c_all, c_old = counts(new), counts(raw)
print("  page now: %s | before: %s" % (json.dumps(c_all, ensure_ascii=False), json.dumps(c_old, ensure_ascii=False)))
print("  FAQ %d (4 old + 20 new); internal links %d all 200; external: %s" % (len(qs), len(inner), ", ".join("%s %s" % (h.split("/")[2], st) for h, st in offi)))
print("  H1 %d chars, SEO title %d, description %d; language gates passed; svg text >= 12px" % (len(H1_NEW), len(SEO_T), len(SEO_D)))

SRC = """# /real-estate-appraiser/ (page 86): where every fact on the page comes from (internal, written by write_g7_page.py, %s)

| Fact | Source |
|---|---|
| Appraiser = registered; degree, exams, internship 1 year at 40 h or 2 years at 20 h, final exam; court filing only by a registered appraiser; fee work only by registered; impersonation 1 year; conflict of interest; complaints (prosecutor, discipline committee, 30-day appeal to the council) | חוק שמאי מקרקעין, התשס"א-2001, ss. 1, 2, 7, 12, 13, 14, 17, 22, 23 (Wikisource, read 26.10.2026) |
| Pass mark 60 | תקנות שמאי מקרקעין (בחינות), התשס"ו-2006, reg. 7(ב) |
| 3,182 licensed, 376 with a city | data.gov.il dataset shamaim, resource 8540534a-..., updated 25.10.2026 (API 26.10.2026) |
| Exam pass rates 2024-2025 (93,728 rows) | data.gov.il shamaim, resource 8b7f49b2-... (updated 1.10.2026), our count of score >= 60 |
| Bank appraisal rules (list, tariff, copy, 90 days, no private, second appraisal, waiver) | kolzchut.org.il "הערכת שמאי למשכנתא" (updated 2.3.2025), citing Bank of Israel housing-loan rules ss. 9-10 |
| Levy: 45 days, decisive appraiser named in 15 days, up to 90,000 re-examination in 14 days, one year on a schedule, appeal on the decisive appraiser 45 days | חוק התכנון והבניה, Third Schedule s.14 (Wikisource) |
| Section 197: 3 years; decisive appraiser by consent in 45 days | חוק התכנון והבניה s.197 and s.198 |
| Decisive appraiser fee table, min 2,000, max 100,000, half each, a quarter on appointment, VAT | תקנות התכנון והבניה (שכרו של שמאי מכריע ושמאי מייעץ), התשס"ט-2009, regs. 2, 5, 6, 7, 9 and the schedule |
| Free authority appraiser in pinui binui (more than two fifths in every building) | pinui.json (G2), from the Pinui Binui law s.2א and gov.il |
| Published prices | midrag.co.il/Content/Price/8151 (3.7.2024); ec-shamaut.co.il (24.8.2025); d.co.il/priceList-49080 (data 9.2026); read 26.10.2026 |
""" % UPDATED
io.open(os.path.join(H, "page-sources-g7.md"), "w", encoding="utf-8").write(SRC)

if DRY:
    pv = os.path.join(H, "preview"); os.makedirs(pv, exist_ok=True)
    io.open(os.path.join(pv, "g7-page-content.html"), "w", encoding="utf-8", newline="").write(new)
    render_shell(os.path.join(pv, "g7-page-render.html"), "/real-estate-appraiser/", "", new.replace("<h2>%s</h2>" % H1_NEW, '<h1 class="nl-h1-from-h2">%s</h1>' % H1_NEW, 1), ["shamai", "shamaireg"])
    print("  --dry: wrote preview/g7-page-content.html, preview/g7-page-render.html, page-sources-g7.md; nothing was posted")
    sys.exit(0)

bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw + "\n<!-- title " + repr((r.get("title") or {}).get("raw")) + " | meta " + repr((r.get("meta") or {}).get("_yoast_wpseo_title")) + " | " + repr((r.get("meta") or {}).get("_yoast_wpseo_metadesc")) + " -->")
req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new, "title": TITLE, "meta": {"_yoast_wpseo_title": SEO_T, "_yoast_wpseo_metadesc": SEO_D}})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,title" % PID)[1]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers=UA), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
title = re.search(r"<title>(.*?)</title>", page, re.S).group(1).strip()
ok = {"read-back": back["content"]["raw"].strip() == new.strip(), "one h1": bd.count("<h1") == 1, "h1 text": H1_NEW in bd, "tools mounted": 'data-nli="shamai"' in bd and 'data-nli="shamaireg"' in bd,
      "shortcode rendered": "[nadlan_tool" not in bd, "svg x3": bd.count("%s-fig" % PFX) == 3, "one FAQPage": page.count('"@type":"FAQPage"') == 1, "24 questions": page.count('"@type":"Question"') == 24,
      "SoftwareApplication": '"@type":"SoftwareApplication"' in page, "shamai.js enqueued": "tools/shamai.js" in page, "SEO title": title.startswith(SEO_T), "updated": ("עודכן %s" % UPDATED) in bd}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
