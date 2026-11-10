# -*- coding: utf-8 -*-
"""Kikar Hamedina from the air: the real city of kikar_world.py (every building within 2 km at its surveyed height, the 2024
canopy, the streets, the sea, the Yarkon, the three towers floor by floor) seen from outside, for the page's first screen and
the photoreal orbit (HAD-699, 10.11.2026). Every picture is an illustration ("הדמיה להמחשה"): the facades, the ground and the
tree shapes are procedural, as kikar_world.py says.

  blender -b --factory-startup --python scripts/interior/kikar_aerial.py -- <out_base> [tod day|sunset|evening] [width 1600]
          [height 1000] [samples 64] [threads 14]
  env KA_CAMS="name:x,y,z,tx,ty,tz,hfov;..."  world metres (X east, Y north, Z up, 0,0 = the plot centre); one render each,
          written to <out_base>-<name>.png. KA_EXP: an exposure offset. KA_ORBIT="n,radius,height,tz,hfov[,start_deg]": n frames
          on a circle around the square (bearing from north, clockwise), written as <out_base>-o00.png ...; each frame's camera
          matrix and the projected screen points of the three towers' floors go to <out_base>-orbit.json, so the page can draw
          a floor or an apartment over the picture.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kikar_world as KW  # noqa: E402

A = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUTB = os.path.abspath(A[0]) if A else os.path.join(HERE, "_renders", "kikar", "aerial")
TODN = A[1] if len(A) > 1 else "day"
WIDTH = int(A[2]) if len(A) > 2 else 1600
HEIGHT = int(A[3]) if len(A) > 3 else 1000
SAMPLES = int(A[4]) if len(A) > 4 else 64
THREADS = int(A[5]) if len(A) > 5 else 14
EXPO = {"day": -3.4, "sunset": -2.9, "evening": -1.2}[TODN] + float(os.environ.get("KA_EXP", "0"))

KW.init(WIDTH, HEIGHT, SAMPLES, THREADS)
KW.sky_params(TODN)
KW.load_world()

cams = []
for item in [x for x in os.environ.get("KA_CAMS", "").split(";") if x.strip()]:
    nm, vals = item.split(":")
    v = [float(x) for x in vals.split(",")]
    cams.append((nm, Vector(v[0:3]), Vector(v[3:6]), v[6] if len(v) > 6 else 50.0))
orbit = os.environ.get("KA_ORBIT")
if orbit:
    p = [float(x) for x in orbit.split(",")]
    n, rad, hgt, tz, hfov = int(p[0]), p[1], p[2], p[3], p[4]
    start = p[5] if len(p) > 5 else 0.0
    for i in range(n):
        b = (start + 360.0 * i / n) * math.pi / 180.0
        cams.append(("o%02d" % i, Vector((rad * math.sin(b), rad * math.cos(b), hgt)), Vector((0.0, 0.0, tz)), hfov))
if not cams:
    cams = [("hero", Vector((520.0, -620.0, 330.0)), Vector((-120.0, 140.0, 45.0)), 48.0)]

# the level of detail follows the first camera (all cameras of one run sit at a similar distance)
eye = cams[0][1]
KW.build_sky(TODN)
KW.build_towers()
KW.build_blocks(eye)
KW.build_ground(eye)
KW.build_trees(eye)
KW.build_cars(eye)
KW.build_sun()

sc = bpy.context.scene
sc.view_settings.exposure = EXPO
KW.add_glare(3.5 / 2 ** EXPO, float(os.environ.get("KA_GLARE", "0.18")))
cd = bpy.data.cameras.new("aerial")
cd.clip_start = 1.0
cd.clip_end = 90000.0
cd.lens_unit = "FOV"
cd.sensor_fit = "HORIZONTAL"
cam = bpy.data.objects.new("aerial", cd)
KW.link(cam)
sc.camera = cam

# the floors to project for the page: each tower's centre line at every floor's mid height
fh = KW.W["model"]["fh"]
proj = {"towers": {}}
for k, t in KW.W["towers"].items():
    proj["towers"][k] = {"floors": int(t.get("floors", 40)), "xy": list(KW.tower_xy(t))[:2]}

from bpy_extras.object_utils import world_to_camera_view  # noqa: E402

frames = []
for nm, loc, tgt, hfov in cams:
    cd.angle = hfov * math.pi / 180.0
    cam.location = loc
    cam.rotation_euler = (tgt - loc).to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()
    out = OUTB + "-" + nm + ".png"
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    pts = {}
    for k, t in proj["towers"].items():
        c = KW.tower_xy(KW.W["towers"][k])
        row = []
        for f in range(1, t["floors"] + 1):
            p = world_to_camera_view(sc, cam, Vector((c.x, c.y, (f - 0.5) * fh)))
            row.append([round(p.x, 4), round(1 - p.y, 4), round(p.z, 1)])
        pts[k] = row
    frames.append({"name": nm, "file": os.path.basename(out), "loc": list(loc), "target": list(tgt), "hfov": hfov, "towers": pts})
    print("WROTE", out)
json.dump({"tod": TODN, "size": [WIDTH, HEIGHT], "floor_h": fh, "frames": frames}, open(OUTB + "-frames.json", "w"), indent=1)
print("DONE", len(frames))
