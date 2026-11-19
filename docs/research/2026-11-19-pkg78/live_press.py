import asyncio, json, os
from playwright.async_api import async_playwright
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "after")
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome")
        for L in ("fr", "ru"):
            ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True); pg = await ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("https://nad-lan.co.il/%s/mortgage-calculator/?t709z=1" % L, wait_until="domcontentloaded"); await pg.wait_for_timeout(5000)
            await pg.locator("#nlmq").scroll_into_view_if_needed()
            before = await pg.locator("#nlmq .nlmq__fig").inner_text()
            await pg.locator('#nlmq [data-y="20"]').click(); await pg.wait_for_timeout(500)
            after20 = await pg.locator("#nlmq .nlmq__fig").inner_text()
            await pg.locator('#nlmq [data-b="leumi"]').click(); await pg.wait_for_timeout(500)
            leumi = await pg.locator("#nlmq .nlmq__fig").inner_text(); src = await pg.locator("#nlmq .nlmq__src").inner_text()
            await pg.locator("#nlmq").screenshot(path=os.path.join(OUT, "live-%s-mortgage-pressed-20y-leumi.png" % L))
            print(L, json.dumps({"25y": before, "20y": after20, "20y_leumi": leumi, "src": src[:120], "errors": errs[:2]}, ensure_ascii=False))
            await ctx.close()
        ctx = await b.new_context(viewport={"width": 1920, "height": 1080}); pg = await ctx.new_page()
        await pg.goto("https://nad-lan.co.il/israel-mortgage-non-residents/?t709z=1", wait_until="domcontentloaded"); await pg.wait_for_timeout(4000)
        info = await pg.evaluate("""()=>({author:(document.querySelector('.wp-block-post-author-name')||{}).innerText, h1font:getComputedStyle(document.querySelector('h1')).fontFamily, toc:!!document.querySelector('.nlpg-toc') && getComputedStyle(document.querySelector('.nlpg-toc')).display, tocItems:document.querySelectorAll('.nlpg-toc li').length, img:(document.querySelector('.wp-post-image')||{}).currentSrc})""")
        print("nonres", json.dumps(info, ensure_ascii=False))
        await pg.evaluate("window.scrollTo(0, document.querySelector('.wp-block-post-content').getBoundingClientRect().top + scrollY - 90)"); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=os.path.join(OUT, "live-nonres-1920-toc.png"))
        await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=os.path.join(OUT, "live-nonres-1920-top.png"))
        await b.close()
asyncio.run(main())
