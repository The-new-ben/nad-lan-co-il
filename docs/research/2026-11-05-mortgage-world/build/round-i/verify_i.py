# -*- coding: utf-8 -*-
"""Round I check: the live page with the ten answer-first paragraphs injected after their headings (route), or the live page (--live).
Phone 390x844: page height, the new paragraph is the visible first paragraph of each folded chapter, links resolve on the site,
console errors, horizontal scroll; screenshot of two chapters."""
import json, os, re, sys, time
from playwright.sync_api import sync_playwright
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); SH = os.path.join(H, "shots"); os.makedirs(SH, exist_ok=True)
A = json.load(open(os.path.join(H, "answers.json"), encoding="utf-8"))
LIVE = "--live" in sys.argv; tag = "live" if LIVE else "i"
def swap(route):
    resp = route.fetch(); body = resp.text()
    if not LIVE:
        for a in A:
            pat = re.compile(r'(<h2[^>]*>\s*' + re.escape(a["h2"]) + r'\s*</h2>)'); assert len(pat.findall(body)) == 1, a["h2"]
            body = pat.sub(lambda m: m.group(1) + '<p class="nlx-ans">' + a["p"] + '</p>', body, count=1)
    route.fulfill(response=resp, body=body, headers={**resp.headers, "content-type": "text/html; charset=UTF-8"})
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    pg = ctx.new_page(); errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "tawk" not in m.text and "ERR_FAILED" not in m.text else None)
    pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
    pg.route(re.compile(r"https://nad-lan\.co\.il/mortgage-calculator/\?vi="), swap)
    pg.goto("https://nad-lan.co.il/mortgage-calculator/?vi=%d" % time.time(), wait_until="load", timeout=90000); time.sleep(3)
    r = pg.evaluate("""() => { const ans = [...document.querySelectorAll('p.nlx-ans')];
      return {height: document.documentElement.scrollHeight, hscroll: document.documentElement.scrollWidth - innerWidth, n: ans.length,
        visible: ans.filter(p => p.offsetHeight > 0).length, keep: ans.filter(p => p.classList.contains('nlmx-keep')).length,
        folded: document.querySelectorAll('.nlmx-folded').length,
        links: ans.flatMap(p => [...p.querySelectorAll('a')].map(a => a.getAttribute('href')))}; }""")
    for i, h in enumerate(("איך בודקים עלות כוללת לפני חתימה?", "איך להשוות בין שתי הצעות בנק?")):
        y = pg.evaluate("t => { const h = [...document.querySelectorAll('h2')].find(x => x.textContent.trim() === t); return h.getBoundingClientRect().top + scrollY - 90; }", h)
        pg.evaluate("y => window.scrollTo(0, y)", y); time.sleep(1.3); pg.screenshot(path=os.path.join(SH, "%s-phone-%d.png" % (tag, i)))
    r["errors"] = errs; b.close()
print(json.dumps(r, ensure_ascii=False, indent=1))
