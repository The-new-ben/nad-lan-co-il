# -*- coding: utf-8 -*-
"""Read-only discovery for the Ashira vs Rainbow audit.
Loads each page at each width, dumps: section order (y), every interactive control (tag, id, class, text, y, visible),
console errors and failed requests. No clicks. Output: discover-<page>-<w>.json"""
import os, json, time
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = {"A": "https://nad-lan.co.il/projects/ashira-sde-dov/", "B": "https://nad-lan.co.il/projects/rainbow-tel-aviv/"}
WIDTHS = [(1440, 900, "d"), (390, 844, "m")]

JS = r"""
() => {
  const sy = window.scrollY;
  const box = el => { const r = el.getBoundingClientRect(); return {y: Math.round(r.top + sy), h: Math.round(r.height), x: Math.round(r.left), w: Math.round(r.width)}; };
  const vis = el => { const s = getComputedStyle(el); const r = el.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0; };
  const sec = el => { let p = el; while (p && p !== document.body) { if (p.id) return p.id; p = p.parentElement; } return ''; };
  const out = {title: document.title, h1: [], lead: [], sections: [], controls: [], ids: []};
  document.querySelectorAll('h1').forEach(e => out.h1.push({t: e.innerText.trim().slice(0,200), ...box(e), v: vis(e)}));
  document.querySelectorAll('.nl-lead').forEach(e => out.lead.push({t: e.innerText.trim().slice(0,300), ...box(e), v: vis(e)}));
  document.querySelectorAll('[id]').forEach(e => { if (vis(e)) { const b = box(e); if (b.h > 60) out.ids.push({id: e.id, tag: e.tagName, cls: (e.className && e.className.baseVal === undefined ? e.className : '').toString().slice(0,80), ...b}); } });
  document.querySelectorAll('section, [class*="nlps"], [class*="nlpjx"]').forEach(e => { if (e.id && vis(e)) out.sections.push({id: e.id, ...box(e)}); });
  const sel = 'button, a[href^="#"], a[href*="wa.me"], a[href*="whatsapp"], [role="button"], [role="tab"], input, select, [data-floor], [data-tower], [data-dir], [data-cat], [data-room], [data-style], [data-unit], [onclick], summary';
  document.querySelectorAll(sel).forEach(e => {
    const attrs = {};
    for (const a of e.attributes) if (a.name.startsWith('data-') || ['id','class','href','type','aria-label','name','value','role'].includes(a.name)) attrs[a.name] = (a.value||'').slice(0,100);
    out.controls.push({tag: e.tagName, sec: sec(e), text: (e.innerText || e.value || e.getAttribute('aria-label') || '').trim().replace(/\s+/g,' ').slice(0,80), attrs, ...box(e), v: vis(e)});
  });
  return out;
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for key, url in PAGES.items():
        for w, h, tag in WIDTHS:
            c = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, locale="he-IL")
            pg = c.new_page()
            cons, fails, bad = [], [], []
            pg.on("console", lambda m: cons.append({"type": m.type, "text": m.text[:400]}) if m.type in ("error", "warning") else None)
            pg.on("pageerror", lambda e: cons.append({"type": "pageerror", "text": str(e)[:400]}))
            pg.on("requestfailed", lambda r: fails.append({"url": r.url[:300], "err": (r.failure or "")[:200]}))
            pg.on("response", lambda r: bad.append({"url": r.url[:300], "status": r.status}) if r.status >= 400 else None)
            pg.goto(url + f"?nlaudit={int(time.time())}", wait_until="load", timeout=120000)
            pg.wait_for_timeout(8000)
            # scroll the whole page slowly so lazy modules mount
            H = pg.evaluate("document.body.scrollHeight")
            y = 0
            while y < H:
                y += 700
                pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(250)
                H = pg.evaluate("document.body.scrollHeight")
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(1500)
            data = pg.evaluate(JS)
            data.update({"url": url, "width": w, "console": cons, "failed": fails, "bad_status": bad, "scrollHeight": H})
            with open(os.path.join(HERE, f"discover-{key}-{tag}.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=1)
            print(key, tag, "controls", len(data["controls"]), "console", len(cons), "failed", len(fails), "bad", len(bad), "H", H)
            c.close()
    b.close()
