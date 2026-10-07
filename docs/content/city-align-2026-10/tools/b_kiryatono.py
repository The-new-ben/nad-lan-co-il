# -*- coding: utf-8 -*-
"""Kiryat Ono (page 4560): body alignment with the official price list (1-3.2026). Data only, nothing applied."""
import re
from mk import Page

P = Page("kiryat-ono-apartment-prices")
D = P.d
SH = "ש\"ח"


def money(v):
    return f"{v:,} {SH}"


def R(k, f="latest"):
    return D["rooms"][k][f]


def NB(name, k):
    for n in D["neighbourhoods"]:
        if n["name"] == name:
            return n["rooms"].get(k)
    raise KeyError(name)


def chg(k):
    v = float(D["rooms"][k]["change_pct"])
    return f"עלייה של {v:g}%" if v >= 0 else f"ירידה של {abs(v):g}%"


def cells(anchor):
    h = P.table_html(anchor)
    body = h[h.find("<tbody"):]
    return [re.findall(r"<td\b[^>]*>(.*?)</td>", r, re.S) for r in re.findall(r"<tr\b[^>]*>(.*?)</tr>", body, re.S)]


def tbl(headers, rows):
    """same indentation as the page's own tables (2/4/6 spaces)."""
    out = ['<table dir="rtl">', '  <thead dir="rtl">', '    <tr dir="rtl">']
    out += [f'      <th dir="rtl">{h}</th>' for h in headers]
    out += ["    </tr>", "  </thead>", '  <tbody dir="rtl">']
    for r in rows:
        out.append('    <tr dir="rtl">')
        out += [f'      <td dir="rtl">{x}</td>' for x in r]
        out.append("    </tr>")
    out += ["  </tbody>", "</table>"]
    return "\n".join(out)


Q1 = "ברבעון הראשון של 2026"
TAX = "לפי נתוני רשות המסים"

# ---------------- edits ----------------
# 1. city average from 'market data pages'
old1 = "לפי דפי נתוני שוק שנבדקו, מחיר ממוצע כללי בעיר נע סביב 3.38-3.41 מיליון ש\"ח, אך ממוצע כזה יכול להטעות."
new1 = f"{TAX} לרבעון הראשון של 2026, חציון מחיר העסקה לכל הדירות בעיר היה {money(R('all'))}, אך גם נתון עירוני כזה יכול להטעות."
e1 = P.edit(old1, new1, ["rooms.all.latest"], "CONFLICT",
            "City average 3.38-3.41M vs the official all-rooms median 3,175,100 (1-3.2026), 6.5% above the floor of the range; it matches "
            "the year-earlier median 3,395,400.")

# 2. the page's own source statement
old2a = "טווח עבודה בלבד:"
new2a = "נקודת ייחוס בלבד:"
e2a = P.edit(old2a, new2a, ["data_quarter"], "WORDING", "Bold lead-in (inside <strong>) of the source statement edited in the next edit.")
old2 = "המספרים בעמוד זה מבוססים על בדיקת שוק גלויה ואינם שומה."
new2 = "חציון מחיר העסקה בעמוד מבוסס על נתוני רשות המסים, ושאר המספרים מבוססים על בדיקת שוק גלויה; אף אחד מהם אינו שומה."
e2 = P.edit(old2, new2, ["data_quarter"], "WORDING",
            "The page now carries official medians next to the market-check figures it keeps; the statement names both sources.")

# 3-4. the 'market measures' table: average row
old3 = "מחיר ממוצע כללי בעיר"
new3 = "חציון מחיר העסקה בעיר, כל הדירות"
e3 = P.edit(old3, new3, ["rooms.all.latest"], "WORDING", "Row label of the cell edited in edit 4 (unique after edit 1).")
old4 = "כ-3.38-3.41 מיליון ש\"ח"
new4 = f"{money(R('all'))} (ינואר-מרץ 2026)"
e4 = P.edit(old4, new4, ["rooms.all.latest"], "CONFLICT", "Same city average as edit 1 inside the market-measures table; the other rows are kept.")

# 5. rooms paragraph before the rooms table
old5 = P.find("דירת 2 חדרים יכולה להופיע סביב 2.0-2.18", "גבוהות או מיוחדות.")
new5 = (f"{TAX} לרבעון הראשון של 2026, חציון מחיר העסקה בקריית אונו היה {money(R('3'))} לדירת 3 חדרים, {money(R('4'))} "
        f"לדירת 4 חדרים ו-{money(R('5'))} לדירת 5 חדרים, עם חריגות כלפי מעלה בדירות חדשות, משופצות, גבוהות או מיוחדות. "
        "דירת 2 חדרים הופיעה בבדיקת שוק גלויה סביב 2.0-2.18 מיליון ש\"ח.")
e5 = P.edit(old5, new5, ["rooms.3.latest", "rooms.4.latest", "rooms.5.latest", "page"], "CONFLICT",
            "5 rooms 3.6-4.1M excludes the official 3,533,500 (1-3.2026); 3 rooms 2.4-2.9M and 4 rooms 3.1-3.5M were consistent and are "
            "restated as the medians. The 2-room range (market check, page checked 5.6.2026) is kept and labelled.")

# 6. intro of the rooms table
old6 = P.find("בטבלה הבאה מוצגים טווחי שוק שנבדקו בדפי נתונים גלויים.", "גבוה או נמוך ביחס לשוק.")
new6 = (f"בטבלה הבאה מוצג חציון מחיר העסקה {TAX} לרבעון הראשון של 2026 והשינוי לעומת אותו רבעון שנה קודם לכן, לצד השכירות "
        "החודשית הנפוצה לפי בדיקת שוק גלויה. הטבלה אינה מחליפה בדיקה פרטנית של עסקה דומה, אך היא עוזרת לזהות האם מחיר מבוקש "
        "נשמע סביר, גבוה או נמוך ביחס לשוק. המחירון הרשמי מפרסם חציון לדירות 3, 4 ו-5 חדרים; דירות 2 חדרים ודירות 6 חדרים "
        "ומעלה כדאי לבדוק מול עסקאות דומות ברחוב ובשכונה.")
e6 = P.edit(old6, new6, ["data_quarter"], "WORDING", "Introduces the official rooms table of edit 7; the 1-2 and 6+-room rows left the table.")

# 7. the rooms table (second-hand / new estimates + rent)
A7 = '<th dir="rtl">מחיר יד שנייה משוער</th>'
t7 = cells(A7)
assert [r[0] for r in t7[1:4]] == ["3 חדרים", "4 חדרים", "5 חדרים"], t7
new7 = tbl(["סוג דירה", "חציון מחיר העסקה, ינואר-מרץ 2026", "שינוי בשנה", "שכירות חודשית נפוצה", "הערת בדיקה"],
           [[t7[i][0], money(R(k)), chg(k), t7[i][3], t7[i][4]] for i, k in ((1, "3"), (2, "4"), (3, "5"))])
e7 = P.table(A7, new7, ["rooms.3.latest", "rooms.3.change_pct", "rooms.4.latest", "rooms.4.change_pct", "rooms.5.latest", "rooms.5.change_pct", "page"],
             "CONFLICT",
             "Rooms table: 5 rooms second-hand 3.76-4.10M and new 3.6-4.7M exclude the official 3,533,500 (1-3.2026); 3 and 4 rooms were "
             "consistent. Replaced by the official medians and the year-on-year change; the rent column (market check, page checked "
             "5.6.2026) and the check notes of rows 3-5 are kept word for word; the 1-2, 6 and 6+/house rows leave the table (their rent "
             "stays in the rent table below).")

# 8-10. neighbourhood rows that have an official median
nbr = {}
for name, old, ks in (("קיראון", "כ-3.2 מיליון ש\"ח בממוצע לפי נתוני שוק גלויים", ("4", "5")),
                      ("גני אילן", "כ-3.4 מיליון ש\"ח בממוצע לפי נתוני עסקאות גלויים", ("3", "5")),
                      ("שיכון רסקו", "כ-3.35 מיליון ש\"ח בממוצע לפי נתוני שוק", ("3", "4"))):
    a, b = ks
    new = f"{TAX}, ינואר-מרץ 2026: חציון {money(NB(name, a))} לדירת {a} חדרים ו-{money(NB(name, b))} לדירת {b} חדרים"
    nbr[name] = P.edit(old, new, [f"neighbourhoods[{name}].rooms.{a}", f"neighbourhoods[{name}].rooms.{b}"], "UNSOURCED",
                       f"{name}: an all-rooms average with no room count; replaced by the official neighbourhood medians by rooms (1-3.2026). "
                       "Rows without an official median keep their market-check figures.")

# 11. rent table: 'relation to the sale price' cell for 5 rooms
old11 = "רלוונטי לדירות סביב 3.6-4.7 מיליון ש\"ח"
new11 = f"רלוונטי לדירות סביב חציון מחיר העסקה, {money(R('5'))} {Q1}"
e11 = P.edit(old11, new11, ["rooms.5.latest"], "CONFLICT", "5-room sale range 3.6-4.7M in the rent table excludes the official 3,533,500.")

# 12. new vs second-hand paragraph
old12 = P.find("בטווחים שנבדקו, דירות 3 חדרים חדשות", "סביב 3.76-4.10 מיליון ש\"ח.")
new12 = ("בטווחים שנבדקו, דירות 3 חדרים חדשות הופיעו סביב 2.4-3.0 מיליון ש\"ח ודירות 4 חדרים חדשות סביב 3.0-4.0 מיליון ש\"ח. "
         "ביד שנייה, דירות 3 חדרים הופיעו סביב 2.43-2.71 מיליון ש\"ח ודירות 4 חדרים סביב 3.14-3.25 מיליון ש\"ח. "
         f"בדירות 5 חדרים, {TAX}, חציון מחיר העסקה {Q1} היה {money(R('5'))}, לעומת {money(R('5', 'year_ago'))} שנה קודם לכן, "
         "ולכן כדאי להשוות דירת 5 חדרים, חדשה או יד שנייה, לעסקאות דומות מהרבעונים האחרונים.")
e12 = P.edit(old12, new12, ["rooms.5.latest", "rooms.5.year_ago", "page"], "CONFLICT",
             "New 5 rooms 3.6-4.7M and second-hand 5 rooms 3.76-4.10M exclude the official 3,533,500; the 3- and 4-room new and second-hand "
             "ranges are consistent and kept word for word.")

# 13. renovation cost cell (tier 2)
old13 = "יכול להגיע ל-100,000-300,000 ש\"ח ואף יותר"
new13 = "יכול להגיע לעלות משמעותית"
e13 = P.edit(old13, new13, ["page"], "UNSOURCED", "Renovation cost range 100,000-300,000 with no source.", tier=2)

# 14. same-street gap (tier 2)
old14 = "שתי דירות באותו רחוב בקריית אונו יכולות להימכר בפער של 300,000 ש\"ח, 500,000 ש\"ח ואף יותר, בגלל הבדלים פנימיים."
new14 = "שתי דירות באותו רחוב בקריית אונו יכולות להימכר בפער של מאות אלפי ש\"ח ואף יותר, בגלל הבדלים פנימיים."
e14 = P.edit(old14, new14, ["page"], "UNSOURCED", "Price gaps of 300,000 / 500,000 inside one street, no source.", tier=2)

# 15. asking vs closing gap (tier 2)
old15 = "פער אפשרי של 2-8 אחוזים ואף יותר"
new15 = "פער אפשרי של כמה אחוזים ואף יותר"
e15 = P.edit(old15, new15, ["page"], "UNSOURCED", "Asking-to-closing gap of 2-8% with no source; the FAQ already says 'כמה אחוזים'.", tier=2)

# 16-18. FAQ
old16 = "בדיקת נתוני שוק גלויים מ-5 ביוני 2026 הצביעה על מחיר ממוצע כללי סביב 3.38-3.41 מיליון ש\"ח. זהו ממוצע עירוני בלבד."
new16 = (f"{TAX}, חציון מחיר העסקה לכל הדירות בקריית אונו {Q1} היה {money(R('all'))}, לעומת {money(R('all', 'year_ago'))} "
         "שנה קודם לכן. זהו נתון עירוני בלבד.")
e16 = P.edit(old16, new16, ["rooms.all.latest", "rooms.all.year_ago"], "CONFLICT",
             "FAQ average: 3.38-3.41M (market check 5.6.2026) vs the official all-rooms median 3,175,100; the answer names the median, not an average.")

old17 = P.find("דירות 5 חדרים נעות לרוב סביב 3.6-4.1 מיליון", "יכולה לעבור את הטווח הזה.")
new17 = (f"{TAX}, חציון מחיר העסקה לדירת 5 חדרים בקריית אונו {Q1} היה {money(R('5'))}, לעומת {money(R('5', 'year_ago'))} שנה "
         "קודם לכן. דירה עם 2 חניות, מחסן, מרפסת גדולה, קומה גבוהה או מיקום מבוקש יכולה להימכר במחיר גבוה יותר.")
e17 = P.edit(old17, new17, ["rooms.5.latest", "rooms.5.year_ago", "page"], "CONFLICT",
             "FAQ 5 rooms: second-hand 3.6-4.1M and new 3.6-4.7M exclude the official 3,533,500.")

old18 = "קיראון היא אזור מבוקש עם פעילות עסקאות משמעותית, ובבדיקת שוק הופיעו בה נתונים סביב 3.2 מיליון ש\"ח בממוצע."
new18 = (f"קיראון היא אזור מבוקש עם פעילות עסקאות משמעותית. {TAX} לרבעון הראשון של 2026, חציון מחיר העסקה בקיראון היה "
         f"{money(NB('קיראון', '4'))} לדירת 4 חדרים ו-{money(NB('קיראון', '5'))} לדירת 5 חדרים, לעומת {money(R('4'))} "
         f"ו-{money(R('5'))} בעיר כולה.")
e18 = P.edit(old18, new18, ["neighbourhoods[קיראון].rooms.4", "neighbourhoods[קיראון].rooms.5", "rooms.4.latest", "rooms.5.latest"], "UNSOURCED",
             "FAQ Kiraon: all-rooms average 3.2M; replaced by the official Kiraon medians, same figures as the neighbourhood table (edit 8).")

# ---------------- claims inventory ----------------
KEEP = "keep (public market check named on the page, checked 5.6.2026)"
C = P.claim
C("p@4420", "מחירי דירות ... סביב 2.4-4.1 מיליון ש\"ח לדירות רגילות", "sale", "CONSISTENT", "keep (3/4/5-room medians inside the range)",
  rooms="3-5", official="2,635,400 / 3,197,900 / 3,533,500", figures=2)
C("p@4420", "דירות 4 חדרים רבות מתכנסות סביב 3.1-3.5 מיליון ש\"ח", "sale", "CONSISTENT", "keep", rooms=4, official="3,197,900", figures=2)
C("p@4420", "דירות חדשות, גדולות ופנטהאוזים יכולים לעבור גם 4.5-7.5 מיליון ש\"ח", "sale", "UNSOURCED", KEEP, rooms="6+", figures=2)
C("p@40353", "שכירות 5,800-8,200 ש\"ח ב-3-5 חדרים; בית פרטי 11,900-14,000", "rent", "UNSOURCED", KEEP, figures=4)
C("p@40979", "בדיקת נתוני שוק מ-5 ביוני 2026: דירות רגילות 2.4-4.1 מיליון", "sale", "CONSISTENT", "keep", rooms="3-5", figures=2)
C("p@40979", "דירות 4 חדרים רבות סביב 3.1-3.5 מיליון ש\"ח", "sale", "CONSISTENT", "keep", rooms=4, official="3,197,900", figures=2)
C("p@40979", "דירות חדשות, גדולות ופנטהאוזים: 4.7 / 6 / 7.5 מיליון ש\"ח", "sale", "UNSOURCED", "keep (dated in the sentence: market data of 5.6.2026)", rooms="6+", figures=3)
C("p@41760", "מחיר ממוצע כללי בעיר נע סביב 3.38-3.41 מיליון ש\"ח", "sale_avg", "CONFLICT", f"edit {e1}", rooms="all",
  official="all rooms 3,175,100 (1-3.2026)", figures=2, note="matches the 1-3.2025 median 3,395,400")
C("tr@42613", "מחיר ממוצע כללי בעיר | כ-3.38-3.41 מיליון ש\"ח", "sale_avg", "CONFLICT", f"edit {e4}", rooms="all", official="3,175,100", figures=2)
C("tr@42800", "מחיר למ\"ר ממוצע | כ-30,000 ש\"ח למ\"ר", "per_m2", "UNSOURCED", KEEP)
C("tr@42976", "דירות 4 חדרים | כ-3.1-3.5 מיליון ש\"ח", "sale", "CONSISTENT", "keep", rooms=4, official="3,197,900", figures=2)
C("tr@43153", "דירות חדשות | מ-3.0 ועד 4.7 מיליון ש\"ח בדירות 4-5 חדרים", "sale_new_used", "CONSISTENT", "keep", rooms="4-5",
  official="3,197,900 / 3,533,500", figures=2)
C("tr@43362", "שכירות ממוצעת כללית | כ-7,600-7,900 ש\"ח בחודש", "rent", "UNSOURCED", KEEP, figures=2)
C("p@43625", "דירת 2 חדרים סביב 2.0-2.18 מיליון ש\"ח", "sale", "UNSOURCED", f"edit {e5}", rooms=2, figures=2, note="kept inside the rewrite, labelled as market check")
C("p@43625", "דירת 3 חדרים סביב 2.4-2.9 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e5}", rooms=3, official="2,635,400", figures=2)
C("p@43625", "דירת 4 חדרים סביב 3.1-3.5 מיליון ש\"ח", "sale", "CONSISTENT", f"edit {e5}", rooms=4, official="3,197,900", figures=2)
C("p@43625", "דירת 5 חדרים סביב 3.6-4.1 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e5}", rooms=5, official="3,533,500 (1-3.2026)", figures=2)
C("tr@44446", "1-2 חדרים | 2.0-2.1 מיליון יד שנייה | 2.18 מיליון חדשה", "sale_new_used", "UNSOURCED", f"edit {e7}", rooms="1-2", figures=3)
C("tr@44446", "1-2 חדרים | שכירות 3,700-4,300", "rent", "UNSOURCED", "keep (row left the table; same figure stays in the rent table tr@51507)", rooms="1-2", figures=2)
C("tr@44713", "3 חדרים | יד שנייה 2.43-2.71 מיליון | חדשה 2.4-3.0 מיליון", "sale_new_used", "CONSISTENT", f"edit {e7}", rooms=3, official="2,635,400", figures=4)
C("tr@44983", "4 חדרים | יד שנייה 3.14-3.25 מיליון | חדשה 3.0-4.0 מיליון", "sale_new_used", "CONSISTENT", f"edit {e7}", rooms=4, official="3,197,900", figures=4)
C("tr@45242", "5 חדרים | יד שנייה 3.76-4.10 מיליון | חדשה 3.6-4.7 מיליון", "sale_new_used", "CONFLICT", f"edit {e7}", rooms=5, official="3,533,500", figures=4)
C("tr@44713..45242", "שכירות חודשית נפוצה 3-5 חדרים: 5,800-6,600 / 7,300-7,500 / 7,900-8,200", "rent", "UNSOURCED",
  f"keep (carried word for word into edit {e7}; market check, page checked 5.6.2026)", rooms="3-5", figures=6)
C("tr@45507", "6 חדרים | 4.04-4.46 מיליון | 4.38 מיליון ומעלה | שכירות 8,700 ומעלה", "sale", "UNSOURCED", f"edit {e7}", rooms=6, figures=4,
  note="row left the table; the 8,700 rent stays in the rent table")
C("tr@45774", "6+ או בית פרטי | 4.8-7.5 מיליון | פנטהאוזים מ-4.0 מיליון | שכירות 11,900-14,000", "sale", "UNSOURCED", f"edit {e7}", rooms="6+", figures=6,
  note="row left the table; the 11,900-14,000 rent stays in the rent table and in the rent card")
C("tr@47680", "קיראון | כ-3.2 מיליון ש\"ח בממוצע לפי נתוני שוק גלויים", "sale_nb", "UNSOURCED", f"edit {nbr['קיראון']}",
  official="קיראון 4 rooms 3,024,700, 5 rooms 3,489,100")
C("tr@48223", "גני אילן | כ-3.4 מיליון ש\"ח בממוצע לפי נתוני עסקאות גלויים", "sale_nb", "UNSOURCED", f"edit {nbr['גני אילן']}",
  official="גני אילן 3 rooms 2,655,200, 5 rooms 3,048,100")
C("tr@49260", "שיכון רסקו | כ-3.35 מיליון ש\"ח בממוצע לפי נתוני שוק", "sale_nb", "UNSOURCED", f"edit {nbr['שיכון רסקו']}",
  official="שיכון רסקו 3 rooms 2,768,900, 4 rooms 3,400,500")
C("tr@47938", "קריית אונו הוותיקה | כ-26,000-28,500 ש\"ח למ\"ר", "per_m2", "UNSOURCED", KEEP, figures=2)
C("tr@48479..49990", "נאות אריאל שרון 4.05 / פסגת אונו 2.6-3.5 / מרכז העיר 3.2 / צומת סביון 3.5 / רייספלד 2.3-3.0 / רימון 2.5-3.3 מיליון",
  "sale_nb", "UNSOURCED", "keep (no official median for these areas; each row names its market-check source, page checked 5.6.2026)", figures=9)
C("tr@51507..52631", "טבלת שכירות לפי בדיקת שוק (6 שורות, 3,700-14,000)", "rent", "UNSOURCED", KEEP, figures=10)
C("tr@51727", "3 חדרים | יכול לתמוך במחיר סביב 2.4-2.9 מיליון ש\"ח", "sale", "CONSISTENT", "keep", rooms=3, official="2,635,400", figures=2)
C("tr@51948", "4 חדרים | מסייע לבדוק דירות סביב 3.1-3.5 מיליון ש\"ח", "sale", "CONSISTENT", "keep", rooms=4, official="3,197,900", figures=2)
C("tr@52184", "5 חדרים | רלוונטי לדירות סביב 3.6-4.7 מיליון ש\"ח", "sale", "CONFLICT", f"edit {e11}", rooms=5, official="3,533,500", figures=2)
C("p@53720", "עסקה של 58 מ\"ר ב-2.34 מיליון (40,344 למ\"ר); 140 מ\"ר ב-3.45 מיליון (24,642 למ\"ר)", "deal", "UNSOURCED",
  "keep (the individual deals of the table below, dated May 2026)", figures=4)
C("tr@54297..55574", "טבלת 6 עסקאות לפי כתובת, מאי 2026: מחיר עסקה ומחיר למ\"ר", "deal", "UNSOURCED", "keep (individual deals, address and month named)", figures=12)
C("p@56553", "חדשות: 3 חדרים 2.4-3.0, 4 חדרים 3.0-4.0; יד שנייה: 3 חדרים 2.43-2.71, 4 חדרים 3.14-3.25", "sale_new_used", "CONSISTENT",
  f"edit {e12}", rooms="3-4", official="2,635,400 / 3,197,900", figures=8, note="kept word for word inside the edit")
C("p@56553", "5 חדרים חדשות 3.6-4.7 מיליון; יד שנייה 3.76-4.10 מיליון", "sale_new_used", "CONFLICT", f"edit {e12}", rooms=5, official="3,533,500", figures=4)
C("tr@57124", "מחיר ראשוני חדשה: 3.0-4.7 מיליון ש\"ח בדירות 4-5 חדרים", "sale_new_used", "CONSISTENT", "keep", rooms="4-5", official="3,197,900 / 3,533,500", figures=2)
C("tr@57858", "שיפוץ יכול להגיע ל-100,000-300,000 ש\"ח", "other", "UNSOURCED", f"edit {e13}", figures=2)
C("p@58921", "שתי דירות באותו רחוב בפער של 300,000 / 500,000 ש\"ח", "other", "UNSOURCED", f"edit {e14}", figures=2)
C("tr@62708", "פער אפשרי של 2-8 אחוזים בין מבוקש לסגירה", "other", "UNSOURCED", f"edit {e15}", figures=2)
C("p@64206", "FAQ: מחיר ממוצע כללי סביב 3.38-3.41 מיליון ש\"ח (נתוני שוק 5.6.2026)", "sale_avg", "CONFLICT", f"edit {e16}", rooms="all", official="3,175,100", figures=2)
C("p@64486", "FAQ 3 חדרים: יד שנייה 2.43-2.71 / חדשה 2.4-3.0 מיליון", "sale_new_used", "CONSISTENT", "keep", rooms=3, official="2,635,400", figures=4)
C("p@64486", "FAQ 3 חדרים: שכירות 5,800-6,600 ש\"ח", "rent", "UNSOURCED", KEEP, rooms=3, figures=2)
C("p@64776", "FAQ 4 חדרים: טווח עבודה 3.1-3.5 מיליון", "sale", "CONSISTENT", "keep", rooms=4, official="3,197,900", figures=2)
C("p@65074", "FAQ 5 חדרים: יד שנייה 3.6-4.1 / חדשה 3.6-4.7 מיליון", "sale_new_used", "CONFLICT", f"edit {e17}", rooms=5, official="3,533,500", figures=4)
C("p@65333", "FAQ קיראון: סביב 3.2 מיליון ש\"ח בממוצע", "sale_nb", "UNSOURCED", f"edit {e18}", official="קיראון 4 rooms 3,024,700, 5 rooms 3,489,100")
C("p@65939", "FAQ נאות אריאל שרון: סביב 4.05 מיליון ש\"ח בחלק מהנתונים", "sale_nb", "UNSOURCED", KEEP + ", same as the table row")

P.write(notes=(
    "Not audited as claims (explicit hypotheticals, kept): 4 rooms advertised at 3.8M and an old 4-room flat at 3.5M (p@46114, 'כאשר "
    "מוכר מפרסם'); 7,500 rent and a 3.5M sale (p@50532); 3.21M / 103 m2 (p@53413, 'אם דירה ... נמכרה'); 3.25M / 3.95M (p@63378, 'אם "
    "דירות דומות נסגרו'); 12-36 months, 5-10 deals, 6-18 months (time and counts). Rent, per-m2, neighbourhood and 2 / 6+-room figures "
    "are kept where the page names its public market check and its check date (5.6.2026; p@40979 dates the check in the sentence); "
    "unsure whether 'בדיקת נתוני שוק גלויים' is a specific enough kind of source; if not, they become tier-2 edits. The deals table "
    "(six addresses, May 2026) is kept as individual dated deals. The one remaining check.py SUSPECT (p@4420, the card above the "
    "price list) is a heuristic misread: the 4.5-7.5M range belongs to new flats, large flats and penthouses (kept, market check), "
    "it only shares a sentence with the consistent 4-room range 3.1-3.5M. Official quirks: the 5-room median fell to 3,533,500 from 3,782,400 in "
    "7-9.2025; the page's 3.38-3.41M city average and 3.76-4.10M 5-room range match the 2025 official levels. No official median for "
    "10-12.2025 for 3, 4 or 5 rooms. Name mapping exact: קיראון, גני אילן, שיכון רסקו."))
