# -*- coding: utf-8 -*-
"""Cross-check of the yield and cash-flow map (tool "invest"): three independent paths must give the same numbers.
  1. Python, from invest.json, with the formulas of dna.md section 6 (gross yield, Spitzer payment, rent minus payment at the 50% cap,
     break-even share = rent x annuity factor / price, equity = price - loan + purchase tax + lawyer 0.5% + VAT).
  2. The research: the computed lines of dna.md section 6 / T2 (each expected figure is also looked up in dna.md itself), and every row
     of the research tables data/cashflow-by-city.csv and data/breakeven-ltv-4rooms.csv.
  3. The tool: tools/invest.js run in node (window.NLIV, the same functions the page uses), on the same cities.
  python tools/instruments/test_invest_math.py      (exit code 1 on any mismatch)"""
import csv, io, json, os, re, statistics, subprocess, sys

if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
A = os.path.join(R, "plugins", "nadlan-config", "assets", "instruments")
U2 = os.path.join(R, "docs", "research", "2026-10-26-upgrades", "u2-investment")
D = json.load(io.open(os.path.join(A, "data", "invest.json"), encoding="utf-8"))
DNA = io.open(os.path.join(U2, "dna.md"), encoding="utf-8").read()
L = D["rules"]; RATE = next(r["rate"] for r in L["rates"] if r["id"] == "fixed"); N = 300
bad = 0


def ok(name, got, want, tol=0):
    global bad
    good = abs(got - want) <= tol if isinstance(want, (int, float)) else got == want
    if not good: bad += 1
    print(("OK   " if good else "BAD  ") + name + ": " + str(got) + ("" if good else "  (want " + str(want) + ")"))


def in_dna(snippet):
    global bad
    hit = snippet in DNA
    if not hit: bad += 1
    print(("OK   " if hit else "BAD  ") + "dna.md says: " + snippet)


def pmt(P, annual, n): r = annual / 1200; return P * r / (1 - (1 + r) ** -n)
def af(annual, n): r = annual / 1200; return (1 - (1 + r) ** -n) / r
def ptax(price, br):
    t = 0; lo = 0
    for hi, rate in br:
        hi = float("inf") if hi is None else hi; top = min(price, hi)
        if top > lo: t += (top - lo) * rate
        if price <= hi: break
        lo = hi
    return t


def row(name): return next(r for r in D["rows"] if r["n"] == name)


def calc(price, rent, ltv=0.5, track="extra", lawyer=0.5):
    loan = price * ltv; pay = pmt(loan, RATE, N); tax = ptax(price, L["ptax"][track]); law = price * lawyer / 100 * (1 + L["vat"])
    return {"gross": rent * 12 / price, "loan": loan, "pay": pay, "cf": rent - pay, "be": rent * af(RATE, N) / price, "tax": tax, "law": law,
            "equity": price - loan + tax + law, "ten": 0.1 * rent, "exempt": rent if rent <= L["rentTax"]["ceiling"] else max(0, 2 * L["rentTax"]["ceiling"] - rent)}


print("== 1. the rules in invest.json ==")
ok("rate: Bank of Israel average fixed not linked, " + L["ratesPeriod"], RATE, 4.62)
ok("investment-home loan cap", L["ltv"]["extra"], 0.5)
ok("purchase tax, additional home, until", L["ptax"]["until"]["extra"], "2027-02-10")
ok("rental exemption ceiling / zero point", (L["rentTax"]["ceiling"], L["rentTax"]["zero"]), (5654, 11308))
ok("annuity factor, 300 months at 4.62%", round(af(RATE, N), 2), 177.73)
ok("payment per 100,000 NIS", round(pmt(100000, RATE, N)), 563)
in_dna("**563 ₪ a month per 100,000 ₪**"); in_dna("annuity factor (177.73 at 4.62%, 300 months)")

print("== 2. the six cities against dna.md section 6 and T2 (4 rooms) ==")
EXPECT = {  # gross %, payment, rent minus payment, break-even %, equity; quarter
    "ישראל":       ("2026-06", 2.85, 5708, -883, 42.3, 1188674),
    "תל אביב-יפו": ("2026-03", 2.29, 14713, -4713, 34.0, 3064140),
    "ירושלים":     ("2026-03", 3.00, 8109, -909, 44.4, 1688798),
    "חיפה":        ("2026-03", 3.31, 4494, -94, 49.0, 935975),
    "באר שבע":     ("2026-03", 3.59, 3385, 215, 53.2, 704955),
    "אשקלון":      ("2026-03", 3.76, 3955, 445, 55.6, 823658),
}
PY = {}
for name, (q, g, pay, cf, be, eq) in EXPECT.items():
    p = row(name)["r"]["4"]; x = calc(p["price"], p["rent"]); PY[name] = x
    ok(name + " quarter", p["q"], q)
    ok(name + " gross yield %", round(100 * x["gross"], 2), g)
    ok(name + " payment", round(x["pay"]), pay)
    ok(name + " rent minus payment", round(x["cf"]), cf)
    ok(name + " break-even share %", round(100 * x["be"], 1), be)
    ok(name + " equity needed", round(x["equity"]), eq)
in_dna("National 42.3%; Tel Aviv 34.0%; Haifa 49.0%; Beer Sheva 53.2%; Ashkelon 55.6%; above 50% in 13 cities")
in_dna("national −883 ₪; Tel Aviv −4,713 ₪")
in_dna("| ירושלים | /investment/jerusalem-investment-apartment/ | 1-3.2026 | 7,200 | 6,139 ±77 | 2,882,400 | 3.00% | 2.56% | 2.42% | 8,109 | -909 | 44.4% | 1,688,798 |")
nat = row("ישראל")["r"]["4"]; xn = PY["ישראל"]
ok("national purchase tax as an additional home", round(xn["tax"]), 162304); in_dna("national 4-room median 2,028,800 ₪ as an additional home: **162,304 ₪**")
ok("national purchase tax in months of rent", round(xn["tax"] / nat["rent"]), 34); in_dna("162,304 ₪ = 34 months of the 4,825 ₪ median rent")
ok("national single-home purchase tax", round(ptax(nat["price"], L["ptax"]["single"])), 1752)

print("== 3. the 65-city lines ==")
c4 = [r for r in D["rows"] if not r.get("nat") and "4" in r["r"] and r["r"]["4"]["q"] == D["cityQ"]]
g4 = sorted((r["r"]["4"]["rent"] * 12 / r["r"]["4"]["price"], r["n"]) for r in c4)
ok("cities with 4-room rent and price for January to March 2026", len(c4), 65)
ok("median gross yield %", round(100 * statistics.median([g for g, _ in g4]), 1), 3.0)
ok("lowest", (round(100 * g4[0][0], 2), g4[0][1]), (2.16, "גבעתיים")); ok("highest", (round(100 * g4[-1][0], 2), g4[-1][1]), (5.36, "נצרת"))
ok("cities between 2.3% and 3.6%", sum(1 for g, _ in g4 if 0.023 <= g <= 0.036), 54)
pos = [r["n"] for r in c4 if calc(r["r"]["4"]["price"], r["r"]["4"]["rent"])["cf"] > 0]
ok("cities where the rent covers the 50% payment", len(pos), 13)
ok("cities with break-even share above 50%", sum(1 for r in c4 if calc(r["r"]["4"]["price"], r["r"]["4"]["rent"])["be"] > 0.5), 13)
in_dna("positive in **13 of 65 cities**"); in_dna("**median 3.0%**, range 2.16% (Givatayim) to 5.36% (Nazareth; small sample, flag)")
maxp = 400000 / (0.5 + 0.08 + 0.005 * (1 + L["vat"]))
ok("400,000 own money buys up to (FAQ 20, about 683,000)", round(maxp, -3), 683000)
cb = row("ישראל")["cbs"]["4"]; ok("national CBS-rent yield % (CBS Q1 / national median Q1)", round(100 * cb["avg"] * 12 / cb["price"], 2), 3.15)
ct = row("תל אביב-יפו")["cbs"]["4"]; ok("Tel Aviv CBS-rent yield %", round(100 * ct["avg"] * 12 / ct["price"], 2), 2.03)
ok("government yield figure, Tel Aviv (all rooms, as the site shows)", row("תל אביב-יפו")["gy"], 2.72)

print("== 4. every row of the research tables ==")
n = 0; skip = 0; before = bad
for t in csv.DictReader(io.open(os.path.join(U2, "data", "cashflow-by-city.csv"), encoding="utf-8-sig")):
    name = "ישראל" if t["city"].startswith("ישראל") else t["city"]; p = row(name)["r"].get(t["rooms"]) if any(r["n"] == name for r in D["rows"]) else None
    qq = t["quarter"].split(".")[1] + "-%02d" % int(t["quarter"].split("-")[1].split(".")[0])
    if not p or p["q"] != qq: skip += 1; continue
    x = calc(p["price"], p["rent"]); n += 1
    got = (p["rent"], p["price"], round(100 * x["gross"], 2), round(x["tax"]), round(x["law"]), round(x["loan"]), round(x["pay"]), round(x["equity"]), round(x["cf"]), round(x["exempt"]), round(x["ten"]))
    want = (int(t["rent"]), int(t["price"]), float(t["gross_pct"]), int(t["ptax"]), int(t["lawyer_vat"]), int(t["loan_50"]), int(t["payment_25y_4.62"]), int(t["equity_needed"]), int(t["rent_minus_payment"]), int(t["exempt_monthly"]), int(t["tax_10pct_monthly"]))
    if got != want: bad += 1; print("BAD  cashflow-by-city.csv", name, t["rooms"], got, want)
ok("cashflow-by-city.csv rows equal (rent, price, gross, purchase tax, lawyer, loan, payment, equity, cash flow, exempt, 10%)", n - (bad - before), n)
print("     (%d rows compared, %d rows with another quarter skipped)" % (n, skip))
n = 0; before = bad
for t in csv.DictReader(io.open(os.path.join(U2, "data", "breakeven-ltv-4rooms.csv"), encoding="utf-8-sig")):
    p = row("ישראל" if t["city"].startswith("ישראל") else t["city"])["r"]["4"]; x = calc(p["price"], p["rent"]); n += 1
    got = (round(100 * x["gross"], 2), round(100 * x["be"], 1), round(x["cf"]), round(x["equity"]))
    want = (float(t["gross_pct"]), float(t["breakeven_loan_share_pct_4.62_25y"]), int(t["rent_minus_payment_50pct"]), int(t["equity_needed_50pct"]))
    if got != want: bad += 1; print("BAD  breakeven-ltv-4rooms.csv", t["city"], got, want)
ok("breakeven-ltv-4rooms.csv rows equal (gross, break-even share, cash flow, equity): 65 cities + Israel", n - (bad - before), 66)

print("== 5. the tool itself (tools/invest.js in node) ==")
JS = r"""
const fs=require('fs'),vm=require('vm'),w={};vm.runInNewContext(fs.readFileSync(process.argv[1],'utf8'),{window:w,Intl,Math,JSON,Object});
const D=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),N=w.NLIV;
const v={track:'extra',ltv:50,rsel:'fixed',years:25,lawyer:0.5,broker:0,reno:0,mgmt:0,upkeep:0,empty:0,taxtrack:'exempt',other:0};
const out={cities:{}};
for(const c of JSON.parse(process.argv[3])){const p=N.pairOf(N.rowOf(D,c),4,'gov');const x=N.calc(Object.assign({},v,{price:p.price,rent:p.rent}),D);out.cities[c]={gross:x.gross,pay:x.pay,cf:x.cf0,be:x.be,equity:x.equity,tax:x.tax};}
const R=N.ranking(D,4,v);out.n=R.length;out.pos=R.filter(c=>c.cf0>0).length;out.per100k=N.pmt(100000,4.62,300);
out.b400=N.budget(Object.assign({},v,{equity:400000,cap:0,brooms:'34'}),D).maxP;
process.stdout.write(JSON.stringify(out));
"""
try:
    js = json.loads(subprocess.run(["node", "-e", JS, os.path.join(A, "tools", "invest.js"), os.path.join(A, "data", "invest.json"), json.dumps(list(EXPECT), ensure_ascii=False)],
                                   capture_output=True, text=True, encoding="utf-8", check=True).stdout)
    for name, x in PY.items():
        j = js["cities"][name]
        ok(name + " JS = Python (gross, payment, cash flow, break-even, equity, purchase tax)",
           (round(100 * j["gross"], 2), round(j["pay"]), round(j["cf"]), round(100 * j["be"], 1), round(j["equity"]), round(j["tax"])),
           (round(100 * x["gross"], 2), round(x["pay"]), round(x["cf"]), round(100 * x["be"], 1), round(x["equity"]), round(x["tax"])))
    ok("JS ranking: cities / rent covers the payment", (js["n"], js["pos"]), (65, 13))
    ok("JS payment per 100,000", round(js["per100k"]), 563)
    ok("JS budget mode, 400,000 own money: highest price (rounded down to 100)", js["b400"], int(maxp // 100 * 100))
except (OSError, subprocess.CalledProcessError) as e:
    bad += 1; print("BAD  node run failed:", e)

print("\n%s: %d mismatches" % ("PASS" if not bad else "FAIL", bad))
sys.exit(1 if bad else 0)
