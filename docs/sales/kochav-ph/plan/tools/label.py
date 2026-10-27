# -*- coding: utf-8 -*-
"""Stamp the mandatory caption "הדמיה על פי תוכנית האדריכל" on publish-ready copies (Edge renders the Hebrew with the Assistant font).
    python label.py  -> renders/labelled/*.jpg"""
import os, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOBS = ["dollhouse-iso-photoreal.png", "dollhouse-iso.png", "topdown.png", "terrace.png", "terrace-photoreal.png"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    for n in JOBS:
        src = os.path.join(H, "renders", n); w, h = Image.open(src).size
        fs = max(18, round(w / 70))
        html = ('<html><head><link href="https://fonts.googleapis.com/css2?family=Assistant:wght@600&display=swap" rel="stylesheet"></head>'
                '<body style="margin:0"><div style="position:relative;width:%dpx;height:%dpx"><img src="%s" style="width:100%%;height:100%%;display:block">'
                '<div dir="rtl" style="position:absolute;right:%dpx;bottom:%dpx;padding:%dpx %dpx;border-radius:999px;background:rgba(255,255,255,.9);'
                'border:1px solid #E3E8EC;color:#1F4B5C;font:600 %dpx Assistant,sans-serif">הדמיה על פי תוכנית האדריכל</div></div></body></html>'
                % (w, h, pathlib.Path(src).as_uri(), fs, fs, fs * 0.35, fs * 0.8, fs))
        tmp = os.path.join(H, "renders", "labelled", "_tmp.html"); open(tmp, "w", encoding="utf-8").write(html)
        pg = b.new_page(viewport={"width": w, "height": h}); pg.goto(pathlib.Path(tmp).as_uri()); pg.wait_for_timeout(900)
        out = os.path.join(H, "renders", "labelled", n.replace(".png", ".jpg"))
        pg.screenshot(path=out, type="jpeg", quality=90); pg.close(); print("saved", out)
    os.remove(tmp)
    b.close()
