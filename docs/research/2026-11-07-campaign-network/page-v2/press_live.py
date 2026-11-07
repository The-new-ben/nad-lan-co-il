import sys, time, json
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
URL = "https://nad-lan.co.il/marketing/?x=%d" % time.time()
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for name, vw in (("phone", {"width": 390, "height": 844}), ("desktop", {"width": 1280, "height": 900})):
        ctx = b.new_context(viewport=vw, locale="he-IL", device_scale_factor=2 if name == "phone" else 1, is_mobile=(name == "phone"), has_touch=(name == "phone"))
        pg = ctx.new_page(); errs = []
        pg.on("console", lambda m: errs.append(m.text[:160]) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append("PAGEERR " + str(e)[:160]))
        pg.goto(URL, wait_until="networkidle", timeout=120000); time.sleep(2)
        r = pg.evaluate("""() => { const h1 = document.querySelector('h1'); const tool = document.querySelector('[data-nli="nlcamp"], .nlcp, #nlcamp');
          return { sw: document.documentElement.scrollWidth, vw: innerWidth, h1: h1 ? h1.innerText.slice(0,80) : null, h1y: h1 ? Math.round(h1.getBoundingClientRect().top + scrollY) : null,
                   tool: !!tool, tooly: tool ? Math.round(tool.getBoundingClientRect().top + scrollY) : null, h2: document.querySelectorAll('h2').length,
                   tables: document.querySelectorAll('table').length, faq: [...document.querySelectorAll('script[type="application/ld+json"]')].some(s => s.textContent.includes('FAQPage')) } }""")
        pg.screenshot(path="shots/%s-top.png" % name)
        steps = []
        try:
            tool = pg.locator(".nlcp").first; tool.scroll_into_view_if_needed(); time.sleep(1)
            pg.screenshot(path="shots/%s-planner.png" % name)
            for k in range(4):
                btn = pg.locator(".nlcp button", has_text="המשיכו").first
                if btn.count() == 0: break
                btn.click(); time.sleep(0.8); steps.append(pg.locator(".nlcp").first.inner_text()[:40].replace("\n", " "))
            pg.screenshot(path="shots/%s-planner-last.png" % name)
        except Exception as e:
            steps.append("ERR " + str(e)[:120])
        r["steps"] = steps; r["errors"] = errs[:8]; out[name] = r
        ctx.close()
    b.close()
print(json.dumps(out, ensure_ascii=False, indent=1))
