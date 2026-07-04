#!/usr/bin/env python3
"""
NadLan approximate-massing generator (the model factory).

Build a grounded, ILLUSTRATIVE 3D massing GLB for a project from real-but-simple
facts (per-building floor counts, footprints, orientation, sea/landmark side) until
the developer's official BIM/GLB arrives. It does NOT invent architecture; it places
volumes at the real relative heights from data you feed it (e.g. scraped/entered from
Madlan or the developer site). Optionally drapes a fed facade photo as a texture so
the massing reads closer to the real building.

Usage:
    python3 scripts/generate-massing.py <spec.json> <out.glb>

spec.json shape:
{
  "floor_height_m": 3.2,
  "sea_side": "west",                       # west|east|north|south|null
  "buildings": [
    {"name":"tower","w":26,"d":26,"floors":35,"x":0,"z":0,"taper_top":0.12},
    {"name":"b16","w":30,"d":22,"floors":16,"x":34,"z":-6}
  ],
  "facade_photo": "assets/projects/<slug>/facade.jpg"   # optional, draped on tower
}

Honesty: output is labelled illustrative in the showroom. Swap the project's
model field for the official BIM/GLB when the developer provides it.
"""
import json, sys, os
import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial

CREAM = (0.86, 0.82, 0.74, 1.0)
GLASS = (0.74, 0.80, 0.82, 1.0)
SEA   = (0.66, 0.80, 0.82, 1.0)
GND   = (0.92, 0.90, 0.85, 1.0)

def building_mesh(b, fh, photo=None):
    h = float(b["floors"]) * fh
    w, d = float(b["w"]), float(b["d"])
    box = trimesh.creation.box(extents=(w, h, d))
    # optional gentle taper at the top (towers read better)
    taper = float(b.get("taper_top", 0))
    if taper > 0:
        v = box.vertices.copy()
        top = v[:, 1] > (h / 2 - 1e-6)
        v[top, 0] *= (1 - taper); v[top, 2] *= (1 - taper)
        box = trimesh.Trimesh(vertices=v, faces=box.faces, process=False)
    box.apply_translation((float(b["x"]), h / 2, float(b["z"])))
    if photo and os.path.isfile(photo) and b.get("name") == "tower":
        try:
            from PIL import Image
            img = Image.open(photo).convert("RGB")
            box.visual = trimesh.visual.TextureVisuals(
                uv=_box_uv(box), material=trimesh.visual.material.PBRMaterial(
                    baseColorTexture=img, roughnessFactor=0.6, metallicFactor=0.05))
            return box
        except Exception as e:
            print("texture skipped:", e)
    box.visual.material = PBRMaterial(baseColorFactor=CREAM, metallicFactor=0.05, roughnessFactor=0.6)
    return box

def _box_uv(mesh):
    # simple planar UV from XY bounds (good enough for an illustrative facade drape)
    v = mesh.vertices
    mn, mx = v.min(0), v.max(0)
    u = (v[:, 0] - mn[0]) / max(mx[0] - mn[0], 1e-6)
    w = (v[:, 1] - mn[1]) / max(mx[1] - mn[1], 1e-6)
    return np.column_stack([u, w])

def main(spec_path, out_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    fh = float(spec.get("floor_height_m", 3.2))
    photo = spec.get("facade_photo")
    meshes = [building_mesh(b, fh, photo) for b in spec["buildings"]]
    ground = trimesh.creation.box(extents=(240, 1, 220)); ground.apply_translation((0, -0.5, 0))
    ground.visual.material = PBRMaterial(baseColorFactor=GND, roughnessFactor=0.9)
    meshes.append(ground)
    side = spec.get("sea_side")
    if side:
        sea = trimesh.creation.box(extents=(60, 0.6, 220))
        off = {"west": (-140, 0), "east": (140, 0), "north": (0, -140), "south": (0, 140)}.get(side, (-140, 0))
        sea.apply_translation((off[0], -0.2, off[1]))
        sea.visual.material = PBRMaterial(baseColorFactor=SEA, metallicFactor=0.1, roughnessFactor=0.4)
        meshes.append(sea)
    trimesh.Scene(meshes).export(out_path)
    print("wrote", out_path, os.path.getsize(out_path), "bytes;",
          "buildings:", [(b["name"], b["floors"], f"{b['floors']*fh:.0f}m") for b in spec["buildings"]])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(1)
    main(sys.argv[1], sys.argv[2])
