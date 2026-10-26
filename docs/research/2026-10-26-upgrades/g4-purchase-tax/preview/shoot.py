# -*- coding: utf-8 -*-
"""G4 local preview: serves the repo root on 127.0.0.1 and opens preview/index.html (the page content with the real ptax v3 tool)
at 390 and 1280 px in Chrome; reports console errors, sideways scroll, the rendered order, and presses the tool (presets, a track,
the partner, the oleh date, late weeks) and saves screenshots next to this file.
  python docs/research/2026-10-26-upgrades/g4-purchase-tax/preview/shoot.py"""
import functools, http.server, os, sys, threading
from playwright.sync_api import sync_playwright
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H)))))
PORT = 47944


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), functools.partial(Quiet, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = "http://127.0.0.1:%d/docs/research/2026-10-26-upgrades/g4-purchase-tax/preview/index.html" % PORT
ok_all = True
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for w, h, tag in ((390, 844, "m"), (1280, 900, "d")):
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2 if tag == "m" else 1)
        errs = []
        pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
        pg.on("console", lambda m: m.type == "error" and "Failed to load resource" not in m.text and errs.append("console: " + m.text))
        pg.on("response", lambda rs: rs.status >= 400 and not rs.url.endswith("/favicon.ico") and errs.append("http %d %s" % (rs.status, rs.url)))
        pg.goto(URL, wait_until="networkidle"); pg.wait_for_timeout(1200)
        sw = pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
        wide = pg.evaluate("""() => { const W = document.documentElement.clientWidth; const out = [];
          document.querySelectorAll('body *').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && (r.right > W + 1 || r.left < -1)) {
            let x = e; let clipped = false; while (x && x !== document.body) { const cs = getComputedStyle(x); if (/(auto|scroll|hidden)/.test(cs.overflowX) && x !== e) { clipped = true; break; } x = x.parentElement; }
            if (!clipped) out.push(e.tagName + '.' + (e.className && e.className.baseVal === undefined ? e.className : '') + ' ' + Math.round(r.left) + '..' + Math.round(r.right)); } });
          return out.slice(0, 8); }""")
        order = pg.evaluate("""() => { const y = s => { const e = document.querySelector(s); return e ? Math.round(e.getBoundingClientRect().top + scrollY) : -1; };
          return {h1: y('h1'), answer: y('h1 ~ p'), cta: y('.nlg4-cta'), tool: y('.nli__panel'), brackets: y('#brackets'), late: y('#late'), faq: y('.nadlan-guide')}; }""")
        ans = pg.locator(".nli__fig").first.inner_text()
        print("[%s %dx%d] answer %s | scrollWidth %s vs %s | order %s" % (tag, w, h, ans, sw[0], sw[1], order))
        if wide: print("   elements past the edge:", wide)
        pg.screenshot(path=os.path.join(H, "page-%s-top.png" % tag))
        tool = pg.locator(".nli__panel").first
        tool.screenshot(path=os.path.join(H, "tool-%s-default.png" % tag))
        # press: the partners preset, then an oleh with an aliyah date, then 6 weeks late
        pg.locator(".nli__pre button[data-k='partners']").click(); pg.wait_for_timeout(300)
        r1 = pg.locator(".nli__lines").first.inner_text()
        tool.screenshot(path=os.path.join(H, "tool-%s-partners.png" % tag))
        pg.locator(".nli__seg button", has_text="עולה חדש").first.click(); pg.wait_for_timeout(200)
        pg.locator(".nli__f", has_text="תאריך העלייה").locator("input").fill("2023-05-01"); pg.wait_for_timeout(300)
        r2 = pg.locator(".nli__note").first.inner_text()
        tool.screenshot(path=os.path.join(H, "tool-%s-oleh.png" % tag))
        late_in = pg.locator(".nli__f", has_text="ואם תשלמו באיחור").locator("input")
        late_in.fill("6"); pg.wait_for_timeout(300)
        r3 = pg.locator(".nli__lines").first.inner_text()
        print("   partners lines:", " | ".join(x for x in r1.split("\n") if "הקונה השני" in x or "שני הקונים" in x or x.startswith("₪")))
        print("   oleh note has regulation 12 choice:", "תקנה 12 (" in r2, "| late line:", [x for x in r3.split("\n") if "שבועות" in x][:2])
        for sel, name in (("#i1", "i1"), ("#i2", "i2"), ("#i3", "i3"), ("#cities", "cities")):
            el = pg.locator(sel)
            el.scroll_into_view_if_needed(); pg.wait_for_timeout(150)
            if name == "cities": pg.screenshot(path=os.path.join(H, "page-%s-cities.png" % tag))
            else: el.screenshot(path=os.path.join(H, "fig-%s-%s.png" % (tag, name)))
        sw2 = pg.evaluate("document.documentElement.scrollWidth")
        print("   console errors:", errs or "none", "| scrollWidth after pressing:", sw2)
        ok_all = ok_all and not errs and sw[0] <= sw[1] and sw2 <= sw[1] and not wide
        pg.close()
    b.close()
srv.shutdown()
print("PREVIEW OK" if ok_all else "PREVIEW HAS ISSUES")
