# -*- coding: utf-8 -*-
"""HAD-534 Mission B (Ben 15.10 + 21.10 "don't drop tasks"): the environment section for /sde-dov/contamination/ (page 8406),
from environment.md (the agent's sourced Hebrew draft) and the official wind rose (IMS Tel Aviv Coast 2410, 2016-2025).
Writes section.html next to this file. No project or company names (owner law for this page). NadLan Instruments palette:
sea #2F6F86 for wind from the sea, ink #12202A, mist #8A9AA5 for wind from the land; IBM Plex Sans Hebrew via the theme."""
import csv, io, math, os, re
H = os.path.dirname(os.path.abspath(__file__))
rows = [r for r in csv.DictReader(io.open(os.path.join(H, "windrose_sectors.csv"), encoding="utf-8")) if r["source"].startswith("IMS")]
SECT = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
pct = {(r["season"], r["sector"]): float(r["percent"]) for r in rows}
SEA = {"SW", "WSW", "W", "WNW", "NW", "NNW"}  # the shore faces west-north-west: these sectors blow in from the sea


def rose(season, title):
    cx, cy, R, top = 170, 182, 104, 16.0
    out = ['<svg viewBox="0 0 340 340" direction="ltr" role="img" aria-label="שושנת הרוחות בחוף תל אביב, %s" style="width:100%%;max-width:340px;height:auto;display:block">' % title,
           '<text x="%d" y="20" font-size="15" font-weight="700" fill="#12202A" text-anchor="middle">%s</text>' % (cx, title)]
    for k in (5, 10, 15):
        out.append('<circle cx="%d" cy="%d" r="%.1f" fill="none" stroke="#C9D3DE" stroke-width="1"/>' % (cx, cy, R * k / top))
        out.append('<text x="%d" y="%.1f" font-size="10" fill="#5B6B76" text-anchor="start">%d%%</text>' % (cx + 3, cy + R * k / top - 3, k))
    for i, sct in enumerate(SECT):
        p = pct.get((season, sct), 0.0); r = R * p / top
        a0, a1 = math.radians(i * 22.5 - 9.5), math.radians(i * 22.5 + 9.5)  # compass: 0 = north, clockwise
        x0, y0 = cx + r * math.sin(a0), cy - r * math.cos(a0); x1, y1 = cx + r * math.sin(a1), cy - r * math.cos(a1)
        col = "#2F6F86" if sct in SEA else "#8A9AA5"
        out.append('<path d="M%d %d L%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f Z" fill="%s"><title>%s: %.1f%%</title></path>' % (cx, cy, x0, y0, r, r, x1, y1, col, sct, p))
    for lab, x, y, anc in (("צפון", cx, cy - R - 10, "middle"), ("דרום", cx, cy + R + 20, "middle"), ("מזרח", cx + R + 8, cy + 4, "start"), ("מערב, הים", cx - R - 8, cy + 4, "end")):
        out.append('<text x="%d" y="%d" font-size="13" font-weight="600" fill="#12202A" text-anchor="%s">%s</text>' % (x, y, anc, lab))
    return "".join(out) + "</svg>"


def svg():
    return ('<div style="display:flex;flex-wrap:wrap;gap:12px 24px;justify-content:center">' + rose("year", "כל השנה") + rose("summer", "בקיץ") + "</div>")


md = io.open(os.path.join(H, "environment.md"), encoding="utf-8").read()
he = md[md.index("## רוח, אוויר"):]
he = re.sub(r" ב-2021 היו 97% [^.]*\.", "", he)  # off-topic line (EU statistics), dropped
html = []
for block in [b.strip() for b in he.split("\n\n") if b.strip()]:
    if block.startswith("## "):
        html.append('<h2 id="sde-dov-environment">' + block[3:].strip() + "</h2>")
    elif block.startswith("### "):
        html.append("<h3>" + block[4:].strip() + "</h3>")
        if "הרוח" in block:
            html.append('<figure class="nl-windrose" style="margin:18px 0">' + svg() + '<figcaption style="font-size:14px;color:#5B6B76;margin-top:8px">'
                        "מאיזה כיוון נושבת הרוח, באחוז מהתצפיות. בכחול: רוח שמגיעה מהים. בתחנת \"תל אביב חוף\" של השירות המטאורולוגי, 2016 עד 2025.</figcaption></figure>")
    else:
        html.append("<p>" + block + "</p>")
out = "\n".join(html)
for bad in ("זיהום", "מזוהמ", "דמרי", "גינדי", "שיכון ובינוי", "אוטופיה", "אשירה", "ריינבו"):
    assert bad not in out, bad
io.open(os.path.join(H, "section.html"), "w", encoding="utf-8", newline="\n").write(out + "\n")
print("section.html", len(out), "chars,", out.count("<h3>"), "subsections")
