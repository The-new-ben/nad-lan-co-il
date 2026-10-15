"""Live press after 1.72.457 (Ben 15.10: no names): plot 2206 card shows the phase + the ask button; no name anywhere."""
import time
from playwright.sync_api import sync_playwright
NAMES = ["מבנה נדל", "גינדי", "חג'ג'", "פרשקובסקי", "דמרי", "שיכון ובינוי", "אוטופיה", "ווג", "זיהום"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, locale="he-IL", is_mobile=True, has_touch=True)
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:140]))
    pg.goto("https://nad-lan.co.il/sde-dov/contamination/?nlpress=%d" % time.time(), wait_until="load", timeout=120000)
    pg.wait_for_selector('[data-nli="soilmap"] .nls__card', timeout=60000); pg.wait_for_timeout(6000)
    h = pg.locator('[data-nli="soilmap"]')
    h.locator(".nls__chips button", has_text="2206").first.click(); pg.wait_for_timeout(2500)
    card = h.locator(".nls__card").inner_text().replace("\n", " | ")
    ask = h.locator(".nls__card a.nls__ask").get_attribute("href")
    h.locator(".nls__card").screenshot(path="docs/tools/live-soil-card-2206-m.png")
    main = pg.locator("main, article, .entry-content").first.inner_text() if pg.locator("main, article, .entry-content").count() else pg.inner_text("body")
    found = [n for n in NAMES if n in pg.locator('[data-nli]').evaluate_all("a => a.map(e => e.innerText).join(' ')")]
    print("card:", card[:330]); print("ask:", ask[:120]); print("names inside the tools:", found, "| errors", errs[:2])
    ctx.close(); b.close()
