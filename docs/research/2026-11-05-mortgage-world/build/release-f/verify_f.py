# -*- coding: utf-8 -*-
"""Round F local check: the live page with the v2 folding block swapped in (route interception), phone 390x844 and desktop 1280.
Measures page height, folded chapters, FAQ list, the open-chapter button, console errors, horizontal scroll; screenshots in shots/.
  python verify_f.py            (v2 swapped in)
  python verify_f.py --live     (the page as it is live, no swap)"""
import json, os, re, sys, time
from playwright.sync_api import sync_playwright
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); SH = os.path.join(H, "shots"); os.makedirs(SH, exist_ok=True)
LIVE = "--live" in sys.argv
EN = "--en" in sys.argv
URL = "https://nad-lan.co.il/en/mortgage-calculator/" if EN else "https://nad-lan.co.il/mortgage-calculator/"
NEW = open(os.path.join(H, "fold-en.html" if EN else "fold-f.html"), encoding="utf-8").read()
NEW_CSS = re.search(r'<style id="nlmx-fold-css">.*?</style>', NEW, re.S).group(0)
NEW_JS = re.search(r'<script id="nlmx-fold-js">.*?</script>', NEW, re.S).group(0)
tag = ("en-" if EN else "") + ("live" if LIVE else "f")


def swap(route):
    resp = route.fetch()
    body = resp.text()
    if not LIVE and EN:
        assert body.count('<section id="faq">') == 1 and 'nlmx-fold-js' not in body
        body = body.replace('<section id="faq">', NEW + '<section id="faq">')
    elif not LIVE:
        a = len(re.findall(r'<style id="nlmx-fold-css">.*?</style>', body, re.S)); b = len(re.findall(r'<script id="nlmx-fold-js">.*?</script>', body, re.S))
        assert a == 1 and b == 1, (a, b)
        body = re.sub(r'<style id="nlmx-fold-css">.*?</style>', lambda m: NEW_CSS, body, flags=re.S)
        body = re.sub(r'<script id="nlmx-fold-js">.*?</script>', lambda m: NEW_JS, body, flags=re.S)
    route.fulfill(response=resp, body=body, headers={**resp.headers, "content-type": "text/html; charset=UTF-8"})


def run(p, w, h, mobile):
    b = p.chromium.launch(channel="chrome", headless=True)
    kw = dict(viewport={"width": w, "height": h})
    if mobile:
        kw.update(is_mobile=True, has_touch=True, user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36")
    ctx = b.new_context(**kw); pg = ctx.new_page(); errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
    u = URL + "?vf=%d" % time.time()
    pg.route(re.compile(r"https://nad-lan\.co\.il/(en/)?mortgage-calculator/\?vf="), swap)
    pg.goto(u, wait_until="networkidle", timeout=90000); time.sleep(2.5)
    r = pg.evaluate("""() => { const f = [...document.querySelectorAll('.nlmx-folded')];
      const faq = document.getElementById('faq');
      return {height: document.documentElement.scrollHeight, hscroll: document.documentElement.scrollWidth - innerWidth,
        folded: f.length, foldedIds: f.map(s => (s.id || (s.querySelector(':scope>h2') || {}).textContent || '').trim().slice(0, 40)),
        buttons: document.querySelectorAll('.nlmx-more').length, faqH: faq ? Math.round(faq.getBoundingClientRect().height) : null,
        faqQ: faq ? faq.querySelectorAll('h3.nlmx-q').length : null,
        words: (document.querySelector('.entry-content') || document.body).textContent.replace(/\\s+/g, ' ').length}; }""")
    if mobile:
        # open one folded chapter and one FAQ answer: both must show their text
        r["open"] = pg.evaluate("""async () => { const s = document.querySelector('.nlmx-folded'); if (!s) return null; const b = s.querySelector('.nlmx-more');
          const before = Math.round(s.getBoundingClientRect().height); b.click(); await new Promise(r => setTimeout(r, 200));
          const q = document.querySelector('#faq h3.nlmx-q'); q.click(); await new Promise(r => setTimeout(r, 200));
          const a = q.nextElementSibling; return {chapterBefore: before, chapterAfter: Math.round(s.getBoundingClientRect().height), stillFolded: s.classList.contains('nlmx-folded'),
            faqOpen: q.getAttribute('aria-expanded'), answerShown: !a.hidden && a.offsetHeight > 0}; }""")
        pg.evaluate("() => { const s = document.querySelectorAll('.nlmx-folded')[2]; if (s) window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 90); }"); time.sleep(1.5)
        pg.screenshot(path=os.path.join(SH, tag + "-phone-fold.png"))
        pg.evaluate("() => { const f = document.getElementById('faq'); window.scrollTo(0, f.getBoundingClientRect().top + scrollY - 90); }"); time.sleep(1.5)
        pg.screenshot(path=os.path.join(SH, tag + "-phone-faq.png"))
    r["errors"] = errs
    b.close()
    return r


with sync_playwright() as p:
    out = {"phone": run(p, 390, 844, True), "desktop": run(p, 1280, 900, False)}
print(json.dumps(out, ensure_ascii=False, indent=1))
json.dump(out, open(os.path.join(H, "verify-%s.json" % tag), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
