"""Step 2c (HAD-810): the furnished plan with room names and sizes opens large. python press_plan.py WxH [OUT]  (LIVE=1 = live page)
Per sample (5 rooms 20-2, 3 rooms, 6 rooms): open the flat, open the plan large (phones: the band's plan button; desktop: the
button on the picture), check every room label sits on the picture, phones list the rooms, desktop keeps the tower on screen."""
import json, os, sys, time
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = [int(x) for x in sys.argv[1].split("x")]; phone = W < 900; LIVE = os.environ.get("LIVE") == "1"
OUT = os.path.join(HERE, sys.argv[2] if len(sys.argv) > 2 else "local10"); os.makedirs(OUT, exist_ok=True)
ASSET = "/wp-content/plugins/nadlan-config/assets/aurelia-viewer/"
LOCAL = "C:/Users/777/nad-lan/nad-lan-co-il/plugins/nadlan-config/assets/aurelia-viewer/"
CT = {"js": "application/javascript", "css": "text/css", "json": "application/json", "webp": "image/webp", "png": "image/png"}
res = {"vp": sys.argv[1], "live": LIVE, "steps": [], "errors": []}
def step(n, ok, **kw):
    res["steps"].append(dict(step=n, ok=bool(ok), **kw)); print(("OK  " if ok else "BAD ") + n, json.dumps(kw, ensure_ascii=False)[:300], flush=True)
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    kw = dict(viewport={"width": W, "height": H}, device_scale_factor=2 if phone else 1, locale="he-IL")
    if phone: kw.update(is_mobile=True, has_touch=True)
    ctx = br.new_context(**kw)
    if not LIVE:
        def serve(r):
            path = r.request.url.split(ASSET, 1)[1].split("?")[0]
            if not os.path.exists(LOCAL + path): r.continue_(); return
            r.fulfill(status=200, content_type=CT[path.rsplit(".", 1)[1]], body=open(LOCAL + path, "rb").read(), headers={"cache-control": "no-store"})
        ctx.route("**" + ASSET + "**", serve)
    pg = ctx.new_page()
    pg.on("console", lambda m: res["errors"].append(m.text[:200]) if m.type == "error" and "status of 404" not in m.text else None)
    pg.on("pageerror", lambda e: res["errors"].append("PAGEERROR " + str(e)[:200]))
    pg.goto("https://nad-lan.co.il/projects/aurelia/?nlv=%d" % int(time.time()), wait_until="load", timeout=120000)
    pg.wait_for_selector("#nlas", state="attached", timeout=90000); pg.wait_for_timeout(2500)
    pg.evaluate("window.scrollTo({top:document.getElementById('nlas').getBoundingClientRect().top+scrollY-%d,behavior:'instant'})" % (60 if phone else 124))
    pg.wait_for_function("window.NLAS && window.__nlas && window.__nlas.interactive", timeout=90000); pg.wait_for_timeout(1500)
    for fid, rooms in (("20-2", 5), ("20-7", 3), ("46-1", 6), ("47-1", 6)):
        ok = pg.evaluate("NLAS.open('%s', false)" % fid); pg.wait_for_timeout(2500)
        if not ok: step("flat %s exists" % fid, False); continue
        if phone:
            pg.evaluate("window.scrollTo({top:document.getElementById('nlas').getBoundingClientRect().top+scrollY-60,behavior:'instant'})"); pg.wait_for_timeout(400)
            pg.locator("#nlas .bd-pic").tap()
        else:
            pg.evaluate("NLAS.tab('cut')"); pg.wait_for_timeout(500)
            if not pg.evaluate("document.getElementById('nlas').classList.contains('nlas-planbig')"): pg.locator("#nlas .pn-bigbtn").click()
        pg.wait_for_timeout(1800)
        g = pg.evaluate("""()=>{const box=document.querySelector('#nlas .pn-cutbox');if(!box)return null;const b=box.getBoundingClientRect();
          const L=[...box.querySelectorAll('.pn-room')].map(e=>{const r=e.getBoundingClientRect();return {t:e.innerText.replace(/\s+/g,' '),in:r.left>=b.left-1&&r.right<=b.right+1&&r.top>=b.top-1&&r.bottom<=b.bottom+1,w:Math.round(r.width)}});
          let ov=0;const R=[...box.querySelectorAll('.pn-room')].map(e=>e.getBoundingClientRect());for(let i=0;i<R.length;i++)for(let j=i+1;j<R.length;j++){const a=R[i],c=R[j];if(Math.min(a.right,c.right)-Math.max(a.left,c.left)>1&&Math.min(a.bottom,c.bottom)-Math.max(a.top,c.top)>1)ov++}
          const st=document.querySelector('#nlas .nlas-stage').getBoundingClientRect();
          return {big:document.getElementById('nlas').classList.contains('nlas-planbig'),pic:[Math.round(b.left),Math.round(b.top),Math.round(b.width),Math.round(b.height)],labels:L,overlap:ov,
            legend:[...document.querySelectorAll('#nlas .pn-legend li')].filter(e=>e.offsetParent).map(e=>e.innerText),stage:[Math.round(st.left),Math.round(st.top),Math.round(st.width),Math.round(st.height)]}}""")
        pg.wait_for_timeout(5200)
        rest = pg.evaluate("NLAS.rest()")
        g2 = pg.evaluate("""()=>{const out=[];const B=[...document.querySelectorAll('body *')].filter(e=>!document.getElementById('nlas').contains(e)&&getComputedStyle(e).position==='fixed').map(e=>e.getBoundingClientRect()).filter(r=>r.width>=40&&r.height>=30&&r.height<=200&&r.top>innerHeight*.5&&r.top<innerHeight);
          for(const e of document.querySelectorAll('#nlas button, #nlas a[href], #nlas [role=tab]')){if(e.closest('.mapboxgl-marker,.mapboxgl-popup,.mapboxgl-ctrl'))continue;const r=e.getBoundingClientRect();if(r.width<8||r.height<8||r.bottom<=0||r.top>=innerHeight)continue;
            for(const b of B){const ox=Math.min(r.right,b.right)-Math.max(r.left,b.left),oy=Math.min(r.bottom,b.bottom)-Math.max(r.top,b.top);if(ox>1&&oy>1&&!(r.left>=b.left-1&&r.right<=b.right+1&&r.top>=b.top-1&&r.bottom<=b.bottom+1))out.push((e.innerText||e.getAttribute('aria-label')||e.className).trim().slice(0,30)+' @'+Math.round(r.top)+'-'+Math.round(r.bottom)+' bar '+Math.round(b.top))}}
          return out}""")
        pg.screenshot(path=os.path.join(OUT, "%s%s-plan-%s.png" % ("live-" if LIVE else "", sys.argv[1], fid)))
        step("%s: at rest no showroom button sits half under the site's bars" % fid, not g2, half=g2, rest=rest, sy=pg.evaluate("Math.round(scrollY)"), log=None if not g2 else pg.evaluate("window.__nlas.restLog"))
        step("%s (%d rooms): plan large" % (fid, rooms), g and g["big"], pic=g and g["pic"])
        step("%s: a label for every room + the balcony, all on the picture, none on another" % fid, g and len(g["labels"]) == rooms + 2 + (1 if rooms >= 6 else 0) + 1 and all(x["in"] for x in g["labels"]) and g["overlap"] == 0, labels=g and [x["t"] for x in g["labels"]], overlap=g and g["overlap"])
        if phone: step("%s: the rooms listed under the picture" % fid, g and len(g["legend"]) >= rooms, legend=g and g["legend"])
        else: step("%s: the tower stays on screen beside the plan" % fid, g and g["stage"][2] >= 380 and g["stage"][1] + g["stage"][3] > 200 and g["stage"][1] < H - 200, stage=g and g["stage"], pic=g and g["pic"])
    step("console errors", not res["errors"], errors=res["errors"][:5])
    br.close()
json.dump(res, open(os.path.join(OUT, "press-plan-%s%s.json" % ("live-" if LIVE else "", sys.argv[1])), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("BAD:", sum(1 for s in res["steps"] if not s["ok"]), "of", len(res["steps"]))
