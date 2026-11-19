import sys, asyncio
from playwright.async_api import async_playwright
async def m(src, out, w, h):
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome"); pg = await b.new_page(viewport={"width": w, "height": h})
        await pg.goto("file:///" + src.replace("\\", "/")); await pg.wait_for_timeout(2500)
        await pg.screenshot(path=out); await b.close()
asyncio.run(m(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])))
