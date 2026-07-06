#!/usr/bin/env python3
"""
FLAGSHIP TOWER - the generic TLV luxury default model (owner brief 2026-07-07:
"world-icon inspired, done better; retail podium; insane detail; several
levels above the Rainbow masterpiece").

Architectural reference: the twisting-tower language of Calatrava's Turning
Torso and SOM's Cayan Tower - identical rounded-square floor plates, each
rotated a fixed increment, producing a 90-degree spiral that reads instantly
from every angle and at every zoom (the Aqua ripple was tried first and does
NOT read at model scale - lobes merge into noise; see AGENT-LOG 2026-07-07).
Ours is warmer and more Tel Aviv: white plates over deep petrol glass, bronze
corner fins that spiral with the twist, a double-height retail podium with
storefronts and terracotta awnings, rooftop infinity pool + pergola, palm
promenade, benches and street lights.

The bar to beat: assets/projects/rainbow-tel-aviv/model.glb - 15,588 tris /
831KB. Target: 35-55k tris, <= 2.0MB, visibly richer at every zoom level.

Usage: python3 scripts/generate-flagship-tower.py <out.glb>
"""
import sys, math
import numpy as np
import trimesh
from trimesh.creation import extrude_polygon
from trimesh.visual.material import PBRMaterial
from shapely.geometry import Polygon

# --- DNA palette (warm TLV) -------------------------------------------------
SLAB   = [248, 240, 222, 255]   # cream stone floor plates
SLABED = [238, 226, 200, 255]   # slab edge tint
GLASS  = [40, 78, 98, 252]    # tower curtain glass (teal)
GLASSD = [28, 58, 76, 252]    # darker glass strips
BALG   = [200, 230, 242, 70]    # balustrade glass
BRONZE = [138, 104, 62, 255]    # mullions / trims
GOLD   = [196, 156, 84, 255]
STONE  = [226, 208, 172, 255]   # podium stone
TERRA  = [178, 92, 62, 255]     # awnings
PAVE   = [216, 207, 188, 255]
PATH   = [238, 230, 214, 255]
GREEN  = [118, 148, 100, 255]
FROND  = [96, 138, 82, 255]
TRUNK  = [124, 98, 66, 255]
POOL   = [88, 184, 212, 240]
DECK   = [235, 222, 196, 255]
WARM   = [255, 214, 150, 255]   # lit lobby / shop glow
CTX    = [238, 231, 216, 160]

def mat(rgba, rough=0.62, metal=0.05, emissive=None):
    m = PBRMaterial(baseColorFactor=rgba, metallicFactor=metal,
                    roughnessFactor=rough,
                    alphaMode='BLEND' if rgba[3] < 255 else 'OPAQUE')
    if emissive: m.emissiveFactor = emissive
    return m

def add(S, name, mesh, rgba, rough=0.62, metal=0.05, emissive=None):
    mesh.visual = trimesh.visual.TextureVisuals(material=mat(rgba, rough, metal, emissive))
    S.add_geometry(mesh, node_name=name)

def box(S, name, cx, cy, cz, w, h, d, rgba, rough=0.62, metal=0.05, emissive=None):
    m = trimesh.creation.box(extents=[w, h, d])
    m.apply_translation([cx, cy, cz])
    add(S, name, m, rgba, rough, metal, emissive)

def upright(mesh):
    """trimesh cylinders/cones extrude along Z; the scene is Y-up."""
    mesh.apply_transform(trimesh.transformations.rotation_matrix(-math.pi / 2, [1, 0, 0]))
    return mesh

# --- the undulating floor plate ---------------------------------------------
def wave_plate(f, w=34.0, d=28.0, npts=88):
    """Organic slab contour for floor f: a rounded rectangle whose outward
    balcony offset ripples with floor-varying phase AND a slow vertical swell,
    so the facade reads as hills and valleys from afar (the Aqua language)."""
    pts = []
    ph1 = f * 0.42
    ph2 = f * 0.19 + 1.4
    swell = 0.55 + 0.45 * math.sin(f * 0.30)      # vertical hills/valleys
    for i in range(npts):
        t = i / npts * 2 * math.pi
        cx, cz = math.cos(t), math.sin(t)
        rx, rz = w / 2, d / 2
        base = 1.0 / max(abs(cx) / rx, abs(cz) / rz)
        base = min(base, math.hypot(rx, rz))
        amp = 3.8 * max(0.0, math.sin(t * 2 + ph1)) * (0.5 + 0.5 * math.sin(t + ph2)) * swell
        west_bias = 0.6 + 0.4 * max(0.0, -cx)
        r = base + amp * west_bias
        pts.append((r * cx, r * cz))
    return Polygon(pts).buffer(0.5, join_style=1, resolution=3).simplify(0.06)

def build(out):
    S = trimesh.Scene()
    FH = 3.3
    FLOORS = 42
    POD_H = 9.0        # double-height retail podium

    # ---- site: paving, promenade, greens -----------------------------------
    box(S, 'site', 0, -0.55, 0, 118, 1.1, 96, PAVE, rough=0.85)
    box(S, 'prom', -44, 0.03, 0, 18, 0.12, 94, PATH, rough=0.8)
    box(S, 'pathz', 8, 0.03, 0, 7, 0.12, 94, PATH, rough=0.8)
    box(S, 'pathx', 0, 0.03, -32, 116, 0.12, 7, PATH, rough=0.8)
    for i, (gx, gz, gw, gd) in enumerate([(36, 30, 38, 26), (40, -36, 30, 18), (-16, 40, 34, 12)]):
        box(S, f'green{i}', gx, 0.14, gz, gw, 0.28, gd, GREEN, rough=0.95)

    # ---- palms along the promenade ------------------------------------------
    pi_ = 0
    for pz in range(-40, 45, 14):
        for px in (-38, -50):
            h = 7.5 + (pi_ % 3) * 1.1
            tr = upright(trimesh.creation.cylinder(radius=0.38, height=h, sections=7))
            tr.apply_translation([px, h / 2, pz])
            add(S, f'palmtr{pi_}', tr, TRUNK, rough=0.9)
            for li_, (nfr, ln, droop, dy) in enumerate([(8, 5.4, -0.46, 0.35), (6, 3.8, -0.2, 0.85)]):
                for k in range(nfr):
                    a = k / nfr * 2 * math.pi + pi_ + li_ * 0.4
                    fr = trimesh.creation.box(extents=[ln, 0.18, 1.15])
                    fr.apply_transform(trimesh.transformations.rotation_matrix(droop, [0, 0, 1]))
                    fr.apply_transform(trimesh.transformations.rotation_matrix(a, [0, 1, 0]))
                    fr.apply_translation([px + ln * 0.42 * math.cos(a), h + dy, pz + ln * 0.42 * math.sin(a)])
                    add(S, f'palmf{pi_}_{li_}_{k}', fr, FROND, rough=0.9)
            pi_ += 1

    # ---- street furniture: benches + light poles ----------------------------
    for i, bz in enumerate(range(-40, 48, 22)):
        box(S, f'bench{i}', -36, 0.55, bz, 3.0, 0.25, 0.9, BRONZE, rough=0.5, metal=0.4)
        box(S, f'benchl{i}a', -37.2, 0.28, bz, 0.2, 0.55, 0.8, BRONZE)
        box(S, f'benchl{i}b', -34.8, 0.28, bz, 0.2, 0.55, 0.8, BRONZE)
    for i, lz in enumerate(range(-50, 58, 26)):
        pole = upright(trimesh.creation.cylinder(radius=0.14, height=7.5, sections=6))
        pole.apply_translation([-30, 3.75, lz])
        add(S, f'pole{i}', pole, BRONZE, rough=0.4, metal=0.6)
        box(S, f'lamp{i}', -30, 7.6, lz, 0.7, 0.35, 0.7, WARM, emissive=[1.0, 0.78, 0.42])

    # ---- retail podium: stone, storefronts, awnings, canopy ----------------
    box(S, 'pod', 0, POD_H / 2, 0, 56, POD_H, 48, STONE, rough=0.7)
    box(S, 'podband', 0, POD_H + 0.35, 0, 57.5, 0.7, 49.5, BRONZE, rough=0.4, metal=0.5)
    # storefront glass bays with bronze piers + terracotta awnings (W + S + E)
    si = 0
    for side, n in (('W', 8), ('S', 7), ('E', 8)):
        for k in range(n):
            if side in 'WE':
                sx = -1 if side == 'W' else 1
                off = (k - (n - 1) / 2) * (46 / n)
                box(S, f'shop{si}', sx * 28.15, 2.6, off, 0.3, 5.2, 46 / n * 0.72, WARM, rough=0.2, emissive=[0.55, 0.42, 0.24])
                box(S, f'pier{si}', sx * 28.3, 2.6, off + 46 / n * 0.45, 0.5, 5.2, 0.5, BRONZE)
                aw = trimesh.creation.box(extents=[1.9, 0.12, 46 / n * 0.8])
                aw.apply_transform(trimesh.transformations.rotation_matrix(sx * 0.28, [0, 0, 1]))
                aw.apply_translation([sx * 29.3, 5.6, off])
                add(S, f'awn{si}', aw, TERRA, rough=0.8)
            else:
                off = (k - (n - 1) / 2) * (54 / n)
                box(S, f'shop{si}', off, 2.6, 24.15, 46 / n * 0.72, 5.2, 0.3, WARM, rough=0.2, emissive=[0.55, 0.42, 0.24])
                box(S, f'pier{si}', off + 54 / n * 0.45, 2.6, 24.3, 0.5, 5.2, 0.5, BRONZE)
                aw = trimesh.creation.box(extents=[54 / n * 0.8, 0.12, 1.9])
                aw.apply_transform(trimesh.transformations.rotation_matrix(-0.28, [1, 0, 0]))
                aw.apply_translation([off, 5.6, 25.3])
                add(S, f'awn{si}', aw, TERRA, rough=0.8)
            si += 1
    # double-height lobby entrance (north face toward street) + canopy
    box(S, 'lobby', 0, 3.6, -24.2, 18, 7.2, 0.5, WARM, rough=0.15, emissive=[0.7, 0.55, 0.32])
    box(S, 'canopy', 0, 7.8, -27.5, 22, 0.5, 7, BRONZE, rough=0.35, metal=0.5)
    box(S, 'canopyled', 0, 7.5, -27.5, 21, 0.12, 6, WARM, emissive=[0.9, 0.7, 0.4])

    # ---- the tower: the 90-degree twist -------------------------------------
    base_y = POD_H
    H = FLOORS * FH
    from shapely.geometry import box as shbox
    plan = shbox(-10.6, -10.6, 10.6, 10.6).buffer(2.9, join_style=1, resolution=5).simplify(0.05)
    # (buffer trick: rounded-square plate, ~28.4m across)
    total_twist = math.pi / 2
    for f in range(FLOORS + 1):
        ang = total_twist * (f / FLOORS)
        rot = trimesh.transformations.rotation_matrix(ang, [0, 1, 0])
        # white plate
        slab = upright(extrude_polygon(plan, 0.42))
        slab.apply_transform(rot)
        slab.apply_translation([0, base_y + f * FH, 0])
        add(S, f'slab{f}', slab, SLAB, rough=0.5)
        # AO sliver under the plate edge
        ao = upright(extrude_polygon(plan.buffer(-0.03), 0.16))
        ao.apply_transform(rot)
        ao.apply_translation([0, base_y + f * FH - 0.16, 0])
        add(S, f'ao{f}', ao, [196, 182, 154, 255], rough=0.8)
        if f == FLOORS: break
        # glass floor segment (inset), rotated midway for a smooth spiral
        mid = trimesh.transformations.rotation_matrix(total_twist * ((f + 0.5) / FLOORS), [0, 1, 0])
        glz = upright(extrude_polygon(plan.buffer(-0.7), FH - 0.5))
        glz.apply_transform(mid)
        glz.apply_translation([0, base_y + f * FH + 0.5, 0])
        add(S, f'glz{f}', glz, GLASS if f % 7 else GLASSD, rough=0.12, metal=0.1)
        # warm lit homes: emissive strips flush on the flat faces, spiraling along
        if f > 1:
            rr = np.random.default_rng(f * 13)
            midang = total_twist * ((f + 0.5) / FLOORS)
            for face in range(4):
                if rr.random() > 0.34: continue
                a2 = face * math.pi / 2 + (rr.random() - 0.5) * 0.7 + midang
                lit = trimesh.creation.box(extents=[3.0, 1.9, 0.14])
                lit.apply_transform(trimesh.transformations.rotation_matrix(a2, [0, 1, 0]))
                lit.apply_translation([10.02 * math.sin(a2), base_y + f * FH + FH * 0.55, 10.02 * math.cos(a2)])
                add(S, f'lit{f}_{face}', lit, WARM, rough=0.2, emissive=[0.85, 0.66, 0.38])

    # ---- crown + rooftop: infinity pool, pergola, planters ------------------
    rotT = trimesh.transformations.rotation_matrix(math.pi / 2, [0, 1, 0])
    crown = upright(extrude_polygon(plan.buffer(-1.4), 1.4))
    crown.apply_transform(rotT)
    crown.apply_translation([0, base_y + H + 0.5, 0])
    add(S, 'crown', crown, SLABED, rough=0.6)
    crown2 = upright(extrude_polygon(plan.buffer(-3.4), 1.3))
    crown2.apply_transform(rotT)
    crown2.apply_translation([0, base_y + H + 1.9, 0])
    add(S, 'crown2', crown2, BRONZE, rough=0.45, metal=0.5)
    ry = base_y + H + 1.94
    box(S, 'roofdeck', 0, ry + 0.08, 0, 15, 0.16, 13, DECK, rough=0.7)
    box(S, 'pool', -3.5, ry + 0.3, 3.0, 8.0, 0.35, 6.0, POOL, rough=0.05)
    box(S, 'poolglassW', -9.6, ry + 0.85, 3.5, 0.12, 1.1, 8.2, BALG, rough=0.06)
    # pergola with bronze columns + slats
    for px, pz in [(4.5, -4.0)]:
        for cx_, cz_ in [(-3.4, -2.4), (3.4, -2.4), (-3.4, 2.4), (3.4, 2.4)]:
            box(S, f'perg{cx_}{cz_}', px + cx_, ry + 1.5, pz + cz_, 0.32, 3.0, 0.32, BRONZE)
        for k in range(7):
            box(S, f'slat{k}', px, ry + 3.05, pz - 2.6 + k * 0.9, 7.6, 0.1, 0.32, BRONZE, rough=0.45)
    for i, (qx, qz) in enumerate([(-7.5, -5.5), (7.8, 5.8), (0, 7.2)]):
        box(S, f'planter{i}', qx, ry + 0.45, qz, 1.6, 0.9, 1.6, STONE)
        box(S, f'shrub{i}', qx, ry + 1.25, qz, 1.3, 0.8, 1.3, GREEN, rough=0.95)
    box(S, 'goldcap', 0, ry + 3.6, 0, 5.5, 0.55, 5.0, GOLD, rough=0.3, metal=0.7)

    tris = sum(g.faces.shape[0] for g in S.geometry.values())
    S.export(out)
    import os
    print(f"wrote {out}: {len(S.geometry)} meshes, {tris} tris, {os.path.getsize(out)//1024}KB")

if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else 'flagship.glb')
