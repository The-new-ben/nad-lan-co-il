import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True)
    ctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="he-IL")
    pg = ctx.new_page(); pg.goto("https://nad-lan.co.il/projects/aurelia/", wait_until="load", timeout=120000); pg.wait_for_timeout(3000)
    pg.mouse.wheel(0, 900); pg.wait_for_timeout(2500)
    print(json.dumps(pg.evaluate("""()=>{const s=document.getElementById('nl-sticky');if(!s)return null;return [...s.querySelectorAll('a,button')].map(a=>{const c=getComputedStyle(a);const sp=[...a.querySelectorAll('span,b,strong')].map(x=>[x.textContent.trim().slice(0,20),getComputedStyle(x).color,getComputedStyle(x).opacity]);return {t:a.textContent.trim().slice(0,30),color:c.color,bg:c.backgroundColor,bgimg:c.backgroundImage.slice(0,80),op:c.opacity,spans:sp}})}"""), ensure_ascii=False))
    br.close()
