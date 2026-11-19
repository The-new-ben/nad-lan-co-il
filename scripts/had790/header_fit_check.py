# -*- coding: utf-8 -*-
"""HAD-790 (20.11.2026, Ben: "rentals management in the home menu, in a fitting place"): measure the site header for overlaps.
  python header_fit_check.py            measure the live header as it is
  python header_fit_check.py --sim      first insert the planned item into the live page (same markup and CSS the release adds)
Widths 1080, 1180, 1280, 1366, 1440, 1600, 1920 and a 390 px phone (the sheet). Pass = no two header parts overlap, nothing leaves
the bar, the nav does not scroll sideways, and on the phone the item shows in the opened sheet right after the rentals panel.
One headless Chrome at a time; the report goes to docs/qa/had-790/header-fit-<mode>.txt."""
import os, sys, json
from playwright.sync_api import sync_playwright

SIM = "--sim" in sys.argv
EXTRA = os.environ.get('HFIT_CSS', '')  # an option under test, added after the planned CSS
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "qa", "had-790")
PAGES = [("he", "/"), ("he", "/projects/hamedina/"), ("en", "/en/")]
LBL = {"he": ("דירות להשכרה", "ניהול השכרה", "/my-rentals/"), "en": ("Apartments", "Rental management", "/my-rentals/?lang=en")}
INJ = """([after, label, href, extra]) => {
  if (document.querySelector('.nlhp-nav__keep')) return 'present';
  const s = [...document.querySelectorAll('#nlhp-nav > details > summary.nlhp-nav__item')].find(x => x.textContent.trim().startsWith(after));
  if (!s) return 'no-anchor';
  const a = document.createElement('a'); a.className = 'nlhp-nav__item nlhp-nav__plain nlhp-nav__keep'; a.href = href; a.textContent = label;
  s.parentElement.after(a);
  const st = document.createElement('style');
  st.textContent = '@media (max-width:1360px){.nlhp-nav__plain.nlhp-nav__keep{display:flex}}@media (max-width:1060px){.nlhp-nav .nlhp-nav__plain.nlhp-nav__keep{display:flex}}';
  document.head.appendChild(st); if (extra) { const x = document.createElement('style'); x.textContent = extra; document.head.appendChild(x); } return 'injected'; }"""
MEASURE = """() => {
  const vis = e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden'; };
  const top = document.querySelector('#nlhp-top .nlhp-top__in'); const nav = document.querySelector('#nlhp-nav');
  const parts = [];
  const add = (e, n) => { if (e && vis(e)) { const r = e.getBoundingClientRect(); parts.push({n, l: r.left, r: r.right, t: r.top, b: r.bottom}); } };
  add(document.querySelector('#nlhp-top .nlhp-logo'), 'logo');
  document.querySelectorAll('#nlhp-nav > details > summary.nlhp-nav__item, #nlhp-nav > a.nlhp-nav__item').forEach(e => add(e, e.textContent.trim()));
  document.querySelectorAll('#nlhp-top .nlhp-top__end > *').forEach(e => add(e, 'end:' + (e.className || e.tagName)));
  const ov = [];
  for (let i = 0; i < parts.length; i++) for (let j = i + 1; j < parts.length; j++) {
    const a = parts[i], b = parts[j];
    if (Math.min(a.r, b.r) - Math.max(a.l, b.l) > 1 && Math.min(a.b, b.b) - Math.max(a.t, b.t) > 1) ov.push(a.n + ' x ' + b.n);
  }
  const out = parts.filter(p => p.l < -1 || p.r > innerWidth + 1).map(p => p.n);
  const keep = document.querySelector('.nlhp-nav__keep');
  return { items: parts.filter(p => !p.n.startsWith('end:') && p.n !== 'logo').map(p => p.n), overlaps: ov, outside: out,
           navScroll: nav ? nav.scrollWidth - nav.clientWidth : 0, keepShown: !!(keep && vis(keep)),
           keepRect: keep && vis(keep) ? [Math.round(keep.getBoundingClientRect().left), Math.round(keep.getBoundingClientRect().right)] : null }; }"""
SHEET = """([after]) => {
  const k = document.querySelector('.nlhp-nav__keep'); if (!k) return {ok: false, why: 'no item'};
  const prev = k.previousElementSibling; const r = k.getBoundingClientRect();
  return {ok: r.height >= 44 && !!prev && prev.textContent.trim().startsWith(after), h: Math.round(r.height), prev: prev ? prev.textContent.trim().slice(0, 30) : '', text: k.textContent.trim(), href: k.getAttribute('href')}; }"""
lines, allok = [], True
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for lang, path in PAGES:
        after, label, href = LBL[lang]
        row = []
        ctx = b.new_context(viewport={"width": 1920, "height": 900})
        pg = ctx.new_page()
        pg.goto("https://nad-lan.co.il" + path + "?hfit=1", wait_until="domcontentloaded", timeout=90000)
        pg.wait_for_timeout(1500)
        if SIM:
            row.append("sim:" + pg.evaluate(INJ, [after, label, href, EXTRA]))
        for w in (1080, 1180, 1279, 1280, 1300, 1366, 1400, 1440, 1600, 1920):
            pg.set_viewport_size({"width": w, "height": 900}); pg.wait_for_timeout(350)
            m = pg.evaluate(MEASURE)
            ok = not m["overlaps"] and not m["outside"] and m["navScroll"] <= 1 and m["keepShown"]
            allok &= ok
            row.append("%d: %s items %d overlap %s outside %s navScroll %d item %s" % (w, "OK" if ok else "BAD", len(m["items"]), m["overlaps"], m["outside"], m["navScroll"], m["keepRect"]))
            if w in (1080, 1280, 1440):
                pg.screenshot(path=os.path.join(OUT, "header-fit-%s-%s-%s-%d.png" % ("sim" if SIM else "live", lang, path.strip("/").replace("/", "_") or "home", w)), clip={"x": 0, "y": 0, "width": w, "height": 90})
        ctx.close()
        ph = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
        pg = ph.new_page()
        pg.goto("https://nad-lan.co.il" + path + "?hfit=2", wait_until="domcontentloaded", timeout=90000)
        pg.wait_for_timeout(1500)
        if SIM:
            pg.evaluate(INJ, [after, label, href, EXTRA])
        m = pg.evaluate(MEASURE)
        pg.locator("#nlhp-top .nlhp-ico--menu").tap(); pg.wait_for_timeout(600)
        s = pg.evaluate(SHEET, [after])
        ok = not m["overlaps"] and s["ok"]
        allok &= ok
        pg.screenshot(path=os.path.join(OUT, "header-fit-%s-%s-%s-phone.png" % ("sim" if SIM else "live", lang, path.strip("/").replace("/", "_") or "home")))
        row.append("phone390: %s bar overlap %s sheet %s" % ("OK" if ok else "BAD", m["overlaps"], json.dumps(s, ensure_ascii=False)))
        ph.close()
        lines.append("%s %s | %s" % (lang, path, " | ".join(row)))
        print(lines[-1])
    b.close()
lines.append("ALL OK" if allok else "SOME BAD")
print(lines[-1])
open(os.path.join(OUT, "header-fit-%s.txt" % (("sim-opt" if EXTRA else "sim") if SIM else "live")), "w", encoding="utf-8").write("\n".join(lines) + "\n")
