# -*- coding: utf-8 -*-
"""Build the 3D model of the Kochav HaTzafon mini penthouse from trace/plan.json and render one view (Blender 5.2, Cycles).
Illustration from the architect's plan: no dimensions anywhere, neutral studio / soft sky, no city, no invented rooms.
    blender -b --python plan3d.py -- --view dollhouse|topdown|terrace [--samples 128] [--scale 100] [--out path.png] [--save-blend]
Materials follow the broker's real photos (tour/real): large light stone tiles in the living space, light oak in bedrooms,
grey tiles in wet rooms, walnut slat wall with a stone panel, matte black kitchen, cream sofa, rust tub chairs, grey wood-look
deck, frameless glass rail, light aluminium pergolas."""
import bpy, bmesh, json, math, os, sys, time
from mathutils import Vector, Matrix
from mathutils.geometry import tessellate_polygon

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PLAN = json.load(open(os.path.join(ROOT, "trace", "plan.json"), encoding="utf-8"))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(name, default=None, cast=str):
    return cast(argv[argv.index(name) + 1]) if name in argv else default
VIEW = arg("--view", "dollhouse")
DOLL_RX = arg("--rx", 52.0, float)
DOLL_RZ = arg("--rz", 10.0, float)
SUN_RZ = arg("--sunrz", None, float)
EXPO = arg("--expo", None, float)
CAM = [float(v) for v in arg("--cam", "3105,545,1.6").split(",")]
TGT = [float(v) for v in arg("--tgt", "2930,1170,1.25").split(",")]
LENS = arg("--lens", 20.0, float)
SAMPLES = arg("--samples", 128, int)
SCALE = arg("--scale", 100, int)
OUT = arg("--out", os.path.join(ROOT, "renders", {"dollhouse": "dollhouse-iso.png", "topdown": "topdown.png", "terrace": "terrace.png"}[VIEW]))
OUT = os.path.abspath(OUT)
FULL = VIEW == "terrace"           # full-height walls + roof for the terrace view; cut-away at 1.2 m otherwise
CUT = 1.2
WALL_H = 2.85
PXM = PLAN["meta"]["internal_scale"]["px_per_m"]
bx0, by0, bx1, by1 = PLAN["meta"]["bbox"]
CX, CY = (bx0 + bx1) / 2.0, (by0 + by1) / 2.0
TOP = WALL_H if FULL else CUT


def W(p):
    """raster px -> Blender metres (x right, y up)"""
    return ((p[0] - CX) / PXM, (CY - p[1]) / PXM)


# ------------------------------------------------------------------ scene reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
COL = bpy.data.collections.new("apt43"); scene.collection.children.link(COL)


def srgb(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(((v / 12.92) if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c) + (1.0,)


# ------------------------------------------------------------------ materials
MATS = {}
def principled(name, color, rough=0.5, metal=0.0, spec=0.5, trans=0.0, ior=1.45, coat=0.0, sheen=0.0, emit=None, emit_s=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes.get("Principled BSDF")
    def put(k, v):
        if k in b.inputs:
            b.inputs[k].default_value = v
    put("Base Color", srgb(color) if isinstance(color, str) else color)
    put("Roughness", rough); put("Metallic", metal)
    put("Specular IOR Level", spec); put("IOR", ior)
    put("Transmission Weight", trans); put("Coat Weight", coat); put("Sheen Weight", sheen)
    if emit:
        put("Emission Color", srgb(emit)); put("Emission Strength", emit_s)
    MATS[name] = m
    return m


def tiled(name, c1, c2, mortar, bw, rh, offset, mortar_size, rough, rot=0.0, noise=0.12, grain=False, bump=0.15):
    """procedural tiles / planks on the UV (= world metres) of the floor"""
    m = principled(name, c1, rough=rough)
    nt = m.node_tree; N = nt.nodes; L = nt.links; b = N.get("Principled BSDF")
    tc = N.new("ShaderNodeTexCoord"); mp = N.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value = (0, 0, math.radians(rot))
    L.new(tc.outputs["UV"], mp.inputs["Vector"])
    br = N.new("ShaderNodeTexBrick")
    br.offset = offset; br.offset_frequency = 2; br.squash = 1.0; br.squash_frequency = 2
    br.inputs["Color1"].default_value = srgb(c1); br.inputs["Color2"].default_value = srgb(c2)
    br.inputs["Mortar"].default_value = srgb(mortar)
    br.inputs["Scale"].default_value = 1.0; br.inputs["Mortar Size"].default_value = mortar_size
    br.inputs["Mortar Smooth"].default_value = 0.1; br.inputs["Bias"].default_value = 0.0
    br.inputs["Brick Width"].default_value = bw; br.inputs["Row Height"].default_value = rh
    L.new(mp.outputs["Vector"], br.inputs["Vector"])
    nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.0 if not grain else 1.2
    nz.inputs["Detail"].default_value = 6.0
    if grain:
        wv = N.new("ShaderNodeTexWave"); wv.bands_direction = "X"; wv.inputs["Scale"].default_value = 18.0
        wv.inputs["Distortion"].default_value = 6.0; wv.inputs["Detail"].default_value = 4.0
        L.new(mp.outputs["Vector"], wv.inputs["Vector"]); src = wv.outputs["Fac"]
    else:
        L.new(mp.outputs["Vector"], nz.inputs["Vector"]); src = nz.outputs["Fac"]
    mix = N.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "OVERLAY"
    mix.inputs["Factor"].default_value = noise
    L.new(br.outputs["Color"], mix.inputs[6]); L.new(src, mix.inputs[7])
    L.new(mix.outputs[2], b.inputs["Base Color"])
    bp = N.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump; bp.inputs["Distance"].default_value = 0.002
    L.new(br.outputs["Fac"], bp.inputs["Height"]); L.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


# floors (from the real photos)
tiled("stone", "#bdb5aa", "#b6aea2", "#958d82", 1.2, 1.2, 0.0, 0.0028, 0.32, rot=45, noise=0.18)
tiled("oak", "#c2a582", "#b59671", "#9a7e5f", 1.4, 0.19, 0.5, 0.0015, 0.45, rot=0, noise=0.35, grain=True, bump=0.08)
tiled("tile", "#a7a29b", "#a09b94", "#8a857f", 0.6, 0.6, 0.0, 0.003, 0.4, noise=0.08)
tiled("deck", "#b39c7f", "#a68f71", "#6e604f", 1.8, 0.16, 0.5, 0.005, 0.55, rot=45, noise=0.25, grain=False, bump=0.25)
tiled("facade", "#d8d6cf", "#d1cfc8", "#a9a7a0", 0.6, 0.6, 0.0, 0.004, 0.5, noise=0.3, bump=0.35)
principled("plaster", "#eeede9", rough=0.85)
principled("walltop", "#1b2730", rough=0.7)
principled("slab", "#e7e9ea", rough=0.8)
principled("slabedge", "#c9cfd3", rough=0.7)
principled("glass", (0.92, 0.96, 0.97, 1), rough=0.0, trans=1.0, ior=1.5, spec=0.5)
principled("frame", "#1c1f22", rough=0.35, metal=0.6)
principled("alu", "#d9dcdc", rough=0.35, metal=0.7)
principled("parapet", "#c9cac6", rough=0.6)
principled("black", "#1e1f21", rough=0.55)
principled("blacktop", "#232426", rough=0.25, coat=0.3)
principled("cream", "#e2dbd0", rough=0.95, sheen=0.6)
principled("cream2", "#d8d0c3", rough=0.95, sheen=0.6)
principled("rust", "#a5532f", rough=0.9, sheen=0.5)
principled("darkstone", "#2f3236", rough=0.3)
principled("lightstone", "#dcdad5", rough=0.25)
principled("rug", "#d9d6cf", rough=1.0, sheen=0.4)
principled("chairfab", "#bdb8b0", rough=0.9, sheen=0.3)
principled("walnut", "#5a3d2a", rough=0.5)
principled("linen", "#f4f3f0", rough=0.95, sheen=0.4)
principled("throw", "#c8ccc9", rough=0.95, sheen=0.5)
principled("headboard", "#b9b6b0", rough=0.9, sheen=0.4)
principled("white", "#f4f4f2", rough=0.6)
principled("porcelain", "#f7f7f5", rough=0.15, coat=0.4)
principled("oakvanity", "#9c7a57", rough=0.5)
principled("steel", "#b8bcbf", rough=0.25, metal=1.0)
principled("hob", "#151618", rough=0.15, coat=0.6)
principled("ground", "#dfe4e7", rough=1.0)
principled("led", "#ffffff", emit="#fff3e2", emit_s=6.0)


# ------------------------------------------------------------------ geometry helpers
def to_obj(name, bm, mats):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); COL.objects.link(ob)
    for m in mats:
        me.materials.append(MATS[m])
    return ob


def extrude(name, polys, z0, z1, mat_side, mat_top=None, mat_bottom=None, uv_world=True, side_classifier=None):
    """polys: [{"exterior": [[x,y]...], "holes": [...]}] in raster px; extruded from z0 to z1 with UVs in metres."""
    mats = [mat_side, mat_top or mat_side, mat_bottom or mat_side]
    extra = []
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    for p in polys:
        rings = [p["exterior"]] + p.get("holes", [])
        rings = [[W(q) for q in r] for r in rings if len(r) >= 3]
        if not rings:
            continue
        flat = [Vector((x, y, 0)) for r in rings for x, y in r]
        tris = tessellate_polygon([[Vector((x, y, 0)) for x, y in r] for r in rings])
        vb = [bm.verts.new((v.x, v.y, z0)) for v in flat]
        vt = [bm.verts.new((v.x, v.y, z1)) for v in flat]
        for t in tris:
            try:
                f = bm.faces.new([vt[t[0]], vt[t[1]], vt[t[2]]]); f.material_index = 1
                if f.normal.z < 0: f.normal_flip()
                for l in f.loops: l[uv].uv = (l.vert.co.x, l.vert.co.y)
                g = bm.faces.new([vb[t[0]], vb[t[1]], vb[t[2]]]); g.material_index = 2
                if g.normal.z > 0: g.normal_flip()
                for l in g.loops: l[uv].uv = (l.vert.co.x, l.vert.co.y)
            except ValueError:
                pass
        k = 0
        for r in rings:
            n = len(r); acc = 0.0
            # orientation: outward normals need ring winding; fix after with normal test against centroid of top tris
            for i in range(n):
                a, b = k + i, k + (i + 1) % n
                L = (flat[b] - flat[a]).length
                try:
                    f = bm.faces.new([vb[a], vb[b], vt[b], vt[a]])
                except ValueError:
                    acc += L; continue
                f.material_index = 0
                us = [acc, acc + L, acc + L, acc]; vs = [z0, z0, z1, z1]
                for l, uu, vv in zip(f.loops, us, vs):
                    l[uv].uv = (uu, vv)
                acc += L
            k += n
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if side_classifier:
        for f in bm.faces:
            if abs(f.normal.z) < 0.2:
                c = f.calc_center_median()
                q = (c.x + f.normal.x * 0.25, c.y + f.normal.y * 0.25)
                if side_classifier(q):
                    f.material_index = 3
        mats.append(side_classifier.mat)
    return to_obj(name, bm, mats)


def box(name, c, size, ang, mat, bevel=0.0):
    """c=(x,y,z) centre in metres (Blender), size=(sx,sy,sz), ang=rotation about Z (rad)"""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    bmesh.ops.rotate(bm, cent=Vector((0, 0, 0)), matrix=Matrix.Rotation(ang, 3, "Z"), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(c), verts=bm.verts)
    ob = to_obj(name, bm, [mat])
    if bevel > 0:
        md = ob.modifiers.new("bevel", "BEVEL"); md.width = bevel; md.segments = 3; md.limit_method = "ANGLE"
    return ob


def cyl(name, c, r, h, mat, seg=40, bevel=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=h)
    bmesh.ops.translate(bm, vec=Vector(c), verts=bm.verts)
    ob = to_obj(name, bm, [mat])
    for p in ob.data.polygons: p.use_smooth = True
    if bevel > 0:
        md = ob.modifiers.new("bevel", "BEVEL"); md.width = bevel; md.segments = 3; md.limit_method = "ANGLE"
    return ob


def arc(name, c, r0, r1, a0, a1, z0, z1, mat, seg=28):
    rings = []
    outer = [(c[0] + r1 * math.cos(a0 + (a1 - a0) * k / seg), c[1] + r1 * math.sin(a0 + (a1 - a0) * k / seg)) for k in range(seg + 1)]
    inner = [(c[0] + r0 * math.cos(a1 - (a1 - a0) * k / seg), c[1] + r0 * math.sin(a1 - (a1 - a0) * k / seg)) for k in range(seg + 1)]
    px = [((x * PXM + CX), (CY - y * PXM)) for x, y in outer + inner]
    ob = extrude(name, [{"exterior": px}], z0, z1, mat, mat, mat)
    for p in ob.data.polygons: p.use_smooth = True
    md = ob.modifiers.new("bevel", "BEVEL"); md.width = 0.03; md.segments = 3; md.limit_method = "ANGLE"
    return ob


def blade(name, c, length, width, thick, ang, tilt, mat):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector((length, width, thick)), verts=bm.verts)
    bmesh.ops.rotate(bm, cent=Vector((0, 0, 0)), matrix=Matrix.Rotation(tilt, 3, "X"), verts=bm.verts)
    bmesh.ops.rotate(bm, cent=Vector((0, 0, 0)), matrix=Matrix.Rotation(ang, 3, "Z"), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(c), verts=bm.verts)
    return to_obj(name, bm, [mat])


def clipz(z0, z1):
    if not FULL:
        z1 = min(z1, CUT)
    return z0, z1


class Frame:
    """local frame of a plan item: centre C, width axis R (u), facing F (v, front = +v); metres"""
    def __init__(self, item):
        P = [Vector(W(q)) for q in item["poly"]]
        self.C = sum(P, Vector((0, 0))) / 4
        e1, e2 = P[1] - P[0], P[2] - P[1]
        fc = item.get("facing")
        if fc:
            F = Vector((fc[0], -fc[1])).normalized()
            if abs(e1.normalized().dot(F)) > abs(e2.normalized().dot(F)):
                self.h, self.w = e1.length, e2.length
            else:
                self.h, self.w = e2.length, e1.length
        else:
            if e1.length >= e2.length:
                R = e1.normalized(); self.w, self.h = e1.length, e2.length
            else:
                R = e2.normalized(); self.w, self.h = e2.length, e1.length
            F = Vector((-R.y, R.x))
        self.F = F; self.R = Vector((F.y, -F.x))
        self.ang = math.atan2(self.R.y, self.R.x)

    def p(self, u, v, z):
        q = self.C + self.R * u + self.F * v
        return (q.x, q.y, z)

    def box(self, name, u, v, z0, z1, su, sv, mat, bevel=0.0):
        z0, z1 = clipz(z0, z1)
        if z1 <= z0 + 1e-4:
            return None
        return box(name, self.p(u, v, (z0 + z1) / 2), (su, sv, z1 - z0), self.ang, mat, bevel)


# ------------------------------------------------------------------ point in polygon (raster px) for facade detection
def pip(pt, ring):
    x, y = pt; inside = False; n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]; x2, y2 = ring[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1:
            inside = not inside
    return inside


INDOOR = [r for r in PLAN["rooms"] if r["id"] not in ("terrace", "balcony", "service", "ledge")]
def is_outside(q):
    x = q[0] * PXM + CX; y = CY - q[1] * PXM
    for r in INDOOR:
        for p in r["poly"]:
            if pip((x, y), p["exterior"]) and not any(pip((x, y), h) for h in p.get("holes", [])):
                return False
    return True
is_outside.mat = "facade"


# ------------------------------------------------------------------ build: slab, floors, walls
SLAB = 0.30
extrude("slab", PLAN["footprint"], -SLAB, -0.001, "slabedge", "slab", "slab")
for r in PLAN["rooms"]:
    extrude("floor-" + r["id"], r["poly"], -0.001, 0.012, r["floor"], r["floor"], r["floor"])
# openings: floor under door gaps
for o in PLAN["openings"]:
    rid = o["rooms"][1] if o["rooms"][1] not in ("outside",) else o["rooms"][0]
    fl = next((r["floor"] for r in PLAN["rooms"] if r["id"] == rid), "stone")
    extrude("sill-floor-" + o["id"], o["wall_poly"], -0.001, 0.011, fl, fl, fl)

walls = extrude("walls", PLAN["walls_union_cut"], 0.0, TOP, "plaster", "walltop" if not FULL else "plaster", "plaster",
                side_classifier=is_outside if FULL else None)
md = walls.modifiers.new("bevel", "BEVEL"); md.width = 0.006; md.segments = 2; md.limit_method = "ANGLE"

# window sills, lintels, glass and frames
def seg_frame(o):
    a = Vector(W(o["a"])); b = Vector(W(o["b"])); d = b - a; L = d.length; R = d.normalized()
    return a, b, L, R, math.atan2(R.y, R.x)

for o in PLAN["openings"]:
    a, b, L, R, ang = seg_frame(o)
    mid = (a + b) / 2
    th = 0.0
    if o["wall_poly"]:
        # wall thickness = polygon area / opening length
        from_px = [Vector(W(q)) for q in o["wall_poly"][0]["exterior"]]
        area = 0.0
        for i in range(len(from_px)):
            p1, p2 = from_px[i], from_px[(i + 1) % len(from_px)]
            area += p1.x * p2.y - p2.x * p1.y
        th = abs(area) / 2 / max(L, 1e-3)
    th = max(0.08, min(th, 0.5))
    if o["type"] == "window":
        sill = o.get("sill") or 0.9
        z0, z1 = clipz(0, sill)
        extrude("sill-" + o["id"], o["wall_poly"], 0.0, min(sill, TOP), "plaster", "walltop" if (not FULL and sill >= CUT) else "white", "plaster",
                side_classifier=is_outside if FULL else None)
        top = 2.35 if FULL else CUT
        if top > sill:
            box("glass-" + o["id"], (mid.x, mid.y, (sill + top) / 2), (L, 0.016, top - sill), ang, "glass")
            for t in (-L / 2 + 0.025, L / 2 - 0.025):
                q = mid + R * t
                box("fr-" + o["id"] + str(t), (q.x, q.y, (sill + top) / 2), (0.05, th * 0.6, top - sill), ang, "frame")
            q = mid; box("frs-" + o["id"], (q.x, q.y, sill + 0.02), (L, th * 0.6, 0.04), ang, "frame")
            if FULL:
                box("frt-" + o["id"], (q.x, q.y, top - 0.02), (L, th * 0.6, 0.04), ang, "frame")
    elif o["type"] == "slider":
        top = 2.6 if FULL else CUT
        half = L * 0.52
        for k, (t, off) in enumerate(((-L / 2 + half / 2, -0.03), (L / 2 - half / 2, 0.03))):
            n = Vector((-R.y, R.x)); q = mid + R * t + n * off
            box("glass-%s-%d" % (o["id"], k), (q.x, q.y, (0.02 + top) / 2), (half, 0.014, top - 0.02), ang, "glass")
            for tt in (-half / 2 + 0.02, half / 2 - 0.02):
                qq = q + R * tt
                box("fr-%s-%d-%.2f" % (o["id"], k, tt), (qq.x, qq.y, (0.02 + top) / 2), (0.04, 0.05, top - 0.02), ang, "frame")
        box("track-" + o["id"], (mid.x, mid.y, 0.016), (L, th * 0.7, 0.02), ang, "frame")
        if FULL:
            box("frt-" + o["id"], (mid.x, mid.y, top - 0.02), (L, th * 0.7, 0.04), ang, "frame")
    elif o["type"] in ("door", "entrance"):
        # door leaf drawn open, as the architect's swing shows it
        hx, hy = W(o["hinge"]); sx, sy = W(o["swing"])
        dv = Vector((sx - hx, sy - hy)); Ld = dv.length; dn = dv.normalized()
        z1 = min(2.1, TOP)
        c = Vector((hx, hy)) + dv / 2
        box("leaf-" + o["id"], (c.x, c.y, z1 / 2 + 0.01), (Ld, 0.04, z1 - 0.02), math.atan2(dn.y, dn.x), "frame" if o["type"] == "entrance" else "white", 0.004)
    if FULL:
        head = 2.6 if o["type"] in ("slider",) else (2.35 if o["type"] == "window" else 2.15)
        extrude("lintel-" + o["id"], o["wall_poly"], head, WALL_H, "plaster", "plaster", "plaster", side_classifier=is_outside)

# parapets: stone curb + frameless glass + slim dark top rail
for q in PLAN["parapets"]:
    P = [Vector(W(p)) for p in q["poly"]]
    extrude("curb-" + q["id"], [{"exterior": q["poly"]}], 0.0, 0.14, "parapet", "parapet", "parapet")
    if len(P) == 4:
        e = [(P[(i + 1) % 4] - P[i]) for i in range(4)]
        i = 0 if e[0].length >= e[1].length else 1
        a = (P[i] + P[(i + 3) % 4]) / 2; b = (P[i + 1] + P[(i + 2) % 4]) / 2
        d = b - a; L = d.length; ang = math.atan2(d.y, d.x); m = (a + b) / 2
        box("rail-" + q["id"], (m.x, m.y, 0.14 + 0.48), (L, 0.016, 0.96), ang, "glass")
        box("cap-" + q["id"], (m.x, m.y, 1.12), (L, 0.05, 0.035), ang, "frame")

# pergolas: perimeter beam, louvres parallel to the living-room wall, posts only where drawn
PH = 2.9
for pg in PLAN["pergolas"]:
    P = [Vector(W(p)) for p in pg["poly"]]
    ax, bx_, dx = P[0], P[1], P[3]
    u = bx_ - ax; v = dx - ax; Lu, Lv = u.length, v.length; un, vn = u.normalized(), v.normalized(); ang = math.atan2(un.y, un.x)
    for t0, t1 in ((0, 0), (1, 1)):
        q = ax + v * t0 + u * 0.5
        box("beam-%s-%d" % (pg["id"], t0), (q.x, q.y, PH), (Lu, 0.12, 0.22), ang, "alu")
    for t in (0, 1):
        q = ax + u * t + v * 0.5
        box("beamv-%s-%d" % (pg["id"], t), (q.x, q.y, PH), (0.12, Lv, 0.22), ang, "alu")
    n = int(Lv / 0.2)
    for k in range(1, n):
        q = ax + vn * (k * Lv / n) + u * 0.5
        blade("louvre-%s-%d" % (pg["id"], k), (q.x, q.y, PH + 0.02), Lu - 0.12, 0.16, 0.022, ang, math.radians(58), "alu")
for k, q in enumerate(PLAN["pergola_posts"]):
    P = [Vector(W(p)) for p in q]; c = sum(P, Vector((0, 0))) / 4
    box("post-%d" % k, (c.x, c.y, PH / 2), (0.14, 0.14, PH), math.radians(45), "alu")
if FULL:
    # roof slab over the indoor rooms (the real terrace has a deep white canopy with a warm LED line)
    extrude("roof", PLAN["indoor_footprint"], WALL_H, WALL_H + 0.32, "white", "slab", "white")

# ------------------------------------------------------------------ furniture (as drawn) + fixtures + beds (staging)
for it in PLAN["furniture"]:
    t = it["type"]; f = Frame(it); w, h = f.w, f.h; nm = it["id"]
    if t == "sofa":
        f.box(nm + "-base", 0, 0, 0.06, 0.40, w, h, "cream", 0.03)
        f.box(nm + "-back", 0, -h / 2 + 0.11, 0.40, 0.80, w - 0.04, 0.22, "cream", 0.05)
        for s in (-1, 1):
            f.box(nm + "-arm%d" % s, s * (w / 2 - 0.09), 0.0, 0.40, 0.62, 0.18, h, "cream", 0.05)
        n = 3 if w > 2.2 else 2; cw = (w - 0.36) / n
        for k in range(n):
            f.box(nm + "-cush%d" % k, -w / 2 + 0.18 + cw * (k + 0.5), 0.08, 0.40, 0.50, cw - 0.02, h - 0.3, "cream2", 0.04)
        f.box(nm + "-plinth", 0, 0, 0.0, 0.06, w - 0.1, h - 0.1, "black")
    elif t == "armchair":
        r = min(w, h) / 2 * 0.92
        c = f.p(0, 0, 0)
        cyl(nm + "-seat", (c[0], c[1], 0.2), r, 0.40, "rust", seg=48, bevel=0.06)
        cyl(nm + "-cush", (c[0], c[1], 0.43), r * 0.86, 0.07, "rust", seg=48, bevel=0.03)
        back_angle = math.atan2(-f.F.y, -f.F.x)
        arc("%s-back" % nm, (c[0], c[1]), r * 0.72, r, back_angle - math.radians(115), back_angle + math.radians(115), 0.38, min(0.76, TOP), "rust")
    elif t == "coffee_table":
        f.box(nm, 0, 0, 0.0, 0.34, w * 0.92, h * 0.92, "darkstone", 0.01)
    elif t == "rug":
        f.box(nm, 0, 0, 0.012, 0.022, w, h, "rug", 0.004)
    elif t == "dining_table":
        f.box(nm + "-top", 0, 0, 0.72, 0.76, w, h, "lightstone", 0.006)
        for su in (-1, 1):
            f.box(nm + "-leg%d" % su, su * (w / 2 - 0.25), 0, 0.0, 0.72, 0.06, h * 0.6, "black")
    elif t == "chair":
        f.box(nm + "-seat", 0, 0.02, 0.42, 0.47, w * 0.9, h * 0.8, "chairfab", 0.02)
        f.box(nm + "-back", 0, -h / 2 + 0.05, 0.47, 0.85, w * 0.85, 0.05, "chairfab", 0.02)
        for su in (-1, 1):
            for sv in (-1, 1):
                f.box(nm + "-l%d%d" % (su, sv), su * (w * 0.36), sv * (h * 0.3), 0.0, 0.42, 0.025, 0.025, "black")
    elif t == "island":
        f.box(nm + "-body", 0, 0, 0.0, 0.88, w - 0.04, h - 0.04, "black", 0.004)
        f.box(nm + "-top", 0, 0, 0.88, 0.92, w, h, "blacktop", 0.004)
    elif t == "hob":
        f.box(nm, 0, 0, 0.92, 0.926, w, h, "hob")
    elif t == "counter":
        f.box(nm + "-body", 0, 0, 0.0, 0.88, w, h, "black", 0.003)
        f.box(nm + "-top", 0, 0, 0.88, 0.92, w, h, "blacktop", 0.003)
    elif t == "sink":
        f.box(nm, 0, 0, 0.90, 0.925, w, h, "steel", 0.01)
    elif t == "tall_units":
        f.box(nm, 0, 0, 0.0, 2.3, w, h, "black", 0.003)
    elif t == "feature_wall":
        # walnut slats with a light stone panel in the middle (DX9wx4ziADM_02)
        n = int(w / 0.055)
        for k in range(n):
            u = -w / 2 + (k + 0.5) * w / n
            if abs(u) < w * 0.14:
                continue
            f.box(nm + "-s%d" % k, u, 0, 0.0, 2.6, 0.032, 0.03, "walnut")
        f.box(nm + "-stone", 0, 0.005, 0.0, 2.6, w * 0.28, 0.03, "lightstone", 0.004)
    elif t == "bed":
        f.box(nm + "-base", 0, 0.03, 0.0, 0.32, w, h - 0.06, "headboard", 0.02)
        f.box(nm + "-mattress", 0, 0.04, 0.32, 0.52, w - 0.04, h - 0.1, "linen", 0.05)
        f.box(nm + "-throw", 0, h / 2 - 0.36, 0.52, 0.55, w + 0.02, 0.6, "throw", 0.02)
        f.box(nm + "-head", 0, -h / 2 + 0.04, 0.0, 1.05, w + 0.04, 0.08, "headboard", 0.03)
        n = 2 if w > 1.2 else 1; pw = (w - 0.2) / n
        for k in range(n):
            f.box(nm + "-pil%d" % k, -w / 2 + 0.1 + pw * (k + 0.5), -h / 2 + 0.28, 0.52, 0.66, pw - 0.06, 0.32, "linen", 0.06)
    elif t == "wardrobe":
        f.box(nm, 0, 0, 0.0, 2.4, w, h, "white", 0.004)
    elif t == "toilet":
        f.box(nm + "-tank", 0, -h / 2 + 0.06, 0.0, 0.8, w * 0.9, 0.12, "porcelain", 0.02)
        c = f.p(0, 0.08, 0); cyl(nm + "-bowl", (c[0], c[1], 0.2), min(w, h) * 0.32, 0.4, "porcelain", bevel=0.03)
    elif t == "basin_round":
        c = f.p(0, 0, 0); cyl(nm, (c[0], c[1], 0.82), min(w, h) * 0.4, 0.12, "porcelain", bevel=0.02)
    elif t == "vanity":
        f.box(nm + "-body", 0, 0, 0.35, 0.82, w, h, "oakvanity", 0.006)
        c = f.p(0, 0, 0); cyl(nm + "-basin", (c[0], c[1], 0.88), min(0.22, h * 0.45), 0.13, "porcelain", bevel=0.02)
    elif t == "bathtub":
        f.box(nm + "-outer", 0, 0, 0.0, 0.55, w, h, "porcelain", 0.03)
        f.box(nm + "-water", 0, 0, 0.54, 0.555, w - 0.12, h - 0.12, "white")
        f.box(nm + "-screen", -w / 2 + 0.45, h / 2 - 0.02, 0.55, 1.9, 0.9, 0.012, "glass")
    elif t == "shower":
        f.box(nm + "-tray", 0, 0, 0.0, 0.03, w, h, "white", 0.01)
        f.box(nm + "-glass", 0, h / 2 - 0.02, 0.03, 2.0, w * 0.7, 0.012, "glass")
    elif t == "washer":
        f.box(nm, 0, 0, 0.0, 0.85, w * 0.95, h * 0.95, "white", 0.02)
    elif t == "water_heater":
        c = f.p(0, 0, 0); cyl(nm, (c[0], c[1], min(1.5, TOP) / 2), min(w, h) * 0.45, min(1.5, TOP), "white", bevel=0.03)
    elif t == "ac_unit":
        f.box(nm, 0, 0, 0.0, 0.62, w, h * 0.6, "alu", 0.01)

# ------------------------------------------------------------------ world, lights, camera, render
world = bpy.data.worlds.new("studio"); scene.world = world; world.use_nodes = True
wn = world.node_tree.nodes; wl = world.node_tree.links
bg = wn.get("Background")
if VIEW == "terrace":
    tc = wn.new("ShaderNodeTexCoord"); sep = wn.new("ShaderNodeSeparateXYZ"); ramp = wn.new("ShaderNodeValToRGB")
    wl.new(tc.outputs["Generated"], sep.inputs[0]); wl.new(sep.outputs["Z"], ramp.inputs["Fac"])
    ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = srgb("#eef1f2")
    ramp.color_ramp.elements[1].position = 0.32; ramp.color_ramp.elements[1].color = srgb("#9ebcd0")
    wl.new(ramp.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 1.0
else:
    bg.inputs["Color"].default_value = srgb("#e6ebee"); bg.inputs["Strength"].default_value = 0.75

sun = bpy.data.lights.new("sun", "SUN"); sun.angle = math.radians(3.0); sun.color = (1.0, 0.95, 0.88)
sob = bpy.data.objects.new("sun", sun); COL.objects.link(sob)
if VIEW == "dollhouse":
    sun.energy = 5.0; sob.rotation_euler = (math.radians(42), 0, math.radians(SUN_RZ if SUN_RZ is not None else -40))
elif VIEW == "topdown":
    sun.energy = 3.4; sob.rotation_euler = (math.radians(32), 0, math.radians(-145))
else:
    sun.energy = 4.2; sun.color = (1.0, 0.93, 0.84); sob.rotation_euler = (math.radians(58), 0, math.radians(SUN_RZ if SUN_RZ is not None else 150))

# soft studio fill from above (dollhouse/topdown)
if not FULL:
    al = bpy.data.lights.new("fill", "AREA"); al.energy = 1500; al.size = 30
    aob = bpy.data.objects.new("fill", al); aob.location = (0, 0, 22); COL.objects.link(aob)
else:
    # warm interior ceiling light so the living room reads through the glass
    for k, (u, v) in enumerate(((3700, 1000), (4700, 1300), (4700, 500), (3900, 400))):
        x, y = W(((u + v) / 2, (u - v) / 2))
        al = bpy.data.lights.new("in%d" % k, "AREA"); al.energy = 320; al.size = 1.8; al.color = (1.0, 0.88, 0.74)
        aob = bpy.data.objects.new("in%d" % k, al); aob.location = (x, y, WALL_H - 0.05); COL.objects.link(aob)
        aob.visible_camera = False; aob.visible_glossy = False; aob.visible_transmission = False
    # the canopy LED line along the terrace edge of the roof (DV6aYANjLBm_02)

if not FULL:
    gp = bpy.data.meshes.new("ground"); bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=120); bm.to_mesh(gp); bm.free()
    gob = bpy.data.objects.new("ground", gp); gob.location = (0, 0, -SLAB - 0.002); COL.objects.link(gob)
    gp.materials.append(MATS["ground"])

cam = bpy.data.cameras.new("cam"); cob = bpy.data.objects.new("cam", cam); COL.objects.link(cob); scene.camera = cob
allpts = []
for p in PLAN["footprint"]:
    for q in p["exterior"]:
        x, y = W(q); allpts += [Vector((x, y, -SLAB)), Vector((x, y, TOP))]
for pg in PLAN["pergolas"]:
    for q in pg["poly"]:
        x, y = W(q); allpts.append(Vector((x, y, 3.05)))


def fit_ortho(rot, aspect, margin=1.06):
    cob.rotation_euler = rot
    bpy.context.view_layer.update()
    M = cob.matrix_world.to_3x3().transposed()
    xs = [(M @ p).x for p in allpts]; ys = [(M @ p).y for p in allpts]
    w = max(xs) - min(xs); h = max(ys) - min(ys)
    cx_, cy_ = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    Mi = cob.matrix_world.to_3x3()
    fwd = Mi @ Vector((0, 0, -1))
    cob.location = Mi @ Vector((cx_, cy_, 0)) - fwd * 60
    cam.type = "ORTHO"; cam.ortho_scale = max(w, h * aspect) * margin
    cam.clip_end = 300


R = scene.render
if VIEW == "dollhouse":
    R.resolution_x, R.resolution_y = 2400, 1600
    fit_ortho((math.radians(DOLL_RX), 0, math.radians(DOLL_RZ)), 2400 / 1600, 1.03)
elif VIEW == "topdown":
    R.resolution_x, R.resolution_y = 2400, 2400
    fit_ortho((0, 0, 0), 1.0, 1.04)
else:
    R.resolution_x, R.resolution_y = 2400, 1600
    cam.type = "PERSP"; cam.lens = LENS; cam.clip_start = 0.05; cam.clip_end = 400
    sx, sy = W(CAM[:2]); tx, ty = W(TGT[:2])
    cob.location = (sx, sy, CAM[2])
    d = Vector((tx - sx, ty - sy, TGT[2] - CAM[2]))
    cob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
R.resolution_percentage = SCALE
R.engine = "CYCLES"
cy = scene.cycles
try:
    cy.device = "CPU"
except Exception:
    pass
cy.samples = SAMPLES; cy.use_denoising = True
try:
    cy.denoiser = "OPENIMAGEDENOISE"
except Exception:
    pass
cy.max_bounces = 8; cy.diffuse_bounces = 4; cy.glossy_bounces = 4; cy.transmission_bounces = 8; cy.transparent_max_bounces = 8
cy.caustics_reflective = False; cy.caustics_refractive = False
cy.sample_clamp_indirect = 8.0
try:
    cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.02
except Exception:
    pass
scene.view_settings.view_transform = "AgX"
for look in ("AgX - Medium High Contrast", "Medium High Contrast", "AgX - Base Contrast"):
    try:
        scene.view_settings.look = look; break
    except Exception:
        continue
scene.view_settings.exposure = EXPO if EXPO is not None else (0.05 if not FULL else 0.0)
R.image_settings.file_format = "PNG"; R.image_settings.color_depth = "8"
R.filepath = OUT
R.threads_mode = "AUTO"
if "--hotspots" in argv:
    # where each room's label point lands on the rendered image (for the web component's 3D hotspots)
    from bpy_extras.object_utils import world_to_camera_view
    bpy.context.view_layer.update()
    hs = {}
    for r in PLAN["rooms"]:
        x, y = W(r["label_at"])
        v = world_to_camera_view(scene, cob, Vector((x, y, 0.05)))
        hs[r["id"]] = [round(v.x, 4), round(1 - v.y, 4)]
    out = os.path.join(ROOT, "renders", "%s-hotspots.json" % VIEW)
    json.dump({"image": os.path.basename(OUT), "size": [R.resolution_x, R.resolution_y], "rooms": hs}, open(out, "w"), indent=1)
    print("HOTSPOTS", out)
    sys.exit(0)
if "--save-blend" in argv:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "apt43-%s.blend" % VIEW))
t0 = time.time()
bpy.ops.render.render(write_still=True)
print("RENDERED", VIEW, OUT, "%.0fs" % (time.time() - t0), "objects", len(COL.objects))
