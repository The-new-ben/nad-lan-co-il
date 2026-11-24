import os, sys, time, json
from playwright.sync_api import sync_playwright
ASSET = "/wp-content/plugins/nadlan-config/assets/aurelia-viewer/"; LOCAL = "C:/Users/777/nad-lan/nad-lan-co-il/plugins/nadlan-config/assets/aurelia-viewer/"
CT = {"js": "application/javascript", "css": "text/css", "json": "application/json", "webp": "image/webp", "png": "image/png"}
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    ctx = br.new_context(viewport={"width": 1280, "height": 720}, locale="he-IL")
    def serve(r):
        path = r.request.url.split(ASSET, 1)[1].split("?")[0]
        if not os.path.exists(LOCAL + path): r.continue_(); return
        r.fulfill(status=200, content_type=CT[path.rsplit(".", 1)[1]], body=open(LOCAL + path, "rb").read(), headers={"cache-control": "no-store"})
    ctx.route("**" + ASSET + "**", serve)
    pg = ctx.new_page(); pg.goto("https://nad-lan.co.il/projects/aurelia/?nlv=%d" % int(time.time()), wait_until="load", timeout=120000)
    pg.wait_for_selector("#nlas", state="attached"); pg.wait_for_timeout(2000)
    pg.evaluate("window.scrollTo({top:document.getElementById('nlas').getBoundingClientRect().top+scrollY-130,behavior:'instant'})")
    pg.wait_for_function("window.NLAS && window.__nlas && window.__nlas.interactive", timeout=90000); pg.wait_for_timeout(1500)
    pg.evaluate("NLAS.open('20-2', false)"); pg.wait_for_timeout(6000)
    ctx.route("**/nadlan/v1/room/available*", lambda r: r.fulfill(status=200, content_type="application/json", body=json.dumps({"ok": True, "now": False})))
    b = pg.locator("#nlas .pn-flat .pn-cta .nlas-call"); b.scroll_into_view_if_needed(); pg.wait_for_timeout(600); b.click()
    for i in range(8):
        pg.wait_for_timeout(400); print(i, pg.evaluate("(()=>{const e=document.querySelector('#nlas .pn-callsheet');if(!e)return null;const b=e.getBoundingClientRect();return [Math.round(scrollY),Math.round(b.top),Math.round(b.bottom),e.parentNode.className]})()"))
    print(pg.evaluate("JSON.stringify(window.__nlas.restLog.slice(-4))"))
    print(json.dumps(pg.evaluate("""()=>{const S=document.getElementById('nlas'),q=s=>{const e=S.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return [Math.round(r.top),Math.round(r.bottom)]};
      return {pmh:S.style.getPropertyValue('--nlas-pmh'),tight:S.classList.contains('nlas-tight'),tab:S.querySelector('.pn-media').dataset.tab,media:q('.pn-media'),cut:q('.pn-cut'),sim:q('.pn-media>.pn-sim'),drag:q('.pn-media>.pn-drag'),cta:q('.pn-flat .pn-cta'),price:q('.pn-price'),decl:q('.pn-flat .pn-decl'),scroll:Math.round(scrollY),nlas:q('.nlas-grid')}}""")))
    br.close()
