# -*- coding: utf-8 -*-
"""HAD-801: home page speed, before and after the release (5 fresh loads each width; median of load event, LCP, bytes).
  python home_speed.py <label> <out json>"""
import json, os, statistics, sys, time
from playwright.sync_api import sync_playwright
CH = os.path.join(os.environ.get("PROGRAMFILES", "C:/Program Files"), "Google/Chrome/Application/chrome.exe")
out = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=CH, headless=True)
    for name, a in (("desktop", dict(viewport={"width": 1440, "height": 900})), ("phone", dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2))):
        rows = []
        for i in range(5):
            ctx = br.new_context(**a); pg = ctx.new_page()
            pg.add_init_script("window.__lcp=0;new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true})")
            pg.goto("https://nad-lan.co.il/?hs=%d%d" % (int(time.time()), i), wait_until="load", timeout=90000); pg.wait_for_timeout(1500)
            rows.append(pg.evaluate("(()=>{const n=performance.getEntriesByType('navigation')[0];return {load:n.loadEventEnd,dcl:n.domContentLoadedEventEnd,lcp:window.__lcp,bytes:performance.getEntriesByType('resource').reduce((s,e)=>s+(e.transferSize||0),n.transferSize||0),tour:performance.getEntriesByType('resource').filter(e=>/tour\/sde-dov\//.test(e.name)).map(e=>e.name.slice(-40))}})()"))
            ctx.close()
        med = lambda k: round(statistics.median(r[k] for r in rows))
        out[name] = {"load_ms": med("load"), "dcl_ms": med("dcl"), "lcp_ms": med("lcp"), "bytes": med("bytes"), "tour_requests_on_load": rows[-1]["tour"], "runs": rows}
    br.close()
out["label"] = sys.argv[1]
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), indent=1)
print(json.dumps({k: {x: v[x] for x in ("load_ms", "dcl_ms", "lcp_ms", "bytes", "tour_requests_on_load")} for k, v in out.items() if k != "label"}, indent=1))
