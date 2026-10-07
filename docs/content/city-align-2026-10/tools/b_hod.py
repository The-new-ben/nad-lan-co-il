# -*- coding: utf-8 -*-
"""Hod Hasharon (page 4558): body alignment with the official price list (1-3.2026). Data only, nothing applied."""
from mk import Page

P = Page("hod-hasharon-apartment-prices")

# ---------------- edits ----------------
# 1. 'the numbers on this page are working ranges'
old1 = "המספרים בעמוד הם טווחי עבודה לבדיקת שוק, ולא שומה."
new1 = "המספרים בעמוד הם נקודות ייחוס לבדיקת שוק, ולא שומה."
e1 = P.edit(old1, new1, ["data_quarter"], "WORDING", "Pointed at the working ranges replaced by the official medians in edit 5.")

# 2-3. market-metrics table, the 'average flat price' row (two cells)
old2 = "מחיר דירה ממוצע לפי דפי נתוני שוק"
new2 = "חציון מחיר העסקה בעיר, ינואר-מרץ 2026"
e2 = P.edit(old2, new2, ["rooms.all.latest"], "CONFLICT", "Row label of the 3.52-3.66M city average; the row now carries the official all-rooms median (edit 3).")
old3 = "כ-3,520,000-3,657,246 ש\"ח"
new3 = "3,149,300 ש\"ח, לפי נתוני רשות המסים"
e3 = P.edit(old3, new3, ["rooms.all.latest"], "CONFLICT", "City average 3,520,000-3,657,246 vs the official all-rooms median 3,149,300 (1-3.2026).")

# 4. intro of the rooms table
old4 = "לכן הטבלה הבאה מציגה טווחי עבודה בלבד."
new4 = ("לכן הטבלה הבאה מציגה את חציון מחיר העסקה בהוד השרון לפי מספר חדרים, לפי נתוני רשות המסים לרבעון הראשון של 2026, לצד "
        "החציון באותו רבעון שנה קודם לכן. המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים, דירות 6 חדרים ומעלה "
        "ובתים פרטיים כדאי לבדוק מול עסקאות דומות ברחוב ובשכונה.")
e4 = P.edit(old4, new4, ["rooms.3.latest", "rooms.3.year_ago", "data_quarter"], "WORDING",
            "Announced working ranges; the table now shows the official medians (edit 5); the 2-room, 6-room, 6+ and private-house rows leave the table.")

# 5. the rooms table
new5 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">סוג דירה</th>
<th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>
<th dir="rtl">ינואר-מרץ 2025</th>
<th dir="rtl">שינוי בשנה</th>
<th dir="rtl">הערת בדיקה</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">3 חדרים</td>
<td dir="rtl">2,647,000 ש"ח</td>
<td dir="rtl">2,633,900 ש"ח</td>
<td dir="rtl">עלייה של 0.5%</td>
<td dir="rtl">עסקאות טובות נבדקות לפי שטח ומצב בניין, לא רק לפי חדרים</td>
</tr>
<tr dir="rtl">
<td dir="rtl">4 חדרים</td>
<td dir="rtl">3,264,800 ש"ח</td>
<td dir="rtl">3,338,700 ש"ח</td>
<td dir="rtl">ירידה של 2.2%</td>
<td dir="rtl">הפער בין ותיק לחדש יכול להיות מאות אלפי שקלים</td>
</tr>
<tr dir="rtl">
<td dir="rtl">5 חדרים</td>
<td dir="rtl">4,245,600 ש"ח</td>
<td dir="rtl">4,409,000 ש"ח</td>
<td dir="rtl">ירידה של 3.7%</td>
<td dir="rtl">בדירה משפחתית יש משקל גבוה לחניה, מרפסת, מחסן וממ"ד</td>
</tr>
</tbody>
</table>"""
e5 = P.table('<th dir="rtl">טווח מחיר חדשה או חדשה יחסית</th>', new5,
             ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct",
              "rooms.5.latest", "rooms.5.year_ago", "rooms.5.change_pct"], "UNSOURCED",
             "Rooms table of working ranges: the 3/4/5-room second-hand and new ranges all hold the official medians (consistent), but the 2-room, "
             "6-room, 6+ and private-house rows (1.7-2.3M, 4.17-4.75M, 5.35-7.15M, 6.5M+) are working ranges with no named source. Replaced by "
             "the official medians with the year-earlier quarter; the check notes of rows 3-5 are kept word for word. The rent column repeats "
             "the rent table further down, which stays; the new / second-hand ranges stay in the new-vs-second-hand table.")

# 6. 'a working range is not a valuation: 5 rooms within 3.9-4.5M'
old6a = "טווח עבודה אינו שומה:"
new6a = "החציון אינו שומה:"
e6a = P.edit(old6a, new6a, ["data_quarter"], "WORDING", "Bold label of the note below; the working ranges left the page (edit 5).")
old6 = "גם כאשר דירת 5 חדרים נראית בתוך טווח של 3.9-4.5 מיליון ש\"ח,"
new6 = "גם כאשר דירת 5 חדרים מוצעת במחיר קרוב לחציון העירוני, 4,245,600 ש\"ח ברבעון הראשון של 2026,"
e6 = P.edit(old6, new6, ["rooms.5.latest"], "CONSISTENT",
            "The 3.9-4.5M 5-room working range holds the official 4,245,600 but pointed at the ranges removed in edit 5; restated with the median.")

# 7. neighbourhood paragraph above the neighbourhood table
old7 = "חלק מהאזורים ותיקים יותר, חלקם מזוהים עם בנייה חדשה יותר, וחלקם נהנים מביקוש משפחתי גבוה בשל אופי הרחובות, מוסדות חינוך, גישה לצירי תנועה, פארקים ומרכזים מסחריים."
new7 = (old7 + " הטבלה הבאה מציגה את חציון מחיר העסקה לפי שכונה ומספר חדרים, לפי נתוני רשות המסים לרבעון הראשון של 2026. לרמתיים, "
        "רמות מנחם, גיל עמל וגרינברג אין חציון שכונתי במחירון הרשמי, ולכן בהן ההשוואה נעשית מול עסקאות דומות ברחוב ובבניין.")
e7 = P.edit(old7, new7, ["data_quarter"], "WORDING",
            "Introduces the official neighbourhood table (edit 9) and names the neighbourhoods that have no official median.")

# 8. neighbourhood table (2023 sample averages)
new8 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">שכונה או מתחם</th>
<th dir="rtl">3 חדרים</th>
<th dir="rtl">4 חדרים</th>
<th dir="rtl">5 חדרים</th>
<th dir="rtl">איך לקרוא את הנתון</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">מגדיאל</td>
<td dir="rtl">2,735,000 ש"ח</td>
<td dir="rtl">3,048,600 ש"ח</td>
<td dir="rtl">3,733,800 ש"ח</td>
<td dir="rtl">אזור מרכזי להשוואה, אך יש פערים בין בניינים ותיקים לחדשים</td>
</tr>
<tr dir="rtl">
<td dir="rtl">מתחם 1200</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">4,225,600 ש"ח</td>
<td dir="rtl">מתחם מבוקש יותר למשפחות</td>
</tr>
<tr dir="rtl">
<td dir="rtl">הדר</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">3,151,300 ש"ח</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">טוב להשוואות נקודתיות, לא לקביעת מחיר אחיד לכל השכונה</td>
</tr>
<tr dir="rtl">
<td dir="rtl">מתחם 200</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">3,351,500 ש"ח</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">צריך לבדוק אם הדירה דומה בגודל, תכנון, חניה ומועד בנייה</td>
</tr>
</tbody>
</table>"""
e8 = P.table('<th dir="rtl">מספר עסקאות שנצפה במדגם מסוים</th>', new8,
             ["neighbourhoods[מגדיאל].rooms.3", "neighbourhoods[מגדיאל].rooms.4", "neighbourhoods[מגדיאל].rooms.5",
              "neighbourhoods[מתחם 1200].rooms.5", "neighbourhoods[הדר].rooms.4", "neighbourhoods[מתחם 200].rooms.4"], "STALE",
             "Neighbourhood table of all-rooms averages from a 2023 sample (3 to 106 deals per row) presented as the neighbourhood level. Replaced "
             "by the official 1-3.2026 medians by rooms for the four neighbourhoods the official list covers ('לא פורסם' where it has no median); "
             "the check notes are kept, trimmed for Mitcham 1200 (its 5-room median is close to the city's, so 'usually a higher price bar' is "
             "dropped); the deal-count column leaves the table.")

# 9. undated renovation range (tier 2)
old9 = "עם זאת, דירה ותיקה יכולה לדרוש שיפוץ של 150,000-400,000 ש\"ח, ולעיתים גם טיפול בצנרת, חשמל, איטום, מטבח ומיזוג."
new9 = "עם זאת, דירה ותיקה יכולה לדרוש שיפוץ בעלות של מאות אלפי ש\"ח, ולעיתים גם טיפול בצנרת, חשמל, איטום, מטבח ומיזוג."
e9 = P.edit(old9, new9, ["page"], "UNSOURCED", "Renovation cost 150,000-400,000 with no source or date; kept in words.", tier=2)

# 10. 'two flats in the same neighbourhood can differ by 300,000-700,000'
old10 = "שתי דירות באותה שכונה ובאותו מספר חדרים יכולות להימכר בפער של 300,000-700,000 ש\"ח, ולעיתים יותר, בגלל פרטים שמופיעים רק בבדיקה מעשית."
new10 = "שתי דירות באותה שכונה ובאותו מספר חדרים יכולות להימכר בפער של מאות אלפי ש\"ח, ולעיתים יותר, בגלל פרטים שמופיעים רק בבדיקה מעשית."
e10 = P.edit(old10, new10, ["page"], "UNSOURCED", "Price gap 300,000-700,000 between similar flats with no source or period; kept in words.")

# 11. renovation row in the factors table (tier 2)
old11 = "יכול לשנות מחיר ב-150,000-400,000 ש\"ח"
new11 = "יכול לשנות מחיר במאות אלפי ש\"ח"
e11 = P.edit(old11, new11, ["page"], "UNSOURCED", "Same undated renovation range in the factors table; kept in words.", tier=2)

# 12-17. FAQ answers
old12 = "בדפי נתוני שוק גלויים שנבדקו ב-5 ביוני 2026 הופיעו ממוצעים סביב 3,520,000-3,657,246 ש\"ח לדירה. זהו נתון עירוני כללי בלבד. בפועל, דירות רבות נבדקות סביב 3.0-4.6 מיליון ש\"ח, אך"
new12 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה בהוד השרון, בכל גדלי הדירות, היה 3,149,300 ש\"ח: 2,647,000 ש\"ח "
         "לדירת 3 חדרים, 3,264,800 ש\"ח לדירת 4 חדרים ו-4,245,600 ש\"ח לדירת 5 חדרים. זהו נתון עירוני כללי בלבד:")
e12 = P.edit(old12, new12, ["rooms.all.latest", "rooms.3.latest", "rooms.4.latest", "rooms.5.latest"], "CONFLICT",
             "FAQ average 3,520,000-3,657,246 (market pages, 5.6.2026) vs the official all-rooms median 3,149,300 (1-3.2026); the consistent "
             "3.0-4.6M sentence in the same answer is replaced by the room medians.")
old13 = "טווח העבודה לדירת 3 חדרים יד שנייה שנצפה נע סביב 2,250,000-2,690,000 ש\"ח, ובדירות חדשות או חדשות יחסית הופיעו טווחים של כ-2,500,000-3,200,000 ש\"ח."
new13 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים בהוד השרון ברבעון הראשון של 2026 היה 2,647,000 ש\"ח, לעומת 2,633,900 ש\"ח "
         "שנה קודם לכן. בבדיקות שוק נצפו טווחים של כ-2,250,000-2,690,000 ש\"ח ביד שנייה וכ-2,500,000-3,200,000 ש\"ח בדירות חדשות או חדשות יחסית.")
e13 = P.edit(old13, new13, ["rooms.3.latest", "rooms.3.year_ago", "page"], "CONSISTENT",
             "FAQ 3 rooms: both ranges hold the official 2,647,000; the answer now leads with the median, as the body table does.")
old14 = "דירות 4 חדרים הופיעו סביב 3,180,000-3,390,000 ש\"ח ביד שנייה, ובטווח של כ-3,200,000-3,700,000 ש\"ח בדירות חדשות לפי בדיקות שוק שונות."
new14 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים בהוד השרון ברבעון הראשון של 2026 היה 3,264,800 ש\"ח, לעומת 3,338,700 ש\"ח "
         "שנה קודם לכן. בבדיקות שוק נצפו טווחים של כ-3,180,000-3,390,000 ש\"ח ביד שנייה וכ-3,200,000-3,700,000 ש\"ח בדירות חדשות.")
e14 = P.edit(old14, new14, ["rooms.4.latest", "rooms.4.year_ago", "page"], "CONSISTENT",
             "FAQ 4 rooms: both ranges hold the official 3,264,800; the answer now leads with the median.")
old15 = "דירות 5 חדרים נצפו סביב 3,960,000-4,380,000 ש\"ח ביד שנייה, ובטווח של כ-3,800,000-4,500,000 ש\"ח בדירות חדשות או בפרויקטים מסוימים."
new15 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 5 חדרים בהוד השרון ברבעון הראשון של 2026 היה 4,245,600 ש\"ח, לעומת 4,409,000 ש\"ח "
         "שנה קודם לכן. בבדיקות שוק נצפו טווחים של כ-3,960,000-4,380,000 ש\"ח ביד שנייה וכ-3,800,000-4,500,000 ש\"ח בדירות חדשות או בפרויקטים מסוימים.")
e15 = P.edit(old15, new15, ["rooms.5.latest", "rooms.5.year_ago", "page"], "CONSISTENT",
             "FAQ 5 rooms: both ranges hold the official 4,245,600; the answer now leads with the median.")
old16 = "במדגם נתוני שוק מסוים משנת 2023 הופיע רמתיים סביב 2,960,000 ש\"ח בממוצע, ומתחם 1200 סביב 4,150,000 ש\"ח בממוצע."
new16 = ("המחירון הרשמי אינו מציג חציון שכונתי לרמתיים. במתחם 1200, לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 5 חדרים ברבעון הראשון "
         "של 2026 היה 4,225,600 ש\"ח.")
e16 = P.edit(old16, new16, ["neighbourhoods[מתחם 1200].rooms.5"], "STALE",
             "FAQ: 2023 sample averages for Ramatayim (2,960,000) and Mitcham 1200 (4,150,000) presented as the current comparison; replaced by "
             "the official Mitcham 1200 5-room median (no official median for Ramatayim).", kept=["1200"])
old17 = "מגדיאל הופיעה במדגם נתוני שוק עם 106 עסקאות וממוצע של כ-3,060,000 ש\"ח בשנת 2023."
new17 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה במגדיאל היה 2,735,000 ש\"ח לדירת 3 חדרים, 3,048,600 ש\"ח "
         "לדירת 4 חדרים ו-3,733,800 ש\"ח לדירת 5 חדרים.")
e17 = P.edit(old17, new17, ["neighbourhoods[מגדיאל].rooms.3", "neighbourhoods[מגדיאל].rooms.4", "neighbourhoods[מגדיאל].rooms.5"], "STALE",
             "FAQ: Magdiel 2023 sample average 3,060,000 (106 deals); replaced by the official Magdiel medians by rooms, 1-3.2026.")
old18 = "במדגם שנבדק הופיעו 51 עסקאות וממוצע של כ-4,150,000 ש\"ח."
new18 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 5 חדרים במתחם 1200 היה 4,225,600 ש\"ח, קרוב לחציון "
         "העירוני לדירת 5 חדרים, 4,245,600 ש\"ח.")
e18 = P.edit(old18, new18, ["neighbourhoods[מתחם 1200].rooms.5", "rooms.5.latest"], "STALE",
             "FAQ: Mitcham 1200 average 4,150,000 from the 2023 sample (51 deals); replaced by the official 5-room median, shown next to the "
             "city 5-room median so the 'more expensive' question is answered honestly.", kept=["1200"])

# 19. the two undated single-address rows in the deals table (tier 2)
old19 = P.table_html('<th dir="rtl">כתובת עסקה לדוגמה</th>')
i = old19.find('<tr dir="rtl">\n<td dir="rtl">אסירי ציון 19</td>')
j = old19.find("</tbody>")
assert i > 0 and j > i
new19 = old19[:i] + old19[j:]
assert "שדרות הנשיאים 42" not in new19 and "דרך רמתיים 108" in new19
e19 = P.table('<th dir="rtl">כתובת עסקה לדוגמה</th>', new19, ["page"], "UNSOURCED",
              "Two single-address prices (אסירי ציון 19 about 3,450,000; שדרות הנשיאים 42 about 3,650,000) with no deal date and no area, "
              "labelled only 'observed public market figure'; the rows leave the table. The three dated deals (May 2026) stay word for word.",
              tier=2)

# ---------------- claims inventory ----------------
C = P.claim
C("p@4371", "דירות רבות בעיר מופיעות סביב 3,000,000-4,600,000 ש\"ח", "sale_avg", "CONSISTENT", "keep (holds the official all-rooms median)",
  rooms="all", official="3,149,300 (1-3.2026)")
C("p@4371", "דירות חדשות, גדולות, גן, פנטהאוזים ... יכולים לעבור גם 4,800,000 ש\"ח ויותר", "sale", "UNSOURCED",
  "keep (premium segment, public market data dated 5.6.2026 in the same sentence)")
C("p@41118", "דירות רגילות נבדקות סביב 3.0-4.6 מיליון ש\"ח", "sale_avg", "CONSISTENT", "keep (holds the official all-rooms median)",
  rooms="all", official="3,149,300 (1-3.2026)")
C("p@41344", "דמי שכירות ממוצעים סביב 7,500-9,100 ש\"ח לדירות 4-5 חדרים", "rent", "UNSOURCED", "keep (market data pages, page checked 5.6.2026)")
C("tr@42467", "מחיר דירה ממוצע לפי דפי נתוני שוק | כ-3,520,000-3,657,246 ש\"ח", "sale_avg", "CONFLICT", f"edit {e3}", rooms="all",
  official="3,149,300 (1-3.2026)", note=f"label cell edit {e2}")
C("tr@42652", "מחיר למ\"ר ממוצע שנצפה | כ-30,000 ש\"ח למ\"ר", "per_m2", "UNSOURCED", "keep (market data pages, page checked 5.6.2026)")
C("tr@42815", "שכירות ממוצעת שנצפתה | כ-7,900-8,500 ש\"ח לחודש", "rent", "UNSOURCED", "keep (market data pages, page checked 5.6.2026)")
C("tr@42990", "דירות 4 חדרים יד שנייה | כ-3,180,000-3,242,000 ש\"ח", "sale", "CONSISTENT", "keep (holds the official median within tolerance)",
  rooms=4, official="3,264,800 (1-3.2026)")
C("tr@43155", "דירות 5 חדרים יד שנייה | כ-3,961,000-4,380,000 ש\"ח", "sale", "CONSISTENT", "keep", rooms=5, official="4,245,600 (1-3.2026)")
C("tr@44002", "2 חדרים | יד שנייה 1.7-2.3M | חדשה 1.7-2.0M", "sale", "UNSOURCED", f"edit {e5}", rooms=2, figures=2)
C("tr@44257", "3 חדרים | יד שנייה 2,250,000-2,690,000 | חדשה 2,500,000-3,200,000", "sale", "CONSISTENT", f"edit {e5}", rooms=3,
  official="2,647,000 (1-3.2026)", figures=2, note="both ranges hold the median; restated as the median when the table is replaced")
C("tr@44507", "4 חדרים | יד שנייה 3,180,000-3,390,000 | חדשה 3,200,000-3,700,000", "sale", "CONSISTENT", f"edit {e5}", rooms=4,
  official="3,264,800 (1-3.2026)", figures=2)
C("tr@44747", "5 חדרים | יד שנייה 3,960,000-4,380,000 | חדשה 3,800,000-4,500,000", "sale", "CONSISTENT", f"edit {e5}", rooms=5,
  official="4,245,600 (1-3.2026)", figures=2)
C("tr@44993..45498", "6 חדרים 4.17-4.75M / 5.17M+; 6+ 5.35-7.15M; בית פרטי 6.5M+", "sale", "UNSOURCED", f"edit {e5}", rooms=6, figures=4)
C("tr@44002..45498", "עמודת שכירות בטבלת החדרים (7 שורות)", "rent", "UNSOURCED", f"edit {e5}", figures=7,
  note="column removed with the table; the same rent figures stay in the rent table tr@50050..51101 (except the 9,000+ house row)")
C("p@46098", "דירת 5 חדרים נראית בתוך טווח של 3.9-4.5 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e6}", rooms=5, official="4,245,600 (1-3.2026)")
C("tr@47029..48462", "ממוצעי שכונה לפי מדגם 2023: מגדיאל 3,060,000 ... גרינברג 5,050,000 (8 שורות)", "sale_nb", "STALE", f"edit {e8}",
  rooms="all", figures=8, official="e.g. מגדיאל 4 rooms 3,048,600, מתחם 1200 5 rooms 4,225,600 (1-3.2026)")
C("tr@47029..48462", "מספר עסקאות במדגם: 106 ... 3 (8 שורות)", "count", "STALE", f"edit {e8}", figures=8, note="2023 sample sizes; column removed")
C("p@49431", "שכירות ממוצעת סביב 8,500; 3 חדרים 4,500-5,900; 4 חדרים 7,537-8,400; 5 חדרים 8,905-9,850", "rent", "UNSOURCED",
  "keep (market data pages, page checked 5.6.2026)", figures=4)
C("tr@50050..51101", "טבלת שכירות לפי חדרים (6 שורות)", "rent", "UNSOURCED", "keep (market data pages, page checked 5.6.2026)", figures=6)
C("p@52112", "עסקאות: מולדת 4 2,900,000; דרך רמתיים 108 2,300,000; אסירי ציון 11 3,490,000 (ומחיר למ\"ר)", "deal", "UNSOURCED",
  "keep (individual deals dated in the table, May 2026)", figures=6)
C("tr@52812..53307", "טבלת עסקאות מתוארכות (19.5, 17.5, 1.5.2026)", "deal", "UNSOURCED", "keep (individual dated deals)", figures=6)
C("tr@53566..53836", "אסירי ציון 19 כ-3,450,000; שדרות הנשיאים 42 כ-3,650,000 (ללא תאריך וללא שטח)", "deal", "UNSOURCED", f"edit {e19}",
  figures=2, note="tier 2: no deal date, no area")
C("p@54744", "דירה ותיקה יכולה לדרוש שיפוץ של 150,000-400,000 ש\"ח", "other", "UNSOURCED", f"edit {e9}", note="renovation cost, no source")
C("tr@55388", "מחיר 3 חדרים | חדשה 2,500,000-3,200,000 | יד שנייה 2,250,000-2,690,000", "sale_new_used", "CONSISTENT", "keep", rooms=3,
  official="2,647,000 (1-3.2026)", figures=2)
C("tr@55584", "מחיר 4 חדרים | חדשה 3,200,000-3,700,000 | יד שנייה 3,180,000-3,390,000", "sale_new_used", "CONSISTENT", "keep", rooms=4,
  official="3,264,800 (1-3.2026)", figures=2)
C("tr@55778", "מחיר 5 חדרים | חדשה 3,800,000-4,500,000 | יד שנייה 3,960,000-4,380,000", "sale_new_used", "CONSISTENT", "keep", rooms=5,
  official="4,245,600 (1-3.2026)", figures=2)
C("p@57112", "שתי דירות ... יכולות להימכר בפער של 300,000-700,000 ש\"ח", "other", "UNSOURCED", f"edit {e10}", note="no source or period")
C("tr@58396", "שיפוץ פנימי | יכול לשנות מחיר ב-150,000-400,000 ש\"ח", "other", "UNSOURCED", f"edit {e11}", note="renovation cost, no source")
C("p@62488", "FAQ: ממוצעים סביב 3,520,000-3,657,246 ש\"ח לדירה (5.6.2026)", "sale_avg", "CONFLICT", f"edit {e12}", rooms="all",
  official="3,149,300 (1-3.2026)")
C("p@62488", "FAQ: דירות רבות נבדקות סביב 3.0-4.6 מיליון ש\"ח", "sale_avg", "CONSISTENT", f"edit {e12}", rooms="all", official="3,149,300 (1-3.2026)")
C("p@62838", "FAQ: 3 חדרים יד שנייה 2,250,000-2,690,000; חדשות 2,500,000-3,200,000", "sale", "CONSISTENT", f"edit {e13}", rooms=3,
  official="2,647,000 (1-3.2026)", figures=2)
C("p@63121", "FAQ: 4 חדרים יד שנייה 3,180,000-3,390,000; חדשות 3,200,000-3,700,000", "sale", "CONSISTENT", f"edit {e14}", rooms=4,
  official="3,264,800 (1-3.2026)", figures=2)
C("p@63421", "FAQ: 5 חדרים יד שנייה 3,960,000-4,380,000; חדשות 3,800,000-4,500,000", "sale", "CONSISTENT", f"edit {e15}", rooms=5,
  official="4,245,600 (1-3.2026)", figures=2)
C("p@63707", "FAQ: מדגם 2023: רמתיים 2,960,000, מתחם 1200 4,150,000 בממוצע", "sale_nb", "STALE", f"edit {e16}", rooms="all", figures=2,
  official="מתחם 1200 5 rooms 4,225,600; no official median for רמתיים")
C("p@63997", "FAQ: מגדיאל 106 עסקאות, ממוצע כ-3,060,000 ש\"ח בשנת 2023", "sale_nb", "STALE", f"edit {e17}", rooms="all", figures=2,
  official="מגדיאל 2,735,000 / 3,048,600 / 3,733,800 (1-3.2026)")
C("p@64295", "FAQ: מתחם 1200, 51 עסקאות, ממוצע כ-4,150,000 ש\"ח", "sale_nb", "STALE", f"edit {e18}", rooms="all", figures=2,
  official="מתחם 1200 5 rooms 4,225,600 (1-3.2026)", note="the 2023 sample per the neighbourhood table")

P.write(notes=(
    "Every city-level 3/4/5-room figure on this page (second-hand and new ranges, the 3.0-4.6M 'regular flats' range, the 3.9-4.5M "
    "5-room range) holds the official 1-3.2026 medians. The conflicts are the city average 3,520,000-3,657,246 (metrics table and FAQ) "
    "against the official all-rooms median 3,149,300, and the STALE 2023 neighbourhood sample averages (table + three FAQ answers). "
    "The rooms table and the 3/4/5 FAQ answers are restated with the official medians (verdict CONSISTENT on those edits); the FAQ answers "
    "keep the page's own consistent second-hand / new ranges after the median. The new-vs-second-hand table (tr@55388..55778) is consistent "
    "and kept. Not audited as claims: the if-example 'מי שרואה דירת 4 חדרים ... במחיר של 3,490,000 ש\"ח' (p@45775, a hypothetical; it "
    "matches the dated Asirei Zion 11 deal), sizes in m2, months to delivery 12-36 / 30-180 days (tr@55997), counts of comparables "
    "(5-10, 10-20, 8-12), floors 3-5. Rent, per-m2 and the three dated May 2026 deals are kept (market data pages, page checked 5.6.2026). "
    "Unsure: (a) the two undated single-address rows (אסירי ציון 19, שדרות הנשיאים 42) are removed as tier 2; they could also be kept under "
    "the page check date; (b) the Mitcham 1200 check note is trimmed ('לרוב עם רף מחיר גבוה יותר' dropped) because its official 5-room "
    "median (4,225,600) is close to the city's (4,245,600); (c) the official neighbourhood 'שרת' (4 rooms 3,210,500, 5 rooms 4,014,000) is "
    "not added to the table because the page never names it and its natural name is not certain. Official quirk: the city 3-room median "
    "is published only for every other quarter (4-6.2024, 10-12.2024, 4-6.2025 and 10-12.2025 are empty), so it rests on few deals; the "
    "year-on-year change (+0.5%) compares 1-3.2026 with 1-3.2025 as published."))
