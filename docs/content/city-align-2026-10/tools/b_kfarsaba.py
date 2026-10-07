# -*- coding: utf-8 -*-
"""Kfar Saba (page 4562): body alignment with the official price list. The list is not on the page yet (it will be added).
Official latest: 3 and 4 rooms 10-12.2025 (the last published), 5 rooms 1-3.2026, all deals 10-12.2025. Built on b_ashkelon.py."""
from mk import Page

P = Page("kfar-saba-apartment-prices")


def tbl(head, rows):
    """table in this page's own HTML style (one tag per line)."""
    out = ['<table dir="rtl">', '<thead dir="rtl">', '<tr dir="rtl">'] + [f'<th dir="rtl">{x}</th>' for x in head] + ['</tr>', '</thead>', '<tbody dir="rtl">']
    for r in rows:
        out += ['<tr dir="rtl">'] + [f'<td dir="rtl">{x}</td>' for x in r] + ['</tr>']
    return "\n".join(out + ['</tbody>', '</table>'])


_old = P.table_html('<th dir="rtl">טווח קנייה שימושי</th>')
assert _old.startswith('<table dir="rtl">\n<thead dir="rtl">\n<tr dir="rtl">\n<th dir="rtl">') and _old.endswith("</tr>\n</tbody>\n</table>"), _old[-40:]

# ---------------- edits ----------------
# 1. lead
old1 = P.find("מחירי דירות בכפר סבא נעים לפי מספר חדרים, שכונה,", "לפי נתוני שוק, עסקאות ולוחות.")
new1 = ("מחירי דירות בכפר סבא נעים לפי מספר חדרים, שכונה, גיל בניין, מצב הדירה ורמת הביקוש ברחוב הספציפי, אבל בדיקת השוק מתחילה "
        "בנתונים ברורים: לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 5 חדרים ברבעון הראשון של 2026 היה 3,544,700 ש\"ח, וברבעון "
        "הרביעי של 2025 (הנתון האחרון שפורסם לדירות 3 ו-4 חדרים) 1,941,300 ש\"ח לדירת 3 חדרים ו-2,817,000 ש\"ח לדירת 4 חדרים. "
        "בשכירות, הממוצע החודשי עומד סביב 7,200 עד 7,350 ש\"ח לפי מקורות שוק שנבדקו ביוני 2026.")
e1 = P.edit(old1, new1, ["rooms.5.latest", "rooms.3.latest", "rooms.4.latest", "page"], "CONFLICT",
            "Lead: a city average of about 2.8M (a real-estate data site read in June 2026) vs the official all-deals median 2,415,900 "
            "(10-12.2025). The 4-room range 2.55-3.7M was consistent; the lead now gives the official medians by rooms. The rent average "
            "7,200-7,350 (market sources, page checked 5.6.2026) is kept.")

# 2. 'by the data checked': city average
old2 = "בבדיקה עירונית רחבה, מחיר ממוצע של דירה בכפר סבא נמצא סביב 2,810,000 ש\"ח באתר נתוני נדל\"ן אחד, כאשר מקורות נוספים הציגו ממוצע קרוב של כ-2,850,000 ש\"ח."
new2 = ("לפי נתוני רשות המסים, חציון מחיר העסקה בכלל העסקאות בכפר סבא ברבעון הרביעי של 2025 היה 2,415,900 ש\"ח, לעומת 2,301,700 ש\"ח "
        "באותו רבעון שנה קודם לכן.")
e2 = P.edit(old2, new2, ["rooms.all.latest", "rooms.all.year_ago"], "CONFLICT",
            "City averages 2,810,000 and 2,850,000 vs the official all-deals median 2,415,900 (10-12.2025).")

# 3. ranges by rooms
old3 = P.find("דירת 3 חדרים יכולה להופיע בטווח רחב של כ-2.1 עד 3.0 מיליון ש\"ח,", "הטווח יכול להיפתח כלפי מעלה.")
new3 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים ברבעון הרביעי של 2025 היה 1,941,300 ש\"ח, לעומת 1,960,100 ש\"ח ברבעון "
        "השלישי של 2025; לדירת 4 חדרים החציון באותו רבעון היה 2,817,000 ש\"ח, ולדירת 5 חדרים 3,544,700 ש\"ח ברבעון הראשון של 2026. "
        "בדירות חדשות, בדירות גן, בפנטהאוזים או בבניינים עם מפרט גבוה, המחיר יכול להיות גבוה יותר.")
e3 = P.edit(old3, new3, ["rooms.3.latest", "rooms.3.quarters[7-9.2025]", "rooms.4.latest", "rooms.5.latest"], "CONFLICT",
            "3 rooms 2.1-3.0M vs the official 1,941,300 (10-12.2025, the last published for 3 rooms). The 4-room (2.55-3.7M) and 5-room "
            "(3.5-4.5M) ranges were consistent and are restated as medians; the previous quarter shows the 3-room level is stable.")

# 4. 'city average' card
old4 = P.find("כ-2.8 עד 2.85 מיליון ש\"ח לדירה, לפי מקורות שוק שנבדקו ביוני 2026.", "זהו עוגן ראשוני, לא מחיר יעד.")
new4 = "2,415,900 ש\"ח: חציון מחיר העסקה בכלל העסקאות ברבעון הרביעי של 2025, לפי נתוני רשות המסים. החציון הוא עוגן ראשוני, לא מחיר יעד."
e4 = P.edit(old4, new4, ["rooms.all.latest"], "CONFLICT", "City average card 2.8-2.85M vs the official all-deals median 2,415,900 (10-12.2025).")

# 5. intro of the rooms table
old5 = "הטבלה הבאה מרכזת טווחי עבודה לפי מספר חדרים. הנתונים משלבים ממוצעים ממקורות שוק, נתוני לוחות ודוגמאות עסקאות."
new5 = ("הטבלה הבאה מציגה את חציון מחיר העסקה בכפר סבא לפי מספר חדרים, לפי נתוני רשות המסים, לצד החציון באותו רבעון שנה קודם לכן. "
        "בדירות 3 ו-4 חדרים מוצג הרבעון הרביעי של 2025, הנתון האחרון שפורסם.")
e5 = P.edit(old5, new5, ["data_quarter", "rooms.3.quarter"], "WORDING", "The intro announced working ranges from mixed market sources; the table becomes the official medians (edit 6).")

# 6. rooms table
new6 = tbl(["סוג דירה", "חציון מחיר העסקה, ינואר-מרץ 2026", "ינואר-מרץ 2025", "שינוי בשנה", "הערת בדיקה"], [
    ["3 חדרים", "1,941,300 ש\"ח (אוקטובר-דצמבר 2025)", "2,466,800 ש\"ח (אוקטובר-דצמבר 2024)", "ירידה של 21.3%", "מתאים לזוגות, משפרי דיור ראשונים ומשקיעים זהירים."],
    ["4 חדרים", "2,817,000 ש\"ח (אוקטובר-דצמבר 2025)", "3,001,300 ש\"ח (אוקטובר-דצמבר 2024)", "ירידה של 6.1%", "פלח מרכזי בכפר סבא, ולכן יש הרבה השוואות זמינות."],
    ["5 חדרים", "3,544,700 ש\"ח", "3,705,300 ש\"ח", "ירידה של 4.3%", "בדיקה לפי שכונה, חניה כפולה, ממ\"ד, מרפסת וגודל סלון."],
])
e6 = P.table('<th dir="rtl">טווח קנייה שימושי</th>', new6,
             ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct",
              "rooms.5.latest", "rooms.5.year_ago", "rooms.5.change_pct"], "CONFLICT",
             "Rooms table: 3 rooms 2.03-3.0M vs the official 1,941,300 (10-12.2025); the 2-room, 6+-room, garden and penthouse rows have no "
             "official counterpart. Replaced by the official medians with the same quarter a year earlier (3 and 4 rooms: 10-12.2025 vs "
             "10-12.2024; 5 rooms: 1-3.2026 vs 1-3.2025). The rent column leaves; the same rents stay in the rent table further down. "
             "Check notes of rows 3-5 kept word for word.")

# 7. sentence after the rooms table
old7 = "טבלת חדרים אינה מחליפה בדיקת מ\"ר."
new7 = ("המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים, דירות 6 חדרים ומעלה, דירות גן ופנטהאוזים כדאי לבדוק מול "
        "עסקאות דומות ברחוב ובשכונה. גם החציון אינו מחליף בדיקת מ\"ר.")
e7 = P.edit(old7, new7, ["data_quarter"], "WORDING", "Follows edit 6: the 2-room, 6+-room, garden and penthouse rows left the table.")

# 8. neighbourhood table
new8 = tbl(["אזור", "חציון מחיר העסקה, ינואר-מרץ 2026", "מה משפיע על המחיר", "איך לקרוא את המספר"], [
    ["כפר סבא הירוקה", "4 חדרים 3,418,700 ש\"ח", "בנייה חדשה יותר, משפחות, חניה, ממ\"ד וסביבה ירוקה.", "לא להשוות ישירות לדירה ותיקה במרכז."],
    ["הזמר העברי", "לא פורסם", "שכונה מבוקשת, דירות משפחתיות, תכנון מודרני.", "צריך לבדוק קומה, מרפסת וחניה בפועל."],
    ["מרכז העיר", "3 חדרים 2,106,700 ש\"ח, 4 חדרים 3,090,200 ש\"ח, 5 חדרים 3,501,900 ש\"ח",
     "מיקום עירוני, קרבה לשירותים, היצע מגוון ובניינים בגילים שונים.", "חציון רחב מדי לדירה אחת, חובה לבדוק רחוב, מצב בניין ומעלית."],
    ["תקומה והראשונים", "בהראשונים, 4 חדרים 2,396,100 ש\"ח", "נגישות, בנייה מעורבת, ביקוש משפחתי.", "לבדוק פער בין בניין מחודש לבניין ותיק."],
    ["הדרים", "לא פורסם", "אזור מוכר, היצע משפחתי, קרבה לשירותים.", "מתאים להשוואת 4 חדרים ו-5 חדרים רק עם התאמות."],
    ["קריית ספיר", "לא פורסם", "מיקום, תמהיל דירות וגיל בניינים.", "מדגם קטן יחסית, אין להסיק ממוצע קשיח."],
    ["יוספטל", "לא פורסם", "תמהיל נכסים, מוצר שונה, עסקאות שאינן מייצגות את כל העיר.", "להיזהר מהסקה ישירה, לבדוק כל נכס לגופו."],
])
e8 = P.table('<th dir="rtl">נתון שוק שנבדק</th>', new8,
             ["neighbourhoods[הירוקה כ\"ס 80].rooms.4", "neighbourhoods[מרכז].rooms.3", "neighbourhoods[מרכז].rooms.4", "neighbourhoods[מרכז].rooms.5",
              "neighbourhoods[ראשונים].rooms.4"], "STALE",
             "Neighbourhood table: all-rooms deal averages from 2023 data (Kfar Saba HaYeruka about 4,000,000, city centre south 2,790,000) "
             "and undated averages (HaZemer HaIvri, centre north, Tkuma and HaRishonim, Hadarim, Kiryat Sapir) presented as the current "
             "level. Replaced by the official neighbourhood medians by rooms, 1-3.2026 ('לא פורסם' where the official file has none); the "
             "two centre rows are merged into one because the official file has one 'מרכז'. Reading columns kept, merged for the centre.")

# 9. paragraph after the neighbourhood table
old9 = "הטעות הנפוצה היא לקחת ממוצע שכונתי ולהחיל אותו על כל דירה."
new9 = ("החציון השכונתי בטבלה הוא לפי נתוני רשות המסים לרבעון הראשון של 2026; בשכונות שבהן לא פורסם חציון, משווים לעסקאות סגורות "
        "דומות ברחוב ובבניין. הטעות הנפוצה היא לקחת ממוצע או חציון שכונתי ולהחיל אותו על כל דירה.")
e9 = P.edit(old9, new9, ["data_quarter"], "WORDING", "Follows edit 8: names the source and quarter of the neighbourhood medians and explains 'לא פורסם'.")

# 10. rent table: purchase-price column
new10 = tbl(["סוג דירה", "שכירות שוק", "חציון מחיר העסקה", "קריאת נתון"], [
    ["2 חדרים", "4,000 עד 4,500 ש\"ח", "לא פורסם", "שוכרים יחידים וזוגות, תלות גבוהה במיקום."],
    ["3 חדרים", "5,550 עד 5,800 ש\"ח", "1,941,300 ש\"ח (אוקטובר-דצמבר 2025)", "מתאים לבדיקת כניסה לשוק או דירה קומפקטית."],
    ["4 חדרים", "6,750 עד 6,800 ש\"ח", "2,817,000 ש\"ח (אוקטובר-דצמבר 2025)", "פלח מרכזי למשפחות, השוואות רבות יחסית."],
    ["5 חדרים", "8,100 עד 9,100 ש\"ח", "3,544,700 ש\"ח (ינואר-מרץ 2026)", "שוק משפחתי, רגיש לאזורי חינוך ולחניה."],
    ["בית פרטי", "כ-13,500 ש\"ח במדגם שוק", "לא פורסם, טווח רחב מאוד", "לא להשוות לדירות רגילות ללא התאמות."],
])
e10 = P.table('<th dir="rtl">מחיר קנייה אופייני</th>', new10, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest"], "CONFLICT",
              "Rent table: the purchase column repeats the rooms-table ranges (3 rooms 2.03-3.0M vs the official 1,941,300; 2 rooms with no "
              "official figure). The purchase cells become the official medians with their quarter; no yield or new number is computed; "
              "the rent column (market sample, page checked 5.6.2026) is kept word for word.")

# 11. new flats
old11 = P.find("בדירות חדשות בכפר סבא נראו טווחים של כ-2.5 עד 3.0 מיליון ש\"ח לדירות 3 חדרים,", "בהתאם למרפסת, קומה, נוף, מפרט ונדירות.")
new11 = ("בדירות חדשות בכפר סבא המחיר נקבע לפי הפרויקט, המפרט, הקומה ומועד המסירה, ודירה חדשה בפרויקט מבוקש יכולה להיות גבוהה מחציון "
         "מחיר העסקה העירוני. פנטהאוזים יקרים יותר, בהתאם למרפסת, קומה, נוף, מפרט ונדירות.")
e11 = P.edit(old11, new11, ["page"], "CONFLICT",
             "New flats: 3 rooms 2.5-3.0M and 4 rooms 3.1-3.7M exclude the official medians 1,941,300 and 2,817,000 (10-12.2025); the 5-room "
             "range was consistent; the 'from 4.0M' penthouse floor has no source. The official list has no new-flat split, so the paragraph "
             "is rephrased without numbers.")

# 12. second-hand 5 rooms
old12 = "דירת 5 חדרים יד שנייה יכולה להופיע סביב 3.75 מיליון ש\"ח בממוצע מסוים, אך השוואה טובה תבדוק אם מדובר בבניין בן 8 שנים, 18 שנים או 45 שנים."
new12 = ("בדירות 5 חדרים, חציון מחיר העסקה ברבעון הראשון של 2026 היה 3,544,700 ש\"ח לפי נתוני רשות המסים, אך השוואה טובה תבדוק אם "
         "מדובר בבניין בן 8 שנים, 18 שנים או 45 שנים.")
e12 = P.edit(old12, new12, ["rooms.5.latest"], "CONFLICT", "Second-hand 5 rooms 'about 3.75M in a certain average' vs the official 3,544,700 (1-3.2026), outside 5%.")

# 13-16. FAQ
old13 = "לפי מקורות שוק שנבדקו ביוני 2026, המחיר הממוצע נע סביב 2.8 עד 2.85 מיליון ש\"ח."
new13 = "לפי נתוני רשות המסים, חציון מחיר העסקה בכלל העסקאות בכפר סבא ברבעון הרביעי של 2025 היה 2,415,900 ש\"ח."
e13 = P.edit(old13, new13, ["rooms.all.latest"], "CONFLICT", "FAQ average 2.8-2.85M vs the official all-deals median 2,415,900 (10-12.2025).")
old14 = "דירות 3 חדרים מופיעות בטווחי עבודה של כ-2.03 עד 3.0 מיליון ש\"ח, כאשר דוגמאות עסקאות במאי 2026 כללו 2,100,000 ש\"ח לדירה של 63 מ\"ר ו-2,550,000 ש\"ח לדירה של 74 מ\"ר."
new14 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים בכפר סבא ברבעון הרביעי של 2025 (הנתון האחרון שפורסם) היה 1,941,300 ש\"ח. "
         "דוגמאות עסקאות במאי 2026 כללו 2,100,000 ש\"ח לדירה של 63 מ\"ר ו-2,550,000 ש\"ח לדירה של 74 מ\"ר.")
e14 = P.edit(old14, new14, ["rooms.3.latest", "page"], "CONFLICT",
             "FAQ 3 rooms: the working range 2.03-3.0M vs the official 1,941,300 (10-12.2025); the two dated May 2026 deals are kept.")
old15 = "דירות 4 חדרים רבות נעות סביב 2.55 עד 3.7 מיליון ש\"ח."
new15 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים בכפר סבא ברבעון הרביעי של 2025 (הנתון האחרון שפורסם) היה 2,817,000 ש\"ח, "
         "לעומת 3,001,300 ש\"ח באותו רבעון שנה קודם לכן.")
e15 = P.edit(old15, new15, ["rooms.4.latest", "rooms.4.year_ago"], "CONSISTENT",
             "FAQ 4 rooms: 2.55-3.7M holds the official 2,817,000 but no longer appears in the body (lead, ranges paragraph and tables were "
             "rebuilt); restated as the median. The dated deals sentence after it is kept.")
old16 = P.find("דירות 5 חדרים נעות לרוב סביב 3.5 עד 4.5 מיליון ש\"ח,", "אך דירות חדשות או נדירות יכולות להיות יקרות יותר.")
new16 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 5 חדרים בכפר סבא ברבעון הראשון של 2026 היה 3,544,700 ש\"ח, לעומת 3,705,300 ש\"ח "
         "שנה קודם לכן, עם שונות לפי שכונה, גודל, בניין ומפרט. בדוגמאות עסקאות ממאי 2026 נראו דירות 5 חדרים סביב 3,850,000 עד 3,900,000 "
         "ש\"ח, אך דירות חדשות או נדירות יכולות להיות יקרות יותר.")
e16 = P.edit(old16, new16, ["rooms.5.latest", "rooms.5.year_ago", "page"], "CONSISTENT",
             "FAQ 5 rooms: 3.5-4.5M holds the official 3,544,700 but no longer appears in the body; restated as the median. The two deal "
             "examples (Antokolsky 1 and HaAyit 12, both May 2026 in the deals table) are kept and now dated in the sentence.")

# ---------------- claims inventory ----------------
C = P.claim
C("p@4293", "סביב 2.8 מיליון ש\"ח כממוצע עירוני לפי אתר נתוני נדל\"ן שנקרא ביוני 2026", "sale_avg", "CONFLICT", f"edit {e1}", rooms="all", official="all deals 2,415,900 (10-12.2025)")
C("p@4293", "סביב 7,200 עד 7,350 ש\"ח שכירות חודשית ממוצעת לפי מקורות שוק", "rent", "UNSOURCED", f"keep (market sources, read June 2026; kept word for word inside edit {e1})", figures=2)
C("p@4293", "דירות 4 חדרים רבות שנעות סביב 2.55 עד 3.7 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e1}", rooms=4, official="2,817,000 (10-12.2025)", figures=2, note="restated as the median")
C("p@5163", "מחיר ממוצע סביב 2,810,000 ש\"ח ... ממוצע קרוב של כ-2,850,000 ש\"ח", "sale_avg", "CONFLICT", f"edit {e2}", rooms="all", official="all deals 2,415,900 (10-12.2025)", figures=2)
C("p@5163", "השכירות החודשית הממוצעת נעה סביב 7,200 עד 7,350 ש\"ח", "rent", "UNSOURCED", "keep (market sources, page checked 5.6.2026)", figures=2)
C("p@5477", "דירת 3 חדרים ... כ-2.1 עד 3.0 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e3}", rooms=3, official="1,941,300 (10-12.2025, last published)", figures=2)
C("p@5477", "דירת 4 חדרים ... סביב 2.55 עד 3.7 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e3}", rooms=4, official="2,817,000 (10-12.2025)", figures=2, note="restated as the median")
C("p@5477", "ודירת 5 חדרים ... סביב 3.5 עד 4.5 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e3}", rooms=5, official="3,544,700 (1-3.2026)", figures=2, note="restated as the median")
C("p@6301", "כ-2.8 עד 2.85 מיליון ש\"ח לדירה, לפי מקורות שוק שנבדקו ביוני 2026", "sale_avg", "CONFLICT", f"edit {e4}", rooms="all", official="all deals 2,415,900", figures=2)
C("p@6483", "שכירות 7,200 עד 7,350; 4 חדרים 6,750 עד 6,800; 5 חדרים 8,100 עד 9,100", "rent", "UNSOURCED", "keep (market sources, page checked 5.6.2026)", figures=6)
C("tr@7386", "2 חדרים | כ-1.45 עד 2.21 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e6}", rooms=2, figures=2)
C("tr@7584", "3 חדרים | כ-2.03 עד 3.0 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e6}", rooms=3, official="1,941,300 (10-12.2025)", figures=2)
C("tr@7785", "4 חדרים | כ-2.55 עד 3.7 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e6}", rooms=4, official="2,817,000 (10-12.2025)", figures=2, note="restated as the median")
C("tr@7985", "5 חדרים | כ-3.5 עד 4.5 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e6}", rooms=5, official="3,544,700 (1-3.2026)", figures=2, note="restated as the median")
C("tr@8188", "6 חדרים ומעלה | כ-4.14 עד 6.1 מיליון ש\"ח ומעלה", "sale", "UNSOURCED", f"edit {e6}", rooms=6, figures=2)
C("tr@8602", "פנטהאוז | מכ-4.0 מיליון ש\"ח בפרויקטים מסוימים", "sale", "UNSOURCED", f"edit {e6}", rooms="penthouse")
C("tr@7386..8602", "עמודת שכירות חודשית בטבלת החדרים (7 שורות)", "rent", "UNSOURCED", f"edit {e6}", figures=12, note="column leaves with the rebuilt table; 2-5 room rents stay in the rent table, garden 8,700 and penthouse 8,950 (market sample) are dropped")
C("p@8836", "דירות 4 חדרים של 89-102 מ\"ר, מחירים למ\"ר סביב 28,061 עד 37,303 ש\"ח", "per_m2", "UNSOURCED", "keep (from the dated May 2026 deals table on the page)", rooms=4, figures=2)
C("tr@10240", "כפר סבא הירוקה | ממוצעים סביב 4,000,000 ש\"ח בחלק מנתוני 2023", "sale_nb", "STALE", f"edit {e8}", official="הירוקה כ\"ס 80, 4 rooms 3,418,700 (1-3.2026)")
C("tr@10482", "הזמר העברי | כ-3,550,000 ש\"ח בממוצע עסקאות מסוים", "sale_nb", "UNSOURCED", f"edit {e8}", official="no official median")
C("tr@10706", "מרכז העיר דרום | כ-118 עסקאות, ממוצע כ-2,790,000 ש\"ח בנתוני 2023", "sale_nb", "STALE", f"edit {e8}", official="מרכז 3=2,106,700 4=3,090,200 5=3,501,900 (1-3.2026)", figures=2)
C("tr@10956", "מרכז העיר צפון | כ-19 עסקאות, ממוצע כ-2,500,000 ש\"ח", "sale_nb", "UNSOURCED", f"edit {e8}", official="מרכז (see above)", figures=2)
C("tr@11179", "תקומה והראשונים | כ-68 עסקאות, ממוצע כ-2,772,500 ש\"ח", "sale_nb", "UNSOURCED", f"edit {e8}", official="ראשונים 4 rooms 2,396,100", figures=2)
C("tr@11402", "הדרים | כ-19 עסקאות, ממוצע כ-2,750,000 ש\"ח", "sale_nb", "UNSOURCED", f"edit {e8}", official="no official median", figures=2)
C("tr@11625", "קריית ספיר | כ-13 עסקאות, ממוצע כ-2,760,000 ש\"ח", "sale_nb", "UNSOURCED", f"edit {e8}", official="no official median", figures=2)
C("p@12964", "דירת 4 חדרים מושכרת סביב 6,750 עד 6,800, 5 חדרים 8,100 עד 9,100", "rent", "UNSOURCED", "keep (market sources, page checked 5.6.2026)", figures=4)
C("tr@13927", "2 חדרים | מחיר קנייה 1.45 עד 2.21 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e10}", rooms=2, figures=2)
C("tr@14116", "3 חדרים | מחיר קנייה 2.03 עד 3.0 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e10}", rooms=3, official="1,941,300 (10-12.2025)", figures=2)
C("tr@14305", "4 חדרים | מחיר קנייה 2.55 עד 3.7 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e10}", rooms=4, official="2,817,000", figures=2, note="restated as the median")
C("tr@14491", "5 חדרים | מחיר קנייה 3.5 עד 4.5 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e10}", rooms=5, official="3,544,700", figures=2, note="restated as the median")
C("tr@13927..14675", "עמודת שכירות שוק (5 שורות, כולל בית פרטי 13,500 במדגם שוק)", "rent", "UNSOURCED", f"keep (market sample, page checked 5.6.2026; kept word for word in edit {e10})", figures=9)
C("tr@15986..17316", "טבלת עסקאות מאי 2026 (8 עסקאות: מחיר ומחיר למ\"ר)", "deal", "UNSOURCED", "keep (individual dated deals, 3-25.5.2026)", figures=16)
C("p@17534", "דירת 4 חדרים נסגרה לפי כ-28,061 ש\"ח למ\"ר, ואחרת לפי כ-37,303", "per_m2", "UNSOURCED", "keep (from the dated deals table)", rooms=4, figures=2)
C("p@18206", "דירות חדשות: 3 חדרים כ-2.5 עד 3.0 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e11}", rooms=3, official="1,941,300", figures=2, note="new flats")
C("p@18206", "דירות חדשות: 4 חדרים כ-3.1 עד 3.7 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e11}", rooms=4, official="2,817,000", figures=2, note="new flats")
C("p@18206", "דירות חדשות: 5 חדרים כ-3.5 עד 4.5 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e11}", rooms=5, official="3,544,700", figures=2, note="new flats; dropped inside the rewrite")
C("p@18206", "פנטהאוזים יכולים להתחיל סביב 4.0 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e11}", rooms="penthouse")
C("p@18484", "דירת 4 חדרים יד שנייה סביב 2.83 מיליון ש\"ח בממוצע מסוים", "sale", "CONSISTENT", "keep", rooms=4, official="2,817,000 (10-12.2025)", note="second-hand")
C("p@18484", "דירת 5 חדרים יד שנייה סביב 3.75 מיליון ש\"ח בממוצע מסוים", "sale", "CONFLICT", f"edit {e12}", rooms=5, official="3,544,700 (1-3.2026)", note="second-hand, +5.8%")
C("p@25712", "FAQ: המחיר הממוצע נע סביב 2.8 עד 2.85 מיליון ש\"ח", "sale_avg", "CONFLICT", f"edit {e13}", rooms="all", official="all deals 2,415,900", figures=2)
C("p@25990", "FAQ: דירות 3 חדרים כ-2.03 עד 3.0 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e14}", rooms=3, official="1,941,300", figures=2)
C("p@25990", "FAQ: עסקאות במאי 2026: 2,100,000 (63 מ\"ר) ו-2,550,000 (74 מ\"ר)", "deal", "UNSOURCED", f"keep (individual dated deals; word for word inside edit {e14})", rooms=3, figures=2)
C("p@26285", "FAQ: דירות 4 חדרים רבות נעות סביב 2.55 עד 3.7 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e15}", rooms=4, official="2,817,000", figures=2, note="restated as the median")
C("p@26285", "FAQ: עסקאות 2,750,000, 3,000,000, 3,300,000, 3,320,000 (89-102 מ\"ר)", "deal", "UNSOURCED", "keep (individual deals of May 2026, dated in the deals table)", rooms=4, figures=4)
C("p@26540", "FAQ: דירות 5 חדרים נעות לרוב סביב 3.5 עד 4.5 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e16}", rooms=5, official="3,544,700", figures=2, note="restated as the median")
C("p@26540", "FAQ: עסקאות 5 חדרים סביב 3,850,000 עד 3,900,000 ש\"ח", "deal", "UNSOURCED", f"keep (two May 2026 deals; date added inside edit {e16})", rooms=5, figures=2)
C("p@26815", "FAQ שכירות: ממוצע 7,200-7,350; לפי חדרים 4,000-9,100", "rent", "UNSOURCED", "keep (market sources, page checked 5.6.2026)", figures=10)

P.write(notes=(
    "The official list is not on the page yet; new text cites the medians directly. Latest official: 3 and 4 rooms and all deals "
    "10-12.2025 (the last published), 5 rooms 1-3.2026; tables mark the quarter in each cell, as the brief prescribes. "
    "Official quirk: the 3-room median fell 21.3% year on year (2,466,800 in 10-12.2024 to 1,941,300 in 10-12.2025), but the fall happened "
    "in one step (1,993,600 already in 1-3.2025) and the last four quarters are flat; the ranges paragraph shows the previous quarter "
    "(1,960,100) for that reason. The official 3-room median sits below the page's own May 2026 deals (2.1M for 63 m2, 2.55M for 74 m2) "
    "and below the 1-3.2026 centre neighbourhood median (2,106,700); worth a second look at the source series before publishing. "
    "Name mapping: 'כפר סבא הירוקה' = official 'הירוקה כ\"ס 80' (the neighbourhood's planning name, fairly sure); 'מרכז העיר דרום' and "
    "'מרכז העיר צפון' merged into one row for the official 'מרכז'; 'הראשונים' = official 'ראשונים' (the row covers Tkuma and HaRishonim, "
    "the cell says the median is HaRishonim's). "
    "Kept: rents (market sources and a market sample, page checked 5.6.2026), the dated May 2026 deals table and the per-m2 figures drawn "
    "from it, the dated deal examples in the FAQ, and the consistent second-hand 4-room 2.83M. "
    "Not audited as claims (hypotheticals and illustrations): the 3,000,000 / 3,300,000 / 3,700,000 / 700,000 example (p@5866), the "
    "900,000 per-m2 arithmetic (p@8836), the 2,750,000 'if an area average' example (p@12096), the 80,000-300,000 renovation range "
    "(li@21555), the 2,900,000 / 3,050,000 / 250,000 example (p@21840), sizes, ages and deal counts. "
    "The h3 'ממוצע עירוני' heading is kept (no number); its card now opens with the median and calls it a median."))
