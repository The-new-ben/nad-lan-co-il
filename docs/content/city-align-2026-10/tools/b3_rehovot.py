# -*- coding: utf-8 -*-
"""Tier 3, Rehovot (page 4591). CBS row: רחובות (table 4.9, Q2 2026). The page writes ₪ and the Hebrew gershayim (U+05F4)."""
from b3lib import *

CITY = "רחובות"
CUR = "₪"
LMS = "הלמ״ס"
Q2S = Q2.replace(" (אפריל עד יוני)", "")


def build(P):
    sizes = by_size(CITY, CUR)
    KEYS = keys_all(CITY)
    G4 = ("1-2", "2.5-3", "3.5-4", "4.5+")
    # --- lead
    old = P.sub('בשכירות, דירת 2 חדרים מבוקשת סביב 3,300 ₪,', 'וממוצע סביב 4,987 ₪.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע ברחובות {Q2} היה {sizes}.'
    P.edit(old, new, "A", 'replaced the asking rents by rooms (2: 3,300; 3: 4,900; 4: 5,700; 5: 7,950) and the ad median 4,500 / average 4,987 with the CBS Rehovot averages by size group, Q2 2026: 3,281 / 4,171 / 5,102 / 6,555 ₪',
           "Lead: asking rents by room count and the ad-sample median (4,500) and average (4,987) replaced by the CBS average monthly rent in Rehovot by size group, Q2 2026 (table 4.9: 3,280.6; 4,171.0; 5,102.2; 6,554.8, rounded half up). The sentence that follows (so a price check starts with rooms, neighbourhood, building age...) stays.",
           keys_all(CITY, G4), url=RENT_URL)

    # --- rent table
    GROUP = {"2 חדרים": "1-2", "3 חדרים": "2.5-3", "4 חדרים": "3.5-4", "5 חדרים": "4.5+"}

    def rent_table(old):
        h, rows = parse_table(old)
        head = [h[0], f'שכר דירה חודשי ממוצע, אפריל עד יוני 2026 ({LMS})', "מה משפיע על השכירות", h[3]]
        body = []
        for r in rows:
            lab = r[0].strip()
            if lab in GROUP:
                k = GROUP[lab]
                infl = "משתנה לפי מיקום ומצב הדירה" if lab == "3 חדרים" else r[2]
                body.append([r[0], f'{c(CITY, k)} {CUR} (דירות של {GROUP_HE[k]})', infl, r[3]])
            else:  # all flats in the ads
                body.append(["כלל הדירות בעיר", f'{c(CITY)} {CUR}', "משתנה לפי גודל הדירה, מיקום ומצב", r[3]])
        return rebuild(old, head, body)
    P.table('<th dir="rtl">חציון או אומדן נוסף</th>', rent_table, "A",
            'rebuilt the rent table on the CBS Rehovot averages (size groups 3,281 / 4,171 / 5,102 / 6,555 and all flats 4,943 ₪, Q2 2026); removed the ad figures (3,300-7,950, 5,425, median 4,500, average 4,987, 3-room median 4,814)',
            "Rent table: the asking-rent column (3,300; 4,900; 5,700; 7,950; all flats 5,425) becomes the CBS average monthly rent in Rehovot, Q2 2026 (each cell names its size group; the last row is the city average). The second column held a 3-room median (4,814) and a sample median/average (4,500 / 4,987): the two numeric cells become hedged 'varies by...' texts, the three hedged cells stay, and the header becomes 'what affects the rent'. The usage column is unchanged.",
            KEYS, url=RENT_URL)
    # --- paragraph on the 97-ad sample
    old = P.sub('נתוני שכירות ממודעות אינם חוזים סגורים. במדגם אחד של 97 מודעות פעילות', 'על כל השכונה.')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע ברחובות {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, לעומת {c("סך הכל")} {CUR} בממוצע הארצי. '
           'מודעת שכירות אחת או שתיים אינן מייצגות שכונה שלמה.')
    P.edit(old, new, "A", 'replaced the 97-ad sample (median 4,500, average 4,987, 3-room median 4,814, national median 4,400, extreme ads 1,920 and 10,200) with the CBS Rehovot average 4,943 and the CBS national average 5,086 ₪, Q2 2026',
           "The paragraph on a 97-ad sample (city median 4,500, average 4,987, 3-room median 4,814 against a national 4,400, and two extreme neighbourhood ads, 1,920 and 10,200) replaced by the CBS average monthly rent in Rehovot (4,942.5) against all of Israel (5,085.5), Q2 2026. The advice that one or two ads do not represent a whole neighbourhood stays in a shorter form.",
           [key(CITY), key("סך הכל")], url=RENT_URL)
    # --- FAQ
    old = P.sub('שכירות מבוקשת עומדת סביב 3,300 ₪ לדירת 2 חדרים,', 'ולכן יש לבדוק דירות מושכרות בפועל.')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע ברחובות {Q2} היה {c(CITY)} {CUR} בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}. '
           'כדאי לבדוק גם דירות מושכרות בפועל.')
    P.edit(old, new, "A", 'replaced the FAQ asking rents (3,300 / 4,900 / 5,700 / 7,950; median 4,500, average 4,987) with the CBS Rehovot averages for all flats and by size group, Q2 2026',
           "FAQ 'how much rent in Rehovot': ad-site asking rents and the sample median/average replaced by the CBS averages for all flats (4,942.5) and by size group, Q2 2026. 'These are ads, not signed contracts, so check flats actually rented' is no longer about ads; it becomes the plain advice to also check flats actually rented.",
           KEYS, url=RENT_URL)
