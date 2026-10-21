# -*- coding: utf-8 -*-
"""Builds a CY-PRUS Instruments tool section, server-rendered with its example already computed (so Google, AI crawlers
and visitors without JavaScript see real numbers), plus a local preview page made from a saved copy of the live host page.

  python build_tool.py purchase-cost --lang he --copy <live-copy.html> --out <preview-dir>

The example is computed by the SAME engine.js through Node, so the server text and the live calculator never disagree."""
import argparse
import json
import re
import shutil
import subprocess
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Hebrew:wght@400;600;700'
         '&family=IBM+Plex+Mono:wght@500&display=swap">')


def run_engine(tool_dir, inp, rules):
    js = ("const E=require(%s);process.stdout.write(JSON.stringify(E.purchaseCost(%s,%s)))"
          % (json.dumps(str(tool_dir / 'engine.js')), json.dumps(inp), json.dumps(rules)))
    return json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout)


def money(n):
    return '€{:,}'.format(int(n))


def rng(lo, hi):
    return '⁦' + (money(lo) if lo == hi else money(lo) + ' – ' + money(hi)) + '⁩'


def chip(name, value, label, on):
    return ('<button type="button" class="cyx-chip" role="radio" data-chip="%s" data-value="%s" aria-checked="%s">%s</button>'
            % (name, value, 'true' if on else 'false', escape(label)))


def purchase_cost_section(lang, rules, T):
    ex = dict(rules['example'])
    r = run_engine(HERE / 'purchase-cost', ex, rules)
    rows = [(T['rows']['vat'], money(r['vat']['amount']), T['vat_rule'][r['vat']['mode']], 'law'),
            (T['rows']['transfer'], money(r['transfer']['amount']), T['transfer_rule'][r['transfer']['mode']], 'law')]
    if rules['stamp_duty'].get('active'):
        rows.append((T['rows']['stamp'], money(r['stamp']['amount']), T['stamp_rule'], 'law'))
    for f in r['fixedFees']:
        rows.append((T['rows'][f['key']], money(f['amount']), T['fixed_rule'][f['key']], 'law'))
    for m in r['market']:
        rows.append((T['market'][m['key']]['label'], rng(m['low'], m['high']), T['market'][m['key']]['rule'], 'market'))
    body = ''.join('<tr class="cyx-row%s"><th scope="row">%s</th><td class="cyx-num"><bdi>%s</bdi></td><td class="cyx-rule">%s</td></tr>'
                   % (' cyx-row--market' if k == 'market' else '', escape(a), b, escape(c)) for a, b, c, k in rows)
    pct = round(r['extraLow'] / r['price'] * 100, 1)
    wa = 'https://wa.me/972525101555?text=' + re.sub(r'\s', '%20', T['wa_text'])
    u = rules['ui']
    return f'''<section class="cyx-tool" data-cyx-tool="purchase-cost" data-lang="{lang}" dir="{'rtl' if lang == 'he' else 'ltr'}"
 data-rules="{escape(json.dumps(rules, ensure_ascii=False))}" data-text="{escape(json.dumps(T, ensure_ascii=False))}" data-example="{escape(json.dumps(ex))}">
<div class="cyx-tool__head"><h2 class="cyx-tool__title">{escape(T['title'])}</h2><p class="cyx-tool__lead">{escape(T['lead'])}</p></div>
<div class="cyx-panel">
 <div class="cyx-field cyx-field--wide"><label class="cyx-label" for="cyx-pc-price">{escape(T['f_price'])}</label>
  <div class="cyx-money"><span>€</span><input id="cyx-pc-price" type="text" inputmode="numeric" autocomplete="off" value="{ex['price']:,}"></div>
  <input id="cyx-pc-price-range" class="cyx-range" type="range" min="{u['price_min']}" max="{u['price_max']}" step="{u['price_step']}" value="{ex['price']}" aria-label="{escape(T['f_price'])}"></div>
 <div class="cyx-field"><span class="cyx-label">{escape(T['f_deal'])}</span><div class="cyx-chips" role="radiogroup">{chip('deal', 'new', T['c_new'], ex['isNew'])}{chip('deal', 'resale', T['c_resale'], not ex['isNew'])}</div></div>
 <div class="cyx-field" data-field="vat"><span class="cyx-label">{escape(T['f_vat'])}</span><div class="cyx-chips" role="radiogroup">{chip('vat', 'standard', T['c_vat_standard'], not ex['reducedVat'])}{chip('vat', 'reduced', T['c_vat_reduced'], ex['reducedVat'])}</div></div>
 <div class="cyx-field" data-field="area" hidden><label class="cyx-label" for="cyx-pc-area">{escape(T['f_area'])}</label><input id="cyx-pc-area" class="cyx-input" type="number" inputmode="numeric" min="20" max="600" value="{ex['area']}"></div>
 <div class="cyx-field"><span class="cyx-label">{escape(T['f_buyers'])}</span><div class="cyx-chips" role="radiogroup">{chip('buyers', '1', T['c_buyers_1'], ex['buyers'] == 1)}{chip('buyers', '2', T['c_buyers_2'], ex['buyers'] == 2)}</div></div>
 <div class="cyx-field"><span class="cyx-label">{escape(T['f_mortgage'])}</span><div class="cyx-chips" role="radiogroup">{chip('mortgage', 'no', T['c_mortgage_no'], not ex['mortgage'])}{chip('mortgage', 'yes', T['c_mortgage_yes'], bool(ex['mortgage']))}</div></div>
 <div class="cyx-field" data-field="mortgage-amount" hidden><label class="cyx-label" for="cyx-pc-ltv">{escape(T['f_ltv'])}</label>
  <div class="cyx-inline"><input id="cyx-pc-ltv" class="cyx-range" type="range" min="10" max="80" step="5" value="{int(ex['ltv'] * 100)}"><bdi data-out="ltv">{int(ex['ltv'] * 100)}%</bdi><bdi data-out="mortgage"></bdi></div></div>
</div>
<div class="cyx-result" aria-live="polite"><div class="cyx-result__kicker">{escape(T['kicker'])}</div>
 <bdi class="cyx-result__figure" data-out="extra">{rng(r['extraLow'], r['extraHigh'])}</bdi>
 <p class="cyx-result__line" data-out="pct">{escape(T['pct'].replace('{p}', str(pct)))}</p>
 <p class="cyx-result__line" data-out="total">{escape(T['total'].replace('{t}', rng(r['totalLow'], r['totalHigh'])))}</p>
 <p class="cyx-result__line" data-out="ils"></p></div>
<p class="cyx-example">{escape(T['example'])}</p>
<div class="cyx-break-wrap"><table class="cyx-break"><thead><tr><th scope="col">{escape(T['th_item'])}</th><th scope="col">{escape(T['th_amount'])}</th><th scope="col">{escape(T['th_rule'])}</th></tr></thead><tbody>{body}</tbody></table></div>
<p class="cyx-source">{escape(T['source'])}</p>
<div class="cyx-next"><a class="cyx-cta" href="{wa}" target="_blank" rel="noopener">{escape(T['cta'])}</a><span class="cyx-next__note">{escape(T['cta_note'])}</span></div>
</section>'''


def inject_after_paragraph(page, section, n=2):
    """Places the tool after the n-th paragraph of the post content (answer first, tool second). Fails open."""
    i = page.find('wp-block-post-content')
    if i < 0:
        return page
    pos = i
    for _ in range(n):
        j = page.find('</p>', pos)
        if j < 0:
            return page
        pos = j + 4
    return page[:pos] + '\n' + section + '\n' + page[pos:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tool')
    ap.add_argument('--lang', default='he')
    ap.add_argument('--copy', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--ship', action='store_true')
    a = ap.parse_args()
    tool_dir = HERE / a.tool
    rules = json.loads((tool_dir / 'rules.json').read_text(encoding='utf-8'))
    if a.ship and not rules.get('verified'):
        raise SystemExit('rules.json is not verified: refusing to build a shippable package')
    T = json.loads((tool_dir / f'text.{a.lang}.json').read_text(encoding='utf-8'))
    section = purchase_cost_section(a.lang, rules, T)
    out = Path(a.out)
    (out / 'cyx').mkdir(parents=True, exist_ok=True)
    for f in ('engine.js', 'ui.js', 'style.css'):
        shutil.copy(tool_dir / f, out / 'cyx' / f)
    page = Path(a.copy).read_text(encoding='utf-8')
    page = inject_after_paragraph(page, section)
    head = FONTS + '<link rel="stylesheet" href="cyx/style.css">'
    page = page.replace('</head>', head + '</head>', 1)
    page = page.replace('</body>', '<script src="cyx/engine.js"></script><script src="cyx/ui.js"></script></body>', 1)
    (out / f'{a.tool}.{a.lang}.html').write_text(page, encoding='utf-8')
    (out / f'{a.tool}.{a.lang}.section.html').write_text(section, encoding='utf-8')
    print('built', out / f'{a.tool}.{a.lang}.html')


if __name__ == '__main__':
    main()
