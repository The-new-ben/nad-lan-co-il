# -*- coding: utf-8 -*-
"""Tier 3, Ashdod (page 4587). CBS row: אשדוד (table 4.9, Q2 2026)."""
from b3lib import *

CITY = "אשדוד"
Q2S = Q2.replace(" (אפריל עד יוני)", "")  # 'ברבעון השני של 2026'


def build(P):
    sizes = by_size(CITY)
    # --- lead
    old = P.sub('בשכירות, דירת 2 חדרים באשדוד מוצגת סביב', '7,650 ש"ח.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע באשדוד {Q2} היה {sizes}.'
    P.edit(old, new, "A", 'replaced the listing-site rents by rooms (2: 3,500; 3: 4,474-4,500; 4: 5,300; 5: 7,650) with the CBS average rent in Ashdod by size group, Q2 2026: 3,119 / 3,906 / 4,855 / 6,239 ש"ח',
           "Lead: rents by room count from listing pages (3,500, 4,474-4,500, 5,300, 7,650) replaced by the CBS average monthly rent in Ashdod by size group, Q2 2026 (table 4.9: 1-2 rooms 3,119.3; 2.5-3 3,905.7; 3.5-4 4,855.4; 4.5+ 6,238.5, rounded half up). The next sentence ('these are opening numbers, not a valuation') still reads correctly.",
           keys_all(CITY, ("1-2", "2.5-3", "3.5-4", "4.5+")), url=RENT_URL)
    # --- districts: private rent for two districts
    old = P.sub('ובדפי נתונים פרטיים הוצגה בהם שכירות סביב 4,000-4,200 ש"ח, אך')
    P.edit(old, 'אך', "B", 'removed the district rent 4,000-4,200 (listing pages; the CBS publishes no district rent); the sentence now ends on the official sale medians',
           "Rent for districts C and F (4,000-4,200) came from private data pages; the CBS publishes no district rent, so the number goes. The sale medians in the same sentence are the Tax Authority figures and stay.")
    # --- rent table
    def swap(r):
        k = {"2 חדרים": "1-2", "3 חדרים": "2.5-3", "4 חדרים": "3.5-4", "5 חדרים": "4.5+"}[r[0].strip()]
        return f'{c(CITY, k)} ש"ח (דירות של {GROUP_HE[k]})'
    P.table('<th dir="rtl">שכירות חודשית נפוצה</th>',
            lambda old: table_cell_swap(old, 1, swap, 'שכר דירה חודשי ממוצע, אפריל עד יוני 2026 (הלמ"ס)'),
            "A", 'replaced the rent column (2 rooms 3,500; 3 rooms 4,474-4,500; 4 rooms 5,300; 5 rooms 7,650) with the CBS Ashdod averages by size group, Q2 2026; each cell names its group because the sale-median column beside it is by exact room count',
            "Rent column of the price table replaced by the CBS average monthly rent in Ashdod, Q2 2026. The rows keep their room labels (the neighbouring column is the Tax Authority median by exact room count), so every rent cell names its CBS size group (2 rooms = 1-2, 3 = 2.5-3, 4 = 3.5-4, 5 = 4.5+). Header says CBS and the quarter; usage notes unchanged.",
            keys_all(CITY, ("1-2", "2.5-3", "3.5-4", "4.5+")), url=RENT_URL)
    # --- private rent source paragraph
    old = P.sub('מקור פרטי לשכירות הציג שכירות חציונית באשדוד', 'וממוצע ארצי סביב 4,400 ש"ח.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע באשדוד {Q2} היה {c(CITY)} ש"ח, לעומת {c("סך הכל")} ש"ח בממוצע הארצי.'
    P.edit(old, new, "A", 'replaced the private rent median 3,925 (250 listings), 3-room 4,474 and national 4,400 with the CBS Ashdod average 4,455 and the CBS national average 5,086 ש"ח, Q2 2026',
           "Private-source city rent median (3,925, 250 listings), 3-room figure (4,474) and national figure (4,400) replaced by the CBS average rent in Ashdod (4,454.6) and in all of Israel (5,085.5), Q2 2026. The following sentence (such data helps spot a flat priced away from the market, not a substitute for live listings and contracts) stays word for word.",
           [key(CITY), key("סך הכל")], url=RENT_URL)
    # --- yield example (hypothetical built on the listing-site 5,300)
    old = P.sub('והשכירות הצפויה היא 5,300 ש"ח, התשואה הגולמית היא כ-2.9% לפני הוצאות, תקופות ריקות, תחזוקה ומס.')
    new = (f'והשכירות הצפויה היא כ-{c(CITY, "3.5-4")} ש"ח, הממוצע של הלמ"ס לדירות של 3.5 עד 4 חדרים {Q2S}, '
           'התשואה הגולמית היא השכירות השנתית חלקי המחיר, לפני הוצאות, תקופות ריקות, תחזוקה ומס.')
    P.edit(old, new, "A", 'replaced the example rent 5,300 with the CBS average for 3.5-4 rooms in Ashdod (4,855, Q2 2026) and dropped the computed yield 2.9% (no new arithmetic); the formula stays',
           "Worked example: the 5,300 rent was the listing-site 4-room figure; it becomes the CBS 3.5-4 rooms average (4,855.4). The result '2.9%' depended on 5,300 and is removed, not recomputed (no new arithmetic); the sentence keeps the method and the two sale prices (hypothetical, already on the page).",
           [key(CITY, "3.5-4"), "page"], kept=["2,200,000"], url=RENT_URL)
    # --- districts again (FAQ)
    old = P.sub('בדפי נתונים פרטיים הוצגה ברובעים האלה שכירות סביב 4,000-4,200 ש"ח. ')
    P.edit(old, '', "B", 'removed the sentence with the district rent 4,000-4,200 (listing pages; no official district rent)',
           "FAQ: same district rent figure as in the body (4,000-4,200 from private pages); the CBS publishes no district rent, so the sentence is removed. 'These are direction-only data' now refers to the official sale medians above it.")
    # --- FAQ: how much rent in Ashdod
    old = P.sub('דירת 2 חדרים מוצגת סביב 3,500 ש"ח לחודש, דירת 3 חדרים סביב', 'אך השונות בין רובעים ודירות גבוהה.')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע באשדוד {Q2} היה {c(CITY)} ש"ח בממוצע לכלל הדירות בעיר, ובחלוקה לפי גודל: {sizes}. '
           'בפועל השכירות משתנה לפי הרובע והדירה.')
    P.edit(old, new, "A", 'replaced the FAQ rents by rooms (3,500 / 4,474-4,500 / 5,300 / 7,650) and the city median 3,925 with the CBS Ashdod averages by size group and for all flats, Q2 2026',
           "FAQ 'how much rent in Ashdod': the listing-site list and the city median 3,925 replaced by the CBS size-group averages and the city average (4,454.6), Q2 2026. 'The variance between districts and flats is high' was a level claim without an official figure; it becomes the hedged 'in practice rent varies by district and flat'.",
           keys_all(CITY), url=RENT_URL)
    # --- FAQ: yield example
    old = P.sub('לדוגמה, דירה שעולה 2,190,000 ש"ח ומושכרת ב-5,300 ש"ח לחודש נותנת שכירות שנתית של 63,600 ש"ח ותשואה גולמית של כ-2.9%.')
    new = (f'לדוגמה, דירה שעולה 2,190,000 ש"ח ומושכרת ב-{c(CITY, "3.5-4")} ש"ח לחודש, שכר הדירה הממוצע של {CBS_NAME} לדירות של 3.5 עד 4 חדרים באשדוד {Q2S}, '
           'נותנת תשואה גולמית לפי אותה נוסחה.')
    P.edit(old, new, "A", 'replaced the example rent 5,300 with the CBS 3.5-4 rooms average for Ashdod (4,855, Q2 2026); dropped the annual rent 63,600 and the yield 2.9% that depended on it (no new arithmetic)',
           "FAQ worked example: rent 5,300 (the listing-site 4-room figure) becomes the CBS 3.5-4 rooms average (4,855.4); annual rent 63,600 and yield 2.9% were derived from it and are removed rather than recomputed.",
           [key(CITY, "3.5-4"), "page"], kept=["2,190,000"], url=RENT_URL)
