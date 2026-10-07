# -*- coding: utf-8 -*-
"""Tier 3, Hod HaSharon (page 4558). No CBS row (Hod HaSharon is not in the CBS big-city list), so every listing-site rent is removed or deleted.
The page writes ש"ח and ASCII quotes."""
from b3lib import *

NOCBS = "The CBS table 4.9 has no Hod HaSharon row (not in the big-city list) and no neighbourhood rents"


def build(P):
    # --- 'common monthly rent' under its own heading
    old = P.sub('בדפי נתוני שוק שנבדקו הופיעו דמי שכירות ממוצעים סביב 7,500-9,100 ש"ח לדירות 4-5 חדרים, עם חריגים למעלה ולמטה לפי גודל, גיל ומיקום.')
    P.edit(old, 'שכר הדירה משתנה לפי גודל הדירה, גיל הבניין והמיקום.', "B", 'removed the market-page average rent 7,500-9,100 for 4-5 rooms; the paragraph under the heading now says only that rent varies by size, building age and location',
           f"The paragraph is the only text under its own heading ('common monthly rent'), so it is rewritten rather than deleted. {NOCBS}; the figure goes and what the sentence could still say without it (rent varies by size, age and location) stays.")

    # --- fact table: average observed rent
    def facts(old):
        h, rows = parse_table(old)
        return rebuild(old, None, [r for r in rows if r[0].strip() != "שכירות ממוצעת שנצפתה"])
    P.table('<th dir="rtl">טווח או נתון שנצפה</th>', facts, "C",
            'deleted the row "average observed rent about 7,900-8,500" from the fact table; the other rows are untouched',
            f"Fact table row 'average observed rent 7,900-8,500 a month, helps understand demand but does not replace a price check'. {NOCBS}; the whole row (figure and note) goes.")
    # --- rent paragraph
    old = P.sub('בהוד השרון הופיעו בדפי נתוני שוק שנבדקו דמי שכירות ממוצעים סביב 8,500 ש"ח לחודש,', 'הפער נובע מגודל, מיקום, גיל הבניין, מרפסת, חניה, ממ"ד ורמת גימור.')
    P.edit(old, 'השכירות בהוד השרון משתנה לפי מספר חדרים, גודל, מיקום, גיל הבניין, מרפסת, חניה, ממ"ד ורמת גימור.', "B",
           'removed the market-page average 8,500 and the ranges by rooms (3: 4,500-5,900; 4: 7,537-8,400; 5: 8,905-9,850); the sentence now lists what rent depends on',
           f"Rent paragraph: private average and per-room ranges. {NOCBS}; the figures go. The closing sentence (the gap comes from size, location, building age, balcony, parking, safe room and finish) becomes the plain statement that rent depends on those factors.")
    # --- rent by rooms table
    P.table('<th dir="rtl">דמי שכירות חודשיים שנצפו</th>', lambda old: "", "C",
            'deleted the rent-by-rooms table (1-2 rooms 4,094-6,000; 3: 4,500-5,900; 4: 7,537-8,400; 5: 8,905-9,850; 6: 10,373; 6+: 12,125) with its notes: private market pages, no official counterpart',
            f"A whole table of private rent ranges by rooms with two advice columns that comment on those ranges ('rent can indicate demand', 'high rent does not always justify a high price'). {NOCBS}; no content without the numbers. The paragraph that follows the table does not refer to it.")
