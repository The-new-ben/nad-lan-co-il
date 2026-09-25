# -*- coding: utf-8 -*-
"""Renders the example apartment's 360 views on more floors (the owner, 25.9: "get inside" from any floor), in the four
directions, in the living room and on the balcony, then cuts them for the web next to floor 25's.
  python scripts/interior/render_floors.py [floors, default 10,36] [width, default 3072] [samples, default 40]
Blender 5.2 Cycles on the CPU; each view takes a few minutes. Progress: scripts/interior/render_floors.log."""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "rainbow", "tour")
TMP = os.path.join(HERE, "_renders")
FLOORS = [int(x) for x in (sys.argv[1] if len(sys.argv) > 1 else "10,36").split(",")]
WIDTH = sys.argv[2] if len(sys.argv) > 2 else "3072"
SAMPLES = sys.argv[3] if len(sys.argv) > 3 else "40"
DIRS = (("w", 270), ("n", 0), ("e", 90), ("s", 180))
os.makedirs(TMP, exist_ok=True)
log = open(os.path.join(HERE, "render_floors.log"), "a", encoding="utf-8")


def say(msg):
    log.write(time.strftime("%H:%M:%S ") + msg + "\n")
    log.flush()


for floor in FLOORS:
    for d, bearing in DIRS:
        for spot in ("living", "balcony"):
            name = f"{spot}-{floor}{d}"
            if os.path.exists(os.path.join(OUT, name + "-2k.jpg")):
                say(f"{name}: already there")
                continue
            png = os.path.join(TMP, name + ".png")
            t0 = time.time()
            r = subprocess.run([BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "rainbow_interior.py"), "--",
                                png, str(floor), str(bearing), WIDTH, SAMPLES, "sunset", spot], capture_output=True, text=True)
            if r.returncode != 0 or not os.path.exists(png):
                say(f"{name}: RENDER FAILED {r.returncode} {r.stderr[-300:]}")
                continue
            c = subprocess.run([sys.executable, os.path.join(HERE, "cut_tour.py"), png, OUT, name], capture_output=True, text=True)
            say(f"{name}: {'ok' if c.returncode == 0 else 'CUT FAILED ' + c.stderr[-200:]} in {int(time.time() - t0)} s")
say("done " + ",".join(map(str, FLOORS)))
