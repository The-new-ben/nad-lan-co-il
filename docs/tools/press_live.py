import time
from playwright.sync_api import sync_playwright
U = {"indexation": "https://nad-lan.co.il/new-projects/construction-input-index/", "delay": "https://nad-lan.co.il/new-projects/contractor-delay-compensation/"}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for tag, vp in (("m", {"width": 390, "height": 844}), ("d", {"width": 1440, "height": 900})):
        ctx = b.new_context(viewport=vp, device_scale_factor=2 if tag == "m" else 1, locale="he-IL", is_mobile=tag == "m", has_touch=tag == "m")
        for tool, url in U.items():
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
            pg.goto(url + "?nlpress=%d" % time.time(), wait_until="load", timeout=120000)
            pg.wait_for_selector('[data-nli="%s"] .nli__fig' % tool, timeout=60000)
            host = pg.locator('[data-nli="%s"]' % tool)
            host.scroll_into_view_if_needed(); pg.wait_for_timeout(800)
            a0 = host.locator(".nli__fig").inner_text()
            if tool == "indexation":
                f = host.locator("input").first; f.fill("3500000"); pg.wait_for_timeout(400)
                host.locator(".nli__seg button", has_text="20/80").click(); pg.wait_for_timeout(400)
                host.locator(".nli__scen button").nth(2).click(); pg.wait_for_timeout(400)
            else:
                host.locator(".nli__seg button", has_text="נמסרה").last.click(); pg.wait_for_timeout(300)
                host.locator('input[type="date"]').nth(2).fill("2026-03-01"); pg.wait_for_timeout(400)
            a1 = host.locator(".nli__fig").inner_text()
            host.locator("details.nli__table summary").click(); pg.wait_for_timeout(300)
            host.screenshot(path=f"live-{tool}-{tag}.png")
            fam = pg.evaluate("()=>getComputedStyle(document.querySelector('.nli__fig')).fontFamily")
            print(tag, tool, "| before", a0, "-> after", a1, "| rows", host.locator("details.nli__table tbody tr").count(), "| font", fam.split(",")[0], "| errors", errs[:2])
            pg.close()
        ctx.close()
    b.close()
