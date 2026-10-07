# -*- coding: utf-8 -*-
"""Raanana (page 167): body alignment with the official price list (1-3.2026). Built on the gold example b_ashkelon.py."""
from mk import Page

P = Page("raanana-apartment-prices")

# ---------------- edits ----------------
# 1. the last sentence before the rooms table
old1 = "לכן הטבלה הבאה מציגה טווחי עבודה ולא מחירון סופי."
new1 = ("לכן הטבלה הבאה מציגה את חציון מחיר העסקה לפי נתוני רשות המסים לרבעון הראשון של 2026, לצד מחירי ייחוס ממקורות השוק, "
        "ולא מחירון סופי לדירה מסוימת. המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2-2.5 חדרים ודירות 6 חדרים ומעלה כדאי "
        "לבדוק מול עסקאות דומות ברחוב ובשכונה.")
e1 = P.edit(old1, new1, ["data_quarter"], "WORDING", "Follows edit 2: the 'common price range' column becomes the official median.", kept=["2.5"])

# 2. the rooms table: the 'common price range' column becomes the official median
new2 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">מספר חדרים</th>
<th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>
<th dir="rtl">מחיר ייחוס לפי מקורות שוק</th>
<th dir="rtl">דגשים לפני השוואה</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">2-2.5 חדרים</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">משתנה מאוד לפי מיקום, בניין ושטח</td>
<td dir="rtl">מתאים לרווקים, זוגות, הורים לילדים בעיר או משפרי דיור שמחפשים דירה קטנה</td>
</tr>
<tr dir="rtl">
<td dir="rtl">3 חדרים</td>
<td dir="rtl">2,814,000 ₪</td>
<td dir="rtl">כ-2.8 מיליון ₪ בדיווחי שוק מסוימים, ודירות חדשות סביב 2.556-3.2 מיליון ₪</td>
<td dir="rtl">יש לבדוק אם מדובר בדירה חדשה, משופצת או דירה ותיקה ללא מעלית</td>
</tr>
<tr dir="rtl">
<td dir="rtl">4 חדרים</td>
<td dir="rtl">3,289,900 ₪</td>
<td dir="rtl">כ-3.3-3.5 מיליון ₪, עם דוגמה סביב 3,310,000 ₪ ברחוב יאיר שטרן 15</td>
<td dir="rtl">הביקוש המשפחתי חזק, ולכן תכנון, חניה וממ"ד משנים את המחיר</td>
</tr>
<tr dir="rtl">
<td dir="rtl">5 חדרים</td>
<td dir="rtl">4,199,400 ₪</td>
<td dir="rtl">כ-3.6-4.2 מיליון ₪, עם דוגמאות סביב 3,395,000 ₪ ו-3,600,000 ₪</td>
<td dir="rtl">הפער בין דירה רגילה לדירה חדשה, גדולה או מיוחדת יכול להגיע למאות אלפי ₪</td>
</tr>
<tr dir="rtl">
<td dir="rtl">6 חדרים ומעלה</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">אין מחיר אחיד, תלוי בבית, דופלקס, פנטהאוז או דירה גדולה</td>
<td dir="rtl">צריך להשוות לנכסים דומים מאוד, לא לממוצע עירוני</td>
</tr>
</tbody>
</table>"""
e2 = P.table('<th dir="rtl">טווח מחיר נפוץ</th>', new2, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest"], "UNSOURCED",
             "Rooms table: the 'common price range' column gave 2-2.5 rooms 2.0-2.7M and 6+ rooms 4.5M+ with no source of any kind; its 3/4/5-room "
             "ranges (2.6-3.2M, 3.1-3.7M, 3.5-4.4M) were consistent with the official medians but differed from the page's other ranges. The column "
             "becomes the official median (1-3.2026, 'לא פורסם' for 2-2.5 and 6+ rooms). The market-reference column and the notes are kept word "
             "for word.")

# 3. renovation cost range in the 3-room paragraph (tier 2)
old3 = ("דירה חדשה כוללת לעיתים מפרט, חניה, ממ\"ד, מרפסת ותכנון עדכני, בעוד דירה ותיקה עשויה לדרוש שיפוץ של 150,000-400,000 ₪, "
        "החלפת תשתיות, התאמת מטבח וריצוף, או שיפור בידוד.")
new3 = ("דירה חדשה כוללת לעיתים מפרט, חניה, ממ\"ד, מרפסת ותכנון עדכני, בעוד דירה ותיקה עשויה לדרוש שיפוץ, החלפת תשתיות, התאמת "
        "מטבח וריצוף, או שיפור בידוד.")
e3 = P.edit(old3, new3, ["page"], "UNSOURCED", "Renovation cost range 150,000-400,000 with no source and no date; rephrased without the number.", tier=2)

# 4. renovation cost cell in the new-vs-second-hand table (tier 2)
old4 = "עשוי להגיע ל-150,000-500,000 ₪ ואף יותר"
new4 = "עשוי לדרוש השקעה משמעותית"
e4 = P.edit(old4, new4, ["page"], "UNSOURCED", "Renovation cost range 150,000-500,000 with no source and no date; rephrased without the number.", tier=2)

# ---------------- claims inventory ----------------
C = P.claim
K5 = "keep (market reading dated 05.06.2026)"
C("p@4285", "סביב כ-3.7 מיליון ₪ לדירה ממוצעת", "sale_avg", "CONSISTENT", K5, rooms="all", official="rooms.all 3,567,200 (+3.7%)")
C("p@4285", "כ-2.6-3.2 מיליון ₪ לדירות 3 חדרים", "sale", "CONSISTENT", K5, rooms=3, official="2,814,000 (1-3.2026)")
C("p@4285", "כ-3.3-3.5 מיליון ₪ לדירות 4 חדרים", "sale", "CONSISTENT", K5, rooms=4, official="3,289,900 (1-3.2026)", note="inside the 1% tolerance of the floor")
C("p@4285", "וכ-3.6-4.2 מיליון ₪ לדירות 5 חדרים", "sale", "CONSISTENT", K5, rooms=5, official="4,199,400 (1-3.2026)")
C("p@4285", "מחיר למ\"ר במקורות השוק סביב כ-31,000-35,000 ₪", "per_m2", "UNSOURCED", K5, figures=2)
C("p@4921", "דירות 3 חדרים סביב כ-2.8 מיליון ₪", "sale", "CONSISTENT", K5, rooms=3, official="2,814,000 (-0.5%)")
C("p@4921", "דירות 4 חדרים סביב כ-3.3-3.5 מיליון ₪", "sale", "CONSISTENT", K5, rooms=4, official="3,289,900")
C("p@4921", "דירות 5 חדרים סביב כ-3.6-4.2 מיליון ₪", "sale", "CONSISTENT", K5, rooms=5, official="4,199,400")
C("tr@6649", "3 חדרים | כ-2.6-3.2 מיליון ₪, עם מרכז סביב כ-2.8 מיליון ₪", "sale", "CONSISTENT", "keep", rooms=3, official="2,814,000", figures=2)
C("tr@6896", "4 חדרים | כ-3.3-3.5 מיליון ₪", "sale", "CONSISTENT", "keep", rooms=4, official="3,289,900")
C("tr@7159", "5 חדרים | כ-3.6-4.2 מיליון ₪", "sale", "CONSISTENT", "keep", rooms=5, official="4,199,400")
C("p@7435", "אליעזר יפה 22 (5 חד') 3,600,000; יאיר שטרן 15 (4 חד') 3,310,000; עקיבא 9 (5 חד') 3,395,000", "deal", "UNSOURCED",
  "keep (individual deals read in the market, page checked 05.06.2026; the text itself says each deal date must be checked)", figures=3)
C("p@7844", "ממוצע עירוני של כ-3.7 מיליון ₪", "sale_avg", "CONSISTENT", K5, rooms="all", official="rooms.all 3,567,200 (+3.7%)")
C("tr@10678", "2-2.5 חדרים | כ-2.0-2.7 מיליון ₪", "sale", "UNSOURCED", f"edit {e2}", rooms=2, note="'common price range', no source of any kind")
C("tr@10911", "3 חדרים | טווח נפוץ כ-2.6-3.2 מיליון ₪", "sale", "CONSISTENT", f"edit {e2}", rooms=3, official="2,814,000", note="column replaced by the median")
C("tr@10911", "3 חדרים | כ-2.8 מיליון ₪ בדיווחי שוק; דירות חדשות סביב 2.556-3.2 מיליון ₪", "sale_new_used", "CONSISTENT",
  f"keep (market reports; carried into the table of edit {e2})", rooms=3, official="2,814,000", figures=2)
C("tr@11169", "4 חדרים | טווח נפוץ כ-3.1-3.7 מיליון ₪", "sale", "CONSISTENT", f"edit {e2}", rooms=4, official="3,289,900", note="column replaced by the median")
C("tr@11169", "4 חדרים | כ-3.3-3.5 מיליון ₪, דוגמה 3,310,000 ₪ ביאיר שטרן 15", "sale", "CONSISTENT", f"keep (carried into the table of edit {e2})",
  rooms=4, official="3,289,900", figures=2, note="3,310,000 is one deal")
C("tr@11416", "5 חדרים | טווח נפוץ כ-3.5-4.4 מיליון ₪", "sale", "CONSISTENT", f"edit {e2}", rooms=5, official="4,199,400", note="column replaced by the median")
C("tr@11416", "5 חדרים | כ-3.6-4.2 מיליון ₪, דוגמאות 3,395,000 ו-3,600,000 ₪", "sale", "CONSISTENT", f"keep (carried into the table of edit {e2})",
  rooms=5, official="4,199,400", figures=3, note="the two examples are single deals (SUSPECT in check.py)")
C("tr@11674", "6 חדרים ומעלה | כ-4.5 מיליון ₪ ומעלה", "sale", "UNSOURCED", f"edit {e2}", rooms=6, note="no source of any kind")
C("p@11929", "דירה ותיקה עשויה לדרוש שיפוץ של 150,000-400,000 ₪", "other", "UNSOURCED", f"edit {e3}", figures=1, note="tier 2")
C("p@12627", "דירות 5 חדרים שנמכרות סביב 3.6 מיליון ₪ ... מגיעות ל-4.2 מיליון ₪ ואף יותר", "sale", "CONSISTENT", "keep (range contains the official median)",
  rooms=5, official="4,199,400")
C("p@13404", "מרכז דרום: מחיר קנייה ממוצע סביב 3,684,253 ₪ (3.68 מיליון)", "sale_nb", "UNSOURCED",
  "keep (one market source, page checked 05.06.2026; all rooms; the official file has no 'מרכז דרום')", figures=1)
C("p@13404", "מרכז דרום: שכירות ממוצעת סביב 9,600 ₪", "rent", "UNSOURCED", "keep (market source, page checked 05.06.2026)")
C("tr@14212", "מרכז דרום | כ-3.68 מיליון ₪ בממוצע וכ-9,600 ₪ שכירות ממוצעת", "sale_nb", "UNSOURCED", "keep (same market source as p@13404)", figures=2)
C("p@16029", "דירות חדשות: כ-2.556 מיליון ₪ לדירות 3 חדרים מסוימות", "sale_new_used", "UNSOURCED",
  "keep (market reports, page checked 05.06.2026; labelled 'certain' flats, not the city level)", rooms=3, official="2,814,000")
C("p@16029", "דירות חדשות: 2.6-3.2 מיליון (3 חד'), 3.32 מיליון (4 חד'), 4.248 מיליון (5 חד')", "sale_new_used", "CONSISTENT",
  "keep (market reports, page checked 05.06.2026)", official="3=2,814,000 4=3,289,900 (+0.9%) 5=4,199,400 (+1.2%)", figures=3)
C("tr@17430", "שיפוץ | עשוי להגיע ל-150,000-500,000 ₪ ואף יותר", "other", "UNSOURCED", f"edit {e4}", note="tier 2")
C("p@19093", "דירת 5 חדרים חדשה מוצעת סביב 4.248 מיליון ₪", "sale_new_used", "CONSISTENT", "keep (same market reports)", rooms=5, official="4,199,400 (+1.2%)")
C("p@19513", "שכירות חציונית כ-8,000 ₪ (מאי 2026, 52 מודעות); 7,257 / 8,559 / 10,959; מרכז דרום 9,600", "rent", "UNSOURCED",
  "keep (dated May 2026 listings + market reports, page checked 05.06.2026)", figures=6)
C("tr@20632..21541", "טבלת שכירות: 8,000 (מאי 2026) / 7,257 / 8,559 / 10,959 / 9,600", "rent", "UNSOURCED", "keep (dated May 2026 + market reports)", figures=5)
C("p@22665", "אליעזר יפה 22 3,600,000; יאיר שטרן 15 3,310,000; עקיבא 9 3,395,000; בר אילן 2,783,384", "deal", "UNSOURCED",
  "keep (individual deal examples read in the market, page checked 05.06.2026)", figures=4)
C("p@29635", "FAQ: דירה ממוצעת סביב כ-3.7 מיליון ₪", "sale_avg", "CONSISTENT", K5, rooms="all", official="rooms.all 3,567,200 (+3.7%)")
C("p@29635", "FAQ: מחיר למ\"ר סביב כ-31,000-35,000 ₪", "per_m2", "UNSOURCED", K5, figures=2)
C("p@29969", "FAQ: 3 חדרים כ-2.6-3.2 מיליון ₪, סביב כ-2.8 מיליון ₪", "sale", "CONSISTENT", "keep", rooms=3, official="2,814,000", figures=2)
C("p@29969", "FAQ: דירות חדשות סביב 2.556 מיליון ₪ וגם 2.6-3.2 מיליון ₪", "sale_new_used", "UNSOURCED", "keep (market reports, page checked 05.06.2026)",
  rooms=3, official="2,814,000 (inside 2.6-3.2)", figures=2)
C("p@30326", "FAQ: 4 חדרים סביב כ-3.3-3.5 מיליון ₪; עסקה 3,310,000 ₪ ביאיר שטרן 15", "sale", "CONSISTENT", "keep", rooms=4, official="3,289,900", figures=2)
C("p@30646", "FAQ: 5 חדרים כ-3.6-4.2 מיליון ₪; דוגמאות 3,600,000 ו-3,395,000 ₪", "sale", "CONSISTENT", "keep (range consistent; the examples are single deals)",
  rooms=5, official="4,199,400", figures=3, note="the two examples show as SUSPECT in check.py")
C("p@32422", "FAQ: מחיר למ\"ר סביב 31,000-35,000 ₪", "per_m2", "UNSOURCED", K5, figures=2)
C("p@33460", "FAQ שכירות: 8,000 / 7,257 / 8,559 / 10,959 / 9,600", "rent", "UNSOURCED", "keep (dated May 2026 + market reports)", figures=5)

P.write(notes=(
    "Every city-level 3/4/5-room figure on this page is consistent with the official medians (the 4-room 3.3-3.5M sits at the 1% edge of "
    "3,289,900; the 3.7M city average is +3.7% from the all-deals median 3,567,200), so the lead, the quick-answer table and the FAQ stay as "
    "they are. The only tier-1 change is the main rooms table: its 'common price range' column (no source of any kind, with 2-2.5-room "
    "and 6+-room ranges the official data cannot support) becomes the official median column; the market-reference column stays. Edits "
    "3 and 4 (renovation cost ranges with no source) are tier 2. Not audited as claims (illustrations or explicit hypotheticals): 4,250,000 "
    "listing / 3,600,000 deal in p@5525, 31,000 vs 35,000 per m2 in p@8719, 2,850,000 in p@11929, 300,000 gap in p@16415, 3.32M in p@18402, "
    "the 3,350,000 / 300,000 / 3,650,000 / 3,600,000 example in p@18666, the 3,700,000 / 7,500-8,500 / 10,000-11,000 if-example in p@19931, "
    "200,000 in p@21775, 250,000 in tr@24155, the 3,300,000-3,500,000 / 3,950,000 example in p@25642, the 3,310,000 / 3,395,000 / "
    "3,600,000 / 250,000 / 3,850,000 example in p@26305, 3,500,000 in p@28405, 3,800,000 / 3,400,000-3,550,000 in p@30996, "
    "100,000-500,000 in p@33799. Remaining SUSPECT lines in check.py: the single-deal examples 3,395,000 and 3,600,000 for 5 rooms "
    "(the rooms table and FAQ p@30646; the same two deals as p@7435, read in the market on 05.06.2026, undated by the page itself) and "
    "the explicit if-example 3,700,000 in p@19931. "
    "'מרכז דרום' (a market-source area, all rooms) is kept: it is not clearly the official 'מרכז' (3=3,016,100, 4=3,137,100), so no "
    "official figure was put in its place. Official medians also exist for קריית דוד רמז, נווה זמר, קזן, לסטר/רבוצקי, לב הפארק and קריית "
    "שרת, which the page does not name; nothing was added for them."))
