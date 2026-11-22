# -*- coding: utf-8 -*-
"""HAD-801 loop cycle 3: the tour's first load on a mid phone. Chrome (headless, GPU) at 390 px, network throttled to a 4G-like
profile (9 Mbit/s down, 1.5 up, 150 ms round trip) and CPU slowed 4x. Three cold loads. Records: time to first paint, time until
the walk is ready (window.tourReady or the street cell live), bytes and requests until ready, and the biggest files.
  python phone_speed.py <url> <out json>"""
import json, os, statistics, sys, time
from playwright.sync_api import sync_playwright
CH = os.path.join(os.environ.get("PROGRAMFILES", "C:/Program Files"), "Google/Chrome/Application/chrome.exe")
URL, OUT = sys.argv[1], sys.argv[2]
runs = []
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=CH, headless=True, args=["--enable-gpu"])
    for i in range(3):
        ctx = br.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
        pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
        cdp.send("Network.enable"); cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
        cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": 150, "downloadThroughput": 9e6 / 8, "uploadThroughput": 1.5e6 / 8})
        cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
        rows = []; t0 = time.time()
        pg.on("response", lambda r: rows.append((round(time.time() - t0, 2), r.url)))
        pg.goto(URL + ("&" if "?" in URL else "?") + "ps=%d%d" % (int(t0), i), wait_until="domcontentloaded", timeout=180000)
        dcl = round(time.time() - t0, 2)
        try:
            pg.wait_for_function("window.tourReady || (window.round2StreetCell && window.round2StreetCell.live)", timeout=180000)
            ready = round(time.time() - t0, 2)
        except Exception:
            ready = None
        m = pg.evaluate("""(()=>{const p=performance.getEntriesByType('paint').find(e=>e.name==='first-contentful-paint');
          const n=performance.getEntriesByType('navigation')[0];const res=performance.getEntriesByType('resource');
          const big=res.map(e=>[Math.round((e.encodedBodySize||e.transferSize||0)/1024),e.name.split('/').slice(-2).join('/').slice(0,70),Math.round(e.responseEnd)]).sort((a,b)=>b[0]-a[0]).slice(0,8);
          return {fcp:p?Math.round(p.startTime):null, html_kb:Math.round((n.encodedBodySize||0)/1024), html_ms:Math.round(n.responseEnd),
                  bytes_kb:Math.round(res.reduce((s,e)=>s+(e.encodedBodySize||e.transferSize||0),n.encodedBodySize||0)/1024), requests:res.length, big}})()""")
        m.update({"dcl_s": dcl, "ready_s": ready}); runs.append(m); ctx.close()
    br.close()
med = lambda k: statistics.median([r[k] for r in runs if r[k] is not None]) if any(r[k] is not None for r in runs) else None
out = {"url": URL, "profile": "390px, 4x CPU, 9/1.5 Mbit/s, 150 ms", "median": {k: med(k) for k in ("fcp", "dcl_s", "ready_s", "html_kb", "html_ms", "bytes_kb", "requests")}, "runs": runs}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out["median"]), "\nbiggest (run 1):", runs[0]["big"])
