"""The stage's poster for the page's stage size (25.9.2026, design system v13+: the stage stands in the first fold, about
716x660 on a 1440 screen, so the old 16:10 poster showed the tower small until the scene took over). Renders the scene at
that aspect, from the same opening view the live stage settles on, with no floor picked, and writes poster.jpg next to
this folder's stage. The phone crops the same picture (object-fit: cover, the tower stays in the middle).
Needs the demo page served on 127.0.0.1:47914 (the stage's demo folder, with the current stage.js, stage.css and
quarter.json copied in), a real GPU (d3d11).
  python scripts/rainbow-stage/checks/poster_stage.py <out.jpg> [width height]"""
import base64, sys, time
from playwright.sync_api import sync_playwright

out = sys.argv[1]
W = int(sys.argv[2]) if len(sys.argv) > 2 else 716
H = int(sys.argv[3]) if len(sys.argv) > 3 else 660
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-gpu"])
    page = b.new_page(viewport={"width": W, "height": H})
    page.goto("http://127.0.0.1:47914/index.html?force3d&ao=on&orbit=0&intro=0&quarter")  # with the quarter's masses, as on the page
    page.wait_for_function('window.__rbs && window.__rbs.phase === "orbit"', timeout=120000)
    page.wait_for_function("window.__rbs.stats().ao === true", timeout=30000)
    time.sleep(2.5)
    url = page.evaluate(f"window.__rbs._engine()._capture({W * 2}, {H * 2}, 0.86)")
    open(out, "wb").write(base64.b64decode(url.split(",", 1)[1]))
    b.close()
print("poster", W * 2, "x", H * 2, "->", out)
