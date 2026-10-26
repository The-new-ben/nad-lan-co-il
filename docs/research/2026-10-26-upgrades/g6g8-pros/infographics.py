# -*- coding: utf-8 -*-
"""The 9 drawings of G6 G7 G8 (NadLan Instruments: white ground, ink #12202A, sea #2F6F86, deep #1F4B5C, line #D3DCE2, survey red
#C42550 only for a limit or a warning; IBM Plex Sans Hebrew + IBM Plex Mono; no cream, no gold, no gradient). Every number is computed
here from the built data files (bedek.json, shamai.json, orechdin.json, ptax.json), never typed in. viewBox 0 0 420 H, direction rtl,
text >= 12 px, an aria-label that says what the drawing shows.
  python infographics.py   writes svg/*.svg and preview/svg.html (all drawings on one page, for the 390 / 700 px look)"""
import io, os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from g6g8_common import BD, SH, OD, PT, num, ils, pct  # noqa: E402

FONT = "font-family:'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif"
MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"
INK, INK2, SEA, DEEP, RED, LINE, MUTE, GROUND = "#12202A", "#3E4C58", "#2F6F86", "#1F4B5C", "#C42550", "#D3DCE2", "#5E6A75", "#F6F8F9"


def tx(x, y, s, anchor="start", size=13, weight=400, fill=INK, mono=False, halo=False, ltr=False):
    """direction is rtl on the svg: anchor start = the right end of the text sits at x."""
    assert size >= 12, "svg text below 12px"
    st = "%s;font-size:%spx;font-weight:%s" % (MONO if mono else FONT, size, weight)
    if halo: st += ";paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-linejoin:round"
    return '<text x="%.1f" y="%.1f" text-anchor="%s"%s style="%s" fill="%s">%s</text>' % (x, y, anchor, ' direction="ltr"' if ltr else "", st, fill, s)


def svg_open(h, label):
    return '<svg viewBox="0 0 420 %d" direction="rtl" role="img" aria-label="%s" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">' % (h, label)


def rect(x, y, w, h, fill, extra=""): return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"%s/>' % (x, y, max(0, w), h, fill, extra)
def line(x1, y1, x2, y2, col=LINE, w=1, dash=""): return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (x1, y1, x2, y2, col, w, ' stroke-dasharray="%s"' % dash if dash else "")


def env(kind, rooms=None):
    """the envelope of the published prices of a kind (and rooms), as the tool computes it"""
    lo, hi = [], []
    for s in BD["prices"]:
        for r in s["rows"]:
            if r[0] != kind: continue
            if rooms is not None and r[4] and not any(r[4][0] <= k <= r[4][1] for k in rooms): continue
            lo.append(r[2]); hi.append(r[3])
    return min(lo), max(hi)


# ======================================================================================= G6
SHORT6 = {"frames": "חלונות, דלתות, אלומיניום", "tiling": "ריצוף וחיפוי פנים", "machines": "דודים ומכונות", "yard": "חצר, חניה ושבילים", "insulation": "בידוד תרמי",
          "piping": "צנרת, ביוב ומרזבים", "sealing": "איטום ורטיבות", "cracks": "סדקים מעל 1.5 מ״מ", "cladding": "חיפוי חוץ", "other": "כל ליקוי אחר"}


def g6_periods():
    """I1: the inspection period (deep) and the 3 warranty years after it (light) for every item of the law's schedule"""
    items = sorted(BD["law"]["items"], key=lambda x: (-x["y"], x["short"]))
    xr, xl, top, rh = 410, 24, 92, 30
    w_lab = 168; x0 = xr - w_lab; span = 10.0; sc = (x0 - xl) / span
    hgt = top + len(items) * rh + 64
    g = [svg_open(hgt, "תקופות הבדק לפי חוק המכר (דירות): מ־שנה לכל ליקוי שאינו ברשימה ועד 7 שנים לחיפוי חוץ, ועוד 3 שנות אחריות אחרי כל תקופה; ליקוי בשלד 20 שנה")]
    g.append(tx(xr, 24, "עד מתי הקבלן אחראי, לפי סוג הליקוי", size=16, weight=600))
    g.append(tx(xr, 46, "תקופת הבדק מיום המסירה (כהה), ועוד 3 שנות אחריות (בהיר)", size=13, fill=INK2))
    g.append(tx(xr, 66, "התוספת לחוק המכר (דירות), התשל״ג-1973", size=12, fill=MUTE))
    for yy in range(0, 11, 2):
        x = x0 - sc * yy
        g.append(line(x, top - 8, x, top + len(items) * rh - 4, LINE))
        g.append(tx(x, top - 12, str(yy), anchor="middle", size=12, mono=True, fill=MUTE))
    for i, it in enumerate(items):
        y = top + i * rh
        g.append(tx(xr, y + 15, SHORT6[it["id"]], size=12.5, weight=500))
        g.append(rect(x0 - sc * it["y"], y + 4, sc * it["y"], 16, DEEP))
        g.append(rect(x0 - sc * (it["y"] + 3), y + 4, sc * 3, 16, SEA, ' fill-opacity=".35"'))
        g.append(tx(x0 - sc * it["y"] + 4, y + 16.5, "%d" % it["y"], size=12, weight=600, fill="#fff", mono=True))
    yb = top + len(items) * rh
    g.append(tx(x0, yb + 14, "שנים מהמסירה", size=12, fill=MUTE))
    g.append(rect(xr - 10, yb + 28, 10, 10, RED)); g.append(tx(xr - 16, yb + 37, "ליקוי יסודי בשלד וביציבות: 20 שנה מהמסירה", size=12.5, weight=500))
    g.append(tx(xr, yb + 56, "ליקוי שאפשר היה לראות במסירה: הודעה לקבלן בתוך שנה", size=12, fill=INK2))
    return "".join(g) + "</svg>"


def g6_prices():
    """I2: the published price ranges by property type (the envelope of 2025-2026 sources, as the tool shows them)"""
    rows = [("דירה 2 עד 3 חדרים", env("apt", [2, 3])), ("דירה 4 עד 5 חדרים", env("apt", [4, 5])), ("דירה 6 חדרים ומעלה", env("apt", [6])),
            ("פנטהאוז או דופלקס", env("roof")), ("בית פרטי עד 200 מ״ר", env("house")), ("וילה או בית גדול", env("villa")), ("רטיבות ותרמוגרפיה בלבד", env("moist"))]
    court = env("court")
    xr, xl, top, rh = 410, 20, 84, 34
    w_lab = 150; x0 = xr - w_lab; vmax = 6500.0; sc = (x0 - xl) / vmax
    hgt = top + len(rows) * rh + 70
    g = [svg_open(hgt, "טווחי המחירים שפורסמו לבדק בית לפי סוג הנכס: דירה של 4 עד 5 חדרים %s עד %s שקלים, בית פרטי %s עד %s" % (num(rows[1][1][0]), num(rows[1][1][1]), num(rows[4][1][0]), num(rows[4][1][1])))]
    g.append(tx(xr, 24, "כמה עולה בדק בית: הטווחים שפורסמו", size=16, weight=600))
    g.append(tx(xr, 46, "הנמוך והגבוה מבין המחירים שפורסמו ב-2025 וב-2026, בשקלים", size=13, fill=INK2))
    g.append(tx(xr, 66, "מידרג כולל מע״מ; בדק מבנים והבודקים לא ציינו", size=12, fill=MUTE))
    for v in (2000, 4000, 6000):
        x = x0 - sc * v; g.append(line(x, top - 4, x, top + len(rows) * rh - 6, LINE)); g.append(tx(x, top - 8, num(v), anchor="middle", size=12, mono=True, fill=MUTE))
    for i, (lab, (lo, hi)) in enumerate(rows):
        y = top + i * rh
        g.append(tx(xr, y + 17, lab, size=13, weight=500))
        g.append(rect(x0 - sc * hi, y + 8, sc * (hi - lo), 14, DEEP if i < 3 else SEA))
        if sc * (hi - lo) > 96: g.append(tx(x0 - sc * lo - 5, y + 19.5, "%s-%s" % (num(lo), num(hi)), size=12, mono=True, fill="#fff", weight=600))
        else: g.append(tx(x0 - sc * hi - 5, y + 19.5, "%s-%s" % (num(lo), num(hi)), size=12, mono=True, halo=True))
    yb = top + len(rows) * rh
    g.append(tx(xr, yb + 20, "חוות דעת מומחה לבית משפט: %s עד %s ₪ (מקור אחד)" % (num(court[0]), num(court[1])), size=12.5, weight=500))
    g.append(tx(xr, yb + 40, "רכוש משותף: %s ₪ לדירה ועוד מע״מ, מינימום %s ₪ לבניין (מידרג)" % (num(BD["shared"]["per_apt"]), num(BD["shared"]["min"])), size=12, fill=INK2))
    g.append(tx(xr, yb + 58, "טווח שפורסם, לא הצעת מחיר.", size=12, fill=MUTE))
    return "".join(g) + "</svg>"


def g6_calendar():
    """I3: when to inspect a new apartment, from the protocol to the 7th year (book 45 days before each end: our suggestion)"""
    stops = [("לפני החתימה", "יד שנייה: בדיקה לפני חוזה, כשעוד יש כוח מיקוח", 0),
             ("יום המסירה", "פרוטוקול מסירה ובדק בית; מכאן רצות התקופות", 0),
             ("10.5 חודשים", "לפני סוף שנת הבדק: כל ליקוי שאינו ברשימה, חשמל, טיח, צבע", 1),
             ("22.5 חודשים", "לפני סוף שנתיים: חלונות, דלתות, אלומיניום, ריצוף וחיפוי פנים", 2),
             ("34.5 חודשים", "לפני סוף 3 שנים: דודים ומכונות, חצר וחניה, בידוד תרמי", 3),
             ("46.5 חודשים", "לפני סוף 4 שנים: צנרת, ביוב, איטום ורטיבות", 4),
             ("58.5 חודשים", "לפני סוף 5 שנים: סדקים מעל 1.5 מ״מ בקירות שאינם נושאים", 5),
             ("82.5 חודשים", "לפני סוף 7 שנים: חיפוי חוץ שמתנתק או מתפורר", 7)]
    top, gap = 84, 46; hgt = top + gap * len(stops) + 40
    g = [svg_open(hgt, "לוח הבדיקות בדירה חדשה: לפני החתימה, ביום המסירה, ולפני סוף כל תקופת בדק אחרי שנה, 2, 3, 4, 5 ו-7 שנים")]
    g.append(tx(410, 24, "מתי להזמין בדק בית בדירה חדשה", size=16, weight=600))
    g.append(tx(410, 46, "45 יום לפני סוף כל תקופת בדק (ההצעה שלנו), כדי שהדוח", size=13, fill=INK2))
    g.append(tx(410, 64, "והמכתב לקבלן יגיעו לפני התאריך", size=13, fill=INK2))
    xl = 392
    g.append(line(xl, top, xl, top + gap * (len(stops) - 1), LINE, 2))
    for i, (a, b, yrs) in enumerate(stops):
        y = top + gap * i; key = i in (1,)
        g.append('<circle cx="%d" cy="%d" r="9" fill="%s" stroke="%s" stroke-width="2"/>' % (xl, y, "#fff" if key else (DEEP if yrs else SEA), RED if key else (DEEP if yrs else SEA)))
        g.append(tx(374, y + 1, a, size=14, weight=600, fill=RED if key else INK)); g.append(tx(374, y + 19, b, size=12.5, fill=INK2))
    g.append(tx(410, hgt - 10, "אחרי כל תקופת בדק יש עוד 3 שנות אחריות; בהן נטל ההוכחה עליכם.", size=12, fill=MUTE))
    return "".join(g) + "</svg>"


# ======================================================================================= G7
def g7_purposes():
    """I1: which appraisal, who orders, who pays, what deadline (from shamai.json purposes)"""
    P = SH["purposes"]
    short_who = {"bank": "שמאי מרשימת הבנק", "buy": "שמאי שתבחרו", "sell": "שמאי שתבחרו", "levy": "שמאי שלכם, אחר כך שמאי מכריע", "s197": "שמאי שלכם", "court": "שמאי רשום בלבד", "renewal": "שמאי לבעלי הדירות", "rent": "שמאי שתבחרו"}
    short_pay = {"bank": "אתם, לפי תעריף הבנק", "buy": "אתם", "sell": "אתם", "levy": "אתם; המכריע: חצי-חצי", "s197": "אתם", "court": "לפי הסכם או פסק", "renewal": "היזם; שמאי הרשות בחינם", "rent": "אתם"}
    top, rh = 86, 50; hgt = top + len(P) * rh + 30
    g = [svg_open(hgt, "איזו שומה צריך, מי מזמין את השמאי, מי משלם ומה המועד: משכנתא, לפני חתימה, מכירה, היטל השבחה 45 ימים, תכנית שפגעה בשווי 3 שנים, בית משפט, התחדשות עירונית ושכירות")]
    g.append(tx(410, 24, "איזה שמאי, מי משלם ועד מתי", size=16, weight=600))
    g.append(tx(410, 46, "שמונה מטרות של שומה, לפי החוק והתקנות", size=13, fill=INK2))
    g.append(tx(410, 70, "מטרה", size=12, weight=600, fill=MUTE)); g.append(tx(250, 70, "מי מזמין · מי משלם", size=12, weight=600, fill=MUTE)); g.append(tx(64, 70, "מועד", size=12, weight=600, fill=MUTE))
    for i, p in enumerate(P):
        y = top + i * rh
        if i % 2 == 0: g.append(rect(10, y - 4, 400, rh - 4, GROUND))
        lab = {"bank": "משכנתא", "buy": "לפני חתימה", "sell": "מכירה", "levy": "היטל השבחה", "s197": "תכנית פגעה בשווי", "court": "ירושה, גירושין, פירוק", "renewal": "פינוי בינוי, תמ״א 38", "rent": "דמי שכירות"}[p["id"]]
        g.append(tx(404, y + 16, lab, size=13, weight=600))
        g.append(tx(250, y + 16, short_who[p["id"]], size=12.5)); g.append(tx(250, y + 34, short_pay[p["id"]], size=12, fill=INK2))
        d = p["deadline"]
        if d: g.append(rect(14, y + 4, 56, 22, RED)); g.append(tx(42, y + 20, "%s %s" % (d.get("days") or d.get("years"), "ימים" if d.get("days") else "שנים"), anchor="middle", size=12.5, weight=600, fill="#fff"))
        else: g.append(tx(42, y + 20, "אין", anchor="middle", size=12, fill=MUTE))
    return "".join(g) + "</svg>"


def g7_exams():
    """I2: the exams on the way to a licence: how many passed in 2025 (official exam file, pass mark 60)"""
    rows = [(e, y25[0], y25[1]) for e, y24, y25 in SH["exams"]["rows"] if y25[0] >= 50]
    rows.sort(key=lambda r: r[2] / r[1])
    short = {"מבוא לתורת השמאות": "מבוא לתורת השמאות", "דינים": "דינים", "יסודות הכלכלה חלק א - מיקרו כלכלה ומקרו כלכלה": "כלכלה: מיקרו ומאקרו",
             "יסודות הכלכלה חלק ב - כלכלה עירונית": "כלכלה עירונית", "יסודות בחשבונאות וניתוח דוחות כספיים": "חשבונאות", "יסודות המימון ושימושם בשומת המקרקעין": "מימון",
             "סטטיסטיקה": "סטטיסטיקה", "יסודות הנדסת בנין והנדסה אזרחית": "הנדסת בניין", "יסודות מדידה ומיפוי": "מדידה ומיפוי",
             "תכנון ובניה חלק א - יסודות התכנון העירוני": "תכנון ובנייה א", "תכנון ובניה חלק ב - דיני התכנון העירוני": "תכנון ובנייה ב: הדינים",
             "מיסוי מקרקעין ומסים אחרים": "מיסוי מקרקעין", "גישות ועקרונות בהערכת מקרקעין": "גישות בהערכת מקרקעין", "יישומים בשומת מקרקעין": "יישומים (הבחינה המסכמת)"}
    xr, top, rh = 410, 100, 27; x0 = 250; xl = 24; sc = (x0 - xl) / 100.0
    hgt = top + len(rows) * rh + 46
    fin = [r for r in rows if r[0] == SH["exams"]["final"]][0]
    g = [svg_open(hgt, "שיעור העוברים בבחינות שמאי המקרקעין ב-2025: מ-%s ב%s ועד %s ב%s; בבחינה המסכמת %s" % (pct(rows[0][2] / rows[0][1], 0), short[rows[0][0]], pct(rows[-1][2] / rows[-1][1], 0), short[rows[-1][0]], pct(fin[2] / fin[1], 0)))]
    g.append(tx(xr, 24, "הדרך לרישיון: כמה עברו כל בחינה ב-2025", size=16, weight=600))
    g.append(tx(xr, 46, "ציון 60 ומעלה, מתוך כל מי שנבחן (כולל נבחנים חוזרים)", size=13, fill=INK2))
    g.append(tx(xr, 66, "קובץ ציוני הבחינות של משרד המשפטים, data.gov.il", size=12, fill=MUTE))
    for v in (25, 50, 75, 100):
        x = x0 - sc * v; g.append(line(x, top - 4, x, top + len(rows) * rh - 4, LINE)); g.append(tx(x, top - 8, "%d%%" % v, anchor="middle", size=12, mono=True, fill=MUTE))
    for i, (e, nn, pp) in enumerate(rows):
        y = top + i * rh; r = pp / nn; is_fin = e == SH["exams"]["final"]
        g.append(tx(xr, y + 15, short[e], size=12.5, weight=600 if is_fin else 400, fill=RED if is_fin else INK))
        g.append(rect(x0 - sc * 100 * r, y + 5, sc * 100 * r, 13, RED if is_fin else (DEEP if r >= 0.6 else SEA)))
        if r > 0.5: g.append(tx(x0 - 4, y + 16, "%s מתוך %s" % (pct(r, 0), num(nn)), size=12, weight=600, fill="#fff"))
        else: g.append(tx(x0 - sc * 100 * r - 4, y + 16, "%s מתוך %s" % (pct(r, 0), num(nn)), size=12, halo=True))
    g.append(tx(xr, hgt - 12, "אחרי האחוז: מספר הנבחנים ב-2025.", size=12, fill=MUTE))
    return "".join(g) + "</svg>"


def g7_decisive():
    """I3: the decisive appraiser's fee by the amount in the request (the regulation's brackets), and the share of each side"""
    T = SH["decisive"]
    def fee(a):
        f = 0
        for lo, hi, r in T["table"]:
            hi = hi or 1e18
            if a > lo: f += (min(a, hi) - lo) * r
        return max(T["min"], min(T["max"], f))
    xr, xl, yb, yt = 396, 40, 250, 92; amax, fmax = 6000000.0, 60000.0
    X = lambda a: xr - (xr - xl) * a / amax
    Y = lambda f: yb - (yb - yt) * f / fmax
    pts = [(a, fee(a)) for a in range(0, int(amax) + 1, 50000)]
    g = [svg_open(320, "שכר שמאי מכריע לפי סכום ההשבחה שבבקשה: 15,000 שקלים על 500 אלף, 25,000 על מיליון, 35,000 על 2 מיליון, 50,000 על 5 מיליון, ועוד מע״מ; כל צד משלם מחצית")]
    g.append(tx(410, 24, "שכר שמאי מכריע לפי התקנות", size=16, weight=600))
    g.append(tx(410, 46, "לפי סכום ההשבחה או התביעה שבבקשה, לפני מע״מ", size=13, fill=INK2))
    g.append(tx(410, 66, "3% עד 500 אלף, 2% עד מיליון, 1% עד 2 מיליון, 0.5% מעל", size=12, fill=MUTE))
    for f in (20000, 40000, 60000):
        g.append(line(xl, Y(f), xr, Y(f), LINE)); g.append(tx(xr, Y(f) - 4, "%d אלף" % (f // 1000), size=12, fill=MUTE))
    g.append(line(xl, yb, xr, yb, INK, 1.2))
    for a in (0, 2000000, 4000000, 6000000):
        g.append(tx(X(a), yb + 18, "%s" % ("0" if a == 0 else "%d מ׳" % (a // 1000000)), anchor="middle", size=12, mono=True, fill=MUTE))
    g.append('<polyline fill="none" stroke="%s" stroke-width="2.6" points="%s"/>' % (DEEP, " ".join("%.1f,%.1f" % (X(a), Y(f)) for a, f in pts)))
    g.append('<polyline fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="5 4" points="%s"/>' % (SEA, " ".join("%.1f,%.1f" % (X(a), Y(f / 2)) for a, f in pts)))
    for a in (500000, 1000000, 2000000, 5000000):
        f = fee(a); g.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s"/>' % (X(a), Y(f), DEEP))
        g.append(tx(X(a), Y(f) - 10, num(f), anchor="middle", size=12, mono=True, weight=600, halo=True))
    g.append(line(xl, Y(T["min"]), xr, Y(T["min"]), RED, 1, "3 3"))
    g.append(tx(410, yb + 40, "הקו המלא: כל השכר. המקווקו: החלק של כל צד.", size=12, fill=INK2))
    g.append(tx(410, yb + 58, "מינימום %s ₪, תקרה %s ₪ למחלוקת, ועוד מע״מ." % (num(T["min"]), num(T["max"])), size=12, fill=MUTE))
    return "".join(g) + "</svg>"


# ======================================================================================= G8
def g8_cap():
    """I1: what a developer may charge the buyer for its lawyer, by the apartment price (2026)"""
    C = OD["cap"]
    xr, xl, yb, yt = 396, 34, 236, 96; pmax, fmax = 6000000.0, 8000.0
    X = lambda p: xr - (xr - xl) * p / pmax
    Y = lambda f: yb - (yb - yt) * f / fmax
    cross = C["fixed"] / C["pct"]
    g = [svg_open(344, "מה מותר לקבלן לגבות מהקונה על עורך הדין שלו ב-2026: 0.5%% מהמחיר עד %s שקלים, ואז %s שקלים קבועים, ועוד מע״מ; מעל %s שקלים אין תקרה" % (num(cross), num(C["fixed"]), num(C["ceiling"])))]
    g.append(tx(410, 24, "עורך הדין של הקבלן: כמה מותר לגבות מכם", size=16, weight=600))
    g.append(tx(410, 46, "התקרה ב-2026 לפי מחיר הדירה, לפני מע״מ", size=13, fill=INK2))
    g.append(tx(410, 66, "תקנות המכר (דירות) (הגבלת גובה ההוצאות המשפטיות)", size=12, fill=MUTE))
    for f in (2000, 4000, 6000):
        g.append(line(xl, Y(f), xr, Y(f), LINE)); g.append(tx(xr, Y(f) - 4, num(f), size=12, mono=True, fill=MUTE))
    g.append(line(xl, yb, xr, yb, INK, 1.2))
    for p in (1000000, 2000000, 3000000, 4000000, 5000000):
        g.append(tx(X(p), yb + 18, "%d מ׳" % (p // 1000000), anchor="middle", size=12, mono=True, fill=MUTE))
    g.append(rect(X(pmax), yt - 6, X(C["ceiling"]) - X(pmax), yb - yt + 6, RED, ' fill-opacity=".12"'))
    g.append(tx(X(C["ceiling"]) - 6, yt + 14, "אין תקרה", size=13, weight=600, fill=RED))
    pts = [(0, 0), (cross, C["fixed"]), (C["ceiling"], C["fixed"])]
    g.append('<polyline fill="none" stroke="%s" stroke-width="2.8" points="%s"/>' % (DEEP, " ".join("%.1f,%.1f" % (X(p), Y(f)) for p, f in pts)))
    g.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s"/>' % (X(cross), Y(C["fixed"]), DEEP))
    g.append(tx(X(cross), Y(C["fixed"]) - 12, "%s ₪" % num(C["fixed"]), anchor="middle", size=12, mono=True, weight=600, halo=True))
    g.append(line(X(C["ceiling"]), yt - 6, X(C["ceiling"]), yb, RED, 1.4, "4 3"))
    g.append(tx(X(C["ceiling"]), yb + 36, num(C["ceiling"]), anchor="middle", size=12, mono=True, fill=RED))
    g.append(tx(410, yb + 58, "0.5%% מהמחיר עד %s ₪, אחר כך %s ₪ קבוע." % (num(cross), num(C["fixed"])), size=12, fill=INK2))
    g.append(tx(410, yb + 94, "ועוד עד %s ₪ לניהול רשימת בעלי הזכויות." % num(C["list_fee"]), size=12, fill=MUTE))
    g.append(tx(410, yb + 76, "הסכום הקבוע מתעדכן לפי המדד בכל ינואר: %s ב-2024, %s ב-2025." % (num(C["hist"][0][1]), num(C["hist"][1][1])), size=12, fill=MUTE))
    return "".join(g) + "</svg>"


def tariff(v):
    T = OD["tariff"]
    if v > T["top"]: return T["top_min"]
    f = sum((min(v, hi) - lo) * r for lo, hi, r in T["tiers"] if v > lo)
    return max(T["min"], f)


def g8_fees():
    """I2: the published fee level (0.5% to 1%, minimum about 5,000) against the Bar's recommended minimum tariff for a contract"""
    xr, xl, yb, yt = 396, 40, 246, 96; pmin, pmax, fmax = 500000.0, 4000000.0, 45000.0
    X = lambda p: xr - (xr - xl) * (p - pmin) / (pmax - pmin)
    Y = lambda f: yb - (yb - yt) * f / fmax
    ps = [pmin + k * 25000 for k in range(int((pmax - pmin) / 25000) + 1)]
    lo = [max(p * 0.005, 5000) for p in ps]; hi = [max(p * 0.01, 6000) for p in ps]; tf = [tariff(p) for p in ps]
    g = [svg_open(340, "שכר טרחה לפי מחיר הדירה: מה שמשרדים פרסמו ב-2026, 0.5%% עד 1%%, מול התעריף המינימלי המומלץ של לשכת עורכי הדין לעריכת חוזה; בדירה של 2 מיליון: %s עד %s מול %s שקלים" % (num(max(1e4, 2e6 * .005)), num(2e6 * .01), num(tariff(2e6))))]
    g.append(tx(410, 24, "שכר טרחה: מה שמפורסם מול מה שהלשכה ממליצה", size=16, weight=600))
    g.append(tx(410, 46, "לפי מחיר הדירה, לפני מע״מ", size=13, fill=INK2))
    g.append(tx(410, 66, "המלצת הלשכה אינה מחייבת; ברוב הפרסומים: כ-0.5%", size=12, fill=MUTE))
    for f in (10000, 20000, 30000, 40000):
        g.append(line(xl, Y(f), xr, Y(f), LINE)); g.append(tx(xr, Y(f) - 4, "%d אלף" % (f // 1000), size=12, fill=MUTE))
    g.append(line(xl, yb, xr, yb, INK, 1.2))
    for p in (1000000, 2000000, 3000000, 4000000):
        g.append(tx(X(p), yb + 18, "%d מ׳" % (p // 1000000), anchor="middle", size=12, mono=True, fill=MUTE))
    band = " ".join("%.1f,%.1f" % (X(p), Y(f)) for p, f in zip(ps, hi)) + " " + " ".join("%.1f,%.1f" % (X(p), Y(f)) for p, f in reversed(list(zip(ps, lo))))
    g.append('<polygon points="%s" fill="%s" fill-opacity=".28"/>' % (band, SEA))
    g.append('<polyline fill="none" stroke="%s" stroke-width="2.4" points="%s"/>' % (SEA, " ".join("%.1f,%.1f" % (X(p), Y(f)) for p, f in zip(ps, lo))))
    g.append('<polyline fill="none" stroke="%s" stroke-width="2.6" points="%s"/>' % (DEEP, " ".join("%.1f,%.1f" % (X(p), Y(f)) for p, f in zip(ps, tf))))
    for p in (1000000, 2000000, 3000000):
        g.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (X(p), Y(tariff(p)), DEEP)); g.append(tx(X(p), Y(tariff(p)) - 10, num(tariff(p)), anchor="middle", size=12, mono=True, weight=600, halo=True))
    g.append(tx(410, yb + 40, "הקו הכהה: התעריף המומלץ של הלשכה לעריכת חוזה.", size=12, fill=INK2))
    g.append(tx(410, yb + 58, "הרצועה: 0.5% עד 1% שמשרדים פרסמו.", size=12, fill=INK2))
    g.append(tx(410, yb + 76, "מינימום שפורסם כ-5,000 ₪. סכומי 2026.", size=12, fill=MUTE))
    return "".join(g) + "</svg>"


def g8_steps():
    """I3: the steps of a second-hand purchase with the dates the law fixes (declaration 30 days, purchase tax 60 days)"""
    P = PT["pay"]
    stops = [("לפני הצעת מחיר", "נסח טאבו, תיק הבית המשותף, היתר וטופס 4, חובות", "check"),
             ("זיכרון דברים", "לא חותמים בלי עורך דין משלכם", "warn"),
             ("יום החתימה", "חוזה, ייפויי כוח, תשלום ראשון בנאמנות", "key"),
             ("מיד אחרי החתימה", "הערת אזהרה בטאבו: %s ₪" % num(dict((r[0], r[2]) for r in OD["land"])["warn"]), "step"),
             ("%d יום" % P["declare_days"], "הצהרה לרשות המסים", "law"),
             ("%d יום" % P["pay_days"], "תשלום מס הרכישה; איחור: 0.2% לשבוע", "law"),
             ("אחרי 40% מהמחיר", "מקדמה על מס שבח: 7.5% (15% בנכס מלפני 7.11.2001)", "law"),
             ("המסירה", "פרוטוקול, מונים, אישור היעדר חובות לוועד", "step"),
             ("הרישום", "אישור עירייה, אישורי מסים, שטר מכר: %s ₪" % num(dict((r[0], r[2]) for r in OD["land"])["sale"]), "step")]
    top, gap = 84, 44; hgt = top + gap * len(stops) + 30
    g = [svg_open(hgt, "צעדי קניית דירה יד שנייה: בדיקות, זיכרון דברים, חתימה, הערת אזהרה, הצהרה בתוך 30 יום, מס רכישה בתוך 60 יום, מקדמה על מס שבח, מסירה ורישום")]
    g.append(tx(410, 24, "קונים יד שנייה: הצעדים והמועדים בחוק", size=16, weight=600))
    g.append(tx(410, 46, "הימים נספרים מיום החתימה (חוק מיסוי מקרקעין)", size=13, fill=INK2))
    g.append(tx(410, 64, "האדום: מועד שהחוק קובע", size=12, fill=MUTE))
    xl = 392
    g.append(line(xl, top, xl, top + gap * (len(stops) - 1), LINE, 2))
    for i, (a, b, k) in enumerate(stops):
        y = top + gap * i
        col = RED if k == "law" else (DEEP if k == "key" else SEA)
        g.append('<circle cx="%d" cy="%d" r="9" fill="%s" stroke="%s" stroke-width="2"/>' % (xl, y, "#fff" if k in ("warn", "law") else col, RED if k == "warn" else col))
        g.append(tx(374, y + 1, a, size=14, weight=600, fill=col if k == "law" else INK)); g.append(tx(374, y + 19, b, size=12.5, fill=INK2))
    return "".join(g) + "</svg>"


ALL = {"g6-1-periods": g6_periods, "g6-2-prices": g6_prices, "g6-3-calendar": g6_calendar, "g7-1-purposes": g7_purposes, "g7-2-exams": g7_exams,
       "g7-3-decisive": g7_decisive, "g8-1-cap": g8_cap, "g8-2-fees": g8_fees, "g8-3-steps": g8_steps}

if __name__ == "__main__":
    os.makedirs(os.path.join(H, "svg"), exist_ok=True); os.makedirs(os.path.join(H, "preview"), exist_ok=True)
    out = []
    for k, f in ALL.items():
        s = f(); io.open(os.path.join(H, "svg", k + ".svg"), "w", encoding="utf-8", newline="\n").write(s); out.append((k, s)); print(k, len(s))
    page = ('<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G6 G7 G8 · הציורים</title>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
            '<style>body{margin:0;padding:16px;background:#fff;font-family:"IBM Plex Sans Hebrew",sans-serif;color:#12202A}h2{font-size:15px;margin:28px 0 6px;color:#3E4C58}</style></head><body>'
            + "".join("<h2>%s</h2>%s" % (k, s) for k, s in out) + "</body></html>")
    io.open(os.path.join(H, "preview", "svg.html"), "w", encoding="utf-8", newline="\n").write(page)
