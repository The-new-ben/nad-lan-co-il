# -*- coding: utf-8 -*-
"""The four inline SVGs of /israel-mortgage-non-residents/ (U3 rewrite, English, LTR).

Design (owner design law 13.10.2026, dna.md 8.5): the world of a cross-border buyer. Passport navy #1E2B47, visa-stamp violet #5B3FA0,
security-print teal #0F7C7A, cool paper white #F6F8FA, slate text #2B3440. Words in Public Sans (a public-forms face), figures in
IBM Plex Mono (the bank statement world); no web font is loaded inside post content, so the stacks fall back to IBM Plex Sans and the
system face. Not the default look: no cream, brass or terracotta, no Inter or Space Grotesk, no acid accent on black, no soft-shadow cards.

viewBox width 420, every text >= 12px in that box, LTR, inline styles only. Every number comes in as an argument from write_u3_page.py,
where it is computed and asserted against dna.md (section 6 facts, 8.4 tables)."""

FONT = "font-family:'Public Sans','IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif"
MONO = "font-family:'IBM Plex Mono',ui-monospace,'SFMono-Regular',Consolas,monospace"
NAVY, VIOLET, TEAL, PAPER, SLATE = "#1E2B47", "#5B3FA0", "#0F7C7A", "#F6F8FA", "#2B3440"
MUTED, LINE, FEES = "#4A5563", "#C9D2DC", "#8A95A3"


def ils(v):
    return "₪{:,.0f}".format(v)


def t(x, y, s, anchor="start", size=13, weight=400, fill=SLATE, mono=False):
    return '<text x="%s" y="%s" text-anchor="%s" style="%s;font-size:%spx;font-weight:%s" fill="%s">%s</text>' % (
        x, y, anchor, MONO if mono else FONT, size, weight, fill, s)


def svg_open(h, label):
    return ('<svg viewBox="0 0 420 %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%s" '
            'style="display:block;width:100%%;height:auto;max-width:640px;background:%s;direction:ltr">' % (h, label, PAPER))


def rulebooks_svg(tax_res_from, top, foreign_to):
    """Citizenship (rows) by residency (columns): the loan cap and the purchase tax track in each cell."""
    H = 472
    g = [svg_open(H, "Two rulebooks: citizenship sets the loan cap, residency sets the purchase tax. Not an Israeli citizen: 50% on any home. "
                     "Israeli citizen, only home in Israel: 75%. Living abroad: purchase tax 8% up to " + ils(top) + " and 10% above; "
                     "living in Israel: resident rates, 0% up to " + ils(tax_res_from) + ".")]
    g.append(t(14, 26, "Two rulebooks, one purchase", size=16, weight=700, fill=NAVY))
    g.append(t(14, 46, "Citizenship sets the loan (Directive 329).", size=12.5, fill=MUTED))
    g.append(t(14, 63, "Residency sets the purchase tax (Tax Authority).", size=12.5, fill=MUTED))
    x0, xa, xb, cw = 14, 90, 254, 158
    g.append(t(xa + cw / 2, 92, "You live in Israel", anchor="middle", size=12.5, weight=600, fill=TEAL))
    g.append(t(xb + cw / 2, 92, "You live abroad", anchor="middle", size=12.5, weight=600, fill=TEAL))
    rows = [("Israeli", "citizen", [
        ("75%", "loan cap, only home", ["Tax: resident rates", "0%% to %s" % ils(tax_res_from), "Olim: relief 12A"]),
        ("75%", "loan cap, only home", ["Tax: foreign rate", "8%% to %s" % ils(top), "10% above"])]),
            ("Not a", "citizen", [
        ("75%*", "by the text of 329", ["*Get it in writing", "Tax: resident rates"]),
        ("50%", "any home at all", ["Tax: foreign rate", "8%% to %s" % ils(top), "10% above"])])]
    y = 102
    for r1, r2, cells in rows:
        ch = 134
        g.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y, xa - x0 - 6, ch, NAVY))
        g.append(t(x0 + 8, y + 26, r1, size=13, weight=700, fill="#FFFFFF"))
        g.append(t(x0 + 8, y + 43, r2, size=13, weight=700, fill="#FFFFFF"))
        for i, (big, cap, lines) in enumerate(cells):
            x = xa if i == 0 else xb
            soft = big.endswith("*")
            g.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#FFFFFF" stroke="%s" stroke-width="1.2"%s/>' % (
                x, y, cw - 6, ch, VIOLET if soft else NAVY, ' stroke-dasharray="5 4"' if soft else ""))
            g.append(t(x + 10, y + 34, big, size=26, weight=600, fill=VIOLET if soft else NAVY, mono=True))
            g.append(t(x + 10, y + 53, cap, size=12, fill=MUTED))
            for j, ln in enumerate(lines):
                g.append(t(x + 10, y + 80 + j * 17, ln, size=12, weight=600 if j == 0 else 400, fill=SLATE))
        y += ch + 8
    g.append('<rect x="%d" y="%d" width="392" height="46" fill="#E3F1F0" stroke="%s"/>' % (x0, y + 2, TEAL))
    g.append(t(x0 + 10, y + 21, "Already own a home in Israel: 50% for any buyer", size=12.5, weight=600, fill=NAVY))
    g.append(t(x0 + 10, y + 39, "(70% for an Israeli citizen who will sell it)", size=12, fill=SLATE))
    g.append(t(x0, H - 10, "Foreign resident rate for purchases until %s." % foreign_to, size=12, fill=MUTED))
    g.append('</svg>')
    return "".join(g)


def cash_svg(rows, fx_label):
    """Four stacked bars for a 4,000,000 home: loan, your cash toward the price, purchase tax, fees.
    rows: [(name, loan, cash_for_price, tax, fees, cash_to_close, usd)]"""
    H = 104 + 92 * len(rows) + 40
    g = [svg_open(H, "Where 4,000,000 shekels comes from, by buyer status: " + "; ".join(
        "%s: loan %s, cash to close %s" % (r[0], ils(r[1]), ils(r[5])) for r in rows))]
    g.append(t(14, 26, "Where ₪4,000,000 comes from", size=16, weight=700, fill=NAVY))
    g.append(t(14, 45, "Loan at the highest cap, 25 years, 4.62% fixed (Aug 2026)", size=12.5, fill=MUTED))
    leg = [("Loan", NAVY), ("Your cash for the price", TEAL), ("Purchase tax", VIOLET), ("Fees", FEES)]
    lx = 14
    for name, col in leg:
        g.append('<rect x="%d" y="58" width="12" height="12" fill="%s"/>' % (lx, col))
        g.append(t(lx + 17, 69, name, size=12, fill=SLATE))
        lx += 17 + int(len(name) * 6.6) + 14
    total_max = max(r[1] + r[2] + r[3] + r[4] for r in rows)
    W = 392.0
    y = 96
    for name, loan, cash, tax, fees, close, usd in rows:
        g.append(t(14, y, name, size=13, weight=700, fill=NAVY))
        x = 14.0
        for v, col, lab in ((loan, NAVY, "Loan " + ils(loan)), (cash, TEAL, ils(cash)), (tax, VIOLET, ""), (fees, FEES, "")):
            w = W * v / total_max
            g.append('<rect x="%.1f" y="%d" width="%.1f" height="26" fill="%s"/>' % (x, y + 8, max(w, 1.0), col))
            if lab and w > len(lab) * 7.3 + 10:
                g.append(t("%.1f" % (x + 6), y + 26, lab, size=12, weight=600, fill="#FFFFFF", mono=True))
            x += w
        g.append(t(14, y + 54, "Cash to close " + ils(close), size=13, weight=700, fill=SLATE, mono=True))
        g.append(t(14, y + 71, "≈ ${:,.0f} · tax {}".format(usd, ils(tax)), size=12, fill=MUTED, mono=True))
        y += 92
    g.append(t(14, H - 26, "$ approx., %s." % fx_label, size=12, fill=MUTED))
    g.append(t(14, H - 10, "Fees: lawyer 0.5% + VAT, appraiser, file fee (typical).", size=12, fill=MUTED))
    g.append('</svg>')
    return "".join(g)


def timeline_svg(steps):
    """A vertical track: the legal clock on the left, the step on the right; a violet tag under the clock where documents are asked for.
    steps: [(clock_line1, clock_line2, title, [detail lines], docs)]"""
    H = 70 + 78 * len(steps) + 6
    g = [svg_open(H, "From approval in principle to the money: " + "; ".join("%s (%s %s)" % (s[2], s[0], s[1]) for s in steps))]
    g.append(t(14, 26, "From approval to money", size=16, weight=700, fill=NAVY))
    g.append(t(14, 45, "The clocks set by rule, and where documents are asked for", size=12.5, fill=MUTED))
    y = 66
    g.append('<line x1="57" y1="%d" x2="57" y2="%d" stroke="%s" stroke-width="2"/>' % (y + 22, y + 78 * (len(steps) - 1) + 22, LINE))
    for c1, c2, title, lines, docs in steps:
        g.append('<rect x="14" y="%d" width="86" height="44" fill="%s"/>' % (y, NAVY))
        g.append(t(57, y + 19, c1, anchor="middle", size=13, weight=600, fill="#FFFFFF", mono=True))
        g.append(t(57, y + 36, c2, anchor="middle", size=12, fill="#DCE3EC"))
        if docs:
            g.append('<rect x="14" y="%d" width="86" height="19" fill="#FFFFFF" stroke="%s"/>' % (y + 49, VIOLET))
            g.append(t(57, y + 63, "documents", anchor="middle", size=12, weight=600, fill=VIOLET))
        g.append(t(112, y + 15, title, size=13.5, weight=700, fill=NAVY))
        for j, ln in enumerate(lines):
            g.append(t(112, y + 33 + j * 16, ln, size=12, fill=SLATE))
        y += 78
    g.append('</svg>')
    return "".join(g)


def rates_svg(path, fixed_avg, foot):
    """Bank of Israel rate in 2026 as steps (prime dashed, 1.5 above) and the monthly average fixed not linked rate as dots.
    path: [(day_of_year, rate)] in force from that day; fixed_avg: [(mid-month day_of_year, rate, month)]."""
    H = 300
    x0, x1, y0, y1 = 44, 404, 250, 74   # plot box: x by day 1..298 (25 Oct), y 2.75..5.75
    lo, hi, dmax = 2.75, 5.75, 298

    def X(d): return x0 + (x1 - x0) * (d - 1) / (dmax - 1)

    def Y(v): return y0 - (y0 - y1) * (v - lo) / (hi - lo)
    g = [svg_open(H, "Bank of Israel rate in 2026: " + ", ".join("%.2f%%" % r for d, r in path) + "; prime 1.5 points above it; "
                     "average fixed not linked mortgage rate " + ", ".join("%s %.2f%%" % (m, r) for d, r, m in fixed_avg))]
    g.append(t(14, 26, "Rates in 2026", size=16, weight=700, fill=NAVY))
    g.append(t(14, 45, "Bank of Israel rate, prime, and the average fixed", size=12.5, fill=MUTED))
    g.append(t(14, 62, "not linked rate on new mortgages", size=12.5, fill=MUTED))
    for v in (3.0, 4.0, 5.0):
        g.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="0.8"/>' % (x0, Y(v), x1, Y(v), LINE))
        g.append(t(x0 - 6, "%.1f" % (Y(v) + 4), "%.0f%%" % v, anchor="end", size=12, fill=MUTED, mono=True))
    for d, lab in ((1, "Jan"), (60, "Mar"), (121, "May"), (182, "Jul"), (244, "Sep")):
        g.append(t("%.1f" % X(d), y0 + 18, lab, size=12, fill=MUTED))
    for off, col, dash, w in ((1.5, VIOLET, ' stroke-dasharray="5 4"', 1.6), (0.0, NAVY, "", 2.6)):
        pts = []
        for i, (d, r) in enumerate(path):
            dn = path[i + 1][0] if i + 1 < len(path) else dmax
            pts += ["%.1f,%.1f" % (X(d), Y(r + off)), "%.1f,%.1f" % (X(dn), Y(r + off))]
        g.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"%s/>' % (" ".join(pts), col, w, dash))
    d0, r0 = path[0]
    g.append(t("%.1f" % (X(d0) + 2), "%.1f" % (Y(r0 + 1.5) - 7), "Prime (Bank of Israel rate + 1.5)", size=12, weight=600, fill=VIOLET))
    g.append(t("%.1f" % (X(d0) + 2), "%.1f" % (Y(r0) - 7), "Bank of Israel rate", size=12, weight=600, fill=NAVY))
    last = path[-1][1]
    g.append(t(x1, "%.1f" % (Y(last + 1.5) - 6), "%.2f%%" % (last + 1.5), anchor="end", size=12, weight=600, fill=VIOLET, mono=True))
    g.append(t(x1, "%.1f" % (Y(last) - 6), "%.2f%%" % last, anchor="end", size=12, weight=600, fill=NAVY, mono=True))
    for d, r, m in fixed_avg:
        g.append('<circle cx="%.1f" cy="%.1f" r="4.2" fill="%s"/>' % (X(d), Y(r), TEAL))
    lx, ly = X(fixed_avg[0][0]) - 12, Y(fixed_avg[0][1]) + 4   # to the left of the first dot, between the prime and the 4% lines
    g.append(t("%.1f" % lx, "%.1f" % ly, "Average fixed, not linked", anchor="end", size=12, weight=600, fill=TEAL))
    g.append(t("%.1f" % lx, "%.1f" % (ly + 16), "%.2f%% %s to %.2f%% %s" % (fixed_avg[0][1], fixed_avg[0][2], fixed_avg[-1][1], fixed_avg[-1][2]),
               anchor="end", size=12, fill=TEAL, mono=True))
    g.append(t(14, H - 10, foot, size=12, fill=MUTED))
    g.append('</svg>')
    return "".join(g)
