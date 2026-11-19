# -*- coding: utf-8 -*-
"""HAD-793: the Sde Dov tour, LOCAL file (pre) or live (/tour/sde-dov/), explore mode: people up close, then walk to the sea."""
import asyncio, os, re, json, sys
from playwright.async_api import async_playwright
H = os.path.dirname(os.path.abspath(__file__))
TAG = sys.argv[1] if len(sys.argv) > 1 else "pre"
SRC = open(os.path.join(H, "..", "..", "..", "plugins", "nadlan-config", "assets", "tours", "sde-dov-tour.html"), "rb").read()
OUT = os.path.join(H, "pre" if TAG == "pre" else "after"); os.makedirs(OUT, exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        for tag, kw in [("desktop", dict(viewport={"width": 1440, "height": 900})), ("phone", dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True))]:
            ctx = await b.new_context(reduced_motion="reduce", **kw); pg = await ctx.new_page(); errs = []; logs = []
            pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: logs.append(m.text) if m.type in ("error", "warning") else None)
            if TAG == "pre":
                await pg.route(re.compile(r".*/tour/sde-dov/.*"), lambda r: r.fulfill(body=SRC, content_type="text/html; charset=utf-8"))
            await pg.goto("https://nad-lan.co.il/tour/sde-dov/?mode=explore&focus=rainbow&t793=" + TAG, wait_until="domcontentloaded", timeout=90000)
            await pg.wait_for_timeout(16000)
            await pg.screenshot(path=os.path.join(OUT, "%s-tour-rainbow-%s.png" % (TAG, tag)))
            ok = await pg.evaluate("!!document.getElementById('mmSea')")
            if ok:
                await pg.evaluate("document.getElementById('mmSea').click()")
                for i in range(30):
                    await pg.wait_for_timeout(1000)
                    st = await pg.evaluate("(()=>{const d=window.__dbg; return d? {node:d.ex.node.id, gl:d.ex.gliding, route:(d.ex.route||[]).length}: null})()")
                    if st and st["node"] == "sea" and not st["gl"]: break
                await pg.wait_for_timeout(2500)
                print(tag, "after walk", st)
                await pg.screenshot(path=os.path.join(OUT, "%s-tour-sea-%s.png" % (TAG, tag)))
            print(tag, "mmSea", ok, "errors", errs[:3], "console", [l for l in logs if 'WebGL' not in l][:4])
            await ctx.close()
        await b.close()
asyncio.run(main())
