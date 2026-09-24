# -*- coding: utf-8 -*-
"""Rainbow's lot in the stage, from its official outline (the site loop, R4b).

The stage drew lot 111 as a 104 x 80 m rectangle turned the wrong way, with the tower about 30 m from its true point. This
tool lays the lot out again from what is on record, checks the design plan's rules, and prints the stage's constants and a
plan drawing for the design system:
  - the outline: TLV GIS plan layer, feature "מגרש 111, אשכול, שדה דב" (docs/research/2026-09-24-rainbow-run/rainbow-facts.md);
  - the tower: its true point 32.10354, 34.78466 (the view and the beam already start there), in the lot's north-east corner;
  - six boutique ("textural") buildings lining the streets around a shared courtyard, 9 floors above the entrance, 8 m apart
    and 12 m from the tower, a 5 m setback toward lot 306 in the west (the approved design plan, 10.5.2023). Where exactly each
    one stands is not public: their places here follow those rules and are an illustration, as the stage's caption says.
The frame is the stage's: metres from the lot's centre (32.103168, 34.784441), turned 10 degrees like the lot, x = grid
east, z = grid south.
  python scripts/project-stage/rainbow_lot_layout.py [--svg out.svg]"""
import io, math, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ORIGIN = (32.103168, 34.784441)
GRID = math.radians(-10)
OUTLINE_LL = [(32.102477, 34.784407), (32.102551, 34.784557), (32.102705, 34.784672), (32.103667, 34.784875),
              (32.103771, 34.784774), (32.103853, 34.784265), (32.102604, 34.783994)]
TOWER_LL = (32.10354, 34.78466)
TOWER_A, TOWER_B, TOWER_ROT = 16.5, 10.8, math.radians(98)   # the stage's elliptical plan (unchanged)
BLOCK_W = 12.5
# the six boutique buildings: quadratic centre line p0 -> p1 -> p2 (p1 pulls the middle toward the courtyard)
BLOCKS = [
    ("W1", (-18.5, -62.0), (-13.5, -53.0), (-18.5, -44.0)),
    ("W2", (-18.5, -23.3), (-13.5, -14.3), (-18.5, -5.3)),
    ("W3", (-18.5, 15.4), (-13.5, 24.4), (-18.5, 33.4)),
    ("S1", (-19.4, 60.0), (-9.4, 55.0), (0.6, 60.0)),
    ("E1", (21.0, -10.0), (16.0, -1.0), (21.0, 8.0)),
    ("E2", (21.0, 28.7), (16.0, 37.7), (21.0, 46.7)),
]


def local(lat, lng):
    e = (lng - ORIGIN[1]) * math.cos(math.radians(ORIGIN[0])) * 111320.0
    n = (lat - ORIGIN[0]) * 110574.0
    X, Z = e, -n
    c, s = math.cos(GRID), math.sin(GRID)
    return (X * c - Z * s, X * s + Z * c)


def ellipse(A, B, cx, cz, rot, M=180):
    c, s = math.cos(rot), math.sin(rot)
    return [(cx + A * math.cos(t) * c - B * math.sin(t) * s, cz + A * math.cos(t) * s + B * math.sin(t) * c)
            for t in (i / M * 2 * math.pi for i in range(M))]


def capsule(p0, p1, p2, w, M=48):
    C, T = [], []
    for i in range(M + 1):
        t = i / M; u = 1 - t
        C.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))
        tx = 2 * u * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]); tz = 2 * u * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
        l = math.hypot(tx, tz) or 1
        T.append((tx / l, tz / l))
    h = w / 2; P = [(C[i][0] - T[i][1] * h, C[i][1] + T[i][0] * h) for i in range(M + 1)]
    e, t = C[M], T[M]; a0 = math.atan2(t[0], -t[1])
    P += [(e[0] + math.cos(a0 - k / 18 * math.pi) * h, e[1] + math.sin(a0 - k / 18 * math.pi) * h) for k in range(1, 18)]
    P += [(C[i][0] + T[i][1] * h, C[i][1] - T[i][0] * h) for i in range(M, -1, -1)]
    e, t = C[0], T[0]; b0 = math.atan2(-t[0], t[1])
    P += [(e[0] + math.cos(b0 - k / 18 * math.pi) * h, e[1] + math.sin(b0 - k / 18 * math.pi) * h) for k in range(1, 18)]
    return P


def seg_dist(p, a, b):
    ax, az = b[0] - a[0], b[1] - a[1]
    L = ax * ax + az * az
    t = 0 if L == 0 else max(0, min(1, ((p[0] - a[0]) * ax + (p[1] - a[1]) * az) / L))
    return math.hypot(p[0] - a[0] - t * ax, p[1] - a[1] - t * az)


def poly_gap(P, Q):
    d = min(seg_dist(p, Q[j], Q[(j + 1) % len(Q)]) for p in P for j in range(len(Q)))
    return min(d, min(seg_dist(q, P[j], P[(j + 1) % len(P)]) for q in Q for j in range(len(P))))


def inside(p, P):
    x, z = p; c = False
    for i in range(len(P)):
        a, b = P[i], P[i - 1]
        if (a[1] > z) != (b[1] > z) and x < (b[0] - a[0]) * (z - a[1]) / (b[1] - a[1]) + a[0]:
            c = not c
    return c


def edge_margin(P, lot):
    return min(seg_dist(p, lot[j], lot[(j + 1) % len(lot)]) for p in P for j in range(len(lot)))


lot = [local(*v) for v in OUTLINE_LL]
tcx, tcz = local(*TOWER_LL)
tower = ellipse(TOWER_A, TOWER_B, tcx, tcz, TOWER_ROT)
caps = [(n, capsule(p0, p1, p2, BLOCK_W)) for n, p0, p1, p2 in BLOCKS]
ok = True
print("lot outline (local):", [(round(x, 1), round(z, 1)) for x, z in lot])
print("tower centre (local): (%.1f, %.1f)" % (tcx, tcz))
print("tower inside the lot:", all(inside(p, lot) for p in tower), "| margin to the lot edge %.1f m" % edge_margin(tower, lot))
for n, P in caps:
    ins = all(inside(p, lot) for p in P)
    m = edge_margin(P, lot)
    gt = poly_gap(P, tower)
    flag = ins and gt >= 12 and m >= 1.5
    ok &= flag
    print("%s inside %s | edge margin %.1f m | to the tower %.1f m %s" % (n, ins, m, gt, "" if flag else "  <-- FAILS"))
for i in range(len(caps)):
    for j in range(i + 1, len(caps)):
        g = poly_gap(caps[i][1], caps[j][1])
        if g < 20:
            flag = g >= 8
            ok &= flag
            print("gap %s-%s %.1f m %s" % (caps[i][0], caps[j][0], g, "" if flag else "  <-- FAILS"))
west = [p for p in lot if p[0] < -25]
print("west setback (lot 306 side, 5 m): W blocks' west faces at x >= %.1f; the lot's west edge at x = %.1f" %
      (min(min(x for x, z in P) for n, P in caps if n.startswith("W")), max(x for x, z in west)))
print("ALL RULES OK" if ok else "RULES FAIL")
print("\n// stage.js constants")
print("const LOT_OUTLINE = [%s];" % ", ".join("[%.1f, %.1f]" % p for p in lot))
print("TOWER cx %.1f cz %.1f" % (tcx, tcz))

if "--svg" in sys.argv:
    out = sys.argv[sys.argv.index("--svg") + 1]
    S, pad = 3.2, 30        # pixels per metre; the drawing is grid-north up
    minx, maxx = min(x for x, z in lot) - 12, max(x for x, z in lot) + 12
    minz, maxz = min(z for x, z in lot) - 12, max(z for x, z in lot) + 12
    W, H = (maxx - minx) * S + 2 * pad, (maxz - minz) * S + 2 * pad
    f = lambda p: "%.1f,%.1f" % ((p[0] - minx) * S + pad, (p[1] - minz) * S + pad)
    path = lambda P: "M" + " L".join(f(p) for p in P) + " Z"
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="תוכנית המגרש של ריינבו, סכמטית">' % (W, H, W, H),
           '<rect width="100%" height="100%" fill="#FAF7F1"/>',
           '<path d="%s" fill="#EFEBE4" stroke="#9C7A3C" stroke-width="1.6"/>' % path(lot)]
    for n, P in caps:
        svg.append('<path d="%s" fill="#FFFFFF" stroke="#1B1A17" stroke-width="1.1"/>' % path(P))
        cx = sum(x for x, z in P) / len(P); cz = sum(z for x, z in P) / len(P)
        svg.append('<text x="%s" y="%s" font-family="Assistant,sans-serif" font-size="11" text-anchor="middle" fill="#1B1A17">%s</text>' % (f((cx, cz)).split(",")[0], float(f((cx, cz)).split(",")[1]) + 4, "בוטיק"))
    svg.append('<path d="%s" fill="#DDE6EA" stroke="#1F4B5C" stroke-width="1.4"/>' % path(tower))
    tx, tz = f((tcx, tcz)).split(",")
    svg.append('<text x="%s" y="%.1f" font-family="Assistant,sans-serif" font-size="12" font-weight="700" text-anchor="middle" fill="#1F4B5C">המגדל</text>' % (tx, float(tz) + 4))
    svg.append('<text x="%d" y="%d" font-family="Assistant,sans-serif" font-size="11" fill="#6D665C">צפון ↑ (המגרש מסובב 10° מזרחה)</text>' % (pad, pad - 10))
    bx, by = W - pad - 20 * S, H - 14
    svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1B1A17" stroke-width="2"/>' % (bx, by, bx + 20 * S, by))
    svg.append('<text x="%.1f" y="%.1f" font-family="Assistant,sans-serif" font-size="10.5" text-anchor="middle" fill="#1B1A17">20 מ׳</text>' % (bx + 10 * S, by - 5))
    svg.append("</svg>")
    io.open(out, "w", encoding="utf-8", newline="\n").write("\n".join(svg))
    print("svg:", out)
