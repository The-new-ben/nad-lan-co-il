"""Read-only probe of the live Rainbow stage: which controls exist (floor, facing, view), which events fire."""
import json, sys, os
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]
URL = "https://nad-lan.co.il/projects/rainbow-tel-aviv/"
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 1920, "height": 1080}, locale="he-IL")
    resp = pg.goto(URL, wait_until="domcontentloaded", timeout=120000)
    print("status", resp.status)
    pg.evaluate("""() => { window.__ev = []; for (const n of ['nl:floor','nl:facing','nl:view','nl:unit','nl:tour']) window.addEventListener(n, e => window.__ev.push([n, JSON.stringify(e.detail||null)])); }""")
    pg.wait_for_selector("section#nlps", timeout=60000)
    pg.evaluate("() => document.querySelector('section#nlps').scrollIntoView({block:'center'})")
    pg.wait_for_timeout(9000)
    info = pg.evaluate("""() => {
      const s = document.querySelector('section#nlps'); const r = s.getBoundingClientRect();
      const ctl = [...s.querySelectorAll('button, [role=button], select, input, a, [data-floor], [data-facing], [data-dir]')].slice(0, 200).map(e => ({tag: e.tagName, cls: (e.className && e.className.baseVal === undefined ? e.className : ''), txt: (e.innerText||e.getAttribute('aria-label')||'').trim().slice(0,60), data: Object.assign({}, e.dataset), vis: e.getBoundingClientRect().width > 0}));
      return {rect: [r.x, r.y, r.width, r.height], ctl, html: s.outerHTML.length};
    }""")
    json.dump(info, open(os.path.join(OUT, "stage_probe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pg.screenshot(path=os.path.join(OUT, "probe_page.png"))
    html = pg.evaluate("() => document.querySelector('section#nlps').outerHTML")
    open(os.path.join(OUT, "stage.html"), "w", encoding="utf-8").write(html)
    # scripts that mention nl:floor
    srcs = pg.evaluate("() => [...document.scripts].map(s => s.src).filter(Boolean)")
    json.dump(srcs, open(os.path.join(OUT, "scripts.json"), "w"), indent=1)
    print("events so far", pg.evaluate("window.__ev"))
    b.close()
