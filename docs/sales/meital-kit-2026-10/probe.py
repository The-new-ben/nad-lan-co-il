import sys, time, json
from playwright.sync_api import sync_playwright
slug = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    c = b.new_context(viewport={"width": 1440, "height": 900}, locale="he-IL")
    pg = c.new_page()
    pg.goto(f"https://nad-lan.co.il/projects/{slug}/?nlshot={int(time.time())}", wait_until="load", timeout=120000)
    pg.wait_for_timeout(8000)
    r = pg.evaluate("""()=>{const out=[];document.querySelectorAll('#nlps button, #nlps [role=button], #nlps a, #nlps-stage button, .nlps button').forEach(e=>{const t=(e.innerText||e.getAttribute('aria-label')||'').trim().replace(/\s+/g,' ');if(t) out.push([e.tagName, e.className.toString().slice(0,60), (e.getAttribute('data-step')||e.getAttribute('data-act')||e.getAttribute('data-k')||''), t.slice(0,50)]);});return out.slice(0,90)}""")
    for x in r: print(x)
    b.close()
