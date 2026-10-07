# -*- coding: utf-8 -*-
"""Screenshots of the local preview pages (headless Chrome, WebGL through SwiftShader) into docs/qa/had-460/i18n-components/,
plus DOM checks: map state, pins, card inside the frame, overflow, console and page errors. Report: report.json there."""
import json
import os
import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SHOTS = pathlib.Path(r"C:\Users\777\nad-lan\nad-lan-co-il\docs\qa\had-460\i18n-components")
SHOTS.mkdir(parents=True, exist_ok=True)
ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]
LANGS = sys.argv[1].split(",") if len(sys.argv) > 1 else ["en", "fr", "ru", "ar", "he"]
SIZES = [("1440", {"width": 1440, "height": 900}, False), ("390", {"width": 390, "height": 844}, True)]
REN = {"he": "זלוציסטי 4", "en": "Zlotisti 4", "fr": "4 rue Zlotisti", "ru": "Злоцисти 4", "ar": "زلوتسيستي 4"}

INFO = """() => { const r = document.querySelector('.nlam'), m = r.__nlamMap, f = r.querySelector('.nlam__frame');
  let ren = -1; try { ren = m && m.getLayer('nlam-ren') ? m.queryRenderedFeatures({layers: ['nlam-ren']}).length : -1 } catch (e) {}
  const pick = s => { const e = r.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(), fb = f.getBoundingClientRect();
    return {l: Math.round(b.left - fb.left), r: Math.round(fb.right - b.right), t: Math.round(b.top - fb.top), b: Math.round(fb.bottom - b.bottom), w: Math.round(b.width)}; };
  return { state: r.getAttribute('data-state'), dir: r.getAttribute('dir'), lang: r.getAttribute('lang'),
    pins: r.querySelectorAll('.nlam__pin').length, renewal_rendered: ren, reset: pick('.nlam__reset'), key: pick('.nlam__key'),
    nav: pick('.maplibregl-ctrl-group'), attrib: pick('.maplibregl-ctrl-attrib'),
    scrollW: document.documentElement.scrollWidth, innerW: innerWidth }; }"""
CARD = """() => { const r = document.querySelector('.nlam'), c = r.querySelector('.nlam__card'), f = r.querySelector('.nlam__frame'); if (c.hidden) return {open: false};
  const b = c.getBoundingClientRect(), fb = f.getBoundingClientRect(), x = c.querySelector('.nlam__x').getBoundingClientRect();
  const k = c.querySelector('.nlam__ck'), kb = k ? k.getBoundingClientRect() : null, t = c.querySelector('.nlam__ct').getBoundingClientRect();
  const over = (a, o) => a && !(a.right <= o.left || a.left >= o.right || a.bottom <= o.top || a.top >= o.bottom);
  return {open: true, text: c.innerText.replace(/\\s+/g, ' ').trim(), side: (b.left - fb.left) < (fb.right - b.right) ? 'left' : 'right',
    inside: b.left >= fb.left - 1 && b.right <= fb.right + 1 && b.top >= fb.top - 1 && b.bottom <= fb.bottom + 1,
    x_side: (x.left - b.left) < (b.right - x.right) ? 'left' : 'right', x_overlaps_kicker: over(kb, x), x_overlaps_title: over(t, x),
    scrollW: document.documentElement.scrollWidth, innerW: innerWidth}; }"""
REN_PT = """(a) => { const r = document.querySelector('.nlam'), m = r.__nlamMap, d = JSON.parse(r.getAttribute('data-cfg'));
  const x = d.rn.find(o => o.a === a), p = m.project([x.x, x.y]), b = m.getCanvas().getBoundingClientRect();
  return {x: b.left + p.x, y: b.top + p.y}; }"""
IDLE = """() => new Promise(res => { const m = document.querySelector('.nlam').__nlamMap; if (!m) return res('no map');
  if (m.loaded() && m.areTilesLoaded()) return res('idle'); m.once('idle', () => res('idle')); setTimeout(() => res('timeout'), 30000); })"""
LABELS = """() => { const m = document.querySelector('.nlam').__nlamMap; const f = m.queryRenderedFeatures().filter(x => x.layer.type === 'symbol' && x.layer.layout && x.layer.layout['text-field']);
  const names = []; f.forEach(x => { const n = x.properties['name:' + document.querySelector('.nlam').lang] || x.properties['name:en'] || x.properties.name; if (n && names.indexOf(n) < 0) names.push(n) });
  return {count: names.length, sample: names.slice(0, 12)}; }"""


def run(pw, lang, tag, vp, mobile, rep):
    b = pw.chromium.launch(channel="chrome", headless=True, args=ARGS)
    ctx = b.new_context(viewport=vp, device_scale_factor=1, is_mobile=mobile, has_touch=mobile, locale={"he": "he-IL", "ar": "ar"}.get(lang, lang))
    page = ctx.new_page()
    errs, cons = [], []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.on("console", lambda m: m.type == "error" and cons.append(m.text))
    page.goto((HERE / (lang + ".html")).as_uri(), wait_until="load")
    page.wait_for_timeout(800)
    r = {"lang": lang, "size": tag}
    # PriceGuide: the section as served, then the premium mode (the comparison chart's longest range)
    pg = page.locator(".nlpg")
    pg.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    pg.screenshot(path=str(SHOTS / ("%s-%s-price.png" % (lang, tag))))
    page.locator('.nlpg input[value="premium"]').click()
    page.wait_for_timeout(300)
    page.locator(".nlpg__calc").screenshot(path=str(SHOTS / ("%s-%s-price-premium.png" % (lang, tag))))
    r["price"] = page.evaluate("""() => { const q = s => (document.querySelector(s) || {}).textContent; return {big: q('[data-pg="p"]'), pm: q('[data-pg="pm"]'),
        tx: q('[data-pg="tx"]'), tt: q('[data-pg="tt"]'), wa: decodeURIComponent((document.querySelector('[data-pg="wa"]') || {href: ''}).href.split('text=')[1] || ''),
        scrollW: document.documentElement.scrollWidth, innerW: innerWidth}; }""")
    # AreaMap
    page.locator(".nlam__frame").scroll_into_view_if_needed()
    page.wait_for_function("() => ['ready','fail'].includes(document.querySelector('.nlam').getAttribute('data-state'))", timeout=60000)
    r["idle"] = page.evaluate(IDLE)
    page.wait_for_timeout(12000)
    r["map"] = page.evaluate(INFO)
    try:
        r["labels"] = page.evaluate(LABELS)
    except Exception as e:  # noqa: BLE001
        r["labels"] = str(e)
    page.locator(".nlam").screenshot(path=str(SHOTS / ("%s-%s-map.png" % (lang, tag))))
    foot = page.locator(".nlam__pin--hero .nlam__pf").bounding_box()
    page.mouse.click(foot["x"] + foot["width"] / 2, foot["y"] + foot["height"] / 2)
    page.wait_for_timeout(1500)
    r["card_project"] = page.evaluate(CARD)
    page.locator(".nlam__frame").screenshot(path=str(SHOTS / ("%s-%s-card-project.png" % (lang, tag))))
    page.locator(".nlam__x").click()
    page.wait_for_timeout(900)
    pt = page.evaluate(REN_PT, REN[lang])
    page.mouse.click(pt["x"], pt["y"])
    page.wait_for_timeout(1500)
    r["card_renewal"] = page.evaluate(CARD)
    page.locator(".nlam__frame").screenshot(path=str(SHOTS / ("%s-%s-card-renewal.png" % (lang, tag))))
    if tag == "1440":
        page.locator(".nlam__list > summary").click()
        page.wait_for_timeout(300)
        page.locator(".nlam__list").screenshot(path=str(SHOTS / ("%s-%s-list.png" % (lang, tag))))
    r["scroll_overflow"] = page.evaluate("() => document.documentElement.scrollWidth - innerWidth")
    r["page_errors"], r["console_errors"] = errs, cons
    b.close()
    rep.append(r)
    print(json.dumps(r, ensure_ascii=False)[:1500])


def main():
    rep = []
    with sync_playwright() as pw:
        for lang in LANGS:
            for tag, vp, mobile in SIZES:
                run(pw, lang, tag, vp, mobile, rep)
    old = []
    fn = SHOTS / "report.json"
    if fn.exists():
        old = [x for x in json.load(open(fn, encoding="utf-8")) if x["lang"] not in LANGS]
    json.dump(old + rep, open(fn, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
