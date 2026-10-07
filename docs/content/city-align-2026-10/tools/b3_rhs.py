# -*- coding: utf-8 -*-
"""Tier 3, Ramat HaSharon (page 160). No CBS row (Ramat HaSharon is not in the CBS big-city list), so every listing-site rent is removed or deleted.
The page writes ש״ח and the Hebrew gershayim (U+05F4)."""
from b3lib import *

NOCBS = "The CBS table 4.9 has no Ramat HaSharon row (not in the big-city list) and no neighbourhood rents"
SH = "ש״ח"


def build(P):
    # --- body: public market data average rent
    old = P.sub(f' בבדיקת נתוני שוק פומביים שנקראו ביום 05.06.2026 הופיע ממוצע שכירות של כ-9,500 {SH}. מקור אחר הציג')
    new = ' בבדיקת נתוני שוק פומביים שנקראו ביום 05.06.2026 הוצג'
    P.edit(old, new, "B", 'removed the public-market average rent 9,500; "another source presented" became "public market data presented" so the average price that follows still has its source',
           f"Body: 'public market data read on 05.06.2026 showed an average rent of about 9,500'. {NOCBS}; the sentence goes. The next sentence ('another source presented an average flat price of about 4.15 million...') loses its 'another', since the rent source it was set against is gone.")
    # --- rent table by property type
    P.table('<th dir="rtl">שכירות חודשית שנצפתה</th>', lambda old: "", "C",
            'deleted the rent table (2 rooms 4,850-6,200; 3: 6,700-8,050; 4: 8,400-9,400; 5: 11,500-11,880; duplex, penthouse or garden flat 11,000-13,250; house 13,500) with its readings and warnings: private data, no official counterpart',
            f"A whole table of private rent ranges by property type with two columns of readings ('a segment for tenants who want a strong city at a lower price than a 4-room flat', 'a gap of 1,350 in monthly rent can change the check', 'family flats enjoy steady demand'...). {NOCBS}; the readings are level claims or warnings built on those numbers and have no content without them.")
    # --- seller's example
    old = P.sub(f'אם דירה מושכרת ב-9,000 {SH} בחודש ומבוקשת ב-4.6 מיליון {SH}')
    P.edit(old, f'אם דירה מושכרת ומבוקשת ב-4.6 מיליון {SH}', "B", 'removed the illustrative rent 9,000 a month from the seller example; the asking price 4.6 million stays',
           f"Seller example: 'a flat rented at 9,000 a month and asked at 4.6 million'. {NOCBS}; the rent goes, the example price is the page's own and stays.")
    # --- FAQ
    old = P.sub('ממוצע שכירות שנצפה עמד סביב 9,500', '8,400 עד 9,400 ש״ח ל-4 חדרים.')
    P.edit(old, 'שכר הדירה ברמת השרון משתנה לפי מספר החדרים, סוג הנכס ומצבו, ולכן כדאי לבדוק מודעות ועסקאות שכירות של נכסים דומים.', "B",
           'removed the FAQ rents (average 9,500; asking 11,750; by rooms 4,850-9,400); the answer says that rent varies by rooms, property type and condition and points to ads and rental deals of similar properties',
           f"FAQ 'how much is rent in Ramat HaSharon': the answer consisted of private figures. {NOCBS}. The question is a heading and stays; the answer becomes a hedged statement with no level claim.")
