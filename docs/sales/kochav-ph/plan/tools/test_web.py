# -*- coding: utf-8 -*-
"""Exercise web/plan.html in Edge (Playwright): tap rooms, toggle 3D, double-tap zoom, keyboard; save screenshots to web/shots/."""
import os, pathlib
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
url = pathlib.Path(os.path.join(H, "web", "plan.html")).as_uri()
S = lambda n: os.path.join(H, "web", "shots", n)
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    # phone
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page(); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(url); pg.wait_for_timeout(1500)
    # tap the living room label area in the SVG
    box = pg.locator("#room-living .floor").bounding_box()
    pg.locator("#np-stage").tap(position={"x": box["x"] - pg.locator("#np-stage").bounding_box()["x"] + box["width"] * 0.5, "y": box["y"] - pg.locator("#np-stage").bounding_box()["y"] + box["height"] * 0.45})
    pg.wait_for_timeout(600)
    print("after tap on living:", pg.locator("#np-panel h3").inner_text(), "| active:", pg.evaluate("[...document.querySelectorAll('.room.active')].map(g=>g.dataset.room)"))
    pg.screenshot(path=S("plan-390-living.png"), full_page=True)
    # chip: main bedroom
    pg.locator('.np-chip[data-room="bed2"]').click(); pg.wait_for_timeout(400)
    pg.screenshot(path=S("plan-390-bed2.png"), full_page=False)
    # 3D + kitchen chip
    pg.locator('.np-seg button[data-mode="3d"]').click(); pg.locator('.np-chip[data-room="kitchen"]').click(); pg.wait_for_timeout(800)
    pg.screenshot(path=S("plan-390-3d-kitchen.png"), full_page=True)
    print("3D kitchen tag:", pg.locator("#np-tag").inner_text(), pg.locator("#np-tag").is_visible())
    # double tap zoom
    pg.locator('.np-seg button[data-mode="2d"]').click(); pg.wait_for_timeout(300)
    st = pg.locator("#np-stage").bounding_box()
    for _ in range(2):
        pg.touchscreen.tap(st["x"] + st["width"] * 0.62, st["y"] + st["height"] * 0.4); pg.wait_for_timeout(120)
    pg.wait_for_timeout(500)
    print("after double tap transform:", pg.evaluate("document.getElementById('np-canvas').style.transform"), "touch-action:", pg.evaluate("document.getElementById('np-stage').style.touchAction"))
    pg.screenshot(path=S("plan-390-zoomed.png"), full_page=False)
    ctx.close()
    # desktop + keyboard
    pg = b.new_page(viewport={"width": 1280, "height": 900}); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(url); pg.wait_for_timeout(1500)
    pg.locator("#room-terrace").focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(500)
    print("keyboard select:", pg.locator("#np-panel h3").inner_text())
    pg.screenshot(path=S("plan-1280-terrace.png"), full_page=True)
    pg.locator('.np-seg button[data-mode="3d"]').click(); pg.locator('.np-chip[data-room="living"]').click(); pg.wait_for_timeout(800)
    pg.screenshot(path=S("plan-1280-3d-living.png"), full_page=True)
    # target sizes
    small = pg.evaluate("[...document.querySelectorAll('button')].filter(b=>{const r=b.getBoundingClientRect();return r.height<44||r.width<44}).map(b=>b.textContent.trim())")
    print("buttons under 44px:", small)
    b.close()
print("console errors:", errs)
