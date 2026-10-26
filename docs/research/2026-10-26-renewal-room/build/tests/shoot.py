# -*- coding: utf-8 -*-
"""RenewalRoomPro screenshots and checks (local only; the preview server must run:
   php -S 127.0.0.1:8765 build/preview/server.php).

   python build/tests/shoot.py            -> build/shots/*.png + build/shots/checks.json

For every screen at 390 and 1280 px: console errors and page errors, sideways scroll (scrollWidth vs clientWidth),
the contrast of every visible enabled button / button-link (text colour vs the first opaque background behind it, WCAG
ratio, must be >= 4.5), and right-to-left order (the first tab sits right of the last one, the room's direction is rtl).
"""
import json, os, sys, datetime
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(HERE)
OUT = os.path.join(B, "shots")
os.makedirs(OUT, exist_ok=True)
BASE = os.environ.get("RR_BASE", "http://127.0.0.1:8765")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CHECK_JS = r"""
() => {
  function rgb(s){ const m = s.match(/rgba?\(([^)]+)\)/); if(!m) return null; const p = m[1].split(',').map(x=>parseFloat(x)); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}; }
  function lum(c){ const f = v => { v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4); }; return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); }
  function bgOf(el){ while(el){ const s = getComputedStyle(el); const c = rgb(s.backgroundColor); if(c && c.a > 0.5) return c; el = el.parentElement; } return {r:255,g:255,b:255,a:1}; }
  const out = { buttons: 0, min: 99, fails: [] };
  const els = [...document.querySelectorAll('.rrp button, .rrp a.rrp-btn, .rrp a.rrp-wa, .nlurd a.nlurl-cta, .nlurd button')];
  for (const el of els) {
    if (el.disabled) continue;
    const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 2) continue;
    const st = getComputedStyle(el); if (st.visibility === 'hidden' || st.display === 'none' || parseFloat(st.opacity) < 0.3) continue;
    let t = el;
    const span = el.querySelector('span'); if (span && span.textContent.trim() && !([...el.childNodes].some(n => n.nodeType===3 && n.textContent.trim()))) t = span;
    if (!t.textContent.trim()) continue;
    const fg = rgb(getComputedStyle(t).color), bg = bgOf(t);
    const L1 = lum(fg), L2 = lum(bg), ratio = (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
    out.buttons++; if (ratio < out.min) out.min = ratio;
    if (ratio < 4.5) out.fails.push({ text: t.textContent.trim().slice(0,30), cls: el.className, ratio: Math.round(ratio*100)/100, fg: getComputedStyle(t).color, bg: `rgb(${bg.r},${bg.g},${bg.b})` });
  }
  out.min = Math.round(out.min*100)/100;
  const de = document.documentElement;
  out.scrollW = de.scrollWidth; out.clientW = de.clientWidth; out.overflow = de.scrollWidth > de.clientWidth + 1;
  const wide = []; document.querySelectorAll('body *').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && (r.right > de.clientWidth + 1 || r.left < -1)) { let p = e.parentElement, clipped = false; while (p) { const o = getComputedStyle(p).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden') { clipped = true; break; } p = p.parentElement; } if (!clipped) wide.push((e.className || e.tagName).toString().slice(0,40) + ' ' + Math.round(r.left) + '..' + Math.round(r.right)); } });
  out.unclipped_wide = wide.slice(0, 8);
  const room = document.querySelector('.rrp'); out.dir = room ? getComputedStyle(room).direction : null;
  const tabs = [...document.querySelectorAll('.rrp-tab')];
  out.rtl_tabs_ok = tabs.length < 2 ? null : tabs[0].getBoundingClientRect().left > tabs[tabs.length-1].getBoundingClientRect().left;
  out.fonts = [...new Set([...document.querySelectorAll('.rrp h2, .rrp .num, .rrp-tab')].slice(0,40).map(e => getComputedStyle(e).fontFamily.split(',')[0]))];
  out.h1 = document.querySelectorAll('h1').length;
  return out;
}
"""

def shoot(p, name, url, width, prep=None, element=None, full=True):
    b = p.chromium.launch(executable_path=CHROME, headless=True)
    ctx = b.new_context(viewport={"width": width, "height": 900 if width > 600 else 844}, device_scale_factor=1, locale="he-IL")
    page = ctx.new_page()
    errs = []
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
    page.clock.set_fixed_time(datetime.datetime(2026, 10, 26, 10, 0, 0))
    page.goto(BASE + url, wait_until="networkidle", timeout=60000)
    page.wait_for_selector(".rrp, .nlurl-hero", timeout=30000)
    page.wait_for_timeout(600)
    if prep:
        prep(page)
        page.wait_for_timeout(500)
    page.evaluate("document.fonts.ready")
    info = page.evaluate(CHECK_JS)
    # model-viewer / fonts may log network noise; keep everything, the report says what it is
    info["console_errors"] = [e for e in errs]
    fn = f"{name}-{width}.png"
    if element:
        page.locator(element).first.screenshot(path=os.path.join(OUT, fn))
        page.screenshot(path=os.path.join(OUT, f"{name}-{width}-page.png"), full_page=True)
    else:
        page.screenshot(path=os.path.join(OUT, fn), full_page=full)
    info["shot"] = fn
    b.close()
    return info

def main():
    ids = json.loads(__import__("urllib.request").request.urlopen(BASE + "/__reset").read())
    A = ids["a"]
    def open_apt(page):
        page.locator('[data-apt="b2-f3-4"]').click()          # a partial apartment: marked signed, one owner unsigned
        page.wait_for_selector("[data-ed-log] time", timeout=15000)
        page.evaluate("() => { const d = document.querySelector('[data-drawer]'); d.style.maxHeight = 'none'; d.style.position = 'static'; }")
    def tab(k):
        return lambda page: page.locator(f'[data-tab="{k}"]').click()
    plan = [
        ("rrp-portfolio", "/room.html?as=staff", None, None),
        ("rrp-complex", f"/room.html?as=staff&space={A}", None, None),
        ("rrp-drawer", f"/room.html?as=staff&space={A}", open_apt, "[data-drawer]"),
        ("rrp-report", f"/room.html?as=staff&space={A}", tab("report"), None),
        ("rrp-updates", f"/room.html?as=staff&space={A}", tab("updates"), None),
        ("rrp-neighbor", f"/room.html?as=neighbor&space={A}", None, None),
        ("rrp-neighbor-pending", f"/room.html?as=pending&space={A}", None, None),
        ("rrp-committee", f"/room.html?as=committee&space={A}", None, None),
        ("rrp-landing", "/room.html?as=anon", None, None),
        ("rrp-complex-en", f"/room.html?as=staff&space={A}&lang=en", None, None),
        ("rrp-complex-ru", f"/room.html?as=staff&space={A}&lang=ru", None, None),
    ]
    only = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    report = {}
    with sync_playwright() as p:
        for name, url, prep, el in plan:
            if only and name not in only:
                continue
            for w in (390, 1280):
                info = shoot(p, name, url, w, prep, el)
                report[f"{name}-{w}"] = info
                print(f"{name}-{w}: buttons={info['buttons']} min_contrast={info['min']} fails={len(info['fails'])} overflow={info['overflow']} dir={info['dir']} rtl_tabs={info['rtl_tabs_ok']} errors={len(info['console_errors'])}")
    path = os.path.join(OUT, "checks.json")
    old = json.load(open(path, encoding="utf-8")) if (only and os.path.exists(path)) else {}
    old.update(report)
    json.dump(old, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
