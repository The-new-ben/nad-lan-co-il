# -*- coding: utf-8 -*-
"""Haifa (page 4579): body alignment with the official price list (1-3.2026). Data only, nothing applied."""
import re
from mk import Page

P = Page("haifa-apartment-prices")
D = P.d
SH = "ש\"ח"


def money(v):
    return f"{v:,} {SH}"


def R(k, f="latest"):
    return D["rooms"][k][f]


def NB(name, k):
    for n in D["neighbourhoods"]:
        if n["name"] == name:
            return n["rooms"].get(k)
    raise KeyError(name)


def QV(k, q):
    for qq, v in D["rooms"][k]["quarters"]:
        if qq == q:
            return v
    raise KeyError(q)


def chg(k):
    v = float(D["rooms"][k]["change_pct"])
    return f"עלייה של {v:g}%" if v >= 0 else f"ירידה של {abs(v):g}%"


def cells(anchor):
    """rows of the tbody of the table that contains anchor: list of lists of raw cell inner html."""
    h = P.table_html(anchor)
    body = h[h.find("<tbody"):]
    return [re.findall(r"<td\b[^>]*>(.*?)</td>", r, re.S) for r in re.findall(r"<tr\b[^>]*>(.*?)</tr>", body, re.S)]


def tbl(headers, rows):
    out = ['<table dir="rtl">', '<thead dir="rtl">', '<tr dir="rtl">']
    out += [f'<th dir="rtl">{h}</th>' for h in headers]
    out += ["</tr>", "</thead>", '<tbody dir="rtl">']
    for r in rows:
        out.append('<tr dir="rtl">')
        out += [f'<td dir="rtl">{x}</td>' for x in r]
        out.append("</tr>")
    out += ["</tbody>", "</table>"]
    return "\n".join(out)


NP = "לא פורסם"
NS = "לא מוצג במחירון"  # neighbourhood absent from the city file (capped at 8); the official files may hold a median
Q1 = "ברבעון הראשון של 2026"

# ---------------- edits ----------------
# 1. the lead paragraph, directly above the price list
old1 = P.find("בטווח עבודה מעשי, דירות רגילות רבות בחיפה", "על ציפייה גבוהה מדי.")
new1 = (f"לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה בחיפה היה {money(R('3'))} לדירת 3 חדרים, "
        f"{money(R('4'))} לדירת 4 חדרים ו-{money(R('5'))} לדירת 5 חדרים. דירות חדשות, גדולות, יוקרתיות או כאלה שנמצאות בכרמל, "
        "בדניה, בגבעת זמר ובמוקדים מבוקשים יכולות להגיע למחירים גבוהים יותר, ודירה מסוימת יכולה להיות רחוקה מהחציון בגלל "
        "מספר החדרים, מצב הנכס והאזור. בדיקת שכירות מוסיפה נקודת ביקורת: השוואה לשכירות של דירות דומות באותו אזור עוזרת להבין "
        "אם מחיר דירה מבוקש נשען על שוק אמיתי או על ציפייה גבוהה מדי.")
e1 = P.edit(old1, new1, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest"], "UNSOURCED",
            "Lead above the list: the 950,000-2,650,000 working range for regular flats was consistent with the official 3/4/5-room medians and is "
            "restated as the medians; the 3,300,000 luxury ceiling and the rent median 3,400 / average 3,867 have no named source on the page "
            "(rent figures are only 'estimated') and are dropped.")

# 2. first 'check measures' table (asking averages by rooms + rent)
t2 = cells('<th dir="rtl">טווח או נתון עבודה</th>')
assert t2[1][0] == "דירות 3 חדרים" and t2[2][0] == "דירות 4 חדרים" and t2[3][0] == "דירות 5 חדרים", t2
new2 = tbl(["מדד בדיקה", "חציון מחיר העסקה, ינואר-מרץ 2026", "איך להשתמש בו"],
           [[t2[i][0], money(R(k)), t2[i][2]] for i, k in ((1, "3"), (2, "4"), (3, "5"))])
e2 = P.table('<th dir="rtl">טווח או נתון עבודה</th>', new2, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest"], "CONFLICT",
             "Check-measures table: 'average asking' 1,250,000 (3 rooms) and 1,750,000 (4 rooms) are 10% and 9.5% above the official medians "
             "1,135,100 and 1,597,500 (1-3.2026); 5 rooms 2,650,000 was consistent; the 2-room, 6+-room and two rent rows have no named source. "
             "Replaced by the official medians for 3/4/5 rooms; the 'how to use it' notes are kept word for word.")

# 3. the sentence after that table: coverage of the official list
old3 = "המספרים בעמוד הם טווחי עבודה והצלבות נתונים, לא שמאות."
new3 = ("המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים ודירות 6 חדרים ומעלה כדאי לבדוק מול עסקאות דומות ברחוב "
        "ובשכונה. החציון הוא נקודת ייחוס, לא שמאות.")
e3 = P.edit(old3, new3, ["data_quarter"], "WORDING", "Follows edit 2: the numbers are no longer 'working ranges'; the 2 and 6+-room rows left the table.")

# 4. city average + per-m2 average
old4 = P.find("נתון כמו ממוצע של כ-1,560,586", "גם אם מספר החדרים דומה.")
new4 = (f"נתון כמו חציון מחיר העסקה לכל הדירות בעיר, {money(R('all'))} {Q1} לפי נתוני רשות המסים, יכול לעזור לפתוח בדיקה, "
        "אבל לא לסגור מחיר לדירה ספציפית. דירה ברחוב מבוקש בכרמל עם נוף, מעלית וחניה עשויה להתרחק מאוד מהחציון, ודירה ישנה "
        "בקומה גבוהה ללא מעלית עשויה להיות זולה משמעותית גם אם מספר החדרים דומה.")
assert old4.endswith("גם אם מספר החדרים דומה.") and "מהממוצע" in old4
e4 = P.edit(old4, new4, ["rooms.all.latest"], "CONFLICT",
            "City average 1,560,586 is 11% above the official all-rooms median 1,406,400 (1-3.2026); the 19,400 per-m2 average has no source. "
            "Replaced by the official all-rooms median; 'מהממוצע' in the next sentence becomes 'מהחציון'.")

# 5. sentence before the rooms table
old5 = "לכן הטבלה מתאימה כנקודת התחלה, ולא כתחליף להשוואה לפי רחוב וסוג בניין."
new5 = ("לכן הטבלה הבאה, שמציגה את חציון מחיר העסקה לפי נתוני רשות המסים לרבעון הראשון של 2026 לצד אותו רבעון שנה קודם לכן, "
        "מתאימה כנקודת התחלה, ולא כתחליף להשוואה לפי רחוב וסוג בניין.")
e5 = P.edit(old5, new5, ["data_quarter"], "WORDING", "Introduces the official rooms table of edit 6 and names its source and quarter.")

# 6. the rooms table (asking averages + per m2)
t6 = cells('<th dir="rtl">מחיר מבוקש ממוצע משוער</th>')
assert [r[0] for r in t6[1:4]] == ["3 חדרים", "4 חדרים", "5 חדרים"], t6
new6 = tbl(["מספר חדרים", "חציון מחיר העסקה, ינואר-מרץ 2026", "ינואר-מרץ 2025", "שינוי בשנה", "פרשנות לקונה או מוכר"],
           [[t6[i][0], money(R(k)), money(R(k, "year_ago")), chg(k), t6[i][3]] for i, k in ((1, "3"), (2, "4"), (3, "5"))])
e6 = P.table('<th dir="rtl">מחיר מבוקש ממוצע משוער</th>', new6,
             ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct",
              "rooms.5.latest", "rooms.5.year_ago", "rooms.5.change_pct"], "CONFLICT",
             "Rooms table: 3 rooms 1,210,000-1,250,000 and 4 rooms 1,750,000-1,830,000 exclude the official medians 1,135,100 and 1,597,500; "
             "5 rooms 2,650,000-2,730,000 was consistent with 2,638,000; the 1-2-room and 6+-room rows and the 'estimated' per-m2 column have "
             "no source. Replaced by the official medians with the year-earlier quarter; notes of rows 3-5 kept word for word.")

# 7. the 'practical question' table that repeats the asking averages
t7 = cells('<th dir="rtl">שאלה מעשית</th>')
assert len(t7) == 5 and t7[1][0] == "בדיקת דירת 3 חדרים", t7
qs = ["האם המחיר נובע ממיקום או ממצב הנכס?",
      f"האם המחיר משקף עסקאות סגורות באזור? חציון מחיר העסקה בעיר {Q1}: {money(R('3'))}",
      f"האם המחיר כולל יתרונות משפחתיים אמיתיים? חציון מחיר העסקה בעיר {Q1}: {money(R('4'))}",
      f"האם המחיר הוא מחיר שוק או מחיר פתיחה למו\"מ? חציון מחיר העסקה בעיר {Q1}: {money(R('5'))}",
      "האם המחיר מתאים לנכס או נשען על דירות יוקרה אחרות?"]
new7 = tbl(["סוג בדיקה", "שאלה מעשית", "מה עלול לשנות את המחיר"], [[t7[i][0], qs[i], t7[i][2]] for i in range(5)])
e7 = P.table('<th dir="rtl">שאלה מעשית</th>', new7, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest"], "CONFLICT",
             "The questions treat the old asking averages as the reference level (1,250,000 for 3 rooms, 1,750,000 for 4 rooms vs official "
             "1,135,100 / 1,597,500; 950,000 for 2 rooms and 3,300,000 for large flats unsourced). Questions keep their sense without the old "
             "figures and show the official city median for 3/4/5 rooms; the third column is kept word for word.")

# 8. sentence before the neighbourhood table
old8 = "השאלה הנכונה היא כמה עולה דירה דומה באזור דומה."
new8 = ("השאלה הנכונה היא כמה עולה דירה דומה באזור דומה. הטבלה הבאה מציגה את חציון מחיר העסקה לפי שכונה ומספר חדרים, לפי נתוני "
        "רשות המסים לרבעון הראשון של 2026. בשכונות שאינן מופיעות במחירון שבעמוד, כדאי לבדוק עסקאות דומות ברחוב עצמו.")
e8 = P.edit(old8, new8, ["data_quarter"], "WORDING", "Introduces the official neighbourhood table of edit 9.")

# 9. neighbourhood table (all-rooms 'averages seen in deal examples')
MAP = {"הדר": "הדר", "נווה שאנן": "נווה שאנן", "קריית חיים מזרחית": "קרית חיים מזרחית", "מרכז הכרמל": "מרכז הכרמל",
       "אחוזה": "אחוזה", "כרמל מערבי": "כרמל מערבי"}
t9 = cells('<th dir="rtl">מחיר ממוצע שנצפה בעסקאות או נתוני שוק</th>')
rows9, keys9 = [], []
for r in t9:
    name = r[0]
    off = MAP.get(name)
    vals = []
    for k in ("3", "4", "5"):
        v = NB(off, k) if off else None
        vals.append(money(v) if v else (NP if off else NS))
        if v:
            keys9.append(f"neighbourhoods[{off}].rooms.{k}")
    rows9.append([name] + vals + [r[2]])
assert len(rows9) == 10, rows9
new9 = tbl(["אזור או שכונה", "3 חדרים", "4 חדרים", "5 חדרים", "מה מאפיין את המחיר"], rows9)
e9 = P.table('<th dir="rtl">מחיר ממוצע שנצפה בעסקאות או נתוני שוק</th>', new9, keys9, "UNSOURCED",
             "Neighbourhood table: all-rooms 'averages seen in deal examples or market data', no period, no room count, no named source "
             "(Hadar 549,379 is half the official Hadar 3-room median 1,066,400). Replaced by the official neighbourhood medians by rooms, "
             "1-3.2026, 'לא פורסם' where a listed neighbourhood has no median; Kiryat Eliezer, Bat Galim, Denia and Hod HaCarmel, Givat Zemer: the city file keeps only 8 neighbourhoods; the official files DO hold 1-3.2026 medians for some of the others (checked 7.10.2026), so these rows say 'לא מוצג במחירון' (not shown in the page's list), never 'לא פורסם'; "
             "the description column is kept word for word.")

# 10. rent by rooms table (tier 2): 'estimated monthly rent' with no source
t10 = cells('<th dir="rtl">שימוש בבדיקת מחיר</th>')
assert len(t10) == 6, t10
new10 = tbl(["מספר חדרים", "שימוש בבדיקת מחיר"], [[r[0], r[2]] for r in t10])
e10 = P.table('<th dir="rtl">שימוש בבדיקת מחיר</th>', new10, ["page"], "UNSOURCED",
              "Rent by rooms: 'estimated monthly rent' 2,187-10,400 with no named source (the page names no listing sample or index for rent). "
              "The rent column is removed; the usage notes stay word for word.", tier=2)

# 11. rent median / average sentence (tier 2)
old11 = "בחיפה, שכירות חציונית סביב 3,400 ש\"ח וממוצעת סביב 3,867 ש\"ח יוצרת נקודת ייחוס כללית."
new11 = "בחיפה, שכירות של דירות דומות באותו אזור יוצרת נקודת ייחוס כללית."
e11 = P.edit(old11, new11, ["page"], "UNSOURCED", "Rent median 3,400 / average 3,867 with no named source; the hypothetical that follows stays.", tier=2)

# 12. rent by neighbourhood table (tier 2)
t12 = cells('<th dir="rtl">מה לבדוק מול מחיר הדירה</th>')
assert len(t12) == 7, t12
new12 = tbl(["שכונה או אזור", "מה לבדוק מול מחיר הדירה"], [[r[0], r[2]] for r in t12])
e12 = P.table('<th dir="rtl">מה לבדוק מול מחיר הדירה</th>', new12, ["page"], "UNSOURCED",
              "Rent by neighbourhood: 'estimated monthly rent' 2,348-3,015 with no named source. The rent column is removed; the check notes stay.",
              tier=2)

# 13. sentence before the street table
old13 = "עסקה מ-2023 לא משקפת בהכרח מחיר ב-2026, ועסקה מדירה חדשה לא משקפת בהכרח בניין ותיק."
new13 = (old13 + " כדי לראות את כיוון השוק, הטבלה הבאה מציגה את חציון מחיר העסקה בחיפה לפי מספר חדרים בחמשת הרבעונים האחרונים "
         "שפורסמו, לפי נתוני רשות המסים.")
e13 = P.edit(old13, new13, ["data_quarter"], "WORDING", "Introduces the official quarterly table of edit 14.")

# 14. street averages table -> official quarterly medians
QS = [("1-3.2025", "ינואר-מרץ 2025"), ("4-6.2025", "אפריל-יוני 2025"), ("7-9.2025", "יולי-ספטמבר 2025"),
      ("10-12.2025", "אוקטובר-דצמבר 2025"), ("1-3.2026", "ינואר-מרץ 2026")]
rows14, keys14 = [], []
for q, lab in QS:
    row = [lab]
    for k in ("3", "4", "5"):
        v = QV(k, q)
        row.append(money(v) if v else NP)
        if v:
            keys14.append(f"rooms.{k}.quarters[{q}]")
    rows14.append(row)
new14 = tbl(["רבעון", "3 חדרים", "4 חדרים", "5 חדרים"], rows14)
e14 = P.table('<th dir="rtl">מספר עסקאות שנצפה</th>', new14, keys14, "UNSOURCED",
              "Street table: five street averages (767,534-2,383,693) with deal counts but no period, no room count and no named source. "
              "Replaced by the official city medians by rooms for the last five published quarters ('לא פורסם' where the official series "
              "has no value: 4 rooms 10-12.2025, 5 rooms 7-9.2025).")

# 15. sentence before the category table
old15 = "אבל גם מחיר למ\"ר אינו מספר קסם: דירה קטנה ומשופצת יכולה להציג מחיר למ\"ר גבוה יותר מדירה גדולה וישנה."
new15 = (old15 + " כדי למקם את חיפה מול שאר ישראל, הטבלה הבאה משווה את חציון מחיר העסקה בעיר לחציון הארצי של אותו רבעון, לפי "
         "נתוני רשות המסים לרבעון הראשון של 2026.")
e15 = P.edit(old15, new15, ["data_quarter"], "WORDING", "Introduces the official Haifa vs Israel table of edit 16.")

# 16. category table (average price, area, per m2, deal counts) -> Haifa vs Israel medians
IL = D["israel"]
new16 = tbl(["קטגוריה", "חציון מחיר העסקה בחיפה, ינואר-מרץ 2026", "חציון ארצי, ינואר-מרץ 2026"],
            [["3 חדרים", money(R("3")), money(IL["3"])], ["4 חדרים", money(R("4")), money(IL["4"])],
             ["5 חדרים", money(R("5")), money(IL["5"])], ["כל הדירות", money(R("all")), money(IL["all"])]])
e16 = P.table('<th dir="rtl">מספר עסקאות בדוגמה</th>', new16,
              ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "rooms.all.latest", "israel.3", "israel.4", "israel.5", "israel.all"], "CONFLICT",
              "Category table: 'estimated average' 1,210,000 (3 rooms, +6.6%) and 1,830,000 (4 rooms, +14.6%) vs official 1,135,100 / 1,597,500; "
              "5 rooms 2,730,000 consistent; 1-2 and 6+ rows, per-m2 and deal counts of an unnamed sample unsourced. Replaced by the official "
              "Haifa medians next to the Israel medians, 1-3.2026.")

# 17. renovation cost range (tier 2)
old17 = "בדירת יד שנייה, המחיר יכול להיראות נמוך יותר, אך שיפוץ של 150,000 עד 400,000 ש\"ח עשוי לשנות את ההשוואה מול דירה חדשה."
new17 = "בדירת יד שנייה, המחיר יכול להיראות נמוך יותר, אך עלות שיפוץ נדרש עשויה לשנות את ההשוואה מול דירה חדשה."
e17 = P.edit(old17, new17, ["page"], "UNSOURCED", "Renovation cost range 150,000-400,000 with no source.", tier=2)

# 18. seller example placed in Ahuza
old18 = "דוגמה למוכר: דירת 4 חדרים באחוזה נמצאת בבניין מטופח, עם מעלית וחניה, ומודעות דומות מוצגות סביב 1,850,000 עד 1,950,000 ש\"ח."
new18 = "דוגמה למוכר: דירת 4 חדרים נמצאת בבניין מטופח, עם מעלית וחניה, ומודעות דומות באותו רחוב מוצגות סביב 1,850,000 עד 1,950,000 ש\"ח."
e18 = P.edit(old18, new18, ["neighbourhoods[אחוזה].rooms.4", "page"], "CONFLICT",
             "The seller example puts Ahuza 4-room listings at 1,850,000-1,950,000 and deals at 1,700,000-1,820,000, while the official Ahuza "
             "4-room median is 2,410,400 (1-3.2026) and now shows in the neighbourhood table. The example keeps its numbers but no longer "
             "names Ahuza (a street-level illustration).")

# 19-25. FAQ answers
old19 = P.find("טווח העבודה הרחב לדירות רגילות בחיפה נע סביב", "יכולות להגיע לכ-3,300,000 ש\"ח ואף יותר.")
new19 = (f"לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה בחיפה היה {money(R('all'))} לכל הדירות, {money(R('3'))} "
         f"לדירת 3 חדרים, {money(R('4'))} לדירת 4 חדרים ו-{money(R('5'))} לדירת 5 חדרים. המחיר בפועל משתנה לפי מספר חדרים, שכונה, "
         "מצב הנכס ושטח, ודירות גדולות, חדשות או יוקרתיות בכרמל, דניה, גבעת זמר ואזורים מבוקשים יכולות להגיע למחירים גבוהים יותר.")
e19 = P.edit(old19, new19, ["rooms.all.latest", "rooms.3.latest", "rooms.4.latest", "rooms.5.latest"], "UNSOURCED",
             "FAQ 'average': the 950,000-2,650,000 range was consistent; the 3,300,000 ceiling has no source. Rewritten from the same official "
             "medians as the lead (the median is not called an average).")

old20 = P.find("דירת 3 חדרים בחיפה נמצאת סביב 1,210,000 עד 1,250,000", "יכולה לקבל תמחור שונה מאוד.")
new20 = (f"לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים בחיפה {Q1} היה {money(R('3'))}, לעומת {money(R('3', 'year_ago'))} "
         "שנה קודם לכן. בפועל, דירת 3 חדרים בהדר, נווה שאנן, בת גלים או אחוזה יכולה לקבל תמחור שונה מאוד: באותו רבעון החציון "
         f"לדירת 3 חדרים היה {money(NB('הדר', '3'))} בהדר ו-{money(NB('אחוזה', '3'))} באחוזה.")
e20 = P.edit(old20, new20, ["rooms.3.latest", "rooms.3.year_ago", "neighbourhoods[הדר].rooms.3", "neighbourhoods[אחוזה].rooms.3"], "CONFLICT",
             "FAQ 3 rooms: 1,210,000-1,250,000 excludes the official 1,135,100; per-m2 16,667-18,400 unsourced. Rewritten with the official "
             "city median, the year-earlier quarter and two official neighbourhood medians named in the same answer.")

old21 = "דירת 4 חדרים בחיפה נעה סביב 1,750,000 עד 1,830,000 ש\"ח בטווחים כלליים."
new21 = f"לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים בחיפה {Q1} היה {money(R('4'))}, לעומת {money(R('4', 'year_ago'))} שנה קודם לכן."
e21 = P.edit(old21, new21, ["rooms.4.latest", "rooms.4.year_ago"], "CONFLICT", "FAQ 4 rooms: 1,750,000-1,830,000 excludes the official 1,597,500.")

old22 = "בדוגמאות שנבדקו, דניה והוד הכרמל הגיעו סביב 3,394,095 ש\"ח וגבעת זמר סביב 2,725,356 ש\"ח, אך כל נכס דורש בדיקה עצמאית."
new22 = (f"לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 4 חדרים היה {money(NB('מרכז הכרמל', '4'))} במרכז הכרמל "
         f"ו-{money(NB('אחוזה', '4'))} באחוזה, לעומת {money(R('4'))} בעיר כולה, אך כל נכס דורש בדיקה עצמאית.")
e22 = P.edit(old22, new22, ["neighbourhoods[מרכז הכרמל].rooms.4", "neighbourhoods[אחוזה].rooms.4", "rooms.4.latest"], "UNSOURCED",
             "FAQ expensive areas: all-rooms 'examples checked' for Denia/Hod HaCarmel and Givat Zemer, no period or source (no official median "
             "for them). Replaced by the official 4-room medians of two areas the same answer names.")

old23 = "לדוגמה, בהדר הופיעו נתונים סביב 549,379 ש\"ח ובקריית אליעזר סביב 668,339 ש\"ח בדוגמאות עסקאות, אך מצב הבניין והרחוב יכולים לשנות את התמונה."
new23 = (f"לדוגמה, לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 3 חדרים בהדר היה {money(NB('הדר', '3'))}, "
         f"לעומת {money(R('3'))} בעיר כולה, אך מצב הבניין והרחוב יכולים לשנות את התמונה.")
e23 = P.edit(old23, new23, ["neighbourhoods[הדר].rooms.3", "rooms.3.latest"], "UNSOURCED",
             "FAQ cheaper areas: all-rooms 'deal examples' 549,379 (Hadar) and 668,339 (Kiryat Eliezer), no period or source. Replaced by the "
             "official Hadar 3-room median (Kiryat Eliezer has none).")

old24 = "חציון שכירות סביב 3,400 ש\"ח וממוצע סביב 3,867 ש\"ח יכולים לעזור לבדוק סבירות, אבל מחיר הדירה נקבע גם לפי מיקום, שטח, מצב, זכויות וביקוש קונים."
new24 = "שכירות של דירות דומות באותו אזור יכולה לעזור לבדוק סבירות, אבל מחיר הדירה נקבע גם לפי מיקום, שטח, מצב, זכויות וביקוש קונים."
e24 = P.edit(old24, new24, ["page"], "UNSOURCED", "FAQ rent: median 3,400 / average 3,867 with no named source (same as edit 11).", tier=2)

old25 = "דירת יד שנייה יכולה להיות זולה יותר במחיר החוזה, אך שיפוץ של 150,000 עד 400,000 ש\"ח עשוי לשנות את הכדאיות."
new25 = "דירת יד שנייה יכולה להיות זולה יותר במחיר החוזה, אך עלות שיפוץ נדרש עשויה לשנות את הכדאיות."
e25 = P.edit(old25, new25, ["page"], "UNSOURCED", "FAQ renovation cost range 150,000-400,000 with no source (same as edit 17).", tier=2)

# ---------------- claims inventory ----------------
C = P.claim
C("p@4341", "דירות רגילות רבות בחיפה נעות סביב 950,000 עד 2,650,000 ש\"ח לפי מספר חדרים", "sale", "CONSISTENT", f"edit {e1}", rooms="3-5",
  official="3: 1,135,100 / 4: 1,597,500 / 5: 2,638,000 (1-3.2026)", figures=2, note="restated as the medians inside the same rewrite")
C("p@4341", "דירות חדשות, גדולות, יוקרתיות... יכולות להגיע גם ל-3,300,000 ש\"ח ואף יותר", "sale", "UNSOURCED", f"edit {e1}", rooms="6+")
C("p@4341", "חציון שכירות סביב 3,400 ש\"ח וממוצע סביב 3,867 ש\"ח", "rent", "UNSOURCED", f"edit {e1}", figures=2,
  note="no named source anywhere on the page for rent")
C("tr@42329", "דירות 2 חדרים | כ-950,000 ש\"ח בממוצע מבוקש", "sale", "UNSOURCED", f"edit {e2}", rooms=2)
C("tr@42507", "דירות 3 חדרים | כ-1,250,000 ש\"ח בממוצע מבוקש", "sale", "CONFLICT", f"edit {e2}", rooms=3, official="1,135,100 (1-3.2026)")
C("tr@42687", "דירות 4 חדרים | כ-1,750,000 ש\"ח בממוצע מבוקש", "sale", "CONFLICT", f"edit {e2}", rooms=4, official="1,597,500 (1-3.2026)")
C("tr@42855", "דירות 5 חדרים | כ-2,650,000 ש\"ח בממוצע מבוקש", "sale", "CONSISTENT", f"edit {e2}", rooms=5, official="2,638,000 (1-3.2026)")
C("tr@43025", "דירות 6 חדרים ומעלה | כ-3,300,000 ש\"ח בממוצע מבוקש", "sale", "UNSOURCED", f"edit {e2}", rooms="6+")
C("tr@43201..43348", "שכירות חציונית כ-3,400 / שכירות ממוצעת כ-3,867", "rent", "UNSOURCED", f"edit {e2}", figures=2)
C("p@43789", "ממוצע של כ-1,560,586 ש\"ח", "sale_avg", "CONFLICT", f"edit {e4}", rooms="all", official="all rooms 1,406,400 (1-3.2026)")
C("p@43789", "מחיר ממוצע סביב 19,400 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"edit {e4}")
C("tr@45206", "1 עד 2 חדרים | 950,000 עד 980,000 | 16,964 עד 20,780 למ\"ר", "sale", "UNSOURCED", f"edit {e6}", rooms="1-2", figures=4)
C("tr@45447", "3 חדרים | כ-1,210,000 עד 1,250,000 ש\"ח", "sale", "CONFLICT", f"edit {e6}", rooms=3, official="1,135,100", figures=2)
C("tr@45447", "3 חדרים | כ-16,667 עד 18,400 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"edit {e6}", rooms=3, figures=2)
C("tr@45678", "4 חדרים | כ-1,750,000 עד 1,830,000 ש\"ח", "sale", "CONFLICT", f"edit {e6}", rooms=4, official="1,597,500", figures=2)
C("tr@45678", "4 חדרים | כ-17,500 עד 19,150 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"edit {e6}", rooms=4, figures=2)
C("tr@45907", "5 חדרים | כ-2,650,000 עד 2,730,000 ש\"ח", "sale", "CONSISTENT", f"edit {e6}", rooms=5, official="2,638,000 (within the 1% floor tolerance)", figures=2)
C("tr@45907", "5 חדרים | כ-19,630 עד 21,500 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"edit {e6}", rooms=5, figures=2)
C("tr@46135", "6 חדרים ומעלה | 3,300,000 עד 3,400,000 | 17,368 עד 21,000 למ\"ר", "sale", "UNSOURCED", f"edit {e6}", rooms="6+", figures=4)
C("tr@46905", "בדיקת דירת 2 חדרים | האם המחיר קרוב ל-950,000 ש\"ח", "sale", "UNSOURCED", f"edit {e7}", rooms=2)
C("tr@47121", "בדיקת דירת 3 חדרים | האם 1,250,000 ש\"ח משקפים עסקאות סגורות", "sale", "CONFLICT", f"edit {e7}", rooms=3, official="1,135,100",
  note="question form, but it uses the removed asking average as the reference level")
C("tr@47308", "בדיקת דירת 4 חדרים | האם 1,750,000 ש\"ח כולל יתרונות משפחתיים", "sale", "CONFLICT", f"edit {e7}", rooms=4, official="1,597,500")
C("tr@47506", "בדיקת דירת 5 חדרים | האם 2,650,000 ש\"ח הוא מחיר שוק", "sale", "CONSISTENT", f"edit {e7}", rooms=5, official="2,638,000")
C("tr@47708", "בדיקת דירה גדולה | האם 3,300,000 ש\"ח מתאים לנכס", "sale", "UNSOURCED", f"edit {e7}", rooms="6+")
C("tr@49215..50823", "טבלת 'מחיר ממוצע שנצפה בעסקאות' לפי שכונה (10 שורות, כל החדרים)", "sale_nb", "UNSOURCED", f"edit {e9}", figures=10,
  official="official medians by rooms for 6 of the 10 areas", note="e.g. Hadar 549,379 vs official Hadar 3 rooms 1,066,400; Merkaz HaCarmel 1,662,150 vs 3 rooms 1,769,300")
C("tr@53843..54615", "טבלת שכירות חודשית משוערת לפי חדרים (6 שורות, 2,187-10,400)", "rent", "UNSOURCED", f"edit {e10}", figures=6)
C("p@54787", "שכירות חציונית סביב 3,400 ש\"ח וממוצעת סביב 3,867 ש\"ח", "rent", "UNSOURCED", f"edit {e11}", figures=2)
C("tr@55367..56233", "טבלת שכירות חודשית משוערת לפי שכונה (7 שורות, 2,348-3,015)", "rent", "UNSOURCED", f"edit {e12}", figures=7)
C("tr@57623..58342", "טבלת רחובות: חסן שוקרי 116 עסקאות 767,534 ... דרך יד לבנים 930,573", "sale_street", "UNSOURCED", f"edit {e14}", figures=5,
  note="deal counts 116/105/93/88/68 with no period or source; mixed room counts")
C("tr@59223", "1 עד 2 חדרים | 980,000 | 20,780 למ\"ר | 996 עסקאות", "sale", "UNSOURCED", f"edit {e16}", rooms="1-2", figures=3)
C("tr@59392", "3 חדרים | כ-1,210,000 ש\"ח מחיר ממוצע משוער", "sale", "CONFLICT", f"edit {e16}", rooms=3, official="1,135,100")
C("tr@59560", "4 חדרים | כ-1,830,000 ש\"ח מחיר ממוצע משוער", "sale", "CONFLICT", f"edit {e16}", rooms=4, official="1,597,500")
C("tr@59728", "5 חדרים | כ-2,730,000 ש\"ח מחיר ממוצע משוער", "sale", "CONSISTENT", f"edit {e16}", rooms=5, official="2,638,000 (+3.5%)")
C("tr@59392..59728", "מחיר למ\"ר משוער 18,400 / 19,150 / 21,500", "per_m2", "UNSOURCED", f"edit {e16}", rooms="3-5", figures=3)
C("tr@59392..59728", "מספר עסקאות בדוגמה 1,921 / 1,240 / 674", "count", "UNSOURCED", f"edit {e16}", rooms="3-5", figures=3)
C("tr@59895", "6 חדרים ומעלה | 3,400,000 | 21,000 למ\"ר | 126 עסקאות", "sale", "UNSOURCED", f"edit {e16}", rooms="6+", figures=3)
C("p@60991", "981 מכירות יד שנייה (+19.2%), 214 חדשות (-33.7%), 4,288 לא מכורות, דצמבר 2025 עד פברואר 2026", "count", "UNSOURCED",
  "keep (published market data, dated period 12.2025-2.2026; sales counts, not prices)", figures=5)
C("tr@61650..62365", "טבלת חדש מול יד שנייה: 981 / 214 / 4,288 / כ-85,000 ארצי במרץ 2026", "count", "UNSOURCED",
  "keep (same dated published data as p@60991; national stock dated March 2026)", figures=4)
C("p@62601", "שיפוץ של 150,000 עד 400,000 ש\"ח", "other", "UNSOURCED", f"edit {e17}", figures=2)
C("p@68809", "דירת 4 חדרים באחוזה, מודעות דומות סביב 1,850,000 עד 1,950,000 ש\"ח", "sale_nb", "CONFLICT", f"edit {e18}", rooms=4,
  official="Ahuza 4 rooms 2,410,400 (1-3.2026)", figures=2, note="a seller example, but it names a real neighbourhood with an official median far above it")
C("p@70991", "FAQ: טווח העבודה ... 950,000 עד 2,650,000 ש\"ח", "sale", "CONSISTENT", f"edit {e19}", rooms="3-5", official="1,135,100 / 1,597,500 / 2,638,000", figures=2)
C("p@70991", "FAQ: יכולות להגיע לכ-3,300,000 ש\"ח ואף יותר", "sale", "UNSOURCED", f"edit {e19}", rooms="6+")
C("p@71274", "FAQ: דירת 3 חדרים סביב 1,210,000 עד 1,250,000 ש\"ח", "sale", "CONFLICT", f"edit {e20}", rooms=3, official="1,135,100", figures=2)
C("p@71274", "FAQ: מחיר למ\"ר סביב 16,667 עד 18,400 ש\"ח", "per_m2", "UNSOURCED", f"edit {e20}", rooms=3, figures=2)
C("p@71539", "FAQ: דירת 4 חדרים סביב 1,750,000 עד 1,830,000 ש\"ח", "sale", "CONFLICT", f"edit {e21}", rooms=4, official="1,597,500", figures=2)
C("p@71754", "FAQ: דניה והוד הכרמל סביב 3,394,095, גבעת זמר סביב 2,725,356", "sale_nb", "UNSOURCED", f"edit {e22}", figures=2)
C("p@72046", "FAQ: הדר סביב 549,379, קריית אליעזר סביב 668,339", "sale_nb", "UNSOURCED", f"edit {e23}", figures=2,
  official="Hadar 3 rooms 1,066,400")
C("p@72665", "FAQ: חציון שכירות 3,400, ממוצע 3,867", "rent", "UNSOURCED", f"edit {e24}", figures=2)
C("p@72938", "FAQ: שיפוץ של 150,000 עד 400,000 ש\"ח", "other", "UNSOURCED", f"edit {e25}", figures=2)

P.write(notes=(
    "Not audited as claims (explicit examples and hypotheticals, kept): 5 rooms at 2,650,000 (p@46389, buyer question); two 3-room flats "
    "150,000 apart (tr@52249); the rent if-example 1,250,000 / 3,820 / 2,700 / 5,000 (p@54787 after edit 11); the per-m2 if-examples "
    "1,210,000 / 1,830,000 / 2,730,000 (p@58553, they reuse the old category averages as worked examples); listing 1,850,000 and if-deals "
    "1,700,000-1,760,000 (p@60086); 1,650,000 + 250,000 and 1,950,000 to 2,050,000 (p@63975); 1,750,000 / 2,300,000 (p@67099); the "
    "Neve Shaanan 3-room buyer example 1,320,000 / 1,180,000-1,260,000 (p@68485, no official 3-room median for Neve Shaanan); the seller "
    "example's if-deals 1,700,000-1,820,000 (p@68809); the Givat Zemer 5-room owner example 2,900,000 / 2,650,000-2,850,000 (p@69145, no "
    "official median for Givat Zemer); the scenario table tr@69646..70248 that sums up these examples; 10% / 15% (p@72367). The remaining "
    "SUSPECT lines of check.py are all among these examples. Rent figures on this page are labelled only 'estimated' with no named source, "
    "so they are tier-2 edits (rent columns removed, check notes kept); the lead and the first table drop rent inside tier-1 edits. Sales "
    "counts (981 / 214 / 4,288 / 85,000) are kept: dated periods and 'published market data', not prices; unsure whether that counts as "
    "a named kind of source. Official quirks: 4 rooms has no 10-12.2025 median and 5 rooms none for 7-9.2025; the all-rooms median rose "
    "10.1% in a year while 3/4/5 rooms were flat or fell (deal mix). Name mapping: page 'קריית חיים מזרחית' = official 'קרית חיים מזרחית'. "
    "Official medians exist also for יזרעאליה and נווה דוד, which the page does not discuss; not added. Kiryat Eliezer, Bat Galim, Denia "
    "and Hod HaCarmel, Givat Zemer are not in the city file: the city file keeps only 8 neighbourhoods; the official files DO hold 1-3.2026 medians for some of the others (checked 7.10.2026), so these rows say 'לא מוצג במחירון' (not shown in the page's list), never 'לא פורסם'."))
