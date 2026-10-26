# -*- coding: utf-8 -*-
"""G8 on /real-estate-lawyer/ (page 11): the owner page of "עורך דין מקרקעין" (1,600 searches a month, KD 24, CPC $12.98; also
"עורך דין נדלן" 590, "עורך דין מכירת דירה" 390, "עורך דין קניית דירה" 320; the exact head term is not seen in Search Console in
90 days; the page has 549 impressions on long-tail lawyer queries). Spec: dna.md (this folder). NOT RUN against the site by the
research session (Ben, 26.10.2026: local only).

What it does (every number from data/orechdin.json and data/ptax.json, built by tools/instruments/build_pros_data.py from the Sale
Law s.6ג and the 2014 regulations with the 2026 notice, the Bar's recommended minimum tariff with the 2026 amounts, the Land Fees
regulations (2026 amounts), the Land Taxation Law ss. 15, 73, the ethics rule 14, and the fee levels law offices published in 2026):
  1. the H1 (the hero h2, printed as the page's h1) with the head term first, the WP title, Yoast title and description;
  2. inside the hero under the H1: the answer, three CTAs and a one-line legal note; before the first section: the tool
     [nadlan_tool id="orechdin"] and T1;
  3. new sections before named old headings: the fees (I2, T2, T3), the steps of a second-hand purchase (I3, T4), the new apartment
     and the developer's lawyer (I1, T5, T6), the registry fees and the other costs (T7), how to choose and check a lawyer and the
     rule on one lawyer for both sides (T8);
  4. 24 new FAQ after the 4 old ones = 28; honesty fixes: the FAQ on who pays gets the legal cap, and the unverified line
     "כתוב ונבדק על-ידי עורך דין מקרקעין" is removed (no reviewing lawyer is named anywhere; Ben's word if one did review);
     an English section and the method line.
Each anchor must match exactly once. Language law on the new visible text; internal links must answer 200 without a redirect.
  python write_g8_page.py --dry   public REST only: writes preview/g8-page-content.html, preview/g8-page-render.html, page-sources-g8.md
  python write_g8_page.py         backup, POST, read-back, live check (BLOCKED below until Ben's word)
  --style                          also the style-only reform of the old gold eyebrow and cream note boxes (Ben's word)"""
import io, json, os, re, sys, time, urllib.parse, urllib.request

H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from g6g8_common import *  # noqa: E402,F401
import infographics as ig  # noqa: E402

DRY = "--dry" in sys.argv; STYLE = "--style" in sys.argv
PID = 11; PFX = "nlod"
H1_OLD = "בעסקת דירה, עורך הדין הוא קו ההגנה לפני הכסף הגדול"
H1_NEW = "עורך דין מקרקעין: מה הוא בודק לפני החתימה, כמה זה עולה ואיך בוחרים"
TITLE = H1_NEW
SEO_T = "עורך דין מקרקעין: שכר טרחה 2026 ובדיקות לפני חתימה"
SEO_D = "עורך דין מקרקעין לקניית דירה: שכר טרחה שפורסם מול התעריף המומלץ של הלשכה, מה מותר לקבלן לגבות (5,915 ₪ ב-2026), אגרות הטאבו, צעדי העסקה ומחשבון."
assert len(SEO_T) <= 60 and len(SEO_D) <= 160, (len(SEO_T), len(SEO_D))
tbl = Tables(PFX)
WA_T = wa_link("שלום, הגעתי מהמדריך לעורך דין מקרקעין באתר נדלן ואשמח לפרטים נוספים")
C = OD["cap"]; TR = OD["tariff"]; LANDF = {r[0]: r[2] for r in OD["land"]}; PAY = PT["pay"]
SRCN = {k: v["label"].split(" (")[0].split(",")[0] for k, v in OD["sources"].items()}
FEES_URL = OD["sources"]["FEES"]["url"]


def tariff(v):
    if v > TR["top"]: return TR["top_min"]
    return max(TR["min"], sum((min(v, hi) - lo) * r for lo, hi, r in TR["tiers"] if v > lo))


def cap(p): return None if p > C["ceiling"] else min(C["fixed"], p * C["pct"])


def same(name, got, want): assert got == want, ("cross-check", name, got, want)
same("cap 2026", C["fixed"], 5915); same("ceiling", C["ceiling"], 4642750); same("tariff 2M", round(tariff(2000000)), 23322); same("warning note", LANDF["warn"], 188)
same("declare / pay days", (PAY["declare_days"], PAY["pay_days"]), (30, 60)); same("cap 1M", cap(1000000), 5000.0)

# ------------------------------------------------------------------ TOP
ANSWER = ('<p class="%s-lead">עורך דין מקרקעין בודק את הזכויות בנכס ואת המוכר, מנסח את החוזה או בודק אותו, רושם הערת אזהרה, מדווח לרשות המסים בתוך 30 יום ומעביר את הבעלות על שמכם. '
          'ב-2026 משרדים מפרסמים שכר טרחה של כ-0.5%% ממחיר הדירה ועוד מע״מ, ועד 1%%, עם מינימום של כ-5,000 עד 6,000 ₪. בדירה חדשה, הקבלן רשאי לגבות מכם על עורך הדין שלו לכל היותר %s ₪ או 0.5%% מהמחיר, '
          'הנמוך מביניהם, ועוד מע״מ; מעל %s ₪ אין תקרה.</p>\n' % (PFX, num(C["fixed"]), num(C["ceiling"])) +
          '<div class="%s-cta"><a class="%s-go" href="#orechdin-tool">כמה יעלה עורך דין בעסקה שלכם</a><a href="%s" target="_blank" rel="noopener">לקבלת פרטים נוספים בוואטסאפ</a><a href="#lawyer-steps">צעדי העסקה והמועדים</a></div>\n' % (PFX, PFX, WA_T) +
          '<p class="%s-legal">המידע כללי ואינו ייעוץ משפטי. האתר אינו מייצג קונים, מוכרים או יזמים.</p>\n' % PFX)
T1 = tbl("עורך דין מקרקעין במספרים (נבדק 26.10.2026)", ["מה", "המספר", "מקור"], [
    ["שכר טרחה שמשרדים פרסמו", "כ-0.5% ועוד מע״מ; עד 1%; מינימום כ-5,000 עד 6,000 ₪", "4 פרסומים, 2026"],
    ["התעריף המומלץ של הלשכה לעריכת חוזה על 2 מיליון ₪", "%s ₪ ועוד מע״מ (המלצה שאינה מחייבת)" % num(tariff(2000000)), "כללי לשכת עורכי הדין, סכומי 2026"],
    ["מה מותר לקבלן לגבות על עורך הדין שלו", "הנמוך מבין %s ₪ ו-0.5%% מהמחיר, ועוד מע״מ" % num(C["fixed"]), "תקנות המכר (דירות), הודעת 2026"],
    ["מעל איזה מחיר אין תקרה", "%s ₪" % num(C["ceiling"]), "תקנה 4"],
    ["ניהול רשימת הזכויות עד הרישום", "עד %s ₪" % num(C["list_fee"]), "צו הפיקוח על המחירים, לפי כל זכות"],
    ["הערת אזהרה בטאבו", "%s ₪; מחיקה %s ₪" % (num(LANDF["warn"]), num(LANDF["warn_del"])), "תקנות המקרקעין (אגרות), 2026"],
    ["רישום המכר / רישום משכנתה", "%s ₪ / %s ₪" % (num(LANDF["sale"]), num(LANDF["mortgage"])), "תקנות המקרקעין (אגרות), 2026"],
    ["הצהרה לרשות המסים", "בתוך %d יום מהעסקה" % PAY["declare_days"], "חוק מיסוי מקרקעין, סעיף 73"],
    ["תשלום מס הרכישה", "בתוך %d יום; איחור: 0.2%% לשבוע ועוד הצמדה וריבית" % PAY["pay_days"], "חוק מיסוי מקרקעין"],
    ["מקדמה על מס שבח שהקונה מעביר", "7.5% מהמחיר (15% בנכס מלפני 7.11.2001), אחרי 40% מהתמורה", "חוק מיסוי מקרקעין, סעיף 15"],
    ["עורך דין אחד לשני הצדדים", "אסור כשיש אינטרסים מנוגדים; עריכת הסכם מותרת בהסכמה בכתב", "כלל 14 לכללי האתיקה"],
], minw=620)
TOOL = (css(PFX, guide=True) + (reform_css(PFX) if STYLE else "") +
        '<div class="%s-tool" id="orechdin-tool">[nadlan_tool id="orechdin"]</div>\n' % PFX + T1)

# ------------------------------------------------------------------ S_FEE (before "נסח טאבו: נקודת פתיחה, לא סוף הבדיקה")
T2 = tbl("שכר טרחה שמשרדי עורכי דין פרסמו ב-2026", ["מקור", "מה פורסם", "פורסם"], [
    [SRCN["DORON"], "כ-0.5% ועוד מע״מ משווי הנכס, בקנייה ובמכירה; בנכסים יקרים לעיתים פחות", "12.10.2026"],
    [SRCN["ADDA"], "כ-0.5% ועוד מע״מ, מינימום כ-5,000 עד 6,000 ₪; יד שנייה עד 2.5 מיליון: 5,000 עד 12,500 ₪; 2.5 עד 5 מיליון: 12,500 עד 25,000 ₪; מקבלן: 5,000 עד 15,000 ₪", "2.7.2026"],
    [SRCN["GELB"], "קנייה או מכירה: 0.5% עד 1%; מכירה: 0.25% עד 1%, לרוב 0.5%; התייעצות: כ-500 ₪, עם בדיקת מסמכים עד 1,000 ₪", "22.9.2026"],
    [SRCN["BIZ"], "0.5% עד 1% ועוד מע״מ (הטווח שבמחשבון עלות הרכישה באתר)", "6.8.2026"],
], minw=560, note="אין תעריף מחייב לשכר טרחה בעסקת דירה; הסכום נקבע בהסכם שכר טרחה בכתב.")
T3 = tbl("התעריף המינימלי המומלץ של לשכת עורכי הדין, 2026", ["פעולה", "התעריף המומלץ"], [
    ["עריכת חוזה: עד 95,004 ₪", "2%, לא פחות מ-790 ₪"],
    ["החלק שבין 95,004 ל-377,607 ₪", "1.5%"], ["החלק שבין 377,607 ל-761,062 ₪", "1.25%"], ["החלק שבין 761,062 ל-2,283,281 ₪", "1%"],
    ["החלק שבין 2,283,281 ל-3,806,082 ₪", "0.75%"], ["חוזה מעל 3,806,082 ₪", "לפי הסכם, לא פחות מ-37,761 ₪"],
    ["רישום מכר, כשעורך הדין לא ערך את החוזה", "1% עד 633,967 ₪ ו-0.75% מעל"],
    ["רישום הערת אזהרה", "748 ₪ (ערך את החוזה) או 1,068 ₪"], ["רישום משכנתא", "0.5% מהחוב, לא פחות מ-1,012 ₪"],
    ["דירה מקבלן: לעורך הדין של הקבלן", "1% מהמחיר (אבל החוק מגביל את מה שמותר לגבות מהקונה)"], ["דירה מקבלן: לעורך הדין של הקונה, בדיקת החוזה והרישום", "0.25% מהמחיר"],
    ["דוגמה: חוזה על 1,000,000 ₪", "%s ₪" % num(tariff(1000000))], ["דוגמה: חוזה על 2,000,000 ₪", "%s ₪" % num(tariff(2000000))], ["דוגמה: חוזה על 3,000,000 ₪", "%s ₪" % num(tariff(3000000))],
], minw=520, note="הכללים קובעים שהתעריף הוא המלצה לחברי הלשכה שאינה מחייבת, ושהסכומים מתעדכנים לפי המדד בכל ינואר; לכל הסכומים מוסיפים מע״מ.")
S_FEE = ('<h2>כמה עולה עורך דין מקרקעין: מה שמפורסם, מה שהלשכה ממליצה ומה שהחוק מגביל</h2>\n'
         '<p>שלושה מספרים שונים מסתובבים בשאלה הזאת. הראשון הוא מה שמשרדים מפרסמים: כ-0.5%% ממחיר הדירה ועוד מע״מ, ועד 1%%, עם מינימום של כמה אלפי שקלים. השני הוא התעריף המינימלי המומלץ של לשכת עורכי הדין, '
         'שאינו מחייב וגבוה בהרבה: על חוזה של 2 מיליון ₪ הוא %s ₪. השלישי הוא מגבלה בחוק, והיא חלה רק על דבר אחד: כמה הקבלן רשאי לגבות מכם על עורך הדין שלו בדירה חדשה.</p>\n' % num(tariff(2000000)) +
         fig(PFX, ig.g8_fees(), "שכר טרחה לפי מחיר הדירה, לפני מע״מ: מה שמשרדים פרסמו ב-2026 מול התעריף המינימלי המומלץ של לשכת עורכי הדין לעריכת חוזה.") + T2 + T3 +
         '<h3>מה נכנס לשכר הטרחה, ומה משלמים בנפרד</h3>\n'
         '<p>שכר הטרחה מכסה בדרך כלל את הבדיקות, המשא ומתן על החוזה, הדיווח לרשות המסים והרישום עד הסוף. בנפרד משלמים את המסים (<a href="/purchase-tax-calculator/">מחשבון מס רכישה</a>), את אגרות הטאבו, '
         'את השמאי ואת בדק הבית. בקשו הצעה כתובה שאומרת אם המחיר כולל מע״מ, מתי משלמים כל חלק, ומה קורה אם העסקה לא יוצאת לפועל.</p>\n')

# ------------------------------------------------------------------ S_STEPS (before "מתי פונים לעורך דין מקרקעין?")
T4 = tbl("קונים דירה יד שנייה: הצעדים, מי עושה, המסמכים", ["שלב", "מי", "מה קורה", "מסמכים"],
         [[s[0], s[1], s[2], ", ".join(s[3]) or "אין"] for s in OD["steps"]["buy2"]], minw=680)
S_STEPS = ('<h2 id="lawyer-steps">צעדי העסקה ביד שנייה: מי עושה מה, ומה המועדים בחוק</h2>\n'
           '<p>רוב השלבים לא קבועים בחוק אלא בחוזה, אבל כמה מועדים כן: ההצהרה לרשות המסים בתוך %d יום מהעסקה, מס הרכישה בתוך %d יום, והמקדמה על מס השבח שהקונה מעביר מתוך התשלומים למוכר. '
           'בכלי למעלה, בלשונית "צעדי העסקה", רושמים את יום החתימה ומקבלים את התאריכים.</p>\n' % (PAY["declare_days"], PAY["pay_days"]) +
           fig(PFX, ig.g8_steps(), "קניית דירה יד שנייה: הצעדים והמועדים שהחוק קובע, מהבדיקות ועד הרישום. הימים לפי חוק מיסוי מקרקעין.") + T4 +
           '<h3>המקדמה על מס שבח: מה הקונה מעביר ומתי</h3>\n'
           '<p>בעסקה שהתמורה בה בכסף, הקונה מעביר לרשות המסים 7.5% מהמחיר על חשבון מס השבח של המוכר, או 15% כשהמוכר רכש את הנכס לפני 7.11.2001. '
           'מעבירים מיד אחרי ששולמו למוכר יותר מ-40% מהתמורה, או במועד ההצהרה, המאוחר מביניהם, והמקדמה נחשבת תשלום למוכר. המוכר או הקונה רשאים לבקש מרשות המסים להקטין אותה עד מועד ההצהרה (סעיף 15).</p>\n')

# ------------------------------------------------------------------ S_NEW (before "עורך דין ברכישת דירה להשקעה")
T5 = tbl("עורך הדין של הקבלן: כמה מותר לגבות מכם, לפי מחיר הדירה (2026)", ["מחיר הדירה", "0.5% מהמחיר", "המרבי לפני מע״מ", "עם מע״מ 18%"],
         [[ils(p), ils(p * C["pct"]), ils(cap(p)) if cap(p) is not None else "אין תקרה", ils(cap(p) * 1.18) if cap(p) is not None else "אין תקרה"] for p in (800000, 1000000, 1183000, 2000000, 3000000, 4642750, 5000000)],
         minw=520, num_cols=True, note="ועוד עד %s ₪ לניהול רשימת בעלי הזכויות. הסכום הקבוע: %s ₪ ב-2024, %s ₪ ב-2025, %s ₪ ב-2026." % (num(C["list_fee"]), "5,575.06", "5,770.77", num(C["fixed"])))
T6 = tbl("קונים דירה חדשה מקבלן: הצעדים", ["שלב", "מי", "מה קורה", "מסמכים"], [[s[0], s[1], s[2], ", ".join(s[3]) or "אין"] for s in OD["steps"]["new"]], minw=680)
S_NEW = ('<h2>דירה מקבלן: מה מותר לקבלן לגבות על עורך הדין שלו</h2>\n'
         '<p>בדירה חדשה, עורך הדין של הקבלן מטפל גם ברישום הזכויות שלכם, והקבלן רשאי לגבות מכם השתתפות בשכר הטרחה שלו. החוק מגביל את הסכום: הנמוך מבין %s ₪ (הסכום לשנת 2026, צמוד למדד) '
         'ו-0.5%% ממחיר הדירה בחוזה, לפני מע״מ. בדירה שמחירה מעל %s ₪ התקנות לא מגבילות. את התשלום מעבירים ישירות לעורך הדין, והוא חייב לתת חשבונית (סעיף 6ג לחוק המכר (דירות)).</p>\n' % (num(C["fixed"]), num(C["ceiling"])) +
         fig(PFX, ig.g8_cap(), "התקרה לשנת 2026: 0.5% ממחיר הדירה עד 1,183,000 ₪, אחר כך 5,915 ₪ קבועים, ועוד מע״מ; מעל 4,642,750 ₪ אין תקרה.") + T5 +
         '<h3>מי מייצג אתכם בדירה מקבלן</h3>\n<p>עורך הדין של הקבלן מייצג את הקבלן. הוא לא יכול לייעץ לכם בנפרד, ובמשא ומתן על החוזה אתם רשאים לשכור עורך דין משלכם ולשלם לו בנפרד. '
         'כל תשלום לקבלן הולך דרך פנקס השוברים לחשבון הפרויקט, ומולו מקבלים ערבות לפי חוק המכר (הבטחת השקעות) או פוליסת ביטוח. אחרי המסירה מתחילות תקופות הבדק והאחריות: <a href="/home-inspection/">בדק בית</a>.</p>\n<h3>הצעדים בדירה מקבלן</h3>\n' + T6)

# ------------------------------------------------------------------ S_FEESREG (before "מה להכין לפני פנייה לעורך דין?")
T7 = tbl("אגרות לשכת רישום המקרקעין (טאבו), 2026", ["פעולה", "אגרה"], [[r[1], ils(r[2])] for r in OD["land"]], minw=420, num_cols=True,
         note='הסכומים לפי <a href="%s" target="_blank" rel="noopener">תקנות המקרקעין (אגרות)</a> לשנת 2026; מתעדכנים לפי המדד בכל ינואר.' % FEES_URL)
S_FEESREG = ('<h2>אגרות הטאבו ומה עוד משלמים בעסקה</h2>\n'
             '<p>אגרות הרישום עצמן קטנות: בעסקת יד שנייה עם משכנתא, הערת אזהרה לטובתכם, הערה לטובת הבנק, רישום המכר ורישום המשכנתה יחד הן %s ₪. הסכומים הגדולים הם מס הרכישה, שכר הטרחה, '
             'השמאי ובדק הבית. את כולם יחד מחשבים ב<a href="/apartment-purchase-cost-calculator/">מחשבון עלות רכישה כוללת</a>.</p>\n'
             % num(LANDF["warn"] * 2 + LANDF["sale"] + LANDF["mortgage"]) + '<h3>אגרות 2026 לפי התקנות</h3>\n' + T7)

# ------------------------------------------------------------------ S_CHOOSE (before "טעויות נפוצות בעסקאות מקרקעין")
T8 = tbl("לפני שבוחרים עורך דין: מה לשאול", ["שאלה", "למה"], [
    ["כמה עסקאות כמו שלי טיפלת בשנה האחרונה?", "יד שנייה, דירה מקבלן, קרקע ותמ״א הן עולמות שונים"],
    ["מה בדיוק כלול בשכר הטרחה?", "בדיקות, חוזה, דיווח לרשות המסים, רישום עד הסוף"],
    ["האם המחיר כולל מע״מ, ומתי משלמים?", "השוואה הוגנת בין הצעות"],
    ["מי מטפל בתיק בפועל?", "עורך הדין עצמו או עובד במשרד"],
    ["האם אתה מייצג גם את הצד השני?", "כלל 14 אוסר ייצוג אינטרסים מנוגדים"],
    ["מה קורה אם העסקה לא יוצאת לפועל?", "שכר חלקי או מלא"],
    ["האם יש לך ביטוח אחריות מקצועית?", "הגנה אם נפלה טעות"],
    ["איך מתעדכנים לאורך העסקה?", "מועדים, מסמכים, תשלומים"],
], minw=520)
S_CHOOSE = ('<h2>איך בוחרים עורך דין מקרקעין, ומה הכלל על עורך דין אחד לשני הצדדים</h2>\n'
            '<p>לפי כלל 14 לכללי האתיקה של לשכת עורכי הדין, עורך דין לא ייצג צדדים בעלי אינטרסים מנוגדים באותו עניין. החריג: עריכת הסכם וטיפול בעניין שהצדדים הסכימו בכתב שייעשו בידי אותו עורך דין. '
            'גם אז הוא לא יכול לייצג רק אתכם. בקנייה ובמכירה של דירה, ההמלצה שלנו פשוטה: לכל צד עורך דין משלו.</p>\n<h3>8 שאלות לפני שבוחרים</h3>\n' + T8 +
            '<p>את הרישום של עורך הדין בלשכה אפשר לבדוק באתר לשכת עורכי הדין. אנחנו אתר מידע: איננו מייצגים אף צד ואיננו גובים עמלה על עסקה.</p>\n')

# ------------------------------------------------------------------ FAQ: 20 new after the 4 old
FAQ_NEW = [
    ("כמה עולה עורך דין לקניית דירה?", "משרדים מפרסמים ב-2026 כ-0.5%% ממחיר הדירה ועוד מע״מ, עד 1%%, עם מינימום של כ-5,000 עד 6,000 ₪. בדירה של 2.4 מיליון ₪: 12,000 עד 24,000 ₪ ועוד מע״מ. אין תעריף מחייב; סוגרים בהסכם כתוב."),
    ("כמה עורך דין גובה על מכירת דירה?", "לפי מה שפורסם ב-2026: לרוב כ-0.5%% ועוד מע״מ, וטווח של 0.25%% עד 1%%. תכנון מס שבח, כמה בעלים או רישום מורכב מייקרים."),
    ("מה מותר לקבלן לגבות על עורך הדין שלו?", "הנמוך מבין %s ₪ (2026) ו-0.5%% ממחיר הדירה, ועוד מע״מ, ועוד עד %s ₪ לניהול רשימת הזכויות. בדירה שמחירה מעל %s ₪ התקנות לא מגבילות. משלמים ישירות לעורך הדין ומקבלים חשבונית." % (num(C["fixed"]), num(C["list_fee"]), num(C["ceiling"]))),
    ("האם התעריף המינימלי של לשכת עורכי הדין מחייב?", "לא. הכללים עצמם קובעים שהתעריף הוא המלצה לחברי הלשכה שאינה מחייבת. לעריכת חוזה על 2 מיליון ₪ הוא %s ₪ ועוד מע״מ, יותר ממה שרוב המשרדים מפרסמים." % num(tariff(2000000))),
    ("האם שכר הטרחה כולל מע״מ?", "כשהשכר נקוב באחוזים, בדרך כלל מדובר בסכום לפני מע״מ, ומוסיפים 18%%. ודאו שבהצעה כתוב במפורש אם המע״מ כלול."),
    ("מתי משלמים לעורך הדין?", "לפי הסכם שכר הטרחה. בקשו שהמועדים יהיו כתובים: כמה בחתימה וכמה ברישום, ומה קורה אם העסקה לא יוצאת לפועל."),
    ("האם עורך דין אחד יכול לייצג את הקונה ואת המוכר?", "כלל 14 לכללי האתיקה אוסר ייצוג צדדים בעלי אינטרסים מנוגדים באותו עניין, ומתיר עריכת הסכם בידי אותו עורך דין רק בהסכמת הצדדים בכתב. גם אז הוא לא מייצג רק אתכם. מומלץ שלכל צד יהיה עורך דין משלו."),
    ("האם עורך הדין של הקבלן מייצג אותי?", "לא. הוא מייצג את הקבלן ומטפל גם ברישום הזכויות שלכם, אבל אינו רשאי לייעץ לכם בנפרד. אתם רשאים לשכור עורך דין משלכם לחוזה ולמשא ומתן."),
    ("מהם השלבים בתהליך קניית דירה?", "בדיקות לפני הצעה, משא ומתן על החוזה, חתימה ותשלום ראשון בנאמנות, הערת אזהרה, הצהרה לרשות המסים בתוך 30 יום, מס רכישה בתוך 60 יום, משכנתא, מסירה, ורישום הבעלות."),
    ("מהן העלויות הנוספות ברכישת דירה?", "מס רכישה לפי המדרגות, שכר טרחת עורך דין, שמאי, בדק בית, אגרות טאבו של מאות שקלים, ועמלות המשכנתא. מחשבון עלות הרכישה הכוללת באתר מחבר את כולם."),
    ("מהן הבדיקות שיש לבצע לפני קניית דירה?", "משפטיות: נסח טאבו או אישור זכויות, תיק הבית המשותף, היתר וטופס 4, חובות לעירייה. הנדסיות: בדק בית. כלכליות: שמאי ואישור עקרוני למשכנתא."),
    ("עד מתי מדווחים על העסקה לרשות המסים?", "בתוך 30 יום מהעסקה, ומס הרכישה משולם בתוך 60 יום. על איחור בתשלום: 0.2%% מהמס לכל שבוע ועוד הצמדה וריבית."),
    ("מה זו מקדמה על מס שבח?", "תשלום שהקונה מעביר לרשות המסים על חשבון מס השבח של המוכר: 7.5%% מהמחיר, או 15%% בנכס שנרכש לפני 7.11.2001, אחרי ששולמו יותר מ-40%% מהתמורה. אפשר לבקש להקטין אותה עד מועד ההצהרה."),
    ("כמה עולה הערת אזהרה?", "אגרת הרישום בטאבו היא %s ₪ ב-2026, ומחיקה לבקשת הצדדים %s ₪. שכר עורך הדין על הרישום נפרד." % (num(LANDF["warn"]), num(LANDF["warn_del"]))),
    ("כמה עולה נסח טאבו?", "נסח מאושר במסר אלקטרוני: %s ₪ ב-2026. העתק או נסח מאושר אחר: %s ₪." % (num(LANDF["extract"]), num(LANDF["extract_paper"]))),
    ("מה ההבדל בין זיכרון דברים לחוזה?", "זיכרון דברים שכולל את הפרטים המהותיים, כמו הצדדים, הנכס, המחיר והמועדים, עלול לחייב כמו חוזה. לכן לא חותמים עליו בלי עורך דין."),
    ("האם צריך עורך דין לדירה מקבלן אם יש לקבלן עורך דין?", "כדאי. עורך הדין של הקבלן מייצג את הקבלן. עורך דין משלכם בודק את החוזה, את המפרט, את לוח התשלומים ואת הערבויות, ומנהל את המשא ומתן."),
    ("איך בוחרים עורך דין מקרקעין?", "לפי ניסיון בעסקאות כמו שלכם, הצעה כתובה שאומרת מה כלול, אם המע״מ כלול ומתי משלמים, מי מטפל בתיק בפועל, ובדיקה שעורך הדין רשום בלשכת עורכי הדין."),
    ("איך מגישים תלונה על עורך דין?", "לוועדת האתיקה של לשכת עורכי הדין במחוז שבו עורך הדין רשום. מצרפים את הסכם שכר הטרחה, את ההתכתבויות ואת המסמכים."),
    ("כמה עולה עורך דין לדירה חדשה מקבלן?", "עורך דין משלכם לדירה מקבלן: משרד שפרסם מחירים מציין 5,000 עד 15,000 ₪ ועוד מע״מ. בנפרד, הקבלן רשאי לגבות על עורך הדין שלו עד %s ₪ או 0.5%% מהמחיר, הנמוך, ועוד מע״מ." % num(C["fixed"])),
    ("האם עורך הדין מטפל גם ברישום המשכנתא?", "בדרך כלל כן: הערת האזהרה לטובת הבנק, שטרי המשכנתא והרישום. אגרת רישום משכנתה בטאבו: %s ₪ ב-2026. התעריף המומלץ של הלשכה לרישום משכנתא: 0.5%% מהחוב ולא פחות מ-1,012 ₪, כהמלצה." % num(LANDF["mortgage"])),
    ("מה ההבדל בין רישום בטאבו, ברמ״י ובחברה משכנת?", "הזכויות בדירה רשומות באחד משלושה מקומות: לשכת רישום המקרקעין (טאבו), רשות מקרקעי ישראל או חברה משכנת. בכל אחד המסמכים לבדיקה ולהעברה שונים, ועורך הדין צריך לדעת איפה הדירה רשומה לפני החתימה."),
    ("כמה עולה עורך דין למתנה בתוך המשפחה או לירושה?", "משרדים רבים גובים סכום קבוע ולא אחוז. בנוסף: אגרת רישום ירושה או צוואה בטאבו %s ₪ ב-2026. בקשו הצעה כתובה." % num(LANDF["inherit"])),
    ("האם האתר ממליץ על עורך דין מסוים?", "לא. אנחנו אתר מידע: איננו מייצגים קונים, מוכרים או יזמים, ואיננו גובים עמלה על עסקה. כאן תמצאו מה לשאול ואיך לבדוק, כדי שתבחרו עורך דין משלכם."),
]
FAQ_NEW = [(q, a.replace("%%", "%")) for q, a in FAQ_NEW]
assert len(FAQ_NEW) == 24

# ------------------------------------------------------------------ English + method
EN_T = tbl("Israel: lawyer fees and the developer cap (2026)", ["Item", "Amount"], [
    ["Fee published by law offices", "about 0.5% plus VAT, up to 1%, minimum about 5,000 to 6,000 NIS"],
    ["Bar Association recommended minimum (non-binding), contract on 2M NIS", "%s NIS plus VAT" % num(tariff(2000000))],
    ["What a developer may charge you for its lawyer", "lower of %s NIS and 0.5%% of the price, plus VAT; no cap above %s NIS" % (num(C["fixed"]), num(C["ceiling"]))],
    ["Warning note at the Land Registry", "%s NIS" % num(LANDF["warn"])], ["Tax declaration / purchase tax", "within 30 / 60 days of signing"]], minw=480)
EN = ('<section class="%s-en" lang="en" dir="ltr">\n<h2>Real estate lawyer in Israel: fees, the developer cap and the steps</h2>\n'
      '<p>An Israeli real estate lawyer checks the title and the seller, drafts or reviews the contract, registers a warning note, files the tax declaration within 30 days and transfers the title to you. '
      'Law offices published fees of about 0.5%% of the price plus 18%% VAT in 2026. When you buy a new apartment, the developer may charge you for its own lawyer no more than the lower of %s NIS and 0.5%% of the price, plus VAT; above %s NIS there is no cap. '
      'One lawyer may not represent sides with opposing interests (Bar ethics rule 14); hire your own. Buying from abroad: <a href="/en/buy-property-in-israel/">buying property in Israel</a>.</p>\n'
      % (PFX, num(C["fixed"]), num(C["ceiling"])) + EN_T + '</section>\n')
METHOD = ('<p class="%s-note">עודכן %s. החוקים, התקנות והתעריף המומלץ בנוסחם היום (סכומי 2026); שכר הטרחה כפי שפורסם בארבעה פרסומים ב-2026. המידע כללי ואינו ייעוץ משפטי.</p>\n' % (PFX, UPDATED))

# ------------------------------------------------------------------ the live content, the anchors
req, raw, r = get_live(PID, DRY)
FAQ_LAST = "חשוב לשאול מראש מה כלול בשירות.</p>"
OLD_PAY = "בדרך כלל כל צד מיוצג על ידי עורך דין מטעמו ומשלם לו בנפרד. בעסקאות קבלן ייתכנו תשלומים נוספים לפי ההסכם, ולכן צריך לקרוא היטב את התנאים."
NEW_PAY = (OLD_PAY + " בדירה חדשה, הקבלן רשאי לגבות מכם על עורך הדין שלו לכל היותר %s ₪ או 0.5%% מהמחיר, הנמוך מביניהם, ועוד מע״מ (2026); מעל %s ₪ אין תקרה." % (num(C["fixed"]), num(C["ceiling"])))
OLD_CLAIM = "המשך הקריאה במדריכים שבדקנו עבורך באותו אשכול נושאי. כתוב ונבדק על-ידי עורך דין מקרקעין."
NEW_CLAIM = "המשך הקריאה במדריכים באותו אשכול נושאי."
R = [
    ("<h2>%s</h2>" % H1_OLD, "<h2>%s</h2>\n" % H1_NEW + ANSWER),
    (before_block(raw, "מה עורך דין מקרקעין בודק לפני קניית דירה?"), TOOL),
    (before_block(raw, "נסח טאבו: נקודת פתיחה, לא סוף הבדיקה"), S_FEE),
    (before_block(raw, "מתי פונים לעורך דין מקרקעין?"), S_STEPS),
    (before_block(raw, "עורך דין ברכישת דירה להשקעה"), S_NEW),
    (before_block(raw, "מה להכין לפני פנייה לעורך דין?"), S_FEESREG),
    (before_block(raw, "טעויות נפוצות בעסקאות מקרקעין"), S_CHOOSE),
    (OLD_PAY, NEW_PAY),
    (FAQ_LAST, FAQ_LAST + "\n" + faq(FAQ_NEW)),
    (OLD_CLAIM, NEW_CLAIM),
]
R = [R[0]] + [(o, n + o) for o, n in R[1:7]] + R[7:]
new = apply(raw, R) + "\n" + EN + METHOD
# HAD-607, two small fixes on this page only: the hero photo was a 404 (the Commons file is gone), and the three batch-link blocks carry the
# placeholder heading "מדריך חדש". The photo: Tel Aviv-Yafo from Jaffa, 5.1.2026, CC BY-SA 4.0, credited in the caption.
OLD_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Tel_Aviv_skyline_from_Jaffa_%282019%29.jpg/960px-Tel_Aviv_skyline_from_Jaffa_%282019%29.jpg"
NEW_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Tel_Aviv-Yafo%2C_5_January_2026_23.jpg/960px-Tel_Aviv-Yafo%2C_5_January_2026_23.jpg"
OLD_CAP = "<figcaption>לפני חתימה, בודקים זכויות, חוזה, מס, בטוחות ולוח תשלומים.</figcaption>"
NEW_CAP = ('<figcaption>לפני חתימה, בודקים זכויות, חוזה, מס, בטוחות ולוח תשלומים. <small>צילום: תל אביב-יפו מיפו, 5.1.2026, '
           '<a href="https://commons.wikimedia.org/wiki/File:Tel_Aviv-Yafo,_5_January_2026_23.jpg" rel="nofollow">מקף־עברי</a>, CC BY-SA 4.0</small></figcaption>')
PH_OLD, PH_NEW = '<h2 dir="rtl">מדריך חדש</h2>', '<h2 dir="rtl">מדריך משלים</h2>'
print("  HAD-607: photo %d, caption %d, placeholder headings %d" % (new.count(OLD_IMG), new.count(OLD_CAP), new.count(PH_OLD)))
if new.count(OLD_IMG) == 1:
    new = new.replace(OLD_IMG, NEW_IMG).replace(OLD_CAP, NEW_CAP)
new = new.replace(PH_OLD, PH_NEW)
NEWS = [ANSWER, TOOL, S_FEE, S_STEPS, S_NEW, S_FEESREG, S_CHOOSE, faq(FAQ_NEW), EN, METHOD]
print("[page %d] live content modified %s, %d chars; %d anchors matched once each (%s)" % (PID, r.get("modified"), len(raw), len(R), "public REST, rendered" if DRY else "raw"))
qs = gates("".join(NEWS) + NEW_PAY, new, 4 + 24)
inner, bad, offi = check_links("".join(NEWS))
assert not bad, ("internal links must answer 200", bad)
c_all, c_old = counts(new), counts(raw)
print("  page now: %s | before: %s" % (json.dumps(c_all, ensure_ascii=False), json.dumps(c_old, ensure_ascii=False)))
print("  FAQ %d (4 old + 24 new); internal links %d all 200; external: %s" % (len(qs), len(inner), ", ".join("%s %s" % (h.split("/")[2], st) for h, st in offi)))
print("  H1 %d chars, SEO title %d, description %d; language gates passed; svg text >= 12px" % (len(H1_NEW), len(SEO_T), len(SEO_D)))

SRC = """# /real-estate-lawyer/ (page 11): where every fact on the page comes from (internal, written by write_g8_page.py, %s)

| Fact | Source |
|---|---|
| Developer lawyer cap: lower of 5,000 indexed (5,915 in 2026) and 0.5%%, before VAT; not above 4,642,750; paid directly, invoice; own lawyer allowed | תקנות המכר (דירות) (הגבלת גובה ההוצאות המשפטיות), התשע"ה-2014, regs. 2-4 and the 2026 notice (ק"ת תשפ"ו 987, takanot-12242.pdf); חוק המכר (דירות) s.6ג |
| 2024 / 2025 amounts (5,575.06 / 5,770.77) and the 300 NIS list fee | kolzchut.org.il (updated 3.2.2026), citing the price-control order |
| Bar recommended minimum tariff 2026: contract tiers 95,004 / 377,607 / 761,062 / 2,283,281 / 3,806,082, min 790, above 37,761; registration 1%% to 633,967 then 0.75%%; warning note 748 / 1,068; mortgage 0.5%% min 1,012; developer 1%%, buyer 0.25%%; non-binding | כללי לשכת עורכי הדין (התעריף המינימלי המומלץ), התש"ס-2000, s.2 and the schedule (Wikisource "all amounts updated to 2026"; י"פ תשפ"ו 2512, yalkut-14118.pdf) |
| Land Registry fees 2026: sale 44, warning note 188, deletion 127, mortgage 188, electronic extract 18, certified copy 88, inheritance 188 | תקנות המקרקעין (אגרות), התשל"ה-1974, the schedule (Wikisource, 2026 amounts) |
| Declaration 30 days, purchase tax 60 days, 0.2%% a week | ptax.json "pay" (Tax Authority buyer guide 2026) |
| CGT advance 7.5%% / 15%% (before 7.11.2001), after more than 40%%, reduction on request | חוק מיסוי מקרקעין (שבח ורכישה) s.15(ב)-(ה) |
| One lawyer for both sides | כללי לשכת עורכי הדין (אתיקה מקצועית), התשמ"ו-1986, rule 14(ב), (ד) |
| Published fees | doron-aharoni.com (12.10.2026), addalaw.co.il (2.7.2026), gelberglaw.co.il (22.9.2026), bizportal (6.8.2026, already in cost.json) |
""" % UPDATED
io.open(os.path.join(H, "page-sources-g8.md"), "w", encoding="utf-8").write(SRC)

if DRY:
    pv = os.path.join(H, "preview"); os.makedirs(pv, exist_ok=True)
    io.open(os.path.join(pv, "g8-page-content.html"), "w", encoding="utf-8", newline="").write(new)
    render_shell(os.path.join(pv, "g8-page-render.html"), "/real-estate-lawyer/", "", new.replace("<h2>%s</h2>" % H1_NEW, '<h1 class="nl-h1-from-h2">%s</h1>' % H1_NEW, 1), ["orechdin"])
    print("  --dry: wrote preview/g8-page-content.html, preview/g8-page-render.html, page-sources-g8.md; nothing was posted")
    sys.exit(0)

bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw + "\n<!-- title " + repr((r.get("title") or {}).get("raw")) + " | meta " + repr((r.get("meta") or {}).get("_yoast_wpseo_title")) + " | " + repr((r.get("meta") or {}).get("_yoast_wpseo_metadesc")) + " -->")
req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new, "title": TITLE, "meta": {"_yoast_wpseo_title": SEO_T, "_yoast_wpseo_metadesc": SEO_D}})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,title" % PID)[1]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers=UA), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
title = re.search(r"<title>(.*?)</title>", page, re.S).group(1).strip()
ok = {"read-back": back["content"]["raw"].strip() == new.strip(), "one h1": bd.count("<h1") == 1, "h1 text": H1_NEW in bd, "tool mounted": 'data-nli="orechdin"' in bd,
      "shortcode rendered": "[nadlan_tool" not in bd, "svg x3": bd.count("%s-fig" % PFX) == 3, "one FAQPage": page.count('"@type":"FAQPage"') == 1, "28 questions": page.count('"@type":"Question"') == 28,
      "SoftwareApplication": '"@type":"SoftwareApplication"' in page, "orechdin.js enqueued": "tools/orechdin.js" in page, "SEO title": title.startswith(SEO_T), "updated": ("עודכן %s" % UPDATED) in bd,
      "unverified claim gone": "כתוב ונבדק על-ידי עורך דין" not in bd, "photo fixed": "Tel_Aviv_skyline_from_Jaffa" not in bd, "no placeholder heading": "מדריך חדש" not in bd}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
