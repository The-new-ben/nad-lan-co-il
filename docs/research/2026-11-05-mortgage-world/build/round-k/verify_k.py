# -*- coding: utf-8 -*-
"""Round K check: the live page with the repo's mbudget.js v2 (route), or live (--live). Phone 390x844: the budget pane's homes
block on the default example, then a budget above the cheapest listing; console errors; horizontal scroll; screenshot."""
import json, os, re, sys, time
from playwright.sync_api import sync_playwright
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); SH = os.path.join(H, "shots"); os.makedirs(SH, exist_ok=True)
JS = open(os.path.abspath(os.path.join(H, "..", "..", "..", "..", "..", "plugins", "nadlan-config", "assets", "instruments", "tools", "mbudget.js")), encoding="utf-8").read()
LIVE = "--live" in sys.argv; tag = "live" if LIVE else "k"
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2).new_page(); errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "tawk" not in m.text and "ERR_FAILED" not in m.text else None)
    pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
    if not LIVE: pg.route(re.compile(r".*/instruments/tools/mbudget\.js.*"), lambda r: r.fulfill(status=200, body=JS, headers={"content-type": "application/javascript; charset=utf-8"}))
    pg.goto("https://nad-lan.co.il/mortgage-calculator/?vk=%d#tool-budget" % time.time(), wait_until="load", timeout=90000); time.sleep(3)
    pg.evaluate("() => document.querySelector('[data-nli=\"mbudget\"]').scrollIntoView()"); time.sleep(4)
    R = "() => { const t = document.querySelector('[data-nli=\"mbudget\"]'); const hb = [...t.querySelectorAll('section')].find(s => /דירות למכירה באתר|הדירות באתר/.test(s.textContent)) || t; return {text: hb.textContent.replace(/\s+/g,' ').slice(0, 420), homes: hb.querySelectorAll('li.nlmb__home').length}; }"
    o = {"default": pg.evaluate(R)}
    y = pg.evaluate("() => { const l = document.querySelector('[data-nli=\"mbudget\"] ul.nlmb__homes') || document.querySelector('[data-nli=\"mbudget\"] .nli__note:last-of-type'); return l ? l.getBoundingClientRect().top + scrollY - 220 : 0; }")
    pg.evaluate("y => window.scrollTo(0, y)", y); time.sleep(1.3); pg.screenshot(path=os.path.join(SH, tag + "-phone-homes.png"))
    o["hscroll"] = pg.evaluate("() => document.documentElement.scrollWidth - innerWidth"); o["errors"] = errs
    b.close()
print(json.dumps(o, ensure_ascii=False, indent=1))
