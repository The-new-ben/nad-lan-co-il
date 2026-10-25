# -*- coding: utf-8 -*-
"""U2 on /investment/ (page 421), the full build after release 1.72.523 (the yield and cash-flow map, tool "invest").
Spec: dna.md section 6 (verified facts), 7 (gaps) and 8 (build spec). Additive law: no existing section loses its text; the only
edits inside existing text are the banned word "סימולציה" in one FAQ answer and the "עודכן" date (footer + Article dateModified).
What it adds, every number computed here from plugins/nadlan-config/assets/instruments/data/invest.json and cross-checked against
tools/instruments/test_invest_math.py, or taken from the dated facts of dna.md section 6:
  1. right under the H1: the answer paragraph, the CTA row (tool anchor, WhatsApp, lawyer), the tool [nadlan_tool id="invest"]
     (mounted outside the .nadlan-guide wrapper so the guide's p/table/th rules do not restyle it), then "השקעות נדל״ן ב־2026" + T1;
  2. before the first old H2: yield by city and rooms (V1 + T2, 65 cities, plus the two rent sources T2b), "כמה מהדירה שכר הדירה
     קונה" (V2 + T3: break-even share, rent minus payment, equity, purchase tax in months of rent), "כמה כסף צריך באמת" (V3 + T4),
     "נדל״ן או שוק ההון" (T5);
  3. inside old sections: purchase tax in shekels (T6), betterment by period (T7), the three rental-tax tracks (T8), what the
     table says by region; before the FAQ: investors today (MoF) and five first steps;
  4. 21 new FAQ (h3 + p) at the end of the old FAQ section: 9 old + 21 = 30, none repeating an old question;
  5. a method-and-sources line with "עודכן 26.10.2026" after the old sources list.
Each anchor must match exactly once. Language law asserted on the visible text (incl. SVG text and aria labels); every internal
link must answer 200 without a redirect. --dry: GET only, writes preview/u2-page-content.html (the raw content),
preview/u2-page-render.html (local render shell) and page-sources.md (the internal source list), then exits.
Without --dry: backup, POST, read-back, live check.
  python docs/research/2026-10-26-upgrades/u2-investment/write_u2_page.py [--dry]"""
import io, json, os, re, statistics, sys, time, urllib.error, urllib.parse, urllib.request

H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
DRY = "--dry" in sys.argv
PID = 421; SITE = "https://nad-lan.co.il"; WA = "972525101555"; UPDATED = "26.10.2026"; UPDATED_ISO = "2026-10-26"

# ------------------------------------------------------------------ data (invest.json) and the formulas of dna.md section 6
D = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "invest.json"), encoding="utf-8"))
L = D["rules"]; RATE = next(r["rate"] for r in L["rates"] if r["id"] == "fixed"); N = 300
VAT = L["vat"]; LAW = L["lawyer"]; LTV = L["ltv"]["extra"]; RT = L["rentTax"]; IDX = L["idx"]; BOI = L["boi"]; PT = L["ptax"]
CQ = D["cityQ"]
MON = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]
QM = {"03": "ינואר עד מרץ", "06": "אפריל עד יוני", "09": "יולי עד ספטמבר", "12": "אוקטובר עד דצמבר"}


def qlab(q): y, m = q.split("-"); return QM[m] + " " + y
def mlab(m): y, mm = m.split("-"); return MON[int(mm) - 1] + " " + y
def dmy(s): y, m, d = s.split("-"); return "%d.%d.%s" % (int(d), int(m), y)
def num(n): return "{:,}".format(int(round(n)))
def ils(n): return num(n) + " ₪"
def pct(x, d=2): return ("%." + str(d) + "f%%") % (100 * x)
def pmt(P): r = RATE / 1200; return P * r / (1 - (1 + r) ** -N)


AF = (1 - (1 + RATE / 1200) ** -N) / (RATE / 1200)


def ptax(price, br):
    t = 0; lo = 0
    for hi, rate in br:
        hi = float("inf") if hi is None else hi; top = min(price, hi)
        if top > lo: t += (top - lo) * rate
        if price <= hi: break
        lo = hi
    return t


def calc(price, rent):
    loan = price * LTV; pay = pmt(loan); tax = ptax(price, PT["extra"]); law = price * LAW / 100 * (1 + VAT)
    return {"price": price, "rent": rent, "gross": rent * 12 / price, "loan": loan, "pay": pay, "cf": rent - pay, "be": rent * AF / price,
            "tax": tax, "law": law, "equity": price - loan + tax + law, "months": tax / rent}


ROWS = {r["n"]: r for r in D["rows"]}
NAT4 = ROWS["ישראל"]["r"]["4"]; XN = calc(NAT4["price"], NAT4["rent"])
CITY = []
for r in D["rows"]:
    if r.get("nat") or "4" not in r["r"] or r["r"]["4"]["q"] != CQ: continue
    p = r["r"]["4"]; x = calc(p["price"], p["rent"]); x.update(n=r["n"], row=r, thin=p["n8"] <= 4, inv=r.get("inv", "")); CITY.append(x)
BY_G = sorted(CITY, key=lambda c: -c["gross"])
BY_BE = sorted(CITY, key=lambda c: -c["be"])
MED = statistics.median(c["gross"] for c in CITY)
POS = [c for c in CITY if c["cf"] > 0]
OUT = [r for r in D["rows"] if not r.get("nat") and not ("4" in r["r"] and r["r"]["4"]["q"] == CQ)]
N54 = sum(1 for c in CITY if 0.023 <= c["gross"] <= 0.036)
DEN = LTV + PT["extra"][0][1] + LAW / 100 * (1 + VAT)  # own money per shekel of price below the 8% band top
MAXP = {e: e / DEN for e in (200000, 400000)}
FITS400 = [(r["n"], k, r["r"][k]) for r in D["rows"] if not r.get("nat") for k in ("3", "4") if k in r["r"] and r["r"][k]["q"] == CQ and r["r"][k]["price"] <= MAXP[400000]]
FULL = [c for c in BY_G if not c["thin"]]  # cities whose median was published in most of the last 8 quarters


def C(name): return next(c for c in CITY if c["n"] == name)


TA, JLM, HFA, BS, ASK = C("תל אביב-יפו"), C("ירושלים"), C("חיפה"), C("באר שבע"), C("אשקלון")

# cross-check: the figures of test_invest_math.py / dna.md section 6 (the script stops if the data or the formulas drift)
def same(name, got, want): assert got == want, ("cross-check", name, got, want)
same("rate", RATE, 4.62); same("annuity factor", round(AF, 2), 177.73); same("per 100,000", round(pmt(100000)), 563)
for x, q, g, pay, cf, be, eq in ((XN, None, 2.85, 5708, -883, 42.3, 1188674), (TA, None, 2.29, 14713, -4713, 34.0, 3064140), (JLM, None, 3.00, 8109, -909, 44.4, 1688798),
                                 (HFA, None, 3.31, 4494, -94, 49.0, 935975), (BS, None, 3.59, 3385, 215, 53.2, 704955), (ASK, None, 3.76, 3955, 445, 55.6, 823658)):
    same("gross", round(100 * x["gross"], 2), g); same("pay", round(x["pay"]), pay); same("cf", round(x["cf"]), cf); same("be", round(100 * x["be"], 1), be); same("equity", round(x["equity"]), eq)
same("national purchase tax", round(XN["tax"]), 162304); same("months of rent", round(XN["months"]), 34)
same("cities", len(CITY), 65); same("median", round(100 * MED, 1), 3.0); same("2.3 to 3.6", N54, 54); same("rent covers", len(POS), 13)
same("above 50%", sum(1 for c in CITY if c["be"] > 0.5), 13); same("400k", round(MAXP[400000], -3), 683000)
same("lowest", (BY_G[-1]["n"], round(100 * BY_G[-1]["gross"], 2)), ("גבעתיים", 2.16)); same("highest", (BY_G[0]["n"], round(100 * BY_G[0]["gross"], 2)), ("נצרת", 5.36))
assert all(c["thin"] for c in CITY if c["gross"] > 0.04), "every city above 4% must be a small-sample city (the answer paragraph says so)"
assert not [f for f in FITS400 if f[1] == "4"], "no 4-room median fits 400,000 (FAQ says so)"
same("single-home tax, national", round(ptax(NAT4["price"], PT["single"])), 1752)

# ------------------------------------------------------------------ SVG (NadLan Instruments: ledger ink, sea, deep, green; survey red only for money that is missing)
FONT = "font-family:'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif"
MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"
INK, INK2, SEA, DEEP, GREEN, RED, LINE = "#12202A", "#3E4C58", "#2F6F86", "#1F4B5C", "#00806A", "#C42550", "#D3DCE2"


def tx(x, y, s, anchor="start", size=13, weight=400, fill=INK, mono=False, halo=False):
    """direction is rtl on the svg: anchor start = the right end of the text sits at x."""
    assert size >= 12, "svg text below 12px"
    st = "%s;font-size:%spx;font-weight:%s" % (MONO if mono else FONT, size, weight)
    if halo: st += ";paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-linejoin:round"
    return '<text x="%.1f" y="%.1f" text-anchor="%s" style="%s" fill="%s">%s</text>' % (x, y, anchor, st, fill, s)


def svg_open(h, label):
    return '<svg viewBox="0 0 420 %d" direction="rtl" role="img" aria-label="%s" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">' % (h, label)


def svg_yield():
    """V1: gross yield, 4 rooms, the 12 highest and the 5 lowest of the 65 cities, the 65-city median as a reference line."""
    top, bot = BY_G[:12], BY_G[-5:]
    W, xr, x1, xmin, gmax = 420, 408, 290, 60, 0.056
    sc = (x1 - xmin) / gmax; H0, rh = 98, 22; rows = top + [None] + bot
    yend = H0 + len(rows) * rh; hgt = yend + 86
    g = [svg_open(hgt, "תשואה ברוטו על דירת 4 חדרים ב־%d ערים, %s: הגבוהה %s ב%s, הנמוכה %s ב%s, החציון %s (החישוב שלנו)" % (
        len(CITY), qlab(CQ), pct(BY_G[0]["gross"]), BY_G[0]["n"], pct(BY_G[-1]["gross"]), BY_G[-1]["n"], pct(MED, 1)))]
    g.append(tx(xr, 24, "תשואה ברוטו על דירת 4 חדרים", size=16, weight=600))
    g.append(tx(xr, 46, "%d ערים, %s: 12 הגבוהות ו־5 הנמוכות" % (len(CITY), qlab(CQ)), size=13, fill=INK2))
    g.append(tx(xr, 66, "החישוב שלנו, לפי החציונים של אתר הנדל״ן הממשלתי", size=13, fill=INK2))
    xm = x1 - sc * MED
    g.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.2" stroke-dasharray="4 3"/>' % (xm, H0 - 4, xm, yend + 2, INK))
    y = H0
    for c in rows:
        if c is None:
            g.append(tx(xr, y + 15, "ועוד %d ערים בטבלה שמתחת" % (len(CITY) - 17), size=13, fill=INK2)); y += rh; continue
        w = sc * c["gross"]; col = GREEN if c["cf"] > 0 else SEA
        g.append(tx(xr, y + 15, c["n"] + (" ◦" if c["thin"] else ""), size=13.5, weight=500))
        g.append('<rect x="%.1f" y="%d" width="%.1f" height="15" fill="%s"%s/>' % (x1 - w, y + 3, w, col, ' fill-opacity=".5"' if c["thin"] else ""))
        g.append(tx(x1 - w - 5, y + 15, pct(c["gross"]), size=13, mono=True, halo=True))
        y += rh
    g.append(tx(xm, yend + 19, "חציון %d הערים: %s" % (len(CITY), pct(MED, 1)), anchor="middle", size=13, weight=600, halo=True))
    ly = yend + 46
    g.append('<rect x="%d" y="%d" width="11" height="11" fill="%s"/>' % (xr - 11, ly - 10, GREEN))
    g.append(tx(xr - 17, ly, "שכר הדירה מכסה משכנתא של 50%", size=13))
    g.append('<rect x="%d" y="%d" width="11" height="11" fill="%s"/>' % (178, ly - 10, SEA))
    g.append(tx(172, ly, "לא מכסה", size=13))
    g.append(tx(xr, ly + 22, "◦ מעט עסקאות: חציון שפורסם ב־4 מתוך 8 הרבעונים או פחות", size=13, fill=INK2))
    g.append('</svg>')
    return "".join(g)


def svg_breakeven():
    """V2: a dot histogram of the break-even share (rent as a 25-year mortgage at the BoI average, as a share of the price), 65 cities,
    against the 50% loan cap. The axis grows to the left, like every bar on the site (the start of a line in Hebrew is on the right)."""
    W, xr, lo, hi, xR, xL, base, bw = 420, 408, 0.30, 0.80, 396, 36, 268, 0.02
    k = (xR - xL) / (hi - lo); px = lambda v: xR - (v - lo) * k
    g = [svg_open(base + 166, "כמה מהדירה שכר הדירה קונה ב־%d ערים: %d ערים מעל 50%%, %d מתחת; תל אביב %s, ירושלים %s, חיפה %s, אשקלון %s (החישוב שלנו)" % (
        len(CITY), len(POS), len(CITY) - len(POS), pct(TA["be"], 1), pct(JLM["be"], 1), pct(HFA["be"], 1), pct(ASK["be"], 1)))]
    g.append(tx(xr, 24, "כמה מהדירה שכר הדירה קונה", size=16, weight=600))
    g.append(tx(xr, 46, "%d ערים, 4 חדרים, %s" % (len(CITY), qlab(CQ)), size=13, fill=INK2))
    g.append(tx(xr, 66, "שכר הדירה כהחזר משכנתא ל־25 שנה בריבית %s%% (החישוב שלנו)" % RATE, size=13, fill=INK2))
    for v in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
        x = px(v)
        g.append(tx(x, 90, "%d%%" % round(100 * v), anchor="middle", size=13, mono=True, fill=INK if v == 0.5 else INK2, weight=600 if v == 0.5 else 400))
        if v != 0.5: g.append('<line x1="%.1f" y1="97" x2="%.1f" y2="%d" stroke="%s" stroke-width="0.8"/>' % (x, x, base + 6, LINE))
    xc = px(0.5)
    g.append('<line x1="%.1f" y1="97" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.3" stroke-dasharray="4 3"/>' % (xc, xc, base + 6, INK))
    g.append(tx(xc - 6, 114, "תקרת המימון לדירה להשקעה", size=13, weight=600))
    bins = {}; at = {}
    for c in sorted(CITY, key=lambda c: c["be"]):
        i = max(0, min(int((c["be"] - lo) // bw), int(round((hi - lo) / bw)) - 1)); kk = bins.get(i, 0); bins[i] = kk + 1
        cx = px(lo + (i + 0.5) * bw); cy = base - 6 - kk * 12; col = GREEN if c["be"] > 0.5 else RED; at[c["n"]] = (cx, cy)
        mark = c["n"] in (TA["n"], JLM["n"], HFA["n"], ASK["n"])
        attr = (' fill-opacity=".4"' if c["thin"] else "") + (' stroke="%s" stroke-width="1.6"' % INK if mark else (' stroke="%s"' % col if c["thin"] else ""))
        g.append('<circle cx="%.1f" cy="%.1f" r="5.2" fill="%s"%s/>' % (cx, cy, col, attr))
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (xL, base + 6, xR, base + 6, INK))
    for c, row in ((TA, 0), (HFA, 0), (ASK, 0), (JLM, 1)):
        cx = at[c["n"]][0]; yl = base + 27 + row * 38
        g.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="0.8"/>' % (cx, base + 8, cx, yl - 13, INK))
        g.append(tx(cx, yl, c["n"].replace("-יפו", ""), anchor="middle", size=14, weight=600))
        g.append(tx(cx, yl + 15, pct(c["be"], 1), anchor="middle", size=13, mono=True))
    ly = base + 106
    g.append('<circle cx="%d" cy="%d" r="5.5" fill="%s"/>' % (xr - 6, ly - 5, GREEN))
    g.append(tx(xr - 17, ly, "מעל 50%%: שכר הדירה מכסה את ההחזר, %d ערים" % len(POS), size=13))
    g.append('<circle cx="%d" cy="%d" r="5.5" fill="%s"/>' % (xr - 6, ly + 17, RED))
    g.append(tx(xr - 17, ly + 22, "מתחת ל־50%%: משלמים כל חודש מהכיס, %d ערים" % (len(CITY) - len(POS)), size=13))
    g.append('<circle cx="%d" cy="%d" r="5.5" fill="%s" fill-opacity=".4" stroke="%s"/>' % (xr - 6, ly + 39, INK2, INK2))
    g.append(tx(xr - 17, ly + 44, "נקודה בהירה: מעט עסקאות בעיר", size=13, fill=INK2))
    g.append('</svg>')
    return "".join(g)


def svg_money():
    """V3: the national median 4-room flat bought as an additional home: where the money goes on the day, and every month."""
    W, xr, xl = 420, 408, 12
    price, tax, law, loan = NAT4["price"], XN["tax"], XN["law"], XN["loan"]; own = price - loan; tot = price + tax + law; s = (xr - xl) / tot
    HG = 452
    g = [svg_open(HG, "דירת 4 חדרים בחציון הארצי, %s: מהכיס %s ביום הקנייה, החזר %s בחודש מול שכר דירה %s (החישוב שלנו)" % (
        ils(price), ils(XN["equity"]), ils(XN["pay"]), ils(NAT4["rent"])))]
    g.append(tx(xr, 24, "לאן הולך הכסף בדירת 4 חדרים", size=16, weight=600))
    g.append(tx(xr, 46, "מחיר %s, החציון הארצי של %s" % (ils(price), qlab(NAT4["q"])), size=13, fill=INK2))
    g.append(tx(xr, 66, "דירה נוספת, משכנתא 50%% ל־25 שנה בריבית %s%% (החישוב שלנו)" % RATE, size=13, fill=INK2))
    g.append(tx(xr, 96, "ביום הקנייה", size=14, weight=600))
    y0, bh = 106, 30; x = xr; seg = []
    for name, v, col in (("own", own, DEEP), ("tax", tax, SEA), ("law", law, INK), ("loan", loan, LINE)):
        w = v * s; seg.append((name, x - w, w))
        g.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="%s"%s/>' % (x - w, y0, w, bh, col, ' stroke="%s" stroke-width="1"' % SEA if name == "loan" else ""))
        x -= w
    g.append(tx(xr - 8, y0 + 20, "מהכיס", size=13.5, weight=600, fill="#FFFFFF"))
    lx = seg[3][1] + seg[3][2] / 2
    g.append(tx(lx, y0 + 20, "מהבנק", anchor="middle", size=13.5, weight=600))
    led = [(DEEP, "חצי מהמחיר", own), (SEA, "מס רכישה, 8% מהשקל הראשון", tax), (INK, "עורך דין 0.5% ומע״מ", law), (LINE, "משכנתא, 50% מהמחיר", loan)]
    y = 166
    for col, lab, v in led:
        g.append('<rect x="%d" y="%d" width="11" height="11" fill="%s"%s/>' % (xr - 11, y - 10, col, ' stroke="%s"' % SEA if col == LINE else ""))
        g.append(tx(xr - 17, y, lab, size=13.5)); g.append(tx(xl, y, ils(v), anchor="end", size=13.5, mono=True)); y += 22
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (xl, y - 11, xr, y - 11, INK))
    g.append(tx(xr, y + 8, "מהכיס שלכם ביום הקנייה", size=14, weight=600, fill=DEEP))
    g.append(tx(xl, y + 8, ils(XN["equity"]), anchor="end", size=14, weight=600, mono=True, fill=DEEP))
    y += 48
    g.append(tx(xr, y, "ובכל חודש", size=14, weight=600))
    s2 = 330 / 6000.0; yb = y + 23
    for lab, v, col in (("שכר דירה חציוני", NAT4["rent"], GREEN), ("החזר המשכנתא", XN["pay"], DEEP)):
        w = v * s2
        g.append(tx(xr, yb, lab, size=13.5))
        g.append('<rect x="%.1f" y="%d" width="%.1f" height="16" fill="%s"/>' % (xr - w, yb + 6, w, col))
        g.append(tx(xr - w - 5, yb + 19, ils(v), size=13.5, mono=True)); yb += 44
    xa, xb = xr - NAT4["rent"] * s2, xr - XN["pay"] * s2; yy = yb - 8
    g.append('<path d="M%.1f %d V%d H%.1f V%d" fill="none" stroke="%s" stroke-width="1.4"/>' % (xa, yy - 6, yy, xb, yy - 6, RED))
    g.append(tx((xa + xb) / 2, yy + 19, "חסרים %s בחודש" % ils(-XN["cf"]), anchor="middle", size=14, weight=600, fill=RED))
    g.append(tx((xa + xb) / 2, yy + 36, "לפני הוצאות ומס", anchor="middle", size=13, fill=INK2))
    g.append('</svg>')
    assert yy + 42 <= HG, yy
    return "".join(g)


def fig(svg, cap):
    return '<figure class="nlu2-fig">%s<figcaption>%s</figcaption></figure>\n' % (svg, cap)


# ------------------------------------------------------------------ tables
TID = [0]


def table(caption, head, rows, minw=560, num=False):
    """The title sits above the scrolling box (a <caption> inside it scrolls away on phones); the table points to it."""
    TID[0] += 1; tid = "u2t%d" % TID[0]
    h = "".join('<th scope="col">%s</th>' % c for c in head)
    b = "".join('<tr><th scope="row">%s</th>%s</tr>' % (r[0], "".join("<td>%s</td>" % c for c in r[1:])) for r in rows)
    return ('<p class="nlu2-cap" id="%s">%s</p>\n<div class="nlu2-t"><table aria-labelledby="%s"%s style="min-width:%dpx"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>\n'
            % (tid, caption, tid, ' class="nlu2-num"' if num else "", minw, h, b))


def link(name, inv): return '<a href="%s">%s</a>' % (inv, name) if inv else name
def cfs(v): return '<span class="nlu2-pos">נשארים %s</span>' % ils(v) if round(v) > 0 else '<span class="nlu2-neg">חסרים %s</span>' % ils(-v)


def ycell(p, label_q=True):
    if not p: return "לא פורסם"
    s = pct(p["rent"] * 12 / p["price"]) + (" ◦" if p["n8"] <= 4 else "")
    if label_q and p["q"] != CQ: s += "<br><small>%s</small>" % qlab(p["q"])
    return s


NATR = ROWS["ישראל"]["r"]
T2_ROWS = [["ישראל<br><small>%s</small>" % qlab(NAT4["q"]), ils(NAT4["price"]), ils(NAT4["rent"]), ycell(NATR.get("3"), False), ycell(NAT4, False), ycell(NATR.get("5"), False), "לא מוצג"]]
for c in BY_G:
    r = c["row"]
    T2_ROWS.append([link(c["n"], c["inv"]), ils(c["price"]), ils(c["rent"]), ycell(r["r"].get("3")), ycell(r["r"]["4"]), ycell(r["r"].get("5")),
                    ("%.2f%%" % r["gy"]) if r.get("gy") is not None else "לא מוצג"])
T2 = table("תשואה ברוטו לפי עיר ומספר חדרים: %d ערים, %s (החישוב שלנו)" % (len(CITY), qlab(CQ)),
           ["עיר", "מחיר חציוני, 4 חדרים", "שכר דירה חציוני, 4 חדרים", "תשואה ברוטו, 3 חדרים", "4 חדרים", "5 חדרים", "התשואה באתר הממשלתי, כל החדרים"], T2_ROWS, 700, True)

CB = []
for r in [ROWS["ישראל"]] + [c["row"] for c in BY_G]:
    cb = (r.get("cbs") or {}).get("4"); p = r["r"]["4"]
    if not cb or (not r.get("nat") and (cb["q"] != CQ or p["q"] != CQ)): continue
    CB.append((r, p, cb, p["rent"] * 12 / p["price"], cb["avg"] * 12 / cb["price"]))
NCB = len(CB) - 1; NLOW = sum(1 for r, p, cb, a, b in CB[1:] if b < a)
T2B = table("שני מקורות לשכר הדירה: חציון אתר הנדל״ן מול ממוצע הלמ״ס, %s (החישוב שלנו)" % qlab(CQ),
            ["עיר", "שכר דירה חציוני, 4 חדרים", "שכר דירה ממוצע, 3.5 עד 4 חדרים", "תשואה לפי החציון", "תשואה לפי הממוצע"],
            [[(link(r["n"], r.get("inv", "")) if not r.get("nat") else "ישראל*"), ils(p["rent"]), "%s<br><small>טעות דגימה %s</small>" % (ils(cb["avg"]), ils(cb["err"])), pct(a), pct(b)]
             for r, p, cb, a, b in CB], 560, True)

T3 = table("כמה מהדירה שכר הדירה קונה, ומה נשאר בחודש: %d ערים, 4 חדרים, %s, משכנתא 50%% ל־25 שנה בריבית %s%% (החישוב שלנו)" % (len(CITY), qlab(CQ), RATE),
           ["עיר", "כמה מהדירה שכר הדירה קונה", "שכר דירה פחות החזר", "הון עצמי נדרש", "מס הרכישה בחודשי שכירות"],
           [[link(c["n"], c["inv"]) + (" ◦" if c["thin"] else ""), pct(c["be"], 1), cfs(c["cf"]), ils(c["equity"]), "%d חודשים" % round(c["months"])] for c in BY_BE], 600, True)

T4 = table("כמה כסף צריך: החציון הארצי וחמש ערים, 4 חדרים, דירה נוספת, משכנתא 50%% ל־25 שנה בריבית %s%% (החישוב שלנו)" % RATE,
           ["עיר", "מחיר חציוני", "מס רכישה", "עורך דין ומע״מ", "הון עצמי נדרש", "החזר חודשי", "שכר דירה חציוני", "מס הרכישה בחודשי שכירות"],
           [["ישראל<br><small>%s</small>" % qlab(NAT4["q"])] + [ils(XN[k]) for k in ("price", "tax", "law", "equity", "pay", "rent")] + ["%d חודשים" % round(XN["months"])]] +
           [[link(c["n"], c["inv"])] + [ils(c[k]) for k in ("price", "tax", "law", "equity", "pay", "rent")] + ["%d חודשים" % round(c["months"])] for c in (TA, JLM, HFA, BS, ASK)], 720, True)

PV = IDX["price"]; pm = PV["m"].split("-"); PWIN = "%s עד %s %s" % (MON[int(pm[1]) - 1], MON[int(pm[1])], pm[0]) if PV.get("window") == 2 else mlab(PV["m"])
T1 = table("המספרים של היום, %s" % UPDATED, ["נתון", "המספר", "מתי ולפי מי"], [
    ["מס רכישה על דירה נוספת", "8%% עד %s, 10%% מעל" % ils(PT["extra"][0][0]), "לרכישות עד %s, הודעת רשות המסים מ־12.10.2026" % dmy(PT["until"]["extra"])],
    ["מימון מרבי לדירה להשקעה", "%d%% משווי הדירה" % round(100 * LTV), "הוראה 329 של בנק ישראל"],
    ["ריבית בנק ישראל", "%s%%, פריים %s%%" % (BOI["rate"], BOI["prime"]), "מאז %s, נכון ל־%s" % (dmy(BOI["from"]), dmy(BOI["asof"]))],
    ["ריבית ממוצעת במשכנתא קבועה לא צמודה", "%s%%" % RATE, "בנק ישראל, %s. קבועה צמודה %s%%, משתנה צמודה %s%%" % (mlab(L["ratesPeriod"]), L["rates"][1]["rate"], L["rates"][2]["rate"])],
    ["פטור ממס על שכר דירה למגורים", "עד %s בחודש" % ils(RT["ceiling"]), "לשנת 2026. מעל התקרה הפטור קטן, והוא נעלם ב־%s" % ils(RT["zero"])],
    ["שכר הדירה", "עלה ב־%s%% בשנה" % IDX["rent"]["yoy"], "מדד שכר הדירה של הלמ״ס, %s" % mlab(IDX["rent"]["m"])],
    ["מחירי הדירות", "ירדו ב־%s%% בשנה" % abs(PV["yoy"]), "מדד מחירי הדירות של הלמ״ס, %s" % PWIN],
    ["משקיעים", "14% מהעסקאות: קנו 1,077 דירות ומכרו 1,171", "הכלכלן הראשי במשרד האוצר, אוגוסט 2026"]], 480)

T5 = table("דירה להשקעה מול שוק ההון: הכללים של היום", ["", "דירה להשקעה", "קרן או מניות בשוק ההון"], [
    ["מינוף", "משכנתא של עד 50% מהמחיר, לפי הוראה 329 של בנק ישראל", "קונים בכסף שלכם"],
    ["כמה כסף צריך כדי להתחיל", "חצי מהמחיר, ועוד מס רכישה ועורך דין: %s בדירת 4 חדרים בחציון הארצי (החישוב שלנו)" % ils(XN["equity"]), "כל סכום"],
    ["עלות הכניסה", "מס רכישה של 8%% מהשקל הראשון: %s בחציון הארצי, %d חודשי שכירות (החישוב שלנו)" % (ils(XN["tax"]), round(XN["months"])), "עמלות קנייה ודמי ניהול"],
    ["הכנסה שוטפת", "שכר דירה. תשואה ברוטו חציונית של %s ב־%d ערים, לפני הוצאות (החישוב שלנו)" % (pct(MED, 1), len(CITY)), "דיבידנד או ריבית, לפי מה שקונים"],
    ["מס על ההכנסה השוטפת", "פטור עד %s בחודש, או 10%%, או מס שולי" % ils(RT["ceiling"]), "לפי כללי המס על ניירות ערך"],
    ["מס על הרווח במכירה", "מס שבח של 25% על השבח הריאלי אצל יחיד", "מס רווחי הון"],
    ["נזילות", "מכירה דורשת קונה, עורך דין ודיווח לרשות המסים", "מוכרים בכל יום מסחר"],
    ["עבודה שוטפת", "שוכר, חוזה, תיקונים וביטוח", "בלי ניהול נכס"],
    ["פיזור", "דירה אחת בעיר אחת", "הרבה נכסים בקרן אחת, גם קרנות ומניות של חברות נדל״ן"]], 520)

T6R = []
for P in (1000000, 1500000, 2000000, 3000000, 6000000):
    e, si = ptax(P, PT["extra"]), ptax(P, PT["single"])
    T6R.append([ils(P), ils(e), ils(si) if round(si) > 0 else "אין מס", ils(e - si)])
T6 = table("מס רכישה לפי מחיר הדירה, לרכישות עד %s (החישוב שלנו)" % dmy(PT["until"]["extra"]), ["מחיר הדירה", "דירה נוספת", "דירה יחידה", "ההפרש"], T6R, 480, True)

T7 = table("מס שבח: שיעור המס על השבח הריאלי (לפי מדריך רשות המסים 2026)", ["החלק של השבח", "שיעור המס"], [
    ["אצל יחיד, על השבח עד 6.11.2001", "47%"], ["אצל יחיד, מ־7.11.2001 עד 31.12.2011", "20%"], ["אצל יחיד, מ־1.1.2012", "25%"],
    ["דירת מגורים מזכה שאינה פטורה, בחישוב הלינארי המוטב", "השבח עד 1.1.2014 פטור, ומשם 25%"], ["אצל חברה", "23%"], ["הסכום האינפלציוני", "10%, רק על התקופה עד 31.12.1993"]], 440)

T8R = []
for rent, lab in ((NAT4["rent"], "החציון הארצי, 4 חדרים"), (RT["ceiling"], "תקרת הפטור"), (8000, ""), (TA["rent"], "החציון בתל אביב, 4 חדרים"), (RT["zero"], "כאן הפטור נעלם")):
    ex = rent if rent <= RT["ceiling"] else max(0, 2 * RT["ceiling"] - rent)
    T8R.append([ils(rent) + ("<br><small>%s</small>" % lab if lab else ""), ils(ex) if round(ex) > 0 else "אין פטור", ils(rent - ex) if round(rent - ex) > 0 else "אין מס",
                ils(RT["ten"] * rent), ils(12 * RT["ten"] * rent)])
T8 = table("מס על שכר דירה למגורים בחודש, בפטור ובמסלול 10% (החישוב שלנו)", ["שכר דירה בחודש", "פטור: החלק הפטור", "פטור: החלק שחייב במס שולי", "מסלול 10%: בחודש", "מסלול 10%: בשנה"], T8R, 560, True)

# ------------------------------------------------------------------ the new copy
WATXT = urllib.parse.quote("שלום, הגעתי מהמדריך נדל״ן להשקעה ואשמח לפרטים נוספים")
CSS = ('<style id="nlu2-css">.nlu2-t{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 0 10px}'
       '.nadlan-guide .nlu2-t table{font-variant-numeric:tabular-nums;overflow:visible}'
       '.nadlan-guide .nlu2-t th,.nadlan-guide .nlu2-t td{padding:8px 10px;font-size:15px;line-height:1.5;vertical-align:top}'
       '.nadlan-guide .nlu2-num td,.nadlan-guide .nlu2-num th[scope=row]{white-space:nowrap}'
       '.nadlan-guide .nlu2-t .nlu2-num td,.nadlan-guide .nlu2-t .nlu2-num th{font-size:14px;padding:8px}'
       '.nadlan-guide .nlu2-num td small{display:block;white-space:normal}'
       '.nadlan-guide .nlu2-t th[scope=row],.nadlan-guide .nlu2-t thead th:first-child{position:sticky;right:0;z-index:1}'
       '.nadlan-guide .nlu2-t td small,.nadlan-guide .nlu2-t th small{font-size:12.5px;color:#3E4C58;font-weight:400}'
       '.nadlan-guide .nlu2-cap{font-weight:700;color:#12202A;font-size:15px;line-height:1.5;margin:22px 0 8px}'
       '.nlu2-pos{color:#00806A;font-weight:700;white-space:nowrap}.nlu2-neg{color:#C42550;font-weight:700;white-space:nowrap}'
       '.nlu2-fig{margin:22px 0}.nlu2-fig figcaption{font-size:14px;color:#3E4C58;margin-top:6px;line-height:1.6}'
       '.nadlan-guide .nlu2-note,.nadlan-guide .nlu2-src{font-size:15px;line-height:1.7;color:#3E4C58}'
       '.nlu2-more{margin:16px 0}.nlu2-more>summary{cursor:pointer;font-weight:700;font-size:16px;line-height:1.5;color:#1F4B5C;padding:10px 0}'
       '#invest-map{scroll-margin-top:96px;margin-top:28px;margin-bottom:28px}'
       '@media(max-width:600px){.nadlan-guide .nlu2-t th,.nadlan-guide .nlu2-t td{font-size:14px;padding:7px 8px}'
       '.nlu2-fig svg{margin-left:calc(50% - 50vw + 6px);margin-right:calc(50% - 50vw + 6px);width:calc(100vw - 12px)!important;max-width:none!important}}</style>\n')

TOP = (CSS +
       '<p dir="rtl"><strong>נדל״ן להשקעה בישראל מכניס היום תשואה ברוטו של כ־%s בשנה על דירת 4 חדרים בחציון הארצי</strong>, כ־%s בתל אביב, ויותר מ־4%% רק בכמה ערי פריפריה שבהן נרשמו מעט עסקאות (החישוב שלנו, לפי החציונים של אתר הנדל״ן הממשלתי). משקיע מקבל משכנתא של עד 50%% ומשלם מס רכישה של 8%% מהשקל הראשון, ולכן ברוב הערים שכר הדירה לא מכסה את ההחזר החודשי: הוא מכסה אותו רק ב־%d מתוך %d ערים.</p>\n'
       % (pct(XN["gross"], 1), pct(TA["gross"], 1), len(POS), len(CITY)) +
       '<div class="cta"><a class="btn" href="#invest-map">לבדיקת התשואה בעיר שלכם</a><a class="btn secondary" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">לקבלת פרטים נוספים בוואטסאפ</a><a class="btn secondary" href="/real-estate-lawyer/">פגישה עם עורך דין מקרקעין</a></div>\n' % (WA, WATXT) +
       '<p dir="rtl">בוחרים עיר ומספר חדרים, והמחשבון מראה את התשואה ברוטו, את ההחזר על משכנתא של 50%%, את ההון העצמי עם מס הרכישה ואת המס על שכר הדירה בשלושת המסלולים. יש לכם סכום מסוים? בחרו "יש לי הון עצמי" ותראו באילו ערים הוא מספיק לדירה.</p>\n'
       '</div></div>\n'
       '<div id="invest-map">\n[nadlan_tool id="invest"]\n</div>\n'
       '<div class="nadlan-guide"><div class="wrap">\n'
       '<h2 dir="rtl">השקעות נדל״ן ב־2026: מה המספרים אומרים</h2>\n'
       '<p dir="rtl">שכר הדירה עולה והמחירים יורדים: מדד שכר הדירה של הלמ״ס עלה ב־%s%% בשנה עד %s, ומדד מחירי הדירות ירד ב־%s%% בשנה. מנגד, משכנתא קבועה לא צמודה עולה בממוצע %s%%, המימון לדירה להשקעה מוגבל ל־50%%, ומס הרכישה על דירה נוספת הוא 8%% מהשקל הראשון. אלה המספרים שקובעים היום כל עסקה של נדל״ן להשקעה:</p>\n'
       % (IDX["rent"]["yoy"], mlab(IDX["rent"]["m"]), abs(PV["yoy"]), RATE) + T1)

OUTL = []
for r in OUT:
    p4 = r["r"].get("4")
    OUTL.append(link(r["n"], r.get("inv", "")) + (" (הנתון האחרון של 4 חדרים: %s)" % qlab(p4["q"]) if p4 else " (אין נתון של 4 חדרים)"))
TAG = ROWS["תל אביב-יפו"]

DATA = (
    '<h2 dir="rtl">תשואה לפי עיר ולפי מספר חדרים</h2>\n'
    '<p dir="rtl">תשואה ברוטו היא שכר הדירה השנתי חלקי מחיר הדירה. חישבנו אותה לכל עיר ולכל מספר חדרים, רק כשהמחיר החציוני ושכר הדירה החציוני פורסמו לאותו רבעון. ב־%d ערים יש נתון של 4 חדרים ל%s: החציון הוא %s, מ־%s ב%s ועד %s ב%s, שבה נרשמו מעט עסקאות. ב־%d ערים התשואה בין 2.3%% ל־3.6%% (החישוב שלנו).</p>\n'
    % (len(CITY), qlab(CQ), pct(MED, 1), pct(BY_G[-1]["gross"]), BY_G[-1]["n"], pct(BY_G[0]["gross"]), BY_G[0]["n"], N54) +
    fig(svg_yield(), "בירוק: הערים ששכר הדירה החציוני בהן מכסה משכנתא של 50%. כל הערים בטבלה.") + T2 +
    '<p class="nlu2-note" dir="rtl">◦ מעט עסקאות: החציון של מספר החדרים הזה פורסם רק ב־4 מתוך 8 הרבעונים האחרונים או פחות. מספר אחד לא מספר את כל העיר. כשהנתון שייך לרבעון מוקדם יותר, הרבעון כתוב מתחתיו. בכל הארץ המחיר ושכר הדירה הם של %s.</p>\n' % qlab(NAT4["q"]) +
    '<p dir="rtl">%d ערים נוספות בקובצי האתר הממשלתי לא פרסמו מחיר ושכר דירה של 4 חדרים ל%s, ולכן הן לא בדירוג: %s. במחשבון אפשר לבדוק אותן לפי מספר החדרים והרבעון האחרון שפורסמו.</p>\n' % (len(OUT), qlab(CQ), ", ".join(OUTL)) +
    '<h3 dir="rtl">שני מקורות לשכר הדירה</h3>\n'
    '<p dir="rtl">לצד החציון של אתר הנדל״ן הממשלתי, הלשכה המרכזית לסטטיסטיקה מפרסמת שכר דירה ממוצע בשוק החופשי, עם טעות דגימה. ב־%d מתוך %d הערים שבהן יש את שני הנתונים, התשואה לפי הממוצע נמוכה מהתשואה לפי החציון: בתל אביב %s מול %s. בארץ כולה הממוצע של הלמ״ס נותן %s (החישוב שלנו). שני המספרים רשמיים, ולכן כדאי להסתכל על שניהם.</p>\n'
    % (NLOW, NCB, pct(next(b for r, p, cb, a, b in CB if r["n"] == TA["n"])), pct(TA["gross"]), pct(CB[0][4])) + T2B +
    '<p class="nlu2-note" dir="rtl">* בארץ כולה החציון הוא של %s והממוצע של %s, כל אחד מול המחיר החציוני של אותו רבעון.</p>\n' % (qlab(NAT4["q"]), qlab(CB[0][2]["q"])) +
    '<h3 dir="rtl">התשואה שמופיעה באתר הנדל״ן הממשלתי</h3>\n'
    '<p dir="rtl">האתר מציג לכל עיר "תשואת שכירות חציונית שנתית", לכל החדרים יחד. בדקנו ב־%d ערים שזה שכר הדירה החציוני של השנה האחרונה כפול 12, חלקי המחיר החציוני השנתי. בתל אביב: %s כפול 12 חלקי %s, כלומר %.2f%%. בטבלה למעלה היא בעמודה האחרונה. החישוב שלנו לפי מספר חדרים ולפי אותו רבעון, ולכן הוא יכול לצאת שונה.</p>\n'
    % (D["checks"]["govYieldFormula"][0], ils(TAG["gyRent"]), ils(TAG["gyPrice"]), TAG["gy"]) +
    '<h2 dir="rtl">כמה מהדירה שכר הדירה קונה</h2>\n'
    '<p dir="rtl">מספר אחד לכל עיר מראה אם דירה להשקעה מחזיקה את עצמה: איזה חלק ממחיר הדירה שכר הדירה החציוני היה מממן, אם כולו היה הולך להחזר משכנתא ל־25 שנה בריבית %s%%. משקיע מקבל משכנתא של עד 50%%. מעל 50%%, שכר הדירה מכסה את כל ההחזר ונשאר עודף. מתחת ל־50%%, משלמים כל חודש מהכיס ובונים על עליית ערך. בארץ כולה %s, בתל אביב %s, בירושלים %s, בחיפה %s, בבאר שבע %s ובאשקלון %s (החישוב שלנו).</p>\n'
    % (RATE, pct(XN["be"], 1), pct(TA["be"], 1), pct(JLM["be"], 1), pct(HFA["be"], 1), pct(BS["be"], 1), pct(ASK["be"], 1)) +
    fig(svg_breakeven(), "%d ערים מעל קו ה־50%%, ו־%d מתחתיו. כל נקודה היא עיר." % (len(POS), len(CITY) - len(POS))) +
    '<p dir="rtl">ההחזר על כל 100,000 ₪ משכנתא הוא %s בחודש (החישוב שלנו). בטבלה: מה נשאר או חסר כל חודש אחרי ההחזר, לפני הוצאות ומס, כמה הון עצמי צריך עם מס הרכישה ועורך הדין, וכמה חודשי שכירות שווה מס הרכישה.</p>\n' % ils(pmt(100000)) +
    '<details class="nlu2-more"><summary>לטבלה המלאה: %d ערים, מהעיר ששכר הדירה בה קונה הכי הרבה מהדירה ועד הכי מעט</summary>\n' % len(CITY) + T3 +
    '<p class="nlu2-note" dir="rtl">◦ מעט עסקאות: החציון של 4 חדרים פורסם רק ב־4 מתוך 8 הרבעונים האחרונים או פחות.</p>\n</details>\n' +
    '<h2 dir="rtl">כמה כסף צריך באמת: הון עצמי, מס רכישה ומשכנתא של 50%%</h2>\n'
    '<p dir="rtl">בדירה להשקעה הבנק מממן עד חצי מהשווי, ומס הרכישה על דירה נוספת מתחיל ב־8%% מהשקל הראשון. לכן ההון העצמי גדול מחצי המחיר. בדירת 4 חדרים בחציון הארצי, במחיר של %s, יוצאים מהכיס %s ביום הקנייה, ואחר כך משלמים החזר של %s בחודש מול שכר דירה של %s (החישוב שלנו).</p>\n'
    % (ils(NAT4["price"]), ils(XN["equity"]), ils(XN["pay"]), ils(NAT4["rent"])) +
    fig(svg_money(), "הדירה נקנית כדירה נוספת. תיווך, שמאות, שיפוץ וריהוט לא בחישוב: מוסיפים אותם במחשבון.") + T4 +
    '<p dir="rtl">מס הרכישה לבדו שווה %d חודשי שכירות בחציון הארצי ו־%d בתל אביב. עוד על המימון במדריך <a href="/investment-property-mortgage/">משכנתא לדירה להשקעה</a>, ועל כל עלויות הקנייה ב<a href="/apartment-purchase-cost-calculator/">מחשבון עלות רכישה כוללת</a>.</p>\n'
    % (round(XN["months"]), round(TA["months"])) +
    '<h2 dir="rtl">נדל״ן או שוק ההון</h2>\n'
    '<p dir="rtl">לפני שבוחרים עיר, כדאי לבדוק אם נדל״ן מתאים לכסף שלכם. ההשוואה בנויה על הכללים שחלים היום, בלי הבטחת תשואה לאף צד: המינוף והפטור על שכר הדירה לטובת הדירה, הנזילות וסכום הכניסה לטובת שוק ההון. עוד על המינוף במדריך <a href="/investment/real-estate-leverage/">מינוף בנדל״ן</a>.</p>\n' + T5)

PTAX = ('<h3 dir="rtl">מס רכישה על דירה נוספת מול דירה יחידה, בשקלים</h3>\n' + T6 +
        '<p dir="rtl">על דירה יחידה המדרגות ב־2026 הן: אין מס עד %s, 3.5%% עד %s, 5%% עד %s, 8%% עד %s ו־10%% מעל, והן מוקפאות עד %s. מגישים הצהרה לרשות המסים תוך 30 יום מיום הרכישה, ומשלמים את המס לפי השומה העצמית תוך 60 יום מתאריך העסקה. החישוב המלא במדריך <a href="/real-estate-tax-advisor/purchase-tax-investor/">מס רכישה למשקיעים</a> וב<a href="/purchase-tax-calculator/">מחשבון מס רכישה</a>.</p>\n'
        % (ils(PT["single"][0][0]), ils(PT["single"][1][0]), ils(PT["single"][2][0]), ils(PT["single"][3][0]), dmy(PT["until"]["single"])))

BETTER = ('<h3 dir="rtl">שיעורי מס השבח לפי תקופה</h3>\n' + T7 +
          '<p dir="rtl">מהשבח מורידים, לפי מדריך רשות המסים, את מס הרכישה ששולם, את שכר הטרחה של עורך הדין, השמאי והמתווך, שיפורים בנכס וריבית ריאלית. לכן שומרים כל חשבונית מיום הקנייה. ההסבר המלא במדריך <a href="/real-estate-tax-advisor/capital-gains-tax-guide/">מס שבח</a>.</p>\n')

RENT = ('<h3 dir="rtl">שלושת המסלולים בשקלים</h3>\n'
        '<p dir="rtl">הפטור נבדק כל חודש, על כל שכר הדירה למגורים מכל הדירות יחד. עד %s בחודש אין מס. מעל זה הפטור קטן שקל מול שקל, והוא נעלם ב־%s. זו התקרה גם ב־2024 וב־2025, כי עדכון סכומי המס הוקפא לשנים 2025 עד 2027. במסלול 10%% משלמים 10%% מכל שכר הדירה, בלי הוצאות ובלי פחת, פעם בשנה, עד 30 יום מתום שנת המס: על 2026 עד 30.1.2027. אי אפשר לשלב אותו עם פטור חלקי על אותה דירה, ובמכירה חייבת במס בעתיד מוסיפים לחישוב מס השבח את הפחת שאפשר היה לדרוש. במס השולי מורידים הוצאות ופחת, ומשלמים לפי המדרגות: מ־%d%% עד גיל 60 ומ־%d%% מגיל 60.</p>\n'
        % (ils(RT["ceiling"]), ils(RT["zero"]), round(100 * RT["under60"]), round(100 * RT["over60"])) + T8 +
        '<p dir="rtl">במס השולי הסכום תלוי בהכנסות ובהוצאות שלכם, ולכן הוא לא בטבלה. במחשבון בעמוד שלושת המסלולים מופיעים זה לצד זה, לפי שכר הדירה בעיר שבחרתם.</p>\n')

def cg(name): c = C(name); return "%s %s" % (link(c["n"].replace("-יפו", ""), c["inv"]), pct(c["gross"]))
WHERE = ('<h3 dir="rtl">מה הנתונים אומרים על הדרום, הצפון והמרכז</h3>\n'
         '<p dir="rtl">בטבלת התשואות הפערים ברורים. בדרום: %s, %s ו%s. בצפון: %s, עכו %s וכרמיאל %s. בירושלים %s. במרכז ובשרון: %s, %s, %s ו%s. כל אלה על דירת 4 חדרים לפי החציונים של %s (החישוב שלנו). התשואות הגבוהות בטבלה הן בערים שבהן המחיר נמוך, ולכן בודקים גם כמה עסקאות נרשמו בעיר ובשכונה. איך בוחרים עיר ושכונה מוסבר במדריך <a href="/investment/where-to-buy-investment-apartment/">איפה כדאי לקנות דירה להשקעה</a>.</p>\n'
         % (cg("אשקלון"), cg("באר שבע"), cg("אשדוד"), cg("חיפה"), pct(C("עכו")["gross"]), pct(C("כרמיאל")["gross"]), pct(JLM["gross"]),
            cg("תל אביב-יפו"), cg("רמת גן"), cg("הרצליה"), cg("רעננה"), qlab(CQ)))

IL = L["invLoans"]
BEFORE_FAQ = (
    '<h2 dir="rtl">מי קונה היום: משקיעים בשוק הדירות</h2>\n'
    '<p dir="rtl">באוגוסט 2026 נרשמו 7,532 עסקאות דירות, כולל דירות בהנחה. משקיעים קנו 1,077 דירות, 14%% מכל העסקאות, ומכרו 1,171. מהדירות שקנו משקיעים, 46%% היו דירות חדשות, ובאזור חיפה קנו משקיעים רק 139 דירות, 9%% מהעסקאות באזור. מאוקטובר 2021, חודש לפני העלאת מס הרכישה על משקיעים, ועד יולי 2026 ירד מלאי הדירות של המשקיעים ב־8,707 דירות. הנתונים מסקירת הכלכלן הראשי במשרד האוצר.</p>\n'
    '<p dir="rtl">באותו חודש נתנו הבנקים %s משכנתאות לדירה להשקעה, בסך %.2f מיליארד ₪, כ־%.2f מיליון ₪ בממוצע להלוואה, לפי בנק ישראל. זה %d%% מכל המשכנתאות החדשות של החודש (החישוב שלנו).</p>\n'
    % (num(IL["n"]), IL["vol"] / 1e9, IL["vol"] / IL["n"] / 1e6, round(100 * IL["n"] / IL["allN"])) +
    '<h2 dir="rtl">נדל״ן למתחילים: חמשת הצעדים הראשונים</h2>\n'
    '<p dir="rtl">במחשבון יש מקרים מוכנים: "200 אלף ₪ הון עצמי" ו"400 אלף ₪ הון עצמי" מראים מיד באילו ערים הסכום מספיק לדירה.</p>\n'
    '<ol dir="rtl">'
    '<li><strong>מחשבים כמה כסף יש באמת.</strong> ההון העצמי צריך לכסות חצי מהמחיר, מס רכישה של 8%% ועורך דין. 200,000 ₪ מספיקים לדירה של עד כ־%d אלף ₪, ו־400,000 ₪ לדירה של עד כ־%d אלף ₪ (החישוב שלנו).</li>'
    '<li><strong>בודקים את ההחזר.</strong> כל 100,000 ₪ משכנתא ל־25 שנה בריבית %s%% עולים כ־%s בחודש, וההחזר לא יעלה על 50%% מההכנסה הפנויה.</li>'
    '<li><strong>בוחרים עיר לפי שכר הדירה, לא רק לפי המחיר.</strong> רק ב־%d מתוך %d ערים שכר הדירה החציוני מכסה משכנתא של 50%%. הטבלאות למעלה והמחשבון מראים את כולן.</li>'
    '<li><strong>בודקים את הדירה עצמה.</strong> מחיר מול עסקאות דומות ב<a href="/property-value-estimator/">מחשבון שווי דירה</a>, מצב הבניין, הרישום בטאבו והשוכר שכבר גר בה.</li>'
    '<li><strong>מחשבים את מס שכר הדירה ושומרים קבלות.</strong> בודקים את שלושת המסלולים לפני שחותמים על חוזה השכירות, ושומרים כל חשבונית למס השבח.</li>'
    '</ol>\n' % (MAXP[200000] // 1000, round(MAXP[400000] / 1000), RATE, ils(pmt(100000)), len(POS), len(CITY)))

F400 = [n for n, k, p in sorted(FITS400, key=lambda f: f[2]["price"], reverse=True)]
F400T = [n for n, k, p in sorted(FITS400, key=lambda f: f[2]["price"], reverse=True) if p["n8"] <= 4]
QA_NEW = [
    ("מה זה נדל״ן להשקעה?", "נכס שקונים כדי להשכיר אותו או למכור אותו ברווח, ולא כדי לגור בו. הרווח מגיע משני מקורות: שכר הדירה ועליית הערך. אצל בנק ישראל דירה להשקעה היא כל דירה שאינה דירה יחידה ואינה דירה חלופית, ועליה חלה תקרת מימון של 50%."),
    ("כמה תשואה נותנת דירה להשקעה בישראל?", "לפי החציונים הרשמיים של %s, ב־%d מתוך %d ערים התשואה ברוטו על דירת 4 חדרים היא בין 2.3%% ל־3.6%% בשנה, והחציון הוא %s (החישוב שלנו). בחציון הארצי של %s היא %s. זו תשואה לפני מס רכישה, הוצאות ומס על שכר הדירה."
     % (qlab(CQ), N54, len(CITY), pct(MED, 1), qlab(NAT4["q"]), pct(XN["gross"]))),
    ("איפה התשואה הכי גבוהה על דירה להשקעה?", "בין הערים שבהן החציון פורסם ברוב הרבעונים: %s על דירת 4 חדרים. בנצרת, בשדרות, בקריית שמונה ובדימונה החישוב יוצא מעל 4%%, אבל שם נרשמו מעט עסקאות. הנמוכות הן גבעתיים %s ותל אביב %s (החישוב שלנו)."
     % (", ".join("%s %s" % (c["n"], pct(c["gross"])) for c in FULL[:3]) + " ו%s %s" % (FULL[3]["n"], pct(FULL[3]["gross"])), pct(C("גבעתיים")["gross"]), pct(TA["gross"]))),
    ("איך מחשבים תשואה על דירה להשקעה?", "תשואה ברוטו: שכר הדירה השנתי חלקי מחיר הדירה. דירה של %s שמושכרת ב־%s בחודש נותנת %s (החישוב שלנו). תשואה נטו: שכר הדירה אחרי הוצאות, חודשים בלי שוכר ומס, חלקי העלות הכוללת עם מס הרכישה ועורך הדין. ההסבר המלא בעמוד <a href=\"/investment/real-estate-yield/\">תשואה על נדל״ן</a>."
     % (ils(NAT4["price"]), ils(NAT4["rent"]), pct(XN["gross"]))),
    ("כמה הון עצמי צריך לדירה להשקעה?", "לפחות חצי מהמחיר, ועוד מס רכישה ועורך דין. בדירת 4 חדרים בחציון הארצי (%s) זה %s: %s לחצי המחיר, %s מס רכישה ו־%s לעורך דין עם מע״מ (החישוב שלנו, בלי תיווך, שמאות ושיפוץ)."
     % (ils(NAT4["price"]), ils(XN["equity"]), ils(NAT4["price"] - XN["loan"]), ils(XN["tax"]), ils(XN["law"]))),
    ("כמה משכנתא אפשר לקבל על דירה להשקעה?", "עד 50% משווי הדירה, לפי הוראה 329 של בנק ישראל. על דירה יחידה התקרה היא 75% ועל דירה חלופית 70%. בכל המקרים ההחזר החודשי לא יעלה על 50% מההכנסה הפנויה."),
    ("האם שכר הדירה יכסה את המשכנתא?", "ברוב הערים לא. בריבית %s%% ל־25 שנה, כל 100,000 ₪ משכנתא עולים כ־%s בחודש. בחציון הארצי ההחזר על חצי מהמחיר הוא %s, מול שכר דירה של %s, כלומר חסרים %s בחודש. שכר הדירה החציוני מכסה את ההחזר רק ב־%d מתוך %d ערים (החישוב שלנו)."
     % (RATE, ils(pmt(100000)), ils(XN["pay"]), ils(NAT4["rent"]), ils(-XN["cf"]), len(POS), len(CITY))),
    ("עד מתי חל מס הרכישה של 8% על דירה נוספת?", "הוראת השעה הוארכה לרכישות עד %s כולל, לפי הודעת רשות המסים מ־12.10.2026. מה יחול אחרי התאריך הזה עוד לא פורסם." % dmy(PT["until"]["extra"])),
    ("האם משלמים מס על שכר דירה?", "על השכרת דירת מגורים בוחרים מסלול: פטור עד תקרה, 10% מכל שכר הדירה, או מס שולי עם ניכוי הוצאות ופחת. הבדיקה היא לפי כל שכר הדירה למגורים מכל הדירות יחד."),
    ("מה תקרת הפטור ממס על שכר דירה ב־2026?", "%s בחודש, אותו סכום כמו ב־2024 וב־2025, כי עדכון סכומי המס הוקפא לשנים 2025 עד 2027. הבדיקה חודשית, וכל שכר הדירה למגורים נספר יחד. מעל התקרה הפטור קטן שקל מול שקל, והוא נעלם ב־%s."
     % (ils(RT["ceiling"]), ils(RT["zero"]))),
    ("מה עדיף, מסלול 10% או פטור?", "עד %s בחודש הפטור משתלם, כי אין מס בכלל. מעל %s אין פטור, והבחירה היא בין 10%% מכל שכר הדירה בלי הוצאות לבין מס שולי על ההכנסה אחרי הוצאות ופחת. בין שני הסכומים מחשבים את שני המסלולים: במחשבון בעמוד שלושתם מופיעים זה לצד זה. אי אפשר לשלב פטור חלקי ומסלול 10%% על אותה דירה."
     % (ils(RT["ceiling"]), ils(RT["zero"]))),
    ("מתי משלמים את המס במסלול 10%?", "פעם בשנה, עד 30 יום מתום שנת המס. על שכר הדירה של 2026 משלמים עד 30.1.2027. במסלול הזה לא מנכים הוצאות ופחת, ובמכירה חייבת במס בעתיד מוסיפים לחישוב מס השבח את הפחת שאפשר היה לדרוש."),
    ("כמה מס שבח משלמים במכירת דירה להשקעה?", "יחיד משלם 25% על השבח הריאלי שנצבר מ־1.1.2012. בדירת מגורים מזכה שאינה פטורה, השבח הריאלי עד 1.1.2014 פטור בחישוב הלינארי המוטב, ועל השבח שאחריו משלמים 25%. חברה משלמת 23%."),
    ("מה מורידים מהשבח?", "לפי מדריך רשות המסים: מס רכישה ששולם, שכר טרחה של עורך דין, שמאי ומתווך, שיפורים בנכס וריבית ריאלית. לכן שומרים כל חשבונית מיום הקנייה."),
    ("נדל״ן או שוק ההון, מה עדיף?", "אין תשובה אחת. נדל״ן נותן מינוף של עד 50%% ופטור על שכר דירה עד %s בחודש, אבל דורש הון גדול, משלם מס רכישה של 8%% מהשקל הראשון ואינו נזיל. לשוק ההון נכנסים בכל סכום, מפזרים בקלות ומוכרים בכל יום מסחר. ההשוואה המלאה בטבלה בעמוד." % ils(RT["ceiling"])),
    ("מה אפשר לעשות עם 400 אלף שקל בנדל״ן?", "במשכנתא של 50%%, אחרי מס רכישה של דירה נוספת ועורך דין, 400,000 ₪ מספיקים לדירה של עד כ־%d אלף ₪ (החישוב שלנו). לפי החציונים של %s זה מתאים לדירת 3 חדרים ב%s, ולא לאף דירת 4 חדרים בחציון.%s במחשבון בחרו \"400 אלף ₪ הון עצמי\" ותראו את הרשימה לפי התזרים."
     % (round(MAXP[400000] / 1000), qlab(CQ), ", ב".join(F400[:-1]) + " וב" + F400[-1],
        (" ב%s נרשמו מעט עסקאות." % (", ב".join(F400T[:-1]) + " וב" + F400T[-1] if len(F400T) > 1 else F400T[0])) if F400T else "")),
    ("שכר הדירה עולה?", "כן. מדד שכר הדירה של הלמ״ס עלה ב־%s%% בשנה עד %s, ובאותה תקופה מדד המחירים לצרכן עלה ב־%s%%." % (IDX["rent"]["yoy"], mlab(IDX["rent"]["m"]), IDX["cpi"]["yoy"])),
    ("מחירי הדירות יורדים?", "לפי מדד מחירי הדירות של הלמ״ס, המחירים ירדו ב־%s%% בשנה (%s), ומחירי הדירות החדשות ירדו ב־%s%%." % (abs(PV["yoy"]), PWIN, abs(IDX["newp"]["yoy"]))),
    ("כמה משקיעים קונים היום?", "באוגוסט 2026 קנו משקיעים 1,077 דירות, 14% מכל העסקאות, ומכרו 1,171, לפי הכלכלן הראשי במשרד האוצר. מאוקטובר 2021 ועד יולי 2026 ירד מלאי הדירות של המשקיעים ב־8,707 דירות."),
    ("מה זה התשואה שמופיעה באתר הנדל״ן הממשלתי?", "האתר מציג לכל עיר \"תשואת שכירות חציונית שנתית\" לכל החדרים יחד. בדקנו ב־%d ערים: זה שכר הדירה החציוני כפול 12 חלקי המחיר החציוני השנתי שהאתר מציג. בתל אביב %.2f%%. אצלנו התשואה מחושבת לפי מספר חדרים ולפי אותו רבעון, ולכן היא יכולה לצאת שונה: בתל אביב %s על דירת 4 חדרים (החישוב שלנו)."
     % (D["checks"]["govYieldFormula"][0], TAG["gy"], pct(TA["gross"]))),
    ("השקעה בנדל״ן בחו״ל או בישראל?", "בחו״ל מחיר הכניסה יכול להיות נמוך יותר, אבל נוספים מס זר, מטבע, ניהול מרחוק ומשפט של מדינה אחרת. בישראל יש משכנתא של עד 50%%, פטור על שכר דירה עד %s בחודש ושוק שאפשר לבדוק בנתונים רשמיים, אבל מס הרכישה על דירה נוספת הוא 8%% מהשקל הראשון." % ils(RT["ceiling"])),
]
FAQ_NEW = "".join('<h3 dir="rtl">%s</h3>\n<p dir="rtl">%s</p>\n' % qa for qa in QA_NEW)

METHOD = (' <p class="nlu2-src" dir="rtl"><strong>שיטה ומקורות.</strong> המחירים ושכר הדירה הם החציונים של <a href="https://www.nadlan.gov.il/">אתר הנדל״ן הממשלתי</a> לפי עיר ומספר חדרים (קובצי %s: בערים %s, בארץ כולה %s), ושכר הדירה הממוצע הוא של <a href="https://www.cbs.gov.il/he/cbsnewbrand/Pages/default.aspx">הלשכה המרכזית לסטטיסטיקה</a> (לוח 4.9, %s). תשואה ברוטו היא שכר דירה חציוני כפול 12 חלקי המחיר החציוני של אותו רבעון ואותו מספר חדרים. ההחזר מחושב בלוח שפיצר ל־25 שנה על משכנתא של 50%%, בריבית הממוצעת של <a href="https://www.boi.org.il/">בנק ישראל</a> למשכנתא קבועה לא צמודה ב%s (%s%%). מס הרכישה לפי <a href="https://www.gov.il/he/pages/pa121026-2">הודעת רשות המסים מ־12.10.2026</a> ומדריך רשות המסים לרוכש 2026, והנתונים על משקיעים מסקירת הכלכלן הראשי במשרד האוצר לאוגוסט 2026. עיר שבה החציון פורסם ב־4 מתוך 8 הרבעונים האחרונים או פחות מסומנת "מעט עסקאות". כל מספר שחושב בעמוד מסומן "החישוב שלנו", ואינו הבטחת תשואה. עודכן %s.</p>'
          % (dmy(D["src"]["gov"]["fileDate"]), qlab(CQ), qlab(NAT4["q"]), qlab(CQ), mlab(L["ratesPeriod"]), RATE, UPDATED))

# ------------------------------------------------------------------ anchored replacements (each old string must appear exactly once in the live content)
FIRST = '<p dir="rtl">נדלן להשקעה בישראל הוא אחד האפיקים הפופולריים ביותר אצל משקיעים פרטיים'
R = [
    (FIRST, TOP + FIRST),
    ('<h2 dir="rtl">מהי השקעת נדלן ולמי היא מתאימה</h2>', DATA + '<h2 dir="rtl">מהי השקעת נדלן ולמי היא מתאימה</h2>'),
    ('<h2 dir="rtl">מס שבח במכירה</h2>', PTAX + '<h2 dir="rtl">מס שבח במכירה</h2>'),
    ('<h2 dir="rtl">מיסוי שכר דירה למגורים בישראל</h2>', BETTER + '<h2 dir="rtl">מיסוי שכר דירה למגורים בישראל</h2>'),
    ('<h2 dir="rtl">איפה כדאי להשקיע בישראל 2026 לפי נתוני עסקאות</h2>', RENT + '<h2 dir="rtl">איפה כדאי להשקיע בישראל 2026 לפי נתוני עסקאות</h2>'),
    ('<h2 dir="rtl">ניהול הנכס והשכרה</h2>', WHERE + '<h2 dir="rtl">ניהול הנכס והשכרה</h2>'),
    ('<h2 dir="rtl">שאלות נפוצות</h2>', BEFORE_FAQ + '<h2 dir="rtl">שאלות נפוצות</h2>'),
    ('<h2 dir="rtl">מקורות</h2>', FAQ_NEW + '<h2 dir="rtl">מקורות</h2>'),
    ('בודקים מול עסקאות ושכירויות בפועל.</li> </ul>', 'בודקים מול עסקאות ושכירויות בפועל.</li> </ul>' + METHOD),
    # the only edits inside existing text: a banned word, and the date
    ('לבצע סימולציה רשמית לפני חתימה', 'לחשב את המס במחשבון של רשות המסים לפני החתימה'),
    ('נכתב ונערך בידי צוות נדלן. עודכן 25.10.2026.', 'נכתב ונערך בידי צוות נדלן. עודכן %s.' % UPDATED),
    ('"dateModified": "2026-10-25"', '"dateModified": "%s"' % UPDATED_ISO),
]
NEWS = [n for o, n in R[:9]]  # the new copy (the old anchor text inside each is old text, kept)

# ------------------------------------------------------------------ the live content (GET), apply, gates
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "u2page"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,modified" % PID)
raw = r["content"]["raw"]; new = raw
for o, n in R:
    c = new.count(o)
    assert c == 1, ("anchor must match once", c, o[:80])
    new = new.replace(o, n)
print("[page %d] live content modified %s, %d chars; %d anchors matched once each" % (PID, r.get("modified"), len(raw), len(R)))


def visible(html):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S); h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    h = re.sub(r"\[nadlan_tool[^\]]*\]", " ", h)  # the shortcode prints the tool, it is not text
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)) + " " + " ".join(re.findall(r'aria-label="([^"]*)"', html))


NEWTXT = "".join(NEWS) + "".join(n for o, n in R[9:])
nv = visible(NEWTXT); pv = visible(new)
BANNED_NEW = r"ממשק|מערכת|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה|טעון אימות|נדל[״\"]?ן חכם|Nadlan|nadlan(?!\.gov)|מודל|מנגנון|שכבה|שכבות|הדגמה|טכנולוגי|יחסית|כמעט|אטלס|Atlas|פיילוט|פרוטוטייפ|רספונסיבי|מובייל|אפס "
BANNED_PAGE = r"ממשק|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה|טעון אימות|נדל[״\"]?ן חכם|Nadlan"
assert not re.search(r"[–—]", pv), "long dash on the page: " + str(re.findall(r".{20}[–—].{20}", pv)[:3])
hits = re.findall(r".{0,25}(?:%s).{0,25}" % BANNED_NEW, nv)
assert not hits, ("language law, new copy", hits[:5])
hits = re.findall(r".{0,25}(?:%s).{0,25}" % BANNED_PAGE, pv)
assert not hits, ("language law, whole page", hits[:5])
assert not re.search(r"(?<![\d.,])0 (₪|חדרים|חודשים|ערים)", nv), "a zero number on visible text"
assert "<h1" not in NEWTXT and new.count("<h1") == 1, "exactly one h1"
for sv in re.findall(r"<svg\b.*?</svg>", NEWTXT, flags=re.S):
    assert min(float(x) for x in re.findall(r"font-size:([\d.]+)px", sv)) >= 12 and 'viewBox="0 0 420 ' in sv and 'direction="rtl"' in sv
# every number in the new copy is either computed above or a dated fact: the computed ones carry the label
OFFICIAL = {"%s%%" % RATE, "%s%%" % L["rates"][1]["rate"], "%s%%" % L["rates"][2]["rate"], "%s%%" % BOI["rate"], "%s%%" % BOI["prime"], "%.2f%%" % TAG["gy"]}
for p in re.findall(r"<p\b[^>]*>.*?</p>", "".join(NEWS), flags=re.S):
    ours = [v for v in re.findall(r"\d\.\d\d%", visible(p)) if v not in OFFICIAL]
    if ours and "nlu2-note" not in p: assert "החישוב שלנו" in p, ("computed number without the label", ours, visible(p)[:90])
for cap in re.findall(r'<p class="nlu2-cap"[^>]*>(.*?)</p>', NEWTXT):
    if any(k in cap for k in ("תשואה", "קונה", "כמה כסף", "מס רכישה לפי", "מס על שכר", "שני מקורות")): assert "החישוב שלנו" in cap, cap
# FAQ: the section the FAQPage schema reads (inc/instruments.php nadlan_nli_faq): h3 + p, 30 questions, none repeated
fs = re.search(r"<h2[^>]*>\s*שאלות נפוצות[^<]{0,60}</h2>(.*?)(?=<h2|$)", re.sub(r"<!--.*?-->", "", new, flags=re.S), flags=re.S).group(1)
QS = [re.sub(r"<[^>]+>", "", q).strip() for q, a in re.findall(r"<h3[^>]*>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*)+)", fs, flags=re.S)]
OLDQ = [re.sub(r"<[^>]+>", "", q).strip() for q in re.findall(r"<h3[^>]*>(.*?)</h3>", re.search(r"<h2 dir=\"rtl\">שאלות נפוצות</h2>(.*?)<h2", raw, flags=re.S).group(1))]
assert len(QS) == 30 and len(set(QS)) == 30 and len(OLDQ) == 9, (len(QS), len(set(QS)), len(OLDQ))


# internal links: every one in the new copy must answer 200 with no redirect; official links are reported
class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None


OP = urllib.request.build_opener(NoRedir); UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"}


def status(u):
    try: return OP.open(urllib.request.Request(u, headers=UA), timeout=60).status
    except urllib.error.HTTPError as e: return e.code
    except Exception as e: return type(e).__name__


hrefs = sorted(set(re.findall(r'href="([^"#][^"]*)"', NEWTXT)))
inner = [h for h in hrefs if h.startswith("/") or h.startswith(SITE)]
bad = []
for h in inner:
    st = status(h if h.startswith("http") else SITE + h)
    if st != 200: bad.append((h, st))
    time.sleep(0.2)
assert not bad, ("internal links must answer 200", bad)
offi = [(h, status(h)) for h in hrefs if h.startswith("http") and not h.startswith(SITE) and "wa.me" not in h]

words_new = len(re.findall(r"[\w֐-׿\"'״]+", visible(re.sub(r"<svg\b.*?</svg>", " ", "".join(NEWS), flags=re.S))))
words_all = len(re.findall(r"[\w֐-׿\"'״]+", visible(re.sub(r"<svg\b.*?</svg>", " ", new, flags=re.S))))
cells = len(re.findall(r"<t[dh][ >]", re.sub(r"<svg\b.*?</svg>", "", new, flags=re.S)))
figs = len(re.findall(r"\d[\d,.]*", re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b.*?</\1>", " ", new, flags=re.S))))
print("  words: %d on the page (%d new) | tables %d (%d new) | table cells %d | figures in text %d | svg %d | h2 %d, h3 %d (in content; the tool adds its own h2) | FAQ %d (9 old + %d new)"
      % (words_all, words_new, new.count("<table"), new.count("<table") - raw.count("<table"), cells, figs, new.count("<svg"), new.count("<h2"), new.count("<h3"), len(QS), len(QA_NEW)))
print("  internal links checked: %d, all 200 | official links: %s" % (len(inner), ", ".join("%s %s" % (h.split("/")[2], st) for h, st in offi)))
print("  language gates: no long dash, no banned word in the new copy or the page, no zero numbers; svg text >= 12px; one h1")
print("  cross-check vs test_invest_math.py: national 42.3%% / Tel Aviv %s / Haifa %s / Beer Sheva %s / Ashkelon %s; %d of %d cities; %s per 100,000"
      % (pct(TA["be"], 1), pct(HFA["be"], 1), pct(BS["be"], 1), pct(ASK["be"], 1), len(POS), len(CITY), ils(pmt(100000))))

# ------------------------------------------------------------------ the internal source list (research stays in the repo, not on the page)
SRC = """# /investment/ (page 421): where every fact on the page comes from (internal, written by write_u2_page.py, %s)

Nothing here is printed on the page. The page carries one method-and-sources line; this file keeps the exact sources.

| Fact on the page | Source |
|---|---|
| Median rent and median deal price by city and rooms; cities %s, Israel %s | data.nadlan.gov.il settlement rent/buy files, version 20-08-2026 (Last-Modified 20.8.2026), read 25.10.2026, via `invest.json` (`src.gov`) |
| The government site's "תשואת שכירות חציונית שנתית" and its formula | nadlan.gov.il per city (eyes, Tel Aviv 2.72%%); formula checked in %d of %d cities (`invest.json` `checks.govYieldFormula`) |
| CBS average free-market rent with sampling error, %s | CBS price bulletin 7/2026, table 4.9 (research parse `data/cbs-rent-table-4-9-2026q2.json`) |
| Rent index +%s%% to %s; dwelling prices %s%% (%s); new dwellings %s%%; CPI +%s%% | CBS API series 120460, 40010, 70000, 120010, fetched 25.10.2026 |
| Average fixed unlinked mortgage rate %s%% (%s), CPI-linked %s%%, variable linked %s%% | Bank of Israel SDMX BIR_MRTG_99 |
| BoI rate %s%%, prime %s%%, since %s | Bank of Israel SDMX MNT_RIB_BOI_D and press release |
| Investment-home mortgages %s, %.2f bn NIS (%s) | Bank of Israel SDMX (BIR_MRTG_99 _62, _776) |
| 50%% LTV on an investment home (75%% single, 70%% replacement), payment up to 50%% of disposable income | Bank of Israel Proper Conduct of Banking Business Directive 329, s.2 and s.5-6 |
| Purchase tax on an additional home 8%% to %s, 10%% above, for purchases to %s | Tax Authority notice 12.10.2026, https://www.gov.il/he/pages/pa121026-2 (eyes; gov.il answers 403 to scripts) |
| Single-home brackets 2026 and the freeze to %s | Tax Authority buyer guide 2026 (Guides_knowrightinland_2026), pp. 61-62; instruction 1/2026 |
| Declaration within 30 days, payment within 60 days by self-assessment (s.51 deferral) | Tax Authority buyer guide 2026, pp. 11, 28 and the payment chapter |
| Betterment: 47%% / 20%% / 25%% by period, company 23%%, inflationary amount 10%%, new linear to 1.1.2014, deductions | Tax Authority buyer guide 2026, pp. 34-37 |
| Rental exemption ceiling %s a month in 2026 (same in 2024 and 2025), zero at %s, monthly test, all residential rents added | לפי כל זכות (updated 22.2.2026, "5,654 נכון ל־2026") and tax-advisor sites; the freeze of tax-amount indexation for 2025 to 2027; Tax Authority form-135 notes for tax year 2025 ("התקרה המתואמת היא 5,654"); Knesset Research Center paper, April 2024 (5,654 for 2024). The Tax Authority's own 2026 table was not opened |
| 10%% track: no deductions or depreciation, paid within 30 days after the tax year (30.1.2027 for 2026), no partial exemption on the same flat, depreciation added on a later taxable sale | Income Tax Ordinance s.122; לפי כל זכות (15.3.2026); Tax Authority payment page; buyer guide 2026 p.35 |
| Marginal track from %d%% (under 60) or %d%% (60+) | Income Tax Ordinance s.121; לפי כל זכות (15.3.2026) |
| Investors August 2026: 1,077 bought, 14%%, 1,171 sold, 46%% new, Haifa area 139 (9%%), stock down 8,707 since October 2021 to July 2026; 7,532 deals | Ministry of Finance chief economist, review for August 2026 (`mof-review-082026.pdf`) |
| Every computed number (gross yield, payment, rent minus payment, break-even share, equity, purchase tax and months of rent, tracks in shekels, 400,000 and 200,000 budgets) | this script, from `invest.json`, cross-checked against `tools/instruments/test_invest_math.py` (national 42.3%%, Tel Aviv 34.0%%, Haifa 49.0%%, Beer Sheva 53.2%%, Ashkelon 55.6%%, 13 of 65, 563 per 100,000) |

Kept off the page (unverified, dna.md section 6): the business threshold for rentals (secondary), commercial yields, multi-home owner counts,
rates after 10.2.2027, maintenance and vacancy norms, the investor surtax effect.
""" % (UPDATED, qlab(CQ), qlab(NAT4["q"]), D["checks"]["govYieldFormula"][0], D["checks"]["govYieldFormula"][1], qlab(CQ), IDX["rent"]["yoy"], mlab(IDX["rent"]["m"]),
       PV["yoy"], PWIN, IDX["newp"]["yoy"], IDX["cpi"]["yoy"], RATE, mlab(L["ratesPeriod"]), L["rates"][1]["rate"], L["rates"][2]["rate"], BOI["rate"], BOI["prime"], dmy(BOI["from"]),
       num(IL["n"]), IL["vol"] / 1e9, mlab(IL["m"]), ils(PT["extra"][0][0]), dmy(PT["until"]["extra"]), dmy(PT["until"]["single"]), ils(RT["ceiling"]), ils(RT["zero"]),
       round(100 * RT["under60"]), round(100 * RT["over60"]))
io.open(os.path.join(H, "page-sources.md"), "w", encoding="utf-8").write(SRC)

if DRY:
    pv_dir = os.path.join(H, "preview"); os.makedirs(pv_dir, exist_ok=True)
    io.open(os.path.join(pv_dir, "u2-page-content.html"), "w", encoding="utf-8", newline="").write(new)
    # a local render shell: the content as the theme prints it (760px column), the tool from the local files as inc/instruments.php mounts it
    A = "../../../../../plugins/nadlan-config/assets/instruments/"
    tool = ('<section class="nli" dir="rtl" lang="he" aria-label="מפת התשואה והתזרים"><div class="nli-host" data-nli="invest" data-nli-data="%sdata/invest.json?ver=local"><div class="nli__panel"><p class="nli__kicker">מחשבון · נדל״ן להשקעה</p><h2 class="nli__title">מפת התשואה והתזרים</h2></div></div></section>' % A)
    shell = ('<!doctype html>\n<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,">'
             '<title>/investment/ · תצוגה מקומית</title>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;800;900&family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">'
             '<link rel="stylesheet" href="%score.css?ver=local"><style>html,body{margin:0;background:#fff;color:#12202A}.entry-content{padding:0 16px}.entry-content>*{max-width:760px;margin-left:auto;margin-right:auto}h1{font:800 30px/1.25 Heebo,sans-serif;margin:24px auto 8px}</style></head>'
             '<body><main><div class="entry-content">%s</div></main><script src="%score.js?ver=local" defer></script><script src="%stools/invest.js?ver=local" defer></script></body></html>'
             % (A, new.replace('[nadlan_tool id="invest"]', tool), A, A))
    io.open(os.path.join(pv_dir, "u2-page-render.html"), "w", encoding="utf-8", newline="").write(shell)
    print("  --dry: wrote preview/u2-page-content.html, preview/u2-page-render.html, page-sources.md; nothing was posted")
    sys.exit(0)

bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers=UA), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
ok = {"read-back": back.strip() == new.strip(), "one h1": bd.count("<h1") == 1, "tool mounted": 'data-nli="invest"' in bd, "shortcode rendered": "[nadlan_tool" not in bd,
      "svg x3 in text": bd.count("nlu2-fig") == 3, "one FAQPage": page.count('"@type":"FAQPage"') == 1, "30 questions": page.count('"@type":"Question"') == 30,
      "SoftwareApplication": '"@type":"SoftwareApplication"' in page, "invest.js enqueued": "tools/invest.js" in page, "updated %s" % UPDATED: ("עודכן %s" % UPDATED) in bd}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
