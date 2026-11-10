# -*- coding: utf-8 -*-
"""The view from every floor (HAD-699, 10.11.2026): the window view of kikar_interior.py's "view" shot (the same frame as the
twist strip) for each tower, each of the plate's four sides and a ladder of floors, by day. The page's apartment cockpit shows
the rendered floor nearest to the chosen one and says which floor it is. Every picture is an illustration ("הדמיה להמחשה").

  python scripts/interior/render_kikar_views.py [towers ABC] [floors 5,10,15,20,25,30,35,40] [sides 0,90,180,270]
         [width 1280] [samples 48] [threads 14]

Output: docs/research/2026-11-10-kikar-showcase/views/<tower><floor>-<side>.jpg (+ -640.jpg) and views.json (the APARTMENT
and CAMERA lines Blender prints: the facing bearing, the eye height). Skips a picture that already exists. Waits while another
Blender runs (renders share this machine). Progress: scripts/interior/render_kikar_views.log."""
import json
import os
import subprocess
import sys
import time

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUT = os.path.join(REPO, "docs", "research", "2026-11-10-kikar-showcase", "views")
TMP = os.path.join(HERE, "_renders", "kikar", "views")
a = sys.argv[1:]
TOWERS = a[0] if len(a) > 0 else "ABC"
FLOORS = [int(x) for x in (a[1] if len(a) > 1 else "5,10,15,20,25,30,35,40").split(",")]
SIDES = [int(x) for x in (a[2] if len(a) > 2 else "0,90,180,270").split(",")]
WIDTH = int(a[3]) if len(a) > 3 else 1280
SAMPLES = a[4] if len(a) > 4 else "48"
THREADS = a[5] if len(a) > 5 else "14"
TOP = {"A": 40, "B": 37, "C": 40}
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)
log = open(os.path.join(HERE, "render_kikar_views.log"), "a", encoding="utf-8")
idx_path = os.path.join(OUT, "views.json")
index = json.load(open(idx_path, encoding="utf-8")) if os.path.exists(idx_path) else {}


def say(m):
    log.write(time.strftime("%H:%M:%S ") + m + "\n")
    log.flush()
    print(m, flush=True)


def blender_running():
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq blender.exe", "/NH"], capture_output=True, text=True)
    return "blender.exe" in r.stdout.lower()


for t in TOWERS:
    for f in FLOORS:
        f = min(f, TOP[t])
        for s in SIDES:
            name = "%s%d-%d" % (t, f, s)
            jpg = os.path.join(OUT, name + ".jpg")
            if os.path.exists(jpg):
                continue
            while blender_running():
                time.sleep(30)
            png = os.path.join(TMP, name + ".png")
            e = dict(os.environ)
            e.update({"KH_TOWER": t, "KH_FLOOR": str(f), "KH_SIDE": str(s)})
            t0 = time.time()
            r = subprocess.run([BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "kikar_interior.py"), "--",
                                png, "view", "day", str(WIDTH), str(round(WIDTH * 9 / 16)), SAMPLES, THREADS],
                               capture_output=True, text=True, env=e, encoding="utf-8", errors="replace")
            info = [ln for ln in r.stdout.splitlines() if ln.startswith(("APARTMENT", "CAMERA"))]
            if r.returncode != 0 or not os.path.exists(png):
                say("%s: RENDER FAILED %s %s" % (name, r.returncode, (r.stderr or r.stdout)[-400:]))
                continue
            im = Image.open(png).convert("RGB")
            im.save(jpg, "JPEG", quality=84, optimize=True, progressive=True)
            im.resize((640, 360), Image.LANCZOS).save(os.path.join(OUT, name + "-640.jpg"), "JPEG", quality=80, optimize=True, progressive=True)
            index[name] = {"tower": t, "floor": f, "side": s, "info": info}
            json.dump(index, open(idx_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            say("%s: ok in %d s | %s" % (name, time.time() - t0, " | ".join(info)))
say("done")
