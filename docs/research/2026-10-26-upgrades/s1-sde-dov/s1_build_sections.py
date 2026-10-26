# -*- coding: utf-8 -*-
"""S1 /sde-dov/ (page 4730): builds the NEW copy of the hub from local data only (no network, nothing posted):
the answer paragraph and the CTA row under the H1, the plot tracker mount [nadlan_tool id="sdplan"], 7 tables, 3 SVG infographics,
16 new FAQ (h3 + p, read by the FAQPage of inc/instruments.php), and a method-and-sources line. Every number comes from
data/sdplan.json and data/s1-facts.json (build_s1_data.py, official files of 26.10.2026) or from the dated facts of dna.md section 4.

Writes:
  data/s1-sections.json        the fragments, keyed by the anchor they go before or after (write_s1_page.py posts them, not run here)
  preview/s1-new-sections.html the new copy alone
  preview/s1-page-render.html  the live hub content as served on 26.10.2026 (REST, rendered) with the fragments placed at the same
                               anchors, the tool mounted from the local files (core.css, core.js, tool/sdplan.js, data/sdplan.json)
Language gates (no long dash, no banned word, no zero numbers, svg text >= 12px, one h1) run on the new copy.
  python docs/research/2026-10-26-upgrades/s1-sde-dov/s1_build_sections.py"""
import html as HT, io, json, os, re, sys, urllib.parse
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
RAW = r"C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\s1"
D = json.load(io.open(os.path.join(H, "data", "sdplan.json"), encoding="utf-8"))
FX = json.load(io.open(os.path.join(H, "data", "s1-facts.json"), encoding="utf-8"))
WA = "972525101555"; UPDATED = "26.10.2026"
CN = {"eshkol": "מתחם אשכול", "merkaz": "מרכז הרובע", "tzafon": "צפון הרובע"}; CO = ["eshkol", "merkaz", "tzafon"]
INK, INK2, MUTE, SEA, DEEP, LINE, RED = "#12202A", "#3E4C58", "#5E6A75", "#2F6F86", "#1F4B5C", "#D3DCE2", "#C42550"
FILL = ["#EEF2F5", "#CFE0E7", "#8DB4C3", "#4F8BA0", "#2F6F86", "#1F4B5C"]
FONT = "font-family:'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif"; MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"


def dmy(s): y, m, d = s[:10].split("-"); return "%d.%d.%s" % (int(d), int(m), y)
def num(n): return "{:,}".format(int(round(n)))
def mil(n, d=1): return ("%." + str(d) + "f") % (n / 1e6)
def ils(n): return num(n) + " ₪"


P = D["plots"]; BY = {r["id"]: r for r in P}; ST = D["stages"]
won = [t for t in FX["tenders"] if t["st"] == "won"]; opn = [t for t in FX["tenders"] if t["st"] == "open"]; nob = [t for t in FX["tenders"] if t["st"] == "nobid"]
SALE = ("בנייה רוויה", "מגורים, מסחר ומלונאות")
res_won = [t for t in won if t["use"] in SALE + ("דיור להשכרה", "דיור מוגן")]
U_ALL = sum(t["units"] for t in won); U_SALE = sum(t["units"] for t in won if t["use"] in SALE); U_RENT = sum(t["units"] for t in won if t["use"] == "דיור להשכרה"); U_SEN = sum(t["units"] for t in won if t["use"] == "דיור מוגן")
RES_PLOTS_WON = sorted(set(p for t in res_won for p in t["plots"]))
BIZ_PLOTS_WON = sorted(set(p for t in won if t["use"] == "מסחר ומשרדים" for p in t["plots"]))
UNDER = [r for r in P if r["s"] == 5]; DESIGN = [r for r in P if r["s"] >= 2]
BIDS = sum(t["bid"] for t in won); DEV = sum(t["dev"] for t in won)
FEB_MAR_25 = [t for t in won if "2025-02-01" <= t["close"] <= "2025-03-31"]
assert U_ALL == 9316 and U_SALE == 6152 and U_RENT == 2514 and U_SEN == 650, (U_ALL, U_SALE, U_RENT, U_SEN)
assert len(RES_PLOTS_WON) == 32 and len(BIZ_PLOTS_WON) == 4, (len(RES_PLOTS_WON), len(BIZ_PLOTS_WON))
assert len(UNDER) == 8 and sum(t["units"] for t in FEB_MAR_25) == 6666 and len(set(t["tender"] for t in FEB_MAR_25)) == 8
SALE_T = [t for t in won if t["use"] in SALE]
def per(t): return (t["bid"] + t["dev"]) / t["units"]
PER = {c: [per(t) for t in SALE_T if BY[t["plots"][0]]["c"] == c] for c in CO}
WAVG = {c: sum(t["bid"] + t["dev"] for t in SALE_T if BY[t["plots"][0]]["c"] == c) / sum(t["units"] for t in SALE_T if BY[t["plots"][0]]["c"] == c) for c in CO}
NAMES = {r["id"]: r["p"]["n"].split(",")[0] for r in P if r.get("p")}
STN = {s["n"]: s for s in D["stations"]}

# ------------------------------------------------------------------ svg helpers (NadLan Instruments: ink, sea, deep; survey red only for a warning)
def tx(x, y, s, anchor="start", size=13, w=400, fill=INK, mono=False, halo=False):
    assert size >= 12
    st = "%s;font-size:%spx;font-weight:%s" % (MONO if mono else FONT, size, w) + (";paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-linejoin:round" if halo else "")
    return '<text x="%.1f" y="%.1f" text-anchor="%s" style="%s" fill="%s">%s</text>' % (x, y, anchor, st, fill, HT.escape(s, quote=False))


def svg_open(h, label): return '<svg viewBox="0 0 420 %d" direction="rtl" role="img" aria-label="%s" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">' % (h, HT.escape(label))


def svg_stages():
    """I1: the residential plots of each compound by official stage today (stacked)."""
    xr, xl, y0 = 408, 12, 96
    rows = []
    for c in CO:
        L = [r for r in P if r["c"] == c and r["use"] in ("res", "special")]
        rows.append((c, [sum(1 for r in L if r["s"] == i) for i in range(6)], len(L)))
    mx = max(n for _, _, n in rows); sc = (xr - xl) / mx
    hgt = y0 + len(rows) * 62 + 120
    g = [svg_open(hgt, "המגרשים למגורים בכל מתחם לפי השלב הרשמי, %s: %s" % (UPDATED, "; ".join("%s %d מגרשים, %d בבנייה" % (CN[c], n, b[5]) for c, b, n in rows)))]
    g.append(tx(xr, 24, "איפה כל מתחם עומד היום", size=16, w=600))
    g.append(tx(xr, 46, "המגרשים למגורים ולדיור מוגן, לפי השלב הרשמי האחרון", size=13, fill=INK2))
    g.append(tx(xr, 66, "רשות מקרקעי ישראל ועיריית תל אביב-יפו, %s" % UPDATED, size=13, fill=INK2))
    y = y0
    for c, b, n in rows:
        g.append(tx(xr, y, "%s · %d מגרשים" % (CN[c], n), size=14, w=600))
        x = xr
        for i, k in enumerate(b):
            if not k: continue
            w = k * sc
            g.append('<rect x="%.1f" y="%d" width="%.1f" height="24" fill="%s" stroke="#fff" stroke-width="1"/>' % (x - w, y + 8, w, FILL[i]))
            if w >= 20: g.append(tx(x - w / 2, y + 25, str(k), anchor="middle", size=13, w=600, fill="#fff" if i >= 3 else INK, mono=True))
            x -= w
        y += 62
    ly = y + 4
    for i, s in enumerate(ST):
        xx = xr if i % 2 == 0 else 200; yy = ly + (i // 2) * 22
        g.append('<rect x="%d" y="%d" width="13" height="13" fill="%s" stroke="%s"/>' % (xx - 13, yy - 10, FILL[i], LINE))
        g.append(tx(xx - 19, yy + 1, s, size=13))
    g.append(tx(xr, ly + 76, "בבנייה: עבודות רשומות באתרי הבנייה של העירייה, או היתר שהבנייה לפיו התחילה", size=12, fill=MUTE))
    g.append("</svg>")
    return "".join(g)


def svg_land():
    """I2: land + development per unit in every tender of apartments for sale, grouped by compound (our calculation, RMI data)."""
    xr, xlab, x0, xl = 408, 408, 262, 12
    mx = 3.6e6; sc = (x0 - xl - 40) / mx
    groups = []
    for c in CO:
        T = sorted([t for t in SALE_T if BY[t["plots"][0]]["c"] == c], key=lambda t: -per(t)); groups.append((c, T))
    hgt = 96 + sum(30 + 21 * len(T) for _, T in groups) + 58
    g = [svg_open(hgt, "קרקע ופיתוח ליחידת דיור במכרזי הדירות למכירה ברובע שדה דב: ממוצע משוקלל %s (החישוב שלנו, לפי רשות מקרקעי ישראל)" %
                  "; ".join("%s %s מיליון ₪" % (CN[c], mil(WAVG[c], 2)) for c in CO))]
    g.append(tx(xr, 24, "כמה עלתה הקרקע ליחידת דיור", size=16, w=600))
    g.append(tx(xr, 46, "סכום הזכייה והוצאות הפיתוח חלקי יחידות הדיור, במכרזי הדירות למכירה", size=13, fill=INK2))
    g.append(tx(xr, 66, "החישוב שלנו, לפי תוצאות המכרזים ברשות מקרקעי ישראל", size=13, fill=INK2))
    y = 96
    for c, T in groups:
        g.append(tx(xr, y + 4, "%s · מכרזי %s · ממוצע משוקלל %s מיליון ₪" % (CN[c], "2021 עד 2022" if c == "eshkol" else "2025", mil(WAVG[c], 2)), size=13, w=600, fill=DEEP))
        y += 18
        for t in T:
            pid = t["plots"][0]; v = per(t); w = v * sc
            lab = ("מגרש " + pid + " · " + NAMES[pid].replace("GINDI VOGUE", "VOGUE")) if pid in NAMES else "מגרש " + pid
            g.append(tx(xlab, y + 12, lab, size=13))
            g.append('<rect x="%.1f" y="%d" width="%.1f" height="13" fill="%s"/>' % (x0 - w, y + 2, w, {"eshkol": DEEP, "merkaz": SEA, "tzafon": "#7FA9B9"}[c]))
            g.append(tx(x0 - w - 5, y + 13, mil(v, 2), size=13, mono=True, halo=True))
            y += 21
        y += 12
    g.append(tx(xr, y + 10, "במיליוני ₪ ליחידת דיור. מכרזי הדירות להשכרה ולדיור מוגן אינם כאן:", size=12, fill=MUTE))
    g.append(tx(xr, y + 28, "המחיר בהם נקבע בתנאים אחרים, והשוואה אליהם מטעה.", size=12, fill=MUTE))
    g.append("</svg>")
    return "".join(g)


MIL = [  # official milestones (dates from the GIS plans layer, RMI tender files, the GIS permits layer; the closure from the hub's history)
    ("2019-04-30", "תכנית 4444, רובע שדה דב, הופקדה"), ("2019-07-01", "שדה התעופה נסגר לטיסות"), ("2019-07-18", "תמ\"ל 3001, מתחם אשכול, הופקדה"),
    ("2020-08-09", "תכנית 4444 נכנסה לתוקף"), ("2021-05-20", "תמ\"ל 3001 נכנסה לתוקף"), ("2021-08-23", "המכרז הראשון: 4 מגרשים, 1,574 דירות"),
    ("2024-01-17", "תכנית העיצוב הראשונה אושרה, מגרש 111"), ("2024-03-21", "ההיתר הראשון ברובע, מגרש 111"), ("2024-12-02", "מכרז מגרשי התעסוקה במתחם אשכול"),
    ("2025-02-13", "תכנית מרכז הרובע נכנסה לתוקף"), ("2025-02-19", "מכרזי מרכז הרובע: %s יחידות דיור" % num(sum(t["units"] for t in won if t["close"] == "2025-02-19"))),
    ("2025-03-26", "מכרזי צפון הרובע: %s יחידות דיור" % num(sum(t["units"] for t in won if t["close"] == "2025-03-26"))), ("2025-06-08", "תכנית צפון הרובע נכנסה לתוקף"),
    ("2026-10-21", "עוד 3 תכניות עיצוב בצפון הרובע אושרו"),
]
NEXT = [("2026-11-16", "נסגר מכרז 5 מגרשי המלונאות במרכז הרובע"), ("2026-11-30", "נסגר מכרז מגרש 304, תעסוקה ומסחר"), ("2026-12-07", "נסגר מכרז מגרש 3204, 217 דירות")]


def svg_timeline():
    """I3: the district's official milestones, and the three closing dates already published."""
    xr, xa = 408, 300
    rows = MIL + [None] + NEXT
    hgt = 84 + len(rows) * 25 + 30
    g = [svg_open(hgt, "ציר הזמן של רובע שדה דב מ-2019 עד היום, והמכרזים שנסגרים עד דצמבר 2026")]
    g.append(tx(xr, 24, "ציר הזמן של הרובע", size=16, w=600))
    g.append(tx(xr, 46, "תכניות, מכרזים והיתרים, לפי הרישומים הרשמיים", size=13, fill=INK2))
    y = 80
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (xa, y - 8, xa, y + len(MIL) * 25 - 14, DEEP))
    for r in rows:
        if r is None:
            g.append(tx(xr, y + 6, "המכרזים הפתוחים, לפי רשות מקרקעי ישראל:", size=13, w=600, fill=SEA)); y += 25; continue
        d, s = r; future = d > "2026-10-26"
        g.append('<circle cx="%d" cy="%d" r="5" fill="%s" stroke="%s" stroke-width="2"/>' % (xa, y, "#fff" if future else DEEP, SEA if future else DEEP))
        g.append(tx(xr, y + 5, dmy(d), size=13, mono=True, fill=INK2))
        g.append(tx(xa - 12, y + 5, s, size=13, w=600 if "נכנסה לתוקף" in s or "המכרז הראשון" in s else 400))
        y += 25
    g.append("</svg>")
    return "".join(g)


def fig(svg, cap): return '<figure class="nls1-fig">%s<figcaption>%s</figcaption></figure>\n' % (svg, cap)


TID = [0]
def table(caption, head, rows, minw=560, num_=False):
    TID[0] += 1; tid = "s1t%d" % TID[0]
    h = "".join('<th scope="col">%s</th>' % c for c in head)
    b = "".join('<tr><th scope="row">%s</th>%s</tr>' % (r[0], "".join("<td>%s</td>" % c for c in r[1:])) for r in rows)
    return ('<p class="nls1-cap" id="%s">%s</p>\n<div class="nls1-t"><table dir="rtl" aria-labelledby="%s"%s style="min-width:%dpx"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>\n'
            % (tid, caption, tid, ' class="nls1-num"' if num_ else "", minw, h, b))


def link(text, href): return '<a href="%s">%s</a>' % (href, text)


# ------------------------------------------------------------------ T1: the three plans (two official sources side by side)
C = D["compounds"]; DI = D["district"]
def g(c, k): v = (C[c].get("gis") or {}).get(k); return num(v) if v else "לא רשום"
T1 = table("שלוש התכניות של רובע שדה דב: מה מותר לבנות בכל מתחם",
           ["", "מתחם אשכול", "מרכז הרובע", "צפון הרובע"],
           [["התכנית", "תמ\"ל/3001", "תא/1/4444", "תא/2/4444"],
            ["בתוקף מ־", dmy(C["eshkol"]["inForce"]), dmy(C["merkaz"]["inForce"]), dmy(C["tzafon"]["inForce"])],
            ["יחידות דיור (עמוד הרובע)", "כ־4,800", "כ־7,100", "כ־4,000"],
            ["יחידות דיור (רישום התכניות)", "לא רשום", g("merkaz", "units"), g("tzafon", "units")],
            ["דיור מיוחד, יחידות", "לא רשום", g("merkaz", "special"), g("tzafon", "special")],
            ["דירות להשכרה בתכנית", g("eshkol", "rent"), g("merkaz", "rent"), "לא רשום"],
            ["דיור בהישג יד", g("eshkol", "afford"), g("merkaz", "afford"), g("tzafon", "afford")],
            ["מסחר, מ״ר", "כ־45,000", "כ־60,000", "כ־20,000"],
            ["תעסוקה, מ״ר", "כ־145,000", "כ־155,000", "כ־30,000"],
            ["חדרי מלון", "לא פורסם", "כ־800", "כ־1,150"],
            ["מגרשים למגורים ששווקו", str(sum(1 for p in RES_PLOTS_WON if BY[p]["c"] == "eshkol")), str(sum(1 for p in RES_PLOTS_WON if BY[p]["c"] == "merkaz")), str(sum(1 for p in RES_PLOTS_WON if BY[p]["c"] == "tzafon"))],
            ["יח״ד במכרזים", num(C["eshkol"]["tenderUnits"]), num(C["merkaz"]["tenderUnits"]), num(C["tzafon"]["tenderUnits"])],
            ["מגרשים בבנייה", str(C["eshkol"]["byStage"][5]), str(C["merkaz"]["byStage"][5]), str(C["tzafon"]["byStage"][5])]], 600)

# ------------------------------------------------------------------ T2: every tendered plot (RMI)
def who(pid, t):
    return (link(NAMES[pid], BY[pid]["p"]["u"]) + "<br><small>%s</small>" % t["winner"]) if pid in NAMES else t["winner"]
T2R = []
for c in CO:
    for t in sorted([t for t in won if BY[t["plots"][0]]["c"] == c and t["use"] != "מסחר ומשרדים"], key=lambda t: (t["close"], int(t["plots"][0]))):
        pid = t["plots"][0]
        T2R.append([" + ".join(t["plots"]), CN[c].replace("מתחם ", ""), t["use"], num(t["area"]), num(t["units"]), "%s<br><small>%s</small>" % (dmy(t["close"]), t["tender"]), str(t["bids"]),
                    mil(t["bid"]), mil(t["dev"]), mil(per(t), 2), who(pid, t)])
T2 = table("כל המגרשים למגורים שהמדינה שיווקה ברובע: מי זכה, כמה הצעות ובכמה. סכום הזכייה והוצאות הפיתוח במיליוני ₪; \"ליחידה\" הוא הקרקע עם הפיתוח חלקי יחידות הדיור, החישוב שלנו",
           ["מגרש", "מתחם", "יעוד", "שטח, מ״ר", "יח״ד", "נסגר", "הצעות", "זכייה", "פיתוח", "ליחידה", "הזוכה או הפרויקט"], T2R, 920, True)
NOBID = "; ".join("מגרש %s (%s יחידות דיור, מכרז %s, %s)" % (t["plots"][0], num(t["units"]), t["tender"], dmy(t["close"])) for t in nob)

# ------------------------------------------------------------------ T3: open tenders now
T3R = []
for t in sorted(opn, key=lambda t: t["close"]):
    T3R.append([" + ".join(t["plots"]), CN[BY[t["plots"][0]]["c"]], t["use"], num(t["units"]) if t["units"] else "לא רלוונטי", dmy(t["close"]), t["tender"]])
T3 = table("המגרשים שבמכרז פתוח עכשיו ברובע שדה דב", ["מגרש", "מתחם", "יעוד", "יח״ד", "המועד האחרון להגשה", "מכרז"], T3R, 560)

# ------------------------------------------------------------------ T4: green line stations
T4R = []
for n in ("זהרה לביטוב", "איינשטיין", "נופי ים", "פרופס", "לוי אשכול"):
    s = STN[n]
    T4R.append([n, "בתוך הרובע" if s["in"] else "ממזרח לרובע, על הקו", str(s["plots400"]), num(s["units400"])])
T4 = table("תחנות הקו הירוק ברובע ולידו: כמה מגרשים ויחידות דיור ממכרזי המדינה נמצאים עד 400 מ׳ מכל תחנה (החישוב שלנו)",
           ["תחנה", "מיקום", "מגרשים עד 400 מ׳", "יח״ד ממכרזים עד 400 מ׳"], T4R, 520)

# ------------------------------------------------------------------ T5: official medians around the district
QM = {"03": "ינואר עד מרץ", "06": "אפריל עד יוני", "09": "יולי עד ספטמבר", "12": "אוקטובר עד דצמבר"}
def ql(q): y, m = q.split("-"); return QM[m] + " " + y
T5R = []
for nb in sorted(FX["neighbourhoods"], key=lambda r: -(r["rooms"].get("all") or {}).get("v", 0)):
    a = nb["rooms"].get("all")
    if nb["n"] == "אזור שדה דב": continue
    if not a: continue
    T5R.append([nb["n"], ils(a["v"]), ql(a["q"]), ils(nb["rooms"]["4"]["v"]) + "<br><small>%s</small>" % ql(nb["rooms"]["4"]["q"]) if "4" in nb["rooms"] else "לא פורסם",
                ("%.2f%%" % float(nb["idx"]["yield"])) if (nb.get("idx") or {}).get("yield") not in (None, "") else "לא פורסם"])
T5 = table("השכונות שסביב רובע שדה דב: המחיר החציוני בעסקאות, לפי אתר הנדל״ן הממשלתי (גרסת 20.8.2026)",
           ["שכונה", "חציון, כל הדירות", "הרבעון", "חציון, 4 חדרים", "תשואת שכירות שנתית באתר"], T5R, 600, True)

# ------------------------------------------------------------------ T6: plan 3700 north of the district
PL = FX["plans"]
T6R = [["3700, צפון מערב תל אביב (תכנית המתאר)", "בתוקף מ־" + dmy(PL["3700"]["inForce"]), "לא רשום", "%s, מהן %s לצמיתות" % (num(PL["3700"]["total_y_diyur_bar_hasaga"]), num(PL["3700"]["diyur_bar_hasaga_yechidot_tz"]))]]
for k in ("3/3700", "4/3700", "5/3700"):
    T6R.append(["%s, %s" % (k, PL[k]["shem_taba"]), "הופקדה ב־" + dmy(PL[k]["deposited"]), num(PL[k]["megurim_yechidot"]), "לא רשום"])
T6 = table("תכנית 3700 מצפון לרובע: התכניות ומספר יחידות הדיור, לפי רישום התכניות של העירייה", ["התכנית", "הסטטוס", "יחידות דיור", "דיור בהישג יד"], T6R, 560)

# ------------------------------------------------------------------ T7: what to check at each stage
T7 = table("מה לבקש מהמוכר בכל שלב של המגרש",
           ["השלב", "המסמך הרשמי", "מה לבקש ולבדוק"],
           [["שווק במכרז", "תוצאות המכרז ברשות מקרקעי ישראל", "את שם החברה הזוכה כפי שנרשם במכרז, ואם היא החברה שחותמת איתכם על החוזה"],
            ["תכנית עיצוב אושרה", "תכנית העיצוב האדריכלי והפיתוח בעירייה", "גובה הבניין, מספר הקומות, קומת הקרקע, הפיתוח סביב, והאם הדירה שלכם מופיעה בה כפי שהוצגה"],
            ["הוגשה בקשה להיתר", "מספר הבקשה להיתר בעירייה", "ממה הבקשה מורכבת: חפירה ודיפון, או הבניין כולו, וכמה יחידות דיור מבוקשות"],
            ["התקבל היתר", "מספר ההיתר ותאריכו", "לאיזה שלב ההיתר: חפירה ודיפון בלבד או בנייה מלאה, ומה תוקפו"],
            ["בבנייה", "רישום אתר הבנייה בעירייה", "שלב העבודות, ליווי בנקאי או ערבויות חוק המכר, ומועד המסירה בחוזה המכר"]], 600)

# ------------------------------------------------------------------ T8: the table behind I1 (every plot, by compound and stage)
T8R = []
for c in CO:
    LL = [r for r in P if r["c"] == c]
    T8R.append([CN[c]] + [str(sum(1 for r in LL if r["s"] == i)) for i in range(6)] + [str(len(LL))])
T8R.append(["כל הרובע"] + [str(sum(1 for r in P if r["s"] == i)) for i in range(6)] + [str(len(P))])
T8 = table("כמה מגרשים בכל שלב, בכל מתחם (כל היעודים: מגורים, מלונאות ותעסוקה), %s" % UPDATED, ["מתחם"] + ST + ["סך הכול"], T8R, 640, True)
STATIC = open(os.path.join(H, "data", "sdplan-static-map.svg"), encoding="utf-8").read()
assert STATIC.startswith("<svg") and "data-sdplot" not in STATIC

# ------------------------------------------------------------------ the new copy
WATXT = urllib.parse.quote("שלום, הגעתי מהמדריך לרובע שדה דב ואשמח לפרטים נוספים")
CSS = ('<style id="nls1-css">.nls1-lead{font-size:18px;line-height:1.75;color:#12202A}'
       '.nls1-cta{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 22px}.nls1-cta a{display:inline-flex;align-items:center;min-height:44px;padding:10px 16px;border-radius:999px;font-weight:600;font-size:15px;text-decoration:none;border:1px solid #2F6F86}'
       '.nls1-cta a.p{background:#2F6F86;color:#fff}.nls1-cta a.s{background:#fff;color:#1F4B5C}'
       '.nls1-t{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 0 10px;border:1px solid #D3DCE2;border-radius:8px}'
       '.nls1-t table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;margin:0}'
       '.nls1-t th,.nls1-t td{padding:8px 10px;font-size:15px;line-height:1.5;vertical-align:top;text-align:right;border-bottom:1px solid #E6ECF0}'
       '.nls1-t thead th{background:#F6F8F9;color:#12202A;font-weight:600;white-space:nowrap}.nls1-t th[scope=row]{font-weight:600;color:#12202A;background:#fff;position:sticky;right:0;z-index:1}'
       '.nls1-num td{white-space:nowrap}.nls1-num td small,.nls1-t small{display:block;white-space:normal;font-size:12.5px;color:#3E4C58;font-weight:400}'
       '.nls1-cap{font-weight:700;color:#12202A;font-size:15px;line-height:1.5;margin:22px 0 8px}'
       '.nls1-fig{margin:22px 0}.nls1-fig figcaption{font-size:14px;color:#3E4C58;margin-top:6px;line-height:1.6}'
       '.nls1-note,.nls1-src{font-size:15px;line-height:1.7;color:#3E4C58}#sdplan-tool{scroll-margin-top:96px;margin:24px 0}'
       'html body .nli .nli-host[data-nli=sdplan] .nli__grid{grid-template-columns:minmax(0,1fr);gap:20px}'
       'html body .nli .nli-host[data-nli=sdplan] .nli__form{grid-template-columns:repeat(auto-fit,minmax(200px,1fr));align-items:end}'
       'html body .nli .nli-host[data-nli=sdplan] .nli__figure svg{max-width:760px}'
       '@media(max-width:600px){.nls1-t th[scope=row]{max-width:42vw;white-space:normal}.nls1-lead{font-size:17px}.nls1-t th,.nls1-t td{font-size:14px;padding:7px 8px}}</style>\n')

LEAD = (CSS +
        '<p class="nls1-lead" dir="rtl"><strong>על חוף צפון תל אביב, משכונת כוכב הצפון ועד רחוב פרופס, נבנה רובע שדה דב</strong>: כ־16,000 דירות לכ־40,000 תושבים על כ־1,300 דונם, בשלושה מתחמים (אשכול, מרכז הרובע וצפון הרובע), עם 4 תחנות של הקו הירוק. '
        'עד היום שיווקה רשות מקרקעי ישראל %d מגרשים למגורים עם %s יחידות דיור, ובשמונה מגרשים כבר בונים. כאן תמצאו כל מגרש, מי זכה בו ובכמה, באיזה שלב הוא היום בעירייה, ואילו פרויקטים בשיווק.</p>\n'
        % (len(RES_PLOTS_WON), num(U_ALL)) +
        '<div class="nls1-cta"><a class="p" href="#sdplan-tool">לכל המגרשים ברובע</a><a class="s" href="/sde-dov/prices/">מחירי דירות בשדה דב</a>'
        '<a class="s" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">לקבלת פרטים נוספים בוואטסאפ</a></div>\n' % (WA, WATXT))

TOOL = (
    '<h2 dir="rtl">כל מגרש ברובע שדה דב: השלב שלו היום</h2>\n'
    '<p dir="rtl">רובע שדה דב בנוי מ־%d מגרשים למגורים, למלונאות ולתעסוקה בשלוש תכניות. לכל אחד יש מסלול רשמי: מכרז של רשות מקרקעי ישראל (או בעלי קרקע פרטיים), תכנית עיצוב אדריכלי שהעירייה מאשרת, בקשה להיתר, היתר ותחילת עבודות. '
    'נכון ל־%s: %d מגרשים בבנייה, %d עם תכנית עיצוב מאושרת שעוד לא הגיעו להיתר, ו־%d מגרשים במכרז פתוח. בחרו מגרש, וקבלו את כל הרישומים שלו במקום אחד.</p>\n'
    % (len(P), UPDATED, len(UNDER), sum(1 for r in P if r["s"] == 2), sum(1 for r in P if r.get("open"))) +
    '<div id="sdplan-tool">\n[nadlan_tool id="sdplan"]\n</div>\n' +
    fig(svg_stages(), "צפון הרובע ומרכז הרובע שווקו ב־2025, ורוב המגרשים שלהם כבר עם תכנית עיצוב מאושרת. במתחם אשכול, ששווק ב־2021, הבנייה כבר התחילה בשמונה מגרשים. המקורות: רשות מקרקעי ישראל ורישומי התכניות, ההיתרים ואתרי הבנייה של עיריית תל אביב-יפו, %s." % UPDATED) +
    T8 +
    '<h2 dir="rtl">רובע שדה דב במספרים: שלוש התכניות</h2>\n'
    '<p dir="rtl">תכנית המתאר תא/4444 נכנסה לתוקף ב־%s וחילקה את הרובע לשלוש תכניות מפורטות. בעמוד הרובע של העירייה: כ־16,000 דירות, כ־126,000 מ״ר מסחר, כ־330,000 מ״ר תעסוקה לכ־15,000 עובדים, כ־2,000 חדרי מלון לאורך חזית הים, '
    'כ־7,000 דירות לאוכלוסיות שיתקשו לקנות או לשכור בתנאי השוק (מהן כ־2,100 דירות בהישג יד בבעלות העירייה, להשכרה לצמיתות) ו־3 מגרשים לדיור מוגן עם כ־900 יחידות. ברישום התכניות של העירייה רשומים מספרים מפורטים יותר לכל תכנית, ולכן בטבלה שני המקורות זה לצד זה:</p>\n'
    % dmy(DI["inForce"]) + T1 + '<p class="nls1-note" dir="rtl">"עמוד הרובע": עמוד רובע שדה דב באתר העירייה, שבו המספרים מעוגלים. "רישום התכניות": הנתונים של כל תכנית באתר המפות של העירייה. מסחר, תעסוקה וחדרי מלון לפי עמוד הרובע.</p>\n' +
    '<p class="nls1-note" dir="rtl">בבנייה המרקמית הגובה עד 9 קומות, ובין הבניינים משולבים מגדלים. בתכנית מרכז הרובע: בנייה של כ־9 קומות, בניינים של 15 עד 18 ושל 25 עד 30 קומות, ומגדלים של כ־45 קומות (המסמך הסביבתי של התכנית, נובמבר 2024). '
    'פינוי האשפה ברובע יהיה בצנרת תת־קרקעית, ובכל מגרש חלה חובה לייצר אנרגיה מתחדשת.</p>\n'
    '<h2 dir="rtl">מכרזי שדה דב: מי זכה בכל מגרש ובכמה</h2>\n'
    '<p dir="rtl">רשות מקרקעי ישראל שיווקה ברובע %d מגרשים למגורים עם %s יחידות דיור: %s דירות למכירה, %s דירות להשכרה ו־%s יחידות דיור מוגן. סכום ההצעות הזוכות, כולל 4 מגרשי תעסוקה ומסחר במתחם אשכול, הוא כ־%s מיליארד ₪, ועוד כ־%s מיליארד ₪ הוצאות פיתוח. '
    'רק בפברואר ובמרץ 2025 נסגרו 8 מכרזים עם 6,666 יחידות דיור. בשני מכרזים לא הוגשו הצעות: %s.</p>\n'
    % (len(RES_PLOTS_WON), num(U_ALL), num(U_SALE), num(U_RENT), num(U_SEN), ("%.1f" % (BIDS / 1e9)), ("%.1f" % (DEV / 1e9)), NOBID) + T2 +
    fig(svg_land(), "במכרזי 2021 במתחם אשכול עלתה הקרקע עם הפיתוח כ־%s מיליון ₪ ליחידת דיור בממוצע משוקלל, ובמכרזי 2025 במרכז הרובע כ־%s מיליון ₪. בצפון הרובע המגרשים הקטנים שליד הים, עם פחות דירות בכל מגרש, יקרים יותר ליחידה (החישוב שלנו)." % (mil(WAVG["eshkol"], 2), mil(WAVG["merkaz"], 2))) +
    '<p dir="rtl">מחיר הקרקע ליחידה הוא נקודת המוצא של היזם, לא מחיר הדירה: עליו נוספים הבנייה, המימון, המיסים והרווח. המחירים שהיזמים דיווחו על הדירות שנמכרו מרוכזים בעמוד ' + link("מחירי דירות בשדה דב", "/sde-dov/prices/") + '.</p>\n' +
    '<h2 dir="rtl">המכרזים הפתוחים ברובע</h2>\n'
    '<p dir="rtl">%d מגרשים במכרז פתוח עכשיו: מגרש 3204 בצפון הרובע עם 217 יחידות דיור למכירה, מגרש תעסוקה ומסחר במתחם אשכול, ו־5 מגרשי מלונאות במרכז הרובע. המועדים לפי אתר המכרזים של רשות מקרקעי ישראל, %s:</p>\n'
    % (len(set(p for t in opn for p in t["plots"])), UPDATED) + T3 +
    fig(svg_timeline(), "מהפקדת התכנית ב־2019 ועד היום. המכרזים הפתוחים נסגרים בנובמבר ובדצמבר 2026.") +
    '<p class="nls1-src" dir="rtl"><strong>שיטה ומקורות.</strong> המגרשים, היעודים והשטחים מ<a href="https://gisn.tel-aviv.gov.il/iview2js4/index.aspx" target="_blank" rel="noopener">אתר המפות (GIS) של עיריית תל אביב-יפו</a> (רישום המגרשים, התכניות ותכניות העיצוב, הבקשות וההיתרים ואתרי הבנייה), '
    'תוצאות המכרזים מ<a href="https://apps.land.gov.il/MichrazimSite/" target="_blank" rel="noopener">אתר המכרזים של רשות מקרקעי ישראל</a>, נתוני הרובע מ<a href="https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx" target="_blank" rel="noopener">עמוד רובע שדה דב של העירייה</a>, ומספרי התכניות מ<a href="https://mavat.iplan.gov.il/" target="_blank" rel="noopener">מינהל התכנון</a>. '
    'השלב של מגרש הוא הרישום הרשמי האחרון שנמצא לו. קרקע ופיתוח ליחידה, המרחקים והספירות הם החישוב שלנו; המרחקים בקו אווירי ממרכז המגרש, וקו המים לפי OpenStreetMap. אין כאן מועד מסירה או אכלוס: אף מקור רשמי לא מפרסם אותו למגרש. עודכן %s.</p>\n' % UPDATED)

N3700 = (
    fig(STATIC, "שלושת המתחמים על המפה: כל מגרש בצבע השלב הרשמי שלו היום, %s. הדרום משמאל והצפון מימין, הים למעלה. מקורות: אתר המפות של עיריית תל אביב-יפו, רשות מקרקעי ישראל, קו המים לפי OpenStreetMap." % UPDATED) +
    '<h2 dir="rtl">תכנית 3700: מה מתוכנן מצפון לרובע</h2>\n'
    '<p dir="rtl">מצפון לרחוב פרופס, בין הרובע לגבול הרצליה, חלה תכנית 3700, "צפון מערב תל אביב". היא בתוקף מ־%s, והתכניות המפורטות של המתחמים שלה הופקדו ב־2018. כשמחפשים "שדה דב תוכנית 3700" מתכוונים בדרך כלל אליה: זו תכנית נפרדת מהרובע, עם מכרזים ולוח זמנים משלה, אבל היא תמשיך את רצף המגורים לאורך החוף צפונה.</p>\n'
    % dmy(PL["3700"]["inForce"]) + T6)

AROUND = (
    '<h2 dir="rtl">מחירי הדירות בשכונות שסביב רובע שדה דב</h2>\n'
    '<p dir="rtl">לשכונה הרשמית "אזור שדה דב" ב<a href="https://www.nadlan.gov.il/" target="_blank" rel="noopener">אתר הנדל״ן הממשלתי</a> עוד אין מחיר חציוני (גרסת 20.8.2026): העסקאות ברובע הן ברובן רכישות על הנייר בפרויקטים. השכונות הוותיקות שסביבו כבר מפרסמות חציון, וכך הן נראות היום:</p>\n'
    + T5 + '<p class="nls1-note" dir="rtl">חציון של כל הדירות מושפע מתמהיל העסקאות באותו רבעון (גודל הדירות, בנייה חדשה מול ישנה), ובשכונה קטנה מספר עסקאות קטן מזיז אותו הרבה. לכן הרבעון כתוב ליד כל מספר. ההשוואה לפרויקטים ברובע עצמו נמצאת בעמוד ' + link("מחירי דירות בשדה דב", "/sde-dov/prices/") + '.</p>\n')

GREEN = (
    '<h3 dir="rtl">הקו הירוק ברובע: 4 תחנות, ורכבת כל 4 דקות בשעת השיא</h3>\n'
    '<p dir="rtl">לפי העירייה, הקו הירוק של הרכבת הקלה חוצה את הרובע מדרום לצפון בהמשך רחוב אבן גבירול, עם 4 תחנות ברובע: זהרה לביטוב, איינשטיין, נופי ים ופרופס. ליד רחוב איינשטיין הקו מתפצל לכיוון האוניברסיטה ורמת החייל, ובשתי השלוחות יחד מתוכננות 16 רכבות לכל כיוון בשעת השיא. '
    'העירייה כותבת שהקו צפוי לפעול במקביל לתחילת אכלוס הרובע; תאריך פתיחה רשמי לקטע של הרובע לא מצאנו, ולכן אנחנו לא כותבים אותו.</p>\n' + T4)

STAGES = ('<h3 dir="rtl">מה לבדוק לפי השלב של המגרש</h3>\n'
          '<p dir="rtl">השלב הרשמי של המגרש אומר אילו מסמכים כבר קיימים, ואותם אפשר לבקש מהמוכר לפני החתימה. השלב של כל מגרש מופיע ב' + link("רשימת המגרשים בראש העמוד", "#sdplan-tool") + '.</p>\n' + T7)

# ------------------------------------------------------------------ 16 new FAQ (h3 + p), none repeating the 10 on the page
def lst(ids): return ", ".join("%s (מגרש %s)" % (NAMES[i], i) if i in NAMES else "מגרש %s" % i for i in ids)
UND_IDS = [r["id"] for r in sorted(UNDER, key=lambda r: r["works"]["start"] if r.get("works") else "9")]
top_bids = sorted([t for t in won if t["use"] in SALE], key=lambda t: -t["bids"])[:3]
near = sorted([r for r in P if r["use"] == "res" and r.get("t") and r["t"]["use"] in SALE], key=lambda r: r["st"][1])[:3]
sea_min = min((r for r in P if r["use"] in ("res", "special")), key=lambda r: r["sea"]); sea_max = max((r for r in P if r["use"] in ("res", "special")), key=lambda r: r["sea"])
QA_NEW = [
    ("כמה מגרשים שווקו במכרזים ברובע שדה דב?", "רשות מקרקעי ישראל שיווקה ברובע %d מגרשים למגורים עם %s יחידות דיור: %s למכירה, %s להשכרה ו־%s בדיור מוגן, ועוד 4 מגרשי תעסוקה ומסחר. בשני מכרזים לא הוגשו הצעות, ו־%d מגרשים נמצאים במכרז פתוח (רשות מקרקעי ישראל, %s)." % (len(RES_PLOTS_WON), num(U_ALL), num(U_SALE), num(U_RENT), num(U_SEN), len(set(p for t in opn for p in t["plots"])), UPDATED)),
    ("מי זכה במכרזי שדה דב?", "במתחם אשכול (2021 עד 2022) זכו בין היתר אביסרור משה ובניו, משולם לוינשטין עם אלייד ומבנה, שיכון ובינוי וחברות ייעודיות שנרשמו בשמות מדף. במרכז הרובע (2025): האחים ישראל, גינדי ישראל, אלקטרה מגורים עם נהור, קבוצת חג'ג', לוזון רונסון, פרשקובסקי מניבים ועוד. בצפון הרובע (2025): י.ח דמרי, אביב מגורים, שיכון ובינוי, יורו ישראל ואחרים. הרשימה המלאה, מגרש אחר מגרש, בטבלת המכרזים בעמוד."),
    ("כמה עלתה הקרקע ליחידת דיור בשדה דב?", "בחישוב שלנו לפי תוצאות המכרזים, סכום הזכייה עם הוצאות הפיתוח חלקי יחידות הדיור: במכרזי 2021 במתחם אשכול כ־%s מיליון ₪ ליחידה בממוצע משוקלל, במכרזי 2025 במרכז הרובע כ־%s מיליון ₪, ובצפון הרובע כ־%s מיליון ₪. זה מחיר הקרקע ליזם, לפני בנייה, מימון ומיסים, ולא מחיר הדירה." % (mil(WAVG["eshkol"], 2), mil(WAVG["merkaz"], 2), mil(WAVG["tzafon"], 2))),
    ("באילו מגרשים כבר בונים ברובע שדה דב?", "לפי רישום אתרי הבנייה וההיתרים של העירייה, ב־%s העבודות התחילו ב־%d מגרשים, כולם במתחם אשכול: %s." % (UPDATED, len(UNDER), lst(UND_IDS))),
    ("מה השלב של כל מגרש ברובע?", "השלב נקבע לפי הרישום הרשמי האחרון: מכרז ברשות מקרקעי ישראל, תכנית עיצוב שאושרה בעירייה, בקשה להיתר, היתר ותחילת עבודות. ב־%s: %d מגרשים בבנייה, %d עם תכנית עיצוב מאושרת, %d אחרי מכרז בלי תכנית עיצוב, והשאר עדיין בתכנית בלבד. השלב של כל מגרש מופיע ברשימת המגרשים בעמוד." % (UPDATED, len(UNDER), sum(1 for r in P if r["s"] == 2), sum(1 for r in P if r["s"] == 1))),
    ("אילו תחנות של הקו הירוק יהיו ברובע שדה דב?", "לפי העירייה, 4 תחנות בתוך הרובע: זהרה לביטוב, איינשטיין, נופי ים ופרופס, לאורך המשך רחוב אבן גבירול. תחנת לוי אשכול נמצאת ממזרח לרובע, על הקו. בשתי השלוחות של הקו מתוכננות 16 רכבות לכל כיוון בשעת השיא."),
    ("מתי הקו הירוק יגיע לשדה דב?", "העירייה כותבת שהקו צפוי לפעול במקביל לתחילת אכלוס הרובע. תאריך פתיחה רשמי לקטע של הרובע לא מצאנו, ולכן לא נכתוב אותו. מה שאפשר לבדוק כבר היום הוא המרחק מהמגרש לתחנה הקרובה, והוא מופיע לכל מגרש ברשימת המגרשים."),
    ("איזה מגרש קרוב לתחנת רכבת?", "מבין המגרשים לדירות למכירה ששווקו, הקרובים ביותר לתחנה הם %s, בקו אווירי. המרחק של כל מגרש מופיע ברשימת המגרשים, ואפשר לסדר אותה לפי המרחק לתחנה." % "; ".join("מגרש %s%s, כ־%s מ׳ מתחנת %s" % (r["id"], " (%s)" % NAMES[r["id"]] if r["id"] in NAMES else "", num(r["st"][1]), r["st"][0]) for r in near)),
    ("כמה רחוק רובע שדה דב מהים?", "בחישוב שלנו, בקו אווירי ממרכז המגרש לקו המים: המגרש למגורים הקרוב ביותר לים הוא מגרש %s, כ־%s מ׳, והרחוק ביותר מגרש %s, כ־%s מ׳. לאורך החוף מתוכנן הפארק החופי, ולכן אין בניינים על קו המים עצמו." % (sea_min["id"], num(sea_min["sea"]), sea_max["id"], num(sea_max["sea"]))),
    ("מה זה תוכנית 3700?", "תכנית 3700, \"צפון מערב תל אביב\", חלה מצפון לרובע שדה דב ועד גבול הרצליה. היא בתוקף מ־%s, ותכניות המתחמים שלה הופקדו ב־2018: מתחם 3 עם %s יחידות דיור, מתחם 4 עם %s ומתחם 5 עם %s (רישום התכניות של העירייה). זו תכנית נפרדת מהרובע." % (dmy(PL["3700"]["inForce"]), num(PL["3/3700"]["megurim_yechidot"]), num(PL["4/3700"]["megurim_yechidot"]), num(PL["5/3700"]["megurim_yechidot"]))),
    ("מה ההבדל בין תכנית 4444 לתמ\"ל 3001?", "תכנית 4444 היא תכנית המתאר של כל הרובע (בתוקף מ־%s): היא קובעת את ההיקפים ואת העקרונות. כדי לבנות צריך תכנית מפורטת לכל מתחם: תמ\"ל 3001 למתחם אשכול (מ־%s), תא/1/4444 למרכז הרובע (מ־%s) ותא/2/4444 לצפון הרובע (מ־%s). מכוחן מוציאים היתרים." % (dmy(DI["inForce"]), dmy(C["eshkol"]["inForce"]), dmy(C["merkaz"]["inForce"]), dmy(C["tzafon"]["inForce"]))),
    ("מה זו תכנית עיצוב אדריכלי, ולמה היא חשובה למי שקונה דירה?", "תכנית עיצוב אדריכלי ופיתוח היא מסמך שהעירייה מאשרת לכל מגרש אחרי התכנית המפורטת: היא קובעת את הבינוי, גובה הבניינים, קומת הקרקע והפיתוח סביב. בלי תכנית עיצוב מאושרת אין בקשה להיתר. לפני חתימה כדאי לבקש אותה ולבדוק שהבניין והדירה תואמים למה שהוצג בשיווק."),
    ("האם אפשר לקנות קרקע בשדה דב?", "מגרשי המדינה נמכרים במכרזים של רשות מקרקעי ישראל, ובחלקם אפשר להגיש הצעה גם כקבוצת רוכשים. היום פתוחים מכרז למגרש 3204 בצפון הרובע (217 יחידות דיור, עד 7.12.2026), למגרש תעסוקה ומסחר במתחם אשכול (עד 30.11.2026) ולחמישה מגרשי מלונאות (עד 16.11.2026). מגרשים שלא שווקו במכרזים שייכים לבעלי קרקע פרטיים או ממתינים לשיווק."),
    ("כמה דירות להשכרה יהיו ברובע שדה דב?", "במכרזי רשות מקרקעי ישראל שווקו %s דירות להשכרה ב־7 מגרשים: 109 ו־106 במתחם אשכול, 2102, 2203 ו־2207 במרכז הרובע, ו־3202, 3209 ו־3208 בצפון הרובע. במגרש 109 העבודות כבר התחילו." % num(U_RENT)),
    ("איפה יהיה דיור מוגן ברובע שדה דב?", "במכרזים שווקו שני מגרשים לדיור מוגן: מגרש 150 בצפון הרובע עם 300 יחידות, ומגרש 2104 במרכז הרובע עם 350 יחידות (רשות מקרקעי ישראל). לפי העירייה, ברובע מתוכננים 3 מגרשים לדיור מוגן עם כ־900 יחידות."),
    ("כמה הצעות הוגשו במכרזי שדה דב?", "במכרזי הדירות למכירה התחרות הייתה גבוהה: %s. במכרזי הדירות להשכרה הוגשו 1 עד 7 הצעות למגרש, ובשני מכרזים לא הוגשה אף הצעה." % "; ".join("מגרש %s קיבל %d הצעות" % (t["plots"][0], t["bids"]) for t in top_bids)),
]
FAQ_NEW = "".join('<h3 dir="rtl">%s</h3>\n<p dir="rtl">%s</p>\n' % (q, a) for q, a in QA_NEW)

SECTIONS = {
    "after_h1": LEAD,
    "before_history": TOOL,
    "before_projects": N3700,
    "before_transport": AROUND,
    "before_affordable": GREEN,
    "before_legal": STAGES,
    "before_summary": FAQ_NEW,
}

# ------------------------------------------------------------------ gates on the new copy
def visible(h):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", h, flags=re.S); h = re.sub(r"\[nadlan_tool[^\]]*\]", " ", h)
    return re.sub(r"\s+", " ", HT.unescape(re.sub(r"<[^>]+>", " ", h))) + " " + " ".join(re.findall(r'aria-label="([^"]*)"', h))
NEW = "".join(SECTIONS.values()); NV = visible(NEW)
BANNED = r"ממשק|מערכת|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה|טעון אימות|מודל|מנגנון|שכב|הדגמה|טכנולוגי|יחסית|כמעט|אטלס|Atlas|פיילוט|פרוטוטייפ|רספונסיבי|מובייל|אפס |זיהום|מזוהמ|PFAS|תלת ממד|לחיצ"
assert not re.search(r"[–—]", NV), re.findall(r".{20}[–—].{20}", NV)[:3]
hits = re.findall(r".{0,25}(?:%s).{0,25}" % BANNED, NV); assert not hits, hits[:5]
assert not re.search(r"(?<![\d.,])0 (₪|חדרים|מגרשים|יח)", NV)
assert "<h1" not in NEW
for sv in re.findall(r"<svg\b.*?</svg>", NEW, flags=re.S):
    assert min(float(x) for x in re.findall(r"font-size:([\d.]+)px", sv)) >= 12 and 'viewBox="0 0 420 ' in sv and 'direction="rtl"' in sv
assert len(QA_NEW) == 16 and len(set(q for q, a in QA_NEW)) == 16
OLDQ = ["איפה נמצא רובע שדה דב?", "כמה דירות מתוכננות בשדה דב?", "מתי צפוי האכלוס בשדה דב?", "כמה עולה דירה בשדה דב?", "מה זה מתחם אשכול בשדה דב?", "מי היזמים הבולטים בשדה דב?", "האם כדאי להשקיע בשדה דב?", "האם יש דיור בר-השגה בשדה דב?", "מה צריך לבדוק לפני חתימה על דירה בשדה דב?", "האם דמי הניהול בשדה דב צפויים להיות גבוהים?"]
assert not set(q for q, a in QA_NEW) & set(OLDQ)
for cap in re.findall(r'<p class="nls1-cap"[^>]*>(.*?)</p>', NEW):
    if "ליחידה" in cap or "400 מ׳" in cap: assert "החישוב שלנו" in cap, cap
words = len(re.findall(r"[\w֐-׿\"'״]+", visible(re.sub(r"<svg\b.*?</svg>", " ", NEW, flags=re.S))))
print("new copy: %d words | tables %d | cells %d | svg %d | h2 %d | h3 %d | FAQ new %d | figures in text %d" % (
    words, NEW.count("<table"), len(re.findall(r"<t[dh][ >]", re.sub(r"<svg\b.*?</svg>", "", NEW, flags=re.S))), NEW.count("<svg"), NEW.count("<h2"), NEW.count("<h3"), len(QA_NEW),
    len(re.findall(r"\d[\d,.]*", re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|svg)\b.*?</\1>", " ", NEW, flags=re.S))))))
io.open(os.path.join(H, "data", "s1-sections.json"), "w", encoding="utf-8").write(json.dumps(SECTIONS, ensure_ascii=False, indent=1))

# ------------------------------------------------------------------ local previews
PV = os.path.join(H, "preview"); os.makedirs(PV, exist_ok=True)
A = "../../../../../plugins/nadlan-config/assets/instruments/"
TOOLHTML = ('<section class="nli" dir="rtl" lang="he" aria-label="כל מגרש ברובע שדה דב"><div class="nli-host" data-nli="sdplan" data-nli-data="../data/sdplan.json"><div class="nli__panel"><p class="nli__kicker">מגרש אחר מגרש · רובע שדה דב</p>'
            '<h2 class="nli__title">כל מגרש ברובע שדה דב: מי זכה בו, בכמה, ובאיזה שלב הוא היום</h2></div></div></section>')
HEAD = ('<!doctype html>\n<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>%s</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;800&family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
        '<link rel="stylesheet" href="%score.css?ver=local"><style>html,body{margin:0;background:#fff;color:#12202A;font:16px/1.7 Heebo,Arial,sans-serif}main{padding:0 16px}main>*{max-width:760px;margin-left:auto;margin-right:auto}'
        'h1{font:800 30px/1.25 Heebo,sans-serif;margin:24px auto 8px}h2{font:700 24px/1.3 Heebo,sans-serif;margin:30px auto 10px}h3{font:700 19px/1.35 Heebo,sans-serif;margin:22px auto 8px}img{max-width:100%%;height:auto}table{border-collapse:collapse}'
        '.nlam{display:none!important}.nlsdt{display:none}</style></head><body><main>' % ("רובע שדה דב · תצוגה מקומית S1", A))
FOOT = '</main><script src="%score.js?ver=local" defer></script><script src="../tool/sdplan.js?ver=local" defer></script></body></html>' % A
io.open(os.path.join(PV, "s1-new-sections.html"), "w", encoding="utf-8", newline="").write(
    HEAD + '<h1>רובע שדה דב: פרויקטים ודירות למכירה</h1>' + "".join(SECTIONS[k] for k in SECTIONS).replace('[nadlan_tool id="sdplan"]', TOOLHTML) + FOOT)
# the live hub content (REST rendered, 26.10.2026) with the fragments at the same anchors
live = io.open(os.path.join(RAW, "ours-rest-4730-rendered.html"), encoding="utf-8").read()
ANCH = {"after_h1": '<h1 class="wp-block-heading nlseo-h1-v1">רובע שדה דב: פרויקטים ודירות למכירה</h1>',
        "before_history": '<h2 dir="rtl">ההיסטוריה: משדה התעופה דב הוז לרובע החדש</h2>', "before_projects": '<h2 dir="rtl">הפרויקטים בשיווק ברובע</h2>',
        "before_transport": '<h2 dir="rtl">תחבורה, פארקים, חופים ומבני ציבור</h2>', "before_affordable": '<h2 dir="rtl">דיור בר-השגה ודיור מיוחד</h2>',
        "before_legal": '<h2 dir="rtl">בדיקות משפטיות לפני רכישה על הנייר בשדה דב</h2>', "before_summary": '<h2 dir="rtl">סיכום קצר</h2>'}
page = live
for k, a in ANCH.items():
    assert page.count(a) == 1, ("anchor", k, page.count(a))
    page = page.replace(a, a + SECTIONS[k]) if k.startswith("after") else page.replace(a, SECTIONS[k] + a)
page = page.replace('[nadlan_tool id="sdplan"]', TOOLHTML)
io.open(os.path.join(PV, "s1-page-render.html"), "w", encoding="utf-8", newline="").write(HEAD + page + FOOT)
print("wrote data/s1-sections.json, preview/s1-new-sections.html, preview/s1-page-render.html (7 anchors matched once in the served content)")
