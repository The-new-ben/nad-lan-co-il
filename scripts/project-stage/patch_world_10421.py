# -*- coding: utf-8 -*-
"""v104.21 (2.10.2026, the V2 loop turn 5, V4 step 2; HAD-380): the basket can step inside the example apartment.
Once the world is ready and has an example apartment, window.__nlInsideGo() takes the visitor to it (its tower, floor and side)
and opens its 360 straight away, where the design styles are (example.js v104.21); basket.js's "להיכנס לדירה ולבחור סגנון"
calls it on a world page (the fleet's stages keep their own .nlat__go). openExampleApt passes a start ('pano') to the album.
  python patch_world_10421.py; and the basket: patch_basket_392.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.js")
BK = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "basket", "basket.js")
s = open(JS, encoding="utf-8").read()
if "v104.21" in s:
    raise SystemExit("already patched")


def sub(text, old, new, name, n=1):
    c = text.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    return text.replace(old, new)


s = sub(s, "  function openExampleApt(id, opener) {", "  function openExampleApt(id, opener, start) { // v104.21: start 'pano' opens the 360 at once", "open sig")
s = sub(s, """        wa: o.wa ? waHref(`${XW.chip} · ${T.towerN(S.tower)}`) : null, opener,""",
        """        wa: o.wa ? waHref(`${XW.chip} · ${T.towerN(S.tower)}`) : null, opener, start,""", "open start")
s = sub(s, """    readyCbs.forEach((f) => f(api));
  }""", """    readyCbs.forEach((f) => f(api));
    // v104.21 (V4): the basket's way inside: to the example apartment's tower, floor and side, and straight into its 360
    if (exList().length) window.__nlInsideGo = () => { const x = exList()[0]; goExample(x.id); openExampleApt(x.id, null, 'pano'); };
  }""", "inside go")
open(JS, "w", encoding="utf-8", newline="\n").write(s)

b = open(BK, encoding="utf-8").read()
if "1.72.392" in b:
    raise SystemExit("basket already patched")
b = sub(b, """  function goInside() {
    close();
    const b = document.querySelector('.nlat__go');
    if (b) b.click();
  }""", """  // 1.72.392: a world page (the shared 3D world) offers its own way inside (window.__nlInsideGo: the example apartment's 360)
  const insideOk = () => !!document.querySelector('.nlat__go') || typeof window.__nlInsideGo === 'function';
  function goInside() {
    close();
    const b = document.querySelector('.nlat__go');
    if (b) b.click(); else if (typeof window.__nlInsideGo === 'function') window.__nlInsideGo();
  }""", "basket goInside")
b = sub(b, "    const has = !!document.querySelector('.nlat__go');", "    const has = insideOk();", "basket has")
open(BK, "w", encoding="utf-8", newline="\n").write(b)
print("world.js (v104.21) + basket.js (1.72.392) patched")
