# -*- coding: utf-8 -*-
"""Rehovot (page 4591): body alignment with the official price list (1-3.2026). The list is not on the page yet; it will be added.
Data only. The page writes ₪ and the Hebrew gershayim ״ (מ״ר, ממ״ד); new text follows it."""
import re
from mk import Page

P = Page("rehovot-apartment-prices")

# ---------------- edits ----------------
# 1. the lead (answer paragraph): asking anchors by rooms and two 'city averages'
old1 = P.find("מחירי דירות ברחובות נעים כיום סביב כ-1.49 מיליון ₪ לדירת 2 חדרים,", "ורק אחר כך לעבור להשוואת עסקאות סגורות.")
tail1 = P.find("בשכירות, דירת 2 חדרים מבוקשת סביב 3,300 ₪,", "ורק אחר כך לעבור להשוואת עסקאות סגורות.")
assert old1.endswith(tail1)
new1 = ("מחירי דירות ברחובות, לפי נתוני רשות המסים לרבעון הראשון של 2026: חציון מחיר העסקה היה 1,921,100 ₪ לדירת 3 חדרים, "
        "2,345,500 ₪ לדירת 4 חדרים ו-3,290,000 ₪ לדירת 5 חדרים, ו-2,421,900 ₪ בכל סוגי הדירות. דירות 6 חדרים ומעלה, דירות חדשות "
        "ודירות באזורים מבוקשים יכולות להיות יקרות יותר. המחיר המבוקש למ״ר במודעות נע לרוב בין 23,000 ל-28,500 ₪, עם חריגות כלפי "
        "מעלה באזורים חדשים, סביב פארק המדע, רחובות המדע, אחוזת הנשיא וצפון העיר. " + tail1)
e1 = P.edit(old1, new1, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "rooms.all.latest", "page"], "CONFLICT",
            "Lead (answer paragraph): the 4-room asking anchor 2.50M is 6.6% above the official median 2,345,500 (1-3.2026); the city 'average' "
            "1.55M (a multi-year private database) and 2.55M (+5.3%) are replaced by the official all-rooms median 2,421,900. 3 rooms 1.95M and "
            "5 rooms 3.19M were consistent and are restated as medians; the 2-room and 6+-room asking anchors (no official series) are dropped. "
            "The per-m2 range is kept and labelled as asking; the rent sentence (97 listings, 6.6.2026) is kept word for word.")

# 2. the multi-year private-database average presented as the city average
old2 = P.find("רחובות היא עיר שבה מחיר דירה ממוצע לא מספר את כל הסיפור.", "והוא עשוי להשתנות עם עדכון המאגר.")
new2 = ("רחובות היא עיר שבה מחיר דירה ממוצע לא מספר את כל הסיפור. לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה "
        "ברחובות בכל סוגי הדירות היה 2,421,900 ₪, לעומת 2,287,600 ₪ ברבעון הראשון של 2025. מאגר פרטי רחב שנסמך על היסטוריית "
        "עסקאות מונה בעיר 41,822 עסקאות לאורך השנים ו-34 שכונות או אזורי משנה. הנתון הזה נותן עומק היסטורי, אך הוא אינו שומה, "
        "אינו מחליף בדיקה משפטית או שמאית, והוא עשוי להשתנות עם עדכון המאגר.")
e2 = P.edit(old2, new2, ["rooms.all.latest", "rooms.all.year_ago", "page"], "STALE",
            "The 1,549,879 'average flat price' is a multi-year average of a private database (41,822 deals over the years) far below the "
            "official all-rooms median 2,421,900 (1-3.2026). Replaced by the official median and its year-earlier quarter; the deal count stays "
            "as historic depth.")

# 3. 'recent databases': average 2,550,000 and the 1.55 vs 2.55 discussion
old3 = P.find("בצד השני, מאגרים עדכניים יותר של מודעות ועסקאות מציגים תמונה גבוהה יותר:", "פנטהאוזים ודירות יוקרה.")
new3 = ("בצד השני, מאגרים עדכניים יותר של מודעות ועסקאות מציגים מחיר למ״ר סביב 25,000 ₪ ו-1,737 עסקאות במאגר אחד. ממוצעים של "
        "מאגרים שונים יכולים להיות רחוקים זה מזה בלי שתהיה ביניהם סתירה: הפער יכול לנבוע משנים שונות, סוגי נכסים שונים, דירות ישנות "
        "מול חדשות, דירות קטנות מול גדולות, סינון חריגים, עסקאות לעומת מודעות, והאם נכללו בתים פרטיים, פנטהאוזים ודירות יוקרה. לכן "
        "נקודת הייחוס בעמוד הזה היא חציון מחיר העסקה לפי נתוני רשות המסים.")
e3 = P.edit(old3, new3, ["rooms.all.latest", "page"], "CONFLICT",
            "Average 2,550,000 of an unnamed recent database is 5.3% above the official all-rooms median 2,421,900 and is set against the "
            "multi-year 1.55M; both averages leave. The per-m2 figure (25,000) and the deal count (1,737) stay as listing/database context.")

# 4. neighbourhood averages of the multi-year private database
old4 = P.find("דוגמה לפערים ניתן לראות במאגר עסקאות פרטי רחב:", "מאשר מחיר שמבוסס על אלפי עסקאות.")
new4 = ("דוגמה לפערים ניתן לראות בנתוני רשות המסים לרבעון הראשון של 2026: חציון מחיר העסקה לדירת 4 חדרים היה 2,012,000 ₪ "
        "בשעריים, 2,342,400 ₪ בסלע, 2,356,000 ₪ בנווה אלון ו-2,557,200 ₪ ברחובות החדשה. מספר העסקאות בכל אזור חשוב לא פחות "
        "מהמחיר, כי חציון שמבוסס על עסקאות מעטות רגיש יותר להרכב הנכסים מאשר חציון שמבוסס על עסקאות רבות.")
e4 = P.edit(old4, new4, ["neighbourhoods[שעריים].rooms.4", "neighbourhoods[סלע].rooms.4", "neighbourhoods[נווה אלון].rooms.4",
                         "neighbourhoods[רחובות החדשה].rooms.4"], "STALE",
            "Seven all-rooms neighbourhood averages of the multi-year private database (e.g. Shaarayim 1,343,842, Neve Alon 1,297,737) presented "
            "as today's gaps; the official 4-room medians (1-3.2026) are far higher. Replaced by official medians for four page neighbourhoods.")

# 5. intro of the rooms table
old5 = P.find("הטבלה הבאה נותנת נקודת פתיחה לפי מחירי ביקוש שפורסמו בעיר ולפי אומדני דירות חדשות.", "או כאשר יש בעיה תכנונית, משפטית או תחזוקתית.")
new5 = ("הטבלה הבאה מציגה את חציון מחיר העסקה ברחובות לפי מספר חדרים, לפי נתוני רשות המסים לרבעון הראשון של 2026, לצד החציון "
        "באותו רבעון שנה קודם לכן. החציון אינו מחליף בדיקה של עסקאות דומות: בין מחיר ביקוש למחיר סגירה, ובין דירה לדירה, יכולים "
        "להיות פערים של עשרות אלפי שקלים ואף יותר, בעיקר כאשר הדירה עומדת זמן רב בשוק או כאשר יש בעיה תכנונית, משפטית או תחזוקתית.")
e5 = P.edit(old5, new5, ["rooms.4.latest", "rooms.4.year_ago"], "CONFLICT",
            "The intro announced asking prices and new-flat estimates; the table is replaced by official medians (edit 6).")

# 6. the rooms table
new6 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">סוג נכס</th>
<th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>
<th dir="rtl">ינואר-מרץ 2025</th>
<th dir="rtl">שינוי בשנה</th>
<th dir="rtl">מה לבדוק לפני שימוש במחיר</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">3 חדרים</td>
<td dir="rtl">1,921,100 ₪</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">התאמה לזוגות צעירים, מרחק לרכבת, מצב פנים הדירה וממ״ד</td>
</tr>
<tr dir="rtl">
<td dir="rtl">4 חדרים</td>
<td dir="rtl">2,345,500 ₪</td>
<td dir="rtl">2,518,800 ₪</td>
<td dir="rtl">ירידה של 6.9%</td>
<td dir="rtl">חניה, מעלית, מרפסת, בית ספר, דמי ועד ועסקאות דומות</td>
</tr>
<tr dir="rtl">
<td dir="rtl">5 חדרים</td>
<td dir="rtl">3,290,000 ₪</td>
<td dir="rtl">3,174,200 ₪</td>
<td dir="rtl">עלייה של 3.6%</td>
<td dir="rtl">קומה, נוף, מספר חניות, מחסן, שטח מרפסת ובניינים חדשים סמוכים</td>
</tr>
</tbody>
</table>"""
e6 = P.table('<th dir="rtl">מחיר ביקוש ממוצע משוער</th>', new6,
             ["rooms.3.latest", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct", "rooms.5.latest", "rooms.5.year_ago",
              "rooms.5.change_pct"], "CONFLICT",
             "Rooms table: the 4-room asking anchor 2,500,000 and the new-flat 'averages' 2,380,000 / 3,110,000 / 3,560,000 contradict the "
             "official medians; the 2-room and 6+-room rows and the per-m2 column are asking-based estimates with no named source. Replaced by "
             "the official medians with the year-earlier quarter (no 3-room median was published for 1-3.2025: 'לא פורסם'); the check notes "
             "of rows 3-5 are kept word for word.")

# 7. the sentence after the table pointed at the removed per-m2 column and the 2 / 6+ rows
old7 = "מחיר למ״ר גבוה בדירות 2 חדרים אינו מפתיע."
new7 = ("המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים ודירות 6 חדרים ומעלה כדאי לבדוק מול עסקאות דומות ברחוב "
        "ובשכונה. מחיר למ״ר גבוה בדירות 2 חדרים אינו מפתיע.")
e7 = P.edit(old7, new7, ["data_quarter"], "WORDING", "Follows edit 6: the 2-room and 6+-room rows and the per-m2 column left the table.")

# 8. '2.5 million for a 4-room flat' (the old asking anchor) in the cost paragraph
old8 = "מחיר של 2.5 מיליון ₪ לדירת 4 חדרים אינו אומר שהעלות הכוללת היא 2.5 מיליון ₪ בלבד."
new8 = "גם חציון מחיר העסקה לדירת 4 חדרים, 2,345,500 ₪ ברבעון הראשון של 2026, אינו העלות הכוללת של הקנייה."
e8 = P.edit(old8, new8, ["rooms.4.latest"], "CONFLICT", "Uses the old 4-room asking anchor 2.5M as the price of a 4-room flat; the official median is 2,345,500.")

# 9. intro of the neighbourhood table (wording)
old9 = "לכן מחיר ממוצע של שכונה הוא התחלה טובה, אך לא נקודת סיום."
new9 = ("לכן חציון המחיר של שכונה הוא התחלה טובה, אך לא נקודת סיום. הטבלה הבאה מציגה את חציון מחיר העסקה לפי שכונה ומספר חדרים, "
        "לפי נתוני רשות המסים לרבעון הראשון של 2026; בשכונות שאינן מופיעות במחירון, כמו רחובות המדע, אחוזת הנשיא, פארק תמר, מכון "
        "ויצמן, היובל ואושיות, משווים לעסקאות דומות ברחוב ובסביבה.")
e9 = P.edit(old9, new9, ["data_quarter"], "WORDING", "Follows edit 10: the neighbourhood table now shows official medians by rooms.")

# 10. neighbourhood table of the multi-year private database
new10 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">שכונה</th>
<th dir="rtl">3 חדרים</th>
<th dir="rtl">4 חדרים</th>
<th dir="rtl">5 חדרים</th>
<th dir="rtl">קריאת מחיר זהירה</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">שעריים</td>
<td dir="rtl">1,933,100 ₪</td>
<td dir="rtl">2,012,000 ₪</td>
<td dir="rtl">3,204,300 ₪</td>
<td dir="rtl">אזור ותיק עם היצע מגוון, יש לבדוק גיל בניין ורחוב ספציפי</td>
</tr>
<tr dir="rtl">
<td dir="rtl">נווה אלון</td>
<td dir="rtl">2,539,700 ₪</td>
<td dir="rtl">2,356,000 ₪</td>
<td dir="rtl">3,783,900 ₪</td>
<td dir="rtl">סוגי הנכסים אינם אחידים, יש להשוות לדירות דומות בגודל ובשנת בנייה</td>
</tr>
<tr dir="rtl">
<td dir="rtl">סלע</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">2,342,400 ₪</td>
<td dir="rtl">3,255,900 ₪</td>
<td dir="rtl">יש לבדוק האם ההשוואה היא לדירות דומות בגודל ובשנת בנייה</td>
</tr>
<tr dir="rtl">
<td dir="rtl">רחובות החדשה</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">2,557,200 ₪</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">בנייה חדשה יחסית בחלקים מהאזור, פערים לפי פרויקט ומפרט</td>
</tr>
<tr dir="rtl">
<td dir="rtl">מתחם התחנה המרכזית</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">3,389,400 ₪</td>
<td dir="rtl">נגישות עירונית טובה, אך יש לבדוק רעש, חניה ותכנון עתידי</td>
</tr>
<tr dir="rtl">
<td dir="rtl">קרית משה</td>
<td dir="rtl">2,238,200 ₪</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">2,762,400 ₪</td>
<td dir="rtl">סוג פרויקט, התחדשות, נגישות ומפרט</td>
</tr>
</tbody>
</table>"""
e10 = P.table('<th dir="rtl">מחיר ממוצע במאגר</th>', new10,
              ["neighbourhoods[שעריים].rooms.3", "neighbourhoods[שעריים].rooms.4", "neighbourhoods[שעריים].rooms.5",
               "neighbourhoods[נווה אלון].rooms.3", "neighbourhoods[נווה אלון].rooms.4", "neighbourhoods[נווה אלון].rooms.5",
               "neighbourhoods[סלע].rooms.4", "neighbourhoods[סלע].rooms.5", "neighbourhoods[רחובות החדשה].rooms.4",
               "neighbourhoods[מתחם התחנה המרכזית].rooms.5", "neighbourhoods[קרית משה].rooms.3", "neighbourhoods[קרית משה].rooms.5"], "STALE",
              "Neighbourhood table: 13 all-rooms averages and deal counts of a multi-year private database (e.g. Oshiyot 762,675 'historic', "
              "Shaarayim 1,343,842) presented as neighbourhood levels. Replaced by the official medians by rooms, 1-3.2026, for the six page "
              "neighbourhoods that have one ('לא פורסם' where the official file has no median). Check notes reused from the old rows (Neve Alon's "
              "note shortened, Kiryat Moshe's taken from the new-build table row).")

# 11. 2023 street averages and single deals
old11 = P.find("גם נתונים שנתיים לפי רחובות ממחישים תנודתיות.", "היא מספרת על הנכס שנמכר, לא על כל הרחוב.")
new11 = ("גם נתונים לפי רחובות ממחישים תנודתיות: באותו רחוב יכולות להיסגר עסקאות במחירים רחוקים זה מזה, ולכן כאשר יש עסקה אחת "
         "בלבד, היא מספרת על הנכס שנמכר, לא על כל הרחוב.")
e11 = P.edit(old11, new11, ["page"], "STALE",
             "2023 street averages (Carmel 5 deals 2,486,400; Har HaTsofim 3 deals 2,866,666) and five single 2023 deals from an unnamed annual "
             "source, older than the official data; rephrased without the numbers (the dated March 2026 deals table stays above).")

# 12. new-build table: drop the estimated price-range column, keep every row
anchor12 = '<th dir="rtl">טווח מחיר משוער</th>'
old12 = P.table_html(anchor12)
rows = old12.split("</tr>")
new_rows = []
for r in rows:
    cells = re.findall(r"\n<t[hd] dir=\"rtl\">.*?</t[hd]>", r)
    if len(cells) == 3:
        r = r.replace(cells[1], "", 1)
    new_rows.append(r)
new12 = "</tr>".join(new_rows).replace('<th dir="rtl">מה משפיע על הטווח</th>', '<th dir="rtl">מה משפיע על המחיר</th>')
assert new12.count("<td dir") == 6 * 2 and new12.count("<th dir") == 2 and "מיליון" not in new12, new12
e12 = P.table(anchor12, new12, ["page"], "UNSOURCED",
              "New-build table: six 'estimated' price ranges by area (1.7-2.2M ... 2.4-3.3M) with no room count, no named source and no period; "
              "the official list does not split new and second-hand. The range column is removed; rows and notes stay ('הטווח' -> 'המחיר' in the header).")

# 13. new-flat estimates by rooms and the 4-room asking anchor
old13 = P.find("לפי אומדן דירות חדשות, דירת 2 חדרים חדשה ברחובות עומדת סביב 1,780,000 ₪,", "אך היא דורשת בדיקה כלכלית ומשפטית.")
new13 = ("המחירון הרשמי אינו מפריד בין דירות חדשות לדירות יד שנייה. לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה "
         "לדירת 4 חדרים בעיר היה 2,345,500 ₪, ודירת קבלן חדשה באותו גודל מתומחרת לרוב מעליו, לפי המיקום והמפרט. הפרמיה עשויה להיות "
         "מוצדקת כאשר מדובר במיקום חזק, מפרט מלא, שתי חניות או פרויקט איכותי, אך היא דורשת בדיקה כלכלית ומשפטית.")
e13 = P.edit(old13, new13, ["rooms.4.latest"], "CONFLICT",
             "New-flat 'estimates' 2,380,000 / 3,110,000 / 3,560,000 for 3/4/5 rooms are far above the official medians, and the 4-room asking "
             "anchor 2,500,000 is 6.6% above 2,345,500; no source or period. Rephrased around the official 4-room median.")

# 14. historic averages of Rehovot HaMada, Ahuzat HaNasi, Park Tamar
old14 = "ברחובות המדע נרשם במאגר פרטי ממוצע של 3,555,117 ₪, באחוזת הנשיא 2,212,740 ₪ ובפארק תמר 3,877,475 ₪, אך צריך לשים לב למספר העסקאות ולהרכב הנכסים."
new14 = ("ברחובות המדע, באחוזת הנשיא ובפארק תמר הופיעו במאגר פרטי היסטורי ממוצעים גבוהים מהממוצע העירוני באותו מאגר, אך המחירון שבעמוד אינו "
         "מציג להם חציון, וצריך לשים לב למספר העסקאות ולהרכב הנכסים.")
e14 = P.edit(old14, new14, ["page"], "STALE",
             "All-rooms averages of the multi-year private database; no official median for these areas. Rephrased without the numbers.")

# 15. FAQ 4 rooms
old15 = "נקודת פתיחה סבירה לדירת 4 חדרים ברחובות היא סביב 2,500,000 ₪ במחירי ביקוש, עם מחיר למ״ר סביב 23,364 ₪. דירה חדשה יכולה להגיע סביב 3,110,000 ₪ בממוצע."
new15 = "לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים ברחובות ברבעון הראשון של 2026 היה 2,345,500 ₪, לעומת 2,518,800 ₪ שנה קודם לכן."
e15 = P.edit(old15, new15, ["rooms.4.latest", "rooms.4.year_ago"], "CONFLICT",
             "FAQ 4 rooms: asking 2,500,000 and new 3,110,000 vs the official 2,345,500 (1-3.2026); the asking per-m2 23,364 leaves with the table column.")

# 16. FAQ 3 rooms
old16 = "דירת 3 חדרים מוצעת סביב 1,950,000 ₪ בממוצע ביקוש, עם מחיר למ״ר סביב 24,375 ₪. דירה חדשה בת 3 חדרים נאמדת סביב 2,380,000 ₪."
new16 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים ברחובות ברבעון הראשון של 2026 היה 1,921,100 ₪. ברבעון הרביעי של "
         "2025 הוא היה 1,621,600 ₪, ולכן כדאי להשוות גם לעסקאות מהרבעונים הקודמים.")
e16 = P.edit(old16, new16, ["rooms.3.latest", "rooms.3.quarters[10-12.2025]"], "CONFLICT",
             "FAQ 3 rooms: the asking 1,950,000 was consistent, but the new-flat 2,380,000 contradicts the official 1,921,100; no year-earlier "
             "median exists for 3 rooms, so the previous quarter (1,621,600, a sharp swing) is shown.")

# 17. FAQ 'average price'
old17 = P.find("יש כמה מספרים אפשריים. מאגר פרטי רחב מציג מחיר ממוצע היסטורי של 1,549,879 ₪", "הפער נובע מתמהיל נתונים, שנים, סוגי נכסים וסינון עסקאות.")
new17 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה ברחובות בכל סוגי הדירות היה 2,421,900 ₪. מאגרים פרטיים "
         "מציגים ממוצעים אחרים, למשל ממוצע היסטורי על בסיס 41,822 עסקאות לאורך השנים, והפער נובע מתמהיל נתונים, שנים, סוגי נכסים "
         "וסינון עסקאות. מאגר עדכני של מודעות ועסקאות מציג מחיר למ״ר סביב 25,000 ₪.")
e17 = P.edit(old17, new17, ["rooms.all.latest", "page"], "STALE",
             "FAQ average: the multi-year 1,549,879 and the 2,550,000 of another database vs the official all-rooms median 2,421,900 (1-3.2026). "
             "The per-m2 25,000 and the 41,822 deal count stay as context.")

# 18. FAQ: pricier neighbourhoods (historic averages)
old18 = P.find("אזורים כמו רחובות המדע, פארק תמר, מכון ויצמן ואחוזת הנשיא מציגים במאגרים פרטיים מחירים ממוצעים גבוהים יותר,", "ולכן חובה לבדוק נכסים דומים.")
new18 = ("אזורים כמו רחובות המדע, פארק תמר, מכון ויצמן ואחוזת הנשיא מציגים במאגרים פרטיים היסטוריים מחירים ממוצעים גבוהים יותר, "
         "אך המחירון שבעמוד אינו מציג להם חציון, ומספר העסקאות בחלק מהם קטן יחסית. בין השכונות שבמחירון, חציון מחיר העסקה לדירת 4 "
         "חדרים ברחובות החדשה היה 2,557,200 ₪ ברבעון הראשון של 2026, לפי נתוני רשות המסים. בכל מקרה חובה לבדוק נכסים דומים.")
e18 = P.edit(old18, new18, ["neighbourhoods[רחובות החדשה].rooms.4", "page"], "STALE",
             "FAQ: 3,555,117 / 3,877,475 / 2,212,740 are multi-year private-database averages; no official median for these areas. Rephrased "
             "without them; the official 4-room median of Rehovot HaHadasha is given.")

# 19. FAQ: older neighbourhoods cheaper?
old19 = "אזורים ותיקים כמו שעריים, נווה אלון, היובל ואושיות כוללים נתונים ממוצעים נמוכים יותר במאגרים היסטוריים."
new19 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 4 חדרים בשעריים היה 2,012,000 ₪, מתחת לחציון העירוני "
         "של 2,345,500 ₪, אך בנווה אלון הוא היה 2,356,000 ₪, כמעט כמו החציון העירוני.")
e19 = P.edit(old19, new19, ["neighbourhoods[שעריים].rooms.4", "rooms.4.latest", "neighbourhoods[נווה אלון].rooms.4"], "STALE",
             "FAQ: 'lower averages in historic databases' for Shaarayim, Neve Alon, HaYovel, Oshiyot; the official 4-room medians show Shaarayim "
             "below the city median but Neve Alon at the city level.")

# ---------------- claims inventory ----------------
C = P.claim
ALL = "all rooms 2,421,900 (1-3.2026)"
C("p@4303", "דירת 2 חדרים כ-1.49 מיליון ₪ (מחירי ביקוש)", "sale", "UNSOURCED", f"edit {e1}", rooms=2, note="no official 2-room series; dropped")
C("p@4303", "דירת 3 חדרים כ-1.95 מיליון ₪", "sale", "CONSISTENT", f"edit {e1}", rooms=3, official="1,921,100 (1-3.2026), +1.5%", note="restated as the median")
C("p@4303", "דירת 4 חדרים כ-2.50 מיליון ₪", "sale", "CONFLICT", f"edit {e1}", rooms=4, official="2,345,500 (1-3.2026), +6.6%")
C("p@4303", "דירת 5 חדרים כ-3.19 מיליון ₪", "sale", "CONSISTENT", f"edit {e1}", rooms=5, official="3,290,000 (1-3.2026), -3.0%", note="restated as the median")
C("p@4303", "דירות 6 חדרים ומעלה כ-4.88 מיליון ₪", "sale", "UNSOURCED", f"edit {e1}", rooms=6, note="no official series; dropped")
C("p@4303", "ממוצע בעיר בין כ-1.55 מיליון (מאגר רב-שנתי) לכ-2.55 מיליון (מאגר עדכני)", "sale_avg", "CONFLICT", f"edit {e1}", figures=2,
  official=ALL, note="1.55M is a multi-year average; 2.55M is +5.3%")
C("p@4303", "מחיר למ״ר בדירות רגילות סביב 23,000-28,500 ₪", "per_m2", "UNSOURCED", "keep (asking data, page checked 6.6.2026; relabelled as asking inside edit 1)", figures=2)
C("p@4303", "שכירות 2/3/4/5 חדרים 3,300 / 4,900 / 5,700 / 7,950; חציון 4,500, ממוצע 4,987", "rent", "UNSOURCED", "keep (listing sample, 97 listings, 6.6.2026)", figures=6)
C("p@5257", "מאגר פרטי: מחיר דירה ממוצע 1,549,879 ₪ (41,822 עסקאות לאורך השנים)", "sale_avg", "STALE", f"edit {e2}", official=ALL)
C("p@5257", "41,822 עסקאות ו-34 שכונות במאגר פרטי", "count", "UNSOURCED", "keep (count, labelled historic depth of a private database)", figures=2)
C("p@5587", "מאגרים עדכניים: מחיר ממוצע סביב 2,550,000 ₪ (והפער מול 1.55 מיליון)", "sale_avg", "CONFLICT", f"edit {e3}", official="all rooms 2,421,900 (1-3.2026), +5.3%")
C("p@5587", "מחיר למ״ר סביב 25,000 ₪; 1,737 עסקאות במאגר אחד", "per_m2", "UNSOURCED", "keep (recent listing/deal databases, page checked 6.6.2026)", figures=2)
C("p@7692", "ממוצעי שכונה במאגר פרטי: שעריים 1,343,842 ... מכון ויצמן 3,490,123 (7 אזורים)", "sale_nb", "STALE", f"edit {e4}", figures=7,
  official="4 rooms: שעריים 2,012,000; סלע 2,342,400; נווה אלון 2,356,000; רחובות החדשה 2,557,200 (1-3.2026)", note="multi-year all-rooms averages")
C("tr@9507", "2 חדרים | 1,485,000 | 28,558 למ״ר | חדשה 1,780,000", "sale", "UNSOURCED", f"edit {e6}", rooms=2, figures=3)
C("tr@9728", "3 חדרים | מחיר ביקוש 1,950,000 ₪", "sale", "CONSISTENT", f"edit {e6}", rooms=3, official="1,921,100 (1-3.2026)")
C("tr@9728", "3 חדרים | 24,375 ₪ למ״ר משוער", "per_m2", "UNSOURCED", f"edit {e6}", rooms=3, note="column removed")
C("tr@9728", "3 חדרים | דירה חדשה ממוצעת 2,380,000 ₪", "sale_new_used", "CONFLICT", f"edit {e6}", rooms=3, official="1,921,100 (1-3.2026)")
C("tr@9944", "4 חדרים | מחיר ביקוש 2,500,000 ₪", "sale", "CONFLICT", f"edit {e6}", rooms=4, official="2,345,500 (1-3.2026)")
C("tr@9944", "4 חדרים | 23,364 ₪ למ״ר משוער", "per_m2", "UNSOURCED", f"edit {e6}", rooms=4)
C("tr@9944", "4 חדרים | דירה חדשה ממוצעת 3,110,000 ₪", "sale_new_used", "CONFLICT", f"edit {e6}", rooms=4, official="2,345,500 (1-3.2026)")
C("tr@10157", "5 חדרים | מחיר ביקוש 3,190,000 ₪", "sale", "CONSISTENT", f"edit {e6}", rooms=5, official="3,290,000 (1-3.2026)")
C("tr@10157", "5 חדרים | 24,167 ₪ למ״ר משוער", "per_m2", "UNSOURCED", f"edit {e6}", rooms=5)
C("tr@10157", "5 חדרים | דירה חדשה ממוצעת 3,560,000 ₪", "sale_new_used", "CONFLICT", f"edit {e6}", rooms=5, official="3,290,000 (1-3.2026)")
C("tr@10380", "6 חדרים ומעלה | 4,880,000 | 19,520 למ״ר", "sale", "UNSOURCED", f"edit {e6}", rooms=6, figures=2)
C("p@10976", "מחיר של 2.5 מיליון ₪ לדירת 4 חדרים", "sale", "CONFLICT", f"edit {e8}", rooms=4, official="2,345,500 (1-3.2026)", note="echoes the table's asking anchor")
C("tr@12299..14282", "טבלת שכונות: מספר עסקאות וממוצע במאגר פרטי (13 שורות)", "sale_nb", "STALE", f"edit {e10}", figures=13,
  note="multi-year all-rooms averages; deal counts leave with them")
C("tr@15834..16611", "טבלת שכירות: 3,300 / 4,900 (חציון 4,814) / 5,700 / 7,950; ממוצע מבוקש 5,425; חציון 4,500 וממוצע 4,987", "rent", "UNSOURCED",
  "keep (listing data, 97 listings dated 6.6.2026)", figures=8)
C("p@16847", "97 מודעות נכון ל-6 ביוני 2026: חציון 4,500, ממוצע 4,987, 3 חדרים 4,814, ארצי 4,400, אבני חן 1,920, רחובות הצעירה 10,200", "rent",
  "UNSOURCED", "keep (listing sample, dated 6.6.2026)", figures=6)
C("p@17256", "ריבית בנק ישראל 3.75%, החלטה מ-25 במאי 2026", "macro", "UNSOURCED", "keep (dated Bank of Israel decision)")
C("tr@18617..20314", "טבלת עסקאות (10 עסקאות, 25.2-19.3.2026) עם מחיר למ״ר", "deal", "UNSOURCED", "keep (individual dated deals)", figures=10)
C("p@20521", "מחיר למ״ר בעסקאות: 18,966 / 29,688 (3 חדרים); 22,300 / 25,000 / 25,814 / 26,667 (4 חדרים)", "per_m2", "UNSOURCED",
  "keep (computed from the dated deals in the table)", figures=6)
C("p@20888", "2023: כרמל 5 עסקאות ממוצע 2,486,400; הר הצופים 3 עסקאות 2,866,666; 5 עסקאות בודדות", "sale_street", "STALE", f"edit {e11}", figures=7,
  note="2023, unnamed annual source")
C("tr@22149..22933", "טבלת דירות קבלן לפי אזור: 1.7-2.2 ... 2.4-3.3 מיליון (6 שורות)", "sale_new_used", "UNSOURCED", f"edit {e12}", figures=6,
  note="'estimated', no room count, no source")
C("p@23109", "אומדן דירות חדשות: 3 חדרים 2,380,000, 4 חדרים 3,110,000, 5 חדרים 3,560,000", "sale_new_used", "CONFLICT", f"edit {e13}", figures=3,
  official="3/4/5 rooms 1,921,100 / 2,345,500 / 3,290,000 (1-3.2026)")
C("p@23109", "אומדן דירה חדשה 2 חדרים 1,780,000", "sale_new_used", "UNSOURCED", f"edit {e13}", rooms=2)
C("p@23109", "מחיר ביקוש כללי סביב 2,500,000 ₪ לדירת 4 חדרים", "sale", "CONFLICT", f"edit {e13}", rooms=4, official="2,345,500 (1-3.2026)")
C("p@23568", "מאגר פרטי: רחובות המדע 3,555,117, אחוזת הנשיא 2,212,740, פארק תמר 3,877,475", "sale_nb", "STALE", f"edit {e14}", figures=3,
  note="multi-year all-rooms averages; no official median for these areas")
C("p@27388", "FAQ 4 חדרים: ביקוש סביב 2,500,000 ₪; דירה חדשה סביב 3,110,000 ₪", "sale", "CONFLICT", f"edit {e15}", rooms=4, figures=2, official="2,345,500 (1-3.2026)")
C("p@27388", "FAQ 4 חדרים: מחיר למ״ר סביב 23,364 ₪", "per_m2", "UNSOURCED", f"edit {e15}", rooms=4)
C("p@27728", "FAQ 3 חדרים: ביקוש סביב 1,950,000 ₪", "sale", "CONSISTENT", f"edit {e16}", rooms=3, official="1,921,100 (1-3.2026)")
C("p@27728", "FAQ 3 חדרים: מחיר למ״ר סביב 24,375 ₪", "per_m2", "UNSOURCED", f"edit {e16}", rooms=3)
C("p@27728", "FAQ 3 חדרים: דירה חדשה נאמדת סביב 2,380,000 ₪", "sale_new_used", "CONFLICT", f"edit {e16}", rooms=3, official="1,921,100 (1-3.2026)")
C("p@28018", "FAQ ממוצע: היסטורי 1,549,879 (41,822 עסקאות)", "sale_avg", "STALE", f"edit {e17}", official=ALL)
C("p@28018", "FAQ ממוצע: מאגר עדכני סביב 2,550,000 ₪", "sale_avg", "CONFLICT", f"edit {e17}", official="all rooms 2,421,900 (1-3.2026), +5.3%")
C("p@28018", "FAQ: מחיר למ״ר סביב 25,000 ₪", "per_m2", "UNSOURCED", f"edit {e17}", note="kept inside the rewrite (recent listing/deal database)")
C("p@28338", "FAQ: רחובות המדע 3,555,117, פארק תמר 3,877,475, אחוזת הנשיא 2,212,740", "sale_nb", "STALE", f"edit {e18}", figures=3)
C("p@28676", "FAQ: שעריים, נווה אלון, היובל ואושיות 'נמוכים יותר במאגרים היסטוריים'", "sale_nb", "STALE", f"edit {e19}",
  official="4 rooms: שעריים 2,012,000; נווה אלון 2,356,000; city 2,345,500 (1-3.2026)", note="no digit; points at the historic database averages")
C("p@29038", "FAQ שכירות: 3,300 / 4,900 / 5,700 / 7,950; חציון 4,500, ממוצע 4,987", "rent", "UNSOURCED", "keep (listing sample, 6.6.2026)", figures=6)
C("p@29716", "FAQ למ״ר: 18,966 / 22,300 / 25,000 / 26,667 / 29,688", "per_m2", "UNSOURCED", "keep (computed from the dated deals in the table)", figures=5)

P.write(notes=(
    "The official price list is not on this page yet; these edits assume it will be added near the top, as on the other city pages. "
    "Not audited as claims (illustrations or structure): the if-example 'a regular 4-room flat asked at about 2.5M while similar deals closed "
    "at 2.2-2.4M' (p@26287; it is an explicit 'לדוגמה, אם' and the closed range contains the official median), '3-5 rooms' (p@8310), 10 m2 "
    "(p@18083), step counts (5-8 deals, 10-15 listings), the CBS release 081/2026 and the 25.5.2026 rate decision named without figures "
    "(p@27055). No SUSPECT line remains after the edits; the if-example p@26287 (2.5M for 4 rooms) passes the scan only because 2.5 "
    "rounds an official figure, and it stays as an explicit hypothetical. Official quirks: 3 rooms has no "
    "1-3.2025 median (year_ago empty, so the rooms table shows 'לא פורסם' and the FAQ shows the previous quarter instead), and the 3-room series "
    "swings hard (2,123,000 in 4-6.2025, 1,621,600 in 10-12.2025, 1,921,100 in 1-3.2026); Neve Alon 3 rooms (2,539,700) is above Neve Alon "
    "4 rooms (2,356,000), shown as published in the table but not quoted in the text. Name mapping: page 'שעריים', 'נווה אלון', 'סלע', "
    "'רחובות החדשה', 'מתחם התחנה המרכזית', 'קרית משה' = official names exactly. The official 'אייזנבר\\ אהרוני' and 'בנימין\\ נורדאו' "
    "(truncated names with a backslash) are not on the page and were not added. The kept per-m2 range 23,000-28,500 is labelled 'asking' "
    "because the page built it from asking prices (the old table's per-m2 column)."))
