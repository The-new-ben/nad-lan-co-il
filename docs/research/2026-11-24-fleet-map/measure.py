"""HAD-823 fleet map: where the stage ends, where the map starts, what is between, per page and size (read-only, a visitor's load).
python measure.py <tag> [rainbow ashira duo] [--sizes 360x740,...]  -> <tag>/<page>-<size>.png + <tag>/measure.json"""
import json, os, sys, time
from playwright.sync_api import sync_playwright
OUT = os.path.dirname(os.path.abspath(__file__))
PAGES = {"rainbow": "https://nad-lan.co.il/projects/rainbow-tel-aviv/", "ashira": "https://nad-lan.co.il/projects/ashira-sde-dov/", "duo": "https://nad-lan.co.il/projects/duo-tel-aviv/"}
args = [a for a in sys.argv[1:] if not a.startswith('--')]
tag = args[0] if args else 'before'
only = args[1:] or list(PAGES)
SIZES = ["360x740", "390x844", "1280x720", "1440x900"]
MOCK = None
for a in sys.argv[1:]:
    if a.startswith('--sizes='): SIZES = a.split('=', 1)[1].split(',')
    if a.startswith('--mock='): MOCK = a.split('=', 1)[1]
PHONE_UA = "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Mobile Safari/537.36"
LAY = r"""()=>{
 const R=e=>{if(!e)return null;const b=e.getBoundingClientRect();return {y:Math.round(b.top+scrollY),b:Math.round(b.bottom+scrollY),h:Math.round(b.height),l:Math.round(b.left),w:Math.round(b.width)}};
 const stage=document.querySelector('.nlps-stagebox')||document.getElementById('nlps'), map=document.getElementById('nlpjx-map'), uni=document.getElementById('nlpjx-unimap');
 const sb=stage?stage.getBoundingClientRect().bottom+scrollY:0, mt=map?map.getBoundingClientRect().top+scrollY:0;
 // what lies between: visible blocks whose box is between the stage's bottom and the map's top (outermost only)
 const between=[]; const seen=new Set();
 document.querySelectorAll('body *').forEach(e=>{const b=e.getBoundingClientRect(); if(b.height<20||b.width<100)return; const y=b.top+scrollY; if(y<sb-2||y+b.height>mt+2)return; if(e.closest('#nlpjx-map'))return; let p=e.parentElement; while(p){ if(seen.has(p))return; p=p.parentElement;} seen.add(e); between.push({tag:e.tagName.toLowerCase(),id:e.id,cls:String(e.className).slice(0,50),y:Math.round(y),h:Math.round(b.height),t:(e.querySelector('h2,h3')||{}).innerText||''});});
 const bars=[...document.querySelectorAll('body *')].filter(e=>{const c=getComputedStyle(e);if(c.position!=='fixed'||c.display==='none'||c.visibility==='hidden'||+c.opacity<.1)return false;const b=e.getBoundingClientRect();return b.width>=40&&b.height>=30&&b.height<=200&&b.top>innerHeight*.5&&b.top<innerHeight}).map(e=>({id:e.id||String(e.className).slice(0,24),t:Math.round(e.getBoundingClientRect().top),h:Math.round(e.getBoundingClientRect().height)}));
 return {h1:R(document.querySelector('h1')),lead:R(document.querySelector('.nl-lead')),nlsh:R(document.querySelector('nav.nlsh')),stagebox:R(stage),nlps:R(document.getElementById('nlps')),below:R(document.querySelector('.nlps-below')),view:R(document.getElementById('nlps-view')),map:R(map),unimap:R(uni),gap:Math.round(mt-sb),between:between.slice(0,30),bars,docH:document.documentElement.scrollHeight,
  order:[...document.querySelectorAll('h1, .nl-lead, nav.nlsh, .nlps-stagebox, #nlps-view, #nlpjx-map, #nlps-tour, #nlps-deals, #nlpjx-price, #nlpg')].map(e=>(e.id||e.tagName+'.'+String(e.className).split(' ')[0])+'@'+Math.round(e.getBoundingClientRect().top+scrollY))}}"""
os.makedirs(os.path.join(OUT, tag), exist_ok=True)
_jp = os.path.join(OUT, tag, "measure.json")
res = json.load(open(_jp, encoding="utf-8")) if os.path.exists(_jp) else {}
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True, args=["--enable-gpu", "--use-angle=d3d11", "--ignore-gpu-blocklist"])
    for k in only:
        for s in SIZES:
            w, h = map(int, s.split('x')); phone = w < 768
            kw = dict(viewport={"width": w, "height": h}, device_scale_factor=2 if phone else 1)
            if phone: kw.update(is_mobile=True, has_touch=True, user_agent=PHONE_UA)
            ctx = br.new_context(**kw); pg = ctx.new_page(); errs = []
            pg.route("**/*", lambda r: r.abort() if any(x in r.request.url for x in ("google-analytics", "googletagmanager", "hotjar", "clarity.ms", "facebook")) else r.continue_())
            if MOCK: pg.route("**/assets/project-stage/bridge.js*", lambda r: r.fulfill(status=200, content_type="application/javascript", body=open(MOCK, "rb").read()))
            pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
            pg.on("console", lambda m: errs.append('console:' + m.text[:200]) if m.type == 'error' else None)
            pg.goto(PAGES[k] + ("?nlps3d" if len(sys.argv) > 99 else ""), wait_until="load", timeout=120000); pg.wait_for_timeout(4000)
            pg.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)"); pg.wait_for_timeout(1500)
            pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(1200)
            lay = pg.evaluate(LAY)
            sb = lay['stagebox']
            if sb:
                pg.evaluate("y=>window.scrollTo(0,y)", max(0, sb['b'] - h // 2)); pg.wait_for_timeout(2500)
                pg.screenshot(path=os.path.join(OUT, tag, "%s-%s-stage-end.png" % (k, s)))
            lay['errors'] = errs[:10]
            res[k + "-" + s] = lay
            print(k, s, 'stage end', sb and sb['b'], 'map top', lay['map'] and lay['map']['y'], 'gap', lay['gap'], 'between', [(b['id'] or b['cls'][:20], b['h']) for b in lay['between']][:8], 'errs', len(errs), flush=True)
            ctx.close(); time.sleep(4)
    br.close()
json.dump(res, open(os.path.join(OUT, tag, "measure.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
