# -*- coding: utf-8 -*-
"""The charts of /property-value-estimator/ stage 2 (Q2), as inline SVG for the page content (post content cannot load fonts or
scripts, so every style is inline). Drawn like a land-registry and survey sheet (owner design law 13.10.2026: the subject's own
world): white paper, graphite #3E4C58 grid, registry blue #1F4FA3 for the data, stamp red #C42550 only for the asking-price pin.
Words in IBM Plex Sans Hebrew, figures in IBM Plex Mono (both are loaded by the site skin). Not the default look: no cream, no gold,
no gradients, no cards. Scales follow the number line (low on the left, high on the right) and time runs left to right, as in CBS
charts. In the SVG, direction is rtl: text-anchor start = the right end of a label, end = its left end.
Every number comes in from write_q2_stage2.py (official files, CBS, our calculation); nothing is typed here."""

FONT = "font-family:'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif"
MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"
BLUE, RED, INK, GRAPH, LINE, PALE = "#1F4FA3", "#C42550", "#12202A", "#3E4C58", "#D3DCE2", "#E8EEF8"
LRM = "‎"  # keeps a sign in front of its number inside rtl text (-2.7% instead of 2.7%-)


def t(x, y, s, anchor="start", size=13, weight=400, fill=INK, mono=False, halo=False):
    """A label; halo = a white outline under the glyphs, so a grid or reference line passing behind never cuts the figure."""
    h = ";paint-order:stroke;stroke:#fff;stroke-width:3.5px;stroke-linejoin:round" if halo else ""
    return '<text x="%s" y="%s" text-anchor="%s" style="%s;font-size:%spx;font-weight:%s%s" fill="%s">%s</text>' % (
        _f(x), _f(y), anchor, MONO if mono else FONT, size, weight, h, fill, s)


def _f(v):
    return ("%.1f" % v).rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def svg_open(w, h, label):
    return ('<svg viewBox="0 0 %d %d" direction="rtl" role="img" aria-label="%s" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">'
            % (w, h, label))


def sparkline(series, label):
    """One tiny line per table row: 22 quarters, left (1-3.2021) to right (4-6.2026); gaps where the file has no median; the last
    point marked. Each row has its own vertical scale (said in the table caption). No text inside."""
    W, Hh, px, top, bot = 110, 28, 4, 4, 24
    vals = [v for v in series if v]
    lo, hi = min(vals), max(vals); span = (hi - lo) or 1.0
    n = len(series)
    xs = [px + i * (W - 2 * px) / float(max(n - 1, 1)) for i in range(n)]
    ys = [None if v is None else bot - (v - lo) / span * (bot - top) for v in series]
    g = ['<svg viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s" style="display:block;width:%dpx;height:%dpx;overflow:visible">'
         % (W, Hh, W, Hh, label, W, Hh)]
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="0.6"/>' % (px, bot + 2, W - px, bot + 2, LINE))
    run = []
    def flush():
        if len(run) >= 2:
            g.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>'
                     % (" ".join("%.1f,%.1f" % p for p in run), BLUE))
        elif len(run) == 1:
            g.append('<circle cx="%.1f" cy="%.1f" r="1.3" fill="%s"/>' % (run[0][0], run[0][1], BLUE))
    for x, y in zip(xs, ys):
        if y is None:
            flush(); run = []
        else:
            run.append((x, y))
    flush()
    last = max(i for i, v in enumerate(series) if v)
    g.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="%s" stroke="#fff" stroke-width="1"/>' % (xs[last], ys[last], BLUE))
    g.append('</svg>')
    return "".join(g)


def anchors_svg(a, title, sub, foot, label):
    """I3: the three checks on one price scale, the band between the lowest and the highest, and the asking price as a red pin.
    a = dict(lo, hi, ticks=[(value, text)], marks=[(value, line1, line2, 'up'|'down')], pin=(value, line1, line2), unit)."""
    W, x0, x1 = 420, 30, 392  # the scale runs left (low) to right (high)
    lo, hi = a["lo"], a["hi"]
    X = lambda v: x0 + (v - lo) / float(hi - lo) * (x1 - x0)
    ys = 156
    g = [svg_open(W, 306, label)]
    g.append(t(W - 12, 25, title, size=16, weight=600))
    g.append(t(W - 12, 47, sub, size=13, fill=GRAPH))
    vals = [m[0] for m in a["marks"]]
    g.append('<rect x="%.1f" y="%d" width="%.1f" height="24" fill="%s" stroke="%s" stroke-width="0.8"/>' % (X(min(vals)), ys - 12, X(max(vals)) - X(min(vals)), PALE, BLUE))
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2"/>' % (x0, ys, x1, ys, INK))
    for v, txt in a["ticks"]:
        g.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="0.8"/>' % (X(v), ys + 14, X(v), ys + 20, GRAPH))
        g.append(t(X(v), ys + 80, txt, anchor="middle", size=13, fill=GRAPH, mono=True))
    g.append(t(x0 + (x1 - x0) / 2.0, ys + 99, a["unit"], anchor="middle", size=13, fill=GRAPH))
    for v, l1, l2, side in a["marks"]:
        x = X(v)
        g.append('<circle cx="%.1f" cy="%d" r="5.5" fill="%s" stroke="#fff" stroke-width="1.5"/>' % (x, ys, BLUE))
        if side == "up":
            g.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="0.8"/>' % (x, ys - 14, x, ys - 26, BLUE))
            g.append(t(x, ys - 50, l1, anchor="middle", size=13.5, weight=600))
            g.append(t(x, ys - 32, l2, anchor="middle", size=13.5, mono=True, fill=BLUE))
        else:
            g.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="0.8"/>' % (x, ys + 14, x, ys + 24, BLUE))
            g.append(t(x, ys + 40, l1, anchor="middle", size=13.5, weight=600))
            g.append(t(x, ys + 58, l2, anchor="middle", size=13.5, mono=True, fill=BLUE))
    pv, p1, p2 = a["pin"]; x = X(pv)
    g.append('<path d="M%.1f %d L%.1f %d A9 9 0 1 1 %.1f %d Z" fill="%s"/>' % (x, ys - 2, x - 7.4, ys - 22, x + 7.4, ys - 22, RED))
    g.append('<circle cx="%.1f" cy="%d" r="3.2" fill="#fff"/>' % (x, ys - 27))
    g.append(t(x, ys + 40, p1, anchor="middle", size=13.5, weight=600, fill=RED))
    g.append(t(x, ys + 58, p2, anchor="middle", size=13.5, mono=True, fill=RED))
    g.append(t(W - 12, 294, foot, size=13, fill=GRAPH))
    g.append('</svg>')
    return "".join(g)


def districts_svg(rows, title, sub, label):
    """I2: two bars per row, the change over 12 months (graphite) and over 5 years (registry blue), on one percent scale with zero
    marked. rows[0] is the national index (outlined bars), and its two values also run as dashed lines behind every district, so
    each district reads against the country. rows = [(name, d12, d5)]."""
    W, zero, k = 420, 56, 5.5          # zero near the left edge: the 12-month changes are small and negative, the 5-year ones large
    X = lambda p: zero + p * k
    top, gap = 100, 46
    yb = top + gap * len(rows) - 8
    g = [svg_open(W, yb + 30, label)]
    g.append(t(W - 12, 25, title, size=16, weight=600))
    g.append(t(W - 12, 47, sub, size=13, fill=GRAPH))
    # legend
    g.append('<rect x="%d" y="61" width="14" height="11" fill="%s"/>' % (W - 26, GRAPH))
    g.append(t(W - 32, 71, "12 חודשים", size=13))
    g.append('<rect x="%d" y="61" width="14" height="11" fill="%s"/>' % (W - 140, BLUE))
    g.append(t(W - 146, 71, "5 שנים", size=13))
    g.append('<rect x="%d" y="61" width="14" height="11" fill="#fff" stroke="%s" stroke-width="1.2"/>' % (W - 238, INK))
    g.append(t(W - 244, 71, "כל הארץ, וגם הקו המקווקו", size=13))
    for p in (0, 10, 20, 30, 40):
        g.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="%s"/>' % (X(p), top - 8, X(p), yb, INK if p == 0 else LINE, "1.1" if p == 0 else "0.7"))
        g.append(t(X(p), yb + 18, "%d%%" % p, anchor="middle", size=13, fill=GRAPH, mono=True))
    n12, n5 = rows[0][1], rows[0][2]
    for v in (n12, n5):  # behind the bars and the labels
        g.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.1" stroke-dasharray="4 3"/>' % (X(v), top - 8, X(v), yb, INK))
    for i, (name, d12, d5) in enumerate(rows):
        y = top + i * gap; nat = i == 0
        g.append(t(W - 12, y + 17, name, size=13.5, weight=600))
        a, b = sorted((X(0), X(d12)))
        g.append('<rect x="%.1f" y="%d" width="%.1f" height="10" fill="%s" stroke="%s" stroke-width="%s"/>' % (a, y, max(b - a, 1.5), "#fff" if nat else GRAPH, GRAPH, "1.2" if nat else "0"))
        g.append(t(X(0) + 5, y + 10, LRM + ("%+.1f%%" % d12), anchor="end", size=13, mono=True, fill=GRAPH, halo=True))
        g.append('<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s" stroke="%s" stroke-width="%s"/>' % (X(0), y + 14, X(d5) - X(0), "#fff" if nat else BLUE, BLUE, "1.4" if nat else "0"))
        g.append(t(X(d5) + 4, y + 26.5, LRM + ("%+.1f%%" % d5), anchor="end", size=13, mono=True, fill=BLUE, halo=True))
    g.append('</svg>')
    return "".join(g)
