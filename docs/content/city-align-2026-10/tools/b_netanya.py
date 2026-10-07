# -*- coding: utf-8 -*-
"""Netanya (page 4577): body alignment with the official price list (1-3.2026; 3 rooms latest 10-12.2025). Data only."""
import re
from mk import Page

P = Page("netanya-apartment-prices")

# ---------------- edits ----------------
# 1. the source note right under the official list called every number on the page a working range
old1 = "המספרים בעמוד זה הם טווחי עבודה שנבנו לפי בדיקת נתוני שוק גלויים מ-6 ביוני 2026, דפי עסקאות, דפי שכירות, דפי מחירון גלויים ומידע רשמי."
new1 = ("חציוני מחיר העסקה במחירון הרשמי בעמוד לקוחים מנתוני רשות המסים, וטווחי העבודה בעמוד נבנו לפי בדיקת נתוני שוק גלויים "
        "מ-6 ביוני 2026, דפי עסקאות, דפי שכירות, דפי מחירון גלויים ומידע רשמי.")
e1 = P.edit(old1, new1, ["data_quarter"], "WORDING",
            "The note under the official list said every number on the page is a working range; the list itself is official medians. "
            "Reworded so the medians and the working ranges are told apart; the 6.6.2026 check date (the dating of the kept rent figures) stays.")

# 2. quick table: 'a pricier flat near the sea, sometimes above 4,000,000'
old2 = "לעיתים מעל 4,000,000 ש\"ח, ובנכסים חריגים גם יותר"
new2 = "לעיתים גבוה בהרבה מחציון מחיר העסקה בעיר, ובנכסים חריגים גם יותר"
e2 = P.edit(old2, new2, ["page"], "UNSOURCED",
            "Sea-side flats 'sometimes above 4,000,000' with no room count, no named source and no period; rephrased without the number "
            "(the official list has no sea-front figure).")

# 3-4. rooms table: 2-room and 6+-room working ranges (no official series, no source)
old3 = "כ-1,100,000 עד 1,850,000 ש\"ח"
new3 = "אין חציון רשמי לדירות 2 חדרים; משווים לעסקאות דומות ברחוב ובשכונה"
e3 = P.edit(old3, new3, ["data_quarter"], "UNSOURCED",
            "2-room working range with no named source; the official list covers 3, 4 and 5 rooms only. The row stays (area, places, checks).")
old4 = "כ-3,400,000 עד 6,500,000 ש\"ח ומעלה"
new4 = "אין חציון רשמי לדירות 6 חדרים ומעלה; משווים לעסקאות דומות ברחוב ובשכונה"
e4 = P.edit(old4, new4, ["data_quarter"], "UNSOURCED",
            "6+-room working range with no named source; no official series. The row stays (area, places, checks).")

# 5. garden / roof premium 10-30% (tier 2: not a price level)
old5 = "תוספת אפשרית של 10% עד 30% לעומת דירה רגילה דומה"
new5 = "לרוב גבוה מדירה רגילה דומה; בודקים מול עסקאות של דירות גן או גג באותו אזור"
e5 = P.edit(old5, new5, ["page"], "UNSOURCED",
            "A 10%-30% garden/roof premium with no source or period; rephrased without the percentages.", tier=2)

# 6. neighbourhood paragraph: official neighbourhood medians in place of the working-range column
old6 = P.find("בבדיקת נתוני שוק גלויים מ-6 ביוני 2026 הופיעו פערים גדולים בין אזורים.", "דירות גדולות או תמהיל בניינים שונה.")
new6 = ("גם בנתוני רשות המסים בולטים פערים גדולים בין אזורים. לפי הנתונים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 4 חדרים "
        "היה 1,967,300 ש\"ח בקריית נורדאו, 2,422,800 ש\"ח במרכז העיר ו-2,463,300 ש\"ח בקריית השרון. בבדיקת נתוני שוק גלויים "
        "מ-6 ביוני 2026 הופיע גם אזור גלי הים כיקר בהרבה מאזורים ותיקים, ושכונת נאות גולדה ברמות מחיר נמוכות יותר. גם חציון שכונתי "
        "יכול להיות מושפע מעסקאות מעטות, דירות קטנות, דירות גדולות או תמהיל בניינים שונה, ולכן הוא נקודת ייחוס ולא מחיר לדירה מסוימת.")
e6 = P.edit(old6, new6, ["neighbourhoods[קריית נורדאו].rooms.4", "neighbourhoods[מרכז העיר].rooms.4", "neighbourhoods[קריית השרון].rooms.4"],
            "UNSOURCED",
            "Intro of the neighbourhood table; the table's working-range price column leaves (edit 7). The official 4-room neighbourhood "
            "medians (1-3.2026) for the three page neighbourhoods that have one are given here; Gali HaYam and Neot Golda stay qualitative.")

# 7. neighbourhood table: drop the 'working range for common flats' column, keep every row and the other columns word for word
anchor7 = '<th dir="rtl">טווח מחיר עבודה לדירות נפוצות</th>'
old7 = P.table_html(anchor7)
rows = old7.split("</tr>")
new_rows = []
for r in rows:
    cells = re.findall(r"\n<t[hd] dir=\"rtl\">.*?</t[hd]>", r)
    if len(cells) == 5:
        r = r.replace(cells[2], "", 1)
    new_rows.append(r)
new7 = "</tr>".join(new_rows)
assert new7.count("<td dir") == 14 * 4 and new7.count("<th dir") == 4 and "ש\"ח" not in new7, (new7.count("<td"), new7.count("<th"))
e7 = P.table(anchor7, new7,
             ["neighbourhoods[קריית נורדאו].rooms.4", "neighbourhoods[מרכז העיר].rooms.4", "neighbourhoods[קריית השרון].rooms.4"], "UNSOURCED",
             "Neighbourhood table: 14 all-rooms 'working ranges for common flats' with no named source and no room count (11 of the 14 "
             "neighbourhoods have no official median). The price column is removed; every row and the other four columns stay word for word. "
             "Official neighbourhood medians are in edit 6 and in the official list.")

# 8-11. 'check item' table: city average of a market page (CONFLICT) and two neighbourhood averages without period
old8 = "ממוצע עירוני בדף שוק"
new8 = "חציון עירוני לפי רשות המסים"
e8 = P.edit(old8, new8, ["rooms.all.latest"], "CONFLICT", "Row label of the city average 1,582,219 (edit 9).")
old9 = "כ-1,582,219 ש\"ח לפי דף נתונים גלוי"
new9 = "2,629,800 ש\"ח בכל סוגי הדירות, ינואר-מרץ 2026"
e9 = P.edit(old9, new9, ["rooms.all.latest"], "CONFLICT",
            "City average 1,582,219 from an unnamed market page (with 76,674 deals: an all-history average) vs the official all-rooms "
            "median 2,629,800 (1-3.2026), the figure the official list shows for 'כל הדירות'.")
old10 = "ממוצע דירות סביב 2,643,946 ש\"ח"
new10 = "ממוצע דירות גבוה בהרבה מאזורים ותיקים"
e10 = P.edit(old10, new10, ["page"], "UNSOURCED",
             "Gali HaYam all-rooms average from an unnamed market page, no period; Gali HaYam has no official median. Rephrased without the number.")
old11 = "ממוצע סביב 869,886 ש\"ח"
new11 = "ממוצע נמוך יותר מרוב אזורי העיר"
e11 = P.edit(old11, new11, ["page"], "UNSOURCED",
             "Neot Golda all-rooms average from an unnamed market page, no period; no official median. Rephrased without the number.")

# 12. FAQ 'how much does a flat cost on average'
old12 = P.find("כטווח עבודה רחב, רבות מהחלטות הקנייה והמכירה בנתניה נעות סביב", "אך יש לראות בהם הקשר רחב ולא שווי לדירה מסוימת.")
new12 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה בנתניה בכל סוגי הדירות היה 2,629,800 ש\"ח, ולדירת 4 חדרים "
         "2,676,100 ש\"ח. כטווח עבודה רחב, רבות מהחלטות הקנייה והמכירה בנתניה נעות סביב 1,500,000 עד 3,500,000 ש\"ח. עם זאת, מספר "
         "עירוני אחד אינו מספיק, מפני שעיר ימים, נוף הטיילת, סי פארק, קריית השרון, מרכז העיר וקריית נורדאו מציגות רמות מחיר שונות, "
         "ולכן יש לראות בו הקשר רחב ולא שווי לדירה מסוימת.")
e12 = P.edit(old12, new12, ["rooms.all.latest", "rooms.4.latest", "page"], "CONFLICT",
             "FAQ on the city average pointed at 'lower city averages' of market pages (the 1,582,219 of edit 9); answered with the official "
             "all-rooms median 2,629,800 and the 4-room median (1-3.2026). The consistent 1.5-3.5M working range stays.")

# ---------------- claims inventory ----------------
C = P.claim
ALL = "all rooms 2,629,800 (1-3.2026); 3/4/5 medians 1,791,300 / 2,676,100 / 3,365,300 inside"
C("p@4366", "חלק גדול מהחלטות הקנייה והמכירה בנתניה סביב 1,500,000 עד 3,500,000 ש\"ח", "sale_avg", "CONSISTENT", "keep (consistent)", official=ALL)
C("p@4366", "דירות משפחתיות נפוצות ... סביב 5,000 עד 8,000 ש\"ח לחודש", "rent", "UNSOURCED", "keep (rent listing pages, page checked 6.6.2026, p@42050)")
C("p@42531", "דירות רגילות נבדקות סביב 1.5 עד 3.5 מיליון ש\"ח", "sale_avg", "CONSISTENT", "keep (consistent)", official=ALL)
C("p@42783", "שכירות של דירות משפחתיות ... סביב 5,000 עד 8,000 ש\"ח לחודש", "rent", "UNSOURCED", "keep (rent listing pages, page checked 6.6.2026)")
C("tr@43379", "כמה עולה דירה רגילה | כ-1,500,000 עד 3,500,000 ש\"ח", "sale_avg", "CONSISTENT", "keep (consistent)", official=ALL)
C("tr@43572", "דירה יקרה יותר ליד הים | לעיתים מעל 4,000,000 ש\"ח", "sale_nb", "UNSOURCED", f"edit {e2}", note="no room count, no source; no official sea-front figure")
C("tr@43776", "שכירות נפוצה לדירת משפחה | כ-5,000 עד 8,000 ש\"ח לחודש", "rent", "UNSOURCED", "keep (rent listing pages, page checked 6.6.2026)")
C("tr@45674", "2 חדרים | כ-1,100,000 עד 1,850,000 ש\"ח", "sale", "UNSOURCED", f"edit {e3}", rooms=2, note="no official 2-room series")
C("tr@45932", "3 חדרים | כ-1,450,000 עד 2,350,000 ש\"ח", "sale", "CONSISTENT", "keep (consistent)", rooms=3, official="1,791,300 (10-12.2025, latest published)")
C("tr@46183", "4 חדרים | כ-1,950,000 עד 3,250,000 ש\"ח", "sale", "CONSISTENT", "keep (consistent)", rooms=4, official="2,676,100 (1-3.2026)")
C("tr@46436", "5 חדרים | כ-2,450,000 עד 4,200,000 ש\"ח", "sale", "CONSISTENT", "keep (consistent)", rooms=5, official="3,365,300 (1-3.2026)")
C("tr@46691", "6 חדרים ומעלה | כ-3,400,000 עד 6,500,000 ש\"ח ומעלה", "sale", "UNSOURCED", f"edit {e4}", rooms=6, note="no official 6+-room series")
C("tr@46965", "דירת גן או גג | תוספת 10% עד 30% לעומת דירה רגילה", "other", "UNSOURCED", f"edit {e5}", figures=2, note="tier 2")
C("tr@49041..52425", "טבלת טווחי מחיר עבודה לפי שכונה (14 שורות, כל סוגי הדירות)", "sale_nb", "UNSOURCED", f"edit {e7}", figures=14,
  official="קריית נורדאו 4r 1,967,300; מרכז העיר 4r 2,422,800; קריית השרון 4r 2,463,300 (1-3.2026)",
  note="no room count; the three neighbourhoods with official medians are given in edit 6")
C("p@53106", "226 מודעות (16.4.2026); שכירות ממוצעת 6,265, חציון 5,300", "rent", "UNSOURCED", "keep (listing data, dated 16.4.2026 / page checked 6.6.2026)", figures=3)
C("tr@54188..55777", "טבלת שכירות (9 שורות): 226 מודעות, 6,265, 5,300, 1 חדר 3,800, 3 חדרים 4,500-6,300, 4 חדרים 5,500-7,500, 5 חדרים בסי פארק 8,000", "rent",
  "UNSOURCED", "keep (listing sample, page checked 6.6.2026)", figures=11)
C("p@56722", "סמילנסקי 26: 3 חדרים, 73 מ\"ר, 1,900,000 ש\"ח, 18 בנובמבר 2024, כ-26,027 ש\"ח למ\"ר", "deal", "UNSOURCED",
  "keep (one specific dated deal, 18.11.2024, not presented as the level)", rooms=3, figures=2, official="3 rooms 1,791,300 (10-12.2025), not compared (single deal)")
C("tr@57313", "עסקת סמילנסקי 26 | 1,900,000 ש\"ח, 18 בנובמבר 2024 | כ-26,027 ש\"ח למ\"ר", "deal", "UNSOURCED", "keep (one specific dated deal)", rooms=3, figures=2)
C("tr@57581", "דף נתונים גלוי הציג כ-76,674 עסקאות בנתניה", "count", "UNSOURCED", "keep (a count, not a price; labelled historic depth, page checked 6.6.2026)")
C("tr@57814", "ממוצע עירוני בדף שוק | כ-1,582,219 ש\"ח", "sale_avg", "CONFLICT", f"edit {e9}", official="all rooms 2,629,800 (1-3.2026)", note=f"label in edit {e8}")
C("tr@58033", "גלי הים בדף שוק | ממוצע דירות סביב 2,643,946 ש\"ח", "sale_nb", "UNSOURCED", f"edit {e10}", note="all rooms, no period; no official median for Gali HaYam")
C("tr@58257", "נאות גולדה בדף שוק | ממוצע סביב 869,886 ש\"ח", "sale_nb", "UNSOURCED", f"edit {e11}", note="all rooms, no period; no official median for Neot Golda")
C("tr@58472", "הלמ\"ס 077/2026: נובמבר 2025 עד ינואר 2026 נמכרו 234 דירות חדשות ו-421 יד שנייה", "count", "UNSOURCED", "keep (CBS release 077/2026, dated)", figures=2)
C("tr@58755", "הלמ\"ס: כ-24,120 דירות נמכרו בארץ, 37.6% חדשות ו-62.4% יד שנייה", "count", "UNSOURCED", "keep (CBS release 077/2026, national)", figures=3)
C("tr@58985", "בנק ישראל, 25 במאי 2026: הריבית ירדה ב-0.25 ל-3.75%", "macro", "UNSOURCED", "keep (dated Bank of Israel decision, 25.5.2026)", figures=2)
C("tr@59227", "הודעת בנק ישראל: עלייה של 0.3% בפברואר עד מרץ, ירידה שנתית של 1.2%", "macro", "UNSOURCED", "keep (Bank of Israel announcement, May 2026; national)", figures=2)
C("p@61416", "הלמ\"ס נובמבר 2025 עד ינואר 2026: 234 חדשות ו-421 יד שנייה", "count", "UNSOURCED", "keep (CBS, dated period)", figures=2)
C("p@69608", "FAQ ממוצע: רבות מההחלטות סביב 1,500,000 עד 3,500,000 ש\"ח", "sale_avg", "CONSISTENT", f"edit {e12}", official=ALL, note="kept word for word inside the FAQ rewrite")
C("p@69608", "FAQ ממוצע: 'דפי נתוני שוק הציגו גם ממוצעים עירוניים נמוכים יותר'", "sale_avg", "CONFLICT", f"edit {e12}",
  official="all rooms 2,629,800 (1-3.2026)", note="no digit; points at the 1,582,219 market-page average")
C("p@70001", "FAQ למ\"ר: בדוגמת סמילנסקי 26 כ-26,027 ש\"ח למ\"ר", "per_m2", "UNSOURCED", "keep (one specific deal, dated 18.11.2024 in the body)")
C("p@70343", "FAQ 3 חדרים: כ-1,450,000 עד 2,350,000 ש\"ח", "sale", "CONSISTENT", "keep (consistent)", rooms=3, official="1,791,300 (10-12.2025)")
C("p@70651", "FAQ 4 חדרים: כ-1,950,000 עד 3,250,000 ש\"ח", "sale", "CONSISTENT", "keep (consistent)", rooms=4, official="2,676,100 (1-3.2026)")
C("p@70967", "FAQ 5 חדרים: כ-2,450,000 עד 4,200,000 ש\"ח", "sale", "CONSISTENT", "keep (consistent)", rooms=5, official="3,365,300 (1-3.2026)")

P.write(notes=(
    "Not audited as claims (illustrations or structure, not market statements): the 'gap of more than 1,000,000' between extremes (p@44992), "
    "the m2 assumptions 55/80/110/130 (p@47279), the if-example 2,850,000 / 105 m2 / 27,143 per m2 / 2,600,000 / 250,000 (p@47596), the 700 rent "
    "gap example (p@56011), the if-example 2,900,000 vs 2,650,000-2,750,000 (FAQ p@72247), step counts (5-8 deals, 3-6 listings), days on market "
    "(60/90/120). The 3/4/5-room working ranges of the rooms table and the FAQ contain the official medians (3 rooms: 10-12.2025 is the latest "
    "published quarter) and are kept; only the 2-room, 6+-room and garden/roof cells lose their numbers, the rows stay. Rent figures are kept: "
    "the page names listing pages and dates its check (6.6.2026; 226 listings 16.4.2026). Remaining SUSPECT lines after the edits are the "
    "explicit if-example (p@47596, 2,850,000 for 4 rooms) and the single dated Smilansky 26 deal (1,900,000, 18.11.2024). The official file "
    "also lists neighbourhoods the page does not name (מע\"ר - מרכז עירוני ר, אבו שדיד, רמת אפרים, מכנס, פרדס הגדוד); they are not added. "
    "Name mapping: page 'מרכז העיר' = official 'מרכז העיר' (not the separate 'מע\"ר - מרכז עירוני ר'), 'קריית נורדאו' and 'קריית השרון' exact. "
    "Official quirk: Kiryat Nordau 5 rooms 3,882,100 is above the city 5-room median; not quoted."))
