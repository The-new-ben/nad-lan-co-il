# -*- coding: utf-8 -*-
"""U3: five data charts on /israel-mortgage-non-residents/ (post 4962), each drawn from a table already on the page (26.10.2026):
  A income needed for ₪1M / ₪2M / ₪3M at the 50% cap and at one third, in dollars;   B average rates May to August 2026 by track;
  C average rates by term (September 2026 reporting month, in force 19.10.2026);      D the ₪11,253 payment in dollars with a 10% shekel move;
  E purchase tax on ₪2M to ₪6M for a foreign resident, an Israeli resident's single home and a new oleh (12A), from data/ptax.json.
Palette of the page (dna 8.5): passport navy #1E2B47, visa violet #5B3FA0, security-print teal #0F7C7A, paper #F6F8FA, slate #2B3440;
Public Sans stack for words, IBM Plex Mono for figures; LTR; text 12px or more in a 420-wide box. Every number is computed here and
asserted against dna.md (11,253 · 22,507 · 33,760 · $3,616 / $3,287 / $4,018 · tax 320,000 / 95,538 / 10,106 on ₪4,000,000).
Exact insertions (each anchor once), backup, read-back, live check.   python .../write_u3_charts.py [--dry]"""
import io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "u3c"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 4962
NAVY, VIO, TEAL, PAPER, SLATE, LINE = "#1E2B47", "#5B3FA0", "#0F7C7A", "#F6F8FA", "#2B3440", "#D3DCE2"
FONT = "font-family:'Public Sans','IBM Plex Sans',system-ui,sans-serif"; MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"
USD = 3.112
D = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "boi-mortgage.json"), encoding="utf-8"))
P = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "ptax.json"), encoding="utf-8"))


def pmt(L, rate, n=300):
    r = rate / 1200.0
    return L * r / (1 - (1 + r) ** -n)


def tax(price, br):
    t, lo = 0.0, 0
    for hi, rt in br:
        top = price if hi is None else min(price, hi)
        if top > lo: t += (top - lo) * rt
        if hi is None or price <= hi: break
        lo = hi
    return round(t)


assert round(pmt(2000000, 4.62)) == 11253 and round(2 * pmt(2000000, 4.62)) == 22507 and round(3 * pmt(2000000, 4.62)) == 33760
assert (round(11253 / USD), round(11253 / (USD * 1.1)), round(11253 / (USD * 0.9))) == (3616, 3287, 4018)
TR = P["tracks"]
assert (tax(4000000, TR["foreign"]), tax(4000000, TR["single"]), tax(4000000, TR["oleh"])) == (320000, 95538, 10106)


def t(x, y, s, anchor="start", size=13, weight=400, fill=SLATE, mono=False):
    return '<text x="%s" y="%s" text-anchor="%s" style="%s;font-size:%spx;font-weight:%s" fill="%s">%s</text>' % (x, y, anchor, MONO if mono else FONT, size, weight, fill, s)


def svg(h, label, body):
    return ('<svg viewBox="0 0 420 %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%s" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">%s</svg>' % (h, label, body))


def fig(s, cap):
    return '<figure class="nlu3-fig">%s<figcaption>%s</figcaption></figure>\n' % (s, cap)


def money(v): return "{:,}".format(int(round(v)))


# A: income needed, dollars
A_rows = [(L, pmt(L, 4.62)) for L in (1000000, 2000000, 3000000)]
g = [t(12, 22, "Net monthly income a loan needs, in dollars", size=15, weight=600, fill=NAVY), t(12, 40, "25 years at 4.62% (Aug 2026 average); approx. at $1 = ₪3.112 (23 Oct 2026)", size=12)]
mx = max(3 * p for _, p in A_rows) / USD
for i, (L, p) in enumerate(A_rows):
    y = 62 + i * 70
    g.append(t(12, y + 12, "Loan ₪" + money(L), size=13, weight=600, fill=NAVY))
    for j, (k, c, lab) in enumerate(((2, TEAL, "at the 50% legal cap"), (3, VIO, "at about one third"))):
        v = k * p / USD; w = 190 * v / mx; yy = y + 20 + j * 22
        g.append('<rect x="12" y="%d" width="%.1f" height="16" fill="%s"/>' % (yy, w, c))
        g.append(t(18 + w, yy + 13, "$" + money(v), size=12.5, weight=600, fill=NAVY, mono=True))
        g.append(t(408, yy + 13, lab, anchor="end", size=12))
CH_A = fig(svg(286, "Net monthly income needed in dollars for loans of 1, 2 and 3 million shekels, at the 50 percent cap and at one third", "".join(g)),
           "The same arithmetic as the table above, in dollars. Banks often prefer about one third; the legal ceiling is 50% of disposable income.")

# B: rates May to August 2026 by track (Bank of Israel, new housing loans)
SER = [("Fixed, not linked", NAVY, [4.77, 4.73, 4.63, 4.62]), ("Fixed, CPI-linked", TEAL, [3.31, 3.27, 3.22, 3.29]),
       ("Variable, CPI-linked", VIO, [3.43, 3.28, 3.17, 3.19]), ("Foreign currency", "#8A6D1F" if False else "#4F6B8A", [5.05, 4.46, 4.98, 4.86])]
assert SER[0][2][-1] == D["rates"]["fixed_nl"]["rate"] and SER[1][2][-1] == D["rates"]["fixed_cpi"]["rate"] and SER[2][2][-1] == D["rates"]["var_cpi"]["rate"]
x0, x1, y0, y1, lo, hi = 60, 236, 60, 250, 3.0, 5.2
X = lambda i: x0 + i * (x1 - x0) / 3.0; Y = lambda v: y1 - (v - lo) * (y1 - y0) / (hi - lo)
g = [t(12, 22, "Average rates on new housing loans, 2026", size=15, weight=600, fill=NAVY), t(12, 40, "Bank of Israel, by track, May to August 2026", size=12)]
for v in (3.0, 3.5, 4.0, 4.5, 5.0):
    g.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s"/>' % (x0, Y(v), x1, Y(v), LINE)); g.append(t(x0 - 6, Y(v) + 4, "%.1f%%" % v, anchor="end", size=12, mono=True))
for i, m in enumerate(("May", "Jun", "Jul", "Aug")): g.append(t(X(i), y1 + 18, m, anchor="middle", size=12))
for k, (name, c, vals) in enumerate(SER):
    g.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.4"/>' % (" ".join("%.1f,%.1f" % (X(i), Y(v)) for i, v in enumerate(vals)), c))
    for i, v in enumerate(vals): g.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (X(i), Y(v), c))
    g.append(t(x1 + 10, Y(vals[-1]) + 4 + (k == 2) * 6 - (k == 1) * 6, "%s %.2f%%" % (name.split(",")[0] if k == 3 else name, vals[-1]), size=12, fill=c, weight=600))
CH_B = fig(svg(282, "Average Israeli mortgage rates May to August 2026: fixed not linked 4.77 to 4.62, fixed CPI-linked 3.31 to 3.29, variable CPI-linked 3.43 to 3.19, foreign currency 5.05 to 4.86", "".join(g)),
           "The table above as lines. CPI-linked rates are before inflation; the variable CPI-linked rate is the benchmark plus the margin.")

# C: rates by term, September 2026 reporting month
nl = [(b["from"], b["eff"]) for b in D["term"]["nl"]["buckets"]]; cp = [(b["from"], b["eff"]) for b in D["term"]["cpi"]["buckets"]]
labs = ["up to 1", "1 to 5", "5 to 10", "10 to 15", "15 to 20", "20 to 25", "over 25"]
x0, x1, y0, y1, lo, hi = 60, 400, 62, 232, 3.0, 5.0
X = lambda i: x0 + i * (x1 - x0) / 6.0; Y = lambda v: y1 - (v - lo) * (y1 - y0) / (hi - lo)
g = [t(12, 22, "Average rates by term, September 2026", size=15, weight=600, fill=NAVY), t(12, 40, "Bank of Israel, effective annual averages, in force from 19 Oct 2026", size=12)]
for v in (3.0, 3.5, 4.0, 4.5, 5.0):
    g.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s"/>' % (x0, Y(v), x1, Y(v), LINE)); g.append(t(x0 - 6, Y(v) + 4, "%.1f%%" % v, anchor="end", size=12, mono=True))
for i, l in enumerate(labs): g.append(t(X(i), y1 + 16 + (i % 2) * 14, l, anchor="middle", size=12))
g.append(t(x1, y1 + 46, "years to repayment", anchor="end", size=12))
ptsn = [(X(i), Y(v)) for i, (_, v) in enumerate(nl)]
ptsc = [(X(i + 1 if i else 0.5), Y(v)) for i, (_, v) in enumerate(cp)]  # CPI-linked starts with "up to 5" (between the first two marks)
for pts, c, name, last in ((ptsn, NAVY, "Not linked", nl[-1][1]), (ptsc, TEAL, "CPI-linked", cp[-1][1])):
    g.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.4"/>' % (" ".join("%.1f,%.1f" % p for p in pts), c))
    for p in pts: g.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (p[0], p[1], c))
g.append(t(x0 + 4, Y(nl[-1][1]) - 10, "Not linked: %.2f%% to %.2f%%" % (nl[0][1], nl[-1][1]), size=12, weight=600, fill=NAVY))
g.append(t(x0 + 4, Y(3.05) + 2, "CPI-linked: %.2f%% to %.2f%% (before inflation)" % (min(v for _, v in cp), max(v for _, v in cp)), size=12, weight=600, fill=TEAL))
CH_C = fig(svg(290, "Average Israeli mortgage rates by term, September 2026: not linked from 4.35 percent up to one year to 4.89 percent over 25 years; CPI-linked between 3.24 and 3.53 percent", "".join(g)),
           "Longer fixed terms cost more in shekels; CPI-linked rates stay flatter but rise with inflation on top.")

# D: the payment in dollars with a 10% shekel move
vals = [("Shekel weakens 10%", 11253 / (USD * 1.1), TEAL), ("Today", 11253 / USD, NAVY), ("Shekel strengthens 10%", 11253 / (USD * 0.9), VIO)]
g = [t(12, 22, "A ₪11,253 payment in dollars", size=15, weight=600, fill=NAVY), t(12, 40, "₪2,000,000 over 25 years at 4.62%; $1 = ₪3.112 on 23 Oct 2026", size=12)]
for i, (lab, v, c) in enumerate(vals):
    y = 62 + i * 46; w = 150 * v / 4100.0
    g.append(t(12, y + 14, lab, size=13, weight=600, fill=NAVY))
    g.append('<rect x="170" y="%d" width="%.1f" height="22" fill="%s"/>' % (y, w, c))
    g.append(t(176 + w, y + 16, "$" + money(v), size=13, weight=600, fill=NAVY, mono=True))
CH_D = fig(svg(206, "A monthly payment of 11,253 shekels is about 3,287 dollars if the shekel weakens 10 percent, 3,616 dollars today and 4,018 dollars if it strengthens 10 percent", "".join(g)),
           "If you earn in dollars, a shekel loan moves with the exchange rate. The Bank of Israel's 30-day range for the dollar is in the calculator.")

# E: purchase tax by price and status
prices = [2000000, 3000000, 4000000, 5000000, 6000000]
cols = [("Foreign resident", TR["foreign"], VIO), ("Israeli resident, single home", TR["single"], NAVY), ("New oleh, 12A", TR["oleh"], TEAL)]
mxv = tax(6000000, TR["foreign"])
g = [t(12, 22, "Purchase tax by price and status", size=15, weight=600, fill=NAVY), t(12, 40, "Tax Authority brackets; foreign resident track until 10 Feb 2027", size=12)]
for i, pr in enumerate(prices):
    y = 58 + i * 64
    g.append(t(12, y + 12, "₪" + money(pr), size=13, weight=600, fill=NAVY, mono=True))
    for j, (lab, br, c) in enumerate(cols):
        v = tax(pr, br); w = max(1.5, 260 * v / mxv); yy = y + 18 + j * 14
        g.append('<rect x="12" y="%d" width="%.1f" height="11" fill="%s"/>' % (yy, w, c))
        g.append(t(18 + w, yy + 10, "₪" + money(v), size=12, fill=NAVY, mono=True))
ly = 58 + len(prices) * 64 + 6
for j, (lab, _, c) in enumerate(cols):
    g.append('<rect x="%d" y="%d" width="12" height="12" fill="%s"/>' % (12 + j * 136, ly, c)); g.append(t(28 + j * 136, ly + 11, lab.replace("Israeli resident, ", "Resident, "), size=12))
CH_E = fig(svg(ly + 24, "Purchase tax on homes from 2 to 6 million shekels for a foreign resident, an Israeli resident buying a single home and a new oleh", "".join(g)),
           "Our arithmetic on the published brackets. On ₪4,000,000: ₪320,000 for a foreign resident, ₪95,538 for a resident's single home, ₪10,106 for a new oleh.")

s, r, _ = req("GET", "/wp-json/wp/v2/posts/%d?context=edit&_fields=content,link" % PID)
raw = r["content"]["raw"]; new = raw
assert raw.count("nlu3-chart-v1") == 0, "already added"


def after_table(text, caption, html):
    i = text.index(caption); assert text.count(caption) == 1, caption
    e = text.index("</figure>", i) + len("</figure>")
    return text[:e] + "\n" + html.replace('<figure class="nlu3-fig">', '<figure class="nlu3-fig nlu3-chart-v1">', 1) + text[e:]


new = after_table(new, "Net monthly income a loan needs", CH_A)
new = after_table(new, "Average rates on new housing loans, May to August 2026", CH_B)
new = after_table(new, "Average mortgage rates by term, reporting month September 2026", CH_C)
new = after_table(new, "monthly payment in your currency", CH_D)
a = '<h2 id="documents-checklist"'
assert new.count(a) == 1
new = new.replace(a, CH_E.replace('<figure class="nlu3-fig">', '<figure class="nlu3-fig nlu3-chart-v1">', 1) + a)
vis = re.sub(r"<[^>]+>", " ", new)
assert not re.search(r"[–—]", vis), "long dash"
print("[post %d] svg %d -> %d" % (PID, raw.count("<svg"), new.count("<svg")))
if DRY:
    io.open(os.path.join(H, "preview", "u3-charts.html"), "w", encoding="utf-8").write('<html lang="en"><meta charset="utf-8"><body style="max-width:680px;margin:20px auto">' + CH_A + CH_B + CH_C + CH_D + CH_E + "</body></html>")
    sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "post-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/posts/%d" % PID, {"content": new})
back = req("GET", "/wp-json/wp/v2/posts/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"read-back": back.strip() == new.strip(), "5 charts": page.count("nlu3-chart-v1") >= 5, "one h1": page[page.find("<body"):].count("<h1") == 1, "lang en": '<html lang="en"' in page, "one FAQPage": page.count('"@type":"FAQPage"') == 1}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
