# -*- coding: utf-8 -*-
"""The owner's report (30.9 evening): on a phone the Kikar page is "scrolling inside scrolling". Real finger swipes (CDP touch
events) on a phone emulation of the LIVE page: does a vertical swipe move the PAGE, or is it swallowed by the world, the
floor panel or the area map? Also: what the area map shows as markers (dots or labels with icons).
  python swipe_test.py <url> <tag>"""
import io, os, sys, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
url, tag = sys.argv[1], sys.argv[2]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "swipe"); os.makedirs(OUT, exist_ok=True)


def swipe(cdp, x, y0, y1, steps=12):
    cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y0}]})
    for i in range(1, steps + 1):
        y = y0 + (y1 - y0) * i / steps
        cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x, "y": y}]})
        time.sleep(0.016)
    cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    time.sleep(0.9)


res = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2,
                        user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36")
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
    pg.goto(url + ("&" if "?" in url else "?") + "swipe=%d" % time.time(), wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(3000)
    Y = lambda: pg.evaluate("Math.round(scrollY)")

    # 1) the world: bring the stage to mid-screen, enter it the way a visitor does (tap the poster / enter), then swipe UP on it
    pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 120); }")
    pg.wait_for_timeout(800)
    y_before_enter = Y()
    r = pg.evaluate("() => { const s = document.getElementById('nlps').getBoundingClientRect(); return {top: s.top, bottom: s.bottom}; }")
    pg.touchscreen.tap(195, int(r["top"] + 200)); pg.wait_for_timeout(6000)
    entered = pg.evaluate("() => !!document.querySelector('#nlps canvas')")
    r = pg.evaluate("() => { const s = document.getElementById('nlps').getBoundingClientRect(); return {top: s.top, bottom: s.bottom}; }")
    y0 = Y(); swipe(cdp, 195, int(min(r["bottom"] - 60, 780)), int(max(r["top"] + 80, 120))); y1 = Y()
    res["world_swipe"] = {"entered": entered, "scroll_before": y0, "scroll_after": y1, "page_moved_px": y1 - y0}
    pg.screenshot(path=os.path.join(OUT, tag + "-1-world.png"))

    # 2) the floor panel: switch to the floor view, swipe UP inside the panel
    pg.evaluate("() => { const t = [...document.querySelectorAll('#nlps .nlw-tab')].find(b => b.dataset.mode === 'tower'); if (t) t.click(); }")
    pg.wait_for_timeout(1500)
    pr = pg.evaluate("() => { const p = document.querySelector('#nlps .nlw-panel'); if (!p) return null; const r = p.getBoundingClientRect(); return {top: r.top, bottom: r.bottom, h: p.clientHeight, sh: p.scrollHeight}; }")
    if pr and pr["bottom"] > 0:
        a, bb = int(min(pr["bottom"] - 20, 830)), int(max(pr["top"] + 20, 40))
        for i in range(3):
            y0 = Y(); swipe(cdp, 195, a, bb); y1 = Y()
            res.setdefault("panel_swipes", []).append({"scroll_before": y0, "scroll_after": y1, "page_moved_px": y1 - y0,
                                                        "panel_scrollTop": pg.evaluate("() => document.querySelector('#nlps .nlw-panel').scrollTop")})
        res["panel"] = pr
    pg.screenshot(path=os.path.join(OUT, tag + "-2-panel.png"))

    # 3) the area map: scroll to it, wait for it, swipe UP on it
    pg.evaluate("() => { const m = document.getElementById('nlpjx-map'); if (m) window.scrollTo(0, m.getBoundingClientRect().top + scrollY - 80); }")
    pg.wait_for_timeout(1500)
    for _ in range(6):  # a few small real swipes to trigger lazy loading like a visitor would
        swipe(cdp, 30, 700, 640, 4)
    pg.wait_for_timeout(5000)
    mp = pg.evaluate("""() => { const m = document.querySelector('#nlpjx-map .mapboxgl-map'); if (!m) return null; const r = m.getBoundingClientRect();
        const mk = [...document.querySelectorAll('#nlpjx-map .mapboxgl-marker')];
        return {top: r.top, bottom: r.bottom, h: r.height, cls: m.className, markers: mk.length,
                markerKinds: mk.slice(0, 8).map(x => ({cls: String(x.className).replace('mapboxgl-marker','').trim().slice(0, 60), text: (x.textContent || '').trim().slice(0, 24), w: Math.round(x.getBoundingClientRect().width), h: Math.round(x.getBoundingClientRect().height), hasIcon: !!x.querySelector('svg, img, i')}))}; }""")
    res["map"] = mp
    if mp and mp["bottom"] > 100:
        mid = int((max(mp["top"], 60) + min(mp["bottom"], 830)) / 2)
        y0 = Y(); swipe(cdp, 195, mid + 150, mid - 150); y1 = Y()
        res["map_swipe"] = {"scroll_before": y0, "scroll_after": y1, "page_moved_px": y1 - y0}
    pg.screenshot(path=os.path.join(OUT, tag + "-3-map.png"))
    b.close()
json.dump(res, open(os.path.join(OUT, tag + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
