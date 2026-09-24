"""The visitor's journey on the Rainbow stage, in headless Chrome (SwiftShader): hero, pick floor 32, pick west on its
ring, then a phone. Screens go to checks/out/journey_*.png; the events the page heard are printed.
usage: python checks/journey.py [--mobile]"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

MOBILE = "--mobile" in sys.argv
OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)
tag = "m" if MOBILE else "d"
logs = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-gpu"])
    if MOBILE:
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True,
                            user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36")
    else:
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = ctx.new_page()
    page.set_default_timeout(180000)
    page.on("console", lambda m: logs.append(f"[{m.type}] {m.text}"))
    page.on("pageerror", lambda e: logs.append(f"[pageerror] {e}"))
    t0 = time.time()
    page.goto("http://127.0.0.1:47914/index.html?force3d&ao=off&orbit=0", wait_until="load")
    page.wait_for_function('window.__rbs && window.__rbs.phase !== "poster"', timeout=90000)
    page.evaluate("window.__rbs.ready")
    print("ready in", round(time.time() - t0, 1), "s; phase", page.evaluate("window.__rbs.phase"))
    time.sleep(9)  # the intro flight
    page.screenshot(path=os.path.join(OUT, f"coast_{tag}_1_hero.png"))

    def tap(pt):
        if MOBILE:
            page.touchscreen.tap(pt["x"], pt["y"])
        else:
            page.mouse.move(pt["x"], pt["y"])
            page.mouse.click(pt["x"], pt["y"])

    pt = page.evaluate("window.__rbs._engine()._floorScreenPoint(32)")
    print("floor 32 at", pt)
    tap(pt)
    time.sleep(4)
    page.screenshot(path=os.path.join(OUT, f"coast_{tag}_2_floor32.png"))
    rp = page.evaluate("window.__rbs._engine()._ringScreenPoint(270, 32)")
    print("ring west at", rp)
    if rp:
        tap(rp)
        time.sleep(3)
    page.screenshot(path=os.path.join(OUT, f"coast_{tag}_3_west.png"))
    print("selection", json.dumps(page.evaluate("window.__rbs.getSelection()"), ensure_ascii=False))
    print("events", json.dumps(page.evaluate("window.__events"), ensure_ascii=False))
    print("stats", json.dumps(page.evaluate("window.__rbs.stats()")))
    b.close()
print("\n".join(l for l in logs if "error" in l.lower() or "warn" in l.lower())[:3000])
