# -*- coding: utf-8 -*-
"""The living room in 360 from every apartment (HAD-699, 10.11.2026, Ben: "complete Kikar seriously"): kikar_interior.py's
"living360" shot (the example apartment's living room, its layout and furniture an illustration) placed in each tower, on a
ladder of floors, facing each of the plate's four sides, by day. The cockpit's "בפנים · 360°" tile then shows the living room
with THAT apartment's real window view (the city around it at the floor's true height). Every picture is "הדמיה להמחשה".

  python scripts/interior/render_kikar_360s.py [towers ABC] [floors 10,20,30,38] [sides 0,90,180,270] [width 2048]
         [samples 64] [threads 14]

Output: docs/research/2026-11-10-kikar-showcase/living360/<tower><floor>-<side>.jpg and index.json (Blender's APARTMENT and
CAMERA lines). Skips a picture that exists; waits while another Blender runs. Progress: scripts/interior/render_kikar_360s.log."""
import json
import os
import subprocess
import sys
import time

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUT = os.path.join(REPO, "docs", "research", "2026-11-10-kikar-showcase", "living360")
TMP = os.path.join(HERE, "_renders", "kikar", "living360")
a = sys.argv[1:]
TOWERS = a[0] if len(a) > 0 else "ABC"
FLOORS = [int(x) for x in (a[1] if len(a) > 1 else "10,20,30,38").split(",")]
SIDES = [int(x) for x in (a[2] if len(a) > 2 else "0,90,180,270").split(",")]
WIDTH = int(a[3]) if len(a) > 3 else 2048
SAMPLES = a[4] if len(a) > 4 else "64"
THREADS = a[5] if len(a) > 5 else "14"
TOP = {"A": 40, "B": 37, "C": 40}
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)
log = open(os.path.join(HERE, "render_kikar_360s.log"), "a", encoding="utf-8")
idx_path = os.path.join(OUT, "index.json")
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
                                png, "living360", "day", str(WIDTH), str(WIDTH // 2), SAMPLES, THREADS],
                               capture_output=True, text=True, env=e, encoding="utf-8", errors="replace")
            info = [ln for ln in r.stdout.splitlines() if ln.startswith(("APARTMENT", "CAMERA"))]
            if r.returncode != 0 or not os.path.exists(png):
                say("%s: RENDER FAILED %s %s" % (name, r.returncode, (r.stderr or r.stdout)[-400:]))
                continue
            Image.open(png).convert("RGB").save(jpg, "JPEG", quality=86, optimize=True, progressive=True)
            index[name] = {"tower": t, "floor": f, "side": s, "info": info}
            json.dump(index, open(idx_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            say("%s: ok in %d s | %s" % (name, time.time() - t0, " | ".join(info)))
say("done")
