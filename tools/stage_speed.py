# -*- coding: utf-8 -*-
"""Read-only: how fast a 3D project stage becomes usable on a phone (Kikar loop, 4.10.2026).

Cold loads (a fresh browser context each time, no cache) of a project page in Chrome with a phone profile (390x844, DPR 3,
touch). Two network profiles: "slow4g" = the Lighthouse mobile benchmark (1.6 Mbps down, 750 kbps up, 150 ms RTT, CPU 4x
slower) and "none" (no throttle). Per load it records, in ms from navigation start: TTFB, FCP, LCP, DOMContentLoaded, load,
the moment the world starts loading (its loader shows) and the moment it is usable (the poster is gone: world.js boot() done,
the scene drawn and the controls live), plus the bytes and the request count up to that moment.

  python tools/stage_speed.py https://nad-lan.co.il/projects/hamedina/ [--runs 3] [--out docs/research/stage-speed/x.json]"""
import json, os, statistics, sys, time

PROFILES = {
    "slow4g": {"down": 1.6e6 / 8, "up": 750e3 / 8, "rtt": 150, "cpu": 4},
    "none": None,
}


def one(p, url, prof):
    b = p.chromium.launch(channel="chrome", headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True,
                        user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Mobile Safari/537.36 NadLan-Speed/1.0")
    page = ctx.new_page()
    cdp = ctx.new_cdp_session(page)
    cdp.send("Network.enable")
    cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
    if prof:
        cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": prof["rtt"], "downloadThroughput": prof["down"], "uploadThroughput": prof["up"]})
        cdp.send("Emulation.setCPUThrottlingRate", {"rate": prof["cpu"]})
    page.add_init_script("""
      window.__nlS = {lcp: 0};
      try { new PerformanceObserver((l) => { for (const e of l.getEntries()) window.__nlS.lcp = e.startTime; }).observe({type: 'largest-contentful-paint', buffered: true}); } catch (e) {}
      const t0 = () => performance.now();
      const mo = new MutationObserver(() => {
        const ld = document.querySelector('.nlw-load');
        if (ld && !ld.hidden && !window.__nlS.loading) window.__nlS.loading = t0();
        const po = document.querySelector('.nlw-poster');
        if (po && !window.__nlS.poster) window.__nlS.poster = t0();
        if (po && po.classList.contains('is-gone') && !window.__nlS.ready) window.__nlS.ready = t0();
      });
      document.addEventListener('DOMContentLoaded', () => mo.observe(document.documentElement, {subtree: true, attributes: true, childList: true, attributeFilter: ['class', 'hidden']}));
    """)
    t = time.time()
    page.goto(url, wait_until="load", timeout=180000)
    deadline = time.time() + 120
    while time.time() < deadline:
        if page.evaluate("!!window.__nlS.ready"):
            break
        page.wait_for_timeout(250)
    r = page.evaluate("""() => {
      const n = performance.getEntriesByType('navigation')[0] || {};
      const fcp = (performance.getEntriesByName('first-contentful-paint')[0] || {}).startTime || 0;
      const S = window.__nlS || {};
      const cut = S.ready || performance.now();
      const res = performance.getEntriesByType('resource').filter((x) => x.startTime <= cut);
      const kb = Math.round((res.reduce((a, x) => a + (x.transferSize || 0), 0) + (n.transferSize || 0)) / 1024);
      const big = res.map((x) => [x.name.split('?')[0].slice(-60), Math.round((x.transferSize || 0) / 1024), Math.round(x.responseEnd)]).sort((a, b) => b[1] - a[1]).slice(0, 6);
      const stage = document.querySelector('#nlps, .nlw');
      const top = stage ? Math.round(stage.getBoundingClientRect().top + scrollY) : null;
      return {ttfb: Math.round(n.responseStart || 0), fcp: Math.round(fcp), lcp: Math.round(S.lcp || 0), dcl: Math.round(n.domContentLoadedEventEnd || 0),
              load: Math.round(n.loadEventEnd || 0), world_loading: Math.round(S.loading || 0), world_ready: Math.round(S.ready || 0),
              kb_to_ready: kb, requests_to_ready: res.length + 1, biggest: big, stage_top: top};
    }""")
    r["wall_s"] = round(time.time() - t, 1)
    b.close()
    return r


def main(argv):
    from playwright.sync_api import sync_playwright
    url = argv[0]
    runs = int(argv[argv.index("--runs") + 1]) if "--runs" in argv else 3
    out = argv[argv.index("--out") + 1] if "--out" in argv else None
    rep = {"url": url, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "runs": runs, "profiles": {}}
    with sync_playwright() as p:
        for name, prof in PROFILES.items():
            rows = []
            for i in range(runs):
                sep = "&" if "?" in url else "?"
                r = one(p, url + sep + f"nlspeed={int(time.time())}{i}", prof)
                rows.append(r)
                print(name, i + 1, {k: r[k] for k in ("ttfb", "fcp", "lcp", "dcl", "load", "world_loading", "world_ready", "kb_to_ready", "requests_to_ready")})
            med = {k: statistics.median([r[k] for r in rows]) for k in ("ttfb", "fcp", "lcp", "dcl", "load", "world_loading", "world_ready", "kb_to_ready", "requests_to_ready")}
            rep["profiles"][name] = {"median": med, "runs": rows}
            print(name, "MEDIAN", med)
    if out:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1))
        print("saved", out)


if __name__ == "__main__":
    main(sys.argv[1:])
