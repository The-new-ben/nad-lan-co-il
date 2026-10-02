# -*- coding: utf-8 -*-
"""Renders the Kikar Hamedina example apartment's 360 living room (kikar_interior.py: tower C, floor 30, facing west, at
sunset) in the design styles (studio_kit.py's palettes, kikar_interior.py's style argument; the same three as Rainbow's
render_styles.py) and cuts each for the web next to the bare 360 with cut_kikar_tour.py --pano:
  plugins/nadlan-config/assets/project-stage/hamedina/tour/living360-c30w-sunset-<style>[.jpg|.webp|-2k.jpg|-2k.webp|
  -card.jpg|-thumb.webp]
The same parameters as the bare 360 (render_kikar_proto.py: 4096 x 2048, 96 samples); the renders stay in
scripts/interior/_renders/kikar/living360-c30w-sunset-<style>.png (not committed).
  python scripts/interior/render_kikar_styles.py [styles warm,light,stone] [samples 96] [threads 12] [--no-cut]
Waits while another Blender runs (other renders share this machine). Progress: scripts/interior/render_kikar_styles.log."""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
TMP = os.path.join(HERE, "_renders", "kikar")
a = [x for x in sys.argv[1:] if not x.startswith("--")]
STYLES = (a[0] if len(a) > 0 else "warm,light,stone").split(",")
SAMPLES = a[1] if len(a) > 1 else "96"
THREADS = a[2] if len(a) > 2 else "12"
CUT = "--no-cut" not in sys.argv
W, H = 4096, 2048
os.makedirs(TMP, exist_ok=True)
log = open(os.path.join(HERE, "render_kikar_styles.log"), "a", encoding="utf-8")


def say(m):
    log.write(time.strftime("%Y-%m-%d %H:%M:%S ") + m + "\n")
    log.flush()
    print(m, flush=True)


def blender_running():
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq blender.exe", "/NH"], capture_output=True, text=True)
    return "blender.exe" in r.stdout.lower()


say("start: styles %s, %d x %d, %s samples, %s threads, living360 sunset" % (",".join(STYLES), W, H, SAMPLES, THREADS))
for st in STYLES:
    while blender_running():
        time.sleep(60)
    name = "living360-c30w-sunset-" + st
    png = os.path.join(TMP, name + ".png")
    t0 = time.time()
    r = subprocess.run([BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "kikar_interior.py"), "--",
                        png, "living360", "sunset", str(W), str(H), SAMPLES, THREADS, st], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    info = [ln for ln in r.stdout.splitlines() if ln.startswith(("APARTMENT", "SUN", "CAMERA", "STYLE"))]
    if r.returncode != 0 or not os.path.exists(png):
        say("%s: RENDER FAILED %s %s" % (name, r.returncode, (r.stderr or r.stdout)[-600:]))
        continue
    say("%s: rendered in %d s | %s" % (name, time.time() - t0, " | ".join(info)))
    if CUT:
        c = subprocess.run([sys.executable, os.path.join(HERE, "cut_kikar_tour.py"), "--pano", png, name], capture_output=True, text=True)
        say("%s: cut %s" % (name, "ok" if c.returncode == 0 else "FAILED " + c.stderr[-300:]))
say("done: " + ",".join(STYLES))
