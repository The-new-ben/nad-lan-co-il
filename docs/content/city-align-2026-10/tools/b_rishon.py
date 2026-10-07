# -*- coding: utf-8 -*-
"""Rishon LeZion (page 4581): body alignment with the official price list (1-3.2026). Built on the b_ashkelon.py pattern.
The 3/4/5-room working ranges of the body are CONSISTENT with the official medians: they are kept word for word and the official
median is shown next to them. The 2-room and 6+-room rows, the six undated 'example deals' and two renovation-cost ranges are edited."""
from mk import Page

P = Page("rishon-lezion-apartment-prices")

# ---------------- edits ----------------
# 1. intro of the rooms table
old1 = "לכן הטבלה הבאה נועדה לתת מסגרת עבודה ולא תחליף לשומת מקרקעין או לבדיקה פרטנית."
new1 = ("לכן הטבלה הבאה מציגה את חציון מחיר העסקה בראשון לציון לפי נתוני רשות המסים לרבעון הראשון של 2026, ולצידו טווח עבודה "
        "לבדיקה, שבתוכו נמצא החציון בכל אחד מסוגי הדירות. היא נועדה לתת מסגרת עבודה ולא תחליף לשומת מקרקעין או לבדיקה פרטנית. "
        "המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים, דירות 6 חדרים ופנטהאוזים כדאי לבדוק מול עסקאות דומות "
        "ברחוב ובשכונה.")
e1 = P.edit(old1, new1, ["rooms.3.latest", "data_quarter"], "WORDING",
            "Intro of the rooms table: announces the official median column added in edit 2 and says why the 2-room and 6+-room rows left the table.")

# 2. the rooms table: official median column added, 3/4/5 rows kept word for word, 2 and 6+ rows leave
new2 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">סוג דירה</th>
<th dir="rtl">שטח נפוץ לבדיקה</th>
<th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>
<th dir="rtl">טווח מחיר עבודה</th>
<th dir="rtl">שכונות שבהן הפערים בולטים</th>
<th dir="rtl">בדיקה משלימה</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">3 חדרים</td>
<td dir="rtl">60 עד 80 מ"ר</td>
<td dir="rtl">1,936,700 ש"ח</td>
<td dir="rtl">1,650,000 עד 2,250,000 ש"ח</td>
<td dir="rtl">רמב"ם, אברמוביץ, שיכוני המזרח, נחלת יהודה</td>
<td dir="rtl">שיפוץ, מעלית, קומה, מרפסת</td>
</tr>
<tr dir="rtl">
<td dir="rtl">4 חדרים</td>
<td dir="rtl">85 עד 110 מ"ר</td>
<td dir="rtl">2,392,600 ש"ח</td>
<td dir="rtl">2,150,000 עד 3,050,000 ש"ח</td>
<td dir="rtl">רמז, נחלת יהודה, קריית גנים, נרקיסים</td>
<td dir="rtl">ממ"ד, חניה, גיל בניין, תכנון פנימי</td>
</tr>
<tr dir="rtl">
<td dir="rtl">5 חדרים</td>
<td dir="rtl">110 עד 135 מ"ר</td>
<td dir="rtl">3,631,900 ש"ח</td>
<td dir="rtl">2,750,000 עד 4,100,000 ש"ח</td>
<td dir="rtl">נווה חוף, נווה ים, קריית חתני פרס נובל, קריית כרמים</td>
<td dir="rtl">קומה, נוף, חניות, מחסן, מרפסת</td>
</tr>
</tbody>
</table>"""
e2 = P.table('<th dir="rtl">טווח מחיר עבודה</th>', new2,
             ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "UNSOURCED",
             "Rooms table: the 3-, 4- and 5-room working ranges contain the official medians (1,936,700 / 2,392,600 / 3,631,900, 1-3.2026) and are "
             "kept word for word next to a new official median column. The 2-room row (1.35-1.85M) and the 6-room / penthouse row (3.9-6.5M) "
             "have no source and no official counterpart: they leave the table (edit 1 says how to check those sizes).")

# 3. renovation range in the neighbourhood paragraph (tier 2)
old3 = "צורך בשיפוץ של 100,000 עד 250,000 ש\"ח או סיכון תכנוני שדורש בדיקה."
new3 = "צורך בשיפוץ יסודי או סיכון תכנוני שדורש בדיקה."
e3 = P.edit(old3, new3, ["page"], "UNSOURCED",
            "A renovation-cost range with no source; rephrased without the number.", tier=2)

# 4. lead-in to the example-deals table (now official neighbourhood medians)
old4 = "מחיר למ\"ר עוזר לנרמל את ההשוואה, אך גם הוא עלול להטעות אם משווים דירה קטנה לדירה גדולה, דירה עם גג לדירה רגילה, או דירה חדשה לדירה ישנה."
new4 = (old4 + " כנקודת ייחוס, הטבלה הבאה מציגה את חציון מחיר העסקה בכמה שכונות בעיר, לפי נתוני רשות המסים לרבעון הראשון של 2026. "
        "בשכונות שאינן בטבלה, כמו נווה ים וקריית חתני פרס נובל, ההשוואה נשענת על עסקאות דומות ברחוב ובשכונה.")
e4 = P.edit(old4, new4, ["data_quarter"], "WORDING", "Lead-in for edit 5: the table now shows official neighbourhood medians instead of undated example deals.")

# 5. example-deals table -> official neighbourhood medians
new5 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">שכונה</th>
<th dir="rtl">3 חדרים</th>
<th dir="rtl">4 חדרים</th>
<th dir="rtl">5 חדרים</th>
<th dir="rtl">איך לקרוא את הנתון</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">רמב"ם</td>
<td dir="rtl">1,876,800 ש"ח</td>
<td dir="rtl">2,086,400 ש"ח</td>
<td dir="rtl">2,497,900 ש"ח</td>
<td dir="rtl">מצב בניין, חניה, רעש, שיפוץ</td>
</tr>
<tr dir="rtl">
<td dir="rtl">רמז</td>
<td dir="rtl">1,802,600 ש"ח</td>
<td dir="rtl">2,140,200 ש"ח</td>
<td dir="rtl">4,153,600 ש"ח</td>
<td dir="rtl">יש לבדוק מעלית, חניה ומרפסת</td>
</tr>
<tr dir="rtl">
<td dir="rtl">אברמוביץ</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">1,941,000 ש"ח</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">חניה, עומס, קומות נמוכות, שיפוץ</td>
</tr>
<tr dir="rtl">
<td dir="rtl">נחלת יהודה</td>
<td dir="rtl">2,354,400 ש"ח</td>
<td dir="rtl">3,460,700 ש"ח</td>
<td dir="rtl">3,610,600 ש"ח</td>
<td dir="rtl">מתאימה להשוואה מול בניינים דומים באזור</td>
</tr>
<tr dir="rtl">
<td dir="rtl">רמת אליהו</td>
<td dir="rtl">1,901,900 ש"ח</td>
<td dir="rtl">2,295,000 ש"ח</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">יש לבדוק מצב בניין ותכניות התחדשות</td>
</tr>
</tbody>
</table>"""
e5 = P.table('<th dir="rtl">דוגמת עסקה לבדיקה</th>', new5,
             ['neighbourhoods[רמב"ם].rooms.3', 'neighbourhoods[רמב"ם].rooms.4', 'neighbourhoods[רמב"ם].rooms.5',
              "neighbourhoods[רמז].rooms.3", "neighbourhoods[רמז].rooms.4", "neighbourhoods[רמז].rooms.5",
              "neighbourhoods[אברמוביץ].rooms.4",
              "neighbourhoods[נחלת יהודה].rooms.3", "neighbourhoods[נחלת יהודה].rooms.4", "neighbourhoods[נחלת יהודה].rooms.5",
              "neighbourhoods[רמת אליהו].rooms.3", "neighbourhoods[רמת אליהו].rooms.4"], "UNSOURCED",
             "Six undated 'example deals' with no source, under the heading 'recent deals' (Remez 4 rooms 2.52M vs official 2,140,200; Nahalat "
             "Yehuda 4 rooms 2.78M vs 3,460,700; Ramat Eliyahu 3 rooms 1.56M vs 1,901,900) plus per-m2 values derived from them. Replaced by the "
             "official neighbourhood medians, 1-3.2026 ('לא פורסם' where the official file has no median). Check notes reused word for word "
             "from the old rows and from the neighbourhood table (Rambam, Abramovitz).")

# 6. renovation range in the new-vs-second-hand table (tier 2)
old6 = "לעיתים 80,000 עד 300,000 ש\"ח"
new6 = "תלוי בהיקף העבודה ובמצב הדירה"
e6 = P.edit(old6, new6, ["page"], "UNSOURCED", "Renovation-cost range in a table cell with no source; rephrased without the number.", tier=2)

# 7-9. FAQ answers: lead with the official median, keep the consistent working range
old7 = "דירת 3 חדרים בראשון לציון יכולה לנוע בטווח עבודה של כ-1,650,000 עד 2,250,000 ש\"ח, בהתאם לשכונה, שטח, מצב הדירה, קומה, מעלית וחניה."
new7 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים בראשון לציון ברבעון הראשון של 2026 היה 1,936,700 ש\"ח, לעומת "
        "1,962,700 ש\"ח שנה קודם לכן. בפועל, דירת 3 חדרים יכולה לנוע בטווח עבודה של כ-1,650,000 עד 2,250,000 ש\"ח, בהתאם לשכונה, "
        "שטח, מצב הדירה, קומה, מעלית וחניה.")
e7 = P.edit(old7, new7, ["rooms.3.latest", "rooms.3.year_ago", "page"], "CONSISTENT",
            "FAQ 3 rooms: the working range contains the official median 1,936,700; the answer now leads with the median, like the table.")
old8 = "דירת 4 חדרים נבדקת לרוב בטווח של כ-2,150,000 עד 3,050,000 ש\"ח."
new8 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים בראשון לציון ברבעון הראשון של 2026 היה 2,392,600 ש\"ח, לעומת "
        "2,371,200 ש\"ח שנה קודם לכן. בפועל, דירת 4 חדרים נבדקת לרוב בטווח של כ-2,150,000 עד 3,050,000 ש\"ח.")
e8 = P.edit(old8, new8, ["rooms.4.latest", "rooms.4.year_ago", "page"], "CONSISTENT",
            "FAQ 4 rooms: the working range contains the official median 2,392,600; the answer now leads with the median.")
old9 = "דירת 5 חדרים יכולה לנוע סביב 2,750,000 עד 4,100,000 ש\"ח, ובמקרים של דירה גדולה, חדשה, מערבית, עם חניה כפולה, מחסן ונוף, גם מעבר לכך."
new9 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 5 חדרים בראשון לציון ברבעון הראשון של 2026 היה 3,631,900 ש\"ח, לעומת "
        "3,560,600 ש\"ח שנה קודם לכן. בפועל, דירת 5 חדרים יכולה לנוע סביב 2,750,000 עד 4,100,000 ש\"ח, ובמקרים של דירה גדולה, חדשה, "
        "מערבית, עם חניה כפולה, מחסן ונוף, גם מעבר לכך.")
e9 = P.edit(old9, new9, ["rooms.5.latest", "rooms.5.year_ago", "page"], "CONSISTENT",
            "FAQ 5 rooms: the working range contains the official median 3,631,900; the answer now leads with the median.")

# ---------------- claims inventory ----------------
C = P.claim
C("p@4322", "חציון שכירות סביב 5,000 ש\"ח, ממוצעים סביב 5,787 עד 6,131 ש\"ח לפי מדגם ושיטת חישוב", "rent", "UNSOURCED",
  "keep (rent sample named in the sentence, page checked 6.6.2026)", figures=3)
C("tr@8356", "2 חדרים | 1,350,000 עד 1,850,000 ש\"ח", "sale", "UNSOURCED", f"edit {e2}", rooms=2, figures=2, note="no official 2-room series, no source; row leaves the table")
C("tr@8578", "3 חדרים | 1,650,000 עד 2,250,000 ש\"ח", "sale", "CONSISTENT", f"edit {e2}", rooms=3, official="1,936,700 (1-3.2026)", figures=2,
  note="kept word for word next to the official median")
C("tr@8810", "4 חדרים | 2,150,000 עד 3,050,000 ש\"ח", "sale", "CONSISTENT", f"edit {e2}", rooms=4, official="2,392,600 (1-3.2026)", figures=2,
  note="kept word for word next to the official median")
C("tr@9047", "5 חדרים | 2,750,000 עד 4,100,000 ש\"ח", "sale", "CONSISTENT", f"edit {e2}", rooms=5, official="3,631,900 (1-3.2026)", figures=2,
  note="kept word for word next to the official median")
C("tr@9295", "6 חדרים ופנטהאוזים | 3,900,000 עד 6,500,000 ש\"ח ומעלה", "sale", "UNSOURCED", f"edit {e2}", rooms=6, figures=2,
  note="no official 6-room series, no source; row leaves the table")
C("p@13670", "צורך בשיפוץ של 100,000 עד 250,000 ש\"ח", "other", "UNSOURCED", f"edit {e3}", figures=2, note="renovation cost, no source (tier 2)")
C("p@14310", "חציון שכירות סביב 5,000 ש\"ח בחלק מהמדגמים, וממוצעים סביב 5,787 עד 6,131 ש\"ח", "rent", "UNSOURCED",
  "keep (rent samples named in the sentence, page checked 6.6.2026)", figures=3)
C("tr@14961..17554", "טבלת שכירות חודשית לדוגמה לפי שכונה (16 שורות, 3,900 עד 8,950 ש\"ח)", "rent", "UNSOURCED",
  "keep (rent samples named in the section text, page checked 6.6.2026)", figures=16,
  note="the header says 'לדוגמה' and the section says 'בחלק מהמדגמים'; weakest kept source on the page")
C("tr@18972", "דירה במרכז ותיק | 3 | 72 מ\"ר | 1,850,000 ש\"ח | 25,694 ש\"ח", "deal", "UNSOURCED", f"edit {e5}", rooms=3,
  official="city 3 rooms 1,936,700 (1-3.2026); no official 'old centre' area", figures=2, note="undated example deal, no source")
C("tr@19198", "דירה ברמז | 4 | 96 מ\"ר | 2,520,000 ש\"ח | 26,250 ש\"ח", "deal", "UNSOURCED", f"edit {e5}", rooms=4,
  official="Remez 4 rooms 2,140,200 (1-3.2026)", figures=2, note="undated example deal, no source; 18% above the official neighbourhood median")
C("tr@19405", "דירה בנחלת יהודה | 4 | 104 מ\"ר | 2,780,000 ש\"ח | 26,731 ש\"ח", "deal", "UNSOURCED", f"edit {e5}", rooms=4,
  official="Nahalat Yehuda 4 rooms 3,460,700 (1-3.2026)", figures=2, note="undated example deal, no source; 20% below the official neighbourhood median")
C("tr@19631", "דירה בנווה ים | 5 | 124 מ\"ר | 3,650,000 ש\"ח | 29,435 ש\"ח", "deal", "UNSOURCED", f"edit {e5}", rooms=5,
  official="no official Neve Yam median; city 5 rooms 3,631,900", figures=2, note="undated example deal, no source")
C("tr@19842", "דירה בקריית חתני פרס נובל | 5 | 132 מ\"ר | 4,050,000 ש\"ח | 30,682 ש\"ח", "deal", "UNSOURCED", f"edit {e5}", rooms=5,
  official="no official Nobel median; city 5 rooms 3,631,900", figures=2, note="undated example deal, no source")
C("tr@20078", "דירה ברמת אליהו | 3 | 68 מ\"ר | 1,560,000 ש\"ח | 22,941 ש\"ח", "deal", "UNSOURCED", f"edit {e5}", rooms=3,
  official="Ramat Eliyahu 3 rooms 1,901,900 (1-3.2026)", figures=2, note="undated example deal, no source; 18% below the official neighbourhood median")
C("tr@22065", "שיפוץ | לעיתים 80,000 עד 300,000 ש\"ח", "other", "UNSOURCED", f"edit {e6}", figures=2, note="renovation cost, no source (tier 2)")
C("p@28502", "FAQ: דירת 3 חדרים בטווח עבודה של כ-1,650,000 עד 2,250,000 ש\"ח", "sale", "CONSISTENT", f"edit {e7}", rooms=3,
  official="1,936,700 (1-3.2026)", figures=2, note="range kept, median added")
C("p@28787", "FAQ: דירת 4 חדרים בטווח של כ-2,150,000 עד 3,050,000 ש\"ח", "sale", "CONSISTENT", f"edit {e8}", rooms=4,
  official="2,392,600 (1-3.2026)", figures=2, note="range kept, median added")
C("p@29047", "FAQ: דירת 5 חדרים סביב 2,750,000 עד 4,100,000 ש\"ח", "sale", "CONSISTENT", f"edit {e9}", rooms=5,
  official="3,631,900 (1-3.2026)", figures=2, note="range kept, median added")
C("p@29860", "FAQ שכירות: חציון 5,000, ממוצעים 5,787 עד 6,131, במערב 7,000 עד 9,000 ש\"ח", "rent", "UNSOURCED",
  "keep (same rent samples as the body, page checked 6.6.2026)", figures=5)

P.write(notes=(
    "No conflicts on this page: the 3/4/5-room working ranges of the rooms table and of the FAQ all contain the official medians "
    "(1,936,700 / 2,392,600 / 3,631,900, 1-3.2026). They are kept word for word; the official median is added next to them (table column, "
    "FAQ first sentence). Not audited as claims (illustrations, not market statements): the 2,300,000 cost example (p@7295), the 2,700,000 "
    "budget example (p@9571), the buyer / seller / owner if-examples 2,420,000 / 2,550,000 / 2,400,000-2,480,000, 2,650,000 / 2,950,000, "
    "150,000 / 180,000 (p@10058, p@10336, p@10594), the 8,000 / 4,500 rent example (p@17742), the six-step example table with its "
    "'דוגמה מספרית' column (tr@26035..26925: 2,380,000-2,620,000 deals, 2,550,000-2,890,000 asking, 5,600-6,300 rent, 80,000 + 35,000 "
    "costs, 2,470,000 offer vs 2,650,000), the seller example 2,850,000 / 2,550,000-2,680,000 (p@27132), the 12% and 10% / 15% "
    "negotiation examples (p@27539, p@30137). Rent figures are kept: the page names samples ('לפי מדגם', 'בחלק מהמדגמים') and shows its "
    "check date 6.6.2026, but it never says the samples are listings; if a stricter reading is wanted, the rent table header "
    "'שכירות חודשית לדוגמה' is the weakest point. Renovation-cost ranges (p@13670, tr@22065) are tier 2. Official quirks: Remez 5 rooms "
    "4,153,600 is above the city 5-room median and Rambam 5 rooms is 2,497,900 (small samples). Qualitative text NOT edited but at odds "
    "with the official neighbourhood medians: the lead (p@4322) and the neighbourhood table (tr@11550..13426) present Ramat Eliyahu as "
    "'נמוך עד בינוני' and Nahalat Yehuda among the older central areas, while the official 4-room medians are Ramat Eliyahu 2,295,000, "
    "Remez 2,140,200, Rambam 2,086,400, Abramovitz 1,941,000 and Nahalat Yehuda 3,460,700. The JSON-LD script and the closing disclaimer "
    "('טווחי בדיקה') are outside the audit and unchanged. The official neighbourhood list in the city file holds exactly 8 names (it may be "
    "capped), so the text does not say that Neve Yam or Nobel have no published median; it says they are not in the table."))
