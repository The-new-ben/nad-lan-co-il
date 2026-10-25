# -*- coding: utf-8 -*-
"""U1 Mortgage 2.0 (Ben 25.10.2026): the official numbers behind the mortgage calculator, one file with a date and a source on
every value. Sources (all public, no key):
  - Bank of Israel SDMX, dataflow BIR_MRTG_99 (new housing loans, total banking system): average rates by track (fixed not
    linked _467, fixed CPI-linked _1492, variable CPI-linked benchmark _1489 + margin _1488), the volume (_897), the number of
    loans (_63), volume by track (_70 _71 _69 _68 _66), by payment-to-income bucket (_161 _160 _815 _806 _159 _158 _157 _156),
    by loan-to-value bucket (_887 _878 _869 _860 _851 _842), the average payment-to-income (_155), average terms (_461 _1491
    _1487) and investment-home loans (_62 _776).
  - Bank of Israel SDMX, series BR/MNT_RIB_BOI_D (the policy rate, daily) -> rate, the date it took effect, the 2026 path.
  - Bank of Israel average mortgage rate by term (the rates used for early-repayment fees): mashfix.xls (not linked) and
    pribmash.xls (CPI-linked), effective annual, converted here to nominal (monthly payments): 12 x ((1 + e)^(1/12) - 1).
    Reading them needs xlrd (run with a venv that has it: python -m venv v && v/Scripts/pip install xlrd==2.0.1).
  - CBS consumer price index, series 120010 (public API): the 12-month change and the average monthly change of the last 12
    indices (the Banking Order's CPI fee on a linked loan repaid between the 1st and the 15th of a month).
  - Rules (directive 329 v12/v13, directive 451, the Banking Order 2002) and the October 2026 Bank of Israel forecast and the
    next decision date are not machine readable; they are carried from the U1 research (dna.md section 6, 25.10.2026).
If a source cannot be read, the value stays the last verified one from dna.md section 6, marked "from research 25.10.2026".
python build_boi_mortgage_data.py -> plugins/nadlan-config/assets/instruments/data/boi-mortgage.json"""
import csv
import datetime
import io
import json
import os
import sys
import tempfile
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "instruments", "data")
OUT = os.path.join(DATA, "boi-mortgage.json")
UA = {"User-Agent": "Mozilla/5.0 NadLan-instruments"}
RESEARCH = "from research 25.10.2026"
RESEARCH_HE = "הערך האחרון שאומת במחקר, 25.10.2026"  # what a visitor reads in a source label when a source was not reachable
SDMX = "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS"
U_BIR = SDMX + "/BIR_MRTG_99/1.0/?c%5BTIME_PERIOD%5D=ge:{start}&format=csv"
U_RATE = SDMX + "/BR/1.0/MNT_RIB_BOI_D?c%5BTIME_PERIOD%5D=ge:2025-11-01&format=csv"
U_MASHFIX = "https://www.boi.org.il/boi_files/Pikuah/mashfix.xls"
U_PRIBMASH = "https://www.boi.org.il/boi_files/Pikuah/pribmash.xls"
U_CBS = "https://api.cbs.gov.il/index/data/price?id=120010&format=json&download=false&lang=he&startPeriod={start}&PageSize=100"
BOI_HOME = "https://www.boi.org.il/"
CBS_HOME = "https://www.cbs.gov.il/"
LOG = []


def log(msg):
    LOG.append(msg)
    print(msg)


def get(url, binary=False, tries=3):
    last = None
    for i in range(tries):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
            return raw if binary else raw.decode("utf-8-sig")
        except Exception as e:  # network, bot wall, timeout
            last = e
            time.sleep(2 + 3 * i)
    raise last


def nominal(eff):
    """effective annual % -> nominal annual % for a loan repaid monthly (the BoI conversion sheet in pribmash.xls)"""
    return round(1200 * ((1 + eff / 100) ** (1 / 12) - 1), 2)


def xl_date(v):
    if isinstance(v, (int, float)) and v > 20000:
        return (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(v))).isoformat()
    s = str(v).strip()
    for fmt in ("%d/%m/%Y", "%d.%m.%Y"):
        try:
            return datetime.datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    return None


# ------------------------------------------------------------------ the last verified values (dna.md section 6, 25.10.2026)
FB = {
    "month": "2026-08",
    "rates": {"fixed_nl": [["2026-06", 4.73], ["2026-07", 4.63], ["2026-08", 4.62]],
              "fixed_cpi": [["2026-06", 3.27], ["2026-07", 3.22], ["2026-08", 3.29]],
              "var_cpi_bench": [["2026-08", 1.64]], "var_cpi_margin": [["2026-08", 1.55]]},
    "loans": 10272, "volume": 10899046.61, "pti_avg": 29.23, "term_nl": 23.81, "term_cpi_fixed": 17.33, "term_cpi_var": 28.97,
    "tracks": {"var_nl": 54.3, "fixed_nl": 35.8, "fixed_cpi": 6.6, "var_cpi": 3.2, "fx": 0.1},
    "ltv": [8.4, 14.8, 27.9, 48.8, 0.04, 0.0], "pti": [2.6, 12.5, 31.8, 52.6, 0.4, 0.0],
    "invest_loans": 694, "invest_volume": 888769.15,
    "policy": {"rate": 3.25, "from": "2026-09-03", "asof": "2026-10-25"},
    "path": [["2026-01-08", 4.0], ["2026-05-28", 3.75], ["2026-07-09", 3.5], ["2026-09-03", 3.25]],
    "nl_term": {"inforce": "2026-10-19", "month": "2026-09-30", "avg": 4.55, "b": [4.35, 4.51, 4.59, 4.61, 4.74, 4.79, 4.89]},
    "cpi_term": {"inforce": "2026-10-19", "month": "2026-09-30", "avg": 3.49, "b": [3.50, 3.49, 3.24, 3.46, 3.37, 3.53]},
    "cpi": {"latest": "2026-09", "y12": 1.6},
}
NL_BUCKETS = [(0, 1, "עד שנה, כולל ריבית שמשתנה במועד לא ידוע (פריים)"), (1, 5, "מעל שנה ועד 5 שנים"), (5, 10, "מעל 5 ועד 10 שנים"),
              (10, 15, "מעל 10 ועד 15 שנים"), (15, 20, "מעל 15 ועד 20 שנים"), (20, 25, "מעל 20 ועד 25 שנים"), (25, 99, "מעל 25 שנים")]
CPI_BUCKETS = [(0, 5, "עד 5 שנים"), (5, 10, "מעל 5 ועד 10 שנים"), (10, 15, "מעל 10 ועד 15 שנים"), (15, 20, "מעל 15 ועד 20 שנים"),
               (20, 25, "מעל 20 ועד 25 שנים"), (25, 99, "מעל 25 שנים")]


# ------------------------------------------------------------------ 1. BIR_MRTG_99
def read_bir():
    start = (datetime.date.today().replace(day=1) - datetime.timedelta(days=430)).strftime("%Y-%m")
    url = U_BIR.format(start=start)
    raw = get(url)
    rows = list(csv.DictReader(io.StringIO(raw)))
    ser = {}
    for r in rows:
        code = r.get("SERIES_CODE", "")
        if not code.startswith("BNK_99034_LR_BIR_MRTG_") or not r.get("OBS_VALUE"):
            continue
        n = code.rsplit("_", 1)[1]
        try:
            ser.setdefault(n, {})[r["TIME_PERIOD"]] = float(r["OBS_VALUE"])
        except ValueError:
            pass
    if "467" not in ser or "63" not in ser:
        raise RuntimeError("BIR_MRTG_99: the rate or the loan count series is missing")
    return ser, url


def build_market(ser, url):
    m = max(k for k in ser["467"] if k in ser.get("63", {}))  # the newest month with both the rates and the loan count
    months = sorted(k for k in ser["467"] if k <= m)[-3:]
    v = lambda n, mm=m: ser.get(n, {}).get(mm)
    src = {"label": "בנק ישראל, הלוואות חדשות לדיור (SDMX BIR_MRTG_99)", "url": url}
    rates = {
        "fixed_nl": {"label": "קבועה לא צמודה (קל״צ)", "series": "_467", "hist": [[k, ser["467"][k]] for k in months], "rate": v("467")},
        "fixed_cpi": {"label": "קבועה צמודה למדד (ק״צ)", "series": "_1492", "hist": [[k, ser["1492"][k]] for k in months if k in ser.get("1492", {})], "rate": v("1492")},
        "var_cpi": {"label": "משתנה צמודה למדד: עוגן ועוד מרווח", "series": "_1489 + _1488", "bench": v("1489"), "margin": v("1488"),
                    "rate": round(v("1489") + v("1488"), 2) if v("1489") is not None and v("1488") is not None else None,
                    "hist": [[k, round(ser["1489"][k] + ser["1488"][k], 2)] for k in months if k in ser.get("1489", {}) and k in ser.get("1488", {})]},
    }
    tr = {"var_nl": v("70"), "fixed_nl": v("71"), "fixed_cpi": v("69"), "var_cpi": v("68"), "fx": v("66")}
    tsum = sum(x for x in tr.values() if x)
    names = {"var_nl": "משתנה לא צמודה, כולל פריים", "fixed_nl": "קבועה לא צמודה", "fixed_cpi": "קבועה צמודה", "var_cpi": "משתנה צמודה", "fx": "מטבע חוץ"}
    tracks = [{"k": k, "label": names[k], "share": round(100 * tr[k] / tsum, 1)} for k in ("var_nl", "fixed_nl", "fixed_cpi", "var_cpi", "fx") if tr[k] is not None]
    ltv_codes = [("887", 0, 30), ("878", 30, 45), ("869", 45, 60), ("860", 60, 75), ("851", 75, 90), ("842", 90, None)]
    lsum = sum(v(c) or 0 for c, _, _ in ltv_codes)
    ltv = [{"from": a, "to": b, "share": round(100 * (v(c) or 0) / lsum, 2)} for c, a, b in ltv_codes]
    pti_codes = [("161", 0, 10), ("160", 10, 20), ("815", 20, 30), ("806", 30, 40), ("159", 40, 50), ("158", 50, 60), ("157", 60, 80), ("156", 80, None)]
    psum = sum(v(c) or 0 for c, _, _ in pti_codes)
    pti = [{"from": a, "to": b, "share": round(100 * (v(c) or 0) / psum, 2)} for c, a, b in pti_codes]
    vol = v("897")  # ILS thousands
    nxt = sorted(k for k in ser.get("897", {}) if k > m)
    market = {"month": m, "loans": int(v("63")), "volume_k": vol, "avg_loan": round(1000 * vol / v("63")), "pti_avg": v("155"),
              "term_nl": v("461"), "term_cpi_fixed": v("1491"), "term_cpi_var": v("1487"), "tracks": tracks, "ltv": ltv, "pti": pti,
              "invest": {"loans": int(v("62")) if v("62") else None, "volume_k": v("776")},
              "next_volume": {"month": nxt[-1], "volume_k": ser["897"][nxt[-1]], "note": "פרסום ראשון"} if nxt else None,
              "src": src, "from": "SDMX"}
    log(f"BIR_MRTG_99 {m}: fixed_nl {rates['fixed_nl']['rate']} fixed_cpi {rates['fixed_cpi']['rate']} var_cpi {rates['var_cpi']['rate']} | loans {market['loans']} avg {market['avg_loan']} | pti avg {market['pti_avg']}")
    return rates, market


def fallback_market():
    src = {"label": "בנק ישראל, הלוואות חדשות לדיור (SDMX BIR_MRTG_99), " + RESEARCH_HE, "url": U_BIR.format(start="2025-01")}
    r = FB["rates"]
    rates = {"fixed_nl": {"label": "קבועה לא צמודה (קל״צ)", "series": "_467", "hist": r["fixed_nl"], "rate": r["fixed_nl"][-1][1], "from": RESEARCH},
             "fixed_cpi": {"label": "קבועה צמודה למדד (ק״צ)", "series": "_1492", "hist": r["fixed_cpi"], "rate": r["fixed_cpi"][-1][1], "from": RESEARCH},
             "var_cpi": {"label": "משתנה צמודה למדד: עוגן ועוד מרווח", "series": "_1489 + _1488", "bench": 1.64, "margin": 1.55, "rate": 3.19, "hist": [["2026-08", 3.19]], "from": RESEARCH}}
    names = {"var_nl": "משתנה לא צמודה, כולל פריים", "fixed_nl": "קבועה לא צמודה", "fixed_cpi": "קבועה צמודה", "var_cpi": "משתנה צמודה", "fx": "מטבע חוץ"}
    edges = [(0, 30), (30, 45), (45, 60), (60, 75), (75, 90), (90, None)]
    pedges = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, None)]
    market = {"month": FB["month"], "loans": FB["loans"], "volume_k": FB["volume"], "avg_loan": round(1000 * FB["volume"] / FB["loans"]), "pti_avg": FB["pti_avg"],
              "term_nl": FB["term_nl"], "term_cpi_fixed": FB["term_cpi_fixed"], "term_cpi_var": FB["term_cpi_var"],
              "tracks": [{"k": k, "label": names[k], "share": s} for k, s in FB["tracks"].items()],
              "ltv": [{"from": a, "to": b, "share": s} for (a, b), s in zip(edges, FB["ltv"])],
              "pti": [{"from": a, "to": b, "share": s} for (a, b), s in zip(pedges, FB["pti"])],
              "invest": {"loans": FB["invest_loans"], "volume_k": FB["invest_volume"]}, "next_volume": None, "src": src, "from": RESEARCH}
    return rates, market


# ------------------------------------------------------------------ 2. the policy rate
def read_policy():
    raw = get(U_RATE)
    rows = list(csv.reader(io.StringIO(raw)))
    head = rows[0]
    ti, vi = head.index("TIME_PERIOD"), head.index("OBS_VALUE")
    s = sorted((r[ti], float(r[vi])) for r in rows[1:] if len(r) > vi and r[vi])
    path, last = [], None
    for d, val in s:
        if val != last:
            path.append([d, val])
            last = val
    path = [p for p in path if p[0] >= "2026-01-01"] or path[-1:]
    cur = s[-1][1]
    since = [p for p in path if p[1] == cur][-1][0]
    log(f"policy rate {cur} since {since}, as of {s[-1][0]}")
    return {"rate": cur, "prime": round(cur + 1.5, 2), "from": since, "asof": s[-1][0], "path2026": path,
            "src": {"label": "בנק ישראל, ריבית בנק ישראל (סדרה MNT_RIB_BOI_D)", "url": U_RATE}}


# ------------------------------------------------------------------ 3. the average rate by term (xls)
def read_xls():
    import xlrd  # noqa: needs the venv
    tmp = tempfile.mkdtemp(prefix="boi-xls-")
    out = {}
    for key, url in (("nl", U_MASHFIX), ("cpi", U_PRIBMASH)):
        p = os.path.join(tmp, key + ".xls")
        open(p, "wb").write(get(url, binary=True))
        b = xlrd.open_workbook(p)
        if key == "nl":
            sh = b.sheet_by_index(0)  # "הלוואות שניתנו מ-01.03.2013"; columns: avg, >25, 20-25, 15-20, 10-15, 5-10, 1-5, <=1, in force from, month
            order, nb = [7, 6, 5, 4, 3, 2, 1], NL_BUCKETS
        else:
            sh = b.sheet_by_name("RESULT")  # columns: avg, >25, 20-25, 15-20, 10-15, 5-10, <=5, in force from, month
            order, nb = [6, 5, 4, 3, 2, 1], CPI_BUCKETS
        n_in, n_m = len(order) + 1, len(order) + 2
        data_rows = []
        for i in range(sh.nrows):
            c = sh.row_values(i)
            if len(c) > n_m and isinstance(c[0], float) and xl_date(c[n_in]):
                data_rows.append(c)
        if not data_rows:
            raise RuntimeError(key + ": no data rows")
        top = max(data_rows, key=lambda c: xl_date(c[n_in]))
        buckets = [{"from": a, "to": (None if b2 == 99 else b2), "label": lab, "eff": round(top[col], 2), "nom": nominal(top[col])}
                   for (a, b2, lab), col in zip(nb, order)]
        hist = sorted({(xl_date(c[n_m]) or xl_date(c[n_in]))[:7]: round(c[0], 2) for c in data_rows}.items())
        out[key] = {"inforce": xl_date(top[n_in]), "month": xl_date(top[n_m]), "avg_eff": round(top[0], 2), "avg_nom": nominal(top[0]),
                    "buckets": buckets, "hist": [[k, v] for k, v in hist],
                    "src": {"label": "בנק ישראל, הריבית הממוצעת על משכנתאות " + ("במגזר השקלי הלא צמוד" if key == "nl" else "צמודות למדד") + " לפי תקופה לפירעון (" + os.path.basename(url) + ")", "url": url}}
        log(f"{os.path.basename(url)}: in force {out[key]['inforce']}, month {out[key]['month']}, avg {out[key]['avg_eff']} eff, buckets {[x['eff'] for x in buckets]}")
    return out


def fallback_xls():
    out = {}
    for key, nb, url in (("nl", NL_BUCKETS, U_MASHFIX), ("cpi", CPI_BUCKETS, U_PRIBMASH)):
        f = FB["nl_term" if key == "nl" else "cpi_term"]
        out[key] = {"inforce": f["inforce"], "month": f["month"], "avg_eff": f["avg"], "avg_nom": nominal(f["avg"]),
                    "buckets": [{"from": a, "to": (None if b == 99 else b), "label": lab, "eff": e, "nom": nominal(e)} for (a, b, lab), e in zip(nb, f["b"])],
                    "hist": [], "from": RESEARCH,
                    "src": {"label": "בנק ישראל, " + os.path.basename(url) + ", " + RESEARCH_HE, "url": url}}
    return out


# ------------------------------------------------------------------ 4. CPI
def read_cpi():
    start = (datetime.date.today().replace(day=1) - datetime.timedelta(days=500)).strftime("%m-%Y")
    d = json.loads(get(U_CBS.format(start=start)))
    rows = sorted(d["month"][0]["date"], key=lambda r: (r["year"], r["month"]))
    base = rows[-1]["currBase"]["baseDesc"]
    rows = [r for r in rows if r["currBase"]["baseDesc"] == base]
    vals = [(f"{r['year']}-{r['month']:02d}", r["currBase"]["value"]) for r in rows]
    if len(vals) < 13:
        raise RuntimeError("CPI: fewer than 13 months in one base")
    return vals, base, U_CBS.format(start=start)


def cpi_block():
    try:
        vals, base, url = read_cpi()
        src = {"label": "הלשכה המרכזית לסטטיסטיקה, מדד המחירים לצרכן (סדרה 120010), בסיס " + base, "url": url}
        frm = "CBS API"
    except Exception as e:
        log(f"CPI API failed ({e}); using the chained local file cbs-120010.json")
        try:
            m = json.load(open(os.path.join(DATA, "cbs-120010.json"), encoding="utf-8"))["months"]
            vals = sorted(m.items())
            src = {"label": "הלשכה המרכזית לסטטיסטיקה, מדד המחירים לצרכן (סדרה 120010)", "url": CBS_HOME}
            frm = "cbs-120010.json"
        except Exception:
            return {"latest": FB["cpi"]["latest"], "y12": FB["cpi"]["y12"], "avg_m12": None, "from": RESEARCH,
                    "src": {"label": "הלשכה המרכזית לסטטיסטיקה, סדרה 120010, " + RESEARCH_HE, "url": CBS_HOME}}
    last13 = vals[-13:]
    ch = [last13[i][1] / last13[i - 1][1] - 1 for i in range(1, 13)]
    y12 = round(100 * (last13[-1][1] / last13[0][1] - 1), 2)
    avg = round(100 * sum(ch) / 12, 4)
    log(f"CPI {last13[-1][0]}: 12 months {y12}%, average monthly change {avg}% ({frm})")
    return {"latest": last13[-1][0], "y12": y12, "avg_m12": avg, "from": frm, "src": src}


# ------------------------------------------------------------------ 5. the rules, the forecast and the fees (research, dated)
def fixed_blocks():
    d329 = {"label": "הוראת ניהול בנקאי תקין 329, מגבלות למתן הלוואות לדיור (גרסה 12, 8.2.2026; גרסה 13, 30.6.2026)", "url": BOI_HOME}
    rules = {
        "ltv": {"single": 0.75, "replace": 0.70, "invest": 0.50, "reduced": 0.75},
        "reduced": {"value_cap": 2100000, "own_min": 100000, "own_min_grant": 60000,
                    "text": "בדירה במחיר מופחת השווי יכול להתבסס על הערכת שמאי; אם ההערכה עולה על 2.1 מיליון ₪, השווי הוא 2.1 מיליון ₪ או מחיר הרכישה, הגבוה מביניהם. הקונה משלם מכספו לפחות 100,000 ₪ (60,000 ₪ בדירה שניתן עליה מענק מחיר למשתכן החדשה)."},
        "pti_max": 0.50, "pti_risk": 0.40, "variable_max": 0.6666, "term_max": 30,
        "any_purpose": {"ltv": 0.50, "ltv_upto": 0.70, "above_cap": 200000},
        "src": d329, "asof": "2026-06-30", "from": RESEARCH,
        "notes": {"ltv": "סעיף 2", "reduced": "סעיף 4א", "pti": "סעיפים 5 ו־6, נספח א", "variable": "סעיף 7", "term": "סעיף 8"},
    }
    baskets = {"src": {"label": "הוראת ניהול בנקאי תקין 451, חוזר 2694 (31.1.2022, בתוקף מ־31.8.2022), נספח 5: שלושה סלים אחידים בכל אישור עקרוני", "url": BOI_HOME},
               "terms": [10, 15, 20, 25, 30], "method": "spitzer",
               "list": [{"k": "b1", "label": "סל אחיד 1", "mix": [["fixed_nl", 1.0]]},
                        {"k": "b2", "label": "סל אחיד 2", "mix": [["fixed_nl", 1 / 3], ["prime", 1 / 3], ["var5_cpi", 1 / 3]]},
                        {"k": "b3", "label": "סל אחיד 3", "mix": [["fixed_nl", 0.5], ["prime", 0.5]]}],
               "from": RESEARCH}
    forecast = {"published": "2026-10-21", "rate_q3_2027": 3.0, "inflation_4q": 2.0, "inflation_2026": 1.5, "inflation_2027": 2.1,
                "market_rate": 3.1, "market_inflation": 1.8, "private_rate": 3.1, "private_rate_range": [2.8, 3.5], "private_inflation": 2.1,
                "next_decision": "2026-11-23",
                "src": {"label": "בנק ישראל, חטיבת המחקר, תחזית אוקטובר 2026 (הודעה לעיתונות 21.10.2026); מועד ההחלטה הבאה מעמוד ההודעות של בנק ישראל", "url": BOI_HOME},
                "from": RESEARCH}
    fees = {"operational_max": 60, "notice_rate": 0.001, "notice_days": 10, "notice_max_days": 45,
            "reduce": [{"after_years": 3, "cut": 0.20}, {"after_years": 5, "cut": 0.30}],
            "reduce_complementary": [{"after_years": 1, "cut": 0.10}, {"after_years": 2, "cut": 0.20}, {"after_years": 3, "cut": 0.30}, {"after_years": 4, "cut": 0.40}],
            "no_cap_fee_if_change_within_months": 12, "cpi_fee": "מחצית השינוי הממוצע במדד ב־12 המדדים האחרונים, בפירעון בין ה־1 ל־15 בחודש",
            "directed_no_fee": True,
            "src": {"label": "צו הבנקאות (פירעון מוקדם של הלוואה לדיור), התשס״ב־2002, סעיפים 2 עד 8 ו־10, ותוספת שנייה", "url": BOI_HOME},
            "from": RESEARCH}
    return rules, baskets, forecast, fees


def main():
    built = time.strftime("%Y-%m-%d")
    try:
        ser, url = read_bir()
        rates, market = build_market(ser, url)
    except Exception as e:
        log(f"BIR_MRTG_99 failed ({e}); keeping the research values")
        rates, market = fallback_market()
    try:
        policy = read_policy()
    except Exception as e:
        log(f"policy rate failed ({e}); keeping the research values")
        p = FB["policy"]
        policy = {"rate": p["rate"], "prime": round(p["rate"] + 1.5, 2), "from": p["from"], "asof": p["asof"], "path2026": FB["path"], "from_research": RESEARCH,
                  "src": {"label": "בנק ישראל, ריבית בנק ישראל (סדרה MNT_RIB_BOI_D), " + RESEARCH_HE, "url": U_RATE}}
    try:
        term = read_xls()
    except Exception as e:
        log(f"BoI average rate by term failed ({e}); keeping the research values")
        term = fallback_xls()
    cpi = cpi_block()
    rules, baskets, forecast, fees = fixed_blocks()
    # the official average for each calculator track (what the rate field opens with) and the reference used by the offer check
    nl = term["nl"]["buckets"]
    tracks = {  # ref: where the opening rate comes from (sdmx = the monthly track average; term = the average-by-term file, nominal)
        "fixed_nl": {"label": "קבועה לא צמודה (קל״צ)", "short": "קל״צ", "linked": False, "kind": "fixed", "rate": rates["fixed_nl"]["rate"], "ref": {"type": "sdmx", "key": "fixed_nl"}, "term_file": "nl"},
        "fixed_cpi": {"label": "קבועה צמודה למדד (ק״צ)", "short": "ק״צ", "linked": True, "kind": "fixed", "rate": rates["fixed_cpi"]["rate"], "ref": {"type": "sdmx", "key": "fixed_cpi"}, "term_file": "cpi"},
        "prime": {"label": "פריים", "short": "פריים", "linked": False, "kind": "prime", "rate": nl[0]["nom"], "ref": {"type": "term", "file": "nl", "bucket": 0}, "term_file": "nl", "term_bucket": 0},
        "var5_cpi": {"label": "משתנה כל 5 שנים, צמודה למדד", "short": "משתנה צמודה", "linked": True, "kind": "var5", "rate": rates["var_cpi"]["rate"], "ref": {"type": "sdmx", "key": "var_cpi"}, "term_file": "cpi", "term_bucket": 0},
        "var5_nl": {"label": "משתנה כל 5 שנים, לא צמודה", "short": "משתנה לא צמודה", "linked": False, "kind": "var5", "rate": nl[1]["nom"], "ref": {"type": "term", "file": "nl", "bucket": 1}, "term_file": "nl", "term_bucket": 1},
        "zakaut": {"label": "הלוואת זכאות", "short": "זכאות", "linked": True, "kind": "fixed", "rate": rates["fixed_cpi"]["rate"], "ref": {"type": "sdmx", "key": "fixed_cpi"}, "directed": True},
    }
    sources = [market["src"], policy["src"], term["nl"]["src"], term["cpi"]["src"], cpi["src"], rules["src"], baskets["src"], fees["src"], forecast["src"]]
    data = {"key": "boim", "built": built, "rates": rates, "market": market, "policy": policy, "term": term, "cpi": cpi, "forecast": forecast,
            "rules": rules, "baskets": baskets, "fees": fees, "tracks": tracks, "sources": sources, "log": LOG}
    json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
