# -*- coding: utf-8 -*-
"""Tier 3, Givatayim (page 4571). No CBS row (Givatayim is not in the CBS big-city list), so every listing-site rent is removed or deleted.
The page writes ש"ח and ASCII quotes."""
from b3lib import *

NOCBS = "The CBS table 4.9 has no Givatayim row (not in the big-city list) and no neighbourhood rents"


def build(P):
    # --- lead
    old = P.sub('גם שכירות חציונית במודעות, סביב 6,000 ש"ח לחודש, עוזרת לבדוק')
    P.edit(old, 'גם שכירות עוזרת לבדוק', "B", 'removed the listing median rent 6,000 from the lead',
           f"Lead: 'a median rent in the ads, around 6,000 a month'. {NOCBS}; the number goes and the sentence keeps its point (a rent check helps test the price).")
    # --- control points
    old = P.sub('שכירות חציונית סביב 6,000 ש"ח, דירות 3 חדרים סביב 6,391 ש"ח ומחיר למ"ר סביב 31,856-42,000 ש"ח הם נקודות בקרה,')
    P.edit(old, 'מחיר למ"ר סביב 31,856-42,000 ש"ח הוא נקודת בקרה,', "B", 'removed the median rent 6,000 and the 3-room rent 6,391 from the control points; the price per m2 (not a rent) stays',
           f"Control points: median rent 6,000, 3-room rent 6,391 and a price per m2. {NOCBS}; the two rents go, the price per m2 stays as the tier-1 text had it, and the sentence reads in the singular.")

    # --- fact table: median rent row
    def facts(old):
        h, rows = parse_table(old)
        return rebuild(old, None, [r for r in rows if r[0].strip() != "שכירות חציונית"])
    P.table('<th dir="rtl">אינדיקציה מספרית</th>', facts, "C",
            'deleted the row "median rent about 6,000" from the fact table; the four sale rows are untouched',
            f"Fact table row 'median rent about 6,000, a sanity check for pricing, especially for 2-4 room flats'. {NOCBS}; the whole row (figure and note) goes.")

    # --- area table: City row is all about rent
    def areas(old):
        h, rows = parse_table(old)
        return rebuild(old, None, [r for r in rows if r[0].strip() != "סיטי"])
    P.table('<th dir="rtl">אינדיקציית מחיר שנצפתה</th>', areas, "C",
            'deleted the "City" row ("expensive rent around 10,450 in an expensive area") from the area table; the other twelve rows are untouched',
            f"The City row held no sale figure: its cells were a rent-level claim (expensive rent around 10,450), 'requires checking the flat mix' and 'do not infer from high rent alone'. {NOCBS}; no content without the number, so the row goes. The area is still named in the lead and in the comparison table.")
    # --- rent paragraph: keep the first sentence only
    old = P.sub(' לפי דף שכירות ייעודי שנבדק ביוני 2026, שכירות חציונית בעיר עמדה סביב 6,000 ש"ח,', 'וכ-10,350 ש"ח ל-5 חדרים.')
    P.edit(old, '', "C", 'deleted the two sentences with the city median 6,000 (293 ads), the 3-room average 6,391 and the indications 5,580 / 6,150 / 7,500 / 10,350',
           f"Rent paragraph: the opening sentence (rent is a good sanity check, especially for 2-4 room flats) stays; the two sentences of private rent figures go. {NOCBS}.")
    # --- rent table: all private
    P.table('<th dir="rtl">סוג בדיקת שכירות</th>', lambda old: "", "C",
            'deleted the rent table (city median 6,000; 293 ads; 2-5 rooms 5,580-10,350; Shenkin 5,393; City 10,450): private ad data, no official counterpart',
            f"A whole table of private rent figures (city, rooms, two areas) with notes that comment on them. {NOCBS}; no content without the numbers.")
    # --- FAQ: Shenkin
    old = P.sub(', ובמקביל כאזור שכירות זול יחסית בדף שכירות מסוים סביב 5,393 ש"ח. המשמעות היא שצריך')
    P.edit(old, '. לכן צריך', "B", 'removed the Shenkin area rent 5,393 ("relatively cheap rent") from the FAQ answer; the advice to check flat type and comparable deals stays',
           f"FAQ 'is Shenkin cheap or expensive': {NOCBS}. The rent clause goes; 'the meaning is that one must check' becomes 'so one must check', since the contrast it rested on is gone.")
