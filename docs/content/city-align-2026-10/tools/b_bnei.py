# -*- coding: utf-8 -*-
"""Bnei Brak (page 4595): body alignment with the official price list (1-3.2026). Built on the gold example b_ashkelon.py."""
from mk import Page

P = Page("bnei-brak-apartment-prices")

# ---------------- edits ----------------
# 1. the lead paragraph
old1 = P.find("מחירי דירות בבני ברק נעים כיום בטווחי עבודה רחבים:", "הן שלוש עסקאות שונות לחלוטין.")
new1 = ("מחירי דירות בבני ברק, לפי נתוני רשות המסים לרבעון הראשון של 2026: חציון מחיר העסקה היה 2,028,000 ש\"ח לדירת 3 חדרים, "
        "2,491,200 ש\"ח לדירת 4 חדרים ו-3,034,100 ש\"ח לדירת 5 חדרים. דירות גדולות, חדשות, נדירות או עם יתרונות כמו מעלית, חניה, "
        "מרפסת וממ\"ד יכולות להיות גבוהות יותר. בשכירות, המחירים המבוקשים במודעות נעים לרוב מכ-4,000 ש\"ח לדירת 2 חדרים ועד כ-7,900 "
        "ש\"ח לדירת 5 חדרים, עם פערים גדולים לפי רחוב, קומה, מצב הבניין והאזור בעיר. החציון הוא נקודת ייחוס ולא שומה: בני ברק היא "
        "שוק צפוף במיוחד שבו מחיר למ\"ר יכול להיות גבוה בגלל מחסור במלאי, ביקוש מקומי חזק, קרבה לרמת גן, גבעתיים, פתח תקווה ותל אביב, "
        "וניצול גבוה של כל מטר בנוי. לכן מספר חדרים לבדו אינו מספיק: דירת 3 חדרים ישנה ברחוב עמוס, דירת 3 חדרים משופצת ליד ציר "
        "תחבורה ודירת 3 חדרים בפרויקט חדש הן שלוש עסקאות שונות לחלוטין.")
e1 = P.edit(old1, new1, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "UNSOURCED",
            "Lead: the 2-room 'closed or offered' range 1.6-1.9M has no source kind and no official series; dropped. The 3/4/5-room working "
            "ranges (1.8-2.15M, 2.2-2.7M, 2.8-3.3M) were consistent with the official medians and are restated as the medians (1-3.2026) so the "
            "lead matches the price list. The rent range 4,000-7,900 is kept and labelled as listing asking rents (the same figures sit in the "
            "rent table and in the FAQ 'לפי נתוני ביקוש', page checked 6.6.2026).")

# 2. 'the ranges on this page are not an appraisal' pointed at the removed working ranges
old2 = "טווחי המחיר בדף זה אינם שומה."
new2 = "המחירים בדף זה אינם שומה."
e2 = P.edit(old2, new2, ["data_quarter"], "WORDING", "Follows edits 1 and 3: the page no longer gives working ranges.")

# 3. the rooms table: the working-range column becomes the official median; the dated asking columns stay
new3 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">סוג נכס</th>
<th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>
<th dir="rtl">מחיר ביקוש ממוצע שנצפה ביוני 2026</th>
<th dir="rtl">מחיר למ"ר מבוקש שנצפה</th>
<th dir="rtl">מה לבדוק לפני השוואה</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">2 חדרים</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">1,720,000 ש"ח</td>
<td dir="rtl">28,667 ש"ח למ"ר</td>
<td dir="rtl">שטח אמיתי, קומה, כיווני אוויר, אפשרות השכרה, מצב הבניין</td>
</tr>
<tr dir="rtl">
<td dir="rtl">3 חדרים</td>
<td dir="rtl">2,028,000 ש"ח</td>
<td dir="rtl">1,980,000 ש"ח</td>
<td dir="rtl">26,400 ש"ח למ"ר</td>
<td dir="rtl">התאמה למשפחה, מעלית, חדרים שימושיים, קרבה לרחוב עמוס</td>
</tr>
<tr dir="rtl">
<td dir="rtl">4 חדרים</td>
<td dir="rtl">2,491,200 ש"ח</td>
<td dir="rtl">2,445,000 ש"ח</td>
<td dir="rtl">24,949 ש"ח למ"ר</td>
<td dir="rtl">ממ"ד, מרפסת, חניה, שיפוץ, צפיפות בבניין</td>
</tr>
<tr dir="rtl">
<td dir="rtl">5 חדרים</td>
<td dir="rtl">3,034,100 ש"ח</td>
<td dir="rtl">3,025,000 ש"ח</td>
<td dir="rtl">23,269 ש"ח למ"ר</td>
<td dir="rtl">חלוקת חדרים, התאמה למשפחה גדולה, מעלית, מחסן, חניה</td>
</tr>
<tr dir="rtl">
<td dir="rtl">6 חדרים ומעלה</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">3,825,000 ש"ח</td>
<td dir="rtl">21,250 ש"ח למ"ר</td>
<td dir="rtl">נדירות, זכויות, בנייה חדשה, פיצול שימושים, ביקוש לקהל מסוים</td>
</tr>
</tbody>
</table>"""
e3 = P.table('<th dir="rtl">טווח עבודה סביר</th>', new3, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "UNSOURCED",
             "Rooms table: the 'reasonable working range' column has no source kind (2-room 1.6-1.9M and 6+-room 3.3M+ are outside the official "
             "list; the 3/4/5-room ranges were consistent). That column is replaced by the official medians (1-3.2026, 'לא פורסם' for 2 and 6+ "
             "rooms). The asking-average and asking-per-m2 columns are kept word for word: they are the 6.6.2026 asking sample of p@5599, and the "
             "header now says 'ביוני 2026'. Check notes kept word for word.")

# 4. the sentence after the rooms table
old4 = "הטבלה מראה תופעה מוכרת: ככל שהדירה גדולה יותר, המחיר הכולל עולה, אך המחיר למ\"ר אינו בהכרח עולה באותו קצב."
new4 = ("המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים ודירות 6 חדרים ומעלה כדאי לבדוק מול עסקאות דומות ברחוב "
        "ובשכונה. בטבלה בולטת גם תופעה מוכרת: ככל שהדירה גדולה יותר, המחיר הכולל עולה, אך המחיר למ\"ר אינו בהכרח עולה באותו קצב.")
e4 = P.edit(old4, new4, ["data_quarter"], "WORDING", "Follows edit 3: the official column has no 2-room and 6+-room median.")

# 5. the paragraph before the street table introduces the new neighbourhood table
old5 = "רחובות ותיקים עם מספר עסקאות גבוה נותנים תמונה רחבה יותר, אבל גם שם צריך לבדוק את הדירה עצמה ולא להסתפק בממוצע."
new5 = ("הטבלה הבאה מציגה את חציון מחיר העסקה לפי שכונה ומספר חדרים, לפי נתוני רשות המסים לרבעון הראשון של 2026. גם כאן צריך "
        "לבדוק את הרחוב ואת הדירה עצמה, ולא להסתפק בחציון של השכונה.")
e5 = P.edit(old5, new5, ["data_quarter"], "WORDING", "Introduces the neighbourhood table of edit 6 (the street averages leave the page).")

# 6. the street-average table becomes the official neighbourhood medians
new6 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">שכונה</th>
<th dir="rtl">3 חדרים</th>
<th dir="rtl">4 חדרים</th>
<th dir="rtl">5 חדרים</th>
<th dir="rtl">משמעות בבדיקת מחיר</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">פרדס כץ</td>
<td dir="rtl">1,861,100 ש"ח</td>
<td dir="rtl">2,458,000 ש"ח</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">מלאי רחב יחסית, כדאי לבדוק פער בין רחובות</td>
</tr>
<tr dir="rtl">
<td dir="rtl">הר שלום</td>
<td dir="rtl">2,023,300 ש"ח</td>
<td dir="rtl">2,795,700 ש"ח</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">השוואה טובה לדירות ותיקות, אך דורשת בדיקת בניין ושטח</td>
</tr>
<tr dir="rtl">
<td dir="rtl">קרית הרצוג</td>
<td dir="rtl">1,859,100 ש"ח</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">טווח מחירים תלוי מיקום נקודתי, מצב דירה וגישה</td>
</tr>
<tr dir="rtl">
<td dir="rtl">נחלת שמעון</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">2,486,900 ש"ח</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">מתאים להשוואת דירות משפחתיות רק לאחר התאמת שטח וגיל בניין</td>
</tr>
<tr dir="rtl">
<td dir="rtl">נוה אחיעזר</td>
<td dir="rtl">1,985,500 ש"ח</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">יש להפריד בין דירות קטנות, דירות משפחתיות ודירות בבניינים משופצים</td>
</tr>
<tr dir="rtl">
<td dir="rtl">אהרונוביץ וסוקולוב</td>
<td dir="rtl">2,043,600 ש"ח</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">השוואה צריכה להפריד בין בניינים וקומות</td>
</tr>
<tr dir="rtl">
<td dir="rtl">רמת אלחנן</td>
<td dir="rtl">2,222,400 ש"ח</td>
<td dir="rtl">2,778,100 ש"ח</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">יש לבדוק האם קיימים מאפייני נכס משופרים</td>
</tr>
<tr dir="rtl">
<td dir="rtl">אזור התעשיה</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">2,330,200 ש"ח</td>
<td dir="rtl">2,812,000 ש"ח</td>
<td dir="rtl">צריך לבדוק האם העסקאות כוללות דירות מיוחדות</td>
</tr>
</tbody>
</table>"""
e6 = P.table('<th dir="rtl">נתון עסקאות או שכירות שנצפה</th>', new6,
             ["neighbourhoods[פרדס כץ].rooms.3", "neighbourhoods[פרדס כץ].rooms.4", "neighbourhoods[הר שלום].rooms.3",
              "neighbourhoods[הר שלום].rooms.4", "neighbourhoods[קרית הרצוג].rooms.3", "neighbourhoods[נחלת שמעון].rooms.4",
              "neighbourhoods[נוה אחיעזר].rooms.3", "neighbourhoods[אהרונוביץ- סוקולוב].rooms.3", "neighbourhoods[רמת אלחנן].rooms.3",
              "neighbourhoods[רמת אלחנן].rooms.4", "neighbourhoods[אזור תעשיה].rooms.4", "neighbourhoods[אזור תעשיה].rooms.5"], "UNSOURCED",
             "Street table: ten all-rooms street averages (14-29 deals each) with no named source, no period and no room count. Replaced by the "
             "official neighbourhood medians by rooms, 1-3.2026 ('לא פורסם' where the official file has no median). Check notes reused from the "
             "old rows (and the Pardes Katz rent row).")

# 7. the sentence after the street table pointed at the removed deal counts
old7 = "כאשר ממוצע רחוב מסוים מבוסס על 14, 18 או 29 עסקאות, הוא נותן כיוון טוב יותר מאשר מודעה בודדת, אך הוא עדיין אינו מספר סופי."
new7 = "חציון של שכונה או ממוצע של רחוב נותנים כיוון טוב יותר מאשר מודעה בודדת, אך הם עדיין אינם מספר סופי."
e7 = P.edit(old7, new7, ["data_quarter"], "WORDING", "Follows edit 6: the street averages and their deal counts left the table.")

# 8. FAQ 3 rooms
old8 = P.find("טווח עבודה סביר לדירת 3 חדרים בבני ברק הוא כ-1.8-2.15 מיליון ש\"ח,", "במיקום מבוקש יכולה לעלות יותר.")
new8 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים בבני ברק ברבעון הראשון של 2026 היה 2,028,000 ש\"ח, לעומת 2,031,600 "
        "ש\"ח שנה קודם לכן. במודעות נצפה מחיר ביקוש ממוצע של כ-1,980,000 ש\"ח וכ-26,400 ש\"ח למ\"ר. דירה קטנה, ישנה או בקומה גבוהה "
        "ללא מעלית יכולה להיות מתחת לחציון, ודירה משופצת, נוחה או במיקום מבוקש יכולה לעלות יותר.")
e8 = P.edit(old8, new8, ["rooms.3.latest", "rooms.3.year_ago", "page"], "CONSISTENT",
            "FAQ 3 rooms: the working range 1.8-2.15M and the 1,980,000 asking average were consistent with the official 2,028,000; the answer now "
            "leads with the same median as the body (the working range no longer exists elsewhere on the page). Asking figures kept.")

# 9. FAQ 4 rooms (first sentence; the dated deal examples stay)
old9 = "דירת 4 חדרים נעה לרוב סביב 2.2-2.7 מיליון ש\"ח, ובנתוני ביקוש שנבדקו הופיע ממוצע של כ-2,445,000 ש\"ח."
new9 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים בבני ברק ברבעון הראשון של 2026 היה 2,491,200 ש\"ח, לעומת 2,554,600 "
        "ש\"ח שנה קודם לכן. בנתוני ביקוש שנבדקו הופיע ממוצע של כ-2,445,000 ש\"ח.")
e9 = P.edit(old9, new9, ["rooms.4.latest", "rooms.4.year_ago", "page"], "CONSISTENT",
            "FAQ 4 rooms: 2.2-2.7M and the 2,445,000 asking average were consistent with the official 2,491,200; restated as the median like the body.")

# ---------------- claims inventory ----------------
C = P.claim
K66 = "keep (asking sample dated 6.6.2026, private listing source)"
C("p@4310", "דירות 2 חדרים נסגרות או מוצעות לעיתים סביב 1.6-1.9 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e1}", rooms=2, note="no source kind, no official 2-room series; dropped")
C("p@4310", "דירות 3 חדרים סביב 1.8-2.15 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e1}", rooms=3, official="2,028,000 (1-3.2026)", note="restated as the median")
C("p@4310", "דירות 4 חדרים סביב 2.2-2.7 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e1}", rooms=4, official="2,491,200 (1-3.2026)", note="restated as the median")
C("p@4310", "דירות 5 חדרים סביב 2.8-3.3 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e1}", rooms=5, official="3,034,100 (1-3.2026)", note="restated as the median")
C("p@4310", "בשכירות ... מכ-4,000 ש\"ח לדירת 2 חדרים ועד כ-7,900 ש\"ח לדירת 5 חדרים", "rent", "UNSOURCED",
  "keep (asking rents by rooms, rent table + FAQ 'לפי נתוני ביקוש', page checked 6.6.2026; relabelled as listing asking rents in edit 1)", figures=2)
C("p@5599", "964 דירות ובתים למכירה; שכר דירה ממוצע מבוקש כ-5,700 ש\"ח (6.6.2026)", "rent", "UNSOURCED", K66, figures=2)
C("p@5599", "תשואה ממוצעת מוצגת של כ-3.6%", "yield", "UNSOURCED", K66)
C("p@5599", "מחיר ביקוש ממוצע כ-1,720,000 ש\"ח לדירות 2 חדרים", "sale", "UNSOURCED", K66, rooms=2)
C("p@5599", "מחיר ביקוש ממוצע כ-1,980,000 ש\"ח לדירות 3 חדרים", "sale", "CONSISTENT", K66, rooms=3, official="2,028,000 (-2.4%)")
C("p@5599", "מחיר ביקוש ממוצע כ-2,445,000 ש\"ח לדירות 4 חדרים", "sale", "CONSISTENT", K66, rooms=4, official="2,491,200 (-1.9%)")
C("p@5599", "מחיר ביקוש ממוצע כ-3,025,000 ש\"ח לדירות 5 חדרים", "sale", "CONSISTENT", K66, rooms=5, official="3,034,100 (-0.3%)")
C("p@5599", "וכ-3,825,000 ש\"ח לדירות 6 חדרים ומעלה", "sale", "UNSOURCED", K66, rooms=6)
C("p@6062", "מאגר עסקאות פרטי ... מחיר ממוצע של כ-2,350,000 ש\"ח", "sale_avg", "CONSISTENT", "keep (private deals database, checked 6.6.2026)",
  rooms="all", official="rooms.all 2,288,600 (1-3.2026, +2.7%)")
C("p@6062", "כ-29,000 ש\"ח למ\"ר וכ-1,460 עסקאות שנצפו במערכת", "per_m2", "UNSOURCED", "keep (private deals database, checked 6.6.2026)", figures=2)
C("p@8392", "נפחי עסקאות: פרדס כץ ויסודות 3,861 ... שכון ה' 817", "count", "UNSOURCED",
  "keep (deal volumes, not prices; deal-analysis source, page checked 6.6.2026)", figures=10)
C("p@12098", "רבי עקיבא 2,450,000 (25.2.2026); אברבנאל 117 2,235,000 (1.3.2026); הרב דנגור 15 2,500,000 (12.3.2026)", "deal", "UNSOURCED",
  "keep (individual dated deals)", rooms=4, figures=3, note="2,235,000 shows as SUSPECT in check.py: one dated deal, not a city level")
C("tr@10520", "2 חדרים | טווח עבודה סביר 1.6-1.9 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e3}", rooms=2)
C("tr@10520", "2 חדרים | מחיר ביקוש ממוצע 1,720,000 ש\"ח", "sale", "UNSOURCED", f"keep (same 6.6.2026 asking sample as p@5599; carried into the table of edit {e3})", rooms=2)
C("tr@10749", "3 חדרים | 1.8-2.15 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e3}", rooms=3, official="2,028,000")
C("tr@10749", "3 חדרים | מחיר ביקוש ממוצע 1,980,000 ש\"ח", "sale", "CONSISTENT", f"keep (carried into the table of edit {e3})", rooms=3, official="2,028,000 (-2.4%)")
C("tr@10976", "4 חדרים | 2.2-2.7 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e3}", rooms=4, official="2,491,200")
C("tr@10976", "4 חדרים | מחיר ביקוש ממוצע 2,445,000 ש\"ח", "sale", "CONSISTENT", f"keep (carried into the table of edit {e3})", rooms=4, official="2,491,200 (-1.9%)")
C("tr@11189", "5 חדרים | 2.8-3.3 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e3}", rooms=5, official="3,034,100")
C("tr@11189", "5 חדרים | מחיר ביקוש ממוצע 3,025,000 ש\"ח", "sale", "CONSISTENT", f"keep (carried into the table of edit {e3})", rooms=5, official="3,034,100 (-0.3%)")
C("tr@11413", "6 חדרים ומעלה | 3.3 מיליון ש\"ח ומעלה", "sale", "UNSOURCED", f"edit {e3}", rooms=6)
C("tr@11413", "6 חדרים ומעלה | מחיר ביקוש ממוצע 3,825,000 ש\"ח", "sale", "UNSOURCED", f"keep (same 6.6.2026 asking sample as p@5599; carried into the table of edit {e3})", rooms=6)
C("tr@10520..11413", "עמודת מחיר למ\"ר מבוקש שנצפה: 28,667 / 26,400 / 24,949 / 23,269 / 21,250", "per_m2", "UNSOURCED",
  f"keep (labelled asking per m2, page checked 6.6.2026; carried into the table of edit {e3})", figures=5)
C("p@11672", "מחיר למ\"ר נצפה: 28,667 / 26,400 / 24,949 / 23,269 / 21,250 ש\"ח", "per_m2", "UNSOURCED", "keep (refers to the asking per-m2 column, page checked 6.6.2026)", figures=5)
C("tr@13505..15303", "טבלת ממוצעי עסקאות לפי רחוב (10 רחובות, 14-29 עסקאות)", "sale_street", "UNSOURCED", f"edit {e6}", figures=10,
  note="no named source, no period, all room counts mixed")
C("p@15888", "שכירות לפי אזור (29.5.2026): פרדס כץ 4,900 ... אזור התעשיה 6,100", "rent", "UNSOURCED", "keep (listing sample dated 29.5.2026)", figures=5)
C("p@16703", "שכר דירה 5,700 במקור אחד; 37 מודעות, ממוצע 4,888, חציון 4,600, זולה 2,500 (29.5.2026)", "rent", "UNSOURCED", "keep (listing sources dated 6.6.2026 and 29.5.2026)", figures=4)
C("tr@17316..18314", "טבלת שכירות: 4,000 / 4,700 / 5,950 / 7,900 לפי חדרים; 5,700 / 4,888 / 4,600", "rent", "UNSOURCED",
  "keep (asking rents; sources dated 6.6.2026 and 29.5.2026 in the paragraphs above)", figures=7)
C("tr@19082..20370", "טבלת שכירות לפי אזור (9 שורות, מספר מודעות ושכר דירה ממוצע)", "rent", "UNSOURCED", "keep (listing sample dated 29.5.2026 in p@15888)", figures=9)
C("p@20902", "מקור עסקאות פרטי הציג מחיר ממוצע של כ-29,000 ש\"ח למ\"ר", "per_m2", "UNSOURCED", "keep (private deals database, checked 6.6.2026)")
C("p@21253", "הרב דנגור 15 2,500,000 (12.3.2026); הנגב 34 1,900,000 (10.3.2026); סמטת רחל 7 1,947,000 (22.2.2026)", "deal", "UNSOURCED",
  "keep (individual dated deals)", figures=3)
C("tr@21874..23927", "טבלת עסקאות אחרונות (10 עסקאות מתוארכות, 22.2-12.3.2026)", "deal", "UNSOURCED", "keep (individual dated deals)", figures=10,
  note="the 3-, 4- and 5-room rows below the official median show as SUSPECT in check.py: single dated deals, not a city level")
C("p@24168", "40,563 ש\"ח למ\"ר (48 מ\"ר, 1,947,000) מול 18,657 ש\"ח למ\"ר (134 מ\"ר, 2,500,000)", "per_m2", "UNSOURCED",
  "keep (per m2 of two dated deals listed in the table)", figures=2)
C("p@26472", "בעיר עם 964 דירות ובתים למכירה לפי מקור דינמי אחד", "count", "UNSOURCED", "keep (same listing source dated 6.6.2026 in p@5599)")
C("p@29319", "בנק ישראל 25.5.2026: ריבית 3.75%; מחירים +0.3% חודשי, -1.2% שנתי", "macro", "UNSOURCED", "keep (dated Bank of Israel decision, 25.5.2026)", figures=3)
C("p@30191", "FAQ: טווח עבודה סביר לדירת 3 חדרים כ-1.8-2.15 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e8}", rooms=3, official="2,028,000")
C("p@30191", "FAQ: נתון ביקוש ממוצע כ-1,980,000 ש\"ח וכ-26,400 ש\"ח למ\"ר", "sale", "CONSISTENT", f"keep (asking figures kept inside edit {e8})", rooms=3,
  official="2,028,000 (-2.4%)", figures=2, note="26,400 is asking per m2 (unsourced, page-dated)")
C("p@30523", "FAQ: דירת 4 חדרים סביב 2.2-2.7 מיליון ש\"ח, ממוצע ביקוש כ-2,445,000 ש\"ח", "sale", "CONSISTENT", f"edit {e9}", rooms=4,
  official="2,491,200", figures=2, note="asking average kept inside the edit")
C("p@30523", "FAQ: עסקאות לדוגמה 2,450,000 / 2,235,000 / 2,500,000 ש\"ח", "deal", "UNSOURCED", "keep (the same dated deals as the deals table)", rooms=4, figures=3)
C("p@30884", "FAQ: מחיר ממוצע של כ-29,000 ש\"ח למ\"ר", "per_m2", "UNSOURCED", "keep (private deals database, checked 6.6.2026)")
C("p@31532", "FAQ: פרדס כץ ויסודות 11 מודעות בממוצע 4,900 ש\"ח", "rent", "UNSOURCED", "keep (listing sample dated 29.5.2026 in the body)")
C("p@31842", "FAQ שכירות: 4,000 / 4,700 / 5,950 / 7,900; ממוצע 4,888, חציון 4,600 (37 מודעות)", "rent", "UNSOURCED",
  "keep (labelled asking data, sources dated in the body)", figures=6)

P.write(notes=(
    "All city-level 3/4/5-room sale figures on this page were already consistent with the official medians (working ranges, the 6.6.2026 "
    "asking averages, the private-database city average 2,350,000 vs 2,288,600). The edits remove the unsourced 2-room and 6+-room working "
    "ranges and the street-average table, and restate the consistent ranges (lead, rooms table, FAQ 3 and 4 rooms) as the official medians "
    "so the body, the FAQ and the price list give one figure per room count. Not audited as claims: the 100,000-200,000 gap illustration "
    "(p@6781), the 3-room / 4-room rent-income if-example 1,980,000 / 2,445,000 / 56,400 / 71,400 (p@18498), the two single listings "
    "6,500 / 2,500 (p@20581, they point at rows of the rent table), the 2,650,000 vs 2,350,000-2,500,000 if-example (p@24498). Remaining "
    "SUSPECT lines in check.py are individual dated deals (p@12098, the deals table tr@21874..23927, FAQ p@30523), not city levels. "
    "Name mapping: page 'פרדס כץ ויסודות' = official 'פרדס כץ'; 'אזור התעשיה' = official 'אזור תעשיה'; the official area 'אהרונוביץ- סוקולוב' "
    "is written 'אהרונוביץ וסוקולוב' and is NOT equated with the page's 'גבעת סוקולוב'; 'רמת אלחנן' is an official neighbourhood the old "
    "text did not name. The 5-room median jumped to 3,402,400 in 10-12.2025 and fell back to 3,034,100 in 1-3.2026 (a one-quarter spike); "
    "the page only uses 1-3.2026."))
