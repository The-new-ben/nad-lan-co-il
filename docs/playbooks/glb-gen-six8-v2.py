# -*- coding: utf-8 -*-
# SIX-8 massing v2 (generic-model chip stays ON) - after the PUBLIC Moshe Tzur
# renders on six-8.avivcomp.co.il (viewed 2026-08-20): rectangular corner slab,
# long N-S frontage to the sea; WEST face = stacked full-width balcony plates
# with glass balustrades wrapping the SW corner; other faces = vertical panel
# mosaic (glass / champagne / white); white pergola crown; 8-floor hotel podium
# (2024 licensing) with stone+glass bands, champagne fins and a rooftop pool
# deck; 10 residential floors above; 4 basements not modeled. Height ~68m
# under the 80m statutory cap. Axes: -Z = north (engine/beam convention),
# so the sea face is -X (west) and the long dimension runs along Z.
import json, math, os, struct

V, PRIMS = [], {}

def quad(mat, a, b, c, d):
    base = len(V)
    for p in (a, b, c, d):
        V.append(p)
    PRIMS.setdefault(mat, []).extend([base, base + 1, base + 2, base, base + 2, base + 3])

def box(mat, x0, y0, z0, x1, y1, z1):
    quad(mat, (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0))
    quad(mat, (x1, y0, z1), (x0, y0, z1), (x0, y1, z1), (x1, y1, z1))
    quad(mat, (x0, y0, z1), (x0, y0, z0), (x0, y1, z0), (x0, y1, z1))
    quad(mat, (x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0))
    quad(mat, (x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1))
    quad(mat, (x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0))

# ---- program (licensing 2024) ----
POD_F, POD_H = 8, 3.6
RES_F, FLOOR_H = 10, 3.6
POD_TOP = POD_F * POD_H            # 28.8
TWR_TOP = POD_TOP + RES_F * FLOOR_H  # 64.8
# plans: podium ~44x31m (~1,364 sqm = 70% of 1,956), tower slab 34(NS) x 22(EW)
PX, PZ = 15.5, 22.0                # podium half extents (x: E-W, z: N-S)
TX, TZ = 11.0, 17.0                # tower half extents
BAL_D = 2.4                        # balcony plate depth to the west
BAL_T = 0.35                       # plate thickness
RAIL_H = 1.05

# ---- podium: stone frame, glass bands, champagne fins, retail ground ----
for f in range(POD_F):
    y0 = f * POD_H
    if f == 0:
        # double-height feel: full glass with stone piers
        box('stone', -PX, y0, -PZ, PX, y0 + 0.25, PZ)
        for zp in range(-3, 4):
            z = zp * PZ / 3.5
            box('stone', -PX - 0.05, y0, z - 0.35, PX + 0.05, y0 + POD_H, z + 0.35)
        box('glass', -PX + 0.02, y0 + 0.25, -PZ + 0.02, PX - 0.02, y0 + POD_H, PZ - 0.02)
    else:
        # stone-dominant hotel floors: warm base, slim ribbon glazing
        box('stone', -PX, y0, -PZ, PX, y0 + 2.05, PZ)
        box('glass', -PX + 0.01, y0 + 2.05, -PZ + 0.01, PX - 0.01, y0 + POD_H - 0.2, PZ - 0.01)
        box('stone', -PX, y0 + POD_H - 0.2, -PZ, PX, y0 + POD_H, PZ)
# champagne fins on the sea-facing podium edge
zf = -PZ + 1.6
while zf < PZ - 1.2:
    box('champ', -PX - 0.45, 0.25, zf, -PX + 0.05, POD_TOP - 0.2, zf + 0.22)
    zf += 3.2
# podium roof deck + the shared rooftop pool, clear of the tower footprint
# (south deck strip - the sixth-floor shared pool story from the developer site)
box('stone', -PX, POD_TOP, -PZ, PX, POD_TOP + 0.35, PZ)
box('white', -8.6, POD_TOP + 0.35, 17.3, 8.6, POD_TOP + 0.44, 21.4)
box('pool', -8.0, POD_TOP + 0.36, 17.7, 8.0, POD_TOP + 0.58, 21.0)

# ---- tower core volume (recessed glass west wall behind balconies) ----
# east / north / south faces: vertical panel mosaic; west: curtain glass
def mosaic_face(face, y0, y1, fidx):
    # face: 'e' (+X plane), 'n' (-Z plane), 's' (+Z plane)
    length = (2 * TZ) if face == 'e' else (2 * TX)
    n = max(6, int(length / 2.6))
    step = length / n
    for i in range(n):
        r = (fidx * 7 + i * 13 + (3 if face == 'n' else 0) + (5 if face == 's' else 0)) % 10
        mat = 'glass' if r < 6 else ('champ' if r < 8 else 'white')
        a, b = i * step, (i + 1) * step - 0.06
        if face == 'e':
            quad(mat, (TX, y0, -TZ + a), (TX, y0, -TZ + b), (TX, y1, -TZ + b), (TX, y1, -TZ + a))
        elif face == 'n':
            quad(mat, (-TX + a, y0, -TZ), (-TX + b, y0, -TZ), (-TX + b, y1, -TZ), (-TX + a, y1, -TZ))
        else:
            quad(mat, (-TX + a, y0, TZ), (-TX + b, y0, TZ), (-TX + b, y1, TZ), (-TX + a, y1, TZ))

for f in range(RES_F):
    y0 = POD_TOP + f * FLOOR_H
    y1 = y0 + FLOOR_H
    mosaic_face('e', y0 + 0.12, y1 - 0.12, f)
    mosaic_face('n', y0 + 0.12, y1 - 0.12, f)
    mosaic_face('s', y0 + 0.12, y1 - 0.12, f)
    # slim white floor lines keep the slab reading
    box('white', -TX, y1 - 0.12, -TZ, TX, y1, TZ)
    # west curtain wall, recessed 1.2m so the terraces read as real depth,
    # punctuated by slim white mullions instead of one glass cliff
    wx = -TX + 1.2
    quad('glass', (wx, y0, TZ), (wx, y0, -TZ), (wx, y1, -TZ), (wx, y1, TZ))
    zm = -TZ + 2.0
    while zm < TZ - 1.0:
        box('white', wx - 0.06, y0, zm - 0.09, wx + 0.1, y1 - 0.12, zm + 0.09)
        zm += 4.4
    # terrace side cheeks close the recess at both ends
    quad('white', (wx, y0, -TZ), (-TX, y0, -TZ), (-TX, y1, -TZ), (wx, y1, -TZ))
    quad('white', (-TX, y0, TZ), (wx, y0, TZ), (wx, y1, TZ), (-TX, y1, TZ))
    # balcony plate: full west width, wrapping the SW corner 8m eastward
    by = y0
    box('white', -TX - BAL_D, by, -TZ + 0.8, -TX + 0.05, by + BAL_T, TZ + 0.0)
    box('white', -TX - BAL_D, by, TZ - 0.05, -TX + 8.0, by + BAL_T, TZ + BAL_D * 0.55)
    # glass balustrades + slim white handrails on the plate edges
    quad('rail', (-TX - BAL_D, by + BAL_T, -TZ + 0.8), (-TX - BAL_D, by + BAL_T, TZ + BAL_D * 0.55),
                 (-TX - BAL_D, by + BAL_T + RAIL_H, TZ + BAL_D * 0.55), (-TX - BAL_D, by + BAL_T + RAIL_H, -TZ + 0.8))
    quad('rail', (-TX - BAL_D, by + BAL_T, TZ + BAL_D * 0.55), (-TX + 8.0, by + BAL_T, TZ + BAL_D * 0.55),
                 (-TX + 8.0, by + BAL_T + RAIL_H, TZ + BAL_D * 0.55), (-TX - BAL_D, by + BAL_T + RAIL_H, TZ + BAL_D * 0.55))
    box('white', -TX - BAL_D - 0.05, by + BAL_T + RAIL_H, -TZ + 0.8, -TX - BAL_D + 0.05, by + BAL_T + RAIL_H + 0.09, TZ + BAL_D * 0.55)
    box('white', -TX - BAL_D - 0.05, by + BAL_T + RAIL_H, TZ + BAL_D * 0.55 - 0.05, -TX + 8.0, by + BAL_T + RAIL_H + 0.09, TZ + BAL_D * 0.55 + 0.05)

# tower roof
box('white', -TX, TWR_TOP, -TZ, TX, TWR_TOP + 0.3, TZ)

# ---- roof: low parapet all around + partial pergola lounge on the south half ----
PP = 0.95
box('white', -TX, TWR_TOP + 0.3, -TZ, TX, TWR_TOP + 0.3 + PP, -TZ + 0.15)
box('white', -TX, TWR_TOP + 0.3, TZ - 0.15, TX, TWR_TOP + 0.3 + PP, TZ)
box('white', -TX, TWR_TOP + 0.3, -TZ, -TX + 0.15, TWR_TOP + 0.3 + PP, TZ)
box('white', TX - 0.15, TWR_TOP + 0.3, -TZ, TX, TWR_TOP + 0.3 + PP, TZ)
PGH = 2.2
PGZ0 = 3.0
for (px, pz) in ((-TX + 1.0, PGZ0 + 0.4), (TX - 1.0, PGZ0 + 0.4), (-TX + 1.0, TZ - 1.0), (TX - 1.0, TZ - 1.0)):
    box('white', px - 0.14, TWR_TOP + 0.3, pz - 0.14, px + 0.14, TWR_TOP + 0.3 + PGH, pz + 0.14)
box('white', -TX + 0.7, TWR_TOP + 0.3 + PGH, PGZ0, TX - 0.7, TWR_TOP + 0.3 + PGH + 0.3, PGZ0 + 0.35)
box('white', -TX + 0.7, TWR_TOP + 0.3 + PGH, TZ - 1.1, TX - 0.7, TWR_TOP + 0.3 + PGH + 0.3, TZ - 0.75)
zs = PGZ0 + 1.2
while zs < TZ - 1.3:
    box('white', -TX + 0.8, TWR_TOP + 0.3 + PGH + 0.04, zs, TX - 0.8, TWR_TOP + 0.3 + PGH + 0.24, zs + 0.26)
    zs += 1.9

# ---- pack glb ----
MAT = {
    'glass': {'name': 'glass', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.36, 0.46, 0.52, 1.0], 'metallicFactor': 0.88, 'roughnessFactor': 0.16}},
    'white': {'name': 'white-metal', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.91, 0.895, 0.865, 1.0], 'metallicFactor': 0.25, 'roughnessFactor': 0.42}},
    'champ': {'name': 'champagne', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.76, 0.66, 0.47, 1.0], 'metallicFactor': 0.75, 'roughnessFactor': 0.3}},
    'stone': {'name': 'stone', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.63, 0.585, 0.51, 1.0], 'metallicFactor': 0.06, 'roughnessFactor': 0.7}},
    'rail':  {'name': 'balustrade', 'doubleSided': True, 'alphaMode': 'BLEND', 'pbrMetallicRoughness': {'baseColorFactor': [0.62, 0.72, 0.76, 0.4], 'metallicFactor': 0.9, 'roughnessFactor': 0.08}},
    'pool':  {'name': 'pool', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.3, 0.62, 0.64, 1.0], 'metallicFactor': 0.15, 'roughnessFactor': 0.25}},
}
pos = b''.join(struct.pack('<3f', *p) for p in V)
prims = sorted(PRIMS.items())
buf = pos
views = [{'buffer': 0, 'byteOffset': 0, 'byteLength': len(pos), 'target': 34962}]
acc = [{'bufferView': 0, 'componentType': 5126, 'count': len(V), 'type': 'VEC3',
        'min': [min(p[i] for p in V) for i in range(3)],
        'max': [max(p[i] for p in V) for i in range(3)]}]
u16 = len(V) < 65500
ctype, fmt = (5123, '<H') if u16 else (5125, '<I')
materials, mat_idx, prim_json, off, tris = [], {}, [], len(buf), 0
for k, (mat, idx) in enumerate(prims):
    if mat not in mat_idx:
        mat_idx[mat] = len(materials); materials.append(MAT[mat])
    ib = b''.join(struct.pack(fmt, i) for i in idx)
    ib += b'\x00' * ((4 - len(ib) % 4) % 4)
    views.append({'buffer': 0, 'byteOffset': off, 'byteLength': len(ib), 'target': 34963})
    acc.append({'bufferView': 1 + k, 'componentType': ctype, 'count': len(idx), 'type': 'SCALAR'})
    prim_json.append({'attributes': {'POSITION': 0}, 'indices': 1 + k, 'material': mat_idx[mat]})
    buf += ib; off += len(ib); tris += len(idx) // 3
gltf = {'asset': {'version': '2.0', 'generator': 'nadlan-parametric-six8-v2'},
        'scene': 0, 'scenes': [{'nodes': [0]}], 'nodes': [{'mesh': 0, 'name': 'SIX8v2'}],
        'meshes': [{'primitives': prim_json, 'name': 'SIX8v2'}], 'materials': materials,
        'buffers': [{'byteLength': len(buf)}], 'bufferViews': views, 'accessors': acc}
js = json.dumps(gltf, separators=(',', ':')).encode('utf-8')
js += b' ' * ((4 - len(js) % 4) % 4)
buf += b'\x00' * ((4 - len(buf) % 4) % 4)
glb = (b'glTF' + struct.pack('<II', 2, 12 + 8 + len(js) + 8 + len(buf))
       + struct.pack('<I', len(js)) + b'JSON' + js
       + struct.pack('<I', len(buf)) + b'BIN\x00' + buf)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'six8-herbert-samuel-massing-v2.glb')
open(out, 'wb').write(glb)
print('SIX-8 v2 GLB: %d KB, %d verts (uint16=%s), %d tris, height %.1fm' % (
    len(glb) // 1024, len(V), u16, tris, TWR_TOP + PGH + 0.35))
