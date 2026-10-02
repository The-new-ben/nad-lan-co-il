# -*- coding: utf-8 -*-
"""Renders Kikar Hamedina's facility 360s (kikar_facility.py: the lobby of tower C at 21.9 17:36, the basement pool, the
basement gym, the basement spa and the residents' parking level -2, all illustrations) one after another and cuts each for
the web with cut_kikar_tour.py --pano, as the apartment's 360 was cut:
  plugins/nadlan-config/assets/project-stage/hamedina/tour/fac-<lobby|pool|gym|spa|parking>-c[.jpg|.webp|-2k.jpg|-2k.webp|
  -card.jpg|-thumb.webp]
The same parameters as the apartment's 360 (render_kikar_styles.py: 4096 x 2048, 96 samples, 12 threads); the renders stay
in scripts/interior/_renders/kikar/fac-<scene>-c.png (not committed).
  python scripts/interior/render_kikar_facilities.py [scenes lobby,pool,gym] [samples 96] [threads 12] [--no-cut]
  e.g. python scripts/interior/render_kikar_facilities.py parking,spa      (2.10.2026: the two rooms added; any of the
  five scene names, comma separated; the default stays the first three)
Waits while another Blender runs (other renders share this machine). Progress, the REPORT and DOOR lines (the doors' yaws
for the building walk): scripts/interior/render_kikar_facilities.log."""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
TMP = os.path.join(HERE, "_renders", "kikar")
a = [x for x in sys.argv[1:] if not x.startswith("--")]
SCENES = [s.strip() for s in (a[0] if len(a) > 0 else "lobby,pool,gym").split(",") if s.strip()]
KNOWN = ("lobby", "pool", "gym", "spa", "parking")
if not SCENES or any(s not in KNOWN for s in SCENES):
    raise SystemExit("render_kikar_facilities: scenes are a comma list of %s, not %r" % (" | ".join(KNOWN), a[0] if a else ""))
SAMPLES = a[1] if len(a) > 1 else "96"
THREADS = a[2] if len(a) > 2 else "12"
CUT = "--no-cut" not in sys.argv
W = 4096
os.makedirs(TMP, exist_ok=True)
log = open(os.path.join(HERE, "render_kikar_facilities.log"), "a", encoding="utf-8")


def say(m):
    log.write(time.strftime("%Y-%m-%d %H:%M:%S ") + m + "\n")
    log.flush()
    print(m, flush=True)


def blender_running():
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq blender.exe", "/NH"], capture_output=True, text=True)
    return "blender.exe" in r.stdout.lower()


say("start: %s, %d x %d, %s samples, %s threads" % (",".join(SCENES), W, W // 2, SAMPLES, THREADS))
for sc in SCENES:
    while blender_running():
        time.sleep(60)
    name = "fac-%s-c" % sc
    png = os.path.join(TMP, name + ".png")
    t0 = time.time()
    r = subprocess.run([BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "kikar_facility.py"), "--",
                        png, sc, str(W), SAMPLES, THREADS], capture_output=True, text=True, encoding="utf-8", errors="replace")
    info = [ln for ln in r.stdout.splitlines() if ln.startswith(("REPORT", "DOOR", "SUN", "RENDER"))]
    if r.returncode != 0 or not os.path.exists(png) or os.path.getmtime(png) < t0:
        say("%s: RENDER FAILED %s %s" % (name, r.returncode, (r.stderr or r.stdout)[-600:]))
        continue
    say("%s: rendered in %d s (%s samples)" % (name, time.time() - t0, SAMPLES))
    for ln in info:
        say("   | " + ln)
    if CUT:
        c = subprocess.run([sys.executable, os.path.join(HERE, "cut_kikar_tour.py"), "--pano", png, name], capture_output=True, text=True)
        say("%s: cut %s" % (name, "ok" if c.returncode == 0 else "FAILED " + c.stderr[-300:]))
say("done: " + ",".join(SCENES))
