# -*- coding: utf-8 -*-
"""Kikar Hamedina: one tower at a time, turned through a full circle, for the page's apartment picker (HAD-712, 11.11.2026; Ben:
"each building turns on its own, and you choose the apartment on the building"). The real city of kikar_world.py stays around the
tower; the two other towers still light and shadow the scene but are not seen by the camera, so they never stand between the
visitor and a floor. Every picture is an illustration ("הדמיה להמחשה"), as kikar_world.py says.

  blender -b --factory-startup --python scripts/interior/kikar_turntable.py -- <out_base> <tower A|B|C> [frames 24] [width 756]
          [height 1080] [samples 48] [threads 14] [tod day]
  env KT_R (camera distance from the tower's centre line, m; 250), KT_H (camera height, m; 92), KT_TZ (the height looked at, m;
      81), KT_HFOV (horizontal field of view, degrees; 31), KT_ONLY="3,7" (render just these frames), KT_EXP (exposure offset).
Writes <out_base>-<tower>-<nn>.png per frame and <out_base>-<tower>.json: per frame the camera's bearing from the tower (the
facade that faces the visitor) and, per floor, the floor band on the picture: left edge, right edge and middle as 0..1 screen
points (x right, y down) at the floor's mid height. With the plate's bearing per floor (world.json: base_bearing, twist) the page
turns a tap into a floor and a facing side."""
import json
import math
import os
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kikar_world as KW  # noqa: E402

A = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUTB = os.path.abspath(A[0]) if A else os.path.join(HERE, "_renders", "kikar", "turn", "t")
KEY = A[1] if len(A) > 1 else "B"
N = int(A[2]) if len(A) > 2 else 24
WIDTH = int(A[3]) if len(A) > 3 else 756
HEIGHT = int(A[4]) if len(A) > 4 else 1080
SAMPLES = int(A[5]) if len(A) > 5 else 48
THREADS = int(A[6]) if len(A) > 6 else 14
TODN = A[7] if len(A) > 7 else "day"
R = float(os.environ.get("KT_R", "250"))
H = float(os.environ.get("KT_H", "92"))
TZ = float(os.environ.get("KT_TZ", "81"))
HFOV = float(os.environ.get("KT_HFOV", "31"))
ONLY = [int(x) for x in os.environ.get("KT_ONLY", "").split(",") if x.strip()]
EXPO = {"day": -3.4, "sunset": -2.9, "evening": -1.2}[TODN] + float(os.environ.get("KT_EXP", "0"))
os.makedirs(os.path.dirname(OUTB), exist_ok=True)

KW.init(WIDTH, HEIGHT, SAMPLES, THREADS)
KW.sky_params(TODN)
KW.load_world()
T = KW.W["towers"][KEY]
C = KW.tower_xy(T)
eye0 = Vector((C.x + R, C.y, H))
KW.build_sky(TODN)
KW.build_towers()
KW.build_blocks(eye0)
KW.build_ground(eye0)
KW.build_trees(eye0)
KW.build_cars(eye0)
KW.build_sun()
for ob in bpy.data.objects:  # the other two towers: still in the light, never in front of the camera
    if ob.name.startswith("tower") and not ob.name.startswith("tower" + KEY):
        ob.visible_camera = False

sc = bpy.context.scene
sc.view_settings.exposure = EXPO
KW.add_glare(3.5 / 2 ** EXPO, float(os.environ.get("KA_GLARE", "0.18")))
cd = bpy.data.cameras.new("turn")
cd.clip_start = 1.0
cd.clip_end = 90000.0
cd.lens_unit = "FOV"
cd.sensor_fit = "HORIZONTAL"
cd.angle = HFOV * math.pi / 180.0
cam = bpy.data.objects.new("turn", cd)
KW.link(cam)
sc.camera = cam

m = KW.W["model"]
FH, half, NEXP = m["fh"], T["side"] / 2, m.get("plate_n", 4.5)
outline = KW.plate_outline(half, NEXP, 72)
frames = []
for i in range(N):
    brg = 360.0 * i / N  # the camera stands at this bearing from the tower (from north, clockwise) and looks at it
    b = brg * math.pi / 180.0
    cam.location = Vector((C.x + R * math.sin(b), C.y + R * math.cos(b), H))
    cam.rotation_euler = (Vector((C.x, C.y, TZ)) - cam.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()
    rows = []
    for f in range(1, T["floors"] + 1):
        th = KW.plate_at(T, f)
        eu, ev = KW.dirv(th), KW.dirv(th + 90)
        z = (f - 0.5) * FH
        P = [world_to_camera_view(sc, cam, Vector((C.x + u * eu.x + v * ev.x, C.y + u * eu.y + v * ev.y, z))) for (u, v) in outline]
        lo, hi = min(P, key=lambda p: p.x), max(P, key=lambda p: p.x)
        mid = world_to_camera_view(sc, cam, Vector((C.x, C.y, z)))
        rows.append([round(lo.x, 4), round(1 - lo.y, 4), round(hi.x, 4), round(1 - hi.y, 4), round(mid.x, 4), round(1 - mid.y, 4)])
    name = "%s-%s-%02d" % (os.path.basename(OUTB), KEY, i)
    frames.append({"i": i, "bearing": round(brg, 2), "file": name + ".png", "floors": rows})
    if ONLY and i not in ONLY:
        continue
    out = os.path.join(os.path.dirname(OUTB), name + ".png")
    if os.path.exists(out) and not ONLY:
        print("HAVE", out)
        continue
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print("WROTE", out, flush=True)
json.dump({"about": "one tower turned through a circle: per frame the camera's bearing from the tower and each floor's band on the picture "
                    "[left x, left y, right x, right y, middle x, middle y], 0..1, x right, y down (scripts/interior/kikar_turntable.py)",
           "tower": KEY, "tod": TODN, "size": [WIDTH, HEIGHT], "floor_h": FH, "floors": T["floors"], "base_bearing": T["base_bearing"],
           "twist": m["twist"], "twist_dir": m["twist_dir"], "cam": {"r": R, "h": H, "tz": TZ, "hfov": HFOV}, "frames": frames},
          open(OUTB + "-" + KEY + ".json", "w"), separators=(",", ":"))
print("DONE", KEY, len(frames))
