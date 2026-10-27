"""View-only captures for the floor-plan research. Only clicks gallery/floor-plan tabs (no forms)."""
import sys, json, asyncio, os, re
from playwright.async_api import async_playwright
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
targets = json.load(open(sys.argv[1], encoding='utf-8')); OUT = sys.argv[2]
DECL = open('declutter.js', encoding='utf-8').read()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, headless=True, args=['--disable-blink-features=AutomationControlled'])
        for t in targets:
            w,h = t.get('vp',[1280,800])
            ctx = await b.new_context(viewport={'width':w,'height':h}, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', locale=t.get('locale','en-US'))
            await ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
            pg = await ctx.new_page(); res={'name':t['name']}
            try:
                await pg.goto(t['url'], wait_until='load', timeout=75000); await pg.wait_for_timeout(t.get('wait',6000))
                await pg.evaluate(DECL)
                if t.get('scroll_text'):
                    loc = pg.get_by_text(t['scroll_text'], exact=False).first
                    await loc.scroll_into_view_if_needed(timeout=8000); await pg.wait_for_timeout(1500)
                if t.get('scroll_y') is not None:
                    await pg.evaluate(f"window.scrollTo(0,{t['scroll_y']})"); await pg.wait_for_timeout(2000)
                if t.get('wheel'):
                    await pg.mouse.move(640, 500)
                    for _ in range(t['wheel'][1]):
                        await pg.mouse.wheel(0, t['wheel'][0]); await pg.wait_for_timeout(250)
                    await pg.wait_for_timeout(2000)
                if t.get('click_re'):
                    loc = pg.get_by_text(re.compile(t['click_re'], re.I)).nth(t.get('nth',0))
                    await loc.scroll_into_view_if_needed(timeout=8000)
                    await loc.click(timeout=10000); await pg.wait_for_timeout(t.get('after',3500))
                    await pg.evaluate(DECL)
                if t.get('click'):
                    loc = pg.get_by_role('button', name=t['click']).first if t.get('role') else pg.get_by_text(t['click'], exact=True).first
                    await loc.click(timeout=10000); await pg.wait_for_timeout(t.get('after',3500))
                    await pg.evaluate(DECL)
                fn = os.path.join(OUT, t['name'] + '.png')
                await pg.screenshot(path=fn, full_page=t.get('full',False))
                res['ok']=fn; res['title']=await pg.title()
            except Exception as e:
                res['err']=str(e)[:200]
                try: await pg.screenshot(path=os.path.join(OUT, t['name'] + '-err.png'))
                except Exception: pass
            print(res, flush=True); await ctx.close()
        await b.close()
asyncio.run(main())
