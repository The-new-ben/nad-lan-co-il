# -*- coding: utf-8 -*-
"""Round N live press (HAD-675): /mortgage-calculator/ on the live site, phone 390x844 and desktop 1280x900.
Per width: the map "כל נושאי המשכנתא" with 8 stages (phone: closed accordions; desktop: all open), every map link resolves to an
element on the page or to a guide path; the four new chips open their panes and the tools mount (height > 200, no console error);
the new chapters exist; back-links; FAQ count; the byline is the last text block; one h1; no horizontal scroll. Shots in shots/live-n-*."""
import json, os, sys, time
from playwright.sync_api import sync_playwright
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); SH = os.path.join(H, "shots"); os.makedirs(SH, exist_ok=True)
URL = "https://nad-lan.co.il/mortgage-calculator/"
NEW = [("tool-hivun", "mhivun"), ("tool-neches", "mneches"), ("tool-rishum", "mrishum"), ("tool-kashe", "mkashe")]
SECS = ["what-is-mortgage", "mortgage-registration", "registration-fees", "mortgage-cancellation", "capitalization-fee",
        "payment-trouble", "mortgage-rights", "existing-property", "mortgage-banks", "rules-2026"]
ST = """(secs) => { const q = s => document.querySelector(s); const vis = e => !!e && e.getBoundingClientRect().height > 0 && getComputedStyle(e).display !== 'none';
  const map = q('#mortgage-map'); const ds = map ? [...map.querySelectorAll('details.nlmap__d')] : [];
  const links = map ? [...map.querySelectorAll('a[href]')].map(a => a.getAttribute('href')) : [];
  const broken = links.filter(h => h.startsWith('#') && !document.getElementById(h.slice(1)));
  const by = q('.nlx-byline'); const after = by ? (() => { let n = 0, e = by.nextElementSibling; while (e) { if (e.tagName !== 'SCRIPT' && e.textContent.trim()) n++; e = e.nextElementSibling; } return n; })() : -1;
  const t = id => { const r = q('[data-nli="' + id + '"]'); return r ? {h: Math.round(r.getBoundingClientRect().height), kids: r.children.length} : null; };
  return {sw: (q('#nlmx-sw-h') || {}).textContent || '', chips: document.querySelectorAll('#tools button[data-sw]').length,
    map: !!map, groups: ds.length, open: ds.filter(d => d.open).length, links: links.length, broken,
    secs: secs.filter(s => !q('#' + s)), backs: document.querySelectorAll('.nlmap-back').length,
    faq: (() => { let n = 0; document.querySelectorAll('script[type="application/ld+json"]').forEach(s => { n += (s.textContent.match(/"@type":\\s*"Question"/g) || []).length; }); return n; })(),
    byline: vis(by), afterByline: after, h1: document.querySelectorAll('h1').length, hs: document.documentElement.scrollWidth - innerWidth,
    tools: {mhivun: t('mhivun'), mneches: t('mneches'), mrishum: t('mrishum'), mkashe: t('mkashe')}}; }"""
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for w, mob in ((390, True), (1280, False)):
        tag = "m390" if mob else "d1280"
        ctx = b.new_context(viewport={"width": w, "height": 844 if mob else 900}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1)
        pg = ctx.new_page(); errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "tawk" not in m.text and "ERR_FAILED" not in m.text and "hotjar" not in m.text.lower() else None)
        pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
        pg.goto(URL + "?pn=%d" % time.time(), wait_until="load", timeout=120000); time.sleep(5)
        o = {"start": pg.evaluate(ST, SECS)}
        y = pg.evaluate("() => { const s = document.getElementById('mortgage-map'); return s ? s.getBoundingClientRect().top + scrollY - 60 : 0; }")
        pg.evaluate("y => window.scrollTo(0, y)", y); time.sleep(1); pg.screenshot(path=os.path.join(SH, "live-n-map-%s.png" % tag))
        for chip, tid in NEW:
            btn = pg.locator('#tools button[data-sw="%s"]' % chip).first
            o["chip-" + tid] = btn.count() > 0
            if btn.count():
                btn.scroll_into_view_if_needed(); btn.click(); time.sleep(3)
                o["after-" + tid] = pg.evaluate(ST, SECS)["tools"][tid]
                y = pg.evaluate("id => { const r = document.querySelector('[data-nli=\"' + id + '\"]'); return r ? r.getBoundingClientRect().top + scrollY - 120 : 0; }", tid)
                pg.evaluate("y => window.scrollTo(0, y)", y); time.sleep(1.5)
                pg.screenshot(path=os.path.join(SH, "live-n-%s-%s.png" % (tid, tag)))
        # a map link to a chip from the map itself
        a = pg.locator('#mortgage-map a[href="#tool-hivun"]').first
        if a.count():
            if mob: pg.evaluate("() => document.querySelectorAll('#mortgage-map details').forEach(d => d.open = true)")
            a.scroll_into_view_if_needed(); a.click(); time.sleep(2)
            o["map_to_chip"] = pg.evaluate("() => (document.querySelector('#tools button[data-sw=\"tool-hivun\"]') || {}).getAttribute ? document.querySelector('#tools button[data-sw=\"tool-hivun\"]').getAttribute('aria-pressed') : null")
        for sid in ("what-is-mortgage", "mortgage-registration", "payment-trouble", "mortgage-banks"):
            y = pg.evaluate("id => { const s = document.getElementById(id); return s ? s.getBoundingClientRect().top + scrollY - 80 : 0; }", sid)
            pg.evaluate("y => window.scrollTo(0, y)", y); time.sleep(1); pg.screenshot(path=os.path.join(SH, "live-n-%s-%s.png" % (sid, tag)))
        o["errors"] = errs; out[tag] = o; ctx.close()
    b.close()
json.dump(out, open(os.path.join(H, "press-live-n.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, o in out.items():
    s = o["start"]
    print(k, "| sw:", s["sw"], "| chips:", s["chips"], "| map groups/open/links/broken:", s["groups"], s["open"], s["links"], s["broken"],
          "| missing secs:", s["secs"], "| backs:", s["backs"], "| faq:", s["faq"], "| byline:", s["byline"], "after:", s["afterByline"],
          "| h1:", s["h1"], "| hs:", s["hs"], "| errors:", o["errors"][:3])
    print("   tools:", {t: o.get("after-" + t) for _, t in NEW}, "| map->chip:", o.get("map_to_chip"))
