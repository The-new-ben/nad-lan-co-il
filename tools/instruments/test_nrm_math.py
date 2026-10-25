# -*- coding: utf-8 -*-
"""U3 nrm v2 (Israel mortgage calculator for foreigners): cross-check of the calculator math.

An independent Python port (Spitzer payment per track, the Directive 329 caps by status and the weighted cap of mixed buyers,
the purchase tax track by residency on the real ptax.json brackets, the income caps at 50% and one third in the buyer's currency,
the cash to close, the "what can my cash buy" solver, prime +1, a year of CPI, the 10% shekel swing and the warnings) recomputes
the cases; the same cases run through the real tool file (plugins/.../tools/nrm.js, window.NLNR.full) in node; every output must
agree to the shekel. The hand values of dna.md (sections 6, 8.4 T3/T5, 8.6, 8.8 FAQ 12 and 25) must hold at the Bank of Israel
rates of 23.10.2026 (dna section 6; the fixture below, since data/boi-fx.json may hold another day). Last, the v1 default case
(git HEAD version of nrm.js) and the v2 default case must show the same loan, payment, tax, fees and cash to close.
    python tools/instruments/test_nrm_math.py      (needs node and git on PATH; exits 1 on any mismatch)"""
import json
import math
import os
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "instruments")
REL = "plugins/nadlan-config/assets/instruments/tools/nrm.js"
N = json.load(open(os.path.join(A, "data", "nrm.json"), encoding="utf-8"))
P = json.load(open(os.path.join(A, "data", "ptax.json"), encoding="utf-8"))
# Bank of Israel representative rates, 23.10.2026 (dna section 6; CAD/AUD/ZAR same day); 30-day range from 23.9
FX = {"key": "fx", "source": "Bank of Israel representative exchange rates (series RER_<currency>_ILS)", "url": "https://www.boi.org.il/",
      "fx": {"USD": {"rate": 3.112, "date": "2026-10-23", "min30": 3.017, "max30": 3.112},
             "EUR": {"rate": 3.4844, "date": "2026-10-23", "min30": 3.4291, "max30": 3.4919},
             "GBP": {"rate": 4.1624, "date": "2026-10-23", "min30": 4.0068, "max30": 4.1624},
             "CAD": {"rate": 2.2204, "date": "2026-10-23", "min30": 2.2204, "max30": 2.2204},
             "AUD": {"rate": 2.1843, "date": "2026-10-23", "min30": 2.1843, "max30": 2.1843},
             "ZAR": {"rate": 0.1879, "date": "2026-10-23", "min30": 0.1879, "max30": 0.1879}}}


# ------------------------------------------------------------------------------------------------ the independent port
def pmt(L, annual, n):
    r = annual / 1200.0
    return L / n if r == 0 else L * r / (1 - (1 + r) ** (-n))


def tax_on(price, brackets):
    total, low = 0.0, 0.0
    for top, rate in brackets:
        top = math.inf if top is None else top
        if price > low:
            total += (min(price, top) - low) * rate
        if price <= top:
            break
        low = top
    return total


CAPS = N["ltv_by_status"]


def status_cap(status, share):
    if status == "mixed":
        s = min(max(share, 0), 100) / 100.0
        return s * CAPS["cit_first"] + (1 - s) * CAPS["foreign"]
    return CAPS[status]


def tax_track(status, live):
    if status == "oleh":
        return "oleh"
    if status == "foreign" or live != "israel":
        return "foreign"
    return "extra" if status == "cit_own" else "single"


RATES = {r["id"]: r for r in N["rates"]}


def mix(c):
    prime = N["prime"] + c.get("spread", 0)
    if c["mix"] == "fx":
        return [dict(k="fx", w=1.0, rate=c["rate"], cpi=False, prime=False, var=True, fx=True)]
    if c["mix"] in N["baskets"]:
        out = []
        for k, w in N["baskets"][c["mix"]]:
            r = RATES[k]
            out.append(dict(k=k, w=w, rate=prime if r.get("prime") else r["rate"], cpi=bool(r.get("cpi")), prime=bool(r.get("prime")), var=bool(r.get("variable")), fx=False))
        return out
    r = RATES[c["track"]]
    return [dict(k=c["track"], w=1.0, rate=c["rate"], cpi=bool(r.get("cpi")), prime=bool(r.get("prime")), var=bool(r.get("variable")), fx=False)]


BASE = dict(status="foreign", share=50, live="abroad", mode="borrow", price=4000000, cash=0, cur="USD", income=0, commit=0, appr=100, ltv=50, years=25,
            mix="one", track="fixed", rate=4.62, spread=0, cpi=2.0, lawyer=0.5)


def py(case):
    c = dict(BASE); c.update(case)
    fxr = FX["fx"][c["cur"]]["rate"]
    n = round(c["years"] * 12)
    capr = status_cap(c["status"], c["share"])
    tt = tax_track(c["status"], c["live"])
    parts = mix(c)
    per_shekel = sum(pmt(p["w"], p["rate"], n) for p in parts)
    inc, com = c["income"] * fxr, c["commit"] * fxr
    disp, has_inc = inc - com, inc > 0
    inc50 = max(0, disp) * 0.5 / per_shekel if has_inc else math.inf
    inc33 = max(0, disp) / 3.0 / per_shekel if has_inc else math.inf
    a, l = min(c["appr"], 100) / 100.0, min(c["ltv"], 100) / 100.0

    def costs(price, loan):
        tax = tax_on(price, P["tracks"][tt])
        lawyer = price * c["lawyer"] / 100 * (1 + N["vat"])
        fee = min(loan * N["mortgage_fee"]["rate"], N["mortgage_fee"]["max"]) if loan > 0 else 0
        appr = N["appraiser"] if loan > 0 else 0
        return tax, lawyer, fee, appr, price - loan + tax + lawyer + fee + appr

    price33 = None
    if c["mode"] == "cash":
        cash_ils = c["cash"] * fxr
        l = min(l, capr)

        def loan_at(p, lim):
            return max(0.0, min(p * a * l, lim))

        def best(lim):  # step search in ₪1,000 (the tool bisects, then floors to ₪1,000): the last step that still fits
            lo, hi = 0, int(5 * cash_ils / 1000) + 1000
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if costs(mid * 1000, loan_at(mid * 1000, lim))[4] <= cash_ils:
                    lo = mid
                else:
                    hi = mid
            return lo * 1000
        price = best(inc50)
        loan = loan_at(price, inc50)
        if has_inc:
            price33 = best(inc33)
    else:
        price = c["price"]
        loan = price * a * l
    value = price * a
    cap_loan = value * capr
    tax, lawyer, fee, appr, cash = costs(price, loan)
    ms = [pmt(loan * p["w"], p["rate"], n) for p in parts]
    first = sum(ms)
    up1 = sum(pmt(loan * p["w"], p["rate"] + 1, n) if (p["prime"] or p["fx"]) else m for p, m in zip(parts, ms))
    year1 = sum(m * (1 + c["cpi"] / 100) if p["cpi"] else m for p, m in zip(parts, ms))
    var_share = sum(p["w"] for p in parts if p["var"] and not (p["fx"] and c["status"] == "foreign"))
    pti = (first / disp if disp > 0 else math.inf) if has_inc else None
    all_fx = all(p["fx"] for p in parts)
    swing = (first / fxr,) * 3 if all_fx else (first / fxr, first / (fxr * 1.1), first / (fxr * 0.9))
    return dict(capR=capr, taxTrack=tt, value=value, capLoan=cap_loan, inc50=None if not has_inc else inc50, inc33=None if not has_inc else inc33,
                maxLoan=min(cap_loan, inc50), binds="income" if has_inc and inc50 < cap_loan - 0.5 else "status", price=price, price33=price33, loan=loan,
                tax=tax, lawyer=lawyer, fee=fee, appr=appr, cash=cash, first=first, up1=up1, year1=year1, interest=sum(m * n for m in ms) - loan,
                varShare=var_share, pti=pti, need50=first / 0.5, need33=first * 3, swing_now=swing[0], swing_weak=swing[1], swing_strong=swing[2],
                w_variable=var_share > N["rules"]["variable_max"] + 0.001, w_term=c["years"] > 30, w_over=loan > cap_loan + 0.5,
                w_pti=pti is not None and pti > 0.5 + 1e-9)


# ------------------------------------------------------------------------------------------------ the cases
CASES = {
    "default_foreign": {},
    "income_status_binds": dict(income=12000),
    "citizen_abroad_75": dict(status="cit_first", live="abroad", ltv=75),
    "oleh_12A": dict(status="oleh", live="israel", ltv=75),
    "resident_single": dict(status="cit_first", live="israel", ltv=75),
    "citizen_owns_extra": dict(status="cit_own", live="israel", ltv=50),
    "citizen_selling_70": dict(status="cit_sell", live="abroad", ltv=70),
    "couple_50_50": dict(status="mixed", share=50, ltv=62.5),
    "couple_70_30_israel": dict(status="mixed", share=70, live="israel", ltv=67.5),
    "loan_500k_usd_30y": dict(price=3112000, ltv=50, years=30),
    "income_binds": dict(status="cit_first", ltv=75, income=5000, commit=500),
    "pti_over_50": dict(status="cit_first", ltv=75, income=8000, commit=3000),
    "over_cap": dict(ltv=60),
    "term_35": dict(years=35),
    "appraisal_90": dict(appr=90, income=15000, cur="EUR"),
    "thirds_b2": dict(mix="b2", spread=-0.5, cpi=2.0, income=12000, cur="GBP"),
    "half_prime_b3": dict(mix="b3", spread=0.3, income=12000),
    "prime_only": dict(mix="one", track="variable", rate=4.75),
    "cpi_fixed_only": dict(mix="one", track="linked", rate=3.29, cpi=2.0),
    "fx_loan_foreign": dict(mix="fx", rate=4.86, income=12000),
    "cad_income": dict(cur="CAD", income=20000, commit=1000),
    "aud": dict(cur="AUD", income=18000),
    "zar": dict(cur="ZAR", income=150000),
    "cash_foreign_800k": dict(mode="cash", cash=800000, income=12000),
    "cash_thirds": dict(mode="cash", cash=800000, mix="b2", income=12000),
    "cash_income_binds": dict(mode="cash", status="cit_first", ltv=75, cash=1500000, income=4000),
    "cash_clipped": dict(mode="cash", cash=600000, ltv=70, cur="EUR"),
    "cash_no_income": dict(mode="cash", cash=500000, status="oleh", live="israel", ltv=75, appr=95),
}

NODE = r"""
const fs = require('fs'), vm = require('vm');
const [src, casesFile, nFile, pFile, fxFile] = process.argv.slice(2);
const win = {}; const ctx = vm.createContext({ window: win, Intl, Math, JSON, console });
vm.runInContext(fs.readFileSync(src, 'utf8'), ctx);
const N = JSON.parse(fs.readFileSync(nFile, 'utf8')), P = JSON.parse(fs.readFileSync(pFile, 'utf8')), FX = JSON.parse(fs.readFileSync(fxFile, 'utf8'));
const cases = JSON.parse(fs.readFileSync(casesFile, 'utf8')), base = cases.__base; delete cases.__base;
const out = {};
for (const k of Object.keys(cases)) {
  const r = win.NLNR.full(Object.assign({}, base, cases[k]), P, N, FX);
  out[k] = { capR: r.capR, taxTrack: r.taxTrack, value: r.value, capLoan: r.capLoan, inc50: r.inc50, inc33: r.inc33, maxLoan: r.maxLoan, binds: r.binds,
    price: r.price, price33: r.price33, loan: r.loan, tax: r.tax, lawyer: r.lawyer, fee: r.fee, appr: r.appr, cash: r.cash, first: r.first, up1: r.up1, year1: r.year1,
    interest: r.interest, varShare: r.varShare, pti: r.pti === Infinity ? 'inf' : r.pti, need50: r.need50, need33: r.need33,
    swing_now: r.swing.now, swing_weak: r.swing.weak, swing_strong: r.swing.strong, w_variable: r.warn.variable, w_term: r.warn.term, w_over: r.warn.over, w_pti: r.warn.pti };
}
process.stdout.write(JSON.stringify(out));
"""

# v1 (git HEAD) and v2 rendered through their own specs: the default case, numbers as the reader sees them
NODE_UI = r"""
const fs = require('fs'), vm = require('vm');
const [oldSrc, newSrc, nOld, nNew, pFile, fxFile] = process.argv.slice(2);
function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
function pick(tx, lang) { const o = {}; Object.keys(tx).forEach(k => { o[k] = tx[k][lang] != null ? tx[k][lang] : tx[k].he; }); return o; }
function load(src, lang) {
  const REG = {}; let spec = null;
  const NI = { register: (id, s) => { REG[id] = s; }, mount: (root, s) => { spec = s; }, langOf: () => lang, pick, esc, fmt: {}, lang };
  const win = { NadLanInstruments: NI }; const ctx = vm.createContext({ window: win, Intl, Math, JSON, console });
  vm.runInContext(fs.readFileSync(src, 'utf8'), ctx);
  return { REG, get spec() { return spec; } };
}
const P = JSON.parse(fs.readFileSync(pFile, 'utf8')), FX = JSON.parse(fs.readFileSync(fxFile, 'utf8'));
const dOld = { ptax: P, nrm: JSON.parse(fs.readFileSync(nOld, 'utf8')), fx: FX }, dNew = { ptax: P, nrm: JSON.parse(fs.readFileSync(nNew, 'utf8')), fx: FX };
const o = load(oldSrc, 'en'), so = o.REG.nrm, ro = so.compute(so.defaults(dOld), dOld);
const out = { old: { answer: ro.answer.value, lines: ro.lines.map(l => [l.label, l.value]), table: ro.table.rows } };
for (const lang of ['en', 'he']) {
  const n = load(newSrc, lang); n.REG.nrm.custom({}, dNew); const sn = n.spec;
  const v = JSON.parse(JSON.stringify(sn.defaults(dNew)));
  const rn = sn.compute(v, dNew, null);
  out[lang] = { answer: rn.answer.value, sub: rn.answer.sub, lines: rn.lines.map(l => [l.label, l.value]), table: rn.table.rows, note: rn.note, scen: rn.scenarios.map(s => s.value),
    fields: sn.fields.map(f => f.id), figure: rn.figure.length, presets: (sn.presets || []).map(p => p.key) };
  // every preset computes without an error
  out[lang].presetErrors = (sn.presets || []).filter(p => { const w = Object.assign(JSON.parse(JSON.stringify(sn.defaults(dNew))), p.set); const r = sn.compute(w, dNew, null); return !!r.error; }).map(p => p.key);
  // cash mode renders too
  const rc = sn.compute(Object.assign({}, v, { mode: 'cash', cash: 800000 }), dNew, null); out[lang].cashAnswer = rc.error ? 'ERROR ' + rc.error.msg : rc.answer.value;
}
process.stdout.write(JSON.stringify(out));
"""

bad = 0


def check(name, got, want, tol=0.5):
    global bad
    ok = (got == want) if isinstance(want, (bool, str, list)) or want is None else (got is not None and abs(got - want) <= tol)
    if not ok:
        bad += 1
    print(("OK   " if ok else "BAD  ") + name + ": " + str(round(got, 2) if isinstance(got, float) else got) + "  (want " + str(want) + ")")


def run_node(script, args):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(script)
        js = f.name
    try:
        res = subprocess.run(["node", js] + args, capture_output=True, text=True, encoding="utf-8")
        if res.returncode:
            print(res.stderr)
            sys.exit(1)
        return json.loads(res.stdout)
    finally:
        os.unlink(js)


def tmpjson(obj):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(obj, f, ensure_ascii=False)
    f.close()
    return f.name


fx_file = tmpjson(FX)
cases_file = tmpjson(dict(CASES, __base=BASE))
JS = run_node(NODE, [os.path.join(A, "tools", "nrm.js"), cases_file, os.path.join(A, "data", "nrm.json"), os.path.join(A, "data", "ptax.json"), fx_file])

print("== 1. the port and the real tool agree (%d cases)" % len(CASES))
KEYS = ["capR", "value", "capLoan", "inc50", "inc33", "maxLoan", "price", "price33", "loan", "tax", "lawyer", "fee", "appr", "cash", "first", "up1", "year1",
        "interest", "varShare", "pti", "need50", "need33", "swing_now", "swing_weak", "swing_strong"]
FLAGS = ["taxTrack", "binds", "w_variable", "w_term", "w_over", "w_pti"]
for k, case in CASES.items():
    p, j = py(case), JS[k]
    miss = []
    for key in KEYS:
        a, b = p[key], j[key]
        if a == math.inf:
            a = "inf"
        if a is None or b is None or isinstance(a, str) or isinstance(b, str):
            if a != b:
                miss.append("%s %s/%s" % (key, a, b))
        elif abs(a - b) > (1e-6 if key in ("capR", "varShare", "pti") else 0.5):
            miss.append("%s %.2f/%.2f" % (key, a, b))
    for key in FLAGS:
        if p[key] != j[key]:
            miss.append("%s %s/%s" % (key, p[key], j[key]))
    if miss:
        bad += 1
    print(("OK   " if not miss else "BAD  ") + k + (": " + "; ".join(miss) if miss else ": loan %s, payment %s, cash %s, tax %s (%s)" % (
        round(j["loan"]), round(j["first"]), round(j["cash"]), round(j["tax"]), j["taxTrack"])))

print("\n== 2. dna.md hand values (BoI rates of 23.10.2026)")
d = JS["default_foreign"]
check("T3: 2,000,000 over 25y at 4.62% -> 11,253", round(d["first"]), 11253, 0)
check("T3: income needed at the 50% cap 22,507", round(d["need50"]), 22507, 0)
check("T3: income needed at one third 33,760", round(d["need33"]), 33760, 0)
check("T3: 22,507 in dollars 7,232", round(d["need50"] / 3.112), 7232, 0)
check("T3: 33,760 in dollars 10,848", round(d["need33"] / 3.112), 10848, 0)
check("T5 non-citizen: loan 2,000,000", d["loan"], 2000000, 0.01)
check("T5 non-citizen: tax 320,000", d["tax"], 320000, 0.01)
check("T5 non-citizen: cash to close 2,344,610", round(d["cash"]), 2344610, 0)
check("T5 non-citizen: cash in $ 753,409", round(d["cash"] / 3.112), 753409, 0)
check("T5 non-citizen: cash in EUR 672,888", round(d["cash"] / 3.4844), 672888, 0)
check("T5 non-citizen: cash in GBP 563,283", round(d["cash"] / 4.1624), 563283, 0)
check("T5 non-citizen: payment in $ 3,616", round(d["swing_now"]), 3616, 0)
c = JS["citizen_abroad_75"]
check("T5 citizen abroad: loan 3,000,000", c["loan"], 3000000, 0.01)
check("T5 citizen abroad: tax 320,000 (non-resident 8%)", c["tax"], 320000, 0.01)
check("T5 citizen abroad: cash to close 1,344,610", round(c["cash"]), 1344610, 0)
check("T5 citizen abroad: cash in $ 432,073", round(c["cash"] / 3.112), 432073, 0)
check("T5 citizen abroad: payment 16,880", round(c["first"]), 16880, 0)
check("T5 citizen abroad: payment in $ 5,424", round(c["first"] / 3.112), 5424, 0)
o = JS["oleh_12A"]
check("T5 oleh 12A: tax 10,106", round(o["tax"]), 10106, 0)
check("T5 oleh 12A: cash to close 1,034,716", round(o["cash"]), 1034716, 0)
check("T5 oleh 12A: cash in $ 332,492", round(o["cash"] / 3.112), 332492, 0)
s = JS["resident_single"]
check("T5 resident single home: tax 95,538", round(s["tax"]), 95538, 0)
check("T5 resident single home: cash to close 1,120,148", round(s["cash"]), 1120148, 0)
check("T5 resident single home: cash in $ 359,945", round(s["cash"] / 3.112), 359945, 0)
u = JS["loan_500k_usd_30y"]
check("FAQ 25: $500,000 = 1,556,000", u["loan"], 1556000, 0.01)
check("FAQ 25: 30 years at 4.62% -> 7,995", round(u["first"]), 7995, 0)
check("FAQ 25: about $2,569", round(u["first"] / 3.112), 2569, 0)
check("8.6 swing: today $3,616", round(d["swing_now"]), 3616, 0)
check("8.6 swing: shekel weakens 10% -> $3,287", round(d["swing_weak"]), 3287, 0)
check("8.6 swing: shekel strengthens 10% -> $4,018", round(d["swing_strong"]), 4018, 0)
check("Q&A joint buyers: 50/50 of 75% and 50% = 62.5%", JS["couple_50_50"]["capR"], 0.625, 1e-9)
check("329 s.2: replacement home 70%", JS["citizen_selling_70"]["capR"], 0.70, 1e-9)
check("329 s.2: citizen who owns a home 50%", JS["citizen_owns_extra"]["capR"], 0.50, 1e-9)

print("\n== 3. purchase tax brackets in ptax.json against dna T5 (reported, not forced)")
for name, track, want in (("foreign resident", "foreign", 320000), ("oleh 12A", "oleh", 10106), ("resident single home", "single", 95538), ("additional home", "extra", 320000)):
    got = tax_on(4000000, P["tracks"][track])
    print(("same " if round(got) == want else "DIFF ") + "%s on 4,000,000: ptax.json gives %s, dna T5 %s" % (name, round(got), want))

print("\n== 4. rules and warnings")
check("thirds: variable 2/3 is within 66.66% (no warning)", JS["thirds_b2"]["w_variable"], False)
check("prime only: 100% variable is flagged", JS["prime_only"]["w_variable"], True)
check("foreign currency loan to a non-citizen: outside the cap (s.12.3)", JS["fx_loan_foreign"]["w_variable"], False)
check("foreign currency loan: payment in $ does not move with the shekel", JS["fx_loan_foreign"]["swing_weak"] - JS["fx_loan_foreign"]["swing_now"], 0, 1e-6)
check("term 35 years is flagged", JS["term_35"]["w_term"], True)
check("60% for a non-citizen is above the cap", JS["over_cap"]["w_over"], True)
check("payment above 50% of income is flagged", JS["pti_over_50"]["w_pti"], True)
check("income binds below the 75% cap", JS["income_binds"]["binds"], "income")
check("12,000 a month: the 50% status cap binds", JS["income_status_binds"]["binds"], "status")
check("prime +1: only the prime half of basket 3 reprices", JS["half_prime_b3"]["up1"] - JS["half_prime_b3"]["first"],
      pmt(JS["half_prime_b3"]["loan"] / 2, N["prime"] + 0.3 + 1, 300) - pmt(JS["half_prime_b3"]["loan"] / 2, N["prime"] + 0.3, 300), 0.01)
check("fixed not linked only: prime +1 changes nothing", JS["default_foreign"]["up1"] - JS["default_foreign"]["first"], 0, 1e-9)
check("CPI-linked fixed: a year of 2% inflation", JS["cpi_fixed_only"]["year1"] / JS["cpi_fixed_only"]["first"], 1.02, 1e-9)
check("appraisal 90%: value 3,600,000", JS["appraisal_90"]["value"], 3600000, 0.01)
check("appraisal 90%: loan 50% of the value", JS["appraisal_90"]["loan"], 1800000, 0.01)
for k in ("cash_foreign_800k", "cash_thirds", "cash_income_binds", "cash_clipped", "cash_no_income"):
    case = dict(BASE); case.update(CASES[k])
    cash_ils = case["cash"] * FX["fx"][case["cur"]]["rate"]
    r = JS[k]
    nxt = py(dict(CASES[k], mode="borrow", price=r["price"] + 1000, ltv=min(case["ltv"], status_cap(case["status"], case["share"]) * 100)))
    # the next ₪1,000 step must not fit: recompute its cash need with the same loan rule (cap, income limit)
    lim = r["inc50"] if r["inc50"] is not None else math.inf
    a = min(case["appr"], 100) / 100
    l = min(case["ltv"] / 100, status_cap(case["status"], case["share"]))
    loan_n = max(0, min((r["price"] + 1000) * a * l, lim))
    tt = tax_track(case["status"], case["live"])
    need_n = (r["price"] + 1000) - loan_n + tax_on(r["price"] + 1000, P["tracks"][tt]) + (r["price"] + 1000) * case["lawyer"] / 100 * 1.18 + (min(loan_n * 0.0025, 360) + 650 if loan_n > 0 else 0)
    check("cash mode %s: price %s fits the cash (%s <= %s)" % (k, round(r["price"]), round(r["cash"]), round(cash_ils)), r["cash"] <= cash_ils + 1e-6, True)
    check("cash mode %s: the next ₪1,000 does not fit" % k, need_n > cash_ils, True)
check("cash mode: 75% cap clipped to the 50% of a non-citizen", JS["cash_clipped"]["loan"] / JS["cash_clipped"]["value"], 0.5, 1e-9)
check("cash mode: income limits the loan", JS["cash_income_binds"]["loan"], JS["cash_income_binds"]["inc50"], 0.5)

print("\n== 5. v1 (git HEAD) against v2: the default case as the reader sees it")
old_src = subprocess.run(["git", "-C", ROOT, "show", "HEAD:" + REL], capture_output=True, text=True, encoding="utf-8").stdout
old_data = subprocess.run(["git", "-C", ROOT, "show", "HEAD:plugins/nadlan-config/assets/instruments/data/nrm.json"], capture_output=True, text=True, encoding="utf-8").stdout
old_js, old_n = tmpjson({}), tmpjson({})
open(old_js, "w", encoding="utf-8").write(old_src)
open(old_n, "w", encoding="utf-8").write(old_data)
real_fx = os.path.join(A, "data", "boi-fx.json")
UI = run_node(NODE_UI, [old_js, os.path.join(A, "tools", "nrm.js"), old_n, os.path.join(A, "data", "nrm.json"), os.path.join(A, "data", "ptax.json"), real_fx])
ol = dict((x[0], x[1]) for x in UI["old"]["lines"])
otab = dict((x[0], x) for x in UI["old"]["table"])
nl = UI["en"]["lines"]
nval = lambda prefix: next((x[1] for x in nl if x[0].startswith(prefix)), None)
ntab = dict((x[0].split(" (")[0], x) for x in UI["en"]["table"])
check("loan  v1 " + ol["Loan"].split(" · ")[0], nval("Your loan"), ol["Loan"].split(" · ")[0])
check("first payment  v1 " + ol["Monthly payment, 300 payments"], nval("First monthly payment"), ol["Monthly payment, 300 payments"])
check("total interest  v1 " + ol["Total interest if the rate holds"], nval("Total interest"), ol["Total interest if the rate holds"])
check("purchase tax  v1 " + ol["Purchase tax, foreign resident"].split(" · ")[0], nval("Purchase tax"), ol["Purchase tax, foreign resident"].split(" · ")[0])
check("lawyer, appraiser, fee  v1 " + ol["Lawyer incl. VAT, appraiser, file fee"], nval("Lawyer incl. VAT"), ol["Lawyer incl. VAT, appraiser, file fee"])
check("cash to close  v1 " + otab["Cash to close"][1] + " · " + UI["old"]["answer"], nval("Cash to close"), otab["Cash to close"][1] + " · " + UI["old"]["answer"])
for row in ("Price", "Lawyer incl. VAT", "Bank appraiser", "Mortgage file fee"):
    check("table row %s  v1 %s" % (row, otab[row][1]), ntab[row][1], otab[row][1])
print("v2 en answer:", UI["en"]["answer"], "|", UI["en"]["sub"])
print("v2 he answer:", UI["he"]["answer"], "|", UI["he"]["sub"])
check("v2 fields keep the v1 ids", all(x in UI["en"]["fields"] for x in ("price", "cur", "ltv", "years", "track", "rate", "lawyer")), True)
check("v2 en presets compute without an error", UI["en"]["presetErrors"], [])
check("v2 he presets compute without an error", UI["he"]["presetErrors"], [])
print("v2 cash mode answer (en / he):", UI["en"]["cashAnswer"], "/", UI["he"]["cashAnswer"])
check("v2 he: no em or en dash in the Hebrew output", any(ch in json.dumps(UI["he"], ensure_ascii=False) for ch in (chr(0x2013), chr(0x2014))), False)
BANNED = ["ממשק", "פלטפורמה", "סימולציה", "אינטראקטיבי", "בקרוב", "המערכת", "מערכת"]
he_src = open(os.path.join(A, "tools", "nrm.js"), encoding="utf-8").read()
check("v2 source: none of the banned Hebrew words", [w for w in BANNED if w in he_src], [])
check("v2 source: no em or en dash", any(ch in he_src for ch in (chr(0x2013), chr(0x2014))), False)

for f in (fx_file, cases_file, old_js, old_n):
    os.unlink(f)
print("\n%s: %d mismatch%s" % ("FAIL" if bad else "PASS", bad, "" if bad == 1 else "es"))
sys.exit(1 if bad else 0)
