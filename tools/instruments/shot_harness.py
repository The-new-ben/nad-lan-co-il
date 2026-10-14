import os, sys, time, http.server, threading, functools
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 47931), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
OUT = os.path.join(ROOT, "docs", "tools", "_harness"); os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for w, h, tag in ((1440, 900, "d"), (390, 844, "m")):
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2 if tag == "m" else 1)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        pg.goto("http://127.0.0.1:47931/tools/instruments/harness.html", wait_until="networkidle"); pg.wait_for_timeout(1500)
        for i, el in enumerate(pg.query_selector_all("[data-nli]")):
            el.screenshot(path=os.path.join(OUT, f"{tag}-{i}.png"))
        print(tag, "errors:", errs[:3], "| answers:", pg.locator(".nli__fig").all_inner_texts())
    b.close()
srv.shutdown()
