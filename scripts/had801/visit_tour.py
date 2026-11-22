# -*- coding: utf-8 -*-
"""HAD-801: walk the Sde Dov 2036 tour as a visitor in the owner's installed Chrome (headless, GPU), desktop 1440 and phone 390.
  python visit_tour.py <tour url> <out dir> [--pages]   (--pages: also /sde-dov/ entry press and the home card)"""
import json, os, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
URL, OUT = sys.argv[1].rstrip("/") + "/", Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
PAGES = "--pages" in sys.argv
CHROME = Path(os.environ.get("PROGRAMFILES", "C:/Program Files")) / "Google/Chrome/Application/chrome.exe"
rep = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=str(CHROME), headless=True, args=["--enable-gpu", "--no-first-run", "--disable-renderer-backgrounding"])
    for name, ctx_args in (("desktop", dict(viewport={"width": 1440, "height": 900})),
                           ("phone", dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True,
                                          user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Mobile Safari/537.36"))):
        ctx = br.new_context(**ctx_args); pg = ctx.new_page(); errs, bad = [], []
        pg.on("console", lambda m: errs.append(m.text[:200]) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append("pageerror " + str(e)[:200]))
        pg.on("response", lambda r: bad.append("%d %s" % (r.status, r.url[-90:])) if r.status >= 400 else None)
        r = {}; t0 = time.time()
        resp = pg.goto(URL, wait_until="domcontentloaded", timeout=120000)
        r["status"] = resp.status; r["robots"] = pg.evaluate("(document.querySelector('meta[name=robots]')||{}).content||null")
        r["title"] = pg.title()
        try:
            pg.wait_for_function("window.tourReady || (window.round2StreetCell && window.round2StreetCell.live)", timeout=150000)
            r["ready_s"] = round(time.time() - t0, 1)
        except Exception as e:
            r["ready_s"] = None; r["ready_err"] = str(e)[:120]
        try:
            pg.wait_for_function("!window.tour || !window.tour.world || (window.tour.world.artReady && window.tour.world.pendingTiles===0)", timeout=60000)
        except Exception:
            r["art_pending"] = True
        pg.wait_for_timeout(2500)
        r["disclaimer"] = pg.evaluate("document.body.innerText.includes('הדמיה להמחשה, על פי התכנית')")
        r["soil"] = pg.evaluate("/זיהום|מזוהמ|קרקע מזוה/.test(document.body.innerText)")
        pg.screenshot(path=str(OUT / ("tour-%s.png" % name)))
        # walk a few steps forward (keyboard on desktop, the on-screen control on phone is the tour's own)
        try:
            pg.mouse.click(ctx_args["viewport"]["width"] // 2, ctx_args["viewport"]["height"] // 2)
            pg.keyboard.down("KeyW"); pg.wait_for_timeout(2500); pg.keyboard.up("KeyW"); pg.wait_for_timeout(1500)
            r["hash_after_walk"] = pg.evaluate("location.hash")
            pg.screenshot(path=str(OUT / ("tour-%s-walk.png" % name)))
        except Exception as e:
            r["walk_err"] = str(e)[:120]
        r["errors"] = errs[:8]; r["http_4xx_5xx"] = bad[:8]
        # the places list
        pg2 = ctx.new_page(); resp = pg2.goto(URL + "places/", wait_until="domcontentloaded", timeout=120000)
        r["places_status"] = resp.status; r["places_articles"] = pg2.evaluate("document.querySelectorAll('article').length")
        r["places_robots"] = pg2.evaluate("(document.querySelector('meta[name=robots]')||{}).content||null")
        r["places_h1"] = pg2.evaluate("(document.querySelector('h1')||{}).innerText")
        r["named_2208"] = pg2.evaluate("(document.getElementById('p=lot-merkaz-2208')||{}).innerText||''")[:160]
        pg2.screenshot(path=str(OUT / ("places-%s.png" % name)))
        if PAGES:
            pg3 = ctx.new_page(); t1 = time.time(); pg3.goto("https://nad-lan.co.il/sde-dov/?v=" + str(int(t1)), wait_until="load", timeout=120000)
            r["sdedov_load_s"] = round(time.time() - t1, 2)
            r["entry"] = pg3.evaluate("""(()=>{const s=document.querySelector('[data-nlq]');if(!s)return null;const b=s.getBoundingClientRect();
              const h1=document.querySelector('h1').getBoundingClientRect(), lead=document.querySelector('.nls1-lead').getBoundingClientRect();
              const map=document.querySelector('.nlam');const img=s.querySelector('.nlq-cover img');
              return {top:Math.round(b.top+scrollY),h:Math.round(b.height),h1:Math.round(h1.top+scrollY),lead:Math.round(lead.top+scrollY),
                map:map?Math.round(map.getBoundingClientRect().top+scrollY):null, anim:img?getComputedStyle(img).animationName:null,
                h2color:getComputedStyle(s.querySelector('h2')).color, wa:!!document.querySelector('a[href*=\"wa.me\"]'),
                engine:performance.getEntriesByType('resource').filter(e=>/tour\\/sde-dov\\/(entry-|packed|data)/.test(e.name)).length}})()""")
            pg3.evaluate("document.querySelector('[data-nlq]').scrollIntoView({block:'start'})"); pg3.wait_for_timeout(1200)
            pg3.screenshot(path=str(OUT / ("sdedov-entry-%s.png" % name)))
            pg3.click("[data-nlq] .nlq-enter"); pg3.wait_for_timeout(1500)
            try:
                pg3.wait_for_function("(()=>{const f=document.querySelector('dialog.nlq-dialog iframe');try{const w=f.contentWindow;return w.tourReady||(w.round2StreetCell&&w.round2StreetCell.live)}catch(e){return false}})()", timeout=150000)
                r["dialog_ready"] = True
            except Exception as e:
                r["dialog_ready"] = str(e)[:100]
            pg3.wait_for_timeout(4000)
            pg3.screenshot(path=str(OUT / ("sdedov-dialog-%s.png" % name)))
            pg4 = ctx.new_page(); pg4.goto("https://nad-lan.co.il/?v=" + str(int(time.time())), wait_until="load", timeout=120000)
            pg4.evaluate("document.querySelector('.nlhp-svcard--tour').scrollIntoView({block:'center'})"); pg4.wait_for_timeout(2500)
            r["home_card_img"] = pg4.evaluate("(()=>{const i=document.querySelector('.nlhp-svcard--tour img');return i?[i.currentSrc.slice(-60),i.complete,i.naturalWidth]:null})()")
            pg4.screenshot(path=str(OUT / ("home-card-%s.png" % name)))
        rep[name] = r; ctx.close()
    br.close()
json.dump(rep, open(OUT / "visit.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(rep, ensure_ascii=False, indent=1))
