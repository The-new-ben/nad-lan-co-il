# -*- coding: utf-8 -*-
"""WCAG 2.2 SC 2.4.11 ("Focus Not Obscured") on the Kikar Hamedina world page (HAD-375, loop turn 18): scroll through the open tower
card in the phone's dock every 20 px (75 positions) and count the positions where the site's floating buttons (the accessibility
button #nla11y-btn, the WhatsApp bar #nlcta) cover a fold heading (#nlps summary) by more than 40 px2.
Each jump dispatches a scroll event, as a real finger's scroll does (a bare scrollTo jump under-fires the buttons' scroll logic and
made the first measurement pessimistic).
  python tools/fold_obscure_check.py [he|en|fr|ru|ar] [--before]   (--before: the page's control lists without '#nlps summary')
Measured 1.10.2026 on the live 1.72.380, he 390: a11y 15 -> 2, bar 10 -> 7 (before -> after); en the same."""
import sys, json, time, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
LANG = sys.argv[1] if len(sys.argv) > 1 else "he"
URL = "https://nad-lan.co.il/projects/hamedina/" if LANG == "he" else f"https://nad-lan.co.il/projects/hamedina-{LANG}/"
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    BASE = "--before" in sys.argv
    def route(r):
        u = r.request.url
        if "wa.me" in u or "analytics" in u or "googletagmanager" in u or r.request.method != "GET":
            return r.abort()
        if BASE and r.request.resource_type == "document" and "/projects/hamedina" in u:
            resp = r.fetch(); h = resp.text().replace("#nlps-view-cta a,#nlps summary')", "#nlps-view-cta a')").replace("#nlps .nlw-enter,#nlps summary'", "#nlps .nlw-enter'")
            return r.fulfill(response=resp, body=h)
        return r.continue_()
    ctx.route("**/*", route)
    pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.goto(URL + "?fl=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3000)
    ver = pg.evaluate("fetch('/wp-json/nadlan/v1/health').then(r => r.json()).then(j => j.version)")
    pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 120); }"); pg.wait_for_timeout(600)
    r = pg.evaluate("() => document.querySelector('#nlps .nlw').getBoundingClientRect().top")
    pg.touchscreen.tap(195, int(r + 180)); pg.wait_for_timeout(7000)
    pg.evaluate("() => { const t = [...document.querySelectorAll('#nlps .nlw-tab')].find(b => b.dataset.mode === 'aerial'); if (t) t.click(); }"); pg.wait_for_timeout(2500)
    pg.evaluate("() => { const t = [...document.querySelectorAll('#nlps .nlw-pin.k-tower .t')].find(x => x.offsetParent !== null && getComputedStyle(x).display !== 'none'); if (t) t.click(); }"); pg.wait_for_timeout(1200)
    top = pg.evaluate("() => { const c = document.querySelector('.nlw-dock .nlw-card'); return c ? c.getBoundingClientRect().top + scrollY : null; }")
    hits = {"a11y": 0, "bar": 0}; n = 0
    for dy in range(-800, 700, 20):
        pg.evaluate(f"() => {{ window.scrollTo(0, {int(top) + dy}); window.dispatchEvent(new Event('scroll')); }}"); pg.wait_for_timeout(420); n += 1
        o = pg.evaluate("""() => { const S = [...document.querySelectorAll('#nlps summary')].map(e => e.getBoundingClientRect()).filter(q => q.height && q.bottom > 0 && q.top < innerHeight);
            const ov = (a, q) => Math.max(0, Math.min(a.right, q.right) - Math.max(a.left, q.left)) * Math.max(0, Math.min(a.bottom, q.bottom) - Math.max(a.top, q.top));
            const A = document.getElementById('nla11y-btn'), B = document.querySelector('#nlcta');
            const a = A ? A.getBoundingClientRect() : null, bb = B ? B.getBoundingClientRect() : null;
            return {a11y: a ? S.some(q => ov(a, q) > 40) : false, bar: bb ? S.some(q => ov(bb, q) > 40) : false}; }""")
        hits["a11y"] += bool(o["a11y"]); hits["bar"] += bool(o["bar"])
    print(json.dumps({"lang": LANG, "before": BASE, "version": ver, "positions": n, "covering_a_fold_heading": hits, "errors": errs}, ensure_ascii=False))
    b.close()
