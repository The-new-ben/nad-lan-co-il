# -*- coding: utf-8 -*-
"""Tier 3, Ashkelon (page 4593). CBS row: אשקלון (table 4.9, Q2 2026)."""
from b3lib import *

CITY = "אשקלון"
Q2S = Q2.replace(" (אפריל עד יוני)", "")


def build(P):
    sizes = by_size(CITY)
    KEYS = keys_all(CITY)
    # --- lead
    old = P.sub('בשכירות, נקודת האמצע העירונית במודעות עומדת סביב 3,500 ש"ח בחודש, ובדירות גדולות או חדשות השכירות גבוהה יותר.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע באשקלון {Q2} היה {sizes}.'
    P.edit(old, new, "A", 'replaced the listing-site city rent midpoint 3,500 with the CBS Ashkelon averages by size group, Q2 2026: 2,740 / 3,261 / 4,031 / 4,906 ש"ח',
           "Lead: the listing midpoint 3,500 (and the unsourced 'bigger or newer flats rent higher') replaced by the CBS average monthly rent in Ashkelon by size group, Q2 2026 (table 4.9: 2,739.9; 3,260.8; 4,031.3; 4,905.7); the size groups themselves show the rise with size.",
           KEYS, url=RENT_URL)
    # --- body: listing counts and private rents
    old = P.sub('לצד שכירות מבוקשת ממוצעת סביב 3,500 ש"ח בחודש במקור אחד,', 'מושכות את הממוצע כלפי מעלה.')
    new = f'ולפי {CBS_NAME}, שכר הדירה החודשי הממוצע בעיר {Q2} היה {c(CITY)} ש"ח.'
    P.edit(old, new, "A", 'replaced the private rent figures (average 3,500, median 3,500 from 279 ads, average 4,130) and the median-vs-average remark with the CBS Ashkelon average 3,698 ש"ח, Q2 2026',
           "Body: asking-rent average and median (3,500), the 279-ad sample, its average (4,130) and the remark built on the gap between them replaced by the CBS average monthly rent in Ashkelon (3,697.9), Q2 2026. The sentence that follows ('so a buyer should not settle for one city number') stays.",
           [key(CITY)], url=RENT_URL)
    # --- neighbourhood rents paragraph: all neighbourhood figures
    P.delete_para('הפערים ניכרים גם בשכירות. מדגם מודעות עדכני הציג מדיאן שכירות',
                  'deleted the paragraph with 9 neighbourhood rent medians (Barnea 3,209, Afridar 4,233, Agamim 4,980, Marina 5,053, Ir HaYayin 5,287, S.Y. Agnon 2,300, Ben Gurion 2,731, Jabotinsky 2,858, Neve Yam 2,918): the CBS publishes no neighbourhood rent',
                  "A whole paragraph of neighbourhood rent medians from a private ad sample. The CBS publishes rent for the city and its size groups only, so there is nothing to replace them with and the paragraph has no content without the numbers. The paragraph before and after it do not refer to it.")
    # --- neighbourhood paragraph above the table
    old = P.sub('בצד השכירות, מדדי מודעות מאפשרים לראות את יחס הביקוש. לדוגמה,', 'ששווי המכירה גבוה באותו שיעור. לשווי מכירה נכנסים גם')
    P.edit(old, 'לשווי מכירה נכנסים', "C", 'deleted the two sentences with neighbourhood rent medians (Ir HaYayin 5,287, Marina 5,053, Agamim 4,980) and the demand reading drawn from them; the sentence on what enters a sale value stays',
           "Neighbourhood rent medians (5,287, 5,053, 4,980) and the inference 'may indicate demand for new flats' have no official counterpart; deleted. The last sentence (land price, building age, project supply, delivery date, legal status, payment terms) is general and stays, with its 'also' dropped so it reads on its own.")
    # --- neighbourhood table: rent column and the price-signal column (derived from the rent level) go
    def hood(old):
        h, rows = parse_table(old)
        return rebuild(old, [h[0], h[3]], [[r[0], r[3]] for r in rows])
    P.table('<th dir="rtl">מדיאן שכירות שנצפה</th>', hood, "C",
            'deleted the neighbourhood rent column (9 values 2,731-5,500) and the price-signal column that restated the rent level; area and what-to-check columns stay',
            "Neighbourhood rent medians from private ads have no official counterpart (the CBS has no neighbourhood rent). The 'price signal' column (sea premium, accessible market, expectation of price...) read the rent level into each area and is a level claim without an official figure; it goes with the rent. The areas and the what-to-check advice stay word for word.")
    # --- rent and value paragraph
    old = P.sub('דירה שמושכרת ב-4,700 ש"ח בחודש עשויה להצדיק מחיר גבוה יותר מדירה שמושכרת ב-3,200 ש"ח,')
    P.edit(old, 'דירה שמושכרת בשכר גבוה יותר עשויה להצדיק מחיר גבוה יותר מדירה שמושכרת בשכר נמוך יותר,', "B",
           'removed the two illustrative rents 4,700 and 3,200; the comparison stays in words',
           "Two illustrative rents (4,700 vs 3,200) were in the range of the listing-site data on the page; the CBS has no single counterpart, so the numbers are removed and the point (a stable higher rent can justify a higher price) is kept.")
    old = P.sub('לפי מדגם עדכני של 279 מודעות, מדיאן השכירות באשקלון היה סביב 3,500 ש"ח,', 'מדיאן ארצי של כ-4,400 ש"ח.')
    new = (f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע באשקלון {Q2} היה {c(CITY)} ש"ח לכלל הדירות ו-{c(CITY, "2.5-3")} ש"ח לדירות של 2.5 עד 3 חדרים, '
           f'לעומת {c("סך הכל")} ו-{c("סך הכל", "2.5-3")} ש"ח בהתאמה בממוצע הארצי.')
    P.edit(old, new, "A", 'replaced the 279-ad sample (median 3,500, average 4,130, 3 rooms 3,629, national median 4,400) with the CBS averages: Ashkelon 3,698 / 3,261 (2.5-3 rooms) against 5,086 / 4,466 nationally, Q2 2026',
           "Listing sample of 279 ads (median 3,500; average 4,130; 3 rooms 3,629; national median 4,400) replaced by the CBS average rent for all flats and for 2.5-3 rooms in Ashkelon and in Israel, Q2 2026. The sentence that follows ('the gap can attract buyers looking for a lower entry price') now rests on an official gap.",
           [key(CITY), key(CITY, "2.5-3"), key("סך הכל"), key("סך הכל", "2.5-3")], url=RENT_URL)
    # --- other listing source
    old = P.sub('מקור מודעות אחר הציג 293 מודעות שכירות, ממוצע של כ-4,108 ש"ח, מדיאן 3,500 ש"ח ועדכון מיום 4 ביוני 2026. מקורות כאלה טובים')
    P.edit(old, 'מקורות מודעות שכירות טובים', "B", 'removed the second listing source (293 ads, average 4,108, median 3,500, 4.6.2026); the general remark on listing sources stays',
           "A second listing-site sample (293 ads, average 4,108, median 3,500) with no official counterpart: the figures go, the general remark that ad sources help see direction (and their limits, in the next sentences) stays.")
    # --- rooms table: rebuilt on the CBS groups
    def rooms(old):
        h, rows = parse_table(old)
        by = {r[0].strip(): r for r in rows}
        nat = lambda g: f'{c("סך הכל", g)} ש"ח'
        head = [h[0], 'שכר דירה חודשי ממוצע באשקלון, אפריל עד יוני 2026 (הלמ"ס)', 'ממוצע ארצי באותה קבוצה (הלמ"ס)', h[4]]
        body = [
            ["1 עד 2 חדרים", f'{c(CITY, "1-2")} ש"ח', nat("1-2"), by["1 חדר"][4] + "; " + by["2 חדרים"][4]],
            ["2.5 עד 3 חדרים", f'{c(CITY, "2.5-3")} ש"ח', nat("2.5-3"), by["3 חדרים"][4]],
            ["3.5 עד 4 חדרים", f'{c(CITY, "3.5-4")} ש"ח', nat("3.5-4"), by["4 חדרים"][4]],
            ["4.5 חדרים ומעלה", f'{c(CITY, "4.5+")} ש"ח', nat("4.5+"), by["5 חדרים"][4]],
        ]
        return rebuild(old, head, body)
    P.table('<th dir="rtl">מדיאן שכירות במדגם מודעות</th>', rooms, "A",
            'rebuilt the rent-by-rooms table on the CBS Ashkelon size groups (2,740 / 3,261 / 4,031 / 4,906 ש"ח, Q2 2026) with the national CBS average for each group; ad counts, the second-source column and the one-ad 6-room row (18,000) deleted',
            "Rent table (6 rows from an ad sample: 2,479; 2,963; 3,629; 4,709; 7,127; 18,000 with ad counts and 'another source' 2.30 / 4.20 / 5.50 thousand) rebuilt on the CBS average monthly rent in Ashkelon by size group, Q2 2026, with the national CBS average of the same group beside it (it replaces the old national median 4,400). Columns deleted: ad counts and the second private source. Rows regrouped to the CBS groups (1 and 2 rooms merged); the 6-room row was one ad (18,000), dropped. Usage notes stay word for word (the merged pair joined).",
            KEYS + [key("סך הכל", g) for g in ("1-2", "2.5-3", "3.5-4", "4.5+")], url=RENT_URL)
    # --- verification example
    old = P.sub('ומושכרת באזור ב-3,600 ש"ח, זה נותן מסגרת.', 'מחיר הקנייה צריך להיבחן בזהירות.')
    new = (f'ומושכרת באזור בכ-{c(CITY, "2.5-3")} ש"ח, הממוצע של הלמ"ס לדירות של 2.5 עד 3 חדרים {Q2S}, זה נותן מסגרת. '
           f'אם דירת 4 חדרים מוצעת ב-1.82 מיליון ש"ח והשכירות האזורית לדירות דומות קרובה ל-{c(CITY, "3.5-4")} ש"ח, הממוצע של הלמ"ס לדירות של 3.5 עד 4 חדרים, '
           'צריך לבדוק האם המחיר משקף יתרון מובהק או ציפייה גבוהה. '
           f'אם דירת 5 חדרים מבוקשת ב-2.6 מיליון ש"ח, אבל השכירות הריאלית קרובה ל-{c(CITY, "4.5+")} ש"ח, הממוצע של הלמ"ס לדירות של 4.5 חדרים ומעלה, '
           'ולא לסכום גבוה בהרבה, מחיר הקנייה צריך להיבחן בזהירות.')
    P.edit(old, new, "A", 'replaced the example rents 3,600 / 4,700 / 5,500 / 7,100 with the CBS Ashkelon averages for 2.5-3, 3.5-4 and 4.5+ rooms (3,261 / 4,031 / 4,906 ש"ח, Q2 2026); the hypothetical sale prices stay',
           "Worked examples built on ad-site rents (3,600; regional median 4,700; 5,500 against 7,100) now use the CBS Ashkelon size-group averages of Q2 2026. The hypothetical sale prices (1.32, 1.82, 2.6 million) were already on the page and are untouched; the 7,100 'asked rent' becomes 'a much higher sum'.",
           [key(CITY, "2.5-3"), key(CITY, "3.5-4"), key(CITY, "4.5+"), "page"], kept=["1.32", "1.82", "2.6"], url=RENT_URL)
    # --- Ir HaYayin / Agamim rents
    old = P.sub('בעיר היין נראו נתוני שכירות סביב 5,287 ש"ח במדיאן, ובאגמים סביב 4,980 ש"ח. אלה מספרים שמאותתים על ביקוש, אך גם על כך שהקונה צריך')
    P.edit(old, 'בשווקים כאלה הקונה צריך', "B", 'removed the neighbourhood rents (Ir HaYayin 5,287, Agamim 4,980); the advice to check the supply still to come stays',
           "Neighbourhood rents from ads, no official counterpart: removed. The remaining point (check how much new supply is coming) is advice and stays.")
    # --- FAQ
    old = P.sub('מדיאן שכירות עירוני שנצפה עמד סביב 3,500 ש"ח בחודש,', 'במדגם מודעות מסוים.')
    new = f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע באשקלון {Q2} היה {c(CITY)} ש"ח בממוצע לכלל הדירות, ובחלוקה לפי גודל: {sizes}.'
    P.edit(old, new, "A", 'replaced the FAQ rents (city median 3,500, averages 4,108-4,130, by rooms 2,963 / 3,629 / 4,709 / 7,127) with the CBS Ashkelon averages for all flats and by size group, Q2 2026',
           "FAQ 'how much rent in Ashkelon': ad-sample medians and averages replaced by the CBS average rent in Ashkelon for all flats (3,697.9) and by size group, Q2 2026.",
           KEYS, url=RENT_URL)
