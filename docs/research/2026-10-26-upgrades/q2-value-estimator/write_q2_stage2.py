# -*- coding: utf-8 -*-
"""Q2 stage 2 on /property-value-estimator/ (page 129), after stage 1 (fix_q2_stage1.py: title, H1, answer, seller section, FAQ 22).
From dna.md section 7 (7.5 order, 7.6 tables, 7.7 infographics, 7.9 FAQ), every number from section 5 re-read today by
fetch_q2_data.py (data/q2-official.json): the Tax Authority settlement files (V1, V2), CBS 40010 and 60000 to 60500 (V7 to V9), the
Ministry of Justice register (V11), or computed here and labelled "החישוב שלנו".
Adds (additive law: nothing removed or reworded except two banned-word fixes in old text, an em dash and "בבדיקה"):
  * hero CTA "בדקו את שווי הדירה עכשיו" + id on the tool section (the [nadlan_tool id="pval"] shortcode is not touched)
  * H2 שלוש בדיקות לשווי אחד: the method, T3 (the V10 worked example) and I3 (the three checks on one scale, asking price pin)
  * H2 מחירי דירות לפי עיר ומספר חדרים: T1, 23 cities + Yavne + Israel (two quarters), with a 22-quarter sparkline per row.
    The tool keeps its own city table (it is printed by the shortcode, plugin side); T1 holds every row and column of it and its
    caption text, so the page stays complete if the tool's table changes.
  * H2 כמה השתנו מחירי הדירות: מדד הלמ"ס לפי מחוז: T2 and I2
  * H2 איך מחשבים שווי של דירה לפי כתובת: steps + T4, before the appraiser section
  * in the appraiser section: H3 משכנתא, ירושה, גירושין, איך בודקים שהשמאי מורשה (register count re-read today) + T5
  * FAQ: the 7.9 questions still missing (3), so 22 -> 25 visible and in schema
  * H2 איך חישבנו ומאיפה הנתונים, after the summary
Exact anchored replacements (each must match once), language and number asserts, internal links must answer 200.
  python docs/research/2026-10-26-upgrades/q2-value-estimator/write_q2_stage2.py --dry   (GET only; writes preview/q2-stage2-content.html)
  python docs/research/2026-10-26-upgrades/q2-value-estimator/write_q2_stage2.py         (backup, POST, read-back, live check)"""
import io, json, os, re, sys, time, urllib.error, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
import infographics as ig
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
DRY = "--dry" in sys.argv
PID = 129
D = json.load(io.open(os.path.join(H, "data", "q2-official.json"), encoding="utf-8"))

# ------------------------------------------------------------------------------------------------ numbers (every one registered)
REG = set()


def reg(s):
    REG.add(s); return s


def n0(v):
    return reg("{:,}".format(int(round(v))))


def r100(v):
    return int(round(v / 100.0)) * 100


def ils(v):
    return n0(v) + " ₪"  # no-break space: the shekel sign never starts a line alone


def pc(x, sign=True):
    """A percent with one decimal; a signed one sits in an ltr span so the sign stays in front of the number in rtl text."""
    s = "%.1f" % abs(x); reg(s)
    if not sign:
        return s + "%"
    return '<span dir="ltr">%s%s%%</span>' % ("+" if x >= 0 else "-", s)


def ix(v):
    return reg("%.1f" % v)


MON = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]


def mon(y, m):
    return "%s %d" % (MON[m - 1], y)


def ql(y, m):
    return "%d-%d.%d" % (m - 2, m, y)


# ------------------------------------------------------------------------------------------------ data
S = {s["code"]: s for s in D["settlements"]}
VER = {s["version"] for s in D["settlements"]}; assert VER == {"20-08-2026"}, VER
FILE_DATE = "20.8.2026"
READ = "26.10.2026"; assert D["read_utc"].startswith("2026-10-26"), D["read_utc"]
ISR = {k: [(y, m, cp) for y, m, sp, cp in S[5000]["rooms"][k]] for k in ("3", "4", "5")}
for s in D["settlements"]:  # the Israel line is the same in every file
    assert [(y, m, cp) for y, m, sp, cp in s["rooms"]["4"]] == ISR["4"], s["name"]
QS = [(y, m) for y, m, _ in ISR["4"]]; assert len(QS) == 22 and QS[0] == (2021, 3) and QS[-1] == (2026, 6), QS
CBS = {sid: {(r[0], r[1]): r[2] for r in v["rows"]} for sid, v in D["cbs"].items()}
for sid, v in D["cbs"].items():
    assert len({r[3] for r in v["rows"]}) == 1, ("one base per series", sid)
LAST = max(CBS["40010"]); assert LAST == (2026, 7), LAST
REGN = D["register"]["total"]; REG_UPD = D["register"]["last_modified"][:10]
REG_UPD_HE = "%d.%d.%s" % (int(REG_UPD[8:10]), int(REG_UPD[5:7]), REG_UPD[:4])
n0(REGN)


def cbs_change(sid, years):
    I = CBS[sid]; y, m = LAST
    return (I[LAST] / I[(y - years, m)] - 1) * 100


def cbs_peak(sid):
    I = CBS[sid]; k = max(I, key=lambda q: I[q])
    return k, I[k], (I[LAST] / I[k] - 1) * 100


# V7 and V8 as published in dna.md: if CBS revised them, stop and re-read the spec before writing
V8 = {"60000": (-0.2, 29.3), "60100": (-0.8, 42.3), "60200": (-1.4, 41.2), "60300": (-2.7, 24.0), "60400": (-1.9, 18.9), "60500": (-1.5, 26.1)}
assert round(cbs_change("40010", 1), 1) == -1.8 and round(cbs_change("40010", 5), 1) == 26.8 and round(cbs_change("40010", 3), 1) == 5.5, "V7"
assert cbs_peak("40010")[0] == (2025, 1) and round(cbs_peak("40010")[2], 1) == -3.2, "V7 peak"
for sid, (a, b) in V8.items():
    assert (round(cbs_change(sid, 1), 1), round(cbs_change(sid, 5), 1)) == (a, b), ("V8", sid)
DIST = [("60000", "ירושלים"), ("60100", "צפון"), ("60200", "חיפה"), ("60300", "מרכז"), ("60400", "תל אביב"), ("60500", "דרום")]
MAHOZ = {"צפון": "מחוז הצפון", "מרכז": "מחוז המרכז", "דרום": "מחוז הדרום"}  # the CBS names; the chart keeps the short ones
mz = lambda nm: MAHOZ.get(nm, "מחוז " + nm)


def med(code, rooms, q):
    for y, m, sp, cp in S[code]["rooms"][rooms]:
        if (y, m) == q:
            return sp
    return None


# V10, recomputed
Y4_21, Y4_26 = med(2660, "4", (2021, 3)), med(2660, "4", (2026, 3))
B_C = r100(Y4_21 * CBS["60300"][LAST] / CBS["60300"][(2021, 3)])
B_N = r100(Y4_21 * CBS["40010"][LAST] / CBS["40010"][(2021, 3)])
C_M = r100(Y4_21 * Y4_26 / Y4_21)
assert (Y4_21, Y4_26, B_C, B_N) == (1780200, 2473700, 2305900, 2341800), (Y4_21, Y4_26, B_C, B_N)
ASK = 2600000  # an example asking price for the I3 pin, labelled on the page as an example, not data
n0(ASK)

# ------------------------------------------------------------------------------------------------ HTML pieces (one line each)


def table(title, src, head, rows, num=(), wide=False, spark=None):
    h = "".join('<th scope="col">%s</th>' % c for c in head)
    body = []
    for r in rows:
        cells = "".join('<td%s>%s</td>' % (' class="n"' if (j + 1) in num else (' class="s"' if spark == j + 1 else ""), c) for j, c in enumerate(r[1:]))
        body.append('<tr><th scope="row">%s</th>%s</tr>' % (r[0], cells))
    return ('<figure class="nlq2-t"><figcaption>%s<small>%s</small></figcaption><div class="nlq2-x"><table%s><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div></figure>\n'
            % (title, src, ' class="w"' if wide else "", h, "".join(body)))


def fig(svg, cap):
    return '<figure class="nlq2-f">%s<figcaption>%s</figcaption></figure>\n' % (svg, cap)


def sec(sid, h2, body):
    return '<section class="nlq2" id="%s">\n<h2>%s</h2>\n%s</section>\n' % (sid, h2, body)


def p(s):
    return "<p>%s</p>\n" % s


def ltr(s):
    return '<span dir="ltr">%s</span>' % s


def fx(s):
    """A formula in a table cell: left to right, as formulas are written in Hebrew text, in the figure face, on one line."""
    return '<span class="f" dir="ltr">%s</span>' % s


def tidy(html):
    """In text nodes outside the SVGs: a quarter (with its ב-/מ-/ל-/ו- prefix) never breaks at its hyphen, and a Latin web address
    keeps its own direction inside Hebrew text."""
    out = []
    for part in re.split(r"(<svg\b.*?</svg>)", html, flags=re.S):
        if part.startswith("<svg"):
            out.append(part); continue
        bits = re.split(r"(<[^>]+>)", part)
        for i in range(0, len(bits), 2):
            b = re.sub(r"(?:[בלמו]-)?(?:1-3|4-6|7-9|10-12)\.20\d\d", lambda m: '<span class="q">%s</span>' % m.group(0), bits[i])
            bits[i] = re.sub(r"\b[a-z]+(?:\.[a-z]+)+\b", lambda m: "<bdi>%s</bdi>" % m.group(0), b)
        out.append("".join(bits))
    return "".join(out)


EXT = {"nadlan": "https://www.nadlan.gov.il/", "files": "https://data.nadlan.gov.il/api/pages/settlement/buy/2660.json",
       "taxinfo": "https://www.gov.il/he/service/real_estate_information", "cbs": "https://www.cbs.gov.il/he/subjects/Pages/%D7%9E%D7%93%D7%93-%D7%9E%D7%97%D7%99%D7%A8%D7%99-%D7%93%D7%99%D7%A8%D7%95%D7%AA.aspx",
       "register": "https://data.gov.il/he/datasets/ministry_of_justice/shamaim", "govmap": "https://www.govmap.gov.il/sites/property_value.html"}


def ext(k, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (EXT[k], text)


CSS = ("<style id=\"nlq2-css\">"
       "#value-tool,.nadlan-guide .nlq2,.nadlan-guide #appraiser{scroll-margin-top:84px}"
       ".nadlan-guide .nlq2 h3{font-size:21px}"
       ".nadlan-guide .nlq2 .nlq2-steps li{margin-bottom:4px}"
       # tables: the theme stacks every article table into cards on phones and paints th beige, all !important; these are data
       # tables with column headings, so they stay tables (wide ones scroll sideways inside the figure, the city column stays put)
       ".nadlan-guide .nlq2 .nlq2-t{margin:18px 0 26px;border:0;border-radius:0;box-shadow:none;background:transparent;overflow:visible}"
       ".nadlan-guide .nlq2 .nlq2-x{overflow-x:auto;-webkit-overflow-scrolling:touch}"
       ".nadlan-guide .nlq2 .nlq2-t table{display:table!important;width:100%!important;border-collapse:separate;border-spacing:0;background:#fff;border:0;border-top:2px solid #12202A;border-bottom:1px solid #12202A;border-radius:0;margin:0!important;overflow:visible;box-shadow:none}"
       ".nadlan-guide .nlq2 .nlq2-t table.w{min-width:600px}"
       ".nadlan-guide .nlq2 .nlq2-t thead{display:table-header-group!important}"
       ".nadlan-guide .nlq2 .nlq2-t tbody{display:table-row-group!important}"
       ".nadlan-guide .nlq2 .nlq2-t tr{display:table-row!important;border:0!important;border-radius:0!important;margin:0!important;padding:0!important;background:#fff!important;box-shadow:none!important}"
       ".nadlan-guide .nlq2 .nlq2-t figcaption{display:block;text-align:right;padding:0 0 8px;margin:0;font-family:Assistant,'Segoe UI',Arial,sans-serif;font-size:16.5px;font-weight:700;color:#12202A;line-height:1.45}"
       ".nadlan-guide .nlq2 .nlq2-t figcaption small{display:block;font-weight:400;font-size:13.5px;color:#3E4C58;margin-top:3px;line-height:1.55}"
       ".nadlan-guide .nlq2 .nlq2-t th,.nadlan-guide .nlq2 .nlq2-t td{display:table-cell!important;width:auto!important;padding:9px 10px!important;border:0!important;border-bottom:1px solid #D3DCE2!important;font-family:Assistant,'Segoe UI',Arial,sans-serif;font-size:15px!important;line-height:1.5!important;text-align:right!important;vertical-align:top;color:#12202A!important;background:#fff!important;font-weight:400!important;letter-spacing:0!important;text-transform:none!important}"
       ".nadlan-guide .nlq2 .nlq2-t thead th{color:#3E4C58!important;font-weight:600!important;font-size:13px!important;border-bottom:1px solid #12202A!important;vertical-align:bottom}"
       ".nadlan-guide .nlq2 .nlq2-t tbody th{font-weight:600!important;min-width:96px}"
       ".nadlan-guide .nlq2 .nlq2-t th a{color:#1F4FA3!important;text-decoration:underline;text-underline-offset:3px;font-weight:600}"
       ".nadlan-guide .nlq2 .nlq2-t td.n{font-family:'IBM Plex Mono',ui-monospace,monospace!important;font-size:14px!important;white-space:nowrap}"
       ".nadlan-guide .nlq2 .nlq2-t td small{display:block;font-family:Assistant,'Segoe UI',Arial,sans-serif;font-size:12.5px;line-height:1.4;color:#3E4C58;white-space:normal}"
       ".nadlan-guide .nlq2 .nlq2-t td.s{vertical-align:middle;padding:6px 10px!important}"
       ".nadlan-guide .nlq2 .nlq2-t td.s svg{display:block}"
       ".nadlan-guide .nlq2 .nlq2-t tr.isr th,.nadlan-guide .nlq2 .nlq2-t tr.isr td{background:#F3F6FB!important}"
       ".nadlan-guide .nlq2 .nlq2-t table.w th:first-child{position:sticky;right:0;z-index:1;box-shadow:-1px 0 0 #D3DCE2}"
       ".nadlan-guide .nlq2 .q{white-space:nowrap}"
       ".nadlan-guide .nlq2 .nlq2-t td .f{font-family:'IBM Plex Mono',ui-monospace,monospace!important;font-size:13.5px!important;white-space:nowrap;unicode-bidi:isolate}"
       ".nadlan-guide .nlq2 .nlq2-f{margin:20px 0 26px;max-width:560px}"
       ".nadlan-guide .nlq2 .nlq2-f figcaption{font-family:Assistant,'Segoe UI',Arial,sans-serif;font-size:14.5px;line-height:1.65;color:#3E4C58;margin-top:8px}"
       ".nadlan-guide .nlq2 .nlq2-f svg{border-top:2px solid #12202A}"
       ".nadlan-guide .nlq2 .nlq2-meta{font-size:14px;line-height:1.7;color:#3E4C58;border-top:1px solid #D3DCE2;padding-top:12px;margin-top:22px}"
       ".nadlan-guide .nlq2 a{color:#1F4FA3}"
       "@media(max-width:640px){.nadlan-guide .nlq2 .nlq2-t th,.nadlan-guide .nlq2 .nlq2-t td{padding:8px 8px!important;font-size:14px!important}"
       ".nadlan-guide .nlq2 .nlq2-t td.n{font-size:13px!important;padding:8px 6px!important}.nadlan-guide .nlq2 .nlq2-t table.w tbody th{min-width:84px}"
       ".nadlan-guide .nlq2 h3{font-size:19px}"
       # phones: the charts take the full screen width (the article column has a double side margin there)
       ".nadlan-guide .nlq2 .nlq2-f{margin-left:-16px;margin-right:-16px;max-width:none}.nadlan-guide .nlq2 .nlq2-f figcaption{padding:0 16px}}"
       "</style>\n")

# ------------------------------------------------------------------------------------------------ T3 + I3: the three checks (V10)
T3 = table("שלוש הבדיקות, דוגמה: דירת 4 חדרים ביבנה",
           "רשות המסים: הקובץ של יבנה, גרסת %s. הלמ\"ס: מדד מחירי הדירות, מחוז המרכז (60300) והמדד הארצי (40010), %s, ערכים זמניים. התוצאות: החישוב שלנו, מעוגלות ל-100 ₪." % (FILE_DATE, mon(*LAST)),
           ["בדיקה", "נוסחה", "תוצאה", "תאריך הנתון"], [
               ["בדיקה 1: החציון ביבנה היום", "החציון לדירת 4 חדרים ב-%s" % ql(2026, 3), ils(Y4_26), ql(2026, 3)],
               ["בדיקה 2: מדד מחוז המרכז", fx("%s × %s ÷ %s" % (n0(Y4_21), ix(CBS["60300"][LAST]), ix(CBS["60300"][(2021, 3)]))), ils(B_C) + "<small>%s</small>" % pc((B_C / float(Y4_21) - 1) * 100), "%s עד %s" % (mon(2021, 3), mon(*LAST))],
               ["בדיקה 2 לפי המדד הארצי", fx("%s × %s ÷ %s" % (n0(Y4_21), ix(CBS["40010"][LAST]), ix(CBS["40010"][(2021, 3)]))), ils(B_N) + "<small>%s</small>" % pc((B_N / float(Y4_21) - 1) * 100), "%s עד %s" % (mon(2021, 3), mon(*LAST))],
               ["בדיקה 3: החציון ביבנה מאז הקנייה", fx("%s × %s ÷ %s" % (n0(Y4_21), n0(Y4_26), n0(Y4_21))), ils(C_M) + "<small>%s</small>" % pc((C_M / float(Y4_21) - 1) * 100), "%s עד %s" % (ql(2021, 3), ql(2026, 3))]],
           num=(2,), wide=True)
GAP = Y4_26 - B_C
I3 = ig.anchors_svg({"lo": 2200000, "hi": 2700000, "unit": "מיליון ₪",
                     "ticks": [(v, reg("%.1f" % (v / 1e6))) for v in (2200000, 2300000, 2400000, 2500000, 2600000, 2700000)],
                     "marks": [(B_C, "לפי מדד המרכז", ils(B_C), "up"), (B_N, "לפי המדד הארצי", ils(B_N), "down"), (Y4_26, "החציון ביבנה היום", ils(Y4_26), "up")],
                     "pin": (ASK, "מחיר מבוקש לדוגמה", ils(ASK))},
                    "שלוש הבדיקות על סרגל אחד", "דירת 4 חדרים ביבנה, נקנתה ב-%s ב-%s. דוגמה" % (ql(2021, 3), ils(Y4_21)),
                    "הטווח בין הבדיקות: %s (החישוב שלנו)" % ils(GAP),
                    "שלוש הבדיקות לדירת 4 חדרים ביבנה: לפי מדד המרכז %s, לפי המדד הארצי %s, החציון היום %s; מחיר מבוקש לדוגמה %s" % (ils(B_C), ils(B_N), ils(Y4_26), ils(ASK)))
S4 = sec("three-checks", "שלוש בדיקות לשווי אחד",
         p("שווי של דירה בודקים משלושה כיוונים, וכל אחד מהם נשען על נתון רשמי עם תאריך: כמה משלמים היום על דירה דומה, כמה השתנו המחירים במחוז מאז שקניתם, "
           "וכמה השתנה החציון בעיר שלכם באותו זמן. כשהבדיקות קרובות זו לזו, הטווח מבוסס. כשהן רחוקות, הפער עצמו מספר משהו על הדירה, על השכונה או על הרבעון.")
         + '<ul class="nlq2-steps">'
         + "<li><strong>בדיקה 1, החציון של היום:</strong> המחיר החציוני של עסקאות שדווחו לרשות המסים באותה עיר או שכונה ובאותו מספר חדרים, ברבעון האחרון שפורסם. הנוסחה: השווי הוא החציון ברבעון האחרון.</li>"
         + "<li><strong>בדיקה 2, מחיר הקנייה לפי מדד הלמ\"ס:</strong> מחיר הקנייה מעודכן לפי מדד מחירי הדירות של המחוז, ולקנייה לפני 2018 לפי המדד הארצי. הנוסחה: מחיר הקנייה × מדד היום ÷ מדד חודש הקנייה.</li>"
         + "<li><strong>בדיקה 3, מחיר הקנייה לפי החציון של העיר:</strong> מחיר הקנייה מעודכן לפי השינוי בחציון של העיר ומספר החדרים מאז הרבעון שבו קניתם. הנוסחה: מחיר הקנייה × חציון היום ÷ חציון רבעון הקנייה.</li>"
         + "</ul>\n"
         + p("הדוגמה מחושבת מנתונים רשמיים בלבד: דירת 4 חדרים ביבנה שנקנתה ב-%s בדיוק בחציון של העיר באותו רבעון, %s." % (ql(2021, 3), ils(Y4_21)))
         + T3
         + fig(I3, "שלוש הבדיקות של הדוגמה על סרגל אחד, והטווח ביניהן. הסיכה האדומה היא מחיר מבוקש לדוגמה, %s, ולא נתון: הוא גבוה ב-%s (%s) מהבדיקה הגבוהה (החישוב שלנו)."
               % (ils(ASK), ils(ASK - Y4_26), pc((ASK / float(Y4_26) - 1) * 100, sign=False)))
         + p("בדוגמה הזאת בדיקה 1 ובדיקה 3 יוצאות זהות, כי מחיר הקנייה היה בדיוק החציון של אותו רבעון; מחיר קנייה אחר משנה את התוצאה של בדיקה 3. "
             "הטווח בין הבדיקות הוא %s, %s מהבדיקה הנמוכה (החישוב שלנו). החציון ביבנה עלה יותר מהמדד של המחוז, כי חציון של עיר זז גם כשמשתנה תמהיל הדירות שנמכרו ברבעון, "
             "למשל כשנמכרו בו יותר דירות חדשות. לכן את <a href=\"#asking-price\">מחיר השיווק הנכון לדירה</a> בונים מהטווח כולו, ולא מהבדיקה הגבוהה בלבד."
             % (ils(GAP), pc(GAP / float(B_C) * 100, sign=False))))

# ------------------------------------------------------------------------------------------------ T1: city medians + sparklines
ORDER = sorted([c for c in S if c != 5000] + [5000], key=lambda c: S[c]["name"])


def city_row(code):
    s = S[code]; r = s["rooms"]
    p4 = {(y, m): sp for y, m, sp, cp in r["4"]}
    q = max(k for k, v in p4.items() if v)
    cells = []
    for k in ("3", "4", "5"):
        pk = {(y, m): sp for y, m, sp, cp in r[k]}
        if pk.get(q):
            cells.append(n0(pk[q]))
        else:
            qk = max(kk for kk, v in pk.items() if v)
            cells.append(n0(pk[qk]) + "<small>%s</small>" % ql(*qk))
    prev = p4.get((q[0] - 1, q[1]))
    yoy = pc((p4[q] / float(prev) - 1) * 100) if prev else ""
    series = [p4[k] for k in QS]
    first = min(i for i, v in enumerate(series) if v); last = max(i for i, v in enumerate(series) if v)
    lab = "החציון לדירת 4 חדרים ב%s: %s ב-%s, %s ב-%s" % (s["name"], ils(series[first]), ql(*QS[first]), ils(series[last]), ql(*QS[last]))
    name = '<a href="%s">%s</a>' % (s["page"], s["name"]) if s.get("page") else s["name"]
    return [name] + cells + [ql(*q), yoy, ig.sparkline(series, lab)], (p4[q] / float(prev) - 1) * 100 if prev else None


def isr_row(q):
    vals = []
    for k in ("3", "4", "5"):
        vals.append(n0(dict(((y, m), cp) for y, m, cp in ISR[k])[q]))
    p4 = dict(((y, m), cp) for y, m, cp in ISR["4"])
    yoy = (p4[q] / float(p4[(q[0] - 1, q[1])]) - 1) * 100
    series = [p4[k] if k <= q else None for k in QS]
    last = max(i for i, v in enumerate(series) if v)
    lab = "החציון לדירת 4 חדרים בכל הארץ: %s ב-%s, %s ב-%s" % (ils(series[0]), ql(*QS[0]), ils(series[last]), ql(*QS[last]))
    return ["כל הארץ"] + vals + [ql(*q), pc(yoy), ig.sparkline(series, lab)], yoy


ROWS, YOY = [], {}
for q in ((2026, 6), (2026, 3)):
    row, y = isr_row(q); ROWS.append(row); YOY[("isr",) + q] = y
for c in ORDER:
    row, y = city_row(c); ROWS.append(row); YOY[c] = y
assert len(ROWS) == 26 and all(YOY[c] is not None for c in ORDER)
T1 = table("מחיר חציוני לפי עיר וחדרים",
           "המחיר החציוני של דירות שנמכרו לפי מספר החדרים, ברבעון האחרון שפורסם לכל עיר (ברובן %s), לפי נתוני רשות המסים (₪). מספר קטן מתחת למחיר: רבעון אחר, האחרון שיש בו חציון. "
           "המקור: קובצי הסיכום של אתר הנדל\"ן הממשלתי, גרסת %s, נקראו ב-%s. השינוי בשנה, מול אותו רבעון בשנה הקודמת, והקו הקטן של 22 רבעונים מ-%s עד %s (כל קו בקנה מידה משלו, "
           "רווח בקו = רבעון שבו הקובץ לא מפרסם חציון): החישוב שלנו מאותם קבצים." % (ql(2026, 3), FILE_DATE, READ, ql(*QS[0]), ql(*QS[-1])),
           ["עיר", "3 חדרים", "4 חדרים", "5 חדרים", "רבעון", "שינוי בשנה (4 חדרים)", "4 חדרים, %d עד %d" % (QS[0][0], QS[-1][0])], ROWS, num=(1, 2, 3, 4, 5), wide=True, spark=6)
T1 = T1.replace('<tr><th scope="row">כל הארץ</th>', '<tr class="isr"><th scope="row">כל הארץ</th>')
down = sorted([c for c in ORDER if YOY[c] < 0], key=lambda c: YOY[c]); up = sorted([c for c in ORDER if YOY[c] > 0], key=lambda c: -YOY[c])
assert len(down) + len(up) == len(ORDER)
reg(str(len(ORDER))); reg(str(len(down))); reg(str(len(up)))
i4 = dict(((y, m), cp) for y, m, cp in ISR["4"])
YAV = S[2660]; reg(str(YAV["neighbourhoods"]))
S5 = sec("city-prices", "מחירי דירות לפי עיר ומספר חדרים",
         p("המחיר החציוני הוא המחיר שבאמצע: חצי מהדירות באותו מספר חדרים נמכרו ביותר, וחצי בפחות. הטבלה מציגה את %d הערים, כולל יבנה, ואת כל הארץ בשני הרבעונים האחרונים, "
           "לפי הקבצים שרשות המסים מפרסמת לכל עיר. הקו הקטן בכל שורה מראה איך זז החציון לדירת 4 חדרים ב-22 הרבעונים האחרונים, והנקודה בסופו היא הרבעון שבטבלה." % len(ORDER))
         + T1
         + p("בשנה האחרונה החציון לדירת 4 חדרים ירד ב-%d ערים מתוך %d, ועלה ב-%d (החישוב שלנו, לפי הרבעון האחרון של כל עיר). בכל הארץ הוא ירד ב-%s, מ-%s ב-%s ל-%s ב-%s. "
             "העלייה הגדולה ביותר הייתה ב%s, %s, והירידה הגדולה ביותר ב%s, %s."
             % (len(down), len(ORDER), len(up), pc(-YOY[("isr", 2026, 6)], sign=False), ils(i4[(2025, 6)]), ql(2025, 6), ils(i4[(2026, 6)]), ql(2026, 6),
                S[up[0]]["name"], pc(YOY[up[0]]), S[down[0]]["name"], pc(YOY[down[0]])))
         + p("יבנה נוספה לטבלה לפי הקובץ הרשמי שלה, שכולל %d שכונות: דירת 4 חדרים נמכרה שם בחציון של %s ב-%s, %s לעומת %s. את החציון לפי שכונה בודקים במחשבון למעלה."
             % (YAV["neighbourhoods"], ils(Y4_26), ql(2026, 3), pc((Y4_26 / float(med(2660, "4", (2025, 3))) - 1) * 100), ql(2025, 3))))
assert not any(YOY[c] == 0 for c in ORDER)

# ------------------------------------------------------------------------------------------------ T2 + I2: CBS by district
d_rows, i2 = [], []
pk_n = cbs_peak("40010")
for sid, nm in [("40010", "כל הארץ")] + DIST:
    a, b, c = cbs_change(sid, 1), cbs_change(sid, 3), cbs_change(sid, 5)
    k, v, fp = cbs_peak(sid)
    d_rows.append([nm if sid == "40010" else mz(nm), pc(a), pc(b), pc(c), pc(fp) + "<small>השיא: %s</small>" % mon(*k)])
    if sid != "40010":
        i2.append((nm, round(a, 1), round(c, 1)))
T2 = table("מדד מחירי הדירות לפי מחוז, %s" % mon(*LAST),
           "הלמ\"ס: סדרה 40010, המדד הארצי (בסיס: ממוצע 1993 = 100), וסדרות המחוזות 60000 עד 60500, נקראו ב-%s. השינויים: החישוב שלנו מהערכים שפורסמו; השיא: החודש הגבוה מאז %s. "
           "ערכי החודשים האחרונים זמניים." % (READ, mon(2018, 1)),
           ["מחוז", "שינוי ב-12 חודשים", "ב-3 שנים", "ב-5 שנים", "מהשיא"], d_rows, num=(1, 2, 3, 4), wide=False)
T2 = T2.replace('<tr><th scope="row">כל הארץ</th>', '<tr class="isr"><th scope="row">כל הארץ</th>')
i2 = [("כל הארץ", round(cbs_change("40010", 1), 1), round(cbs_change("40010", 5), 1))] + i2
for nm, a, c in i2:
    reg("%.1f" % abs(a)); reg("%.1f" % abs(c))
I2 = ig.districts_svg(i2, "מדד מחירי הדירות לפי מחוז, עד %s" % mon(*LAST), "השינוי ב-12 חודשים וב-5 שנים, לפי הלמ\"ס",
                      "השינוי במדד מחירי הדירות עד %s: " % mon(*LAST) + ", ".join("%s %s%% בשנה ו-%s%% בחמש שנים" % (nm, ("%+.1f" % a), ("%+.1f" % c)) for nm, a, c in i2))
ch = {sid: (cbs_change(sid, 1), cbs_change(sid, 5), cbs_peak(sid)) for sid, _ in DIST}
worst12 = min(DIST, key=lambda x: ch[x[0]][0]); best5 = max(DIST, key=lambda x: ch[x[0]][1]); low5 = min(DIST, key=lambda x: ch[x[0]][1])
far = min(DIST, key=lambda x: ch[x[0]][2][2])
assert all(ch[sid][0] < 0 for sid, _ in DIST), "the text says every district fell in 12 months"
r5 = [ch[sid][1] for sid, _ in DIST]
S6 = sec("cbs-index", "כמה השתנו מחירי הדירות: מדד הלמ\"ס לפי מחוז",
         p("מדד מחירי הדירות של הלשכה המרכזית לסטטיסטיקה מחושב כל חודש מהעסקאות שדווחו. ב%s עמד המדד הארצי על %s נקודות, ירידה של %s מהחודש הקודם ושל %s משנה קודם. "
           "בשלוש שנים המחירים עלו ב-%s ובחמש שנים ב-%s. השיא היה ב%s, %s נקודות, והמדד היום נמוך ממנו ב-%s."
           % (mon(*LAST), ix(CBS["40010"][LAST]), pc(-(CBS["40010"][LAST] / CBS["40010"][(2026, 6)] - 1) * 100, sign=False), pc(-cbs_change("40010", 1), sign=False),
              pc(cbs_change("40010", 3), sign=False), pc(cbs_change("40010", 5), sign=False), mon(*pk_n[0]), ix(pk_n[1]), pc(-pk_n[2], sign=False)))
         + p("בכל ששת המחוזות המדד ירד בשנה האחרונה, והירידה הגדולה ביותר הייתה ב%s, %s. בחמש שנים המחירים עלו הכי הרבה ב%s, %s, והכי מעט ב%s, %s. "
             "הכי רחוק מהשיא שלו נמצא היום %s: %s מתחת ל%s."
             % (mz(worst12[1]), pc(-ch[worst12[0]][0], sign=False), mz(best5[1]), pc(ch[best5[0]][1], sign=False), mz(low5[1]), pc(ch[low5[0]][1], sign=False),
                mz(far[1]), pc(-ch[far[0]][2][2], sign=False), mon(*ch[far[0]][2][0])))
         + T2
         + fig(I2, "השינוי במדד מחירי הדירות לפי מחוז, עד %s: ירידה קטנה בשנה האחרונה בכל המחוזות, מול עלייה של %s עד %s בחמש שנים (החישוב שלנו מהערכים שפרסמה הלמ\"ס)."
               % (mon(*LAST), pc(min(r5), sign=False), pc(max(r5), sign=False)))
         + p("המדד הוא אינדיקטור לשינוי במחירי הדירות ואינו חלק ממדד המחירים לצרכן. הערכים של החודשים האחרונים זמניים, והלמ\"ס מעדכנת אותם כל חודש כשמדווחות עסקאות נוספות. "
             "לשווי משתמשים בו כך, כמו בדיקה 2 למעלה: מכפילים את מחיר הקנייה במדד של המחוז היום ומחלקים במדד של חודש הקנייה. "
             + ext("cbs", "מדד מחירי הדירות באתר הלמ\"ס") + "."))

# ------------------------------------------------------------------------------------------------ T4: by address
T4 = table("איפה בודקים מה", "המקורות הרשמיים לבדיקת שווי, ומה כל אחד מהם לא מראה. govmap נבדק ב-25.10.2026.", ["מקור", "מה הוא נותן", "מה הוא לא נותן"], [
    [ext("nadlan", "אתר הנדל\"ן הממשלתי"), "עסקאות שדווחו לרשות המסים, לפי כתובת, רחוב, שכונה, גוש וחלקה", "מצב פנימי, שיפוץ ונוף; לא שווי לדירה מסוימת"],
    [ext("taxinfo", "מאגר מידע נדל\"ן של רשות המסים"), "השירות של רשות המסים לנתוני עסקאות במקרקעין, באתר gov.il", "פרשנות לעסקה ומצב הנכס"],
    [ext("cbs", "מדד מחירי הדירות של הלמ\"ס"), "השינוי החודשי במחירי הדירות, ארצי ולפי 6 מחוזות", "מחיר לעיר, לשכונה או לדירה; הערכים האחרונים זמניים"],
    [ext("register", "מאגר שמאי המקרקעין של משרד המשפטים"), "%s שמאים מורשים: שם, מספר רישיון ומספר תיק (עדכון %s)" % (n0(REGN), REG_UPD_HE), "מחירים, התמחות וזמינות"],
    [ext("govmap", "מחשבון שווי נכס ב-govmap"), "הערכה לפי שכונה, שטח, סוג נכס, קומה, חדרים ושנת בנייה", "גישה לציבור: נפתח רק אחרי התחברות"],
    ["המחשבון בעמוד הזה", "החציון לפי עיר, שכונה ומספר חדרים עם הרבעון שלו, והתאמות לשטח, לקומה, לחניה, למרפסת ולמצב", "חוות דעת שמאית או מסמך לבנק, לבית משפט או לרשויות"]], wide=False)
S9 = sec("by-address", "איך מחשבים שווי של דירה לפי כתובת",
         p("באתר הנדל\"ן הממשלתי של רשות המסים אפשר לחפש כל כתובת ולראות את העסקאות שדווחו בבניין, ברחוב ובשכונה. כך עושים את זה, צעד אחר צעד:")
         + '<ol class="nlq2-steps">'
         + "<li>נכנסים ל" + ext("nadlan", "אתר הנדל\"ן הממשלתי") + " ומקלידים עיר, רחוב ומספר בית, או גוש וחלקה.</li>"
         + "<li>בוחרים עסקאות מכירה, ומסננים לפי מספר חדרים ולפי תאריכים, למשל השנה האחרונה.</li>"
         + "<li>לכל עסקה מחשבים מחיר למ\"ר: המחיר חלקי השטח שדווח.</li>"
         + "<li>מוציאים עסקאות חריגות: מכירה בין קרובים, חלק מדירה, או דירה ששונה מאוד בשטח, בקומה או במצב.</li>"
         + "<li>לוקחים את המחיר האמצעי למ\"ר של העסקאות הדומות שנשארו, ומכפילים בשטח של הדירה שלכם.</li>"
         + "<li>מתאימים לקומה, לחניה, למרפסת ולמצב במחשבון, ומשווים לחציון של השכונה ולשלוש הבדיקות.</li>"
         + "</ol>\n"
         + p("מה הרשימה לא מראה: מצב פנימי, שיפוץ, נוף, כיווני אוויר ולחץ הזמן של הצדדים. לכן שתי עסקאות באותו בניין יכולות להיות רחוקות זו מזו, והפער לא אומר שאחת מהן טעות. "
             "ב-govmap יש גם מחשבון שווי נכס לפי שכונה, שטח, סוג נכס, קומה, חדרים ושנת בנייה, אבל הוא נפתח רק אחרי התחברות עם שם משתמש וסיסמה.")
         + T4)

# ------------------------------------------------------------------------------------------------ appraiser H3s + T5
T5 = table("מחשבון או שמאי", "מתי מספיקה הערכה ראשונית ומתי צריך מסמך של שמאי מקרקעין. את שכר הטרחה מסכמים מול השמאי בהצעה בכתב.",
           ["מטרה", "מספיקה הערכה ראשונית?", "מי מזמין", "המסמך שנדרש"], [
               ["מכירה", "כן, כנקודת פתיחה למחיר השיווק", "המוכר", "אין חובה; חוות דעת שמאית כשהנכס חריג או כשאין עסקאות דומות"],
               ["קנייה", "כן, לבדיקת המחיר המבוקש לפני הצעה", "הקונה", "אין חובה; שמאות מוקדמת כשהמחיר גבוה מהטווח או כשהמשכנתא גבוהה"],
               ["משכנתא", "לא", "לפי דרישת הבנק", "שומה של שמאי מקרקעין לבנק"],
               ["ירושה", "לתיאום ציפיות בין היורשים", "היורשים", "חוות דעת שמאית כשיש מחלוקת, או כשרשות או בית משפט מבקשים"],
               ["גירושין", "לא כמסמך", "אחד הצדדים, שניהם יחד, או בית המשפט", "חוות דעת של שמאי מקרקעין"],
               ["בית משפט", "לא", "הצד שמגיש, או שבית המשפט ממנה שמאי", "חוות דעת שמאית לפי דרישת בית המשפט"]], wide=True)
APPR = ('<div class="nlq2">\n'
        + "<h3>הערכת שווי דירה למשכנתא</h3>\n"
        + p("לפני אישור משכנתא הבנק מבקש שומה של שמאי מקרקעין. כששומת השמאי לבנק נמוכה מהמחיר בחוזה, המשכנתא שמאושרת עלולה להיות נמוכה מהצפוי, וההפרש נדרש מההון העצמי. "
            "לכן בודקים את הטווח במחשבון ואת שלוש הבדיקות לפני החתימה, ואם המחיר בחוזה גבוה מהן, מזמינים שמאות מוקדמת.")
        + "<h3>הערכת שווי בירושה לפני מכירה</h3>\n"
        + p("כשדירה עוברת בירושה, היורשים צריכים טווח משותף לפני שמחליטים אם למכור, להשכיר, או שאחד מהם יקנה את החלקים של האחרים. "
            "מתחילים מהחציון לפי מספר החדרים ומהעסקאות בבניין וברחוב, כדי שכולם יראו את אותם מספרים. כשיש מחלוקת, או כשנדרש מסמך לרשויות או לבית משפט, מזמינים חוות דעת של שמאי מקרקעין.")
        + "<h3>הערכת שווי בגירושין</h3>\n"
        + p("בחלוקת רכוש בגירושין השווי של הדירה קובע כמה מקבל כל צד, ולכן מחשבון לא מספיק כמסמך. בהליך משפטי מגישים חוות דעת של שמאי מקרקעין, ולעיתים בית המשפט ממנה שמאי מטעמו. "
            "המחשבון עוזר לשני הצדדים להבין את הטווח לפני הפגישה עם עורכי הדין.")
        + "<h3>איך בודקים שהשמאי מורשה</h3>\n"
        + p("משרד המשפטים מפרסם את " + ext("register", "מאגר שמאי המקרקעין") + " באתר data.gov.il. לפי העדכון של %s יש בו %s שמאים מורשים, עם שם, מספר רישיון ומספר תיק. "
            "לפני שמזמינים שומה מבקשים מהשמאי את מספר הרישיון ומחפשים אותו במאגר, לפי המספר או לפי השם. המאגר לא מציג מחירים, ואת שכר הטרחה מסכמים מול השמאי בהצעה בכתב."
            % (REG_UPD_HE, n0(REGN)))
        + "<h3>מתי מספיקה הערכה ראשונית ומתי צריך שמאי</h3>\n"
        + T5
        + "</div>\n")

# ------------------------------------------------------------------------------------------------ FAQ (7.9 questions still missing) + method
QA_NEW = [
    ("איך קובעים מחיר שיווק לדירה?",
     "מתחילים משלוש בדיקות: החציון של עסקאות שנסגרו בשכונה ובמספר החדרים, מחיר הקנייה מעודכן לפי מדד מחירי הדירות של הלמ\"ס, והעסקאות האחרונות בבניין וברחוב. "
     "את המחיר המבוקש ממקמים בתוך הטווח שהן יוצרות לפי קומה, חניה, מרפסת ומצב, וקובעים מראש מחיר תחתון. מחיר גבוה הרבה מעל הטווח מביא פחות פניות."),
    ("מהי הערכת שווי דירה מבוססת AI, ובמה היא שונה מחישוב לפי עסקאות?",
     "הערכה מבוססת AI היא מספר שתוכנה מחשבת מתוך עסקאות, מודעות ונתוני סביבה, בדרך כלל בלי לפרסם אילו עסקאות נבחרו ואיזה משקל קיבל כל נתון. "
     "חישוב לפי עסקאות מתחיל במחיר החציוני שדווח לרשות המסים, עם הרבעון שלו, וכל התאמה כתובה לפניכם. כך אפשר לבדוק כל שלב ולהשוות את התוצאה לעסקאות בבניין."),
    ("כמה מוסיפים חניה, מחסן ומרפסת לשווי?",
     "אין סכום אחד שמתאים לכל עיר. במחשבון מזינים את השווי של חניה ושל מחסן בשקלים ואת שטח המרפסת כפול שווי למ\"ר מרפסת, ובודקים אותם מול עסקאות באותו בניין או ברחוב, עם חניה ובלי חניה. "
     "רישום ההצמדה בנסח קובע אם החניה והמחסן הם חלק מהדירה."),
]
FAQ_HTML = "".join("\n      <h3>%s</h3>\n      <p>%s</p>" % qa for qa in QA_NEW)
S13 = sec("method", "איך חישבנו ומאיפה הנתונים",
          p("כל מספר בעמוד מגיע ממקור רשמי, עם התאריך שלו, ומה שחישבנו בעצמנו מסומן \"החישוב שלנו\".")
          + "<ul>"
          + "<li><strong>חציון לפי עיר ומספר חדרים:</strong> קובצי הסיכום של רשות המסים (data.nadlan.gov.il) שעליהם בנוי " + ext("nadlan", "אתר הנדל\"ן הממשלתי") + ", גרסת %s, 22 רבעונים מ-%s עד %s: "
            "החציון ל-3, 4 ו-5 חדרים לכל עיר, וקו של כל הארץ. נקראו ב-%s.</li>" % (FILE_DATE, ql(*QS[0]), ql(*QS[-1]), READ)
          + "<li><strong>מדד מחירי הדירות:</strong> הלמ\"ס, סדרה 40010 (בסיס: ממוצע 1993 = 100) וסדרות המחוזות 60000 עד 60500, עד %s. נקראו ב-%s.</li>" % (mon(*LAST), READ)
          + "<li><strong>מאגר שמאי המקרקעין:</strong> משרד המשפטים באתר data.gov.il, עדכון %s, %s שמאים.</li>" % (REG_UPD_HE, n0(REGN))
          + "<li><strong>מחשבון שווי נכס ב-govmap:</strong> נבדק ב-25.10.2026; נפתח רק אחרי התחברות.</li>"
          + "</ul>\n"
          + p("הנוסחאות: השינוי בשנה הוא החציון ברבעון האחרון חלקי החציון באותו רבעון שנה קודם, פחות 1. השינוי לפי המדד הוא המדד בחודש האחרון חלקי המדד בחודש שבודקים, פחות 1. "
              "מחיר לפי המדד הוא מחיר הקנייה כפול היחס בין שני המדדים. המרחק מהשיא הוא המדד היום מול החודש הגבוה מאז %s. תוצאות במחיר מעוגלות ל-100 ₪." % mon(2018, 1))
          + p("החציון אינו שווי של דירה מסוימת: הוא המחיר האמצעי של העסקאות שדווחו. ברבעונים שבהם הקובץ לא מפרסם חציון לעיר, הקו הקטן בטבלה נקטע. "
              "ערכי המדד של החודשים האחרונים זמניים ומתעדכנים. כל מה שבעמוד הוא הערכה ראשונית, לא חוות דעת שמאית.")
          + '<p class="nlq2-meta">עודכן ב-%s: קובצי רשות המסים (גרסת %s), מדד הלמ"ס עד %s ומאגר השמאים (עדכון %s).</p>\n' % (READ, FILE_DATE, mon(*LAST), REG_UPD_HE))

S4, S5, S6, S9, APPR, S13 = (tidy(x) for x in (S4, S5, S6, S9, APPR, S13))

# ------------------------------------------------------------------------------------------------ the replacements
HERO_CTA = '<div class="cta"><a class="btn" href="/property-value/">מדריך הערכת שווי</a><a class="btn secondary" href="/real-estate-appraiser/">מתי צריך שמאי</a></div>'
SUM_CTA = ('<div class="cta"><a class="btn" href="/property-value/">מדריך הערכת שווי</a><a class="btn secondary" href="/real-estate-appraiser/">שמאי מקרקעין</a>'
           '<a class="btn secondary" href="/selling-apartment/">מכירת דירה</a></div>\n    </section>\n')
R = [
    ('<div class="nadlan-guide">', CSS + '<div class="nadlan-guide">'),
    (HERO_CTA, HERO_CTA.replace('<div class="cta">', '<div class="cta"><a class="btn" href="#value-tool">בדקו את שווי הדירה עכשיו</a>')),
    ('<section class="wrap" aria-label="מחשבון שווי דירה">', '<section class="wrap" id="value-tool" aria-label="מחשבון שווי דירה">'),
    ("    <section>\n      <h2>איך מתחילים הערכת שווי דירה?</h2>", S4 + S5 + S6 + "    <section>\n      <h2>איך מתחילים הערכת שווי דירה?</h2>"),
    ("    <section>\n      <h2>מתי צריך שמאי מקרקעין?</h2>", S9 + "    <section id=\"appraiser\">\n      <h2>מתי צריך שמאי מקרקעין?</h2>"),
    ("שמאות נמוכה אחרי חתימה יכולה ליצור צורך בהון עצמי נוסף, ולכן עדיף לבדוק סיכון כזה בזמן.</p>\n    </section>",
     "שמאות נמוכה אחרי חתימה יכולה ליצור צורך בהון עצמי נוסף, ולכן עדיף לבדוק סיכון כזה בזמן.</p>\n" + APPR + "    </section>"),
    ("במקרה כזה בודקים גם עסקאות בודדות ברחוב.</p>\n    </section>", "במקרה כזה בודקים גם עסקאות בודדות ברחוב.</p>" + FAQ_HTML + "\n    </section>"),
    (SUM_CTA, SUM_CTA + S13),
    # banned in old text (language law): an em dash, and "בבדיקה"
    ('<a href="/apartment-prices/">מחירון הדירות של ישראל</a> — טווחי', '<a href="/apartment-prices/">מחירון הדירות של ישראל</a>: טווחי'),
    ("כך כדאי להשקיע יותר בבדיקה לפני התחייבות.", "כך כדאי להשקיע יותר בבדיקות לפני התחייבות."),
]

# ------------------------------------------------------------------------------------------------ GET, replace, check
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "q2s2"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,meta,link,modified" % PID)
assert s == 200, s
raw = r["content"]["raw"]; new = raw
assert "nlq2-css" not in raw, "stage 2 is already live"
for o, n in R:
    c = new.count(o)
    assert c == 1, (c, o[:80])
    new = new.replace(o, n)
ADDED = CSS + S4 + S5 + S6 + S9 + APPR + FAQ_HTML + S13


def visible(html):
    """Text a reader sees or hears: text nodes (SVG text included) and aria-labels; no styles, comments or tags."""
    h = re.sub(r"<style\b.*?</style>|<!--.*?-->", " ", html, flags=re.S)
    labels = " ".join(re.findall(r'aria-label="([^"]*)"', h))
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h) + " " + labels).replace(ig.LRM, "")


VIS_ALL, VIS_NEW = visible(new), visible(ADDED)
assert not re.search("[–—−]", VIS_ALL), "long dash in the visible text: %r" % re.findall(".{20}[–—−].{20}", VIS_ALL)[:3]
BANNED = r"ממשק|מערכת|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה|טעון אימות|נדל\"?ן חכם|דמו\b|הדגמה|מנגנון|שכבה|טכנולוגי|מודל\b"
assert not re.search(BANNED, VIS_NEW), "language DNA (new text): %r" % re.findall(r".{15}(?:%s).{15}" % BANNED, VIS_NEW)[:5]
assert not re.search(r"ממשק|מערכת|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה|טעון אימות|נדל\"?ן חכם", VIS_ALL), "language DNA (whole page)"
for sent in re.split(r"[.:;?]", VIS_NEW):  # our result is never a valuation: שומה only in a sentence about an appraiser or the bank
    if "שומה" in sent or "שומת" in sent:
        assert re.search("שמאי|הבנק|לבנק|מזמינים", sent), sent
# every number in the new text: registered from the data, a date of a source, a quarter, a series id, or a small count
txt = re.sub(r"\b(?:1-3|4-6|7-9|10-12)\.20(?:21|22|23|24|25|26)\b", " ", VIS_NEW)
CONST = {"20.8.2026", "25.10.2026", "26.10.2026", REG_UPD_HE, "1993", "100", "40010", "60000", "60300", "60500", "22", *[str(y) for y in range(2018, 2027)], "0", "10", "20", "30", "40", "360"}
bad = [x for x in re.findall(r"\d+(?:[.,]\d+)*", txt) if x not in REG and x not in CONST and not (x.isdigit() and int(x) <= 12)]
assert not bad, "untraced numbers: %r" % sorted(set(bad))[:20]
# internal links in the new text answer 200 (no redirect)


class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPEN = urllib.request.build_opener(NoRedir)
links = sorted(set(re.findall(r'href="(/[^"#]*)"', ADDED + R[1][1])))
for u in links:
    for attempt in range(4):  # a 5xx from a busy server is retried; a 3xx or 404 fails at once
        try:
            st = OPEN.open(urllib.request.Request("https://nad-lan.co.il" + u, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).status
        except urllib.error.HTTPError as e:
            st = e.code
        if st < 500:
            break
        time.sleep(10 * (attempt + 1))
    assert st == 200, (u, st)
faq_n = len(re.findall(r"<h3>", new[new.index("<h2>שאלות נפוצות"):new.index("<h2>סיכום")]))
qs_all = re.findall(r"<h3>(.*?)</h3>", new[new.index("<h2>שאלות נפוצות"):new.index("<h2>סיכום")])
assert faq_n == 25 and len(set(qs_all)) == 25, (faq_n, len(set(qs_all)))
assert new.count("<h1") == 1 and new.count('[nadlan_tool id="pval"') == raw.count('[nadlan_tool id="pval"') == 1
assert re.search(r"\[nadlan_tool id=\"pval\"[^\]]*\]", raw).group(0) in new
for o in re.findall(r"<h2[^>]*>(.*?)</h2>", raw):  # nothing old lost
    assert o in new, o
WORDS = lambda v: len(re.findall(r"[\w֐-׿\"']+", v))
svg_n = ADDED.count("<svg"); spark_n = ADDED.count('viewBox="0 0 110 28"')
print("[page %d] %d replacements, all matched once | internal links in new text: %d, all 200" % (PID, len(R), len(links)))
print("[new content] %d words (+%d in SVG labels) | tables %d | svg %d (%d sparklines + %d infographics) | h2 %d | h3 %d (%d FAQ) | numbers traced %d"
      % (WORDS(visible(re.sub(r"<svg\b.*?</svg>", " ", ADDED, flags=re.S))), WORDS(VIS_NEW) - WORDS(visible(re.sub(r"<svg\b.*?</svg>", " ", ADDED, flags=re.S))),
         ADDED.count("<table"), svg_n, spark_n, svg_n - spark_n, ADDED.count("<h2"), ADDED.count("<h3"), len(QA_NEW), len(REG)))
print("[whole content] %d words | tables %d in content (+1 in the tool) | svg %d | h2 %d | h3 %d | FAQ %d"
      % (WORDS(visible(re.sub(r"<svg\b.*?</svg>", " ", new, flags=re.S))), new.count("<table"), new.count("<svg"), new.count("<h2"), new.count("<h3"), faq_n))
print("[order] " + " > ".join(re.sub(r"<[^>]+>", "", h)[:28] for h in re.findall(r"<h2[^>]*>(.*?)</h2>", new)))
if DRY:
    os.makedirs(os.path.join(H, "preview"), exist_ok=True)
    io.open(os.path.join(H, "preview", "q2-stage2-content.html"), "w", encoding="utf-8", newline="").write(new)
    print("dry: preview/q2-stage2-content.html written; nothing sent")
    sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-stage2-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
s, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new}); assert s == 200, s
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
ok = {"read-back": back.strip() == new.strip(), "one h1": bd.count("<h1") == 1, "tool mounted": 'data-nli="pval"' in bd, "tool city table": "ברובן 1-3.2026" in bd,
      "T1 to T5": all(x in bd for x in ("מחיר חציוני לפי עיר וחדרים", "מדד מחירי הדירות לפי מחוז", "שלוש הבדיקות, דוגמה", "איפה בודקים מה", "מחשבון או שמאי")),
      "svg %d" % svg_n: bd.count('viewBox="0 0 110 28"') == spark_n and bd.count("<svg") >= svg_n, "one FAQPage": page.count('"@type":"FAQPage"') == 1,
      "25 questions": page.count('"@type":"Question"') == 25, "SoftwareApplication": '"@type":"SoftwareApplication"' in page, "css": 'id="nlq2-css"' in bd}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
