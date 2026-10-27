# -*- coding: utf-8 -*-
"""Screenshot a local SVG/HTML file with headless Chromium (Playwright).  python shot.py <file> <out.png> [width] [height] [scale] [--full]"""
import sys, os, pathlib
from playwright.sync_api import sync_playwright
src, out = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 1400; h = int(sys.argv[4]) if len(sys.argv) > 4 else 1400
sc = float(sys.argv[5]) if len(sys.argv) > 5 else 1
full = "--full" in sys.argv
url = pathlib.Path(os.path.abspath(src)).as_uri()
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=sc)
    if src.endswith(".svg"):
        pg.set_content('<html><body style="margin:0;background:#fff"><img src="%s" style="width:%dpx;height:%dpx;display:block"></body></html>' % (url, w, h))
        # an <img> cannot fetch fonts: inline the SVG instead so the Google fonts load
        svg = open(src, encoding="utf-8").read()
        pg.set_content('<html><head><link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Noto+Serif+Hebrew:wght@500;600&display=swap" rel="stylesheet"></head><body style="margin:0;background:#fff"><div style="width:%dpx;height:%dpx">%s</div></body></html>' % (w, h, svg.replace('width="', 'data-w="', 1).replace('height="', 'data-h="', 1).replace("<svg ", '<svg style="width:100%;height:100%" ', 1)))
    else:
        pg.goto(url)
    pg.wait_for_timeout(1500)
    try:
        pg.evaluate("document.fonts.ready")
    except Exception:
        pass
    pg.wait_for_timeout(500)
    pg.screenshot(path=out, full_page=full)
    b.close()
print("saved", out)
