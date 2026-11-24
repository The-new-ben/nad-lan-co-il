import json, os, sys, time
from playwright.sync_api import sync_playwright
W, H = [int(x) for x in sys.argv[1].split("x")]; phone = W < 900
ASSET = "/wp-content/plugins/nadlan-config/assets/aurelia-viewer/"
LOCAL = "C:/Users/777/nad-lan/nad-lan-co-il/plugins/nadlan-config/assets/aurelia-viewer/"
CT = {"js": "application/javascript", "css": "text/css", "json": "application/json", "webp": "image/webp", "png": "image/png"}
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    kw = dict(viewport={"width": W, "height": H}, device_scale_factor=2 if phone else 1, locale="he-IL")
    if phone: kw.update(is_mobile=True, has_touch=True)
    ctx = br.new_context(**kw)
    def serve(r):
        path = r.request.url.split(ASSET, 1)[1].split("?")[0]
        if not os.path.exists(LOCAL + path): r.continue_(); return
        r.fulfill(status=200, content_type=CT[path.rsplit(".", 1)[1]], body=open(LOCAL + path, "rb").read(), headers={"cache-control": "no-store"})
    ctx.route("**" + ASSET + "**", serve)
    pg = ctx.new_page()
    pg.on("console", lambda m: print("CONSOLE", m.type, m.text[:300]) if m.type in ("error","warning") else None)
    pg.on("pageerror", lambda e: print("PAGEERROR", str(e)[:400]))
    pg.goto("https://nad-lan.co.il/projects/aurelia/?nlv=%d" % int(time.time()), wait_until="load", timeout=120000)
    pg.wait_for_selector("#nlas", state="attached", timeout=90000); pg.wait_for_timeout(2500)
    pg.evaluate("window.scrollTo({top:document.getElementById('nlas').getBoundingClientRect().top+scrollY-60,behavior:'instant'})")
    pg.wait_for_function("window.NLAS && window.__nlas && window.__nlas.interactive", timeout=90000); pg.wait_for_timeout(1500)
    pg.evaluate("NLAS.open('20-2', false)"); pg.wait_for_timeout(2500)
    pg.evaluate("window.scrollTo({top:document.getElementById('nlas').getBoundingClientRect().top+scrollY-60,behavior:'instant'})"); pg.wait_for_timeout(400)
    if phone: pg.locator("#nlas .bd-pic").tap()
    else:
        pg.evaluate("NLAS.tab('cut')"); pg.wait_for_timeout(500)
        if not pg.evaluate("document.getElementById('nlas').classList.contains('nlas-planbig')"): pg.locator("#nlas .pn-bigbtn").click()
    for i in range(14):
        pg.wait_for_timeout(700)
        print(i, pg.evaluate("[Math.round(scrollY), JSON.stringify(NLAS.rest().score), [...document.querySelectorAll('#nlcta, #nlcta *, #nl-sticky, #nla11y')].filter(e=>getComputedStyle(e).position==='fixed').map(e=>e.id+e.className.toString().slice(0,20)+':'+Math.round(e.getBoundingClientRect().top)).join(' ')]"))
    print(json.dumps(pg.evaluate("window.__nlas.restLog"), ensure_ascii=False, indent=0))
    pg.screenshot(path="local11/dbg762-%s.png" % sys.argv[1])
    br.close()
