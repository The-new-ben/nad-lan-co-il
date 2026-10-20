# -*- coding: utf-8 -*-
"""The film's 3D shots, rendered frame by frame from the walk (../world/index.html, cineFrame): 1920x1080, 30 fps -> shots3d/<name>/f00000.jpg
  python rec_3d.py [name ...]"""
import os, subprocess, sys, time
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(os.path.dirname(H), "world"); OUT = os.path.join(H, "shots3d")
FPS = 30
# each shot: seconds, time of day, label groups/point, and a JS function of t (0..1) returning [px,py,pz, lx,ly,lz, fov]
SHOTS = {
 "open": (7.5, "day", None, """t => { const e = t*t*(3-2*t), C = [-40, 40], a = (-160 + 34*e) * Math.PI/180, R = 560 - 90*e, h = 280 - 70*e;
   return [C[0] + R*Math.sin(a), h, C[1] + R*Math.cos(a), C[0], 0, C[1], 48]; }"""),
 "street": (5.5, "day", None, """t => { const e = t*t*(3-2*t), A = [-235, 84], B = [-70, 14]; const x = A[0] + (B[0]-A[0])*e, z = A[1] + (B[1]-A[1])*e;
   return [x, 16 - 4*e, z, x + (B[0]-A[0])*0.35, 6, z + (B[1]-A[1])*0.35, 55]; }"""),
 "centre": (7, "day", [["food", "essentials"], -50, -24, 75], """t => { const e = t*t*(3-2*t), C = [-50, -24], a = (150 + 55*e) * Math.PI/180, R = 95 - 25*e;
   return [C[0] + R*Math.sin(a), 42 - 12*e, C[1] + R*Math.cos(a), C[0], 4, C[1], 52]; }"""),
 "approach": (5.5, "day", None, """t => { const w = window.__walk, X = w.XC, U = w.U, e = t*t*(3-2*t); const s = -190 + 80*e;
   return [X[0] + U[0]*s - 14, 30 - 22*e, X[1] + U[1]*s, X[0] + U[0]*10, 5, X[1] + U[1]*10, 52]; }"""),
 "walk": (7.5, "day", None, """t => { const p = window.__walk.BR[0].path, n = p.length; const f = 30 + (n*0.62 - 30) * t, i = Math.floor(f), k = f - i;
   const a = p[i], b = p[Math.min(n-1, i+1)], q = p[Math.min(n-1, i+22)]; const x = a.x + (b.x-a.x)*k, z = a.z + (b.z-a.z)*k, y = a.y + (b.y-a.y)*k;
   return [x - a.nx*0.8, y + 2.2, z - a.nz*0.8, q.x, q.y + 1.6, q.z, 62]; }"""),
 "reveal": (6.5, "day", None, """t => { const w = window.__walk, p = w.BR[0].path, X = w.XC, U = w.U, e = t*t*(3-2*t); const end = p[p.length-1];
   const x = end.x + 30 + 90*e, z = end.z + 60 + 140*e; return [x, 6 + 110*e, z, X[0] + U[0]*40, 2, X[1] + U[1]*40, 50]; }"""),
 "night": (9, "night", None, """t => { const w = window.__walk, X = w.XC, U = w.U, NW = [-U[1], U[0]], e = t;
   const c = [X[0] + U[0]*48, X[1] + U[1]*48]; const x = c[0] + NW[0]*(-40 + 30*e) + U[0]*55, z = c[1] + NW[1]*(-40 + 30*e) + U[1]*55;
   return [x, 2.2 + 3*e, z, X[0] + U[0]*30, 5.5, X[1] + U[1]*30, 52]; }"""),
}
names = [a for a in sys.argv[1:]] or list(SHOTS)
srv = subprocess.Popen([sys.executable, "-m", "http.server", "47933", "--bind", "127.0.0.1"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=False, args=["--ignore-gpu-blocklist", "--enable-gpu-rasterization"])
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto("http://127.0.0.1:47933/index.html"); pg.wait_for_function("window.__walk && window.__walk.ready", timeout=180000)
        pg.evaluate("window.__walk.cineOn()")
        for name in names:
            sec, tod, lab, fn = SHOTS[name]; d = os.path.join(OUT, name); os.makedirs(d, exist_ok=True)
            pg.evaluate("m => window.__walk.setTime(m)", tod)
            pg.evaluate("a => window.__walk.cineLabels(a ? a[0] : [], a ? a[1] : 0, a ? a[2] : 0, a ? a[3] : 0)", lab)
            n = int(sec * FPS)
            pg.evaluate("f => { window.__shot = eval(f); }", fn)
            for _ in range(4): pg.evaluate("() => { const c = window.__shot(0); window.__walk.cineFrame(...c, 1/30); }"); pg.wait_for_timeout(150)
            for i in range(n):
                pg.evaluate("t => { const c = window.__shot(t); window.__walk.cineFrame(...c, 1/30); }", i / max(1, n - 1))
                pg.screenshot(path=os.path.join(d, "f%05d.jpg" % i), type="jpeg", quality=92)
            print(name, n, "frames", flush=True)
        b.close()
finally:
    srv.terminate()
print("DONE", flush=True)
