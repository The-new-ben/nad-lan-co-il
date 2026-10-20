# Reference frames (1536x1024, no labels) from the 3D world, for the photoreal versions (gen_photoreal.py)
import os, subprocess, sys, time
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(os.path.dirname(H), "world")
V = {
 "aerial": "() => { const C = [-40, 40], a = -143 * Math.PI/180, R = 500, h = 240; return [C[0] + R*Math.sin(a), h, C[1] + R*Math.cos(a), C[0], 0, C[1], 48]; }",
 "centre": "() => { const C = [-50, -24], a = 175 * Math.PI/180, R = 80; return [C[0] + R*Math.sin(a), 36, C[1] + R*Math.cos(a), C[0], 4, C[1], 52]; }",
 "bridge_day": "() => { const w = window.__walk, X = w.XC, U = w.U; return [X[0] + U[0]*120 - 60, 14, X[1] + U[1]*120 + 10, X[0] + U[0]*10, 5, X[1] + U[1]*10, 50]; }",
 "bridge_top": "() => { const w = window.__walk, X = w.XC, U = w.U; return [X[0] - 150, 95, X[1] - 40, X[0] + U[0]*25, 0, X[1] + U[1]*25, 45]; }",
}
srv = subprocess.Popen([sys.executable, "-m", "http.server", "47934", "--bind", "127.0.0.1"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=False, args=["--ignore-gpu-blocklist"])
        pg = b.new_page(viewport={"width": 1536, "height": 1024})
        pg.goto("http://127.0.0.1:47934/index.html"); pg.wait_for_function("window.__walk && window.__walk.ready", timeout=180000)
        pg.evaluate("window.__walk.cineOn()"); pg.evaluate("window.__walk.setTime('day')")
        for k, f in V.items():
            for _ in range(4): pg.evaluate("f => { const c = eval(f)(); window.__walk.cineFrame(...c, 1/30); }", f); pg.wait_for_timeout(200)
            pg.screenshot(path=os.path.join(H, "ref", k + ".png")); print(k)
        b.close()
finally:
    srv.terminate()
