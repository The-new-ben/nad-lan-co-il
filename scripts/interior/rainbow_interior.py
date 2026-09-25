# -*- coding: utf-8 -*-
"""Rainbow's example apartment from the inside, as a 360 panorama (the site loop, R5; design system ApartmentTour).

An example apartment, labelled so on the page: no floor plans of Rainbow are public, so the room is an illustration of a
living room with an open kitchen, delivered as new apartments are in Israel (floor, walls, kitchen, no furniture). What is
true in it comes from the record and our data:
  - the height: the floor's level from the stage (first residential floor 7.2 m above the street, 3.75 m floor to floor),
    so floor 25 stands at 97.2 m and the eye at 98.8 m, the heightM the page shows;
  - the direction: the tower's curved glass line (the stage's ellipse) facing the chosen true bearing;
  - the view through the glass: the city's buildings standing today (city.json, TLV GIS layer 513) at their recorded
    heights, the coastline 713 m from the lot's centre, the sea, the sun low in the west.
Cycles on the CPU (this machine has no supported GPU): a 4096 x 2048 equirectangular render takes minutes.
  blender -b --factory-startup --python scripts/interior/rainbow_interior.py -- <out.png> [floor] [bearing] [width] [samples] [light] [spot]
light: sunset (a September late afternoon over the sea) or noon (the sun high in the south); spot: living (in the living room,
3.1 m inside the glass) or balcony (standing on the balcony where it is deepest, the railing in front)."""
import json, math, os, sys

import bmesh
import bpy
from mathutils import Vector

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = ARGS[0] if ARGS else os.path.join(os.path.dirname(os.path.abspath(__file__)), "living.png")
FLOOR = int(ARGS[1]) if len(ARGS) > 1 else 25
BEARING = float(ARGS[2]) if len(ARGS) > 2 else 270.0          # true bearing the window wall faces
WIDTH = int(ARGS[3]) if len(ARGS) > 3 else 4096
SAMPLES = int(ARGS[4]) if len(ARGS) > 4 else 128
LIGHT = ARGS[5] if len(ARGS) > 5 else "sunset"
SPOT = ARGS[6] if len(ARGS) > 6 else "living"

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CITY = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "rainbow", "city.json")
QUARTER = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "rainbow", "quarter.json")
G = math.radians(-10)                 # the stage's grid angle (lot 111 turned 10° east of north)
TOWER = dict(cx=13.2, cz=-44.1, rot=math.radians(98), A=16.5, B=10.8, y0=7.2, fh=3.75)
COAST_X = -713.0                      # the waterline, grid x from the lot's centre
FLOOR_Z = TOWER["y0"] + (FLOOR - 1) * TOWER["fh"]
CEIL = 2.95                           # net room height (3.75 floor to floor)


def grid_to_bl(lx, lz):
    """the stage's grid frame (x grid east, z grid south) -> Blender (x east, y north) in true north"""
    X = lx * math.cos(G) + lz * math.sin(G)
    Z = -lx * math.sin(G) + lz * math.cos(G)
    return X, -Z


def ellipse_pt(t, grow=0.0):
    """a point of the tower's glass line (the stage's ellipse), grown outwards by grow metres, in Blender coordinates"""
    A, B, r = TOWER["A"] + grow, TOWER["B"] + grow, TOWER["rot"]
    lx = TOWER["cx"] + A * math.cos(t) * math.cos(r) - B * math.sin(t) * math.sin(r)
    lz = TOWER["cz"] + A * math.cos(t) * math.sin(r) + B * math.sin(t) * math.cos(r)
    return grid_to_bl(lx, lz)


TCX, TCY = grid_to_bl(TOWER["cx"], TOWER["cz"])


def t_for_bearing(bearing):
    """the ellipse parameter whose point lies in the true bearing from the tower's centre"""
    want = math.radians(bearing)
    best, bt = 1e9, 0.0
    for i in range(3600):
        t = i / 3600 * 2 * math.pi
        x, y = ellipse_pt(t)
        b = math.atan2(x - TCX, y - TCY)
        d = abs(math.atan2(math.sin(b - want), math.cos(b - want)))
        if d < best:
            best, bt = d, t
    return bt


# ---------------------------------------------------------------- scene
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
scene.cycles.glossy_bounces = 3
scene.cycles.transmission_bounces = 8
scene.cycles.transparent_max_bounces = 32
scene.cycles.sample_clamp_indirect = 8.0
scene.render.resolution_x = WIDTH
scene.render.resolution_y = WIDTH // 2
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = -1.0 if SPOT == "living" else -1.9   # outside there is no dark room to lift


def mat(name, color, rough=0.5, metal=0.0, alpha=1.0, transmission=0.0, emission=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if transmission:
        b.inputs["Transmission Weight"].default_value = transmission
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
    if emission:
        b.inputs["Emission Color"].default_value = (*emission[0], 1)
        b.inputs["Emission Strength"].default_value = emission[1]
    return m


def glass_mat(tint=(0.94, 0.97, 0.97)):
    """thin clear glass (windows and the balcony railing): a clear sheet with a Fresnel reflection and no refraction, so
    nothing seen edge-on turns black; transparent to shadow rays, so the sky and the sun light the room without noise"""
    m = bpy.data.materials.new("glass")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    lp = nt.nodes.new("ShaderNodeLightPath")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    tr.inputs["Color"].default_value = (*tint, 1)
    gl = nt.nodes.new("ShaderNodeBsdfGlossy")
    gl.inputs["Roughness"].default_value = 0.02
    fr = nt.nodes.new("ShaderNodeFresnel")
    fr.inputs["IOR"].default_value = 1.5
    face = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(fr.outputs[0], face.inputs[0])
    nt.links.new(tr.outputs[0], face.inputs[1])
    nt.links.new(gl.outputs[0], face.inputs[2])
    shadow = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Shadow Ray"], mix.inputs[0])
    nt.links.new(face.outputs[0], mix.inputs[1])
    nt.links.new(shadow.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    return m


M = {
    "floor": None,                                            # large-format porcelain tiles (below)
    "wall": mat("wall", (0.84, 0.82, 0.78), 0.85),
    "base": mat("baseboard", (0.74, 0.71, 0.66), 0.5),
    "door": mat("door", (0.70, 0.64, 0.56), 0.45),
    "void": mat("void", (0.10, 0.10, 0.10), 0.9),
    "ceil": mat("ceiling", (0.93, 0.92, 0.90), 0.9),
    "frame": mat("frame", (0.09, 0.09, 0.09), 0.35, 0.6),  # slim dark aluminium
    "glass": glass_mat(),
    "slab": mat("slab", (0.92, 0.91, 0.88), 0.6),
    "deck": mat("deck", (0.46, 0.43, 0.39), 0.6),
    "counter": mat("counter", (0.93, 0.92, 0.90), 0.18),  # white quartz
    "cabinet": mat("cabinet", (0.80, 0.76, 0.69), 0.5),    # light oak veneer tone
    "cabinet_dark": mat("cabinet_dark", (0.19, 0.19, 0.2), 0.45),
    "city": mat("city", (0.86, 0.82, 0.74), 0.8),
    "quarter": mat("quarter", (0.93, 0.91, 0.86), 0.7, alpha=0.45),
    # the ground far below: a physical sky lights it strongly, so it stays dark in value (building sites, streets, park)
    "ground": mat("ground", (0.13, 0.12, 0.105), 0.95),
    "park": mat("park", (0.06, 0.09, 0.045), 0.95),
    "sand": mat("sand", (0.40, 0.35, 0.27), 0.95),
    "sea": mat("sea", (0.035, 0.15, 0.22), 0.11),
    "light": mat("downlight", (1, 1, 1), 0.5, emission=((1.0, 0.86, 0.70), 18.0)),
}


def tile_floor():
    """120 x 60 cm porcelain tiles, warm light greige, thin grout, a soft sheen"""
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


M["floor"] = tile_floor()
M["sea"].node_tree.nodes["Principled BSDF"].inputs["IOR"].default_value = 1.33   # water: less mirror at the horizon


def hazed(m, haze=(0.66, 0.69, 0.72), dist=3200.0):
    """aerial perspective for the world outside: the base colour drifts to the haze with distance from the camera, so land
    far away pales into the sky as it does over Tel Aviv, instead of staying dark and reading as a sea on the horizon"""
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    base = tuple(b.inputs["Base Color"].default_value)
    cam = nt.nodes.new("ShaderNodeCameraData")
    div = nt.nodes.new("ShaderNodeMath"); div.operation = "DIVIDE"; div.inputs[1].default_value = -dist
    ex = nt.nodes.new("ShaderNodeMath"); ex.operation = "EXPONENT"
    inv = nt.nodes.new("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1.0
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
    mix.inputs[6].default_value = base
    mix.inputs[7].default_value = (*haze, 1)
    nt.links.new(cam.outputs["View Distance"], div.inputs[0])
    nt.links.new(div.outputs[0], ex.inputs[0])
    nt.links.new(ex.outputs[0], inv.inputs[1])
    nt.links.new(inv.outputs[0], mix.inputs[0])
    nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    return m


for _k in ("ground", "park", "sand", "city"):
    hazed(M[_k])


def add_mesh(name, verts, faces, material):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material)
    bpy.context.collection.objects.link(ob)
    return ob


def prism(name, poly, z0, z1, material):
    """a vertical prism from a 2D polygon (counter-clockwise or not), with caps"""
    bm = bmesh.new()
    vs0 = [bm.verts.new((x, y, z0)) for x, y in poly]
    vs1 = [bm.verts.new((x, y, z1)) for x, y in poly]
    n = len(poly)
    try:
        bm.faces.new(vs0[::-1])
        bm.faces.new(vs1)
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
    bpy.context.collection.objects.link(ob)
    return ob


def box(name, cx, cy, cz, sx, sy, sz, material, rot=0.0):
    c, s = math.cos(rot), math.sin(rot)
    pts = [(-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)]
    poly = [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]
    return prism(name, poly, cz - sz / 2, cz + sz / 2, material)


# ---------------------------------------------------------------- the world outside
# ground and sea (the waterline 713 m west of the lot's centre, along the grid), 40 km out: a plane that ends closer lets the
# sky's dark ground show as a false sea on the horizon inland (seen facing north and east)
FAR = 40000
coast = [grid_to_bl(COAST_X, z) for z in (-FAR, FAR)]
sea_poly = [grid_to_bl(COAST_X - FAR, -FAR), grid_to_bl(COAST_X, -FAR), grid_to_bl(COAST_X, FAR), grid_to_bl(COAST_X - FAR, FAR)]
add_mesh("sea", [(x, y, -0.3) for x, y in sea_poly], [(0, 1, 2, 3)], M["sea"])
land = [grid_to_bl(COAST_X, -FAR), grid_to_bl(FAR, -FAR), grid_to_bl(FAR, FAR), grid_to_bl(COAST_X, FAR)]
add_mesh("land", [(x, y, 0) for x, y in land], [(0, 1, 2, 3)], M["ground"])
beach = [grid_to_bl(COAST_X, -FAR), grid_to_bl(COAST_X + 45, -FAR), grid_to_bl(COAST_X + 45, FAR), grid_to_bl(COAST_X, FAR)]
add_mesh("beach", [(x, y, 0.05) for x, y in beach], [(0, 1, 2, 3)], M["sand"])
park = [grid_to_bl(COAST_X + 45, -FAR), grid_to_bl(COAST_X + 120, -FAR), grid_to_bl(COAST_X + 120, FAR), grid_to_bl(COAST_X + 45, FAR)]
add_mesh("coastal-park", [(x, y, 0.08) for x, y in park], [(0, 1, 2, 3)], M["park"])

# the city standing today (TLV GIS layer 513, city.json), one mesh
city = json.load(open(CITY, encoding="utf-8"))
bm = bmesh.new()
for b in city.get("b", []):
    h = float(b[0])
    pts = b[3:]
    poly = [grid_to_bl(pts[i], pts[i + 1]) for i in range(0, len(pts) - 1, 2)]
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
bpy.context.collection.objects.link(ob)

# our projects in the quarter: the stage's schematic masses (their floors), pale and translucent as on the stage
q = json.load(open(QUARTER, encoding="utf-8"))
for p in q.get("projects", []):
    X, Z = float(p["x"]), float(p["z"])            # world metres, x east, z south
    bx, by = X, -Z
    h = max(12.0, float(p.get("floors") or 10) * 3.3 + 4)
    rot = -G                                        # the masses stand on the turned grid
    if (p.get("floors") or 0) >= 20:
        box("q-" + str(p["id"]), bx, by, h / 2, 26, 26, h, M["quarter"], rot)
    else:
        box("q-" + str(p["id"]), bx, by, h / 2, 44, 26, h, M["quarter"], rot)

# the rest of Rainbow: the tower's own floors above and below, as simple slabs with glass (seen from the balcony edge)
for f in range(FLOOR - 3, FLOOR + 4):
    if f == FLOOR:
        continue
    zf = TOWER["y0"] + (f - 1) * TOWER["fh"]
    ring = [ellipse_pt(i / 96 * 2 * math.pi, 1.9) for i in range(96)]
    prism("slab-%d" % f, ring, zf - 0.3, zf, M["slab"])

# ---------------------------------------------------------------- the apartment
t0 = t_for_bearing(BEARING)
# the glass line: an arc of the ellipse about 8.4 m long around the chosen bearing
arc = []
L = 0.0
span = 4.2
step = 0.002
# walk the ellipse both ways from t0 until half the width is reached
def walk(dirn):
    pts, t, acc = [], t0, 0.0
    prev = ellipse_pt(t)
    while acc < span:
        t += dirn * step
        cur = ellipse_pt(t)
        acc += math.dist(prev, cur)
        prev = cur
        pts.append((t, cur))
    return pts
left, right = walk(-1), walk(1)
ts = [t for t, _ in left[::-1]] + [t0] + [t for t, _ in right]
glass_line = [ellipse_pt(t) for t in ts]
# inward direction: towards the tower's centre
mx, my = ellipse_pt(t0)
inx, iny = TCX - mx, TCY - my
il = math.hypot(inx, iny)
inx, iny = inx / il, iny / il
DEPTH = 6.6
back_l = (glass_line[0][0] + inx * DEPTH, glass_line[0][1] + iny * DEPTH)
back_r = (glass_line[-1][0] + inx * DEPTH, glass_line[-1][1] + iny * DEPTH)
# the room's floor and ceiling polygon: the glass arc and the back wall
room = glass_line + [back_r, back_l]
Z0 = FLOOR_Z
prism("room-floor", room, Z0 - 0.35, Z0, M["floor"])
prism("room-ceiling", room, Z0 + CEIL, Z0 + CEIL + 0.4, M["ceil"])


def wall(name, a, b, z0, z1, material, thick=0.2):
    dx, dy = b[0] - a[0], b[1] - a[1]
    Ln = math.hypot(dx, dy)
    if Ln < 1e-4:
        return None
    nx, ny = -dy / Ln * thick / 2, dx / Ln * thick / 2
    poly = [(a[0] - nx, a[1] - ny), (b[0] - nx, b[1] - ny), (b[0] + nx, b[1] + ny), (a[0] + nx, a[1] + ny)]
    return prism(name, poly, z0, z1, material)


wall("wall-left", glass_line[0], back_l, Z0, Z0 + CEIL, M["wall"])
wall("wall-right", glass_line[-1], back_r, Z0, Z0 + CEIL, M["wall"])
wall("wall-back", back_l, back_r, Z0, Z0 + CEIL, M["wall"])
# baseboards, a door to the rest of the apartment on the left wall, an opening to the corridor on the right
for nm, a, b in (("left", glass_line[0], back_l), ("right", glass_line[-1], back_r), ("back", back_l, back_r)):
    wall("base-" + nm, a, b, Z0, Z0 + 0.08, M["base"], 0.24)
dl = (glass_line[0][0] + (back_l[0] - glass_line[0][0]) * 0.72, glass_line[0][1] + (back_l[1] - glass_line[0][1]) * 0.72)
dang = math.atan2(back_l[1] - glass_line[0][1], back_l[0] - glass_line[0][0])
box("door-left", dl[0], dl[1], Z0 + 1.1, 0.95, 0.24, 2.2, M["door"], dang)
dr = (glass_line[-1][0] + (back_r[0] - glass_line[-1][0]) * 0.8, glass_line[-1][1] + (back_r[1] - glass_line[-1][1]) * 0.8)
drang = math.atan2(back_r[1] - glass_line[-1][1], back_r[0] - glass_line[-1][0])
box("corridor-opening", dr[0], dr[1], Z0 + 1.15, 1.1, 0.26, 2.3, M["void"], drang)

# the glazing: floor-to-ceiling panels along the arc, slim mullions every ~1.4 m, a head and a sill profile
seg = []
acc = 0.0
last = glass_line[0]
marks = [0]
for i in range(1, len(glass_line)):
    acc += math.dist(glass_line[i - 1], glass_line[i])
    if acc >= 1.4 * len(marks):
        marks.append(i)
if marks[-1] != len(glass_line) - 1:
    marks.append(len(glass_line) - 1)
marks = sorted(set(marks))
def ribbon(name, pts, z0, z1, material):
    """one continuous single-sided strip (glass): no inner faces for a ray to cross"""
    verts, faces = [], []
    for i, (x, y) in enumerate(pts):
        verts += [(x, y, z0), (x, y, z1)]
        if i:
            a = 2 * (i - 1)
            faces.append((a, a + 2, a + 3, a + 1))
    return add_mesh(name, verts, faces, material)


def thin(P, k):
    return P[::k] + ([P[-1]] if (len(P) - 1) % k else [])


NOGLASS = os.environ.get("RBI_NOGLASS") == "1"   # diagnostics: the view without the glass
if not NOGLASS:
    ribbon("glazing", thin(glass_line, 6), Z0 + 0.06, Z0 + CEIL - 0.08, M["glass"])
for i in marks:
    x, y = glass_line[i]
    box("mullion-%d" % i, x, y, Z0 + CEIL / 2, 0.06, 0.06, CEIL, M["frame"])
gl_thin = thin(glass_line, 6)
for i in range(len(gl_thin) - 1):
    a, b = gl_thin[i], gl_thin[i + 1]
    wall("head-%d" % i, a, b, Z0 + CEIL - 0.08, Z0 + CEIL, M["frame"], 0.08)
    wall("sill-%d" % i, a, b, Z0, Z0 + 0.06, M["frame"], 0.08)

# the balcony: a slab outside the glass whose edge waves like the stage's bands (0.9 to 2.3 m), a glass railing
bal_out = []
for idx, t in enumerate(ts):
    s = idx / (len(ts) - 1)
    depth = 1.6 + 0.7 * math.sin(2 * math.pi * 1.2 * s + 0.6)
    bal_out.append(ellipse_pt(t, depth))
balcony = glass_line + bal_out[::-1]
prism("balcony-slab", balcony, Z0 - 0.3, Z0 - 0.02, M["slab"])
prism("balcony-deck", balcony, Z0 - 0.02, Z0, M["deck"])
if not NOGLASS:
    ribbon("rail-glass", thin(bal_out, 6), Z0, Z0 + 1.08, M["glass"])
bo_thin = thin(bal_out, 6)
for i in range(len(bo_thin) - 1):
    wall("rail-cap-%d" % i, bo_thin[i], bo_thin[i + 1], Z0 + 1.08, Z0 + 1.12, M["frame"], 0.05)
# the balcony above (its soffit frames the view)
prism("balcony-above", balcony, Z0 + TOWER["fh"] - 0.3, Z0 + TOWER["fh"], M["slab"])

# the kitchen: a run along the back wall and an island
bx0, by0 = back_l
bx1, by1 = back_r
ux, uy = (bx1 - bx0), (by1 - by0)
ul = math.hypot(ux, uy)
ux, uy = ux / ul, uy / ul
ang = math.atan2(uy, ux)
kc = (bx0 + ux * ul * 0.55 - inx * 0.33, by0 + uy * ul * 0.55 - iny * 0.33)
box("kitchen-run", kc[0], kc[1], Z0 + 0.45, 4.2, 0.62, 0.9, M["cabinet_dark"], ang)
box("kitchen-top", kc[0] - inx * 0.02, kc[1] - iny * 0.02, Z0 + 0.915, 4.26, 0.66, 0.03, M["counter"], ang)
box("kitchen-tall", kc[0] + ux * 2.55, kc[1] + uy * 2.55, Z0 + 1.2, 0.9, 0.62, 2.4, M["cabinet"], ang)
box("kitchen-upper", kc[0] - ux * 0.3, kc[1] - uy * 0.3, Z0 + 2.15, 3.4, 0.36, 0.72, M["cabinet"], ang)
ic = (kc[0] - inx * 1.55, kc[1] - iny * 1.55)
box("island", ic[0], ic[1], Z0 + 0.45, 2.4, 0.95, 0.9, M["cabinet"], ang)
box("island-top", ic[0], ic[1], Z0 + 0.915, 2.5, 1.0, 0.03, M["counter"], ang)

# recessed lights in the ceiling (warm, subtle), a light for the kitchen
for k in range(3):
    for j in range(2):
        s = (k + 0.5) / 3
        p = (glass_line[0][0] + (glass_line[-1][0] - glass_line[0][0]) * s + inx * (1.9 + j * 2.4),
             glass_line[0][1] + (glass_line[-1][1] - glass_line[0][1]) * s + iny * (1.9 + j * 2.4))
        box("downlight-%d-%d" % (k, j), p[0], p[1], Z0 + CEIL - 0.005, 0.09, 0.09, 0.01, M["light"])

# ---------------------------------------------------------------- sky and sun: late afternoon light from the west
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
if LIGHT == "noon":
    SUN_ELEV = math.radians(57)       # Tel Aviv at the end of September, around 12:45
    SUN_AZ = math.radians(185)
else:
    SUN_ELEV = math.radians(11)
    SUN_AZ = math.radians(262)        # just south of west, a September late afternoon over the sea
for attr, val in (("sun_elevation", SUN_ELEV), ("sun_rotation", math.radians(90) - SUN_AZ + math.pi), ("altitude", 100.0),
                  ("air_density", 1.2), ("dust_density", 2.2), ("ozone_density", 1.0), ("sun_intensity", 0.6)):
    if hasattr(sky, attr):
        setattr(sky, attr, val)
bg = nt.nodes.new("ShaderNodeBackground")
bg.inputs["Strength"].default_value = 0.42
out = nt.nodes.new("ShaderNodeOutputWorld")
nt.links.new(sky.outputs[0], bg.inputs[0])
nt.links.new(bg.outputs[0], out.inputs[0])

sun_data = bpy.data.lights.new("sun", "SUN")
sun_data.energy = 2.6 if LIGHT == "sunset" else 3.4
sun_data.color = (1.0, 0.86, 0.72) if LIGHT == "sunset" else (1.0, 0.97, 0.93)
sun_data.angle = math.radians(0.8)
sun = bpy.data.objects.new("sun", sun_data)
bpy.context.collection.objects.link(sun)
d = Vector((math.sin(SUN_AZ) * math.cos(SUN_ELEV), math.cos(SUN_AZ) * math.cos(SUN_ELEV), math.sin(SUN_ELEV)))
sun.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()

# the photographer's window pull: a soft light just inside the glass, invisible to the camera, lifts the room so the view
# outside keeps its colour instead of burning out (the sky alone lights the outside far more than the inside)
fill = bpy.data.lights.new("window-fill", "AREA")
fill.shape = "RECTANGLE"
fill.size, fill.size_y = 8.0, 2.6
fill.energy = 380.0
fill.color = (1.0, 0.95, 0.88)
fill_ob = bpy.data.objects.new("window-fill", fill)
bpy.context.collection.objects.link(fill_ob)
fill_ob.location = (mx + inx * 0.35, my + iny * 0.35, Z0 + CEIL / 2)
fill_ob.rotation_euler = Vector((inx, iny, 0)).to_track_quat("-Z", "Z").to_euler()
fill_ob.visible_camera = False
fill_ob.visible_glossy = False

# ---------------------------------------------------------------- the 360 camera: standing in the living room
cam_data = bpy.data.cameras.new("pano")
# a new camera sees only 1 km: the land and the sea beyond it were cut, and the sky's dark lower half showed through as a
# false sea on every horizon (seen 25.9.2026). The view reaches 60 km.
cam_data.clip_start = 0.05
cam_data.clip_end = 60000.0
cam_data.type = "PANO"
try:
    cam_data.panorama_type = "EQUIRECTANGULAR"
except (AttributeError, TypeError):
    cam_data.cycles.panorama_type = "EQUIRECTANGULAR"
cam = bpy.data.objects.new("pano", cam_data)
bpy.context.collection.objects.link(cam)
if SPOT == "balcony":
    # where the balcony is deepest (its wave peaks near one end): 1.1 m out from the glass
    best = max(range(len(ts)), key=lambda i: math.dist(glass_line[i], bal_out[i]))
    gx, gy = glass_line[best]
    ox, oy = bal_out[best]
    dl = math.dist((gx, gy), (ox, oy))
    eye = (gx + (ox - gx) / dl * 1.1, gy + (oy - gy) / dl * 1.1, Z0 + 1.6)
else:
    eye = (mx + inx * 3.1, my + iny * 3.1, Z0 + 1.6)
cam.location = eye
# the panorama's centre looks out through the glass (towards the bearing)
look = math.atan2(-inx, -iny)
cam.rotation_euler = (math.radians(90), 0, -look)
scene.camera = cam

print("floor", FLOOR, "floor level %.1f m, eye %.1f m" % (Z0, Z0 + 1.6), "| bearing", BEARING, "| glass centre", (round(mx, 1), round(my, 1)))
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("wrote", OUT)
