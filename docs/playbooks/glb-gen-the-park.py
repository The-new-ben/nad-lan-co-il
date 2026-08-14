# -*- coding: utf-8 -*-
# Parametric GLB generator: THE PARK Bnei Brak massing, ~20k triangles.
# Pure python (struct+json), glTF 2.0 binary. Y-up, meters, origin at base center.
import io, json, struct, math

# ---- geometry helpers -------------------------------------------------
V = []   # positions
N = []   # normals
PRIMS = {}  # material -> index list

def quad(mat, a, b, c, d):
    # flat-shaded quad abcd (counter-clockwise seen from outside)
    ux, uy, uz = b[0]-a[0], b[1]-a[1], b[2]-a[2]
    vx, vy, vz = d[0]-a[0], d[1]-a[1], d[2]-a[2]
    nx, ny, nz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
    l = math.sqrt(nx*nx+ny*ny+nz*nz) or 1.0
    nx, ny, nz = nx/l, ny/l, nz/l
    base = len(V)
    for p in (a, b, c, d):
        V.append(p); N.append((nx, ny, nz))
    PRIMS.setdefault(mat, []).extend([base, base+1, base+2, base, base+2, base+3])

def ring(w, d, r, y, segs_per_side=10, corner_segs=11):
    # rounded-rectangle ring of points at height y (width w along x, depth d along z)
    pts = []
    hw, hd = w/2.0-r, d/2.0-r
    corners = [(hw, hd, 0), (-hw, hd, 90), (-hw, -hd, 180), (hw, -hd, 270)]
    for cx, cz, a0 in corners:
        for i in range(corner_segs+1):
            a = math.radians(a0 + 90.0*i/corner_segs)
            pts.append((cx + r*math.cos(a), y, cz + r*math.sin(a)))
    return pts

def band(mat, w, d, r, y0, y1, inset=0.0):
    lo = ring(w-2*inset, d-2*inset, max(r-inset, 0.3), y0)
    hi = ring(w-2*inset, d-2*inset, max(r-inset, 0.3), y1)
    n = len(lo)
    for i in range(n):
        j = (i+1) % n
        quad(mat, lo[i], lo[j], hi[j], hi[i])

def tri(mat, a, b, c):
    ux, uy, uz = b[0]-a[0], b[1]-a[1], b[2]-a[2]
    vx, vy, vz = c[0]-a[0], c[1]-a[1], c[2]-a[2]
    nx, ny, nz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
    l = math.sqrt(nx*nx+ny*ny+nz*nz) or 1.0
    base = len(V)
    for p in (a, b, c):
        V.append(p); N.append((nx/l, ny/l, nz/l))
    PRIMS.setdefault(mat, []).extend([base, base+1, base+2])

def slab(mat, w, d, r, y, out=0.0):
    # horizontal cap: triangle fan to center
    pts = ring(w+2*out, d+2*out, r+out, y)
    n = len(pts)
    for i in range(n):
        j = (i+1) % n
        tri(mat, pts[i], (0.0, y, 0.0), pts[j])

# ---- THE PARK massing -------------------------------------------------
# podium: 8 levels, retail+lobby, wider; tower: 44 office floors; crown.
POD_W, POD_D, POD_R = 62.0, 46.0, 6.0
TWR_W, TWR_D, TWR_R = 44.0, 30.0, 7.0
POD_FLOORS, POD_H = 8, 4.2
TWR_FLOORS, GLASS_H, SPAN_H = 44, 2.5, 0.8
FLOOR_H = GLASS_H + SPAN_H
POD_TOP = POD_FLOORS * POD_H
CROWN_H = 7.9  # totals 186.7m, the published height

# podium: glass bands with stone spandrels, slight vertical rhythm
for f in range(POD_FLOORS):
    y0 = f * POD_H
    band('stone', POD_W, POD_D, POD_R, y0, y0+0.8)
    band('glass', POD_W, POD_D, POD_R, y0+0.8, y0+POD_H-0.4, inset=0.35)
    band('stone', POD_W, POD_D, POD_R, y0+POD_H-0.4, y0+POD_H)
slab('stone', POD_W, POD_D, POD_R, POD_TOP, out=0.6)

# tower floors
for f in range(TWR_FLOORS):
    y0 = POD_TOP + f*FLOOR_H
    band('glass', TWR_W, TWR_D, TWR_R, y0, y0+GLASS_H, inset=0.30)
    band('span',  TWR_W, TWR_D, TWR_R, y0+GLASS_H, y0+FLOOR_H)
    # vertical fins on every segment + a horizontal ledge lip per floor
    fins = ring(TWR_W, TWR_D, TWR_R, y0)
    for i in range(len(fins)):
        x, _, z = fins[i]
        l = math.sqrt(x*x+z*z) or 1
        ox, oz = x/l*0.22, z/l*0.22
        quad('span', (x, y0, z), (x+ox, y0, z+oz), (x+ox, y0+GLASS_H, z+oz), (x, y0+GLASS_H, z))
    lip_lo = ring(TWR_W+0.5, TWR_D+0.5, TWR_R+0.25, y0+GLASS_H)
    lip_hi = ring(TWR_W, TWR_D, TWR_R, y0+GLASS_H+0.12)
    for i in range(len(lip_lo)):
        j = (i+1) % len(lip_lo)
        quad('span', lip_lo[i], lip_lo[j], lip_hi[j], lip_hi[i])

TWR_TOP = POD_TOP + TWR_FLOORS*FLOOR_H
# crown
band('span', TWR_W, TWR_D, TWR_R, TWR_TOP, TWR_TOP+CROWN_H, inset=0.6)
band('glass', TWR_W-4, TWR_D-4, TWR_R, TWR_TOP+1.0, TWR_TOP+CROWN_H-1.0, inset=1.4)
slab('span', TWR_W-2, TWR_D-2, TWR_R, TWR_TOP+CROWN_H)

# ---- write GLB --------------------------------------------------------
def floats(arr):
    return b''.join(struct.pack('<3f', *p) for p in arr)

pos_bin = floats(V)
nrm_bin = floats(N)
prim_list = sorted(PRIMS.items())
idx_bins = [b''.join(struct.pack('<I', i) for i in idx) for _, idx in prim_list]

buffers = pos_bin + nrm_bin
views = [
    {'buffer': 0, 'byteOffset': 0, 'byteLength': len(pos_bin), 'target': 34962},
    {'buffer': 0, 'byteOffset': len(pos_bin), 'byteLength': len(nrm_bin), 'target': 34962},
]
accessors = [
    {'bufferView': 0, 'componentType': 5126, 'count': len(V), 'type': 'VEC3',
     'min': [min(p[i] for p in V) for i in range(3)],
     'max': [max(p[i] for p in V) for i in range(3)]},
    {'bufferView': 1, 'componentType': 5126, 'count': len(N), 'type': 'VEC3'},
]
prims_json = []
mat_defs = {
    'glass': {'name': 'glass', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.16, 0.24, 0.30, 1.0], 'metallicFactor': 0.9, 'roughnessFactor': 0.15}},
    'span':  {'name': 'spandrel', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.78, 0.70, 0.52, 1.0], 'metallicFactor': 0.4, 'roughnessFactor': 0.5}},
    'stone': {'name': 'stone', 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': [0.62, 0.58, 0.50, 1.0], 'metallicFactor': 0.05, 'roughnessFactor': 0.8}},
}
materials = []
mat_index = {}
for mi, (mat, _) in enumerate(prim_list):
    mat_index[mat] = len(materials)
    materials.append(mat_defs[mat])
off = len(buffers)
tri_total = 0
for k, (mat, idx) in enumerate(prim_list):
    ib = idx_bins[k]
    views.append({'buffer': 0, 'byteOffset': off, 'byteLength': len(ib), 'target': 34963})
    accessors.append({'bufferView': 2+k, 'componentType': 5125, 'count': len(idx), 'type': 'SCALAR'})
    prims_json.append({'attributes': {'POSITION': 0, 'NORMAL': 1}, 'indices': 2+k, 'material': mat_index[mat]})
    buffers += ib
    off += len(ib)
    tri_total += len(idx)//3

gltf = {
    'asset': {'version': '2.0', 'generator': 'nadlan-parametric'},
    'scene': 0, 'scenes': [{'nodes': [0]}],
    'nodes': [{'mesh': 0, 'name': 'ThePark'}],
    'meshes': [{'primitives': prims_json, 'name': 'ThePark'}],
    'materials': materials,
    'buffers': [{'byteLength': len(buffers)}],
    'bufferViews': views, 'accessors': accessors,
}
js = json.dumps(gltf, separators=(',', ':')).encode('utf-8')
js += b' ' * ((4 - len(js) % 4) % 4)
buffers += b'\x00' * ((4 - len(buffers) % 4) % 4)
glb = (b'glTF' + struct.pack('<II', 2, 12+8+len(js)+8+len(buffers))
       + struct.pack('<I', len(js)) + b'JSON' + js
       + struct.pack('<I', len(buffers)) + b'BIN\x00' + buffers)
out = r'C:\Users\pro\AppData\Local\Temp\claude\C--Users-pro-nad-lan\a1527a51-5842-4f81-8165-9a594085b50f\scratchpad\the-park-tower.glb'
open(out, 'wb').write(glb)
print('GLB written: %d KB, %d verts, %d triangles, height %.1fm' % (len(glb)//1024, len(V), tri_total, TWR_TOP+CROWN_H))
