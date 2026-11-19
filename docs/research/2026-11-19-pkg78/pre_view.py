# -*- coding: utf-8 -*-
import asyncio, os, re, json, sys
from playwright.async_api import async_playwright
H = os.path.dirname(os.path.abspath(__file__))
JS = open(os.path.join(H, "..", "..", "..", "scripts", "had793", "live", "bridge.js"), "rb").read()
OUT = os.path.join(H, "pre"); os.makedirs(OUT, exist_ok=True)
URL = sys.argv[1] if len(sys.argv) > 1 else "https://nad-lan.co.il/projects/rainbow-tel-aviv/"
TAG = sys.argv[2] if len(sys.argv) > 2 else "pre"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        for tag, kw in [("desktop", dict(viewport={"width": 1440, "height": 900})), ("phone", dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True))]:
            ctx = await b.new_context(**kw); pg = await ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            if TAG == "pre":
                await pg.route(re.compile(r".*/assets/project-stage/bridge\.js.*"), lambda r: r.fulfill(body=JS, content_type="application/javascript"))
            await pg.goto(URL + ("&" if "?" in URL else "?") + "t793v=" + TAG, wait_until="domcontentloaded", timeout=90000)
            await pg.wait_for_timeout(9000)
            await pg.evaluate("window.dispatchEvent(new CustomEvent('nl:facing',{detail:{floor:9,heightM:33,bearing:355}}))")
            await pg.wait_for_timeout(1500)
            await pg.evaluate("(document.getElementById('nlps-view-map')||document.body).scrollIntoView({block:'center'})")
            await pg.wait_for_timeout(9000)
            el = await pg.query_selector("#nlps-view") or await pg.query_selector("#nlps-view-map")
            await (el.screenshot(path=os.path.join(OUT, "%s-view-plan-%s.png" % (TAG, tag))) if el else pg.screenshot(path=os.path.join(OUT, "%s-view-plan-%s.png" % (TAG, tag))))
            info = await pg.evaluate("(()=>{const b=document.querySelector('.nlps-plan');return b?{text:b.innerText.slice(0,400),pressed:[...b.querySelectorAll('[aria-pressed=true]')].map(x=>x.innerText)}:null})()")
            print(tag, json.dumps(info, ensure_ascii=False)); print("errors", errs[:4])
            if info:
                await pg.click(".nlps-plan [data-plan=today]"); await pg.wait_for_timeout(3000)
                await el.screenshot(path=os.path.join(OUT, "%s-view-today-%s.png" % (TAG, tag)))
            await ctx.close()
        await b.close()
asyncio.run(main())
