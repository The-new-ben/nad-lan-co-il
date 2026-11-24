"""761 debug: pills, markers and symbol layers under them in the compact phone map (local module)."""
import json, os, sys, time
from playwright.sync_api import sync_playwright
W, H = 390, 844
URL = "https://nad-lan.co.il/projects/aurelia/?nlv=%d#dira=20-2" % int(time.time())
ASSET = "/wp-content/plugins/nadlan-config/assets/aurelia-viewer/"
LOCAL = "C:/Users/777/nad-lan/nad-lan-co-il/plugins/nadlan-config/assets/aurelia-viewer/"
CT = {"js": "application/javascript", "css": "text/css", "json": "application/json", "webp": "image/webp", "png": "image/png"}
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    ctx = br.new_context(viewport={"width": W, "height": H}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="he-IL")
    def serve(r):
        path = r.request.url.split(ASSET, 1)[1].split("?")[0]
        if not os.path.exists(LOCAL + path): r.continue_(); return
        r.fulfill(status=200, content_type=CT[path.rsplit(".", 1)[1]], body=open(LOCAL + path, "rb").read(), headers={"cache-control": "no-store"})
    ctx.route("**" + ASSET + "**", serve)
    pg = ctx.new_page(); pg.goto(URL, wait_until="load", timeout=120000)
    pg.wait_for_function("window.NLAS && NLAS.state().mode==='flat'", timeout=90000); pg.wait_for_timeout(9000)
    print(json.dumps(pg.evaluate("""()=>{const c=document.getElementById('nlpjx-unimap');const map=window.NLPJX_MAP;
      const pills=[...c.querySelectorAll('.mapboxgl-marker')].map(m=>{const r=m.getBoundingClientRect();let L=[];try{L=[...new Set(map.queryRenderedFeatures([[r.left-c.getBoundingClientRect().left,r.top-c.getBoundingClientRect().top],[r.right-c.getBoundingClientRect().left,r.bottom-c.getBoundingClientRect().top]]).map(f=>f.layer.id))]}catch(e){}
        return {k:m.dataset.nlas,cls:m.className.slice(0,60),txt:m.textContent.trim().slice(0,12),t:Math.round(r.top),l:Math.round(r.left),w:Math.round(r.width),h:Math.round(r.height),tr:m.style.translate,hide:m.classList.contains('nlas-hide'),L}});
      const layers=map.getStyle().layers.filter(l=>l.type==='symbol'&&!/^(road|poi|place|settlement|water|airport|transit|natural|state|country|continent|building|housenum|aeroway|ferry|golf)/.test(l.id)).map(l=>l.id);
      return {pills,layers,cr:c.getBoundingClientRect().top,scroll:scrollY}}"""), ensure_ascii=False, indent=0))
    pg.screenshot(path="local9/dbg761.png"); br.close()
