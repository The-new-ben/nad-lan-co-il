# -*- coding: utf-8 -*-
"""HAD-376 frame check: (1) quarter.json landmarks: which frame reproduces their stated bearing from the tower;
(2) how many registry places stand inside a building of city.json in the legacy frame vs the stage frame."""
import io, json, math, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
GRID = {"rainbow": 10, "duo": 10, "dimri": 11, "ashira": 11}

def inside(poly, x, z):
    c = False; j = len(poly) - 1
    for i in range(len(poly)):
        xi, zi = poly[i]; xj, zj = poly[j]
        if (zi > z) != (zj > z) and x < (xj - xi) * (z - zi) / (zj - zi + 1e-12) + xi:
            c = not c
        j = i
    return c

for pk, g in GRID.items():
    d = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", pk)
    Q = json.load(io.open(os.path.join(d, "quarter.json"), encoding="utf-8"))
    C = json.load(io.open(os.path.join(d, "city.json"), encoding="utf-8"))
    P = json.load(io.open(os.path.join(d, "places.json"), encoding="utf-8"))
    o = (Q["origin"]["lat"], Q["origin"]["lng"]); t = (Q["tower"]["lat"], Q["tower"]["lng"])
    ke = 111320 * math.cos(math.radians(o[0]))
    def stage(lat, lng, grid, kn):
        X, Z = (lng - o[1]) * ke, -(lat - o[0]) * kn
        G = math.radians(grid); c, s = math.cos(-G), math.sin(-G)
        return X * c - Z * s, X * s + Z * c
    B = []
    for b in C["b"]:
        pts = b[3:]; poly = [(pts[i], pts[i + 1]) for i in range(0, len(pts) - 1, 2)]
        xs, zs = [p[0] for p in poly], [p[1] for p in poly]
        B.append((b[0], b[1], b[2], poly, (min(xs), min(zs), max(xs), max(zs))))
    def host(x, z):
        for h, fl, yr, poly, bb in B:
            if bb[0] <= x <= bb[2] and bb[1] <= z <= bb[3] and inside(poly, x, z):
                return (h, fl, yr)
        return None
    # (1) landmarks: bearing from the tower, computed from x/z unturned vs turned back by the grid
    print("==", pk, "grid", g, "buildings", len(B), "| city origin", C.get("origin"))
    for grid_try in (0, g):
        errs = []
        for it in Q.get("places", []):
            tx, tz = stage(t[0], t[1], grid_try, 110574)
            dx, dz = it["x"] - tx, it["z"] - tz
            G = math.radians(grid_try)   # back to true north: undo the turn
            X = dx * math.cos(G) - dz * math.sin(G); Z = dx * math.sin(G) + dz * math.cos(G)
            br = (math.degrees(math.atan2(X, -Z)) + 360) % 360
            errs.append(round(((br - it["bearing"] + 540) % 360) - 180, 1))
        print("   landmarks read in a frame turned %2d deg: bearing error vs stated %s" % (grid_try, errs))
    # (2) places inside a building
    n = len(P["places"])
    leg = sum(1 for p in P["places"] if host(p["x"], p["z"]))
    rot_old_k = sum(1 for p in P["places"] if host(*stage(p["lat"], p["lng"], g, 111320)))
    rot = sum(1 for p in P["places"] if host(*stage(p["lat"], p["lng"], g, 110574)))
    near = [p for p in P["places"] if math.hypot(p["x"], p["z"]) < 750]
    leg_n = sum(1 for p in near if host(p["x"], p["z"])); rot_n = sum(1 for p in near if host(*stage(p["lat"], p["lng"], g, 110574)))
    print("   places %d | inside a building: legacy frame %d, turned (lat 111320) %d, stage frame (turned, lat 110574) %d" % (n, leg, rot_old_k, rot))
    print("   within 750 m of the origin: %d places | inside: legacy %d, stage frame %d" % (len(near), leg_n, rot_n))
