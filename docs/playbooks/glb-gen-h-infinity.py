# -*- coding: utf-8 -*-
# ToHa2 massing v2 - same geometry family, 3x lighter for mobile:
#  - SEG 96 -> 64 (5.6 deg facets; the metallic facade reads as panelized anyway)
#  - NORMAL accessor dropped: verts are unshared per quad, so client-computed
#    flat normals are byte-identical to what we stored (glTF spec behaviour)
#  - uint16 indices (guarded: falls back to uint32 if verts >= 65500)
# Honest massing study, generic-model chip stays on.
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
def ring(rx, rz, y, twist=0.0):
    pts = []
    for i in range(SEG):
        a = 2*math.pi*i/SEG + twist
        pts.append((rx*math.cos(a), y, rz*math.sin(a)))
    return pts

def band(mat, rx0, rz0, y0, rx1, rz1, y1, tw0=0.0, tw1=0.0):
    lo, hi = ring(rx0, rz0, y0, tw0), ring(rx1, rz1, y1, tw1)
    for i in range(SEG):
        j = (i+1) % SEG
        quad(mat, lo[i], lo[j], hi[j], hi[i])

def cap(mat, rx, rz, y, tw=0.0):
    pts = ring(rx, rz, y, tw)
    for i in range(SEG):
        tri(mat, pts[i], (0.0, y, 0.0), pts[(i+1) % SEG])

H_TOTAL = 187.0
FLOORS = 52
POD_FLOORS, POD_H = 2, 5.0
POD_TOP = POD_FLOORS * POD_H
CROWN = 6.0
FLOOR_H = (H_TOTAL - POD_TOP - CROWN) / FLOORS
GLASS = FLOOR_H * 0.74
RX0, RZ0 = 15.5, 12.5
RX1, RZ1 = 14.0, 11.5
SKY_A, SKY_B = -9, -9

for f in range(POD_FLOORS):
    y0 = f * POD_H
    band('stone', RX0*1.18, RZ0*1.18, y0, RX0*1.18, RZ0*1.18, y0+0.9)
    band('glass', RX0*1.16, RZ0*1.16, y0+0.9, RX0*1.16, RZ0*1.16, y0+POD_H-0.5)
    band('stone', RX0*1.18, RZ0*1.18, y0+POD_H-0.5, RX0*1.18, RZ0*1.18, y0+POD_H)
cap('stone', RX0*1.18, RZ0*1.18, POD_TOP)

def radii(f):
    k = f / float(FLOORS)
    ease = k*k*(3-2*k)
    rx = RX0 + (RX1-RX0)*ease
    rz = RZ0 + (RZ1-RZ0)*ease
    if SKY_A <= f <= SKY_B:
        rx, rz = rx*0.93, rz*0.93
    return rx, rz

TWIST = math.radians(0.0)
for f in range(FLOORS):
    y0 = POD_TOP + f*FLOOR_H
    rx0, rz0 = radii(f)
    rx1, rz1 = radii(f+1)
    t0, t1 = TWIST*f/FLOORS, TWIST*(f+1)/FLOORS
    band('glass', rx0, rz0, y0, rx0+(rx1-rx0)*0.74, rz0+(rz1-rz0)*0.74, y0+GLASS, t0, t0+(t1-t0)*0.74)
    band('span', rx0+(rx1-rx0)*0.74, rz0+(rz1-rz0)*0.74, y0+GLASS, rx1, rz1, y0+FLOOR_H, t0+(t1-t0)*0.74, t1)
    lip_lo = ring(rx1*1.012, rz1*1.012, y0+FLOOR_H-0.16, t1)
    lip_hi = ring(rx1, rz1, y0+FLOOR_H, t1)
    for i in range(SEG):
        j = (i+1) % SEG
        quad('span', lip_lo[i], lip_lo[j], lip_hi[j], lip_hi[i])

TOP = POD_TOP + FLOORS*FLOOR_H
band('span', RX1, RZ1, TOP, RX1*0.95, RZ1*0.95, TOP+CROWN*0.55, TWIST, TWIST)
band('glass', RX1*0.93, RZ1*0.93, TOP+0.8, RX1*0.9, RZ1*0.9, TOP+CROWN*0.5, TWIST, TWIST)
band('span', RX1*0.95, RZ1*0.95, TOP+CROWN*0.55, RX1*0.72, RZ1*0.72, TOP+CROWN, TWIST, TWIST)
cap('span', RX1*0.72, RZ1*0.72, TOP+CROWN, TWIST)


# boutique building: 7 floors, offset east of the tower
BX, BZ, BOFF = 9.0, 7.0, 24.0
def bring(rx, rz, y):
    pts = []
    for i in range(SEG):
        a = 2*math.pi*i/SEG
        pts.append((BOFF + rx*math.cos(a), y, rz*math.sin(a)))
    return pts
def bband(mat, y0, y1):
    lo, hi = bring(BX, BZ, y0), bring(BX, BZ, y1)
    for i in range(SEG):
        j = (i+1) % SEG
        quad(mat, lo[i], lo[j], hi[j], hi[i])
BF_H = 3.3
for f in range(7):
    y0 = f * BF_H
    bband('glass', y0, y0 + BF_H*0.75)
    bband('span',  y0 + BF_H*0.75, y0 + BF_H)
bpts = bring(BX, BZ, 7*BF_H)
for i in range(SEG):
    tri('span', bpts[i], (BOFF, 7*BF_H, 0.0), bpts[(i+1) % SEG])

pos = b''.join(struct.pack('<3f', *p) for p in V)
prims = sorted(PRIMS.items())
buf = pos
views = [{'buffer': 0, 'byteOffset': 0, 'byteLength': len(pos), 'target': 34962}]
acc = [{'bufferView': 0, 'componentType': 5126, 'count': len(V), 'type': 'VEC3',
        'min': [min(p[i] for p in V) for i in range(3)],
        'max': [max(p[i] for p in V) for i in range(3)]}]
MAT = {
    'glass': {'name': 'glass', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.17, 0.26, 0.33, 1.0], 'metallicFactor': 0.92, 'roughnessFactor': 0.13}},
    'span':  {'name': 'spandrel', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.84, 0.84, 0.86, 1.0], 'metallicFactor': 0.55, 'roughnessFactor': 0.38}},
    'stone': {'name': 'stone', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.58, 0.56, 0.52, 1.0], 'metallicFactor': 0.05, 'roughnessFactor': 0.82}},
}
u16 = len(V) < 65500
ctype, fmt, isize = (5123, '<H', 2) if u16 else (5125, '<I', 4)
materials, mat_idx, prim_json, off, tris = [], {}, [], len(buf), 0
for k, (mat, idx) in enumerate(prims):
    if mat not in mat_idx:
        mat_idx[mat] = len(materials); materials.append(MAT[mat])
    ib = b''.join(struct.pack(fmt, i) for i in idx)
    ib += b'\x00' * ((4 - len(ib) % 4) % 4)   # 4-byte view alignment
    views.append({'buffer': 0, 'byteOffset': off, 'byteLength': len(ib), 'target': 34963})
    acc.append({'bufferView': 1+k, 'componentType': ctype, 'count': len(idx), 'type': 'SCALAR'})
    prim_json.append({'attributes': {'POSITION': 0}, 'indices': 1+k, 'material': mat_idx[mat]})
    buf += ib; off += len(ib); tris += len(idx)//3
gltf = {'asset': {'version': '2.0', 'generator': 'nadlan-parametric-hinfinity'},
        'scene': 0, 'scenes': [{'nodes': [0]}], 'nodes': [{'mesh': 0, 'name': 'HInfinity'}],
        'meshes': [{'primitives': prim_json, 'name': 'HInfinity'}], 'materials': materials,
        'buffers': [{'byteLength': len(buf)}], 'bufferViews': views, 'accessors': acc}
js = json.dumps(gltf, separators=(',', ':')).encode('utf-8')
js += b' ' * ((4 - len(js) % 4) % 4)
buf += b'\x00' * ((4 - len(buf) % 4) % 4)
glb = (b'glTF' + struct.pack('<II', 2, 12+8+len(js)+8+len(buf))
       + struct.pack('<I', len(js)) + b'JSON' + js
       + struct.pack('<I', len(buf)) + b'BIN\x00' + buf)
out = r'C:\Users\pro\AppData\Local\Temp\claude\C--Users-pro-nad-lan\a1527a51-5842-4f81-8165-9a594085b50f\scratchpad\h-infinity.glb'
open(out, 'wb').write(glb)
print('ToHa2 v2 GLB: %d KB, %d verts (uint16=%s), %d triangles, height %.1fm' % (
    len(glb)//1024, len(V), u16, tris, TOP+CROWN))
