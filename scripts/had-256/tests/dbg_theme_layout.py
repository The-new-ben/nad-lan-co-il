"""debug (theme bench): where the first field sits on the first screen at 390x844, and what each block above it costs"""
import json, os, sys
from bench import Browser, reset, page_url
V = 'theme'
br = Browser()
try:
    reset(V)
    for lang in ('he', 'en'):
        ctx = br.ctx('390', lang); page = ctx.new_page()
        page.goto(page_url(V, lang)); page.wait_for_selector('#nlj-signup'); page.wait_for_timeout(600)
        out = page.evaluate('''() => {
          const r = e => { if (!e) return null; const b = e.getBoundingClientRect(); return [Math.round(b.top), Math.round(b.bottom)]; };
          const q = s => document.querySelector(s);
          const blocks = Array.from(document.querySelectorAll('main .entry-content > *')).map(e => [e.tagName.toLowerCase() + '.' + String(e.className).split(' ')[0], r(e)]);
          const app = q('#nlj-app');
          const inner = app ? Array.from(app.querySelectorAll('.nlj-wrap > *, .nlj-bar, .nlj-head > *, .nlj-card > *')).slice(0, 14).map(e => [e.tagName.toLowerCase() + '.' + String(e.className).split(' ')[0] + (e.id ? '#' + e.id : ''), r(e), (e.innerText || '').trim().slice(0, 40)]) : [];
          return {header: r(q('.nlhp-top')), h1: r(q('main h1')), blocks, inner, first_input: r(q('#j-name')), bar: r(q('#nlcta .nlcta-wa')), a11y: r(q('#nla11y-btn')), vh: innerHeight};
        }''')
        print(lang, json.dumps(out, ensure_ascii=False, indent=0))
        ctx.close()
finally:
    br.close()
