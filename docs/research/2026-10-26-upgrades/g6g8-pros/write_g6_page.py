# -*- coding: utf-8 -*-
"""G6 on /home-inspection/ (page 90): the owner page of "בדק בית" (2,900 searches a month, KD 2, CPC $16.57; not seen in Search
Console in 90 days) and of its price intents ("בדק בית מחיר" 390, "כמה עולה בדק בית" 140). Spec: dna.md (this folder), sections 4
(verified facts), 5 (gaps) and 6 (build spec). NOT RUN against the site by the research session (Ben, 26.10.2026: local only).

What it does (every number from plugins/nadlan-config/assets/instruments/data/bedek.json, built and checked against the law text
and the published price pages by tools/instruments/build_pros_data.py):
  1. WP title (the H1 of this template) "בדק בית: מה בודקים, כמה זה עולה ועד מתי הקבלן אחראי", Yoast title and description;
  2. TOP, before the old first paragraph: the answer paragraph (head term first), three CTAs, [nadlan_tool id="bedek"], T1;
  3. new sections at exact anchors (before the named old heading): what is checked part by part (T3), the law's periods (I1, T2,
     the rules of notice, proof and repair, the sub-buyer), second-hand against new (T6), the inspection calendar (I3, T5), every
     published price (I2, T4), the letter to the contractor, how to choose and what the report must hold (T7);
  4. 20 new FAQ after the 5 old ones = 25, an English section and the method line "עודכן 26.10.2026";
  5. honesty fixes in the old text (R_FIX): the unsourced "1,200 עד 2,600" price line becomes the dated published range, and the
     "עודכן ונבדק" date.
Each anchor must match exactly once. Language law on the new visible text (incl. SVG text and aria labels); every internal link
must answer 200 without a redirect.
  python write_g6_page.py --dry   public REST only (no login): anchors checked against the live rendered content; writes
                                  preview/g6-page-content.html, preview/g6-page-render.html and page-sources-g6.md
  python write_g6_page.py         backup, POST, read-back, live check (BLOCKED below until Ben's word)"""
import io, json, os, re, sys, time, urllib.parse, urllib.request

H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from g6g8_common import *  # noqa: E402,F401
import infographics as ig  # noqa: E402

DRY = "--dry" in sys.argv
PID = 90; PFX = "nlbd"
TITLE = "בדק בית: מה בודקים, כמה זה עולה ועד מתי הקבלן אחראי"
SEO_T = "בדק בית: מחירים 2026, מה בודקים ועד מתי הקבלן אחראי"
SEO_D = "בדק בית לדירה חדשה מקבלן וליד שנייה: מחירים שפורסמו ב-2026 לפי סוג הנכס, מה בודקים, איך בוחרים מהנדס, ותקופות הבדק והאחריות לפי חוק המכר."
OLD_TITLE = "בדק בית לפני קניית דירה: מה בודקים ואיך משתמשים בדוח"
assert len(SEO_T) <= 60 and len(SEO_D) <= 160, (len(SEO_T), len(SEO_D))
L = BD["law"]; tbl = Tables(PFX)
WA_T = wa_link("שלום, הגעתי מהמדריך לבדק בית באתר נדלן ואשמח לפרטים נוספים")
SRCN = {k: v["label"].split(" (")[0].split(",")[0] for k, v in BD["sources"].items()}


def env(kind, rooms=None):
    lo, hi, n = [], [], 0
    for s in BD["prices"]:
        for r in s["rows"]:
            if r[0] != kind: continue
            if rooms is not None and r[4] and not any(r[4][0] <= k <= r[4][1] for k in rooms): continue
            lo.append(r[2]); hi.append(r[3]); n += 1
    return min(lo), max(hi), n


A35 = env("apt", [3, 4, 5]); HOUSE = env("house"); A6 = env("apt", [6]); COURT = env("court"); ROOF = env("roof"); MOIST = env("moist"); VILLA = env("villa")
SHR = BD["shared"]; ADD = BD["addon_roof"]; GRP = BD["group"]


def same(name, got, want): assert got == want, ("cross-check", name, got, want)
same("apartment 3-5 rooms", A35[:2], (1100, 2500)); same("house", HOUSE[:2], (1947, 6000)); same("court", COURT[:2], (2500, 10000))
same("schedule", [x["y"] for x in L["items"]], [2, 2, 3, 3, 3, 4, 4, 5, 7, 1]); same("warranty", L["warranty_y"], 3); same("struct", L["struct_y"], 20)

YRS = lambda y: "שנה" if y == 1 else "%d שנים" % y

# ------------------------------------------------------------------ TOP: answer, CTAs, tool, T1
T1 = tbl("בדק בית במספרים (נבדק 26.10.2026)", ["מה", "המספר", "מקור ותאריך"], [
    ["תקופת בדק לפי חוק המכר (דירות)", "שנה עד 7 שנים, לפי 10 סוגי ליקויים", "התוספת לחוק"],
    ["תקופת אחריות", "3 שנים מסוף כל תקופת בדק", "סעיף 4 לחוק"],
    ["ליקוי יסודי בשלד וביציבות", "20 שנה מיום המסירה", "סעיף 4 לחוק"],
    ["הודעה על ליקוי שנראה כבר במסירה", "בתוך שנה מהמסירה", "סעיף 4א לחוק"],
    ["דירה עד 120 מ״ר", "1,200 עד 1,900 ₪ כולל מע״מ", "מידרג, 17.12.2025"],
    ["בית פרטי: ממוצע ששולם", "2,516 ₪ כולל מע״מ; 84% שילמו פחות מ-2,900 ₪", "מידרג, 13.7.2025"],
    ["רכוש משותף של בניין", "%s ₪ לדירה ועוד מע״מ, מינימום %s ₪" % (num(SHR["per_apt"]), num(SHR["min"])), "מידרג, 17.12.2025"],
    ["חוות דעת לבית משפט", "%s עד %s ₪" % (num(COURT[0]), num(COURT[1])), "בדק מבנים, 12.1.2026"],
    ["מי בודק", "מהנדס או הנדסאי בניין; בודקים רישום בפנקס המהנדסים והאדריכלים", '<a href="%s" target="_blank" rel="noopener">משרד העבודה</a>' % BD["sources"]["ENG"]["url"]],
], minw=560)

TOP = (css(PFX) +
       '<p class="%s-lead">בדק בית הוא בדיקה הנדסית של דירה או בית: לפני שקונים יד שנייה, ביום המסירה מהקבלן ולפני שתקופת הבדק נגמרת. בסופה מקבלים דוח ליקויים עם תמונות, מיקום ואומדן לתיקון. '
       'לפי המחירים שפורסמו ב-2025 וב-2026, בדק בית לדירה של 3 עד 5 חדרים עולה %s עד %s ₪, ולבית פרטי עד 200 מ״ר %s עד %s ₪. בדירה חדשה, חוק המכר (דירות) נותן לכל סוג ליקוי תקופת בדק של שנה עד 7 שנים מיום המסירה, '
       'ועוד 3 שנות אחריות אחריה; לליקוי בשלד: 20 שנה.</p>\n' % (PFX, num(A35[0]), num(A35[1]), num(HOUSE[0]), num(HOUSE[1])) +
       '<div class="%s-cta"><a class="%s-go" href="#bedek-tool">בדקו עד מתי הקבלן אחראי</a><a href="%s" target="_blank" rel="noopener">לקבלת פרטים נוספים בוואטסאפ</a><a href="#bedek-prices">כל המחירים שפורסמו</a></div>\n' % (PFX, PFX, WA_T) +
       '<div class="%s-tool" id="bedek-tool">[nadlan_tool id="bedek"]</div>\n' % PFX + T1)

# ------------------------------------------------------------------ S_CHECK (before "מתי עושים בדק בית?"): what is checked, part by part
T3 = tbl("מה בודקים בבדק בית, חלק אחר חלק", ["חלק בדירה", "מה הבודק עושה", "בעזרת מה", "תקופת הבדק בחוק"], [
    ["איטום ורטיבות", "קירות חוץ, תקרות, חדרים רטובים, מרפסות וגג; הצפה מבוקרת במרפסות ובגג שטוח", "מד לחות, מצלמה תרמית", "4 שנים"],
    ["צנרת, ביוב ומרזבים", "לחץ וספיקת מים, נזילות, ניקוז כיורים, מקלחות ואסלות", "מד לחץ, מצלמה תרמית", "4 שנים"],
    ["חשמל", "לוח החשמל, מפסק הפחת, הארקה, שקעים ונקודות מול המפרט", "בודק הארקה ופחת", "שנה"],
    ["ריצוף וחיפוי פנים", "אריחים חלולים, שקיעות, שיפועים לניקוז, רובה", "פטיש בדיקה, פלס", "שנתיים"],
    ["חלונות, תריסים ודלתות", "אטימות, סגירה ונעילה, עובי הזכוכית", "מד עובי זכוכית", "שנתיים"],
    ["סדקים", "רוחב הסדק, האם הוא פעיל, האם הוא ברכיב נושא", "מד סדקים", "5 שנים מעל 1.5 מ״מ; בשלד 20 שנה"],
    ["טיח וצבע", "סדקים, התקלפות, אחידות הגמר", "פנס ועין מקצועית", "שנה"],
    ["חיפוי חוץ", "אבנים רופפות, התנתקות, התפוררות", "בדיקה מקרוב, לעיתים רחפן", "7 שנים"],
    ["דוד ומכונות", "חימום, נזילות, חיבורים", "בדיקת תפקוד", "3 שנים"],
    ["בידוד תרמי", "הפרשי חום בקירות ובגג", "מצלמה תרמית", "3 שנים"],
    ["חצר, חניה ומחסן", "שקיעות, ניקוז, מרצפות בקומת הקרקע", "פלס", "3 שנים"],
    ["ממ״ד", "סגירת הדלת והחלון, אטימות, אמצעי הסינון", "בדיקת תפקוד", "לפי סוג הליקוי בתוספת"],
    ["מעקות ומרפסות", "גובה ויציבות המעקה, שיפוע לניקוז", "מטר ופלס", "לפי סוג הליקוי בתוספת"],
    ["התאמה למפרט ולתוכנית", "שטחי החדרים, מיקום נקודות, החומרים שהובטחו", "מד לייזר", "כל סטייה מהמפרט, מתקן רשמי או מתקנות הבנייה"],
], minw=640)
S_CHECK = ('<h2>מה בודקים בבדק בית, חלק אחר חלק</h2>\n'
           '<p>בדק בית טוב עובר על כל חלק בדירה עם כלי מדידה, ולא רק במבט. הטבלה מסדרת את החלקים לפי מה שהבודק עושה, הכלי שהוא מביא, ותקופת הבדק שחוק המכר (דירות) נותן לאותו חלק בדירה חדשה. '
           'כך הדוח הופך לרשימת פעולה: ליד כל ליקוי רואים עד מתי אפשר לדרוש תיקון מהקבלן.</p>\n' + T3 +
           '<p>החוק עצמו קובע מה נחשב ליקוי: דירה שונה מהמפרט, מתקן רשמי או מתקנות הבנייה היא אי התאמה, בלי קשר לתקופה (סעיף 4(א)(1)). לכן בודק טוב מצטט את המפרט ואת התקן, '
           'למשל <a href="/glossary/%D7%AA%D7%99-466/">ת״י 466</a> לבטון, ולא רק כותב "ליקוי". גם הוראות תחזוקה ושימוש: מוכר שלא מסר אותן לא קיים את חיוביו (סעיף 4(א)(6)).</p>\n')

# ------------------------------------------------------------------ S_LAW (before "בדק בית לדירה יד שנייה"): the periods, the rules
T2 = tbl("תקופות הבדק והאחריות לפי חוק המכר (דירות)", ["סוג הליקוי (נוסח התוספת)", "תקופת בדק", "אחריות אחריה", "הקבלן אחראי בסך הכול", "מזמינים בדיקה לפני"], [
    [it["law"], YRS(it["y"]), "3 שנים", "%d שנים" % (it["y"] + 3), "סוף שנה %d מהמסירה" % it["y"] if it["y"] > 1 else "סוף השנה הראשונה"] for it in L["items"]
] + [["אי התאמה יסודית: חלקי הבניין הנושאים, היציבות והבטיחות", "20 שנה", "", "20 שנה, ואחריהן אם תוכיחו את המקור", "כל סימן לכשל"]], minw=680)
S_LAW = ('<h2>בדק בית לפי חוק המכר: תקופות הבדק והאחריות</h2>\n'
         '<p>בדירה חדשה מקבלן, "שנת בדק" היא רק אחת מעשר תקופות. חוק המכר (דירות) קובע לכל סוג ליקוי תקופת בדק משלו, שמתחילה ביום שבו הדירה הועמדה לרשות הקונה: שנה לכל ליקוי שאינו ברשימה, '
         'שנתיים לחלונות ולריצוף, 3 שנים לדודים, לחצר ולבידוד, 4 שנים לצנרת ולאיטום, 5 שנים לסדקים ו-7 שנים לחיפוי חוץ. אחרי כל תקופה מתחילות 3 שנות אחריות.</p>\n' +
         fig(PFX, ig.g6_periods(), "תקופת הבדק לכל סוג ליקוי, ועוד 3 שנות אחריות. המקור: התוספת לחוק המכר (דירות), התשל״ג-1973.") + T2 +
         '<h3>מה ההבדל בין תקופת בדק לתקופת אחריות</h3>\n'
         '<p>בתקופת הבדק, ליקוי שהתגלה הוא באחריות הקבלן, אלא אם הקבלן יוכיח שהוא נגרם בגללכם (סעיף 4(א)(2)). בתקופת האחריות הקבלן עדיין אחראי, אבל עכשיו אתם צריכים להוכיח שמקור הליקוי בתכנון, בעבודה או בחומרים (סעיף 4(א)(3)). '
         'בפועל: דוח בדק בית שנעשה לפני סוף תקופת הבדק חוסך את הוויכוח על נטל ההוכחה.</p>\n'
         '<h3>עד מתי מודיעים לקבלן</h3>\n'
         '<p>ליקוי שאפשר היה לראות ביום המסירה: הודעה לקבלן בתוך שנה מהמסירה (סעיף 4א(א)(1)). ליקוי שלא היה אפשר לגלות כשבדקתם את הדירה במסירה: תוך זמן סביר אחרי שגיליתם אותו. '
         'לכן רושמים בפרוטוקול המסירה כל מה שנראה, ושולחים מכתב מסודר לפני שהשנה נגמרת על כל מה שלא תוקן.</p>\n'
         '<h3>תיקון: מה הקבלן חייב ומתי מותר לתקן לבד</h3>\n'
         '<p>הקונה צריך לתת לקבלן הזדמנות נאותה לתקן, והקבלן חייב לתקן תוך זמן סביר (סעיף 4ב(א)). אם הליקוי חזר אחרי שהקבלן תיקן אותו, בתוך שנתיים מההודעה שלכם, או שהתיקון דחוף והקבלן לא תיקן בזמן סביר, '
         'מותר לכם לתקן והקבלן יישא בהוצאות (סעיף 4ב(ב)). אם הגעתם לשלב של תביעה, המדריך ל<a href="/real-estate-lawyer/construction-defects-lawsuit/">תביעת ליקויי בנייה</a> מסביר את השלבים.</p>\n'
         '<div class="%s-box">קונים דירה בת שנתיים או שלוש מבעלים פרטיים? החוק נותן גם ל"קונה משנה" את תקופות הבדק והאחריות, והן נספרות מהיום שבו הדירה נמסרה לקונה הראשון. '
         'כלפי הקבלן הן ממשיכות לרוץ גם אחרי שהדירה עברה ידיים. כלפי המוכר הפרטי חל החוזה שלכם איתו.</div>\n' % PFX)

# ------------------------------------------------------------------ S_TWO (before "בדק בית לדירה חדשה מקבלן"): second-hand against new
T6 = tbl("דירה חדשה מקבלן מול יד שנייה: מה שונה בבדק הבית", ["נושא", "דירה חדשה מקבלן", "יד שנייה מבעלים פרטיים"], [
    ["מה מגן עליכם", "חוק המכר (דירות): תקופות בדק ואחריות, תיקון על חשבון הקבלן", "החוזה עם המוכר; הרבה חוזים קובעים מכירה במצבה"],
    ["מתי בודקים", "לפני המסירה, ושוב לפני סוף כל תקופת בדק", "לפני החתימה על זיכרון דברים או חוזה"],
    ["מה עושים עם הממצאים", "פרוטוקול מסירה ומכתב לקבלן", "משא ומתן על המחיר, תיקון לפני המסירה או סעיף בחוזה"],
    ["דירה צעירה, עד 7 שנים מהמסירה", "", "תקופות הבדק של הקבלן ממשיכות לרוץ לכם כקונה משנה"],
    ["מה בודקים במיוחד", "התאמה למפרט, ממ״ד, איטום מרפסות, ריצוף", "רטיבות חוזרת, צנרת ישנה, חשמל, תיקונים שנצבעו"],
    ["מסמכים לבודק", "מפרט, תוכנית מכר, פרוטוקול מסירה", "תוכנית הדירה, פרטי שיפוצים, היתר אם יש"],
], minw=600)
S_TWO = ('<h2>בדק בית ליד שנייה מול דירה חדשה: מה ההבדל</h2>\n'
         '<p>הבדיקה ההנדסית דומה, אבל מה שעושים עם הדוח שונה. בדירה מקבלן הדוח הוא הבסיס לדרישת תיקון לפי החוק. ביד שנייה הדוח הוא כלי למשא ומתן לפני שחותמים, כי אחרי החתימה רוב החוזים מעבירים את הסיכון אליכם.</p>\n' + T6)

# ------------------------------------------------------------------ S_CAL (before "מה בודקים בבדק בית?"): the inspection calendar
T5 = tbl("לוח הבדיקות בדירה חדשה מקבלן", ["שלב", "מתי", "מה בודקים", "מה שולחים"], [
    ["פרוטוקול מסירה", "לפני קבלת המפתח", "כל ליקוי גלוי והתאמה למפרט", "רישום בפרוטוקול, עותק אצלכם"],
    ["סוף השנה הראשונה", "כחודש וחצי לפני", "כל ליקוי שאינו ברשימה: חשמל, טיח, צבע, ארונות; ומה שנרשם במסירה ולא תוקן", "מכתב לקבלן עם הדוח"],
    ["סוף שנתיים", "כחודש וחצי לפני", "חלונות, דלתות, אלומיניום, ריצוף וחיפוי פנים", "מכתב לקבלן"],
    ["סוף 3 שנים", "כחודש וחצי לפני", "דודים ומכונות, חצר וחניה, בידוד תרמי", "מכתב לקבלן"],
    ["סוף 4 שנים", "כחודש וחצי לפני", "צנרת, ביוב, איטום ורטיבות", "מכתב לקבלן"],
    ["סוף 5 שנים", "כחודש וחצי לפני", "סדקים מעל 1.5 מ״מ בקירות שאינם נושאים", "מכתב לקבלן"],
    ["סוף 7 שנים", "כחודש וחצי לפני", "חיפוי חוץ שמתנתק או מתפורר (בדרך כלל דרך נציגות הבית)", "מכתב לקבלן"],
    ["עד 20 שנה", "בכל סימן", "שלד ויציבות", "בדיקת מהנדס קונסטרוקציה ומכתב"],
], minw=620)
S_CAL = ('<h2>מתי לעשות בדק בית בדירה חדשה: הלוח מהמסירה ועד השנה השביעית</h2>\n'
         '<p>מי שעושה בדק בית רק ביום המסירה מפספס את רוב הזכויות. ליקויי רטיבות וצנרת מופיעים לרוב אחרי חורף או שניים, ולכן החוק נותן להם 4 שנים. הלוח הזה מראה מתי כל תקופה נגמרת, '
         'ומתי כדאי להזמין בודק כדי שהדוח והמכתב לקבלן יגיעו בזמן. בכלי למעלה, בלשונית "לוח הבדיקות", מקבלים את התאריכים המדויקים לפי יום המסירה שלכם.</p>\n' +
         fig(PFX, ig.g6_calendar(), "מתי להזמין בדיקה: 45 יום לפני סוף כל תקופת בדק (ההצעה שלנו). המועדים לפי התוספת לחוק המכר (דירות).") + T5)

# ------------------------------------------------------------------ S_PRICE (before "ליקויים נפוצים שמגלים לפני קנייה"): every published price
rows4 = []
for s in BD["prices"]:
    for r in s["rows"]:
        rows4.append([SRCN[s["src"]], r[1], ("%s עד %s ₪" % (num(r[2]), num(r[3]))) if r[3] > r[2] else "%s ₪" % num(r[2]), {"incl": "כולל", "plus": "ועוד מע״מ", "ns": "לא צוין"}[s["vat"]], dmy(s["date"])])
rows4.append([SRCN[SHR["src"]], "רכוש משותף: לכל דירה, מינימום %s ₪ לבניין" % num(SHR["min"]), "%s ₪" % num(SHR["per_apt"]), "ועוד מע״מ", dmy(SHR["date"])])
rows4.append([SRCN[ADD["src"]], "תוספת לבדיקת גג או גינה בדירה", "%s עד %s ₪" % (num(ADD["lo"]), num(ADD["hi"])), "לא צוין", dmy(ADD["date"])])
rows4.append([SRCN[GRP["src"]], "קבוצה של 10 דירות ומעלה: לכל דירה", "%s עד %s ₪" % (num(GRP["lo"]), num(GRP["hi"])), "לא צוין", dmy(GRP["date"])])
T4 = tbl("כל המחירים שפורסמו לבדק בית, מקור אחר מקור", ["מקור", "מה כלול", "מחיר", "מע״מ", "פורסם"], rows4, minw=640)
S_PRICE = ('<h2 id="bedek-prices">כמה עולה בדק בית: כל המחירים שפורסמו ב-2025 וב-2026</h2>\n'
           '<p>אין מחירון רשמי לבדק בית. מה שיש הוא מחירים שפרסמו אתר ההשוואה מידרג (כולל מחירים שלקוחות דיווחו ששילמו) ומשרדי בדק בית, כל אחד בתאריך אחר, וחלקם בלי לומר אם המע״מ כלול. '
           'ריכזנו את כולם בטבלה אחת, עם התאריך ומצב המע״מ של כל מחיר, וממנה נבנה הטווח שבכלי.</p>\n' +
           fig(PFX, ig.g6_prices(), "הטווח לכל סוג נכס: המחיר הנמוך והגבוה מבין המחירים שפורסמו. מידרג כולל מע״מ; בדק מבנים והבודקים לא ציינו.") + T4 +
           '<h3>מה מייקר בדק בית</h3>\n'
           '<p>הגודל וסוג הנכס קובעים את רוב המחיר: דירת 4 חדרים עולה %s עד %s ₪ לפי המקורות, דירה של 6 חדרים ומעלה %s עד %s ₪, פנטהאוז או דופלקס %s עד %s ₪ (מקור אחד), ובית פרטי עד 200 מ״ר %s עד %s ₪. '
           'גג או גינה צמודים מוסיפים לפי מידרג %s עד %s ₪ (מחיר מ-2022). בדיקת רטיבות ותרמוגרפיה בלבד, בלי בדק בית מלא, פורסמה ב-%s עד %s ₪. חוות דעת לבית משפט נכתבת אחרת ועולה %s עד %s ₪.</p>\n'
           % (num(env("apt", [4])[0]), num(env("apt", [4])[1]), num(A6[0]), num(A6[1]), num(ROOF[0]), num(ROOF[1]), num(HOUSE[0]), num(HOUSE[1]), num(ADD["lo"]), num(ADD["hi"]), num(MOIST[0]), num(MOIST[1]), num(COURT[0]), num(COURT[1])) +
           '<h3>איך מוזילים בלי לוותר על הבדיקה</h3>\n'
           '<p>קבוצה: כשעשר דירות ומעלה באותו פרויקט מזמינות בודק אחד, מידרג פרסם מחיר של %s עד %s ₪ לדירה, והבודקים מציעים לקבוצות רוכשים עד 15%% הנחה. רכוש משותף: הזמנה דרך נציגות הבית, '
           'לפי מידרג %s ₪ לדירה ועוד מע״מ עם מינימום של %s ₪ לבניין, כך שבבניין של 24 דירות זה %s ₪ ועוד מע״מ לכל הבניין. בכלי, בלשונית "כמה זה עולה", מחשבים את זה לבניין שלכם.</p>\n'
           % (num(GRP["lo"]), num(GRP["hi"]), num(SHR["per_apt"]), num(SHR["min"]), num(max(SHR["min"], 24 * SHR["per_apt"]))))

# ------------------------------------------------------------------ S_LETTER (before "איך בוחרים מהנדס או חברת בדק בית?"): what to do with the report
S_LETTER = ('<h2>אחרי הדוח: המכתב לקבלן, צעד אחר צעד</h2>\n'
            '<p>דוח שנשאר במגירה לא מתקן דבר. בדירה מקבלן, ההודעה בכתב היא מה שמפעיל את חובת התיקון ואת השעון של סעיף 4ב. כך עושים את זה:</p>\n'
            '<ol>\n<li>שולחים לקבלן מכתב בדואר רשום או בדואר אלקטרוני עם אישור קבלה, ומצרפים את הדוח והתמונות.</li>\n'
            '<li>כותבים את יום המסירה, ולכל ליקוי את סוגו לפי התוספת לחוק, כדי שיהיה ברור שהוא בתוך תקופת הבדק או האחריות.</li>\n'
            '<li>מבקשים מועד לתיקון ונותנים לקבלן הזדמנות נאותה לבצע אותו.</li>\n'
            '<li>אחרי התיקון בודקים שוב. ליקוי שחזר בתוך שנתיים מההודעה מאפשר לתקן על חשבון הקבלן.</li>\n'
            '<li>שומרים כל מכתב, אישור ותשובה. אם הקבלן מסרב, פונים ל<a href="/real-estate-lawyer/">עורך דין מקרקעין</a> עם התיק המלא.</li>\n</ol>\n'
            '<p>ביד שנייה הסדר הפוך: הדוח מגיע לפני החתימה, והוא חומר למשא ומתן. ליקוי מהותי נכנס לחוזה כתיקון שהמוכר מבצע לפני המסירה, כהפחתה במחיר או כסכום שנשאר בנאמנות. '
            'אם הליקוי פוגע בשווי, <a href="/real-estate-appraiser/">שמאי מקרקעין</a> יכול להעריך את ירידת הערך.</p>\n')

# ------------------------------------------------------------------ S_CHOOSE (before the checklist heading): how to choose, what the report must hold
T7 = tbl("מה צריך להיות בדוח בדק בית", ["פריט בדוח", "למה זה חשוב"], [
    ["שם הבודק, השכלתו ומספר הרישום", "כדי שאפשר יהיה לבדוק אותו ולהסתמך עליו מול הקבלן"],
    ["תאריך הבדיקה ויום המסירה", "כדי לשייך כל ליקוי לתקופת הבדק או האחריות"],
    ["כל ליקוי עם מיקום ותמונה", "כדי שהקבלן לא יטען שאינו מבין מה לתקן"],
    ["הדרישה שהליקוי סוטה ממנה", "מפרט, תקן רשמי או תקנות הבנייה, כמו שהחוק מגדיר אי התאמה"],
    ["חומרה ודחיפות", "בטיחות קודם, אחר כך רטיבות ותפקוד, ובסוף מראה"],
    ["אומדן עלות לתיקון", "בסיס למשא ומתן ביד שנייה ולדרישה מהקבלן"],
    ["תדפיסי מכשירים", "מד לחות ומצלמה תרמית: ראיה ולא רק התרשמות"],
    ["חתימה", "דוח לא חתום קשה להציג"],
], minw=520)
S_CHOOSE = ('<h2>איך בוחרים בודק: 9 שאלות לפני שמזמינים</h2>\n'
            '<p>לא מצאנו בחוק רישיון נפרד לבודקי בדק בית; בפועל בודקים מהנדסים והנדסאי בניין. לכן השאלה הראשונה היא מי מגיע בפועל, והאם הוא רשום. '
            'את הרישום בודקים בעצמכם ב<a href="%s" target="_blank" rel="noopener">פנקס המהנדסים והאדריכלים של משרד העבודה</a>. ואלה השאלות שכדאי לשאול בטלפון:</p>\n'
            '<ol>\n<li>מי הבודק שיגיע, ומה מספר הרישום שלו?</li>\n<li>האם מצלמה תרמית, מד לחות ובדיקת לחץ מים כלולים במחיר?</li>\n<li>האם המחיר סופי, ואם המע״מ כלול?</li>\n'
            '<li>תוך כמה ימים מגיע הדוח, והאם הוא חתום?</li>\n<li>האם הדוח כולל אומדן עלות לתיקון לכל ליקוי?</li>\n<li>אפשר לראות דוח לדוגמה?</li>\n'
            '<li>האם אפשר להיות נוכחים כשהבודק עובר על הדירה?</li>\n<li>האם בדיקה חוזרת אחרי התיקונים כלולה, ובכמה?</li>\n<li>האם הבודק מכיר דירות מהסוג שלי: גג, גן, בית פרטי, דירה אחרי שיפוץ?</li>\n</ol>\n'
            % BD["sources"]["ENG"]["url"] + T7)

# ------------------------------------------------------------------ FAQ: 20 new after the 5 old
FAQ_NEW = [
    ("כמה עולה בדק בית?", "לפי המחירים שפורסמו ב-2025 וב-2026: דירה של 3 עד 5 חדרים %s עד %s ₪, דירה של 6 חדרים ומעלה %s עד %s ₪, ובית פרטי עד 200 מ״ר %s עד %s ₪. במידרג המחיר כולל מע״מ; אצל השאר לא צוין, ולכן שואלים." % (num(A35[0]), num(A35[1]), num(A6[0]), num(A6[1]), num(HOUSE[0]), num(HOUSE[1]))),
    ("כמה עולה בדק בית לדירה יד שנייה?", "המחיר נקבע לפי הגודל וסוג הנכס ולא לפי גיל הדירה: דירה עד 120 מ״ר 1,200 עד 1,900 ₪ כולל מע״מ לפי מידרג, ודירת 4 חדרים %s עד %s ₪ לפי כל המקורות. בדירה ישנה כדאי לוודא שבדיקת הצנרת ומד הלחות כלולים." % (num(env("apt", [4])[0]), num(env("apt", [4])[1]))),
    ("מה נבדק בבדק בית?", "איטום ורטיבות, צנרת וביוב, חשמל, ריצוף וחיפוי, חלונות ודלתות, סדקים, טיח וצבע, חיפוי חוץ, דוד ומכונות, בידוד, חצר וחניה, ממ״ד ומעקות, והתאמה למפרט ולתוכנית. הטבלה בעמוד מפרטת את הכלי ואת תקופת הבדק לכל חלק."),
    ("תוך כמה זמן מקבלים את הדוח?", "לפי מה שבודקים פרסמו, הדוח מגיע בין 3 ל-14 ימים, ודוח לבית משפט לוקח יותר. שאלו לפני ההזמנה, במיוחד כשתקופת בדק עומדת להיגמר."),
    ("מהי שנת בדק?", "שנת בדק היא תקופת הבדק הקצרה ביותר בחוק המכר (דירות): שנה מהמסירה לכל ליקוי שאינו ברשימה, כמו חשמל, טיח וצבע. לחלונות, לריצוף, לצנרת, לאיטום, לסדקים ולחיפוי חוץ יש תקופות ארוכות יותר, עד 7 שנים."),
    ("מה ההבדל בין תקופת בדק לתקופת אחריות?", "בתקופת הבדק הקבלן אחראי לליקוי אלא אם יוכיח שגרמתם לו. בתקופת האחריות, 3 שנים אחרי כל תקופת בדק, הקבלן עדיין אחראי, אבל אתם צריכים להוכיח שמקור הליקוי בתכנון, בעבודה או בחומרים."),
    ("האם בדק בית כולל מצלמה תרמית?", "לא תמיד. חלק מהבודקים כוללים תרמוגרפיה בסיסית במחיר של דירת 4 עד 5 חדרים, ואחרים מתמחרים אותה בנפרד. שאלו מראש, כי בלי מצלמה תרמית ומד לחות קשה לאתר רטיבות נסתרת."),
    ("קניתי דירה יד שנייה בת 3 שנים: האם הקבלן עדיין אחראי?", "כן, לליקויים שתקופתם לא נגמרה. החוק נותן גם לקונה משנה את תקופות הבדק והאחריות, והן נספרות מהמסירה לקונה הראשון: צנרת ואיטום 4 שנים ועוד 3 שנות אחריות, סדקים 5, חיפוי חוץ 7."),
    ("עד מתי מודיעים לקבלן על ליקוי שראיתי כבר במסירה?", "בתוך שנה מיום המסירה (סעיף 4א(א)(1) לחוק המכר (דירות)). ליקוי שלא היה אפשר לראות במסירה: תוך זמן סביר מהגילוי."),
    ("מה עושים אם הקבלן לא מתקן?", "שולחים מכתב בכתב עם הדוח ונותנים הזדמנות נאותה לתקן. אם הליקוי חזר אחרי תיקון בתוך שנתיים מההודעה, או שתיקון דחוף לא בוצע בזמן סביר, מותר לתקן בעצמכם על חשבון הקבלן. אחר כך: עורך דין ותביעה."),
    ("מה זה ליקוי יסודי?", "אי התאמה בחלקי הבניין הנושאים ומעבירים עומסים לקרקע, שנוגעת ליציבות ולבטיחות. עליו הקבלן אחראי 20 שנה מהמסירה, ואחריהן אם תוכיחו שמקורו בתכנון, בעבודה או בחומרים."),
    ("מי רשאי לבצע בדק בית?", "לא מצאנו בחוק רישיון נפרד לבדק בית. בפועל בודקים מהנדסים והנדסאי בניין. בקשו את שם הבודק ובדקו אותו בפנקס המהנדסים והאדריכלים של משרד העבודה."),
    ("כמה עולה בדק בית לרכוש משותף?", "לפי מידרג %s ₪ לדירה ועוד מע״מ, עם מינימום של %s ₪ לבניין. בבניין של פחות מ-17 דירות המינימום מייקר את החלק של כל דירה. מזמינים דרך נציגות הבית." % (num(SHR["per_apt"]), num(SHR["min"]))),
    ("האם כדאי לעשות בדק בית לדירה חדשה מקבלן?", "כן: לפני פרוטוקול המסירה, ושוב לפני סוף כל תקופת בדק. דירה חדשה אינה דירה בלי ליקויים, והדוח הוא מה שהופך תלונה לדרישה לפי החוק."),
    ("האם בדק בית לבית פרטי יקר יותר?", "כן. בית פרטי עד 200 מ״ר פורסם ב-%s עד %s ₪, ובית גדול או וילה ב-%s עד %s ₪, כי בודקים גם גג, חצר וקירות חוץ." % (num(HOUSE[0]), num(HOUSE[1]), num(VILLA[0]), num(VILLA[1]))),
    ("אפשר להזמין בדיקה חוזרת אחרי שהקבלן תיקן?", "כן, וכדאי. חלק מהבודקים כוללים בדיקה חוזרת במחיר וחלק גובים בנפרד; שאלו לפני ההזמנה הראשונה. הבדיקה החוזרת היא גם הראיה שהליקוי חזר, אם יחזור."),
    ("מה צריך להיות בדוח בדק בית?", "שם הבודק ומספר הרישום, תאריך הבדיקה ויום המסירה, כל ליקוי עם מיקום ותמונה, הדרישה שהוא סוטה ממנה, חומרה, אומדן עלות לתיקון, תדפיסי מכשירים וחתימה."),
    ("האם בדק בית עוזר להוריד את המחיר ביד שנייה?", "כן, כשהוא נעשה לפני החתימה. ליקוי מהותי עם אומדן עלות נכנס למשא ומתן כהפחתה, כתיקון לפני המסירה או כסכום בנאמנות. אחרי החתימה רוב החוזים מעבירים את הסיכון לקונה."),
    ("מה הקשר בין בדק בית לתקנים?", "החוק קובע שדירה שונה מהמפרט, מתקן רשמי או מתקנות הבנייה היא אי התאמה. לכן דוח טוב מציין ליד כל ליקוי את הדרישה שהוא סוטה ממנה, ולא רק תיאור."),
    ("האם הקבלן חייב לתת הוראות תחזוקה?", "כן. המוכר מצרף לחוזה מפרט והוראות תחזוקה ושימוש, וכשהפרטים חסרים בחתימה הוא מוסר אותן חתומות במסירה. מוכר שלא מסר הוראות תחזוקה לא קיים את חיוביו (סעיף 4(א)(6))."),
]
assert len(FAQ_NEW) == 20

# ------------------------------------------------------------------ English section + method
EN_T = tbl("The builder's warranty in Israel (Sale of Apartments Law)", ["Defect", "Inspection period", "Then warranty"], [
    ["Any defect not listed (electrical, plaster, paint)", "1 year", "3 years"], ["Windows, doors, aluminium; interior tiling", "2 years", "3 years"],
    ["Boilers and machines; yard; thermal insulation", "3 years", "3 years"], ["Plumbing, sewage, gutters; waterproofing", "4 years", "3 years"],
    ["Cracks over 1.5 mm in non-bearing parts", "5 years", "3 years"], ["Exterior cladding coming loose", "7 years", "3 years"],
    ["Structure and stability", "20 years", ""]], minw=480)
EN = ('<section class="%s-en" lang="en" dir="ltr">\n<h2>Home inspection in Israel (bedek bayit): prices and the builder\'s warranty</h2>\n'
      '<p>A bedek bayit is an engineering inspection of an apartment or house: before you buy a resale home, on the day a developer hands over a new one, and before an inspection period ends. '
      'Published prices in 2025 and 2026: %s to %s NIS for a 3 to 5 room apartment and %s to %s NIS for a private house up to 200 m² (Midrag quotes include VAT; other sources do not say).</p>\n'
      '<p>For a new apartment, the Sale of Apartments Law gives every defect type an inspection period from handover, during which the developer must repair unless he proves you caused the defect, followed by 3 warranty years in which you must show the cause is in design, work or materials. '
      'A later buyer of a young apartment keeps the same periods, counted from the first handover. Notify the developer in writing; a defect visible at handover must be reported within one year.</p>\n' % (PFX, num(A35[0]), num(A35[1]), num(HOUSE[0]), num(HOUSE[1])) +
      EN_T + '<p>Check the inspector in the Ministry of Labor register of engineers and architects before you book. Buying from abroad? Start with <a href="/en/buy-property-in-israel/">buying property in Israel</a>.</p>\n</section>\n')
METHOD = ('<p class="%s-note">עודכן %s. תקופות הבדק והאחריות לפי נוסח חוק המכר (דירות) היום; המחירים כפי שפורסמו במידרג (12.2025, 7.2025, 2.2022), בבדק מבנים (1.2026) ובהבודקים (6.2026). '
          'המידע כללי ואינו מחליף בדיקה הנדסית או ייעוץ משפטי.</p>\n' % (PFX, UPDATED))

# ------------------------------------------------------------------ the live content, the anchors
DRYF = "--from" in sys.argv
if DRYF:
    raw = io.open(sys.argv[sys.argv.index("--from") + 1], encoding="utf-8").read(); req = None; r = {"modified": "local file", "link": SITE + "/home-inspection/"}
else:
    req, raw, r = get_live(PID, DRY)
OLD_DATE = "עודכן ונבדק: 2026-06-02."
OLD_PRICE = "בסריקת מחירונים ציבוריים של אתרי שירות ובדק בית בישראל נמצאו בדרך כלל טווחים של כ-1,200 עד 2,600"
NEW_PRICE = "במחירים שפורסמו ב-2025 וב-2026 (הטבלה למטה, מקור אחר מקור) בדק בית לדירה של 3 עד 5 חדרים עולה %s עד %s" % (num(A35[0]), num(A35[1]))
a_top = before_block(raw, OLD_DATE)
R_ADD = [
    (before_block(raw, "מתי עושים בדק בית?"), S_CHECK),
    (before_block(raw, "בדק בית לדירה יד שנייה"), S_LAW),
    (before_block(raw, "בדק בית לדירה חדשה מקבלן"), S_TWO),
    (before_block(raw, "מה בודקים בבדק בית?"), S_CAL),
    (before_block(raw, "ליקויים נפוצים שמגלים לפני קנייה"), S_PRICE),
    (before_block(raw, "איך בוחרים מהנדס או חברת בדק בית?"), S_LETTER),
    (before_block(raw, "קבעו את הבדיקה לפני חתימה או לפני פרוטוקול מסירה"), None),  # resolved below (the checklist block)
    (before_block(raw, "השלב הבא בקניית דירה"), faq(FAQ_NEW)),
]
# the checklist heading has an apostrophe; anchor on its first item instead and insert S_CHOOSE before the checklist heading block
ck_head = raw[:raw.find("קבעו את הבדיקה לפני חתימה או לפני פרוטוקול מסירה")].rfind("<h2")
ck_anchor = before_block(raw, raw[ck_head:raw.find("</h2>", ck_head)].split(">", 1)[1])
R_ADD[6] = (ck_anchor, S_CHOOSE)
R = [(a_top, TOP + a_top.replace(OLD_DATE, "עודכן ונבדק: %s." % UPDATED))] + [(o, n + o) for o, n in R_ADD] + [(OLD_PRICE, NEW_PRICE)]
new = apply(raw, R) + "\n" + EN + METHOD
NEWS = [TOP, S_CHECK, S_LAW, S_TWO, S_CAL, S_PRICE, S_LETTER, S_CHOOSE, faq(FAQ_NEW), EN, METHOD]
print("[page %d] live content modified %s, %d chars; %d anchors matched once each (%s)" % (PID, r.get("modified"), len(raw), len(R), "public REST, rendered" if DRY else "raw"))
qs = gates("".join(NEWS) + NEW_PRICE, new, 5 + 20)
inner, bad, offi = check_links("".join(NEWS))
assert not bad, ("internal links must answer 200", bad)
c_all, c_old = counts(new), counts(raw)
print("  page now: %s | before: %s" % (json.dumps(c_all, ensure_ascii=False), json.dumps(c_old, ensure_ascii=False)))
print("  FAQ %d (5 old + 20 new); internal links %d all 200; external: %s" % (len(qs), len(inner), ", ".join("%s %s" % (h.split("/")[2], st) for h, st in offi)))
print("  title %d chars, SEO title %d, description %d; language gates passed; svg text >= 12px" % (len(TITLE), len(SEO_T), len(SEO_D)))

SRC = """# /home-inspection/ (page 90): where every fact on the page comes from (internal, written by write_g6_page.py, %s)

| Fact | Source |
|---|---|
| The 10 inspection periods, 3 warranty years, 20 years structural, notice within a year, the repair rule, the sub-buyer, spec/standard/regulations as non-conformity, maintenance instructions | חוק המכר (דירות), התשל"ג-1973, ss. 1, 2, 4, 4א, 4ב and the schedule (Wikisource, read 26.10.2026); same table as the live warranty.js |
| Apartment up to 120 m² 1,200-1,900 incl. VAT; house up to 200 m² 2,200-2,950 incl. VAT; shared property 180 + VAT per apartment, min 3,000 + VAT | midrag.co.il/Content/Tip/981 (modified 17.12.2025), read 26.10.2026 |
| Private house average paid 2,516.29 incl. VAT, min 1,947, max 3,300, 84%% under 2,900 | midrag.co.il/Content/PriceList/540007 (data 13.7.2025) |
| Roof or garden add-on 200-300; groups of 10-30 apartments 1,000-1,200 per apartment | midrag.co.il/Content/Price/7261 (15.2.2022) |
| 2-3 rooms 1,100-1,600; 4-5 rooms 1,500-2,500; 5+ 1,800-3,500; penthouse 2,500-4,500; small house 2,000-6,000; villa 2,500-6,000; moisture only 600-1,800; court 2,500-10,000 (VAT not stated) | bedek-mivnim.co.il item 32 (modified 12.1.2026) |
| Fixed list 1,200 / 1,300 / 1,400 / 1,500 / 1,600 by rooms; groups up to 15%% (VAT not stated) | ha-bodkim.co.il blog (June 2026) |
| Report in 3 to 14 days | bedek-mivnim (3-7) and at-terminal (7-14), competitor pages read 26.10.2026 |
| Engineers register lookup | data.labor.gov.il/EngineersAndArchitects.aspx (200, 26.10.2026) |
""" % UPDATED
io.open(os.path.join(H, "page-sources-g6.md"), "w", encoding="utf-8").write(SRC)

if DRY or DRYF:
    pv = os.path.join(H, "preview"); os.makedirs(pv, exist_ok=True)
    io.open(os.path.join(pv, "g6-page-content.html"), "w", encoding="utf-8", newline="").write(new)
    render_shell(os.path.join(pv, "g6-page-render.html"), "/home-inspection/", TITLE, new, ["bedek"])
    print("  --dry: wrote preview/g6-page-content.html, preview/g6-page-render.html, page-sources-g6.md; nothing was posted")
    sys.exit(0)

bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw + "\n<!-- title " + repr((r.get("title") or {}).get("raw")) + " | meta " + repr((r.get("meta") or {}).get("_yoast_wpseo_title")) + " | " + repr((r.get("meta") or {}).get("_yoast_wpseo_metadesc")) + " -->")
req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new, "title": TITLE, "meta": {"_yoast_wpseo_title": SEO_T, "_yoast_wpseo_metadesc": SEO_D}})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,title" % PID)[1]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers=UA), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
title = re.search(r"<title>(.*?)</title>", page, re.S).group(1).strip()
ok = {"read-back": back["content"]["raw"].strip() == new.strip(), "WP title": back["title"]["raw"] == TITLE, "one h1": bd.count("<h1") == 1, "h1 text": TITLE in bd,
      "tool mounted": 'data-nli="bedek"' in bd, "shortcode rendered": "[nadlan_tool" not in bd, "svg x3": bd.count("%s-fig" % PFX) == 3,
      "one FAQPage": page.count('"@type":"FAQPage"') == 1, "25 questions": page.count('"@type":"Question"') == 25, "SoftwareApplication": '"@type":"SoftwareApplication"' in page,
      "bedek.js enqueued": "tools/bedek.js" in page, "SEO title": title.startswith(SEO_T), "updated": ("עודכן %s" % UPDATED) in bd}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
