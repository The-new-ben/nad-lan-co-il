"""The stage's first picture on a mid Android (Lighthouse's mobile profile: 4x CPU slowdown, Slow 4G 1.6 Mbps / 150 ms):
when the poster is painted, the LCP element and time, and when the live 3D takes over. A real GPU (d3d11)."""
import json, sys, time
from playwright.sync_api import sync_playwright
url = sys.argv[1]
runs = int(sys.argv[2]) if len(sys.argv) > 2 else 1
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-gpu"])
    for r in range(runs):
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True,
                            user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36")
        pg = ctx.new_page()
        cdp = ctx.new_cdp_session(pg)
        cdp.send("Network.enable")
        cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": 150, "downloadThroughput": 1638400 / 8, "uploadThroughput": 675000 / 8})
        cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
        pg.add_init_script("""
          window.__lcp = [];
          new PerformanceObserver((l) => { for (const e of l.getEntries()) window.__lcp.push({t: Math.round(e.startTime), el: e.element ? (e.element.tagName + '.' + (e.element.className || '')).slice(0, 60) : '', url: (e.url || '').split('/').pop().slice(0, 40)}); }).observe({type: 'largest-contentful-paint', buffered: true});
          window.__fcp = 0; new PerformanceObserver((l) => { for (const e of l.getEntries()) if (e.name === 'first-contentful-paint') window.__fcp = Math.round(e.startTime); }).observe({type: 'paint', buffered: true});
        """)
        t0 = time.time()
        pg.goto(url + ("&" if "?" in url else "?") + "fp=%d%d" % (int(time.time()), r), wait_until="commit", timeout=120000)
        poster_t = None; live_t = None; deadline = time.time() + 90
        while time.time() < deadline:
            st = pg.evaluate("""(() => { const im = document.querySelector('.rbs img, .rbs-poster img, #nlps img'); const r = im && im.getBoundingClientRect();
              return { poster: !!(im && im.complete && im.naturalWidth > 0 && r && r.top < innerHeight), phase: window.__nlpsStage && window.__nlpsStage.phase || null }; })()""")
            now = time.time() - t0
            if st["poster"] and poster_t is None: poster_t = now
            if st["phase"] and st["phase"] != "poster" and live_t is None: live_t = now
            if poster_t is not None and live_t is not None: break
            time.sleep(0.1)
        time.sleep(1.0)
        res = pg.evaluate("""(() => { const e = performance.getEntriesByType('resource').filter(x => /poster\.jpg|three\.module|stage\.js|bridge\.js|city\.json/.test(x.name));
            return e.map(x => [x.name.split('/').pop().split('?')[0], Math.round(x.startTime), Math.round(x.responseEnd), x.transferSize]); })()""")
        print(json.dumps({"run": r, "poster_visible_s": round(poster_t, 2) if poster_t else None, "live_3d_s": round(live_t, 2) if live_t else None,
                          "fcp_ms": pg.evaluate("window.__fcp"), "lcp": pg.evaluate("window.__lcp.slice(-2)"), "res": res}, ensure_ascii=False))
        ctx.close()
    b.close()
