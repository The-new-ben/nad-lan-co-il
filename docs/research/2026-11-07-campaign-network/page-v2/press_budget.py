import sys, time, json
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for name, vw, mob in (("phone", {"width": 390, "height": 844}, True), ("desktop", {"width": 1280, "height": 900}, False)):
        ctx = b.new_context(viewport=vw, locale="he-IL", device_scale_factor=2 if mob else 1, is_mobile=mob, has_touch=mob)
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
        pg.goto("https://nad-lan.co.il/marketing/?b=%d" % time.time(), wait_until="networkidle", timeout=120000); time.sleep(2)
        box = pg.locator('[data-nli="nlbudget"]').first
        box.scroll_into_view_if_needed(); time.sleep(1)
        before = box.inner_text()[:2000]
        inp = box.locator("input[type=number], input[inputmode=numeric], input[type=text]").first
        try:
            inp.fill("200"); inp.press("Tab"); time.sleep(0.6)
        except Exception as e: errs.append("fill " + str(e)[:80])
        after = box.inner_text()[:2000]
        box.screenshot(path="shots/%s-budget.png" % name)
        y = box.evaluate("e => Math.round(e.getBoundingClientRect().top + scrollY)")
        res[name] = {"budget_y": y, "changed_after_input": before != after, "sw": pg.evaluate("document.documentElement.scrollWidth"),
                     "errors": errs, "head": after[:220].replace("\n", " | ")}
        ctx.close()
    b.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
