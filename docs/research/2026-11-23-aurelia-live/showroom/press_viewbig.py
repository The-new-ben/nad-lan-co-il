import json,os,sys,time
from playwright.sync_api import sync_playwright
ASSET="/wp-content/plugins/nadlan-config/assets/aurelia-viewer/"; LOCAL="C:/Users/777/nad-lan/nad-lan-co-il/plugins/nadlan-config/assets/aurelia-viewer/"
OUT="C:/Users/777/nad-lan/nad-lan-co-il/docs/research/2026-11-23-aurelia-live/showroom/local8/"; os.makedirs(OUT,exist_ok=True)
LIVE=os.environ.get("LIVE")=="1"; pre="live-" if LIVE else ""
CT={"js":"application/javascript","css":"text/css","json":"application/json","webp":"image/webp","png":"image/png"}
errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(channel="chrome",headless=True,args=["--use-angle=swiftshader","--enable-unsafe-swiftshader"])
    for W,H in ((1440,900),(390,844)):
        ph=W<900; kw=dict(viewport={"width":W,"height":H},locale="he-IL")
        if ph: kw.update(is_mobile=True,has_touch=True,device_scale_factor=2,user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Mobile Safari/537.36")
        ctx=br.new_context(**kw)
        def serve(r):
            path=r.request.url.split(ASSET,1)[1].split("?")[0]
            if not os.path.exists(LOCAL+path): r.continue_(); return
            r.fulfill(status=200,content_type=CT[path.rsplit(".",1)[1]],body=open(LOCAL+path,"rb").read())
        if not LIVE: ctx.route("**"+ASSET+"**",serve)
        pg=ctx.new_page(); pg.on("console",lambda m: errs.append(m.text[:150]) if m.type=="error" and "404" not in m.text else None)
        pg.goto("https://nad-lan.co.il/projects/aurelia/?nlv=%d"%time.time(),wait_until="load",timeout=120000)
        pg.wait_for_selector("#nlas",state="attached",timeout=90000); pg.wait_for_timeout(2500)
        pg.evaluate("window.scrollTo(0,document.getElementById('nlas').getBoundingClientRect().top+scrollY-130)")
        pg.wait_for_function("window.__nlas && window.__nlas.interactive",timeout=90000)
        pg.evaluate("NLAS.open('20-5',false)"); pg.wait_for_timeout(2500)
        pg.locator("#nlas .pn-tabs [data-tab=view]").click(); pg.wait_for_timeout(3500)
        r=pg.evaluate("""()=>{const v=document.querySelector('#nlas .nlas-viewbig');const b=v&&!v.hidden?v.getBoundingClientRect():null;return {big:b?[Math.round(b.width),Math.round(b.height),Math.round(b.top)]:null,tags:v?v.querySelectorAll('.pn-tag:not([hidden])').length:0,small:document.querySelectorAll('#nlas .nlas-panel .pn-tag:not([hidden])').length}}""")
        print(W,"view",r)
        pg.screenshot(path=OUT+pre+"%dx%d-b-view.png"%(W,H))
        if r["big"] and r["tags"]:
            t=pg.locator("#nlas .nlas-viewbig .pn-tag:not([hidden])").first; bb=t.bounding_box(); pg.mouse.click(bb["x"]+10,bb["y"]+bb["height"]/2); pg.wait_for_timeout(1200)
            print(W,"card",pg.evaluate("(()=>{const c=document.querySelector('#nlas .nlas-viewbig .pn-tagcard');return c&&!c.hidden?c.innerText.slice(0,60):null})()"))
            pg.screenshot(path=OUT+pre+"%dx%d-b-view-tag.png"%(W,H))
            pg.locator("#nlas .pn-tabs [data-tab=plan]").click(); pg.wait_for_timeout(600)
            print(W,"closed on plan tab",pg.evaluate("document.querySelector('#nlas .nlas-viewbig').hidden"))
        ctx.close()
    br.close()
print("errors",errs[:5])
