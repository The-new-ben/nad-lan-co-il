import os, sys, http.server, threading, functools
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
class Q(H.func):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 47932), functools.partial(Q, directory=ROOT)); threading.Thread(target=srv.serve_forever, daemon=True).start()
OUT = os.path.join(ROOT, "docs", "tools", "_harness"); os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for w, h, tag in ((1440, 900, "d"), (390, 844, "m")):
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2 if tag == "m" else 1)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        pg.goto("http://127.0.0.1:47932/tools/instruments/harness_greece.html", wait_until="networkidle"); pg.wait_for_timeout(1200)
        print(tag, "errors:", errs[:3], "| answers:", pg.locator(".nli__fig").all_inner_texts(), "| scrollW", pg.evaluate("document.documentElement.scrollWidth"))
        roots = pg.query_selector_all("[data-nli]")
        for i, el in enumerate(roots): el.screenshot(path=os.path.join(OUT, f"greece-{tag}-{i}.png"))
        if tag == "d":
            for k in ("after2027", "mortgage", "glyfada-new"):
                pg.click(f"[data-nli=grbuy] .nli__pre button[data-k={k}]"); pg.wait_for_timeout(300)
                print("  grbuy", k, pg.locator("[data-nli=grbuy] .nli__fig").inner_text(), "|", pg.locator("[data-nli=grbuy] .nli__asub").inner_text())
            for k in ("athens800", "crete400", "two400", "airbnb", "conv250", "halkidiki400"):
                pg.click(f"[data-nli=grgv] .nli__pre button[data-k={k}]"); pg.wait_for_timeout(300)
                print("  grgv", k, pg.locator("[data-nli=grgv] .nli__fig").inner_text())
            for k in ("athens", "piraeus", "glyfada", "thess"):
                pg.click(f"[data-nli=gryield] .nli__pre button[data-k={k}]"); pg.wait_for_timeout(300)
                print("  gryield", k, pg.locator("[data-nli=gryield] .nli__fig").inner_text(), "|", pg.locator("[data-nli=gryield] .nli__asub").inner_text())
            pg.fill("[data-nli=grbuy] input[id$='-price']", "200000"); pg.wait_for_timeout(300)
            print("  typed price -> pressed presets:", pg.locator("[data-nli=grbuy] .nli__pre button[aria-pressed=true]").count(), pg.locator("[data-nli=grbuy] .nli__fig").inner_text())
    b.close()
srv.shutdown()
