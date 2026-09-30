# -*- coding: utf-8 -*-
"""The world's poster (Kikar Hamedina, P5, LOCAL): a pre-rendered aerial frame that paints at once, before any 3D loads.

    python scripts/project-stage/poster_world_hamedina.py

Serves the repo root on 127.0.0.1:8766, opens docs/research/2026-09-30-kikar-hamedina/world-test.html in Chrome
(Playwright, the local GPU) with no chrome and no labels, and writes
    plugins/nadlan-config/assets/project-stage/hamedina/poster-1600.webp / .jpg   1600x1000 (desktop, 16:10)
    plugins/nadlan-config/assets/project-stage/hamedina/poster-800.webp / .jpg    800x1000  (phone, 4:5)
The same aerial pose the world opens with (21 September, 10:00), so the poster and the first 3D frame match.
Use: mountWorld(el, { poster: { src: '.../poster-1600.jpg', srcset: '.../poster-800.webp 800w, .../poster-1600.webp 1600w',
sizes: '100vw' } }).
"""
import functools, http.server, io, pathlib, socketserver, sys, threading

from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = pathlib.Path(__file__).resolve().parents[2]
OUT = REPO / "plugins/nadlan-config/assets/project-stage/hamedina"
PORT = 8766
PAGE = "http://127.0.0.1:%d/docs/research/2026-09-30-kikar-hamedina/world-test.html?mode=aerial&season=9&hour=10&clean=1&labels=0" % PORT


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main():
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", PORT), functools.partial(Quiet, directory=str(REPO)))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=d3d11", "--ignore-gpu-blocklist"])
        for name, w, h in (("1600", 1600, 1000), ("800", 800, 1000)):
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, locale="he-IL")
            page = ctx.new_page()
            page.goto(PAGE, wait_until="load")
            page.wait_for_function("window.__ready === true", timeout=180000)
            page.wait_for_timeout(800)
            png = OUT / ("_poster-%s.png" % name)
            page.screenshot(path=str(png))
            ctx.close()
            im = Image.open(png).convert("RGB")
            im.save(OUT / ("poster-%s.webp" % name), "WEBP", quality=80, method=6)
            im.save(OUT / ("poster-%s.jpg" % name), "JPEG", quality=82, optimize=True, progressive=True)
            png.unlink()
            for ext in ("webp", "jpg"):
                f = OUT / ("poster-%s.%s" % (name, ext))
                print(f.name, f.stat().st_size, "bytes")
        browser.close()
    httpd.shutdown()


main()
