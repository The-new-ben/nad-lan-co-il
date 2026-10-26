# -*- coding: utf-8 -*-
"""G1 on /dira-behanacha/ (page 8541): the full upgrade for "מחיר למשתכן" (90,500 searches a month) and "דירה בהנחה" (74,000).
Spec: dna.md (this folder), sections 6 (verified facts), 7 (gaps) and 8 (build spec). NOT RUN against the live site by the
research session (owner order 26.10.2026: local only). The releaser runs it after the release that ships the two new tools.

Additive law: no existing paragraph, table, link or tool loses its text. The only edits inside existing text:
  1. a stale future-tense sentence (certificates "אמורה להיפתח מחדש ב־5.10.2026", a date that has passed);
  2. "הקובץ הפתוח עדיין לא כולל את מסלול המילואים, ולכן הכלי לא מחשב אותו" now points to the new check that does use the
     ministry's reserve figures.
What it adds, every number computed here from plugins/nadlan-config/assets/instruments/data/dira-round.json (built by
tools/instruments/build_dira_round.py, checked by tools/instruments/test_dirafit.js) or a dated official fact of dna.md section 6:
  TOP (before the old first paragraph): answer paragraph for both head terms, CTA row, [nadlan_tool id="dirafit"], T1 today's numbers;
  after "מה זו דירה בהנחה": the four tracks and the name (T2);
  before "בני מקום ומשרתי מילואים": round 11 in every town (V1 + T3) and the rounds since 2022 (V2 + T4);
  before "איך בוחרים שלוש ערים": priorities and quotas (V3 + T5);
  before "מי זכאי לדירה בהנחה": the three-town list in numbers;
  before "ההגרלה האחרונה וההגרלה הבאה": the eligibility matrix (T6) and the certificate (T7);
  before "מה קורה אחרי הזכייה": what to check before round 12 (official status only);
  before "שאלות נפוצות": the money section with [nadlan_tool id="diracost"], the price against the town's deal prices (T8), the
     financing rules (T9) and the path from certificate to keys (V4);
  after the last old FAQ answer: 22 new FAQ (8 old + 22 = 30, none repeated), then "שיטה ומקורות" with the update date.
Title, H1 and meta (kw_guard OK, dna.md 8.1) are written with the content. Each anchor must match exactly once. Language law
asserted on the visible new text (incl. SVG text and aria labels). Every internal link must answer 200 without a redirect.
  python write_g1_page.py --dry --from ../../2026-10-22-dira-behanacha/page.html   (offline: no REST at all; writes preview/)
  python write_g1_page.py --dry       (GET the live content over REST, write preview/, post nothing)
  python write_g1_page.py             (backup, POST content + title + Yoast meta, read back, live check)"""
import io, json, os, re, statistics, sys, time, urllib.error, urllib.parse, urllib.request

H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
DRY = "--dry" in sys.argv
FROM = sys.argv[sys.argv.index("--from") + 1] if "--from" in sys.argv else None
NOLINKS = "--no-links" in sys.argv
PID = 8541; SITE = "https://nad-lan.co.il"; WA = "972525101555"; UPDATED = "26.10.2026"
TITLE = "דירה בהנחה (מחיר למשתכן): מי זכאי, ההגרלות והסיכוי לזכות בכל עיר"
SEO_T = "מחיר למשתכן ודירה בהנחה 2026: זכאות, הגרלות וסיכויים"
SEO_D = "דירה בהנחה ומחיר למשתכן 2026: בדיקת זכאות, שלוש הערים עם הסיכוי הגבוה, ההגרלה ה־11 בכל עיר, מילואים 18.6%, המחיר מול העסקאות בעיר והצעדים עד המפתח."
OLD_TITLE = "דירה בהנחה: מה הסיכוי לזכות בהגרלה, בכל עיר"
assert len(SEO_T) <= 60 and len(SEO_D) <= 160, (len(SEO_T), len(SEO_D))

# ------------------------------------------------------------------ data
DP = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")
D = json.load(io.open(os.path.join(DP, "dira-round.json"), encoding="utf-8"))
B = json.load(io.open(os.path.join(DP, "boi-mortgage.json"), encoding="utf-8"))
PT = json.load(io.open(os.path.join(DP, "ptax.json"), encoding="utf-8"))
R11, RL, T_ = D["r11"], D["rules"], D["towns"]
MON = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]
QM = {"03": "ינואר עד מרץ", "06": "אפריל עד יוני", "09": "יולי עד ספטמבר", "12": "אוקטובר עד דצמבר"}


def qlab(q): y, m = q.split("-"); return QM[m] + " " + y
def dmy(s): y, m, d = s[:10].split("-"); return "%d.%d.%s" % (int(d), int(m), y)
def num(n): return "{:,}".format(int(round(n)))
def ils(n): return num(n) + " ₪"
def pct(x, d=1): return ("%." + str(d) + "f%%") % (100 * x)
def med(a): return statistics.median(a) if a else None


TOWN = {t["n"]: t for t in T_}
BY = sorted(T_, key=lambda t: -t["per100"])
G_ALL = R11["units"] / R11["households"]; G_RES = R11["res_wins"] / R11["res_regs"]
G_REST = (R11["units"] - R11["res_wins"]) / (R11["households"] - R11["res_regs"]); PERHH = R11["town_regs"] / R11["households"]
L22 = [dict(zip(D["lots22"]["cols"], r)) for r in D["lots22"]["rows"]]
ODDS22 = [x["wins"] / x["subs"] for x in L22]
RD = {r["n"]: r for r in D["rounds"]}
RATE = B["rates"]["fixed_nl"]["rate"]; RATE_M = B["rates"]["fixed_nl"]["hist"][-1][0]


def pmt(P, r=RATE, years=25): i = r / 1200; return P * i / (1 - (1 + i) ** (-12 * years))


def cost(pm, size=100, vat=True):
    price = pm * size * (1.18 if vat else 1); cap = RL["ltv"] * price
    return {"price": price, "cap": cap, "own": price - cap, "pay": pmt(cap)}


# T8 rows: the towns of round 11 whose last price per m2 in the file is from 2024 or 2025, against the town's 4-room deal median
REC = [t for t in T_ if t.get("pm") and t["pm"]["date"] >= "2024-01-01" and t.get("mkt") and "4" in t["mkt"]]
for t in REC:
    c = cost(t["pm"]["v"]); m = t["mkt"]["4"]; t["_c"] = c; t["_gap"] = (m["price"] - c["price"]) / m["price"]
REC.sort(key=lambda t: t["_gap"])
OLDP = [t for t in T_ if t.get("pm") and t["pm"]["date"] < "2024-01-01"]
NOMKT = [t for t in T_ if t.get("pm") and t["pm"]["date"] >= "2024-01-01" and not (t.get("mkt") and "4" in t["mkt"])]

# ------------------------------------------------------------------ cross-check: the figures of test_dirafit.js and the releases
def same(name, got, want): assert got == want, ("cross-check", name, got, want)
same("flats", sum(t["units"] for t in T_), 7922); same("lotteries", sum(t["lots"] for t in T_), 82); same("town regs", R11["town_regs"], 313415)
same("all", round(100 * G_ALL, 1), 6.9); same("reserve", round(100 * G_RES, 1), 18.6); same("others", round(100 * G_REST, 2), 3.56); same("towns per household", round(PERHH, 2), 2.73)
same("top three", [t["n"] for t in BY[:3]], ["כפר מנדא", "מעלה אדומים", "קריית גת"]); same("bottom", [t["n"] for t in BY[-2:]], ["ראשון לציון", "רחובות"])
same("file lotteries", D["file"]["n"], 2352); same("file newest", D["file"]["last"], "2025-01-27"); same("since 2022", len(L22), 635)
same("median since 2022", round(100 * med(ODDS22), 2), 0.60); same("round 1", round(100 * RD[1]["odds"], 2), 1.14); same("round 9", round(100 * RD[9]["odds"], 2), 0.29)
same("Kiryat Gat price", round(cost(11802)["price"]), 1392636); same("rate", RATE, 4.62)
same("recent price towns", [t["n"] for t in REC], ["קריית גת", "ראשון לציון", "אילת", "רחובות", "כפר סבא", "בית שמש"])
same("Kiryat Gat gap", round(100 * TOWN["קריית גת"]["_gap"], 1), 3.5); same("Beit Shemesh gap", round(100 * TOWN["בית שמש"]["_gap"], 1), 40.6)

# ------------------------------------------------------------------ SVG (NadLan Instruments: ink, sea, deep, line; survey red only for a warning)
FONT = "font-family:'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif"
MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"
INK, INK2, SEA, DEEP, RED, LINE, MUTE = "#12202A", "#3E4C58", "#2F6F86", "#1F4B5C", "#C42550", "#D3DCE2", "#5E6A75"


def tx(x, y, s, anchor="start", size=13, weight=400, fill=INK, mono=False, halo=False):
    """direction is rtl on the svg: anchor start = the right end of the text sits at x."""
    assert size >= 12, "svg text below 12px"
    st = "%s;font-size:%spx;font-weight:%s" % (MONO if mono else FONT, size, weight)
    if halo: st += ";paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-linejoin:round"
    return '<text x="%.1f" y="%.1f" text-anchor="%s" style="%s" fill="%s">%s</text>' % (x, y, anchor, st, fill, s)


def svg_open(h, label):
    return '<svg viewBox="0 0 420 %d" direction="rtl" role="img" aria-label="%s" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">' % (h, label)


def svg_towns():
    """V1: flats per 100 households registered in each town, round 11 (the 23.6.2026 table), 19 towns ranked."""
    xr, x1, xmin, vmax, H0, rh = 408, 300, 70, 8.5, 92, 21
    sc = (x1 - xmin) / vmax; yend = H0 + len(BY) * rh; hgt = yend + 64
    allc = 100 * R11["units"] / R11["town_regs"]
    g = [svg_open(hgt, "דירות לכל 100 משקי בית שנרשמו בכל עיר בהגרלה ה־11: הגבוה %s ב%s, הנמוך %s ב%s" % (num1(BY[0]["per100"]), BY[0]["n"], num2(BY[-1]["per100"]), BY[-1]["n"]))]
    g.append(tx(xr, 24, "ההגרלה ה־11: דירות לכל 100 נרשמים בעיר", size=16, weight=600))
    g.append(tx(xr, 46, "19 יישובים, 7,922 דירות, לפי הודעת משרד הבינוי והשיכון", size=13, fill=INK2))
    g.append(tx(xr, 66, "מ־23.6.2026. הקו המקווקו: כל הערים יחד", size=13, fill=INK2))
    xa = x1 - sc * allc
    g.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.2" stroke-dasharray="4 3"/>' % (xa, H0 - 6, xa, yend + 2, INK))
    g.append(tx(xa - 4, H0 - 9, "%s" % num1(allc), size=12, mono=True, fill=INK2))
    y = H0
    for i, t in enumerate(BY):
        w = sc * t["per100"]; col = DEEP if i < 3 else SEA
        g.append(tx(xr, y + 14, t["n"], size=13, weight=500 if i < 3 else 400))
        g.append('<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s"%s/>' % (x1 - w, y + 3, w, col, "" if i < 3 else ' fill-opacity=".72"'))
        g.append(tx(x1 - w - 5, y + 14, num1(t["per100"]) if t["per100"] >= 1 else num2(t["per100"]), size=12.5, mono=True, halo=True))
        y += rh
    g.append(tx(xr, yend + 24, "דירות בעיר חלקי משקי הבית שנרשמו להגרלות בה. משק בית נרשם", size=12, fill=INK2))
    g.append(tx(xr, yend + 42, "לעד 3 ערים וזוכה לכל היותר פעם אחת. החישוב שלנו.", size=12, fill=INK2))
    return "".join(g) + "</svg>"


def num1(x): return ("%.1f" % x)
def num2(x): return ("%.2f" % x)


def svg_rounds():
    """V2: the median odds of a single lottery in each round since March 2022 (rounds 1 to 9 from the official file)."""
    rs = [RD[n] for n in range(1, 10)]
    left, right, top, base = 30, 370, 96, 250
    vmax = 0.0125; bw = (right - left) / len(rs)
    g = [svg_open(330, "הסיכוי בהגרלה טיפוסית בכל סבב של דירה בהנחה מ־2022: מ־%s במרץ 2022 עד %s בדצמבר 2024" % (pct(rs[0]["odds"], 2), pct(rs[-1]["odds"], 2)))]
    g.append(tx(408, 24, "הסיכוי בהגרלה טיפוסית, לפי סבב", size=16, weight=600))
    g.append(tx(408, 46, "חציון זוכים חלקי נרשמים בכל הגרלה, סבבים 1 עד 9", size=13, fill=INK2))
    g.append(tx(408, 66, "הקובץ הרשמי, 635 הגרלות. החישוב שלנו.", size=13, fill=INK2))
    for v in (0.005, 0.01):
        y = base - (base - top) * v / vmax
        g.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>' % (left, y, right, y, LINE))
        g.append(tx(416, y + 4, pct(v, 1), size=12, mono=True, fill=MUTE))
    for i, r in enumerate(rs):
        xc = right - bw * (i + 0.5); h = (base - top) * r["odds"] / vmax
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (xc - bw * 0.32, base - h, bw * 0.64, h, DEEP if i in (0, len(rs) - 1) else SEA))
        g.append(tx(xc, base - h - 6, pct(r["odds"], 2), anchor="middle", size=12, mono=True, halo=True))
        g.append(tx(xc, base + 18, str(r["n"]), anchor="middle", size=13, weight=600))
        g.append(tx(xc, base + 34, r["label"].split(" ")[1][2:], anchor="middle", size=12, fill=MUTE, mono=True))
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2"/>' % (left, base, right, base, INK))
    g.append(tx(408, 304, "מספר הסבב ושנתו. הסבבים 10 ו־11 עוד לא נכנסו לקובץ.", size=12, fill=INK2))
    return "".join(g) + "</svg>"


def svg_groups():
    """V3: how many of each group won in round 11 (2.8.2026 release; the rest is our calculation)."""
    rows = [("משרתי מילואים", G_RES, "%s זכו מתוך %s" % (num(R11["res_wins"]), num(R11["res_regs"])), DEEP),
            ("כל משקי הבית", G_ALL, "%s דירות, %s משקי בית" % (num(R11["units"]), num(R11["households"])), SEA),
            ("כל השאר", G_REST, "החישוב שלנו", MUTE)]
    x1, xmin, vmax = 270, 40, 0.20; sc = (x1 - xmin) / vmax
    g = [svg_open(230, "בהגרלה ה־11 זכו %s ממשרתי המילואים שנרשמו, %s מכלל משקי הבית ו־%s מכל השאר" % (pct(G_RES), pct(G_ALL), pct(G_REST)))]
    g.append(tx(408, 24, "מי זכה בהגרלה ה־11", size=16, weight=600))
    g.append(tx(408, 46, "זוכים מכל 100 משקי בית שנרשמו, לפי קבוצה", size=13, fill=INK2))
    y = 74
    for lab, v, sub, col in rows:
        w = sc * v
        g.append(tx(408, y + 16, lab, size=14, weight=600)); g.append(tx(408, y + 34, sub, size=12, fill=INK2))
        g.append('<rect x="%.1f" y="%d" width="%.1f" height="22" fill="%s"/>' % (x1 - w, y + 4, w, col))
        g.append(tx(x1 - w - 6, y + 21, pct(v), size=14, weight=600, mono=True, halo=True))
        y += 48
    g.append(tx(408, 222, "מקור: משרד הבינוי והשיכון, 23.6.2026 ו־2.8.2026", size=12, fill=MUTE))
    return "".join(g) + "</svg>"


def svg_path():
    """V4: from certificate to keys, with the official durations."""
    steps = [("אישור זכאות", "200 ₪, עד 10 ימי עבודה"), ("הרשמה באתר ההגרלות", "עד 3 יישובים, לכל ההגרלות בהם"), ("ההגרלה", "הגרלה על התור לבחירת דירה"),
             ("תוצאות", "מסרון, דואר אלקטרוני, האזור האישי"), ("היתר בנייה", "לפי המדריך: זמן רב"), ("בחירת דירה", "לפי סדר הזכייה, 45 דקות"),
             ("חוזה עם היזם", "בתוך 30 ימי עבודה מהבחירה"), ("איסור מכירה", "5 שנים מטופס 4 או 7 מההגרלה")]
    top, gap = 78, 40; hgt = top + gap * len(steps) + 14
    g = [svg_open(hgt, "הדרך לדירה בהנחה בשמונה שלבים, מאישור הזכאות ועד איסור המכירה")]
    g.append(tx(408, 24, "מהזכאות ועד המפתח", size=16, weight=600))
    g.append(tx(408, 46, "השלבים והזמנים לפי משרד הבינוי והשיכון", size=13, fill=INK2))
    xl = 392
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (xl, top, xl, top + gap * (len(steps) - 1), LINE))
    for i, (a, b) in enumerate(steps):
        y = top + gap * i
        last = i == len(steps) - 1
        g.append('<circle cx="%d" cy="%d" r="9" fill="%s" stroke="%s" stroke-width="2"/>' % (xl, y, "#fff" if last else SEA, RED if last else SEA))
        g.append(tx(xl, y + 4.5, str(i + 1), anchor="middle", size=12, weight=600, fill=RED if last else "#fff", mono=True))
        g.append(tx(374, y + 1, a, size=14, weight=600, fill=RED if last else INK)); g.append(tx(374, y + 18, b, size=12.5, fill=INK2))
    return "".join(g) + "</svg>"


def fig(svg, cap): return '<figure class="nlg1-fig">%s<figcaption>%s</figcaption></figure>\n' % (svg, cap)


def table(cap, head, rows, num_cols=(), note=""):
    th = "".join('<th scope="col">%s</th>' % h for h in head)
    body = ""
    for r in rows:
        cells = []
        for i, c in enumerate(r):
            if i == 0: cells.append('<th scope="row">%s</th>' % c)
            else: cells.append('<td%s>%s</td>' % (' class="n"' if i in num_cols else "", c))
        body += "<tr>" + "".join(cells) + "</tr>"
    return ('<p class="nlg1-cap">%s</p><div class="nlg1-t"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>\n' % (cap, th, body)
            + ('<p class="nlg1-note">%s</p>\n' % note if note else ""))


# ------------------------------------------------------------------ tables
T1 = table("המספרים של היום (נבדק 26.10.2026)", ["מה", "המספר", "מקור ותאריך"], [
    ["דירות בהגרלה האחרונה (ה־11)", "7,922 ב־19 יישובים, 82 הגרלות", "משרד הבינוי והשיכון, 25.5.2026"],
    ["משקי בית שנרשמו", "114,848, שביצעו כ־1.7 מיליון הרשמות", "משרד הבינוי והשיכון, 23.6.2026"],
    ["זכו מכלל משקי הבית", pct(G_ALL), "7,922 דירות חלקי 114,848 משקי בית"],
    ["משרתי מילואים", "זכו %s: %s מתוך %s" % (pct(G_RES), num(R11["res_wins"]), num(R11["res_regs"])), "משרד הבינוי והשיכון, 2.8.2026"],
    ["כל השאר", "זכו %s" % pct(G_REST), "החישוב שלנו מאותן הודעות"],
    ["אישור זכאות", "200 ₪, עד 10 ימי עבודה, תוקף שנה, חידוש 50 ₪", "gov.il, עודכן 24.9.2026"],
    ["כמה ערים אפשר לבחור", "עד 3 יישובים, לכל ההגרלות בהם", "משרד הבינוי והשיכון, 25.5.2026"],
    ["משכנתא לזכאים", "עד 75% מהמחיר, או לפי שווי שמאי עם 100,000 ₪ הון עצמי ושווי עד 2.1 מיליון ₪", "gov.il, עודכן 24.2.2026"],
    ["מענק", "40,000 או 60,000 ₪ ביישובים מזכים", "gov.il, עודכן 24.2.2026"],
    ["ההגרלה הבאה", "אין הודעה רשמית על מועד, ערים או מספר דירות", "עמוד דירה בהנחה, gov.il, נבדק 26.10.2026"]])

T2 = table("ארבעת המסלולים של דירה בהנחה", ["מסלול", "איך נקבע המחיר", "מי נרשם", "מענק במסלול"], [
    ["מחיר למשתכן", "הקבלן זוכה בקרקע לפי המחיר הנמוך ביותר למ״ר שהוא מציע לזכאים", "חסרי דירה; משפרי דיור בהגרלות המשך", "40,000 או 60,000 ₪ ביישובים מזכים"],
    ["מחיר מטרה", "המחיר נקבע כהנחה ממחיר השוק של הדירה, לפי שמאות", "חסרי דירה; משפרי דיור בהגרלות המשך", "40,000 ₪"],
    ["מחיר מופחת", "מחיר מופחת שנקבע במכרז הקרקע", "חסרי דירה; משפרי דיור בהגרלות המשך", "40,000 ₪"],
    ["דירה להשכיר", "שכירות לטווח ארוך, באתר נפרד של התוכנית", "לפי תנאי המסלול", "אין"]],
    note="השם הכולל והמסלולים: עמוד דירה בהנחה של משרד הבינוי והשיכון. המענקים: עמוד ההטבות במימון (עודכן 24.2.2026). אופן קביעת המחיר: לפי תנאי המכרזים של רשות מקרקעי ישראל, כפי שהם מתוארים בפרסומים הציבוריים.")

T3R = []
for t in BY:
    h = t["hist"]
    T3R.append([t["n"], str(t["order"]), str(t["lots"]), num(t["units"]), num(t["hh"]), num1(t["per100"]) if t["per100"] >= 1 else num2(t["per100"]),
                (pct(h["odds"], 2) if h["odds"] is not None else "אין הגרלות") + ("<small>%d הגרלות</small>" % h["n"] if h["n"] else ""),
                pct(h["lodds"], 2) if h["lodds"] is not None else "אין"])
T3 = table("ההגרלה ה־11 בכל עיר, מהגבוה לנמוך", ["עיר", "סדר ההגרלה", "הגרלות", "דירות", "משקי בית שנרשמו", "דירות לכל 100 נרשמים", "הסיכוי בהגרלה בקובץ (חציון)", "בני מקום בקובץ"],
           T3R, num_cols=(1, 2, 3, 4, 5, 6, 7),
           note="דירות, הגרלות ומשקי בית: הודעות משרד הבינוי והשיכון מ־25.5 ומ־23.6.2026. דירות לכל 100 נרשמים: החישוב שלנו. הסיכוי בקובץ: החציון של כל הגרלות העיר בקובץ הרשמי, %s עד %s. מזכרת בתיה לא הופיעה בקובץ עד ינואר 2025." % (dmy(D["file"]["first"]), dmy(D["file"]["last"])))

T4R = []
for n in range(1, 12):
    r = RD[n]
    if r["src"] == "file":
        T4R.append([str(n), r["label"], str(r["towns"]), str(r["lotteries"]), num(r["units"]), num(r["regs"]), num(r["wins"]), pct(r["odds"], 2)])
    elif n == 10:
        T4R.append([str(n), r["label"], str(r["towns"]), "", num(r["units"]), "", "", "עוד לא בקובץ"])
    else:
        T4R.append([str(n), r["label"], str(r["towns"]), str(r["lotteries"]), num(r["units"]), "%s משקי בית" % num(r["households"]), "", "%s ממשקי הבית" % pct(r["odds_hh"])])
T4 = table("כל סבבי דירה בהנחה מ־2022", ["סבב", "נפתח", "יישובים", "הגרלות", "דירות", "הרשמות", "זוכים", "הסיכוי בהגרלה טיפוסית"], T4R, num_cols=(2, 3, 4, 5, 6, 7),
           note="סבבים 1 עד 9: הקובץ הרשמי (הרשמה נספרת בכל הגרלה שמשק הבית נרשם אליה). סבב 10: 7,479 דירות ב־21 יישובים, לפי הודעת משרד הבינוי והשיכון שצוטטה בעיתונות; הקובץ עוד לא כולל אותו. סבב 11: הודעות משרד הבינוי והשיכון. הסיכוי בהגרלה טיפוסית: החישוב שלנו.")

# T10: every lottery of rounds 1 to 9 (the official file), collapsed: the "רשימת הגרלות" / "טבלת דירות מחיר למשתכן" searches
T10R = []
for x in sorted(L22, key=lambda x: (x["round"], x["town"], x["date"], x["hood"])):
    T10R.append([x["town"], str(x["round"]), x["hood"] or "", dmy(x["date"]), num(x["units"]), num(x["subs"]), num(x["wins"]), pct(x["wins"] / x["subs"], 2), ils(x["pm"]) if x["pm"] else ""])
T10 = ('<details class="nlg1-more"><summary>כל %s ההגרלות של סבבים 1 עד 9, לפי סבב ועיר</summary>\n' % num(len(L22)) +
       table("ההגרלות של דירה בהנחה, מרץ 2022 עד דצמבר 2024, מהקובץ הרשמי", ["עיר", "סבב", "שכונה", "תאריך ההגרלה", "דירות", "נרשמים", "זוכים", "סיכוי", "מחיר למ״ר"], T10R, num_cols=(1, 3, 4, 5, 6, 7, 8),
             note="מקור: הקובץ של תוכנית דירה בהנחה ב־data.gov.il, עודכן %s. סיכוי: זוכים חלקי נרשמים, החישוב שלנו. מחיר למ״ר לפני מע״מ." % dmy(D["file"]["modified"])) + "</details>\n")

T5 = table("מי מקבל עדיפות בהגרלה ובכמה דירות", ["העדיפות", "למי", "כמה דירות"], [
    ["ראשונה", "נכה רתוק (80% עד 100% נכות, מרותק לכיסא גלגלים), ואחריו בן משפחה מדרגה ראשונה שגר איתו", "דירה אחת לכל 30 דירות, ולפחות אחת"],
    ["שנייה, ביישובי פריפריה 1 עד 4 באזור עדיפות לאומית", "משרתי מילואים פעילים", "עד 50% מהדירות, מתוכן עד 25% קודם ללוחמים"],
    ["שנייה, בשאר היישובים", "משרתי מילואים פעילים", "עד 35% מהדירות, מתוכן עד 15% קודם ללוחמים"],
    ["שלישית", "בני מקום", "עד 20% מהדירות; בפריפריה, כל העדיפויות יחד עד 73%"],
    ["בהגרלה ה־11 בפועל", "משרתי מילואים פעילים", "כ־50% מהדירות, כמחצית מהן ללוחמים"]],
    note="הכללים במסלול מחיר מטרה: עמוד הזכאות של משרד הבינוי והשיכון, עודכן 26.5.2026. ההגרלה ה־11: הודעות 25.5, 23.6 ו־2.8.2026.")

T6 = table("טבלת הזכאות: מי נרשם לאיזו הגרלה", ["המצב שלכם", "חסרי דירה", "משפרי דיור", "מה צריך לדעת"], [
    ["זוג נשוי או ידועים בציבור", "כן", "רק הגרלות המשך", "המצב האישי צריך להיות מעודכן במשרד הפנים"],
    ["זוג שמתחתן בתוך 3 חודשים", "כן", "רק הגרלות המשך", "בלי חתונה בתוך 3 חודשים הזכאות והזכייה מתבטלות"],
    ["יחיד או יחידה מגיל 35", "כן", "רק הגרלות המשך", ""],
    ["הורה עם ילד רווק מתחת לגיל 21", "כן", "רק הגרלות המשך", "תצהיר שלילדים אין ולא הייתה דירה ב־3 השנים האחרונות"],
    ["הורה גרוש מתחת לגיל 35 שהילדים לא בחזקתו", "כן", "רק הגרלות המשך", ""],
    ["אזרח ישראלי הנשוי לאזרח חוץ", "כן", "רק הגרלות המשך", "תצהיר חתום בפני עורך דין"],
    ["יחיד מגיל 21 עם נכות מוכרת או אלמן", "כן", "רק הגרלות המשך", "נכות 75% לצמיתות, או מעל 50% עם קצבת ניידות; נכה רתוק מקבל עדיפות"],
    ["יחיד מתחת לגיל 35 בלי ילדים", "לא", "לא", "לא מופיע ברשימת הזכאים"],
    ["החזיק שתי דירות במקביל שנה ב־3 השנים האחרונות", "לא", "לא", ""],
    ["קנה או זכה בעבר בתוכנית של מחיר מפוקח", "לא", "לא", "גם לא כמשפר דיור"],
    ["חבר קיבוץ", "לא", "לא", ""]],
    note="חסר דירה: אין ולא הייתה לו דירה, או יותר משליש דירה, ב־3 השנים האחרונות, וכך גם ביום החוזה. משפר דיור: בעל דירה יחידה, שחייב למכור אותה בתוך 12 חודשים מהאכלוס. לכולם: היחיד או כל אחד מבני הזוג לא מוגדרים כחייבי גיוס שלא הסדירו את מעמדם. מקור: עמוד הזכאות של משרד הבינוי והשיכון, עודכן 26.5.2026.")

T7 = table("אישור זכאות: איפה, כמה ומתי", ["חברת ההרשמה", "טלפון", "עלות", "זמן טיפול", "תוקף", "חידוש לפני שפג"], [
    [c[0], c[1], "200 ₪", "עד 10 ימי עבודה", "שנה", "50 ₪"] for c in RL["cert"]["companies"]],
    num_cols=(1,), note="אישור שפג תוקפו מנפיקים מחדש ב־200 ₪. משפרי דיור מחדשים מ־1.1.2025 בעצמם, מול חברת ההרשמה. מוקד הסיוע בדיור של משרד הבינוי והשיכון: 5442*, ימים א׳ עד ה׳, 8:30 עד 16:00. מקורות: הודעת משרד הבינוי והשיכון 25.5.2026, gov.il.")

T8R = []
for t in REC:
    m = t["mkt"]["4"]; c = t["_c"]
    T8R.append([('<a href="%s">%s</a>' % (t["page"], t["n"])) if t.get("page") else t["n"], ils(t["pm"]["v"]), dmy(t["pm"]["date"]), ils(c["price"]), ils(m["price"]), qlab(m["q"]), pct(t["_gap"])])
T8 = table("המחיר בהגרלה מול חציון העסקאות בעיר: דירת 100 מ״ר מול דירות 4 חדרים", ["עיר", "מחיר למ״ר בהגרלה האחרונה בקובץ", "תאריך ההגרלה", "דירת 100 מ״ר עם מע״מ", "חציון העסקאות, 4 חדרים", "רבעון", "הפער"],
           T8R, num_cols=(1, 3, 4, 6),
           note="רק ערי ההגרלה ה־11 שבהן המחיר האחרון בקובץ הוא מ־2024 או 2025. 100 מ״ר הוא דוגמה, והמחיר למ״ר לפני מע״מ, כמו שהוא מוצג בעמודי הפרויקטים; בחישוב הוספנו 18%%. חציון העסקאות כולל דירות יד שנייה. החישוב שלנו, לפי הקובץ הרשמי של התוכנית ואתר הנדל״ן הממשלתי (גרסה %s)." % D["inv"]["version"])

T9 = table("המימון של זוכה בדירה בהנחה", ["הכלל", "מה זה אומר", "מקור"], [
    ["משכנתא עד 75% מהמחיר", "על דירה של %s צריך לפחות %s הון עצמי" % (ils(TOWN["קריית גת"]["_c"]["price"]), ils(TOWN["קריית גת"]["_c"]["own"])), "הנחיות בנק ישראל, gov.il 24.2.2026"],
    ["משכנתא לפי שווי שמאי", "באישור בנק ישראל: לפי שווי השוק, עם 100,000 ₪ הון עצמי לפחות, כשהשווי עד 2.1 מיליון ₪", "gov.il 24.2.2026"],
    ["מענק", "40,000 או 60,000 ₪ במחיר למשתכן ביישובים מזכים, 40,000 ₪ במחיר מטרה ובמחיר מופחת; משתחרר אחרי ההון העצמי", "gov.il 24.2.2026"],
    ["משכנתא לזכאים מהמדינה", "לחסרי דירה 10 שנים: ריבית נמוכה ב־0.5% מהממוצע על משכנתאות צמודות, עד 3.0%, ל־10 עד 30 שנה", "gov.il 24.2.2026"],
    ["ההחזר החודשי", "%s על משכנתא של %s, בריבית הממוצעת %s%% ל־25 שנה (החישוב שלנו)" % (ils(TOWN["קריית גת"]["_c"]["pay"]), ils(TOWN["קריית גת"]["_c"]["cap"]), RATE), "בנק ישראל, ממוצע קבועה לא צמודה %s" % ".".join(str(int(x)) for x in RATE_M.split("-")[::-1])],
    ["מס רכישה", "דירה יחידה פטורה עד %s" % ils(PT["tracks"]["single"][0][0]), "רשות המסים"],
    ["איסור מכירה", "5 שנים מטופס 4 או 7 שנים מיום ההגרלה, המוקדם מביניהם", "המדריך להשתתפות, gov.il"]])

# ------------------------------------------------------------------ the new copy
WATXT = urllib.parse.quote("שלום, הגעתי מהמדריך דירה בהנחה ואשמח לפרטים נוספים")
CSS = ('<style id="nlg1-css">.nlg1-lead{font-size:18px;line-height:1.75}'
       '.nlg1-cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px;margin-bottom:8px}'
       '.nlg1-cta a{display:inline-flex;align-items:center;min-height:48px;padding:10px 18px;border-radius:6px;border:1.5px solid #1F4B5C;color:#1F4B5C;font-weight:700;text-decoration:none;font-size:16px;line-height:1.3}'
       '.nlg1-cta a.is-primary{background:#1F4B5C;color:#fff}.nlg1-cta a:focus-visible{outline:3px solid #2F6F86;outline-offset:2px}'
       '.nlg1-t{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:0;margin-bottom:10px}'
       '.nlg1-t table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;font-size:15px;line-height:1.5}'
       '.nlg1-t th,.nlg1-t td{padding:8px 10px;border-bottom:1px solid #D3DCE2;text-align:right;vertical-align:top}'
       '.nlg1-t thead th{background:#F6F8F9;color:#12202A;font-weight:700;font-size:14px}'
       '.nlg1-t tbody th{font-weight:600;color:#12202A;background:#fff;position:sticky;right:0;z-index:1}'
       '.nlg1-t td.n{white-space:nowrap;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:14px}'
       '.nlg1-t td small{display:block;font-size:12.5px;color:#5E6A75;font-family:inherit}'
       '.nlg1-cap{font-weight:700;color:#12202A;font-size:15px;line-height:1.5;margin-top:22px;margin-bottom:8px}'
       '.nlg1-note,.nlg1-src{font-size:15px;line-height:1.7;color:#3E4C58}'
       '.nlg1-fig{margin-top:22px;margin-bottom:22px}.nlg1-fig figcaption{font-size:14px;color:#3E4C58;margin-top:6px;line-height:1.6}'
       '.nlg1-check{padding-right:1.2em}.nlg1-check li{margin:6px 0}'
       '.nlg1-more{margin-top:16px;margin-bottom:16px}.nlg1-more>summary{cursor:pointer;font-weight:700;font-size:16px;line-height:1.5;color:#1F4B5C;padding:12px 0;min-height:44px}'
       '#nlg1-fit,#nlg1-cost{scroll-margin-top:96px}'
       '@media(max-width:600px){.nlg1-t table{font-size:14px}.nlg1-t th,.nlg1-t td{padding:7px 8px}}</style>\n')

LEAD = ('<p class="nlg1-lead"><strong>דירה בהנחה</strong> היא תוכנית הדיור של משרד הבינוי והשיכון ורשות מקרקעי ישראל, שמוכרת לזכאים חסרי דירה דירות חדשות מקבלן במחיר מופחת, '
        'בהגרלה. <strong>מחיר למשתכן</strong> הוא השם הקודם שלה, והיום הוא אחד מארבעה מסלולים בתוכה, לצד מחיר מטרה, מחיר מופחת ודירה להשכיר. בהגרלה האחרונה, ה־11, '
        'נרשמו %s משקי בית ל־%s דירות ב־19 יישובים, וזכו %s מהם; משרתי מילואים זכו ב־%s. על ההגרלה ה־12 עוד אין הודעה רשמית.</p>\n'
        % (num(R11["households"]), num(R11["units"]), pct(G_ALL), pct(G_RES)))
CTA = ('<div class="nlg1-cta"><a class="is-primary" href="#nlg1-fit">לבדיקת הזכאות והערים שלכם</a>'
       '<a href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">לקבלת פרטים נוספים בוואטסאפ</a>'
       '<a href="/real-estate-lawyer/">פגישה עם עורך דין מקרקעין</a></div>\n' % (WA, WATXT))
TOP = (CSS + LEAD + CTA +
       '<p>ארבע שאלות, והבדיקה מראה אם אתם זכאים לפי ההגדרות של משרד הבינוי והשיכון, אילו עדיפויות יש לכם, ואילו שלוש ערים נתנו הכי הרבה דירות לכל משק בית שנרשם בהגרלה האחרונה. '
       'גרים באחת מערי ההגרלה? סמנו אותה, והעיר שלכם תעלה לראש הרשימה כשיש לה תוצאות של בני מקום.</p>\n'
       '<div id="nlg1-fit"></div>\n[nadlan_tool id="dirafit"]\n'
       '<h2>דירה בהנחה במספרים, אוקטובר 2026</h2>\n'
       '<p>המספרים שקובעים היום כל החלטה על דירה בהנחה: כמה דירות היו בהגרלה האחרונה, כמה נרשמו, כמה זכו בכל קבוצה, כמה עולה אישור הזכאות ומה כללי המימון. כל מספר עם המקור והתאריך שלו.</p>\n'
       + T1 +
       '<p>הבדיקה המלאה של הסיכוי לפי עיר, הגרלה אחרי הגרלה, נמצאת בכלי שמתחת: בוחרים עיר ורואים כל הגרלה שהייתה בה מאז 2016.</p>\n')

NAMES = ('<h3>מחיר למשתכן, מחיר מטרה ומחיר מופחת: מה ההבדל</h3>\n'
         '<p>מחיר למשתכן הוא השם שבו רוב האנשים עדיין מחפשים את התוכנית, ובצדק: גם אתר ההגרלות של משרד הבינוי והשיכון שמר את השם בכותרת, ובקובץ הרשמי של ההגרלות %s מתוך %s ההגרלות רשומות במסלול מחיר למשתכן. '
         'ההבדל בין המסלולים הוא בדרך שבה נקבע המחיר: במחיר למשתכן הקבלן זוכה בקרקע כשהוא מציע את המחיר הנמוך ביותר למ״ר, ובמחיר מטרה המחיר נקבע כהנחה ממחיר השוק של הדירה, לפי שמאות. '
         'לזכאים התהליך זהה: אישור זכאות, הרשמה באתר ההגרלות, הגרלה על התור ובחירת דירה.</p>\n' % (num(2340), num(D["file"]["n"])) + T2)

R11SEC = ('<h2>ההגרלה ה־11 בכל עיר: דירות, נרשמים וסיכוי</h2>\n'
          '<p>ההגרלה ה־11 נפתחה ב־25.5.2026 ונסגרה ב־22.6.2026, עם %s דירות ב־19 יישובים ו־82 הגרלות. משרד הבינוי והשיכון פרסם כמה משקי בית נרשמו בכל עיר, וזה מאפשר לחשב כמה דירות היו לכל 100 נרשמים. '
          'בראש הרשימה %s, עם %s דירות לכל 100 נרשמים (%s דירות ו־%s משקי בית), %s עם %s ו%s עם %s. בתחתית %s, עם %s בלבד (%s דירות מול %s משקי בית), ו%s עם %s. '
          'בכפר סבא נרשמו הכי הרבה משקי בית, %s, על %s דירות.</p>\n'
          % (num(R11["units"]), BY[0]["n"], num1(BY[0]["per100"]), num(BY[0]["units"]), num(BY[0]["hh"]), BY[1]["n"], num1(BY[1]["per100"]), BY[2]["n"], num1(BY[2]["per100"]),
             BY[-1]["n"], num2(BY[-1]["per100"]), num(BY[-1]["units"]), num(BY[-1]["hh"]), BY[-2]["n"], num2(BY[-2]["per100"]), num(TOWN["כפר סבא"]["hh"]), num(TOWN["כפר סבא"]["units"])) +
          fig(svg_towns(), "בכהה: שלוש הערים עם הכי הרבה דירות לכל 100 נרשמים. כל הנתונים בטבלה.") + T3 +
          '<p>שימו לב לפער בין שני המספרים: בכל עיר נספרים רק משקי הבית שנרשמו אליה, ויחד הערים מגיעות ל־%s הרשמות לעיר מ־%s משקי בית, כלומר כל משק בית נרשם בממוצע ל־%s ערים (החישוב שלנו). '
          'לכן בכל עיר בנפרד יש %s דירות לכל 100 הרשמות לעיר, אבל מכלל משקי הבית זכו %s.</p>\n'
          % (num(R11["town_regs"]), num(R11["households"]), "%.2f" % PERHH, num1(100 * R11["units"] / R11["town_regs"]), pct(G_ALL)) +
          '<h3>כל סבבי דירה בהנחה מ־2022</h3>\n'
          '<p>הקובץ הרשמי של התוכנית ב־data.gov.il כולל %s הגרלות מ־%s עד %s, ומתוכן %s הגרלות בתשעת הסבבים של דירה בהנחה מאז מרץ 2022. בסבבים האלה הוגרלו %s דירות מול %s הרשמות, '
          'והסיכוי בהגרלה טיפוסית ירד מ־%s בסבב הראשון ל־%s בסבב התשיעי, בדצמבר 2024. ב־%s מההגרלות מ־2022 הסיכוי היה מתחת לאחוז אחד (החישוב שלנו). '
          'הקובץ עודכן לאחרונה ב־%s, אבל הסבבים 10 ו־11 עוד לא נכנסו אליו, ולכן את המספרים שלהם הבאנו מהודעות משרד הבינוי והשיכון.</p>\n'
          % (num(D["file"]["n"]), dmy(D["file"]["first"]), dmy(D["file"]["last"]), num(len(L22)), num(sum(x["units"] for x in L22)), num(sum(x["subs"] for x in L22)),
             pct(RD[1]["odds"], 2), pct(RD[9]["odds"], 2), pct(sum(o < 0.01 for o in ODDS22) / len(ODDS22), 0), dmy(D["file"]["modified"])) +
          fig(svg_rounds(), "הסיכוי בהגרלה טיפוסית בכל סבב: זוכים חלקי נרשמים, החציון של הגרלות הסבב.") + T4 + T10)

PRIOR = ('<h2>מילואים, בני מקום ונכים: מי מקבל עדיפות ובכמה</h2>\n'
         '<p>בהגרלה ה־11 נרשמו %s משרתי מילואים פעילים, ו־%s מהם זכו בדירה: %s, פי %s מכל השאר, שבהם זכו %s (החישוב שלנו: %s דירות שלא הלכו למילואים חלקי %s משקי בית). '
         'לפי משרד הבינוי והשיכון, כ־60%% מכלל הזוכים היו משרתי מילואים. העדיפות שמורה למי ששירת 60 ימים לפחות בצו 8 מ־7.10.2023, ואישור זכאות שהונפק עד 5.8.2025 לא נותן אותה. '
         'את ההגדרה בודקים במוקד המילואים, 1111 שלוחה 4, כי לחברות ההרשמה אין את המידע. ההטבות בדיור למשרתי המילואים מרוכזות גם ב<a href="https://www.miluim.idf.il/articles-list/קדימות-בהטבות-דיור/" target="_blank" rel="noopener">אתר המילואים של צה״ל</a>.</p>\n'
         % (num(R11["res_regs"]), num(R11["res_wins"]), pct(G_RES), "%.0f" % (G_RES / G_REST), pct(G_REST), num(R11["units"] - R11["res_wins"]), num(R11["households"] - R11["res_regs"])) +
         fig(svg_groups(), "כל השאר: החישוב שלנו, בהנחה שכל 7,922 הדירות הוגרלו, כמו שעולה מההודעה על כ־60% זוכים ממשרתי המילואים.") + T5)

THREE = ('<h3>שלוש ערים במספרים</h3>\n'
         '<p>בהגרלה ה־11 כל משק בית נרשם בממוצע ל־%s ערים, כלומר רוב הנרשמים מיצו את שלוש האפשרויות. זה מה שהנתונים מלמדים על הבחירה:</p>\n'
         '<ul class="nlg1-check"><li>בני מקום מתחילים מהעיר שלהם: בקריית גת הסיכוי הטיפוסי בקובץ היה %s לכל הנרשמים ו־%s לבני מקום, ביקנעם עלית %s מול %s.</li>'
         '<li>עיר עם הרבה דירות לכל נרשם שווה יותר מעיר עם הרבה דירות: בכפר סבא היו %s דירות, אבל רק %s לכל 100 נרשמים; בכפר מנדא %s דירות ו־%s לכל 100.</li>'
         '<li>בודקים את המחיר למ״ר מול חציון העסקאות בעיר, כי ההנחה לא זהה בכל מקום: בקובץ, הפער נע בין %s ל־%s בערים שבהן יש מחיר מ־2024 או 2025 (בטבלה בפרק המחיר).</li>'
         '<li>משרתי מילואים: העדיפות חלה בכל עיר, ולכן כדאי לשלב עיר אחת שבה הסיכוי הכללי נמוך אבל העיר מתאימה לכם.</li></ul>\n'
         % ("%.2f" % PERHH, pct(TOWN["קריית גת"]["hist"]["odds"], 2), pct(TOWN["קריית גת"]["hist"]["lodds"], 2), pct(TOWN["יקנעם עלית"]["hist"]["odds"], 2), pct(TOWN["יקנעם עלית"]["hist"]["lodds"], 2),
            num(TOWN["כפר סבא"]["units"]), num1(TOWN["כפר סבא"]["per100"]), num(TOWN["כפר מנדא"]["units"]), num1(TOWN["כפר מנדא"]["per100"]), pct(REC[0]["_gap"]), pct(REC[-1]["_gap"])))

ELIG = ('<h3>טבלת הזכאות ואישור הזכאות</h3>\n'
        '<p>אותם כללים בטבלה אחת: מי יכול להירשם להגרלות הראשונות, מי רק להגרלות המשך, ומי לא זכאי בכלל. משפרי דיור נרשמים רק להגרלות המשך שהוגדרו להם, לפי החלטת מועצת מקרקעי ישראל.</p>\n'
        + T6 + T7 +
        '<p>זוג שעומד להתחתן חותם על מסמך זכאות מותנית עם אישור רישום ברבנות, או על תצהיר בפני עורך דין, ומעדכן את הנישואין בתוך 6 חודשים מהנפקת הזכאות. '
        'אזרח ישראלי הנשוי לאזרח חוץ מצרף תצהיר תושב זר. הורה לילד מתחת לגיל 21 ממלא תצהיר בעלויות ילדים. את כל הטפסים מורידים מ<a href="https://www.gov.il/he/pages/tenaey_zkaut" target="_blank" rel="noopener">עמוד הזכאות של משרד הבינוי והשיכון</a>.</p>\n')

NEXT = ('<h3>לפני ההגרלה הבאה: מה לבדוק עכשיו</h3>\n'
        '<p>נכון ל־26.10.2026 אין הודעה רשמית על ההגרלה ה־12: לא מועד, לא רשימת יישובים ולא מספר דירות. את ההגרלה ה־11 הודיע משרד הבינוי והשיכון ב־12.4.2026 לפתיחה ב־15.4.2026, ובפועל ההרשמה נפתחה ב־25.5.2026; '
        'אישורי זכאות אפשר היה להנפיק רק עד 7.6.2026, שבועיים לפני הסגירה. לכן מכינים עכשיו:</p>\n'
        '<ul class="nlg1-check"><li>אישור זכאות בתוקף, אצל מילגם, אלונים או מעוף; חידוש לפני שפג עולה 50 ₪ ואחרי שפג 200 ₪.</li>'
        '<li>משרתי מילואים: בדיקה במוקד המילואים שההגדרה שלכם נכונה, ואישור זכאות שהונפק אחרי 5.8.2025.</li>'
        '<li>שני בני הזוג: מעמד מוסדר מול צה״ל, כי הזכאות מותנית בכך שאיש מכם לא מוגדר כחייב גיוס שלא הסדיר את מעמדו.</li>'
        '<li>כתובת המגורים ברשות האוכלוסין מעודכנת, כדי שמעמד בני המקום יחושב נכון. אין אפשרות לערער עליו.</li>'
        '<li>הון עצמי של 25% מהמחיר, או 100,000 ₪ לפחות למסלול השמאי.</li>'
        '<li>רשימת שלוש ערים, לפי הבדיקה האישית בראש העמוד.</li>'
        '<li>הצטרפות למידעון של משרד הבינוי והשיכון, שם מתפרסמת ההגרלה הבאה, ומעקב אחרי <a href="https://moch.maps.arcgis.com/apps/webappviewer/index.html?id=40c996fd924c46f6815e77a9eef81362" target="_blank" rel="noopener">מפת הפרויקטים הרשמית</a>: בירוק פרויקט פתוח להרשמה, בצהוב פרויקט שייפתח, ובאפור פרויקט שפורסמו תוצאותיו.</li></ul>\n'
        '<p>יש גם דירות בלי הגרלה: בפרויקטים שבהם נשארו דירות, זכאים חסרי דירה ומשפרי דיור פונים ישירות לקבלן, לפי הסדר, עם אישור זכאות בתוקף. '
        'הרשימה מתעדכנת ב<a href="https://www.gov.il/he/pages/mechirat_dirot_lelo_hagralah" target="_blank" rel="noopener">עמוד הדירות ללא הגרלה של משרד הבינוי והשיכון</a>.</p>\n')

MONEY = ('<h2>כמה עולה דירה בהנחה, ומה ההנחה מול מחירי העסקאות</h2>\n'
         '<p>המחיר של דירה בהנחה נקבע במכרז, כמחיר למ״ר שמופיע בעמוד הפרויקט באתר ההגרלות, לפני מע״מ. כדי לדעת אם ההנחה גדולה, משווים את המחיר המלא של הדירה למחיר שבו נמכרות דירות בעיר. '
         'במחשבון מכניסים את המחיר למ״ר ואת השטח, ורואים את המחיר עם מע״מ, את הפער מול חציון העסקאות, את ההון העצמי לפי כללי התוכנית ואת ההחזר החודשי.</p>\n'
         '<div id="nlg1-cost"></div>\n[nadlan_tool id="diracost"]\n'
         '<p>בערי ההגרלה ה־11 שבהן המחיר האחרון בקובץ הוא מ־2024 או 2025, דירת 100 מ״ר במחיר ההגרלה הייתה זולה מחציון העסקאות של דירות 4 חדרים בעיר ב־%s בקריית גת, ועד %s בבית שמש (החישוב שלנו). '
         'בקריית גת, שבה דירה של 4 חדרים נמכרת בחציון ב־%s, דירת 100 מ״ר בהגרלה עלתה %s עם מע״מ. בכפר סבא הפער %s, ובראשון לציון %s. '
         'זה לא אומר שאין הנחה בקריית גת: החציון כולל דירות ישנות, והדירה מההגרלה חדשה. אבל זה אומר שבעיר זולה ההנחה בשקלים קטנה, ובעיר יקרה היא גדולה.</p>\n'
         % (pct(REC[0]["_gap"]), pct(REC[-1]["_gap"]), ils(TOWN["קריית גת"]["mkt"]["4"]["price"]), ils(TOWN["קריית גת"]["_c"]["price"]), pct(TOWN["כפר סבא"]["_gap"]), pct(TOWN["ראשון לציון"]["_gap"]))
         + T8 +
         '<p>%s ערים נוספות מההגרלה ה־11 מופיעות בקובץ רק עם מחירים מ־2023 או מוקדם יותר (%s), ולכן לא השווינו אותן: מחיר ישן מול חציון עסקאות של 2026 היה מראה הנחה שלא קיימת. '
         'ב%s יש מחיר מ־2024 או 2025, אבל אין חציון רשמי של דירות 4 חדרים לרבעון האחרון. במחשבון אפשר להכניס את המחיר מעמוד הפרויקט ולקבל את ההשוואה לכל עיר שיש לה חציון.</p>\n'
         % (len(OLDP), ", ".join("%s %s" % (t["n"], t["pm"]["date"][:4]) for t in sorted(OLDP, key=lambda t: t["pm"]["date"])), ", ב".join(x["n"] for x in NOMKT[:-1]) + " וב" + NOMKT[-1]["n"])
         + T9 + '<p>את ההחזר בכל תמהיל מסלולים, וכמה אפשר ללוות לפי ההכנסה, מחשבים ב<a href="/mortgage-calculator/">מחשבון המשכנתא</a>, ואת ההצמדה של התשלומים לקבלן ב<a href="/new-projects/construction-input-index/">מחשבון ההצמדה למדד תשומות הבנייה</a>.</p>\n' + fig(svg_path(), "השלבים, מהאישור ועד איסור המכירה. בין ההגרלה לבחירת הדירה עוברים בדרך כלל זמן ההיתר וזמן הבנייה."))

QA_NEW = [
    ("מה זה מחיר למשתכן?", "מחיר למשתכן הוא השם המוכר של תוכנית הדיור הממשלתית שבה זכאים חסרי דירה קונים דירה חדשה מקבלן במחיר מופחת, בהגרלה. היום השם הרשמי הוא דירה בהנחה, ומחיר למשתכן הוא אחד מארבעה מסלולים בתוכה, לצד מחיר מטרה, מחיר מופחת ודירה להשכיר."),
    ("מה ההבדל בין מחיר למשתכן לדירה בהנחה?", "דירה בהנחה הוא השם הכולל של כל תוכניות הדיור של משרד הבינוי והשיכון ורשות מקרקעי ישראל, ומחיר למשתכן הוא מסלול אחד בתוכו. ההגרלות, אישור הזכאות ואתר ההרשמה משותפים לכל המסלולים."),
    ("מה ההבדל בין מחיר מטרה למחיר למשתכן?", "במחיר למשתכן הקבלן זוכה בקרקע כשהוא מציע את המחיר הנמוך ביותר למ״ר. במחיר מטרה המחיר נקבע כהנחה ממחיר השוק של הדירה, לפי שמאות. המענק שונה: במחיר למשתכן 40,000 או 60,000 ₪ ביישובים מזכים, ובמחיר מטרה 40,000 ₪."),
    ("מי זכאי לדירה בהנחה?", "חסרי דירה: מי שלא הייתה לו דירה, או יותר משליש דירה, ב־3 השנים האחרונות. במצב משפחתי: זוגות נשואים או ידועים בציבור, זוג שמתחתן בתוך 3 חודשים, יחידים מגיל 35, הורה עם ילד רווק מתחת לגיל 21, נכים ואלמנים מגיל 21, ועוד מקרים בעמוד הזכאות של משרד הבינוי והשיכון. משפרי דיור נרשמים רק להגרלות המשך."),
    ("איך מוציאים אישור זכאות לדירה בהנחה?", "מגישים בקשה באינטרנט דרך אחת מחברות ההרשמה: מילגם (6078*), אלונים (2850*) או מעוף (9344*). העלות 200 ₪, הטיפול עד 10 ימי עבודה, והאישור מגיע בדואר אלקטרוני עם סיסמה זמנית לאתר ההגרלות."),
    ("כמה זמן תקף אישור זכאות?", "שנה. הארכה כשהאישור עדיין בתוקף עולה 50 ₪, ואחרי שפג מנפיקים אישור חדש ב־200 ₪. משפרי דיור מחדשים מ־1.1.2025 בעצמם, מול חברת ההרשמה."),
    ("איך נרשמים להגרלה של דירה בהנחה?", "נכנסים לאתר ההגרלות של משרד הבינוי והשיכון עם תעודת זהות והסיסמה, בוחרים פרויקט ברשימת הפרויקטים הפתוחים, לוחצים על הרשמה ומאשרים את התקנון. מקבלים דואר אלקטרוני שמאשר את ההרשמה. נרשמים רק עם אישור זכאות תקף ביום ההרשמה."),
    ("לכמה ערים אפשר להירשם בהגרלה?", "לעד 3 יישובים, ולכל ההגרלות שבהם. מועד ההרשמה בתוך תקופת ההרשמה לא משנה את הסיכוי. בהגרלה ה־11 כל משק בית נרשם בממוצע ל־%s ערים." % ("%.2f" % PERHH)),
    ("האם ההרשמה להגרלת מחיר למשתכן פתוחה עכשיו?", "לא. נכון ל־26.10.2026 אין הגרלה פתוחה ואין הודעה רשמית על ההגרלה ה־12. ההגרלה ה־11 נסגרה להרשמה ב־22.6.2026 ונערכה ב־26.7.2026."),
    ("באילו ערים הייתה ההגרלה האחרונה?", "ההגרלה ה־11 נערכה ב־19 יישובים: ראשון לציון, אשדוד, בית שמש, רחובות, חדרה, כפר סבא, קריית גת, נהריה, אילת, מעלה אדומים, יהוד, יקנעם עלית, קדימה צורן, כפר מנדא, מזכרת בתיה, רכסים, בית דגן, בני עי״ש ובת חפר. על ערי ההגרלה הבאה אין עדיין הודעה רשמית."),
    ("איך נכנסים לאזור האישי באתר ההגרלות?", "בכניסה הראשונה מקלידים את מספר תעודת הזהות ואת הסיסמה הזמנית שהגיעה עם אישור הזכאות, ומחליפים אותה לסיסמה קבועה. אם הסיסמה לא מתקבלת, לוחצים על שכחתי סיסמה, ואם זה לא עוזר פונים לחברת ההרשמה שהנפיקה את האישור."),
    ("מה הסיכוי של משרת מילואים לזכות בדירה בהנחה?", "בהגרלה ה־11 נרשמו %s משרתי מילואים פעילים ו־%s מהם זכו, %s. משאר משקי הבית זכו כ־%s (החישוב שלנו), כלומר הסיכוי של משרת מילואים היה גבוה פי %s." % (num(R11["res_regs"]), num(R11["res_wins"]), pct(G_RES), pct(G_REST), "%.0f" % (G_RES / G_REST))),
    ("מי נחשב בן מקום?", "מי שגר בתחום הרשות שבה נבנה הפרויקט ב־3 השנים האחרונות, או 4 מתוך 10 השנים האחרונות. משרד הבינוי והשיכון בודק את הכתובות של כל בן זוג בנפרד לפי רשות האוכלוסין, ואין אפשרות לערער. בני מקום מקבלים עד 20% מהדירות."),
    ("כמה דירות מוקצות למשרתי מילואים?", "במסלול מחיר מטרה, ביישובי פריפריה 1 עד 4 עד 50% מהדירות, ובשאר היישובים עד 35%. בהגרלה ה־11 הוקצו בפועל כ־50% מהדירות למשרתי מילואים פעילים, וכמחצית מהן ללוחמים."),
    ("אפשר לבטל זכייה בדירה בהנחה?", "כן. לפי כל זכות אפשר לבטל את הזכייה עד חתימת החוזה, ולפי המדריך של משרד הבינוי והשיכון מקדמה ששולמה בבחירת הדירה עלולה לא לחזור. מי שזכה ורוצה להירשם שוב בודק קודם מול חברת ההרשמה את מעמד הזכאות שלו."),
    ("האם מקבלים מענק בדירה בהנחה?", "ביישובים מזכים כן: במחיר למשתכן 40,000 או 60,000 ₪, ובמחיר מטרה ובמחיר מופחת 40,000 ₪. המענק הוא חלק מהמימון ומשתחרר אחרי שמשלמים את ההון העצמי. הוא הלוואה שלא מחזירים אם מחזיקים בדירה עד סוף תקופת ההתחייבות."),
    ("מה הריבית במשכנתא של משרד הבינוי והשיכון לזכאים?", "לחסרי דירה שאין ולא הייתה להם דירה 10 שנים: ריבית נמוכה ב־0.5% מהריבית הממוצעת על משכנתאות צמודות שבנק ישראל מפרסם, ולא יותר מ־3.0%, לתקופה של 10 עד 30 שנה. פונים לאחד הבנקים למשכנתאות."),
    ("האם משלמים מס רכישה על דירה בהנחה?", "משלמים לפי המדרגות הרגילות. על דירה יחידה אין מס עד %s, ולכן רוב הזוכים לא משלמים מס רכישה. את המס המדויק לכל מחיר מחשבים במחשבון מס הרכישה." % ils(PT["tracks"]["single"][0][0])),
    ("כמה באמת זולה דירה בהנחה ממחיר השוק?", "זה תלוי בעיר. בערי ההגרלה ה־11 שבהן יש בקובץ מחיר מ־2024 או 2025, דירת 100 מ״ר במחיר ההגרלה, עם מע״מ, הייתה זולה מחציון העסקאות של דירות 4 חדרים ב־%s בקריית גת ועד %s בבית שמש (החישוב שלנו). במחשבון בעמוד בודקים כל פרויקט לפי המחיר למ״ר שלו." % (pct(REC[0]["_gap"]), pct(REC[-1]["_gap"]))),
    ("מה זה דירות ללא הגרלה?", "בפרויקטים שבהם נשארו דירות אחרי ההגרלות, זכאים חסרי דירה ומשפרי דיור יכולים לקנות ישירות מהקבלן, לפי סדר הפנייה ועם אישור זכאות בתוקף. בחלק מהפרויקטים נרשמים בדואר אלקטרוני בתוך 48 שעות מפתיחת המכירה. הרשימה בעמוד של משרד הבינוי והשיכון."),
    ("מה זה הגרלת המשך?", "הגרלה נוספת בפרויקט שכבר הייתה בו הגרלה ראשונה. משפרי דיור יכולים להירשם רק להגרלות המשך שהוגדרו להם, ולא להגרלות הראשונות, שמיועדות לחסרי דירה."),
    ("כמה דירות הוגרלו מאז 2022?", "בתשעת הסבבים שבקובץ הרשמי, ממרץ 2022 עד דצמבר 2024, הוגרלו %s דירות ב־%s הגרלות. בסבב 10 (2025) הוגרלו 7,479 דירות ובסבב 11 (2026) %s דירות, לפי הודעות משרד הבינוי והשיכון." % (num(sum(x["units"] for x in L22)), num(len(L22)), num(R11["units"]))),
]
FAQ_NEW = "".join("<h3>%s</h3>\n<p>%s</p>\n" % qa for qa in QA_NEW)
METHOD = ('<h2>שיטה ומקורות</h2>\n'
          '<p class="nlg1-src">הנתונים על ההגרלות מגיעים משני מקורות רשמיים: <a href="%s" target="_blank" rel="noopener">הקובץ של תוכנית דירה בהנחה ב־data.gov.il</a> (%s הגרלות מ־%s עד %s, עודכן %s), '
          'וההודעות של משרד הבינוי והשיכון על ההגרלה ה־11 (<a href="%s" target="_blank" rel="noopener">25.5.2026</a>, <a href="%s" target="_blank" rel="noopener">23.6.2026</a>, <a href="%s" target="_blank" rel="noopener">2.8.2026</a>). '
          'הכללים לפי <a href="%s" target="_blank" rel="noopener">עמוד הזכאות</a>, <a href="%s" target="_blank" rel="noopener">עמוד המימון</a> ו<a href="%s" target="_blank" rel="noopener">המדריך להשתתפות</a> של משרד הבינוי והשיכון. '
          'חציון העסקאות לפי <a href="https://www.nadlan.gov.il/" target="_blank" rel="noopener">אתר הנדל״ן הממשלתי</a> (גרסה %s), והריבית הממוצעת לפי <a href="https://www.boi.org.il/" target="_blank" rel="noopener">בנק ישראל</a>. '
          'סיכוי בהגרלה הוא זוכים חלקי נרשמים; דירות לכל 100 נרשמים הוא דירות בעיר חלקי משקי הבית שנרשמו בה. כל מספר שחושב מסומן "החישוב שלנו". '
          'ההרשמה, הזכאות והתוצאות נקבעות רק באתר ההגרלות של משרד הבינוי והשיכון. עודכן %s.</p>\n'
          % (D["file"]["url"], num(D["file"]["n"]), dmy(D["file"]["first"]), dmy(D["file"]["last"]), dmy(D["file"]["modified"]), D["sp"]["open"]["url"], D["sp"]["regs"]["url"], D["sp"]["wins"]["url"],
             RL["srcs"]["zk"]["url"], RL["srcs"]["fn"]["url"], RL["srcs"]["gd"]["url"], D["inv"]["version"], UPDATED))

# ------------------------------------------------------------------ anchored edits (each old string must appear exactly once in the live content)
FIRST = '<p><strong>הסיכוי לזכות בדירה בהנחה:</strong>'
LASTQ = '<p>חמש שנים מקבלת טופס 4, או שבע שנים מיום ההגרלה, המוקדם מביניהם. מכירה מוקדמת עלולה לחייב החזר של ההטבה.</p>'
R = [
    (FIRST, TOP + FIRST),
    ('<h2>איך מחושב הסיכוי בכלי</h2>', NAMES + '<h2>איך מחושב הסיכוי בכלי</h2>'),
    ('<h2>בני מקום ומשרתי מילואים</h2>', R11SEC + '<h2>בני מקום ומשרתי מילואים</h2>'),
    ('<h2>איך בוחרים שלוש ערים</h2>', PRIOR + '<h2>איך בוחרים שלוש ערים</h2>'),
    ('<h2>מי זכאי לדירה בהנחה</h2>', THREE + '<h2>מי זכאי לדירה בהנחה</h2>'),
    ('<h2>ההגרלה האחרונה וההגרלה הבאה</h2>', ELIG + '<h2>ההגרלה האחרונה וההגרלה הבאה</h2>'),
    ('<h2>מה קורה אחרי הזכייה</h2>', NEXT + '<h2>מה קורה אחרי הזכייה</h2>'),
    ('<h2>שאלות נפוצות</h2>', MONEY + '<h2>שאלות נפוצות</h2>'),
    (LASTQ, LASTQ + "\n" + FAQ_NEW + METHOD),
    # the only edits inside existing text: a passed date in the future tense, and a sentence the new check makes untrue
    ('הנפקת אישורי הזכאות נעצרה זמנית, ולפי הודעת משרד השיכון היא אמורה להיפתח מחדש ב־5.10.2026.',
     'הנפקת אישורי הזכאות נעצרה זמנית, והודעת משרד השיכון קבעה את 5.10.2026 כמועד הפתיחה מחדש.'),
    ('הקובץ הפתוח עדיין לא כולל את מסלול המילואים, ולכן הכלי לא מחשב אותו.',
     'הקובץ הפתוח עדיין לא כולל את מסלול המילואים, ולכן כלי הסיכוי לפי עיר לא מחשב אותו. את הסיכוי של משרתי המילואים בהגרלה ה־11, %s, מראה הבדיקה האישית בראש העמוד, לפי הודעת משרד השיכון מ־2.8.2026.' % pct(G_RES)),
]
NEWS = [n for o, n in R[:9]]


def visible(html):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S); h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    h = re.sub(r"\[nadlan_tool[^\]]*\]", " ", h)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)) + " " + " ".join(re.findall(r'aria-label="([^"]*)"', html))


# ------------------------------------------------------------------ the content: a local file (--from) or the live page over REST
req = None
if FROM:
    raw = io.open(os.path.join(H, FROM) if not os.path.isabs(FROM) else FROM, encoding="utf-8").read().strip() + "\n"; link = SITE + "/dira-behanacha/"; modified = "(local file %s)" % FROM
else:
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "g1page"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
    req = ns["req"]
    s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,modified,title,slug" % PID)
    assert r["slug"] == "dira-behanacha", r.get("slug")
    raw, link, modified = r["content"]["raw"], r["link"], r.get("modified")
new = raw
for o, n in R:
    c = new.count(o)
    assert c == 1, ("anchor must match once", c, o[:80])
    new = new.replace(o, n)
print("[page %d] content %s, %d chars; %d anchors matched once each" % (PID, modified, len(raw), len(R)))

# ------------------------------------------------------------------ gates
NEWTXT = "".join(NEWS) + "".join(n for o, n in R[9:])
nv = visible(NEWTXT); pv = visible(new)
BANNED_NEW = r"ממשק(?!י (?:ה)?בית)|מערכת|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה|טעון אימות|נדל[״\"]?ן חכם|מודל|מנגנון|שכבה|שכבות|הדגמה|טכנולוגי|יחסית|אמור|אטלס|Atlas|פיילוט|פרוטוטייפ|רספונסיבי|מובייל|אפס "
BANNED_PAGE = r"ממשק(?!י (?:ה)?בית)|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה|טעון אימות|נדל[״\"]?ן חכם"
assert not re.search(r"[–—]", pv), "long dash on the page: " + str(re.findall(r".{20}[–—].{20}", pv)[:3])
hits = re.findall(r".{0,25}(?:%s).{0,25}" % BANNED_NEW, nv)
assert not hits, ("language law, new copy", hits[:5])
hits = re.findall(r".{0,25}(?:%s).{0,25}" % BANNED_PAGE, pv)
assert not hits, ("language law, whole page", hits[:5])
assert not re.search(r"(?<![\d.,])0 (₪|חדרים|חודשים|ערים|דירות)", nv), "a zero number on visible text"
assert "<h1" not in NEWTXT and new.count("<h1") == 0, "the theme prints the only h1 from the title"
for sv in re.findall(r"<svg\b.*?</svg>", NEWTXT, flags=re.S):
    assert min(float(x) for x in re.findall(r"font-size:([\d.]+)px", sv)) >= 12 and 'viewBox="0 0 420 ' in sv and 'direction="rtl"' in sv
# computed percentages in new prose carry the label (official figures listed)
OFFICIAL = {pct(G_ALL), pct(G_RES), "75%", "20%", "50%", "35%", "25%", "15%", "73%", "18%", "60%", "0.5%", "3.0%", "80%", "100%"}
for p in re.findall(r"<p\b[^>]*>.*?</p>", "".join(NEWS), flags=re.S):
    ours = [v for v in re.findall(r"\d+(?:\.\d+)?%", visible(p)) if v not in OFFICIAL]
    if ours and "nlg1-note" not in p and "nlg1-src" not in p: assert "החישוב שלנו" in p, ("computed number without the label", ours, visible(p)[:120])
# FAQ: the section the FAQPage schema reads (inc/instruments.php nadlan_nli_faq): h3 + p, 30 questions, none repeated
fs = re.search(r"<h2[^>]*>\s*שאלות נפוצות[^<]{0,60}</h2>(.*?)(?=<h2|$)", re.sub(r"<!--.*?-->", "", new, flags=re.S), flags=re.S).group(1)
QS = [re.sub(r"<[^>]+>", "", q).strip() for q, a in re.findall(r"<h3[^>]*>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*)+)", fs, flags=re.S)]
assert len(QS) == 30 and len(set(QS)) == 30, (len(QS), len(set(QS)))
assert new.count('[nadlan_tool id="dira"]') == 1 and new.count('[nadlan_tool id="dirafit"]') == 1 and new.count('[nadlan_tool id="diracost"]') == 1
# the rendered order: answer paragraph, CTA row, the first tool, then the facts (content-first law)
assert new.find("nlg1-lead") < new.find("nlg1-cta") < new.find('[nadlan_tool id="dirafit"]') < new.find("המספרים של היום") < new.find(FIRST)


class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None


OP = urllib.request.build_opener(NoRedir); UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"}


def status(u):
    try:
        p = urllib.parse.urlsplit(u); u = urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(urllib.parse.unquote(p.path)), p.query, p.fragment))
        return OP.open(urllib.request.Request(u, headers=UA), timeout=60).status
    except urllib.error.HTTPError as e: return e.code
    except Exception as e: return type(e).__name__


hrefs = sorted(set(re.findall(r'href="([^"#][^"]*)"', NEWTXT)))
inner = [h for h in hrefs if h.startswith("/") or h.startswith(SITE)]
if not NOLINKS:  # public GETs of our own pages only
    bad = []
    for h in inner:
        st = status(h if h.startswith("http") else SITE + h)
        if st != 200: bad.append((h, st))
        time.sleep(0.2)
    assert not bad, ("internal links must answer 200", bad)
words_new = len(re.findall(r"[\w֐-׿\"'״]+", visible(re.sub(r"<svg\b.*?</svg>", " ", "".join(NEWS), flags=re.S))))
words_all = len(re.findall(r"[\w֐-׿\"'״]+", visible(re.sub(r"<svg\b.*?</svg>", " ", new, flags=re.S))))
cells = len(re.findall(r"<t[dh][ >]", re.sub(r"<svg\b.*?</svg>", "", new, flags=re.S)))
print("  words in content: %d (%d new) | tables %d | cells %d | svg %d | h2 %d, h3 %d | FAQ %d (8 old + %d new) | tools 3"
      % (words_all, words_new, new.count("<table"), cells, new.count("<svg"), new.count("<h2"), new.count("<h3"), len(QS), len(QA_NEW)))
print("  internal links: %d %s | official links: %d" % (len(inner), "skipped (--no-links)" if NOLINKS else "all 200", len([h for h in hrefs if "gov.il" in h or "boi.org.il" in h])))
print("  gates: no long dash, no banned word, no zero numbers, svg text >= 12px, computed numbers labelled, 30 FAQ, rendered order")

# the internal source list (research stays in the repo, not on the page)
SRCS = """# /dira-behanacha/ (page 8541): where every fact on the page comes from (internal, written by write_g1_page.py, %s)

| Fact on the page | Source |
|---|---|
| Round 11: 7,922 flats, 19 towns, 82 lotteries, order of the lotteries; opened 25.5.2026, closes 22.6.2026, certificates to 7.6.2026, three towns | %s (read in Chrome 26.10.2026) |
| Households per town (313,415 town registrations), 114,848 households, 1.7 million registrations | %s |
| Reserve: 25,394 registered, 4,734 won, about 60%% of winners, about half of the reserve flats to combat soldiers | %s |
| Round 11 announced 12.4.2026 (first planned opening 15.4.2026) | %s |
| Every lottery 2016 to 27.1.2025: registrations, winners, flats, local quota and results, price per m2, round | data.gov.il resource 7c8255d0 (modified %s) via dira-round.json; 2,340 of 2,352 rows labelled "מחיר למשתכן" |
| Round 10: 7,479 flats, 21 towns, opened 10.8.2025, notices 23.11.2025 | ministry notice 6.8.2025 as published by rashuiot.co.il; mako 23.11.2025 (secondary: the file does not have the round) |
| Eligibility, improvers, not eligible, IDF condition, locals, reserve definitions, quotas (wheelchair 1/30, reserve 50/25 and 35/15, locals 20%%, 73%% cap) | %s |
| Certificate 200 ₪, 10 working days, companies, improvers only continuation lotteries | %s; phone codes and one-year validity, 50 ₪ renewal: ministry notice 25.5.2026 |
| Registration steps, results by SMS, mail, voice and anonymous file | %s |
| 75%% financing, appraisal route (100,000 ₪, 2.1M cap), grants 40,000 / 60,000, the state loan rule (0.5%% below, max 3.0%%, 10 to 30 years) | %s |
| 45 minutes to choose, 30 working days to sign, sale lock 5 years from Form 4 or 7 from the lottery | %s (chapter 7, read in Chrome 22.10.2026) |
| Flats without a lottery | https://www.gov.il/he/pages/mechirat_dirot_lelo_hagralah (updated 30.5.2024) |
| How the price is set per track (lowest bid per m2; discount from the appraised market price) | Wikipedia "מחיר למשתכן" and "מחיר מטרה" (secondary); the RAMI decision text (4.7) was not opened. The discount percentage is not printed on the page for that reason |
| Price per m2 is before VAT | the lottery site's project pages as shown by two independent trackers (wizbid.co.il, mishtaken-hacham.co.il); the official document was not opened. The tool lets the reader switch it |
| Deal medians by rooms and quarter | data.nadlan.gov.il version %s via invest.json |
| Average fixed unlinked mortgage rate %s%% | Bank of Israel SDMX via boi-mortgage.json (%s) |
| Single-home purchase tax exemption to %s | Tax Authority via ptax.json |
| Every computed number (flats per 100, groups, odds per round, the gap against deal prices, equity, payment) | this script, from dira-round.json, cross-checked against tools/instruments/test_dirafit.js |
""" % (UPDATED, D["sp"]["open"]["url"], D["sp"]["regs"]["url"], D["sp"]["wins"]["url"], D["sp"]["apr"]["url"], D["file"]["modified"], RL["srcs"]["zk"]["url"], RL["srcs"]["el"]["url"],
       RL["srcs"]["rg"]["url"], RL["srcs"]["fn"]["url"], RL["srcs"]["gd"]["url"], D["inv"]["version"], RATE, RATE_M, ils(PT["tracks"]["single"][0][0]))
io.open(os.path.join(H, "page-sources.md"), "w", encoding="utf-8").write(SRCS)
SVGD = os.path.join(H, "svg"); os.makedirs(SVGD, exist_ok=True)
for name, sv in (("v1-round11-towns", svg_towns()), ("v2-rounds", svg_rounds()), ("v3-groups", svg_groups()), ("v4-path", svg_path())):
    io.open(os.path.join(SVGD, name + ".svg"), "w", encoding="utf-8").write(sv.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1))

if DRY:
    pv_dir = os.path.join(H, "preview"); os.makedirs(pv_dir, exist_ok=True)
    io.open(os.path.join(pv_dir, "g1-page-content.html"), "w", encoding="utf-8", newline="").write(new)
    A = "../../../../../plugins/nadlan-config/assets/instruments/"
    def mount(tid, data, kicker, name):
        dd = ",".join("%sdata/%s?ver=local" % (A, f) for f in data)
        return ('<section class="nli" dir="rtl" lang="he" aria-label="%s"><div class="nli-host" data-nli="%s" data-nli-data="%s"><div class="nli__panel"><p class="nli__kicker">%s</p><h2 class="nli__title">%s</h2></div></div></section>' % (name, tid, dd, kicker, name))
    body = (new.replace('[nadlan_tool id="dira"]', mount("dira", ["dira.json"], "מחשבון · דירה בהנחה", "דירה בהנחה: מה הסיכוי לזכות בהגרלה"))
               .replace('[nadlan_tool id="dirafit"]', mount("dirafit", ["dira-round.json"], "בדיקה אישית · דירה בהנחה", "מי זכאי, באיזה מסלול, ואיפה הכי כדאי להירשם"))
               .replace('[nadlan_tool id="diracost"]', mount("diracost", ["dira-round.json", "boi-mortgage.json", "ptax.json"], "מחשבון · דירה בהנחה", "כמה תעלה הדירה מההגרלה")))
    shell = ('<!doctype html>\n<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,">'
             '<title>/dira-behanacha/ · תצוגה מקומית</title>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;800;900&family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
             '<link rel="stylesheet" href="%score.css?ver=local"><style>html,body{margin:0;background:#fff;color:#12202A;font-family:Heebo,"IBM Plex Sans Hebrew",sans-serif}'
             '.entry-content{padding:0 16px}.entry-content>*{max-width:760px;margin-left:auto;margin-right:auto}p,li{font-size:17px;line-height:1.75}h1{font:800 30px/1.25 Heebo,sans-serif;margin:24px auto 12px}'
             'h2{font:800 26px/1.3 Heebo,sans-serif;margin:36px auto 12px}h3{font:700 20px/1.4 Heebo,sans-serif;margin:24px auto 8px}a{color:#1F4B5C}</style></head>'
             '<body><main><div class="entry-content"><header><h1>%s</h1></header>%s</div></main><script src="%score.js?ver=local" defer></script><script src="%stools/dira.js?ver=local" defer></script><script src="%stools/dirafit.js?ver=local" defer></script></body></html>'
             % (A, TITLE, body, A, A, A))
    io.open(os.path.join(pv_dir, "g1-page-render.html"), "w", encoding="utf-8", newline="").write(shell)
    print("  --dry: wrote preview/g1-page-content.html, preview/g1-page-render.html, page-sources.md, svg/*.svg; nothing was posted")
    sys.exit(0)

# ------------------------------------------------------------------ live write (NOT run by the research session)
assert req is not None
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
stamp = time.strftime("%Y%m%d-%H%M%S")
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, stamp)), "w", encoding="utf-8", newline="").write(raw)
s0, m0, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=title,meta" % PID)
io.open(os.path.join(bk, "page-%d-%s-meta.json" % (PID, stamp)), "w", encoding="utf-8").write(json.dumps(m0, ensure_ascii=False))
assert m0["title"]["raw"] == OLD_TITLE, ("the title changed since the spec", m0["title"]["raw"])
req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new, "title": TITLE, "meta": {"_yoast_wpseo_title": SEO_T, "_yoast_wpseo_metadesc": SEO_D}})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,title,meta" % PID)[1]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(link + "?x=%d" % time.time(), headers=UA), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
ok = {"read-back content": back["content"]["raw"].strip() == new.strip(), "read-back title": back["title"]["raw"] == TITLE, "yoast title": (back.get("meta") or {}).get("_yoast_wpseo_title") == SEO_T,
      "one h1": bd.count("<h1") == 1, "h1 text": TITLE in bd, "seo title in <title>": SEO_T in page, "3 tools mounted": all(('data-nli="%s"' % t) in bd for t in ("dira", "dirafit", "diracost")),
      "shortcode rendered": "[nadlan_tool" not in bd, "svg x4": bd.count("nlg1-fig") == 4, "one FAQPage": page.count('"@type":"FAQPage"') == 1, "30 questions": page.count('"@type":"Question"') == 30,
      "dirafit.js enqueued": "tools/dirafit.js" in page, "updated %s" % UPDATED: ("עודכן %s" % UPDATED) in bd,
      "answer before the first tool": 0 <= bd.find("nlg1-lead") < bd.find('data-nli="dirafit"')}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
print("PAGE", link, "ALL OK" if all(ok.values()) else "CHECK FAILED: restore from page-backup/page-%d-%s.html and its meta" % (PID, stamp))
