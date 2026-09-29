# -*- coding: utf-8 -*-
"""Screenshots of kikar-world.html (LOCAL ONLY). Chrome via Playwright, desktop 1440x900 and phone 390x844.

  python docs/research/2026-09-30-kikar-hamedina/prototype/shoot.py            (all views, both sizes)
  python docs/research/2026-09-30-kikar-hamedina/prototype/shoot.py aerial     (one view)
"""
import io, os, sys, time, pathlib
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parent
PAGE = (HERE / "kikar-world.html").as_uri()
VIEWS = [
    ("aerial", "a-aerial-three-quarter"),
    ("overview", "a2-overview-25-places"),
    ("street", "b-street-level-ring"),
    ("c30west", "c1-window-tower-C-floor30-west"),
    ("a30north", "c2-window-tower-A-floor30-north"),
    ("shade", "d-sun-shade-21dec-1300"),
    ("twist", "e-towers-twist-closeup"),
]
SIZES = [("desktop", 1440, 900, 1), ("mobile", 390, 844, 2)]
only = set(a for a in sys.argv[1:] if not a.startswith("--"))
extra = next((a[2:] for a in sys.argv[1:] if a.startswith("--q=")), "")

def sun_study(browser):
    """six tiles (21 June / 21 December x 09:00 / 13:00 / 17:00) from one camera, composed into one 1440x900 sheet"""
    from PIL import Image
    ctx = browser.new_context(viewport={"width": 720, "height": 450}, device_scale_factor=1, locale="he-IL")
    page = ctx.new_page()
    tiles = []
    for key in ("jun09", "jun13", "jun17", "dec09", "dec13", "dec17"):
        page.goto(PAGE + "?view=study&clean=1&sun=" + key, wait_until="load")
        page.wait_for_function("window.__ready === true", timeout=120000)
        page.wait_for_timeout(400)
        f = HERE / ("_tile-%s.png" % key)
        page.screenshot(path=str(f))
        tiles.append(f)
    ctx.close()
    sheet = Image.new("RGB", (1440, 1350), (250, 247, 241))
    for i, f in enumerate(tiles):
        im = Image.open(f)
        june, row = i < 3, i % 3
        sheet.paste(im, (720 if june else 0, row * 450))
        f.unlink()
    # order: rows = 09:00 / 13:00 / 17:00, columns = June (right, RTL) / December (left)
    out = HERE / "kikar-d2-sun-study-6-times-desktop.png"
    sheet.save(out)
    print("sun study", out.name)


with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True,
                                args=["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-gpu-rasterization"])
    if "--study" in sys.argv:
        sun_study(browser)
        browser.close()
        sys.exit(0)
    for size, w, h, dsf in SIZES:
        if "--desktop" in sys.argv and size != "desktop":
            continue
        if "--mobile" in sys.argv and size != "mobile":
            continue
        ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=dsf, locale="he-IL")
        page = ctx.new_page()
        logs = []
        page.on("console", lambda m: logs.append("%s: %s" % (m.type, m.text)))
        page.on("pageerror", lambda e: logs.append("pageerror: %s" % e))
        for view, fname in VIEWS:
            if only and view not in only:
                continue
            url = PAGE + "?view=" + view + ("&" + extra if extra else "")
            t0 = time.time()
            page.goto(url, wait_until="load")
            try:
                page.wait_for_function("window.__ready === true", timeout=120000)
            except Exception as e:
                print("NOT READY", view, size, e)
                print("\n".join(logs[-20:]))
                continue
            page.wait_for_timeout(600)
            out = HERE / ("kikar-%s-%s.png" % (fname, size))
            page.screenshot(path=str(out))
            gl = page.evaluate("""() => { const c = document.createElement('canvas').getContext('webgl2');
                const e = c && c.getExtension('WEBGL_debug_renderer_info'); return e ? c.getParameter(e.UNMASKED_RENDERER_WEBGL) : 'n/a'; }""")
            print("%-9s %-8s %5.1fs  %s  [%s]" % (view, size, time.time() - t0, out.name, gl))
        errs = [l for l in logs if l.startswith(("error", "pageerror"))]
        if errs:
            print("console errors:", "\n".join(errs[:10]))
        ctx.close()
    browser.close()
