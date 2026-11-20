"""Cold-load measurement of the x-ray harness at a 390 x 844 viewport, ambient-shading pass ON and OFF (round 3).
   DESKTOP Chrome with a real GPU emulating a phone viewport, NOT a real phone.
   python docs/design-lab/rentals-xray/measure.py [--port 8765]"""
import json, os, time, argparse, statistics
from playwright.sync_api import sync_playwright
ap = argparse.ArgumentParser(); ap.add_argument("--port", default="8765"); a = ap.parse_args()
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
R = os.path.join(REPO, "docs", "rentals", "design", "board1b")
BASE = f"http://127.0.0.1:{a.port}/docs/design-lab/rentals-xray/xray.html?mode=xray&markers=1"
ARGS = ["--enable-gpu", "--use-angle=d3d11", "--ignore-gpu-blocklist", "--hide-scrollbars"]
def pct(v, p): v = sorted(v); return round(v[min(len(v) - 1, int(round(p / 100 * (len(v) - 1))))], 2)
def stats(v): return {"n": len(v), "mean": round(statistics.mean(v), 2), "median": round(statistics.median(v), 2), "p95": pct(v, 95), "max": round(max(v), 2)}
def kind(u):
    if "three@" in u: return "three.js (jsDelivr, compressed)"
    if "fonts.g" in u: return "web fonts (Google Fonts)"
    return "own files (local server, uncompressed)"
def one(p, qs, first):
    b = p.chromium.launch(channel="chrome", headless=True, args=ARGS)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg); cdp.send("Network.enable"); req, fin = {}, {}
    cdp.on("Network.requestWillBeSent", lambda e: req.setdefault(e["requestId"], e["request"]["url"])); cdp.on("Network.loadingFinished", lambda e: fin.__setitem__(e["requestId"], e["encodedDataLength"]))
    pg.goto(BASE + qs); pg.wait_for_function("window.__xrayReady===true && window.xray.ready()", timeout=120000); time.sleep(1.2)
    tim = pg.evaluate("xray.timings()"); items = [(u, fin.get(i, 0)) for i, u in req.items() if not u.startswith("data:")]
    by = {}; [by.__setitem__(kind(u), by.get(kind(u), 0) + n) for u, n in items]
    rec = {"requests": len(items), "transferredBytes": sum(n for _, n in items), "bytesByKind": by, "firstRenderMs": round(tim["firstRenderMs"], 1), "firstPresentedMs": round(tim["firstPresentedMs"], 1), "envReadyMs": round(tim["envReadyMs"], 1), "gl": pg.evaluate("xray.gl()")}
    if first:
        rec["urls"] = [{"url": u.replace(f"http://127.0.0.1:{a.port}", ""), "bytes": n, "kind": kind(u)} for u, n in items]
        rec["bench150FramesOrbit"] = pg.evaluate("xray.bench(150)"); sp = pg.evaluate("xray.spin(3000)")
        rec["spin3s"] = {"frameGapMs": stats(sp["gaps"]), "renderCallMs": stats(sp["renders"])}; rec["stats"] = pg.evaluate("xray.stats()")
    b.close(); return rec
res = {}
with sync_playwright() as p:
    for name, qs in [("ao_on", ""), ("ao_off", "&ao=0")]:
        runs = [one(p, qs, i == 0) for i in range(3)]; med = sorted(runs, key=lambda r: r["firstRenderMs"])[1]
        res[name] = {"median_of_3_cold_loads": {k: med[k] for k in ("requests", "transferredBytes", "bytesByKind", "firstRenderMs", "firstPresentedMs", "envReadyMs", "gl")}, "all_runs": [{k: r[k] for k in ("requests", "transferredBytes", "firstRenderMs", "firstPresentedMs", "envReadyMs")} for r in runs],
                     "request_list_run1": runs[0]["urls"], "bench150FramesOrbit": runs[0]["bench150FramesOrbit"], "spin3s_run1": runs[0]["spin3s"], "scene_stats": runs[0]["stats"]}
out = {"what": "cold load of xray.html?mode=xray&markers=1 at a 390 x 844 viewport, DPR 2, touch emulation: DESKTOP Chrome with a real GPU (ANGLE/D3D11, AMD Radeon integrated) emulating a phone viewport. NOT a real phone: a phone's CPU/GPU, radio and thermal limits are not measured.",
       "note": "bench150FramesOrbit renders 150 frames with a 1-pixel read-back so the GPU has really finished (cpuSubmitMs = time to issue the draw calls, withGpuSyncMs = issue + GPU). spin3s is the engine's own helper (frame gap is capped at 30 fps in this headless Chrome). Own files are served uncompressed by python http.server and the plugin's three.js addons come from jsDelivr.", **res,
       "ao_cost_ms_per_frame": {"p95_withGpuSync": round(res["ao_on"]["bench150FramesOrbit"]["withGpuSyncMs"]["p95"] - res["ao_off"]["bench150FramesOrbit"]["withGpuSyncMs"]["p95"], 2), "median_withGpuSync": round(res["ao_on"]["bench150FramesOrbit"]["withGpuSyncMs"]["median"] - res["ao_off"]["bench150FramesOrbit"]["withGpuSyncMs"]["median"], 2)}}
json.dump(out, open(os.path.join(R, "gate", "measure-ao.json"), "w", encoding="utf8"), indent=1, ensure_ascii=False)
json.dump(out, open(os.path.join(R, "renders", "measure.json"), "w", encoding="utf8"), indent=1, ensure_ascii=False)
for n in ("ao_on", "ao_off"): print(n, json.dumps(res[n]["median_of_3_cold_loads"]), json.dumps(res[n]["bench150FramesOrbit"]), json.dumps(res[n]["all_runs"]))
print(json.dumps(out["ao_cost_ms_per_frame"]))
