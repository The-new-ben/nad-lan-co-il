# -*- coding: utf-8 -*-
"""G5 rentals hub (Ben 26.10.2026: a winning owner page for "דירות להשכרה" / "דירה להשכרה"): data for the tool "rentfair"
("כמה שכר דירה הוגן לדירה הזאת"), assets/instruments/data/rent.json. NEW file, local only until a release.

Joins three official feeds and the law, every value with its period and its source:
  1. data.nadlan.gov.il settlement rent files (the government real-estate site, "מחיר חציוני"), version 20-08-2026, as fetched by
     the U2 research on 25.10.2026 (docs/research/2026-10-26-upgrades/u2-investment/fetch_nadlan_gov.py, 1 request a second):
     per city the median rent for 3 / 4 / 5 / all rooms for 22 quarters (to April to June 2026), the file's own last-year figure and
     its yearly change, and the median rent of every neighbourhood the file lists (all sizes).
  2. CBS price bulletin, table 4.9: the average free-market rent with its sampling error, 20 cities + 6 districts + Israel, room
     groups 1-2 / 2.5-3 / 3.5-4 / 4.5+, 2024 Q4 to 2026 Q2 (the research parse docs/.../u2-investment/data/cbs-rent-table-4-9-2026q2.json).
  3. CBS API, rent index 120460 (monthly change and change over 12 months, to September 2026).
  4. The law and the tax rules, each with its source (Rental and Loan Law 5731-1971, chapter 2 sign 6 as amended 5777-2017, 5783 and
     5786, Nevo text current to 30.9.2026 and Wikisource; Kol Zchut pages on the rental-income tax tracks, updated 22.2.2026).
Nothing is estimated in the file. The tool's own calculations (a neighbourhood x rooms figure, the median carried to September by
the index) are done in the browser and labelled there as ours.

  python tools/instruments/build_rent_data.py            # build from the research raw files (fetched 25.10.2026)
  python tools/instruments/build_rent_data.py --out X    # write elsewhere (compare a fresh fetch with the published file)
Checks on every build: Tel Aviv 3 rooms April to June 2026 = 8,250; Israel 4 rooms = 4,825; CBS Israel total Q2 2026 = 5,085.5;
every city has at least one room size; the national series equals the countryPrice of every city file."""
import glob, io, json, os, sys

if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PRIV = os.path.abspath(os.path.join(R, "..", "_private-research", "2026-10-26-upgrades", "raw"))
GOV = os.path.join(PRIV, "u2", "data", "nadlan-gov")
CBS_TABLE = os.path.join(R, "docs", "research", "2026-10-26-upgrades", "u2-investment", "data", "cbs-rent-table-4-9-2026q2.json")
CBS_IDX = os.path.join(PRIV, "u2", "data", "cbs_120460.json")
DATA = os.path.join(R, "plugins", "nadlan-config", "assets", "instruments", "data")
OUT = os.path.join(DATA, "rent.json")
if "--out" in sys.argv: OUT = os.path.abspath(sys.argv[sys.argv.index("--out") + 1])

inv = json.load(io.open(os.path.join(DATA, "invest.json"), encoding="utf-8"))
NAMES = {r["code"]: r["n"] for r in inv["rows"]}  # the names the other tools use (U2 normalised them)
FIX = {"רהט": "רהט", "אום אל-פחם": "אום אל-פחם"}


def qk(e): return "%d-%02d" % (e["year"], e["month"])


def num(x):
    try: return float(str(x).replace(",", "").strip())
    except (TypeError, ValueError): return None


# ---------------------------------------------------------------- 1. government median rents
cities, nat, nat_series, version = [], None, {}, set()
for f in sorted(glob.glob(os.path.join(GOV, "rent_*.json"))):
    x = json.load(io.open(f, encoding="utf-8-sig"))
    version.add(x.get("version"))
    code = int(x["settlementID"]); name = NAMES.get(code) or FIX.get(x["settlementName"].strip(), x["settlementName"].replace(" -", "-").strip())
    rooms = {}
    for r in x["trends"]["rooms"]:
        k = str(r["numRooms"])
        ser = [[qk(e), int(e["settlementPrice"])] for e in r["graphData"] if e.get("settlementPrice")]
        nser = [[qk(e), int(e["countryPrice"])] for e in r["graphData"] if e.get("countryPrice")]
        for q, v in nser:  # the national median is printed in every city file; it must agree everywhere
            nat_series.setdefault(k, {}).setdefault(q, set()).add(v)
        if not ser: continue
        ser.sort()
        sm = r.get("summary") or {}
        rooms[k] = {"q": ser[-1][0], "v": ser[-1][1], "ly": int(sm["lastYearAvgPrice"]) if sm.get("lastYearAvgPrice") else None,
                    "yoy": num(sm.get("priceDifferencePercentage")), "s": ser[-12:]}
    if not rooms: continue
    nb = sorted([[n["title"].strip(), int(round(n["price"]))] for n in (x.get("neighborhoodsPrices") or []) if n.get("price")], key=lambda a: -a[1])
    cities.append({"n": name, "code": code, "r": rooms, "nb": nb})
cities.sort(key=lambda c: c["n"])
natr = {}
for k, qs in nat_series.items():
    for q, vals in qs.items():
        assert len(vals) == 1, ("national median differs between city files", k, q, vals)
    ser = sorted([q, list(v)[0]] for q, v in qs.items())
    natr[k] = {"q": ser[-1][0], "v": ser[-1][1], "s": ser[-12:]}
nat = {"n": "ישראל", "code": 0, "r": natr}

# ---------------------------------------------------------------- 2. CBS table 4.9
cbs_rows = json.load(io.open(CBS_TABLE, encoding="utf-8"))
CBS_NAME = {"תל אביב": "תל אביב-יפו", "פתח תקוה": "פתח תקווה"}
G = ["1-2", "2.5-3", "3.5-4", "4.5+", "total"]
cbs = {}
for t in cbs_rows:
    nm = CBS_NAME.get(t["area"], t["area"])
    g = t["rooms"]
    if g not in G: continue
    rec = {"a": num(t.get("2026Q2_avg")), "e": num(t.get("2026Q2_err")), "a1": num(t.get("2026Q1_avg")), "p": num(t.get("2025Q2_avg")),
           "y25": num(t.get("2025Y_avg"))}
    if rec["a"] is None: continue
    cbs.setdefault(nm, {})[g] = rec
by = {c["n"]: c for c in cities}
cbs_city = 0
for nm, rec in cbs.items():
    if nm in by: by[nm]["cbs"] = rec; cbs_city += 1
nat["cbs"] = cbs["ישראל"]
dist = [{"n": nm, "cbs": rec} for nm, rec in cbs.items() if nm.startswith("מחוז")]

# ---------------------------------------------------------------- 3. CBS rent index
ix = json.load(io.open(CBS_IDX, encoding="utf-8-sig"))["month"][0]
ser = sorted(["%d-%02d" % (d["year"], d["month"]), d["percent"], d["percentYear"]] for d in ix["date"])
idx = {"name": ix["name"], "code": 120460, "last": ser[-1][0], "mom": ser[-1][1], "yoy": ser[-1][2], "s": ser,
       "base": ix["date"][0]["currBase"]["baseDesc"], "v": ix["date"][0]["currBase"]["value"]}

# ---------------------------------------------------------------- 4. the law and the tax rules
law = {
    "guarantee": {"months": 3, "share": 1 / 3, "returnDays": 60,
                  "what": "ערבות בנקאית, ערבות מנותן ערבות אחר (בעל רישיון למתן אשראי, לשירותי פיקדון ואשראי, לשירותי תשלום יציבותי, או מבטח) או מזומן",
                  "uses": ["דמי שכירות שלא שולמו, עם הצמדה וריבית לפי החוזה", "ליקויים שהשוכר אחראי להם ולא תיקן, עד עלות התיקון",
                           "ארנונה, מים, חשמל, גז וועד בית שלא שולמו", "אי פינוי הדירה בסוף התקופה, לפי החוזה"], "sec": "25י"},
    "repairs": {"urgent": 3, "other": 30, "sec": "25ח"},
    "notice": {"landlordOption": 90, "tenantOption": 60, "landlordCancel": 90, "tenantCancel": 60, "sec": "25יב, 25יג"},
    "scope": {"minMonths": 3, "maxYears": 10, "ceiling": 20000, "ceilingNote": "20,000 ₪ לפי נוסח החוק, מתעדכן ב־1 בינואר בכל שנה לפי מדד המחירים לצרכן ומעוגל ל־10 ₪", "sec": "25טו"},
    "tenantPays": ["דמי השכירות", "מסים החלים על המחזיק בדירה, ובהם ארנונה", "מים, חשמל, גז וחימום", "אחזקה שוטפת לוועד הבית או לחברת הניהול"],
    "tenantNot": ["רכישה או השבחה של מערכות ומיתקנים קבועים בדירה (אלא אם השוכר ביקש)", "ביטוח מבנה של הדירה", "דמי תיווך של מתווך שפעל מטעם המשכיר"],
    "unfit": ["אין ניקוז וסילוק סדיר של שפכים", "אין חשמל או תאורה", "אין פתחי אוורור ותאורה טבעית, דלתות וחלונות, ודלת כניסה ננעלת",
              "אין מים לשתייה", "אין מחיצה בין השירותים לדירה", "יש סיכון בלתי סביר לבטיחות או לבריאות"],
    "contract": ["כתובת הדירה", "שמות הצדדים, תעודות זהות ומענים", "תיאור הדירה, הריהוט והאבזרים והחלקים הצמודים מהרכוש המשותף",
                 "תקופת השכירות, אופציה להארכה ותנאיה, וזכות ביטול ותנאיה", "דמי השכירות, מועד התשלום ואופן התשלום",
                 "תשלומים נוספים על השוכר וגובהם", "פגמים וליקויים שהמשכיר יודע עליהם, ומטרדים בסביבה שהוא יודע עליהם"],
    "excluded": ["בית מלון או דירת נופש", "מעון", "דיור מוגן", "מעונות סטודנטים, תלמידים או עובדים", "דירה שחוק הגנת הדייר חל עליה",
                 "חוזה עד 3 חודשים בלי אופציה", "חוזה מעל 10 שנים בלי זכות ביטול למשכיר", "דמי שכירות מעל התקרה לחודש"],
}
tax = {"ceiling": 5654, "double": 11308, "year": 2026, "history": [[2022, 5196], [2023, 5471], [2024, 5654], [2025, 5654], [2026, 5654]],
       "ten": 0.10, "tenDue": "30.1.2027", "offsetCap": 7500, "first": 0.31, "first60": 0.10,
       "note": "הפטור מחושב לכל חודש בנפרד ועל סך שכר הדירה מכל הדירות; מסלול 10% בלי ניכוי הוצאות ופחת; במסלול הרגיל מנכים הוצאות ופחת ומשלמים לפי מדרגות, מ־31% (10% מגיל 60)"}
src = {
    "gov": {"he": "אתר הנדל״ן הממשלתי, שכר דירה חציוני לפי עיר, חדרים ושכונה, גרסה " + "/".join(sorted(v for v in version if v)), "url": "https://www.nadlan.gov.il/",
            "api": "https://data.nadlan.gov.il/api/pages/settlement/rent/{code}.json", "read": "2026-10-25"},
    "cbs49": {"he": "הלשכה המרכזית לסטטיסטיקה, ירחון המחירים, לוח 4.9: שכר דירה ממוצע בשוק החופשי, אפריל עד יוני 2026, עם טעות הדגימה", "url": "https://www.cbs.gov.il/he/subjects/Pages/%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D-%D7%9E%D7%9E%D7%95%D7%A6%D7%A2%D7%99%D7%9D-%D7%A9%D7%9C-%D7%A9%D7%9B%D7%A8-%D7%93%D7%99%D7%A8%D7%94.aspx"},
    "cbsIdx": {"he": "הלשכה המרכזית לסטטיסטיקה, מדד שכר הדירה (120460)", "url": "https://api.cbs.gov.il/index/data/price?id=120460&format=json&lang=he"},
    "law": {"he": "חוק השכירות והשאילה, התשל״א־1971, סימן ו׳ (חוזה שכירות למגורים), נוסח עדכני ל־30.9.2026", "url": "https://www.nevo.co.il/law_html/law00/5149.htm"},
    "tax": {"he": "כל זכות: פטור ממס על הכנסה מהשכרת דירה למגורים, ומסלול 10% (עודכן 22.2.2026); רשות המסים: מדריך המסלולים", "url": "https://www.kolzchut.org.il/he/%D7%A4%D7%98%D7%95%D7%A8_%D7%9E%D7%9E%D7%A1_%D7%A2%D7%9C_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9E%D7%94%D7%A9%D7%9B%D7%A8%D7%AA_%D7%93%D7%99%D7%A8%D7%94_%D7%9C%D7%9E%D7%92%D7%95%D7%A8%D7%99%D7%9D",
            "url2": "https://www.gov.il/he/pages/detail-tracks-payment-tax-relief-rental-apartments"},
}
out = {"key": "rent", "built": "2026-10-26", "nat": nat, "cities": cities, "dist": dist, "idx": idx, "law": law, "tax": tax, "src": src}

# ---------------------------------------------------------------- checks
def city(n): return next(c for c in cities if c["n"] == n)
assert city("תל אביב-יפו")["r"]["3"]["v"] == 8250 and city("תל אביב-יפו")["r"]["3"]["q"] == "2026-06", city("תל אביב-יפו")["r"]["3"]
assert nat["r"]["4"]["v"] == 4825 and nat["r"]["4"]["q"] == "2026-06", nat["r"]["4"]
assert abs(nat["cbs"]["total"]["a"] - 5085.5) < 0.01, nat["cbs"]["total"]
assert all(c["r"] for c in cities)
assert idx["last"] == "2026-09" and idx["yoy"] == 3.2, idx["last"]
nbs = sum(len(c["nb"]) for c in cities)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print("wrote %s: %d cities, %d neighbourhoods, CBS cities %d + %d districts, index to %s; %d bytes" % (OUT, len(cities), nbs, cbs_city, len(dist), idx["last"], os.path.getsize(OUT)))
