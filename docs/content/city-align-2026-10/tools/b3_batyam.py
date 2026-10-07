# -*- coding: utf-8 -*-
"""Tier 3, Bat Yam (page 4583). CBS row: בת ים (table 4.9, Q2 2026). The page writes ₪ and the Hebrew gershayim (U+05F4)."""
from b3lib import *

CITY = "בת ים"
CUR = "₪"
LMS = "הלמ״ס"
Q2S = Q2.replace(" (אפריל עד יוני)", "")


def build(P):
    sizes = by_size(CITY, CUR)
    KEYS = keys_all(CITY)
    G4 = ("1-2", "2.5-3", "3.5-4", "4.5+")
    # --- opening paragraph: private average rents
    old = P.sub(', ושכירות מבוקשת ממוצעת סביב 5,500 ₪. לפי אתר Realta,', 'תוארו כפופולריות במיוחד.')
    new = f'. לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בבת ים {Q2} היה {c(CITY)} {CUR}.'
    P.edit(old, new, "A", 'replaced the private average rents (asking average 5,500; second source 5,760) and the remark that 3-room flats are popular with the CBS Bat Yam average 4,407 ₪, Q2 2026; the count of sale listings stays',
           "Opening paragraph: asking-rent average 5,500 and a second ad site's average 5,760 replaced by the CBS average monthly rent in Bat Yam (4,407.4), Q2 2026. 'Three-room flats were described as especially popular' came from the same ad site and has no official figure; it goes. The sentence on the number of sale listings is not a rent figure and stays.",
           [key(CITY)], url=RENT_URL)
    # --- rent and yield section
    old = P.sub('לפי נתוני מדדירות, שהם נתוני אתר מתחרה דינמיים ולא מקור רשמי, הוצגו דוגמאות שכירות של', 'הוצגה סביב 5,760 ₪ לחודש.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בבת ים {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}.'
    P.edit(old, new, "A", 'replaced the ad-site examples (2 rooms 4,200; 3 rooms 4,600; 4 rooms 6,600; 5 rooms 8,950) and the second source average 5,760 with the CBS Bat Yam averages for all flats and by size group, Q2 2026',
           "Rent section: two ad-site sources (examples by rooms and an average of 5,760) replaced by the CBS average monthly rent in Bat Yam for all flats and by size group, Q2 2026 (4,407.4; 3,692.4; 4,107.4; 5,249.3; 7,110.1).",
           KEYS, url=RENT_URL)

    def swap(r):
        k = {"2 חדרים": "1-2", "3 חדרים": "2.5-3", "4 חדרים": "3.5-4", "5 חדרים": "4.5+"}[r[0].strip()]
        return f'{c(CITY, k)} {CUR} (דירות של {GROUP_HE[k]})'
    P.table('<th dir="rtl">שכירות חודשית לבדיקת שוק</th>',
            lambda old: table_cell_swap(old, 1, swap, f'שכר דירה חודשי ממוצע, אפריל עד יוני 2026 ({LMS})'),
            "A", 'replaced the rent ranges (2 rooms 3,800-4,800; 3 rooms 4,300-5,600; 4 rooms 5,800-7,200; 5 rooms 7,200-9,500) with the CBS Bat Yam averages by size group, Q2 2026; each cell names its group because the sale-median column beside it is by exact room count',
            "Rent column of the price table (ranges from private data, no date) replaced by the CBS average monthly rent in Bat Yam, Q2 2026. The rows keep their room labels (the neighbouring column is the Tax Authority median by exact room count), so each cell names its CBS size group. Header names the CBS and the quarter; the other columns are unchanged.",
            keys_all(CITY, G4), url=RENT_URL)
    # --- worked example 1
    old = P.sub('לדוגמה, דירה שנרכשת ב-2,000,000 ₪ ומושכרת ב-5,000 ₪ לחודש מייצרת 60,000 ₪ בשנה לפני הוצאות, כלומר כ-3.0% ברוטו.')
    new = (f'לדוגמה, דירה שנרכשת ב-2,000,000 ₪ ומושכרת ב-{c(CITY, "2.5-3")} ₪ לחודש, שכר הדירה הממוצע של {LMS} לדירות של 2.5 עד 3 חדרים בבת ים {Q2S}, '
           'מייצרת שכירות שנתית, ומחלקים אותה במחיר הקנייה כדי לקבל תשואה ברוטו, לפני הוצאות.')
    P.edit(old, new, "A", 'replaced the example rent 5,000 with the CBS 2.5-3 rooms average for Bat Yam (4,107 ₪, Q2 2026); dropped the annual rent 60,000 and the yield 3.0% that depended on it (no new arithmetic)',
           "Worked example: the round rent 5,000 sat inside the page's own 3-4 room ad ranges; it becomes the CBS 2.5-3 rooms average (4,107.4). The annual rent (60,000) and the yield (3.0%) were derived from it and are removed, not recomputed (no new arithmetic). The purchase price 2,000,000 is the example's own and stays.",
           [key(CITY, "2.5-3"), "page"], kept=["2,000,000"], url=RENT_URL)
    # --- worked example 2
    old = P.sub('אם דירה בת 3 חדרים יכולה להניב 5,200 ₪ בחודש, והמחיר המבוקש הוא 2,600,000 ₪, הקונה עשוי לטעון שהתשואה הגסה נמוכה מכ-2.4%.')
    new = (f'אם דירה בת 3 חדרים יכולה להניב {c(CITY, "2.5-3")} ₪ בחודש, שכר הדירה הממוצע של {LMS} לדירות של 2.5 עד 3 חדרים בבת ים {Q2S}, '
           'והמחיר המבוקש הוא 2,600,000 ₪, הקונה עשוי לטעון שהתשואה הגסה נמוכה.')
    P.edit(old, new, "A", 'replaced the example rent 5,200 with the CBS 2.5-3 rooms average for Bat Yam (4,107 ₪, Q2 2026); dropped the yield 2.4% that depended on it',
           "Second example: the rent 5,200 becomes the CBS 2.5-3 rooms average (4,107.4); the yield 'about 2.4%' came from 5,200 and is removed, the sentence keeps its point (the buyer may argue the gross yield is low).",
           [key(CITY, "2.5-3"), "page"], kept=["2,600,000"], url=RENT_URL)
    # --- asking vs closed rent gap
    old = P.sub('פער של 300-700 ₪ בחודש יכול לשנות את התמונה השנתית ב-3,600-8,400 ₪.')
    P.edit(old, 'פער של כמה מאות שקלים בחודש יכול לשנות את התמונה השנתית באלפי שקלים.', "B",
           'removed the unsourced monthly gap 300-700 and its annual 3,600-8,400; the sentence says it in words',
           "A typical asking-vs-closed gap of 300-700 per month (3,600-8,400 per year) has no official source; the numbers go and the arithmetic point stays in words.")
    # --- FAQ
    old = P.sub('לפי נתוני מדדירות, שהם נתוני אתר מתחרה דינמיים לצורכי השוואה ולא מקור רשמי, שכירות מבוקשת ממוצעת הוצגה סביב 5,500 ₪. לפי Realta, מקור מודעות שכירות, שכירות ממוצעת הוצגה סביב 5,760 ₪.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בבת ים {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}.'
    P.edit(old, new, "A", 'replaced the FAQ asking averages (5,500 and 5,760) with the CBS Bat Yam averages for all flats and by size group, Q2 2026',
           "FAQ 'average rent in Bat Yam': two ad-site averages replaced by the CBS average (4,407.4) and the size-group averages, Q2 2026. The sentence that follows (separate 2, 3, 4 and 5 rooms in a practical check) now follows the breakdown.",
           KEYS, url=RENT_URL)
