# -*- coding: utf-8 -*-
"""Ramat Gan (page 4570): body alignment with the official price list (1-3.2026). Data only."""
from mk import Page

P = Page("ramat-gan-apartment-prices")

# ---------------- edits ----------------
# 1. market-data table: share of the Tel Aviv district in the national housing stock, no source (tier 2)
old1 = "19.5%"
new1 = "נתח ניכר מהמלאי הארצי"
e1 = P.edit(old1, new1, ["page"], "UNSOURCED",
            "A 19.5% share of the Tel Aviv district in the national housing stock with no named source or period; rephrased without the number.",
            tier=2)

# 2-4. rooms table: 1-room, 2-room and 6+-room working ranges (no official series, no source); rows stay
old2 = "כ-1,300,000 עד 2,000,000 ש\"ח"
new2 = "אין חציון רשמי לדירות חדר אחד; משווים לעסקאות דומות ברחוב ובשכונה"
e2 = P.edit(old2, new2, ["data_quarter"], "UNSOURCED",
            "1-room working range with no named source; the official list covers 3, 4 and 5 rooms only. The row stays (area, rent, checks).")
old3 = "כ-1,790,000 עד 2,500,000 ש\"ח"
new3 = "אין חציון רשמי לדירות 2 חדרים; משווים לעסקאות דומות ברחוב ובשכונה"
e3 = P.edit(old3, new3, ["data_quarter"], "UNSOURCED",
            "2-room working range with no named source (its floor is one dated deal, HaMaagal 37); no official 2-room series. The row stays.")
old4 = "כ-5,500,000 ש\"ח ומעלה"
new4 = "אין חציון רשמי לדירות 6 חדרים ומעלה; משווים לעסקאות דומות ברחוב ובשכונה"
e4 = P.edit(old4, new4, ["data_quarter"], "UNSOURCED", "6+-room floor with no named source; no official 6+-room series. The row stays.")

# 5. street averages paragraph -> official neighbourhood medians
old5 = P.find("במחירי מכירה לפי רחובות, דפי שוק שנבדקו הציגו לדוגמה 192 עסקאות", "רחוב ממוצע אינו מספיק: צריך להבין אילו דירות יצרו את הממוצע.")
new5 = ("במחירי מכירה לפי שכונה, לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 4 חדרים היה 3,014,100 ש\"ח "
        "במתחם נגבה, 3,133,700 ש\"ח בנחלת גנים, 3,231,300 ש\"ח ביד לבנים ו-3,991,600 ש\"ח בחרוזים. גם ממוצע של רחוב אינו מספיק: "
        "צריך להבין אילו דירות יצרו אותו, ולהשוות לעסקאות דומות באותו רחוב.")
e5 = P.edit(old5, new5, ["neighbourhoods[מתחם נגבה].rooms.4", "neighbourhoods[נחלת גנים].rooms.4", "neighbourhoods[יד לבנים].rooms.4",
                         "neighbourhoods[חרוזים].rooms.4"], "UNSOURCED",
            "Nine street averages (192/46/41/38/27/22/21/20/19 deals) from unnamed market pages, no period, no room count, mixed property "
            "types; replaced by official 4-room neighbourhood medians (1-3.2026) for four neighbourhoods the page names.")

# 6. new vs second-hand: renovation cost in the paragraph (tier 2)
old6 = "דירת יד שנייה יכולה להיות זולה יותר במחיר הכולל, אך לדרוש שיפוץ של 150,000-500,000 ש\"ח ולעיתים גם התאמות תשתית."
new6 = ("דירת יד שנייה יכולה להיות זולה יותר במחיר הכולל, אך לדרוש שיפוץ יקר ולעיתים גם התאמות תשתית, ואת עלות השיפוץ כדאי "
        "לתמחר מראש לפי הצעות מחיר.")
e6 = P.edit(old6, new6, ["page"], "UNSOURCED", "Renovation cost 150,000-500,000 with no source or period; rephrased without the number.", tier=2)

# 7-10. new vs second-hand table cells (tier 2)
old7 = "לעיתים נמוך ב-5%-20%"
new7 = "לעיתים נמוך יותר מדירה חדשה דומה"
e7 = P.edit(old7, new7, ["page"], "UNSOURCED", "Second-hand discount 5%-20% with no source or period; rephrased without the percentages.", tier=2)
old8 = "עשוי להיות סביב 30,000-38,000 ש\"ח באזורים רבים"
new8 = "לרוב נמוך יותר מדירה חדשה באותו אזור"
e8 = P.edit(old8, new8, ["page"], "UNSOURCED",
            "Second-hand per-m2 range 30,000-38,000 with no source or period (the dated city figure of 36,000 per m2 stays elsewhere); rephrased.", tier=2)
old9 = "עשוי להגיע ל-40,000-55,000 ש\"ח ומעלה בפרויקטים חזקים"
new9 = "עשוי להיות גבוה בהרבה בפרויקטים חזקים"
e9 = P.edit(old9, new9, ["page"], "UNSOURCED", "New-flat per-m2 range 40,000-55,000 with no source or period; rephrased without the numbers.", tier=2)
old10 = "עלול לדרוש 150,000-500,000 ש\"ח"
new10 = "עלול לדרוש השקעה משמעותית"
e10 = P.edit(old10, new10, ["page"], "UNSOURCED", "Renovation cost 150,000-500,000 (table) with no source; rephrased without the number.", tier=2)

# 11. FAQ 4 rooms: official median first, the 'above 5M' tail tied to the dated deal
old11 = "בדיקת עבודה לדירות 4 חדרים מצביעה על טווח רחב של כ-2,560,000 עד 4,100,000 ש\"ח, ובמקרים יקרים יותר גם מעל 5,000,000 ש\"ח."
new11 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים ברמת גן ברבעון הראשון של 2026 היה 3,330,400 ש\"ח, ובדיקת עבודה "
         "מצביעה על טווח רחב של כ-2,560,000 עד 4,100,000 ש\"ח. בדירות יקרות במיוחד המחיר עובר לעיתים גם את 5,000,000 ש\"ח, כמו "
         "בעסקה ברחוב סמדר 3 במרץ 2026.")
e11 = P.edit(old11, new11, ["rooms.4.latest", "page"], "UNSOURCED",
             "FAQ 4 rooms: the working range is consistent with the official median 3,330,400 (1-3.2026), which now leads the answer; the "
             "undated 'above 5,000,000 in expensive cases' is tied to the one dated deal that supports it (Smadar 3, 8.3.2026, 5,306,190).")

# 12. FAQ asking vs closing gap 3%-8% (tier 2)
old12 = "לעיתים פער של 3%-8% בין מחיר מבוקש למחיר סביר יכול להיות תוצאה של משא ומתן, ולעיתים הפער גדול יותר."
new12 = "לעיתים פער של כמה אחוזים בין מחיר מבוקש למחיר סביר הוא תוצאה של משא ומתן, ולעיתים הפער גדול יותר."
e12 = P.edit(old12, new12, ["page"], "UNSOURCED", "Asking-to-closing gap 3%-8% with no source or period; rephrased without the percentages.", tier=2)

# ---------------- claims inventory ----------------
C = P.claim
ALL = "all rooms 3,122,300 (1-3.2026), +2.5%"
C("p@4318", "בדיקת נתוני שוק גלויים מ-5 ביוני 2026: ממוצע סביב 3,200,000 ש\"ח", "sale_avg", "CONSISTENT", "keep (consistent, dated 5.6.2026)", official=ALL)
C("p@4318", "מחיר ממוצע סביב 36,000 ש\"ח למ\"ר", "per_m2", "UNSOURCED", "keep (public market data, dated 5.6.2026 in the sentence)")
C("p@41493", "שכירות חציונית 6,000, ממוצעת 6,411; 2 חדרים 4,896, 3 חדרים 6,486, 4 חדרים 7,736", "rent", "UNSOURCED",
  "keep (listing data, June 2026, 520 listings, p@52482)", figures=5)
C("p@42110", "ממוצע כללי סביב 3,200,000 ש\"ח (5.6.2026)", "sale_avg", "CONSISTENT", "keep (consistent, dated)", official=ALL)
C("p@42110", "מחיר ממוצע סביב 36,000 ש\"ח למ\"ר (5.6.2026)", "per_m2", "UNSOURCED", "keep (public market data, dated 5.6.2026)")
C("p@42110", "שכירות סביב 6,000-6,500 ש\"ח בחציון או בממוצע", "rent", "UNSOURCED", "keep (listing data, June 2026)")
C("p@43101", "3,787 דירות ובתים למכירה; 2,418 עסקאות בדף עסקאות", "count", "UNSOURCED", "keep (counts, not prices; market pages, page checked 6.6.2026)", figures=2)
C("tr@43937", "מחיר ממוצע כללי | כ-3,200,000 ש\"ח", "sale_avg", "CONSISTENT", "keep (consistent)", official=ALL)
C("tr@44102", "מחיר ממוצע למ\"ר | כ-36,000 ש\"ח", "per_m2", "UNSOURCED", "keep (public market data, 5.6.2026)")
C("tr@44266..44427", "שכירות חציונית כ-6,000; שכירות ממוצעת כ-6,411", "rent", "UNSOURCED", "keep (listing data, June 2026)", figures=2)
C("tr@44584..44909", "520 מודעות שכירות; 3,787 נכסים למכירה; 2,418 עסקאות", "count", "UNSOURCED", "keep (counts, not prices; page checked 6.6.2026)", figures=3)
C("tr@45077", "חלק מחוז תל אביב במלאי הדירות בישראל | 19.5%", "other", "UNSOURCED", f"edit {e1}", note="no named source; tier 2")
C("tr@46130", "1 חדר | כ-1,300,000 עד 2,000,000 ש\"ח", "sale", "UNSOURCED", f"edit {e2}", rooms=1, note="no official 1-room series")
C("tr@46380", "2 חדרים | כ-1,790,000 עד 2,500,000 ש\"ח", "sale", "UNSOURCED", f"edit {e3}", rooms=2, note="no official 2-room series")
C("tr@46628", "3 חדרים | כ-2,300,000 עד 3,200,000 ש\"ח", "sale", "CONSISTENT", "keep (consistent)", rooms=3, official="2,701,700 (1-3.2026)")
C("tr@46870", "4 חדרים | כ-2,560,000 עד 4,100,000 ש\"ח", "sale", "CONSISTENT", "keep (consistent)", rooms=4, official="3,330,400 (1-3.2026)")
C("tr@47128", "5 חדרים | כ-3,900,000 עד 6,000,000 ש\"ח ומעלה", "sale", "CONSISTENT", "keep (consistent)", rooms=5, official="4,636,200 (1-3.2026)")
C("tr@47381", "6 חדרים ומעלה | כ-5,500,000 ש\"ח ומעלה", "sale", "UNSOURCED", f"edit {e4}", rooms=6, note="no official 6+-room series")
C("tr@46130..47381", "עמודת שכירות שוק: 3,368 / 4,896 / 6,486 / 7,736 / 10,209 / 12,279", "rent", "UNSOURCED", "keep (listing data, June 2026)", figures=6)
C("p@47648", "עסקאות: המעגל 37 1,790,000 (19.3.2026), גרשום 7 2,580,000 (15.3.2026), שד' ירושלים 97 2,900,000 (8.3.2026), סמדר 3 5,306,190",
  "deal", "UNSOURCED", "keep (individual dated deals, March 2026)", figures=4, note="Smadar 3 is dated 8.3.2026 in the deals table")
C("tr@49125..51674", "טבלת שכירות לפי אזור (13 שורות)", "rent", "UNSOURCED", "keep (observed listings, page checked 6.6.2026)", figures=13)
C("p@51897", "ממוצעי רחוב: רפאל איתן 3,741,942 ... תל חי 3,374,473 (9 רחובות)", "sale_street", "UNSOURCED", f"edit {e5}", figures=9,
  note="unnamed market pages, no period, no room count")
C("p@52482", "שכירות מיוני 2026: חציון 6,000, ממוצע 6,411, 520 מודעות; ארצי 4,400", "rent", "UNSOURCED", "keep (listing data, dated June 2026)", figures=4)
C("tr@53111..53967", "טבלת שכירות לפי חדרים (6 שורות)", "rent", "UNSOURCED", "keep (listing data, June 2026)", figures=6)
C("tr@55192..57322", "טבלת עסקאות (10 עסקאות, 1.3-19.3.2026)", "deal", "UNSOURCED", "keep (individual dated deals, March 2026)", figures=10)
C("p@58225", "שיפוץ של 150,000-500,000 ש\"ח", "other", "UNSOURCED", f"edit {e6}", note="tier 2")
C("tr@58867", "מחיר כולל יד שנייה | לעיתים נמוך ב-5%-20%", "sale_new_used", "UNSOURCED", f"edit {e7}", note="tier 2")
C("tr@59084", "מחיר למ\"ר | יד שנייה 30,000-38,000 | חדשה 40,000-55,000 ומעלה", "per_m2", "UNSOURCED", f"edit {e8}", figures=2, note=f"also edit {e9}; tier 2")
C("tr@59353", "שיפוץ | עלול לדרוש 150,000-500,000 ש\"ח", "other", "UNSOURCED", f"edit {e10}", note="tier 2")
C("p@65692", "FAQ ממוצע: סביב 3,200,000 ש\"ח (5.6.2026)", "sale_avg", "CONSISTENT", "keep (consistent, dated)", official=ALL)
C("p@65992", "FAQ: מחיר ממוצע סביב 36,000 ש\"ח למ\"ר", "per_m2", "UNSOURCED", "keep (public market data, dated 5.6.2026 in the body)")
C("p@66281", "FAQ 3 חדרים: כ-2,300,000 עד 3,200,000 ש\"ח", "sale", "CONSISTENT", "keep (consistent)", rooms=3, official="2,701,700 (1-3.2026)")
C("p@66281", "FAQ 3 חדרים: עסקאות 2,580,000 (75 מ\"ר) ו-3,018,000 (92 מ\"ר)", "deal", "UNSOURCED", "keep (individual deals dated in the deals table, March 2026)", rooms=3, figures=2)
C("p@66542", "FAQ 4 חדרים: כ-2,560,000 עד 4,100,000 ש\"ח", "sale", "CONSISTENT", f"edit {e11}", rooms=4, official="3,330,400 (1-3.2026)", note="range kept inside the rewrite")
C("p@66542", "FAQ 4 חדרים: במקרים יקרים גם מעל 5,000,000 ש\"ח", "sale", "UNSOURCED", f"edit {e11}", rooms=4, official="3,330,400 (1-3.2026)",
  note="a tail statement, now tied to the dated Smadar 3 deal")
C("p@66542", "FAQ 4 חדרים: עסקאות 2,560,000 / 2,900,000 / 3,150,000 / 5,306,190", "deal", "UNSOURCED", "keep (individual deals dated in the deals table)", rooms=4, figures=4)
C("p@66849", "FAQ 5 חדרים: סביב 3,900,000-6,000,000 ש\"ח ומעלה", "sale", "CONSISTENT", "keep (consistent)", rooms=5, official="4,636,200 (1-3.2026)")
C("p@67140", "FAQ שכירות: 9,090 ברמת חן, 10,775 ברמת אפעל, 11,890 בקריניצי", "rent", "UNSOURCED", "keep (observed listings, page checked 6.6.2026)", figures=3)
C("p@67431", "FAQ שכירות באזור הבורסה סביב 6,793", "rent", "UNSOURCED", "keep (observed listings, page checked 6.6.2026)")
C("p@67733", "FAQ: פער של 3%-8% בין מחיר מבוקש למחיר סביר", "other", "UNSOURCED", f"edit {e12}", note="tier 2")
C("p@68429", "FAQ: שכירות בעיר סביב 6,000-6,411", "rent", "UNSOURCED", "keep (listing data, June 2026)")

P.write(notes=(
    "Not audited as claims (illustrations or structure): the 3,450,000 / 2,900,000 illustration (p@43467), m2 definitions (p@42678, p@45343), "
    "the if-example 2,850,000-3,050,000 vs 3,250,000 (p@65332), step counts (6-12 deals, 10-20 listings), 90 days, 12-48 months. "
    "The city 'average about 3,200,000' (dated market data, 5.6.2026) is within 2.5% of the official all-rooms median 3,122,300 and is kept; "
    "the 3/4/5-room working ranges contain the official medians and are kept; only the 1-room, 2-room and 6+-room cells lose their numbers, "
    "the rows stay. Rent figures are kept (listing data, June 2026, 520 listings). Tier 2 = seven edits of 'other' figures with no named source "
    "(19.5% district share, renovation 150,000-500,000 twice, second-hand discount 5%-20%, per-m2 30,000-38,000 / 40,000-55,000, 3%-8% "
    "negotiation gap). The 9 remaining SUSPECT lines after the edits are all individual deals dated March 2026 in the deals table: Smadar 3 "
    "5,306,190 (8.3.2026; in p@47648 and its table row), Masada 27 4,150,000, Moshe Dayan 26 2,560,000, Uziel 93 2,950,000, Gershom 11 "
    "3,150,000, Sderot Yerushalayim 97 2,900,000, Tarpab 14 3,018,000 (table row and FAQ p@66281). "
    "Name mapping: page 'נחלת גנים', 'חרוזים', 'יד לבנים', 'מתחם נגבה' = official names exactly; the page's 'מרכז העיר' was NOT mapped to "
    "the official 'מרכז העיר א' (a sub-area), so it is not quoted."))
