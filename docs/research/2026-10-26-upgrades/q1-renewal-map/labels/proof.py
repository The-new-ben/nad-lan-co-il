"""PROOF for the renewal-map labels proposal (26.10.2026). Playwright + real Chrome. READ-ONLY toward the live site.

BEFORE = https://nad-lan.co.il/urban-renewal/map/ as served now.
AFTER  = the same live page, fetched now, with ONLY its map block swapped (in this local browser, in memory) for the block
         that urban-map-labels.patch.php.txt produces (lib.swapped_live_page). Page, data, tracker, scroll: all real.

Safety: every non-GET request to nad-lan.co.il is aborted (no writes, no beacons) and analytics / session-recording hosts
are blocked, so these test visits do not land in the owner's statistics or recordings. The map token stays in memory.

Measured at 390 px (phone: touch, mobile) and 1280 px, at three zoom levels (country = the page's own first view,
central district, Tel Aviv area): label contrast (computed WCAG and sampled from pixels), overlapping label boxes,
cities whose name is readable, cities whose count is visible, cities you can tap at all, tap target size, overlapping
tap targets; then clicks: a city (list, card, tracker), a group, zoom buttons, drag pan, wheel and one-finger page scroll.

    python proof.py            (writes before-*.png, after-*.png, proof-results.json)
"""
import io
import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone

from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib  # noqa: E402

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
VIEWS = [('390', 390, 844, True, 2), ('1280', 1280, 900, False, 2)]  # desktop captured at 2x too: same CSS layout, crisp pixels for the contrast sampling
ZOOMS = [('country', None, None), ('central', [34.85, 32.05], 9), ('tlv', [34.80, 32.07], 11)]
BLOCK_HOSTS = ['google-analytics.com', 'googletagmanager.com', 'analytics.google.com', 'hotjar.com', 'hotjar.io', 'clarity.ms',
               'facebook.net', 'facebook.com/tr', 'doubleclick.net', 'tiktok.com', 'linkedin.com/px', 'bing.com/action', 'stats.wp.com']
HOOK = """(function(){var _m;Object.defineProperty(window,'mapboxgl',{configurable:true,get:function(){return _m},set:function(v){_m=v;
try{var o=v.Map.prototype.addControl;v.Map.prototype.addControl=function(){window.__nlmap=this;return o.apply(this,arguments)}}catch(e){}}})})();"""

MEASURE = r"""
(args) => {
  const mode = args.mode, cities = args.cities, map = window.__nlmap, cont = map.getContainer(), cr = cont.getBoundingClientRect();
  const L = c => { const v = c.match(/[\d.]+/g).slice(0,3).map(Number).map(x => { x/=255; return x <= 0.03928 ? x/12.92 : Math.pow((x+0.055)/1.055, 2.4); }); return 0.2126*v[0]+0.7152*v[1]+0.0722*v[2]; };
  const CR = (a,b) => { const x=L(a), y=L(b); return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05); };
  const inside = (x,y) => x > cr.left+0.5 && x < cr.right-0.5 && y > cr.top+0.5 && y < cr.bottom-0.5;
  const topPin = (x,y) => { const s = document.elementsFromPoint(x,y); for (const e of s) { const p = e.closest && e.closest('.nlurm-pin'); if (p) return p; if (e.classList && (e.classList.contains('mapboxgl-canvas') || e.classList.contains('nlurm-card'))) return e.classList.contains('nlurm-card') ? e : null; } return null; };
  const pts = (r, n) => { const o=[]; const y=(r.top+r.bottom)/2; for (let i=0;i<n;i++) o.push([r.left+1+(r.width-2)*(i+0.5)/n, y]); return o; };
  const grid = r => { const o=[]; for (let i=0;i<5;i++) for (let j=0;j<3;j++) o.push([r.left+r.width*(i+0.5)/5, r.top+r.height*(j+0.5)/3]); return o; };
  const clear = (r, el, n) => r.width > 0 && pts(r, n).every(([x,y]) => inside(x,y) && topPin(x,y) === el);
  const anyHit = (r, el) => grid(r).some(([x,y]) => inside(x,y) && topPin(x,y) === el);
  const rel = r => [r.left-cr.left, r.top-cr.top, r.right-cr.left, r.bottom-cr.top];
  const ix = (a,b) => Math.min(a.right,b.right)-Math.max(a.left,b.left) > 1 && Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top) > 1;
  const proj = {}; let inView = 0;
  cities.forEach(c => { const q = map.project([c[1], c[2]]); const v = q.x >= 0 && q.y >= 0 && q.x <= cont.clientWidth && q.y <= cont.clientHeight; proj[c[0]] = v; if (v) inView++; });
  const res = { zoom: +map.getZoom().toFixed(2), in_view: inView, names: [], complete: [], counts_alone: [], counts_covered: [], tappable: [], contrast_text: [], contrast_count: [],
                tap_min_w: null, tap_min_h: null, label_overlaps: 0, name_overlaps: 0, tap_overlaps: 0, boxes: [], fonts: {}, groups: 0, shown: 0 };
  const pins = [...document.querySelectorAll('.nlurm-pin')];
  const taps = [];
  if (mode === 'before') {
    const vis = [];
    pins.forEach(el => {
      const t = el.firstChild && el.firstChild.nodeType === 3 ? el.firstChild.textContent : el.textContent;
      const i = t.lastIndexOf(' · '); const city = t.slice(0, i), cnt = t.slice(i+3);
      if (!proj[city]) return;
      const r = el.getBoundingClientRect(); vis.push(r); taps.push(r);
      const rg = document.createRange(); rg.setStart(el.firstChild, 0); rg.setEnd(el.firstChild, city.length); const nr = rg.getBoundingClientRect();
      const rc = document.createRange(); rc.setStart(el.firstChild, t.length - cnt.length); rc.setEnd(el.firstChild, t.length); const cn = rc.getBoundingClientRect();
      const cs = getComputedStyle(el);
      const nOk = clear(nr, el, 5), cOk = clear(cn, el, 3);
      if (nOk) { res.names.push(city); res.boxes.push({k:'name', city, r: rel(nr)}); }
      if (cOk) { res.counts_alone.push(city); res.counts_covered.push(city); }
      if (nOk && cOk) res.complete.push(city);
      if (anyHit(r, el)) res.tappable.push(city);
      res.contrast_text.push(+CR(cs.color, cs.backgroundColor).toFixed(2));
      res.contrast_count.push(+CR(cs.color, cs.backgroundColor).toFixed(2));
      res.fonts = { family: cs.fontFamily, size: cs.fontSize, weight: cs.fontWeight, color: cs.color, bg: cs.backgroundColor };
      res.shown++;
    });
    for (let a=0;a<vis.length;a++) for (let b=a+1;b<vis.length;b++) if (ix(vis[a],vis[b])) res.label_overlaps++;
    res.name_overlaps = res.label_overlaps;
  } else {
    const names = [], dots = [];
    pins.forEach(el => {
      if (el.style.display === 'none') return;
      const grp = el.classList.contains('nlurm-grp');
      const members = grp ? (el._m || []).map(p => p.c.city) : [el.lastChild.textContent];
      const r = el.getBoundingClientRect(); const cx = (r.left+r.right)/2, cy = (r.top+r.bottom)/2;
      if (!inside(cx, cy)) return;
      res.shown++; if (grp) res.groups++;
      taps.push(r);
      const dot = el.firstChild, nm = el.lastChild, dr = dot.getBoundingClientRect(), nr = nm.getBoundingClientRect();
      dots.push({r: dr, el});
      const ncs = getComputedStyle(nm), dcs = getComputedStyle(dot);
      const named = /\bis-(ne|nw|se|sw|e|w|n|s)\b/.test(el.className) && ncs.visibility === 'visible';
      if (named) { names.push({r: nr, el}); }
      if (named && clear(nr, el, 5)) { res.names.push(members[0]); res.boxes.push({k:'name', city: members[0], r: rel(nr)}); }
      const countOk = clear({left: dr.left+dr.width*0.2, right: dr.right-dr.width*0.2, top: dr.top, bottom: dr.bottom, width: dr.width*0.6}, el, 3);
      if (countOk) { if (!grp) res.counts_alone.push(members[0]); members.forEach(m => res.counts_covered.push(m)); }
      if (countOk && named && clear(nr, el, 5)) res.complete.push(members[0] + (grp ? ' (group)' : ''));
      if (anyHit(r, el)) members.forEach(m => res.tappable.push(m + (grp ? ' (group)' : '')));
      if (named) { const halo = (ncs.textShadow.match(/rgba?\([^)]*\)/) || ['rgb(255, 255, 255)'])[0]; res.contrast_text.push(+CR(ncs.color, halo).toFixed(2)); }
      res.contrast_count.push(+CR(dcs.color, dcs.backgroundColor).toFixed(2));
      if (!grp) res.fonts = { name_family: ncs.fontFamily, name_size: ncs.fontSize, name_weight: ncs.fontWeight, name_color: ncs.color, count_family: dcs.fontFamily, count_size: dcs.fontSize, count_color: dcs.color, count_bg: dcs.backgroundColor };
    });
    for (let a=0;a<names.length;a++) for (let b=a+1;b<names.length;b++) if (ix(names[a].r, names[b].r)) res.name_overlaps++;
    // association: a name is ambiguous when another circle's edge is as near to it as its own circle's edge (+4px)
    const egap = (r, d) => { const cx=(d.left+d.right)/2, cy=(d.top+d.bottom)/2, rr=d.width/2; const x=Math.max(r.left,Math.min(cx,r.right)), y=Math.max(r.top,Math.min(cy,r.bottom)); return Math.hypot(x-cx,y-cy)-rr; };
    res.ambiguous = 0;
    names.forEach(n => { const own = dots.find(d => d.el === n.el); if (!own) return; const g0 = egap(n.r, own.r); if (dots.some(d => d.el !== n.el && egap(n.r, d.r) < g0 + 4)) res.ambiguous++; });
    let lo = res.name_overlaps;
    names.forEach(n => dots.forEach(d => { if (d.el !== n.el && ix(n.r, d.r)) lo++; }));
    for (let a=0;a<dots.length;a++) for (let b=a+1;b<dots.length;b++) if (ix(dots[a].r, dots[b].r)) lo++;
    res.label_overlaps = lo;
  }
  for (let a=0;a<taps.length;a++) for (let b=a+1;b<taps.length;b++) if (ix(taps[a],taps[b])) res.tap_overlaps++;
  if (taps.length) { res.tap_min_w = +Math.min(...taps.map(r=>r.width)).toFixed(1); res.tap_min_h = +Math.min(...taps.map(r=>r.height)).toFixed(1); }
  res.counts_covered = [...new Set(res.counts_covered)];
  res.base = { language: map.getLanguage ? (map.getLanguage() || null) : null, rtl: window.mapboxgl.getRTLTextPluginStatus ? window.mapboxgl.getRTLTextPluginStatus() : null };
  return res;
}
"""

JUMP = """async (a) => { const m = window.__nlmap; m.jumpTo({center: a.c, zoom: a.z});
  await new Promise(res => { let d = false; m.once('idle', () => { d = true; res(); }); setTimeout(() => { if (!d) res(); }, 9000); });
  await new Promise(r => setTimeout(r, 700)); return m.getZoom(); }"""


def pixel_contrast(png, boxes, dsf):
    im = Image.open(png).convert('RGB')
    out = []
    for b in boxes:
        x0, y0, x1, y1 = [int(round(v * dsf)) for v in b['r']]
        if x1 - x0 < 4 or y1 - y0 < 4:
            continue
        px = list(im.crop((x0, y0, x1, y1)).getdata())

        def lum(p):
            v = []
            for c in p:
                c /= 255
                v.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
            return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
        ls = sorted(lum(p) for p in px)
        lo, hi = ls[int(len(ls) * 0.05)], ls[int(len(ls) * 0.95) - 1]
        out.append(round((hi + 0.05) / (lo + 0.05), 2))
    return out


def wait_ready(pg, mode):
    pg.wait_for_function("document.querySelectorAll('.nlurm-pin:not(.nlurm-grp)').length>=76", timeout=90000)
    pg.wait_for_function("window.__nlmap && window.__nlmap.loaded()", timeout=90000)
    if mode == 'after':
        try:
            pg.wait_for_function("window.mapboxgl.getRTLTextPluginStatus()==='loaded'", timeout=20000)
        except Exception:
            pass
    pg.evaluate("document.fonts.ready.then(()=>1)")
    pg.evaluate("""async () => { const m = window.__nlmap; await new Promise(res => { let d=false; m.once('idle', ()=>{d=true;res()}); m.triggerRepaint(); setTimeout(()=>{ if(!d) res(); }, 6000); }); await new Promise(r => setTimeout(r, 1200)); }""")


def center_map(pg):
    pg.evaluate("document.getElementById('nlurm-map').scrollIntoView({block:'center'})")
    time.sleep(0.6)


def interactions(pg, mode, mob, cdp):
    out = {}
    js_state = "() => { const m = window.__nlmap; const c = m.getCenter(); return {z: m.getZoom(), lng: c.lng, lat: c.lat, sy: window.scrollY}; }"
    # 1. tap a city at the Tel Aviv zoom: the list (today's behaviour) must load; AFTER also the card and the tracker
    pg.evaluate(JUMP, {'c': [34.80, 32.07], 'z': 11})
    center_map(pg)
    target = pg.evaluate("""(mode) => {
      const cont = window.__nlmap.getContainer(), cr = cont.getBoundingClientRect();
      const ok = (x,y) => { const s = document.elementsFromPoint(x,y); for (const e of s) { const p = e.closest && e.closest('.nlurm-pin'); if (p) return p; } return null; };
      const want = ['גבעתים', 'רמת גן', 'תל אביב יפו', 'בני ברק', 'חולון'];
      for (const w of want) {
        for (const el of document.querySelectorAll('.nlurm-pin:not(.nlurm-grp)')) {
          if (el.style.display === 'none') continue;
          const name = mode === 'before' ? el.textContent.split(' · ')[0] : el.lastChild.textContent;
          if (name !== w) continue;
          const r = (mode === 'before' ? el : el.firstChild).getBoundingClientRect();
          for (let i=0;i<9;i++) { const x = r.left + r.width*((i%3)+0.5)/3, y = r.top + r.height*(Math.floor(i/3)+0.5)/3;
            if (x>cr.left && x<cr.right && y>cr.top && y<cr.bottom && ok(x,y) === el) return {city: w, x, y}; }
        }
      }
      return null; }""", mode)
    out['city_tap_target'] = target
    if target:
        if mob:
            pg.touchscreen.tap(target['x'], target['y'])
        elif mode == 'after':
            # the clickable states on the real page: hover, then pressed; the release completes the click (selected state follows)
            clip = {'x': target['x'] - 150, 'y': target['y'] - 60, 'width': 300, 'height': 120}
            pg.mouse.move(target['x'] + 40, target['y'] + 40)
            time.sleep(0.3)
            pg.screenshot(path=os.path.join(HERE, 'after-1280-state-default.png'), clip=clip)
            pg.mouse.move(target['x'], target['y'])
            time.sleep(0.35)
            pg.screenshot(path=os.path.join(HERE, 'after-1280-state-hover.png'), clip=clip)
            pg.mouse.down()
            time.sleep(0.25)
            pg.screenshot(path=os.path.join(HERE, 'after-1280-state-pressed.png'), clip=clip)
            pg.mouse.up()
            time.sleep(0.5)
            pg.mouse.move(target['x'] + 200, target['y'] + 150)
            time.sleep(0.3)
            pg.screenshot(path=os.path.join(HERE, 'after-1280-state-selected.png'), clip=clip)
        else:
            pg.mouse.click(target['x'], target['y'])
        try:
            pg.wait_for_function("document.querySelectorAll('#nlurm-list .nlur-hit a').length>0", timeout=15000)
            out['list_loaded'] = pg.evaluate("document.querySelectorAll('#nlurm-list .nlur-hit a').length")
            out['list_first'] = pg.evaluate("document.querySelector('#nlurm-list .nlur-hit').textContent.slice(0,80)")
        except Exception:
            out['list_loaded'] = 0
        if mode == 'after':
            try:
                pg.wait_for_function("document.querySelector('.nlurm-card .nlurm-bar')", timeout=15000)
                time.sleep(0.4)
                out['card'] = pg.evaluate("""() => { const c = document.querySelector('.nlurm-card'); const r = c.getBoundingClientRect(); const go = c.querySelector('.go');
                  return {text: c.innerText.replace(/\\s+/g,' ').slice(0,400), w: Math.round(r.width), h: Math.round(r.height), close_w: c.querySelector('.nlurm-x').getBoundingClientRect().width,
                          buttons: [...c.querySelectorAll('.nlurm-acts button')].map(b => ({t: b.textContent, h: Math.round(b.getBoundingClientRect().height)})), tracker_button: !!go,
                          selected_pin: !!document.querySelector('.nlurm-pin.is-on')}; }""")
                pg.locator('#nlurm-map').screenshot(path=os.path.join(HERE, 'after-%s-card.png' % ('390' if mob else '1280')))
                if out['card']['tracker_button']:
                    btn = pg.locator('.nlurm-card .go')
                    if mob:
                        btn.tap()
                    else:
                        btn.click()
                    time.sleep(1.8)
                    out['tracker'] = pg.evaluate("""() => { const s = document.querySelector('#nlur2-track select[id$="-city"]'); const t = s.getBoundingClientRect();
                      const ans = document.querySelector('#nlur2-track .nli__answer, #nlur2-track [class*=answer]');
                      const hdr = document.elementsFromPoint(window.innerWidth/2, t.top + 2).some(e => e.closest && e.closest('header'));
                      return {select_value: s && s.value, select_in_view: t.top > 0 && t.bottom < window.innerHeight * 0.7, select_under_header: hdr, answer: ans ? ans.innerText.replace(/\\s+/g,' ').slice(0,160) : null}; }""")
                    pg.screenshot(path=os.path.join(HERE, 'after-%s-tracker.png' % ('390' if mob else '1280')))
                    center_map(pg)
            except Exception as e:
                out['card_error'] = str(e)[:200]
    # 2. AFTER: tap a group at the country zoom: the map zooms in
    if mode == 'after':
        pg.evaluate("() => { const c = document.querySelector('.nlurm-card .nlurm-x'); if (c) c.click(); }")
        pg.evaluate(JUMP, {'c': [34.9, 31.9], 'z': 7})
        center_map(pg)
        g = pg.evaluate("""() => { const cont = window.__nlmap.getContainer(), cr = cont.getBoundingClientRect();
          for (const el of document.querySelectorAll('.nlurm-grp')) { if (el.style.display === 'none') continue; const r = el.firstChild.getBoundingClientRect();
            const x = (r.left+r.right)/2, y = (r.top+r.bottom)/2; if (x>cr.left+5 && x<cr.right-5 && y>cr.top+5 && y<cr.bottom-5) return {x, y, label: el.lastChild.textContent, n: el.firstChild.textContent, members: (el._m||[]).length}; } return null; }""")
        if g:
            z0 = pg.evaluate(js_state)['z']
            (pg.touchscreen.tap if mob else pg.mouse.click)(g['x'], g['y'])
            time.sleep(1.6)
            g['zoom_before'] = round(z0, 2)
            g['zoom_after'] = round(pg.evaluate(js_state)['z'], 2)
        out['group_tap'] = g
    # 2b. keyboard (desktop): focus a city label, press Enter: the list loads (and AFTER: the card opens, Escape closes it)
    if not mob:
        pg.evaluate("() => { const c = document.querySelector('.nlurm-card .nlurm-x'); if (c) c.click(); document.getElementById('nlurm-list').innerHTML = ''; }")
        pg.evaluate(JUMP, {'c': [34.80, 32.07], 'z': 11})
        center_map(pg)
        kb_city = pg.evaluate("""() => { for (const el of document.querySelectorAll('.nlurm-pin:not(.nlurm-grp)')) { if (el.style.display === 'none') continue;
            const r = el.getBoundingClientRect(), cr = document.getElementById('nlurm-map').getBoundingClientRect();
            if (r.left > cr.left && r.right < cr.right && r.top > cr.top && r.bottom < cr.bottom) { el.focus(); return el.getAttribute('aria-label') || el.textContent; } } return null; }""")
        pg.keyboard.press('Enter')
        kb = {'focused': kb_city}
        try:
            pg.wait_for_function("document.querySelectorAll('#nlurm-list .nlur-hit a').length>0", timeout=15000)
            kb['list_loaded'] = pg.evaluate("document.querySelectorAll('#nlurm-list .nlur-hit a').length")
        except Exception:
            kb['list_loaded'] = 0
        if mode == 'after':
            kb['card_open'] = pg.evaluate("!!document.querySelector('.nlurm-card')")
            pg.keyboard.press('Escape')
            time.sleep(0.3)
            kb['escape_closes'] = pg.evaluate("!document.querySelector('.nlurm-card')")
        out['keyboard'] = kb
    # 3. zoom buttons
    pg.evaluate(JUMP, {'c': [34.9, 31.9], 'z': 7})
    center_map(pg)
    z0 = pg.evaluate(js_state)['z']
    pg.locator('.mapboxgl-ctrl-zoom-in').click()
    time.sleep(1.2)
    out['zoom_button'] = {'before': round(z0, 2), 'after': round(pg.evaluate(js_state)['z'], 2)}
    pg.evaluate(JUMP, {'c': [34.9, 31.9], 'z': 7})
    center_map(pg)
    # a point on the map with no label under it (sea side), and a point on the biggest visible label
    spots = pg.evaluate("""(mode) => { const cont = window.__nlmap.getContainer(), cr = cont.getBoundingClientRect(); let empty = null, label = null;
      for (let i=1;i<10 && !empty;i++) for (let j=2;j<8 && !empty;j++) { const x = cr.left + cr.width*i/10, y = cr.top + cr.height*j/10;
        const s = document.elementsFromPoint(x,y); if (!s.some(e => e.closest && (e.closest('.nlurm-pin') || e.closest('.mapboxgl-ctrl')))) empty = {x, y}; }
      let best = -1; for (const el of document.querySelectorAll('.nlurm-pin')) { if (el.style.display === 'none') continue; const r = (mode==='before'?el:el.firstChild).getBoundingClientRect();
        const x=(r.left+r.right)/2, y=(r.top+r.bottom)/2; if (x<cr.left+10||x>cr.right-10||y<cr.top+10||y>cr.bottom-10) continue;
        const n = mode==='before' ? +el.textContent.split(' · ')[1] : +el.firstChild.textContent; if (n > best) { best = n; label = {x, y}; } }
      return {empty, label}; }""", mode)
    out['spots'] = spots
    if not mob:
        # 4. drag pan on an empty spot
        if spots['empty']:
            s0 = pg.evaluate(js_state)
            x, y = spots['empty']['x'], spots['empty']['y']
            pg.mouse.move(x, y)
            pg.mouse.down()
            for k in range(1, 11):
                pg.mouse.move(x - 15 * k, y + 4 * k)
                time.sleep(0.03)
            pg.mouse.up()
            time.sleep(1.0)
            s1 = pg.evaluate(js_state)
            out['drag_pan'] = {'moved_lng': round(s1['lng'] - s0['lng'], 4), 'moved_lat': round(s1['lat'] - s0['lat'], 4), 'pans': abs(s1['lng'] - s0['lng']) > 0.01}
            pg.evaluate(JUMP, {'c': [34.9, 31.9], 'z': 7})
        # 5. wheel over the map scrolls the page (no ctrl), the map does not zoom
        for where in ('empty', 'label'):
            if not spots.get(where):
                continue
            center_map(pg)
            s0 = pg.evaluate(js_state)
            pg.mouse.move(spots[where]['x'], spots[where]['y'])
            time.sleep(0.1)
            sp = pg.evaluate("""(p) => { const cr = document.getElementById('nlurm-map').getBoundingClientRect(); return {x: p.x, y: p.y}; }""", spots[where])
            pg.mouse.wheel(0, 450)
            time.sleep(1.0)
            s1 = pg.evaluate(js_state)
            out['wheel_' + where] = {'page_scrolled_px': round(s1['sy'] - s0['sy']), 'map_zoom_change': round(s1['z'] - s0['z'], 3)}
    else:
        # 5. one-finger swipe (real touch events through CDP) over the map, on an empty spot and starting on a label, scrolls the
        #    page and does not move the map; the control swipe is on page text above the map (proves the method scrolls at all)
        def swipe(x, y, dy=-250, steps=12):
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'id': 1}]})
            for k in range(1, steps + 1):
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y + dy * k / steps, 'id': 1}]})
                time.sleep(0.016)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        center_map(pg)
        top = pg.evaluate("document.getElementById('nlurm-map').getBoundingClientRect().top")
        for where in ('control_above_map', 'empty', 'label'):
            center_map(pg)
            pt = {'x': 120, 'y': max(30, top - 50)} if where == 'control_above_map' else spots.get(where)
            if not pt:
                continue
            s0 = pg.evaluate(js_state)
            swipe(pt['x'], pt['y'])
            time.sleep(1.2)
            s1 = pg.evaluate(js_state)
            out['swipe_' + where] = {'page_scrolled_px': round(s1['sy'] - s0['sy']), 'map_moved': abs(s1['lng'] - s0['lng']) + abs(s1['lat'] - s0['lat']) > 1e-4, 'map_zoom_change': round(s1['z'] - s0['z'], 3),
                                     'opened_card': bool(pg.evaluate("!!document.querySelector('.nlurm-card')"))}
    return out


def main():
    cities = [[c['city'], c['lnglat'][0], c['lnglat'][1]] for c in json.load(open(os.path.join(HERE, 'live-data.json'), encoding='utf-8'))['cities'] if c.get('lnglat')]
    results = {'at_utc': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), 'live_url': lib.LIVE_URL, 'views': {}}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME, headless=True, args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--disable-blink-features=AutomationControlled'])
        for vname, w, h, mob, dsf in VIEWS:
            for mode in ('before', 'after'):
                ctx = br.new_context(viewport={'width': w, 'height': h}, is_mobile=mob, has_touch=mob, device_scale_factor=dsf, locale='he-IL')
                ctx.add_init_script(HOOK)
                blocked = {'n': 0}

                def guard(route):
                    r = route.request
                    u = r.url
                    if any(hh in u for hh in BLOCK_HOSTS) or ('nad-lan.co.il' in u and r.method != 'GET'):
                        blocked['n'] += 1
                        return route.abort()
                    if mode == 'after' and r.resource_type == 'document' and u.split('?')[0].rstrip('/') == lib.LIVE_URL.rstrip('/'):
                        resp = route.fetch()
                        return route.fulfill(response=resp, body=lib.swapped_live_page(resp.text()), headers={**resp.headers, 'content-type': 'text/html; charset=UTF-8'})
                    return route.continue_()
                ctx.route('**/*', guard)
                pg = ctx.new_page()
                errs = []
                lookups = []
                pg.on('pageerror', lambda e, _e=errs: _e.append(str(e)[:200]))
                pg.on('response', lambda r, _l=lookups: _l.append(r.status) if 'renewal-lookup' in r.url else None)
                cdp = ctx.new_cdp_session(pg)
                pg.goto(lib.LIVE_URL + '?lblproof=' + mode, wait_until='domcontentloaded', timeout=90000)
                wait_ready(pg, mode)
                center_map(pg)
                rec = {'states': {}}
                for zname, c, z in ZOOMS:
                    if c:
                        pg.evaluate(JUMP, {'c': c, 'z': z})
                        center_map(pg)
                    m = pg.evaluate(MEASURE, {'mode': mode, 'cities': cities})
                    shot = os.path.join(HERE, '%s-%s-%s.png' % (mode, vname, zname))
                    pg.locator('#nlurm-map').screenshot(path=shot)
                    m['contrast_pixels'] = pixel_contrast(shot, m.pop('boxes'), dsf)
                    rec['states'][zname] = m
                    print(vname, mode, zname, 'in view', m['in_view'], 'names', len(m['names']), 'complete', len(m['complete']), 'counts alone', len(m['counts_alone']), 'covered', len(m['counts_covered']),
                          'tappable', len(m['tappable']), 'overlaps', m['label_overlaps'], 'name overlaps', m['name_overlaps'], 'tap', m['tap_min_w'], m['tap_min_h'], 'tap overlaps', m['tap_overlaps'], 'ambiguous', m.get('ambiguous'),
                          'contrast min', min(m['contrast_text'] or [0]), 'px median', statistics.median(m['contrast_pixels']) if m['contrast_pixels'] else None)
                rec['interactions'] = interactions(pg, mode, mob, cdp)
                print(vname, mode, 'interactions', json.dumps(rec['interactions'], ensure_ascii=False)[:1500])
                rec['page_errors'] = errs
                rec['lookup_statuses'] = lookups  # 429 = the site's own limit (30 lookups per IP per hour), not a broken click
                rec['blocked_requests'] = blocked['n']
                results['views'].setdefault(vname, {})[mode] = rec
                ctx.close()
        br.close()
    json.dump(results, open(os.path.join(HERE, 'proof-results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('written proof-results.json')


if __name__ == '__main__':
    main()
