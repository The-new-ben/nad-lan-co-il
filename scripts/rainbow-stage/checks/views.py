"""Hero framings to compare (bearing, elevation, distance multiplier), GPU headless. python checks/views.py"""
import os, time
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), "out")
VIEWS = [(188, 10, 1.0), (170, 16, 1.25), (150, 20, 1.5), (120, 14, 1.3), (205, 22, 1.6)]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-gpu"])
    page = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
    page.goto("http://127.0.0.1:47914/index.html?force3d&ao=off&orbit=0&intro=0", wait_until="load")
    page.wait_for_function('window.__rbs && window.__rbs.phase !== "poster"', timeout=90000)
    time.sleep(6)
    for bb, ee, dd in VIEWS:
        page.evaluate(f"window.__rbs._engine()._view({bb},{ee},{dd})")
        time.sleep(3)
        page.screenshot(path=os.path.join(OUT, f"view_{bb}_{ee}_{dd}.png"))
        print("saved", bb, ee, dd)
    b.close()
