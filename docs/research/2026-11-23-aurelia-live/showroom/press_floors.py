"""HAD-810 1.72.762: every residential floor can be chosen. python press_floors.py WxH [OUT]  (LIVE=1 = live page)
(1) on the tower picture: for each floor 6..47, find a balcony of that floor on the picture (NLAS.screenOf) and tap it as a visitor;
    the flat that opens must be on that floor. A floor with no balcony on the picture is reported (not a failure by itself).
(2) the floor stepper: from floor 6 the arrow up is pressed once per floor up to 47; every floor 6..47 must open; the arrow up is
    off on 47 and the arrow down on 6."""
import json, os, sys, time
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = [int(x) for x in sys.argv[1].split("x")]; phone = W < 900; LIVE = os.environ.get("LIVE") == "1"
OUT = os.path.join(HERE, sys.argv[2] if len(sys.argv) > 2 else "local11"); os.makedirs(OUT, exist_ok=True)
ASSET = "/wp-content/plugins/nadlan-config/assets/aurelia-viewer/"
LOCAL = "C:/Users/777/nad-lan/nad-lan-co-il/plugins/nadlan-config/assets/aurelia-viewer/"
CT = {"js": "application/javascript", "css": "text/css", "json": "application/json", "webp": "image/webp", "png": "image/png"}
res = {"vp": sys.argv[1], "live": LIVE, "at": time.strftime("%Y-%m-%d %H:%M:%S"), "steps": [], "errors": []}
def step(n, ok, **kw):
    res["steps"].append(dict(step=n, ok=bool(ok), **kw)); print(("OK  " if ok else "BAD ") + n, json.dumps(kw, ensure_ascii=False)[:400], flush=True)
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
    top = "window.scrollTo({top:document.getElementById('nlas').getBoundingClientRect().top+scrollY-%d,behavior:'instant'})" % (60 if phone else 130)
    pg.evaluate(top); pg.wait_for_timeout(500)
    pg.wait_for_function("window.NLAS && window.__nlas && window.__nlas.interactive", timeout=90000); pg.wait_for_timeout(1500)
    FL = pg.evaluate("fetch('%sflats.json?x='+Date.now()).then(r=>r.json()).then(j=>({b:j.building||null,fl:[...new Set(j.flats.map(f=>f.f))].sort((a,b)=>a-b),ids:j.flats.map(f=>f.id)}))" % ASSET)
    step("data: the building is 47 floors / 320 flats, residential floors 6..47 each with a sample flat", FL["b"] and FL["b"]["floors"] == 47 and FL["b"]["flats"] == 320 and FL["fl"] == list(range(6, 48)), building=FL["b"], floors=[FL["fl"][0], FL["fl"][-1], len(FL["fl"])])
    # (1) the tower picture
    tapped, notpic, wrong = [], [], []
    for fl in range(6, 48):
        pg.evaluate(top); pg.wait_for_timeout(250)
        ids = [i for i in FL["ids"] if i.startswith("%d-" % fl)]
        pt = None
        for i in ids:
            pt = pg.evaluate("NLAS.screenOf('%s')" % i)
            if pt and 0 < pt["y"] < H - 80 and 0 < pt["x"] < W: break
            pt = None
        if not pt: notpic.append(fl); continue
        (pg.touchscreen.tap if phone else pg.mouse.click)(pt["x"], pt["y"]); pg.wait_for_timeout(1600 if not tapped else 700)
        st = pg.evaluate("NLAS.state()")
        sel = st["sel"] or ""
        if sel.split("-")[0] == str(fl): tapped.append(fl)
        else: wrong.append([fl, sel])
    step("tower picture: every floor with a balcony on the picture opens its own floor", not wrong, chosen=len(tapped), wrong=wrong, not_on_picture=notpic)
    # (2) the stepper from 6 to 47
    pg.evaluate("NLAS.open('6-1', false)"); pg.wait_for_timeout(1500)
    pg.evaluate(top); pg.wait_for_timeout(300)
    down6 = pg.evaluate("(document.querySelector('#nlas .pn-fl [data-fl=\"-1\"]')||{}).disabled")
    seen, stuck = [6], None
    for k in range(41):
        b = pg.locator('#nlas .pn-fl [data-fl="1"]')
        if b.is_disabled(): stuck = seen[-1]; break
        b.scroll_into_view_if_needed(); (b.tap if phone else b.click)(); pg.wait_for_timeout(350)
        f = int((pg.evaluate("NLAS.state().sel") or "0-0").split("-")[0]); seen.append(f)
    up47 = pg.evaluate("(document.querySelector('#nlas .pn-fl [data-fl=\"1\"]')||{}).disabled")
    rng = pg.evaluate("(document.querySelector('#nlas .pn-fl')||{}).getAttribute && document.querySelector('#nlas .pn-fl').getAttribute('aria-label')")
    pg.screenshot(path=os.path.join(OUT, "%s%s-floor47.png" % ("live-" if LIVE else "", sys.argv[1])))
    missing = [x for x in range(6, 48) if x not in seen]
    step("stepper: every floor 6..47 opens, one press each", not missing and seen == list(range(6, 48)), missing=missing, last=seen[-1], stuck=stuck)
    step("stepper: up is off on 47, down is off on 6, the range is 6..47", up47 is True and down6 is True and rng == "קומות 6 עד 47", up47=up47, down6=down6, range=rng)
    txt = pg.evaluate("document.getElementById('nlas').innerText")
    step("47th floor flat: a sample flat, 6 rooms, the deals line groups 5 rooms and up", "דירה לדוגמה" in txt and "קומה 47" in txt and "5 חדרים ומעלה" in txt, has=[w for w in ["דירה לדוגמה", "קומה 47", "5 חדרים ומעלה"] if w in txt])
    bad = [w for w in ["265", "46 קומות", "47 קומות ו-265"] if w in txt]
    step("no visible 265 / 46 floors as the building's size", not bad, found=bad)
    step("console errors", not res["errors"], errors=res["errors"][:5])
    br.close()
json.dump(res, open(os.path.join(OUT, "press-floors-%s%s.json" % ("live-" if LIVE else "", sys.argv[1])), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("BAD:", sum(1 for s in res["steps"] if not s["ok"]), "of", len(res["steps"]))
