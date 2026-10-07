# -*- coding: utf-8 -*-
"""Ashdod (page 4587): body alignment with the official price list (1-3.2026). Built on the Ashkelon gold example."""
import re
from mk import Page

P = Page("ashdod-apartment-prices")


def tbl(headers, rows):
    """table in this page's own style: line breaks, <thead>/<tr>/<tbody> without dir, dir="rtl" on th/td."""
    out = ['<table dir="rtl">', "<thead>", "<tr>"] + [f'<th dir="rtl">{x}</th>' for x in headers] + ["</tr>", "</thead>", "<tbody>"]
    for r in rows:
        out += ["<tr>"] + [f'<td dir="rtl">{x}</td>' for x in r] + ["</tr>"]
    out += ["</tbody>", "</table>"]
    return "\n".join(out)


def rows_of(anchor):
    html = P.table_html(anchor)
    return [re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S) for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", html.split("<tbody", 1)[1], re.S)]


# ---------------- edits ----------------
# 1. lead paragraph above the price list
old1 = P.find("מחירי דירות באשדוד נעים בדרך כלל סביב 1.33-1.39 מיליון ש\"ח לדירת 2 חדרים", "בהתאם לשיטת המדידה, סוג הדירות והתקופה.")
new1 = ("מחירי דירות באשדוד, לפי נתוני רשות המסים לרבעון הראשון של 2026: חציון מחיר העסקה היה 1,603,300 ש\"ח לדירת 3 חדרים, "
        "2,130,200 ש\"ח לדירת 4 חדרים ו-2,784,800 ש\"ח לדירת 5 חדרים, ו-2,030,100 ש\"ח לכל הדירות. דירות 2 חדרים ודירות 6 חדרים "
        "ומעלה כדאי לבדוק מול עסקאות דומות ברחוב וברובע, ודירות גדולות, קרבה לים, מרינה, קומה גבוהה, ממ\"ד, חניה, מעלית ובנייה "
        "חדשה משנים את המחיר בפועל. בדפי נתונים פרטיים המחיר למ\"ר מוצג בטווח רחב של כ-21,000-26,800 ש\"ח למ\"ר, בהתאם לשיטת "
        "המדידה, סוג הדירות והתקופה.")
e1 = P.edit(old1, new1, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "rooms.all.latest", "page"], "CONFLICT",
            "Lead above the list: the 3-room range 1.66-1.68M excludes the official median 1,603,300 (1-3.2026); the 4- and 5-room ranges and the "
            "2.0-2.06M city average were consistent and are restated as the medians. The undated 2-room and 6+-room ranges are dropped; the "
            "per-m2 range (private data pages, page checked 6.6.2026) and the rent sentence that follows are kept.")

# 2. sentence before the rooms table
old2 = "עם זאת, באשדוד הטבלה צריכה להיקרא כטווח ולא כמחיר קשיח."
new2 = ("הטבלה הבאה מציגה את חציון מחיר העסקה באשדוד לפי מספר חדרים, לפי נתוני רשות המסים לרבעון הראשון של 2026, לצד החציון "
        "באותו רבעון שנה קודם לכן. עם זאת, החציון הוא נקודת אמצע ולא מחיר קשיח.")
e2 = P.edit(old2, new2, ["data_quarter"], "WORDING", "Introduces the replaced rooms table (edit 3), which no longer shows ranges.")

# 3. rooms table
A3 = '<th dir="rtl">מחיר פתיחה נפוץ לפי נתוני ביקוש ועסקאות</th>'
N3 = {r[0]: r[-1] for r in rows_of(A3)}
new3 = tbl(["סוג דירה", "חציון מחיר העסקה, ינואר-מרץ 2026", "ינואר-מרץ 2025", "שינוי בשנה", "מה בודקים לפני שמסיקים שווי"], [
    ["3 חדרים", "1,603,300 ש\"ח", "1,598,300 ש\"ח", "עלייה של 0.3%", N3["3 חדרים"]],
    ["4 חדרים", "2,130,200 ש\"ח", "2,006,000 ש\"ח", "עלייה של 6.2%", N3["4 חדרים"]],
    ["5 חדרים", "2,784,800 ש\"ח", "2,955,900 ש\"ח", "ירידה של 5.8%", N3["5 חדרים"]],
])
e3 = P.table(A3, new3, ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct",
                        "rooms.5.latest", "rooms.5.year_ago", "rooms.5.change_pct"], "CONFLICT",
             "Rooms table: the 3-room 'common opening price' 1.66-1.68M contradicts the official median 1,603,300; the 2-room and 6+-room rows "
             "have no official series and no dated source, and the per-m2 column is asking data. Replaced by the official medians with the "
             "year-earlier quarter; the check notes of rows 3-5 are kept word for word.")

# 4. paragraph after the table: the 6+-room figures
old4 = P.find("הפער בין נתונים שונים בדירות 6 חדרים ומעלה", "יכולים שניהם להיות רלוונטיים, אך לנכסים שונים.")
new4 = ("המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים ודירות 6 חדרים ומעלה כדאי לבדוק מול עסקאות דומות ברחוב "
        "וברובע. בדירות 6 חדרים ומעלה בולטת הבעיה בהסתמכות על ממוצע יחיד. דירות גדולות יכולות לכלול דירות גג, פנטהאוזים, דירות גן "
        "ודירות רגילות שהורחבו או תוכננו מחדש. לכן שני מחירים רחוקים זה מזה יכולים שניהם להיות רלוונטיים, אך לנכסים שונים.")
e4 = P.edit(old4, new4, ["data_quarter"], "UNSOURCED",
            "Follows edit 3: the 6+-room figures 3.74M / 4.49M (no source, no date) leave with the table row; the sentence on 2 / 6+ rooms is added.")

# 5. Rova V and Rova G averages in the neighbourhood intro
old5 = P.find("ברובע ו וברובע ג, למשל, הוצגו בדפי נתונים פרטיים מחירים ממוצעים", "יכולות לסטות משמעותית מהממוצע.")
new5 = ("ברובע ו וברובע ג, למשל, חציון מחיר העסקה לדירת 3 חדרים ברבעון הראשון של 2026 היה 1,613,900 ש\"ח ו-1,506,400 ש\"ח "
        "בהתאמה, לפי נתוני רשות המסים, ובדפי נתונים פרטיים הוצגה בהם שכירות סביב 4,000-4,200 ש\"ח, אך נתון כזה אינו אומר שכל דירה "
        "ברובע נמכרת סביב אותו מספר. דירה משופצת, קומה גבוהה, חניה ומעלית יכולות לסטות משמעותית מהחציון.")
e5 = P.edit(old5, new5, ["neighbourhoods[רובע ו].rooms.3", "neighbourhoods[רובע ג].rooms.3", "page"], "UNSOURCED",
            "All-rooms neighbourhood averages 1.59-1.69M from private data pages with no period; replaced by the official 3-room medians of "
            "Rova V and Rova G. The rent 4,000-4,200 (private data pages, page checked 6.6.2026) is kept.")

# 6-7. neighbourhood table cells for Rova V and Rova G
old6 = "בדוגמה פרטית: סביב 1,689,478 ש\"ח וסביב 22,822 ש\"ח למ\"ר"
new6 = "חציון מחיר העסקה, ינואר-מרץ 2026: 1,613,900 ש\"ח לדירת 3 חדרים ו-1,924,700 ש\"ח לדירת 4 חדרים"
e6 = P.edit(old6, new6, ["neighbourhoods[רובע ו].rooms.3", "neighbourhoods[רובע ו].rooms.4"], "UNSOURCED",
            "Table cell: a 'private example' all-rooms average and per-m2 for Rova V, no period; replaced by the official medians.")
old7 = "בדוגמה פרטית: סביב 1,592,084 ש\"ח וסביב 21,472 ש\"ח למ\"ר"
new7 = "חציון מחיר העסקה, ינואר-מרץ 2026: 1,506,400 ש\"ח לדירת 3 חדרים"
e7 = P.edit(old7, new7, ["neighbourhoods[רובע ג].rooms.3"], "UNSOURCED",
            "Table cell: a 'private example' all-rooms average and per-m2 for Rova G, no period; replaced by the official 3-room median.")

# 8. the paragraph after the table calls the figure an average
old8 = "אין להעתיק את הממוצע לכל דירה ברובע."
new8 = "אין להעתיק את החציון לכל דירה ברובע."
e8 = P.edit(old8, new8, ["page"], "WORDING", "Follows edits 5-7: the Rova V / Rova G figure is now an official median, not an average.")

# 9. rent and yield table: purchase prices -> official medians, yield column removed
A9 = '<th dir="rtl">תשואה גולמית משוערת</th>'
R9 = rows_of(A9)
MED = {"2 חדרים": "לא פורסם", "3 חדרים": "1,603,300 ש\"ח", "4 חדרים": "2,130,200 ש\"ח", "5 חדרים": "2,784,800 ש\"ח"}
new9 = tbl(["סוג דירה", "שכירות חודשית נפוצה", "חציון מחיר העסקה, ינואר-מרץ 2026", "הערת שימוש"],
           [[r[0], r[1], MED[r[0]], r[4]] for r in R9])
e9 = P.table(A9, new9, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
             "Rent table: the purchase-price column repeats the old ranges (3 rooms 1.66-1.68M in conflict with 1,603,300) and the gross-yield "
             "column is derived from them. Purchase prices replaced by the official medians, the yield column removed (no new arithmetic); the "
             "rents and the usage notes are kept word for word.")

# 10. deals and streets table: keep the three dated deals, drop the undated street averages
A10 = '<th dir="rtl">נתון שהוצג במקורות פרטיים</th>'
R10 = rows_of(A10)
new10 = tbl(["דוגמת עסקה או רחוב", "נתון שהוצג במקורות פרטיים", "מה אפשר ללמוד", "מה חייבים לבדוק"], R10[:3])
assert all("15.3.2026" in r[1] for r in R10[:3]) and all("עסקאות, מחיר ממוצע" in r[1] for r in R10[3:])
e10 = P.table(A10, new10, ["page"], "UNSOURCED",
              "Deals table: the seven street averages (43-25 deals per street) have no period and no named source and are removed; the three "
              "individual deals dated 15.3.2026 are kept word for word.")

# 11. new projects: marketing ranges
old11 = P.find("בפרויקטים חדשים מוצגים לעיתים טווחים שיווקיים כמו", "צריך להתייחס בזהירות למספרים כאלה,")
new11 = ("בפרויקטים חדשים מוצגים לעיתים טווחים שיווקיים לפי מספר חדרים ומחיר למ\"ר, וכדאי להשוות אותם לחציון מחיר העסקה בעיר: "
         "לפי נתוני רשות המסים לרבעון הראשון של 2026, 1,603,300 ש\"ח לדירת 3 חדרים, 2,130,200 ש\"ח לדירת 4 חדרים ו-2,784,800 ש\"ח "
         "לדירת 5 חדרים. צריך להתייחס בזהירות לטווחים שיווקיים,")
e11 = P.edit(old11, new11, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest"], "CONFLICT",
             "New-project marketing ranges: 5 rooms 2.1-2.6M is below the official median 2,784,800; the 2-room, penthouse and 17,000-18,000 "
             "per-m2 ranges have no source or date (3 and 4 rooms were consistent). Replaced by the official city medians to compare against.")

# 12-16. FAQ answers
old12 = "דירת 4 חדרים באשדוד מוצגת בדרך כלל סביב 2.05-2.19 מיליון ש\"ח לפי מקורות פרטיים שונים, אך הטווח בפועל רחב."
new12 = "לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים באשדוד ברבעון הראשון של 2026 היה 2,130,200 ש\"ח, לעומת 2,006,000 ש\"ח שנה קודם לכן, אך הטווח בפועל רחב."
e12 = P.edit(old12, new12, ["rooms.4.latest", "rooms.4.year_ago"], "CONSISTENT",
             "FAQ 4 rooms: 2.05-2.19M was consistent with 2,130,200; rewritten from the same facts as the body.")

old13 = "דירת 3 חדרים באשדוד מוצגת סביב 1.66-1.68 מיליון ש\"ח, כאשר יש דוגמאות עסקאות כמו דירת 3 חדרים בשטח 75 מ\"ר במחיר 1,750,000 ש\"ח."
new13 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים באשדוד ברבעון הראשון של 2026 היה 1,603,300 ש\"ח. דירה מסוימת "
         "יכולה להימכר מעליו או מתחתיו: דירת 3 חדרים בשטח 75 מ\"ר ברחוב דב גאפונוב, למשל, נמכרה ב-1,750,000 ש\"ח.")
e13 = P.edit(old13, new13, ["rooms.3.latest", "page"], "CONFLICT",
             "FAQ 3 rooms: 1.66-1.68M vs the official 1,603,300; the individual deal (dated 15.3.2026 in the deals table) is kept as an example.")

old14 = "מקורות פרטיים מציגים מחיר ממוצע סביב 2,000,000-2,055,148 ש\"ח, אך ממוצע עירוני הוא נתון גס."
new14 = "לפי נתוני רשות המסים, חציון מחיר העסקה לכל הדירות באשדוד ברבעון הראשון של 2026 היה 2,030,100 ש\"ח, אך נתון עירוני כולל הוא נתון גס."
e14 = P.edit(old14, new14, ["rooms.all.latest"], "CONSISTENT",
             "FAQ city average: 2,000,000-2,055,148 was consistent with the official all-apartments median 2,030,100; rewritten from the same facts.")

old15 = ("מקורות שונים מציגים מחיר למ\"ר סביב 21,000 ש\"ח ועד 26,800 ש\"ח, ובטבלאות חדרים אפשר לראות גם כ-26,226 ש\"ח למ\"ר בדירות 2 "
         "חדרים וכ-18,250 ש\"ח למ\"ר בדירות 4 חדרים.")
new15 = ("דפי נתונים פרטיים שונים מציגים מחיר למ\"ר סביב 21,000 ש\"ח ועד 26,800 ש\"ח, ובנתוני ביקוש לפי חדרים הוצגו גם כ-26,226 ש\"ח "
         "למ\"ר בדירות 2 חדרים וכ-18,250 ש\"ח למ\"ר בדירות 4 חדרים.")
e15 = P.edit(old15, new15, ["page"], "WORDING",
             "FAQ per m2: the answer pointed at the per-m2 column of the rooms table, removed in edit 3; the asking figures are kept and labelled.")

old16 = "בדוגמאות פרטיות הוצג רובע ג סביב 1,592,084 ש\"ח ורובע ו סביב 1,689,478 ש\"ח, עם שכירות סביב 4,000-4,200 ש\"ח."
new16 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 3 חדרים היה 1,506,400 ש\"ח ברובע ג ו-1,613,900 ש\"ח "
         "ברובע ו, לעומת 1,603,300 ש\"ח בכל העיר. בדירות 4 חדרים, החציון ברובע ו היה 1,924,700 ש\"ח, לעומת 2,130,200 ש\"ח בכל העיר. "
         "בדפי נתונים פרטיים הוצגה ברובעים האלה שכירות סביב 4,000-4,200 ש\"ח.")
e16 = P.edit(old16, new16, ["neighbourhoods[רובע ג].rooms.3", "neighbourhoods[רובע ו].rooms.3", "neighbourhoods[רובע ו].rooms.4", "rooms.3.latest",
                            "rooms.4.latest", "page"], "UNSOURCED",
             "FAQ Rova G / Rova V: 'private examples' of all-rooms averages, no period; replaced by the official medians next to the city medians. "
             "The rent range is kept.")

# ---------------- claims inventory ----------------
C = P.claim
C("p@4292", "דירת 2 חדרים סביב 1.33-1.39 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e1}", rooms=2, note="no official 2-room series, no source; dropped")
C("p@4292", "דירת 3 חדרים סביב 1.66-1.68 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e1}", rooms=3, official="1,603,300 (1-3.2026)")
C("p@4292", "דירת 4 חדרים סביב 2.05-2.19 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e1}", rooms=4, official="2,130,200 (1-3.2026)", note="restated as the median")
C("p@4292", "דירת 5 חדרים סביב 2.78-2.89 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e1}", rooms=5, official="2,784,800 (1-3.2026)", note="restated as the median")
C("p@4292", "דירות 6 חדרים ומעלה סביב 3.74-4.49 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e1}", rooms=6)
C("p@4292", "מחיר ממוצע עירוני בדפי נתונים פרטיים סביב 2.0-2.06 מיליון ש\"ח", "sale_avg", "CONSISTENT", f"edit {e1}", rooms="all", official="2,030,100 (all apartments, 1-3.2026)", note="restated as the official median")
C("p@4292", "מחיר למ\"ר כ-21,000-26,800 ש\"ח", "per_m2", "UNSOURCED", "keep (private data pages, page checked 6.6.2026)")
C("p@4292", "שכירות 3,500 / 4,474-4,500 / 5,300 / 7,650 ש\"ח לפי חדרים", "rent", "UNSOURCED", "keep (private rent source on 250 active listings, page checked 6.6.2026)", figures=4)
C("p@42050", "ממוצע עירוני סביב 2,000,000 ש\"ח, מקור אחר סביב 2,055,148 ש\"ח", "sale_avg", "CONSISTENT", "keep (consistent with 2,030,100)", rooms="all", official="2,030,100", figures=2)
C("p@42050", "טבלאות ביקוש: דירת 4 חדרים סביב 2.19 מיליון ש\"ח", "sale", "CONSISTENT", "keep (consistent, +2.8%)", rooms=4, official="2,130,200")
C("tr@46717", "2 חדרים | כ-1.33-1.39 מיליון | כ-26,226 למ\"ר", "sale", "UNSOURCED", f"edit {e3}", rooms=2, figures=2, note="per-m2 figure stays in the per-m2 FAQ as an asking figure")
C("tr@46931", "3 חדרים | כ-1.66-1.68 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e3}", rooms=3, official="1,603,300")
C("tr@46931", "3 חדרים | כ-19,765 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"edit {e3}", rooms=3, note="column removed")
C("tr@47134", "4 חדרים | כ-2.05-2.19 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e3}", rooms=4, official="2,130,200")
C("tr@47134", "4 חדרים | כ-18,250 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"edit {e3}", rooms=4, note="column removed; the figure stays in the per-m2 FAQ")
C("tr@47336", "5 חדרים | כ-2.78-2.89 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e3}", rooms=5, official="2,784,800 (within rounding of the floor)")
C("tr@47336", "5 חדרים | כ-18,063 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"edit {e3}", rooms=5, note="column removed")
C("tr@47536", "6 חדרים ומעלה | כ-3.74-4.49 מיליון | כ-15,754 למ\"ר", "sale", "UNSOURCED", f"edit {e3}", rooms=6, figures=2)
C("p@47809", "מחיר של 3.74 מיליון ש\"ח ומחיר של 4.49 מיליון ש\"ח (6 חדרים ומעלה)", "sale", "UNSOURCED", f"edit {e4}", rooms=6, figures=2)
C("p@48982", "רובע ו ורובע ג: ממוצעים סביב 1.59-1.69 מיליון ש\"ח", "sale_nb", "UNSOURCED", f"edit {e5}", official="Rova V 3 rooms 1,613,900; Rova G 3 rooms 1,506,400")
C("p@48982", "רובע ו ורובע ג: שכירות סביב 4,000-4,200 ש\"ח", "rent", "UNSOURCED", "keep (private data pages, page checked 6.6.2026)")
C("tr@50730", "רובע ו | בדוגמה פרטית: 1,689,478 ש\"ח, 22,822 ש\"ח למ\"ר", "sale_nb", "UNSOURCED", f"edit {e6}", figures=2, official="Rova V 3/4: 1,613,900 / 1,924,700")
C("tr@50976", "רובע ג | בדוגמה פרטית: 1,592,084 ש\"ח, 21,472 ש\"ח למ\"ר", "sale_nb", "UNSOURCED", f"edit {e7}", figures=2, official="Rova G 3 rooms 1,506,400")
C("tr@52789..53452", "טבלת שכירות: 3,500 / 4,474-4,500 / 5,300 / 7,650 ש\"ח", "rent", "UNSOURCED", "keep (private rent source on 250 active listings, page checked 6.6.2026)", figures=4)
C("tr@52789", "טבלת שכירות: מחיר קנייה 2 חדרים כ-1.33-1.39 מיליון", "sale", "UNSOURCED", f"edit {e9}", rooms=2)
C("tr@53013", "טבלת שכירות: מחיר קנייה 3 חדרים כ-1.66-1.68 מיליון", "sale", "CONFLICT", f"edit {e9}", rooms=3, official="1,603,300")
C("tr@53240", "טבלת שכירות: מחיר קנייה 4 חדרים כ-2.05-2.19 מיליון", "sale", "CONSISTENT", f"edit {e9}", rooms=4, official="2,130,200")
C("tr@53452", "טבלת שכירות: מחיר קנייה 5 חדרים כ-2.78-2.89 מיליון", "sale", "CONSISTENT", f"edit {e9}", rooms=5, official="2,784,800")
C("tr@52789..53452", "תשואה גולמית 3.0%-3.2% / 3.2% / 2.9%-3.1% / 3.2%-3.3%", "yield", "UNSOURCED", f"edit {e9}", figures=4, note="derived from the old purchase ranges; column removed, no new yield computed")
C("p@53693", "שכירות חציונית 3,925 (250 מודעות), 3 חדרים 4,474, ממוצע ארצי 4,400", "rent", "UNSOURCED", "keep (listing sample of 250 active listings, page checked 6.6.2026)", figures=3)
C("tr@55475..55936", "3 עסקאות 15.3.2026: 1,750,000 / 2,700,000 / 3,800,000 ש\"ח", "deal", "UNSOURCED", "keep (individual dated deals, 15.3.2026)", figures=3)
C("tr@56181..57493", "ממוצעי רחוב: גור דב 1,604,604 ... רוגוזין 1,850,076 (7 שורות)", "sale_street", "UNSOURCED", f"edit {e10}", figures=7, note="no period, 'private sources'")
C("p@58695", "פרויקטים חדשים: 2 חדרים 800,000-950,000 ש\"ח", "sale_new_used", "UNSOURCED", f"edit {e11}", rooms=2)
C("p@58695", "פרויקטים חדשים: 3 חדרים 1.45-1.65 מיליון ש\"ח", "sale_new_used", "CONSISTENT", f"edit {e11}", rooms=3, official="1,603,300")
C("p@58695", "פרויקטים חדשים: 4 חדרים 1.5-2.2 מיליון ש\"ח", "sale_new_used", "CONSISTENT", f"edit {e11}", rooms=4, official="2,130,200")
C("p@58695", "פרויקטים חדשים: 5 חדרים 2.1-2.6 מיליון ש\"ח", "sale_new_used", "CONFLICT", f"edit {e11}", rooms=5, official="2,784,800")
C("p@58695", "פרויקטים חדשים: פנטהאוזים 2.5-4.3 מיליון ש\"ח", "sale_new_used", "UNSOURCED", f"edit {e11}")
C("p@58695", "דירות חדשות: 17,000-18,000 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"edit {e11}")
C("p@63494", "FAQ: דירת 4 חדרים סביב 2.05-2.19 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e12}", rooms=4, official="2,130,200")
C("p@63829", "FAQ: דירת 3 חדרים סביב 1.66-1.68 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e13}", rooms=3, official="1,603,300")
C("p@63829", "FAQ: דירת 3 חדרים 75 מ\"ר במחיר 1,750,000 ש\"ח", "deal", "UNSOURCED", "keep (individual deal, dated 15.3.2026 in the deals table)", rooms=3)
C("p@64107", "FAQ: מחיר ממוצע סביב 2,000,000-2,055,148 ש\"ח", "sale_avg", "CONSISTENT", f"edit {e14}", rooms="all", official="2,030,100")
C("p@64398", "FAQ: 21,000-26,800 למ\"ר; 26,226 (2 חד'); 18,250 (4 חד')", "per_m2", "UNSOURCED", f"keep (private data pages and asking data, page checked 6.6.2026; reference reworded in edit {e15})", figures=3)
C("p@65051", "FAQ: רובע ג סביב 1,592,084, רובע ו סביב 1,689,478 ש\"ח", "sale_nb", "UNSOURCED", f"edit {e16}", figures=2, official="Rova G 3 rooms 1,506,400; Rova V 3/4 rooms 1,613,900 / 1,924,700")
C("p@65051", "FAQ: שכירות סביב 4,000-4,200 ש\"ח", "rent", "UNSOURCED", "keep (private data pages, page checked 6.6.2026)")
C("p@65347", "FAQ שכירות: 3,500 / 4,474-4,500 / 5,300 / 7,650; חציונית 3,925", "rent", "UNSOURCED", "keep (listing sample of 250 active listings, page checked 6.6.2026)", figures=5)

P.write(notes=(
    "Not audited as claims (illustrations, not market statements): renovation cost 150,000-300,000 (p@44754 and the checks table), sizes "
    "88 / 115 / 75 / 138 / 192 m2, the yield if-example 2,200,000 / 5,300 / 2.9% / 2,500,000 (p@54038, no room count), the per-m2 arithmetic "
    "on the three dated deals (p@57708, 'אם דירת 3 חדרים של 75 מ\"ר נמכרה ב-1,750,000'), the FAQ yield example 2,190,000 / 5,300 / 63,600 / "
    "2.9% (p@65640, 'לדוגמה'), the 3,264-deal count (p@54848), the 39-day selling time and the CBS release number. Kept as consistent with no "
    "edit: the opening of p@42050 (city averages 2,000,000 / 2,055,148 and a 4-room asking 2.19M are all within tolerance). Remaining "
    "SUSPECT lines: p@42050 is a false positive of the heuristic (2,000,000 is the all-rooms city average, consistent with 2,030,100; the "
    "'4 rooms' in that sentence belongs to the 2.19M asking figure, consistent with 2,130,200); all the others are the individual deals dated 15.3.2026 (Dov Gaponov 3 rooms 75 m2 1,750,000; Uzi Hitman 5 rooms 192 m2 3,800,000) in the "
    "deals table, in the per-m2 if-examples of p@57708 and in the 3-room FAQ; they are single dated deals, not market levels. Unsure: all "
    "three deals carry the same date, 15.3.2026, which is also the date of the CBS release cited in p@58125; it may be a reading date rather "
    "than the deal date, so the FAQ names the street without a date. Official quirk: the all-apartments median rose 12.7% in a year "
    "(1,801,100 to 2,030,100) while 3 rooms +0.3%, 4 rooms +6.2% and 5 rooms -5.8%, a mix effect; the new text uses the all-apartments "
    "median only as the level, not its change. Rova V's 3-room median (1,613,900) is slightly above the city's (1,603,300), so the FAQ "
    "'are Rova G and Rova V cheaper' now answers with both room counts. Names map exactly (רובע ג, רובע ו); Rova Yod-Gimel, Tet-Vav and "
    "Yod-Zayin have no official median and stay qualitative."))
