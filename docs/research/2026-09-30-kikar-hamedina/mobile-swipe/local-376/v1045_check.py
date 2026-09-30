# -*- coding: utf-8 -*-
"""v104.5 acceptance (Codex's QA items) on the LIVE page, with the local world/areamap swapped in and the page's WhatsApp-bar
control list rewritten to the release's (#nlps input), unless --live.
  python v1045_check.py <he|en|ar> <tag> [--live] [--w 390]
M15 the area map at its OPENING zoom: rendered places, each with its name (text actually placed)
M17 the world (aerial, phone): no icon without its name; tap areas apart
M24 desktop 1440: wheel after a click on the stage scrolls the page, camera still; Ctrl+wheel zooms, page still
bar the WhatsApp bar never over the floor slider while scrolling through the dock (phone)"""
import io, os, sys, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
LANG, TAG = sys.argv[1], sys.argv[2]
LIVE = "--live" in sys.argv
WPH = int(sys.argv[sys.argv.index("--w") + 1]) if "--w" in sys.argv else 390
URL = {"he": "https://nad-lan.co.il/projects/hamedina/", "en": "https://nad-lan.co.il/projects/hamedina-en/",
       "ar": "https://nad-lan.co.il/projects/hamedina-ar/"}[LANG]
PN = r"C:\Users\777\nad-lan\nad-lan-co-il\plugins\nadlan-config"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "v1045"); os.makedirs(OUT, exist_ok=True)
SWAP = {"/assets/project-stage/world/world.js": "assets/project-stage/world/world.js",
        "/assets/project-stage/world/world.css": "assets/project-stage/world/world.css",
        "/assets/arealife/areamap.js": "assets/arealife/areamap.js"}


def route(r):
    u = r.request.url; path = u.split("?")[0]
    if "wa.me" in u or "whatsapp" in u or "google-analytics" in u or "googletagmanager" in u or r.request.method != "GET":
        return r.abort()
    if not LIVE:
        for k, v in SWAP.items():
            if path.endswith(k):
                body = open(os.path.join(PN, v), encoding="utf-8").read()
                return r.fulfill(status=200, body=body, headers={"content-type": ("text/css" if v.endswith(".css") else "application/javascript") + "; charset=utf-8"})
        if r.request.resource_type == "document" and "/projects/hamedina" in path:
            resp = r.fetch(); html = resp.text()
            html = html.replace("#nlps a,#nlps-pick button,", "#nlps a,#nlps input,#nlps-pick button,")
            return r.fulfill(response=resp, body=html)
    return r.continue_()


def swipe(cdp, x, y0, y1, steps=12):
    cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y0}]})
    for i in range(1, steps + 1):
        cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x, "y": y0 + (y1 - y0) * i / steps}]}); time.sleep(0.016)
    cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []}); time.sleep(0.7)


CAM = "() => { const c = window.__nlpsWorld._debug().camera; return [+c.position.x.toFixed(2), +c.position.y.toFixed(2), +c.position.z.toFixed(2)]; }"
res = {"lang": LANG, "live": LIVE, "w": WPH}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    # ---------------- phone
    ctx = b.new_context(viewport={"width": WPH, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2,
                        user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36")
    ctx.route("**/*", route)
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.goto(URL + "?v5=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3500)
    # M15: the area map at its opening zoom (no jumpTo)
    pg.evaluate("() => { const m = document.getElementById('nlpjx-map'); window.scrollTo(0, m.getBoundingClientRect().top + scrollY - 60); }")
    pg.wait_for_timeout(1200)
    for _ in range(5):
        swipe(cdp, 24, 700, 660, 4)
    pg.wait_for_timeout(6000)
    res["M15"] = pg.evaluate("""() => { const m = window.NLPJX_MAP; if (!m || !m.getLayer('nlam-pin')) return null;
        const f = m.queryRenderedFeatures({layers: ['nlam-pin']});
        return {zoom: +m.getZoom().toFixed(2), rendered: f.length, textField: JSON.stringify(m.getLayoutProperty('nlam-pin', 'text-field')), textOptional: m.getLayoutProperty('nlam-pin', 'text-optional'), names: f.slice(0, 10).map(x => x.properties.name)}; }""")
    pg.evaluate("() => { const m = document.getElementById('nlpjx-unimap') || document.getElementById('nlpjx-map'); window.scrollTo(0, m.getBoundingClientRect().top + scrollY - 70); }")
    pg.wait_for_timeout(1200)
    pg.screenshot(path=os.path.join(OUT, f"{LANG}-{TAG}-map-open.png"))
    # M17: the world, aerial, phone
    pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 120); }")
    pg.wait_for_timeout(700)
    r = pg.evaluate("() => document.querySelector('#nlps .nlw').getBoundingClientRect().top")
    pg.touchscreen.tap(WPH // 2, int(r + 180)); pg.wait_for_timeout(7000)
    pg.evaluate("() => { const t = [...document.querySelectorAll('#nlps .nlw-tab')].find(b => b.dataset.mode === 'aerial'); if (t) t.click(); }")
    pg.wait_for_timeout(3000)
    res["M17"] = pg.evaluate("""() => { const v = [...document.querySelectorAll('#nlps .nlw-pin')].filter(e => e.style.display !== 'none');
        const iconNoName = v.filter(e => e.classList.contains('has-i') && (e.classList.contains('is-dot') || getComputedStyle(e.querySelector('.t')).display === 'none'));
        const chips = v.map(e => e.querySelector('.t')).filter(t => t && getComputedStyle(t).display !== 'none').map(t => t.getBoundingClientRect());
        let tapOverlaps = 0; const pad = 7;
        for (let i = 0; i < chips.length; i++) for (let j = i + 1; j < chips.length; j++) { const a = chips[i], b = chips[j];
            if (!(a.right < b.left || a.left > b.right || a.bottom + pad < b.top - pad || a.top - pad > b.bottom + pad)) tapOverlaps++; }
        const icons = v.filter(e => e.classList.contains('has-i')).map(e => e.querySelector('.i').getBoundingClientRect());
        let iconOverlaps = 0;
        for (let i = 0; i < icons.length; i++) for (let j = i + 1; j < icons.length; j++) { const a = icons[i], b = icons[j];
            if (!(a.right <= b.left || a.left >= b.right || a.bottom <= b.top || a.top >= b.bottom)) iconOverlaps++; }
        return {visible: v.length, named: chips.length, withIcon: icons.length, iconWithoutName: iconNoName.length, tapOverlaps, iconOverlaps,
                ariaHidden: v.filter(e => e.querySelector('.i') && e.querySelector('.i').getAttribute('aria-hidden') === 'true').length}; }""")
    pg.evaluate("() => { const s = document.querySelector('#nlps .nlw'); window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 70); }")
    pg.wait_for_timeout(900)
    pg.screenshot(path=os.path.join(OUT, f"{LANG}-{TAG}-world-aerial.png"))
    # the bar vs the floor slider, scrolling through the dock in the floor view
    pg.evaluate("() => { const t = [...document.querySelectorAll('#nlps .nlw-tab')].find(b => b.dataset.mode === 'tower'); if (t) t.click(); }")
    pg.wait_for_timeout(2000)
    top = pg.evaluate("() => document.querySelector('.nlw-dock').getBoundingClientRect().top + scrollY")
    hits = []
    for dy in range(-700, 500, 40):
        pg.evaluate(f"() => window.scrollTo(0, {int(top) + dy})"); pg.wait_for_timeout(350)
        o = pg.evaluate("""() => { const bar = document.querySelector('#nlcta'); const s = document.querySelector('.nlw-dock input.nlw-range');
            if (!bar || !s) return null; const a = bar.getBoundingClientRect(), b = s.getBoundingClientRect();
            const x = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)), y = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
            return x * y; }""")
        if o: hits.append(dy)
    res["bar_on_slider_positions"] = len(hits)
    res["errors_phone"] = errs
    ctx.close()
    # ---------------- M24 desktop
    ctx = b.new_context(viewport={"width": 1440, "height": 1000})
    ctx.route("**/*", route)
    pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.goto(URL + "?v5d=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3500)
    pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 100); }")
    pg.wait_for_timeout(700)
    rr = pg.evaluate("() => { const b = document.querySelector('#nlps .nlw').getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; }")
    cx, cy = int(rr[0] + rr[2] * 0.6), int(rr[1] + rr[3] * 0.55)
    pg.mouse.click(cx, cy); pg.wait_for_timeout(7000)       # enter the world (the poster)
    pg.mouse.click(cx, cy - 120); pg.wait_for_timeout(1500)  # a plain click on the stage (the M24 case)
    c0 = pg.evaluate(CAM); y0 = pg.evaluate("Math.round(scrollY)")
    pg.mouse.move(cx, cy); pg.mouse.wheel(0, 260); pg.wait_for_timeout(1500)
    c1 = pg.evaluate(CAM); y1 = pg.evaluate("Math.round(scrollY)")
    res["M24_wheel"] = {"page_px": y1 - y0, "camera_moved": c0 != c1}
    pg.evaluate(f"() => window.scrollTo(0, {y0})"); pg.wait_for_timeout(600)
    c0 = pg.evaluate(CAM); y0 = pg.evaluate("Math.round(scrollY)")
    pg.keyboard.down("Control"); pg.mouse.move(cx, cy); pg.mouse.wheel(0, -260); pg.wait_for_timeout(200); pg.keyboard.up("Control"); pg.wait_for_timeout(1500)
    c1 = pg.evaluate(CAM); y1 = pg.evaluate("Math.round(scrollY)")
    res["M24_ctrl_wheel"] = {"page_px": y1 - y0, "camera_moved": c0 != c1}
    res["hint"] = pg.evaluate("() => { const h = document.querySelector('.nlw-hint'); return h ? {hidden: h.hidden, text: h.textContent} : null; }")
    res["M19_tabs"] = pg.evaluate("""() => { const t = [...document.querySelectorAll('#nlps .nlw-tab')]; t.forEach(x => x.style.fontSize = '30px');
        const r = t.map(x => [x.scrollWidth, x.clientWidth, Math.round(x.getBoundingClientRect().height)]); t.forEach(x => x.style.fontSize = ''); return r; }""")
    res["errors_desktop"] = errs
    b.close()
json.dump(res, open(os.path.join(OUT, f"{LANG}-{TAG}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
