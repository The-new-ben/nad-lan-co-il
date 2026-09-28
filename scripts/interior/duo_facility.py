# -*- coding: utf-8 -*-
"""DUO's shared facilities as 360 panoramas: the infinity pool on the lobby building's roof, the main lobby, and the wellness
complex with the gym and the residents' club (all ILLUSTRATIONS), in the world the DUO stage draws (duo_world.py).

What is sourced (duo/facilities.json, its Hebrew lines given here in English; docs/research/2026-09-28-stages/
stage-geometry.md, sections 3.3 and 3.4):
  - pool: "an outdoor infinity pool and a toddler pool, on the roof of the lobby building between the two residential towers"
    (the developer's site, duo-tlv.com/residential-towers); the licensing decision 1-25-0172 (21.9.2025) puts the
    residents' areas, the toddler pool and a shade pergola for the pool on residential floor 1, which fits a deck one
    level above the plaza;
  - lobby: "a main lobby about 7 m high, joining the two towers like an inner street, and a lobby on every floor" (the
    developer's site);
  - wellness: "a wellness complex with a direct entrance from the lobby, an advanced gym and a residents' club" (the
    developer's site; the floor is not published);
  - around them: the two towers (GIS 513 footprints, 50 residential floors, penthouses 48-50, technical floors 51-52), the
    three commercial buildings and the sunken courtyard in the west half (licensing decision), the lot (GIS 837), the
    city today (city.json) and H Infinity's pale mass (quarter.json), at the heights the stage draws.
What is an illustration (the stage's own illustrations, followed here, and this script's):
  - every height: the stage's 3.3 m a floor over a 7.0 m lobby (floor 1 at 8.6 m, the pool deck at 8.2 m, the towers'
    roofs at 173.6 m, their crowns at 185.8 m); the lobby building's outline (the towers' width, between them); the pool's
    place and size (the stage's POOL, 8 x 21 m along the deck's west edge, its infinity edge open to the west) and the
    toddler pool's (KIDPOOL, 4.6 x 3.6 m); the pergola's place (the stage's, 21.5-29.8 x -3.5-12.5); the loungers' line;
    the commercial buildings' shapes; the facade;
  - in this script: the pool's depth (1.2 m), its mosaic, coping and catch trough; all furniture, finishes and lights;
    the lobby's plan (the hall's glass lines are the stage's; its stone walls at the towers, the lift portals, the
    concierge desk, the lounges, the raised coffer: the hall is 6.0 m to the glass head, the stage's glass under the
    1.0 m slab that carries the pool, and 6.7 m under a central coffer, the developer's "about 7 m"); the wellness
    complex's place and plan: the stage pins the club at the north tower's base on its west side (facilityPoint 'club'),
    so the scene is that tower's ground floor in its north-west corner (its tall recessed glass, the stage's lobbyL,
    Y to floor 1): a residents' lounge with a kitchen bar, a gym behind a glass screen, a sauna.
Light: a late-September afternoon, 16:00 (sun 30° high at 246°, computed for Tel Aviv on 28.9), so the sun clears the
west commercial building the stage draws (at 11°, rainbow_interior.py's 'sunset', it would leave the deck in its shadow).
Cycles on the CPU, always FIXED threads (other renders share this machine):
  blender -b --factory-startup --python scripts/interior/duo_facility.py -- <out.png> <pool|lobby|wellness> [width 1536]
          [samples 24] [threads 6]
  (scene "aerial": a check view of the towers from the south-west with an ordinary camera, not for the page; it shows the
  towers as the stage builds them: the GIS footprints, corners eased 1.4 m, the plates' balconies deep at the corners and in
  the middle of the west and east faces. Close to a tower an equirectangular panorama bends its straight floors into arcs.)
Diagnostics: DUO_PROBE="yaw:pitch,..." (degrees from the panorama's centre) prints what the camera's rays hit, without
rendering; DUO_EYE="x,z,h" moves the eye first (stage-local metres).
What the panoramas show (true bearings; yaw = degrees right of the panorama's centre):
  pool      the eye on the deck by the pool's east coping, between two loungers (x 13.45, z 2.2, eye 9.86 m); the centre
            looks west (280, the sea's side) across the pool and over its infinity edge to the plaza, the sunken
            courtyard's trees and the west commercial building; the north tower rises at yaw +95, the south tower at -98;
            the toddler pool at +109, the pergola's lounge behind (-169); the sun at -34, 30° high.
  lobby     the eye in the middle of the hall, 1.6 m above its floor (x 15.2, z 3.1); the centre looks west (280) to the
            entrance doors, the plaza and the courtyard, between two olive trees and two lounges; the north tower's lift
            portal at yaw +97, the south tower's at -97; the concierge desk and its walnut screen behind (180), the Ben
            Saruk entrance beyond them.
  wellness  the eye in the residents' lounge (x 9.3, z -33.4, eye 2.81 m); the centre looks north (10) through the gym's
            glass screen and the tower's north glass to Givat HaMoreh's open space and the new municipality building
            (+10); the lounge and the west glass (the plaza, the north commercial building) at -90; the kitchen bar at +85;
            the long table behind (+167); the sauna at -130."""
import math, os, sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import duo_world as W  # noqa: E402
import studio_kit as SK  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = ARGS[0] if ARGS else os.path.join(HERE, "_renders", "duo-fac-pool.png")
SCENE = ARGS[1] if len(ARGS) > 1 else "pool"
WIDTH = int(ARGS[2]) if len(ARGS) > 2 else 1536
SAMPLES = int(ARGS[3]) if len(ARGS) > 3 else 24
THREADS = int(ARGS[4]) if len(ARGS) > 4 else 6
assert SCENE in ("pool", "lobby", "wellness", "aerial"), SCENE     # aerial: a check view of the towers, not a panorama

SUN_EL, SUN_AZ = 30.0, 246.0
W.init(WIDTH, SAMPLES, THREADS, exposure={"pool": -1.7, "lobby": -1.05, "wellness": -1.5, "aerial": -1.7}[SCENE], glossy=3 if SCENE == "pool" else 8)
M = W.M
Y = W.Y

# ---------------------------------------------------------------- the world (the stage's)
W.build_ground_and_city(fine_radius=90.0)       # the city's trees within 90 m drawn leaf by leaf (seen through the glass)
W.build_lot(fine_trees=True)
LOBBY_COLS = (lambda x, z: 1.5 < x < 33.0 and -12.5 < z < 18.8) if SCENE == "lobby" else None
TI = W.build_towers(clear_ground=("N",) if SCENE == "wellness" else (), skip_col=LOBBY_COLS)
if SCENE == "pool":
    W.build_lobby_building(deck=False)
elif SCENE == "lobby":
    W.build_lobby_building(glass=False)
else:
    W.build_lobby_building()
W.build_retail()
W.sky(SUN_EL, SUN_AZ, sun_energy=2.9, color=(1.0, 0.9, 0.8))
W.camera()
rnd = W.rnd


# ---------------------------------------------------------------- helpers in the stage frame (x grid east, z grid south)
def fbox(name, c, f, u, v, y0, y1, su, sv, material, bev=0.0, segs=3):
    """a box in a local frame at c facing f: u metres across (to f's right-hand side), v metres along f; su x sv wide"""
    fx, fz = f
    rx, rz = -fz, fx
    x, z = c[0] + rx * u + fx * v, c[1] + rz * u + fz * v
    ob = W.box(name, x, -z, (y0 + y1) / 2, su, sv, y1 - y0, material, math.atan2(-rz, rx))
    return SK.smooth_bevel(ob, bev, segs) if bev else ob


def fpt(c, f, u, v):
    fx, fz = f
    return c[0] - fz * u + fx * v, c[1] + fx * u + fz * v


def ccyl(name, x, z, y0, y1, r, material, seg=32, r2=None):
    return W.cyl(name, x, -z, y0, y1, r, material, seg, r2)


def cball(name, x, z, y, r, material, scale=(1, 1, 1)):
    return W.ball(name, x, -z, y, r, material, scale=scale)


def hide(ob):
    ob.hide_render = True
    return ob


def cut(target, cutter):
    md = target.modifiers.new("cut-" + cutter.name, "BOOLEAN")
    md.operation = "DIFFERENCE"
    md.object = cutter
    try:
        md.solver = "EXACT"
    except TypeError:
        pass


def sofa(name, c, f, L, fab, y0, accent=None):
    """a sofa facing f, L long: base, seat, back, arms, two cushions"""
    fbox(name + "-base", c, f, 0, 0, y0 + 0.1, y0 + 0.4, L, 0.95, fab, 0.03)
    fbox(name + "-seat", c, f, 0, 0.06, y0 + 0.4, y0 + 0.55, L - 0.2, 0.78, fab, 0.07, 4)
    fbox(name + "-back", c, f, 0, -0.36, y0 + 0.4, y0 + 0.88, L - 0.1, 0.22, fab, 0.08, 4)
    for t in (-1, 1):
        fbox("%s-arm-%d" % (name, t), c, f, t * (L / 2 - 0.1), 0, y0 + 0.1, y0 + 0.64, 0.2, 0.95, fab, 0.06, 4)
        if accent:
            fbox("%s-cushion-%d" % (name, t), c, f, t * (L / 2 - 0.55), -0.18, y0 + 0.55, y0 + 0.95, 0.46, 0.14, accent, 0.06, 4)


def armchair(name, c, f, fab, legs, y0):
    fbox(name + "-seat", c, f, 0, 0, y0 + 0.2, y0 + 0.45, 0.82, 0.82, fab, 0.07, 4)
    fbox(name + "-back", c, f, 0, -0.34, y0 + 0.4, y0 + 0.85, 0.8, 0.16, fab, 0.07, 4)
    for t in (-1, 1):
        fbox("%s-arm-%d" % (name, t), c, f, t * 0.38, 0, y0 + 0.2, y0 + 0.62, 0.12, 0.82, fab, 0.05, 4)
        for u in (-1, 1):
            fbox("%s-leg-%d-%d" % (name, t, u), c, f, t * 0.32, u * 0.32, y0, y0 + 0.2, 0.035, 0.035, legs, 0.004)


def downlight_grid(prefix, spots, yc, energy, dl_mat):
    for k, (x, z) in enumerate(spots):
        ccyl("%s-%d" % (prefix, k), x, z, yc - 0.012, yc, 0.06, dl_mat, 20)
        ccyl("%s-trim-%d" % (prefix, k), x, z, yc - 0.006, yc + 0.002, 0.085, M["frame"], 20)
        lo = W.light("%s-light-%d" % (prefix, k), "AREA", (x, -z, yc - 0.03), energy, (1.0, 0.84, 0.66), size=0.12)
        lo.data.shape = "DISK"


def glass_line(name, p0, p1, y0, y1, material=None):
    return W.loop_wall(name, [[p0[0], p0[1], 0, 0, 0], [p1[0], p1[1], 0, 0, 0]], y0, y1, material or M["glass"], 1.5, y1 - y0, closed=False)


def clip_half(poly, a, b, c):
    """the part of a polygon where a*x + b*z <= c (Sutherland-Hodgman)"""
    out = []
    n = len(poly)
    for i in range(n):
        P, Q = poly[i], poly[(i + 1) % n]
        dp, dq = a * P[0] + b * P[1] - c, a * Q[0] + b * Q[1] - c
        if dp <= 0:
            out.append(P)
        if (dp <= 0) != (dq <= 0):
            t = dp / (dp - dq)
            out.append((P[0] + (Q[0] - P[0]) * t, P[1] + (Q[1] - P[1]) * t))
    return out


def report(label, centre, marks):
    print("ILLUSTRATION %s | panorama centre bearing %.1f (%s)" % (label, centre, W.sector_words(centre)))
    for nm, b in marks:
        print("   %-34s bearing %6.1f  yaw %+6.1f" % (nm, b, W.yaw_of(b, centre)))


# ================================================================ 1. the infinity pool on the lobby building's roof
def build_pool():
    D = W.DECK_Y + 0.06                        # the deck's top, 8.26 m (the stage's deck slab)
    WL = D - 0.035                             # the water line: the infinity wall's top
    P = W.POOL
    PX0, PX1, PZ0, PZ1 = P["cx"] - P["w"] / 2, P["cx"] + P["w"] / 2, P["cz"] - P["d"] / 2, P["cz"] + P["d"] / 2   # 4.6..12.6, -7.5..13.5
    K = W.KIDPOOL
    KX0, KX1, KZ0, KZ1 = K["cx"] - K["w"] / 2, K["cx"] + K["w"] / 2, K["cz"] - K["d"] / 2, K["cz"] + K["d"] / 2
    DEPTH = 1.2
    TX0 = PX0 - 0.64                           # the catch trough's outer wall, outside the infinity edge
    deck_stone = W.stone_tiles("deck-limestone", (0.66, 0.60, 0.51), (0.6, 1.2), 0.005, 0.09, 0.58, 0.0, 1.1)
    teak = SK.wood("teak-deck", (0.30, 0.19, 0.11), (0.40, 0.27, 0.16), rough=0.5, planks=True)
    coping = W.vary(W.mat("coping", (0.80, 0.77, 0.71), 0.35), 0.06, 1.5)
    pool_tile = W.boxmap(W.tile_mat("pool-mosaic", (0.42, 0.72, 0.74), (0.47, 0.76, 0.78), (0.78, 0.80, 0.78), 0.05, 0.15))
    edge_stone = W.mat("edge-stone", (0.16, 0.17, 0.17), 0.3)
    cushion = SK.fabric("cushion", (0.80, 0.77, 0.70))
    towel = SK.fabric("towel", (0.20, 0.33, 0.40))
    canopy = SK.fabric("parasol-canvas", (0.86, 0.83, 0.76))
    W._p(canopy).inputs["Transmission Weight"].default_value = 0.25
    frame_wood = SK.wood("lounger-teak", (0.32, 0.20, 0.11), (0.42, 0.28, 0.16), rough=0.45)
    planter = W.vary(W.mat("planter-fibrecement", (0.22, 0.22, 0.21), 0.8), 0.12, 2.0)
    white_alu = W.mat("white-alu", (0.82, 0.82, 0.80), 0.35, 0.3)
    outdoor = SK.fabric("outdoor-fabric", (0.66, 0.63, 0.57))

    # --- the deck on the lobby building's roof slab (the stage's outline), cut for the two pools
    deck = W.gbox("pool-deck", W.LB_XW - 0.4, W.LB_XE + 0.4, W.LB_ZN + 0.2, W.LB_ZS - 0.2, W.DECK_Y - 0.02, D, deck_stone)
    slab = bpy.data.objects["lobby-roof-slab"]
    c1 = hide(W.gbox("pool-cutter", TX0, PX1, PZ0, PZ1, D - DEPTH - 0.5, D + 1.0, M["white"]))
    c2 = hide(W.gbox("kidpool-cutter", KX0, KX1, KZ0, KZ1, D - 0.9, D + 1.0, M["white"]))
    for ob in (deck, slab):
        cut(ob, c1)
        cut(ob, c2)
    # the glass balustrades on the open west and east edges (the stage's), a steel shoe, the stage's white cap
    for x in (W.LB_XW - 0.45, W.LB_XE + 0.45):
        glass_line("deck-balustrade-%d" % int(x), (x, W.LB_ZN + 0.3), (x, W.LB_ZS - 0.3), D, D + 1.1, M["rail-glass"])
        W.gbox("deck-shoe-%d" % int(x), x - 0.05, x + 0.05, W.LB_ZN + 0.3, W.LB_ZS - 0.3, D, D + 0.08, M["steel"])
        W.gbox("deck-cap-%d" % int(x), x - 0.06, x + 0.06, W.LB_ZN + 0.3, W.LB_ZS - 0.3, D + 1.1, D + 1.2, M["white"], 0.01)
        z = W.LB_ZN + 0.3
        while z < W.LB_ZS - 0.3:
            ccyl("deck-clamp-%d-%d" % (int(x), int(z * 10)), x, z, D, D + 1.1, 0.014, M["steel"], 8)
            z += 1.5

    # --- the pool: a mosaic basin, the infinity edge on the west into a catch trough, stone coping on three sides
    FL = WL - DEPTH
    W.gbox("pool-floor", PX0 - 0.2, PX1, PZ0, PZ1, FL - 0.05, FL, pool_tile)
    W.gbox("pool-wall-east", PX1, PX1 + 0.2, PZ0 - 0.2, PZ1 + 0.2, FL - 0.05, D - 0.03, pool_tile)
    W.gbox("pool-wall-north", TX0, PX1, PZ0 - 0.2, PZ0, FL - 0.05, D - 0.03, pool_tile)
    W.gbox("pool-wall-south", TX0, PX1, PZ1, PZ1 + 0.2, FL - 0.05, D - 0.03, pool_tile)
    W.gbox("pool-infinity-wall", PX0 - 0.2, PX0, PZ0, PZ1, FL - 0.05, WL - 0.004, edge_stone)
    W.gbox("pool-trough-floor", TX0 + 0.04, PX0 - 0.2, PZ0, PZ1, D - 0.42, D - 0.38, edge_stone)
    W.gbox("pool-trough-wall", TX0, TX0 + 0.04, PZ0, PZ1, D - 0.42, D, edge_stone)
    W.gbox("pool-water", PX0 - 0.2, PX1, PZ0, PZ1, WL - 0.02, WL, M["pool-water"])
    W.gbox("pool-trough-water", TX0 + 0.04, PX0 - 0.2, PZ0, PZ1, D - 0.34, D - 0.33, M["pool-water"])
    W.gbox("pool-sheet", PX0 - 0.215, PX0 - 0.2, PZ0, PZ1, D - 0.34, WL, M["pool-water"])     # the water falling over the edge
    W.gbox("coping-east", PX1 - 0.02, PX1 + 0.4, PZ0 - 0.4, PZ1 + 0.4, D - 0.06, D + 0.025, coping, 0.01)
    W.gbox("coping-north", TX0 - 0.02, PX1 - 0.02, PZ0 - 0.4, PZ0 + 0.02, D - 0.06, D + 0.025, coping, 0.01)
    W.gbox("coping-south", TX0 - 0.02, PX1 - 0.02, PZ1 - 0.02, PZ1 + 0.4, D - 0.06, D + 0.025, coping, 0.01)
    # steps into the pool at its south-east corner, a steel ladder at the north end, underwater lights in the east wall
    for k in range(3):
        W.gbox("pool-step-%d" % k, PX1 - 1.6, PX1, PZ1 - 0.4 * (k + 1), PZ1, FL, D - 0.3 - k * 0.33, pool_tile)
    for dx in (-0.25, 0.25):
        ccyl("ladder-%d" % int(dx * 100), P["cx"] + dx, PZ0 + 0.3, D - 1.0, D + 0.75, 0.022, M["steel"], 12)
    pool_light = W.mat("pool-light", (1, 1, 1), 0.3, emission=((0.75, 0.92, 1.0), 5.0))
    for k, z in enumerate((-3.5, 3.0, 9.5)):
        ob = ccyl("pool-light-%d" % k, PX1 - 0.06, z, FL + 0.55, FL + 0.67, 0.09, pool_light, 20)
        ob.rotation_euler = (0, math.radians(90), 0)

    # --- the toddler pool (shallow, coping all round)
    KF = WL - 0.45
    W.gbox("kid-floor", KX0, KX1, KZ0, KZ1, KF - 0.05, KF, pool_tile)
    for nm, (a, b, c, d) in (("w", (KX0 - 0.2, KX0, KZ0 - 0.2, KZ1 + 0.2)), ("e", (KX1, KX1 + 0.2, KZ0 - 0.2, KZ1 + 0.2)),
                             ("n", (KX0, KX1, KZ0 - 0.2, KZ0)), ("s", (KX0, KX1, KZ1, KZ1 + 0.2))):
        W.gbox("kid-wall-" + nm, a, b, c, d, KF - 0.05, D - 0.03, pool_tile)
    W.gbox("kid-water", KX0, KX1, KZ0, KZ1, WL - 0.02, WL, M["pool-water"])
    for nm, (a, b, c, d) in (("w", (KX0 - 0.4, KX0 + 0.02, KZ0 - 0.4, KZ1 + 0.4)), ("e", (KX1 - 0.02, KX1 + 0.4, KZ0 - 0.4, KZ1 + 0.4)),
                             ("n", (KX0 + 0.02, KX1 - 0.02, KZ0 - 0.4, KZ0 + 0.02)), ("s", (KX0 + 0.02, KX1 - 0.02, KZ1 - 0.02, KZ1 + 0.4))):
        W.gbox("kid-coping-" + nm, a, b, c, d, D - 0.06, D + 0.025, coping, 0.01)

    # --- the loungers on the stage's line (x 14.9, feet to the pool, one every 2.35 m; the one on the toddler pool left out)
    LX = P["cx"] + P["w"] / 2 + 2.3
    zs = [z for z in [PZ0 + 1.5 + 2.35 * i for i in range(12)] if z <= PZ1 - 1.2 and abs(z - K["cz"]) > K["d"] / 2 + 0.6]
    W.gbox("teak-strip", LX - 1.25, LX + 1.6, zs[0] - 0.8, zs[-1] + 0.8, D, D + 0.03, teak, 0.004)
    for i, z in enumerate(zs):
        W.gbox("lounger-frame-%d" % i, LX - 1.0, LX + 1.0, z - 0.36, z + 0.36, D + 0.26, D + 0.32, frame_wood, 0.012)
        for dx in (-0.85, 0.85):
            for dz in (-0.3, 0.3):
                W.gbox("lounger-leg-%d-%d-%d" % (i, int(dx * 10), int(dz * 10)), LX + dx - 0.03, LX + dx + 0.03, z + dz - 0.03, z + dz + 0.03,
                       D + 0.03, D + 0.26, frame_wood, 0.008)
        W.gbox("lounger-seat-%d" % i, LX - 1.0, LX + 0.3, z - 0.34, z + 0.34, D + 0.32, D + 0.41, cushion, 0.035, 4)
        tilt = math.radians(-38)
        W.obox("lounger-back-%d" % i, (LX + 0.62, -z, D + 0.55), (0.8, 0.68, 0.09), cushion, yaw=0.0, tilt=tilt, bev=0.035, segs=4)
        W.obox("lounger-backframe-%d" % i, (LX + 0.66, -z, D + 0.505), (0.84, 0.72, 0.035), frame_wood, yaw=0.0, tilt=tilt, bev=0.008)
        W.gbox("lounger-strut-%d" % i, LX + 0.9, LX + 0.95, z - 0.3, z + 0.3, D + 0.32, D + 0.72, frame_wood, 0.008)
        if i % 3 == 0:
            ob = ccyl("towel-%d" % i, LX - 0.3, z, D + 0.44 - 0.31, D + 0.44 + 0.31, 0.075, towel, 20)
            ob.rotation_euler = (math.radians(90), 0, 0)
    for i in range(0, len(zs) - 1, 2):
        zt = (zs[i] + zs[i + 1]) / 2
        ccyl("side-table-%d" % i, LX + 0.55, zt, D + 0.03, D + 0.42, 0.2, frame_wood, 28)
        ccyl("carafe-%d" % i, LX + 0.6, zt, D + 0.42, D + 0.64, 0.045, M["rail-glass"], 20)
        ccyl("parasol-base-%d" % i, LX + 1.45, zt, D, D + 0.09, 0.3, edge_stone, 24)
        ccyl("parasol-pole-%d" % i, LX + 1.45, zt, D + 0.09, D + 2.62, 0.022, white_alu, 12)
        ccyl("parasol-canopy-%d" % i, LX + 1.45, zt, D + 2.22, D + 2.58, 1.45, canopy, 10, r2=0.05)
        ccyl("parasol-finial-%d" % i, LX + 1.45, zt, D + 2.58, D + 2.66, 0.03, white_alu, 10)

    # --- the shade pergola (the stage's place and slats) over a lounge: armchairs in pairs across low tables
    px0, px1, pz0, pz1, top = 21.5, 29.8, -3.5, 12.5, W.DECK_Y + 3.3
    x = px0
    k = 0
    while x <= px1 + 0.01:
        W.gbox("pergola-slat-%d" % k, x - 0.07, x + 0.07, pz0, pz1, top - 0.3, top, white_alu, 0.004)
        x += 0.75
        k += 1
    for (x, z) in ((px0, pz0), (px1, pz0), (px0, pz1), (px1, pz1), (px0, (pz0 + pz1) / 2), (px1, (pz0 + pz1) / 2)):
        W.gbox("pergola-post-%d-%d" % (int(x), int(z)), x - 0.13, x + 0.13, z - 0.13, z + 0.13, D, top - 0.3, white_alu, 0.006)
    for z in (pz0, pz1):
        W.gbox("pergola-beam-%d" % int(z), px0 - 0.15, px1 + 0.15, z - 0.1, z + 0.1, top - 0.5, top - 0.3, white_alu, 0.004)
    W.gbox("pergola-deck", px0 + 0.3, px1 - 0.3, pz0 + 0.4, pz1 - 0.4, D, D + 0.03, teak, 0.004)
    for k, z in enumerate([pz0 + 2 + 3.2 * i for i in range(5)]):
        armchair("pergola-chair-w-%d" % k, (24.2, z), (1, 0), outdoor, frame_wood, D + 0.03)
        armchair("pergola-chair-e-%d" % k, (27.4, z), (-1, 0), outdoor, frame_wood, D + 0.03)
        ccyl("pergola-table-%d" % k, 25.8, z, D + 0.03, D + 0.4, 0.42, frame_wood, 32)
        ccyl("pergola-bowl-%d" % k, 25.8, z, D + 0.4, D + 0.48, 0.12, white_alu, 24, r2=0.08)

    # --- planters at the deck's north and south ends, by the towers (the stage's planter line): troughs of shrubs
    for side, (z0, z1) in (("n", (W.LB_ZN + 1.15, W.LB_ZN + 2.05)), ("s", (W.LB_ZS - 2.05, W.LB_ZS - 1.15))):
        W.gbox("planter-" + side, TX0, 29.2, z0, z1, D, D + 0.55, planter, 0.01)
        W.gbox("planter-soil-" + side, TX0 + 0.05, 29.15, z0 + 0.05, z1 - 0.05, D + 0.5, D + 0.51, M["soil"])
        x = TX0 + 0.3
        k = 0
        while x < 29.0:
            r_ = 0.3 + rnd.random() * 0.12
            W.shrub("shrub-%s-%d" % (side, k), x, (z0 + z1) / 2 + rnd.uniform(-0.1, 0.1), D + 0.5, r_,
                    (M["leaf"], M["leaf2"], M["leaf-olive"])[k % 3])
            x += 0.5 + rnd.random() * 0.15
            k += 1
    for i, (x, z) in enumerate(((31.0, W.LB_ZS - 2.9), (20.4, W.LB_ZN + 3.0))):
        ccyl("olive-pot-%d" % i, x, z, D, D + 0.7, 0.42, planter, 32, r2=0.36)
        ccyl("olive-soil-%d" % i, x, z, D + 0.66, D + 0.68, 0.38, M["soil"], 24)
        W.tree("olive-%d" % i, x, z, D + 0.68, 0.95, material=M["olive"], fine=True)
    # an outdoor shower at the pool's south-east corner, on a teak grate
    sx, sz = PX1 + 1.2, PZ1 + 0.9
    W.gbox("shower-grate", sx - 0.4, sx + 0.4, sz - 0.4, sz + 0.4, D, D + 0.04, teak, 0.004)
    ccyl("shower-post", sx + 0.3, sz, D + 0.04, D + 2.25, 0.035, M["steel"], 16)
    W.gbox("shower-arm", sx, sx + 0.3, sz - 0.015, sz + 0.015, D + 2.2, D + 2.23, M["steel"])
    ccyl("shower-head", sx, sz, D + 2.14, D + 2.18, 0.12, M["steel"], 24)

    # --- the camera: on the deck by the pool's east coping, between two loungers, 1.6 m above the deck; the panorama's
    # centre looks west across the pool and over its infinity edge, the two towers rising on both sides
    ex, ez = PX1 + 0.85, 2.2
    centre = W.place_camera(ex, ez, D + 1.6, -1.0, 0.0)
    N, S = W.TOWER_BY["N"], W.TOWER_BY["S"]
    report("pool: the infinity pool on the lobby building's roof (the developer), deck %.2f m, eye %.2f m, the stage's POOL 8 x 21 m"
           % (D, D + 1.6), centre,
           [("the north tower (its centre)", W.bearing_to(ex, ez, N["cx"], N["cz"])), ("the south tower (its centre)", W.bearing_to(ex, ez, S["cx"], S["cz"])),
            ("the infinity edge (grid west)", W.bearing_to(ex, ez, PX0, ez)), ("the pergola", W.bearing_to(ex, ez, 25.6, 4.5)),
            ("the toddler pool", W.bearing_to(ex, ez, K["cx"], K["cz"])), ("the sun", SUN_AZ)])


# ================================================================ 2. the main lobby, joining the two towers
def build_lobby():
    F = Y + 0.012
    X0, X1 = W.LB_XW + 0.8, W.LB_XE - 0.8        # the stage's lobby glass lines: west 3.0, east 30.8
    ZN, ZS = W.LB_ZN, W.LB_ZS                     # the towers' faces: -10.9 and 17.1
    HG = W.DECK_Y - 1.0                           # the glass head and the ceiling around the coffer: 7.2 m (6.0 m clear)
    HC = HG + 0.7                                 # the raised coffer: 7.9 m (6.7 m clear)
    CX0, CX1, CZ0, CZ1 = 9.4, 24.6, -4.5, 10.7
    XM, ZM = (X0 + X1) / 2, (ZN + ZS) / 2         # the hall's middle: 16.9, 3.1
    floor_stone = W.stone_tiles("lobby-floor", (0.44, 0.40, 0.34), (1.2, 1.2), 0.0025, 0.06, 0.26, 0.0, 0.9)
    wall_stone = W.stone_tiles("lobby-wall-stone", (0.40, 0.36, 0.31), (1.2, 2.4), 0.003, 0.06, 0.45, 0.0, 0.8)
    plaster = W.vary(W.mat("lobby-plaster", (0.83, 0.80, 0.75), 0.85), 0.05, 0.4)
    walnut = SK.wood("walnut-slat", (0.17, 0.10, 0.06), (0.26, 0.16, 0.09), rough=0.45)
    backing = W.mat("slat-backing", (0.05, 0.04, 0.035), 0.8)
    desk_stone = SK.stone("desk-travertine", (0.78, 0.72, 0.62), rough=0.32)
    desk_top = SK.wood("desk-oak", (0.46, 0.32, 0.19), (0.56, 0.40, 0.25), rough=0.35)
    sofa_fab = SK.fabric("lobby-sofa", (0.74, 0.70, 0.62))
    accent = SK.leather("lobby-leather", (0.17, 0.085, 0.045))
    rug = SK.rugmat("lobby-rug", (0.48, 0.44, 0.38))
    dark_stone = SK.stone("table-stone", (0.16, 0.15, 0.14), rough=0.25)
    pot = W.vary(W.mat("pot-stone", (0.42, 0.39, 0.35), 0.75), 0.1, 3.0)
    brass = SK.metal("brass")
    globe = SK.glow()
    W._p(globe).inputs["Emission Strength"].default_value = 9.0
    dl = W.mat("downlight", (1, 1, 1), 0.5, emission=((1.0, 0.86, 0.70), 30.0))
    cove = W.mat("cove-led", (1, 1, 1), 0.5, emission=((1.0, 0.84, 0.66), 12.0))
    black = W.mat("lobby-black", (0.03, 0.03, 0.03), 0.4, 0.8)

    # the floor; the plaster ceiling at the glass head, open over the coffer; the coffer; its cove of light
    W.gbox("lobby-floor", X0, X1, ZN, ZS, Y, F, floor_stone)
    for k, (a, b, c, d) in enumerate(((X0, CX0, ZN, ZS), (CX1, X1, ZN, ZS), (CX0, CX1, ZN, CZ0), (CX0, CX1, CZ1, ZS))):
        W.gbox("lobby-ceiling-%d" % k, a, b, c, d, HG - 0.03, HG, plaster)
    W.gbox("coffer-ceiling", CX0, CX1, CZ0, CZ1, HC, HC + 0.03, plaster)
    for k, (a, b, c, d) in enumerate(((CX0 - 0.03, CX0, CZ0, CZ1), (CX1, CX1 + 0.03, CZ0, CZ1), (CX0, CX1, CZ0 - 0.03, CZ0), (CX0, CX1, CZ1, CZ1 + 0.03))):
        W.gbox("coffer-side-%d" % k, a, b, c, d, HG - 0.03, HC, plaster)
    for k, (a, b, c, d) in enumerate(((CX0, CX0 + 0.25, CZ0, CZ1), (CX1 - 0.25, CX1, CZ0, CZ1), (CX0, CX1, CZ0, CZ0 + 0.25), (CX0, CX1, CZ1 - 0.25, CZ1))):
        W.gbox("coffer-ledge-%d" % k, a, b, c, d, HG + 0.12, HG + 0.16, plaster)
    for k, (a, b, c, d) in enumerate(((CX0 + 0.2, CX0 + 0.24, CZ0 + 0.2, CZ1 - 0.2), (CX1 - 0.24, CX1 - 0.2, CZ0 + 0.2, CZ1 - 0.2),
                                      (CX0 + 0.2, CX1 - 0.2, CZ0 + 0.2, CZ0 + 0.24), (CX0 + 0.2, CX1 - 0.2, CZ1 - 0.24, CZ1 - 0.2))):
        W.gbox("coffer-led-%d" % k, a, b, c, d, HG + 0.16, HG + 0.18, cove)
    # a ceiling of walnut slats hung inside the coffer, lit from above
    z = CZ0 + 0.35
    k = 0
    while z < CZ1 - 0.3:
        W.gbox("coffer-slat-%d" % k, CX0 + 0.35, CX1 - 0.35, z - 0.025, z + 0.025, HC - 0.34, HC - 0.26, walnut, 0.005, 2)
        z += 0.16
        k += 1
    for x in (CX0 + 0.5, (CX0 + CX1) / 2, CX1 - 0.5):
        W.gbox("coffer-slat-rail-%d" % int(x), x - 0.03, x + 0.03, CZ0 + 0.3, CZ1 - 0.3, HC - 0.26, HC - 0.22, backing)
    slab = bpy.data.objects["lobby-roof-slab"]
    cut(slab, hide(W.gbox("coffer-cutter", CX0 - 0.05, CX1 + 0.05, CZ0 - 0.05, CZ1 + 0.05, HG - 0.5, HC + 0.01, M["white"])))

    # the glass: the stage's west and east lines, slim bronze mullions every 1.5 m inside, a transom at 3.0 m, doors on the axis
    for nm, x, sgn in (("w", X0, 1), ("e", X1, -1)):
        for a, b in ((ZN, ZM - 1.3), (ZM + 1.3, ZS)):
            glass_line("lobby-glass-%s-%d" % (nm, int(a)), (x, a), (x, b), Y, HG)
        glass_line("lobby-glass-%s-over" % nm, (x, ZM - 1.3), (x, ZM + 1.3), Y + 3.05, HG)
        z = ZN + 1.5
        while z < ZS - 0.5:
            if abs(z - ZM) > 1.4:
                W.gbox("mullion-%s-%d" % (nm, int(z * 10)), x + sgn * 0.0 - 0.03 + sgn * 0.08, x + sgn * 0.08 + 0.03, z - 0.03, z + 0.03, Y, HG, M["bronze"])
            z += 1.5
        W.gbox("transom-%s" % nm, min(x, x + sgn * 0.12), max(x, x + sgn * 0.12), ZN, ZS, Y + 3.0, Y + 3.06, M["bronze"])
        # the entrance: two glass leaves in slim bronze frames under the transom, a mat inside
        for t in (-1, 1):
            zc = ZM + t * 0.62
            glass_line("door-leaf-%s-%d" % (nm, t), (x + sgn * 0.02, zc - 0.55), (x + sgn * 0.02, zc + 0.55), Y + 0.12, Y + 2.9)
            W.gbox("door-stile-%s-%d" % (nm, t), x - 0.03 + sgn * 0.02, x + 0.03 + sgn * 0.02, ZM + t * 0.035 - 0.025, ZM + t * 0.035 + 0.025, Y, Y + 2.95, M["bronze"])
            W.gbox("door-jamb-%s-%d" % (nm, t), x - 0.04, x + 0.04, ZM + t * 1.24 - 0.04, ZM + t * 1.24 + 0.04, Y, Y + 3.0, M["bronze"])
            W.gbox("door-rail-b-%s-%d" % (nm, t), x - 0.03 + sgn * 0.02, x + 0.03 + sgn * 0.02, zc - 0.58, zc + 0.58, Y, Y + 0.12, M["bronze"])
            W.gbox("door-rail-t-%s-%d" % (nm, t), x - 0.03 + sgn * 0.02, x + 0.03 + sgn * 0.02, zc - 0.58, zc + 0.58, Y + 2.9, Y + 2.95, M["bronze"])
            W.gbox("door-pull-%s-%d" % (nm, t), x + sgn * 0.12 - 0.02, x + sgn * 0.12 + 0.02, ZM + t * 0.14 - 0.02, ZM + t * 0.14 + 0.02, Y + 0.7, Y + 2.1, M["bronze"])
        W.gbox("door-mat-%s" % nm, min(x, x + sgn * 1.7), max(x, x + sgn * 1.7), ZM - 1.2, ZM + 1.2, F, F + 0.014, SK.rugmat("mat-" + nm, (0.18, 0.17, 0.16)))

    # the towers' walls at the hall's ends: stone, each with a portal into the tower's lift hall (bronze lift doors)
    PX0, PX1, PH = XM - 3.0, XM + 3.0, Y + 3.6
    for nm, zw, sgn in (("n", ZN, -1), ("s", ZS, 1)):
        zb = zw + sgn * 1.4                       # the lift hall's back wall
        zo = zw + sgn * 0.3
        W.gbox("wall-%s-a" % nm, X0 - 0.1, PX0, min(zw, zo), max(zw, zo), Y, HG, wall_stone)
        W.gbox("wall-%s-b" % nm, PX1, X1 + 0.1, min(zw, zo), max(zw, zo), Y, HG, wall_stone)
        W.gbox("wall-%s-lintel" % nm, PX0, PX1, min(zw, zo), max(zw, zo), PH, HG, wall_stone)
        x = X0 + 1.2
        while x < X1 - 0.6:                       # slim bronze reveals between the stone slabs
            if not (PX0 - 0.3 < x < PX1 + 0.3):
                W.gbox("reveal-%s-%d" % (nm, int(x * 10)), x - 0.02, x + 0.02, min(zw, zw - sgn * 0.012), max(zw, zw - sgn * 0.012), Y, HG, M["bronze"])
            x += 2.4
        W.gbox("lifthall-%s-floor" % nm, PX0, PX1, min(zw, zb), max(zw, zb), Y, F, floor_stone)
        W.gbox("lifthall-%s-ceiling" % nm, PX0, PX1, min(zw, zb), max(zw, zb), PH - 0.03, PH, plaster)
        W.gbox("lifthall-%s-back" % nm, PX0 - 0.2, PX1 + 0.2, min(zb, zb + sgn * 0.2), max(zb, zb + sgn * 0.2), Y, PH + 0.3, wall_stone)
        for t in (-1, 1):
            xs = PX0 if t < 0 else PX1
            W.gbox("lifthall-%s-side-%d" % (nm, t), min(xs, xs + t * 0.2), max(xs, xs + t * 0.2), min(zw, zb), max(zw, zb), Y, PH + 0.3, wall_stone)
        for k, xl in enumerate((XM - 1.9, XM, XM + 1.9)):
            W.gbox("lift-door-%s-%d" % (nm, k), xl - 0.55, xl + 0.55, min(zb, zb - sgn * 0.04), max(zb, zb - sgn * 0.04), Y, Y + 2.6, M["bronze"])
            W.gbox("lift-frame-%s-%d" % (nm, k), xl - 0.65, xl + 0.65, min(zb, zb - sgn * 0.05), max(zb, zb - sgn * 0.05), Y + 2.6, Y + 2.72, M["bronze"])
        W.gbox("portal-frame-%s" % nm, PX0 - 0.12, PX1 + 0.12, min(zw, zw - sgn * 0.04), max(zw, zw - sgn * 0.04), PH, PH + 0.1, M["bronze"])
        for k in range(3):
            ccyl("lifthall-%s-dl-%d" % (nm, k), XM - 1.9 + 1.9 * k, (zw + zb) / 2, PH - 0.04, PH - 0.03, 0.06, dl, 16)
            lo = W.light("lifthall-%s-light-%d" % (nm, k), "AREA", (XM - 1.9 + 1.9 * k, -(zw + zb) / 2, PH - 0.05), 30.0, (1.0, 0.84, 0.66), size=0.12)
            lo.data.shape = "DISK"
        # a bench and a canvas on each stone wall, west of the portal
        W.gbox("bench-%s" % nm, 6.0, 9.4, min(zw - sgn * 0.3, zw - sgn * 0.85), max(zw - sgn * 0.3, zw - sgn * 0.85), Y, Y + 0.45, desk_top, 0.02)
        art = SK.artmat(((0.55, 0.36, 0.22), (0.86, 0.80, 0.70), (0.30, 0.32, 0.30)) if nm == "n" else ((0.30, 0.34, 0.36), (0.88, 0.84, 0.76), (0.62, 0.46, 0.30)))
        W.gbox("art-%s" % nm, 5.8, 9.6, min(zw - sgn * 0.02, zw - sgn * 0.06), max(zw - sgn * 0.02, zw - sgn * 0.06), Y + 1.2, Y + 3.7, art, 0.004)
        W.gbox("console-%s" % nm, 23.4, 27.0, min(zw - sgn * 0.02, zw - sgn * 0.47), max(zw - sgn * 0.02, zw - sgn * 0.47), Y + 0.1, Y + 0.82, desk_stone, 0.02)
        ccyl("console-vase-%s" % nm, 24.2, zw - sgn * 0.25, Y + 0.82, Y + 1.22, 0.11, SK.paint("vase-" + nm, (0.12, 0.11, 0.1), 0.3), 32, r2=0.07)
        branch = SK.paint("branch-" + nm, (0.30, 0.24, 0.17), 0.8)
        for k in range(7):
            x_, y_ = 24.2, -(zw - sgn * 0.25)
            W.rod("twig-%s-%d" % (nm, k), (x_, y_, Y + 1.15), (x_ + rnd.uniform(-0.45, 0.45), y_ + rnd.uniform(-0.3, 0.3), Y + 1.9 + rnd.random() * 0.6),
                  0.008, 0.003, branch, 5)

    # the concierge desk behind the camera, in front of a screen of walnut slats (east of the hall's middle)
    DX = 25.4
    W.gbox("desk", DX - 0.42, DX + 0.42, ZM - 1.9, ZM + 1.9, Y, Y + 1.05, desk_stone, 0.02)
    W.gbox("desk-top", DX - 0.5, DX + 0.55, ZM - 2.0, ZM + 2.0, Y + 1.05, Y + 1.1, desk_top, 0.01)
    W.gbox("desk-screen", DX + 0.1, DX + 0.13, ZM - 0.6, ZM - 0.1, Y + 1.1, Y + 1.42, black, 0.004)
    ccyl("desk-lamp-base", DX, ZM + 1.3, Y + 1.1, Y + 1.12, 0.08, brass, 20)
    ccyl("desk-lamp-stem", DX, ZM + 1.3, Y + 1.12, Y + 1.5, 0.008, brass, 8)
    cball("desk-lamp-globe", DX, ZM + 1.3, Y + 1.56, 0.09, globe)
    SX = 27.9
    W.gbox("screen-backing", SX, SX + 0.04, ZM - 5.6, ZM + 5.6, Y, Y + 4.6, backing)
    z = ZM - 5.5
    k = 0
    while z < ZM + 5.5:
        W.gbox("screen-slat-%d" % k, SX - 0.07, SX, z - 0.0225, z + 0.0225, Y + 0.02, Y + 4.58, walnut, 0.006, 2)
        z += 0.11
        k += 1
    for k in range(8):
        zz = ZM - 4.9 + k * 1.4
        lo = W.light("screen-wash-%d" % k, "SPOT", (SX - 0.6, -zz, Y + 4.4), 70.0, (1.0, 0.8, 0.58), size=0.05)
        lo.data.spot_size = math.radians(70)
        lo.data.spot_blend = 0.6
        lo.rotation_euler = W.aim((0.6, 0.0, -3.5))

    # two lounges by the west glass, each: a rug, two sofas across a stone table, two leather armchairs, a pendant cluster
    for g, (gx, gz) in enumerate(((8.0, -5.2), (8.0, 11.4))):
        W.gbox("rug-%d" % g, gx - 2.3, gx + 2.3, gz - 1.9, gz + 1.9, F, F + 0.016, rug)
        sofa("sofa-%d-a" % g, (gx, gz - 1.3), (0, 1), 2.4, sofa_fab, F, accent)
        sofa("sofa-%d-b" % g, (gx, gz + 1.3), (0, -1), 2.4, sofa_fab, F, accent)
        armchair("chair-%d-a" % g, (gx - 2.0, gz), (1, 0), accent, brass, F)
        armchair("chair-%d-b" % g, (gx + 2.0, gz), (-1, 0), accent, brass, F)
        W.gbox("coffee-%d" % g, gx - 0.8, gx + 0.8, gz - 0.5, gz + 0.5, F, F + 0.38, dark_stone, 0.03)
        for i, c in enumerate(((0.8, 0.76, 0.68), (0.2, 0.25, 0.28), (0.55, 0.3, 0.18))):
            W.box("book-%d-%d" % (g, i), gx - 0.3, -(gz + 0.1), F + 0.395 + i * 0.035, 0.28, 0.22, 0.03, SK.paint("book-%d-%d" % (g, i), c), 0.1 * i)
        ccyl("bowl-%d" % g, gx + 0.35, gz - 0.1, F + 0.38, F + 0.48, 0.16, brass, 32, r2=0.12)
        for k, (da, db, h) in enumerate(((0, 0, 3.2), (0.5, 0.45, 3.6), (-0.45, 0.5, 3.4), (0.4, -0.5, 3.8), (-0.5, -0.4, 3.0), (0.05, 0.9, 3.9))):
            cball("pendant-%d-%d" % (g, k), gx + da, gz + db, F + h, 0.16, globe)
            ccyl("pendant-cord-%d-%d" % (g, k), gx + da, gz + db, F + h + 0.16, HG, 0.005, brass, 6)
            if k < 4:
                W.light("pendant-light-%d-%d" % (g, k), "POINT", (gx + da, -(gz + db), F + h - 0.3), 22.0, (1.0, 0.8, 0.58), size=0.1)
        ccyl("pendant-canopy-%d" % g, gx, gz, HG - 0.03, HG, 0.4, brass, 32)
    # two olive trees in stone planters flanking the hall's axis, benches beside them
    for k, zt in enumerate((ZM - 3.4, ZM + 3.4)):
        ccyl("tall-pot-%d" % k, 12.4, zt, Y, Y + 0.9, 0.62, pot, 40, r2=0.52)
        ccyl("tall-soil-%d" % k, 12.4, zt, Y + 0.86, Y + 0.88, 0.56, M["soil"], 24)
        W.tree("lobby-olive-%d" % k, 12.4, zt, Y + 0.88, 1.35, material=M["olive"], fine=True)
    # the ceiling's downlights (outside the coffer), lights in the coffer
    spots = []
    for x in [X0 + 1.4 + 2.4 * i for i in range(12)]:
        for z in [ZN + 1.4 + 2.4 * i for i in range(12)]:
            if x < X1 - 0.8 and z < ZS - 0.8 and not (CX0 - 0.4 < x < CX1 + 0.4 and CZ0 - 0.4 < z < CZ1 + 0.4) \
                    and not (abs(x - 8.0) < 2.6 and (abs(z + 5.2) < 2.2 or abs(z - 11.4) < 2.2)):
                spots.append((x, z))
    downlight_grid("lobby-dl", spots, HG - 0.03, 40.0, dl)
    for k, (x, z) in enumerate(((13.2, -0.4), (13.2, 6.6), (20.8, -0.4), (20.8, 6.6))):
        lo = W.light("coffer-light-%d" % k, "AREA", (x, -z, HC - 0.05), 90.0, (1.0, 0.86, 0.7), size=4.5)
        lo.data.shape = "DISK"
        lo = W.light("coffer-down-%d" % k, "AREA", (x, -z, HC - 0.4), 200.0, (1.0, 0.86, 0.7), size=3.0, cam=False)
        lo.data.shape = "DISK"
    for k, (a, b) in enumerate(((CX0 + 0.3, 0), (CX1 - 0.3, 0), (0, CZ0 + 0.3), (0, CZ1 - 0.3))):
        x = a if a else (CX0 + CX1) / 2
        z = b if b else (CZ0 + CZ1) / 2
        vert = bool(a)
        lo = W.light("cove-light-%d" % k, "AREA", (x, -z, HG + 0.2), 120.0, (1.0, 0.84, 0.66), size=0.2 if vert else CX1 - CX0 - 1,
                     size_y=CZ1 - CZ0 - 1 if vert else 0.2, cam=False)
        lo.rotation_euler = W.aim((0, 0, 1))

    ex, ez = XM - 1.7, ZM
    centre = W.place_camera(ex, ez, F + 1.6, -1.0, 0.0)
    report("lobby: the main lobby between the towers (the developer: about 7 m high, joining the towers); floor %.2f m, ceiling %.2f m "
           "(%.1f m clear), coffer %.2f m (%.1f m clear), eye %.2f m" % (F, HG, HG - F, HC, HC - F, F + 1.6), centre,
           [("the west entrance, the plaza, the court", W.bearing_to(ex, ez, X0, ZM)), ("the north tower's lifts", W.bearing_to(ex, ez, XM, ZN)),
            ("the south tower's lifts", W.bearing_to(ex, ez, XM, ZS)), ("the concierge desk", W.bearing_to(ex, ez, DX, ZM)),
            ("the east entrance (Ben Saruk)", W.bearing_to(ex, ez, X1, ZM)), ("the sun", SUN_AZ)])


# ================================================================ 3. the wellness complex, the gym and the residents' club
def build_wellness():
    TW = W.TOWER_BY["N"]
    lobbyL = TI["N"]["lobbyL"]                      # the tall recessed ground-floor glass (the stage's lobbyL)
    F = Y + 0.012
    CE = W.Y0 - 0.48                                # a plaster ceiling under floor 1's slab: 8.12 m (6.9 m clear)
    XE, ZSW = 15.5, -26.5                           # the complex's east wall (the core side) and south wall (the tower's lobby)
    ZG = -38.3                                      # the gym's glass screen
    poly = [(p[0], p[1]) for p in lobbyL]
    room = clip_half(clip_half(poly, 1, 0, XE), 0, 1, ZSW)
    gym = clip_half(room, 0, 1, ZG)

    def gx(z):
        """the west glass line's x at z (the lobbyL line of the tower's west face)"""
        best = None
        for i in range(len(lobbyL)):
            a, b = lobbyL[i], lobbyL[(i + 1) % len(lobbyL)]
            if a[3] < -0.8 and (a[1] - z) * (b[1] - z) <= 0 and a[1] != b[1]:
                t = (z - a[1]) / (b[1] - a[1])
                best = a[0] + (b[0] - a[0]) * t
        return best

    def gz(x):
        best = None
        for i in range(len(lobbyL)):
            a, b = lobbyL[i], lobbyL[(i + 1) % len(lobbyL)]
            if a[4] < -0.8 and (a[0] - x) * (b[0] - x) <= 0 and a[0] != b[0]:
                t = (x - a[0]) / (b[0] - a[0])
                best = a[1] + (b[1] - a[1]) * t
        return best

    oak = SK.wood("club-oak", (0.40, 0.31, 0.22), (0.50, 0.40, 0.29), scale=3.0, rough=0.36, planks=True)
    rubber = W.add_noise_bump(W.vary(W.mat("gym-rubber", (0.055, 0.055, 0.06), 0.85), 0.25, 30.0), 400.0, 0.2)
    plaster = W.vary(W.mat("club-plaster", (0.84, 0.82, 0.78), 0.85), 0.05, 0.4)
    green = SK.paint("kitchen-green", (0.16, 0.22, 0.18), 0.45)
    counter = SK.stone("club-counter", (0.86, 0.84, 0.80), rough=0.2)
    shelf_oak = SK.wood("shelf-oak", (0.46, 0.32, 0.19), (0.56, 0.40, 0.25), rough=0.4)
    table_oak = SK.wood("table-oak", (0.40, 0.26, 0.14), (0.50, 0.34, 0.20), rough=0.35)
    chair_fab = SK.fabric("club-chair", (0.62, 0.55, 0.45))
    arm_fab = SK.fabric("club-armchair", (0.30, 0.34, 0.30))
    leather = SK.leather("club-leather", (0.16, 0.08, 0.04))
    sofa_fab = SK.fabric("club-sofa", (0.70, 0.66, 0.58))
    rug = SK.rugmat("club-rug", (0.62, 0.58, 0.50))
    black = W.mat("matte-black", (0.03, 0.03, 0.03), 0.45, 0.6)
    mirror = W.mat("mirror", (0.9, 0.9, 0.9), 0.02, 1.0)
    brass = SK.metal("brass")
    globe = SK.glow()
    dl = W.mat("club-downlight", (1, 1, 1), 0.5, emission=((1.0, 0.86, 0.70), 30.0))
    strip = W.mat("led-strip", (1, 1, 1), 0.5, emission=((1.0, 0.84, 0.66), 14.0))
    pot = W.vary(W.mat("club-pot", (0.72, 0.66, 0.58), 0.8), 0.1, 3.0)
    cedar = SK.wood("sauna-cedar", (0.42, 0.26, 0.13), (0.55, 0.36, 0.19), rough=0.6)
    spa_stone = W.stone_tiles("spa-stone", (0.36, 0.34, 0.31), (0.6, 0.6), 0.003, 0.05, 0.3, 0.0, 0.8)
    lb = W.mat("gym-light", (1, 1, 1), 0.5, emission=((1.0, 0.94, 0.86), 16.0))

    # floors: oak planks in the club, rubber in the gym, stone at the sauna; the plaster ceiling; the two inner walls
    W.prism_l("club-floor", room, Y, F, oak)
    W.prism_l("gym-floor", gym, F, F + 0.004, rubber)
    W.gbox("spa-floor", gx(ZSW) - 0.3, 8.6, -30.9, ZSW, F, F + 0.006, spa_stone)
    W.prism_l("club-ceiling", room, CE - 0.02, CE, plaster)
    W.gbox("wall-east", XE, XE + 0.3, gz(XE) - 0.1, ZSW + 0.3, Y, CE, plaster)
    W.gbox("wall-south", gx(ZSW) - 0.2, XE + 0.3, ZSW, ZSW + 0.3, Y, CE, plaster)
    # the door to the main lobby (the developer: "a direct entrance from the lobby"), a glass door in a black frame
    glass_line("lobby-door", (11.6, ZSW + 0.01), (13.4, ZSW + 0.01), Y, Y + 2.7)
    W.gbox("lobby-door-frame", 11.5, 13.5, ZSW - 0.02, ZSW + 0.04, Y + 2.7, Y + 2.8, black)
    for x in (11.5, 13.45):
        W.gbox("lobby-door-jamb-%d" % int(x * 10), x, x + 0.05, ZSW - 0.02, ZSW + 0.04, Y, Y + 2.8, black)
    wall_s = bpy.data.objects["wall-south"]
    cut(wall_s, hide(W.gbox("lobby-door-cutter", 11.6, 13.4, ZSW - 0.2, ZSW + 0.5, Y - 0.1, Y + 2.7, M["white"])))
    # slim black mullions inside the tall glass, every 1.5 m on the west and north faces
    acc, last = 0.0, lobbyL[0]
    for i, p in enumerate(lobbyL):
        acc += math.dist(last[:2], p[:2])
        last = p
        if acc < 1.5:
            continue
        acc = 0.0
        if p[0] < XE - 0.2 and p[1] < ZSW - 0.2:
            ang = math.atan2(-p[4], p[3])
            W.box("mullion-%d" % i, p[0] - p[3] * 0.07, -(p[1] - p[4] * 0.07), (Y + CE) / 2, 0.12, 0.05, CE - Y, black, ang)

    # --- the gym (behind a glass screen, facing the north glass and the park): treadmills, bikes, a rack, a mirror wall
    x0g = gx(ZG) + 3.0
    glass_line("gym-screen", (x0g, ZG), (XE, ZG), Y, Y + 3.0)
    for x in [x0g + 1.5 * i for i in range(int((XE - x0g) / 1.5) + 1)]:
        W.gbox("gym-screen-post-%d" % int(x * 10), x - 0.025, x + 0.025, ZG - 0.025, ZG + 0.025, Y, Y + 3.0, black)
    W.gbox("gym-screen-head", x0g, XE, ZG - 0.03, ZG + 0.03, Y + 3.0, Y + 3.06, black)
    W.gbox("gym-mirror", XE - 0.02, XE, -43.4, ZG - 0.4, F + 0.3, F + 2.4, mirror, 0.004)
    zt = -41.3
    for k, xt in enumerate((4.6, 6.4, 8.2)):
        W.gbox("treadmill-deck-%d" % k, xt - 0.4, xt + 0.4, zt - 0.95, zt + 0.95, F, F + 0.22, black, 0.03)
        W.gbox("treadmill-belt-%d" % k, xt - 0.26, xt + 0.26, zt - 0.8, zt + 0.8, F + 0.22, F + 0.24, SK.paint("belt-%d" % k, (0.02, 0.02, 0.02), 0.7))
        for t in (-1, 1):
            W.obox("treadmill-upright-%d-%d" % (k, t), (xt + t * 0.36, -(zt - 0.85), F + 0.7), (0.07, 0.06, 1.0), black, yaw=math.pi / 2,
                   tilt=math.radians(12), bev=0.01)
        W.obox("treadmill-console-%d" % k, (xt, -(zt - 1.0), F + 1.28), (0.28, 0.72, 0.05), black, yaw=math.pi / 2, tilt=math.radians(-35), bev=0.01)
        W.obox("treadmill-screen-%d" % k, (xt, -(zt - 0.985), F + 1.295), (0.2, 0.4, 0.052), SK.paint("screen-%d" % k, (0.05, 0.08, 0.1), 0.1),
               yaw=math.pi / 2, tilt=math.radians(-35))
    for k, xb in enumerate((10.3, 11.9)):
        W.gbox("bike-base-%d" % k, xb - 0.25, xb + 0.25, zt - 0.6, zt + 0.6, F, F + 0.08, black, 0.02)
        W.obox("bike-frame-%d" % k, (xb, -zt, F + 0.5), (0.1, 0.9, 0.1), black, yaw=0, tilt=0, bev=0.01).rotation_euler = (math.radians(-50), 0, 0)
        ob = ccyl("bike-wheel-%d" % k, xb, zt - 0.45, F + 0.18, F + 0.3, 0.3, M["steel"], 32)
        ob.rotation_euler = (0, math.radians(90), 0)
        ob.location = (xb, -(zt - 0.45), F + 0.42)
        W.gbox("bike-seat-%d" % k, xb - 0.12, xb + 0.12, zt + 0.25, zt + 0.55, F + 0.95, F + 1.02, leather, 0.02)
        W.gbox("bike-post-%d" % k, xb - 0.03, xb + 0.03, zt + 0.37, zt + 0.43, F + 0.08, F + 0.95, black)
        W.gbox("bike-bar-%d" % k, xb - 0.25, xb + 0.25, zt - 0.62, zt - 0.56, F + 1.15, F + 1.19, black, 0.01)
        W.gbox("bike-stem-%d" % k, xb - 0.03, xb + 0.03, zt - 0.62, zt - 0.56, F + 0.08, F + 1.15, black)
    W.gbox("rack", XE - 0.75, XE - 0.2, -42.8, -40.0, F, F + 0.85, black, 0.01)
    for row, h in enumerate((0.45, 0.9)):
        for k in range(6):
            zb = -42.5 + k * 0.45
            rr = 0.045 + 0.008 * k
            for t in (-1, 1):
                ob = ccyl("dumbbell-%d-%d-%d" % (row, k, t), XE - 0.47 + t * 0.13, zb, F + h + rr - 0.035, F + h + rr + 0.035, rr, black, 20)
                ob.rotation_euler = (0, math.radians(90), 0)
            ob = ccyl("dumbbell-bar-%d-%d" % (row, k), XE - 0.47, zb, F + h + rr - 0.17, F + h + rr + 0.17, 0.016, M["steel"], 10)
            ob.rotation_euler = (0, math.radians(90), 0)
    W.gbox("bench-pad", 12.9, 14.1, -39.6, -39.3, F + 0.38, F + 0.48, SK.leather("bench-leather", (0.04, 0.04, 0.04)), 0.03)
    W.gbox("bench-frame", 13.0, 14.0, -39.5, -39.4, F, F + 0.38, M["steel"], 0.01)
    for k, xm in enumerate((10.0, 12.2)):
        W.gbox("yoga-mat-%d" % k, xm - 0.3, xm + 0.3, -39.9, -38.9, F + 0.004, F + 0.012, SK.paint("mat-%d" % k, (0.30, 0.38, 0.36), 0.8))
    for k in range(3):
        xl = 5.0 + k * 3.8
        W.gbox("gym-light-%d" % k, xl - 1.2, xl + 1.2, -41.4, -41.3, CE - 0.04, CE, lb)
        lo = W.light("gym-area-%d" % k, "AREA", (xl, 41.35, CE - 0.06), 180.0, (1.0, 0.94, 0.86), size=2.4, size_y=0.2, cam=False)
    ccyl("gym-pot", gx(-43.0) + 1.0, -43.2, F, F + 0.6, 0.34, pot, 32, r2=0.3)
    W.tree("gym-plant", gx(-43.0) + 1.0, -43.2, F + 0.6, 0.75, material=M["tree"], fine=True)

    # --- the residents' club: a lounge by the west glass, a kitchen bar on the east wall, a long table, a library wall
    LX, LZ = 5.9, -33.2
    W.gbox("club-rug", LX - 2.0, LX + 2.0, LZ - 2.2, LZ + 2.2, F, F + 0.014, rug)
    sofa("club-sofa", (LX, LZ + 1.6), (0, -1), 2.5, sofa_fab, F, leather)
    armchair("club-arm-a", (LX - 0.75, LZ - 1.5), (0, 1), arm_fab, brass, F)
    armchair("club-arm-b", (LX + 0.75, LZ - 1.5), (0, 1), arm_fab, brass, F)
    W.gbox("club-table", LX - 0.65, LX + 0.65, LZ - 0.4, LZ + 0.4, F, F + 0.36, SK.stone("club-table-stone", (0.30, 0.28, 0.26), rough=0.25), 0.03)
    ccyl("club-bowl", LX + 0.3, LZ, F + 0.36, F + 0.44, 0.13, brass, 32, r2=0.09)
    book_m = [SK.paint("club-book-%d" % i, c, 0.7) for i, c in enumerate(((0.62, 0.55, 0.45), (0.2, 0.24, 0.26), (0.55, 0.3, 0.18),
                                                                          (0.82, 0.78, 0.7), (0.3, 0.34, 0.3), (0.12, 0.12, 0.12)))]
    for i in range(3):
        W.box("club-tbook-%d" % i, LX - 0.2, -(LZ + 0.05), F + 0.375 + i * 0.03, 0.26, 0.2, 0.03, book_m[i], 0.12 * i)
    ccyl("floor-lamp-base", LX + 1.6, LZ + 1.6, F, F + 0.02, 0.16, brass, 24)
    ccyl("floor-lamp-pole", LX + 1.6, LZ + 1.6, F, F + 1.5, 0.012, brass, 8)
    shade = SK.fabric("club-shade", (0.93, 0.9, 0.84), 0.9)
    W._p(shade).inputs["Transmission Weight"].default_value = 0.6
    ccyl("floor-lamp-shade", LX + 1.6, LZ + 1.6, F + 1.36, F + 1.66, 0.2, shade, 32)
    W.light("floor-lamp", "POINT", (LX + 1.6, -(LZ + 1.6), F + 1.5), 45.0, (1.0, 0.8, 0.58), size=0.12)
    # a floating ceiling of oak slats over the lounge, at 4.6 m, with big globe pendants under it
    for k in range(40):
        z = LZ - 3.0 + k * 0.15
        W.gbox("club-slat-%d" % k, gx(z) + 0.9, 8.6, z - 0.025, z + 0.025, F + 4.4, F + 4.48, shelf_oak, 0.004, 2)
    for t in (-1, 1):
        W.gbox("club-slat-rail-%d" % t, gx(LZ) + 1.2 if t < 0 else 8.3, gx(LZ) + 1.26 if t < 0 else 8.36, LZ - 3.1, LZ + 3.0, F + 4.48, F + 4.52, black)
    for k, (dx, dz, h) in enumerate(((0.0, 0.0, 2.6), (0.7, 0.5, 2.9), (-0.6, 0.4, 2.75), (0.4, -0.6, 3.05))):
        cball("club-pendant-%d" % k, LX + dx, LZ + dz, F + h, 0.17, globe)
        ccyl("club-cord-%d" % k, LX + dx, LZ + dz, F + h + 0.17, F + 4.4, 0.004, brass, 6)
        W.light("club-pendant-light-%d" % k, "POINT", (LX + dx, -(LZ + dz), F + h - 0.3), 22.0, (1.0, 0.8, 0.58), size=0.1)
    # the kitchen bar on the east wall: green fronts, a stone counter, oak shelves, a fridge column; an island with stools
    KZ0, KZ1 = -37.0, -31.0
    kz = (KZ0 + KZ1) / 2
    W.gbox("kitchen-run", XE - 0.64, XE - 0.02, KZ0, KZ1, F + 0.1, F + 0.9, green, 0.006)
    W.gbox("kitchen-plinth", XE - 0.6, XE - 0.02, KZ0, KZ1, F, F + 0.1, black)
    W.gbox("kitchen-top", XE - 0.68, XE - 0.02, KZ0 - 0.02, KZ1 + 0.02, F + 0.9, F + 0.94, counter, 0.004)
    W.gbox("kitchen-splash", XE - 0.03, XE - 0.01, KZ0, KZ1, F + 0.94, F + 1.5, counter)
    for k, h in enumerate((1.75, 2.2)):
        W.gbox("kitchen-shelf-%d" % k, XE - 0.3, XE - 0.02, KZ0 + 0.3, KZ1 - 1.4, F + h, F + h + 0.04, shelf_oak, 0.004)
    W.gbox("under-shelf-led", XE - 0.29, XE - 0.27, KZ0 + 0.35, KZ1 - 1.45, F + 1.745, F + 1.75, strip)
    W.gbox("fridge-column", XE - 0.66, XE - 0.02, KZ1 - 0.02, KZ1 + 0.88, F, F + 2.3, green, 0.008)
    W.gbox("coffee-machine", XE - 0.5, XE - 0.08, KZ0 + 0.4, KZ0 + 0.76, F + 0.94, F + 1.34, M["steel"], 0.02)
    W.gbox("sink", XE - 0.54, XE - 0.12, kz + 0.3, kz + 0.9, F + 0.935, F + 0.945, M["steel"])
    ccyl("tap", XE - 0.12, kz + 0.6, F + 0.94, F + 1.25, 0.012, M["steel"], 10)
    for k in range(9):
        ccyl("jar-%d" % k, XE - 0.16, KZ0 + 0.6 + k * 0.42, F + 1.79 + (k % 2) * 0.45, F + 1.79 + (k % 2) * 0.45 + 0.12 + (k % 3) * 0.05,
             0.05 + (k % 2) * 0.015, [counter, shelf_oak, M["rail-glass"]][k % 3], 16)
    IX = XE - 2.4
    W.gbox("island", IX - 0.45, IX + 0.45, kz - 1.6, kz + 1.6, F, F + 0.95, table_oak, 0.01)
    W.gbox("island-top", IX - 0.55, IX + 0.55, kz - 1.7, kz + 1.7, F + 0.95, F + 1.0, counter, 0.006)
    for k in range(4):
        zb = kz - 1.2 + k * 0.8
        ccyl("stool-seat-%d" % k, IX - 0.85, zb, F + 0.68, F + 0.74, 0.19, leather, 28)
        ccyl("stool-pole-%d" % k, IX - 0.85, zb, F + 0.02, F + 0.68, 0.02, black, 10)
        ccyl("stool-foot-%d" % k, IX - 0.85, zb, F, F + 0.02, 0.2, black, 28)
    for k in range(3):
        cball("bar-globe-%d" % k, IX, kz - 1.0 + k * 1.0, F + 2.3, 0.13, globe)
        ccyl("bar-cord-%d" % k, IX, kz - 1.0 + k * 1.0, F + 2.43, CE, 0.004, brass, 6)
        W.light("bar-light-%d" % k, "POINT", (IX, -(kz - 1.0 + k * 1.0), F + 2.08), 22.0, (1.0, 0.8, 0.58), size=0.1)
    # the library wall on the east wall, south of the kitchen
    LB0, LB1 = -29.9, -26.9
    W.gbox("library-back", XE - 0.04, XE, LB0, LB1, F, F + 3.1, shelf_oak)
    for k in range(6):
        W.gbox("library-shelf-%d" % k, XE - 0.36, XE - 0.02, LB0, LB1, F + 0.02 + k * 0.52, F + 0.05 + k * 0.52, shelf_oak, 0.004)
    for k in range(4):
        W.gbox("library-side-%d" % k, XE - 0.36, XE - 0.02, LB0 + k * (LB1 - LB0) / 3 - 0.02, LB0 + k * (LB1 - LB0) / 3 + 0.02, F, F + 2.65, shelf_oak, 0.004)
    for sh in range(1, 5):
        zb = LB0 + 0.1
        while zb < LB1 - 0.15:
            if rnd.random() < 0.18:
                zb += 0.35
                continue
            w_ = rnd.uniform(0.025, 0.05)
            h_ = rnd.uniform(0.2, 0.3)
            W.gbox("club-book-%d-%d" % (sh, int(zb * 1000)), XE - 0.3, XE - 0.1, zb, zb + w_, F + 0.05 + sh * 0.52, F + 0.05 + sh * 0.52 + h_,
                   book_m[rnd.randrange(len(book_m))])
            zb += w_ + 0.004
    # the long table for eight under a linear pendant
    TX, TZ = 10.4, -28.6
    W.gbox("long-table", TX - 1.9, TX + 1.9, TZ - 0.5, TZ + 0.5, F + 0.72, F + 0.77, table_oak, 0.012)
    for t in (-1, 1):
        W.gbox("long-table-leg-%d" % t, TX + t * 1.6 - 0.04, TX + t * 1.6 + 0.04, TZ - 0.42, TZ + 0.42, F, F + 0.72, black, 0.006)
    for side in (-1, 1):
        for k in range(4):
            c = (TX - 1.2 + k * 0.8, TZ + side * 0.78)
            fbox("lt-seat-%d-%d" % (side, k), c, (0, -side), 0, 0, F + 0.43, F + 0.49, 0.46, 0.46, chair_fab, 0.025)
            fbox("lt-back-%d-%d" % (side, k), c, (0, -side), 0, -0.21, F + 0.49, F + 0.86, 0.44, 0.05, chair_fab, 0.02)
            for u in (-1, 1):
                for v in (-1, 1):
                    fbox("lt-leg-%d-%d-%d-%d" % (side, k, u, v), c, (0, -side), u * 0.19, v * 0.19, F, F + 0.43, 0.025, 0.025, black, 0.003)
    W.gbox("linear-pendant", TX - 1.6, TX + 1.6, TZ - 0.06, TZ + 0.06, F + 1.85, F + 1.9, black, 0.01)
    W.gbox("linear-diffuser", TX - 1.55, TX + 1.55, TZ - 0.04, TZ + 0.04, F + 1.845, F + 1.85, strip)
    for t in (-1, 1):
        ccyl("linear-cord-%d" % t, TX + t * 1.4, TZ, F + 1.9, CE, 0.004, black, 6)
    lo = W.light("table-light", "AREA", (TX, -TZ, F + 1.83), 140.0, (1.0, 0.84, 0.66), size=3.0, size_y=0.1)
    ccyl("table-vase", TX + 0.5, TZ, F + 0.77, F + 1.05, 0.07, SK.paint("vase", (0.9, 0.88, 0.84), 0.35), 20)

    # --- the wellness corner: a cedar sauna with a glass front against the south wall, a stone bench, towels, plants
    SX0, SX1, SZ0 = gx(ZSW) + 0.6, gx(ZSW) + 3.8, -29.2
    W.gbox("sauna-back", SX0, SX1, ZSW - 0.1, ZSW, F, F + 2.35, cedar)
    W.gbox("sauna-side-w", SX0, SX0 + 0.1, SZ0, ZSW, F, F + 2.35, cedar)
    W.gbox("sauna-side-e", SX1 - 0.1, SX1, SZ0, ZSW, F, F + 2.35, cedar)
    W.gbox("sauna-roof", SX0, SX1, SZ0, ZSW, F + 2.35, F + 2.45, cedar)
    glass_line("sauna-front", (SX0 + 0.1, SZ0 + 0.02), (SX1 - 0.1, SZ0 + 0.02), F, F + 2.35)
    W.gbox("sauna-door-frame", SX1 - 1.0, SX1 - 0.95, SZ0, SZ0 + 0.05, F, F + 2.1, black)
    for k, h in enumerate((0.45, 0.9)):
        W.gbox("sauna-bench-%d" % k, SX0 + 0.1, SX1 - 0.1, ZSW - 0.1 - (0.9 - k * 0.45), ZSW - 0.1, F + h - 0.05, F + h, cedar, 0.01)
    W.gbox("sauna-heater", SX0 + 0.15, SX0 + 0.55, SZ0 + 0.3, SZ0 + 0.7, F, F + 0.7, black, 0.01)
    W.light("sauna-glow", "AREA", ((SX0 + SX1) / 2, -(SZ0 + ZSW) / 2, F + 2.3), 60.0, (1.0, 0.72, 0.45), size=2.0, size_y=1.2).rotation_euler = W.aim((0, 0, -1))
    W.gbox("spa-bench", SX0 + 0.2, SX1 + 1.4, SZ0 - 1.3, SZ0 - 0.85, F, F + 0.45, SK.stone("spa-bench-stone", (0.62, 0.58, 0.52), rough=0.3), 0.02)
    for k in range(3):
        ob = ccyl("spa-towel-%d" % k, SX1 + 0.5 + k * 0.28, SZ0 - 1.07, F + 0.45 + 0.08 - 0.28, F + 0.45 + 0.08 + 0.28, 0.08,
                  SK.fabric("spa-towel-%d" % k, (0.86, 0.84, 0.8)), 20)
        ob.rotation_euler = (math.radians(90), 0, 0)
    for k, (x, z, r) in enumerate(((SX1 + 1.8, ZSW - 0.6, 0.85), (gx(-35.0) + 0.8, -36.4, 0.8))):
        ccyl("club-pot-%d" % k, x, z, F, F + 0.6, 0.34, pot, 32, r2=0.3)
        W.tree("club-plant-%d" % k, x, z, F + 0.6, r, material=M["tree"], fine=True)

    # --- the lights: downlights on the tall ceiling, a soft pull at the west glass (the photographer's)
    spots = []
    for x in [gx(-35.0) + 1.3 + 2.6 * i for i in range(6)]:
        for z in [-43.0 + 2.6 * i for i in range(7)]:
            if x < XE - 0.8 and z < ZSW - 0.8 and not (x < 8.8 and LZ - 3.2 < z < LZ + 3.1):
                spots.append((x, z))
    downlight_grid("club-dl", spots, CE, 70.0, dl)
    fl = W.light("club-fill", "AREA", (gx(-34.0) + 0.9, 34.0, F + 3.0), 220.0, (1.0, 0.95, 0.88), size=14.0, size_y=2.5, cam=False)
    fl.rotation_euler = W.aim((1.0, 0.0, 0.0))

    ex, ez = 9.3, -33.4
    centre = W.place_camera(ex, ez, F + 1.6, 0.0, -1.0)
    report("wellness: the wellness complex, the gym and the residents' club (the developer; the floor is not published), placed at the "
           "north tower's base on its west side as the stage pins the club; floor %.2f m, ceiling %.2f m (%.1f m clear), eye %.2f m"
           % (F, CE, CE - F, F + 1.6), centre,
           [("the gym and the north glass (the park)", W.bearing_to(ex, ez, ex, -42.0)), ("the west glass (the plaza)", W.bearing_to(ex, ez, gx(ez), ez)),
            ("the lounge", W.bearing_to(ex, ez, LX, LZ)), ("the kitchen bar", W.bearing_to(ex, ez, XE, kz)),
            ("the sauna", W.bearing_to(ex, ez, (SX0 + SX1) / 2, SZ0)), ("the long table", W.bearing_to(ex, ez, TX, TZ)),
            ("the municipality building (GIS 513)", W.bearing_to(ex, ez, 20.3, -96.2)), ("the sun", SUN_AZ)])


def build_aerial():
    """a check view (not for the page): a perspective camera from the south-west, above the plaza, like the stage's poster"""
    cd = bpy.data.cameras.new("aerial")
    cd.lens = 32
    cd.clip_end = 60000.0
    ob = bpy.data.objects.new("aerial", cd)
    bpy.context.collection.objects.link(ob)
    ob.parent = W.SITE
    import mathutils
    eye, tgt = mathutils.Vector((-150.0, -120.0, 120.0)), mathutils.Vector((17.0, -2.0, 70.0))   # grid-frame Blender coordinates
    ob.location = eye
    ob.rotation_euler = (tgt - eye).to_track_quat("-Z", "Y").to_euler()
    W.scene.camera = ob
    W.CAM = ob


{"pool": build_pool, "lobby": build_lobby, "wellness": build_wellness, "aerial": build_aerial}[SCENE]()
W.finish(os.path.abspath(OUT))
