# -*- coding: utf-8 -*-
"""Ramat HaSharon (page 160): body alignment with the official price list (1-3.2026). Built on the b_ashkelon.py pattern.
The page writes ש״ח / מ״ר with gershayim (U+05F4); the new text does the same."""
import re
from mk import Page

P = Page("ramat-hasharon-apartment-prices")
SH = "ש״ח"

# ---------------- edits ----------------
# 1. the 4-room spread in the opening section
old1 = ("אותה דירת 4 חדרים יכולה להיבדק סביב 3.2 מיליון ש״ח בבניין ותיק, סביב 3.8 עד 4.5 מיליון ש״ח בדירה טובה יותר עם מעלית וחניה, "
        "וסביב 4.7 עד 5.5 מיליון ש״ח כאשר מדובר בדירה חדשה, גדולה, משודרגת או במיקום מבוקש במיוחד.")
new1 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים ברמת השרון ברבעון הראשון של 2026 היה 3,809,600 ש״ח. אותה דירת 4 חדרים "
        "יכולה להימכר מתחת לחציון בבניין ותיק, סביב 3.8 עד 4.5 מיליון ש״ח בדירה טובה יותר עם מעלית וחניה, ומעל לכך כאשר מדובר בדירה "
        "חדשה, גדולה, משודרגת או במיקום מבוקש במיוחד.")
e1 = P.edit(old1, new1, ["rooms.4.latest", "page"], "CONFLICT",
            "4 rooms: 'about 3.2M in an old building' and '4.7-5.5M new' are outside the official median 3,809,600 (1-3.2026); the 3.8-4.5M "
            "range for a better flat contains it and is kept. The official median now opens the sentence.")

# 2. the city average from public market data
old2 = "בבדיקת נתוני שוק פומביים שנקראו ביום 05.06.2026 הופיע ממוצע רכישה עירוני של כ-3,969,719 ש״ח וממוצע שכירות של כ-9,500 ש״ח."
new2 = ("לפי נתוני רשות המסים, חציון מחיר העסקה ברמת השרון, בכל מספרי החדרים, היה 4,212,500 ש״ח ברבעון הראשון של 2026. בבדיקת נתוני "
        "שוק פומביים שנקראו ביום 05.06.2026 הופיע ממוצע שכירות של כ-9,500 ש״ח.")
e2 = P.edit(old2, new2, ["rooms.all.latest", "page"], "CONFLICT",
            "City purchase average 3,969,719 (market data read 5.6.2026) is 5.8% below the official all-rooms median 4,212,500 (1-3.2026); "
            "replaced by the official figure. The dated rent average 9,500 is kept.")

# 3. intro of the rooms table
old3 = "לכן הטבלה מציגה טווחי עבודה לפי נתוני שוק שנבדקו, ולא מחיר קבוע."
new3 = ("לכן הטבלה מציגה את חציון מחיר העסקה לפי נתוני רשות המסים לרבעון הראשון של 2026, לצד החציון באותו רבעון שנה קודם לכן, "
        "ולא מחיר קבוע לכל דירה.")
e3 = P.edit(old3, new3, ["rooms.3.latest", "rooms.3.year_ago"], "CONFLICT",
            "The intro announced working ranges from market data; the table is replaced by official medians (edit 4).")

# 4. the rooms table
new4 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">מספר חדרים</th>
<th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>
<th dir="rtl">ינואר-מרץ 2025</th>
<th dir="rtl">שינוי בשנה</th>
<th dir="rtl">פירוש מעשי</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">3 חדרים</td>
<td dir="rtl">3,544,800 ש״ח</td>
<td dir="rtl">3,044,100 ש״ח</td>
<td dir="rtl">עלייה של 16.4%</td>
<td dir="rtl">פלח מבוקש לזוגות, משפחות קטנות ומשפרי דיור שמעדיפים כניסה לרמת השרון במחיר נמוך יותר.</td>
</tr>
<tr dir="rtl">
<td dir="rtl">4 חדרים</td>
<td dir="rtl">3,809,600 ש״ח</td>
<td dir="rtl">4,265,500 ש״ח</td>
<td dir="rtl">ירידה של 10.7%</td>
<td dir="rtl">זהו פלח מרכזי בעיר. ההבדל בין 3.4 ל-4.6 מיליון ש״ח נובע לעיתים ממעלית, חניה, מרפסת ומצב הבניין.</td>
</tr>
<tr dir="rtl">
<td dir="rtl">5 חדרים</td>
<td dir="rtl">4,663,600 ש״ח</td>
<td dir="rtl">4,776,200 ש״ח</td>
<td dir="rtl">ירידה של 2.4%</td>
<td dir="rtl">דירות משפחתיות גדולות מושפעות מאוד משטח, תכנון, קומה, ממ״ד, מרפסת וחניה כפולה.</td>
</tr>
</tbody>
</table>"""
e4 = P.table('<th dir="rtl">טווח מחיר דירה חדשה</th>', new4,
             ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct",
              "rooms.5.latest", "rooms.5.year_ago", "rooms.5.change_pct", "page"], "CONFLICT",
             "Rooms table: 3-room second-hand 2.75-3.49M, 4-room new 4.01-5.0M and 5-room new 5.42-6.7M exclude the official medians "
             "(3,544,800 / 3,809,600 / 4,663,600, 1-3.2026); the 2-room and 6+-room rows have no official counterpart and no source. Replaced by "
             "the official medians with the year-earlier quarter; the practical notes of rows 3-5 are kept word for word (the 3.4-4.6M spread "
             "in the 4-room note contains the median). The rent column leaves this table: the same rent ranges stay in the rent table below.")

# 5. the paragraph after the rooms table: 2 / 6+ rooms sentence, the 5.95M 'sale' without date
old5 = P.find("הטבלה גם מסבירה למה לא מספיק לשאול כמה עולה דירת 4 חדרים ברמת השרון.", "הבניין והסטנדרט משנים את התוצאה.")
new5 = ("המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים ודירות 6 חדרים ומעלה כדאי לבדוק מול עסקאות דומות ברחוב "
        "ובשכונה. גם החציון אינו מספיק כדי לענות כמה עולה דירת 4 חדרים ברמת השרון. דירה של 92 מ״ר שנמכרה סביב 3.2 מיליון ש״ח באפריל "
        "2026 אינה מספר השוואה ישיר לדירה גדולה של 127 מ״ר שנמכרה במחיר גבוה בהרבה. שתיהן יכולות להיקרא דירת 4 חדרים, אבל המחיר "
        "למ״ר, המיקום, הבניין והסטנדרט משנים את התוצאה.")
e5 = P.edit(old5, new5, ["data_quarter", "page"], "UNSOURCED",
            "Follows edit 4 (2-room and 6+-room rows left the table). The 92 m2 / 3.2M sale is the dated deal of 16.04.2026 in the deals table "
            "(date added); the 127 m2 / 5.95M 'sale' appears nowhere else on the page and has no date or source: kept without the number.")

# 6. lead-in of the neighbourhood table: the official neighbourhood medians
old6 = "ואזורים שבהם מלאי חדש או צמודי קרקע מעלים את הממוצע."
new6 = ("ואזורים שבהם מלאי חדש או צמודי קרקע מעלים את הממוצע. לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת "
        "4 חדרים היה 3,560,000 ש״ח במורשה ו-3,872,200 ש״ח בהדר, ולדירת 5 חדרים 3,848,700 ש״ח במורשה ו-4,631,300 ש״ח בהדר. בשאר "
        "השכונות כדאי להשוות לעסקאות דומות ברחוב ובשכונה.")
e6 = P.edit(old6, new6, ["neighbourhoods[מורשה].rooms.4", "neighbourhoods[הדר].rooms.4", "neighbourhoods[מורשה].rooms.5",
                         "neighbourhoods[הדר].rooms.5"], "STALE",
            "The neighbourhood table (edit 7) loses its 2023 averages; the official medians for the two neighbourhoods in the official file "
            "(Morasha, Hadar; 1-3.2026) are given in the lead-in instead.")

# 7. neighbourhood table: the 2023 deal-count/average column leaves; the qualitative columns are kept word for word
old7 = P.table_html('<th dir="rtl">נתון עסקאות או טווח שנבדק</th>')


def drop_col(tbl, idx):
    def row(m):
        cells = re.findall(r"<t[hd] dir=\"rtl\">.*?</t[hd]>\n", m.group(0), re.S)
        assert len(cells) == 4, cells
        out = m.group(0)
        return out.replace(cells[idx], "", 1)
    return re.sub(r"<tr dir=\"rtl\">\n.*?</tr>", row, tbl, flags=re.S)


new7 = drop_col(old7, 1)
# the Hadar check note pointed at the removed range ('הנתון'); reworded to point at the comparison deal
new7 = new7.replace("לבדוק אם הנתון מתייחס לדירה חדשה, יד שנייה, שדרוג,", "לבדוק אם העסקה להשוואה כוללת דירה חדשה או יד שנייה, שדרוג,")
assert "העסקה להשוואה כוללת" in new7
assert "2023" not in new7 and "ממוצע כ-" not in new7 and new7.count("<tr dir=\"rtl\">") == 8, new7
e7 = P.table('<th dir="rtl">נתון עסקאות או טווח שנבדק</th>', new7,
             ["page"], "STALE",
             "Neighbourhood table: deal counts and all-rooms averages from 2023 (Morasha 3,495,000 ... Neve Gan 5,450,000) presented as the "
             "current level, and an undated, unsourced 2.7-3.8M range for Hadar. The data column leaves the table; the area, relative-price and "
             "what-to-check columns stay word for word. Official neighbourhood medians are in the lead-in (edit 6).")

# 8. renovation range (tier 2)
old8 = "עם תשתיות ישנות וצורך בשיפוץ של 250,000 עד 600,000 ש״ח."
new8 = "עם תשתיות ישנות וצורך בשיפוץ יסודי."
e8 = P.edit(old8, new8, ["page"], "UNSOURCED", "A renovation-cost range with no source; rephrased without the number.", tier=2)

# 9. new vs second-hand table: the second-hand purchase cell
old9 = "3 חדרים סביב 2.75 עד 3.49 מיליון ש״ח, 5 חדרים סביב 4.55 עד 5.85 מיליון ש״ח"
new9 = "בדרך כלל נמוך מדירה חדשה דומה, לפי מצב הדירה, הקומה והשיפוץ הנדרש"
e9 = P.edit(old9, new9, ["page"], "CONFLICT",
            "Second-hand 3 rooms 2.75-3.49M excludes the official 3-room median 3,544,800 (1-3.2026); the cell is rephrased without numbers "
            "(the 5-room 4.55-5.85M part was consistent but sits in the same cell). The new-flat cell (3.35-3.9M / up to 6.7M) is consistent and kept.")

# 10. renovation range in the list (tier 2)
old10 = "פער של 200,000 עד 700,000 ש״ח בעלויות שיפוץ יכול להסביר פער במחיר."
new10 = "פער גדול בעלויות השיפוץ יכול להסביר פער במחיר."
e10 = P.edit(old10, new10, ["page"], "UNSOURCED", "A renovation-cost range with no source; rephrased without the number.", tier=2)

# 11. the 'two 4-room flats' illustration: made explicit and anchored to the official median
old11 = "שתי דירות 4 חדרים יכולות להופיע באותה קטגוריה, אך אחת תימכר סביב 3.35 מיליון ש״ח והשנייה סביב 4.75 מיליון ש״ח."
new11 = ("לדוגמה, שתי דירות 4 חדרים יכולות להופיע באותה קטגוריה, אך אחת תימכר ב-3.35 מיליון ש״ח, מתחת לחציון העירוני של 3,809,600 "
         "ש״ח ברבעון הראשון של 2026, והשנייה ב-4.75 מיליון ש״ח, הרבה מעליו.")
e11 = P.edit(old11, new11, ["rooms.4.latest", "page"], "WORDING",
             "An illustration of the spread within 4 rooms; marked as an example and placed against the official 4-room median.")

# 12-14. FAQ by rooms
old12 = ("דירת 3 חדרים ברמת השרון נעה בדרך כלל סביב 2.8 עד 3.4 מיליון ש״ח ביד שנייה, ובדירות חדשות או משודרגות סביב 3.35 עד 3.9 "
         "מיליון ש״ח.")
new12 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים ברמת השרון ברבעון הראשון של 2026 היה 3,544,800 ש״ח, לעומת 3,044,100 "
         "ש״ח ברבעון הראשון של 2025. החציון לדירות 3 חדרים בעיר משתנה בחדות בין רבעונים: ברבעון השלישי של 2025 הוא היה 2,564,400 ש״ח, "
         "ולכן כדאי להשוות גם לעסקאות מהרבעונים הקודמים. דירות חדשות או משודרגות נבדקות לרוב סביב 3.35 עד 3.9 מיליון ש״ח.")
e12 = P.edit(old12, new12, ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.quarters[7-9.2025]", "page"], "CONFLICT",
             "FAQ 3 rooms: second-hand 2.8-3.4M vs the official 3,544,800; the new-flat range 3.35-3.9M is consistent and kept. The 3-room "
             "series is sparse and jumpy (2,564,400 in 7-9.2025, 10-12.2025 not published), so the previous published quarter is shown.")
old13 = P.find("בדירות 4 חדרים רבות הטווח המעשי הוא כ-3.3 עד 4.6 מיליון ש״ח,", "ולכן חובה להשוות לפי שטח ומאפיינים.")
new13 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים ברמת השרון ברבעון הראשון של 2026 היה 3,809,600 ש״ח, לעומת 4,265,500 "
         "ש״ח שנה קודם לכן. בדירות 4 חדרים רבות הטווח המעשי הוא כ-3.3 עד 4.6 מיליון ש״ח, ובדירות חדשות או איכותיות במיוחד המחיר עשוי "
         "להיות גבוה מכך. בעסקאות שנבדקו מאפריל ומאי 2026 הופיעו דירות 4 חדרים שנמכרו ב-3.2 מיליון ש״ח, 4.6 מיליון ש״ח וגם 4.77 "
         "מיליון ש״ח, ולכן חובה להשוות לפי שטח ומאפיינים.")
e13 = P.edit(old13, new13, ["rooms.4.latest", "rooms.4.year_ago", "page"], "CONFLICT",
             "FAQ 4 rooms: 'about 5M and more' for new flats vs the official 3,809,600; the 3.3-4.6M range is consistent and kept; the three "
             "sales are the dated deals of 16.04, 07.05 and 28.04.2026 in the deals table (months added).")
old14 = "דירות 5 חדרים נבדקות לרוב סביב 4.5 עד 5.9 מיליון ש״ח ביד שנייה, ובדירות חדשות סביב 5.4 עד 6.7 מיליון ש״ח."
new14 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 5 חדרים ברמת השרון ברבעון הראשון של 2026 היה 4,663,600 ש״ח, לעומת 4,776,200 "
         "ש״ח שנה קודם לכן. דירות 5 חדרים נבדקות לרוב סביב 4.5 עד 5.9 מיליון ש״ח, ודירות חדשות נמכרות בדרך כלל מעל החציון.")
e14 = P.edit(old14, new14, ["rooms.5.latest", "rooms.5.year_ago", "page"], "CONFLICT",
             "FAQ 5 rooms: new flats 5.4-6.7M vs the official 4,663,600; the 4.5-5.9M range contains the median and is kept (its "
             "'second-hand' label dropped, since the median covers all deals).")

# 15. FAQ city average
old15 = P.find("במקורות שוק שנקראו ביום 05.06.2026 הופיעו ממוצעים סביב 3.97 עד 4.15 מיליון ש״ח לדירה.", "ונכסים מיוחדים.")
new15 = ("לפי נתוני רשות המסים, חציון מחיר העסקה ברמת השרון, בכל מספרי החדרים, היה 4,212,500 ש״ח ברבעון הראשון של 2026. נתון כזה "
         "מתאים להתמצאות ראשונית בלבד, מפני שהוא מערבב דירות קטנות, דירות גדולות, פרויקטים חדשים, יד שנייה ונכסים מיוחדים.")
e15 = P.edit(old15, new15, ["rooms.all.latest"], "CONFLICT",
             "FAQ average: 3.97-4.15M (market sources read 5.6.2026) just below the official all-rooms median 4,212,500 (1-3.2026); replaced "
             "by the official figure, the caution sentence kept.")

# 16. FAQ neighbourhoods: 'in the data checked' pointed at the removed 2023 averages
old16 = ("המחיר משתנה לפי תמהיל הנכסים, אך בנתונים שנבדקו נווה גן, קרית יערים וחלק מאזורי הפרימיום הציגו רמות מחיר גבוהות יחסית, בעוד "
         "מורשה יכולה להציג מחיר כניסה נמוך יותר בחלק מהמקרים.")
new16 = ("המחיר משתנה לפי תמהיל הנכסים, אך נווה גן, קרית יערים וחלק מאזורי הפרימיום נחשבים ליקרים יחסית, בעוד מורשה יכולה להציג מחיר "
         "כניסה נמוך יותר בחלק מהמקרים. לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 4 חדרים במורשה היה "
         "3,560,000 ש״ח, לעומת 3,809,600 ש״ח בכל העיר.")
e16 = P.edit(old16, new16, ["neighbourhoods[מורשה].rooms.4", "rooms.4.latest"], "WORDING",
             "'In the data checked' referred to the 2023 averages removed in edit 7; the Morasha statement is now backed by the official 4-room medians.")

# ---------------- claims inventory ----------------
C = P.claim
C("p@4333", "סביב כ-40,000 עד 48,000 ש״ח למ״ר בדירות רבות", "per_m2", "UNSOURCED", "keep (market sources read 5.6.2026, same paragraph; page checked 5.6.2026)", figures=2,
  note="weak source kind ('מקורות שוק'); the dated deals on the page run 31,724-45,890 per m2 without the outlier")
C("p@4333", "דירות 3 חדרים רבות נבדקות סביב 2.8 עד 3.9 מיליון ש״ח", "sale", "CONSISTENT", "keep (contains the official median)", rooms=3, official="3,544,800 (1-3.2026)", figures=2)
C("p@4333", "דירות 4 חדרים סביב 3.3 עד 4.6 מיליון ש״ח", "sale", "CONSISTENT", "keep (contains the official median)", rooms=4, official="3,809,600 (1-3.2026)", figures=2)
C("p@4333", "דירות 5 חדרים או דירות חדשות גדולות סביב 4.2 עד 6.7 מיליון ש״ח", "sale", "CONSISTENT", "keep (contains the official median)", rooms=5, official="4,663,600 (1-3.2026)", figures=2)
C("p@4333", "6 חדרים סביב 6.7 מיליון ש״ח ונכסים חריגים מעל 10 מיליון (מקורות שוק, 05.06.2026)", "deal", "UNSOURCED", "keep (dated market sources 5.6.2026; matches the dated deals of 18.05 and 26.04.2026)", rooms=6, figures=2)
C("p@4960", "דירת 4 חדרים סביב 3.2 מיליון ש״ח בבניין ותיק", "sale", "CONFLICT", f"edit {e1}", rooms=4, official="3,809,600 (1-3.2026)")
C("p@4960", "דירת 4 חדרים סביב 3.8 עד 4.5 מיליון ש״ח בדירה טובה יותר", "sale", "CONSISTENT", f"edit {e1}", rooms=4, official="3,809,600", figures=2, note="kept inside the rewrite")
C("p@4960", "דירת 4 חדרים סביב 4.7 עד 5.5 מיליון ש״ח בדירה חדשה", "sale_new_used", "CONFLICT", f"edit {e1}", rooms=4, official="3,809,600", figures=2)
C("p@5321", "ממוצע רכישה עירוני של כ-3,969,719 ש״ח (05.06.2026)", "sale_avg", "CONFLICT", f"edit {e2}", rooms="all", official="4,212,500 (1-3.2026), -5.8%")
C("p@5321", "ממוצע שכירות של כ-9,500 ש״ח (נתוני שוק פומביים, 05.06.2026)", "rent", "UNSOURCED", "keep (dated public market data, 5.6.2026)")
C("p@5321", "מקור אחר: מחיר דירה ממוצע של כ-4.15 מיליון ש״ח", "sale_avg", "CONSISTENT", "keep (within 5% of the official all-rooms median)", rooms="all", official="4,212,500")
C("p@5321", "3 חדרים חדשות כ-3.35 עד 3.9 מיליון ש״ח", "sale_new_used", "CONSISTENT", "keep (contains the official median)", rooms=3, official="3,544,800", figures=2)
C("p@5321", "4 חדרים חדשות כ-3.5 עד 5.0 מיליון ש״ח", "sale_new_used", "CONSISTENT", "keep (contains the official median)", rooms=4, official="3,809,600", figures=2)
C("p@5321", "5 חדרים חדשות כ-4.1 עד 6.7 מיליון ש״ח", "sale_new_used", "CONSISTENT", "keep (contains the official median)", rooms=5, official="4,663,600", figures=2)
C("tr@7883", "2 חדרים | כ-2.2 עד 2.9 מיליון ש״ח | כ-2.24 מיליון ש״ח ומעלה", "sale", "UNSOURCED", f"edit {e4}", rooms=2, figures=3, note="no official 2-room series; row leaves the table")
C("tr@8169", "3 חדרים | יד שנייה כ-2.75 עד 3.49 מיליון ש״ח", "sale_new_used", "CONFLICT", f"edit {e4}", rooms=3, official="3,544,800", figures=2)
C("tr@8169", "3 חדרים | חדשה כ-3.12 עד 3.9 מיליון ש״ח", "sale_new_used", "CONSISTENT", f"edit {e4}", rooms=3, official="3,544,800", figures=2)
C("tr@8451", "4 חדרים | יד שנייה כ-3.3 עד 4.6 מיליון ש״ח", "sale_new_used", "CONSISTENT", f"edit {e4}", rooms=4, official="3,809,600", figures=2)
C("tr@8451", "4 חדרים | חדשה כ-4.01 עד 5.0 מיליון ש״ח", "sale_new_used", "CONFLICT", f"edit {e4}", rooms=4, official="3,809,600", figures=2)
C("tr@8451", "4 חדרים | ההבדל בין 3.4 ל-4.6 מיליון ש״ח", "sale", "CONSISTENT", f"edit {e4}", rooms=4, official="3,809,600", figures=2, note="kept word for word in the note column")
C("tr@8741", "5 חדרים | יד שנייה כ-4.55 עד 5.85 מיליון ש״ח", "sale_new_used", "CONSISTENT", f"edit {e4}", rooms=5, official="4,663,600", figures=2)
C("tr@8741", "5 חדרים | חדשה כ-5.42 עד 6.7 מיליון ש״ח", "sale_new_used", "CONFLICT", f"edit {e4}", rooms=5, official="4,663,600", figures=2)
C("tr@9018", "6 חדרים ומעלה | כ-7.4 עד 9.5 מיליון בממוצעי פרסום | 8.95 מיליון ומעלה", "sale", "UNSOURCED", f"edit {e4}", rooms=6, figures=3, note="row leaves the table")
C("tr@7883..9018", "עמודת שכירות חודשית שנצפתה (5 שורות, 4,850 עד 13,500 ש״ח)", "rent", "UNSOURCED", f"edit {e4}", figures=10,
  note="column leaves the rooms table; the same ranges stay in the rent table tr@14231..15452")
C("p@9386", "דירה של 92 מ״ר שנמכרה סביב 3.2 מיליון ש״ח", "deal", "UNSOURCED", f"edit {e5}", rooms=4, note="the dated deal of 16.04.2026 (רד״ק 9); kept, month added")
C("p@9386", "דירה של 127 מ״ר שנמכרה סביב 5.95 מיליון ש״ח", "deal", "UNSOURCED", f"edit {e5}", rooms=4, official="4 rooms 3,809,600",
  note="no date, no source, not in the deals table; number dropped")
C("tr@10649..11908", "מורשה 168 עסקאות ב-2023 ממוצע 3,495,000 ... נווה מגן 12 עסקאות ממוצע 3,267,500 (6 שורות)", "sale_nb", "STALE", f"edit {e7}", rooms="all", figures=6,
  official="Morasha 4 rooms 3,560,000, 5 rooms 3,848,700 (1-3.2026); Neve Raskov, Alon, Kiryat Yearim, Neve Gan, Neve Magen not in the official file",
  note="2023 all-rooms averages with deal counts, presented as the neighbourhood level")
C("tr@12176", "הדר | נבדקו כ-2.7 עד 3.8 מיליון ש״ח בחלק מהמקורות", "sale_nb", "UNSOURCED", f"edit {e7}", rooms="all", figures=2,
  official="Hadar 3 rooms 3,664,500, 4 rooms 3,872,200, 5 rooms 4,631,300 (1-3.2026)", note="no date, no named source, no room count")
C("tr@14231..15452", "טבלת שכירות חודשית שנצפתה לפי סוג נכס (6 שורות) ופער של 1,350 ש״ח", "rent", "UNSOURCED",
  "keep (observed rent, public market data read 5.6.2026, page checked 5.6.2026)", figures=12, note="the page never says listings; weakest kept source")
C("tr@17047..18732", "7 עסקאות עם כתובת ותאריך (16.04-18.05.2026), 3.2 עד 10.16 מיליון ש״ח, מחיר למ״ר", "deal", "UNSOURCED",
  "keep (individual dated deals with address)", figures=14)
C("p@19030", "מ-31,724 ועד 79,976 ש״ח למ״ר בדוגמאות שנבדקו", "per_m2", "UNSOURCED", "keep (computed from the dated deals above)", figures=2)
C("p@19670", "צורך בשיפוץ של 250,000 עד 600,000 ש״ח", "other", "UNSOURCED", f"edit {e8}", figures=2, note="renovation cost, no source (tier 2)")
C("tr@20481", "חדשה: 3 חדרים סביב 3.35 עד 3.9 מיליון, 5 חדרים עד 6.7 מיליון ואף יותר", "sale_new_used", "CONSISTENT", "keep (contains the official medians)",
  rooms="3,5", official="3,544,800 / 4,663,600", figures=3)
C("tr@20481", "יד שנייה: 3 חדרים סביב 2.75 עד 3.49 מיליון ש״ח", "sale_new_used", "CONFLICT", f"edit {e9}", rooms=3, official="3,544,800", figures=2)
C("tr@20481", "יד שנייה: 5 חדרים סביב 4.55 עד 5.85 מיליון ש״ח", "sale_new_used", "CONSISTENT", f"edit {e9}", rooms=5, official="4,663,600", figures=2,
  note="same cell as the 3-room conflict; dropped with it")
C("li@23777", "פער של 200,000 עד 700,000 ש״ח בעלויות שיפוץ", "other", "UNSOURCED", f"edit {e10}", figures=2, note="renovation cost, no source (tier 2)")
C("p@29362", "FAQ: 3 חדרים 2.8 עד 3.4 מיליון ביד שנייה", "sale_new_used", "CONFLICT", f"edit {e12}", rooms=3, official="3,544,800", figures=2)
C("p@29362", "FAQ: 3 חדרים חדשות 3.35 עד 3.9 מיליון", "sale_new_used", "CONSISTENT", f"edit {e12}", rooms=3, official="3,544,800", figures=2, note="kept")
C("p@29637", "FAQ: 4 חדרים כ-3.3 עד 4.6 מיליון", "sale", "CONSISTENT", f"edit {e13}", rooms=4, official="3,809,600", figures=2, note="kept")
C("p@29637", "FAQ: 4 חדרים חדשות עד כ-5 מיליון ואף יותר", "sale_new_used", "CONFLICT", f"edit {e13}", rooms=4, official="3,809,600")
C("p@29637", "FAQ: עסקאות 4 חדרים ב-3.2, 4.6 ו-4.77 מיליון", "deal", "UNSOURCED", f"edit {e13}", rooms=4, figures=3,
  note="the dated deals of the deals table; kept, months added")
C("p@29974", "FAQ: 5 חדרים 4.5 עד 5.9 מיליון ביד שנייה", "sale_new_used", "CONSISTENT", f"edit {e14}", rooms=5, official="4,663,600", figures=2, note="range kept")
C("p@29974", "FAQ: 5 חדרים חדשות 5.4 עד 6.7 מיליון", "sale_new_used", "CONFLICT", f"edit {e14}", rooms=5, official="4,663,600", figures=2)
C("p@30240", "FAQ: ממוצעים סביב 3.97 עד 4.15 מיליון ש״ח לדירה (05.06.2026)", "sale_avg", "CONFLICT", f"edit {e15}", rooms="all",
  official="4,212,500 (1-3.2026)", figures=2, note="just outside the 1% range tolerance")
C("p@30518", "FAQ: טווח של כ-40,000 עד 48,000 ש״ח למ״ר", "per_m2", "UNSOURCED", "keep (market checks, page checked 5.6.2026)", figures=2)
C("p@30518", "FAQ: 31,724 / 34,782 / 45,023 / 79,976 ש״ח למ״ר בדוגמאות", "per_m2", "UNSOURCED", "keep (from the dated deals)", figures=4)
C("p@31690", "FAQ שכירות: 9,500 במקור אחד, 11,750 ממוצע מבוקש, טווחים לפי חדרים", "rent", "UNSOURCED",
  "keep (dated public market data 5.6.2026, asking average)", figures=8)

P.write(notes=(
    "Not audited as claims (illustrations, not market statements): the 9,000 rent / 4.6M asking example (p@16043), the 4.5M price with "
    "1.8M / 1.1M equity example (p@22484), the 300,000 renovation example (tr@20804), the 4.9M ad / 3.8M old deal example (p@26992), the "
    "asking-vs-closing scenario table (tr@27533..28366: 4.25 / 4.10-4.25, 4.75 / 4.35-4.55, 3.55 / 3.25-3.45, 5.20 / 5.00-5.20, 7.50; no room "
    "counts), the 4.6M if-example (p@28956). Remaining SUSPECTs after the edits: p@24366 is an explicit example ('לדוגמה', edit 11); the "
    "deals-table row רד״ק 9 (16.04.2026, 3.2M) is an individual dated deal; the FAQ 4-room sales 3.2 / 4.6 / 4.77M are the individual deals "
    "dated April-May 2026 in the deals table. In the neighbourhood table, the Hadar check note said 'the figure' and now says 'the comparison "
    "deal' (the figure left the table). Kept consistent ranges: the lead "
    "(3, 4, 5 rooms), the 'other source' new-flat ranges (p@5321) and the new-flat cell of the new-vs-second-hand table. Official quirks: the "
    "3-room series is sparse (published for 4 of 8 quarters) and jumps from 2,564,400 (7-9.2025) to 3,544,800 (1-3.2026), +16.4% on the "
    "year; the all-rooms median jumped from 3,395,600 (10-12.2025) to 4,212,500. The official file has only two neighbourhoods (Hadar, "
    "Morasha), so the neighbourhood table keeps its qualitative columns without numbers; its relative wording (Alon 'גבוה יותר ממורשה', "
    "Neve Gan 'רמת מחיר גבוהה') came from the removed 2023 averages and is not backed by official data. Rent and per-m2 figures are kept "
    "because the page dates its sources (05.06.2026) and calls them public market data / observed rent; it never says listings. The rent "
    "column of the rooms table duplicated the rent table and leaves with the table rewrite. The JSON-LD script and the closing disclaimer "
    "are outside the audit and unchanged."))
