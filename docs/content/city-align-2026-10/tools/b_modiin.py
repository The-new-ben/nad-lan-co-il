# -*- coding: utf-8 -*-
"""Modiin (page 4555): body alignment with the official price list (3 rooms 10-12.2025, 4/5 rooms 1-3.2026).
The list itself is not on the page yet (it will be added). Data only, nothing applied."""
from mk import Page

P = Page("modiin-apartment-prices")
R3 = "2,039,500 שקל לדירת 3 חדרים ברבעון הרביעי של 2025 (הנתון האחרון שפורסם לדירות 3 חדרים)"

# ---------------- edits ----------------
# 1. the lead paragraph
old1 = P.find("מחירי דירות במודיעין מכבים רעות נעים כיום,", "וסביב כ-4.1 עד 5.3 מיליון שקל בדירות גדולות של 6 חדרים ומעלה.")
new1 = ("מחירי דירות במודיעין מכבים רעות, לפי נתוני רשות המסים: חציון מחיר העסקה היה 2,559,800 שקל לדירת 4 חדרים ו-3,648,800 שקל "
        "לדירת 5 חדרים ברבעון הראשון של 2026, ו-" + R3 + ". בדירות גדולות של 6 חדרים ומעלה הציגו מקורות שוק שנבדקו ביום 5.6.2026 "
        "מחירים סביב כ-4.1 עד 5.3 מיליון שקל.")
e1 = P.edit(old1, new1, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
            "Lead: 3 rooms 2.4-2.7M and 4 rooms 2.8-3.2M (market sources read 5.6.2026) exclude the official medians 2,039,500 (10-12.2025) "
            "and 2,559,800 (1-3.2026); 5 rooms 3.6-4.1M was consistent and is restated as the median 3,648,800. The 6+ room range keeps its "
            "dated source; the rent sentence after it is untouched.")

# 2. quick-metrics table: the two city averages become one official row
old2 = P.table_html('<th dir="rtl">מקור ותאריך</th>')
a = old2.find('<tr dir="rtl">\n<td dir="rtl">מחיר קנייה ממוצע</td>')
b = old2.find('<tr dir="rtl">\n<td dir="rtl">מחיר למ"ר</td>')
assert 0 < a < b
new_row = """<tr dir="rtl">
<td dir="rtl">חציון מחיר העסקה, כל הדירות</td>
<td dir="rtl">2,512,500 שקל</td>
<td dir="rtl">רשות המסים, ינואר-מרץ 2026</td>
<td dir="rtl">חציון עירוני, לא מחיר לשכונה או לדירה מסוימת</td>
</tr>
"""
new2 = old2[:a] + new_row + old2[b:]
e2 = P.table('<th dir="rtl">מקור ותאריך</th>', new2, ["rooms.all.latest"], "CONFLICT",
             "Quick-metrics table: the city averages 2,701,971 (data site, 5.6.2026) and 3,350,000 (portal, 5.6.2026) vs the official all-rooms "
             "median 2,512,500 (1-3.2026), 7.5% and 33% apart. Both rows become one official row; the other six rows (per m2, rent, yield, "
             "listing counts) are kept word for word.")

# 3. rooms paragraph (asking prices by rooms from a portal)
old3 = P.find("לפי מדדירות, שנקרא ביום 5.6.2026, מחירי הביקוש בעיר הוצגו כך:", "ו-29,661 שקל למ\"ר בדירות 6 חדרים ומעלה.")
new3 = ("לפי נתוני רשות המסים, חציון מחיר העסקה היה 2,559,800 שקל לדירת 4 חדרים ו-3,648,800 שקל לדירת 5 חדרים ברבעון הראשון של 2026, "
        "ו-" + R3 + ". המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים ודירות 6 חדרים ומעלה כדאי לבדוק מול עסקאות "
        "דומות ברחוב ובשכונה. לפי מדדירות, שנקרא ביום 5.6.2026, מחירי הביקוש במודעות היו סביב 2,700,000 שקל לדירות 2 חדרים וסביב "
        "5,250,000 שקל לדירות 6 חדרים ומעלה, ובאותו מקור הופיע מחיר מבוקש למ\"ר לפי חדרים: 38,571 שקל למ\"ר בדירות 2 חדרים, 31,176 שקל "
        "למ\"ר בדירות 3 חדרים, 28,482 שקל למ\"ר בדירות 4 חדרים, 29,286 שקל למ\"ר בדירות 5 חדרים ו-29,661 שקל למ\"ר בדירות 6 חדרים ומעלה.")
e3 = P.edit(old3, new3, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
            "Portal asking prices read 5.6.2026: 3 rooms 2,650,000, 4 rooms 3,190,000, 5 rooms 4,100,000 vs the official medians 2,039,500 "
            "(10-12.2025), 2,559,800 and 3,648,800 (1-3.2026). Replaced by the medians; the 2-room and 6+ asking prices and the asking per-m2 "
            "figures keep their named, dated source and are labelled as asking.")

# 4. new / second-hand split by rooms from a data site
old4 = P.find("אתר נתוני נדל\"ן, שנקרא ביום 5.6.2026, הציג הפרדה בין דירות חדשות לדירות יד שנייה בחלק מקטגוריות החדרים:",
              "לעומת דירת 6 חדרים יד שנייה סביב 4.16 מיליון שקל.")
new4 = ("אתר נתוני נדל\"ן, שנקרא ביום 5.6.2026, הציג שכר דירה לפי חדרים: סביב 6,200 שקל לדירת 3 חדרים, 6,950 שקל לדירת 4 חדרים ו-8,500 "
        "שקל לדירת 5 חדרים, ובדירות 6 חדרים מחיר של כ-4.65 מיליון שקל לדירה חדשה לעומת כ-4.16 מיליון שקל ליד שנייה. הטבלה הבאה מציגה את "
        "חציון מחיר העסקה לפי מספר חדרים, לפי נתוני רשות המסים, לצד החציון באותו רבעון שנה קודם לכן.")
e4 = P.edit(old4, new4, ["rooms.3.year_ago", "page"], "CONFLICT",
            "New / second-hand split read 5.6.2026: 3 rooms second-hand 2.43M, 4 rooms new 2.15M and second-hand 2.98M are outside tolerance "
            "of the official medians 2,039,500 and 2,559,800 (3 rooms new 2.0M, 5 rooms 3.59M / 3.62M were consistent). The 3/4/5 split is "
            "dropped here (the new-vs-second-hand section explains it, edit 11); rents and the 6-room split keep their dated source.")

# 5. rooms table
new5 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">מספר חדרים</th>
<th dir="rtl">חציון מחיר העסקה, ינואר-מרץ 2026</th>
<th dir="rtl">ינואר-מרץ 2025</th>
<th dir="rtl">שינוי בשנה</th>
<th dir="rtl">פירוש מעשי</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">3 חדרים</td>
<td dir="rtl">2,039,500 שקל (אוקטובר-דצמבר 2025)</td>
<td dir="rtl">2,414,500 שקל (אוקטובר-דצמבר 2024)</td>
<td dir="rtl">ירידה של 15.5%</td>
<td dir="rtl">מתאים לזוגות, משפרי דיור ראשונים וחלק מהמשקיעים</td>
</tr>
<tr dir="rtl">
<td dir="rtl">4 חדרים</td>
<td dir="rtl">2,559,800 שקל</td>
<td dir="rtl">3,044,600 שקל</td>
<td dir="rtl">ירידה של 15.9%</td>
<td dir="rtl">קטגוריית משפחות מרכזית בעיר, רגישה מאוד לשכונה ולמצב הבניין</td>
</tr>
<tr dir="rtl">
<td dir="rtl">5 חדרים</td>
<td dir="rtl">3,648,800 שקל</td>
<td dir="rtl">3,833,400 שקל</td>
<td dir="rtl">ירידה של 4.8%</td>
<td dir="rtl">שוק משפחתי חזק, עם פערים בין דירות רגילות לדירות מיוחדות</td>
</tr>
</tbody>
</table>"""
e5 = P.table('<th dir="rtl">מחיר מבוקש לפי מדדירות</th>', new5,
             ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct",
              "rooms.5.latest", "rooms.5.year_ago", "rooms.5.change_pct"], "CONFLICT",
             "Rooms table: asking 2,650,000 / 3,190,000 / 4,100,000 and the 3-4 room new / second-hand cells contradict the official medians. "
             "Replaced by the official medians with the same quarter a year earlier (3 rooms: 10-12.2025 vs 10-12.2024, written in the cells); "
             "the 'practical reading' notes of rows 3-5 are kept word for word. The 2-room and 6+ rows leave the table (named in edit 3); the "
             "asking per-m2 figures stay in the paragraph of edit 3 and the rents in edit 4 and the rent section.")

# 6. neighbourhood paragraph: 2023 deal averages
old6 = P.find("לפי מדדירות, שנקרא ביום 5.6.2026, טבלת עסקאות רשות המסים לשנת 2023 הראתה למשל", "באבני חן במחיר ממוצע של 2,950,000 שקל.")
new6 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 4 חדרים היה 2,403,500 שקל בכרמים, 2,717,500 שקל בשכונת "
        "המגינים, 2,794,500 שקל בשכונת הנביאים, 2,940,600 שקל באבני חן ו-2,944,000 שקל בשכונת הנחלים. בהפרחים פורסם חציון לדירות 3 חדרים "
        "בלבד: 2,188,900 שקל.")
e6 = P.edit(old6, new6, ["neighbourhoods[הכרמים].rooms.4", "neighbourhoods[המגינים].rooms.4", "neighbourhoods[הנביאים].rooms.4",
                         "neighbourhoods[אבני חן].rooms.4", "neighbourhoods[הנחלים].rooms.4", "neighbourhoods[הפרחים].rooms.3"], "STALE",
            "2023 all-rooms neighbourhood deal averages (Karmim 2,677,500, Nechalim 2,625,000, Haprachim 2,850,000, Avnei Chen 2,950,000) "
            "presented as the current comparison; replaced by the official 1-3.2026 neighbourhood medians.")

# 7. neighbourhood table
new7 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">שכונה או אזור</th>
<th dir="rtl">חציון מחיר העסקה לפי חדרים, ינואר-מרץ 2026</th>
<th dir="rtl">ממוצע לפי שנתון עירוני יוני 2026</th>
<th dir="rtl">מה לבדוק לפני הסתמכות</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">כרמים</td>
<td dir="rtl">3 חדרים: 1,578,700 שקל; 4 חדרים: 2,403,500 שקל; 5 חדרים: 3,332,700 שקל</td>
<td dir="rtl">2,455,296 שקל</td>
<td dir="rtl">רחוב, גיל בניין, גודל דירות ותמהיל משפחות</td>
</tr>
<tr dir="rtl">
<td dir="rtl">הנחלים</td>
<td dir="rtl">3 חדרים: 2,339,400 שקל; 4 חדרים: 2,944,000 שקל; 5 חדרים: 3,373,400 שקל</td>
<td dir="rtl">2,797,582 שקל באזור טכנולוגי, מרכז עינב והנחלים לפי הסיכום</td>
<td dir="rtl">קרבה לצירי תנועה, שטח הדירה, חניה ומעלית</td>
</tr>
<tr dir="rtl">
<td dir="rtl">הפרחים</td>
<td dir="rtl">3 חדרים: 2,188,900 שקל; 4 ו-5 חדרים: לא פורסם</td>
<td dir="rtl">3,507,639 שקל</td>
<td dir="rtl">פער בין תקופות ומדגמים מחייב בדיקת עסקאות רחוב</td>
</tr>
<tr dir="rtl">
<td dir="rtl">אבני חן</td>
<td dir="rtl">4 חדרים: 2,940,600 שקל; 3 ו-5 חדרים: לא פורסם</td>
<td dir="rtl">3,119,657 שקל</td>
<td dir="rtl">נדרש סינון לפי סוג דירה</td>
</tr>
<tr dir="rtl">
<td dir="rtl">נופים</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">4,048,211 שקל</td>
<td dir="rtl">שכונה חדשה יותר, לבדוק מסירה, פיתוח סביבתי והיצע עתידי</td>
</tr>
<tr dir="rtl">
<td dir="rtl">מורשת</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">3,202,845 שקל</td>
<td dir="rtl">לבדוק פרויקטים חדשים, זמני אכלוס, פיתוח והנחות ביחס לדירות מוכנות</td>
</tr>
<tr dir="rtl">
<td dir="rtl">מוריה ובוכמן דרום</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">מוריה 4,120,139 שקל</td>
<td dir="rtl">אזור יקר יחסית, נדרש להשוות רק לנכסים דומים</td>
</tr>
<tr dir="rtl">
<td dir="rtl">הציפורים</td>
<td dir="rtl">לא פורסם</td>
<td dir="rtl">3,321,363 שקל</td>
<td dir="rtl">לבדוק בנייה חדשה, שטח, מרפסת, חניה ומלאי דירות</td>
</tr>
<tr dir="rtl">
<td dir="rtl">הנביאים</td>
<td dir="rtl">3 חדרים: 2,471,700 שקל; 4 חדרים: 2,794,500 שקל; 5 חדרים: 3,448,200 שקל</td>
<td dir="rtl">2,728,012 שקל</td>
<td dir="rtl">גיל בניין, קומה, חניה, מעלית וקרבה לצירי תנועה</td>
</tr>
<tr dir="rtl">
<td dir="rtl">המגינים</td>
<td dir="rtl">3 חדרים: 2,542,200 שקל; 4 חדרים: 2,717,500 שקל; 5 חדרים: לא פורסם</td>
<td dir="rtl">3,007,645 שקל</td>
<td dir="rtl">גיל בניין, קומה, חניה, מעלית וקרבה לצירי תנועה</td>
</tr>
</tbody>
</table>"""
e7 = P.table('<th dir="rtl">נתון עסקאות לפי מדדירות, רשות המסים 2023</th>', new7,
             ["neighbourhoods[הכרמים].rooms.3", "neighbourhoods[הכרמים].rooms.4", "neighbourhoods[הכרמים].rooms.5",
              "neighbourhoods[הנחלים].rooms.3", "neighbourhoods[הנחלים].rooms.4", "neighbourhoods[הנחלים].rooms.5",
              "neighbourhoods[הפרחים].rooms.3", "neighbourhoods[אבני חן].rooms.4",
              "neighbourhoods[הנביאים].rooms.3", "neighbourhoods[הנביאים].rooms.4", "neighbourhoods[הנביאים].rooms.5",
              "neighbourhoods[המגינים].rooms.3", "neighbourhoods[המגינים].rooms.4", "page"], "STALE",
             "Neighbourhood table: the 'portal, Tax Authority 2023' column (deal counts and all-rooms averages) is STALE; replaced by the "
             "official 1-3.2026 medians by rooms ('לא פורסם' where the official file has none). The municipal yearbook column (named, dated "
             "June 2026) and the check notes are kept; rows for הנביאים and המגינים (official medians, yearbook averages already shown in the "
             "paragraph above) are added; the Avnei Chen note drops 'relatively many deals', which referred to the removed 2023 count.",
             kept=["2,728,012", "3,007,645"])

# 8. 'a city average of 2.7 or 3.35M is not enough'
old8 = "ממוצע עירוני של 2.7 או 3.35 מיליון שקל אינו מספיק כאשר דירה אחת נמצאת בכרמים ודירה אחרת בנופים, במוריה או במורשת."
new8 = ("חציון עירוני של 2,512,500 שקל, לפי נתוני רשות המסים לרבעון הראשון של 2026, אינו מספיק כאשר דירה אחת נמצאת בכרמים ודירה אחרת "
        "בנופים, במוריה או במורשת.")
e8 = P.edit(old8, new8, ["rooms.all.latest"], "CONFLICT", "City averages 2.7M / 3.35M vs the official all-rooms median 2,512,500 (1-3.2026).")

# 9. purchase / rent table: purchase prices conflict, the yield column is derived from them
new9 = """<table dir="rtl">
<thead dir="rtl">
<tr dir="rtl">
<th dir="rtl">סוג דירה</th>
<th dir="rtl">חציון מחיר העסקה</th>
<th dir="rtl">שכר דירה חודשי לפי אתר נתוני נדל"ן</th>
<th dir="rtl">שכר דירה שנתי</th>
</tr>
</thead>
<tbody dir="rtl">
<tr dir="rtl">
<td dir="rtl">3 חדרים</td>
<td dir="rtl">2,039,500 שקל (אוקטובר-דצמבר 2025)</td>
<td dir="rtl">6,200 שקל</td>
<td dir="rtl">74,400 שקל</td>
</tr>
<tr dir="rtl">
<td dir="rtl">4 חדרים</td>
<td dir="rtl">2,559,800 שקל (ינואר-מרץ 2026)</td>
<td dir="rtl">6,950 שקל</td>
<td dir="rtl">83,400 שקל</td>
</tr>
<tr dir="rtl">
<td dir="rtl">5 חדרים</td>
<td dir="rtl">3,648,800 שקל (ינואר-מרץ 2026)</td>
<td dir="rtl">8,500 שקל</td>
<td dir="rtl">102,000 שקל</td>
</tr>
<tr dir="rtl">
<td dir="rtl">ממוצע עירוני לפי מדדירות</td>
<td dir="rtl">לא מוצג כמחיר יחיד בטבלה זו</td>
<td dir="rtl">7,200 שקל מבוקש</td>
<td dir="rtl">86,400 שקל</td>
</tr>
</tbody>
</table>"""
e9 = P.table('<th dir="rtl">תשואה גולמית מקורבת</th>', new9,
             ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
             "Purchase/rent table: the example purchase prices are the data site's second-hand figures, 2,430,000 for 3 rooms and 2,980,000 "
             "for 4 rooms, against the official 2,039,500 and 2,559,800 (5 rooms 3,620,000 was consistent). Purchase cells replaced by the "
             "official medians with their quarter; the gross-yield column (computed from the old prices) is removed, no new yield computed; "
             "dated rents and annual rents kept. The source's own 2.9% city yield stays in the rent paragraph and the quick-metrics table.")

# 10. portal deal count + average
old10 = "דירובוט, שנקרא ביום 5.6.2026, הציג 1,135 עסקאות, מחיר ממוצע של 3,350,000 שקל ומחיר של 27,000 שקל למ\"ר, וכן דוגמאות עסקאות מחודש מרץ 2026."
new10 = ("דירובוט, שנקרא ביום 5.6.2026, הציג 1,135 עסקאות ומחיר של 27,000 שקל למ\"ר, וכן דוגמאות עסקאות מחודש מרץ 2026. לפי נתוני "
         "רשות המסים, חציון מחיר העסקה בכל העסקאות בעיר ברבעון הראשון של 2026 היה 2,512,500 שקל.")
e10 = P.edit(old10, new10, ["rooms.all.latest", "page"], "CONFLICT",
             "Portal average 3,350,000 (read 5.6.2026) vs the official all-rooms median 2,512,500; the deal count and the per-m2 figure keep their dated source.")

# 11. new vs second-hand section
old11 = P.find("הנתונים שנקראו ביום 5.6.2026 באתר נתוני נדל\"ן מדגימים את המורכבות:", "מדגם ודרך הצגת הנתון.")
new11 = ("הנתונים שנקראו ביום 5.6.2026 באתר נתוני נדל\"ן מדגימים את המורכבות. חציון מחיר העסקה של רשות המסים מחושב מכלל העסקאות שדווחו "
         "בכל מספר חדרים, בלי הפרדה בין דירה חדשה לדירת יד שנייה. האתר הציג הפרדה כזו, אך בדירות 3 ו-4 חדרים המספרים שלו רחוקים מחציון "
         "העסקאות הרשמי, ולכן כדאי לבדוק אותם מול עסקאות דומות. בדירות 5 חדרים הפער כמעט נסגר, 3.59 מיליון שקל חדש מול 3.62 מיליון שקל "
         "יד שנייה, קרוב לחציון הרשמי של 3,648,800 שקל; ובדירות 6 חדרים הופיע 4.65 מיליון שקל חדש מול 4.16 מיליון שקל יד שנייה. פער כזה "
         "יכול לנבוע ממיקום, שלב פרויקט, שטח, סוג נכס, מדגם ודרך הצגת הנתון.")
e11 = P.edit(old11, new11, ["rooms.5.latest", "page"], "CONFLICT",
             "Same new / second-hand split as edit 4: 3 rooms second-hand 2.43M, 4 rooms 2.15M / 2.98M conflict with the official medians; "
             "the consistent 5-room pair and the 6-room pair keep their dated source; the median is said to cover all deals.")

# 12-15. FAQ answers
old12 = P.find("לפי מקורות שנקראו ביום 5.6.2026, דירות 3 חדרים מוצגות סביב 2.4 עד 2.7 מיליון שקל,", "אלה טווחים כלליים בלבד,")
new12 = ("לפי נתוני רשות המסים, חציון מחיר העסקה במודיעין היה 2,559,800 שקל לדירת 4 חדרים ו-3,648,800 שקל לדירת 5 חדרים ברבעון "
         "הראשון של 2026, ו-" + R3 + ". בדירות 6 חדרים ומעלה הציגו מקורות שנקראו ביום 5.6.2026 מחירים סביב 4.1 עד 5.3 מיליון שקל. "
         "אלה נקודות ייחוס כלליות בלבד,")
e12 = P.edit(old12, new12, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
             "FAQ 'how much does a flat cost': same ranges as the lead (3 rooms 2.4-2.7M, 4 rooms 2.8-3.2M in conflict); rewritten from the same facts as edit 1.")
old13 = P.find("מדדירות הציג ביום 5.6.2026 מחיר מבוקש של 3,190,000 שקל לדירת 4 חדרים", "ולא לפי כותרת חדרים בלבד.")
new13 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים במודיעין ברבעון הראשון של 2026 היה 2,559,800 שקל, לעומת 3,044,600 שקל "
         "שנה קודם לכן. מדדירות הציג ביום 5.6.2026 מחיר מבוקש של 28,482 שקל למ\"ר לדירת 4 חדרים, ואתר נתוני נדל\"ן אחר הציג באותו מועד "
         "שכר דירה סביב 6,950 שקל. כדאי לבדוק לפי נכס דומה ולא לפי כותרת חדרים בלבד.")
e13 = P.edit(old13, new13, ["rooms.4.latest", "rooms.4.year_ago", "page"], "CONFLICT",
             "FAQ 4 rooms: asking 3,190,000, new 2.15M and second-hand 2.98M vs the official 2,559,800 (1-3.2026); per-m2 and rent keep their dated sources.")
old14 = "לפי מדדירות, מוריה ובוכמן דרום הופיעו עם 25 עסקאות וממוצע של 4,300,000 שקל בשנת 2023."
new14 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 4 חדרים היה 2,944,000 שקל בשכונת הנחלים ו-2,940,600 שקל "
         "באבני חן, לעומת 2,403,500 שקל בכרמים.")
e14 = P.edit(old14, new14, ["neighbourhoods[הנחלים].rooms.4", "neighbourhoods[אבני חן].rooms.4", "neighbourhoods[הכרמים].rooms.4"], "STALE",
             "FAQ: Moria and Buchman South 2023 average (25 deals, 4,300,000); replaced by official 1-3.2026 neighbourhood medians (no official "
             "median for Moria). The municipal yearbook averages in the same answer are kept (named, June 2026).")
old15 = "אתר אחד הציג ביום 5.6.2026 מחיר קנייה ממוצע של 2,701,971 שקל, מדדירות הציג טבלאות ביקוש לפי חדרים ושכונות, ודירובוט הציג מחיר ממוצע של 3,350,000 שקל ומחיר של 27,000 שקל למ\"ר."
new15 = ("אתר אחד הציג ביום 5.6.2026 מחיר קנייה ממוצע, מדדירות הציג טבלאות ביקוש לפי חדרים ושכונות, ודירובוט הציג מחיר ממוצע אחר ומחיר "
         "של 27,000 שקל למ\"ר. נתוני רשות המסים מבוססים על עסקאות שדווחו בפועל: חציון מחיר העסקה בכל העסקאות בעיר ברבעון הראשון של 2026 "
         "היה 2,512,500 שקל.")
e15 = P.edit(old15, new15, ["rooms.all.latest", "page"], "CONFLICT",
             "FAQ on source gaps: city averages 2,701,971 and 3,350,000 vs the official all-rooms median 2,512,500; the per-m2 figure keeps its dated source.")

# ---------------- claims inventory ----------------
C = P.claim
C("p@4480", "דירות 3 חדרים סביב כ-2.4 עד 2.7 מיליון שקל (5.6.2026)", "sale", "CONFLICT", f"edit {e1}", rooms=3, official="2,039,500 (10-12.2025)")
C("p@4480", "דירות 4 חדרים סביב כ-2.8 עד 3.2 מיליון שקל", "sale", "CONFLICT", f"edit {e1}", rooms=4, official="2,559,800 (1-3.2026)")
C("p@4480", "דירות 5 חדרים סביב כ-3.6 עד 4.1 מיליון שקל", "sale", "CONSISTENT", f"edit {e1}", rooms=5, official="3,648,800 (1-3.2026)",
  note="restated as the median inside the same rewrite")
C("p@4480", "6 חדרים ומעלה סביב כ-4.1 עד 5.3 מיליון שקל", "sale", "UNSOURCED", f"edit {e1}", rooms=6,
  note="kept inside the rewrite: market sources named on the page, read 5.6.2026")
C("p@4480", "שכר הדירה הממוצע ... סביב 7,200 עד 7,600 שקל לחודש", "rent", "UNSOURCED", "keep (sources named in p@4990, read 5.6.2026)")
C("tr@6012", "מחיר קנייה ממוצע | 2,701,971 שקל | אתר נתוני נדל\"ן, 5.6.2026", "sale_avg", "CONFLICT", f"edit {e2}", rooms="all",
  official="2,512,500 (1-3.2026)")
C("tr@6216", "מחיר ממוצע נוסף | 3,350,000 שקל | דירובוט, 5.6.2026", "sale_avg", "CONFLICT", f"edit {e2}", rooms="all", official="2,512,500 (1-3.2026)")
C("tr@6399", "מחיר למ\"ר | 27,000 שקל | דירובוט, 5.6.2026", "per_m2", "UNSOURCED", "keep (named portal, read 5.6.2026)")
C("tr@6577..6758", "שכר דירה ממוצע 7,600 / מבוקש 7,200 (5.6.2026)", "rent", "UNSOURCED", "keep (named sources, read 5.6.2026)", figures=2)
C("tr@6960", "תשואה עירונית ממוצעת | 2.9% | מדדירות, 5.6.2026", "yield", "UNSOURCED", "keep (named portal, read 5.6.2026)")
C("tr@7146..7330", "דירות למכירה 470; בתים ודירות למכירה 1,112", "count", "UNSOURCED", "keep (named sources, read 5.6.2026)", figures=2)
C("p@7952", "מחיר ביקוש 2 חדרים סביב 2,700,000 שקל (מדדירות, 5.6.2026)", "sale", "UNSOURCED", f"edit {e3}", rooms=2,
  note="kept inside the rewrite, labelled as an asking price (named portal, dated)")
C("p@7952", "מחיר ביקוש 3 חדרים סביב 2,650,000 שקל", "sale", "CONFLICT", f"edit {e3}", rooms=3, official="2,039,500 (10-12.2025)")
C("p@7952", "מחיר ביקוש 4 חדרים סביב 3,190,000 שקל", "sale", "CONFLICT", f"edit {e3}", rooms=4, official="2,559,800 (1-3.2026)")
C("p@7952", "מחיר ביקוש 5 חדרים סביב 4,100,000 שקל", "sale", "CONFLICT", f"edit {e3}", rooms=5, official="3,648,800 (1-3.2026)")
C("p@7952", "מחיר ביקוש 6 חדרים ומעלה סביב 5,250,000 שקל", "sale", "UNSOURCED", f"edit {e3}", rooms=6, note="kept inside the rewrite (named portal, dated)")
C("p@7952", "מחיר למ\"ר לפי חדרים: 38,571 / 31,176 / 28,482 / 29,286 / 29,661", "per_m2", "UNSOURCED", f"edit {e3}", figures=5,
  note="kept inside the rewrite, labelled as asking per m2 (named portal, dated)")
C("p@8530", "3 חדרים: חדשה סביב 2.0 מיליון", "sale_new_used", "CONSISTENT", f"edit {e4}", rooms=3, official="2,039,500 (10-12.2025)",
  note="dropped with the conflicting cells of the same split")
C("p@8530", "3 חדרים: יד שנייה סביב 2.43 מיליון", "sale_new_used", "CONFLICT", f"edit {e4}", rooms=3, official="2,039,500 (10-12.2025)")
C("p@8530", "4 חדרים: חדשה סביב 2.15 מיליון, יד שנייה סביב 2.98 מיליון", "sale_new_used", "CONFLICT", f"edit {e4}", rooms=4,
  official="2,559,800 (1-3.2026)", figures=2)
C("p@8530", "5 חדרים: חדשה סביב 3.59 מיליון, יד שנייה סביב 3.62 מיליון", "sale_new_used", "CONSISTENT", f"edit {e4}", rooms=5,
  official="3,648,800 (1-3.2026)", figures=2, note="kept in the new-vs-second-hand section (edit 11)")
C("p@8530", "6 חדרים: חדשה סביב 4.65 מיליון, יד שנייה סביב 4.16 מיליון", "sale_new_used", "UNSOURCED", f"edit {e4}", rooms=6, figures=2,
  note="kept inside the rewrite (named data site, read 5.6.2026)")
C("p@8530", "שכר דירה 6,200 / 6,950 / 8,500 לפי חדרים", "rent", "UNSOURCED", f"edit {e4}", figures=3, note="kept inside the rewrite (dated)")
C("tr@9347", "2 חדרים | 2,700,000 | 38,571 למ\"ר", "sale", "UNSOURCED", f"edit {e5}", rooms=2, figures=2, note="row leaves the table; figures stay in p@7952")
C("tr@9583", "3 חדרים | מבוקש 2,650,000 | יד שנייה 2.43 מיליון", "sale", "CONFLICT", f"edit {e5}", rooms=3, official="2,039,500 (10-12.2025)", figures=2)
C("tr@9583", "3 חדרים | חדשה 2.0 מיליון", "sale_new_used", "CONSISTENT", f"edit {e5}", rooms=3, official="2,039,500 (10-12.2025)")
C("tr@9840", "4 חדרים | מבוקש 3,190,000 | חדשה 2.15 מיליון | יד שנייה 2.98 מיליון", "sale", "CONFLICT", f"edit {e5}", rooms=4,
  official="2,559,800 (1-3.2026)", figures=3)
C("tr@10110", "5 חדרים | מבוקש 4,100,000", "sale", "CONFLICT", f"edit {e5}", rooms=5, official="3,648,800 (1-3.2026)")
C("tr@10110", "5 חדרים | חדשה 3.59 מיליון | יד שנייה 3.62 מיליון", "sale_new_used", "CONSISTENT", f"edit {e5}", rooms=5,
  official="3,648,800 (1-3.2026)", figures=2)
C("tr@10377", "6 חדרים ומעלה | 5,250,000 | 4.65 חדש | 4.16 יד שנייה", "sale", "UNSOURCED", f"edit {e5}", rooms=6, figures=3,
  note="row leaves the table; figures stay in edits 3, 4 and 11")
C("tr@9583..10377", "עמודות מחיר למ\"ר ושכירות בטבלת החדרים", "per_m2", "UNSOURCED", f"edit {e5}", figures=7,
  note="columns leave the table; the same dated figures stay in p@7952 / p@8530 and the rent section")
C("p@11189", "רשות המסים 2023: כרמים 2,677,500, הנחלים 2,625,000, הפרחים 2,850,000, אבני חן 2,950,000 (60/45/44/63 עסקאות)", "sale_nb",
  "STALE", f"edit {e6}", rooms="all", figures=8, official="e.g. כרמים 4 rooms 2,403,500, אבני חן 4 rooms 2,940,600 (1-3.2026)")
C("p@11710", "שנתון עירוני יוני 2026: הפרחים 3,507,639 ... מוריה 4,120,139 (10 שכונות)", "sale_nb", "UNSOURCED",
  "keep (municipal yearbook, June 2026)", rooms="all", figures=10)
C("tr@12414..13880", "עמודת 'מדדירות, רשות המסים 2023': עסקאות וממוצעים (6 שכונות + 2 'לא נמסר')", "sale_nb", "STALE", f"edit {e7}",
  rooms="all", figures=12)
C("tr@12414..13880", "עמודת שנתון עירוני יוני 2026 (8 שורות)", "sale_nb", "UNSOURCED", "keep (municipal yearbook, June 2026; column kept in edit 7)",
  rooms="all", figures=8)
C("p@14126", "ממוצע עירוני של 2.7 או 3.35 מיליון שקל", "sale_avg", "CONFLICT", f"edit {e8}", rooms="all", official="2,512,500 (1-3.2026)", figures=2)
C("p@14465", "שכר דירה ממוצע 7,600; מבוקש 7,200; תשואה 2.9% (5.6.2026)", "rent", "UNSOURCED", "keep (named sources, read 5.6.2026)", figures=3)
C("p@14863", "שכירות 6,200 / 6,950 / 8,500 לפי חדרים", "rent", "UNSOURCED", "keep (named data site, read 5.6.2026)", figures=3)
C("tr@15656", "3 חדרים יד שנייה | מחיר קנייה לדוגמה 2,430,000 שקל", "sale", "CONFLICT", f"edit {e9}", rooms=3, official="2,039,500 (10-12.2025)")
C("tr@15831", "4 חדרים יד שנייה | 2,980,000 שקל", "sale", "CONFLICT", f"edit {e9}", rooms=4, official="2,559,800 (1-3.2026)")
C("tr@16006", "5 חדרים יד שנייה | 3,620,000 שקל", "sale", "CONSISTENT", f"edit {e9}", rooms=5, official="3,648,800 (1-3.2026)")
C("tr@15656..16006", "תשואה גולמית מקורבת כ-3.1% / 2.8% / 2.8%", "yield", "UNSOURCED", f"edit {e9}", figures=3,
  note="computed by the page from the old purchase prices; column removed, nothing recomputed")
C("tr@15656..16182", "שכר דירה 6,200 / 6,950 / 8,500 / 7,200 ושנתי 74,400 / 83,400 / 102,000 / 86,400", "rent", "UNSOURCED",
  "keep (dated; kept word for word inside edit 9)", figures=8)
C("tr@16182", "2.9% לפי המקור", "yield", "UNSOURCED", f"edit {e9}", note="leaves the table with the yield column; stays in p@14465 and tr@6960")
C("p@16975", "דירובוט: 1,135 עסקאות, מחיר ממוצע 3,350,000 שקל", "sale_avg", "CONFLICT", f"edit {e10}", rooms="all", official="2,512,500 (1-3.2026)")
C("p@16975", "דירובוט: 27,000 שקל למ\"ר; 1,135 עסקאות", "per_m2", "UNSOURCED", "keep (named portal, read 5.6.2026; kept inside edit 10)", figures=2)
C("tr@17595..18414", "5 עסקאות מתוארכות, 3-12.3.2026 (2,150,000 עד 4,706,978 שקל)", "deal", "UNSOURCED", "keep (individual dated deals)", figures=10)
C("p@18638", "עסקאות הדוגמה: 2.15-2.21 מיליון (3 חד'), 4.707 (6 חד'), 2.87 ו-2.835 (4 חד')", "deal", "UNSOURCED",
  "keep (the same individual dated deals)", figures=4)
C("p@19882", "3 חדרים 2.0 חדש / 2.43 יד שנייה; 4 חדרים 2.15 / 2.98", "sale_new_used", "CONFLICT", f"edit {e11}", rooms="3,4", figures=4,
  official="2,039,500 (10-12.2025) / 2,559,800 (1-3.2026)", note="3 rooms new 2.0M alone is consistent")
C("p@19882", "5 חדרים 3.59 חדש / 3.62 יד שנייה", "sale_new_used", "CONSISTENT", f"edit {e11}", rooms=5, official="3,648,800 (1-3.2026)",
  figures=2, note="kept inside the rewrite")
C("p@19882", "6 חדרים 4.65 חדש / 4.16 יד שנייה", "sale_new_used", "UNSOURCED", f"edit {e11}", rooms=6, figures=2,
  note="kept inside the rewrite (named data site, read 5.6.2026)")
C("tr@22791", "תשואה ממוצעת של 2.9%", "yield", "UNSOURCED", "keep (same figure as the named, dated portal yield)")
C("p@25201", "FAQ: 3 חדרים 2.4-2.7 מיליון", "sale", "CONFLICT", f"edit {e12}", rooms=3, official="2,039,500 (10-12.2025)")
C("p@25201", "FAQ: 4 חדרים 2.8-3.2 מיליון", "sale", "CONFLICT", f"edit {e12}", rooms=4, official="2,559,800 (1-3.2026)")
C("p@25201", "FAQ: 5 חדרים 3.6-4.1 מיליון", "sale", "CONSISTENT", f"edit {e12}", rooms=5, official="3,648,800 (1-3.2026)")
C("p@25201", "FAQ: 6 חדרים ומעלה 4.1-5.3 מיליון", "sale", "UNSOURCED", f"edit {e12}", rooms=6, note="kept inside the rewrite (dated sources)")
C("p@25543", "FAQ 4 חדרים: מבוקש 3,190,000; חדשה 2.15 מיליון; יד שנייה 2.98 מיליון", "sale", "CONFLICT", f"edit {e13}", rooms=4,
  official="2,559,800 (1-3.2026)", figures=3)
C("p@25543", "FAQ 4 חדרים: 28,482 שקל למ\"ר; שכירות 6,950", "per_m2", "UNSOURCED", f"edit {e13}", rooms=4, figures=2,
  note="kept inside the rewrite (named, dated)")
C("p@25898", "FAQ: שנתון יוני 2026: מוריה 4,120,139, נופים 4,048,211, הפרחים 3,507,639, הציפורים 3,321,363", "sale_nb", "UNSOURCED",
  "keep (municipal yearbook, June 2026)", rooms="all", figures=4)
C("p@25898", "FAQ: מוריה ובוכמן דרום, 25 עסקאות, ממוצע 4,300,000 בשנת 2023", "sale_nb", "STALE", f"edit {e14}", rooms="all", figures=2)
C("p@26228", "FAQ שכירות: 7,600 / 7,200; 6,200 / 6,950 / 8,500", "rent", "UNSOURCED", "keep (named sources, read 5.6.2026)", figures=5)
C("p@27524", "FAQ: מחיר קנייה ממוצע 2,701,971; דירובוט ממוצע 3,350,000", "sale_avg", "CONFLICT", f"edit {e15}", rooms="all",
  official="2,512,500 (1-3.2026)", figures=2)
C("p@27524", "FAQ: 27,000 שקל למ\"ר (דירובוט)", "per_m2", "UNSOURCED", "keep (named portal, read 5.6.2026; kept inside edit 15)")

P.write(notes=(
    "The official list is not on this page yet; these edits assume it will be added. The page names dated sources for most figures "
    "(two portals and a data site read 5.6.2026, the municipal yearbook June 2026, Tax Authority deals of 2023 via a portal). Per the "
    "brief, every city-level 3/4/5-room figure was compared with the official median whatever its label: the asking 3-room 2,650,000 "
    "vs the official 2,039,500 (10-12.2025, the latest published 3-room quarter) is the clearest conflict; the 4-room asking 3,190,000 "
    "vs 2,559,800 and the city averages 2,701,971 / 3,350,000 vs 2,512,500 follow. 2023 neighbourhood deal averages are STALE. "
    "Named and dated non-sale figures are kept: per m2, rents, yield 2.9%, listing counts, the municipal yearbook neighbourhood averages "
    "(all rooms), the 2-room and 6+ asking prices (labelled as asking), and the five March 2026 deals. "
    "Not audited as claims: the if-example 'אם דירת 4 חדרים מוצעת ב-3.45 מיליון שקל' (p@10651), the financing illustration 'פער של "
    "150,000 עד 300,000 שקל' (p@24899), sizes in m2, counts of comparables (5 עד 10). Remaining check.py SUSPECTs (6) are "
    "the individual deals of 3-12.3.2026 (tr@17595..18414 and their recap p@18638), which are dated single deals and stay as they are. "
    "Official quirks: no 3-room median was published for 1-3.2026 (nor 1-3.2025), so 3 rooms is shown for 10-12.2025 against 10-12.2024; "
    "the city medians fell sharply (4 rooms 2,748,200 in 10-12.2025 to 2,559,800 in 1-3.2026, -15.9% in a year; all rooms -18.5% in a "
    "year and about -15% in one quarter), worth a second look before publishing. Name mapping: 'כרמים' on the page = official 'הכרמים'; "
    "'הנחלים', 'הפרחים', 'אבני חן', 'הנביאים', 'המגינים' match; 'משואה' (4 rooms 2,915,000) is not named on the page and is not added. "
    "Unsure: (a) the 2-room asking price 2,700,000 is kept as a dated asking figure although it sits above the official 3-room deal "
    "median; it could be dropped; (b) the neighbourhood table adds rows for הנביאים and המגינים with generic check notes written new; "
    "(c) the purchase/rent table loses its gross-yield column (derived from the old prices) instead of recomputing yields."))
