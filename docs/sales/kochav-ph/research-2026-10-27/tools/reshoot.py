"""Re-shoot clean first screens: overlays (cookie/consent/survey/sign-in prompts/welcome modals) are hidden with
display:none in the local render only. Nothing is clicked or submitted."""
import sys, json, asyncio, os
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(__file__))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
targets = json.load(open(sys.argv[1], encoding='utf-8')); SH = sys.argv[2]
only = set(sys.argv[3].split(',')) if len(sys.argv) > 3 else None
UA_DESK = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
UA_MOB = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1'
DECLUTTER = r"""
() => {
  const vw = innerWidth, vh = innerHeight; const hidden = [];
  const rx = /cookie|consent|privacy|we value your|welcome to|fair housing|qualtrics|planning on buying|sign in with google|כניסה ל|עוגיות|באמצעות חשבון|this site uses|got it|allow all|manage cookies|accept all|decline all|are you planning|subscribe|newsletter|chat live|interested in arranging/i;
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el); if (cs.position !== 'fixed' && cs.position !== 'absolute' && cs.position !== 'sticky') continue;
    if (cs.display === 'none') continue; const r = el.getBoundingClientRect(); if (r.width*r.height < 2000) continue;
    const t = (el.innerText||'').slice(0,400); const z = parseInt(cs.zIndex)||0;
    const isGoogle = el.tagName==='IFRAME' && /accounts\.google|gsi/.test(el.src||'');
    const backdrop = cs.position==='fixed' && r.width>=vw*0.9 && r.height>=vh*0.9 && t.trim().length===0 && !el.querySelector('img,video,canvas');
    if (isGoogle || (cs.position!=='sticky' && rx.test(t) && t.length < 1500 && (z>=10 || cs.position==='fixed')) || backdrop) { el.style.setProperty('display','none','important'); hidden.push(t.slice(0,50)); }
  }
  for (const id of ['credential_picker_container','credential_picker_iframe']) { const e = document.getElementById(id); if (e) e.style.setProperty('display','none','important'); }
  document.documentElement.style.overflow='auto'; document.body.style.overflow='auto';
  return hidden;
}
"""
async def shot(b, t, mode):
    w = 390 if mode=='m' else 1280
    if only and t['name'] not in only: return None
    if mode=='m':
        ctx = await b.new_context(viewport={'width':390,'height':844}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=UA_MOB, locale=t.get('locale','en-US'))
    else:
        ctx = await b.new_context(viewport={'width':1280,'height':800}, user_agent=UA_DESK, locale=t.get('locale','en-US'))
    await ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
    p = await ctx.new_page(); out = {'name': t['name'], 'w': w}
    try:
        await p.goto(t['url'], wait_until='load', timeout=75000); await p.wait_for_timeout(t.get('wait', 7000))
        out['hidden'] = await p.evaluate(DECLUTTER); await p.wait_for_timeout(500)
        out['hidden2'] = await p.evaluate(DECLUTTER); await p.wait_for_timeout(300)
        await p.screenshot(path=os.path.join(SH, f"{t['name']}-{w}.png"))
        out['title'] = await p.title()
    except Exception as e:
        out['error'] = str(e)[:200]
    await ctx.close(); return out
async def main():
    sem = asyncio.Semaphore(4)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=CHROME, headless=True, args=['--disable-blink-features=AutomationControlled'])
        async def run(t,m):
            async with sem: return await shot(b,t,m)
        res = await asyncio.gather(*[run(t,m) for t in targets for m in ('m','d')])
        await b.close()
    for r in res:
        if r: print(r)
asyncio.run(main())
