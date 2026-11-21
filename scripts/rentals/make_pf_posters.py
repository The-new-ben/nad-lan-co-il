# -*- coding: utf-8 -*-
"""The still globe of the rentals opening (HAD-795): the first paint of the stage before the live map arrives.
Photographs the real stage's world view (map and marks only, no chrome) from the lab pages, he and en, desktop and phone.
The map key is read at run time from the public page and never written. Chrome with a real GPU.
Usage: python scripts/rentals/make_pf_posters.py   (server at the repo root on 47921; run build_pf_lab.php first)"""
import re, subprocess, pathlib, io
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "plugins/nadlan-config/assets/rentals/portfolio/img"
html = subprocess.run(["curl", "-s", "https://nad-lan.co.il/my-rentals/"], capture_output=True).stdout.decode("utf-8", "replace")
KEY = re.search(r"pk\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+", html).group(0)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--enable-gpu", "--use-angle=d3d11", "--ignore-gpu-blocklist", "--hide-scrollbars"])
    for lang in ("he", "en"):
        for name, w, h, dpr in (("desk", 1280, 900, 1), ("phone", 390, 664, 2)):
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, has_touch=w < 700)
            pg = ctx.new_page()
            pg.goto("http://127.0.0.1:47921/docs/design-lab/rentals-portfolio/stage-%s.html?t=%s" % (lang, KEY), wait_until="domcontentloaded")
            pg.wait_for_selector("#nlpf.is-map", timeout=60000)
            pg.wait_for_function("() => window.__nlpfMap && !window.__nlpfMap.isMoving() && window.__nlpfMap.areTilesLoaded()", timeout=30000)
            pg.wait_for_timeout(2500)
            pg.add_style_tag(content="#nlpf .nlpf-top, #nlpf .nlpf-say, #nlpf .nlpf-tray, #nlpf .nlpf-poster { visibility: hidden !important; } #nlpf .is-care > .nlpf-ring { animation: none !important; opacity: .55 !important; transform: scale(1.5) !important; } #nlpf .is-care > .nlpf-ring--2 { display: none !important; }")
            pg.wait_for_timeout(400)
            png = pg.locator("#nlpf").screenshot()
            im = Image.open(io.BytesIO(png)).convert("RGB")
            f = OUT / ("poster-%s-%s.webp" % (lang, name))
            im.save(f, "WEBP", quality=70, method=6)
            print(f.name, im.size, f.stat().st_size)
            ctx.close()
    b.close()
