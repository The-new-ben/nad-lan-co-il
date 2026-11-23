# -*- coding: utf-8 -*-
"""HAD-801: look at the breadcrumb on the places list and on the tour card, desktop 1440 and phone 390; JSON-LD parsed.
  python hierarchy_check.py <base url ending in /tour/sde-dov/> <out dir>"""
import json, os, sys
from playwright.sync_api import sync_playwright
B, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
CH = os.path.join(os.environ.get("PROGRAMFILES", "C:/Program Files"), "Google/Chrome/Application/chrome.exe")
rep = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=CH, headless=True, args=["--enable-gpu"])
    for name, a in (("desktop", dict(viewport={"width": 1440, "height": 900})), ("phone", dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2))):
        ctx = br.new_context(**a); pg = ctx.new_page(); errs = []
        pg.on("console", lambda m: errs.append(m.text[:100]) if m.type == "error" else None)
        pg.goto(B + "places/", wait_until="load", timeout=90000); pg.wait_for_timeout(800)
        r = pg.evaluate("""(()=>{const n=document.querySelector('.nlbc');const ld=[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>{try{return JSON.parse(s.textContent)['@type']}catch(e){return 'BAD'}});
          return {crumb:n?n.innerText:null,line:(document.querySelector('.nlparent')||{}).innerText,ld,h1:document.querySelector('h1').innerText,
          hub:[...document.querySelectorAll('a[href="https://nad-lan.co.il/sde-dov/"]')].map(x=>x.innerText).reduce((m,t)=>(m[t]=(m[t]||0)+1,m),{})}})()""")
        pg.screenshot(path=os.path.join(OUT, "places-top-%s.png" % name)); rep[name + "-places"] = r
        pg.goto(B, wait_until="domcontentloaded"); pg.wait_for_function("window.tourReady||(window.round2StreetCell&&window.round2StreetCell.live)", timeout=120000); pg.wait_for_timeout(3000)
        rep[name + "-tour"] = pg.evaluate("""(()=>{const n=document.querySelector('#hud .nlbc');const r=n&&n.getBoundingClientRect();return {crumb:n?n.innerText:null,box:r?[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)]:null,
          ld:[...document.querySelectorAll('script[type="application/ld+json"]')].length}})()""")
        pg.screenshot(path=os.path.join(OUT, "tour-card-%s.png" % name))
        rep[name + "-errors"] = errs[:3]; ctx.close()
    br.close()
print(json.dumps(rep, ensure_ascii=False, indent=1))
