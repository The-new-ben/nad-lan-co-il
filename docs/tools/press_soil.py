"""Live presses of /sde-dov/contamination/ (HAD-534): phone + desktop, the map draws, a chip, a project search, any plot, the calculator."""
import time
from playwright.sync_api import sync_playwright
U = "https://nad-lan.co.il/sde-dov/contamination/"
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for tag, vp in (("m", {"width": 390, "height": 844}), ("d", {"width": 1440, "height": 900})):
        ctx = b.new_context(viewport=vp, device_scale_factor=2 if tag == "m" else 1, locale="he-IL", is_mobile=tag == "m", has_touch=tag == "m")
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:140]))
        pg.goto(U + "?nlpress=%d" % time.time(), wait_until="load", timeout=120000)
        pg.wait_for_selector('[data-nli="soilmap"] .nls__card', timeout=60000); pg.wait_for_timeout(7000)
        h = pg.locator('[data-nli="soilmap"]')
        canvas = h.locator("canvas.maplibregl-canvas").count()
        y_h1 = pg.locator("h1").first.bounding_box()["y"]; y_tool = h.bounding_box()["y"]
        c0 = h.locator(".nls__card .nls__ct").inner_text()
        h.locator(".nls__chips button", has_text="2206").first.click(); pg.wait_for_timeout(2500); c1 = h.locator(".nls__card .nls__ct").inner_text()
        h.locator(".nls__q input").fill("דמרי ים"); h.locator(".nls__q input").press("Enter"); pg.wait_for_timeout(2500); c2 = h.locator(".nls__card .nls__ct").inner_text()
        h.locator(".nls__q input").fill("2227"); h.locator(".nls__q input").press("Enter"); pg.wait_for_timeout(2500); c3 = h.locator(".nls__card").inner_text()[:140].replace("\n", " | ")
        h.locator(".nls__chips button", has_text="303").first.click(); pg.wait_for_timeout(3500)
        h.screenshot(path=f"docs/tools/live-soil-{tag}.png")
        q = pg.locator('[data-nli="pfas"]'); a0 = q.locator(".nli__fig").inner_text()
        q.locator(".nli__seg button", has_text="מיליגרם").click(); pg.wait_for_timeout(400); a1 = q.locator(".nli__fig").inner_text()
        q.screenshot(path=f"docs/tools/live-pfas-{tag}.png")
        tw = pg.evaluate("[...document.querySelectorAll('.nli__tw')].map(e => e.clientWidth + '/' + e.scrollWidth)")
        print(tag, "| map canvas", canvas, "| h1 y", int(y_h1), "map tool y", int(y_tool), "| start", c0, "| chip", c1, "| project", c2, "\n   any plot:", c3,
              "\n   pfas", a0, "-> as mg/kg", a1, "| tables", tw, "| errors", errs[:3])
        ctx.close()
    b.close()
