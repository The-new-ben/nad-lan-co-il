# the world card's height on a phone, before (live) and after (local): open tower C's card by tapping its name label
import os, sys, json, time
LIVE = "--live" in sys.argv; SHOT = sys.argv[1]
sys.argv = ["x", "he", "cp"] + (["--live"] if LIVE else [])
src = open("v1045_check.py", encoding="utf-8").read()
exec(src[:src.index("CAM = ")])
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    ctx.route("**/*", route)
    pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.goto(URL + "?cp=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3000)
    pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 120); }"); pg.wait_for_timeout(600)
    r = pg.evaluate("() => document.querySelector('#nlps .nlw').getBoundingClientRect().top")
    pg.touchscreen.tap(195, int(r + 180)); pg.wait_for_timeout(7000)
    pg.evaluate("() => { const t = [...document.querySelectorAll('#nlps .nlw-tab')].find(b => b.dataset.mode === 'aerial'); if (t) t.click(); }"); pg.wait_for_timeout(3000)
    ok = pg.evaluate("""() => { const t = [...document.querySelectorAll('#nlps .nlw-pin.k-tower .t')].find(x => x.offsetParent !== null && getComputedStyle(x).display !== 'none'); if (!t) return false; t.click(); return true; }""")
    pg.wait_for_timeout(1500)
    info = pg.evaluate("""() => { const c = document.querySelector('.nlw-card'); if (!c || c.hidden) return null; const r = c.getBoundingClientRect();
        const f = c.querySelector('.nlw-more'); return {h: Math.round(r.height), fold: !!f, foldOpen: f ? f.open : null, facts: c.querySelectorAll('.nlw-facts li').length,
        title: (c.querySelector('.nlw-title') || {}).textContent}; }""")
    pg.evaluate("() => { const c = document.querySelector('.nlw-card'); if (c) c.scrollIntoView({block: 'start'}); window.scrollBy(0, -60); }"); pg.wait_for_timeout(700)
    pg.locator(".nlw-card").screenshot(path=f"v1045/card-{SHOT}.png")
    print(json.dumps({"live": LIVE, "opened": ok, "card": info, "errors": errs}, ensure_ascii=False))
    b.close()
