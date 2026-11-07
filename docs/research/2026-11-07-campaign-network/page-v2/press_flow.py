import sys, time, json
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
T = ".nlcp"
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for name, vw, mob in (("phone", {"width": 390, "height": 844}, True), ("desktop", {"width": 1280, "height": 900}, False)):
        ctx = b.new_context(viewport=vw, locale="he-IL", device_scale_factor=2 if mob else 1, is_mobile=mob, has_touch=mob)
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
        pg.goto("https://nad-lan.co.il/marketing/?y=%d" % time.time(), wait_until="networkidle", timeout=120000)
        pg.locator(T).first.scroll_into_view_if_needed(); time.sleep(1)
        cnt = lambda: pg.locator(T + " .nlcp__count").first.inner_text().strip()
        nxt = lambda: (pg.locator(T + ' button[data-act="next"]').first.click(), pg.wait_for_timeout(300))
        log = [cnt()]
        pg.locator(T + ' button.nlcp__chip[data-m="fr"]').first.click(); pg.locator(T + ' button.nlcp__chip[data-m="us"]').first.click()
        rec = pg.locator(T + ' [data-o="rec"]').first.inner_text(); nxt(); log.append(cnt())
        pg.locator(T + " label.nlcp__card").nth(1).click(); nxt(); log.append(cnt())
        nxt(); log.append(cnt())
        log.append("s4cards=%d" % pg.locator(T + " label.nlcp__card").count()); pg.locator(T + " label.nlcp__card").first.click(); pg.wait_for_timeout(300)
        pg.locator(T + ' input[data-f="ref"]').first.fill("פרויקט בדיקה"); nxt(); log.append(cnt())
        pg.locator(T).first.scroll_into_view_if_needed(); time.sleep(0.6)
        pg.locator(T).first.screenshot(path="shots/%s-step5.png" % name)
        res[name] = {"steps": log, "rec": rec, "step5": pg.locator(T + " h3.nlcp__h").first.inner_text(), "errors": errs,
                     "sw": pg.evaluate("document.documentElement.scrollWidth"), "pay_text": pg.locator(T).first.inner_text()[-260:].replace("\n", " | ")}
        ctx.close()
    b.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
