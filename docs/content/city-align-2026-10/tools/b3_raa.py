# -*- coding: utf-8 -*-
"""Tier 3, Raanana (page 167). No CBS row (Raanana is not in the CBS big-city list), so every listing-site rent is removed or deleted.
The page writes ₪ and ASCII quotes."""
from b3lib import *

NOCBS = "The CBS table 4.9 has no Raanana row (not in the big-city list) and no neighbourhood rents"


def build(P):
    # --- Merkaz Darom in the body: rent and the demand reading drawn from it
    old = P.sub(' ושכירות ממוצעת סביב 9,600 ₪. המספרים האלה מסמנים ביקוש חזק, אך הם אינם אומרים')
    P.edit(old, '. המספר הזה אינו אומר', "B", 'removed the Merkaz Darom rent 9,600 and "these numbers indicate strong demand"; the average purchase price and the caution that it does not price every flat stay',
           f"Body: a neighbourhood rent (Merkaz Darom, 9,600) and the reading 'these numbers mark strong demand'. {NOCBS}; the rent goes and so does the demand reading drawn from it (a level claim without an official figure). The purchase-price part is a sale figure left by tier 1.")

    # --- area table: Merkaz Darom row
    def areas(old):
        return old.replace("דיווחי שוק סביב כ-3.68 מיליון ₪ בממוצע וכ-9,600 ₪ שכירות ממוצעת", "דיווחי שוק סביב כ-3.68 מיליון ₪ בממוצע")
    P.table('<th dir="rtl">למי זה רלוונטי</th>', areas, "B",
            'removed the rent 9,600 from the Merkaz Darom row of the area table; the average purchase price in the same cell stays',
            f"Area table, Merkaz Darom row: 'market reports around 3.68 million on average and an average rent of about 9,600'. {NOCBS}; the rent goes, the sale figure (as tier 1 left it) stays.")
    # --- rent paragraph
    old = P.sub(' לפי נתוני שוק שנקראו, שכירות חציונית ברעננה עמדה סביב כ-8,000 ₪ במאי 2026', 'לא תחליף לבדיקה של דירה מסוימת.')
    P.edit(old, ' שכירות בפועל משתנה לפי סוג הדירה והאזור, והיא אינה תחליף לבדיקה של דירה מסוימת.', "B",
           'removed the median 8,000 (52 ads), the levels 7,257 / 8,559 / 10,959 and the Merkaz Darom rent 9,600; the paragraph keeps its first sentence and says that rent varies by flat type and area',
           f"Rent paragraph: private rent figures (median 8,000 on 52 ads; 7,257; 8,559; 10,959; 9,600 for Merkaz Darom). {NOCBS}. The opening sentence (rent helps test whether a price is reasonable) stays; the closing sentence keeps its point without 'these are context data'.")
    old = P.sub('אבל דירות דומות מושכרות סביב 7,500-8,500 ₪,')
    P.edit(old, 'אבל דירות דומות מושכרות בשכר נמוך יחסית למחיר הזה,', "B", 'removed the illustrative rent range 7,500-8,500 for a 4-room flat offered at 3,700,000',
           f"Worked example (4-room flat offered at 3,700,000): 'similar flats rent around 7,500-8,500' sits in the private data range. {NOCBS}; the range goes and the case is stated in words.")
    old = P.sub('מושכרת סביב 10,000-11,000 ₪ ויש ביקוש יציב')
    P.edit(old, 'מושכרת בשכר גבוה ויש ביקוש יציב', "B", 'removed the illustrative rent range 10,000-11,000 for a 5-room flat',
           f"Worked example (5-room flat): 'rented around 10,000-11,000' sits in the private data range. {NOCBS}; the range goes and the case is stated in words.")
    # --- rent-levels table
    P.table('<th dir="rtl">סוג נתון שכירות</th>', lambda old: "", "C",
            'deleted the table of rent levels (median 8,000 on 52 ads; 7,257 / 8,559 / 10,959 market reports; Merkaz Darom 9,600) with its readings: private data, no official counterpart',
            f"A whole table of private rent levels with readings of what each level 'means' (lower level suits small or old flats, higher level may reflect large or new flats...). {NOCBS}; the readings are level claims that rested on those numbers and have no content without them.")
    # --- FAQ
    old = P.sub('שכירות סביב 8,000 ₪ בחציון עירוני, נתוני שוק סביב 7,257 ₪, 8,559 ₪ ו-10,959 ₪, ושכירות ממוצעת סביב 9,600 ₪ באזור מרכז דרום, נותנים הקשר לביקוש.')
    P.edit(old, 'שכירות נותנת הקשר לביקוש.', "B", 'removed the FAQ rents (median 8,000; 7,257 / 8,559 / 10,959; Merkaz Darom 9,600); the answer keeps "rent gives context for demand" and the caution that follows',
           f"FAQ 'does rent help understand the price of a flat in Raanana': the figures go. {NOCBS}. 'Yes, rent gives context for demand. However rent does not set the price alone...' stays.")
