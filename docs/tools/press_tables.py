"""Every Instruments table on a phone (390px): open the detail table, measure box vs content width, count errors."""
import time
from playwright.sync_api import sync_playwright
PAGES = ["/new-projects/construction-input-index/", "/new-projects/contractor-delay-compensation/", "/cpi-calculator/",
         "/mortgage-calculator/mortgage-interest-rates/", "/real-estate-lawyer/construction-defects-lawsuit/"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, locale="he-IL", is_mobile=True, has_touch=True)
    for u in PAGES:
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:100]))
        pg.goto("https://nad-lan.co.il" + u + "?nlpress=%d" % time.time(), wait_until="load", timeout=120000)
        pg.wait_for_selector(".nli .nli__fig", timeout=60000)
        h = pg.locator(".nli").first
        t = h.locator("details.nli__table")
        if t.count() and t.is_visible():
            t.locator("summary").click(); pg.wait_for_timeout(300)
            box = t.locator(".nli__tw").evaluate("e => [e.clientWidth, e.scrollWidth]")
            cols = t.locator("thead th").evaluate_all("a => a.filter(x => getComputedStyle(x).display !== 'none').length")
            if "construction-input" in u:
                h.screenshot(path="docs/tools/live-indexation-m.png")
        else:
            box, cols = None, 0
        print(u, "| answer", h.locator(".nli__fig").inner_text(), "| table box/content", box, "| visible columns", cols, "| errors", errs[:2])
        pg.close()
    b.close()
