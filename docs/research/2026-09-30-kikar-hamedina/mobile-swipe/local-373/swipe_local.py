# -*- coding: utf-8 -*-
"""v104.3 acceptance on the LIVE page with the LOCAL world + area map + icons swapped in (Playwright routes; nothing written
anywhere). Real finger swipes over CDP, a phone (390x844, touch, mobile UA).
  python swipe_local.py <lang: he|en|ar> <tag> [--live]   (--live = no swap, the 'before')"""
import io, os, sys, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
LANG, TAG = sys.argv[1], sys.argv[2]
LIVE = "--live" in sys.argv
URL = {"he": "https://nad-lan.co.il/projects/hamedina/", "en": "https://nad-lan.co.il/projects/hamedina-en/",
       "ar": "https://nad-lan.co.il/projects/hamedina-ar/"}[LANG]
PN = r"C:\Users\777\nad-lan\nad-lan-co-il\plugins\nadlan-config"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "after"); os.makedirs(OUT, exist_ok=True)
ICONS = open(os.path.join(PN, "assets", "arealife", "place-icons.js"), encoding="utf-8").read()
SWAP = {"/assets/project-stage/world/world.js": "assets/project-stage/world/world.js",
        "/assets/project-stage/world/world.css": "assets/project-stage/world/world.css",
        "/assets/arealife/areamap.js": "assets/arealife/areamap.js",
        "/assets/arealife/place-icons.js": "assets/arealife/place-icons.js"}
served = []


def route(r):
    u = r.request.url
    path = u.split("?")[0]
    for k, v in SWAP.items():
        if path.endswith(k):
            body = open(os.path.join(PN, v), encoding="utf-8").read()
            if k.endswith("areamap.js"):
                body = ICONS + "\n" + body  # the live PHP does not enqueue place-icons.js yet; the release does
            served.append(k)
            ct = "text/css" if v.endswith(".css") else "application/javascript"
            return r.fulfill(status=200, body=body, headers={"content-type": ct + "; charset=utf-8", "cache-control": "no-store"})
    if "wa.me" in u or "whatsapp" in u or "google-analytics" in u or "googletagmanager" in u or r.request.method != "GET":
        return r.abort()
    return r.continue_()


def swipe(cdp, x, y0, y1, steps=12):
    cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y0}]})
    for i in range(1, steps + 1):
        cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x, "y": y0 + (y1 - y0) * i / steps}]})
        time.sleep(0.016)
    cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    time.sleep(0.9)


res = {"lang": LANG, "live": LIVE}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    ctx = b.new_context(viewport={"width": int(os.environ.get("NL_W", "390")), "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2,
                        user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36")
    if not LIVE:
        ctx.route("**/*", route)
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:300]))
    pg.goto(URL + "?sw=%d" % time.time(), wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(3500)
    Y = lambda: pg.evaluate("Math.round(scrollY)")

    # 1) the world: enter it like a visitor, swipe UP on the canvas
    pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 120); }")
    pg.wait_for_timeout(800)
    r = pg.evaluate("() => { const s = document.querySelector('#nlps .nlw') || document.getElementById('nlps'); const b = s.getBoundingClientRect(); return {top: b.top, bottom: b.bottom}; }")
    pg.touchscreen.tap(int(os.environ.get("NL_W", "390")) // 2, int(r["top"] + 180)); pg.wait_for_timeout(7000)
    info = pg.evaluate("""() => { const c = document.querySelector('#nlps canvas'); const w = document.querySelector('#nlps .nlw');
        const d = document.querySelector('#nlps .nlw-dock');
        return {canvas: !!c, touchAction: c ? getComputedStyle(c).touchAction : null, inlineTA: c ? c.style.touchAction : null,
                worldH: w ? Math.round(w.getBoundingClientRect().height) : null, docked: !!d, dockH: d ? Math.round(d.getBoundingClientRect().height) : 0,
                sectionH: Math.round(document.getElementById('nlps').getBoundingClientRect().height)}; }""")
    res["world"] = info
    r = pg.evaluate("() => { const b = document.querySelector('#nlps .nlw').getBoundingClientRect(); return {top: b.top, bottom: b.bottom}; }")
    y0 = Y(); swipe(cdp, int(os.environ.get("NL_W", "390")) // 2, int(min(r["bottom"] - 60, 780)), int(max(r["top"] + 80, 120))); y1 = Y()
    res["world_swipe_px"] = y1 - y0
    pg.screenshot(path=os.path.join(OUT, f"{LANG}-{TAG}-1-world.png"))

    # 2) the floor view: the panel (docked or the sheet), swipe UP on it
    pg.evaluate("() => { const t = [...document.querySelectorAll('#nlps .nlw-tab')].find(b => b.dataset.mode === 'tower'); if (t) t.click(); }")
    pg.wait_for_timeout(2000)
    pr = pg.evaluate("""() => { const p = document.querySelector('#nlps .nlw-panel'); if (!p) return null; const r = p.getBoundingClientRect(); const cs = getComputedStyle(p);
        return {top: r.top, bottom: r.bottom, h: p.clientHeight, sh: p.scrollHeight, overflowY: cs.overflowY, overscroll: cs.overscrollBehaviorY, inDock: !!p.closest('.nlw-dock')}; }""")
    res["panel"] = pr
    if pr:
        pg.evaluate("() => { const p = document.querySelector('#nlps .nlw-panel'); window.scrollTo(0, p.getBoundingClientRect().top + scrollY - 200); }")
        pg.wait_for_timeout(600)
        pr2 = pg.evaluate("() => { const r = document.querySelector('#nlps .nlw-panel').getBoundingClientRect(); return {top: r.top, bottom: r.bottom}; }")
        a, bb = int(min(pr2["bottom"] - 20, 800)), int(max(pr2["top"] + 20, 60))
        if a - bb > 120:
            y0 = Y(); swipe(cdp, int(os.environ.get("NL_W", "390")) // 2, a, bb); y1 = Y()
            res["panel_swipe_px"] = y1 - y0
            res["panel_scrollTop"] = pg.evaluate("() => document.querySelector('#nlps .nlw-panel').scrollTop")
    # the floor view as the visitor sees it: the world + the top of the dock
    pg.evaluate("() => { const s = document.querySelector('#nlps .nlw'); window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 70); }")
    pg.wait_for_timeout(1200)
    pg.screenshot(path=os.path.join(OUT, f"{LANG}-{TAG}-2-dock.png"))
    # nested scrollers left on the page (outside full screen): overflow auto/scroll AND overscroll contain, content taller than box
    res["nested_scrollers"] = pg.evaluate("""() => [...document.querySelectorAll('body *')].filter(e => { const cs = getComputedStyle(e);
        return /(auto|scroll)/.test(cs.overflowY) && cs.overscrollBehaviorY === 'contain' && e.scrollHeight > e.clientHeight + 4 && e.getClientRects().length; })
        .map(e => (e.className || e.tagName).toString().slice(0, 50))""")

    # 3) the world's aerial pins (icons, never a bare dot)
    pg.evaluate("() => { const t = [...document.querySelectorAll('#nlps .nlw-tab')].find(b => b.dataset.mode === 'aerial'); if (t) t.click(); }")
    pg.wait_for_timeout(3500)
    res["world_pins"] = pg.evaluate("""() => { const v = [...document.querySelectorAll('#nlps .nlw-pin')].filter(e => e.style.display !== 'none');
        return {visible: v.length, withIcon: v.filter(e => e.classList.contains('has-i')).length,
                bareDots: v.filter(e => e.classList.contains('is-dot') && !e.classList.contains('has-i') && !e.classList.contains('k-tower')).length,
                kinds: [...new Set(v.map(e => [...e.classList].find(c => c.startsWith('k-'))))]}; }""")
    pg.evaluate("() => { const s = document.querySelector('#nlps .nlw'); window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 70); }")
    pg.wait_for_timeout(800)
    pg.screenshot(path=os.path.join(OUT, f"{LANG}-{TAG}-4-pins.png"))

    # 4) the area map: scroll to it, let it load, zoom 15.3 on the building, read what Mapbox placed
    pg.evaluate("() => { const m = document.getElementById('nlpjx-map'); if (m) window.scrollTo(0, m.getBoundingClientRect().top + scrollY - 60); }")
    pg.wait_for_timeout(1500)
    for _ in range(6):
        swipe(cdp, 30, 700, 650, 4)
    pg.wait_for_timeout(5000)
    pg.evaluate("() => { const m = window.NLPJX_MAP; if (m) m.jumpTo({zoom: 15.3}); }")
    pg.wait_for_timeout(3500)
    res["map"] = pg.evaluate("""() => { const m = window.NLPJX_MAP; if (!m || !m.getLayer('nlam-pin')) return {layer: false};
        const f = m.queryRenderedFeatures({layers: ['nlam-pin']});
        const L = m.getLayoutProperty('nlam-pin', 'icon-allow-overlap');
        return {layer: true, placed: f.length, zoom: +m.getZoom().toFixed(2), allowOverlap: L,
                images: m.listImages().filter(i => i.startsWith('nlpi-')).length, kinds: [...new Set(f.map(x => x.properties.ic))].slice(0, 30)}; }""")
    pg.evaluate("() => { const m = document.getElementById('nlpjx-unimap') || document.getElementById('nlpjx-map'); window.scrollTo(0, m.getBoundingClientRect().top + scrollY - 70); }")
    pg.wait_for_timeout(1500)
    pg.screenshot(path=os.path.join(OUT, f"{LANG}-{TAG}-3-map.png"))
    # 5) walking on a phone opens full screen; the WhatsApp consult pill is there; leaving full screen goes back to the page
    pg.evaluate("() => { const s = document.querySelector('#nlps .nlw'); window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 70); }")
    pg.wait_for_timeout(600)
    pg.evaluate("() => { const t = [...document.querySelectorAll('#nlps .nlw-tab')].find(b => b.dataset.mode === 'walk'); if (t) t.click(); }")
    pg.wait_for_timeout(3000)
    res["walk_full"] = pg.evaluate("""() => { const w = document.querySelector('.nlw'); const a = document.querySelector('.nlw-wafull'); const r = a ? a.getBoundingClientRect() : null;
        const hit = r ? document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) : null;
        return {full: w.classList.contains('nlw--full'), mode: w.dataset.mode, pill: r ? {w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top)} : null,
                pillOnTop: !!(hit && a && a.contains(hit)), panelInRoot: !!w.querySelector('.nlw-panel'), text: a ? a.textContent : ''}; }""")
    pg.screenshot(path=os.path.join(OUT, f"{LANG}-{TAG}-5-walkfull.png"))
    pg.evaluate("() => document.querySelector('.nlw-fullbtn').click()")
    pg.wait_for_timeout(2500)
    res["after_exit"] = pg.evaluate("() => { const w = document.querySelector('.nlw'); return {full: w.classList.contains('nlw--full'), mode: w.dataset.mode, docked: !!document.querySelector('.nlw-dock .nlw-panel')}; }")
    res["errors"] = errs
    res["served_local"] = sorted(set(served))
    b.close()
json.dump(res, open(os.path.join(OUT, f"{LANG}-{TAG}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
