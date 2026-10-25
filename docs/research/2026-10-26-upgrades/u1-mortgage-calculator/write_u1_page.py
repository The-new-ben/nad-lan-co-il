# -*- coding: utf-8 -*-
"""U1 on /mortgage-calculator/ (page 121): the content upgrade of dna.md sections 8.1 to 8.8, around the new tool Mortgage 2.0
(tools/mortgage.js, registry id `mortgage`, release 1.72.523).

ADDITIVE: nothing existing is removed. Title and H1 stay (8.1). The two old inline calculators (id="nlc-mortgage" and the `nmc`
block) stay on the page, untouched; every original line of the live content must still be there afterwards (asserted). The only
edits inside old text are the two banned words that dna.md section 9.3 orders out in the same release ("Nadlan", "סימולציה").

What it adds:
  1. under the H1: the 50-word answer paragraph (8.2), a CTA row (#mortgage-tool, #bank-offer-check) and the tool mount
     <div id="mortgage-tool"></div>[nadlan_tool id="mortgage"], BEFORE the old nlc-mortgage block;
  2. after the old widgets, before the existing article: the sections of 8.3 items 5 to 14 with tables T1 to T9 BUILT FROM DATA
     (plugins/nadlan-config/assets/instruments/data/boi-mortgage.json + boi-rate.json) and our own amortization, and the
     infographics V1 to V4 as inline SVG (NadLan Instruments palette); a short related-calculators line; method, sources and
     "עודכן 26.10.2026" at the end of the block (the honesty statement is written by the coordinator, not here);
  3. 25 questions appended to the existing FAQ so the visible FAQ reaches 30 (8.8; no duplicate of the 5 already there).
Asserts: every anchor matches once; hand values of dna.md 8.4 (5,627 / 687,997; 7,183 to 3,346 / 579,425; T5; T6); effective to
nominal matches the data file; every number in the new visible text is traceable (dna.md section 6, the data files, or our own
computation registered here); language law (no em or en dash, no spaced hyphen, banned words, no zero amounts, no ASCII double
quote that WordPress would curl); every internal link answers 200 with no redirect; old content kept line by line.
  python docs/research/2026-10-26-upgrades/u1-mortgage-calculator/write_u1_page.py --dry   (GET only, writes preview/u1-page-content.html)
  python docs/research/2026-10-26-upgrades/u1-mortgage-calculator/write_u1_page.py         (backup, POST, read-back, live check)"""
import io, json, math, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 121
SITE = "https://nad-lan.co.il"
UPDATED = "26.10.2026"
DATA = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")
D = json.load(io.open(os.path.join(DATA, "boi-mortgage.json"), encoding="utf-8"))
BR = json.load(io.open(os.path.join(DATA, "boi-rate.json"), encoding="utf-8"))
DNA = io.open(os.path.join(H, "dna.md"), encoding="utf-8").read()

# ------------------------------------------------------------------------------------------------ number provenance
NUMRE = re.compile(r"\d+(?:[.,]\d+)*")
ALLOW = set()


def norm(tok):
    return tok.replace(",", "") if re.fullmatch(r"\d{1,3}(?:,\d{3})+", tok) else tok


def reg(s):
    """Register every number printed by a helper (data or our own computation) as traceable, and return the string."""
    for tok in NUMRE.findall(s):
        ALLOW.add(norm(tok))
    return s


def _allow_text(txt):
    for tok in NUMRE.findall(txt):
        ALLOW.add(norm(tok))
        for part in re.split(r"[.,]", tok):  # "8.1 → 4.00%" style dates and lists in dna.md
            pass


def _allow_json(o):
    if isinstance(o, dict):
        for v in o.values(): _allow_json(v)
    elif isinstance(o, list):
        for v in o: _allow_json(v)
    elif isinstance(o, bool):
        pass
    elif isinstance(o, (int, float)):
        for f in ("%g", "%.1f", "%.2f"):
            ALLOW.add(f % o)
        if float(o).is_integer(): ALLOW.add(str(int(o)))
        if 0 < o < 1:
            for f in ("%g", "%.2f"):
                ALLOW.add(f % (o * 100))
    elif isinstance(o, str):
        _allow_text(o)


SEC6 = DNA[DNA.index("## 6. Verified facts"):DNA.index("## 7. Our page")]
_allow_text(SEC6)
_allow_json(D)
_allow_json(BR)


def rnd(x):
    return int(math.floor(x + 0.5))


def ils(x):
    return reg("{:,}".format(rnd(x)))


def pc(x, d=2):
    return reg(("%." + str(d) + "f") % x + "%")


def num(x, d=1):
    return reg(("%." + str(d) + "f") % x)


def dt(iso):
    y, m, d = iso[:10].split("-")
    return reg("%d.%d.%s" % (int(d), int(m), y))


def dm(iso):
    y, m, d = iso[:10].split("-")
    return reg("%d.%d" % (int(d), int(m)))


HEM = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]


def mon(ym):
    return reg("%s %s" % (HEM[int(ym[5:7]) - 1], ym[:4]))


def mil(x, d=2):
    s = ("%." + str(d) + "f") % (x / 1e6)
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return reg(s)


# ------------------------------------------------------------------------------------------------ the data
P, F, C, M = D["policy"], D["forecast"], D["cpi"], D["market"]
RT, TN, TC, RU, FE, TRK = D["rates"], D["term"]["nl"], D["term"]["cpi"], D["rules"], D["fees"], D["tracks"]
FIX = RT["fixed_nl"]["rate"]            # 4.62, קל"צ average, August 2026
FIXC = RT["fixed_cpi"]["rate"]          # 3.29
VARC = RT["var_cpi"]["rate"]            # 3.19
PRIMEAVG = TRK["prime"]["rate"]         # 4.27, BoI "up to 1 year" not-linked average, nominal (the prime part of the baskets)
MONTH = M["month"]                      # 2026-08
assert TN["buckets"][0]["nom"] == PRIMEAVG and TRK["var5_cpi"]["rate"] == VARC


def eff2nom(e):
    return 1200.0 * ((1 + e / 100.0) ** (1 / 12.0) - 1)


for blk in (TN, TC):  # the file converts from the unrounded xls value, so allow the rounding of a 2-decimal effective rate
    assert abs(eff2nom(blk["avg_eff"]) - blk["avg_nom"]) < 0.011, blk["avg_eff"]
    for b in blk["buckets"]:
        assert abs(eff2nom(b["eff"]) - b["nom"]) < 0.011, (b["label"], b["eff"], b["nom"])

# ------------------------------------------------------------------------------------------------ our own amortization


def pmt(P0, annual, n):
    r = annual / 1200.0
    return P0 / n if r == 0 else P0 * r / (1 - (1 + r) ** -n)


def sched(P0, annual, months, method="spitzer", grace=0, grace_kind="partial", cpi=0.0):
    """Monthly schedule: Spitzer (annuity), equal principal, bullet, balloon; grace inside the term (partial = interest only,
    full = interest added to the balance); CPI linkage applied to the balance every month, payment re-annuitized."""
    r = annual / 1200.0
    f = (1 + cpi / 100.0) ** (1 / 12.0) if cpi else 1.0
    bal = float(P0); pays = []; interest = 0.0; link = 0.0
    for m in range(1, months + 1):
        if f != 1.0:
            link += bal * (f - 1); bal *= f
        i = bal * r; rem = months - m + 1
        if m <= grace:
            if grace_kind == "partial":
                pay = i
            else:
                pay = 0.0; bal += i
            interest += i; pays.append(pay); continue
        if method == "spitzer":
            pay = pmt(bal, annual, rem)
        elif method == "equal":
            pay = bal / rem + i
        elif method == "bullet":
            pay = i + (bal if m == months else 0.0)
        elif method == "balloon":
            if m < months:
                bal += i; interest += i; pays.append(0.0); continue
            pay = bal + i
        else:
            raise ValueError(method)
        interest += i; bal -= (pay - i); pays.append(pay)
    return {"pays": pays, "interest": interest, "link": link, "total": sum(pays), "first": pays[0], "last": pays[-1], "max": max(pays)}


MIL = 1000000
S25 = sched(MIL, FIX, 300); E25 = sched(MIL, FIX, 300, "equal")
GP = sched(MIL, FIX, 300, grace=12); GF = sched(MIL, FIX, 300, grace=12, grace_kind="full")
BU = sched(MIL, FIX, 300, "bullet"); BA = sched(MIL, FIX, 300, "balloon")
BU3 = sched(MIL, FIX, 36, "bullet"); BA3 = sched(MIL, FIX, 36, "balloon")


def basket(k, years):
    n = years * 12
    if k == "b1": return pmt(MIL, FIX, n)
    if k == "b2": return pmt(MIL / 3.0, FIX, n) + pmt(MIL / 3.0, PRIMEAVG, n) + pmt(MIL / 3.0, VARC, n)
    return pmt(MIL / 2.0, FIX, n) + pmt(MIL / 2.0, PRIMEAVG, n)


def basket_interest(k, years):
    n = years * 12
    return basket(k, years) * n - MIL


# the opening mix of the tool (README of the preview): 600,000 קל"צ, 400,000 prime-track average, 200,000 variable CPI, 25 years, CPI 2%
MX = [sched(600000, FIX, 300), sched(400000, PRIMEAVG, 300), sched(200000, VARC, 300, cpi=F["inflation_4q"])]
MIX_FIRST = sum(s["first"] for s in MX); MIX_MAX = max(sum(s["pays"][m] for s in MX) for m in range(300))
MIX_INT = sum(s["interest"] for s in MX); MIX_LINK = MX[2]["link"]; MIX_TOTAL = sum(s["total"] for s in MX)
# hand values of dna.md 8.4 and the preview README (must match to the shekel)
HAND = {"spitzer 25y 4.62": (rnd(S25["first"]), 5627), "spitzer interest": (rnd(S25["interest"]), 687997),
        "equal first": (rnd(E25["first"]), 7183), "equal last": (rnd(E25["last"]), 3346), "equal interest": (rnd(E25["interest"]), 579425),
        "T6 4.5% 25y": (rnd(pmt(MIL, 4.5, 300)), 5558), "T6 5% 25y": (rnd(pmt(MIL, 5.0, 300)), 5846),
        "T5 20y b1": (rnd(basket("b1", 20)), 6391), "T5 20y b2": (rnd(basket("b2", 20)), 6079), "T5 20y b3": (rnd(basket("b3", 20)), 6297),
        "T5 25y b1": (rnd(basket("b1", 25)), 5627), "T5 25y b2": (rnd(basket("b2", 25)), 5299), "T5 25y b3": (rnd(basket("b3", 25)), 5528),
        "T5 30y b1": (rnd(basket("b1", 30)), 5138), "T5 30y b2": (rnd(basket("b2", 30)), 4796), "T5 30y b3": (rnd(basket("b3", 30)), 5035),
        "tool opening first": (rnd(MIX_FIRST), 6517), "tool opening highest": (rnd(MIX_MAX), 7136), "tool opening interest": (rnd(MIX_INT), 772977),
        "tool opening linkage": (rnd(MIX_LINK), 67452), "tool opening total": (rnd(MIX_TOTAL), 2040429)}
bad = {k: v for k, v in HAND.items() if v[0] != v[1]}
assert not bad, bad
print("[math] %d hand values match (dna.md 8.4 + the tool's opening numbers)" % len(HAND))

# ------------------------------------------------------------------------------------------------ links (internal: 200, no redirect)
LINKS = {
    "reverse": "/mortgage-calculator/reverse-mortgage/", "capacity": "/mortgage-calculator/mortgage-repayment-capacity/",
    "ltv": "/mortgage-calculator/mortgage-ltv-ratio/", "rates": "/mortgage-calculator/mortgage-interest-rates/",
    "any": "/mortgage-calculator/mortgage-for-any-purpose/", "bridge": "/mortgage-calculator/bridge-loan-apartment/",
    "ptax": "/purchase-tax-calculator/", "pcost": "/apartment-purchase-cost-calculator/", "refi": "/mortgage-refinance/",
    "grace": "/glossary/mortgage-grace-period/", "cpi": "/cpi-calculator/", "dira": "/dira-behanacha/",
}
EXT = {"boi_rates": "https://www.boi.org.il/information/interestrates/", "d451": "https://www.boi.org.il/media/ptchkgxk/451-1-1.pdf",
       "mashfix": TN["src"]["url"], "pribmash": TC["src"]["url"], "sdmx": M["src"]["url"], "boirate": P["src"]["url"], "cbs": C["src"]["url"]}


def check_url(u, internal):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u + ("?x=%d" % time.time() if internal else ""), headers={"User-Agent": "Mozilla/5.0"}), timeout=60)
        return r.status, r.geturl().split("?")[0] == u
    except Exception as e:  # noqa
        return str(e)[:60], False


for k, p in LINKS.items():
    st, same = check_url(SITE + p, True)
    assert st == 200 and same, ("internal link not 200 / redirected", p, st, same)
ext_state = {k: check_url(u, False) for k, u in EXT.items()}
print("[links] %d internal links answer 200 with no redirect | external: %s" % (len(LINKS), ", ".join("%s %s" % (k, v[0]) for k, v in ext_state.items())))


def a(key, text):
    return '<a href="%s">%s</a>' % (LINKS[key], text)


def ax(key, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (EXT[key], text)


# ------------------------------------------------------------------------------------------------ HTML pieces (one line each: wpautop safe)


def table(title, src, head, rows, num_cols=()):
    """A real data table; the figure caption = title + source and date, kept outside the scroll area so it never scrolls away.
    Five columns or more get class w: on phones the first column stays in place while the numbers scroll sideways."""
    h = "".join('<th scope="col">%s</th>' % c for c in head)
    body = []
    for r in rows:
        cells = "".join('<td%s>%s</td>' % (' class="n"' if (j + 1) in num_cols else "", c) for j, c in enumerate(r[1:]))
        body.append('<tr><th scope="row">%s</th>%s</tr>' % (r[0], cells))
    return ('<figure class="nlu1-t"><figcaption>%s<small>%s</small></figcaption><div class="nlu1-x"><table%s><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div></figure>\n'
            % (title, src, ' class="w"' if len(head) >= 5 else "", h, "".join(body)))


def fig(svg, cap):
    return '<figure class="nlu1-f"><div class="nlu1-svg">%s</div><figcaption>%s</figcaption></figure>\n' % (svg, cap)


def sec(sid, h2, body):
    return '<section id="%s">\n<h2>%s</h2>\n%s</section>\n' % (sid, h2, body)


def p(s):
    return "<p>%s</p>\n" % s


# ------------------------------------------------------------------------------------------------ SVG (NadLan Instruments)
FONT = "font-family:'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif"
MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"
INK, INK2, SEA, DEEP, MID, LIGHT, GREY, LINE, RED = "#12202A", "#3E4C58", "#2F6F86", "#1F4B5C", "#5B97AD", "#B5D0DB", "#B9C8D1", "#D3DCE2", "#C42550"
W = 420


def t(x, y, s, anchor="start", size=13, weight=400, fill=INK, mono=False, halo=False):
    hs = ' stroke="#fff" stroke-width="3" paint-order="stroke"' if halo else ""
    return '<text x="%s" y="%s" text-anchor="%s" style="%s;font-size:%spx;font-weight:%s" fill="%s"%s>%s</text>' % (
        ("%.1f" % x) if isinstance(x, float) else x, ("%.1f" % y) if isinstance(y, float) else y, anchor, MONO if mono else FONT, size, weight, fill, hs, s)


def svg_open(h, label):
    return ('<svg viewBox="0 0 %d %d" direction="rtl" role="img" aria-label="%s" style="display:block;width:100%%;height:auto;max-width:560px;background:#fff">' % (W, h, label))


def tw(s, size, mono=False):
    """Rough text width in viewBox units (Plex Sans Hebrew ~0.53 em per letter, Plex Mono 0.6 em), for legend layout."""
    w = 0.0
    for ch in s:
        w += (0.6 if mono else (0.56 if ch.isdigit() else 0.53)) * size if not ch.isspace() else 0.28 * size
    return w


def legend(items, y, size=13.5, gap=18, sw=18):
    """Right-aligned legend rows (RTL): each item = a swatch (line, dashed line, box, hatch or ring) then its word; wraps."""
    out = []; x = W - 12; row = 0
    for kind, col, dash, word in items:
        need = sw + 6 + tw(word, size) + gap
        if x - need < 8:
            row += 1; x = W - 12
        yy = y + row * (size + 9)
        if kind == "line":
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.4"%s/>' % (x - sw, yy - size * 0.32, x, yy - size * 0.32, col, (' stroke-dasharray="%s"' % dash) if dash else ""))
        elif kind == "ring":
            out.append('<circle cx="%.1f" cy="%.1f" r="5" fill="#fff" stroke="%s" stroke-width="2"/>' % (x - sw / 2.0, yy - size * 0.32, col))
        else:
            out.append('<rect x="%.1f" y="%.1f" width="13" height="13" fill="%s" stroke="%s" stroke-width="0.6"/>' % (x - 13, yy - size * 0.8, col, INK))
        out.append(t(x - sw - 6, yy, word, size=size))
        x -= need
    return out, y + row * (size + 9)


def v1_tracks():
    """V1: how August's mortgages were taken: one stacked bar of the volume by track + three numbers beside it."""
    tr = M["tracks"]; vol = M["volume_k"] / 1e6
    cols = {"var_nl": DEEP, "fixed_nl": MID, "fixed_cpi": LIGHT, "var_cpi": "url(#nlu1hatch)", "fx": INK}
    H_ = 196 + 27 * len(tr)
    lab = "איך לקחו משכנתא ב%s: %s" % (mon(MONTH), ", ".join("%s %s" % (x["label"], pc(x["share"], 1)) for x in tr))
    g = [svg_open(H_, lab), '<defs><pattern id="nlu1hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="%s"/><line x1="0" y1="0" x2="0" y2="6" stroke="%s" stroke-width="1.6"/></pattern></defs>' % (LIGHT, DEEP)]
    g.append(t(W - 12, 27, "איך לקחו משכנתא ב%s" % mon(MONTH), size=17, weight=600))
    g.append(t(W - 12, 49, "%s מיליארד ₪ במשכנתאות חדשות, לפי מסלול" % num(vol, 2), size=13.5, fill=INK2))
    stats = [(ils(M["loans"]), "משכנתאות חדשות"), ("%s מיליון ₪" % mil(M["avg_loan"]), "ממוצע למשכנתא"), ("%s שנים" % num(M["term_nl"], 1), "תקופה ממוצעת")]
    for i, (v, l) in enumerate(stats):
        xr = W - 12 - i * 136
        if i: g.append('<line x1="%d" y1="66" x2="%d" y2="114" stroke="%s"/>' % (xr + 7, xr + 7, LINE))
        g.append(t(xr, 91, v, size=21, weight=500, mono=not re.search(r"[א-ת]", v)))
        g.append(t(xr, 110, l, size=13, fill=INK2))
    x1, x0, y, hb = W - 12, 12, 130, 34; span = x1 - x0; cur = x1
    for x in tr:  # right to left, the biggest track first; a 2 px surface gap between fills
        w = span * x["share"] / 100.0
        if w >= 0.5:
            gap = 2 if cur - w > x0 + 1 else 0
            g.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="%s"><title>%s: %s</title></rect>' % (cur - w + gap, y, max(w - gap, 0.6), hb, cols[x["k"]], x["label"], pc(x["share"], 1)))
            if w > 70:
                g.append(t(cur - w / 2, y + 23, pc(x["share"], 1), anchor="middle", size=15, weight=500, fill="#fff", mono=True))
        cur -= w
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (x0, y + hb + 8, x1, y + hb + 8, LINE))
    for i, x in enumerate(tr):
        yy = 198 + i * 27
        g.append('<rect x="%d" y="%d" width="14" height="14" fill="%s" stroke="%s" stroke-width="0.6"/>' % (W - 26, yy - 12, cols[x["k"]], INK))
        g.append(t(W - 34, yy, x["label"], size=14.5))
        g.append(t(14, yy, pc(x["share"], 1), anchor="end", size=14.5, weight=500, mono=True))
    g.append("</svg>")
    return "".join(g)


def buckets_svg(title, sub, blist, lines, words, label, unit_word):
    """V2/V3: last month's volume by bucket, left to right like the tool, with the directive's lines; `words` names each line
    in the legend, so identity is never colour alone."""
    n = len(blist); x0, x1 = 16, W - 16; bw = (x1 - x0) / float(n); yb, ytop = 262, 112
    mx = max(b["share"] for b in blist)
    big = max(range(n), key=lambda i: blist[i]["share"])
    leg, ly = legend([("line", l[1], l[2], wd) for l, wd in zip(lines, words)], yb + 66)
    g = [svg_open(int(ly + 14), label)]
    g.append(t(W - 12, 27, title, size=17, weight=600))
    g.append(t(W - 12, 49, sub, size=13.5, fill=INK2))
    for k in range(5):
        yy = yb - (yb - ytop) * k / 4.0
        g.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="%s"/>' % (x0, yy, x1, yy, LINE if k else INK, 1 if k else 1.3))
    def xof(v):
        for i, b in enumerate(blist):
            hi = b["to"] if b["to"] is not None else b["from"] + 10
            if v <= hi or i == n - 1:
                return x0 + bw * (i + min(1.0, max(0.0, (v - b["from"]) / float(hi - b["from"]))))
        return x1
    lxs = [xof(l[0]) for l in lines]
    bars, labels = [], []
    for i, b in enumerate(blist):
        xl = x0 + bw * i; hh = (yb - ytop) * b["share"] / mx
        lab = ("עד %d" % b["to"]) if b["from"] == 0 else (("מעל %d" % b["from"]) if b["to"] is None else ("%d עד %d" % (b["from"], b["to"])))
        reg(lab)
        sh = pc(b["share"], 2 if b["share"] < 0.1 else 1)
        if b["share"] > 0:
            bars.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1.5" fill="%s"><title>%s%%: %s</title></rect>' % (xl + 3, yb - max(hh, 2), bw - 6, max(hh, 2), SEA if i == big else GREY, lab, sh))
            cx, half = xl + bw / 2, tw(sh, 14, mono=True) / 2 + 3
            for lx in lxs:  # a directive line through the value: move the value into the free part of the bar
                if cx - half < lx < cx + half:
                    cx = (xl + 3 + lx) / 2 if lx - (xl + 3) > (xl + bw - 3) - lx else (lx + xl + bw - 3) / 2
            labels.append(t(cx, yb - max(hh, 2) - 6, sh, anchor="middle", size=14, weight=600 if i == big else 400, mono=True, halo=True))
        else:
            labels.append(t(xl + bw / 2, yb - 8, "לא ניתנו", anchor="middle", size=13, fill=INK2, halo=True))
        labels.append(t(xl + bw / 2, yb + 20, lab, anchor="middle", size=13.5, fill=INK2))
    g += bars
    for (v, col, dash, tag), xx in zip(lines, lxs):
        g.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2"%s/>' % (xx, ytop - 22, xx, yb, col, (' stroke-dasharray="%s"' % dash) if dash else ""))
        g.append(t(xx, ytop - 27, tag, anchor="middle", size=13.5, weight=600, fill=col, mono=True))
    g += labels
    g.append(t(W / 2.0, yb + 41, unit_word, anchor="middle", size=13, fill=INK2))
    g += leg
    g.append("</svg>")
    return "".join(g)


def _blab(b, d):
    rng = ("עד %d%%" % b["to"]) if b["from"] == 0 else (("מעל %d%%" % b["from"]) if b["to"] is None else ("%d%% עד %d%%" % (b["from"], b["to"])))
    return "%s: %s" % (rng, pc(b["share"], d(b["share"])))


def v2_pti():
    bl = [b for b in M["pti"] if b["from"] < 50] + [{"from": 50, "to": None, "share": sum(b["share"] for b in M["pti"] if b["from"] >= 50)}]
    lines = [(M["pti_avg"], SEA, "2 3", num(M["pti_avg"], 2)), (RU["pti_risk"] * 100, INK, "5 3", "40"), (RU["pti_max"] * 100, RED, None, "50")]
    lab = "התפלגות ההחזר מההכנסה במשכנתאות החדשות של %s: %s" % (mon(MONTH), ", ".join(_blab(b, lambda s: 1) for b in bl))
    words = ["ממוצע %s" % pc(M["pti_avg"]), "יותר הון מעל 40%", "תקרה 50%"]
    return buckets_svg("כמה מההכנסה הולך להחזר", "חלק מסכום המשכנתאות החדשות לפי ההחזר מההכנסה, %s" % mon(MONTH), bl, lines, words, reg(lab), "ההחזר מההכנסה, באחוזים")


def v3_ltv():
    bl = [b for b in M["ltv"] if b["from"] < 75] + [{"from": 75, "to": None, "share": round(sum(b["share"] for b in M["ltv"] if b["from"] >= 75), 2)}]
    lines = [(RU["ltv"]["invest"] * 100, DEEP, "2 3", "50"), (RU["ltv"]["replace"] * 100, INK, "5 3", "70"), (RU["ltv"]["single"] * 100, RED, None, "75")]
    lab = "התפלגות שיעור המימון במשכנתאות החדשות של %s: %s" % (mon(MONTH), ", ".join(_blab(b, lambda s: 2 if s < 1 else 1) for b in bl))
    words = ["דירה להשקעה 50%", "חליפית 70%", "יחידה 75%"]
    return buckets_svg("כמה מימון לקחו", "חלק מסכום המשכנתאות החדשות לפי שיעור המימון, %s" % mon(MONTH), bl, lines, words, reg(lab), "שיעור המימון, באחוזים משווי הדירה")


def v4_history():
    """V4: monthly averages since 2011 (CPI-linked) and 2013 (not linked), effective, the BoI rate as a step line (from 2015 in our
    file) and the October 2026 forecast point (3.0%, Q3 2027)."""
    def tx(xf): return x0 + (xf - X0) / (X1 - X0) * (x1 - x0)
    def ty(v): return yb - (yb - ytop) * v / 6.0
    def fr(ym): return int(ym[:4]) + (int(ym[5:7]) - 0.5) / 12.0
    nl, cp = TN["hist"], TC["hist"]
    leg, ly = legend([("line", DEEP, None, "לא צמודה"), ("line", MID, None, "צמודה למדד"), ("line", INK, "4 2", "ריבית בנק ישראל, מ-2015"), ("ring", INK, None, "תחזית")], 74)
    reg("2015")
    x0, x1, X0, X1 = 38, 352, 2011.5, 2028.0
    ytop = ly + 22; yb = ytop + 196
    lab = ("ריבית המשכנתא הממוצעת: לא צמודה מ%s עד %s, צמודה מ%s, וריבית בנק ישראל; בספטמבר 2026 %s ו-%s, ריבית בנק ישראל %s, תחזית %s ברבע השלישי 2027"
           % (mon(nl[0][0]), mon(nl[-1][0]), mon(cp[0][0]), pc(nl[-1][1]), pc(cp[-1][1]), pc(P["rate"]), pc(F["rate_q3_2027"], 1)))
    g = [svg_open(int(yb + 32), lab)]
    g.append(t(W - 12, 27, "ריבית המשכנתא לאורך השנים", size=17, weight=600))
    g.append(t(W - 12, 49, "ממוצע חודשי במשכנתאות, ריבית אפקטיבית, וריבית בנק ישראל", size=13.5, fill=INK2))
    g += leg
    for v in range(0, 7):
        yy = ty(v)
        g.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="%s"/>' % (x0, yy, x1, yy, INK if v == 0 else LINE, 1.3 if v == 0 else 1))
        g.append(t(x0 - 6, yy + 4.5, reg("%d%%" % v), size=13, fill=INK2, mono=True))
    for y in range(2012, 2028, 3):
        xx = tx(y)
        g.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s"/>' % (xx, yb, xx, yb + 5, INK))
        g.append(t(xx, yb + 21, reg(str(y)), anchor="middle", size=13, fill=INK2, mono=True))

    def path(series, col, w_, title):
        d = "M" + " L".join("%.1f %.1f" % (tx(fr(ym)), ty(v)) for ym, v in series)
        return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round"><title>%s</title></path>' % (d, col, w_, title)
    pts = []
    for c in BR["changes"]:
        y_, m_, d_ = (int(z) for z in c["from"].split("-")); xf = y_ + (m_ - 1 + (d_ - 1) / 30.0) / 12.0
        if pts: pts.append((xf, pts[-1][1]))
        pts.append((xf, c["rate"]))
    y_, m_, d_ = (int(z) for z in P["asof"].split("-")); xnow = y_ + (m_ - 1 + (d_ - 1) / 30.0) / 12.0
    pts.append((xnow, P["rate"]))
    g.append('<path d="M%s" fill="none" stroke="%s" stroke-width="1.7" stroke-dasharray="4 2"><title>ריבית בנק ישראל, %s היום</title></path>' % (" L".join("%.1f %.1f" % (tx(xf), ty(v)) for xf, v in pts), INK, pc(P["rate"])))
    g.append(path(cp, MID, 2.2, "צמודה למדד, ממוצע חודשי"))
    g.append(path(nl, DEEP, 2.2, "לא צמודה, ממוצע חודשי"))
    xf_ = 2027 + 7.5 / 12.0
    g.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.7" stroke-dasharray="1.5 3"/>' % (tx(xnow), ty(P["rate"]), tx(xf_), ty(F["rate_q3_2027"]), INK))
    g.append('<circle cx="%.1f" cy="%.1f" r="5" fill="#fff" stroke="%s" stroke-width="2"><title>תחזית בנק ישראל: %s ברבע השלישי 2027</title></circle>' % (tx(xf_), ty(F["rate_q3_2027"]), INK, pc(F["rate_q3_2027"], 1)))
    ends = [(ty(nl[-1][1]), pc(nl[-1][1]), DEEP, tx(fr(nl[-1][0])), ty(nl[-1][1])), (ty(cp[-1][1]), pc(cp[-1][1]), MID, tx(fr(cp[-1][0])), ty(cp[-1][1])),
            (ty(F["rate_q3_2027"]), pc(F["rate_q3_2027"], 1), INK, tx(xf_) + 6, ty(F["rate_q3_2027"]))]
    ends.sort(key=lambda e: e[0]); last = -99
    for yy, s, col, lx_, ly_ in ends:  # values only (the legend names the series), at least 17 units apart
        yy = max(yy, last + 17); last = yy
        g.append('<line x1="%.1f" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>' % (lx_, ly_, x1 + 5, yy, col))
        g.append(t(x1 + 8, yy + 4.5, s, anchor="end", size=13.5, weight=500, mono=True))
    g.append("</svg>")
    return "".join(g)


# ------------------------------------------------------------------------------------------------ the copy
GER = "״"  # gershayim, so WordPress does not curl an ASCII quote inside Hebrew abbreviations
KLZ, KZ = "קל" + GER + "צ", "ק" + GER + "צ"
M8 = mon(MONTH); INF = dt(TN["inforce"]); T_MONTH = mon(TN["month"][:7]); CPI_M = mon(C["latest"])
r25 = lambda P0, rate=FIX: pmt(P0, rate, 300)

LEAD = ("מחשבון משכנתא מחשב את ההחזר החודשי, הריבית וסך התשלומים לפי הסכום, המסלולים והתקופה. הקלידו סכום, בחרו תמהיל או אחד משלושת "
        "הסלים האחידים של בנק ישראל, וראו את ההחזר הראשון, את ההחזר הגבוה הצפוי, והאם הריבית שהבנק הציע לכם גבוהה מהממוצע שבנק ישראל פרסם "
        "החודש. כל הנתונים ממקורות רשמיים, עם תאריך.")
assert len(LEAD.split()) == 50, len(LEAD.split())

CSS = ("<style id=\"nlu1-css\">"
       ".nlu1-lead{font-size:18px;line-height:1.75;color:#12202A;max-width:74ch;margin:6px 0 14px}"
       ".nlu1-cta{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 18px}"
       # specificity above the skin's "body.nl-skin-a .nadlan-guide a{color:...!important}"
       "body .nlu1-cta a.nlu1-btn.nlu1-btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:10px 18px;border-radius:999px;border:1.5px solid #2F6F86;background:#fff!important;color:#2F6F86!important;text-decoration:none!important;font-weight:600;font-size:16px;line-height:1.2}"
       "body .nlu1-cta a.nlu1-btn.nlu1-btn.is-main{background:#2F6F86!important;color:#fff!important}"
       "a.nlu1-btn:focus-visible{outline:3px solid #12202A;outline-offset:2px}"
       ".nlu1-anchor{scroll-margin-top:84px}"
       ".nadlan-guide .nlu1 section{scroll-margin-top:84px}"
       ".nadlan-guide .nlu1 h3{font-size:21px}"
       ".nadlan-guide .nlu1-strip{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:2px solid #12202A;border-bottom:1px solid #12202A;margin:16px 0 8px;background:#fff}"
       ".nadlan-guide .nlu1-strip div{padding:10px 12px;border-inline-start:1px solid #D3DCE2}"
       ".nadlan-guide .nlu1-strip div:first-child{border-inline-start:0}"
       ".nadlan-guide .nlu1-strip b{display:block;font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:24px;font-weight:500;color:#12202A;line-height:1.3}"
       ".nadlan-guide .nlu1-strip span{display:block;font-size:13px;line-height:1.4;color:#3E4C58}"
       # tables: the theme stacks every article table into cards on phones and paints th beige, all !important; these are
       # data tables with column headings, so they stay tables (numbers scroll sideways inside the figure, never the page)
       ".nadlan-guide .nlu1-t{margin:18px 0 24px}"
       ".nadlan-guide .nlu1-x{overflow-x:auto;-webkit-overflow-scrolling:touch}"
       ".nadlan-guide .nlu1 .nlu1-t table{display:table!important;width:100%!important;border-collapse:separate;border-spacing:0;background:#fff;border:0;border-top:2px solid #12202A;border-bottom:1px solid #12202A;border-radius:0;margin:0;overflow:visible}"
       ".nadlan-guide .nlu1 .nlu1-t thead{display:table-header-group!important}"
       ".nadlan-guide .nlu1 .nlu1-t tbody{display:table-row-group!important}"
       ".nadlan-guide .nlu1 .nlu1-t tr{display:table-row!important;border:0!important;border-radius:0!important;margin:0!important;padding:0!important;background:#fff!important;box-shadow:none!important}"
       ".nadlan-guide .nlu1 .nlu1-t figcaption{display:block;text-align:right;padding:0 0 8px;margin:0;font-family:Assistant,'Segoe UI',Arial,sans-serif;font-size:16.5px;font-weight:700;color:#12202A;line-height:1.45}"
       ".nadlan-guide .nlu1 .nlu1-t figcaption small{display:block;font-weight:400;font-size:13.5px;color:#3E4C58;margin-top:3px;line-height:1.5}"
       ".nadlan-guide .nlu1 .nlu1-t th,.nadlan-guide .nlu1 .nlu1-t td{display:table-cell!important;width:auto!important;padding:9px 10px!important;border:0!important;border-bottom:1px solid #D3DCE2!important;font-family:Assistant,'Segoe UI',Arial,sans-serif;font-size:15px!important;line-height:1.5!important;text-align:right!important;vertical-align:top;color:#12202A!important;background:#fff!important;font-weight:400!important;letter-spacing:0!important}"
       ".nadlan-guide .nlu1 .nlu1-t thead th{color:#3E4C58!important;font-weight:600!important;font-size:13px!important;border-bottom:1px solid #12202A!important;vertical-align:bottom}"
       ".nadlan-guide .nlu1 .nlu1-t tbody th{font-weight:600!important;min-width:104px;overflow-wrap:anywhere}"
       ".nadlan-guide .nlu1 .nlu1-t tbody th small{display:block;font-weight:400;font-size:12.5px;line-height:1.45;color:#3E4C58;margin-top:2px}"
       ".nadlan-guide .nlu1 .nlu1-t td.n{font-family:'IBM Plex Mono',ui-monospace,monospace!important;font-size:14.5px!important;white-space:nowrap}"
       ".nadlan-guide .nlu1 .nlu1-t table.w th:first-child{position:sticky;right:0;z-index:1;box-shadow:-1px 0 0 #D3DCE2}"
       ".nadlan-guide .nlu1-f{margin:20px 0 26px}"
       ".nadlan-guide .nlu1-svg svg{max-width:560px!important}"
       ".nadlan-guide .nlu1-f figcaption,.nadlan-guide .nlu1-strip span,.nadlan-guide .nlu1-meta{font-family:Assistant,'Segoe UI',Arial,sans-serif}"
       ".nadlan-guide .nlu1-f figcaption{font-size:14.5px;line-height:1.65;color:#3E4C58;margin-top:8px;max-width:560px}"
       ".nadlan-guide .nlu1-go{margin:14px 0 6px}"
       ".nadlan-guide .nlu1-rel{border-top:2px solid #12202A;padding-top:10px;margin-top:26px}"
       ".nadlan-guide .nlu1-meta{font-size:14px;line-height:1.7;color:#3E4C58;border-top:1px solid #D3DCE2;padding-top:12px;margin-top:22px}"
       ".nadlan-guide .nlu1-meta a{color:#2F6F86}"
       "@media(max-width:640px){.nadlan-guide .nlu1-strip{grid-template-columns:repeat(2,minmax(0,1fr))}.nadlan-guide .nlu1-strip div:nth-child(3){border-inline-start:0}"
       ".nadlan-guide .nlu1-strip div:nth-child(n+3){border-top:1px solid #D3DCE2}"
       ".nadlan-guide .nlu1 .nlu1-t th,.nadlan-guide .nlu1 .nlu1-t td{padding:8px 8px!important;font-size:14px!important}.nadlan-guide .nlu1 .nlu1-t td.n{font-size:13px!important;padding:8px 6px!important}.nadlan-guide .nlu1 .nlu1-t table.w tbody th{min-width:88px}"
       ".nadlan-guide .nlu1-f .nlu1-svg{margin:0 -16px}.nadlan-guide .nlu1 h3{font-size:19px}}"
       "</style>")

TOP = (CSS + "\n"
       + '<p class="nlu1-lead">%s</p>\n' % LEAD
       + '<div class="nlu1-cta"><a class="nlu1-btn is-main" href="#mortgage-tool">לחישוב ההחזר</a><a class="nlu1-btn" href="#bank-offer-check">בדיקת הצעה מהבנק</a></div>\n'
       + '<div id="mortgage-tool" class="nlu1-anchor"></div>[nadlan_tool id="mortgage"]\n')

# --- 5. the numbers of today + T1
S5 = sec("mortgage-numbers-today", "המספרים של היום: ריבית, פריים ומדד",
         p("ריבית בנק ישראל עומדת על %s מאז %s, ובהחלטה של %s היא נשארה ללא שינוי. הפריים, שהבנקים קובעים כריבית בנק ישראל ועוד %s, עומד על %s. "
           "ההחלטה הבאה על הריבית תתפרסם ב-%s. אלה המספרים שהמחשבון למעלה פותח בהם, וכל אחד מהם מופיע כאן עם התאריך והמקור שלו."
           % (pc(P["rate"]), dt(P["from"]), dt(F["published"]), pc(P["prime"] - P["rate"], 1), pc(P["prime"]), dt(F["next_decision"])))
         + '<div class="nlu1-strip"><div><b>%s</b><span>ריבית בנק ישראל</span></div><div><b>%s</b><span>פריים</span></div><div><b>%s</b><span>%s ממוצע, %s</span></div><div><b>%s</b><span>מדד, 12 חודשים עד %s</span></div></div>\n'
         % (pc(P["rate"]), pc(P["prime"]), pc(FIX), KLZ, M8, pc(C["y12"], 1), CPI_M)
         + table("המספרים של היום", "נכון ל-%s. המקור של כל שורה כתוב מתחת לשם הנתון." % dt(P["asof"]),
                 ["הנתון והמקור", "הערך", "נכון ל"],
                 [[nm + "<small>%s</small>" % srcx, v, when] for nm, v, when, srcx in [
                     ("ריבית בנק ישראל", pc(P["rate"]), "בתוקף מ-%s" % dt(P["from"]), "בנק ישראל, סדרה MNT_RIB_BOI_D"),
                     ("ריבית הפריים", pc(P["prime"]), dt(P["asof"]), "ריבית בנק ישראל ועוד %s, כמקובל בבנקים" % pc(P["prime"] - P["rate"], 1)),
                     ("ההחלטה הבאה על הריבית", dt(F["next_decision"]), dt(P["asof"]), "עמוד ההודעות של בנק ישראל"),
                     ("מדד המחירים לצרכן, 12 חודשים", pc(C["y12"], 1), CPI_M, "הלשכה המרכזית לסטטיסטיקה, סדרה 120010"),
                     ("תחזית בנק ישראל לריבית, ממוצע ברבע השלישי של 2027", pc(F["rate_q3_2027"], 1), "תחזית %s" % dt(F["published"]), "חטיבת המחקר של בנק ישראל"),
                     ("תחזית בנק ישראל לאינפלציה, ארבעת הרבעונים הבאים", pc(F["inflation_4q"], 1), "תחזית %s" % dt(F["published"]), "חטיבת המחקר של בנק ישראל"),
                     ("ריבית ממוצעת, קבועה לא צמודה (%s)" % KLZ, pc(FIX), M8, "בנק ישראל, הלוואות חדשות לדיור"),
                     ("ריבית ממוצעת, קבועה צמודה (%s)" % KZ, pc(FIXC), M8, "בנק ישראל, הלוואות חדשות לדיור"),
                     ("ריבית ממוצעת, משתנה צמודה", pc(VARC), M8, "בנק ישראל, הלוואות חדשות לדיור")]], num_cols=(1,)))

# --- 6. the moat: your offer vs the BoI average
B2025 = [b for b in TN["buckets"] if b["from"] == 20][0]
OFF = 5.0
off_p, avg_p = pmt(MIL, OFF, 300), pmt(MIL, B2025["nom"], 300)
S6 = sec("offer-vs-average", "ההצעה שלכם מול הממוצע של בנק ישראל",
         p("קיבלתם הצעה מהבנק? הקלידו אותה בבדיקת ההצעה שבתוך המחשבון, מסלול אחר מסלול. לכל מסלול מופיעה הריבית הממוצעת שבנק ישראל פרסם לאותו סוג "
           "של ריבית והצמדה במשכנתאות החדשות של %s, וגם הריבית הממוצעת לאותה תקופה לפירעון, בתוקף מ-%s. הפער מתורגם לשקלים: כמה תשלמו יותר, או "
           "פחות, בחודש הראשון ולאורך כל ההלוואה." % (M8, INF))
         + p("<strong>דוגמה:</strong> הצעה של %s ₪ ב%s ל-25 שנה בריבית %s. ההחזר החודשי: %s ₪. הממוצע של בנק ישראל להלוואות לא צמודות לתקופה של %s "
             "הוא %s נומינלית (%s אפקטיבית), ובו ההחזר %s ₪. ההפרש: %s ₪ בחודש, ו-%s ₪ לאורך 25 השנים. עם מספר כזה כדאי לחזור לבנק."
             % (ils(MIL), KLZ, pc(OFF), ils(off_p), B2025["label"].replace("שנים", "שנה"), pc(B2025["nom"]), pc(B2025["eff"]), ils(avg_p), ils(off_p - avg_p), ils((off_p - avg_p) * 300)))
         + p("אחרי ההשוואה המחשבון מראה איפה המשכנתא שלכם עומדת בין %s המשכנתאות החדשות של %s: לפי ההחזר מההכנסה, לפי שיעור המימון, לפי גודל ההלוואה "
             "מול הממוצע של %s ₪ ולפי התקופה מול %s שנים בהלוואות הלא צמודות." % (ils(M["loans"]), M8, ils(M["avg_loan"]), num(M["term_nl"], 1)))
         + p("הגבולות של הבדיקה: הממוצעים כוללים את כל הלווים ואת כל שיעורי המימון, ולווה עם הכנסה יציבה ומימון נמוך יכול לקבל ריבית נמוכה מהממוצע. "
             "זו אינה הצעה לאשראי ואינה ייעוץ.")
         + '<div class="nlu1-cta nlu1-go"><a class="nlu1-btn is-main" href="#bank-offer-check">לבדיקת ההצעה שלכם</a></div>\n')

# --- 7. your mortgage among all of this month's mortgages (V1, V2 + T9a, V3 + T9b)
TRS = {x["k"]: x["share"] for x in M["tracks"]}
PTI = {(b["from"], b["to"]): b["share"] for b in M["pti"]}
LTVB = {(b["from"], b["to"]): b["share"] for b in M["ltv"]}
over75 = round(sum(b["share"] for b in M["ltv"] if b["from"] >= 75), 2)
over50 = sum(b["share"] for b in M["pti"] if b["from"] >= 50)
assert over50 == 0
inv_avg = M["invest"]["volume_k"] * 1000 / M["invest"]["loans"]
T9A = table("המשכנתאות החדשות לפי ההחזר מההכנסה", "חלק מסכום ההלוואות, %s. מקור: בנק ישראל, הלוואות חדשות לדיור (SDMX BIR_MRTG_99)." % M8,
            ["ההחזר מההכנסה", "חלק מהסכום"],
            [[("עד %d%%" % b["to"]) if b["from"] == 0 else ("%d%% עד %d%%" % (b["from"], b["to"])), pc(b["share"], 1)] for b in M["pti"] if b["from"] < 50]
            + [["מעל 50%", "לא ניתנו"]], num_cols=(1,))
T9B = table("המשכנתאות החדשות לפי שיעור המימון", "חלק מסכום ההלוואות, %s. מקור: בנק ישראל, הלוואות חדשות לדיור (SDMX BIR_MRTG_99)." % M8,
            ["שיעור המימון", "חלק מהסכום"],
            [[("עד %d%%" % b["to"]) if b["from"] == 0 else ("%d%% עד %d%%" % (b["from"], b["to"])), pc(b["share"], 2 if b["share"] < 1 else 1)] for b in M["ltv"] if b["from"] < 75]
            + [["מעל 75%", pc(over75, 2)]], num_cols=(1,))
for s_ in ("עד 10%", "עד 30%", "מעל 50%", "מעל 75%"): reg(s_)
S7 = sec("mortgages-this-month", "המשכנתא שלכם מול כל המשכנתאות של החודש",
         p("ב%s ניתנו בישראל %s משכנתאות חדשות בסך %s מיליארד ₪, בממוצע %s מיליון ₪ למשכנתא. %s מהן ניתנו לדירה להשקעה, בסך %s מיליארד ₪, כ-%s מיליון ₪ לכל אחת. "
           "בספטמבר, לפי פרסום ראשון של בנק ישראל, ניתנו משכנתאות בסך %s מיליארד ₪."
           % (M8, ils(M["loans"]), num(M["volume_k"] / 1e6, 2), mil(M["avg_loan"]), ils(M["invest"]["loans"]), num(M["invest"]["volume_k"] / 1e6, 2), mil(inv_avg), num(M["next_volume"]["volume_k"] / 1e6, 2)))
         + fig(v1_tracks(), "יותר ממחצית הכסף, %s, ניתן בריבית משתנה לא צמודה, כולל פריים, ועוד %s בריבית קבועה לא צמודה. המסלולים הצמודים למדד תפסו יחד %s בלבד. התקופה הממוצעת היא של ההלוואות הלא צמודות. מקור: בנק ישראל, הלוואות חדשות לדיור, %s."
               % (pc(TRS["var_nl"], 1), pc(TRS["fixed_nl"], 1), pc(TRS["fixed_cpi"] + TRS["var_cpi"], 1), M8))
         + "<h3>ההחזר מההכנסה</h3>\n"
         + p("באוגוסט ההחזר הממוצע היה %s מההכנסה. %s מהכסף ניתן למשכנתאות שההחזר בהן %s עד %s מההכנסה, ורק %s מעל %s. מעל %s לא ניתנה אף משכנתא, כי בנק ישראל אוסר זאת."
             % (pc(M["pti_avg"]), pc(PTI[(30, 40)], 1), "30%", "40%", pc(PTI[(40, 50)], 1), "40%", "50%"))
         + fig(v2_pti(), "הקו המקווקו הכחול הוא הממוצע. מעל 40%% הבנק נדרש להחזיק יותר הון כנגד ההלוואה, ומעל 50%% אסור לאשר משכנתא (הוראה 329, סעיפים 5 ו-6). מקור: בנק ישראל, %s." % M8)
         + T9A
         + "<h3>שיעור המימון</h3>\n"
         + p("%s מהכסף ניתן במימון של 60%% עד 75%% משווי הדירה, עד התקרה של דירה יחידה. מעל 75%% ניתנו %s בלבד. במחשבון, אחרי שמקלידים מחיר והכנסה, רואים איפה אתם בשתי ההתפלגויות."
             % (pc(LTVB[(60, 75)], 1), pc(over75, 2)))
         + fig(v3_ltv(), "הקווים הם תקרות המימון של בנק ישראל: 50%% בדירה להשקעה, 70%% בדירה חליפית ו-75%% בדירה יחידה (הוראה 329, סעיף 2). מקור: בנק ישראל, %s." % M8)
         + T9B)

# --- 8. average rates by track and by term (T2, T3a, T3b, V4)
hist = lambda k: {ym: v for ym, v in RT[k]["hist"]}
MS = [ym for ym, _ in RT["fixed_nl"]["hist"]]
T2 = table("ריבית ממוצעת במשכנתאות חדשות לפי מסלול", "שלושת החודשים האחרונים שפורסמו, ותקופה ממוצעת לפירעון באותו חודש. מקור: בנק ישראל, הלוואות חדשות לדיור (SDMX BIR_MRTG_99).",
           ["מסלול"] + [mon(m) for m in MS] + ["תקופה ממוצעת, ב%s" % M8],
           [["קבועה לא צמודה (%s)" % KLZ] + [pc(hist("fixed_nl")[m]) for m in MS] + ["%s שנים" % num(M["term_nl"], 1)],
            ["קבועה צמודה (%s)" % KZ] + [pc(hist("fixed_cpi")[m]) for m in MS] + ["%s שנים" % num(M["term_cpi_fixed"], 1)],
            ["משתנה צמודה (ב%s: עוגן %s ועוד מרווח %s)" % (M8, pc(RT["var_cpi"]["bench"]), pc(RT["var_cpi"]["margin"]))] + [pc(hist("var_cpi")[m]) for m in MS] + ["%s שנים" % num(M["term_cpi_var"], 1)]],
           num_cols=(1, 2, 3, 4))


def t3(blk, title, file_):
    rows = [["ממוצע כל התקופות", pc(blk["avg_eff"]), pc(blk["avg_nom"])]] + [[b["label"], pc(b["eff"]), pc(b["nom"])] for b in blk["buckets"]]
    return table(title, "בתוקף מ-%s, חודש הדיווח %s. מקור: בנק ישראל, %s. הנומינלית מחושבת מהאפקטיבית לפי תשלום חודשי." % (dt(blk["inforce"]), mon(blk["month"][:7]), file_),
                 ["התקופה לפירעון", "ריבית אפקטיבית", "ריבית נומינלית"], rows, num_cols=(1, 2))


nl_peak = max(TN["hist"], key=lambda x: x[1])
S8 = sec("average-mortgage-rates", "ריבית משכנתא ממוצעת לפי מסלול ולפי תקופה",
         p("בנק ישראל מפרסם כל חודש את הריבית הממוצעת במשכנתאות החדשות לפי מסלול. ב%s: %s ב%s, %s ב%s ו-%s במשתנה צמודה. לפריים בנק ישראל לא מפרסם ממוצע נפרד."
           % (M8, pc(FIX), KLZ, pc(FIXC), KZ, pc(VARC)))
         + T2
         + "<h3>ריבית ממוצעת לפי התקופה לפירעון</h3>\n"
         + p("בנוסף, בנק ישראל מפרסם ריבית ממוצעת לפי התקופה לפירעון, בנפרד למשכנתאות לא צמודות ולצמודות. לפי הריביות האלה מחשבים עמלת פירעון מוקדם, והן בתוקף מ-%s. "
             "הקובץ נותן ריבית אפקטיבית; לצידה מופיעה הנומינלית, הריבית השנתית שמחלקים לתשלומים חודשיים, כמו בלוח שפיצר. במסלול משתנה התקופה היא עד שינוי הריבית." % INF)
         + t3(TN, "ריבית ממוצעת במשכנתאות לא צמודות לפי תקופה", "mashfix.xls")
         + t3(TC, "ריבית ממוצעת במשכנתאות צמודות למדד לפי תקופה", "pribmash.xls")
         + "<h3>הריבית לאורך השנים</h3>\n"
         + p("הממוצע הלא צמוד הגיע לשיא של %s ב%s, ומאז ירד ל-%s ב%s. הממוצע הצמוד עמד על %s באותו חודש. לריבית בנק ישראל ולפריים לאורך זמן: %s."
             % (pc(nl_peak[1]), mon(nl_peak[0]), pc(TN["hist"][-1][1]), mon(TN["hist"][-1][0]), pc(TC["hist"][-1][1]), a("rates", "ריבית משכנתא היום")))
         + fig(v4_history(), "ממוצע חודשי, ריבית אפקטיבית: לא צמודה מ%s, צמודה מ%s. ריבית בנק ישראל מינואר 2015, והנקודה בסוף היא תחזית חטיבת המחקר מ-%s: %s בממוצע ברבע השלישי של 2027. מקור: בנק ישראל (mashfix.xls, pribmash.xls, MNT_RIB_BOI_D)."
               % (mon(TN["hist"][0][0]), mon(TC["hist"][0][0]), dt(F["published"]), pc(F["rate_q3_2027"], 1))))
reg("ינואר 2015")

# --- 9. payment for 1M, 1.5M, 2M (T6, T6b)
TERMS = [15, 20, 25, 30]
RATES = [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
T6 = table("החזר חודשי על משכנתא של %s ₪ לפי ריבית ותקופה" % ils(MIL), "בשקלים, לוח שפיצר, ריבית קבועה בלי הצמדה. חישוב שלנו לפי הנוסחה שבסעיף שפיצר.",
           ["ריבית שנתית"] + ["%d שנה" % y for y in TERMS],
           [[pc(r)] + [ils(pmt(MIL, r, y * 12)) for y in TERMS] for r in RATES], num_cols=(1, 2, 3, 4))
AMTS = [1000000, 1200000, 1500000, 2000000]
T6B = table("החזר חודשי לפי סכום המשכנתא, בריבית %s" % pc(FIX), "בשקלים, לוח שפיצר. %s הוא הממוצע ב%s במשכנתאות החדשות של %s (בנק ישראל)." % (pc(FIX), KLZ, M8),
            ["סכום המשכנתא"] + ["%d שנה" % y for y in TERMS] + ["סך הריבית ב-25 שנה"],
            [[ils(x) + " ₪"] + [ils(pmt(x, FIX, y * 12)) for y in TERMS] + [ils(pmt(x, FIX, 300) * 300 - x)] for x in AMTS], num_cols=(1, 2, 3, 4, 5))
for y in TERMS: reg("%d שנה" % y)
d_half = pmt(MIL, 5.0, 300) - pmt(MIL, 4.5, 300)
i30 = pmt(MIL, FIX, 360) * 360 - MIL
S9 = sec("payment-per-million", "כמה ההחזר על משכנתא של מיליון, מיליון וחצי ושני מיליון",
         p("התשובה המהירה: משכנתא של %s ₪ ל-25 שנה בריבית %s, הממוצע ב%s ב%s, עולה %s ₪ בחודש בלוח שפיצר, ובסך הכל משלמים %s ₪ ריבית. "
           "הארכה ל-30 שנה מורידה את ההחזר ל-%s ₪, אבל מוסיפה %s ₪ ריבית." % (ils(MIL), pc(FIX), KLZ, M8, ils(S25["first"]), ils(S25["interest"]), ils(pmt(MIL, FIX, 360)), ils(i30 - S25["interest"])))
         + T6
         + p("כל חצי אחוז מורגש: על %s ₪ ל-25 שנה, ההפרש בין %s ל-%s הוא %s ₪ בחודש, %s ₪ לאורך כל התקופה." % (ils(MIL), pc(4.5), pc(5.0), ils(d_half), ils(d_half * 300)))
         + T6B)

# --- 10. the three uniform baskets (T5)
mixdesc = {"b1": "כל ההלוואה בקבועה לא צמודה", "b2": "שליש קבועה לא צמודה, שליש פריים, שליש משתנה כל 5 שנים צמודה", "b3": "חצי קבועה לא צמודה, חצי פריים"}
T5 = table("שלושת הסלים האחידים: החזר ראשון על %s ₪" % ils(MIL),
           "בשקלים, לוח שפיצר, בריביות הממוצעות: %s %s (%s), פריים %s (הממוצע הנומינלי להלוואות לא צמודות שהריבית בהן משתנה עד שנה, כולל פריים, בתוקף מ-%s), משתנה צמודה %s לפני הצמדה. בלי שינוי בפריים ובלי עליית מדד. ההרכב לפי הוראה 451, חוזר 2694."
           % (KLZ, pc(FIX), M8, pc(PRIMEAVG), INF, pc(VARC)),
           ["הסל וההרכב", "20 שנה", "25 שנה", "30 שנה", "סך הריבית ב-25 שנה"],
           [[x["label"] + "<small>%s</small>" % mixdesc[x["k"]]] + [ils(basket(x["k"], y)) for y in (20, 25, 30)] + [ils(basket_interest(x["k"], 25))] for x in D["baskets"]["list"]],
           num_cols=(1, 2, 3, 4))
reg("סל אחיד 1 סל אחיד 2 סל אחיד 3")
S10 = sec("uniform-baskets", "שלושת הסלים האחידים של בנק ישראל",
          p("בכל אישור עקרוני הבנק חייב להציג שלושה תמהילים אחידים, כדי שאפשר יהיה להשוות בין בנקים. סל 1: כל ההלוואה בריבית קבועה לא צמודה. סל 2: שליש קבועה לא צמודה, "
            "שליש פריים ושליש משתנה כל 5 שנים צמודה למדד. סל 3: חצי קבועה לא צמודה וחצי פריים. הבנק מציג אותם בלוח שפיצר, לתקופה של 10, 15, 20, 25 או 30 שנה, עם הריבית "
            "הכוללת הצפויה, סך ההחזר הצפוי וההחזר החודשי הגבוה הצפוי (הוראה 451, חוזר 2694, בתוקף מ-31.8.2022).")
          + T5
          + p("בריביות של היום סל 2 נותן את ההחזר הראשון הנמוך ביותר, %s ₪ ל-25 שנה, כי שליש ממנו צמוד למדד ושליש בפריים. הוא גם החשוף ביותר: החלק הצמוד גדל עם המדד, "
              "והפריים זז עם כל החלטת ריבית. במחשבון למעלה כל סל נפתח בלחיצה, עם ההחזר הגבוה הצפוי לפי תחזית בנק ישראל." % ils(basket("b2", 25))))

# --- 11. what the Bank of Israel allows (T4)
T4 = table("כללי בנק ישראל למשכנתא", "הוראת ניהול בנקאי תקין 329, גרסה 12 (8.2.2026) וגרסה 13 (30.6.2026), והשאלות והתשובות להוראה.",
           ["הכלל", "מה מותר", "הסעיף"],
           [["שיעור מימון, דירה יחידה", "עד %s משווי הדירה" % pc(RU["ltv"]["single"] * 100, 0), "סעיף 2"],
            ["שיעור מימון, דירה חליפית", "עד %s" % pc(RU["ltv"]["replace"] * 100, 0), "סעיף 2"],
            ["שיעור מימון, דירה להשקעה", "עד %s. מי שאינו אזרח ישראלי לא נחשב בעל דירה יחידה, ולכן גם לו עד %s" % (pc(RU["ltv"]["invest"] * 100, 0), pc(RU["ltv"]["invest"] * 100, 0)), "סעיף 2"],
            ["דירה במחיר מופחת (מחיר למשתכן, מחיר מטרה)", RU["reduced"]["text"], "סעיף 4א"],
            ["החזר מההכנסה", "עד %s מההכנסה הפנויה. מעל %s הבנק נדרש להחזיק יותר הון כנגד ההלוואה (משקל סיכון של 100%%)" % (pc(RU["pti_max"] * 100, 0), pc(RU["pti_risk"] * 100, 0)), "סעיפים 5 ו-6"],
            ["ההכנסה הפנויה", "נטו, פחות התחייבויות קבועות ל-18 חודשים, מזונות ושכר דירה אם לא עוברים לגור בדירה. מחצית מהכנסת ערב מדרגה ראשונה יכולה להיחשב, ובן זוג שגר עם הלווה במלואה", "נספח א"],
            ["ריבית משתנה", "עד %s מההלוואה, כלומר לפחות שליש בריבית קבועה" % pc(RU["variable_max"] * 100, 2), "סעיף 7"],
            ["תקופה", "עד %d שנה" % RU["term_max"], "סעיף 8"],
            ["מחזור", "לא יוצר חריגה מהכללים ולא מגדיל חריגה קיימת", "סעיף 9"],
            ["הלוואה לכל מטרה", "עד %s משווי הדירה, ועד %s אם החלק שמעל %s הוא עד %s ₪" % (pc(RU["any_purpose"]["ltv"] * 100, 0), pc(RU["any_purpose"]["ltv_upto"] * 100, 0), pc(RU["any_purpose"]["ltv"] * 100, 0), ils(RU["any_purpose"]["above_cap"])), "סעיפים 4 ו-10א"],
            ["פטור ממגבלת ההחזר", "הלוואת גישור לתקופה של עד 3 שנים; הלוואה לכל מטרה עד 120,000 ₪", "סעיפים 11 ו-12"],
            ["בנייה עצמית וקבוצת רכישה", "השווי לצורך המימון הוא הנמוך מהשמאות ומהעלות הצפויה, בלי רווח יזמי ובלי עליית ערך צפויה", "שאלות ותשובות, 2.18"]])
S11 = sec("bank-of-israel-rules", "מה בנק ישראל מתיר: מימון, החזר מהכנסה, תמהיל ותקופה",
          p("ארבעה כללים של הוראת ניהול בנקאי תקין 329 קובעים כמה משכנתא אפשר לקבל ובאיזה מבנה: שיעור המימון, ההחזר מההכנסה, החלק בריבית משתנה והתקופה. בכלל התמהיל "
            "חשוב לדייק: יש אתרים שעדיין מתארים מגבלה ישנה על מסלולים שהריבית בהם משתנה בתוך פחות מחמש שנים. לפי ההוראה בגרסתה הנוכחית, המגבלה היא על כל החלק המשתנה יחד, "
            "פריים ומשתנה כל 5 שנים: עד %s מההלוואה, כלומר לפחות שליש בריבית קבועה. המחשבון בודק את ארבעת הכללים ומסביר במילים כשמשהו חורג." % pc(RU["variable_max"] * 100, 2))
          + T4
          + p("לחישוב לפי ההכנסה וההון העצמי שלכם: %s. עוד על התקרה לפי סוג הדירה: %s. הלוואה על דירה שכבר בבעלותכם: %s. מי שמוכר דירה וקונה אחרת: %s."
              % (a("capacity", "כמה משכנתא אפשר לקחת"), a("ltv", "אחוז מימון"), a("any", "משכנתא לכל מטרה"), a("bridge", "הלוואת גישור"))))

# --- 12. Spitzer, equal principal, balloon, grace (T8)
T8 = table("שיטות ההחזר על %s ₪ ל-25 שנה בריבית %s" % (ils(MIL), pc(FIX)), "בשקלים. חישוב שלנו על אותו סכום, אותה ריבית ואותה תקופה; הגרייס בתוך 25 השנים. %s הוא הממוצע ב%s ב%s (בנק ישראל)." % (pc(FIX), KLZ, M8),
           ["השיטה", "החזר בחודש הראשון", "החזר בחודש האחרון", "סך הריבית", "סך כל התשלומים"],
           [["שפיצר", ils(S25["first"]), ils(S25["last"]), ils(S25["interest"]), ils(S25["total"])],
            ["קרן שווה", ils(E25["first"]), ils(E25["last"]), ils(E25["interest"]), ils(E25["total"])],
            ["גרייס חלקי של 12 חודשים, ואז שפיצר", ils(GP["first"]), ils(GP["last"]), ils(GP["interest"]), ils(GP["total"])],
            ["גרייס מלא של 12 חודשים, ואז שפיצר", "אין תשלום", ils(GF["last"]), ils(GF["interest"]), ils(GF["total"])],
            ["בוליט: ריבית בלבד, הקרן בסוף", ils(BU["first"]), ils(BU["last"]), ils(BU["interest"]), ils(BU["total"])],
            ["בלון: הכל בסוף", "אין תשלום", ils(BA["last"]), ils(BA["interest"]), ils(BA["total"])]], num_cols=(1, 2, 3, 4))
S12 = sec("spitzer-equal-balloon-grace", "שפיצר, קרן שווה, בלון וגרייס",
          p("בלוח שפיצר ההחזר החודשי קבוע. בהתחלה רובו ריבית, ועם הזמן חלק הקרן גדל: בחודש הראשון %s ₪ מתוך %s ₪ הם ריבית. בקרן שווה מחזירים כל חודש אותו סכום קרן, "
            "ולכן ההחזר מתחיל גבוה ויורד. בבוליט משלמים כל חודש רק ריבית ומחזירים את הקרן בסוף, ובבלון לא משלמים עד הסוף, והריבית מצטרפת לקרן. גרייס הוא תקופה בתחילת "
            "ההלוואה שבה משלמים רק ריבית (גרייס חלקי) או לא משלמים כלל (גרייס מלא)." % (ils(MIL * FIX / 1200.0), ils(S25["first"])))
          + p("ההחזר בשפיצר: סכום ההלוואה כפול הריבית החודשית, חלקי אחד פחות (אחד ועוד הריבית החודשית) בחזקת מינוס מספר החודשים. הריבית החודשית היא הריבית השנתית חלקי 12.")
          + T8
          + p("בקרן שווה משלמים %s ₪ פחות ריבית מאשר בשפיצר, אבל ההחזר הראשון גבוה ב-%s ₪. בלון ובוליט מתאימים בעיקר לתקופה קצרה, למשל עד מכירת דירה קיימת: בוליט ל-3 שנים על %s ₪ "
              "באותה ריבית עולה %s ₪ בחודש וריבית של %s ₪, ובלון ל-3 שנים נגמר בתשלום אחד של %s ₪. הלוואת גישור לתקופה של עד 3 שנים פטורה ממגבלת ההחזר מההכנסה (הוראה 329, סעיף 11). "
              "פרטים: %s · %s."
              % (ils(rnd(S25["interest"]) - rnd(E25["interest"])), ils(rnd(E25["first"]) - rnd(S25["first"])), ils(MIL), ils(BU3["first"]), ils(BU3["interest"]), ils(BA3["last"]), a("bridge", "הלוואת גישור"), a("grace", "גרייס במשכנתא"))))
reg("12 חודשים")

# --- 13. CPI, prime and what is expected
path = P["path2026"]
assert len(path) == 4 and all(path[i][1] < path[i - 1][1] for i in range(1, 4)) and path[-1][1] == P["rate"], path  # "ירדה השנה ארבע פעמים"
assert [c for c in BR["changes"] if c["from"] < "2026-01-01"][-1]["rate"] > path[0][1]
CPIP = MX[2]
S13 = sec("cpi-prime-forecast", "מדד, פריים ומה צפוי בריבית",
          p("מדד המחירים לצרכן עלה ב-%s ב-12 החודשים שעד %s. ריבית בנק ישראל ירדה השנה ארבע פעמים: %s, והפריים ירד איתה ל-%s."
            % (pc(C["y12"], 1), CPI_M, ", ".join("ל-%s ב-%s" % (pc(r_), dt(d_)) for d_, r_ in path[:-1]) + " ול-%s ב-%s" % (pc(path[-1][1]), dt(path[-1][0])), pc(P["prime"])))
          + p("תחזית חטיבת המחקר של בנק ישראל מ-%s: ריבית של %s בממוצע ברבע השלישי של 2027, ואינפלציה של %s בארבעת הרבעונים הבאים (%s ב-2026 ו-%s ב-2027). "
              "השווקים צופים ריבית של %s ואינפלציה של %s, והחזאים הפרטיים ריבית של %s (בין %s ל-%s) ואינפלציה של %s. ההחלטה הבאה על הריבית: %s."
              % (dt(F["published"]), pc(F["rate_q3_2027"], 1), pc(F["inflation_4q"], 1), pc(F["inflation_2026"], 1), pc(F["inflation_2027"], 1), pc(F["market_rate"], 1), pc(F["market_inflation"], 1),
                 pc(F["private_rate"], 1), pc(F["private_rate_range"][0], 1), pc(F["private_rate_range"][1], 1), pc(F["private_inflation"], 1), dt(F["next_decision"])))
          + p("מה זה אומר על המשכנתא: במסלול צמוד הקרן מוצמדת למדד בכל חודש, וההחזר גדל איתה. דוגמה מהתמהיל שהמחשבון פותח בו: %s ₪ במשתנה צמודה ל-25 שנה בריבית %s. "
              "במדד של %s בשנה, תחזית בנק ישראל, ההחזר מתחיל ב-%s ₪ ומגיע ל-%s ₪ בחודש האחרון, וההצמדה מוסיפה לקרן %s ₪ לאורך ההלוואה, אם הריבית במסלול לא משתנה."
              % (ils(200000), pc(VARC), pc(F["inflation_4q"], 1), ils(CPIP["first"]), ils(CPIP["last"]), ils(CPIP["link"])))
          + p("בפריים כל שינוי בריבית בנק ישראל עובר להחזר. הפריים הוא ריבית בנק ישראל ועוד %s, ולכן אם הריבית תגיע ל-%s כמו בתחזית, הפריים יעמוד על %s. במחשבון בוחרים "
              "את מסלול הפריים: ללא שינוי, לפי תחזית בנק ישראל, לפי ציפיות השוק, או עלייה של 2%%. להצמדת סכום למדד: %s."
              % (pc(P["prime"] - P["rate"], 1), pc(F["rate_q3_2027"], 1), pc(F["rate_q3_2027"] + P["prime"] - P["rate"], 1), a("cpi", "מחשבון הצמדה למדד"))))

# --- 14. early repayment and refinance (T7)
T7 = table("עמלות פירעון מוקדם של משכנתא", "צו הבנקאות (פירעון מוקדם של הלוואה לדיור), התשס%sב-2002, שתוקן ב-2014, סעיפים 2 עד 8 ו-10." % GER,
           ["העמלה", "מתי גובים אותה", "כמה"],
           [["עמלה תפעולית", "בכל פירעון מוקדם", "עד %s ₪" % ils(FE["operational_max"])],
            ["עמלת הודעה מוקדמת", "כשההודעה לבנק ניתנת פחות מ-%d ימים לפני הפירעון. לא נגבית כשהבנק עצמו ממחזר את ההלוואה, או כשהלווה נפטר" % FE["notice_days"], pc(FE["notice_rate"] * 100, 1) + " מהסכום"],
            ["עמלת היוון", "במסלול בריבית קבועה, כשהריבית הממוצעת ביום הפירעון נמוכה מהריבית בהלוואה. לפי הנמוך משני חישובים שבצו", "לפי החישוב, בהנחה של %s אחרי %d שנים ושל %s אחרי %d שנים"
             % (pc(FE["reduce"][0]["cut"] * 100, 0), FE["reduce"][0]["after_years"], pc(FE["reduce"][1]["cut"] * 100, 0), FE["reduce"][1]["after_years"])],
            ["הלוואה משלימה", "הנחה בעמלת ההיוון", ", ".join("%s אחרי %s" % (pc(x["cut"] * 100, 0), {1: "שנה", 2: "שנתיים"}.get(x["after_years"], "%d שנים" % x["after_years"])) for x in FE["reduce_complementary"][:-1])
             + " ו-%s אחרי %d שנים" % (pc(FE["reduce_complementary"][-1]["cut"] * 100, 0), FE["reduce_complementary"][-1]["after_years"])],
            ["פריים ומסלול שמשתנה לפחות פעם בשנה", "הריבית משתנה לפחות פעם ב-12 חודשים או במועד לא ידוע; וגם ביום שינוי ריבית בכל מסלול", "ללא עמלת היוון"],
            ["מסלול צמוד למדד", "בפירעון בין ה-1 ל-15 בחודש", "מחצית השינוי הממוצע במדד ב-12 המדדים האחרונים: %s מהסכום לפי המדדים עד %s" % (pc(C["avg_m12"] / 2.0, 3), CPI_M)],
            ["הלוואה מכוונת (זכאות)", "בכל מועד", "ללא עמלה ובלי הודעה מוקדמת"]])
S14 = sec("early-repayment-refinance", "פירעון מוקדם ומחזור",
          p("מותר לפרוע משכנתא לפני הזמן, כולה או חלקה, והעמלות קבועות בצו הבנקאות משנת 2002, שתוקן ב-2014. אפשר להודיע לבנק עד %d ימים מראש." % FE["notice_max_days"])
          + T7
          + p("עמלת ההיוון נמדדת מול הריביות הממוצעות לפי תקופה שבטבלה למעלה. כשהריביות הממוצעות יורדות מתחת לריבית שלכם במסלול הקבוע, העמלה עולה. במחשבון מוסיפים פירעון "
              "עתידי, בוחרים קיצור תקופה או הקטנת החזר, ורואים הערכה של העמלה.")
          + p("מחזור משכנתא לא יכול ליצור חריגה מכללי בנק ישראל או להגדיל חריגה קיימת (הוראה 329, סעיף 9). לבדיקה אם מחזור משתלם לכם: %s." % a("refi", "מחזור משכנתא")))

REL = ('<div class="nlu1-rel"><h3>מחשבונים קרובים</h3>\n'
       + p(" · ".join([a("reverse", "מחשבון משכנתא הפוכה"), a("capacity", "כמה משכנתא אפשר לקחת"), a("ltv", "אחוז מימון"), a("rates", "ריבית משכנתא היום"),
                        a("any", "משכנתא לכל מטרה"), a("bridge", "הלוואת גישור"), a("ptax", "מחשבון מס רכישה"), a("pcost", "עלות רכישה כוללת")])) + "</div>\n")
META = ('<p class="nlu1-meta">איך חישבנו: ההחזרים בלוח שפיצר לפי הנוסחה שבעמוד, ריבית חודשית היא הריבית השנתית חלקי 12; בקרן שווה הקרן מתחלקת שווה בין החודשים; '
        'במסלול צמוד הקרן מוצמדת למדד בכל חודש. הריבית הנומינלית מחושבת מהאפקטיבית לפי תשלום חודשי. המקורות: %s · %s · %s · %s · %s · %s · %s · '
        'הוראת ניהול בנקאי תקין 329 (גרסה 13, 30.6.2026) · צו הבנקאות (פירעון מוקדם של הלוואה לדיור), 2002 · תחזית חטיבת המחקר של בנק ישראל, %s. עודכן %s.</p>\n'
        % (ax("sdmx", "בנק ישראל, הלוואות חדשות לדיור"), ax("boirate", "ריבית בנק ישראל"), ax("mashfix", "ריבית ממוצעת לפי תקופה, לא צמודה"), ax("pribmash", "ריבית ממוצעת לפי תקופה, צמודה"),
           ax("cbs", "הלשכה המרכזית לסטטיסטיקה, מדד 120010"), ax("d451", "הוראה 451"), ax("boi_rates", "ריביות ועמלות פירעון בבנק ישראל"), dt(F["published"]), reg(UPDATED)))

NEW_BLOCK = '<div class="wrap nlu1">\n' + S5 + S6 + S7 + S8 + S9 + S10 + S11 + S12 + S13 + S14 + REL + META + "</div>\n"

# --- FAQ: 25 more (8.8; 25 and 29 are the existing "short or long" and "refinance" questions, 21 is folded into 20)
b2k = lambda k: ils(basket(k, 25))
loan6000 = 6000 * (1 - (1 + FIX / 1200.0) ** -300) / (FIX / 1200.0)
QA = [
    ("מה זה מחשבון משכנתא ואיך משתמשים בו?",
     "מחשבון משכנתא מחשב כמה תחזירו בכל חודש וכמה תשלמו בסך הכל, לפי סכום ההלוואה, הריבית, התקופה ושיטת ההחזר. מקלידים סכום, בוחרים מסלולים או אחד משלושת הסלים "
     "האחידים, ורואים את ההחזר הראשון, את ההחזר הגבוה הצפוי, את סך הריבית ואת ההצמדה. הריביות במחשבון נפתחות בממוצעים שבנק ישראל פרסם (%s, ולפי תקופה מ-%s)." % (M8, INF)),
    ("איך מחשבים החזר חודשי של משכנתא?",
     "בלוח שפיצר: סכום ההלוואה כפול הריבית החודשית, חלקי אחד פחות (אחד ועוד הריבית החודשית) בחזקת מינוס מספר החודשים. על %s ₪ ל-25 שנה בריבית %s, הממוצע ב%s ב%s, "
     "ההחזר %s ₪ בחודש. בקרן שווה ההחזר מתחיל ב-%s ₪ ויורד עד %s ₪." % (ils(MIL), pc(FIX), KLZ, M8, ils(S25["first"]), ils(E25["first"]), ils(E25["last"]))),
    ("כמה החזר חודשי על משכנתא של מיליון שקל?",
     "בריבית %s, הממוצע ב%s ב%s, בלוח שפיצר: %s ₪ ל-15 שנה, %s ₪ ל-20 שנה, %s ₪ ל-25 שנה ו-%s ₪ ל-30 שנה. הטבלה בעמוד מראה כל ריבית מ-%s עד %s."
     % (pc(FIX), KLZ, M8, ils(pmt(MIL, FIX, 180)), ils(pmt(MIL, FIX, 240)), ils(pmt(MIL, FIX, 300)), ils(pmt(MIL, FIX, 360)), pc(RATES[0]), pc(RATES[-1]))),
    ("כמה החזר חודשי על משכנתא של %s מיליון שקל?" % mil(1200000),
     "בריבית %s (%s) ול-25 שנה: %s ₪ בחודש בלוח שפיצר. בתמהיל שהמחשבון פותח בו, %s ₪ בשלושה מסלולים עם מדד של %s בשנה, ההחזר הראשון %s ₪ וההחזר הגבוה הצפוי %s ₪."
     % (pc(FIX), M8, ils(r25(1200000)), ils(1200000), pc(F["inflation_4q"], 1), ils(MIX_FIRST), ils(MIX_MAX))),
    ("כמה החזר חודשי אקבל על משכנתא של 2 מיליון ש%sח?" % GER,
     "בריבית %s (%s), בלוח שפיצר: %s ₪ ל-25 שנה ו-%s ₪ ל-30 שנה. לשם השוואה, המשכנתא הממוצעת ב%s הייתה %s ₪. כדי לקבל %s ₪ בדירה יחידה, הדירה צריכה להיות שווה לפחות %s ₪, "
     "כי המימון מוגבל ל-%s." % (pc(FIX), M8, ils(r25(2000000)), ils(pmt(2000000, FIX, 360)), M8, ils(M["avg_loan"]), ils(2000000), ils(2000000 / RU["ltv"]["single"]), pc(RU["ltv"]["single"] * 100, 0))),
    ("איך מחשבים משכנתא לפי החזר חודשי שאני יכול לשלם?",
     "הופכים את הנוסחה: ההחזר החודשי כפול אחד פחות (אחד ועוד הריבית החודשית) בחזקת מינוס מספר החודשים, חלקי הריבית החודשית. החזר של %s ₪ ל-25 שנה בריבית %s (%s) "
     "מממן %s ₪. במחשבון בוחרים לפי החזר חודשי, והסכום מחושב לפי התמהיל שלכם." % (ils(6000), pc(FIX), M8, ils(loan6000))),
    ("כמה משכנתא אפשר לקחת?",
     "שני כללים של בנק ישראל קובעים את התקרה: שיעור המימון, עד %s משווי דירה יחידה, %s בדירה חליפית ו-%s בדירה להשקעה, וההחזר מההכנסה, עד %s מההכנסה הפנויה "
     "(הוראה 329, גרסה 13, 30.6.2026). לחישוב לפי ההכנסה וההון העצמי שלכם: %s."
     % (pc(75, 0), pc(70, 0), pc(50, 0), pc(50, 0), a("capacity", "כמה משכנתא אפשר לקחת"))),
    ("כמה כסף צריך להרוויח כדי לקבל משכנתא?",
     "ההחזר לא יכול לעלות על %s מההכנסה הפנויה, ומעל %s הבנק נדרש להחזיק יותר הון כנגד ההלוואה. להחזר של %s ₪ (%s ₪ ל-25 שנה ב-%s): בתקרה של %s צריך הכנסה פנויה "
     "של %s ₪, ב-%s צריך %s ₪, וביחס הממוצע של %s, %s, צריך %s ₪."
     % (pc(50, 0), pc(40, 0), ils(S25["first"]), ils(MIL), pc(FIX), pc(50, 0), ils(S25["first"] / 0.5), pc(40, 0), ils(S25["first"] / 0.4), M8, pc(M["pti_avg"]), ils(S25["first"] / (M["pti_avg"] / 100.0)))),
    ("כמה הון עצמי נדרש כדי לקבל משכנתא?",
     "לפחות %s מהשווי בדירה יחידה, %s בדירה חליפית ו-%s בדירה להשקעה, כי אלה תקרות המימון של בנק ישראל (הוראה 329, סעיף 2). בדירה של %s ₪ כדירה יחידה: לפחות %s ₪. "
     "מעבר לזה צריך כסף למס רכישה, עורך דין ושאר עלויות הקנייה: %s · %s."
     % (pc(100 - RU["ltv"]["single"] * 100, 0), pc(100 - RU["ltv"]["replace"] * 100, 0), pc(100 - RU["ltv"]["invest"] * 100, 0), ils(2000000), ils(2000000 * (1 - RU["ltv"]["single"])), a("ptax", "מחשבון מס רכישה"), a("pcost", "עלות רכישה כוללת"))),
    ("האם אפשר לקחת משכנתא בלי הון עצמי?",
     "לא במשכנתא על הדירה שקונים: בנק ישראל מתיר מימון של עד %s בדירה יחידה, כך שלפחות רבע מהשווי בא מכסף שלכם. בדירה במחיר מופחת השווי יכול להתבסס על הערכת שמאי, "
     "עד %s מיליון ₪ או מחיר הרכישה אם הוא גבוה יותר, והקונה משלם מכספו לפחות %s ₪, או %s ₪ בדירה שניתן עליה מענק מחיר למשתכן החדש (הוראה 329, סעיף 4א, גרסה 12, 8.2.2026). "
     "על ההגרלות: %s." % (pc(75, 0), mil(RU["reduced"]["value_cap"]), ils(RU["reduced"]["own_min"]), ils(RU["reduced"]["own_min_grant"]), a("dira", "דירה בהנחה"))),
    ("כמה אחוז מהמשכורת יכול לצאת על משכנתא?",
     "עד %s מההכנסה הפנויה, לפי הוראה 329. מעל %s הבנק נדרש להחזיק יותר הון כנגד ההלוואה. ב%s, %s מסכום המשכנתאות החדשות ניתן בהחזר של %s עד %s מההכנסה, ורק %s מעל %s. "
     "ההחזר הממוצע: %s." % (pc(50, 0), pc(40, 0), M8, pc(PTI[(30, 40)], 1), pc(30, 0), pc(40, 0), pc(PTI[(40, 50)], 1), pc(40, 0), pc(M["pti_avg"]))),
    ("מה ההבדל בין מסלולי משכנתא?",
     "מסלול מוגדר לפי שתי שאלות: האם הריבית קבועה או משתנה, והאם הקרן צמודה למדד. %s: קבועה לא צמודה, ההחזר ידוע מראש. %s: קבועה צמודה, הריבית נמוכה יותר אבל הקרן "
     "גדלה עם המדד. פריים: משתנה עם ריבית בנק ישראל. משתנה כל 5 שנים: הריבית מתעדכנת בתחנות, צמודה או לא צמודה. ב%s הריבית הממוצעת הייתה %s ב%s, %s ב%s ו-%s במשתנה צמודה."
     % (KLZ, KZ, M8, pc(FIX), KLZ, pc(FIXC), KZ, pc(VARC))),
    ("מה ההבדל בין %s לפריים?" % KLZ,
     "ב%s הריבית קבועה לכל התקופה, וב%s הממוצע היה %s. בפריים הריבית היא הפריים ועוד או פחות מרווח, והיא זזה עם כל החלטה של בנק ישראל; הפריים היום %s. בנק ישראל לא "
     "מפרסם ממוצע נפרד לפריים; הממוצע להלוואות לא צמודות שהריבית בהן משתנה עד שנה, כולל פריים, הוא %s נומינלית (בתוקף מ-%s). בפריים אין עמלת היוון בפירעון מוקדם."
     % (KLZ, M8, pc(FIX), pc(P["prime"]), pc(PRIMEAVG), INF)),
    ("מה זה תמהיל משכנתא ואיך בודקים אותו?",
     "תמהיל הוא החלוקה של המשכנתא בין מסלולים. בודקים שלושה דברים: שהחלק בריבית משתנה לא עולה על %s (הוראה 329, סעיף 7), מה ההחזר הגבוה הצפוי ולא רק הראשון, ומה סך "
     "התשלומים לעומת שלושת הסלים האחידים. בדיקת ההצעה שבמחשבון משווה כל מסלול לממוצע של בנק ישראל לאותו מסלול ולאותה תקופה." % pc(RU["variable_max"] * 100, 2)),
    ("מה הם שלושת הסלים האחידים של בנק ישראל?",
     "שלושה תמהילים שכל בנק חייב להציג באישור העקרוני, כדי שאפשר יהיה להשוות: סל 1, כולו קבועה לא צמודה; סל 2, שליש קבועה לא צמודה, שליש פריים ושליש משתנה כל 5 שנים צמודה; "
     "סל 3, חצי קבועה לא צמודה וחצי פריים (הוראה 451, חוזר 2694, בתוקף מ-31.8.2022). על %s ₪ ל-25 שנה, בריביות הממוצעות שבטבלה (%s ו-%s): %s, %s ו-%s ₪ בחודש הראשון."
     % (ils(MIL), M8, INF, b2k("b1"), b2k("b2"), b2k("b3"))),
    ("כמה מהמשכנתא מותר לקחת בריבית משתנה?",
     "עד %s מההלוואה, כלומר לפחות שליש בריבית קבועה (הוראה 329, סעיף 7). המגבלה חלה על כל החלק המשתנה יחד, פריים ומשתנה כל 5 שנים. ב%s, %s מסכום המשכנתאות החדשות ניתן בריבית משתנה."
     % (pc(RU["variable_max"] * 100, 2), M8, pc(TRS["var_nl"] + TRS["var_cpi"], 1))),
    ("מה ריבית הפריים היום ומתי ההחלטה הבאה?",
     "הפריים %s: ריבית בנק ישראל, %s מאז %s, ועוד %s. ב-%s הריבית נשארה ללא שינוי, וההחלטה הבאה ב-%s. תחזית בנק ישראל מאוקטובר 2026: ריבית של %s בממוצע ברבע השלישי של 2027."
     % (pc(P["prime"]), pc(P["rate"]), dt(P["from"]), pc(P["prime"] - P["rate"], 1), dt(F["published"]), dt(F["next_decision"]), pc(F["rate_q3_2027"], 1))),
    ("מה הריבית הממוצעת על משכנתא החודש?",
     "לפי הנתונים האחרונים של בנק ישראל, במשכנתאות החדשות של %s: %s בקבועה לא צמודה, %s בקבועה צמודה ו-%s במשתנה צמודה. הממוצע לפי תקופה, בתוקף מ-%s: %s בלא צמודות ו-%s בצמודות "
     "(ריבית אפקטיבית)." % (M8, pc(FIX), pc(FIXC), pc(VARC), INF, pc(TN["avg_eff"]), pc(TC["avg_eff"]))),
    ("איך אדע אם הריבית שהבנק הציע לי טובה?",
     "משווים כל מסלול לממוצע של בנק ישראל לאותו מסלול ולאותה תקופה. בבדיקת ההצעה שבמחשבון מקלידים את ההצעה ורואים את הפער באחוזים ובשקלים. דוגמה: %s ב%s על %s ₪ ל-25 שנה, "
     "מול ממוצע של %s לתקופה הזו (בתוקף מ-%s), עולה %s ₪ יותר לאורך ההלוואה. הממוצע כולל את כל הלווים, ולווה עם הכנסה יציבה ומימון נמוך יכול לקבל פחות."
     % (pc(OFF), KLZ, ils(MIL), pc(B2025["nom"]), INF, ils((off_p - avg_p) * 300))),
    ("מה זה לוח שפיצר ומה ההבדל מקרן שווה?",
     "בשפיצר ההחזר קבוע לאורך כל התקופה; בהתחלה רובו ריבית, ועם הזמן חלק הקרן גדל, ולכן ההחזר קבוע אבל חלק הריבית בו יורד. בקרן שווה הקרן מתחלקת שווה בין החודשים, "
     "וההחזר מתחיל גבוה ויורד. על %s ₪ ל-25 שנה ב-%s (%s): שפיצר %s ₪ בכל חודש וריבית של %s ₪; קרן שווה מ-%s ₪ עד %s ₪, וריבית של %s ₪."
     % (ils(MIL), pc(FIX), M8, ils(S25["first"]), ils(S25["interest"]), ils(E25["first"]), ils(E25["last"]), ils(E25["interest"]))),
    ("מה זה משכנתא בלון ובוליט ומתי משתמשים בהן?",
     "בבוליט משלמים כל חודש רק את הריבית, ואת הקרן מחזירים בסוף. בבלון לא משלמים עד הסוף, והריבית מצטרפת לקרן. הן מתאימות בעיקר לתקופה קצרה, למשל הלוואת גישור עד מכירת "
     "דירה קיימת; הלוואת גישור של עד 3 שנים פטורה ממגבלת ההחזר מההכנסה (הוראה 329, סעיף 11). על %s ₪ ל-3 שנים בריבית %s (%s): בבוליט %s ₪ בחודש, ובבלון תשלום אחד של %s ₪ בסוף."
     % (ils(MIL), pc(FIX), M8, ils(BU3["first"]), ils(BA3["last"]))),
    ("מה זה גרייס במשכנתא וכמה הוא עולה?",
     "גרייס הוא תקופה בתחילת ההלוואה בלי החזר קרן. בגרייס חלקי משלמים רק ריבית; בגרייס מלא לא משלמים, והריבית מצטרפת לקרן. על %s ₪ ל-25 שנה ב-%s (%s), שנה של גרייס חלקי "
     "מוסיפה %s ₪ לסך הריבית, ושנה של גרייס מלא מוסיפה %s ₪, לעומת שפיצר רגיל." % (ils(MIL), pc(FIX), M8, ils(GP["interest"] - S25["interest"]), ils(GF["interest"] - S25["interest"]))),
    ("איך המדד משפיע על המשכנתא שלי?",
     "במסלול צמוד הקרן מוצמדת למדד בכל חודש, וההחזר גדל איתה. המדד עלה ב-%s ב-12 החודשים שעד %s, ובנק ישראל צופה %s בארבעת הרבעונים הבאים (תחזית %s). על %s ₪ במשתנה צמודה "
     "ל-25 שנה ב-%s, מדד של %s בשנה מעלה את ההחזר מ-%s ₪ ל-%s ₪ ומוסיף לקרן %s ₪."
     % (pc(C["y12"], 1), CPI_M, pc(F["inflation_4q"], 1), dt(F["published"]), ils(200000), pc(VARC), pc(F["inflation_4q"], 1), ils(CPIP["first"]), ils(CPIP["last"]), ils(CPIP["link"]))),
    ("כמה עולה פירעון מוקדם של משכנתא?",
     "עמלה תפעולית של עד %s ₪; %s מהסכום אם ההודעה ניתנה פחות מ-%d ימים מראש; ובמסלול קבוע עמלת היוון כשהריבית הממוצעת ירדה מתחת לריבית שלכם, בהנחה של %s אחרי 3 שנים "
     "ושל %s אחרי 5 שנים. בפריים ובמסלול שמשתנה לפחות פעם בשנה אין עמלת היוון, ובהלוואת זכאות אין עמלה כלל (צו הבנקאות, 2002)."
     % (ils(FE["operational_max"]), pc(FE["notice_rate"] * 100, 1), FE["notice_days"], pc(20, 0), pc(30, 0))),
    ("האם ניתן לקבל משכנתא על נכס קיים?",
     "כן, כהלוואה לכל מטרה: עד %s משווי הדירה, ועד %s אם החלק שמעל %s הוא עד %s ₪ (הוראה 329, סעיפים 4 ו-10א). הלוואה לכל מטרה של עד %s ₪ פטורה ממגבלת ההחזר מההכנסה. "
     "פרטים: %s. למשכנתא הפוכה יש עמוד ומחשבון נפרדים: %s."
     % (pc(50, 0), pc(70, 0), pc(50, 0), ils(200000), ils(120000), a("any", "משכנתא לכל מטרה"), a("reverse", "מחשבון משכנתא הפוכה"))),
]
FAQ_ADD = "".join("<h3>%s</h3>\n<p>%s</p>\n" % qa for qa in QA)

# ------------------------------------------------------------------------------------------------ the replacements
FAQ_LAST = "<p>לא. הוא כלי ראשון בלבד. לפני קנייה צריך לבדוק אישור עקרוני, שמאות, מס רכישה, חוזה, טאבו, הוצאות נלוות ותמהיל מתאים.</p>\n</section>"
NEW_ANCHOR = '</section>\n<div class="wrap">\n<section>\n<h2>איך משתמשים במחשבון המשכנתא?</h2>'
R = [
    ("<!-- /wp:heading -->\n", "<!-- /wp:heading -->\n" + TOP),                                                     # 1. lead, CTA, tool, before nlc-mortgage
    (NEW_ANCHOR, '</section>\n' + NEW_BLOCK + NEW_ANCHOR[len('</section>\n'):]),                                   # 2. new sections after the old widgets
    (FAQ_LAST, FAQ_LAST[:-len("</section>")] + FAQ_ADD + "</section>"),                                            # 3. 25 questions at the end of the FAQ
]
LANG_FIX = [  # dna.md 9.3: banned words in old text, the same release (one word each, nothing else changes)
    ("אם הדירה מיועדת להשקעה, כדאי לעבור גם למחשבון התזרים של Nadlan ולבדוק", "אם הדירה מיועדת להשקעה, כדאי לעבור גם למחשבון התזרים באתר ולבדוק"),
    (": סימולציה מלאה שנה אחר שנה,", ": חישוב מלא שנה אחר שנה,"),
]

sys.stdout.flush()  # the deploy helper below rewraps stdout; keep what was printed so far
sys.path.insert(0, H)
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "u1page"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,title,modified" % PID)
assert s == 200, s
raw = r["content"]["raw"]
assert 'id="mortgage-tool"' not in raw and "nlu1" not in raw, "already upgraded: refuse to apply twice"
assert raw.count('id="nlc-mortgage"') == 1 and raw.count('id="nmc-loan"') == 1
old_nlc = raw[raw.index('<style>\n.nlc-calc'):raw.index('<style id="nadlan-mortgage-calculator-20260528">')]
old_nmc = raw[raw.index('<section class="calc-shell wrap"'):raw.index(NEW_ANCHOR) + len("</section>")]
old_q = re.findall(r"<h3>(.*?)</h3>", raw[raw.index('<section id="faq">'):raw.index(FAQ_LAST)] + FAQ_LAST)
new = raw
for o, n_ in R + LANG_FIX:
    c = new.count(o)
    assert c == 1, (c, o[:70])
    new = new.replace(o, n_)
print("[page %d] %s | modified %s | %d anchored replacements + %d word fixes, each matched once" % (PID, r["link"], r["modified"], len(R), len(LANG_FIX)))

# ------------------------------------------------------------------------------------------------ checks on the result
fixmap = dict(LANG_FIX)
for line in raw.split("\n"):  # additive: every original line survives (the two fixed lines in their fixed form)
    ln = line
    for o, n_ in LANG_FIX:
        ln = ln.replace(o, n_)
    assert ln in new, ("an original line is missing", line[:80])
assert old_nlc in new and old_nmc in new, "old widgets must stay untouched"
pos = [new.index(x) for x in ('<h1 ', 'class="nlu1-lead"', 'class="nlu1-cta"', 'id="mortgage-tool"', '[nadlan_tool id="mortgage"]', 'id="nlc-mortgage"', 'id="nmc-loan"',
                              'class="wrap nlu1"', "<h2>איך משתמשים במחשבון המשכנתא?</h2>", '<section id="faq">')]
assert pos == sorted(pos), ("content order", pos)
assert new.count("<h1") == 1


def visible(html, keep_svg=True):
    """Text a reader sees (SVG text and hover titles included unless keep_svg is False)."""
    h_ = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S)
    if not keep_svg:
        h_ = re.sub(r"<svg\b.*?</svg>", " ", h_, flags=re.S)
    h_ = re.sub(r"<!--.*?-->", " ", h_, flags=re.S)
    h_ = re.sub(r"\[nadlan_tool[^\]]*\]", " ", h_)
    h_ = re.sub(r"<[^>]+>", " ", h_)
    return re.sub(r"\s+", " ", h_.replace("&nbsp;", " ").replace("&quot;", '"').replace("&amp;", "&"))


ADDED = TOP + NEW_BLOCK + FAQ_ADD
ARIA = " ".join(re.findall(r'aria-label="([^"]*)"', ADDED))  # screen readers read these: same language law
vis_new = visible(ADDED) + " " + ARIA; vis_new_text = visible(ADDED, keep_svg=False); vis_all = visible(new) + " " + ARIA
BANNED = r"ממשק|מערכת|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה|טעון אימות|נדלן חכם|Nadlan|מנגנון|מודל|הדגמה|טכנולוגי|PMT|אטלס|Atlas|\bדמו\b|אפס"
for name, v in (("new content", vis_new), ("whole page content", vis_all)):
    assert not re.search(r"[–—]", v), (name, "long dash")
    assert not re.search(r"(?:^|\s)-{1,3}(?:\s|$)|--", v), (name, "spaced hyphen or double hyphen (WordPress turns it into a dash)")
    m_ = re.search(BANNED, v)
    assert not m_, (name, "banned word", m_.group(0) if m_ else "")
assert '"' not in vis_new and "'" not in vis_new, "ASCII quote in new visible text (use gershayim)"
assert "..." not in vis_new
assert not re.search(r"(?<![\d.,])0(?![\d.,])", vis_new_text), "a zero amount in visible text (the 0% baseline of the V4 axis is the only zero, inside the SVG)"
untraced = sorted({norm(tk) for tk in NUMRE.findall(vis_new)} - ALLOW)
assert not untraced, ("numbers not traceable to dna.md section 6, the data files or our computation", untraced)
dup = [q for q, _ in QA if q in old_q]
assert not dup, ("duplicate FAQ", dup)
faq_html = new[new.index('<section id="faq">'):]
faq_html = faq_html[:faq_html.index("</section>")]
faq_n = len(re.findall(r"<h3[^>]*>.*?</h3>\s*<p", faq_html, flags=re.S))
assert faq_n == 30, faq_n
hrefs = set(re.findall(r'href="(/[^"#]*)"', ADDED))
assert hrefs <= set(LINKS.values()), ("internal href not checked", hrefs - set(LINKS.values()))

WORDS = lambda v: len(re.findall(r"[\w֐-׿״׳%₪.,]+", v))
n_tables = ADDED.count("<table"); n_svg = ADDED.count("<svg")
print("[new content] %d words of text (+%d inside the 4 SVGs) | tables %d | svg %d | h2 %d | h3 %d (of them %d FAQ) | FAQ on page %d (5 kept + %d new) | numbers traced %d"
      % (WORDS(vis_new_text), WORDS(vis_new) - WORDS(vis_new_text), n_tables, n_svg, ADDED.count("<h2"), ADDED.count("<h3"), len(QA), faq_n, len(QA),
         len(set(norm(tk) for tk in NUMRE.findall(vis_new)))))
print("[whole content] %d words | tables %d | svg %d | h2 %d | h3 %d | internal links in new content %d (all 200)" % (
    WORDS(visible(new, keep_svg=False)), new.count("<table"), new.count("<svg"), new.count("<h2"), new.count("<h3"), len(re.findall(r'href="/', ADDED))))

if DRY:
    out = os.path.join(H, "preview", "u1-page-content.html")
    io.open(out, "w", encoding="utf-8", newline="").write(new)
    print("[dry] GET only, nothing written to the site | preview:", out)
    sys.exit(0)

# ------------------------------------------------------------------------------------------------ live write (coordinator only)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new})
assert s2 in (200, 201), s2
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
ok = {"read-back": back.strip() == new.strip(), "one h1": bd.count("<h1") == 1, "tool mounted": 'data-nli="mortgage"' in bd, "mortgage.js enqueued": "tools/mortgage.js" in page,
      "old nlc-mortgage kept": 'id="nlc-mortgage"' in bd, "old nmc kept": 'id="nmc-loan"' in bd, "4 svg figures": bd.count('class="nlu1-f"') == 4,
      "lead under h1": bd.index('class="nlu1-lead"') < bd.index('data-nli="mortgage"') < bd.index('id="nlc-mortgage"'),
      "one FAQPage": page.count('"@type":"FAQPage"') == 1, "30 questions": page.count('"@type":"Question"') == 30, "SoftwareApplication": '"@type":"SoftwareApplication"' in page,
      "no Nadlan / סימולציה in body text": not re.search(r"Nadlan|סימולציה", visible(bd[:bd.find("<footer")]))}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
