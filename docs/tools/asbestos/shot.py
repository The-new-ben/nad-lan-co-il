"""Local press of the asbestos page harness (docs/tools/asbestos/harness.html): phone and desktop, every tool pressed."""
import functools, http.server, os, threading
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
H.log_message = lambda *a, **k: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 47933), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
OUT = os.path.join(ROOT, "docs", "qa", "asbestos"); os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for tag, vp in (("m", {"width": 390, "height": 844}), ("d", {"width": 1366, "height": 900})):
        ctx = b.new_context(viewport=vp, device_scale_factor=2 if tag == "m" else 1, locale="he-IL", is_mobile=tag == "m", has_touch=tag == "m")
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        pg.on("console", lambda m: errs.append("console:" + m.text[:160]) if m.type == "error" else None)
        pg.goto("http://127.0.0.1:47933/docs/tools/asbestos/harness.html", wait_until="load"); pg.wait_for_timeout(9000)
        pg.screenshot(path=os.path.join(OUT, f"harness-top-{tag}.png"))
        pg.locator(".asbh").first.screenshot(path=os.path.join(OUT, f"harness-hero-{tag}.png"))
        c = pg.locator('[data-nli="asbcheck"]')
        r0 = c.locator(".asbx__out").inner_text()[:90].replace("\n", " | ")
        c.locator("button[data-v=debris]").click(); c.locator("button[data-v=crumbling]").click(); pg.wait_for_timeout(300)
        r1 = c.locator(".asbx__out").inner_text()[:140].replace("\n", " | ")
        c.locator("button[data-v=planter]").click(); c.locator("button[data-v=cracked]").click(); pg.wait_for_timeout(300)
        r2 = c.locator(".asbx__out").inner_text()[:160].replace("\n", " | ")
        c.screenshot(path=os.path.join(OUT, f"harness-check-{tag}.png"))
        k = pg.locator('[data-nli="asbcost"]'); a0 = k.locator(".nli__fig").inner_text().replace("\n", " ")
        k.locator(".nli__seg button", has_text="החלפת גג").click(); pg.wait_for_timeout(300); a1 = k.locator(".nli__fig").inner_text().replace("\n", " ")
        k.screenshot(path=os.path.join(OUT, f"harness-cost-{tag}.png"))
        w = pg.locator('[data-nli="asbwho"]'); w0 = w.locator(".asbw__out").inner_text()[:160].replace("\n", " | ")
        w.locator("input").fill("נהרייה"); pg.wait_for_timeout(300); w1 = w.locator(".asbw__card").inner_text()[:120].replace("\n", " | ")
        w.screenshot(path=os.path.join(OUT, f"harness-who-{tag}.png"))
        mp = pg.locator('[data-nli="asbmap"]'); canvas = mp.locator("canvas.maplibregl-canvas").count()
        mp.locator(".asbm__chips button", has_text="לימן").click(); pg.wait_for_timeout(3000)
        mp.screenshot(path=os.path.join(OUT, f"harness-map-{tag}.png"))
        sw = pg.evaluate("document.documentElement.scrollWidth")
        print(tag, "| scrollWidth", sw, "| canvas", canvas, "\n  check start:", r0, "\n  debris+crumbling:", r1, "\n  planter+cracked:", r2,
              "\n  cost:", a0, "\n  roof:", a1, "\n  who start:", w0, "\n  who nahariya:", w1, "\n  errors", errs[:5])
        ctx.close()
    b.close()
srv.shutdown()
