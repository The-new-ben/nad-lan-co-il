# -*- coding: utf-8 -*-
"""Tier 3, Petah Tikva (page 4573). CBS row: פתח תקוה (table 4.9, Q2 2026). The page writes ש"ח and ASCII quotes."""
from b3lib import *

CITY = "פתח תקוה"
CUR = 'ש"ח'
LMS = 'הלמ"ס'
Q2S = Q2.replace(" (אפריל עד יוני)", "")


def build(P):
    sizes = by_size(CITY, CUR)
    KEYS = keys_all(CITY)
    fam = (f'{c(CITY, "3.5-4")} {CUR} לדירות של 3.5 עד 4 חדרים ו-{c(CITY, "4.5+")} {CUR} לדירות של 4.5 חדרים ומעלה')
    # --- lead
    old = P.sub('בדיקת שכירות סביב 5,000-8,000 ש"ח בחלק גדול מהשכונות עוזרת לבחון היגיון כלכלי בסיסי, אבל')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בפתח תקווה {Q2} היה {c(CITY)} {CUR}, ובדיקת שכירות עוזרת לבחון היגיון כלכלי בסיסי, אבל'
    P.edit(old, new, "A", 'replaced the rent range 5,000-8,000 "in most neighbourhoods" with the CBS Petah Tikva average 5,138 ש"ח (Q2 2026)',
           "Lead: 'a rent check around 5,000-8,000 in a large part of the neighbourhoods' replaced by the CBS average monthly rent in Petah Tikva (5,138.4), Q2 2026; the clause that a rent check helps basic economic sense but does not replace comparable closed deals is unchanged.",
           [key(CITY)], url=RENT_URL)
    # --- section 'rent and m2 as a sense check': neighbourhood example rents
    old = P.sub('בדפי שוק שנבדקו נראו דמי שכירות ממוצעים לדוגמא סביב 4,383 ש"ח בעמישב,', 'אלו מספרי הקשר, לא שומה.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בפתח תקווה {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}. אלו מספרי הקשר, לא שומה.'
    P.edit(old, new, "A", 'replaced the five neighbourhood example rents (Amishav 4,383; centre 5,098; Kfar Ganim A 6,681; Em HaMoshavot 8,209; Neve Gan 9,875) with the CBS Petah Tikva averages for all flats and by size group, Q2 2026',
           "Neighbourhood example rents from market pages have no official counterpart (the CBS has no neighbourhood rent). The paragraph sits under its own heading, so it is replaced rather than deleted: the CBS average monthly rent in Petah Tikva for all flats (5,138.4) and by size group, Q2 2026. 'These are context numbers, not a valuation' stays.",
           KEYS, url=RENT_URL)

    # --- quick-facts table: family-flat rent row
    def quick(old):
        h, rows = parse_table(old)
        out = []
        for r in rows:
            if r[0].strip() == "שכירות בדירות משפחתיות":
                out.append([f'שכר דירה חודשי ממוצע בדירות משפחתיות, אפריל עד יוני 2026 ({LMS})', fam, r[2]])
            else:
                out.append(r)
        return rebuild(old, None, out)
    P.table('<th dir="rtl">טווח או נתון עבודה</th>', quick, "A",
            'in the quick-facts table replaced the family-flat rent range 5,500-8,700 with the CBS Petah Tikva averages for 3.5-4 and 4.5+ rooms (5,311 / 7,099 ש"ח, Q2 2026); the other rows are untouched',
            "Quick-facts table: the row 'rent in family flats, about 5,500-8,700 in a large part of the neighbourhoods' becomes the CBS average monthly rent in Petah Tikva for 3.5-4 rooms (5,311.1) and 4.5+ rooms (7,099.0), Q2 2026; the usage note stays; all other rows are untouched.",
            [key(CITY, "3.5-4"), key(CITY, "4.5+")], url=RENT_URL)
    # --- sample sizes of the rent pages
    old = P.sub(' בדפי שכירות שנבדקו נראו 184-233 מודעות פעילות במדגמים שונים, ולכן כדאי להתייחס למספרים כמדד שוק משתנה.')
    P.edit(old, '', "C", 'deleted the sentence on the 184-233 active rent ads in the samples (the neighbourhood rents it qualified are gone)',
           "The sentence gives the size of the listing samples behind the neighbourhood rents and tells the reader to treat those numbers as a changing market measure. With the neighbourhood rents removed it has no object; deleted.")

    # --- neighbourhood rent table
    notes = {"המרכז השקט": "יש לבדוק רחוב שקט, נגישות ומצב דירה",
             "נווה גן": "דורש השוואה לנכסים גדולים ומאובזרים",
             "עמישב": "יש לבדוק רמת ביקוש ומלאי",
             "אחדות": "מתאים לבדיקת דירות ותיקות"}

    def hoods(old):
        h, rows = parse_table(old)
        return rebuild(old, [h[0], h[2]], [[r[0], notes.get(r[0].strip(), r[2])] for r in rows])
    P.table('<th dir="rtl">שכירות חודשית לדוגמה</th>', hoods, "C",
            'deleted the neighbourhood rent column (15 values 4,383-9,875 ש"ח); four notes that read a rent level into the area ("premium", "relatively high rent", "lower rent reflects demand", "more accessible price") became checks; the other eleven notes stay',
            "Neighbourhood example rents from market pages have no official counterpart. The rent column goes. Four notes depended on the rent level and are rewritten as checks without a level claim: HaMerkaz HaShaket ('premium for a quiet street...' -> check street, access, condition), Neve Gan ('relatively high rent requires comparison...' -> requires comparison...), Amishav ('lower rent also reflects demand and stock' -> check demand and stock), Achdut ('...at a more accessible price' -> '...'). The other eleven notes are advice and stay word for word.")
    # --- Em HaMoshavot FAQ
    old = P.sub('בבדיקות שכירות נראתה דוגמה סביב 8,209 ש"ח לחודש, נתון שמחזק את הצורך להשוות לדירות דומות באותו אזור.')
    P.edit(old, 'כדאי להשוות לדירות דומות באותו אזור.', "B", 'removed the Em HaMoshavot example rent 8,209; the advice to compare with similar flats in the same area stays',
           "FAQ: a neighbourhood example rent (8,209) with no official counterpart is removed; the advice it supported stays on its own.")
