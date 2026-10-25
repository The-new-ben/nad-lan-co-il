# -*- coding: utf-8 -*-
"""The two infographics of /glossary/מחירון-דקל-לבנייה-ותשתיות/ (Q3 stage 2), inline SVG with inline styles. A checked tender bill of
quantities (owner design law 13.10.2026: from the subject's own world): white sheet, graphite ruled grid, ink-blue column heads, the
checker's red-pen ring around the price cell; IBM Plex Sans Hebrew for words, IBM Plex Mono for codes and numbers. Not the default
look: no cream, no terracotta or gold, no dark ground with one neon accent. No Dekel price is shown (Dekel sells them); the item code
format is from a public tender (Afula municipality, "מהדורת מאי 2025"). In the SVG, direction is rtl: text-anchor start = the right end."""
import io, json, os
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
D = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "dekel.json"), encoding="utf-8"))
FONT = "font-family:'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif"
MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"
INK, INK2, BLUE, RED, GRID = "#12202A", "#3E4C58", "#1F4FA3", "#C42550", "#B9C3CB"


def t(x, y, s, anchor="start", size=13, weight=400, fill=INK, mono=False):
    return '<text x="%s" y="%s" text-anchor="%s" style="%s;font-size:%spx;font-weight:%s" fill="%s">%s</text>' % (x, y, anchor, MONO if mono else FONT, size, weight, fill, s)


def anatomy_svg():
    """One bill-of-quantities line, split into its fields, each with what to check (Dekel FAQ rules)."""
    W = 420
    cols = [("קוד", 92, "68.035.0010"), ("תיאור", 102, "תיאור הסעיף"), ("יחידה", 46, "יח'"), ("כמות", 50, "24"), ("מחיר יחידה", 76, "₪ ____")]  # right to left
    g = ['<svg viewBox="0 0 %d 360" direction="rtl" role="img" aria-label="אנטומיה של סעיף במחירון דקל: קוד, תיאור, יחידה, כמות ומחיר יחידה, ומה בודקים בכל אחד" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">' % W]
    g.append(t(W - 12, 22, "אנטומיה של סעיף דקל, כמו בכתב כמויות", size=15, weight=600))
    g.append(t(W - 12, 42, "קוד בפורמט פרק . תת פרק . סעיף. מחיר היחידה מהמנוי, לא מכאן", size=12, fill=INK2))
    x = W - 12; y0 = 58
    xs = []
    for name, w, val in cols:
        g.append('<rect x="%d" y="%d" width="%d" height="26" fill="#EEF2F8" stroke="%s"/>' % (x - w, y0, w, GRID))
        g.append(t(x - w / 2, y0 + 18, name, anchor="middle", size=12.5, weight=600, fill=BLUE))
        g.append('<rect x="%d" y="%d" width="%d" height="34" fill="#fff" stroke="%s"/>' % (x - w, y0 + 26, w, GRID))
        g.append(t(x - w / 2, y0 + 48, val, anchor="middle", size=12.5, mono=name in ("קוד", "כמות", "מחיר יחידה")))
        xs.append((x - w / 2, name)); x -= w
    px = xs[-1][0]
    g.append('<ellipse cx="%d" cy="%d" rx="44" ry="22" fill="none" stroke="%s" stroke-width="2"/>' % (px, y0 + 43, RED))
    notes = [("קוד", "פרק, תת פרק וסעיף. אותו קוד בהצעה ובמחירון, מאותה מהדורה"), ("תיאור", "מה כלול בעבודה. האם ברזל הזיון בפנים או בסעיף נפרד"),
             ("יחידה", "מ\"ר, מ\"ק, מטר אורך, יחידה או קומפלט. הכמות נמדדת באותה יחידה"), ("כמות", "מכתב הכמויות או מהמדידה בשטח"),
             ("מחיר יחידה", "לפי המהדורה של החודש: עבודה, חומרים ורווח קבלן, אלא אם כתוב אחרת")]
    y = y0 + 92
    for i, (name, txt) in enumerate(notes):
        cx = [c for c, n in xs if n == name][0]
        yy = y + i * 46
        g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="0.8" stroke-dasharray="2 3"/>' % (cx, y0 + 60, cx, yy - 12, GRID))
        g.append('<circle cx="%d" cy="%d" r="3" fill="%s"/>' % (cx, yy - 12, RED if name == "מחיר יחידה" else BLUE))
        g.append(t(W - 12, yy, name, size=12.5, weight=600, fill=RED if name == "מחיר יחידה" else BLUE))
        g.append(t(W - 12, yy + 17, txt, size=12, fill=INK2))
    g.append('</svg>')
    return "".join(g)


def tree_svg():
    """The kind of work to the Dekel list, the same rule as the dkpick tool."""
    K = list(D["kinds"].keys()); W, top, step = 420, 60, 36
    hgt = top + step * len(K) + 10
    g = ['<svg viewBox="0 0 %d %d" direction="rtl" role="img" aria-label="איזה מחירון דקל לאיזו עבודה" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">' % (W, hgt)]
    g.append(t(W - 12, 22, "איזה מחירון דקל לאיזו עבודה", size=15, weight=600))
    g.append(t(W - 12, 44, "העבודה", size=12, fill=INK2)); g.append(t(160, 44, "המחירון", size=12, fill=INK2))
    for i, k in enumerate(K):
        y = top + i * step; L = D["lists"][D["kinds"][k]["list"]]
        g.append('<rect x="236" y="%d" width="172" height="26" fill="#fff" stroke="%s"/>' % (y - 14, BLUE))
        g.append(t(402, y + 4, D["kinds"][k]["label"], size=12.5))
        g.append('<line x1="236" y1="%d" x2="166" y2="%d" stroke="%s" stroke-width="1.2"/>' % (y - 1, y - 1, BLUE))
        g.append(t(160, y + 4, L["name"].replace("מחירון דקל ", "").replace("מחירון ", ""), size=12.5, weight=600, fill=BLUE))
        if L.get("min"):
            g.append(t(160, y + 19, "%s עד %s ₪" % ("{:,}".format(L["min"]), "{:,}".format(L["max"])), size=10.5, fill=INK2, mono=True))
    g.append('</svg>')
    return "".join(g)


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else H
    for n, f in (("anatomy", anatomy_svg), ("tree", tree_svg)):
        s = f().replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        io.open(os.path.join(out, "q3-%s.svg" % n), "w", encoding="utf-8").write(s)
        print(n, len(s), "bytes")
