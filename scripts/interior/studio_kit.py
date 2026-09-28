# -*- coding: utf-8 -*-
"""Furniture and finish styles for the example apartment's 360 rooms (design system BuyJourney v78: the design step).

Called by rainbow_interior.py when its style argument is not "bare". Everything here is an illustration of a design idea in
an example apartment, not the developer's specification (the page says so). Built from Blender primitives only (no
downloaded assets): bevelled boxes, cylinders and spheres with procedural materials.

The room frame: P(a, b) is a point a metres along the back wall's direction (u, from back_l to back_r) and b metres inward
from the glass centre m (in). The camera stands at P(0, 3.1), 1.6 m above the floor, looking out through the glass."""
import math
import random

import bmesh
import bpy
from mathutils import Vector

STYLES = {
    # floor tones (plank light, plank dark) or a stone tile; walls; kitchen fronts (run, tall/upper); counter; sofa; accent;
    # rug; dining wood; chair fabric; coffee table; lamp metal
    "warm": dict(floor=("oak", (0.52, 0.34, 0.19), (0.60, 0.41, 0.24)), wall=(0.86, 0.83, 0.78),
                 run=("wood", (0.20, 0.12, 0.07), (0.28, 0.17, 0.10)), upper=("wood", (0.20, 0.12, 0.07), (0.28, 0.17, 0.10)),
                 counter=(0.93, 0.92, 0.90), sofa=("fabric", (0.62, 0.56, 0.48)), accent=("fabric", (0.52, 0.25, 0.15)),
                 rug=(0.78, 0.74, 0.66), dining=("wood", (0.46, 0.30, 0.16), (0.58, 0.40, 0.23)), chair=("fabric", (0.70, 0.64, 0.55)),
                 table=("stone", (0.80, 0.74, 0.64)), metal="brass", art=((0.62, 0.36, 0.20), (0.86, 0.78, 0.64), (0.25, 0.30, 0.28))),
    "light": dict(floor=("oak", (0.66, 0.56, 0.42), (0.76, 0.67, 0.53)), wall=(0.90, 0.89, 0.86),
                  run=("paint", (0.40, 0.48, 0.40)), upper=("paint", (0.90, 0.89, 0.86)),
                  counter=(0.95, 0.95, 0.94), sofa=("fabric", (0.74, 0.73, 0.70)), accent=("fabric", (0.40, 0.48, 0.40)),
                  rug=(0.82, 0.81, 0.78), dining=("wood", (0.68, 0.58, 0.44), (0.78, 0.69, 0.55)), chair=("fabric", (0.86, 0.84, 0.80)),
                  table=("wood", (0.68, 0.58, 0.44), (0.78, 0.69, 0.55)), metal="black", art=((0.40, 0.48, 0.40), (0.93, 0.92, 0.88), (0.70, 0.62, 0.50))),
    "stone": dict(floor=("stone", (0.40, 0.38, 0.35)), wall=(0.78, 0.75, 0.70),
                  run=("paint", (0.09, 0.09, 0.09)), upper=("paint", (0.12, 0.12, 0.12)),
                  counter=(0.30, 0.29, 0.28), sofa=("leather", (0.36, 0.17, 0.07)), accent=("fabric", (0.80, 0.76, 0.68)),
                  rug=(0.20, 0.20, 0.20), dining=("wood", (0.20, 0.12, 0.07), (0.28, 0.17, 0.10)), chair=("leather", (0.06, 0.06, 0.06)),
                  table=("stone", (0.26, 0.25, 0.24)), metal="black", art=((0.78, 0.74, 0.66), (0.20, 0.20, 0.20), (0.55, 0.38, 0.24))),
}


# ---------------------------------------------------------------- materials
def _p(m):
    return m.node_tree.nodes["Principled BSDF"]


def fabric(name, color, rough=0.92):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = _p(m)
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    for k in ("Sheen Weight",):
        if k in b.inputs: b.inputs[k].default_value = 0.6
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 900.0
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.12
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def leather(name, color):
    m = fabric(name, color, rough=0.42)
    b = _p(m)
    if "Sheen Weight" in b.inputs: b.inputs["Sheen Weight"].default_value = 0.0
    if "Coat Weight" in b.inputs: b.inputs["Coat Weight"].default_value = 0.15
    return m


def paint(name, color, rough=0.55):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = _p(m); b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough
    return m


def wood(name, c0, c1, scale=6.0, rough=0.42, planks=False):
    """wood: fine long fibres (noise stretched along the board) in a narrow range between two tones, a faint figure, and for
    floors 180 x 20 cm boards whose tone varies a little from board to board"""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = _p(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1.2, 42.0, 1.2)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    fib = nt.nodes.new("ShaderNodeTexNoise"); fib.inputs["Scale"].default_value = 3.0; fib.inputs["Detail"].default_value = 9.0
    fib.inputs["Roughness"].default_value = 0.62
    nt.links.new(mp.outputs["Vector"], fib.inputs["Vector"])
    mp2 = nt.nodes.new("ShaderNodeMapping"); mp2.inputs["Scale"].default_value = (0.6, 6.0, 0.6)
    nt.links.new(tc.outputs["Object"], mp2.inputs["Vector"])
    fig = nt.nodes.new("ShaderNodeTexNoise"); fig.inputs["Scale"].default_value = 1.4; fig.inputs["Detail"].default_value = 3.0
    nt.links.new(mp2.outputs["Vector"], fig.inputs["Vector"])
    mixf = nt.nodes.new("ShaderNodeMix"); mixf.data_type = "FLOAT"; mixf.inputs[0].default_value = 0.35
    nt.links.new(fib.outputs["Fac"], mixf.inputs[2]); nt.links.new(fig.outputs["Fac"], mixf.inputs[3])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.35; ramp.color_ramp.elements[1].position = 0.68
    ramp.color_ramp.elements[0].color = (*c0, 1); ramp.color_ramp.elements[1].color = (*c1, 1)
    nt.links.new(mixf.outputs[0], ramp.inputs["Fac"])
    col = ramp.outputs["Color"]
    if planks:
        br = nt.nodes.new("ShaderNodeTexBrick")
        br.inputs["Scale"].default_value = 1.0; br.inputs["Brick Width"].default_value = 1.8; br.inputs["Row Height"].default_value = 0.2
        br.inputs["Mortar Size"].default_value = 0.0012; br.inputs["Bias"].default_value = 0.0; br.offset = 0.37
        br.inputs["Color1"].default_value = (1, 1, 1, 1); br.inputs["Color2"].default_value = (0.9, 0.88, 0.86, 1)
        br.inputs["Mortar"].default_value = (0.45, 0.45, 0.45, 1)
        nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
        mul = nt.nodes.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"; mul.inputs[0].default_value = 1.0
        nt.links.new(col, mul.inputs[6]); nt.links.new(br.outputs["Color"], mul.inputs[7])
        col = mul.outputs[2]
    nt.links.new(col, b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    if "Coat Weight" in b.inputs: b.inputs["Coat Weight"].default_value = 0.18 if planks else 0.08
    if "Coat Roughness" in b.inputs: b.inputs["Coat Roughness"].default_value = 0.2
    return m


def stone(name, color, tile=None, rough=0.38):
    """honed stone: soft cloudy variation; tile=(w, h) adds large-format joints"""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = _p(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 1.6; nz.inputs["Detail"].default_value = 8.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*[c * 0.9 for c in color], 1); ramp.color_ramp.elements[1].color = (*[min(1, c * 1.1) for c in color], 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
    col = ramp.outputs["Color"]
    if tile:
        br = nt.nodes.new("ShaderNodeTexBrick")
        br.inputs["Scale"].default_value = 1.0; br.inputs["Brick Width"].default_value = tile[0]; br.inputs["Row Height"].default_value = tile[1]
        br.inputs["Mortar Size"].default_value = 0.002; br.offset = 0.0
        br.inputs["Color1"].default_value = (1, 1, 1, 1); br.inputs["Color2"].default_value = (0.95, 0.95, 0.95, 1)
        br.inputs["Mortar"].default_value = (0.55, 0.55, 0.55, 1)
        nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
        mul = nt.nodes.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"; mul.inputs[0].default_value = 1.0
        nt.links.new(col, mul.inputs[6]); nt.links.new(br.outputs["Color"], mul.inputs[7])
        col = mul.outputs[2]
    nt.links.new(col, b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    return m


def rugmat(name, color):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = _p(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.0; nz.inputs["Detail"].default_value = 6.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*[c * 0.88 for c in color], 1); ramp.color_ramp.elements[1].color = (*color, 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 1.0
    fine = nt.nodes.new("ShaderNodeTexNoise"); fine.inputs["Scale"].default_value = 1400.0
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.35
    nt.links.new(fine.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def metal(kind):
    m = bpy.data.materials.new("metal-" + kind); m.use_nodes = True
    b = _p(m)
    if kind == "brass":
        b.inputs["Base Color"].default_value = (0.86, 0.66, 0.38, 1); b.inputs["Roughness"].default_value = 0.28
    else:
        b.inputs["Base Color"].default_value = (0.03, 0.03, 0.03, 1); b.inputs["Roughness"].default_value = 0.4
    b.inputs["Metallic"].default_value = 1.0
    return m


def artmat(cols):
    """an abstract canvas: soft colour fields"""
    m = bpy.data.materials.new("art"); m.use_nodes = True
    nt = m.node_tree; b = _p(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 1.1; nz.inputs["Detail"].default_value = 2.0
    nz.inputs["Distortion"].default_value = 1.4
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "CONSTANT"
    e = ramp.color_ramp.elements
    e[0].color = (*cols[1], 1); e[1].position = 0.52; e[1].color = (*cols[0], 1)
    e3 = e.new(0.64); e3.color = (*cols[2], 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.85
    return m


def leafmat():
    m = bpy.data.materials.new("leaf"); m.use_nodes = True
    nt = m.node_tree; b = _p(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 18.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (0.05, 0.11, 0.03, 1); ramp.color_ramp.elements[1].color = (0.16, 0.26, 0.08, 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.5
    if "Subsurface Weight" in b.inputs: b.inputs["Subsurface Weight"].default_value = 0.2
    return m


def sheer():
    m = bpy.data.materials.new("sheer"); m.use_nodes = True
    b = _p(m)
    b.inputs["Base Color"].default_value = (0.95, 0.93, 0.89, 1); b.inputs["Roughness"].default_value = 0.9
    b.inputs["Transmission Weight"].default_value = 0.55
    if "Sheen Weight" in b.inputs: b.inputs["Sheen Weight"].default_value = 0.5
    return m


def glow():
    m = bpy.data.materials.new("globe"); m.use_nodes = True
    b = _p(m)
    b.inputs["Base Color"].default_value = (1, 0.97, 0.92, 1); b.inputs["Roughness"].default_value = 0.3
    b.inputs["Emission Color"].default_value = (1.0, 0.82, 0.62, 1); b.inputs["Emission Strength"].default_value = 6.0
    return m


def make(spec, name):
    kind = spec[0]
    if kind == "wood": return wood(name, spec[1], spec[2])
    if kind == "oak": return wood(name, spec[1], spec[2], scale=3.0, rough=0.35, planks=True)
    if kind == "stone": return stone(name, spec[1])
    if kind == "fabric": return fabric(name, spec[1])
    if kind == "leather": return leather(name, spec[1])
    return paint(name, spec[1])


# ---------------------------------------------------------------- geometry
def smooth_bevel(ob, width, segs=3):
    if width <= 0:
        return ob
    md = ob.modifiers.new("bevel", "BEVEL"); md.width = width; md.segments = segs; md.limit_method = "NONE"
    try:
        md.harden_normals = True
    except Exception:
        pass
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def cylinder(name, cx, cy, z0, z1, r, material, seg=40):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r, radius2=r, depth=z1 - z0)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); ob.data.materials.append(material)
    ob.location = (cx, cy, (z0 + z1) / 2)
    bpy.context.collection.objects.link(ob)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def sphere(name, cx, cy, cz, r, material, seg=24):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=r)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); ob.data.materials.append(material)
    ob.location = (cx, cy, cz)
    bpy.context.collection.objects.link(ob)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def furnish(ctx, style_name):
    st = STYLES[style_name]
    box = ctx["box"]; M = ctx["M"]; Z0 = ctx["Z0"]; CEIL = ctx["CEIL"]
    mx, my = ctx["mx"], ctx["my"]; inx, iny = ctx["inx"], ctx["iny"]; ux, uy = ctx["ux"], ctx["uy"]; ang = ctx["ang"]
    gl = ctx["glass_line"]
    rnd = random.Random(7)

    def P(a, b):
        return (mx + ux * a + inx * b, my + uy * a + iny * b)

    def AB(pt):
        dx, dy = pt[0] - mx, pt[1] - my
        return dx * ux + dy * uy, dx * inx + dy * iny

    aL, bL = AB(gl[0]); aR, bR = AB(gl[-1])
    if aL > aR:  # keep aL on the negative side
        aL, aR, bL, bR = aR, aL, bR, bL

    def B(name, a, b, z0, z1, sa, sb, mat, bev=0.0, segs=3, rot=0.0):
        x, y = P(a, b)
        return smooth_bevel(box(name, x, y, Z0 + (z0 + z1) / 2, sa, sb, z1 - z0, mat, ang + rot), bev, segs)

    # --- the finishes
    fl = st["floor"]
    floor_mat = wood("floor-" + style_name, fl[1], fl[2], scale=3.0, rough=0.33, planks=True) if fl[0] == "oak" else stone("floor-" + style_name, fl[1], tile=(1.2, 1.2), rough=0.3)
    for ob in bpy.data.objects:
        if ob.name.startswith("room-floor"):
            ob.data.materials.clear(); ob.data.materials.append(floor_mat)
    _p(M["wall"]).inputs["Base Color"].default_value = (*st["wall"], 1)
    run = make(st["run"], "run-" + style_name); upper = make(st["upper"], "upper-" + style_name)
    for ob in bpy.data.objects:
        if ob.name.startswith("kitchen-run") or ob.name.startswith("island") and not ob.name.startswith("island-top"):
            ob.data.materials.clear(); ob.data.materials.append(run)
        elif ob.name.startswith("kitchen-tall") or ob.name.startswith("kitchen-upper"):
            ob.data.materials.clear(); ob.data.materials.append(upper)
    _p(M["counter"]).inputs["Base Color"].default_value = (*st["counter"], 1)

    sofa = make(st["sofa"], "sofa"); accent = make(st["accent"], "accent"); chairm = make(st["chair"], "chair")
    dining = make(st["dining"], "dining"); tablem = make(st["table"], "coffee"); met = metal(st["metal"])
    rug = rugmat("rug", st["rug"]); leaf = leafmat(); pot = paint("pot", (0.72, 0.66, 0.58), 0.8)
    if style_name == "stone":
        pot = paint("pot", (0.15, 0.15, 0.15), 0.7)

    # --- the lounge: a three-seat sofa with its back to the right wall, facing into the room
    sa_c = aR - 0.62            # the sofa's centre line
    sb_c = 2.35
    B("sofa-base", sa_c, sb_c, 0.10, 0.40, 0.98, 2.56, sofa, 0.03)
    for i, off in enumerate((-0.82, 0.0, 0.82)):
        B("sofa-seat-%d" % i, sa_c - 0.08, sb_c + off, 0.40, 0.56, 0.78, 0.80, sofa, 0.07, 4)
        B("sofa-back-%d" % i, sa_c + 0.36, sb_c + off, 0.44, 0.94, 0.24, 0.80, sofa, 0.09, 4)
    for s in (-1, 1):
        B("sofa-arm-%d" % s, sa_c, sb_c + s * 1.36, 0.10, 0.66, 0.98, 0.20, sofa, 0.07, 4)
    B("pillow-a", sa_c + 0.18, sb_c - 1.0, 0.56, 0.98, 0.14, 0.46, accent, 0.07, 4, rot=0.25)
    B("pillow-b", sa_c + 0.18, sb_c + 1.0, 0.56, 0.98, 0.14, 0.46, accent, 0.07, 4, rot=-0.25)
    B("throw", sa_c - 0.1, sb_c + 0.9, 0.56, 0.59, 0.6, 0.5, accent, 0.02)
    # a rug and a round coffee table
    B("rug", sa_c - 1.2, sb_c, 0.0, 0.012, 2.5, 3.3, rug, 0.0)
    tx, ty = P(sa_c - 1.55, sb_c)
    cylinder("coffee-top", tx, ty, Z0 + 0.34, Z0 + 0.39, 0.55, tablem)
    cylinder("coffee-base", tx, ty, Z0 + 0.0, Z0 + 0.34, 0.22, tablem)
    bx, by = P(sa_c - 1.62, sb_c - 0.12)
    for k, (h, c) in enumerate(((0.035, (0.85, 0.82, 0.76)), (0.03, (0.25, 0.3, 0.33)), (0.025, (0.7, 0.4, 0.25)))):
        box("book-%d" % k, bx, by, Z0 + 0.39 + 0.03 * k + h / 2, 0.28, 0.21, h, paint("book%d" % k, c), ang + 0.1 * k)
    vx, vy = P(sa_c - 1.4, sb_c + 0.22)
    cylinder("bowl", vx, vy, Z0 + 0.39, Z0 + 0.47, 0.13, met)
    # an armchair across the table, and its side table
    ca, cb = sa_c - 2.75, sb_c - 0.55
    B("chair-seat", ca, cb, 0.18, 0.44, 0.82, 0.82, chairm if st["chair"][0] != "leather" else sofa, 0.07, 4)
    B("chair-back", ca - 0.34, cb, 0.40, 0.86, 0.18, 0.80, chairm if st["chair"][0] != "leather" else sofa, 0.07, 4)
    for s in (-1, 1):
        B("chair-arm-%d" % s, ca, cb + s * 0.38, 0.18, 0.62, 0.82, 0.12, chairm if st["chair"][0] != "leather" else sofa, 0.05, 4)
    for s in (-1, 1):
        for t in (-1, 1):
            B("chair-leg-%d%d" % (s, t), ca + s * 0.33, cb + t * 0.33, 0.0, 0.18, 0.035, 0.035, met, 0.005)
    stx, sty = P(ca + 0.05, cb + 0.72)
    cylinder("side-top", stx, sty, Z0 + 0.5, Z0 + 0.53, 0.22, tablem)
    cylinder("side-leg", stx, sty, Z0 + 0.0, Z0 + 0.5, 0.025, met)
    # a floor lamp at the sofa's window end, with a warm light in its shade
    lx, ly = P(aR - 0.35, sb_c - 1.72)
    cylinder("lamp-base", lx, ly, Z0, Z0 + 0.02, 0.17, met)
    cylinder("lamp-pole", lx, ly, Z0, Z0 + 1.52, 0.012, met)
    shade = fabric("shade", (0.93, 0.9, 0.84), 0.9)
    _p(shade).inputs["Transmission Weight"].default_value = 0.6
    cylinder("lamp-shade", lx, ly, Z0 + 1.38, Z0 + 1.7, 0.21, shade)
    ld = bpy.data.lights.new("lamp", "POINT"); ld.energy = 45.0; ld.color = (1.0, 0.8, 0.58); ld.shadow_soft_size = 0.12
    lo = bpy.data.objects.new("lamp", ld); lo.location = (lx, ly, Z0 + 1.5); bpy.context.collection.objects.link(lo)

    # --- the dining corner by the kitchen island: a table for six under three globe pendants
    da, db = aL + 1.75, 3.55
    B("dine-top", da, db, 0.72, 0.76, 1.0, 2.1, dining, 0.012)
    for s in (-1, 1):
        for t in (-1, 1):
            B("dine-leg-%d%d" % (s, t), da + s * 0.42, db + t * 0.95, 0.0, 0.72, 0.07, 0.07, dining, 0.01)
    for s in (-1, 1):
        for k, off in enumerate((-0.68, 0.0, 0.68)):
            ca2 = da + s * 0.72
            B("dchair-seat-%d%d" % (s, k), ca2, db + off, 0.42, 0.48, 0.46, 0.46, chairm, 0.03, 3)
            B("dchair-back-%d%d" % (s, k), ca2 + s * 0.21, db + off, 0.48, 0.88, 0.05, 0.44, chairm, 0.02, 3)
            for u2 in (-1, 1):
                for v2 in (-1, 1):
                    B("dchair-leg-%d%d%d%d" % (s, k, u2, v2), ca2 + u2 * 0.19, db + off + v2 * 0.19, 0.0, 0.42, 0.028, 0.028, met, 0.004)
    gm = glow()
    for k, off in enumerate((-0.6, 0.0, 0.6)):
        px, py = P(da, db + off)
        sphere("globe-%d" % k, px, py, Z0 + 1.82, 0.13, gm)
        cylinder("cord-%d" % k, px, py, Z0 + 1.95, Z0 + CEIL, 0.004, met)
    # a vase with branches on the table
    vx, vy = P(da, db + 0.2)
    cylinder("vase", vx, vy, Z0 + 0.76, Z0 + 1.06, 0.07, paint("vase", (0.9, 0.88, 0.84), 0.35))
    branch = paint("branch", (0.30, 0.24, 0.17), 0.8)
    for k in range(7):
        ob = cylinder("twig-%d" % k, vx, vy, Z0 + 1.0, Z0 + 1.62 + rnd.random() * 0.25, 0.006, branch, 8)
        ob.rotation_euler = (rnd.uniform(-0.35, 0.35), rnd.uniform(-0.35, 0.35), 0)
    # bar stools at the island
    ia, ib = ctx["ic_ab"]
    for k, off in enumerate((-0.7, 0.0, 0.7)):
        sx, sy = P(ia + off, ib - 0.78)
        cylinder("stool-seat-%d" % k, sx, sy, Z0 + 0.64, Z0 + 0.7, 0.2, chairm)
        cylinder("stool-pole-%d" % k, sx, sy, Z0 + 0.02, Z0 + 0.64, 0.02, met)
        cylinder("stool-foot-%d" % k, sx, sy, Z0, Z0 + 0.02, 0.2, met)

    # --- a tall plant in a stone pot at the glass, left
    pa, pb = aL + 0.6, bL + 0.7
    px, py = P(pa, pb)
    cylinder("pot", px, py, Z0, Z0 + 0.5, 0.26, pot)
    cylinder("trunk", px, py, Z0 + 0.45, Z0 + 1.4, 0.02, branch, 10)
    for k in range(90):
        r = 0.35 * math.sqrt(rnd.random()); t = rnd.random() * math.tau
        z = Z0 + 1.15 + rnd.random() * 0.95
        sphere("leaf-%d" % k, px + r * math.cos(t), py + r * math.sin(t), z, 0.05 + rnd.random() * 0.06, leaf, 10)

    # --- sheer curtains stacked at both ends of the glass
    sh = sheer()
    for side, (a0, b0) in (("l", (aL + 0.25, bL + 0.28)), ("r", (aR - 0.25, bR + 0.28))):
        for k in range(9):
            off = (k - 4) * 0.075 * (1 if side == "l" else -1)
            B("curtain-%s-%d" % (side, k), a0 + off, b0 + (0.035 if k % 2 else -0.035), 0.01, CEIL - 0.03, 0.08, 0.02, sh, 0.0)

    # --- a large canvas on the left wall, over a low sideboard
    wa = aL + 0.06
    B("canvas", wa, 1.95, 1.05, 2.05, 0.035, 1.5, artmat(st["art"]), 0.004)
    B("sideboard", aL + 0.26, 1.95, 0.12, 0.62, 0.46, 1.9, dining, 0.012)
    B("sideboard-legs", aL + 0.26, 1.95, 0.0, 0.12, 0.40, 1.8, met, 0.0)
    return {"aL": aL, "aR": aR, "bL": bL, "bR": bR}
