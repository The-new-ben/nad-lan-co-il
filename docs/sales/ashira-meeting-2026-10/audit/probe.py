# -*- coding: utf-8 -*-
"""Read-only probe: every visible element with cursor:pointer (clickable) anywhere on the page, with its nearest id
section, class, text and y. Output probe-<page>-<w>.txt"""
import os, sys, time
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = {"A": "https://nad-lan.co.il/projects/ashira-sde-dov/", "B": "https://nad-lan.co.il/projects/rainbow-tel-aviv/"}
JS = r"""
() => {
  const sy = window.scrollY, out = [];
  const sec = el => { let p = el; while (p && p !== document.body) { if (p.id) return p.id; p = p.parentElement; } return ''; };
  document.querySelectorAll('body *').forEach(e => {
    const s = getComputedStyle(e); if (s.cursor !== 'pointer') return;
    const pc = e.parentElement ? getComputedStyle(e.parentElement).cursor : '';
    if (pc === 'pointer' && !(e.matches('button,a,[role=button],[data-floor],[data-nlps-floor]'))) return; // only outermost clickable
    const r = e.getBoundingClientRect(); if (r.width < 4 || r.height < 4 || s.visibility === 'hidden' || s.display === 'none') return;
    const da = [...e.attributes].filter(a => a.name.startsWith('data-') || a.name==='aria-label' || a.name==='href').map(a => a.name + '=' + a.value.slice(0,60)).join(' ');
    out.push([Math.round(r.top + sy), Math.round(r.left), sec(e), e.tagName, (e.className && e.className.baseVal === undefined ? e.className : '').toString().slice(0,50), (e.innerText||'').trim().replace(/\s+/g,' ').slice(0,50), da.slice(0,160)].join(' | '));
  });
  return out;
}
"""
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for key in sys.argv[1:]:
        k, tag = key.split("-")
        w, h = (1440, 900) if tag == "d" else (390, 844)
        c = b.new_context(viewport={"width": w, "height": h}, locale="he-IL")
        pg = c.new_page()
        pg.goto(PAGES[k] + f"?nlaudit={int(time.time())}", wait_until="load", timeout=120000)
        pg.wait_for_timeout(9000)
        H = pg.evaluate("document.body.scrollHeight"); y = 0
        while y < H:
            y += 700; pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(200); H = pg.evaluate("document.body.scrollHeight")
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(1500)
        rows = pg.evaluate(JS)
        open(os.path.join(HERE, f"probe-{key}.txt"), "w", encoding="utf-8").write("\n".join(rows))
        print(key, len(rows))
        c.close()
    b.close()
