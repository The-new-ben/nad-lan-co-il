# -*- coding: utf-8 -*-
import asyncio, os, re, urllib.request, json
from playwright.async_api import async_playwright
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
JS = open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "tools", "mquick.js"), "rb").read()
HTML = urllib.request.urlopen(urllib.request.Request("https://nad-lan.co.il/en/mortgage-calculator/?pre793=1", headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8")
OUT = os.path.join(os.path.dirname(__file__), "pre"); os.makedirs(OUT, exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome")
        for L in ("fr", "ru", "en"):
            h = HTML.replace('<section class="nli" dir="ltr" lang="en"', '<section class="nli" dir="ltr" lang="%s"' % L)
            assert h.count('lang="%s"' % L) >= 1
            ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
            pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.route(re.compile(r".*/tools/mquick\.js.*"), lambda r: r.fulfill(body=JS, content_type="application/javascript"))
            def mk(hh):
                return lambda r: r.fulfill(body=hh, content_type="text/html; charset=utf-8")
            await pg.route(re.compile(r".*/en/mortgage-calculator/\?pre793=1$"), mk(h))
            await pg.goto("https://nad-lan.co.il/en/mortgage-calculator/?pre793=1", wait_until="domcontentloaded")
            await pg.wait_for_timeout(4000)
            await pg.evaluate("document.getElementById('nlmq') && document.getElementById('nlmq').scrollIntoView()")
            await pg.wait_for_timeout(800)
            # press the 20-year term and "by price" to exercise the strings
            await pg.evaluate("(()=>{const b=document.querySelector('#nlmq [data-y=\"20\"]'); b&&b.click(); const m=document.querySelector('#nlmq [data-m=\"price\"]'); m&&m.click();})()")
            await pg.wait_for_timeout(600)
            info = await pg.evaluate("(()=>{const r=document.getElementById('nlmq');return r?{lang:r.getAttribute('lang'),dir:r.dir,fig:r.querySelector('.nlmq__fig').innerText,ol:r.querySelector('.nlmq__ol').innerText,sub:r.querySelector('.nlmq__sub').innerText,ltv:r.querySelector('.nlmq__ltv').innerText,src:r.querySelector('.nlmq__src').innerText.slice(0,160),h:r.querySelector('h2').innerText}:null})()")
            print(L, json.dumps(info, ensure_ascii=False)); print("errors", errs[:3])
            await pg.screenshot(path=os.path.join(OUT, "pre-mquick-%s-phone.png" % L))
            await ctx.close()
        await b.close()
asyncio.run(main())
