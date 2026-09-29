# -*- coding: utf-8 -*-
"""The buyer's map path, measured (HAD-346, Codex's acceptance for v101.2): pick a unit, press the card's "הנוף והמפה",
wait for the scroll and the map's turn to settle, then measure in CSS pixels of the viewport:
  - the stage, the real map canvas, the cone's marker and its drawn wedge (the <path>, what the buyer sees),
  - every fixed control near the bottom (the wide WhatsApp pill, the accessibility button),
  - overlaps between the wedge and those controls, and whether the wedge is fully inside the viewport under the header,
  - the unit named by the card, by the map's summary (when there is one) and by the ConsultSheet's context,
  - then "back to the building" (when offered) and the stage rectangle before/after the card's fold.
Run through the preview (no deploy, no lead):
  python scripts/project-stage/preview_v101.py "/projects/rainbow-tel-aviv/?unit=13-e" --w 390 --h 844 --probe scripts/project-stage/probe_map_landing.py
Screenshots go to $NL_PROBE_SHOTS (default: the current folder) as landing-<W>.png / back-<W>.png."""
import os

MEASURE = r"""() => {
  const R = (e) => { if (!e) return null; const r = e.getBoundingClientRect(); return { top: +r.top.toFixed(2), bottom: +r.bottom.toFixed(2), left: +r.left.toFixed(2), right: +r.right.toFixed(2) }; };
  const vis = (e) => { if (!e) return false; const cs = getComputedStyle(e); const r = e.getBoundingClientRect(); return cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > 0.05 && r.width > 4 && r.height > 4; };
  const hit = (a, b) => a && b && a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
  const H = innerHeight, W = innerWidth;
  // the site header (sticky/fixed at the top)
  let head = 0;
  document.querySelectorAll('body *').forEach((e) => { const cs = getComputedStyle(e); if ((cs.position === 'fixed' || cs.position === 'sticky') && vis(e)) { const r = e.getBoundingClientRect(); if (r.top <= 1 && r.height < 140 && r.width > W * 0.6) head = Math.max(head, r.bottom); } });
  // fixed controls in the lower part of the viewport (the pill, the accessibility button ...)
  const ctrls = [];
  document.querySelectorAll('body *').forEach((e) => {
    const cs = getComputedStyle(e); if (cs.position !== 'fixed' || !vis(e)) return;
    const r = e.getBoundingClientRect(); if (r.top < H * 0.45 || r.height > 200 || r.width > W * 0.95) return;
    if (e.parentElement && getComputedStyle(e.parentElement).position === 'fixed' && e.parentElement.getBoundingClientRect().top >= H * 0.45) return;
    ctrls.push({ sel: e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : ''), rect: R(e), label: (e.getAttribute('aria-label') || e.textContent || '').trim().slice(0, 40) });
  });
  const canvas = document.querySelector('#nlpjx-unimap .mapboxgl-canvas') || document.querySelector('#nlpjx-unimap');
  const cone = document.querySelector('.nlps-cone'), wedge = cone && cone.querySelector('path');
  const stage = document.querySelector('#nlps');
  const w = R(wedge);
  const inView = !!w && w.top >= head - 0.5 && w.bottom <= H + 0.5 && w.left >= -0.5 && w.right <= W + 0.5;
  const sum = document.querySelector('.nlps-mapsum');
  return {
    viewport: [W, H], header_bottom: +head.toFixed(2), scrollY: Math.round(scrollY),
    stage: R(stage), canvas: R(canvas), cone_marker: R(cone), wedge: w,
    wedge_fully_in_view: inView,
    overlaps: ctrls.filter((c) => hit(c.rect, w)).map((c) => c.sel),
    canvas_hidden_by_controls: ctrls.filter((c) => hit(c.rect, R(canvas))).map((c) => c.sel),
    controls: ctrls,
    stage_to_canvas: stage && canvas ? +(canvas.getBoundingClientRect().top - stage.getBoundingClientRect().bottom).toFixed(2) : null,
    card_title: (document.querySelector('#nlps-pick .rbs-label-title') || {}).textContent || '',
    pick: window.__nlpsPick || null,
    map_summary: sum && vis(sum) ? sum.textContent.replace(/\s+/g, ' ').trim() : null,
    map_summary_rect: sum ? R(sum) : null,
  };
}"""


def run(pg, W, H, mob):
    out_dir = os.environ.get("NL_PROBE_SHOTS", ".")
    if os.environ.get("NL_PROBE_STEP"):
        # the other path: nothing picked, the steps rail's "הנוף והמפה" picks the sea-side example unit, then lands
        pg.evaluate("async () => { const s = window.__nlpsStage; if (s && s.ready) await Promise.race([s.ready, new Promise(r => setTimeout(r, 30000))]); }")
        pg.evaluate("() => { const e = document.querySelector('#nlps'); scrollTo(0, e.getBoundingClientRect().top + scrollY - 70); }")
        pg.wait_for_timeout(2500)
        pg.locator('[data-nlps-step="view"]').first.click()
        pg.wait_for_timeout(3500)
        m = pg.evaluate(MEASURE)
        pg.screenshot(path=os.path.join(out_dir, "step-%d.png" % W))
        return {"step_landing": m}
    pg.evaluate("async () => { const s = window.__nlpsStage; if (s && s.ready) await Promise.race([s.ready, new Promise(r => setTimeout(r, 30000))]); }")
    # phones start the 3D only when the stage is in view
    pg.evaluate("() => { const e = document.querySelector('#nlps'); scrollTo(0, e.getBoundingClientRect().top + scrollY - 70); }")
    pg.wait_for_timeout(2500)
    if not pg.evaluate("() => !!document.querySelector('#nlps-pick .rbs-label.is-on')"):
        pg.evaluate("() => window.__nlpsStage && window.__nlpsStage.selectUnit('13-e', 'user')")
        pg.wait_for_timeout(1200)
    st0 = pg.evaluate("() => { const r = document.querySelector('#nlps').getBoundingClientRect(); return [+(r.top + scrollY).toFixed(2), +r.height.toFixed(2)]; }")
    # the card's fold must not move the stage
    fold = None
    if pg.locator("#nlps-pick .rbs-label-min").count():
        pg.locator("#nlps-pick .rbs-label-min").first.click(); pg.wait_for_timeout(500)
        st1 = pg.evaluate("() => { const r = document.querySelector('#nlps').getBoundingClientRect(); return [+(r.top + scrollY).toFixed(2), +r.height.toFixed(2)]; }")
        pg.locator("#nlps-pick .rbs-label-min").first.click(); pg.wait_for_timeout(500)
        fold = {"before": st0, "folded": st1, "moved": abs(st1[0] - st0[0]) > 0.5 or abs(st1[1] - st0[1]) > 0.5}
    before_title = pg.evaluate("() => (document.querySelector('#nlps-pick .rbs-label-title') || {}).textContent || ''")
    # the explicit action: the card's "הנוף והמפה"
    pg.locator('#nlps-pick .rbs-act[data-act="view"]').first.click()
    pg.wait_for_timeout(3200)
    landing = pg.evaluate(MEASURE)
    pg.screenshot(path=os.path.join(out_dir, "landing-%d.png" % W))
    land_y = pg.evaluate("() => scrollY")
    # free scroll: the cone passes the pill's resting place; the pill rises above it, then rests again once the cone has passed
    ride = pg.evaluate("""async () => {
      const w = document.querySelector('.nlps-cone path'), box = document.getElementById('nlcta'), pill = box && box.querySelector('.nlcta-wa');
      if (!w || !pill) return null;
      const rest = Number(box.getAttribute('data-rest')) || 0, restTop = innerHeight - rest;
      const hit = (a, b) => a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
      const snap = () => { const r = w.getBoundingClientRect(), p = pill.getBoundingClientRect(); return { wedge: [+r.top.toFixed(1), +r.bottom.toFixed(1)], pill: [+p.top.toFixed(1), +p.bottom.toFixed(1)], overlap: hit(r, p), lifted: box.classList.contains('is-cone') }; };
      const go = async (dy) => { window.scrollTo({ top: scrollY + dy, behavior: 'instant' }); await new Promise((r) => setTimeout(r, 450)); };
      await go(w.getBoundingClientRect().top - (restTop + 12));
      const inBand = snap();
      await go(w.getBoundingClientRect().bottom - (restTop - 60));
      const passed = snap();
      return { rest_top: restTop, in_band: inBand, after_pass: passed };
    }""")
    if ride:
        pg.evaluate("() => { const w = document.querySelector('.nlps-cone path'); const box = document.getElementById('nlcta'); const restTop = innerHeight - (Number(box.getAttribute('data-rest')) || 0); window.scrollTo({ top: scrollY + w.getBoundingClientRect().top - (restTop + 12), behavior: 'instant' }); }")
        pg.wait_for_timeout(450)
        pg.screenshot(path=os.path.join(out_dir, "scroll-%d.png" % W))
    # the controls under the map: nothing removed
    ctl = pg.evaluate("""() => { const q = (s) => document.querySelector('#nlpjx-map > ' + s); const b = q('.nlam-bar') || q('.nlpjx-maplayers'); if (!b) return null;
      window.scrollTo({ top: b.getBoundingClientRect().top + scrollY - innerHeight * 0.3, behavior: 'instant' });
      return { order: [...document.getElementById('nlpjx-map').children].filter((c) => c.tagName !== 'SCRIPT').map((c) => c.id || String(c.className).split(' ')[0] || c.tagName).slice(0, 10),
        groups: document.querySelectorAll('#nlpjx-map .nlam-bar button').length, ranges: document.querySelectorAll('#nlpjx-map .nlam-range button').length, layers: [...document.querySelectorAll('#nlpjx-map .nlpjx-maplayers button')].map((x) => x.getAttribute('data-layer')) }; }""")
    pg.wait_for_timeout(500)
    pg.screenshot(path=os.path.join(out_dir, "controls-%d.png" % W))
    pg.evaluate("y => window.scrollTo({ top: y, behavior: 'instant' })", land_y)
    pg.wait_for_timeout(500)
    # the ConsultSheet from the wide pill, at the map
    sheet = None
    if pg.locator("#nlcta a, #nlcta button").count():
        pg.locator("#nlcta a, #nlcta button").first.click(); pg.wait_for_timeout(700)
        sheet = pg.evaluate("() => { const d = document.querySelector('#nlcta-sheet'); if (!d || !d.open) return null; const c = d.querySelector('.nlcs-ctx'); const t = d.querySelector('textarea'); return { context: c ? c.textContent.trim() : '', text_has_unit: !!(t && /13-e/.test(t.value)), link: ((t && t.value.match(/https?:[^\\s]+/)) || [''])[0] }; }")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    # back to the building, when the landing offers it
    back = None
    if pg.locator(".nlps-mapsum [data-nlps-back]").count() and not os.environ.get("NL_PROBE_NOBACK"):
        pg.locator(".nlps-mapsum [data-nlps-back]").first.click(); pg.wait_for_timeout(1800)
        back = pg.evaluate("""() => { const r = document.querySelector('#nlps').getBoundingClientRect(); const B = (s) => { const e = document.querySelector(s); if (!e || !e.getClientRects().length || getComputedStyle(e).display === 'none') return null; const q = e.getBoundingClientRect(); return [+q.top.toFixed(1), +q.bottom.toFixed(1), +q.left.toFixed(1), +q.right.toFixed(1)]; };
          const hit = (a, b) => !!a && !!b && a[2] < b[3] && b[2] < a[3] && a[0] < b[1] && b[0] < a[1]; const pill = B('#nlcta .nlcta-wa');
          return { stage_top: +r.top.toFixed(2), stage_bottom: +r.bottom.toFixed(2), card_on: !!document.querySelector('#nlps-pick .rbs-label.is-on'), card_title: (document.querySelector('#nlps-pick .rbs-label-title') || {}).textContent || '', unit: (window.__nlpsPick || {}).unit || '', focus: document.activeElement ? (document.activeElement.className || document.activeElement.tagName) : '',
            stage_notice: B('#nlps .rbs-caption'), card_notice: B('#nlps-pick .nlps-pick-cap'), pill: pill, pill_over_stage_notice: hit(pill, B('#nlps .rbs-caption')), pill_over_card: hit(pill, B('#nlps-pick')) }; }""")
        pg.screenshot(path=os.path.join(out_dir, "back-%d.png" % W))
    return {"fold": fold, "card_before": before_title, "landing": landing, "ride": ride, "controls": ctl, "sheet": sheet, "back": back}
