# -*- coding: utf-8 -*-
"""HAD-390 local extras (ConsultBand applied to the HTML): the bar is the element under its own centre and asks for WhatsApp (the
request is caught, never sent); the accessibility button opens its panel fully on screen; the album, the 360 viewer and the
world's full screen cover the band; a resize to 1440 drops the band; Rainbow and DUO keep the floating bar (no band)."""
import io, os, sys, time, json, importlib.util
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
spec = importlib.util.spec_from_file_location("band_hunks", os.path.join(REPO, "scripts", "project-stage", "consult_band_396.py"))
bh = importlib.util.module_from_spec(spec); spec.loader.exec_module(bh)
OUT = os.path.join(REPO, "docs", "qa", "had-390"); os.makedirs(OUT, exist_ok=True)
APPLIED = {}; WA = []


def route(r):
    u = r.request.url
    if "wa.me" in u or "api.whatsapp" in u:
        WA.append(u[:60]); return r.abort()
    if "analytics" in u or "googletagmanager" in u or "hotjar" in u or r.request.method != "GET":
        return r.abort()
    if r.request.resource_type == "document":
        resp = r.fetch(); body = resp.text()
        for name, old, new in bh.HTML_HUNKS:
            APPLIED.setdefault(r.request.url.split("?")[0], {})[name] = body.count(old); body = body.replace(old, new)
        return r.fulfill(response=resp, body=body)
    return r.continue_()


BAND = "() => { const b = document.getElementById('nlcta').getBoundingClientRect(); return { band: b.width >= innerWidth * 0.9 && b.bottom >= innerHeight - 2, top: Math.round(b.top), h: Math.round(b.height) }; }"
TOPAT = "([x, y]) => { const e = document.elementFromPoint(x, y); return e ? (e.closest('#nlcta') ? 'nlcta' : e.closest('#nla11y') ? 'a11y' : (e.closest('.nlex') ? 'album' : e.closest('.nlat-viewer') ? 'viewer' : e.closest('.nlw--full') ? 'world-full' : e.tagName + '.' + String(e.className).slice(0, 20))) : null; }"
APT = "[...document.querySelectorAll('#nlps .nlw-apt')].find((x) => /צפון-מערבית/.test(x.getAttribute('aria-label')))"
res = {}
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    ctx = br.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2); ctx.route("**/*", route)
    pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.goto("https://nad-lan.co.il/projects/hamedina/?bx=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(4000)
    R = res["he-390"] = {"band_at_load": pg.evaluate(BAND)}
    wa = pg.evaluate("() => { const r = document.querySelector('#nlcta .nlcta-wa').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2, Math.round(r.width), Math.round(r.height)]; }")
    R["wa_box"] = wa[2:]; R["wa_center_is"] = pg.evaluate(TOPAT, wa[:2])
    pg.touchscreen.tap(int(wa[0]), int(wa[1])); pg.wait_for_timeout(1500)
    for x in ctx.pages[1:]:
        try:
            WA.append("popup:" + x.url[:50]); x.close()
        except Exception:
            pass
    R["wa_tap_requested_whatsapp"] = WA[:2]
    ac = pg.evaluate("() => { const r = document.getElementById('nla11y-btn').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }")
    R["a11y_center_is"] = pg.evaluate(TOPAT, ac)
    pg.touchscreen.tap(int(ac[0]), int(ac[1])); pg.wait_for_timeout(800)
    R["a11y_panel"] = pg.evaluate("() => { const p = document.getElementById('nla11y-panel'); if (!p || p.hidden) return null; const r = p.getBoundingClientRect(); return { top: Math.round(r.top), bottom: Math.round(r.bottom), inView: r.top >= 0 && r.bottom <= innerHeight && r.left >= 0 && r.right <= innerWidth }; }")
    pg.screenshot(path=os.path.join(OUT, "x-a11y-panel.png"))
    pg.touchscreen.tap(int(ac[0]), int(ac[1])); pg.wait_for_timeout(600)
    pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo({ top: s.getBoundingClientRect().top + scrollY - 80, behavior: 'instant' }); }"); pg.wait_for_timeout(1200)
    rr = pg.evaluate("() => { const b = document.querySelector('#nlps .nlw').getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; }")
    pg.touchscreen.tap(int(rr[0] + rr[2] / 2), int(rr[1] + 160)); pg.wait_for_timeout(6500)
    R["world_full"] = pg.evaluate(TOPAT, [200, 820]) if pg.evaluate("() => !!document.querySelector('#nlps .nlw--full')") else "not full (inline world)"
    pg.evaluate("() => " + APT + ".scrollIntoView({ block: 'center', behavior: 'instant' })"); pg.wait_for_timeout(1200)
    b = pg.evaluate("() => { const t = " + APT + ".querySelector('text').getBoundingClientRect(); return [t.left + t.width / 2, t.top + t.height / 2 + 8]; }")
    pg.touchscreen.tap(int(b[0]), int(b[1])); pg.wait_for_timeout(2500)
    pg.evaluate("() => document.querySelector('#nlps [data-example]').scrollIntoView({ block: 'center', behavior: 'instant' })"); pg.wait_for_timeout(1200)
    b = pg.evaluate("() => { const r = document.querySelector('#nlps [data-example]').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }")
    pg.touchscreen.tap(int(b[0]), int(b[1])); pg.wait_for_timeout(3500)
    R["album_over_band"] = pg.evaluate(TOPAT, [120, 820])
    b = pg.evaluate("() => { const e = document.querySelector('.nlex [data-pano]'); e.scrollIntoView({ block: 'center', behavior: 'instant' }); const r = e.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }"); pg.wait_for_timeout(800)
    pg.touchscreen.tap(int(b[0]), int(b[1])); pg.wait_for_timeout(6000)
    R["viewer_over_band"] = pg.evaluate(TOPAT, [120, 820])
    pg.screenshot(path=os.path.join(OUT, "x-viewer.png"))
    R["errors"] = errs
    ctx.close()
    ctx = br.new_context(viewport={"width": 390, "height": 844}); ctx.route("**/*", route)
    pg = ctx.new_page(); pg.goto("https://nad-lan.co.il/projects/hamedina-en/?bx=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3500)
    a = pg.evaluate(BAND); pg.set_viewport_size({"width": 1440, "height": 1000}); pg.wait_for_timeout(1500)
    res["resize_en"] = {"390": a, "1440": pg.evaluate(BAND), "padB_1440": pg.evaluate("() => getComputedStyle(document.body).paddingBottom")}
    ctx.close()
    for slug in ("rainbow-tel-aviv", "duo-tel-aviv"):
        ctx = br.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2); ctx.route("**/*", route)
        pg = ctx.new_page(); e2 = []; pg.on("pageerror", lambda e: e2.append(str(e)[:200]))
        pg.goto(f"https://nad-lan.co.il/projects/{slug}/?bx=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(4000)
        res[slug] = {"band": pg.evaluate(BAND), "padB": pg.evaluate("() => getComputedStyle(document.body).paddingBottom"), "errors": e2}
        ctx.close()
    br.close()
res["applied_per_document"] = APPLIED
print(json.dumps(res, ensure_ascii=False, indent=1))
