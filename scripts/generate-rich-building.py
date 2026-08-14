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

PLASTER = [242, 238, 228, 255]   # Israeli plaster white
PLASTER2 = [232, 226, 210, 255]  # shadow tone
WGLASS  = [70, 96, 112, 255]     # punched-window dark glass
FRAME   = [210, 202, 186, 255]
AC      = [236, 236, 232, 255]
AWNING  = [194, 86, 58, 255]     # terracotta storefront awnings
SOLARP  = [42, 52, 64, 255]      # solar collector panel
TANK    = [238, 238, 234, 255]

def cyl(scene, name, cx, cy, cz, r, h, rgba, axis='y', sections=8):
    m = trimesh.creation.cylinder(radius=r, height=h, sections=sections)
    if axis == 'x':
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 0, 1]))
    elif axis == 'z':
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
    m.apply_translation([cx, cy, cz])
    m.visual = trimesh.visual.TextureVisuals(material=PBRMaterial(
        baseColorFactor=rgba, metallicFactor=0.05, roughnessFactor=0.7))
    scene.add_geometry(m, node_name=name)

def build_standard(spec, out):
    """The STANDARD ISRAELI BUILDING (owner 2026-07-11): a normal Tel Aviv
    street building a developer recognizes as "could be my project" - plaster
    body, punched windows with AC units, continuous balcony bands, pilotis or
    storefront ground floor, rooftop solar heaters + pergola. HOTSPOT
    CONVENTION: main building ~26.4m square, centered at origin, floors from
    y=0 at floor_h 3.05 - the engine formula lands hotspots on the facade
    with zero authoring. Light low-alpha context, honest small site."""
    S = trimesh.Scene()
    fh = spec.get('floor_h', 3.05)
    fl = int(spec.get('floors', 8))
    w = d = spec.get('width', 26.4)
    commercial = bool(spec.get('commercial_ground', False))
    H = fl * fh
    sw, sd = spec.get('site', [96, 78])

    # honest site: plate + street + sidewalk + greens + trees
    box(S, 'site', 0, -0.5, 0, sw, 1.0, sd, PAVE)
    box(S, 'road', 0, 0.02, sd*0.36, sw, 0.08, 9, [88, 86, 82, 255])
    box(S, 'lane', 0, 0.08, sd*0.36, sw*0.9, 0.02, 0.35, [214, 208, 196, 255])
    box(S, 'walk', 0, 0.06, sd*0.27, sw, 0.16, 4.5, PATH)
    box(S, 'green1', -sw*0.32, 0.1, -sd*0.22, sw*0.24, 0.28, sd*0.3, GREEN)
    box(S, 'green2', sw*0.33, 0.1, -sd*0.2, sw*0.2, 0.28, sd*0.26, GREEN)
    ti = 0
    for gx, gz in [(-sw*0.32, -sd*0.22), (sw*0.33, -sd*0.2), (sw*0.18, sd*0.16)]:
        for dx, dz in [(0, 0), (6, 4), (-5, 3), (3, -5)]:
            t = trimesh.creation.cone(radius=2.4, height=5.8, sections=7)
            t.apply_translation([gx+dx, 2.9+2.0, gz+dz])
            t.visual = trimesh.visual.TextureVisuals(material=PBRMaterial(baseColorFactor=GREEN, roughnessFactor=0.9))
            S.add_geometry(t, node_name=f'stree{ti}')
            tr = trimesh.creation.cylinder(radius=0.4, height=2.2, sections=6)
            tr.apply_translation([gx+dx, 1.1, gz+dz])
            tr.visual = trimesh.visual.TextureVisuals(material=PBRMaterial(baseColorFactor=TRUNK, roughnessFactor=0.9))
            S.add_geometry(tr, node_name=f'strunk{ti}'); ti += 1
    # low-alpha neighbor masses (never a big plate, never a fake skyline)
    for i, c in enumerate(spec.get('context', [[-34, -26, 18, 14, 15], [34, -24, 16, 13, 12], [-33, 20, 17, 13, 18], [34, 22, 15, 12, 9]])):
        x, z, cw, cd, ch = c
        box(S, f'sctx{i}', x, ch/2, z, cw, ch, cd, CTX)

    g0 = 1 if commercial else 1   # residential floors start at floor 1 (GF is pilotis/commercial)
    # main body: plaster, floors from y=0 (convention)
    box(S, 'body', 0, H/2 + (fh*g0)/2, 0, w-0.2, H - fh*g0, d-0.2, PLASTER)
    # floor slab lines (subtle shadow bands)
    for f in range(g0, fl+1):
        box(S, f'slab{f}', 0, f*fh, 0, w+0.15, 0.18, d+0.15, PLASTER2)

    # punched windows + AC units on all 4 facades; balcony bands on S + W
    nwin = 6
    for f in range(g0, fl):
        y = f*fh + fh*0.5
        for side in 'NSEW':
            horiz = side in 'NS'
            length = w if horiz else d
            for k in range(nwin):
                off = (k - (nwin-1)/2) * (length/nwin)
                if side in 'SW':  # balcony sides get doors instead of windows
                    continue
                wx = off if horiz else (w/2 + 0.06) * (1 if side == 'E' else -1)
                wz = (d/2 + 0.06) * (1 if side == 'S' else -1) if horiz else off
                if horiz:
                    box(S, f'wf{f}{side}{k}', wx, y, wz, 1.7, 1.6, 0.14, FRAME)
                    box(S, f'wg{f}{side}{k}', wx, y, wz + (0.04 if side == 'S' else -0.04), 1.45, 1.35, 0.1, WGLASS)
                    box(S, f'ws{f}{side}{k}', wx, y - 0.95, wz + (0.12 if side == 'S' else -0.12), 1.8, 0.12, 0.3, PLASTER2)
                    if True:
                        box(S, f'ac{f}{side}{k}', wx + 0.55, y - 1.35, wz + (0.3 if side == 'S' else -0.3), 0.68, 0.5, 0.45, AC)
                else:
                    box(S, f'wf{f}{side}{k}', wx, y, wz, 0.14, 1.6, 1.7, FRAME)
                    box(S, f'wg{f}{side}{k}', wx + (0.04 if side == 'E' else -0.04), y, wz, 0.1, 1.35, 1.45, WGLASS)
                    box(S, f'ws{f}{side}{k}', wx + (0.12 if side == 'E' else -0.12), y - 0.95, wz, 0.3, 0.12, 1.8, PLASTER2)
                    if True:
                        box(S, f'ac{f}{side}{k}', wx + (0.3 if side == 'E' else -0.3), y - 1.35, wz + 0.55, 0.45, 0.5, 0.68, AC)
        # continuous balcony bands, south + west (the street faces)
        for side in ('S', 'W'):
            if side == 'S':
                bz = d/2 + 1.3
                box(S, f'bal{f}S', 0, f*fh + 0.1, bz, w*0.86, 0.22, 2.4, CREAM)
                box(S, f'balg{f}S', 0, f*fh + 0.75, bz + 1.05, w*0.86, 1.1, 0.08, BALG)
                for fin in range(4):
                    fx = (fin - 1.5) * (w*0.86/4)
                    box(S, f'balf{f}S{fin}', fx, f*fh + 0.7, bz, 0.14, 1.15, 2.2, PLASTER2)
                # glazed balcony doors behind the band
                for k in range(3):
                    off = (k - 1) * (w*0.24)
                    box(S, f'bd{f}S{k}', off, f*fh + fh*0.5, d/2 - 0.02, 1.9, 2.1, 0.1, WGLASS)
                if f % 2 == 0:
                    for k in range(2):
                        off = (k - 0.5) * (w*0.4)
                        box(S, f'bp{f}S{k}', off, f*fh + 0.5, bz + 0.85, 1.6, 0.5, 0.5, TRUNK)
                        box(S, f'bpg{f}S{k}', off, f*fh + 0.9, bz + 0.85, 1.5, 0.4, 0.42, GREEN)
            else:
                bx = -(w/2 + 1.3)
                box(S, f'bal{f}W', bx, f*fh + 0.1, 0, 2.4, 0.22, d*0.86, CREAM)
                box(S, f'balg{f}W', bx - 1.05, f*fh + 0.75, 0, 0.08, 1.1, d*0.86, BALG)
                for fin in range(4):
                    fz = (fin - 1.5) * (d*0.86/4)
                    box(S, f'balf{f}W{fin}', bx, f*fh + 0.7, fz, 2.2, 1.15, 0.14, PLASTER2)
                for k in range(3):
                    off = (k - 1) * (d*0.24)
                    box(S, f'bd{f}W{k}', -(w/2 - 0.02), f*fh + fh*0.5, off, 0.1, 2.1, 1.9, WGLASS)
                if f % 2 == 1:
                    for k in range(2):
                        off = (k - 0.5) * (d*0.4)
                        box(S, f'bp{f}W{k}', bx - 0.85, f*fh + 0.5, off, 0.5, 0.5, 1.6, TRUNK)
                        box(S, f'bpg{f}W{k}', bx - 0.85, f*fh + 0.9, off, 0.42, 0.4, 1.5, GREEN)

    # ground floor
    if commercial:
        # storefront glass + terracotta awnings + signage band (street sides)
        box(S, 'gfcore', 0, fh*0.5, 0, w-0.2, fh, d-0.2, STONE)
        box(S, 'store_s', 0, fh*0.45, d/2 - 0.05, w*0.92, fh*0.8, 0.25, GLASS)
        box(S, 'store_w', -(w/2 - 0.05), fh*0.45, 0, 0.25, fh*0.8, d*0.92, GLASS)
        box(S, 'sign', 0, fh - 0.25, d/2 + 0.18, w*0.94, 0.5, 0.14, PLASTER2)
        for k in range(4):
            off = (k - 1.5) * (w*0.23)
            box(S, f'awn{k}', off, fh*0.72, d/2 + 0.75, w*0.2, 0.1, 1.5, AWNING)
    else:
        # pilotis: columns + recessed glazed lobby + canopy
        box(S, 'lobby', 0, fh*0.5, 0, w*0.55, fh, d*0.55, GLASS)
        box(S, 'lobbywall', -w*0.1, fh*0.5, -d*0.12, w*0.3, fh, 0.3, STONE)
        for i2, (px, pz) in enumerate([(-w/2+1.2, -d/2+1.2), (w/2-1.2, -d/2+1.2), (-w/2+1.2, d/2-1.2), (w/2-1.2, d/2-1.2), (0, d/2-1.2), (0, -d/2+1.2), (-w/2+1.2, 0), (w/2-1.2, 0)]):
            cyl(S, f'col{i2}', px, fh*0.5, pz, 0.34, fh, PLASTER2)
        box(S, 'canopy', 0, fh + 0.1, d/2 + 1.6, 7.5, 0.2, 3.0, STONE)
        box(S, 'entry', 0, fh*0.45, d/2 - 0.15, 2.6, fh*0.85, 0.2, WGLASS)

    # roof: parapet + Israeli solar heaters + pergola + mechanical
    box(S, 'par_n', 0, H + 0.55, -(d/2 - 0.15), w, 1.1, 0.3, PLASTER)
    box(S, 'par_s', 0, H + 0.55, d/2 - 0.15, w, 1.1, 0.3, PLASTER)
    box(S, 'par_e', w/2 - 0.15, H + 0.55, 0, 0.3, 1.1, d, PLASTER)
    box(S, 'par_w', -(w/2 - 0.15), H + 0.55, 0, 0.3, 1.1, d, PLASTER)
    for i3 in range(4):
        sx = -w*0.28 + i3 * (w*0.19)
        panel = trimesh.creation.box(extents=[2.0, 0.12, 2.6])
        panel.apply_transform(trimesh.transformations.rotation_matrix(-0.5, [1, 0, 0]))
        panel.apply_translation([sx, H + 0.9, -d*0.22])
        panel.visual = trimesh.visual.TextureVisuals(material=PBRMaterial(baseColorFactor=SOLARP, roughnessFactor=0.4))
        S.add_geometry(panel, node_name=f'solar{i3}')
        cyl(S, f'tank{i3}', sx, H + 1.55, -d*0.22 + 1.7, 0.5, 1.9, TANK, axis='x')
    box(S, 'perg1', w*0.24, H + 1.3, d*0.24, 6.5, 0.15, 5.0, TRUNK)
    for pi in range(3):
        cyl(S, f'pergp{pi}', w*0.24 - 2.6 + pi*2.6, H + 0.65, d*0.24 + 2.2, 0.14, 1.3, TRUNK)
        cyl(S, f'pergp2{pi}', w*0.24 - 2.6 + pi*2.6, H + 0.65, d*0.24 - 2.2, 0.14, 1.3, TRUNK)
    for sl in range(7):
        box(S, f'pslat{sl}', w*0.24 - 2.9 + sl*0.95, H + 1.42, d*0.24, 0.18, 0.1, 5.0, TRUNK)
    cyl(S, 'antenna', -w*0.3, H + 2.2, -d*0.3, 0.06, 2.6, PLASTER2)
    box(S, 'mech', -w*0.28, H + 0.8, d*0.26, 3.2, 1.6, 2.4, PLASTER2)
    # street furniture: low hedge along the sidewalk + two lamp posts
    box(S, 'hedge', 0, 0.5, sd*0.235, sw*0.8, 0.7, 0.9, GREEN)
    for li, lx in enumerate([-sw*0.3, sw*0.3]):
        cyl(S, f'lamp{li}', lx, 2.6, sd*0.3, 0.09, 5.2, PLASTER2)
        box(S, f'lamph{li}', lx, 5.3, sd*0.3 + 0.5, 0.28, 0.14, 1.1, GOLD)

    tris = sum(g.faces.shape[0] for g in S.geometry.values())
    S.export(out)
    print(f"wrote {out}: {len(S.geometry)} meshes, {tris} tris")

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1]))
    if spec.get('style') == 'standard':
        build_standard(spec, sys.argv[2])
    else:
        build(spec, sys.argv[2])
