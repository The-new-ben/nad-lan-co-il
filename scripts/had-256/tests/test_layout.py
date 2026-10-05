"""L14 (layout, the floating bar, targets, focus, contrast) on every screen, real Chrome + real WordPress (bench).

The floating "ייעוץ חינם" bar is the site's own #nlcta from inc/conversion-cta.php (the real markup and CSS; on the
bench it shows the module's fallback words "לפרטים נוספים" because inc/i18n.php is not loaded).
Per screen, language and width:
  bar      every focusable element in the journey is focused (the browser scrolls it into view, as a keyboard user
           sees it); document.elementFromPoint at its centre must be the element or inside it, never the bar or
           anything else; the element must be inside the viewport.
  overflow no horizontal scroll (document.scrollWidth <= innerWidth).
  targets  buttons, inputs, selects, checkboxes' labels and stand-alone links at least 44x44 (links inside running
           text are listed apart: WCAG 2.5.8 exempts them).
  focus    a focused control shows an outline or a box-shadow ring.
  contrast every text node: computed colour on the effective background (alpha-blended up the ancestors); 4.5:1,
           or 3:1 for 24px+ or 18.66px+ bold; placeholders too; disabled controls listed apart (WCAG exempts them).
    python test_layout.py                 # every width, he and en
    python test_layout.py 390 he          # one
"""
import json
import sys

from bench import Browser, record, shot, clear, QA
from screens import visit

WIDTHS = ['320', '360', '390', '412', '1440']
SHOT_SETS = {('390', 'he'), ('320', 'he'), ('390', 'en'), ('1440', 'he')}

PROBE = r"""
() => {
  const app = document.getElementById('nlj-app');
  const bar = document.getElementById('nlcta');
  const out = {bar: [], offscreen: [], overflow: null, small: [], inline_small: [], nofocus: [], contrast: [], contrast_exempt: [], checked: {focus: 0, text: 0}};
  out.overflow = {scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth};
  out.bar_present = !!bar && getComputedStyle(bar).display !== 'none';
  const sel = 'a[href],button,input:not([type=hidden]):not(.nlj-file),select,textarea,summary,[tabindex]:not([tabindex="-1"])';
  const shut = e => { const d = e.closest('details'); return d && !d.open && !e.closest('summary'); };   // inside a closed <details>: not shown, not focusable
  const els = Array.from(app.querySelectorAll(sel)).filter(e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return (r.width > 0 && r.height > 0) && cs.visibility !== 'hidden' && !e.closest('[hidden]') && !e.closest('[aria-hidden="true"]') && !shut(e); });
  const name = e => (e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.getAttribute('data-act') ? '[' + e.getAttribute('data-act') + ']' : '') + ' "' + (e.innerText || e.value || e.getAttribute('aria-label') || '').trim().slice(0, 40) + '"');
  for (const e of els) {
    out.checked.focus++;
    e.focus({preventScroll: false});
    if (document.activeElement !== e) { e.scrollIntoView({block: 'nearest'}); }
    const r = e.getBoundingClientRect();
    const rs = e.getClientRects(); const r0 = rs.length > 1 ? rs[0] : r;   // a link that wraps: the centre of its first line box
    const cx = r0.left + r0.width / 2, cy = r0.top + r0.height / 2;
    if (cy < 0 || cy > innerHeight || cx < 0 || cx > innerWidth) { out.offscreen.push(name(e)); continue; }
    const hit = document.elementFromPoint(cx, cy);
    const label = e.closest('label');
    if (!hit || !(hit === e || e.contains(hit) || (label && label.contains(hit)))) {
      out.bar.push({el: name(e), covered_by: hit ? (hit.closest('#nlcta') ? '#nlcta (the floating bar)' : hit.tagName.toLowerCase() + '.' + hit.className) : null});
    }
    // focus ring
    if (document.activeElement === e) {
      const cs = getComputedStyle(e);
      const ring = (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) || (cs.boxShadow && cs.boxShadow !== 'none');
      if (!ring && !(e.type === 'checkbox' || e.type === 'radio')) { out.nofocus.push(name(e)); }
    }
    // target size
    const inText = e.tagName === 'A' && e.closest('p,li,small') && !e.classList.contains('nlj-btn');
    const tr = (e.type === 'checkbox' || e.type === 'radio') && label ? label.getBoundingClientRect() : r;
    if (tr.width < 43.5 || tr.height < 43.5) { (inText ? out.inline_small : out.small).push(name(e) + ' ' + Math.round(tr.width) + 'x' + Math.round(tr.height)); }
  }
  const e0 = document.activeElement; if (e0 && e0.blur) { e0.blur(); }
  // contrast
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(x => parseFloat(x)); return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const blend = (top, bot) => ({r: top.r * top.a + bot.r * (1 - top.a), g: top.g * top.a + bot.g * (1 - top.a), b: top.b * top.a + bot.b * (1 - top.a), a: 1});
  const bgOf = el => {
    const layers = [];
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') { return {img: true}; }
      const c = parse(cs.backgroundColor);
      if (c && c.a > 0) { layers.push(c); if (c.a >= 1) break; }
    }
    let acc = {r: 255, g: 255, b: 255, a: 1};
    for (let i = layers.length - 1; i >= 0; i--) { acc = blend(layers[i], acc); }
    return acc;
  };
  const walker = document.createTreeWalker(app, NodeFilter.SHOW_TEXT, {acceptNode: n => n.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT});
  const seen = new Set();
  const check = (el, txt, colorStr, tag) => {
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) return;
    const r = el.getBoundingClientRect(); if (r.width === 0 || r.height === 0) return;
    if (el.closest('.nlj-sr,.nlj-file')) return;
    const key = el.tagName + '|' + txt.slice(0, 30) + '|' + colorStr;
    if (seen.has(key)) return; seen.add(key);
    out.checked.text++;
    const bg = bgOf(el);
    if (bg.img) { out.contrast_exempt.push({text: txt.slice(0, 40), why: 'over an image'}); return; }
    let fg = parse(colorStr); if (!fg) return;
    let op = 1; for (let n = el; n && n.nodeType === 1; n = n.parentElement) { op *= parseFloat(getComputedStyle(n).opacity); }
    fg = blend({r: fg.r, g: fg.g, b: fg.b, a: fg.a * op}, bg);
    const L1 = lum(fg), L2 = lum(bg), ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight, 10) >= 700;
    const large = size >= 24 || (bold && size >= 18.66);
    const need = large ? 3 : 4.5;
    if (ratio + 1e-6 < need) {
      const row = {text: txt.slice(0, 50), where: tag, ratio: Math.round(ratio * 100) / 100, need, size: size, bold, fg: colorStr, bg: 'rgb(' + Math.round(bg.r) + ',' + Math.round(bg.g) + ',' + Math.round(bg.b) + ')'};
      if (el.closest('[disabled],[aria-disabled="true"],fieldset[disabled]')) { out.contrast_exempt.push(Object.assign(row, {why: 'disabled control'})); } else { out.contrast.push(row); }
    }
  };
  let n; while ((n = walker.nextNode())) { const el = n.parentElement; if (shut(el)) continue; check(el, n.nodeValue.trim(), getComputedStyle(el).color, el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : '')); }
  for (const i of app.querySelectorAll('input[placeholder],textarea[placeholder]')) { if (!i.value && i.placeholder) check(i, 'placeholder: ' + i.placeholder, getComputedStyle(i, '::placeholder').color, 'placeholder'); }
  return out;
}
"""


def main(widths, langs):
    br = Browser()
    allrows = {}
    try:
        for lang in langs:
            for vp in widths:
                found = {}

                def on_screen(page, name, vp=vp, lang=lang):
                    page.evaluate('() => window.scrollTo(0, 0)')
                    if (vp, lang) in SHOT_SETS:
                        shot(page, 'after', 'L14-%s-%s-%s' % (name, vp, lang), full=True)
                    found[name] = page.evaluate(PROBE)
                errs = visit(br, lang, vp, on_screen)
                allrows['%s-%s' % (vp, lang)] = {'screens': found, 'js_errors': errs}
                bar = {k: v['bar'] for k, v in found.items() if v['bar']}
                off = {k: v['offscreen'] for k, v in found.items() if v['offscreen']}
                ovf = {k: v['overflow'] for k, v in found.items() if v['overflow']['scrollWidth'] > v['overflow']['innerWidth']}
                small = {k: v['small'] for k, v in found.items() if v['small']}
                nof = {k: v['nofocus'] for k, v in found.items() if v['nofocus']}
                con = {k: v['contrast'] for k, v in found.items() if v['contrast']}
                present = all(v['bar_present'] for v in found.values())
                checked = sum(v['checked']['focus'] for v in found.values())
                texts = sum(v['checked']['text'] for v in found.values())
                record({'id': 'L14', 'variant': 'after', 'label': 'real-wp+chrome', 'title': 'the floating bar never covers a focused control (%s px, %s)' % (vp, lang), 'status': 'pass' if present and not bar and not off else 'fail',
                        'evidence': {'bar_on_every_screen': present, 'controls_focused': checked, 'covered': bar, 'outside_viewport_after_focus': off, 'screens': list(found)}})
                record({'id': 'L14', 'variant': 'after', 'label': 'real-wp+chrome', 'title': 'no horizontal overflow, 44 px targets, visible focus, no JS errors (%s px, %s)' % (vp, lang), 'status': 'pass' if not ovf and not small and not nof and not errs else 'fail',
                        'evidence': {'overflow': ovf, 'under_44px': small, 'inline_links_under_44px (exempt)': {k: v['inline_small'] for k, v in found.items() if v['inline_small']}, 'no_focus_ring': nof, 'js_errors': errs}})
                record({'id': 'L14', 'variant': 'after', 'label': 'real-wp+chrome', 'title': 'text contrast 4.5:1 (3:1 large) on computed colours (%s px, %s)' % (vp, lang), 'status': 'pass' if not con else 'fail',
                        'evidence': {'text_nodes_checked': texts, 'under': con, 'exempt': {k: v['contrast_exempt'] for k, v in found.items() if v['contrast_exempt']}}})
    finally:
        br.close()
    (QA / 'layout-probe.json').write_text(json.dumps(allrows, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    w = [a for a in sys.argv[1:] if a.isdigit()] or WIDTHS
    l = [a for a in sys.argv[1:] if a in ('he', 'en')] or ['he', 'en']
    for vp in w:
        for lang in l:
            clear('L14', 'after', 'the floating bar never covers a focused control (%s px, %s)' % (vp, lang))
    main(w, l)
