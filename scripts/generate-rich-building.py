#!/usr/bin/env python3
"""
Rich-model factory: Rainbow-grade illustrative GLBs from real composition specs.

Per building it builds: tinted glass core, cream floor slabs, rhythmic balcony
plates, corner fins, roof crown, podium/lobby, small honest site plate (NEVER a
1km ground, NEVER a sea unless the spec says seafront). PBR colors follow the
site DNA (cream paper, warm stone, teal glass, gold crown accents).

Usage: python3 scripts/generate-rich-building.py <spec.json> <out.glb>
Spec: {"floor_h":3.2, "seafront":false, "site":[w,d],
       "buildings":[{"w":26,"d":26,"floors":35,"x":0,"z":0,"balconies":"WES",
                     "taper":0.1,"podium":0}], "context":[[x,z,w,d,h],...]}
"""
import sys, json
import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial

CREAM  = [244, 233, 204, 255]   # warm slab cream
STONE  = [226, 205, 160, 255]   # warmer stone, real contrast vs slabs
GLASS  = [96, 178, 205, 210]    # saturated teal
GLASS2 = [78, 156, 188, 215]
BALG   = [168, 220, 238, 130]   # balustrade glass
GOLD   = [196, 156, 84, 255]
PAVE   = [214, 204, 184, 255]
PATH   = [238, 230, 214, 255]
GREEN  = [124, 152, 104, 255]
TRUNK  = [122, 96, 66, 255]
CTX    = [238, 231, 216, 170]
WATER  = [96, 168, 198, 225]
POOL   = [92, 186, 212, 235]

def box(scene, name, cx, cy, cz, w, h, d, rgba):
    m = trimesh.creation.box(extents=[w, h, d])
    m.apply_translation([cx, cy, cz])
    m.visual = trimesh.visual.TextureVisuals(material=PBRMaterial(
        baseColorFactor=rgba, metallicFactor=0.05,
        roughnessFactor=0.6 if rgba[3] == 255 else 0.15,
        alphaMode='BLEND' if rgba[3] < 255 else 'OPAQUE'))
    scene.add_geometry(m, node_name=name)

def build(spec, out):
    S = trimesh.Scene()
    fh = spec.get('floor_h', 3.2)
    sw, sd = spec.get('site', [160, 130])
    # site plate + paths + green + court
    box(S, 'site', 0, -0.6, 0, sw, 1.2, sd, PAVE)
    box(S, 'pathx', 0, 0.02, 0, sw*0.96, 0.1, 6, PATH)
    box(S, 'pathz', 0, 0.02, 0, 6, 0.1, sd*0.96, PATH)
    box(S, 'green1', -sw*0.28, 0.1, sd*0.3, sw*0.3, 0.3, sd*0.25, GREEN)
    box(S, 'green2', sw*0.3, 0.1, -sd*0.28, sw*0.22, 0.3, sd*0.2, GREEN)
    cx_, cz_ = spec.get('court', [sw*0.18, sd*0.22])[:2] if isinstance(spec.get('court'), list) else (sw*0.18, sd*0.22)
    if spec.get('court', True):
        box(S, 'courtdeck', cx_, 0.06, cz_, 34, 0.22, 22, [235, 222, 196, 255])
        box(S, 'pool', cx_, 0.2, cz_, 24, 0.3, 12, POOL)
    # trees: clustered cones on the green
    import itertools
    ti = 0
    for gx, gz in [(-sw*0.28, sd*0.3), (sw*0.3, -sd*0.28), (-sw*0.34, -sd*0.18), (sw*0.2, sd*0.34)]:
        for dx, dz in [(0,0),(7,4),(-6,5),(4,-6)]:
            t = trimesh.creation.cone(radius=2.6, height=6.5, sections=7)
            t.apply_translation([gx+dx, 3.2+2.2, gz+dz])
            t.visual = trimesh.visual.TextureVisuals(material=PBRMaterial(baseColorFactor=GREEN, roughnessFactor=0.9))
            S.add_geometry(t, node_name=f'tree{ti}')
            tr = trimesh.creation.cylinder(radius=0.45, height=2.4, sections=6)
            tr.apply_translation([gx+dx, 1.2, gz+dz])
            tr.visual = trimesh.visual.TextureVisuals(material=PBRMaterial(baseColorFactor=TRUNK, roughnessFactor=0.9))
            S.add_geometry(tr, node_name=f'trunk{ti}'); ti += 1
    if spec.get('seafront'):
        box(S, 'sea', -(sw/2 + 45), -0.9, 0, 90, 0.8, sd + 60, WATER)
        box(S, 'beach', -(sw/2 + 4), -0.35, 0, 12, 0.7, sd + 30, [240, 226, 190, 255])
    for i, c in enumerate(spec.get('context', [])):
        x, z, w, d, h = c
        box(S, f'ctx{i}', x, h/2, z, w, h, d, CTX)

    for bi, b in enumerate(spec['buildings']):
        w, d, fl = b['w'], b['d'], b['floors']
        x0, z0 = b.get('x', 0), b.get('z', 0)
        H = fl * fh
        pod = b.get('podium', 0)
        # glass core (slightly inset)
        gc = GLASS if bi % 2 == 0 else GLASS2
        box(S, f'b{bi}glass', x0, H/2, z0, w-1.6, H, d-1.6, gc)
        # floor slabs
        for f in range(fl + 1):
            y = f * fh
            t = 1 - b.get('taper', 0) * (f / max(fl, 1))
            box(S, f'b{bi}s{f}', x0, y, z0, w*t, 0.35, d*t, CREAM)
        # balconies: sides in string e.g. "WS" (west/-x, south/+z, east/+x, north/-z)
        sides = b.get('balconies', 'WS')
        segn = max(2, int(w // 8))
        for f in range(1, fl):
            y = f * fh + fh*0.45
            t = 1 - b.get('taper', 0) * (f / max(fl, 1))
            wt, dt = w*t, d*t
            shift = (f % 2) * (wt/segn) * 0.5   # alternating rhythm
            for s in sides:
                for k in range(segn):
                    off = (k - (segn-1)/2) * (wt/segn) + shift
                    seg = dt/segn*0.78
                    if s in 'WE':
                        sx = -1 if s == 'W' else 1
                        bx = x0 + sx*(wt/2 + 1.1)
                        box(S, f'b{bi}f{f}{s}{k}', bx, y, z0 + off*(dt/wt), 2.2, 0.22, seg, STONE)
                        box(S, f'b{bi}g{f}{s}{k}', bx + sx*0.95, y + 0.62, z0 + off*(dt/wt), 0.1, 1.05, seg, BALG)
                    else:
                        sz = 1 if s == 'S' else -1
                        bz = z0 + sz*(dt/2 + 1.1)
                        segw = wt/segn*0.78
                        box(S, f'b{bi}f{f}{s}{k}', x0 + off, y, bz, segw, 0.22, 2.2, STONE)
                        box(S, f'b{bi}g{f}{s}{k}', x0 + off, y + 0.62, bz + sz*0.95, segw, 1.05, 0.1, BALG)
        # corner fins
        for sx in (-1, 1):
            for sz in (-1, 1):
                box(S, f'b{bi}fin{sx}{sz}', x0 + sx*(w/2-0.5), H/2, z0 + sz*(d/2-0.5), 1.0, H, 1.0, STONE)
        # crown + gold band
        box(S, f'b{bi}crown', x0, H + 1.2, z0, w*0.86, 2.4, d*0.86, STONE)
        box(S, f'b{bi}gold', x0, H + 2.6, z0, w*0.5, 0.5, d*0.5, GOLD)
        # podium/lobby
        if pod:
            box(S, f'b{bi}pod', x0, pod*fh/2, z0, w*1.5, pod*fh, d*1.5, STONE)
            box(S, f'b{bi}podglass', x0, pod*fh/2, z0, w*1.5+0.4, pod*fh*0.6, d*1.5+0.4, GLASS)

    tris = sum(g.faces.shape[0] for g in S.geometry.values())
    S.export(out)
    print(f"wrote {out}: {len(S.geometry)} meshes, {tris} tris")

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1]))
    build(spec, sys.argv[2])
