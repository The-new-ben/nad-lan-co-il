# -*- coding: utf-8 -*-
"""AbroadGuide kit (design system component AbroadGuide, 22.10.2026, HAD-592): the parts of a deep guide page, written into the
page body with one inline <style>. Identity: the land-registry dossier (NadLan Instruments tokens: chart paper, ink, sea, survey
red; Karantina for big figures, IBM Plex Sans Hebrew for text, IBM Plex Mono for amounts). Every rule starts with .nlag so the
theme's !important colours and sizes cannot reach in. No visible em/en dashes. Phones first: tables become labelled cards.

  from nlag import css, ledger, bill, chart, table, route, checks, israel, honest, faq, cluster, wrap
"""
import html as _h

E = _h.escape


def num(x, d=0):
    return ("{:,.%df}" % d).format(x)


def money(eur, fx=None, d=0):
    """€ amount, and the ₪ amount under it at the Bank of Israel rate."""
    s = '<bdi class="m">€' + num(eur, d) + '</bdi>'
    if fx:
        s += ' <small class="ils"><bdi>₪' + num(eur * fx) + '</bdi></small>'
    return s


CSS = """<style id="nlag-css">
.nlag{--g:#F6F8F9;--w:#FFFFFF;--i:#12202A;--i2:#3E4C58;--mu:#5E6A75;--ln:#D3DCE2;--sea:#2F6F86;--deep:#1F4B5C;--red:#C42550;--sea-t:#E6F0F3;--red-t:#FBE9EE;
 --disp:"Karantina","IBM Plex Sans Hebrew",system-ui,sans-serif;--sans:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace;
 direction:rtl;color:var(--i2);font-family:var(--sans)}
.nlag *{box-sizing:border-box}
.nlag bdi{white-space:nowrap;unicode-bidi:isolate;font-variant-numeric:tabular-nums}
.nlag .m,.nlag .nlag-ledger bdi,.nlag .nlag-bill bdi,.nlag table bdi,.nlag .nlag-route .who{font-family:var(--mono)}
.nlag .nlag-answer{font-size:1.08rem;line-height:1.75;color:var(--i);margin:0 0 18px}
.nlag .nlag-answer strong{color:var(--i)}
.nlag .nlag-ledger{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border:1px solid var(--ln);background:var(--w);border-radius:6px;margin:0 0 22px;position:relative;overflow:hidden}
.nlag .nlag-ledger::before{content:"";position:absolute;inset:0;pointer-events:none;background-image:linear-gradient(var(--ln) 1px,transparent 1px),linear-gradient(90deg,var(--ln) 1px,transparent 1px);background-size:16px 16px;opacity:.18}
.nlag .nlag-ledger div{padding:12px 14px;border-inline-start:1px solid var(--ln);border-bottom:1px solid var(--ln);position:relative;display:grid;gap:2px}
.nlag .nlag-ledger span{font:500 12.5px/17px var(--sans);color:var(--mu)}
.nlag .nlag-ledger b{font:700 34px/34px var(--disp);color:var(--i);letter-spacing:.01em;direction:ltr;text-align:right;unicode-bidi:plaintext}
.nlag .nlag-ledger small{font:400 11.5px/15px var(--mono);color:var(--mu)}
.nlag .nlag-ledger .warn b{color:var(--red)}
.nlag h2{scroll-margin-top:80px}
.nlag .nlag-bill{border:1px solid var(--ln);background:var(--w);border-radius:6px;padding:16px;margin:12px 0 22px}
.nlag .nlag-bill h3{margin:0 0 10px;font:600 1.05rem/1.4 var(--sans);color:var(--i)}
.nlag .nlag-bill ol{list-style:none;margin:0;padding:0;display:grid;gap:9px}
.nlag .nlag-bill li{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,2fr) auto;gap:10px;align-items:center}
.nlag .nlag-bill .lb{font:500 14px/19px var(--sans);color:var(--i2)}
.nlag .nlag-bill .lb small{display:block;color:var(--mu);font:400 12px/16px var(--sans)}
.nlag .nlag-bill .bar{height:12px;background:var(--sea-t);border-radius:2px;overflow:hidden}
.nlag .nlag-bill .bar i{display:block;height:100%;background:var(--sea);transform-origin:right;transform:scaleX(var(--s,1))}
.nlag .nlag-bill li.red .bar i{background:var(--red)}
.nlag .nlag-bill .am{text-align:left;font:500 14px/18px var(--mono);color:var(--i)}
.nlag .nlag-bill .am small{display:block;color:var(--mu);font-size:12px}
.nlag .nlag-bill .tot{margin-top:12px;padding-top:10px;border-top:3px double var(--i);display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
.nlag .nlag-bill .tot span{font:600 15px/20px var(--sans);color:var(--i)}
.nlag .nlag-bill .tot b{font:700 30px/30px var(--disp);color:var(--i)}
@media (prefers-reduced-motion:no-preference){.nlag .nlag-bill.anim .bar i{transform:scaleX(0);transition:transform .6s cubic-bezier(.2,.7,.2,1)}.nlag .nlag-bill.anim.on .bar i{transform:scaleX(var(--s,1))}}
.nlag .nlag-chart{border:1px solid var(--ln);background:var(--w);border-radius:6px;padding:14px 14px 8px;margin:12px 0 8px}
.nlag .nlag-chart h3{margin:0 0 6px;font:600 1.05rem/1.4 var(--sans);color:var(--i)}
.nlag .nlag-chart svg{width:100%;height:auto;display:block;direction:ltr}
.nlag .nlag-chart .ax{stroke:var(--ln);stroke-width:1}
.nlag .nlag-chart .ln{fill:none;stroke:var(--deep);stroke-width:2.2;stroke-linejoin:round}
.nlag .nlag-chart .ln2{fill:none;stroke:var(--sea);stroke-width:1.6;stroke-dasharray:5 4}
.nlag .nlag-chart .ar{fill:var(--sea-t);opacity:.55}
.nlag .nlag-chart text{font:11px var(--mono);fill:var(--mu)}
.nlag .nlag-chart .pt{fill:var(--red)}
.nlag .nlag-chart .pl{font:600 12px var(--mono);fill:var(--i)}
.nlag .nlag-chart .key{display:flex;gap:14px;flex-wrap:wrap;font:400 12px/16px var(--sans);color:var(--mu);margin:6px 0 0}
.nlag .nlag-chart .key i{display:inline-block;width:18px;height:0;border-top:2.2px solid var(--deep);vertical-align:middle;margin-inline-end:6px}
.nlag .nlag-chart .key i.d{border-top:1.6px dashed var(--sea)}
.nlag .nlag-tw{overflow-x:auto;margin:10px 0 22px;border:1px solid var(--ln);border-radius:6px;background:var(--w)}
.nlag table.nlag-t{width:100%;border-collapse:collapse;font-size:14.5px}
.nlag table.nlag-t caption{text-align:start;font:600 14px/20px var(--sans);color:var(--i);padding:10px 12px}
.nlag table.nlag-t th,.nlag table.nlag-t td{padding:9px 12px;border-top:1px solid var(--ln);text-align:start;vertical-align:top}
.nlag table.nlag-t thead th{background:var(--g);font:600 13px/18px var(--sans);color:var(--i2)}
.nlag table.nlag-t td.n{font-family:var(--mono);white-space:nowrap}
.nlag table.nlag-t .l{display:none}
@media (max-width:600px){
 .nlag table.nlag-t .l{display:inline;font-weight:600;color:var(--mu);font-family:var(--sans)}
 .nlag table.nlag-t,.nlag table.nlag-t tbody,.nlag table.nlag-t caption{display:block;width:100%}
 .nlag table.nlag-t tr{display:block;border-top:1px solid var(--ln);padding:8px 0}
 .nlag table.nlag-t td,.nlag table.nlag-t th{display:block;border:0;padding:3px 12px}
 .nlag .nlag-bill li{grid-template-columns:minmax(0,1fr) auto}
 .nlag .nlag-bill .bar{grid-column:1 / -1;order:3}
 .nlag .nlag-ledger{grid-template-columns:repeat(2,minmax(0,1fr))}
 .nlag .nlag-ledger b{font-size:30px;line-height:30px}
}
.nlag .nlag-route{list-style:none;margin:12px 0 22px;padding:0;counter-reset:st;position:relative}
.nlag .nlag-route li{position:relative;padding:0 46px 18px 0;counter-increment:st}
.nlag .nlag-route li::before{content:counter(st);position:absolute;right:0;top:0;width:32px;height:32px;border-radius:50%;background:var(--w);border:2px solid var(--sea);color:var(--sea);font:700 15px/28px var(--mono);text-align:center}
.nlag .nlag-route li::after{content:"";position:absolute;right:15px;top:34px;bottom:2px;border-right:2px dotted var(--sea)}
.nlag .nlag-route li:last-child::after{display:none}
.nlag .nlag-route b{display:block;color:var(--i);font:600 15.5px/22px var(--sans)}
.nlag .nlag-route .who{font:400 12.5px/18px var(--mono);color:var(--mu)}
.nlag .nlag-route p{margin:4px 0 0;line-height:1.7}
.nlag .nlag-checks{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin:12px 0 22px}
.nlag .nlag-checks div{border:1px solid var(--ln);border-inline-start:4px solid var(--red);background:var(--w);border-radius:4px;padding:12px 14px}
.nlag .nlag-checks b{display:block;color:var(--i);font:600 15px/21px var(--sans);margin-bottom:4px}
.nlag .nlag-checks p{margin:0;line-height:1.65;font-size:14.5px}
.nlag .nlag-checks .doc{display:inline-block;margin-top:6px;font:500 12px/16px var(--mono);color:var(--sea);border:1px solid var(--sea);border-radius:2px;padding:1px 6px}
.nlag .nlag-il{border:1px solid var(--sea);background:var(--sea-t);border-radius:6px;padding:14px 16px;margin:12px 0 22px}
.nlag .nlag-il h3{margin:0 0 6px;color:var(--deep);font:600 1.05rem/1.4 var(--sans)}
.nlag .nlag-honest{border:1px dashed var(--i2);border-radius:6px;padding:14px 16px;margin:22px 0;background:var(--w)}
.nlag .nlag-honest h3{margin:0 0 6px;font:600 1rem/1.4 var(--sans);color:var(--i)}
.nlag .nlag-honest ul{margin:6px 0 0;padding-inline-start:18px;line-height:1.7}
.nlag .nlag-cluster{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:8px;margin:12px 0 22px;padding:0;list-style:none}
.nlag .nlag-cluster a{display:block;border:1px solid var(--ln);background:var(--w);border-radius:4px;padding:10px 12px;text-decoration:none;color:var(--i)}
.nlag .nlag-cluster a b{display:block;color:var(--sea);font:600 14.5px/20px var(--sans)}
.nlag .nlag-cluster a span{font-size:13px;color:var(--mu);line-height:1.5}
.nlag .nlag-cluster a:hover{border-color:var(--sea)}
.nlag .nlag-cluster a[aria-current]{background:var(--g);pointer-events:none}
.nlag .ils{color:var(--mu)}
</style>"""

ANIM = ("<script>(function(){var b=document.querySelectorAll('.nlag-bill:not(.anim)');if(!b.length||!('IntersectionObserver' in window)||(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches))return;"
        "var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('on');o.unobserve(e.target);}})},{threshold:.2});"
        "[].forEach.call(b,function(x){x.classList.add('anim');o.observe(x)});setTimeout(function(){[].forEach.call(b,function(x){x.classList.add('on')})},5000);})();</script>")


def css():
    return CSS


def ledger(items):
    """items: (label, figure, small, warn=False)"""
    out = '<div class="nlag-ledger" role="list">'
    for it in items:
        lab, fig, sm = it[:3]; warn = len(it) > 3 and it[3]
        out += '<div role="listitem"%s><span>%s</span><b>%s</b><small>%s</small></div>' % (' class="warn"' if warn else '', E(lab), E(fig), E(sm))
    return out + '</div>'


def bill(title, lines, total_label, fx=None, note=None):
    """lines: (label, sub, eur, red=False). The bars scale to the biggest line."""
    mx = max(l[2] for l in lines) or 1
    tot = sum(l[2] for l in lines)
    out = '<figure class="nlag-bill"><h3>%s</h3><ol>' % E(title)
    for l in lines:
        lab, sub, eur = l[:3]; red = len(l) > 3 and l[3]
        out += ('<li%s><span class="lb">%s%s</span><span class="bar" aria-hidden="true"><i style="--s:%.3f"></i></span>'
                '<span class="am">%s</span></li>') % (' class="red"' if red else '', E(lab), ('<small>%s</small>' % E(sub)) if sub else '', eur / mx,
                                                       '<bdi>€' + num(eur) + '</bdi>' + ('<small><bdi>₪' + num(eur * fx) + '</bdi></small>' if fx else ''))
    out += '</ol><div class="tot"><span>%s</span><b><bdi>€%s</bdi></b></div>' % (E(total_label), num(tot))
    if fx:
        out += '<p style="margin:4px 0 0;text-align:left;font:400 13px/18px var(--mono);color:var(--mu)"><bdi>₪%s</bdi></p>' % num(tot * fx)
    if note:
        out += '<figcaption style="margin-top:8px;font-size:13px;color:var(--mu);line-height:1.6">%s</figcaption>' % note
    return out + '</figure>' + ANIM


def chart(title, labels, series, series2=None, s1="", s2="", unit="", every=4, mark_last=True):
    """A line chart drawn as inline SVG (left-to-right time), plus the data as a hidden-on-wide table for readers and search."""
    W, Hh, L, R, T, B = 640, 260, 44, 14, 14, 30
    vals = [v for v in series if v is not None] + ([v for v in series2 if v is not None] if series2 else [])
    lo, hi = min(vals), max(vals); pad = (hi - lo) * .08 or 1; lo -= pad; hi += pad
    n = len(labels)
    X = lambda i: L + (W - L - R) * (i / max(1, n - 1))
    Y = lambda v: T + (Hh - T - B) * (1 - (v - lo) / (hi - lo))
    def path(s):
        d = ""; pen = False
        for i, v in enumerate(s):
            if v is None: pen = False; continue
            d += ("L" if pen else "M") + "%.1f,%.1f" % (X(i), Y(v)); pen = True
        return d
    g = '<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (W, Hh, E(title))
    for k in range(5):
        v = lo + (hi - lo) * k / 4; y = Y(v)
        g += '<line class="ax" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/><text x="4" y="%.1f">%s</text>' % (L, W - R, y, y, y + 4, num(v))
    for i, l in enumerate(labels):
        if i % every == 0 or i == n - 1:
            g += '<text x="%.1f" y="%d" text-anchor="middle">%s</text>' % (X(i), Hh - 10, E(l))
    first = next(i for i, v in enumerate(series) if v is not None)
    g += '<path class="ar" d="%sL%.1f,%.1fL%.1f,%.1fZ"/>' % (path(series), X(n - 1), Hh - B, X(first), Hh - B)
    if series2: g += '<path class="ln2" d="%s"/>' % path(series2)
    g += '<path class="ln" d="%s"/>' % path(series)
    if mark_last:
        li = max(i for i, v in enumerate(series) if v is not None)
        g += '<circle class="pt" cx="%.1f" cy="%.1f" r="4"/><text class="pl" x="%.1f" y="%.1f" text-anchor="end">%s%s</text>' % (X(li), Y(series[li]), X(li) - 6, Y(series[li]) - 8, num(series[li], 1 if series[li] < 1000 else 0), unit)
    g += '</svg>'
    key = '<p class="key"><span><i></i>%s</span>%s</p>' % (E(s1), ('<span><i class="d"></i>%s</span>' % E(s2)) if series2 else '')
    return '<figure class="nlag-chart"><h3>%s</h3>%s%s</figure>' % (E(title), g, key if s1 else '')


def table(caption, head, rows, num_cols=()):
    """rows: lists of cells (strings, may hold markup). Each cell carries its own phone label."""
    out = '<div class="nlag-tw"><table class="nlag-t"><caption>%s</caption><thead><tr>%s</tr></thead><tbody>' % (E(caption), "".join("<th>%s</th>" % E(h) for h in head))
    for r in rows:
        out += "<tr>" + "".join('<td%s><span class="l">%s:</span> %s</td>' % (' class="n"' if i in num_cols else '', E(head[i]), c) for i, c in enumerate(r)) + "</tr>"
    return out + "</tbody></table></div>"


def route(steps):
    """steps: (title, who_and_time, text)"""
    return '<ol class="nlag-route">' + "".join('<li><b>%s</b><span class="who">%s</span><p>%s</p></li>' % (E(t), E(w), x) for t, w, x in steps) + '</ol>'


def checks(items):
    """items: (risk, text, document)"""
    return '<div class="nlag-checks">' + "".join('<div><b>%s</b><p>%s</p>%s</div>' % (E(r), x, ('<span class="doc">%s</span>' % E(d)) if d else '') for r, x, d in items) + '</div>'


def israel(title, html):
    return '<aside class="nlag-il"><h3>%s</h3>%s</aside>' % (E(title), html)


def honest(title, items, asof):
    return '<aside class="nlag-honest"><h3>%s</h3><ul>%s</ul><p style="margin:8px 0 0;font:400 12.5px/18px var(--mono);color:var(--mu)">%s</p></aside>' % (E(title), "".join("<li>%s</li>" % x for x in items), E(asof))


def faq(title, qas):
    return '<h2>%s</h2>' % E(title) + "".join('<h3>%s</h3><p>%s</p>' % (E(q), a) for q, a in qas)


def cluster(items, current=None):
    """items: (href, title, line)"""
    return '<ul class="nlag-cluster">' + "".join('<li><a href="%s"%s><b>%s</b><span>%s</span></a></li>' % (E(h), ' aria-current="page"' if h == current else '', E(t), E(l)) for h, t, l in items) + '</ul>'


def bars(title, rows, unit="", note=None, hi=None):
    """Horizontal bar infographic as inline SVG (right-aligned for RTL): rows = (label, value, sub). hi = index drawn in survey red."""
    W, rowh, lab = 640, 34, 230
    mx = max(r[1] for r in rows) or 1
    Hh = rowh * len(rows) + 10
    g = '<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="direction:rtl">' % (W, Hh, E(title))
    for i, r in enumerate(rows):
        y = 6 + i * rowh; w = (W - lab - 90) * r[1] / mx
        fill = "var(--red)" if hi is not None and i == hi else "var(--sea)"
        g += '<text x="%d" y="%d" text-anchor="end" style="font:500 13px var(--sans);fill:var(--i)">%s</text>' % (W - 4, y + 17, E(r[0]))
        g += '<rect x="%d" y="%d" width="%.1f" height="16" rx="2" style="fill:%s"/>' % (W - lab - w, y + 5, w, fill)
        g += '<text x="%d" y="%d" text-anchor="end" style="font:500 12px var(--mono);fill:var(--i)">%s%s</text>' % (W - lab - w - 6, y + 17, E(r[2] if len(r) > 2 and r[2] else num(r[1])), E(unit))
    g += '</svg>'
    return '<figure class="nlag-chart"><h3>%s</h3>%s%s</figure>' % (E(title), g, ('<p class="key">%s</p>' % note) if note else '')


def timeline(title, items):
    """A dated rule timeline as inline SVG: items = (date label, text, kind) kind in {'law','plan','end'}; read right to left."""
    W, Hh = 640, 150 + 0
    n = len(items)
    g = '<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (W, Hh, E(title))
    g += '<line x1="20" x2="%d" y1="56" y2="56" style="stroke:var(--i2);stroke-width:2"/>' % (W - 20)
    for i, (d, t, k) in enumerate(items):
        x = W - 40 - i * (W - 80) / max(1, n - 1)
        col = {"law": "var(--sea)", "plan": "var(--red)", "end": "var(--deep)"}.get(k, "var(--sea)")
        g += '<circle cx="%.1f" cy="56" r="7" style="fill:%s"/>' % (x, col)
        g += '<text x="%.1f" y="36" text-anchor="middle" style="font:600 12px var(--mono);fill:var(--i)">%s</text>' % (x, E(d))
        words = t.split(" "); lines = [""]
        for w_ in words:
            if len(lines[-1]) + len(w_) > 14: lines.append(w_)
            else: lines[-1] = (lines[-1] + " " + w_).strip()
        for j, ln in enumerate(lines[:4]):
            g += '<text x="%.1f" y="%d" text-anchor="middle" style="font:500 12px var(--sans);fill:var(--i2);direction:rtl">%s</text>' % (x, 82 + j * 16, E(ln))
    g += '</svg>'
    key = '<p class="key"><span><i style="border-top-color:var(--sea)"></i>חוק בתוקף</span><span><i style="border-top-color:var(--red)"></i>הצעה, עוד לא חוק</span><span><i style="border-top-color:var(--deep)"></i>סוף תוקף</span></p>'
    return '<figure class="nlag-chart"><h3>%s</h3>%s%s</figure>' % (E(title), g, key)


def sources(items):
    """One quiet line of official sources (the research law: no citation clutter; this is the line, not footnotes)."""
    return '<p style="margin:14px 0 0;font:400 13px/20px var(--sans);color:var(--mu)">המקורות הרשמיים: ' + " · ".join('<a href="%s" rel="noopener" target="_blank" style="color:var(--sea)">%s</a>' % (E(u), E(t)) for t, u in items) + '</p>'


def wrap(inner, crumbs):
    """The page body: the trail shortcode first (it renders above the H1), then the kit's style and the content."""
    return crumbs + "\n" + CSS + '\n<div class="nlag">\n' + inner + '\n</div>'
