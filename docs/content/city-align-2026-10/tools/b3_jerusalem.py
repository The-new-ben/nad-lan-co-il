# -*- coding: utf-8 -*-
"""Tier 3, Jerusalem (page 4575). CBS row: ירושלים (table 4.9, Q2 2026). The page writes ש"ח and ASCII quotes."""
from b3lib import *

CITY = "ירושלים"
CUR = 'ש"ח'
LMS = 'הלמ"ס'
Q2S = Q2.replace(" (אפריל עד יוני)", "")


def build(P):
    sizes = by_size(CITY, CUR)
    KEYS = keys_all(CITY)
    # --- lead: family-flat rent range
    old = P.sub('בדיקות שכירות רבות מציבות דירות משפחתיות או מרכזיות נפוצות סביב 5,500-8,500 ש"ח לחודש, ולפעמים יותר בדירות יוקרה, דירות גדולות או בניינים חדשים.')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בירושלים {Q2} היה {c(CITY, "3.5-4")} {CUR} לדירות של 3.5 עד 4 חדרים '
           f'ו-{c(CITY, "4.5+")} {CUR} לדירות של 4.5 חדרים ומעלה.')
    P.edit(old, new, "A", 'replaced the listing-site family-flat rent range 5,500-8,500 (and "more in luxury, large or new flats") with the CBS Jerusalem averages for 3.5-4 and 4.5+ rooms, Q2 2026: 6,180 / 7,748 ש"ח',
           "Lead: 'family or central flats usually rent around 5,500-8,500' (listing checks) replaced by the CBS average monthly rent in Jerusalem for 3.5-4 rooms (6,179.6) and 4.5+ rooms (7,748.2), Q2 2026; the 4.5+ group already includes the large flats the old clause pointed at.",
           [key(CITY, "3.5-4"), key(CITY, "4.5+")], url=RENT_URL)
    # --- rent and price per m2 paragraph
    old = P.sub(' ושכירות מבוקשת ממוצעת סביב 7,100 ש"ח. בדיקות שכירות אזוריות הראו פערים של אלפי שקלים בין שכונות, ולכן יש לבדוק')
    new = (f'. לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בירושלים {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות. '
           'השכירות משתנה בין שכונות, ולכן יש לבדוק')
    P.edit(old, new, "A", 'replaced the asking-rent average 7,100 with the CBS Jerusalem average 5,347 ש"ח (Q2 2026); "gaps of thousands between neighbourhoods" became "rent varies between neighbourhoods"',
           "Rent and price per m2: the asking rent 7,100 (market indices) replaced by the CBS average monthly rent in Jerusalem (5,347.4), Q2 2026. The per-m2 price 39,700 is not a rent figure and stays (tier 1 left it). 'Gaps of thousands of shekels between neighbourhoods' had no official figure behind it; it becomes the hedged 'rent varies between neighbourhoods'.",
           [key(CITY)], url=RENT_URL)

    # --- market snapshot table: rent rows
    def snapshot(old):
        h, rows = parse_table(old)
        out = []
        for r in rows:
            lab = r[0].strip()
            if lab == "שכירות מבוקשת ממוצעת בדפי שוק":
                out.append([f'שכר דירה חודשי ממוצע בירושלים, אפריל עד יוני 2026 ({LMS})', f'{c(CITY)} {CUR} לחודש', r[2]])
            elif lab == "מדד שכירות חציוני שפורסם במאי 2026":
                continue
            else:
                out.append(r)
        return rebuild(old, None, out)
    P.table('<th dir="rtl">ערך עבודה</th>', snapshot, "A",
            'in the market-snapshot table replaced the asking-rent average 7,100 with the CBS Jerusalem average 5,347 ש"ח (Q2 2026) and deleted the ad-site median row 6,200 (361 ads); the other rows are untouched',
            "Snapshot table: the row 'asking rent average 7,100' becomes the CBS average monthly rent in Jerusalem (5,347.4), Q2 2026; the row 'median rent published in May 2026, 6,200 on 361 ads' is deleted (the CBS publishes no median rent). The rows on population, official sale median, price per m2 and the number of rent listings are not rent figures and stay word for word.",
            [key(CITY)], url=RENT_URL)
    # --- rent section paragraph
    old = P.sub('לפי דפי שכירות שנבדקו, חציון שכירות סביב מאי 2026 עמד על כ-6,200 ש"ח', 'יש להשוות אותם לחוזים בפועל כאשר ניתן.')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בירושלים {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}. '
           'השכירות בפועל משתנה לפי השכונה והדירה, ולכן יש להשוות אותה לחוזים בפועל כאשר ניתן.')
    P.edit(old, new, "A", 'replaced the ad-site median 6,200 (361 ads, May 2026) and the average 7,100 with the CBS Jerusalem averages for all flats and by size group, Q2 2026',
           "Rent section: ad-site median (6,200 on 361 ads) and wider-market average (7,100) replaced by the CBS average monthly rent in Jerusalem for all flats (5,347.4) and by size group, Q2 2026. 'These are ad data, so compare to actual contracts' becomes 'rent varies by neighbourhood and flat, so compare to actual contracts'.",
           KEYS, url=RENT_URL)

    # --- neighbourhood rent table: rent column out, rent-level readings out
    def hoods(old):
        h, rows = parse_table(old)
        out = []
        for r in rows:
            lab = r[0].strip()
            if lab == "רוממה":
                continue  # its only note is about the rent sample
            note = r[2]
            if lab == "קטמון הישנה":
                note = "יש לבדוק ביקוש למיקום, אופי בנייה ונדירות."
            out.append([r[0], note])
        return rebuild(old, [h[0], h[2]], out)
    P.table('<th dir="rtl">דמי שכירות חודשיים שהופיעו בבדיקות שוק</th>', hoods, "C",
            'deleted the neighbourhood rent column (12 values 5,684-12,714 ש"ח) and the Romema row, whose note was only about the rent sample; the Old Katamon note "higher rent can reflect..." became a check; the other notes stay',
            "Neighbourhood rents from ad pages have no official counterpart (the CBS has no neighbourhood rent). The rent column goes. Romema ('the sample may be affected by large or new flats') only commented on the rent sample and has no content without it. Old Katamon's note ('higher rent can reflect demand for location, building character and rarity') was a level claim; it becomes the check 'verify demand for location, building character and rarity'. The other eleven notes are advice or hedged and stay word for word.")
