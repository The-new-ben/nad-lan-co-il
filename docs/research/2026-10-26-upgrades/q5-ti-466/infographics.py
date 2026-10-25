# -*- coding: utf-8 -*-
"""The two infographics of /glossary/תי-466/ (Q5 stage 2), inline SVG with inline styles. A structural drawing sheet (owner design law
13.10.2026: from the subject's own world): white paper, black line work, concrete in the drafting dots-and-triangles hatch, the five
parts in five drafting inks (blue, green, red, violet, graphite), IBM Plex Sans Hebrew for words and IBM Plex Mono for standard numbers
and dates. Not the default look: no cream, no gold, no dark card with a neon accent. Facts: SII standard pages (dna.md section 6).
In the SVG, direction is rtl: text-anchor start = the right end of a label."""
import io, json, os
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
D = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "t466.json"), encoding="utf-8"))
FONT = "font-family:'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif"
MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"
INK, INK2, MUTE = "#12202A", "#3E4C58", "#5E6A75"
C = {k: v["ink"] for k, v in D["parts"].items()}
HATCH = ('<pattern id="q5c" width="9" height="9" patternUnits="userSpaceOnUse"><rect width="9" height="9" fill="#fff"/><circle cx="2" cy="2" r="0.9" fill="#8A97A2"/>'
         '<path d="M6 5 l1.6 2.6 h-3.2z" fill="none" stroke="#8A97A2" stroke-width="0.7"/></pattern>')


def t(x, y, s, anchor="start", size=13, weight=400, fill=INK, mono=False):
    return '<text x="%s" y="%s" text-anchor="%s" style="%s;font-size:%spx;font-weight:%s" fill="%s">%s</text>' % (x, y, anchor, MONO if mono else FONT, size, weight, fill, s)


def building_svg():
    """A section through a residential building, every element in the ink of the part that governs it."""
    W, x0, x1, gy = 420, 150, 352, 268
    g = ['<svg viewBox="0 0 %d 300" direction="rtl" role="img" aria-label="חתך בניין מגורים: חלק 1 חל על כל המבנה, חלק 2 על השלד היצוק, חלק 3 על תקרה דרוכה, חלק 4 על חזית טרומית, חלק 5 על תקרת לוחדים" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">' % W,
         '<defs>' + HATCH + '</defs>']
    g.append(t(W - 12, 22, "ת\"י 466 בבניין: איזה חלק חל על כל אלמנט", size=15, weight=600))
    g.append('<rect x="%d" y="40" width="%d" height="%d" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="6 4"/>' % (x0 - 14, x1 - x0 + 44, gy - 40 + 22, C["1"]))
    g.append(t(x1 + 26, 56, "חלק 1: עקרונות כלליים, לכל המבנה", size=12, fill=C["1"], weight=600))
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2"/>' % (x0 - 30, gy, x1 + 34, gy, INK))
    g.append('<rect x="%d" y="%d" width="%d" height="14" fill="url(#q5c)" stroke="%s" stroke-width="2"/>' % (x0 - 6, gy, x1 - x0 + 12, C["2"]))
    for cx in (x0 + 6, (x0 + x1) // 2, x1 - 18):
        g.append('<rect x="%d" y="80" width="12" height="%d" fill="url(#q5c)" stroke="%s" stroke-width="2"/>' % (cx, gy - 80, C["2"]))
    g.append('<rect x="%d" y="200" width="%d" height="10" fill="url(#q5c)" stroke="%s" stroke-width="2"/>' % (x0, x1 - x0, C["2"]))
    g.append('<rect x="%d" y="140" width="%d" height="12" fill="#fff" stroke="%s" stroke-width="2"/>' % (x0, x1 - x0, C["5"]))
    for cx in range(x0 + 9, x1 - 4, 16):
        g.append('<circle cx="%d" cy="146" r="4" fill="none" stroke="%s" stroke-width="1"/>' % (cx, C["5"]))
    g.append('<rect x="%d" y="76" width="%d" height="12" fill="url(#q5c)" stroke="%s" stroke-width="2"/>' % (x0, x1 - x0, C["3"]))
    g.append('<path d="M%d 79 Q%d 90 %d 79" fill="none" stroke="%s" stroke-width="1.6"/>' % (x0 + 2, (x0 + x1) // 2, x1 - 2, C["3"]))
    for py in range(88, gy, 60):
        g.append('<rect x="%d" y="%d" width="12" height="%d" fill="url(#q5c)" stroke="%s" stroke-width="2"/>' % (x1 + 2, py, min(58, gy - py), C["4"]))
    for y, k, lab in ((82, "3", "תקרה דרוכה"), (146, "5", "תקרת לוח\"דים"), (205, "2", "שלד יצוק"), (240, "4", "חזית טרומית")):
        g.append('<circle cx="%d" cy="%d" r="10" fill="%s"/>' % (x0 - 32, y - 4, C[k]))
        g.append(t(x0 - 32, y + 1, k, anchor="middle", size=13, weight=600, fill="#fff", mono=True))
        g.append(t(x0 - 48, y, lab, size=13, weight=500))
    g.append('</svg>')
    return "".join(g)


EVENTS = [  # year, part, text, still in force?
    ("1977", "4", "מפרט 17, שקדם לחלק 4", False),
    ("1979", "2", "חלק 2, המהדורה הקודמת", False),
    ("1987", "3", "חלק 3, המהדורה הקודמת (יולי)", False),
    ("1987", "5", "חלק 5: תקרות מטבלות חלולות (1.12.1987)", True),
    ("1991", "4", "חלק 4: בטון טרום (1.4.1991)", True),
    ("2003", "1", "חלק 1, המהדורה הקודמת", False),
    ("2015", "2", "חלק 2: רכיבים (31.12.2015)", True),
    ("2017", "3", "חלק 3: בטון דרוך (31.3.2017)", True),
    ("2022", "1", "חלק 1: עקרונות כלליים (15.8.2022)", True),
    ("2025", "1", "תיקון טעות לחלק 1 (ספטמבר 2025)", True),
]


def timeline_svg():
    """The editions on one vertical line: filled = in force today, hollow = replaced."""
    W, top, step = 420, 62, 30
    hgt = top + step * len(EVENTS) + 34
    g = ['<svg viewBox="0 0 %d %d" direction="rtl" role="img" aria-label="ציר המהדורות של ת&quot;י 466 מ-1977 עד 2025" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">' % (W, hgt)]
    g.append(t(W - 12, 22, "ציר המהדורות של ת\"י 466", size=15, weight=600))
    g.append(t(W - 12, 42, "מלא: בתוקף היום. חלול: מהדורה שהוחלפה", size=12, fill=INK2))
    xl = W - 74
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.4"/>' % (xl, top - 8, xl, top + step * (len(EVENTS) - 1) + 8, INK))
    for i, (yr, k, txt, live) in enumerate(EVENTS):
        y = top + i * step
        g.append(t(W - 12, y + 5, yr, size=13, weight=600, mono=True))
        g.append('<circle cx="%d" cy="%d" r="7" fill="%s" stroke="%s" stroke-width="2"/>' % (xl, y, C[k] if live else "#fff", C[k]))
        g.append(t(xl - 16, y + 5, txt, size=13, weight=500 if live else 400, fill=INK if live else MUTE))
    g.append(t(W - 12, hgt - 10, "לפי עמודי התקנים באתר מכון התקנים, 25.10.2026", size=11.5, fill=INK2))
    g.append('</svg>')
    return "".join(g)


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else H
    for n, f in (("building", building_svg), ("timeline", timeline_svg)):
        s = f().replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        io.open(os.path.join(out, "q5-%s.svg" % n), "w", encoding="utf-8").write(s)
        print(n, len(s), "bytes")
