# -*- coding: utf-8 -*-
"""DUO Tel Aviv's world for the 360 panoramas (duo_facility.py, duo_interior.py): the site and the city as the DUO stage
draws them (plugins/nadlan-config/assets/project-stage/duo/stage.js, buildWorld and its constants), rebuilt for Cycles.

Imported by the scene scripts inside Blender (it builds nothing on import; init() starts a scene). The materials and mesh
helpers are rainbow_facility.py's, copied here so no Rainbow file changes.

What the stage's numbers are (stage.js header; docs/research/2026-09-28-stages/stage-geometry.md, section 3):
  OFFICIAL      the lot outline (GIS 837, lots 111 + 112 of plan 2988א, 8,338 m², the permit's site); both towers'
                footprints (GIS 513 oids 44499 and 42941, 1,082 and 918 m²), the towers in the east half, three commercial
                buildings and a sunken courtyard in the west half (licensing decision 1-25-0172, 21.9.2025); 50 residential
                floors, penthouses on 48-50, private pools on 49-50, technical floors 51-52 (54 floors in all, with the
                gallery floor and the ground floor); the city standing today (city.json: TLV GIS layers 513 buildings at
                their recorded heights, 837 lots, 507/508 streets, 503 green areas, 628 trees, 579 beaches).
  DEVELOPER     the lobby of about 7 m joining the towers, the infinity pool and a toddler pool on the lobby building's roof,
                the wellness complex, the gym and the residents' club (duo-tlv.com, residential-towers).
  ILLUSTRATION  every height: no official height or floor-to-floor height exists, so the stage uses 3.3 m a floor over a
                7.0 m lobby (floor 1 at 8.6 m, floor 25 at 87.8 m, the roof of floor 50 at 173.6 m, the crown at 185.8 m);
                the lobby building's outline, the commercial buildings' shapes and places inside the west half, the
                courtyard's shape, the pools' shapes, the balconies and the facade.
Frame: stage-local metres, x = grid east, z = grid south, from the area-weighted centroid of lots 111 + 112 (32.085698,
34.782856); the grid is turned 10° east of true north (GRID_ANGLE). Blender builds every object in the grid frame
(Blender x = stage x, Blender y = -stage z, Blender z = up) and parents it to the empty SITE, turned as the stage turns its
site group, so a grid bearing + 10° is the true bearing."""
import json, math, os, random, sys

import bmesh
import bpy
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import studio_kit as SK  # noqa: E402

REPO = os.path.dirname(os.path.dirname(HERE))
DUO = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "duo")
CITY = os.path.join(DUO, "city.json")
QUARTER = os.path.join(DUO, "quarter.json")

# ---------------------------------------------------------------- the stage's numbers (duo/stage.js, verbatim)
G = math.radians(-10)                     # GRID_ANGLE
PLOT_H = 1.2                              # PLOT.h: the plaza (plinth) above the street
Y = PLOT_H
LOT_OUTLINE = [(-42.3, -48.5), (44.5, -49.0), (44.6, -5.8), (40.0, -5.7), (40.0, 1.7), (39.7, 37.2), (39.3, 41.0), (37.9, 44.5),
               (34.6, 48.4), (32.6, 50.0), (28.1, 51.8), (25.7, 52.1), (-41.9, 48.6), (-42.1, 2.2)]
FH = 3.3                                  # a floor (illustration: no official floor height)
LOBBY_H = 7.0                             # the lobby, about 7 m (the developer)
Y0 = PLOT_H + LOBBY_H + 0.4               # floor 1's level, 8.6 m
FLOORS = 50
PH_FROM = 48
TECH_H = 4.4
TOWERS = [
    dict(id="N", k=1, poly=[(1.13, -45.65), (31.64, -45.96), (31.46, -10.86), (-0.11, -11.01)]),
    dict(id="S", k=2, poly=[(1.55, 17.28), (33.94, 17.11), (32.78, 46.12), (1.48, 45.9)]),
]
for _T in TOWERS:
    _T["cx"] = sum(p[0] for p in _T["poly"]) / 4
    _T["cz"] = sum(p[1] for p in _T["poly"]) / 4
    _T["roof"] = Y0 + FLOORS * FH         # 173.6
    _T["top"] = _T["roof"] + 2 * TECH_H + 3.4
TOWER_BY = {T["id"]: T for T in TOWERS}
LOBBY = [(2.2, -11.0), (31.0, -10.9), (31.6, 17.1), (2.2, 17.2)]
LB_XW, LB_XE = min(LOBBY[0][0], LOBBY[3][0]), max(LOBBY[1][0], LOBBY[2][0])
LB_ZN, LB_ZS = max(LOBBY[0][1], LOBBY[1][1]), min(LOBBY[2][1], LOBBY[3][1])
DECK_Y = PLOT_H + LOBBY_H                 # the pool deck: the lobby building's roof, 8.2 m
POOL = dict(cx=8.6, cz=3.0, w=8.0, d=21.0)        # the infinity pool along the deck's west edge (illustration)
KIDPOOL = dict(cx=16.4, cz=-6.2, w=4.6, d=3.6)    # the toddler pool (the developer; its place an illustration)
RETAIL = [
    dict(id="w", poly=[(-40.6, -33.0), (-31.0, -33.0), (-31.0, 31.0), (-40.2, 31.0)], floors=4, roof=True),
    dict(id="n", poly=[(-28.4, -47.0), (-5.0, -47.2), (-5.0, -30.6), (-28.4, -30.6)], floors=3, roof=False),
    dict(id="s", poly=[(-28.4, 30.0), (-5.0, 30.0), (-5.0, 47.4), (-28.4, 47.0)], floors=3, roof=False),
]
RETAIL_FH = 4.6
COURT = dict(x0=-27.0, x1=-6.4, z0=-24.0, z1=24.0, floor=-4.6)
EYE_M = 1.6
C45 = math.sqrt(0.5)


def floor_level(n):
    return Y0 + (n - 1) * FH


def smoothstep(a, b, x):
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


# module state, set by init()
scene = None
SITE = None
M = {}
rnd = random.Random(11)


# ---------------------------------------------------------------- render setup (rainbow_facility.py's pipeline)
def init(width, samples, threads, exposure, glossy=8):
    global scene, SITE, M, rnd
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.02
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 8
    scene.cycles.diffuse_bounces = 4
    scene.cycles.glossy_bounces = glossy
    scene.cycles.transmission_bounces = 8
    scene.cycles.transparent_max_bounces = 32
    scene.cycles.sample_clamp_indirect = 8.0
    scene.render.resolution_x = width
    scene.render.resolution_y = width // 2
    scene.render.resolution_percentage = 100
    scene.render.threads_mode = "FIXED"     # always: other renders share this machine
    scene.render.threads = max(1, threads)
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = exposure
    SITE = bpy.data.objects.new("site", None)
    bpy.context.collection.objects.link(SITE)
    SITE.rotation_euler = (0, 0, G)
    rnd = random.Random(11)
    M = make_materials()
    return scene


# ---------------------------------------------------------------- materials (rainbow_facility.py)
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
    """thin clear glass: a clear sheet with a Fresnel reflection and no refraction, transparent to shadow rays (both faces
    reflect as glass does from the air, so nothing seen edge-on turns black)"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    lp = nt.nodes.new("ShaderNodeLightPath")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); tr.inputs["Color"].default_value = (*tint, 1)
    gl = nt.nodes.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.02
    fr = nt.nodes.new("ShaderNodeFresnel")
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
    frames at every panel and floor line and a slight tone change from pane to pane"""
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
    """pool water: a refracting surface (IOR 1.333) that reflects the sky by Fresnel, a gentle wave bump, clear to shadow
    rays so the sun still lights the pool's tiles"""
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
    """tiles on every face: a brick pattern fed by object coordinates projected on the face's dominant plane"""
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
    """honed stone or porcelain in large tiles: a cloudy tone, each tile a little lighter or darker, recessed joints,
    a soft change of sheen (box-mapped, so walls get tiles too)"""
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
    """leaves in mass: clumps (Voronoi) and fine noise, a strong bump so a canopy reads as leaves and not as a ball"""
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
    """a leaf: tone drifting from leaf to leaf, a soft sheen, some light through it when the sun is behind"""
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
    """aerial perspective: the base colour drifts to the haze with distance from the camera"""
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


def make_materials():
    Mx = {
        "white": add_noise_bump(vary(mat("render-white", (0.86, 0.85, 0.82), 0.62), 0.05, 0.35), 60.0, 0.03),
        "deckband": vary(mat("balcony-deck", (0.50, 0.46, 0.41), 0.55), 0.1, 1.2),
        "facade": facade_glass(),
        "glass": glass_mat(),
        "rail-glass": glass_mat("rail-glass", (0.90, 0.96, 0.94)),
        "frame": mat("frame", (0.05, 0.05, 0.05), 0.35, 0.7),
        "bronze": mat("bronze", (0.36, 0.25, 0.16), 0.32, 1.0),
        "steel": mat("steel", (0.62, 0.62, 0.62), 0.22, 1.0),
        "paving": stone_tiles("paving", (0.50, 0.48, 0.44), (1.2, 1.2), 0.006, 0.08, 0.6, 0.0, 0.3),
        "plinth": vary(mat("plinth-stone", (0.62, 0.59, 0.54), 0.7), 0.06, 0.8),
        "court": stone_tiles("court-paving", (0.56, 0.53, 0.48), (0.9, 0.9), 0.005, 0.07, 0.55, 0.0, 0.5),
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
        "green": mat("green-area", (0.07, 0.10, 0.05), 0.95),
        "sand": mat("sand", (0.40, 0.35, 0.27), 0.95),
        "prom": mat("promenade", (0.45, 0.42, 0.37), 0.8),
        "sea": mat("sea", (0.035, 0.15, 0.22), 0.11),
        "city": mat("city", (0.86, 0.82, 0.74), 0.8),
        "far": mat("far-city", (0.84, 0.81, 0.75), 0.8),
        "citytree": foliage_mat("city-tree", (0.05, 0.08, 0.035), (0.14, 0.19, 0.08)),
        "quarter": mat("quarter", (0.93, 0.91, 0.86), 0.7, alpha=0.45),
        "pool-water": water_mat(),
    }
    _p(Mx["sea"]).inputs["IOR"].default_value = 1.33
    _p(Mx["sea"]).inputs["Roughness"].default_value = 0.09
    add_noise_bump(Mx["sea"], 0.35, 0.05, 3.0)
    for k in ("ground", "street", "plate", "park", "green", "sand", "prom", "city", "far", "citytree"):
        hazed(Mx[k])
    return Mx


# ---------------------------------------------------------------- 2D helpers (stage frame: x grid east, z grid south)
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


def resample_loop(P, n, cw=0.0):
    """stage.js resampleLoop: a closed polyline resampled to n points by arc length plus extra weight on turns:
    [x, z, s, nx, nz] with s the arc fraction and n the outward normal"""
    Mn = len(P)
    ln = [math.dist(P[i], P[(i + 1) % Mn]) for i in range(Mn)]
    turn = []
    for i in range(Mn):
        a, b, c = P[i - 1], P[i], P[(i + 1) % Mn]
        d = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(b[1] - a[1], b[0] - a[0])
        turn.append(abs(math.atan2(math.sin(d), math.cos(d))))
    cumL, cumW = [0.0], [0.0]
    for i in range(Mn):
        cumL.append(cumL[-1] + ln[i])
        cumW.append(cumW[-1] + ln[i] + cw * 0.5 * (turn[i] + turn[(i + 1) % Mn]))
    L, W = cumL[Mn], cumW[Mn]
    pts, j = [], 0
    for k in range(n):
        target = k / n * W
        while j < Mn - 1 and cumW[j + 1] < target:
            j += 1
        seg = cumW[j + 1] - cumW[j]
        f = (target - cumW[j]) / seg if seg > 0 else 0
        a, b = P[j], P[(j + 1) % Mn]
        pts.append([a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, (cumL[j] + ln[j] * f) / L, 0.0, 0.0])
    return set_normals(pts)


def resample(P, n):
    return resample_loop(P, n, 0.0)


def offset(pts, d):
    return [[p[0] + p[3] * d, p[1] + p[4] * d, p[2], p[3], p[4]] for p in pts]


def loop_from_poly(P):
    """stage.js loopFromPoly: the polygon's own points, with outward normals (for straight-sided rectangles)"""
    pts = [[x, z, 0.0, 0.0, 0.0] for x, z in P]
    L = sum(math.dist(P[i], P[(i + 1) % len(P)]) for i in range(len(P)))
    acc = 0.0
    for i in range(len(P)):
        pts[i][2] = acc / L
        acc += math.dist(P[i], P[(i + 1) % len(P)])
    return set_normals(pts)


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


def in_poly(x, z, L):
    c = False
    j = len(L) - 1
    for i in range(len(L)):
        (xi, zi), (xj, zj) = L[i][:2], L[j][:2]
        if (zi > z) != (zj > z) and x < (xj - xi) * (z - zi) / (zj - zi) + xi:
            c = not c
        j = i
    return c


# ---------------------------------------------------------------- meshes (stage-local points -> the grid frame)
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


def drop_collinear(poly, tol=2e-4):
    """leave out the points that lie on the line of their neighbours (a straight side sampled every metre): an n-gon cap
    with collinear points triangulates into slivers whose normals shade black"""
    out = list(poly)
    changed = True
    while changed and len(out) > 3:
        changed = False
        for i in range(len(out)):
            a, b, c = out[i - 1], out[i], out[(i + 1) % len(out)]
            ux, uz, vx, vz = b[0] - a[0], b[1] - a[1], c[0] - b[0], c[1] - b[1]
            lu, lv = math.hypot(ux, uz), math.hypot(vx, vz)
            if lu < 1e-6 or lv < 1e-6 or abs(ux * vz - uz * vx) < tol * lu * lv and ux * vx + uz * vz > 0:
                del out[i]
                changed = True
                break
    return out


def prism_l(name, poly, z0, z1, material, top=True, bottom=True):
    """a vertical prism from a stage-local polygon (its caps triangulated cleanly)"""
    poly = drop_collinear(dedupe([tuple(p[:2]) for p in poly]))
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
    caps = [f for f in bm.faces if len(f.verts) > 4]
    if caps:
        bmesh.ops.triangulate(bm, faces=caps, quad_method="BEAUTY", ngon_method="BEAUTY")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material)
    return link(ob)


def box(name, cx, cy, cz, sx, sy, sz, material, rot=0.0):
    """a box in the grid frame's Blender coordinates (cx, cy = stage x, -z), turned rot about its centre"""
    c, s = math.cos(rot), math.sin(rot)
    pts = [(-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)]
    poly = [(cx + x * c - y * s, -(cy + x * s + y * c)) for x, y in pts]
    return prism_l(name, poly, cz - sz / 2, cz + sz / 2, material)


def gbox(name, x0, x1, z0, z1, y0, y1, material, bev=0.0, segs=3):
    """an axis-aligned box in stage coordinates: x0..x1 (grid east), z0..z1 (grid south), y0..y1 (up)"""
    ob = prism_l(name, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)], y0, y1, material)
    return SK.smooth_bevel(ob, bev, segs) if bev else ob


def obox(name, loc, size, material, yaw=0.0, tilt=0.0, bev=0.0, segs=3):
    """a box built at the origin and placed by its object transform (for tilted parts)"""
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


def loop_wall(name, pts, y0, y1, material, panel=1.5, row=3.3, v0=0.0, closed=True):
    """a vertical single-sided ribbon along a loop (closed) or a path, with UVs in panels (u) and floors (v)"""
    n = len(pts)
    verts, faces, uvs = [], [], []
    acc = 0.0
    for i in range(n + 1 if closed else n):
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
    """stage.js addBand: a floor band swept along a loop, depth(s) metres out: the floor, a rounded parapet Hp high and
    tp thick, the slab edge Ts deep with a rounded soffit corner rb"""
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


def plate(name, loop, y, D, Ts, rb, hb, white=None, deck=None):
    """stage.js addPlate: a floor plate grown out by the balcony depth D[i] at each loop point: its floor (deck), its
    rounded edge and soffit (white), and a glass balustrade hb metres high on the plate's outer line (hb 0: none)"""
    white = white or M["white"]
    deck = deck or M["deckband"]
    n = len(loop)
    out = set_normals([[p[0] + p[3] * D[i], p[1] + p[4] * D[i], p[2], 0.0, 0.0] for i, p in enumerate(loop)])
    strip = [("i", 0, 0), ("o", -0.02, 0), ("o", 0, -rb * 0.5), ("o", 0, -Ts + rb), ("o", -rb * (1 - C45), -Ts + rb * (1 - C45)),
             ("o", -rb, -Ts), ("i", 0, -Ts)]
    inset = 0.3
    m_ = len(strip)
    verts, faces, fm = [], [], []
    for i in range(n):
        p, o = loop[i], out[i]
        for k, u, v in strip:
            if k == "i":
                verts.append((p[0] - p[3] * inset, -(p[1] - p[4] * inset), y + v))
            else:
                verts.append((o[0] + o[3] * u, -(o[1] + o[4] * u), y + v))
    for i in range(n):
        i2 = (i + 1) % n
        for j in range(m_ - 1):
            faces.append((i * m_ + j, i2 * m_ + j, i2 * m_ + j + 1, i * m_ + j + 1))
            fm.append(1 if j == 0 else 0)
    ob = add_mesh(name, verts, faces, white, smooth=True, mats=[deck], sharp=48)
    for poly, mi in zip(ob.data.polygons, fm):
        poly.material_index = mi
    if hb > 0:
        rail = [[o[0] - o[3] * 0.06, o[1] - o[4] * 0.06, o[2], o[3], o[4]] for o in out]
        loop_wall(name + "-rail", rail, y, y + hb, M["rail-glass"], 1.2, 1.0)
    return ob, out


def smooth_box(name, cx, cy, cz, sx, sy, sz, material, rot=0.0, bev=0.01, segs=3):
    return SK.smooth_bevel(box(name, cx, cy, cz, sx, sy, sz, material, rot), bev, segs)


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
    """rainbow_facility.py's tree: a leaning trunk, branches spreading into the crown and thousands of leaf blades in
    clusters on an uneven shell, with a darker dense core. fine: small leaves for plants at arm's length"""
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


def shrub(name, x, z, y, r, lm=None):
    """a shrub at arm's length: a dense dome of small leaf blades on a dark core (y: the soil's level)"""
    lm = lm or (M["leaf"] if rnd.random() < 0.5 else M["leaf2"])
    cx, cy, cz = x, -z, y + r * 0.55
    count = int(1500 * (r / 0.4) ** 2)
    L, Wd = 0.09, 0.045
    verts, faces = [], []
    for k in range(count):
        u = rnd.uniform(-0.3, 1.0)
        th = rnd.random() * math.tau
        ring = math.sqrt(max(0.0, 1 - u * u))
        sh = 0.78 + 0.22 * rnd.random()
        pnt = Vector((cx + math.cos(th) * ring * r * sh, cy + math.sin(th) * ring * r * sh, cz + u * r * 0.8 * sh))
        az = rnd.random() * math.tau
        pit = math.radians(rnd.uniform(-50, 50))
        t = Vector((math.cos(az) * math.cos(pit), math.sin(az) * math.cos(pit), math.sin(pit)))
        sd = t.cross(Vector((0, 0, 1)))
        if sd.length < 1e-3:
            sd = Vector((1, 0, 0))
        sd.normalize()
        ls = L * rnd.uniform(0.7, 1.25)
        i0 = len(verts)
        verts += [tuple(pnt - t * ls * 0.5), tuple(pnt - t * ls * 0.1 + sd * Wd * 0.5), tuple(pnt + t * ls * 0.5),
                  tuple(pnt - t * ls * 0.1 - sd * Wd * 0.5)]
        faces.append((i0, i0 + 1, i0 + 2, i0 + 3))
    me_ = bpy.data.meshes.new(name + "-leaves")
    me_.from_pydata(verts, [], faces)
    me_.update()
    ob_ = bpy.data.objects.new(name + "-leaves", me_)
    ob_.data.materials.append(lm)
    link(ob_)
    ball(name + "-core", cx, cy, cz, r * 0.8, M["leaf-core"], scale=(1, 1, 0.85))


def simple_trees(name, spots, material):
    """many trees as one mesh (the city's trees, far from the eye): a trunk and a faceted canopy, as the stage draws them"""
    bm = bmesh.new()
    for (x, z, y, r) in spots:
        h = r * 1.25
        res = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6, radius1=0.18, radius2=0.13, depth=h)
        bmesh.ops.translate(bm, vec=(x, -z, y + h / 2), verts=res["verts"])
        for lobe in range(3):                        # a canopy of three soft lobes, not one faceted ball
            rr = r * (0.8 if lobe else 0.95)
            ox, oy = (0.0, 0.0) if not lobe else (math.cos(lobe * 2.4 + x) * r * 0.35, math.sin(lobe * 2.4 + z) * r * 0.35)
            res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
            bmesh.ops.scale(bm, vec=(rr, rr, rr * 0.82), verts=res["verts"])
            bmesh.ops.translate(bm, vec=(x + ox, -z + oy, y + h + r * (0.75 if not lobe else 0.55)), verts=res["verts"])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p_ in me.polygons:
        p_.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material)
    return link(ob)


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


# ================================================================ the world
def coast_x(z, cst):
    return cst["x0"] + cst["k"] * z


def build_ground_and_city(city_trees=True, fine_radius=0.0):
    """the land (the sunken courtyard cut out), the beach, the promenade and the sea on the coastline city.json fits
    through the city's beach polygons; the city as it stands (streets, plan lots, green areas, the buildings at their
    recorded heights, the far city as boxes to the sea, the city's trees); our other projects as pale masses"""
    city = json.load(open(CITY, encoding="utf-8"))
    cst = {"x0": float(city["coast"]["x0"]), "k": float(city["coast"]["k"])}
    ZA, ZB, FAR = -40000.0, 40000.0, 40000.0
    xc = lambda z: coast_x(z, cst)
    C = COURT
    for nm, poly in (("land-n", [(xc(ZA), ZA), (FAR, ZA), (FAR, C["z0"]), (xc(C["z0"]), C["z0"])]),
                     ("land-s", [(xc(C["z1"]), C["z1"]), (FAR, C["z1"]), (FAR, ZB), (xc(ZB), ZB)]),
                     ("land-w", [(xc(C["z0"]), C["z0"]), (C["x0"], C["z0"]), (C["x0"], C["z1"]), (xc(C["z1"]), C["z1"])]),
                     ("land-e", [(C["x1"], C["z0"]), (FAR, C["z0"]), (FAR, C["z1"]), (C["x1"], C["z1"])])):
        prism_l(nm, poly, -0.05, 0.0, M["ground"], bottom=False)
    prism_l("beach", [(xc(ZA), ZA), (xc(ZA) + 42, ZA), (xc(ZB) + 42, ZB), (xc(ZB), ZB)], 0.0, 0.12, M["sand"], bottom=False)
    prism_l("promenade", [(xc(ZA) + 42, ZA), (xc(ZA) + 56, ZA), (xc(ZB) + 56, ZB), (xc(ZB) + 42, ZB)], 0.0, 0.45, M["prom"], bottom=False)
    prism_l("sea", [(xc(ZA) - FAR, ZA), (xc(ZA) + 6, ZA), (xc(ZB) + 6, ZB), (xc(ZB) - FAR, ZB)], -0.35, -0.3, M["sea"])

    def pts_of(a, k):
        return [(a[i], a[i + 1]) for i in range(k, len(a) - 1, 2)]

    # streets (GIS 507/508 axes, a drawing width by class): ribbons, one mesh
    verts, faces = [], []
    for s in city.get("s", []):
        P = pts_of(s, 2)
        if len(P) < 2:
            continue
        w = float(s[0] or 10)
        base = len(verts)
        n = len(P)
        for i in range(n):
            p, q = P[max(0, i - 1)], P[min(n - 1, i + 1)]
            tx, tz = q[0] - p[0], q[1] - p[1]
            l = math.hypot(tx, tz) or 1
            tx, tz = tx / l, tz / l
            verts += [(P[i][0] - tz * w / 2, -(P[i][1] + tx * w / 2), 0.05), (P[i][0] + tz * w / 2, -(P[i][1] - tx * w / 2), 0.05)]
        for i in range(n - 1):
            faces.append((base + 2 * i, base + 2 * i + 2, base + 2 * i + 3, base + 2 * i + 1))
    add_mesh("streets", verts, faces, M["street"])
    plan_lots = []
    for i, l in enumerate(city.get("lots", [])):                 # the Somail plans' lots (GIS 837)
        poly = pts_of(l, 2)
        if len(poly) >= 3:
            prism_l("lot-%d" % i, poly, 0.0, 0.22 if l[0] == "park" else 0.3, M["park"] if l[0] == "park" else M["plate"], bottom=False)
            plan_lots.append(poly)
    for i, g in enumerate(city.get("g", [])):                    # green areas (GIS 503)
        poly = pts_of(g, 1)
        if len(poly) >= 3:
            prism_l("green-%d" % i, poly, 0.0, 0.26, M["green"], bottom=False)
    # the buildings standing today (GIS 513), at their recorded heights: one mesh
    bm = bmesh.new()
    for b in city.get("b", []):
        h = float(b[0])
        poly = [(x, -z) for x, z in pts_of(b, 3)]
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
    # the far city, each building as its box (x, z, w, d, turn in degrees, height), to the sea
    f = city.get("f", [])
    bm = bmesh.new()
    for i in range(0, len(f) - 5, 6):
        x, z, w, d, rot, h = f[i], f[i + 1], max(2.0, f[i + 2]), max(2.0, f[i + 3]), math.radians(f[i + 4]), f[i + 5]
        if h <= 0:
            continue
        P = rotate_poly([(x - w / 2, z - d / 2), (x + w / 2, z - d / 2), (x + w / 2, z + d / 2), (x - w / 2, z + d / 2)], x, z, rot)
        v0 = [bm.verts.new((px, -pz, 0)) for px, pz in P]
        v1 = [bm.verts.new((px, -pz, h)) for px, pz in P]
        bm.faces.new(v1)
        for a in range(4):
            c = (a + 1) % 4
            bm.faces.new((v0[a], v0[c], v1[c], v1[a]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("far-city")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("far-city", me)
    ob.data.materials.append(M["far"])
    link(ob)
    # the city's trees (GIS 628, their real positions)
    t = city.get("t", [])
    if city_trees and t:
        spots = [(t[i], t[i + 1], 0.05, 2.0 + rnd.random() * 1.3) for i in range(0, len(t) - 1, 2)]
        near = [s_ for s_ in spots if math.hypot(s_[0], s_[1]) < fine_radius]     # close to the eye: leaf by leaf
        for k, (x, z, y, r) in enumerate(near):
            tree("city-tree-%d" % k, x, z, y, r)
        simple_trees("city-trees", [s_ for s_ in spots if s_ not in near], M["citytree"])
    # our other projects in the quarter (quarter.json): pale schematic masses at their floors' height, on a plate
    q = json.load(open(QUARTER, encoding="utf-8"))
    cg, sg = math.cos(G), math.sin(G)
    for p in q.get("projects", []):
        X, Z = float(p["x"]), float(p["z"])
        lx, lz = X * cg - Z * sg, X * sg + Z * cg
        fl = float(p.get("floors") or 10)
        h = max(12.0, fl * 3.3 + 4)
        if not any(in_poly(lx, lz, L) for L in plan_lots):
            prism_l("q-%s-plate" % p["id"], round_rect(lx, lz, 64, 52, 8, 6), 0.0, 0.55, M["plate"], bottom=False)
        if fl >= 20:
            gbox("q-%s" % p["id"], lx - 12.5, lx + 12.5, lz - 12.5, lz + 12.5, 0.55, h, M["quarter"])
            gbox("q-%s-base" % p["id"], lx - 26, lx + 14, lz + 9.5, lz + 22.5, 0.55, 20, M["quarter"])
        else:
            gbox("q-%s" % p["id"], lx - 22, lx + 22, lz - 13, lz + 13, 0.55, h, M["quarter"])
    return cst


def build_lot(fine_trees=True):
    """DUO's lot: the plinth (the courtyard cut out), the sunken courtyard, the plaza's trees, the kerbs"""
    lot = ease_corners(LOT_OUTLINE, 1.6, 6)
    plinth = prism_l("lot-plinth", lot, 0.0, Y, M["paving"])
    C = COURT
    cutter = gbox("court-cutter", C["x0"], C["x1"], C["z0"], C["z1"], -6.0, Y + 1.0, M["white"])
    cutter.hide_render = True
    md = plinth.modifiers.new("court-hole", "BOOLEAN")
    md.operation = "DIFFERENCE"
    md.object = cutter
    try:
        md.solver = "EXACT"
    except TypeError:
        pass
    # the sunken courtyard (its shape and place an illustration): the floor, the stone walls, the lower level's shop
    # fronts on the long sides, a canopy ledge over them, a glass balustrade around the top, wide steps down at the south
    # end with two escalators beside them, planters with trees
    F = C["floor"]
    gbox("court-floor", C["x0"], C["x1"], C["z0"], C["z1"], F - 0.3, F, M["court"])
    for nm, (a, b, c, d) in (("w", (C["x0"] - 0.3, C["x0"], C["z0"] - 0.3, C["z1"] + 0.3)), ("e", (C["x1"], C["x1"] + 0.3, C["z0"] - 0.3, C["z1"] + 0.3)),
                             ("n", (C["x0"], C["x1"], C["z0"] - 0.3, C["z0"])), ("s", (C["x0"], C["x1"], C["z1"], C["z1"] + 0.3))):
        gbox("court-wall-" + nm, a, b, c, d, F, Y, M["plinth"])
    for nm, x in (("w", C["x0"] + 0.12), ("e", C["x1"] - 0.12)):
        loop_wall("court-shops-" + nm, [[x, C["z0"] + 0.4, 0, 0, 0], [x, C["z1"] - 9.6, 0, 0, 0]], F + 0.3, Y - 1.1, M["facade"], 3.0, 3.0, closed=False)
        xa = C["x0"] + 0.55 if nm == "w" else C["x1"] - 0.55
        gbox("court-ledge-" + nm, xa - 0.55, xa + 0.55, C["z0"], C["z1"], Y - 1.25, Y - 0.95, M["white"])
    rail = offset(loop_from_poly([(C["x0"], C["z0"]), (C["x1"], C["z0"]), (C["x1"], C["z1"]), (C["x0"], C["z1"])]), 0.3)
    loop_wall("court-rail", rail, Y, Y + 1.05, M["rail-glass"], 1.2, 1.0)
    band("court-rail-cap", rail, Y + 1.0, lambda s: 0.02, 0.06, 0.06, 0.08, 0.02, inset=0.0, floor=False, white=M["steel"])
    n, rise, run, sx0, sw = 26, (Y - F) / 26, 0.34, C["x0"] + 1.5, 7.5
    for i in range(n):
        zz = C["z1"] - (n - i) * run
        gbox("court-step-%d" % i, sx0, sx0 + sw, zz, C["z1"], F, F + (i + 1) * rise, M["court"])
    ln, ang = math.hypot(n * run, Y - F), math.atan2(Y - F, n * run)
    for k, ex in enumerate((sx0 + sw + 1.1, sx0 + sw + 2.8)):
        ob = obox("escalator-%d" % k, (ex, -(C["z1"] - n * run / 2), (F + Y) / 2 + 0.25), (1.25, ln, 0.55), M["steel"], 0.0, 0.0)
        ob.rotation_euler = (-ang, 0, 0)
    for k, (px, pz) in enumerate(((-13, -15), (-20, -3), (-11, 5), (-19, 12))):
        gbox("court-planter-%d" % k, px - 1.3, px + 1.3, pz - 1.3, pz + 1.3, F, F + 0.55, M["plinth"])
        gbox("court-planter-soil-%d" % k, px - 1.1, px + 1.1, pz - 1.1, pz + 1.1, F + 0.55, F + 0.6, M["soil"])
        if fine_trees:
            tree("court-tree-%d" % k, px, pz, F + 0.6, 1.9 + rnd.random() * 0.5)
    # the plaza's trees (illustration): a row between the courtyard and the lobby, a row along Ben Saruk
    spots = [(-3.2, z) for z in [-22 + 7.3 * i for i in range(7)]] + [(40.6, z) for z in [-40 + 9.4 * i for i in range(10)] if z <= 44]
    for k, (x, z) in enumerate(spots):
        gbox("plaza-pit-%d" % k, x - 0.9, x + 0.9, z - 0.9, z + 0.9, Y, Y + 0.02, M["soil"])
        if fine_trees:
            tree("plaza-tree-%d" % k, x, z, Y, 2.0 + rnd.random() * 0.5)
    if not fine_trees:
        simple_trees("plaza-trees", [(x, z, Y, 2.2) for x, z in spots], M["tree"])


def tower_loops(TW):
    fp = ease_corners(TW["poly"], 1.4, 5)
    loop = resample_loop(fp, 136, 4)
    xs = sorted(p[0] for p in TW["poly"])
    wMid, eMid = ((xs[0] + xs[1]) / 2, TW["cz"]), ((xs[2] + xs[3]) / 2, TW["cz"])
    D = []
    for p in loop:
        dc = min(math.hypot(p[0] - c[0], p[1] - c[1]) for c in TW["poly"])
        corner = 1 - smoothstep(5.8, 8.6, dc)
        onWE = abs(p[3]) > 0.85
        dm = min(math.hypot(p[0] - wMid[0], p[1] - wMid[1]), math.hypot(p[0] - eMid[0], p[1] - eMid[1])) if onWE else 1e9
        mid = 1 - smoothstep(4.2, 5.6, dm)
        D.append(0.42 + 1.95 * max(corner, mid * 0.82))
    return loop, D


def ph_pools(TW):
    P = sorted(TW["poly"], key=lambda p: p[0])
    w2 = sorted([P[0], P[1]], key=lambda p: p[1])
    NW, SW = w2
    L = math.dist(NW, SW)
    tx, tz = (SW[0] - NW[0]) / L, (SW[1] - NW[1]) / L
    nx, nz = tz, -tx
    if nx > 0:
        nx, nz = -nx, -nz
    return [dict(f=49, cx=NW[0] + tx * 4.0, cz=NW[1] + tz * 4.0, ux=tx, uz=tz, nx=nx, nz=nz),
            dict(f=50, cx=SW[0] - tx * 4.0, cz=SW[1] - tz * 4.0, ux=tx, uz=tz, nx=nx, nz=nz)]


def build_towers(clear_ground=(), room=None, ground_glass=True, skip_col=None):
    """the two towers as the stage draws them: the tall recessed ground-floor glass (the lobby) behind slim columns, the
    curtain wall of floors 1-47 on the footprint's line, the penthouse floors 48-50 set back 2.2 m, a floor plate with a
    glass balustrade on every floor (the balconies deep at the corners and in the middle of the west and east faces), the
    roof, the technical floors 51-52 set back, the crown's bronze fins, the private pools on floors 49 and 50.
    clear_ground: tower ids whose ground-floor glass is clear (a scene inside it). room: the example apartment's window
    (dict tower, y0, y1, face=(ax, az, ux, uz), half) where the curtain wall is left open."""
    info = {}
    for TW in TOWERS:
        tid = TW["id"]
        loop, D = tower_loops(TW)
        lobbyL = offset(loop, -1.7)
        # the setbacks: stage.js offsets the 1.4 m-eased loop by -2.2 and -3.2 m, more than the corners' radius, which folds
        # small spikes into the corners (hidden on the stage, not in a close render); floorPlan() in stage.js eases the
        # corners 4.1 m first so the line stays clean: the same here
        pent_base = resample_loop(ease_corners(TW["poly"], 4.1, 5), 136, 4)
        pentL = offset(pent_base, -2.2)
        techL = offset(pent_base, -3.2)
        Dp = [d + 2.2 for d in D]
        if ground_glass:
            loop_wall("t%s-ground-glass" % tid, lobbyL, Y, Y0, M["glass"] if tid in clear_ground else M["facade"], 1.5, Y0 - Y)
        step = max(1, round(len(loop) / 18))
        for i in range(0, len(loop), step):
            p = loop[i]
            if skip_col and skip_col(p[0], p[1]):
                continue
            cyl("t%s-column-%d" % (tid, i), p[0] - p[3] * 0.2, -(p[1] - p[4] * 0.2), Y, Y0 - 0.45, 0.42, M["white"], 24)
        cap("t%s-ground-ceiling" % tid, loop, Y0 - 0.46, M["white"])
        y_ph = floor_level(PH_FROM)
        if room and room["tower"] == tid:
            loop_wall("t%s-glass-lo" % tid, loop, Y0 - 0.5, room["y0"], M["facade"], 1.5, FH)
            loop_wall("t%s-glass-hi" % tid, loop, room["y1"], y_ph, M["facade"], 1.5, FH, (room["y1"] - Y0 + 0.5) / FH)
            # the room's floor: the curtain wall all round except the window (exact ends at the window's edges)
            ax, az, ux, uz = room["face"]
            half = room["half"]
            along = [(p[0] - ax) * ux + (p[1] - az) * uz for p in loop]
            across = [abs((p[0] - ax) * uz - (p[1] - az) * ux) for p in loop]
            inside = [abs(a) <= half + 1e-6 and c < 1.0 for a, c in zip(along, across)]
            n = len(loop)
            last_in = max(i for i in range(n) if inside[i] and not inside[(i + 1) % n])
            rest = [[ax + ux * half, az + uz * half, 0, 0, 0]] if along[last_in] > 0 else [[ax - ux * half, az - uz * half, 0, 0, 0]]
            k = (last_in + 1) % n
            while not inside[k]:
                rest.append(loop[k])
                k = (k + 1) % n
            end_sign = 1 if along[k] > 0 else -1
            rest.append([ax + ux * half * end_sign, az + uz * half * end_sign, 0, 0, 0])
            loop_wall("t%s-glass-room" % tid, rest, room["y0"], room["y1"], M["facade"], 1.5, FH, (room["y0"] - Y0 + 0.5) / FH, closed=False)
        else:
            loop_wall("t%s-glass" % tid, loop, Y0 - 0.5, y_ph, M["facade"], 1.5, FH)
        loop_wall("t%s-glass-pent" % tid, pentL, y_ph - 0.5, TW["roof"], M["facade"], 1.5, FH)
        for f in range(1, FLOORS + 1):
            ph = f >= PH_FROM
            plate("t%s-plate-%d" % (tid, f), pentL if ph else loop, floor_level(f), Dp if ph else D, 0.46, 0.1, 1.05)
        plate("t%s-roof-plate" % tid, pentL, TW["roof"], [d * 0.35 + 0.4 for d in Dp], 0.6, 0.12, 0)
        cap("t%s-roof" % tid, pentL, TW["roof"] + 0.01, M["white"])
        loop_wall("t%s-tech" % tid, techL, TW["roof"], TW["roof"] + 2 * TECH_H, M["white"], 1.5, TECH_H)
        cap("t%s-tech-roof" % tid, techL, TW["roof"] + 2 * TECH_H, M["white"])
        # the crown: bronze fins every ~1.25 m at the glass line, a band at the top
        per = sum(math.dist(loop[i][:2], loop[(i + 1) % len(loop)][:2]) for i in range(len(loop)))
        nF = round(per / 1.25)
        hf = TW["top"] - TW["roof"] - 0.4
        bm = bmesh.new()
        for k in range(nF):
            p = loop[int(k / nF * len(loop))]
            res = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(0.95, 0.16, hf), verts=res["verts"])      # 0.95 along the normal, 0.16 across
            ang = math.atan2(-p[4], p[3])                                       # the normal in Blender's frame
            bmesh.ops.rotate(bm, verts=res["verts"], cent=(0, 0, 0), matrix=Matrix.Rotation(ang, 3, "Z"))
            bmesh.ops.translate(bm, vec=(p[0] + p[3] * 0.2, -(p[1] + p[4] * 0.2), (TW["roof"] + TW["top"]) / 2 + 0.2), verts=res["verts"])
        me = bpy.data.meshes.new("t%s-fins" % tid)
        bm.to_mesh(me)
        bm.free()
        ob = bpy.data.objects.new("t%s-fins" % tid, me)
        ob.data.materials.append(M["bronze"])
        link(ob)
        band("t%s-crown" % tid, offset(loop, 0.35), TW["top"] - 0.5, lambda s: 0.3, 0.5, 0.4, 0.26, 0.1, inset=0.0, floor=False)
        # the private pools on the penthouse terraces (illustration of which terrace)
        for pp in ph_pools(TW):
            y = floor_level(pp["f"]) + 0.02
            rot = math.atan2(pp["uz"], pp["ux"])
            P = rotate_poly(round_rect(pp["cx"], pp["cz"], 2.2, 4.0, 0.4, 6), pp["cx"], pp["cz"], rot + math.pi / 2)
            prism_l("t%s-ph-pool-%d" % (tid, pp["f"]), P, y, y + 0.06, M["pool-water"])
            prism_l("t%s-ph-coping-%d" % (tid, pp["f"]), [(p[0], p[1]) for p in offset(resample(P, 60), 0.3)], y - 0.02, y + 0.03, M["white"])
        info[tid] = dict(loop=loop, D=D, lobbyL=lobbyL)
    return info


def build_lobby_building(glass=None, deck=True, pools=True):
    """the stage's lobby building between the towers: glass all round under a 1.0 m roof slab, the pool deck on the
    roof (its outline is not public: the towers' width, as an illustration), glass balustrades on the open west and east
    edges, the infinity pool, the toddler pool, loungers, the shade pergola and planters (the stage's simple forms)"""
    xW, xE, zN, zS = LB_XW, LB_XE, LB_ZN, LB_ZS
    if glass is not False:
        gl = loop_from_poly([(xW + 0.8, zN), (xE - 0.8, zN), (xE - 0.8, zS), (xW + 0.8, zS)])
        loop_wall("lobby-glass", gl, Y, DECK_Y - 1.0, glass or M["facade"], 1.5, 6.0)
    gbox("lobby-roof-slab", xW - 0.6, xE + 0.6, zN, zS, DECK_Y - 1.0, DECK_Y, M["white"])
    if not deck:
        return
    gbox("lobby-deck", xW - 0.4, xE + 0.4, zN + 0.2, zS - 0.2, DECK_Y, DECK_Y + 0.06, M["paving"])
    for x in (xW - 0.45, xE + 0.45):
        loop_wall("deck-rail-%d" % int(x), [[x, zN + 0.3, 0, 0, 0], [x, zS - 0.3, 0, 0, 0]], DECK_Y + 0.06, DECK_Y + 1.15, M["rail-glass"], 1.2, 1.0, closed=False)
        gbox("deck-rail-cap-%d" % int(x), x - 0.06, x + 0.06, zN + 0.3, zS - 0.3, DECK_Y + 1.1, DECK_Y + 1.2, M["white"])
    if not pools:
        return
    for nm, P in (("pool", POOL), ("kidpool", KIDPOOL)):
        poly = round_rect(P["cx"], P["cz"], P["w"], P["d"], 0.5 if nm == "pool" else 0.8, 8)
        prism_l("deck-%s" % nm, poly, DECK_Y + 0.06, DECK_Y + 0.10, M["pool-water"])
        prism_l("deck-%s-coping" % nm, [(p[0], p[1]) for p in offset(resample(poly, 80), 0.45)], DECK_Y + 0.06, DECK_Y + 0.09, M["white"])
    for z in [POOL["cz"] - POOL["d"] / 2 + 1.5 + 2.35 * i for i in range(12)]:
        if z > POOL["cz"] + POOL["d"] / 2 - 1.2:
            break
        x = POOL["cx"] + POOL["w"] / 2 + 2.3
        if abs(z - KIDPOOL["cz"]) < KIDPOOL["d"] / 2 + 0.6:
            continue
        gbox("deck-lounger-%d" % int(z * 10), x - 0.95, x + 0.95, z - 0.39, z + 0.39, DECK_Y + 0.06, DECK_Y + 0.42, M["white"])
    px0, px1, pz0, pz1, top = 21.5, 29.8, -3.5, 12.5, DECK_Y + 3.3
    x = px0
    while x <= px1 + 0.01:
        gbox("deck-pergola-%d" % int(x * 10), x - 0.07, x + 0.07, pz0, pz1, top - 0.3, top, M["white"])
        x += 0.75
    for (x, z) in ((px0, pz0), (px1, pz0), (px0, pz1), (px1, pz1), (px0, (pz0 + pz1) / 2), (px1, (pz0 + pz1) / 2)):
        gbox("deck-post-%d-%d" % (int(x), int(z)), x - 0.13, x + 0.13, z - 0.13, z + 0.13, DECK_Y + 0.06, top - 0.3, M["white"])


def build_retail():
    """the three commercial buildings in the west half (their shapes and places an illustration): recessed shop fronts
    under the first floor's overhang, glass above, a band at every floor, white fins, a roof garden"""
    for R in RETAIL:
        fp = ease_corners(R["poly"], 1.2, 4)
        loop = resample_loop(fp, 64, 3)
        hTop = Y + R["floors"] * RETAIL_FH
        loop_wall("r%s-shops" % R["id"], offset(loop, -1.4), Y, Y + RETAIL_FH, M["facade"], 3.0, RETAIL_FH)
        cap("r%s-shops-ceiling" % R["id"], loop, Y + RETAIL_FH - 0.3, M["white"])
        loop_wall("r%s-glass" % R["id"], loop, Y + RETAIL_FH - 0.3, hTop - 0.2, M["facade"], 1.5, RETAIL_FH)
        for f in range(2, R["floors"] + 1):
            band("r%s-band-%d" % (R["id"], f), loop, Y + (f - 1) * RETAIL_FH, lambda s: 0.55, 0.95, 0.55, 0.2, 0.1)
        per = sum(math.dist(loop[i][:2], loop[(i + 1) % len(loop)][:2]) for i in range(len(loop)))
        nF = round(per / 2.4)
        hf = hTop - Y - RETAIL_FH - 0.6
        for k in range(nF):
            p = loop[int(k / nF * len(loop))]
            ang = math.atan2(-p[4], p[3])
            obox("r%s-fin-%d" % (R["id"], k), (p[0] + p[3] * 0.2, -(p[1] + p[4] * 0.2), (Y + RETAIL_FH + hTop) / 2 + 0.3), (0.6, 0.14, hf),
                 M["white"], yaw=ang)
        band("r%s-roof-band" % R["id"], loop, hTop, lambda s: 0.35, 0.9, 0.6, 0.26, 0.12)
        cap("r%s-roof" % R["id"], loop, hTop + 0.02, M["white"])
        garden = offset(loop, -2.2)
        prism_l("r%s-garden" % R["id"], [(p[0], p[1]) for p in garden], hTop, hTop + 0.3, M["roofgarden"])
        if R["roof"]:
            cxr = (R["poly"][0][0] + R["poly"][1][0]) / 2
            gbox("r%s-roof-box" % R["id"], cxr - 2.6, cxr + 2.6, -8, 8, hTop, hTop + 3.2, M["white"])
        for k in range(6):
            p = garden[int((k + 0.5) / 6 * len(garden))]
            ball("r%s-bush-%d" % (R["id"], k), p[0], -p[1], hTop + 0.8, 0.9, M["tree2"], scale=(1.4, 0.9, 0.7))


# ---------------------------------------------------------------- the sky and the sun
def sky(elev_deg, az_deg, sun_energy=2.6, strength=0.42, color=(1.0, 0.86, 0.72)):
    """a physical sky and the sun at a true azimuth and elevation (Tel Aviv, late September)"""
    world = bpy.data.worlds.new("sky")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    sk = nt.nodes.new("ShaderNodeTexSky")
    try:
        sk.sky_type = "NISHITA"
    except TypeError:
        pass
    el, az = math.radians(elev_deg), math.radians(az_deg)
    for attr, val in (("sun_elevation", el), ("sun_rotation", math.radians(90) - az + math.pi), ("altitude", 100.0),
                      ("air_density", 1.2), ("dust_density", 2.2), ("ozone_density", 1.0), ("sun_intensity", 0.6)):
        if hasattr(sk, attr):
            setattr(sk, attr, val)
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = strength
    wout = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(sk.outputs[0], bg.inputs[0])
    nt.links.new(bg.outputs[0], wout.inputs[0])
    sd = bpy.data.lights.new("sun", "SUN")
    sd.energy = sun_energy
    sd.color = color
    sd.angle = math.radians(0.8)
    sun = bpy.data.objects.new("sun", sd)
    bpy.context.collection.objects.link(sun)
    d = Vector((math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)))
    sun.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    return sun


# ---------------------------------------------------------------- the camera
CAM = None


def camera():
    global CAM
    cd = bpy.data.cameras.new("pano")
    cd.clip_start = 0.05
    cd.clip_end = 60000.0
    cd.type = "PANO"
    try:
        cd.panorama_type = "EQUIRECTANGULAR"
    except (AttributeError, TypeError):
        cd.cycles.panorama_type = "EQUIRECTANGULAR"
    CAM = bpy.data.objects.new("pano", cd)
    bpy.context.collection.objects.link(CAM)
    CAM.parent = SITE
    scene.camera = CAM
    return CAM


def place_camera(x, z, h, dx, dz):
    """the eye at stage-local (x, z), h metres above the street; the panorama's centre along (dx, dz); returns the true
    bearing of the panorama's centre"""
    CAM.location = (x, -z, h)
    look = math.atan2(dx, -dz)                   # clockwise from the grid's north
    CAM.rotation_euler = (math.radians(90), 0, -look)
    return (math.degrees(look) - math.degrees(G)) % 360


def bearing_to(x0, z0, x1, z1):
    """the true bearing from one stage-local point to another"""
    return (math.degrees(math.atan2(x1 - x0, -(z1 - z0))) - math.degrees(G)) % 360


def yaw_of(bearing, centre):
    return (bearing - centre + 540) % 360 - 180


SECTORS = [(235, 315, "לכיוון הים"), (315, 20, "לכיוון נמל תל אביב והירקון"), (20, 70, "לכיוון פארק הירקון"),
           (70, 120, "לכיוון כיכר המדינה"), (120, 180, "לכיוון מגדלי עזריאלי ושרונה"), (180, 235, "לכיוון כיכר רבין ומרכז העיר")]


def sector_words(b):
    """the DUO config's sectors (inc/project-stage.php, 'duo-tel-aviv' => sectors): what lies that way, in the page's words"""
    b %= 360
    for a0, a1, w in SECTORS:
        if (a0 <= b < a1) if a0 < a1 else (b >= a0 or b < a1):
            return w
    return ""


def finish(out, probe_env="DUO_PROBE"):
    """parent everything to the site, then either print what the camera's rays hit (the probe) or render"""
    for ob in bpy.data.objects:
        if ob.parent is None and ob.name not in ("site", "sun"):
            ob.parent = SITE
    eye = os.environ.get("DUO_EYE")                # diagnostics: "x,z,h" moves the eye (stage-local) before the probe
    if eye:
        ex_, ez_, eh_ = (float(v) for v in eye.split(","))
        CAM.location = (ex_, -ez_, eh_)
    probe = os.environ.get(probe_env)
    if probe:
        dg = bpy.context.evaluated_depsgraph_get()
        cw = CAM.matrix_world
        for item in probe.split(","):
            yw, pt = (math.radians(float(v)) for v in item.split(":"))
            d_local = Vector((math.sin(yw) * math.cos(pt), math.sin(pt), -math.cos(yw) * math.cos(pt)))
            d_world = (cw.to_3x3() @ d_local).normalized()
            o = cw.translation.copy()
            for hop in range(6):
                hit, loc, nrm, idx, obj, _ = scene.ray_cast(dg, o, d_world)
                if not hit:
                    print("PROBE", item, "hop", hop, "-> sky")
                    break
                print("PROBE", item, "hop", hop, "->", obj.name, obj.active_material.name if obj.active_material else "-",
                      "%.2f m" % (loc - cw.translation).length)
                o = loc + d_world * 0.002
        sys.exit(0)
    print("objects %d | %d x %d, %d samples, %d threads" % (len(bpy.data.objects), scene.render.resolution_x, scene.render.resolution_y,
                                                            scene.cycles.samples, scene.render.threads))
    out = os.path.abspath(out)                   # (a relative path would land in the drive's root)
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print("wrote", out)
