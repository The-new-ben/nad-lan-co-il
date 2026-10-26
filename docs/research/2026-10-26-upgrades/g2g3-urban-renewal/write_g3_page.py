# -*- coding: utf-8 -*-
"""G3 on /urban-renewal/ (page 73): the owner page of "התחדשות עירונית" (8,100 searches a month), the umbrella of the cluster:
the tracks side by side, the tax and authorities tracks, TAMA 38 and what replaces it in each city, the authority, the numbers,
urban renewal by city. Spec: dna.md sections 5, 6 and 7. NOT RUN: Ben's word first (local-only round).

What it does, every number from plugins/nadlan-config/assets/instruments/data/urcity.json, pinui.json, renewal-track.json or the
dated facts of dna.md section 5:
  1. the H1 and, right under it, the answer paragraph, three CTAs, the tool [nadlan_tool id="urcity"] and the numbers table T1;
  2. new sections at exact anchors: the three tracks side by side (I1, T2), the tax and authorities tracks (I2, T3, T4), TAMA 38 in
     every city (T5, T6, I3, T7), urban renewal by city (T8, city H3s), the authority and the administrations;
  3. 18 new FAQ (h3 + p) after the 7 old ones = 25, an English section and the method line with "עודכן 26.10.2026";
  4. fixes inside the old text: the "בקרוב" promise of a project room that exists today (/my-renewal/), "מערכת" and "מודל" in the
     start band, and the start band, the two small link lines, the Tel Aviv cluster box and the old infographic frame moved from the
     cream, brown and terracotta palette to the Instruments palette (style attributes only, text kept);
  5. the Yoast title (71 chars and four protected terms of other pages today -> 57 chars, only its own term) and description.
  python write_g3_page.py --dry   public REST only (no login): anchors checked against the live rendered content, writes
                                  preview/g3-page-content.html, preview/g3-page-render.html and page-sources-g3.md
  python write_g3_page.py         (NOT to be run without Ben's word) backup, POST, read-back, live check"""
import io, json, math, os, re, sys, time, urllib.parse, urllib.request

H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from g2g3_common import *  # noqa: E402,F401
import infographics as ig  # noqa: E402

DRY = "--dry" in sys.argv
PID = 73; PFX = "nlur3"
TITLE = "התחדשות עירונית: המסלולים, המספרים והמתחמים בכל עיר | נדלן"
DESC = "התחדשות עירונית בישראל: פינוי בינוי, תמ\"א 38 ותכנית לרישוי מהיר זה לצד זה, 993 מתחמים ב-79 ערים במפת הרשות, תמ\"א 38 בכל עיר, ובדיקה לבניין שלכם."
H1_OLD = '<h1 class="nlur-h1">התחדשות עירונית: מה בודקים לפני שחותמים</h1>'
H1_NEW = '<h1 class="nlur-h1">התחדשות עירונית: המסלולים, המספרים בכל עיר ומה בודקים לפני שחותמים</h1>'
assert len(TITLE) <= 60 and len(DESC) <= 160, (len(TITLE), len(DESC))
tbl = Tables(PFX); B = U["building2025"]; AVG = P["series"]["approval_to_permit"][-1]
WATXT = urllib.parse.quote("שלום, הגעתי מהמדריך להתחדשות עירונית באתר נדלן ואשמח לפרטים נוספים")
STG = ["ללא שלב במפה", "תכנון ראשוני", "תכנון סטטוטורי", "תכנית מאושרת לפני מימוש", "תכנית מאושרת במימוש", "אחרי רישוי"]


def same(name, got, want): assert got == want, ("cross-check", name, got, want)


same("map", (NCX, NCITY), (993, 79)); same("stages", STAGE_N[:5], [188, 105, 302, 345, 53]); same("tracks", TRACK_N[1:], [551, 240, 202])
same("key", (K["ur_share_approved"], K["starts_share"], K["permits_units"]), (35, 28, 28902))

# ------------------------------------------------------------------ per city: the map (renewal-track.json) + the report (urcity.json)
def find(lst, c): return next((x for x in lst if x["c"] == c), None)


CITY = {}
for r in ON:
    c = CITY.setdefault(r["c"], {"n": 0, "appr": 0, "e": 0, "p": 0, "pe": 0, "pp": 0})
    c["n"] += 1; s = r["s"][LM]
    if s >= 3: c["appr"] += 1
    c["e"] += r.get("e", 0) or 0; c["p"] += r.get("p", 0) or 0
    if r.get("e") and r.get("p"): c["pe"] += r["e"]; c["pp"] += r["p"]
for k, c in CITY.items(): c["mult"] = c["pp"] / c["pe"] if c["pe"] else 0


def tama_line(c):
    r = find(U["replace"], c)
    if r: return r["st"] + ("" if r["ext"] else "; בלי הארכה לתמ\"א 38")
    if c in U["inforce"]: return "תכנית עירונית בתוקף ערב הפקיעה"
    return ""


TOPC = sorted(CITY, key=lambda c: (-CITY[c]["n"], c))[:30]

# ------------------------------------------------------------------ tables
T1 = tbl("התחדשות עירונית במספרים: 2025 ומפת הרשות היום", ["נושא", "המספר", "המקור"], [
    ["החלק של התחדשות עירונית מהדירות שאושרו בתכנון ב-2025", "%d%%" % K["ur_share_approved"], "דוח הרשות לשנת 2025"],
    ["החלק שלה מהתחלות הבנייה", "%d%%" % K["starts_share"], "שם"],
    ["דירות שנמכרו במיזמי התחדשות", "כל דירה חמישית שנמכרה ב-2025", "שם"],
    ["היתרי בנייה ב-2025", "%s דירות: %s בפינוי בינוי (%d מתחמים) ו-%s בהתחדשות בניינית (%d מבנים)" % (num(K["permits_units"]), num(K["permits_pb_units"]), K["permits_pb_complexes"], num(K["permits_bld_units"]), K["permits_bld_projects"]), "שם, עמ' 22"],
    ["תכניות פינוי בינוי שאושרו ב-2025", "%d, עם %s דירות" % (K["pb_plans"], num(K["pb_units"])), "שם, עמ' 25"],
    ["תכניות עירוניות שמחליפות את תמ\"א 38, בתכנון ב-2025", "%d, עם תוספת של כ-%s דירות" % (K["replace_plans"], num(K["replace_added"])), "שם, עמ' 22"],
    ["מתחמים במפת הרשות", "%s ב-%d ערים (%s)" % (num(NCX), NCITY, dmy(MAPD)), "מפת הרשות"],
    ["מסלול מיסוי / רשויות / טרם הוכרז", "%d / %d / %d" % tuple(TRACK_N[1:]), "שם"],
    ["דירות במתחמים: היום ואחרי הבנייה", "%s ← %s" % (num(STATS["map"]["existing"]), num(STATS["map"]["proposed"])), "שם"],
    ["מינהלות עירוניות להתחדשות", num(K["minhalot"]), "דוח הרשות, עמ' 18"],
    ["תקציב הרשות ב-2025", "%d מיליון ₪ בהרשאה להתחייב" % K["budget_m"], "שם, עמ' 18"]], minw=0)

A = U["tracks"]
T2 = tbl("שלושת המסלולים של התחדשות עירונית, זה לצד זה (נספח א לדוח הרשות לשנת 2025)", ["מאפיין"] + [t["name"] for t in A], [
    ["מה עושים"] + [t["do"] for t in A], ["הבניין"] + [t["bld"] for t in A], ["איך מאשרים"] + [t["route"] for t in A],
    ["הכרזה על מתחם"] + [t["declare"] for t in A], ["חובת תכנית"] + [t["plan"] for t in A], ["היקף במצב הקיים"] + [t["scope"] for t in A], ["זכויות במצב החדש"] + [t["rights"] for t in A],
    ["הרוב בחוק", "שני שלישים מהדירות במקבץ, שלוש חמישיות בכל בניין, יותר ממחצית הרכוש המשותף", "חיזוק עם דירות חדשות או הריסה: שני שלישים מהדירות ומהרכוש המשותף, באישור המפקח; הרחבה בלבד: 60%", "כמו בתמ\"א 38"],
    ["פטור ממס שבח", "פרק חמישי 4, בלי הגבלה על מספר הדירות", "פרק חמישי 5, עד סוף 2033; בהריסה 2 דירות בבניין", "כמו בתמ\"א 38"],
    ["תקרת הפטור", "120 מ\"ר, 150% מהשווי, או 50% יותר עד 200 מ\"ר", "חיזוק: 25 מ\"ר; הריסה: 25 מ\"ר או שווי עד 1,777,600 ₪", "כמו בתמ\"א 38"],
    ["היטל השבחה", "25%, או לפי העירייה 50% או פטור, לתכניות שייקלטו עד מאי 2027", "פטור לזכויות התמ\"א; בהריסה 25% מעבר ל-2.5 קומות", "25% עד הזכויות שבחוק, 50% מעליהן"],
    ["זכויות מרביות", "לפי התכנית", "לפי התמ\"א", "הריסה ובנייה עד 400%, באיחוד 3 מגרשים עד 500%, חיזוק 200%"]], minw=720)

TD = P["series"]["taxdecl"]
T3 = tbl("מתחמים שהוכרזו במסלול המיסוי בכל שנה (דוח הרשות, עמ' 70)", ["שנה", "מתחמים", "דירות מוצעות"], [[str(y), str(n), num(u)] for y, n, u in reversed(TD)], minw=360, num_cols=True)
T4 = tbl("החלטות מקדמיות במסלול המיסוי, מצטבר עד סוף 2025, לפי מחוז (דוח הרשות, עמ' 68)", ["מחוז", "מתחמים", "דירות היום", "דירות מוצעות"],
         [[d, str(n), num(e), num(p)] for d, n, e, p in U["taxpre"]] + [["סך הכול", str(sum(r[1] for r in U["taxpre"])), num(sum(r[2] for r in U["taxpre"])), num(sum(r[3] for r in U["taxpre"]))]], minw=440, num_cols=True)
same("T4 total", sum(r[1] for r in U["taxpre"]), 627)

RP = [x for x in U["replace"] if not x.get("self")]
T5 = tbl("תמ\"א 38 בכל עיר: התכניות העירוניות שמחליפות אותה (דוח הרשות לשנת 2025, עמ' 92 ו-93)", ["עיר", "מצב התכנית", "מבנים בתכנית", "דירות היום", "דירות מוצעות", "הארכה לתמ\"א 38"],
         [[x["name"], x["st"], num(x["bld"]), num(x["e"]), num(x["p"]), "הוארכה עד אישור התכנית" if x["ext"] else "לא הוארכה"] for x in RP]
         + [[x["name"], x["st"], "", "", "", "הוארכה עד אישור התכנית" if x["ext"] else "לא הוארכה"] for x in U["replace"] if x.get("self")], minw=680)
T6 = tbl("התחדשות בניינית ב-2025: בקשות, היתרים ואכלוס (דוח הרשות, עמ' 96)", ["", "חיזוק ועיבוי", "הריסה ובנייה מחדש", "סך הכול"], [
    ["בקשות להיתר: מבנים / דירות", "%d / %s" % (B["requests"]["strengthen"][0], num(B["requests"]["strengthen"][1])), "%d / %s" % (B["requests"]["rebuild"][0], num(B["requests"]["rebuild"][1])), "%d / %s" % tuple([B["requests"]["total"][0], num(B["requests"]["total"][1])])],
    ["היתרים שניתנו: מבנים / דירות", "%d / %s" % (B["permits"]["strengthen"][0], num(B["permits"]["strengthen"][1])), "%d / %s" % (B["permits"]["rebuild"][0], num(B["permits"]["rebuild"][1])), "%d / %s" % (B["permits"]["total"][0], num(B["permits"]["total"][1]))],
    ["דירות שנוספו בהיתרים", num(B["added"]["strengthen"]), num(B["added"]["rebuild"]), num(B["added"]["total"])],
    ["מבנים שאוכלסו / דירות", "%d / %s" % (B["occupied"]["strengthen"][0], num(B["occupied"]["strengthen"][1])), "%d / %s" % (B["occupied"]["rebuild"][0], num(B["occupied"]["rebuild"][1])), "%d / %s" % (B["occupied"]["total"][0], num(B["occupied"]["total"][1]))]], minw=480, num_cols=True)
RQ = sorted(U["req2permit"], key=lambda x: -x["y"])
T7 = tbl("התחדשות בניינית: כמה שנים מהבקשה ועד ההיתר, לפי עיר, היתרים שניתנו ב-2025 (דוח הרשות, עמ' 109 ו-110)", ["עיר", "שנים בממוצע", "היתרים ב-2025"], [[x["c"], "%.1f" % x["y"], str(x["n"])] for x in RQ], minw=360, num_cols=True)


def sold(c): x = find(U["sold"], c); return num(x["n"]) if x else ""


T8 = tbl("התחדשות עירונית לפי עיר: 30 הערים עם הכי הרבה מתחמים במפת הרשות (%s)" % dmy(MAPD), ["עיר", "מתחמים", "מאושרת או במימוש", "דירות אחרי הבנייה", "מכפיל (החישוב שלנו)", "דירות שנמכרו ב-2025", "תמ\"א 38 בעיר"],
         [[c, str(CITY[c]["n"]), str(CITY[c]["appr"]), num(CITY[c]["p"]), "%.2f" % CITY[c]["mult"] if CITY[c]["mult"] else "", sold(c), tama_line(c)] for c in TOPC], minw=760)


def city_h3(c, name=None):
    x = CITY.get(c); rq = find(U["req2permit"], c); so = find(U["sold"], c); tx_ = find(U["taxcity"], c); tl = tama_line(c)
    parts = ["במפת הרשות יש ב%s %d מתחמים (%s), %d מהם בתכנית מאושרת או במימוש, עם %s דירות היום ו-%s אחרי הבנייה; מכפיל של %.2f לפי החישוב שלנו." % (name or c, x["n"], dmy(MAPD), x["appr"], num(x["e"]), num(x["p"]), x["mult"])]
    if tx_: parts.append("עד סוף 2025 הוכרזו בעיר %d מתחמים במסלול המיסוי, עם %s דירות מוצעות." % (tx_["n"], num(tx_["p"])))
    if tl: parts.append("תמ\"א 38: %s (דוח הרשות לשנת 2025)." % tl)
    if rq: parts.append("בהתחדשות בניינית עברו %.1f שנים בממוצע מהבקשה ועד ההיתר (%d היתרים ב-2025)." % (rq["y"], rq["n"]))
    if so: parts.append("ב-2025 נמכרו בעיר %s דירות במיזמי התחדשות." % num(so["n"]))
    return "<h3>התחדשות עירונית ב%s</h3>\n<p>%s</p>\n" % (name or c, " ".join(parts))


CITIES_H3 = [("ירושלים", None), ("חיפה", None), ("תל אביב יפו", "תל אביב יפו"), ("רמת גן", None), ("באר שבע", None), ("פתח תקוה", "פתח תקווה"), ("נתניה", None), ("בת ים", None), ("חולון", None), ("ראשון לציון", None)]
for c, _ in CITIES_H3: assert c in CITY, c

# ------------------------------------------------------------------ the new copy
TOP = (css(PFX) + H1_NEW + "\n" +
       '<p class="nlur3-answer"><strong>התחדשות עירונית היא חיזוק, הרחבה או הריסה ובנייה מחדש של בנייני מגורים ותיקים, במימון זכויות בנייה שהיזם מקבל, כך שבעלי הדירות לא משלמים מכיסם.</strong> יש לה שלושה מסלולים: פינוי בינוי של מתחם שלם, תמ"א 38 לבניין אחד, ותכנית לרישוי מהיר, שנקראת גם חלופת שקד. ב-2025 התחדשות עירונית הייתה %d%% מהדירות שאושרו בתכנון ו-%d%% מהתחלות הבנייה, ובמפת הרשות הממשלתית להתחדשות עירונית יש היום %s מתחמים ב-%d ערים (%s).</p>\n'
       % (K["ur_share_approved"], K["starts_share"], num(NCX), NCITY, dmy(MAPD)) +
       '<div class="nlur3-cta"><a class="nlur3-go" href="#urcity-tool">התחדשות עירונית בעיר שלכם</a><a href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">לקבלת פרטים נוספים בוואטסאפ</a><a href="/urban-renewal/check/">בדיקת בניין חינמית</a></div>\n' % (WA, WATXT) +
       '<div id="urcity-tool" class="nlur3-tool">\n[nadlan_tool id="urcity"]\n</div>\n' + T1)

TRACKS = ('<h2>שלושת המסלולים של התחדשות עירונית, זה לצד זה</h2>\n'
          '<p>ההבדל בין המסלולים הוא לא רק מה בונים, אלא מי מאשר, איזה רוב צריך ואיזה פטור ממס מקבלים. <a href="/urban-renewal/pinui-binui/">פינוי בינוי</a> עובד על מתחם של כמה בניינים, עם הכרזה ותכנית מפורטת. <a href="/urban-renewal/tama-38/">תמ"א 38</a> עובדת על בניין אחד שההיתר שלו ניתן לפני 1980, בהיתר בנייה בלי תכנית. התכנית לרישוי מהיר, לפי סעיף 145א1 לחוק התכנון והבנייה (תיקון 139), מחליפה את תמ"א 38 בתכנית בוועדה המקומית, ואפשר להגיש בקשה להיתר כבר בשלב ההפקדה. עוד עליה בעמוד <a href="/urban-renewal/tama-38-alternatives/">מה במקום תמ"א 38</a>.</p>\n' +
          fig(PFX, ig.g3_tracks(), "שלושה מסלולים: מה בונים, מי מאשר, הרוב בחוק, הסף ותקרת הפטור ממס. נספח א לדוח הרשות לשנת 2025.") + T2 +
          '<p>בהתחדשות בניינית, הריסה ובנייה מחדש עוקפת את החיזוק: ב-2025 היו %d%% מההיתרים בהריסה ובנייה ו-%d%% בחיזוק ועיבוי, לעומת %d%% ו-%d%% ב-2013. גם בבקשות להיתר: %d%% בהריסה ב-2025.</p>\n'
          % (U["permit_split"][-1][1], U["permit_split"][-1][2], U["permit_split"][0][1], U["permit_split"][0][2], U["request_split"][-1][1]) +
          fig(PFX, ig.g3_permit_split(), "היתרים בהתחדשות בניינית לפי מסלול, 2013 עד 2025. דוח הרשות לשנת 2025, עמוד 34."))

DECL = ('<h2>מסלול מיסוי ומסלול רשויות: איך מתחם מוכרז</h2>\n'
        '<p>מתחם פינוי בינוי מוכרז באחד משני מסלולים. ב<strong>מסלול המיסוי</strong> היזם מוביל: ההכרזה ניתנת כשהתכנית הופקדה להתנגדויות או אושרה, ונחתמו הסכמים עם 66%% לפחות מבעלי הדירות בכל מקבץ ו-60%% בכל בניין (דוח הרשות, עמוד 68). ב<strong>מסלול הרשויות</strong> הרשות הממשלתית או העירייה מקדמות את התכנון מכסף ציבורי, לפעמים לפני שיש יזם; ב-2025 הקצתה הרשות %s מיליון ₪ לתכנון. במפת הרשות היום: %d מתחמים במסלול המיסוי, %d במסלול הרשויות ו-%d שטרם הוכרזו.</p>\n'
        % ("94.1", TRACK_N[1], TRACK_N[2], TRACK_N[3]) +
        fig(PFX, ig.g3_taxdecl(), "מתחמים שהוכרזו במסלול המיסוי בכל שנה, 2015 עד 2025, והדירות המוצעות בהם. דוח הרשות לשנת 2025, עמוד 70.") + T3 + T4 +
        '<p class="nlur3-note">בדוח עצמו שתי הטבלאות של ההכרזות המצטברות לא מסתכמות זו לזו (בעמוד 71 השורות מסתכמות ב-336 מתחמים מול סך של 337, ובעמוד 72 הערים מסתכמות ב-133,044 דירות מול 133,321). לכן אנחנו מביאים כאן את ההחלטות המקדמיות של עמוד 68, שמסתכמות בדיוק, ואת הערים כפי שנכתבו.</p>\n'
        '<p>החשבון של הרוב, בניין אחר בניין, והמועדים שהחוק נותן ליזם, נמצאים במדריך <a href="/urban-renewal/pinui-binui/">פינוי בינוי</a>, עם מחשבון לבניין שלכם.</p>\n')

TAMA = ('<h2>תמ"א 38 בכל עיר: התכניות שמחליפות אותה</h2>\n'
        '<p>תוקף תמ"א 38 פקע באוקטובר 2023. בערים שמקדמות תכנית עירונית מחליפה, המועצה הארצית לתכנון ולבנייה האריכה את התוקף עד מאי 2026 או עד אישור התכנית העירונית, המוקדם מביניהם; בבני ברק ובבת ים לא, ובתל אביב יפו לא ניתנה הארכה. תכנית כזאת מחלקת את העיר לאזורים וקובעת לכל בניין את המסלול שלו, חיזוק ועיבוי או הריסה ובנייה מחדש, כך שאפשר להוציא היתר בלי תכנית נוספת (דוח הרשות לשנת 2025, עמודים 90 עד 93). מה חל היום בבניין שלכם בודקים בוועדה המקומית; הטבלה היא מה שהדוח כתב.</p>\n' + T5 +
        '<p class="nlur3-note">לפי הדוח, ערב פקיעת תמ"א 38 כבר הייתה בתוקף תכנית עירונית להתחדשות בניינית גם ב%s.</p>\n' % ", ".join(c.replace("יקנעם עילית", "יקנעם") for c in U["inforce"]) +
        '<h3>התחדשות בניינית ב-2025 במספרים</h3>\n' + T6 +
        '<p>הבקשות להיתר ירדו: %s דירות ב-2025 לעומת %s ב-2024, ירידה של כ-60%%. ההיתרים נשארו דומים: %s דירות ב-2025 ו-%s ב-2024. הזמן מהבקשה להיתר משתנה מאוד בין ערים:</p>\n'
        % (num(B["requests"]["total"][1]), num(B["requests2024_units"]), num(B["permits"]["total"][1]), num(B["permits2024_units"])) + T7)

CITIES = ('<h2>התחדשות עירונית לפי עיר</h2>\n'
          '<p>הטבלה מחברת שני מקורות: המתחמים מתוך מפת הרשות (%s), והשורות של דוח הרשות לשנת 2025 על המכירות ועל תמ"א 38. המכפיל הוא כמה דירות יהיו אחרי הבנייה לכל דירה שיש היום, במתחמים שיש להם את שני המספרים; בכל הארץ %.2f. את כל הערים, ואת המתחמים של כל עיר, מראה המחשבון בראש העמוד וגם <a href="/urban-renewal/map/">מפת התחדשות עירונית</a>.</p>\n'
          % (dmy(MAPD), MULT) + T8 + "".join(city_h3(c, n) for c, n in CITIES_H3))

AUTH = ('<h2>הרשות הממשלתית להתחדשות עירונית והמינהלות העירוניות</h2>\n'
        '<p>הרשות הממשלתית להתחדשות עירונית הוקמה בחוק ב-2016, והיא מכריזה על מתחמים, מממנת תכנון ומינהלות, מלווה דיירים ומפרסמת דוח שנתי. ב-2025 עמד התקציב שלה על %d מיליון ₪ בהרשאה להתחייב, ופעלו %d מינהלות עירוניות להתחדשות; מינהלת היא שירות של העירייה שמלווה דיירים בחינם, ואם אין כזאת בעיר פונים למחלקת ההנדסה. ברשות פועלת גם הממונה על פניות הדיירים: ב-2025 הוגשו לה כ-%d פניות, והיא הכריעה בכ-%d, כולל משנים קודמות.</p>\n'
        % (K["budget_m"], K["minhalot"], K["ombud_filed"], K["ombud_decided"]) +
        '<ul>\n<li><strong>שמאי בחינם:</strong> בעלי 40%% מהדירות במקבץ יכולים לבקש מהרשות שמאי פינוי ובינוי שיבדוק אם העסקה שהוצעה להם כדאית (<a href="https://www.gov.il/he/service/bakasha-leminuy-shamay-renewal" rel="nofollow noopener" target="_blank">הבקשה ב-gov.il</a>).</li>\n'
        '<li><strong>הסכמים לדוגמה:</strong> הרשות מפרסמת הסכם לדוגמה בין בעלי דירות ליזם בפינוי בינוי, הסכם לדוגמה לחיזוק ועיבוי והסכם לדוגמה לשירותים משפטיים.</li>\n'
        '<li><strong>מחשבון כדאיות:</strong> מחשבון פתוח לפי תקן 21, עם ההנחות שלו, למשל %d חודשים מהפינוי ועד דירת התמורה.</li>\n'
        '<li><strong>הדוח השנתי:</strong> <a href="https://www.gov.il/he/pages/urban_renewal_report_2025" rel="nofollow noopener" target="_blank">דוח הרשות לשנת 2025</a>, שפורסם ב-26.5.2026, הוא המקור של רוב המספרים בעמוד הזה.</li>\n</ul>\n' % P["model"]["evac_months"])

FAQ_NEW = faq([
    ("מה זה התחדשות עירונית?", "התחדשות עירונית היא שם כולל לחיזוק, הרחבה או הריסה ובנייה מחדש של בנייני מגורים ותיקים, ולשדרוג השטחים הציבוריים סביבם. היזם מקבל זכויות לבנות דירות נוספות ולמכור אותן, ובתמורה מחזק או בונה מחדש, בלי שבעלי הדירות משלמים על הבנייה. הפרויקט יכול לצאת לדרך רק בהסכמה של בעלי הדירות, כי הם בעלי הזכויות בקרקע."),
    ("מה ההבדל בין התחדשות עירונית לפינוי בינוי?", "התחדשות עירונית היא השם הכולל. <a href=\"/urban-renewal/pinui-binui/\">פינוי בינוי</a> הוא אחד המסלולים שלה: הריסה של מתחם של כמה בניינים ובנייה מחדש, עם הכרזה ותכנית מפורטת. שני המסלולים האחרים הם תמ\"א 38 לבניין אחד ותכנית לרישוי מהיר."),
    ("מה זה התחדשות בניינית?", "התחדשות בניינית היא התחדשות של בניין אחד: חיזוק ועיבוי או הריסה ובנייה מחדש, לפי תמ\"א 38, לפי תכנית עירונית שמחליפה אותה או לפי תכנית לרישוי מהיר. ב-2025 ניתנו היתרים ל-%d מבנים עם %s דירות, ו-%d%% מההיתרים היו בהריסה ובנייה." % (B["permits"]["total"][0], num(B["permits"]["total"][1]), U["permit_split"][-1][1])),
    ("מה קרה לתמ\"א 38?", "תוקף תמ\"א 38 פקע באוקטובר 2023. בערים שמקדמות תכנית עירונית מחליפה הוא הוארך עד מאי 2026 או עד אישור התכנית, המוקדם מביניהם; בתל אביב יפו לא ניתנה הארכה, וגם לא בבני ברק ובבת ים. לפי דוח הרשות לשנת 2025, תכניות כאלה אושרו ב-2024 וב-2025 ברמלה, ביבנה, ברעננה, בכפר סבא, בפתח תקווה, בבאר שבע, בלוד ובגבעתיים."),
    ("מה זה חלופת שקד?", "חלופת שקד היא השם המקובל לתכנית לרישוי מהיר לפי סעיף 145א1 לחוק התכנון והבנייה (תיקון 139). זו תכנית בוועדה המקומית לבניין של 2 קומות ו-4 דירות לפחות, עם זכויות של עד 400% בהריסה ובנייה, עד 500% באיחוד של 3 מגרשים ועד 200% בחיזוק. אפשר להגיש בקשה להיתר כבר בשלב ההפקדה. עוד בעמוד <a href=\"/urban-renewal/tama-38-alternatives/\">מה במקום תמ\"א 38</a>."),
    ("מי מממן התחדשות עירונית?", "היזם. לפי הרשות הממשלתית להתחדשות עירונית, היום מקובל שהיזמים משלמים על מלוא עלויות הפרויקט: הבנייה, שכר הדירה בתקופת הבנייה ואנשי המקצוע של הדיירים. את העלויות מכסה מכירת הדירות הנוספות, ולכן פרויקט צריך להיות כדאי כלכלית לפי תקן 21."),
    ("כמה זמן לוקחת התחדשות עירונית?", "בפינוי בינוי הרשות מודדת %.1f שנים בממוצע מאישור התכנית ועד היתר ראשון (%d מתחמים, 2025). בהתחדשות בניינית הזמן מהבקשה ועד ההיתר נע ב-2025 בין %.1f שנים ב%s ל-%.1f ב%s. התארגנות, חתימות ובנייה מתווספות לזה." % (AVG[1], AVG[2], RQ[-1]["y"], RQ[-1]["c"], RQ[0]["y"], RQ[0]["c"])),
    ("כמה מתחמי התחדשות עירונית יש בישראל?", "במפת הרשות היו ב-%s %s מתחמים ב-%d ערים: %d בתכנון ראשוני, %d בתכנון סטטוטורי, %d בתכנית מאושרת לפני מימוש, %d במימוש ו-%d בלי שלב במפה. בקובץ הפתוח ב-data.gov.il, שעודכן ב-15.8.2026, היו 970 מתחמים ב-76 ערים." % (dmy(MAPD), num(NCX), NCITY, STAGE_N[1], STAGE_N[2], STAGE_N[3], STAGE_N[4], STAGE_N[0])),
    ("באיזו עיר יש הכי הרבה התחדשות עירונית?", "במספר המתחמים במפת הרשות: %s." % ", ".join("%s %d" % (c, CITY[c]["n"]) for c in TOPC[:6]) + " במכירות של דירות במיזמי התחדשות ב-2025 מובילות תל אביב יפו (1,292), פתח תקווה (817) וירושלים (769), לפי דוח הרשות."),
    ("מה זה מסלול מיסוי ומה זה מסלול רשויות?", "במסלול המיסוי היזם מוביל, וההכרזה ניתנת כשהתכנית הופקדה או אושרה ונחתמו הסכמים עם 66%% בכל מקבץ ו-60%% בכל בניין. במסלול הרשויות הרשות או העירייה מקדמות את התכנון מכסף ציבורי. ב-2025 הוכרזו במסלול המיסוי %d מתחמים חדשים עם %s דירות." % (K["tax_new"], num(K["tax_new_units"]))),
    ("מה זו מינהלת התחדשות עירונית?", "מינהלת היא גוף של העירייה, בתמיכת הרשות הממשלתית, שמלווה דיירים בחינם: מידע, תכנון, תיווך מול יזמים. ב-2025 פעלו %d מינהלות ברשויות מקומיות. אם אין מינהלת בעיר שלכם, פונים למחלקת ההנדסה בעירייה." % K["minhalot"]),
    ("מה עושה הרשות הממשלתית להתחדשות עירונית?", "הרשות מכריזה על מתחמי פינוי בינוי, מממנת תכנון ומינהלות עירוניות, ממנה שמאי פינוי ובינוי לבקשת הדיירים, מפרסמת הסכמים לדוגמה ומחשבון כדאיות, ומפעילה את הממונה על פניות הדיירים. התקציב שלה ב-2025: %d מיליון ₪ בהרשאה להתחייב." % K["budget_m"]),
    ("יש פטור ממס בתמ\"א 38?", "כן. לפי נספח א לדוח הרשות: פטור ממס שבח לפי פרק חמישי 5, בתוקף עד סוף 2033, אין חבות במס רכישה, ומע\"מ אפס על שירותי הבנייה. בהריסה ובנייה הפטור הוא ל-2 דירות בבניין, ובחיזוק ועיבוי בלי הגבלה. התקרה: תוספת של 25 מ\"ר, ובהריסה גם דירה בשווי של עד 1,777,600 ₪."),
    ("מה זה היטל השבחה בהתחדשות עירונית?", "בפינוי בינוי במתחם מוכרז ההיטל הוא ככלל 25% מההשבחה, וממאי 2022 העירייה רשאית לקבוע לפי אזורים 25%, 50% או פטור, לתכניות שייקלטו עד מאי 2027. בתמ\"א 38 יש פטור מלא לזכויות שבתמ\"א, ובהריסה ובנייה 25% על זכויות מעבר ל-2.5 קומות; בתכנית לרישוי מהיר 25% עד הזכויות שבחוק ו-50% מעליהן."),
    ("מה זה תקן 21?", "תקן 21 של מועצת השמאים מגדיר איך בודקים את הכדאיות של פינוי בינוי: עלויות, טיפול בדיירים, קרן תחזוקה, היטל השבחה והכנסות היזם. מאז העדכון של 13.6.2022 הוא מציג טבלת רגישות של רווח היזם בכל תמורה, במקום תמורה מקובלת של כ-25 מ\"ר."),
    ("איך יודעים אם הבניין שלי במתחם התחדשות עירונית?", "בודקים במפת הרשות או בקובץ הפתוח ב-data.gov.il. ב<a href=\"/urban-renewal/map/\">מפת התחדשות עירונית</a> אצלנו, ביומן המתחמים, מחפשים לפי עיר, רחוב או מספר תכנית ורואים את השלב, המסלול ומה השתנה מאז הבדיקה הקודמת. בניין שלא נמצא יכול עדיין להתאים למסלול בניין בודד."),
    ("כמה חתימות צריך להתחדשות עירונית?", "תלוי במסלול. בפינוי בינוי: שני שלישים מהדירות במקבץ, שלוש חמישיות בכל בניין ויותר ממחצית הרכוש המשותף. בתמ\"א 38 עם דירות חדשות או בהריסה ובנייה: שני שלישים מהדירות ומהרכוש המשותף, באישור המפקח על המקרקעין; בהרחבת דירות בלבד 60%. המחשבון בראש העמוד מחשב את זה לבניין שלכם."),
    ("איך נמנעים מעסקה פוגענית בהתחדשות עירונית?", "לפני העסקה הראשונה היזם חייב לכנס את בעלי הדירות ולמסור מסמך עיקרי הצעה שבועיים מראש; אם לא, רוב יכול לבטל כל עוד חתמו פחות מ-40%%. הממונה על פניות הדיירים יכולה לבטל עסקה שנחתמה בהחתמה פוגענית, למשל בשפה שבעל הדירה לא מבין או עם מידע מטעה. ב-2025 הוגשו לה כ-%d פניות." % K["ombud_filed"]),
])

EN = ('<h2 lang="en" dir="ltr" class="nlur3-en">Urban renewal in Israel: the short answer in English</h2>\n'
      '<div lang="en" dir="ltr" class="nlur3-en">\n'
      '<p>Urban renewal (hitchadshut ironit) is the strengthening, extension or demolition and rebuilding of old residential buildings, paid for by the extra building rights a developer receives, so the owners do not pay for the construction. There are three tracks: pinui binui (evacuation and construction) of a whole complex, TAMA 38 for a single building, and the fast licensing plan of section 145A1 of the Planning and Building Law, which replaces TAMA 38 in many cities.</p>\n'
      '<p>In 2025, urban renewal made up %d%% of the housing units approved by planning institutions and %d%% of construction starts, and one in five apartments sold in Israel was in a renewal project. On %s the map of the Government Authority for Urban Renewal listed %s complexes in %d cities.</p>\n'
      '<p>TAMA 38 expired in October 2023; in cities preparing a replacement plan it was extended until May 2026 or the plan\'s approval, whichever came first, but not in Tel Aviv. More in English: <a href="/urban-renewal/english-guide/">our guide to pinui binui and TAMA 38 for apartment owners and olim</a>.</p>\n</div>\n'
      % (K["ur_share_approved"], K["starts_share"], dmy(MAPD), num(NCX), NCITY))

METHOD = ('<h2>איך נאסף המידע בעמוד הזה</h2>\n'
          '<p class="nlur3-note">המספרים: <a href="https://www.gov.il/he/pages/urban_renewal_report_2025" rel="nofollow noopener" target="_blank">דוח הרשות הממשלתית להתחדשות עירונית לשנת 2025</a> (פורסם ב-26.5.2026, עודכן ב-16.6.2026), כל טבלה עם העמוד שלה. המתחמים: <a href="https://www.gov.il/he/departments/topics/mapa-renewal" rel="nofollow noopener" target="_blank">מפת הרשות</a> ב-%s, דרך יומן המתחמים שלנו, ו<a href="https://data.gov.il/dataset/urban_renewal" rel="nofollow noopener" target="_blank">הקובץ הפתוח ב-data.gov.il</a>. הרוב בחוק: חוק פינוי ובינוי (עידוד מיזמי פינוי ובינוי) וחוק המקרקעין (חיזוק בתים משותפים מפני רעידות אדמה), בנוסחם המעודכן עד תשפ"ג, נקראו ב-26.10.2026. המכפיל וכל מספר שחישבנו מסומנים "החישוב שלנו". מה שהדוח לא אומר, למשל מה חל בכל עיר אחרי מאי 2026, לא כתוב כאן. עודכן %s.</p>\n'
          % (dmy(MAPD), UPDATED))

# ------------------------------------------------------------------ anchored changes
OLD_INFO = 'style="margin:30px 0;background:#FAF7F1;border:1px solid #E2DCD0;border-radius:18px;padding:14px"'
R_ADD = [
    (H1_OLD, TOP),
    ('<h2>ההחלטה הראשונה: איזה מסלול מתאים לבניין שלכם</h2>', TRACKS + '<h2>ההחלטה הראשונה: איזה מסלול מתאים לבניין שלכם</h2>'),
    ('<h2>המספרים שכולם מתווכחים עליהם: כמה הסכמה באמת צריך</h2>', DECL + '<h2>המספרים שכולם מתווכחים עליהם: כמה הסכמה באמת צריך</h2>'),
    ('<h2>שישה עקרונות למשא ומתן של נציגות חכמה</h2>', TAMA + '<h2>שישה עקרונות למשא ומתן של נציגות חכמה</h2>'),
    ('<h2>שאלות נפוצות</h2>', CITIES + AUTH + '<h2>שאלות נפוצות</h2>'),
    ('<h2>ההמשך שלכם מכאן</h2>', FAQ_NEW + EN + METHOD + '<h2>ההמשך שלכם מכאן</h2>'),
]
R_FIX = [
    ('בקרוב נשיק כאן חדר פרויקט דיגיטלי שמנהל את כל זה במקום אחד: מפת הסכמות על גבי מודל תלת ממדי של הבניין, מסמכים, עדכונים ואנשי מקצוע. בינתיים, הכלים בעמוד הזה פתוחים לכולם.',
     'לנציגות יש מקום אחד שמרכז את כל זה: <a href="/my-renewal/">חדר הפרויקט של הבניין</a>, עם מצב ההסכמות של כל דירה, השלבים, המסמכים והעדכונים. הכלים בעמוד הזה פתוחים לכולם.'),
    ('לבניין שלכם מגיעה מערכת, לא אקסל', 'לבניין שלכם מגיע חדר פרויקט, לא קובץ אקסל'),
    ('פותחים חדר פרויקט עם מודל תלת-ממדי של ההסכמות', 'פותחים חדר פרויקט עם תמונה תלת-ממדית של ההסכמות'),
    # the start band, the two link lines, the Tel Aviv box and the old infographic frame: from cream, brown and terracotta to the Instruments palette
    ('style="background:#14130F;border-radius:18px;padding:26px 24px;margin:26px 0"', 'style="background:#12202A;border-radius:6px;padding:26px 24px;margin:26px 0"'),
    ('style="color:#E9D9A8;font:700 12.5px Heebo,sans-serif;letter-spacing:.06em;margin:0 0 6px"', 'style="color:#A9C3CF;font:600 13px \'IBM Plex Sans Hebrew\',Heebo,sans-serif;letter-spacing:.06em;margin:0 0 6px"'),
    ("style=\"color:#FAF7F1;font-family:'Frank Ruhl Libre',Georgia,serif;font-size:1.35rem;margin:0 0 8px\"", "style=\"color:#FFFFFF;font:700 1.35rem/1.4 'IBM Plex Sans Hebrew',Heebo,sans-serif;margin:0 0 8px\""),
    ('style="color:#C9C2B4;font:400 14px/1.7 Heebo,sans-serif;margin:0 0 16px"', 'style="color:#D3DCE2;font:400 14px/1.7 \'IBM Plex Sans Hebrew\',Heebo,sans-serif;margin:0 0 16px"'),
    ('style="background:#C2563A;color:#FAF7F1;font:700 14px Heebo,sans-serif;border-radius:10px;padding:13px 20px;text-decoration:none"', 'style="background:#2F6F86;color:#FFFFFF;font:700 14px Heebo,sans-serif;border-radius:6px;padding:13px 20px;text-decoration:none"'),
    ('style="background:transparent;color:#E9D9A8;border:1.5px solid rgba(233,217,168,.5);font:700 14px Heebo,sans-serif;border-radius:10px;padding:13px 20px;text-decoration:none"', 'style="background:transparent;color:#FFFFFF;border:1.5px solid rgba(255,255,255,.55);font:700 14px Heebo,sans-serif;border-radius:6px;padding:13px 20px;text-decoration:none"'),
    ('style="font:400 13px Heebo,sans-serif;color:#6D665C;margin:8px 0 0;text-align:center"', 'style="font:400 13px Heebo,sans-serif;color:#3E4C58;margin:8px 0 0;text-align:center"'),
    ('style="font:400 13px Heebo,sans-serif;color:#6D665C;margin:4px 0 0;text-align:center"', 'style="font:400 13px Heebo,sans-serif;color:#3E4C58;margin:4px 0 0;text-align:center"'),
    ('<a href="/urban-renewal/english-guide/" style="color:#9C7A3C;font-weight:600">', '<a href="/urban-renewal/english-guide/" style="color:#1F4B5C;font-weight:600">'),
    ('<a href="/urban-renewal/tama-38-alternatives/" style="color:#9C7A3C;font-weight:600">', '<a href="/urban-renewal/tama-38-alternatives/" style="color:#1F4B5C;font-weight:600">'),
    ('style="margin:26px 0;padding:16px 20px;border:1px solid #9C7A3C;border-radius:14px;background:#F3EEE3"', 'style="margin:26px 0;padding:16px 20px;border:1px solid #D3DCE2;border-radius:6px;background:#F6F8F9"'),
    (OLD_INFO, 'style="margin:30px 0;background:#FFFFFF;border:1px solid #D3DCE2;border-radius:6px;padding:14px"'),
]
R = R_ADD + R_FIX
NEWS = [n for o, n in R_ADD]

req, raw, r = get_live(PID, DRY)
new = apply(raw, R)
print("[page %d] live content modified %s, %d chars; %d anchors matched once each (%s)" % (PID, r.get("modified"), len(raw), len(R), "public REST, rendered" if DRY else "raw"))
NEWTXT = "".join(NEWS) + "".join(n for o, n in R_FIX[:3])
qs = gates(NEWTXT, new, 7 + 18)
inner, bad, offi = check_links(NEWTXT)
assert not bad, ("internal links must answer 200", bad)
c_all, c_old = counts(new), counts(raw)
print("  page now: %s | before: %s" % (json.dumps(c_all, ensure_ascii=False), json.dumps(c_old, ensure_ascii=False)))
print("  FAQ %d (7 old + 18 new); internal links %d all 200; official: %s" % (len(qs), len(inner), ", ".join("%s %s" % (h.split("/")[2], st) for h, st in offi)))
print("  title %d chars, description %d chars; language gates passed; one h1; svg text >= 12px" % (len(TITLE), len(DESC)))
left = [c for c in ("#9C7A3C", "#C2563A", "#E9D9A8", "#FAF7F1", "#F3EEE3", "Frank Ruhl") if c in re.sub(r"<svg\b.*?</svg>", "", new, flags=re.S)]
print("  old palette left outside SVGs:", left or "none")

SRC = """# /urban-renewal/ (page 73): where every fact on the page comes from (internal, written by write_g3_page.py, %s)

| Fact | Source |
|---|---|
| 35%% of approved units, 28%% of starts, one in five sold, published 26.5.2026 | gov.il/he/pages/urban_renewal_report_2025 (read via reader proxy) |
| Permits 28,902 (13,066 + 15,836), 186 plans / 75,925, 21 replacement plans / ~286,500, 86 complexes started, 51 administrations, budget 366m, planning 94.1m | R25 pp. 18, 22 |
| Tracks comparison, taxes, betterment, ILA | R25 annex A pp. 114-116 |
| Fast licensing rights 400 / 500 / 200, mobility 300 / 100, orders 450-550, permit at deposit | R25 p. 94 |
| TAMA 38 expiry, extension, replacement plans by city, self-promoted cities, plans in force before | R25 pp. 90-93 |
| Building renewal 2025 (requests, permits, added, occupied), 2024 comparison; permits and requests split 2013-2025 | R25 pp. 34, 96, 102 (p.102 prints 52%% strengthening for 2016, p.34 prints 58%%; p.34 kept) |
| Request to permit by city | R25 pp. 109-110 |
| Tax-track declarations per year; preliminary decisions by district; declarations by locality (the report's own sums differ, noted on the page) | R25 pp. 68, 70, 71, 72 |
| Apartments sold in renewal projects by city, 2025 | R25 p. 41 |
| Complexes, stages, tracks, units, multiplier per city | renewal-track.json (the authority's map %s), our calculation; renewal-stats.json for the national units |
| Majorities | Pinui Binui law s.1; strengthening law ss.4, 5, 5א (open law book, read 26.10.2026) |
""" % (UPDATED, dmy(MAPD))
io.open(os.path.join(H, "page-sources-g3.md"), "w", encoding="utf-8").write(SRC)

if DRY:
    pv = os.path.join(H, "preview"); os.makedirs(pv, exist_ok=True)
    io.open(os.path.join(pv, "g3-page-content.html"), "w", encoding="utf-8", newline="").write(new)
    render_shell(os.path.join(pv, "g3-page-render.html"), "/urban-renewal/", new, ["urcity"], PFX)
    print("  --dry: wrote preview/g3-page-content.html, preview/g3-page-render.html, page-sources-g3.md; nothing was posted")
    sys.exit(0)

# 26.10.2026: release run after 1.72.531 (Ben: build the gap pages to the end); the local-only stop removed
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw + "\n<!-- meta " + repr((r.get("meta") or {}).get("_yoast_wpseo_title")) + " | " + repr((r.get("meta") or {}).get("_yoast_wpseo_metadesc")) + " -->")
req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new, "meta": {"_yoast_wpseo_title": TITLE, "_yoast_wpseo_metadesc": DESC}})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers=UA), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
title = re.search(r"<title>(.*?)</title>", page, re.S).group(1).strip()
ok = {"read-back": back.strip() == new.strip(), "one h1": bd.count("<h1") == 1, "tool mounted": 'data-nli="urcity"' in bd, "shortcode rendered": "[nadlan_tool" not in bd,
      "svg x3 in text": bd.count("nlur3-fig") == 3, "one FAQPage": page.count('"@type":"FAQPage"') == 1, "25 questions": page.count('"@type":"Question"') == 25,
      "SoftwareApplication": '"@type":"SoftwareApplication"' in page, "urcity.js enqueued": "tools/urcity.js" in page, "title": title == TITLE, "updated": ("עודכן %s" % UPDATED) in bd}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
