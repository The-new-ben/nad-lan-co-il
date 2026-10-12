import sys, time
from playwright.sync_api import sync_playwright
slug = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    c = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2, locale="he-IL")
    pg = c.new_page()
    pg.goto(f"https://nad-lan.co.il/projects/{slug}/?nlshot={int(time.time())}", wait_until="load", timeout=120000)
    pg.wait_for_timeout(8000)
    pg.click("button.rbs-open"); pg.wait_for_timeout(8000)
    pg.screenshot(path=f"shots/{slug}-d-tour.png")
    r = pg.evaluate("""()=>{const out=[];document.querySelectorAll('button,[role=button],[role=tab]').forEach(e=>{const s=getComputedStyle(e);if(s.display==='none'||s.visibility==='hidden'||!e.offsetParent)return;const t=(e.innerText||e.getAttribute('aria-label')||'').trim().replace(/\s+/g,' ');if(t) out.push([e.className.toString().slice(0,50), t.slice(0,40)]);});return out}""")
    for x in r[:120]: print(x)
    b.close()
