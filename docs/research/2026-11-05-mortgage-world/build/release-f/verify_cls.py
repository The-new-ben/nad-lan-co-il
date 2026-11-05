# -*- coding: utf-8 -*-
"""Round F2 check: CLS on phone widths and desktop, live (--live) or with the reserve style injected before the quick calculator."""
import sys, time, re, os
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
LIVE = "--live" in sys.argv
ns = {}; src = open(os.path.join(H, "write_page_f2.py"), encoding="utf-8").read()
exec(src[src.index("TOOL = "):src.index("P_END = ")], ns)
INIT = """window.__cls=0;window.__src=[];new PerformanceObserver(l=>{for(const e of l.getEntries()){if(e.hadRecentInput)continue;window.__cls+=e.value;
 window.__src.push(+e.value.toFixed(4)+' '+(e.sources||[]).map(s=>s.node&&s.node.nodeType===1?s.node.tagName.toLowerCase()+'.'+String(s.node.className).slice(0,30):'#').join(','));}}).observe({type:'layout-shift',buffered:true});"""
def run(p, url, res, w, mob):
    b = p.chromium.launch(channel="chrome", headless=True)
    ctx = b.new_context(viewport={"width": w, "height": 844 if mob else 900}, is_mobile=mob, has_touch=mob); ctx.add_init_script(INIT)
    pg = ctx.new_page()
    def swap(route):
        r = route.fetch(); body = r.text()
        if not LIVE:
            i = body.find('<section class="nli"'); assert i > 0; body = body[:i] + res + body[i:]
        route.fulfill(response=r, body=body, headers={**r.headers, "content-type": "text/html; charset=UTF-8"})
    pg.route(re.compile(re.escape(url) + r"\?vc="), swap)
    pg.goto(url + "?vc=%d" % time.time(), wait_until="load", timeout=90000); time.sleep(5)
    v = pg.evaluate("[window.__cls, window.__src, document.documentElement.scrollWidth - innerWidth]"); b.close(); return v
with sync_playwright() as p:
    for url, res in (("https://nad-lan.co.il/mortgage-calculator/", ns["RES_HE"]), ("https://nad-lan.co.il/en/mortgage-calculator/", ns["RES_EN"])):
        for w, mob in ((360, True), (390, True), (412, True), (768, False), (1280, False)):
            c, s, hs = run(p, url, res, w, mob)
            print(("live " if LIVE else "f2   ") + url.split(".il")[1], w, "CLS", round(c, 4), "hscroll", hs, s[:3])
