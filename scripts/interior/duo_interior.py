# -*- coding: utf-8 -*-
"""DUO's example apartment from the inside, as a 360 panorama (the living room of an example apartment, "as delivered").

An example apartment, labelled so on the page: no floor plans of DUO are public, so the room is an illustration of a living
room with an open kitchen, delivered as new apartments are in Israel (light porcelain tiles, painted walls, the kitchen,
no furniture): rainbow_interior.py's bare room (8.4 m of floor-to-ceiling glass, 6.6 m deep, a kitchen run and an island,
a door on the left wall, the corridor on the right), set on a flat face of a DUO tower. rainbow_interior.py is not
changed; the DUO world comes from duo_world.py (the DUO stage's numbers). What is true in it:
  - the face: the example apartments of the DUO page sit one per face of a tower floor, on true bearings n 10, e 100,
    s 190, w 280 (inc/project-stage.php, 'duo-tel-aviv' => units); the stage puts each one in the middle of that face of
    the tower's footprint (GIS 513, oids 44499 north and 42941 south). The faces' own true bearings from the footprints:
    north tower 9.4 (n), 100.3 (e), 282.1 (w); south tower 190.4 (s). The north tower's south face looks straight at the
    south tower 28 m away, so the s apartment is on the south tower's south face (tower "auto"); n, e and w are on the
    north tower, the tower the stage opens a floor on when none is named;
  - the height: floor 25 at 87.8 m above the street and the eye at 89.4 m, the stage's floorLevel and floorEyeHeight
    (an illustration itself: no official floor height exists, the stage uses 3.3 m a floor over a 7.0 m lobby);
  - the view through the glass: the city standing today (duo/city.json: TLV GIS buildings at their recorded heights, the
    far city to the sea, streets, green areas, the city's trees), H Infinity as the stage's pale mass (duo/quarter.json),
    the coastline city.json fits through the beaches, the sea, DUO's own two towers, lobby building, commercial buildings
    and sunken courtyard as the stage draws them; the sky and the sun of a late-September afternoon (sun 11° high at 262°,
    rainbow_interior.py's 'sunset').
  - ILLUSTRATION: the room (its size, its 2.8 m ceiling, the kitchen, the finishes), the facade and the balconies (the
    stage's: a 0.42 m ledge in the middle of the north and south faces, a 2 m sun balcony in the middle of the west and
    east faces, glass balustrades).
Cycles on the CPU, fixed threads (other renders share the machine):
  blender -b --factory-startup --python scripts/interior/duo_interior.py -- <out.png> [floor 25] [bearing 280]
          [width 1536] [samples 16] [threads 6] [tower auto|N|S]
Diagnostics: DUO_PROBE="yaw:pitch,..." prints what the camera's rays hit, without rendering (DUO_EYE="x,z,h" moves the eye).
The four panoramas (the centre looks out through the glass; yaw -90 is the left wall with the door, +90 the right wall with
the opening to the corridor, 180 the kitchen); what lies ahead, in the DUO config's sector words:
  n  north tower, face 9.4    "לכיוון נמל תל אביב והירקון"   (the new municipality building's roof below, H Infinity's pale mass)
  e  north tower, face 100.3  "לכיוון כיכר המדינה"          (a 2 m sun balcony in front)
  s  south tower, face 190.4  "לכיוון כיכר רבין ומרכז העיר"
  w  north tower, face 282.1  "לכיוון הים"                 (a 2 m sun balcony in front; the sea a thin band 1.4 km away)
The low western sun glances off the glass balustrades, so the north room shows a reflected patch of sun on its back wall
(physically so: the balustrade's glass reflects at a grazing angle)."""
import math, os, sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import duo_world as W  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = ARGS[0] if ARGS else os.path.join(HERE, "_renders", "duo-living-25w.png")
FLOOR = int(ARGS[1]) if len(ARGS) > 1 else 25
BEARING = float(ARGS[2]) if len(ARGS) > 2 else 280.0
WIDTH = int(ARGS[3]) if len(ARGS) > 3 else 1536
SAMPLES = int(ARGS[4]) if len(ARGS) > 4 else 16
THREADS = int(ARGS[5]) if len(ARGS) > 5 else 6
TOWER = ARGS[6] if len(ARGS) > 6 else "auto"

CEIL = 2.8                 # net room height under a 3.3 m floor (illustration)
HALF = 4.2                 # half the window: 8.4 m of glass, as rainbow_interior.py
DEPTH = 6.6

W.init(WIDTH, SAMPLES, THREADS, exposure=-1.25, glossy=3)   # (rainbow_interior.py: -1.0; the glass balustrades let in more light)
M = W.M


def adiff(a, b):
    return abs((a - b + 540) % 360 - 180)


if TOWER == "auto":
    TOWER = "S" if adiff(BEARING, 190) <= 45 else "N"
TW = W.TOWER_BY[TOWER]


def faces_of(T):
    P, out = T["poly"], []
    for i in range(4):
        a, b = P[i], P[(i + 1) % 4]
        L = math.dist(a, b)
        tx, tz = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        nx, nz = tz, -tx
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        if (mid[0] - T["cx"]) * nx + (mid[1] - T["cz"]) * nz < 0:
            nx, nz = -nx, -nz
        out.append(dict(mid=mid, n=(nx, nz), L=L, bearing=(math.degrees(math.atan2(nx, -nz)) - math.degrees(W.G)) % 360))
    return out


FACE = min(faces_of(TW), key=lambda f: adiff(f["bearing"], BEARING))
MX, MZ = FACE["mid"]
NX, NZ = FACE["n"]                 # outward
RX, RZ = -NZ, NX                   # to the right, standing inside and looking out
Z0 = W.floor_level(FLOOR)


def P(a, b):
    """a point a metres to the right of the window's centre (looking out) and b metres inside the glass, stage-local"""
    return (MX + RX * a - NX * b, MZ + RZ * a - NZ * b)


def PB(a, b):
    x, z = P(a, b)
    return x, -z


ANG = math.atan2(-RZ, RX)          # the back wall's direction in the grid frame's Blender coordinates

# ---------------------------------------------------------------- the world outside (the DUO stage's)
W.build_ground_and_city()
W.build_lot(fine_trees=False)
W.build_towers(room=dict(tower=TOWER, y0=Z0 - 0.3, y1=Z0 + CEIL + 0.3, face=(MX, MZ, RX, RZ), half=HALF))
W.build_lobby_building()
W.build_retail()


# ---------------------------------------------------------------- the room (rainbow_interior.py's bare room)
def rmat(name, color, rough=0.5, metal=0.0, emission=None):
    return W.mat(name, color, rough, metal, emission=emission)


R = {
    "wall": rmat("wall", (0.84, 0.82, 0.78), 0.85),
    "base": rmat("baseboard", (0.74, 0.71, 0.66), 0.5),
    "door": rmat("door", (0.70, 0.64, 0.56), 0.45),
    "void": rmat("void", (0.10, 0.10, 0.10), 0.9),
    "ceil": rmat("ceiling", (0.93, 0.92, 0.90), 0.9),
    "frame": rmat("window-frame", (0.09, 0.09, 0.09), 0.35, 0.6),
    "counter": rmat("counter", (0.93, 0.92, 0.90), 0.18),
    "cabinet": rmat("cabinet", (0.80, 0.76, 0.69), 0.5),
    "cabinet_dark": rmat("cabinet_dark", (0.19, 0.19, 0.2), 0.45),
    "light": rmat("downlight", (1, 1, 1), 0.5, emission=((1.0, 0.86, 0.70), 18.0)),
}


def tile_floor():
    """120 x 60 cm porcelain tiles, warm light greige, thin grout, a soft sheen (rainbow_interior.py)"""
    m = bpy.data.materials.new("floor")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = 1.2
    br.inputs["Row Height"].default_value = 0.6
    br.inputs["Mortar Size"].default_value = 0.0025
    br.inputs["Color1"].default_value = (0.55, 0.51, 0.46, 1)
    br.inputs["Color2"].default_value = (0.57, 0.53, 0.48, 1)
    br.inputs["Mortar"].default_value = (0.40, 0.38, 0.35, 1)
    br.offset = 0.5
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.24
    return m


R["floor"] = tile_floor()


def rbox(name, a, b, z0, z1, sa, sb, material, rot=0.0):
    x, y = PB(a, b)
    return W.box(name, x, y, (z0 + z1) / 2, sa, sb, z1 - z0, material, ANG + rot)


def wall(name, pa, pb, z0, z1, material, thick=0.2):
    """a wall from stage-local point pa to pb, thick metres, centred on the line"""
    dx, dz = pb[0] - pa[0], pb[1] - pa[1]
    Ln = math.hypot(dx, dz)
    nx, nz = -dz / Ln * thick / 2, dx / Ln * thick / 2
    return W.prism_l(name, [(pa[0] - nx, pa[1] - nz), (pb[0] - nx, pb[1] - nz), (pb[0] + nx, pb[1] + nz), (pa[0] + nx, pa[1] + nz)],
                     z0, z1, material)


GL, GR = P(-HALF, 0), P(HALF, 0)               # the glass line's ends (left, right)
BL, BR = P(-HALF, DEPTH), P(HALF, DEPTH)       # the back wall's ends
room = [GL, GR, BR, BL]
W.prism_l("room-floor", room, Z0 - 0.35, Z0 + 0.01, R["floor"])
W.prism_l("room-ceiling", room, Z0 + CEIL, Z0 + CEIL + 0.4, R["ceil"])
wall("wall-left", GL, BL, Z0, Z0 + CEIL, R["wall"])
wall("wall-right", GR, BR, Z0, Z0 + CEIL, R["wall"])
wall("wall-back", BL, BR, Z0, Z0 + CEIL, R["wall"])
for nm, a_, b_ in (("left", GL, BL), ("right", GR, BR), ("back", BL, BR)):
    wall("base-" + nm, a_, b_, Z0, Z0 + 0.08, R["base"], 0.24)
rbox("door-left", -HALF, DEPTH * 0.72, Z0, Z0 + 2.2, 0.24, 0.95, R["door"])
rbox("corridor-opening", HALF, DEPTH * 0.8, Z0, Z0 + 2.3, 0.26, 1.1, R["void"])

# the glazing: floor-to-ceiling glass on the face's line, slim mullions every 1.4 m, a head and a sill profile
NOGLASS = os.environ.get("DUO_NOGLASS") == "1"
if not NOGLASS:
    W.loop_wall("glazing", [[GL[0], GL[1], 0, 0, 0], [GR[0], GR[1], 0, 0, 0]], Z0 + 0.06, Z0 + CEIL - 0.08, M["glass"], 1.4, CEIL, closed=False)
k = 0
a_ = -HALF
while a_ <= HALF + 1e-6:
    rbox("mullion-%d" % k, a_, 0.0, Z0, Z0 + CEIL, 0.06, 0.06, R["frame"])
    a_ += 2 * HALF / 6
    k += 1
rbox("window-head", 0.0, 0.0, Z0 + CEIL - 0.08, Z0 + CEIL, 2 * HALF, 0.08, R["frame"])
rbox("window-sill", 0.0, 0.0, Z0, Z0 + 0.06, 2 * HALF, 0.08, R["frame"])
# the facade over the window, up to the next floor's slab
W.loop_wall("facade-head", [[GL[0], GL[1], 0, 0, 0], [GR[0], GR[1], 0, 0, 0]], Z0 + CEIL, Z0 + W.FH - 0.46, M["facade"], 1.5, W.FH, closed=False)

# the kitchen: a run along the back wall and an island (rainbow_interior.py's)
KA, KB = -HALF + 0.55 * 2 * HALF, DEPTH - 0.33
rbox("kitchen-run", KA, KB, Z0, Z0 + 0.9, 4.2, 0.62, R["cabinet_dark"])
rbox("kitchen-top", KA, KB - 0.02, Z0 + 0.9, Z0 + 0.93, 4.26, 0.66, R["counter"])
rbox("kitchen-tall", KA + 2.55, KB, Z0, Z0 + 2.4, 0.9, 0.62, R["cabinet"])
rbox("kitchen-upper", KA - 0.3, KB, Z0 + 1.79, Z0 + 2.51, 3.4, 0.36, R["cabinet"])
rbox("island", KA, KB - 1.55, Z0, Z0 + 0.9, 2.4, 0.95, R["cabinet"])
rbox("island-top", KA, KB - 1.55, Z0 + 0.9, Z0 + 0.93, 2.5, 1.0, R["counter"])
# recessed lights in the ceiling (warm, subtle)
for i in range(3):
    for j in range(2):
        rbox("downlight-%d-%d" % (i, j), -HALF + (i + 0.5) / 3 * 2 * HALF, 1.9 + j * 2.4, Z0 + CEIL - 0.01, Z0 + CEIL, 0.09, 0.09, R["light"])

# ---------------------------------------------------------------- sky and sun: a late-September afternoon over the sea
W.sky(11, 262)
# the photographer's window pull: a soft light just inside the glass, invisible to the camera (rainbow_interior.py)
fx, fy = PB(0, 0.35)
fl = W.light("window-fill", "AREA", (fx, fy, Z0 + CEIL / 2), 380.0, (1.0, 0.95, 0.88), size=8.0, size_y=2.6, cam=False)
fl.rotation_euler = W.aim((-NX, NZ, 0.0))

# ---------------------------------------------------------------- the 360 camera: standing in the living room
W.camera()
ex, ez = P(0, 3.1)
centre = W.place_camera(ex, ez, Z0 + 1.6, NX, NZ)
d_face = math.dist((MX, MZ), (TW["cx"], TW["cz"]))
print("DUO example apartment | tower %s | floor %d, floor level %.1f m, eye %.1f m | face bearing %.1f (asked %.0f), %.1f m wide"
      % (TOWER, FLOOR, Z0, Z0 + 1.6, FACE["bearing"], BEARING, FACE["L"]))
print("panorama centre bearing %.1f: %s | yaw -90 (bearing %.1f): the left wall with the door | yaw +90 (bearing %.1f): the right "
      "wall, the opening to the corridor | behind: the kitchen" % (centre, W.sector_words(centre), (centre - 90) % 360, (centre + 90) % 360))
for yw in (-45, -30, 0, 30, 45):
    b = (centre + yw) % 360
    print("  through the glass at yaw %+d: bearing %.1f, %s" % (yw, b, W.sector_words(b)))
W.finish(OUT)
