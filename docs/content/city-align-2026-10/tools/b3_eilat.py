# -*- coding: utf-8 -*-
"""Tier 3, Eilat (page 4597). No CBS row (Eilat is not in the CBS big-city list), so every listing-site rent is removed or deleted.
The page writes ₪ and ASCII quotes."""
from b3lib import *

NOCBS = "The CBS table 4.9 has no Eilat row (not in the big-city list) and no neighbourhood rents"


def build(P):
    # --- lead
    old = P.sub('הצביעו על מאות נכסים מוצעים למכירה, ועל שכר דירה מבוקש שמתחיל סביב 3,100 ₪ בדירות 2 חדרים ומגיע גם לכ-8,850 ₪ בדירות 5 חדרים.')
    P.edit(old, 'הצביעו על מאות נכסים מוצעים למכירה.', "B", 'removed the asking rents 3,100 (2 rooms) to 8,850 (5 rooms) from the lead',
           f"Lead: asking rents from supply data (3,100 to 8,850). {NOCBS}, so the clause goes and the supply remark stays.")
    # --- rent layer paragraph
    old = P.sub('נתוני מודעות שכירות עדכניים מסוף מאי 2026', 'דירות נופש ודירות רגילות.')
    new = 'השכירות משתנה לפי סוג הנכס, מיקום, ריהוט, עונתיות, דירות נופש ודירות רגילות.'
    P.edit(old, new, "B", 'removed all rent figures from the paragraph (188 ads, average 4,486, median 3,585, minimum 530; second source average 3,500, yield 6.1%, 3,100 / 3,900 / 6,250 / 8,850); the remark that rent differs by property type, location, furnishing and season stays in general form',
           f"The paragraph consisted of private rent figures: an ad sample (188 ads; 4,486; 3,585; 530) and a second source (3,500; yield 6.1%; by rooms). {NOCBS}. The opening sentence stays; the closing sentence (why sources differ) becomes the plain remark that rent varies by property type, location, furnishing, season, holiday flats and regular flats.")
    # --- caution paragraph: average and median
    old = P.sub('לכן שכר דירה ממוצע של 4,486 ₪ וחציון של 3,585 ₪ אינם עונים לבד על השאלה כמה שווה דירה. הם מסייעים')
    P.edit(old, 'לכן שכר דירה ממוצע או חציוני אינו עונה לבד על השאלה כמה שווה דירה. הוא מסייע', "B", 'removed the average 4,486 and the median 3,585 from the caution paragraph',
           f"{NOCBS}; the two private figures go and the sentence reads in the singular.")
    # --- area rents paragraph
    P.delete_para('מקור מודעות שכירות עדכני מסוף מאי 2026 הציג 188 מודעות באילת',
                  'deleted the paragraph with the Eilat average 4,486, median 3,585, minimum 530 and 14 area averages (Shahamon 7,087 ... the hotels 6,500) from a private ad source',
                  f"A whole paragraph of private rent figures (188 ads, city average and median, 14 areas). {NOCBS}; the paragraph has no content without the numbers.")
    # --- area rent table
    P.table('<th dir="rtl">שימוש נכון בנתון</th>', lambda old: "", "C",
            'deleted the table of the Eilat average and 12 area averages with ad counts (4,486 / 3,585; Shahamon 7,087 ... the hotels 6,500): private ad data, no official counterpart',
            f"A whole table of private rent figures (the city and 12 areas, 1-35 ads each) with notes that only comment on the rent level or the sample size. {NOCBS}; no content without the numbers.")
    # --- second source by rooms
    old = P.sub('מקור נוסף הציג שכר דירה לפי חדרים: 2 חדרים סביב 3,100 ₪, 3 חדרים סביב 3,900 ₪, 4 חדרים סביב 6,250 ₪, ו-5 חדרים סביב 8,850 ₪. ')
    P.edit(old, '', "C", 'deleted the sentence with the second-source rents by rooms (3,100 / 3,900 / 6,250 / 8,850); the advice on reconciling different rent sources stays',
           f"{NOCBS}. The sentence only listed the private rents; the next sentences (do not pick one number by convenience; check date, property type, source, actual vs estimated rent, fit of the sample) stay.")
    # --- rent by rooms table
    P.table('<th dir="rtl">שכר דירה לפי מקור ביקוש עדכני</th>', lambda old: "", "C",
            'deleted the table of rent by rooms (2 rooms 3,100; 3 rooms 3,900; 4 rooms 6,250; 5 rooms 8,850) with its messages to the buyer: private source, no official counterpart',
            f"Rent by rooms from a private demand source. {NOCBS}. The messages beside the numbers ('different sample can change the picture completely', 'check active ads') refer to that sample and have no content without it.")
    # --- buyer's four numbers
    old = P.sub('אם דמי השכירות הצפויים הם 3,900 ₪ בלבד ולא 6,250 ₪, החישוב משתנה שוב.')
    P.edit(old, 'אם דמי השכירות הצפויים נמוכים מהמצופה, החישוב משתנה שוב.', "B", 'removed the two illustrative rents 3,900 and 6,250',
           f"Two private rent figures (3,900 and 6,250) used as an example. {NOCBS}; the numbers go and the point (a lower expected rent changes the calculation) stays.")
    # --- yield from one source
    old = P.sub('תשואה ממוצעת של 6.1% במקור אחד יכולה להיראות אטרקטיבית,')
    P.edit(old, 'תשואה שמוצגת במקור אחד יכולה להיראות אטרקטיבית,', "B", 'removed the private-source yield 6.1% (built on private rents)',
           f"A yield of 6.1% from one private source, computed from the private rents. {NOCBS}; the number goes and the caution that follows stays.")
    # --- FAQ
    old = P.sub('נתוני שכירות שונים הציגו ממוצע כללי של 4,486 ₪ וחציון 3,585 ₪,', '8,850 ₪ לדירת 5 חדרים. ')
    P.edit(old, '', "C", 'deleted the FAQ sentence with the average 4,486, the median 3,585 and the rents by rooms (3,100 / 3,900 / 6,250 / 8,850)',
           f"FAQ 'does the rent in Eilat justify a high purchase price': the sentence only listed private rent figures. {NOCBS}. The answer keeps 'sometimes yes and sometimes no' and the list of what to calculate (net income, vacant months, renovation, maintenance, tax, financing, management fees).")
