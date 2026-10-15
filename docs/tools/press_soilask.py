"""Live presses of the letter generator on /sde-dov/contamination/ (HAD-534): phone + desktop."""
import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for tag, vp in (("m", {"width": 390, "height": 844}), ("d", {"width": 1440, "height": 900})):
        ctx = b.new_context(viewport=vp, device_scale_factor=2 if tag == "m" else 1, locale="he-IL", is_mobile=tag == "m", has_touch=tag == "m")
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:140]))
        pg.goto("https://nad-lan.co.il/sde-dov/contamination/?nlpress=%d" % time.time(), wait_until="load", timeout=120000)
        pg.wait_for_selector('[data-nli="soilask"] .nli__doc', timeout=60000)
        h = pg.locator('[data-nli="soilask"]'); h.scroll_into_view_if_needed(); pg.wait_for_timeout(500)
        a0 = h.locator(".nli__fig").inner_text(); d0 = h.locator(".nli__doc").inner_text().split("\n")[0]
        h.locator("select").select_option("303"); pg.wait_for_timeout(400); s1 = h.locator(".nli__asub").inner_text()
        h.locator(".nli__seg button", has_text="וואטסאפ").click(); pg.wait_for_timeout(400); a2 = h.locator(".nli__fig").inner_text(); d2 = h.locator(".nli__doc").inner_text()[:90].replace("\n", " | ")
        h.locator(".nli__seg button", has_text="מכתב מלא").click(); pg.wait_for_timeout(300)
        h.screenshot(path=f"docs/tools/live-soilask-{tag}.png")
        print(tag, "| start", a0, "|", d0, "| plot 303:", s1, "| wa:", a2, d2, "| errors", errs[:2])
        ctx.close()
    b.close()
