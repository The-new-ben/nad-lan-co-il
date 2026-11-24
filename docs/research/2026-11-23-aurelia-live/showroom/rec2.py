"""Aurelia showroom round 2 (HAD-810): a short phone recording of the LIVE page as a visitor (390x844, touch):
tap a flat -> the pull-out -> the information under the tower -> the map with the beam and the places that way.
python rec2.py OUTDIR      (video .webm in OUTDIR; the room-availability call is answered 'not now' so nobody is paged)"""
import json, os, sys, time
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
URL = "https://nad-lan.co.il/projects/aurelia/?nlv=%d" % int(time.time())
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    ctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="he-IL",
                         user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Mobile Safari/537.36",
                         record_video_dir=OUT, record_video_size={"width": 390, "height": 844})
    ctx.route("**/nadlan/v1/room/available*", lambda r: r.fulfill(status=200, content_type="application/json", body=json.dumps({"ok": True, "now": False})))
    pg = ctx.new_page()
    pg.goto(URL, wait_until="load", timeout=120000); pg.wait_for_timeout(2500)
    pg.evaluate("(()=>{const e=document.getElementById('nlas');window.scrollTo({top:e.getBoundingClientRect().top+scrollY-60,behavior:'instant'})})()")
    pg.wait_for_function("window.__nlas && window.__nlas.interactive", timeout=60000); pg.wait_for_timeout(1800)
    pt = pg.evaluate("NLAS.screenOf('20-5')") or pg.evaluate("NLAS.screenOf('20-2')")
    pg.touchscreen.tap(pt["x"], pt["y"]); pg.wait_for_timeout(5500)  # the pull-out, then tower + map + beam on one screen
    for y in (300, 300, 300, 300, 300):  # down through the places that way and the information
        pg.mouse.wheel(0, y); pg.wait_for_timeout(1100)
    pg.wait_for_timeout(1200)
    pg.evaluate("(()=>{const e=document.getElementById('nlpjx-unimap');window.scrollTo({top:e.getBoundingClientRect().top+scrollY-120,behavior:'smooth'})})()")
    pg.wait_for_timeout(3500)
    if os.environ.get("PLAN") == "1":  # 762: the plan opens large from the band, then the floor arrows up to 47
        pg.evaluate("(()=>{const e=document.getElementById('nlas');window.scrollTo({top:e.getBoundingClientRect().top+scrollY-60,behavior:'smooth'})})()"); pg.wait_for_timeout(1500)
        pg.locator("#nlas .bd-pic").tap(); pg.wait_for_timeout(5000)
        pg.mouse.wheel(0, 250); pg.wait_for_timeout(1500)
        pg.evaluate("NLAS.open('46-1', false)"); pg.wait_for_timeout(2500)
        b = pg.locator('#nlas .pn-fl [data-fl="1"]'); b.scroll_into_view_if_needed(); pg.wait_for_timeout(800); b.tap(); pg.wait_for_timeout(2500)
    v = pg.video.path(); ctx.close(); br.close()
    print(v)
