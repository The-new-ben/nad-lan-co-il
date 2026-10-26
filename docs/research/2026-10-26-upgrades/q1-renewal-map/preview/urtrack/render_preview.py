# -*- coding: utf-8 -*-
"""Renders preview/urtrack/index.html (the real core.css + core.js + tools/urtrack.js + renewal-track.json, inline) in Chrome at
390 and 1280 px, presses every control of the first tool (every preset, both views, city, search with spelling folding, a search
with no result and clearing it, the complex select, the full-breakdown table, copy, WhatsApp, print), then every preset of every
case on the page, and checks: no console error or warning, no sideways scroll, nothing past the viewport outside a table scroller.
Writes render-report.json and shot-{p,d}-*.png next to this file.
    python docs/research/2026-10-26-upgrades/q1-renewal-map/preview/urtrack/render_preview.py"""
import json, os, pathlib, sys
from playwright.sync_api import sync_playwright
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
URL = (HERE / "index.html").as_uri()
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
report = {"url": "preview/urtrack/index.html", "widths": {}}


def ans(pg, h):
    return pg.evaluate("(h)=>{var a=document.querySelector('#'+h+' .nli__answer');return a?a.innerText.replace(/\\s+/g,' ').trim():''}", h)


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    for w, tag in ((390, "p"), (1280, "d")):
        ctx = b.new_context(viewport={"width": w, "height": 900}, device_scale_factor=1)
        pg = ctx.new_page(); errs = []; steps = []
        pg.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
        pg.add_init_script("window.__prints=0;window.print=function(){window.__prints++;};")
        pg.goto(URL); pg.wait_for_timeout(1800)
        R = {"instances": pg.locator(".nli__panel").count(), "overflow_on_load": pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth")}
        root = pg.locator("#h0"); step = lambda name: steps.append([name, ans(pg, "h0")[:140]])
        pres = root.locator(".nli__pre button")
        for i in range(pres.count()):
            pres.nth(i).click(); pg.wait_for_timeout(200); step("preset " + pres.nth(i).locator("span").inner_text())
        seg = root.locator(".nli__seg button")
        seg.nth(1).click(); pg.wait_for_timeout(200); step("view: מה זז במאגר")
        sels = root.locator("select")
        sels.nth(0).select_option(value="ירושלים"); pg.wait_for_timeout(200); step("moves view, city ירושלים")
        seg.nth(0).click(); pg.wait_for_timeout(200); step("view: מתחם אחד (the complex comes back)")
        sels.nth(0).select_option(value="חיפה"); pg.wait_for_timeout(200); step("city חיפה (opens on its newest move)")
        q = root.locator("input[type=text]")
        for t in ("פתח תקווה", "גבעתיים", "zzqx", ""):
            q.fill(t); pg.wait_for_timeout(350); step("search '%s' -> %d options%s" % (t, sels.nth(1).locator("option").count(), " | error: " + " ".join(x for x in root.locator(".nli__err").all_inner_texts() if x) if t == "zzqx" else ""))
        sels.nth(1).select_option(index=2); pg.wait_for_timeout(200); step("complex select, third option")
        root.locator("details.nli__table summary").click(); pg.wait_for_timeout(150)
        R["table_rows"] = root.locator("details.nli__table tbody tr").count()
        sh = root.locator(".nli__share > *")
        sh.nth(0).click(); pg.wait_for_timeout(250); R["copy"] = sh.nth(0).inner_text()
        try:
            with ctx.expect_page(timeout=4000) as pi:
                sh.nth(1).click()
            R["whatsapp"] = pi.value.url[:60]; pi.value.close()
        except Exception as e:
            R["whatsapp"] = "no page: %s" % e
        sh.nth(2).click(); pg.wait_for_timeout(150); R["print_calls"] = pg.evaluate("window.__prints")
        n = 0
        for hi in range(pg.locator(".nli-host").count()):
            pb = pg.locator("#h%d .nli__pre button" % hi)
            for i in range(pb.count()):
                pb.nth(i).click(); pg.wait_for_timeout(100); n += 1
        R["presets_pressed_all_cases"] = n
        pg.reload(); pg.wait_for_timeout(1500)
        for hi in range(pg.locator(".nli-host").count()):
            pg.locator("#h%d details.nli__table summary" % hi).click()
        pg.wait_for_timeout(300)
        R["overflow_tables_open"] = pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth")
        R["past_viewport"] = pg.evaluate("""()=>{var W=document.documentElement.clientWidth,o=[];document.querySelectorAll('.nli *').forEach(function(e){var r=e.getBoundingClientRect();if((r.right>W+1||r.left<-1)&&!e.closest('.nli__tw'))o.push(e.tagName+'.'+e.className)});return o.slice(0,10)}""")
        for hi, name in ((0, "default"), (3, "approved-xplan"), (4, "two-sources"), (8, "moves")):
            el = pg.locator("#h%d .nli__out" % hi) if tag == "p" else pg.locator("#h%d .nli__panel" % hi)
            el.screenshot(path=str(HERE / ("shot-%s-%s.png" % (tag, name))))
        R["steps"] = steps; R["console"] = errs or "none"
        report["widths"][str(w)] = R
        print(w, "| instances", R["instances"], "| overflow", R["overflow_on_load"], R["overflow_tables_open"], "| past viewport", R["past_viewport"] or "none", "| console", R["console"], "| presets pressed", n, "| print", R["print_calls"], "| copy", R["copy"], "| wa", R["whatsapp"])
        ctx.close()
    b.close()
(HERE / "render-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
