# -*- coding: utf-8 -*-
"""Live eyes on 1.72.375: the floor view's quiet link -> the example button -> the album with a real picture, phone and desktop.
  python live_example_check.py <he|en|ar|ru|fr> <w>"""
import io, os, sys, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
LANG, W = sys.argv[1], int(sys.argv[2])
URL = "https://nad-lan.co.il/projects/hamedina/" if LANG == "he" else f"https://nad-lan.co.il/projects/hamedina-{LANG}/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "live375"); os.makedirs(OUT, exist_ok=True)
phone = W < 700
res = {"lang": LANG, "w": W}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    kw = dict(viewport={"width": W, "height": 844 if phone else 900})
    if phone:
        kw.update(is_mobile=True, has_touch=True, device_scale_factor=2)
    ctx = b.new_context(**kw)
    ctx.route("**/*", lambda r: r.abort() if ("wa.me" in r.request.url or "analytics" in r.request.url or "googletagmanager" in r.request.url or r.request.method != "GET") else r.continue_())
    pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    reqs = []; pg.on("request", lambda r: reqs.append(r.url) if "/hamedina/tour/" in r.url or "example." in r.url else None)
    pg.goto(URL + "?x375=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3500)
    res["health"] = pg.evaluate("fetch('/wp-json/nadlan/v1/health').then(r => r.json()).then(j => j.version)")
    pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 100); }"); pg.wait_for_timeout(700)
    r = pg.evaluate("() => { const b = document.querySelector('#nlps .nlw').getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; }")
    if phone:
        pg.touchscreen.tap(int(r[0] + r[2] / 2), int(r[1] + 180))
    else:
        pg.mouse.click(int(r[0] + r[2] * 0.6), int(r[1] + r[3] * 0.55))
    pg.wait_for_timeout(7000)
    res["before_press_requests"] = len(reqs)
    pg.evaluate("() => { const t = [...document.querySelectorAll('#nlps .nlw-tab')].find(b => b.dataset.mode === 'tower'); if (t) t.click(); }")
    pg.wait_for_timeout(2500)
    res["quiet_link"] = pg.evaluate("() => { const a = document.querySelector('.nlw-exlink'); return a ? a.textContent.trim() : null; }")
    pg.evaluate("() => { const a = document.querySelector('.nlw-exlink'); if (a) a.click(); }")
    pg.wait_for_timeout(3500)
    res["button"] = pg.evaluate("() => { const x = document.querySelector('.nlw-btn--ex'); return x ? x.textContent.trim() : null; }")
    pg.evaluate("() => { const x = document.querySelector('.nlw-btn--ex'); if (x) x.scrollIntoView({block: 'center'}); }"); pg.wait_for_timeout(600)
    pg.screenshot(path=os.path.join(OUT, f"{LANG}-{W}-1-button.png"))
    pg.evaluate("() => { const x = document.querySelector('.nlw-btn--ex'); if (x) x.click(); }")
    pg.wait_for_timeout(5000)
    res["album"] = pg.evaluate("""() => { const a = document.querySelector('.nlex'); if (!a) return null;
        const imgs = [...a.querySelectorAll('img')]; const main = imgs[0];
        return {open: a.getClientRects().length > 0, title: (a.querySelector('.nlex__title') || {}).textContent, imgs: imgs.length,
                mainLoaded: !!(main && main.complete && main.naturalWidth > 0), mainSrc: main ? main.currentSrc.split('/').pop() : null,
                label: (a.textContent || '').includes('להמחשה') || (a.textContent || '').length > 0,
                wa: !!a.querySelector('a[href*="wa.me"], a[href*="whatsapp"], .nlex__wa, [class*="wa"]')}; }""")
    res["after_press_requests"] = len(reqs)
    pg.screenshot(path=os.path.join(OUT, f"{LANG}-{W}-2-album.png"))
    res["errors"] = errs
    b.close()
print(json.dumps(res, ensure_ascii=False))
