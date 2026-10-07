# -*- coding: utf-8 -*-
"""Bat Yam (page 4583): body alignment with the official price list (1-3.2026). Built on the Ashkelon gold example."""
import re
from mk import Page

P = Page("bat-yam-apartment-prices")


def tbl(headers, rows):
    """table in this page's own style: one line, <thead>/<tr>/<tbody> without dir, dir="rtl" on th/td."""
    h = "".join(f'<th dir="rtl">{x}</th>' for x in headers)
    b = "".join("<tr>" + "".join(f'<td dir="rtl">{x}</td>' for x in r) + "</tr>" for r in rows)
    return f'<table dir="rtl"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


def rows_of(anchor):
    html = P.table_html(anchor)
    return [re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S) for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", html.split("<tbody", 1)[1], re.S)]


# ---------------- edits ----------------
# 1. lead paragraph above the price list
old1 = P.find("מחירי דירות בבת ים נעים כיום בטווח רחב:", "לא שומה ולא מחיר מחייב.")
new1 = ("מחירי דירות בבת ים, לפי נתוני רשות המסים לרבעון הראשון של 2026: חציון מחיר העסקה היה 1,823,700 ₪ לדירת 3 חדרים, "
        "2,692,600 ₪ לדירת 4 חדרים ו-3,468,600 ₪ לדירת 5 חדרים, ו-1,901,500 ₪ לכל הדירות. דירות קטנות וישנות יכולות להופיע "
        "במחירים נמוכים יותר, ודירות גדולות, חדשות או קרובות לים יכולות להגיע לסכומים גבוהים בהרבה. באתרי נתונים פרטיים מחיר "
        "למ״ר מוצג לעיתים סביב 29,000 ₪, אך זה נתון סטטיסטי בלבד, לא שומה ולא מחיר מחייב.")
e1 = P.edit(old1, new1, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "rooms.all.latest", "page"], "CONFLICT",
            "Lead above the list: the 'average shown on private data sites' 2,450,000 is far from the official all-apartments median 1,901,500 "
            "(1-3.2026). The 3- and 4-room ranges were consistent and are restated as the medians; the undated small-flat and large/new-flat "
            "ranges are dropped; the per-m2 figure (private data sites, named in the recent-deals section, page checked 6.6.2026) is kept.")

# 1b. the 2.3M illustration becomes an explicit if-example anchored on the official medians
old1b = "לכן מחיר של 2,300,000 ₪ לדירת 3 חדרים יכול להיות גבוה באזור אחד, סביר באזור שני ונמוך באזור שלישי, בהתאם לגודל, בניין, קומה, חניה, נוף ועסקאות אחרונות."
new1b = ("לכן אם דירת 3 חדרים מוצעת ב-2,300,000 ₪, המחיר יכול להיות גבוה באזור אחד וסביר באזור אחר, בהתאם לגודל, בניין, קומה, "
         "חניה, נוף ועסקאות אחרונות: לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 3 חדרים היה 1,823,700 ₪ "
         "בכל העיר ו-2,322,100 ₪ ברמת יוסף.")
e1b = P.edit(old1b, new1b, ["rooms.3.latest", "neighbourhoods[רמת יוסף].rooms.3", "page"], "WORDING",
             "Illustration of spread ('2.3M for 3 rooms can be high in one area, reasonable in a second and low in a third'): no official "
             "3-room median is above 2,322,100 (Ramat Yosef), so 'low' is dropped and the example is made an explicit if-example next to the "
             "city and Ramat Yosef medians. Not counted as a claim.")

# 2. sentence before the rooms table
old2 = P.find("טבלת החדרים היא נקודת הכניסה למחירון.", "גם אם שתיהן מופיעות באותה קטגוריית חדרים.")
new2 = ("הטבלה הבאה מציגה את חציון מחיר העסקה בבת ים לפי מספר חדרים, לפי נתוני רשות המסים לרבעון הראשון של 2026, לצד החציון "
        "באותו רבעון שנה קודם לכן. היא נקודת הכניסה למחירון, ולא מיועדת לקבוע מחיר סופי, אלא לסנן דירות, להבין האם מודעה נמצאת "
        "מעל או מתחת לשוק, ולהכין שאלות לבדיקה. בבת ים יש משקל גדול לשטח בפועל: דירת 3 חדרים של 62 מ״ר ודירת 3 חדרים של 82 מ״ר "
        "לא שייכות לאותו טווח מעשי, גם אם שתיהן מופיעות באותה קטגוריית חדרים. המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; "
        "דירות קטנות של עד 2 חדרים, דירות גן או גג ודירות חדשות כדאי לבדוק מול עסקאות דומות ברחוב ובשכונה.")
e2 = P.edit(old2, new2, ["data_quarter"], "WORDING", "Introduces the replaced rooms table (edit 4); the small-flat, garden/roof and new-flat rows leave it.")

# 3. rooms table
A3 = '<th dir="rtl">טווח מחיר בדיקה</th>'
R3 = {r[0]: r for r in rows_of(A3)}
new3 = tbl(["סוג דירה", "חציון מחיר העסקה, ינואר-מרץ 2026", "ינואר-מרץ 2025", "שינוי בשנה", "מה מעלה מחיר", "מה מוריד מחיר"], [
    ["3 חדרים", "1,823,700 ₪", "1,844,800 ₪", "ירידה של 1.1%", R3["2.5-3 חדרים"][3], R3["2.5-3 חדרים"][4]],
    ["4 חדרים", "2,692,600 ₪", "2,582,700 ₪", "עלייה של 4.3%", R3["3.5-4 חדרים"][3], R3["3.5-4 חדרים"][4]],
    ["5 חדרים", "3,468,600 ₪", "3,069,800 ₪", "עלייה של 13%", R3["4.5-5 חדרים"][3], R3["4.5-5 חדרים"][4]],
])
e3 = P.table(A3, new3, ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct",
                        "rooms.5.latest", "rooms.5.year_ago", "rooms.5.change_pct"], "UNSOURCED",
             "Rooms table: the 'checking ranges' for 2.5-3, 3.5-4 and 4.5-5 rooms contained the official medians (consistent), but the 1-2 room, "
             "garden/roof and new-flat ranges have no source or date. Replaced by the official 3/4/5-room medians with the year-earlier quarter; "
             "the 'raises / lowers the price' notes of those rows are kept word for word (the common-size column is dropped).")

# 4. seller paragraph pointed at the removed ranges
old4 = "מוכר צריך להשתמש בטווחי המחיר בצורה הפוכה:"
new4 = "מוכר צריך להשתמש בנתוני המחיר בצורה הפוכה:"
e4 = P.edit(old4, new4, ["page"], "WORDING", "Follows edit 4: the table no longer shows price ranges.")

# 5. neighbourhood paragraph: official neighbourhood medians replace the range column of the area table
old5 = "לכן השוואה בין 2 דירות באותה שכונה חייבת לרדת לרמת רחוב, בניין וקומה."
new5 = (old5 + " כנקודת פתיחה, לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 3 חדרים היה 2,322,100 ₪ ברמת "
        "יוסף, 2,014,800 ₪ בדרום מערב העיר, 1,757,100 ₪ במרכז העיר ו-1,696,800 ₪ ברמת הנשיא, ולדירת 4 חדרים 3,010,600 ₪ בצפון מערב "
        "העיר ו-2,591,300 ₪ במרכז העיר.")
e5 = P.edit(old5, new5, ["neighbourhoods[רמת יוסף].rooms.3", "neighbourhoods[דרום-מערב].rooms.3", "neighbourhoods[מרכז העיר].rooms.3",
                         "neighbourhoods[רמת הנשיא].rooms.3", "neighbourhoods[צפון-מערב].rooms.4", "neighbourhoods[מרכז העיר].rooms.4"], "UNSOURCED",
            "The area table's 3-4 room ranges (edit 7) leave; official neighbourhood medians are given in the paragraph that introduces it.")

# 6. area table: drop the unsourced range column, keep the areas and the page's notes
A6 = '<th dir="rtl">טווח מחיר אופייני לדירות 3-4 חדרים</th>'
new6 = tbl(["אזור בדיקה", "מאפייני ביקוש", "שאלות שצריך לשאול"], [[r[0], r[2], r[3]] for r in rows_of(A6)])
e6 = P.table(A6, new6, ["neighbourhoods[צפון-מערב].rooms.3", "neighbourhoods[דרום-מערב].rooms.3", "neighbourhoods[מרכז העיר].rooms.3"], "CONFLICT",
             "Area table: the 3-4 room ranges of the west (from 2.25M) and the centre (from 1.8M) exclude the official 3-room medians of "
             "North-West 1,906,800, South-West 2,014,800 and the city centre 1,757,100; the other four rows (south, renewal areas, old interior "
             "buildings, new towers) have no source, no date and no official counterpart. The price column is removed; areas, demand notes "
             "and questions are kept word for word.")

# 7. rent and yield table: purchase prices -> official medians, yield column removed
A7 = '<th dir="rtl">יחס שנתי גס לפני הוצאות</th>'
MED = {"2 חדרים": "לא פורסם", "3 חדרים": "1,823,700 ₪", "4 חדרים": "2,692,600 ₪", "5 חדרים": "3,468,600 ₪"}
R7 = [r for r in rows_of(A7) if r[0] in MED]
assert len(R7) == 4
new7 = tbl(["סוג דירה", "שכירות חודשית לבדיקת שוק", "חציון מחיר העסקה, ינואר-מרץ 2026", "מה לבדוק מעבר למספר"],
           [[r[0], r[1], MED[r[0]], r[4]] for r in R7])
e7 = P.table(A7, new7, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "UNSOURCED",
             "Rent table: the purchase column repeats the checking ranges (3-5 rooms consistent, 2 rooms and new flats near the sea unsourced) and "
             "the gross-ratio column is derived from them. Purchase prices replaced by the official medians, the ratio column and the unsourced "
             "'new flat near the sea' row removed (no new arithmetic); the 2-5 room rent ranges and notes are kept word for word.")

# 8. private-site average in the recent-deals section
old8 = P.find("אתר Dirobot, שהוא אתר נתוני עסקאות ולא מקור רשמי, הציג לבת ים מחיר ממוצע סביב 2,450,000 ₪", "נתוני רשות המסים לעסקאות בפועל.")
new8 = ("אתר Dirobot, שהוא אתר נתוני עסקאות ולא מקור רשמי, הציג לבת ים מחיר למ״ר סביב 29,000 ₪ וכ-2,425 עסקאות. נתוני אתרים כאלה "
        "יכולים לעזור בהשוואה ראשונית, אך המקור הרשמי לבדיקה הוא אתר הנדל״ן הממשלתי או נתוני רשות המסים לעסקאות בפועל: לפי נתוני "
        "רשות המסים, חציון מחיר העסקה לכל הדירות בבת ים ברבעון הראשון של 2026 היה 1,901,500 ₪.")
e8 = P.edit(old8, new8, ["rooms.all.latest", "page"], "CONFLICT",
            "A private site's city average 2,450,000 vs the official all-apartments median 1,901,500; the named site's per-m2 figure and deal count "
            "are kept (page checked 6.6.2026).")

# 9. deals table: keep the three dated deals, drop the 'average flat by a private site' row
A9 = '<th dir="rtl">מחיר למ״ר מחושב</th>'
R9 = rows_of(A9)
assert all(r[1] == "מרץ 2026" for r in R9[:3]) and "2,450,000" in R9[3][3] and len(R9) == 4
new9 = tbl(["דוגמת עסקה לבדיקה", "חודש ושנה", "שטח", "מחיר עסקה", "מחיר למ״ר מחושב", "איך להשתמש בזה"], R9[:3])
e9 = P.table(A9, new9, ["page"], "CONFLICT",
             "Deals table: the last row puts the private site's 2,450,000 city average next to real deals (official all-apartments median "
             "1,901,500); the row is removed. The three deals dated March 2026 are kept word for word.")

# 10-12. FAQ answers
old10 = P.find("אתרי נתונים פרטיים מציגים לעיתים מחיר ממוצע סביב 2,450,000 ₪", "יכולות להגיע ל-4,000,000-6,500,000 ₪ ואף יותר.")
new10 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לכל הדירות בבת ים ברבעון הראשון של 2026 היה 1,901,500 ₪, ולפי מספר חדרים: "
         "1,823,700 ₪ לדירת 3 חדרים, 2,692,600 ₪ לדירת 4 חדרים ו-3,468,600 ₪ לדירת 5 חדרים. אתרי נתונים פרטיים מציגים לעיתים מחיר "
         "למ״ר סביב 29,000 ₪, אך זהו נתון סטטיסטי בלבד. דירות קטנות וישנות יכולות להופיע במחירים נמוכים יותר, ודירות חדשות, גדולות "
         "או קרובות לים יכולות להגיע לסכומים גבוהים בהרבה.")
e10 = P.edit(old10, new10, ["rooms.all.latest", "rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
             "FAQ average flat: 2,450,000 vs the official all-apartments median 1,901,500; the small-flat and new/large-flat ranges have no source "
             "and are rephrased without numbers; the per-m2 figure of private data sites is kept.")

old11 = "דירת 3 חדרים בבת ים נעה בדרך כלל סביב 1,650,000-2,450,000 ₪, אך דירה משופצת, עם מעלית, חניה, מרפסת או מיקום מערבי יכולה לחרוג למעלה."
new11 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים בבת ים ברבעון הראשון של 2026 היה 1,823,700 ₪, לעומת 1,844,800 ₪ "
         "שנה קודם לכן. דירה משופצת, עם מעלית, חניה, מרפסת או מיקום מערבי יכולה לחרוג למעלה.")
e11 = P.edit(old11, new11, ["rooms.3.latest", "rooms.3.year_ago"], "CONSISTENT",
             "FAQ 3 rooms: 1,650,000-2,450,000 contained the official 1,823,700; rewritten from the same facts as the body.")

old12 = "דירות 4 חדרים רבות נמצאות בטווח בדיקה של 2,150,000-3,250,000 ₪."
new12 = "לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים בבת ים ברבעון הראשון של 2026 היה 2,692,600 ₪, לעומת 2,582,700 ₪ שנה קודם לכן."
e12 = P.edit(old12, new12, ["rooms.4.latest", "rooms.4.year_ago"], "CONSISTENT",
             "FAQ 4 rooms: 2,150,000-3,250,000 contained the official 2,692,600; rewritten from the same facts as the body.")

# ---------------- claims inventory ----------------
C = P.claim
C("p@4373", "דירות קטנות וישנות סביב 1,450,000-1,900,000 ₪", "sale", "UNSOURCED", f"edit {e1}", note="no room count, no source; dropped")
C("p@4373", "דירות 3 חדרים רבות סביב 1,800,000-2,450,000 ₪", "sale", "CONSISTENT", f"edit {e1}", rooms=3, official="1,823,700 (1-3.2026)", note="restated as the median")
C("p@4373", "דירות 4 חדרים סביב 2,250,000-3,200,000 ₪", "sale", "CONSISTENT", f"edit {e1}", rooms=4, official="2,692,600 (1-3.2026)", note="restated as the median")
C("p@4373", "דירות גדולות, חדשות או קרובות לים 3,500,000-5,500,000 ₪", "sale", "UNSOURCED", f"edit {e1}", note="no room count, no source; dropped")
C("p@4373", "מחיר ממוצע באתרי נתונים פרטיים סביב 2,450,000 ₪", "sale_avg", "CONFLICT", f"edit {e1}", rooms="all", official="1,901,500 (all apartments, 1-3.2026)")
C("p@4373", "מחיר למ״ר סביב 29,000 ₪", "per_m2", "UNSOURCED", "keep (private data site, named Dirobot in p@53743, page checked 6.6.2026)")
C("p@41875", "מדדירות: 2,675 דירות למכירה, שכירות מבוקשת 5,500 ₪; Realta: 5,760 ₪", "rent", "UNSOURCED", "keep (named listing sources, page checked 6.6.2026)", figures=2)
C("p@43650", "למ״ס 15.3.2026: -0.1% / -0.9% ארצי; מחוז ת״א +0.7% / -2.8%", "macro", "UNSOURCED", "keep (dated CBS release, 15.3.2026)", figures=4)
C("p@44056", "בנק ישראל 25.5.2026: -0.25 נקודה ל-3.75%; 85,000 דירות חדשות במלאי", "macro", "UNSOURCED", "keep (dated Bank of Israel release, 25.5.2026)", figures=3)
C("tr@45415", "1-2 חדרים | 1,250,000-1,850,000 ₪", "sale", "UNSOURCED", f"edit {e3}", rooms=2)
C("tr@45645", "2.5-3 חדרים | 1,650,000-2,450,000 ₪", "sale", "CONSISTENT", f"edit {e3}", rooms=3, official="1,823,700")
C("tr@45882", "3.5-4 חדרים | 2,150,000-3,250,000 ₪", "sale", "CONSISTENT", f"edit {e3}", rooms=4, official="2,692,600")
C("tr@46109", "4.5-5 חדרים | 2,850,000-4,400,000 ₪", "sale", "CONSISTENT", f"edit {e3}", rooms=5, official="3,468,600")
C("tr@46343", "דירת גן או גג | 3,200,000-5,800,000 ₪", "other", "UNSOURCED", f"edit {e3}")
C("tr@46591", "דירה חדשה או כמעט חדשה | 2,700,000-6,500,000 ₪", "sale_new_used", "UNSOURCED", f"edit {e3}")
C("tr@48371", "מערב העיר וקרבה לים | 2,250,000-4,800,000 ₪ (3-4 חדרים)", "sale_nb", "CONFLICT", f"edit {e6}", rooms="3-4",
  official="North-West 3/4: 1,906,800 / 3,010,600; South-West 3/4: 2,014,800 / 2,928,200", note="the 3-room medians fall below the floor")
C("tr@48593", "מרכז בת ים | 1,800,000-2,900,000 ₪ (3-4 חדרים)", "sale_nb", "CONFLICT", f"edit {e6}", rooms="3-4",
  official="city centre 3/4: 1,757,100 / 2,591,300", note="3-room median 1.4% below the floor tolerance")
C("tr@48797", "דרום בת ים | 1,750,000-3,100,000 ₪", "sale_nb", "UNSOURCED", f"edit {e6}", rooms="3-4", note="no official area of that name; not mapped")
C("tr@49006..49473", "התחדשות / בניינים ותיקים פנימיים / חדשות ומגדלים: 1.5-6.5 מיליון", "other", "UNSOURCED", f"edit {e6}", figures=3)
C("p@50953", "מדדירות: 4,200 / 4,600 / 6,600 / 8,950 ₪ לפי חדרים; Realta 5,760 ₪", "rent", "UNSOURCED", "keep (named listing sources, page checked 6.6.2026)", figures=5)
C("tr@51672..52244", "טבלת שכירות: 3,800-4,800 / 4,300-5,600 / 5,800-7,200 / 7,200-9,500 ₪", "rent", "UNSOURCED",
  "keep (checking ranges around the named listing figures of p@50953, page checked 6.6.2026)", figures=4)
C("tr@51672", "טבלת שכירות: מחיר קנייה 2 חדרים 1,300,000-1,850,000 ₪", "sale", "UNSOURCED", f"edit {e7}", rooms=2)
C("tr@51864", "טבלת שכירות: מחיר קנייה 3 חדרים 1,650,000-2,450,000 ₪", "sale", "CONSISTENT", f"edit {e7}", rooms=3, official="1,823,700")
C("tr@52056", "טבלת שכירות: מחיר קנייה 4 חדרים 2,150,000-3,250,000 ₪", "sale", "CONSISTENT", f"edit {e7}", rooms=4, official="2,692,600")
C("tr@52244", "טבלת שכירות: מחיר קנייה 5 חדרים 2,850,000-4,400,000 ₪", "sale", "CONSISTENT", f"edit {e7}", rooms=5, official="3,468,600")
C("tr@51672..52441", "יחס שנתי גס 2.5%-4.0% ... 1.8%-3.8%", "yield", "UNSOURCED", f"edit {e7}", figures=5, note="derived from the checking ranges; column removed, no new yield computed")
C("tr@52441", "דירה חדשה קרובה לים | 7,500-13,000 ₪ | 3,500,000-6,500,000 ₪", "sale_new_used", "UNSOURCED", f"edit {e7}", figures=2, note="row removed with its unsourced rent")
C("p@53743", "Dirobot: מחיר ממוצע סביב 2,450,000 ₪", "sale_avg", "CONFLICT", f"edit {e8}", rooms="all", official="1,901,500")
C("p@53743", "Dirobot: מחיר למ״ר סביב 29,000 ₪", "per_m2", "UNSOURCED", "keep (named private site, page checked 6.6.2026)")
C("tr@54317..54758", "3 עסקאות מרץ 2026: 1,470,000 / 2,800,000 / 2,350,000 ₪ (ו-למ״ר מחושב)", "deal", "UNSOURCED", "keep (individual deals dated March 2026)", figures=6)
C("tr@54970", "דירה ממוצעת לפי אתר נתונים פרטי | כ-2,450,000 ₪ | כ-29,000 ₪ למ״ר", "sale_avg", "CONFLICT", f"edit {e9}", rooms="all", official="1,901,500", figures=2)
C("p@56302", "למ״ס 15.3.2026: דירות חדשות -0.1%, -0.4% בניכוי תמיכה", "macro", "UNSOURCED", "keep (dated CBS release, 15.3.2026)", figures=2)
C("p@62414", "FAQ: מחיר ממוצע סביב 2,450,000 ₪", "sale_avg", "CONFLICT", f"edit {e10}", rooms="all", official="1,901,500")
C("p@62414", "FAQ: מחיר למ״ר סביב 29,000 ₪", "per_m2", "UNSOURCED", "keep (private data sites, page checked 6.6.2026)")
C("p@62414", "FAQ: דירות קטנות 1,250,000-1,850,000; חדשות או גדולות 4,000,000-6,500,000 ₪", "sale", "UNSOURCED", f"edit {e10}", figures=2)
C("p@62740", "FAQ: דירת 3 חדרים 1,650,000-2,450,000 ₪", "sale", "CONSISTENT", f"edit {e11}", rooms=3, official="1,823,700")
C("p@63011", "FAQ: דירות 4 חדרים 2,150,000-3,250,000 ₪", "sale", "CONSISTENT", f"edit {e12}", rooms=4, official="2,692,600")
C("p@63266", "FAQ שכירות: מדדירות 5,500 ₪; Realta 5,760 ₪", "rent", "UNSOURCED", "keep (named listing sources, page checked 6.6.2026)", figures=2)

P.write(notes=(
    "Not audited as claims (illustrations, not market statements): the 2,300,000 3-room spread illustration (p@43263, reworded in edit 2 as an "
    "explicit if-example; official 3-room neighbourhood medians run from 1,696,800 to 2,322,100), the "
    "2,350,000 / 180,000 example (p@46854), the 2,200,000 / 2,550,000 seller example (p@47278), the 150,000-300,000 one-feature gap (p@47609), "
    "the yield example 2,000,000 / 5,000 / 60,000 / 3.0% (p@52670), the if-example 5,200 / 2,600,000 / 2.4% (p@53145), the 300-700 / "
    "3,600-8,400 arithmetic (p@53451), the two dated deals repeated in p@55229, the 200,000-500,000 renewal premium (p@58144), renovation "
    "100,000-300,000 and purchase costs 3%-12% in the checks table (rule-of-thumb magnitudes), the 'נניח' offer example (p@60916) and the "
    "1,900,000 seller example (p@61316). The page names its listing and data sites (מדדירות, Realta, Dirobot) and shows its check date "
    "(עודכן ונבדק: 2026-06-06), so their rent, per-m2 and count figures are kept; the private-site city average 2,450,000 is replaced "
    "everywhere by the official all-apartments median. Unsure: the area table rows are categories (west and sea, centre, south, renewal "
    "areas, old interior buildings, new towers), not official neighbourhoods; only 'west' (North-West / South-West) and 'centre' (מרכז העיר) "
    "were compared, 'south' was not mapped to Ramat HaNasi, Amidar or Ramat Yosef. The common-size column of the rooms table (35-160 m2) is "
    "dropped with the table; sizes are not claims. Official quirks: the 5-room median rose 13% in a year (3,069,800 to 3,468,600) and the "
    "5-room series has no median in 10-12.2024, 4-6.2025 and 10-12.2025; Ramat HaNasi shows 1,696,800 for 3 rooms but 3,003,900 for 4 "
    "rooms. Name mapping: 'דרום מערב העיר' = official 'דרום-מערב', 'צפון מערב העיר' = 'צפון-מערב'. Remaining SUSPECT lines, if any, are "
    "the individual deals dated March 2026 or the explicit illustrations above."))
