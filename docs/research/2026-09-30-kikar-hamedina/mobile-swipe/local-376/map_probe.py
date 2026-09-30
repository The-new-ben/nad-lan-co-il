import os, sys, json, time
sys.argv = ["x", "he", "mp"]
src = open("v1045_check.py", encoding="utf-8").read()
exec(src[:src.index("CAM = ")])
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    ctx.route("**/*", route)
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
    pg.goto(URL + "?mp=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3000)
    pg.evaluate("() => { const m = document.getElementById('nlpjx-map'); window.scrollTo(0, m.getBoundingClientRect().top + scrollY - 60); }")
    pg.wait_for_timeout(1000)
    for _ in range(5): swipe(cdp, 24, 700, 660, 4)
    pg.wait_for_timeout(7000)
    pg.evaluate("() => { const m = document.getElementById('nlpjx-unimap') || document.getElementById('nlpjx-map'); window.scrollTo(0, m.getBoundingClientRect().top + scrollY - 70); }")
    print(pg.evaluate("() => ({rtl: mapboxgl.getRTLTextPluginStatus && mapboxgl.getRTLTextPluginStatus(), v: mapboxgl.version, z: NLPJX_MAP.getZoom(), styleLoaded: NLPJX_MAP.isStyleLoaded(), sz: JSON.stringify(NLPJX_MAP.getLayoutProperty('nlam-pin','text-size')), op: JSON.stringify(NLPJX_MAP.getPaintProperty('nlam-pin','text-opacity')), font: JSON.stringify(NLPJX_MAP.getLayoutProperty('nlam-pin','text-font')), src: JSON.stringify(Object.keys(NLPJX_MAP.getSource('nlam').serialize()))})"))
    for z in (14.4, 14.9, 15.3):
        pg.evaluate(f"() => NLPJX_MAP.jumpTo({{zoom: {z}}})"); pg.wait_for_timeout(3500)
        pg.screenshot(path=f"v1045/mp-{z}.png")
    pg.evaluate("() => { NLPJX_MAP.jumpTo({zoom: 14.4}); NLPJX_MAP.setLayoutProperty('nlam-pin','text-field','X'); }"); pg.wait_for_timeout(3500)
    pg.screenshot(path="v1045/mp-14.4-latin.png")
    pg.evaluate("() => { NLPJX_MAP.setLayoutProperty('nlam-pin','text-field',['get','name']); }"); pg.wait_for_timeout(3500)
    pg.screenshot(path="v1045/mp-14.4-relayout.png")
    b.close()
