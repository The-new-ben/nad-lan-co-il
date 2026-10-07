# -*- coding: utf-8 -*-
"""Tier 3, Modiin (page 4555). No CBS row (Modiin is not in the CBS big-city list), so every listing-site rent is removed or deleted.
The page writes the word שקל and ASCII quotes."""
from b3lib import *

NOCBS = "The CBS table 4.9 has no Modiin row (not in the big-city list) and no neighbourhood rents"


def build(P):
    # --- fact table: three rows built on the listing sites' rent
    def facts(old):
        h, rows = parse_table(old)
        drop = ("שכר דירה ממוצע", "שכר דירה מבוקש ממוצע", "תשואה עירונית ממוצעת")
        return rebuild(old, None, [r for r in rows if r[0].strip() not in drop])
    P.table('<th dir="rtl">מקור ותאריך</th>', facts, "C",
            'deleted three rows from the quick-index table: average rent 7,600, asking rent 7,200 and average city yield 2.9% (listing sites, read 5.6.2026); the sale median, price per m2 and listing-count rows are untouched',
            f"Quick-index table: the rows 'average rent 7,600' (a real-estate data site), 'asking rent 7,200' and 'average city yield 2.9%' (a listing site). {NOCBS}; the yield was computed from those rents. The three rows (figure, source and reading) go.")
    # --- rooms paragraph: rents by rooms
    old = P.sub('הציג שכר דירה לפי חדרים: סביב 6,200 שקל לדירת 3 חדרים, 6,950 שקל לדירת 4 חדרים ו-8,500 שקל לדירת 5 חדרים, ובדירות 6 חדרים מחיר')
    P.edit(old, 'הציג בדירות 6 חדרים מחיר', "B", 'removed the rents by rooms (3: 6,200; 4: 6,950; 5: 8,500) from the sentence; the 6-room sale prices that follow stay',
           f"Paragraph before the sale-median table: rents by room count from a data site. {NOCBS}; the rents go, the 6-room sale prices (not rent, left by tier 1) and the lead-in to the table stay.")
    # --- rent section: average rent, asking rent, yield
    old = P.sub(' לפי אתר נתוני נדל"ן, שנקרא ביום 5.6.2026, שכר הדירה הממוצע בעיר עמד על 7,600 שקל.', 'הוצגה כ-2.9%.')
    P.edit(old, '', "C", 'deleted the two sentences with the average rent 7,600, the asking rent 7,200 and the average city yield 2.9% (read 5.6.2026)',
           f"Rent section: two sentences of listing-site figures (average rent 7,600; asking rent 7,200; yield 2.9%). {NOCBS}; the yield was computed from those rents. The opening sentences (who uses the rent and why) stay.")
    old = P.sub('בטבלת החדרים של האתר הראשון הוצגו נתוני שכירות נקודתיים:', 'המשמעות היא שדירה משפחתית')
    P.edit(old, 'דירה משפחתית', "B", 'removed the sentence with the rents by rooms (3: 6,200; 4: 6,950; 5: 8,500); "the meaning is that a regular family flat" became "a regular family flat"',
           f"The sentence listed rents from a data site's table. {NOCBS}. The conclusion that follows (a regular family flat is judged by purchase price and by its rentability, vacancy, tenant quality, fees, repairs, insurance, mortgage and tax) does not depend on the numbers and stays; its opening 'the meaning is that' goes with the sentence it referred to.")
    # --- the rent table: monthly and annual rent columns and the city-average row
    P.table('<th dir="rtl">שכר דירה חודשי לפי אתר נתוני נדל"ן</th>', lambda old: "", "C",
            'deleted the rent-by-rooms table (monthly rent 6,200 / 6,950 / 8,500, annual rent 74,400 / 83,400 / 102,000, asking average 7,200 and 86,400): listing-site rents and the annual figures derived from them',
            f"Rent table: its two rent columns (monthly and annual, the annual being 12 times the monthly) and its city-average row are listing-site data. {NOCBS}. What is left would repeat the sale medians that the rooms table above already shows (3 rooms 2,039,500, 4 rooms 2,559,800, 5 rooms 3,648,800 with their quarters), so the table goes whole.")
    # --- FAQ: 4-room flat
    old = P.sub(', ואתר נתוני נדל"ן אחר הציג באותו מועד שכר דירה סביב 6,950 שקל.')
    P.edit(old, '.', "B", 'removed the 4-room rent 6,950 from the FAQ answer; the asking price per m2 and the advice stay',
           f"FAQ 'what does a 4-room flat in Modiin cost': a rent of 6,950 from a data site. {NOCBS}; the clause goes.")
    # --- FAQ: what is the rent in Modiin
    old = P.sub('אתר נתוני נדל"ן, שנקרא ביום 5.6.2026, הציג שכר דירה ממוצע של 7,600 שקל.', 'ודירת 5 חדרים סביב 8,500 שקל.')
    P.edit(old, 'שכר הדירה במודיעין משתנה לפי מספר החדרים, השכונה ומצב הדירה, ולכן כדאי לבדוק מודעות ועסקאות שכירות של דירות דומות.', "B",
           'removed the FAQ rents (average 7,600; asking 7,200; by rooms 6,200 / 6,950 / 8,500); the answer says that rent varies by rooms, neighbourhood and condition and points to ads and rental deals of similar flats',
           f"FAQ 'what is the rent in Modiin': the answer consisted of listing-site figures. {NOCBS}. The question is a heading and stays; the answer becomes a hedged statement that makes no level claim.")

    # --- users table: the 2.9% yield
    def users(old):
        return old.replace("לבנות חישוב נטו ולא רק תשואה ממוצעת של 2.9%", "לבנות חישוב נטו ולא רק תשואה ממוצעת")
    P.table('<th dir="rtl">פעולה מומלצת</th>', users, "B",
            'removed the listing-site yield 2.9% from the investor row of the users table; the advice to build a net calculation stays',
            f"Users table, investor row: 'build a net calculation and not only an average yield of 2.9%'. The 2.9% is a listing-site yield computed from asking rents. {NOCBS}; the figure goes and the advice stays.")
