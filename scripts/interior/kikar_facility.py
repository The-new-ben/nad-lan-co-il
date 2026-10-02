# -*- coding: utf-8 -*-
"""Kikar Hamedina's shared facilities as 360 panoramas: the lobby of tower C, the residents' pool, the gym, the spa and the
residents' parking level (all ILLUSTRATIONS, "המקום להמחשה"), for the project page's 360 viewer
(assets/project-stage/world/example.js 'fac' scenes).

  blender -b --factory-startup --python scripts/interior/kikar_facility.py -- <out.png> <lobby|pool|gym|spa|parking>
          [width 4096] [samples 96] [threads 12]
  (an equirectangular 360, height = width / 2; Cycles on the CPU, FIXED threads: other renders share this machine)
Env: KF_TOD=day|sunset (the lobby's hour, kikar_world.TIMES; default sunset), KF_EXP (an exposure offset), KF_PULL (the
lobby glass's window pull), KF_EYE="x,y,z" (moves the eye, room-local metres). Diagnostics, no render:
KF_PROBE="yaw:pitch,..." prints what the camera's rays hit; KF_LOCATE="name,..." prints objects' centres as yaw:pitch (as
DUO_PROBE / DUO_LOCATE in duo_world.py). Every render also prints its REPORT and DOOR lines (the doors' yaws, for the
building walk).

What is SOURCED (docs/research/2026-09-30-kikar-hamedina/facts.md 1.4, 1.6, 1.8, 1.9, 1.12):
  - the pool, the gym, the spa, treatment rooms and multi-purpose halls are on ONE OF THE BASEMENT LEVELS (Ashtrom:
    "באחת מקומות המרתף ייבנו בריכה, חדר כושר, מתחם ספא, חדרי טיפולים ואולמות רב תכליתיים"; newhomesisrael: "Basement pool,
    gym, spa"). So the pool and the gym have no window, no daylight, no sky and no view: every light in them is
    architectural and artificial (coves, linear lights, downlights, the pool's underwater lights, and a backlit onyx wall
    that is plainly a lit stone panel, never a window);
  - a lobby with a security guard (Sotheby's listing): the concierge desk;
  - tower C as the shared world draws it (kikar_world.py, world.json): its place and size (the municipal footprint), the
    superellipse plate (n 4.5), floor 1's turn (31.86 degrees, so the plate's south-west side faces 211.9 degrees, the
    square's park), 4.0 m a floor (provisional), the white curtain wall with white aluminium (MYS; Alum Eshet), the round
    slip-formed core (Ashtrom, CivilEng; its 5.2 m radius is kikar_interior.py's, not published); and around the lobby
    the real world of kikar_world.py: the square's park and its ecological pond (the world's outlines), towers A and B,
    the city at its surveyed heights, the city's canopy trees (their places and radii), the sun of 21.9.2026 at 17:36
    Israel time (at that hour the square's western blocks already shade the ground at the tower's base: true, kept).
What is an ILLUSTRATION (no plan, finish or render of these rooms is published):
  - every room's size, plan, height and place. The lobby takes tower C's whole ground floor (floor 1's glass line) and is
    double height: floor 2's slab is left out, 7.05 m clear under the ceiling, the glass rising to floor 3's slab (a
    listing's "floor 4 is like floor 7 because of the high lobby" is only a claim). The main entrance on the plate's
    north-west side, the concierge desk, the lounges, the three lift portals on the core's south-west face (29 lifts in
    the project; how many are in tower C's core is not published), the round coffer and the floor's ring;
  - the basement level: -1 here, its floor 6.0 m below the street (3 parking levels are published, the facilities'
    level is not). The pool hall (15 x 28.5 m, 4.8 m clear) and the gym (11 x 18 m, 3.6 m clear) under tower C and its
    south-west plaza, turned with floor 1's plate;
  - the pool: 20 x 7.5 m, 1.4 m deep, a deck-level edge, three lanes marked on its floor, steps across the near end;
  - every finish, furnishing, piece of equipment, plant and light; the terrace and plaza at the tower's base; the lawn's
    and the pond's surfaces (their outlines are the world's); the form of the trees' crowns within 320 m of the lobby's eye
    (built leaf by leaf from 8 crown variants; beyond, kikar_world's own crowns).
What the panoramas show (yaw = degrees right of the panorama's centre, pitch up; the script prints them, REPORT and DOOR):
  lobby  the eye 1.6 m above the lobby's floor (2.07 m above the street), 8.6 m south-west of the core's centre and 0.75 m
         right of its axis, between two mullions; the centre looks 211.9 (the plate's south-west glass) over the terrace
         and the park's lawn to the pond (yaw -5.6) and tower A beyond it (yaw -0.1); tower B at -47.2; the lounge at
         -69.3, the concierge desk at -107.0; the sun of 17:36 at +50.9 (12.7 degrees high); DOORS: the main entrance (the
         north-west glass doors) +106.4, the lift portals on the round core -145.2, -168.5 and +161.5.
  pool   the eye 1.6 m above the deck, 1.1 m before the pool's near end, on its axis; the centre looks down the 20 m pool
         (211.9) to the backlit onyx (yaw 0); the loungers on the right (+28), the stone bench on the left (-32); DOOR: the
         entrance's glass door +121.8.
  gym    the eye 1.6 m above the rubber floor, 4.0 m from the door wall; the centre looks down the turf lane (211.9) to the
         power rack on its platform (yaw 0); the treadmills facing the moss wall on the left (-48), the dumbbells before the
         mirror wall on the right (+53); DOOR: the entrance's glass door -135.0.
  spa    (added 2.10.2026) the eye 1.6 m above the stone floor, 4.0 m from the door wall; the centre looks down the room
         (211.9) to the sauna's glass front in the far wall (yaw 0); the relaxation loungers before the basalt wall on the
         right, the planter of olives in the middle, the treatment rooms' doors along the oak wall on the left, the
         reception's counter and backlit onyx behind (left). The REPORT and DOOR lines give the yaws.
  parking (added 2.10.2026) the eye 1.6 m above the slab, in the drive aisle 2.4 m past the vestibule's pedestrian
         crossing; the centre looks down the aisle (211.9) between the columns and the marked bays to four generic parked
         cars (18-32 m); the lift vestibule's glass doors behind on the left, the storage rooms' doors on the walls behind.
         The REPORT and DOOR lines give the yaws.

The spa and the parking level (2.10.2026), SOURCED (facts.md 1.6, 1.9):
  - the spa: "מתחם ספא, חדרי טיפולים" on one of the basement levels, with the pool and the gym (Ashtrom); so it is a
    basement room like them: no window, no daylight, every light artificial;
  - the parking: 1,620 spaces on 3 underground levels (Ashtrom); 1,626 = 906 private for the apartment owners + 720
    public (Globes 14.12.2022, Mako 24.9.2026); two private spaces per unit and a storage room (ICE 2022, listings). So the
    level shown is the RESIDENTS' private parking (no sign, label or number says so or says anything else): underground,
    artificial light, columns, marked bays, a lift vestibule with glass doors at tower C's round core, storage-room doors.
  ILLUSTRATED (nothing of these rooms is published): the spa's place (beside the pool hall, opposite the gym, on the
  same level -1, the gym's plan mirrored), its size (11 x 16 m, 3.4 m clear), plan, the reception, the loungers, the
  planter, the three treatment-room doors, the sauna and every finish, fitting and light. The parking's level (-2; a search
  snippet, source unidentified, says levels -1 and -2 are private), its floor 9.6 m below the street (3.6 m under level
  -1's), its 3.1 m soffit, the column grid (8.1 m), the bays (2.5 x 5.0 m), the 6 m aisle, the vestibule, the storage
  doors and every finish and light; the four parked cars are generic shapes (no make, no badge, no plate), no EV charger,
  no sign, no number anywhere."""
import math
import os
import random
import sys

import bmesh
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kikar_world as KW  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = os.path.abspath(ARGS[0]) if ARGS else os.path.join(HERE, "_renders", "kikar", "fac-test.png")
SCENE = ARGS[1] if len(ARGS) > 1 else "lobby"
WIDTH = int(ARGS[2]) if len(ARGS) > 2 else 4096
SAMPLES = int(ARGS[3]) if len(ARGS) > 3 else 96
THREADS = int(ARGS[4]) if len(ARGS) > 4 else 12
if SCENE not in ("lobby", "pool", "gym", "spa", "parking"):
    raise SystemExit("kikar_facility: scene must be lobby | pool | gym | spa | parking, not %r" % SCENE)
TODN = os.environ.get("KF_TOD", "sunset")
DEG = math.pi / 180.0
rnd = random.Random({"lobby": 11, "pool": 22, "gym": 33, "spa": 55, "parking": 44}[SCENE])

KW.init(WIDTH, WIDTH // 2, SAMPLES, THREADS)
KW.sky_params(TODN)
KW.load_world()
T = KW.W["towers"]["C"]
MOD = KW.W["model"]
NEXP = MOD.get("plate_n", 4.5)
HALF = T["side"] / 2
AG = HALF - MOD["slab_out"]                      # the glass line's half size (15.05 m)
TH1 = KW.plate_at(T, 1)                          # floor 1's plate (31.86 degrees)
FACE = (TH1 + 180.0) % 360.0                     # the plate's south-west side: the park (211.86)
CT = KW.tower_xy(T)
FWD, RIGHT = KW.dirv(FACE), KW.dirv(FACE + 90.0)
RC = 5.2                                         # the round core's radius (kikar_interior.py; not published)
FF = MOD["slab_t"] + 0.02                        # the lobby's finished floor: floor 1's slab top + the stone (0.47 m)
BASE_Z = -6.0                                    # the basement level's floor (an illustration)
PARK_Z = -9.6                                    # the parking level -2's floor (an illustration: 3.6 m under level -1's)
Z0 = FF if SCENE == "lobby" else (PARK_Z if SCENE == "parking" else BASE_Z)

# the room's frame: X to the right of the facing, Y along the facing (bearing FACE), Z up from the room's floor
FR = bpy.data.objects.new("ROOM", None)
KW.link(FR)
FR.location = (CT.x, CT.y, Z0)
FR.rotation_euler = (0, 0, -FACE * DEG)


def W_of(x, y, z=0.0):
    return Vector((CT.x + x * RIGHT.x + y * FWD.x, CT.y + x * RIGHT.y + y * FWD.y, Z0 + z))


def outline_frame(half, m=144):
    """the plate's superellipse (plate u, v) in the room frame: X = -v, Y = -u (the plate's -u side faces FACE)"""
    return [(-v, -u) for (u, v) in KW.plate_outline(half, NEXP, m)]


# ============================================================================================ materials
M = {}


def _mat(name):
    m, nt, b, out = KW.new_mat(name)
    M[name] = m
    return m, nt, b, out


def pmat(name, color, rough=0.5, metal=0.0, spec=0.5, coat=0.0, sheen=0.0, bump=0.0, bump_scale=200.0, aniso=0.0,
         emission=None, coat_rough=0.12, subsurf=0.0):
    m, nt, b, out = _mat(name)
    p = b.principled(Base_Color=color, Roughness=rough, Metallic=metal)
    b.put(p.inputs["Specular IOR Level"], spec)
    if coat:
        b.put(p.inputs["Coat Weight"], coat)
        b.put(p.inputs["Coat Roughness"], coat_rough)
    if sheen:
        b.put(p.inputs["Sheen Weight"], sheen)
        b.put(p.inputs["Sheen Roughness"], 0.45)
    if aniso:
        b.put(p.inputs["Anisotropic"], aniso)
    if subsurf:
        b.put(p.inputs["Subsurface Weight"], subsurf)
    if bump:
        tc = b.n("ShaderNodeTexCoord")
        nz = b.noise(tc.outputs["Object"], bump_scale, 6.0, 0.6)
        b.put(p.inputs["Normal"], b.bump(nz.outputs["Fac"], bump, 0.2))
    if emission:
        b.put(p.inputs["Emission Color"], emission[0])
        b.put(p.inputs["Emission Strength"], emission[1])
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def emit(name, color, strength):
    m, nt, b, out = _mat(name)
    e = b.n("ShaderNodeEmission", {"Color": color, "Strength": strength})
    nt.links.new(e.outputs[0], out.inputs["Surface"])
    return m


def wood(name, c0, c1, scale=18.0, rough=0.42, along="Z", coat=0.0):
    """kikar_interior.py's wood: rings and fibres along an axis of the object's space"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    x, y, z = b.sep(ob)
    if along == "Z":
        vec = b.combine(b.m("MULTIPLY", x, scale), b.m("MULTIPLY", y, scale), b.m("MULTIPLY", z, 0.6))
    elif along == "X":
        vec = b.combine(b.m("MULTIPLY", x, 0.6), b.m("MULTIPLY", y, scale), b.m("MULTIPLY", z, scale))
    else:
        vec = b.combine(b.m("MULTIPLY", x, scale), b.m("MULTIPLY", y, 0.6), b.m("MULTIPLY", z, scale))
    nz = b.noise(vec, 1.0, 7.0, 0.62)
    wv = b.n("ShaderNodeTexWave", wave_type="RINGS")
    b.put(wv.inputs["Vector"], vec)
    wv.inputs["Scale"].default_value = 0.35
    wv.inputs["Distortion"].default_value = 9.0
    wv.inputs["Detail"].default_value = 4.0
    g = b.m("ADD", b.m("MULTIPLY", wv.outputs["Fac"], 0.5), b.m("MULTIPLY", nz.outputs["Fac"], 0.5))
    col = b.ramp(g, [(0.3, c0), (0.75, c1)])
    p = b.principled(Base_Color=col, Roughness=b.m("ADD", rough, b.m("MULTIPLY", g, 0.1)))
    if coat:
        b.put(p.inputs["Coat Weight"], coat)
        b.put(p.inputs["Coat Roughness"], 0.2)
    bev = b.n("ShaderNodeBevel", {"Radius": 0.002})
    b.put(p.inputs["Normal"], b.bump(nz.outputs["Fac"], 0.04, 0.2, bev.outputs[0]))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def fabric(name, color, kind="boucle", color2=None):
    """kikar_interior.py's upholstery: a boucle loop or a linen weave in the bump, a soft sheen"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    if kind == "boucle":
        vo = b.n("ShaderNodeTexVoronoi", feature="SMOOTH_F1")
        b.put(vo.inputs["Vector"], ob)
        vo.inputs["Scale"].default_value = 520.0
        nz = b.noise(ob, 180.0, 4.0, 0.6)
        h = b.m("ADD", vo.outputs["Distance"], b.m("MULTIPLY", nz.outputs["Fac"], 0.6))
        strength = 0.55
    else:
        w1 = b.n("ShaderNodeTexWave", wave_type="BANDS", bands_direction="X")
        b.put(w1.inputs["Vector"], ob)
        w1.inputs["Scale"].default_value = 420.0
        w1.inputs["Distortion"].default_value = 1.5
        w2 = b.n("ShaderNodeTexWave", wave_type="BANDS", bands_direction="Z")
        b.put(w2.inputs["Vector"], ob)
        w2.inputs["Scale"].default_value = 420.0
        w2.inputs["Distortion"].default_value = 1.5
        nz = b.noise(ob, 60.0, 5.0, 0.6)
        h = b.m("ADD", b.m("MULTIPLY", w1.outputs["Fac"], w2.outputs["Fac"]), b.m("MULTIPLY", nz.outputs["Fac"], 0.3))
        strength = 0.35
    cn = b.noise(ob, 1.5, 3.0, 0.5)
    col = b.mix(b.m("MULTIPLY", cn.outputs["Fac"], 0.10), color, color2 or tuple(c * 0.86 for c in color))
    p = b.principled(Base_Color=col, Roughness=0.95)
    b.put(p.inputs["Sheen Weight"], 0.7)
    b.put(p.inputs["Sheen Roughness"], 0.5)
    b.put(p.inputs["Specular IOR Level"], 0.25)
    b.put(p.inputs["Normal"], b.bump(h, strength, 0.1))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def leather(name, color, rough=0.34):
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    vo = b.n("ShaderNodeTexVoronoi", feature="F1")
    b.put(vo.inputs["Vector"], ob)
    vo.inputs["Scale"].default_value = 260.0
    cn = b.noise(ob, 4.0, 5.0, 0.6)
    col = b.mix(b.m("MULTIPLY", cn.outputs["Fac"], 0.5), color, tuple(min(1, c * 1.35 + 0.004) for c in color))
    p = b.principled(Base_Color=col, Roughness=b.m("ADD", rough, b.m("MULTIPLY", cn.outputs["Fac"], 0.2)))
    b.put(p.inputs["Coat Weight"], 0.15)
    b.put(p.inputs["Normal"], b.bump(vo.outputs["Distance"], 0.12, 0.05))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def plaster(name, color, rough=0.88):
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    nz = b.noise(ob, 2.0, 5.0, 0.6)
    col = b.mix(b.m("MULTIPLY", nz.outputs["Fac"], 0.12), color, tuple(c * 0.95 for c in color))
    p = b.principled(Base_Color=col, Roughness=rough)
    b.put(p.inputs["Specular IOR Level"], 0.3)
    fine = b.noise(ob, 90.0, 3.0, 0.6)
    b.put(p.inputs["Normal"], b.bump(fine.outputs["Fac"], 0.015, 0.1))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def marble(name, base=(0.86, 0.85, 0.83), vein=(0.40, 0.38, 0.35), gold=(0.62, 0.52, 0.38), cloud_col=(0.80, 0.79, 0.76),
           rough=0.16):
    """kikar_interior.py's honed marble: grey and warm veins, soft clouding"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    mp = b.n("ShaderNodeMapping")
    b.put(mp.inputs["Vector"], ob)
    mp.inputs["Rotation"].default_value = (0.3, 0.8, 0.5)
    wv = b.n("ShaderNodeTexWave", wave_type="BANDS", bands_direction="DIAGONAL", wave_profile="SIN")
    b.put(wv.inputs["Vector"], mp.outputs[0])
    wv.inputs["Scale"].default_value = 0.9
    wv.inputs["Distortion"].default_value = 14.0
    wv.inputs["Detail"].default_value = 8.0
    wv.inputs["Detail Scale"].default_value = 1.6
    wv.inputs["Detail Roughness"].default_value = 0.62
    v1 = b.ramp(wv.outputs["Fac"], [(0.0, (1, 1, 1)), (0.035, (0, 0, 0)), (0.07, (1, 1, 1))])
    nz = b.noise(ob, 3.0, 8.0, 0.65)
    v2 = b.ramp(nz.outputs["Fac"], [(0.47, (1, 1, 1)), (0.5, (0.55, 0.55, 0.55)), (0.53, (1, 1, 1))])
    cl = b.n("ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
    b.put(cl.inputs["Factor"], 1.0)
    b.put(cl.inputs[6], v1)
    b.put(cl.inputs[7], v2)
    vf = b.sep(cl.outputs[2])[0]
    cloud = b.noise(ob, 0.8, 4.0, 0.55)
    base2 = b.mix(b.m("MULTIPLY", cloud.outputs["Fac"], 0.35), base, cloud_col)
    veincol = b.mix(b.m("GREATER_THAN", nz.outputs["Fac"], 0.55), vein, gold)
    col = b.mix(b.m("SUBTRACT", 1.0, vf), base2, veincol)
    p = b.principled(Base_Color=col, Roughness=rough)
    b.put(p.inputs["Coat Weight"], 0.25)
    b.put(p.inputs["Coat Roughness"], 0.06)
    b.put(p.inputs["Subsurface Weight"], 0.06)
    bev = b.n("ShaderNodeBevel", {"Radius": 0.003})
    b.put(p.inputs["Normal"], bev.outputs[0])
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def travertine(name, tone=(0.78, 0.71, 0.60), flute=None, rough=0.42):
    """a honed, filled travertine (kikar_interior.py's); flute = (axis 'X'|'Y', pitch m): vertical reeds in the bump"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    wv = b.n("ShaderNodeTexWave", wave_type="BANDS", bands_direction="Z")
    b.put(wv.inputs["Vector"], ob)
    wv.inputs["Scale"].default_value = 6.0
    wv.inputs["Distortion"].default_value = 3.0
    wv.inputs["Detail"].default_value = 6.0
    col = b.ramp(wv.outputs["Fac"], [(0.2, tuple(c * 0.85 for c in tone)), (0.5, tuple(tone)), (0.85, tuple(c * 0.92 for c in tone))])
    vo = b.n("ShaderNodeTexVoronoi", feature="F1")
    b.put(vo.inputs["Vector"], ob)
    vo.inputs["Scale"].default_value = 60.0
    nz = b.noise(ob, 30.0, 4.0, 0.6)
    pit = b.m("MULTIPLY", b.m("LESS_THAN", vo.outputs["Distance"], 0.12), b.m("GREATER_THAN", nz.outputs["Fac"], 0.55))
    col = b.mix(b.m("MULTIPLY", pit, 0.7), col, tuple(c * 0.52 for c in tone))
    p = b.principled(Base_Color=col, Roughness=rough)
    h = b.m("SUBTRACT", 1.0, pit)
    if flute:
        x, y, z = b.sep(ob)
        a = x if flute[0] == "X" else y
        reed = b.m("POWER", b.m("ABSOLUTE", b.m("SINE", b.m("MULTIPLY", a, math.pi / flute[1]))), 0.5)
        h = b.m("ADD", b.m("MULTIPLY", h, 0.15), b.m("MULTIPLY", reed, 1.0))
        bev = b.n("ShaderNodeBevel", {"Radius": 0.004})
        b.put(p.inputs["Normal"], b.bump(h, 0.6, 0.012, bev.outputs[0]))
    else:
        bev = b.n("ShaderNodeBevel", {"Radius": 0.004})
        b.put(p.inputs["Normal"], b.bump(h, 0.25, 0.2, bev.outputs[0]))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def stone_tiles(name, color, sx=1.2, sy=0.6, joint=0.003, rough=0.30, plane="XY", cloud=0.8, var=0.5, jcol=0.55, spec=0.5):
    """large-format honed stone (kikar_interior.py's stone floor): a tone per tile, soft clouding, joints; plane = the
    two object axes the tiles run on (XY a floor, XZ / YZ a wall)"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    x, y, z = b.sep(ob)
    u, v = {"XY": (x, y), "XZ": (x, z), "YZ": (y, z)}[plane]
    j = b.m("MAXIMUM", b.m("LESS_THAN", b.m("FRACT", b.m("DIVIDE", u, sx)), joint / sx),
            b.m("LESS_THAN", b.m("FRACT", b.m("DIVIDE", v, sy)), joint / sy))
    rw = b.white(b.combine(b.m("FLOOR", b.m("DIVIDE", u, sx)), b.m("FLOOR", b.m("DIVIDE", v, sy)), 0.0))
    cl = b.noise(ob, 1.6, 8.0, 0.6)
    col = b.mix(b.m("MULTIPLY", cl.outputs["Fac"], cloud), tuple(c * 0.90 for c in color), tuple(min(1.0, c * 1.10) for c in color))
    col = b.mix(b.m("MULTIPLY", rw, var), col, tuple(c * 0.91 for c in color))
    col = b.mix(j, col, tuple(c * jcol for c in color))
    p = b.principled(Base_Color=col, Roughness=b.m("ADD", rough, b.m("MULTIPLY", rw, 0.06)))
    b.put(p.inputs["Specular IOR Level"], spec)
    b.put(p.inputs["Normal"], b.bump(b.m("SUBTRACT", 1.0, j), 0.15, 0.02))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def rug(name, color, cx, cy, hx, hy, rot=0.0):
    """a hand-knotted wool rug with a quiet border (kikar_interior.py's), the border measured from the rug's own centre"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    nz = b.noise(ob, 700.0, 3.0, 0.7)
    cn = b.noise(ob, 3.0, 5.0, 0.6)
    x, y, z = b.sep(ob)
    c, s = math.cos(-rot * DEG), math.sin(-rot * DEG)
    dx, dy = b.m("SUBTRACT", x, cx), b.m("SUBTRACT", y, cy)
    lx = b.m("SUBTRACT", b.m("MULTIPLY", dx, c), b.m("MULTIPLY", dy, s))
    ly = b.m("ADD", b.m("MULTIPLY", dx, s), b.m("MULTIPLY", dy, c))
    border = b.m("MAXIMUM", b.m("GREATER_THAN", b.m("ABSOLUTE", lx), hx - 0.16), b.m("GREATER_THAN", b.m("ABSOLUTE", ly), hy - 0.16))
    c_a, c_b = tuple(color), tuple(cc * 0.89 for cc in color)
    c_border = tuple(cc * 0.72 for cc in color) if sum(color) / 3 > 0.35 else tuple(min(1.0, cc * 1.5 + 0.03) for cc in color)
    col = b.mix(b.m("MULTIPLY", cn.outputs["Fac"], 0.4), c_a, c_b)
    col = b.mix(b.m("MULTIPLY", border, 0.8), col, c_border)
    p = b.principled(Base_Color=col, Roughness=1.0)
    b.put(p.inputs["Sheen Weight"], 1.0)
    b.put(p.inputs["Sheen Roughness"], 0.6)
    b.put(p.inputs["Specular IOR Level"], 0.2)
    b.put(p.inputs["Normal"], b.bump(nz.outputs["Fac"], 0.7, 0.05))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def concrete(name, color=(0.58, 0.56, 0.52)):
    """the slip-formed core's fair-faced concrete: soft mottling, the faint horizontal lines of the slip form's daily
    lifts, small pores (an illustration of the finish; the slip-formed round core is published)"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    x, y, z = b.sep(ob)
    n1 = b.noise(ob, 0.7, 6.0, 0.6)
    n2 = b.noise(ob, 7.0, 4.0, 0.55)
    col = b.mix(b.m("MULTIPLY", n1.outputs["Fac"], 0.7), tuple(c * 0.86 for c in color), tuple(min(1, c * 1.07) for c in color))
    col = b.mix(b.m("MULTIPLY", n2.outputs["Fac"], 0.25), col, tuple(c * 0.94 for c in color))
    wob = b.noise(ob, 0.4, 2.0, 0.5)
    zz = b.m("ADD", z, b.m("MULTIPLY", wob.outputs["Fac"], 0.06))
    line = b.m("LESS_THAN", b.m("FRACT", b.m("DIVIDE", zz, 1.5)), 0.0035)
    col = b.mix(b.m("MULTIPLY", line, 0.30), col, tuple(c * 0.70 for c in color))
    streak = b.noise(b.combine(b.m("MULTIPLY", x, 1.0), b.m("MULTIPLY", y, 1.0), b.m("MULTIPLY", z, 0.12)), 3.0, 4.0, 0.6)
    col = b.mix(b.m("MULTIPLY", b.m("GREATER_THAN", streak.outputs["Fac"], 0.62), 0.15), col, tuple(c * 0.86 for c in color))
    vo = b.n("ShaderNodeTexVoronoi", feature="F1")
    b.put(vo.inputs["Vector"], ob)
    vo.inputs["Scale"].default_value = 70.0
    pore = b.m("MULTIPLY", b.m("LESS_THAN", vo.outputs["Distance"], 0.07), b.m("GREATER_THAN", n2.outputs["Fac"], 0.5))
    col = b.mix(b.m("MULTIPLY", pore, 0.6), col, tuple(c * 0.45 for c in color))
    p = b.principled(Base_Color=col, Roughness=0.74)
    b.put(p.inputs["Specular IOR Level"], 0.35)
    fine = b.noise(ob, 120.0, 3.0, 0.6)
    b.put(p.inputs["Normal"], b.bump(b.m("ADD", b.m("SUBTRACT", 1.0, pore), b.m("MULTIPLY", fine.outputs["Fac"], 0.3)), 0.12, 0.02))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def leaf_mat():
    m, nt, b, out = _mat("leaf")
    geo = b.n("ShaderNodeNewGeometry")
    pr = b.attr("lrand").outputs["Fac"]
    front = b.mix(pr, (0.10, 0.13, 0.07), (0.17, 0.20, 0.11))
    col = b.mix(geo.outputs["Backfacing"], front, (0.36, 0.40, 0.32))
    p = b.principled(Base_Color=col, Roughness=0.45)
    b.put(p.inputs["Specular IOR Level"], 0.45)
    tr = b.n("ShaderNodeBsdfTranslucent", {"Color": (0.20, 0.26, 0.08)})
    s = b.mixs(0.22, p.outputs[0], tr.outputs[0])
    nt.links.new(s, out.inputs["Surface"])
    return m


def glass_pull(name, pull):
    """the curtain wall from inside (kikar_interior.py's glass): a clear sheet with a Fresnel reflection, transparent to
    shadow rays; what the CAMERA sees through it is darker by the window pull (real-estate photography's, in the render)"""
    m, nt, b, out = _mat(name)
    lp = b.n("ShaderNodeLightPath")
    tint = (0.92, 0.95, 0.94)
    tr = b.n("ShaderNodeBsdfTransparent", {"Color": tint})
    trc = b.n("ShaderNodeBsdfTransparent", {"Color": tuple(c * pull for c in tint)})
    gl = b.n("ShaderNodeBsdfGlossy", {"Roughness": 0.0})
    lw = b.n("ShaderNodeLayerWeight", {"Blend": 0.12})
    fr = b.m("ADD", lw.outputs["Fresnel"], 0.04)
    s_other = b.mixs(fr, tr.outputs[0], gl.outputs[0])
    s_cam = b.mixs(fr, trc.outputs[0], gl.outputs[0])
    s = b.mixs(lp.outputs["Is Camera Ray"], s_other, s_cam)
    s = b.mixs(lp.outputs["Is Shadow Ray"], s, tr.outputs[0])
    nt.links.new(s, out.inputs["Surface"])
    return m


def glass_clear(name, tint=(0.93, 0.96, 0.95), blend=0.1):
    m, nt, b, out = _mat(name)
    lp = b.n("ShaderNodeLightPath")
    tr = b.n("ShaderNodeBsdfTransparent", {"Color": tint})
    gl = b.n("ShaderNodeBsdfGlossy", {"Roughness": 0.0})
    lw = b.n("ShaderNodeLayerWeight", {"Blend": blend})
    s = b.mixs(b.m("ADD", lw.outputs["Fresnel"], 0.03), tr.outputs[0], gl.outputs[0])
    s = b.mixs(lp.outputs["Is Shadow Ray"], s, tr.outputs[0])
    nt.links.new(s, out.inputs["Surface"])
    return m


def ext_mat(name, build):
    """an outdoor material that fades with distance into the sky's horizon like the rest of kikar_world (its haze)"""
    m, nt, b, out = _mat(name)
    surf = build(b)
    KW.haze(b, out, surf)
    return m


def lawn_mat():
    def build(b):
        ob = b.n("ShaderNodeTexCoord").outputs["Object"]
        n1 = b.noise(ob, 0.08, 4.0, 0.6)
        n2 = b.noise(ob, 0.9, 5.0, 0.6)
        n3 = b.noise(ob, 9.0, 3.0, 0.6)
        col = b.ramp(n1.outputs["Fac"], [(0.3, (0.070, 0.135, 0.032)), (0.55, (0.095, 0.165, 0.040)), (0.75, (0.12, 0.18, 0.05))])
        col = b.mix(b.m("MULTIPLY", n2.outputs["Fac"], 0.45), col, (0.14, 0.19, 0.06))
        col = b.mix(b.m("MULTIPLY", n3.outputs["Fac"], 0.25), col, (0.05, 0.10, 0.025))
        p = b.principled(Base_Color=col, Roughness=0.9)
        b.put(p.inputs["Specular IOR Level"], 0.12)
        b.put(p.inputs["Sheen Weight"], 0.25)
        b.put(p.inputs["Sheen Roughness"], 0.5)
        b.put(p.inputs["Sheen Tint"], (0.45, 0.75, 0.30))
        fine = b.noise(ob, 70.0, 3.0, 0.7)
        b.put(p.inputs["Normal"], b.bump(b.m("ADD", fine.outputs["Fac"], b.m("MULTIPLY", n3.outputs["Fac"], 0.5)), 0.6, 0.05))
        return p.outputs[0]
    return ext_mat("lawn", build)


def paver_mat(name, color, sx, sy, joint=0.008, var=0.5, rough=0.62):
    def build(b):
        ob = b.n("ShaderNodeTexCoord").outputs["Object"]
        x, y, z = b.sep(ob)
        u = b.m("ADD", x, b.m("MULTIPLY", b.m("FLOOR", b.m("DIVIDE", y, sy)), sx * 0.5))   # a running bond
        j = b.m("MAXIMUM", b.m("LESS_THAN", b.m("FRACT", b.m("DIVIDE", u, sx)), joint / sx),
                b.m("LESS_THAN", b.m("FRACT", b.m("DIVIDE", y, sy)), joint / sy))
        rw = b.white(b.combine(b.m("FLOOR", b.m("DIVIDE", u, sx)), b.m("FLOOR", b.m("DIVIDE", y, sy)), 3.0))
        cl = b.noise(ob, 0.5, 6.0, 0.6)
        col = b.mix(b.m("MULTIPLY", cl.outputs["Fac"], 0.6), tuple(c * 0.9 for c in color), tuple(min(1, c * 1.08) for c in color))
        col = b.mix(b.m("MULTIPLY", rw, var), col, tuple(c * 0.86 for c in color))
        col = b.mix(j, col, tuple(c * 0.5 for c in color))
        p = b.principled(Base_Color=col, Roughness=rough)
        b.put(p.inputs["Specular IOR Level"], 0.35)
        fine = b.noise(ob, 60.0, 3.0, 0.6)
        b.put(p.inputs["Normal"], b.bump(b.m("ADD", b.m("SUBTRACT", 1.0, j), b.m("MULTIPLY", fine.outputs["Fac"], 0.2)), 0.25, 0.02))
        return p.outputs[0]
    return ext_mat(name, build)


def pond_mat():
    """the ecological pond (1 m deep, published; its outline the world's): a calm dark water mirroring the sky"""
    def build(b):
        ob = b.n("ShaderNodeTexCoord").outputs["Object"]
        mp = b.n("ShaderNodeMapping")
        b.put(mp.inputs["Vector"], ob)
        mp.inputs["Scale"].default_value = (1.0, 2.5, 1.0)
        n1 = b.noise(mp.outputs[0], 0.7, 4.0, 0.55)
        n2 = b.noise(ob, 4.0, 3.0, 0.5)
        h = b.m("ADD", n1.outputs["Fac"], b.m("MULTIPLY", n2.outputs["Fac"], 0.3))
        nrm = b.bump(h, 0.08, 0.1)
        gl = b.n("ShaderNodeBsdfGlossy", {"Color": (0.85, 0.88, 0.88), "Roughness": 0.02, "Normal": nrm})
        fr = b.n("ShaderNodeFresnel", {"IOR": 1.333, "Normal": nrm})
        body = b.n("ShaderNodeBsdfDiffuse", {"Color": (0.012, 0.022, 0.016)})
        return b.mixs(b.m("ADD", b.m("MULTIPLY", fr.outputs[0], 0.85), 0.1), body.outputs[0], gl.outputs[0])
    return ext_mat("pond_water", build)


def pool_water():
    """the pool's water: a refracting surface (IOR 1.333), barely moving, transparent to shadow rays (the lights reach
    the tiles without caustic noise; the tiles carry a caustic pattern instead)"""
    m, nt, b, out = _mat("pool_water")
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    n1 = b.noise(ob, 0.55, 3.0, 0.5)
    wv = b.n("ShaderNodeTexWave", wave_type="BANDS", bands_direction="Y")
    b.put(wv.inputs["Vector"], ob)
    wv.inputs["Scale"].default_value = 0.45
    wv.inputs["Distortion"].default_value = 3.0
    wv.inputs["Detail"].default_value = 2.0
    n2 = b.noise(ob, 3.0, 2.0, 0.5)
    h = b.m("ADD", b.m("ADD", b.m("MULTIPLY", n1.outputs["Fac"], 0.6), b.m("MULTIPLY", wv.outputs["Fac"], 0.25)),
            b.m("MULTIPLY", n2.outputs["Fac"], 0.12))
    nrm = b.bump(h, 0.05, 0.03)
    tint = (0.80, 0.95, 0.96)
    gl = b.n("ShaderNodeBsdfGlass", {"Color": tint, "Roughness": 0.0, "IOR": 1.333, "Normal": nrm})
    lp = b.n("ShaderNodeLightPath")
    tr = b.n("ShaderNodeBsdfTransparent", {"Color": (0.90, 0.98, 0.98)})
    s = b.mixs(lp.outputs["Is Shadow Ray"], gl.outputs[0], tr.outputs[0])
    nt.links.new(s, out.inputs["Surface"])
    return m


def mosaic(name, c1, c2, grout, size=0.025, lanes=None, caustic=0.0, water_z=-0.03):
    """glass mosaic tiles (2.5 cm) on whichever face they cover (the object-space normal picks the plane), a tone per tile;
    lanes = (centres in X, y0, y1): dark lane lines and T ends on the floor; caustic = the light's net under the water"""
    m, nt, b, out = _mat(name)
    tc = b.n("ShaderNodeTexCoord")
    ob = tc.outputs["Object"]
    x, y, z = b.sep(ob)
    nx, ny, nz = b.sep(tc.outputs["Normal"])
    isz = b.m("GREATER_THAN", b.m("ABSOLUTE", nz), 0.5)
    isx = b.m("GREATER_THAN", b.m("ABSOLUTE", nx), 0.5)
    u = b.mixf(isx, x, y)
    v = b.mixf(isz, z, y)
    fu = b.m("FRACT", b.m("DIVIDE", u, size))
    fv = b.m("FRACT", b.m("DIVIDE", v, size))
    g = 0.09
    jo = b.m("MAXIMUM", b.m("LESS_THAN", fu, g), b.m("LESS_THAN", fv, g))
    cell = b.combine(b.m("FLOOR", b.m("DIVIDE", u, size)), b.m("FLOOR", b.m("DIVIDE", v, size)), b.m("MULTIPLY", isz, 7.0))
    rw = b.white(cell)
    col = b.mix(rw, c1, c2)
    if lanes:
        xs, y0, y1 = lanes
        ln = None
        for xc in xs:
            d = b.m("LESS_THAN", b.m("ABSOLUTE", b.m("SUBTRACT", x, xc)), 0.125)
            ln = d if ln is None else b.m("MAXIMUM", ln, d)
        iny = b.m("MULTIPLY", b.m("GREATER_THAN", y, y0), b.m("LESS_THAN", y, y1))
        tee = None
        for yt in (y0, y1):
            d = b.m("LESS_THAN", b.m("ABSOLUTE", b.m("SUBTRACT", y, yt)), 0.125)
            near = None
            for xc in xs:
                e = b.m("LESS_THAN", b.m("ABSOLUTE", b.m("SUBTRACT", x, xc)), 0.5)
                near = e if near is None else b.m("MAXIMUM", near, e)
            t_ = b.m("MULTIPLY", d, near)
            tee = t_ if tee is None else b.m("MAXIMUM", tee, t_)
        lane = b.m("MULTIPLY", b.m("MAXIMUM", b.m("MULTIPLY", ln, iny), tee), isz)
        col = b.mix(lane, col, (0.055, 0.085, 0.12))
    col = b.mix(jo, col, grout)
    if caustic:
        wob = b.noise(ob, 0.8, 2.0, 0.5)
        uu = b.m("ADD", u, b.m("MULTIPLY", wob.outputs["Fac"], 0.35))
        net = None
        for sc_, sh in ((2.0, 0.0), (3.2, 3.3)):
            vo = b.n("ShaderNodeTexVoronoi", feature="DISTANCE_TO_EDGE")
            b.put(vo.inputs["Vector"], b.combine(b.m("ADD", uu, sh), v, 0.0))
            vo.inputs["Scale"].default_value = sc_
            ln_ = b.m("POWER", b.m("SUBTRACT", 1.0, b.m("DIVIDE", vo.outputs["Distance"], 0.06), clamp=True), 2.5)
            net = ln_ if net is None else b.m("MAXIMUM", net, b.m("MULTIPLY", ln_, 0.7))
        under = b.m("LESS_THAN", z, water_z - 0.05)
        k = b.m("ADD", 1.0, b.m("MULTIPLY", b.m("MULTIPLY", net, under), caustic))
        cm = b.n("ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
        b.put(cm.inputs["Factor"], 1.0)
        b.put(cm.inputs[6], col)
        b.put(cm.inputs[7], b.combine(k, k, k))
        col = cm.outputs[2]
    p = b.principled(Base_Color=col, Roughness=b.mixf(jo, 0.08, 0.7))
    b.put(p.inputs["Coat Weight"], 0.3)
    b.put(p.inputs["Normal"], b.bump(b.m("SUBTRACT", 1.0, jo), 0.3, 0.002))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def onyx(name, color=(1.0, 0.80, 0.52), strength=2.2, plane="XZ"):
    """a backlit honey onyx: a polished stone panel lit from behind, plainly a lit panel (an illustration)"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    x, y, z = b.sep(ob)
    u = x if plane == "XZ" else y
    mp = b.n("ShaderNodeMapping")
    b.put(mp.inputs["Vector"], b.combine(u, z, 0.0))
    mp.inputs["Rotation"].default_value = (0.0, 0.0, 0.35)
    wv = b.n("ShaderNodeTexWave", wave_type="BANDS", bands_direction="X", wave_profile="SIN")
    b.put(wv.inputs["Vector"], mp.outputs[0])
    wv.inputs["Scale"].default_value = 0.55
    wv.inputs["Distortion"].default_value = 11.0
    wv.inputs["Detail"].default_value = 6.0
    wv.inputs["Detail Scale"].default_value = 1.4
    nz = b.noise(b.combine(u, z, 1.0), 1.2, 6.0, 0.6)
    pat = b.m("ADD", b.m("MULTIPLY", wv.outputs["Fac"], 0.55), b.m("MULTIPLY", nz.outputs["Fac"], 0.45))
    glow = b.ramp(pat, [(0.15, tuple(c * 0.42 for c in color)), (0.45, tuple(c * 0.80 for c in color)), (0.62, tuple(color)),
                        (0.78, (1.0, 0.93, 0.80)), (0.92, tuple(c * 0.6 for c in color))])
    # the panels: 1.5 x 2.6 m slabs, book-matched joints
    j = b.m("MAXIMUM", b.m("LESS_THAN", b.m("FRACT", b.m("DIVIDE", b.m("ADD", u, 0.0), 1.5)), 0.003),
            b.m("LESS_THAN", b.m("FRACT", b.m("DIVIDE", b.m("SUBTRACT", z, 0.45), 1.95)), 0.0025))
    glow = b.mix(j, glow, (0.08, 0.05, 0.03))
    em = b.n("ShaderNodeEmission", {"Color": glow, "Strength": strength})
    p = b.principled(Base_Color=b.mix(0.5, glow, (0.6, 0.5, 0.4)), Roughness=0.08)
    b.put(p.inputs["Coat Weight"], 0.4)
    nt.links.new(b.addsh(b.mixs(0.75, p.outputs[0], em.outputs[0]), em.outputs[0]), out.inputs["Surface"])
    return m


def rubber_floor(name="rubber"):
    """the gym's floor: 1 m rubber tiles, charcoal with EPDM flecks"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    x, y, z = b.sep(ob)
    cell = b.combine(b.m("FLOOR", b.m("MULTIPLY", x, 260.0)), b.m("FLOOR", b.m("MULTIPLY", y, 260.0)), 0.0)
    r = b.white(cell)
    fl1 = b.m("LESS_THAN", r, 0.05)
    fl2 = b.m("GREATER_THAN", r, 0.98)
    base = (0.040, 0.041, 0.044)
    cl = b.noise(ob, 0.9, 4.0, 0.6)
    col = b.mix(b.m("MULTIPLY", cl.outputs["Fac"], 0.5), base, (0.052, 0.052, 0.055))
    col = b.mix(fl1, col, (0.13, 0.13, 0.13))
    col = b.mix(fl2, col, (0.10, 0.12, 0.16))
    j = b.m("MAXIMUM", b.m("LESS_THAN", b.m("FRACT", x), 0.002), b.m("LESS_THAN", b.m("FRACT", y), 0.002))
    col = b.mix(j, col, (0.018, 0.018, 0.02))
    p = b.principled(Base_Color=col, Roughness=0.86)
    b.put(p.inputs["Specular IOR Level"], 0.35)
    fine = b.noise(ob, 400.0, 3.0, 0.6)
    b.put(p.inputs["Normal"], b.bump(b.m("ADD", fine.outputs["Fac"], b.m("SUBTRACT", 1.0, j)), 0.25, 0.01))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def moss_mat():
    """a preserved-moss wall (an illustration): cushions of moss in greens, a few pale lichen patches, deep relief"""
    m, nt, b, out = _mat("moss")
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    vo = b.n("ShaderNodeTexVoronoi", feature="SMOOTH_F1")
    b.put(vo.inputs["Vector"], ob)
    vo.inputs["Scale"].default_value = 11.0
    nz = b.noise(ob, 45.0, 6.0, 0.65)
    big = b.noise(ob, 0.8, 3.0, 0.5)
    cl = b.m("ADD", b.m("MULTIPLY", b.m("SUBTRACT", 1.0, vo.outputs["Distance"]), 0.6), b.m("MULTIPLY", nz.outputs["Fac"], 0.4))
    col = b.ramp(cl, [(0.25, (0.020, 0.045, 0.012)), (0.45, (0.06, 0.12, 0.025)), (0.65, (0.12, 0.20, 0.045)), (0.85, (0.20, 0.27, 0.08))])
    col = b.mix(b.m("MULTIPLY", b.m("GREATER_THAN", big.outputs["Fac"], 0.70), 0.35), col, (0.30, 0.34, 0.22))
    col = b.mix(b.m("MULTIPLY", b.m("LESS_THAN", big.outputs["Fac"], 0.36), 0.4), col, (0.10, 0.16, 0.05))
    p = b.principled(Base_Color=col, Roughness=1.0)
    b.put(p.inputs["Sheen Weight"], 0.6)
    b.put(p.inputs["Specular IOR Level"], 0.2)
    b.put(p.inputs["Normal"], b.bump(cl, 1.0, 0.03))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def screen_mat(name, glow=(0.20, 0.42, 0.70), strength=0.9):
    """a console's display, on: a dark glossy glass with a dim UI glow in bands"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    x, y, z = b.sep(ob)
    band = b.m("LESS_THAN", b.m("FRACT", b.m("MULTIPLY", b.m("ADD", b.m("ADD", x, y), z), 9.0)), 0.5)
    p = b.principled(Base_Color=(0.01, 0.012, 0.015), Roughness=0.05)
    b.put(p.inputs["Coat Weight"], 0.6)
    b.put(p.inputs["Emission Color"], glow)
    b.put(p.inputs["Emission Strength"], b.m("MULTIPLY", b.m("ADD", 0.6, b.m("MULTIPLY", band, 0.4)), strength))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def grille_mat(name, along):
    """the deck-level overflow grating: white slats across the channel, dark water between them"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    x, y, z = b.sep(ob)
    a = y if along == "Y" else x
    gap = b.m("LESS_THAN", b.m("FRACT", b.m("MULTIPLY", a, 28.0)), 0.30)
    col = b.mix(gap, (0.80, 0.80, 0.78), (0.02, 0.05, 0.06))
    p = b.principled(Base_Color=col, Roughness=b.mixf(gap, 0.35, 0.05))
    b.put(p.inputs["Normal"], b.bump(b.m("SUBTRACT", 1.0, gap), 0.8, 0.01))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def turf_mat():
    """synthetic turf: green blades in the bump, white lines every 2 m and along both edges"""
    m, nt, b, out = _mat("turf")
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    x, y, z = b.sep(ob)
    n1 = b.noise(ob, 1.2, 4.0, 0.6)
    n2 = b.noise(ob, 260.0, 3.0, 0.7)
    col = b.mix(b.m("MULTIPLY", n1.outputs["Fac"], 0.8), (0.026, 0.065, 0.020), (0.045, 0.095, 0.030))
    cross = b.m("LESS_THAN", b.m("ABSOLUTE", b.m("SUBTRACT", b.m("FRACT", b.m("DIVIDE", b.m("SUBTRACT", y, 12.4), 2.0)), 0.5)), 0.010)
    edge = b.m("GREATER_THAN", b.m("ABSOLUTE", b.m("SUBTRACT", x, GX)), 0.86)
    line = b.m("MAXIMUM", cross, edge)
    col = b.mix(b.m("MULTIPLY", line, 0.9), col, (0.62, 0.63, 0.60))
    p = b.principled(Base_Color=col, Roughness=0.8)
    b.put(p.inputs["Sheen Weight"], 0.2)
    b.put(p.inputs["Sheen Tint"], (0.4, 0.8, 0.3))
    b.put(p.inputs["Specular IOR Level"], 0.3)
    b.put(p.inputs["Normal"], b.bump(n2.outputs["Fac"], 0.7, 0.01))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def common_materials():
    pmat("shadowgap", (0.04, 0.04, 0.04), 0.8)
    pmat("alu_white", (0.83, 0.83, 0.82), 0.30, spec=0.6)
    pmat("brass", (0.80, 0.60, 0.34), 0.26, metal=1.0, aniso=0.5)
    pmat("bronze", (0.40, 0.28, 0.17), 0.30, metal=1.0, aniso=0.6)
    pmat("blacksteel", (0.035, 0.035, 0.035), 0.38, metal=0.8)
    pmat("black_coat", (0.028, 0.028, 0.030), 0.42, spec=0.5, coat=0.25, coat_rough=0.3)
    pmat("chrome", (0.86, 0.87, 0.88), 0.07, metal=1.0)
    pmat("steel", (0.62, 0.62, 0.63), 0.26, metal=1.0, aniso=0.6)
    pmat("rubber_black", (0.032, 0.032, 0.034), 0.62, spec=0.3)
    pmat("black_glass", (0.01, 0.01, 0.012), 0.05, spec=1.0, coat=0.5)
    pmat("ceramic_white", (0.85, 0.84, 0.80), 0.25, coat=0.3)
    pmat("ceramic_clay", (0.62, 0.50, 0.40), 0.75, bump=0.08, bump_scale=40.0)
    pmat("soil", (0.06, 0.045, 0.035), 1.0, bump=0.4, bump_scale=80.0)
    pmat("bark", (0.22, 0.19, 0.15), 0.9, bump=0.5, bump_scale=60.0)
    pmat("stone_planter", (0.60, 0.57, 0.52), 0.85, bump=0.15, bump_scale=30.0)
    pmat("towel", (0.90, 0.89, 0.86), 1.0, sheen=0.9, bump=0.5, bump_scale=300.0)
    pmat("towel_grey", (0.42, 0.42, 0.40), 1.0, sheen=0.9, bump=0.5, bump_scale=300.0)
    pmat("paper_a", (0.70, 0.66, 0.58), 0.8)
    pmat("paper_b", (0.30, 0.34, 0.33), 0.7)
    pmat("paper_c", (0.55, 0.30, 0.20), 0.7)
    pmat("paper_d", (0.85, 0.83, 0.78), 0.7)
    pmat("mirror", (0.93, 0.93, 0.93), 0.012, metal=1.0)
    emit("led_warm", (1.0, 0.80, 0.58), 12.0)
    emit("downlight_emit", (1.0, 0.85, 0.66), 18.0)
    pmat("downlight_rim", (0.06, 0.06, 0.06), 0.4)
    leaf_mat()
    wood("walnut", (0.13, 0.075, 0.045), (0.25, 0.15, 0.085), 22.0, 0.38)
    wood("oak", (0.42, 0.29, 0.17), (0.56, 0.41, 0.26), 22.0, 0.42)
    wood("teak", (0.34, 0.21, 0.11), (0.46, 0.30, 0.17), 20.0, 0.55)
    wood("oak_slat", (0.40, 0.27, 0.15), (0.54, 0.38, 0.23), 26.0, 0.45, along="Z")
    fabric("boucle", (0.80, 0.76, 0.68), "boucle")
    fabric("linen_cream", (0.84, 0.81, 0.75), "linen")
    fabric("linen_rust", (0.52, 0.27, 0.15), "linen")
    fabric("linen_sage", (0.45, 0.48, 0.40), "linen")
    fabric("linen_sand", (0.70, 0.64, 0.55), "linen")
    fabric("linen_taupe", (0.56, 0.51, 0.45), "linen")
    leather("leather", (0.30, 0.14, 0.06))
    leather("leather_black", (0.025, 0.025, 0.027), 0.38)


# ============================================================================================ geometry (room frame)
def own(ob):
    ob.parent = FR
    return ob


def obj(name, verts, faces, mat, smooth=False):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    KW.link(ob)
    if mat:
        me.materials.append(M[mat] if isinstance(mat, str) else mat)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    return own(ob)


def fix_normals(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(ob.data)
    bm.free()
    return ob


def bevel(ob, width, segs=3):
    b = ob.modifiers.new("bevel", "BEVEL")
    b.width = width
    b.segments = segs
    b.limit_method = "ANGLE"
    b.angle_limit = 50 * DEG
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def subsurf(ob, lv=2):
    s = ob.modifiers.new("sub", "SUBSURF")
    s.levels = s.render_levels = lv
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def displace(ob, strength=0.01, scale=0.25):
    tex = bpy.data.textures.new("n_" + ob.name, "CLOUDS")
    tex.noise_scale = scale
    d = ob.modifiers.new("disp", "DISPLACE")
    d.texture = tex
    d.strength = strength
    d.texture_coords = "LOCAL"
    return ob


def box(name, cx, cy, z0, sx, sy, sz, mat, rot=0.0, bev=0.0, segs=3, sub=0):
    """a box centred at (cx, cy), from z0 up sz; rot turns it about Z (degrees, its local x toward the rotated x)"""
    c, s = math.cos(rot * DEG), math.sin(rot * DEG)
    V = []
    for dz in (0, sz):
        for (dx, dy) in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
            V.append((cx + dx * c - dy * s, cy + dx * s + dy * c, z0 + dz))
    F = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    ob = obj(name, V, F, mat)
    if sub:
        if bev:
            bevel(ob, bev, 1)
        subsurf(ob, sub)
    elif bev:
        bevel(ob, bev, segs)
    return ob


def gbox(name, x0, x1, y0, y1, z0, z1, mat, bev=0.0, segs=3):
    return box(name, (x0 + x1) / 2, (y0 + y1) / 2, z0, abs(x1 - x0), abs(y1 - y0), z1 - z0, mat, 0.0, bev, segs)


def cyl(name, cx, cy, z0, z1, r, mat, seg=48, bev=0.0, r_top=None):
    rt = r if r_top is None else r_top
    V = [(cx + r * math.cos(2 * math.pi * k / seg), cy + r * math.sin(2 * math.pi * k / seg), z0) for k in range(seg)]
    V += [(cx + rt * math.cos(2 * math.pi * k / seg), cy + rt * math.sin(2 * math.pi * k / seg), z1) for k in range(seg)]
    F = [tuple(range(seg))[::-1], tuple(range(seg, 2 * seg))] + [(k, (k + 1) % seg, seg + (k + 1) % seg, seg + k) for k in range(seg)]
    ob = obj(name, V, F, mat, smooth=True)
    if bev:
        bevel(ob, bev, 3)
    return ob


def rod(name, p0, p1, r, mat, seg=16, r1=None, bev=0.0):
    """a capped cylinder between two points"""
    p0, p1 = Vector(p0), Vector(p1)
    t = (p1 - p0).normalized()
    a = Vector((0, 0, 1)) if abs(t.z) < 0.9 else Vector((1, 0, 0))
    u = t.cross(a).normalized()
    w = t.cross(u).normalized()
    r1 = r if r1 is None else r1
    V = [tuple(p0 + (u * math.cos(2 * math.pi * k / seg) + w * math.sin(2 * math.pi * k / seg)) * r) for k in range(seg)]
    V += [tuple(p1 + (u * math.cos(2 * math.pi * k / seg) + w * math.sin(2 * math.pi * k / seg)) * r1) for k in range(seg)]
    F = [tuple(range(seg))[::-1], tuple(range(seg, 2 * seg))] + [(k, (k + 1) % seg, seg + (k + 1) % seg, seg + k) for k in range(seg)]
    ob = obj(name, V, F, mat, smooth=True)
    if bev:
        bevel(ob, bev, 2)
    return ob


def sphere(name, cx, cy, cz, r, mat, sx=1.0, sy=1.0, sz=1.0, seg=24):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=r)
    for v in bm.verts:
        v.co = Vector((cx + v.co.x * sx, cy + v.co.y * sy, cz + v.co.z * sz))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    KW.link(ob)
    me.materials.append(M[mat] if isinstance(mat, str) else mat)
    for p in me.polygons:
        p.use_smooth = True
    return own(ob)


def tube(name, pts, r, mat, seg=10):
    V, F = [], []
    n = len(pts)
    for i, p in enumerate(pts):
        p = Vector(p)
        t = (Vector(pts[min(i + 1, n - 1)]) - Vector(pts[max(i - 1, 0)])).normalized()
        a = Vector((0, 0, 1)) if abs(t.z) < 0.9 else Vector((1, 0, 0))
        u = t.cross(a).normalized()
        w = t.cross(u).normalized()
        rr = r[i] if isinstance(r, (list, tuple)) else r
        for k in range(seg):
            an = 2 * math.pi * k / seg
            V.append(tuple(p + (u * math.cos(an) + w * math.sin(an)) * rr))
    for i in range(n - 1):
        for k in range(seg):
            F.append((i * seg + k, i * seg + (k + 1) % seg, (i + 1) * seg + (k + 1) % seg, (i + 1) * seg + k))
    return obj(name, V, F, mat, smooth=True)


def poly_prism(name, poly, z0, z1, mat):
    n = len(poly)
    V = [(x, y, z0) for (x, y) in poly] + [(x, y, z1) for (x, y) in poly]
    F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(k, (k + 1) % n, n + (k + 1) % n, n + k) for k in range(n)]
    return fix_normals(obj(name, V, F, mat))


def ring_prism(name, outer, inner, z0, z1, mat):
    """a closed ring between two loops of the same count (outer, inner), from z0 to z1"""
    n = len(outer)
    V = [(x, y, z0) for (x, y) in outer] + [(x, y, z1) for (x, y) in outer] + [(x, y, z0) for (x, y) in inner] + [(x, y, z1) for (x, y) in inner]
    F = []
    for k in range(n):
        k2 = (k + 1) % n
        F.append((k, k2, n + k2, n + k))                     # the outer wall
        F.append((2 * n + k2, 2 * n + k, 3 * n + k, 3 * n + k2))   # the inner wall
        F.append((n + k, n + k2, 3 * n + k2, 3 * n + k))     # the top
        F.append((k2, k, 2 * n + k, 2 * n + k2))             # the bottom
    return fix_normals(obj(name, V, F, mat))


def grid_wall_x(name, x, y0, y1, z0, z1, ny, nz, mat):
    """a fine vertical grid in the plane X = x, facing +X (for a displaced relief)"""
    V, F = [], []
    for j in range(nz + 1):
        for i in range(ny + 1):
            V.append((x, y0 + (y1 - y0) * i / ny, z0 + (z1 - z0) * j / nz))
    for j in range(nz):
        for i in range(ny):
            a = j * (ny + 1) + i
            F.append((a, a + 1, a + ny + 2, a + ny + 1))
    return obj(name, V, F, mat, smooth=True)


def circle(r, n=144, a0=0.0):
    return [(r * math.cos(a0 + 2 * math.pi * k / n), r * math.sin(a0 + 2 * math.pi * k / n)) for k in range(n)]


def polar_match(pts, r):
    """the circle of radius r at the polar angles of pts (to ring a superellipse with a circle)"""
    return [(r * math.cos(math.atan2(y, x)), r * math.sin(math.atan2(y, x))) for (x, y) in pts]


def flat_ring(name, outer, inner, z, mat, down=True):
    """a one-sided flat ring (a ceiling: facing down) between two loops of the same count"""
    n = len(outer)
    V = [(x, y, z) for (x, y) in outer] + [(x, y, z) for (x, y) in inner]
    F = []
    for k in range(n):
        k2 = (k + 1) % n
        F.append((k, k2, n + k2, n + k))
    ob = obj(name, V, F, mat)
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.normal_update()
    bmesh.ops.reverse_faces(bm, faces=[f for f in bm.faces if (f.normal.z > 0) == down])
    bm.to_mesh(ob.data)
    bm.free()
    return ob


def sector(name, a0, a1, r_in, r_out, z0, z1, mat, seg=None):
    """an annulus sector, closed (its ends are the reveals), angles from +Y toward +X (degrees)"""
    seg = seg or max(2, int(abs(a1 - a0) / 2.5))
    ang = [a0 + (a1 - a0) * k / seg for k in range(seg + 1)]
    outer = [(r_out * math.sin(a * DEG), r_out * math.cos(a * DEG)) for a in ang]
    inner = [(r_in * math.sin(a * DEG), r_in * math.cos(a * DEG)) for a in ang]
    poly = outer + inner[::-1]
    return poly_prism(name, poly, z0, z1, mat)


def cushion(name, cx, cy, z0, sx, sy, sz, mat, rot=0.0, puff=0.012, bev=0.04):
    ob = box(name, cx, cy, z0, sx, sy, sz, mat, rot)
    bv = ob.modifiers.new("bevel", "BEVEL")
    bv.width = min(bev, sx / 2.2, sy / 2.2, sz / 2.2)
    bv.segments = 5
    bv.profile = 0.62
    sub = ob.modifiers.new("sub", "SUBSURF")
    sub.subdivision_type = "SIMPLE"
    sub.levels = sub.render_levels = 3
    for p in ob.data.polygons:
        p.use_smooth = True
    displace(ob, puff, 0.35)
    return ob


def pillow(name, cx, cy, z0, w, h, t, mat, rot=0.0, tilt=0.0, fullness=0.5, puff=0.004):
    """a sewn cushion standing w wide and h high, its faces toward local y; tilt leans its top back (+y)"""
    n = 16
    V, F, idx = [], [], {}

    def vid(i, j, side):
        border = i in (0, n) or j in (0, n)
        key = (i, j, 0 if border else side)
        if key in idx:
            return idx[key]
        a = 2 * i / n - 1
        bb = 2 * j / n - 1
        prof = max(0.0, (1 - abs(a) ** 3) * (1 - abs(bb) ** 3)) ** fullness
        x = a * w / 2 * (1 - 0.05 * bb * bb)
        z = (bb + 1) * h / 2 * (1 - 0.03 * a * a) + h * 0.015 * a * a
        y = (0 if border else side) * t / 2 * prof
        th = -tilt * DEG
        y2 = y * math.cos(th) - z * math.sin(th)
        z2 = y * math.sin(th) + z * math.cos(th)
        c, sn = math.cos(rot * DEG), math.sin(rot * DEG)
        V.append((cx + x * c - y2 * sn, cy + x * sn + y2 * c, z0 + z2))
        idx[key] = len(V) - 1
        return idx[key]

    for side in (-1, 1):
        for i in range(n):
            for j in range(n):
                q = (vid(i, j, side), vid(i + 1, j, side), vid(i + 1, j + 1, side), vid(i, j + 1, side))
                F.append(q if side > 0 else q[::-1])
    ob = obj(name, V, F, mat, smooth=True)
    sub = ob.modifiers.new("sub", "SUBSURF")
    sub.levels = sub.render_levels = 1
    displace(ob, puff, 0.12)
    return ob


def piping(name, cx, cy, z, sx, sy, rot, r, mat, inset=0.02, corner=0.05):
    c, sn = math.cos(rot * DEG), math.sin(rot * DEG)
    hx, hy = sx / 2 - inset, sy / 2 - inset
    pts = []
    for (qx, qy, a0) in ((hx - corner, hy - corner, 0), (-hx + corner, hy - corner, 90), (-hx + corner, -hy + corner, 180), (hx - corner, -hy + corner, 270)):
        for k in range(7):
            a = math.radians(a0 + 90 * k / 6)
            x, y = qx + corner * math.cos(a), qy + corner * math.sin(a)
            pts.append((cx + x * c - y * sn, cy + x * sn + y * c, z))
    pts.append(pts[0])
    return tube(name, pts, r, mat, 6)


def Pr(cx, cy, rot):
    c, s = math.cos(rot * DEG), math.sin(rot * DEG)
    return lambda x, y: (cx + x * c - y * s, cy + x * s + y * c)


# ============================================================================================ furniture (illustration)
def sofa(cx, cy, rot, length=3.0, depth=1.0, mat="boucle", pillows=True):
    """kikar_interior.py's sofa: a recessed plinth, a seat of three cushions, a back of three, rounded arms; with rot 0 its
    front faces -Y"""
    P = Pr(cx, cy, rot)
    x, y = P(0, 0)
    box("sofa_plinth", x, y, 0.0, length - 0.2, depth - 0.2, 0.08, "shadowgap", rot, bev=0.01)
    x, y = P(0, 0.05)
    cushion("sofa_base", x, y, 0.08, length - 0.02, depth, 0.28, mat, rot, 0.003, 0.03)
    arm = 0.18
    for sgn in (-1, 1):
        x, y = P(sgn * (length / 2 - arm / 2), 0.05)
        cushion("sofa_arm", x, y, 0.08, arm, depth, 0.46, mat, rot, 0.003, 0.07)
        piping("sofa_arm_pipe", x, y, 0.535, arm, depth, rot, 0.0055, mat, 0.012, 0.06)
    x, y = P(0, depth / 2 - 0.02)
    cushion("sofa_backframe", x, y, 0.08, length - 2 * arm + 0.02, 0.15, 0.58, mat, rot, 0.003, 0.05)
    seat_w = (length - 2 * arm) / 3
    for i in range(3):
        xo = -length / 2 + arm + seat_w * (i + 0.5)
        x, y = P(xo, -0.08)
        cushion("sofa_seat%d" % i, x, y, 0.36, seat_w - 0.012, depth - 0.26, 0.15, mat, rot, 0.010, 0.05)
        piping("sofa_seat_pipe%d" % i, x, y, 0.505, seat_w - 0.012, depth - 0.26, rot, 0.0055, mat, 0.014, 0.05)
        x, y = P(xo, depth / 2 - 0.16)
        pillow("sofa_back%d" % i, x, y, 0.42, seat_w - 0.03, 0.46, 0.24, mat, rot, 10.0, 0.35, 0.006)
    if pillows:
        for i, (xo, mt, w, tl) in enumerate(((-length * 0.34, "linen_rust", 0.52, 16), (-length * 0.19, "linen_sage", 0.46, 12),
                                             (length * 0.34, "linen_cream", 0.5, 14))):
            x, y = P(xo, 0.12)
            pillow("pillow%d" % i, x, y, 0.49, w, w * 0.9, 0.17, mt, rot + (-6 if xo < 0 else 5), tl, 0.5, 0.004)


def lounge_chair(cx, cy, rot, wood_m="walnut", seat="leather"):
    """kikar_interior.py's lounge chair: a walnut frame with leather cushions; with rot 0 it faces -Y"""
    P = Pr(cx, cy, rot)
    for sx in (-0.36, 0.36):
        for sy in (-0.32, 0.30):
            x, y = P(sx, sy)
            box("lc_leg", x, y, 0.0, 0.04, 0.04, 0.34 if sy < 0 else 0.58, wood_m, rot, bev=0.01)
        x, y = P(sx, 0)
        box("lc_rail", x, y, 0.30, 0.045, 0.72, 0.045, wood_m, rot, bev=0.012)
        x, y = P(sx, -0.05)
        box("lc_armrest", x, y, 0.55, 0.06, 0.62, 0.035, wood_m, rot, bev=0.012)
    x, y = P(0, -0.05)
    cushion("lc_seat", x, y, 0.30, 0.66, 0.62, 0.12, seat, rot, 0.006, 0.04)
    x, y = P(0, 0.30)
    cushion("lc_back", x, y, 0.40, 0.66, 0.11, 0.46, seat, rot, 0.006, 0.04)


def olive_tree(name, cx, cy, height=2.4, seed=3, pot_r=0.32, pot_h=0.55, leaves=9000, pot_mat="stone_planter", z0=0.0):
    """kikar_interior.py's olive: a gnarled trunk, branches, narrow silver-green leaves, in a planter (an illustration)"""
    r = random.Random(seed)
    cyl(name + "_pot", cx, cy, z0, z0 + pot_h, pot_r, pot_mat, 56, bev=0.02, r_top=pot_r * 1.06)
    cyl(name + "_soil", cx, cy, z0 + pot_h - 0.06, z0 + pot_h - 0.04, pot_r * 1.01, "soil", 48)
    twigs = []

    def grow(p, d, length, rad, depth):
        pts, rads = [p], [rad]
        n = 6
        for i in range(n):
            d = (d + Vector((r.uniform(-0.25, 0.25), r.uniform(-0.25, 0.25), r.uniform(-0.05, 0.2)))).normalized()
            p = p + d * (length / n)
            pts.append(p)
            rads.append(rad * (1 - 0.6 * (i + 1) / n))
        tube(name + "_br", [tuple(q) for q in pts], rads, "bark", 8)
        if depth == 0:
            twigs.extend(pts[2:])
            return
        for k in range(r.randint(2, 4)):
            i = r.randint(2, n)
            nd = (d + Vector((r.uniform(-0.9, 0.9), r.uniform(-0.9, 0.9), r.uniform(0.1, 0.6)))).normalized()
            grow(pts[i], nd, length * r.uniform(0.55, 0.75), rads[i] * 0.8, depth - 1)

    grow(Vector((cx, cy, z0 + pot_h - 0.05)), Vector((0.05, 0.02, 1)).normalized(), height * 0.5, 0.055 * height / 2.3, 3)
    V, F, LR = [], [], []
    for k in range(leaves):
        t = r.choice(twigs)
        c = t + Vector((r.gauss(0, 0.10), r.gauss(0, 0.10), r.gauss(0, 0.08)))
        dvec = Vector((r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-0.3, 0.9))).normalized()
        side = dvec.cross(Vector((0, 0, 1)))
        if side.length < 0.1:
            side = Vector((1, 0, 0))
        side.normalize()
        up = side.cross(dvec).normalized()
        ln, wd = r.uniform(0.06, 0.09), r.uniform(0.010, 0.015)
        b0 = len(V)
        V += [tuple(c), tuple(c + dvec * ln * 0.5 + side * wd + up * 0.003), tuple(c + dvec * ln), tuple(c + dvec * ln * 0.5 - side * wd + up * 0.003)]
        F.append((b0, b0 + 1, b0 + 2, b0 + 3))
        LR.append(r.random())
    me = bpy.data.meshes.new(name + "_leaves")
    me.from_pydata(V, [], F)
    me.update()
    at = me.attributes.new("lrand", "FLOAT", "FACE")
    at.data.foreach_set("value", LR)
    me.materials.append(M["leaf"])
    ob = bpy.data.objects.new(name + "_leaves", me)
    KW.link(ob)
    own(ob)


def branches_vase(name, cx, cy, z, h=0.42, r=0.09, mat="ceramic_clay", n=6, reach=0.35):
    cyl(name, cx, cy, z, z + h, r, mat, 32, r_top=r * 0.55)
    for k in range(n):
        a_ = rnd.uniform(0, 6.28)
        tube(name + "_stem", [(cx, cy, z + h - 0.1), (cx + reach * 0.4 * math.cos(a_), cy + reach * 0.4 * math.sin(a_), z + h + 0.45),
                              (cx + reach * math.cos(a_), cy + reach * math.sin(a_), z + h + 0.85)], 0.004, "bark", 5)


def books(cx, cy, z, rot=0.0):
    for k, (mt, h) in enumerate((("paper_a", 0.035), ("paper_b", 0.028), ("paper_d", 0.03))):
        box("book%d" % k, cx, cy, z + 0.034 * k, 0.30 - 0.02 * k, 0.23, h - 0.002, mt, rot + 12 - 9 * k, bev=0.003)


# ============================================================================================ lights, camera, report
def light(name, kind, loc, energy, color=(1.0, 0.82, 0.62), size=0.1, size_y=None, aim=None, spot=None, blend=0.6,
          spread=None):
    """a lamp in the room frame; aim = the direction it shines (frame vector); lamps are not seen by the camera or in
    reflections (the emitting surfaces modelled with them are)"""
    ld = bpy.data.lights.new(name, kind)
    ld.energy = energy
    ld.color = color
    if kind == "AREA":
        ld.shape = "RECTANGLE" if size_y else "DISK"
        ld.size = size
        if size_y:
            ld.size_y = size_y
        if spread:
            ld.spread = spread * DEG
    else:
        ld.shadow_soft_size = size
    if kind == "SPOT":
        ld.spot_size = (spot or 60.0) * DEG
        ld.spot_blend = blend
    ob = bpy.data.objects.new(name, ld)
    KW.link(ob)
    own(ob)
    ob.location = loc
    if aim is not None:
        ob.rotation_euler = Vector(aim).normalized().to_track_quat("-Z", "Y").to_euler()
    ob.visible_camera = False
    ob.visible_glossy = False
    return ob


def downlight(name, x, y, zc, energy, spot=60.0, color=(1.0, 0.83, 0.62), r=0.045):
    cyl(name + "_rim", x, y, zc - 0.004, zc - 0.001, r + 0.015, "downlight_rim", 24)
    cyl(name + "_em", x, y, zc - 0.005, zc - 0.004, r, "downlight_emit", 20)
    light(name, "SPOT", (x, y, zc - 0.03), energy, color, 0.03, aim=(0, 0, -1), spot=spot, blend=0.55)


CAM = None


def camera(x, y, z, yaw=0.0):
    global CAM
    cd = bpy.data.cameras.new("cam")
    cd.clip_start = 0.05
    cd.clip_end = 90000.0
    cd.type = "PANO"
    cd.panorama_type = "EQUIRECTANGULAR"
    CAM = bpy.data.objects.new("cam", cd)
    KW.link(CAM)
    own(CAM)
    if os.environ.get("KF_EYE"):
        x, y, z = (float(v) for v in os.environ["KF_EYE"].split(","))
    CAM.location = (x, y, z)
    CAM.rotation_euler = (90 * DEG, 0, -yaw * DEG)
    bpy.context.scene.camera = CAM
    return CAM


def yaw_pitch(px, py, pz):
    """a room-frame point as yaw (degrees right of the panorama's centre), pitch and distance from the camera"""
    c = CAM.location
    dx, dy, dz = px - c.x, py - c.y, pz - c.z
    return math.degrees(math.atan2(dx, dy)), math.degrees(math.atan2(dz, math.hypot(dx, dy))), math.sqrt(dx * dx + dy * dy + dz * dz)


def bearing_world(p):
    c = W_of(CAM.location.x, CAM.location.y, CAM.location.z)
    return math.degrees(math.atan2(p.x - c.x, p.y - c.y)) % 360


def report(label, marks, doors):
    print("REPORT %s | panorama centre bearing %.1f | eye %.2f m above the room's floor (floor %.2f m)" % (label, FACE, CAM.location.z, Z0))
    for nm, (px, py, pz) in marks:
        yw, pt, d = yaw_pitch(px, py, pz)
        print("REPORT    %-40s yaw %+7.1f pitch %+5.1f dist %6.1f m bearing %6.1f" % (nm, yw, pt, d, (FACE + yw) % 360))
    for nm, (px, py, pz) in doors:
        yw, pt, d = yaw_pitch(px, py, pz)
        print("DOOR %s yaw %+.1f pitch %+.1f dist %.2f m bearing %.1f" % (nm, yw, pt, d, (FACE + yw) % 360))


def diagnostics():
    if os.environ.get("KF_DIAG"):                    # a diagnostic script run on the built scene (no render)
        exec(open(os.environ["KF_DIAG"], encoding="utf-8").read())
        raise SystemExit(0)
    probe = os.environ.get("KF_PROBE")
    if probe:
        bpy.context.view_layer.update()             # the parented camera's and objects' world matrices (only the lobby's
        dg = bpy.context.evaluated_depsgraph_get()  # build updates them itself); a diagnostic run only, never a render
        cw = CAM.matrix_world
        for item in probe.split(","):
            yw, pt = (math.radians(float(v)) for v in item.split(":"))
            d_local = Vector((math.sin(yw) * math.cos(pt), math.sin(pt), -math.cos(yw) * math.cos(pt)))
            d_world = (cw.to_3x3() @ d_local).normalized()
            o = cw.translation.copy()
            for hop in range(5):
                hit, loc, nrm, idx, ob, _ = bpy.context.scene.ray_cast(dg, o, d_world)
                if not hit:
                    print("PROBE", item, "hop", hop, "-> sky")
                    break
                print("PROBE", item, "hop", hop, "->", ob.name, ob.active_material.name if ob.active_material else "-", "%.2f m" % (loc - cw.translation).length)
                o = loc + d_world * 0.002
        raise SystemExit(0)
    locate = os.environ.get("KF_LOCATE")
    if locate:
        bpy.context.view_layer.update()             # as KF_PROBE: fresh world matrices (a diagnostic run only)
        inv = CAM.matrix_world.inverted()
        for name in locate.split(","):
            ob = bpy.data.objects.get(name)
            if not ob:
                print("LOCATE", name, "-> missing")
                continue
            c = sum((ob.matrix_world @ Vector(v) for v in ob.bound_box), Vector()) / 8.0
            p = inv @ c
            print("LOCATE %s yaw %+.2f pitch %+.2f dist %.2f m" % (name, math.degrees(math.atan2(p.x, -p.z)),
                                                                 math.degrees(math.atan2(p.y, math.hypot(p.x, p.z))), p.length))
        raise SystemExit(0)


# ============================================================================================ 1. the lobby of tower C
LCEIL = 7.05                                     # the lobby's ceiling (double height, an illustration)
GTOP = 2 * MOD["fh"] - FF                        # floor 3's slab underside, room-local (7.53)
DOOR_H = 2.85                                    # the lift portals' head
EYE_L = (0.0, 8.6, 1.6)


NEAR_TREES = 320.0


def near_leaf_mat():
    """the near trees' leaves: clusters of leaves in greens (a tone per cluster and per tree), light through them"""
    def build(b):
        geo = b.n("ShaderNodeNewGeometry")
        lr = b.attr("lrand").outputs["Fac"]
        oi = b.n("ShaderNodeObjectInfo")
        tone = b.m("ADD", b.m("MULTIPLY", lr, 0.65), b.m("MULTIPLY", oi.outputs["Random"], 0.35))
        col = b.ramp(tone, [(0.0, (0.026, 0.048, 0.016)), (0.35, (0.050, 0.085, 0.026)), (0.7, (0.080, 0.112, 0.036)),
                            (1.0, (0.115, 0.130, 0.052))])
        col = b.mix(geo.outputs["Backfacing"], col, b.mix(0.45, col, (0.17, 0.21, 0.09)))
        p = b.principled(Base_Color=col, Roughness=0.55)
        b.put(p.inputs["Specular IOR Level"], 0.35)
        tr = b.n("ShaderNodeBsdfTranslucent", {"Color": (0.13, 0.19, 0.045)})
        return b.mixs(0.25, p.outputs[0], tr.outputs[0])
    return ext_mat("near_leaf", build)


def crown_variant(k, leaf, bark, n_cards=3400):
    """one crown in unit size (radius 1, height radius 0.82, its centre at the origin): 9-14 clumps of leaf clusters on
    their branches, a darker inner mass; scaled by each tree's radius"""
    r = random.Random(900 + k)
    clumps = []
    for i in range(r.randint(9, 14)):
        v = Vector((r.gauss(0, 1), r.gauss(0, 1), r.gauss(0, 1) * 0.8 + 0.3)).normalized()
        rad = r.uniform(0.42, 0.78)
        clumps.append(Vector((v.x * rad, v.y * rad, v.z * rad * 0.82)))
    V, F, LR, MI = [], [], [], []
    for i in range(n_cards):
        c = r.choice(clumps)
        p = c + Vector((r.gauss(0, 0.25), r.gauss(0, 0.25), r.gauss(0, 0.20)))
        e = math.sqrt(p.x * p.x + p.y * p.y + (p.z / 0.82) ** 2)
        if e > 0.98:
            p *= 0.98 / e
        nrm = (p.normalized() * 0.6 + Vector((r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-0.4, 1.0))) * 0.6).normalized()
        a = nrm.orthogonal().normalized()
        bv = nrm.cross(a)
        t = r.uniform(0, 6.283)
        a, bv = a * math.cos(t) + bv * math.sin(t), -a * math.sin(t) + bv * math.cos(t)
        s = r.uniform(0.042, 0.072)
        b0 = len(V)
        V += [tuple(p + a * s), tuple(p + bv * s * 0.55), tuple(p - a * s), tuple(p - bv * s * 0.55)]
        F.append((b0, b0 + 1, b0 + 2, b0 + 3))
        LR.append(r.random())
        MI.append(0)
    # the inner mass (keeps the crown from reading as a sieve)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.52)
    b0 = len(V)
    for v in bm.verts:
        j = 1.0 + r.uniform(-0.12, 0.12)
        V.append((v.co.x * j, v.co.y * j, v.co.z * 0.82 * j + 0.04))
    for f in bm.faces:
        F.append(tuple(b0 + v.index for v in f.verts))
        LR.append(0.05)
        MI.append(0)
    bm.free()
    # the branches: from the trunk's top into the clumps
    seg = 6
    for c in clumps[:7]:
        p0, p1 = Vector((0, 0, -0.62)), c * 0.92
        tdir = (p1 - p0).normalized()
        u = tdir.cross(Vector((1, 0, 0)) if abs(tdir.x) < 0.9 else Vector((0, 1, 0))).normalized()
        w = tdir.cross(u).normalized()
        b0 = len(V)
        for (pp, rad) in ((p0, 0.028), (p1, 0.010)):
            for q in range(seg):
                an = 2 * math.pi * q / seg
                V.append(tuple(pp + (u * math.cos(an) + w * math.sin(an)) * rad))
        for q in range(seg):
            F.append((b0 + q, b0 + (q + 1) % seg, b0 + seg + (q + 1) % seg, b0 + seg + q))
            LR.append(0.0)
            MI.append(1)
    me = bpy.data.meshes.new("crown%d" % k)
    me.from_pydata(V, [], F)
    me.update()
    me.materials.append(leaf)
    me.materials.append(bark)
    me.polygons.foreach_set("material_index", MI)
    at = me.attributes.new("lrand", "FLOAT", "FACE")
    at.data.foreach_set("value", LR)
    return me


def near_trees(trees):
    """the canopy's trees near the lobby: each at its place and radius from the world's data, at the world's size rule
    (trunk 2 + 0.35 r, crown r), a crown variant instanced, scaled and turned; a tapered trunk"""
    leaf = near_leaf_mat()
    bark = KW.MAT.get("bark") or M["bark"]
    variants = [crown_variant(k, leaf, bark) for k in range(8)]
    rr = random.Random(77)
    tv, tf = [], []
    for (x, y, r) in trees:
        r = max(1.2, r)
        h0 = 2.0 + 0.35 * r
        cz = h0 + 0.86 * r
        j = 1.0 + rr.uniform(-0.08, 0.08)
        ob = bpy.data.objects.new("ntree", variants[rr.randrange(len(variants))])
        KW.link(ob)
        ob.location = (x, y, cz)
        ob.scale = (r * j, r * j * rr.uniform(0.9, 1.1), r * j)
        ob.rotation_euler = (0, 0, rr.uniform(0, 6.283))
        seg = 7
        rb, rt = 0.08 + 0.025 * r, 0.045 + 0.012 * r
        top = cz - 0.5 * r
        b0 = len(tv)
        for (zz, rad) in ((0.0, rb), (top, rt)):
            for q in range(seg):
                an = 2 * math.pi * q / seg
                tv.append((x + rad * math.cos(an), y + rad * math.sin(an), zz))
        for q in range(seg):
            tf.append((b0 + q, b0 + (q + 1) % seg, b0 + seg + (q + 1) % seg, b0 + seg + q))
    KW.mesh_object("near_trunks", tv, tf, [bark])
    print("NEAR TREES %d (within %.0f m of the eye), %d crown variants" % (len(trees), NEAR_TREES, len(variants)))


def lobby_world():
    """kikar_world's city around the lobby: the towers (tower C's floors 1-2 left to this script), every building, the
    ground, the park and the pond, the canopy's trees, the cars; then the near field made fit for a 1.6 m eye"""
    KW.build_sky(TODN)
    eye = W_of(*EYE_L)
    KW.build_towers(skip=lambda key, fl, phi: key == "C" and fl <= 2)
    KW.build_blocks(eye)
    KW.build_ground(eye)
    # the city's canopy: kikar_world's crowns beyond 320 m; nearer, the same trees (place and radius from the data) built
    # leaf by leaf for an eye at 1.6 m (crown variants as instances; an illustration of each crown's form)
    allt = KW.W["trees"]
    near = [t for t in allt if math.hypot(t[0] - eye.x, t[1] - eye.y) < NEAR_TREES]
    KW.W["trees"] = [t for t in allt if math.hypot(t[0] - eye.x, t[1] - eye.y) >= NEAR_TREES]
    KW.build_trees(eye)
    KW.W["trees"] = allt
    near_trees(near)
    KW.build_cars(eye)
    # the double-height lobby: floor 2's slab of tower C is left out
    ob = bpy.data.objects["towerC_slabs"]
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    kill = [f for f in bm.faces if all(MOD["fh"] - 0.1 < v.co.z < MOD["fh"] + MOD["slab_t"] + 0.1 for v in f.verts)]
    bmesh.ops.delete(bm, geom=kill, context="FACES")
    bm.to_mesh(ob.data)
    bm.free()
    # the GIS street lines run under the new towers (the old layout): their parked cars within 40 m are left out
    ob = bpy.data.objects["cars"]
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.faces.ensure_lookup_table()
    kill = []
    for i in range(0, len(bm.faces), 6):
        fs = bm.faces[i:i + 6]
        c = sum((v.co for f in fs for v in f.verts), Vector()) / (4 * len(fs))
        if math.hypot(c.x - CT.x, c.y - CT.y) < 40.0:
            kill += fs
    bmesh.ops.delete(bm, geom=kill, context="FACES")
    bm.to_mesh(ob.data)
    bm.free()
    # the park's lawn and the pond: the world's outlines, surfaces for an eye at 1.6 m
    lawn = lawn_mat()
    bpy.data.objects["park"].data.materials[0] = lawn
    bpy.data.objects["pond"].data.materials[0] = pond_mat()
    # the tower's base: a stone terrace at the lobby's level, three steps, a paved plaza (an illustration), in the frame
    terr = paver_mat("terrace", (0.62, 0.58, 0.52), 1.2, 0.6, 0.005, 0.35, 0.5)
    plaza = paver_mat("plaza", (0.50, 0.47, 0.43), 0.6, 0.3, 0.008, 0.6, 0.65)
    gl = outline_frame(AG, 144)
    ring = lambda s: [(x * s, y * s) for (x, y) in gl]
    ring_prism("terrace", ring((AG + 3.6) / AG), ring((AG - 0.05) / AG), -FF, -0.012, terr)
    for k, (w, top) in enumerate(((0.4, 0.32), (0.4, 0.19))):
        s0 = (AG + 3.6 + 0.4 * k) / AG
        ring_prism("step%d" % k, ring(s0 + w / AG), ring(s0), -FF, top - FF, terr)
    cdisc = circle(27.0, 180)
    poly_prism("plaza", cdisc, -FF, 0.05 - FF, plaza)
    return eye


def lobby_materials():
    stone_tiles("lobby_floor", (0.66, 0.61, 0.53), 1.2, 0.6, 0.003, 0.24, "XY", 0.9, 0.5, 0.5)
    stone_tiles("ring_stone", (0.20, 0.19, 0.18), 0.6, 0.6, 0.002, 0.22, "XY", 0.6, 0.3)
    concrete("core_concrete", (0.50, 0.48, 0.445))
    plaster("lobby_ceiling", (0.84, 0.83, 0.80))
    pmat("walnut_ceiling", (0.06, 0.04, 0.028), 0.6)
    glass_pull("lobby_glass", float(os.environ.get("KF_PULL", "0.55")))
    travertine("desk_trav", (0.80, 0.73, 0.62), flute=("Y", 0.045), rough=0.38)
    travertine("travertine", (0.78, 0.71, 0.60))
    marble("table_marble", (0.13, 0.12, 0.12), (0.60, 0.58, 0.55), (0.52, 0.44, 0.32), (0.11, 0.105, 0.10))
    pmat("mat_coir", (0.10, 0.085, 0.065), 1.0, bump=0.8, bump_scale=300.0)
    pmat("opal", (0.95, 0.93, 0.90), 0.3, emission=((1.0, 0.82, 0.60), 6.0), subsurf=0.2)
    pmat("shade_linen", (0.88, 0.85, 0.78), 0.9, sheen=0.5)
    pmat("screen_dark", (0.012, 0.013, 0.016), 0.08, coat=0.6, emission=((0.55, 0.62, 0.70), 0.25))
    emit("cove_led", (1.0, 0.78, 0.55), 28.0)


def lobby_facade():
    """floor 1-2's curtain wall, double height: glass to the ceiling, a white spandrel to floor 3's slab, white aluminium
    mullions at the world's fin positions (every 1.5 m), the 300 mm fins outside (none at a side's middle, as world.js),
    a transom at floor 2's line; the entrance doors in the north-west glass"""
    P = outline_frame(AG, 144)
    n = len(P)
    door = [k for k in range(n) if (P[k][0] + P[(k + 1) % n][0]) / 2 > 10 and 2.6 < (P[k][1] + P[(k + 1) % n][1]) / 2 < 5.5]
    DH = 3.05
    gv, gf, sv, sf = [], [], [], []
    for k in range(n):
        (x0, y0), (x1, y1) = P[k], P[(k + 1) % n]
        zb = DH if k in door else -0.02
        b0 = len(gv)
        gv += [(x0, y0, zb), (x1, y1, zb), (x1, y1, LCEIL), (x0, y0, LCEIL)]
        gf.append((b0, b0 + 1, b0 + 2, b0 + 3))
        b1 = len(sv)
        sv += [(x0, y0, LCEIL), (x1, y1, LCEIL), (x1, y1, GTOP), (x0, y0, GTOP)]
        sf.append((b1, b1 + 1, b1 + 2, b1 + 3))
    obj("lobby_glass", gv, gf, "lobby_glass")
    obj("spandrel", sv, sf, "alu_white")
    # mullions and fins (the world's rule, on the 144-point plate outline)
    go = KW.plate_outline(AG, NEXP, 144)
    glen = [0.0]
    for k in range(1, len(go) + 1):
        glen.append(glen[-1] + math.dist(go[k - 1], go[k % len(go)]))
    per = glen[-1]
    nfin = int(per / 1.5)
    ys = [P[k][1] for k in door] + [P[(k + 1) % n][1] for k in door]
    dy0, dy1 = min(ys), max(ys)
    sw_mull = []
    for q in range(nfin):
        sq = (q + 0.5) * per / nfin
        k = next((kk for kk in range(len(go)) if glen[kk + 1] >= sq), len(go) - 1)
        f = (sq - glen[k]) / max(1e-6, glen[k + 1] - glen[k])
        a, bb = go[k], go[(k + 1) % len(go)]
        pu, pv = a[0] + (bb[0] - a[0]) * f, a[1] + (bb[1] - a[1]) * f
        tu, tv = bb[0] - a[0], bb[1] - a[1]
        tl = math.hypot(tu, tv)
        tu, tv = tu / tl, tv / tl
        nu, nv = tv, -tu
        if nu * pu + nv * pv < 0:
            nu, nv = -nu, -nv
        X, Y, TX, TY, NX, NY = -pv, -pu, -tv, -tu, -nv, -nu
        if X > 10 and dy0 - 0.4 < Y < dy1 + 0.4:
            continue
        rot = math.degrees(math.atan2(TY, TX))
        if Y > AG - 0.5:
            sw_mull.append(X)
        box("mullion%d" % q, X - NX * 0.085, Y - NY * 0.085, -0.02, 0.06, 0.16, LCEIL + 0.02, "alu_white", rot)
        phi = math.degrees(math.atan2(pv, pu))
        side_phi = min(abs(((phi - c + 180) % 360) - 180) for c in (0, 90, 180, 270))
        if side_phi >= 16.3:
            box("fin%d" % q, X + NX * 0.16, Y + NY * 0.16, -0.012, 0.05, 0.30, GTOP + 0.012, "alu_white", rot)
    # the transom at floor 2's line
    s_out, s_in = (AG - 0.005) / AG, (AG - 0.13) / AG
    ring_prism("transom", [(x * s_out, y * s_out) for (x, y) in P], [(x * s_in, y * s_in) for (x, y) in P],
               MOD["fh"] - FF - 0.05, MOD["fh"] - FF + 0.04, "alu_white")
    # the entrance: two glass leaves in bronze frames, a bronze head and jambs, pulls, a coir mat inside
    xd = sum(P[k][0] for k in door) / len(door) - 0.01
    yc = (dy0 + dy1) / 2
    wd = dy1 - dy0
    for t in (-1, 1):
        lc = yc + t * wd / 4
        obj("door_leaf%d" % t, [(xd, lc - wd / 4 + 0.03, 0.03), (xd, lc + wd / 4 - 0.03, 0.03), (xd, lc + wd / 4 - 0.03, DH - 0.06),
                                (xd, lc - wd / 4 + 0.03, DH - 0.06)], [(0, 1, 2, 3)], "lobby_glass")
        for (ya, yb) in ((lc - wd / 4, lc - wd / 4 + 0.05), (lc + wd / 4 - 0.05, lc + wd / 4)):
            gbox("door_stile", xd - 0.025, xd + 0.025, ya, yb, 0.0, DH - 0.05, "bronze")
        gbox("door_rail_b", xd - 0.025, xd + 0.025, lc - wd / 4, lc + wd / 4, 0.0, 0.12, "bronze")
        gbox("door_rail_t", xd - 0.025, xd + 0.025, lc - wd / 4, lc + wd / 4, DH - 0.11, DH - 0.05, "bronze")
        rod("door_pull%d" % t, (xd - 0.09, yc + t * 0.16, 0.75), (xd - 0.09, yc + t * 0.16, 2.05), 0.016, "bronze", 12)
        for zz in (0.85, 1.95):
            rod("door_pull_post", (xd - 0.09, yc + t * 0.16, zz), (xd - 0.02, yc + t * 0.16, zz), 0.008, "bronze", 8)
    gbox("door_head", xd - 0.06, xd + 0.06, dy0 - 0.06, dy1 + 0.06, DH - 0.05, DH + 0.06, "bronze")
    for yy in (dy0, dy1):
        gbox("door_jamb", xd - 0.07, xd + 0.07, yy - 0.04, yy + 0.04, 0.0, DH, "bronze")
    gbox("entrance_mat", xd - 2.0, xd - 0.15, yc - 1.4, yc + 1.4, 0.0, 0.012, "mat_coir", bev=0.004)
    sw_mull.sort()
    m0 = min(sw_mull, key=abs)
    m1 = min((m for m in sw_mull if m > m0), default=m0 + 1.5)
    return (xd, yc), (m0 + m1) / 2


def lobby_core():
    """the round slip-formed core (published), fair-faced, three lift portals in bronze on its south-west face"""
    T_ = 0.35
    ops = (-26.0, 0.0, 26.0)
    ha = math.degrees(0.70 / RC)
    edges = []
    for a in ops:
        edges += [a - ha, a + ha]
    # the wall below the door heads, in pieces between the openings; the wall above in one ring
    pieces = [(edges[1], edges[2]), (edges[3], edges[4]), (edges[5], 360.0 + edges[0])]
    for i, (a0, a1) in enumerate(pieces):
        sector("core_low%d" % i, a0, a1, RC - T_, RC, -0.05, DOOR_H, "core_concrete")
    ring_prism("core_high", circle(RC, 180), circle(RC - T_, 180), DOOR_H, GTOP + 0.3, "core_concrete")
    lifts = []
    for i, a in enumerate(ops):
        n_ = Vector((math.sin(a * DEG), math.cos(a * DEG), 0))
        t_ = Vector((math.cos(a * DEG), -math.sin(a * DEG), 0))
        rot = math.degrees(math.atan2(t_.y, t_.x))
        c = n_ * (RC - 0.29)
        for s in (-1, 1):
            p = c + t_ * (s * 0.275)
            box("lift%d_leaf%d" % (i, s), p.x, p.y, 0.0, 0.545, 0.03, 2.62, "bronze", rot, bev=0.003)
        p = c - n_ * 0.03
        box("lift%d_back" % i, p.x, p.y, 0.0, 1.40, 0.02, DOOR_H, "shadowgap", rot)
        for s in (-1, 1):
            p = n_ * (RC - 0.15) + t_ * (s * 0.69)
            box("lift%d_jamb" % i, p.x, p.y, 0.0, 0.02, 0.30, DOOR_H, "bronze", rot)
        p = n_ * (RC - 0.15)
        box("lift%d_head" % i, p.x, p.y, 2.62, 1.40, 0.30, DOOR_H - 2.62, "bronze", rot)
        p = n_ * (RC + 0.006)
        box("lift%d_ind" % i, p.x, p.y, 3.05, 0.62, 0.012, 0.07, "black_glass", rot)
        lifts.append((n_.x * (RC - 0.29), n_.y * (RC - 0.29), 1.3))
    for i, a in enumerate((-13.0, 13.0)):
        n_ = Vector((math.sin(a * DEG), math.cos(a * DEG), 0))
        t_ = Vector((math.cos(a * DEG), -math.sin(a * DEG), 0))
        p = n_ * (RC + 0.006)
        box("lift_call%d" % i, p.x, p.y, 1.02, 0.075, 0.012, 0.22, "steel", math.degrees(math.atan2(t_.y, t_.x)), bev=0.003)
    return lifts


def lobby_ceiling():
    """the ceiling: plaster, a raised round coffer around the core (the square's circle) lit by a hidden cove, a shadow
    gap with a light line at the core, downlights beyond"""
    P = outline_frame(AG, 144)
    R1 = 9.5
    flat_ring("ceiling_outer", P, polar_match(P, R1), LCEIL, "lobby_ceiling")
    flat_ring("ceiling_coffer", circle(R1, 180), circle(RC + 0.15, 180), LCEIL + 0.45, "walnut_ceiling")
    r_ = RC + 0.42
    while r_ < R1 - 0.40:
        ring_prism("coffer_slat", circle(r_ + 0.025, 180), circle(r_ - 0.025, 180), LCEIL + 0.33, LCEIL + 0.43, "walnut")
        r_ += 0.11
    ob = ring_prism("coffer_side", circle(R1 + 0.03, 180), circle(R1, 180), LCEIL - 0.001, LCEIL + 0.46, "lobby_ceiling")
    ring_prism("coffer_ledge", circle(R1, 180), circle(R1 - 0.26, 180), LCEIL + 0.10, LCEIL + 0.135, "lobby_ceiling")
    flat_ring("coffer_led", circle(R1 - 0.12, 180), circle(R1 - 0.15, 180), LCEIL + 0.137, "cove_led", down=False)
    flat_ring("core_gap_top", circle(RC + 0.15, 180), circle(RC, 180), LCEIL + 0.9, "shadowgap")
    flat_ring("core_gap_led", circle(RC + 0.14, 180), circle(RC + 0.11, 180), LCEIL + 0.62, "cove_led")
    # the cove's light on the coffer: area lamps on the ledge, facing up
    for k in range(16):
        a = 2 * math.pi * k / 16
        light("cove%d" % k, "AREA", ((R1 - 0.13) * math.sin(a), (R1 - 0.13) * math.cos(a), LCEIL + 0.15), 26.0, (1.0, 0.80, 0.58),
              0.5, None, aim=(0, 0, 1), spread=160)
    # grazing scallops on the round core, from small adjustable downlights in the coffer
    for k in range(20):
        a = 2 * math.pi * (k + 0.5) / 20
        p = Vector(((RC + 0.32) * math.sin(a), (RC + 0.32) * math.cos(a), LCEIL + 0.40))
        tgt = Vector((RC * math.sin(a), RC * math.cos(a), 0.6))
        light("graze%d" % k, "SPOT", tuple(p), 55.0, (1.0, 0.80, 0.58), 0.02, aim=tuple(tgt - p), spot=32.0, blend=0.35)
        cyl("graze_rim%d" % k, p.x, p.y, LCEIL + 0.446, LCEIL + 0.449, 0.045, "downlight_rim", 20)
        cyl("graze_em%d" % k, p.x, p.y, LCEIL + 0.445, LCEIL + 0.446, 0.028, "downlight_emit", 16)
    # downlights beyond the coffer
    pts = []
    for i in range(-6, 7):
        for j in range(-6, 7):
            x, y = i * 2.6, j * 2.6
            if math.hypot(x, y) < R1 + 0.9:
                continue
            if abs(x) ** NEXP + abs(y) ** NEXP > (AG - 1.1) ** NEXP:
                continue
            pts.append((x, y))
    for k, (x, y) in enumerate(pts):
        downlight("dl%d" % k, x, y, LCEIL, 26.0, 60.0)


def lobby_desk(cx=-8.2, cy=6.0):
    """the concierge desk (the listing's security guard): a fluted travertine counter facing the entrance across the
    lobby, a walnut ledge, a work top behind, a screen of walnut slats behind it"""
    L, D = 3.4, 0.85
    x0, x1 = cx - D / 2, cx + D / 2
    gbox("desk_body", x0 + 0.06, x1, cy - L / 2, cy + L / 2, 0.08, 1.06, "desk_trav", bev=0.004)
    gbox("desk_plinth", x0 + 0.12, x1 - 0.06, cy - L / 2 + 0.06, cy + L / 2 - 0.06, 0.0, 0.08, "shadowgap")
    gbox("desk_ledge", x0 + 0.20, x1 + 0.06, cy - L / 2 - 0.04, cy + L / 2 + 0.04, 1.06, 1.11, "walnut", bev=0.006)
    gbox("desk_brass", x1 + 0.0, x1 + 0.006, cy - L / 2, cy + L / 2, 0.08, 0.10, "brass")
    gbox("desk_work", x0 - 0.20, x0 + 0.20, cy - L / 2 + 0.05, cy + L / 2 - 0.05, 0.74, 0.78, "walnut", bev=0.005)
    # a monitor, a keyboard, a lamp, flowers
    box("desk_monitor", x0 + 0.05, cy - 0.5, 0.95, 0.03, 0.56, 0.34, "screen_dark", 0, bev=0.004)
    box("desk_monitor_stand", x0 + 0.07, cy - 0.5, 0.78, 0.04, 0.05, 0.17, "blacksteel", 0)
    box("desk_keys", x0 - 0.10, cy - 0.5, 0.78, 0.14, 0.40, 0.015, "blacksteel", 0, bev=0.003)
    cyl("desk_lamp_base", x0 + 0.02, cy + 1.15, 1.11, 1.13, 0.07, "brass", 24)
    cyl("desk_lamp_stem", x0 + 0.02, cy + 1.15, 1.13, 1.48, 0.007, "brass", 8)
    sphere("desk_lamp_globe", x0 + 0.02, cy + 1.15, 1.55, 0.085, "opal")
    light("desk_lamp", "POINT", (x0 + 0.02, cy + 1.15, 1.55), 7.0, (1.0, 0.78, 0.55), 0.07)
    branches_vase("desk_vase", x1 - 0.12, cy + 0.85, 1.11, 0.30, 0.07, "ceramic_white", 5, 0.25)
    # the guard's chair
    P = Pr(x0 - 0.55, cy - 0.3, 90)
    x, y = P(0, 0)
    cyl("chair_base", x, y, 0.0, 0.04, 0.32, "blacksteel", 5)
    cyl("chair_post", x, y, 0.04, 0.45, 0.025, "chrome", 16)
    cushion("chair_seat", x, y, 0.45, 0.50, 0.48, 0.09, "leather_black", 90, 0.004, 0.03)
    x, y = P(0, 0.24)
    cushion("chair_back", x, y, 0.58, 0.48, 0.07, 0.52, "leather_black", 90, 0.004, 0.03)
    # the walnut screen behind the desk
    xs = cx - 2.3
    gbox("screen_base", xs - 0.06, xs + 0.06, cy - 2.6, cy + 2.6, 0.0, 0.05, "blacksteel")
    gbox("screen_top", xs - 0.06, xs + 0.06, cy - 2.6, cy + 2.6, 3.85, 3.9, "blacksteel")
    y = cy - 2.55
    while y < cy + 2.56:
        gbox("screen_slat", xs - 0.04, xs + 0.04, y - 0.022, y + 0.022, 0.05, 3.85, "walnut", bev=0.004)
        y += 0.1
    return (x1, cy)


def lobby_furniture():
    # the lounge by the south-west glass (left of the view)
    LX, LY = -6.0, 11.15
    box("rug_l", LX, LY, 0.0, 4.4, 3.4, 0.014, rug("rug_l", (0.72, 0.68, 0.60), LX, LY, 2.2, 1.7), 0, bev=0.004)
    sofa(LX, LY + 1.45, 0.0, 2.9, 1.0, "boucle")
    lounge_chair(LX - 1.2, LY - 1.45, 195.0)
    lounge_chair(LX + 1.2, LY - 1.45, 165.0)
    cyl("coffee", LX, LY, 0.0, 0.34, 0.58, "travertine", 72, bev=0.012)
    cyl("coffee2", LX + 0.95, LY + 0.25, 0.0, 0.26, 0.30, "travertine", 48, bev=0.01)
    books(LX - 0.15, LY + 0.05, 0.34)
    cyl("ctbowl", LX + 0.25, LY - 0.15, 0.34, 0.42, 0.11, "ceramic_clay", 40, r_top=0.13)
    cyl("side_l", LX - 1.95, LY + 1.55, 0.0, 0.52, 0.22, "walnut", 40, bev=0.01)
    cyl("flamp_base", LX + 1.95, LY + 1.65, 0.0, 0.02, 0.17, "brass", 32)
    cyl("flamp_pole", LX + 1.95, LY + 1.65, 0.02, 1.52, 0.012, "brass", 10)
    sh = cyl("flamp_shade", LX + 1.95, LY + 1.65, 1.38, 1.70, 0.22, "shade_linen", 40, r_top=0.19)
    light("flamp", "POINT", (LX + 1.95, LY + 1.65, 1.5), 22.0, (1.0, 0.78, 0.55), 0.08)
    # a cluster of opal globes hanging into the double height over the lounge
    for k, (dx, dy, h) in enumerate(((0.0, 0.0, 3.3), (0.55, 0.45, 3.9), (-0.5, 0.4, 3.6), (0.45, -0.5, 4.3), (-0.55, -0.4, 3.1),
                                      (0.05, 0.85, 4.6), (-0.95, 0.05, 4.1))):
        sphere("globe%d" % k, LX + dx, LY + dy, h, 0.17, "opal")
        cyl("globe_cord%d" % k, LX + dx, LY + dy, h + 0.17, LCEIL, 0.004, "brass", 6)
        if k < 4:
            light("globe_l%d" % k, "POINT", (LX + dx, LY + dy, h - 0.3), 14.0, (1.0, 0.80, 0.58), 0.12)
    cyl("globe_canopy", LX, LY + 0.2, LCEIL - 0.03, LCEIL, 0.35, "brass", 40)
    # two lounge chairs and a marble table by the glass (right of the view)
    lounge_chair(6.1, 12.55, -12.0, "walnut", "linen_sand")
    lounge_chair(8.05, 12.15, 14.0, "walnut", "linen_sand")
    cyl("rtable", 7.05, 11.65, 0.0, 0.48, 0.30, "table_marble", 56, bev=0.01)
    branches_vase("rvase", 7.05, 11.65, 0.48, 0.26, 0.06, "ceramic_white", 4, 0.22)
    # olive trees in stone planters (the double height carries them)
    olive_tree("olive_a", 3.9, 12.9, 3.1, seed=5, pot_r=0.58, pot_h=0.72, leaves=11000)
    olive_tree("olive_b", 11.0, 9.6, 2.8, seed=9, pot_r=0.52, pot_h=0.68, leaves=9000)
    olive_tree("olive_c", -11.2, 9.0, 2.6, seed=13, pot_r=0.5, pot_h=0.65, leaves=8000)
    # a long bench on the core's south-east side
    a = -60.0
    p = Vector((math.sin(a * DEG), math.cos(a * DEG), 0)) * (RC + 0.55)
    box("core_bench", p.x, p.y, 0.0, 2.4, 0.5, 0.44, "travertine", math.degrees(math.atan2(-math.sin(a * DEG), math.cos(a * DEG))), bev=0.01)


def build_lobby():
    lobby_materials()
    lobby_world()
    gl = outline_frame(AG, 144)
    poly_prism("lobby_floor", gl, -0.02, 0.0, "lobby_floor")
    ring_prism("floor_ring", circle(6.75, 180), circle(6.25, 180), -0.01, 0.0015, "ring_stone")
    for r_ in (6.25, 6.75):
        ring_prism("floor_brass", circle(r_ + 0.007, 180), circle(r_ - 0.007, 180), -0.01, 0.002, "brass")
    entrance, eye_x = lobby_facade()
    lifts = lobby_core()
    lobby_ceiling()
    desk = lobby_desk()
    lobby_furniture()
    # portals over the four sides of glass: they guide the sky's light into the hall
    for k, (dx, dy) in enumerate(((0, 1), (1, 0), (0, -1), (-1, 0))):
        ld = bpy.data.lights.new("portal%d" % k, "AREA")
        ld.shape = "RECTANGLE"
        ld.size, ld.size_y = 25.0, LCEIL
        ld.cycles.is_portal = True
        ob = bpy.data.objects.new("portal%d" % k, ld)
        KW.link(ob)
        own(ob)
        ob.location = (dx * (AG - 0.1), dy * (AG - 0.1), LCEIL / 2)
        ob.rotation_euler = Vector((-dx, -dy, 0)).to_track_quat("-Z", "Y").to_euler()
    KW.build_sun()
    camera(eye_x, EYE_L[1], EYE_L[2])                 # between two mullions: the panorama's centre is clear glass
    bpy.context.view_layer.update()
    A, B = KW.W["towers"]["A"], KW.W["towers"]["B"]
    inv = lambda wp: (lambda d: ((d.x * RIGHT.x + d.y * RIGHT.y), (d.x * FWD.x + d.y * FWD.y)))(wp - CT)
    pond = KW.W["pond"]
    pc = Vector((sum(p[0] for p in pond) / len(pond), sum(p[1] for p in pond) / len(pond), 0))
    marks = [("the pond (its centroid, the world's outline)", inv(pc) + (0.1 - FF,)),
             ("tower A (its axis, 20 m up)", inv(KW.tower_xy(A)) + (20.0,)),
             ("tower B (its axis, 20 m up)", inv(KW.tower_xy(B)) + (20.0,)),
             ("the concierge desk", (desk[0], desk[1], 1.0)),
             ("the lounge (the coffee table)", (-6.0, 11.15, 0.34))]
    sunv = KW.dirv(KW.TOD["bearing"])
    sx_, sy_ = sunv.x * RIGHT.x + sunv.y * RIGHT.y, sunv.x * FWD.x + sunv.y * FWD.y
    marks.append(("the sun (%s, %.1f deg high)" % (KW.TOD["label"], KW.TOD["alt"]),
                  (CAM.location.x + sx_ * 100, CAM.location.y + sy_ * 100, CAM.location.z + 100 * math.tan(KW.TOD["alt"] * DEG))))
    doors = [("lobby_main_entrance", (entrance[0], entrance[1], 1.4))]
    for i, (x, y, z) in enumerate(lifts):
        doors.append(("lobby_lift_%d" % (i + 1), (x, y, z)))
    report("lobby: tower C's ground floor, double height (an illustration); the floor %.2f m above the street, ceiling %.2f m "
           "clear, eye %.2f m above the street; %s" % (FF, LCEIL, FF + CAM.location.z, KW.TOD["label"]), marks, doors)


# ============================================================================================ 2. the pool (basement)
PCEIL = 4.8
PX, PY0, PY1 = 3.75, 11.0, 31.0                  # the pool: 7.5 x 20 m (an illustration)
HX0, HX1, HY0, HY1 = -7.5, 7.5, 6.5, 35.0        # the hall
WL = -0.012                                      # the water's surface (a deck-level edge)
GR = 0.30                                        # the overflow grating's width


def build_pool():
    bpy.context.scene.world = _black_world()
    deck = stone_tiles("deck_stone", (0.55, 0.51, 0.45), 1.2, 0.6, 0.003, 0.34, "XY", 0.7, 0.45, 0.62)
    basalt = stone_tiles("basalt_wall", (0.17, 0.162, 0.152), 1.2, 2.4, 0.003, 0.36, "YZ", 0.6, 0.35, 0.4)
    basalt_x = stone_tiles("basalt_far", (0.17, 0.162, 0.152), 1.2, 2.4, 0.003, 0.36, "XZ", 0.6, 0.35, 0.4)
    stone_tiles("bench_stone", (0.15, 0.145, 0.14), 1.8, 0.5, 0.003, 0.34, "XY", 0.6, 0.3, 0.4)
    mosaic("pool_tile", (0.46, 0.60, 0.63), (0.54, 0.68, 0.70), (0.74, 0.77, 0.76), 0.025, ((-2.5, 0.0, 2.5), PY0 + 3.2, PY1 - 2.0),
           0.28, WL)
    mosaic("pool_tile_dark", (0.06, 0.09, 0.12), (0.08, 0.11, 0.14), (0.55, 0.58, 0.58), 0.025)
    pool_water()
    plaster("pool_ceiling", (0.82, 0.81, 0.78))
    onyx("onyx", (1.0, 0.70, 0.40), 2.6, "XZ")
    emit("uw_lens", (0.80, 0.96, 1.0), 22.0)
    emit("cove_led", (1.0, 0.80, 0.58), 16.0)
    emit("strip_led", (1.0, 0.84, 0.66), 24.0)
    grille_mat("grille_y", "Y")
    grille_mat("grille_x", "X")
    pmat("lounger_frame", (0.80, 0.79, 0.77), 0.4, spec=0.5, coat=0.2)
    fabric("cushion_white", (0.86, 0.84, 0.79), "linen")
    # the deck, around the pool and its grating
    gx0, gx1, gy0, gy1 = -PX - GR, PX + GR, PY0 - GR, PY1 + GR
    for nm, a in (("l", (HX0, gx0, HY0, HY1)), ("r", (gx1, HX1, HY0, HY1)), ("n", (gx0, gx1, HY0, gy0)), ("f", (gx0, gx1, gy1, HY1))):
        gbox("deck_" + nm, a[0], a[1], a[2], a[3], -0.3, 0.0, deck)
    gbox("grille_l", gx0, -PX, gy0, gy1, -0.3, -0.003, "grille_y")
    gbox("grille_r", PX, gx1, gy0, gy1, -0.3, -0.003, "grille_y")
    gbox("grille_n", -PX, PX, gy0, PY0, -0.3, -0.003, "grille_x")
    gbox("grille_f", -PX, PX, PY1, gy1, -0.3, -0.003, "grille_x")
    # the basin: mosaic walls and floor, steps across the near end, dark nosings
    FLZ = -1.40
    gbox("pool_floor", -PX, PX, PY0, PY1, FLZ - 0.1, FLZ, "pool_tile")
    gbox("pool_wall_l", -PX - 0.2, -PX, PY0 - 0.2, PY1 + 0.2, FLZ - 0.1, -0.3, "pool_tile")
    gbox("pool_wall_r", PX, PX + 0.2, PY0 - 0.2, PY1 + 0.2, FLZ - 0.1, -0.3, "pool_tile")
    gbox("pool_wall_n", -PX, PX, PY0 - 0.2, PY0, FLZ - 0.1, -0.3, "pool_tile")
    gbox("pool_wall_f", -PX, PX, PY1, PY1 + 0.2, FLZ - 0.1, -0.3, "pool_tile")
    for k in range(3):
        top = -0.35 * (k + 1)
        y0, y1 = PY0, PY0 + 0.45 * (k + 1)
        gbox("pool_step%d" % k, -PX, PX, y0, y1, FLZ, top, "pool_tile")
        gbox("pool_nosing%d" % k, -PX, PX, y1 - 0.05, y1 + 0.001, top - 0.05, top + 0.001, "pool_tile_dark")
    obj("pool_water", [(-PX, PY0, WL), (PX, PY0, WL), (PX, PY1, WL), (-PX, PY1, WL)], [(0, 1, 2, 3)], "pool_water")
    # underwater lights in the long walls, a pair in the far wall
    for s in (-1, 1):
        for k, y in enumerate((15.0, 19.0, 23.0, 27.0)):
            rod("uw_lens_%d_%d" % (s, k), (s * (PX + 0.001), y, -0.62), (s * (PX - 0.018), y, -0.62), 0.11, "uw_lens", 24)
            rod("uw_ring_%d_%d" % (s, k), (s * (PX + 0.001), y, -0.62), (s * (PX - 0.012), y, -0.62), 0.135, "steel", 24)
            light("uw_%d_%d" % (s, k), "SPOT", (s * (PX - 0.06), y, -0.62), 26.0, (0.80, 0.95, 1.0), 0.06, aim=(-s, 0, 0.05), spot=110.0, blend=0.8)
    for k, x in enumerate((-1.6, 1.6)):
        rod("uw_lens_f%d" % k, (x, PY1 - 0.001, -0.62), (x, PY1 - 0.018, -0.62), 0.11, "uw_lens", 24)
        light("uw_f%d" % k, "SPOT", (x, PY1 - 0.06, -0.62), 26.0, (0.80, 0.95, 1.0), 0.06, aim=(0, -1, 0.05), spot=110.0, blend=0.8)
    # the walls: basalt on the left, oak slats on the right and behind, the backlit onyx at the far end
    gbox("wall_l", HX0 - 0.2, HX0, HY0, HY1, 0.0, PCEIL, basalt)
    gbox("wall_r_back", HX1 + 0.04, HX1 + 0.2, HY0, HY1, 0.0, PCEIL, "shadowgap")
    y = HY0 + 0.06
    k = 0
    while y < HY1 - 0.03:
        gbox("slat_r%d" % k, HX1 - 0.005, HX1 + 0.04, y - 0.026, y + 0.026, 0.0, PCEIL, "oak_slat")
        y += 0.11
        k += 1
    gbox("wall_f", HX0, HX1, HY1, HY1 + 0.2, 0.0, PCEIL, basalt_x)
    gbox("onyx_panel", -6.0, 6.0, HY1 - 0.03, HY1, 0.45, 4.35, "onyx")
    gbox("onyx_frame_b", -6.05, 6.05, HY1 - 0.06, HY1, 0.40, 0.45, "bronze")
    gbox("onyx_frame_t", -6.05, 6.05, HY1 - 0.06, HY1, 4.35, 4.40, "bronze")
    for x in (-6.05, 6.0):
        gbox("onyx_frame_s", x, x + 0.05, HY1 - 0.06, HY1, 0.40, 4.40, "bronze")
    # the back wall: oak slats, the entrance's glass door in a bronze frame, the towel cabinet
    DX0, DX1 = 4.35, 5.65
    gbox("wall_b_back", HX0, HX1, HY0 - 0.2, HY0 - 0.04, 0.0, PCEIL, "shadowgap")
    x = HX0 + 0.06
    while x < HX1 - 0.03:
        z_from = 2.62 if DX0 - 0.1 < x < DX1 + 0.1 else 0.0          # over the door the slats start at its head
        gbox("slat_b", x - 0.026, x + 0.026, HY0 - 0.04, HY0 + 0.005, z_from, PCEIL, "oak_slat")
        x += 0.11
    glass_clear("door_glass")
    obj("pool_door_glass", [(DX0 + 0.05, HY0 - 0.02, 0.02), (DX1 - 0.05, HY0 - 0.02, 0.02), (DX1 - 0.05, HY0 - 0.02, 2.5),
                            (DX0 + 0.05, HY0 - 0.02, 2.5)], [(0, 1, 2, 3)], "door_glass")
    gbox("pool_door_frame_l", DX0, DX0 + 0.05, HY0 - 0.05, HY0 + 0.01, 0.0, 2.55, "bronze")
    gbox("pool_door_frame_r", DX1 - 0.05, DX1, HY0 - 0.05, HY0 + 0.01, 0.0, 2.55, "bronze")
    gbox("pool_door_frame_t", DX0, DX1, HY0 - 0.05, HY0 + 0.01, 2.5, 2.62, "bronze")
    rod("pool_door_pull", (DX0 + 0.2, HY0 + 0.07, 0.8), (DX0 + 0.2, HY0 + 0.07, 1.9), 0.015, "bronze", 12)
    gbox("pool_corridor", DX0 - 0.4, DX1 + 0.4, HY0 - 2.5, HY0 - 0.2, 0.0, 0.01, deck)
    # the towel cabinet: oak, an open niche of rolled towels lit from above
    gbox("towel_cab_low", -6.6, -3.8, HY0, HY0 + 0.55, 0.0, 1.0, "oak", bev=0.004)
    gbox("towel_cab_top", -6.6, -3.8, HY0, HY0 + 0.55, 1.8, 2.2, "oak", bev=0.004)
    for xx in (-6.6, -3.95):
        gbox("towel_cab_side", xx, xx + 0.15, HY0, HY0 + 0.55, 1.0, 1.8, "oak", bev=0.003)
    gbox("towel_cab_back", -6.45, -3.95, HY0, HY0 + 0.04, 1.0, 1.8, "walnut")
    for k in range(5):
        for r_ in range(2):
            rod("towel_roll", (-6.2 + k * 0.48, HY0 + 0.06, 1.095 + r_ * 0.18), (-6.2 + k * 0.48, HY0 + 0.50, 1.095 + r_ * 0.18), 0.088,
                "towel" if (k + r_) % 2 else "towel_grey", 20)
    gbox("towel_niche_led", -6.45, -3.95, HY0 + 0.44, HY0 + 0.48, 1.795, 1.8, "strip_led")
    light("towel_niche_l", "AREA", (-5.2, HY0 + 0.42, 1.78), 12.0, (1.0, 0.84, 0.66), 2.4, 0.04, aim=(0, 0, -1), spread=140)
    # the ceiling: plaster, a raised coffer over the pool with a hidden cove, linear lights over the decks
    CC = PCEIL + 0.5
    for nm, a in (("l", (HX0, gx0, HY0, HY1)), ("r", (gx1, HX1, HY0, HY1)), ("n", (gx0, gx1, HY0, gy0)), ("f", (gx0, gx1, gy1, HY1))):
        gbox("ceil_" + nm, a[0], a[1], a[2], a[3], PCEIL, PCEIL + 0.05, "pool_ceiling")
    gbox("ceil_coffer", gx0, gx1, gy0, gy1, CC, CC + 0.05, "pool_ceiling")
    for nm, a in (("l", (gx0 - 0.03, gx0, gy0, gy1)), ("r", (gx1, gx1 + 0.03, gy0, gy1)), ("n", (gx0, gx1, gy0 - 0.03, gy0)),
                  ("f", (gx0, gx1, gy1, gy1 + 0.03))):
        gbox("coffer_side_" + nm, a[0], a[1], a[2], a[3], PCEIL, CC, "pool_ceiling")
    for nm, a in (("l", (gx0, gx0 + 0.25, gy0, gy1)), ("r", (gx1 - 0.25, gx1, gy0, gy1)), ("n", (gx0, gx1, gy0, gy0 + 0.25)),
                  ("f", (gx0, gx1, gy1 - 0.25, gy1))):
        gbox("coffer_ledge_" + nm, a[0], a[1], a[2], a[3], PCEIL + 0.10, PCEIL + 0.13, "pool_ceiling")
    for nm, a in (("l", (gx0 + 0.10, gx0 + 0.13, gy0 + 0.1, gy1 - 0.1)), ("r", (gx1 - 0.13, gx1 - 0.10, gy0 + 0.1, gy1 - 0.1)),
                  ("n", (gx0 + 0.1, gx1 - 0.1, gy0 + 0.10, gy0 + 0.13)), ("f", (gx0 + 0.1, gx1 - 0.1, gy1 - 0.13, gy1 - 0.10))):
        gbox("coffer_led_" + nm, a[0], a[1], a[2], a[3], PCEIL + 0.13, PCEIL + 0.132, "cove_led")
    for k, (x, y, w, h) in enumerate(((gx0 + 0.12, (gy0 + gy1) / 2, 0.06, gy1 - gy0 - 0.4), (gx1 - 0.12, (gy0 + gy1) / 2, 0.06, gy1 - gy0 - 0.4),
                                      (0.0, gy0 + 0.12, gx1 - gx0 - 0.4, 0.06), (0.0, gy1 - 0.12, gx1 - gx0 - 0.4, 0.06))):
        light("coffer_cove%d" % k, "AREA", (x, y, PCEIL + 0.15), 240.0 if h > w else 90.0, (1.0, 0.82, 0.62), w, h, aim=(0, 0, 1), spread=150)
    for s in (-1, 1):
        xl = s * 5.8
        gbox("line_slot%d" % s, xl - 0.05, xl + 0.05, HY0 + 1.2, HY1 - 1.2, PCEIL - 0.004, PCEIL, "shadowgap")
        gbox("line_led%d" % s, xl - 0.03, xl + 0.03, HY0 + 1.25, HY1 - 1.25, PCEIL - 0.006, PCEIL - 0.004, "strip_led")
        light("line%d" % s, "AREA", (xl, (HY0 + HY1) / 2, PCEIL - 0.02), 420.0, (1.0, 0.84, 0.66), 0.08, HY1 - HY0 - 2.6, aim=(0, 0, -1), spread=120)
    # grazing light down the basalt wall, and the bench's LED slot
    for k in range(8):
        y = HY0 + 2.5 + k * 3.2
        light("graze%d" % k, "SPOT", (HX0 + 0.35, y, PCEIL - 0.08), 110.0, (1.0, 0.82, 0.62), 0.02, aim=(-0.38, 0, -1), spot=36.0, blend=0.4)
        cyl("graze_dl%d" % k, HX0 + 0.35, y, PCEIL - 0.006, PCEIL - 0.001, 0.05, "downlight_rim", 20)
        cyl("graze_em%d" % k, HX0 + 0.35, y, PCEIL - 0.007, PCEIL - 0.006, 0.035, "downlight_emit", 16)
    gbox("bench", HX0, HX0 + 0.6, 14.4, 27.6, 0.08, 0.46, "bench_stone", bev=0.008)
    gbox("bench_recess", HX0, HX0 + 0.5, 14.45, 27.55, 0.0, 0.08, "shadowgap")
    gbox("bench_led", HX0 + 0.47, HX0 + 0.5, 14.5, 27.5, 0.074, 0.078, "strip_led")
    light("bench_glow", "AREA", (HX0 + 0.48, 21.0, 0.075), 45.0, (1.0, 0.82, 0.62), 0.03, 13.0, aim=(0, 0, -1), spread=150)
    olive_tree("olive_bl", -6.3, 12.6, 2.5, seed=23, pot_r=0.48, pot_h=0.66, leaves=8000)
    olive_tree("olive_bf", -6.3, 29.4, 2.4, seed=31, pot_r=0.48, pot_h=0.66, leaves=8000)
    for k, y in enumerate((16.0, 16.65, 22.0, 25.8, 26.4)):
        rod("bench_towel%d" % k, (HX0 + 0.12, y, 0.55), (HX0 + 0.48, y, 0.55), 0.085, "towel" if k % 2 == 0 else "towel_grey", 20)
    # the loungers on the right deck: teak, white cushions, feet to the pool
    for k, y in enumerate((13.6, 16.4, 19.2, 22.0, 24.8, 27.6)):
        lounger("lounger%d" % k, 5.9, y)
        if k % 2 == 0:
            cyl("lside%d" % k, 6.55, y + 1.4, 0.0, 0.42, 0.21, "teak", 36, bev=0.008)
            if k == 2:
                cyl("lcarafe", 6.5, y + 1.4, 0.42, 0.64, 0.05, "door_glass", 24)
            rod("ltowel%d" % k, (6.2, y - 0.05, 0.52), (6.85, y - 0.05, 0.52), 0.08, "towel", 20)
    # olive trees flanking the onyx, a third by the door
    olive_tree("olive_l", -5.6, HY1 - 1.6, 2.7, seed=3, pot_r=0.5, pot_h=0.7, leaves=9000)
    olive_tree("olive_r", 5.6, HY1 - 1.6, 2.6, seed=7, pot_r=0.5, pot_h=0.7, leaves=9000)
    olive_tree("olive_d", 6.4, 8.0, 2.3, seed=17, pot_r=0.42, pot_h=0.6, leaves=7000)
    # downlights at the far deck and by the door
    for k, (x, y) in enumerate(((-2.4, 34.0), (2.4, 34.0), (0.0, 7.8), (-3.0, 7.8), (3.0, 7.8))):
        downlight("pdl%d" % k, x, y, PCEIL, 32.0, 55.0)
    camera(0.0, 9.6, 1.6)
    marks = [("the onyx wall (its middle)", (0.0, HY1, 2.4)), ("the pool's far end", (0.0, PY1, 0.0)),
             ("the loungers (the middle pair)", (5.9, 20.6, 0.4)), ("the stone bench", (HX0 + 0.3, 21.0, 0.46))]
    doors = [("pool_entrance", ((DX0 + DX1) / 2, HY0, 1.3))]
    report("pool: the residents' pool on a basement level (the builder: 'on one of the basement levels'), level -1 and "
           "its place an illustration; pool %.1f x %.1f m, %.1f m deep; hall %.0f x %.0f m, %.1f m clear; no window"
           % (2 * PX, PY1 - PY0, -FLZ, HX1 - HX0, HY1 - HY0, PCEIL), marks, doors)


def lounger(name, cx, cy):
    """a teak sun lounger, its back raised, its feet toward the pool (-X)"""
    L, Wd = 1.98, 0.72
    x0 = cx - L / 2
    gbox(name + "_rail_a", x0, x0 + L, cy - Wd / 2, cy - Wd / 2 + 0.05, 0.26, 0.32, "teak", bev=0.008)
    gbox(name + "_rail_b", x0, x0 + L, cy + Wd / 2 - 0.05, cy + Wd / 2, 0.26, 0.32, "teak", bev=0.008)
    for xx in (x0 + 0.08, x0 + L - 0.1):
        for yy in (cy - Wd / 2 + 0.025, cy + Wd / 2 - 0.025):
            gbox(name + "_leg", xx - 0.03, xx + 0.03, yy - 0.025, yy + 0.025, 0.0, 0.29, "teak", bev=0.006)
    x = x0 + 0.06
    while x < x0 + 1.25:
        gbox(name + "_slat", x - 0.03, x + 0.03, cy - Wd / 2 + 0.05, cy + Wd / 2 - 0.05, 0.28, 0.31, "teak", bev=0.004)
        x += 0.09
    cushion(name + "_seat", x0 + 0.66, cy, 0.31, 1.26, Wd - 0.06, 0.08, "cushion_white", 0, 0.004, 0.03)
    # the raised back: a tilted board and its cushion
    ang = 38.0
    pivot = Vector((x0 + 1.30, cy, 0.33))
    dirv = Vector((math.cos(ang * DEG), 0, math.sin(ang * DEG)))
    up = Vector((-math.sin(ang * DEG), 0, math.cos(ang * DEG)))
    for nm, (off, th, mt, w) in (("board", (0.0, 0.03, "teak", Wd - 0.02)), ("bcush", (0.05, 0.07, "cushion_white", Wd - 0.06))):
        c = pivot + dirv * 0.34 + up * (off + th / 2)
        ob = box(name + "_" + nm, 0, 0, -th / 2, 0.68, w, th, mt, 0.0)
        ob.location = c
        ob.rotation_euler = (0, -ang * DEG, 0)
        if mt != "teak":
            bv = ob.modifiers.new("bevel", "BEVEL")
            bv.width = 0.03
            bv.segments = 4
            subsurf(ob, 2)
        else:
            bevel(ob, 0.006, 2)
    gbox(name + "_strut", x0 + 1.55, x0 + 1.6, cy - 0.25, cy + 0.25, 0.30, 0.62, "teak", bev=0.004)


def _black_world():
    w = bpy.data.worlds.new("basement")
    w.use_nodes = True
    nt = w.node_tree
    for n in list(nt.nodes):
        if n.type == "BACKGROUND":
            n.inputs["Strength"].default_value = 0.0
            n.inputs["Color"].default_value = (0, 0, 0, 1)
    return w


# ============================================================================================ 3. the gym (basement)
GCEIL = 3.6
GX = 15.0                                        # the gym's middle (X), beside the pool hall
GX0, GX1, GY0, GY1 = GX - 5.5, GX + 5.5, 6.5, 24.5


def treadmill(name, cx, cy):
    """a treadmill facing -X (the moss wall): a deck and belt, a motor hood, two uprights, handrails, a console"""
    L, Wd = 2.0, 0.86
    xf, xb = cx - L / 2, cx + L / 2
    gbox(name + "_deck", xf + 0.25, xb, cy - Wd / 2, cy + Wd / 2, 0.04, 0.20, "black_coat", bev=0.02)
    gbox(name + "_belt", xf + 0.3, xb - 0.06, cy - 0.27, cy + 0.27, 0.20, 0.215, "rubber_black")
    for s in (-1, 1):
        gbox(name + "_rail%d" % s, xf + 0.3, xb - 0.04, cy + s * 0.34 - 0.07, cy + s * 0.34 + 0.07, 0.20, 0.225, "deck_grey", bev=0.004)
        gbox(name + "_foot%d" % s, xf + 0.05, xb, cy + s * 0.40 - 0.03, cy + s * 0.40 + 0.03, 0.0, 0.05, "black_coat", bev=0.01)
    box(name + "_hood", xf + 0.25, cy, 0.04, 0.42, Wd, 0.30, "black_coat", bev=0.04)
    for s in (-1, 1):
        rod(name + "_upright%d" % s, (xf + 0.18, cy + s * 0.38, 0.30), (xf + 0.02, cy + s * 0.38, 1.28), 0.032, "black_coat", 16)
        tube(name + "_hand%d" % s, [(xf + 0.06, cy + s * 0.38, 1.05), (xf + 0.38, cy + s * 0.40, 1.05), (xf + 0.62, cy + s * 0.40, 1.02)], 0.016, "steel", 10)
    ob = box(name + "_console", 0, 0, -0.03, 0.30, Wd - 0.04, 0.06, "black_coat", 0.0, bev=0.012)
    ob.location = (xf + 0.04, cy, 1.36)
    ob.rotation_euler = (0, 35 * DEG, 0)                 # the display tilted up toward the runner (+X)
    ob = box(name + "_screen", 0, 0, -0.002, 0.20, 0.42, 0.004, "screen_on", 0.0)
    ob.location = (xf + 0.04 + 0.032 * math.sin(35 * DEG), cy, 1.36 + 0.032 * math.cos(35 * DEG))
    ob.rotation_euler = (0, 35 * DEG, 0)


def bike(name, cx, cy):
    """an upright bike facing -X: a flywheel shroud, a frame, a saddle, handlebars, a console"""
    xf = cx - 0.5
    cyl(name + "_base", cx, cy, 0.0, 0.05, 0.05, "black_coat", 8)
    gbox(name + "_rail", xf - 0.05, cx + 0.55, cy - 0.06, cy + 0.06, 0.0, 0.06, "black_coat", bev=0.01)
    for xx in (xf, cx + 0.5):
        gbox(name + "_stab", xx - 0.05, xx + 0.05, cy - 0.28, cy + 0.28, 0.0, 0.06, "black_coat", bev=0.012)
    rod(name + "_fly", (xf + 0.12, cy - 0.07, 0.40), (xf + 0.12, cy + 0.07, 0.40), 0.30, "black_coat", 40, bev=0.02)
    rod(name + "_flyhub", (xf + 0.12, cy - 0.075, 0.40), (xf + 0.12, cy + 0.075, 0.40), 0.10, "steel", 24)
    rod(name + "_down", (xf + 0.12, cy, 0.42), (cx + 0.2, cy, 0.06), 0.035, "black_coat", 12)
    rod(name + "_seatpost", (cx + 0.15, cy, 0.30), (cx + 0.25, cy, 0.98), 0.03, "steel", 12)
    rod(name + "_seatlink", (cx + 0.15, cy, 0.30), (xf + 0.12, cy, 0.42), 0.035, "black_coat", 12)
    cushion(name + "_saddle", cx + 0.27, cy, 0.98, 0.26, 0.17, 0.06, "leather_black", 0, 0.003, 0.025)
    rod(name + "_stem", (xf + 0.05, cy, 0.6), (xf - 0.02, cy, 1.18), 0.03, "black_coat", 12)
    tube(name + "_bars", [(xf - 0.02, cy - 0.24, 1.18), (xf + 0.02, cy - 0.20, 1.22), (xf + 0.02, cy + 0.20, 1.22), (xf - 0.02, cy + 0.24, 1.18)], 0.016, "rubber_black", 10)
    ob = box(name + "_console", 0, 0, -0.02, 0.16, 0.26, 0.04, "black_coat", 0.0, bev=0.008)
    ob.location = (xf - 0.06, cy, 1.30)
    ob.rotation_euler = (0, 40 * DEG, 0)


def rower(name, cx, cy):
    """a rowing machine along X: the flywheel housing toward the wall (-X), a long rail, a seat, footrests"""
    xf, xb = cx - 1.2, cx + 1.2
    rod(name + "_fly", (xf + 0.25, cy - 0.12, 0.38), (xf + 0.25, cy + 0.12, 0.38), 0.30, "black_coat", 40, bev=0.02)
    gbox(name + "_rail", xf + 0.25, xb, cy - 0.05, cy + 0.05, 0.30, 0.36, "steel", bev=0.006)
    gbox(name + "_back_leg", xb - 0.1, xb, cy - 0.25, cy + 0.25, 0.0, 0.30, "black_coat", bev=0.01)
    gbox(name + "_front_leg", xf + 0.1, xf + 0.4, cy - 0.28, cy + 0.28, 0.0, 0.08, "black_coat", bev=0.01)
    cushion(name + "_seat", cx + 0.35, cy, 0.36, 0.30, 0.26, 0.07, "leather_black", 0, 0.003, 0.025)
    for s in (-1, 1):
        ob = box(name + "_foot%d" % s, 0, 0, -0.01, 0.30, 0.13, 0.02, "black_coat", 0.0, bev=0.005)
        ob.location = (xf + 0.62, cy + s * 0.1, 0.45)
        ob.rotation_euler = (0, 50 * DEG, 0)
    rod(name + "_handle", (xf + 0.6, cy - 0.25, 0.62), (xf + 0.6, cy + 0.25, 0.62), 0.016, "rubber_black", 10)


def dumbbell(name, x, y, z, r, half_len=0.17, axis="X"):
    hl = half_len
    d = Vector((1, 0, 0)) if axis == "X" else Vector((0, 1, 0))
    c = Vector((x, y, z))
    for s in (-1, 1):
        rod(name + "_head%d" % s, tuple(c + d * s * (hl - 0.07)), tuple(c + d * s * (hl + 0.0)), r, "rubber_black", 20)
    rod(name + "_bar", tuple(c - d * (hl - 0.06)), tuple(c + d * (hl - 0.06)), 0.016, "chrome", 12)


def plate(name, c, axis, r, th, mat="rubber_black"):
    c = Vector(c)
    d = Vector(axis).normalized()
    rod(name, tuple(c - d * th / 2), tuple(c + d * th / 2), r, mat, 40, bev=0.006)
    rod(name + "_hub", tuple(c - d * (th / 2 + 0.003)), tuple(c + d * (th / 2 + 0.003)), 0.05, "steel", 20)


def build_gym():
    bpy.context.scene.world = _black_world()
    rubber_floor()
    moss_mat()
    plaster("gym_ceiling", (0.52, 0.505, 0.48), 0.9)
    pmat("deck_grey", (0.085, 0.085, 0.09), 0.75, spec=0.3)
    turf_mat()
    plaster("gym_wall", (0.64, 0.62, 0.58))
    screen_mat("screen_on")
    emit("strip_led", (1.0, 0.86, 0.70), 24.0)
    emit("line_led", (1.0, 0.92, 0.82), 15.0)
    wood("platform_oak", (0.45, 0.32, 0.19), (0.58, 0.43, 0.28), 24.0, 0.40, along="X")
    leather("pad_black", (0.03, 0.03, 0.032), 0.4)
    wood("ply", (0.62, 0.48, 0.32), (0.70, 0.56, 0.38), 30.0, 0.5)
    pmat("ball_grey", (0.10, 0.10, 0.11), 0.7, bump=0.3, bump_scale=200.0)
    pmat("mat_green", (0.20, 0.26, 0.22), 0.85)
    pmat("mat_sand", (0.55, 0.48, 0.38), 0.85)
    # the room: the floor, the walls, the ceiling
    gbox("gym_floor", GX0, GX1, GY0, GY1, -0.05, 0.0, "rubber")
    gbox("gym_wall_l", GX0 - 0.2, GX0, GY0, GY1, 0.0, GCEIL, "gym_wall")
    gbox("gym_wall_r", GX1, GX1 + 0.2, GY0, GY1, 0.0, GCEIL, "gym_wall")
    gbox("gym_wall_f_back", GX0, GX1, GY1 + 0.04, GY1 + 0.2, 0.0, GCEIL, "shadowgap")
    gbox("gym_wall_b", GX0, GX1, GY0 - 0.2, GY0 - 0.004, 0.0, GCEIL, "shadowgap")
    gbox("gym_ceiling", GX0, GX1, GY0, GY1, GCEIL, GCEIL + 0.05, "gym_ceiling")
    # the far wall: oak slats with three vertical light lines
    x = GX0 + 0.06
    while x < GX1 - 0.03:
        gbox("gslat", x - 0.026, x + 0.026, GY1 - 0.005, GY1 + 0.04, 0.0, GCEIL, "oak_slat")
        x += 0.11
    for k, xl in enumerate((GX - 3.3, GX + 3.3)):
        gbox("gslat_led%d" % k, xl - 0.015, xl + 0.015, GY1 - 0.01, GY1 - 0.005, 0.15, GCEIL - 0.15, "strip_led")
        light("gslat_glow%d" % k, "AREA", (xl, GY1 - 0.05, GCEIL / 2), 70.0, (1.0, 0.86, 0.70), 0.04, GCEIL - 0.3, aim=(0, -1, 0), spread=160)
    # the left wall: the preserved-moss panel in an oak frame
    MY0, MY1 = 10.6, 21.6
    gbox("moss_panel", GX0, GX0 + 0.06, MY0, MY1, 0.35, 3.15, "moss")
    displace(grid_wall_x("moss_relief", GX0 + 0.075, MY0 + 0.02, MY1 - 0.02, 0.37, 3.13, 220, 56, "moss"), 0.05, 0.05)
    for (a, b_, c_, d_) in ((MY0 - 0.08, MY0, 0.27, 3.23), (MY1, MY1 + 0.08, 0.27, 3.23)):
        gbox("moss_frame", GX0, GX0 + 0.14, a, b_, c_, d_, "oak")
    for (zz0, zz1) in ((0.27, 0.35), (3.15, 3.23)):
        gbox("moss_frame", GX0, GX0 + 0.14, MY0 - 0.08, MY1 + 0.08, zz0, zz1, "oak")
    for k in range(6):
        y = MY0 + 0.9 + k * 1.85
        light("moss_graze%d" % k, "SPOT", (GX0 + 0.45, y, GCEIL - 0.06), 40.0, (1.0, 0.86, 0.68), 0.02, aim=(-0.22, 0, -1), spot=45.0, blend=0.5)
        cyl("mg_rim%d" % k, GX0 + 0.45, y, GCEIL - 0.004, GCEIL - 0.001, 0.05, "downlight_rim", 20)
        cyl("mg_em%d" % k, GX0 + 0.45, y, GCEIL - 0.005, GCEIL - 0.004, 0.035, "downlight_emit", 16)
    # the right wall: a mirror in black-framed panels, a light washing down from a slot above it
    gbox("mirror", GX1 - 0.012, GX1, 8.6, 23.4, 0.25, 2.65, "mirror")
    for y in [8.6 + 1.85 * k for k in range(9)]:
        gbox("mirror_joint", GX1 - 0.015, GX1, y - 0.008, y + 0.008, 0.25, 2.65, "black_coat")
    gbox("mirror_frame_b", GX1 - 0.02, GX1, 8.6, 23.4, 0.22, 0.26, "black_coat")
    gbox("mirror_frame_t", GX1 - 0.02, GX1, 8.6, 23.4, 2.64, 2.68, "black_coat")
    gbox("wash_slot", GX1 - 0.25, GX1, 8.0, 24.0, GCEIL - 0.004, GCEIL, "shadowgap")
    gbox("wash_led", GX1 - 0.16, GX1 - 0.13, 8.1, 23.9, GCEIL - 0.006, GCEIL - 0.004, "strip_led")
    light("wash", "AREA", (GX1 - 0.15, 16.0, GCEIL - 0.03), 260.0, (1.0, 0.86, 0.70), 0.06, 15.8, aim=(0, 0, -1), spread=110)
    # the ceiling's linear lights
    for k, xo in enumerate((-3.0, -1.0, 1.0, 3.0)):
        xl = GX + xo
        gbox("gline_slot%d" % k, xl - 0.04, xl + 0.04, 7.8, 23.2, GCEIL - 0.004, GCEIL, "shadowgap")
        gbox("gline_led%d" % k, xl - 0.025, xl + 0.025, 7.85, 23.15, GCEIL - 0.006, GCEIL - 0.004, "line_led")
        light("gline%d" % k, "AREA", (xl, 15.5, GCEIL - 0.02), 340.0, (1.0, 0.92, 0.82), 0.06, 15.3, aim=(0, 0, -1), spread=130)
    # the treadmills facing the moss wall, two bikes and a rower beyond them
    for k, y in enumerate((11.7, 12.9, 14.1, 15.3)):
        treadmill("tm%d" % k, GX0 + 2.2, y)
    for k, y in enumerate((16.9, 18.0)):
        bike("bike%d" % k, GX0 + 1.6, y)
    rower("rower", GX0 + 2.1, 19.6)
    # the dumbbells before the mirror: a two-tier rack, ten pairs
    RX = GX1 - 0.65
    RY0, RY1 = 11.8, 16.6
    for yy in (RY0, (RY0 + RY1) / 2, RY1):
        gbox("drack_leg", RX - 0.25, RX + 0.25, yy - 0.03, yy + 0.03, 0.0, 0.05, "black_coat", bev=0.008)
        rod("drack_post", (RX - 0.12, yy, 0.05), (RX - 0.12, yy, 0.82), 0.03, "black_coat", 12)
        rod("drack_post2", (RX + 0.12, yy, 0.05), (RX + 0.12, yy, 0.98), 0.03, "black_coat", 12)
    for (xx, zz) in ((RX - 0.14, 0.62), (RX + 0.14, 0.88)):
        gbox("drack_tray", xx - 0.12, xx + 0.12, RY0 - 0.05, RY1 + 0.05, zz - 0.04, zz, "black_coat", bev=0.006)
    for k in range(10):
        y = RY0 + 0.25 + k * 0.46
        r = 0.050 + 0.0042 * k
        dumbbell("db_lo%d" % k, RX - 0.14, y, 0.62 + r, r, 0.17 + 0.006 * k, "X")
        dumbbell("db_hi%d" % k, RX + 0.14, y, 0.88 + r * 0.8, r * 0.8, 0.15 + 0.005 * k, "X")
    # two adjustable benches
    for k, y in enumerate((13.0, 15.4)):
        bx = GX + 1.9
        gbox("bench%d_frame" % k, bx - 0.6, bx + 0.6, y - 0.04, y + 0.04, 0.06, 0.36, "black_coat", bev=0.008)
        for xx in (bx - 0.6, bx + 0.55):
            gbox("bench%d_foot" % k, xx - 0.04, xx + 0.04, y - 0.25, y + 0.25, 0.0, 0.06, "black_coat", bev=0.01)
        cushion("bench%d_pad" % k, bx - 0.25, y, 0.36, 0.72, 0.28, 0.07, "pad_black", 0, 0.003, 0.03)
        ob = cushion("bench%d_back" % k, 0, 0, -0.035, 0.62, 0.28, 0.07, "pad_black", 0, 0.003, 0.03)
        ob.location = (bx + 0.36, y, 0.52)
        ob.rotation_euler = (0, -25 * DEG, 0)
    # the lifting platform and the power rack at the far end, a barbell racked, plates on the horns
    gbox("platform", GX - 1.5, GX + 1.5, 20.6, 23.6, 0.0, 0.035, "platform_oak", bev=0.004)
    for x in (GX - 1.5, GX + 1.0):
        gbox("platform_rubber", x, x + 0.5, 20.6, 23.6, 0.0, 0.036, "rubber")
    for xx in (GX - 0.62, GX + 0.62):
        for yy in (21.9, 23.1):
            gbox("rack_up", xx - 0.04, xx + 0.04, yy - 0.04, yy + 0.04, 0.035, 2.3, "black_coat", bev=0.004)
        gbox("rack_side_t", xx - 0.04, xx + 0.04, 21.86, 23.14, 2.22, 2.3, "black_coat", bev=0.004)
        gbox("rack_side_b", xx - 0.04, xx + 0.04, 21.86, 23.14, 0.035, 0.11, "black_coat", bev=0.004)
        gbox("rack_jhook", xx - 0.05, xx + 0.05, 21.82, 21.98, 1.38, 1.44, "steel", bev=0.004)
        rod("rack_horn", (xx, 23.1, 0.55), (xx + (0.3 if xx > GX else -0.3), 23.1, 0.55), 0.025, "steel", 12)
    for yy in (21.9, 23.1):
        gbox("rack_cross", GX - 0.66, GX + 0.66, yy - 0.04, yy + 0.04, 2.22, 2.3, "black_coat", bev=0.004)
    rod("barbell", (GX - 1.1, 21.9, 1.47), (GX + 1.1, 21.9, 1.47), 0.014, "chrome", 12)
    for s in (-1, 1):
        rod("barbell_sleeve%d" % s, (GX + s * 0.78, 21.9, 1.47), (GX + s * 1.1, 21.9, 1.47), 0.025, "chrome", 16)
        plate("bb_plate%d" % s, (GX + s * 0.82, 21.9, 1.47), (1, 0, 0), 0.225, 0.065)
        plate("bb_plate2%d" % s, (GX + s * 0.885, 21.9, 1.47), (1, 0, 0), 0.225, 0.05)
        for k in range(3):
            plate("horn_plate%d%d" % (s, k), (GX + s * (0.68 + 0.05 * k), 23.1, 0.55), (1, 0, 0), 0.225, 0.045)
    # the cable crossover at the far right
    for xx in (GX + 2.7, GX + 4.9):
        gbox("cable_tower", xx - 0.18, xx + 0.18, 23.4, 23.9, 0.0, 2.35, "black_coat", bev=0.01)
        gbox("cable_stack", xx - 0.12, xx + 0.12, 23.36, 23.42, 0.15, 1.05, "steel")
        for k in range(14):
            gbox("cable_plate", xx - 0.11, xx + 0.11, 23.30, 23.40, 0.15 + k * 0.06, 0.20 + k * 0.06, "black_coat", bev=0.003)
        rod("cable_pulley", (xx, 23.3, 2.2), (xx, 23.22, 2.2), 0.06, "steel", 20)
    gbox("cable_top", GX + 2.5, GX + 5.1, 23.5, 23.8, 2.3, 2.42, "black_coat", bev=0.008)
    # kettlebells on a low shelf at the far left, medicine balls, plyo boxes, mats
    gbox("kb_shelf", GX - 5.3, GX - 3.1, 23.6, 24.3, 0.0, 0.05, "black_coat", bev=0.006)
    gbox("kb_shelf2", GX - 5.3, GX - 3.1, 23.6, 24.3, 0.42, 0.46, "black_coat", bev=0.006)
    for xx in (GX - 5.25, GX - 3.15):
        gbox("kb_post", xx - 0.03, xx + 0.03, 23.6, 24.3, 0.0, 0.46, "black_coat")
    for k in range(5):
        for t in range(2):
            x = GX - 5.05 + k * 0.42
            zb = 0.05 if t == 0 else 0.46
            r = 0.085 + 0.012 * k
            sphere("kb%d%d" % (k, t), x, 23.95, zb + r * 0.95, r, "black_coat", 1.0, 1.0, 0.95)
            tube("kb_handle%d%d" % (k, t), [(x - r * 0.6, 23.95, zb + r * 1.6), (x - r * 0.5, 23.95, zb + r * 2.25), (x + r * 0.5, 23.95, zb + r * 2.25),
                                            (x + r * 0.6, 23.95, zb + r * 1.6)], 0.012, "black_coat", 8)
    for k, (x, y) in enumerate(((GX + 3.55, 18.3), (GX + 3.9, 18.45), (GX + 3.65, 18.75))):
        sphere("medball%d" % k, x, y, 0.15, 0.15, "ball_grey")
    for k, (x, y, h) in enumerate(((GX + 1.65, 20.15, 0.6), (GX + 2.3, 20.2, 0.5), (GX + 1.7, 20.15, 0.6))):
        if k == 2:
            box("plyo%d" % k, x, y, 0.6, 0.6, 0.6, 0.45, "ply", 12.0, bev=0.012)
        else:
            box("plyo%d" % k, x, y, 0.0, 0.6, 0.6, h, "ply", 4.0 * k, bev=0.012)
    for k, (x, mt) in enumerate(((GX + 1.45, "mat_green"), (GX + 2.2, "mat_sand"), (GX + 2.95, "mat_green"))):
        gbox("yoga%d" % k, x - 0.31, x + 0.31, 16.9, 18.7, 0.0, 0.008, mt, bev=0.002)
    # a turf lane down the middle, from the door wall to the lifting platform (sled and carry work)
    gbox("turf", GX - 0.95, GX + 0.95, 12.4, 20.4, 0.0, 0.014, "turf")
    for k in range(3):
        rod("roller%d" % k, (GX - 4.95 + k * 0.0, 22.2 + k * 0.17, 0.075), (GX - 4.35, 22.2 + k * 0.17, 0.075), 0.075, "mat_green" if k % 2 else "black_coat", 20)
    # the door wall: the entrance's glass door, a water station, a towel shelf
    DX0, DX1 = GX - 4.65, GX - 3.35
    x = GX0 + 0.06
    while x < GX1 - 0.03:
        z_from = 2.62 if DX0 - 0.1 < x < DX1 + 0.1 else 0.0          # over the door the slats start at its head
        gbox("bslat", x - 0.026, x + 0.026, GY0 - 0.005, GY0 + 0.035, z_from, GCEIL, "oak_slat")
        x += 0.11
    gbox("ballrack_back", GX1 - 0.06, GX1 - 0.02, 6.8, 8.6, 0.0, 1.75, "black_coat", bev=0.005)
    for zz in (0.25, 0.85, 1.45):
        gbox("ballrack_shelf", GX1 - 0.42, GX1, 6.8, 8.6, zz - 0.03, zz, "black_coat", bev=0.004)
        for k in range(3):
            sphere("rball", GX1 - 0.2, 7.1 + k * 0.6, zz + 0.15 + 0.01 * k, 0.15 - 0.012 * k, "ball_grey" if (k + int(zz * 10)) % 2 else "rubber_black")
    for yy in (6.85, 8.55):
        for xx in (GX1 - 0.40, GX1 - 0.06):
            gbox("ballrack_post", xx - 0.02, xx + 0.02, yy - 0.02, yy + 0.02, 0.0, 1.75, "black_coat")
    glass_clear("door_glass")
    obj("gym_door_glass", [(DX0 + 0.05, GY0 + 0.02, 0.02), (DX1 - 0.05, GY0 + 0.02, 0.02), (DX1 - 0.05, GY0 + 0.02, 2.5),
                           (DX0 + 0.05, GY0 + 0.02, 2.5)], [(0, 1, 2, 3)], "door_glass")
    wall_b = bpy.data.objects["gym_wall_b"]
    cutter = gbox("door_cutter", DX0, DX1, GY0 - 0.5, GY0 + 0.5, -0.1, 2.55, "shadowgap")
    md = wall_b.modifiers.new("cut", "BOOLEAN")
    md.operation = "DIFFERENCE"
    md.object = cutter
    md.solver = "EXACT"
    cutter.hide_render = True
    gbox("gym_door_frame_l", DX0, DX0 + 0.05, GY0 - 0.02, GY0 + 0.05, 0.0, 2.55, "black_coat")
    gbox("gym_door_frame_r", DX1 - 0.05, DX1, GY0 - 0.02, GY0 + 0.05, 0.0, 2.55, "black_coat")
    gbox("gym_door_frame_t", DX0, DX1, GY0 - 0.02, GY0 + 0.05, 2.5, 2.6, "black_coat")
    rod("gym_door_pull", (DX1 - 0.2, GY0 + 0.1, 0.8), (DX1 - 0.2, GY0 + 0.1, 1.9), 0.015, "steel", 12)
    gbox("gym_corridor", DX0 - 0.4, DX1 + 0.4, GY0 - 2.5, GY0 - 0.2, 0.0, 0.01, "rubber")
    gbox("towel_shelf", GX + 2.4, GX + 4.6, GY0, GY0 + 0.4, 0.0, 1.0, "oak", bev=0.004)
    for k in range(4):
        for r_ in range(2):
            rod("gtowel", (GX + 2.6 + k * 0.5, GY0 + 0.05, 1.08 + r_ * 0.16), (GX + 2.6 + k * 0.5, GY0 + 0.37, 1.08 + r_ * 0.16), 0.075,
                "towel" if (k + r_) % 2 else "towel_grey", 20)
    gbox("water_station", GX + 0.9, GX + 1.4, GY0, GY0 + 0.35, 0.0, 1.45, "steel", bev=0.01)
    gbox("water_station_top", GX + 0.92, GX + 1.38, GY0 + 0.02, GY0 + 0.36, 1.1, 1.3, "black_coat")
    for k, (x, y) in enumerate(((GX - 2.0, 8.0), (GX + 2.0, 8.0))):
        downlight("gdl%d" % k, x, y, GCEIL, 28.0, 60.0)
    camera(GX, 10.5, 1.6)
    marks = [("the power rack", (GX, 22.5, 1.2)), ("the treadmills (their middle)", (GX0 + 2.2, 13.5, 1.0)),
             ("the dumbbell rack", (RX, 14.2, 0.8)), ("the moss wall (its middle)", (GX0, 16.1, 1.8)),
             ("the mirror wall (its middle)", (GX1, 16.0, 1.5))]
    doors = [("gym_entrance", ((DX0 + DX1) / 2, GY0, 1.3))]
    report("gym: the residents' gym on a basement level (the builder: 'on one of the basement levels'), level -1 and its "
           "place an illustration; room %.0f x %.0f m, %.1f m clear; no window" % (GX1 - GX0, GY1 - GY0, GCEIL), marks, doors)


# ============================================================================================ shared by the spa and the parking
def catmull(pts, k=6):
    """a Catmull-Rom curve through 2D points, k points per span"""
    out = []
    Q = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(Q) - 2):
        p0, p1, p2, p3 = Q[i - 1], Q[i], Q[i + 1], Q[i + 2]
        for s in range(k):
            t = s / k
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[d] + (-p0[d] + p2[d]) * t + (2 * p0[d] - 5 * p1[d] + 4 * p2[d] - p3[d]) * t2
                                    + (-p0[d] + 3 * p1[d] - 3 * p2[d] + p3[d]) * t3) for d in range(2)))
    out.append(tuple(pts[-1]))
    return out


def prof_normal(prof, i):
    """the left normal (up for a profile running +x) of a side profile at point i"""
    (xa, za), (xb, zb) = prof[max(i - 1, 0)], prof[min(i + 1, len(prof) - 1)]
    tl = math.hypot(xb - xa, zb - za) or 1.0
    return -(zb - za) / tl, (xb - xa) / tl


def sweep(name, prof, width, th, mat, cx, cy, rot, soft=0.03):
    """a slab th thick swept along a side profile [(x, z)] (local x along rot, the slab grows along the profile's left
    normal), width across; soft: a bevel and a subdivision for an upholstered or eased edge"""
    P = Pr(cx, cy, rot)
    V, F = [], []
    n = len(prof)
    for i, (x, z) in enumerate(prof):
        nx, nz = prof_normal(prof, i)
        for (dy, dt) in ((-width / 2, 0.0), (width / 2, 0.0), (width / 2, th), (-width / 2, th)):
            wx, wy = P(x + nx * dt, dy)
            V.append((wx, wy, z + nz * dt))
    for i in range(n - 1):
        a, c = 4 * i, 4 * (i + 1)
        for k in range(4):
            F.append((a + k, a + (k + 1) % 4, c + (k + 1) % 4, c + k))
    F.append((0, 3, 2, 1))
    F.append((4 * (n - 1), 4 * (n - 1) + 1, 4 * (n - 1) + 2, 4 * (n - 1) + 3))
    ob = fix_normals(obj(name, V, F, mat))
    if soft:
        bv = ob.modifiers.new("bevel", "BEVEL")
        bv.width = soft
        bv.segments = 4
        bv.limit_method = "ANGLE"
        bv.angle_limit = 50 * DEG
        bv.profile = 0.62
        sb = ob.modifiers.new("sub", "SUBSURF")
        sb.subdivision_type = "SIMPLE"
        sb.levels = sb.render_levels = 2
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def towel_cabinet(nm, x0, x1, yb, face=1):
    """the pool's towel cabinet (oak, an open niche of rolled towels lit from above) against a wall at y = yb, facing +Y
    (face 1) or -Y (face -1)"""
    d = 0.55 * face
    ya, yz = (yb, yb + d) if face > 0 else (yb + d, yb)
    gbox(nm + "_low", x0, x1, ya, yz, 0.0, 1.0, "oak", bev=0.004)
    gbox(nm + "_top", x0, x1, ya, yz, 1.8, 2.2, "oak", bev=0.004)
    for xx in (x0, x1 - 0.15):
        gbox(nm + "_side", xx, xx + 0.15, ya, yz, 1.0, 1.8, "oak", bev=0.003)
    gbox(nm + "_back", x0 + 0.15, x1 - 0.15, yb, yb + 0.04 * face, 1.0, 1.8, "walnut")
    n = int((x1 - x0 - 0.3) / 0.48)
    for k in range(n):
        xc = x0 + 0.15 + (x1 - x0 - 0.3) * (k + 0.5) / n
        for r_ in range(2):
            rod(nm + "_roll", (xc, yb + 0.06 * face, 1.095 + r_ * 0.18), (xc, yb + 0.50 * face, 1.095 + r_ * 0.18), 0.088,
                "towel" if (k + r_) % 2 else "towel_grey", 20)
    gbox(nm + "_led", x0 + 0.15, x1 - 0.15, yb + 0.44 * face, yb + 0.48 * face, 1.795, 1.8, "strip_led")
    light(nm + "_l", "AREA", ((x0 + x1) / 2, yb + 0.42 * face, 1.78), 12.0, (1.0, 0.84, 0.66), x1 - x0 - 0.3, 0.04, aim=(0, 0, -1),
          spread=140)


# ============================================================================================ 4. the spa (basement)
SCEIL = 3.4
SX = -15.0                                       # the spa's middle (X): the pool hall's other side, the gym mirrored
SX0, SX1, SY0, SY1 = SX - 5.5, SX + 5.5, 6.5, 22.5
SAU_X0, SAU_X1, SAU_D, SAU_H = SX - 2.2, SX + 2.2, 2.5, 2.3     # the sauna, behind the far wall's glass
TREAT_Y = (12.2, 15.6, 19.0)                     # the treatment rooms' doors on the left wall


def plank(name, c0, c1, along="X", stack="Z", pitch=0.095, rough=0.55):
    """a sauna's softwood panelling (an illustration): planks along one axis stacked along another, a tone per plank,
    a fine grain, the tongue-and-groove joints"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    x, y, z = b.sep(ob)
    ax = {"X": x, "Y": y, "Z": z}
    row = b.m("FLOOR", b.m("DIVIDE", ax[stack], pitch))
    rw = b.white(b.combine(row, 0.0, 5.0))
    sc = {k: (0.9 if k == along else 30.0) for k in "XYZ"}
    vec = b.combine(b.m("ADD", b.m("MULTIPLY", x, sc["X"]), b.m("MULTIPLY", rw, 17.0)),
                    b.m("ADD", b.m("MULTIPLY", y, sc["Y"]), b.m("MULTIPLY", rw, 11.0)), b.m("MULTIPLY", z, sc["Z"]))
    nz = b.noise(vec, 1.0, 6.0, 0.6)
    col = b.ramp(nz.outputs["Fac"], [(0.3, c0), (0.72, c1)])
    col = b.mix(b.m("MULTIPLY", rw, 0.45), col, tuple(c * 0.84 for c in c0))
    j = b.m("LESS_THAN", b.m("FRACT", b.m("DIVIDE", ax[stack], pitch)), 0.06)
    col = b.mix(j, col, tuple(c * 0.42 for c in c0))
    p = b.principled(Base_Color=col, Roughness=rough)
    b.put(p.inputs["Specular IOR Level"], 0.35)
    b.put(p.inputs["Normal"], b.bump(b.m("ADD", b.m("SUBTRACT", 1.0, j), b.m("MULTIPLY", nz.outputs["Fac"], 0.1)), 0.3, 0.01))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def pebble_bed(name):
    """a bed of pale river pebbles (an illustration): rounded cells in stone tones, dark gaps between them"""
    if name in M:
        return M[name]
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    vo = b.n("ShaderNodeTexVoronoi", feature="F1")
    b.put(vo.inputs["Vector"], ob)
    vo.inputs["Scale"].default_value = 24.0
    rr = b.sep(vo.outputs["Color"])[0]
    col = b.ramp(rr, [(0.0, (0.40, 0.39, 0.37)), (0.45, (0.62, 0.60, 0.56)), (1.0, (0.80, 0.78, 0.74))])
    gap = b.m("GREATER_THAN", vo.outputs["Distance"], 0.52)
    col = b.mix(gap, col, (0.16, 0.15, 0.14))
    p = b.principled(Base_Color=col, Roughness=0.55)
    b.put(p.inputs["Normal"], b.bump(b.m("SUBTRACT", 1.0, vo.outputs["Distance"]), 0.8, 0.02))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def relax_lounger(name, cx, cy, rot, cush="linen_sand", shell="walnut"):
    """a spa relaxation lounger (an illustration): a walnut shell on a recessed plinth, an upholstered mattress along its
    curve, a bolster at the head, a rolled towel at the foot; with rot 0 its head is toward +X"""
    L = 1.95
    base = catmull([(0.00, 0.40), (0.35, 0.37), (0.80, 0.33), (1.08, 0.36), (1.36, 0.51), (1.60, 0.72), (1.80, 0.92),
                    (1.95, 1.03)], 6)
    prof = [(x - L / 2, z) for (x, z) in base]
    TH = 0.11
    sweep(name + "_shell", [(x, z - 0.035) for (x, z) in prof], 0.74, 0.035, shell, cx, cy, rot, soft=0.008)
    sweep(name + "_mat", prof, 0.70, TH, cush, cx, cy, rot, soft=0.04)
    P = Pr(cx, cy, rot)
    x, y = P(-0.17, 0)
    box(name + "_plinth", x, y, 0.0, 0.80, 0.42, 0.30, shell, rot, bev=0.01)
    # the bolster: on the mattress where the back rises
    i = min(range(len(prof)), key=lambda k: abs(prof[k][0] - (L / 2 - 0.24)))
    nx, nz = prof_normal(prof, i)
    rb = 0.075
    bx, bz = prof[i][0] + nx * (TH + rb - 0.01), prof[i][1] + nz * (TH + rb - 0.01)
    p0, p1 = P(bx, -0.30), P(bx, 0.30)
    rod(name + "_bolster", (p0[0], p0[1], bz), (p1[0], p1[1], bz), rb, "linen_cream", 24, bev=0.02)
    # a rolled towel at the foot
    i = min(range(len(prof)), key=lambda k: abs(prof[k][0] - (-L / 2 + 0.30)))
    nx, nz = prof_normal(prof, i)
    tx, tz = prof[i][0] + nx * (TH + 0.06), prof[i][1] + nz * (TH + 0.06)
    p0, p1 = P(tx, -0.24), P(tx, 0.24)
    rod(name + "_towel", (p0[0], p0[1], tz), (p1[0], p1[1], tz), 0.068, "towel", 20)


def build_sauna():
    """the sauna behind the far wall's glass (an illustration): softwood panelling, two tiers of slatted benches lit
    from beneath, a backrest with a light behind it, a stove with its stones behind a slatted guard, a bucket"""
    x0, x1, y0, y1, H = SAU_X0, SAU_X1, SY1, SY1 + SAU_D, SAU_H
    gbox("sauna_floor", x0 - 0.1, x1 + 0.1, y0, y1, -0.05, 0.0, "spa_floor")
    gbox("sauna_back", x0, x1, y1, y1 + 0.1, 0.0, H, "sauna_wall_x")
    gbox("sauna_side_l", x0 - 0.1, x0, y0, y1 + 0.1, 0.0, H, "sauna_wall_y")
    gbox("sauna_side_r", x1, x1 + 0.1, y0, y1 + 0.1, 0.0, H, "sauna_wall_y")
    gbox("sauna_ceil", x0 - 0.1, x1 + 0.1, y0, y1 + 0.1, H, H + 0.08, "sauna_ceil")
    UB0, LB0 = y1 - 0.62, y1 - 1.22

    def slats(nm, ya, yb, z):
        y = ya + 0.04
        while y < yb - 0.02:
            gbox(nm, x0 + 0.01, x1 - 0.01, y - 0.034, y + 0.034, z - 0.03, z, "sauna_bench", bev=0.004)
            y += 0.085

    slats("sauna_ub", UB0, y1, 0.95)
    slats("sauna_lb", LB0, UB0, 0.47)
    gbox("sauna_ub_skirt", x0, x1, UB0 + 0.07, UB0 + 0.10, 0.47, 0.92, "sauna_wall_x")
    gbox("sauna_lb_skirt", x0, x1, LB0 + 0.07, LB0 + 0.10, 0.0, 0.44, "sauna_wall_x")
    for (yy, zz, e) in ((UB0 + 0.05, 0.915, 16.0), (LB0 + 0.05, 0.435, 12.0)):
        gbox("sauna_led", x0 + 0.05, x1 - 0.05, yy - 0.01, yy + 0.01, zz - 0.004, zz, "sauna_led")
        light("sauna_bench_l", "AREA", ((x0 + x1) / 2, yy, zz - 0.01), e, (1.0, 0.62, 0.30), x1 - x0 - 0.2, 0.03, aim=(0, -0.25, -1),
              spread=150)
    for zz in (1.24, 1.42):
        gbox("sauna_backrest", x0 + 0.15, x1 - 0.15, y1 - 0.05, y1, zz - 0.045, zz + 0.045, "sauna_bench", bev=0.006)
    gbox("sauna_back_led", x0 + 0.2, x1 - 0.2, y1 - 0.02, y1 - 0.01, 1.47, 1.474, "sauna_led")
    light("sauna_back_l", "AREA", ((x0 + x1) / 2, y1 - 0.06, 1.48), 9.0, (1.0, 0.62, 0.30), x1 - x0 - 0.4, 0.03, aim=(0, 0.35, 1),
          spread=150)
    # the stove (front left), its stones, a slatted guard
    sx_, sy_ = x0 + 0.42, y0 + 0.55
    box("sauna_stove", sx_, sy_, 0.08, 0.44, 0.40, 0.52, "blacksteel", bev=0.01)
    for (dx, dy) in ((-0.2, -0.18), (0.2, -0.18), (0.2, 0.18), (-0.2, 0.18)):
        box("sauna_stove_foot", sx_ + dx * 0.9, sy_ + dy * 0.9, 0.0, 0.04, 0.04, 0.08, "blacksteel")
    rs = random.Random(5)
    for k in range(46):
        r = rs.uniform(0.035, 0.055)
        sphere("sauna_stone", sx_ + rs.uniform(-0.17, 0.17), sy_ + rs.uniform(-0.15, 0.15), 0.60 + r * 0.7 + rs.uniform(0, 0.08),
               r, "sauna_stone", 1.0, rs.uniform(0.8, 1.1), 0.72, 10)
    for k in range(7):
        xx = sx_ - 0.30 + k * 0.10
        gbox("sauna_guard", xx - 0.025, xx + 0.025, sy_ - 0.32, sy_ - 0.30, 0.10, 0.92, "sauna_bench", bev=0.004)
    for k in range(6):
        yy = sy_ - 0.25 + k * 0.10
        gbox("sauna_guard", sx_ + 0.30, sx_ + 0.32, yy - 0.025, yy + 0.025, 0.10, 0.92, "sauna_bench", bev=0.004)
    # a bucket and a ladle on the lower bench
    bx, by = x1 - 0.65, LB0 + 0.32
    cyl("sauna_bucket", bx, by, 0.47, 0.68, 0.12, "sauna_bench", 32, r_top=0.135)
    for zz in (0.51, 0.64):
        cyl("sauna_bucket_band", bx, by, zz, zz + 0.012, 0.128 + (zz - 0.47) * 0.07, "steel", 32)
    rod("sauna_ladle", (bx, by, 0.55), (bx + 0.18, by + 0.08, 0.92), 0.012, "sauna_bench", 8)
    # the glass front: a fixed pane, a mullion, the door (its wooden handle), a fixed strip; bronze frame around
    DXa, DXb = x1 - 0.95, x1 - 0.12
    obj("spa_sauna_glass", [(x0 + 0.02, y0, 0.02), (DXa - 0.03, y0, 0.02), (DXa - 0.03, y0, H - 0.02), (x0 + 0.02, y0, H - 0.02)],
        [(0, 1, 2, 3)], "sauna_glass")
    obj("spa_sauna_door_glass", [(DXa + 0.01, y0 - 0.012, 0.02), (DXb - 0.01, y0 - 0.012, 0.02), (DXb - 0.01, y0 - 0.012, 2.08),
                                  (DXa + 0.01, y0 - 0.012, 2.08)], [(0, 1, 2, 3)], "sauna_glass")
    obj("spa_sauna_transom", [(DXa - 0.03, y0, 2.12), (x1 - 0.02, y0, 2.12), (x1 - 0.02, y0, H - 0.02), (DXa - 0.03, y0, H - 0.02)],
        [(0, 1, 2, 3)], "sauna_glass")
    obj("spa_sauna_strip", [(DXb + 0.01, y0, 0.02), (x1 - 0.02, y0, 0.02), (x1 - 0.02, y0, 2.08), (DXb + 0.01, y0, 2.08)],
        [(0, 1, 2, 3)], "sauna_glass")
    gbox("sauna_mull", DXa - 0.03, DXa, y0 - 0.02, y0 + 0.02, 0.0, H, "bronze")
    gbox("sauna_mull", DXb, DXb + 0.012, y0 - 0.02, y0 + 0.02, 0.0, 2.10, "bronze")
    gbox("sauna_door_head", DXa, x1, y0 - 0.02, y0 + 0.02, 2.08, 2.12, "bronze")
    for k, (hx, hy) in enumerate(((DXb - 0.06, 0.35), (DXb - 0.06, 1.75))):
        gbox("sauna_hinge", hx - 0.03, hx + 0.03, y0 - 0.03, y0 + 0.006, hy, hy + 0.11, "bronze", bev=0.004)
    hx = DXa + 0.12
    gbox("sauna_handle", hx - 0.02, hx + 0.02, y0 - 0.085, y0 - 0.045, 0.85, 1.55, "sauna_bench", bev=0.008)
    for zz in (0.92, 1.48):
        rod("sauna_handle_post", (hx, y0 - 0.05, zz), (hx, y0 - 0.012, zz), 0.008, "bronze", 8)
    gbox("sauna_frame_t", x0 - 0.12, x1 + 0.12, y0 - 0.03, y0 + 0.02, H - 0.04, H + 0.10, "bronze")
    for xx in (x0 - 0.12, x1):
        gbox("sauna_frame_s", xx, xx + 0.12, y0 - 0.03, y0 + 0.02, 0.0, H + 0.10, "bronze")
    gbox("sauna_sill", x0, x1, y0 - 0.03, y0 + 0.03, 0.0, 0.012, "bronze")


def build_spa():
    bpy.context.scene.world = _black_world()
    deck = stone_tiles("spa_floor", (0.55, 0.51, 0.45), 1.2, 0.6, 0.003, 0.34, "XY", 0.7, 0.45, 0.62)    # the pool deck's
    basalt = stone_tiles("basalt_wall", (0.17, 0.162, 0.152), 1.2, 2.4, 0.003, 0.36, "YZ", 0.6, 0.35, 0.4)
    basalt_x = stone_tiles("basalt_far", (0.17, 0.162, 0.152), 1.2, 2.4, 0.003, 0.36, "XZ", 0.6, 0.35, 0.4)
    plaster("spa_ceiling", (0.82, 0.81, 0.78))
    travertine("desk_trav", (0.80, 0.73, 0.62), flute=("X", 0.045), rough=0.38)
    travertine("travertine", (0.78, 0.71, 0.60))
    onyx("onyx", (1.0, 0.70, 0.40), 2.0, "XZ")
    emit("cove_led", (1.0, 0.80, 0.58), 16.0)
    emit("strip_led", (1.0, 0.84, 0.66), 24.0)
    emit("sauna_led", (1.0, 0.62, 0.30), 14.0)
    glass_clear("door_glass")
    glass_clear("sauna_glass", (0.91, 0.88, 0.83), 0.08)
    pmat("opal", (0.95, 0.93, 0.90), 0.3, emission=((1.0, 0.82, 0.60), 5.0), subsurf=0.2)
    pmat("sauna_stone", (0.21, 0.205, 0.20), 0.9, bump=0.6, bump_scale=30.0)
    wood("walnut_door", (0.12, 0.07, 0.042), (0.23, 0.14, 0.08), 22.0, 0.36, along="Z", coat=0.15)
    plank("sauna_wall_x", (0.56, 0.40, 0.25), (0.68, 0.51, 0.33), "X", "Z")
    plank("sauna_wall_y", (0.56, 0.40, 0.25), (0.68, 0.51, 0.33), "Y", "Z")
    plank("sauna_ceil", (0.52, 0.37, 0.23), (0.64, 0.48, 0.31), "X", "Y")
    plank("sauna_bench", (0.60, 0.44, 0.28), (0.72, 0.55, 0.36), "X", "Y", 10.0, 0.6)     # separate slats: no joint lines
    # the room: the floor, the ceiling, the walls
    gbox("spa_floor", SX0, SX1, SY0, SY1, -0.05, 0.0, deck)
    # the near wall: oak slats (the pool's and the gym's), over the entrance door they start at its head
    DX0, DX1 = SX + 3.35, SX + 4.65
    gbox("spa_wall_b_back", SX0, SX1, SY0 - 0.2, SY0 - 0.04, 0.0, SCEIL, "shadowgap")
    x = SX0 + 0.06
    while x < SX1 - 0.03:
        z_from = 2.62 if DX0 - 0.1 < x < DX1 + 0.1 else 0.0
        gbox("spa_slat_b", x - 0.026, x + 0.026, SY0 - 0.04, SY0 + 0.005, z_from, SCEIL, "oak_slat")
        x += 0.11
    obj("spa_entrance_glass", [(DX0 + 0.05, SY0 - 0.02, 0.02), (DX1 - 0.05, SY0 - 0.02, 0.02), (DX1 - 0.05, SY0 - 0.02, 2.5),
                               (DX0 + 0.05, SY0 - 0.02, 2.5)], [(0, 1, 2, 3)], "door_glass")
    gbox("spa_door_frame_l", DX0, DX0 + 0.05, SY0 - 0.05, SY0 + 0.01, 0.0, 2.55, "bronze")
    gbox("spa_door_frame_r", DX1 - 0.05, DX1, SY0 - 0.05, SY0 + 0.01, 0.0, 2.55, "bronze")
    gbox("spa_door_frame_t", DX0, DX1, SY0 - 0.05, SY0 + 0.01, 2.5, 2.62, "bronze")
    rod("spa_door_pull", (DX0 + 0.2, SY0 + 0.07, 0.8), (DX0 + 0.2, SY0 + 0.07, 1.9), 0.015, "bronze", 12)
    gbox("spa_corridor", DX0 - 0.4, DX1 + 0.4, SY0 - 2.5, SY0 - 0.2, 0.0, 0.01, deck)
    # the left wall: oak slats, the three treatment rooms' doors (walnut, bronze frames and pulls)
    gbox("spa_wall_l_back", SX0 - 0.2, SX0 - 0.04, SY0, SY1, 0.0, SCEIL, "shadowgap")
    y = SY0 + 0.06
    while y < SY1 - 0.03:
        z_from = 2.62 if any(abs(y - ty) < 0.62 for ty in TREAT_Y) else 0.0
        gbox("spa_slat_l", SX0 - 0.04, SX0 + 0.005, y - 0.026, y + 0.026, z_from, SCEIL, "oak_slat")
        y += 0.11
    for k, ty in enumerate(TREAT_Y):
        gbox("spa_treat_door%d" % k, SX0 - 0.03, SX0 + 0.005, ty - 0.5, ty + 0.5, 0.0, 2.52, "walnut_door", bev=0.003)
        gbox("spa_treat_back%d" % k, SX0 - 0.2, SX0 - 0.03, ty - 0.55, ty + 0.55, 0.0, 2.6, "shadowgap")
        for yy in (ty - 0.55, ty + 0.51):
            gbox("spa_treat_jamb", SX0 - 0.03, SX0 + 0.03, yy, yy + 0.04, 0.0, 2.6, "bronze")
        gbox("spa_treat_head", SX0 - 0.03, SX0 + 0.03, ty - 0.55, ty + 0.55, 2.52, 2.62, "bronze")
        rod("spa_treat_pull%d" % k, (SX0 + 0.07, ty + 0.34, 0.85), (SX0 + 0.07, ty + 0.34, 1.75), 0.014, "bronze", 12)
        for zz in (0.95, 1.65):
            rod("spa_treat_post", (SX0 + 0.005, ty + 0.34, zz), (SX0 + 0.07, ty + 0.34, zz), 0.007, "bronze", 8)
    # the right wall: basalt (the pool's), grazed from above
    gbox("spa_wall_r", SX1, SX1 + 0.2, SY0, SY1, 0.0, SCEIL, basalt)
    # the far wall: basalt around the sauna's glass front
    gbox("spa_wall_f_l", SX0, SAU_X0 - 0.1, SY1, SY1 + 0.2, 0.0, SCEIL, basalt_x)
    gbox("spa_wall_f_r", SAU_X1 + 0.1, SX1, SY1, SY1 + 0.2, 0.0, SCEIL, basalt_x)
    gbox("spa_wall_f_t", SAU_X0 - 0.1, SAU_X1 + 0.1, SY1, SY1 + 0.2, SAU_H + 0.08, SCEIL, basalt_x)
    build_sauna()
    # the reception (near left): a backlit onyx panel in bronze on the slats, a fluted travertine counter, a walnut ledge
    OX0, OX1 = SX0 + 1.0, SX0 + 4.6
    gbox("spa_onyx", OX0, OX1, SY0 + 0.04, SY0 + 0.07, 0.45, 2.95, "onyx")
    gbox("spa_onyx_frame_b", OX0 - 0.05, OX1 + 0.05, SY0 + 0.0, SY0 + 0.09, 0.40, 0.45, "bronze")
    gbox("spa_onyx_frame_t", OX0 - 0.05, OX1 + 0.05, SY0 + 0.0, SY0 + 0.09, 2.95, 3.00, "bronze")
    for xx in (OX0 - 0.05, OX1):
        gbox("spa_onyx_frame_s", xx, xx + 0.05, SY0 + 0.0, SY0 + 0.09, 0.40, 3.00, "bronze")
    CX0, CX1, CY0, CY1 = OX0 + 0.2, OX1 - 0.2, SY0 + 1.75, SY0 + 2.45
    gbox("spa_counter", CX0, CX1, CY0, CY1 - 0.06, 0.08, 1.05, "desk_trav", bev=0.004)
    gbox("spa_counter_plinth", CX0 + 0.06, CX1 - 0.06, CY0 + 0.06, CY1 - 0.12, 0.0, 0.08, "shadowgap")
    gbox("spa_counter_ledge", CX0 - 0.04, CX1 + 0.04, CY0 - 0.06, CY1, 1.05, 1.10, "walnut", bev=0.006)
    gbox("spa_counter_brass", CX0, CX1, CY1 - 0.066, CY1 - 0.06, 0.08, 0.10, "brass")
    gbox("spa_counter_work", CX0 + 0.05, CX1 - 0.05, CY0 - 0.40, CY0, 0.74, 0.78, "walnut", bev=0.005)
    branches_vase("spa_vase", CX0 + 0.45, CY0 + 0.32, 1.10, 0.30, 0.07, "ceramic_white", 5, 0.25)
    cyl("spa_bowl", CX1 - 0.6, CY0 + 0.30, 1.10, 1.17, 0.15, "ceramic_clay", 40, r_top=0.18)
    for k in range(3):
        rod("spa_desk_towel", (CX1 - 1.25 + k * 0.17, CY0 + 0.12, 1.155), (CX1 - 1.25 + k * 0.17, CY0 + 0.46, 1.155), 0.05, "towel", 16)
    for k, xx in enumerate((CX0 + 0.8, CX1 - 0.8)):
        sphere("spa_pendant%d" % k, xx, (CY0 + CY1) / 2, 2.35, 0.15, "opal")
        cyl("spa_pendant_cord", xx, (CY0 + CY1) / 2, 2.50, SCEIL, 0.004, "brass", 6)
        cyl("spa_pendant_canopy", xx, (CY0 + CY1) / 2, SCEIL - 0.02, SCEIL, 0.06, "brass", 24)
        light("spa_pendant_l%d" % k, "POINT", (xx, (CY0 + CY1) / 2, 2.30), 9.0, (1.0, 0.80, 0.58), 0.1)
    # the towel cabinet beside the entrance
    towel_cabinet("spa_towels", SX + 0.4, SX + 2.95, SY0, 1)
    # the relaxation loungers before the basalt wall (heads to the wall), side tables between them
    LYS = (12.0, 14.25, 16.5, 18.75)
    for k, ly in enumerate(LYS):
        relax_lounger("spa_lounger%d" % k, SX1 - 1.55, ly, 0.0, "linen_sand" if k % 2 == 0 else "boucle")
    for k, ty in enumerate(((LYS[0] + LYS[1]) / 2, (LYS[2] + LYS[3]) / 2)):
        cyl("spa_side%d" % k, SX1 - 0.75, ty, 0.0, 0.46, 0.21, "travertine", 48, bev=0.01)
        if k == 0:
            cyl("spa_carafe", SX1 - 0.80, ty - 0.05, 0.46, 0.70, 0.048, "door_glass", 24)
            cyl("spa_glass", SX1 - 0.68, ty + 0.08, 0.46, 0.56, 0.032, "door_glass", 20)
        else:
            box("spa_folded", SX1 - 0.75, ty, 0.46, 0.26, 0.20, 0.05, "towel", 8.0, bev=0.015)
            cyl("spa_cup", SX1 - 0.70, ty + 0.05, 0.51, 0.58, 0.04, "ceramic_white", 24)
    # the planter down the middle: travertine, pale pebbles, two olive trees
    QX0, QX1, QY0, QY1 = SX - 2.2, SX - 0.9, 11.6, 19.2
    for nm, a in (("l", (QX0, QX0 + 0.07, QY0, QY1)), ("r", (QX1 - 0.07, QX1, QY0, QY1)), ("n", (QX0 + 0.07, QX1 - 0.07, QY0, QY0 + 0.07)),
                  ("f", (QX0 + 0.07, QX1 - 0.07, QY1 - 0.07, QY1))):
        gbox("spa_planter_" + nm, a[0], a[1], a[2], a[3], 0.0, 0.42, "travertine", bev=0.006)
    gbox("spa_planter_bed", QX0 + 0.07, QX1 - 0.07, QY0 + 0.07, QY1 - 0.07, 0.0, 0.355, pebble_bed("pebble_bed"))
    pmat("pebble", (0.70, 0.68, 0.64), 0.55, bump=0.2, bump_scale=60.0)
    pmat("pebble_d", (0.46, 0.45, 0.43), 0.55, bump=0.2, bump_scale=60.0)
    rp = random.Random(41)
    for k in range(140):
        r = rp.uniform(0.03, 0.055)
        sphere("spa_pebble", rp.uniform(QX0 + 0.09, QX1 - 0.09), rp.uniform(QY0 + 0.09, QY1 - 0.09), 0.355 + r * 0.32, r,
               "pebble" if rp.random() < 0.7 else "pebble_d", 1.0, rp.uniform(0.7, 1.0), 0.5, 10)
    olive_tree("spa_olive_a", (QX0 + QX1) / 2, 13.4, 2.6, seed=43, pot_r=0.28, pot_h=0.35, leaves=15000, pot_mat="pebble_bed")
    olive_tree("spa_olive_b", (QX0 + QX1) / 2, 17.4, 2.4, seed=47, pot_r=0.28, pot_h=0.35, leaves=14000, pot_mat="pebble_bed")
    # a wool runner along the treatment rooms' doors
    RX0, RX1, RY0, RY1 = SX0 + 0.45, SX0 + 1.75, 10.6, 20.6
    box("spa_runner", (RX0 + RX1) / 2, (RY0 + RY1) / 2, 0.0, RX1 - RX0, RY1 - RY0, 0.012,
        rug("spa_runner", (0.30, 0.26, 0.22), (RX0 + RX1) / 2, (RY0 + RY1) / 2, (RX1 - RX0) / 2, (RY1 - RY0) / 2), 0, bev=0.004)
    # two tall ceramic vessels flanking the sauna
    for k, xx in enumerate((SAU_X0 - 1.1, SAU_X1 + 1.1)):
        cyl("spa_vessel%d" % k, xx, SY1 - 0.55, 0.0, 0.95, 0.24, "ceramic_clay", 48, bev=0.02, r_top=0.15)
    # the ceiling: plaster, a raised coffer over the lounge with a hidden cove (the pool's), a wash slot along the doors
    KX0, KX1, KY0, KY1 = SX - 3.4, SX + 3.0, 10.8, 20.4
    CC = SCEIL + 0.35
    for nm, a in (("l", (SX0, KX0, SY0, SY1)), ("r", (KX1, SX1, SY0, SY1)), ("n", (KX0, KX1, SY0, KY0)), ("f", (KX0, KX1, KY1, SY1))):
        gbox("spa_ceil_" + nm, a[0], a[1], a[2], a[3], SCEIL, SCEIL + 0.05, "spa_ceiling")
    gbox("spa_coffer", KX0, KX1, KY0, KY1, CC, CC + 0.05, "spa_ceiling")
    for nm, a in (("l", (KX0 - 0.03, KX0, KY0, KY1)), ("r", (KX1, KX1 + 0.03, KY0, KY1)), ("n", (KX0, KX1, KY0 - 0.03, KY0)),
                  ("f", (KX0, KX1, KY1, KY1 + 0.03))):
        gbox("spa_coffer_side_" + nm, a[0], a[1], a[2], a[3], SCEIL, CC, "spa_ceiling")
    for nm, a in (("l", (KX0, KX0 + 0.13, KY0, KY1)), ("r", (KX1 - 0.13, KX1, KY0, KY1)), ("n", (KX0, KX1, KY0, KY0 + 0.13)),
                  ("f", (KX0, KX1, KY1 - 0.13, KY1))):
        gbox("spa_coffer_ledge_" + nm, a[0], a[1], a[2], a[3], SCEIL + 0.10, SCEIL + 0.13, "spa_ceiling")
    for nm, a in (("l", (KX0 + 0.08, KX0 + 0.11, KY0 + 0.1, KY1 - 0.1)), ("r", (KX1 - 0.11, KX1 - 0.08, KY0 + 0.1, KY1 - 0.1)),
                  ("n", (KX0 + 0.1, KX1 - 0.1, KY0 + 0.08, KY0 + 0.11)), ("f", (KX0 + 0.1, KX1 - 0.1, KY1 - 0.11, KY1 - 0.08))):
        gbox("spa_coffer_led_" + nm, a[0], a[1], a[2], a[3], SCEIL + 0.13, SCEIL + 0.132, "cove_led")
    for k, (x, y, w, h) in enumerate(((KX0 + 0.095, (KY0 + KY1) / 2, 0.05, KY1 - KY0 - 0.4), (KX1 - 0.095, (KY0 + KY1) / 2, 0.05, KY1 - KY0 - 0.4),
                                      ((KX0 + KX1) / 2, KY0 + 0.095, KX1 - KX0 - 0.4, 0.05), ((KX0 + KX1) / 2, KY1 - 0.095, KX1 - KX0 - 0.4, 0.05))):
        light("spa_cove%d" % k, "AREA", (x, y, SCEIL + 0.15), 75.0 if h > w else 52.0, (1.0, 0.82, 0.62), w, h, aim=(0, 0, 1), spread=150)
    xl = SX0 + 0.28
    gbox("spa_wash_slot", xl - 0.10, xl + 0.10, SY0 + 1.0, SY1 - 1.0, SCEIL - 0.004, SCEIL, "shadowgap")
    gbox("spa_wash_led", xl - 0.03, xl + 0.03, SY0 + 1.05, SY1 - 1.05, SCEIL - 0.006, SCEIL - 0.004, "strip_led")
    light("spa_wash", "AREA", (xl, (SY0 + SY1) / 2, SCEIL - 0.02), 190.0, (1.0, 0.84, 0.66), 0.06, SY1 - SY0 - 2.1, aim=(0, 0, -1), spread=110)
    for k in range(6):
        y = SY0 + 3.3 + k * 2.1
        light("spa_graze%d" % k, "SPOT", (SX1 - 0.35, y, SCEIL - 0.08), 70.0, (1.0, 0.82, 0.62), 0.02, aim=(0.38, 0, -1), spot=36.0, blend=0.4)
        cyl("spa_graze_rim%d" % k, SX1 - 0.35, y, SCEIL - 0.006, SCEIL - 0.001, 0.05, "downlight_rim", 20)
        cyl("spa_graze_em%d" % k, SX1 - 0.35, y, SCEIL - 0.007, SCEIL - 0.006, 0.035, "downlight_emit", 16)
    for k, x in enumerate((SAU_X0 - 1.6, SAU_X0 - 0.6, SAU_X1 + 0.6, SAU_X1 + 1.6)):
        light("spa_fgraze%d" % k, "SPOT", (x, SY1 - 0.35, SCEIL - 0.08), 55.0, (1.0, 0.82, 0.62), 0.02, aim=(0, 0.38, -1), spot=36.0, blend=0.4)
        cyl("spa_fgraze_rim%d" % k, x, SY1 - 0.35, SCEIL - 0.006, SCEIL - 0.001, 0.05, "downlight_rim", 20)
        cyl("spa_fgraze_em%d" % k, x, SY1 - 0.35, SCEIL - 0.007, SCEIL - 0.006, 0.035, "downlight_emit", 16)
    for k, (x, y) in enumerate(((SX + 1.7, SY0 + 1.6), (SX + 4.0, SY0 + 1.6), (SX - 0.5, SY0 + 2.6), (SX - 2.0, SY1 - 1.2),
                                (SX + 2.0, SY1 - 1.2))):
        downlight("spa_dl%d" % k, x, y, SCEIL, 26.0, 60.0)
    camera(SX, SY0 + 4.0, 1.6)
    marks = [("the sauna's glass front (its middle)", (SX, SY1, 1.2)), ("the loungers (their middle)", (SX1 - 1.55, 15.4, 0.6)),
             ("the planter's olives (its middle)", ((QX0 + QX1) / 2, 15.4, 1.5)),
             ("the reception counter", ((CX0 + CX1) / 2, (CY0 + CY1) / 2, 1.05)), ("the backlit onyx", ((OX0 + OX1) / 2, SY0, 1.7))]
    doors = [("spa_entrance", ((DX0 + DX1) / 2, SY0, 1.3))]
    for k, ty in enumerate(TREAT_Y):
        doors.append(("spa_treatment_room_%d" % (k + 1), (SX0, ty, 1.3)))
    doors.append(("spa_sauna_door", ((SAU_X1 - 0.95 + SAU_X1 - 0.12) / 2, SY1, 1.2)))
    report("spa: the residents' spa and treatment rooms on a basement level (the builder: 'on one of the basement levels'), "
           "level -1 beside the pool hall and its place an illustration; room %.0f x %.0f m, %.1f m clear; sauna %.1f x %.1f m; "
           "no window" % (SX1 - SX0, SY1 - SY0, SCEIL, SAU_X1 - SAU_X0, SAU_D), marks, doors)


# ============================================================================================ 5. the parking (basement level -2)
PCL = 3.1                                        # the slab's soffit, room-local
XA0, XA1 = 7.6, 13.6                             # the drive aisle (6 m), along the facing
XB0, XB1 = 2.6, 18.6                             # the bays' back walls (5 m bays on each side)
PY_END, PY_FAR = -8.0, 58.5                      # the end wall behind the eye, the far wall
VX, VY, VCEIL = 7.4, 3.3, 2.7                    # the lift vestibule: its glass front, half width, ceiling
COLS_Y = [-7.2 + 8.1 * k for k in range(9)]      # the column lines: 8.1 m, three 2.5 m bays between
EYE_PK = (10.6, 3.6, 1.6)                       # in the aisle, past the crossing


def epoxy(name, color, rough=0.26, joint=6.0):
    """a car park's epoxy-coated slab: a soft mottle, tyre-worn patches in the gloss, the slab's saw-cut joints every 6 m"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    x, y, z = b.sep(ob)
    n1 = b.noise(ob, 0.25, 5.0, 0.6)
    n2 = b.noise(ob, 2.5, 4.0, 0.6)
    n3 = b.noise(ob, 40.0, 3.0, 0.6)
    col = b.mix(b.m("MULTIPLY", n1.outputs["Fac"], 0.9), tuple(c * 0.90 for c in color), tuple(min(1, c * 1.07) for c in color))
    col = b.mix(b.m("MULTIPLY", n2.outputs["Fac"], 0.25), col, tuple(c * 0.92 for c in color))
    j = b.m("MAXIMUM", b.m("LESS_THAN", b.m("FRACT", b.m("DIVIDE", x, joint)), 0.006 / joint),
            b.m("LESS_THAN", b.m("FRACT", b.m("DIVIDE", y, joint)), 0.006 / joint))
    col = b.mix(b.m("MULTIPLY", j, 0.8), col, tuple(c * 0.45 for c in color))
    p = b.principled(Base_Color=col, Roughness=b.m("ADD", rough, b.m("MULTIPLY", n2.outputs["Fac"], 0.18)))
    b.put(p.inputs["Coat Weight"], 0.35)
    b.put(p.inputs["Coat Roughness"], b.m("ADD", 0.06, b.m("MULTIPLY", n1.outputs["Fac"], 0.12)))
    b.put(p.inputs["Normal"], b.bump(b.m("ADD", b.m("SUBTRACT", 1.0, j), b.m("MULTIPLY", n3.outputs["Fac"], 0.15)), 0.2, 0.01))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def banded(name, top, band, band_h=1.05, rough=0.8, line=(0.40, 0.29, 0.18)):
    """a painted wall or column: a warm white above, a charcoal band below, a thin bronze-tone line between"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    x, y, z = b.sep(ob)
    nz = b.noise(ob, 1.5, 5.0, 0.6)
    col = b.mix(b.m("MULTIPLY", nz.outputs["Fac"], 0.10), top, tuple(c * 0.94 for c in top))
    lo = b.m("LESS_THAN", z, band_h)
    ln = b.m("MULTIPLY", b.m("GREATER_THAN", z, band_h), b.m("LESS_THAN", z, band_h + 0.03))
    col = b.mix(lo, col, band)
    col = b.mix(ln, col, line)
    p = b.principled(Base_Color=col, Roughness=b.mixf(lo, rough, 0.45))
    b.put(p.inputs["Specular IOR Level"], 0.35)
    fine = b.noise(ob, 90.0, 3.0, 0.6)
    b.put(p.inputs["Normal"], b.bump(fine.outputs["Fac"], 0.012, 0.1))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def hatch_mat(name, color, pitch=0.7, frac=0.32):
    """painted diagonal hatching (a no-parking area): paint stripes, the floor showing between them"""
    m, nt, b, out = _mat(name)
    ob = b.n("ShaderNodeTexCoord").outputs["Object"]
    x, y, z = b.sep(ob)
    s = b.m("LESS_THAN", b.m("FRACT", b.m("DIVIDE", b.m("ADD", x, y), pitch)), frac)
    p = b.principled(Base_Color=color, Roughness=0.5)
    tr = b.n("ShaderNodeBsdfTransparent", {"Color": (1, 1, 1)})
    nt.links.new(b.mixs(s, tr.outputs[0], p.outputs[0]), out.inputs["Surface"])
    return m


def car(name, cx, cy, rot, paint, kind="sedan"):
    """a generic parked car, no make (an illustration): a body lofted from 16-point sections along its length (its plan's
    rounded corners, the wheel arches cut into its underside, a glasshouse over the belt line), dark glass, black trim,
    lamp lenses (off), four wheels; no badge, no plate, no lettering. With rot 0 its nose points +X"""
    P = Pr(cx, cy, rot)
    if kind == "suv":
        L, Wd, R, FO, WB = 4.70, 1.90, 0.37, 0.92, 2.80
        prof = [(0.0, 0.92), (0.03, 1.06), (0.07, 1.14), (0.10, 1.50), (0.16, 1.66), (0.60, 1.68), (0.71, 1.40), (0.79, 1.16),
                (0.90, 1.08), (0.97, 0.99), (1.0, 0.84)]
        belt_r, belt_f, zb0, b_pillar = 1.13, 1.08, 0.25, (0.45, 0.48)
    else:
        L, Wd, R, FO, WB = 4.80, 1.84, 0.33, 0.95, 2.85
        prof = [(0.0, 0.80), (0.03, 0.94), (0.10, 1.01), (0.21, 1.03), (0.30, 1.24), (0.39, 1.42), (0.60, 1.44), (0.70, 1.20),
                (0.78, 1.00), (0.92, 0.92), (0.98, 0.84), (1.0, 0.70)]
        belt_r, belt_f, zb0, b_pillar = 1.01, 0.96, 0.20, (0.485, 0.51)

    def top(t):
        for (t0, z0_), (t1, z1) in zip(prof, prof[1:]):
            if t <= t1:
                return z0_ + (z1 - z0_) * (t - t0) / (t1 - t0)
        return prof[-1][1]

    axles = (L / 2 - FO, L / 2 - FO - WB)

    def bottom(x, t):
        zb = zb0 + 0.10 * max(0.0, abs(2 * t - 1) - 0.82) / 0.18
        for xw in axles:
            d, ra = abs(x - xw), R + 0.07
            if d < ra:
                zb = max(zb, R + math.sqrt(ra * ra - d * d))
        return zb

    CR = 0.50

    def half_w(x):
        d = L / 2 - abs(x)
        return Wd / 2 if d >= CR else Wd / 2 - CR + math.sqrt(max(0.0, CR * CR - (CR - d) ** 2))

    def gl(t):
        return max(0.0, min(1.0, (top(t) - (belt_r + (belt_f - belt_r) * t)) / 0.22))

    NS = 84
    ts = [0.5 - 0.5 * math.cos(math.pi * i / (NS - 1)) for i in range(NS)]
    V, F, MI = [], [], []
    for t in ts:
        x = -L / 2 + t * L
        w = half_w(x)
        zt = top(t)
        zbl = min(belt_r + (belt_f - belt_r) * t, zt)
        g = gl(t)
        zb = bottom(x, t)
        lp = lambda a, c: a + (c - a) * g
        half = [(0.0, zb), (0.80 * w, zb), (0.97 * w, zb + 0.07), (w, (zb + 0.07 + zbl - 0.10) / 2), (w, zbl - 0.10), (0.975 * w, zbl),
                (lp(0.93 * w, 0.80 * w), lp(zbl + 0.012, zbl + 0.85 * (zt - zbl))), (lp(0.62 * w, 0.68 * w), lp(zbl + 0.03, zt)),
                (0.0, lp(zbl + 0.04, zt + 0.012))]
        for (yy, zz) in half + [(-yy, zz) for (yy, zz) in half[-2:0:-1]]:
            px, py = P(x, yy)
            V.append((px, py, zz))
    for i in range(NS - 1):
        tm = (ts[i] + ts[i + 1]) / 2
        gm = gl(tm)
        steep = abs(top(ts[i + 1]) - top(ts[i])) / max(1e-6, (ts[i + 1] - ts[i]) * L) > 0.45
        for j in range(16):
            a, c = i * 16 + j, (i + 1) * 16 + j
            F.append((a, i * 16 + (j + 1) % 16, (i + 1) * 16 + (j + 1) % 16, c))
            e = j if j < 8 else 15 - j
            mi = 0
            if e in (0, 1):
                mi = 2
            elif e in (5, 6) and gm > 0.55:
                mi = 2 if b_pillar[0] < tm < b_pillar[1] else 1
            elif e == 7 and gm > 0.55 and steep:
                mi = 1
            elif e == 2 and tm > 0.975:
                mi = 2
            elif e in (3, 4) and tm > 0.955:
                mi = 3
            elif e == 4 and tm < 0.035:
                mi = 4
            MI.append(mi)
    F.append(tuple(range(16))[::-1])
    MI.append(0)
    F.append(tuple((NS - 1) * 16 + k for k in range(16)))
    MI.append(0)
    me = bpy.data.meshes.new(name)
    me.from_pydata(V, [], F)
    me.update()
    for mt in (paint, "car_glass", "car_trim", "car_head", "car_tail"):
        me.materials.append(M[mt])
    me.polygons.foreach_set("material_index", MI)
    crease = {2: 0.55, 14: 0.55, 5: 0.8, 11: 0.8, 7: 0.6, 9: 0.6}
    ca = me.attributes.new("crease_edge", "FLOAT", "EDGE")
    vals = []
    for ed in me.edges:
        v0, v1 = ed.vertices
        same = v0 % 16 == v1 % 16 and abs(v0 // 16 - v1 // 16) == 1
        vals.append(crease.get(v0 % 16, 0.0) if same else 0.0)
    ca.data.foreach_set("value", vals)
    ob = bpy.data.objects.new(name, me)
    KW.link(ob)
    own(ob)
    fix_normals(ob)
    sb = ob.modifiers.new("sub", "SUBSURF")
    sb.levels = sb.render_levels = 2
    for p in me.polygons:
        p.use_smooth = True
    # the side mirrors
    tmir = 0.70 if kind != "suv" else 0.72
    xm = -L / 2 + tmir * L
    for s in (-1, 1):
        mx, my = P(xm, s * (half_w(xm) + 0.07))
        box(name + "_mirror", mx, my, belt_r + (belt_f - belt_r) * tmir + 0.05, 0.20, 0.14, 0.12, paint, rot, bev=0.03)
    # the wheels: a tyre, a dark disc, a rim lip, five spokes, a hub
    for xw in axles:
        for s in (-1, 1):
            yo, yi = s * (Wd / 2 - 0.035), s * (Wd / 2 - 0.27)
            q = lambda lx, ly, lz: (P(lx, ly)[0], P(lx, ly)[1], lz)
            rod(name + "_tyre", q(xw, yi, R), q(xw, yo, R), R, "rubber_black", 40, bev=0.05)
            rod(name + "_disc", q(xw, yo - s * 0.01, R), q(xw, yo + s * 0.004, R), R * 0.66, "car_trim", 36)
            ring = [q(xw + R * 0.63 * math.cos(2 * math.pi * k / 36), yo + s * 0.006, R + R * 0.63 * math.sin(2 * math.pi * k / 36)) for k in range(37)]
            tube(name + "_lip", ring, 0.02, "car_rim", 8)
            for k in range(5):
                an = 2 * math.pi * k / 5 + 0.3
                rod(name + "_spoke", q(xw + 0.05 * math.cos(an), yo + s * 0.008, R + 0.05 * math.sin(an)),
                    q(xw + R * 0.61 * math.cos(an), yo + s * 0.008, R + R * 0.61 * math.sin(an)), 0.026, "car_rim", 10)
            rod(name + "_hub", q(xw, yo, R), q(xw, yo + s * 0.016, R), 0.065, "car_rim", 20)
    return ob


def park_core():
    """the round slip-formed core (published) at level -2: fair-faced concrete from the slab to the soffit, two lift
    portals in bronze (the lobby's) on its face toward the aisle, inside the vestibule"""
    T_, DH = 0.35, 2.35
    ops = (76.0, 104.0)
    ha = math.degrees(0.70 / RC)
    edges = [e for a in ops for e in (a - ha, a + ha)]
    for i, (a0, a1) in enumerate(((edges[1], edges[2]), (edges[3], 360.0 + edges[0]))):
        sector("pcore_low%d" % i, a0, a1, RC - T_, RC, -0.05, DH, "core_concrete")
    ring_prism("pcore_high", circle(RC, 180), circle(RC - T_, 180), DH, PCL + 0.05, "core_concrete")
    lifts = []
    for i, a in enumerate(ops):
        n_ = Vector((math.sin(a * DEG), math.cos(a * DEG), 0))
        t_ = Vector((math.cos(a * DEG), -math.sin(a * DEG), 0))
        rot = math.degrees(math.atan2(t_.y, t_.x))
        c = n_ * (RC - 0.29)
        for s in (-1, 1):
            p = c + t_ * (s * 0.275)
            box("park_lift%d_leaf%d" % (i + 1, s), p.x, p.y, 0.0, 0.545, 0.03, 2.12, "bronze", rot, bev=0.003)
        p = c - n_ * 0.03
        box("park_lift%d_back" % (i + 1), p.x, p.y, 0.0, 1.40, 0.02, DH, "shadowgap", rot)
        for s in (-1, 1):
            p = n_ * (RC - 0.15) + t_ * (s * 0.69)
            box("park_lift%d_jamb" % (i + 1), p.x, p.y, 0.0, 0.02, 0.30, DH, "bronze", rot)
        p = n_ * (RC - 0.15)
        box("park_lift%d_head" % (i + 1), p.x, p.y, 2.12, 1.40, 0.30, DH - 2.12, "bronze", rot)
        lifts.append((c.x, c.y, 1.2))
    box("park_lift_call", RC + 0.006, 0.0, 1.02, 0.012, 0.075, 0.22, "steel", 0.0, bev=0.003)
    return lifts


def storage_door(nm, cx, cy, rot):
    """a storage room's door (an illustration): a painted steel leaf in a frame, a lever, a louvred vent; no number"""
    P = Pr(cx, cy, rot)
    x, y = P(0, 0.0)
    box(nm, x, y, 0.0, 0.95, 0.05, 2.12, "store_door", rot, bev=0.004)
    for s in (-1, 1):
        x, y = P(s * 0.51, 0.0)
        box(nm + "_jamb", x, y, 0.0, 0.07, 0.07, 2.19, "store_frame", rot, bev=0.004)
    x, y = P(0, 0.0)
    box(nm + "_head", x, y, 2.12, 1.09, 0.07, 0.07, "store_frame", rot, bev=0.004)
    x, y = P(0, 0.03)
    box(nm + "_vent", x, y, 0.14, 0.50, 0.012, 0.26, "car_trim", rot)
    for k in range(6):
        box(nm + "_louvre", x, y + 0.0, 0.16 + k * 0.04, 0.48, 0.02, 0.012, "store_door", rot)
    a, b_ = P(0.34, 0.04), P(0.34, 0.075)
    rod(nm + "_lever_post", (a[0], a[1], 1.02), (b_[0], b_[1], 1.02), 0.012, "steel", 10)
    a, b_ = P(0.34, 0.075), P(0.20, 0.075)
    rod(nm + "_lever", (a[0], a[1], 1.02), (b_[0], b_[1], 1.02), 0.011, "steel", 10)
    x, y = P(0.34, 0.03)
    box(nm + "_rose", x, y, 0.95, 0.05, 0.012, 0.16, "steel", rot, bev=0.002)


def build_parking():
    bpy.context.scene.world = _black_world()
    epoxy("park_floor", (0.30, 0.295, 0.283), 0.20)
    pmat("paint_line", (0.80, 0.79, 0.75), 0.5, spec=0.4)
    hatch_mat("paint_hatch", (0.80, 0.79, 0.75))
    banded("park_wall", (0.80, 0.785, 0.75), (0.075, 0.075, 0.08), 1.05)
    banded("park_col", (0.82, 0.81, 0.78), (0.075, 0.075, 0.08), 1.05)
    plaster("park_soffit", (0.74, 0.735, 0.71), 0.92)
    plaster("vest_wall", (0.80, 0.78, 0.74))
    pmat("store_door", (0.20, 0.19, 0.18), 0.42, spec=0.5, coat=0.15)
    pmat("store_frame", (0.11, 0.105, 0.10), 0.45)
    pmat("pipe_paint", (0.80, 0.80, 0.78), 0.45)
    pmat("fan_body", (0.62, 0.63, 0.64), 0.32, metal=0.7)
    pmat("mat_coir", (0.10, 0.085, 0.065), 1.0, bump=0.8, bump_scale=300.0)
    emit("batten_led", (1.0, 0.93, 0.84), 30.0)
    emit("cove_led", (1.0, 0.80, 0.58), 16.0)
    stone_tiles("vest_floor", (0.66, 0.61, 0.53), 1.2, 0.6, 0.003, 0.24, "XY", 0.9, 0.5, 0.5)   # the lobby's stone
    concrete("core_concrete", (0.50, 0.48, 0.445))
    plaster("vest_ceiling", (0.84, 0.83, 0.80))
    glass_clear("vest_glass")
    pmat("car_white", (0.78, 0.78, 0.76), 0.22, coat=1.0, coat_rough=0.03)
    pmat("car_graphite", (0.055, 0.06, 0.065), 0.32, metal=0.6, coat=1.0, coat_rough=0.03)
    pmat("car_silver", (0.56, 0.57, 0.58), 0.34, metal=0.8, coat=1.0, coat_rough=0.03)
    pmat("car_slate", (0.07, 0.085, 0.10), 0.34, metal=0.6, coat=1.0, coat_rough=0.03)
    pmat("car_sand", (0.42, 0.38, 0.32), 0.34, metal=0.6, coat=1.0, coat_rough=0.03)
    pmat("car_glass", (0.010, 0.012, 0.014), 0.03, spec=0.9, coat=0.6, coat_rough=0.02)
    pmat("car_trim", (0.022, 0.022, 0.024), 0.5)
    pmat("car_head", (0.50, 0.52, 0.53), 0.06, metal=0.6, coat=1.0, coat_rough=0.02)
    pmat("car_tail", (0.22, 0.012, 0.010), 0.08, coat=1.0, coat_rough=0.02)
    pmat("car_rim", (0.55, 0.56, 0.57), 0.28, metal=1.0)
    # the slab, the soffit, the walls
    gbox("park_floor", XB0 - 0.3, XB1 + 0.3, PY_END - 0.3, PY_FAR + 0.3, -0.3, 0.0, "park_floor")
    gbox("park_soffit", XB0 - 0.3, XB1 + 0.3, PY_END - 0.3, PY_FAR + 0.3, PCL, PCL + 0.3, "park_soffit")
    gbox("park_wall_r", XB1, XB1 + 0.25, PY_END, PY_FAR, 0.0, PCL, "park_wall")
    gbox("park_wall_far", XB0, XB1, PY_FAR, PY_FAR + 0.25, 0.0, PCL, "park_wall")
    gbox("park_wall_end", XB0 - 0.25, XB1, PY_END - 0.25, PY_END, 0.0, PCL, "park_wall")
    gbox("park_wall_l", XB0 - 0.25, XB0, 4.3, PY_FAR, 0.0, PCL, "park_wall")
    gbox("park_wall_l2", XB0 - 0.25, XB0, PY_END, -4.3, 0.0, PCL, "park_wall")
    # the round core and the lift vestibule: a glazed front on the aisle in bronze, double glass doors, the lobby's stone
    lifts = park_core()
    for s in (-1, 1):
        y0_, y1_ = (VY, VY + 0.2) if s > 0 else (-VY - 0.2, -VY)
        gbox("park_vest_side", 3.6, VX + 0.06, y0_, y1_, 0.0, PCL, "park_wall")
        yi = (VY - 0.02, VY) if s > 0 else (-VY, -VY + 0.02)
        gbox("park_vest_side_in", 3.6, VX - 0.02, yi[0] - 0.0001 * s, yi[1] - 0.0001 * s, 0.0, VCEIL, "vest_wall")
    gbox("park_vest_floor", 3.2, VX, -VY, VY, 0.0, 0.008, "vest_floor")
    gbox("park_vest_ceiling", 3.2, VX - 0.02, -VY, VY, VCEIL, VCEIL + 0.05, "vest_ceiling")
    VD = 1.0
    for nm, (ya, yb, za, zb) in (("park_vest_side_l", (-VY + 0.06, -VD - 0.06, 0.02, 2.53)), ("park_vest_side_r", (VD + 0.06, VY - 0.06, 0.02, 2.53)),
                                 ("park_vest_transom", (-VD, VD, 2.42, 2.53))):
        obj(nm, [(VX, ya, za), (VX, yb, za), (VX, yb, zb), (VX, ya, zb)], [(0, 1, 2, 3)], "vest_glass")
    xd = VX + 0.02
    obj("park_vestibule_doors", [(xd, -VD + 0.05, 0.03), (xd, -0.03, 0.03), (xd, -0.03, 2.33), (xd, -VD + 0.05, 2.33),
                                 (xd, 0.03, 0.03), (xd, VD - 0.05, 0.03), (xd, VD - 0.05, 2.33), (xd, 0.03, 2.33)],
        [(0, 1, 2, 3), (4, 5, 6, 7)], "vest_glass")
    for t in (-1, 1):
        lc = t * VD / 2
        for (ya, yb) in ((lc - VD / 2, lc - VD / 2 + 0.05), (lc + VD / 2 - 0.05, lc + VD / 2)):
            gbox("park_door_stile", xd - 0.025, xd + 0.025, ya, yb, 0.0, 2.36, "bronze")
        gbox("park_door_rail_b", xd - 0.025, xd + 0.025, lc - VD / 2, lc + VD / 2, 0.0, 0.10, "bronze")
        gbox("park_door_rail_t", xd - 0.025, xd + 0.025, lc - VD / 2, lc + VD / 2, 2.30, 2.36, "bronze")
        rod("park_door_pull%d" % t, (xd + 0.09, t * 0.15, 0.75), (xd + 0.09, t * 0.15, 1.95), 0.016, "bronze", 12)
        for zz in (0.85, 1.85):
            rod("park_door_pull_post", (xd + 0.02, t * 0.15, zz), (xd + 0.09, t * 0.15, zz), 0.008, "bronze", 8)
    gbox("park_vest_head", VX - 0.04, VX + 0.06, -VD - 0.06, VD + 0.06, 2.36, 2.42, "bronze")
    for yy in (-VY, -VD - 0.06, VD, VY - 0.06):
        gbox("park_vest_mullion", VX - 0.05, VX + 0.06, yy, yy + 0.06, 0.0, 2.55, "bronze")
    gbox("park_vest_fascia", VX - 0.06, VX + 0.10, -VY - 0.2, VY + 0.2, 2.53, 2.74, "bronze")
    gbox("park_vest_above", VX - 0.06, VX + 0.06, -VY - 0.2, VY + 0.2, 2.74, PCL, "park_wall")
    gbox("park_vest_sill", VX - 0.06, VX + 0.08, -VY, VY, 0.0, 0.012, "bronze")
    gbox("park_vest_mat", 5.6, VX - 0.15, -1.1, 1.1, 0.008, 0.02, "mat_coir", bev=0.004)
    for k, yy in enumerate((-1.9, 0.0, 1.9)):
        downlight("park_vest_dl%d" % k, 6.6, yy, VCEIL, 18.0, 70.0)
    for (lx, ly, lz) in lifts:
        p = Vector((lx, ly, 0)) * ((RC + 0.75) / (RC - 0.29))
        light("park_vest_graze", "SPOT", (p.x, p.y, VCEIL - 0.03), 30.0, (1.0, 0.80, 0.58), 0.02, aim=(lx - p.x, ly - p.y, 1.1 - VCEIL),
              spot=38.0, blend=0.4)
    gbox("park_vest_cove", VX - 0.30, VX - 0.24, -VY + 0.1, VY - 0.1, VCEIL - 0.004, VCEIL, "cove_led")
    light("park_vest_cove_l", "AREA", (VX - 0.27, 0.0, VCEIL - 0.02), 22.0, (1.0, 0.80, 0.58), 0.05, 2 * VY - 0.3, aim=(0, 0, -1), spread=120)
    for yy in (-2.4, 2.4):
        cyl("park_bollard", VX + 0.45, yy, 0.0, 0.9, 0.08, "steel", 32, bev=0.01)
        cyl("park_bollard_band", VX + 0.45, yy, 0.72, 0.78, 0.0805, "car_trim", 32)
    # the columns, the drop panels over them
    for yc in COLS_Y:
        for xc in ((6.8, 14.4) if yc > 8.0 else (14.4,)):
            box("park_col", xc, yc, 0.0, 0.60, 0.60, PCL, "park_col", bev=0.025)
            gbox("park_drop", xc - 1.2, xc + 1.2, yc - 1.2, yc + 1.2, PCL - 0.22, PCL, "park_soffit")
    # the bays: white lines, three 2.5 m bays between the columns; the aisle and its crossing
    for k in range(len(COLS_Y) - 1):
        ya, yb = COLS_Y[k] + 0.3, COLS_Y[k + 1] - 0.3
        sides = (((XA1, XB1),) if COLS_Y[k] > 0.0 else ()) + (((XB0, XA0),) if COLS_Y[k] > 8.0 else ())
        for side in sides:
            for j in range(4):
                yl = ya + (yb - ya) * j / 3
                gbox("park_line", side[0], side[1], yl - 0.05, yl + 0.05, 0.0, 0.003, "paint_line")
    for k in range(7):
        x = XA0 + 0.25 + k * 0.85
        gbox("park_crossing", x, x + 0.45, -1.2, 1.2, 0.0, 0.003, "paint_line")
    gbox("park_hatch", XB0, XA0, 4.7, COLS_Y[2] - 0.35, 0.0, 0.003, "paint_hatch")
    for (a, b_, c, d) in ((XB0, XA0, 4.7, 4.8), (XB0, XA0, COLS_Y[2] - 0.45, COLS_Y[2] - 0.35), (XA0 - 0.1, XA0, 4.7, COLS_Y[2] - 0.35)):
        gbox("park_hatch_edge", a, b_, c, d, 0.0, 0.0035, "paint_line")
    # the storage rooms' doors: along the end wall behind the eye and the right wall beside it
    for k, x in enumerate((3.9, 6.5, 9.3, 11.9, 14.7, 17.3)):
        storage_door("park_storage_e%d" % k, x, PY_END + 0.025, 0.0)
    for k, y in enumerate((-5.4, -2.6)):
        storage_door("park_storage_r%d" % k, XB1 - 0.025, y, 90.0)
    # the light: linear LED battens under the soffit, over the aisle's edges and over the bays
    nl = 0
    rows = [(8.6, 2.7), (12.6, 2.7), (16.1, 4.05), (5.1, 4.05)]
    for (xr, step) in rows:
        y = PY_END + 1.4
        while y < PY_FAR - 0.8:
            if not (xr < 8.0 and y < COLS_Y[2] - 0.5):
                zb = PCL - 0.10
                box("park_batten", xr, y, zb, 0.08, 1.5, 0.06, "alu_white", bev=0.006)
                gbox("park_batten_led", xr - 0.03, xr + 0.03, y - 0.72, y + 0.72, zb - 0.002, zb, "batten_led")
                light("park_batten_l", "AREA", (xr, y, zb - 0.01), 42.0, (1.0, 0.93, 0.84), 0.05, 1.42, aim=(0, 0, -1), spread=150)
                for s in (-1, 1):
                    rod("park_batten_rod", (xr, y + s * 0.6, zb + 0.06), (xr, y + s * 0.6, PCL), 0.004, "steel", 6)
                nl += 1
            y += step
    # the sprinkler main and branches (painted), the heads; two jet fans over the aisle
    xm = 11.5
    rod("park_sprinkler_main", (xm, PY_END + 0.3, PCL - 0.30), (xm, PY_FAR - 0.3, PCL - 0.30), 0.05, "pipe_paint", 16)
    y = PY_END + 2.0
    while y < PY_FAR - 1.0:
        rod("park_hanger", (xm, y, PCL - 0.25), (xm, y, PCL), 0.006, "steel", 6)
        y += 4.0
    for k in range(len(COLS_Y) - 1):
        yb_ = (COLS_Y[k] + COLS_Y[k + 1]) / 2
        xs_ = VX + 0.06 if abs(yb_) < VY + 0.3 else XB0 + 0.4
        rod("park_branch", (xs_, yb_, PCL - 0.15), (XB1 - 0.4, yb_, PCL - 0.15), 0.025, "pipe_paint", 12)
        rod("park_branch_drop", (xm, yb_, PCL - 0.25), (xm, yb_, PCL - 0.15), 0.025, "pipe_paint", 12)
        for x in (XB0 + 1.5, XB0 + 4.5, XA0 + 1.5, XA1 - 1.5, XA1 + 1.5, XB1 - 1.5):
            if x < 8.0 and COLS_Y[k] < 8.0:
                continue
            cyl("park_head", x, yb_, PCL - 0.22, PCL - 0.15, 0.012, "steel", 10)
            cyl("park_head_def", x, yb_, PCL - 0.225, PCL - 0.218, 0.03, "steel", 16)
    for k, yf in enumerate((COLS_Y[3] + 4.05, COLS_Y[6] + 4.05)):
        xf, zf = 9.6, PCL - 0.42
        rod("park_fan%d" % k, (xf, yf - 0.8, zf), (xf, yf + 0.8, zf), 0.27, "fan_body", 40, bev=0.01)
        for s in (-1, 1):
            rod("park_fan_mouth", (xf, yf + s * 0.79, zf), (xf, yf + s * 0.805, zf), 0.24, "car_trim", 32)
            for r_ in (0.10, 0.17, 0.235):
                ring = [(xf + r_ * math.cos(2 * math.pi * q / 32), yf + s * 0.81, zf + r_ * math.sin(2 * math.pi * q / 32)) for q in range(33)]
                tube("park_fan_grille", ring, 0.004, "steel", 6)
            gbox("park_fan_bracket", xf - 0.18, xf + 0.18, yf + s * 0.5 - 0.03, yf + s * 0.5 + 0.03, zf + 0.22, PCL, "steel")
    # a few generic parked cars (no make, badge or plate)
    cars = [("park_car_a", 5.20, 21.15, 0.0, "car_graphite", "sedan"), ("park_car_b", 16.0, 21.15, 180.0, "car_slate", "suv"),
            ("park_car_c", 5.25, 26.75, 180.0, "car_white", "suv"), ("park_car_d", 16.0, 34.85, 0.0, "car_sand", "sedan")]
    for (nm, x, y, r, pt, kd) in cars:
        car(nm, x, y, r, pt, kd)
    camera(*EYE_PK)
    marks = [("the aisle's far wall (its middle)", (EYE_PK[0], PY_FAR, 1.5)), ("the storage doors on the end wall (the middle)", (10.6, PY_END, 1.1)),
             ("the round core (its face beside the vestibule)", (RC * math.sin(55 * DEG), RC * math.cos(55 * DEG), 1.5))]
    marks += [("car %s (%s)" % (nm[-1], kd), (x, y, 0.8)) for (nm, x, y, r, pt, kd) in cars]
    doors = [("park_lift_vestibule", (VX, 0.0, 1.2))]
    for i, (x, y, z) in enumerate(lifts):
        doors.append(("park_lift_%d" % (i + 1), (x, y, z)))
    doors += [("park_storage_end_wall", (10.6, PY_END, 1.1)), ("park_storage_right_wall", (XB1, -4.0, 1.1))]
    report("parking: the residents' private parking (1,620 spaces on 3 underground levels, the builder; 906 private + 720 "
           "public, Globes/Mako), level -2 and everything in it an illustration; floor %.1f m below the street, %.1f m to "
           "the soffit, aisle %.0f m, bays 2.5 x 5.0 m, columns every 8.1 m; %d LED battens; %d generic cars; no window, no "
           "sign, no number" % (-PARK_Z, PCL, XA1 - XA0, nl, len(cars)), marks, doors)


# ============================================================================================ build and render
common_materials()
{"lobby": build_lobby, "pool": build_pool, "gym": build_gym, "spa": build_spa, "parking": build_parking}[SCENE]()
diagnostics()
sc = bpy.context.scene
EXPO = {"lobby": {"sunset": -1.55, "day": -1.4}.get(TODN, -1.5), "pool": -0.6, "gym": -0.3, "spa": -0.35, "parking": -0.5}[SCENE]
sc.view_settings.exposure = EXPO + float(os.environ.get("KF_EXP", "0"))
if not os.environ.get("KF_NOGLARE"):
    KW.add_glare(3.5 / 2 ** sc.view_settings.exposure, float(os.environ.get("KF_GLARE", "0.18")))
if os.environ.get("KF_BORDER"):                   # a test of a region only: "x0,y0,x1,y1" in fractions of the frame
    bx0, by0, bx1, by1 = (float(v) for v in os.environ["KF_BORDER"].split(","))
    sc.render.use_border, sc.render.use_crop_to_border = True, True
    sc.render.border_min_x, sc.render.border_min_y, sc.render.border_max_x, sc.render.border_max_y = bx0, by0, bx1, by1
sc.render.filepath = OUT
print("RENDER %s | %d x %d, %d samples, %d threads, exposure %.2f | objects %d" % (SCENE, sc.render.resolution_x, sc.render.resolution_y,
                                                                                   sc.cycles.samples, sc.render.threads, sc.view_settings.exposure,
                                                                                   len(bpy.data.objects)))
bpy.ops.render.render(write_still=True)
print("WROTE", OUT)
