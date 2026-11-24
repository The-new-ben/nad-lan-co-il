"""HAD-823: press Rainbow / Ashira / DUO as a visitor: tap the tower, "הנוף והמפה" (phones 5 times), the map under the stage, the beam
turned to the flat's side, a second side. python press.py <tag> [rainbow ashira duo] [--sizes=...] [--mock=<bridge.js>]
Frames + press.json into <tag>/. Read-only on the site (analytics and WhatsApp hosts blocked)."""
import json, os, sys, time
from playwright.sync_api import sync_playwright
OUT = os.path.dirname(os.path.abspath(__file__))
PAGES = {"rainbow": "https://nad-lan.co.il/projects/rainbow-tel-aviv/", "ashira": "https://nad-lan.co.il/projects/ashira-sde-dov/", "duo": "https://nad-lan.co.il/projects/duo-tel-aviv/"}
args = [a for a in sys.argv[1:] if not a.startswith('--')]
tag = args[0]; only = args[1:] or list(PAGES)
SIZES = ["390x844", "360x740", "1280x720", "1440x900"]; MOCK = None; REP = 5
for a in sys.argv[1:]:
    if a.startswith('--sizes='): SIZES = a.split('=', 1)[1].split(',')
    if a.startswith('--mock='): MOCK = a.split('=', 1)[1]
    if a.startswith('--repeat='): REP = int(a.split('=', 1)[1])
PHONE_UA = "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Mobile Safari/537.36"
BLOCK = ("google-analytics", "googletagmanager", "hotjar", "clarity.ms", "facebook", "doubleclick", "wa.me", "api.whatsapp")
INIT = "window.__ev=[];for(const n of ['nl:floor','nl:facing'])addEventListener(n,e=>{try{window.__ev.push([n,e.detail])}catch(_){}});"
GEO = r"""()=>{
 const R=e=>{if(!e)return null;const b=e.getBoundingClientRect();return {t:Math.round(b.top),b:Math.round(b.bottom),y:Math.round(b.top+scrollY),h:Math.round(b.height),l:Math.round(b.left),w:Math.round(b.width)}};
 const vis=e=>{if(!e)return false;const c=getComputedStyle(e),b=e.getBoundingClientRect();return b.width>0&&b.height>0&&c.visibility!=='hidden'&&c.display!=='none'&&+c.opacity>.05};
 const bars=[...document.querySelectorAll('body *')].filter(e=>{const c=getComputedStyle(e);if(c.position!=='fixed'||c.display==='none'||c.visibility==='hidden'||+c.opacity<.1)return false;const b=e.getBoundingClientRect();return b.width>=40&&b.height>=30&&b.height<=200&&b.top>innerHeight*.5&&b.top<innerHeight}).map(e=>Object.assign(R(e),{id:e.id||String(e.className).slice(0,24)}));
 const head=Math.max(0,...[...document.querySelectorAll('body *')].filter(e=>{const c=getComputedStyle(e);if(!(c.position==='fixed'||c.position==='sticky'))return false;const b=e.getBoundingClientRect();return b.top<=2&&b.bottom>0&&b.height<=130&&b.width>=innerWidth*.5&&vis(e)}).map(e=>Math.round(e.getBoundingClientRect().bottom)));
 const sec=document.getElementById('nlpjx-map');
 // our controls of the map and the stage resting half under a bar (a control fully under a bar is the page scrolled on: not at rest)
 const half=[]; if(sec) [...sec.querySelectorAll('button, a[href]'), ...document.querySelectorAll('.rbs-label.is-on button, .rbs-label.is-on a[href]')].filter(vis).forEach(e=>{const b=e.getBoundingClientRect();if(b.bottom<0||b.top>innerHeight)return;bars.forEach(r=>{const ox=Math.min(b.right,r.l+r.w)-Math.max(b.left,r.l),oy=Math.min(b.bottom,r.b)-Math.max(b.top,r.t);if(ox>4&&oy>4&&b.top<r.t-4)half.push((e.innerText||e.className||'').trim().slice(0,24).replace(/\s+/g,' ')+'@'+r.id)})});
 const m=window.NLPJX_MAP; let mb=null; try{ if(m) mb=Math.round(((m.getBearing()%360)+360)%360) }catch(_){}
 const cone=document.querySelector('#nlpjx-unimap .nlps-cone');
 return {sy:Math.round(scrollY),vh:innerHeight,head,bars,stage:R(document.querySelector('.nlps-stagebox')),nlps:R(document.getElementById('nlps')),pick:R(document.querySelector('.rbs-label.is-on')),
  map:R(sec),uni:R(document.getElementById('nlpjx-unimap')),view:R(document.getElementById('nlps-view')),prices:R(document.getElementById('nlpg')),mapup:!!document.getElementById('nlps-mapup'),
  h1:R(document.querySelector('h1')),lead:R(document.querySelector('.nl-lead')),cta:R(document.querySelector('nav.nlsh')),
  mapBearing:mb,mapReady:!!m,cone:cone?{on:true,tf:cone.style.transform}:null,half,
  sum:(document.querySelector('.nlps-mapsum-t')||{}).innerText||''}}"""
def ang(a, b):
    if a is None or b is None: return None
    d = abs((a - b) % 360); return min(d, 360 - d)
res = {}
os.makedirs(os.path.join(OUT, tag), exist_ok=True)
jp = os.path.join(OUT, tag, "press.json")
if os.path.exists(jp): res = json.load(open(jp, encoding="utf-8"))
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True, args=["--enable-gpu", "--use-angle=d3d11", "--ignore-gpu-blocklist"])
    for k in only:
        for s in SIZES:
            w, h = map(int, s.split('x')); phone = w < 768
            kw = dict(viewport={"width": w, "height": h}, device_scale_factor=2 if phone else 1)
            if phone: kw.update(is_mobile=True, has_touch=True, user_agent=PHONE_UA)
            ctx = br.new_context(**kw); pg = ctx.new_page(); errs = []; rec = {"size": s, "page": k}
            pg.route("**/*", lambda r: r.abort() if any(x in r.request.url for x in BLOCK) else r.continue_())
            if MOCK: pg.route("**/assets/project-stage/bridge.js*", lambda r: r.fulfill(status=200, content_type="application/javascript", body=open(MOCK, "rb").read()))
            pg.on("pageerror", lambda e: errs.append("pageerror:" + str(e)[:200]))
            pg.on("console", lambda m: errs.append('console:' + m.text[:200]) if m.type == 'error' else None)
            pg.add_init_script(INIT)
            shot = lambda n: pg.screenshot(path=os.path.join(OUT, tag, "%s-%s-%s.png" % (k, s, n)))
            pg.goto(PAGES[k], wait_until="load", timeout=120000); pg.wait_for_timeout(3500)
            rec["rest"] = pg.evaluate(GEO)
            # the stage under the header, as a visitor scrolls to it; wait for the 3D
            pg.evaluate("()=>{const e=document.getElementById('nlps');window.scrollTo(0,e.getBoundingClientRect().top+scrollY-80)}"); pg.wait_for_timeout(9000)
            shot("1-stage")
            box = pg.evaluate("(()=>{const b=document.getElementById('nlps-stage').getBoundingClientRect();return [b.left,b.top,b.width,b.height]})()")
            x, y = box[0] + box[2] * 0.5, box[1] + box[3] * 0.42
            (pg.touchscreen.tap(x, y) if phone else pg.mouse.click(x, y)); pg.wait_for_timeout(2500)
            ev = pg.evaluate("window.__ev.map(e=>[e[0],e[1]&&e[1].floor,e[1]&&e[1].bearing,e[1]&&e[1].unit])")
            rec["tap"] = "real" if ev else "api"
            if not ev:
                pg.evaluate("window.__nlpsStage && window.__nlpsStage.selectFloor(20)"); pg.wait_for_timeout(2500)
                ev = pg.evaluate("window.__ev.map(e=>[e[0],e[1]&&e[1].floor,e[1]&&e[1].bearing,e[1]&&e[1].unit])")
            rec["events1"] = ev
            fac = [e for e in ev if e[0] == 'nl:facing']
            b1 = fac[-1][2] if fac else None; rec["b1"] = b1
            shot("2-tap")
            rec["after_tap"] = pg.evaluate(GEO)
            # "הנוף והמפה" from the floor card (phones: five presses, each from the stage)
            lands = []
            for i in range(REP if phone else 1):
                if i:
                    pg.evaluate("()=>{const e=document.getElementById('nlps');window.scrollTo({top:e.getBoundingClientRect().top+scrollY-80,behavior:'instant'})}"); pg.wait_for_timeout(1200)
                nud = pg.evaluate("(()=>{const b=[...document.querySelectorAll('button,a')].find(x=>x.innerText.trim()==='לא עכשיו'&&x.getBoundingClientRect().height>0);if(b){b.click();return true}return false})()")
                if nud: pg.wait_for_timeout(800)
                bt = pg.query_selector(".rbs-label.is-on .rbs-act[data-act='view']") or pg.query_selector(".rbs-act[data-act='view']")
                if not bt: lands.append({"err": "no view button"}); break
                bb = bt.bounding_box()
                if bb and (bb['y'] < 0 or bb['y'] + bb['height'] > h): bt.scroll_into_view_if_needed(); pg.wait_for_timeout(500); bb = bt.bounding_box()
                (pg.touchscreen.tap(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2) if phone else pg.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2))
                pg.wait_for_timeout(3500)
                g = pg.evaluate(GEO); lands.append(dict({k2: g[k2] for k2 in ("sy", "head", "uni", "map", "half", "bars")}, nudge=nud))
                shot("3-viewmap" if i == 0 else "3-viewmap-press%d" % (i + 1))
            rec["lands"] = lands
            # the map starts when the visitor stops on it (a real wheel / swipe, then stillness); then the beam turns
            if phone:
                pg.touchscreen.tap(w * 0.1, h * 0.5) if False else None
            pg.mouse.move(w / 2, h / 2); pg.mouse.wheel(0, 40); pg.wait_for_timeout(300); pg.mouse.wheel(0, -40)
            for _ in range(24):
                if pg.evaluate("!!window.NLPJX_MAP"): break
                pg.wait_for_timeout(500)
            pg.wait_for_timeout(2500)
            g = pg.evaluate(GEO); rec["beam1"] = {"mapBearing": g["mapBearing"], "cone": g["cone"], "ready": g["mapReady"], "off": ang(g["mapBearing"], b1), "sum": g["sum"]}
            pg.evaluate("()=>{const u=document.getElementById('nlpjx-unimap');if(u){const b=u.getBoundingClientRect();if(b.top<0||b.bottom>innerHeight)u.scrollIntoView({block:'center'})}}"); pg.wait_for_timeout(1500)
            shot("4-beam1")
            # a second side of the same floor, the events a tap on the ring sends
            sides = pg.evaluate("(()=>{try{return JSON.parse(document.getElementById('nlps').dataset.cfg).units}catch(e){return []}})()")
            fl = fac[-1][1] if fac else 20; u1 = (fac[-1][3] or '') if fac else ''
            other = [sd for sd in sides if not u1.endswith('-' + sd[0])]
            if other:
                sd = sorted(other, key=lambda z: -(ang(z[1], b1) or 0))[0]
                pg.evaluate("u=>window.__nlpsStage.selectUnit(u,'user')", "%s-%s" % (fl, sd[0])); pg.wait_for_timeout(3500)
                ev2 = pg.evaluate("window.__ev.filter(e=>e[0]==='nl:facing').map(e=>[e[1].floor,e[1].bearing,e[1].unit])")
                b2 = ev2[-1][1] if ev2 else None
                g = pg.evaluate(GEO); rec["beam2"] = {"unit": "%s-%s" % (fl, sd[0]), "b2": b2, "mapBearing": g["mapBearing"], "off": ang(g["mapBearing"], b2), "sum": g["sum"]}
                shot("5-beam2")
            rec["errors"] = errs[:12]
            res[k + "-" + s] = rec
            json.dump(res, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            st = rec["rest"]["stage"]; mp = rec["rest"]["map"]
            print(k, s, "tap", rec["tap"], "b1", b1, "| stage end", st and st["y"] + st["h"], "map top", mp and mp["y"], "gap", st and mp and mp["y"] - st["y"] - st["h"],
                  "| beam1", rec["beam1"], "| beam2", rec.get("beam2"), "| half", [l.get("half") for l in lands], "| errs", len(errs), flush=True)
            ctx.close(); time.sleep(4)
    br.close()
