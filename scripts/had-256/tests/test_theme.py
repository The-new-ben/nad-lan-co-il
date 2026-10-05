"""T4 (open item 4): the journey inside the site's REAL theme, real Chrome, the theme bench (start.mjs theme 2ce0a741 9405).

The bench runs snapshot 3 (owner-wizard 2.0.0 + broker-drop 1.1.4, LF bytes = the QA-SNAPSHOT-3 hashes) as Code
Snippets on top of the real nadlan-config plugin and the real themes (nadlan-revenue + nadlan-platform-child, the
child's platform.css = the live public bytes), Hebrew RTL as on the live site. Per screen, language and width:
  page     exactly one visible H1 in the document; the site header (.nlhp-top) and footer (.nlpc-site-footer) present;
           the site's floating bar (#nlcta) and accessibility button (#nla11y-btn) present (their boxes recorded)
  overlap  every focusable control of the journey is focused, forward (Tab) and then backward (Shift+Tab), and measured
           once the site's smooth scroll has settled: its own box must not intersect #nlcta, #nla11y-btn or a
           sticky/fixed site header (stricter than a centre test; a checkbox's long label under an overlay is info),
           elementFromPoint at its centre must be the control, and it must be inside the viewport
  layout   the L14 probe: no horizontal overflow, 44 px targets, a visible focus ring, contrast 4.5:1 (3:1 large) in the app
  page text contrast of the page's own text around the app (the H1, the paragraph, the plugin's "how it works" box)
  chrome   contrast of the header and footer text (site-wide, reported as info, not a HAD-256 gate)
Screenshots (full page, JPEG) at 390x844 and 1440x900 for he and en: docs/qa/had-256/theme/<lang>-<width>/.
    python test_theme.py                # 320, 390, 412, 1440 x he, en (shots at 390 and 1440)
    python test_theme.py 390 he
"""
import json
import os
import sys

from bench import Browser, record, clear, QA, REPO, bench
from screens import visit
from test_layout import PROBE as L14_PROBE

V = 'theme'   # the bench (bench.PORTS['theme'] = NLJ_THEME_PORT, default 9405)
TAG = os.environ.get('NLJ_THEME_TAG', '')   # e.g. "candidate-2.0.1" for another commit on another port: own rows, own folder
PAGE_VARIANT = os.environ.get('NLJ_PAGE_VARIANT', '')   # old | A | B: the text of page 4958 the bench serves (empty: as seeded)
RV = V + ('-' + TAG if TAG else '')
WIDTHS = ['320', '360', '390', '412', '1440']
SHOT_W = {'390', '1440'}
OUT = QA / 'theme' / TAG if TAG else QA / 'theme'

_old = "(hit.closest('#nlcta') ? '#nlcta (the floating bar)' :"
assert L14_PROBE.count(_old) == 1
PROBE = L14_PROBE.replace(_old, "(hit.closest('#nlcta') ? '#nlcta (the floating bar)' : hit.closest('#nla11y') ? '#nla11y (the accessibility button)' : hit.closest('.nlhp-top') ? '.nlhp-top (the site header)' :")

PAGE = r"""
async () => {
  // a smooth scroll may start a frame or two after focus(): wait 6 frames, then until scrollY is still for 6 frames (max ~2.5 s)
  const settle = async () => { let last = scrollY, same = 0; for (let i = 0; i < 150 && (i < 6 || same < 6); i++) { await new Promise(r => requestAnimationFrame(r)); const y = scrollY; same = (y === last) ? same + 1 : 0; last = y; } };
  const vis = e => { if (!e) return false; const r = e.getBoundingClientRect(), cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0; };
  const box = e => { if (!e) return null; const r = e.getBoundingClientRect(); return {x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height), pos: getComputedStyle(e).position}; };
  const h1s = Array.from(document.querySelectorAll('h1')).filter(vis).map(h => h.innerText.trim().slice(0, 80));
  const hdr = document.querySelector('.nlhp-top') || document.querySelector('header');
  const ftr = document.querySelector('.nlpc-site-footer') || document.querySelector('footer');
  const bar = document.getElementById('nlcta'), a11y = document.getElementById('nla11y-btn');
  const out = {h1: h1s, header: vis(hdr) ? (hdr.className || hdr.tagName) : null, footer: vis(ftr) ? (ftr.className || ftr.tagName) : null,
    bar: vis(bar) ? box(bar.querySelector('.nlcta-wa') || bar) : null, bar_text: bar ? bar.innerText.replace(/\s+/g, ' ').trim() : null,
    a11y: vis(a11y) ? box(a11y) : null, header_pos: hdr ? getComputedStyle(hdr).position : null,
    html: {lang: document.documentElement.lang, dir: document.documentElement.dir}, app: null, overlap: [], label_overlap: [], centre: [], offscreen: [], checked: 0, smooth: getComputedStyle(document.documentElement).scrollBehavior, page_contrast: [], chrome_contrast: [], text_checked: 0,
    page_blocks: Array.from(document.querySelectorAll('main .entry-content > *')).filter(vis).map(e => e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ')[0] : '') + (e.id ? '#' + e.id : '') + ' "' + (e.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 60) + '"')};
  const app = document.getElementById('nlj-app');
  window.scrollTo({top: 0, left: 0, behavior: 'instant'});   // a plain scrollTo is smooth on this site: start from a still page
  await settle();
  out.app = app ? {dir: app.getAttribute('dir'), lang: app.getAttribute('lang')} : null;
  out.how = {plugin_box: Array.from(document.querySelectorAll('.nlpub-how')).filter(vis).length, plugin_box_in_html: document.querySelectorAll('.nlpub-how').length,
             journey_box: Array.from(document.querySelectorAll('.nlj-aside--how')).filter(vis).length, any_how_h2: Array.from(document.querySelectorAll('h2')).filter(h => vis(h) && /איך זה עובד|מה קורה אחר כך|How it works|What comes next/.test(h.innerText)).map(h => h.innerText.trim())};
  const sh = document.querySelector('.nlj-shell');
  out.shell = sh ? {lang: sh.getAttribute('lang'), dir: sh.getAttribute('dir'), text: sh.innerText.trim().slice(0, 160)} : null;
  out.title = document.title;
  out.page_text = Array.from(document.querySelectorAll('main .entry-content > p, main .nlj-shell > p')).filter(vis).map(p => p.innerText.trim().slice(0, 140));
  if (bar && a11y && vis(bar) && vis(a11y)) {
    const b = (bar.querySelector('.nlcta-wa') || bar).getBoundingClientRect(), c = a11y.getBoundingClientRect();
    out.bar_a11y_overlap = Math.max(0, Math.min(b.right, c.right) - Math.max(b.left, c.left)) * Math.max(0, Math.min(b.bottom, c.bottom) - Math.max(b.top, c.top));
  }
  // overlap of every journey control (focused, scrolled as the keyboard does) with the fixed overlays
  const overlays = [['#nlcta', bar && (bar.querySelector('.nlcta-wa') || bar)], ['#nla11y-btn', a11y]];
  if (hdr && /fixed|sticky/.test(getComputedStyle(hdr).position)) overlays.push(['.nlhp-top (sticky header)', hdr]);
  if (app) {
    const sel = 'a[href],button,input:not([type=hidden]):not(.nlj-file),select,textarea,summary,[tabindex]:not([tabindex="-1"])';
    const shut = e => { const d = e.closest('details'); return d && !d.open && !e.closest('summary'); };
    const all = Array.from(app.querySelectorAll(sel)).filter(e => vis(e) && !e.closest('[hidden]') && !e.closest('[aria-hidden="true"]') && !shut(e));
    // a disabled control cannot take the focus (the promotion screen is switched off): listed apart, not a gate
    const els = all.filter(e => !(e.disabled || e.closest('fieldset[disabled]')));
    out.disabled_skipped = all.length - els.length;
    // forward = Tab (the page scrolls down to each control); then backward = Shift+Tab from the last one (the page scrolls
    // UP to each control: that is where a sticky header can cover it)
    // at rest (the first screen, nothing focused yet): which controls do the fixed overlays sit on? (info: a tap there
    // reaches the overlay; a focus scrolls the control clear)
    out.rest_overlap = [];
    for (const e of els) {
      const lab = (e.type === 'checkbox' || e.type === 'radio') && e.closest('label') ? e.closest('label') : e;
      const r = lab.getBoundingClientRect();
      for (const [name, o] of overlays) {
        if (!o || !vis(o)) continue;
        const q = o.getBoundingClientRect();
        const ix = Math.max(0, Math.min(r.right, q.right) - Math.max(r.left, q.left)), iy = Math.max(0, Math.min(r.bottom, q.bottom) - Math.max(r.top, q.top));
        if (ix * iy > 0.5) out.rest_overlap.push({el: e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + ' "' + (e.innerText || e.value || e.getAttribute('aria-label') || e.getAttribute('placeholder') || '').trim().slice(0, 30) + '"', under: name, area: Math.round(ix * iy), share: Math.round(100 * ix * iy / Math.max(1, r.width * r.height)) + '%'});
      }
    }
    // the first field of the screen at rest (what a phone shows before any tap)
    const ff = els.find(e => e.tagName === 'INPUT' && e.type !== 'checkbox' && e.type !== 'radio');
    if (ff) {
      const r = ff.getBoundingClientRect();
      const under = [];
      for (const [name, o] of overlays) { if (!o || !vis(o)) continue; const q = o.getBoundingClientRect(); const a = Math.max(0, Math.min(r.right, q.right) - Math.max(r.left, q.left)) * Math.max(0, Math.min(r.bottom, q.bottom) - Math.max(r.top, q.top)); if (a > 0.5) under.push(name + ' ' + Math.round(a) + 'px2'); }
      out.first_field = {el: ff.id || ff.name, top: Math.round(r.top), bottom: Math.round(r.bottom), in_view: r.bottom <= innerHeight, under};
    }
    const order = els.map(e => ['fwd', e]).concat(els.slice().reverse().map(e => ['back', e]));
    for (const [dir, e] of order) {
      out.checked++;
      e.focus({preventScroll: false});
      if (document.activeElement !== e) { e.scrollIntoView({block: 'nearest'}); }
      await settle();   // the site scrolls smoothly (html{scroll-behavior:smooth}): measure where the scroll ends
      const lab = (e.type === 'checkbox' || e.type === 'radio') && e.closest('label') ? e.closest('label') : e;
      const r = lab.getBoundingClientRect();
      const rs = e.getClientRects(), r0 = rs.length > 1 ? rs[0] : e.getBoundingClientRect();
      const cx = r0.left + r0.width / 2, cy = r0.top + r0.height / 2;
      const nm = e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.getAttribute('data-act') ? '[' + e.getAttribute('data-act') + ']' : '') + ' "' + (e.innerText || e.value || e.getAttribute('aria-label') || '').trim().slice(0, 30) + '"';
      if (cy < 0 || cy > innerHeight || cx < 0 || cx > innerWidth) { out.offscreen.push(dir + ' ' + nm); continue; }
      const hit = document.elementFromPoint(cx, cy);
      if (!hit || !(hit === e || e.contains(hit) || (lab !== e && lab.contains(hit)))) { out.centre.push({dir, el: nm, covered_by: hit ? (hit.closest('#nlcta') ? '#nlcta' : hit.closest('#nla11y') ? '#nla11y' : hit.closest('.nlhp-top') ? '.nlhp-top' : hit.tagName.toLowerCase() + '.' + String(hit.className).split(' ')[0]) : null}); }
      // the gate: the focused control's own box (for a checkbox the box itself); its label's box apart, as info
      const own = e.getBoundingClientRect();
      for (const [name, o] of overlays) {
        if (!o || !vis(o)) continue;
        const q = o.getBoundingClientRect();
        const area = rr => Math.max(0, Math.min(rr.right, q.right) - Math.max(rr.left, q.left)) * Math.max(0, Math.min(rr.bottom, q.bottom) - Math.max(rr.top, q.top));
        if (area(own) > 0.5) out.overlap.push({dir, el: nm, under: name, area: Math.round(area(own))});
        else if (lab !== e && area(r) > 0.5) out.label_overlap.push({dir, el: nm, under: name, label_area: Math.round(area(r))});
      }
    }
    const a = document.activeElement; if (a && a.blur) a.blur();
  }
  // contrast of the page's own text (outside the app) and of the site chrome
  const parse = c => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(x => parseFloat(x)); return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const blend = (t, b) => ({r: t.r * t.a + b.r * (1 - t.a), g: t.g * t.a + b.g * (1 - t.a), b: t.b * t.a + b.b * (1 - t.a), a: 1});
  const bgOf = el => { const L = []; for (let n = el; n && n.nodeType === 1; n = n.parentElement) { const cs = getComputedStyle(n); if (cs.backgroundImage && cs.backgroundImage !== 'none' && !/gradient/.test(cs.backgroundImage)) return {img: true}; const c = parse(cs.backgroundColor); if (c && c.a > 0) { L.push(c); if (c.a >= 1) break; } } let acc = {r: 255, g: 255, b: 255, a: 1}; for (let i = L.length - 1; i >= 0; i--) acc = blend(L[i], acc); return acc; };
  const scan = (root, sink, skip) => {
    if (!root) return;
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {acceptNode: n => n.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT});
    const seen = new Set(); let n;
    while ((n = w.nextNode())) {
      const el = n.parentElement; if (!el || (skip && skip.contains(el)) || el.closest('details:not([open]) > :not(summary)') || el.closest('[hidden],script,style,.screen-reader-text,.nlj-sr')) continue;
      if (!vis(el)) continue;
      const cs = getComputedStyle(el); const txt = n.nodeValue.trim();
      const key = el.tagName + '|' + txt.slice(0, 30) + '|' + cs.color; if (seen.has(key)) continue; seen.add(key);
      out.text_checked++;
      const bg = bgOf(el); if (bg.img) continue;
      let fg = parse(cs.color); if (!fg) continue;
      let op = 1; for (let m = el; m && m.nodeType === 1; m = m.parentElement) op *= parseFloat(getComputedStyle(m).opacity);
      fg = blend({r: fg.r, g: fg.g, b: fg.b, a: fg.a * op}, bg);
      const L1 = lum(fg), L2 = lum(bg), ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
      const size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight, 10) >= 700, large = size >= 24 || (bold && size >= 18.66), need = large ? 3 : 4.5;
      if (ratio + 1e-6 < need) sink.push({text: txt.slice(0, 50), where: el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : ''), ratio: Math.round(ratio * 100) / 100, need, fg: cs.color, bg: 'rgb(' + Math.round(bg.r) + ',' + Math.round(bg.g) + ',' + Math.round(bg.b) + ')'});
    }
  };
  scan(document.querySelector('main'), out.page_contrast, app);
  scan(hdr, out.chrome_contrast, null);
  scan(ftr, out.chrome_contrast, null);
  return out;
}
"""


def main(widths, langs):
    if PAGE_VARIANT:
        s, j, _ = bench(V, '/page', {'variant': PAGE_VARIANT})
        assert s == 200, (s, j)
        print('[page] variant', PAGE_VARIANT, j)
    br = Browser()
    allrows = {}
    try:
        for lang in langs:
            for vp in widths:
                found, shots = {}, []

                def on_screen(page, name, vp=vp, lang=lang):
                    page.wait_for_timeout(250)
                    page.evaluate("() => window.scrollTo({top: 0, left: 0, behavior: 'instant'})")
                    if vp in SHOT_W:
                        d = OUT / ('%s-%s' % (lang, vp))
                        d.mkdir(parents=True, exist_ok=True)
                        n = len(shots) // 2 + 1
                        p = d / ('%02d-%s.jpg' % (n, name))
                        page.screenshot(path=str(p), full_page=True, type='jpeg', quality=70)
                        shots.append(str(p.relative_to(REPO)).replace('\\', '/'))
                        page.wait_for_timeout(150)
                        q = d / ('%02d-%s-view.jpg' % (n, name))   # the first screen as the visitor sees it (the fixed bar and button where they really are)
                        page.screenshot(path=str(q), full_page=False, type='jpeg', quality=75)
                        shots.append(str(q.relative_to(REPO)).replace('\\', '/'))
                    pg = page.evaluate(PAGE)
                    page.evaluate("() => window.scrollTo({top: 0, left: 0, behavior: 'instant'})")
                    page.evaluate("() => { const s = document.createElement('style'); s.id = 'nlj-probe-instant'; s.textContent = 'html{scroll-behavior:auto!important}'; document.head.appendChild(s); }")
                    l14 = page.evaluate(PROBE)
                    page.evaluate("() => { const s = document.getElementById('nlj-probe-instant'); if (s) s.remove(); window.scrollTo(0, 0); }")
                    found[name] = {'page': pg, 'l14': l14}
                errs = visit(br, lang, vp, on_screen, V=V)
                key = '%s-%s' % (vp, lang)
                allrows[key] = {'screens': found, 'js_errors': errs, 'shots': shots}
                pg = {k: v['page'] for k, v in found.items()}
                l14 = {k: v['l14'] for k, v in found.items()}
                h1_bad = {k: v['h1'] for k, v in pg.items() if len(v['h1']) != 1}
                chrome_missing = {k: {'header': v['header'], 'footer': v['footer'], 'bar': bool(v['bar']), 'a11y': bool(v['a11y'])} for k, v in pg.items() if not (v['header'] and v['footer'] and v['bar'] and v['a11y'])}
                overlap = {k: v['overlap'] for k, v in pg.items() if v['overlap']}
                covered = {k: v['centre'] for k, v in pg.items() if v['centre']}
                off = {k: v['offscreen'] for k, v in pg.items() if v['offscreen']}
                covered_i = {k: v['bar'] for k, v in l14.items() if v['bar']}
                off_i = {k: v['offscreen'] for k, v in l14.items() if v['offscreen']}
                ovf = {k: v['overflow'] for k, v in l14.items() if v['overflow']['scrollWidth'] > v['overflow']['innerWidth']}
                small = {k: v['small'] for k, v in l14.items() if v['small']}
                nof = {k: v['nofocus'] for k, v in l14.items() if v['nofocus']}
                con = {k: v['contrast'] for k, v in l14.items() if v['contrast']}
                pcon = {k: v['page_contrast'] for k, v in pg.items() if v['page_contrast']}
                rest = {k: v.get('rest_overlap') for k, v in pg.items() if v.get('rest_overlap')}
                labels = {k: v.get('label_overlap') for k, v in pg.items() if v.get('label_overlap')}
                ccon = {k: v['chrome_contrast'] for k, v in pg.items() if v['chrome_contrast']}
                t = '(%s px, %s, real theme)' % (vp, lang)
                record({'id': 'T4', 'variant': RV, 'label': 'real-wp+theme+chrome', 'title': 'one H1, the site header, footer, floating bar and accessibility button on every screen ' + t,
                        'status': 'pass' if not h1_bad and not chrome_missing else 'fail',
                        'evidence': {'screens': list(found), 'h1_not_one': h1_bad, 'missing': chrome_missing, 'h1_text': sorted({h for v in pg.values() for h in v['h1']}),
                                     'html': sorted({json.dumps(v['html']) for v in pg.values()}), 'app': sorted({json.dumps(v['app']) for v in pg.values()}),
                                     'bar_text': sorted({v['bar_text'] or '' for v in pg.values()}), 'bar_box': next(iter(pg.values()))['bar'], 'a11y_box': next(iter(pg.values()))['a11y'],
                                     'bar_a11y_overlap_px2': sorted({v.get('bar_a11y_overlap') for v in pg.values()}, key=str), 'header_position': next(iter(pg.values()))['header_pos'], 'shots': shots}})
                record({'id': 'T4', 'variant': RV, 'label': 'real-wp+theme+chrome', 'title': 'no journey control under the floating bar, the accessibility button or the header ' + t,
                        'status': 'pass' if not overlap and not covered and not off else 'fail',
                        'evidence': {'controls_focused': sum(v['checked'] for v in pg.values()), 'scroll_behavior': sorted({v['smooth'] for v in pg.values()}), 'box_overlap': overlap, 'centre_covered': covered, 'outside_viewport_after_focus': off, 'first_screen_overlays_on_controls (info)': rest, 'label_text_under_an_overlay_while_its_checkbox_is_clear (info)': labels,
                                     'instant_scroll_L14 (info)': {'centre_covered': covered_i, 'outside_viewport': off_i}}})
                record({'id': 'T4', 'variant': RV, 'label': 'real-wp+theme+chrome', 'title': 'no overflow, 44 px targets, focus ring, no JS errors, app text 4.5:1 ' + t,
                        'status': 'pass' if not ovf and not small and not nof and not errs and not con else 'fail',
                        'evidence': {'overflow': ovf, 'under_44px': small, 'no_focus_ring': nof, 'js_errors': errs, 'app_contrast_under': con, 'app_text_nodes': sum(v['checked']['text'] for v in l14.values())}})
                auth = [k for k in pg if k.startswith('auth-')]
                ff = {k: pg[k].get('first_field') for k in auth}
                # the landing screens a visitor opens (the sign-up form, and the sign-in form via ?screen=login); the
                # screens reached by a tap (recovery, the existing-email answer) are listed as info
                LANDING = ('auth-signup', 'auth-login')
                ff_bad = {k: v for k, v in ff.items() if k in LANDING and v and v.get('under')} if int(vp) < 768 else {}
                record({'id': 'T4', 'variant': RV, 'label': 'real-wp+theme+chrome', 'title': 'first screen: the first field is not under the floating bar or the accessibility button (phones) ' + t,
                        'status': 'pass' if not ff_bad else 'fail', 'evidence': {'page_variant': PAGE_VARIANT or 'seeded', 'first_field_at_rest': ff, 'under': ff_bad, 'applies': int(vp) < 768}})
                how = {k: v.get('how') for k, v in pg.items()}
                how_bad = {k: v for k, v in how.items() if v and (v['plugin_box'] or (k.startswith('auth-') and v['journey_box'] != 1))}
                record({'id': 'T4', 'variant': RV, 'label': 'real-wp+theme+chrome', 'title': 'one "how it works" box (the journey\'s own on the visitor screens, no plugin box) ' + t,
                        'status': 'pass' if not how_bad else 'fail', 'evidence': {'page_variant': PAGE_VARIANT or 'seeded', 'bad': how_bad, 'auth_screens': {k: how[k] for k in auth}}})
                shells = {k: (v.get('shell'), v.get('h1'), v.get('title'), v.get('page_text')) for k, v in pg.items() if k in ('auth-signup', 'details-empty', 'published')}
                lang_bad = {}
                for k, v in pg.items():
                    if lang == 'en' and not (v.get('shell') and v['shell'].get('lang') == 'en' and v['h1'] == ['List your property for sale or rent, free']):
                        lang_bad[k] = (v.get('shell'), v.get('h1'))
                    if lang == 'he' and v.get('shell'):
                        lang_bad[k] = ('a shell on the Hebrew page', v.get('shell'))
                record({'id': 'T4', 'variant': RV, 'label': 'real-wp+theme+chrome', 'title': 'the page around the journey speaks the journey\'s language (he: the page H1; en: an English shell, lang en) ' + t,
                        'status': 'pass' if not lang_bad else 'fail', 'evidence': {'page_variant': PAGE_VARIANT or 'seeded', 'bad': lang_bad, 'samples': shells}})
                record({'id': 'T4', 'variant': RV, 'label': 'real-wp+theme+chrome', 'title': 'the page text around the app 4.5:1 (H1, paragraph, how-it-works) ' + t,
                        'status': 'pass' if not pcon else 'fail',
                        'evidence': {'under': pcon, 'page_blocks': next(iter(pg.values()))['page_blocks'], 'site_chrome_under (info, site-wide)': ccon}})
    finally:
        br.close()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'theme-probe.json').write_text(json.dumps(allrows, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    w = [a for a in sys.argv[1:] if a.isdigit()] or WIDTHS
    l = [a for a in sys.argv[1:] if a in ('he', 'en')] or ['he', 'en']
    main(w, l)
