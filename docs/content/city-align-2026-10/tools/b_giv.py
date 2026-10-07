# -*- coding: utf-8 -*-
"""Givatayim (page 4571): body alignment with the official price list (1-3.2026). Built on the gold example b_ashkelon.py."""
from mk import Page

P = Page("givatayim-apartment-prices")

# ---------------- edits ----------------
# 1. the lead paragraph
# (the paragraph opens with a bold '...ורק אחר כך בפרשנות:' that stays; the old starts after the </strong>)
old1 = P.find("בדיקת נתוני שוק גלויים מ-5 ביוני 2026 מציגה פער גדול", "וממוצע עירוני אחד עלול להטעות.")
new1 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה היה 2,815,300 ש\"ח לדירת 3 חדרים, 4,158,900 ש\"ח לדירת 4 חדרים ו-4,960,000 ש\"ח לדירת 5 חדרים. גם שכירות חציונית "
        "במודעות, סביב 6,000 ש\"ח לחודש, עוזרת לבדוק אם מחיר הדירה הגיוני, אבל גבעתיים אינה שוק אחד: בורוכוב, שינקין, ארלוזורוב, "
        "גבעת רמב\"ם, הל\"ה, פועלי הרכבת, תל גנים, סיטי, קריית יוסף וכיסים חדשים או יקרים מתנהגים אחרת. מחיר מבוקש אינו מחיר סגירה, "
        "והחציון העירוני הוא נקודת ייחוס ולא מחיר לדירה מסוימת.")
e1 = P.edit(old1, new1, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
            "Lead: the 4-room working range 3.1-3.6M excludes the official median 4,158,900 (1-3.2026), and the 'city averages 2.85-4.35M' "
            "are two sources' averages (2,847,355 and 4,350,000), each about 20% from the official all-deals median 3,635,300. The 3-room "
            "2.4-2.9M range and the 5-room floor 4.3M were consistent. All restated as the official medians. Rent: the 6,000 listing median "
            "(dedicated rent page, June 2026, same page) is kept and labelled; the untraceable 6,500 top is dropped.")

# 2. the 'working range for price' box
old2 = "בדפי נתוני שוק שנבדקו הופיעו ממוצעים עירוניים של כ-2.85-4.35 מיליון ש\"ח. הטווח הרחב נובע מהבדלי שטח, גיל בניין, חניה, ממ\"ד, קומה, מעלית, רחוב ואזור."
new2 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה בגבעתיים בכל העסקאות היה 3,635,300 ש\"ח. המחיר של דירה "
        "מסוימת יכול להיות רחוק ממנו בגלל הבדלי שטח, גיל בניין, חניה, ממ\"ד, קומה, מעלית, רחוב ואזור.")
e2 = P.edit(old2, new2, ["rooms.all.latest"], "CONFLICT",
            "Box under 'טווח עבודה למחיר': the two city averages 2.85M and 4.35M are each about 20% from the official all-deals median 3,635,300.")

# 3. the two-sources paragraph
old3 = P.find("הנתונים שנבדקו מציגים כמה שכבות.", "צריך להיות טווח עבודה ולא שומה.")
new3 = ("הנתונים שנבדקו מציגים כמה שכבות. לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה בגבעתיים בכל העסקאות היה "
        "3,635,300 ש\"ח. בדפי נתוני שוק גלויים הופיע מחיר למ\"ר של כ-31,856 ש\"ח, ובמקור אחר כ-42,000 ש\"ח למ\"ר. הפער אינו בהכרח סתירה: "
        "מקור אחד יכול לכלול יותר עסקאות קטנות וישנות, ומקור אחר יכול לתת משקל גבוה יותר לדירות גדולות, חדשות או יקרות יותר. לכן "
        "החציון הוא נקודת ייחוס ולא שומה.")
e3 = P.edit(old3, new3, ["rooms.all.latest", "page"], "CONFLICT",
            "City averages 2,847,355 (-21.7%) and 4,350,000 (+19.7%) vs the official all-deals median 3,635,300 (1-3.2026). Replaced by the "
            "median; the two per-m2 figures (market pages checked 5.6.2026) are kept.")

# 4. the 'indicator' table
new4 = """<table dir="rtl">
  <thead dir="rtl">
    <tr dir="rtl">
      <th dir="rtl">מדד שנבדק</th>
      <th dir="rtl">אינדיקציה מספרית</th>
      <th dir="rtl">איך להשתמש במספר</th>
    </tr>
  </thead>
  <tbody dir="rtl">
    <tr dir="rtl">
      <td dir="rtl">חציון מחיר העסקה בעיר, כל העסקאות, ינואר-מרץ 2026</td>
      <td dir="rtl">3,635,300 ש"ח</td>
      <td dir="rtl">מתאים לפתיחת בדיקה בלבד, כי תמהיל הדירות הקטנות, הוותיקות, הגדולות והחדשות משפיע עליו.</td>
    </tr>
    <tr dir="rtl">
      <td dir="rtl">חציון מחיר העסקה לדירת 4 חדרים, ינואר-מרץ 2026</td>
      <td dir="rtl">4,158,900 ש"ח</td>
      <td dir="rtl">נקודת ייחוס לדירת 4 חדרים, לפני התאמה לשטח, לקומה, לחניה ולרחוב.</td>
    </tr>
    <tr dir="rtl">
      <td dir="rtl">מחיר למ"ר לפי מקור רחב</td>
      <td dir="rtl">כ-31,856 ש"ח</td>
      <td dir="rtl">נקודת ייחוס כללית בלבד, לא מספר סגירה לדירה ספציפית.</td>
    </tr>
    <tr dir="rtl">
      <td dir="rtl">מחיר למ"ר לפי מקור עסקאות אחר</td>
      <td dir="rtl">כ-42,000 ש"ח</td>
      <td dir="rtl">מתאים לבדיקה זהירה כאשר הדירה קרובה לאזורי ביקוש או בעלת מאפיינים חזקים.</td>
    </tr>
    <tr dir="rtl">
      <td dir="rtl">שכירות חציונית</td>
      <td dir="rtl">כ-6,000 ש"ח</td>
      <td dir="rtl">בדיקת סבירות לתמחור, במיוחד בדירות 2-4 חדרים.</td>
    </tr>
  </tbody>
</table>"""
e4 = P.table('<th dir="rtl">אינדיקציה מספרית</th>', new4, ["rooms.all.latest", "rooms.4.latest", "page"], "CONFLICT",
             "Indicator table: the two city-average rows (2,847,355 and 4,350,000) conflict with the official all-deals median 3,635,300, and the "
             "'4 rooms in a market calculator' row (3.32M, shown range 3.05-3.59M) conflicts with the official 4-room median 4,158,900. Those three "
             "rows become the two official medians; the per-m2 rows and the rent-median row are kept word for word.")

# 5. the intro of the rooms table
old5 = P.find("בטבלה הבאה מופיעים טווחי עבודה על בסיס דפי נתוני שוק גלויים", "התחדשות עירונית או עסקה חריגה.")
new5 = ("בטבלה הבאה מופיע חציון מחיר העסקה לפי מספר חדרים, לפי נתוני רשות המסים לרבעון הראשון של 2026, לצד שטח אופייני ומחיר "
        "למ\"ר מדפי נתוני שוק גלויים שנבדקו ב-5 ביוני 2026. המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים ודירות "
        "3.5 חדרים כדאי לבדוק מול עסקאות דומות ברחוב ובשכונה. הנתונים נועדו לסייע לקונה, מוכר או בעל נכס להתחיל בדיקת שוק, ולא "
        "להחליף בדיקת עסקאות או הערכת שווי מקצועית. כאשר המחיר המבוקש רחוק מהחציון, אין פירוש הדבר שהוא שגוי, אבל צריך להסביר את "
        "הפער באמצעות נתונים: רחוב, בניין, מצב, חניה, מרפסת, התחדשות עירונית או עסקה חריגה.")
e5 = P.edit(old5, new5, ["data_quarter", "page"], "WORDING", "Follows edit 6: the table now leads with the official medians.", kept=["3.5"])

# 6. the rooms table
new6 = """<table dir="rtl">
  <thead dir="rtl">
    <tr dir="rtl">
      <th dir="rtl">סוג דירה</th>
      <th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>
      <th dir="rtl">שטח אופייני שנצפה</th>
      <th dir="rtl">מחיר למ"ר שנצפה</th>
      <th dir="rtl">הערת בדיקה</th>
    </tr>
  </thead>
  <tbody dir="rtl">
    <tr dir="rtl">
      <td dir="rtl">2 חדרים</td>
      <td dir="rtl">לא פורסם</td>
      <td dir="rtl">כ-56 מ"ר</td>
      <td dir="rtl">כ-33,223 ש"ח למ"ר</td>
      <td dir="rtl">נבדקו 563 עסקאות באחד מדפי השוק, במחיר ממוצע של כ-1,833,563 ש"ח. בדירות קטנות יש רגישות גבוהה לקומה, מעלית ומצב הבניין.</td>
    </tr>
    <tr dir="rtl">
      <td dir="rtl">3 חדרים</td>
      <td dir="rtl">2,815,300 ש"ח</td>
      <td dir="rtl">כ-65-83 מ"ר</td>
      <td dir="rtl">כ-32,070 ש"ח למ"ר ומעלה</td>
      <td dir="rtl">בדוגמאות 2026 הופיעו עסקאות סביב 2.42, 2.70, 2.717 ו-3.00 מיליון ש"ח.</td>
    </tr>
    <tr dir="rtl">
      <td dir="rtl">3.5 חדרים</td>
      <td dir="rtl">לא פורסם</td>
      <td dir="rtl">כ-80-93 מ"ר</td>
      <td dir="rtl">כ-30,000-36,000 ש"ח למ"ר לפי עסקה</td>
      <td dir="rtl">עסקאות 2026 שנצפו: כ-2,870,000-3,010,000 ש"ח. דירות 3.5 חדרים דורשות בדיקת תכנון: חצי חדר שימושי, מרפסת, חניה ויכולת השבחה.</td>
    </tr>
    <tr dir="rtl">
      <td dir="rtl">4 חדרים</td>
      <td dir="rtl">4,158,900 ש"ח</td>
      <td dir="rtl">כ-88-117 מ"ר</td>
      <td dir="rtl">כ-31,704-42,000 ש"ח למ"ר</td>
      <td dir="rtl">דוגמאות שוק הציגו 3.15, 3.20, 3.50, 3.85, 4.10 ו-5.03 מיליון ש"ח לפי רחוב וגודל.</td>
    </tr>
    <tr dir="rtl">
      <td dir="rtl">5 חדרים</td>
      <td dir="rtl">4,960,000 ש"ח</td>
      <td dir="rtl">כ-112-159 מ"ר</td>
      <td dir="rtl">כ-32,829 ש"ח למ"ר ומעלה</td>
      <td dir="rtl">טווח המחירים מושפע מאוד מדירות חדשות, חניה כפולה, מרפסת, נוף ותכנון משפחתי.</td>
    </tr>
  </tbody>
</table>"""
e6 = P.table('<th dir="rtl">אינדיקציית מחיר</th>', new6, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
             "Rooms table: the 4-room indication 3,096,234-3,600,000 excludes the official median 4,158,900 (1-3.2026); the 3-room "
             "(2,401,393-2,900,000) and 5-room (4,150,000-5,030,000) indications were consistent. The indication column becomes the official "
             "median ('לא פורסם' for 2 and 3.5 rooms). The 2-room market average (563 deals, market page checked 5.6.2026) and the 3.5-room range "
             "of dated 2026 deals move into the check note; size, per-m2 and the other notes are kept word for word.")

# 7. the intro of the area table
old7 = "בטבלת האזורים מופיעים נתונים שהוזכרו בדפי שוק גלויים לצד דוגמאות רחוב."
new7 = ("בטבלת האזורים מופיעים חציוני מחיר העסקה לפי נתוני רשות המסים לרבעון הראשון של 2026 בבורוכוב ובארלוזורוב, לצד נתונים "
        "שהוזכרו בדפי שוק גלויים ודוגמאות רחוב.")
e7 = P.edit(old7, new7, ["data_quarter"], "WORDING", "Follows edits 8 and 9: two rows of the area table now carry official neighbourhood medians.")

# 8-9. area table: Borochov and Arlozorov all-rooms indications -> official neighbourhood medians by rooms
old8 = "כ-3,950,000 ש\"ח"
new8 = "חציון מחיר העסקה, ינואר-מרץ 2026: 3,206,100 ש\"ח לדירת 3 חדרים, 4,356,800 ש\"ח לדירת 4 חדרים"
e8 = P.edit(old8, new8, ["neighbourhoods[בורוכוב].rooms.3", "neighbourhoods[בורוכוב].rooms.4"], "UNSOURCED",
            "Area table, Borochov: an all-rooms 'observed indication' of 3,950,000 with no room count; replaced by the official Borochov "
            "medians by rooms (1-3.2026). The per-m2 cell (market pages) is kept.")
old9 = "כ-3,200,000 ש\"ח"
new9 = ("חציון מחיר העסקה, ינואר-מרץ 2026: 2,592,800 ש\"ח לדירת 3 חדרים, 4,059,300 ש\"ח לדירת 4 חדרים, 5,442,200 ש\"ח לדירת 5 חדרים")
e9 = P.edit(old9, new9, ["neighbourhoods[ארלוזרוב].rooms.3", "neighbourhoods[ארלוזרוב].rooms.4", "neighbourhoods[ארלוזרוב].rooms.5"], "UNSOURCED",
            "Area table, Arlozorov: an all-rooms indication of 3,200,000; replaced by the official Arlozorov medians by rooms (1-3.2026).")

# 10. recent-deals summary paragraph
old10 = P.find("בדוגמאות עסקאות שנצפו בפברואר ומרץ 2026 הופיעו עסקאות רבות", "במספר החדרים ובתכנון הדירה.")
new10 = ("בדוגמאות עסקאות שנצפו בפברואר ומרץ 2026 הופיעו עסקאות סביב 2.7-3.15 מיליון ש\"ח לדירות 3 ו-3.5 חדרים ולדירת 4 חדרים "
         "קומפקטית, לצד עסקאות סביב 3.85-5.03 מיליון ש\"ח לדירות גדולות יותר או בעלות מאפיינים חזקים. לכן מחיר למ\"ר הוא כלי עזר, "
         "אך הוא חייב להיות מלווה במספר החדרים ובתכנון הדירה. לשם השוואה, לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר "
         "העסקה לדירת 4 חדרים בגבעתיים היה 4,158,900 ש\"ח.")
e10 = P.edit(old10, new10, ["rooms.4.latest", "page"], "CONFLICT",
             "'Many deals around 2.7-3.15M for small and medium 3-4 room flats' reads as a 4-room level far below the official 4,158,900. The "
             "sentence now says which deals of the table fall in that band (3 and 3.5 rooms and one compact 4-room flat) and gives the official "
             "4-room median.", kept=["3.5"])

# 11. renovation cost with no source (tier 2)
old11 = "ייתכן צורך ב-150,000-500,000 ש\"ח"
new11 = "ייתכן צורך בשיפוץ משמעותי"
e11 = P.edit(old11, new11, ["page"], "UNSOURCED", "Renovation cost range with no source and no date; rephrased without the number.", tier=2)

# 12. FAQ average price
old12 = P.find("בדיקת נתוני שוק גלויים מ-5 ביוני 2026 הציגה ממוצעים שונים", "ולא כמחיר לדירה מסוימת.")
new12 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה בגבעתיים בכל העסקאות היה 3,635,300 ש\"ח, ולדירת 4 חדרים "
         "4,158,900 ש\"ח. החציון מושפע מתמהיל העסקאות, השטחים, האזורים וסוגי הדירות, ולכן הוא מתאים רק כנקודת פתיחה, ולא כמחיר לדירה מסוימת.")
e12 = P.edit(old12, new12, ["rooms.all.latest", "rooms.4.latest"], "CONFLICT",
             "FAQ average: the two city averages 2.85M and 4.35M vs the official all-deals median 3,635,300 (1-3.2026).")

# 13. FAQ 3 rooms
old13 = P.find("אינדיקציות שוק לדירות 3 חדרים בגבעתיים נעו סביב 2.4-2.9 מיליון ש\"ח", "הטווח משתנה לפי רחוב, קומה, מצב וחניה.")
new13 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים בגבעתיים ברבעון הראשון של 2026 היה 2,815,300 ש\"ח, לעומת 3,091,900 "
         "ש\"ח שנה קודם לכן. בעסקאות שנצפו הופיעו דוגמאות כמו 2.42 מיליון ש\"ח לדירה של 65 מ\"ר, 2.70 מיליון ש\"ח לדירה של 80 מ\"ר "
         "ו-2.717 מיליון ש\"ח לדירה של 83 מ\"ר. המחיר משתנה לפי רחוב, קומה, מצב וחניה.")
e13 = P.edit(old13, new13, ["rooms.3.latest", "rooms.3.year_ago", "page"], "CONSISTENT",
             "FAQ 3 rooms: 2.4-2.9M was consistent with the official 2,815,300; restated as the median like the body. Deal examples kept.")

# 14. FAQ 4 rooms
old14 = P.find("דירת 4 חדרים בגבעתיים יכולה להופיע סביב 3.1-3.6 מיליון ש\"ח", "אינה דומה לדירת 117 מ\"ר.")
new14 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים בגבעתיים ברבעון הראשון של 2026 היה 4,158,900 ש\"ח, לעומת 4,362,200 "
         "ש\"ח שנה קודם לכן. מחיר של דירה מסוימת יכול להיות רחוק מהחציון לפי השטח, הרחוב ומאפייני הבניין: דירת 4 חדרים של 88 מ\"ר "
         "אינה דומה לדירת 117 מ\"ר.")
e14 = P.edit(old14, new14, ["rooms.4.latest", "rooms.4.year_ago"], "CONFLICT",
             "FAQ 4 rooms: the 3.1-3.6M 'basic working range' vs the official 4,158,900 (1-3.2026). The deal examples (3.85 / 4.10 / 5.03M) are "
             "dropped here; they stay in the dated deals table.")

# 15. FAQ 5 rooms (first sentence)
old15 = "בדפי שוק שנבדקו הופיעה אינדיקציה ממוצעת של כ-4,290,568 ש\"ח לדירות 5 חדרים, עם שטח ממוצע סביב 130 מ\"ר."
new15 = "לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 5 חדרים בגבעתיים ברבעון הראשון של 2026 היה 4,960,000 ש\"ח, לעומת 5,044,100 ש\"ח שנה קודם לכן."
e15 = P.edit(old15, new15, ["rooms.5.latest", "rooms.5.year_ago"], "CONFLICT",
             "FAQ 5 rooms: the market-page average 4,290,568 is 13.5% below the official 4,960,000 (1-3.2026). The 4.15-5.03M deal sentence that "
             "follows is consistent and stays.")

# 16. FAQ Borochov
old16 = "בורוכוב הופיעה כאחד האזורים החזקים בבדיקת השוק, עם אינדיקציה סביב 3.95 מיליון ש\"ח וכ-43,839 ש\"ח למ\"ר."
new16 = ("בורוכוב הופיעה כאחד האזורים החזקים בבדיקת השוק, עם כ-43,839 ש\"ח למ\"ר בדפי השוק שנבדקו. לפי נתוני רשות המסים לרבעון "
         "הראשון של 2026, חציון מחיר העסקה בבורוכוב היה 3,206,100 ש\"ח לדירת 3 חדרים ו-4,356,800 ש\"ח לדירת 4 חדרים, מעל החציון "
         "העירוני לאותם סוגי דירות.")
e16 = P.edit(old16, new16, ["neighbourhoods[בורוכוב].rooms.3", "neighbourhoods[בורוכוב].rooms.4", "rooms.3.latest", "rooms.4.latest", "page"],
             "UNSOURCED", "FAQ Borochov: the all-rooms 3.95M indication becomes the official Borochov medians by rooms, as in the area table (edit 8). "
             "Both medians are above the city medians (2,815,300 and 4,158,900).")

# ---------------- claims inventory ----------------
C = P.claim
KM = "keep (market pages checked 5.6.2026, page checked 6.6.2026)"
C("p@4196", "ממוצעים עירוניים נעים בערך בין 2.85 מיליון ש\"ח ל-4.35 מיליון ש\"ח", "sale_avg", "CONFLICT", f"edit {e1}", rooms="all",
  official="rooms.all 3,635,300 (1-3.2026)", figures=2, note="two sources' averages shown as a range; each about 20% off the median")
C("p@4196", "דירות 3 חדרים נעות לרוב סביב 2.4-2.9 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e1}", rooms=3, official="2,815,300 (1-3.2026)", note="restated as the median")
C("p@4196", "דירות 4 חדרים סביב 3.1-3.6 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e1}", rooms=4, official="4,158,900 (1-3.2026)")
C("p@4196", "דירות 5 חדרים יכולות לעבור 4.3 מיליון ש\"ח ואף יותר", "sale", "CONSISTENT", f"edit {e1}", rooms=5, official="4,960,000 (1-3.2026)", note="restated as the median")
C("p@4196", "שכירות סביב 6,000-6,500 ש\"ח לדירה טיפוסית", "rent", "UNSOURCED", f"edit {e1}", figures=2,
  note="6,000 kept as the June 2026 listing median (p@16100); 6,500 appears nowhere else and is dropped")
C("p@5049", "ממוצעים עירוניים של כ-2.85-4.35 מיליון ש\"ח", "sale_avg", "CONFLICT", f"edit {e2}", rooms="all", official="rooms.all 3,635,300", figures=2)
C("p@5300", "שכירות חציונית סביב 6,000 ש\"ח, דירות 3 חדרים סביב 6,391 ש\"ח", "rent", "UNSOURCED", "keep (dedicated rent page checked June 2026, p@16100)", figures=2)
C("p@5300", "מחיר למ\"ר סביב 31,856-42,000 ש\"ח", "per_m2", "UNSOURCED", KM, figures=2)
C("p@5777", "דירת 3 חדרים ותיקה באזור מרכזי סביב 2.7-3.0 מיליון ש\"ח", "sale", "CONSISTENT", "keep (contains the official median)", rooms=3, official="2,815,300")
C("p@5777", "דירת 4 חדרים גדולה, משופצת או חדשה יותר 3.8-5.0 מיליון ש\"ח", "sale", "CONSISTENT", "keep (contains the official median)", rooms=4, official="4,158,900")
C("p@5777", "בדירות 5 חדרים עסקאות סביב 4.1-5.0 מיליון ש\"ח", "sale", "CONSISTENT", "keep (contains the official median)", rooms=5, official="4,960,000")
C("p@6216", "ממוצע עירוני של כ-2,847,355 ש\"ח", "sale_avg", "CONFLICT", f"edit {e3}", rooms="all", official="rooms.all 3,635,300 (-21.7%)")
C("p@6216", "מקור אחר: מחיר ממוצע של כ-4,350,000 ש\"ח", "sale_avg", "CONFLICT", f"edit {e3}", rooms="all", official="rooms.all 3,635,300 (+19.7%)")
C("p@6216", "מחיר למ\"ר של כ-31,856 ש\"ח ... כ-42,000 ש\"ח", "per_m2", "UNSOURCED", KM, figures=2)
C("p@6628", "1,237 עסקאות במקור אחד, 1,070 במקור אחר, 3,675 בדף רחב יותר", "count", "UNSOURCED", "keep (deal counts, not prices; market pages checked 5.6.2026)", figures=3)
C("tr@7462", "ממוצע עירוני נמוך יותר שנצפה | כ-2,847,355 ש\"ח", "sale_avg", "CONFLICT", f"edit {e4}", rooms="all", official="rooms.all 3,635,300")
C("tr@7682", "ממוצע עירוני גבוה יותר שנצפה | כ-4,350,000 ש\"ח", "sale_avg", "CONFLICT", f"edit {e4}", rooms="all", official="rooms.all 3,635,300")
C("tr@7889..8082", "מחיר למ\"ר: כ-31,856 / כ-42,000 ש\"ח", "per_m2", "UNSOURCED", f"keep (market pages checked 5.6.2026; carried into the table of edit {e4})", figures=2)
C("tr@8302", "דוגמת 4 חדרים במחשבון שוק | כ-3.32 מיליון ש\"ח | טווח 3.05-3.59 מיליון, כ-318 עסקאות", "sale", "CONFLICT", f"edit {e4}", rooms=4,
  official="4,158,900 (1-3.2026)", figures=2)
C("tr@8523", "שכירות חציונית | כ-6,000 ש\"ח", "rent", "UNSOURCED", f"keep (rent page checked June 2026; carried into the table of edit {e4})")
C("tr@9707", "2 חדרים | כ-1,833,563 ש\"ח (563 עסקאות באחד מדפי השוק)", "sale", "UNSOURCED", f"keep (market page checked 5.6.2026; moved into the check note by edit {e6})", rooms=2)
C("tr@10000", "3 חדרים | כ-2,401,393-2,900,000 ש\"ח", "sale", "CONSISTENT", f"edit {e6}", rooms=3, official="2,815,300", note="restated as the median")
C("tr@10000", "3 חדרים | דוגמאות 2026: 2.42, 2.70, 2.717, 3.00 מיליון ש\"ח", "deal", "UNSOURCED", f"keep (individual 2026 deals; kept in the note of edit {e6})", rooms=3, figures=4)
C("tr@10294", "3.5 חדרים | כ-2,870,000-3,010,000 ש\"ח", "sale", "UNSOURCED", f"keep (range of the dated 2026 deals in the deals table; moved into the note by edit {e6})",
  rooms="3.5", figures=1, note="no official 3.5-room series")
C("tr@10608", "4 חדרים | כ-3,096,234-3,600,000 ש\"ח", "sale", "CONFLICT", f"edit {e6}", rooms=4, official="4,158,900 (1-3.2026)")
C("tr@10608", "4 חדרים | דוגמאות שוק 3.15, 3.20, 3.50, 3.85, 4.10, 5.03 מיליון ש\"ח", "deal", "UNSOURCED", f"keep (individual deal examples; kept in the note of edit {e6})",
  rooms=4, figures=6, note="3.15 / 3.85 / 4.10 / 5.03 are dated in the deals table; 3.20 and 3.50 only by the market-page check")
C("tr@10915", "5 חדרים | כ-4,150,000-5,030,000 ש\"ח", "sale", "CONSISTENT", f"edit {e6}", rooms=5, official="4,960,000", note="restated as the median")
C("tr@9707..10915", "עמודת מחיר למ\"ר שנצפה (33,223 / 32,070+ / 30,000-36,000 / 31,704-42,000 / 32,829+)", "per_m2", "UNSOURCED",
  f"keep (market pages checked 5.6.2026; carried into the table of edit {e6})", figures=7)
C("p@11234", "ז'בוטינסקי 4 חדרים 95 מ\"ר סביב 3.15 מיליון; המאבק 4 חדרים 117 מ\"ר סביב 5.03 מיליון", "deal", "UNSOURCED",
  "keep (individual deals, dated 24.2.2026 and 26.2.2026 in the deals table)", rooms=4, figures=2)
C("tr@12683", "בורוכוב | כ-3,950,000 ש\"ח", "sale_nb", "UNSOURCED", f"edit {e8}", official="בורוכוב 3=3,206,100 4=4,356,800", note="all-rooms indication")
C("tr@12901", "שינקין | כ-3,440,270 ש\"ח", "sale_nb", "UNSOURCED", "keep (market pages, page checked 6.6.2026; no official median for Shenkin)")
C("tr@13128", "ארלוזורוב | כ-3,200,000 ש\"ח", "sale_nb", "UNSOURCED", f"edit {e9}", official="ארלוזרוב 3=2,592,800 4=4,059,300 5=5,442,200")
C("tr@13343", "גבעת רמב\"ם | כ-3,100,000 ש\"ח", "sale_nb", "UNSOURCED", "keep (market pages, page checked 6.6.2026; no official median for Givat Rambam)")
C("tr@12683..13343", "מחיר למ\"ר באזורים: 43,839 / 38,000 / 35,000 / 34,000", "per_m2", "UNSOURCED", "keep (market pages, page checked 6.6.2026)", figures=4)
C("tr@14258", "סיטי | שכירות יקרה סביב 10,450 ש\"ח", "rent", "UNSOURCED", "keep (rent page checked June 2026, tr@18322)")
C("tr@14514", "קריית יוסף | 3 חדרים ב-2.42 מיליון ש\"ח, 65 מ\"ר", "deal", "UNSOURCED", "keep (one observed 2026 deal)", rooms=3)
C("tr@14757..15490", "ממוצעי רחוב: קק\"ל 3,992,666 (12), ערבי נחל 3,871,875 (16), כצנלסון 2,091,121 (33), ההסתדרות 4,247,761 (21)", "sale_street",
  "UNSOURCED", "keep (street averages of observed deals from market pages, page checked 6.6.2026; no official street series)", figures=4)
C("tr@14997", "ערבי נחל: 5 חדרים, 127 מ\"ר, סביב 5.00 מיליון ש\"ח", "deal", "UNSOURCED", "keep (one observed deal; close to the 5-room median 4,960,000)", rooms=5)
C("p@16100", "שכירות חציונית 6,000 (293 מודעות, יוני 2026); 3 חדרים 6,391; 5,580 / 6,150 / 7,500 / 10,350", "rent", "UNSOURCED",
  "keep (dedicated rent page checked June 2026 + market pages)", figures=6)
C("tr@17018..18322", "טבלת שכירות: 6,000; 293 מודעות; 5,580; 6,150-6,391; 7,500; 10,350; שינקין 5,393; סיטי 10,450", "rent", "UNSOURCED",
  "keep (rent pages checked June 2026)", figures=9)
C("tr@17735", "4 חדרים: בודק אם מחיר מכירה של 3.5-4.2 מיליון ש\"ח נשען על שוק שכירות", "sale", "CONSISTENT", "keep (contains the official median)", rooms=4, official="4,158,900")
C("p@19276", "עסקאות רבות סביב 2.7-3.15 מיליון ש\"ח לדירות 3-4 חדרים קטנות ובינוניות", "sale", "CONFLICT", f"edit {e10}", rooms=4,
  official="4,158,900 (the 3-room part is consistent with 2,815,300)")
C("p@19276", "עסקאות סביב 3.85-5.03 מיליון ש\"ח לדירות גדולות", "deal", "UNSOURCED", "keep (summary of the dated Feb-Mar 2026 deals in the table)", figures=1)
C("tr@19884..22365", "טבלת עסקאות (10 עסקאות מתוארכות, 22.2-10.3.2026)", "deal", "UNSOURCED", "keep (individual dated deals)", figures=10)
C("tr@25091", "שיפוץ | ייתכן צורך ב-150,000-500,000 ש\"ח", "other", "UNSOURCED", f"edit {e11}", figures=1, note="tier 2")
C("p@30684", "FAQ: ממוצעים שונים, בערך בין 2.85 מיליון ל-4.35 מיליון ש\"ח", "sale_avg", "CONFLICT", f"edit {e12}", rooms="all", official="rooms.all 3,635,300", figures=2)
C("p@30966", "FAQ: 31,856 עד 42,000 ש\"ח למ\"ר; בורוכוב 43,839; שינקין 38,000", "per_m2", "UNSOURCED", KM, figures=4)
C("p@31262", "FAQ: דירות 3 חדרים נעו סביב 2.4-2.9 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e13}", rooms=3, official="2,815,300", note="restated as the median")
C("p@31262", "FAQ: דוגמאות 2.42 / 2.70 / 2.717 מיליון ש\"ח", "deal", "UNSOURCED", f"keep (individual observed deals; kept in edit {e13})", rooms=3, figures=3)
C("p@31554", "FAQ: דירת 4 חדרים סביב 3.1-3.6 מיליון ש\"ח כטווח עבודה בסיסי", "sale", "CONFLICT", f"edit {e14}", rooms=4, official="4,158,900 (1-3.2026)")
C("p@31554", "FAQ: עסקאות הגיעו גם ל-3.85, 4.10 ואף 5.03 מיליון ש\"ח", "deal", "UNSOURCED", f"edit {e14}", rooms=4, figures=3,
  note="dropped from the FAQ; the same deals stay in the dated deals table")
C("p@31856", "FAQ: אינדיקציה ממוצעת של כ-4,290,568 ש\"ח לדירות 5 חדרים", "sale", "CONFLICT", f"edit {e15}", rooms=5, official="4,960,000 (1-3.2026, -13.5%)")
C("p@31856", "FAQ: דוגמאות עסקאות סביב 4.15-5.03 מיליון ש\"ח לדירות של 112-159 מ\"ר", "deal", "CONSISTENT", "keep (contains the official 5-room median)", rooms=5, official="4,960,000")
C("p@32127", "FAQ: בורוכוב, אינדיקציה סביב 3.95 מיליון ש\"ח", "sale_nb", "UNSOURCED", f"edit {e16}", official="בורוכוב 3=3,206,100 4=4,356,800")
C("p@32127", "FAQ: בורוכוב כ-43,839 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"keep (market pages; kept in edit {e16})")
C("p@32378", "FAQ: שינקין כ-3.44 מיליון ש\"ח", "sale_nb", "UNSOURCED", "keep (market page, page checked 6.6.2026; no official median for Shenkin)")
C("p@32378", "FAQ: שינקין כ-38,000 ש\"ח למ\"ר; שכירות סביב 5,393 ש\"ח", "per_m2", "UNSOURCED", KM, figures=2, note="one per-m2 and one rent figure")

P.write(notes=(
    "The 4-room level is the main conflict: every 4-room range on the page (3.1-3.6M lead and FAQ, 3,096,234-3,600,000 table, 3.32M "
    "calculator) sat well below the official median 4,158,900 (1-3.2026; the 8-quarter series runs 3.80-4.36M). The two 'city averages' "
    "2,847,355 and 4,350,000 were each about 20% from the official all-deals median 3,635,300 and are replaced everywhere (lead, box, "
    "two-sources paragraph, indicator table, FAQ). 3- and 5-room ranges were consistent and are restated as medians where they sat in "
    "edited blocks; p@5777 (2.7-3.0 / 3.8-5.0 / 4.1-5.0M by segment) is consistent and kept. Shenkin, Givat Rambam and the four street "
    "averages are kept (market pages, page checked 6.6.2026; the official file has no median for them). Tel Ganim has full official "
    "medians (3=3,589,400, 4=4,614,700, 5=5,202,800) but its area-table row carries no number, so nothing was added there. Not audited "
    "as claims: the 5% / 10% / 15% buyer check (li@30071), 6-10 deal counts, m2 sizes. Edit 11 (renovation 150,000-500,000, no source) is "
    "tier 2. Remaining SUSPECT lines in check.py: the deals table and p@11234 (individual dated deals, 22.2-10.3.2026), the 3- and 4-room "
    "check notes in the new rooms table (lists of individual 2026 deal examples), and the 3.5-room rows, which the scan reads as '5 rooms' "
    "because of the '3.5' (a regex artefact: they are individual 3.5-room deals). Name mapping: page 'ארלוזורוב' = official 'ארלוזרוב'. "
    "The all-rooms median fell 12.7% year on year (4,164,300 to 3,635,300), largely a mix effect; the page does not quote that change. Also SUSPECT: the ערבי נחל row (tr@15201), an all-rooms street average that the scan pairs "
    "with the 5-room deal example in the same row."))
