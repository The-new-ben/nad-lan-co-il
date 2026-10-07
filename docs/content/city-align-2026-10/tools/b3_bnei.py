# -*- coding: utf-8 -*-
"""Tier 3, Bnei Brak (page 4595). CBS row: בני ברק (table 4.9, Q2 2026). The page writes ש"ח and ASCII quotes."""
from b3lib import *

CITY = "בני ברק"
CUR = 'ש"ח'
LMS = 'הלמ"ס'
Q2S = Q2.replace(" (אפריל עד יוני)", "")


def build(P):
    sizes = by_size(CITY, CUR)
    KEYS = keys_all(CITY)
    G4 = ("1-2", "2.5-3", "3.5-4", "4.5+")
    # --- lead
    old = P.sub('בשכירות, המחירים המבוקשים במודעות נעים לרוב מכ-4,000 ש"ח לדירת 2 חדרים ועד כ-7,900 ש"ח לדירת 5 חדרים, עם פערים גדולים לפי רחוב, קומה, מצב הבניין והאזור בעיר.')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בבני ברק {Q2} נע מ-{c(CITY, "1-2")} {CUR} לדירות של 1 עד 2 חדרים ועד {c(CITY, "4.5+")} {CUR} לדירות של 4.5 חדרים ומעלה, '
           'ובפועל השכירות משתנה לפי רחוב, קומה, מצב הבניין והאזור בעיר.')
    P.edit(old, new, "A", 'replaced the asking rents 4,000 (2 rooms) to 7,900 (5 rooms) with the CBS Bnei Brak range by size group, Q2 2026: 3,443 (1-2 rooms) to 6,272 (4.5+ rooms) ש"ח',
           "Lead: asking-rent range from ads (4,000 to 7,900) replaced by the CBS average monthly rent in Bnei Brak, 1-2 rooms 3,442.5 to 4.5+ rooms 6,271.6, Q2 2026. 'Large gaps by street, floor, building condition and area' was a level claim without an official figure; it becomes the hedged 'in practice rent varies by street, floor, building condition and area'.",
           [key(CITY, "1-2"), key(CITY, "4.5+")], url=RENT_URL)
    # --- body: private average rent and yield
    old = P.sub('במקור פרטי דינמי, לצד שכר דירה ממוצע מבוקש של כ-5,700 ש"ח ותשואה ממוצעת מוצגת של כ-3.6%. באותו מקור הופיעו')
    new = f'במקור פרטי דינמי. לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בבני ברק {Q2} היה {c(CITY)} {CUR}. במקור הפרטי הופיעו'
    P.edit(old, new, "A", 'replaced the private asking rent 5,700 with the CBS Bnei Brak average 4,483 ש"ח (Q2 2026); removed the private yield 3.6%',
           "Body: asking-rent average 5,700 replaced by the CBS average monthly rent in Bnei Brak (4,482.5), Q2 2026; the private-source yield 'about 3.6%' was built on that rent and has no official counterpart, so it is removed. 'The same source' becomes 'the private source' because the CBS sentence now sits between.",
           [key(CITY)], url=RENT_URL)
    # --- regional rent paragraph: delete
    P.delete_para('גם שמות אזוריים דורשים זהירות. נתוני שכירות שנבדקו ב-29 במאי 2026',
                  'deleted the paragraph with 5 area rents (Pardes Katz 4,900; Tel Giborim 4,100; Givat Rokach 5,350; Nahalat Shimon 4,313; industrial zone 6,100): the CBS publishes no area rent',
                  "A paragraph of area rent averages from a private ad site (5 areas, 2-11 ads each). The CBS publishes rent for the city and its size groups only; the paragraph has no content without the numbers.")
    # --- two private sources
    old = P.sub('בדיקת לוחות ומקורות פרטיים מצאה שכר דירה מבוקש ממוצע של כ-5,700 ש"ח במקור אחד,', 'את הדירה הרגילה.')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בבני ברק {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}. '
           'ממוצע עירוני אחד מסתיר שוני בין דירות קטנות לגדולות, ולכן משווים לפי גודל הדירה.')
    P.edit(old, new, "A", 'replaced the two private rent sources (asking average 5,700; 37 ads: average 4,888, median 4,600, cheapest 2,500) and the remark built on their gap with the CBS Bnei Brak averages for all flats and by size group, Q2 2026',
           "Two private rent sources (5,700 asking average; a 37-ad sample with average 4,888, median 4,600 and cheapest 2,500) and the sentences about the gap between them replaced by the CBS average monthly rent in Bnei Brak for all flats and by size group, Q2 2026. The new closing sentence is carried by the CBS size groups themselves (3,443 against 6,272).",
           KEYS, url=RENT_URL)

    # --- rent table
    def rent_table(old):
        h, rows = parse_table(old)
        by = {r[0].strip(): r for r in rows}
        head = [h[0], f'שכר דירה חודשי ממוצע, אפריל עד יוני 2026 ({LMS})', h[2]]
        body = [
            ["1 עד 2 חדרים", f'{c(CITY, "1-2")} {CUR}', by["2 חדרים"][2]],
            ["2.5 עד 3 חדרים", f'{c(CITY, "2.5-3")} {CUR}', by["3 חדרים"][2]],
            ["3.5 עד 4 חדרים", f'{c(CITY, "3.5-4")} {CUR}', by["4 חדרים"][2]],
            ["4.5 חדרים ומעלה", f'{c(CITY, "4.5+")} {CUR}', by["5 חדרים"][2]],
            ["ממוצע עירוני לכלל הדירות", f'{c(CITY)} {CUR}', by["ממוצע שכירות מקור פרטי"][2]],
        ]
        return rebuild(old, head, body)
    P.table('<th dir="rtl">חתך שכירות</th>', rent_table, "A",
            'rebuilt the rent table on the CBS Bnei Brak averages (size groups 3,443 / 4,236 / 5,030 / 6,272 and all flats 4,483 ש"ח, Q2 2026); the private average 5,700, the second source 4,888 and the median 4,600 rows deleted',
            "Rent table (2, 3, 4, 5 rooms: 4,000; 4,700; 5,950; 7,900 and three source rows: private average 5,700, another average 4,888, median 4,600) rebuilt on the CBS average monthly rent in Bnei Brak by size group and for all flats, Q2 2026. Rows regrouped to the CBS groups; the city-average row keeps the note of the old private-average row ('good as a general measure, not a substitute for checking a specific flat'); the second-source and median rows (notes on the gap between sources and on median vs average) have no meaning on an official figure and are deleted.",
            KEYS, url=RENT_URL)
    # --- worked examples
    old = P.sub('ומושכרת סביב 4,700 ש"ח, דמי השכירות השנתיים הם כ-56,400 ש"ח לפני הוצאות, תקופות ריקות, תיקונים ומיסוי.', 'דמי השכירות השנתיים הם כ-71,400 ש"ח.')
    new = (f'ומושכרת ב-{c(CITY, "2.5-3")} {CUR}, שכר הדירה הממוצע של {LMS} לדירות של 2.5 עד 3 חדרים בבני ברק {Q2S}, מכפילים ב-12 ומקבלים את דמי השכירות השנתיים, '
           f'לפני הוצאות, תקופות ריקות, תיקונים ומיסוי. אם דירת 4 חדרים עולה 2,445,000 {CUR} ומושכרת ב-{c(CITY, "3.5-4")} {CUR}, '
           f'הממוצע של {LMS} לדירות של 3.5 עד 4 חדרים, אותו חישוב נותן את דמי השכירות השנתיים של דירה כזו.')
    P.edit(old, new, "A", 'replaced the example rents 4,700 and 5,950 with the CBS Bnei Brak averages for 2.5-3 and 3.5-4 rooms (4,236 / 5,030 ש"ח, Q2 2026); dropped the annual rents 56,400 and 71,400 (no new arithmetic)',
           "Worked examples: rents 4,700 and 5,950 (ad-site figures from the table) become the CBS size-group averages; the annual rents 56,400 and 71,400 were derived from them and are removed, not recomputed. The sale prices (1,980,000 and 2,445,000) are the page's own and stay.",
           [key(CITY, "2.5-3"), key(CITY, "3.5-4"), "page"], kept=["2,445,000"], url=RENT_URL)
    # --- table of areas: delete (neighbourhood rents + listing counts)
    P.table('<th dir="rtl">אזור שכירות</th>', lambda old: "", "C",
            'deleted the table of 9 area rents (Pardes Katz 4,900 ... Shikun HaHistadrut 2,500) with their ad counts and notes: the CBS publishes no area rent',
            "A whole table of area rents from a private ad site (9 areas, 1-11 ads each) with notes that only comment on the sample size or on the rent level. No official area rent exists, and without the numbers the table has no content. The paragraphs before and after it do not refer to it by name.")
    # --- asking vs signed contract (two single ads)
    old = P.sub('מודעה במחיר 6,500 ש"ח אינה אומרת שהדירה הושכרה במחיר זה, ומודעה של 2,500 ש"ח יכולה להיות חריגה')
    P.edit(old, 'מודעה במחיר גבוה אינה אומרת שהדירה הושכרה במחיר זה, ומודעה במחיר נמוך מאוד יכולה להיות חריגה', "B",
           'removed the two single-ad rents 6,500 and 2,500 (they came from the deleted area table); the caution stays in words',
           "The two example ad prices (6,500 and 2,500) were single listings of the deleted area table; the numbers go, the caution (an ad price is not a signed contract; an extreme ad can be an exception) stays.")
    # --- FAQ areas
    old = P.sub('נתוני שכירות שנבדקו מצאו בפרדס כץ ויסודות 11 מודעות בממוצע 4,900 ש"ח, אך זה נתון שכירות ולא מחיר מכירה. ')
    P.edit(old, '', "B", 'removed the Pardes Katz area rent 4,900 (11 ads) from the FAQ answer; the answer ends on the advice to check similar deals',
           "FAQ: the area rent (4,900, 11 ads) has no official counterpart. The sentence is removed; the answer keeps its hedged gaps-by-street remark and the advice to check similar deals in the same area.")
    # --- FAQ rent by rooms
    old = P.sub('לפי נתוני ביקוש, דירות 2 חדרים הוצגו סביב 4,000 ש"ח,', 'חציון 4,600 ש"ח מתוך 37 מודעות.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בבני ברק {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}.'
    P.edit(old, new, "A", 'replaced the FAQ rents by rooms (4,000 / 4,700 / 5,950 / 7,900) and the second source (average 4,888, median 4,600, 37 ads) with the CBS Bnei Brak averages for all flats and by size group, Q2 2026',
           "FAQ 'how much rent in Bnei Brak': ad-site rents by rooms and a second source replaced by the CBS averages for all flats and by size group, Q2 2026. The closing advice (verify against signed contracts and rental deals) stays.",
           KEYS, url=RENT_URL)
