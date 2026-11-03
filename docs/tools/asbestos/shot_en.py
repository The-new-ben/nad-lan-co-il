import functools, http.server, os, threading
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
H.log_message = lambda *a, **k: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 47934), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
OUT = os.path.join(ROOT, "docs", "qa", "asbestos")
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, locale="en-US", is_mobile=True, has_touch=True)
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.goto("http://127.0.0.1:47934/docs/tools/asbestos/harness-en.html", wait_until="load"); pg.wait_for_timeout(8000)
    he = pg.evaluate("""() => [...document.querySelectorAll('.nli')].map(s => (s.innerText.match(/[\u0590-\u05FF][\u0590-\u05FF\s]*/g) || []).slice(0, 6).join(' / '))""")
    pg.locator(".asbh").first.screenshot(path=os.path.join(OUT, "harness-en-hero-m.png"))
    pg.locator('[data-nli="asbcheck"]').screenshot(path=os.path.join(OUT, "harness-en-check-m.png"))
    print("hebrew inside the English tools:", he, "| scrollWidth", pg.evaluate("document.documentElement.scrollWidth"), "| errors", errs[:3])
    b.close()
srv.shutdown()
