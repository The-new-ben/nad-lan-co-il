# -*- coding: utf-8 -*-
"""Round M live press (HAD-675): /mortgage-calculator/ on the live site, phone 390x844 and desktop 1280x900, no routes.
Per width: the switcher says nine tools; the chips "בדיקה לפני חתימה" and "מחשבון זכאות" open their panes and the tools mount
(height > 200, no console errors); the mnomeff converter turns 4.95 into 5.06; the two new chapters, 41 FAQ questions, the byline
is the last text block of the article, one h1, no horizontal scroll. Screenshots in shots/live-m-*."""
import json, os, sys, time
from playwright.sync_api import sync_playwright
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); SH = os.path.join(H, "shots"); os.makedirs(SH, exist_ok=True)
URL = "https://nad-lan.co.il/mortgage-calculator/"
ST = """() => { const q = s => document.querySelector(s); const vis = e => !!e && e.getBoundingClientRect().height > 0 && getComputedStyle(e).display !== 'none';
  const t = id => { const r = q('[data-nli="' + id + '"]'); return r ? {h: Math.round(r.getBoundingClientRect().height), vis: vis(r), kids: r.children.length} : null; };
  const by = q('.nlx-byline'); const after = by ? (() => { let n = 0, e = by.nextElementSibling; while (e) { if (e.tagName !== 'SCRIPT' && e.textContent.trim()) n++; e = e.nextElementSibling; } return n; })() : -1;
  return {sw: (q('#nlmx-sw-h') || {}).textContent || '', mcheck: t('mcheck'), mzakaut: t('mzakaut'), mnomeff: t('mnomeff'),
          before: !!q('#before-signing'), elig: !!q('#eligibility-loan'), method: !!q('#calculator-method'),
          faq: (() => { let n = 0; document.querySelectorAll('script[type="application/ld+json"]').forEach(s => { n += (s.textContent.match(/"@type":\\s*"Question"/g) || []).length; }); return n; })(),
          byline: by ? by.textContent.trim() : '', bylineVisible: vis(by), afterByline: after, h1: document.querySelectorAll('h1').length,
          hs: document.documentElement.scrollWidth - innerWidth}; }"""
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for w, mob in ((390, True), (1280, False)):
        tag = "m390" if mob else "d1280"
        ctx = b.new_context(viewport={"width": w, "height": 844 if mob else 900}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1)
        pg = ctx.new_page(); errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "tawk" not in m.text and "ERR_FAILED" not in m.text and "hotjar" not in m.text.lower() else None)
        pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
        pg.goto(URL + "?pm=%d" % time.time(), wait_until="load", timeout=120000); time.sleep(4)
        o = {"start": pg.evaluate(ST)}
        for chip, tid in (("בדיקה לפני חתימה", "mcheck"), ("מחשבון זכאות", "mzakaut")):
            btn = pg.locator('#tools button[data-sw="tool-%s"]' % ("check" if tid == "mcheck" else "zakaut")).first
            o["chip-" + tid] = btn.count() > 0
            if btn.count():
                btn.scroll_into_view_if_needed(); btn.click(); time.sleep(3)
                o["after-" + tid] = pg.evaluate(ST)
                y = pg.evaluate("id => { const r = document.querySelector('[data-nli=\"' + id + '\"]'); return r ? r.getBoundingClientRect().top + scrollY - 120 : 0; }", tid)
                pg.evaluate("y => window.scrollTo(0, y)", y); time.sleep(1.5)
                pg.screenshot(path=os.path.join(SH, "live-m-%s-%s.png" % (tid, tag)))
        more = pg.locator('#average-mortgage-rates button.nlmx-more').first
        o["converter_folded"] = more.count() > 0
        if more.count():
            more.scroll_into_view_if_needed(); more.click(); time.sleep(1)
        conv = pg.locator('[data-nli="mnomeff"] input').first
        if conv.count():
            conv.scroll_into_view_if_needed(); conv.fill("4.95"); conv.dispatch_event("input"); time.sleep(1)
            o["mnomeff_text"] = pg.evaluate("() => (document.querySelector('[data-nli=\"mnomeff\"]') || {}).innerText || ''")[:400]
            pg.screenshot(path=os.path.join(SH, "live-m-mnomeff-%s.png" % tag))
        for sid in ("before-signing", "eligibility-loan"):
            y = pg.evaluate("id => { const s = document.getElementById(id); return s ? s.getBoundingClientRect().top + scrollY - 80 : 0; }", sid)
            pg.evaluate("y => window.scrollTo(0, y)", y); time.sleep(1); pg.screenshot(path=os.path.join(SH, "live-m-%s-%s.png" % (sid, tag)))
        y = pg.evaluate("() => { const s = document.querySelector('.nlx-byline'); return s ? s.getBoundingClientRect().top + scrollY - 500 : 0; }")
        pg.evaluate("y => window.scrollTo(0, y)", y); time.sleep(1); pg.screenshot(path=os.path.join(SH, "live-m-byline-%s.png" % tag))
        o["errors"] = errs; out[tag] = o; ctx.close()
    b.close()
json.dump(out, open(os.path.join(H, "press-live-m.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, o in out.items():
    s = o["start"]; c = o.get("after-mcheck") or {}; z = o.get("after-mzakaut") or {}
    print(k, "| sw:", s["sw"], "| mcheck:", c.get("mcheck"), "| mzakaut:", z.get("mzakaut"), "| mnomeff:", s["mnomeff"], "| chapters:", s["before"], s["elig"], s["method"],
          "| faq:", s["faq"], "| byline:", s["bylineVisible"], "after:", s["afterByline"], "| h1:", s["h1"], "| hs:", max(s["hs"], c.get("hs", 0), z.get("hs", 0)), "| errors:", o["errors"][:3])
    print("   converter:", (o.get("mnomeff_text") or "").replace("\n", " ")[:200])
