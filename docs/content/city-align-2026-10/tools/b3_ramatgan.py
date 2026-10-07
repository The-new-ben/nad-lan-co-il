# -*- coding: utf-8 -*-
"""Tier 3, Ramat Gan (page 4570). CBS row: רמת גן (table 4.9, Q2 2026). The page writes ש"ח and ASCII quotes."""
from b3lib import *

CITY = "רמת גן"
CUR = 'ש"ח'
LMS = 'הלמ"ס'
Q2S = Q2.replace(" (אפריל עד יוני)", "")


def build(P):
    sizes = by_size(CITY, CUR)
    KEYS = keys_all(CITY)
    G4 = ("1-2", "2.5-3", "3.5-4", "4.5+")
    # --- opening: median 6,000, average 6,411 and 2/3/4 rooms
    old = P.sub('שכירות חציונית סביב 6,000 ש"ח ושכירות ממוצעת סביב 6,411 ש"ח נותנות בדיקת שוק ראשונית.', 'אך שכירות אינה מחליפה')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע ברמת גן {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}, אך שכירות אינה מחליפה'
    P.edit(old, new, "A", 'replaced the median 6,000, the average 6,411 (the "about 6,411" the CEO flagged) and the per-room rents (2: 4,896; 3: 6,486; 4: 7,736) with the CBS Ramat Gan averages for all flats and by size group, Q2 2026',
           "Opening: listing-site median (6,000), average (6,411) and per-room rents (4,896; 6,486; 7,736) replaced by the CBS average monthly rent in Ramat Gan for all flats (5,893.8, against the listing average 6,411) and by size group (4,168.3; 5,468.9; 6,826.5; 8,254.5), Q2 2026. The CBS publishes no median rent.",
           KEYS, url=RENT_URL)
    # --- overview paragraph
    old = P.sub('שכירות סביב 6,000-6,500 ש"ח בחציון או בממוצע עוזרת לבצע בדיקת היגיון, אבל')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע ברמת גן {Q2} היה {c(CITY)} {CUR}, והוא עוזר לבצע בדיקת היגיון, אבל'
    P.edit(old, new, "A", 'replaced the rent 6,000-6,500 (median or average) with the CBS Ramat Gan average 5,894 ש"ח (Q2 2026)',
           "Overview: 'rent around 6,000-6,500, median or average' replaced by the CBS average monthly rent in Ramat Gan (5,893.8), Q2 2026.",
           [key(CITY)], url=RENT_URL)

    # --- fact table: median, average and the ad count
    def facts(old):
        h, rows = parse_table(old)
        out = []
        for r in rows:
            lab = r[0].strip()
            if lab in ("שכירות חציונית", "מודעות שכירות פעילות שנבדקו"):
                continue
            if lab == "שכירות ממוצעת":
                out.append([f'שכר דירה חודשי ממוצע, אפריל עד יוני 2026 ({LMS})', f'{c(CITY)} {CUR}', r[2]])
            else:
                out.append(r)
        return rebuild(old, None, out)
    P.table('<th dir="rtl">מספר עבודה</th>', facts, "A",
            'in the fact table replaced the average rent 6,411 with the CBS Ramat Gan average 5,894 ש"ח (Q2 2026) and deleted the median row 6,000 and the "520 active rent ads checked" row; the other rows are untouched',
            "Fact table: the row 'average rent about 6,411' becomes the CBS average monthly rent in Ramat Gan (5,893.8), Q2 2026; the row 'median rent about 6,000' is deleted (the CBS publishes no median rent) and so is the row with the 520-ad sample size, which only qualified those two figures. Rows on sale price, price per m2, listings, deals and the Tel Aviv district share stay word for word.",
            [key(CITY)], url=RENT_URL)

    # --- rooms table
    GROUP = {"1 חדר": "1-2", "2 חדרים": "1-2", "3 חדרים": "2.5-3", "4 חדרים": "3.5-4", "5 חדרים": "4.5+", "6 חדרים ומעלה": "4.5+"}

    def swap(r):
        k = GROUP[r[0].strip()]
        return f'{c(CITY, k)} {CUR} (דירות של {GROUP_HE[k]})'
    P.table('<th dir="rtl">שכירות שוק שנבדקה</th>',
            lambda old: table_cell_swap(old, 3, swap, f'שכר דירה חודשי ממוצע, אפריל עד יוני 2026 ({LMS})'),
            "A", 'replaced the listing-site rents by rooms (1: 3,368; 2: 4,896; 3: 6,486; 4: 7,736; 5: 10,209; 6+: 12,279) with the CBS Ramat Gan averages by size group, Q2 2026: 4,168 / 5,469 / 6,827 / 8,255 ש"ח; each cell names its group',
            "Rent column of the rooms table replaced by the CBS average monthly rent in Ramat Gan by size group, Q2 2026. The rows keep their exact room labels (the neighbouring columns are area and price range by room count), so 1 and 2 rooms both show the 1-2 group and 5 rooms and 6 rooms and up both show the 4.5+ group, each cell naming its group. Header names the CBS and the quarter.",
            keys_all(CITY, G4), url=RENT_URL)

    # --- area table: rent column out, one rent-level note out
    def areas(old):
        h, rows = parse_table(old)
        out = []
        for r in rows:
            feat = r[1]
            if r[0].strip() == "שיכון ותיקים":
                feat = "שוק שקט יותר"
            out.append([r[0], feat, r[3]])
        return rebuild(old, [h[0], h[1], h[3]], out)
    P.table('<th dir="rtl">שכירות חודשית שנצפתה</th>', areas, "C",
            'deleted the area rent column (14 values 4,350-11,890 ש"ח); in the Shikun Vatikim row "quiet market and relatively low rent" lost its rent clause; the other notes stay',
            "Area rents from market pages have no official counterpart (the CBS has no area rent). The rent column goes. 'A quiet market and a relatively low rent' (Shikun Vatikim) was a rent-level claim; it keeps 'a quieter market'. The price-feature and what-to-check columns are otherwise unchanged.")
    # --- rent section paragraph
    old = P.sub('לפי בדיקת נתוני שכירות מיוני 2026, החציון בעיר עמד סביב 6,000 ש"ח,', 'שוק ישראלי רחב יותר.')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע ברמת גן {Q2} היה {c(CITY)} {CUR}, לעומת {c("סך הכל")} {CUR} בממוצע הארצי, '
           'נתון שממחיש את הפער בין רמת גן לבין שוק ישראלי רחב יותר.')
    P.edit(old, new, "A", 'replaced the median 6,000, average 6,411, the 520-ad sample and the national median 4,400 with the CBS Ramat Gan average 5,894 and the CBS national average 5,086 ש"ח, Q2 2026',
           "Rent section: listing sample (median 6,000, average 6,411, 520 ads) and its national median (4,400) replaced by the CBS average monthly rent in Ramat Gan (5,893.8) against all of Israel (5,085.5), Q2 2026; the closing clause (the gap between Ramat Gan and the wider Israeli market) now stands on an official gap.",
           [key(CITY), key("סך הכל")], url=RENT_URL)

    # --- rent by rooms table (second)
    def rent_rooms(old):
        h, rows = parse_table(old)
        by = {r[0].strip(): r for r in rows}
        head = [h[0], f'שכר דירה חודשי ממוצע, אפריל עד יוני 2026 ({LMS})', h[2]]
        body = [
            ["1 עד 2 חדרים", f'{c(CITY, "1-2")} {CUR}', by["1 חדר"][2] + "; " + by["2 חדרים"][2]],
            ["2.5 עד 3 חדרים", f'{c(CITY, "2.5-3")} {CUR}', by["3 חדרים"][2]],
            ["3.5 עד 4 חדרים", f'{c(CITY, "3.5-4")} {CUR}', by["4 חדרים"][2]],
            ["4.5 חדרים ומעלה", f'{c(CITY, "4.5+")} {CUR}', by["5 חדרים"][2] + "; " + by["6 חדרים"][2]],
        ]
        return rebuild(old, body=body, head=head)
    P.table('<th dir="rtl">שכירות חודשית שנבדקה</th>', rent_rooms, "A",
            'rebuilt the rent-by-rooms table on the CBS Ramat Gan size groups (4,168 / 5,469 / 6,827 / 8,255 ש"ח, Q2 2026); six rows (1-6 rooms, 3,368-12,279) regrouped to four',
            "Rent-by-rooms table (six rows, ranges such as 4,600-4,896 and 10,000-10,209 from market pages) rebuilt on the CBS average monthly rent in Ramat Gan by size group, Q2 2026. 1 and 2 rooms merged into 1-2, 5 and 6 rooms into 4.5+; usage notes stay word for word, the merged pairs joined.",
            keys_all(CITY, G4), url=RENT_URL)
    # --- FAQ: family areas
    old = P.sub(' נתוני שכירות שנבדקו הציגו כ-9,090 ש"ח ברמת חן, כ-10,775 ש"ח ברמת אפעל וכ-11,890 ש"ח בקריניצי.')
    P.edit(old, '', "B", 'removed the area rents (Ramat Chen 9,090; Ramat Efal 10,775; Kiryat Krinitzi 11,890) from the FAQ answer',
           "FAQ: three area rents from market pages have no official counterpart; the sentence is removed and the answer keeps its hedged description and the advice to check a comparable deal.")
    # --- FAQ: Bursa
    old = P.sub(' נתון שכירות שנבדק באזור הבורסה עמד סביב 6,793 ש"ח.')
    P.edit(old, '', "B", 'removed the Bursa-area rent 6,793 from the FAQ answer',
           "FAQ: one area rent (6,793) with no official counterpart; the sentence is removed, the rest of the answer (employment, transport, towers, access roads) stays.")
    # --- FAQ: rent as a sense check
    old = P.sub('בעיקר כאשר השכירות בעיר סביב 6,000-6,411 ש"ח, אך מחיר רכישה')
    new = f'בעיקר כאשר משווים אותה לשכר הדירה הממוצע בעיר, {c(CITY)} {CUR} לפי {CBS_NAME} {Q2S}, אך מחיר רכישה'
    P.edit(old, new, "A", 'replaced the city rent 6,000-6,411 with the CBS Ramat Gan average 5,894 ש"ח (Q2 2026) in the FAQ answer',
           "FAQ 'does rent decide the price': 'city rent around 6,000-6,411' replaced by the CBS average monthly rent (5,893.8), Q2 2026.",
           [key(CITY)], url=RENT_URL)
