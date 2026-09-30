import os, sys, json, time
PAGE = sys.argv[1]; SHOT = sys.argv[2]
sys.argv = ["x", "he", "hp", "--live"]
src = open("v1045_check.py", encoding="utf-8").read()
exec(src[:src.index("CAM = ")])
URL = "https://nad-lan.co.il/" + PAGE.strip("/") + "/"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    ctx.route("**/*", route)
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.goto(URL + "?hp=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3000)
    pg.evaluate("() => { const m = document.getElementById('nlpjx-map'); window.scrollTo(0, m.getBoundingClientRect().top + scrollY - 60); }"); pg.wait_for_timeout(1000)
    for _ in range(5): swipe(cdp, 24, 700, 660, 4)
    pg.wait_for_timeout(7000)
    pg.evaluate("() => { const m = document.getElementById('nlpjx-unimap') || document.getElementById('nlpjx-map'); window.scrollTo(0, m.getBoundingClientRect().top + scrollY - 70); }"); pg.wait_for_timeout(1500)
    r = pg.evaluate("() => { const m = window.NLPJX_MAP; return m ? {home: !!m.getLayer('nlam-home'), homeRendered: m.getLayer('nlam-home') ? m.queryRenderedFeatures({layers: ['nlam-home']}).length : 0, homeVis: m.getLayer('nlam-home') ? m.getLayoutProperty('nlam-home','visibility') : null, places: m.queryRenderedFeatures({layers: ['nlam-pin']}).length, title: document.getElementById('nlpjx-unimap').dataset.title} : null; }")
    pg.screenshot(path=f"v1045/home-{SHOT}.png")
    print(json.dumps({"page": PAGE, "r": r, "errors": errs}, ensure_ascii=False))
    b.close()
