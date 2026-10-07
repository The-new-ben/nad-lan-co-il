# -*- coding: utf-8 -*-
"""Rebuild the TIER-2 edits of docs/content/city-align-2026-10/<slug>.align-edits.json under the CEO rule of 7.10.2026.

DATA ONLY: reads the live pages (public GET), writes only the 14 JSON files that hold tier-2 edits. Tier-1 edits and every other key are
left byte-for-byte as loaded (the file is re-dumped with the same json settings).

Rule: (A) an official dated value exists for the same thing -> the number is replaced by it, with its period
(rent: CBS table 4.9 Q2 2026 in tools/cbs_rent_2026_q2.json; sale prices: the city JSON; dwelling share: CBS press release 021/2026);
(B) no official dated source -> the number goes and the sentence or cell stays only as advice or a hedged statement that makes no
price-level claim; (C) a sentence, row or column that has no value without the number is deleted.

python b_tier2_ceo.py [--live-dir DIR] [--dry]
"""
import io, json, os, re, sys, time, urllib.request
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.dirname(HERE)
CBS = json.load(io.open(os.path.join(HERE, "cbs_rent_2026_q2.json"), encoding="utf-8"))
RENT_URL = CBS["urls"]["table_he_pdf"]
DWELL_URL = CBS["dwellings_share"]["url"]
RECHECK_NOTE = ("re-fetched 7.10.2026 after tier 1 went live (tier-1 'new' texts present); every tier-2 'old' matches exactly once in the "
                "live content.rendered, in the order listed")

LIVE_DIR = None
for i, a in enumerate(sys.argv):
    if a == "--live-dir":
        LIVE_DIR = sys.argv[i + 1]
DRY = "--dry" in sys.argv


def r0(v):
    """CBS one-decimal average -> whole shekels, half up"""
    return f"{int(Decimal(str(v)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)):,}"


def cbs(city_he, grp="total"):
    row = CBS["rows"][city_he]
    return row["total"] if grp == "total" else row["groups"][grp]


def cbs_key(city_he, grp="total"):
    return f"cbs_rent[{city_he}].{grp}.q2_2026"


def load_live(slug, pid):
    if LIVE_DIR:
        p = json.load(io.open(os.path.join(LIVE_DIR, slug + ".json"), encoding="utf-8"))
    else:
        u = "https://nad-lan.co.il/wp-json/wp/v2/pages/%d?_fields=id,link,modified,content&nlca=%d" % (pid, time.time())
        p = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-cityalign"}), timeout=90).read().decode("utf-8"))
        p["retrieved_utc"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    return p


def raw_risk(old, spans_tags):
    r = []
    if '"' in old:
        r.append("straight double quote")
    if "'" in old:
        r.append("apostrophe")
    if "–" in old:
        r.append("en dash")
    if "\n" in old:
        r.append("line break")
    if "  " in old:
        r.append("double space")
    if spans_tags:
        r.append("whole table: apply via anchor")
    elif "<" in old:
        r.append("contains tags")
    return r


# ---- table helpers -------------------------------------------------------------------------------------------------
def parse_table(h):
    """-> (header cells, [row cells]) as inner HTML strings"""
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", h, re.S)
    cells = [re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S) for r in rows]
    return cells[0], cells[1:]


def table_fmt(old):
    """(attribute string, separator between tags) of an existing table, so the rebuilt table keeps the page's own markup style"""
    attr = ' dir="rtl"' if old.startswith('<table dir="rtl"') else ""
    m = re.match(r"<table[^>]*>(\s*)<thead", old)
    return attr, m.group(1)


def table_html(head, body, fmt):
    attr, sep = fmt

    def tr(cs, tag):
        return f"<tr{attr}>" + sep + sep.join(f"<{tag}{attr}>{c}</{tag}>" for c in cs) + sep + "</tr>"
    return (f"<table{attr}>" + sep + f"<thead{attr}>" + sep + tr(head, "th") + sep + "</thead>" + sep + f"<tbody{attr}>" + sep
            + sep.join(tr(r, "td") for r in body) + sep + "</tbody>" + sep + "</table>")


# ---- the revised tier-2 edits ----------------------------------------------------------------------------------------
# SPEC[slug][n] = dict(action 'A'|'B'|'C', new=..., note=..., why=..., keys=[...], old=... (optional, widened), url=..., table=callable(old_html)->new_html,
#                     kept=[numbers already on the page], anchor=... (whole-table edits keep their anchor))
SPEC = {}


def spec(slug, n, **kw):
    SPEC.setdefault(slug, {})[n] = kw


H = "haifa-apartment-prices"
HZ = "herzliya-apartment-prices"
HOL = "holon-apartment-prices"
RG = "ramat-gan-apartment-prices"
PT = "petah-tikva-apartment-prices"
HOD = "hod-hasharon-apartment-prices"
JER = "jerusalem-apartment-prices"
KO = "kiryat-ono-apartment-prices"
EIL = "eilat-apartment-prices"
GIV = "givatayim-apartment-prices"
NET = "netanya-apartment-prices"
RAA = "raanana-apartment-prices"
RHS = "ramat-hasharon-apartment-prices"
RIS = "rishon-lezion-apartment-prices"

CBS_NAME = "הלשכה המרכזית לסטטיסטיקה"
Q2 = 'ברבעון השני של 2026 (אפריל עד יוני)'

# ===== HAIFA ==========================================================================================================
def haifa_rooms_table(old):
    head, rows = parse_table(old)
    notes = [r[2] for r in rows]  # usage notes of 1,2,3,4,5,6 rooms
    new_head = [head[0], 'שכר דירה חודשי ממוצע, אפריל עד יוני 2026 (הלמ"ס)', head[2]]
    body = [
        ["1 עד 2 חדרים", f'{r0(cbs("חיפה", "1-2"))} ש"ח',
         "מתאים להשוואת דירות קטנות ויחידות דיור, למשל בהדר, בת גלים ובאזורים סמוכים למוסדות לימוד, עם רגישות גבוהה למיקום"],
        ["2.5 עד 3 חדרים", f'{r0(cbs("חיפה", "2.5-3"))} ש"ח', notes[2]],
        ["3.5 עד 4 חדרים", f'{r0(cbs("חיפה", "3.5-4"))} ש"ח', notes[3]],
        ["4.5 חדרים ומעלה", f'{r0(cbs("חיפה", "4.5+"))} ש"ח', notes[4] + "; בנכסים גדולים, יוקרתיים או חריגים כדאי לבדוק בזהירות"],
    ]
    return table_html(new_head, body, table_fmt(old))


spec(H, 10, action="A", table=haifa_rooms_table,
     keys=[cbs_key("חיפה", g) for g in ("1-2", "2.5-3", "3.5-4", "4.5+")], url=RENT_URL,
     why=("Rent by rooms: the unsourced 'estimated monthly rent' column (2,187-10,400) is replaced by the CBS average monthly rent in Haifa by size group, "
          "Q2 2026 (table 4.9: 1-2 rooms 2,477.9; 2.5-3 3,118.5; 3.5-4 4,060.6; 4.5+ 5,420.3, rounded to whole shekels). The six rows become the four CBS size "
          "groups (1 and 2 rooms merged, 5 and 6 merged); the usage notes stay word for word, the two merged pairs joined. Tier 2 under the CEO rule."),
     note="replaced the 6-row rent column with the CBS average rent for Haifa by size group (1-2, 2.5-3, 3.5-4, 4.5+ rooms), Q2 2026: 2,478 / 3,119 / 4,061 / 5,420 ש\"ח; rows regrouped to the CBS groups, usage notes kept")

spec(H, 11, action="A",
     old=('בחיפה, שכירות חציונית סביב 3,400 ש"ח וממוצעת סביב 3,867 ש"ח יוצרת נקודת ייחוס כללית. אם דירת 3 חדרים מוצעת במחיר של 1,250,000 ש"ח '
          'ומושכרת סביב 3,820 ש"ח, אפשר לבדוק האם היחס סביר ביחס לאזור.'),
     new=(f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בחיפה {Q2} היה {r0(cbs("חיפה"))} ש"ח, והוא יוצר נקודת ייחוס כללית. '
          f'אם דירת 3 חדרים מוצעת במחיר של 1,250,000 ש"ח ומושכרת סביב {r0(cbs("חיפה", "2.5-3"))} ש"ח, הממוצע לדירות של 2.5 עד 3 חדרים באותו רבעון, '
          'אפשר לבדוק האם היחס סביר ביחס לאזור.'),
     keys=[cbs_key("חיפה"), cbs_key("חיפה", "2.5-3"), "page"], url=RENT_URL, kept=["1,250,000"],
     why=("Unsourced rent median 3,400 / average 3,867 replaced by the CBS average rent in Haifa, Q2 2026 (3,405.4). The old sentence widened by the next one: its "
          "'3,820' was the removed table figure for 3 rooms; it becomes the CBS 2.5-3 rooms average (3,118.5). The hypothetical 1,250,000 offer stays as the page had it."),
     note="replaced rent 'median 3,400 / average 3,867' with the CBS average 3,405 ש\"ח (Haifa, Q2 2026); the example sentence's 3,820 rent became the CBS 2.5-3 rooms average 3,119")

spec(H, 12, action="C",
     table=lambda old: table_html(*(lambda h, rows: ([h[0], h[2]], [[r[0], r[2]] for r in rows]))(*parse_table(old)), table_fmt(old)),
     keys=["page"],
     why=("Rent by neighbourhood (2,348-3,015): the CBS publishes no neighbourhood rent, so the rent column is deleted. The 'what to check' column is advice, makes no "
          "price-level claim and stays word for word. Tier 2 under the CEO rule."),
     note="deleted the neighbourhood rent column (no official neighbourhood rent exists); the 'what to check' notes stay")

spec(H, 17, action="B",
     why="Renovation cost 150,000-400,000 has no official source: the number is removed, the caution stays (advice, no price claim).",
     note="removed the renovation cost range 150,000-400,000 (no official source); caution sentence kept")
spec(H, 24, action="A",
     new=(f'שכר הדירה הממוצע בחיפה, {r0(cbs("חיפה"))} ש"ח בחודש {Q2.replace("(אפריל עד יוני)", "").strip()} לפי {CBS_NAME}, '
          'יכול לעזור לבדוק סבירות, אבל מחיר הדירה נקבע גם לפי מיקום, שטח, מצב, זכויות וביקוש קונים.'),
     keys=[cbs_key("חיפה")], url=RENT_URL,
     why="FAQ rent: median 3,400 / average 3,867 (no source) replaced by the CBS average rent in Haifa, Q2 2026 (3,405.4), same as edit 11.",
     note="replaced rent 'median 3,400 / average 3,867' with the CBS average 3,405 ש\"ח (Haifa, Q2 2026)")
spec(H, 25, action="B",
     why="FAQ renovation cost 150,000-400,000 has no official source: the number is removed, the caution stays (same as edit 17).",
     note="removed the renovation cost range 150,000-400,000 (no official source); caution sentence kept")

# ===== HERZLIYA =======================================================================================================
spec(HZ, 1, action="B",
     new=('אין להרצליה מחיר אחד: מרכז העיר, הרצליה הצעירה, הרצליה ב\', הירוקה, גליל ים, נוה עמל, נוף ים, המרינה והרצליה פיתוח מתנהגים כשווקים שונים, '
          'ולכן גם דירות באותו מספר חדרים נמכרות במחירים שונים לפי האזור.'),
     why=("A spread 'of hundreds of thousands and even more than a million' between two flats with the same room count has no official source: the amount is removed "
          "and the sentence says only what it can support, that prices differ by area. Tier 2 under the CEO rule."),
     note="removed 'hundreds of thousands, even over a million' (no official source); the sentence now only says that same-size flats sell at different prices by area")
spec(HZ, 4, action="B",
     why="City per-m2 average 34,000-38,000 has no official source and no date on the page: the number is removed, the advice to check 5-10 similar deals stays.",
     note="removed the city per-m2 figure 34,000-38,000 (no official source); the advice stays")
spec(HZ, 10, action="A",
     new=(f'לפי {CBS_NAME}, שכר הדירה החודשי הממוצע בהרצליה {Q2} היה {r0(cbs("הרצליה"))} ש"ח. '
          'אפשר להשתמש בשכירות כדי לבדוק אם מחיר מכירה נראה סביר ביחס לביקוש למגורים באזור.'),
     keys=[cbs_key("הרצליה")], url=RENT_URL,
     why=("Undated rents for 3 rooms (6,500-6,800) and 4 rooms (7,500-8,500) replaced by the CBS average rent in Herzliya, Q2 2026 (all sizes 6,774.5; the size groups "
          "follow in edits 11, 12 and 16). Tier 2 under the CEO rule."),
     note="replaced rents 6,500-6,800 (3 rooms) and 7,500-8,500 (4 rooms) with the CBS average rent for Herzliya, Q2 2026: 6,775 ש\"ח")
spec(HZ, 11, action="A",
     new=(f'לפי הלמ"ס, ברבעון השני של 2026 שכר הדירה הממוצע בהרצליה נע מ-{r0(cbs("הרצליה", "1-2"))} ש"ח לדירות של 1 עד 2 חדרים ועד {r0(cbs("הרצליה", "4.5+"))} ש"ח '
          'לדירות של 4.5 חדרים ומעלה, והטבלה שלהלן מפרטת את כל קבוצות הגודל. '
          'הפער בין דירות קטנות לדירות גדולות מסביר מדוע צריך לקרוא את השכירות לפי גודל הדירה ולפי אזור ולא רק לפי עיר.'),
     keys=[cbs_key("הרצליה", "1-2"), cbs_key("הרצליה", "4.5+")], url=RENT_URL,
     why=("Rent median 7,200 / average 7,661 / 3 rooms 6,686 and the undated per-room list (5,500, 6,800, 8,500, 12,200) replaced by the CBS range across Herzliya size "
          "groups, Q2 2026 (1-2 rooms 4,443.9 to 4,5+ rooms 9,460.5); the median is gone because the CBS publishes no median rent. Tier 2 under the CEO rule."),
     note="replaced the unsourced rent median / average / per-room list with the CBS size-group range for Herzliya, Q2 2026: 4,444 (1-2 rooms) to 9,461 (4.5+ rooms); median dropped (the CBS publishes none)")


def herzliya_rent_table(old):
    head, rows = parse_table(old)
    by = {r[0].strip(): r for r in rows}
    avg, two, three, four, five = (by["ממוצע עירוני בהרצליה"], by["2 חדרים"], by["3 חדרים"], by["4 חדרים"], by["5 חדרים"])
    new_head = [head[0], 'שכר דירה חודשי ממוצע, אפריל עד יוני 2026 (הלמ"ס)', head[2], head[3]]
    body = [
        [avg[0], f'{r0(cbs("הרצליה"))} ש"ח', avg[2], avg[3].replace("להשוות לחציון, לאזור", "להשוות לאזור")],
        ["1 עד 2 חדרים", f'{r0(cbs("הרצליה", "1-2"))} ש"ח', two[2], two[3]],
        ["2.5 עד 3 חדרים", f'{r0(cbs("הרצליה", "2.5-3"))} ש"ח',
         'שכירות כזו, מול חציון מחיר העסקה לדירת 3 חדרים (2,793,600 ש"ח ברבעון הראשון של 2026), מאפשרת לבדוק אם המחיר המבוקש סביר, בכפוף לאזור ולמצב הדירה.',
         three[3]],
        ["3.5 עד 4 חדרים", f'{r0(cbs("הרצליה", "3.5-4"))} ש"ח', four[2], four[3]],
        ["4.5 חדרים ומעלה", f'{r0(cbs("הרצליה", "4.5+"))} ש"ח', five[2], five[3]],
    ]
    return table_html(new_head, body, table_fmt(old))


spec(HZ, 12, action="A", table=herzliya_rent_table,
     keys=[cbs_key("הרצליה", g) for g in ("total", "1-2", "2.5-3", "3.5-4", "4.5+")] + ["rooms.3.latest"], url=RENT_URL,
     why=("Rent table (12 rows, no source, no date) rebuilt on the CBS average rent in Herzliya, Q2 2026: city average 6,774.5 and the four size groups (1-2: 4,443.9; "
          "2.5-3: 5,605.7; 3.5-4: 7,040.8; 4.5+: 9,460.5). Deleted: the median row (the CBS publishes no median rent) and the six neighbourhood rows (Neve Israel, Herzliya "
          "Hatzeira, Nof Yam, Herzliya B, Marina, Pituach: no official neighbourhood rent, and their readings were price-level claims). The 3-room reading keeps the official "
          "sale median 2,793,600 (1-3.2026). Tier 2 under the CEO rule."),
     note="rebuilt the rent table on the CBS Herzliya figures (city 6,775; 1-2: 4,444; 2.5-3: 5,606; 3.5-4: 7,041; 4.5+: 9,461 ש\"ח, Q2 2026); median row and 6 neighbourhood rows deleted (no official source)")
spec(HZ, 13, action="B",
     why="City per-m2 range 34,000-38,000 repeated: the number is removed, the question the reader should ask stays.",
     note="removed the city per-m2 figure 34,000-38,000 (no official source); the advice stays")
spec(HZ, 15, action="B",
     new='מחיר למ"ר בהרצליה משתנה לפי אזור, גודל וסוג נכס, ולכן אין מספר עירוני אחד שאפשר להשתמש בו לבד.',
     why="FAQ per-m2: the undated 34,000-38,000 range is removed; the answer says only that no single city figure should be used alone.",
     note="removed the city per-m2 range 34,000-38,000 (no official source); the answer now says no single city figure fits")
spec(HZ, 16, action="A",
     new=(f'לפי {CBS_NAME}, {Q2} שכר הדירה החודשי הממוצע בהרצליה היה {r0(cbs("הרצליה", "1-2"))} ש"ח לדירות של 1 עד 2 חדרים, '
          f'{r0(cbs("הרצליה", "2.5-3"))} ש"ח לדירות של 2.5 עד 3 חדרים, {r0(cbs("הרצליה", "3.5-4"))} ש"ח לדירות של 3.5 עד 4 חדרים '
          f'ו-{r0(cbs("הרצליה", "4.5+"))} ש"ח לדירות של 4.5 חדרים ומעלה.'),
     keys=[cbs_key("הרצליה", g) for g in ("1-2", "2.5-3", "3.5-4", "4.5+")], url=RENT_URL,
     why="FAQ rent by rooms (5,000-12,200, no source, no date) replaced by the CBS average rent in Herzliya by size group, Q2 2026.",
     note="replaced the undated per-room rent list with the CBS Herzliya size-group averages, Q2 2026: 4,444 / 5,606 / 7,041 / 9,461 ש\"ח")

# ===== HOLON (uses the Hebrew gershayim U+05F4 in m2 and ₪) =========================================================
spec(HOL, 3, action="B",
     new='פער של 10 מ״ר בלבד כבר משנה את המחיר, ולכן משווים דירות בשטח דומה.',
     why=("The 250,000-350,000 effect of 10 m2 and the 25,000-29,000 per m2 it rested on have no official source (the per-m2 range came from private data sites): "
          "both numbers are removed, the 10 m2 stays as the example size and the advice to compare flats of similar size stays. Tier 2 under the CEO rule."),
     note="removed 250,000-350,000 and the per-m2 range 25,000-29,000 (no official source); the 10 m2 example and the advice stay")
spec(HOL, 4, action="B",
     why="A 5%-12% gap between a low floor and a flat with balcony, parking and access has no official source: the number is removed, the hedged sentence stays.",
     note="removed the 5%-12% floor / balcony gap (no official source); hedged sentence kept")
spec(HOL, 12, action="B",
     new='מחיר גבוה מדירת יד שנייה דומה יכול להיות סביר במקרים מסוימים, אך הוא לא אוטומטי.',
     why="An 8%-20% new-flat premium has no official source: the number is removed, the sentence stays as a hedged caution.",
     note="removed the 8%-20% new-flat premium (no official source); hedged sentence kept")
spec(HOL, 14, action="B",
     why="A renovation cost 80,000-300,000 in a table cell has no official source: the number is removed, the cell says a renovation may be needed.",
     note="removed the renovation cost 80,000-300,000 (no official source); cell kept as 'a renovation may be needed'")
spec(HOL, 15, action="B",
     why="A 50,000-250,000 effect of the deals check on the offer has no official source: the number is removed, the cell stays.",
     note="removed the 50,000-250,000 effect on the offer (no official source); cell kept")
spec(HOL, 16, action="B",
     why="A renovation cost 80,000-300,000 has no official source: the number is removed, the cell stays as advice.",
     note="removed the renovation cost 80,000-300,000 (no official source); cell kept as advice")
spec(HOL, 20, action="B",
     why="The 8%-20% new-flat premium again, no official source: the number is removed, the hedged sentence stays.",
     note="removed the 8%-20% new-flat premium (no official source); hedged sentence kept")

# ===== RAMAT GAN ======================================================================================================
spec(RG, 1, action="A",
     new='19.5%, לפי נתוני הלמ"ס ליולי 2025',
     keys=["cbs_dwellings[מחוז תל אביב].share_2025"], url=DWELL_URL, kept=["19.5"],
     why=("The share of the Tel Aviv district in Israel's dwellings is official: 19.5% in 2025 (CBS press release 021/2026 of 19.1.2026, dwelling register as of July 2025). "
          "The same value now carries its source and period. Tier 2 under the CEO rule."),
     note="kept 19.5% and added its official source and period: CBS dwelling register, July 2025 (press release 021/2026, 19.1.2026)")
spec(RG, 6, action="B",
     new=('דירת יד שנייה יכולה להיות זולה יותר במחיר הכולל, אך לדרוש שיפוץ ולעיתים גם התאמות תשתית, '
          'ואת עלות השיפוץ כדאי לתמחר מראש לפי הצעות מחיר.'),
     why="Renovation cost 150,000-500,000 has no official source: the number is removed, the advice to price the work from quotes stays.",
     note="removed the renovation cost 150,000-500,000 (no official source); advice to price it from quotes kept")
spec(RG, 7, action="B",
     why="A 5%-20% second-hand discount has no official source: the number is removed, the cell stays as a hedged 'sometimes lower'.",
     note="removed the 5%-20% second-hand discount (no official source); cell kept as a hedged 'sometimes lower'")
spec(RG, 8, action="B",
     new='בודקים מול עסקאות סגורות של דירות יד שנייה באותו אזור',
     why=("Second-hand per-m2 range 30,000-38,000 has no official source: the number is removed and the cell becomes the check to run (a statement 'usually lower than new' "
          "would be a price-level claim without an official figure)."),
     note="removed the second-hand per-m2 range 30,000-38,000 (no official source); cell now says what to compare against")
spec(RG, 9, action="B",
     new='בודקים מול עסקאות בפרויקטים חדשים דומים',
     why="New-flat per-m2 range 40,000-55,000 has no official source: the number is removed and the cell becomes the check to run.",
     note="removed the new-flat per-m2 range 40,000-55,000 (no official source); cell now says what to compare against")
spec(RG, 10, action="B",
     new='עלול לדרוש שיפוץ, לפי מצב הדירה',
     why="Renovation cost 150,000-500,000 in a table cell has no official source: the number is removed, the cell says a renovation may be needed.",
     note="removed the renovation cost 150,000-500,000 (no official source); cell kept as 'may need a renovation'")
spec(RG, 12, action="B",
     new='לעיתים פער בין מחיר מבוקש למחיר סביר יכול להיות תוצאה של משא ומתן, ולעיתים הפער גדול יותר.',
     why="An asking-to-reasonable gap of 3%-8% has no official source: the number is removed, the sentence stays.",
     note="removed the 3%-8% asking-price gap (no official source); sentence kept")

# ===== PETAH TIKVA ====================================================================================================
spec(PT, 1, action="B",
     why="A new-vs-second-hand premium of 8%-22% has no official source: the number is removed, the cell says it varies by project, specification and delivery date.",
     note="removed the 8%-22% new-vs-second-hand premium (no official source); cell says it varies by project")
spec(PT, 7, action="B",
     new='עשוי להיות גבוה מדירה לא משופצת דומה, לפי איכות השיפוץ',
     why="A renovation premium of 5%-12% has no official source: the number is removed, the cell stays hedged.",
     note="removed the 5%-12% renovation premium (no official source); cell kept hedged")
spec(PT, 8, action="B",
     new='עשוי להיות גבוה מיד שנייה דומה, לפי מפרט, מיקום וגיל הבניין',
     why="A new-flat premium of 8%-18% has no official source: the number is removed, the cell stays hedged.",
     note="removed the 8%-18% new-flat premium (no official source); cell kept hedged")
spec(PT, 9, action="B",
     new='משתנה לפי פרויקט ומועד מסירה',
     why="An off-plan premium of 10%-22% has no official source: the number is removed, the cell says it varies by project and delivery date.",
     note="removed the 10%-22% off-plan premium (no official source); cell says it varies by project")
spec(PT, 13, action="B",
     new='במקרים מסוימים הפער קטן, ובמקרים אחרים גדול, בעיקר כאשר המודעה יקרה ביחס לעסקאות.',
     why="Asking-to-deal gaps of 2%-4% and 8%-12% have no official source: the numbers are removed, the sentence stays.",
     note="removed the 2%-4% and 8%-12% asking-to-deal gaps (no official source); sentence kept")

# ===== HOD HASHARON ===================================================================================================
spec(HOD, 10, action="B",
     new='עם זאת, דירה ותיקה יכולה לדרוש שיפוץ, ולעיתים גם טיפול בצנרת, חשמל, איטום, מטבח ומיזוג.',
     why="Renovation cost 150,000-400,000 has no official source or date: the number is removed ('hundreds of thousands' would still be a number), the sentence stays.",
     note="removed the renovation cost 150,000-400,000 (no official source); sentence kept")
spec(HOD, 12, action="B",
     new='יכול לשנות מחיר, לפי היקף העבודה',
     why="The same renovation range in the factors table: the number is removed, the cell stays.",
     note="removed the renovation cost 150,000-400,000 (no official source); cell kept")
spec(HOD, 20, action="C",
     why=("Two single-address prices (אסירי ציון 19 about 3,450,000; שדרות הנשיאים 42 about 3,650,000) have no deal date, no area and no official source: the two rows are "
          "deleted. The three dated deals (May 2026) stay word for word."),
     note="deleted the two undated single-address price rows (אסירי ציון 19, שדרות הנשיאים 42); the three dated May 2026 deals stay")

# ===== JERUSALEM ======================================================================================================
spec(JER, 11, action="B",
     why="A 10%-25% new-flat per-m2 premium has no official source: the number is removed, the cell stays as a hedged 'sometimes higher'.",
     note="removed the 10%-25% new-flat per-m2 premium (no official source); cell kept hedged")
spec(JER, 12, action="B",
     new='יכול להיות נמוך יותר, אך שיפוץ יכול להוסיף לעלות הכוללת',
     why="Renovation cost 150,000-600,000 has no official source ('hundreds of thousands' would still be a number): the number is removed, the cell stays.",
     note="removed the renovation cost 150,000-600,000 (no official source); cell kept")
spec(JER, 13, action="B",
     new='התעלמות מעלויות שיפוץ.',
     why="The same renovation range in the steps table: the number is removed, the 'common mistake' stays.",
     note="removed the renovation cost 150,000-600,000 (no official source); 'common mistake' cell kept")

# ===== KIRYAT ONO =====================================================================================================
spec(KO, 14, action="B",
     new='ייתכן צורך בשיפוץ, ועלותו נקבעת לפי הצעות מחיר',
     why="Renovation cost 100,000-300,000 has no official source: the number is removed, the cell says a renovation may be needed and that quotes set its cost.",
     note="removed the renovation cost 100,000-300,000 (no official source); cell kept as 'quotes set the cost'")
spec(KO, 15, action="B",
     new='שתי דירות באותו רחוב בקריית אונו יכולות להימכר במחירים שונים, בגלל הבדלים פנימיים.',
     why="Same-street gaps of 300,000 and 500,000 have no official source ('hundreds of thousands' would still be a number): the numbers are removed, the sentence stays.",
     note="removed same-street gaps 300,000 / 500,000 (no official source); sentence kept")
spec(KO, 16, action="B",
     new='ייתכן פער בין מחיר מבוקש למחיר סגירה',
     why="An asking-to-closing gap of 2-8 percent has no official source: the number is removed, the cell stays.",
     note="removed the 2-8 percent asking-to-closing gap (no official source); cell kept")

# ===== EILAT ==========================================================================================================
spec(EIL, 14, action="C",
     old=('מולו, מקור ישן או אגרגטיבי יותר בהקשר דירות חדשות וקבלן הציג נתוני שכירות נמוכים יותר: 2 חדרים 1,341 ₪ ותשואה 5.1%, 3 חדרים 1,998 ₪ ותשואה 4.6%, '
          '4 חדרים 2,321 ₪ ותשואה 3.7%, ו-5 חדרים 3,096 ₪ ותשואה 3.4%. כאשר מקורות שונים מציגים פערים כאלה, לא בוחרים מספר אחד לפי הנוחות.'),
     new='כאשר מקורות שונים מציגים נתוני שכירות שונים, לא בוחרים מספר אחד לפי הנוחות.',
     why=("Rents 1,341-3,096 and yields 3.4%-5.1% from a source the page itself calls old, with no date and no official counterpart (the CBS has no Eilat figure): the sentence "
          "is deleted. The next sentence pointed at 'such gaps' and is widened to stand alone. Tier 2 under the CEO rule."),
     note="deleted the sentence with the old-source rents 1,341-3,096 and yields 3.4%-5.1% (undated, no official counterpart: the CBS has no Eilat figure); the next sentence made self-standing")


def eilat_table(old):
    head, rows = parse_table(old)
    new_head = [head[0], head[1], head[3]]
    body = [[r[0], r[1], r[3]] for r in rows]
    for r in body:
        if r[2].startswith("פער המקורות מחייב"):
            r[2] = "כדאי לבדוק מודעות פעילות ועסקאות שכירות בפועל"
    return table_html(new_head, body, table_fmt(old))


spec(EIL, 15, action="C", table=eilat_table,
     keys=["page"],
     why=("Rent table: the column of the undated old source (rents and yields) is deleted; the current asking-rent column (page checked 6.6.2026) and the buyer notes stay. "
          "The note 'the gap between the sources requires...' pointed at the deleted column and becomes 'worth checking active listings and actual rental deals'. "
          "Tier 2 under the CEO rule."),
     note="deleted the old-source rent and yield column (undated, no official counterpart); the note that pointed at the gap between sources reworded")

# ===== GIVATAYIM / NETANYA / RAANANA / RAMAT HASHARON / RISHON ========================================================
spec(GIV, 11, action="B",
     new='ייתכן צורך בשיפוץ, לפי מצב הדירה',
     why="Renovation cost 150,000-500,000 has no official source or date: the number is removed, the cell says a renovation may be needed.",
     note="removed the renovation cost 150,000-500,000 (no official source); cell kept")
spec(NET, 5, action="B",
     new='בודקים מול עסקאות דומות של דירות גן או גג באותו אזור',
     why=("A 10%-30% garden / roof premium has no official source: the number is removed and the cell becomes the check to run (a statement 'usually higher' would be a "
          "price-level claim without an official figure)."),
     note="removed the 10%-30% garden / roof premium (no official source); cell now says what to compare against")
spec(RAA, 3, action="B",
     why="Renovation cost 150,000-400,000 has no official source or date: the number is removed, the sentence stays.",
     note="removed the renovation cost 150,000-400,000 (no official source); sentence kept")
spec(RAA, 4, action="B",
     new='עשוי לדרוש שיפוץ, לפי מצב הדירה',
     why="Renovation cost 150,000-500,000 has no official source or date: the number is removed, the cell says a renovation may be needed.",
     note="removed the renovation cost 150,000-500,000 (no official source); cell kept")
spec(RHS, 8, action="B",
     why="Renovation cost 250,000-600,000 has no official source: the number is removed, the sentence stays.",
     note="removed the renovation cost 250,000-600,000 (no official source); sentence kept")
spec(RHS, 10, action="B",
     new='פער בעלויות השיפוץ יכול להסביר פער במחיר.',
     why="A renovation cost gap of 200,000-700,000 has no official source: the numbers are removed, the sentence stays.",
     note="removed the renovation cost gap 200,000-700,000 (no official source); sentence kept")
spec(RIS, 3, action="B",
     why="Renovation cost 100,000-250,000 has no official source: the number is removed, the sentence stays.",
     note="removed the renovation cost 100,000-250,000 (no official source); sentence kept")
spec(RIS, 6, action="B",
     why="Renovation cost 80,000-300,000 in a table cell has no official source: the number is removed, the cell stays.",
     note="removed the renovation cost 80,000-300,000 (no official source); cell kept")

ACTION_WORD = {"A": "replaced", "B": "removed", "C": "deleted"}


def main():
    summary = []
    for fn in sorted(os.listdir(OUTDIR)):
        if not fn.endswith(".align-edits.json"):
            continue
        slug = fn[:-len(".align-edits.json")]
        path = os.path.join(OUTDIR, fn)
        raw = io.open(path, encoding="utf-8", newline="").read()
        J = json.loads(raw)
        t2 = [e for e in J["edits"] if e.get("tier") == 2]
        if not t2:
            continue
        assert slug in SPEC, slug
        assert sorted(SPEC[slug]) == sorted(e["n"] for e in t2), (slug, sorted(SPEC[slug]), [e["n"] for e in t2])
        page = load_live(slug, J["page"]["id"])
        live = page["content"]["rendered"]
        text = live
        for e in J["edits"]:
            if e.get("tier") != 2:
                continue
            s = SPEC[slug][e["n"]]
            old = s.get("old", e["old"])
            if "table" in s:
                anchor = e["anchor"]
                assert text.count(anchor) == 1, (slug, e["n"], "anchor", text.count(anchor))
                i = text.find(anchor)
                a, z = text.rfind("<table", 0, i), text.find("</table>", i)
                cur = text[a:z + len("</table>")]
                assert cur == e["old"] == old, (slug, e["n"], "table old differs from the live table")
                new = s["table"](cur)
                text = text[:a] + new + text[z + len("</table>"):]
            else:
                assert text.count(old) == 1, (slug, e["n"], "old matches", text.count(old), old[:80])
                new = s.get("new", e["new"])
                text = text.replace(old, new)
            e["old"] = old
            e["new"] = new
            e["why"] = s["why"]
            if "keys" in s:
                e["source_keys"] = s["keys"]
            if "kept" in s:
                e["kept_numbers"] = s["kept"]
            e["matches_in_live"] = 1
            e["raw_risk"] = raw_risk(old, bool(e.get("spans_tags")))
            e["ceo_action"] = ACTION_WORD[s["action"]]
            e["ceo_note"] = s["note"]
            if s.get("url"):
                e["source_url"] = s["url"]
            elif "source_url" in e:
                del e["source_url"]
            summary.append((slug, e["n"], s["action"], s["note"], s.get("url")))
        J["apply_rules"] = [r for r in J["apply_rules"] if not r.startswith("Tier 2 under the CEO rule")] + [
            "Tier 2 under the CEO rule (7.10.2026): apply AFTER tier 1 (tier 1 is already live on this page), on the live content, in the listed order. Each tier-2 "
            "edit carries ceo_action (replaced = an official dated value now stands there, with its source_url; removed = number gone, sentence or cell kept; deleted = "
            "sentence, row or column gone) and ceo_note."]
        J["tier2_ceo_recheck"] = {"retrieved_utc": page.get("retrieved_utc"), "modified": page.get("modified"), "result": RECHECK_NOTE,
                                 "edits": len(t2), "replaced": sum(1 for e in t2 if e["ceo_action"] == "replaced"),
                                 "removed": sum(1 for e in t2 if e["ceo_action"] == "removed"),
                                 "deleted": sum(1 for e in t2 if e["ceo_action"] == "deleted")}
        out = json.dumps(J, ensure_ascii=False, indent=1) + "\n"
        if not DRY:
            io.open(path, "w", encoding="utf-8", newline="\n").write(out)
        print(f"{slug}: {len(t2)} tier-2 edits rebuilt ({'dry' if DRY else 'written'})")
    print(len(summary), "edits", {a: sum(1 for x in summary if x[2] == a) for a in "ABC"})


if __name__ == "__main__":
    main()
