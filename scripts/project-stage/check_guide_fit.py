# -*- coding: utf-8 -*-
"""HAD-743 (17.11.2026, Ben: "the face is cut", "an old Windows scrollbar inside her window"): opens the deals guide in a real
Chrome at 375x812, 1280x720, 1366x768, 1440x900 and 1920x1080 and measures, in three states of her window (questions, an answer,
the details form), whether the window needs an inner scroll and whether a scrollbar is drawn; saves a close-up of the face and
each window. python scripts/project-stage/check_guide_fit.py <url> <out-folder>"""
import os, sys, json
from playwright.sync_api import sync_playwright
URL, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
VPS = [("375", 375, 812, True), ("1280", 1280, 720, False), ("1366", 1366, 768, False), ("1440", 1440, 900, False), ("1920", 1920, 1080, False)]
MEASURE = """() => { const p = document.querySelector('.nldg-pan'); const r = p.getBoundingClientRect();
  return { h: Math.round(r.height), top: Math.round(r.top), scrollH: p.scrollHeight, clientH: p.clientHeight, inner_scroll: p.scrollHeight > p.clientHeight + 1,
           bar_px: p.offsetWidth - p.clientWidth - (parseFloat(getComputedStyle(p).borderLeftWidth) || 0) - (parseFloat(getComputedStyle(p).borderRightWidth) || 0), vh: innerHeight }; }"""
res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome", headless=True)
    for tag, w, h, mob in VPS:
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2, is_mobile=mob, has_touch=mob, locale="he-IL")
        pg = ctx.new_page(); pg.goto(URL, wait_until="domcontentloaded", timeout=90000)
        pg.add_style_tag(content=".nldg *{transition:none!important}")
        pg.wait_for_selector(".nldg.is-in .nldg-face", timeout=30000); pg.wait_for_timeout(800)
        fb = pg.locator(".nldg-face").bounding_box()
        pg.screenshot(path=os.path.join(OUT, tag + "-face.png"), clip={"x": max(0, fb["x"] - 16), "y": max(0, fb["y"] - 16), "width": fb["width"] + 32, "height": fb["height"] + 32})
        r = {"face": {k: round(v) for k, v in fb.items()}}
        pg.evaluate("() => { const b = document.querySelector('.nldg-bx'); if (b) b.click(); }")
        pg.click(".nldg-face"); pg.wait_for_selector(".nldg-pan.is-in", timeout=10000); pg.wait_for_timeout(1500)
        r["questions"] = pg.evaluate(MEASURE); pg.screenshot(path=os.path.join(OUT, tag + "-1-questions.png"))
        pg.locator(".nldg-chip", has_text="20/80").first.click(); pg.wait_for_timeout(2500)
        r["answer"] = pg.evaluate(MEASURE); pg.screenshot(path=os.path.join(OUT, tag + "-2-answer.png"))
        pg.click(".nldg-tolead"); pg.wait_for_selector("form.nldg-lead:not([hidden])"); pg.wait_for_timeout(600)
        r["details"] = pg.evaluate(MEASURE); pg.screenshot(path=os.path.join(OUT, tag + "-3-details.png"))
        a11y = pg.evaluate("() => { const a = document.getElementById('nla11y'); const f = document.querySelector('.nldg-pf'); if (!a || !f) return null; const x = a.getBoundingClientRect(), y = f.getBoundingClientRect(); return !(x.right < y.left || x.left > y.right || x.bottom < y.top || x.top > y.bottom); }")
        r["a11y_covers_footer"] = a11y
        res[tag] = r
        ctx.close()
    b.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
