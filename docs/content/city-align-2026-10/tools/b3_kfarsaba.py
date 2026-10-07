# -*- coding: utf-8 -*-
"""Tier 3, Kfar Saba (page 4562). CBS row: כפר סבא (table 4.9, Q2 2026; the 1-2 rooms cell is not published). The page writes ש"ח and ASCII quotes."""
from b3lib import *

CITY = "כפר סבא"
CUR = 'ש"ח'
LMS = 'הלמ"ס'
Q2S = Q2.replace(" (אפריל עד יוני)", "")


def build(P):
    G3 = ("2.5-3", "3.5-4", "4.5+")  # the CBS published no 1-2 rooms average for Kfar Saba
    sizes = by_size(CITY, CUR, G3)
    # --- lead
    old = P.sub('בשכירות, הממוצע החודשי עומד סביב 7,200 עד 7,350 ש"ח לפי מקורות שוק שנבדקו ביוני 2026.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בכפר סבא {Q2} היה {c(CITY)} {CUR}.'
    P.edit(old, new, "A", 'replaced the market-source average rent 7,200-7,350 with the CBS Kfar Saba average 6,146 ש"ח (Q2 2026)',
           "Lead: 'the monthly average rent is around 7,200 to 7,350 according to market sources checked in June 2026' replaced by the CBS average monthly rent in Kfar Saba (6,145.8), Q2 2026.",
           [key(CITY)], url=RENT_URL)
    # --- section 'how much does a flat cost'
    old = P.sub('השכירות החודשית הממוצעת נעה סביב 7,200 עד 7,350 ש"ח. אלה מספרים טובים לפתיחת בדיקה')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בכפר סבא {Q2} היה {c(CITY)} {CUR}. אלה מספרים טובים לפתיחת בדיקה'
    P.edit(old, new, "A", 'replaced the average rent 7,200-7,350 with the CBS Kfar Saba average 6,146 ש"ח (Q2 2026)',
           "Same figure as in the lead (7,200 to 7,350, market sources) replaced by the CBS average monthly rent in Kfar Saba (6,145.8), Q2 2026; the sale medians in the paragraph are the Tax Authority figures and stay.",
           [key(CITY)], url=RENT_URL)
    # --- rent section
    old = P.sub('אם דירת 4 חדרים מושכרת סביב 6,750 עד 6,800 ש"ח לחודש, ודירת 5 חדרים סביב 8,100 עד 9,100 ש"ח, ניתן להבין את עומק הביקוש המשפחתי בעיר.')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בכפר סבא {Q2} היה {c(CITY, "3.5-4")} {CUR} לדירות של 3.5 עד 4 חדרים '
           f'ו-{c(CITY, "4.5+")} {CUR} לדירות של 4.5 חדרים ומעלה, ומכאן ניתן להבין את עומק הביקוש המשפחתי בעיר.')
    P.edit(old, new, "A", 'replaced the family-flat rents (4 rooms 6,750-6,800; 5 rooms 8,100-9,100) with the CBS Kfar Saba averages for 3.5-4 and 4.5+ rooms, Q2 2026: 6,042 / 7,796 ש"ח',
           "Rent section: 4-room and 5-room asking rents replaced by the CBS average monthly rent in Kfar Saba for 3.5-4 rooms (6,041.6) and 4.5+ rooms (7,795.9), Q2 2026.",
           [key(CITY, "3.5-4"), key(CITY, "4.5+")], url=RENT_URL)

    # --- rent / sale median table
    def swap(r):
        lab = r[0].strip()
        k = {"3 חדרים": "2.5-3", "4 חדרים": "3.5-4", "5 חדרים": "4.5+"}.get(lab)
        if k is None:  # 2 rooms (the CBS has no cell) and the private house (not a CBS category)
            return "לא פורסם"
        return f'{c(CITY, k)} {CUR} (דירות של {GROUP_HE[k]})'
    P.table('<th dir="rtl">שכירות שוק</th>',
            lambda old: table_cell_swap(old, 1, swap, f'שכר דירה חודשי ממוצע, אפריל עד יוני 2026 ({LMS})'),
            "A", 'replaced the market rents (2 rooms 4,000-4,500; 3 rooms 5,550-5,800; 4 rooms 6,750-6,800; 5 rooms 8,100-9,100; private house 13,500) with the CBS Kfar Saba averages (4,771 / 6,042 / 7,796 ש"ח, Q2 2026); the 2-room and private-house cells say "לא פורסם" (the CBS has no such figure)',
            "Rent column of the table replaced by the CBS average monthly rent in Kfar Saba by size group, Q2 2026; the rows keep their room labels (the next column is the Tax Authority median by exact room count) so each cell names its group. The CBS table has no 1-2 rooms cell for Kfar Saba (dash) and no private-house category: those two cells read 'לא פורסם', the same wording the table already uses for the missing sale median. Header names the CBS and the quarter.",
            keys_all(CITY, G3), url=RENT_URL)
    # --- FAQ
    old = P.sub('השכירות החודשית הממוצעת נעה סביב 7,200 עד 7,350 ש"ח. לפי סוג דירה, דירות 2 חדרים', 'סביב 8,100 עד 9,100 ש"ח.')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בכפר סבא {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}. '
           'לדירות של 1 עד 2 חדרים לא פורסם ממוצע.')
    P.edit(old, new, "A", 'replaced the FAQ rents (average 7,200-7,350; by rooms 4,000-9,100) with the CBS Kfar Saba averages for all flats and by size group, Q2 2026; states that no 1-2 rooms average was published',
           "FAQ 'what is the average rent in Kfar Saba': market-source average and per-room ranges replaced by the CBS averages for all flats (6,145.8) and for 2.5-3, 3.5-4 and 4.5+ rooms, Q2 2026. The CBS table has no 1-2 rooms cell for Kfar Saba, so the answer says so instead of keeping the 4,000-4,500 asking range.",
           keys_all(CITY, ("total",) + G3), url=RENT_URL)
