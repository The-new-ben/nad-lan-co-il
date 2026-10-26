# -*- coding: utf-8 -*-
"""Local preview checks for G6 G7 G8 (no live site touched): open a local page at 390 and 1280 px in Edge (playwright), full-page
screenshot, console errors, sideways scroll (document wider than the viewport), and the tools mounted.
  python shot.py <url> <name> [--widths 390,1280] [--out preview/shots]   prints a JSON report and writes PNGs."""
import json, os, sys, time
from playwright.sync_api import sync_playwright

H = os.path.dirname(os.path.abspath(__file__))
url, name = sys.argv[1], sys.argv[2]
widths = [int(x) for x in (sys.argv[sys.argv.index("--widths") + 1] if "--widths" in sys.argv else "390,1280").split(",")]
out = os.path.join(H, sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else os.path.join(H, "preview", "shots")
os.makedirs(out, exist_ok=True)
rep = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for w in widths:
        ctx = b.new_context(viewport={"width": w, "height": 900}, device_scale_factor=1, locale="he-IL", is_mobile=w < 600, has_touch=w < 600)
        pg = ctx.new_page(); errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
        pg.goto(url, wait_until="networkidle", timeout=90000)
        time.sleep(1.2)
        info = pg.evaluate("""() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, h: document.documentElement.scrollHeight,
            tools: [...document.querySelectorAll('[data-nli]')].map(e => [e.getAttribute('data-nli'), !!e.querySelector('.nli__answer'), (e.querySelector('.nli__fig')||{}).textContent || '']),
            wide: [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.right > document.documentElement.clientWidth + 1 || r.left < -1) && getComputedStyle(e).position !== 'fixed' && !e.closest('.nli__tw,.nlbd-t,.nlsm-t,.nlod-t,[style*="overflow"]'); }).slice(0, 6).map(e => e.tagName + '.' + (e.className && e.className.baseVal === undefined ? e.className : '') + ' ' + Math.round(e.getBoundingClientRect().right))})""")
        f = os.path.join(out, "%s-%d.png" % (name, w))
        pg.screenshot(path=f, full_page=True)
        rep.append({"width": w, "scrollWidth": info["sw"], "clientWidth": info["cw"], "sideways": info["sw"] > info["cw"], "height": info["h"], "tools": info["tools"], "wide": info["wide"], "console_errors": errs, "png": f})
        ctx.close()
    b.close()
print(json.dumps(rep, ensure_ascii=False, indent=1))
