# -*- coding: utf-8 -*-
"""G5: the owner page for "דירות להשכרה" / "דירה להשכרה" (27,100 searches a month each, Israel; we are not seen in Search Console).
NEW page at /דירות-להשכרה/ (URL word audit: "דירות" 0 owners, "להשכרה" 0 owners; dna.md section 2). Spec: dna.md sections 6 to 8.
NOT RUN against the live site by the research session (owner order 26.10.2026: local only). Creating a new URL for a tier-A head
term is Ben's decision (keyword-guard rule 7); the releaser runs it after (1) Ben's yes, (2) the release that ships rentfair.js,
rent.json and the [nadlan_rent_listings] shortcode (instruments-snippet.md).

Every number on the page is computed here from plugins/nadlan-config/assets/instruments/data/rent.json (tools/instruments/
build_rent_data.py, checked by tools/instruments/test_rentfair.js) or is a dated official fact of dna.md section 6. Our own
calculations carry the words "החישוב שלנו". The listings are never typed: the shortcode prints the live count and cards.
Rendered order (content-first law): H1 (theme, from the title) -> answer paragraph -> CTA row -> [nadlan_tool id="rentfair"] ->
the listings -> today's numbers -> the city and neighbourhood tables -> the law -> tax -> checklists -> FAQ -> English -> sources.

  python write_g5_page.py --dry               (no REST at all: writes preview/, svg/, page-sources.md, kw-guard input; checks links by GET)
  python write_g5_page.py --dry --no-links    (fully offline)
  python write_g5_page.py --create            (Ben's yes only: creates the page as a DRAFT, reads it back)
  python write_g5_page.py --create --publish  (Ben's yes only: creates and publishes, then the live checks)"""
import io, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
DRY = "--dry" in sys.argv or "--create" not in sys.argv
PUBLISH = "--publish" in sys.argv
NOLINKS = "--no-links" in sys.argv
SITE = "https://nad-lan.co.il"; SLUG = "דירות-להשכרה"; PATH = "/" + SLUG + "/"; UPDATED = "26.10.2026"
TITLE = "דירות להשכרה: שכר הדירה בכל עיר ושכונה, הדירות באתר והחוק"
SEO_T = "דירות להשכרה 2026: מחירי שכירות בכל עיר ומחשבון שכר דירה"
SEO_D = "מחפשים דירה להשכרה? שכר הדירה החציוני ב־72 ערים ו־945 שכונות, ממוצעי הלמ״ס, בדיקת שכר דירה הוגן, הערובה המותרת בחוק והמס למשכיר. נתונים רשמיים 2026."
assert len(SEO_T) <= 60 and len(SEO_D) <= 160, (len(SEO_T), len(SEO_D))

A = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments")
D = json.load(io.open(os.path.join(A, "data", "rent.json"), encoding="utf-8"))
NAT, CITIES, IDX, LAW, TAX, SRC = D["nat"], D["cities"], D["idx"], D["law"], D["tax"], D["src"]
BY = {c["n"]: c for c in CITIES}
QM = {"03": "ינואר עד מרץ", "06": "אפריל עד יוני", "09": "יולי עד ספטמבר", "12": "אוקטובר עד דצמבר"}
HM = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]
def qlab(q): y, m = q.split("-"); return QM[m] + " " + y
def mlab(m): y, mm = m.split("-"); return HM[int(mm) - 1] + " " + y
def num(n, d=0): return ("{:,.%df}" % d).format(n)
def ils(n): return num(round(n)) + " ₪"
def sp(x, d=1): return ("+" if x > 0 else "−" if x < 0 else "") + ("%." + str(d) + "f%%") % abs(100 * x)
GROUP = {"2": "1-2", "3": "2.5-3", "4": "3.5-4", "5": "4.5+"}
GL = {"1-2": "1 עד 2 חדרים", "2.5-3": "2.5 עד 3 חדרים", "3.5-4": "3.5 עד 4 חדרים", "4.5+": "4.5 חדרים ומעלה", "total": "כל הגדלים"}
EN = {"אשדוד": "Ashdod", "אשקלון": "Ashkelon", "באר שבע": "Beersheba", "בית שמש": "Beit Shemesh", "בני ברק": "Bnei Brak", "בת ים": "Bat Yam",
      "הרצליה": "Herzliya", "חדרה": "Hadera", "חולון": "Holon", "חיפה": "Haifa", "ירושלים": "Jerusalem", "כפר סבא": "Kfar Saba", "נתניה": "Netanya",
      "פתח תקווה": "Petah Tikva", "ראשון לציון": "Rishon LeZion", "רחובות": "Rehovot", "רמת גן": "Ramat Gan", "תל אביב-יפו": "Tel Aviv-Yafo"}

# ------------------------------------------------------------------ the numbers the copy uses (cross-checked)
Q = NAT["r"]["4"]["q"]; QL = qlab(Q)
N4 = NAT["r"]["4"]["v"]; N3 = NAT["r"]["3"]["v"]; N5 = NAT["r"]["5"]["v"]
TA = BY["תל אביב-יפו"]; JLM = BY["ירושלים"]; HFA = BY["חיפה"]; BS = BY["באר שבע"]
CBS_T = NAT["cbs"]["total"]["a"]; CBS_T_P = NAT["cbs"]["total"]["p"]
NB = sum(len(c["nb"]) for c in CITIES); NC = len(CITIES); NCBS = len([c for c in CITIES if c.get("cbs")])
assert (N4, N3, NC, NB, NCBS) == (4825, 3875, 72, 945, 18), (N4, N3, NC, NB, NCBS)
assert abs(CBS_T - 5085.5) < 0.01 and TA["r"]["4"]["v"] == 10500 and IDX["last"] == "2026-09" and IDX["yoy"] == 3.2
cbs_rank = sorted([c for c in CITIES if c.get("cbs") and c["cbs"].get("total")], key=lambda c: -c["cbs"]["total"]["a"])
CHEAP, DEAR = cbs_rank[-1], cbs_rank[0]
TEN_BE = TAX["double"] * TAX["first"] / (2 * TAX["first"] - TAX["ten"])  # 12(2R - D)r1 = 12 R r10  ->  R = D r1 / (2 r1 - r10)

# ------------------------------------------------------------------ drawings (Instruments palette, 420 wide, rtl text, 12 px min)
INK, SEA, DEEP, LINE, MUTE, PAPER = "#12202A", "#2F6F86", "#1F4B5C", "#D3DCE2", "#5E6A75", "#F6F8F9"
def tx(x, y, s, anchor="right", size=13, weight=400, fill=INK, mono=False):
    # anchor is visual: "right" = the text's right edge at x, "left" = its left edge at x. With direction="rtl" SVG reads
    # text-anchor in the writing direction (start = right edge), so the mapping differs for Hebrew and for mono numbers.
    if mono: a = {"right": "end", "left": "start", "middle": "middle"}[anchor]; fam = ' font-family="IBM Plex Mono, ui-monospace, monospace" direction="ltr"'
    else: a = {"right": "start", "left": "end", "middle": "middle"}[anchor]; fam = ' direction="rtl"'
    return '<text x="%s" y="%s" text-anchor="%s" font-size="%s" font-weight="%s" fill="%s"%s>%s</text>' % (round(x, 1), round(y, 1), a, size, weight, fill, fam, s)
def svg_open(h, label):
    g = "".join('<line x1="%d" y1="0" x2="%d" y2="%d" stroke="%s" stroke-width="0.5" opacity="0.55"/>' % (x, x, h, LINE) for x in range(0, 421, 21))
    return ('<svg viewBox="0 0 420 %d" role="img" aria-label="%s" font-family="IBM Plex Sans Hebrew, system-ui, sans-serif" style="max-width:100%%;height:auto;display:block">'
            '<rect width="420" height="%d" fill="%s"/>%s' % (h, label, h, PAPER, g))

def svg_cities():
    rows = sorted([c for c in CITIES if c.get("cbs") and c["cbs"].get("3.5-4")], key=lambda c: -c["cbs"]["3.5-4"]["a"])
    nat = NAT["cbs"]["3.5-4"]["a"]; top = 70; rh = 22; h = top + rh * len(rows) + 44
    mx = max(c["cbs"]["3.5-4"]["a"] + c["cbs"]["3.5-4"]["e"] for c in rows); x0 = 262; L = 246
    xv = lambda v: x0 - L * v / mx
    s = svg_open(h, "שכר דירה ממוצע לדירת 3.5 עד 4 חדרים ב־%d ערים, %s, עם טעות הדגימה" % (len(rows), QL))
    s += tx(410, 24, "שכר דירה ממוצע, 3.5 עד 4 חדרים", size=15, weight=700) + tx(410, 44, "%s · הלמ״ס, לוח 4.9 · בשקלים לחודש" % QL, size=12, fill=MUTE)
    s += tx(xv(nat) + 4, top - 8, "ממוצע ארצי " + num(nat), anchor="left", size=12, fill=INK)
    for i, c in enumerate(rows):
        y = top + i * rh; v = c["cbs"]["3.5-4"]["a"]; e = c["cbs"]["3.5-4"]["e"]
        s += tx(410, y + 15, c["n"], size=13)
        s += tx(318, y + 15, num(v), size=12.5, mono=True)
        s += '<rect x="%.1f" y="%d" width="%.1f" height="13" fill="%s"/>' % (xv(v), y + 4, x0 - xv(v), SEA if v >= nat else "#8FB3C1")
        s += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.5"/>' % (xv(v + e), y + 10.5, xv(v - e), y + 10.5, INK)
    s += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.2" stroke-dasharray="4 3"/>' % (xv(nat), top - 2, xv(nat), top + rh * len(rows), INK)
    s += tx(410, h - 26, "עמודה כהה: מעל הממוצע הארצי. בהירה: מתחתיו.", size=12, fill=MUTE) + tx(410, h - 10, "הקו הדק בקצה כל עמודה: טעות הדגימה של הלמ״ס", size=12, fill=MUTE)
    return s + "</svg>"

def svg_index():
    ser = IDX["s"]; h = 260; x0, x1, y0, y1 = 44, 400, 76, 206
    lo, hi = 2.0, 5.0
    xs = lambda i: x0 + (x1 - x0) * i / (len(ser) - 1); ys = lambda v: y1 - (y1 - y0) * (v - lo) / (hi - lo)
    s = svg_open(h, "מדד שכר הדירה של הלמ״ס, השינוי ב־12 חודשים בכל חודש, %s עד %s" % (mlab(ser[0][0]), mlab(ser[-1][0])))
    s += tx(410, 24, "שכר הדירה ב־12 חודשים, כל חודש", size=15, weight=700) + tx(410, 44, "מדד שכר הדירה של הלמ״ס, %s עד %s" % (mlab(ser[0][0]), mlab(ser[-1][0])), size=12, fill=MUTE)
    for v in (2, 3, 4, 5):
        s += '<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s"/>' % (x0, ys(v), x1, ys(v), LINE) + tx(x0 - 6, ys(v) + 4, "%d%%" % v, anchor="right", size=12, fill=MUTE, mono=True)
    s += '<polyline fill="none" stroke="%s" stroke-width="2.4" points="%s"/>' % (SEA, " ".join("%.1f,%.1f" % (xs(i), ys(m[2])) for i, m in enumerate(ser)))
    for i in (0, len(ser) - 1):
        s += '<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (xs(i), ys(ser[i][2]), DEEP)
        s += tx(xs(i) + (6 if i == 0 else -6), ys(ser[i][2]) - 10, "%.1f%%" % ser[i][2], anchor="left" if i == 0 else "right", size=13, weight=600, mono=True)
    for i, m in enumerate(ser):
        if m[0].endswith("-01") or i in (0, len(ser) - 1):
            s += tx(xs(i), y1 + 20, m[0][5:] + "/" + m[0][2:4], anchor="middle", size=12, fill=MUTE, mono=True)
    s += tx(410, h - 12, "בציר: חודש/שנה. המדד הוא חלק ממדד המחירים לצרכן", size=12, fill=MUTE)
    return s + "</svg>"

def svg_lease():
    g = LAW["guarantee"]; rp = LAW["repairs"]; nt = LAW["notice"]
    steps = [("לפני החתימה", "חוזה בכתב, העתק חתום לכל צד. ערובה שעולה כסף: עד %d חודשי שכירות או שליש מהתקופה, הנמוך מביניהם" % g["months"]),
             ("מסירת הדירה", "דירה ראויה למגורים, פנויה, עם הוראות תחזוקה ושימוש"),
             ("במהלך השכירות", "ליקוי שלא מאפשר לגור: תיקון עד %d ימים. ליקוי אחר: עד %d יום" % (rp["urgent"], rp["other"])),
             ("%d יום לפני הסוף" % nt["landlordOption"], "המשכיר מודיע אם הוא מממש אופציה, או מבטל לפי סעיף ביטול"),
             ("%d יום לפני הסוף" % nt["tenantOption"], "השוכר מודיע אם הוא מממש אופציה, או מבטל לפי סעיף ביטול"),
             ("עד %d יום אחרי הסוף" % g["returnDays"], "המשכיר מחזיר את הערובה עם פירותיה, אחרי שהדירה הוחזרה והחובות שולמו")]
    h = 76 + 66 * len(steps) + 6
    s = svg_open(h, "חוזה שכירות למגורים על ציר הזמן לפי חוק השכירות והשאילה")
    s += tx(410, 26, "החוזה על ציר הזמן", size=15, weight=700) + tx(410, 46, "חוק השכירות והשאילה, סימן ו׳: חוזה שכירות למגורים", size=12, fill=MUTE)
    s += '<line x1="398" y1="76" x2="398" y2="%d" stroke="%s" stroke-width="2"/>' % (76 + 66 * (len(steps) - 1), DEEP)
    for i, (a, b) in enumerate(steps):
        y = 76 + 66 * i
        s += '<circle cx="398" cy="%d" r="7" fill="%s" stroke="%s" stroke-width="2"/>' % (y, "#FFFFFF" if i % 2 else SEA, DEEP)
        s += tx(382, y + 5, a, size=14, weight=700)
        words, line, lines = b.split(" "), "", []
        for w in words:
            if len(line) + len(w) > 50: lines.append(line.strip()); line = ""
            line += w + " "
        lines.append(line.strip())
        for k, ln in enumerate(lines[:2]): s += tx(382, y + 24 + 16 * k, ln, size=12.5, fill="#3E4C58")
    return s + "</svg>"

def fig(svg, cap): return '<figure class="nlrh-fig">%s<figcaption>%s</figcaption></figure>\n' % (svg, cap)
def table(cap, head, rows, num_cols=(), note=""):
    h = '<p class="nlrh-cap">%s</p>\n<div class="nlrh-t"><table><thead><tr>%s</tr></thead><tbody>\n' % (cap, "".join("<th>%s</th>" % x for x in head))
    for r in rows:
        h += "<tr>" + "".join(("<th>%s</th>" % c) if i == 0 else ('<td class="n">%s</td>' % c if i in num_cols else "<td>%s</td>" % c) for i, c in enumerate(r)) + "</tr>\n"
    return h + "</tbody></table></div>\n" + ('<p class="nlrh-note">%s</p>\n' % note if note else "")

# ------------------------------------------------------------------ tables
def t_national():
    rows = []
    for r in ("2", "3", "4", "5", "all"):
        g = NAT["r"].get(r); cg = "total" if r == "all" else GROUP[r]; c = NAT["cbs"].get(cg)
        lab = {"2": "עד 2 חדרים", "all": "כל הגדלים"}.get(r, r + " חדרים")
        rows.append([lab, ils(g["v"]) if g else "אין חציון רשמי", GL[cg], (ils(c["a"]) + "<small>±%s</small>" % num(c["e"])) if c else "", sp(c["a"] / c["p"] - 1) if c and c.get("p") else ""])
    return table("שכר הדירה בישראל היום, לפי מספר החדרים", ["גודל", "חציון, " + QL + " (אתר הנדל״ן הממשלתי)", "קבוצת הלמ״ס", "ממוצע, " + QL + " (הלמ״ס)", "מול " + qlab("2025-06") + " (החישוב שלנו)"],
                 rows, (1, 3, 4), "החציון: חצי מהחוזים יקרים ממנו וחצי זולים. הממוצע של הלמ״ס מגיע עם טעות הדגימה (±). שני המקורות נמדדים במדגמים ובשיטות שונים, ולכן המספרים לא זהים.")

def t_cbs_cities():
    rows = []
    for c in cbs_rank:
        cb = c["cbs"]; cell = lambda g: (num(cb[g]["a"]) + "<small>±%s</small>" % num(cb[g]["e"])) if cb.get(g) else ""
        rows.append([c["n"], cell("1-2"), cell("2.5-3"), cell("3.5-4"), cell("4.5+"), cell("total"), sp(cb["total"]["a"] / cb["total"]["p"] - 1) if cb["total"].get("p") else ""])
    n = NAT["cbs"]; cell = lambda g: num(n[g]["a"]) + "<small>±%s</small>" % num(n[g]["e"])
    rows.append(["כל הארץ", cell("1-2"), cell("2.5-3"), cell("3.5-4"), cell("4.5+"), cell("total"), sp(n["total"]["a"] / n["total"]["p"] - 1)])
    return table("שכר דירה ממוצע ב־%d הערים הגדולות, %s, בשקלים לחודש" % (len(cbs_rank), QL), ["עיר", "1 עד 2 חדרים", "2.5 עד 3", "3.5 עד 4", "4.5 ומעלה", "כל הגדלים", "בשנה (החישוב שלנו)"],
                 rows, (1, 2, 3, 4, 5, 6), "הלמ״ס, ירחון המחירים, לוח 4.9: שכר דירה ממוצע בשוק החופשי. השינוי בשנה: כל הגדלים מול %s." % qlab("2025-06"))

def t_districts():
    rows = [[x["n"], num(x["cbs"]["total"]["a"]) + "<small>±%s</small>" % num(x["cbs"]["total"]["e"]), num(x["cbs"]["3.5-4"]["a"]) if x["cbs"].get("3.5-4") else "", sp(x["cbs"]["total"]["a"] / x["cbs"]["total"]["p"] - 1)]
            for x in sorted(D["dist"], key=lambda x: -x["cbs"]["total"]["a"])]
    return table("שכר דירה ממוצע לפי מחוז, %s" % QL, ["מחוז", "כל הגדלים", "3.5 עד 4 חדרים", "בשנה (החישוב שלנו)"], rows, (1, 2, 3))

def t_all_cities():
    rows = []
    for c in sorted(CITIES, key=lambda c: c["n"]):
        r = c["r"]; cell = lambda k: ils(r[k]["v"]) if r.get(k) else ""
        al = r.get("all")
        rows.append([c["n"], cell("3"), cell("4"), cell("5"), cell("all"), sp(al["yoy"] / 100) if al and al.get("yoy") is not None else ""])
    return table("שכר הדירה החציוני ב־%d ערים לפי מספר החדרים, %s" % (NC, QL), ["עיר", "3 חדרים", "4 חדרים", "5 חדרים", "כל הגדלים", "השינוי השנתי בקובץ"],
                 rows, (1, 2, 3, 4, 5), "אתר הנדל״ן הממשלתי, קובצי השכירות לפי עיר, גרסה %s. תא ריק: הקובץ לא מפרסם חציון לגודל הזה בעיר. השינוי השנתי: כפי שהקובץ מפרסם אותו, כל הגדלים." % SRC["gov"]["he"].split("גרסה ")[-1])

def t_hoods():
    rows = []
    for n in ("תל אביב-יפו", "ירושלים", "חיפה", "רמת גן", "פתח תקווה", "ראשון לציון", "נתניה", "באר שבע"):
        c = BY[n]; nb = c["nb"]; all_ly = c["r"]["all"]["ly"]
        top = "<br>".join("%s <small>%s</small>" % (x[0], ils(x[1])) for x in nb[:3]); low = "<br>".join("%s <small>%s</small>" % (x[0], ils(x[1])) for x in nb[-3:][::-1])
        rows.append([n, ils(all_ly), top, low, str(len(nb))])
    return table("השכונות היקרות והזולות לשכירות ב־8 ערים, כל הגדלים, השנה האחרונה בקובץ", ["עיר", "העיר כולה", "3 השכונות היקרות", "3 השכונות הזולות", "שכונות בקובץ"], rows, (1, 4),
                 "שכר דירה חציוני לכל הגדלים בכל שכונה, כפי שאתר הנדל״ן הממשלתי מפרסם אותו. דירה גדולה בשכונה זולה יכולה לעלות יותר מדירה קטנה בשכונה יקרה; במחשבון למעלה בוחרים שכונה ומספר חדרים.")

def t_ta():
    c = TA; ly = c["r"]["all"]["ly"]; r3 = c["r"]["3"]["v"]
    rows = [[x[0], ils(x[1]), sp(x[1] / ly - 1), ils(round(r3 * x[1] / ly / 50) * 50)] for x in c["nb"]]
    return table("דירות להשכרה בתל אביב: שכר הדירה החציוני בכל %d השכונות בקובץ" % len(rows), ["שכונה", "כל הגדלים, השנה האחרונה", "מול העיר (%s)" % ils(ly), "הערכה ל־3 חדרים (החישוב שלנו)"], rows, (1, 2, 3),
                 "הערכה ל־3 חדרים = החציון של דירות 3 חדרים בעיר (%s, %s) כפול היחס בין השכונה לעיר. זו הערכה, לא נתון רשמי." % (ils(r3), QL))

def t_index():
    rows = [[mlab(m[0]), sp(m[1] / 100), sp(m[2] / 100)] for m in IDX["s"][-12:][::-1]]
    return table("מדד שכר הדירה, 12 החודשים האחרונים", ["חודש", "שינוי בחודש", "שינוי ב־12 חודשים"], rows, (1, 2), "הלמ״ס, מדד שכר הדירה (120460): " + IDX["name"] + ".")

def t_guarantee():
    rows = []
    for rent in (3000, 4500, 6000, 8000, 10000, 15000):
        rows.append([ils(rent)] + [ils(min(3 * rent, rent * m / 3)) for m in (6, 9, 12, 24)])
    return table("הערובה המרבית שמותר לבקש לפי החוק, כשהערובה עולה לשוכר כסף", ["שכר דירה לחודש", "חוזה ל־6 חודשים", "9 חודשים", "12 חודשים", "24 חודשים"], rows, (1, 2, 3, 4),
                 "חוק השכירות והשאילה, סעיף 25י(ב): הנמוך מבין 3 חודשי שכירות ושליש משכר הדירה לכל התקופה. חל על פיקדון במזומן, ערבות בנקאית וערבות מחברה מורשית; כתב ערבות של ערבים אישיים, שלא עולה לשוכר כסף, לא נספר בתקרה.")

def t_pays():
    rows = [[a, b] for a, b in zip(LAW["tenantPays"] + [""] * 3, LAW["tenantNot"] + [""] * 4)][:4]
    return table("מי משלם מה בשכירות למגורים", ["השוכר משלם", "השוכר לא משלם"], rows, (), "סעיף 25ט לחוק. אי אפשר להתנות על זה בחוזה לרעת השוכר (סעיף 25יד).")

def t_deadlines():
    g, rp, nt, sc = LAW["guarantee"], LAW["repairs"], LAW["notice"], LAW["scope"]
    rows = [["ליקוי שלא מאפשר לגור בדירה באופן סביר", "המשכיר מתקן עד %d ימים מהדרישה" % rp["urgent"], "25ח(ב)"],
            ["ליקוי אחר, שאינו קל ערך", "המשכיר מתקן עד %d יום מהדרישה" % rp["other"], "25ח(ב)"],
            ["ליקוי שנגרם משימוש לא סביר", "על השוכר", "25ח(א)"],
            ["אופציה של המשכיר להאריך", "הודעה לפחות %d יום לפני הסוף, ורק בתנאים שנקבעו מראש" % nt["landlordOption"], "25יב(ב)"],
            ["אופציה של השוכר להאריך", "הודעה לפחות %d יום לפני הסוף" % nt["tenantOption"], "25יב(ג)"],
            ["ביטול בלי הפרה", "רק אם גם לשוכר יש זכות כזו; המשכיר מודיע %d יום מראש, השוכר %d יום" % (nt["landlordCancel"], nt["tenantCancel"]), "25יג"],
            ["החזרת הערובה", "עד %d יום מהחזרת הדירה, או מתשלום החובות, המאוחר, עם הפירות" % g["returnDays"], "25י(ה)"],
            ["מכירת הדירה בזמן השכירות", "המשכיר מודיע בכתב, עם פרטי הקונה, לפני המסירה לקונה", "25יא"]]
    return table("המועדים שבחוק", ["מה", "הכלל", "סעיף"], rows, (), "הפרק חל על חוזה ליותר מ־%d חודשים (או עם אופציה) ועד %d שנים, כששכר הדירה עד %s." % (sc["minMonths"], sc["maxYears"], sc["ceilingNote"]))

def taxrow(R):
    C, Dd = TAX["ceiling"], TAX["double"]; t = 0 if R <= C else (2 * R - Dd if R < Dd else R)
    return [ils(R), "פטור מלא" if t == 0 else ils(t), "0 ₪" if t == 0 else ils(12 * t * TAX["first"]), ils(12 * R * TAX["ten"]), ils(12 * R * TAX["first"])]
def t_tax():
    rows = [taxrow(R) for R in (4000, TAX["ceiling"], 7000, 9000, TAX["double"], 14000)]
    rows = [[r[0], r[1], r[2] if r[2] != "0 ₪" else "אין מס", r[3], r[4]] for r in rows]
    return table("מס על שכר דירה למגורים, %d: שלושת המסלולים, בשקלים (החישוב שלנו)" % TAX["year"], ["שכר דירה לחודש", "חייב במס בחודש, מסלול הפטור", "מס בשנה, מסלול הפטור, 31%", "מס בשנה, מסלול 10%", "מס בשנה, מסלול רגיל, 31% לפני הוצאות"],
                 rows, (1, 2, 3, 4), "תקרת הפטור %s לחודש; הפטור החלקי עד %s. 31%% הוא שיעור המס המזערי על הכנסה כזאת למי שמתחת לגיל 60 (10%% מגיל 60), במסלול הפטור ובמסלול הרגיל; במסלול הרגיל מנכים הוצאות ופחת, ולכן המס בו נמוך מהסכום בטבלה. מסלול 10%% משלמים עד %s." % (ils(TAX["ceiling"]), ils(TAX["double"]), TAX["tenDue"]))
def t_ceiling():
    rows = [[str(y), ils(v)] for y, v in TAX["history"][::-1]]
    return table("תקרת הפטור ממס על שכר דירה, לחודש", ["שנה", "תקרה"], rows, (1,), "כל זכות, לפי הודעות רשות המסים.")

def ul(items): return "<ul>" + "".join("<li>%s</li>" % x for x in items) + "</ul>\n"

# ------------------------------------------------------------------ copy (language DNA: portal category words, second person plural, no tech talk)
LEAD = ('<p class="nlrh-lead">מחפשים דירה להשכרה? שכר הדירה החציוני לדירת 4 חדרים בישראל עמד על %s ב%s, ובתל אביב-יפו על %s. כאן תמצאו את שכר הדירה ב־%d ערים ו־%s שכונות לפי אתר הנדל״ן הממשלתי והלמ״ס, '
        'בדיקה אם שכר הדירה שמבקשים מכם הוגן, את הדירות להשכרה שמפורסמות באתר, ואת הכללים שבחוק: ערובה של עד 3 חודשי שכירות, תיקון ליקוי דחוף תוך 3 ימים, ופטור ממס למשכיר עד %s בחודש.</p>\n'
        % (ils(N4), QL, ils(TA["r"]["4"]["v"]), NC, num(NB), ils(TAX["ceiling"])))
CTA = ('<div class="nlrh-cta"><a class="is-primary" href="#rentfair">בדקו את שכר הדירה</a><a href="#listings">לדירות להשכרה באתר</a>'
       '<a href="%s/post-listing/">פרסום מודעה בחינם</a><a href="#law">הזכויות בחוק</a></div>\n' % SITE)
TOOL = '<div id="rentfair">[nadlan_tool id="rentfair"]</div>\n'
LIST = ('<h2 id="listings">הדירות להשכרה באתר עכשיו</h2>\n<p>מודעות של מתווכים עם רישיון ושל בעלי דירות. בכל מודעה שכר הדירה כשפורסם, החדרים, השטח, הקומה ומה יש בדירה, '
        'ובמודעה של מתווך גם שמו ומספר הרישיון. פונים ישירות למפרסם מתוך המודעה.</p>\n[nadlan_rent_listings limit="12"]\n'
        '<p>יש לכם דירה להשכרה? <a href="%s/post-listing/">פרסום מודעה בחינם</a>, בלי עמלה. רוצים לנהל את הדירות המושכרות שלכם במקום אחד: '
        '<a href="%s/my-rentals/">ניהול נכסים מושכרים</a>.</p>\n' % (SITE, SITE))
TODAY = ('<h2>שכר הדירה היום: המספרים</h2>\n'
         '<p>שני גופים רשמיים מפרסמים את שכר הדירה בישראל. אתר הנדל״ן הממשלתי מפרסם <strong>חציון</strong> לכל עיר, לפי מספר החדרים ולכל שכונה. הלמ״ס מפרסמת <strong>ממוצע</strong> ל־%d הערים הגדולות ולמחוזות, עם טעות הדגימה. '
         'לפי הלמ״ס, שכר הדירה הממוצע בישראל ב%s עמד על %s לחודש, %s לעומת %s. מדד שכר הדירה עלה ב־%s ב־12 החודשים שעד %s.</p>\n'
         % (NCBS, QL, ils(CBS_T), sp(CBS_T / CBS_T_P - 1), qlab("2025-06"), "%.1f%%" % IDX["yoy"], mlab(IDX["last"]))) + t_national()
CITY = ('<h2>שכר דירה ממוצע בכל עיר</h2>\n'
        '<p>ב%s העיר היקרה ביותר לשכירות מבין %d הערים הגדולות הייתה %s, עם ממוצע של %s לחודש לכל הגדלים, והזולה ביותר %s, עם %s. '
        'דירת 3.5 עד 4 חדרים בתל אביב-יפו עלתה בממוצע %s לחודש, בירושלים %s, בחיפה %s ובבאר שבע %s.</p>\n'
        % (QL, NCBS, DEAR["n"], ils(DEAR["cbs"]["total"]["a"]), CHEAP["n"], ils(CHEAP["cbs"]["total"]["a"]), ils(TA["cbs"]["3.5-4"]["a"]), ils(JLM["cbs"]["3.5-4"]["a"]), ils(HFA["cbs"]["3.5-4"]["a"]), ils(BS["cbs"]["3.5-4"]["a"])))
CITY += fig(svg_cities(), "שכר דירה ממוצע לדירת 3.5 עד 4 חדרים, %s, עם טעות הדגימה של הלמ״ס. הקו המקווקו: הממוצע הארצי." % QL) + t_cbs_cities() + t_districts()
ALLC = ('<h2>שכר הדירה החציוני ב־%d ערים, לפי מספר החדרים</h2>\n<p>החציון של אתר הנדל״ן הממשלתי מגיע ל־%d ערים ולשלושה גדלים: 3, 4 ו־5 חדרים. בישראל כולה: %s לדירת 3 חדרים, %s ל־4 חדרים ו־%s ל־5 חדרים (%s). '
        'בטבלה כל עיר, מסודרת לפי א״ב; במחשבון למעלה בוחרים עיר ושכונה ורואים גם את השכונות.</p>\n' % (NC, NC, ils(N3), ils(N4), ils(N5), QL)) + t_all_cities()
HOODS = ('<h2>השכונות היקרות והזולות לשכירות</h2>\n<p>האתר הממשלתי מפרסם שכר דירה חציוני ל־%s שכונות ב־%d ערים. הפערים בתוך העיר גדולים: בתל אביב-יפו השכונה היקרה בקובץ, %s, עומדת על %s לחודש לכל הגדלים, '
         'והזולה, %s, על %s.</p>\n' % (num(NB), len([c for c in CITIES if c["nb"]]), TA["nb"][0][0], ils(TA["nb"][0][1]), TA["nb"][-1][0], ils(TA["nb"][-1][1]))) + t_hoods()
TAS = ('<h2>דירות להשכרה בתל אביב: שכר הדירה בכל שכונה</h2>\n<p>תל אביב-יפו היא העיר עם שכר הדירה הגבוה בישראל: החציון לדירת 3 חדרים %s, ל־4 חדרים %s ול־5 חדרים %s (%s). '
       'רוב הדירות להשכרה שמפורסמות היום באתר נמצאות בתל אביב, בנופי ים, צוקי אביב, רמת אביב ושרונה.</p>\n' % (ils(TA["r"]["3"]["v"]), ils(TA["r"]["4"]["v"]), ils(TA["r"]["5"]["v"]), QL)) + t_ta()
TREND = ('<h2>איך שכר הדירה זז: מדד שכר הדירה</h2>\n<p>מדד שכר הדירה של הלמ״ס עולה בכל חודש, אבל לאט יותר: %s ב־12 החודשים שעד %s, ו־%s בחודש האחרון, לעומת %s ב־12 החודשים שעד %s.מי שחוזה השכירות שלו צמוד למדד המחירים לצרכן יכול לחשב את ההצמדה '
         'ב<a href="%s/cpi-calculator/">מחשבון הצמדה למדד</a>; מי שמתחדש לו חוזה יכול לבדוק את הסכום החדש במחשבון שכר הדירה בראש העמוד.</p>\n'
         % ("%.1f%%" % IDX["yoy"], mlab(IDX["last"]), "%.1f%%" % IDX["mom"], "%.1f%%" % IDX["s"][0][2], mlab(IDX["s"][0][0]), SITE)) + fig(svg_index(), "השינוי ב־12 חודשים במדד שכר הדירה, כל חודש מ%s עד %s." % (mlab(IDX["s"][0][0]), mlab(IDX["last"]))) + t_index()
LAWS = ('<h2 id="law">מה החוק אומר: חוק שכירות הוגנת</h2>\n<p>מאז 2017 יש בחוק השכירות והשאילה פרק על שכירות למגורים, שנקרא חוק שכירות הוגנת. ברוב הסעיפים אי אפשר לוותר עליו בחוזה לרעת השוכר. '
        'הפרק חל על חוזה ליותר מ־3 חודשים ועד 10 שנים, ולא חל על בית מלון או דירת נופש, מעונות, דיור מוגן, דירה בשכירות מוגנת ושכר דירה מעל התקרה. בשנת התשפ״ו הוסיף המחוקק להגדרת הערובה גם ערבות של חברות אשראי, תשלומים וביטוח.</p>\n'
        + fig(svg_lease(), "החוזה על ציר הזמן: הערובה, המסירה, התיקונים, ההודעות וההחזר, לפי סימן ו׳ של חוק השכירות והשאילה.")
        + '<h3>כמה ערובה מותר לבקש</h3>\n<p>כשהערובה עולה לשוכר כסף, פיקדון במזומן, ערבות בנקאית או ערבות מחברה, הסכום הכולל מוגבל לנמוך מבין 3 חודשי שכירות ושליש משכר הדירה לכל התקופה. '
          'המשכיר רשאי לממש את הערובה רק על שכר דירה שלא שולם, ליקוי שהשוכר אחראי לו ולא תיקן, ארנונה וחשבונות שלא שולמו, או אי פינוי, ורק אחרי הודעה מראש.</p>\n' + t_guarantee()
        + '<h3>מי משלם מה</h3>\n' + t_pays()
        + '<h3>מתי הדירה לא ראויה למגורים</h3>\n<p>המשכיר חייב למסור דירה ראויה למגורים. לפי התוספת הראשונה לחוק, דירה אינה ראויה אם:</p>\n' + ul(LAW["unfit"])
        + '<h3>מה חייב להיות בחוזה</h3>\n<p>חוזה שכירות למגורים נערך בכתב, נחתם בידי שני הצדדים, וכל צד מקבל העתק חתום. לפי התוספת השנייה הוא כולל:</p>\n' + ul(LAW["contract"])
        + '<p>הסעיפים, הנוסח והבטוחות בפירוט: <a href="%s/real-estate-lawyer/residential-lease-agreement/">חוזה שכירות דירה</a>.</p>\n' % SITE
        + '<h3>המועדים</h3>\n' + t_deadlines())
TAXS = ('<h2>מס על שכר דירה: שלושת המסלולים למשכיר</h2>\n<p>מי שמשכיר דירה למגורים בוחר בין שלושה מסלולים. <strong>פטור:</strong> עד %s בחודש, על סך שכר הדירה מכל הדירות, לא משלמים מס; בין %s ל־%s הפטור קטן, ומעל %s אין פטור. '
        '<strong>10%%:</strong> מס של 10%% מהשקל הראשון, בלי הוצאות ופחת, ומשלמים פעם בשנה עד %s. <strong>רגיל:</strong> מנכים הוצאות ופחת ומשלמים לפי מדרגות המס.</p>\n'
        '<p>לפי החישוב שלנו, למשכיר מתחת לגיל 60 מסלול 10%% זול ממסלול הפטור החל מכ־%s בחודש. מגיל 60 המדרגה הראשונה היא 10%%, ולכן מסלול הפטור לא יקר ממסלול 10%% עד %s. '
        'בעל דירה יחידה שמשכיר אותה ושוכר דירה אחרת למגוריו מקטין את הבסיס במסלול 10%% בשכר הדירה שהוא משלם, עד %s בחודש.</p>\n'
        % (ils(TAX["ceiling"]), ils(TAX["ceiling"]), ils(TAX["double"]), ils(TAX["double"]), TAX["tenDue"], ils(round(TEN_BE / 10) * 10), ils(TAX["double"]), ils(TAX["offsetCap"]))) + t_tax() + t_ceiling()
CHECK = ('<h2>לפני שחותמים: רשימת בדיקה לשוכרים</h2>\n' + ul([
    'בדקו את שכר הדירה מול החציון בעיר ובשכונה, במחשבון בראש העמוד.',
    'ודאו שמי שמשכיר הוא בעל הדירה או מורשה מטעמו: <a href="%s/tabu-extract-check/">בדיקת נסח טאבו</a>.' % SITE,
    'קראו את החוזה לפני החתימה ובדקו את סעיף ההעלאה, האופציה והביטול.',
    'חשבו את הערובה מול התקרה בחוק, וקבעו בכתב מתי ואיך היא חוזרת.',
    'צלמו את הדירה ביום המסירה ורשמו בפרוטוקול כל ליקוי, מונה וריהוט.',
    'העבירו על שמכם את הארנונה, החשמל, המים והגז מיום הכניסה.',
    'שאלו מי הזמין את המתווך: מתווך מטעם המשכיר לא גובה מהשוכר.']) +
    '<h2>למשכירים: לקבוע מחיר, להשכיר ולנהל</h2>\n' + ul([
    'קבעו מחיר לפי החציון בעיר ובשכונה, ולפי מה שיש בדירה: חניה, מעלית, ממ״ד, מרפסת וריהוט.',
    'בחרו מסלול מס לפני תחילת השנה, לפי שכר הדירה מכל הדירות שלכם.',
    'פרסמו את הדירה בחינם: <a href="%s/post-listing/">פרסום מודעה בחינם</a>.' % SITE,
    'נהלו שוכרים, תשלומים, תיקונים ומסמכים במקום אחד: <a href="%s/my-rentals/">ניהול נכסים מושכרים</a>.' % SITE,
    'שוקלים לקנות דירה להשקעה? התשואה משכירות בכל עיר: <a href="%s/investment/">נדל״ן להשקעה</a>.' % SITE]) +
    '<h2>שכירות לטווח ארוך, דירה להשכיר ודמי מפתח</h2>\n'
    '<p><strong>שכירות לטווח ארוך</strong> היא דירה בבניין שנבנה להשכרה, לרוב בחוזה לכמה שנים עם עדכון מחיר שנקבע מראש. החברה הממשלתית "דירה להשכיר" מקדמת מכרזים לפרויקטים כאלה, ויזמים פרטיים משכירים בבניינים משלהם; התנאים, ההנחות והזכאות נקבעים בכל פרויקט.</p>\n'
    '<p><strong>דמי מפתח</strong> הם תשלום על שכירות מוגנת לפי חוק הגנת הדייר: דייר מוגן שילם בתחילת הדרך, ובעזיבה מתחלקים דמי המפתח לפי החוק. על דירה כזאת לא חל פרק השכירות ההוגנת.</p>\n'
    '<p>מתלבטים אם להמשיך לשכור או לקנות? <a href="%s/buy-vs-rent/">מחשבון קנייה מול שכירות</a>.</p>\n' % SITE)

FAQ = [
 ("כמה עולה לשכור דירה בישראל?", "לפי הלמ״ס, שכר הדירה הממוצע ב%s עמד על %s לחודש לכל הגדלים: %s לדירת 1 עד 2 חדרים, %s ל־2.5 עד 3 חדרים, %s ל־3.5 עד 4 חדרים ו־%s לדירה של 4.5 חדרים ומעלה. החציון של אתר הנדל״ן הממשלתי לדירת 4 חדרים עמד על %s."
   % (QL, ils(CBS_T), ils(NAT["cbs"]["1-2"]["a"]), ils(NAT["cbs"]["2.5-3"]["a"]), ils(NAT["cbs"]["3.5-4"]["a"]), ils(NAT["cbs"]["4.5+"]["a"]), ils(N4))),
 ("מה שכר הדירה הממוצע בתל אביב?", "לפי הלמ״ס, %s לחודש לכל הגדלים ב%s, ו־%s לדירת 3.5 עד 4 חדרים. החציון של אתר הנדל״ן הממשלתי: %s לדירת 3 חדרים ו־%s לדירת 4 חדרים. בטבלת השכונות למעלה כל %d השכונות בקובץ."
   % (ils(TA["cbs"]["total"]["a"]), QL, ils(TA["cbs"]["3.5-4"]["a"]), ils(TA["r"]["3"]["v"]), ils(TA["r"]["4"]["v"]), len(TA["nb"]))),
 ("באיזו עיר הכי זול לשכור דירה?", "מבין %d הערים הגדולות שהלמ״ס מודדת, הזולה ביותר ב%s הייתה %s, עם ממוצע של %s לחודש לכל הגדלים. בקובץ של אתר הנדל״ן הממשלתי, שמגיע ל־%d ערים, יש ערים קטנות עם שכר דירה נמוך עוד יותר; הכול בטבלת הערים."
   % (NCBS, QL, CHEAP["n"], ils(CHEAP["cbs"]["total"]["a"]), NC)),
 ("מה ההבדל בין שכר דירה חציוני לשכר דירה ממוצע?", "חציון הוא הסכום שחצי מהחוזים מעליו וחצי מתחתיו, ולכן דירות יוקרה מעטות לא מושכות אותו למעלה. ממוצע מושפע מכל דירה. אתר הנדל״ן הממשלתי מפרסם חציון, הלמ״ס מפרסמת ממוצע עם טעות דגימה, ושני המקורות נמדדים במדגמים שונים."),
 ("איך יודעים אם שכר הדירה שמבקשים הוגן?", "משווים לחציון של אותו מספר חדרים באותה עיר, ואם אפשר באותה שכונה, ובודקים מה יש בדירה: בניין חדש, חניה, מעלית, ממ״ד, ריהוט וקומה מסבירים פער. המחשבון בראש העמוד עושה את ההשוואה ומראה גם את הערובה המותרת."),
 ("כמה ערבות מותר לבקש משוכר דירה?", "כשהערובה עולה לשוכר כסף, פיקדון, ערבות בנקאית או ערבות מחברה, הסכום הכולל מוגבל לנמוך מבין 3 חודשי שכירות ושליש משכר הדירה לכל התקופה. בחוזה לשנה ב־6,000 ₪ לחודש: עד 18,000 ₪."),
 ("אילו ערבויות לא נכללות בתקרה?", "התקרה חלה רק על ערובה שעולה לשוכר כסף. כתב ערבות של ערבים אישיים לא נספר בה. גם בין קרובי משפחה, בחוזה של עד 3 חודשים בלי אופציה, ובשכר דירה מעל התקרה, ההגבלה לא חלה."),
 ("תוך כמה זמן המשכיר חייב להחזיר את הערבות?", "עד 60 יום מהיום שהדירה הוחזרה לו, או מהיום שהשוכר שילם את חובותיו, המאוחר מביניהם, יחד עם הריבית או הרווח שהערובה צברה."),
 ("מי משלם דמי תיווך בשכירות?", "מי שהזמין את המתווך. החוק אוסר לגלגל על השוכר דמי תיווך של מתווך שפעל מטעם המשכיר. מתווך שהשוכר עצמו הזמין גובה ממנו לפי הזמנה בכתב."),
 ("תוך כמה זמן המשכיר חייב לתקן תקלה בדירה?", "ליקוי שלא מאפשר לגור בדירה באופן סביר: עד 3 ימים מהדרישה. ליקוי אחר שאינו קל ערך: עד 30 יום. ליקוי שנגרם משימוש לא סביר מתקן השוכר על חשבונו."),
 ("מתי צריך להודיע על הארכת חוזה שכירות?", "כשיש אופציה, המשכיר מודיע לפחות 90 יום לפני סוף התקופה והשוכר לפחות 60 יום. בלי אופציה, המשכיר מודיע זמן סביר מראש אם הוא רוצה להאריך ובאילו תנאים."),
 ("האם המשכיר יכול לבטל את החוזה באמצע?", "רק אם בחוזה יש סעיף ביטול שנותן את אותה זכות גם לשוכר. במקרה כזה המשכיר מודיע לפחות 90 יום מראש, והשוכר לפחות 60 יום. סעיף ביטול רק לטובת המשכיר בטל."),
 ("האם מותר להעלות שכר דירה באמצע החוזה?", "החוק לא קובע תקרה לשכר הדירה. שכר הדירה, מועדי התשלום וההצמדה הם מה שנכתב בחוזה. העלאה באמצע התקופה שלא נקבעה בחוזה היא שינוי של החוזה, ודורשת את הסכמת שני הצדדים."),
 ("מה זה דירה שאינה ראויה למגורים?", "דירה בלי ניקוז, חשמל או תאורה, אוורור ואור טבעי, דלת כניסה ננעלת, מי שתייה או מחיצה לשירותים, או דירה עם סיכון בלתי סביר לבטיחות ולבריאות. מסירת דירה כזאת היא הפרת חוזה."),
 ("על מי חל חוק שכירות הוגנת?", "על חוזה שכירות למגורים ליותר מ־3 חודשים (או עם אופציה) ועד 10 שנים. הוא לא חל על דירת נופש או מלון, מעונות, דיור מוגן, דירה בשכירות מוגנת, ושכר דירה מעל 20,000 ₪ לחודש לפי נוסח החוק, סכום שמתעדכן כל שנה לפי המדד."),
 ("האם שכר דירה פטור ממס?", "כן, עד תקרה. ב־%d שכר דירה למגורים עד %s בחודש, על סך כל הדירות, פטור ממס. בין %s ל־%s יש פטור חלקי, ומעל %s אין פטור." % (TAX["year"], ils(TAX["ceiling"]), ils(TAX["ceiling"]), ils(TAX["double"]), ils(TAX["double"]))),
 ("מהו גובה הפטור ממס על השכרת דירה בשנת 2026?", "%s לחודש, כמו ב־2024 וב־2025. ב־2023 התקרה הייתה %s וב־2022 %s." % (ils(TAX["ceiling"]), ils(5471), ils(5196))),
 ("איך משלמים מס הכנסה בגובה 10% על שכר דירה?", "פעם בשנה, עד 30 בינואר של השנה הבאה: על שכר הדירה של %d משלמים עד %s. מי שיש לו תיק במס הכנסה משלם באתר רשות המסים; מי שאין לו, בבנק הדואר עם השובר \"בקשה לתשלום מס על הכנסה מהשכרת דירה\" ממשרד פקיד השומה." % (TAX["year"], TAX["tenDue"])),
 ("איזה מסלול מס הכי משתלם למשכיר?", "עד %s בחודש מסלול הפטור לא עולה כסף. לפי החישוב שלנו, מתחת לגיל 60 מסלול 10%% זול ממסלול הפטור החל מכ־%s בחודש. מי שיש לו הוצאות גדולות, ריבית על משכנתא או פחת, בודק גם את המסלול הרגיל." % (ils(TAX["ceiling"]), ils(round(TEN_BE / 10) * 10))),
 ("אני משכיר את הדירה שלי ושוכר דירה אחרת. מה עם המס?", "בעל דירה יחידה שמשכיר אותה ושוכר דירה אחרת למגוריו רשאי, במסלול 10%%, להפחית את שכר הדירה שהוא משלם, עד %s בחודש, ולשלם 10%% רק על ההפרש." % ils(TAX["offsetCap"])),
 ("מה ההבדל בין מדד שכר הדירה למדד המחירים לצרכן?", "מדד שכר הדירה של הלמ״ס מודד רק את השינוי בשכר הדירה, והוא חלק ממדד המחירים לצרכן, שמודד סל רחב. רוב החוזים צמודים, אם בכלל, למדד המחירים לצרכן."),
 ("מה זה שכירות לטווח ארוך?", "דירה בבניין שנבנה להשכרה, לרוב בחוזה לכמה שנים עם עדכון מחיר שנקבע מראש. פרויקטים כאלה יוצאים במכרזים של החברה הממשלתית \"דירה להשכיר\" ושל יזמים פרטיים, והתנאים נקבעים בכל פרויקט."),
 ("מה זה דמי מפתח?", "תשלום בשכירות מוגנת לפי חוק הגנת הדייר. הדייר המוגן שילם דמי מפתח בכניסה, ובעזיבה הם מתחלקים לפי החוק. על דירה בשכירות מוגנת לא חל פרק השכירות ההוגנת."),
 ("איך מוצאים דירה להשכרה בלי תיווך?", "באתר מסומנות מודעות של בעלי דירות כ\"מבעלי הנכס\". גם כשמתווך מעורב, אם הוא פעל מטעם המשכיר, השוכר לא משלם לו."),
]
FAQH = '<h2>שאלות נפוצות</h2>\n' + "".join("<h3>%s</h3>\n<p>%s</p>\n" % (q, a) for q, a in FAQ)

ENR = sorted([c for c in CITIES if c.get("cbs") and c["cbs"].get("3.5-4")], key=lambda c: -c["cbs"]["3.5-4"]["a"])
ENSEC = ('<section class="nlrh-en" lang="en" dir="ltr">\n<h2>Apartments for rent in Israel: rents by city and the law, in English</h2>\n'
         '<p>The official numbers for renting in Israel. The Israeli government real-estate site publishes the <strong>median</strong> rent per city, by room count and by neighbourhood; the Central Bureau of Statistics (CBS) publishes the <strong>average</strong> rent for the %d largest cities with its sampling error. '
         'In %s the national median for a 4-room flat (3 bedrooms, as Israelis count the living room as a room) was %s a month; the CBS average for all sizes was %s, up %s on a year earlier (our calculation).</p>\n'
         % (NCBS, "April to June 2026", ils(N4).replace(" ₪", " NIS"), ils(CBS_T).replace(" ₪", " NIS"), sp(CBS_T / CBS_T_P - 1).replace("−", "-")))
ENSEC += '<div class="nlrh-t"><table><thead><tr><th>City</th><th>CBS average, 3.5 to 4 rooms (NIS)</th><th>Government median, 4 rooms (NIS)</th></tr></thead><tbody>\n'
for c in ENR:
    ENSEC += '<tr><th>%s</th><td class="n">%s</td><td class="n">%s</td></tr>\n' % (EN[c["n"]], num(c["cbs"]["3.5-4"]["a"]), num(c["r"]["4"]["v"]) if c["r"].get("4") else "")
ENSEC += ('</tbody></table></div>\n<p><strong>The fair-rental rules</strong> (Rental and Loan Law, chapter on residential leases, from 2017): a written lease; a deposit or bank guarantee of no more than 3 months\' rent or a third of the lease\'s total rent, whichever is lower, returned within 60 days; '
          'urgent repairs within 3 days, others within 30; 90 days\' notice from the landlord and 60 from the tenant on options and cancellation clauses; the tenant does not pay building insurance or the landlord\'s broker. '
          'The chapter covers leases of more than 3 months and up to 10 years, below a rent ceiling of 20,000 NIS a month in the law\'s text, updated each year by the consumer price index.</p>\n'
          '<p><strong>Tax for landlords</strong> (2026): residential rent up to %s NIS a month is tax-free (partly up to %s NIS); or a flat 10%% of the gross rent paid by %s; or the regular track with expenses and depreciation. '
          'The calculator above is in Hebrew; pick a city (עיר), rooms (חדרים) and the rent (שכר הדירה).</p>\n</section>\n' % (num(TAX["ceiling"]), num(TAX["double"]), "30 January 2027"))
SRCS_P = ('<h2>שיטה ומקורות</h2>\n<p class="nlrh-src">החציונים: <a href="https://www.nadlan.gov.il/" rel="nofollow noopener" target="_blank">אתר הנדל״ן הממשלתי</a>, קובצי השכירות לפי עיר (%s), שנקראו ב־25.10.2026. הממוצעים: '
          '<a href="%s" rel="nofollow noopener" target="_blank">הלמ״ס, שכר דירה ממוצע, לוח 4.9</a>, %s. המדד: <a href="%s" rel="nofollow noopener" target="_blank">מדד שכר הדירה של הלמ״ס</a> עד %s. '
          'החוק: <a href="%s" rel="nofollow noopener" target="_blank">חוק השכירות והשאילה, התשל״א־1971</a>, בנוסח העדכני ל־30.9.2026. המס: <a href="%s" rel="nofollow noopener" target="_blank">כל זכות, פטור ממס על השכרת דירה</a> '
          'ו<a href="%s" rel="nofollow noopener" target="_blank">מדריך המסלולים של רשות המסים</a>. כל מספר שחישבנו בעצמנו מסומן "החישוב שלנו". המודעות מתפרסמות בידי מתווכים ובעלי דירות; האתר מפרסם אותן ואינו מתווך. '
          'זה לא ייעוץ משפטי או ייעוץ מס. עודכן %s.</p>\n' % (SRC["gov"]["he"].split("לפי עיר, חדרים ושכונה, ")[-1], SRC["cbs49"]["url"], QL, SRC["cbsIdx"]["url"], mlab(IDX["last"]), SRC["law"]["url"], SRC["tax"]["url"], SRC["tax"]["url2"], UPDATED))

CSS = ('<style id="nlrh-css">.nlrh-lead{font-size:18px;line-height:1.75}.nlrh-cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px;margin-bottom:8px}'
       '.nlrh-cta a{display:inline-flex;align-items:center;min-height:48px;padding:10px 18px;border-radius:6px;border:1.5px solid #1F4B5C;color:#1F4B5C;font-weight:700;text-decoration:none;font-size:16px;line-height:1.3}'
       '.nlrh-cta a.is-primary{background:#1F4B5C;color:#fff}.nlrh-cta a:focus-visible{outline:3px solid #2F6F86;outline-offset:2px}'
       '.nlrh-t{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:0;margin-bottom:10px;max-width:100%}.nlrh-t table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;font-size:15px;line-height:1.5}'
       '.nlrh-t th,.nlrh-t td{padding:8px 10px;border-bottom:1px solid #D3DCE2;text-align:right;vertical-align:top}.nlrh-t thead th{background:#F6F8F9;color:#12202A;font-weight:700;font-size:14px}'
       '.nlrh-t tbody th{font-weight:600;color:#12202A;background:#fff;position:sticky;right:0;z-index:1}.nlrh-t td.n{white-space:nowrap;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:14px}'
       '.nlrh-t td small,.nlrh-t th small{display:block;font-size:12.5px;color:#5E6A75;font-family:inherit;font-weight:400}.nlrh-cap{font-weight:700;color:#12202A;font-size:15px;line-height:1.5;margin-top:22px;margin-bottom:8px}'
       '.nlrh-note,.nlrh-src{font-size:15px;line-height:1.7;color:#3E4C58}.nlrh-fig{margin:18px auto;max-width:560px}.nlrh-fig svg{width:100%;height:auto;display:block;border:1px solid #D3DCE2;border-radius:6px}'
       '.nlrh-fig figcaption{font-size:14px;line-height:1.6;color:#5E6A75;margin-top:6px}.nlrh-en{direction:ltr;text-align:left;border-top:1px solid #D3DCE2;margin-top:28px;padding-top:6px}.nlrh-en .nlrh-t th,.nlrh-en .nlrh-t td{text-align:left}'
       '.nlrh-en .nlrh-t tbody th{right:auto;left:0}@media (max-width:600px){.nlrh-cta{display:grid;grid-template-columns:1fr 1fr;gap:8px}.nlrh-cta a{justify-content:center;text-align:center;padding:10px 8px;font-size:15px}.nlrh-t table{font-size:14px}}</style>\n')

NEW = CSS + LEAD + CTA + TOOL + LIST + TODAY + CITY + ALLC + HOODS + TAS + TREND + LAWS + TAXS + CHECK + FAQH + ENSEC + SRCS_P

# ------------------------------------------------------------------ gates
def visible(html):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S); h = re.sub(r"<!--.*?-->", " ", h, flags=re.S); h = re.sub(r"\[nadlan_[a-z_]+[^\]]*\]", " ", h)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)) + " " + " ".join(re.findall(r'aria-label="([^"]*)"', html))
pv = visible(NEW)
assert not re.search(r"[–—]", pv), "long dash: " + str(re.findall(r".{20}[–—].{20}", pv)[:3])
BANNED = r"ממשק|מערכת|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה|טעון אימות|מודל|מנגנון|שכבה|שכבות|הדגמה|טכנולוגי|יחסית|אמור|אטלס|Atlas|פיילוט|פרוטוטייפ|רספונסיבי|מובייל|אפס |הסוכן שלכם|נתווך|אנחנו נמצא לכם"
hits = re.findall(r".{0,25}(?:%s).{0,25}" % BANNED, pv)
assert not hits, ("language law", hits[:5])
assert not re.search(r"(?<![\d.,])0 (₪|חדרים|חודשים|ערים|דירות|מודעות)", pv.replace("0 ₪</td>", "")), "a zero number on visible text"
assert "<h1" not in NEW, "the theme prints the only h1 from the title"
for sv in re.findall(r"<svg\b.*?</svg>", NEW, flags=re.S):
    assert min(float(x) for x in re.findall(r'font-size="([\d.]+)"', sv)) >= 12 and 'viewBox="0 0 420 ' in sv and 'direction="rtl"' in sv
fs = re.search(r"<h2[^>]*>\s*שאלות נפוצות[^<]{0,60}</h2>(.*?)(?=<h2|<section|$)", NEW, flags=re.S).group(1)
QS = [re.sub(r"<[^>]+>", "", q).strip() for q, a in re.findall(r"<h3[^>]*>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*)+)", fs, flags=re.S)]
assert len(QS) == len(FAQ) == 24 and len(set(QS)) == 24, (len(QS), len(set(QS)))
assert NEW.count('[nadlan_tool id="rentfair"]') == 1 and NEW.count("[nadlan_rent_listings") == 1
assert 0 < NEW.find('class="nlrh-lead"') < NEW.find('class="nlrh-cta"') < NEW.find('[nadlan_tool id="rentfair"]') < NEW.find("[nadlan_rent_listings") < NEW.find('class="nlrh-cap"'), "content-first order"
for p in re.findall(r"<p\b[^>]*>.*?</p>", LEAD + TODAY + CITY + ALLC + HOODS + TAS + TREND + TAXS + FAQH, flags=re.S):  # computed % in prose carry the label
    v = visible(p)
    if re.search(r"[+−]\d+(?:\.\d+)?%", v) and "nlrh-note" not in p: assert "החישוב שלנו" in v or "מדד" in v, ("computed percent without the label", v[:140])
# protected keywords: the bare head term leads only here; anchors carry no protected head term except to its owner
ANCH = re.findall(r'<a href="([^"#]+)">([^<]+)</a>', NEW)
for href, txt in ANCH:
    assert not re.search(r"דירות? להשכרה", txt), ("protected rent term in an anchor", href, txt)
words = len(re.findall(r"[\w֐-׿']+", pv)); tables = NEW.count("<table"); figs = NEW.count("<svg")
print("[G5] new page %s: %d visible words, %d tables, %d drawings, %d FAQ, %d internal links; gates OK" % (PATH, words, tables, figs, len(QS), len(ANCH)))

# ------------------------------------------------------------------ links (public GETs of our own pages, no redirect allowed)
class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
OP = urllib.request.build_opener(NoRedir); UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"}
def status(u):
    try:
        p = urllib.parse.urlsplit(u); u = urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(urllib.parse.unquote(p.path)), p.query, p.fragment))
        return OP.open(urllib.request.Request(u, headers=UA), timeout=60).status
    except urllib.error.HTTPError as e: return e.code
    except Exception as e: return str(e)[:40]
if not NOLINKS:
    for u in sorted(set(h for h, t in ANCH if h.startswith(SITE))):
        st = status(u); print("   link", st, u); assert st == 200, ("internal link not 200", u, st)

# ------------------------------------------------------------------ local outputs
SRCMD = """# /דירות-להשכרה/ (G5, new page): where every fact on the page comes from (internal, written by write_g5_page.py, %s)

| Fact on the page | Source |
|---|---|
| Median rent by city (72), rooms 3/4/5/all, 22 quarters to April to June 2026, the file's yearly change, 945 neighbourhood medians (all sizes, last year) | data.nadlan.gov.il settlement rent files, %s, read 25.10.2026 (U2 fetch, raw in _private-research/.../raw/u2/data/nadlan-gov); nadlan.gov.il labels them "מחיר חציוני" |
| Average rent with sampling error, 18 cities + 6 districts + Israel, groups 1-2 / 2.5-3 / 3.5-4 / 4.5+, Q2 2026 and Q2 2025 | CBS price bulletin, table 4.9 (research parse docs/research/2026-10-26-upgrades/u2-investment/data/cbs-rent-table-4-9-2026q2.json); the same figures ynet (8.9.2026) quotes: Israel 5,086 in Q2 |
| Rent index monthly and 12-month change to %s | CBS API series 120460 |
| Fair-rental chapter: sections 25א to 25טו, first and second schedules, the 5786 amendment of 25י | Nevo law00/5149 (current to 30.9.2026) and he.wikisource (edited 30.9.2026), raw in raw/g5/gov |
| Guarantee cap rules incl. personal guarantors not counted, relatives excluded | Kol Zchut "הגבלת סכום הערובה שמותר לדרוש משוכר דירה" (raw/g5/comp/c16.html) |
| Tax: ceiling 5,654 (2024 to 2026), 5,471 (2023), 5,196 (2022), partial up to 11,308, 10%% due 30.1, offset up to 7,500, 31%% / 10%% first bracket, payment at the post office voucher | Kol Zchut pages updated 22.2.2026 (raw/g5/gov/g05, g06); the Tax Authority guide (403 to scripts, its AI-overview summary matches) |
| "דירה להשכיר" is the government company for long-term rental tenders | renten.co.il (raw/g5/comp/c06.html) |
| Every computed number (yearly change from CBS Q2 2025, the tax table, the 10%% break-even %s, neighbourhood estimates) | this script, from rent.json, cross-checked by tools/instruments/test_rentfair.js |
""" % (UPDATED, SRC["gov"]["he"], mlab(IDX["last"]), ils(round(TEN_BE / 10) * 10))
io.open(os.path.join(H, "page-sources.md"), "w", encoding="utf-8").write(SRCMD)
SVGD = os.path.join(H, "svg"); os.makedirs(SVGD, exist_ok=True)
for name, sv in (("v1-cities", svg_cities()), ("v2-index", svg_index()), ("v3-lease", svg_lease())):
    io.open(os.path.join(SVGD, name + ".svg"), "w", encoding="utf-8").write(sv.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1))
io.open(os.path.join(H, "en-section.html"), "w", encoding="utf-8").write("<!-- G5 English section, part of the page content (lang=en dir=ltr), see dna.md 8.9 -->\n" + ENSEC)

if DRY:
    pv_dir = os.path.join(H, "preview"); os.makedirs(pv_dir, exist_ok=True)
    io.open(os.path.join(pv_dir, "g5-page-content.html"), "w", encoding="utf-8", newline="").write(NEW)
    AS = "../../../../../plugins/nadlan-config/assets/instruments/"
    snap = io.open(os.path.join(H, "preview", "listings-snapshot.html"), encoding="utf-8").read() if os.path.exists(os.path.join(H, "preview", "listings-snapshot.html")) else "<p>(listings snapshot missing)</p>"
    body = (NEW.replace('[nadlan_tool id="rentfair"]', '<section class="nli" dir="rtl" lang="he" aria-label="כמה שכר דירה הוגן לדירה הזאת"><div class="nli-host" data-nli="rentfair" data-nli-data="%sdata/rent.json?ver=local"><div class="nli__panel"><p class="nli__kicker">בדיקה · שכר דירה</p><h2 class="nli__title">כמה שכר דירה הוגן לדירה הזאת</h2></div></div></section>' % AS)
               .replace('[nadlan_rent_listings limit="12"]', snap))
    shell = ('<!doctype html>\n<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,">'
             '<title>/דירות-להשכרה/ · תצוגה מקומית</title>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;800;900&family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
             '<link rel="stylesheet" href="%score.css?ver=local"><style>html,body{margin:0;background:#fff;color:#12202A;font-family:Heebo,"IBM Plex Sans Hebrew",sans-serif}'
             '.entry-content{padding:0 16px}.entry-content>*{max-width:760px;margin-left:auto;margin-right:auto}p,li{font-size:17px;line-height:1.75}h1{font:800 30px/1.25 Heebo,sans-serif;margin:24px auto 12px}'
             'h2{font:800 26px/1.3 Heebo,sans-serif;margin:36px auto 12px}h3{font:700 20px/1.4 Heebo,sans-serif;margin:24px auto 8px}a{color:#1F4B5C}</style></head>'
             '<body><main><div class="entry-content"><header><h1>%s</h1></header>%s</div></main><script src="%score.js?ver=local" defer></script><script src="%stools/rentfair.js?ver=local" defer></script></body></html>'
             % (AS, TITLE, body, AS, AS))
    io.open(os.path.join(pv_dir, "g5-page-render.html"), "w", encoding="utf-8", newline="").write(shell)
    print("  --dry: wrote preview/g5-page-content.html, preview/g5-page-render.html, page-sources.md, en-section.html, svg/*.svg; nothing was posted")
    sys.exit(0)

# ------------------------------------------------------------------ live create (NOT run by the research session; Ben's yes first)
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "g5page"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, hv, _ = req("GET", "/wp-json/nadlan/v1/health"); print("live version", (hv or {}).get("version"))
s, ex, _ = req("GET", "/wp-json/wp/v2/pages?slug=%s&status=any&_fields=id,slug,status" % urllib.parse.quote(SLUG))
assert not ex, ("a page with this slug exists already", ex)
st0 = status(SITE + "/wp-content/plugins/nadlan-config/assets/instruments/tools/rentfair.js"); assert st0 == 200, ("ship rentfair.js first", st0)
s, made, _ = req("POST", "/wp-json/wp/v2/pages", {"title": TITLE, "slug": SLUG, "content": NEW, "status": "publish" if PUBLISH else "draft",
                                                  "meta": {"_yoast_wpseo_title": SEO_T, "_yoast_wpseo_metadesc": SEO_D}})
pid = made["id"]; bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-created-%s.json" % (pid, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8").write(json.dumps({"id": pid, "link": made.get("link"), "status": made.get("status")}, ensure_ascii=False))
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,title,meta,slug,status,link" % pid)[1]
ok = {"read-back content": back["content"]["raw"].strip() == NEW.strip(), "title": back["title"]["raw"] == TITLE, "yoast title": (back.get("meta") or {}).get("_yoast_wpseo_title") == SEO_T,
      "slug": urllib.parse.unquote(back["slug"]) == SLUG}
if PUBLISH:
    time.sleep(3)
    page = urllib.request.urlopen(urllib.request.Request(SITE + urllib.parse.quote(PATH) + "?x=%d" % time.time(), headers=UA), timeout=90).read().decode("utf-8", "replace")
    bd = page[page.find("<body"):]
    ok.update({"one h1": bd.count("<h1") == 1, "h1 text": TITLE in bd, "seo title": SEO_T in page, "tool mounted": 'data-nli="rentfair"' in bd, "listings rendered": "[nadlan_rent_listings" not in bd and "nlrh-list" in bd,
               "one FAQPage": page.count('"@type":"FAQPage"') == 1, "24 questions": page.count('"@type":"Question"') == 24, "index,follow": "noindex" not in page[:page.find("</head>")],
               "answer before the tool": 0 <= bd.find("nlrh-lead") < bd.find('data-nli="rentfair"')})
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
print("PAGE", back.get("link"), back.get("status"), "ALL OK" if all(ok.values()) else "CHECK FAILED: move page %d to draft and report" % pid)
