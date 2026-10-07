# -*- coding: utf-8 -*-
"""Jerusalem (page 4575): body alignment with the official price list (1-3.2026). Data only, nothing applied."""
from mk import Page

P = Page("jerusalem-apartment-prices")

# ---------------- edits ----------------
# 1. 'average flat price about 2.9M' under the h3 'טווח עבודה למחיר דירה'
old1 = "לפי דפי נתוני שוק שנבדקו, מחיר דירה ממוצע בירושלים מופיע סביב 2.9 מיליון ש\"ח, אך זו נקודת פתיחה בלבד."
new1 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה בירושלים, בכל גדלי הדירות, היה 2,717,100 ש\"ח, "
        "אך זו נקודת פתיחה בלבד.")
e1 = P.edit(old1, new1, ["rooms.all.latest"], "CONFLICT",
            "City average 2.9M from market pages vs the official all-rooms median 2,717,100 (1-3.2026), 6.7% apart; restated as the official median.")

# 2. 'price ranges here are a market check' (the ranges leave the page)
old2 = "טווחי המחירים כאן הם בדיקת שוק ואינם שומה."
new2 = "המספרים כאן הם נקודות ייחוס ואינם שומה."
e2 = P.edit(old2, new2, ["data_quarter"], "WORDING", "Pointed at the working ranges replaced in edits 6 and 9.")

# 3-4. market-metrics table, the 'average flat price' row (two cells)
old3 = "מחיר דירה ממוצע בדפי שוק"
new3 = "חציון מחיר העסקה בעיר, ינואר-מרץ 2026"
e3 = P.edit(old3, new3, ["rooms.all.latest"], "CONFLICT", "Row label of the 2.9M city average; the row now carries the official all-rooms median (edit 4).")
old4 = "כ-2,900,000 ש\"ח"
new4 = "2,717,100 ש\"ח, לפי נתוני רשות המסים"
e4 = P.edit(old4, new4, ["rooms.all.latest"], "CONFLICT", "City average 2,900,000 vs the official all-rooms median 2,717,100 (1-3.2026).")

# 5. intro of the rooms table
old5 = "מחיר דירה בירושלים לפי מספר חדרים צריך להיקרא כטווח עבודה, לא כמחירון מחייב."
new5 = ("הטבלה הבאה מציגה את חציון מחיר העסקה בירושלים לפי מספר חדרים, לפי נתוני רשות המסים לרבעון הראשון של 2026, לצד החציון "
        "באותו רבעון שנה קודם לכן. החציון הוא נקודת ייחוס ולא מחירון מחייב. המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; "
        "דירות 2 חדרים, דירות 6 חדרים ומעלה ונכסי יוקרה כדאי לבדוק מול עסקאות דומות ברחוב ובשכונה.")
e5 = P.edit(old5, new5, ["rooms.3.latest", "rooms.3.year_ago", "data_quarter"], "WORDING",
            "Announced working ranges; the table now shows official medians (edit 6); the 2-room, 6-room and luxury rows leave the table.")

# 6. the rooms table
new6 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">סוג דירה</th>
<th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>
<th dir="rtl">ינואר-מרץ 2025</th>
<th dir="rtl">שינוי בשנה</th>
<th dir="rtl">שטח אופייני לבדיקה</th>
<th dir="rtl">איפה הפערים גדולים במיוחד</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">דירת 3 חדרים</td>
<td dir="rtl">2,376,700 ש"ח</td>
<td dir="rtl">2,308,400 ש"ח</td>
<td dir="rtl">עלייה של 3%</td>
<td dir="rtl">55-75 מ"ר</td>
<td dir="rtl">קריית היובל, גילה, פסגת זאב, קטמון, בית הכרם ומרכז העיר.</td>
</tr>
<tr dir="rtl">
<td dir="rtl">דירת 4 חדרים</td>
<td dir="rtl">2,882,400 ש"ח</td>
<td dir="rtl">3,195,500 ש"ח</td>
<td dir="rtl">ירידה של 9.8%</td>
<td dir="rtl">78-105 מ"ר</td>
<td dir="rtl">ארנונה, בקעה, תלפיות, רמות, הר חומה, רוממה ובית הכרם.</td>
</tr>
<tr dir="rtl">
<td dir="rtl">דירת 5 חדרים</td>
<td dir="rtl">3,934,400 ש"ח</td>
<td dir="rtl">4,229,500 ש"ח</td>
<td dir="rtl">ירידה של 7%</td>
<td dir="rtl">105-135 מ"ר</td>
<td dir="rtl">שכונות משפחתיות, דירות חדשות, בניינים עם חניה ומעלית.</td>
</tr>
</tbody>
</table>"""
e6 = P.table('<th dir="rtl">טווח מחיר עבודה בירושלים</th>', new6,
             ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct",
              "rooms.5.latest", "rooms.5.year_ago", "rooms.5.change_pct"], "UNSOURCED",
             "Rooms table of undated working ranges with no named source: the 3/4/5-room ranges hold the official medians (consistent) but the "
             "2-room, 6-room and luxury rows (1.35-2.35M, 4.2-8.5M, above 8.5M / 12M) have no source or date. Replaced by the official medians with "
             "the year-earlier quarter; the size column and the 'where the gaps are' column of rows 3-5 are kept word for word.")

# 7. 'one more room can mean 400,000 in one neighbourhood and over 1,200,000 in another'
old7 = "לכן אותה תוספת של חדר יכולה לייצר פער של 400,000 ש\"ח בשכונה אחת ויותר מ-1,200,000 ש\"ח בשכונה אחרת."
new7 = ("לכן אותה תוספת של חדר יכולה לייצר פער קטן יחסית בשכונה אחת ופער גדול בהרבה בשכונה אחרת. לפי נתוני רשות המסים לרבעון "
        "הראשון של 2026, בגילה חציון מחיר העסקה היה 1,929,200 ש\"ח לדירת 3 חדרים ו-2,470,800 ש\"ח לדירת 4 חדרים, ובקטמונים 2,719,100 ש\"ח "
        "לדירת 3 חדרים ו-4,109,700 ש\"ח לדירת 4 חדרים.")
e7 = P.edit(old7, new7, ["neighbourhoods[גילה].rooms.3", "neighbourhoods[גילה].rooms.4", "neighbourhoods[קטמונים].rooms.3",
                         "neighbourhoods[קטמונים].rooms.4"], "UNSOURCED",
            "Room-premium figures 400,000 / 1,200,000 with no source or period; the point is kept in words and shown with official "
            "neighbourhood medians (no computed differences).")

# 8. neighbourhood paragraph above the neighbourhood table
old8 = P.find("שכונה היא אחד מסנני המחיר החזקים בירושלים.", "וחלק ממעמד שכונתי שנוצר לאורך שנים.")
new8 = ("שכונה היא אחד מסנני המחיר החזקים בירושלים. יש פערים רחבים בין שכונות משפחתיות גדולות כמו פסגת זאב, גילה, רמות, קריית היובל "
        "והר חומה, לבין אזורים מרכזיים או יוקרתיים כמו מרכז העיר, רחביה, טלביה, מקור ברוך ובית הכרם. חלק מהפער נובע ממיקום, חלק מאופי "
        "הבנייה, חלק מהיקף דירות חדשות, וחלק ממעמד שכונתי שנוצר לאורך שנים. הטבלה הבאה מציגה את חציון מחיר העסקה לפי שכונה ומספר חדרים, "
        "לפי נתוני רשות המסים לרבעון הראשון של 2026.")
e8 = P.edit(old8, new8, ["data_quarter"], "WORDING",
            "Pointed at the market-page averages and the 'thousands of historical deals' column replaced in edit 9; now introduces the official table.")

# 9. neighbourhood table
new9 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">שכונה</th>
<th dir="rtl">3 חדרים</th>
<th dir="rtl">4 חדרים</th>
<th dir="rtl">5 חדרים</th>
<th dir="rtl">מה לבדוק לפני השוואה</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">פסגת זאב</td>
<td dir="rtl">1,754,200 ש"ח</td>
<td dir="rtl">1,666,200 ש"ח</td>
<td dir="rtl">2,826,000 ש"ח</td>
<td dir="rtl">רכבת קלה, קומה, חניה, גיל בניין, מרחק מציר ראשי.</td>
</tr>
<tr dir="rtl">
<td dir="rtl">גילה</td>
<td dir="rtl">1,929,200 ש"ח</td>
<td dir="rtl">2,470,800 ש"ח</td>
<td dir="rtl">3,336,600 ש"ח</td>
<td dir="rtl">בניין מדורג, נגישות, מעלית, נוף, חניה ושיפוץ.</td>
</tr>
<tr dir="rtl">
<td dir="rtl">רמות</td>
<td dir="rtl">2,553,100 ש"ח</td>
<td dir="rtl">3,368,600 ש"ח</td>
<td dir="rtl">4,144,300 ש"ח</td>
<td dir="rtl">רמות א, ב, ג, ד ואזורים חדשים יותר אינם זהים.</td>
</tr>
<tr dir="rtl">
<td dir="rtl">קריית היובל</td>
<td dir="rtl">2,323,100 ש"ח</td>
<td dir="rtl">3,514,800 ש"ח</td>
<td dir="rtl">4,279,700 ש"ח</td>
<td dir="rtl">התחדשות עירונית, קומה, מעלית, קרבה לעין כרם ולרכבת קלה.</td>
</tr>
<tr dir="rtl">
<td dir="rtl">נווה יעקב</td>
<td dir="rtl">2,083,400 ש"ח</td>
<td dir="rtl">2,637,800 ש"ח</td>
<td dir="rtl">3,182,300 ש"ח</td>
<td dir="rtl">ריחוק יחסי, תחבורה, בניין ותיק מול בנייה חדשה יותר.</td>
</tr>
<tr dir="rtl">
<td dir="rtl">הר חומה</td>
<td dir="rtl">2,201,700 ש"ח</td>
<td dir="rtl">2,568,100 ש"ח</td>
<td dir="rtl">3,350,000 ש"ח</td>
<td dir="rtl">דירות משפחתיות, חניה, מרפסות, נגישות ליציאה מהעיר.</td>
</tr>
<tr dir="rtl">
<td dir="rtl">קטמונים</td>
<td dir="rtl">2,719,100 ש"ח</td>
<td dir="rtl">4,109,700 ש"ח</td>
<td dir="rtl">5,662,200 ש"ח</td>
<td dir="rtl">הבדל בין רחובות, פינוי בינוי, בניינים ותיקים ושיפוץ.</td>
</tr>
<tr dir="rtl">
<td dir="rtl">בית הכרם</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">4,109,100 ש"ח</td>
<td dir="rtl">5,088,200 ש"ח</td>
<td dir="rtl">רחוב, קרבה לרכבת קלה, מוסדות חינוך, חניה ודירות גדולות.</td>
</tr>
</tbody>
</table>"""
e9 = P.table('<th dir="rtl">מחיר ממוצע או טווח הקשר שנבדק</th>', new9,
             ["neighbourhoods[פסגת זאב].rooms.3", "neighbourhoods[פסגת זאב].rooms.4", "neighbourhoods[פסגת זאב].rooms.5",
              "neighbourhoods[גילה].rooms.3", "neighbourhoods[גילה].rooms.4", "neighbourhoods[גילה].rooms.5",
              "neighbourhoods[רמות].rooms.3", "neighbourhoods[רמות].rooms.4", "neighbourhoods[רמות].rooms.5",
              "neighbourhoods[קרית היובל].rooms.3", "neighbourhoods[קרית היובל].rooms.4", "neighbourhoods[קרית היובל].rooms.5",
              "neighbourhoods[נווה יעקב].rooms.3", "neighbourhoods[נווה יעקב].rooms.4", "neighbourhoods[נווה יעקב].rooms.5",
              "neighbourhoods[חומת שמואל-הר חומה].rooms.3", "neighbourhoods[חומת שמואל-הר חומה].rooms.4",
              "neighbourhoods[חומת שמואל-הר חומה].rooms.5",
              "neighbourhoods[קטמונים].rooms.3", "neighbourhoods[קטמונים].rooms.4", "neighbourhoods[קטמונים].rooms.5",
              "neighbourhoods[בית הכרם].rooms.4", "neighbourhoods[בית הכרם].rooms.5"], "UNSOURCED",
             "Neighbourhood table: 12 all-rooms averages 'in market pages' over thousands of historical deals (no period; far below the official "
             "1-3.2026 medians, e.g. Gila 1,215,394 vs 1,929,200 for 3 rooms) and 7 undated 'working ranges' for central and luxury areas. "
             "Replaced by the official neighbourhood medians by rooms for the 8 neighbourhoods the official list covers; the check notes of those "
             "rows are kept word for word; the deal-count column leaves the table.")

# 10. after the neighbourhood table: the neighbourhoods that have no official median
old10 = "גם בתוך שכונה אחת קיימים הבדלים: רמות אינה נקודה אחת, קטמון אינה זהה לקטמונים, ותלפיות אינה תמיד זהה לארנונה."
new10 = (old10 + " לשכונות כמו מרכז העיר, רחביה, טלביה, בקעה, המושבה הגרמנית, ארנונה, תלפיות, נחלאות, מקור ברוך, רוממה וארמון הנציב "
         "המחירון שבעמוד אינו מציג חציון שכונתי, ולכן בהן ההשוואה נעשית מול עסקאות דומות ברחוב ובבניין.")
e10 = P.edit(old10, new10, ["data_quarter"], "WORDING",
             "Follows edit 9: the rows of central and luxury neighbourhoods (no official median) left the table; the reader is told how to check them.")

# 11-13. new vs second-hand table and the steps table: undated premium and renovation figures (tier 2)
old11 = "לעיתים גבוה ב-10%-25% ביחס לדירה ותיקה דומה"
new11 = "לעיתים גבוה יותר ביחס לדירה ותיקה דומה"
e11 = P.edit(old11, new11, ["page"], "UNSOURCED", "New-flat per-m2 premium 10%-25% with no source or date; kept in words.", tier=2)
old12 = "יכול להיות נמוך יותר, אך שיפוץ יכול להוסיף 150,000-600,000 ש\"ח"
new12 = "יכול להיות נמוך יותר, אך שיפוץ יכול להוסיף מאות אלפי ש\"ח"
e12 = P.edit(old12, new12, ["page"], "UNSOURCED", "Renovation cost 150,000-600,000 with no source or date; kept in words.", tier=2)
old13 = "התעלמות מעלויות שיפוץ של 150,000-600,000 ש\"ח."
new13 = "התעלמות מעלויות שיפוץ שיכולות להגיע למאות אלפי ש\"ח."
e13 = P.edit(old13, new13, ["page"], "UNSOURCED", "Same undated renovation range in the steps table; kept in words.", tier=2)

# 14-17. FAQ answers
old14 = "בבדיקת נתוני שוק גלויים מ-6 ביוני 2026 הופיע מחיר דירה ממוצע סביב 2.9 מיליון ש\"ח."
new14 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה בירושלים, בכל גדלי הדירות, היה 2,717,100 ש\"ח: 2,376,700 ש\"ח "
         "לדירת 3 חדרים, 2,882,400 ש\"ח לדירת 4 חדרים ו-3,934,400 ש\"ח לדירת 5 חדרים.")
e14 = P.edit(old14, new14, ["rooms.all.latest", "rooms.3.latest", "rooms.4.latest", "rooms.5.latest"], "CONFLICT",
             "FAQ average 2.9M (market pages, 6.6.2026) vs the official all-rooms median 2,717,100 (1-3.2026).")
old15 = "טווח עבודה זהיר לדירת 3 חדרים בירושלים הוא כ-1.75-3.05 מיליון ש\"ח, אך הטווח משתנה מאוד."
new15 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים בירושלים ברבעון הראשון של 2026 היה 2,376,700 ש\"ח, לעומת 2,308,400 ש\"ח "
         "שנה קודם לכן, אך המחיר משתנה מאוד לפי שכונה.")
e15 = P.edit(old15, new15, ["rooms.3.latest", "rooms.3.year_ago"], "CONSISTENT",
             "FAQ 3 rooms: the 1.75-3.05M working range holds the official 2,376,700 but the body table is now the official median; rewritten from the same facts.")
old16 = "דירת 4 חדרים בירושלים נעה בטווח עבודה של כ-2.25-4.25 מיליון ש\"ח ברבות מהבדיקות, אך דירה חדשה, דירה עם חניה וממ\"ד, או דירה בשכונה מבוקשת יכולה לחרוג כלפי מעלה."
new16 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים בירושלים ברבעון הראשון של 2026 היה 2,882,400 ש\"ח, לעומת 3,195,500 ש\"ח "
         "שנה קודם לכן. דירה חדשה, דירה עם חניה וממ\"ד, או דירה בשכונה מבוקשת יכולה להיות גבוהה מהחציון.")
e16 = P.edit(old16, new16, ["rooms.4.latest", "rooms.4.year_ago"], "CONSISTENT",
             "FAQ 4 rooms: the 2.25-4.25M range holds the official 2,882,400; rewritten from the same facts as the body.")
old17 = "דירת 5 חדרים בירושלים נעה לעיתים סביב 2.85-5.75 מיליון ש\"ח, ובאזורים יקרים או בדירות חדשות יכולה להגיע מעבר לכך."
new17 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 5 חדרים בירושלים ברבעון הראשון של 2026 היה 3,934,400 ש\"ח, לעומת 4,229,500 ש\"ח "
         "שנה קודם לכן. באזורים יקרים או בדירות חדשות המחיר יכול להיות גבוה בהרבה.")
e17 = P.edit(old17, new17, ["rooms.5.latest", "rooms.5.year_ago"], "CONSISTENT",
             "FAQ 5 rooms: the 2.85-5.75M range holds the official 3,934,400; rewritten from the same facts as the body.")

# ---------------- claims inventory ----------------
C = P.claim
C("p@4699", "בדיקות שכירות רבות ... סביב 5,500-8,500 ש\"ח לחודש", "rent", "UNSOURCED",
  "keep (rent checks of public market data, dated 6.6.2026 in the same paragraph)")
C("p@42332", "מחיר דירה ממוצע בירושלים מופיע סביב 2.9 מיליון ש\"ח", "sale_avg", "CONFLICT", f"edit {e1}", rooms="all",
  official="2,717,100 (1-3.2026)")
C("p@42617", "מחיר ממוצע למ\"ר סביב 39,700 ש\"ח", "per_m2", "UNSOURCED", "keep (public market indices, page checked 6.6.2026)")
C("p@42617", "שכירות מבוקשת ממוצעת סביב 7,100 ש\"ח", "rent", "UNSOURCED", "keep (asking rent from market indices, page checked 6.6.2026)")
C("tr@44251", "מחיר דירה ממוצע בדפי שוק | כ-2,900,000 ש\"ח", "sale_avg", "CONFLICT", f"edit {e4}", rooms="all", official="2,717,100 (1-3.2026)",
  note=f"label cell edit {e3}")
C("tr@44411", "מחיר ממוצע למ\"ר בדפי שוק | כ-39,726 ש\"ח למ\"ר", "per_m2", "UNSOURCED", "keep (market pages, page checked 6.6.2026)")
C("tr@44587", "שכירות מבוקשת ממוצעת בדפי שוק | כ-7,100 ש\"ח לחודש", "rent", "UNSOURCED", "keep (market pages, page checked 6.6.2026)")
C("tr@44774", "מדד שכירות חציוני שפורסם במאי 2026 | כ-6,200 ש\"ח על בסיס 361 מודעות", "rent", "UNSOURCED",
  "keep (listing sample, dated May 2026)", figures=2)
C("tr@44961", "היצע שכירות גלוי בדפי שוק | כ-3,150 מודעות", "count", "UNSOURCED", "keep (listing count, page checked 6.6.2026)")
C("tr@45811", "דירת 2 חדרים | כ-1.35-2.35 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e6}", rooms=2, note="no official 2-room series, no source")
C("tr@46008", "דירת 3 חדרים | כ-1.75-3.05 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e6}", rooms=3, official="2,376,700 (1-3.2026)",
  note="range holds the median; restated as the median when the table is replaced")
C("tr@46208", "דירת 4 חדרים | כ-2.25-4.25 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e6}", rooms=4, official="2,882,400 (1-3.2026)")
C("tr@46406", "דירת 5 חדרים | כ-2.85-5.75 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e6}", rooms=5, official="3,934,400 (1-3.2026)")
C("tr@46605", "דירת 6 חדרים או פנטהאוז רגיל | כ-4.2-8.5 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e6}", rooms=6)
C("tr@46825", "דירת יוקרה או נכס חריג | מעל 8.5 מיליון ש\"ח, ולעיתים מעל 12 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e6}", figures=2)
C("p@47090", "תוספת של חדר יכולה לייצר פער של 400,000 ש\"ח ... ויותר מ-1,200,000 ש\"ח", "other", "UNSOURCED", f"edit {e7}", figures=2,
  note="room premium by neighbourhood, no source or period")
C("tr@48600..50852", "ממוצעי שכונה בדפי שוק: פסגת זאב 1,362,695 ... רוממה 2,426,638 (12 שורות)", "sale_nb", "UNSOURCED", f"edit {e9}",
  rooms="all", figures=12, official="e.g. גילה 3 rooms 1,929,200, פסגת זאב 4 rooms 1,666,200 (1-3.2026)",
  note="all-rooms averages over thousands of historical deals (p@47982), no period; all far below the current official medians")
C("tr@48600..50852", "מספר עסקאות גלוי בדפי שוק: 9,003 ... 3,475 (12 שורות)", "count", "UNSOURCED", f"edit {e9}", figures=12,
  note="historical deal counts, no period; the column leaves the table")
C("tr@51056..52320", "טווחי עבודה: ארנונה 2.6-5.8, בקעה 3.0-7.5, המושבה הגרמנית 4.0-10.0, רחביה 3.6-9.5, טלביה 4.5-12.0, נחלאות 2.2-5.8, "
  "ארמון הנציב 1.8-3.6 מיליון", "sale_nb", "UNSOURCED", f"edit {e9}", rooms="all", figures=7,
  note="no official median for these neighbourhoods; rows removed and named in edit 10")
C("p@52996", "חציון שכירות סביב מאי 2026 כ-6,200 ש\"ח (361 מודעות); ממוצע סביב 7,100 ש\"ח", "rent", "UNSOURCED",
  "keep (listing data, dated May 2026)", figures=3)
C("tr@53619..55358", "טבלת שכירות לפי שכונה: קריית היובל 5,684 ... רוממה 12,714 (12 שורות)", "rent", "UNSOURCED",
  "keep (listing data per p@52996, page checked 6.6.2026)", figures=13)
C("tr@56981", "הלמ\"ס 077/2026, 12.3.2026: כ-24,120 דירות נמכרו", "count", "UNSOURCED", "keep (CBS, dated)")
C("tr@57204", "37.6% דירות חדשות ו-62.4% יד שנייה", "other", "UNSOURCED", "keep (CBS, same dated release)", figures=2)
C("tr@57414..57785", "מחוז 660 / 1,450; עיר 522 / 1,007; 10,340 דירות חדשות שנותרו למכירה בינואר 2026", "count", "UNSOURCED",
  "keep (CBS, dated)", figures=5)
C("tr@57984", "בנק ישראל 25.5.2026: הריבית ירדה ב-0.25 נקודת אחוז ל-3.75%", "macro", "UNSOURCED", "keep (Bank of Israel, dated)", figures=2)
C("tr@58194", "מחירי הדירות עלו 0.3% בפברואר-מרץ וירדו 1.2% במונחים שנתיים", "macro", "UNSOURCED",
  "keep (Bank of Israel, dated; national index, not the city median)", figures=2)
C("tr@60481", "מחיר למ\"ר בדירה חדשה לעיתים גבוה ב-10%-25%", "sale_new_used", "UNSOURCED", f"edit {e11}", note="no source, no date")
C("tr@60481", "שיפוץ יכול להוסיף 150,000-600,000 ש\"ח", "other", "UNSOURCED", f"edit {e12}", note="renovation cost, no source")
C("tr@61402", "הלמ\"ס: כ-10,340 דירות חדשות שנותרו למכירה; 1,007 עסקאות יד שנייה", "count", "UNSOURCED", "keep (CBS, dated)", figures=2)
C("tr@65549", "עלויות שיפוץ של 150,000-600,000 ש\"ח", "other", "UNSOURCED", f"edit {e13}", note="renovation cost, no source")
C("p@67423", "FAQ: מחיר דירה ממוצע סביב 2.9 מיליון ש\"ח (6.6.2026)", "sale_avg", "CONFLICT", f"edit {e14}", rooms="all",
  official="2,717,100 (1-3.2026)")
C("p@67716", "FAQ: מחיר ממוצע למ\"ר סביב 39,726 ש\"ח בדפי שוק", "per_m2", "UNSOURCED", "keep (market pages, page checked 6.6.2026)")
C("p@68023", "FAQ: דירת 3 חדרים כ-1.75-3.05 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e15}", rooms=3, official="2,376,700 (1-3.2026)")
C("p@68277", "FAQ: דירת 4 חדרים כ-2.25-4.25 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e16}", rooms=4, official="2,882,400 (1-3.2026)")
C("p@68550", "FAQ: דירת 5 חדרים כ-2.85-5.75 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e17}", rooms=5, official="3,934,400 (1-3.2026)")

P.write(notes=(
    "No figure in the body conflicted per room count: the 3/4/5-room working ranges are wide enough to hold the official medians. The real "
    "conflicts are the city average 2.9M (three places) against the official all-rooms median 2,717,100, and the neighbourhood table: 12 "
    "all-rooms averages over thousands of historical deals (e.g. Gila 1,215,394, Neve Yaakov 1,144,649) sit far below the official 1-3.2026 "
    "medians by rooms and would contradict the price list directly below the lead. The rooms table and the 3/4/5 FAQ answers are rewritten "
    "to the official medians so the body says the same thing as the list (verdict CONSISTENT on those edits). "
    "Not audited as claims (illustrations or method, not market statements): the per-m2 arithmetic examples 3,200,000/80 and 2,100,000/70 "
    "(p@58456), the 'example deal check' table 2.4M / 3.6M / 5.2M / 1.85M (tr@59069..59593), the offer / listing examples 2,720,000 / "
    "2,850,000 / 3,150,000 / 3,300,000 (p@66081), the 15% size tolerance (tr@65038), months to delivery 12-48 / 3-9 (tr@61176), counts of "
    "comparables 3-6 / 5-10, flat sizes in m2, and the population row 1,078,424 (tr@44054, not a price). "
    "Rent, per-m2, listing counts, CBS and Bank of Israel figures are outside the official list and are kept where the page names the kind "
    "of source and dates it (6.6.2026 check date, May 2026, CBS 12.3.2026, BoI 25.5.2026). The 5,500-8,500 rent range in the lead is kept "
    "as a dated rent-check summary; it is consistent with the dated listing table further down (5,684-9,442). "
    "Name mapping: 'הר חומה' in the text = official 'חומת שמואל-הר חומה'; 'קריית היובל' = official 'קרית היובל'; 'קטמונים' kept as the "
    "official name (the rent table's 'קטמון א-ו' and 'קטמון הישנה' are left untouched). Official quirk: in Pisgat Zeev the 3-room median "
    "(1,754,200) is above the 4-room median (1,666,200) in 1-3.2026; shown as published. The 4-room city median fell 9.8% in a year "
    "(3,256,800 in 10-12.2025 to 2,882,400). The rooms table keeps the page's size column as a sixth column; it may need horizontal scroll "
    "on phones. Headings 'טווח עבודה למחיר דירה' and 'מדד שוק שנבדק | ערך עבודה' are kept (no number)."))
