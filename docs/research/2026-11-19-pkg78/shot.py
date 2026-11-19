# -*- coding: utf-8 -*-
"""HAD-793 evidence shots: python shot.py <outdir> <name> <url> [phone|desktop|both] [scrollY] [waitms]"""
import sys, os, asyncio
from playwright.async_api import async_playwright
out, name, url = sys.argv[1], sys.argv[2], sys.argv[3]
mode = sys.argv[4] if len(sys.argv) > 4 else "both"
sy = int(sys.argv[5]) if len(sys.argv) > 5 else 0
wait = int(sys.argv[6]) if len(sys.argv) > 6 else 2500
os.makedirs(out, exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        sizes = []
        if mode in ("desktop", "both"): sizes.append(("desktop", dict(viewport={"width": 1440, "height": 900})))
        if mode in ("phone", "both"): sizes.append(("phone", dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")))
        for tag, kw in sizes:
            ctx = await b.new_context(**kw); pg = await ctx.new_page()
            await pg.goto(url, wait_until="domcontentloaded", timeout=90000)
            await pg.wait_for_timeout(wait)
            if sy: await pg.evaluate("window.scrollTo(0,%d)" % sy); await pg.wait_for_timeout(1200)
            f = os.path.join(out, "%s-%s.png" % (name, tag)); await pg.screenshot(path=f); print(f)
            await ctx.close()
        await b.close()
asyncio.run(main())
