# -*- coding: utf-8 -*-
"""Rainbow's shared facilities as 360 panoramas: the roof pool, the tower's lobby and the Rainbow Club (all ILLUSTRATIONS).

The owner (28.9.2026): a buyer should be able to "walk into the pool, the club, the lobby". Nothing of these interiors is
published (no plans, no renders we may use), so every scene here is an illustration of the facility the record names, placed
where the stage (assets/project-stage/rainbow/stage.js) places it, in the world the stage draws:
  - the site: lot 111's line (LOT_OUTLINE) on its 1.2 m courtyard deck (PLOT.h), the courtyard lawns and trees, the street
    trees; the tower's ellipse with all 39 floors of rainbow balcony bands (K = 3 waves, 0.7-3.6 m deep, the phase turning
    0.16 rad a floor), the recessed 6 m lobby glass, the penthouse setback, the roof parapet and the crown ring; the six
    boutique buildings (BLOCKS, curved capsules BLOCK_W = 12.5 m wide, 9 floors, a 4.4 m ground floor and 3.2 m floors,
    5-wave balcony bands, the top floor set back 2.4 m, roof gardens and pergolas);
  - the world outside: the city standing today (city.json, TLV GIS layer 513) at its recorded heights, the Sde Dov plan's
    lots, our other projects in the quarter (quarter.json) as pale schematic masses, the coastline 713 m to the grid west,
    the beach, the coastal park and the sea; the sky and the sun of a late-September afternoon (rainbow_interior.py).
The scenes:
  roofpool  the roof of boutique building BLOCKS[5] (the stage's roof:5 pin). The design plan (10.5.2023) puts two pools on
            the roofs of two boutique buildings and does not say which two; the stage shows them on BLOCKS[3] and BLOCKS[5],
            as an illustration, and this scene follows it. The pool, its deck and furniture are an illustration.
  lobby     the tower's double-height entrance lobby at the courtyard level (the stage's tower:lobby pin, the tower's grid-west
            side): the layout and finishes are an illustration.
  club      the Rainbow Club, the residents' club at the tower's base, courtyard side (the stage's tower:court pin, on the
            base floor at y0): lounge, kitchenette bar, long table, gym corner; the layout is an illustration.
The roof pool runs along BLOCKS[5]'s curve, which runs grid north-south, so "along the pool" looks north: the panorama's
centre (bearing ~355) has the tower ahead-right (yaw about +12) and the sea to the left (yaw about -75), where it shows as a
thin band between the west boutique buildings (their roofs stand at the eye's height, 32.9 m; the sea lies 2.6° below the
horizon). The script prints these bearings and yaws.
Cycles on the CPU (no supported GPU here), always FIXED threads (other agents share the machine):
  blender -b --factory-startup --python scripts/interior/rainbow_facility.py -- <out.png> <roofpool|lobby|club> [width 1536]
          [samples 24] [threads 6]
Diagnostics: RBF_PROBE="yaw:pitch,..." (degrees from the panorama's centre) casts the camera's rays and prints what they hit,
without rendering."""
import json, math, os, random, sys

import bmesh
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import studio_kit as SK  # noqa: E402  (furniture materials and primitives: fabric, leather, wood, stone, rug, metal, leaf)

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = ARGS[0] if ARGS else os.path.join(HERE, "_renders", "fac-roofpool.png")
SCENE = ARGS[1] if len(ARGS) > 1 else "roofpool"
WIDTH = int(ARGS[2]) if len(ARGS) > 2 else 1536
SAMPLES = int(ARGS[3]) if len(ARGS) > 3 else 24
THREADS = int(ARGS[4]) if len(ARGS) > 4 else 6
assert SCENE in ("roofpool", "lobby", "club"), SCENE

REPO = os.path.dirname(os.path.dirname(HERE))
RB = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "rainbow")
CITY = os.path.join(RB, "city.json")
QUARTER = os.path.join(RB, "quarter.json")

# ---------------------------------------------------------------- the stage's numbers (stage.js)
G = math.radians(-10)                 # GRID_ANGLE: lot 111 turned 10° east of north; the site group turns by it
PLOT_H = 1.2
LOT_OUTLINE = [(-30.7, 68.7), (-29.5, -71.7), (19.3, -71.1), (30.7, -61.4), (30.3, 46.6), (22.6, 65.3), (10.1, 75.8)]
TOWER = dict(cx=13.2, cz=-44.1, rot=math.radians(98), A=16.5, B=10.8, y0=7.2, fh=3.75, floors=39)
TOWER["roof"] = TOWER["y0"] + TOWER["floors"] * TOWER["fh"]
BLOCK_W = 12.5
BLOCKS = [
    dict(p0=(-18.5, -62), p1=(-13.5, -53), p2=(-18.5, -44), floors=9, ph=0.3),
    dict(p0=(-18.5, -23.3), p1=(-13.5, -14.3), p2=(-18.5, -5.3), floors=9, ph=1.7),
    dict(p0=(-18.5, 15.4), p1=(-13.5, 24.4), p2=(-18.5, 33.4), floors=9, ph=2.9),
    dict(p0=(-19.4, 60), p1=(-9.4, 55), p2=(0.6, 60), floors=9, ph=4.1),
    dict(p0=(21, -10), p1=(16, -1), p2=(21, 8), floors=9, ph=5.3),
    dict(p0=(21, 28.7), p1=(16, 37.7), p2=(21, 46.7), floors=9, ph=0.9),
]
COAST_X = -713.0
POOL_BLOCK = 5                        # the roof:5 pin
Y = PLOT_H

# ---------------------------------------------------------------- render setup (rainbow_interior.py's pipeline)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = SAMPLES
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.02
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 8
scene.cycles.diffuse_bounces = 4
scene.cycles.glossy_bounces = 3 if SCENE == "roofpool" else 8
scene.cycles.transmission_bounces = 8
scene.cycles.transparent_max_bounces = 32
scene.cycles.sample_clamp_indirect = 8.0
scene.render.resolution_x = WIDTH
scene.render.resolution_y = WIDTH // 2
scene.render.resolution_percentage = 100
scene.render.threads_mode = "FIXED"     # always: other agents render on this machine too
scene.render.threads = max(1, THREADS)
scene.render.image_settings.file_format = "PNG"
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = {"roofpool": -1.9, "lobby": -1.05, "club": -1.0}[SCENE]

# every object of the site is built in the stage's grid frame (Blender x = stage x, Blender y = -stage z) and parented to
# this empty, which turns the grid 10° as the stage's site group does (site.rotation.y = GRID_ANGLE)
SITE = bpy.data.objects.new("site", None)
bpy.context.collection.objects.link(SITE)
SITE.rotation_euler = (0, 0, G)


# ---------------------------------------------------------------- materials
def _p(m):
    return m.node_tree.nodes["Principled BSDF"]


def mat(name, color, rough=0.5, metal=0.0, alpha=1.0, emission=None, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = _p(m)
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
    if emission:
        b.inputs["Emission Color"].default_value = (*emission[0], 1)
        b.inputs["Emission Strength"].default_value = emission[1]
    if coat:
        b.inputs["Coat Weight"].default_value = coat
    return m


def add_noise_bump(m, scale=40.0, strength=0.08, detail=4.0):
    nt = m.node_tree
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = scale; nz.inputs["Detail"].default_value = detail
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = strength
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], _p(m).inputs["Normal"])
    return m


def vary(m, amount=0.08, scale=0.6):
    """a soft cloudy variation of the base colour (render, plaster, concrete): no surface is one flat value"""
    nt = m.node_tree
    b = _p(m)
    base = tuple(b.inputs["Base Color"].default_value)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = scale; nz.inputs["Detail"].default_value = 6.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*[c * (1 - amount) for c in base[:3]], 1)
    ramp.color_ramp.elements[1].color = (*[min(1, c * (1 + amount * 0.6)) for c in base[:3]], 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    return m


def glass_mat(name="glass", tint=(0.94, 0.97, 0.97)):
    """thin clear glass (rainbow_interior.py): a clear sheet with a Fresnel reflection and no refraction, transparent to
    shadow rays, so the sky and the sun light the room without noise and nothing seen edge-on turns black"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    lp = nt.nodes.new("ShaderNodeLightPath")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); tr.inputs["Color"].default_value = (*tint, 1)
    gl = nt.nodes.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.02
    fr = nt.nodes.new("ShaderNodeFresnel")
    # the Fresnel node takes 1/IOR on a back face, so a ray inside a thin glass sheet (a closed pane, or a ribbon seen from
    # its back) is totally reflected at grazing angles and bounces until it dies into black: feed it 1/1.5 on back faces,
    # so both faces reflect as glass does from the air
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ior = nt.nodes.new("ShaderNodeMath"); ior.operation = "MULTIPLY_ADD"
    nt.links.new(geo.outputs["Backfacing"], ior.inputs[0])
    ior.inputs[1].default_value = 1 / 1.5 - 1.5
    ior.inputs[2].default_value = 1.5
    nt.links.new(ior.outputs[0], fr.inputs["IOR"])
    face = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(fr.outputs[0], face.inputs[0]); nt.links.new(tr.outputs[0], face.inputs[1]); nt.links.new(gl.outputs[0], face.inputs[2])
    shadow = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Shadow Ray"], mix.inputs[0]); nt.links.new(face.outputs[0], mix.inputs[1]); nt.links.new(shadow.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    return m


def facade_glass(name="facade-glass", c1=(0.045, 0.058, 0.068), c2=(0.075, 0.082, 0.088)):
    """the buildings' own glass seen from outside: dark, reflective, in panels (UV u = panels, v = floors) with slim dark
    frames at every panel and floor line and a slight tone change from pane to pane (curtains, rooms)"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = _p(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.0
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = 1.0
    br.inputs["Row Height"].default_value = 1.0
    br.inputs["Mortar Size"].default_value = 0.022
    br.inputs["Mortar Smooth"].default_value = 0.1
    br.inputs["Bias"].default_value = 0.0
    br.inputs["Color1"].default_value = (*c1, 1)
    br.inputs["Color2"].default_value = (*c2, 1)
    br.inputs["Mortar"].default_value = (0.035, 0.035, 0.034, 1)
    nt.links.new(tc.outputs["UV"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    rmix = nt.nodes.new("ShaderNodeMix"); rmix.data_type = "FLOAT"
    rmix.inputs[2].default_value = 0.035; rmix.inputs[3].default_value = 0.45
    nt.links.new(br.outputs["Fac"], rmix.inputs[0]); nt.links.new(rmix.outputs[0], b.inputs["Roughness"])
    b.inputs["IOR"].default_value = 1.52
    b.inputs["Specular IOR Level"].default_value = 1.0
    b.inputs["Coat Weight"].default_value = 0.6
    b.inputs["Coat Roughness"].default_value = 0.02
    return m


def water_mat(name="water", tint=(0.80, 0.95, 0.94), scale=1.4, strength=0.10):
    """pool water: a refracting surface (IOR 1.333) that reflects the sky by Fresnel, a gentle wave bump, and clear to
    shadow rays so the sun still lights the pool's tiles (no caustics to wait for)"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    w1 = nt.nodes.new("ShaderNodeTexNoise"); w1.inputs["Scale"].default_value = scale; w1.inputs["Detail"].default_value = 3.0
    w2 = nt.nodes.new("ShaderNodeTexWave"); w2.inputs["Scale"].default_value = scale * 0.9; w2.inputs["Distortion"].default_value = 6.0
    w2.inputs["Detail"].default_value = 3.0
    nt.links.new(tc.outputs["Object"], w1.inputs["Vector"]); nt.links.new(tc.outputs["Object"], w2.inputs["Vector"])
    add = nt.nodes.new("ShaderNodeMath"); add.operation = "ADD"
    nt.links.new(w1.outputs["Fac"], add.inputs[0]); nt.links.new(w2.outputs["Fac"], add.inputs[1])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = strength; bump.inputs["Distance"].default_value = 0.02
    nt.links.new(add.outputs[0], bump.inputs["Height"])
    gl = nt.nodes.new("ShaderNodeBsdfGlass")
    gl.inputs["Color"].default_value = (*tint, 1); gl.inputs["Roughness"].default_value = 0.015; gl.inputs["IOR"].default_value = 1.333
    nt.links.new(bump.outputs["Normal"], gl.inputs["Normal"])
    lp = nt.nodes.new("ShaderNodeLightPath")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); tr.inputs["Color"].default_value = (*tint, 1)
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Shadow Ray"], mix.inputs[0]); nt.links.new(gl.outputs[0], mix.inputs[1]); nt.links.new(tr.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    return m


def tile_mat(name, c1, c2, mortar, size=0.05, rough=0.2, obj=True):
    """small mosaic or large-format tiles: a brick grid (no offset) with a little tone change from tile to tile"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = _p(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.0
    br.inputs["Scale"].default_value = 1.0 / size
    br.inputs["Brick Width"].default_value = 1.0
    br.inputs["Row Height"].default_value = 1.0
    br.inputs["Mortar Size"].default_value = 0.06
    br.inputs["Color1"].default_value = (*c1, 1); br.inputs["Color2"].default_value = (*c2, 1)
    br.inputs["Mortar"].default_value = (*mortar, 1)
    nt.links.new(tc.outputs["Object" if obj else "UV"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    return m


def boxmap(m):
    """tiles on every face: a brick pattern fed by object coordinates projected on the face's dominant plane (the Brick
    texture is 2D, so on a wall plain object x, y would draw stripes)"""
    nt = m.node_tree
    for node in list(nt.nodes):
        if node.bl_idname != "ShaderNodeTexBrick":
            continue
        lk = next((l for l in nt.links if l.to_socket == node.inputs["Vector"]), None)
        if lk is None or lk.from_socket.name != "Object":
            continue
        tc = lk.from_node
        sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sp.inputs[0])
        sn = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Normal"], sn.inputs[0])

        def ab(sock):
            n_ = nt.nodes.new("ShaderNodeMath"); n_.operation = "ABSOLUTE"; nt.links.new(sock, n_.inputs[0])
            return n_.outputs[0]

        def gt(a_, b_):
            n_ = nt.nodes.new("ShaderNodeMath"); n_.operation = "GREATER_THAN"
            nt.links.new(a_, n_.inputs[0])
            if isinstance(b_, float):
                n_.inputs[1].default_value = b_
            else:
                nt.links.new(b_, n_.inputs[1])
            return n_.outputs[0]

        def comb(u, v):
            n_ = nt.nodes.new("ShaderNodeCombineXYZ"); nt.links.new(u, n_.inputs[0]); nt.links.new(v, n_.inputs[1])
            return n_.outputs[0]

        ax, ay, az = ab(sn.outputs[0]), ab(sn.outputs[1]), ab(sn.outputs[2])
        side = nt.nodes.new("ShaderNodeMix"); side.data_type = "VECTOR"
        nt.links.new(gt(ax, ay), side.inputs[0])
        nt.links.new(comb(sp.outputs[0], sp.outputs[2]), side.inputs[4]); nt.links.new(comb(sp.outputs[1], sp.outputs[2]), side.inputs[5])
        top = nt.nodes.new("ShaderNodeMix"); top.data_type = "VECTOR"
        nt.links.new(gt(az, 0.5), top.inputs[0])
        nt.links.new(side.outputs[1], top.inputs[4]); nt.links.new(comb(sp.outputs[0], sp.outputs[1]), top.inputs[5])
        nt.links.new(top.outputs[1], node.inputs["Vector"])
    return m


def stone_tiles(name, color, tile=(1.2, 0.6), joint=0.004, spread=0.07, rough=0.32, bond=0.0, cloud=1.4):
    """honed stone or porcelain in large tiles: a cloudy tone, each tile a little lighter or darker, recessed joints that
    catch the light, a soft change of sheen (box-mapped, so walls get tiles too)"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = _p(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = cloud; nz.inputs["Detail"].default_value = 8.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*[c * 0.9 for c in color], 1)
    ramp.color_ramp.elements[1].color = (*[min(1, c * 1.08) for c in color], 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = bond
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = tile[0]
    br.inputs["Row Height"].default_value = tile[1]
    br.inputs["Mortar Size"].default_value = joint
    br.inputs["Mortar Smooth"].default_value = 0.3
    br.inputs["Bias"].default_value = 0.0
    br.inputs["Color1"].default_value = (1, 1, 1, 1)
    br.inputs["Color2"].default_value = (1 - spread, 1 - spread * 1.05, 1 - spread * 1.1, 1)
    br.inputs["Mortar"].default_value = (0.55, 0.53, 0.5, 1)
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    mul = nt.nodes.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"; mul.inputs[0].default_value = 1.0
    nt.links.new(ramp.outputs["Color"], mul.inputs[6]); nt.links.new(br.outputs["Color"], mul.inputs[7])
    nt.links.new(mul.outputs[2], b.inputs["Base Color"])
    inv = nt.nodes.new("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1.0
    nt.links.new(br.outputs["Fac"], inv.inputs[1])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.35; bump.inputs["Distance"].default_value = 0.002
    nt.links.new(inv.outputs[0], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    rr = nt.nodes.new("ShaderNodeMapRange")
    rr.inputs["To Min"].default_value = rough * 0.8; rr.inputs["To Max"].default_value = rough * 1.25
    nt.links.new(nz.outputs["Fac"], rr.inputs["Value"])
    rj = nt.nodes.new("ShaderNodeMix"); rj.data_type = "FLOAT"
    nt.links.new(br.outputs["Fac"], rj.inputs[0]); nt.links.new(rr.outputs["Result"], rj.inputs[2]); rj.inputs[3].default_value = 0.8
    nt.links.new(rj.outputs[0], b.inputs["Roughness"])
    return boxmap(m)


def foliage_mat(name, c0=(0.035, 0.075, 0.025), c1=(0.13, 0.20, 0.06), grey=0.0):
    """leaves: clumps (Voronoi) and fine noise, a strong bump so a canopy reads as leaves and not as a ball"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = _p(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 9.0
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 26.0; nz.inputs["Detail"].default_value = 6.0
    nt.links.new(tc.outputs["Object"], vo.inputs["Vector"]); nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    if grey:
        c0 = tuple(c * (1 - grey) + 0.12 * grey for c in c0); c1 = tuple(c * (1 - grey) + 0.30 * grey for c in c1)
    ramp.color_ramp.elements[0].color = (*c0, 1); ramp.color_ramp.elements[1].color = (*c1, 1)
    mixf = nt.nodes.new("ShaderNodeMix"); mixf.data_type = "FLOAT"; mixf.inputs[0].default_value = 0.5
    nt.links.new(vo.outputs["Distance"], mixf.inputs[2]); nt.links.new(nz.outputs["Fac"], mixf.inputs[3])
    nt.links.new(mixf.outputs[0], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.9; bump.inputs["Distance"].default_value = 0.05
    nt.links.new(mixf.outputs[0], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.6
    b.inputs["Subsurface Weight"].default_value = 0.15
    return m


def leaf_mat(name, c0, c1, trans=0.3):
    """a leaf: tone drifting from leaf to leaf, a soft sheen, and some light through it when the sun is behind"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = _p(m)
    out = nt.nodes["Material Output"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.2; nz.inputs["Detail"].default_value = 4.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*c0, 1); ramp.color_ramp.elements[1].color = (*c1, 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.42
    b.inputs["Specular IOR Level"].default_value = 0.45
    tl = nt.nodes.new("ShaderNodeBsdfTranslucent")
    nt.links.new(ramp.outputs["Color"], tl.inputs["Color"])
    mix = nt.nodes.new("ShaderNodeMixShader"); mix.inputs[0].default_value = trans
    nt.links.new(b.outputs[0], mix.inputs[1]); nt.links.new(tl.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    return m


def hazed(m, haze=(0.66, 0.69, 0.72), dist=3200.0):
    """aerial perspective (rainbow_interior.py): the base colour drifts to the haze with distance from the camera"""
    nt = m.node_tree
    b = _p(m)
    src = None
    for l in nt.links:
        if l.to_socket == b.inputs["Base Color"]:
            src = l.from_socket
    base = tuple(b.inputs["Base Color"].default_value)
    cam = nt.nodes.new("ShaderNodeCameraData")
    div = nt.nodes.new("ShaderNodeMath"); div.operation = "DIVIDE"; div.inputs[1].default_value = -dist
    ex = nt.nodes.new("ShaderNodeMath"); ex.operation = "EXPONENT"
    inv = nt.nodes.new("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1.0
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
    if src is not None:
        nt.links.new(src, mix.inputs[6])
    else:
        mix.inputs[6].default_value = base
    mix.inputs[7].default_value = (*haze, 1)
    nt.links.new(cam.outputs["View Distance"], div.inputs[0]); nt.links.new(div.outputs[0], ex.inputs[0])
    nt.links.new(ex.outputs[0], inv.inputs[1]); nt.links.new(inv.outputs[0], mix.inputs[0])
    nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    return m


M = {
    "white": add_noise_bump(vary(mat("render-white", (0.86, 0.85, 0.82), 0.62), 0.05, 0.35), 60.0, 0.03),
    "deckband": vary(mat("balcony-deck", (0.50, 0.46, 0.41), 0.55), 0.1, 1.2),
    "facade": facade_glass(),
    "glass": glass_mat(),
    "rail-glass": glass_mat("rail-glass", (0.90, 0.96, 0.94)),
    "frame": mat("frame", (0.05, 0.05, 0.05), 0.35, 0.7),
    "bronze": mat("bronze", (0.36, 0.25, 0.16), 0.32, 1.0),
    "steel": mat("steel", (0.62, 0.62, 0.62), 0.22, 1.0),
    "paving": stone_tiles("paving", (0.50, 0.48, 0.44), (0.6, 0.6), 0.006, 0.08, 0.6, 0.0, 0.3),
    "lawn": add_noise_bump(vary(mat("lawn", (0.10, 0.17, 0.05), 0.9), 0.3, 0.9), 300.0, 0.3),
    "soil": mat("soil", (0.07, 0.05, 0.035), 0.95),
    "bark": add_noise_bump(mat("bark", (0.16, 0.13, 0.10), 0.85), 30.0, 0.3),
    "tree": foliage_mat("tree"),
    "tree2": foliage_mat("tree2", (0.05, 0.08, 0.03), (0.17, 0.22, 0.09)),
    "olive": foliage_mat("olive", (0.08, 0.10, 0.07), (0.25, 0.29, 0.20)),
    "leaf": leaf_mat("leaf", (0.03, 0.07, 0.02), (0.11, 0.19, 0.05)),
    "leaf-core": mat("leaf-core", (0.02, 0.035, 0.012), 0.8),
    "leaf2": leaf_mat("leaf2", (0.05, 0.08, 0.025), (0.16, 0.21, 0.07)),
    "leaf-olive": leaf_mat("leaf-olive", (0.07, 0.09, 0.06), (0.22, 0.26, 0.17), 0.2),
    "leaf-fig": leaf_mat("leaf-fig", (0.02, 0.06, 0.015), (0.07, 0.15, 0.04), 0.2),
    "roofgarden": add_noise_bump(vary(mat("roof-garden", (0.09, 0.14, 0.05), 0.9), 0.3, 1.5), 200.0, 0.4),
    "ground": mat("ground", (0.13, 0.12, 0.105), 0.95),
    "street": mat("street", (0.075, 0.075, 0.075), 0.9),
    "plate": mat("plate", (0.30, 0.285, 0.26), 0.9),
    "park": mat("park", (0.06, 0.09, 0.045), 0.95),
    "sand": mat("sand", (0.40, 0.35, 0.27), 0.95),
    "sea": mat("sea", (0.035, 0.15, 0.22), 0.11),
    "city": mat("city", (0.86, 0.82, 0.74), 0.8),
    "quarter": mat("quarter", (0.93, 0.91, 0.86), 0.7, alpha=0.45),
    "pool-water": water_mat(),
}
_p(M["sea"]).inputs["IOR"].default_value = 1.33
for _k in ("ground", "street", "plate", "park", "sand", "city"):
    hazed(M[_k])


# ---------------------------------------------------------------- geometry: the stage's 2D helpers (x grid east, z grid south)
def set_normals(pts):
    n = len(pts)
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    sgn = 1 if area > 0 else -1
    for i in range(n):
        a, b = pts[(i - 1) % n], pts[(i + 1) % n]
        tx, tz = b[0] - a[0], b[1] - a[1]
        l = math.hypot(tx, tz) or 1
        pts[i][3] = sgn * tz / l
        pts[i][4] = -sgn * tx / l
    return pts


def resample(P, n):
    """a closed polyline resampled to n points by arc length: [x, z, s, nx, nz], s = arc position from P[0]"""
    Mn = len(P)
    seg = [math.dist(P[i], P[(i + 1) % Mn]) for i in range(Mn)]
    cum = [0.0]
    for L_ in seg:
        cum.append(cum[-1] + L_)
    total = cum[-1]
    pts, j = [], 0
    for k in range(n):
        t = k / n * total
        while j < Mn - 1 and cum[j + 1] < t:
            j += 1
        f = (t - cum[j]) / seg[j] if seg[j] > 0 else 0
        a, b = P[j], P[(j + 1) % Mn]
        pts.append([a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, t / total, 0.0, 0.0])
    return set_normals(pts)


def offset(pts, d):
    return [[p[0] + p[3] * d, p[1] + p[4] * d, p[2], p[3], p[4]] for p in pts]


def ellipse_poly(A, B, cx, cz, rot, n=720):
    c, s = math.cos(rot), math.sin(rot)
    return [(cx + A * math.cos(t) * c - B * math.sin(t) * s, cz + A * math.cos(t) * s + B * math.sin(t) * c)
            for t in (i / n * 2 * math.pi for i in range(n))]


def qbez(bk, t):
    u = 1 - t
    p0, p1, p2 = bk["p0"], bk["p1"], bk["p2"]
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def qtan(bk, t):
    u = 1 - t
    p0, p1, p2 = bk["p0"], bk["p1"], bk["p2"]
    tx, tz = 2 * u * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]), 2 * u * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
    l = math.hypot(tx, tz) or 1
    return tx / l, tz / l


def capsule_poly(bk, w, n=40):
    C = [qbez(bk, i / n) for i in range(n + 1)]
    Tn = [qtan(bk, i / n) for i in range(n + 1)]
    h = w / 2
    P = [(C[i][0] - Tn[i][1] * h, C[i][1] + Tn[i][0] * h) for i in range(n + 1)]
    e, t = C[n], Tn[n]
    a0 = math.atan2(t[0], -t[1])
    P += [(e[0] + math.cos(a0 - k / 18 * math.pi) * h, e[1] + math.sin(a0 - k / 18 * math.pi) * h) for k in range(1, 18)]
    P += [(C[i][0] + Tn[i][1] * h, C[i][1] - Tn[i][0] * h) for i in range(n, -1, -1)]
    e, t = C[0], Tn[0]
    b0 = math.atan2(-t[0], t[1])
    P += [(e[0] + math.cos(b0 - k / 18 * math.pi) * h, e[1] + math.sin(b0 - k / 18 * math.pi) * h) for k in range(1, 18)]
    return P


def round_rect(cx, cz, w, d, r, seg=10):
    P = []
    hx, hz = w / 2 - r, d / 2 - r
    for ox, oz, a0 in ((hx, hz, 0), (-hx, hz, 90), (-hx, -hz, 180), (hx, -hz, 270)):
        for k in range(seg + 1):
            a = math.radians(a0 + k / seg * 90)
            P.append((cx + ox + math.cos(a) * r, cz + oz + math.sin(a) * r))
    return P


def rotate_poly(P, cx, cz, rot):
    c, s = math.cos(rot), math.sin(rot)
    return [(cx + (x - cx) * c - (z - cz) * s, cz + (x - cx) * s + (z - cz) * c) for x, z in P]


def ease_corners(P, d, seg=6):
    out = []
    n = len(P)
    for i in range(n):
        a, b, c = P[(i - 1) % n], P[i], P[(i + 1) % n]
        la, lc = math.dist(a, b), math.dist(c, b)
        ka, kc = min(d, la * 0.4) / la, min(d, lc * 0.4) / lc
        p0 = (b[0] + (a[0] - b[0]) * ka, b[1] + (a[1] - b[1]) * ka)
        p2 = (b[0] + (c[0] - b[0]) * kc, b[1] + (c[1] - b[1]) * kc)
        for k in range(seg + 1):
            t = k / seg
            u = 1 - t
            out.append((u * u * p0[0] + 2 * u * t * b[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * b[1] + t * t * p2[1]))
    return out


def dedupe(P, eps=1e-3):
    out = []
    for p in P:
        if not out or math.dist(out[-1][:2], p[:2]) > eps:
            out.append(p)
    if len(out) > 2 and math.dist(out[0][:2], out[-1][:2]) <= eps:
        out.pop()
    return out


# ---------------------------------------------------------------- geometry: meshes (stage-local points -> the grid frame)
def link(ob):
    bpy.context.collection.objects.link(ob)
    ob.parent = SITE
    return ob


def add_mesh(name, verts, faces, material, smooth=False, uvs=None, mats=None, sharp=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    if uvs is not None:
        uvl = me.uv_layers.new(name="UVMap")
        for poly in me.polygons:
            for li in poly.loop_indices:
                uvl.data[li].uv = uvs[me.loops[li].vertex_index]
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material)
    for extra in (mats or []):
        ob.data.materials.append(extra)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
        if sharp:
            try:
                me.set_sharp_from_angle(angle=math.radians(sharp))
            except Exception:
                pass
    return link(ob)


def fix_normals(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(ob.data)
    bm.free()
    return ob


def prism_l(name, poly, z0, z1, material, top=True, bottom=True):
    """a vertical prism from a stage-local polygon"""
    poly = dedupe(list(poly))
    bm = bmesh.new()
    vs0 = [bm.verts.new((x, -z, z0)) for x, z in poly]
    vs1 = [bm.verts.new((x, -z, z1)) for x, z in poly]
    n = len(poly)
    for vs, on in ((vs0[::-1], bottom), (vs1, top)):
        if on:
            try:
                bm.faces.new(vs)
            except ValueError:
                pass
    for i in range(n):
        j = (i + 1) % n
        try:
            bm.faces.new((vs0[i], vs0[j], vs1[j], vs1[i]))
        except ValueError:
            pass
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material)
    return link(ob)


def box(name, cx, cy, cz, sx, sy, sz, material, rot=0.0):
    """rainbow_interior.py's box, in the grid frame's Blender coordinates (cx, cy = stage x, -z)"""
    c, s = math.cos(rot), math.sin(rot)
    pts = [(-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)]
    poly = [(cx + x * c - y * s, -(cy + x * s + y * c)) for x, y in pts]
    return prism_l(name, poly, cz - sz / 2, cz + sz / 2, material)


def obox(name, loc, size, material, yaw=0.0, tilt=0.0, bev=0.0, segs=3):
    """a box built at the origin and placed by its object transform (for tilted parts: backrests, consoles)"""
    sx, sy, sz = size
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material)
    ob.location = loc
    ob.rotation_euler = (0, tilt, yaw)
    link(ob)
    return SK.smooth_bevel(ob, bev, segs) if bev else ob


def cyl(name, x, y, z0, z1, r, material, seg=32, r2=None):
    """a cylinder (or a cone frustum with r2) in the grid frame's Blender coordinates"""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=z1 - z0)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material)
    ob.location = (x, y, (z0 + z1) / 2)
    for p in me.polygons:
        p.use_smooth = True
    try:
        me.set_sharp_from_angle(angle=math.radians(50))
    except Exception:
        pass
    return link(ob)


def ball(name, x, y, z, r, material, seg=16, scale=(1, 1, 1)):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2 if seg <= 16 else 3, radius=r)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material)
    ob.location = (x, y, z)
    ob.scale = scale
    for p in me.polygons:
        p.use_smooth = True
    return link(ob)


def loop_wall(name, pts, y0, y1, material, panel=1.5, row=3.75, v0=0.0):
    """a vertical single-sided ribbon along a closed loop, with UVs in panels (u) and floors (v)"""
    n = len(pts)
    verts, faces, uvs = [], [], []
    acc = 0.0
    for i in range(n + 1):
        p = pts[i % n]
        if i:
            acc += math.dist(pts[i - 1][:2], p[:2])
        verts += [(p[0], -p[1], y0), (p[0], -p[1], y1)]
        uvs += [(acc / panel, v0), (acc / panel, v0 + (y1 - y0) / row)]
        if i:
            a = 2 * (i - 1)
            faces.append((a, a + 2, a + 3, a + 1))
    return add_mesh(name, verts, faces, material, smooth=True, uvs=uvs)


def cap(name, pts, y, material, thick=0.0):
    poly = [(p[0], p[1]) for p in pts]
    if thick:
        return prism_l(name, poly, y - thick, y, material)
    poly = dedupe(poly)
    bm = bmesh.new()
    vs = [bm.verts.new((x, -z, y)) for x, z in poly]
    try:
        bm.faces.new(vs)
    except ValueError:
        pass
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material)
    return link(ob)


def band(name, pts, y, depth, Hp, Ts, tp, rb, inset=0.3, floor=True, white=None, deck=None):
    """stage.js addBand: a floor band swept along a loop, depth(s) metres out from the glass line: the balcony floor,
    a rounded solid parapet Hp high and tp thick, the slab edge Ts deep with a rounded soffit corner rb"""
    white = white or M["white"]
    deck = deck or M["deckband"]
    n = len(pts)
    out = set_normals([[p[0] + p[3] * depth(p[2]), p[1] + p[4] * depth(p[2]), p[2], 0.0, 0.0] for p in pts])
    rt = tp / 2
    strip2 = [("o", -tp, 0.0)]
    for k in range(7):
        th = math.pi * (1 - k / 6)
        strip2.append(("o", -rt + rt * math.cos(th), Hp - rt + rt * math.sin(th)))
    for k in range(5):
        ph_ = -k / 4 * math.pi / 2
        strip2.append(("o", -rb + rb * math.cos(ph_), -Ts + rb + rb * math.sin(ph_)))
    strip2.append(("i", 0.0, -Ts))
    strips = ([[("i", 0.0, 0.0), ("o", -tp, 0.0)]] if floor else []) + [strip2]
    verts, faces, fmat = [], [], []
    for si, strip in enumerate(strips):
        m_ = len(strip)
        base = len(verts)
        for i in range(n):
            p, o = pts[i], out[i]
            for k, u, v in strip:
                if k == "i":
                    verts.append((p[0] - p[3] * inset, -(p[1] - p[4] * inset), y + v))
                else:
                    verts.append((o[0] + o[3] * u, -(o[1] + o[4] * u), y + v))
        for i in range(n):
            i2 = (i + 1) % n
            for j in range(m_ - 1):
                faces.append((base + i * m_ + j, base + i2 * m_ + j, base + i2 * m_ + j + 1, base + i * m_ + j + 1))
                fmat.append(1 if (floor and si == 0) else 0)
    ob = add_mesh(name, verts, faces, white, smooth=True, mats=[deck], sharp=48)
    for poly, mi in zip(ob.data.polygons, fmat):
        poly.material_index = mi
    return ob, out


def bevelled(ob, w=0.01, segs=2):
    return SK.smooth_bevel(ob, w, segs)


# ---------------------------------------------------------------- the world outside (rainbow_interior.py, in the grid frame)
FAR = 40000
prism_l("sea", [(COAST_X - FAR, -FAR), (COAST_X, -FAR), (COAST_X, FAR), (COAST_X - FAR, FAR)], -0.35, -0.3, M["sea"])
_p(M["sea"]).inputs["Roughness"].default_value = 0.09
add_noise_bump(M["sea"], 0.35, 0.05, 3.0)
prism_l("land", [(COAST_X, -FAR), (FAR, -FAR), (FAR, FAR), (COAST_X, FAR)], -0.05, 0.0, M["ground"], bottom=False)
prism_l("beach", [(COAST_X, -FAR), (COAST_X + 45, -FAR), (COAST_X + 45, FAR), (COAST_X, FAR)], 0.0, 0.05, M["sand"], bottom=False)
prism_l("coastal-park", [(COAST_X + 45, -FAR), (COAST_X + 120, -FAR), (COAST_X + 120, FAR), (COAST_X + 45, FAR)], 0.0, 0.08, M["park"], bottom=False)

city = json.load(open(CITY, encoding="utf-8"))
bm = bmesh.new()
for b in city.get("b", []):
    h = float(b[0])
    pts = b[3:]
    poly = [(pts[i], -pts[i + 1]) for i in range(0, len(pts) - 1, 2)]
    if len(poly) < 3 or h <= 0:
        continue
    v0 = [bm.verts.new((x, y, 0)) for x, y in poly]
    v1 = [bm.verts.new((x, y, h)) for x, y in poly]
    try:
        bm.faces.new(v1)
    except ValueError:
        pass
    for i in range(len(poly)):
        j = (i + 1) % len(poly)
        try:
            bm.faces.new((v0[i], v0[j], v1[j], v1[i]))
        except ValueError:
            pass
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
me = bpy.data.meshes.new("city")
bm.to_mesh(me)
bm.free()
ob = bpy.data.objects.new("city", me)
ob.data.materials.append(M["city"])
link(ob)
# the Sde Dov plan's lots as plates (the stage's lots), the planned park in green
for i, l in enumerate(city.get("lots", [])):
    pts = l[2:]
    poly = [(pts[k], pts[k + 1]) for k in range(0, len(pts) - 1, 2)]
    if len(poly) >= 3:
        prism_l("lot-%d" % i, poly, 0.0, 0.2 if l[0] == "park" else 0.3, M["park"] if l[0] == "park" else M["plate"], bottom=False)

# our other projects in the quarter: the stage's schematic masses (pale, translucent), in the grid frame
q = json.load(open(QUARTER, encoding="utf-8"))
cg, sg = math.cos(G), math.sin(G)
for p in q.get("projects", []):
    X, Z = float(p["x"]), float(p["z"])
    lx, lz = X * cg - Z * sg, X * sg + Z * cg
    fl = float(p.get("floors") or 10)
    h = max(12.0, fl * 3.3 + 4)
    if fl >= 20:
        prism_l("q-%s" % p["id"], [(lx - 13, lz - 13), (lx + 13, lz - 13), (lx + 13, lz + 13), (lx - 13, lz + 13)], 0.55, h, M["quarter"])
        prism_l("q-%s-base" % p["id"], [(lx - 26, lz + 9), (lx + 18, lz + 9), (lx + 18, lz + 23), (lx - 26, lz + 23)], 0.55, 14, M["quarter"])
    else:
        prism_l("q-%s" % p["id"], [(lx - 22, lz - 13), (lx + 22, lz - 13), (lx + 22, lz + 13), (lx - 22, lz + 13)], 0.55, h, M["quarter"])

# ---------------------------------------------------------------- the lot: the courtyard deck, lawns, trees
lot = ease_corners(LOT_OUTLINE, 3.2, 8)
prism_l("lot-deck", lot, 0.0, PLOT_H, M["paving"])
for i, poly in enumerate((round_rect(1, 8, 14, 34, 5, 8), round_rect(1, 38, 14, 12, 4, 8), round_rect(-3.5, -49, 8, 14, 3, 8),
                          rotate_poly(round_rect(1, -16, 12, 5, 2.5, 6), 1, -16, math.radians(18)))):
    prism_l("lawn-%d" % i, poly, Y, Y + 0.18, M["lawn"])
    band("lawn-kerb-%d" % i, resample(poly, 120), Y + 0.18, lambda s: 0.12, 0.05, 0.18, 0.12, 0.02, inset=0.0, floor=False,
         white=M["paving"])
rnd = random.Random(11)


def rod(name, p0, p1, r0, r1, material, seg=8):
    """a tapered cylinder from p0 to p1 (grid frame Blender coordinates)"""
    v = Vector(p1) - Vector(p0)
    L = v.length
    bm_ = bmesh.new()
    bmesh.ops.create_cone(bm_, cap_ends=True, cap_tris=False, segments=seg, radius1=r0, radius2=r1, depth=L)
    me_ = bpy.data.meshes.new(name)
    bm_.to_mesh(me_)
    bm_.free()
    ob_ = bpy.data.objects.new(name, me_)
    ob_.data.materials.append(material)
    ob_.location = (Vector(p0) + Vector(p1)) / 2
    ob_.rotation_euler = v.to_track_quat("Z", "Y").to_euler()
    for p_ in me_.polygons:
        p_.use_smooth = True
    return link(ob_)


def tree(name, x, z, y, r, material=None, trunk=None, fine=False, crown=0.8, leaf=None):
    """a tree (the stage's canopy radius r): a leaning trunk, branches spreading up into the crown, and a crown of real
    leaves, thousands of small leaf blades in clusters on an uneven shell, about as much leaf as a tree carries (a leaf
    area of 2-3 times the crown's footprint), with a darker dense core. fine: small leaves for plants at arm's length"""
    lm = leaf or (M["leaf"] if rnd.random() < 0.6 else M["leaf2"])
    if material is M.get("olive"):
        lm = M["leaf-olive"]
    elif material is M.get("tree") and fine:
        lm = M["leaf-fig"]
    material = material or M["tree"]
    bark = trunk or M["bark"]
    bx, by = x, -z
    h = r * 1.25
    rt = 0.045 + r * 0.04
    top = (bx + rnd.uniform(-0.08, 0.08) * r, by + rnd.uniform(-0.08, 0.08) * r, y + h)
    rod(name + "-trunk", (bx, by, y), top, rt, rt * 0.7, bark)
    cc = (top[0], top[1], y + h + r * 0.62)
    nb = 4 + rnd.randint(0, 2)
    for k in range(nb):
        az = k / nb * math.tau + rnd.uniform(-0.4, 0.4)
        el = math.radians(rnd.uniform(38, 62))
        L = r * rnd.uniform(0.65, 0.95)
        p1 = (top[0] + math.cos(az) * math.cos(el) * L, top[1] + math.sin(az) * math.cos(el) * L, top[2] - 0.1 * h + math.sin(el) * L)
        rod("%s-branch-%d" % (name, k), (top[0], top[1], top[2] - 0.1 * h), p1, rt * 0.55, rt * 0.18, bark, 6)
    if lm is M["leaf-olive"]:
        L, W = 0.075, 0.018
    elif fine:
        L, W = 0.16, 0.08
    else:
        L, W = 0.2, 0.1
    n_leaves = int(min(14000 if fine else 6500, math.pi * r * r * (2.4 if fine else 2.6) / (0.5 * L * W)))
    clusters = max(14, n_leaves // (80 if fine else 70))
    per = max(1, n_leaves // clusters)
    cl_r = r * (0.24 if fine else 0.3)
    verts, faces = [], []
    for c in range(clusters):
        u = rnd.uniform(-0.5, 1.0)
        th = rnd.random() * math.tau
        ring = math.sqrt(max(0.0, 1 - u * u))
        sh = 0.55 + 0.45 * math.sqrt(rnd.random())
        k0 = Vector((cc[0] + math.cos(th) * ring * r * sh, cc[1] + math.sin(th) * ring * r * sh, cc[2] + u * r * crown * sh))
        for l in range(per):
            dv = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1)))
            dv = dv.normalized() * cl_r * rnd.random() ** 0.5 if dv.length > 1e-6 else Vector((0, 0, 0))
            pnt = k0 + dv
            az = rnd.random() * math.tau
            pit = math.radians(rnd.uniform(-55, 40))
            t = Vector((math.cos(az) * math.cos(pit), math.sin(az) * math.cos(pit), math.sin(pit)))
            sd = t.cross(Vector((0, 0, 1)))
            if sd.length < 1e-3:
                sd = Vector((1, 0, 0))
            sd.normalize()
            roll = rnd.uniform(-0.7, 0.7)
            nrm = t.cross(sd)
            sd = sd * math.cos(roll) + nrm * math.sin(roll)
            ls = L * rnd.uniform(0.75, 1.2)
            i0 = len(verts)
            verts += [tuple(pnt - t * ls * 0.5), tuple(pnt - t * ls * 0.1 + sd * W * 0.5), tuple(pnt + t * ls * 0.5),
                      tuple(pnt - t * ls * 0.1 - sd * W * 0.5)]
            faces.append((i0, i0 + 1, i0 + 2, i0 + 3))
    me_ = bpy.data.meshes.new(name + "-leaves")
    me_.from_pydata(verts, [], faces)
    me_.update()
    ob_ = bpy.data.objects.new(name + "-leaves", me_)
    ob_.data.materials.append(lm)
    link(ob_)
    for i in range(0 if fine else 3):
        ball("%s-core-%d" % (name, i), cc[0] + rnd.uniform(-0.25, 0.25) * r, cc[1] + rnd.uniform(-0.25, 0.25) * r, cc[2] + rnd.uniform(-0.15, 0.2) * r,
             r * 0.45, M["leaf-core"], scale=(1, 1, 0.75))


for k, (x, z) in enumerate(((-6, -22), (8, -24), (-7, -3), (10, 2), (-7, 20), (10, 22), (-6, 44), (9, 47), (-5, -62), (1, -65),
                            (24, -24), (-20, 46), (12, 60))):
    tree("ctree-%d" % k, x, z, Y + 0.18, 2.1 + rnd.random() * 0.7)


def in_lot(x, z):
    c = False
    L = LOT_OUTLINE
    j = len(L) - 1
    for i in range(len(L)):
        (xi, zi), (xj, zj) = L[i], L[j]
        if (zi > z) != (zj > z) and x < (xj - xi) * (z - zi) / (zj - zi) + xi:
            c = not c
        j = i
    return c


for i in range(len(LOT_OUTLINE)):
    a, b = LOT_OUTLINE[i], LOT_OUTLINE[(i + 1) % len(LOT_OUTLINE)]
    dx, dz = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(dx, dz)
    if ln < 20:
        continue
    nx, nz = dz / ln, -dx / ln
    if in_lot((a[0] + b[0]) / 2 + nx, (a[1] + b[1]) / 2 + nz):
        nx, nz = -nx, -nz
    n = max(1, round((ln - 8) / 14))
    for k in range(n + 1):
        t = (4 + k * (ln - 8) / n) / ln
        tree("stree-%d-%d" % (i, k), a[0] + dx * t + nx * 4.5, a[1] + dz * t + nz * 4.5, 0.0, 1.7 + rnd.random() * 0.4)
    # the street and its pavement along this side of the lot
    px, pz = nx * 1.0, nz * 1.0
    prism_l("pavement-%d" % i, [(a[0], a[1]), (b[0], b[1]), (b[0] + nx * 7, b[1] + nz * 7), (a[0] + nx * 7, a[1] + nz * 7)],
            0.0, 0.15, M["paving"], bottom=False)
    prism_l("street-%d" % i, [(a[0] + nx * 7 - dx / ln * 12, a[1] + nz * 7 - dz / ln * 12), (b[0] + nx * 7 + dx / ln * 12, b[1] + nz * 7 + dz / ln * 12),
                              (b[0] + nx * 20 + dx / ln * 12, b[1] + nz * 20 + dz / ln * 12), (a[0] + nx * 20 - dx / ln * 12, a[1] + nz * 20 - dz / ln * 12)],
            0.0, 0.02, M["street"], bottom=False)

# ---------------------------------------------------------------- the tower (stage.js: ellipse, bands, lobby, penthouse, crown)
T_ = TOWER
tLoop = resample(ellipse_poly(T_["A"], T_["B"], T_["cx"], T_["cz"], T_["rot"]), 360)
tLobby = offset(tLoop, -2.2)
tPent = offset(tLoop, -1.3)
TOP = T_["floors"] - 3
CLEAR_LOBBY = SCENE == "lobby"
CLEAR_F1 = SCENE == "club"
loop_wall("tower-lobby-glass", tLobby, Y, T_["y0"], M["glass"] if CLEAR_LOBBY else M["facade"], 1.5, 6.0)
f1_top = T_["y0"] + T_["fh"] - 0.4
loop_wall("tower-glass-f1", tLoop, T_["y0"] - 0.5, f1_top, M["glass"] if CLEAR_F1 else M["facade"], 1.5, T_["fh"])
loop_wall("tower-glass", tLoop, f1_top, T_["y0"] + TOP * T_["fh"], M["facade"], 1.5, T_["fh"], (f1_top - T_["y0"] + 0.5) / T_["fh"])
loop_wall("tower-glass-pent", tPent, T_["y0"] + TOP * T_["fh"] - 0.5, T_["roof"], M["facade"], 1.5, T_["fh"])
cap("tower-ceiling-lobby", tLoop, T_["y0"] - 0.02, M["white"], thick=0.4)       # the base floor's slab, over the lobby
cap("tower-slab-f2", tLoop, T_["y0"] + T_["fh"] - 0.02, M["white"], thick=0.4)
for f in range(1, T_["floors"] + 1):
    y = T_["y0"] + (f - 1) * T_["fh"]
    ph = 0.4 + f * 0.16
    pent = f > TOP
    dmin, dmax = (2.4, 4.8) if pent else (0.7, 3.6)
    band("tower-band-%d" % f, tPent if pent else tLoop, y,
         lambda s, ph=ph, dmin=dmin, dmax=dmax: dmin + (dmax - dmin) * (0.5 + 0.5 * math.sin(2 * math.pi * 3 * s + ph)),
         1.05, 0.4, 0.24, 0.12)
band("tower-roof-parapet", tPent, T_["roof"], lambda s: 0.55, 1.2, 0.5, 0.3, 0.14)
cap("tower-roof", tPent, T_["roof"] + 0.02, M["white"])
crown = offset(tLoop, 0.6)
band("tower-crown", crown, T_["roof"] + 5.4, lambda s: 2.1, 0.3, 0.6, 0.3, 0.14, inset=0.0)
for k in range(8):
    p = crown[int(k / 8 * len(crown))]
    cyl("crown-post-%d" % k, p[0] + p[3] * 0.9, -(p[1] + p[4] * 0.9), T_["roof"], T_["roof"] + 5.2, 0.32, M["white"], 12)

# ---------------------------------------------------------------- the six boutique buildings
BLK = []
for bi, bk in enumerate(BLOCKS):
    lp = resample(capsule_poly(bk, BLOCK_W, 40), 220)
    ground0 = offset(lp, -1.0)
    top_in = offset(lp, -2.4)
    gh, fh, nF = 4.4, 3.2, bk["floors"]
    y_top = Y + gh + (nF - 2) * fh
    roofY = Y + gh + (nF - 1) * fh
    loop_wall("b%d-glass-ground" % bi, ground0, Y, Y + gh, M["facade"], 1.5, gh)
    loop_wall("b%d-glass" % bi, lp, Y + gh - 0.4, y_top, M["facade"], 1.5, fh, -0.4 / fh)
    loop_wall("b%d-glass-top" % bi, top_in, y_top - 0.4, roofY, M["facade"], 1.5, fh, -0.4 / fh)
    cap("b%d-slab-top" % bi, lp, y_top, M["white"], thick=0.38)
    for f in range(2, nF + 1):
        y = Y + gh + (f - 2) * fh
        ph = bk["ph"] + f * 0.42
        dep = lambda s, ph=ph: 0.75 + 1.55 * (0.5 + 0.5 * math.sin(2 * math.pi * 5 * s + ph))
        if f == nF:
            band("b%d-band-%d" % (bi, f), top_in, y, lambda s, dep=dep: 2.4 + dep(s), 1.0, 0.38, 0.22, 0.11)
        else:
            band("b%d-band-%d" % (bi, f), lp, y, dep, 1.0, 0.38, 0.22, 0.11)
    BLK.append(dict(loop=lp, top=top_in, roofY=roofY))
    if bi == POOL_BLOCK:
        continue                       # its roof is the scene's pool deck, built below
    band("b%d-roof-parapet" % bi, top_in, roofY, lambda s: 0.4, 0.9, 0.45, 0.26, 0.12)
    cap("b%d-roof" % bi, top_in, roofY + 0.02, M["white"])
    garden = offset(top_in, -1.6)
    if bi != 3:
        prism_l("b%d-garden" % bi, [(p[0], p[1]) for p in garden], roofY, roofY + 0.32, M["roofgarden"])
    for k in range(5):
        p = garden[int((k + 0.5) / 5 * len(garden))]
        ball("b%d-bush-%d" % (bi, k), p[0], -p[1], roofY + 0.75, 0.62, M["tree2"], scale=(1.4, 0.9, 0.75))
    mid = garden[int(len(garden) * 0.25)]
    tan = math.atan2(bk["p2"][1] - bk["p0"][1], bk["p2"][0] - bk["p0"][0])
    pcx = (bk["p0"][0] + bk["p2"][0]) / 2 * 0.5 + mid[0] * 0.5
    pcz = (bk["p0"][1] + bk["p2"][1]) / 2 * 0.5 + mid[1] * 0.5
    for k in range(-3, 4):
        box("b%d-pergola-%d" % (bi, k), pcx + math.cos(tan) * k * 0.9, -(pcz + math.sin(tan) * k * 0.9), roofY + 2.6, 0.18, 4.2, 0.2, M["white"], -tan)
    for sx in (-3, 3):
        for sz in (-1.9, 1.9):
            ppx = pcx + math.cos(tan) * sx * 0.9 - math.sin(tan) * sz
            ppz = pcz + math.sin(tan) * sx * 0.9 + math.cos(tan) * sz
            box("b%d-post-%d-%d" % (bi, sx, int(sz * 10)), ppx, -ppz, roofY + 1.4, 0.2, 0.2, 2.2, M["white"], -tan)
    if bi == 3:
        # the stage's second pool (an illustration: which two roofs was not published)
        bpx = bk["p1"][0] * 0.5 + (bk["p0"][0] + bk["p2"][0]) * 0.25
        bpz = bk["p1"][1] * 0.5 + (bk["p0"][1] + bk["p2"][1]) * 0.25
        pr = round_rect(bpx, bpz, 9, 3.4, 1.1, 8)
        prism_l("b3-pool-coping", [(p[0], p[1]) for p in offset(resample(pr, 120), 0.45)], roofY, roofY + 0.12, M["white"])
        prism_l("b3-pool", pr, roofY, roofY + 0.13, M["pool-water"])
        for k in range(4):
            box("b3-lounger-%d" % k, bpx - 3.9 + k * 2.6, -(bpz + 3.2), roofY + 0.22, 0.8, 1.6, 0.35, M["white"])

# ---------------------------------------------------------------- the sky and the sun (rainbow_interior.py, sunset)
world = bpy.data.worlds.new("sky")
scene.world = world
world.use_nodes = True
nt = world.node_tree
nt.nodes.clear()
sky = nt.nodes.new("ShaderNodeTexSky")
try:
    sky.sky_type = "NISHITA"
except TypeError:
    pass
SUN_ELEV = math.radians(11)
SUN_AZ = math.radians(262)            # just south of west, a September late afternoon over the sea
for attr, val in (("sun_elevation", SUN_ELEV), ("sun_rotation", math.radians(90) - SUN_AZ + math.pi), ("altitude", 100.0),
                  ("air_density", 1.2), ("dust_density", 2.2), ("ozone_density", 1.0), ("sun_intensity", 0.6)):
    if hasattr(sky, attr):
        setattr(sky, attr, val)
bg = nt.nodes.new("ShaderNodeBackground")
bg.inputs["Strength"].default_value = 0.42
wout = nt.nodes.new("ShaderNodeOutputWorld")
nt.links.new(sky.outputs[0], bg.inputs[0])
nt.links.new(bg.outputs[0], wout.inputs[0])
sun_data = bpy.data.lights.new("sun", "SUN")
sun_data.energy = 2.6
sun_data.color = (1.0, 0.86, 0.72)
sun_data.angle = math.radians(0.8)
sun = bpy.data.objects.new("sun", sun_data)
bpy.context.collection.objects.link(sun)
d = Vector((math.sin(SUN_AZ) * math.cos(SUN_ELEV), math.cos(SUN_AZ) * math.cos(SUN_ELEV), math.sin(SUN_ELEV)))
sun.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()


def light(name, kind, loc, energy, color=(1.0, 0.82, 0.62), size=0.1, rot=None, size_y=None, cam=True):
    ld = bpy.data.lights.new(name, kind)
    ld.energy = energy
    ld.color = color
    if kind == "AREA":
        ld.shape = "RECTANGLE"
        ld.size = size
        ld.size_y = size_y or size
    else:
        ld.shadow_soft_size = size
    lo = bpy.data.objects.new(name, ld)
    lo.location = loc
    if rot is not None:
        lo.rotation_euler = rot
    if not cam:
        lo.visible_camera = False
        lo.visible_glossy = False
    return link(lo)


def aim(vec):
    """an Euler rotation that points a light's -Z along vec (grid frame)"""
    return Vector(vec).to_track_quat("-Z", "Y").to_euler()


# ---------------------------------------------------------------- the camera
cam_data = bpy.data.cameras.new("pano")
cam_data.clip_start = 0.05
cam_data.clip_end = 60000.0
cam_data.type = "PANO"
try:
    cam_data.panorama_type = "EQUIRECTANGULAR"
except (AttributeError, TypeError):
    cam_data.cycles.panorama_type = "EQUIRECTANGULAR"
cam = bpy.data.objects.new("pano", cam_data)
bpy.context.collection.objects.link(cam)
cam.parent = SITE
scene.camera = cam


def place_camera(x, z, h, dx, dz):
    """the eye at stage-local (x, z), h metres above the street; the panorama's centre along (dx, dz)"""
    cam.location = (x, -z, h)
    look = math.atan2(dx, -dz)                   # clockwise from the grid's north
    cam.rotation_euler = (math.radians(90), 0, -look)
    return (math.degrees(look) - math.degrees(G)) % 360   # the true bearing of the panorama's centre


def bearing_to(x0, z0, x1, z1):
    return (math.degrees(math.atan2(x1 - x0, -(z1 - z0))) - math.degrees(G)) % 360


# ================================================================ the scenes
def smooth_box(name, cx, cy, cz, sx, sy, sz, material, rot=0.0, bev=0.01, segs=3):
    return SK.smooth_bevel(box(name, cx, cy, cz, sx, sy, sz, material, rot), bev, segs)


# ---------------------------------------------------------------- 1. the roof pool on BLOCKS[5]
def build_roofpool():
    bk = BLOCKS[POOL_BLOCK]
    info = BLK[POOL_BLOCK]
    roofY = info["roofY"]
    D = roofY + 0.05                                # the deck's top (a raised deck carries the pool's plumbing)
    # the centreline by arc length, extended straight past its ends (for the round caps)
    NS = 600
    C = [qbez(bk, i / NS) for i in range(NS + 1)]
    cum = [0.0]
    for i in range(NS):
        cum.append(cum[-1] + math.dist(C[i], C[i + 1]))
    LEN = cum[-1]

    def frame(sm):
        sa = LEN / 2 + sm
        if sa <= 0:
            t0 = qtan(bk, 0.0)
            c0 = C[0]
            pt, tg = (c0[0] + t0[0] * sa, c0[1] + t0[1] * sa), t0
        elif sa >= LEN:
            t1 = qtan(bk, 1.0)
            c1 = C[-1]
            pt, tg = (c1[0] + t1[0] * (sa - LEN), c1[1] + t1[1] * (sa - LEN)), t1
        else:
            lo_, hi_ = 0, NS
            while hi_ - lo_ > 1:
                mid_ = (lo_ + hi_) // 2
                if cum[mid_] <= sa:
                    lo_ = mid_
                else:
                    hi_ = mid_
            f = (sa - cum[lo_]) / max(1e-9, cum[hi_] - cum[lo_])
            t = (lo_ + f) / NS
            pt, tg = qbez(bk, t), qtan(bk, t)
        w = (-tg[1], tg[0])
        if w[0] > 0:                                # n > 0 is the courtyard (grid west) side
            w = (-w[0], -w[1])
        return pt, tg, w

    def cv(sm, n):
        pt, tg, w = frame(sm)
        return (pt[0] + w[0] * n, pt[1] + w[1] * n)

    def cangle(sm):
        _, tg, _ = frame(sm)
        return math.atan2(-tg[1], tg[0])             # the tangent's angle in the grid frame's Blender coordinates

    def curved(name, sm0, sm1, n0, n1, y0, y1, material, step=0.3, bev=0.0):
        k = max(1, int(math.ceil((sm1 - sm0) / step)))
        verts, faces = [], []
        for i in range(k + 1):
            s_ = sm0 + (sm1 - sm0) * i / k
            for n_, y_ in ((n0, y0), (n1, y0), (n1, y1), (n0, y1)):
                x_, z_ = cv(s_, n_)
                verts.append((x_, -z_, y_))
        for i in range(k):
            a_, b_ = 4 * i, 4 * (i + 1)
            for j in range(4):
                j2 = (j + 1) % 4
                faces.append((a_ + j, a_ + j2, b_ + j2, b_ + j))
        faces.append((0, 3, 2, 1))
        faces.append((4 * k, 4 * k + 1, 4 * k + 2, 4 * k + 3))
        ob = fix_normals(add_mesh(name, verts, faces, material))
        return SK.smooth_bevel(ob, bev, 2) if bev else ob

    def cbox(name, sm, n, y0, y1, sl, sn, material, bev=0.01, segs=3, rot=0.0):
        x_, z_ = cv(sm, n)
        return smooth_box(name, x_, -z_, (y0 + y1) / 2, sl, sn, y1 - y0, material, cangle(sm) + rot, bev, segs)

    def cpt(sm, n, h):
        x_, z_ = cv(sm, n)
        return (x_, -z_, h)

    # --- materials of the roof
    deck_stone = stone_tiles("deck-limestone", (0.63, 0.57, 0.48), (0.6, 1.2), 0.005, 0.09, 0.58, 0.0, 1.1)
    teak = SK.wood("teak-deck", (0.30, 0.19, 0.11), (0.40, 0.27, 0.16), rough=0.5, planks=True)
    coping = vary(mat("coping", (0.80, 0.77, 0.71), 0.35), 0.06, 1.5)
    pool_tile = boxmap(tile_mat("pool-mosaic", (0.42, 0.72, 0.74), (0.47, 0.76, 0.78), (0.78, 0.80, 0.78), 0.05, 0.15))
    edge_stone = mat("edge-stone", (0.16, 0.17, 0.17), 0.3)
    cushion = SK.fabric("cushion", (0.80, 0.77, 0.70))
    towel = SK.fabric("towel", (0.20, 0.33, 0.40))
    canopy = SK.fabric("parasol-canvas", (0.86, 0.83, 0.76))
    _p(canopy).inputs["Transmission Weight"].default_value = 0.25
    frame_wood = SK.wood("lounger-teak", (0.32, 0.20, 0.11), (0.42, 0.28, 0.16), rough=0.45)
    planter = vary(mat("planter-fibrecement", (0.22, 0.22, 0.21), 0.8), 0.12, 2.0)
    white_alu = mat("white-alu", (0.82, 0.82, 0.80), 0.35, 0.3)

    # --- the roof slab and deck (the top floor's setback line, 0.25 m out: the stage's roof edge), a hole for the pool
    edge_pts = offset(info["top"], 0.25)
    slab = prism_l("pool-roof-slab", [(p[0], p[1]) for p in edge_pts], roofY - 0.45, D, deck_stone)
    PS0, PS1, PN0, PN1 = -6.0, 6.0, 0.0, 3.5         # the pool: 12 m along the curve, 3.5 m across (n: courtyard side +)
    cut = curved("pool-cutter", PS0 - 0.02, PS1 + 0.02, PN0 - 0.02, 3.97, D - 2.0, D + 1.0, M["white"], 0.25)
    cut.hide_render = True
    md = slab.modifiers.new("pool-hole", "BOOLEAN")
    md.operation = "DIFFERENCE"
    md.object = cut
    try:
        md.solver = "EXACT"
    except TypeError:
        pass
    # the slab's edge in the facade's white render, a thin stainless shoe and the frameless glass balustrade
    loop_wall("pool-roof-edge", offset(edge_pts, 0.006), roofY - 0.45, D - 0.005, M["white"], 1.0, 1.0)
    rail = offset(info["top"], 0.15)
    band("pool-roof-shoe", rail, D, lambda s: 0.0, 0.1, 0.0, 0.06, 0.02, inset=0.0, floor=False, white=M["steel"])
    loop_wall("pool-roof-balustrade", rail, D + 0.06, D + 1.12, M["rail-glass"], 1.2, 1.0)
    band("pool-roof-cap", offset(rail, 0.02), D + 1.1, lambda s: 0.0, 0.03, 0.0, 0.045, 0.01, inset=0.0, floor=False, white=M["steel"])
    # the balustrade's panel joints every 1.2 m (slim vertical steel clamps)
    acc, last = 0.0, rail[0]
    for i, p in enumerate(rail):
        acc += math.dist(last[:2], p[:2])
        last = p
        if acc >= 1.2:
            acc = 0.0
            cyl("rail-joint-%d" % i, p[0], -p[1], D + 0.06, D + 1.1, 0.012, M["steel"], 8)

    # --- the pool: mosaic basin, the infinity edge on the courtyard side into a catch trough, stone coping on three sides
    WL = D - 0.035                                   # the water line: the infinity wall's top
    curved("pool-floor", PS0, PS1, PN0, PN1, D - 1.45, D - 1.4, pool_tile, 0.25)
    curved("pool-wall-east", PS0, PS1, PN0 - 0.2, PN0, D - 1.45, D - 0.03, pool_tile, 0.25)
    curved("pool-wall-north", PS0 - 0.2, PS0, PN0 - 0.2, 3.97, D - 1.45, D - 0.03, pool_tile, 0.25)
    curved("pool-wall-south", PS1, PS1 + 0.2, PN0 - 0.2, 3.97, D - 1.45, D - 0.03, pool_tile, 0.25)
    curved("pool-infinity-wall", PS0, PS1, PN1, PN1 + 0.2, D - 1.45, WL - 0.004, edge_stone, 0.25)
    curved("pool-trough-floor", PS0, PS1, PN1 + 0.2, 3.97, D - 0.42, D - 0.38, edge_stone, 0.25)
    curved("pool-trough-wall", PS0, PS1, 3.95, 3.99, D - 0.42, D, edge_stone, 0.25)
    water = curved("pool-water", PS0, PS1, PN0, PN1 + 0.04, WL - 0.02, WL, M["pool-water"], 0.2)
    curved("pool-trough-water", PS0, PS1, PN1 + 0.2, 3.95, D - 0.34, D - 0.33, M["pool-water"], 0.3)
    curved("pool-sheet", PS0, PS1, PN1 + 0.2, PN1 + 0.215, D - 0.34, WL, M["pool-water"], 0.3)   # the water falling over the edge
    curved("coping-east", PS0 - 0.4, PS1 + 0.4, PN0 - 0.4, PN0 + 0.02, D - 0.06, D + 0.025, coping, 0.25, bev=0.01)
    curved("coping-north", PS0 - 0.4, PS0 + 0.02, PN0 + 0.02, 3.99, D - 0.06, D + 0.025, coping, 0.1, bev=0.01)
    curved("coping-south", PS1 - 0.02, PS1 + 0.4, PN0 + 0.02, 3.99, D - 0.06, D + 0.025, coping, 0.1, bev=0.01)
    # steps into the pool at the south end, a stainless ladder at the north end, three underwater lights
    for k in range(3):
        curved("pool-step-%d" % k, PS1 - 0.4 * (k + 1), PS1, PN0 + 0.02, 1.4, D - 1.45, D - 0.3 - k * 0.35, pool_tile, 0.2)
    for sgn in (-1, 1):
        x_, y_, _ = cpt(PS0 + 0.35, 1.2 + sgn * 0.25, 0)
        cyl("ladder-%d" % sgn, x_, y_, D - 1.0, D + 0.75, 0.022, M["steel"], 12)
    pool_light = mat("pool-light", (1, 1, 1), 0.3, emission=((0.75, 0.92, 1.0), 5.0))
    for k, sm in enumerate((-3.5, 0.0, 3.5)):
        x_, y_, _ = cpt(sm, PN0 + 0.012, 0)
        ob = cyl("pool-light-%d" % k, x_, y_, D - 0.72, D - 0.6, 0.09, pool_light, 20)
        ob.rotation_euler = (math.radians(90), 0, cangle(sm))

    # --- the deck's east side: teak under the loungers, loungers with cushions, side tables, two parasols
    curved("teak-strip", -5.2, 5.2, -3.35, -0.45, D, D + 0.03, teak, 0.25, bev=0.004)
    LG = [-4.6, -3.3, 0.6, 1.9]                       # the loungers' positions along the curve (camera at the south end)
    for i, sm in enumerate(LG):
        a = cangle(sm) + math.pi / 2                  # the lounger's long axis across the building (feet to the pool)
        # frame: a low teak platform on four legs
        for j, (n0, n1) in enumerate(((-0.95, -2.95),)):
            x_, y_, _ = cpt(sm, (n0 + n1) / 2, 0)
            smooth_box("lounger-frame-%d" % i, x_, y_, D + 0.03 + 0.26, 2.0, 0.72, 0.06, frame_wood, a, 0.012)
            for u in (-0.85, 0.85):
                for v in (-0.3, 0.3):
                    xx, yy, _ = cpt(sm + v, (n0 + n1) / 2 + u, 0)
                    smooth_box("lounger-leg-%d-%d-%d" % (i, int(u * 10), int(v * 10)), xx, yy, D + 0.03 + 0.13, 0.06, 0.06, 0.26, frame_wood, a, 0.008)
        # the seat cushion (feet end, towards the pool) and the raised back cushion (the east end)
        x_, y_, _ = cpt(sm, -1.55, 0)
        smooth_box("lounger-seat-%d" % i, x_, y_, D + 0.03 + 0.33, 1.3, 0.68, 0.09, cushion, a, 0.035, 4)
        bx_, by_, _ = cpt(sm, -2.55, 0)
        tilt = math.radians(-38)
        obox("lounger-back-%d" % i, (bx_, by_, D + 0.03 + 0.52), (0.8, 0.68, 0.09), cushion, yaw=a, tilt=tilt, bev=0.035, segs=4)
        ux_, uy_ = math.cos(a), math.sin(a)
        obox("lounger-backframe-%d" % i, (bx_ + ux_ * 0.045, by_ + uy_ * 0.045, D + 0.03 + 0.465), (0.84, 0.72, 0.035), frame_wood,
             yaw=a, tilt=tilt, bev=0.008)
        sx2, sy2, _ = cpt(sm, -2.86, 0)
        smooth_box("lounger-strut-%d" % i, sx2, sy2, D + 0.03 + 0.5, 0.05, 0.6, 0.38, frame_wood, a, 0.008)
        if i in (0, 2):
            tx_, ty_, _ = cpt(sm, -1.2, 0)
            ob = cyl("towel-%d" % i, tx_, ty_, D + 0.48 - 0.31, D + 0.48 + 0.31, 0.075, towel, 20)
            ob.rotation_euler = (math.radians(90), 0, a)
    for i, sm in enumerate((-3.95, 1.25)):
        x_, y_, _ = cpt(sm, -2.35, 0)
        cyl("side-table-%d" % i, x_, y_, D + 0.03, D + 0.42, 0.2, frame_wood, 28)
        cyl("carafe-%d" % i, x_ + 0.05, y_, D + 0.42, D + 0.64, 0.045, M["rail-glass"], 20)
        # a parasol for each pair: a pole, a shallow canvas cone, a stone base
        px_, py_, _ = cpt(sm, -3.05, 0)
        cyl("parasol-base-%d" % i, px_, py_, D + 0.03, D + 0.12, 0.3, edge_stone, 24)
        cyl("parasol-pole-%d" % i, px_, py_, D + 0.12, D + 2.62, 0.022, white_alu, 12)
        cyl("parasol-canopy-%d" % i, px_, py_, D + 2.22, D + 2.58, 1.45, canopy, 10, r2=0.05)
        cyl("parasol-finial-%d" % i, px_, py_, D + 2.58, D + 2.66, 0.03, white_alu, 10)
    # planters along the east balustrade: long fibre-cement troughs with shrubs and grasses, olive trees in the corners
    for i, (s0, s1) in enumerate(((-9.0, -5.6), (-5.0, -1.6), (-0.8, 2.6), (3.2, 6.4))):
        curved("planter-%d" % i, s0, s1, -3.98, -3.45, D, D + 0.55, planter, 0.25, bev=0.01)
        curved("planter-soil-%d" % i, s0 + 0.05, s1 - 0.05, -3.93, -3.5, D + 0.5, D + 0.51, M["soil"], 0.3)
        k_ = 0
        s_ = s0 + 0.3
        while s_ < s1 - 0.2:
            x_, y_, _ = cpt(s_, -3.72, 0)
            r_ = 0.28 + rnd.random() * 0.12
            ball("shrub-%d-%d" % (i, k_), x_, y_, D + 0.62 + r_ * 0.4, r_, M["tree"] if k_ % 3 else M["olive"], scale=(1, 1, 0.8))
            s_ += 0.42 + rnd.random() * 0.15
            k_ += 1
    for i, (sm, n) in enumerate(((-10.6, 2.4), (8.4, -2.2))):
        x_, y_, _ = cpt(sm, n, 0)
        cyl("olive-pot-%d" % i, x_, y_, D, D + 0.7, 0.42, planter, 32, r2=0.36)
        cyl("olive-soil-%d" % i, x_, y_, D + 0.66, D + 0.68, 0.38, M["soil"], 24)
        tree("olive-%d" % i, x_, -y_, D + 0.68, 0.95, material=M["olive"], fine=True)
    # an outdoor shower post at the pool's south end, on a teak grate
    sx_, sy_, _ = cpt(PS1 + 1.6, -1.4, 0)
    curved("shower-grate", PS1 + 1.2, PS1 + 2.0, -1.8, -1.0, D, D + 0.04, teak, 0.2, bev=0.004)
    cyl("shower-post", sx_, sy_, D + 0.04, D + 2.25, 0.035, M["steel"], 16)
    hx_, hy_, _ = cpt(PS1 + 1.6, -1.1, 0)
    obox("shower-arm", ((sx_ + hx_) / 2, (sy_ + hy_) / 2, D + 2.22), (0.34, 0.03, 0.03), M["steel"], yaw=cangle(PS1 + 1.6) + math.pi / 2)
    cyl("shower-head", hx_, hy_, D + 2.16, D + 2.2, 0.12, M["steel"], 24)
    cyl("shower-tap", sx_, sy_, D + 1.0, D + 1.1, 0.05, M["steel"], 16)
    # the north end: a white pergola over an outdoor lounge (the stage draws a pergola on every roof)
    for k in range(7):
        cbox("pergola-slat-%d" % k, -9.6 + k * 0.5, 0.0, D + 2.7, D + 2.9, 0.12, 6.4, white_alu, 0.004, 2)
    for sm in (-9.6, -6.6):
        for n in (-3.0, 3.0):
            cbox("pergola-post-%d-%d" % (int(sm), int(n)), sm, n, D, D + 2.7, 0.14, 0.14, white_alu, 0.004, 2)
    for k, n in enumerate((-2.0, -0.95, 0.1)):
        cbox("lounge-seat-%d" % k, -8.6, n, D + 0.12, D + 0.42, 0.85, 1.0, cushion, 0.04, 4)
    cbox("lounge-back", -9.1, -0.95, D + 0.12, D + 0.85, 0.22, 3.1, cushion, 0.05, 4)
    cbox("lounge-plinth", -8.7, -0.95, D, D + 0.12, 1.0, 3.2, frame_wood, 0.01)
    cbox("lounge-table", -7.3, -0.95, D, D + 0.36, 0.8, 1.4, edge_stone, 0.02)
    # the roof's stair and lift exit at the far north tip, in the facade's white render with a glass door
    cbox("roof-exit", -10.9, -0.6, D, D + 3.0, 2.0, 2.8, M["white"], 0.03)
    cbox("roof-exit-door", -9.89, -0.6, D + 0.02, D + 2.3, 0.02, 1.1, M["glass"], 0.0)
    cbox("roof-exit-frame", -9.88, -0.6, D + 2.3, D + 2.36, 0.04, 1.2, M["frame"], 0.0)

    # --- the camera: at the pool's south end, 1.6 m above the deck, the panorama's centre looking along the pool
    ex, ez = cv(PS1 + 0.75, 1.75)
    ax, az = cv(PS1 - 4.0, 1.75)
    centre = place_camera(ex, ez, D + 1.6, ax - ex, az - ez)
    tb = bearing_to(ex, ez, T_["cx"], T_["cz"])
    sea = (math.degrees(math.atan2(-1, 0)) - math.degrees(G)) % 360
    print("ILLUSTRATION roofpool: the roof of boutique building BLOCKS[5] (the stage's roof:5 pin; the design plan puts pools on "
          "two boutique roofs without saying which), deck %.2f m, eye %.2f m" % (D, D + 1.6))
    print("panorama centre bearing %.1f | tower at %.1f (yaw %+.1f) | sea (grid west) at %.1f (yaw %+.1f)" % (
        centre, tb, (tb - centre + 540) % 360 - 180, sea, (sea - centre + 540) % 360 - 180))


# ---------------------------------------------------------------- the tower's frame for the lobby and the club
TR = T_["rot"]


def TP(a, b):
    """a point a metres along the tower's long axis (grid south +) and b across (grid west +), stage-local"""
    return (T_["cx"] + a * math.cos(TR) - b * math.sin(TR), T_["cz"] + a * math.sin(TR) + b * math.cos(TR))


def TB(a, b):
    x, z = TP(a, b)
    return x, -z


def tbox(name, a, b, z0, z1, sa, sb, material, bev=0.01, segs=3, rot=0.0):
    x, y = TB(a, b)
    ob = box(name, x, y, (z0 + z1) / 2, sa, sb, z1 - z0, material, -TR + rot)
    return SK.smooth_bevel(ob, bev, segs) if bev else ob


def tcyl(name, a, b, z0, z1, r, material, seg=32, r2=None):
    x, y = TB(a, b)
    return cyl(name, x, y, z0, z1, r, material, seg, r2)


def tball(name, a, b, z, r, material, scale=(1, 1, 1)):
    x, y = TB(a, b)
    return ball(name, x, y, z, r, material, scale=scale)


def half_width(a, A, B):
    return B * math.sqrt(max(0.0, 1 - (a / A) ** 2))


def glass_mullions(name, pts, y0, y1, keep, depth=0.14, every=1.5, transoms=()):
    """slim frames on the inside of a clear glass line (where keep(a, b) says the camera can see them)"""
    acc, last = 0.0, pts[0]
    for i, p in enumerate(pts):
        acc += math.dist(last[:2], p[:2])
        last = p
        if acc < every:
            continue
        acc = 0.0
        dx, dz = p[0] - T_["cx"], p[1] - T_["cz"]
        a = dx * math.cos(TR) + dz * math.sin(TR)
        b = -dx * math.sin(TR) + dz * math.cos(TR)
        if not keep(a, b):
            continue
        ang = math.atan2(p[4], p[3])
        box("%s-%d" % (name, i), p[0] - p[3] * depth / 2, -(p[1] - p[4] * depth / 2), (y0 + y1) / 2, depth, 0.05, y1 - y0, M["frame"], -ang)
    for k, ty in enumerate(transoms):
        band("%s-transom-%d" % (name, k), offset(pts, -0.03), ty, lambda s: 0.0, 0.05, 0.0, 0.05, 0.01, inset=0.0, floor=False, white=M["frame"])


def fill_light(name, a, b, z, width, height, energy, inward):
    """the photographer's window pull (rainbow_interior.py): a soft light just inside the glass, invisible to the camera"""
    x, y = TB(a, b)
    ia, ib = inward
    dx, dy = TB(a + ia, b + ib)
    lo = light(name, "AREA", (x, y, z), energy, (1.0, 0.95, 0.88), size=width, size_y=height, cam=False)
    lo.rotation_euler = aim((dx - x, dy - y, 0.0))
    return lo


def downlights(prefix, spots, zc, material):
    for k, (a, b) in enumerate(spots):
        tcyl("%s-%d" % (prefix, k), a, b, zc - 0.012, zc, 0.06, material, 20)
        tcyl("%s-trim-%d" % (prefix, k), a, b, zc - 0.006, zc + 0.002, 0.085, M["frame"], 20)


# ---------------------------------------------------------------- 2. the lobby
def build_lobby():
    F = Y                                          # the lobby floor: the courtyard deck's level
    CEIL = T_["y0"] - 0.43                         # the plaster ceiling under the base floor's slab: a 5.6 m double-height hall
    AL, BL = T_["A"] - 2.2, T_["B"] - 2.2          # the recessed lobby glass (tLobby)
    floor_stone = stone_tiles("lobby-floor", (0.50, 0.45, 0.38), (1.2, 1.2), 0.0025, 0.06, 0.2, 0.0, 0.9)
    wall_plaster = vary(mat("lobby-plaster", (0.83, 0.80, 0.75), 0.85), 0.05, 0.4)
    core_stone = SK.stone("core-stone", (0.52, 0.48, 0.43), rough=0.3)
    walnut = SK.wood("walnut-slat", (0.17, 0.10, 0.06), (0.26, 0.16, 0.09), rough=0.45)
    backing = mat("slat-backing", (0.05, 0.04, 0.035), 0.8)
    desk_stone = SK.stone("desk-travertine", (0.78, 0.72, 0.62), rough=0.32)
    desk_top = SK.wood("desk-oak", (0.46, 0.32, 0.19), (0.56, 0.40, 0.25), rough=0.35)
    sofa = SK.fabric("lobby-sofa", (0.74, 0.70, 0.62))
    accent = SK.leather("lobby-leather", (0.17, 0.085, 0.045))
    rug = SK.rugmat("lobby-rug", (0.48, 0.44, 0.38))
    dark_stone = SK.stone("table-stone", (0.16, 0.15, 0.14), rough=0.25)
    pot = vary(mat("pot-stone", (0.42, 0.39, 0.35), 0.75), 0.1, 3.0)
    brass = SK.metal("brass")
    globe = SK.glow()
    _p(globe).inputs["Emission Strength"].default_value = 9.0
    dl = mat("downlight", (1, 1, 1), 0.5, emission=((1.0, 0.86, 0.70), 30.0))
    mat_black = mat("lobby-black", (0.03, 0.03, 0.03), 0.4, 0.8)
    books = [SK.paint("book-%d" % i, c) for i, c in enumerate(((0.8, 0.76, 0.68), (0.2, 0.25, 0.28), (0.55, 0.3, 0.18)))]

    # the floor, the ceiling (the base floor's slab, in plaster)
    cap("lobby-floor", tLobby, F + 0.012, floor_stone, thick=0.3)
    cap("lobby-ceiling", tLoop, CEIL + 0.006, wall_plaster, thick=0.006)
    # the core (lifts, stairs, services) in the middle, clad in stone; its courtyard face carries the feature wall
    CA0, CA1, CB0, CB1 = -7.0, 4.6, -4.4, 1.4
    tbox("core", (CA0 + CA1) / 2, (CB0 + CB1) / 2, F, CEIL, CA1 - CA0, CB1 - CB0, core_stone, 0.02)
    # the retail beyond the lobby on the street side (the stage's tower:street), closed by a plaster wall; services east
    hw = half_width(-8.2, AL, BL)
    tbox("retail-wall", -8.2, 0.0, F, CEIL, 0.3, 2 * hw - 0.1, wall_plaster, 0.01)
    hw2 = half_width(10.5, AL, BL)
    tbox("service-wall", (CA1 + 10.5) / 2 + 0.6, CB0 + 0.15, F, CEIL, 10.5 - CA1 + 1.2, 0.3, wall_plaster, 0.01)
    tbox("service-wall-2", 10.5, (CB0 - hw2) / 2, F, CEIL, 0.3, abs(-hw2 - CB0) + 0.1, wall_plaster, 0.01)
    # the feature wall: vertical walnut slats, floor to ceiling, on the core's courtyard face, lit from above
    tbox("feature-backing", (CA0 + CA1) / 2, CB1 + 0.02, F, CEIL, CA1 - CA0 - 0.2, 0.04, backing, 0.0)
    a = CA0 + 0.2
    k = 0
    while a < CA1 - 0.2:
        tbox("slat-%d" % k, a, CB1 + 0.07, F + 0.02, CEIL - 0.02, 0.045, 0.07, walnut, 0.006, 2)
        a += 0.11
        k += 1
    for k in range(10):
        aa = CA0 + 0.6 + k * (CA1 - CA0 - 1.2) / 9
        x, y = TB(aa, CB1 + 0.55)
        lo = light("wallwash-%d" % k, "SPOT", (x, y, CEIL - 0.05), 90.0, (1.0, 0.8, 0.58), size=0.05)
        lo.data.spot_size = math.radians(70)
        lo.data.spot_blend = 0.6
        tx, ty = TB(aa, CB1)
        lo.rotation_euler = aim((tx - x, ty - y, -3.5))
    # the reception desk: a travertine monolith with an oak top, in front of the feature wall
    tbox("desk", -1.2, CB1 + 2.1, F, F + 1.05, 3.8, 0.85, desk_stone, 0.02)
    tbox("desk-top", -1.2, CB1 + 2.0, F + 1.05, F + 1.1, 4.0, 1.05, desk_top, 0.01)
    tbox("desk-shelf", -1.2, CB1 + 1.55, F + 0.72, F + 0.76, 3.6, 0.35, desk_top, 0.006)
    tcyl("desk-lamp-base", -2.6, CB1 + 2.2, F + 1.1, F + 1.12, 0.08, brass, 20)
    tcyl("desk-lamp-stem", -2.6, CB1 + 2.2, F + 1.12, F + 1.5, 0.008, brass, 8)
    tball("desk-lamp-globe", -2.6, CB1 + 2.2, F + 1.56, 0.09, globe)
    tbox("desk-screen", -0.4, CB1 + 1.8, F + 1.1, F + 1.42, 0.5, 0.03, mat_black, 0.004)
    tbox("desk-orchid-pot", 0.8, CB1 + 2.2, F + 1.1, F + 1.25, 0.18, 0.18, pot, 0.01)
    for j in range(5):
        tball("orchid-%d" % j, 0.8 + (j - 2) * 0.04, CB1 + 2.2, F + 1.4 + j * 0.05, 0.05, SK.paint("orchid", (0.92, 0.9, 0.88), 0.5))
    # the lifts on the core's south face: bronze doors in stone frames
    for k, bb in enumerate((-2.9, -1.5, -0.1)):
        tbox("lift-door-%d" % k, CA1 + 0.01, bb, F, F + 2.6, 0.04, 1.1, M["bronze"], 0.004)
        tbox("lift-frame-%d" % k, CA1 + 0.02, bb, F + 2.6, F + 2.72, 0.05, 1.3, M["bronze"], 0.004)
    # the seating area in the south of the hall, by the glass: two sofas across a stone table, two leather armchairs, a rug
    SA, SB = 9.2, 0.6
    tbox("lobby-rug", SA, SB, F + 0.012, F + 0.028, 4.2, 3.4, rug, 0.0)
    for sgn in (-1, 1):
        aa = SA + sgn * 1.35
        tbox("sofa-base-%d" % sgn, aa, SB, F + 0.1, F + 0.4, 0.95, 2.4, sofa, 0.03)
        tbox("sofa-seat-%d" % sgn, aa - sgn * 0.06, SB, F + 0.4, F + 0.55, 0.78, 2.2, sofa, 0.07, 4)
        tbox("sofa-back-%d" % sgn, aa + sgn * 0.36, SB, F + 0.4, F + 0.88, 0.22, 2.3, sofa, 0.08, 4)
        for t in (-1, 1):
            tbox("sofa-arm-%d-%d" % (sgn, t), aa, SB + t * 1.25, F + 0.1, F + 0.64, 0.95, 0.2, sofa, 0.06, 4)
        tbox("cushion-%d" % sgn, aa + sgn * 0.2, SB - 0.7, F + 0.55, F + 0.95, 0.14, 0.44, accent, 0.06, 4, rot=0.2)
    tbox("coffee-table", SA, SB, F, F + 0.38, 1.0, 1.6, dark_stone, 0.03)
    for i, bm_ in enumerate(books):
        tbox("coffee-book-%d" % i, SA - 0.1, SB - 0.3, F + 0.38 + i * 0.035, F + 0.41 + i * 0.035, 0.28, 0.22, bm_, 0.004, rot=0.1 * i)
    tcyl("coffee-bowl", SA + 0.15, SB + 0.35, F + 0.38, F + 0.48, 0.16, brass, 32, r2=0.12)
    for sgn in (-1, 1):
        cb = SB + sgn * 2.45
        tbox("armchair-seat-%d" % sgn, SA, cb, F + 0.2, F + 0.45, 0.82, 0.82, accent, 0.07, 4)
        tbox("armchair-back-%d" % sgn, SA, cb + sgn * 0.34, F + 0.4, F + 0.85, 0.8, 0.16, accent, 0.07, 4)
        for t in (-1, 1):
            tbox("armchair-arm-%d-%d" % (sgn, t), SA + t * 0.38, cb, F + 0.2, F + 0.62, 0.12, 0.82, accent, 0.05, 4)
            for u in (-1, 1):
                tbox("armchair-leg-%d-%d-%d" % (sgn, t, u), SA + t * 0.32, cb + u * 0.32, F, F + 0.2, 0.035, 0.035, brass, 0.004)
    # a pendant cluster over the seating: glass globes on long brass cords at staggered heights
    for k, (da, db, h) in enumerate(((0, 0, 3.2), (0.5, 0.45, 3.6), (-0.45, 0.5, 3.4), (0.4, -0.5, 3.8), (-0.5, -0.4, 3.0),
                                      (0.05, 0.9, 3.9), (0.1, -0.95, 3.5))):
        tball("pendant-%d" % k, SA + da, SB + db, F + h, 0.16, globe)
        tcyl("pendant-cord-%d" % k, SA + da, SB + db, F + h + 0.16, CEIL, 0.005, brass, 6)
    tcyl("pendant-canopy", SA, SB, CEIL - 0.03, CEIL, 0.4, brass, 32)
    # a floating ceiling of walnut slats over the seating, lit at its edge
    for k in range(46):
        bb = SB - 3.4 + k * 0.15
        if abs(bb - SB) > 3.45:
            continue
        tbox("ceiling-slat-%d" % k, SA - 0.2, bb, CEIL - 0.34, CEIL - 0.26, 6.2, 0.05, walnut, 0.005, 2)
    for t in (-1, 1):
        tbox("ceiling-slat-rail-%d" % t, SA - 0.2 + t * 2.6, SB, CEIL - 0.26, CEIL - 0.22, 0.06, 7.0, backing, 0.0)
    # a large canvas on the retail wall, over a stone console with a vase and branches
    art = SK.artmat(((0.55, 0.36, 0.22), (0.86, 0.80, 0.70), (0.30, 0.32, 0.30)))
    tbox("lobby-art", -8.03, 1.6, F + 1.3, F + 3.9, 0.04, 3.4, art, 0.004)
    tbox("lobby-art-frame", -8.04, 1.6, F + 1.26, F + 3.94, 0.03, 3.48, mat_black, 0.004)
    tbox("console", -7.75, 1.6, F + 0.1, F + 0.82, 0.45, 2.6, desk_stone, 0.02)
    tbox("console-base", -7.75, 1.6, F, F + 0.1, 0.35, 2.4, mat_black, 0.0)
    tcyl("console-vase", -7.75, 2.3, F + 0.82, F + 1.22, 0.11, SK.paint("vase-lobby", (0.12, 0.11, 0.1), 0.3), 32, r2=0.07)
    branch = SK.paint("branch", (0.30, 0.24, 0.17), 0.8)
    for k in range(8):
        x_, y_ = TB(-7.75, 2.3)
        rod("console-twig-%d" % k, (x_, y_, F + 1.15), (x_ + rnd.uniform(-0.45, 0.45), y_ + rnd.uniform(-0.45, 0.45), F + 1.9 + rnd.random() * 0.6),
            0.008, 0.003, branch, 5)
    # a bench and books along the glass on the north side, and tall planters: olive trees and a fig
    tbox("bench", -4.0, half_width(-4.0, AL, BL) - 1.1, F, F + 0.45, 3.2, 0.55, desk_top, 0.02)
    for k, (a_, b_, r_, m_) in enumerate(((5.8, 5.2, 1.1, M["olive"]), (11.8, 3.6, 1.0, M["olive"]), (-6.6, 4.6, 0.9, M["tree"]),
                                          (1.6, 6.2, 0.8, M["tree"]))):
        tcyl("tall-pot-%d" % k, a_, b_, F, F + 0.9, 0.5, pot, 40, r2=0.42)
        tcyl("tall-soil-%d" % k, a_, b_, F + 0.86, F + 0.88, 0.46, M["soil"], 24)
        x_, y_ = TB(a_, b_)
        tree("lobby-tree-%d" % k, x_, -y_, F + 0.88, r_ * 1.2, material=m_, fine=True)
    # the glass: slim bronze mullions every 1.5 m, a transom at the door height, the entrance doors at the grid-west side
    glass_mullions("lobby-mullion", tLobby, F, CEIL, lambda a_, b_: a_ > -9.0, 0.16, 1.5, transoms=(F + 3.0,))
    ea = 7.6
    eb = half_width(ea, AL, BL) - 0.08
    for sgn in (-1, 1):
        tbox("door-frame-%d" % sgn, ea + sgn * 1.2, eb, F, F + 3.0, 0.08, 0.1, M["bronze"], 0.004)
        tbox("door-pull-%d" % sgn, ea + sgn * 0.12, eb - 0.1, F + 0.7, F + 2.1, 0.035, 0.035, M["bronze"], 0.004)
    tbox("door-head", ea, eb, F + 2.95, F + 3.05, 2.5, 0.12, M["bronze"], 0.004)
    # two glass door leaves in slim bronze frames (stiles, top and bottom rails), meeting in the middle
    for sgn in (-1, 1):
        c_ = ea + sgn * 0.6
        tbox("door-leaf-glass-%d" % sgn, c_, eb - 0.02, F + 0.12, F + 2.9, 1.1, 0.012, M["glass"], 0.0)
        tbox("door-stile-%d" % sgn, ea + sgn * 0.035, eb - 0.02, F, F + 2.95, 0.05, 0.06, M["bronze"], 0.003)
        tbox("door-rail-bottom-%d" % sgn, c_, eb - 0.02, F, F + 0.12, 1.15, 0.06, M["bronze"], 0.003)
        tbox("door-rail-top-%d" % sgn, c_, eb - 0.02, F + 2.9, F + 2.95, 1.15, 0.06, M["bronze"], 0.003)
    tbox("door-mat", ea, eb - 1.1, F + 0.012, F + 0.026, 2.4, 1.6, SK.rugmat("mat", (0.18, 0.17, 0.16)), 0.0)
    # the ceiling: downlights on a grid, a cove of light around the core's top
    spots = []
    for a_ in [-6.5 + 2.2 * i for i in range(10)]:
        for b_ in (2.7, 4.9, -2.2, 0.0):
            if (a_ / (AL - 0.8)) ** 2 + (b_ / (BL - 0.8)) ** 2 < 1 and not (CA0 - 0.3 < a_ < CA1 + 0.3 and CB0 - 0.3 < b_ < CB1 + 0.3) \
                    and a_ > -8.0 and not (a_ < 10.5 and b_ < CB0) and abs(a_ - SA) + abs(b_ - SB) > 1.5:
                spots.append((a_, b_))
    downlights("lobby-dl", spots, CEIL, dl)
    for (a_, b_) in spots:
        x, y = TB(a_, b_)
        lo = light("lobby-dl-light-%d-%d" % (int(a_ * 10), int(b_ * 10)), "AREA", (x, y, CEIL - 0.03), 40.0, (1.0, 0.84, 0.66), size=0.12)
        lo.data.shape = "DISK"
    for k, (da, db, h) in enumerate(((0, 0, 3.2), (0.5, 0.45, 3.6), (-0.45, 0.5, 3.4), (0.4, -0.5, 3.8), (-0.5, -0.4, 3.0))):
        x, y = TB(SA + da, SB + db)
        light("pendant-light-%d" % k, "POINT", (x, y, F + h - 0.3), 22.0, (1.0, 0.8, 0.58), size=0.1)
    # (no window fill here: the hall has its own light, and a fill threw the planters' shadows into the room)

    ca, cb = 3.2, 4.4
    ex, ez = TP(ca, cb)
    tx, tz = TP(ca + 3.0, cb + 3.0)
    centre = place_camera(ex, ez, F + 1.6, tx - ex, tz - ez)
    print("ILLUSTRATION lobby: the tower's double-height entrance hall at the courtyard level (the stage's tower:lobby side), "
          "floor %.2f m, ceiling %.2f m (%.1f m high), eye %.2f m; panorama centre bearing %.1f" % (F, CEIL, CEIL - F, F + 1.6, centre))


# ---------------------------------------------------------------- 3. the Rainbow Club
def build_club():
    F = T_["y0"] + 0.012                           # the base floor (the stage's tower:court pin stands on it)
    CEIL = T_["y0"] + T_["fh"] - 0.42 - 0.2        # a plaster ceiling under the next slab
    AL, BL = T_["A"], T_["B"]
    oak = SK.wood("club-oak", (0.40, 0.31, 0.22), (0.50, 0.40, 0.29), scale=3.0, rough=0.36, planks=True)
    rubber = add_noise_bump(vary(mat("gym-rubber", (0.055, 0.055, 0.06), 0.85), 0.25, 30.0), 400.0, 0.2)
    plaster = vary(mat("club-plaster", (0.84, 0.82, 0.78), 0.85), 0.05, 0.4)
    green = SK.paint("kitchen-green", (0.16, 0.22, 0.18), 0.45)
    counter = SK.stone("club-counter", (0.86, 0.84, 0.80), rough=0.2)
    shelf_oak = SK.wood("shelf-oak", (0.46, 0.32, 0.19), (0.56, 0.40, 0.25), rough=0.4)
    table_oak = SK.wood("table-oak", (0.40, 0.26, 0.14), (0.50, 0.34, 0.20), rough=0.35)
    chair_fab = SK.fabric("club-chair", (0.62, 0.55, 0.45))
    arm_fab = SK.fabric("club-armchair", (0.30, 0.34, 0.30))
    arm_leather = SK.leather("club-leather", (0.16, 0.08, 0.04))
    rug = SK.rugmat("club-rug", (0.70, 0.66, 0.58))
    black = mat("matte-black", (0.03, 0.03, 0.03), 0.45, 0.6)
    mirror = mat("mirror", (0.9, 0.9, 0.9), 0.02, 1.0)
    brass = SK.metal("brass")
    globe = SK.glow()
    dl = mat("club-downlight", (1, 1, 1), 0.5, emission=((1.0, 0.86, 0.70), 30.0))
    strip = mat("led-strip", (1, 1, 1), 0.5, emission=((1.0, 0.84, 0.66), 14.0))
    pot = vary(mat("club-pot", (0.72, 0.66, 0.58), 0.8), 0.1, 3.0)
    lb = mat("gym-light", (1, 1, 1), 0.5, emission=((1.0, 0.94, 0.86), 16.0))

    CA = 2.4                                       # the club's back wall across the tower; the club takes the south end
    GB = -3.6                                      # the glass partition of the gym corner (grid east of it)
    # floors: oak planks in the lounge, rubber in the gym; the ceiling; the back wall with a door
    cap("club-floor", tLoop, F, oak, thick=0.05)
    a_end = AL * math.sqrt(max(0, 1 - (GB / BL) ** 2))
    gym_poly = [TP(CA, GB)]
    for i in range(41):
        a_ = CA + (a_end - CA) * i / 40
        b_ = -half_width(a_, AL, BL)
        if b_ < GB:
            gym_poly.append(TP(a_, b_ - 0.0))
    gym_poly.append(TP(a_end, GB))
    prism_l("gym-floor", [(p[0], p[1]) for p in gym_poly], F, F + 0.012, rubber)
    cap("club-ceiling", tLoop, CEIL + 0.02, plaster, thick=0.02)
    hw = half_width(CA, AL, BL)
    tbox("club-back-wall", CA - 0.15, 0.0, F, CEIL, 0.3, 2 * hw - 0.05, plaster, 0.01)
    tbox("club-door", CA + 0.005, 9.3, F, F + 2.4, 0.04, 1.0, shelf_oak, 0.004)
    tbox("club-door-frame", CA + 0.01, 9.3, F + 2.4, F + 2.46, 0.05, 1.1, black, 0.002)
    # a library wall of oak shelves with books and objects, west of the kitchenette
    LB0, LB1 = 4.9, 8.5
    tbox("library-back", CA + 0.02, (LB0 + LB1) / 2, F, CEIL, 0.04, LB1 - LB0, shelf_oak, 0.0)
    for k in range(6):
        tbox("library-shelf-%d" % k, CA + 0.19, (LB0 + LB1) / 2, F + 0.02 + k * 0.52, F + 0.05 + k * 0.52, 0.34, LB1 - LB0, shelf_oak, 0.004)
    for k in range(5):
        tbox("library-side-%d" % k, CA + 0.19, LB0 + k * (LB1 - LB0) / 4, F, F + 2.65, 0.34, 0.04, shelf_oak, 0.004)
    book_cols = [(0.62, 0.55, 0.45), (0.2, 0.24, 0.26), (0.55, 0.3, 0.18), (0.82, 0.78, 0.7), (0.3, 0.34, 0.3), (0.12, 0.12, 0.12)]
    book_m = [SK.paint("club-book-%d" % i, c, 0.7) for i, c in enumerate(book_cols)]
    for sh in range(1, 5):
        bb = LB0 + 0.1
        while bb < LB1 - 0.15:
            if rnd.random() < 0.18:
                bb += 0.35
                continue
            w_ = rnd.uniform(0.025, 0.05)
            h_ = rnd.uniform(0.2, 0.3)
            tbox("club-book-%d-%d" % (sh, int(bb * 100)), CA + 0.2, bb, F + 0.05 + sh * 0.52, F + 0.05 + sh * 0.52 + h_, 0.2, w_,
                 book_m[rnd.randrange(len(book_m))], 0.0)
            bb += w_ + 0.004
    # the kitchenette bar on the back wall: green fronts, a stone counter, oak shelves, a fridge column, a coffee machine
    KB0, KB1 = -2.6, 3.8
    kb = (KB0 + KB1) / 2
    tbox("kitchen-run", CA + 0.31, kb, F + 0.1, F + 0.9, 0.62, KB1 - KB0, green, 0.006)
    tbox("kitchen-plinth", CA + 0.33, kb, F, F + 0.1, 0.56, KB1 - KB0, black, 0.0)
    tbox("kitchen-top", CA + 0.33, kb, F + 0.9, F + 0.94, 0.68, KB1 - KB0 + 0.04, counter, 0.004)
    tbox("kitchen-splash", CA + 0.01, kb, F + 0.94, F + 1.5, 0.02, KB1 - KB0, counter, 0.0)
    for k, zz in enumerate((1.75, 2.2)):
        tbox("shelf-%d" % k, CA + 0.16, kb - 0.6, F + zz, F + zz + 0.04, 0.3, KB1 - KB0 - 1.4, shelf_oak, 0.004)
    tbox("under-shelf-led", CA + 0.28, kb - 0.6, F + 1.745, F + 1.75, 0.02, KB1 - KB0 - 1.5, strip, 0.0)
    tbox("fridge-column", CA + 0.33, KB1 + 0.45, F, F + 2.3, 0.66, 0.9, green, 0.008)
    tbox("coffee-machine", CA + 0.3, KB0 + 0.7, F + 0.94, F + 1.34, 0.42, 0.36, M["steel"], 0.02)
    tbox("sink", CA + 0.33, kb + 0.6, F + 0.935, F + 0.945, 0.42, 0.6, M["steel"], 0.0)
    tcyl("tap", *[CA + 0.1, kb + 0.6], F + 0.94, F + 1.25, 0.012, M["steel"], 10)
    # cups and jars on the shelves
    for k in range(9):
        tcyl("jar-%d" % k, CA + 0.16, kb - 2.4 + k * 0.42, F + 1.79 + (k % 2) * 0.45, F + 1.79 + (k % 2) * 0.45 + 0.12 + (k % 3) * 0.05,
             0.05 + (k % 2) * 0.015, [counter, shelf_oak, M["rail-glass"]][k % 3], 16)
    # the bar island with four stools
    IA = CA + 1.9
    tbox("island", IA, kb, F, F + 0.95, 0.9, 3.2, table_oak, 0.01)
    tbox("island-top", IA, kb, F + 0.95, F + 1.0, 1.1, 3.4, counter, 0.006)
    for k in range(4):
        sb = kb - 1.2 + k * 0.8
        tcyl("stool-seat-%d" % k, IA + 0.85, sb, F + 0.68, F + 0.74, 0.19, arm_leather, 28)
        tcyl("stool-pole-%d" % k, IA + 0.85, sb, F + 0.02, F + 0.68, 0.02, black, 10)
        tcyl("stool-foot-%d" % k, IA + 0.85, sb, F, F + 0.02, 0.2, black, 28)
        tcyl("stool-ring-%d" % k, IA + 0.85, sb, F + 0.28, F + 0.3, 0.14, black, 24)
    for k in range(3):
        tball("bar-globe-%d" % k, IA, kb - 1.0 + k * 1.0, F + 2.0, 0.13, globe)
        tcyl("bar-cord-%d" % k, IA, kb - 1.0 + k * 1.0, F + 2.13, CEIL, 0.004, brass, 6)
        x_, y_ = TB(IA, kb - 1.0 + k * 1.0)
        light("bar-light-%d" % k, "POINT", (x_, y_, F + 1.78), 22.0, (1.0, 0.8, 0.58), size=0.1)
    # the long table for ten under a linear pendant
    LA, LB = 7.9, 0.4
    tbox("long-table", LA, LB, F + 0.72, F + 0.77, 1.05, 4.2, table_oak, 0.012)
    for t in (-1, 1):
        tbox("long-table-leg-%d" % t, LA, LB + t * 1.75, F, F + 0.72, 0.9, 0.08, black, 0.006)
    for side in (-1, 1):
        for k in range(5):
            cb = LB - 1.6 + k * 0.8
            ca_ = LA + side * 0.78
            tbox("lt-chair-seat-%d-%d" % (side, k), ca_, cb, F + 0.43, F + 0.49, 0.46, 0.46, chair_fab, 0.025, 3)
            tbox("lt-chair-back-%d-%d" % (side, k), ca_ + side * 0.21, cb, F + 0.49, F + 0.86, 0.05, 0.44, chair_fab, 0.02, 3)
            for u in (-1, 1):
                for v in (-1, 1):
                    tbox("lt-chair-leg-%d-%d-%d-%d" % (side, k, u, v), ca_ + u * 0.19, cb + v * 0.19, F, F + 0.43, 0.025, 0.025, black, 0.003)
    tbox("linear-pendant", LA, LB, F + 1.85, F + 1.9, 0.12, 3.2, black, 0.01)
    tbox("linear-pendant-diffuser", LA, LB, F + 1.845, F + 1.85, 0.08, 3.1, strip, 0.0)
    for t in (-1, 1):
        tcyl("linear-cord-%d" % t, LA, LB + t * 1.4, F + 1.9, CEIL, 0.004, black, 6)
    lo = light("table-light", "AREA", (*TB(LA, LB), F + 1.83), 140.0, (1.0, 0.84, 0.66), size=0.1, size_y=3.0)
    lo.rotation_euler = (0, 0, -TR)
    tcyl("table-vase", LA, LB + 0.5, F + 0.77, F + 1.05, 0.07, SK.paint("vase", (0.9, 0.88, 0.84), 0.35), 20)
    # a floating ceiling of oak slats over the long table
    for k in range(13):
        tbox("club-ceiling-slat-%d" % k, LA - 0.9 + k * 0.15, LB, CEIL - 0.24, CEIL - 0.18, 0.05, 5.0, shelf_oak, 0.004, 2)
    # a lounge by the west glass: a sofa, two armchairs, a coffee table, a rug, a lamp
    WA, WB = 9.0, 6.4
    tbox("west-rug", WA, WB, F, F + 0.012, 3.6, 3.0, SK.rugmat("club-rug-2", (0.46, 0.42, 0.36)), 0.0)
    sofa2 = SK.fabric("club-sofa", (0.70, 0.66, 0.58))
    tbox("west-sofa-base", WA, WB + 1.25, F + 0.1, F + 0.4, 2.5, 0.95, sofa2, 0.03)
    tbox("west-sofa-seat", WA, WB + 1.19, F + 0.4, F + 0.55, 2.3, 0.78, sofa2, 0.07, 4)
    tbox("west-sofa-back", WA, WB + 1.6, F + 0.4, F + 0.88, 2.4, 0.22, sofa2, 0.08, 4)
    for t in (-1, 1):
        tbox("west-sofa-arm-%d" % t, WA + t * 1.15, WB + 1.25, F + 0.1, F + 0.64, 0.2, 0.95, sofa2, 0.06, 4)
        tbox("west-cushion-%d" % t, WA + t * 0.8, WB + 1.45, F + 0.55, F + 0.95, 0.46, 0.14, arm_leather, 0.06, 4, rot=0.2 * t)
    tbox("west-table", WA, WB, F, F + 0.36, 1.2, 0.7, SK.stone("club-table-stone", (0.30, 0.28, 0.26), rough=0.25), 0.03)
    for t in (-1, 1):
        ca_, cb_ = WA + t * 0.75, WB - 1.15
        tbox("west-arm-seat-%d" % t, ca_, cb_, F + 0.18, F + 0.44, 0.8, 0.8, arm_fab, 0.07, 4)
        tbox("west-arm-back-%d" % t, ca_, cb_ - 0.34, F + 0.4, F + 0.84, 0.8, 0.16, arm_fab, 0.07, 4)
        for u in (-1, 1):
            tbox("west-arm-arm-%d-%d" % (t, u), ca_ + u * 0.38, cb_, F + 0.18, F + 0.6, 0.12, 0.8, arm_fab, 0.05, 4)
    for i_, bm_ in enumerate(book_m[:3]):
        tbox("west-book-%d" % i_, WA - 0.2, WB + 0.05, F + 0.36 + i_ * 0.03, F + 0.39 + i_ * 0.03, 0.26, 0.2, bm_, 0.003, rot=0.12 * i_)
    tcyl("west-bowl", WA + 0.3, WB - 0.1, F + 0.36, F + 0.44, 0.13, brass, 32, r2=0.09)

    for k in range(3):
        tcyl("table-candle-%d" % k, LA + 0.1, LB - 1.0 + k * 0.3, F + 0.77, F + 0.95, 0.025, SK.paint("candle", (0.92, 0.9, 0.85), 0.6), 12)
    # armchairs by the south glass around a low table on a rug, a floor lamp, plants
    RA, RB = 12.2, 2.6
    tbox("club-rug", RA, RB, F, F + 0.012, 2.8, 3.4, rug, 0.0)
    tcyl("low-table", RA, RB, F, F + 0.36, 0.5, table_oak, 40)
    for k, (da, db, m_) in enumerate(((-1.05, -0.6, arm_fab), (-1.05, 0.7, arm_fab), (1.0, 1.15, arm_leather), (0.9, -1.2, arm_leather))):
        rot = math.atan2(db, -da)
        ca_, cb_ = RA + da, RB + db
        ux, ub = -da / math.hypot(da, db), -db / math.hypot(da, db)
        tbox("arm-seat-%d" % k, ca_, cb_, F + 0.18, F + 0.44, 0.8, 0.8, m_, 0.07, 4, rot=rot)
        tbox("arm-back-%d" % k, ca_ - ux * 0.34, cb_ - ub * 0.34, F + 0.4, F + 0.84, 0.16, 0.8, m_, 0.07, 4, rot=rot)
        for t in (-1, 1):
            tbox("arm-arm-%d-%d" % (k, t), ca_ - ub * t * 0.38, cb_ + ux * t * 0.38, F + 0.18, F + 0.6, 0.8, 0.12, m_, 0.05, 4, rot=rot)
    tcyl("floor-lamp-base", RA - 1.6, RB + 1.5, F, F + 0.02, 0.16, brass, 24)
    tcyl("floor-lamp-pole", RA - 1.6, RB + 1.5, F, F + 1.5, 0.012, brass, 8)
    shade = SK.fabric("club-shade", (0.93, 0.9, 0.84), 0.9)
    _p(shade).inputs["Transmission Weight"].default_value = 0.6
    tcyl("floor-lamp-shade", RA - 1.6, RB + 1.5, F + 1.36, F + 1.66, 0.2, shade, 32)
    x_, y_ = TB(RA - 1.6, RB + 1.5)
    light("floor-lamp", "POINT", (x_, y_, F + 1.5), 45.0, (1.0, 0.8, 0.58), size=0.12)
    for k, (a_, b_, r_) in enumerate(((11.4, 6.9, 0.9), (14.6, 4.2, 0.8), (13.6, -2.6, 0.7))):
        tcyl("club-pot-%d" % k, a_, b_, F, F + 0.6, 0.34, pot, 32, r2=0.3)
        x_, y_ = TB(a_, b_)
        tree("club-plant-%d" % k, x_, -y_, F + 0.6, r_ * 0.8, material=M["tree"], fine=True)
    # the gym corner behind a glass partition: two treadmills facing the glass, a bench, a dumbbell rack, a mirror wall
    tbox("gym-partition-glass", (CA + a_end) / 2, GB, F, CEIL, a_end - CA - 0.1, 0.012, M["glass"], 0.0)
    for k in range(int((a_end - CA) / 1.4) + 1):
        tbox("gym-partition-post-%d" % k, CA + k * 1.4, GB, F, CEIL, 0.05, 0.05, black, 0.004)
    tbox("gym-partition-head", (CA + a_end) / 2, GB, CEIL - 0.06, CEIL, a_end - CA, 0.06, black, 0.0)
    tbox("gym-partition-sill", (CA + a_end) / 2, GB, F, F + 0.05, a_end - CA, 0.06, black, 0.0)
    tbox("gym-mirror", CA + 0.02, (GB - hw) / 2, F + 0.3, F + 2.3, 0.02, abs(-hw - GB) - 0.8, mirror, 0.004)
    for k, tb_ in enumerate((-5.1, -6.7)):
        ta = 9.2
        tbox("treadmill-deck-%d" % k, ta, tb_, F, F + 0.22, 1.9, 0.8, black, 0.03)
        tbox("treadmill-belt-%d" % k, ta, tb_, F + 0.22, F + 0.24, 1.6, 0.52, SK.paint("belt", (0.02, 0.02, 0.02), 0.7), 0.004)
        for t in (-1, 1):
            obox("treadmill-upright-%d-%d" % (k, t), (*TB(ta + 0.85, tb_ + t * 0.36), F + 0.7), (0.07, 0.06, 1.0), black,
                 yaw=-TR, tilt=math.radians(-12), bev=0.01)
        obox("treadmill-console-%d" % k, (*TB(ta + 1.0, tb_), F + 1.28), (0.28, 0.72, 0.05), black, yaw=-TR, tilt=math.radians(-35), bev=0.01)
        obox("treadmill-screen-%d" % k, (*TB(ta + 0.985, tb_), F + 1.29), (0.2, 0.4, 0.052), SK.paint("screen", (0.05, 0.08, 0.1), 0.1),
             yaw=-TR, tilt=math.radians(-35))
    tbox("bench-pad", 6.0, -6.2, F + 0.38, F + 0.48, 1.2, 0.3, SK.leather("bench-leather", (0.04, 0.04, 0.04)), 0.03, 3)
    tbox("bench-frame", 6.0, -6.2, F, F + 0.38, 1.0, 0.1, M["steel"], 0.01)
    tbox("bench-foot", 6.0, -6.2, F, F + 0.05, 0.1, 0.5, M["steel"], 0.01)
    tbox("rack", 4.1, -7.1, F, F + 0.85, 0.55, 1.8, black, 0.01)
    for row, zz in enumerate((0.45, 0.9)):
        for k in range(5):
            bb = -7.8 + k * 0.35
            rr = 0.045 + 0.008 * k
            zc = F + zz + rr
            ob = tcyl("dumbbell-bar-%d-%d" % (row, k), 4.1, bb, zc - 0.17, zc + 0.17, 0.016, M["steel"], 10)
            ob.rotation_euler = (math.radians(90), 0, -TR + math.pi / 2)
            for t in (-1, 1):
                ob = tcyl("dumbbell-%d-%d-%d" % (row, k, t), 4.1 + t * 0.13, bb, zc - 0.035, zc + 0.035, rr, black, 20)
                ob.rotation_euler = (math.radians(90), 0, -TR + math.pi / 2)
    tbox("yoga-mat", 7.0, -8.2, F + 0.012, F + 0.02, 1.8, 0.6, SK.paint("mat", (0.30, 0.38, 0.36), 0.8), 0.0)
    for k in range(4):
        a_ = CA + 1.4 + k * 2.6
        if a_ < a_end - 0.5:
            tbox("gym-light-%d" % k, a_, (GB - half_width(a_, AL, BL)) / 2, CEIL - 0.04, CEIL, 1.2, 0.06, lb, 0.0)
    # the glass line: slim frames, the terrace (the base floor's own balcony band) outside
    glass_mullions("club-mullion", tLoop, T_["y0"] - 0.1, CEIL + 0.3, lambda a_, b_: a_ > CA - 0.5, 0.1, 1.5)
    spots = []
    for a_ in (4.0, 6.2, 8.4, 10.6, 12.8, 15.0):
        for b_ in (-1.8, 0.6, 3.0, 5.4, 7.8):
            if (a_ / (AL - 0.8)) ** 2 + (b_ / (BL - 0.8)) ** 2 < 1 and not (LA - 1.2 < a_ < LA + 1.2 and -2.3 < b_ < 3.0) and abs(a_ - IA) > 0.8:
                spots.append((a_, b_))
    downlights("club-dl", spots, CEIL, dl)
    for (a_, b_) in spots:
        x, y = TB(a_, b_)
        lo = light("club-dl-light-%d-%d" % (int(a_ * 10), int(b_ * 10)), "AREA", (x, y, CEIL - 0.03), 22.0, (1.0, 0.84, 0.66), size=0.12)
        lo.data.shape = "DISK"
    fill_light("club-fill", AL - 1.3, 0.0, CEIL - 0.3, 10.0, 1.2, 120.0, (-1, 0))

    ca, cb = 5.9, 4.3
    ex, ez = TP(ca, cb)
    tx, tz = TP(ca + 4.0, cb - 1.0)
    centre = place_camera(ex, ez, F + 1.6, tx - ex, tz - ez)
    print("ILLUSTRATION club: the Rainbow Club on the tower's base floor, courtyard side (the stage's tower:court pin), floor %.2f m, "
          "ceiling %.2f m, eye %.2f m; panorama centre bearing %.1f" % (F, CEIL, F + 1.6, centre))


{"roofpool": build_roofpool, "lobby": build_lobby, "club": build_club}[SCENE]()

# every object that is not the camera, the sun or the site itself stands in the grid frame
for ob in bpy.data.objects:
    if ob.parent is None and ob.name not in ("site", "sun"):
        ob.parent = SITE

PROBE = os.environ.get("RBF_PROBE")          # diagnostics: "yaw:pitch,yaw:pitch" -> what the camera's ray hits there
if PROBE:
    dg = bpy.context.evaluated_depsgraph_get()
    cw = cam.matrix_world
    for item in PROBE.split(","):
        yw, pt = (math.radians(float(v)) for v in item.split(":"))
        d_local = Vector((math.sin(yw) * math.cos(pt), math.sin(pt), -math.cos(yw) * math.cos(pt)))
        d_world = (cw.to_3x3() @ d_local).normalized()
        o = cw.translation.copy()
        for hop in range(6):
            hit, loc, nrm, idx, obj, _ = scene.ray_cast(dg, o, d_world)
            if not hit:
                print("PROBE", item, "hop", hop, "-> sky")
                break
            print("PROBE", item, "hop", hop, "->", obj.name, obj.active_material.name if obj.active_material else "-", "%.2f m" % (loc - cw.translation).length)
            o = loc + d_world * 0.002
    sys.exit(0)
LOCATE = os.environ.get("RBF_LOCATE")        # diagnostics: "name,name" -> each object's centre as yaw:pitch (degrees, + = right/up)
if LOCATE:                                   # (the doors between the 360 rooms, design system BuildingWalk)
    bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted()
    for name in LOCATE.split(","):
        ob = bpy.data.objects.get(name)
        if not ob:
            print("LOCATE", name, "-> missing")
            continue
        c = sum((ob.matrix_world @ Vector(v) for v in ob.bound_box), Vector()) / 8.0
        p = inv @ c
        print("LOCATE %s yaw %+.2f pitch %+.2f dist %.2f m" % (name, math.degrees(math.atan2(p.x, -p.z)), math.degrees(math.atan2(p.y, math.hypot(p.x, p.z))), p.length))
    sys.exit(0)
print("scene", SCENE, "| %d objects" % len(bpy.data.objects), "| %d x %d, %d samples, %d threads" % (WIDTH, WIDTH // 2, SAMPLES, THREADS))
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("wrote", OUT)
