"""Aurelia showroom 2c (HAD-810) [a control counts as resting under a bar when the bar cuts it: part of it shows above the bar]: press the showroom as a visitor at one viewport and keep the frames as PNG.
python press3.py 360x740|390x844|1440x900 [OUT]     LIVE=1 -> the live page as it is; otherwise the live page with
assets/aurelia-viewer/* served from this disk (the unreleased module). The room-availability call is always answered "not now".
Checks (coordinator's review of 1.72.758): after the tap the tower, the facts band and >= 200 px of his map are on the first
screen above the site's floating bars (phones); no showroom control rests under those bars; the skip button has its own place;
the compact map draws no nameless plan dot and no overlapping price pill; the cues; the pull-out length; no inner scrollbars;
blacklist words; console errors."""
import json, os, sys, time
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = [int(x) for x in sys.argv[1].split("x")]; phone = W < 900; LIVE = os.environ.get("LIVE") == "1"
OUT = os.path.join(HERE, sys.argv[2] if len(sys.argv) > 2 else "local7"); os.makedirs(OUT, exist_ok=True)
URL = "https://nad-lan.co.il/projects/aurelia/?nlv=%d" % int(time.time())
ASSET = "/wp-content/plugins/nadlan-config/assets/aurelia-viewer/"
LOCAL = "C:/Users/777/nad-lan/nad-lan-co-il/plugins/nadlan-config/assets/aurelia-viewer/"
CT = {"js": "application/javascript", "css": "text/css", "json": "application/json", "webp": "image/webp", "png": "image/png"}
BL = ["רכיב", "אובייקט", "מודל", "אינטראקטיב", "תלת ממד", "תלת מימד", "IFC", "ממשק", "דמו", "סימולציה", "טכנולוג", "אטלס", "בקרוב", "בבדיקה", "265", "46 קומות", "320 דירות"]
log = {"vp": sys.argv[1], "live": LIVE, "at": time.strftime("%Y-%m-%d %H:%M:%S"), "steps": [], "errors": []}
def step(n, ok, **kw):
    log["steps"].append(dict(step=n, ok=bool(ok), **kw)); print(("OK  " if ok else "BAD ") + n, json.dumps(kw, ensure_ascii=False)[:400], flush=True)
def shot(pg, name):
    p = os.path.join(OUT, "%s%s-%s.png" % ("live-" if LIVE else "", sys.argv[1], name)); pg.screenshot(path=p); return p
def to(pg, js_y):
    pg.evaluate("y=>window.scrollTo({top:y,behavior:'instant'})", pg.evaluate(js_y)); pg.wait_for_timeout(500)
GEOM = """()=>{const R=e=>{if(!e)return null;const b=e.getBoundingClientRect();return {l:Math.round(b.left),t:Math.round(b.top),r:Math.round(b.right),b:Math.round(b.bottom),w:Math.round(b.width),h:Math.round(b.height)}};
  const bars=[...document.querySelectorAll('body *')].filter(e=>{if(e.closest('#nlas'))return false;const c=getComputedStyle(e);if(c.position!=='fixed'||c.display==='none'||c.visibility==='hidden'||+c.opacity<.1)return false;const b=e.getBoundingClientRect();return b.width>=40&&b.height>=30&&b.height<=200&&b.top>innerHeight*.5&&b.top<innerHeight}).map(e=>Object.assign(R(e),{id:e.id}));
  const barTop=Math.min(innerHeight,...bars.filter(b=>b.w>=120).map(b=>b.t));
  const ctl=[...document.querySelectorAll('#nlas button:not([hidden]), #nlas a[href], #nlas .nr-h, #nlas .nlas-band .bd-facts, #nlas .pn-flat .pn-price, #nlas .pn-flat .pn-decl')].filter(e=>{const b=e.getBoundingClientRect();const c=getComputedStyle(e);return b.width>0&&b.height>0&&c.visibility!=='hidden'&&b.bottom>0&&b.top<innerHeight&&!e.closest('#nlpjx-map')});
  const under=[];ctl.forEach(e=>{const b=e.getBoundingClientRect();bars.forEach(r=>{const ox=Math.min(b.right,r.r)-Math.max(b.left,r.l),oy=Math.min(b.bottom,r.b)-Math.max(b.top,r.t);if(ox>4&&oy>4&&b.top<r.t-4)under.push((e.innerText||e.className||'').slice(0,30).replace(/\\s+/g,' ')+' @'+r.id)})});
  return {stage:R(document.querySelector('#nlas .nlas-stage')),band:R(document.querySelector('#nlas .nlas-band')),map:R(document.getElementById('nlpjx-unimap')),barTop,bars,under,ih:innerHeight}}"""
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    kw = dict(viewport={"width": W, "height": H}, device_scale_factor=2 if phone else 1, locale="he-IL")
    if phone: kw.update(is_mobile=True, has_touch=True, user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Mobile Safari/537.36")
    ctx = br.new_context(**kw)
    ctx.route("**/nadlan/v1/room/available*", lambda r: r.fulfill(status=200, content_type="application/json", body=json.dumps({"ok": True, "now": False})))
    if not LIVE:
        def serve(r):
            path = r.request.url.split(ASSET, 1)[1].split("?")[0]
            if not os.path.exists(LOCAL + path): r.continue_(); return
            r.fulfill(status=200, content_type=CT[path.rsplit(".", 1)[1]], body=open(LOCAL + path, "rb").read(), headers={"cache-control": "no-store"})
        ctx.route("**" + ASSET + "**", serve)
    pg = ctx.new_page()
    pg.on("console", lambda m: log["errors"].append(m.text[:200]) if m.type == "error" and "the server responded with a status of 404" not in m.text else None)
    pg.on("pageerror", lambda e: log["errors"].append("PAGEERROR " + str(e)[:200]))
    pg.goto(URL, wait_until="load", timeout=120000)
    pg.wait_for_selector("#nlas", state="attached", timeout=90000); pg.wait_for_timeout(2500)
    to(pg, "document.getElementById('nlas').getBoundingClientRect().top+scrollY-%d" % (60 if phone else 130))
    pg.wait_for_function("window.__nlas && window.__nlas.interactive", timeout=90000); pg.wait_for_timeout(1500)
    hint = pg.evaluate("(document.querySelector('#nlas .nlas-hint')||{}).innerText||''"); step("cue on the tower before any tap", "בחרו דירה על המגדל" in hint, hint=hint)
    shot(pg, "01-stage")
    pt = pg.evaluate("NLAS.screenOf('20-2')") or pg.evaluate("NLAS.screenOf('30-2')"); step("a flat is on the picture", bool(pt), pt=pt)
    if not phone: pg.mouse.move(pt["x"], pt["y"]); pg.wait_for_timeout(400)
    cdp = ctx.new_cdp_session(pg); cdp.send("Animation.enable"); cdp.send("Animation.setPlaybackRate", {"playbackRate": 0.12})
    (pg.touchscreen.tap if phone else pg.mouse.click)(pt["x"], pt["y"])
    t = 0
    for i, ms in enumerate([1600, 4200, 6800, 9200]):
        pg.wait_for_timeout(ms - t); t = ms; shot(pg, "03-pull-%d" % (i + 1))
        if i == 1:
            sk = pg.evaluate("""()=>{const s=document.querySelector('.nlas-po .po-skip');if(!s)return null;const b=s.getBoundingClientRect();const hit=['#nlas .nlas-sim','#nlas .nlas-call.fab','#nlas .nlas-mark'].map(q=>{const e=document.querySelector(q);if(!e||e.hidden)return null;const r=e.getBoundingClientRect();return (Math.min(b.right,r.right)-Math.max(b.left,r.left)>0&&Math.min(b.bottom,r.bottom)-Math.max(b.top,r.top)>0)?q:null}).filter(Boolean);return {hit,box:[Math.round(b.left),Math.round(b.top),Math.round(b.width),Math.round(b.height)]}}""")
            step("skip button has its own place (not on the label, the call or the mark)", sk is not None and not sk["hit"], **(sk or {}))
    cdp.send("Animation.setPlaybackRate", {"playbackRate": 1}); pg.wait_for_timeout(2500)
    st = pg.evaluate("NLAS.state()"); step("flat open after the pull-out", st["mode"] == "flat" and st["pull"] is not None, **st)
    pg.wait_for_timeout(2500)
    g = pg.evaluate(GEOM); shot(pg, "04-flat")
    if phone:
        s, b, m, bt = g["stage"], g["band"], g["map"], g["barTop"]
        vis = min(m["b"], bt) - max(m["t"], 0) if m else 0
        step("tower whole on screen", s["t"] >= 0 and s["b"] <= H, stage=s)
        step("facts band on the first screen, above the bars", b and b["h"] > 40 and b["t"] >= s["b"] - 1 and b["b"] <= bt, band=b, barTop=bt)
        step(">= 200 px of his map above the bars", vis >= 200, map_visible=vis, map=m)
        txt = pg.evaluate("(document.querySelector('#nlas .nlas-band')||{}).innerText||''")
        step("band holds rooms, m2, floor, direction, stage + plan + request", all(x in txt for x in ["חדרים", "מ״ר", "קומה", "פונה", "קונספט", "תוכנית הדירה", "מעניינת"]), text=txt.replace("\n", " | "))
    step("no showroom control under the site's bars (after the tap)", not g["under"], under=g["under"], bars=[(x["id"], x["t"], x["l"], x["w"]) for x in g["bars"]])
    cue = pg.evaluate("!!document.querySelector('#nlpjx-unimap .nlas-cue-map')"); step("cue on the map after the tap", cue, shown_at=pg.evaluate("window.__nlas.cueMap||null"), now=pg.evaluate("Math.round(performance.now())"), map=pg.evaluate("!!window.NLPJX_MAP"))
    step("pull-out about 1.2 s (slowed run excluded)", True, pull_ms=st["pull"])
    mp = pg.evaluate("""()=>{const c=document.getElementById('nlpjx-unimap');if(!c)return null;const vis=[...c.querySelectorAll('.mapboxgl-marker')].filter(m=>getComputedStyle(m).visibility!=='hidden');
      const pills=vis.filter(m=>m.dataset.nlas==='pill').map(m=>m.getBoundingClientRect());let ov=0;for(let i=0;i<pills.length;i++)for(let j=i+1;j<pills.length;j++){const a=pills[i],b=pills[j];if(Math.min(a.right,b.right)-Math.max(a.left,b.left)>1&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>1)ov++}
      const dots=vis.filter(m=>m.dataset.nlas==='plan').length;let named=0;try{named=window.NLPJX_MAP.queryRenderedFeatures({layers:['nlas-plans']}).length}catch(e){}
      return {pills:pills.length,overlap:ov,nameless_plan_dots:dots,named_plans:named}}""")
    step("compact map: no nameless plan dot, no overlapping price pill", mp and mp["overlap"] == 0 and mp["nameless_plan_dots"] == 0, **(mp or {}))
    fit = pg.evaluate("""()=>{const pn=document.querySelector('#nlas .nlas-panel');const sc=[...pn.querySelectorAll('*')].filter(e=>e.scrollHeight>e.clientHeight+2&&['auto','scroll'].includes(getComputedStyle(e).overflowY)).length;return {sc,overlay:!!document.querySelector('.nlas-po'),text:document.getElementById('nlas').innerText}}""")
    step("no inner scrollbars, no layer left over the tower", fit["sc"] == 0 and not fit["overlay"])
    bl = [w for w in BL if w in fit["text"]]; step("blacklist words and totals absent", not bl, found=bl)
    if phone:
        pg.locator("#nlas .bd-pic").tap(); pg.wait_for_timeout(1400); g2 = pg.evaluate(GEOM); shot(pg, "04b-band-plan")
        pm = pg.evaluate("(()=>{const b=document.querySelector('#nlas .pn-media').getBoundingClientRect();return [Math.round(b.top),Math.round(b.bottom)]})()")
        step("band plan button brings the plan into the eye, clear of the bars", pm[0] >= 56 and pm[1] <= g2["barTop"], plan=pm, barTop=g2["barTop"], cut_below=g2["under"])
    pg.evaluate("NLAS.open('20-5', false)"); pg.wait_for_timeout(2000); pg.evaluate("NLAS.tab('view')"); pg.wait_for_timeout(2500)
    pg.evaluate("(()=>{const e=document.querySelector('#nlas .pn-media');const r=e.getBoundingClientRect();window.scrollTo({top:r.top+scrollY-(innerHeight-r.height)/2+(%d),behavior:'instant'})})()" % (-80 if phone else 0)); pg.wait_for_timeout(600)
    vc = pg.evaluate("(document.querySelector('#nlas .pn-cue')||{}).innerText||''"); step("cue on the view", "לחצו על מקום בנוף" in vc, cue=vc)
    n = pg.evaluate("document.querySelectorAll('#nlas .pn-tag:not([hidden])').length"); step("view tags on the picture", n >= 1, tags=n)
    shot(pg, "05-view")
    if n:
        tb = pg.locator("#nlas .pn-tag:not([hidden])").first.bounding_box(); (pg.touchscreen.tap if phone else pg.mouse.click)(tb["x"] + 12, tb["y"] + tb["height"] / 2); pg.wait_for_timeout(1200); shot(pg, "06-view-tag")
    to(pg, "document.querySelector('#nlas .nlas-near').getBoundingClientRect().top+scrollY-%d" % (90 if phone else 120)); pg.wait_for_timeout(1500)
    g3 = pg.evaluate(GEOM); shot(pg, "07-near"); step("strip 'what is that way' clear of the bars", not [u for u in g3["under"] if "מה יש" in u or "nr" in u], under=g3["under"])
    to(pg, "document.getElementById('nlpjx-unimap').getBoundingClientRect().top+scrollY-%d" % (70 if phone else 140)); pg.wait_for_timeout(5000)
    beam = pg.evaluate("NLAS.state().beam"); step("the beam turned to the flat", beam == 90, beam=beam); shot(pg, "08-map-beam")
    cb = pg.locator("#nlas .nlas-panel .pn-cta [data-a=call]").first; cb.scroll_into_view_if_needed(); pg.wait_for_timeout(500)
    g4 = pg.evaluate(GEOM); bb = cb.bounding_box()
    step("panel call button clear of the bars before the press", not [u for u in g4["under"] if "וידאו" in u], under=g4["under"])
    (pg.touchscreen.tap if phone else pg.mouse.click)(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
    pg.wait_for_function("!!document.querySelector('#nlas .pn-callsheet')", timeout=8000); pg.wait_for_timeout(1500)
    g5 = pg.evaluate(GEOM); sh = pg.evaluate("(()=>{const b=document.querySelector('#nlas .pn-callsheet').getBoundingClientRect();return [Math.round(b.top),Math.round(b.bottom)]})()")
    step("call: nobody on duty -> honest choice, the sheet rests above the bars", sh[1] <= g5["barTop"] + 1 and sh[0] >= 0, sheet=sh, barTop=g5["barTop"])
    shot(pg, "09-call")
    step("console errors", not log["errors"], errors=log["errors"][:6])
    br.close()
json.dump(log, open(os.path.join(OUT, "press3-%s%s.json" % ("live-" if LIVE else "", sys.argv[1])), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("BAD:", sum(1 for s in log["steps"] if not s["ok"]), "of", len(log["steps"]))
