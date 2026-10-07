# -*- coding: utf-8 -*-
"""Tier 3, Rishon LeZion (page 4581). CBS row: ראשון לציון (table 4.9, Q2 2026). The page writes ש"ח and ASCII quotes."""
from b3lib import *

CITY = "ראשון לציון"
CUR = 'ש"ח'
LMS = 'הלמ"ס'
Q2S = Q2.replace(" (אפריל עד יוני)", "")


def build(P):
    sizes = by_size(CITY, CUR)
    KEYS = keys_all(CITY)
    # --- lead
    old = P.sub('חציון שכירות סביב 5,000 ש"ח לחודש, ממוצעים סביב 5,787 עד 6,131 ש"ח לפי מדגם ושיטת חישוב,', 'קרובות יותר לצירי ביקוש.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בראשון לציון {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}.'
    P.edit(old, new, "A", 'replaced the lead rents (median 5,000; averages 5,787-6,131 the CEO flagged; higher in western neighbourhoods) with the CBS Rishon LeZion averages for all flats (5,273) and by size group, Q2 2026',
           "Lead: 'median rent about 5,000, averages 5,787 to 6,131 by sample and method, higher in western, new or demand-axis neighbourhoods' replaced by the CBS average monthly rent in Rishon LeZion for all flats (5,272.9, against the listing averages 5,787-6,131) and by size group (3,732.3; 4,701.8; 5,554.7; 7,497.7), Q2 2026. The western-neighbourhood clause was a neighbourhood level claim without an official figure and goes.",
           KEYS, url=RENT_URL)
    # --- body
    old = P.sub('בראשון לציון חציון שכירות סביב 5,000 ש"ח בחלק מהמדגמים,', 'שמעלות את הממוצע.')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בראשון לציון {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות ו-{c(CITY, "4.5+")} {CUR} לדירות של 4.5 חדרים ומעלה, '
           'ומכאן שדירות גדולות מעלות את הממוצע.')
    P.edit(old, new, "A", 'replaced the median 5,000, the averages 5,787-6,131 and the remark on large/western/new flats with the CBS Rishon LeZion averages 5,273 (all flats) and 7,498 (4.5+ rooms), Q2 2026',
           "Body: median/average gap (5,000 against 5,787-6,131) and its explanation replaced by the CBS average for all flats (5,272.9) and for 4.5+ rooms (7,497.7), Q2 2026; the explanation 'large flats lift the average' now stands on the two official figures. 'Western neighbourhoods and new flats' (no figure) goes.",
           [key(CITY), key(CITY, "4.5+")], url=RENT_URL)

    # --- neighbourhood rent table
    over = {"נווה דקלים": "לא להסיק מנתון בודד", "נרקיסים": "לבדוק גודל דירה ושלב אכלוס"}

    def hoods(old):
        h, rows = parse_table(old)
        return rebuild(old, [h[0], h[3]], [[r[0], over.get(r[0].strip(), r[3])] for r in rows])
    P.table('<th dir="rtl">שכירות חודשית לדוגמה</th>', hoods, "C",
            'deleted the neighbourhood rent column (16 values 3,900-8,950 ש"ח) and the "what the number may hint" column (premium, moderate, relatively high...); the caution column stays, two cautions that pointed at a rent sample were reworded',
            "Neighbourhood example rents have no official counterpart (the CBS has no neighbourhood rent). The rent column goes, and so does the column that read each number ('premium for the west', 'moderate rent', 'relatively high rent'): without the number every cell of it is a rent-level claim without an official figure. The caution column (what to check) stays word for word except two cells that pointed at a rent sample: Neve Dekalim 'do not conclude from one rent alone' -> 'do not conclude from a single figure', Narkissim 'check a recent sample and flat size' -> 'check flat size and occupancy stage'.")
    # --- hypothetical rents 8,000 / 4,500
    old = P.sub('דירה שמושכרת ב-8,000 ש"ח אך נמכרת במחיר המשקף פרמיה חריגה', 'דירה שמושכרת ב-4,500 ש"ח אך נמכרת במחיר נמוך יחסית')
    new = ('דירה שמושכרת בשכר גבוה אך נמכרת במחיר המשקף פרמיה חריגה עדיין דורשת בדיקת עסקאות סגורות. לעומת זאת, '
           'דירה שמושכרת בשכר נמוך אך נמכרת במחיר נמוך יחסית')
    P.edit(old, new, "B", 'removed the two illustrative rents 8,000 and 4,500; the two cases are stated in words',
           "Two invented comparison rents (8,000 'high', 4,500 'low') that sit inside the listing-site range on the page; the CBS has no single counterpart (the flat's size is not given). The numbers go, the logic (a high rent with a premium price still needs closed-deal checks; a low rent with a low price can suit a renovator) stays.")

    # --- worked example step 4
    def steps(old):
        h, rows = parse_table(old)
        out = []
        for r in rows:
            if r[1].strip() == "בדיקת שכירות":
                r = [r[0], r[1], f'שכירות צפויה {c(CITY, "3.5-4")} {CUR}, הממוצע של {LMS} לדירות של 3.5 עד 4 חדרים באפריל עד יוני 2026', r[3]]
            out.append(r)
        return rebuild(old, None, out)
    P.table('<th dir="rtl">דוגמה מספרית</th>', steps, "A",
            'in the worked-example table replaced the expected rent 5,600-6,300 for the 4-room flat with the CBS Rishon LeZion average for 3.5-4 rooms (5,555 ש"ח, Q2 2026); the other steps are untouched',
            "Step 4 of the worked example (4-room flat, 98 m2): 'expected rent 5,600 to 6,300' replaced by the CBS average monthly rent for 3.5-4 rooms in Rishon LeZion (5,554.7), Q2 2026. The other steps (deals range, active listings, renovation and transaction costs, first offer) are not rent figures and stay.",
            [key(CITY, "3.5-4")], url=RENT_URL)
    # --- FAQ
    old = P.sub('חציון שכירות יכול להיות סביב 5,000 ש"ח לחודש, וממוצעים שונים נעים סביב 5,787 עד 6,131 ש"ח לפי מדגם ושיטת חישוב.', 'לכ-7,000 עד 9,000 ש"ח.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בראשון לציון {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}.'
    P.edit(old, new, "A", 'replaced the FAQ rents (median 5,000; averages 5,787-6,131; 7,000-9,000 in western or large flats) with the CBS Rishon LeZion averages for all flats and by size group, Q2 2026',
           "FAQ 'how much rent in Rishon LeZion': sample median and averages and the 7,000-9,000 'western or large and new flats' range replaced by the CBS averages for all flats (5,272.9) and by size group, Q2 2026.",
           KEYS, url=RENT_URL)
