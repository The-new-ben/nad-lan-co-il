import asyncio, os, re, sys
from playwright.async_api import async_playwright
H = os.path.dirname(os.path.abspath(__file__))
TAG = sys.argv[1] if len(sys.argv) > 1 else "pre"
SRC = open(os.path.join(H, "..", "..", "..", "plugins", "nadlan-config", "assets", "tours", "sde-dov-tour.html"), "rb").read()
OUT = os.path.join(H, "pre" if TAG == "pre" else "after")
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        ctx = await b.new_context(reduced_motion="reduce", viewport={"width": 1440, "height": 900}); pg = await ctx.new_page()
        if TAG == "pre":
            await pg.route(re.compile(r".*/tour/sde-dov/.*"), lambda r: r.fulfill(body=SRC, content_type="text/html; charset=utf-8"))
        await pg.goto("https://nad-lan.co.il/tour/sde-dov/?mode=explore&focus=sea&t793=" + TAG, wait_until="domcontentloaded", timeout=90000)
        await pg.wait_for_timeout(14000)
        await pg.screenshot(path=os.path.join(OUT, "%s-tour-sea-arrival.png" % TAG))
        for name, x, y, z, yaw, pitch in [("plaza", -4, 1.75, -244, 0.15, -0.12), ("beach", -150, 1.75, -42, 0.2, -0.1)]:
            await pg.evaluate("([x,y,z,yaw,pitch])=>{const d=window.__dbg; d.ex.pos.set(x,y,z); d.ex.from.set(x,y,z); d.ex.to.set(x,y,z); d.ex.gliding=false; d.ex.yaw=d.ex.tYaw=yaw; d.ex.pitch=d.ex.tPitch=pitch; d.ex.fov=d.ex.fovT=52;}", [x, y, z, yaw, pitch])
            await pg.wait_for_timeout(3500)
            await pg.screenshot(path=os.path.join(OUT, "%s-people-%s.png" % (TAG, name)))
        await b.close()
asyncio.run(main())
