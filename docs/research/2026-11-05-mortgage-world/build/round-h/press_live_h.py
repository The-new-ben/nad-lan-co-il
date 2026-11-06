# -*- coding: utf-8 -*-
"""Round H live press: /mortgage-calculator/ at 390x844 (phone) and 1280x900. Opens the 7th chip, reads the headline and the timeline,
presses every plan, grace and term chip, checks that every tool on the page mounted, no console errors, no horizontal scroll,
and that #tool-keys in the address opens the pane. Screenshots in shots/live-*."""
import json, os, sys, time
from playwright.sync_api import sync_playwright
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); SH = os.path.join(H, "shots"); os.makedirs(SH, exist_ok=True)
URL = "https://nad-lan.co.il/mortgage-calculator/"
READ = """() => { const t = document.querySelector('[data-nli="mkeys"]'); if (!t) return 'no host';
  const q = s => t.querySelector(s); const txt = e => e ? e.textContent.replace(/\\s+/g, ' ').trim() : null;
  return {mounted: !!t.querySelector('button'), headline: txt([...t.querySelectorAll('*')].find(e => /nlmk__fig|nlmk__big|nlmk__n/.test(e.className || '')) || null),
          sub: txt(q('.nlmk__sub')), rows: t.querySelectorAll('ol li').length, first: txt(q('ol li')), last: txt(q('ol li:last-child')),
          paneHidden: document.getElementById('tool-keys').hidden, hscroll: document.documentElement.scrollWidth - innerWidth}; }"""
out = {}
with sync_playwright() as p:
    for name, w, mob in (("phone", 390, True), ("desktop", 1280, False)):
        b = p.chromium.launch(channel="chrome", headless=True)
        ctx = b.new_context(viewport={"width": w, "height": 844 if mob else 900}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1)
        pg = ctx.new_page(); errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "tawk" not in m.text and "ERR_FAILED" not in m.text else None)
        pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
        pg.goto(URL + "?ph=%d" % time.time(), wait_until="load", timeout=90000); time.sleep(3)
        o = {"tools": pg.evaluate("() => [...document.querySelectorAll('[data-nli]')].map(h => h.getAttribute('data-nli') + ':' + (h.querySelector('button,input,select') ? 'mounted' : 'summary'))")}
        pg.click('button[data-sw="tool-keys"]'); time.sleep(2)
        o["tools_after"] = pg.evaluate("() => [...document.querySelectorAll('[data-nli]')].filter(h => h.offsetParent).map(h => h.getAttribute('data-nli') + ':' + (h.querySelector('button,input,select') ? 'mounted' : 'summary'))")
        o["default"] = pg.evaluate(READ)
        chips = pg.evaluate("() => [...document.querySelectorAll('[data-nli=\"mkeys\"] button')].map(b => b.textContent.trim()).filter(t => t && t !== 'העתקת התוצאה')")
        o["chips"] = chips; o["pressed"] = {}
        for c in chips:
            pg.click('[data-nli="mkeys"] button:has-text("%s")' % c); time.sleep(0.35)
            r = pg.evaluate(READ); o["pressed"][c] = [r["headline"], r["rows"]] if isinstance(r, dict) else r
        for c in ("לפי שלבים", "משלמים ריבית", "25 שנה"):
            if c in chips: pg.click('[data-nli="mkeys"] button:has-text("%s")' % c); time.sleep(0.3)
        y = pg.evaluate("() => document.getElementById('tool-keys').getBoundingClientRect().top + scrollY - 70")
        pg.evaluate("y => window.scrollTo(0, y)", y); time.sleep(1.5); pg.screenshot(path=os.path.join(SH, "live-%s-top.png" % name))
        y = pg.evaluate("() => { const t = document.querySelector('[data-nli=\"mkeys\"] ol'); return t.getBoundingClientRect().top + scrollY - 200; }")
        pg.evaluate("y => window.scrollTo(0, y)", y); time.sleep(1.5); pg.screenshot(path=os.path.join(SH, "live-%s-timeline.png" % name))
        o["final"] = pg.evaluate(READ); o["errors"] = errs
        ctx.close()
        ctx = b.new_context(viewport={"width": w, "height": 844}, is_mobile=mob, has_touch=mob); pg = ctx.new_page()
        pg.goto(URL + "?ph2=%d#tool-keys" % time.time(), wait_until="load", timeout=90000); time.sleep(3)
        o["hash_opens"] = pg.evaluate("() => !document.getElementById('tool-keys').hidden && document.querySelector('button[data-sw=\"tool-keys\"]').getAttribute('aria-pressed') === 'true'")
        b.close()
        out[name] = o
print(json.dumps(out, ensure_ascii=False, indent=1))
json.dump(out, open(os.path.join(H, "press-live-h.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
