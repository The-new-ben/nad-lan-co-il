# -*- coding: utf-8 -*-
"""The poster frame for the site page: one frame of the 16:9 film drawn by film.html WITHOUT the subtitle box, scaled to
1280x720, JPEG under 200 KB.

  python poster.py [--variant <name>] [--at <seconds>]

The moment comes from the variant's "poster" entry: {"scene": <scene id>, "group": <voice group>, "at": "start"|"end",
"offset": <s>} (main-he: the end of scene s12's third line minus 0.2 s = 116.43 s), or from --at. Out: the variant's
outputs.poster.
"""
import io, json, os, shutil, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import variant as VAR
from render import Server, open_page, H as BUILD

VA = VAR.load(); PA = VAR.Paths(VA)
TL = json.load(open(PA.tl_web, encoding="utf-8"))
if "--at" in sys.argv:
    t = float(VAR.arg("--at"))
else:
    P = VA["poster"]; b = [x for x in TL["voice"] if x["scene"] == P["scene"] and x["k"] == P.get("group", 1)][0]
    t = round((b["b"] if P.get("at", "end") == "end" else b["a"]) + P.get("offset", 0), 2)
shutil.copyfile(os.path.join(BUILD, "film.html"), os.path.join(VAR.WEB, "film.html"))
srv = Server(VAR.WEB)
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, pg = open_page(p, srv.base, "h", PA.tl_rel)
        pg.evaluate("t => window.render(t)", t); pg.evaluate("window.subsOff()"); pg.wait_for_timeout(300)
        png = pg.screenshot(type="png"); b.close()
finally:
    srv.stop()
im = Image.open(io.BytesIO(png)).convert("RGB").resize((1280, 720), Image.LANCZOS)
for q in (90, 86, 82, 78, 74, 70):
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
    if buf.tell() < 200 * 1024:
        break
out = PA.files["poster"]; os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "wb").write(buf.getvalue())
print(out, f"{t} s", f"q{q}", f"{buf.tell() / 1024:.0f} KB")
