# -*- coding: utf-8 -*-
"""Beer Sheva (page 4589): body alignment with the official price list (1-3.2026; 5 rooms latest 7-9.2025).
The list itself is not on the page yet (it will be added). Data only, nothing applied."""
import re
from mk import Page

P = Page("beer-sheva-apartment-prices")
D = P.d
NIS = "₪"
MR = "מ״ר"  # the page writes m2 with gershayim


def money(v):
    return f"{v:,} {NIS}"


def R(k, f="latest"):
    return D["rooms"][k][f]


def NB(name, k):
    for n in D["neighbourhoods"]:
        if n["name"] == name:
            return n["rooms"].get(k)
    raise KeyError(name)


def chg(k):
    v = float(D["rooms"][k]["change_pct"])
    return f"עלייה של {v:g}%" if v >= 0 else f"ירידה של {abs(v):g}%"


def cells(anchor):
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


assert D["rooms"]["5"]["quarter"] == "7-9.2025" and D["rooms"]["3"]["quarter"] == "1-3.2026" and D["rooms"]["4"]["quarter"] == "1-3.2026"
TAX = "לפי נתוני רשות המסים"
Q1 = "ברבעון הראשון של 2026"
FIVE = f"ולדירת 5 חדרים {money(R('5'))} ברבעון השלישי של 2025 (הנתון האחרון שפורסם לדירות 5 חדרים)"
NP = "לא פורסם"
NS = "לא מוצג במחירון"  # neighbourhood absent from the city file (capped at 8); the official files may hold a median

# ---------------- edits ----------------
# 1. lead paragraph (top of the article; the price list will be added to the page)
old1 = P.find("מחירי דירות בבאר שבע נעים בדרך כלל סביב 616,000-650,000", "וכ-4,750-5,740 ₪ לדירת 5 חדרים.")
tail1 = " הפערים בין שכונה ד"
assert P._text.find(old1 + tail1) >= 0
new1 = (f"מחירי דירות בבאר שבע, {TAX}: חציון מחיר העסקה {Q1} היה {money(R('3'))} לדירת 3 חדרים ו-{money(R('4'))} "
        f"לדירת 4 חדרים, {FIVE}. חציון מחיר העסקה לכל הדירות בעיר {Q1} היה {money(R('all'))}. בשכירות, המחיר המבוקש "
        "במודעות נע לרוב מכ-2,300 ₪ לדירת 2 חדרים, כ-2,600-2,760 ₪ לדירת 3 חדרים, כ-3,170-3,640 ₪ לדירת 4 חדרים וכ-4,750-5,740 ₪ "
        "לדירת 5 חדרים.")
e1 = P.edit(old1, new1, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "rooms.5.quarter", "rooms.all.latest", "page"], "CONFLICT",
            "Lead: 5 rooms 1.86-1.89M vs the official 1,766,500 (7-9.2025, the latest published for 5 rooms); 3 rooms 800,000-832,000, "
            "4 rooms 1.19-1.22M and the city average 1.18M were consistent and are restated as the medians. The 2-room and 6+-room ranges "
            "and the 11,900 per-m2 average carry only 'a combination of deal and demand data' and are dropped; the asking rents (listings, "
            "page checked 6.6.2026) are kept and labelled as listing asks. The rest of the paragraph is untouched.")

# 2. city average + per m2
old2 = P.find("לכן מחיר ממוצע עירוני של כ-1,179,412", "בממוצע כללי של העיר.")
new2 = (f"לכן חציון מחיר העסקה העירוני, {money(R('all'))} לכל הדירות {Q1} {TAX}, הוא נקודת פתיחה בלבד. מי שמוכר דירה ברחוב "
        "מצדה, קונה דירה בנווה זאב או בודק דירת 3 חדרים ליד האוניברסיטה לא יכול להסתפק בנתון כללי של העיר.")
e2 = P.edit(old2, new2, ["rooms.all.latest"], "UNSOURCED",
            "City average 1,179,412 is within 5% of the official all-rooms median 1,153,400 and is restated as the median; the 11,900 "
            "per-m2 average has no named source.")

# 3. 'price steps' paragraph
old3 = P.find("נתוני עסקאות וביקוש מצביעים על מדרגות מחיר ברורות:", "דירות גן ופנטהאוזים.")
new3 = (f"נתוני רשות המסים מצביעים על מדרגות מחיר ברורות: חציון מחיר העסקה {Q1} היה {money(R('3'))} לדירת 3 חדרים "
        f"ו-{money(R('4'))} לדירת 4 חדרים, {FIVE}. "
        + old3[old3.find("אלה מספרים רחבים"):].replace("אלה מספרים רחבים", "אלה נתונים רחבים"))
assert "אלה נתונים רחבים, מפני שהם מערבבים" in new3
e3 = P.edit(old3, new3, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "rooms.5.quarter"], "CONFLICT",
            "5 rooms 1,865,000-1,888,938 vs the official 1,766,500 (7-9.2025); 3 and 4 rooms were consistent; the 2-room and 6-room ranges "
            "have no named source. Restated with the official medians; the closing sentence is kept.")

# 4. the page's own source statement
old4 = "המספרים בדף הם כלי עבודה למחירון עירוני, לא שומה."
new4 = "חציון מחיר העסקה בדף מבוסס על נתוני רשות המסים, ונתוני השכירות על מודעות; כולם כלי עבודה למחירון עירוני, לא שומה."
e4 = P.edit(old4, new4, ["data_quarter"], "WORDING", "Names the two kinds of numbers the page keeps after the edits (official medians, listing rents).")

# 5. sentence before the rooms table
old5 = P.find("היא משלבת נתוני ביקוש ועסקאות, ולכן יש לקרוא אותה כטווח עבודה ולא כמחיר מחייב.", "שנמכרה ב-1,100,000 ₪.")
new5 = (f"היא מציגה את חציון מחיר העסקה {TAX}, לצד אותו רבעון שנה קודם לכן, ולכן יש לקרוא אותה כנקודת ייחוס ולא כמחיר "
        "מחייב. המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים ודירות 6 חדרים ומעלה כדאי לבדוק מול עסקאות "
        "דומות ברחוב ובשכונה. דירת 4 חדרים בשטח 87 מ״ר בשכונה ה שנמכרה במאי 2025 ב-860,000 ₪ אינה דומה לדירת 4 חדרים חדשה "
        "יותר בנווה זאב בשטח 109 מ״ר שנמכרה באותו חודש ב-1,100,000 ₪.")
assert old5.count("שנמכרה") == 2
e5 = P.edit(old5, new5, ["data_quarter", "page"], "WORDING",
            "Introduces the official rooms table of edit 6 (the 2 and 6+-room rows left the table) and dates the two example deals "
            "(8.5.2025 and 5.5.2025 in the deals table).")

# 6. rooms table
A6 = '<th dir="rtl">מחיר ביקוש נפוץ</th>'
t6 = cells(A6)
assert [r[0] for r in t6[1:4]] == ["3 חדרים", "4 חדרים", "5 חדרים"], t6
rows6 = [[t6[1][0], money(R("3")), money(R("3", "year_ago")), chg("3"), t6[1][5]],
         [t6[2][0], money(R("4")), money(R("4", "year_ago")), chg("4"), t6[2][5]],
         [t6[3][0], f"{money(R('5'))} (יולי-ספטמבר 2025)", f"{money(R('5', 'year_ago'))} (יולי-ספטמבר 2024)", chg("5"), t6[3][5]]]
new6 = tbl(["סוג דירה", "חציון מחיר העסקה, ינואר-מרץ 2026", "ינואר-מרץ 2025", "שינוי בשנה", "מה לבדוק לפני החלטה"], rows6)
e6 = P.table(A6, new6, ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct",
                        "rooms.5.latest", "rooms.5.year_ago", "rooms.5.change_pct", "rooms.5.quarter"], "CONFLICT",
             "Rooms table: 5 rooms asking 1,865,000 and average deal 1,888,938 vs the official 1,766,500 (7-9.2025); 3 and 4 rooms were "
             "consistent; the 2-room and 6+-room rows, the per-m2 column and the average-area column come from an unnamed mix of demand "
             "and deal data. Replaced by the official medians with the year-earlier quarter (5 rooms: 7-9.2025 vs 7-9.2024, written in the "
             "cells); the check notes of rows 3-5 are kept word for word.")

# 7. sentence after the table
old7 = "מצד שני, מחיר נמוך מהממוצע אינו בהכרח מציאה,"
new7 = "מצד שני, מחיר נמוך מהחציון אינו בהכרח מציאה,"
e7 = P.edit(old7, new7, ["data_quarter"], "WORDING", "Follows edit 6: the table now shows medians.")

# 8. neighbourhood paragraph
old8 = P.find("נתוני שכונות מראים פערים גדולים: אזור תעשיה סביב 1,900,618", "ומספר הדירות שנכנסו למדגם.")
new8 = (f"{TAX} לרבעון הראשון של 2026, הפערים גדולים: חציון מחיר העסקה לדירת 4 חדרים היה {money(NB('אזור תעשיה', '4'))} באזור תעשיה, "
        f"{money(NB('רמות הרכס', '4'))} ברמות הרכס, {money(NB('נווה זאב', '4'))} בנווה זאב ו-{money(NB('ד', '4'))} בשכונה ד. "
        "ההבדל אינו רק יוקרה, אלא גם תמהיל נכסים, שטחים, בנייה חדשה מול ישנה, עסקאות קטנות וגדולות ומספר העסקאות שנרשמו בכל שכונה.")
e8 = P.edit(old8, new8, ["neighbourhoods[אזור תעשיה].rooms.4", "neighbourhoods[רמות הרכס].rooms.4", "neighbourhoods[נווה זאב].rooms.4",
                         "neighbourhoods[ד].rooms.4"], "UNSOURCED",
            "Neighbourhood all-rooms averages and per-m2 averages (5 areas) with no named source or period; replaced by the official "
            "4-room neighbourhood medians (Neve Menachem has none and drops from the sentence).")

# 9. neighbourhood table
MAP = {"אזור תעשיה": "אזור תעשיה", "רמות הרכס": "רמות הרכס", "נווה זאב": "נווה זאב", "שכונה ב": "ב", "שכונה ה": "ה", "שכונה ד": "ד"}
A9 = '<th dir="rtl">בדיקת שווי מומלצת</th>'
t9 = cells(A9)
rows9, keys9 = [], []
for r in t9:
    off = MAP.get(r[0])
    vals = []
    for k in ("3", "4", "5"):
        v = NB(off, k) if off else None
        vals.append(money(v) if v else (NP if off else NS))
        if v:
            keys9.append(f"neighbourhoods[{off}].rooms.{k}")
    rows9.append([r[0]] + vals + [r[4]])
assert len(rows9) == 10, rows9
new9 = tbl(["שכונה או אזור", "3 חדרים", "4 חדרים", "5 חדרים", "בדיקת שווי מומלצת"], rows9)
e9 = P.table(A9, new9, keys9, "UNSOURCED",
             "Neighbourhood table: all-rooms averages and per-m2 for 10 areas, no named source or period. Replaced by the official "
             "neighbourhood medians by rooms, 1-3.2026 ('לא מוצג במחירון' for Neve Menachem, Shchuna Tet, Shchuna Alef, Shchuna Gimel: "
             "the city file keeps only 8 neighbourhoods; the official files DO hold 1-3.2026 medians for some of the others (checked 7.10.2026), so these rows say 'לא מוצג במחירון' (not shown in the page's list), never 'לא פורסם'; 'לא פורסם' only where a listed neighbourhood has no median); the recommended-check column is kept word for word, the 'main feature' column is dropped "
             "to keep five columns.")

# 10. 2023 street averages
old10 = P.find("נתוני רחובות מחזקים את הצורך לרדת לרזולוציה קטנה. בשנת 2023", "צריך לבדוק גודל דירה, קומה ומצב.")
new10 = ("נתוני רחובות מחזקים את הצורך לרדת לרזולוציה קטנה. ברחובות שבהם נרשמו עסקאות רבות, כמו מצדה, סנהדרין, מבצע עובדה, "
         "שאול המלך, דרך המשחררים, יוהנה ז'בוטינסקי, אברהם אבינו ובני אור, אפשר להשוות דירה לעסקאות באותו רחוב עצמו. רחוב פעיל "
         "נותן תמונה טובה יותר מממוצע שכונתי, אך גם בו צריך לבדוק גודל דירה, קומה, מצב ואת תאריך העסקה.")
e10 = P.edit(old10, new10, ["page"], "STALE",
             "2023 street averages (eight streets, 30-62 deals each) shown as the reference level, three years older than the official "
             "data and without room counts. The street names stay; the 2023 averages go.")

# 11-14. FAQ
old11 = P.find("דירת 3 חדרים בבאר שבע נעה בדרך כלל סביב 800,000-832,000", "וביקוש לשכירות.")
new11 = (f"{TAX}, חציון מחיר העסקה לדירת 3 חדרים בבאר שבע {Q1} היה {money(R('3'))}, לעומת {money(R('3', 'year_ago'))} שנה "
         "קודם לכן. בשכונה ג, שכונה ד או אזורים ליד האוניברסיטה המחיר יכול להיות שונה מאוד לפי רחוב, קומה, מצב דירה וביקוש "
         f"לשכירות; בשכונה ד, למשל, החציון לדירת 3 חדרים באותו רבעון היה {money(NB('ד', '3'))}.")
e11 = P.edit(old11, new11, ["rooms.3.latest", "rooms.3.year_ago", "neighbourhoods[ד].rooms.3"], "UNSOURCED",
             "FAQ 3 rooms: the 800,000-832,000 range was consistent (restated as the median); the per-m2 range 10,811-11,571 has no named source.")

old12 = P.find("דירת 4 חדרים נעה לרוב סביב 1.19-1.22 מיליון", "אין לקבוע מחיר לפי מספר חדרים בלבד.")
new12 = (f"{TAX}, חציון מחיר העסקה לדירת 4 חדרים בבאר שבע {Q1} היה {money(R('4'))}, לעומת {money(R('4', 'year_ago'))} שנה "
         "קודם לכן. עסקאות בודדות מאפריל ומאי 2025 מראות גם מחירים של 750,000 ₪, 860,000 ₪ ו-1,100,000 ₪ לפי שכונה, שטח ומצב "
         "נכס. אין לקבוע מחיר לפי מספר חדרים בלבד.")
e12 = P.edit(old12, new12, ["rooms.4.latest", "rooms.4.year_ago", "page"], "STALE",
             "FAQ 4 rooms: the 1.19-1.22M range was consistent (restated as the median); the 750,000 / 860,000 / 1,100,000 deals are "
             "called 'recent' but date from 27.4-8.5.2025 (deals table), older than the official quarter. They stay, with their months.")

old13 = P.find("מחיר ממוצע למ״ר בעיר עומד סביב 11,900", "חייב להיבדק מול דירות דומות בלבד.")
new13 = (f"המחירון הרשמי מפרסם חציון מחיר עסקה לפי מספר חדרים ולא מחיר ל{MR}. כדי לחשב מחיר ל{MR}, מחלקים את מחיר העסקה של "
         f"דירות דומות בשטח הרשום שלהן, ואז מתגלים פערים רחבים בין שכונות, למשל בין שכונה יא, שכונה ד, שכונה ב ואזור תעשיה. "
         f"המחיר ל{MR} חייב להיבדק מול דירות דומות בלבד.")
e13 = P.edit(old13, new13, ["page"], "UNSOURCED",
             "FAQ per m2: city average 11,900 and neighbourhood per-m2 figures (9,951-15,814) with no named source or period. Rephrased "
             "without numbers: how to compute per m2 from similar deals.")

old14 = "בנתונים שנבדקו, רמות הרכס, נווה מנחם, נווה זאב ושכונה ב מציגות מחירים ממוצעים גבוהים יחסית לחלק מהשכונות הוותיקות."
new14 = (f"{TAX} לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 4 חדרים היה {money(NB('רמות הרכס', '4'))} ברמות הרכס ו-{money(NB('נווה זאב', '4'))} "
         f"בנווה זאב, לעומת {money(NB('ד', '4'))} בשכונה ד ו-{money(R('4'))} בעיר כולה.")
e14 = P.edit(old14, new14, ["neighbourhoods[רמות הרכס].rooms.4", "neighbourhoods[נווה זאב].rooms.4", "neighbourhoods[ד].rooms.4", "rooms.4.latest"],
             "WORDING", "FAQ 'which area is more expensive' pointed at the removed neighbourhood averages; rewritten from the same official "
             "figures as edit 8.")

# ---------------- claims inventory ----------------
KEEPR = "keep (asking rents from listings; 628 active listings named on the page, page checked 6.6.2026)"
C = P.claim
C("p@4311", "דירות 2 חדרים סביב 616,000-650,000 ₪", "sale", "UNSOURCED", f"edit {e1}", rooms=2, figures=2)
C("p@4311", "כ-800,000-832,000 ₪ לדירות 3 חדרים", "sale", "CONSISTENT", f"edit {e1}", rooms=3, official="808,800 (1-3.2026)", figures=2)
C("p@4311", "כ-1.19-1.22 מיליון ₪ לדירות 4 חדרים", "sale", "CONSISTENT", f"edit {e1}", rooms=4, official="1,203,200 (1-3.2026)", figures=2)
C("p@4311", "כ-1.86-1.89 מיליון ₪ לדירות 5 חדרים", "sale", "CONFLICT", f"edit {e1}", rooms=5, official="1,766,500 (7-9.2025, latest published)", figures=2)
C("p@4311", "כ-2.53-2.59 מיליון ₪ בדירות 6 חדרים ומעלה", "sale", "UNSOURCED", f"edit {e1}", rooms="6+", figures=2)
C("p@4311", "מחיר ממוצע בעיר עומד סביב 1.18 מיליון ₪", "sale_avg", "CONSISTENT", f"edit {e1}", rooms="all", official="1,153,400 (1-3.2026, +2.3%)",
  note="restated as the all-rooms median")
C("p@4311", "מחיר ממוצע למ״ר סביב 11,900 ₪", "per_m2", "UNSOURCED", f"edit {e1}")
C("p@4311", "שכירות מבוקשת 2,300 / 2,600-2,760 / 3,170-3,640 / 4,750-5,740 ₪", "rent", "UNSOURCED",
  f"keep (carried into edit {e1} with the same figures, labelled as listing asks; page checked 6.6.2026)", figures=7)
C("p@5139", "מחיר ממוצע עירוני של כ-1,179,412 ₪", "sale_avg", "CONSISTENT", f"edit {e2}", rooms="all", official="1,153,400 (+2.3%)")
C("p@5139", "מחיר ממוצע של כ-11,900 ₪ למ״ר", "per_m2", "UNSOURCED", f"edit {e2}")
C("p@5531", "דירות 2 חדרים סביב 616,277-649,500 ₪", "sale", "UNSOURCED", f"edit {e3}", rooms=2, figures=2)
C("p@5531", "דירות 3 חדרים סביב 800,000-832,043 ₪", "sale", "CONSISTENT", f"edit {e3}", rooms=3, official="808,800", figures=2)
C("p@5531", "דירות 4 חדרים סביב 1,195,000-1,224,662 ₪", "sale", "CONSISTENT", f"edit {e3}", rooms=4, official="1,203,200", figures=2)
C("p@5531", "דירות 5 חדרים סביב 1,865,000-1,888,938 ₪", "sale", "CONFLICT", f"edit {e3}", rooms=5, official="1,766,500 (7-9.2025)", figures=2)
C("p@5531", "דירות 6 חדרים סביב 2,533,982-2,590,000 ₪", "sale", "UNSOURCED", f"edit {e3}", rooms=6, figures=2)
C("p@5934", "חציון שכירות כ-2,600, ממוצע כ-3,003, 628 מודעות; 3 חדרים 2,759", "rent", "UNSOURCED", KEEPR, figures=3)
C("p@8807", "4 חדרים 87 מ״ר בשכונה ה ב-860,000; 4 חדרים 109 מ״ר בנווה זאב ב-1,100,000", "deal", "UNSOURCED",
  f"edit {e5}", rooms=4, figures=2,
  note="individual deals (8.5.2025 and 5.5.2025 in the deals table); kept with the month added to the sentence")
C("tr@9405", "2 חדרים | 649,500 | 616,277 | 12,490-12,665 למ״ר", "sale", "UNSOURCED", f"edit {e6}", rooms=2, figures=4)
C("tr@9647", "3 חדרים | ביקוש 800,000 | עסקה ממוצעת 832,043", "sale", "CONSISTENT", f"edit {e6}", rooms=3, official="808,800", figures=2)
C("tr@9647", "3 חדרים | 10,811-11,571 למ״ר", "per_m2", "UNSOURCED", f"edit {e6}", rooms=3, figures=2)
C("tr@9883", "4 חדרים | ביקוש 1,195,000 | עסקה ממוצעת 1,224,662", "sale", "CONSISTENT", f"edit {e6}", rooms=4, official="1,203,200", figures=2)
C("tr@9883", "4 חדרים | 11,065-11,527 למ״ר", "per_m2", "UNSOURCED", f"edit {e6}", rooms=4, figures=2)
C("tr@10133", "5 חדרים | ביקוש 1,865,000 | עסקה ממוצעת 1,888,938", "sale", "CONFLICT", f"edit {e6}", rooms=5, official="1,766,500 (7-9.2025)", figures=2)
C("tr@10133", "5 חדרים | 11,303-12,856 למ״ר", "per_m2", "UNSOURCED", f"edit {e6}", rooms=5, figures=2)
C("tr@10376", "6 חדרים ומעלה | 2,590,000 | 2,533,982 | 10,000-13,552 למ״ר", "sale", "UNSOURCED", f"edit {e6}", rooms="6+", figures=4)
C("p@11490", "אזור תעשיה 1,900,618 ... שכונה ד 730,698 (5 אזורים, כל החדרים)", "sale_nb", "UNSOURCED", f"edit {e8}", figures=5,
  official="4-room medians: אזור תעשיה 1,772,300, רמות הרכס 1,397,700, נווה זאב 1,319,800, ד 916,400")
C("p@11490", "15,814 / 12,583 / 12,993 / 11,803 / 12,019 ₪ למ״ר", "per_m2", "UNSOURCED", f"edit {e8}", figures=5)
C("tr@12147..14073", "טבלת מחיר ממוצע לפי שכונה (10 שורות, כל החדרים)", "sale_nb", "UNSOURCED", f"edit {e9}", figures=10,
  note="e.g. שכונה ד 730,698 all rooms vs official ד 3 rooms 686,700 / 4 rooms 916,400")
C("tr@12147..14073", "טבלת מחיר למ״ר לפי שכונה (10 שורות)", "per_m2", "UNSOURCED", f"edit {e9}", figures=10)
C("p@14302", "בשנת 2023: מצדה 62 עסקאות 773,161 ... בני אור 30 עסקאות 794,966 (8 רחובות)", "sale_street", "STALE", f"edit {e10}", figures=8,
  note="2023 averages, no room counts; deal counts 30-62 go with them")
C("tr@15857..16887", "טבלת שכירות לפי חדרים: מבוקשת לפי מקור אחד / חציון לפי מקור נוסף / טווח עבודה", "rent", "UNSOURCED", KEEPR, figures=21)
C("p@17119", "חציון שכירות לפי שכונה: ב 2,366 ... נווה זאב 5,377 (11 אזורים)", "rent", "UNSOURCED", KEEPR, figures=11)
C("tr@18708..19883", "טבלת 6 עסקאות לפי תאריך, רחוב, חדרים ושטח (27.4-8.5.2025)", "deal", "UNSOURCED", "keep (individual dated deals)", figures=6)
C("p@21252", "חציון שכירות פארק הנחל 5,313, נווה זאב 5,377, שכונה ג 2,672", "rent", "UNSOURCED", KEEPR, figures=3)
C("p@26305", "FAQ: דירת 3 חדרים 800,000-832,000 ₪", "sale", "CONSISTENT", f"edit {e11}", rooms=3, official="808,800", figures=2)
C("p@26305", "FAQ: מחיר למ״ר 10,811-11,571 ₪", "per_m2", "UNSOURCED", f"edit {e11}", rooms=3, figures=2)
C("p@26626", "FAQ: דירת 4 חדרים 1.19-1.22 מיליון ₪", "sale", "CONSISTENT", f"edit {e12}", rooms=4, official="1,203,200", figures=2)
C("p@26626", "FAQ: 'עסקאות אחרונות' 750,000 / 860,000 / 1,100,000 ₪", "deal", "STALE", f"edit {e12}", rooms=4, figures=3,
  note="April-May 2025 deals called recent; kept with their months")
C("p@26889", "FAQ: מחיר ממוצע למ״ר 11,900; יא 9,951, ד 12,019, ב 12,967, 15,814", "per_m2", "UNSOURCED", f"edit {e13}", figures=5)
C("p@27499", "FAQ שכירות: חציון 2,600, ממוצע 3,003, לפי חדרים 2,200-5,738", "rent", "UNSOURCED", KEEPR, figures=10)

P.write(notes=(
    "The official price list is not on this page yet; the edits align the body with it in advance. 5 rooms has no median for 10-12.2025 "
    "or 1-3.2026, so every 5-room figure is the latest published, 7-9.2025 (1,766,500), with its year-earlier quarter 7-9.2024 "
    "(1,846,700), written as such in the text and the table. Not audited as claims: sizes (50-191 m2, 87 / 109 m2), 3.5 rooms in the "
    "deals table, the CBS release number and date (p@20130), counts of deals or weeks in advice (5-10 deals, 5 deals, 2-4 weeks). "
    "Rents are kept: the page labels them as asking rents from listings (628 active listings at one check) and dates its check "
    "(6.6.2026); the lead and the source statement now call them listing figures. The deals table (six dated deals, April-May 2025) "
    "is kept; the 860,000 / 1,100,000 deals in p@8807 are the same dated deals, and edit 5 adds their month to the sentence. The three "
    "remaining check.py SUSPECTs are these individual dated deals (p@8807 twice, the 8.5.2025 row of the deals table). Name mapping: 'שכונה ב/ד/ה' = official 'ב', 'ד', 'ה'; 'אזור תעשיה' exact; Neve Menachem, Shchuna Tet, "
    "Alef and Gimel are not in the city file (the city file keeps only 8 neighbourhoods; the official files DO hold 1-3.2026 medians for some of the others (checked 7.10.2026), so these rows say 'לא מוצג במחירון' (not shown in the page's list), never 'לא פורסם'). Official medians also exist for שכונה ו and שכונה יא, which the table does "
    "not list; not added. The page writes m2 as 'מ״ר' (gershayim) and the currency as ₪; the new text follows."))
