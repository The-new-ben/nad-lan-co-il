import sys, asyncio, os
from playwright.async_api import async_playwright
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT = r"C:\Users\777\nad-lan\nad-lan-co-il\docs\sales\kochav-ph\research-2026-10-27\shots\plans"
DECL = open('declutter.js', encoding='utf-8').read()
T = [("p02-sothebys-39crosby-floorplan","https://www.sothebysrealty.com/nyc/eng/sales/detail/709-l-1178-67s98b/39-crosby-street-phn-soho-new-york-ny-10013","floor plan",0),
     ("p04-centralparktower-dev-floorplan","https://centralparktower.com/availability","view",3)]
CLICK = r"""([txt, n]) => { const els = Array.from(document.querySelectorAll('button,a,span,div,li')).filter(e => (e.innerText||'').trim().toLowerCase()===txt && e.children.length<=2);
  const vis = els.filter(e => { const r=e.getBoundingClientRect(); return r.width>0 && r.height>0; });
  const el = vis[n] || vis[0] || els[n] || els[0]; if (!el) return 'none ' + els.length; el.scrollIntoView({block:'center'}); el.click(); return 'clicked ' + el.tagName + ' of ' + vis.length + '/' + els.length; }"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, headless=True, args=['--disable-blink-features=AutomationControlled'])
        for name, url, txt, n in T:
            ctx = await b.new_context(viewport={'width':1280,'height':800}, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36')
            pg = await ctx.new_page()
            try:
                await pg.goto(url, wait_until='load', timeout=75000); await pg.wait_for_timeout(7000)
                await pg.evaluate(DECL)
                print(name, await pg.evaluate(CLICK, [txt, n]))
                await pg.wait_for_timeout(5000); await pg.evaluate(DECL)
                await pg.screenshot(path=os.path.join(OUT, name + '.png'))
                imgs = await pg.evaluate("""() => Array.from(document.images).filter(i=>{const r=i.getBoundingClientRect(); return r.width>300 && r.top<800 && r.bottom>0}).map(i=>(i.currentSrc||i.src).slice(0,160)+' '+Math.round(i.getBoundingClientRect().width))""")
                print('  imgs', imgs[:5])
            except Exception as e: print(name, 'ERR', str(e)[:150])
            await ctx.close()
        await b.close()
asyncio.run(main())
