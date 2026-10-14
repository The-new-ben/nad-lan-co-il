import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for tag, vp in (("m", {"width": 390, "height": 844}), ("d", {"width": 1440, "height": 900})):
        ctx = b.new_context(viewport=vp, device_scale_factor=2 if tag == "m" else 1, locale="he-IL", is_mobile=tag == "m", has_touch=tag == "m")
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
        pg.goto("https://nad-lan.co.il/cpi-calculator/?nlpress=%d" % time.time(), wait_until="load", timeout=120000)
        pg.wait_for_selector('[data-nli="cpi"] .nli__fig', timeout=60000)
        h = pg.locator('[data-nli="cpi"]'); h.scroll_into_view_if_needed(); pg.wait_for_timeout(600)
        a0 = h.locator(".nli__fig").inner_text()
        h.locator(".nli__seg button", has_text="המדד בגין החודש").click(); pg.wait_for_timeout(400); a1 = h.locator(".nli__fig").inner_text()
        h.locator(".nli__seg button", has_text="שכר דירה").click(); pg.wait_for_timeout(500)
        vis = [x for x in h.locator(".nli__f").all() if x.is_visible()]
        a2 = h.locator(".nli__fig").inner_text()
        h.locator("details.nli__table summary").click(); pg.wait_for_timeout(300)
        h.screenshot(path=f"live-cpi-{tag}.png")
        top = pg.locator("h1").first.bounding_box()["y"]; tool = h.bounding_box()["y"]
        print(tag, "| sum", a0, "-> for-month", a1, "-> rent", a2, "| visible fields in rent mode", len(vis), "| table rows", h.locator("tbody tr").count(), "| h1 y", int(top), "tool y", int(tool), "| errors", errs[:2])
        ctx.close()
    b.close()
