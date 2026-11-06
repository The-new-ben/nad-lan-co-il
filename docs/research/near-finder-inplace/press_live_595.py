# -*- coding: utf-8 -*-
"""Release 1.72.595 live press: the near finder in place. Phone 390x844 and desktop 1280x900, on the live pages as they are (no
route). Per page: no floating launcher; the switch where it belongs; the map choice shows the app with results; back to the list
or projects; "מסך מלא" opens the dialog and Escape returns; #lidi opens in place; console errors; horizontal scroll. The card page:
no finder at all. Screenshots in shots/live595-*."""
import json, os, sys, time
from playwright.sync_api import sync_playwright
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); SH = os.path.join(H, "shots"); os.makedirs(SH, exist_ok=True)
B = "https://nad-lan.co.il"
PAGES = [("home", "/", "דירות לידי"), ("properties", "/properties/", None),
         ("rent", "/%D7%93%D7%99%D7%A8%D7%95%D7%AA-%D7%9C%D7%94%D7%A9%D7%9B%D7%A8%D7%94/", "על המפה"), ("broker", "/brokers/meital-katzir/", "על המפה"),
         ("card", "/professionals/meital-katzir/", None)]
ST = """() => { const app = document.getElementById('nlnf-app'); const l = document.getElementById('nlnf-launch');
  const vis = e => !!e && e.offsetParent !== null && e.getBoundingClientRect().height > 0;
  const rows = app ? app.querySelectorAll('[class*="nlnf-row"], [class*="nlnf__item"], li[data-id], .nlnf-card, .nlnf__res li').length : 0;
  return {launcher: vis(l), app: !!app, appVisible: vis(app), inDlg: !!(app && app.closest('.nlnf-dlg')), dlgOpen: (() => { const d = document.getElementById('nlnf-dlg'); return !!d && !d.hidden; })(),
          rows: rows, count: app ? ((app.querySelector('[class*="count"]') || {}).textContent || '').trim().slice(0, 40) : '',
          hs: document.documentElement.scrollWidth - innerWidth, finderJs: !!document.querySelector('script[src*="near-finder/finder.js"]')}; }"""
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for w, mob in ((390, True), (1280, False)):
        for name, path, label in PAGES:
            ctx = b.new_context(viewport={"width": w, "height": 844 if mob else 900}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1,
                                geolocation={"latitude": 32.0853, "longitude": 34.7818}, permissions=["geolocation"])
            pg = ctx.new_page(); errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "tawk" not in m.text and "ERR_FAILED" not in m.text else None)
            pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
            pg.goto(B + path + "?lp=%d" % time.time(), wait_until="load", timeout=90000); time.sleep(3)
            o = {"start": pg.evaluate(ST)}
            tag = "%s-%s" % (name, "m390" if mob else "d1280")
            if label:
                btn = pg.locator('button:has-text("%s")' % label).first
                o["switch"] = btn.count() > 0
                if o["switch"]:
                    btn.scroll_into_view_if_needed(); time.sleep(0.5); btn.click(); time.sleep(6)
                    o["map"] = pg.evaluate(ST)
                    y = pg.evaluate("() => document.getElementById('nlnf-app').getBoundingClientRect().top + scrollY - 150")
                    pg.evaluate("y => window.scrollTo(0, y)", y); time.sleep(2); pg.screenshot(path=os.path.join(SH, "live595-%s-map.png" % tag))
                    fs = pg.locator('#nlnf-app button:has-text("מסך מלא")').first
                    if fs.count():
                        fs.click(); time.sleep(2); o["fullscreen"] = pg.evaluate(ST); pg.keyboard.press("Escape"); time.sleep(1.5); o["afterEsc"] = pg.evaluate(ST)
                    back = pg.locator('button:has-text("%s")' % ("פרויקטים חדשים" if name == "home" else "רשימה")).first
                    if back.count(): back.click(); time.sleep(1.5); o["back"] = pg.evaluate(ST)
            elif name == "properties":
                y = pg.evaluate("() => document.getElementById('nlnf').getBoundingClientRect().top + scrollY - 100"); pg.evaluate("y => window.scrollTo(0, y)", y); time.sleep(6)
                o["map"] = pg.evaluate(ST); pg.screenshot(path=os.path.join(SH, "live595-%s-map.png" % tag))
            o["errors"] = errs; ctx.close()
            if label:
                ctx = b.new_context(viewport={"width": w, "height": 844 if mob else 900}, is_mobile=mob, has_touch=mob); pg = ctx.new_page()
                pg.goto(B + path + "?lp2=%d#lidi" % time.time(), wait_until="load", timeout=90000); time.sleep(5)
                o["lidi"] = pg.evaluate(ST); ctx.close()
            out[tag] = o
    b.close()
json.dump(out, open(os.path.join(H, "press-live-595.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, o in out.items():
    s = o["start"]; m = o.get("map") or {}; f = o.get("fullscreen") or {}; e = o.get("afterEsc") or {}; bk = o.get("back") or {}; ld = o.get("lidi") or {}
    print("%-16s launcher=%s finderJs=%s | switch=%s map: visible=%s rows=%s count=%r | full: dlg=%s esc: dlg=%s inDlg=%s | back: visible=%s | lidi: visible=%s dlg=%s | hs=%s errors=%s" % (
        k, s["launcher"], s["finderJs"], o.get("switch"), m.get("appVisible"), m.get("rows"), m.get("count"), f.get("dlgOpen"), e.get("dlgOpen"), e.get("inDlg"),
        bk.get("appVisible"), ld.get("appVisible"), ld.get("dlgOpen"), max([x.get("hs", 0) for x in (s, m, bk) if x] or [0]), o["errors"][:2]))
