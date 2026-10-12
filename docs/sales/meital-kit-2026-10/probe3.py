import sys, time
from playwright.sync_api import sync_playwright
slug, x, y = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    c = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2, locale="he-IL")
    pg = c.new_page()
    pg.goto(f"https://nad-lan.co.il/projects/{slug}/?nlshot={int(time.time())}", wait_until="load", timeout=120000)
    pg.wait_for_timeout(8000)
    pg.click("button.rbs-open"); pg.wait_for_timeout(6000)
    pg.mouse.click(x, y); pg.wait_for_timeout(5000)
    pg.screenshot(path=f"shots/{slug}-d-floor.png")
    steps = pg.query_selector_all("button.nlps-step")
    if len(steps) > 1:
        steps[1].click(); pg.wait_for_timeout(6000)
        pg.screenshot(path=f"shots/{slug}-d-step2.png")
        v = pg.query_selector("#nlps-view")
        if v: v.screenshot(path=f"shots/{slug}-d-view2.png")
    if len(steps) > 2:
        steps[2].click(); pg.wait_for_timeout(8000)
        pg.screenshot(path=f"shots/{slug}-d-step3.png")
    b.close()
