# -*- coding: utf-8 -*-
"""Renders DUO's 360 panoramas (duo_facility.py: the pool, the lobby, the wellness complex; duo_interior.py: the example
apartment's living room on floor 25 in the four directions) and cuts them for the web exactly as Rainbow's (cut_tour.py):
  fac-<scene>.jpg + fac-<scene>-2k.jpg (the facilities, 3072 wide like rainbow/tour/fac-*.jpg: no card),
  living-25<d>.jpg + -2k.jpg + -card.jpg (the living rooms, 4096 wide like rainbow/tour/living-25*.jpg).
The raw renders stay in scripts/interior/_renders/duo-*.png. Before each render it waits while any other Blender runs
(other renders share this machine); every render uses fixed threads.
  python scripts/interior/render_duo.py [items all | fac-pool,living-25w,...] [facility samples 64] [living samples 40]
         [threads 6] [facility width 3072] [living width 4096]
(40 samples at 3072-4096 is what Rainbow's finals used, render_floors.py / render_styles.py; the facilities, lit by many
lamps, take 64)
Progress: scripts/interior/render_duo.log."""
import os, shutil, subprocess, sys, time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # the scenes print Hebrew sector words
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "duo", "tour")
TMP = os.path.join(HERE, "_renders")
a = sys.argv[1:]
ITEMS = a[0] if len(a) > 0 else "all"
FAC_S = a[1] if len(a) > 1 else "64"
LIV_S = a[2] if len(a) > 2 else "40"
THREADS = a[3] if len(a) > 3 else "6"
FAC_W = a[4] if len(a) > 4 else "3072"
LIV_W = a[5] if len(a) > 5 else "4096"
ALL = [("fac-pool", "facility", "pool"), ("fac-lobby", "facility", "lobby"), ("fac-wellness", "facility", "wellness"),
       ("living-25w", "interior", "280"), ("living-25n", "interior", "10"), ("living-25e", "interior", "100"), ("living-25s", "interior", "190")]
todo = ALL if ITEMS == "all" else [x for x in ALL if x[0] in ITEMS.split(",")]
os.makedirs(OUT, exist_ok=True)
log = open(os.path.join(HERE, "render_duo.log"), "a", encoding="utf-8")


def say(m):
    log.write(time.strftime("%H:%M:%S ") + m + "\n")
    log.flush()
    print(m, flush=True)


def blender_running():
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq blender.exe", "/NH"], capture_output=True, text=True)
    return "blender.exe" in r.stdout.lower()


for name, kind, arg in todo:
    waited = 0
    while blender_running():
        if not waited:
            say("%s: another Blender is running, waiting" % name)
        time.sleep(120)
        waited += 120
    png = os.path.join(TMP, "duo-%s.png" % name)
    if kind == "facility":
        cmd = [BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "duo_facility.py"), "--", png, arg, FAC_W, FAC_S, THREADS]
    else:
        cmd = [BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "duo_interior.py"), "--", png, "25", arg, LIV_W, LIV_S, THREADS]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    info = [l for l in r.stdout.splitlines() if l.startswith(("ILLUSTRATION", "DUO example", "panorama centre", "   ", "  through"))]
    if r.returncode != 0 or not os.path.exists(png):
        say("%s: RENDER FAILED %s %s" % (name, r.returncode, (r.stderr or r.stdout)[-400:]))
        continue
    if kind == "facility":
        cut_dir = os.path.join(TMP, "duo-cut-" + name)
        c = subprocess.run([sys.executable, os.path.join(HERE, "cut_tour.py"), png, cut_dir, name], capture_output=True, text=True)
        for fn in (name + ".jpg", name + "-2k.jpg"):
            if os.path.exists(os.path.join(cut_dir, fn)):
                shutil.copyfile(os.path.join(cut_dir, fn), os.path.join(OUT, fn))
        shutil.rmtree(cut_dir, ignore_errors=True)
    else:
        c = subprocess.run([sys.executable, os.path.join(HERE, "cut_tour.py"), png, OUT, name], capture_output=True, text=True)
    say("%s: ok in %d s (%s wide, %s samples)%s" % (name, time.time() - t0, FAC_W if kind == "facility" else LIV_W,
                                                    FAC_S if kind == "facility" else LIV_S,
                                                 "" if c.returncode == 0 else " | CUT FAILED " + c.stderr[-200:]))
    for l in info:
        say("   | " + l.strip())
say("done " + ",".join(x[0] for x in todo))
