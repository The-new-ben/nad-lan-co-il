# -*- coding: utf-8 -*-
"""Renders the example apartment's design styles (studio_kit.py; design system BuyJourney v78) as 360 rooms and cuts them
for the web next to the bare ones: living-<floor><dir>-<style>.jpg / -2k.jpg / -card.jpg.
  python scripts/interior/render_styles.py [floor 25] [dir w] [styles warm,light,stone] [width 3072] [samples 40] [threads 12]"""
import os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "rainbow", "tour")
TMP = os.path.join(HERE, "_renders")
a = sys.argv[1:]
FLOOR = a[0] if len(a) > 0 else "25"
D = a[1] if len(a) > 1 else "w"
STYLES = (a[2] if len(a) > 2 else "warm,light,stone").split(",")
WIDTH = a[3] if len(a) > 3 else "3072"
SAMPLES = a[4] if len(a) > 4 else "40"
THREADS = a[5] if len(a) > 5 else "12"
BEAR = {"w": 270, "n": 0, "e": 90, "s": 180}[D]
os.makedirs(TMP, exist_ok=True)
log = open(os.path.join(HERE, "render_styles.log"), "a", encoding="utf-8")
def say(m):
    log.write(time.strftime("%H:%M:%S ") + m + "\n"); log.flush(); print(m, flush=True)
for st in STYLES:
    name = "living-%s%s-%s" % (FLOOR, D, st)
    png = os.path.join(TMP, name + ".png")
    t0 = time.time()
    r = subprocess.run([BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "rainbow_interior.py"), "--",
                        png, FLOOR, str(BEAR), WIDTH, SAMPLES, "sunset", "living", st, THREADS], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(png):
        say("%s: RENDER FAILED %s %s" % (name, r.returncode, r.stderr[-300:])); continue
    c = subprocess.run([sys.executable, os.path.join(HERE, "cut_tour.py"), png, OUT, name], capture_output=True, text=True)
    say("%s: ok in %d s%s" % (name, time.time() - t0, "" if c.returncode == 0 else " | CUT FAILED " + c.stderr[-200:]))
say("done " + ",".join(STYLES))
