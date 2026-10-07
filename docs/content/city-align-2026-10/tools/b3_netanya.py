# -*- coding: utf-8 -*-
"""Tier 3, Netanya (page 4577). CBS row: נתניה (table 4.9, Q2 2026). The page writes ש"ח and ASCII quotes."""
from b3lib import *

CITY = "נתניה"
CUR = 'ש"ח'
LMS = 'הלמ"ס'
Q2S = Q2.replace(" (אפריל עד יוני)", "")


def build(P):
    sizes = by_size(CITY, CUR)
    KEYS = keys_all(CITY)
    G4 = ("1-2", "2.5-3", "3.5-4", "4.5+")
    fam = (f'{c(CITY, "3.5-4")} {CUR} לדירות של 3.5 עד 4 חדרים ו-{c(CITY, "4.5+")} {CUR} לדירות של 4.5 חדרים ומעלה')
    # --- lead
    old = P.sub('בבדיקות שכירות, דירות משפחתיות נפוצות נעות פעמים רבות סביב 5,000 עד 8,000 ש"ח לחודש, אך גם כאן יש פערים חדים לפי גודל,')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בנתניה {Q2} היה {fam}, ובפועל השכירות משתנה לפי גודל,'
    P.edit(old, new, "A", 'replaced the family-flat rent range 5,000-8,000 with the CBS Netanya averages for 3.5-4 and 4.5+ rooms, Q2 2026: 5,273 / 6,695 ש"ח; "sharp gaps" became "rent varies"',
           "Lead: 'family flats usually rent around 5,000 to 8,000' (rental checks) replaced by the CBS average monthly rent in Netanya for 3.5-4 rooms (5,272.9) and 4.5+ rooms (6,695.1), Q2 2026. 'Sharp gaps by size, coastline, parking...' was a level claim without a figure; it becomes the hedged 'in practice rent varies by size, coastline, parking...' (the rest of the sentence is unchanged).",
           [key(CITY, "3.5-4"), key(CITY, "4.5+")], url=RENT_URL)
    # --- price per m2 section
    old = P.sub('שכירות של דירות משפחתיות נבדקת לעיתים סביב 5,000 עד 8,000 ש"ח לחודש. השכירות מסייעת')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בנתניה {Q2} היה {fam}. השכירות מסייעת'
    P.edit(old, new, "A", 'replaced the family-flat rent range 5,000-8,000 with the CBS Netanya averages for 3.5-4 and 4.5+ rooms (5,273 / 6,695 ש"ח, Q2 2026)',
           "Section on rent and price per m2: the same 5,000-8,000 range as in the lead, replaced by the CBS averages for 3.5-4 and 4.5+ rooms, Q2 2026. The next sentence ('rent helps check economic sense but does not replace comparable sales') stays.",
           [key(CITY, "3.5-4"), key(CITY, "4.5+")], url=RENT_URL)

    # --- quick-facts table: the common family-flat rent row
    def quick(old):
        h, rows = parse_table(old)
        out = []
        for r in rows:
            if r[0].strip() == "מה טווח שכירות נפוץ לדירת משפחה":
                out.append([f'מה שכר הדירה הממוצע לדירת משפחה, אפריל עד יוני 2026 ({LMS})', fam, r[2]])
            else:
                out.append(r)
        return rebuild(old, None, out)
    P.table('<th dir="rtl">שאלה מהירה</th>', quick, "A",
            'in the quick-facts table replaced the family-flat rent range 5,000-8,000 with the CBS Netanya averages for 3.5-4 and 4.5+ rooms (5,273 / 6,695 ש"ח, Q2 2026); the other rows are untouched',
            "Quick-facts table: the row 'common rent range for a family flat, about 5,000 to 8,000 a month' becomes the CBS average monthly rent in Netanya for 3.5-4 and 4.5+ rooms, Q2 2026 (the question and the usage note are reworded only as far as the figure requires); all other rows are untouched.",
            [key(CITY, "3.5-4"), key(CITY, "4.5+")], url=RENT_URL)
    # --- rent section
    old = P.sub('לפי דפי שכירות גלויים שנבדקו, נראו מאות מודעות פעילות, ובדף שכירות אחד הופיעו 226 מודעות', 'לא חוזי שכירות רשמיים לכל דירה.')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בנתניה {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}. '
           'אלה ממוצעים עירוניים, לא שכירות של דירה מסוימת.')
    P.edit(old, new, "A", 'replaced the ad counts (hundreds; 226 ads on 16.4.2026) and the market-page average 6,265 and median 5,300 with the CBS Netanya averages for all flats and by size group, Q2 2026',
           "Rent section: ad-page counts, a market-page average (6,265) and median (5,300) replaced by the CBS average monthly rent in Netanya for all flats (4,815.5) and by size group, Q2 2026. 'These are ad and market data, not official rental contracts' no longer applies; the closing sentence now says the figures are city averages, not the rent of a specific flat.",
           KEYS, url=RENT_URL)

    # --- rent check table
    def rent_table(old):
        h, rows = parse_table(old)
        by = {r[0].strip(): r for r in rows}
        head = [h[0], f'שכר דירה חודשי ממוצע, אפריל עד יוני 2026 ({LMS})', h[3]]
        body = [
            ["כלל הדירות בעיר", f'{c(CITY)} {CUR} לחודש', by["שכירות ממוצעת בדף שוק"][3]],
            ["1 עד 2 חדרים", f'{c(CITY, "1-2")} {CUR}', by["דירת 1 חדר במרכז צפון"][3]],
            ["2.5 עד 3 חדרים", f'{c(CITY, "2.5-3")} {CUR}', by["דירת 3 חדרים"][3]],
            ["3.5 עד 4 חדרים", f'{c(CITY, "3.5-4")} {CUR}', by["דירת 4 חדרים"][3]],
            ["4.5 חדרים ומעלה", f'{c(CITY, "4.5+")} {CUR}', by["4.5 חדרים במרכז דרום"][3] + "; " + by["5 חדרים בסי פארק"][3]],
            [by["דירה ליד הים או עם נוף"][0], "לא פורסם", by["דירה ליד הים או עם נוף"][3]],
        ]
        return rebuild(old, head, body)
    P.table('<th dir="rtl">סוג בדיקת שכירות</th>', rent_table, "A",
            'rebuilt the rent-check table on the CBS Netanya averages (all flats 4,816; 1-2: 3,084; 2.5-3: 4,116; 3.5-4: 5,273; 4.5+: 6,695 ש"ח, Q2 2026); the ad-count row, the market-page median row, the "working range" column (3,200-9,500) and the unsourced sea-view premium range were deleted; the sea-view row now reads "לא פורסם"',
            "Rent-check table (4 columns, 10 rows): the 226-ad row, the market-page average (6,265) and median (5,300), the example rents (3,800; 6,000; 8,000), the 'working range' column (3,200-9,500) and the 'hundreds to thousands per month' sea-view premium are all private or unsourced. Rebuilt on the CBS average monthly rent in Netanya for all flats and by size group, Q2 2026. The usage notes stay word for word (the 4.5+ row joins the two notes of the old 4.5-room and 5-room rows); the sea-view row keeps its advice and shows 'לא פורסם' because the CBS has no such figure.",
            KEYS, url=RENT_URL)
    # --- the 700 gap
    old = P.sub('פער של 700 ש"ח לחודש בשכירות יכול לשקף')
    P.edit(old, 'פער משמעותי בשכירות יכול לשקף', "B", 'removed the illustrative rent gap 700 ש"ח a month',
           "An illustrative gap of 700 a month has no official source; the number goes and the point (a gap can reflect upkeep, location, size or a different tenant pool) stays.")
