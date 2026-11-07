# -*- coding: utf-8 -*-
"""The poster frame for the site page: one frame of the 16:9 film drawn by film.html WITHOUT the subtitle box, scaled to
1280x720, JPEG under 200 KB.

  python poster.py <scratch>/film3 <seconds> <out.jpg>
"""
import io, os, shutil, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import Server, open_page, H as BUILD

S, t, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
shutil.copyfile(os.path.join(BUILD, "film.html"), os.path.join(S, "web", "film.html"))
srv = Server(os.path.join(S, "web"))
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, pg = open_page(p, srv.base, "h")
        pg.evaluate("t => window.render(t)", t); pg.evaluate("window.subsOff()"); pg.wait_for_timeout(300)
        png = pg.screenshot(type="png"); b.close()
finally:
    srv.stop()
im = Image.open(io.BytesIO(png)).convert("RGB").resize((1280, 720), Image.LANCZOS)
for q in (90, 86, 82, 78, 74, 70):
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
    if buf.tell() < 200 * 1024:
        break
open(out, "wb").write(buf.getvalue())
print(out, f"{t} s", f"q{q}", f"{buf.tell() / 1024:.0f} KB")
