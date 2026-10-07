# -*- coding: utf-8 -*-
"""Eilat (page 4597): body alignment with the official price list (1-3.2026). Built on the Ashkelon gold example."""
import re
from mk import Page

P = Page("eilat-apartment-prices")


def tbl(headers, rows):
    """table in this page's own style: one line, dir="rtl" on every element."""
    h = "".join(f'<th dir="rtl">{x}</th>' for x in headers)
    b = "".join('<tr dir="rtl">' + "".join(f'<td dir="rtl">{x}</td>' for x in r) + "</tr>" for r in rows)
    return f'<table dir="rtl"><thead dir="rtl"><tr dir="rtl">{h}</tr></thead><tbody dir="rtl">{b}</tbody></table>'


def notes_of(anchor):
    """first cell -> last cell of every body row of the table around anchor (to reuse the page's own notes word for word)."""
    html = P.table_html(anchor)
    out = {}
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", html.split("<tbody", 1)[1], re.S):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        out[cells[0]] = cells[-1]
    return out


# ---------------- edits ----------------
# 1. lead paragraph above the price list
old1 = P.find("מחירי דירות באילת נעים בטווח רחב במיוחד:", "לפי נתוני היצע מסוימים.")
new1 = ("מחירי דירות באילת, לפי נתוני רשות המסים לרבעון הראשון של 2026: חציון מחיר העסקה היה 1,516,100 ₪ לדירת 3 חדרים, "
        "1,719,300 ₪ לדירת 4 חדרים ו-2,587,900 ₪ לדירת 5 חדרים. נכסים גדולים, דירות עם נוף לים, דירות באזור המלונות, גנים ב, "
        "גנים א, מצפה ים או בתים צמודי קרקע יכולים להגיע לסכומים גבוהים בהרבה. נתוני היצע שנבדקו ב-6 ביוני 2026 הצביעו על מאות "
        "נכסים מוצעים למכירה, ועל שכר דירה מבוקש שמתחיל סביב 3,100 ₪ בדירות 2 חדרים ומגיע גם לכ-8,850 ₪ בדירות 5 חדרים.")
e1 = P.edit(old1, new1, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
            "Lead above the list: the 3-room working range 1.1-1.45M excludes the official median 1,516,100 (1-3.2026); the 4- and 5-room ranges "
            "were consistent and are restated as the medians. The undated 2-room range, the all-history deal average (1.12M, far from the "
            "all-apartments median 1,624,100) and the 2021-2025 annual averages (1.65-1.92M) are dropped. The asking rent 3,100-8,850 (listing "
            "data checked 6.6.2026) is kept.")

# 2. asking averages by rooms (June 2026 listing data)
old2 = P.find("על בסיס נתוני ההיצע שנבדקו ביוני 2026, דירות 2 חדרים", "ודירות 6 חדרים ומעלה סביב 3,025,000 ₪.")
new2 = ("בנתוני ההיצע שנבדקו ביוני 2026, דירות 2 חדרים הוצגו סביב 860,000 ₪ בממוצע ביקוש ודירות 6 חדרים ומעלה סביב 3,025,000 ₪. "
        "לדירות 3, 4 ו-5 חדרים יש נתון חזק יותר, חציון מחיר העסקה לפי נתוני רשות המסים: ברבעון הראשון של 2026 הוא היה 1,516,100 ₪ "
        "לדירת 3 חדרים, 1,719,300 ₪ לדירת 4 חדרים ו-2,587,900 ₪ לדירת 5 חדרים.")
e2 = P.edit(old2, new2, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
            "Asking averages by rooms: 3 rooms 1,365,000 (-10%) and 5 rooms 2,450,000 (-5.3%) are outside tolerance of the official medians "
            "1,516,100 and 2,587,900; 4 rooms 1,670,000 was consistent. The 3/4/5 asking averages give way to the medians; the 2-room and 6+-room "
            "asking averages (listing data, June 2026) are kept, and so is the per-m2 sentence that follows.")

# 3. deal averages: all-history average and 2021-2025 annual averages
old3 = P.find("בצד העסקאות, מקור נתונים רחב על אילת הציג 24,567 עסקאות", "סוג הנכס, השכונה והשטח.")
new3 = ("בצד העסקאות, לפי נתוני רשות המסים, חציון מחיר העסקה לכל הדירות באילת היה 1,624,100 ₪ ברבעון הראשון של 2026, לעומת "
        "1,580,000 ₪ ברבעון הראשון של 2025, עלייה של 2.8%. ממוצע של כל העסקאות לאורך שנים מערבב תקופות, סוגי נכסים ושטחים שונים, "
        "ולכן חייבים לבדוק את תקופת העסקה, סוג הנכס, השכונה והשטח.")
e3 = P.edit(old3, new3, ["rooms.all.latest", "rooms.all.year_ago", "rooms.all.change_pct"], "CONFLICT",
            "An all-history average of 24,567 deals of every property type (1,119,463) is far from the official all-apartments median 1,624,100; "
            "the 2021-2025 annual averages are older periods presented as the recent level (STALE). Replaced by the official all-apartments "
            "median with the year-earlier quarter.")

# 4. Shahamon all-history average
old4 = "לפי מקור עסקאות רחב, בשחמון נרשמו 7,506 עסקאות במחיר ממוצע של 1,233,971 ₪."
new4 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה בשחמון היה 1,432,700 ₪ לדירת 3 חדרים, 1,678,300 ₪ לדירת "
        "4 חדרים ו-2,269,800 ₪ לדירת 5 חדרים.")
e4 = P.edit(old4, new4, ["neighbourhoods[שחמון].rooms.3", "neighbourhoods[שחמון].rooms.4", "neighbourhoods[שחמון].rooms.5"], "UNSOURCED",
            "All-rooms, all-history neighbourhood average from an unnamed 'broad deal source' with no period; replaced by the official Shahamon medians.")

# 5. city centre and hotels area averages
old5 = P.find("מרכז העיר הציג 803 עסקאות במחיר ממוצע של 1,782,675 ₪", "שווה מעל 4 מיליון ₪, אלא שהרכב העסקאות שונה:")
new5 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 3 חדרים במרכז העיר היה 1,640,200 ₪, מעל החציון "
        "העירוני לדירת 3 חדרים. באזור המלונות העסקאות מעטות ומגוונות, ומחיר ממוצע גבוה שם אינו אומר שכל נכס באזור שווה סכום כזה, "
        "אלא שהרכב העסקאות שונה:")
e5 = P.edit(old5, new5, ["neighbourhoods[מרכז העיר].rooms.3", "rooms.3.latest"], "UNSOURCED",
            "All-rooms neighbourhood averages (city centre 1,782,675, hotels area 4,296,592) with no period or named source; the city centre gets its "
            "official 3-room median, the hotels area (no official median) is described without a number.")

# 6. Mitzpe Yam, Ganim A/B, Neve Midbar averages
old6 = P.find("מצפה ים הציגה 853 עסקאות", "ונווה מדבר 69 עסקאות במחיר ממוצע של 1,933,492 ₪.")
new6 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 4 חדרים במצפה ים היה 1,384,300 ₪. בגנים א, בגנים ב "
        "ובנווה מדבר העסקאות מעטות יותר.")
e6 = P.edit(old6, new6, ["neighbourhoods[מצפה ים].rooms.4"], "UNSOURCED",
            "All-rooms neighbourhood averages with no period or named source; Mitzpe Yam gets its official 4-room median, Ganim A, Ganim B and Neve "
            "Midbar have no official median and are described without numbers.")

# 7. sentence before the rooms table
old7 = "טבלת חדרים נותנת נקודת התחלה נוחה, אך באילת היא עלולה להטעות כאשר לא בודקים שטח, מיקום, נוף, קומה וסוג בניין."
new7 = ("הטבלה הבאה מציגה את חציון מחיר העסקה באילת לפי מספר חדרים, לפי נתוני רשות המסים לרבעון הראשון של 2026, לצד החציון "
        "באותו רבעון שנה קודם לכן. המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים ודירות 6 חדרים ומעלה כדאי לבדוק "
        "מול עסקאות דומות ברחוב ובשכונה. טבלת חדרים נותנת נקודת התחלה נוחה, אך באילת היא עלולה להטעות כאשר לא בודקים שטח, מיקום, "
        "נוף, קומה וסוג בניין.")
e7 = P.edit(old7, new7, ["data_quarter"], "WORDING", "Introduces the replaced rooms table (edit 8); the 2-room and 6+-room rows leave it.")

# 8. rooms table
A8 = '<th dir="rtl">טווח עבודה לקונה או מוכר</th>'
N8 = notes_of(A8)
new8 = tbl(["סוג נכס", "חציון מחיר העסקה, ינואר-מרץ 2026", "ינואר-מרץ 2025", "שינוי בשנה", "איך לקרוא את הנתון"], [
    ["3 חדרים", "1,516,100 ₪", "1,505,800 ₪", "עלייה של 0.7%", N8["3 חדרים"]],
    ["4 חדרים", "1,719,300 ₪", "1,781,400 ₪", "ירידה של 3.5%", N8["4 חדרים"]],
    ["5 חדרים", "2,587,900 ₪", "2,506,300 ₪", "עלייה של 3.3%", N8["5 חדרים"]],
])
e8 = P.table(A8, new8, ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct",
                        "rooms.5.latest", "rooms.5.year_ago", "rooms.5.change_pct"], "CONFLICT",
             "Rooms table: the 3-room working range and the 3- and 5-room asking averages (1,365,000 / 2,450,000) contradict the official medians; "
             "the 2-room and 6+-room rows have no official series and the per-m2 column is asking data (it stays in the paragraph after the "
             "price list). Replaced by the official medians with the year-earlier quarter; the notes of rows 3-5 are kept word for word.")

# 9. property-type averages paragraph
old9 = P.find("לפי פילוח סוגי נכסים במאגר עסקאות רחב,", "דירת גג במחיר ממוצע של 1,753,809 ₪.")
new9 = ("לפי נתוני רשות המסים, חציון מחיר העסקה לכל הדירות באילת ברבעון הראשון של 2026 היה 1,624,100 ₪. בניין, קרקע, קוטג' דו "
        "משפחתי, דירת גן, וילה ודירת גג מתומחרים אחרת, ולכל סוג נכס כזה צריך מדגם עסקאות משלו ולא השוואה לחציון של דירה רגילה.")
e9 = P.edit(old9, new9, ["rooms.all.latest"], "CONFLICT",
            "All-history average for apartments (1,016,692) is far from the official all-apartments median 1,624,100; the averages for buildings, "
            "land, cottages, garden flats, villas and penthouses have no period or named source and no official counterpart.")

# 10. property-type table: keep the type and its meaning, drop the unsourced counts and averages
A10 = '<th dir="rtl">מספר עסקאות שנמצא</th>'
N10 = notes_of(A10)
new10 = tbl(["סוג נכס", "משמעות לשווי"], [[k, v] for k, v in N10.items()])
e10 = P.table(A10, new10, ["rooms.all.latest"], "CONFLICT",
              "Property-type table: the apartment average 1,016,692 conflicts with the official all-apartments median; the other averages and the "
              "deal counts have no period or named source. The table keeps the property types and the page's own 'meaning for value' notes, word for word.")

# 11. paragraph above the neighbourhood table
old11 = P.find("השוואת שכונות באילת צריכה להתחיל ממספר העסקאות", "נכסים עם שימוש תיירותי.")
new11 = ("השוואת שכונות באילת צריכה להתחיל ממספר החדרים, סוג הנכסים ומידת הדמיון לנכס הנבדק. שכונה עם עסקאות רבות מספקת מדגם "
         "רחב יותר משכונה עם עסקאות בודדות, ואזור שבו המחיר הממוצע גבוה מאוד, כמו אזור המלונות, אינו בהכרח מתאים להשוואה לדירת "
         "מגורים רגילה, אם חלק מהעסקאות כוללות נכסים מיוחדים או נכסים עם שימוש תיירותי. הטבלה הבאה מציגה את חציון מחיר העסקה לפי "
         "שכונה ומספר חדרים, לפי נתוני רשות המסים לרבעון הראשון של 2026; בשכונות שאינן בטבלה, כמו הדקל, אורים, גנים א, גנים ב "
         "ונווה מדבר, בודקים מול עסקאות דומות ברחוב.")
e11 = P.edit(old11, new11, ["data_quarter"], "UNSOURCED",
             "Deal counts (7,506 / 69) and the hotels-area average 4,296,592 with no period or named source; rephrased without numbers and "
             "turned into the introduction of the official neighbourhood table (edit 12).")

# 12. neighbourhood table
A12 = '<th dir="rtl">עסקאות שנמצאו</th>'
N12 = notes_of(A12)
NB = [("שחמון", "1,432,700 ₪", "1,678,300 ₪", "2,269,800 ₪"),
      ("בנה ביתך", "1,287,800 ₪", "לא פורסם", "לא פורסם"),
      ("מרכז העיר", "1,640,200 ₪", "לא פורסם", "לא פורסם"),
      ("צאלים", "986,500 ₪", "1,471,500 ₪", "לא פורסם"),
      ("הערבה", "893,300 ₪", "לא פורסם", "לא פורסם"),
      ("אופיר", "999,400 ₪", "לא פורסם", "לא פורסם"),
      ("יעלים", "לא פורסם", "1,054,100 ₪", "לא פורסם"),
      ("מצפה ים", "לא פורסם", "1,384,300 ₪", "לא פורסם")]
new12 = tbl(["שכונה", "3 חדרים", "4 חדרים", "5 חדרים", "אות מחיר מרכזי"], [list(r) + [N12[r[0]]] for r in NB])
e12 = P.table(A12, new12, ["neighbourhoods[שחמון].rooms.3", "neighbourhoods[שחמון].rooms.4", "neighbourhoods[שחמון].rooms.5",
                           "neighbourhoods[בנה ביתך].rooms.3", "neighbourhoods[מרכז העיר].rooms.3", "neighbourhoods[צאלים].rooms.3",
                           "neighbourhoods[צאלים].rooms.4", "neighbourhoods[הערבה].rooms.3", "neighbourhoods[אופיר].rooms.3",
                           "neighbourhoods[יעלים].rooms.4", "neighbourhoods[מצפה ים].rooms.4"], "UNSOURCED",
              "Neighbourhood table: 15 all-rooms, all-history averages with deal counts from an unnamed source and no period; replaced by the "
              "official neighbourhood medians by rooms, 1-3.2026 ('לא פורסם' where the official file has no median). The page's own notes are "
              "kept word for word for the 8 neighbourhoods in the official list.")

# 13. street examples of 2023 (first street paragraph)
old13 = P.find("מתוך דוגמאות עסקאות רחוב לשנת 2023 נמצאו", "ו-9 עסקאות במשעול הגאונים במחיר ממוצע של 642,222 ₪.")
new13 = ("דוגמאות עסקאות רחוב משנת 2023 הראו פער גדול בין רחובות כמו עין נטפים, חטיבת הנגב, שדרות ששת הימים ודרך יותם, שבהם "
         "המחיר הממוצע היה גבוה יותר, לבין משעול התלמוד, מלכת שבא, משעול הגאונים וצין, שבהם הוא היה נמוך בהרבה. גם בין השכונות "
         "הפער גדול: לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 3 חדרים היה 893,300 ₪ בהערבה ו-1,640,200 ₪ "
         "במרכז העיר.")
e13 = P.edit(old13, new13, ["neighbourhoods[הערבה].rooms.3", "neighbourhoods[מרכז העיר].rooms.3"], "STALE",
             "Street averages from 2023 deal examples (10 streets, all rooms) shown as the street level; the 2023 contrast is kept in words and "
             "the current gap is shown with two official neighbourhood medians.")

# 14-15. rent paragraph and rent table: the older 'contractor or aggregation' source (tier 2)
old14 = P.find("מולו, מקור ישן או אגרגטיבי יותר בהקשר דירות חדשות וקבלן הציג נתוני שכירות נמוכים יותר:", "ו-5 חדרים 3,096 ₪ ותשואה 3.4%.")
new14 = "מולו, מקור ישן או אגרגטיבי יותר בהקשר דירות חדשות וקבלן, בלי תאריך עדכון, הציג נתוני שכירות ותשואה נמוכים בהרבה."
e14 = P.edit(old14, new14, ["page"], "UNSOURCED",
             "Rent 1,341-3,096 and yields 3.4-5.1% from a source the page itself calls old, with no date; rephrased without the numbers.", tier=2)

A15 = '<th dir="rtl">שכר דירה לפי מקור קבלן או אגרגציה ישן יותר</th>'
old15_html = P.table_html(A15)
R15 = []
for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", old15_html.split("<tbody", 1)[1], re.S):
    c = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
    R15.append([c[0], c[1], c[3]])
new15 = tbl(["מספר חדרים", "שכר דירה לפי מקור ביקוש עדכני", "מסר לקונה"], R15)
e15 = P.table(A15, new15, ["page"], "UNSOURCED",
              "Rent table: the column of the undated old source (rents and yields) is removed; the current asking-rent column (page checked "
              "6.6.2026) and the buyer notes are kept word for word.", tier=2)

# 16. street sample paragraph in the recent-deals section
old16 = P.find("באילת, מדגם רחוב יכול להראות טווחים גדולים גם בתוך אותה עיר.", "מציגים רמות מחיר שונות לגמרי.")
new16 = ("באילת, מדגם רחוב יכול להראות טווחים גדולים גם בתוך אותה עיר, ולכן עסקה ישנה ברחוב מסוים היא רק נקודת התחלה. גם החציון "
         "העירוני משתנה מרבעון לרבעון, ולכן משווים לעסקאות מאותה תקופה. הטבלה הבאה מציגה את חציון מחיר העסקה באילת לפי מספר חדרים, "
         "מינואר-מרץ 2025 ועד ינואר-מרץ 2026, לפי נתוני רשות המסים.")
e16 = P.edit(old16, new16, ["data_quarter"], "STALE",
             "The same 2023 street averages repeated without a date as the level of each street; rephrased without numbers and turned into the "
             "introduction of the quarterly table (edit 17).")

# 17. street table -> official quarterly medians
A17 = '<th dir="rtl">רחוב או אזור עסקה</th>'
new17 = tbl(["רבעון", "3 חדרים", "4 חדרים", "5 חדרים"], [
    ["ינואר-מרץ 2025", "1,505,800 ₪", "1,781,400 ₪", "2,506,300 ₪"],
    ["אפריל-יוני 2025", "1,181,600 ₪", "1,337,400 ₪", "לא פורסם"],
    ["יולי-ספטמבר 2025", "1,253,600 ₪", "1,633,800 ₪", "2,277,700 ₪"],
    ["אוקטובר-דצמבר 2025", "1,434,300 ₪", "1,623,100 ₪", "2,432,400 ₪"],
    ["ינואר-מרץ 2026", "1,516,100 ₪", "1,719,300 ₪", "2,587,900 ₪"],
])
e17 = P.table(A17, new17, ["rooms.3.quarters[1-3.2025]", "rooms.3.quarters[4-6.2025]", "rooms.3.quarters[7-9.2025]", "rooms.3.quarters[10-12.2025]",
                           "rooms.3.quarters[1-3.2026]", "rooms.4.quarters[1-3.2025]", "rooms.4.quarters[4-6.2025]", "rooms.4.quarters[7-9.2025]",
                           "rooms.4.quarters[10-12.2025]", "rooms.4.quarters[1-3.2026]", "rooms.5.quarters[1-3.2025]", "rooms.5.quarters[7-9.2025]",
                           "rooms.5.quarters[10-12.2025]", "rooms.5.quarters[1-3.2026]"], "STALE",
              "Street table: 2023 street averages (10 rows, all rooms) presented as street levels. No official street data exists, so the table now "
              "shows the official city medians by rooms for the last five quarters, which serves the section's point (deal period matters).")

# 18. Shahamon vs asking averages (new projects section)
old18 = P.find("כאשר ממוצע עסקאות רחב בשחמון עומד על 1,233,971 ₪,", "קומות, נוף ומפרט.")
new18 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה בשחמון היה 1,678,300 ₪ לדירת 4 חדרים ו-2,269,800 ₪ לדירת "
         "5 חדרים. כאשר מודעה בשחמון מבקשת סכום גבוה בהרבה, הפער עשוי לשקף תמהיל שונה של שטחים, בנייה חדשה, קומות, נוף ומפרט.")
e18 = P.edit(old18, new18, ["neighbourhoods[שחמון].rooms.4", "neighbourhoods[שחמון].rooms.5"], "CONFLICT",
             "Shahamon all-history average 1,233,971 (unsourced) set against city asking averages 1,670,000 (4 rooms, consistent) and 2,450,000 "
             "(5 rooms, outside tolerance of 2,587,900); replaced by the official Shahamon 4- and 5-room medians.")

# 19. Ganim A/B averages
old19 = P.find("גנים א הציגה 229 עסקאות במחיר ממוצע של 1,748,264 ₪", "אך מספר העסקאות קטן בהרבה משחמון.")
new19 = "הפער בינן לבין שכונות ותיקות כמו אורים, הערבה או אופיר משמעותי, אך מספר העסקאות בהן קטן בהרבה משחמון."
e19 = P.edit(old19, new19, ["page"], "UNSOURCED",
             "Ganim A / Ganim B all-rooms averages with no period or named source and no official median; rephrased without numbers.")

# 20. hotels-area average
old20 = "מחיר ממוצע של 4,296,592 ₪ באזור המלונות אינו מתאים להשוואה אוטומטית לדירת 3 חדרים בשכונה רגילה."
new20 = "מחיר ממוצע גבוה באזור המלונות אינו מתאים להשוואה אוטומטית לדירת 3 חדרים בשכונה רגילה."
e20 = P.edit(old20, new20, ["page"], "UNSOURCED", "Hotels-area average 4,296,592 with no period or named source; the number is dropped.")

# 21-27. FAQ answers
old21 = "טווח עבודה סביר לדירת 2 חדרים באילת הוא לרוב סביב 800,000-1,050,000 ₪, כאשר מקור ביקוש שנבדק הציג ממוצע סביב 860,000 ₪ ומחיר למ\"ר סביב 17,200 ₪."
new21 = ("המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים, ולכן דירת 2 חדרים באילת כדאי לבדוק מול עסקאות דומות ברחוב ובשכונה. "
         "בנתוני ההיצע שנבדקו ביוני 2026 הופיע ממוצע ביקוש סביב 860,000 ₪ לדירת 2 חדרים ומחיר למ\"ר סביב 17,200 ₪.")
e21 = P.edit(old21, new21, ["page"], "UNSOURCED",
             "FAQ 2 rooms: the 'working range' 800,000-1,050,000 has no source; the asking average and asking per-m2 (listing data, June 2026) are kept.")

old22 = "דירת 3 חדרים באילת נעה בדרך כלל סביב 1,100,000-1,450,000 ₪, ובנתוני ביקוש מסוימים הופיע ממוצע של 1,365,000 ₪ ומחיר למ\"ר של 18,200 ₪."
new22 = "לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 3 חדרים באילת ברבעון הראשון של 2026 היה 1,516,100 ₪, לעומת 1,505,800 ₪ שנה קודם לכן."
e22 = P.edit(old22, new22, ["rooms.3.latest", "rooms.3.year_ago"], "CONFLICT", "FAQ 3 rooms: 1.1-1.45M and the 1,365,000 asking average vs the official 1,516,100.")

old23 = "דירת 4 חדרים באילת נעה לרוב סביב 1,450,000-1,900,000 ₪. ממוצע ביקוש שנמצא עמד על 1,670,000 ₪ ומחיר למ\"ר של 16,700 ₪."
new23 = "לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 4 חדרים באילת ברבעון הראשון של 2026 היה 1,719,300 ₪, לעומת 1,781,400 ₪ שנה קודם לכן."
e23 = P.edit(old23, new23, ["rooms.4.latest", "rooms.4.year_ago"], "CONSISTENT",
             "FAQ 4 rooms: the range and the asking average were consistent with 1,719,300; the answer is rewritten from the same facts as the body.")

old24 = "דירת 5 חדרים באילת נעה לרוב סביב 2,100,000-2,700,000 ₪, ובחלק מנתוני הביקוש הופיע ממוצע של 2,450,000 ₪ ומחיר למ\"ר של 14,848 ₪."
new24 = "לפי נתוני רשות המסים, חציון מחיר העסקה לדירת 5 חדרים באילת ברבעון הראשון של 2026 היה 2,587,900 ₪, לעומת 2,506,300 ₪ שנה קודם לכן."
e24 = P.edit(old24, new24, ["rooms.5.latest", "rooms.5.year_ago"], "CONFLICT",
             "FAQ 5 rooms: the 2,450,000 asking average is outside tolerance of the official 2,587,900 (the 2.1-2.7M range itself was consistent).")

old25 = P.find("לפי נתוני עסקאות רחבים, אזור המלונות הציג ממוצע גבוה מאוד", "ונווה מדבר 1,933,492 ₪.")
new25 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 3 חדרים היה 1,640,200 ₪ במרכז העיר ו-1,432,700 ₪ "
         "בשחמון, ולדירת 4 חדרים 1,678,300 ₪ בשחמון. אזור המלונות, גנים ב ונווה מדבר מציגים ממוצעים גבוהים מאוד.")
e25 = P.edit(old25, new25, ["neighbourhoods[מרכז העיר].rooms.3", "neighbourhoods[שחמון].rooms.3", "neighbourhoods[שחמון].rooms.4"], "UNSOURCED",
             "FAQ priciest neighbourhood: all-rooms averages (4,296,592 / 2,963,280 / 1,933,492) with no period or named source; replaced by "
             "official neighbourhood medians, the three areas without an official median are named without numbers.")

old26 = P.find("נתון רחב הציג בשחמון 7,506 עסקאות במחיר ממוצע של 1,233,971 ₪.", "אך כל דירה צריכה להיבדק לגופה.")
new26 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה לדירת 3 חדרים היה 1,432,700 ₪ בשחמון, לעומת 986,500 ₪ "
         "בצאלים, 999,400 ₪ באופיר ו-893,300 ₪ בהערבה, אך כל דירה צריכה להיבדק לגופה.")
e26 = P.edit(old26, new26, ["neighbourhoods[שחמון].rooms.3", "neighbourhoods[צאלים].rooms.3", "neighbourhoods[אופיר].rooms.3",
                            "neighbourhoods[הערבה].rooms.3"], "UNSOURCED",
             "FAQ Shahamon vs older neighbourhoods: all-rooms, all-history averages (Shahamon 1,233,971; Arava, Urim, Ofir, Hadekel) without "
             "period or named source; replaced by official 3-room medians (Urim and Hadekel have none).")

old27 = "באילת נמצאו למשל דירות 3 חדרים בממוצע ביקוש סביב 1,365,000 ₪, אך עסקאות לפי רחוב ושנה יכולות להראות מספרים אחרים לגמרי."
new27 = ("באילת, למשל, חציון מחיר העסקה לדירת 3 חדרים ברבעון הראשון של 2026 היה 1,516,100 ₪ לפי נתוני רשות המסים, אך מודעות "
         "ועסקאות לפי רחוב ושנה יכולות להראות מספרים אחרים לגמרי.")
e27 = P.edit(old27, new27, ["rooms.3.latest"], "CONFLICT", "FAQ asking vs deal: the 3-room asking average 1,365,000 vs the official median 1,516,100.")

# ---------------- claims inventory ----------------
C = P.claim
C("p@4299", "דירת 2 חדרים סביב 800,000-1,050,000 ₪", "sale", "UNSOURCED", f"edit {e1}", rooms=2, note="no official 2-room series, no source; dropped")
C("p@4299", "דירת 3 חדרים סביב 1,100,000-1,450,000 ₪", "sale", "CONFLICT", f"edit {e1}", rooms=3, official="1,516,100 (1-3.2026)")
C("p@4299", "דירת 4 חדרים סביב 1,450,000-1,900,000 ₪", "sale", "CONSISTENT", f"edit {e1}", rooms=4, official="1,719,300 (1-3.2026)", note="restated as the median")
C("p@4299", "דירת 5 חדרים סביב 2,100,000-2,700,000 ₪", "sale", "CONSISTENT", f"edit {e1}", rooms=5, official="2,587,900 (1-3.2026)", note="restated as the median")
C("p@4299", "ממוצע עסקאות היסטורי סביב 1.12 מיליון ₪", "sale_avg", "CONFLICT", f"edit {e1}", rooms="all", official="1,624,100 (all apartments, 1-3.2026)")
C("p@4299", "ממוצעי עסקאות שנתיים של כ-1.65-1.92 מיליון ₪ בשנים האחרונות", "sale_avg", "STALE", f"edit {e1}", rooms="all", official="1,624,100 (1-3.2026)", note="2021-2025 annual averages, all property types")
C("p@4299", "שכר דירה שמתחיל סביב 3,100 ₪ (2 חד') ומגיע לכ-8,850 ₪ (5 חד')", "rent", "UNSOURCED", "keep (listing data checked 6.6.2026, dated in the sentence)", figures=2)
C("p@42485", "דירות 2 חדרים הוצגו סביב 860,000 ₪ בממוצע ביקוש", "sale", "UNSOURCED", "keep (listing data, June 2026, dated in the sentence)", rooms=2)
C("p@42485", "דירות 3 חדרים סביב 1,365,000 ₪ (ממוצע ביקוש)", "sale", "CONFLICT", f"edit {e2}", rooms=3, official="1,516,100 (-10%)")
C("p@42485", "דירות 4 חדרים סביב 1,670,000 ₪ (ממוצע ביקוש)", "sale", "CONSISTENT", f"edit {e2}", rooms=4, official="1,719,300 (-2.9%)", note="replaced by the median in the same rewrite")
C("p@42485", "דירות 5 חדרים סביב 2,450,000 ₪ (ממוצע ביקוש)", "sale", "CONFLICT", f"edit {e2}", rooms=5, official="2,587,900 (-5.3%)")
C("p@42485", "דירות 6 חדרים ומעלה סביב 3,025,000 ₪ (ממוצע ביקוש)", "sale", "UNSOURCED", "keep (listing data, June 2026, dated in the sentence)", rooms=6)
C("p@42485", "מחיר למ\"ר בביקוש: 17,200 / 18,200 / 16,700 / 14,848 / 12,900 ₪", "per_m2", "UNSOURCED", "keep (listing data, June 2026, same paragraph)", figures=5)
C("p@42949", "24,567 עסקאות, מחיר ממוצע של 1,119,463 ₪", "sale_avg", "CONFLICT", f"edit {e3}", rooms="all", official="1,624,100 (1-3.2026)", note="all-history average, every property type")
C("p@42949", "2025: 909 עסקאות במחיר ממוצע של 1,695,617 ₪", "sale_avg", "STALE", f"edit {e3}", rooms="all", official="1,624,100 (1-3.2026)", note="a 2025 mean of all property types presented as the recent level")
C("p@42949", "2024-2021: 1,864,420 / 1,650,005 / 1,921,145 / 1,884,283 ₪", "sale_avg", "STALE", f"edit {e3}", rooms="all", figures=4)
C("p@43529", "188 מודעות, ממוצע 4,486, חציון 3,585, מינימום 530 ₪ (סוף מאי 2026)", "rent", "UNSOURCED", "keep (listing data dated end of May 2026)", figures=3)
C("p@43529", "שכר דירה מבוקש ממוצע 3,500; לפי חדרים 3,100 / 3,900 / 6,250 / 8,850 ₪", "rent", "UNSOURCED", "keep (asking-rent source, page checked 6.6.2026)", figures=5)
C("p@43529", "תשואה ממוצעת של 6.1%", "yield", "UNSOURCED", "keep (same asking-rent source, page checked 6.6.2026)")
C("p@44768", "בשחמון 7,506 עסקאות במחיר ממוצע של 1,233,971 ₪", "sale_nb", "UNSOURCED", f"edit {e4}", official="Shahamon 3/4/5: 1,432,700 / 1,678,300 / 2,269,800")
C("p@45189", "מרכז העיר 1,782,675 ₪; המלונות 4,296,592 ₪ (ממוצעים)", "sale_nb", "UNSOURCED", f"edit {e5}", figures=2, official="city centre 3 rooms 1,640,200", note="also the derived 'above 1.7M / 4M' wording")
C("p@45618", "מצפה ים 1,147,722; גנים א 1,748,264; גנים ב 2,963,280; נווה מדבר 1,933,492", "sale_nb", "UNSOURCED", f"edit {e6}", figures=4, official="Mitzpe Yam 4 rooms 1,384,300")
C("tr@47827", "2 חדרים | 800,000-1,050,000 | 860,000 | 17,200 למ\"ר", "sale", "UNSOURCED", f"edit {e8}", rooms=2, figures=3, note="asking average and per-m2 stay in p@42485")
C("tr@48033", "3 חדרים | 1,100,000-1,450,000 ₪", "sale", "CONFLICT", f"edit {e8}", rooms=3, official="1,516,100")
C("tr@48033", "3 חדרים | ממוצע ביקוש 1,365,000 ₪", "sale", "CONFLICT", f"edit {e8}", rooms=3, official="1,516,100")
C("tr@48033", "3 חדרים | 18,200 ₪ למ\"ר", "per_m2", "UNSOURCED", f"edit {e8}", rooms=3, note="column removed; the figure stays in p@42485")
C("tr@48251", "4 חדרים | 1,450,000-1,900,000 ₪", "sale", "CONSISTENT", f"edit {e8}", rooms=4, official="1,719,300")
C("tr@48251", "4 חדרים | ממוצע ביקוש 1,670,000 ₪", "sale", "CONSISTENT", f"edit {e8}", rooms=4, official="1,719,300 (-2.9%)")
C("tr@48251", "4 חדרים | 16,700 ₪ למ\"ר", "per_m2", "UNSOURCED", f"edit {e8}", rooms=4)
C("tr@48460", "5 חדרים | 2,100,000-2,700,000 ₪", "sale", "CONSISTENT", f"edit {e8}", rooms=5, official="2,587,900")
C("tr@48460", "5 חדרים | ממוצע ביקוש 2,450,000 ₪", "sale", "CONFLICT", f"edit {e8}", rooms=5, official="2,587,900 (-5.3%)")
C("tr@48460", "5 חדרים | 14,848 ₪ למ\"ר", "per_m2", "UNSOURCED", f"edit {e8}", rooms=5)
C("tr@48675", "6 חדרים ומעלה | 2,700,000 ומעלה | 3,025,000 | 12,900 למ\"ר", "sale", "UNSOURCED", f"edit {e8}", rooms=6, figures=3)
C("p@49248", "22,694 עסקאות בדירות במחיר ממוצע של 1,016,692 ₪", "sale_avg", "CONFLICT", f"edit {e9}", rooms="all", official="1,624,100 (1-3.2026)")
C("p@49248", "בניין 2,010,951; קרקע 5,082,600; קוטג' 1,335,097; דירת גן 1,303,740; וילה 2,215,116; דירת גג 1,753,809", "other", "UNSOURCED", f"edit {e9}", figures=6)
C("tr@49876", "דירה | 22,694 | 1,016,692 ₪", "sale_avg", "CONFLICT", f"edit {e10}", rooms="all", official="1,624,100")
C("tr@50020..50775", "טבלת ממוצעים לפי סוג נכס (6 שורות: בניין עד דירת גג)", "other", "UNSOURCED", f"edit {e10}", figures=6)
C("p@51366", "אזור עם מחיר ממוצע של 4,296,592 ₪", "sale_nb", "UNSOURCED", f"edit {e11}")
C("tr@51894..54060", "טבלת ממוצעי עסקאות לפי שכונה (15 שורות)", "sale_nb", "UNSOURCED", f"edit {e12}", figures=15, official="8 official neighbourhoods, 1-3.2026")
C("p@54593", "עסקאות רחוב 2023: עין נטפים 1,569,950 ... משעול הגאונים 642,222 ₪", "sale_street", "STALE", f"edit {e13}", figures=10)
C("p@55564", "שכר דירה ממוצע 4,486 ₪, חציון 3,585 ₪", "rent", "UNSOURCED", "keep (listing data dated end of May 2026, p@43529)", figures=2)
C("p@55942", "188 מודעות; ממוצע 4,486, חציון 3,585, מינימום 530; ממוצעי שכירות ל-14 שכונות", "rent", "UNSOURCED", "keep (listing data dated end of May 2026)", figures=17)
C("tr@56875..58481", "טבלת שכירות לפי שכונה (12 שורות + כלל העיר)", "rent", "UNSOURCED", "keep (listing data dated end of May 2026, previous paragraph)", figures=14)
C("p@58633", "מקור נוסף: 3,100 / 3,900 / 6,250 / 8,850 ₪ לפי חדרים", "rent", "UNSOURCED", "keep (asking-rent source, page checked 6.6.2026)", figures=4)
C("p@58633", "מקור ישן: שכירות 1,341 / 1,998 / 2,321 / 3,096 ₪", "rent", "UNSOURCED", f"edit {e14}", figures=4, note="the page calls the source old; no date")
C("p@58633", "מקור ישן: תשואה 5.1% / 4.6% / 3.7% / 3.4%", "yield", "UNSOURCED", f"edit {e14}", figures=4)
C("tr@59403..59931", "טבלת שכירות: עמודת מקור ביקוש עדכני 3,100-8,850 ₪", "rent", "UNSOURCED", "keep (asking-rent source, page checked 6.6.2026)", figures=4)
C("tr@59403..59931", "טבלת שכירות: עמודת מקור ישן 1,341-3,096 ₪", "rent", "UNSOURCED", f"edit {e15}", figures=4)
C("tr@59403..59931", "טבלת שכירות: תשואות 5.1% / 4.6% / 3.7% / 3.4%", "yield", "UNSOURCED", f"edit {e15}", figures=4)
C("p@61168", "מדגם רחוב: עין נטפים 1,569,950 ... אילות 1,008,636 ₪", "sale_street", "STALE", f"edit {e16}", figures=10, note="the 2023 street sample repeated without its date")
C("tr@61988..63303", "טבלת ממוצעי רחוב בדוגמה (10 שורות)", "sale_street", "STALE", f"edit {e17}", figures=10)
C("p@64238", "ריבית 3.75% (25.5.2026); מחירי דיור +0.3% חודשי, -1.2% שנתי", "macro", "UNSOURCED", "keep (dated Bank of Israel decision, 25.5.2026)", figures=3)
C("p@65253", "ממוצע עסקאות רחב בשחמון 1,233,971 ₪", "sale_nb", "UNSOURCED", f"edit {e18}", official="Shahamon 4/5: 1,678,300 / 2,269,800")
C("p@65253", "דירות 4 חדרים בממוצעי ביקוש סביב 1,670,000 ₪", "sale", "CONSISTENT", f"edit {e18}", rooms=4, official="1,719,300 (-2.9%)")
C("p@65253", "דירות 5 חדרים סביב 2,450,000 ₪", "sale", "CONFLICT", f"edit {e18}", rooms=5, official="2,587,900 (-5.3%)")
C("p@65605", "גנים א 229 עסקאות 1,748,264 ₪; גנים ב 102 עסקאות 2,963,280 ₪", "sale_nb", "UNSOURCED", f"edit {e19}", figures=2)
C("p@65992", "מחיר ממוצע של 4,296,592 ₪ באזור המלונות", "sale_nb", "UNSOURCED", f"edit {e20}")
C("tr@69062", "ריבית של 3.75% משפיעה על כוח הקנייה", "macro", "UNSOURCED", "keep (Bank of Israel, 25.5.2026, dated in p@64238)")
C("p@70193", "תשואה ממוצעת של 6.1% במקור אחד", "yield", "UNSOURCED", "keep (asking-rent source of p@43529, page checked 6.6.2026)")
C("p@71011", "FAQ: טווח עבודה לדירת 2 חדרים 800,000-1,050,000 ₪", "sale", "UNSOURCED", f"edit {e21}", rooms=2)
C("p@71011", "FAQ: ממוצע ביקוש 860,000 ₪, 17,200 ₪ למ\"ר (2 חדרים)", "sale", "UNSOURCED", "keep (listing data, June 2026; the date is added in the same rewrite)", rooms=2, figures=2)
C("p@71340", "FAQ: דירת 3 חדרים 1,100,000-1,450,000, ממוצע ביקוש 1,365,000, 18,200 למ\"ר", "sale", "CONFLICT", f"edit {e22}", rooms=3, official="1,516,100", figures=3)
C("p@71634", "FAQ: דירת 4 חדרים 1,450,000-1,900,000, ממוצע ביקוש 1,670,000, 16,700 למ\"ר", "sale", "CONSISTENT", f"edit {e23}", rooms=4, official="1,719,300", figures=3, note="per-m2 asking figure dropped from the answer; it stays in p@42485")
C("p@71905", "FAQ: דירת 5 חדרים 2,100,000-2,700,000, ממוצע ביקוש 2,450,000, 14,848 למ\"ר", "sale", "CONFLICT", f"edit {e24}", rooms=5, official="2,587,900", figures=3, note="range consistent, asking average in conflict")
C("p@72184", "FAQ: המלונות 4,296,592; גנים ב 2,963,280; נווה מדבר 1,933,492 ₪", "sale_nb", "UNSOURCED", f"edit {e25}", figures=3)
C("p@72532", "FAQ: שחמון 1,233,971; הערבה 587,881; אורים 587,593; אופיר 613,913; הדקל 707,600", "sale_nb", "UNSOURCED", f"edit {e26}", figures=5)
C("p@72917", "FAQ שכירות: 4,486 / 3,585; לפי חדרים 3,100 / 3,900 / 6,250 / 8,850 ₪", "rent", "UNSOURCED", "keep (listing data end of May 2026 and asking-rent source, page checked 6.6.2026)", figures=6)
C("p@73725", "FAQ: דירות 3 חדרים בממוצע ביקוש סביב 1,365,000 ₪", "sale", "CONFLICT", f"edit {e27}", rooms=3, official="1,516,100")
C("p@74413", "FAQ: ריבית 3.75% (25.5.2026)", "macro", "UNSOURCED", "keep (dated Bank of Israel decision)")

P.write(notes=(
    "Not audited as claims (illustrations, not market statements): the per-m2 if-example 18,200 / 16,700 (p@63458, 'אם דירת 3 חדרים מוצעת לפי'), "
    "the buyer if-example 1,670,000 price / 120,000 renovation / 3,900 vs 6,250 rent (p@69868, no room count), sizes 90 / 55 m2 (p@60898), "
    "'6-10 עסקאות' and '5 שכבות' (counts of steps). Rent and listing figures (end of May 2026 listing data, the June 2026 asking data, the "
    "asking-rent source with its 6.1% yield) are kept because the page dates them or shows its check date (עודכן ונבדק: 2026-06-06) and names "
    "the kind of source; the rent/yield of the 'old contractor or aggregation' source, which the page itself calls old and does not date, is "
    "removed in tier 2 (edits 14-15). The neighbourhood, street and property-type averages came from an unnamed 'broad deal database' covering "
    "all years and all property types; they are replaced by official neighbourhood medians where the official file has them (8 neighbourhoods; "
    "Hadekel, Urim, Ganim A, Ganim B, Neve Midbar, the hotels area and the new industrial zone have none and are named without numbers). "
    "The 2023 street table has no official counterpart, so it now shows the official city medians for the last five quarters (edit 17). "
    "Official quirk: a sharp dip in 4-6.2025 (3 rooms 1,181,600, 4 rooms 1,337,400; no 5-room median that quarter) between 1,505,800 / "
    "1,781,400 a quarter earlier and the recovery to 1,516,100 / 1,719,300 in 1-3.2026; the quarterly table shows it as published. "
    "Name mapping: 'ערבה' in the rent text = official 'הערבה'; all other names match the official file exactly. Remaining SUSPECT lines, if any, "
    "are listed by check.py."))
