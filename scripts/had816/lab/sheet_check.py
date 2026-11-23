# HAD-816 lab: the phone sheet must rest above a floating bottom bar (the lab bar imitates the site's WhatsApp pill)
import os, mimetypes, sys
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__)); PLUG = os.path.join(H, '..', '..', '..', 'plugins', 'nadlan-config')
BASE = sys.argv[1] if len(sys.argv) > 1 else 'https://lab.local/transit/'
def route(r):
    u = r.request.url
    if u.startswith('https://lab.local/plugin/'):
        p = os.path.join(PLUG, u.split('/plugin/', 1)[1].split('?')[0]); return r.fulfill(path=p, content_type='application/json' if p.endswith('.json') else (mimetypes.guess_type(p)[0] or 'text/plain'))
    if u.startswith('https://lab.local/'): return r.fulfill(path=os.path.join(H, 'out-he.html'), content_type='text/html; charset=utf-8')
    return r.continue_()
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge')
    for w, h in ((390, 844), (360, 780)):
        pg = b.new_page(viewport={'width': w, 'height': h}, is_mobile=True, has_touch=True)
        if 'lab.local' in BASE: pg.route('**/*', route)
        pg.goto(BASE); pg.wait_for_timeout(7000)
        for q, tag in (('ארלוזורוב', 'station'), ('DUO', 'project')):
            pg.fill('#nltr-q', q); pg.wait_for_timeout(600); pg.click('.nltr-res button'); pg.wait_for_timeout(2500)
            r = pg.evaluate("""(()=>{const c=document.getElementById('nltr-card').getBoundingClientRect();let bt=innerHeight;document.querySelectorAll('body *').forEach(e=>{const s=getComputedStyle(e);if(s.position==='fixed'&&!document.getElementById('nltr').contains(e)){const b=e.getBoundingClientRect();if(b.height>30&&b.height<160&&b.width>120&&b.top>innerHeight*0.55&&b.bottom<=innerHeight+2)bt=Math.min(bt,b.top)}});return {cardTop:Math.round(c.top),cardBottom:Math.round(c.bottom),barTop:Math.round(bt),clear:c.bottom<=bt+1}})()""")
            pg.screenshot(path=os.path.join(H, 'shots', 'sheet-%s-%d.png' % (tag, w))); print(w, tag, r)
    b.close()
