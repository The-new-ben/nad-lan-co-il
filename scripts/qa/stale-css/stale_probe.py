# -*- coding: utf-8 -*-
"""The owner's phone (2.10.2026 evening): on the live Kikar page the apartment card lay over the 3D and the key plan was a huge black
shape. Cause: world.js loads world.css WITHOUT the module's ?ver (new URL('./world.css', import.meta.url)), and the server sends
max-age=31536000, so a phone that once loaded world.css keeps that old file under the new world.js.
This probe simulates such a phone: any request for world.css with NO query is answered with the 1.72.385 world.css (from git).
  python stale_probe.py <tag> [--fixed]
--fixed swaps world.js with the working tree's (the one-line fix: the CSS carries the module's ?ver), so world.css is asked with
?ver and gets the current file. Nothing is deployed."""
import io, os, sys, time, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TAG = sys.argv[1]; FIXED = "--fixed" in sys.argv
OUT = os.path.join(REPO, "docs", "qa", "stale-css"); os.makedirs(OUT, exist_ok=True)
STALE = os.path.join(OUT, "world-1.72.385.css")
WJS = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.js")
SEEN = []


def route(r):
    u = r.request.url; path = u.split("?")[0]
    if "wa.me" in u or "googletagmanager" in u or "analytics" in u or r.request.method != "GET":
        return r.abort()
    if path.endswith("/project-stage/world/world.css"):
        SEEN.append(u.split("/world/")[1][:40])
        if "?" not in u:
            return r.fulfill(status=200, body=open(STALE, "rb").read(), headers={"content-type": "text/css"})
    if FIXED and path.endswith("/project-stage/world/world.js"):
        return r.fulfill(status=200, body=open(WJS, "rb").read(), headers={"content-type": "application/javascript"})
    return r.continue_()


res = {}
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    for W, H, mob in ((390, 844, True), (1440, 900, False)):
        SEEN.clear()
        kw = dict(viewport={"width": W, "height": H})
        if mob:
            kw.update(is_mobile=True, has_touch=True, device_scale_factor=2)
        ctx = br.new_context(**kw); ctx.route("**/*", route)
        pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        T = pg.touchscreen.tap if mob else pg.mouse.click
        pg.goto("https://nad-lan.co.il/projects/hamedina/?sc=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(4000)
        pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo({ top: s.getBoundingClientRect().top + scrollY - 80, behavior: 'instant' }); }"); pg.wait_for_timeout(1200)
        rr = pg.evaluate("() => { const b = document.querySelector('#nlps .nlw').getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; }")
        T(int(rr[0] + rr[2] / 2), int(rr[1] + min(160, rr[3] / 3))); pg.wait_for_timeout(6500)
        R = {"css_requests": list(SEEN)}
        R["plan"] = pg.evaluate("() => { const s = document.querySelector('#nlps .nlw-plansvg'); if (!s) return null; const r = s.getBoundingClientRect(); const p = s.querySelector('path'); return { w: Math.round(r.width), h: Math.round(r.height), fill: p ? getComputedStyle(p).fill : null }; }")
        R["overlap_panel_on_3d"] = pg.evaluate("""() => { const c = document.querySelector('#nlps .nlw canvas'); const pn = document.querySelector('#nlps .nlw-panel'); if (!c || !pn) return null;
          const a = c.getBoundingClientRect(), b = pn.getBoundingClientRect(); return Math.round(Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) * Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top))); }""")
        pg.screenshot(path=os.path.join(OUT, f"{TAG}-{W}.png"))
        R["errors"] = errs
        res[str(W)] = R
        print(W, json.dumps(R, ensure_ascii=False), flush=True)
        ctx.close()
    br.close()
json.dump(res, open(os.path.join(OUT, f"{TAG}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
