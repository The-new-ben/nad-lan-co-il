"""Live press after 1.72.459 (Mission A): project chip card, green buildings on the map, no names inside the tools."""
import time
from playwright.sync_api import sync_playwright
NAMES = ["מבנה נדל", "גינדי", "חג'ג'", "פרשקובסקי", "דמרי", "שיכון ובינוי", "אוטופיה", "ווג", "אביסרור", "ישראל קנדה", "נחמיאס", "ריינבו", "אשירה", "זיהום"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for tag, vp in (("d", {"width": 1440, "height": 900}), ("m", {"width": 390, "height": 844})):
        ctx = b.new_context(viewport=vp, device_scale_factor=1 if tag == "d" else 2, locale="he-IL", is_mobile=tag == "m", has_touch=tag == "m")
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:140]))
        pg.goto("https://nad-lan.co.il/sde-dov/contamination/?nlpress=%d" % time.time(), wait_until="load", timeout=120000)
        pg.wait_for_selector('[data-nli="soilmap"] .nls__card', timeout=60000); pg.wait_for_timeout(7000)
        h = pg.locator('[data-nli="soilmap"]')
        h.locator(".nls__chips button", has_text="111 ·").first.click(); pg.wait_for_timeout(3500)
        card = h.locator(".nls__card").inner_text().replace("\n", " | ")
        h.locator(".nls__stage").screenshot(path=f"docs/tools/live-soil-green-{tag}.png")
        found = [n for n in NAMES if n in pg.locator('[data-nli]').evaluate_all("a => a.map(e => e.innerText).join(' ')")]
        print(tag, "| card 111:", card[:220], "| names:", found, "| errors", errs[:2])
        ctx.close()
    b.close()
