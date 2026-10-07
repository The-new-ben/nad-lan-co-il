# -*- coding: utf-8 -*-
"""Tier 3, Kiryat Ono (page 4560). No CBS row (Kiryat Ono is not in the CBS big-city list), so every listing-site rent is removed or deleted.
The page writes ש"ח and ASCII quotes."""
from b3lib import *

NOCBS = "The CBS table 4.9 has no Kiryat Ono row (not in the big-city list) and no house rents"


def build(P):
    # --- 'useful rent range' under its own heading
    old = P.sub('מחירי שכירות בקריית אונו נעים לרוב סביב 5,800-8,200 ש"ח בדירות 3-5 חדרים,', 'ל-11,900-14,000 ש"ח בחודש.')
    new = 'השכירות בקריית אונו משתנה בין דירה ותיקה ללא חניה לבין דירה חדשה יותר עם ממ"ד, מעלית וחניה.'
    P.edit(old, new, "B", 'removed the rent range 5,800-8,200 for 3-5 rooms and the 11,900-14,000 for a house or very large flat; the paragraph under the heading keeps the contrast between an old flat without parking and a newer one with a safe room, lift and parking',
           f"The paragraph is the only text under its own heading ('a useful rent range'), so it is rewritten rather than deleted. {NOCBS}; both ranges go. The contrast between an old flat without parking and a newer one with safe room, lift and parking is hedged advice and stays.")

    # --- fact table: average rent
    def facts(old):
        h, rows = parse_table(old)
        return rebuild(old, None, [r for r in rows if r[0].strip() != "שכירות ממוצעת כללית"])
    P.table('<th dir="rtl">טווח או נתון שנבדק</th>', facts, "C",
            'deleted the row "general average rent 7,600-7,900" from the fact table; the other rows are untouched',
            f"Fact table row 'general average rent 7,600-7,900 a month, suits understanding demand, not replacing a check of rental contracts'. {NOCBS}; the whole row goes.")
    # --- illustrative rent
    old = P.sub('משפחה שמוכנה לשלם 7,500 ש"ח בחודש עבור דירת 4 חדרים טובה מצביעה')
    P.edit(old, 'משפחה שמוכנה לשלם שכר דירה גבוה עבור דירת 4 חדרים טובה מצביעה', "B", 'removed the illustrative rent 7,500',
           f"An illustrative rent (7,500 for a good 4-room flat) at the level of the listing data on the page. {NOCBS}; the number goes and the point (a family willing to pay a high rent signals demand for the neighbourhood, schools, access and lifestyle) stays.")

    # --- the sentence that introduces the sale-median table names the rent column that is about to go
    old = P.sub(', לצד השכירות החודשית הנפוצה לפי בדיקת שוק גלויה. הטבלה אינה מחליפה')
    P.edit(old, '. הטבלה אינה מחליפה', "B", 'removed "alongside the common monthly rent from a visible market check" from the sentence that introduces the sale-median table (the rent column is deleted in the next edit)',
           f"The sentence announcing the table said it shows the median, the yearly change 'alongside the common monthly rent'. {NOCBS}; the rent column goes (next edit), so the announcement loses that clause.")

    # --- sale medians with a rent column
    def sale_rent(old):
        h, rows = parse_table(old)
        return rebuild(old, [h[0], h[1], h[2], h[4]], [[r[0], r[1], r[2], r[4]] for r in rows])
    P.table('<th dir="rtl">שכירות חודשית נפוצה</th>', sale_rent, "C",
            'deleted the "common monthly rent" column (3 rooms 5,800-6,600; 4 rooms 7,300-7,500; 5 rooms 7,900-8,200) from the sale-median table; median, yearly change and check note stay',
            f"Rent column of the sale-median table (private market pages). {NOCBS}; the column goes, the Tax Authority medians, the yearly change and the check notes stay word for word.")
    # --- rent by rooms table
    P.table('<th dir="rtl">שכירות חודשית לפי בדיקת שוק</th>', lambda old: "", "C",
            'deleted the rent-by-rooms table (1-2 rooms 3,700-4,300; 3: 5,800-6,600; 4: 7,300-7,500; 5: 7,900-8,200; 6: 8,700+; house 11,900-14,000) with its "relation to the sale price" column: private market pages, no official counterpart',
            f"A whole table of private rent ranges by rooms. {NOCBS}. Its last column ('can support a price of about 2.4-2.9 million', 'helps check flats around 3.1-3.5 million') is a price band read off those rents and has no content without them; the 'what affects the rent' column is a hedged remark that goes with the table.")
    # --- FAQ
    old = P.sub(' השכירות הנפוצה לדירות כאלה נעה סביב 5,800-6,600 ש"ח בחודש, לפי אזור ומצב הדירה.')
    P.edit(old, '', "C", 'deleted the FAQ sentence with the common rent 5,800-6,600 for such 3-room flats',
           f"FAQ 'what does a 3-room flat in Kiryat Ono cost': the sentence only gave the private rent range. {NOCBS}; the answer keeps the sale ranges (as tier 1 left them).")
