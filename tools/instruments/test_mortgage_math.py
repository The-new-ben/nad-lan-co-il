# -*- coding: utf-8 -*-
"""U1 Mortgage 2.0: cross-check of the calculator math. An independent Python port of the schedule (Spitzer, equal principal,
balloon, bullet, partial and full grace, CPI linkage, prime path and resets, prepayment, the payment-to-loan solver and the
Banking Order capitalization fee) recomputes 16 cases; the same cases run through the real tool file (tools/mortgage.js,
window.NLMG) in node; every output must agree to the shekel, and the hand values of dna.md (T5, T6, T8) must hold.
python test_mortgage_math.py   (needs node on PATH; exits 1 on any mismatch)"""
import json
import math
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "instruments")
D = json.load(open(os.path.join(A, "data", "boi-mortgage.json"), encoding="utf-8"))


# ------------------------------------------------------------------------------------------------------------ the port
def pmt(B, rm, n):
    if n <= 0:
        return B
    return B / n if rm == 0 else B * rm / (1 - (1 + rm) ** (-n))


def solve_n(B, rm, P):
    if B <= 0:
        return 0
    if rm == 0:
        return math.ceil(B / P)
    x = 1 - B * rm / P
    return math.ceil(-math.log(x) / math.log(1 + rm) - 1e-9) if x > 0 else math.inf


def scenario(o):
    kind, to, months = o.get("prime", "none"), o.get("rampTo", 0), max(1, o.get("rampMonths", 1))
    sh, frm = o.get("shock", 0), max(1, round(o.get("shockMonth", 1)))

    def prime(m):
        if kind in ("boi", "market"):
            return to * min(1, m / months)
        if kind == "up2":
            return 2
        if kind == "custom":
            return sh if m >= frm else 0
        return 0

    def reset(m):
        if kind == "up2":
            return 2
        if kind == "custom":
            return sh if m >= frm else 0
        return 0
    return {"cpi": o.get("cpi", 0), "all": o.get("all", 0), "prime": prime, "reset": reset}


def track(t, sc):
    N = max(1, round(t["years"] * 12))
    g = min(max(0, round(t.get("grace", 0))), N - 1)
    f = (1 + sc["cpi"] / 100) ** (1 / 12) if t.get("linked") else 1.0
    B, C, end, r = float(t["amount"]), 0.0, N, t["rate"]
    S = {"N": N, "pay": [], "reg": [], "bal": [], "sumI": 0.0, "sumL": 0.0, "sumP": 0.0, "lump": 0.0, "lumpMonth": 0, "prepay": None}
    pp = t.get("prepay")
    for m in range(1, N + 1):
        if B <= 0.005 or m > end:
            S["pay"].append(0.0); S["reg"].append(0.0); S["bal"].append(0.0)
            continue
        if t["kind"] == "prime":
            r = t["rate"] + sc["all"] + sc["prime"](m)
        elif t["kind"] == "var5":
            if m == 1:
                r = t["rate"] + sc["all"]
            elif (m - 1) % 60 == 0:
                r = t["rate"] + sc["all"] + sc["reset"](m)
        else:
            r = t["rate"] + sc["all"]
        L = B * (f - 1); B += L; C *= f
        rm = max(0.0, r) / 1200; I = B * rm; n = end - m + 1; lump = 0.0
        meth = t.get("method", "spitzer")
        if m <= g:
            P = 0.0 if t.get("graceType") == "full" else I
        elif meth == "equal":
            P = I + B / n
        elif meth == "bullet":
            P = I
            if n == 1:
                P = I + B; lump = B
        elif meth == "balloon":
            P = 0.0
            if n == 1:
                P = B + I; lump = P
        else:
            P = pmt(B, rm, n)
        if P < I:
            C += I - P
        else:
            x = min(C, P - I); C -= x
        B = B + I - P
        if B < 0.005:
            B = 0.0
        S["sumI"] += I; S["sumL"] += L; S["sumP"] += P
        if lump:
            S["lump"], S["lumpMonth"] = lump, m
        if pp and m == round(pp["month"]) and B > 0 and pp["amount"] > 0:
            a = min(pp["amount"], B); share = a / B
            S["prepay"] = {"month": m, "amount": a, "before": B, "rate": r, "share": share, "endBefore": end}
            C -= C * share; B -= a
            if B < 0.005:
                B = 0.0
            if pp["mode"] == "shorten" and m > g and B > 0:
                if meth == "equal":
                    q = P - I
                    if q > 0:
                        end = min(end, m + math.ceil(B / q - 1e-9))
                elif meth not in ("bullet", "balloon"):
                    k = solve_n(B, rm, P)
                    if k != math.inf:
                        end = min(end, m + k)
            S["prepay"]["endAfter"] = end
        S["pay"].append(P); S["reg"].append(P - lump); S["bal"].append(B)
    return S


def mix(rows, sc):
    T = [track(t, sc) for t in rows]
    N = max(s["N"] for s in T)
    pay = [sum(s["pay"][i] for s in T if i < s["N"]) for i in range(N)]
    reg = [sum(s["reg"][i] for s in T if i < s["N"]) for i in range(N)]
    bal = [sum(s["bal"][i] for s in T if i < s["N"]) for i in range(N)]
    hi, hm = 0.0, 0
    for j in range(N):
        if reg[j] > hi + 1e-9:
            hi, hm = reg[j], j + 1
    pre = sum(s["prepay"]["amount"] for s in T if s["prepay"])
    loan = sum(t["amount"] for t in rows)
    totP = sum(s["sumP"] for s in T) + pre
    return {"first": pay[0], "highest": hi, "highestMonth": hm, "totalPaid": totP, "totalInterest": sum(s["sumI"] for s in T),
            "totalLinkage": sum(s["sumL"] for s in T), "perShekel": totP / loan if loan else 0, "bal60": bal[59] if N >= 60 else 0,
            "bal120": bal[119] if N >= 120 else 0, "pay": pay, "T": T, "lumps": [s["lump"] for s in T]}


def solve_loan(rows, shares, sc, target, basis):
    tot = sum(shares) or 1
    probe = mix([dict(t, amount=1e6 * shares[i] / tot, prepay=None) for i, t in enumerate(rows)], sc)
    per = probe["highest"] if basis == "max" else probe["first"]
    return target * 1e6 / per


def bucket(lst, years):
    for i, b in enumerate(lst):
        to = 1e9 if b["to"] is None else b["to"]
        if years <= to and (i == 0 or years > b["from"]):
            return b
    return lst[-1]


def pv(stream, annual):
    q = 1 + annual / 1200
    return sum(x / q ** (i + 1) for i, x in enumerate(stream))


def stream(B, annual, n_left, h, method):
    rm, out, b = annual / 1200, [], B
    for i in range(1, h + 1):
        n = n_left - i + 1; I = b * rm
        if method == "equal":
            P = I + b / n
        elif method == "bullet":
            P = I + b if n == 1 else I
        elif method == "balloon":
            P = b + I if n == 1 else 0.0
        else:
            P = pmt(b, rm, n)
        b = b + I - P
        if i == h and b > 0.005:
            P += b
        out.append(P)
    return out


def cap_fee(t, P, drop):
    if t.get("directed") or t["kind"] == "prime":
        return 0.0
    left = P["endBefore"] - P["month"]; h = left
    if t["kind"] == "var5":
        nxt = 60 * math.ceil(P["month"] / 60) + 1
        h = min(left, nxt - 1 - P["month"])
        if h <= 0:
            return 0.0
    if left <= 0:
        return 0.0
    b = bucket(D["term"]["cpi" if t.get("linked") else "nl"]["buckets"], h / 12)
    Cr = b["nom"]; Ar = Cr - drop; R = P["rate"]
    s = stream(P["before"], R, left, h, t.get("method", "spitzer"))
    pvA, pvC = pv(s, Ar), pv(s, Cr)
    f3 = max(0.0, pvA - P["before"]) if Ar < R else 0.0
    f4 = max(0.0, pvA - pvC) if Cr < R else None
    cap = f3 if f4 is None else min(f3, f4)
    cut = 0.0
    for x in D["fees"]["reduce"]:
        if P["month"] / 12 >= x["after_years"]:
            cut = x["cut"]
    return cap * (1 - cut) * P["share"]


# ------------------------------------------------------------------------------------------------------------ cases
def row(**k):
    base = {"amount": 1e6, "rate": 4.62, "years": 25, "method": "spitzer", "grace": 0, "graceType": "partial", "kind": "fixed", "linked": False}
    base.update(k)
    return base


TR = D["tracks"]
FC, POL = D["forecast"], D["policy"]
y0, m0 = int(D["built"][:4]), int(D["built"][5:7])
RAMP = max(1, (2027 - y0) * 12 + (8 - m0))
OPEN = [row(amount=600000), row(amount=400000, rate=TR["prime"]["rate"], kind="prime"), row(amount=200000, rate=TR["var5_cpi"]["rate"], kind="var5", linked=True)]
CASES = [
    ("1 Spitzer 1M 25y 4.62%", [row()], {"cpi": 0}),
    ("2 equal principal 1M 25y 4.62%", [row(method="equal")], {"cpi": 0}),
    ("3 balloon 500k 10y 4.43%", [row(amount=500000, years=10, rate=4.43, method="balloon")], {"cpi": 0}),
    ("4 bullet 300k 5y 4.62%", [row(amount=300000, years=5, method="bullet")], {"cpi": 0}),
    ("5 partial grace 12m", [row(grace=12)], {"cpi": 0}),
    ("6 full grace 12m", [row(grace=12, graceType="full")], {"cpi": 0}),
    ("7 CPI-linked fixed 3.29%, CPI 2%", [row(rate=TR["fixed_cpi"]["rate"], linked=True)], {"cpi": 2}),
    ("8 prime 4.27%, +1.5% from month 13", [row(rate=TR["prime"]["rate"], kind="prime")], {"cpi": 0, "prime": "custom", "shock": 1.5, "shockMonth": 13}),
    ("9 prime, BoI forecast path", [row(rate=TR["prime"]["rate"], kind="prime")], {"cpi": 0, "prime": "boi", "rampTo": FC["rate_q3_2027"] - POL["rate"], "rampMonths": RAMP}),
    ("10 var5 CPI 3.19%, +2% at the resets, CPI 2%", [row(rate=TR["var5_cpi"]["rate"], kind="var5", linked=True)], {"cpi": 2, "prime": "up2"}),
    ("11 opening mix, CPI 2%", OPEN, {"cpi": 2}),
    ("12 old +2% check on every track", OPEN, {"cpi": 2, "all": 2}),
    ("13 prepay 100k month 60, shorten", [row(prepay={"month": 60, "amount": 100000, "mode": "shorten"})], {"cpi": 0}),
    ("14 prepay 100k month 60, reduce", [row(prepay={"month": 60, "amount": 100000, "mode": "reduce"})], {"cpi": 0}),
    ("15 equal principal prepay shorten, CPI-linked", [row(method="equal", rate=3.29, linked=True, prepay={"month": 36, "amount": 50000, "mode": "shorten"})], {"cpi": 2}),
]
KEYS = ["first", "highest", "highestMonth", "totalPaid", "totalInterest", "totalLinkage", "bal60", "bal120"]

NODE = r"""
const fs=require('fs'),vm=require('vm');const [file,casesFile]=process.argv.slice(2);const w={};
vm.runInNewContext(fs.readFileSync(file,'utf8'),{window:w,Math,Intl,JSON,console});const M=w.NLMG;
const C=JSON.parse(fs.readFileSync(casesFile,'utf8'));const out={};
for(const c of C.cases){const sc=M.scenario(c.sc);const R=M.mix(c.rows,sc);
 const o={first:R.first,highest:R.highest,highestMonth:R.highestMonth,totalPaid:R.totalPaid,totalInterest:R.totalInterest,totalLinkage:R.totalLinkage,bal60:R.bal60,bal120:R.bal120,
 pay13:R.pay[12]||0,last:R.pay[R.N-1]||0,lump:(R.lumps[0]||{}).amount||0};
 const P=R.T[0].prepay; if(P){o.endAfter=P.endAfter; o.fee0=M.prepayFee(c.rows[0],P,C.data,0).cap; o.fee1=M.prepayFee(c.rows[0],P,C.data,1).cap;}
 out[c.name]=o;}
out.solve=M.solveLoan(C.solve.rows,C.solve.shares,M.scenario(C.solve.sc),C.solve.target,'first');
out.solveMax=M.solveLoan(C.solve.rows,C.solve.shares,M.scenario(C.solve.sc),C.solve.target,'max');
process.stdout.write(JSON.stringify(out));
"""


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    solve = {"rows": [dict(r, amount=0) for r in OPEN], "shares": [50, 100 / 3, 50 / 3], "sc": {"cpi": 2}, "target": 6000}
    tmp = tempfile.mkdtemp(prefix="nlmg-")
    cf = os.path.join(tmp, "cases.json"); jf = os.path.join(tmp, "run.js")
    json.dump({"cases": [{"name": n, "rows": r, "sc": s} for n, r, s in CASES], "solve": solve, "data": D}, open(cf, "w", encoding="utf-8"))
    open(jf, "w", encoding="utf-8").write(NODE)
    pr = subprocess.run(["node", jf, os.path.join(A, "tools", "mortgage.js"), cf], capture_output=True, text=True, encoding="utf-8")
    if pr.returncode:
        sys.exit("node failed: " + pr.stderr)
    js = json.loads(pr.stdout)
    bad = 0

    def cmp(name, key, py, j, tol=0.5):
        nonlocal bad
        ok = abs(py - j) < tol
        bad += 0 if ok else 1
        return ("OK " if ok else "BAD") + f" {key}: py {py:,.2f} | js {j:,.2f}"

    for name, rows, s in CASES:
        R = mix(rows, scenario(s)); o = js[name]
        print("== " + name)
        for k in KEYS:
            print("   " + cmp(name, k, R[k], o[k], 0.5 if k != "highestMonth" else 0.01))
        print("   " + cmp(name, "payment month 13", R["pay"][12], o["pay13"]))
        print("   " + cmp(name, "last payment", R["pay"][-1], o["last"]))
        if R["lumps"][0]:
            print("   " + cmp(name, "end payment (balloon or bullet)", R["lumps"][0], o["lump"]))
        P = R["T"][0]["prepay"]
        if P:
            print("   " + cmp(name, "new end month", P["endAfter"], o["endAfter"], 0.01))
            print("   " + cmp(name, "capitalization fee, averages unchanged", cap_fee(rows[0], P, 0), o["fee0"]))
            print("   " + cmp(name, "capitalization fee, averages 1 point lower", cap_fee(rows[0], P, 1), o["fee1"]))
    sv = solve_loan(solve["rows"], solve["shares"], scenario(solve["sc"]), solve["target"], "first")
    svm = solve_loan(solve["rows"], solve["shares"], scenario(solve["sc"]), solve["target"], "max")
    print("== 16 payment 6,000 -> loan (opening shares, CPI 2%)")
    print("   " + cmp("solve", "loan by the first payment", sv, js["solve"]))
    print("   " + cmp("solve", "loan by the highest payment", svm, js["solveMax"]))
    chk = mix([dict(r, amount=sv * sh / 100) for r, sh in zip(solve["rows"], solve["shares"])], scenario(solve["sc"]))["first"]
    print("   " + cmp("solve", "first payment of the solved loan = 6,000", chk, 6000, 0.01))

    print("== hand values (dna.md 8.4)")
    hand = []
    r1 = mix([row()], scenario({"cpi": 0})); r2 = mix([row(method="equal")], scenario({"cpi": 0}))
    hand += [("T8 Spitzer first payment", round(r1["first"]), 5627), ("T8 Spitzer total interest", round(r1["totalInterest"]), 687997),
             ("T8 equal principal first", round(r2["first"]), 7183), ("T8 equal principal last", round(r2["pay"][-1]), 3346), ("T8 equal principal interest", round(r2["totalInterest"]), 579425),
             ("T6 4.5% 25y", round(pmt(1e6, 4.5 / 1200, 300)), 5558), ("T6 5% 25y", round(pmt(1e6, 5 / 1200, 300)), 5846)]
    want = {20: (6391, 6079, 6297), 25: (5627, 5299, 5528), 30: (5138, 4796, 5035)}
    for y, w in want.items():
        for k, (mx, ww) in enumerate(zip(([("fixed_nl", 1)], [("fixed_nl", 1 / 3), ("prime", 1 / 3), ("var5_cpi", 1 / 3)], [("fixed_nl", .5), ("prime", .5)]), w)):
            got = mix([row(amount=1e6 * sh, rate=TR[t]["rate"], years=y, kind=TR[t]["kind"], linked=False) for t, sh in mx], scenario({"cpi": 0}))["first"]
            hand.append((f"T5 basket {k + 1} {y}y (CPI part before indexation)", round(got), ww))
    hand.append(("prime track opening rate = 4.35% effective as nominal", round(D["tracks"]["prime"]["rate"], 2), 4.27))
    for name, got, want_ in hand:
        ok = got == want_
        bad += 0 if ok else 1
        print(("   OK  " if ok else "   BAD ") + f"{name}: {got:,} (want {want_:,})")
    print("\nALL MATCH" if not bad else f"\n{bad} MISMATCH(ES)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
