# -*- coding: utf-8 -*-
"""National hub /apartment-prices/ (page 7151): city cards carry 'chips' copied from the old city reviews. Aligned with the official
3-room medians in apartment-prices.json (cities[...]), which the national price list and the city lists show."""
from mk import Page

P = Page("apartment-prices")

# (old chip text, new chip text, slug, verdict, official note)
chips = [
    ("מ-45 אלף למ\"ר", "חציון 3 חד' 4.23 מיליון", "tel-aviv-apartment-prices", "UNSOURCED", "per m2, no source on the hub; 3 rooms 4,225,800 (1-3.2026)", "per_m2"),
    ("ממוצע ~3.2 מיליון", "חציון 3 חד' 2.7 מיליון", "ramat-gan-apartment-prices", "CONSISTENT", "all rooms 3,122,300; 3 rooms 2,701,700 (1-3.2026)", "sale_avg"),
    ("3 חד' 2.4–2.9 מיליון", "חציון 3 חד' 2.82 מיליון", "givatayim-apartment-prices", "CONSISTENT", "3 rooms 2,815,300 (1-3.2026)", "sale"),
    ("3 חד' 1.8–2.15 מיליון", "חציון 3 חד' 2.03 מיליון", "bnei-brak-apartment-prices", "CONSISTENT", "3 rooms 2,028,000 (1-3.2026)", "sale"),
    ("3 חד' מ-1.55 מיליון", "חציון 3 חד' 2.06 מיליון", "petah-tikva-apartment-prices", "CONSISTENT", "3 rooms 2,057,000 (1-3.2026)", "sale"),
    ("3 חד' מ-1.65 מיליון", "חציון 3 חד' 1.94 מיליון", "rishon-lezion-apartment-prices", "CONSISTENT", "3 rooms 1,936,700 (1-3.2026)", "sale"),
    ("ממוצע ~3.4 מיליון", "חציון 3 חד' 2.64 מיליון", "kiryat-ono-apartment-prices", "CONFLICT", "all rooms 3,175,100 (1-3.2026), 7% below the stated average; 3 rooms 2,635,400", "sale_avg"),
    ("3 חד' מ-2.5 מיליון", "חציון 3 חד' 2.79 מיליון", "herzliya-apartment-prices", "CONSISTENT", "3 rooms 2,793,600 (1-3.2026)", "sale"),
    ("3 חד' ~2.8 מיליון", "חציון 3 חד' 2.81 מיליון", "raanana-apartment-prices", "CONSISTENT", "3 rooms 2,814,000 (1-3.2026)", "sale"),
    ("3 חד' 2–3 מיליון", "חציון 3 חד' 1.94 מיליון", "kfar-saba-apartment-prices", "CONFLICT", "3 rooms 1,941,300 (10-12.2025, the latest published), below the 2M floor", "sale"),
    ("3 חד' מ-2.25 מיליון", "חציון 3 חד' 2.65 מיליון", "hod-hasharon-apartment-prices", "CONSISTENT", "3 rooms 2,647,000 (1-3.2026)", "sale"),
    ("3 חד' מ-1.45 מיליון", "חציון 3 חד' 1.79 מיליון", "netanya-apartment-prices", "CONSISTENT", "3 rooms 1,791,300 (10-12.2025, the latest published)", "sale"),
    ("3 חד' ~2.65 מיליון", "חציון 3 חד' 2.04 מיליון", "modiin-apartment-prices", "CONFLICT", "3 rooms 2,039,500 (10-12.2025, the latest published)", "sale"),
    ("3 חד' מ-1.0 מיליון", "חציון 3 חד' 918 אלף", "ashkelon-apartment-prices", "CONFLICT", "3 rooms 918,100 (1-3.2026), below the 1.0M floor", "sale"),
]

# 1. lead
old1 = "טווחי עבודה לפי מספר חדרים, מחיר למ\"ר ושכירות, יחד עם הבדיקות שחשוב לעשות לפני שמסתמכים על מספר כלשהו. המספרים בכרטיסים לקוחים מהסקירה המלאה של כל עיר."
new1 = ("חציון מחיר העסקה לפי מספר חדרים, מחיר למ\"ר ושכירות, יחד עם הבדיקות שחשוב לעשות לפני שמסתמכים על מספר כלשהו. "
        "המספר בכל כרטיס הוא חציון מחיר העסקה לדירת 3 חדרים מהמחירון של אותה עיר.")
e1 = P.edit(old1, new1, ["cities[ashkelon-apartment-prices].rooms.3.latest"], "WORDING",
            "The lead called the card numbers working ranges copied from each review; they become the official 3-room medians (edits 3-16).")

# 2. notice above the cards
old2 = "הטווחים הם מספרי עבודה שנאספו ממקורות פומביים ומתעדכנים מעת לעת"
new2 = ("המספר בכל כרטיס הוא חציון מחיר העסקה לדירת 3 חדרים בעיר, לפי נתוני רשות המסים לרבעון הראשון של 2026 (בכפר סבא, "
        "בנתניה ובמודיעין: הרבעון הרביעי של 2025, הנתון האחרון שפורסם לדירות 3 חדרים). המספרים מתעדכנים מעת לעת")
e2 = P.edit(old2, new2, ["cities[kfar-saba-apartment-prices].rooms.3.quarter", "cities[netanya-apartment-prices].rooms.3.quarter",
                         "cities[modiin-apartment-prices].rooms.3.quarter"], "WORDING",
            "The notice described the cards as working numbers from public sources; it now says what the number is and from which quarter.")

nums = {}
for old, new, slug, verdict, off, measure in chips:
    nums[slug] = P.edit(old, new, [f"cities[{slug}].rooms.3.latest"], verdict,
                        ("Card figure vs the official 3-room median: " + off + "." +
                         (" Restated as the median so every card shows the same measure." if verdict == "CONSISTENT" else "")))

# footer
old_f = "המחירון מבוסס על סקירות שוק פומביות ומתעדכן. הטווחים אינם ייעוץ ואינם שומה;"
new_f = "המחירון מבוסס על נתוני העסקאות של רשות המסים ועל סקירות השוק של כל עיר, ומתעדכן. המספרים אינם ייעוץ ואינם שומה;"
P.edit(old_f, new_f, ["data_quarter"], "WORDING", "Footer: the card numbers are now official medians, not ranges.")

C = P.claim
for old, new, slug, verdict, off, measure in chips:
    C("span.chip", f"{slug.split('-apartment')[0]}: {old}", measure, verdict, f"edit {nums[slug]}", rooms=("" if measure != "sale" else "3"),
      official=off)

P.write(notes=("Audited on the copy retrieved 10:34 UTC, before the national price list was added (it was on the page by 11:17 UTC; the text outside it is unchanged). All 14 city cards are restated as the official "
               "3-room median so the cards share one measure and match the city lists; 9 of them were already consistent with it. "
               "Cards without a chip (Jerusalem, Haifa, Holon, Bat Yam, Rehovot, Ashdod, Beer Sheva, Eilat, house towns, luxury pages) "
               "are left as they are. The em dash in the lead sentence before 'טווחי עבודה' is outside the edited strings."))
