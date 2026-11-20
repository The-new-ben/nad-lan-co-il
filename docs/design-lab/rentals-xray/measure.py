"""Cold-load measurement of the x-ray harness at a 390 x 844 viewport (desktop Chrome with a real GPU emulating a phone viewport, NOT a real phone).
   python docs/design-lab/rentals-xray/measure.py [--port 8765]"""
import json, os, time, argparse, statistics
from playwright.sync_api import sync_playwright
ap = argparse.ArgumentParser(); ap.add_argument("--port", default="8765"); a = ap.parse_args()
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUT = os.path.join(REPO, "docs", "rentals", "design", "board1b", "renders", "measure.json")
URL = f"http://127.0.0.1:{a.port}/docs/design-lab/rentals-xray/xray.html?mode=xray"
ARGS = ["--enable-gpu", "--use-angle=d3d11", "--ignore-gpu-blocklist", "--hide-scrollbars"]
def pct(v, p): v = sorted(v); return round(v[min(len(v) - 1, int(round(p / 100 * (len(v) - 1))))], 2)
def stats(v): return {"n": len(v), "mean": round(statistics.mean(v), 2), "median": round(statistics.median(v), 2), "p95": pct(v, 95), "max": round(max(v), 2)}
runs = []
with sync_playwright() as p:
    for attempt in range(3):   # three cold loads, each in a fresh browser (empty cache)
        b = p.chromium.launch(channel="chrome", headless=True, args=ARGS)
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg); cdp.send("Network.enable")
        req, fin = {}, {}
        cdp.on("Network.requestWillBeSent", lambda e: req.setdefault(e["requestId"], e["request"]["url"]))
        cdp.on("Network.loadingFinished", lambda e: fin.__setitem__(e["requestId"], e["encodedDataLength"]))
        cdp.on("Network.responseReceived", lambda e: None)
        t0 = time.time(); pg.goto(URL)
        pg.wait_for_function("window.__xrayReady===true && window.xray.ready()", timeout=120000); time.sleep(1.0)
        tim = pg.evaluate("xray.timings()"); gl = pg.evaluate("xray.gl()")
        items = [(u, fin.get(i, 0)) for i, u in req.items() if not u.startswith("data:")]
        tot = sum(n for _, n in items); three = sum(n for u, n in items if "three@" in u)
        rec = {"requests": len(items), "transferredBytes": tot, "threeJsBytes": three, "firstRenderMs": round(tim["firstRenderMs"], 1), "firstPresentedMs": round(tim["firstPresentedMs"], 1), "envReadyMs": round(tim["envReadyMs"], 1), "gl": gl,
               "urls": [{"url": u.replace(f"http://127.0.0.1:{a.port}", ""), "bytes": n} for u, n in items]}
        if attempt == 0:
            r = pg.evaluate("xray.spin(3000)")
            gaps, rend = r["gaps"], r["renders"]
            rec["orbit3s"] = {"frameGapMs": stats(gaps), "renderCallMs": stats(rend), "stats": pg.evaluate("xray.stats()")}
        runs.append(rec); b.close()
best = sorted(runs, key=lambda r: r["firstRenderMs"])[len(runs) // 2]
out = {"what": "cold load of xray.html at a 390 x 844 viewport, DPR 2, touch emulation: DESKTOP Chrome with a real GPU (ANGLE/D3D11) emulating a phone viewport. NOT a real phone; a phone's CPU/GPU, radio and thermal limits are not measured.",
       "page": "docs/design-lab/rentals-xray/xray.html?mode=xray", "server": "python http.server on 127.0.0.1 (no compression, no CDN for our own files); three.js from jsDelivr (compressed in transit)",
       "median_of_3_cold_loads": {k: best[k] for k in best if k not in ("urls",)}, "all_runs": [{k: r[k] for k in ("requests", "transferredBytes", "threeJsBytes", "firstRenderMs", "firstPresentedMs", "envReadyMs")} for r in runs],
       "request_list_run1": runs[0]["urls"], "orbit_spin_3s_run1": runs[0]["orbit3s"], "note_orbit": "renderCallMs is the CPU time inside renderer.render per drawn frame (command submission); frameGapMs is the time between animation frames. Neither is a phone measurement."}
json.dump(out, open(OUT, "w", encoding="utf8"), indent=1, ensure_ascii=False); print(json.dumps({k: out[k] for k in ("median_of_3_cold_loads", "all_runs", "orbit_spin_3s_run1")}, indent=1))
