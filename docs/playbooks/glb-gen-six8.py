# -*- coding: utf-8 -*-
# SIX-8 honest massing study (generic-model chip stays ON).
# Official basis: permit-request 2024 = 8 hotel podium floors + 10 residential
# floors above, 4 basements (not modeled); statutory height cap 80m; plot 1,956 sqm,
# tower coverage 70% (design plan 2020). Podium ellipse ~1,360 sqm, tower slimmer.
import json, math, struct

V, PRIMS = [], {}

def quad(mat, a, b, c, d):
    base = len(V)
    for p in (a, b, c, d):
        V.append(p)
    PRIMS.setdefault(mat, []).extend([base, base+1, base+2, base, base+2, base+3])

def tri(mat, a, b, c):
    base = len(V)
    for p in (a, b, c):
        V.append(p)
    PRIMS.setdefault(mat, []).extend([base, base+1, base+2])

SEG = 64
def ring(rx, rz, y):
    pts = []
    for i in range(SEG):
        a = 2*math.pi*i/SEG
        pts.append((rx*math.cos(a), y, rz*math.sin(a)))
    return pts

def band(mat, rx0, rz0, y0, rx1, rz1, y1):
    lo, hi = ring(rx0, rz0, y0), ring(rx1, rz1, y1)
    for i in range(SEG):
        j = (i+1) % SEG
        quad(mat, lo[i], lo[j], hi[j], hi[i])

def cap(mat, rx, rz, y):
    pts = ring(rx, rz, y)
    for i in range(SEG):
        tri(mat, pts[i], (0.0, y, 0.0), pts[(i+1) % SEG])

POD_FLOORS, POD_H = 8, 3.6      # hotel podium per 2024 licensing
RES_FLOORS, FLOOR_H = 10, 3.6   # residential tower per 2024 licensing
CROWN = 3.4                     # technical roof
POD_TOP = POD_FLOORS * POD_H    # 28.8
GLASS = FLOOR_H * 0.74
PRX, PRZ = 24.0, 18.0           # podium ellipse ~1,357 sqm (70% of 1,956)
RX0, RZ0 = 16.0, 12.5           # tower base
RX1, RZ1 = 15.0, 11.8           # gentle taper

# podium: stone frame + glass bands (boutique hotel base) - slim mullions, mostly glass
for f in range(POD_FLOORS):
    y0 = f * POD_H
    band('stone', PRX, PRZ, y0, PRX, PRZ, y0+0.35)
    band('glass', PRX*0.99, PRZ*0.99, y0+0.35, PRX*0.99, PRZ*0.99, y0+POD_H-0.2)
    band('stone', PRX, PRZ, y0+POD_H-0.2, PRX, PRZ, y0+POD_H)
cap('stone', PRX, PRZ, POD_TOP)   # podium roof = the floor-6 pool deck story

def radii(f):
    k = f / float(RES_FLOORS)
    ease = k*k*(3-2*k)
    return RX0 + (RX1-RX0)*ease, RZ0 + (RZ1-RZ0)*ease

for f in range(RES_FLOORS):
    y0 = POD_TOP + f*FLOOR_H
    rx0, rz0 = radii(f)
    rx1, rz1 = radii(f+1)
    band('glass', rx0, rz0, y0, rx0+(rx1-rx0)*0.74, rz0+(rz1-rz0)*0.74, y0+GLASS)
    band('span', rx0+(rx1-rx0)*0.74, rz0+(rz1-rz0)*0.74, y0+GLASS, rx1, rz1, y0+FLOOR_H)
    lip_lo = ring(rx1*1.012, rz1*1.012, y0+FLOOR_H-0.14)
    lip_hi = ring(rx1, rz1, y0+FLOOR_H)
    for i in range(SEG):
        j = (i+1) % SEG
        quad('span', lip_lo[i], lip_lo[j], lip_hi[j], lip_hi[i])

TOP = POD_TOP + RES_FLOORS*FLOOR_H   # 64.8
band('span', RX1, RZ1, TOP, RX1*0.94, RZ1*0.94, TOP+CROWN*0.55)
band('glass', RX1*0.92, RZ1*0.92, TOP+0.7, RX1*0.9, RZ1*0.9, TOP+CROWN*0.5)
band('span', RX1*0.94, RZ1*0.94, TOP+CROWN*0.55, RX1*0.7, RZ1*0.7, TOP+CROWN)
cap('span', RX1*0.7, RZ1*0.7, TOP+CROWN)

pos = b''.join(struct.pack('<3f', *p) for p in V)
prims = sorted(PRIMS.items())
buf = pos
views = [{'buffer': 0, 'byteOffset': 0, 'byteLength': len(pos), 'target': 34962}]
acc = [{'bufferView': 0, 'componentType': 5126, 'count': len(V), 'type': 'VEC3',
        'min': [min(p[i] for p in V) for i in range(3)],
        'max': [max(p[i] for p in V) for i in range(3)]}]
MAT = {
    'glass': {'name': 'glass', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.2, 0.29, 0.35, 1.0], 'metallicFactor': 0.9, 'roughnessFactor': 0.14}},
    'span':  {'name': 'spandrel', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.38, 0.42, 0.46, 1.0], 'metallicFactor': 0.6, 'roughnessFactor': 0.35}},
    'stone': {'name': 'stone', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.62, 0.57, 0.49, 1.0], 'metallicFactor': 0.08, 'roughnessFactor': 0.72}},
}
u16 = len(V) < 65500
ctype, fmt = (5123, '<H') if u16 else (5125, '<I')
materials, mat_idx, prim_json, off, tris = [], {}, [], len(buf), 0
for k, (mat, idx) in enumerate(prims):
    if mat not in mat_idx:
        mat_idx[mat] = len(materials); materials.append(MAT[mat])
    ib = b''.join(struct.pack(fmt, i) for i in idx)
    ib += b'\x00' * ((4 - len(ib) % 4) % 4)
    views.append({'buffer': 0, 'byteOffset': off, 'byteLength': len(ib), 'target': 34963})
    acc.append({'bufferView': 1+k, 'componentType': ctype, 'count': len(idx), 'type': 'SCALAR'})
    prim_json.append({'attributes': {'POSITION': 0}, 'indices': 1+k, 'material': mat_idx[mat]})
    buf += ib; off += len(ib); tris += len(idx)//3
gltf = {'asset': {'version': '2.0', 'generator': 'nadlan-parametric-six8'},
        'scene': 0, 'scenes': [{'nodes': [0]}], 'nodes': [{'mesh': 0, 'name': 'SIX8'}],
        'meshes': [{'primitives': prim_json, 'name': 'SIX8'}], 'materials': materials,
        'buffers': [{'byteLength': len(buf)}], 'bufferViews': views, 'accessors': acc}
js = json.dumps(gltf, separators=(',', ':')).encode('utf-8')
js += b' ' * ((4 - len(js) % 4) % 4)
buf += b'\x00' * ((4 - len(buf) % 4) % 4)
glb = (b'glTF' + struct.pack('<II', 2, 12+8+len(js)+8+len(buf))
       + struct.pack('<I', len(js)) + b'JSON' + js
       + struct.pack('<I', len(buf)) + b'BIN\x00' + buf)
import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'six8-herbert-samuel.glb')
open(out, 'wb').write(glb)
print('SIX-8 GLB: %d KB, %d verts (uint16=%s), %d triangles, height %.1fm' % (
    len(glb)//1024, len(V), u16, tris, TOP+CROWN))
