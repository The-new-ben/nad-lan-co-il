# -*- coding: utf-8 -*-
"""G1 (/dira-behanacha/, Ben 26.10.2026 "win מחיר למשתכן + דירה בהנחה"): data for the two new tools "dirafit" (who is eligible,
which track, which three towns) and "diracost" (what the flat really costs against the town's deal prices).
NEW file, nothing live reads it until a release ships it: plugins/nadlan-config/assets/instruments/data/dira-round.json.

Sources, all official, every number carries its source and date in the JSON:
  1. data.gov.il "נתונים תקופתיים - תכנית דירה בהנחה", resource 7c8255d0 "מעקב אחר הגרלות דירה בהנחה" (the same file as dira.json):
     every lottery 2016 to January 2025 with registrations, winners, flats, local quota, local registrations and winners, price per
     m2, town, round (CentralizationType). The file was last modified 16.8.2026 but its newest lottery is January 2025: rounds 10
     (2025) and 11 (2026) are not in it. Rounds 1 to 9 of "דירה בהנחה" (March 2022 to December 2024) are grouped from it.
  2. Ministry of Construction and Housing press releases on gov.il (read in Chrome 26.10.2026, gov.il answers 403 to scripts):
     25.5.2026 (round 11 opens: towns, flats, lotteries, order), 23.6.2026 (households registered per town), 2.8.2026 (reserve:
     25,394 registered, 4,734 won). Typed here from the pages; the raw text is in _private-research/2026-10-26-upgrades/raw/g1/.
  3. The rules (eligibility, quotas, costs, mortgage, grant, sale lock) from gov.il tenaey_zkaut (updated 26.5.2026),
     request_for_eligibility_confirmation (24.9.2026), benefits_in_apartment_funding (24.2.2026), the participation guide.
  4. Town deal prices: plugins/.../data/invest.json (data.nadlan.gov.il medians by rooms and quarter, version 20.8.2026).
Nothing is estimated. Where the official sources are silent the field is absent and the tool says so.
  python tools/instruments/build_dira_round.py [--cache path/to/datastore.json]"""
import io, json, os, re, statistics, sys, time, urllib.request
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")
OUT = os.path.join(DATA, "dira-round.json")
RES = "7c8255d0-49ef-49db-8904-4cf917586031"
UA = {"User-Agent": "Mozilla/5.0 NadLan-instruments"}

# ------------------------------------------------------------------ 1. the official lottery file
if "--cache" in sys.argv:
    rec = json.load(io.open(sys.argv[sys.argv.index("--cache") + 1], encoding="utf-8"))["result"]["records"]; mod = "2026-08-16"
else:
    pk = json.load(urllib.request.urlopen(urllib.request.Request("https://data.gov.il/api/3/action/package_show?id=mechir-lamishtaken", headers=UA), timeout=120))["result"]
    mod = (next(r for r in pk["resources"] if r["id"] == RES).get("last_modified") or pk["metadata_modified"])[:10]
    rec = json.load(urllib.request.urlopen(urllib.request.Request("https://data.gov.il/api/3/action/datastore_search?resource_id=%s&limit=32000" % RES, headers=UA), timeout=300))["result"]["records"]


def num(x):
    try:
        return float(str(x).replace(",", ""))
    except (TypeError, ValueError):
        return None


def key(s):  # town names differ between the file and the press releases: "קרית גת" / "קריית גת", "קדימה-צורן" / "קדימה צורן"
    return re.sub(r"[^א-ת]", "", str(s or "").replace("קריית", "קרית").replace("עילית", "עלית"))


def med(a):
    return statistics.median(a) if a else None


# rounds of "דירה בהנחה" in the file (CentralizationType), numbered as the ministry numbers them (round 6 opened 26.12.2023,
# round 10 opened 10.8.2025, round 11 opened 25.5.2026)
ROUNDS = [("הגרלה גדולה מרץ 2022", 1, "מרץ 2022"), ("יולי 2022", 2, "יולי 2022"), ("הגרלת אוקטובר 2022", 3, "אוקטובר 2022"),
          ("הגרלת דצמבר 2022", 4, "דצמבר 2022"), ("הגרלה גדולה - אפריל 2023", 5, "אפריל 2023"), ("הגרלה גדולה - דצמבר 2023", 6, "דצמבר 2023"),
          ("הגרלה גדולה - מאי 2024", 7, "מאי 2024"), ("הגרלה גדולה - ספטמבר 2024", 8, "ספטמבר 2024"), ("הגרלה גדולה - דצמבר 2024", 9, "דצמבר 2024")]
RN = {c: (n, lab) for c, n, lab in ROUNDS}
rows = []
for r in rec:
    s, w, u = num(r["Subscribers"]), num(r["Winners"]), num(r["LotteryHousingUnits"])
    if not s or w is None:
        continue
    lw = num(r["WinnersBneyMakom"])
    rows.append({"town": re.sub(r"\s*-\s*", "-", (r["LamasName"] or "").strip()), "hood": (r["Neighborhood"] or "").strip().strip("-").strip(),
                 "date": (r["LotteryExecutionDate"] or "")[:10], "subs": int(s), "wins": int(w), "units": int(u or 0),
                 "lunits": int(num(r["LotteryNativeHousingUnits"]) or 0), "lsubs": int(num(r["SubscribersBenyMakom"]) or 0),
                 "lwins": int(lw) if lw is not None else -1, "pm": int(num(r["PriceForMeter"]) or 0), "round": RN.get(r["CentralizationType"], (0, ""))[0],
                 "first": r["LotteryType"] == "ראשונה", "track": r["MarketingMethodDesc"], "id": r["LotteryId"]})
last = max(x["date"] for x in rows if x["date"])
since22 = [x for x in rows if x["round"]]

rounds = []
for c, n, lab in ROUNDS:
    rr = [x for x in since22 if x["round"] == n]
    rounds.append({"n": n, "label": lab, "src": "file", "lotteries": len(rr), "towns": len({x["town"] for x in rr}), "units": sum(x["units"] for x in rr),
                   "regs": sum(x["subs"] for x in rr), "wins": sum(x["wins"] for x in rr), "odds": round(med([x["wins"] / x["subs"] for x in rr]), 5),
                   "pm": int(med([x["pm"] for x in rr if x["pm"]]) or 0), "from": min(x["date"] for x in rr), "to": max(x["date"] for x in rr)})

# ------------------------------------------------------------------ 2. round 10 and round 11 from the ministry's own releases
SP = {"open": {"label": "משרד הבינוי והשיכון, הודעת דוברות 25.5.2026", "url": "https://www.gov.il/he/pages/spokesman-25052026"},
      "regs": {"label": "משרד הבינוי והשיכון, הודעת דוברות 23.6.2026 (עודכנה 6.8.2026)", "url": "https://www.gov.il/he/pages/spokesman-23062026"},
      "wins": {"label": "משרד הבינוי והשיכון, הודעת דוברות 2.8.2026", "url": "https://www.gov.il/he/pages/spokesman-02082026"},
      "apr": {"label": "משרד הבינוי והשיכון, הודעת דוברות 12.4.2026", "url": "https://www.gov.il/he/pages/spokesman-12042026"}}
# order of the lotteries, town, lotteries, flats for the eligible, households registered to the town's lotteries (23.6.2026 table)
R11 = [(1, "ראשון לציון", 2, 148, 23425), (2, "אשדוד", 1, 256, 16299), (3, "בית שמש", 4, 425, 15012), (4, "רחובות", 1, 30, 7623),
       (5, "חדרה", 4, 268, 22711), (6, "כפר סבא", 11, 1045, 38732), (7, "קריית גת", 9, 1433, 28514), (8, "נהריה", 2, 218, 12522),
       (9, "אילת", 1, 99, 8875), (10, "מעלה אדומים", 16, 1663, 22658), (11, "יהוד", 1, 121, 7630), (12, "יקנעם עלית", 1, 89, 5717),
       (13, "קדימה צורן", 6, 315, 23241), (14, "כפר מנדא", 2, 131, 1652), (15, "מזכרת בתיה", 4, 427, 19721), (16, "רכסים", 5, 405, 12404),
       (17, "בית דגן", 5, 399, 26402), (18, "בני עי\"ש", 4, 179, 10145), (19, "בת חפר", 3, 271, 10132)]
assert sum(x[3] for x in R11) == 7922 and sum(x[2] for x in R11) == 82, "the 23.6.2026 table totals"
# the town column sums to 313,415 while the table's total line says 114,840 households (the text: 114,848): a household registers
# in up to three towns, so the same household appears in up to three town rows. 313,415 / 114,848 = 2.73 towns per household.
assert sum(x[4] for x in R11) == 313415
R11_TOT = {"households": 114848, "households_table": 114840, "town_regs": 313415, "regs": 1700000, "units": 7922, "towns": 19, "lotteries": 82, "opened": "2026-05-25", "closed": "2026-06-22",
           "elig_until": "2026-06-07", "drawn": "2026-07-26", "notices": "2026-08-02", "res_regs": 25394, "res_wins": 4734, "res_share_units": 0.5,
           "res_combat_share": "כמחצית מדירות המילואים", "res_winner_share": "כ־60% מכלל הזוכים"}
rounds.append({"n": 10, "label": "אוגוסט 2025", "src": "news", "units": 7479, "towns": 21, "from": "2025-08-10", "to": "2025-11-23",
               "note": "7,479 דירות ב־21 יישובים; ההרשמה נפתחה 10.8.2025, הודעות הזכייה 23.11.2025. הקובץ הפתוח עוד לא כולל את הסבב הזה, והמספרים מההודעות שצוטטו בעיתונות",
               "srcs": [{"label": "רשויות, הודעת משרד הבינוי והשיכון 6.8.2025", "url": "https://www.rashuiot.co.il/html5/arcLookup.taf?_function=details&_ID=73334&did=1118&G=&SM="},
                        {"label": "mako, 23.11.2025", "url": "https://www.mako.co.il/finances-real-estate/Article-74be72cad30ba91027.htm"}]})
rounds.append({"n": 11, "label": "מאי 2026", "src": "gov", "lotteries": 82, "towns": 19, "units": 7922, "households": 114848, "wins_res": 4734,
               "from": "2026-05-25", "to": "2026-08-02", "odds_hh": round(7922 / 114848, 5)})

# ------------------------------------------------------------------ 3. per town of round 11: the official round numbers + the town's history in the file + deal prices
inv = json.load(io.open(os.path.join(DATA, "invest.json"), encoding="utf-8"))
INV = {key(r["n"]): r for r in inv["rows"] if not r.get("nat")}
by_town = {}
for x in rows:
    by_town.setdefault(key(x["town"]), []).append(x)
towns = []
for order, name, lots, units, hh in R11:
    h = by_town.get(key(name), [])
    h22 = [x for x in h if x["round"]]
    lo = [x["lwins"] / x["lsubs"] for x in h if x["lsubs"] > 0 and x["lwins"] >= 0]
    lastp = sorted([x for x in h if x["pm"]], key=lambda x: x["date"])[-1] if any(x["pm"] for x in h) else None
    t = {"order": order, "n": name, "lots": lots, "units": units, "hh": hh, "per100": round(100 * units / hh, 2),
         "hist": {"n": len(h), "n22": len(h22), "odds": round(med([x["wins"] / x["subs"] for x in h]), 5) if h else None,
                  "odds22": round(med([x["wins"] / x["subs"] for x in h22]), 5) if h22 else None,
                  "lodds": round(med(lo), 5) if lo else None, "ln": len(lo), "first": min(x["date"] for x in h) if h else None, "last": max(x["date"] for x in h) if h else None},
         "pm": {"v": lastp["pm"], "date": lastp["date"], "hood": lastp["hood"]} if lastp else None}
    m = INV.get(key(name))
    if m:
        t["mkt"] = {k: {"price": m["r"][k]["price"], "q": m["r"][k]["q"]} for k in ("3", "4", "5") if k in m["r"]}
        if m.get("pp"): t["page"] = m["pp"]
    towns.append(t)

# ------------------------------------------------------------------ 4. every lottery since March 2022 (rounds 1 to 9), for the tables
lots22 = sorted(since22, key=lambda x: (x["round"], x["town"], x["date"]))
L22 = [[x["round"], x["town"], x["hood"], x["date"], x["units"], x["lunits"], x["subs"], x["wins"], x["lsubs"], x["lwins"], x["pm"], 1 if x["first"] else 0] for x in lots22]

# ------------------------------------------------------------------ 5. the rules, each with its official page and date
ZK = {"label": "משרד הבינוי והשיכון, מי זכאי בתוכניות דירה בהנחה (עודכן 26.5.2026)", "url": "https://www.gov.il/he/pages/tenaey_zkaut"}
EL = {"label": "בקשת אישור זכאות, gov.il (עודכן 24.9.2026)", "url": "https://www.gov.il/he/service/request_for_eligibility_confirmation"}
RG = {"label": "הרשמה להגרלה, gov.il (עודכן 24.9.2026)", "url": "https://www.gov.il/he/service/register_for_discounted_housing_lottery"}
FN = {"label": "הטבות והקלות במימון הדירה, gov.il (עודכן 24.2.2026)", "url": "https://www.gov.il/he/departments/general/benefits_in_apartment_funding"}
GD = {"label": "המדריך להשתתפות בתוכניות דירה בהנחה, gov.il", "url": "https://www.gov.il/he/pages/mechir_lamishtaken_guide"}
rules = {
    "status": [{"t": "הנפקה וחידוש של אישורי זכאות נעצרו זמנית להתאמת המערכות לתנאי בג״ץ על חייבי גיוס, ולפי ההודעה נפתחו מחדש ב־5.10.2026", "src": RG},
               {"t": "על ההגרלה הבאה (ה־12) אין הודעה רשמית: אין מועד, אין רשימת יישובים ואין מספר דירות", "src": {"label": "עמוד הנושא דירה בהנחה, gov.il, נבדק 26.10.2026", "url": "https://www.gov.il/he/departments/topics/dira"}}],
    "family": [  # who may hold a certificate (tenaey_zkaut)
        {"k": "couple", "label": "זוג נשוי או ידועים בציבור", "ok": True},
        {"k": "engaged", "label": "זוג שמתחתן בתוך 3 חודשים", "ok": True, "note": "הזכאות מותנית בחתונה בתוך 3 חודשים מהגשת הבקשה; בלי חתונה הזכאות והזכייה מתבטלות"},
        {"k": "single35", "label": "יחיד או יחידה מגיל 35", "ok": True},
        {"k": "parent", "label": "הורה עם ילד רווק מתחת לגיל 21", "ok": True},
        {"k": "divorced", "label": "הורה גרוש מתחת לגיל 35 שהילדים לא בחזקתו", "ok": True},
        {"k": "foreign", "label": "אזרח ישראלי הנשוי לאזרח חוץ", "ok": True, "note": "תצהיר תושב זר הנשוי לאזרח ישראלי, חתום בפני עורך דין"},
        {"k": "disabled", "label": "יחיד מגיל 21 עם נכות מוכרת", "ok": True, "note": "75% נכות רפואית לצמיתות, או מעל 50% עם קצבת ניידות ושירותים מיוחדים, או נפגע פעולות איבה או נכה משרד הביטחון 50% ומעלה"},
        {"k": "widow", "label": "אלמן או אלמנה מגיל 21", "ok": True},
        {"k": "single", "label": "יחיד מתחת לגיל 35 בלי ילדים", "ok": False, "note": "לא מופיע ברשימת הזכאים של משרד הבינוי והשיכון"}],
    "home": [
        {"k": "none", "label": "לא הייתה לי דירה, או עד שליש דירה, ב־3 השנים האחרונות", "status": "חסר דירה", "first": True, "cont": True},
        {"k": "one", "label": "הייתה לי דירה יחידה (יותר משליש) ב־3 השנים האחרונות", "status": "משפר דיור", "first": False, "cont": True,
         "note": "משפרי דיור נרשמים רק להגרלות המשך שהוגדרו להם, וחייבים למכור את הדירה הקיימת בתוך 12 חודשים מהאכלוס. מ־1.1.2025 הזכאות שלהם לא מתחדשת לבד"},
        {"k": "two", "label": "החזקתי שתי דירות במקביל שנה ומעלה ב־3 השנים האחרונות", "status": "לא זכאי", "first": False, "cont": False},
        {"k": "past", "label": "כבר קניתי או זכיתי בעבר בתוכנית של מחיר מפוקח", "status": "לא זכאי", "first": False, "cont": False},
        {"k": "kibbutz", "label": "אני חבר קיבוץ", "status": "לא זכאי", "first": False, "cont": False}],
    "service": "היחיד או כל אחד מבני הזוג לא מוגדרים לפי נתוני צה״ל כחייבי גיוס שלא הסדירו את מעמדם (בג״ץ; נבדק אחרי סגירת ההרשמה)",
    "towns_max": 3,
    "local": {"def": "גר בתחום הרשות 3 השנים האחרונות, או 4 מתוך 10 השנים האחרונות, לפי רשות האוכלוסין, כל בן זוג בנפרד, בלי ערעור", "quota": 0.2},
    "reserve": {"def": "60 ימי מילואים לפחות בצו 8 מ־7.10.2023; לוחם = משתייך למערך הלוחם לפי צה״ל", "cert_after": "2025-08-05",
                "target_periph": 0.5, "target_periph_combat": 0.25, "target_other": 0.35, "target_other_combat": 0.15, "r11": 0.5,
                "check": "מוקד המילואים 1111 שלוחה 4"},
    "wheelchair": {"per": 30, "min": 1},
    "cap73": 0.73,
    "cert": {"cost": 200, "renew": 50, "days": 10, "valid": "שנה", "companies": [["מילגם", "*6078"], ["אלונים", "*2850"], ["מעוף", "*9344"]]},
    "ltv": 0.75, "appraisal": {"equity_min": 100000, "value_cap": 2100000},
    "grant": {"mishtaken": [40000, 60000], "matara": 40000, "mufchat": 40000, "note": "ביישובים מזכים בלבד; ניתן אחרי תשלום ההון העצמי, כהלוואה שלא מחזירים אם מחזיקים בדירה עד סוף תקופת ההתחייבות"},
    "state_loan": {"t": "משכנתא לזכאים חסרי דירה (בלי דירה 10 שנים): ריבית נמוכה ב־0.5% מהריבית הממוצעת על משכנתאות צמודות שבנק ישראל מפרסם, ולא יותר מ־3.0%, לתקופה של 10 עד 30 שנה", "src": FN},
    "lock": {"t": "אסור למכור 5 שנים מטופס 4 או 7 שנים מיום ההגרלה, המוקדם מביניהם", "src": GD},
    "after": [["אישור זכאות", "עד 10 ימי עבודה"], ["הרשמה באתר ההגרלות", "עד 3 יישובים, לכל ההגרלות בהם; מועד ההרשמה לא משנה"], ["ההגרלה", "הגרלה על התור לבחירת דירה, במחשב ובפיקוח רואה חשבון"],
              ["היתר בנייה", "הזוכים מחכים להיתר; לפי המדריך זה צפוי להימשך זמן רב"], ["בחירת דירה", "לפי סדר הזכייה, 45 דקות לכל זוכה"], ["חוזה", "בתוך 30 ימי עבודה מהבחירה"]],
    "srcs": {"zk": ZK, "el": EL, "rg": RG, "fn": FN, "gd": GD},
}

data = {"key": "diraround", "built": time.strftime("%Y-%m-%d"),
        "file": {"source": "data.gov.il, נתונים תקופתיים - תכנית דירה בהנחה, מעקב אחר הגרלות דירה בהנחה", "url": "https://data.gov.il/dataset/mechir-lamishtaken",
                 "modified": mod, "first": min(x["date"] for x in rows if x["date"]), "last": last, "n": len(rows), "n22": len(since22)},
        "sp": SP, "r11": R11_TOT, "rounds": sorted(rounds, key=lambda r: r["n"]), "towns": towns, "rules": rules,
        "lots22": {"cols": ["round", "town", "hood", "date", "units", "lunits", "subs", "wins", "lsubs", "lwins", "pm", "first"], "rows": L22},
        "inv": {"source": "אתר הנדל״ן הממשלתי, עסקאות לפי רשות המסים, חציון לפי מספר חדרים ורבעון", "url": "https://www.nadlan.gov.il/", "version": "20.8.2026"}}
json.dump(data, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

# ------------------------------------------------------------------ the figures the page will quote, printed for the cross-check
res_odds = R11_TOT["res_wins"] / R11_TOT["res_regs"]
oth_odds = (R11_TOT["units"] - R11_TOT["res_wins"]) / (R11_TOT["households"] - R11_TOT["res_regs"])
print("dira-round.json: %d lotteries in the file (%d since 3.2022), last %s, file modified %s, size %d" % (len(rows), len(since22), last, mod, os.path.getsize(OUT)))
print("round 11: %.2f flats per 100 households; reserve %.1f%%, others (our calc, all 7,922 flats won) %.2f%%, ratio %.1f" % (100 * 7922 / 114848, 100 * res_odds, 100 * oth_odds, res_odds / oth_odds))
for r in data["rounds"]:
    print("round %2d %-14s lots %4s towns %3s units %6s regs %8s wins %6s odds %s pm %s" % (r["n"], r["label"], r.get("lotteries", ""), r.get("towns", ""), r.get("units", ""), r.get("regs", ""), r.get("wins", ""), r.get("odds", ""), r.get("pm", "")))
for t in sorted(towns, key=lambda t: -t["per100"]):
    print("%-12s per100 %5.2f | hist n %3d odds %s local %s (%d) | pm %s | 4r %s" % (t["n"], t["per100"], t["hist"]["n"], t["hist"]["odds"], t["hist"]["lodds"], t["hist"]["ln"], t["pm"], (t.get("mkt") or {}).get("4")))
