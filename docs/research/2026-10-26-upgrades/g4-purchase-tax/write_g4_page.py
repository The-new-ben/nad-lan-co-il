# -*- coding: utf-8 -*-
"""G4 on /purchase-tax-calculator/ (page 6): round 2 of the purchase-tax page, after the 22.10.2026 rebuild (HAD-592,
docs/research/2026-10-22-purchase-tax/build_page.py) and the 25.10.2026 extension fix (fix_ptax_extension.py). Spec: dna.md
sections 7 and 8 in this folder. Goal (Ben, 26.10.2026): win "מס רכישה" (6,600 a month, no impressions today) and climb on
"מחשבון מס רכישה" (4,400, position 55), with the tool ptax v3 (tools/ptax.js, release pending).

ADDITIVE: nothing existing is removed. Every original line of the live content must still be there afterwards (asserted), except
the four corrected sentences below, which are replaced in place:
  C1 the payment step said "איחור: קנס של 5% מהמס": no such fine in the Tax Authority's 2026 guide or instruction 1/2026; the guide
     (p.59) lists 0.2% of the tax per week of late payment (s.94b) and the declaration fine of 310 ₪ per two weeks (s.94a);
  C2 the payment step said "לא לפני 60 יום מהעסקה" as the deadline: s.90a says pay within 60 days, s.51 defers it (guide p.58);
  C3 the ledger tile said "תשלום לא לפני 60 יום": the same;
  C4 the answer paragraph said "משלמים בדרך כלל לא לפני 60 יום": the same.
What it adds:
  1. under the answer, before the tool: a CTA row (#ptax-tool, #brackets, #late) and the tool anchor;
  2. ids on two existing h2 (#brackets, #pay) for the CTA links;
  3. at the end of the 22.10 block (inside .nlag, before the old guide): seven sections with tables T1 to T5 and the infographics
     I1 to I3 (inline SVG, NadLan Instruments palette), the English aside for foreign residents, the updated line and sources;
  4. 10 questions appended to the FAQ (23 -> 33; FAQPage carries h3 + p).
Optional (--title): the Yoast title and description (dna.md 8.1; keyword guard and title-start audit results are there).

Asserts: every anchor matches once; the corrected sentences match once; every number in the new visible text is traced (the data
file, our computation, or the facts list FACTS from the official sources in dna.md section 7); language law (no long dash, no spaced
hyphen, banned words, no ASCII double quote, no zero amounts in text); one h1; content order; FAQ count; internal links answer 200
with no redirect (--links, or always in the live run).

  python docs/research/2026-10-26-upgrades/g4-purchase-tax/write_g4_page.py --local [--links]
        no network write and no credentials: applies to page-backup/page-6-reconstructed-20261025.html (the 25.10 13:01 live raw,
        rebuilt from the 25.10 backup + fix_ptax_extension.py, checked word for word against the public REST content on 26.10),
        writes preview/g4-page-content.html and preview/index.html (a local page with the real tool)
  python .../write_g4_page.py --dry [--title]     GET the live raw through the bridge (read only) and build, no write
  python .../write_g4_page.py [--title]           coordinator only: backup, POST, read-back, live check   (NOT RUN BY THE BUILDER)
"""
import html as HT, io, json, math, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
LOCAL, DRY, LINKS, TITLE = "--local" in sys.argv, "--dry" in sys.argv, "--links" in sys.argv, "--title" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 6
SITE = "https://nad-lan.co.il"
UPDATED = "26.10.2026"
RECON = os.path.join(H, "page-backup", "page-6-reconstructed-20261025.html")
RECON_MODIFIED = "2026-10-25T13:01:56"
DATA = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")
P = json.load(io.open(os.path.join(DATA, "ptax.json"), encoding="utf-8"))
V = json.load(io.open(os.path.join(DATA, "value.json"), encoding="utf-8"))
SEO_TITLE = "מחשבון מס רכישה 2026: מדרגות, הקלות ומתי משלמים"  # 26.10: no "סימולטור" (language law); guard OK
SEO_DESC = ("מחשבון מס רכישה 2026 לפי רשות המסים: דירה יחידה, נוספת, עולה, נכה, תושב חוץ ושני קונים. מדרגות, מתי משלמים, "
            "מה עולה שבוע איחור ועד מתי למכור דירה קודמת.")

# ------------------------------------------------------------------------------------------------ number provenance
NUMRE = re.compile(r"\d+(?:[.,]\d+)*")
ALLOW = set()


def norm(tok):
    return tok.replace(",", "") if re.fullmatch(r"\d{1,3}(?:,\d{3})+", tok) else tok


def reg(s):
    for tok in NUMRE.findall(str(s)):
        ALLOW.add(norm(tok))
    return s


def _allow_json(o):
    if isinstance(o, dict):
        for x in o.values(): _allow_json(x)
    elif isinstance(o, list):
        for x in o: _allow_json(x)
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        reg("%s" % o); reg("{:,}".format(o) if float(o).is_integer() else str(o))
    elif isinstance(o, str):
        reg(o)


_allow_json(P)
# official facts used in the text (dna.md section 7, each with its source there): sections, forms, days, dates, rates
FACTS = ("סעיף 9 51 73 76 90 91 94 תקנה 11 12 12א 16 20 21 טופס 7000 7013 7085 2973 6130 ימים 14 15 20 30 45 60 חודשים 8 12 18 24 שנים 2 4 7 "
         "0.2% 0.5% 3.5% 5% 6% 8% 10% 1/3 1/2 16.1.2026 15.1.2027 15.1.2028 16.1.2025 15.8.2024 1.3.2024 31.8.2026 28.2.2026 31.5.2026 "
         "1.6.2025 1.6.2023 31.5.2025 10.2.2027 31.12.2026 12.10.2026 18 1997 1.1.1997 2026 2027 2028 100,000 26.10.2026 1-3.2026 10-12.2025 "
         "7-9.2025 310 250 631,335 0.5 24 3 2,500,000 1,978,745 2,347,040 6,055,070 20,183,565 1,988,090 18.1.2026 30.3.2026 1,000")
reg(FACTS)
for c in V["cities"].values():
    for k in ("r3", "r4", "r5"): reg("{:,}".format(c[k]))
    for k in ("q", "q3", "q4", "q5"): reg(c[k])


def rnd(x):
    return int(math.floor(x + 0.5))


def ils(x):
    return reg("₪{:,}".format(rnd(x)))


def num(x):
    return reg("{:,}".format(rnd(x)))


def pc(x, d=1):
    s = ("%." + str(d) + "f") % x
    if "." in s: s = s.rstrip("0").rstrip(".")
    return reg(s + "%")


def dt(iso):
    y, m, d_ = iso.split("-")
    return reg("%d.%d.%s" % (int(d_), int(m), y))


# ------------------------------------------------------------------------------------------------ the rules (mirror of ptax.js)
def tax(price, br):
    t = 0.0; lo = 0.0
    for hi, r in br:
        h = float("inf") if hi is None else hi
        top = min(price, h)
        if top > lo: t += (top - lo) * r
        if price <= h: break
        lo = h
    return t


T = P["tracks"]
single = lambda p: tax(p, T["single"])
extra = lambda p: tax(p, T["extra"])
oleh12a = lambda p: tax(p, T["single"]) if p > P["oleh_cap"] else tax(p, T["oleh"])
oleh12 = lambda p: tax(p, P["oleh12"])
def disabled(p, only=True): return max(0, p - T["single"][0][0]) * P["disabled"]["rate"] if only and p <= P["disabled"]["single_cap"] else p * P["disabled"]["rate"]
gift = lambda p: single(p) * P["gift"]
LATE = P["pay"]["late_week"]
# the hand values of dna.md (the tool test checks the same): any drift stops here
assert rnd(single(3e6)) == 45538 and rnd(extra(3e6)) == 240000 and rnd(oleh12a(3e6)) == 5106 and rnd(oleh12(3e6)) == 60536
assert rnd(oleh12a(4e6)) == 10106 and rnd(oleh12(4e6)) == 110536 and rnd(single(1e7)) == 513886 and rnd(gift(3e6)) == 15179
assert rnd(disabled(3e6)) == 15000 and rnd(single(6e6)) == 195538
# where regulation 12 overtakes 12A on an only home (both under the 20,183,565 cap): solve on the 8% / 5% segment
_lo, _hi = 6055070.0, 20183565.0
for _ in range(200):
    _m = (_lo + _hi) / 2
    if oleh12a(_m) < oleh12(_m): _lo = _m
    else: _hi = _m
CROSS = _hi
assert 12.4e6 < CROSS < 12.6e6, CROSS


def lnk(href, text, lang=None):
    return '<a href="%s"%s>%s</a>' % (href, (' lang="%s" dir="ltr" hreflang="%s"' % (lang, lang)) if lang else "", text)


LINKS_USED = {"/glossary/kvutzat-rechisha/", "/israel-purchase-tax-foreign-residents/", "/real-estate-tax-advisor/purchase-tax-first-home/", "/real-estate-tax-advisor/purchase-tax-investor/",
              "/real-estate-tax-advisor/gift-transfer-apartment/", "/apartment-purchase-cost-calculator/", "/mortgage-calculator/bridge-loan-apartment/",
              "/israel-mortgage-non-residents/", "/buying-new-apartment-developer-2026-negotiation/"}
for c in V["cities"].values():
    if c.get("page"): LINKS_USED.add(c["page"])


# ------------------------------------------------------------------------------------------------ html helpers (the nlag kit on the page)
def esc(s):
    return HT.escape(s, quote=False)


def table(caption, head, rows, num_cols=(), src=None):
    out = '<div class="nlag-tw"><table class="nlag-t"><caption>%s</caption><thead><tr>%s</tr></thead><tbody>' % (esc(caption), "".join("<th>%s</th>" % esc(h) for h in head))
    for r in rows:
        out += "<tr>" + "".join('<td%s><span class="l">%s:</span> %s</td>' % (' class="n"' if i in num_cols else '', esc(head[i]), c) for i, c in enumerate(r)) + "</tr>"
    out += "</tbody></table></div>"
    if src: out += '<p class="nlg4-src">%s</p>' % src
    return out


def b(x):
    return "<bdi>%s</bdi>" % x


def taxcell(t):
    return b(ils(t)) if rnd(t) > 0 else "אין מס"


# SVG kit: phone-first viewBox (400 wide) so 13 px text stays about 11 px on a 360 px screen; capped at 640 px on a desktop
INK, INK2, MUTE, LINE, SEA, DEEP, RED, SEAT = "#12202A", "#3E4C58", "#5E6A75", "#D3DCE2", "#2F6F86", "#1F4B5C", "#C42550", "#E6F0F3"
MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"
SANS = "font-family:'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif"


def tx(x, y, s, size=13, anchor="start", weight=400, fill=INK2, mono=False, rtl=False):
    st = "%s;font-size:%spx;font-weight:%s%s" % (MONO if mono else SANS, size, weight, ";direction:rtl;unicode-bidi:plaintext" if rtl else "")
    return '<text x="%.1f" y="%.1f" text-anchor="%s" style="%s" fill="%s">%s</text>' % (x, y, anchor, st, fill, esc(s))


def fig(fid, title, svg, key=None, cap=None):
    return ('<figure class="nlag-chart nlg4-fig" id="%s"><h3>%s</h3>%s%s%s</figure>' % (fid, esc(title), svg, ('<p class="key">%s</p>' % key) if key else "",
            ('<figcaption class="nlg4-cap">%s</figcaption>' % cap) if cap else ""))


def i1_staircase():
    """I1: the rate on each shekel, three tracks, 0 to 7 million (LTR numeric axis)."""
    W, Hh, L, R, Tp, B = 400, 268, 40, 390, 16, 226
    xmax, ymax = 7000000.0, 0.11
    X = lambda p: L + (R - L) * p / xmax
    Y = lambda r: B - (B - Tp) * r / ymax
    g = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (W, Hh, esc("שיעור מס הרכישה על כל שקל לפי מחיר הדירה: דירה יחידה, דירה נוספת ועולה חדש, 2026"))]
    for r in (0, 0.02, 0.04, 0.06, 0.08, 0.10):
        g.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>' % (L, R, Y(r), Y(r), LINE))
        g.append(tx(L - 4, Y(r) + 4.5, pc(r * 100, 0), size=12, anchor="end", mono=True, fill=MUTE))
    for m in range(1, 8):
        g.append(tx(X(m * 1e6), B + 17, reg(str(m)), size=12, anchor="middle", mono=True, fill=MUTE))
    g.append(tx((L + R) / 2, B + 36, "מחיר הדירה, מיליוני ₪", size=12.5, anchor="middle", fill=INK2, rtl=True))

    def steps(br, top=xmax):
        pts, lo = [], 0.0
        for hi, r in br:
            h = top if hi is None or hi > top else hi
            pts += [(lo, r), (h, r)]
            if hi is None or hi >= top: break
            lo = hi
        return "M" + " L".join("%.1f,%.1f" % (X(a), Y(c)) for a, c in pts)
    g.append('<path d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="miter"/>' % (steps(T["extra"]), RED))
    g.append('<path d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="miter"/>' % (steps(T["single"]), DEEP))
    g.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.2" stroke-dasharray="6 4"/>' % (steps(T["oleh"]), SEA))
    for p_ in (T["single"][0][0], T["single"][1][0], T["single"][2][0]):
        g.append('<line x1="%.1f" x2="%.1f" y1="%.1f" y2="%.1f" stroke="%s" stroke-width="1" stroke-dasharray="2 3"/>' % (X(p_), X(p_), Tp, B, MUTE))
    g.append(tx(X(4.2e6), Y(0.05) - 7, pc(5, 0), size=13, anchor="middle", weight=600, fill=DEEP, mono=True))
    g.append(tx(X(1.93e6), Y(0.035) + 4, pc(3.5), size=12, anchor="end", weight=600, fill=DEEP, mono=True))
    g.append(tx(X(3.0e6), Y(0.08) - 7, pc(8, 0), size=13, anchor="middle", weight=600, fill=RED, mono=True))
    g.append(tx(X(6.55e6), Y(0.10) - 7, pc(10, 0), size=13, anchor="middle", weight=600, fill=RED, mono=True))
    g.append(tx(X(6.55e6), Y(0.08) + 16, pc(8, 0), size=13, anchor="middle", weight=600, fill=DEEP, mono=True))
    g.append(tx(X(4.2e6), Y(0.005) - 7, pc(0.5), size=12, anchor="middle", weight=600, fill=SEA, mono=True))
    g.append('</svg>')
    key = ('<span><i style="border-top:3px solid %s"></i>דירה יחידה</span><span><i style="border-top:3px solid %s"></i>דירה נוספת, תושב חוץ וחברה</span>'
           '<span><i class="d"></i>עולה חדש, תקנה 12א</span>' % (DEEP, RED))
    cap = ("הקווים המקווקווים: %s, %s ו־%s ₪. מעל %s ₪ דירה יחידה ועולה משלמים %s, ומעל %s ₪ %s. המדרגה הגבוהה חלה רק על החלק שמעליה."
           % (num(T["single"][0][0]), num(T["single"][1][0]), num(T["single"][2][0]), num(T["single"][2][0]), pc(8, 0), num(T["single"][3][0]), pc(10, 0)))
    return fig("i1", "השיעור על כל שקל: מדרגות מס הרכישה 2026", "".join(g), key, cap)


BUYERS = [  # I2: one apartment of 3,000,000, ten buyers (our computation by the rules above)
    ("עולה חדש, תקנה 12א", oleh12a(3e6), 0),
    ("נכה, תקנה 11", disabled(3e6), 0),
    ("מתנה לבן או לבת", gift(3e6), 0),
    ("דירה יחידה", single(3e6), 0),
    ("משפר דיור שמכר בזמן", single(3e6), 0),
    ("תושב חוץ שיהפוך לתושב", single(3e6), 0),
    ("עולה ותיק, תקנה 12", oleh12(3e6), 0),
    ("דירה נוספת", extra(3e6), 1),
    ("תושב חוץ", extra(3e6), 1),
    ("משפר דיור שלא מכר בזמן", extra(3e6), 1),
]


def i2_buyers():
    W, top, row = 400, 14, 31
    Hh = top + row * len(BUYERS) + 26
    mx = max(x[1] for x in BUYERS)
    x0, blen = 214, 128
    g = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (W, Hh, esc("מס רכישה על אותה דירה ב־3,000,000 ₪ לפי מי שקונה אותה"))]
    for i, (lab, val, red) in enumerate(BUYERS):
        y = top + i * row
        L_ = max(2.0, blen * val / mx)
        g.append(tx(392, y + 17, lab, size=13, anchor="start", fill=INK, rtl=True))
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="14" rx="2" fill="%s"/>' % (x0 - L_, y + 6, L_, RED if red else SEA))
        g.append(tx(x0 - L_ - 6, y + 17.5, ils(val), size=12.5, anchor="end", weight=500, fill=RED if red else INK, mono=True))
    g.append('<line x1="%d" x2="%d" y1="%d" y2="%d" stroke="%s"/>' % (x0, x0, top, top + row * len(BUYERS), LINE))
    g.append('</svg>')
    cap = ("אותו מחיר, אותו יום, ופער של פי %s בין הזול ליקר. נכה: בדירה יחידה עד %s ₪ יש פטור עד המדרגה הראשונה, וכאן המחיר מעליה ולכן %s מכל המחיר. "
           "משפר דיור שלא מכר בזמן משלים את ההפרש עם הפרשי הצמדה וריבית." % (num(extra(3e6) / oleh12a(3e6)), num(P["disabled"]["single_cap"]), pc(0.5)))
    key = '<span><i style="border-top:3px solid %s"></i>מדרגות מופחתות או דירה יחידה</span><span><i style="border-top:3px solid %s"></i>%s מהשקל הראשון</span>' % (SEA, RED, pc(8, 0))
    return fig("i2", "דירה אחת ב־3,000,000 ₪, עשרה קונים", "".join(g), key, cap)


STEPS = [  # I3: from signing to the Land Registry (guide pp. 11, 54-55, 58-59; s.9(c1)(c2) for upgraders)
    ("יום 0", "חתימה על החוזה: יום העסקה, ממנו נספרים המועדים", SEA),
    ("יום 30", "הצהרה לרשות המסים, טופס 7000, דרך עורך הדין", SEA),
    ("עד יום 50", "הודעת שומה עצמית ושובר, תוך 20 יום מההצהרה", SEA),
    ("יום 60", "תשלום המס, או מאוחר יותר אם החזקה ורוב התשלום נדחים", DEEP),
    ("כל שבוע", "איחור בתשלום: 0.2% מהמס, ועוד הפרשי הצמדה וריבית", RED),
    ("8 חודשים", "שומת המנהל מיום ההצהרה; יתרה משולמת תוך 15 יום", SEA),
    ("השגה", "תוך 30 יום מהשומה, טופס 7013; ערר לוועדה תוך 30 יום מההחלטה", SEA),
    ("24 חודשים", "משפרי דיור: המועד למכור את הדירה הקודמת (רכישה מ־1.6.2025)", DEEP),
    ("4 שנים", "תיקון שומה, טופס 7085", SEA),
]


def i3_timeline():
    W, top, row = 400, 18, 46
    Hh = top + row * len(STEPS) + 6
    ax = 318
    g = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (W, Hh, esc("המועדים של מס רכישה מהחתימה ועד תיקון השומה"))]
    g.append('<line x1="%d" x2="%d" y1="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (ax, ax, top + 6, top + row * (len(STEPS) - 1) + 6, LINE))
    for i, (when, what, col) in enumerate(STEPS):
        y = top + i * row
        g.append('<circle cx="%d" cy="%d" r="6.5" fill="#fff" stroke="%s" stroke-width="2.5"/>' % (ax, y + 6, col))
        g.append(tx(392, y + 11, reg(when), size=13, anchor="start", weight=600, fill=col if col != SEA else INK, rtl=True))
        words, lines = what.split(" "), [""]
        for w_ in words:
            if len(lines[-1]) + len(w_) + 1 > 36: lines.append(w_)
            else: lines[-1] = (lines[-1] + " " + w_).strip()
        for j, ln in enumerate(lines[:2]):
            g.append(tx(ax - 14, y + 11 + j * 17, reg(ln), size=12.5, anchor="start", fill=INK2, rtl=True))
    g.append('</svg>')
    cap = "דוגמה: עסקה שנחתמה ב־%s, הצהרה עד %s ותשלום עד %s. במחשבון: התאריכים לפי יום העסקה שלכם, עם ספירה לאחור." % (dt("2026-10-26"), dt("2026-11-25"), dt("2026-12-25"))
    return fig("i3", "מהחתימה ועד הטאבו: כל המועדים", "".join(g), None, cap)


# ------------------------------------------------------------------------------------------------ tables
W_LATE = [2, 4, 8, 13, 26, 52]
LATE_CASES = [("דירה יחידה, ₪3,000,000", single(3e6)), ("דירה נוספת, ₪3,000,000", extra(3e6)), ("דירה יחידה, ₪5,000,000", single(5e6)), ("דירה יחידה, ₪10,000,000", single(1e7))]
reg("3,000,000 5,000,000 10,000,000")
T1 = table("קנס על איחור בתשלום מס רכישה, לפי מספר השבועות", ["העסקה", "המס"] + ["%s שבועות" % reg(str(w)) for w in W_LATE],
           [[esc(n_), b(ils(t))] + [b(ils(t * LATE * w)) for w in W_LATE] for n_, t in LATE_CASES], num_cols=tuple(range(1, 2 + len(W_LATE))),
           src="קנס של %s מהמס לכל שבוע (סעיף 94ב). לא כולל הפרשי הצמדה וריבית, שמתווספים עד יום התשלום. מדריך רשות המסים 2026, עמ׳ 59." % pc(0.2))

MARG = [1900000, 2000000, 2300000, 2500000, 3000000, 4000000, 6000000, 6100000, 10000000]


def nextb(p, br):
    for i, (hi, r) in enumerate(br):
        if hi is not None and p < hi:
            return hi - p, br[i + 1][1] if i + 1 < len(br) else None
    return None, None


rows2 = []
for p_ in MARG:
    dist, nr = nextb(p_, T["single"])
    last = [r for hi, r in T["single"] if hi is None or p_ <= hi][0]
    rows2.append([b(ils(p_)), b(pc(last * 100)), b(ils(single(p_ + 1e5) - single(p_))), b(ils(extra(p_ + 1e5) - extra(p_))),
                  (b(ils(dist)) + " עד " + b(pc(nr * 100))) if dist else "המדרגה העליונה"])
T2 = table("כמה מוסיפים עוד ₪100,000 במחיר", ["מחיר הדירה", "שיעור השקל האחרון, דירה יחידה", "תוספת מס, דירה יחידה", "תוספת מס, דירה נוספת", "עד המדרגה הבאה, דירה יחידה"],
           rows2, num_cols=(0, 1, 2, 3, 4), src="חישוב שלנו לפי מדרגות 2026 (הוראת ביצוע 1/2026).")

CITY = sorted(V["cities"].items(), key=lambda kv: -kv[1]["r4"])
rows3, free4 = [], 0
for name, c in CITY:
    if rnd(single(c["r4"])) == 0: free4 += 1
    rows3.append([lnk(c["page"], esc(name)) if c.get("page") else esc(name), b(ils(c["r4"])) + "<br><small>%s</small>" % esc(reg(c["q4"])),
                  taxcell(single(c["r4"])), b(ils(extra(c["r4"]))), b(ils(c["r5"])) + "<br><small>%s</small>" % esc(reg(c["q5"])), taxcell(single(c["r5"]))])
T3 = table("מס רכישה על דירה במחיר העסקאות בכל עיר", ["עיר", "4 חדרים, מחיר חציוני", "מס, דירה יחידה", "מס, דירה נוספת", "5 חדרים, מחיר חציוני", "מס, דירה יחידה"],
           rows3, num_cols=(1, 2, 3, 4, 5),
           src="המחירים: חציון העסקאות הסגורות לפי רשות המסים, אתר נדל״ן הממשלתי, הרבעון האחרון שפורסם לכל עיר (קובץ %s). המס: חישוב שלנו לפי מדרגות 2026." % esc(reg(V["file"])))

PARTNERS = [  # (price, your share, your track, partner track)
    (3000000, 0.5, "single", "extra"), (2000000, 0.5, "single", "single"), (4000000, 1 / 3.0, "single", "oleh"), (6000000, 0.5, "single", "foreign"),
]
TN = {"single": "דירה יחידה", "extra": "דירה נוספת", "oleh": "עולה חדש, 12א", "foreign": "תושב חוץ"}
TF = {"single": single, "extra": extra, "oleh": oleh12a, "foreign": extra}
rows4 = []
for pr, sh, a_, p2 in PARTNERS:
    ya, yb = TF[a_](pr) * sh, TF[p2](pr) * (1 - sh)
    rows4.append([b(ils(pr)), "%s, %s" % (TN[a_], b(pc(sh * 100, 0 if sh == 0.5 else 1))), taxcell(ya), "%s, %s" % (TN[p2], b(pc((1 - sh) * 100, 0 if sh == 0.5 else 1))), taxcell(yb), b(ils(ya + yb))])
T4 = table("שני קונים שאינם תא משפחתי אחד", ["מחיר הדירה", "קונה א׳ וחלקו", "מס קונה א׳", "קונה ב׳ וחלקו", "מס קונה ב׳", "יחד"], rows4, num_cols=(0, 2, 4, 5),
           src="כל קונה: המס על שווי הדירה כולה לפי המעמד שלו, כפול החלק שלו (מדריך רשות המסים 2026, עמ׳ 51). חישוב שלנו.")

OLEH_P = [2000000, 3000000, 4000000, 6000000, 10000000, 15000000, 25000000]
rows5 = []
for p_ in OLEH_P:
    a12 = oleh12a(p_)
    rows5.append([b(ils(p_)), taxcell(a12) + ("<br><small>מעל התקרה: כדירה יחידה</small>" if p_ > P["oleh_cap"] else ""), taxcell(oleh12(p_)), b(ils(extra(p_))), taxcell(single(p_))])
T5 = table("עולה חדש: תקנה 12א מול תקנה 12", ["מחיר הדירה", "תקנה 12א, דירה יחידה", "תקנה 12, למי שעלה לפני 15.8.2024", "דירה נוספת בלי הקלה", "דירה יחידה בלי הקלה"],
           rows5, num_cols=(0, 1, 2, 3, 4), src="השיעורים: הוראת ביצוע 1/2026, סעיף 2ג. חישוב שלנו.")

# ------------------------------------------------------------------------------------------------ text
def p(s):
    return "<p>%s</p>" % s


Y_ = P["pay"]
G4 = "\n".join([
    '<!-- nlg4-v1 (G4, %s) -->' % UPDATED,
    '<h2 id="late">איחור בתשלום מס רכישה: מה עולה כל שבוע</h2>',
    p("מס רכישה משלמים תוך %s יום מיום העסקה. אם עד אז לא קיבלתם חזקה, לא שילמתם יותר ממחצית המחיר ולא קיבלתם ייפוי כוח לרישום, התשלום נדחה למוקדם מביניהם (סעיף 51), "
      "ועל תקופת הדחייה נוספים הפרשי הצמדה וריבית. כשהתנאי מתקיים, מודיעים לרשות המסים תוך %s יום." % (reg(Y_["pay_days"]), reg(Y_["cease_notice_days"]))),
    p("מי שמשלם אחרי המועד משלם קנס של <strong>%s מסכום המס לכל שבוע</strong> (סעיף 94ב), ועוד הפרשי הצמדה וריבית עד יום התשלום. על דירה יחידה ב־₪3,000,000 זה %s לכל שבוע, "
      "ועל דירה נוספת באותו מחיר %s לכל שבוע. איחור בהגשת ההצהרה עולה %s לכל שבועיים, ואיחור בהודעה %s לכל שבועיים (הסכומים של %s עד %s). "
      "שני הקנסות לא חלים על אותה תקופה, ורשות המסים רשאית לפטור מהם כשיש סיבה מספקת."
      % (pc(LATE * 100), ils(single(3e6) * LATE), ils(extra(3e6) * LATE), ils(Y_["decl_fine"]), ils(Y_["notice_fine"]), dt(Y_["fine_from"]), dt(Y_["fine_to"]))),
    T1,
    i3_timeline(),
    '<h2 id="how">איך עובדות המדרגות: כל שקל לפי המדרגה שלו</h2>',
    p("מס רכישה מחושב כמו מס הכנסה: המחיר מתחלק לפרוסות, וכל פרוסה משלמת את השיעור שלה. מי שעובר את הסף ב־₪1,000 משלם את השיעור הגבוה רק על ה־₪1,000 האלה. "
      "דירה יחידה ב־%s משלמת %s; ב־%s המס הוא %s, כלומר %s נוספים על %s נוספים במחיר."
      % (ils(2e6), ils(single(2e6)), ils(2.1e6), ils(single(2.1e6)), ils(single(2.1e6) - single(2e6)), ils(1e5))),
    i1_staircase(),
    T2,
    '<h2 id="buyers">אותה דירה, עשרה קונים</h2>',
    p("מי שקונה קובע יותר מהמחיר. על אותה דירה ב־₪3,000,000 עולה חדש משלם %s, מי שזו דירתו היחידה %s, ומי שיש לו כבר דירה %s. "
      "במחשבון למעלה רואים את כל המסלולים על המחיר שלכם, בלחיצה אחת." % (ils(oleh12a(3e6)), ils(single(3e6)), ils(extra(3e6)))),
    i2_buyers(),
    '<h2 id="cities">מס רכישה על דירה במחיר העסקאות בכל עיר</h2>',
    p("כמה מס רכישה יוצא על דירה טיפוסית? לקחנו את המחיר החציוני של דירות 4 ו־5 חדרים שנמכרו בכל עיר, לפי רשות המסים, וחישבנו את המס. "
      "ב־%s מתוך %s הערים, דירת 4 חדרים במחיר החציוני פטורה ממס כדירה יחידה. בתל אביב יפו, דירת 4 חדרים במחיר החציוני (%s) משלמת %s כדירה יחידה ו־%s כדירה נוספת."
      % (num(free4), num(len(CITY)), ils(V["cities"]["תל אביב יפו"]["r4"]), ils(single(V["cities"]["תל אביב יפו"]["r4"])), ils(extra(V["cities"]["תל אביב יפו"]["r4"])))),
    T3,
    '<h2 id="partners">שני קונים שאינם בני זוג: כל אחד לפי המעמד שלו</h2>',
    p("קונים דירה עם אח, חבר או שותף? המס לא מתחלק לפי מעמד אחד. כל קונה מחשב את המס על שווי הדירה כולה לפי המעמד שלו, ומשלם לפי החלק שלו, וכל אחד מגיש הצהרת רוכש. "
      "בני זוג וילדים עד גיל 18 נחשבים קונה אחד, ולכן אצלם המעמד משותף. חלק של %s או פחות בדירה אחרת, או חלק של עד %s בדירה שהתקבלה בירושה, לא הופך את הדירה החדשה לדירה נוספת. "
      "במחשבון: הקלידו את החלק שלכם ובחרו מי קונה את השאר." % (reg("1/3"), reg("1/2"))),
    T4,
    '<h2 id="oleh-choice">עולה חדש: חלון של 8 שנים, ותקנה 12 מול 12א</h2>',
    p("ההקלה לעולה חלה על רכישה משנה לפני העלייה ועד %s שנים אחריה. תקנה 12א, לדירה יחידה עד %s: פטור עד %s, %s עד %s ו־%s עד התקרה; מעל התקרה ההקלה לא חלה. "
      "מי שעלה לפני 15.8.2024 יכול לבחור בתקנה 12: %s עד %s ו־%s מעל, גם בדירה שאינה יחידה ובלי תקרה."
      % (reg("7"), ils(P["oleh_cap"]), ils(T["oleh"][0][0]), pc(0.5), ils(T["oleh"][1][0]), pc(8, 0), pc(0.5), ils(P["oleh12"][0][0]), pc(5, 0))),
    p("מה עדיף? בדירה יחידה עד כ־%s תקנה 12א זולה יותר; מעל זה, ובדירה שאינה יחידה, תקנה 12 חוסכת הרבה: בדירה נוספת ב־₪3,000,000, %s במקום %s. "
      "במחשבון: הקלידו את תאריך העלייה, והוא יבדוק את החלון ויראה את שתי התקנות זו לצד זו." % (ils(round(CROSS, -5)), ils(oleh12(3e6)), ils(extra(3e6)))),
    T5,
    '<h2 id="resident">תושב חוץ שעובר לגור בישראל</h2>',
    p("תושב חוץ משלם כמו דירה נוספת, %s עד %s ו־%s מעל, גם אם זו דירתו היחידה. אבל מי שהופך לתושב ישראל לראשונה, או לתושב חוזר ותיק, תוך %s שנים מהרכישה, נחשב תושב, "
      "ואם זו הדירה היחידה שלו הוא משלם לפי מדרגות דירה יחידה. הארכת המלחמה חלה גם כאן: מי שקנה ב־1.3.2024 יכול היה להפוך לתושב עד 31.8.2026 (הוראת ביצוע 2/2026). "
      "מי שלא הופך לתושב בזמן משלים את המס לדירה נוספת. משכנתא לתושבי חוץ: %s." % (pc(8, 0), ils(T["extra"][0][0]), pc(10, 0), reg("2"), lnk("/israel-mortgage-non-residents/", "המדריך באנגלית", "en"))),
    '<h2 id="inheritance">ירושה, גירושין וביטול עסקה</h2>',
    p("ירושה אינה מכירה לפי חוק מיסוי מקרקעין, וגם העברת זכות במקרקעין אגב גירושין אינה מכירה, ולכן אין עליהן מס רכישה. מתנה לקרוב משלמת %s מהמס הרגיל, "
      "ומתנה לבן זוג שגר עם הנותן באותה דירה פטורה (%s). חלק של יותר מ־%s בדירה שהתקבלה בירושה נחשב דירה שלכם, וזה עשוי להפוך דירה שתקנו אחר כך לדירה נוספת."
      % (reg("1/3"), lnk("/real-estate-tax-advisor/gift-transfer-apartment/", "העברה ללא תמורה"), reg("1/2"))),
    p("עסקה שמתבטלת: מגישים לרשות המסים הודעה על ביטול בטופס %s. אם רשות המסים השתכנעה שהעסקה בוטלה מעיקרה, היא מבטלת את השומות ומחזירה את המס ששולם." % reg(P["cancel_form"])),
    '<h2 id="farm">נחלה, משק חקלאי וקבוצת רכישה</h2>',
    p("מי שרוכש זכות במקרקעין כדי להקים משק חקלאי או לקיים אותו (תקנה 16) משלם על החלק שאינו בניין מגורים %s עד %s ו־%s מעל, ברכישה מ־%s עד %s. "
      "על בית המגורים שבנחלה משלמים לפי מדרגות דירת מגורים. בקבוצת רכישה המס מחושב על שווי הנכס הבנוי, לא על שווי הקרקע בלבד (מדריך רשות המסים 2026, עמ׳ 52). פירוט: %s."
      % (pc(0.5), ils(P["farm"]["rates"][0][0]), pc(5, 0), dt(P["farm"]["from"]), dt(P["farm"]["to"]), lnk("/glossary/kvutzat-rechisha/", "קבוצת רכישה"))),
    ('<aside class="nlag-il nlg4-en" lang="en" dir="ltr"><h3>Israel purchase tax, in English</h3><p>Buying in Israel from abroad? Purchase tax for a foreign '
     'resident is 8%% up to ₪6,055,070 and 10%% above, from the first shekel, unless you become an Israeli resident within two years and the home is your only one. '
     'The full English guide, with the brackets, olim relief, payment dates and worked examples: %s.</p></aside>'
     % lnk("/israel-purchase-tax-foreign-residents/", "Israel purchase tax for foreign residents")),
    '<p class="nlg4-upd">עודכן %s לפי הוראות הביצוע של רשות המסים 1/2026 ו־2/2026, הודעת רשות המסים מ־12.10.2026 ומדריך רשות המסים לרוכש 2026. '
    'מס רכישה על דירה ראשונה: %s. על דירה נוספת ולמשקיעים: %s. כל העלויות של קניית דירה: %s.</p>'
    % (reg(UPDATED), lnk("/real-estate-tax-advisor/purchase-tax-first-home/", "המדריך לדירה ראשונה"), lnk("/real-estate-tax-advisor/purchase-tax-investor/", "המדריך לדירה נוספת"),
       lnk("/apartment-purchase-cost-calculator/", "מחשבון עלות רכישה כוללת")),
    '<p style="margin:14px 0 0;font:400 13px/20px var(--sans);color:var(--mu)">המקורות הרשמיים: '
    + " · ".join('<a href="%s" rel="noopener" target="_blank" style="color:var(--sea)">%s</a>' % (u, t_) for t_, u in [
        ("מדריך רשות המסים לרוכש 2026", P["guide"]["url"]), ("הוראת ביצוע 1/2026", P["instruction"]["url"]), ("הוראת ביצוע 2/2026", P["war"]["url"]),
        ("הודעת רשות המסים 12.10.2026", P["extension"]["url"]), ("נתוני העסקאות, אתר נדל״ן הממשלתי", V["url"])]) + '</p>',
])

CSS4 = ('<style id="nlg4-css">.nlg4-cta{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 6px;direction:rtl}'
        'html body .nlg4-cta a{display:inline-flex;align-items:center;min-height:44px;padding:10px 16px;border-radius:6px;border:1px solid #2F6F86;color:#1F4B5C !important;'
        'background:#fff;font:600 15px/20px "IBM Plex Sans Hebrew",system-ui,sans-serif;text-decoration:none !important}'
        'html body .nlg4-cta a.is-primary{background:#2F6F86;color:#fff !important}html body .nlg4-cta a:focus-visible{outline:3px solid #12202A;outline-offset:2px}'
        '.nlg4-anchor,.nlag h2[id]{scroll-margin-top:84px}.nlag .nlg4-fig{max-width:640px}.nlag .nlg4-fig svg{width:100%;height:auto;display:block;direction:ltr}'
        '.nlag .nlg4-cap{margin:8px 0 0;font:400 13px/1.6 var(--sans);color:var(--mu)}.nlag .nlg4-src{margin:-12px 0 22px;font:400 12.5px/1.6 var(--sans);color:var(--mu)}'
        '.nlag table.nlag-t a,.nlag .nlg4-upd a,.nlag .nlag-il a{color:var(--sea);text-decoration:underline;text-underline-offset:2px}.nlag .nlg4-upd{margin:20px 0 0;font:400 14px/1.7 var(--sans);color:var(--i2)}.nlag .nlg4-en{direction:ltr;text-align:left}'
        '.nlag .nlg4-en h3{font-family:"IBM Plex Sans",system-ui,sans-serif}'
        '@media (max-width:600px){.nlag table.nlag-t thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}'
        '.nadlan-guide .eyebrow{background:#E6F0F3 !important;border-color:#2F6F86 !important;color:#1F4B5C !important}'
        '.nadlan-guide .note{background:#F6F8F9 !important;border-color:#D3DCE2 !important;color:#12202A !important}</style>')
TOP = ('<!-- wp:html -->\n' + CSS4 + '\n<p class="nlg4-cta"><a class="is-primary" href="#ptax-tool">חשבו את מס הרכישה שלכם</a>'
       '<a href="#brackets">לטבלת המדרגות 2026</a><a href="#late">מתי משלמים ומה עולה איחור</a></p>\n<div id="ptax-tool" class="nlg4-anchor"></div>\n<!-- /wp:html -->\n\n')

QA = [
    ("מי צריך לשלם מס רכישה?",
     "הקונה. מס רכישה חל על מי שרוכש זכות במקרקעין בישראל: דירה, בית, קרקע או נכס מסחרי, לפי שווי העסקה. גם כשאין מס לתשלום מגישים הצהרה תוך %s יום מהעסקה. "
     "ירושה ומעבר זכות אגב גירושין אינם מכירה, ולכן אין עליהם מס רכישה." % reg(Y_["declare_days"])),
    ("מתי משלמים מס רכישה על דירה מקבלן?",
     "תוך %s יום מהעסקה, אלא אם עד אז לא קיבלתם חזקה, לא שילמתם יותר ממחצית המחיר ולא קיבלתם ייפוי כוח לרישום. אז התשלום נדחה למוקדם מביניהם (סעיף 51), ועל תקופת הדחייה "
     "נוספים הפרשי הצמדה וריבית. כשהתנאי מתקיים מודיעים לרשות המסים תוך %s יום. המס מחושב על המחיר כולל מע״מ." % (reg(Y_["pay_days"]), reg(Y_["cease_notice_days"]))),
    ("מתי משלמים מס רכישה על דירה שנייה?",
     "באותם מועדים: הצהרה תוך %s יום ותשלום תוך %s יום, או מאוחר יותר לפי סעיף 51. השיעור: %s עד %s ו־%s מעל, לפי הוראת השעה שהוארכה לרכישות עד 10.2.2027. פירוט: %s."
     % (reg(Y_["declare_days"]), reg(Y_["pay_days"]), pc(8, 0), ils(T["extra"][0][0]), pc(10, 0), lnk("/real-estate-tax-advisor/purchase-tax-investor/", "המדריך לדירה נוספת ולמשקיעים"))),
    ("מה הקנס על איחור בתשלום מס רכישה?",
     "%s מסכום המס לכל שבוע של איחור (סעיף 94ב), ועוד הפרשי הצמדה וריבית עד יום התשלום. על דירה יחידה ב־₪3,000,000 (מס של %s) זה %s לכל שבוע; על דירה נוספת באותו מחיר "
     "(%s) זה %s לכל שבוע. רשות המסים רשאית לפטור מהקנס כשיש סיבה מספקת." % (pc(LATE * 100), ils(single(3e6)), ils(single(3e6) * LATE), ils(extra(3e6)), ils(extra(3e6) * LATE))),
    ("מה הקנס על איחור בהגשת ההצהרה?",
     "%s לכל שבועיים של איחור בהצהרה, ו־%s לכל שבועיים על הודעה, בסכומים של %s עד %s. הקנס על איחור בהצהרה והקנס על איחור בתשלום לא חלים על אותה תקופה."
     % (ils(Y_["decl_fine"]), ils(Y_["notice_fine"]), dt(Y_["fine_from"]), dt(Y_["fine_to"]))),
    ("האם יורש משלם מס רכישה?",
     "לא. הורשה אינה מכירה לפי חוק מיסוי מקרקעין, ולכן קבלת דירה בירושה אינה חייבת במס רכישה. חלק של יותר ממחצית בדירה שהתקבלה בירושה נחשב דירה שבבעלותכם, "
     "וזה עשוי להפוך דירה שתקנו אחר כך לדירה נוספת."),
    ("מה קורה למס הרכישה כשעסקה מתבטלת?",
     "מגישים לרשות המסים הודעה על ביטול בטופס %s. אם רשות המסים השתכנעה שהעסקה בוטלה מעיקרה, היא מבטלת את השומות ומחזירה את המס ששולם." % reg(P["cancel_form"])),
    ("קונים דירה עם שותף שיש לו דירה: כמה כל אחד משלם?",
     "כל קונה מחשב את המס על שווי הדירה כולה לפי המעמד שלו, ומשלם לפי החלק שלו. בדירה ב־₪3,000,000, חצי וחצי: מי שזו דירתו היחידה משלם %s, והשותף שיש לו דירה %s. "
     "בני זוג וילדים עד גיל 18 נחשבים קונה אחד." % (ils(single(3e6) / 2), ils(extra(3e6) / 2))),
    ("עליתי לפני 15.8.2024: מה עדיף, תקנה 12 או 12א?",
     "בדירה יחידה עד כ־%s תקנה 12א זולה יותר: בדירה ב־₪4,000,000, %s לעומת %s. תקנה 12 עדיפה בדירה שאינה יחידה (בדירה ב־₪3,000,000, %s במקום %s), "
     "בדירה יחידה יקרה מזה, ומעל %s, שם תקנה 12א לא חלה." % (ils(round(CROSS, -5)), ils(oleh12a(4e6)), ils(oleh12(4e6)), ils(oleh12(3e6)), ils(extra(3e6)), ils(P["oleh_cap"]))),
    ("תושב חוץ שעובר לגור בישראל משלם כמו דירה יחידה?",
     "כן, אם זו הדירה היחידה שלו והוא הופך לתושב ישראל לראשונה, או לתושב חוזר ותיק, תוך %s שנים מהרכישה. מי שלא הופך לתושב בזמן משלים את המס לדירה נוספת. "
     "המדריך באנגלית: %s." % (reg("2"), lnk("/israel-purchase-tax-foreign-residents/", "Israel purchase tax for foreign residents", "en"))),
]
FAQ_ADD = "".join("<h3>%s</h3><p>%s</p>" % qa for qa in QA)

# ------------------------------------------------------------------------------------------------ the replacements
ANS_OLD = "ומשלמים בדרך כלל לא לפני 60 יום מיום העסקה.</p>"
ANS_NEW = "ומשלמים תוך 60 יום, או מאוחר יותר כשהחזקה ורוב התשלום נדחים.</p>"
FIX = [  # C1 to C4 (the only edits inside old text)
    ("<p>טופס 7000, בדיווח מקוון. איחור: קנס של 5% מהמס, הצמדה וריבית, ועוד 310 ₪ לכל שבועיים של איחור בהצהרה.</p>",
     "<p>טופס 7000, בדיווח מקוון. איחור בהצהרה: 310 ₪ לכל שבועיים (2026).</p>"),
    ('<span class="who">לא לפני 60 יום מהעסקה</span><p>המועד לפי החוק: המוקדם מבין קבלת החזקה, תשלום של יותר ממחצית או ייפוי כוח לרישום. תשלום מאוחר נושא הצמדה וריבית.',
     '<span class="who">תוך 60 יום מהעסקה, או במועד שנדחה</span><p>אם עד אז לא התקבלה חזקה, לא שולם יותר ממחצית המחיר ולא ניתן ייפוי כוח לרישום, התשלום נדחה למוקדם מביניהם, '
     'ועל הדחייה נוספים הפרשי הצמדה וריבית. איחור בתשלום: קנס של 0.2% מהמס לכל שבוע, ועוד הצמדה וריבית.'),
    ("<small>תשלום לא לפני 60 יום</small>", "<small>תשלום תוך 60 יום</small>"),
    (ANS_OLD, ANS_NEW),
]
SHORTCODE = '<!-- wp:shortcode -->\n[nadlan_tool id="ptax"]\n<!-- /wp:shortcode -->'
END_NLAG = 'בדיקת החזר</a></p>\n</div>\n<div class="nadlan-guide">'
FAQ_LAST = 'ועל ההחלטה אפשר לערור לוועדת ערר תוך 30 יום.</p><h2>בדיקה מהירה לפני שממשיכים לעסקה</h2>'
R = [
    (SHORTCODE, TOP + SHORTCODE),                                                                            # 1. CTA row + anchor before the tool
    ("<h2>מדרגות מס רכישה 2026 לכל המסלולים</h2>", '<h2 id="brackets">מדרגות מס רכישה 2026 לכל המסלולים</h2>'),  # 2. ids for the CTA links
    ("<h2>מתי ואיך משלמים מס רכישה</h2>", '<h2 id="pay">מתי ואיך משלמים מס רכישה</h2>'),
    (END_NLAG, 'בדיקת החזר</a></p>\n' + G4 + '\n</div>\n<div class="nadlan-guide">'),                         # 3. the G4 sections inside .nlag
    (FAQ_LAST, FAQ_LAST.replace("</p><h2>", "</p>" + FAQ_ADD + "<h2>")),                                        # 4. 10 questions at the end of the FAQ
]


def get_raw():
    if LOCAL:
        return io.open(RECON, encoding="utf-8").read(), {"link": SITE + "/purchase-tax-calculator/", "modified": RECON_MODIFIED + " (reconstructed)"}, None
    sys.stdout.flush()
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "g4page"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
    req = ns["req"]
    s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,title,modified,meta" % PID)
    assert s == 200, s
    return r["content"]["raw"], r, req


raw, r, req = get_raw()
assert "nlg4-v1" not in raw and 'id="ptax-tool"' not in raw, "already upgraded: refuse to apply twice"
new = raw
for o, n_ in FIX + R:
    c = new.count(o)
    assert c == 1, (c, o[:80])
    new = new.replace(o, n_)
print("[page %d] %s | modified %s | %d corrections + %d anchored insertions, each matched once" % (PID, r["link"], r["modified"], len(FIX), len(R)))

# ------------------------------------------------------------------------------------------------ checks on the result
for line in raw.split("\n"):  # additive: every original line survives (corrected lines in their corrected form)
    ln = line
    for o, n_ in FIX + R[1:3] + R[4:]:  # corrected lines, the two ids, and the FAQ line that receives the new questions
        ln = ln.replace(o, n_)
    assert ln in new, ("an original line is missing", line[:90])
pos = [new.index(x) for x in ('<h1 ', ANS_NEW, 'class="nlg4-cta"', 'id="ptax-tool"', '[nadlan_tool id="ptax"]', '<div class="nlag">', 'id="brackets"', 'id="pay"', 'nlg4-v1',
                              'id="late"', 'id="i3"', 'id="i1"', 'id="i2"', 'id="cities"', 'class="nadlan-guide"', '<h2>שאלות נפוצות על מס רכישה</h2>', QA[0][0], '<h2>בדיקה מהירה')]
assert pos == sorted(pos), ("content order", pos)
assert new.count("<h1") == 1


def visible(h, keep_svg=True):
    h_ = re.sub(r"<(script|style)\b.*?</\1>", " ", h, flags=re.S)
    if not keep_svg: h_ = re.sub(r"<svg\b.*?</svg>", " ", h_, flags=re.S)
    h_ = re.sub(r"<!--.*?-->", " ", h_, flags=re.S)
    h_ = re.sub(r"\[nadlan_[a-z]+[^\]]*\]", " ", h_)
    h_ = re.sub(r"<[^>]+>", " ", h_)
    return re.sub(r"\s+", " ", HT.unescape(h_.replace("&nbsp;", " ")))


ADDED = TOP + G4 + FAQ_ADD + "".join(n_ for _, n_ in FIX)
EN = re.search(r'<aside class="nlag-il nlg4-en".*?</aside>', G4, flags=re.S).group(0)
ARIA = " ".join(re.findall(r'aria-label="([^"]*)"', ADDED))
vis_new = visible(ADDED.replace(EN, " ")) + " " + ARIA
vis_new_text = visible(ADDED.replace(EN, " "), keep_svg=False)
BANNED = r"ממשק|מערכת|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה|טעון אימות|נדלן חכם|Nadlan|מנגנון|מודל|הדגמה|טכנולוגי|אטלס|Atlas|\bדמו\b|אפס|להמחשה"
for name, v_ in (("new content", vis_new), ("English aside", visible(EN))):
    assert not re.search(r"[–—]", v_), (name, "long dash")
    assert not re.search(r"(?:^|\s)-{1,3}(?:\s|$)|--", v_), (name, "spaced hyphen or double hyphen")
    m_ = re.search(BANNED, v_)
    assert not m_, (name, "banned word", m_.group(0) if m_ else "")
    assert '"' not in v_, (name, "ASCII double quote (use gershayim)")
    assert "..." not in v_
assert not re.search(r"(?<![\d.,₪/])0(?![\d.,%])", vis_new_text), "a zero amount in visible text (tables say אין מס)"
untraced = sorted({norm(tk) for tk in NUMRE.findall(vis_new + " " + visible(EN))} - ALLOW)
assert not untraced, ("numbers not traceable to the data file, our computation or FACTS", untraced)
faq_html = new[new.index("<h2>שאלות נפוצות על מס רכישה</h2>"):new.index("<h2>בדיקה מהירה")]
old_q = re.findall(r"<h3>(.*?)</h3>", raw[raw.index("<h2>שאלות נפוצות על מס רכישה</h2>"):raw.index("<h2>בדיקה מהירה")])
assert not [q for q, _ in QA if q in old_q], "duplicate FAQ"
faq_n = len(re.findall(r"<h3[^>]*>.*?</h3>\s*<p", faq_html, flags=re.S))
assert faq_n == len(old_q) + len(QA) == 33, (faq_n, len(old_q))
hrefs = set(re.findall(r'href="(/[^"#]*)"', ADDED))
assert hrefs <= LINKS_USED, ("internal href not in the checked list", hrefs - LINKS_USED)


def check_url(u):
    q = urllib.request.Request(SITE + u, headers={"User-Agent": "Mozilla/5.0 nadlan-g4-check"})

    class NoRedir(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k): return None
    try:
        code = urllib.request.build_opener(NoRedir).open(q, timeout=40).status
    except urllib.error.HTTPError as e:
        code = e.code
    return code


if LINKS or not (LOCAL or DRY):
    bad = {u: c for u, c in ((u, check_url(u)) for u in sorted(hrefs)) if c != 200}
    assert not bad, ("internal links not 200 (no redirect)", bad)
    print("[links] %d internal links in the new content, all 200 with no redirect" % len(hrefs))

WORDS = lambda v_: len(re.findall(r"[\w֐-׿%₪.,]+", v_))
print("[new content] %d words of text (+%d inside the 3 SVGs, +%d English) | tables %d | svg %d | h2 %d | h3 %d (of them %d FAQ) | FAQ on page %d | numbers traced %d"
      % (WORDS(vis_new_text), WORDS(vis_new) - WORDS(vis_new_text) - WORDS(ARIA), WORDS(visible(EN)), ADDED.count("<table"), ADDED.count("<svg"), ADDED.count("<h2"),
         ADDED.count("<h3"), len(QA), faq_n, len({norm(tk) for tk in NUMRE.findall(vis_new)})))
print("[whole content] %d words | tables %d | svg %d | h2 %d | h3 %d" % (WORDS(visible(new, keep_svg=False)), new.count("<table"), new.count("<svg"), new.count("<h2"), new.count("<h3")))
print("[facts] regulation 12 overtakes 12A on an only home from %s; free 4-room medians as an only home: %d of %d cities" % (num(CROSS), free4, len(CITY)))
if TITLE: print("[title] %s (%d chars) | description %d chars" % (SEO_TITLE, len(SEO_TITLE), len(SEO_DESC)))

if LOCAL or DRY:
    out = os.path.join(H, "preview", "g4-page-content.html"); os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8", newline="").write(new)
    # a local page that renders the content with the real tool (served from the repo root by preview/shoot.py)
    body = new
    body = re.sub(r"\[nadlan_crumbs[^\]]*\]", '<nav class="nlbc" style="font:500 13px/18px \'IBM Plex Sans Hebrew\',sans-serif;color:#5E6A75;margin:4px 0 10px">'
                  '<a href="#" style="color:#2F6F86">בית</a> › <a href="#" style="color:#2F6F86">מיסוי מקרקעין</a> › <span>מחשבון מס רכישה</span></nav>', body)
    A = "../../../../../plugins/nadlan-config/assets/instruments/"
    body = body.replace('[nadlan_tool id="ptax"]', '<section class="nli" dir="rtl" lang="he" aria-label="מחשבון מס רכישה"><div class="nli-host" data-nli="ptax" data-nli-data="%sdata/ptax.json"></div></section>' % A)
    page = ('<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G4 preview: purchase tax</title>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
            '<link rel="stylesheet" href="%score.css"><style>body{margin:0;background:#fff;color:#12202A;font-family:"IBM Plex Sans Hebrew",system-ui,sans-serif;overflow-x:hidden}'
            '.wrap{max-width:860px;margin:0 auto;padding:12px 16px 60px}h1{font:700 30px/1.25 "IBM Plex Sans Hebrew",sans-serif;margin:8px 0 12px}p{line-height:1.75}'
            '.entry h2{font-size:1.45rem;line-height:1.3;margin:34px 0 10px}</style></head><body><div class="wrap entry">%s</div>'
            '<script src="%score.js"></script><script src="%stools/ptax.js"></script></body></html>' % (A, body, A, A))
    io.open(os.path.join(H, "preview", "index.html"), "w", encoding="utf-8", newline="").write(page)
    print("[%s] nothing written to the site | preview: %s and preview/index.html" % ("local" if LOCAL else "dry", out))
    sys.exit(0)

# ------------------------------------------------------------------------------------------------ live write (coordinator only, after ptax v3 is released)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
body = {"content": new}
if TITLE:
    meta = r.get("meta") or {}
    io.open(os.path.join(bk, "page-%d-meta-%s.json" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8").write(json.dumps({k: meta.get(k) for k in ("_yoast_wpseo_title", "_yoast_wpseo_metadesc")}, ensure_ascii=False))
    body["meta"] = {"_yoast_wpseo_title": SEO_TITLE, "_yoast_wpseo_metadesc": SEO_DESC}
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, body)
assert s2 in (200, 201), s2
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
live = urllib.request.urlopen(urllib.request.Request(r["link"] + "?g4=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
bd = live[live.find("<body"):]
ok = {"read-back": back.strip() == new.strip(), "one h1": bd.count("<h1") == 1, "tool mounted": 'data-nli="ptax"' in bd, "ptax.js enqueued": "tools/ptax.js" in live,
      "ptax v3 live (NLPT.payDue)": "payDue" in urllib.request.urlopen(urllib.request.Request(SITE + "/wp-content/plugins/nadlan-config/assets/instruments/tools/ptax.js?g4=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8", "replace"),
      "CTA before the tool": bd.index('class="nlg4-cta"') < bd.index('data-nli="ptax"'), "3 figures": bd.count('class="nlag-chart nlg4-fig"') == 3,
      "inherited check 20,183,565": "20,183,565" in bd, "one FAQPage": live.count('"@type":"FAQPage"') == 1, "33 questions": live.count('"@type":"Question"') == 33,
      "no 5% fine sentence": "קנס של 5% מהמס" not in bd, "English aside lang=en": 'class="nlag-il nlg4-en" lang="en"' in bd}
if TITLE: ok["title"] = ("<title>" + SEO_TITLE) in live
for k, v_ in ok.items(): print("   ", "OK " if v_ else "BAD", k)
