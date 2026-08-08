# -*- coding: utf-8 -*-
# Parametric massing for ToHa2 Tel Aviv, ~50k triangles.
# HONEST MODEL: a tapering elliptical tower with rounded corners and a sky-lobby
# band - the published massing family (298m, ~75 floors, Ron Arad + Yashar).
# It is a MASSING STUDY, not the architect's geometry: the page must show the
# generic-model chip. Y-up, metres, origin at base centre.
import io, json, math, struct

V, N, PRIMS = [], [], {}

def quad(mat, a, b, c, d):
    ux, uy, uz = b[0]-a[0], b[1]-a[1], b[2]-a[2]
    vx, vy, vz = d[0]-a[0], d[1]-a[1], d[2]-a[2]
    nx, ny, nz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
    l = math.sqrt(nx*nx+ny*ny+nz*nz) or 1.0
    base = len(V)
    for p in (a, b, c, d):
        V.append(p); N.append((nx/l, ny/l, nz/l))
    PRIMS.setdefault(mat, []).extend([base, base+1, base+2, base, base+2, base+3])

def tri(mat, a, b, c):
    ux, uy, uz = b[0]-a[0], b[1]-a[1], b[2]-a[2]
    vx, vy, vz = c[0]-a[0], c[1]-a[1], c[2]-a[2]
    nx, ny, nz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
    l = math.sqrt(nx*nx+ny*ny+nz*nz) or 1.0
    base = len(V)
    for p in (a, b, c):
        V.append(p); N.append((nx/l, ny/l, nz/l))
    PRIMS.setdefault(mat, []).extend([base, base+1, base+2])

SEG = 96                      # points per ring -> smooth ellipse
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

# ---- proportions from the verified dossier -------------------------------
H_TOTAL = 298.2               # CTBUH height
FLOORS = 75
POD_FLOORS, POD_H = 5, 6.0    # generous public podium / lobby zone
POD_TOP = POD_FLOORS * POD_H
CROWN = 9.0
FLOOR_H = (H_TOTAL - POD_TOP - CROWN) / FLOORS
GLASS = FLOOR_H * 0.74
RX0, RZ0 = 31.0, 22.0         # base plate radii (~2,700 sqm typical floor)
RX1, RZ1 = 24.0, 17.5         # crown plate radii: gentle taper
SKY_A, SKY_B = 34, 37         # sky-lobby band floors

# podium: stone with a deep glazed lobby
for f in range(POD_FLOORS):
    y0 = f * POD_H
    band('stone', RX0*1.18, RZ0*1.18, y0, RX0*1.18, RZ0*1.18, y0+0.9)
    band('glass', RX0*1.16, RZ0*1.16, y0+0.9, RX0*1.16, RZ0*1.16, y0+POD_H-0.5)
    band('stone', RX0*1.18, RZ0*1.18, y0+POD_H-0.5, RX0*1.18, RZ0*1.18, y0+POD_H)
cap('stone', RX0*1.18, RZ0*1.18, POD_TOP)

def radii(f):
    k = f / float(FLOORS)
    ease = k*k*(3-2*k)                      # smoothstep taper
    rx = RX0 + (RX1-RX0)*ease
    rz = RZ0 + (RZ1-RZ0)*ease
    if SKY_A <= f <= SKY_B:                 # sky-lobby recess reads in the skyline
        rx, rz = rx*0.93, rz*0.93
    return rx, rz

TWIST = math.radians(9.0)                   # subtle rotation over full height
for f in range(FLOORS):
    y0 = POD_TOP + f*FLOOR_H
    rx0, rz0 = radii(f)
    rx1, rz1 = radii(f+1)
    t0, t1 = TWIST*f/FLOORS, TWIST*(f+1)/FLOORS
    band('glass', rx0, rz0, y0, rx0+(rx1-rx0)*0.74, rz0+(rz1-rz0)*0.74, y0+GLASS, t0, t0+(t1-t0)*0.74)
    band('span', rx0+(rx1-rx0)*0.74, rz0+(rz1-rz0)*0.74, y0+GLASS, rx1, rz1, y0+FLOOR_H, t0+(t1-t0)*0.74, t1)
    # floor lip catches light and gives the facade its horizontal rhythm
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

# ---- glTF binary ---------------------------------------------------------
pos = b''.join(struct.pack('<3f', *p) for p in V)
nrm = b''.join(struct.pack('<3f', *n) for n in N)
prims = sorted(PRIMS.items())
buf = pos + nrm
views = [{'buffer': 0, 'byteOffset': 0, 'byteLength': len(pos), 'target': 34962},
         {'buffer': 0, 'byteOffset': len(pos), 'byteLength': len(nrm), 'target': 34962}]
acc = [{'bufferView': 0, 'componentType': 5126, 'count': len(V), 'type': 'VEC3',
        'min': [min(p[i] for p in V) for i in range(3)],
        'max': [max(p[i] for p in V) for i in range(3)]},
       {'bufferView': 1, 'componentType': 5126, 'count': len(N), 'type': 'VEC3'}]
MAT = {
    'glass': {'name': 'glass', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.17, 0.26, 0.33, 1.0], 'metallicFactor': 0.92, 'roughnessFactor': 0.13}},
    'span':  {'name': 'spandrel', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.84, 0.84, 0.86, 1.0], 'metallicFactor': 0.55, 'roughnessFactor': 0.38}},
    'stone': {'name': 'stone', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.58, 0.56, 0.52, 1.0], 'metallicFactor': 0.05, 'roughnessFactor': 0.82}},
}
materials, mat_idx, prim_json, off, tris = [], {}, [], len(buf), 0
for k, (mat, idx) in enumerate(prims):
    if mat not in mat_idx:
        mat_idx[mat] = len(materials); materials.append(MAT[mat])
    ib = b''.join(struct.pack('<I', i) for i in idx)
    views.append({'buffer': 0, 'byteOffset': off, 'byteLength': len(ib), 'target': 34963})
    acc.append({'bufferView': 2+k, 'componentType': 5125, 'count': len(idx), 'type': 'SCALAR'})
    prim_json.append({'attributes': {'POSITION': 0, 'NORMAL': 1}, 'indices': 2+k, 'material': mat_idx[mat]})
    buf += ib; off += len(ib); tris += len(idx)//3
gltf = {'asset': {'version': '2.0', 'generator': 'nadlan-parametric-toha2'},
        'scene': 0, 'scenes': [{'nodes': [0]}], 'nodes': [{'mesh': 0, 'name': 'ToHa2'}],
        'meshes': [{'primitives': prim_json, 'name': 'ToHa2'}], 'materials': materials,
        'buffers': [{'byteLength': len(buf)}], 'bufferViews': views, 'accessors': acc}
js = json.dumps(gltf, separators=(',', ':')).encode('utf-8')
js += b' ' * ((4 - len(js) % 4) % 4)
buf += b'\x00' * ((4 - len(buf) % 4) % 4)
glb = (b'glTF' + struct.pack('<II', 2, 12+8+len(js)+8+len(buf))
       + struct.pack('<I', len(js)) + b'JSON' + js
       + struct.pack('<I', len(buf)) + b'BIN\x00' + buf)
out = r'C:\Users\pro\AppData\Local\Temp\claude\C--Users-pro-nad-lan\a1527a51-5842-4f81-8165-9a594085b50f\scratchpad\toha2-tower.glb'
open(out, 'wb').write(glb)
print('ToHa2 GLB: %d KB, %d verts, %d triangles, height %.1fm, floors %d, typical plate ~%d sqm' % (
    len(glb)//1024, len(V), tris, TOP+CROWN, FLOORS, int(math.pi*RX0*RZ0)))
