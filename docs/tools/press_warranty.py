import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for tag, vp in (("m", {"width": 390, "height": 844}), ("d", {"width": 1440, "height": 900})):
        ctx = b.new_context(viewport=vp, device_scale_factor=2 if tag == "m" else 1, locale="he-IL", is_mobile=tag == "m", has_touch=tag == "m")
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
        pg.goto("https://nad-lan.co.il/real-estate-lawyer/construction-defects-lawsuit/?nlpress=%d" % time.time(), wait_until="load", timeout=120000)
        pg.wait_for_selector('[data-nli="warranty"] .nli__fig', timeout=60000)
        h = pg.locator('[data-nli="warranty"]'); h.scroll_into_view_if_needed(); pg.wait_for_timeout(600)
        a0 = h.locator(".nli__fig").inner_text()
        h.locator("input[type=date]").first.fill("2020-01-10"); h.locator("input[type=date]").first.dispatch_event("change"); pg.wait_for_timeout(500)
        a1 = h.locator(".nli__fig").inner_text()
        h.locator("details.nli__table summary").click(); pg.wait_for_timeout(300)
        tw = h.locator(".nli__tw").evaluate("e => [e.clientWidth, e.scrollWidth]")
        h.screenshot(path=f"live-warranty-{tag}.png")
        top = pg.locator("h1").first.bounding_box()["y"]; tool = h.bounding_box()["y"]
        print(tag, "| answer", a0, "-> after handover 10.1.2020:", a1, "| table rows", h.locator("tbody tr").count(), "| table box/content", tw,
              "| h1 y", int(top), "tool y", int(tool), "| errors", errs[:2])
        ctx.close()
    b.close()
