import os, sys, json, time
sys.argv = ["x", "he", "tprobe"]
src = open("swipe_local.py", encoding="utf-8").read()
exec(src[:src.index("res = {\"lang\": LANG")])
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    ctx.route("**/*", route)
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
    pg.goto(URL + "?tp=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3000)
    pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 120); }"); pg.wait_for_timeout(600)
    r = pg.evaluate("() => document.querySelector('#nlps .nlw').getBoundingClientRect().top")
    pg.touchscreen.tap(195, int(r + 180))
    T = "() => { const c = window.__nlpsWorld._debug().camera; const d = c.position.clone(); c.getWorldDirection(d); return [+d.y.toFixed(4), +c.position.x.toFixed(1), +c.position.y.toFixed(1), +c.position.z.toFixed(1)]; }"
    for i in range(2):
        pg.wait_for_timeout(1000)
        try: print(i + 1, "s", pg.evaluate(T), pg.evaluate("() => window.__nlpsWorld.getState().mode"))
        except Exception as e: print(i + 1, "s", "not yet", str(e)[:60])
    rr = pg.evaluate("() => { const b = document.querySelector('#nlps .nlw').getBoundingClientRect(); return [b.top, b.bottom]; }")
    print("before swipe", pg.evaluate(T))
    swipe(cdp, 195, int(min(rr[1] - 60, 780)), int(max(rr[0] + 80, 120)))
    for i in range(3):
        pg.wait_for_timeout(700); print("after vertical swipe", pg.evaluate(T), "scrollY", pg.evaluate("Math.round(scrollY)"))
    rr = pg.evaluate("() => { const b = document.querySelector('#nlps .nlw').getBoundingClientRect(); return [b.top, b.bottom]; }")
    ym = int((max(rr[0], 60) + min(rr[1], 800)) / 2)
    cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": 320, "y": ym}]})
    for i in range(1, 13):
        cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": 320 - 200 * i / 12, "y": ym}]}); time.sleep(0.016)
    cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    pg.wait_for_timeout(1500)
    print("after sideways swipe", pg.evaluate(T), "scrollY", pg.evaluate("Math.round(scrollY)"))
    b.close()
