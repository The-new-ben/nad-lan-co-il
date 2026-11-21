# -*- coding: utf-8 -*-
"""The home parts as pictures on the live sample page, as a visitor (HAD-795, 1.72.737): every part tile on the day screen, in the
apartment sheet and in "add an appliance" is a loaded picture of the opening's family, with its state mark; no drawn part glyph is left.
Usage: python scripts/rentals/live_parts.py <out dir> [base url]   (default base: the live sample page)"""
import sys, json
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]
B = sys.argv[2] if len(sys.argv) > 2 else "https://nad-lan.co.il/my-rentals/?sample=1"
LIVE = B.startswith("https://")
res = []
def check(name, ok, info=""):
    res.append({"check": name, "ok": bool(ok), "info": str(info)[:300]}); print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:260] if not ok else ""))
PICS = """() => { const q = s => [...document.querySelectorAll(s)]; const ok = i => i.complete && i.naturalWidth > 0;
  const t = q('#nt2 .nt2-tb .np2-part[data-part]'); const sh = document.querySelector('#nt2 .nt2-sheet');
  return { tiles: t.length, tilePics: t.filter(b => { const i = b.querySelector('img.np2-pic'); return i && ok(i); }).length, tileSvg: t.filter(b => b.querySelector('svg')).length,
    marks: t.map(b => (b.querySelector('.np2-bd') || {}).className || ''), sizes: t.map(b => Math.round(b.getBoundingClientRect().width)),
    sheetPics: sh ? q('#nt2 .nt2-sheet img.np2-pic').length : 0, sheetOk: sh ? q('#nt2 .nt2-sheet img.np2-pic').filter(ok).length : 0, kinds: sh ? q('#nt2 .nt2-sheet .nt2-kind').length : 0, kindSvg: sh ? q('#nt2 .nt2-sheet .nt2-kind svg').length : 0,
    font: getComputedStyle(document.querySelector('.nt2-head h1')).fontFamily.split(',')[0], radius: getComputedStyle(document.querySelector('.nt2-tb')).borderRadius, ov: document.scrollingElement.scrollWidth - innerWidth }; }"""
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for lang in ("he", "en"):
        for w, h, tag in ((390, 844, "phone"), (1280, 800, "desk")):
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if w < 900 else 1, has_touch=w < 900, locale="he-IL")
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
            pg.goto(B + ("&" if "?" in B else "?") + ("lang=en&" if lang == "en" else ("" if LIVE else "lang=he&")) + "u=21#/today/21", wait_until="domcontentloaded" if LIVE else "networkidle")
            pg.wait_for_function("window.NLRMTour && window.NLRM && NLRM.store && NLRM.store.d", timeout=40000)
            pg.wait_for_timeout(2500)
            m = pg.evaluate(PICS); T = "%s %s " % (lang, tag)
            check(T + "day screen: %d part tiles, each a loaded picture, none drawn, each with a state mark (one fault, the rest fine)" % m["tiles"],
                  m["tiles"] >= 4 and m["tilePics"] == m["tiles"] and m["tileSvg"] == 0 and sum("fault" in x for x in m["marks"]) == 1 and sum("--ok" in x for x in m["marks"]) == m["tiles"] - 1 and min(m["sizes"]) >= 44, m)
            check(T + "day screen in the opening's family: face %s, round sheet %s, no sideways scroll" % (m["font"], m["radius"]), "Assistant" in m["font"] and m["radius"] == "18px" and m["ov"] <= 0, m)
            if lang == "he": pg.screenshot(path=OUT + "/parts-%s-1-day.png" % tag)
            pg.click("#nt2 [data-act='add-part']"); pg.wait_for_timeout(1500)
            m = pg.evaluate(PICS)
            check(T + "add an appliance: %d kinds, each with a loaded picture, none drawn" % m["kinds"], m["kinds"] == 11 and m["sheetPics"] == 11 and m["sheetOk"] == 11 and m["kindSvg"] == 0, m)
            if lang == "he" and tag == "phone": pg.screenshot(path=OUT + "/parts-phone-2-add.png")
            pg.evaluate("document.querySelector('#nt2 .nt2-sheet [data-close]').click()"); pg.wait_for_timeout(600)
            pg.click("#nt2 .nt2-tb [data-part]"); pg.wait_for_timeout(1500)
            m = pg.evaluate(PICS)
            check(T + "the apartment sheet: its parts are loaded pictures", m["sheetPics"] >= 4 and m["sheetOk"] == m["sheetPics"], m)
            if lang == "he" and tag == "phone": pg.screenshot(path=OUT + "/parts-phone-3-sheet.png")
            check(T + "no script error", not errs, errs[:2])
            ctx.close()
    b.close()
json.dump(res, open(OUT + "/results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("RESULT %d/%d checks passed" % (sum(r["ok"] for r in res), len(res)))
