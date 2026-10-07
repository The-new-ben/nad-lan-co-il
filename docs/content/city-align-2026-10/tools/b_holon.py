# -*- coding: utf-8 -*-
"""Holon (page 4585): body alignment with the official price list (1-3.2026). Built on the b_ashkelon.py pattern.
Currency on this page: ₪. Its tables use <thead>/<tbody>/<tr> without dir; the new tables keep that style."""
import re
from mk import Page

P = Page("holon-apartment-prices")


def cells(row_html):
    return re.findall(r"<t[hd] dir=\"rtl\">.*?</t[hd]>", row_html, re.S)


def rows(tbl):
    return re.findall(r"<tr>\n.*?</tr>", tbl, re.S)


# ---------------- edits ----------------
# 1. lead paragraph
old1 = P.find("מחירי דירות בחולון מתחילים בדרך כלל סביב", "ומחיר למ״ר מוצג לא פעם סביב 25,000-29,000 ₪.")
new1 = ("מחירי דירות בחולון, לפי נתוני רשות המסים לרבעון הראשון של 2026: חציון מחיר העסקה היה 1,918,700 ₪ לדירת 3 חדרים, "
        "2,428,500 ₪ לדירת 4 חדרים ו-3,142,700 ₪ לדירת 5 חדרים. דירות גדולות יותר, פנטהאוזים, דירות חדשות או נכסים במיקומים חזקים "
        "במיוחד יכולים להגיע גם ל-3,000,000-4,800,000 ₪. לפי אתרי נתונים פרטיים ודינמיים, מחיר למ״ר מוצג לא פעם סביב 25,000-29,000 ₪.")
e1 = P.edit(old1, new1, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
            "Lead: the asking average 'around 2,400,000' is 8.1% above the official all-rooms median 2,219,400 (1-3.2026); the undated "
            "1.6-1.9M for small flats has no source. The 1.9-2.5M range for 3-4 rooms was consistent and is restated as the official medians; "
            "the 3.0-4.8M range for large or new flats (contains the 5-room median) and the per-m2 range of private data sites are kept.")

# 2. 'an average of 2,400,000 can mislead'
old2 = "לכן מחיר ממוצע של 2,400,000 ₪ יכול להטעות:"
new2 = "לכן גם מחיר עירוני אחד, כמו חציון מחיר העסקה של 2,219,400 ₪ בכל העסקאות ברבעון הראשון של 2026, יכול להטעות:"
e2 = P.edit(old2, new2, ["rooms.all.latest"], "CONFLICT", "Repeats the 2,400,000 city average; replaced by the official all-rooms median 2,219,400 (1-3.2026).")

# 3. the 10 m2 example: 350,000 does not follow from the page's own 25,000-29,000 per m2 (tier 2)
old3 = "פער של 10 מ״ר בלבד יכול לשנות מחיר ב-250,000-350,000 ₪ כאשר המחיר למ״ר נע סביב 25,000-29,000 ₪."
new3 = "פער של 10 מ״ר בלבד יכול לשנות מחיר ב-250,000 ₪ ויותר כאשר המחיר למ״ר נע סביב 25,000-29,000 ₪."
e3 = P.edit(old3, new3, ["page"], "UNSOURCED",
            "10 m2 at 25,000-29,000 per m2 is 250,000-290,000; the 350,000 top does not follow from the page's own figures. Kept the floor.", tier=2)

# 4. floor / balcony premium percent (tier 2)
old4 = "פער בין קומה נמוכה לדירה עם מרפסת, חניה ונגישות טובה יכול להגיע ל-5%-12% באותו אזור."
new4 = "פער בין קומה נמוכה לדירה עם מרפסת, חניה ונגישות טובה יכול להיות משמעותי גם באותו אזור."
e4 = P.edit(old4, new4, ["page"], "UNSOURCED", "A 5%-12% premium with no source; rephrased without the number.", tier=2)

# 5. intro of the rooms table
old5 = "הנתונים הבאים משלבים נקודת ייחוס ממודעות ומאגרי נתונים פרטיים, לצד טווח בדיקה סביר לדירות יד שנייה ודירות חדשות בחולון."
new5 = ("הטבלה הבאה מציגה את חציון מחיר העסקה לפי נתוני רשות המסים לרבעון הראשון של 2026, לצד נקודת ייחוס ממודעות ומאגרי נתונים "
        "פרטיים וטווח בדיקה סביר לדירות בחולון. המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים, דירות 6 חדרים ומעלה "
        "ודירות חדשות בפרויקטים כדאי לבדוק מול עסקאות דומות ברחוב, בשכונה ובפרויקט.")
e5 = P.edit(old5, new5, ["rooms.3.latest", "data_quarter"], "WORDING",
            "Intro of the rooms table: announces the official median column (edit 6) and says why the 2-room, 6+-room and new-project rows left the table.")

# 6. rooms table: official median column added; rows 2.5-3 / 4 / 5 kept word for word; 2, 6+ and new-project rows leave
A6 = '<th dir="rtl">טווח בדיקה סביר בחולון</th>'
old6 = P.table_html(A6)
R = rows(old6)
assert len(R) == 7, len(R)
MED = {1: "1,918,700 ₪ ל-3 חדרים", 2: "2,428,500 ₪", 3: "3,142,700 ₪"}
out_rows = []
hdr = R[0]
c0 = cells(hdr)[0]
out_rows.append(hdr.replace(c0 + "\n", c0 + "\n" + '<th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>' + "\n", 1))
for i in (2, 3, 4):
    r = R[i]
    c0 = cells(r)[0]
    out_rows.append(r.replace(c0 + "\n", c0 + "\n" + '<td dir="rtl">' + MED[i - 1] + "</td>\n", 1))
new6 = ("<table dir=\"rtl\">\n<thead>\n" + out_rows[0] + "\n</thead>\n<tbody>\n" + "\n".join(out_rows[1:]) + "\n</tbody>\n</table>")
assert new6.count("<tr>") == 4 and "1,550,000" not in new6 and "8%-20%" not in new6 and "4,850,000" not in new6, new6
e6 = P.table(A6, new6, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "UNSOURCED",
             "Rooms table: the 3-, 4- and 5-room asking averages and check ranges contain or sit within 5% of the official medians "
             "(1,918,700 / 2,428,500 / 3,142,700, 1-3.2026) and are kept word for word next to a new official median column. The 2-room "
             "row (1.55-1.95M check range), the 6+-room row (3.9-5.4M) and the new-project row (8%-20% over second-hand) have no source for "
             "their ranges and no official counterpart: they leave the table. The named asking averages for 2 and 6+ rooms stay in the "
             "paragraph above the table.")

# 7. lead-in of the neighbourhood table
old7 = "באזורים מבוקשים יותר או בבנייה חדשה המחיר הכולל גבוה יותר, וההשוואה מול דירה ישנה צריכה לכלול גם עלויות שיפוץ, תחזוקה וזמן כניסה."
new7 = (old7 + " בטבלה הבאה מופיע חציון מחיר העסקה לפי נתוני רשות המסים לרבעון הראשון של 2026 בשכונות שבהן הוא זמין; בשאר השכונות "
        "ההשוואה נשענת על עסקאות דומות ברחוב ובשכונה.")
e7 = P.edit(old7, new7, ["data_quarter"], "WORDING", "Lead-in for edit 8: the neighbourhood table now carries official medians.")

# 8. neighbourhood table: the undated all-rooms 'check range' column becomes the official median column
A8 = '<th dir="rtl">טווח מחיר בדיקה לדירות רגילות</th>'
old8 = P.table_html(A8)
NB = {"1,800,000-2,700,000 ₪": "3 חדרים: 1,836,700 ₪, 4 חדרים: 2,600,400 ₪",
      "1,850,000-2,900,000 ₪": "3 חדרים: 1,685,200 ₪, 4 חדרים: 2,595,200 ₪",
      "1,700,000-2,650,000 ₪": "3 חדרים: 1,700,800 ₪, 4 חדרים: 2,069,400 ₪",
      "1,550,000-2,300,000 ₪": "משווים לעסקאות דומות ברחוב",
      "1,450,000-2,250,000 ₪": "משווים לעסקאות דומות ברחוב",
      "2,100,000-3,200,000 ₪": "בקרית שרת מערב, 4 חדרים: 2,310,000 ₪, 5 חדרים: 3,427,300 ₪",
      "1,700,000-2,600,000 ₪": "משווים לעסקאות דומות ברחוב"}
new8 = old8.replace(A8, '<th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>')
for k, v in NB.items():
    cell = '<td dir="rtl">' + k + "</td>"
    assert new8.count(cell) == 1, k
    new8 = new8.replace(cell, '<td dir="rtl">' + v + "</td>")
e8 = P.table(A8, new8,
             ["neighbourhoods[אגרובנק].rooms.3", "neighbourhoods[אגרובנק].rooms.4", "neighbourhoods[קרית עבודה].rooms.3",
              "neighbourhoods[קרית עבודה].rooms.4", "neighbourhoods[נאות רחל].rooms.3", "neighbourhoods[נאות רחל].rooms.4",
              "neighbourhoods[קרית שרת מערב].rooms.4", "neighbourhoods[קרית שרת מערב].rooms.5"], "UNSOURCED",
             "Neighbourhood table: seven all-rooms 'check ranges' with no source or room count (e.g. Kiryat Avoda 1.85-2.9M while its official "
             "3-room median is 1,685,200). Replaced by the official neighbourhood medians, 1-3.2026, where the official file has them "
             "(Agrobank, Kiryat Avoda, Neot Rachel; 'קריית שרת' mapped to the official 'קרית שרת מערב', named in the cell); the other three rows "
             "point to street deals. The other four columns stay word for word.")

# 9. street averages from 2023
old9 = P.find("דוגמאות רחובות יכולות לעזור להבין את עומק השוק, אך לא להחליף בדיקה פרטנית.",
              "הנתונים שימושיים כנקודת השוואה, אך רחוב אחד יכול לכלול בניינים שונים מאוד זה מזה.")
new9 = ("גם נתונים לפי שכונה יכולים לעזור להבין את עומק השוק, אך לא להחליף בדיקה פרטנית. לפי נתוני רשות המסים לרבעון הראשון של "
        "2026, חציון מחיר העסקה לדירת 4 חדרים היה 2,265,800 ₪ בקרית בן גוריון, 2,567,300 ₪ ברסקו א׳ ו-3,017,400 ₪ בקרית פנחס איילון. "
        "גם בתוך שכונה, רחוב אחד יכול לכלול בניינים שונים מאוד זה מזה.")
e9 = P.edit(old9, new9, ["neighbourhoods[קרית בן גוריון].rooms.4", "neighbourhoods[רסקו א].rooms.4", "neighbourhoods[קרית פנחס איילון].rooms.4"],
            "STALE",
            "Street averages by number of deals in 2023 (Hankin 1,878,862 ... Fichman 3,195,392), all rooms mixed, used as a current comparison "
            "point; replaced by official 4-room neighbourhood medians, 1-3.2026.")

# 10. yield table: the 2-room and new/upgraded rows leave (unsourced purchase prices); rows 3-5 kept word for word
A10 = '<th dir="rtl">תשואה ברוטו משוערת</th>'
old10 = P.table_html(A10)
R10 = rows(old10)
assert len(R10) == 6
new10 = old10.replace(R10[1] + "\n", "", 1).replace("\n" + R10[5], "", 1)
assert new10.count("<tr>") == 4 and "1,550,000" not in new10 and "2,700,000-4,200,000" not in new10, new10
e10 = P.table(A10, new10, ["page"], "UNSOURCED",
              "Rent and yield table: the 2-room purchase range (1.55-1.95M) and the new/upgraded purchase range (2.7-4.2M) have no source and no "
              "official counterpart; their rows (and the yields derived from them) leave the table. Rows 3-5 stay word for word: their purchase "
              "ranges contain the official medians and their asking rents are the named reference of the section.")

# 11. Dirobot average
old11 = "Dirobot מציג לחולון מחיר ממוצע סביב 2,400,000 ₪, מחיר למ״ר סביב 29,000 ₪ וכ-1,821 עסקאות."
new11 = "Dirobot מציג לחולון מחיר למ״ר סביב 29,000 ₪ וכ-1,821 עסקאות."
e11 = P.edit(old11, new11, ["page"], "CONFLICT",
             "A named platform's city average 2,400,000 is 8.1% above the official all-rooms median 2,219,400 (1-3.2026); the average is "
             "dropped, the platform's per-m2 figure and deal count are kept.")

# 12. new-flat premium percent (tier 2)
old12 = "פער של 8%-20% מעל דירת יד שנייה דומה יכול להיות סביר במקרים מסוימים, אך הוא לא אוטומטי."
new12 = "פער מעל דירת יד שנייה דומה יכול להיות סביר במקרים מסוימים, אך הוא לא אוטומטי."
e12 = P.edit(old12, new12, ["page"], "UNSOURCED", "An 8%-20% new-flat premium with no source; rephrased without the number.", tier=2)

# 13. new vs second-hand table: the new-flat purchase cell
old13 = "לעיתים 2,600,000-4,200,000 ₪ ומעלה"
new13 = "בדרך כלל גבוה מדירת יד שנייה דומה, לפי מפרט, קומה ומועד מסירה"
e13 = P.edit(old13, new13, ["page"], "UNSOURCED",
             "A new-flat price range with no room count and no source; rephrased without numbers. The second-hand cell (1.8-2.8M for regular "
             "flats) contains the official all-rooms median 2,219,400 and is kept.")

# 14. renovation cost in the new vs second-hand table (tier 2)
old14 = "ייתכן שיפוץ של 80,000-300,000 ₪"
new14 = "ייתכן צורך בשיפוץ, לפי מצב הדירה"
e14 = P.edit(old14, new14, ["page"], "UNSOURCED", "A renovation-cost range with no source; rephrased without the number.", tier=2)

# 15. offer change range in the checks table (tier 2)
old15 = "יכול לשנות הצעה ב-50,000-250,000 ₪"
new15 = "יכול לשנות את סכום ההצעה"
e15 = P.edit(old15, new15, ["page"], "UNSOURCED", "A 50,000-250,000 effect on the offer with no source; rephrased without the number.", tier=2)

# 16. renovation cost in the checks table (tier 2)
old16 = "שיפוץ יכול לנוע סביב 80,000-300,000 ₪"
new16 = "עלות שיפוץ משתנה לפי היקף העבודה ומצב הדירה"
e16 = P.edit(old16, new16, ["page"], "UNSOURCED", "A renovation-cost range with no source; rephrased without the number.", tier=2)

# 17-19. FAQ
old17 = P.find("נקודות ייחוס פרטיות מציגות מחיר ממוצע סביב 2,400,000 ₪", "יכולות להגיע ל-3,000,000 ₪ ומעלה.")
new17 = ("לפי נתוני רשות המסים, חציון מחיר העסקה בחולון, בכל מספרי החדרים, היה 2,219,400 ₪ ברבעון הראשון של 2026, אך זהו נתון "
         "עירוני רחב. לפי מספר חדרים, החציון היה 1,918,700 ₪ לדירת 3 חדרים, 2,428,500 ₪ לדירת 4 חדרים ו-3,142,700 ₪ לדירת 5 חדרים, "
         "ודירות גדולות או חדשות יכולות להגיע ל-3,000,000 ₪ ומעלה.")
e17 = P.edit(old17, new17, ["rooms.all.latest", "rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
             "FAQ average: 2,400,000 vs the official all-rooms median 2,219,400; the undated 1.6-1.9M for small flats is dropped; the 4-room "
             "range (consistent) is restated as the median; the 3,000,000+ floor for large or new flats is kept.")
old18 = "דירת 3 חדרים בחולון נעה לעיתים סביב 1,750,000-2,250,000 ₪, כאשר במדדירות מוצג מחיר מבוקש ממוצע סביב 1,920,000 ₪."
new18 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים בחולון ברבעון הראשון של 2026 היה 1,918,700 ₪, לעומת 1,899,500 ₪ "
         "שנה קודם לכן. בפועל, דירת 3 חדרים נעה לעיתים סביב 1,750,000-2,250,000 ₪, כאשר במדדירות מוצג מחיר מבוקש ממוצע סביב "
         "1,920,000 ₪.")
e18 = P.edit(old18, new18, ["rooms.3.latest", "rooms.3.year_ago", "page"], "CONSISTENT",
             "FAQ 3 rooms: the range and the named asking average match the official median 1,918,700; the answer now leads with the median, like the table.")
old19 = "דירת 4 חדרים רגילה נבדקת לרוב סביב 2,150,000-2,750,000 ₪."
new19 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים בחולון ברבעון הראשון של 2026 היה 2,428,500 ₪, לעומת 2,578,200 ₪ "
         "שנה קודם לכן. דירת 4 חדרים רגילה נבדקת לרוב סביב 2,150,000-2,750,000 ₪.")
e19 = P.edit(old19, new19, ["rooms.4.latest", "rooms.4.year_ago", "page"], "CONSISTENT",
             "FAQ 4 rooms: the range and the named asking average 2,390,000 match the official median 2,428,500; the answer now leads with the median.")

# 20. FAQ new-flat premium percent (tier 2)
old20 = "דירה חדשה יכולה להיות יקרה ב-8%-20% מדירה דומה יד שנייה, אך הפער צריך להיות מוסבר ולא להתקבל אוטומטית."
new20 = "דירה חדשה יכולה להיות יקרה מדירה דומה יד שנייה, אך הפער צריך להיות מוסבר ולא להתקבל אוטומטית."
e20 = P.edit(old20, new20, ["page"], "UNSOURCED", "The 8%-20% new-flat premium again, no source; rephrased without the number.", tier=2)

# ---------------- claims inventory ----------------
C = P.claim
C("p@4374", "1,600,000-1,900,000 ₪ לדירות קטנות", "sale", "UNSOURCED", f"edit {e1}", rooms="2 (small)", figures=2, note="no source, no room count; dropped")
C("p@4374", "1,900,000-2,500,000 ₪ בדירות 3-4 חדרים", "sale", "CONSISTENT", f"edit {e1}", rooms="3,4", official="1,918,700 / 2,428,500 (1-3.2026)",
  figures=2, note="restated as the official medians")
C("p@4374", "3,000,000-4,800,000 ₪ בדירות גדולות, פנטהאוזים, דירות חדשות", "sale", "CONSISTENT", f"edit {e1}", rooms="5+",
  official="5 rooms 3,142,700", figures=2, note="kept inside the rewrite")
C("p@4374", "לפי אתרי נתונים פרטיים, מחיר מבוקש ממוצע בעיר סביב 2,400,000 ₪", "sale_avg", "CONFLICT", f"edit {e1}", rooms="all",
  official="2,219,400 (1-3.2026), +8.1%")
C("p@4374", "מחיר למ״ר מוצג סביב 25,000-29,000 ₪ (אתרי נתונים פרטיים)", "per_m2", "UNSOURCED",
  "keep (private data sites, page checked 6.6.2026; carried inside edit 1)", figures=2)
C("p@5339", "מדדירות: 2,473 דירות למכירה ולהשכרה, שכירות מבוקשת 5,150, לפי חדרים 4,100 / 4,500 / 5,800 / 8,200", "rent", "UNSOURCED",
  "keep (named listing portal, page checked 6.6.2026)", figures=6)
C("p@6560", "מחיר ממוצע של 2,400,000 ₪ יכול להטעות", "sale_avg", "CONFLICT", f"edit {e2}", rooms="all", official="2,219,400")
C("li@7619", "דירת 3 חדרים ישנה ... סביב 1,700,000-2,000,000 ₪", "sale", "CONSISTENT", "keep (contains the official median)", rooms=3,
  official="1,918,700", figures=2)
C("li@7709", "דירת 4 חדרים משופצת ... סביב 2,200,000-2,700,000 ₪", "sale", "CONSISTENT", "keep (contains the official median)", rooms=4,
  official="2,428,500", figures=2)
C("li@7794", "דירת 5 חדרים חדשה ... 3,000,000-3,700,000 ₪, ולעיתים יותר", "sale", "CONSISTENT", "keep (contains the official median)", rooms=5,
  official="3,142,700", figures=2)
C("li@7885", "פער של 10 מ״ר יכול לשנות מחיר ב-250,000-350,000 ₪", "other", "UNSOURCED", f"edit {e3}", figures=2,
  note="the page's own 25,000-29,000 per m2 gives 250,000-290,000 (tier 2)")
C("li@7990", "פער ... יכול להגיע ל-5%-12% באותו אזור", "other", "UNSOURCED", f"edit {e4}", figures=2, note="tier 2")
C("p@8808", "מדדירות: מחיר ביקוש ממוצע 1,690,000 ל-2 חדרים ו-4,850,000 ל-6 חדרים ומעלה", "sale", "UNSOURCED",
  "keep (named listing portal, page checked 6.6.2026)", rooms="2,6", figures=2)
C("p@8808", "מדדירות: 1,920,000 ל-3 חדרים, 2,390,000 ל-4 חדרים, 3,290,000 ל-5 חדרים", "sale", "CONSISTENT",
  "keep (within 5% of the official medians)", rooms="3,4,5", official="1,918,700 / 2,428,500 / 3,142,700", figures=3, note="5 rooms +4.7%")
C("p@8808", "מחיר למ״ר מוצג שם סביב 20,208-27,480 ₪", "per_m2", "UNSOURCED", "keep (named listing portal, page checked 6.6.2026)", figures=2)
C("tr@9504", "2 חדרים | כ-1,690,000 | 1,550,000-1,950,000 | כ-27,480 למ״ר", "sale", "UNSOURCED", f"edit {e6}", rooms=2, figures=4,
  note="row leaves the table; the named asking average stays in p@8808")
C("tr@9721", "2.5-3 חדרים | כ-1,920,000 ל-3 חדרים | 1,750,000-2,250,000", "sale", "CONSISTENT", f"edit {e6}", rooms=3, official="1,918,700",
  figures=3, note="kept word for word next to the official median")
C("tr@9941", "4 חדרים | כ-2,390,000 | 2,150,000-2,750,000", "sale", "CONSISTENT", f"edit {e6}", rooms=4, official="2,428,500", figures=3,
  note="kept word for word")
C("tr@10153", "5 חדרים | כ-3,290,000 | 2,850,000-3,700,000", "sale", "CONSISTENT", f"edit {e6}", rooms=5, official="3,142,700", figures=3,
  note="kept word for word")
C("tr@9721..10153", "עמודת מחיר למ״ר מוצג: 25,600 / 23,431 / 25,308", "per_m2", "UNSOURCED", "keep (named listing portal; kept word for word in edit 6)",
  figures=3)
C("tr@10371", "6 חדרים ומעלה | כ-4,850,000 | 3,900,000-5,400,000 | כ-20,208 למ״ר", "sale", "UNSOURCED", f"edit {e6}", rooms=6, figures=4,
  note="row leaves the table; the named asking average stays in p@8808")
C("tr@10589", "דירה חדשה בפרויקט | לעיתים 8%-20% מעל יד שנייה דומה", "sale_new_used", "UNSOURCED", f"edit {e6}", figures=2, note="row leaves the table")
C("tr@12304..13699", "טווח מחיר בדיקה לדירות רגילות לפי שכונה (7 שורות, 1,450,000 עד 3,200,000)", "sale_nb", "UNSOURCED", f"edit {e8}",
  rooms="all", figures=14,
  official="Agrobank 3r 1,836,700 4r 2,600,400; Kiryat Avoda 3r 1,685,200 4r 2,595,200; Neot Rachel 3r 1,700,800 4r 2,069,400; "
           "Kiryat Sharet West 4r 2,310,000 5r 3,427,300; Tel Giborim, Jessy Cohen, Shikun Vatikim not in the official file",
  note="no source, no period, no room count")
C("p@13947", "מדדירות: רחובות לפי מספר עסקאות בשנת 2023, חנקין 1,878,862 ... פיכמן 3,195,392", "sale_street", "STALE", f"edit {e9}",
  rooms="all", figures=5, note="2023 street averages used as a current comparison point")
C("p@15229", "מדדירות 5,150, Realta 5,721 וחציון 5,200, Scoutr 5,563", "rent", "UNSOURCED", "keep (named portals, page checked 6.6.2026)", figures=4)
C("tr@15845", "2 חדרים | 4,100 | 3,700-4,600 | 1,550,000-1,950,000 | 2.5%-3.4%", "sale", "UNSOURCED", f"edit {e10}", rooms=2, figures=7,
  note="unsourced 2-room purchase range and the yield derived from it; row leaves the table")
C("tr@16015..16355", "מחיר קנייה משוער 3-5 חדרים: 1,750,000-2,250,000 / 2,150,000-2,750,000 / 2,850,000-3,700,000", "sale", "CONSISTENT",
  "keep (each contains the official median)", rooms="3,4,5", official="1,918,700 / 2,428,500 / 3,142,700", figures=6)
C("tr@16015..16355", "שכירות מבוקשת 4,500 / 5,800 / 8,200 וטווחי שכירות בדיקה", "rent", "UNSOURCED",
  "keep (named asking-rent reference of p@5339, page checked 6.6.2026)", figures=9)
C("tr@16015..16355", "תשואה ברוטו משוערת 2.4%-3.6% / 2.3%-3.6% / 2.2%-3.7%", "yield", "UNSOURCED",
  "keep (labelled estimates from the kept rents and the consistent purchase ranges)", figures=6, note="weakest kept figures on the page")
C("tr@16525", "דירה חדשה או משודרגת | 5,800-9,500 | 2,700,000-4,200,000", "sale_new_used", "UNSOURCED", f"edit {e10}", figures=4, note="row leaves the table")
C("p@17787", "Dirobot: מחיר ממוצע סביב 2,400,000 ₪", "sale_avg", "CONFLICT", f"edit {e11}", rooms="all", official="2,219,400, +8.1%")
C("p@17787", "Dirobot: מחיר למ״ר סביב 29,000 ₪ וכ-1,821 עסקאות", "per_m2", "UNSOURCED", "keep (named platform, page checked 6.6.2026)", figures=2)
C("tr@18328..19431", "6 עסקאות עם רחוב ומספר, מרץ 2026 (1,680,000 עד 2,260,000 ₪, מחיר למ״ר)", "deal", "UNSOURCED",
  "keep (individual dated deals with address)", figures=12)
C("p@20502", "פער של 8%-20% מעל דירת יד שנייה דומה", "sale_new_used", "UNSOURCED", f"edit {e12}", figures=2, note="tier 2")
C("tr@21509", "יד שנייה: לעיתים 1,800,000-2,800,000 ₪ בדירות רגילות", "sale_new_used", "CONSISTENT", "keep (contains the official all-rooms median)",
  rooms="all", official="2,219,400", figures=2)
C("tr@21509", "חדשה: לעיתים 2,600,000-4,200,000 ₪ ומעלה", "sale_new_used", "UNSOURCED", f"edit {e13}", figures=2, note="no room count, no source")
C("tr@21895", "ייתכן שיפוץ של 80,000-300,000 ₪", "other", "UNSOURCED", f"edit {e14}", figures=2, note="tier 2")
C("p@22508", "הלמ״ס הודעה 081/2026 (15.3.2026), בנק ישראל ריבית 3.75% (25.5.2026), מלאי כ-85 אלף דירות חדשות (מרץ 2026)", "macro",
  "UNSOURCED", "keep (dated; CBS and Bank of Israel named)", figures=2, note="the 85 thousand inventory figure says only 'דווח'")
C("tr@23697", "יכול לשנות הצעה ב-50,000-250,000 ₪", "other", "UNSOURCED", f"edit {e15}", figures=2, note="tier 2")
C("tr@24311", "שיפוץ יכול לנוע סביב 80,000-300,000 ₪", "other", "UNSOURCED", f"edit {e16}", figures=2, note="tier 2")
C("tr@24507", "ריבית 3.75% משפיעה על תקציב", "macro", "UNSOURCED", "keep (Bank of Israel decision dated 25.5.2026 in p@22508)")
C("p@26260", "FAQ: מחיר ממוצע סביב 2,400,000 ₪", "sale_avg", "CONFLICT", f"edit {e17}", rooms="all", official="2,219,400")
C("p@26260", "FAQ: דירות קטנות 1,600,000-1,900,000 ₪", "sale", "UNSOURCED", f"edit {e17}", rooms="2 (small)", figures=2)
C("p@26260", "FAQ: דירות 4 חדרים 2,150,000-2,750,000 ₪", "sale", "CONSISTENT", f"edit {e17}", rooms=4, official="2,428,500", figures=2,
  note="restated as the median")
C("p@26260", "FAQ: דירות גדולות או חדשות 3,000,000 ₪ ומעלה", "sale", "CONSISTENT", f"edit {e17}", rooms="5+", official="5 rooms 3,142,700",
  note="kept")
C("p@26559", "FAQ: 3 חדרים 1,750,000-2,250,000, מדדירות 1,920,000", "sale", "CONSISTENT", f"edit {e18}", rooms=3, official="1,918,700", figures=3,
  note="kept, median added")
C("p@26798", "FAQ: 4 חדרים 2,150,000-2,750,000", "sale", "CONSISTENT", f"edit {e19}", rooms=4, official="2,428,500", figures=2, note="kept, median added")
C("p@26798", "FAQ: מדדירות 2,390,000 ומחיר למ״ר 23,431", "sale", "CONSISTENT", "keep (named asking average within 5% of the median; per m2 named)",
  rooms=4, official="2,428,500", figures=2)
C("p@27050", "FAQ: 25,000-29,000 ₪ למ״ר, Dirobot 29,000", "per_m2", "UNSOURCED", "keep (named private platforms, page checked 6.6.2026)", figures=3)
C("p@27916", "FAQ: שכירות 5,150-5,721, חציון 5,200", "rent", "UNSOURCED", "keep (named portals of p@15229)", figures=3)
C("p@27916", "FAQ: מחיר קנייה של 2,000,000-2,700,000 ₪", "sale_avg", "CONSISTENT", "keep (contains the official all-rooms median)", rooms="all",
  official="2,219,400", figures=2)
C("p@28227", "FAQ: דירה חדשה יקרה ב-8%-20%", "sale_new_used", "UNSOURCED", f"edit {e20}", figures=2, note="tier 2")

P.write(notes=(
    "Most per-room figures on this page are consistent with the official medians (3-5 rooms); the conflicts are the 2,400,000 city "
    "average repeated four times (lead, p@6560, the named platform in p@17787, FAQ) against the official all-rooms median 2,219,400. "
    "Not audited as claims (illustrations, not market statements): the 3%-7% asking-vs-closing condition (p@11323), the yield example "
    "1,950,000 / 4,500-5,000 / 2.8%-3.1% and the 2,300,000 / 4,700 if-example (p@14845), the 3,100,000 / 2,600,000 / 500,000 new-vs-used "
    "if-example (p@20502), the seller example 2,250,000-2,400,000 / 2,690,000 / 2,290,000 (p@25473), the 150,000 gap example (p@25868), "
    "the 7%-12% if-example (p@27647). Remaining SUSPECT after the edits: tr@18704 (נס ציונה 3, March 2026, 2.5 rooms, 1,680,000) is an "
    "individual dated deal with an address. Portal names (מדדירות, Dirobot) stay only where old text kept word for word attributes kept figures "
    "(the rooms-table header, the FAQ 3-room answer, the Dirobot sentence); no new text names a portal. Name mapping: the page's 'קריית "
    "שרת' is matched to the official 'קרית שרת מערב' (part of it) and the cell names it; 'קריית עבודה' = 'קרית עבודה'; 'רסקו א׳' = "
    "'רסקו א'. The official neighbourhood list holds 8 names (may be capped), so Tel Giborim, Jessy Cohen and Shikun Vatikim are pointed "
    "to street deals without saying no median exists. Rent, per-m2 and yield figures are kept where the page names the source (מדדירות, "
    "Realta, Scoutr, Dirobot) and shows its check date 6.6.2026; the yields of rows 3-5 are the page's own estimates (tier 2 candidates "
    "if a stricter reading is wanted). Seven tier-2 edits remove rule-of-thumb figures with no source (renovation 80,000-300,000 twice, "
    "50,000-250,000 offer effect, 5%-12% floor premium, 8%-20% new-flat premium twice) and fix the 10 m2 example whose 350,000 top does "
    "not follow from 25,000-29,000 per m2. The JSON-LD script and the closing disclaimer are outside the audit and unchanged."))
