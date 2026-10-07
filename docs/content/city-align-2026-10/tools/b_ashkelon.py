# -*- coding: utf-8 -*-
"""Ashkelon (page 4593): body alignment with the official price list (1-3.2026). GOLD EXAMPLE for the other pages."""
from mk import Page

P = Page("ashkelon-apartment-prices")
Q = "ברבעון הראשון של 2026"

# ---------------- edits ----------------
# 1. the lead paragraph, directly above the price list
old1 = P.find("מחירי דירות באשקלון נעים כיום בטווח עבודה רחב:", "לא שומה ולא הערכת שווי מחייבת.")
new1 = ("מחירי דירות באשקלון, לפי נתוני רשות המסים לרבעון הראשון של 2026: חציון מחיר העסקה היה 918,100 ש\"ח לדירת 3 חדרים, "
        "1,405,800 ש\"ח לדירת 4 חדרים ו-1,891,000 ש\"ח לדירת 5 חדרים. דירות 6 חדרים, דירות חדשות, דירות גדולות, דירות עם נוף לים "
        "או נכסים באזורי פרמיה כמו מרינה, ברנע, אפרידר, אגמים ועיר היין יכולים להיות גבוהים יותר. בשכירות, נקודת האמצע העירונית "
        "במודעות עומדת סביב 3,500 ש\"ח בחודש, ובדירות גדולות או חדשות השכירות גבוהה יותר. המחיר המבוקש למ\"ר במודעות נע בערך בין "
        "10,900 ל-17,400 ש\"ח לפי גודל וסוג הנכס, ולכן אין מחיר אחד לעיר: צריך לפצל לפי חדרים, שכונה, קומה, חניה, ממ\"ד, מעלית, "
        "קרבה לים, גיל בניין ועסקאות אמת. החציון הוא נקודת ייחוס ולא שומה: דירה מסוימת יכולה להיות רחוקה ממנו בגלל הקומה, המצב, "
        "החניה והשכונה.")
e1 = P.edit(old1, new1, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
            "Lead above the list: 3 rooms 1.0-1.35M and 4 rooms 1.45-1.85M exclude the official medians 918,100 and 1,405,800 (1-3.2026); "
            "5 rooms 1.9-2.5M was consistent and is restated as the median. The undated 2-room range and the untraceable rent range "
            "2,300 / 5,000-5,800 are dropped; the 3,500 rent midpoint (dated listing source, 4.6.2026, same page) and the asking per-m2 "
            "range (listing data, page checked 6.6.2026) are kept and labelled as listing figures.")

# 2. intro of the rooms table
old2 = "הטבלה הבאה נותנת טווחי עבודה למחירי דירות באשקלון לפי מספר חדרים. היא משלבת דפוסי ביקוש, נתוני מודעות, דוגמאות עסקאות והיגיון שוק מקומי. הטווחים אינם מחליפים בדיקה פרטנית,"
new2 = ("הטבלה הבאה מציגה את חציון מחיר העסקה באשקלון לפי מספר חדרים, לפי נתוני רשות המסים לרבעון הראשון של 2026, לצד החציון "
        "באותו רבעון שנה קודם לכן. החציון אינו מחליף בדיקה פרטנית,")
e2 = P.edit(old2, new2, ["rooms.3.latest", "rooms.3.year_ago"], "CONFLICT",
            "The intro announced working ranges built from asking patterns; the table is replaced by official medians (edit 3).")

# 3. the rooms table
new3 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">סוג נכס</th>
<th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>
<th dir="rtl">ינואר-מרץ 2025</th>
<th dir="rtl">שינוי בשנה</th>
<th dir="rtl">הערת בדיקה</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">3 חדרים</td>
<td dir="rtl">918,100 ש"ח</td>
<td dir="rtl">1,156,700 ש"ח</td>
<td dir="rtl">ירידה של 20.6%</td>
<td dir="rtl">קטגוריה נפוצה להשוואה, אך יש פער בין ותיק, משופץ וחדש יחסית</td>
</tr>
<tr dir="rtl">
<td dir="rtl">4 חדרים</td>
<td dir="rtl">1,405,800 ש"ח</td>
<td dir="rtl">1,597,300 ש"ח</td>
<td dir="rtl">ירידה של 12%</td>
<td dir="rtl">קטגוריית משפחות מרכזית, מושפעת מחניה, ממ"ד, מרפסת ובית ספר קרוב</td>
</tr>
<tr dir="rtl">
<td dir="rtl">5 חדרים</td>
<td dir="rtl">1,891,000 ש"ח</td>
<td dir="rtl">2,142,600 ש"ח</td>
<td dir="rtl">ירידה של 11.7%</td>
<td dir="rtl">טווח רחב במיוחד באגמים, עיר היין, ברנע ומרינה</td>
</tr>
</tbody>
</table>"""
e3 = P.table('<th dir="rtl">עוגן ביקוש שנצפה</th>', new3,
             ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct",
              "rooms.5.latest", "rooms.5.year_ago", "rooms.5.change_pct"], "CONFLICT",
             "Rooms table: the 3- and 4-room working ranges and every asking anchor (1.2M, 1.69M, 2.2M) contradict the official medians; the 2-room "
             "and 6+-room rows and the per-m2 column have no named or dated source. Replaced by the official medians with the year-earlier quarter; "
             "the check notes of rows 3-5 are kept word for word.")

# 4. the sentence after the table pointed at the removed per-m2 column
old4 = "בטבלת המחירים בולטת תופעה רגילה: ככל שהדירה גדולה יותר, מחיר כולל עולה, אך מחיר למ\"ר יכול לרדת."
new4 = ("המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים ודירות 6 חדרים ומעלה כדאי לבדוק מול עסקאות דומות ברחוב "
        "ובשכונה. בשוק של אשקלון בולטת גם תופעה רגילה: ככל שהדירה גדולה יותר, המחיר הכולל עולה, אך המחיר למ\"ר יכול לרדת.")
e4 = P.edit(old4, new4, ["data_quarter"], "WORDING", "Follows edit 3: the per-m2 column and the 2 / 6+ rows left the table.")

# 5. the Afridar 'example in the style of market data'
old5 = "דוגמה בסגנון נתוני שוק הציגה באפרידר דירת 4 חדרים בשטח 100 מ\"ר שנמכרה ב-1,560,000 ש\"ח, כלומר כ-15,600 ש\"ח למ\"ר, בתאריך 10 באפריל 2025."
new5 = "באפרידר, למשל, חציון מחיר העסקה לדירת 4 חדרים ברבעון הראשון של 2026 היה 1,506,400 ש\"ח, לפי נתוני רשות המסים."
e5 = P.edit(old5, new5, ["neighbourhoods[אפרידר].rooms.4"], "UNSOURCED",
            "An 'example in the style of market data' from April 2025 with no named source; replaced by the official Afridar 4-room median (1-3.2026).")

# 6. street averages paragraph
old6 = P.find("גם טבלאות רחוב מועילות כמדד. למשל, נראו נתוני עסקאות רחוב", "ויוספטל כלל 30 עסקאות עם ממוצע של 934,416 ש\"ח.")
new6 = ("גם בדיקה לפי שכונה ולפי רחוב מועילה כמדד. לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 4 חדרים "
        "היה 1,055,300 ש\"ח בשכונת בן גוריון, 1,506,400 ש\"ח באפרידר ו-1,667,700 ש\"ח בשכונת האגמים.")
e6 = P.edit(old6, new6, ["neighbourhoods[בן גוריון].rooms.4", "neighbourhoods[אפרידר].rooms.4", "neighbourhoods[האגמים].rooms.4"], "UNSOURCED",
            "Street averages (74/46/44/30 deals) with no source, no period and no room count; replaced by official neighbourhood medians.")

# 7. street table
new7 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">שכונה</th>
<th dir="rtl">3 חדרים</th>
<th dir="rtl">4 חדרים</th>
<th dir="rtl">5 חדרים</th>
<th dir="rtl">מה לאמת</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">אפרידר</td>
<td dir="rtl">1,413,800 ש"ח</td>
<td dir="rtl">1,506,400 ש"ח</td>
<td dir="rtl">2,577,000 ש"ח</td>
<td dir="rtl">מצב בניין, קומה, מעלית, שיפוץ ורישום</td>
</tr>
<tr dir="rtl">
<td dir="rtl">נווה הדרים</td>
<td dir="rtl">1,299,600 ש"ח</td>
<td dir="rtl">1,560,400 ש"ח</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">שטחים, שנים, סוגי נכסים ופיזור מחירים</td>
</tr>
<tr dir="rtl">
<td dir="rtl">בן גוריון</td>
<td dir="rtl">961,600 ש"ח</td>
<td dir="rtl">1,055,300 ש"ח</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">האם העסקאות דומות לדירה הנבדקת או כוללות נכסים ישנים יותר</td>
</tr>
<tr dir="rtl">
<td dir="rtl">גני ברנע</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">1,455,100 ש"ח</td>
<td dir="rtl">1,758,900 ש"ח</td>
<td dir="rtl">שטח דירה, חניה, קומה ומצב הבניין</td>
</tr>
<tr dir="rtl">
<td dir="rtl">האגמים</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">1,667,700 ש"ח</td>
<td dir="rtl">1,805,000 ש"ח</td>
<td dir="rtl">סוגי דירות, דירות גדולות, בתים או נכסים מיוחדים</td>
</tr>
</tbody>
</table>"""
e7 = P.table('<th dir="rtl">מקור השוואה</th>', new7,
             ["neighbourhoods[אפרידר].rooms.3", "neighbourhoods[אפרידר].rooms.4", "neighbourhoods[אפרידר].rooms.5",
              "neighbourhoods[נווה הדרים].rooms.3", "neighbourhoods[נווה הדרים].rooms.4", "neighbourhoods[בן גוריון].rooms.3",
              "neighbourhoods[בן גוריון].rooms.4", "neighbourhoods[גני ברנע].rooms.4", "neighbourhoods[גני ברנע].rooms.5",
              "neighbourhoods[האגמים].rooms.4", "neighbourhoods[האגמים].rooms.5"], "UNSOURCED",
             "Street table (four street averages + the April 2025 Afridar example) without source or period; replaced by the official "
             "neighbourhood medians, 1-3.2026 ('לא פורסם' where the official file has no median). Check notes reused from the old rows.")

# 8. 'close to the city anchor for 4 rooms'
old8 = "בצד הקונה, אם דירה מבוקשת ב-1.69 מיליון ש\"ח, קרובה לעוגן העירוני לדירת 4 חדרים, אך אין לה חניה או ממ\"ד, ייתכן שנדרש תיקון מחיר."
new8 = ("בצד הקונה, אם דירת 4 חדרים מבוקשת ב-1.69 מיליון ש\"ח, מעל חציון מחיר העסקה העירוני לדירת 4 חדרים ברבעון הראשון של 2026 "
        "(1,405,800 ש\"ח), ואין לה חניה או ממ\"ד, ייתכן שנדרש תיקון מחיר.")
e8 = P.edit(old8, new8, ["rooms.4.latest", "page"], "CONFLICT", "Calls 1.69M the city anchor for 4 rooms; the official median is 1,405,800.")

# 9-11. FAQ answers
old9 = "דירת 3 חדרים באשקלון נעה לרוב סביב 1.0-1.35 מיליון ש\"ח כטווח עבודה, כאשר עוגני ביקוש מסוימים מצביעים סביב 1.2 מיליון ש\"ח וכ-15,789 ש\"ח למ\"ר."
new9 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים באשקלון ברבעון הראשון של 2026 היה 918,100 ש\"ח. ברבעון הרביעי של "
        "2025 הוא היה 1,142,100 ש\"ח, ולכן כדאי להשוות גם לעסקאות מהרבעונים הקודמים.")
e9 = P.edit(old9, new9, ["rooms.3.latest", "rooms.3.quarters[10-12.2025]"], "CONFLICT",
            "FAQ 3 rooms: 1.0-1.35M and the 1.2M anchor vs the official 918,100; the sharp one-quarter drop is shown with the previous quarter.")
old10 = "דירת 4 חדרים באשקלון נעה בדרך כלל סביב 1.45-1.85 מיליון ש\"ח, עם עוגן ביקוש שנצפה סביב 1.69 מיליון ש\"ח וכ-15,089 ש\"ח למ\"ר."
new10 = "לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים באשקלון ברבעון הראשון של 2026 היה 1,405,800 ש\"ח, לעומת 1,597,300 ש\"ח שנה קודם לכן."
e10 = P.edit(old10, new10, ["rooms.4.latest", "rooms.4.year_ago"], "CONFLICT", "FAQ 4 rooms: 1.45-1.85M and the 1.69M anchor vs the official 1,405,800.")
old11 = "דירת 5 חדרים באשקלון נעה לרוב סביב 1.9-2.5 מיליון ש\"ח, כאשר עוגן ביקוש שנצפה עמד סביב 2.2 מיליון ש\"ח."
new11 = "לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 5 חדרים באשקלון ברבעון הראשון של 2026 היה 1,891,000 ש\"ח, לעומת 2,142,600 ש\"ח שנה קודם לכן."
e11 = P.edit(old11, new11, ["rooms.5.latest", "rooms.5.year_ago"], "CONFLICT", "FAQ 5 rooms: the 2.2M anchor vs the official 1,891,000 (the 1.9-2.5M range itself was consistent).")

# ---------------- claims inventory ----------------
C = P.claim
C("p@4300", "דירת 2 חדרים ... סביב 850,000-1,050,000 ש\"ח", "sale", "UNSOURCED", f"edit {e1}", rooms=2, note="no official 2-room series, no source; dropped")
C("p@4300", "דירת 3 חדרים סביב 1.0-1.35 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e1}", rooms=3, official="918,100 (1-3.2026)")
C("p@4300", "דירת 4 חדרים סביב 1.45-1.85 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e1}", rooms=4, official="1,405,800 (1-3.2026)")
C("p@4300", "דירת 5 חדרים סביב 1.9-2.5 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e1}", rooms=5, official="1,891,000 (1-3.2026)", note="restated as the median inside the same rewrite")
C("p@4300", "בשכירות, נקודת האמצע העירונית סביב 3,500 ש\"ח", "rent", "UNSOURCED", "keep (dated listing source on the page, 4.6.2026)")
C("p@4300", "טווחים של כ-2,300 ש\"ח ... ועד כ-5,000-5,800 ש\"ח", "rent", "UNSOURCED", f"edit {e1}", figures=3, note="5,800 appears nowhere else on the page; dropped")
C("p@4300", "בערכי ביקוש של כ-10,900-17,400 ש\"ח למ\"ר", "per_m2", "UNSOURCED", "keep (listing data, page checked 6.6.2026; relabelled as asking)", figures=2)
C("p@42581", "3,097 דירות ובתים למכירה; שכירות ממוצעת 3,500; מדיאן 3,500 (279 מודעות); ממוצע 4,130", "rent", "UNSOURCED", "keep (listing sample, page checked 6.6.2026)", figures=3)
C("p@44652", "מדיאן שכירות 3,209 בברנע ... 2,918 בנווה ים", "rent", "UNSOURCED", "keep (listing sample, page checked 6.6.2026)", figures=9)
C("tr@47027", "2 חדרים | 850,000-1,050,000 | כ-870,000 | כ-17,400 למ\"ר", "sale", "UNSOURCED", f"edit {e3}", rooms=2, figures=3)
C("tr@47256", "3 חדרים | 1,000,000-1,350,000 ש\"ח", "sale", "CONFLICT", f"edit {e3}", rooms=3, official="918,100")
C("tr@47256", "3 חדרים | עוגן ביקוש כ-1,200,000 ש\"ח", "sale", "CONFLICT", f"edit {e3}", rooms=3, official="918,100")
C("tr@47256", "3 חדרים | כ-15,789 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"edit {e3}", rooms=3, note="column removed; the figure stays in the per-m2 FAQ as an asking anchor")
C("tr@47498", "4 חדרים | 1,450,000-1,850,000 ש\"ח", "sale", "CONFLICT", f"edit {e3}", rooms=4, official="1,405,800")
C("tr@47498", "4 חדרים | עוגן ביקוש כ-1,690,000 ש\"ח", "sale", "CONFLICT", f"edit {e3}", rooms=4, official="1,405,800")
C("tr@47498", "4 חדרים | כ-15,089 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"edit {e3}", rooms=4)
C("tr@47744", "5 חדרים | 1,900,000-2,500,000 ש\"ח", "sale", "CONSISTENT", f"edit {e3}", rooms=5, official="1,891,000 (within rounding of the floor)")
C("tr@47744", "5 חדרים | עוגן ביקוש כ-2,200,000 ש\"ח", "sale", "CONFLICT", f"edit {e3}", rooms=5, official="1,891,000")
C("tr@47744", "5 חדרים | כ-15,068 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"edit {e3}", rooms=5)
C("tr@47972", "6 חדרים ומעלה | 2,800,000-3,800,000 | כ-3,500,000 | כ-10,938 למ\"ר", "sale", "UNSOURCED", f"edit {e3}", rooms=6, figures=3)
C("p@49901", "מדיאן שכירות 5,287 בעיר היין, 5,053 במרינה, 4,980 באגמים", "rent", "UNSOURCED", "keep (listing sample, page checked 6.6.2026)", figures=3)
C("tr@50476..51981", "טבלת מדיאן שכירות לפי שכונה (9 שורות)", "rent", "UNSOURCED", "keep (listing sample, page checked 6.6.2026)", figures=9)
C("p@52732", "מדגם 279 מודעות: מדיאן 3,500, ממוצע 4,130, 3 חדרים 3,629 מול 4,400 ארצי", "rent", "UNSOURCED", "keep (listing sample, page checked 6.6.2026)", figures=4)
C("p@53236", "293 מודעות, ממוצע 4,108, מדיאן 3,500, עדכון 4 ביוני 2026", "rent", "UNSOURCED", "keep (dated: 4.6.2026)", figures=2)
C("tr@53928..55034", "טבלת מדיאן שכירות לפי חדרים (6 שורות + מקור נוסף)", "rent", "UNSOURCED", "keep (listing sample, page checked 6.6.2026)", figures=10)
C("p@56345", "באפרידר דירת 4 חדרים 100 מ\"ר נמכרה ב-1,560,000 ש\"ח, 10 באפריל 2025", "deal", "UNSOURCED", f"edit {e5}", rooms=4, official="Afridar 4 rooms 1,506,400 (1-3.2026)", figures=2, note="'example in the style of market data', no named source")
C("p@56794", "רחוב עלי 74 עסקאות 1,147,202 ... יוספטל 934,416", "sale_street", "UNSOURCED", f"edit {e6}", figures=4, note="no source, no period, mixed property types")
C("tr@57411..58028", "טבלת ממוצעי רחוב (4 שורות)", "sale_street", "UNSOURCED", f"edit {e7}", figures=4)
C("tr@58218", "אפרידר, דירת 4 חדרים | 1,560,000 | 15,600 למ\"ר | 10/04/2025", "deal", "UNSOURCED", f"edit {e7}", rooms=4, figures=2)
C("p@58847", "ריבית 3.75% (מאי 2026); מחירים +0.3% חודשי, -1.2% שנתי", "macro", "UNSOURCED", "keep (dated Bank of Israel decision, May 2026)", figures=3)
C("p@62980", "דירה מבוקשת ב-1.69 מיליון, קרובה לעוגן העירוני לדירת 4 חדרים", "sale", "CONFLICT", f"edit {e8}", rooms=4, official="1,405,800")
C("p@65597", "FAQ: דירת 3 חדרים 1.0-1.35 מיליון, עוגן 1.2 מיליון, 15,789 למ\"ר", "sale", "CONFLICT", f"edit {e9}", rooms=3, official="918,100", figures=3)
C("p@65927", "FAQ: דירת 4 חדרים 1.45-1.85 מיליון, עוגן 1.69 מיליון, 15,089 למ\"ר", "sale", "CONFLICT", f"edit {e10}", rooms=4, official="1,405,800", figures=3)
C("p@66223", "FAQ: דירת 5 חדרים 1.9-2.5 מיליון, עוגן 2.2 מיליון", "sale", "CONFLICT", f"edit {e11}", rooms=5, official="1,891,000", figures=2, note="range consistent, anchor in conflict")
C("p@67123", "FAQ שכירות: מדיאן 3,500, ממוצעים 4,108-4,130, לפי חדרים 2,963-7,127", "rent", "UNSOURCED", "keep (listing sample, page checked 6.6.2026)", figures=6)
C("p@67733", "FAQ: עוגני ביקוש 17,400 / 15,789 / 15,089 / 15,068 ש\"ח למ\"ר", "per_m2", "UNSOURCED", "keep (labelled asking anchors, page checked 6.6.2026)", figures=4)

P.write(notes=("Not audited as claims (illustrations, not market statements): 4,700 / 3,200 rent example (p@52732), the 1.32M / 1.82M / 2.6M "
               "if-examples (p@55258), 1,560,000 'a flat sold in some street' (p@56345 first sentence), 2.2M new-flat example (p@62294), "
               "1.75M / 1.58-1.65M if-example (p@62980 first sentence). Rent and listing figures are outside the official list and are kept "
               "where the page dates its check (6.6.2026) and names the kind of source. The 3-room median fell 20.6% in one quarter "
               "(1,142,100 in 10-12.2025 to 918,100 in 1-3.2026); the FAQ shows both quarters."))
