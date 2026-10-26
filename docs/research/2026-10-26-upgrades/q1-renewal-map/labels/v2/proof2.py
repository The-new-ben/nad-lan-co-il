"""PROOF for the renewal-map v2 proposal (26.10.2026). Playwright + real Chrome. READ-ONLY toward the live site.

BEFORE = https://nad-lan.co.il/urban-renewal/map/ as served now.
AFTER  = the same live page, fetched now, with ONLY its note and map block swapped (in this local browser, in memory) for the
         ones urban-map-v2.patch.php.txt produces (lib2.swapped_live_page). Page, data, tracker, scroll: all real.

Safety: every non-GET request to nad-lan.co.il is aborted (no writes, no beacons) and analytics / session-recording hosts are
blocked, so these test visits do not land in the owner's statistics or Hotjar recordings. The map token stays in memory.
Screenshots: the sticky site header is set to static in the test browser only (it would cut element screenshots); the floating
WhatsApp bar and the accessibility button stay, as visitors see them.

Measured at 390 px (phone: touch, mobile) and 1280 px, at three zooms (country = the page's own first view, central district,
Tel Aviv area): readable names, facts on screen, overlaps, contrast (computed and sampled from pixels), tap sizes, tap overlaps,
names tied to the wrong point; then every interaction: a city (list, card, peek), all complexes and their links, the tracker
(city and one complex), search, the five chips, hover preview, keyboard, zoom buttons, "כל הארץ", drag pan, wheel, one-finger
page scroll, the lookup calls (HAD-605) and load timing.

    python proof2.py            (writes before-*.png, after-*.png, proof-results.json)
"""
import io
import json
import os
import random
import statistics
import sys
import time
import urllib.request
from datetime import datetime, timezone

from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib2  # noqa: E402

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
VIEWS = [('390', 390, 844, True, 2), ('1280', 1280, 900, False, 2)]
ZOOMS = [('country', None, None), ('central', [34.85, 32.05], 9), ('tlv', [34.80, 32.07], 11)]
BLOCK_HOSTS = ['google-analytics.com', 'googletagmanager.com', 'analytics.google.com', 'hotjar.com', 'hotjar.io', 'clarity.ms',
               'facebook.net', 'facebook.com/tr', 'doubleclick.net', 'tiktok.com', 'linkedin.com/px', 'bing.com/action', 'stats.wp.com']
HOOK = """(function(){var _m;Object.defineProperty(window,'mapboxgl',{configurable:true,get:function(){return _m},set:function(v){_m=v;
try{var o=v.Map.prototype.addControl;v.Map.prototype.addControl=function(){window.__nlmap=this;return o.apply(this,arguments)}}catch(e){}}})})();
window.__t0=performance.now();"""
STATIC_HEADER = '#nlhp-top,header.nlhp-top{position:static!important}'

MEASURE = r"""
(args) => {
  const mode = args.mode, cities = args.cities, map = window.__nlmap, cont = map.getContainer(), cr = cont.getBoundingClientRect();
  const L = c => { const v = c.match(/[\d.]+/g).slice(0,3).map(Number).map(x => { x/=255; return x <= 0.03928 ? x/12.92 : Math.pow((x+0.055)/1.055, 2.4); }); return 0.2126*v[0]+0.7152*v[1]+0.0722*v[2]; };
  const CR = (a,b) => { const x=L(a), y=L(b); return +((Math.max(x,y)+0.05)/(Math.min(x,y)+0.05)).toFixed(2); };
  const inside = (x,y) => x > cr.left+0.5 && x < cr.right-0.5 && y > cr.top+0.5 && y < cr.bottom-0.5;
  const sel = mode === 'before' ? '.nlurm-pin' : '.nlurm-lb .tg';
  const topOf = (x,y) => { for (const e of document.elementsFromPoint(x,y)) { const p = e.closest && e.closest(sel); if (p) return p; if (e.closest && (e.closest('.nlurm-peek') || e.closest('.nlurm-pop') || e.closest('.mapboxgl-ctrl') || e.closest('#nlcta'))) return e; if (e.classList && e.classList.contains('mapboxgl-canvas')) return null; } return null; };
  const pts = (r, n) => { const o=[]; const y=(r.top+r.bottom)/2; for (let i=0;i<n;i++) o.push([r.left+1+(r.width-2)*(i+0.5)/n, y]); return o; };
  const clear = (r, el, n) => r.width > 0 && pts(r, n).every(([x,y]) => inside(x,y) && topOf(x,y) === el);
  const rel = r => [r.left-cr.left, r.top-cr.top, r.right-cr.left, r.bottom-cr.top];
  const ix = (a,b) => Math.min(a.right,b.right)-Math.max(a.left,b.left) > 1 && Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top) > 1;
  let inView = 0; const proj = {};
  cities.forEach(c => { const q = map.project([c[1], c[2]]); const v = q.x >= 0 && q.y >= 0 && q.x <= cont.clientWidth && q.y <= cont.clientHeight; proj[c[0]] = v; if (v) inView++; });
  const res = { zoom: +map.getZoom().toFixed(2), in_view: inView, shown: 0, names: [], complete: [], counts: [], facts: 0, facts_per_tag: null, tiers: {}, contrast_text: [], contrast_facts: [],
                tap_min_w: null, tap_min_h: null, overlaps: 0, tap_overlaps: 0, over_lines: 0, ambiguous: 0, boxes: [], fonts: {}, tappable: 0 };
  const taps = [];
  if (mode === 'before') {
    document.querySelectorAll('.nlurm-pin').forEach(el => {
      const t = el.textContent; const i = t.lastIndexOf(' · '); const city = t.slice(0, i), cnt = t.slice(i+3);
      if (!proj[city]) return;
      const r = el.getBoundingClientRect(); taps.push(r); res.shown++;
      const rg = document.createRange(); rg.setStart(el.firstChild, 0); rg.setEnd(el.firstChild, city.length); const nr = rg.getBoundingClientRect();
      const rc = document.createRange(); rc.setStart(el.firstChild, t.length - cnt.length); rc.setEnd(el.firstChild, t.length); const cn = rc.getBoundingClientRect();
      const cs = getComputedStyle(el);
      const nOk = clear(nr, el, 5), cOk = clear(cn, el, 3);
      if (nOk) { res.names.push(city); res.boxes.push({city, r: rel(nr)}); }
      if (cOk) { res.counts.push(city); res.facts++; }
      if (nOk && cOk) res.complete.push(city);
      if (clear({left: r.left+r.width/2-1, right: r.left+r.width/2+1, top: r.top, bottom: r.bottom, width: 2}, el, 1)) res.tappable++;
      res.contrast_text.push(CR(cs.color, cs.backgroundColor)); res.contrast_facts.push(CR(cs.color, cs.backgroundColor));
      res.fonts = { family: cs.fontFamily, size: cs.fontSize, weight: cs.fontWeight, color: cs.color, bg: cs.backgroundColor };
    });
    res.facts_per_tag = res.names.length ? +(res.facts / Math.max(1, res.shown)).toFixed(2) : 0;
  } else {
    const tags = [...document.querySelectorAll('.nlurm-lb .tg')].filter(b => b.style.display !== 'none');
    const pe = new Map(tags.map(b => [b, getComputedStyle(b).pointerEvents]));  // read before the test style below
    const tst = document.createElement('style'); tst.textContent = '.nlurm-lb .tg{pointer-events:auto!important}'; document.head.appendChild(tst);  // so elementsFromPoint sees name-only tags too
    const lines = [...document.querySelectorAll('.nlurm-lb .ld')].filter(l => l.style.display !== 'none').map(l => { const m = l.parentNode.getBoundingClientRect(); const w = parseFloat(l.style.width); const a = parseFloat((l.style.transform.match(/rotate\(([-\d.e]+)rad\)/)||[0,0])[1]); return {el: l.parentNode, x1: m.left, y1: m.top, x2: m.left + w*Math.cos(a), y2: m.top + w*Math.sin(a)}; });
    const dots = [...document.querySelectorAll('.nlurm-lb .dt')].filter(d => getComputedStyle(d).display !== 'none').map(d => { const r = d.getBoundingClientRect(); return {el: d.parentNode, x: (r.left+r.right)/2, y: (r.top+r.bottom)/2}; }).filter(d => inside(d.x, d.y));
    const boxes = [];
    tags.forEach(b => {
      const r = b.getBoundingClientRect(); const cx = (r.left+r.right)/2, cy = (r.top+r.bottom)/2;
      if (!inside(cx, cy)) return;
      res.shown++; boxes.push({r, el: b.parentNode}); if (pe.get(b) !== 'none') taps.push(r); else res.name_only_through_map = (res.name_only_through_map||0) + 1;
      const t = (b.className.match(/\bt([LMS])\b/)||[])[1]; res.tiers[t] = (res.tiers[t]||0)+1;
      const nm = b.querySelector('.nm'), nrg = document.createRange(); nrg.selectNodeContents(nm); const nr = nrg.getBoundingClientRect(), name = nm.textContent;  // the text itself, not the block
      const fs = [...b.querySelectorAll('.f')];
      const nOk = clear(nr, b, 5);
      if (nOk) { res.names.push(name); res.boxes.push({city: name, r: rel(nr)}); }
      let fOk = 0; fs.forEach(f => { const frg = document.createRange(); frg.selectNodeContents(f); if (clear(frg.getBoundingClientRect(), b, 4)) { fOk++; if (/מתחמ/.test(f.textContent)) res.counts.push(name); } });
      res.facts += fOk + (b.querySelector('.sb') ? 1 : 0);
      if (nOk && fOk) res.complete.push(name);
      if (pe.get(b) === 'none' || clear({left: cx-1, right: cx+1, top: r.top, bottom: r.bottom, width: 2}, b, 1)) res.tappable++;
      const bs = getComputedStyle(b), ns = getComputedStyle(nm);
      const bg = t === 'S' ? 'rgb(255, 255, 255)' : bs.backgroundColor;  // name-only tags read against their white halo
      res.contrast_text.push(CR(ns.color, bg));
      fs.forEach(f => { const s = getComputedStyle(f); res.contrast_facts.push(CR(s.color, bg)); const nb = f.querySelector('b'); if (nb) res.contrast_facts.push(CR(getComputedStyle(nb).color, bg)); });
      res.fonts = { name_family: ns.fontFamily, name_size: ns.fontSize, name_weight: ns.fontWeight, name_color: ns.color, facts_family: fs[0] ? getComputedStyle(fs[0]).fontFamily : null,
                    facts_size: fs[0] ? getComputedStyle(fs[0]).fontSize : null, number_family: b.querySelector('.f b') ? getComputedStyle(b.querySelector('.f b')).fontFamily : null };
      // ambiguity: another city's dot is as near to this tag's pointer as its own dot (tags joined by a line are tied explicitly)
      const own = dots.find(d => d.el === b.parentNode);
      if (own && !b.classList.contains('is-c')) {
        const px = Math.max(r.left, Math.min(own.x, r.right)), py = Math.max(r.top, Math.min(own.y, r.bottom)), d0 = Math.hypot(px-own.x, py-own.y);
        const other = dots.find(d => d.el !== b.parentNode && Math.hypot(Math.max(r.left, Math.min(d.x, r.right)) - d.x, Math.max(r.top, Math.min(d.y, r.bottom)) - d.y) + 2 < d0);
        if (other) { res.ambiguous++; res.ambiguous_who = res.ambiguous_who || []; res.ambiguous_who.push([name, (other.el.querySelector('.tg .nm')||{}).textContent || other.el.querySelector('.tg').getAttribute('aria-label')]); }
      }
    });
    for (let a=0;a<boxes.length;a++) for (let b=a+1;b<boxes.length;b++) if (ix(boxes[a].r, boxes[b].r)) res.overlaps++;
    res.over_lines_who = [];
    lines.forEach(l => boxes.forEach(bx => { if (bx.el === l.el) return; const r = bx.r; for (let k=0.08;k<0.97;k+=0.03) { const x = l.x1+(l.x2-l.x1)*k, y = l.y1+(l.y2-l.y1)*k; if (x>r.left&&x<r.right&&y>r.top&&y<r.bottom) { res.over_lines++; res.over_lines_who.push([l.el.querySelector('.nm') && l.el.querySelector('.nm').textContent, bx.el.querySelector('.nm').textContent]); break; } } }));
    res.lines = lines.length; tst.remove();
    res.facts_per_tag = res.shown ? +(res.facts / res.shown).toFixed(2) : 0;
  }
  if (mode === 'before') { for (let a=0;a<taps.length;a++) for (let b=a+1;b<taps.length;b++) if (ix(taps[a],taps[b])) res.overlaps++; }
  for (let a=0;a<taps.length;a++) for (let b=a+1;b<taps.length;b++) if (ix(taps[a],taps[b])) res.tap_overlaps++;
  if (taps.length) { res.tap_min_w = +Math.min(...taps.map(r=>r.width)).toFixed(1); res.tap_min_h = +Math.min(...taps.map(r=>r.height)).toFixed(1); }
  res.names_n = res.names.length; res.counts = [...new Set(res.counts)];
  return res;
}
"""

JUMP = """async (a) => { const m = window.__nlmap; m.jumpTo({center: a.c, zoom: a.z});
  await new Promise(res => { let d = false; m.once('idle', () => { d = true; res(); }); setTimeout(() => { if (!d) res(); }, 9000); });
  await new Promise(r => setTimeout(r, 900)); return m.getZoom(); }"""
STATE = "() => { const m = window.__nlmap; const c = m.getCenter(); return {z: m.getZoom(), lng: c.lng, lat: c.lat, sy: window.scrollY}; }"


def pixel_contrast(png, boxes, dsf):
    im = Image.open(png).convert('RGB')
    out = []

    def lum(p):
        v = []
        for c in p:
            c /= 255
            v.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    for b in boxes:
        x0, y0, x1, y1 = [int(round(v * dsf)) for v in b['r']]
        if x1 - x0 < 4 or y1 - y0 < 4:
            continue
        ls = sorted(lum(p) for p in im.crop((x0, y0, x1, y1)).getdata())
        lo, hi = ls[int(len(ls) * 0.05)], ls[int(len(ls) * 0.95) - 1]
        out.append(round((hi + 0.05) / (lo + 0.05), 2))
    return out


def wait_ready(pg, mode):
    if mode == 'before':
        pg.wait_for_function("document.querySelectorAll('.nlurm-pin').length>=76", timeout=90000)
    else:
        pg.wait_for_function("[...document.querySelectorAll('.nlurm-lb .tg')].some(b=>b.style.display!=='none')", timeout=90000)
    t_ready = pg.evaluate("performance.now()-window.__t0")
    pg.wait_for_function("window.__nlmap && window.__nlmap.loaded()", timeout=90000)
    try:
        pg.wait_for_function("window.mapboxgl.getRTLTextPluginStatus()==='loaded'", timeout=20000 if mode == 'after' else 1)
    except Exception:
        pass
    pg.evaluate("document.fonts.ready.then(()=>1)")
    pg.evaluate("""async () => { const m = window.__nlmap; await new Promise(res => { let d=false; m.once('idle', ()=>{d=true;res()}); m.triggerRepaint(); setTimeout(()=>{ if(!d) res(); }, 6000); }); await new Promise(r => setTimeout(r, 1500)); }""")
    return round(t_ready)


def center_map(pg):
    pg.evaluate("document.getElementById('nlurm-map').scrollIntoView({block:'center'})")
    time.sleep(0.6)


def find_tag(pg, names):
    return pg.evaluate("""(names) => { const cr = document.getElementById('nlurm-map').getBoundingClientRect();
      for (const w of names) for (const b of document.querySelectorAll('.nlurm-lb .tg')) { if (b.style.display === 'none') continue; const n = b.querySelector('.nm'); if (!n || n.textContent !== w) continue;
        const r = b.getBoundingClientRect(); const x = (r.left+r.right)/2, y = r.top + Math.min(14, r.height/2);
        if (x > cr.left+4 && x < cr.right-4 && y > cr.top+4 && y < cr.bottom-4) { const t = document.elementFromPoint(x, y); if (t && t.closest('.tg') === b) return {city: w, x, y}; } }
      return null; }""", names)


def interactions_after(pg, mob, cdp, vname):
    out = {}
    tap = (lambda x, y: pg.touchscreen.tap(x, y)) if mob else (lambda x, y: pg.mouse.click(x, y))
    # 1. a city: its tag at the Tel Aviv zoom -> the panel (and the peek on a phone) with every complex
    pg.evaluate(JUMP, {'c': [34.80, 32.07], 'z': 11})
    center_map(pg)
    t = find_tag(pg, ['תל אביב יפו', 'רמת גן', 'גבעתים', 'בני ברק', 'חולון'])
    out['city_tap_target'] = t
    if t:
        if not mob:
            pg.mouse.move(t['x'], t['y'])
            time.sleep(0.5)
            out['hover_preview'] = pg.evaluate("""() => { const p = document.querySelector('.nlurm-pop'); if (!p || p.style.display === 'none') return null; const r = p.getBoundingClientRect();
              return {text: p.innerText.replace(/\\s+/g,' ').slice(0,300), w: Math.round(r.width), h: Math.round(r.height), complexes_named: p.querySelectorAll('.nlurm-top3 li').length}; }""")
            pg.locator('.nlurm-v2').screenshot(path=os.path.join(HERE, 'after-1280-hover.png'))
        tap(t['x'], t['y'])
        time.sleep(1.2)
        out['city'] = pg.evaluate("""() => { const s = document.querySelector('.nlurm-side'); const ct = s.querySelector('.ct'); const pk = document.querySelector('.nlurm-peek');
          return {panel_city: ct && ct.textContent, rows: s.querySelectorAll('.nlurm-cx li').length, links: s.querySelectorAll('.nlurm-cx a.cxm').length,
                  more_button: !!s.querySelector('[data-a=more]'), facts: [...s.querySelectorAll('.nlurm-dl > div')].map(d => d.innerText.replace(/\\s+/g,' ')).slice(0,9),
                  peek: pk && pk.style.display !== 'none' ? {text: pk.innerText.replace(/\\s+/g,' ').slice(0,200), h: Math.round(pk.getBoundingClientRect().height),
                         buttons: [...pk.querySelectorAll('button')].map(b => [b.textContent, Math.round(b.getBoundingClientRect().width), Math.round(b.getBoundingClientRect().height)])} : null,
                  selected_tag: !!document.querySelector('.nlurm-lb .tg.is-on')}; }""")
        pg.locator('.nlurm-v2').screenshot(path=os.path.join(HERE, 'after-%s-city.png' % vname))
        if mob:
            pg.locator('#nlurm-map').screenshot(path=os.path.join(HERE, 'after-390-peek.png'))
        # every complex: open the full list
        more = pg.locator('.nlurm-side [data-a=more]')
        if more.count():
            (more.tap if mob else more.click)()
            time.sleep(0.6)
        out['city']['rows_all'] = pg.evaluate("document.querySelectorAll('.nlurm-side .nlurm-cx li').length")
        out['city']['links_all'] = pg.evaluate("[...document.querySelectorAll('.nlurm-side .nlurm-cx a.cxm')].map(a => a.getAttribute('href'))")
        out['city']['row_tap_min_h'] = pg.evaluate("Math.min(...[...document.querySelectorAll('.nlurm-side .nlurm-cx .cxm, .nlurm-side .nlurm-cx .cxt')].map(e => e.getBoundingClientRect().height))")
        # the tracker, set to the city
        b = pg.locator('.nlurm-side [data-a=trk]')
        if b.count():
            (b.tap if mob else b.click)()
            time.sleep(1.8)
            out['tracker_city'] = pg.evaluate("""() => { const s = document.querySelector('#nlur2-track select[id$="-city"]'); const t = s.getBoundingClientRect();
              const hdr = document.elementsFromPoint(window.innerWidth/2, t.top + 2).some(e => e.closest && e.closest('header'));
              return {select_value: s.value, in_view: t.top > 0 && t.bottom < window.innerHeight * 0.75, under_header: hdr}; }""")
            pg.screenshot(path=os.path.join(HERE, 'after-%s-tracker.png' % vname))
        # one complex "ביומן": the tracker on that complex
        center_map(pg)
        pg.evaluate("document.querySelector('.nlurm-side').scrollIntoView({block:'start'})")
        time.sleep(0.4)
        cx = pg.evaluate("""() => { const b = document.querySelector('.nlurm-side .nlurm-cx .cxt'); if (!b) return null; b.scrollIntoView({block:'center'}); return {k: b.getAttribute('data-k'), name: b.closest('li').querySelector('b').textContent}; }""")
        if cx:
            time.sleep(0.4)
            bb = pg.locator('.nlurm-side .nlurm-cx .cxt').first
            (bb.tap if mob else bb.click)()
            time.sleep(1.8)
            cx['tracker'] = pg.evaluate("""() => { const c = document.querySelector('#nlur2-track select[id$="-cx"]'); const s = document.querySelector('#nlur2-track select[id$="-city"]'); const a = document.querySelector('#nlur2-track .nli__answer');
              return {cx_value: c && c.value, city_value: s && s.value, answer: a ? a.innerText.replace(/\\s+/g,' ').slice(0,120) : null}; }""")
            cx['ok'] = cx['tracker']['cx_value'] == cx['k']
        out['complex_to_tracker'] = cx
    # 1b. phone: a name-only tag has no button of its own; a tap on it opens the city through the map's tap test
    if mob:
        pg.evaluate("() => { const b = document.querySelector('.nlurm-side [data-a=back]'); if (b) b.click(); }")
        pg.evaluate(JUMP, {'c': [34.85, 32.05], 'z': 9})
        time.sleep(1.5)  # let any smooth page scroll from the tracker buttons finish
        center_map(pg)
        time.sleep(0.6)
        FIND_S = """() => { const cr = document.getElementById('nlurm-map').getBoundingClientRect(); if (cr.top < 0 || cr.bottom > window.innerHeight) return {err: 'map not in view', top: cr.top};
          for (const b of document.querySelectorAll('.nlurm-lb .tg.tS')) { if (b.style.display === 'none') continue; const r = b.getBoundingClientRect(); const x = (r.left+r.right)/2, y = (r.top+r.bottom)/2;
            if (x > cr.left+10 && x < cr.right-10 && y > cr.top+10 && y < cr.bottom-10) return {name: b.querySelector('.nm').textContent, x, y, sy: window.scrollY}; } return null; }"""
        s_tag = None
        for _ in range(12):  # wait until the page has stopped scrolling (a smooth scroll from the tracker buttons can still run)
            center_map(pg)
            a1 = pg.evaluate(FIND_S)
            time.sleep(0.4)
            a2 = pg.evaluate(FIND_S)
            if a1 and a2 and 'err' not in a2 and a1.get('y') == a2.get('y') and a1.get('sy') == a2.get('sy'):
                s_tag = a2
                break
        if s_tag and 'err' not in s_tag:
            pg.evaluate("() => { window.__clk = []; window.__nlmap.on('click', e => window.__clk.push([Math.round(e.point.x), Math.round(e.point.y)])); }")
            s_tag['under_finger'] = pg.evaluate("(p) => document.elementsFromPoint(p.x, p.y).slice(0, 2).map(e => e.tagName + '.' + String(e.className).split(' ')[0])", s_tag)
            pg.touchscreen.tap(s_tag['x'], s_tag['y'])
            time.sleep(1.0)
            s_tag['map_click'] = pg.evaluate("window.__clk")
            s_tag['opened'] = pg.evaluate("(document.querySelector('.nlurm-side .ct')||{}).textContent || null")
            s_tag['ok'] = s_tag['opened'] == s_tag['name']
        out['name_only_tap'] = s_tag
        pg.evaluate("() => { const b = document.querySelector('.nlurm-side [data-a=back]'); if (b) b.click(); }")
    # 2. search: a complex by name, and a city with a spelling variant
    center_map(pg)
    pg.evaluate("document.querySelector('.nlurm-v2').scrollIntoView({block:'start'}); window.scrollBy(0,-90)")
    time.sleep(0.4)
    qi = pg.locator('#nlurm-qi')
    (qi.tap if mob else qi.click)()
    qi.fill('')
    qi.type('גניש', delay=40)
    time.sleep(0.5)
    out['search_complex'] = pg.evaluate("""() => { const r = document.querySelector('.nlurm-res'); return {open: !r.hidden, results: [...r.querySelectorAll('button')].map(b => b.innerText.replace(/\\s+/g,' ')).slice(0,4)}; }""")
    pg.locator('.nlurm-v2').screenshot(path=os.path.join(HERE, 'after-%s-search.png' % vname))
    first = pg.locator('.nlurm-res button').first
    if first.count():
        (first.tap if mob else first.click)()
        time.sleep(1.6)
        out['search_complex']['picked'] = pg.evaluate("""() => ({panel_city: (document.querySelector('.nlurm-side .ct')||{}).textContent, highlighted: (document.querySelector('.nlurm-side .nlurm-cx li.is-hi b')||{}).textContent, zoom: +window.__nlmap.getZoom().toFixed(2)})""")
    pg.evaluate("document.querySelector('.nlurm-v2').scrollIntoView({block:'start'}); window.scrollBy(0,-90)")
    (qi.tap if mob else qi.click)()
    qi.fill('')
    qi.type('גבעתיים', delay=40)
    time.sleep(0.5)
    out['search_spelling'] = pg.evaluate("[...document.querySelectorAll('.nlurm-res button')].map(b => b.innerText.replace(/\\s+/g,' ')).slice(0,2)")
    pg.keyboard.press('Escape')
    # close the city
    pg.evaluate("() => { const b = document.querySelector('.nlurm-side [data-a=back]'); if (b) b.click(); }")
    time.sleep(0.5)
    # 3. the five chips at the country zoom
    pg.evaluate(JUMP, {'c': [34.9, 31.9], 'z': 7})
    center_map(pg)
    chips = {}
    for m in ['all', 'ap', 'un', 'px', 'mv']:
        c = pg.locator('.nlurm-bar .nlurm-chip[data-m=%s]' % m)
        c.scroll_into_view_if_needed()
        (c.tap if mob else c.click)()
        time.sleep(0.9)
        chips[m] = pg.evaluate("""() => { const t = [...document.querySelectorAll('.nlurm-lb .tg')].filter(b => b.style.display !== 'none'); const cr = document.getElementById('nlurm-map').getBoundingClientRect();
          const vis = t.filter(b => { const r = b.getBoundingClientRect(); return r.left < cr.right && r.right > cr.left && r.top < cr.bottom && r.bottom > cr.top; });
          return {tags: vis.length, with_facts: vis.filter(b => b.querySelector('.f')).length, sample: vis.filter(b => b.querySelector('.f')).slice(0,3).map(b => b.innerText.replace(/\\s+/g,' ')),
                  pressed: document.querySelector('.nlurm-bar .nlurm-chip[aria-pressed=true]').textContent, first_row: (document.querySelector('.nlurm-side .ctr')||{innerText:''}).innerText.replace(/\\s+/g,' ')}; }""")
        pg.locator('#nlurm-map').screenshot(path=os.path.join(HERE, 'after-%s-mode-%s.png' % (vname, m)))
    out['chips'] = chips
    c = pg.locator('.nlurm-bar .nlurm-chip[data-m=all]')
    c.scroll_into_view_if_needed()
    (c.tap if mob else c.click)()
    time.sleep(0.6)
    # 4. keyboard (desktop): Tab to a tag, Enter opens it, Escape closes
    if not mob:
        pg.evaluate(JUMP, {'c': [34.80, 32.07], 'z': 11})
        center_map(pg)
        name = pg.evaluate("""() => { for (const b of document.querySelectorAll('.nlurm-lb .tg')) { if (b.style.display === 'none') continue; b.focus(); return b.querySelector('.nm').textContent; } return null; }""")
        pg.keyboard.press('Enter')
        time.sleep(0.8)
        kb = {'focused': name, 'panel_city': pg.evaluate("(document.querySelector('.nlurm-side .ct')||{}).textContent || null")}
        pg.keyboard.press('Escape')
        time.sleep(0.4)
        kb['escape_closes'] = pg.evaluate("!document.querySelector('.nlurm-side .ct')")
        out['keyboard'] = kb
    # 5. zoom buttons and "כל הארץ"
    pg.evaluate(JUMP, {'c': [34.9, 31.9], 'z': 7})
    center_map(pg)
    z0 = pg.evaluate(STATE)['z']
    zi = pg.locator('.mapboxgl-ctrl-zoom-in')
    (zi.tap if mob else zi.click)()
    time.sleep(1.2)
    out['zoom_button'] = {'before': round(z0, 2), 'after': round(pg.evaluate(STATE)['z'], 2)}
    pg.evaluate(JUMP, {'c': [34.8, 32.08], 'z': 12})
    center_map(pg)
    hb = pg.locator('.nlurm-home button')
    (hb.tap if mob else hb.click)()
    time.sleep(1.4)
    out['home_button'] = {'zoom_from': 12, 'zoom_after': round(pg.evaluate(STATE)['z'], 2)}
    # 6. drag, wheel, one-finger page scroll
    pg.evaluate(JUMP, {'c': [34.9, 31.9], 'z': 7})
    center_map(pg)
    spots = pg.evaluate("""() => { const cr = document.getElementById('nlurm-map').getBoundingClientRect(); let empty = null, label = null;
      for (let i=1;i<10 && !empty;i++) for (let j=2;j<8 && !empty;j++) { const x = cr.left + cr.width*i/10, y = cr.top + cr.height*j/10;
        if (!document.elementsFromPoint(x,y).some(e => e.closest && (e.closest('.nlurm-lb .tg') || e.closest('.mapboxgl-ctrl') || e.closest('.nlurm-peek') || e.closest('#nlcta')))) empty = {x, y}; }
      for (const b of document.querySelectorAll('.nlurm-lb .tg')) { if (b.style.display === 'none') continue; const r = b.getBoundingClientRect(); const x=(r.left+r.right)/2, y=(r.top+r.bottom)/2;
        if (x>cr.left+10&&x<cr.right-10&&y>cr.top+10&&y<cr.bottom-10 && document.elementFromPoint(x,y) && document.elementFromPoint(x,y).closest('.tg') === b) { label = {x, y}; break; } }
      return {empty, label}; }""")
    out['spots'] = spots
    if not mob:
        if spots['empty']:
            s0 = pg.evaluate(STATE)
            x, y = spots['empty']['x'], spots['empty']['y']
            pg.mouse.move(x, y)
            pg.mouse.down()
            for k in range(1, 11):
                pg.mouse.move(x - 15 * k, y + 4 * k)
                time.sleep(0.03)
            pg.mouse.up()
            time.sleep(1.0)
            s1 = pg.evaluate(STATE)
            out['drag_pan'] = {'moved_lng': round(s1['lng'] - s0['lng'], 4), 'pans': abs(s1['lng'] - s0['lng']) > 0.01, 'opened_city': pg.evaluate("!!document.querySelector('.nlurm-side .ct')")}
            pg.evaluate(JUMP, {'c': [34.9, 31.9], 'z': 7})
        for where in ('empty', 'label'):
            if not spots.get(where):
                continue
            center_map(pg)
            s0 = pg.evaluate(STATE)
            pg.mouse.move(spots[where]['x'], spots[where]['y'])
            time.sleep(0.1)
            pg.mouse.wheel(0, 450)
            time.sleep(1.0)
            s1 = pg.evaluate(STATE)
            out['wheel_' + where] = {'page_scrolled_px': round(s1['sy'] - s0['sy']), 'map_zoom_change': round(s1['z'] - s0['z'], 3)}
    else:
        def swipe(x, y, dy=-250, steps=12):
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'id': 1}]})
            for k in range(1, steps + 1):
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y + dy * k / steps, 'id': 1}]})
                time.sleep(0.016)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        center_map(pg)
        top = pg.evaluate("document.querySelector('.nlurm-v2').getBoundingClientRect().top")
        for where in ('control_above_map', 'empty', 'label', 'chips', 'peek'):
            center_map(pg)
            if where == 'peek':
                t2 = find_tag(pg, [n for n in ['תל אביב יפו', 'רמת גן', 'ירושלים', 'חיפה', 'נתניה', 'באר שבע', 'אשדוד']])
                if not t2:
                    continue
                pg.touchscreen.tap(t2['x'], t2['y'])
                time.sleep(0.8)
                center_map(pg)
                pt = pg.evaluate("(() => { const p = document.querySelector('.nlurm-peek'); if (!p || p.style.display === 'none') return null; const r = p.getBoundingClientRect(); return {x: r.left + 60, y: r.top + 30}; })()")
            elif where == 'chips':
                pt = pg.evaluate("(() => { const r = document.querySelector('.nlurm-bar .nlurm-chips').getBoundingClientRect(); return {x: r.left + r.width/2, y: r.top + r.height/2}; })()")
            elif where == 'control_above_map':
                pt = {'x': 120, 'y': max(30, top - 60)}
            else:
                pt = spots.get(where)
            if not pt or pt['y'] < 10:
                continue
            s0 = pg.evaluate(STATE)
            swipe(pt['x'], pt['y'])
            time.sleep(1.2)
            s1 = pg.evaluate(STATE)
            out['swipe_' + where] = {'page_scrolled_px': round(s1['sy'] - s0['sy']), 'map_moved': abs(s1['lng'] - s0['lng']) + abs(s1['lat'] - s0['lat']) > 1e-4, 'map_zoom_change': round(s1['z'] - s0['z'], 3)}
    return out


def interactions_before(pg, mob, cdp):
    out = {}
    pg.evaluate(JUMP, {'c': [34.80, 32.07], 'z': 11})
    center_map(pg)
    target = pg.evaluate("""() => { const cr = document.getElementById('nlurm-map').getBoundingClientRect();
      for (const w of ['גבעתים', 'רמת גן', 'תל אביב יפו', 'בני ברק', 'חולון']) for (const el of document.querySelectorAll('.nlurm-pin')) { if (el.textContent.split(' · ')[0] !== w) continue;
        const r = el.getBoundingClientRect(); const x = (r.left+r.right)/2, y = (r.top+r.bottom)/2; if (x>cr.left&&x<cr.right&&y>cr.top&&y<cr.bottom&&document.elementFromPoint(x,y).closest('.nlurm-pin')===el) return {city: w, x, y}; }
      return null; }""")
    out['city_tap_target'] = target
    if target:
        (pg.touchscreen.tap if mob else pg.mouse.click)(target['x'], target['y'])
        try:
            pg.wait_for_function("document.querySelector('#nlurm-list .nlur-hit') && !/טוענים/.test(document.querySelector('#nlurm-list').textContent)", timeout=15000)
        except Exception:
            pass
        out['list'] = pg.evaluate("() => ({items: document.querySelectorAll('#nlurm-list .nlur-hit a').length, text: document.querySelector('#nlurm-list').innerText.replace(/\\s+/g,' ').slice(0,160)})")
    pg.evaluate(JUMP, {'c': [34.9, 31.9], 'z': 7})
    center_map(pg)
    z0 = pg.evaluate(STATE)['z']
    pg.locator('.mapboxgl-ctrl-zoom-in').click()
    time.sleep(1.2)
    out['zoom_button'] = {'before': round(z0, 2), 'after': round(pg.evaluate(STATE)['z'], 2)}
    return out


def check_links(hrefs, n=6):
    random.seed(26)
    pick = random.sample(hrefs, min(n, len(hrefs)))
    res = []
    for h in pick:
        u = 'https://nad-lan.co.il' + h
        try:
            req = urllib.request.Request(u, headers={'User-Agent': lib2.UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                body = r.read(250000).decode('utf-8', 'replace')
                t = body[body.find('<title>') + 7: body.find('</title>')][:90] if '<title>' in body else ''
                res.append({'href': h, 'status': r.status, 'final': r.geturl() == u, 'title': t})
        except Exception as e:  # noqa: BLE001
            res.append({'href': h, 'error': str(e)[:120]})
    return res


def main():
    cities = [[c['city'], c['lnglat'][0], c['lnglat'][1]] for c in json.load(open(os.path.join(HERE, 'cache', 'renewal-map-data.json'), encoding='utf-8'))['cities'] if c.get('lnglat')]
    results = {'at_utc': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), 'live_url': lib2.LIVE_URL, 'views': {}}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME, headless=True, args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        for vname, w, h, mob, dsf in VIEWS:
            for mode in (('after',) if os.environ.get('STATES_ONLY') else ('before', 'after')):
                ctx = br.new_context(viewport={'width': w, 'height': h}, is_mobile=mob, has_touch=mob, device_scale_factor=dsf, locale='he-IL')
                ctx.add_init_script(HOOK)
                blocked = {'n': 0}
                net = {'lookup': [], 'track': 0, 'rtl': 0, 'map_data': 0}

                def make_guard(_mode):
                    def guard(route):
                        return _guard(route, _mode)
                    return guard

                def _guard(route, _mode):
                    r = route.request
                    u = r.url
                    if any(hh in u for hh in BLOCK_HOSTS) or ('nad-lan.co.il' in u and r.method != 'GET'):
                        blocked['n'] += 1
                        return route.abort()
                    if _mode == 'after' and r.resource_type == 'document' and u.split('?')[0].rstrip('/') == lib2.LIVE_URL.rstrip('/'):
                        resp = route.fetch()
                        return route.fulfill(response=resp, body=lib2.swapped_live_page(resp.text()), headers={**resp.headers, 'content-type': 'text/html; charset=UTF-8'})
                    return route.continue_()
                ctx.route('**/*', make_guard(mode))
                pg = ctx.new_page()
                errs = []
                pg.on('pageerror', lambda e, _e=errs: _e.append(str(e)[:200]))

                def on_req(rq, _n=net):
                    u = rq.url
                    if 'renewal-track.json' in u:
                        _n['track'] += 1
                    if 'mapbox-gl-rtl-text' in u:
                        _n['rtl'] += 1
                    if 'renewal-map-data' in u:
                        _n['map_data'] += 1
                pg.on('request', on_req)
                pg.on('response', lambda r, _n=net: _n['lookup'].append(r.status) if 'renewal-lookup' in r.url else None)
                cdp = ctx.new_cdp_session(pg)
                pg.goto(lib2.LIVE_URL + '?v2proof=' + mode, wait_until='domcontentloaded', timeout=90000)
                t_ready = wait_ready(pg, mode)
                pg.add_style_tag(content=STATIC_HEADER)
                center_map(pg)
                rec = {'ms_to_labels': t_ready, 'states': {}}
                for zname, c, z in ZOOMS:
                    if c:
                        pg.evaluate(JUMP, {'c': c, 'z': z})
                        center_map(pg)
                    m = pg.evaluate(MEASURE, {'mode': mode, 'cities': cities})
                    shot = os.path.join(HERE, '%s-%s-%s.png' % (mode, vname, zname))
                    pg.locator('#nlurm-map').screenshot(path=shot)
                    if mode == 'after':
                        pg.locator('.nlurm-v2').screenshot(path=os.path.join(HERE, 'after-%s-%s-full.png' % (vname, zname)))
                    m['contrast_pixels'] = pixel_contrast(shot, m.pop('boxes'), dsf)
                    rec['states'][zname] = m
                    print(vname, mode, zname, 'in view', m['in_view'], 'shown', m['shown'], 'names', m['names_n'], 'complete', len(m['complete']), 'facts', m['facts'], 'per tag', m['facts_per_tag'],
                          'overlaps', m['overlaps'], 'tap', m['tap_min_w'], m['tap_min_h'], 'tap overlaps', m['tap_overlaps'], 'ambiguous', m['ambiguous'], 'over lines', m['over_lines'],
                          'contrast min', min(m['contrast_text'] or [0]), min(m['contrast_facts'] or [0]), 'px median', statistics.median(m['contrast_pixels']) if m['contrast_pixels'] else None, m.get('tiers'))
                rec['interactions'] = {} if os.environ.get('STATES_ONLY') else (interactions_after(pg, mob, cdp, vname) if mode == 'after' else interactions_before(pg, mob, cdp))
                print(vname, mode, 'interactions', json.dumps(rec['interactions'], ensure_ascii=False)[:2500])
                rec['page_errors'] = errs
                rec['network'] = net
                rec['blocked_requests'] = blocked['n']
                results['views'].setdefault(vname, {})[mode] = rec
                ctx.close()
        br.close()
    # the complex links of the panel: a sample, GET (not the lookup), status and title
    links = [] if os.environ.get('STATES_ONLY') else (results['views'].get('1280', {}).get('after', {}).get('interactions', {}).get('city', {}).get('links_all') or [])
    results['link_check'] = check_links(links) if links else []
    json.dump(results, open(os.path.join(HERE, 'out' if os.environ.get('STATES_ONLY') else '', 'proof-results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('links', json.dumps(results['link_check'], ensure_ascii=False))
    print('written proof-results.json')


if __name__ == '__main__':
    main()
