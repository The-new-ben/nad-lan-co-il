"""Local press of the soil map + PFAS calculator (harness_soil.html): phone and desktop, a chip, a search, a plot tap."""
import functools, http.server, os, threading
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
H.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 47932), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
OUT = os.path.join(ROOT, "docs", "tools", "_harness"); os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for tag, vp in (("m", {"width": 390, "height": 844}), ("d", {"width": 1366, "height": 900})):
        ctx = b.new_context(viewport=vp, device_scale_factor=2 if tag == "m" else 1, locale="he-IL", is_mobile=tag == "m", has_touch=tag == "m")
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
        pg.on("console", lambda m: errs.append("console:" + m.text[:160]) if m.type == "error" else None)
        pg.goto("http://127.0.0.1:47932/tools/instruments/harness_soil.html", wait_until="load"); pg.wait_for_timeout(9000)
        h = pg.locator('[data-nli="soilmap"]')
        c0 = h.locator(".nls__card").inner_text()[:80].replace("\n", " | ")
        h.locator(".nls__chips button", has_text="2206").first.click(); pg.wait_for_timeout(2500)
        c1 = h.locator(".nls__card").inner_text()[:80].replace("\n", " | ")
        h.locator(".nls__chips button", has_text="101").first.click(); pg.wait_for_timeout(2500)
        c2 = h.locator(".nls__card").inner_text()[:80].replace("\n", " | ")
        h.locator(".nls__q input").fill("2227"); h.locator(".nls__q input").press("Enter"); pg.wait_for_timeout(2500)
        c3 = h.locator(".nls__card").inner_text()[:120].replace("\n", " | ")
        canvas = h.locator("canvas.maplibregl-canvas").count()
        h.locator(".nls__chips button", has_text="303").first.click(); pg.wait_for_timeout(3000)
        h.screenshot(path=os.path.join(OUT, f"soil-{tag}.png"))
        q = pg.locator('[data-nli="pfas"]'); q.screenshot(path=os.path.join(OUT, f"pfas-{tag}.png"))
        a = q.locator(".nli__fig").inner_text()
        print(tag, "| canvas", canvas, "| start:", c0, "\n  chip 2206:", c1, "\n  search דמרי:", c2, "\n  search 2227:", c3, "\n  pfas:", a, "| errors", errs[:4])
        ctx.close()
    b.close()
srv.shutdown()
