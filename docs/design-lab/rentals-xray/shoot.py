"""Render the board-1b pictures, the six fly stills and the short film (round 2).
   Needs: python -m http.server 8765 --bind 127.0.0.1 from the repo root, desktop Chrome with a real GPU, ffmpeg (imageio_ffmpeg or Shotcut).
   python docs/design-lab/rentals-xray/shoot.py [--only name1,name2] [--no-film]"""
import sys, json, time, os, argparse, subprocess, shutil, glob, tempfile
from playwright.sync_api import sync_playwright
ap = argparse.ArgumentParser(); ap.add_argument("--port", default="8765"); ap.add_argument("--only", default=""); ap.add_argument("--no-film", action="store_true")
a = ap.parse_args()
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUT = os.path.join(REPO, "docs", "rentals", "design", "board1b", "renders")
os.makedirs(OUT, exist_ok=True)
URL = f"http://127.0.0.1:{a.port}/docs/design-lab/rentals-xray/xray.html"
ARGS = ["--enable-gpu", "--use-angle=d3d11", "--ignore-gpu-blocklist", "--hide-scrollbars"]
only = set(filter(None, a.only.split(",")))
want = lambda n: not only or n in only
def ffmpeg():
    for c in [r"C:\Users\777\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe", r"C:\Users\777\AppData\Local\Programs\Shotcut\ffmpeg.exe", shutil.which("ffmpeg") or ""]:
        if c and os.path.exists(c): return c
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=ARGS)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    pg = ctx.new_page(); logs = []
    pg.on("console", lambda m: logs.append(m.type + ": " + m.text)); pg.on("pageerror", lambda e: logs.append("PAGEERROR " + str(e)))
    pg.goto(URL); pg.wait_for_function("window.__xrayReady===true && window.xray.ready()", timeout=90000); time.sleep(1.0)
    stage = pg.locator("#stage")
    settle = lambda: (pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))"), time.sleep(0.25))
    def shot(name, js):
        if not want(name): return
        pg.evaluate(js); time.sleep(0.4); settle(); stage.screenshot(path=os.path.join(OUT, name + ".png"))
    J = lambda o: f"xray.jump({json.dumps(o)})"
    shot("normal-all", J({"mode": "normal", "layer": "all", "focus": None}))
    shot("xray-all", J({"mode": "xray", "layer": "all", "focus": None}))
    for l in ["w", "e", "g", "ac"]: shot("xray-" + l, J({"mode": "xray", "layer": l, "focus": None}))
    for part, lay in [("boiler", "w"), ("acLiving", "e"), ("sink", "w"), ("cooktop", "g")]:
        shot(f"focus-{part}-{lay}", J({"mode": "xray", "layer": lay, "focus": part}))
    if want("fly") or not only:
        pg.evaluate(J({"mode": "xray", "layer": "w", "focus": None}))
        for i in range(6):
            pg.evaluate(f"xray.scrub('boiler', {i/5})"); time.sleep(0.35); settle()
            stage.screenshot(path=os.path.join(OUT, f"fly-boiler-0{i+1}.png"))
    if not only:
        out = {}
        for key, o in [("overview", {"mode": "xray", "layer": "all", "focus": None}), ("focus-boiler", {"mode": "xray", "layer": "w", "focus": "boiler"}), ("focus-acLiving", {"mode": "xray", "layer": "e", "focus": "acLiving"}),
                       ("focus-sink", {"mode": "xray", "layer": "w", "focus": "sink"}), ("focus-cooktop", {"mode": "xray", "layer": "g", "focus": "cooktop"})]:
            pg.evaluate(J(o)); out[key] = pg.evaluate("xray.parts()")
        out["plan"] = pg.evaluate("'plugins/nadlan-config/assets/designer/' + xray.plan"); out["rooms"] = pg.evaluate("xray.rooms()")
        out["focusDistancesFromPartM"] = {k: pg.evaluate(f"xray.focusInfo('{k}').distToPartM") for k in ["boiler", "acLiving", "sink", "cooktop"]}
        pg.evaluate(J({"mode": "xray", "layer": "all", "focus": None})); out["overviewFill"] = pg.evaluate("xray.fill()")
        out["stage"] = {"cssWidth": 390, "cssHeight": 444, "note": "x, y in CSS px from the stage's top-left; onStage says whether the anchor falls inside the stage; the PNGs are the same stage at device scale factor 2 (780 x 888)"}
        json.dump(out, open(os.path.join(OUT, "parts.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        print(json.dumps(pg.evaluate("xray.audit()")), json.dumps(out["overviewFill"]), out["focusDistancesFromPartM"])
    if (not only and not a.no_film) or "film" in only:
        n = int(round(pg.evaluate("xray.filmLength") * 30)); tmp = tempfile.mkdtemp(prefix="xrayfilm_")
        for i in range(n):
            pg.evaluate(f"xray.film({i/30})"); pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))"); time.sleep(0.06)
            stage.screenshot(path=os.path.join(tmp, f"f{i:03d}.png"))
        ff = ffmpeg(); mp4 = os.path.join(OUT, "fly-boiler.mp4")
        if ff:
            subprocess.run([ff, "-y", "-loglevel", "error", "-framerate", "30", "-i", os.path.join(tmp, "f%03d.png"), "-c:v", "libx264", "-preset", "veryslow", "-crf", "27", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", mp4], check=True)
            print("film", n, "frames ->", mp4, os.path.getsize(mp4), "bytes")
        else:
            for i, f in enumerate(sorted(glob.glob(os.path.join(tmp, "f*.png")))[::2]): shutil.copy(f, os.path.join(OUT, f"fly-film-{i+1:03d}.png"))
            print("no ffmpeg: wrote fly-film-NNN.png at 15 fps")
        shutil.rmtree(tmp, ignore_errors=True)
    print("\n".join(l for l in logs if "404" not in l)[:1500]); b.close()
