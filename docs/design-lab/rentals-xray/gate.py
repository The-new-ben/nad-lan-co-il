"""Round 3 gate frames: frame1-overview.png, frame2-part.png, clusters.json, plan-4r.png, plan-4r.json into docs/rentals/design/board1b/gate/.
   Needs: python -m http.server 8765 --bind 127.0.0.1 from the repo root, desktop Chrome with a real GPU.
   python docs/design-lab/rentals-xray/gate.py"""
import os, json, time, argparse
from playwright.sync_api import sync_playwright
ap = argparse.ArgumentParser(); ap.add_argument("--port", default="8765"); a = ap.parse_args()
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUT = os.path.join(REPO, "docs", "rentals", "design", "board1b", "gate"); os.makedirs(OUT, exist_ok=True)
BASE = f"http://127.0.0.1:{a.port}/docs/design-lab/rentals-xray/"
ARGS = ["--enable-gpu", "--use-angle=d3d11", "--ignore-gpu-blocklist", "--hide-scrollbars"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=ARGS)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    def settle(pg): pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))"); time.sleep(0.4)
    # frame one: x-ray, all layers, the home turned toward the boiler's room, room-cluster markers
    pg = ctx.new_page(); pg.goto(BASE + "xray.html?mode=xray&layer=all&markers=1"); pg.wait_for_function("window.__xrayReady===true && window.xray.ready()", timeout=90000); time.sleep(1.5); settle(pg)
    pg.locator("#stage").screenshot(path=os.path.join(OUT, "frame1-overview.png"))
    cl = pg.evaluate("xray.clusters()"); fill = pg.evaluate("xray.fill()"); json.dump(cl, open(os.path.join(OUT, "clusters.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    # frame two: the boiler close-up, water layer lit
    pg.evaluate("xray.jump({mode:'xray',layer:'w'})"); pg.evaluate("xray.closeup('boiler',{d:4.0,az:-138,el:38,fov:42,ndcY:0.12,aim:[22,-55,-30]})"); time.sleep(0.8); settle(pg)
    pg.locator("#stage").screenshot(path=os.path.join(OUT, "frame2-part.png"))
    print("fill", json.dumps(fill)); print("clusters", json.dumps([(c["room"], c["x"], c["y"], c["count"], c["state"]) for c in cl], ensure_ascii=False)); pg.close()
    # the flat drawing of the same plan
    pg = ctx.new_page(); pg.goto(BASE + "plan4r.html"); pg.wait_for_function("window.__ready===true", timeout=30000); time.sleep(1.0)
    pg.locator("#plan").screenshot(path=os.path.join(OUT, "plan-4r.png")); json.dump(pg.evaluate("window.__plan"), open(os.path.join(OUT, "plan-4r.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    b.close()
