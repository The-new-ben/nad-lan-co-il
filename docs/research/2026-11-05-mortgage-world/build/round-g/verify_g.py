# -*- coding: utf-8 -*-
"""Round G check (T8): the live pages with the repo's mquick.js v5 served in place of the live file (route), or the live file (--live).
Phone 390x844 and desktop 1280: the two fields start empty, the total is hidden; typing 250 and 600 shows payment + 850 with a
three-part breakdown; emptying one field leaves two parts; the "by payment" mode adds the costs to the typed payment; English page
the same; the mounted height per width (for the page's min-height reserve); console errors; horizontal scroll. Screenshots in shots/."""
import json, os, re, sys, time
from playwright.sync_api import sync_playwright
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); SH = os.path.join(H, "shots"); os.makedirs(SH, exist_ok=True)
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", "..", ".."))
JS = open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "tools", "mquick.js"), encoding="utf-8").read()
LIVE = "--live" in sys.argv
tag = "live" if LIVE else "g"


def page(p, url, w, mob):
    b = p.chromium.launch(channel="chrome", headless=True)
    ctx = b.new_context(viewport={"width": w, "height": 844 if mob else 900}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if w == 390 else 1)
    pg = ctx.new_page(); errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "tawk" not in m.text and "ERR_FAILED" not in m.text else None)
    pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
    if not LIVE:
        pg.route(re.compile(r".*/instruments/tools/mquick\.js.*"), lambda r: r.fulfill(status=200, body=JS, headers={"content-type": "application/javascript; charset=utf-8"}))
    pg.goto(url + "?vg=%d" % time.time(), wait_until="load", timeout=90000); time.sleep(3)
    return b, pg, errs


def typ(pg, sel, val):
    pg.fill(sel, ""); pg.type(sel, val); time.sleep(0.25)


R = """() => { const q = s => document.querySelector(s); const t = q('#nlmq .nlmq__tot');
  return {ins: q('#nlmq-xi').value, arn: q('#nlmq-xa').value, totHidden: t.hidden, fig: q('#nlmq .nlmq__fig').textContent.trim(),
          tf: q('#nlmq .nlmq__tf').textContent.trim(), tb: q('#nlmq .nlmq__tb').textContent.trim(), sub: q('#nlmq .nlmq__sub').textContent.trim(),
          labels: [...document.querySelectorAll('#nlmq .nlmq__x2 label')].map(l => l.textContent), note: q('#nlmq .nlmq__xn').textContent.slice(0, 90),
          links: [...document.querySelectorAll('#nlmq .nlmq__xn a')].map(a => a.href), h: Math.round(q('#nlmq').getBoundingClientRect().height),
          hscroll: document.documentElement.scrollWidth - innerWidth}; }"""
out = {}
with sync_playwright() as p:
    for url, key in (("https://nad-lan.co.il/mortgage-calculator/", "he"), ("https://nad-lan.co.il/en/mortgage-calculator/", "en")):
        b, pg, errs = page(p, url, 390, True)
        o = {"start": pg.evaluate(R)}
        typ(pg, "#nlmq-xi", "250"); typ(pg, "#nlmq-xa", "600"); o["typed"] = pg.evaluate(R)
        pg.focus("#nlmq-a"); time.sleep(0.2)
        y = pg.evaluate("() => document.querySelector('#nlmq .nlmq__out').getBoundingClientRect().top + scrollY - 70")
        pg.evaluate("y => window.scrollTo(0, y)", y); time.sleep(1.2); pg.screenshot(path=os.path.join(SH, "%s-%s-phone-total.png" % (tag, key)))
        typ(pg, "#nlmq-xi", ""); o["one"] = pg.evaluate(R)
        pg.click('#nlmq button[data-m="pay"]'); time.sleep(0.3); o["paymode"] = pg.evaluate(R)
        typ(pg, "#nlmq-xa", ""); o["cleared"] = pg.evaluate(R)
        o["errors"] = errs; b.close()
        heights = {}
        for w in (360, 375, 390, 412, 430, 600, 768, 1024, 1280):
            b, pg, e2 = page(p, url, w, w < 600)
            heights[w] = pg.evaluate("() => Math.round(document.querySelector('[data-nli=\"mquick\"]').getBoundingClientRect().height)"); b.close()
        o["mounted"] = heights
        out[key] = o
print(json.dumps(out, ensure_ascii=False, indent=1))
json.dump(out, open(os.path.join(H, "verify-%s.json" % tag), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
