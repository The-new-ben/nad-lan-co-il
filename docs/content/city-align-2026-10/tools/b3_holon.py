# -*- coding: utf-8 -*-
"""Tier 3, Holon (page 4585). CBS row: חולון (table 4.9, Q2 2026). The page writes ₪ and the Hebrew gershayim (U+05F4)."""
from b3lib import *

CITY = "חולון"
CUR = "₪"
LMS = "הלמ״ס"
Q2S = Q2.replace(" (אפריל עד יוני)", "")


def build(P):
    sizes = by_size(CITY, CUR)
    KEYS = keys_all(CITY)
    G4 = ("1-2", "2.5-3", "3.5-4", "4.5+")
    # --- opening: private asking rents
    old = P.sub(', ושכירות מבוקשת ממוצעת סביב 5,150 ₪. באותו מקור מופיעות דוגמאות שכירות לפי חדרים:', 'אלה נתוני השוואה של מודעות ושוק פרטי,')
    new = (f'. לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בחולון {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}. '
           'נתוני המודעות הם נתוני השוואה של שוק פרטי,')
    P.edit(old, new, "A", 'replaced the private asking rent 5,150 and the examples by rooms (4,100 / 4,500 / 5,800 / 8,200) with the CBS Holon averages for all flats and by size group, Q2 2026; the count of sale listings stays',
           "Opening: asking-rent average 5,150 and the per-room examples from an ad site replaced by the CBS average monthly rent in Holon (4,944.5) and by size group (3,556.8; 4,320.9; 5,433.5; 6,981.2), Q2 2026. The sentence on the number of listings is not a rent figure and stays; 'these are comparison data of listings and a private market' becomes 'the listing data are comparison data of a private market'.",
           KEYS, url=RENT_URL)
    # --- worked example
    old = P.sub('והשכירות הסבירה שלה היא 4,500-5,000 ₪,', 'ושכירותה עדיין סביב 4,700 ₪,')
    new = (f'והשכירות הסבירה שלה קרובה ל-{c(CITY, "2.5-3")} {CUR}, הממוצע של {LMS} לדירות של 2.5 עד 3 חדרים בחולון {Q2S}, '
           'מתקבלת תשואה ברוטו שנתית שמחשבים מהשכירות השנתית ומהמחיר, לפני הוצאות, תקופות ריקות, תיקונים, מס ושונות. '
           'אם דירה דומה מוצעת ב-2,300,000 ₪ ושכירותה עדיין קרובה לממוצע הזה,')
    P.edit(old, new, "A", 'replaced the example rents 4,500-5,000 and 4,700 with the CBS 2.5-3 rooms average for Holon (4,321 ₪, Q2 2026); dropped the computed yield 2.8%-3.1% (no new arithmetic)',
           "Worked example: the 'reasonable rent' 4,500-5,000 and the 4,700 come from the ad-site rents; they become the CBS 2.5-3 rooms average (4,320.9). The yield '2.8%-3.1%' was derived from the rent range and is removed, not recomputed. The sale prices 1,950,000 and 2,300,000 are the example's own and stay.",
           [key(CITY, "2.5-3"), "page"], kept=["1,950,000", "2,300,000"], url=RENT_URL)
    # --- paragraph on the spread between private sources
    P.delete_para('מקורות פרטיים מציגים טווחים שונים לשכירות בחולון.',
                  'deleted the paragraph that set three private rent sources against each other (5,150; 5,721 and median 5,200; 5,563)',
                  "The paragraph only compared three private rent sources (5,150, 5,721 with median 5,200, 5,563) and advised working with a range. With the CBS figure on the page there is nothing left to reconcile; no official counterpart for the three source figures.")

    # --- rent / price / yield table
    def rent_table(old):
        h, rows = parse_table(old)
        k = {"3 חדרים": "2.5-3", "4 חדרים": "3.5-4", "5 חדרים": "4.5+"}
        head = [h[0], f'שכר דירה חודשי ממוצע, אפריל עד יוני 2026 ({LMS})', h[3]]
        body = [[r[0], f'{c(CITY, k[r[0].strip()])} {CUR} (דירות של {GROUP_HE[k[r[0].strip()]]})', r[3]] for r in rows]
        return rebuild(old, head, body)
    P.table('<th dir="rtl">טווח שכירות בדיקה</th>', rent_table, "A",
            'replaced the private asking rent (4,500 / 5,800 / 8,200) with the CBS Holon averages by size group, Q2 2026 (4,321 / 5,434 / 6,981 ₪); deleted the private rent-range column (4,200-8,800) and the gross-yield column (2.2%-3.7%) built on it; the purchase-price column stays',
            "Table of rent, purchase price and gross yield by rooms: the asking-rent column becomes the CBS average rent in Holon by size group, Q2 2026 (each cell names its group because the purchase-price column is by exact room count). Deleted: the private rent-range column and the gross-yield column, which were computed from the private rents and cannot be recomputed without new arithmetic. The estimated purchase prices stay (tier 1 found them consistent with the official medians).",
            keys_all(CITY, ("2.5-3", "3.5-4", "4.5+")), url=RENT_URL)
    # --- FAQ
    old = P.sub('שכירות ממוצעת פרטית מוצגת סביב 5,150-5,721 ₪, וחציון סביב 5,200 ₪. מול מחיר קנייה של 2,000,000-2,700,000 ₪ מתקבלת לרוב תשואה ברוטו מתונה, לפני הוצאות ומסים.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בחולון {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות.'
    P.edit(old, new, "A", 'replaced the FAQ private average 5,150-5,721 and median 5,200 with the CBS Holon average 4,945 ₪ (Q2 2026); deleted the unsourced "moderate gross yield" claim against 2,000,000-2,700,000',
           "FAQ 'does rent in Holon justify the purchase prices': private average (5,150-5,721) and median (5,200) replaced by the CBS average rent (4,944.5), Q2 2026. 'Usually a moderate gross yield' against a price band was a level claim built on the private rents with no official yield figure; it is deleted.",
           [key(CITY)], url=RENT_URL)
