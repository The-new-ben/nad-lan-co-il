import sys, json, time, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
LANG = sys.argv[1]
URL = f"https://nad-lan.co.il/projects/hamedina-{LANG}/"
names = json.load(open("named_en.json", encoding="utf-8"))
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    ctx.route("**/*", lambda r: r.abort() if ("wa.me" in r.request.url or "analytics" in r.request.url or "googletagmanager" in r.request.url or r.request.method != "GET") else r.continue_())
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.goto(URL + "?nm=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3000)
    pg.evaluate("() => { const m = document.getElementById('nlpjx-map'); window.scrollTo(0, m.getBoundingClientRect().top + scrollY - 60); }"); pg.wait_for_timeout(1000)
    for _ in range(5):
        cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": 24, "y": 700}]})
        for i in range(1, 5): cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": 24, "y": 700 - 10 * i}]}); time.sleep(0.016)
        cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []}); time.sleep(0.6)
    pg.wait_for_timeout(7000)
    # open the whole list so every place shows
    for _ in range(12):
        if not pg.evaluate("() => { const m = document.querySelector('.nlam-more'); if (m) { m.click(); return true; } return false; }"): break
        pg.wait_for_timeout(300)
    txt = pg.evaluate("() => (document.querySelector('.nlam-list') || {}).innerText || ''")
    feats = pg.evaluate("() => { const m = window.NLPJX_MAP; if (!m) return []; m.jumpTo({zoom: 15.6}); return []; }")
    pg.wait_for_timeout(3500)
    onmap = pg.evaluate("() => { const m = window.NLPJX_MAP; return m ? m.queryRenderedFeatures({layers: ['nlam-pin']}).map(f => f.properties.name) : []; }")
    found = [n for n in names if n in txt]
    generic = sum(1 for line in txt.split("\n") if line.strip() in ("School", "Café", "Restaurant", "Kindergarten", "Bus stop", "Shop", "Clinic", "Park"))
    pg.evaluate("() => { const m = document.getElementById('nlpjx-unimap'); window.scrollTo(0, m.getBoundingClientRect().top + scrollY - 70); }"); pg.wait_for_timeout(1500)
    pg.screenshot(path=f"v1045/names-{LANG}.png")
    print(json.dumps({"lang": LANG, "named_in_list": found, "of": len(names), "generic_lines": generic, "on_map_named": [n for n in onmap if n in names], "errors": errs}, ensure_ascii=False))
    b.close()
