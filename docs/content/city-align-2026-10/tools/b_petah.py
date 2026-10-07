# -*- coding: utf-8 -*-
"""Petah Tikva (page 4573): body alignment with the official price list (1-3.2026). Built on the gold example b_ashkelon.py."""
from mk import Page

P = Page("petah-tikva-apartment-prices")

# ---------------- edits ----------------
# 1. parameter table: new vs second-hand premium (tier 2)
e1 = P.edit("לעיתים כ-8%-22%", "משתנה לפי פרויקט, מפרט ומועד מסירה",
            ["page"], "UNSOURCED",
            "A new-vs-second-hand premium of 8%-22% with no named source (an estimate, not something a listing check measures); "
            "rephrased without the number. Tier 2.", tier=2)

# 2. rooms table
new2 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">סוג דירה</th>
<th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>
<th dir="rtl">ינואר-מרץ 2025</th>
<th dir="rtl">שינוי בשנה</th>
<th dir="rtl">דגשים שמשנים מחיר</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">3 חדרים</td>
<td dir="rtl">2,057,000 ש"ח</td>
<td dir="rtl">1,971,600 ש"ח</td>
<td dir="rtl">עלייה של 4.3%</td>
<td dir="rtl">קומה, מעלית, מצב פנימי ופוטנציאל התחדשות; במחנה יהודה ובעין גנים החציון נמוך יותר</td>
</tr>
<tr dir="rtl">
<td dir="rtl">4 חדרים</td>
<td dir="rtl">2,444,100 ש"ח</td>
<td dir="rtl">2,500,000 ש"ח</td>
<td dir="rtl">ירידה של 2.2%</td>
<td dir="rtl">חניה, ממ"ד, מרפסת, מעלית ושכונה יוצרים פער גדול</td>
</tr>
<tr dir="rtl">
<td dir="rtl">5 חדרים</td>
<td dir="rtl">3,322,600 ש"ח</td>
<td dir="rtl">3,326,300 ש"ח</td>
<td dir="rtl">ירידה של 0.1%</td>
<td dir="rtl">שכונה, שטח, קומה, חניות, ממ"ד ומרפסת; בשכונות חזקות המחיר גבוה יותר</td>
</tr>
</tbody>
</table>"""
e2 = P.table('<th dir="rtl">טווח מחיר עבודה</th>', new2,
             ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct",
              "rooms.5.latest", "rooms.5.year_ago", "rooms.5.change_pct", "neighbourhoods[מחנה יהודה].rooms.3", "neighbourhoods[עין גנים].rooms.3"],
             "UNSOURCED",
             "Rooms table of 'working ranges': the 3, 4 and 5-room ranges hold the official medians (consistent) but the 2, 2.5, 3.5-room, garden "
             "and penthouse rows and the Achdut neighbourhood ranges in the notes column have no named source. Replaced by the official medians "
             "with the year-earlier quarter; the 4-room note is kept word for word, the 3 and 5-room notes are rewritten without numbers "
             "(Mahane Yehuda 1,951,200 and Ein Ganim 1,890,700 are below the city 3-room median). The typical-size column leaves with the old rows.")

# 3. the sentence after the rooms table pointed at the old table
old3 = "טבלת חדרים טובה נותנת תשובה מהירה לשאלה כמה עולה דירה בפתח תקווה, אבל היא עדיין אינה מספיקה להצעה רצינית."
new3 = ("המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים, דירות עם חצי חדר, דירות גן ופנטהאוזים כדאי לבדוק מול "
        "עסקאות דומות ברחוב ובשכונה. החציון נותן תשובה מהירה לשאלה כמה עולה דירה בפתח תקווה, אבל הוא עדיין אינו מספיק להצעה רצינית.")
e3 = P.edit(old3, new3, ["data_quarter"], "WORDING", "Follows edit 2: the 2, 2.5, 3.5-room, garden and penthouse rows left the table.")

# 4. neighbourhood per-m2 table
new4 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">שכונה או אזור</th>
<th dir="rtl">סוג מלאי נפוץ</th>
<th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>
<th dir="rtl">איך לקרוא את האזור</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">מרכז העיר</td>
<td dir="rtl">בניינים ותיקים, מסחר, כיסי התחדשות</td>
<td dir="rtl">3 חדרים 1,885,500 ש"ח, 4 חדרים 2,338,000 ש"ח, 5 חדרים 2,960,100 ש"ח</td>
<td dir="rtl">בודקים רחוב, רעש, קומה, מעלית וסיכוי להתחדשות</td>
</tr>
<tr dir="rtl">
<td dir="rtl">המרכז השקט</td>
<td dir="rtl">דירות ותיקות ומשופצות</td>
<td dir="rtl">לא מוצג במחירון</td>
<td dir="rtl">לעיתים פרמיה על רחובות שקטים ונגישות טובה</td>
</tr>
<tr dir="rtl">
<td dir="rtl">כפר גנים א'</td>
<td dir="rtl">דירות משפחתיות ובניינים מגוונים</td>
<td dir="rtl">4 חדרים 2,490,000 ש"ח, 5 חדרים 3,155,200 ש"ח</td>
<td dir="rtl">השוואה פנימית לפי רחוב וגיל בניין קריטית</td>
</tr>
<tr dir="rtl">
<td dir="rtl">כפר גנים ב'</td>
<td dir="rtl">דירות משפחתיות, חלקן גדולות</td>
<td dir="rtl">3 חדרים 2,212,400 ש"ח</td>
<td dir="rtl">חניה, מחסן ומרפסת משפיעים מאוד</td>
</tr>
<tr dir="rtl">
<td dir="rtl">כפר גנים ג'</td>
<td dir="rtl">מלאי מבוקש, דירות גדולות יותר</td>
<td dir="rtl">לא מוצג במחירון</td>
<td dir="rtl">פער גדול בין דירה רגילה לדירה משודרגת</td>
</tr>
<tr dir="rtl">
<td dir="rtl">אם המושבות החדשה</td>
<td dir="rtl">בניינים חדשים יחסית, משפחות, מגדלים</td>
<td dir="rtl">לא מוצג במחירון</td>
<td dir="rtl">קרבה לצירים, קומה, נוף ודמי ניהול משנים מחיר</td>
</tr>
<tr dir="rtl">
<td dir="rtl">נווה גן</td>
<td dir="rtl">דירות גדולות וחדשות יחסית</td>
<td dir="rtl">לא מוצג במחירון</td>
<td dir="rtl">מחיר גבוה יותר צריך להיבדק מול עסקאות קרובות מאוד</td>
</tr>
<tr dir="rtl">
<td dir="rtl">רמת ורבר</td>
<td dir="rtl">ותיק לצד התחדשות</td>
<td dir="rtl">3 חדרים 2,435,200 ש"ח, 4 חדרים 2,489,300 ש"ח</td>
<td dir="rtl">פוטנציאל עתידי אינו מחיר סגירה מובטח</td>
</tr>
<tr dir="rtl">
<td dir="rtl">עין גנים</td>
<td dir="rtl">מלאי ותיק, דירות בינוניות</td>
<td dir="rtl">3 חדרים 1,890,700 ש"ח, 4 חדרים 2,153,800 ש"ח</td>
<td dir="rtl">מצב בניין ורחוב קובעים יותר מהממוצע</td>
</tr>
<tr dir="rtl">
<td dir="rtl">מחנה יהודה</td>
<td dir="rtl">דירות ותיקות ועסקאות קטנות יחסית</td>
<td dir="rtl">3 חדרים 1,951,200 ש"ח, 4 חדרים 2,291,100 ש"ח</td>
<td dir="rtl">משווים לדירות ותיקות דומות בגודל, בקומה ובמצב</td>
</tr>
<tr dir="rtl">
<td dir="rtl">אחדות</td>
<td dir="rtl">מלאי ותיק ומשפחתי</td>
<td dir="rtl">לא מוצג במחירון</td>
<td dir="rtl">משווים לעסקאות דומות ברחוב ובבניין</td>
</tr>
<tr dir="rtl">
<td dir="rtl">עמישב</td>
<td dir="rtl">דירות ותיקות, מחירים נגישים יותר</td>
<td dir="rtl">לא מוצג במחירון</td>
<td dir="rtl">בודקים מצב פיזי, הצמדות וחידוש סביבתי</td>
</tr>
<tr dir="rtl">
<td dir="rtl">קרול</td>
<td dir="rtl">דירות ותיקות, קרבה למרכז</td>
<td dir="rtl">לא מוצג במחירון</td>
<td dir="rtl">פערים לפי רחוב, קומה ושיפוץ</td>
</tr>
<tr dir="rtl">
<td dir="rtl">סגולה ורמת סיב</td>
<td dir="rtl">מגורים לצד תעסוקה, מסחר וצירים</td>
<td dir="rtl">לא מוצג במחירון</td>
<td dir="rtl">בודקים רעש, נגישות, שימושים מעורבים ותוכניות עתידיות</td>
</tr>
</tbody>
</table>"""
e4 = P.table('<th dir="rtl">טווח מחיר למ"ר לבדיקה</th>', new4,
             ["neighbourhoods[מרכז העיר].rooms.3", "neighbourhoods[מרכז העיר].rooms.4", "neighbourhoods[מרכז העיר].rooms.5",
              "neighbourhoods[כפר גנים א].rooms.4", "neighbourhoods[כפר גנים א].rooms.5", "neighbourhoods[כפר גנים ב].rooms.3",
              "neighbourhoods[רמת ורבר].rooms.3", "neighbourhoods[רמת ורבר].rooms.4", "neighbourhoods[עין גנים].rooms.3",
              "neighbourhoods[עין גנים].rooms.4", "neighbourhoods[מחנה יהודה].rooms.3", "neighbourhoods[מחנה יהודה].rooms.4"],
             "CONFLICT",
             "Neighbourhood table: 14 per-m2 ranges, 12 of them with no source marker at all, plus two 3-room sale ranges: Mahane Yehuda 1.5-1.9M "
             "vs the official neighbourhood median 1,951,200 (conflict) and Achdut 1.6-2.1M (no official median). The per-m2 column becomes the "
             "official neighbourhood medians by rooms, 1-3.2026 ('לא מוצג במחירון' for the 8 page areas not in the city file: the city file keeps only 8 neighbourhoods; the official files DO hold 1-3.2026 medians for some of the others (checked 7.10.2026), so these rows say 'לא מוצג במחירון' (not shown in the page's list), never 'לא פורסם'). Inventory and how-to-read columns kept "
             "word for word except the two cells that held the sale ranges.")

# 5. first sentence after the neighbourhood table explains the medians and the 'לא פורסם' cells
old5 = "המחיר בשכונה מבוקשת אינו אוטומטי לכל דירה."
new5 = ("החציון בטבלה הוא לפי נתוני רשות המסים לרבעון הראשון של 2026; בשכונות שאינן מופיעות במחירון, משווים לעסקאות סגורות דומות ברחוב "
        "ובבניין. גם המחיר בשכונה מבוקשת אינו אוטומטי לכל דירה.")
e5 = P.edit(old5, new5, ["data_quarter"], "WORDING", "Follows edit 4: names the source and quarter of the neighbourhood medians and explains 'לא פורסם'.")

# 6. deals and per-m2 table
new6 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">נתון או דוגמה</th>
<th dir="rtl">מספר שנבדק</th>
<th dir="rtl">מה לומדים ממנו</th>
<th dir="rtl">מה לא להסיק ממנו</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">רחוב זכרון יעקב, 4 חדרים</td>
<td dir="rtl">86 מ"ר, קומה 2 מתוך 7, 2 חניות, 2.46 מיליון ש"ח</td>
<td dir="rtl">דוגמה טובה לכיול דירת 4 חדרים דומה</td>
<td dir="rtl">לא ממוצע עירוני לכל דירות 4 חדרים</td>
</tr>
<tr dir="rtl">
<td dir="rtl">פתח תקווה, דירות 4 חדרים</td>
<td dir="rtl">2,444,100 ש"ח, חציון מחיר העסקה ינואר-מרץ 2026</td>
<td dir="rtl">נקודת ייחוס עירונית לדירת 4 חדרים</td>
<td dir="rtl">לא מחיר סגירה לדירה מסוימת</td>
</tr>
<tr dir="rtl">
<td dir="rtl">מחנה יהודה, דירות 3 חדרים</td>
<td dir="rtl">1,951,200 ש"ח, חציון מחיר העסקה ינואר-מרץ 2026</td>
<td dir="rtl">נקודת ייחוס לדירות ותיקות יותר</td>
<td dir="rtl">לא מתאים לכפר גנים או אם המושבות</td>
</tr>
<tr dir="rtl">
<td dir="rtl">מחנה יהודה, מחיר למ"ר</td>
<td dir="rtl">כ-20,000-24,000 ש"ח למ"ר</td>
<td dir="rtl">מדד לאזור נגיש יותר במחיר</td>
<td dir="rtl">לא כולל בהכרח דירות משודרגות או חדשות</td>
</tr>
<tr dir="rtl">
<td dir="rtl">מרכז העיר לפי הקשר שוק</td>
<td dir="rtl">כ-25,000-26,000 ש"ח למ"ר</td>
<td dir="rtl">מסגרת לבדיקה של בניינים ותיקים</td>
<td dir="rtl">לא מתאים לדירה חדשה עם מפרט גבוה</td>
</tr>
<tr dir="rtl">
<td dir="rtl">אזורים סמוכים וחזקים יותר</td>
<td dir="rtl">כ-28,000-32,000 ש"ח למ"ר</td>
<td dir="rtl">עוזר לזהות פרמיית שכונה ואיכות</td>
<td dir="rtl">לא כל רחוב באזור שווה אותו דבר</td>
</tr>
</tbody>
</table>"""
e6 = P.table('<th dir="rtl">מספר שנבדק</th>', new6,
             ["rooms.4.latest", "neighbourhoods[מחנה יהודה].rooms.3", "page"], "CONFLICT",
             "Deals table: Mahane Yehuda 3 rooms 1.5-1.9M conflicts with the official neighbourhood median 1,951,200; the two Achdut ranges "
             "(3 and 5 rooms) and the '+15% deal volume' row have no named source and no official counterpart. Replaced by the official "
             "figures (city 4-room median beside the Zichron Yaakov deal, Mahane Yehuda 3-room median); the dated deal and the three per-m2 rows "
             "the page labels as checked are kept word for word.")

# 7-9. new vs second-hand table: premium percentages (tier 2)
e7 = P.edit("כ-5%-12% מעל דירה לא משופצת דומה", "מעל דירה לא משופצת דומה, לפי איכות השיפוץ", ["page"], "UNSOURCED",
            "Renovation premium 5%-12% with no source; rephrased without the number. Tier 2.", tier=2)
e8 = P.edit("כ-8%-18% מעל יד שנייה דומה", "מעל יד שנייה דומה, לפי מפרט, מיקום וגיל הבניין", ["page"], "UNSOURCED",
            "New-flat premium 8%-18% with no source; rephrased without the number. Tier 2.", tier=2)
e9 = P.edit("כ-10%-22% לפי פרויקט ומועד", "לפי פרויקט, מפרט ומועד מסירה", ["page"], "UNSOURCED",
            "Off-plan premium 10%-22% with no source; rephrased without the number. Tier 2.", tier=2)

# 10-12. FAQ answers 3 / 4 / 5 rooms
old10 = P.find("טווח עבודה לדירת 3 חדרים נע סביב 1.55-2.25 מיליון ש\"ח,", "ובאחדות דירות 70-80 מ\"ר סביב 1.6-2.1 מיליון ש\"ח.")
new10 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים בפתח תקווה ברבעון הראשון של 2026 היה 2,057,000 ש\"ח, לעומת 1,971,600 ש\"ח "
         "שנה קודם לכן. בשכונות ותיקות החציון נמוך יותר: 1,951,200 ש\"ח במחנה יהודה ו-1,890,700 ש\"ח בעין גנים.")
e10 = P.edit(old10, new10, ["rooms.3.latest", "rooms.3.year_ago", "neighbourhoods[מחנה יהודה].rooms.3", "neighbourhoods[עין גנים].rooms.3"],
             "CONFLICT",
             "FAQ 3 rooms: Mahane Yehuda 1.5-1.9M vs the official neighbourhood median 1,951,200; Achdut 1.6-2.1M has no official median; "
             "the city range 1.55-2.25M was consistent and is restated as the median (same figures as the rooms table).")
old11 = "דירות 4 חדרים נבדקות לרוב סביב 2.15-3.15 מיליון ש\"ח, אך דירה חדשה, דירה עם מרפסת גדולה, חניה כפולה או מיקום חזק יכולה לעלות יותר."
new11 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים בפתח תקווה ברבעון הראשון של 2026 היה 2,444,100 ש\"ח, לעומת 2,500,000 ש\"ח "
         "שנה קודם לכן. דירה חדשה, דירה עם מרפסת גדולה, חניה כפולה או מיקום חזק יכולה לעלות יותר.")
e11 = P.edit(old11, new11, ["rooms.4.latest", "rooms.4.year_ago"], "CONSISTENT",
             "FAQ 4 rooms: the range 2.15-3.15M holds the official 2,444,100 but came from the replaced rooms table; restated as the median so "
             "the FAQ matches the body. The Zichron Yaakov deal sentence after it is kept.")
old12 = P.find("דירות 5 חדרים נעות בטווח עבודה רחב של כ-2.65-4.20 מיליון ש\"ח,", "דירות משפחתיות יכולות להיבדק בטווח גבוה יותר.")
new12 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 5 חדרים בפתח תקווה ברבעון הראשון של 2026 היה 3,322,600 ש\"ח, לעומת 3,326,300 ש\"ח "
         "שנה קודם לכן. המחיר משתנה לפי שכונה, שטח, קומה, חניות, ממ\"ד ומרפסת: באותו רבעון החציון לדירת 5 חדרים היה 2,960,100 ש\"ח "
         "במרכז העיר, 3,155,200 ש\"ח בכפר גנים א' ו-3,790,800 ש\"ח בנווה עוז הירוקה.")
e12 = P.edit(old12, new12, ["rooms.5.latest", "rooms.5.year_ago", "neighbourhoods[מרכז העיר].rooms.5", "neighbourhoods[כפר גנים א].rooms.5",
                            "neighbourhoods[נווה עוז הירוקה].rooms.5"], "UNSOURCED",
             "FAQ 5 rooms: the city range 2.65-4.20M was consistent; the Achdut 2.2-2.85M range has no source or official median, and the claim "
             "that Kfar Ganim is checked in a higher range does not hold for Kfar Ganim A 5 rooms (3,155,200, below the city 3,322,600). "
             "Rewritten with the official city and neighbourhood medians.")

# 13. FAQ: how much to take off the asking price (tier 2)
old13 = "במקרים מסוימים הפער יהיה 2%-4%, ובמקרים אחרים 8%-12% או יותר, בעיקר כאשר המודעה יקרה ביחס לעסקאות."
new13 = "במקרים מסוימים הפער קטן, ובמקרים אחרים גדול בהרבה, בעיקר כאשר המודעה יקרה ביחס לעסקאות."
e13 = P.edit(old13, new13, ["page"], "UNSOURCED", "Asking-to-deal gaps of 2%-4% and 8%-12% with no source; rephrased without the numbers. Tier 2.", tier=2)

# ---------------- claims inventory ----------------
C = P.claim
C("p@4371", "הפער בין דירות ... יכול להגיע ... ואף ליותר מ-1,000,000 ש\"ח", "other", "CONSISTENT", "keep (official 3-room 2,057,000 vs 5-room 3,322,600)")
C("p@4371", "בדיקת שכירות סביב 5,000-8,000 ש\"ח בחלק גדול מהשכונות", "rent", "UNSOURCED", "keep (listing sample on the page, 184-233 active listings; market check dated 6.6.2026)", figures=2)
C("p@42022", "טווח העבודה ... מכ-1.5 מיליון ש\"ח ... ועד כ-4.2 מיליון ש\"ח בדירות 5 חדרים", "sale", "CONSISTENT", "keep (floor and ceiling hold the official 3, 4, 5-room medians)", rooms="all", official="3=2,057,000 4=2,444,100 5=3,322,600 (1-3.2026)", figures=2)
C("p@42331", "דמי שכירות ממוצעים לדוגמא 4,383 בעמישב ... 9,875 בנווה גן", "rent", "UNSOURCED", "keep (market pages checked, page checked 6.6.2026)", figures=5)
C("tr@43339", "החלטת קנייה נפוצה | כ-1.7-3.4 מיליון ש\"ח", "sale", "CONSISTENT", "keep", rooms="all", official="3=2,057,000 4=2,444,100 5=3,322,600 all=2,441,100", figures=2)
C("tr@43507", "מרכז ותיק | כ-25,000-26,000 ש\"ח למ\"ר בהקשרים שנבדקו", "per_m2", "UNSOURCED", "keep (usage note above the table: public market check of 6.6.2026)", figures=2)
C("tr@43674", "אזורים מבוקשים יותר | כ-28,000-32,000 ש\"ח למ\"ר בחלק מהבדיקות", "per_m2", "UNSOURCED", "keep (same dated market check)", figures=2)
C("tr@43847", "שכירות בדירות משפחתיות | כ-5,500-8,700 ש\"ח", "rent", "UNSOURCED", "keep (same dated market check; matches the rent listing table)", figures=2)
C("tr@44047", "פער דירה חדשה מול יד שנייה | לעיתים כ-8%-22%", "sale_new_used", "UNSOURCED", f"edit {e1}", figures=2, note="tier 2")
C("tr@44920", "2 חדרים | כ-1.25-1.75 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e2}", rooms=2, figures=2)
C("tr@45113", "2.5 חדרים | כ-1.45-1.95 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e2}", rooms="2.5", figures=2)
C("tr@45298", "3 חדרים | כ-1.55-2.25 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e2}", rooms=3, official="2,057,000 (1-3.2026)", figures=2, note="restated as the median in the rebuilt table")
C("tr@45298", "במחנה יהודה ואחדות נראו הקשרים סביב 1.5-2.1 מיליון ש\"ח", "sale_nb", "UNSOURCED", f"edit {e2}", rooms=3, official="Mahane Yehuda 3 rooms 1,951,200 (inside); Achdut: no official median", figures=2)
C("tr@45491", "3.5 חדרים | כ-1.85-2.45 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e2}", rooms="3.5", figures=2)
C("tr@45689", "4 חדרים | כ-2.15-3.15 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e2}", rooms=4, official="2,444,100 (1-3.2026)", figures=2, note="restated as the median")
C("tr@45876", "5 חדרים | כ-2.65-4.20 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e2}", rooms=5, official="3,322,600 (1-3.2026)", figures=2, note="restated as the median")
C("tr@45876", "באחדות נראו הקשרים סביב 2.2-2.85 מיליון ש\"ח", "sale_nb", "UNSOURCED", f"edit {e2}", rooms=5, official="Achdut: no official median", figures=2)
C("tr@46092", "דירת גן | כ-2.75-4.80 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e2}", rooms="garden", figures=2)
C("tr@46295", "פנטהאוז או דירת גג | כ-3.80-6.50 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e2}", rooms="penthouse", figures=2)
C("p@46515", "דירת 4 חדרים של 86 מ\"ר עם 2 חניות שנמכרה ב-2.46 מיליון ש\"ח ברחוב זכרון יעקב", "deal", "UNSOURCED", "keep (one specific deal, page checked 6.6.2026)", rooms=4, official="city 4 rooms 2,444,100 (1-3.2026)")
C("tr@47980..50609", "טבלת טווח מחיר למ\"ר לפי שכונה (14 שורות)", "per_m2", "UNSOURCED", f"edit {e4}", figures=28, note="12 rows with no source marker; the two rows marked 'בהקשרים שנבדקו' repeat figures kept in the parameter and deals tables")
C("tr@49811", "מחנה יהודה | דירות 3 חדרים נבדקו סביב 1.5-1.9 מיליון ש\"ח", "sale_nb", "CONFLICT", f"edit {e4}", rooms=3, official="Mahane Yehuda 3 rooms 1,951,200 (1-3.2026)", figures=2)
C("tr@50036", "אחדות | דירות 3 חדרים סביב 1.6-2.1 מיליון ש\"ח בהקשר שוק", "sale_nb", "UNSOURCED", f"edit {e4}", rooms=3, official="Achdut: no official median", figures=2)
C("p@51244", "בדפי שכירות שנבדקו נראו 184-233 מודעות פעילות", "count", "UNSOURCED", "keep (listing sample, page checked 6.6.2026)", figures=2)
C("tr@51881..53795", "טבלת שכירות חודשית לדוגמה לפי שכונה (15 שורות)", "rent", "UNSOURCED", "keep (listing sample of 184-233 active listings, page checked 6.6.2026)", figures=15)
C("tr@55038", "רחוב זכרון יעקב, 4 חדרים | 86 מ\"ר ... 2.46 מיליון ש\"ח", "deal", "UNSOURCED", f"keep (one specific deal, page checked 6.6.2026; row kept word for word in edit {e6})", rooms=4, official="city 4 rooms 2,444,100")
C("tr@55277", "מחנה יהודה, דירות 3 חדרים | כ-1.5-1.9 מיליון ש\"ח", "sale_nb", "CONFLICT", f"edit {e6}", rooms=3, official="Mahane Yehuda 3 rooms 1,951,200 (1-3.2026)", figures=2)
C("tr@55489", "מחנה יהודה, מחיר למ\"ר | כ-20,000-24,000 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"keep (labelled as checked; row kept word for word in edit {e6})", figures=2)
C("tr@55697", "אחדות, דירות 3 חדרים | 70-80 מ\"ר סביב 1.6-2.1 מיליון ש\"ח", "sale_nb", "UNSOURCED", f"edit {e6}", rooms=3, official="Achdut: no official median", figures=2)
C("tr@55922", "אחדות, דירות 5 חדרים | כ-2.2-2.85 מיליון ש\"ח", "sale_nb", "UNSOURCED", f"edit {e6}", rooms=5, official="Achdut: no official median", figures=2)
C("tr@56132", "נפח עסקאות 5 חדרים באחדות | עלייה של כ-15% ברבעון 1 של 2026", "count", "UNSOURCED", f"edit {e6}", rooms=5, note="no named source; the official list publishes no deal counts")
C("tr@56388", "מרכז העיר לפי הקשר שוק | כ-25,000-26,000 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"keep (labelled market context, same figure as the parameter table; row kept word for word in edit {e6})", figures=2)
C("tr@56597", "אזורים סמוכים וחזקים יותר | כ-28,000-32,000 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"keep (same figure as the parameter table; row kept word for word in edit {e6})", figures=2)
C("tr@58477", "דירת יד שנייה משופצת | כ-5%-12% מעל דירה לא משופצת דומה", "sale_new_used", "UNSOURCED", f"edit {e7}", figures=2, note="tier 2")
C("tr@58690", "דירה חדשה לאחר אכלוס | כ-8%-18% מעל יד שנייה דומה", "sale_new_used", "UNSOURCED", f"edit {e8}", figures=2, note="tier 2")
C("tr@58913", "דירה על הנייר | כ-10%-22% לפי פרויקט ומועד", "sale_new_used", "UNSOURCED", f"edit {e9}", figures=2, note="tier 2")
C("p@64920", "FAQ ממוצע: טווח רחב של כ-1.5-4.2 מיליון ש\"ח ברוב הדירות הרגילות", "sale_avg", "CONSISTENT", "keep (dated market check 6.6.2026; official all-rooms median 2,441,100 inside)", rooms="all", official="2,441,100 (1-3.2026)", figures=2)
C("p@65222", "FAQ מ\"ר: 25,000-26,000 במרכז, 28,000-32,000 באזורים מבוקשים", "per_m2", "UNSOURCED", "keep (labelled as observed in the page's dated market check)", figures=4)
C("p@65537", "FAQ: דירת 3 חדרים נע סביב 1.55-2.25 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e10}", rooms=3, official="2,057,000", figures=2, note="restated as the median")
C("p@65537", "FAQ: במחנה יהודה נראו דוגמאות סביב 1.5-1.9 מיליון ש\"ח", "sale_nb", "CONFLICT", f"edit {e10}", rooms=3, official="Mahane Yehuda 1,951,200", figures=2)
C("p@65537", "FAQ: באחדות דירות 70-80 מ\"ר סביב 1.6-2.1 מיליון ש\"ח", "sale_nb", "UNSOURCED", f"edit {e10}", rooms=3, official="Achdut: no official median", figures=2)
C("p@65837", "FAQ: דירות 4 חדרים נבדקות לרוב סביב 2.15-3.15 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e11}", rooms=4, official="2,444,100", figures=2, note="restated as the median")
C("p@65837", "FAQ: 4 חדרים ברחוב זכרון יעקב ... נמכרה ב-2.46 מיליון ש\"ח", "deal", "UNSOURCED", "keep (one specific deal, page checked 6.6.2026)", rooms=4)
C("p@66136", "FAQ: דירות 5 חדרים ... כ-2.65-4.20 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e12}", rooms=5, official="3,322,600", figures=2, note="restated as the median")
C("p@66136", "FAQ: באחדות נראו הקשרים סביב 2.2-2.85 מיליון ש\"ח", "sale_nb", "UNSOURCED", f"edit {e12}", rooms=5, official="Achdut: no official median", figures=2)
C("p@66744", "FAQ: שכירות באם המושבות החדשה סביב 8,209 ש\"ח לחודש", "rent", "UNSOURCED", "keep (rent listing check, page checked 6.6.2026)")
C("p@67043", "FAQ: מרכז העיר סביב 25,000-26,000 ש\"ח למ\"ר", "per_m2", "UNSOURCED", "keep (labelled 'בדיקות שוק הצביעו', page checked 6.6.2026)", figures=2)
C("p@67326", "FAQ: הפער ממחיר מבוקש 2%-4% או 8%-12%", "other", "UNSOURCED", f"edit {e13}", figures=4, note="tier 2")

P.write(notes=(
    "Not audited as claims (illustrations and method numbers, not market statements): the 8-12 m2 / one-vs-two parking example (p@46975), "
    "the 10 m2 x 28,000 = 280,000 arithmetic example (p@56855), the comparison counts 10-15 / 4-8 deals (p@57112), the steps table working "
    "numbers including 'פער סביר יכול להיות 5%-15%' between comparables (tr@62678..63791), the 100,000-300,000 negotiation illustration "
    "(p@64623) and the 10-20 listings / 6-10 deals counts (p@67326). "
    "Per-m2 figures are kept only where the page ties them to its own dated public market check ('בדיקת שוק גלויה מ-6 ביוני 2026', usage note "
    "p@42858, and rows marked 'בהקשרים שנבדקו' / 'לפי הקשר שוק' / 'בדיקות שוק הצביעו'); the kind of source is generic, so this keep is "
    "borderline and can be revisited. The neighbourhood per-m2 table (12 of 14 rows unlabelled) is replaced by official neighbourhood medians. "
    "The Mahane Yehuda per-m2 range 20,000-24,000 comes from the same check whose 3-room range (1.5-1.9M) sits below the official 1,951,200; "
    "it is kept as labelled but is the weakest kept figure. "
    "Name mapping: page 'כפר גנים א'' / 'כפר גנים ב'' = official 'כפר גנים א' / 'כפר גנים ב'. The official 'הדר המושבות החדשה' is NOT mapped "
    "to the page's 'אם המושבות החדשה' (different names; shown as 'לא מוצג במחירון'); the official 'נווה עוז הירוקה' appears only in the 5-room FAQ. "
    "The remaining SUSPECT on p@42022 is a floor/ceiling span (1.5M for small old flats up to 4.2M for 5 rooms, new flats and demanded areas) "
    "that holds the official 5-room median 3,322,600; it is a heuristic false positive, kept as CONSISTENT. "
    "Official quirk: none sharp; 4 rooms moved 2,565,500 (10-12.2025) to 2,444,100 (1-3.2026)."))
