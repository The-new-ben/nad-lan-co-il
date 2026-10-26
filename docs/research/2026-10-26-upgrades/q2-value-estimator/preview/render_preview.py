# -*- coding: utf-8 -*-
"""Render preview/index.html (the real engine core.css + core.js, the real tools/pval.js, the real data inline) in Chrome at 390 and
1280 px, press every control of every case, and report: sideways scroll, console errors and page errors, the result of every case
after the presses, and the screenshots (full page + the V10 case + the asking-price case).
  python docs/research/2026-10-26-upgrades/q2-value-estimator/preview/render_preview.py"""
import json
import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(H, "index.html").replace("\\", "/")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# the print and copy buttons call window.print() and the clipboard; in a headless run they are replaced by recorders
INIT = "window.__printed=0;window.print=function(){window.__printed++};try{Object.defineProperty(navigator,'clipboard',{value:{writeText:function(t){window.__copied=t;return Promise.resolve()}}})}catch(e){}"

PRESS = r"""
async (hid) => {
  const wait = (ms) => new Promise(r => setTimeout(r, ms));
  const host = document.getElementById(hid); const log = [];
  const settle = async () => { await wait(130); };
  const vis = (e) => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length) && !e.closest('[hidden]');
  // presets
  for (const b of [...host.querySelectorAll('.nli__pre button')]) { b.click(); await settle(); log.push('preset ' + b.getAttribute('data-k')); }
  // segmented groups: every button, then back to the first pressed state
  const groups = [...host.querySelectorAll('.nli__seg')];
  for (let gi = 0; gi < groups.length; gi++) {
    const g = host.querySelectorAll('.nli__seg')[gi]; if (!g || !vis(g)) continue;
    const btns = [...g.querySelectorAll('button')]; const was = btns.findIndex(b => b.getAttribute('aria-pressed') === 'true');
    for (const b of btns) { b.click(); await settle(); }
    if (was >= 0) { btns[was].click(); await settle(); }
    log.push('seg ' + g.getAttribute('aria-label') + ' x' + btns.length);
  }
  // selects: the second option, the last, then back
  for (const s of [...host.querySelectorAll('select')]) {
    if (!vis(s)) continue; const was = s.value; const n = s.options.length;
    for (const i of [1, n - 1]) { if (i > 0 && i < n) { s.selectedIndex = i; s.dispatchEvent(new Event('change', { bubbles: true })); await settle(); } }
    s.value = was; s.dispatchEvent(new Event('change', { bubbles: true })); await settle(); log.push('select ' + s.id.split('-').pop() + ' x' + n);
  }
  // a purchase year opens the month and price fields: press them too
  const by = [...host.querySelectorAll('select')].find(s => /-buyY$/.test(s.id));
  if (by && by.options.length > 6) {
    const wasY = by.value; by.value = '2021'; by.dispatchEvent(new Event('change', { bubbles: true })); await settle();
    const bm = [...host.querySelectorAll('select')].find(s => /-buyM$/.test(s.id)); const bp = [...host.querySelectorAll('input')].find(s => /-bought$/.test(s.id));
    if (bm) { const wm = bm.value; bm.value = '3'; bm.dispatchEvent(new Event('change', { bubbles: true })); await settle(); log.push('buyM'); if (bp) { const wp = bp.value; bp.value = '1,500,000'; bp.dispatchEvent(new Event('input', { bubbles: true })); await settle(); log.push('bought'); bp.value = wp; bp.dispatchEvent(new Event('input', { bubbles: true })); await settle(); } bm.value = wm; bm.dispatchEvent(new Event('change', { bubbles: true })); await settle(); }
    by.value = wasY; by.dispatchEvent(new Event('change', { bubbles: true })); await settle();
  }
  // text inputs: a value, then back
  for (const i of [...host.querySelectorAll('input')]) {
    if (!vis(i)) continue; const was = i.value;
    i.value = '3'; i.dispatchEvent(new Event('input', { bubbles: true })); await settle();
    i.value = was; i.dispatchEvent(new Event('input', { bubbles: true })); i.dispatchEvent(new Event('blur')); await settle(); log.push('input ' + i.id.split('-').pop());
  }
  for (const b of [...host.querySelectorAll('.nli__scen button')]) { b.click(); await settle(); }
  log.push('scenarios x' + host.querySelectorAll('.nli__scen button').length);
  const sum = host.querySelector('.nli__table summary'); if (sum && vis(sum)) { sum.click(); await settle(); sum.click(); await settle(); log.push('table'); }
  const share = host.querySelectorAll('.nli__share > *');
  if (share[0]) { share[0].click(); await wait(200); log.push('copy ' + (window.__copied ? 'ok' : 'none')); }
  if (share[1]) { share[1].addEventListener('click', e => e.preventDefault(), { once: true }); share[1].click(); log.push('whatsapp ' + (share[1].href.indexOf('https://wa.me/?text=') === 0 ? 'ok' : share[1].href)); }
  if (share[2]) { share[2].click(); log.push('print ' + window.__printed); }
  // after the presses the host holds the last preset's case; the answer and any field error are reported
  const ans = host.querySelector('.nli__fig'); const errs = [...host.querySelectorAll('.nli__err')].map(e => e.textContent).filter(Boolean);
  return { log, answer: ans ? ans.textContent : null, errs, svgs: host.querySelectorAll('.nli__figure svg').length };
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    report = {}
    for w in (390, 1280):
        ctx = b.new_context(viewport={"width": w, "height": 900}, device_scale_factor=1 if w > 400 else 2)
        ctx.add_init_script(INIT)
        ctx.route("https://wa.me/**", lambda r: r.abort())
        pg = ctx.new_page()
        errs = []
        pg.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
        pg.goto(URL)
        pg.wait_for_timeout(1800)
        tag = "p" if w < 500 else "d"
        pg.screenshot(path=os.path.join(H, "shot-%s-full.png" % tag), full_page=True)
        for hid, name in (("h1", "v10"), ("h2", "ask"), ("h5", "house")):
            pg.locator("#" + hid).screenshot(path=os.path.join(H, "shot-%s-%s.png" % (tag, name)))
        first = pg.evaluate("[...document.querySelectorAll('.nli-host')].map(h => { const f = h.querySelector('.nli__fig'); return [h.id, f ? f.textContent : null, h.querySelectorAll('.nli__figure svg').length]; })")
        over = pg.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
        wide = pg.evaluate("[...document.querySelectorAll('.nli-host *')].filter(e => e.getBoundingClientRect().right > document.documentElement.clientWidth + 1).slice(0, 5).map(e => e.tagName + '.' + e.className)")
        pressed = {}
        for hid in [x[0] for x in first]:
            pressed[hid] = pg.evaluate(PRESS, hid)
        over2 = pg.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
        report[w] = {"opening": first, "overflow_x": over, "overflow_x_after_presses": over2, "wider_than_viewport": wide, "pressed": pressed, "console": errs, "height": pg.evaluate("document.body.scrollHeight")}
        ctx.close()
    b.close()
json.dump(report, open(os.path.join(H, "render-report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for w, r in report.items():
    print("== %d px: height %d, overflow-x %s / after presses %s, console %s" % (w, r["height"], r["overflow_x"], r["overflow_x_after_presses"], r["console"] or "none"))
    if r["wider_than_viewport"]:
        print("   wider than the viewport:", r["wider_than_viewport"])
    for hid, ans, n in r["opening"]:
        x = r["pressed"][hid]
        print("   %s opening %s, %d drawings | after %d presses: %s, errors %s" % (hid, ans, n, len(x["log"]), x["answer"], x["errs"] or "none"))
    print("   controls:", "; ".join(r["pressed"]["h1"]["log"]))
