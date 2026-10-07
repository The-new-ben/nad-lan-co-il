# -*- coding: utf-8 -*-
"""Herzliya (page 154): body alignment with the official price list (1-3.2026). Built on the gold example b_ashkelon.py.
The page has no visible check date, so undated rent and per-m2 figures are rephrased without numbers (tier 2)."""
from mk import Page

P = Page("herzliya-apartment-prices")


def tbl(head, rows):
    """table in this page's own HTML style (single spaces between tags, one line)."""
    h = " ".join(f'<th dir="rtl">{x}</th>' for x in head)
    b = " ".join('<tr dir="rtl"> ' + " ".join(f'<td dir="rtl">{x}</td>' for x in r) + " </tr>" for r in rows)
    return f'<table dir="rtl"> <thead dir="rtl"> <tr dir="rtl"> {h} </tr> </thead> <tbody dir="rtl"> {b} </tbody> </table>'


# sanity: the page's own table style matches tbl()
_old = P.table_html('<th dir="rtl">טווח מחיר עבודה</th>')
assert _old.startswith('<table dir="rtl"> <thead dir="rtl"> <tr dir="rtl"> <th dir="rtl">') and _old.endswith("</tr> </tbody> </table>"), _old[-60:]

# ---------------- edits ----------------
# 1. lead: 'more than a million' spread inside one room count (tier 2)
old1 = P.find("אין להרצליה מחיר אחד:", "ואף ליותר ממיליון ש\"ח.")
new1 = old1.replace("ואף ליותר ממיליון ש\"ח.", "ואף יותר.")
e1 = P.edit(old1, new1, ["page"], "UNSOURCED",
            "A spread of more than a million shekels between two flats with the same room count, with no source or date; the number is "
            "dropped, the sentence stays. Tier 2.", tier=2)

# 2. 'by the data checked': 2-room range and the 6M premium ceiling
old2 = P.find("דירת 2 חדרים רגילה עשויה להופיע סביב", "ולעיתים הרבה מעבר לכך.")
new2 = ("דירת 3 חדרים עשויה להופיע סביב כ-2.5-3.1 מיליון ש\"ח, דירת 4 חדרים סביב כ-3.1-3.8 מיליון ש\"ח, ודירת 5 חדרים סביב "
        "כ-4.0-5.0 מיליון ש\"ח. בדירות חדשות, בדירות גדולות במיוחד, בפרויקטים מבוקשים, בקרבה לים או באזורים פרימיום כמו המרינה "
        "והרצליה פיתוח, המחיר יכול להיות גבוה בהרבה.")
e2 = P.edit(old2, new2, ["page"], "UNSOURCED",
            "The 2-room range 2.0-2.5M and the 'beyond 6M' premium ceiling have no named source and no date; dropped. The 3, 4 and 5-room "
            "ranges hold the official medians (2,793,600 / 3,272,800 / 4,251,200) and are kept word for word.")

# 3. 'the numbers agree with market indications': city average and new-flat figures
old3 = P.find("המספרים מתיישבים עם כמה אינדיקציות שוק שנבדקו:", "בהתאם לשטח, רחוב, גיל בניין ואזור.")
new3 = ("המספרים מתיישבים עם נתוני רשות המסים לרבעון הראשון של 2026: חציון מחיר העסקה היה 2,793,600 ש\"ח לדירת 3 חדרים, "
        "3,272,800 ש\"ח לדירת 4 חדרים ו-4,251,200 ש\"ח לדירת 5 חדרים, וחציון כלל העסקאות בעיר היה 3,202,200 ש\"ח. לעומת הרבעון "
        "הראשון של 2025, החציון לדירת 4 חדרים ירד ב-9.1% ולדירת 5 חדרים ב-8.9%, ולכן כדאי להשוות לעסקאות עדכניות, בהתאם לשטח, רחוב, "
        "גיל בניין ואזור.")
e3 = P.edit(old3, new3, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "rooms.all.latest", "rooms.4.change_pct", "rooms.5.change_pct"],
            "CONFLICT",
            "A city 'purchase average' of 4.0-4.24M vs the official all-deals median 3,202,200, and new 4-room flats at 3.49-3.55M vs the "
            "official 4-room median 3,272,800 (1-3.2026). The new 3 and 5-room figures and the 4-room deal range were consistent. Rewritten "
            "with the official medians and the year-on-year drop of the 4 and 5-room medians.")

# 4. per-m2 city average (tier 2)
old4 = "זו הסיבה שממוצע עירוני של כ-34,000-38,000 ש\"ח למ\"ר יכול לתת כיוון, אך אינו מחליף בדיקה של 5-10 עסקאות דומות לפי רחוב, שטח, קומה ומועד מכירה."
new4 = "זו הסיבה שממוצע עירוני למ\"ר יכול לתת כיוון, אך אינו מחליף בדיקה של 5-10 עסקאות דומות לפי רחוב, שטח, קומה ומועד מכירה."
e4 = P.edit(old4, new4, ["page"], "UNSOURCED", "City per-m2 average 34,000-38,000 with no source and no date (the page shows no check date); number dropped. Tier 2.", tier=2)

# 5. intro of the rooms table
old5 = P.find("הטבלה הבאה מרכזת טווחי עבודה לדירות בהרצליה לפי מספר חדרים.", "לא כנוסחת שווי אוטומטית.")
new5 = ("הטבלה הבאה מציגה את חציון מחיר העסקה בהרצליה לפי מספר חדרים, לפי נתוני רשות המסים לרבעון הראשון של 2026, לצד החציון "
        "באותו רבעון שנה קודם לכן. היא מיועדת לסינון ראשוני: להבין אם דירה מסוימת נמצאת באזור השוק, מתומחרת באגרסיביות, או מחייבת "
        "בדיקה עמוקה יותר של עסקאות דומות.")
e5 = P.edit(old5, new5, ["rooms.3.latest", "rooms.3.year_ago"], "WORDING",
            "The intro announced working ranges and a rent column; the table becomes the official medians (edit 6) and the undated rent column leaves.")

# 6. rooms table
new6 = tbl(["סוג דירה", "חציון מחיר העסקה, ינואר-מרץ 2026", "ינואר-מרץ 2025", "שינוי בשנה", "מה לבדוק לפני הסתמכות"], [
    ["3 חדרים", "2,793,600 ש\"ח", "2,776,600 ש\"ח", "עלייה של 0.6%",
     "האם מדובר בדירת זוג צעיר רגילה, דירה משופצת, דירה עם ממ\"ד, או דירה ישנה שדורשת שיפוץ של 150-300 אלף ש\"ח."],
    ["4 חדרים", "3,272,800 ש\"ח", "3,602,100 ש\"ח", "ירידה של 9.1%",
     "שטח של כ-85 מ\"ר לעומת כ-105 מ\"ר, מרפסת, חניה, מעלית, גיל הבניין, קרבה לבתי ספר ולתחבורה."],
    ["5 חדרים", "4,251,200 ש\"ח", "4,668,900 ש\"ח", "ירידה של 8.9%",
     "האם זו דירת משפחה רגילה או דירה חדשה, איכות הפרויקט, מספר חניות, מחסן, כיווני אוויר, מרפסת וגודל סלון."],
])
e6 = P.table('<th dir="rtl">טווח מחיר עבודה</th>', new6,
             ["rooms.3.latest", "rooms.3.year_ago", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.year_ago", "rooms.4.change_pct",
              "rooms.5.latest", "rooms.5.year_ago", "rooms.5.change_pct"], "UNSOURCED",
             "Rooms table of working ranges: the 3, 4 and 5-room ranges hold the official medians, but the 2-room and 6+-room rows and the "
             "whole rent column have no source and no date. Replaced by the official medians with the year-earlier quarter; the check notes of "
             "rows 3-5 are kept word for word. The same rents stay (as figures) only where tier 2 is not applied.")

# 7. sentence after the rooms table
old7 = "הטבלה מראה מדוע מספר חדרים לבדו אינו מספיק."
new7 = ("המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים ודירות 6 חדרים ומעלה כדאי לבדוק מול עסקאות דומות ברחוב "
        "ובשכונה. וגם בתוך אותו מספר חדרים, החציון לבדו אינו מספיק.")
e7 = P.edit(old7, new7, ["data_quarter"], "WORDING", "Follows edit 6: the 2-room and 6+-room rows left the table.")

# 8. neighbourhood table: the working-range column leaves (only the city centre has official medians; given in edit 9)
new8 = tbl(["אזור בהרצליה", "כיוון מחיר יחסי", "מה משנה את המחיר באזור"], [
    ["מרכז העיר", "בינוני עד גבוה", "קרבה למסחר, תחבורה, רעש, חניה, מעלית, מצב בניין ופוטנציאל התחדשות."],
    ["הרצליה הצעירה", "גבוה", "ביקוש משפחות, סביבת בתי ספר, חניה, מרפסת, ממ\"ד, רחוב שקט וגיל הבניין."],
    ["הרצליה ב' והירוקה", "גבוה עד גבוה מאוד", "סביבה ירוקה, איכות בנייה, דירות גדולות, קומה, מעלית, חניה כפולה ומחסן."],
    ["גליל ים", "גבוה", "פרמיית בנייה חדשה, תכנון שכונתי, מרפסת, ממ\"ד, חניה, ועד בית ואיכות הפרויקט."],
    ["נוה עמל ונוה אמירים", "בינוני עד גבוה", "שיפוץ, בניין ותיק מול חדש, נגישות, חניה, שטח רשום והאם קיימת היתכנות תכנונית."],
    ["נוף ים", "גבוה עד פרימיום", "קרבה לים, נדירות, נוף, גודל דירה, זכויות, חניה ורמת הבנייה."],
    ["המרינה", "פרימיום", "נוף לים או למרינה, קומה, מרפסת, חניה, שירותי בניין, דמי ניהול ונדירות עסקה."],
    ["הרצליה פיתוח", "פרימיום גבוה", "קרבה לים, מגרש, בנייה יוקרתית, רחוב, פרטיות, שטח, נוף, רמת גמר ותמהיל נכסים ייחודי."],
])
e8 = P.table('<th dir="rtl">טווח עבודה נפוץ לדירות רגילות</th>', new8, ["page"], "UNSOURCED",
             "Neighbourhood working ranges (8 rows) with no source and no date; the official file has a median only for the city centre "
             "(and Weizmann, not on the page). The range column leaves; the relative-price and what-changes-the-price columns are kept "
             "word for word; the official centre and Weizmann medians are given right after the table (edit 9).")

# 9. paragraph after the neighbourhood table: official neighbourhood medians
old9 = P.find("הטבלה אינה מחליפה בדיקה של עסקאות סגורות, אך היא מסבירה", "או מיקום פחות מבוקש בתוך אותה שכונה.")
new9 = ("לפי נתוני רשות המסים לרבעון הראשון של 2026, חציון מחיר העסקה במרכז העיר היה 2,928,500 ש\"ח לדירת 3 חדרים, 3,360,900 ש\"ח "
        "לדירת 4 חדרים ו-4,045,400 ש\"ח לדירת 5 חדרים, ובשכונת וייצמן 3,518,800 ש\"ח לדירת 4 חדרים. בשאר האזורים לא פורסם חציון "
        "לרבעון, ולכן משווים לעסקאות סגורות דומות ברחוב ובבניין. " + old9)
e9 = P.edit(old9, new9, ["neighbourhoods[מרכז העיר].rooms.3", "neighbourhoods[מרכז העיר].rooms.4", "neighbourhoods[מרכז העיר].rooms.5",
                         "neighbourhoods[וייצמן].rooms.4"], "UNSOURCED",
            "Follows edit 8: the unsourced neighbourhood ranges are replaced by the official neighbourhood medians where published (1-3.2026). "
            "The original sentence is kept after the new ones.")

# 10-11. rent paragraphs (tier 2: no date anywhere on the page)
old10 = ("אם דירת 3 חדרים מושכרת סביב כ-6,500-6,800 ש\"ח בחודש ודירת 4 חדרים סביב כ-7,500-8,500 ש\"ח בחודש, אפשר להשתמש בשכירות כדי "
         "לבדוק אם מחיר מכירה נראה סביר ביחס לביקוש למגורים באזור.")
new10 = "כאשר יודעים בכמה מושכרות דירות דומות באותו אזור, אפשר להשתמש בשכירות כדי לבדוק אם מחיר מכירה נראה סביר ביחס לביקוש למגורים באזור."
e10 = P.edit(old10, new10, ["page"], "UNSOURCED", "Rent levels for 3 and 4 rooms with no source and no date; rephrased without the numbers. Tier 2.", tier=2)
old11 = P.find("נתוני שכירות שנבדקו הצביעו על שכירות חציונית בהרצליה", "מדוע צריך לקרוא את השכירות לפי אזור ולא רק לפי עיר.")
new11 = ("בנתוני שכירות שנבדקו, הממוצע העירוני גבוה מהחציון, ודירות 5 חדרים ודירות באזורי יוקרה מושכרות בסכומים גבוהים בהרבה מדירות "
         "קטנות. הפער בין חציון, ממוצע ודירות יוקרה מסביר מדוע צריך לקרוא את השכירות לפי אזור ולא רק לפי עיר.")
e11 = P.edit(old11, new11, ["page"], "UNSOURCED",
             "Rent median, average and per-room rents from unnamed 'rent data' and 'other rent tables', undated; rephrased without the numbers, "
             "keeping what they showed (average above median, large and luxury flats far above small ones). Tier 2.", tier=2)

# 12. rent table (tier 2): the undated rent column leaves
new12 = tbl(["אזור או סוג דירה", "מה השכירות אומרת על מחיר הדירה", "בדיקה לפני הסתמכות"], [
    ["ממוצע עירוני בהרצליה", "נותן מדד כללי לביקוש, אך מושפע מדירות גדולות, אזורי פרימיום ודירות יוקרה.",
     "להשוות לחציון, לאזור ולמספר החדרים, ולא להסתמך על ממוצע יחיד."],
    ["חציון עירוני בהרצליה", "יכול לשקף טוב יותר את דירת השוק הרגילה לעומת ממוצע שמושפע מעסקאות יקרות.",
     "לבדוק האם הדירה דומה למדגם: שטח, קומה, ריהוט, מצב ושכונה."],
    ["2 חדרים", "מתאים לבדיקת דירות קטנות, שוכרים יחידים, זוגות צעירים ומשקיעים.",
     "לוודא שאין שטח קטן במיוחד, חוסר חניה, רעש או בניין בעייתי."],
    ["3 חדרים", "עוזר לבדוק אם המחיר המבוקש סביר ביחס לחציון מחיר העסקה לדירת 3 חדרים, 2,793,600 ש\"ח ברבעון הראשון של 2026, בכפוף לאזור ולמצב הדירה.",
     "להשוות לדירות דומות באותו אזור, לא לכל דירות 3 החדרים בעיר."],
    ["4 חדרים", "מתאים לשוק משפחות, ולכן המחיר מושפע גם מבתי ספר, מעלית, חניה, ממ\"ד ומרפסת.",
     "לבדוק אם השכירות משקפת דירה משופצת או דירה רגילה שדורשת השקעה."],
    ["5 חדרים", "פער רחב שמושפע מאוד מגודל, איכות פרויקט, קומה, חניות, מרפסת ואזור.",
     "להפריד בין דירת משפחה רגילה לבין דירה חדשה או דירה באזור פרימיום."],
    ["נוה ישראל", "שכירות נמוכה יחסית עשויה להצביע על רמת מחיר נמוכה יותר ביחס לאזורים מבוקשים יותר בעיר.",
     "לבדוק סוג דירות במדגם, גיל בניין, שטח ומצב תחזוקה."],
    ["הרצליה הצעירה", "משקף ביקוש חזק יחסית של משפחות ושוכרים המחפשים אזור מגורים מבוסס.",
     "להשוות רק לדירות באותו גודל וברמת בניין דומה."],
    ["נוף ים", "קרבה לים יכולה להעלות גם שכירות וגם מחיר מכירה, אך אינה זהה בכל רחוב.",
     "לבדוק מרחק אמיתי מהים, נוף, חניה, קומה ואיכות הבניין."],
    ["הרצליה ב'", "שכירות גבוהה יחסית יכולה לתמוך במחירי דירות גבוהים יותר, בעיקר בדירות משפחה איכותיות.",
     "לבדוק אם מדובר בדירה רגילה, דירה גדולה, דירת גן או נכס חריג."],
    ["המרינה", "שוק פרימיום עם השפעה של נוף, בניין, שירותים ודמי ניהול.",
     "להפריד בין דירות קטנות, דירות נופש, דירות מגורים ודירות יוקרה."],
    ["הרצליה פיתוח", "תת שוק יוקרתי שאינו מייצג את מחיר הדירה הרגילה בהרצליה.",
     "לא להשתמש בשכירות של האזור הזה להערכת דירה במרכז העיר, בנוה עמל או בגליל ים."],
])
e12 = P.table('<th dir="rtl">שכירות חודשית שנבדקה</th>', new12, ["rooms.3.latest"], "UNSOURCED",
              "Rent table (12 rows) with no source name and no date; the rent column leaves, the reading and check columns stay word for word "
              "except where they pointed at the removed figure. The 3-room row's sale range 2.5-3.1M (consistent) becomes the official "
              "3-room median. Tier 2.", tier=2)

# 13. per-m2 sentence before the deals table (tier 2)
old13 = "כאשר מופיע מחיר למ\"ר סביב כ-34,000-38,000 ש\"ח, צריך לשאול האם הוא מתאים לדירה הנבדקת או רק משקף ערבוב של אזורים וסוגי נכסים."
new13 = "כאשר מופיע מחיר למ\"ר עירוני, צריך לשאול האם הוא מתאים לדירה הנבדקת או רק משקף ערבוב של אזורים וסוגי נכסים."
e13 = P.edit(old13, new13, ["page"], "UNSOURCED", "Repeats the undated city per-m2 34,000-38,000; number dropped. Tier 2.", tier=2)

# 14. deals and data table
new14 = tbl(["דוגמה או נתון לבדיקה", "מספרים שנבדקו", "איך לקרוא את הנתון", "מה לא להסיק ממנו לבד"], [
    ["חציון מחיר העסקה בעיר", "3,202,200 ש\"ח, כלל העסקאות בינואר-מרץ 2026", "נותן תמונת גובה כללית של השוק בהרצליה.",
     "לא מחיר לדירה מסוימת; תמהיל החדרים והאזורים ברבעון משנה אותו."],
    ["דירת 3 חדרים", "2,793,600 ש\"ח, חציון מחיר העסקה ינואר-מרץ 2026", "נקודת ייחוס לבדיקת דירות קטנות ובינוניות, לפי אזור ומצב.",
     "לא כל דירת 3 חדרים בהרצליה קרובה לחציון, במיוחד ליד הים או בבנייה חדשה."],
    ["דירת 4 חדרים", "3,272,800 ש\"ח, חציון מחיר העסקה ינואר-מרץ 2026", "סביב החציון, שונות השטח, הקומה והבניין משפיעה מאוד.",
     "לא ניתן להשוות דירת 86 מ\"ר לדירת 109 מ\"ר רק לפי מספר חדרים."],
    ["דירת 5 חדרים", "4,251,200 ש\"ח, חציון מחיר העסקה ינואר-מרץ 2026", "מתאים לשוק משפחות, במיוחד בדירות עם ממ\"ד, חניה ומרפסת.",
     "לא מבדיל לבד בין דירה חדשה, דירת יד שנייה ודירת פרימיום."],
    ["עסקה לדוגמה ברחוב אחד העם", "4 חדרים, כ-109 מ\"ר, סביב כ-3.98 מיליון ש\"ח, תאריך 19.11.2025",
     "עסקה כזו יכולה לשמש עוגן אם הדירה הנבדקת דומה בשטח, ברחוב, בבניין ובמועד.",
     "לא נכון להחיל אותה על דירה קטנה יותר, אזור אחר או בניין שונה מהותית."],
    ["פער בין מחיר מבוקש למחיר סגירה", "יכול לנוע מעשרות אלפי ש\"ח ועד מאות אלפי ש\"ח",
     "הפער תלוי בתחרות, זמן על המדף, תמחור פתיחה, מצב הדירה וכוח המיקוח.", "לא כל מוכר יוריד מחיר, ולא כל מחיר מבוקש מנופח."],
])
e14 = P.table('<th dir="rtl">מספרים שנבדקו</th>', new14,
              ["rooms.all.latest", "rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
              "Deals table: the city 'purchase average' 4.0-4.24M (and 'not every 4-room flat is worth about 4M') conflicts with the official "
              "all-deals median 3,202,200; the per-m2 row and the four street examples (1.77M to 3.98M, no room count, no date) have no "
              "dated source. Rebuilt with the official city and 3/4/5-room medians (the 3/4/5 ranges were consistent, the 3-room top "
              "2.78M sits just under the median 2,793,600); the dated Ahad Ha'am deal and the asking-vs-closing row are kept word for word.")

# 15. FAQ per-m2 (tier 2)
old15 = "מחיר למ\"ר בהרצליה יכול לנוע סביב כ-34,000-38,000 ש\"ח למ\"ר כאינדיקציה עירונית רחבה, אבל אין להשתמש במספר הזה לבד."
new15 = "מחיר למ\"ר בהרצליה משתנה מאוד לפי אזור, גודל וסוג נכס, ולכן אין מספר עירוני אחד שאפשר להשתמש בו לבד."
e15 = P.edit(old15, new15, ["page"], "UNSOURCED", "FAQ per-m2: the undated 34,000-38,000 range; rephrased without the number. Tier 2.", tier=2)

# 16. FAQ rent (tier 2)
old16 = ("דירות 2 חדרים יכולות לנוע סביב כ-5,000-5,500 ש\"ח, דירות 3 חדרים סביב כ-6,500-6,800 ש\"ח, דירות 4 חדרים סביב "
         "כ-7,500-8,500 ש\"ח ודירות 5 חדרים סביב כ-9,000-12,200 ש\"ח.")
new16 = "דירות גדולות ודירות במצב טוב מושכרות בדרך כלל ביותר, ולכן משווים לחוזים של דירות דומות באותו אזור."
e16 = P.edit(old16, new16, ["page"], "UNSOURCED", "FAQ rent by rooms with no source and no date; rephrased without the numbers. Tier 2.", tier=2)

# ---------------- claims inventory ----------------
C = P.claim
C("p@4135", "כ-2.5-3.0 מיליון ש\"ח לדירת 3 חדרים רגילה", "sale", "CONSISTENT", "keep", rooms=3, official="2,793,600 (1-3.2026)", figures=2)
C("p@4135", "כ-3.1-3.8 מיליון ש\"ח לדירת 4 חדרים", "sale", "CONSISTENT", "keep", rooms=4, official="3,272,800 (1-3.2026)", figures=2)
C("p@4135", "וכ-4.0-5.0 מיליון ש\"ח לדירת 5 חדרים", "sale", "CONSISTENT", "keep", rooms=5, official="4,251,200 (1-3.2026)", figures=2)
C("p@4135", "הפער בין שתי דירות באותו מספר חדרים ... ליותר ממיליון ש\"ח", "other", "UNSOURCED", f"edit {e1}", note="tier 2; written as a word, no digits")
C("p@40348", "דירת 2 חדרים רגילה עשויה להופיע סביב כ-2.0-2.5 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e2}", rooms=2, figures=2)
C("p@40348", "דירת 3 חדרים סביב כ-2.5-3.1 מיליון ש\"ח", "sale", "CONSISTENT", f"keep (word for word inside edit {e2})", rooms=3, official="2,793,600", figures=2)
C("p@40348", "דירת 4 חדרים סביב כ-3.1-3.8 מיליון ש\"ח", "sale", "CONSISTENT", f"keep (word for word inside edit {e2})", rooms=4, official="3,272,800", figures=2)
C("p@40348", "ודירת 5 חדרים סביב כ-4.0-5.0 מיליון ש\"ח", "sale", "CONSISTENT", f"keep (word for word inside edit {e2})", rooms=5, official="4,251,200", figures=2)
C("p@40348", "באזורים פרימיום ... הטווח יכול לעבור גם 6 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e2}", rooms="premium")
C("p@40813", "עמודי מידע עירוניים הראו ממוצעי רכישה סביב כ-4.0-4.24 מיליון ש\"ח", "sale_avg", "CONFLICT", f"edit {e3}", rooms="all", official="all deals 3,202,200 (1-3.2026)", figures=2)
C("p@40813", "נתוני דירות חדשות: דירות 3 חדרים סביב כ-2.78 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e3}", rooms=3, official="2,793,600", note="new flats")
C("p@40813", "נתוני דירות חדשות: דירות 4 חדרים סביב כ-3.49-3.55 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e3}", rooms=4, official="3,272,800", figures=2, note="new flats")
C("p@40813", "נתוני דירות חדשות: דירות 5 חדרים סביב כ-3.95-4.45 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e3}", rooms=5, official="4,251,200", figures=2, note="new flats")
C("p@40813", "עמודי עסקאות נקודתיים: דירות 4 חדרים סביב כ-3.05-3.98 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e3}", rooms=4, official="3,272,800", figures=2)
C("p@41665", "הערת שימוש: טווח של 3.2-3.6 מיליון ש\"ח לדירת 4 חדרים יכול להיות סביר בשכונה אחת", "sale", "CONSISTENT", "keep", rooms=4, official="3,272,800", figures=2)
C("p@41990", "ממוצע עירוני של כ-34,000-38,000 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"edit {e4}", figures=2, note="tier 2; no date on the page")
C("tr@43392", "2 חדרים | כ-2.0-2.5 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e6}", rooms=2, figures=2)
C("tr@43625", "3 חדרים | כ-2.5-3.1 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e6}", rooms=3, official="2,793,600", figures=2, note="restated as the median")
C("tr@43874", "4 חדרים | כ-3.1-3.8 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e6}", rooms=4, official="3,272,800", figures=2, note="restated as the median")
C("tr@44107", "5 חדרים | כ-4.0-5.0 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e6}", rooms=5, official="4,251,200", figures=2, note="restated as the median")
C("tr@44355", "6 חדרים ומעלה | כ-5.5-8.0 מיליון ש\"ח ומעלה", "sale", "UNSOURCED", f"edit {e6}", rooms=6, figures=2)
C("tr@43392..44355", "עמודת שכירות חודשית אופיינית (5 שורות)", "rent", "UNSOURCED", f"edit {e6}", figures=9, note="no date; the column leaves with the rebuilt table")
C("tr@47163", "מרכז העיר | כ-2.5-3.7 מיליון ש\"ח לדירות 3-4 חדרים", "sale_nb", "CONSISTENT", f"edit {e8}", rooms="3-4", official="centre 3=2,928,500 4=3,360,900", figures=2, note="official centre medians given in edit 9")
C("tr@47404..48846", "טווחי עבודה לפי אזור: הרצליה הצעירה עד הרצליה פיתוח (7 שורות)", "sale_nb", "UNSOURCED", f"edit {e8}", figures=13, note="no official median for these areas")
C("p@50463", "אם דירת 3 חדרים מושכרת סביב כ-6,500-6,800 ... 4 חדרים כ-7,500-8,500", "rent", "UNSOURCED", f"edit {e10}", figures=4, note="tier 2; asserts the rent level")
C("p@50875", "שכירות חציונית כ-7,200, ממוצע כ-7,661, 3 חדרים כ-6,686; 2-5 חדרים 5,500-12,200", "rent", "UNSOURCED", f"edit {e11}", figures=7, note="tier 2")
C("tr@51501..54269", "טבלת שכירות חודשית שנבדקה (12 שורות)", "rent", "UNSOURCED", f"edit {e12}", figures=19, note="tier 2")
C("tr@52280", "3 חדרים | שכירות כזו יכולה לתמוך במחיר סביב כ-2.5-3.1 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e12}", rooms=3, official="2,793,600", figures=2, note="restated as the median inside the tier-2 rent table")
C("p@55574", "כאשר מופיע מחיר למ\"ר סביב כ-34,000-38,000 ש\"ח", "per_m2", "UNSOURCED", f"edit {e13}", figures=2, note="tier 2")
C("tr@56188", "ממוצע רכישה עירוני | כ-4.0-4.24 מיליון ש\"ח | ... סביב 4 מיליון ש\"ח", "sale_avg", "CONFLICT", f"edit {e14}", rooms="all", official="all deals 3,202,200", figures=3)
C("tr@56414", "מחיר למ\"ר עירוני | כ-34,000-38,000 ש\"ח למ\"ר", "per_m2", "UNSOURCED", f"edit {e14}", figures=2)
C("tr@56668", "דירת 3 חדרים | כ-2.52-2.78 מיליון ש\"ח בחלק מהנתונים", "sale", "CONSISTENT", f"edit {e14}", rooms=3, official="2,793,600", figures=2, note="edge: median 0.5% above the top; restated as the median")
C("tr@56947", "דירת 4 חדרים | כ-3.05-3.98 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e14}", rooms=4, official="3,272,800", figures=2, note="restated as the median")
C("tr@57218", "דירת 5 חדרים | כ-3.95-4.45 מיליון ש\"ח, עם חריגים מעל 5 מיליון", "sale", "CONSISTENT", f"edit {e14}", rooms=5, official="4,251,200", figures=3, note="restated as the median")
C("tr@57505", "עסקה ברחוב אחד העם | 4 חדרים, כ-109 מ\"ר, כ-3.98 מיליון ש\"ח, 19.11.2025", "deal", "UNSOURCED", f"keep (one dated deal; row kept word for word in edit {e14})", rooms=4, official="city 4 rooms 3,272,800")
C("tr@57832", "דוגמאות רחוב: כ-1.77, 2.78, 3.60 ו-3.98 מיליון ש\"ח", "sale_street", "UNSOURCED", f"edit {e14}", figures=4, note="no room count, no date")
C("p@68746", "FAQ: דירת 3 חדרים סביב כ-2.5-3.1 מיליון ש\"ח", "sale", "CONSISTENT", "keep (same range as the body, p@40348)", rooms=3, official="2,793,600", figures=2)
C("p@69092", "FAQ: דירת 4 חדרים סביב כ-3.1-3.8 מיליון ש\"ח", "sale", "CONSISTENT", "keep (same range as the body)", rooms=4, official="3,272,800", figures=2)
C("p@69458", "FAQ: דירת 5 חדרים סביב כ-4.0-5.0 מיליון ש\"ח", "sale", "CONSISTENT", "keep (same range as the body)", rooms=5, official="4,251,200", figures=2)
C("p@69809", "FAQ: מחיר למ\"ר סביב כ-34,000-38,000 ש\"ח", "per_m2", "UNSOURCED", f"edit {e15}", figures=2, note="tier 2")
C("p@70648", "FAQ שכירות: 2 חדרים 5,000-5,500 ... 5 חדרים 9,000-12,200", "rent", "UNSOURCED", f"edit {e16}", figures=8, note="tier 2")

P.write(notes=(
    "The page shows no check date anywhere (only the Ahad Ha'am deal is dated, 19.11.2025), so no undated rent or per-m2 figure qualifies "
    "for keep: they are rephrased without numbers in tier 2. Applying tier 1 alone still leaves those rent and per-m2 figures in place. "
    "Not audited as claims (illustrations, not market statements): the 3.95M asking / 3.75M closing example (p@42385), the 2.55M 3-room "
    "and 4.4M 5-room if-examples (p@44663), the 150-300 thousand renovation cost in the rooms-table note, the 8,000 rent / 3.8M example "
    "(p@54532), the 200,000-400,000 gap (p@59544), the 3.8M / 3.45M / 350,000 / 250,000 new-vs-second-hand example (p@62227), 'פי 2' "
    "(p@63813), sizes in m2, counts of deals and months. Remaining SUSPECTs are those hypotheticals (p@42385, p@44663, p@62227) and the "
    "individual dated Ahad Ha'am deal (3.98M, 19.11.2025). "
    "The lead (above the price list), the 'by the data checked' paragraph and the 3/4/5-room FAQ answers keep their working ranges: each holds "
    "the official median (3: 2.5-3.0/3.1M vs 2,793,600; 4: 3.1-3.8M vs 3,272,800; 5: 4.0-5.0M vs 4,251,200). "
    "Official quirk: the 4 and 5-room medians fell 9.1% and 8.9% year on year; the 4-room series has no 10-12.2025 value and the 5-room "
    "median dropped from 4,730,400 (10-12.2025) to 4,251,200. Official neighbourhoods: only 'מרכז העיר' (3/4/5) and 'וייצמן' (4 rooms); "
    "'וייצמן' is not one of the page's areas and was not mapped to 'הרצליה הצעירה' or any other row; it appears only in the sentence after "
    "the neighbourhood table."))
