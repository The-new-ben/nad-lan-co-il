"""Optimise raw Meshy GLBs for the apartment designer (HAD-704/705) and render a contact sheet.

Run with Blender in background mode:

  blender -b --factory-startup --python scripts/interior/designer_models_optimize.py -- \
      optimize <raw_dir> <out_dir> [--rot sofa3=180,desk120=90] [--only sofa3,bed160]
  blender -b --factory-startup --python scripts/interior/designer_models_optimize.py -- \
      render <out_dir> <png_dir>

optimize: for every <id>.glb in raw_dir whose id is in SPECS: import, join meshes, apply transforms,
optional Z rotation (so the FRONT faces Blender -Y = glTF +Z), origin at footprint centre on the floor,
uniform scale to the real size (the axis with the largest real dimension is matched exactly, the other
axes report their remaining mismatch), decimate, shrink textures, export GLB (WebP, no Draco).
Writes <out_dir>/models.json and prints one JSON line per model.

render: 3/4 front view, neutral light, 512 px PNG per GLB in out_dir.
"""
import bpy, bmesh, sys, os, json, math
from mathutils import Vector, Matrix

# id: (w, d, h) cm, small piece?
SPECS = {
    'sofa3': (240, 95, 82, False), 'armchair': (85, 85, 80, False), 'dining6': (180, 90, 75, False),
    'dining-chair': (45, 52, 82, True), 'bed160': (160, 200, 100, False), 'bed120': (120, 200, 90, False),
    'wardrobe200': (200, 60, 240, False), 'tv180': (180, 40, 45, False), 'desk120': (120, 60, 75, False),
    'office-chair': (60, 60, 95, True), 'coffee-table': (110, 60, 40, True), 'floor-lamp': (40, 40, 160, True),
    'plant': (45, 45, 140, True), 'bedside': (45, 40, 50, True),
}


def args():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    opts = {}
    pos = []
    i = 0
    while i < len(a):
        if a[i].startswith('--'):
            opts[a[i][2:]] = a[i + 1]
            i += 2
        else:
            pos.append(a[i])
            i += 1
    return pos, opts


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def mesh_objects():
    return [o for o in bpy.context.scene.objects if o.type == 'MESH']


def world_bbox(objs):
    lo = Vector((1e9, 1e9, 1e9)); hi = Vector((-1e9, -1e9, -1e9))
    for o in objs:
        for v in o.data.vertices:
            p = o.matrix_world @ v.co
            lo = Vector(map(min, lo, p)); hi = Vector(map(max, hi, p))
    return lo, hi


def tri_count(objs):
    n = 0
    for o in objs:
        for p in o.data.polygons:
            n += len(p.vertices) - 2
    return n


def optimize_one(src, dst, mid, rot_deg):
    w, d, h, small = SPECS[mid]
    reset()
    bpy.ops.import_scene.gltf(filepath=src)
    objs = mesh_objects()
    # drop empties/parents after baking their transforms into meshes
    for o in objs:
        mw = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = mw
    for o in list(bpy.context.scene.objects):
        if o.type != 'MESH':
            bpy.data.objects.remove(o, do_unlink=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    if rot_deg:
        ob.data.transform(Matrix.Rotation(math.radians(rot_deg), 4, 'Z'))
    # origin: centre of footprint, floor at z=0
    lo, hi = world_bbox([ob])
    ob.data.transform(Matrix.Translation(Vector(((lo.x + hi.x) / -2, (lo.y + hi.y) / -2, -lo.z))))
    lo, hi = world_bbox([ob])
    size = hi - lo  # metres, x=width y=depth z=height
    target = Vector((w / 100, d / 100, h / 100))
    axis = max(range(3), key=lambda k: target[k])
    s = target[axis] / size[axis]
    ob.data.transform(Matrix.Scale(s, 4))
    lo, hi = world_bbox([ob])
    size = hi - lo
    # decimate
    limit = 6000 if small else 12000
    tris_before = tri_count([ob])
    if tris_before > limit:
        m = ob.modifiers.new('dec', 'DECIMATE')
        m.ratio = (limit / tris_before) * 0.98
        m.use_collapse_triangulate = True
        bpy.ops.object.modifier_apply(modifier=m.name)
    # triangulate for honest counts
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bm.to_mesh(ob.data); bm.free()
    tris = tri_count([ob])
    # textures
    tmax = 512 if small else 1024
    for img in bpy.data.images:
        if img.size[0] > tmax or img.size[1] > tmax:
            img.scale(tmax, tmax)
    ob.name = mid
    ob.data.name = mid
    fmt = 'WEBP'

    def export():
        nonlocal fmt
        try:
            bpy.ops.export_scene.gltf(filepath=dst, export_format='GLB', export_image_format=fmt,
                                      export_image_quality=72,
                                      export_draco_mesh_compression_enable=False, export_apply=True,
                                      export_yup=True, export_animations=False, export_cameras=False,
                                      export_lights=False)
        except TypeError:
            fmt = 'JPEG'
            bpy.ops.export_scene.gltf(filepath=dst, export_format='GLB', export_image_format='JPEG',
                                      export_draco_mesh_compression_enable=False, export_apply=True,
                                      export_yup=True)

    export()
    # size budget: geometry dominates (~50 B per triangle after UV splits), so decimate further if needed
    budget = 440_000
    for _ in range(4):
        sz = os.path.getsize(dst)
        if sz <= budget:
            break
        m = ob.modifiers.new('dec2', 'DECIMATE')
        m.ratio = max(0.5, min(0.9, (budget / sz) * 0.85))
        m.use_collapse_triangulate = True
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.modifier_apply(modifier=m.name)
        export()
    tris = tri_count([ob])
    lo, hi = world_bbox([ob])
    size = hi - lo
    cm = [round(v * 100, 1) for v in size]
    return {
        'id': mid, 'file': os.path.basename(dst), 'w': cm[0], 'd': cm[1], 'h': cm[2],
        'triangles': tris, 'bytes': os.path.getsize(dst), 'front': '+z', 'source': 'meshy text-to-3d',
        'made': '2026-11-11',
        '_target': [w, d, h], '_mismatch_pct': [round((cm[k] / [w, d, h][k] - 1) * 100, 1) for k in range(3)],
        '_tris_raw': tris_before, '_tex': fmt, '_rot': rot_deg,
    }


def cmd_optimize(raw, out, opts):
    os.makedirs(out, exist_ok=True)
    rots = {}
    for kv in filter(None, opts.get('rot', '').split(',')):
        k, v = kv.split('=')
        rots[k] = float(v)
    only = set(filter(None, opts.get('only', '').split(',')))
    jpath = os.path.join(out, 'models.json')
    rows = {r['id']: r for r in json.load(open(jpath, encoding='utf-8'))} if os.path.exists(jpath) else {}
    meta = {}
    mpath = os.path.join(raw, '_optimize-meta.json')
    if os.path.exists(mpath):
        meta = json.load(open(mpath, encoding='utf-8'))
    for mid in SPECS:
        src = os.path.join(raw, mid + '.glb')
        if not os.path.exists(src) or (only and mid not in only):
            continue
        r = optimize_one(src, os.path.join(out, mid + '.glb'), mid, rots.get(mid, 0))
        meta[mid] = {k: r.pop(k) for k in [k for k in r if k.startswith('_')]}
        rows[mid] = r
        print('MODEL', json.dumps({**r, **meta[mid]}))
    ordered = [rows[k] for k in SPECS if k in rows]
    with open(jpath, 'w', encoding='utf-8') as f:
        json.dump(ordered, f, indent=1)
    with open(mpath, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=1)


def cmd_render(out, pngdir):
    os.makedirs(pngdir, exist_ok=True)
    for mid in SPECS:
        src = os.path.join(out, mid + '.glb')
        if not os.path.exists(src):
            continue
        reset()
        sc = bpy.context.scene
        bpy.ops.import_scene.gltf(filepath=src)
        objs = mesh_objects()
        lo, hi = world_bbox(objs)
        c = (lo + hi) / 2
        r = (hi - lo).length / 2
        # floor
        bpy.ops.mesh.primitive_plane_add(size=max(6, r * 8), location=(c.x, c.y, 0))
        fl = bpy.context.active_object
        fm = bpy.data.materials.new('floor'); fm.use_nodes = True
        fm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.82, 0.82, 0.83, 1)
        fl.data.materials.append(fm)
        # world + light
        wd = bpy.data.worlds.new('w'); sc.world = wd; wd.use_nodes = True
        bg = wd.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.85, 0.86, 0.88, 1); bg.inputs[1].default_value = 0.9
        sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 2.5; sun.angle = math.radians(25)
        so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so)
        so.rotation_euler = (math.radians(50), 0, math.radians(30))
        # camera: 3/4 from front-right (front = Blender -Y)
        cam = bpy.data.cameras.new('cam'); cam.lens = 50
        co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
        dirv = Vector((0.55, -1.0, 0.55)).normalized()
        fov = 2 * math.atan(18 / cam.lens)
        dist = r / math.sin(fov / 2) * 1.08
        co.location = c + dirv * dist
        co.rotation_euler = (-dirv).to_track_quat('-Z', 'Y').to_euler()
        cam.clip_end = dist * 10
        sc.render.resolution_x = sc.render.resolution_y = 512
        sc.render.film_transparent = False
        try:
            sc.render.engine = 'BLENDER_EEVEE'
        except TypeError:
            sc.render.engine = 'BLENDER_EEVEE_NEXT'
        sc.view_settings.view_transform = 'Standard' if 'Standard' in [i.identifier for i in sc.view_settings.bl_rna.properties['view_transform'].enum_items] else sc.view_settings.view_transform
        sc.render.filepath = os.path.join(pngdir, mid + '.png')
        try:
            bpy.ops.render.render(write_still=True)
        except Exception as e:  # Eevee may need a GPU context; fall back to Cycles CPU
            print('eevee failed', e)
            sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.cycles.device = 'CPU'
            bpy.ops.render.render(write_still=True)
        print('RENDER', mid)


pos, opts = args()
pos = pos[:1] + [os.path.abspath(p) for p in pos[1:]]  # Blender resolves bare relative render paths oddly
if pos and pos[0] == 'optimize':
    cmd_optimize(pos[1], pos[2], opts)
elif pos and pos[0] == 'render':
    cmd_render(pos[1], pos[2])
else:
    print(__doc__)
