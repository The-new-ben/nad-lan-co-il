"""761 debug: pills, markers and symbol layers under them in the compact phone map (local module)."""
import json, os, sys, time
from playwright.sync_api import sync_playwright
W, H = [int(x) for x in sys.argv[1].split("x")]
URL = "https://nad-lan.co.il/projects/aurelia/?nlv=%d#dira=20-2" % int(time.time())
ASSET = "/wp-content/plugins/nadlan-config/assets/aurelia-viewer/"
LOCAL = "C:/Users/777/nad-lan/nad-lan-co-il/plugins/nadlan-config/assets/aurelia-viewer/"
CT = {"js": "application/javascript", "css": "text/css", "json": "application/json", "webp": "image/webp", "png": "image/png"}
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    ctx = br.new_context(viewport={"width": W, "height": H}, locale="he-IL")
    def serve(r):
        path = r.request.url.split(ASSET, 1)[1].split("?")[0]
        if not os.path.exists(LOCAL + path): r.continue_(); return
        r.fulfill(status=200, content_type=CT[path.rsplit(".", 1)[1]], body=open(LOCAL + path, "rb").read(), headers={"cache-control": "no-store"})
    ctx.route("**" + ASSET + "**", serve)
    pg = ctx.new_page(); pg.goto(URL, wait_until="load", timeout=120000)
    pg.wait_for_function("window.NLAS && NLAS.state().mode==='flat'", timeout=90000); pg.wait_for_timeout(9000)
    pg.evaluate("window.scrollTo({top:document.getElementById('nlas').getBoundingClientRect().top+scrollY-124,behavior:'instant'})"); pg.wait_for_timeout(1500)
    print(json.dumps(pg.evaluate("""()=>{const fl=document.querySelector('#nlas .pn-flat');return {pmh:document.getElementById('nlas').style.getPropertyValue('--nlas-pmh'),pn:[...fl.children].map(e=>{const r=e.getBoundingClientRect();return [e.className,Math.round(r.top),Math.round(r.bottom),Math.round(r.left),Math.round(r.right)]})}}"""), ensure_ascii=False))
    pg.screenshot(path="local9/dbg761.png"); br.close()
