# -*- coding: utf-8 -*-
"""Kikar Hamedina (P9b prototype): "דירה לדוגמה", an example apartment inside tower C, floor 30, facing west to the sea.

  blender -b --factory-startup --python scripts/interior/kikar_interior.py -- <out.png> <shot> <tod> [width] [height]
          [samples] [threads]
  shot: living | bedroom | balcony | living360 | view   tod: day | sunset | evening

REAL (the same numbers as the shared web world, kikar_world.py): the tower's place and size (the municipal footprint), the
floor's height (floor 30: 116 m to the slab, the floor finish at 116.47 m, provisional 4.0 m a floor), the facing (floor 30's
plate turned 1.25 degrees a floor, so its west side faces 265.6 degrees, not 270), the facade system (MYS: white slabs and
white curtain walls; Alum Eshet: floor-to-ceiling unitised curtain wall, 300 mm aluminium fins, full-height pivot windows with
inner railings), the city in the window (every building at its surveyed height, the streets, the trees, the sea) and the sun
at the true hour.
ILLUSTRATION ("דירה לדוגמה"): the layout (a quarter of the floor, derived below), the room sizes, the ceiling height, the
balcony's size, every finish and every piece of furniture. The unit mix and the floor plans of the towers are not published.

The layout, derived: the glass line is world.js's superellipse plate (n 4.5) at 15.05 m from the tower's centre; a round core
(the slip-formed "circular turning core", its size is not published: 5.2 m radius here) and a 1.6 m lobby ring leave 8.25 m
of depth on the axis; four apartments a floor (453 apartments / 117 floors = 3.9) make each one a quarter of the plate,
about 150 m2 gross, which matches the published 4-room deals of 140 m2 (Globes 2.5.2025). The balcony: 4,000 m of balcony
railings for 453 apartments is about 8.8 m of railing each (Alum Eshet), on the slab's 1.25 m edge: 8.8 x 1.25 = 11 m2, near
the published "12 m2 balcony" (Sotheby's, floor 35)."""
import math
import os
import random
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kikar_world as KW  # noqa: E402

A = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = os.path.abspath(A[0]) if A else os.path.join(HERE, "_renders", "kikar-test.png")
SHOT = A[1] if len(A) > 1 else "living"
TODN = A[2] if len(A) > 2 else "sunset"
WIDTH = int(A[3]) if len(A) > 3 else 960
HEIGHT = int(A[4]) if len(A) > 4 else 540
SAMPLES = int(A[5]) if len(A) > 5 else 64
THREADS = int(A[6]) if len(A) > 6 else 14
TOWER = os.environ.get("KH_TOWER", "C")
FLOOR = int(os.environ.get("KH_FLOOR", "30"))
PHI_C = float(os.environ.get("KH_SIDE", "270"))       # the plate-local side the apartment faces (270 = its west side on floor 30)
DEG = math.pi / 180.0
rnd = random.Random(30)

KW.init(WIDTH, HEIGHT, SAMPLES, THREADS)
KW.sky_params(TODN)
KW.load_world()
NIGHT = TODN == "evening"
DUSK = TODN in ("sunset", "evening")
INSIDE = SHOT in ("living", "living3q", "bedroom", "living360", "view")
# the "window pull" of real-estate photography, done in the render: only what the camera sees THROUGH the curtain wall is
# darker (the light entering the room is untouched), so the view keeps its colour while the room is exposed for itself
PULL = float(os.environ.get("KH_PULL", {"day": 0.26, "sunset": 0.38, "evening": 1.0}[TODN])) if INSIDE else 1.0
# a shot seen from the room's dark back corner gets more exposure and, to keep the view the same, a stronger pull
SHOT_EXP = {("living3q", "day"): (0.8, 0.15)}
if (SHOT, TODN) in SHOT_EXP and "KH_PULL" not in os.environ:
    PULL = SHOT_EXP[(SHOT, TODN)][1]

T = KW.W["towers"][TOWER]
MOD = KW.W["model"]
NEXP = MOD.get("plate_n", 4.5)
HALF = T["side"] / 2
AG = HALF - MOD["slab_out"]                       # the glass line's half size (15.05 m for C)
TH = KW.plate_at(T, FLOOR)
BFACE = (TH + PHI_C) % 360                        # the true bearing the apartment faces
Y0 = (FLOOR - 1) * MOD["fh"]                      # the slab's underside
Z0 = Y0 + MOD["slab_t"]                           # the slab's top
FF = Z0 + 0.02                                    # the finished floor (parquet)
CEIL = 3.05                                       # the ceiling above the finished floor (illustration; "high ceilings" is a listing claim)
TOPG = Y0 + MOD["fh"] - FF                        # the glass reaches the slab above
CT = KW.tower_xy(T)
OUTL = (math.cos(PHI_C * DEG), math.sin(PHI_C * DEG))
RIGHTL = (math.cos((PHI_C + 90) * DEG), math.sin((PHI_C + 90) * DEG))
CORE_R = 5.2 + 1.6                               # the core (5.2 m radius, not published) and its 1.6 m lobby ring
BAL = 4.4                                         # half the balcony (8.8 m)


def plate_uv(s, d):
    """local (s to the right when facing out, d inward from the glass centre) -> plate-local (u, v)"""
    k = AG - d
    return (RIGHTL[0] * s + OUTL[0] * k, RIGHTL[1] * s + OUTL[1] * k)


def world_of(s, d, z=0.0):
    u, v = plate_uv(s, d)
    eu, ev = KW.dirv(TH), KW.dirv(TH + 90)
    return Vector((CT.x + u * eu.x + v * ev.x, CT.y + u * eu.y + v * ev.y, FF + z))


def d_glass(s):
    x = min(1.0, abs(s) / AG)
    return AG - AG * (1 - x ** NEXP) ** (1 / NEXP)


# the apartment's own frame: X = s (right), Y = outward (toward the view), Z up; origin = the glass centre at the floor
APT = bpy.data.objects.new("APT", None)
KW.link(APT)
APT.location = world_of(0, 0, 0)
APT.rotation_euler = (0, 0, -BFACE * DEG)
EYE_H_WORLD = KW.eye_h(FLOOR)


def L(s, d, z=0.0):
    return (s, -d, z)


def own(ob):
    ob.parent = APT
    return ob


print("APARTMENT tower %s floor %d plate %.2f faces %.2f; floor finish %.2f m; world eye %.1f m" % (TOWER, FLOOR, TH % 360, BFACE, FF, EYE_H_WORLD))


# ============================================================================================ interior materials
M = {}


def _mat(name):
    m, nt, b, out = KW.new_mat(name)
    M[name] = m
    return m, nt, b, out


def principled_mat(name, color, rough=0.5, metal=0.0, spec=0.5, coat=0.0, sheen=0.0, bump=None, bump_scale=200.0,
                   bump_strength=0.1, aniso=0.0, emission=None):
    m, nt, b, out = _mat(name)
    p = b.principled(Base_Color=color, Roughness=rough, Metallic=metal)
    b.put(p.inputs["Specular IOR Level"], spec)
    if coat:
        b.put(p.inputs["Coat Weight"], coat)
        b.put(p.inputs["Coat Roughness"], 0.12)
    if sheen:
        b.put(p.inputs["Sheen Weight"], sheen)
        b.put(p.inputs["Sheen Roughness"], 0.45)
    if aniso:
        b.put(p.inputs["Anisotropic"], aniso)
    if bump:
        tc = b.n("ShaderNodeTexCoord")
        nz = b.noise(tc.outputs["Object"], bump_scale, 6.0, 0.6)
        b.put(p.inputs["Normal"], b.bump(nz.outputs["Fac"], bump_strength, 0.2))
    if emission:
        b.put(p.inputs["Emission Color"], emission[0])
        b.put(p.inputs["Emission Strength"], emission[1])
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def oak_floor_mat():
    """oiled oak planks: grain along each plank, a tone per plank, a 1.5 mm rounded edge"""
    m, nt, b, out = _mat("oak_floor")
    uv = b.n("ShaderNodeUVMap", uv_map="grain")
    u, v, _ = b.sep(uv.outputs[0])
    pr = b.attr("prand").outputs["Fac"]
    g1 = b.noise(b.combine(b.m("MULTIPLY", u, 1.2), b.m("MULTIPLY", v, 90.0), b.m("MULTIPLY", pr, 17.0)), 1.0, 5.0, 0.55)
    g2 = b.noise(b.combine(b.m("MULTIPLY", u, 4.0), b.m("MULTIPLY", v, 140.0), b.m("MULTIPLY", pr, 29.0)), 1.0, 3.0, 0.5)
    wave = b.n("ShaderNodeTexWave", wave_type="BANDS", bands_direction="Y")
    b.put(wave.inputs["Vector"], b.combine(b.m("MULTIPLY", u, 0.4), b.m("ADD", v, b.m("MULTIPLY", pr, 3.0)), pr))
    wave.inputs["Scale"].default_value = 70.0
    wave.inputs["Distortion"].default_value = 2.5
    wave.inputs["Detail"].default_value = 2.0
    grain = b.m("ADD", b.m("MULTIPLY", wave.outputs["Fac"], 0.35), b.m("MULTIPLY", g1.outputs["Fac"], 0.65))
    base = b.ramp(grain, [(0.2, (0.385, 0.255, 0.14)), (0.55, (0.44, 0.30, 0.17)), (0.85, (0.475, 0.335, 0.195))])
    tone = b.ramp(pr, [(0.0, (0.80, 0.78, 0.76)), (0.3, (0.93, 0.92, 0.90)), (0.6, (1.0, 1.0, 1.0)), (1.0, (1.12, 1.07, 1.0))])
    col = b.n("ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
    b.put(col.inputs["Factor"], 1.0)
    b.put(col.inputs[6], base)
    b.put(col.inputs[7], tone)
    fleck = b.m("GREATER_THAN", g2.outputs["Fac"], 0.66)
    col2 = b.mix(b.m("MULTIPLY", fleck, 0.25), col.outputs[2], (0.58, 0.44, 0.28))
    rough = b.m("ADD", 0.30, b.m("MULTIPLY", grain, 0.18))
    p = b.principled(Base_Color=col2, Roughness=rough)
    b.put(p.inputs["Specular IOR Level"], 0.45)
    bev = b.n("ShaderNodeBevel", {"Radius": 0.0018})
    bev.samples = 6
    b.put(p.inputs["Normal"], b.bump(b.m("MULTIPLY", g1.outputs["Fac"], 1.0), 0.06, 0.2, bev.outputs[0]))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def wood_mat(name, c0, c1, scale=18.0, rough=0.42, along="Z", coat=0.0):
    m, nt, b, out = _mat(name)
    tc = b.n("ShaderNodeTexCoord")
    ob = tc.outputs["Object"]
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


def marble_mat(name="marble", base=(0.86, 0.85, 0.83), vein=(0.40, 0.38, 0.35), gold=(0.62, 0.52, 0.38)):
    """a honed white marble with grey and warm veins (the listings' "designer marble" is a claim; this is an illustration)"""
    m, nt, b, out = _mat(name)
    tc = b.n("ShaderNodeTexCoord")
    ob = tc.outputs["Object"]
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
    base2 = b.mix(b.m("MULTIPLY", cloud.outputs["Fac"], 0.35), base, (0.80, 0.79, 0.76))
    veincol = b.mix(b.m("GREATER_THAN", nz.outputs["Fac"], 0.55), vein, gold)
    col = b.mix(b.m("SUBTRACT", 1.0, vf), base2, veincol)
    p = b.principled(Base_Color=col, Roughness=0.16)
    b.put(p.inputs["Coat Weight"], 0.25)
    b.put(p.inputs["Coat Roughness"], 0.06)
    b.put(p.inputs["Subsurface Weight"], 0.08)
    bev = b.n("ShaderNodeBevel", {"Radius": 0.003})
    b.put(p.inputs["Normal"], bev.outputs[0])
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def travertine_mat():
    m, nt, b, out = _mat("travertine")
    tc = b.n("ShaderNodeTexCoord")
    ob = tc.outputs["Object"]
    wv = b.n("ShaderNodeTexWave", wave_type="BANDS", bands_direction="Z")
    b.put(wv.inputs["Vector"], ob)
    wv.inputs["Scale"].default_value = 6.0
    wv.inputs["Distortion"].default_value = 3.0
    wv.inputs["Detail"].default_value = 6.0
    col = b.ramp(wv.outputs["Fac"], [(0.2, (0.66, 0.57, 0.45)), (0.5, (0.78, 0.71, 0.60)), (0.85, (0.72, 0.64, 0.52))])
    vo = b.n("ShaderNodeTexVoronoi", feature="F1")
    b.put(vo.inputs["Vector"], ob)
    vo.inputs["Scale"].default_value = 60.0
    nz = b.noise(ob, 30.0, 4.0, 0.6)
    pit = b.m("MULTIPLY", b.m("LESS_THAN", vo.outputs["Distance"], 0.12), b.m("GREATER_THAN", nz.outputs["Fac"], 0.55))
    col = b.mix(b.m("MULTIPLY", pit, 0.7), col, (0.42, 0.35, 0.26))
    p = b.principled(Base_Color=col, Roughness=0.42)
    bev = b.n("ShaderNodeBevel", {"Radius": 0.004})
    b.put(p.inputs["Normal"], b.bump(b.m("SUBTRACT", 1.0, pit), 0.25, 0.2, bev.outputs[0]))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def fabric_mat(name, color, kind="boucle", color2=None):
    m, nt, b, out = _mat(name)
    tc = b.n("ShaderNodeTexCoord")
    ob = tc.outputs["Object"]
    if kind == "boucle":
        vo = b.n("ShaderNodeTexVoronoi", feature="SMOOTH_F1")
        b.put(vo.inputs["Vector"], ob)
        vo.inputs["Scale"].default_value = 520.0
        nz = b.noise(ob, 180.0, 4.0, 0.6)
        h = b.m("ADD", vo.outputs["Distance"], b.m("MULTIPLY", nz.outputs["Fac"], 0.6))
        strength = 0.55
    else:  # linen: a plain weave
        x, y, z = b.sep(ob)
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


def leather_mat(name, color):
    m, nt, b, out = _mat(name)
    tc = b.n("ShaderNodeTexCoord")
    ob = tc.outputs["Object"]
    vo = b.n("ShaderNodeTexVoronoi", feature="F1")
    b.put(vo.inputs["Vector"], ob)
    vo.inputs["Scale"].default_value = 260.0
    cn = b.noise(ob, 4.0, 5.0, 0.6)
    col = b.mix(b.m("MULTIPLY", cn.outputs["Fac"], 0.5), color, tuple(min(1, c * 1.35) for c in color))
    p = b.principled(Base_Color=col, Roughness=b.m("ADD", 0.34, b.m("MULTIPLY", cn.outputs["Fac"], 0.2)))
    b.put(p.inputs["Coat Weight"], 0.15)
    b.put(p.inputs["Normal"], b.bump(vo.outputs["Distance"], 0.12, 0.05))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def wall_mat(name="wall", color=(0.80, 0.78, 0.74)):
    m, nt, b, out = _mat(name)
    tc = b.n("ShaderNodeTexCoord")
    nz = b.noise(tc.outputs["Object"], 2.0, 5.0, 0.6)
    col = b.mix(b.m("MULTIPLY", nz.outputs["Fac"], 0.12), color, tuple(c * 0.95 for c in color))
    p = b.principled(Base_Color=col, Roughness=0.88)
    b.put(p.inputs["Specular IOR Level"], 0.3)
    fine = b.noise(tc.outputs["Object"], 90.0, 3.0, 0.6)
    b.put(p.inputs["Normal"], b.bump(fine.outputs["Fac"], 0.015, 0.1))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def rug_mat():
    m, nt, b, out = _mat("rug")
    tc = b.n("ShaderNodeTexCoord")
    ob = tc.outputs["Object"]
    nz = b.noise(ob, 700.0, 3.0, 0.7)
    cn = b.noise(ob, 3.0, 5.0, 0.6)
    x, y, z = b.sep(ob)
    # a quiet border, a hand-knotted wool look
    bx = b.m("GREATER_THAN", b.m("ABSOLUTE", x), 1.62)
    by = b.m("GREATER_THAN", b.m("ABSOLUTE", y), 1.22)
    border = b.m("MAXIMUM", bx, by)
    col = b.mix(b.m("MULTIPLY", cn.outputs["Fac"], 0.4), (0.74, 0.70, 0.62), (0.66, 0.62, 0.55))
    col = b.mix(b.m("MULTIPLY", border, 0.8), col, (0.52, 0.47, 0.40))
    p = b.principled(Base_Color=col, Roughness=1.0)
    b.put(p.inputs["Sheen Weight"], 1.0)
    b.put(p.inputs["Sheen Roughness"], 0.6)
    b.put(p.inputs["Specular IOR Level"], 0.2)
    b.put(p.inputs["Normal"], b.bump(nz.outputs["Fac"], 0.7, 0.05))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def glass_interior():
    """the curtain wall's glass, from inside: a clear sheet with a Fresnel reflection, transparent to shadow rays (the sun
    and the sky light the room without caustic noise)"""
    m, nt, b, out = _mat("apt_glass")
    lp = b.n("ShaderNodeLightPath")
    tint = (0.92, 0.95, 0.94)
    tr = b.n("ShaderNodeBsdfTransparent", {"Color": tint})
    trc = b.n("ShaderNodeBsdfTransparent", {"Color": tuple(c * PULL for c in tint)})
    gl = b.n("ShaderNodeBsdfGlossy", {"Roughness": 0.0})
    lw = b.n("ShaderNodeLayerWeight", {"Blend": 0.12})
    fr = b.m("ADD", lw.outputs["Fresnel"], 0.04)
    s_other = b.mixs(fr, tr.outputs[0], gl.outputs[0])
    s_cam = b.mixs(fr, trc.outputs[0], gl.outputs[0])
    s = b.mixs(lp.outputs["Is Camera Ray"], s_other, s_cam)
    s = b.mixs(lp.outputs["Is Shadow Ray"], s, tr.outputs[0])
    nt.links.new(s, out.inputs["Surface"])
    # the balcony's railing glass: no pull (the view behind it would darken twice)
    m2, nt2, b2, out2 = _mat("rail_glass")
    lp2 = b2.n("ShaderNodeLightPath")
    tr2 = b2.n("ShaderNodeBsdfTransparent", {"Color": tint})
    gl2 = b2.n("ShaderNodeBsdfGlossy", {"Roughness": 0.0})
    lw2 = b2.n("ShaderNodeLayerWeight", {"Blend": 0.1})
    s2 = b2.mixs(lw2.outputs["Fresnel"], tr2.outputs[0], gl2.outputs[0])
    s2 = b2.mixs(lp2.outputs["Is Shadow Ray"], s2, tr2.outputs[0])
    nt2.links.new(s2, out2.inputs["Surface"])
    return m


def sheer_mat():
    m, nt, b, out = _mat("sheer")
    tc = b.n("ShaderNodeTexCoord")
    nz = b.noise(tc.outputs["Object"], 300.0, 3.0, 0.6)
    tr = b.n("ShaderNodeBsdfTransparent", {"Color": (1, 1, 1)})
    tl = b.n("ShaderNodeBsdfTranslucent", {"Color": (0.93, 0.90, 0.84)})
    df = b.n("ShaderNodeBsdfDiffuse", {"Color": (0.90, 0.87, 0.81)})
    s = b.mixs(0.35, tl.outputs[0], df.outputs[0])
    s = b.mixs(b.m("ADD", 0.42, b.m("MULTIPLY", nz.outputs["Fac"], 0.12)), s, tr.outputs[0])
    nt.links.new(s, out.inputs["Surface"])
    return m


def emit_mat(name, color, strength):
    m, nt, b, out = _mat(name)
    e = b.n("ShaderNodeEmission", {"Color": color, "Strength": strength})
    nt.links.new(e.outputs[0], out.inputs["Surface"])
    return m


def art_mat():
    """an abstract canvas in warm earth tones (an illustration)"""
    m, nt, b, out = _mat("art")
    tc = b.n("ShaderNodeTexCoord")
    ob = tc.outputs["Object"]
    nz = b.noise(ob, 1.3, 2.0, 0.5)
    col = b.ramp(nz.outputs["Fac"], [(0.30, (0.78, 0.72, 0.62)), (0.45, (0.62, 0.36, 0.22)), (0.55, (0.80, 0.74, 0.64)),
                                      (0.66, (0.28, 0.33, 0.29)), (0.74, (0.84, 0.79, 0.70))], "CONSTANT")
    fine = b.noise(ob, 140.0, 4.0, 0.6)
    p = b.principled(Base_Color=col, Roughness=0.8)
    b.put(p.inputs["Normal"], b.bump(fine.outputs["Fac"], 0.2, 0.05))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def leaf_mat():
    m, nt, b, out = _mat("leaf")
    geo = b.n("ShaderNodeNewGeometry")
    pr = b.attr("lrand").outputs["Fac"]
    front = b.mix(pr, (0.10, 0.13, 0.07), (0.17, 0.20, 0.11))
    back = (0.36, 0.40, 0.32)
    col = b.mix(geo.outputs["Backfacing"], front, back)
    p = b.principled(Base_Color=col, Roughness=0.45)
    b.put(p.inputs["Specular IOR Level"], 0.45)
    tr = b.n("ShaderNodeBsdfTranslucent", {"Color": (0.20, 0.26, 0.08)})
    s = b.mixs(0.22, p.outputs[0], tr.outputs[0])
    nt.links.new(s, out.inputs["Surface"])
    return m


def tile_mat():
    """large-format outdoor porcelain (warm grey stone look) with 3 mm joints, 60 x 120 cm"""
    m, nt, b, out = _mat("balcony_tile")
    tc = b.n("ShaderNodeTexCoord")
    ob = tc.outputs["Object"]
    x, y, z = b.sep(ob)
    fx = b.m("FRACT", b.m("DIVIDE", x, 1.2))
    fy = b.m("FRACT", b.m("DIVIDE", y, 0.6))
    j = b.m("MAXIMUM", b.m("LESS_THAN", fx, 0.0025), b.m("LESS_THAN", fy, 0.005))
    cell = b.combine(b.m("FLOOR", b.m("DIVIDE", x, 1.2)), b.m("FLOOR", b.m("DIVIDE", y, 0.6)), 0.0)
    rw = b.white(cell)
    nz = b.noise(ob, 9.0, 6.0, 0.6)
    col = b.mix(b.m("MULTIPLY", nz.outputs["Fac"], 0.5), (0.56, 0.53, 0.49), (0.66, 0.63, 0.58))
    col = b.mix(b.m("MULTIPLY", rw, 0.3), col, (0.60, 0.57, 0.52))
    col = b.mix(j, col, (0.30, 0.29, 0.27))
    p = b.principled(Base_Color=col, Roughness=0.6)
    b.put(p.inputs["Normal"], b.bump(b.m("SUBTRACT", 1.0, j), 0.2, 0.05))
    nt.links.new(p.outputs[0], out.inputs["Surface"])
    return m


def make_materials():
    oak_floor_mat()
    wall_mat()
    wall_mat("ceiling", (0.84, 0.83, 0.80))
    principled_mat("skirting", (0.80, 0.78, 0.74), 0.5)
    principled_mat("shadowgap", (0.05, 0.05, 0.05), 0.8)
    principled_mat("alu_white", (0.83, 0.83, 0.82), 0.30, spec=0.6)
    glass_interior()
    marble_mat()
    travertine_mat()
    fabric_mat("boucle", (0.79, 0.75, 0.67), "boucle")
    fabric_mat("linen_taupe", (0.56, 0.51, 0.45), "linen")
    fabric_mat("linen_rust", (0.52, 0.27, 0.15), "linen")
    fabric_mat("linen_clay", (0.50, 0.33, 0.24), "linen")
    fabric_mat("linen_sage", (0.45, 0.48, 0.40), "linen")
    fabric_mat("linen_cream", (0.84, 0.81, 0.75), "linen")
    fabric_mat("linen_sand", (0.70, 0.64, 0.55), "linen")
    fabric_mat("headboard", (0.66, 0.60, 0.52), "boucle")
    leather_mat("leather", (0.30, 0.14, 0.06))
    wood_mat("walnut", (0.13, 0.075, 0.045), (0.25, 0.15, 0.085), 22.0, 0.38)
    wood_mat("oak_veneer", (0.36, 0.23, 0.13), (0.50, 0.35, 0.21), 26.0, 0.42)
    wood_mat("oak_light", (0.48, 0.34, 0.20), (0.62, 0.47, 0.30), 20.0, 0.40)
    wood_mat("teak", (0.34, 0.21, 0.11), (0.46, 0.30, 0.17), 20.0, 0.55)
    principled_mat("brass", (0.80, 0.60, 0.34), 0.26, metal=1.0, aniso=0.5)
    principled_mat("blacksteel", (0.035, 0.035, 0.035), 0.38, metal=0.8)
    principled_mat("black_glass", (0.01, 0.01, 0.012), 0.05, spec=1.0, coat=0.5)
    principled_mat("ceramic_clay", (0.62, 0.50, 0.40), 0.75, bump=True, bump_scale=40.0, bump_strength=0.08)
    principled_mat("ceramic_white", (0.85, 0.84, 0.80), 0.25, coat=0.3)
    principled_mat("soil", (0.06, 0.045, 0.035), 1.0, bump=True, bump_scale=80.0, bump_strength=0.4)
    principled_mat("lemon", (0.78, 0.55, 0.05), 0.4, bump=True, bump_scale=220.0, bump_strength=0.15)
    principled_mat("paper_a", (0.70, 0.66, 0.58), 0.8)
    principled_mat("paper_b", (0.30, 0.34, 0.33), 0.7)
    principled_mat("paper_c", (0.55, 0.30, 0.20), 0.7)
    principled_mat("paper_d", (0.85, 0.83, 0.78), 0.7)
    principled_mat("door_paint", (0.79, 0.77, 0.73), 0.55)
    principled_mat("duvet", (0.90, 0.89, 0.86), 0.9, sheen=0.6, bump=True, bump_scale=120.0, bump_strength=0.05)
    principled_mat("vrf", (0.10, 0.10, 0.10), 0.7)
    principled_mat("downlight_rim", (0.06, 0.06, 0.06), 0.4)
    principled_mat("stone_planter", (0.52, 0.49, 0.45), 0.85, bump=True, bump_scale=30.0, bump_strength=0.15)
    rug_mat()
    sheer_mat()
    art_mat()
    leaf_mat()
    tile_mat()
    principled_mat("bark", (0.22, 0.19, 0.15), 0.9, bump=True, bump_scale=60.0, bump_strength=0.5)
    emit_mat("lamp_warm", (1.0, 0.72, 0.45), 6.0 if NIGHT else (2.0 if DUSK else 0.0))
    emit_mat("cove", (1.0, 0.75, 0.50), 5.0 if NIGHT else 0.0)
    emit_mat("downlight_emit", (1.0, 0.80, 0.60), 3.5 if NIGHT else (3.0 if DUSK else 0.0))


# ============================================================================================ geometry helpers
def obj(name, verts, faces, mat, smooth=False, mods=()):
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
    own(ob)
    return ob


def bevel(ob, width, segs=3, harden=True):
    b = ob.modifiers.new("bevel", "BEVEL")
    b.width = width
    b.segments = segs
    b.limit_method = "ANGLE"
    b.angle_limit = 50 * DEG
    b.harden_normals = False
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def subsurf(ob, lv=2):
    s = ob.modifiers.new("sub", "SUBSURF")
    s.levels = lv
    s.render_levels = lv
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def displace(ob, strength=0.01, scale=0.25):
    tex = bpy.data.textures.new("n_" + ob.name, "CLOUDS")
    tex.noise_scale = scale
    d = ob.modifiers.new("disp", "DISPLACE")
    d.texture = tex
    d.strength = strength
    d.texture_coords = "OBJECT" if False else "LOCAL"
    return ob


def box(name, cx, cy, z0, sx, sy, sz, mat, rot=0.0, bev=0.0, segs=3, sub=0):
    """an axis box in the apartment frame: centre (cx, cy) in (s, y = -d), from z0 up sz; rot about Z (degrees)"""
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


def sbox(name, s0, s1, d0, d1, z0, z1, mat, bev=0.0, segs=3):
    """a box by its (s, d) extents"""
    return box(name, (s0 + s1) / 2, -(d0 + d1) / 2, z0, abs(s1 - s0), abs(d1 - d0), z1 - z0, mat, 0.0, bev, segs)


def cyl(name, cx, cy, z0, z1, r, mat, seg=48, bev=0.0, r_top=None):
    rt = r if r_top is None else r_top
    V = [(cx + r * math.cos(2 * math.pi * k / seg), cy + r * math.sin(2 * math.pi * k / seg), z0) for k in range(seg)]
    V += [(cx + rt * math.cos(2 * math.pi * k / seg), cy + rt * math.sin(2 * math.pi * k / seg), z1) for k in range(seg)]
    F = [tuple(range(seg))[::-1], tuple(range(seg, 2 * seg))] + [(k, (k + 1) % seg, seg + (k + 1) % seg, seg + k) for k in range(seg)]
    ob = obj(name, V, F, mat, smooth=True)
    if bev:
        bevel(ob, bev, 3)
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
    me.materials.append(M[mat])
    for p in me.polygons:
        p.use_smooth = True
    return own(ob)


def tube(name, pts, r, mat, seg=10):
    """a round rod along a polyline (apartment frame)"""
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


def flip_down(me, closed=False):
    """the (s, d) -> (s, y = -d) mirror turns polygons over: make every face point out"""
    bm = bmesh.new()
    bm.from_mesh(me)
    if closed:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    else:
        bm.normal_update()
        bmesh.ops.reverse_faces(bm, faces=[f for f in bm.faces if f.normal.z < -0.5])
    bm.to_mesh(me)
    bm.free()


def poly_prism(name, poly, z0, z1, mat, flip=False):
    """a prism over a polygon in (s, d)"""
    n = len(poly)
    V = [(s, -d, z0) for (s, d) in poly] + [(s, -d, z1) for (s, d) in poly]
    F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(k, (k + 1) % n, n + (k + 1) % n, n + k) for k in range(n)]
    ob = obj(name, V, F, mat)
    flip_down(ob.data, closed=True)
    return ob


def inside(poly, s, d):
    c = False
    j = len(poly) - 1
    for i in range(len(poly)):
        (xi, yi), (xj, yj) = poly[i], poly[j]
        if (yi > d) != (yj > d) and s < (xj - xi) * (d - yi) / (yj - yi + 1e-12) + xi:
            c = not c
        j = i
    return c


# ============================================================================================ the shell
def glass_points():
    """the glass line of the apartment's quarter (plate-local polyline, as world.js draws it) in (s, d)"""
    go = KW.plate_outline(AG, NEXP, 720)
    pts = []
    for (u, v) in go:
        phi = math.degrees(math.atan2(v, u)) % 360
        dphi = ((phi - PHI_C + 180) % 360) - 180
        if abs(dphi) <= 45.0:
            # plate (u, v) -> (s, d)
            s = u * RIGHTL[0] + v * RIGHTL[1]
            k = u * OUTL[0] + v * OUTL[1]
            pts.append((dphi, s, AG - k))
    pts.sort()
    return [(s, d) for (_, s, d) in pts]


def fin_positions():
    """the fins' places (world.js: one every 1.5 m of the glass line, counted from the plate's axis), as (s, d, ts, td)"""
    go = KW.plate_outline(AG, NEXP, 144)
    Mn = len(go)
    glen = [0.0]
    for k in range(1, Mn + 1):
        glen.append(glen[-1] + math.dist(go[k - 1], go[k % Mn]))
    per = glen[-1]
    nfin = int(per / 1.5)
    out = []
    for q in range(nfin):
        sq = (q + 0.5) * per / nfin
        k = next((kk for kk in range(Mn) if glen[kk + 1] >= sq), Mn - 1)
        f = (sq - glen[k]) / max(1e-6, glen[k + 1] - glen[k])
        a, b2 = go[k], go[(k + 1) % Mn]
        u, v = a[0] + (b2[0] - a[0]) * f, a[1] + (b2[1] - a[1]) * f
        phi = math.degrees(math.atan2(v, u)) % 360
        if abs(((phi - PHI_C + 180) % 360) - 180) > 45:
            continue
        tu, tv = b2[0] - a[0], b2[1] - a[1]
        s = u * RIGHTL[0] + v * RIGHTL[1]
        d = AG - (u * OUTL[0] + v * OUTL[1])
        ts = tu * RIGHTL[0] + tv * RIGHTL[1]
        td = -(tu * OUTL[0] + tv * OUTL[1])
        tl = math.hypot(ts, td)
        out.append((s, d, ts / tl, td / tl))
    out.sort()
    return out


GL = glass_points()
FINS = fin_positions()
SC = 45 * DEG
DIAG_S = AG * math.sin(SC) / (math.sin(SC) ** NEXP + math.cos(SC) ** NEXP) ** (1 / NEXP) if False else GL[-1][0]


def core_d(s):
    return AG - math.sqrt(max(0.0, CORE_R ** 2 - s * s))


def apartment_polygon():
    """the quarter: the glass, the two party walls on the diagonals, the core's lobby ring"""
    poly = list(GL)
    sR, dR = GL[-1]
    sL, dL = GL[0]
    ce = CORE_R * math.sqrt(0.5)
    poly.append((ce, AG - ce))
    for k in range(1, 30):
        a = 45 - 90 * k / 30
        poly.append((CORE_R * math.sin(a * DEG), AG - CORE_R * math.cos(a * DEG)))
    poly.append((-ce, AG - ce))
    return poly


APOLY = apartment_polygon()
BACK_D = 7.40                   # the great room's back wall (kitchen)
PART_R = 4.72                   # the partition to the master bedroom
PART_L = -5.00                  # the partition to the second bedroom
BED_BACK = 5.20                 # the master bedroom's back wall (the dressing room and bath behind)


def shell():
    # the floor's base (a plain oak border shows at the walls) and the ceiling
    poly_prism("floor_base", APOLY, -0.02, -0.001, "oak_floor")
    fb = bpy.data.objects["floor_base"]
    me = fb.data
    uvl = me.uv_layers.new(name="grain")
    for li in range(len(me.loops)):
        co = me.vertices[me.loops[li].vertex_index].co
        uvl.data[li].uv = (co.x, co.y)
    me.attributes.new("prand", "FLOAT", "FACE")
    ceil = poly_prism("ceiling", APOLY, CEIL, CEIL + 0.05, "ceiling")
    # party walls along the diagonals and the core wall (outside the quarter)
    sR, dR = GL[-1]
    sL, dL = GL[0]
    ce = CORE_R * math.sqrt(0.5)
    for nm, (a, b2) in (("party_R", ((sR, dR), (ce, AG - ce))), ("party_L", ((sL, dL), (-ce, AG - ce)))):
        (s0, d0), (s1, d1) = a, b2
        L_ = math.hypot(s1 - s0, d1 - d0)
        ns, nd = (d1 - d0) / L_, -(s1 - s0) / L_
        if (ns * (0 - s0) + nd * (4 - d0)) > 0:
            ns, nd = -ns, -nd
        t = 0.25
        poly = [(s0, d0), (s1, d1), (s1 + ns * t, d1 + nd * t), (s0 + ns * t, d0 + nd * t)]
        poly_prism(nm, poly, -0.05, TOPG, "wall")
    arc_in = [(CORE_R * math.sin(a * DEG), AG - CORE_R * math.cos(a * DEG)) for a in range(-46, 47, 2)]
    arc_out = [((CORE_R - 0.3) * math.sin(a * DEG), AG - (CORE_R - 0.3) * math.cos(a * DEG)) for a in range(46, -47, -2)]
    poly_prism("core_wall", arc_in + arc_out, -0.05, TOPG, "wall")


def wall_seg(name, s0, d0, s1, d1, z0=0.0, z1=None, t=0.12, mat="wall", openings=()):
    """a straight partition from (s0, d0) to (s1, d1); openings are (from, to, head) in metres along it"""
    z1 = CEIL if z1 is None else z1
    Ltot = math.hypot(s1 - s0, d1 - d0)
    us, ud = (s1 - s0) / Ltot, (d1 - d0) / Ltot
    cuts = [0.0]
    for (a, b2, head) in sorted(openings):
        cuts += [a, b2]
    cuts.append(Ltot)
    ops = sorted(openings)
    pieces = [(cuts[i], cuts[i + 1], None) for i in range(0, len(cuts), 2)]
    for (a, b2, head) in ops:
        pieces.append((a, b2, head))
    for i, (a, b2, head) in enumerate(pieces):
        if b2 - a < 0.005:
            continue
        cs, cd = s0 + us * (a + b2) / 2, d0 + ud * (a + b2) / 2
        rot = math.degrees(math.atan2(-ud, us))
        if head is None:
            box("%s_%d" % (name, i), cs, -cd, z0, b2 - a, t, z1 - z0, mat, rot)
        else:
            box("%s_%dh" % (name, i), cs, -cd, head, b2 - a, t, z1 - head, mat, rot)


def door(name, s, d, rot, w=0.92, h=2.45):
    """a flush door (painted) in a 3 mm shadow-gap frame, with a black lever"""
    c, sn = math.cos(rot * DEG), math.sin(rot * DEG)
    box(name + "_gap", s, -d, 0.0, w + 0.012, 0.128, h + 0.006, "shadowgap", rot)
    box(name + "_leaf", s, -d, 0.004, w, 0.132, h - 0.002, "door_paint", rot, bev=0.002)
    for side in (-1, 1):
        hx, hy = s + c * (w / 2 - 0.09) - sn * side * 0.08, -d + sn * (w / 2 - 0.09) + c * side * 0.08
        box(name + "_lev%d" % side, hx - c * 0.06, hy - sn * 0.06, 1.02, 0.13, 0.018, 0.018, "blacksteel", rot, bev=0.004)


def partitions():
    # the partition to the master bedroom (s = 4.72), a door near the back
    dg = d_glass(PART_R)
    wall_seg("part_R", PART_R, dg + 0.02, PART_R, BACK_D, openings=((5.55 - dg, 6.47 - dg, 2.45),))
    door("door_master", PART_R, 6.01, 90)
    dgl = d_glass(PART_L)
    wall_seg("part_L", PART_L, dgl + 0.02, PART_L, BACK_D, openings=((5.4 - dgl, 6.32 - dgl, 2.45),))
    door("door_b2", PART_L, 5.86, 90)
    # the great room's back wall: an opening to the entrance hall, the kitchen run
    wall_seg("back", PART_L, BACK_D, PART_R, BACK_D, t=0.14, openings=((0.44, 1.36, 2.45),))
    door("door_hall", PART_L + 0.9, BACK_D, 0)
    # the master bedroom's back wall: a door to the dressing room and bath
    wall_seg("bed_back", PART_R, BED_BACK, AG - BED_BACK, BED_BACK, openings=((0.5, 1.4, 2.45),))
    door("door_dress", PART_R + 0.95, BED_BACK, 0)
    # skirting: 7 cm, white, with a shadow line
    for (s0, d0, s1, d1) in ((PART_L + 0.07, 0.15, PART_L + 0.07, BACK_D - 0.08), (PART_R - 0.07, 0.15, PART_R - 0.07, 5.5)):
        sbox("skirt", s0 - 0.006, s0 + 0.006, d0, d1, 0.0, 0.07, "skirting")


def curtain_wall():
    """the glass, the white aluminium mullions inside (at the fins' places), the fins outside, a low sill, the curtain
    pocket in the ceiling; a full-height pivot window with its inner railing (Alum Eshet) left of the balcony door"""
    top = TOPG
    V, F = [], []
    for i in range(len(GL) - 1):
        (s0, d0), (s1, d1) = GL[i], GL[i + 1]
        b0 = len(V)
        V += [(s0, -d0, -0.02), (s1, -d1, -0.02), (s1, -d1, top), (s0, -d0, top)]
        F.append((b0, b0 + 1, b0 + 2, b0 + 3))
    obj("glass", V, F, "apt_glass")
    for q, (s, d, ts, td) in enumerate(FINS):
        rot = math.degrees(math.atan2(-td, ts))
        ns, nd = td, -ts          # the inward normal (toward +d)
        if nd < 0:
            ns, nd = -ns, -nd
        # the mullion inside: 60 mm wide, 140 mm deep
        box("mull%d" % q, s + ns * 0.075, -(d + nd * 0.075), -0.02, 0.06, 0.14, top + 0.02, "alu_white", rot)
        # the fin outside: 50 mm thick, 300 mm deep (not in front of the balcony)
        if abs(s) > BAL + 0.1:
            box("fin%d" % q, s - ns * 0.16, -(d - nd * 0.16), -0.02, 0.05, 0.30, top + 0.02, "alu_white", rot)
    # the sill profile along the glass, inside
    V, F = [], []
    for i in range(len(GL) - 1):
        (s0, d0), (s1, d1) = GL[i], GL[i + 1]
        b0 = len(V)
        V += [(s0, -(d0 + 0.005), 0.0), (s1, -(d1 + 0.005), 0.0), (s1, -(d1 + 0.005), 0.05), (s0, -(d0 + 0.005), 0.05)]
        F.append((b0, b0 + 1, b0 + 2, b0 + 3))
    obj("sill", V, F, "alu_white")
    # the curtain pocket: a 14 cm slot in the ceiling along the glass, dark inside, the LED cove on its back edge
    V, F, V2, F2 = [], [], [], []
    for i in range(len(GL) - 1):
        (s0, d0), (s1, d1) = GL[i], GL[i + 1]
        b0 = len(V)
        V += [(s0, -(d0 + 0.02), CEIL - 0.001), (s1, -(d1 + 0.02), CEIL - 0.001), (s1, -(d1 + 0.16), CEIL - 0.001), (s0, -(d0 + 0.16), CEIL - 0.001)]
        F.append((b0, b0 + 1, b0 + 2, b0 + 3))
        b1 = len(V2)
        V2 += [(s0, -(d0 + 0.15), CEIL - 0.004), (s1, -(d1 + 0.15), CEIL - 0.004), (s1, -(d1 + 0.155), CEIL - 0.004), (s0, -(d0 + 0.155), CEIL - 0.004)]
        F2.append((b1, b1 + 1, b1 + 2, b1 + 3))
    obj("pocket", V, F, "shadowgap")
    if NIGHT:
        obj("cove", V2, F2, "cove")
    # the balcony door: the module left of the axis gets a door frame and a pull; the one beyond it an inner railing
    mods = [f for f in FINS if abs(f[0]) < BAL]
    if len(mods) >= 3:
        s_door = (mods[len(mods) // 2 - 1][0] + mods[len(mods) // 2][0]) / 2
        mr = min((f for f in FINS if f[0] > s_door), key=lambda f: f[0] - s_door)
        box("door_pull", mr[0] - 0.13, -(0.11), 0.95, 0.022, 0.03, 0.34, "brass", 0, bev=0.008)
    pv = [f for f in FINS if -BAL - 2.0 < f[0] < -BAL]
    rail_s = (-BAL - 1.45, -BAL - 0.05)
    tube("inner_rail", [(rail_s[0], -0.20, 1.0), (rail_s[1], -0.20, 1.0)], 0.02, "alu_white")
    for sx in rail_s:
        box("inner_rail_post", sx, -0.16, 0.95, 0.03, 0.08, 0.1, "alu_white")
    tube("inner_rail_b", [(6.6, -(d_glass(6.6) + 0.2), 1.0), (8.05, -(d_glass(8.05) + 0.2), 1.0)], 0.02, "alu_white")


def balcony():
    """the balcony: 8.8 m of the slab's 1.25 m edge, a glass railing (1.1 m) with a slim white top rail, returns at both
    ends, porcelain on the slab"""
    edge = []
    for a in range(-40, 41):
        s = BAL * a / 40
        # the slab's edge: the superellipse at the slab's half size, in local d (negative = outside the glass)
        x = min(1.0, abs(s) / HALF)
        dd = AG - HALF * (1 - x ** NEXP) ** (1 / NEXP)
        edge.append((s, dd))
    glass_line = [(s, d_glass(s)) for (s, _) in edge]
    poly = [(s, d + 0.03) for (s, d) in glass_line] + [(s, d) for (s, d) in edge[::-1]]
    ob = poly_prism("bal_tiles", poly, -0.02, -0.005, "balcony_tile")
    # the railing
    V, F = [], []
    for i in range(len(edge) - 1):
        (s0, d0), (s1, d1) = edge[i], edge[i + 1]
        b0 = len(V)
        V += [(s0, -(d0 + 0.06), 0.0), (s1, -(d1 + 0.06), 0.0), (s1, -(d1 + 0.06), 1.08), (s0, -(d0 + 0.06), 1.08)]
        F.append((b0, b0 + 1, b0 + 2, b0 + 3))
    for sgn in (-1, 1):
        s = sgn * BAL
        de, dg = edge[0 if sgn < 0 else -1][1], d_glass(s)
        b0 = len(V)
        V += [(s, -(de + 0.06), 0.0), (s, -(dg - 0.02), 0.0), (s, -(dg - 0.02), 1.08), (s, -(de + 0.06), 1.08)]
        F.append((b0, b0 + 1, b0 + 2, b0 + 3))
    obj("bal_glass", V, F, "rail_glass")
    tube("bal_toprail", [(s, -(d + 0.06), 1.1) for (s, d) in edge], 0.022, "alu_white", 8)
    for sgn in (-1, 1):
        s = sgn * BAL
        tube("bal_toprail_ret%d" % sgn, [(s, -(edge[0 if sgn < 0 else -1][1] + 0.06), 1.1), (s, -(d_glass(s) - 0.03), 1.1)], 0.022, "alu_white", 8)
    # the base channel of the glass railing
    tube("bal_shoe", [(s, -(d + 0.06), 0.025) for (s, d) in edge], 0.03, "alu_white", 6)


# ============================================================================================ the herringbone floor
def herringbone(room_poly, name, inset=0.11, Lp=0.60, Wp=0.10, angle=0.0):
    """oak planks 60 x 10 cm in a herringbone whose zigzag runs toward the view; a plain border at the walls"""
    V, F, UV, PR = [], [], [], []
    r2 = 1 / math.sqrt(2)
    ca, sa = math.cos(angle * DEG), math.sin(angle * DEG)
    xs = [p[0] for p in room_poly]
    ds = [p[1] for p in room_poly]
    smin, smax, dmin, dmax = min(xs) - 1, max(xs) + 1, min(ds) - 1, max(ds) + 1

    def ok(s, d):
        if not inside(room_poly, s, d):
            return False
        for k in range(len(room_poly)):
            (x0, y0), (x1, y1) = room_poly[k], room_poly[(k + 1) % len(room_poly)]
            ex, ey = x1 - x0, y1 - y0
            L2 = ex * ex + ey * ey
            t = max(0, min(1, ((s - x0) * ex + (d - y0) * ey) / L2)) if L2 else 0
            if math.hypot(s - x0 - t * ex, d - y0 - t * ey) < inset:
                return False
        return True

    gap = 0.0012
    for k in range(-14, 22):
        for n in range(-20, 95):
            for kind in (0, 1):
                a0 = k * Lp + n * Wp
                b0 = -k * Lp + n * Wp
                if kind == 0:
                    rect = (a0, b0, Lp, Wp)
                else:
                    rect = (a0, b0 + Wp, Wp, Lp)
                ra, rb, rw, rh = rect
                corners = [(ra + gap, rb + gap), (ra + rw - gap, rb + gap), (ra + rw - gap, rb + rh - gap), (ra + gap, rb + rh - gap)]
                sd = []
                for (a_, b_) in corners:
                    s = (a_ - b_) * r2
                    d = (a_ + b_) * r2
                    s, d = s * ca - d * sa, s * sa + d * ca
                    sd.append((s, d))
                cs = sum(p[0] for p in sd) / 4
                cd = sum(p[1] for p in sd) / 4
                if cs < smin or cs > smax or cd < dmin or cd > dmax:
                    continue
                if not all(ok(s, d) for (s, d) in sd):
                    continue
                pr = rnd.random()
                b0i = len(V)
                zt = 0.0
                for (s, d) in sd:
                    V.append((s, -d, zt))
                for (s, d) in sd:
                    V.append((s, -d, zt - 0.012))
                F.append((b0i, b0i + 1, b0i + 2, b0i + 3))
                for fc in ((0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)):
                    F.append(tuple(b0i + c for c in fc))
                off = rnd.random() * 5
                if kind == 0:
                    uvq = [(off, 0), (off + Lp, 0), (off + Lp, Wp), (off, Wp)]
                else:
                    uvq = [(off, Wp), (off, 0), (off + Lp, 0), (off + Lp, Wp)]
                UV.append(uvq)
                for _ in range(4):
                    UV.append([(off, 0)] * 4)
                PR += [pr] * 5
    me = bpy.data.meshes.new(name)
    me.from_pydata(V, [], F)
    me.update()
    uvl = me.uv_layers.new(name="grain")
    for poly, uvq in zip(me.polygons, UV):
        for c, li in enumerate(poly.loop_indices):
            uvl.data[li].uv = uvq[c]
    at = me.attributes.new("prand", "FLOAT", "FACE")
    at.data.foreach_set("value", PR)
    flip_down(me)
    me.materials.append(M["oak_floor"])
    ob = bpy.data.objects.new(name, me)
    KW.link(ob)
    own(ob)
    print("herringbone %s: %d planks" % (name, len(PR) // 5))
    return ob


# ============================================================================================ furniture (illustration)
def cushion(name, cx, cy, z0, sx, sy, sz, mat, rot=0.0, puff=0.012, bev=0.04):
    """tailored upholstery: a box with rounded (5-segment) edges, finely subdivided, pushed out a little in the middle"""
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
    """a sewn cushion: two faces meeting at a seam all round, full in the middle (thickness t), standing w wide and h
    high, its faces toward local y; tilt leans its top back (+y) by degrees; rot turns it about Z like box()"""
    n = 16
    V, F = [], []
    idx = {}

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
    """the welt along a cushion's top edge: a thin cord following the rounded rectangle"""
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


def sofa(cx, cy, rot, length=3.3, depth=1.05, mat="boucle"):
    """a low, deep sofa: a recessed plinth, a seat of three cushions, a back of three, rounded arms"""
    c, s = math.cos(rot * DEG), math.sin(rot * DEG)

    def P(x, y):
        return cx + x * c - y * s, cy + x * s + y * c

    x, y = P(0, 0)
    box("sofa_plinth", x, y, 0.0, length - 0.2, depth - 0.2, 0.08, "shadowgap", rot, bev=0.01)
    x, y = P(0, 0.05)
    cushion("sofa_base", x, y, 0.08, length - 0.02, depth, 0.28, mat, rot, 0.003, 0.03)
    arm = 0.18
    for sgn in (-1, 1):
        x, y = P(sgn * (length / 2 - arm / 2), 0.05)
        cushion("sofa_arm", x, y, 0.08, arm, depth, 0.46, mat, rot, 0.003, 0.07)
        x, y = P(sgn * (length / 2 - arm / 2), 0.05)
        piping("sofa_arm_pipe", x, y, 0.535, arm, depth, rot, 0.0055, mat, 0.012, 0.06)
    # the upholstered back frame the loose cushions lean on (seen from the room, the sofa's back)
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
    # scatter pillows, leaning on the back cushions
    for i, (xo, mt, w, tl) in enumerate(((-1.12, "linen_rust", 0.52, 16), (-0.64, "linen_sage", 0.46, 12), (1.12, "linen_cream", 0.5, 14))):
        x, y = P(xo, 0.12)
        pillow("pillow%d" % i, x, y, 0.49, w, w * 0.9, 0.17, mt, rot + (-6 if xo < 0 else 5), tl, 0.5, 0.004)


def lounge_chair(cx, cy, rot):
    """a walnut frame with cognac leather cushions"""
    c, s = math.cos(rot * DEG), math.sin(rot * DEG)

    def P(x, y):
        return cx + x * c - y * s, cy + x * s + y * c

    for sx in (-0.36, 0.36):
        for sy in (-0.32, 0.30):
            x, y = P(sx, sy)
            box("lc_leg", x, y, 0.0, 0.04, 0.04, 0.34 if sy < 0 else 0.58, "walnut", rot, bev=0.01)
        x, y = P(sx, 0)
        box("lc_rail", x, y, 0.30, 0.045, 0.72, 0.045, "walnut", rot, bev=0.012)
        x, y = P(sx, -0.05)
        box("lc_armrest", x, y, 0.55, 0.06, 0.62, 0.035, "walnut", rot, bev=0.012)
    x, y = P(0, -0.05)
    cushion("lc_seat", x, y, 0.30, 0.66, 0.62, 0.12, "leather", rot, 0.006, 0.04)
    x, y = P(0, 0.30)
    ob = cushion("lc_back", x, y, 0.40, 0.66, 0.11, 0.46, "leather", rot, 0.006, 0.04)


def dining_chair(cx, cy, rot):
    c, s = math.cos(rot * DEG), math.sin(rot * DEG)

    def P(x, y):
        return cx + x * c - y * s, cy + x * s + y * c

    for sx in (-0.2, 0.2):
        for sy in (-0.2, 0.2):
            x, y = P(sx, sy)
            cyl("dc_leg", x, y, 0.0, 0.44, 0.017, "oak_light", 12, r_top=0.014)
    x, y = P(0, 0)
    cushion("dc_seat", x, y, 0.42, 0.48, 0.47, 0.07, "linen_taupe", rot, 0.004, 0.03)
    x, y = P(0, 0.215)
    pillow("dc_back", x, y, 0.52, 0.45, 0.30, 0.07, "linen_taupe", rot, 8.0, 0.25, 0.002)


def olive_tree(name, cs, cd, height=2.4, spread=0.9, seed=3, pot_r=0.32, pot_h=0.55, leaves=9000):
    """an olive tree in a stone planter: a gnarled trunk, branches, and narrow silver-green leaves (an illustration)"""
    r = random.Random(seed)
    cx, cy = cs, -cd
    cyl(name + "_pot", cx, cy, 0.0, pot_h, pot_r, "stone_planter", 48, bev=0.02, r_top=pot_r * 1.08)
    cyl(name + "_soil", cx, cy, pot_h - 0.06, pot_h - 0.04, pot_r * 1.02, "soil", 48)
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

    base = Vector((cx, cy, pot_h - 0.05))
    grow(base, Vector((0.05, 0.02, 1)).normalized(), height * 0.5, 0.055, 3)
    # leaves: narrow blades clustered on the twigs
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


def sheer(name, s0, s1, d_of, gather=2.2, height=None):
    """a linen sheer hanging from the curtain pocket, gathered in soft folds"""
    h = (height or CEIL) - 0.02
    n = max(12, int(abs(s1 - s0) * 90))
    V, F = [], []
    fw = 0.15
    for i in range(n + 1):
        s = s0 + (s1 - s0) * i / n
        d = d_of(s) + 0.09 + 0.035 * math.sin(i * 2 * math.pi * abs(s1 - s0) / (n * fw) * 1.0)
        for zz in (0.01, h):
            V.append((s, -d, zz))
    for i in range(n):
        F.append((2 * i, 2 * i + 2, 2 * i + 3, 2 * i + 1))
    ob = obj(name, V, F, "sheer", smooth=True)
    return ob


def pendant_linear(cs, cd, length=1.7, z=2.02):
    cy = -cd
    for k in (-0.6, 0.6):
        tube("pend_wire", [(cs, cy + k * length / 2, z + 0.03), (cs, cy + k * length / 2, CEIL)], 0.0015, "blacksteel", 6)
    box("pend_body", cs, cy, z, 0.07, length, 0.05, "brass", 0, bev=0.012)
    box("pend_diff", cs, cy, z - 0.004, 0.05, length - 0.04, 0.006, "lamp_warm", 0)


def kitchen():
    """a warm oak tall run on the back wall (a fridge, an oven, a coffee niche), a marble island with waterfall ends"""
    s0, s1 = 0.95, PART_R - 0.08
    dfront = BACK_D - 0.07 - 0.62
    n = 6
    w = (s1 - s0) / n
    for i in range(n):
        a = s0 + i * w
        sbox("tall_gap%d" % i, a, a + w, dfront + 0.004, BACK_D - 0.07, 0.0, 2.72, "shadowgap")
        sbox("tall%d" % i, a + 0.0015, a + w - 0.0015, dfront, dfront + 0.02, 0.09, 2.70, "oak_veneer", bev=0.0015)
    # the oven and the coffee niche (black glass), a lit shelf
    k = 3
    a = s0 + k * w
    sbox("oven", a + 0.03, a + w - 0.03, dfront - 0.001, dfront + 0.01, 0.82, 1.42, "black_glass")
    sbox("niche_back", a + 0.02, a + w - 0.02, dfront + 0.3, dfront + 0.31, 1.46, 1.98, "marble")
    sbox("niche_front_cut", a + 0.02, a + w - 0.02, dfront - 0.001, dfront + 0.3, 1.46, 1.98, "shadowgap")
    sbox("toe", s0, s1, dfront + 0.06, BACK_D - 0.07, 0.0, 0.09, "shadowgap")
    # the island
    i0, i1 = 1.25, 4.25
    ib0, ib1 = 4.72, 5.72
    sbox("island_body", i0 + 0.03, i1 - 0.03, ib0 + 0.25, ib1 - 0.02, 0.1, 0.88, "oak_veneer", bev=0.002)
    sbox("island_toe", i0 + 0.1, i1 - 0.1, ib0 + 0.3, ib1 - 0.08, 0.0, 0.1, "shadowgap")
    sbox("island_top", i0, i1, ib0, ib1, 0.88, 0.92, "marble", bev=0.004)
    for sx in (i0, i1 - 0.04):
        sbox("island_wf", sx, sx + 0.04, ib0, ib1, 0.0, 0.88, "marble", bev=0.003)
    # the tap (brass), a bowl of lemons, a board
    tube("tap", [(3.35, -(ib0 + 0.82), 0.92), (3.35, -(ib0 + 0.82), 1.26), (3.35, -(ib0 + 0.66), 1.30), (3.35, -(ib0 + 0.58), 1.22)], 0.012, "brass", 10)
    cyl("bowl", 2.05, -(ib0 + 0.42), 0.92, 1.0, 0.16, "ceramic_white", 40, r_top=0.19)
    for k in range(5):
        a_ = k * 1.2566
        sphere("lemon%d" % k, 2.05 + 0.07 * math.cos(a_), -(ib0 + 0.42) + 0.07 * math.sin(a_), 1.02 + 0.02 * (k % 2), 0.045, "lemon", 1.0, 1.0, 0.9)
    box("board", 2.75, -(ib0 + 0.35), 0.92, 0.42, 0.28, 0.025, "oak_light", 8, bev=0.006)
    # three stools on the living side
    for k, s in enumerate((1.75, 2.75, 3.75)):
        cyl("stool_seat%d" % k, s, -(ib0 - 0.28), 0.68, 0.74, 0.19, "leather", 40, bev=0.02)
        for a_ in range(4):
            an = a_ * math.pi / 2 + math.pi / 4
            tube("stool_leg", [(s + 0.15 * math.cos(an), -(ib0 - 0.28) + 0.15 * math.sin(an), 0.0), (s + 0.1 * math.cos(an), -(ib0 - 0.28) + 0.1 * math.sin(an), 0.68)], 0.011, "blacksteel", 8)
        tube("stool_ring", [(s + 0.13 * math.cos(t / 12 * 2 * math.pi), -(ib0 - 0.28) + 0.13 * math.sin(t / 12 * 2 * math.pi), 0.26) for t in range(13)], 0.008, "blacksteel", 6)


def living():
    """the living area (left, facing the view) and the dining (right)"""
    # rug and sofa, the coffee table, two chairs
    box("rug", -2.35, -2.05, 0.0, 3.6, 2.7, 0.012, "rug", 0, bev=0.004)
    sofa(-2.35, -2.95, 180, 3.3, 1.02)          # its back to the room, looking out
    cyl("coffee", -2.35, -1.62, 0.0, 0.32, 0.56, "travertine", 72, bev=0.012)
    cyl("coffee2", -1.5, -1.85, 0.0, 0.24, 0.28, "travertine", 48, bev=0.01)
    lounge_chair(-4.3, -1.55, 75)
    lounge_chair(-0.45, -1.45, -75)
    # a stack of books and a bowl on the coffee table
    for k, (mt, h) in enumerate((("paper_a", 0.035), ("paper_b", 0.028), ("paper_d", 0.03))):
        box("book%d" % k, -2.5, -1.6, 0.32 + 0.034 * k, 0.30 - 0.02 * k, 0.23, h - 0.002, mt, 12 - 9 * k, bev=0.003)
    cyl("ctbowl", -2.12, -1.72, 0.32, 0.40, 0.10, "ceramic_clay", 40, r_top=0.12)
    # a linen throw folded over the sofa's arm
    box("throw_sofa", -3.85, -3.0, 0.62, 0.3, 0.8, 0.03, "linen_rust", 0, bev=0.01, sub=2)
    # a side table and lamp by the sofa's end
    cyl("side", -0.45, -3.1, 0.0, 0.52, 0.22, "walnut", 40, bev=0.01)
    cyl("lamp_base", -0.45, -3.1, 0.52, 0.86, 0.07, "ceramic_clay", 32, r_top=0.05)
    cyl("lamp_shade", -0.45, -3.1, 0.86, 1.10, 0.19, "linen_cream", 40, r_top=0.15)
    cyl("lamp_bulb", -0.45, -3.1, 0.90, 1.05, 0.05, "lamp_warm", 16)
    # the console and the canvas on the left partition
    sbox("console", PART_L + 0.08, PART_L + 0.50, 2.2, 4.4, 0.12, 0.70, "walnut", bev=0.006)
    sbox("console_plinth", PART_L + 0.10, PART_L + 0.46, 2.3, 4.3, 0.0, 0.12, "shadowgap")
    sbox("canvas", PART_L + 0.07, PART_L + 0.11, 2.45, 4.15, 1.05, 2.45, "art", bev=0.004)
    cyl("vase_tall", PART_L + 0.28, -2.6, 0.70, 1.12, 0.09, "ceramic_clay", 32, r_top=0.05)
    for k in range(5):
        a_ = rnd.uniform(0, 6.28)
        tube("stem%d" % k, [(PART_L + 0.28, -2.6, 1.0), (PART_L + 0.28 + 0.15 * math.cos(a_), -2.6 + 0.15 * math.sin(a_), 1.5), (PART_L + 0.28 + 0.3 * math.cos(a_), -2.6 + 0.3 * math.sin(a_), 1.85)], 0.004, "bark", 5)
    # the olive tree by the glass
    olive_tree("olive", -4.35, 0.75, 2.3, seed=5)
    # the dining: an oak table along the depth, six chairs, a linear pendant
    tcx, tc0, tc1 = 2.75, 1.25, 3.55
    sbox("table_top", tcx - 0.52, tcx + 0.52, tc0, tc1, 0.72, 0.76, "oak_light", bev=0.008)
    for dd in (tc0 + 0.35, tc1 - 0.35):
        sbox("table_leg", tcx - 0.42, tcx + 0.42, dd - 0.045, dd + 0.045, 0.0, 0.72, "oak_light", bev=0.006)
    for k, dd in enumerate((tc0 + 0.45, (tc0 + tc1) / 2, tc1 - 0.45)):
        dining_chair(tcx - 0.78, -dd, 90)
        dining_chair(tcx + 0.78, -dd, -90)
    pendant_linear(tcx, (tc0 + tc1) / 2, 1.6, 2.05)
    cyl("dvase", tcx + 0.05, -2.2, 0.76, 1.02, 0.07, "ceramic_white", 32, r_top=0.045)
    for k in range(4):
        a_ = rnd.uniform(0, 6.28)
        tube("dstem%d" % k, [(tcx + 0.05, -2.2, 0.95), (tcx + 0.05 + 0.12 * math.cos(a_), -2.2 + 0.12 * math.sin(a_), 1.25), (tcx + 0.05 + 0.2 * math.cos(a_), -2.2 + 0.2 * math.sin(a_), 1.45)], 0.003, "bark", 5)
    sheer("sheer_L", PART_L + 0.02, PART_L + 1.1, d_glass)
    sheer("sheer_R", PART_R - 0.9, PART_R - 0.02, d_glass)


def master_bedroom():
    """the corner bedroom: the bed faces the glass (west), the curved glass turns to the north-west"""
    bc = 7.35           # the bed's centre in s
    head = BED_BACK - 0.02
    sbox("headboard", bc - 1.7, bc + 1.7, head - 0.09, head, 0.0, 1.35, "headboard", bev=0.03)
    sbox("bed_base", bc - 0.95, bc + 0.95, head - 2.22, head - 0.09, 0.08, 0.34, "linen_taupe", bev=0.03)
    sbox("bed_plinth", bc - 0.85, bc + 0.85, head - 2.1, head - 0.2, 0.0, 0.08, "shadowgap")
    cushion("mattress", bc, -(head - 1.16), 0.30, 1.84, 2.06, 0.26, "duvet", 0, 0.004, 0.06)
    duv = cushion("duvet", bc, -(head - 1.28), 0.26, 2.06, 1.86, 0.34, "duvet", 0, 0.018, 0.10)
    displace(duv, 0.012, 0.08)
    fold = cushion("duvet_fold", bc, -(head - 0.47), 0.52, 2.02, 0.26, 0.10, "duvet", 0, 0.012, 0.05)
    # a linen throw over the foot of the bed, draped: lying on the duvet, then falling over the edge in soft folds
    foot = head - 2.21
    path = [(foot + 0.62, 0.612), (foot + 0.4, 0.618), (foot + 0.2, 0.614), (foot + 0.06, 0.603), (foot - 0.012, 0.58),
            (foot - 0.03, 0.53), (foot - 0.036, 0.45), (foot - 0.04, 0.36), (foot - 0.042, 0.28)]
    V, F = [], []
    ncol = 90
    fine = []
    for k in range(len(path) - 1):
        (d0, z0), (d1, z1) = path[k], path[k + 1]
        n_ = 1 if d0 < foot + 0.05 else 6
        for j in range(n_):
            fine.append((d0 + (d1 - d0) * j / n_, z0 + (z1 - z0) * j / n_))
    fine.append(path[-1])
    path = fine
    for ri, (dd, zz) in enumerate(path):
        hang = max(0.0, (foot - dd) / 0.04)
        for ci in range(ncol + 1):
            ss = bc - 1.07 + 2.14 * ci / ncol
            fold = math.sin((ss - bc) * 11.0 + ri * 0.3) * (0.012 + 0.02 * min(1.0, hang))
            wr = 0.0 if hang else (0.010 * math.sin(ss * 13.0 + dd * 20.0) + 0.006 * math.sin(ss * 29.0 - dd * 11.0) + 0.004 * math.sin(ss * 47.0 + dd * 37.0))
            V.append((ss, -(dd - fold * min(1.0, hang)), zz + max(-0.004, wr)))
    for ri in range(len(path) - 1):
        for ci in range(ncol):
            a0 = ri * (ncol + 1) + ci
            F.append((a0, a0 + 1, a0 + ncol + 2, a0 + ncol + 1))
    th = obj("throw", V, F, "linen_clay", smooth=True)
    so = th.modifiers.new("solid", "SOLIDIFY")
    so.thickness = 0.012
    sub = th.modifiers.new("sub", "SUBSURF")
    sub.levels = sub.render_levels = 1
    for k, x in enumerate((-0.48, 0.48)):
        pillow("pillow_b%d" % k, bc + x, -(head - 0.22), 0.6, 0.8, 0.52, 0.2, "duvet", 180, 18, 0.5, 0.006)
        pillow("pillow_f%d" % k, bc + x * 0.95, -(head - 0.4), 0.6, 0.7, 0.44, 0.18, "duvet", 180, 16, 0.5, 0.006)
    pillow("pillow_c", bc, -(head - 0.56), 0.6, 0.5, 0.34, 0.15, "linen_sage", 180, 12, 0.5, 0.004)
    for sgn in (-1, 1):
        ns = bc + sgn * 1.32
        sbox("nightstand", ns - 0.26, ns + 0.26, head - 0.48, head - 0.02, 0.12, 0.52, "walnut", bev=0.006)
        cyl("ns_lamp_b", ns, -(head - 0.25), 0.52, 0.80, 0.06, "ceramic_white", 32, r_top=0.045)
        cyl("ns_lamp_s", ns, -(head - 0.25), 0.80, 0.98, 0.15, "linen_cream", 40, r_top=0.12)
        cyl("ns_lamp_bulb", ns, -(head - 0.25), 0.82, 0.95, 0.04, "lamp_warm", 16)
    box("bed_rug", bc, -(head - 1.3), 0.0, 3.0, 2.6, 0.012, "rug", 0, bev=0.004)
    sbox("bench", bc - 0.7, bc + 0.7, head - 2.72, head - 2.32, 0.30, 0.45, "boucle", bev=0.04)
    for sx in (bc - 0.62, bc + 0.62):
        sbox("bench_leg", sx - 0.02, sx + 0.02, head - 2.68, head - 2.36, 0.0, 0.30, "walnut")
    lounge_chair(11.2, -2.7, 225)
    cyl("bside", 10.55, -2.1, 0.0, 0.5, 0.2, "travertine", 40, bev=0.01)
    olive_tree("olive_b", 5.35, 0.8, 1.8, seed=11, pot_r=0.25, pot_h=0.45, leaves=5000)
    sheer("sheer_B", PART_R + 0.02, 6.2, d_glass)


def teak_chair(cx, cy, rot):
    """a slatted teak armchair with linen cushions (an illustration)"""
    c, s = math.cos(rot * DEG), math.sin(rot * DEG)

    def P(x, y):
        return cx + x * c - y * s, cy + x * s + y * c

    for sx in (-0.29, 0.29):
        for sy in (-0.28, 0.28):
            x, y = P(sx, sy)
            box("tc_leg", x, y, 0.0, 0.04, 0.04, 0.36 if sy < 0 else 0.66, "teak", rot, bev=0.008)
        x, y = P(sx, -0.02)
        box("tc_arm", x, y, 0.56, 0.05, 0.62, 0.028, "teak", rot, bev=0.008)
        x, y = P(sx, 0.0)
        box("tc_rail", x, y, 0.22, 0.035, 0.58, 0.05, "teak", rot, bev=0.008)
    for k in range(6):
        x, y = P(0, -0.27 + k * 0.105)
        box("tc_slat", x, y, 0.27, 0.58, 0.075, 0.022, "teak", rot, bev=0.005)
    x, y = P(0, -0.04)
    cushion("tc_seat", x, y, 0.295, 0.56, 0.56, 0.08, "linen_sand", rot, 0.004, 0.03)
    x, y = P(0, 0.27)
    cushion("tc_back", x, y, 0.37, 0.54, 0.08, 0.36, "linen_sand", rot, 0.004, 0.03)


def balcony_furniture():
    teak_chair(2.05, 0.66, 205)
    teak_chair(3.05, 0.60, 155)
    cyl("bal_table", 2.55, 0.28, 0.0, 0.42, 0.2, "teak", 36, bev=0.01)
    cyl("bal_glass1", 2.5, 0.25, 0.42, 0.55, 0.03, "rail_glass", 24)
    olive_tree("olive_bal", -3.8, -0.62, 1.5, seed=21, pot_r=0.26, pot_h=0.5, leaves=5000)


def ceiling_details():
    """recessed downlights (a black rim), the linear air-conditioning grille near the back"""
    pts = []
    for s in (-3.9, -2.35, -0.8):
        for d in (1.4, 3.6, 5.6):
            pts.append((s, d))
    for s in (1.6, 3.9):
        for d in (4.2, 6.2):
            pts.append((s, d))
    for (s, d) in ((6.2, 1.6), (8.5, 1.6), (6.2, 3.6), (8.5, 3.6)):
        pts.append((s, d))
    for k, (s, d) in enumerate(pts):
        cyl("dl_rim%d" % k, s, -d, CEIL - 0.004, CEIL - 0.001, 0.045, "downlight_rim", 24)
        cyl("dl_em%d" % k, s, -d, CEIL - 0.005, CEIL - 0.004, 0.03, "downlight_emit", 16)
    sbox("vrf", PART_L + 0.4, PART_R - 0.4, 6.85, 6.97, CEIL - 0.004, CEIL - 0.001, "vrf")
    for k, s0 in enumerate((-3.4, -1.3)):
        sbox("track%d" % k, s0 - 0.012, s0 + 0.012, 1.1, 3.9, CEIL - 0.03, CEIL, "blacksteel")
        for j, dd in enumerate((1.5, 2.5, 3.5)):
            cyl("spot%d%d" % (k, j), s0, -dd, CEIL - 0.13, CEIL - 0.03, 0.028, "blacksteel", 20)
            cyl("spot_em%d%d" % (k, j), s0, -dd, CEIL - 0.1305, CEIL - 0.129, 0.02, "downlight_emit", 12)
    # a lowered band over the kitchen (the air conditioning runs above it), with a 2 cm shadow gap
    sbox("bulkhead", 0.8, PART_R - 0.06, 5.95, BACK_D - 0.07, CEIL - 0.28, CEIL - 0.001, "ceiling")
    sbox("bulk_gap", 0.8, PART_R - 0.06, 5.93, 5.95, CEIL - 0.04, CEIL - 0.001, "shadowgap")
    return pts


# ============================================================================================ lights and camera
def lights(downs):
    # portals at the glass: help the sky's light through the windows
    def portal(name, s, d, w, h, rot=0.0):
        ld = bpy.data.lights.new(name, "AREA")
        ld.shape = "RECTANGLE"
        ld.size, ld.size_y = w, h
        ld.cycles.is_portal = True
        ob = bpy.data.objects.new(name, ld)
        KW.link(ob)
        own(ob)
        ob.location = (s, -d, h / 2)
        ob.rotation_euler = (-90 * DEG, 0, rot * DEG)
        return ob

    portal("portal_living", -0.15, 0.25, 9.6, 3.1)
    portal("portal_bed1", 7.2, 0.5, 4.8, 3.1, 0)
    portal("portal_bed2", 11.11, 1.545, 3.7, 3.1, -27.9)
    power = 16.0 if NIGHT else (3.0 if TODN == "sunset" else 0.0)
    if power:
        for k, (s, d) in enumerate(downs):
            ld = bpy.data.lights.new("dl%d" % k, "SPOT")
            ld.energy = power
            ld.color = (1.0, 0.80, 0.60)
            ld.spot_size = 70 * DEG
            ld.spot_blend = 0.6
            ld.shadow_soft_size = 0.03
            ob = bpy.data.objects.new("dl%d" % k, ld)
            KW.link(ob)
            own(ob)
            ob.location = (s, -d, CEIL - 0.02)
        for nm, (s, d, z, e) in {"lamp_sofa": (-0.45, 3.1, 0.97, 18.0), "pend": (2.75, 2.4, 1.98, 30.0),
                                  "ns1": (6.03, 4.93, 0.9, 10.0), "ns2": (8.67, 4.93, 0.9, 10.0)}.items():
            ld = bpy.data.lights.new(nm, "POINT")
            ld.energy = e * (2.0 if NIGHT else 0.5)
            ld.color = (1.0, 0.72, 0.46)
            ld.shadow_soft_size = 0.05
            ob = bpy.data.objects.new(nm, ld)
            KW.link(ob)
            own(ob)
            ob.location = (s, -d, z)


def camera(s, d, z, yaw=0.0, pitch=0.0, hfov=80.0, pano=False, shift_y=0.0):
    cd = bpy.data.cameras.new("cam")
    cd.clip_start = 0.05
    cd.clip_end = 90000.0
    if pano:
        cd.type = "PANO"
        cd.panorama_type = "EQUIRECTANGULAR"
    else:
        cd.lens_unit = "FOV"
        cd.sensor_fit = "HORIZONTAL"
        cd.angle = hfov * DEG
        cd.shift_y = shift_y
    cam = bpy.data.objects.new("cam", cd)
    KW.link(cam)
    own(cam)
    cam.location = (s, -d, z)
    # local: look along +Y (out); yaw positive turns right (clockwise from above)
    cam.rotation_euler = ((90 + pitch) * DEG, 0, -yaw * DEG)
    bpy.context.scene.camera = cam
    return cam


# ============================================================================================ build
def build():
    KW.build_sky(TODN)
    make_materials()
    eye = world_of(0, 3.0, 1.5)
    sector = lambda key, fl, phi: key == TOWER and fl == FLOOR and abs(((phi - PHI_C + 180) % 360) - 180) <= 45.5
    KW.build_towers(skip=sector)
    KW.build_blocks(eye)
    KW.build_ground(eye)
    KW.build_trees(eye)
    KW.build_cars(eye)
    shell()
    curtain_wall()
    partitions()
    balcony()
    kitchen()
    living()
    master_bedroom()
    balcony_furniture()
    downs = ceiling_details()
    # the herringbone: the great room and the bedroom
    room = [(PART_L + 0.06, d_glass(PART_L + 0.06) + 0.06)] + [(s, d + 0.06) for (s, d) in GL if PART_L + 0.06 < s < PART_R - 0.06] + \
           [(PART_R - 0.06, d_glass(PART_R - 0.06) + 0.06), (PART_R - 0.06, BACK_D - 0.07), (PART_L + 0.06, BACK_D - 0.07)]
    herringbone(room, "hb_living")
    bed = [(PART_R + 0.06, d_glass(PART_R + 0.06) + 0.06)] + [(s, d + 0.06) for (s, d) in GL if PART_R + 0.06 < s < GL[-1][0] - 0.3] + \
          [(AG - BED_BACK - 0.1, BED_BACK - 0.07), (PART_R + 0.06, BED_BACK - 0.07)]
    herringbone(bed, "hb_bed")
    lights(downs)
    KW.build_sun()


SHOTS = {
    # s, d, z, yaw (deg, + = right of the facing), pitch, hfov; chosen from the previews (p5-p9)
    "living": dict(s=-0.35, d=7.05, z=1.38, yaw=-2.0, pitch=0.0, hfov=82.0, shift=-0.04),       # straight out, the sun on the axis
    "living3q": dict(s=-4.5, d=6.9, z=1.40, yaw=22.0, pitch=0.0, hfov=80.0, shift=0.0),        # from the hall's corner, three-quarters
    "bedroom": dict(s=6.2, d=4.5, z=1.60, yaw=30.0, pitch=-2.0, hfov=90.0, shift=0.0),         # the corner glass, the sea to the north-west
    "balcony": dict(s=2.6, d=-0.3, z=1.55, yaw=-48.0, pitch=-4.0, hfov=84.0, shift=0.0),       # tower A turning, the city, the sea
    "living360": dict(s=0.35, d=3.9, z=1.5, yaw=0.0, pitch=0.0, hfov=0, shift=0.0),
    "view": dict(s=0.0, d=1.2, z=1.5, yaw=0.0, pitch=-4.0, hfov=70.0, shift=0.0),              # the same frame on every floor (the twist)
}

build()
for nm in [x for x in os.environ.get("KH_HIDE", "").split(",") if x]:
    for ob in bpy.data.objects:
        if ob.name.startswith(nm):
            ob.hide_render = True
if os.environ.get("KH_CAMS"):
    # preview: name:s,d,z,yaw,pitch,hfov;...  (one build, several framings)
    sc = bpy.context.scene
    base = os.path.splitext(OUT)[0]
    for item in os.environ["KH_CAMS"].split(";"):
        nm, vals = item.split(":")
        sv, dv, zv, yv, pv, fv = [float(x) for x in vals.split(",")]
        camera(sv, dv, zv, yv, pv, fv)
        sc.view_settings.exposure = {("in", "day"): -1.5, ("in", "sunset"): -1.7, ("in", "evening"): 0.1,
                                     ("out", "day"): -3.4, ("out", "sunset"): -2.9, ("out", "evening"): -1.2}[("in" if INSIDE else "out", TODN)] + float(os.environ.get("KH_EXP", "0"))
        if not os.environ.get("KH_NOGLARE"):
            KW.add_glare(3.5 / 2 ** sc.view_settings.exposure, float(os.environ.get("KH_GLARE", "0.22")))
        sc.render.filepath = base + "-" + nm + ".png"
        bpy.ops.render.render(write_still=True)
        print("WROTE", sc.render.filepath)
    raise SystemExit(0)
sh = SHOTS[SHOT]
cam = camera(sh["s"], sh["d"], sh["z"], sh["yaw"], sh["pitch"], sh["hfov"], pano=(SHOT == "living360"), shift_y=sh.get("shift", 0.0))
sc = bpy.context.scene
EXPO = {("in", "day"): -1.5, ("in", "sunset"): -1.7, ("in", "evening"): 0.85,
        ("out", "day"): -3.4, ("out", "sunset"): -2.9, ("out", "evening"): -1.2}
sc.view_settings.exposure = EXPO[("in" if INSIDE else "out", TODN)] + SHOT_EXP.get((SHOT, TODN), (0.0, 0))[0] + float(os.environ.get("KH_EXP", "0"))
if not os.environ.get("KH_NOGLARE"):
    KW.add_glare(3.5 / 2 ** sc.view_settings.exposure, float(os.environ.get("KH_GLARE", "0.22")))
sc.render.filepath = OUT
bpy.context.view_layer.update()
cw = cam.matrix_world.translation
print("CAMERA %s world (%.1f, %.1f, %.2f) m; facing %.1f deg; %s %s" % (SHOT, cw.x, cw.y, cw.z, (BFACE + sh["yaw"]) % 360, TODN, KW.TOD["label"]))
if os.environ.get("KH_DIAG"):
    exec(open(os.environ["KH_DIAG"], encoding="utf-8").read())
    raise SystemExit(0)
if os.environ.get("KH_SAVE"):
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["KH_SAVE"])
bpy.ops.render.render(write_still=True)
print("WROTE", OUT)
