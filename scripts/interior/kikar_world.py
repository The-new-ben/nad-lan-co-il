# -*- coding: utf-8 -*-
"""Kikar Hamedina (P9b prototype): the real city around the three towers, for the example apartment's renders.

Imported by kikar_interior.py inside Blender 5.2 (Cycles, CPU). What is REAL here, and where it comes from:
  - every building within 2 km of the plot centre, at its surveyed height: the shared world's data file
    plugins/nadlan-config/assets/project-stage/hamedina/world.json (Tel Aviv GIS 513 + the city's 2019 survey; far blocks at
    0.5 m quantisation), the streets (GIS 507) at their width class, the green areas, the city's 2024 tree canopy (crown
    centres and radii), the sea and the Yarkon (GIS 504 water, with the breakwaters), the square's park outline;
  - the three towers exactly as the web world draws them (world.js buildTowers): the municipal base footprint's centre and
    size, a superellipse plate (n 4.5), 4.0 m a floor (provisional), a 0.45 m slab reaching 1.25 m beyond the glass, each
    floor turned 1.25 degrees counter-clockwise from above (world.json model), towers A and C 40 floors, B 37 + a crown;
  - the sun: the same suncalc formula the world uses, for 32.086758 N 34.789776 E and Israel's clock (UTC+3 on 21.9.2026).
What is an ILLUSTRATION: every facade texture (plaster tones, windows, shutters, roof clutter, the towers' glass and fins at
1.5 m), the ground between buildings, the tree shapes, the water's waves, the haze. The world's frame: x metres east, z metres
south of the plot centre; Blender here: X east, Y north (= -z), Z up.
No file is downloaded: every material is procedural, every object is built from primitives."""
import base64
import datetime
import json
import math
import os
import random
import struct

import bmesh
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
WORLD_JSON = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "hamedina", "world.json")
DEG = math.pi / 180.0
LAT, LNG = 32.086758, 34.789776

scene = None
W = {}          # the decoded world
TOD = {}        # the chosen time of day
rnd = random.Random(1948)


# ============================================================================================ the sun (world.js sunPos)
def sun_pos(dt_utc):
    J1970, J2000, OBL = 2440588, 2451545, DEG * 23.4397
    lw, phi = DEG * -LNG, DEG * LAT
    d = dt_utc.timestamp() / 86400.0 - 0.5 + J1970 - J2000
    M = DEG * (357.5291 + 0.98560028 * d)
    C = DEG * (1.9148 * math.sin(M) + 0.02 * math.sin(2 * M) + 0.0003 * math.sin(3 * M))
    L = M + C + DEG * 102.9372 + math.pi
    dec = math.asin(math.sin(OBL) * math.sin(L))
    ra = math.atan2(math.sin(L) * math.cos(OBL), math.cos(L))
    H = DEG * (280.16 + 360.9856235 * d) - lw - ra
    az = math.atan2(math.sin(H), math.cos(H) * math.sin(phi) - math.tan(dec) * math.cos(phi))
    alt = math.asin(math.sin(phi) * math.sin(dec) + math.cos(phi) * math.cos(dec) * math.cos(H))
    return ((az / DEG) + 180 + 360) % 360, alt / DEG


def sun_at(month, day, hour, utc_off=3):
    t = datetime.datetime(2026, month, day, tzinfo=datetime.timezone.utc) + datetime.timedelta(minutes=round(hour * 60) - utc_off * 60)
    return sun_pos(t)


# the three times of day of the prototype (21.9.2026, the world's default season; Israel daylight time UTC+3)
TIMES = {
    "day": dict(m=9, d=21, h=14.5, label="21.9 · 14:30"),
    "sunset": dict(m=9, d=21, h=17.6, label="21.9 · 17:36"),
    # evening v2 (1.10.2026): 19:00, the sun 5.06 degrees below the horizon (this file's suncalc); 19:06 (the first evening
    # render) is 6.33 below, past civil twilight: the western afterglow is gone and the room outshines the view
    "evening": dict(m=9, d=21, h=19.0, label="21.9 · 19:00"),
}


def dirv(b):
    return Vector((math.sin(b * DEG), math.cos(b * DEG), 0.0))


# ============================================================================================ the world data (world.js decode)
def _ints(x):
    if isinstance(x, str):
        raw = base64.b64decode(x)
        return struct.unpack("<%dh" % (len(raw) // 2), raw)
    return x


def _unpack(arr, off, n, q):
    x = z = 0
    P = []
    for i in range(n):
        x += arr[off + 2 * i]
        z += arr[off + 2 * i + 1]
        P.append((x * q, -z * q))          # -> Blender (X east, Y north)
    return P


def load_world():
    d = json.load(open(WORLD_JSON, encoding="utf-8"))
    W["raw"] = d
    W["model"] = d["model"]
    A = _ints(d["blocks"]["data"])
    bq, bqf = d["blocks"]["q"], d["blocks"].get("q_far", d["blocks"]["q"])
    blocks, o = [], 0
    while o < len(A):
        n, h, floors, year, flags = A[o], A[o + 1] * bq, A[o + 2], A[o + 3], A[o + 4] & 0xFFFF
        P = _unpack(A, o + 5, n, bqf if flags & 256 else bq)
        o += 5 + 2 * n
        blocks.append(dict(P=P, h=h, floors=floors, year=year, flags=flags))
    W["blocks"] = blocks
    S = _ints(d["streets"]["data"])
    streets, o = [], 0
    while o < len(S):
        n, w, fl = S[o], S[o + 1], S[o + 2]
        streets.append(dict(w=w, ring=bool(fl & 1), P=_unpack(S, o + 4, n, d["streets"]["q"])))
        o += 4 + 2 * n
    W["streets"] = streets
    G = _ints(d["greens"]["data"])
    greens, o = [], 0
    while o < len(G):
        n, fl = G[o], G[o + 2]
        greens.append(dict(square=bool(fl & 1), P=_unpack(G, o + 3, n, d["greens"]["q"])))
        o += 3 + 2 * n
    W["greens"] = greens
    W["water"] = [dict(outer=bool(w["o"]), name=(d["names"][w["n"]] if w["n"] >= 0 else ""),
                       P=_unpack(w["p"], 0, len(w["p"]) // 2, d["water"]["q"])) for w in d["water"]["rings"]]
    T = _ints(d["trees"]["data"])
    tq = d["trees"]["q"]
    W["trees"] = [(T[i] * tq, -T[i + 1] * tq, T[i + 2] * tq) for i in range(0, len(T) - 2, 3)]
    W["park"] = _unpack(d["park"]["p"], 0, len(d["park"]["p"]) // 2, d["park"]["q"]) if d.get("park") else None
    W["pond"] = _unpack(d["pond"]["p"], 0, len(d["pond"]["p"]) // 2, d["pond"]["q"]) if d.get("pond") else None
    W["towers"] = {t["key"]: t for t in d["towers"]}
    return W


# ============================================================================================ tower geometry (world.js)
def plate_radius(half, n, phi):
    return half / (abs(math.cos(phi)) ** n + abs(math.sin(phi)) ** n) ** (1.0 / n)


def plate_outline(half, n, M=144):
    pts = []
    for k in range(M):
        t = k / M * 2 * math.pi
        c, s = math.cos(t), math.sin(t)
        pts.append((half * math.copysign(abs(c) ** (2 / n), c), half * math.copysign(abs(s) ** (2 / n), s)))
    return pts


def plate_at(t, f):
    m = W["model"]
    N = t["floors"]
    return t["base_bearing"] + m["twist_dir"] * m["twist"] * (min(max(f, 1), N) - 1)


def tower_xy(t):
    return Vector((t["cx"], -t["cz"], 0.0))


def eye_h(f):
    return (f - 1) * W["model"]["fh"] + 1.6


def facing_bearings(k, f):
    th = plate_at(W["towers"][k], f)
    lst = sorted(((th + i * 45) % 360) for i in range(8))
    s = min(range(8), key=lambda i: min(lst[i], 360 - lst[i]))
    return lst[s:] + lst[:s]


# ============================================================================================ render setup
def init(width, height, samples, threads, exposure=0.0, look="AgX - Base Contrast"):
    global scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    c = scene.cycles
    c.device = "CPU"
    c.samples = samples
    c.use_adaptive_sampling = True
    c.adaptive_threshold = 0.012
    c.adaptive_min_samples = 32
    c.use_denoising = True
    try:
        c.denoiser = "OPENIMAGEDENOISE"
        c.denoising_input_passes = "RGB_ALBEDO_NORMAL"
        c.denoising_prefilter = "ACCURATE"
        c.denoising_quality = "HIGH"
    except Exception:
        pass
    c.max_bounces = 10
    c.diffuse_bounces = 5
    c.glossy_bounces = 4
    c.transmission_bounces = 10
    c.transparent_max_bounces = 24
    c.volume_bounces = 0
    c.caustics_reflective = False
    c.caustics_refractive = False
    c.blur_glossy = 1.0
    c.sample_clamp_direct = 0.0
    c.sample_clamp_indirect = 6.0
    try:
        c.use_light_tree = True
    except Exception:
        pass
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.threads_mode = "FIXED"
    scene.render.threads = max(1, threads)
    scene.render.use_persistent_data = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_depth = "16"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = look
    scene.view_settings.exposure = exposure
    scene.render.film_transparent = False
    return scene


def link(ob):
    bpy.context.scene.collection.objects.link(ob)
    return ob


def mesh_object(name, verts, faces, mats=None, smooth=False):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate(clean_customdata=False)
    me.update()
    ob = bpy.data.objects.new(name, me)
    for m in (mats or []):
        me.materials.append(m)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    return link(ob)


# ============================================================================================ node helpers
class NB:
    """a small node-tree builder: n() makes a node, m() a math node, v() a vector-math node; inputs may be sockets or numbers"""

    def __init__(self, nt):
        self.nt = nt
        self.x = 0

    def n(self, typ, inputs=None, **props):
        nd = self.nt.nodes.new(typ)
        nd.location = (self.x, 0)
        self.x += 40
        for k, v in props.items():
            setattr(nd, k, v)
        for k, v in (inputs or {}).items():
            self.put(nd.inputs[k], v)
        return nd

    def put(self, sock, v):
        if hasattr(v, "is_output") or hasattr(v, "links"):
            self.nt.links.new(v, sock)
        elif isinstance(v, bpy.types.Node):
            self.nt.links.new(v.outputs[0], sock)
        else:
            if isinstance(v, (tuple, list)) and len(v) == 3 and getattr(sock, "type", "") == "RGBA":
                v = (*v, 1.0)
            sock.default_value = v

    def m(self, op, a, b=None, clamp=False):
        nd = self.n("ShaderNodeMath", operation=op, use_clamp=clamp)
        self.put(nd.inputs[0], a)
        if b is not None:
            self.put(nd.inputs[1], b)
        return nd.outputs[0]

    def mix(self, fac, a, b):
        nd = self.n("ShaderNodeMix", data_type="RGBA", blend_type="MIX")
        self.put(nd.inputs["Factor"], fac)
        self.put(nd.inputs[6], a)
        self.put(nd.inputs[7], b)
        return nd.outputs[2]

    def mixf(self, fac, a, b):
        nd = self.n("ShaderNodeMix", data_type="FLOAT")
        self.put(nd.inputs["Factor"], fac)
        self.put(nd.inputs[2], a)
        self.put(nd.inputs[3], b)
        return nd.outputs[0]

    def mixs(self, fac, a, b):
        nd = self.n("ShaderNodeMixShader")
        self.put(nd.inputs[0], fac)
        self.nt.links.new(a, nd.inputs[1])
        self.nt.links.new(b, nd.inputs[2])
        return nd.outputs[0]

    def addsh(self, a, b):
        nd = self.n("ShaderNodeAddShader")
        self.nt.links.new(a, nd.inputs[0])
        self.nt.links.new(b, nd.inputs[1])
        return nd.outputs[0]

    def ramp(self, fac, stops, interp="LINEAR"):
        nd = self.n("ShaderNodeValToRGB")
        cr = nd.color_ramp
        cr.interpolation = interp
        while len(cr.elements) > 1:
            cr.elements.remove(cr.elements[-1])
        cr.elements[0].position = stops[0][0]
        cr.elements[0].color = (*stops[0][1], 1)
        for p, c in stops[1:]:
            e = cr.elements.new(p)
            e.color = (*c, 1)
        self.put(nd.inputs[0], fac)
        return nd.outputs[0]

    def noise(self, vec, scale, detail=3.0, rough=0.55, dims="3D", w=None):
        nd = self.n("ShaderNodeTexNoise", noise_dimensions=dims)
        if vec is None:
            vec = self.n("ShaderNodeTexCoord").outputs["Object"]
        self.put(nd.inputs["Vector"], vec)
        nd.inputs["Scale"].default_value = scale
        nd.inputs["Detail"].default_value = detail
        nd.inputs["Roughness"].default_value = rough
        if w is not None and "W" in nd.inputs:
            self.put(nd.inputs["W"], w)
        return nd

    def white(self, vec, dims="3D"):
        nd = self.n("ShaderNodeTexWhiteNoise", noise_dimensions=dims)
        self.put(nd.inputs["Vector"], vec)
        return nd.outputs["Value"]

    def combine(self, x, y, z):
        nd = self.n("ShaderNodeCombineXYZ")
        self.put(nd.inputs[0], x)
        self.put(nd.inputs[1], y)
        self.put(nd.inputs[2], z)
        return nd.outputs[0]

    def sep(self, vec):
        nd = self.n("ShaderNodeSeparateXYZ")
        self.put(nd.inputs[0], vec)
        return nd.outputs

    def bump(self, height, strength, dist=1.0, normal=None):
        nd = self.n("ShaderNodeBump")
        self.put(nd.inputs["Height"], height)
        nd.inputs["Strength"].default_value = strength
        nd.inputs["Distance"].default_value = dist
        if normal is not None:
            self.put(nd.inputs["Normal"], normal)
        return nd.outputs[0]

    def attr(self, name, kind="GEOMETRY"):
        nd = self.n("ShaderNodeAttribute", attribute_type=kind, attribute_name=name)
        return nd

    def principled(self, **ins):
        nd = self.n("ShaderNodeBsdfPrincipled")
        for k, v in ins.items():
            self.put(nd.inputs[k.replace("_", " ")], v)
        return nd


def new_mat(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    return m, nt, NB(nt), out


# ============================================================================================ sky, sun and haze
SKY = {}
SKY_FILL = 0.85          # the sky's light on diffuse surfaces, relative to the sky one sees
SKY_FILL_DESAT = 0.30    # and how much of its blue is taken out


def sky_params(tod):
    t = TIMES[tod]
    if tod == "evening" and os.environ.get("KH_EVE_H"):       # previews of the blue hour at another minute
        hh = float(os.environ["KH_EVE_H"])
        t = dict(t, h=hh, label="21.9 · %02d:%02d" % (int(hh), round(hh % 1 * 60)))
    b, a = sun_at(t["m"], t["d"], t["h"])
    TOD.update(name=tod, bearing=b, alt=a, label=t["label"])
    # coastal September air: humid, a little dusty; the haze's reach in metres (the far city fades into the sky)
    if tod == "day":
        TOD.update(air=1.25, aerosol=2.2, ozone=1.0, strength=0.30, haze_L=7500.0, night=0.0, exposure=0.0)
    elif tod == "sunset":
        TOD.update(air=1.2, aerosol=1.9, ozone=1.0, strength=0.34, haze_L=6500.0, night=0.0, exposure=0.0)
    else:
        TOD.update(air=1.3, aerosol=2.4, ozone=1.2, strength=0.95, haze_L=7000.0, night=1.0, exposure=0.0)
    return TOD


def sky_node(b, disc):
    sk = b.n("ShaderNodeTexSky")
    sk.sky_type = "MULTIPLE_SCATTERING"
    sk.sun_disc = disc
    sk.sun_elevation = TOD["alt"] * DEG
    sk.sun_rotation = TOD["bearing"] * DEG            # checked: the rotation is the true bearing, clockwise from north
    sk.altitude = 120.0
    sk.air_density = TOD["air"]
    sk.aerosol_density = TOD["aerosol"]
    sk.ozone_density = TOD["ozone"]
    if disc:
        sk.sun_size = 0.545 * DEG
        sk.sun_intensity = 1.0
    return sk


def build_sky(tod):
    """the world: a physical sky (multiple scattering) at the true sun position; its sun disc is seen by the camera and in
    glossy reflections (the sea's glitter path), while the Sun lamp (calibrated from the same sky) lights diffuse surfaces"""
    sky_params(tod)
    world = bpy.data.worlds.new("sky")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    b = NB(nt)
    s_no = sky_node(b, False)
    s_disc = sky_node(b, TOD["alt"] > -0.5)
    lp = b.n("ShaderNodeLightPath")
    vis = b.m("MAXIMUM", lp.outputs["Is Camera Ray"], lp.outputs["Is Glossy Ray"])
    # the fill the sky gives to shadows: less saturated and a little weaker than the sky one sees (in a city the shade is
    # also lit by warm, sunlit walls; an open-field sky made every shadow on the ground read as blue water)
    bw = b.n("ShaderNodeRGBToBW")
    b.put(bw.inputs[0], s_no.outputs[0])
    fill = b.mix(SKY_FILL_DESAT, s_no.outputs[0], b.combine(bw.outputs[0], bw.outputs[0], bw.outputs[0]))
    fillm = b.n("ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
    b.put(fillm.inputs["Factor"], 1.0)
    b.put(fillm.inputs[6], fill)
    b.put(fillm.inputs[7], (SKY_FILL, SKY_FILL, SKY_FILL))
    col = b.mix(vis, fillm.outputs[2], s_disc.outputs[0])
    bg = b.n("ShaderNodeBackground", {"Color": col, "Strength": TOD["strength"]})
    out = b.n("ShaderNodeOutputWorld")
    nt.links.new(bg.outputs[0], out.inputs[0])
    try:
        world.cycles.sampling_method = "MANUAL"
        world.cycles.sample_map_resolution = 2048
    except Exception:
        pass
    SKY["world"] = world
    return world


def calibrate_sun():
    """measures the sky's own sun disc (radiance x solid angle) with a tiny camera aimed at it, so the Sun lamp carries the
    same colour and power as the sky's sun at this hour (orange and weak at 10 degrees, white at 48)"""
    if TOD["alt"] < 0.3:
        return None
    sc = scene
    keep = (sc.render.resolution_x, sc.render.resolution_y, sc.cycles.samples, sc.camera, sc.view_settings.view_transform,
            sc.view_settings.look, sc.view_settings.exposure, sc.cycles.use_denoising, sc.render.image_settings.file_format,
            sc.render.image_settings.color_depth)
    cd = bpy.data.cameras.new("probe")
    cd.lens_unit = "FOV"
    cd.angle = 0.30 * DEG                     # smaller than the disc (0.545): every pixel sees the sun
    cd.clip_start = 0.1
    cam = bpy.data.objects.new("probe", cd)
    link(cam)
    d = Vector((math.sin(TOD["bearing"] * DEG) * math.cos(TOD["alt"] * DEG), math.cos(TOD["bearing"] * DEG) * math.cos(TOD["alt"] * DEG),
                math.sin(TOD["alt"] * DEG)))
    cam.location = (0, 0, 20000)             # high above everything
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    hide = [o for o in sc.objects if o.type == "MESH"]
    for o in hide:
        o.hide_render = True
    sc.camera = cam
    sc.render.resolution_x = sc.render.resolution_y = 8
    sc.cycles.samples = 16
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = 0.0
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    p = os.path.join(bpy.app.tempdir or HERE, "sunprobe.exr")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = list(im.pixels[:])
    n = len(px) // 4
    rgb = [sum(px[i * 4 + c] for i in range(n)) / n for c in range(3)]
    bpy.data.images.remove(im)
    for o in hide:
        o.hide_render = False
    (sc.render.resolution_x, sc.render.resolution_y, sc.cycles.samples, sc.camera, sc.view_settings.view_transform,
     sc.view_settings.look, sc.view_settings.exposure, sc.cycles.use_denoising, sc.render.image_settings.file_format,
     sc.render.image_settings.color_depth) = keep
    bpy.data.objects.remove(cam)
    # radiance (already x background strength) x the disc's solid angle = irradiance on a surface facing the sun
    omega = 2 * math.pi * (1 - math.cos(0.2725 * DEG))
    E = [c * omega for c in rgb]
    peak = max(E)
    TOD["sun_rgb"] = [c / peak for c in E] if peak > 0 else [1, 1, 1]
    TOD["sun_E"] = peak
    return E


def build_sun():
    if TOD["alt"] < 0.3:
        return None
    E = calibrate_sun()
    sd = bpy.data.lights.new("sun", "SUN")
    sd.energy = TOD["sun_E"]
    sd.color = TOD["sun_rgb"]
    sd.angle = 0.545 * DEG
    ob = bpy.data.objects.new("sun", sd)
    link(ob)
    ob.visible_glossy = False            # the sky's disc gives the glossy highlight (the sea's glitter); no double sun
    ob.visible_camera = False
    d = Vector((math.sin(TOD["bearing"] * DEG) * math.cos(TOD["alt"] * DEG), math.cos(TOD["bearing"] * DEG) * math.cos(TOD["alt"] * DEG),
                math.sin(TOD["alt"] * DEG)))
    ob.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    print("SUN bearing %.1f alt %.2f E %.3f rgb %s" % (TOD["bearing"], TOD["alt"], TOD["sun_E"], [round(c, 3) for c in TOD["sun_rgb"]]))
    return ob


def haze(b, out_node, surf, reach=None):
    """aerial perspective: the surface fades into the sky's own horizon colour in the direction it is seen, over the
    haze's reach (1 - exp(-distance / reach)); the far city pales into the sky as it does over Tel Aviv"""
    L = reach or TOD["haze_L"]
    cd = b.n("ShaderNodeCameraData")
    fac = b.m("SUBTRACT", 1.0, b.m("EXPONENT", b.m("MULTIPLY", cd.outputs["View Distance"], -1.0 / L)), clamp=True)
    fac = b.m("MULTIPLY", fac, 0.97)
    geo = b.n("ShaderNodeNewGeometry")
    inc = b.sep(geo.outputs["Incoming"])
    hx = b.m("MULTIPLY", inc[0], -1.0)
    hy = b.m("MULTIPLY", inc[1], -1.0)
    vec = b.n("ShaderNodeVectorMath", operation="NORMALIZE")
    b.put(vec.inputs[0], b.combine(hx, hy, 0.035 if TOD["alt"] > 2 else 0.06))
    sk = sky_node(b, False)
    b.put(sk.inputs["Vector"], vec.outputs[0])
    em = b.n("ShaderNodeEmission", {"Color": sk.outputs[0], "Strength": TOD["strength"]})
    final = b.mixs(fac, surf, em.outputs[0])
    b.nt.links.new(final, out_node.inputs["Surface"])
    return final


def add_glare(threshold, strength=0.3, size=0.6):
    """a gentle photographic bloom in the compositor (scene-linear, before the view transform): only what is far brighter
    than the picture's white glows (the sun's disc, a hot reflection, a lamp at night), as it does through a real lens"""
    sc = bpy.context.scene
    tree = bpy.data.node_groups.new("bloom", "CompositorNodeTree")
    tree.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = tree.nodes.new("CompositorNodeRLayers")
    gl = tree.nodes.new("CompositorNodeGlare")
    out = tree.nodes.new("NodeGroupOutput")
    gl.inputs["Type"].default_value = "Bloom"
    gl.inputs["Quality"].default_value = "High"
    gl.inputs["Threshold"].default_value = threshold
    gl.inputs["Strength"].default_value = strength
    gl.inputs["Size"].default_value = size
    tree.links.new(rl.outputs["Image"], gl.inputs["Image"])
    tree.links.new(gl.outputs["Image"], out.inputs[0])
    sc.compositing_node_group = tree
    sc.render.use_compositing = True
    return tree


# ============================================================================================ exterior materials
MAT = {}

# evening v2 (1.10.2026): the lit windows of the city at the blue hour. Emission per window = a room behind the glass, found
# by INTERIOR MAPPING (Joost van Dongen, "Interior Mapping", CGI 2008,
# https://www.proun-game.com/Oogst3D/CODING/InteriorMapping/InteriorMapping.pdf; the idea as a three.js port:
# https://github.com/codedgar/three-fenestra): the view ray is cast, inside the shader, against the virtual floor, ceiling,
# side walls and back wall of a room behind each window cell, and the surface it meets is shaded by one lamp in that room.
# The rooms, which ones are lit, their lamps, curtains and colours are an ILLUSTRATION (random per building, floor and room).
NIGHT_LIT = {"tall": 0.30, "low": 0.42}       # the share of apartments with a light on (x 0.82 of their rooms + a few singles)
NIGHT_K = {"tall": 0.60, "low": 1.20}         # emission at the lamp's peak (the room's radiance is shaded below it)


def _vmath(b, op, a, c=None, out="Vector"):
    nd = b.n("ShaderNodeVectorMath", operation=op)
    b.put(nd.inputs[0], a)
    if c is not None:
        b.put(nd.inputs[1], c)
    return nd.outputs[out]


def night_windows(b, geo, u, v, s, tall, glasstower, fh, bay, cu, cv, fu, fv, gl):
    """the city's lit windows at night, as rooms (interior mapping). Returns (emission colour, emission strength).
    Towers (btall): rooms 3.0 / 4.5 / 6.0 m wide on the 1.5 m mullion grid, 2-3 rooms an apartment, lit in runs along a floor;
    glass towers keep a dark slab band (floor edge + spandrel) between the floors. Low-rise: each window bay is a room, three
    bays an apartment. About 25-30% of the windows lit: warm 2700-3800 K, a few cool white, a few TV-blue; some sheers half
    drawn, some blinds half down; each lit room has a back wall, a ceiling, a floor and side walls lit by its own lamp."""
    m = b.m
    I = geo.outputs["Incoming"]
    N = geo.outputs["Normal"]
    T = _vmath(b, "NORMALIZE", _vmath(b, "CROSS_PRODUCT", (0.0, 0.0, 1.0), N))   # along the wall (+u), the walls are vertical
    du = m("MULTIPLY", _vmath(b, "DOT_PRODUCT", I, T, "Value"), -1.0)             # the ray into the room, in the wall's frame
    dv = m("MULTIPLY", b.sep(I)[2], -1.0)
    dn = m("MAXIMUM", _vmath(b, "DOT_PRODUCT", I, N, "Value"), 0.03)
    # the room grid
    wt = m("MULTIPLY", 1.5, m("ADD", 2.0, m("FLOOR", m("MULTIPLY", m("FRACT", m("MULTIPLY", s, 11.3)), 2.999))))
    nat = m("ADD", 2.0, m("FLOOR", m("MULTIPLY", m("FRACT", m("MULTIPLY", s, 5.9)), 1.999)))
    rit = m("FLOOR", m("DIVIDE", u, wt))
    Wr = b.mixf(tall, bay, wt)
    px = b.mixf(tall, m("MULTIPLY", fu, bay), m("MULTIPLY", m("FRACT", m("DIVIDE", u, wt)), wt))
    ri = b.mixf(tall, cu, rit)
    ap = b.mixf(tall, m("FLOOR", m("DIVIDE", cu, 3.0)), m("FLOOR", m("DIVIDE", rit, nat)))
    Hr = fh
    py = m("MULTIPLY", fv, fh)
    # per room: three randoms and a fourth; per apartment: is anybody home
    wn = b.n("ShaderNodeTexWhiteNoise", noise_dimensions="3D")
    b.put(wn.inputs["Vector"], b.combine(ri, cv, m("ADD", m("MULTIPLY", s, 91.0), m("MULTIPLY", tall, 7.0))))
    r1, r2, r3 = b.sep(wn.outputs["Color"])
    r4 = wn.outputs["Value"]
    ra = b.white(b.combine(ap, cv, m("MULTIPLY", s, 57.0)))
    rq = b.white(b.combine(ri, cv, m("ADD", m("MULTIPLY", s, 23.0), 5.0)))
    homeA = m("LESS_THAN", ra, b.mixf(tall, NIGHT_LIT["low"], NIGHT_LIT["tall"]))
    lit = m("MAXIMUM", m("MULTIPLY", homeA, m("LESS_THAN", rq, 0.82)), m("LESS_THAN", rq, 0.035))
    # a dim glow (a light left on in the hall, deeper in the flat) in some of the other rooms
    lit = m("MAXIMUM", lit, m("MULTIPLY", m("GREATER_THAN", rq, 0.90), 0.16))
    Dr = m("ADD", 3.2, m("MULTIPLY", r2, 3.0))
    # interior mapping: the distance along the ray to the side wall, the floor or ceiling, and the back wall ahead of it
    gx = m("GREATER_THAN", du, 0.0)
    tx = m("DIVIDE", m("ADD", px, m("MULTIPLY", gx, m("SUBTRACT", Wr, m("MULTIPLY", px, 2.0)))), m("ADD", m("ABSOLUTE", du), 1e-4))
    gy = m("GREATER_THAN", dv, 0.0)
    ty = m("DIVIDE", m("ADD", py, m("MULTIPLY", gy, m("SUBTRACT", Hr, m("MULTIPLY", py, 2.0)))), m("ADD", m("ABSOLUTE", dv), 1e-4))
    tz = m("DIVIDE", Dr, dn)
    txy = m("MINIMUM", tx, ty)
    t = m("MINIMUM", txy, tz)
    hx = m("ADD", px, m("MULTIPLY", du, t))
    hy = m("ADD", py, m("MULTIPLY", dv, t))
    hz = m("MULTIPLY", dn, t)
    back = m("LESS_THAN", tz, txy)
    side = m("MULTIPLY", m("SUBTRACT", 1.0, back), m("LESS_THAN", tx, ty))
    # what it meets: a pale back wall (or a darker wardrobe, a picture wall), side walls, a white ceiling, a wooden floor
    alb = b.mixf(back, b.mixf(side, b.mixf(gy, 0.26, 0.72), 0.55), m("ADD", 0.38, m("MULTIPLY", r3, 0.47)))
    # the room's lamp: a ceiling light or a standing lamp, somewhere in the room; light falls off with distance
    lx = m("MULTIPLY", Wr, m("ADD", 0.2, m("MULTIPLY", r1, 0.6)))
    lz = m("MULTIPLY", Dr, m("ADD", 0.3, m("MULTIPLY", m("FRACT", m("MULTIPLY", r1, 7.7)), 0.45)))
    ly = b.mixf(m("GREATER_THAN", r2, 0.5), 1.25, m("SUBTRACT", Hr, 0.35))
    d2 = m("ADD", m("ADD", m("POWER", m("SUBTRACT", hx, lx), 2.0), m("POWER", m("SUBTRACT", hy, ly), 2.0)),
           m("POWER", m("SUBTRACT", hz, lz), 2.0))
    E = m("ADD", 0.10, m("DIVIDE", 1.6, m("ADD", 1.0, m("MULTIPLY", d2, 0.9))))
    # the light's colour: mostly warm (2700-3800 K), some cool white; a few rooms lit only by a television
    tk = m("FRACT", m("MULTIPLY", r3, 3.7))
    tint = b.ramp(tk, [(0.0, (1.0, 0.36, 0.10)), (0.30, (1.0, 0.47, 0.17)), (0.55, (1.0, 0.56, 0.26)), (0.80, (1.0, 0.68, 0.44)),
                       (0.90, (0.90, 0.90, 0.96))], "LINEAR")
    tv = m("GREATER_THAN", m("FRACT", m("MULTIPLY", r2, 9.1)), 0.93)
    tint = b.mix(tv, tint, (0.30, 0.45, 1.0))
    E = m("MULTIPLY", E, b.mixf(tv, 1.0, 0.45))
    room = b.n("ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
    b.put(room.inputs["Factor"], 1.0)
    b.put(room.inputs[6], tint)
    ae = m("MULTIPLY", alb, E)
    b.put(room.inputs[7], b.combine(ae, ae, ae))
    room = room.outputs[2]
    # curtains just behind the glass: open (42%), sheers drawn in from the sides (36%), blinds down from the top (22%)
    tc = m("DIVIDE", 0.2, dn)
    xn = m("DIVIDE", m("ADD", px, m("MULTIPLY", du, tc)), Wr)
    yn = m("DIVIDE", m("ADD", py, m("MULTIPLY", dv, tc)), Hr)
    is_sheer = m("MULTIPLY", m("GREATER_THAN", r4, 0.42), m("LESS_THAN", r4, 0.78))
    is_blind = m("GREATER_THAN", r4, 0.78)
    cwl = m("ADD", 0.08, m("MULTIPLY", m("FRACT", m("MULTIPLY", r4, 7.3)), 0.42))
    cwr = m("ADD", 0.08, m("MULTIPLY", m("FRACT", m("MULTIPLY", r4, 13.1)), 0.42))
    sheer = m("MULTIPLY", is_sheer, m("MAXIMUM", m("LESS_THAN", xn, cwl), m("GREATER_THAN", xn, m("SUBTRACT", 1.0, cwr))))
    bl = m("ADD", 0.15, m("MULTIPLY", m("FRACT", m("MULTIPLY", r4, 5.7)), 0.6))
    blind = m("MULTIPLY", is_blind, m("GREATER_THAN", yn, m("SUBTRACT", 1.0, bl)))
    slat = m("ADD", 0.72, m("MULTIPLY", m("LESS_THAN", m("FRACT", m("MULTIPLY", yn, 14.0)), 0.55), 0.28))
    glow = m("MULTIPLY", m("ADD", 0.28, m("MULTIPLY", r3, 0.22)), b.mixf(blind, 0.9, m("MULTIPLY", slat, 0.55)))
    ccol = b.n("ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
    b.put(ccol.inputs["Factor"], 1.0)
    b.put(ccol.inputs[6], tint)
    b.put(ccol.inputs[7], b.combine(glow, glow, glow))
    cov = m("MAXIMUM", m("MULTIPLY", sheer, 0.82), m("MULTIPLY", blind, 0.96))
    col = b.mix(cov, room, ccol.outputs[2])
    # where light can come out: the glass (gl: reveals, shutters and mullions already dark); glass towers keep a slab band
    band = b.mixf(glasstower, 1.0, m("MULTIPLY", m("GREATER_THAN", fv, 0.10), m("LESS_THAN", fv, 0.93)))
    k = b.mixf(tall, NIGHT_K["low"], NIGHT_K["tall"])
    k = m("MULTIPLY", k, m("ADD", 0.45, m("MULTIPLY", m("POWER", m("FRACT", m("MULTIPLY", r2, 3.3)), 1.6), 1.25)))
    estr = m("MULTIPLY", m("MULTIPLY", m("MULTIPLY", lit, gl), band), k)
    return col, estr


def facade_material():
    """the city's buildings: plaster in the tones of Tel Aviv's streets, rows of windows, some roller shutters half down,
    a dark shaded ground floor (pilotis and shop fronts), balcony shadow lines; glass towers and white towers above 45 m.
    Per building: the face attribute 'bseed' (0..1) and 'btall'; per face: the UV map (metres along the wall, height)"""
    m, nt, b, out = new_mat("city_facade")
    at = b.attr("bseed")
    s = at.outputs["Fac"]
    tall = b.attr("btall").outputs["Fac"]
    uv = b.n("ShaderNodeUVMap", uv_map="fac")
    u, v, _ = b.sep(uv.outputs[0])
    geo = b.n("ShaderNodeNewGeometry")
    nz = b.sep(geo.outputs["Normal"])[2]
    roof = b.m("GREATER_THAN", nz, 0.5)
    # per-building rhythm
    fh = b.m("ADD", 2.95, b.m("MULTIPLY", b.m("FRACT", b.m("MULTIPLY", s, 7.31)), 0.45))
    bay = b.m("ADD", 2.6, b.m("MULTIPLY", b.m("FRACT", b.m("MULTIPLY", s, 13.7)), 1.6))
    ww = b.m("ADD", 0.34, b.m("MULTIPLY", b.m("FRACT", b.m("MULTIPLY", s, 5.13)), 0.26))
    uo = b.m("ADD", u, b.m("MULTIPLY", s, 17.0))
    cu = b.m("FLOOR", b.m("DIVIDE", uo, bay))
    cv = b.m("FLOOR", b.m("DIVIDE", v, fh))
    fu = b.m("FRACT", b.m("DIVIDE", uo, bay))
    fv = b.m("FRACT", b.m("DIVIDE", v, fh))
    half = b.m("MULTIPLY", ww, 0.5)
    inu = b.m("MULTIPLY", b.m("GREATER_THAN", fu, b.m("SUBTRACT", 0.5, half)), b.m("LESS_THAN", fu, b.m("ADD", 0.5, half)))
    inv = b.m("MULTIPLY", b.m("GREATER_THAN", fv, 0.30), b.m("LESS_THAN", fv, 0.84))
    above = b.m("GREATER_THAN", v, 3.3)
    win = b.m("MULTIPLY", b.m("MULTIPLY", inu, inv), above)
    ground = b.m("LESS_THAN", v, 3.1)
    cell = b.combine(cu, cv, b.m("MULTIPLY", s, 91.0))
    rw = b.white(cell)
    rw2 = b.white(b.combine(cv, cu, b.m("MULTIPLY", s, 53.0)))
    # roller shutters (the Tel Aviv "trisim"): some down a little, some half, a few closed
    sh = b.m("MULTIPLY", b.m("POWER", rw, 2.2), 0.95)
    wv = b.m("DIVIDE", b.m("SUBTRACT", fv, 0.30), 0.54)          # 0 at the sill, 1 at the head
    shut = b.m("MULTIPLY", win, b.m("GREATER_THAN", wv, b.m("SUBTRACT", 1.0, sh)))
    glass = b.m("MULTIPLY", win, b.m("SUBTRACT", 1.0, shut))
    # plaster tones (by building), soiled by weather
    plaster = b.ramp(s, [(0.00, (0.66, 0.62, 0.56)), (0.13, (0.59, 0.55, 0.49)), (0.26, (0.64, 0.58, 0.48)),
                         (0.38, (0.54, 0.49, 0.42)), (0.50, (0.70, 0.67, 0.62)), (0.61, (0.51, 0.48, 0.44)),
                         (0.72, (0.62, 0.54, 0.43)), (0.82, (0.58, 0.50, 0.42)), (0.91, (0.68, 0.63, 0.55)), (1.0, (0.60, 0.57, 0.52))], "CONSTANT")
    dirt = b.noise(b.combine(b.m("MULTIPLY", u, 0.35), b.m("MULTIPLY", v, 0.08), b.m("MULTIPLY", s, 40.0)), 1.0, 4.0, 0.6)
    dfac = b.m("ADD", 0.84, b.m("MULTIPLY", dirt.outputs["Fac"], 0.26))
    pl = b.n("ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
    b.put(pl.inputs["Factor"], 1.0)
    b.put(pl.inputs[6], plaster)
    b.put(pl.inputs[7], b.combine(dfac, dfac, dfac))
    pl = pl.outputs[2]
    # balcony parapets: a bright band and a shadow line under each slab
    band = b.m("MULTIPLY", b.m("LESS_THAN", fv, 0.07), b.m("GREATER_THAN", v, 2.9))
    col = b.mix(b.m("MULTIPLY", band, 0.45), pl, (0.24, 0.23, 0.21))
    # window reveals, and recessed balconies (a bright parapet, a deep shadow): the striped look of Tel Aviv's blocks
    rev = b.m("MULTIPLY", b.m("MULTIPLY", b.m("GREATER_THAN", fu, b.m("SUBTRACT", 0.46, half)), b.m("LESS_THAN", fu, b.m("ADD", 0.54, half))),
              b.m("MULTIPLY", b.m("GREATER_THAN", fv, 0.25), b.m("LESS_THAN", fv, 0.88)))
    col = b.mix(b.m("MULTIPLY", b.m("MULTIPLY", rev, above), 0.45), col, (0.16, 0.155, 0.15))
    rw3 = b.white(b.combine(cu, b.m("FLOOR", b.m("DIVIDE", cv, 50.0)), b.m("MULTIPLY", s, 17.0)))
    balc = b.m("MULTIPLY", b.m("LESS_THAN", rw3, b.m("MULTIPLY", b.m("FRACT", b.m("MULTIPLY", s, 3.1)), 0.9)), above)
    par = b.m("MULTIPLY", balc, b.m("LESS_THAN", fv, 0.36))
    deep = b.m("MULTIPLY", balc, b.m("MULTIPLY", b.m("GREATER_THAN", fv, 0.36), b.m("LESS_THAN", fv, 0.95)))
    col = b.mix(b.m("MULTIPLY", par, 0.6), col, (0.70, 0.68, 0.64))
    col = b.mix(deep, col, (0.075, 0.07, 0.065))
    win = b.m("MULTIPLY", win, b.m("SUBTRACT", 1.0, balc))
    col = b.mix(b.m("MULTIPLY", ground, 0.85), col, (0.16, 0.155, 0.15))
    # towers (btall): half glass curtain walls, half white with ribbon windows
    glasstower = b.m("MULTIPLY", tall, b.m("LESS_THAN", b.m("FRACT", b.m("MULTIPLY", s, 3.7)), 0.55))
    whitetower = b.m("MULTIPLY", tall, b.m("SUBTRACT", 1.0, glasstower))
    rib = b.m("MULTIPLY", whitetower, b.m("MULTIPLY", b.m("GREATER_THAN", fv, 0.34), b.m("LESS_THAN", fv, 0.92)))
    mull = b.m("LESS_THAN", b.m("FRACT", b.m("DIVIDE", u, 1.5)), 0.05)
    gt = b.m("MULTIPLY", glasstower, b.m("SUBTRACT", 1.0, mull))
    tglass = b.m("MAXIMUM", gt, b.m("MULTIPLY", rib, b.m("SUBTRACT", 1.0, mull)))
    lowrise = b.m("SUBTRACT", 1.0, tall)
    col = b.mix(tall, col, b.mix(glasstower, (0.83, 0.82, 0.79), (0.55, 0.57, 0.58)))
    # the glass: dark with a sky reflection; a faint warm interior behind some panes by day
    shut = b.m("MULTIPLY", win, b.m("GREATER_THAN", wv, b.m("SUBTRACT", 1.0, sh)))
    glass = b.m("MULTIPLY", win, b.m("SUBTRACT", 1.0, shut))
    gl = b.m("MAXIMUM", b.m("MULTIPLY", glass, lowrise), tglass)
    shutcol = b.mix(rw2, (0.60, 0.58, 0.54), (0.74, 0.72, 0.68))
    col = b.mix(b.m("MULTIPLY", shut, lowrise), col, shutcol)
    gcol = b.mix(rw2, (0.018, 0.020, 0.023), (0.05, 0.045, 0.04))
    gcol = b.mix(tall, gcol, (0.17, 0.20, 0.22))
    col = b.mix(gl, col, gcol)
    # roofs: concrete, a pale coating or dark bitumen (the roof's UV is not a wall's: no window, glass or balcony on it)
    wall = b.m("SUBTRACT", 1.0, roof)
    gl = b.m("MULTIPLY", gl, wall)
    tglass = b.m("MULTIPLY", tglass, wall)
    ground = b.m("MULTIPLY", ground, wall)
    rr = b.m("FRACT", b.m("MULTIPLY", s, 29.3))
    rcol = b.ramp(rr, [(0.0, (0.44, 0.42, 0.39)), (0.45, (0.56, 0.54, 0.50)), (0.75, (0.26, 0.25, 0.24)), (0.9, (0.48, 0.44, 0.39))], "CONSTANT")
    rn = b.noise(None, 0.35, 5.0, 0.6)
    rcol2 = b.mix(b.m("MULTIPLY", rn.outputs["Fac"], 0.35), rcol, (0.30, 0.29, 0.27))
    col = b.mix(roof, col, rcol2)
    rough = b.mixf(gl, 0.86, 0.14)
    rough = b.mixf(tglass, rough, 0.05)
    rough = b.mixf(roof, rough, 0.9)
    spec = b.mixf(gl, 0.35, 0.5)
    spec = b.mixf(tglass, spec, 1.0)
    spec = b.mixf(roof, spec, 0.2)
    p = b.principled(Base_Color=col, Roughness=rough)
    b.put(p.inputs["Specular IOR Level"], spec)
    b.put(p.inputs["Metallic"], b.m("MULTIPLY", tglass, 0.45))
    if TOD.get("night"):
        # night (evening v2): every lit window is a room seen through the glass (interior mapping), see night_windows()
        ecol, estr = night_windows(b, geo, u, v, s, tall, glasstower, fh, bay, cu, cv, fu, fv, gl)
        shop = b.m("MULTIPLY", b.m("MULTIPLY", ground, b.m("LESS_THAN", rw, 0.45)), 0.9)
        shopcol = b.mix(b.m("GREATER_THAN", rw, 0.85), (1.0, 0.60, 0.30), (0.85, 0.88, 1.0))
        ecol = b.mix(ground, ecol, shopcol)
        b.put(p.inputs["Emission Color"], ecol)
        b.put(p.inputs["Emission Strength"], b.m("ADD", estr, b.m("MULTIPLY", shop, lowrise)))
        haze(b, out, p.outputs[0])
        MAT["facade"] = m
        return m
    # night: some windows lit (warm and a few cool), shops lit on the ground floor
    # towers: windows lit in runs along a floor (an apartment), not a random mosaic of single panes
    rwt = b.white(b.combine(cv, b.m("FLOOR", b.m("DIVIDE", cu, 4.0)), b.m("MULTIPLY", s, 71.0)))
    litp = b.mixf(tall, b.m("LESS_THAN", rw2, 0.42), b.m("LESS_THAN", rwt, 0.30))
    lit = b.m("MULTIPLY", litp if TOD.get("night") else 0.0, gl)
    ecol = b.mix(b.m("GREATER_THAN", rw, 0.85), (1.0, 0.60, 0.30), (0.85, 0.88, 1.0))
    estr = b.m("MULTIPLY", b.m("MULTIPLY", lit, b.m("ADD", 0.5, rw)), b.mixf(tall, 0.42, 0.13) if TOD.get("night") else 0.0)
    shop = b.m("MULTIPLY", b.m("MULTIPLY", ground, b.m("LESS_THAN", rw, 0.45)), 0.9 * TOD.get("night", 0.0))
    b.put(p.inputs["Emission Color"], ecol)
    b.put(p.inputs["Emission Strength"], b.m("ADD", estr, b.m("MULTIPLY", shop, lowrise)))
    haze(b, out, p.outputs[0])
    MAT["facade"] = m
    return m


def simple_ext(name, color, rough=0.8, noise_scale=0.0, noise_amt=0.0, color2=None, spec=0.5, bump=0.0, emission=None, reach=None):
    m, nt, b, out = new_mat(name)
    col = color
    if noise_scale and color2 is not None:
        nz = b.noise(None, noise_scale, 6.0, 0.62)
        col = b.mix(b.m("MULTIPLY", nz.outputs["Fac"], noise_amt), color, color2)
    p = b.principled(Base_Color=col, Roughness=rough)
    b.put(p.inputs["Specular IOR Level"], spec)
    if bump:
        nz2 = b.noise(None, 3.0, 4.0, 0.6)
        b.put(p.inputs["Normal"], b.bump(nz2.outputs["Fac"], bump))
    if emission:
        b.put(p.inputs["Emission Color"], emission[0])
        b.put(p.inputs["Emission Strength"], emission[1])
    haze(b, out, p.outputs[0], reach)
    MAT[name] = m
    return m


def ground_material():
    """the ground between buildings: courtyards, gardens and paving, mixed at the scale of a Tel Aviv block"""
    m, nt, b, out = new_mat("ground")
    tc = b.n("ShaderNodeTexCoord")
    n1 = b.noise(tc.outputs["Object"], 0.035, 4.0, 0.6)
    n2 = b.noise(tc.outputs["Object"], 0.4, 3.0, 0.6)
    col = b.ramp(n1.outputs["Fac"], [(0.35, (0.19, 0.17, 0.145)), (0.5, (0.10, 0.11, 0.065)), (0.62, (0.065, 0.08, 0.04)), (0.75, (0.16, 0.145, 0.12))])
    col = b.mix(b.m("MULTIPLY", n2.outputs["Fac"], 0.5), col, (0.20, 0.19, 0.17))
    p = b.principled(Base_Color=col, Roughness=0.95)
    b.put(p.inputs["Specular IOR Level"], 0.1)
    haze(b, out, p.outputs[0])
    MAT["ground"] = m
    return m


def street_material():
    m, nt, b, out = new_mat("street")
    tc = b.n("ShaderNodeTexCoord")
    nz = b.noise(tc.outputs["Object"], 0.8, 5.0, 0.6)
    col = b.mix(b.m("MULTIPLY", nz.outputs["Fac"], 0.6), (0.075, 0.075, 0.078), (0.14, 0.135, 0.13))
    p = b.principled(Base_Color=col, Roughness=0.85)
    b.put(p.inputs["Specular IOR Level"], 0.12)
    if TOD.get("night"):
        b.put(p.inputs["Emission Color"], (1.0, 0.62, 0.30))
        b.put(p.inputs["Emission Strength"], 0.20)        # evening v2: the street lights (was 0.10)
    haze(b, out, p.outputs[0])
    MAT["street"] = m
    return m


def grass_material(name="grass", c1=(0.085, 0.13, 0.045), c2=(0.19, 0.22, 0.10)):
    m, nt, b, out = new_mat(name)
    tc = b.n("ShaderNodeTexCoord")
    nz = b.noise(tc.outputs["Object"], 0.25, 5.0, 0.62)
    col = b.mix(nz.outputs["Fac"], c1, c2)
    p = b.principled(Base_Color=col, Roughness=0.92)
    b.put(p.inputs["Specular IOR Level"], 0.1)
    haze(b, out, p.outputs[0])
    MAT[name] = m
    return m


def tree_material():
    """street and garden trees (ficus, plane, poinciana): clumped foliage with light passing through the leaves"""
    m, nt, b, out = new_mat("trees")
    tc = b.n("ShaderNodeTexCoord")
    ob = b.n("ShaderNodeObjectInfo")
    rid = b.attr("tseed").outputs["Fac"]
    vo = b.n("ShaderNodeTexVoronoi", feature="F1")
    b.put(vo.inputs["Vector"], tc.outputs["Object"])
    vo.inputs["Scale"].default_value = 2.2
    nz = b.noise(tc.outputs["Object"], 4.0, 4.0, 0.6)
    col = b.ramp(rid, [(0.0, (0.035, 0.065, 0.022)), (0.35, (0.055, 0.085, 0.030)), (0.7, (0.08, 0.095, 0.04)), (1.0, (0.10, 0.11, 0.055))])
    shade = b.m("ADD", 0.55, b.m("MULTIPLY", vo.outputs["Distance"], 0.9))
    colm = b.n("ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
    b.put(colm.inputs["Factor"], 1.0)
    b.put(colm.inputs[6], col)
    b.put(colm.inputs[7], b.combine(shade, shade, shade))
    p = b.principled(Base_Color=colm.outputs[2], Roughness=0.7)
    b.put(p.inputs["Specular IOR Level"], 0.3)
    b.put(p.inputs["Normal"], b.bump(b.m("ADD", vo.outputs["Distance"], b.m("MULTIPLY", nz.outputs["Fac"], 0.5)), 0.8, 0.4))
    tr = b.n("ShaderNodeBsdfTranslucent", {"Color": (0.10, 0.16, 0.03)})
    surf = b.mixs(0.18, p.outputs[0], tr.outputs[0])
    haze(b, out, surf)
    MAT["trees"] = m
    return m


def sea_material():
    """the Mediterranean from 118 m: a calm September sea, dark blue-green under the sky's reflection; long swells and
    small waves in the normal, so the sun draws its glitter path"""
    m, nt, b, out = new_mat("sea")
    tc = b.n("ShaderNodeTexCoord")
    ob = tc.outputs["Object"]
    mp = b.n("ShaderNodeMapping")
    b.put(mp.inputs["Vector"], ob)
    mp.inputs["Scale"].default_value = (1.0, 3.2, 1.0)        # swell crests run roughly along the coast (north-south)
    n1 = b.noise(mp.outputs[0], 0.08, 6.0, 0.62)
    n2 = b.noise(ob, 0.9, 8.0, 0.6)
    h = b.m("ADD", n1.outputs["Fac"], b.m("MULTIPLY", n2.outputs["Fac"], 0.35))
    nrm = b.bump(h, 0.9, 1.0)
    gl = b.n("ShaderNodeBsdfGlossy", {"Color": (0.78, 0.84, 0.88), "Roughness": 0.13, "Normal": nrm}, distribution="GGX")
    fr = b.n("ShaderNodeFresnel", {"IOR": 1.333, "Normal": nrm})
    body = b.n("ShaderNodeBsdfDiffuse", {"Color": (0.008, 0.028, 0.040)})
    surf = b.mixs(b.m("MULTIPLY", fr.outputs[0], 0.72), body.outputs[0], gl.outputs[0])
    haze(b, out, surf, 16000.0)
    MAT["sea"] = m
    return m


def tower_materials():
    """the three towers: white slabs and white aluminium (MYS: 'a repetitive system of floor slabs and white curtain
    walls'); insulated glass (Alum Eshet); the glass seen from outside is a dark mirror of the sky"""
    slab = simple_ext("tower_slab", (0.80, 0.80, 0.78), 0.55, 1.5, 0.25, (0.72, 0.72, 0.70), spec=0.4)
    alu = simple_ext("tower_alu", (0.84, 0.84, 0.83), 0.32, spec=0.6)
    m, nt, b, out = new_mat("tower_glass")
    p = b.principled(Base_Color=(0.030, 0.040, 0.046), Roughness=0.015, IOR=1.52)
    rw = b.white(b.n("ShaderNodeTexCoord").outputs["Object"])
    if TOD.get("night"):
        tc = b.n("ShaderNodeTexCoord")
        cell = b.m("FLOOR", b.m("MULTIPLY", b.sep(tc.outputs["Object"])[2], 0.25))
        rr = b.white(b.combine(cell, b.m("FLOOR", b.m("MULTIPLY", b.sep(tc.outputs["Object"])[0], 0.12)), 3.0))
        b.put(p.inputs["Emission Color"], (1.0, 0.72, 0.45))
        b.put(p.inputs["Emission Strength"], b.m("MULTIPLY", b.m("LESS_THAN", rr, 0.35), 0.9))
    haze(b, out, p.outputs[0])
    MAT["tower_glass"] = m
    rail = glass_ext("tower_rail")
    return slab, alu, m


def glass_ext(name):
    m, nt, b, out = new_mat(name)
    lp = b.n("ShaderNodeLightPath")
    tr = b.n("ShaderNodeBsdfTransparent", {"Color": (0.90, 0.95, 0.94)})
    gl = b.n("ShaderNodeBsdfGlossy", {"Roughness": 0.01})
    fr = b.n("ShaderNodeFresnel", {"IOR": 1.5})
    s = b.mixs(fr.outputs[0], tr.outputs[0], gl.outputs[0])
    s = b.mixs(lp.outputs["Is Shadow Ray"], s, tr.outputs[0])
    nt.links.new(s, out.inputs["Surface"])
    MAT[name] = m
    return m


# ============================================================================================ the city
def _poly_area(P):
    a = 0.0
    for i in range(len(P)):
        j = (i + 1) % len(P)
        a += P[i][0] * P[j][1] - P[j][0] * P[i][1]
    return a / 2


def build_blocks(eye, keep=lambda b: True):
    """every building: walls with a metre UV (along, up), a flat roof; one mesh; attributes bseed/btall per face"""
    fac = facade_material()
    verts, faces, uvs, seeds, talls = [], [], [], [], []
    clutter = []
    for bi, bl in enumerate(W["blocks"]):
        P = bl["P"]
        if len(P) < 3 or not keep(bl):
            continue
        h = max(bl["h"], 2.5)
        if _poly_area(P) < 0:
            P = P[::-1]
        s = rnd.random()
        tall = 1.0 if h >= 45 else 0.0
        base = len(verts)
        n = len(P)
        for (x, y) in P:
            verts.append((x, y, 0.0))
        for (x, y) in P:
            verts.append((x, y, h))
        acc = 0.0
        for i in range(n):
            j = (i + 1) % n
            L = math.dist(P[i], P[j])
            if L < 0.02:
                continue
            faces.append((base + i, base + j, base + n + j, base + n + i))
            uvs.append(((acc, 0.0), (acc + L, 0.0), (acc + L, h), (acc, h)))
            acc += L
            seeds.append(s)
            talls.append(tall)
        faces.append(tuple(base + n + i for i in range(n)))
        uvs.append(tuple((x / 10.0, y / 10.0) for (x, y) in P))
        seeds.append(s)
        talls.append(tall)
        # the roof's clutter (solar water heaters, air conditioners, a stair head) on the near low-rise
        dist = math.hypot(sum(p[0] for p in P) / n - eye.x, sum(p[1] for p in P) / n - eye.y)
        if dist < 1500 and 6 < h < 45 and abs(_poly_area(P)) > 60:
            clutter.append((P, h, s))
    me = bpy.data.meshes.new("city")
    me.from_pydata(verts, [], faces)
    me.update()
    uvl = me.uv_layers.new(name="fac")
    for poly, uvp in zip(me.polygons, uvs):
        for k, li in enumerate(poly.loop_indices):
            uvl.data[li].uv = uvp[k]
    a1 = me.attributes.new("bseed", "FLOAT", "FACE")
    a1.data.foreach_set("value", seeds)
    a2 = me.attributes.new("btall", "FLOAT", "FACE")
    a2.data.foreach_set("value", talls)
    me.materials.append(fac)
    ob = bpy.data.objects.new("city", me)
    link(ob)
    build_clutter(clutter)
    return ob


def _box(verts, faces, mats, cx, cy, z0, sx, sy, sz, rot, mi):
    c, s = math.cos(rot), math.sin(rot)
    b = len(verts)
    for dz in (0, sz):
        for (dx, dy) in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
            verts.append((cx + dx * c - dy * s, cy + dx * s + dy * c, z0 + dz))
    for f in ((0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)):
        faces.append(tuple(b + k for k in f))
        mats.append(mi)


def _inside(P, x, y):
    c = False
    j = len(P) - 1
    for i in range(len(P)):
        xi, yi = P[i]
        xj, yj = P[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi:
            c = not c
        j = i
    return c


def build_clutter(items):
    verts, faces, mats = [], [], []
    for P, h, s in items:
        r = random.Random(int(s * 1e6))
        xs = [p[0] for p in P]
        ys = [p[1] for p in P]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        # a stair / lift head
        for _ in range(8):
            cx, cy = r.uniform(x0, x1), r.uniform(y0, y1)
            if _inside(P, cx, cy):
                _box(verts, faces, mats, cx, cy, h, r.uniform(2.4, 3.6), r.uniform(2.4, 4.0), r.uniform(2.3, 2.8), r.uniform(0, 3.14), 0)
                break
        # solar water heaters: a white tank on a frame and a dark collector tilted to the south, in a row
        k = r.randint(1, 5)
        for _ in range(k * 3):
            cx, cy = r.uniform(x0, x1), r.uniform(y0, y1)
            if not _inside(P, cx, cy):
                continue
            _box(verts, faces, mats, cx, cy + 0.6, h, 1.3, 0.55, 1.35, 0.0, 1)
            # the collector: a thin slab, tilted (approximated by a low box stepped up to the north)
            _box(verts, faces, mats, cx, cy - 0.3, h + 0.2, 1.1, 1.8, 0.35, 0.0, 2)
            k -= 1
            if k <= 0:
                break
        # air conditioners
        for _ in range(r.randint(2, 7)):
            cx, cy = r.uniform(x0, x1), r.uniform(y0, y1)
            if _inside(P, cx, cy):
                _box(verts, faces, mats, cx, cy, h, 0.85, 0.35, 0.62, r.uniform(0, 3.14), 3)
    white = simple_ext("clutter_white", (0.78, 0.78, 0.76), 0.5)
    panel = simple_ext("clutter_panel", (0.035, 0.045, 0.06), 0.12, spec=0.9)
    head = simple_ext("clutter_head", (0.70, 0.68, 0.63), 0.85)
    ac = simple_ext("clutter_ac", (0.66, 0.66, 0.64), 0.6)
    me = bpy.data.meshes.new("roof_clutter")
    me.from_pydata(verts, [], faces)
    me.update()
    for mm in (head, white, panel, ac):
        me.materials.append(mm)
    me.polygons.foreach_set("material_index", mats)
    ob = bpy.data.objects.new("roof_clutter", me)
    link(ob)
    return ob


def build_ground(eye):
    """land (a 16 km square with the sea cut out), streets, greens, the square's park; the sea on its own curved surface"""
    gm = ground_material()
    sea_ring = max((w for w in W["water"] if w["outer"] and "הים" in w["name"]), key=lambda w: abs(_poly_area(w["P"])))
    land = bpy.data.meshes.new("land")
    bm = bmesh.new()
    S = 8000.0
    top = [bm.verts.new((x, y, 0.0)) for (x, y) in ((-S, -S), (S, -S), (S, S), (-S, S))]
    bot = [bm.verts.new((x, y, -6.0)) for (x, y) in ((-S, -S), (S, -S), (S, S), (-S, S))]
    bm.faces.new(top)
    bm.faces.new(bot[::-1])
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((bot[i], bot[j], top[j], top[i]))
    bm.to_mesh(land)
    bm.free()
    lob = bpy.data.objects.new("land", land)
    link(lob)
    P = sea_ring["P"]
    if _poly_area(P) < 0:
        P = P[::-1]
    sm = bpy.data.meshes.new("sea_cut")
    bm = bmesh.new()
    t = [bm.verts.new((x, y, 3.0)) for (x, y) in P]
    bo = [bm.verts.new((x, y, -12.0)) for (x, y) in P]
    bm.faces.new(t)
    bm.faces.new(bo[::-1])
    n = len(P)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((bo[i], bo[j], t[j], t[i]))
    bm.to_mesh(sm)
    bm.free()
    cut = bpy.data.objects.new("sea_cut", sm)
    link(cut)
    mod = lob.modifiers.new("cut", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.solver = "EXACT"
    mod.object = cut
    bpy.context.view_layer.objects.active = lob
    dg = bpy.context.evaluated_depsgraph_get()
    ev = lob.evaluated_get(dg)
    newme = bpy.data.meshes.new_from_object(ev)
    lob.modifiers.clear()
    lob.data = newme
    bpy.data.objects.remove(cut)
    # the boolean's mesh carries an empty material slot first: clear it, or the land renders with the default white
    lob.data.materials.clear()
    lob.data.materials.append(gm)
    for p in lob.data.polygons:
        p.material_index = 0
    # the breakwaters (the sea ring's small islands) as low rock
    rock = simple_ext("rock", (0.30, 0.29, 0.27), 0.9, 2.0, 0.5, (0.18, 0.17, 0.16))
    for w in W["water"]:
        if w["outer"] and "הים" in w["name"] and w is not sea_ring and len(w["P"]) >= 3:
            mesh_object("breakwater", [(x, y, 0.6) for (x, y) in w["P"]], [tuple(range(len(w["P"])))], [rock])
    # the sea: a polar grid around the eye, curved with the earth (radius 6371 km, refraction k 0.13), to 70 km
    sea = sea_material()
    R = 6371000.0 / (1 - 0.13)
    rings = [0.0] + [30.0 * (1.12 ** i) for i in range(70)]
    rings = [r for r in rings if r < 70000] + [70000.0]
    NA = 256
    verts, faces = [], []
    for ri, r in enumerate(rings):
        for a in range(NA):
            t = a / NA * 2 * math.pi
            verts.append((eye.x + r * math.cos(t), eye.y + r * math.sin(t), -0.25 - r * r / (2 * R)))
    for ri in range(len(rings) - 1):
        for a in range(NA):
            b2 = (a + 1) % NA
            faces.append((ri * NA + a, ri * NA + b2, (ri + 1) * NA + b2, (ri + 1) * NA + a))
    sob = mesh_object("sea", verts, faces, [sea])
    # the Yarkon and the park lake (not the sea)
    water2 = simple_ext("river", (0.035, 0.05, 0.042), 0.22, spec=0.5)
    for w in W["water"]:
        if w["outer"] and "הים" not in w["name"] and len(w["P"]) >= 3:
            mesh_object("water_" + w["name"], [(x, y, 0.05) for (x, y) in w["P"]], [tuple(range(len(w["P"])))], [water2])
    # streets
    st = street_material()
    verts, faces = [], []
    for s in W["streets"]:
        w = max(4.0, s["w"] * 0.92) * 0.5
        P = s["P"]
        for i in range(len(P) - 1):
            (x0, y0), (x1, y1) = P[i], P[i + 1]
            L = math.hypot(x1 - x0, y1 - y0)
            if L < 0.05:
                continue
            nx, ny = -(y1 - y0) / L * w, (x1 - x0) / L * w
            b0 = len(verts)
            verts += [(x0 + nx, y0 + ny, 0.03), (x0 - nx, y0 - ny, 0.03), (x1 - nx, y1 - ny, 0.03), (x1 + nx, y1 + ny, 0.03)]
            faces.append((b0, b0 + 1, b0 + 2, b0 + 3))
    mesh_object("streets", verts, faces, [st])
    # greens
    gr = grass_material()
    for g in W["greens"]:
        if len(g["P"]) >= 3:
            mesh_object("green", [(x, y, 0.06) for (x, y) in g["P"]], [tuple(range(len(g["P"])))], [gr])
    if W.get("park"):
        pk = grass_material("park", (0.10, 0.15, 0.05), (0.20, 0.24, 0.11))
        mesh_object("park", [(x, y, 0.08) for (x, y) in W["park"]], [tuple(range(len(W["park"])))], [pk])
    if W.get("pond"):
        mesh_object("pond", [(x, y, 0.1) for (x, y) in W["pond"]], [tuple(range(len(W["pond"])))], [water2])
    return lob


def build_cars(eye, reach=1400.0):
    """cars parked along both kerbs and a few in the lanes, every street within reach of the eye (an illustration)"""
    r = random.Random(77)
    cols = [("car_white", (0.58, 0.58, 0.57)), ("car_silver", (0.34, 0.35, 0.36)), ("car_grey", (0.16, 0.17, 0.18)),
            ("car_black", (0.02, 0.02, 0.022)), ("car_blue", (0.05, 0.10, 0.22)), ("car_red", (0.35, 0.04, 0.03)),
            ("car_sand", (0.55, 0.50, 0.42))]
    weights = [0.30, 0.22, 0.16, 0.16, 0.07, 0.04, 0.05]
    mats = []
    for nm, c in cols:
        m, nt, b, out = new_mat(nm)
        p = b.principled(Base_Color=c, Roughness=0.35)
        b.put(p.inputs["Coat Weight"], 0.25)
        b.put(p.inputs["Coat Roughness"], 0.12)
        b.put(p.inputs["Specular IOR Level"], 0.35)
        haze(b, out, p.outputs[0])
        mats.append(m)
    gm, nt, b, out = new_mat("car_glass")
    p = b.principled(Base_Color=(0.01, 0.012, 0.014), Roughness=0.05)
    haze(b, out, p.outputs[0])
    mats.append(gm)
    verts, faces, mi = [], [], []
    for st in W["streets"]:
        w = max(4.0, st["w"] * 0.92) * 0.5
        P = st["P"]
        for i in range(len(P) - 1):
            (x0, y0), (x1, y1) = P[i], P[i + 1]
            if min(math.hypot(x0 - eye.x, y0 - eye.y), math.hypot(x1 - eye.x, y1 - eye.y)) > reach:
                continue
            L = math.hypot(x1 - x0, y1 - y0)
            if L < 6:
                continue
            ux, uy = (x1 - x0) / L, (y1 - y0) / L
            nx, ny = -uy, ux
            rot = math.atan2(uy, ux)
            lanes = [(w - 1.3, 0.45), (-(w - 1.3), 0.45)] if w > 3.5 else [(0.0, 0.2)]
            if w > 6:
                lanes += [(w * 0.35, 0.10), (-w * 0.35, 0.10)]
            for off, prob in lanes:
                t = r.uniform(2, 6)
                while t < L - 3:
                    if r.random() < prob:
                        cx, cy = x0 + ux * t + nx * off, y0 + uy * t + ny * off
                        k = r.choices(range(7), weights)[0]
                        ln, wd = r.uniform(4.1, 4.8), r.uniform(1.75, 1.9)
                        _box(verts, faces, mi, cx, cy, 0.18, ln, wd, 0.82, rot, k)
                        _box(verts, faces, mi, cx - ux * 0.2, cy - uy * 0.2, 1.0, ln * 0.52, wd * 0.9, 0.48, rot, 7)
                    t += r.uniform(5.6, 7.5)
    me = bpy.data.meshes.new("cars")
    me.from_pydata(verts, [], faces)
    me.update()
    for m in mats:
        me.materials.append(m)
    me.polygons.foreach_set("material_index", mi)
    ob = bpy.data.objects.new("cars", me)
    link(ob)
    print("cars:", len(mi) // 12)
    return ob


def build_trees(eye):
    """the city's 2024 canopy: one crown per canopy footprint, at the world's size rule (trunk 2 + 0.35 r, crown r)"""
    tm = tree_material()
    verts, faces, seeds = [], [], []
    bm0 = bmesh.new()
    bmesh.ops.create_icosphere(bm0, subdivisions=2, radius=1.0)
    ico2 = [(v.co.x, v.co.y, v.co.z) for v in bm0.verts]
    ico2f = [tuple(v.index for v in f.verts) for f in bm0.faces]
    bm0.free()
    bm0 = bmesh.new()
    bmesh.ops.create_icosphere(bm0, subdivisions=1, radius=1.0)
    ico1 = [(v.co.x, v.co.y, v.co.z) for v in bm0.verts]
    ico1f = [tuple(v.index for v in f.verts) for f in bm0.faces]
    bm0.free()
    trunk_v, trunk_f = [], []
    for (x, y, r) in W["trees"]:
        r = max(1.2, r)
        d = math.hypot(x - eye.x, y - eye.y)
        if d > 3000:
            continue
        rr = random.Random(int(x * 13 + y * 7))
        V, F = (ico2, ico2f) if d < 700 else (ico1, ico1f)
        h0 = 2.0 + r * 0.35
        cz = h0 + r * 0.86
        b0 = len(verts)
        sd = rr.random()
        for (vx, vy, vz) in V:
            j = 1.0 + (rr.random() - 0.5) * 0.28
            verts.append((x + vx * r * j, y + vy * r * j, cz + vz * r * 0.82 * j))
        for f in F:
            faces.append(tuple(b0 + k for k in f))
            seeds.append(sd)
        if d < 900:
            tb = len(trunk_v)
            for (dx, dy) in ((-0.15, -0.15), (0.15, -0.15), (0.15, 0.15), (-0.15, 0.15)):
                trunk_v.append((x + dx, y + dy, 0.0))
            for (dx, dy) in ((-0.1, -0.1), (0.1, -0.1), (0.1, 0.1), (-0.1, 0.1)):
                trunk_v.append((x + dx, y + dy, cz))
            for f in ((0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
                trunk_f.append(tuple(tb + k for k in f))
    me = bpy.data.meshes.new("trees")
    me.from_pydata(verts, [], faces)
    me.update()
    a = me.attributes.new("tseed", "FLOAT", "FACE")
    a.data.foreach_set("value", seeds)
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(tm)
    link(bpy.data.objects.new("trees", me))
    bark = simple_ext("bark", (0.12, 0.10, 0.08), 0.9)
    mesh_object("trunks", trunk_v, trunk_f, [bark])


def build_towers(skip=None):
    """the three towers, floor by floor, turned 1.25 degrees a floor (world.js buildTowers): slabs, glass, the white
    aluminium fins every 1.5 m (Alum Eshet: 300 mm deep), and each flat side's balcony railing (an illustration: 4,000 m of
    balcony railings for 453 apartments is about 8.8 m of railing each). skip(key, floor, phi) -> True leaves that stretch
    of glass out (the example apartment builds its own)"""
    slab_m, alu_m, glass_m = tower_materials()
    rail_m = MAT["tower_rail"]
    m = W["model"]
    FH, SLAB_T, SLAB_OUT, NEXP = m["fh"], m["slab_t"], m["slab_out"], m.get("plate_n", 4.5)
    for key, t in W["towers"].items():
        N, half = t["floors"], t["side"] / 2
        gHalf = half - SLAB_OUT
        C = tower_xy(t)
        so = plate_outline(half, NEXP, 144)
        go = plate_outline(gHalf, NEXP, 144)
        M = len(go)
        glen = [0.0]
        for k in range(1, M + 1):
            a, bb = go[k - 1], go[k % M]
            glen.append(glen[-1] + math.dist(a, bb))
        per = glen[-1]
        sv, sf, gv, gf, fv, ff, rv, rf = [], [], [], [], [], [], [], []

        def W2(th, u, v, z):
            eu, ev = dirv(th), dirv(th + 90)
            return (C.x + u * eu.x + v * ev.x, C.y + u * eu.y + v * ev.y, z)

        for i in range(1, N + 2):
            th = plate_at(t, min(i, N))
            y0 = (i - 1) * FH
            y1 = y0 + SLAB_T
            b0 = len(sv)
            for (u, v) in so:
                sv.append(W2(th, u, v, y0))
            for (u, v) in so:
                sv.append(W2(th, u, v, y1))
            sf.append(tuple(b0 + k for k in range(M))[::-1])
            sf.append(tuple(b0 + M + k for k in range(M)))
            for k in range(M):
                k2 = (k + 1) % M
                sf.append((b0 + k, b0 + k2, b0 + M + k2, b0 + M + k))
            if i > N:
                continue
            g0, g1 = y1, y0 + FH
            for k in range(M):
                k2 = (k + 1) % M
                phi = math.atan2(go[k][1] + go[k2][1], go[k][0] + go[k2][0]) / DEG
                if skip and skip(key, i, phi):
                    continue
                b1 = len(gv)
                gv += [W2(th, go[k][0], go[k][1], g0), W2(th, go[k2][0], go[k2][1], g0), W2(th, go[k2][0], go[k2][1], g1), W2(th, go[k][0], go[k][1], g1)]
                gf.append((b1, b1 + 1, b1 + 2, b1 + 3))
            # fins: every 1.5 m of the glass line, radial, 0.30 m deep and 0.05 m thick; none in front of a balcony
            nfin = int(per / 1.5)
            for q in range(nfin):
                sq = (q + 0.5) * per / nfin
                k = max(0, min(M - 1, next((kk for kk in range(M) if glen[kk + 1] >= sq), M - 1)))
                f = (sq - glen[k]) / max(1e-6, glen[k + 1] - glen[k])
                a, bb = go[k], go[(k + 1) % M]
                pu, pv = a[0] + (bb[0] - a[0]) * f, a[1] + (bb[1] - a[1]) * f
                tu, tv = bb[0] - a[0], bb[1] - a[1]
                tl = math.hypot(tu, tv)
                tu, tv = tu / tl, tv / tl
                nu, nv = tv, -tu
                if nu * pu + nv * pv < 0:
                    nu, nv = -nu, -nv
                phi = math.atan2(pv, pu) / DEG
                side_phi = min(abs(((phi - c + 180) % 360) - 180) for c in (0, 90, 180, 270))
                on_balcony = side_phi < 16.3        # the flat middle of each side (8.8 m at the glass)
                if on_balcony or (skip and skip(key, i, phi)):
                    continue
                w2 = 0.025
                pts = []
                for (du, dv) in ((-tu * w2, -tv * w2), (tu * w2, tv * w2)):
                    for dep in (0.0, 0.30):
                        pts.append((pu + du + nu * dep, pv + dv + nv * dep))
                b2 = len(fv)
                for z in (g0, g1):
                    for (u, v) in (pts[0], pts[1], pts[3], pts[2]):
                        fv.append(W2(th, u, v, z))
                for fc in ((0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)):
                    ff.append(tuple(b2 + c for c in fc))
            # balcony railing on each flat side: 1.1 m of glass at the slab's edge
            for c in (0, 90, 180, 270):
                if skip and skip(key, i, c):
                    continue
                pts = []
                for a_ in range(-15, 16):
                    ph = (c + a_) * DEG
                    r_ = plate_radius(half, NEXP, ph) - 0.05
                    pts.append((r_ * math.cos(ph), r_ * math.sin(ph)))
                for q in range(len(pts) - 1):
                    b3 = len(rv)
                    rv += [W2(th, *pts[q], y1), W2(th, *pts[q + 1], y1), W2(th, *pts[q + 1], y1 + 1.1), W2(th, *pts[q], y1 + 1.1)]
                    rf.append((b3, b3 + 1, b3 + 2, b3 + 3))
        mesh_object("tower%s_slabs" % key, sv, sf, [slab_m])
        mesh_object("tower%s_glass" % key, gv, gf, [glass_m])
        mesh_object("tower%s_fins" % key, fv, ff, [alu_m])
        mesh_object("tower%s_rails" % key, rv, rf, [rail_m])
        # tower B: the published 157 m is reached by a roof crown (an illustration, as the world draws it)
        top = N * FH + SLAB_T
        if t["h"] > top + 1:
            th = plate_at(t, N)
            ring_o = plate_outline(gHalf - 1.2, NEXP, 96)
            cv = [W2(th, u, v, top) for (u, v) in ring_o] + [W2(th, u, v, t["h"]) for (u, v) in ring_o]
            n = len(ring_o)
            cf = [(k, (k + 1) % n, n + (k + 1) % n, n + k) for k in range(n)] + [tuple(n + k for k in range(n))]
            mesh_object("tower%s_crown" % key, cv, cf, [slab_m])
