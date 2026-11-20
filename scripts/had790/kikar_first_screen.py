# -*- coding: utf-8 -*-
"""HAD-790 (20.11.2026, Ben: the Kikar first paragraph must always be there): the first screen of the Kikar pages, cold.
  python kikar_first_screen.py before|after [base_url_suffix]
Hebrew and English Kikar pages, a 390 px phone and a 1440 desktop, each in a fresh context with the cache off (Chrome DevTools
Network.setCacheDisabled). Records the layout shift (CLS, every shift without recent input, buffered from the first paint), where the
title, the paragraph, the buttons and the showroom end up, and two screenshots of the first screen: early (domcontentloaded + 400 ms)
and settled (load + 5 s). Output: docs/qa/had-790/kikar-first/<tag>/ (png + result.json)."""
import os, sys, json, time
from playwright.sync_api import sync_playwright

TAG = sys.argv[1] if len(sys.argv) > 1 else "before"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "qa", "had-790", "kikar-first", TAG)
os.makedirs(OUT, exist_ok=True)
PAGES = [("he", "/projects/hamedina/"), ("en", "/projects/hamedina-en/")]
DEV = [("phone390", dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)),
       ("desk1440", dict(viewport={"width": 1440, "height": 900}))]
INIT = """window.__cls = 0; window.__shifts = [];
try { new PerformanceObserver(l => { for (const e of l.getEntries()) { if (e.hadRecentInput) continue; window.__cls += e.value;
  window.__shifts.push({t: Math.round(e.startTime), v: +e.value.toFixed(4), n: (e.sources || []).map(s => s.node && s.node.nodeType === 1 ? (s.node.id || s.node.className || s.node.tagName).toString().slice(0, 40) : '').join('|')}); } })
  .observe({type: 'layout-shift', buffered: true}); } catch (e) {}"""
POS = """() => { const T = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return r.height ? Math.round(r.top + scrollY) : null; };
  const fcp = (performance.getEntriesByName('first-contentful-paint')[0] || {}).startTime;
  return { h1: T('h1'), lead: T('.nl-lead'), cta: T('.nlps-ctawrap'), showroom: T('#nlsr'), showroomReal: !!document.querySelector('.nlsr'), map: T('#nlpjx-map'),
           cls: +(window.__cls || 0).toFixed(4), shifts: (window.__shifts || []).slice(0, 12), fcp: fcp ? Math.round(fcp) : null, vh: innerHeight }; }"""
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kikar_route import LOCAL, precheck_routes  # noqa: E402


res = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for dev, o in DEV:
        for lang, path in PAGES:
            ctx = b.new_context(**o)
            ctx.add_init_script(INIT)
            if LOCAL:
                precheck_routes(ctx, lang)
            pg = ctx.new_page()
            cdp = ctx.new_cdp_session(pg)
            cdp.send("Network.enable"); cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
            url = "https://nad-lan.co.il" + path + "?kf=%d" % time.time()
            pg.goto(url, wait_until="domcontentloaded", timeout=120000)
            pg.wait_for_timeout(400)
            name = "%s-%s" % (dev, lang)
            pg.screenshot(path=os.path.join(OUT, name + "-early.png"))
            early = pg.evaluate(POS)
            pg.wait_for_load_state("load", timeout=120000)
            pg.wait_for_timeout(5000)
            pg.screenshot(path=os.path.join(OUT, name + "-settled.png"))
            late = pg.evaluate(POS)
            row = dict(device=dev, lang=lang, page=path, early=early, settled=late)
            res.append(row)
            print(json.dumps(dict(device=dev, lang=lang, cls=late["cls"], fcp=late["fcp"], early={k: early[k] for k in ("h1", "lead", "showroom")},
                                  settled={k: late[k] for k in ("h1", "lead", "cta", "showroom", "map")}, shifts=late["shifts"][:6]), ensure_ascii=False))
            ctx.close()
            time.sleep(1)
    b.close()
json.dump(res, open(os.path.join(OUT, "result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
