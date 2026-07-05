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

CREAM  = [235, 224, 194, 255]
STONE  = [255, 240, 194, 255]
GLASS  = [158, 220, 235, 185]
GLASS2 = [120, 190, 215, 205]
GOLD   = [212, 175, 108, 255]
PAVE   = [226, 220, 208, 255]
GREEN  = [140, 165, 120, 255]
CTX    = [242, 238, 228, 160]
WATER  = [122, 180, 205, 220]

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
    # site plate + paths + green
    box(S, 'site', 0, -0.6, 0, sw, 1.2, sd, PAVE)
    box(S, 'green1', -sw*0.28, 0.05, sd*0.3, sw*0.3, 0.15, sd*0.25, GREEN)
    box(S, 'green2', sw*0.3, 0.05, -sd*0.28, sw*0.22, 0.15, sd*0.2, GREEN)
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
            for s in sides:
                for k in range(segn):
                    off = (k - (segn-1)/2) * (wt/segn)
                    if s == 'W':
                        box(S, f'b{bi}f{f}W{k}', x0 - wt/2 - 0.8, y, z0 + off*(dt/wt), 1.6, 0.18, dt/segn*0.72, STONE)
                    elif s == 'E':
                        box(S, f'b{bi}f{f}E{k}', x0 + wt/2 + 0.8, y, z0 + off*(dt/wt), 1.6, 0.18, dt/segn*0.72, STONE)
                    elif s == 'S':
                        box(S, f'b{bi}f{f}S{k}', x0 + off, y, z0 + dt/2 + 0.8, wt/segn*0.72, 0.18, 1.6, STONE)
                    elif s == 'N':
                        box(S, f'b{bi}f{f}N{k}', x0 + off, y, z0 - dt/2 - 0.8, wt/segn*0.72, 0.18, 1.6, STONE)
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
