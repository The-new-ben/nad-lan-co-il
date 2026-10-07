# -*- coding: utf-8 -*-
"""Sde Dov components in a language (7.10.2026, HAD-460): builds a local preview page per language (a stand-in page head,
the PriceGuide from price_guide/sde-dov-prices[.<lang>].json and the AreaMap from area_map/sde-dov[.<lang>].json, with their
CSS and script, in the page's lang/dir) into the system temp folder, then opens it in headless Chrome (WebGL through
SwiftShader) at 390x844 and takes the shots docs/qa/had-460/i18n-components/sde-dov-<lang>-390-*.png.
DOM checks: page overflow, any component element past the section's edges, Hebrew letters in the components' text,
console and page errors, the calculator's values in the "sea" mode, the WhatsApp text, map state and pins.
Usage: python shoot_sde_dov.py [en,ar] [--noshots fr,ru]. Report: sde-dov-report.json in the same folder."""
import io
import json
import os
import pathlib
import sys
import tempfile

from playwright.sync_api import sync_playwright

REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
sys.path.insert(0, os.path.join(REPO, "scripts", "project-stage", "price_guide"))
sys.path.insert(0, os.path.join(REPO, "scripts", "project-stage", "area_map"))
import render as PG  # noqa: E402
import render_map as AM  # noqa: E402

SHOTS = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
TMP = pathlib.Path(tempfile.gettempdir()) / "nlsd-i18n-preview"
TMP.mkdir(parents=True, exist_ok=True)
ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]
HEAD = {"he": ("רובע שדה דב: מחירי הדירות", "(פסקת הפתיחה של העמוד)"),
        "en": ("Sde Dov apartment prices", "(The page's opening paragraph, translated elsewhere.)"),
        "fr": ("Les prix des appartements à Sde Dov", "(Le paragraphe d’ouverture de la page, traduit ailleurs.)"),
        "ru": ("Цены на квартиры в районе Сде-Дов", "(Вступительный абзац страницы, переводится отдельно.)"),
        "ar": ("أسعار الشقق في سديه دوف", "(الفقرة الافتتاحية للصفحة، تُترجم في مكان آخر.)")}
CSSX = """
body{margin:0;background:#f7f6f2;font-family:Assistant,"Segoe UI",Arial,sans-serif;color:#14212b}
.px{padding:24px 0 60px}
.px-ctx{max-width:1240px;margin:0 auto;padding:0 clamp(16px,3vw,32px);display:grid;gap:10px}
.px-h1{font-family:"Noto Serif Hebrew",Georgia,serif;font-weight:600;font-size:clamp(26px,4vw,34px);line-height:1.2;margin:0}
.px-lead{margin:0;font-size:17px;line-height:1.7;color:#3b4753}
.px-gap{max-width:1240px;margin:28px auto 0;padding:0 clamp(16px,3vw,32px)}
.px-gap div{height:600px;border-radius:22px;background:#1f4b5c}
"""


def page(lang):
    sfx = "" if lang == "he" else "." + lang
    pd = json.load(io.open(os.path.join(REPO, "scripts", "project-stage", "price_guide", "sde-dov-prices%s.json" % sfx), encoding="utf-8"))
    md = AM.load("sde-dov" + sfx)
    u = PG.ui(pd)
    h1, lead = HEAD[lang]
    return ('<!doctype html>\n<html lang="%s" dir="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Sde Dov components %s</title>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@500;600;700&amp;family=Assistant:wght@400;600;700&amp;display=swap">'
            '<style>%s%s%s</style></head><body><div class="px"><div class="px-ctx"><h1 class="px-h1">%s</h1><p class="px-lead">%s</p></div>'
            '%s%s<div class="px-gap"><div></div></div></div><script>%s</script><script>%s</script></body></html>\n') % (
        u["lang"], u["dir"], lang, CSSX, PG.CSS, AM.CSS, h1, lead, PG.html(pd, "972525101555"), AM.html(md), PG.JS, AM.JS)


EDGES = """(sel) => { const root = document.querySelector(sel); const rb = root.getBoundingClientRect(); const out = [];
  root.querySelectorAll('*').forEach(e => { if (e.closest('.nlam__map')) return; const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden') return;
    const b = e.getBoundingClientRect(); if (!b.width || !b.height) return;
    if (b.right > rb.right + 1 || b.left < rb.left - 1) out.push({tag: e.tagName, cls: e.className && e.className.baseVal === undefined ? e.className : '', l: Math.round(b.left - rb.left), r: Math.round(rb.right - b.right), text: (e.innerText || '').slice(0, 60)}); });
  return out.slice(0, 10); }"""
HEB = """(sel) => { const t = document.querySelector(sel).innerText; const m = t.match(/[\\u0590-\\u05ff][\\u0590-\\u05ff\\s"'״׳-]*/g); return m ? m.slice(0, 8) : []; }"""
IDLE = """() => new Promise(res => { const m = document.querySelector('.nlam').__nlamMap; if (!m) return res('no map');
  if (m.loaded() && m.areTilesLoaded()) return res('idle'); m.once('idle', () => res('idle')); setTimeout(() => res('timeout'), 30000); })"""
LABELS = """() => { const r = document.querySelector('.nlam'), m = r.__nlamMap; const f = m.queryRenderedFeatures().filter(x => x.layer.type === 'symbol' && x.layer.layout && x.layer.layout['text-field']);
  const names = []; f.forEach(x => { const n = x.properties['name:' + r.lang] || x.properties['name:en'] || x.properties.name || x.properties.name; if (n && names.indexOf(n) < 0) names.push(n) });
  return {count: names.length, hebrew: names.filter(n => /[\\u0590-\\u05ff]/.test(n)).slice(0, 10), sample: names.slice(0, 12)}; }"""
CARD = """() => { const r = document.querySelector('.nlam'), c = r.querySelector('.nlam__card'), f = r.querySelector('.nlam__frame'); if (c.hidden) return {open: false};
  const b = c.getBoundingClientRect(), fb = f.getBoundingClientRect();
  return {open: true, text: c.innerText.replace(/\\s+/g, ' ').trim(), href: (c.querySelector('a') || {}).href || null,
    inside: b.left >= fb.left - 1 && b.right <= fb.right + 1 && b.top >= fb.top - 1 && b.bottom <= fb.bottom + 1}; }"""


def run(pw, lang, shots, rep):
    fn = TMP / ("sde-dov-%s.html" % lang)
    io.open(fn, "w", encoding="utf-8", newline="\n").write(page(lang))
    b = pw.chromium.launch(channel="chrome", headless=True, args=ARGS)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True,
                        locale={"he": "he-IL", "ar": "ar"}.get(lang, lang))
    page_ = ctx.new_page()
    errs, cons = [], []
    page_.on("pageerror", lambda e: errs.append(str(e)))
    page_.on("console", lambda m: m.type == "error" and cons.append(m.text))
    page_.goto(fn.as_uri(), wait_until="load")
    page_.wait_for_timeout(900)
    r = {"lang": lang, "size": "390x844"}
    shot = lambda loc, name: shots and loc.screenshot(path=str(SHOTS / ("sde-dov-%s-390-%s.png" % (lang, name))))
    pg = page_.locator(".nlpg")
    pg.scroll_into_view_if_needed()
    page_.wait_for_timeout(300)
    shot(pg, "price")
    r["price_default"] = page_.evaluate("""() => { const q = s => (document.querySelector(s) || {}).textContent; return {big: q('[data-pg="p"]'), pm: q('[data-pg="pm"]'), tx: q('[data-pg="tx"]'), tt: q('[data-pg="tt"]')}; }""")
    page_.locator('.nlpg input[value="sea"]').click(force=True)
    page_.wait_for_timeout(300)
    shot(page_.locator(".nlpg__calc"), "price-sea")
    r["price_sea"] = page_.evaluate("""() => { const q = s => (document.querySelector(s) || {}).textContent; return {big: q('[data-pg="p"]'), pm: q('[data-pg="pm"]'),
        tx: q('[data-pg="tx"]'), tt: q('[data-pg="tt"]'), why: q('[data-pg="why"]'), chart: [...document.querySelectorAll('.nlpg__chart text')].map(t => t.textContent),
        wa: decodeURIComponent((document.querySelector('[data-pg="wa"]') || {href: ''}).href.split('text=')[1] || '')}; }""")
    page_.locator(".nlpg__more").click()
    page_.wait_for_timeout(400)
    shot(page_.locator(".nlpg__list"), "price-list")
    r["price_edges"] = page_.evaluate(EDGES, ".nlpg")
    r["price_hebrew"] = page_.evaluate(HEB, ".nlpg")
    r["price_rows_visible"] = page_.evaluate("() => [...document.querySelectorAll('.nlpg__table tbody tr:not(.nlpg__gh)')].filter(t => t.offsetHeight).length")
    # AreaMap
    page_.locator(".nlam__frame").scroll_into_view_if_needed()
    page_.wait_for_function("() => ['ready','fail'].includes(document.querySelector('.nlam').getAttribute('data-state'))", timeout=60000)
    r["idle"] = page_.evaluate(IDLE)
    page_.wait_for_timeout(12000)
    r["map"] = page_.evaluate("""() => { const r = document.querySelector('.nlam'); return {state: r.getAttribute('data-state'), dir: r.getAttribute('dir'), lang: r.getAttribute('lang'),
        pins: r.querySelectorAll('.nlam__pin').length, chips: [...r.querySelectorAll('.nlam__chip')].map(c => c.textContent.trim())}; }""")
    try:
        r["basemap_labels"] = page_.evaluate(LABELS)
    except Exception as e:  # noqa: BLE001
        r["basemap_labels"] = str(e)
    shot(page_.locator(".nlam"), "map")
    pin = page_.locator(".nlam__pin").first.locator(".nlam__pf").bounding_box()
    page_.mouse.click(pin["x"] + pin["width"] / 2, pin["y"] + pin["height"] / 2)
    page_.wait_for_timeout(1500)
    r["card_project"] = page_.evaluate(CARD)
    shot(page_.locator(".nlam__frame"), "card")
    page_.locator(".nlam__x").click()
    page_.wait_for_timeout(600)
    page_.locator(".nlam__list > summary").click()
    page_.wait_for_timeout(300)
    shot(page_.locator(".nlam__list"), "map-list")
    r["map_edges"] = page_.evaluate(EDGES, ".nlam")
    r["map_hebrew"] = page_.evaluate(HEB, ".nlam")
    r["scroll_overflow"] = page_.evaluate("() => document.documentElement.scrollWidth - innerWidth")
    r["page_errors"], r["console_errors"] = errs, cons
    b.close()
    rep.append(r)
    print(json.dumps(r, ensure_ascii=False)[:2500])


def main():
    args = sys.argv[1:]
    langs = args[0].split(",") if args and not args[0].startswith("--") else ["en", "ar"]
    quiet = args[args.index("--noshots") + 1].split(",") if "--noshots" in args else []
    rep = []
    with sync_playwright() as pw:
        for lang in langs:
            run(pw, lang, True, rep)
        for lang in quiet:
            run(pw, lang, False, rep)
    json.dump(rep, open(SHOTS / "sde-dov-report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
