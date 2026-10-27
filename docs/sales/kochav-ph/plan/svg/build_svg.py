# -*- coding: utf-8 -*-
"""Luxury 2D marketing plan from trace/plan.json -> plan-lux.svg (Hebrew) and plan-lux-en.svg (English).
No dimensions, no numbers, no scale bar. Every room is an addressable <g id="room-..."> for the web component.
Palette: ink #14212B, deep teal #1F4B5C, sea #2F6F86, line #E3E8EC, white rooms. Type: Noto Serif Hebrew + Assistant.
    python build_svg.py"""
import json, math, os, sys
H = os.path.dirname(os.path.abspath(__file__))
PLAN = json.load(open(os.path.join(os.path.dirname(H), "trace", "plan.json"), encoding="utf-8"))

INK, TEAL, SEA, LINE = "#14212B", "#1F4B5C", "#2F6F86", "#E3E8EC"
VB = (150, -40, 3990, 4000)   # viewBox x y w h (raster px frame)

LABEL = {  # label position, font size, optional line break / rotation (raster px frame)
    "living": ((2160, 1150), 78), "dining": ((3180, 1592), 50), "kitchen": ((2385, 2000), 70),
    "entry": ((1600, 2335), 54), "corridor": ((1357, 2690), 46), "wc": ((1140, 2585), 34),
    "room_a": ((800, 2410), 60), "bed1": ((790, 3035), 60), "bed2": ((1345, 3645), 58), "bed3": ((1765, 2905), 60),
    "closet": ((705, 3660), 50), "ensuite": ((1780, 3528), 38), "bath": ((1815, 3172), 44), "laundry": ((2118, 3200), 34),
    "ledge": ((2150, 3372), 30), "terrace": ((3745, 1640), 74), "balcony": ((2318, 2752), 28), "service": ((447, 3240), 34),
}
LABEL_EN = {"living": ((2310, 1200), 64)}
SPLIT = {"wc": True, "ensuite": True, "ledge": True}
ROT = {"service": -90, "dining": 45}

TXT = {
    "he": dict(title="מיני פנטהאוז", sub="כוכב הצפון · צפון תל אביב", sub2="חמישה חדרים · מרפסת גג עם פרגולות",
               note="הדמיה על פי תוכנית האדריכל", note2="להמחשה בלבד, ללא מידות", core="מעליות ומדרגות",
               perg="פרגולה", legend=[("stone", "אבן גדולה"), ("oak", "פרקט עץ אלון"), ("tile", "אריחים בחדרים הרטובים"), ("deck", "דק במרפסות")],
               rail="מעקה זכוכית", entry="כניסה"),
    "en": dict(title="Mini Penthouse", sub="Kochav HaTzafon · North Tel Aviv", sub2="Five rooms · roof terrace with pergolas",
               note="Illustration based on the architect's plan", note2="For illustration only, no dimensions", core="Lifts and stairs",
               perg="Pergola", legend=[("stone", "Large stone tiles"), ("oak", "Light oak floor"), ("tile", "Tiled wet rooms"), ("deck", "Terrace decking")],
               rail="Glass railing", entry="Entrance"),
}


def pts(r):
    return " ".join("%.1f,%.1f" % (x, y) for x, y in r)


def path_poly(p):
    d = "M" + " L".join("%.1f %.1f" % (x, y) for x, y in p["exterior"]) + " Z"
    for h in p.get("holes", []):
        d += " M" + " L".join("%.1f %.1f" % (x, y) for x, y in h) + " Z"
    return d


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def frame(f):
    """local frame for an oriented rectangle: centre, angle (deg) with local +y = facing, width w (across), depth h (along facing)"""
    P = f["poly"]; cx = sum(p[0] for p in P) / 4; cy = sum(p[1] for p in P) / 4
    e1 = (P[1][0] - P[0][0], P[1][1] - P[0][1]); e2 = (P[2][0] - P[1][0], P[2][1] - P[1][1])
    l1, l2 = math.hypot(*e1), math.hypot(*e2)
    fc = f.get("facing")
    if fc:
        fx, fy = fc
        # depth = edge most parallel to facing
        if abs(e1[0] * fx + e1[1] * fy) / l1 > abs(e2[0] * fx + e2[1] * fy) / l2:
            h, w = l1, l2
        else:
            h, w = l2, l1
    else:
        fx, fy = (-e2[0] / l2, -e2[1] / l2) if l2 else (0, 1)
        w, h = l1, l2
        if w < h:  # keep the long side along local x
            fx, fy = (e1[0] / l1, e1[1] / l1); w, h = l2, l1
    ang = math.degrees(math.atan2(-fx, fy))
    return cx, cy, ang, w, h


def sym(f):
    t = f["type"]; cx, cy, a, w, h = frame(f)
    g = []; W2, H2 = w / 2, h / 2
    S = 'stroke="%s" stroke-width="2.2" stroke-linejoin="round"' % INK
    if t == "sofa":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="22" fill="#fff" %s/>' % (-W2, -H2, w, h, S))
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="16" fill="%s" stroke="%s" stroke-width="1.6"/>' % (-W2 + 8, -H2 + 8, w - 16, h * 0.26, LINE, INK))
        arm = min(0.13 * w, 34)
        for sx in (-W2 + 6, W2 - 6 - arm):
            g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="12" fill="#fff" stroke="%s" stroke-width="1.6"/>' % (sx, -H2 + 8, arm, h - 16, INK))
        n = 3 if w > 2.4 * h else 2
        cw = (w - 2 * arm - 24) / n
        for k in range(n):
            x0 = -W2 + 12 + arm + k * cw
            g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="12" fill="#fff" stroke="%s" stroke-width="1.4"/>' % (x0 + 2, -H2 + h * 0.3, cw - 4, h * 0.62, INK))
    elif t == "armchair":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="40" fill="#fff" %s/>' % (-W2 + 6, -H2 + 6, w - 12, h - 12, S))
        g.append('<path d="M%.1f %.1f Q0 %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="10" stroke-linecap="round"/>' % (-W2 + 22, -H2 + h * 0.42, -H2 - 6, W2 - 22, -H2 + h * 0.42, TEAL))
    elif t == "coffee_table":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="10" fill="%s" stroke="none"/>' % (-W2 + 10, -H2 + 10, w - 20, h - 20, "#2A3A45"))
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="none" stroke="#5F7785" stroke-width="1.4"/>' % (-W2 + 22, -H2 + 22, w - 44, h - 44))
    elif t == "rug":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="#E9EEF1" stroke="#D3DCE2" stroke-width="2"/>' % (-W2, -H2, w, h))
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="none" stroke="#D3DCE2" stroke-width="1.2"/>' % (-W2 + 18, -H2 + 18, w - 36, h - 36))
    elif t == "dining_table":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="10" fill="#fff" %s/>' % (-W2, -H2, w, h, S))
        g.append('<line x1="%.1f" y1="0" x2="%.1f" y2="0" stroke="%s" stroke-width="1"/>' % (-W2 + 30, W2 - 30, LINE))
    elif t == "chair":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="14" fill="#fff" stroke="%s" stroke-width="1.8"/>' % (-W2 + 6, -H2 + 4, w - 12, h - 8, INK))
        g.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="6" stroke-linecap="round"/>' % (-W2 + 16, -H2 + 10, W2 - 16, -H2 + 10, TEAL))
    elif t == "island":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#24343F"/>' % (-W2, -H2, w, h))
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="none" stroke="#4A6070" stroke-width="1.4"/>' % (-W2 + 8, -H2 + 8, w - 16, h - 16))
    elif t == "hob":
        for dx in (-0.22, 0.22):
            for dy in (-0.22, 0.22):
                g.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#9FB4C0" stroke-width="2"/>' % (dx * w, dy * h, 0.16 * min(w, h)))
    elif t in ("counter",):
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#33454F" stroke="#5B7280" stroke-width="1.4"/>' % (-W2, -H2, w, h))
    elif t == "tall_units":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#33454F" stroke="#5B7280" stroke-width="1.4"/>' % (-W2, -H2, w, h))
        for k in range(1, 4):
            x = -W2 + k * w / 4
            g.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#5B7280" stroke-width="1.6"/>' % (x, -H2 + 6, x, H2 - 6))
    elif t == "sink":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="10" fill="#5D7280" stroke="#9FB4C0" stroke-width="1.5"/>' % (-W2, -H2, w, h))
    elif t == "feature_wall":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#5B3F2E"/>' % (-W2, -H2, w, h))
    elif t == "bed":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="10" fill="#fff" %s/>' % (-W2, -H2, w, h, S))
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="%s"/>' % (-W2, -H2, w, 16, TEAL))
        n = 2 if w > 150 else 1; pw = (w - 30 - (n - 1) * 10) / n
        for k in range(n):
            g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="14" fill="#fff" stroke="%s" stroke-width="1.5"/>' % (-W2 + 15 + k * (pw + 10), -H2 + 26, pw, 48, INK))
        g.append('<path d="M%.1f %.1f H%.1f V%.1f H%.1f Z" fill="#DCE8ED" stroke="%s" stroke-width="1.4"/>' % (-W2 + 4, H2 - h * 0.34, W2 - 4, H2 - 4, -W2 + 4, INK))
        g.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.2"/>' % (-W2 + 4, -H2 + h * 0.36, W2 - 4, -H2 + h * 0.36, INK))
    elif t == "wardrobe":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#fff" stroke="%s" stroke-width="1.8"/>' % (-W2, -H2, w, h, INK))
        g.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.2"/>' % (-W2, H2 - 10, W2, H2 - 10, SEA))
        g.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>' % (-W2, -H2, W2, H2 - 10, LINE))
    elif t == "toilet":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="#fff" stroke="%s" stroke-width="1.8"/>' % (-W2 + 4, -H2, w - 8, h * 0.3, INK))
        g.append('<ellipse cx="0" cy="%.1f" rx="%.1f" ry="%.1f" fill="#fff" stroke="%s" stroke-width="1.8"/>' % (H2 - h * 0.36, w * 0.36, h * 0.34, INK))
    elif t == "basin_round":
        g.append('<ellipse cx="0" cy="0" rx="%.1f" ry="%.1f" fill="#fff" stroke="%s" stroke-width="1.8"/>' % (W2 * 0.85, H2 * 0.7, INK))
    elif t == "vanity":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#E9E1D6" stroke="%s" stroke-width="1.6"/>' % (-W2, -H2, w, h, INK))
        g.append('<ellipse cx="0" cy="0" rx="%.1f" ry="%.1f" fill="#fff" stroke="%s" stroke-width="1.6"/>' % (min(48, W2 * 0.4), H2 * 0.62, INK))
    elif t == "bathtub":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="14" fill="#fff" %s/>' % (-W2, -H2, w, h, S))
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="30" fill="#EEF3F6" stroke="%s" stroke-width="1.2"/>' % (-W2 + 14, -H2 + 12, w - 28, h - 24, INK))
    elif t == "shower":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#EEF3F6" stroke="%s" stroke-width="1.2"/>' % (-W2, -H2, w, h, LINE))
        g.append('<path d="M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f" stroke="#C9D3DA" stroke-width="1.2"/>' % (-W2, -H2, W2, H2, W2, -H2, -W2, H2))
        g.append('<circle cx="0" cy="0" r="6" fill="none" stroke="%s" stroke-width="1.5"/>' % SEA)
    elif t == "washer":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="#fff" stroke="%s" stroke-width="1.6"/>' % (-W2 + 4, -H2 + 4, w - 8, h - 8, INK))
        g.append('<circle cx="0" cy="0" r="%.1f" fill="none" stroke="%s" stroke-width="1.6"/>' % (min(w, h) * 0.3, SEA))
    elif t == "water_heater":
        g.append('<circle cx="0" cy="0" r="%.1f" fill="#fff" stroke="%s" stroke-width="1.6"/>' % (min(w, h) * 0.45, INK))
    elif t == "ac_unit":
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#fff" stroke="%s" stroke-width="1.4"/>' % (-W2, -H2, w, h, INK))
        for k in range(1, 5):
            g.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>' % (-W2 + 8, -H2 + k * h / 5, W2 - 8, -H2 + k * h / 5, LINE))
    else:
        return ""
    return '<g transform="translate(%.1f %.1f) rotate(%.2f)">%s</g>' % (cx, cy, a, "".join(g))


def opening_svg(o, floor_fill):
    a, b = o["a"], o["b"]; dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    out = ['<polygon points="%s" fill="%s"/>' % (pts(o["poly"]), floor_fill)]
    t = o["type"]
    if t in ("window", "slider"):
        # wall thickness from the polygon
        P = o["poly"]; e = [math.hypot(P[(i + 1) % 4][0] - P[i][0], P[(i + 1) % 4][1] - P[i][1]) for i in range(4)]
        th = min(e) * 0.75
        out.append('<polygon points="%s" fill="#F4F8FA" stroke="%s" stroke-width="2"/>' % (pts(o["poly"]), SEA))
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        if t == "window":
            for k in (-0.18, 0.18):
                out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.4"/>' % (a[0] + nx * th * k, a[1] + ny * th * k, b[0] + nx * th * k, b[1] + ny * th * k, SEA))
        else:
            half = L * 0.53
            for k, s0 in ((-0.16, 0.0), (0.16, L - half)):
                x0, y0 = a[0] + ux * s0 + nx * th * k, a[1] + uy * s0 + ny * th * k
                out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="5" stroke-linecap="square"/>' % (x0, y0, x0 + ux * half, y0 + uy * half, SEA))
    else:
        hx, hy = o["hinge"]; sx, sy = o["swing"]
        # far jamb = the end of a/b farther from the hinge
        fa = a if math.hypot(a[0] - hx, a[1] - hy) > math.hypot(b[0] - hx, b[1] - hy) else b
        # project far jamb onto the hinge line along the wall
        r = math.hypot(sx - hx, sy - hy)
        vx, vy = fa[0] - hx, fa[1] - hy; vl = math.hypot(vx, vy) or 1
        ex, ey = hx + vx / vl * r, hy + vy / vl * r
        cross = (sx - hx) * (ey - hy) - (sy - hy) * (ex - hx)
        sweep = 1 if cross > 0 else 0
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (hx, hy, sx, sy, TEAL))
        out.append('<path d="M%.1f %.1f A%.1f %.1f 0 0 %d %.1f %.1f" fill="none" stroke="%s" stroke-width="1.8" stroke-dasharray="10 8"/>' % (sx, sy, r, r, sweep, ex, ey, SEA))
    return "".join(out)


def build(lang):
    T = TXT[lang]
    rooms = {r["id"]: r for r in PLAN["rooms"]}
    FILL = {"stone": "url(#pStone)", "oak": "url(#pOak)", "tile": "url(#pTile)", "deck": "url(#pDeck)"}
    BASE = {"stone": "#F6F7F7", "oak": "#F3EFEA", "tile": "#EEF1F3", "deck": "#E8ECEE"}
    o = []
    o.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%d %d %d %d" width="%d" height="%d" lang="%s" role="img" aria-label="%s">'
             % (VB + (VB[2] // 2, VB[3] // 2, "he" if lang == "he" else "en", esc(T["title"] + " - " + T["note"]))))
    o.append('<title>%s - %s</title>' % (esc(T["title"]), esc(T["note"])))
    o.append("""<defs><style>@import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&amp;family=Noto+Serif+Hebrew:wght@500;600&amp;display=swap');
 .serif{font-family:'Noto Serif Hebrew','Noto Serif',Georgia,serif} .sans{font-family:'Assistant','Segoe UI',Arial,sans-serif}
 .lbl{paint-order:stroke;stroke:#fff;stroke-width:14px;stroke-linejoin:round;fill:%s}
 .room .hl{fill:%s;fill-opacity:0;transition:fill-opacity .25s} .room.active .hl{fill-opacity:.16} .room.active .lbl{fill:%s}
</style>
<pattern id="pStone" patternUnits="userSpaceOnUse" width="189" height="189" patternTransform="rotate(45)"><rect width="189" height="189" fill="%s"/><path d="M0 0H189M0 0V189" stroke="#E3E7EA" stroke-width="2"/></pattern>
<pattern id="pOak" patternUnits="userSpaceOnUse" width="378" height="62"><rect width="378" height="62" fill="%s"/><path d="M0 0.5H378M0 31.5H378M120 0V31M310 0V31M40 31V62M230 31V62" stroke="#E6DDD3" stroke-width="1.6"/></pattern>
<pattern id="pTile" patternUnits="userSpaceOnUse" width="94" height="94"><rect width="94" height="94" fill="%s"/><path d="M0 0H94M0 0V94" stroke="#DCE2E6" stroke-width="1.5"/></pattern>
<pattern id="pDeck" patternUnits="userSpaceOnUse" width="240" height="24" patternTransform="rotate(45)"><rect width="240" height="24" fill="%s"/><path d="M0 0.5H240" stroke="#D3DADF" stroke-width="2"/><path d="M90 0V24" stroke="#DCE2E6" stroke-width="1.2"/></pattern>
<pattern id="pCore" patternUnits="userSpaceOnUse" width="26" height="26" patternTransform="rotate(45)"><rect width="26" height="26" fill="#EEF1F3"/><path d="M0 0V26" stroke="#DDE3E7" stroke-width="3"/></pattern>
<filter id="fWall" x="-5%%" y="-5%%" width="110%%" height="110%%"><feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="%s" flood-opacity=".28"/></filter>
<filter id="fFurn" x="-10%%" y="-10%%" width="120%%" height="120%%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="%s" flood-opacity=".16"/></filter>
</defs>""" % (INK, SEA, TEAL, BASE["stone"], BASE["oak"], BASE["tile"], BASE["deck"], INK, INK))
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#FFFFFF"/>' % VB)
    # building core (context only)
    o.append('<g id="core" pointer-events="none"><polygon points="%s" fill="url(#pCore)" stroke="#D3DADF" stroke-width="3"/>' % pts(PLAN["core"]["poly"]))
    cx = sum(p[0] for p in PLAN["core"]["poly"]) / 4; cy = sum(p[1] for p in PLAN["core"]["poly"]) / 4
    o.append('<text x="%.0f" y="%.0f" class="sans" font-size="44" fill="#8A9AA5" text-anchor="middle" dominant-baseline="middle">%s</text></g>' % (cx, cy, esc(T["core"])))
    # rooms
    o.append('<g id="rooms">')
    order = ["terrace", "balcony", "service", "ledge", "living", "dining", "kitchen", "entry", "corridor", "wc", "room_a", "bed1", "bed2", "bed3", "closet", "ensuite", "bath", "laundry"]
    for rid in order:
        r = rooms[rid]
        name = r["he"] if lang == "he" else r["en"]
        d = " ".join(path_poly(p) for p in r["poly"])
        o.append('<g id="room-%s" class="room" data-room="%s" data-name="%s" tabindex="0" role="button" aria-label="%s">' % (rid, rid, esc(name), esc(name)))
        o.append('<path class="floor" d="%s" fill="%s"/>' % (d, FILL[r["floor"]]))
        o.append('<path class="hl" d="%s"/>' % d)
        o.append('</g>')
    o.append('</g>')
    # pergolas (over the deck)
    o.append('<g id="pergolas" pointer-events="none">')
    for p in PLAN["pergolas"]:
        P = p["poly"]
        o.append('<polygon points="%s" fill="%s" fill-opacity=".05" stroke="%s" stroke-width="5"/>' % (pts(P), SEA, TEAL))
        # slats parallel to the living-room wall = parallel to edge P0->P1
        ax, ay = P[0]; bx, by = P[1]; cx2, cy2 = P[3]
        n = 22
        for k in range(1, n):
            t = k / n
            x0, y0 = ax + (cx2 - ax) * t, ay + (cy2 - ay) * t
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-opacity=".55" stroke-width="7"/>' % (x0, y0, x0 + bx - ax, y0 + by - ay, SEA))
    for q in PLAN["pergola_posts"]:
        o.append('<polygon points="%s" fill="%s"/>' % (pts(q), INK))
    o.append('</g>')
    # furniture + fixtures
    o.append('<g id="furniture" filter="url(#fFurn)" pointer-events="none">')
    for f in sorted(PLAN["furniture"], key=lambda f: 0 if f["type"] == "rug" else 1):
        o.append(sym(f))
    o.append('</g>')
    # parapets with glass rail
    o.append('<g id="parapets" pointer-events="none">')
    for q in PLAN["parapets"]:
        o.append('<polygon points="%s" fill="#DDEAF0" stroke="%s" stroke-width="2.5"/>' % (pts(q["poly"]), TEAL))
    o.append('</g>')
    # walls (cut), with soft shadow
    wd = " ".join(path_poly(p) for p in PLAN["walls_union_cut"])
    o.append('<g id="walls" pointer-events="none"><path d="%s" fill="%s" fill-rule="evenodd" filter="url(#fWall)"/></g>' % (wd, INK))
    # openings
    o.append('<g id="openings" pointer-events="none">')
    for op in PLAN["openings"]:
        r0 = op["rooms"][1] if op["rooms"][1] in rooms else op["rooms"][0]
        o.append(opening_svg(op, BASE[rooms[r0]["floor"]]))
    o.append('</g>')
    # entrance marker
    o.append('<g id="entrance-mark" pointer-events="none"><path d="M1118 2228 L1170 2275 L1118 2322 Z" fill="%s"/>' % TEAL)
    o.append('<text x="1090" y="2275" class="sans" font-size="40" font-weight="600" fill="%s" text-anchor="end" dominant-baseline="middle">%s</text></g>' % (TEAL, esc(T["entry"])))
    # labels
    o.append('<g id="labels" pointer-events="none">')
    for rid, ((x, y), fs) in LABEL.items():
        if lang == "en" and rid in LABEL_EN:
            (x, y), fs = LABEL_EN[rid]
        r = rooms[rid]; name = r["he"] if lang == "he" else r["en"]
        cls = "serif" if fs >= 58 else "sans"
        wt = ' font-weight="600"' if cls == "sans" else ""
        rot = ' transform="rotate(%d %d %d)"' % (ROT[rid], x, y) if rid in ROT else ""
        parts = name.split(" ", 1) if SPLIT.get(rid) and " " in name else [name]
        if len(parts) == 1:
            o.append('<text x="%d" y="%d" class="%s lbl" font-size="%d"%s text-anchor="middle" dominant-baseline="middle" data-for="%s"%s>%s</text>' % (x, y, cls, fs, wt, rid, rot, esc(name)))
        else:
            o.append('<text x="%d" y="%d" class="%s lbl" font-size="%d"%s text-anchor="middle" data-for="%s"%s><tspan x="%d" dy="-0.2em">%s</tspan><tspan x="%d" dy="1.05em">%s</tspan></text>' % (x, y, cls, fs, wt, rid, rot, x, esc(parts[0]), x, esc(parts[1])))
    for p in PLAN["pergolas"]:
        P = p["poly"]; px = sum(q[0] for q in P) / 4; py = sum(q[1] for q in P) / 4
        o.append('<text x="%.0f" y="%.0f" class="sans lbl" font-size="34" font-weight="600" fill="%s" text-anchor="middle" dominant-baseline="middle" style="fill:%s">%s</text>' % (px, py - 140, TEAL, TEAL, esc(T["perg"])))
    o.append('</g>')
    # title block (top-left empty corner) + legend (bottom-right)
    he = lang == "he"
    tx = 1650 if he else 300; anchor = "end" if he else "start"
    o.append('<g id="title" pointer-events="none">')
    o.append('<text x="%d" y="300" class="serif" font-size="150" font-weight="600" fill="%s" text-anchor="%s">%s</text>' % (tx, INK, anchor, esc(T["title"])))
    o.append('<text x="%d" y="400" class="sans" font-size="62" font-weight="600" fill="%s" text-anchor="%s">%s</text>' % (tx, TEAL, anchor, esc(T["sub"])))
    o.append('<text x="%d" y="478" class="sans" font-size="50" fill="%s" text-anchor="%s">%s</text>' % (tx, SEA, anchor, esc(T["sub2"])))
    o.append('<rect x="%d" y="525" width="520" height="5" fill="%s"/>' % (tx - 520 if he else tx, SEA))
    o.append('<text x="%d" y="600" class="sans" font-size="46" font-weight="700" fill="%s" text-anchor="%s">%s</text>' % (tx, INK, anchor, esc(T["note"])))
    o.append('<text x="%d" y="656" class="sans" font-size="38" fill="#5F7785" text-anchor="%s">%s</text>' % (tx, anchor, esc(T["note2"])))
    o.append('</g>')
    lx = 3940 if he else 3330; ly = 2640
    o.append('<g id="legend" pointer-events="none">')
    sw = {"stone": "url(#pStone)", "oak": "url(#pOak)", "tile": "url(#pTile)", "deck": "url(#pDeck)"}
    for k, (key, txt) in enumerate(T["legend"] + [("rail", T["rail"]), ("perg", T["perg"])]):
        y = ly + k * 92
        x0 = lx - 70 if he else lx
        if key in sw:
            o.append('<rect x="%d" y="%d" width="70" height="56" rx="6" fill="%s" stroke="#C9D3DA" stroke-width="2"/>' % (x0, y, sw[key]))
        elif key == "rail":
            o.append('<rect x="%d" y="%d" width="70" height="20" fill="#DDEAF0" stroke="%s" stroke-width="2.5"/>' % (x0, y + 18, TEAL))
        else:
            o.append('<rect x="%d" y="%d" width="70" height="56" fill="none" stroke="%s" stroke-width="4"/>' % (x0, y, TEAL))
            for j in range(1, 5):
                o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-opacity=".55" stroke-width="5"/>' % (x0, y + j * 11, x0 + 70, y + j * 11, SEA))
        tx2 = x0 - 26 if he else x0 + 96
        o.append('<text x="%d" y="%d" class="sans" font-size="42" fill="%s" text-anchor="%s" dominant-baseline="middle">%s</text>' % (tx2, y + 29, INK, "end" if he else "start", esc(txt)))
    o.append('</g>')
    o.append('</svg>')
    return "\n".join(o)


for lang, name in (("he", "plan-lux.svg"), ("en", "plan-lux-en.svg")):
    s = build(lang)
    open(os.path.join(H, name), "w", encoding="utf-8").write(s)
    print(name, len(s))
