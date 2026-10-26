# -*- coding: utf-8 -*-
"""G2 + G3 page infographics (NadLan Instruments identity: ink #12202A, sea #2F6F86, deep #1F4B5C, line #D3DCE2, survey red #C42550
only for a gap; IBM Plex Sans Hebrew + IBM Plex Mono). Every figure is drawn from the data files of the tools, never typed by hand:
  plugins/nadlan-config/assets/instruments/data/pinui.json, urcity.json, renewal-track.json.
Why not the default AI look: a planning sheet, not a card: hairline grid, one ink, one sea, red only where something is missing;
no cream, no brass, no gradient, no emoji.
  python infographics.py   writes ./svg/*.svg (the page writers import the functions)"""
import io, json, math, os

H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
DATA = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")
P = json.load(io.open(os.path.join(DATA, "pinui.json"), encoding="utf-8"))
U = json.load(io.open(os.path.join(DATA, "urcity.json"), encoding="utf-8"))
T = json.load(io.open(os.path.join(DATA, "renewal-track.json"), encoding="utf-8"))
FONT = "font-family:'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif"
MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"
INK, INK2, MUTE, SEA, DEEP, RED, LINE, GROUND = "#12202A", "#3E4C58", "#5E6A75", "#2F6F86", "#1F4B5C", "#C42550", "#D3DCE2", "#EDF1F4"


def num(n): return "{:,}".format(int(round(n)))


def tx(x, y, s, anchor="start", size=13, weight=400, fill=INK, mono=False):
    """direction is rtl on the svg: anchor start = the right end of the text sits at x."""
    assert size >= 12, "svg text below 12px"
    return '<text x="%.1f" y="%.1f" text-anchor="%s" style="%s;font-size:%spx;font-weight:%s" fill="%s">%s</text>' % (x, y, anchor, MONO if mono else FONT, size, weight, fill, s)


def svg_open(h, label):
    return ('<svg viewBox="0 0 420 %d" direction="rtl" role="img" aria-label="%s" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">'
            '<defs><pattern id="g%d" width="14" height="14" patternUnits="userSpaceOnUse"><path d="M14 0H0V14" fill="none" stroke="%s" stroke-width=".5"/></pattern></defs>'
            '<rect width="420" height="%d" fill="url(#g%d)" opacity=".45"/>' % (h, label, h, LINE, h, h))


# ------------------------------------------------------------------ G2
def g2_majority():
    """Three buildings of the page example (24/17, 16/9, 8/6): each apartment a cell, signed filled; the three-fifths line per building;
    the cluster line at two thirds. Shows the trap: two thirds of the cluster and still one building short."""
    rows = [(24, 17), (16, 9), (8, 6)]; L = P["law"]
    h = 330; o = [svg_open(h, "שלושה בניינים: 17 מתוך 24, 9 מתוך 16, 6 מתוך 8. במקבץ 32 מתוך 48, שני שלישים; בבניין השני חסרה חתימה אחת לשלוש חמישיות")]
    o.append(tx(410, 26, "שני שלישים במקבץ, ועדיין חסרה חתימה", size=17, weight=700))
    o.append(tx(410, 46, "כל ריבוע דירה; מלא: חתמו. הקו האדום: שלוש חמישיות בבניין", size=13, fill=INK2))
    y = 70; cw = 13; gap = 3
    for i, (u, s) in enumerate(rows):
        need = math.ceil(u * 3 / 5 - 1e-9); per_row = 8; nrow = math.ceil(u / per_row)
        o.append(tx(410, y + 12, "בניין %d" % (i + 1), size=14, weight=600))
        o.append(tx(410, y + 30, "%d מתוך %d" % (s, u), size=13, fill=INK2, mono=True))
        for k in range(u):
            r, c = divmod(k, per_row); x = 320 - c * (cw + gap); yy = y + r * (cw + gap)
            fill = DEEP if k < s else "#fff"; stroke = DEEP if k < s else MUTE
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="1"/>' % (x, yy, cw, cw, fill, stroke))
        r, c = divmod(need, per_row)
        xn = 320 - c * (cw + gap) + cw + gap / 2 if c else 320 + cw + gap / 2 - per_row * (cw + gap)
        ok = s >= need
        o.append(tx(150, y + 12, ("צריך %d ✓" % need) if ok else ("צריך %d, חסרה %d" % (need, need - s)), size=13, weight=600, fill=INK if ok else RED))
        if not ok:
            r0, c0 = divmod(s, per_row); xx = 320 - c0 * (cw + gap); yy = y + r0 * (cw + gap)
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="3 2"/>' % (xx - 2, yy - 2, cw + 4, cw + 4, RED))
        y += max(nrow, 2) * (cw + gap) + 26
    N = sum(u for u, s in rows); S = sum(s for u, s in rows); cn = math.ceil(N * 2 / 3 - 1e-9)
    o.append('<line x1="20" y1="%d" x2="400" y2="%d" stroke="%s"/>' % (y - 6, y - 6, LINE))
    o.append(tx(410, y + 14, "כל המקבץ: %d מתוך %d, צריך %d (שני שלישים) ✓" % (S, N, cn), size=14, weight=600))
    o.append(tx(410, y + 34, "סעיף 1 לחוק: 2/3 במקבץ, 3/5 בכל בניין, וגם הרכוש המשותף", size=12, fill=MUTE))
    o[0] = o[0].replace('viewBox="0 0 420 %d"' % h, 'viewBox="0 0 420 %d"' % (y + 46)).replace('height="%d" fill="url' % h, 'height="%d" fill="url' % (y + 46))
    return "".join(o) + "</svg>"


def g2_clock():
    """Section 1ד from the first signed deal, then the authority's average from approval to a first permit (dashed: an average)."""
    c = P["law"]["clock"]; avg = P["series"]["approval_to_permit"][-1]
    XR, XL, y0 = 380, 30, 124; span = 60
    X = lambda m: XR - (XR - XL) * m / span
    H = y0 + 168
    o = [svg_open(H, "השעון של סעיף 1ד: בתוך שנתיים חצי מבעלי הדירות; בתוך 4 שנים שלוש חמישיות; בתוך 4.5 שנים הגשת תכנית; שנה נוספת במתחם של 120 יחידות. אחרי אישור התכנית 4.0 שנים בממוצע עד היתר ראשון")]
    o.append(tx(410, 26, "השעון שהחוק נותן ליזם", size=17, weight=700))
    o.append(tx(410, 46, "מהעסקה הראשונה שנחתמה בבניין", size=13, fill=INK2))
    o.append(tx(410, 64, "לא עמד בו? רוב באסיפה כללית יכול לאפשר ביטול", size=13, fill=INK2))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (XL, y0, XR, y0, INK))
    for yr in range(0, 6):
        o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s"/>' % (X(yr * 12), y0 - 4, X(yr * 12), y0 + 4, INK))
        o.append(tx(X(yr * 12), y0 + 20, "%d" % yr, anchor="middle", size=12, fill=MUTE, mono=True))
    # labels: the first deal and 24 months above; 48 months above-left; 54 months below (the two are 6 months apart)
    o.append('<circle cx="%.1f" cy="%d" r="7" fill="#fff" stroke="%s" stroke-width="2"/>' % (X(0), y0, DEEP))
    o.append(tx(410, y0 - 22, "העסקה הראשונה", size=13, weight=600))
    for m, lab, up in ((c["half_months"], "חצי מבעלי הדירות", True), (c["three_fifths_months"], "שלוש חמישיות", True), (c["plan_months"], "הגשת תכנית", False)):
        x = X(m)
        o.append('<circle cx="%.1f" cy="%d" r="7" fill="%s" stroke="#fff" stroke-width="2"/>' % (x, y0, DEEP))
        if up:
            o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s"/>' % (x, y0 - 10, x, y0 - 16, DEEP))
            o.append(tx(x, y0 - 22, lab, anchor="middle", size=13, weight=600))
            o.append(tx(x, y0 - 38, "%d חודשים" % m, anchor="middle", size=12, fill=INK2))
        else:
            o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s"/>' % (x, y0 + 10, x, y0 + 28, DEEP))
            o.append(tx(x, y0 + 42, lab, anchor="middle", size=13, weight=600))
            o.append(tx(x, y0 + 58, "%d חודשים" % m, anchor="middle", size=12, fill=INK2))
    o.append(tx(410, y0 + 42, "שנים מהעסקה הראשונה", size=12, fill=MUTE))
    o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="3" stroke-dasharray="5 4"/>' % (X(c["plan_months"]), y0 + 74, X(c["plan_months"] + 12) if c["plan_months"] + 12 <= span else XL, y0 + 74, SEA))
    o.append(tx(410, y0 + 79, "120 יחידות ומעלה: שנה נוספת לכל מועד", size=12, fill=SEA))
    o.append('<line x1="20" y1="%d" x2="400" y2="%d" stroke="%s"/>' % (y0 + 96, y0 + 96, LINE))
    o.append(tx(410, y0 + 118, "אחרי אישור התכנית: %.1f שנים בממוצע עד היתר" % avg[1], size=14, weight=600))
    o.append(tx(410, y0 + 138, "ממוצע של %d מתחמים שקיבלו היתר ב-%d, לא תחזית" % (avg[2], avg[0]), size=12, fill=MUTE))
    o.append(tx(410, y0 + 156, "סעיף 1ד לחוק פינוי ובינוי; דוח הרשות לשנת 2025", size=12, fill=MUTE))
    return "".join(o) + "</svg>"


def g2_permit_years():
    """R25 p.87: average years from plan approval to the first permit, by permit year (bars), with the number of complexes."""
    s = P["series"]["approval_to_permit"]; h = 70 + len(s) * 26 + 40
    o = [svg_open(h, "שנים מאישור תכנית פינוי בינוי עד היתר ראשון, לפי שנת ההיתר: " + ", ".join("%d %.1f" % (y, v) for y, v, n in s))]
    o.append(tx(410, 26, "מאישור התכנית עד היתר ראשון", size=17, weight=700))
    o.append(tx(410, 46, "שנים בממוצע, לפי השנה שבה ניתן ההיתר (בסוגריים: מתחמים)", size=13, fill=INK2))
    XR, W, y = 330, 250, 70; mx = 6.5
    for yr, v, n in s:
        w = W * v / mx
        o.append(tx(410, y + 5, "%d" % yr, size=13, mono=True))
        o.append('<rect x="%.1f" y="%d" width="%.1f" height="16" fill="%s"/>' % (XR - w, y - 8, w, DEEP if yr >= 2024 else SEA))
        o.append(tx(XR - w - 6, y + 5, "%.1f (%d)" % (v, n), size=13, mono=True))
        y += 26
    o.append(tx(410, y + 14, "דוח הרשות הממשלתית להתחדשות עירונית לשנת 2025, עמוד 87", size=12, fill=MUTE))
    return "".join(o) + "</svg>"


def g2_plans():
    """R25 p.25: pinui binui plans approved per year and the units in them (bars = units)."""
    s = P["series"]["plans"]; h = 82 + len(s) * 22 + 36
    o = [svg_open(h, "תכניות פינוי בינוי שאושרו בכל שנה ומספר הדירות בהן: " + ", ".join("%d %d תכניות %d דירות" % (y, n, u) for y, n, u in s))]
    o.append(tx(410, 26, "תכניות פינוי בינוי שאושרו, לפי שנה", size=17, weight=700))
    o.append(tx(410, 46, "הפס והמספר שבסופו: דירות בתכניות שאושרו", size=13, fill=INK2))
    XR, W, y = 318, 240, 70; mx = max(u for _, _, u in s)
    o.append(tx(410, 62, "שנה", size=12, fill=MUTE)); o.append(tx(362, 62, "תכניות", anchor="middle", size=12, fill=MUTE))
    y = 82
    for yr, n, u in s:
        w = max(2, W * u / mx)
        o.append(tx(410, y + 5, "%d" % yr, size=12, mono=True))
        o.append(tx(362, y + 5, "%d" % n, anchor="middle", size=12, fill=INK2, mono=True))
        o.append('<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s"/>' % (XR - w, y - 7, w, DEEP if yr == 2025 else SEA))
        o.append(tx(XR - w - 6, y + 5, num(u), size=12, mono=True))
        y += 22
    o.append(tx(410, y + 14, "דוח הרשות לשנת 2025, עמוד 25", size=12, fill=MUTE))
    return "".join(o) + "</svg>"


# ------------------------------------------------------------------ G3
def g3_tracks():
    """The three tracks as three columns of a planning sheet: what is built, who approves, the majority, the threshold, the tax ceiling."""
    rows = [("מה בונים", ["הריסה של כמה בניינים", "חיזוק ותוספת, או הריסה", "בעיקר הריסה ובנייה"]),
            ("מי מאשר", ["תכנית בוועדה המחוזית", "היתר בוועדה המקומית", "תכנית בוועדה המקומית"]),
            ("הרוב בחוק", ["2/3 במקבץ, 3/5 בבניין", "2/3 דירות ורכוש", "2/3 דירות ורכוש"]),
            ("הסף", ["24 יחידות קיימות", "היתר לפני 1980", "4 דירות לפחות"]),
            ("תקרת פטור ממס", ["120 מ\"ר או 50% יותר", "25 מ\"ר נוספים", "כמו בתמ\"א 38"])]
    cols = [(410, "פינוי בינוי", "מתחם"), (272, "תמ\"א 38", "בניין"), (134, "רישוי מהיר", "בניין")]
    y = 52; top = y + 112; hgt = top + len(rows) * 44 + 8
    o = [svg_open(hgt + 34, "שלושת המסלולים: פינוי בינוי במתחם, תמ\"א 38 לבניין, תכנית לרישוי מהיר; מה בונים, מי מאשר, הרוב בחוק, הסף ותקרת הפטור ממס")]
    o.append(tx(410, 26, "שלושה מסלולים, שלוש דרכים לאשר", size=17, weight=700))
    for x, name, kind in cols:
        o.append('<rect x="%d" y="%d" width="128" height="%d" fill="#fff" stroke="%s"/>' % (x - 128, y, hgt - y, LINE))
        o.append('<rect x="%d" y="%d" width="128" height="44" fill="%s"/>' % (x - 128, y, DEEP if kind == "מתחם" else SEA))
        o.append(tx(x - 8, y + 20, name, size=14, weight=700, fill="#fff"))
        o.append(tx(x - 8, y + 37, kind, size=12, fill="#fff"))
        bx = x - 118; by = y + 56
        blocks = [(0, 30), (34, 44), (68, 24)] if kind == "מתחם" else [(40, 44)]
        for dx, hh in blocks:
            o.append('<rect x="%d" y="%d" width="28" height="%d" fill="none" stroke="%s" stroke-width="1.5"/>' % (bx + dx, by + 46 - hh, hh, INK))
            for fy in range(by + 46 - hh + 6, by + 46, 8):
                o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (bx + dx + 5, fy, bx + dx + 23, fy, LINE))
    y2 = top
    for lab, vals in rows:
        o.append(tx(210, y2 + 12, lab, anchor="middle", size=12, fill=MUTE))
        for (x, _, _), v in zip(cols, vals):
            o.append(tx(x - 8, y2 + 30, v, size=12, fill=INK))
        o.append('<line x1="6" y1="%d" x2="410" y2="%d" stroke="%s" stroke-dasharray="2 3"/>' % (y2 + 40, y2 + 40, LINE))
        y2 += 44
    o.append(tx(410, hgt + 22, "נספח א לדוח הרשות לשנת 2025; הרוב לפי חוק פינוי ובינוי וחוק החיזוק", size=12, fill=MUTE))
    return "".join(o) + "</svg>"


def g3_taxdecl():
    """R25 p.70: complexes declared in the tax track per year, bars of units."""
    s = P["series"]["taxdecl"]
    h = 82 + len(s) * 24 + 36
    o = [svg_open(h, "מתחמים שהוכרזו במסלול המיסוי בכל שנה: " + ", ".join("%d %d מתחמים %d דירות" % (y, n, u) for y, n, u in s))]
    o.append(tx(410, 26, "הכרזות במסלול המיסוי, לפי שנה", size=17, weight=700))
    o.append(tx(410, 46, "הפס והמספר שבסופו: דירות מוצעות במתחמים", size=13, fill=INK2))
    XR, W = 318, 240; mx = max(u for _, _, u in s)
    o.append(tx(410, 62, "שנה", size=12, fill=MUTE)); o.append(tx(362, 62, "מתחמים", anchor="middle", size=12, fill=MUTE))
    y = 82
    for yr, n, u in s:
        w = max(2, W * u / mx)
        o.append(tx(410, y + 5, "%d" % yr, size=12, mono=True))
        o.append(tx(362, y + 5, "%d" % n, anchor="middle", size=12, fill=INK2, mono=True))
        o.append('<rect x="%.1f" y="%d" width="%.1f" height="15" fill="%s"/>' % (XR - w, y - 8, w, DEEP if yr >= 2024 else SEA))
        o.append(tx(XR - w - 6, y + 5, num(u), size=12, mono=True))
        y += 24
    o.append(tx(410, y + 14, "דוח הרשות לשנת 2025, עמוד 70", size=12, fill=MUTE))
    return "".join(o) + "</svg>"


def g3_permit_split():
    """R25 p.34: building-renewal permits, demolition and rebuild vs strengthening, 2013-2025 (stacked to 100%)."""
    s = U["permit_split"]; h = 70 + len(s) * 22 + 50
    o = [svg_open(h, "היתרים בהתחדשות בניינית לפי מסלול: " + ", ".join("%d הריסה %d%% חיזוק %d%%" % (y, a, b) for y, a, b in s))]
    o.append(tx(410, 26, "היתרים בהתחדשות בניינית: הריסה מול חיזוק", size=17, weight=700))
    o.append(tx(410, 46, "כהה: הריסה ובנייה מחדש. בהיר: חיזוק ועיבוי", size=13, fill=INK2))
    XR, W, y = 360, 300, 70
    for yr, a, b in s:
        wa = W * a / 100
        o.append(tx(410, y + 5, "%d" % yr, size=12, mono=True))
        o.append('<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s"/>' % (XR - wa, y - 7, wa, DEEP))
        o.append('<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s"/>' % (XR - W, y - 7, W - wa, "#A9C3CF"))
        o.append(tx(XR - 4, y + 5, "%d%%" % a, size=12, fill="#fff", mono=True))
        o.append(tx(XR - W + 4, y + 5, "%d%%" % b, anchor="end", size=12, fill=INK, mono=True))
        y += 22
    o.append(tx(410, y + 14, "דוח הרשות לשנת 2025, עמוד 34", size=12, fill=MUTE))
    return "".join(o) + "</svg>"


ALL = {"g2-majority": g2_majority, "g2-clock": g2_clock, "g2-permit-years": g2_permit_years, "g2-plans": g2_plans,
       "g3-tracks": g3_tracks, "g3-taxdecl": g3_taxdecl, "g3-permit-split": g3_permit_split}

if __name__ == "__main__":
    out = os.path.join(H, "svg"); os.makedirs(out, exist_ok=True)
    for k, f in ALL.items():
        s = f(); io.open(os.path.join(out, k + ".svg"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="utf-8"?>\n' + s.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1))
        print(k, len(s), "bytes")
