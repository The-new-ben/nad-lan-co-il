# -*- coding: utf-8 -*-
"""Renders the P9b prototype of the Kikar Hamedina example apartment (kikar_interior.py: tower C, floor 30, facing west)
and saves the web cuts into docs/research/2026-09-30-kikar-hamedina/interiors-proto/.
  python scripts/interior/render_kikar_proto.py [items all | living-sunset,bedroom-day,...] [still samples 160]
         [360 samples 96] [threads 14]
Stills: 2048 x 1152 (JPG q88, and a 1200 px card). The 360: 4096 x 2048 equirectangular, cut by cut_tour.py exactly as the
fleet's tour pictures (<name>.jpg 4096, -2k.jpg, -card.jpg). The twist strip: the same frame on floors 20, 30 and 38.
Waits while another Blender runs (other renders share this machine). Progress: scripts/interior/render_kikar_proto.log."""
import os
import subprocess
import sys
import time

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUT = os.path.join(REPO, "docs", "research", "2026-09-30-kikar-hamedina", "interiors-proto")
TMP = os.path.join(HERE, "_renders", "kikar")
a = sys.argv[1:]
ITEMS = a[0] if len(a) > 0 else "all"
S_STILL = a[1] if len(a) > 1 else "160"
S_360 = a[2] if len(a) > 2 else "96"
THREADS = a[3] if len(a) > 3 else "14"

# name, shot, time of day, width, height, samples, extra environment
ALL = [
    ("living-sunset", "living", "sunset", 2048, 1152, S_STILL, {}),
    ("bedroom-day", "bedroom", "day", 2048, 1152, S_STILL, {}),
    ("balcony-sunset", "balcony", "sunset", 2048, 1152, S_STILL, {}),
    ("living-day", "living3q", "day", 2048, 1152, S_STILL, {}),
    # evening v2 (1.10.2026) replaces "living-evening" (19:06, rejected; its files stay as they were)
    ("living-evening-v2", "living_eve", "evening", 2048, 1152, S_STILL, {}),
    ("living360-sunset", "living360", "sunset", 4096, 2048, S_360, {}),
    ("twist-floor20", "view", "day", 1280, 720, "48", {"KH_FLOOR": "20"}),
    ("twist-floor30", "view", "day", 1280, 720, "48", {"KH_FLOOR": "30"}),
    ("twist-floor38", "view", "day", 1280, 720, "48", {"KH_FLOOR": "38"}),
]
todo = ALL if ITEMS == "all" else [x for x in ALL if x[0] in ITEMS.split(",")]
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)
log = open(os.path.join(HERE, "render_kikar_proto.log"), "a", encoding="utf-8")


def say(m):
    log.write(time.strftime("%H:%M:%S ") + m + "\n")
    log.flush()
    print(m, flush=True)


def blender_running():
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq blender.exe", "/NH"], capture_output=True, text=True)
    return "blender.exe" in r.stdout.lower()


for name, shot, tod, w, h, samples, env in todo:
    while blender_running():
        time.sleep(60)
    png = os.path.join(TMP, "final-%s.png" % name)
    t0 = time.time()
    e = dict(os.environ)
    e.update(env)
    r = subprocess.run([BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "kikar_interior.py"), "--",
                        png, shot, tod, str(w), str(h), str(samples), THREADS], capture_output=True, text=True, env=e,
                       encoding="utf-8", errors="replace")
    info = [ln for ln in r.stdout.splitlines() if ln.startswith(("APARTMENT", "SUN", "CAMERA"))]
    if r.returncode != 0 or not os.path.exists(png):
        say("%s: RENDER FAILED %s %s" % (name, r.returncode, (r.stderr or r.stdout)[-600:]))
        continue
    if shot == "living360":
        c = subprocess.run([sys.executable, os.path.join(HERE, "cut_tour.py"), png, OUT, name], capture_output=True, text=True)
        say("%s: cut %s" % (name, "ok" if c.returncode == 0 else c.stderr[-300:]))
    else:
        im = Image.open(png).convert("RGB")
        im.save(os.path.join(OUT, name + ".jpg"), "JPEG", quality=88, optimize=True, progressive=True)
        im.resize((1200, round(1200 * im.height / im.width)), Image.LANCZOS).save(
            os.path.join(OUT, name + "-1200.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
    say("%s: ok in %d s | %s" % (name, time.time() - t0, " | ".join(info)))
say("done: " + ",".join(x[0] for x in todo))
