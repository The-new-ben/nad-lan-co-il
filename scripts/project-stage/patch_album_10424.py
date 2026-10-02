# -*- coding: utf-8 -*-
"""v104.24 (2.10.2026, the V2 loop turn 8): the album's tile grid never leaves one tile alone on a row. With the spa and the car park
the album has 9 tiles (4 of the apartment + 5 rooms): 4 columns left the car park alone on a third row; 3 columns give three full
rows of slightly larger tiles. The rule: 3 columns when 4 would leave a single orphan and 3 would not.
  python patch_album_10424.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
W = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "assets", "project-stage", "world")
JS, CSS = os.path.join(W, "example.js"), os.path.join(W, "example.css")
js, css = open(JS, encoding="utf-8").read(), open(CSS, encoding="utf-8").read()
if "nlex__strip--3" in js or "nlex__strip--3" in css:
    raise SystemExit("already patched")
old = """        <div class="nlex__strip" role="group" aria-label="${esc(T.gallery)}">${tiles}</div>"""
if js.count(old) != 1:
    raise SystemExit("strip anchor x%d" % js.count(old))
js = js.replace(old, """        <div class="nlex__strip${stripCols(tiles) === 3 ? ' nlex__strip--3' : ''}" role="group" aria-label="${esc(T.gallery)}">${tiles}</div>""")
old2 = """  function build() {
    const size = ex.size || {};"""
if js.count(old2) != 1:
    raise SystemExit("build anchor x%d" % js.count(old2))
js = js.replace(old2, """  // v104.24: never one tile alone on a row (9 tiles: 3 full rows of 3, not 4 + 4 + 1)
  function stripCols(html) {
    const n = (html.match(/class="nlex__tile[ "]/g) || []).length;
    return n > 4 && n % 4 === 1 && n % 3 !== 1 ? 3 : 4;
  }

  function build() {
    const size = ex.size || {};""")
css = css.rstrip("\n") + "\n/* v104.24: the album never leaves one tile alone on a row (example.js stripCols) */\n.nlex__strip.nlex__strip--3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }\n"
open(JS, "w", encoding="utf-8", newline="\n").write(js)
open(CSS, "w", encoding="utf-8", newline="\n").write(css)
print("example.js + example.css patched (v104.24 strip)")
