# -*- coding: utf-8 -*-
"""Tier 3, Beer Sheva (page 4589). CBS row: באר שבע (table 4.9, Q2 2026). The page writes ₪ and the Hebrew gershayim (U+05F4)."""
from b3lib import *

CITY = "באר שבע"
CUR = "₪"
LMS = "הלמ״ס"
Q2S = Q2.replace(" (אפריל עד יוני)", "")


def build(P):
    sizes = by_size(CITY, CUR)
    KEYS = keys_all(CITY)
    G4 = ("1-2", "2.5-3", "3.5-4", "4.5+")
    # --- lead
    old = P.sub('בשכירות, המחיר המבוקש במודעות נע לרוב מכ-2,300 ₪ לדירת 2 חדרים,', 'וכ-4,750-5,740 ₪ לדירת 5 חדרים.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בבאר שבע {Q2} היה {sizes}.'
    P.edit(old, new, "A", 'replaced the asking rents by rooms (2: 2,300; 3: 2,600-2,760; 4: 3,170-3,640; 5: 4,750-5,740) with the CBS Beer Sheva averages by size group, Q2 2026: 2,321 / 2,788 / 3,501 / 4,908 ₪',
           "Lead: asking rents by room count from ad sites replaced by the CBS average monthly rent in Beer Sheva by size group, Q2 2026 (table 4.9: 2,321.3; 2,787.8; 3,500.8; 4,907.9, rounded half up).",
           keys_all(CITY, G4), url=RENT_URL)
    # --- body: median, average, listing count, 3-room asking rent
    old = P.sub('חציון שכירות של כ-2,600 ₪ בחודש, מחיר ממוצע של כ-3,003 ₪ ו-628 מודעות פעילות במועד בדיקה אחד', 'סביב 2,759 ₪ אינה בהכרח')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בבאר שבע {Q2} היה {c(CITY)} {CUR}, והוא מלמד על רף ביקוש. '
           f'דירת 3 חדרים שמושכרת בשכר הדירה הממוצע של {LMS} לדירות של 2.5 עד 3 חדרים באותו רבעון, {c(CITY, "2.5-3")} {CUR}, אינה בהכרח')
    P.edit(old, new, "A", 'replaced the ad-site median 2,600, average 3,003, the 628-ad count and the 3-room asking rent 2,759 with the CBS Beer Sheva average 3,183 ₪ and the 2.5-3 rooms average 2,788 ₪, Q2 2026',
           "Body: ad-sample median (2,600), average (3,003), its 628-ad count and a 3-room asking rent (2,759) replaced by the CBS average monthly rent in Beer Sheva (3,182.9) and for 2.5-3 rooms (2,787.8), Q2 2026. The remark 'an active ad is not a closed deal' was about the ad data and goes with it; the rest of the sentence (vacancy, repairs, building committee, tax, interest, competition) stays.",
           [key(CITY), key(CITY, "2.5-3")], url=RENT_URL)

    # --- rent-by-rooms table
    def rooms(old):
        h, rows = parse_table(old)
        by = {r[0].strip(): r for r in rows}
        head = [h[0], f'שכר דירה חודשי ממוצע, אפריל עד יוני 2026 ({LMS})', h[4]]
        body = [
            ["1 עד 2 חדרים", f'{c(CITY, "1-2")} {CUR}', by["חדר אחד"][4] + "; " + by["2 חדרים"][4]],
            ["2.5 עד 3 חדרים", f'{c(CITY, "2.5-3")} {CUR}', by["3 חדרים"][4]],
            ["3.5 עד 4 חדרים", f'{c(CITY, "3.5-4")} {CUR}', by["4 חדרים"][4]],
            ["4.5 חדרים ומעלה", f'{c(CITY, "4.5+")} {CUR}', by["5 חדרים"][4] + "; " + by["6 חדרים"][4]],
        ]
        return rebuild(old, head, body)
    P.table('<th dir="rtl">חציון שכירות לפי מקור נוסף</th>', rooms, "A",
            'rebuilt the rent table on the CBS Beer Sheva size groups (2,321 / 2,788 / 3,501 / 4,908 ₪, Q2 2026); the three private-source rent columns (asking, median, working range) deleted; rows regrouped to the CBS groups',
            "Rent table (three columns from private sources: asking, median, 'working range'; 1,800-6,427) rebuilt on the CBS average monthly rent in Beer Sheva by size group, Q2 2026. Rows regrouped to the CBS groups (1 room + 2 rooms, 5 rooms + 6 rooms); the usage notes stay word for word, the merged pairs joined.",
            keys_all(CITY, G4), url=RENT_URL)
    # --- neighbourhood rents
    P.delete_para('ברמת שכונות, חציון שכירות של כ-2,366',
                  'deleted the paragraph with 11 neighbourhood rent medians (Gimel 2,672, Dalet 2,479, Ramot 3,971, Ramot B 5,244, Park HaNahal 5,313, Neve Zeev 5,377 and others): the CBS publishes no neighbourhood rent',
                  "A whole paragraph of neighbourhood rent medians from private data. The CBS publishes rent for the city and its size groups only, so there is nothing to replace them with and the paragraph (a reading of demand drawn from those numbers) has no content without them.")
    old = P.sub('אם חציון שכירות בפארק הנחל סביב 5,313 ₪ ובנווה זאב סביב 5,377 ₪, אין להשוות אותן ישירות לדירת 3 חדרים בשכונה ג סביב 2,672 ₪ בלי לנרמל מספר חדרים, שטח וקהל יעד.')
    new = 'אין להשוות ישירות שכירות של דירה בפארק הנחל או בנווה זאב לשכירות של דירת 3 חדרים בשכונה ג בלי לנרמל מספר חדרים, שטח וקהל יעד.'
    P.edit(old, new, "B", 'removed the neighbourhood rents (Park HaNahal 5,313, Neve Zeev 5,377, Gimel 2,672); the caution to normalise rooms, size and target group stays',
           "Neighbourhood rents from private data, no official counterpart: removed. The advice (do not compare across neighbourhoods without normalising rooms, size and target group) is kept as a plain caution.")
    # --- FAQ
    old = P.sub('חציון שכירות עירוני סביב 2,600 ₪ וממוצע סביב 3,003 ₪. דירות 2 חדרים נעות סביב', 'השכירות יכולה להיות גבוהה יותר בגלל תמהיל דירות גדול.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בבאר שבע {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}.'
    P.edit(old, new, "A", 'replaced the FAQ rents (median 2,600, average 3,003, by rooms 2,200-5,738) with the CBS Beer Sheva averages for all flats and by size group, Q2 2026; deleted the unsourced remark that rent is higher in Neve Zeev, Park HaNahal and Ramot B',
           "FAQ 'how much rent in Beer Sheva': ad-sample median and average and the per-room ranges replaced by the CBS averages for all flats (3,182.9) and by size group, Q2 2026. The closing sentence (rent can be higher in Neve Zeev, Park HaNahal and Ramot B because of a large-flat mix) is a neighbourhood level claim with no official figure and is deleted.",
           KEYS, url=RENT_URL)
