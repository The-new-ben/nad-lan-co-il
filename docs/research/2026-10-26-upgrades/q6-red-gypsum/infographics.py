# -*- coding: utf-8 -*-
"""The two infographics of /glossary/לוח-גבס-אדום/ (Q6 stage 2), as inline SVG for the page and the design board.
Drawn like a fire-safety plan sheet (owner design law 13.10.2026: from the subject's own world): white paper, black line work,
fire-rated board in red hatch (#C42550, the site red), mineral wool in the grey wave drafters use, IBM Plex Sans Hebrew for words and
IBM Plex Mono for minutes, thicknesses and standard numbers. Not the default look: no cream, no gold, no dark hero, no cards.
Every number is from dna.md section 6 (Rotenberg tested partitions 11.5.2025; Tambour catalogue 27.7.2026); the wall thickness is
a calculation (4 x 12.5 + 70 = 120 mm), labelled. In the SVG, direction is rtl: text-anchor start = the right end of a label."""

FONT = "font-family:'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif"
MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"
RED, INK, INK2, LINE = "#C42550", "#12202A", "#3E4C58", "#D3DCE2"

DEFS = ('<defs>'
        '<pattern id="q6fr" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#FBEAEF"/><line x1="0" y1="0" x2="0" y2="8" stroke="%s" stroke-width="1.3"/></pattern>'
        '<pattern id="q6fd" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" fill="#F6D9E1"/><line x1="0" y1="0" x2="0" y2="5" stroke="%s" stroke-width="1.6"/></pattern>'
        '<pattern id="q6fm" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#DCEEDF"/><line x1="0" y1="0" x2="0" y2="8" stroke="%s" stroke-width="1.3"/></pattern>'
        '<pattern id="q6wool" width="14" height="10" patternUnits="userSpaceOnUse"><path d="M0 5 Q3.5 0 7 5 T14 5" fill="none" stroke="#8A97A2" stroke-width="1.1"/></pattern>'
        '</defs>') % (RED, RED, RED)


def t(x, y, s, cls="", anchor="start", size=13, weight=400, fill=INK, mono=False):
    return '<text x="%s" y="%s" text-anchor="%s" style="%s;font-size:%spx;font-weight:%s" fill="%s">%s</text>' % (x, y, anchor, MONO if mono else FONT, size, weight, fill, s)


def partition_svg():
    """The tested 120-minute partition, a plan cut: 2 pink boards, 70 mm steel studs with 5 cm wool, 2 pink boards."""
    W, x0, x1 = 420, 24, 236   # the wall band on the left half; labels on the right
    y = 112
    g = ['<svg viewBox="0 0 %d 440" direction="rtl" role="img" aria-label="חתך מחיצה חסינת אש שנבדקה: שני לוחות ורודים של 12.5 מילימטר מכל צד, ניצבי פלדה של 70 מילימטר וצמר של 5 סנטימטר, 120 דקות לפי נתוני ספק" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">' % W, DEFS]
    g.append(t(W - 12, 24, "חתך מחיצה חסינת אש, מבט מלמעלה", size=15, weight=600))
    g.append(t(W - 12, 44, "מחיצה שספק פרסם עם הבדיקה שלה (רוטנברג, 11.5.2025)", size=12, fill=INK2))
    g.append('<rect x="%d" y="58" width="150" height="42" fill="#fff" stroke="%s" stroke-width="1.6"/>' % (W - 162, RED))
    g.append(t(W - 87, 78, "120 דקות", anchor="middle", size=16, weight=600, fill=RED))
    g.append(t(W - 87, 94, "בבדיקה לפי ת\"י 931", anchor="middle", size=11, fill=RED))
    rows = [("b", 12.5), ("b", 12.5), ("c", 70), ("b", 12.5), ("b", 12.5)]
    ys = []
    for kind, mm in rows:
        h = mm * 1.6
        if kind == "b":
            g.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="url(#q6fr)" stroke="%s" stroke-width="1"/>' % (x0, y, x1 - x0, h, INK))
        else:
            g.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="#fff" stroke="%s" stroke-width="0.6"/>' % (x0, y, x1 - x0, h, INK))
            g.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="url(#q6wool)"/>' % (x0 + 2, y + 18, x1 - x0 - 4, 50 * 1.6))
            for sx in (x0 + 8, (x0 + x1) // 2 - 7, x1 - 22):  # C studs (no spacing claimed)
                g.append('<path d="M%d %.1f H%d V%.1f H%d" fill="none" stroke="%s" stroke-width="2.4"/>' % (sx + 14, y, sx, y + h, sx + 14, INK))
        ys.append((y, h, kind))
        y += h
    # labels with leaders (rtl: anchor end = the label's left end sits at x)
    lab = [(ys[0][0] + 20, "2 × לוח ורוד 12.5 מ\"מ", "צד א"), (ys[2][0] + ys[2][1] / 2 + 5, "ניצבי פלדה 70 מ\"מ", "צמר 5 ס\"מ, 24 ק\"ג למ\"ק"),
           (ys[3][0] + 20, "2 × לוח ורוד 12.5 מ\"מ", "צד ב")]
    for ly, a, b in lab:
        g.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="0.8"/>' % (x1 + 2, ly - 4, x1 + 12, ly - 4, INK))
        g.append(t(x1 + 16, ly, a, anchor="end", size=14, weight=500))
        g.append(t(x1 + 16, ly + 18, b, anchor="end", size=12.5, fill=INK2))
    yb = y + 16
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (x0, yb, x1, yb, INK))
    g.append(t((x0 + x1) // 2, yb + 18, "עובי הקיר כ-120 מ\"מ (חישוב: 4 × 12.5 + 70)", anchor="middle", size=12, mono=False))
    yt = yb + 44
    for i, (std, what) in enumerate([("ת\"י 931", "בדיקת הקיר כולו"), ("ת\"י 755", "סיווג הלוח באש"), ("ת\"י 1490 חלק 1", "תקן הלוח")]):
        xr = W - 12 - i * 136
        g.append('<rect x="%d" y="%d" width="128" height="40" fill="#fff" stroke="%s"/>' % (xr - 128, yt, INK))
        g.append(t(xr - 64, yt + 17, std, anchor="middle", size=13, weight=600, mono=True))
        g.append(t(xr - 64, yt + 33, what, anchor="middle", size=11.5, fill=INK2))
    g.append('</svg>')
    return "".join(g)


BOARDS = [  # colour, name, use, fire board?
    ("#FFFFFF", None, "לבן", "רגיל, חדר יבש", False),
    ("#7FB98A", None, "ירוק", "מים ולחות", False),
    (None, "q6fr", "ורוד או אדום", "מעכב בעירה (FR)", True),
    (None, "q6fm", "ירוק ורוד", "אש ומים (FM)", True),
    (None, "q6fd", "ורוד עבה", "פירים ופלדה", True),
    ("#6F9FD8", None, "כחול", "חוץ וחדר רטוב", False),
    ("#F0A04B", None, "כתום", "חיפוי חוץ", False),
    ("#F2D15A", None, "צהוב", "חוץ ופנים, רטיבות", False),
    ("#C9CED3", None, "כסוף", "אקוסטי וחזק", False),
]


def colours_svg():
    """Nine boards, three by three: the colour, what it is for, and whether it is a fire board."""
    W, cw, ch = 420, 132, 92
    g = ['<svg viewBox="0 0 %d 352" direction="rtl" role="img" aria-label="מפת צבעי לוחות הגבס: לבן, ירוק, ורוד, משולב, ורוד עבה, כחול, כתום, צהוב וכסוף, ואילו מהם לוחות אש" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">' % W, DEFS]
    g.append(t(W - 12, 24, "מפת צבעי לוחות הגבס", size=15, weight=600))
    g.append(t(W - 12, 42, "רק ורוד, משולב וורוד עבה הם לוחות אש. כתום, צהוב וכחול אינם", size=12, fill=INK2))
    for i, (col, pat, name, use, fire) in enumerate(BOARDS):
        r, c = divmod(i, 3)
        xr = W - 12 - c * (cw + 6); y = 56 + r * ch
        g.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#fff" stroke="%s"/>' % (xr - cw, y, cw, ch - 8, LINE))
        g.append('<rect x="%d" y="%d" width="30" height="62" fill="%s" stroke="%s"/>' % (xr - 38, y + 9, ("url(#%s)" % pat) if pat else col, INK))
        g.append(t(xr - 46, y + 26, name, size=13, weight=600))
        g.append(t(xr - 46, y + 44, use, size=11.5, fill=INK2))
        g.append(t(xr - 46, y + 66, "לוח אש" if fire else "לא לוח אש", size=11.5, weight=600 if fire else 400, fill=RED if fire else "#5E6A75"))
    g.append(t(W - 12, 56 + 3 * ch + 4, "לפי קטלוג טמבור (27.7.2026) ואתרי היבואנים. לוח אדום וורוד הם אותו לוח.", size=11.5, fill=INK2))
    g.append('</svg>')
    return "".join(g)


if __name__ == "__main__":
    import io, os, sys
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    for n, f in (("partition", partition_svg), ("colours", colours_svg)):
        s = f().replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        io.open(os.path.join(out, "q6-%s.svg" % n), "w", encoding="utf-8").write(s)
        print(n, len(s), "bytes")
