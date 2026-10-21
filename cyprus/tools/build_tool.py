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


def run_engine(tool_dir, inp, rules, fn='purchaseCost', extra=None):
    """Runs engine.js in Node. Arguments go through stdin as UTF-8 JSON (Hebrew text never touches the command line)."""
    args = [inp, rules] + ([extra] if extra is not None else [])
    js = ("const E=require(%s);let s='';process.stdin.setEncoding('utf8');process.stdin.on('data',d=>s+=d);"
          "process.stdin.on('end',()=>{const a=JSON.parse(s);process.stdout.write(JSON.stringify(E.%s(...a)))});"
          % (json.dumps(str(tool_dir / 'engine.js')), fn))
    res = subprocess.run(['node', '-e', js], input=json.dumps(args, ensure_ascii=False).encode('utf-8'),
                         capture_output=True, check=True)
    return json.loads(res.stdout.decode('utf-8'))


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


def pct(x):
    return '%.1f%%' % (round(x * 1000) / 10)


def neg(n):
    return ('−' + money(n)) if n else money(0)


def net_yield_section(lang, rules, T, pc_rules):
    ex = dict(rules['example'])
    r = run_engine(HERE / 'net-yield', ex, rules, 'netYield', pc_rules)
    lo, hi = pct(r['netYieldLow']), pct(r['netYieldHigh'])
    y = lo if lo == hi else lo + ' \u2013 ' + hi
    rows = [('gross', money(r['gross']), False), ('ghs', neg(r['ghs']), False),
            ('cy_tax', neg(r['cyTax']), False), ('expenses', neg(r['expenses']), False)]
    if ex['israelTrack']:
        rows.append(('il_tax', neg(r['ilTax']), False))
    rows.append(('net', money(r['net']), True))
    rows.append(('cost', rng(r['totalLow'], r['totalHigh']), False))
    body = ''.join('<tr class="cyx-row%s"><th scope="row">%s</th><td class="cyx-num"><bdi>%s</bdi></td><td class="cyx-rule">%s</td></tr>'
                   % (' cyx-row--total' if s else '', escape(T['rows'][k]), v, escape(T['rules_text'][k])) for k, v, s in rows)
    wa = 'https://wa.me/972525101555?text=' + re.sub(r'\s', '%20', T['wa_text'])
    city_chips = ''.join(chip('city', k, T['cities'][k], k == ex['city']) for k in rules['cities'])
    ils = '\u2066\u20AA{:,}\u2069'.format(round(r['netMonthly'] * rules['fx']['eur_ils']))
    monthly = T['net_monthly'].replace('{m}', '\u2066' + money(r['netMonthly']) + '\u2069').replace('{s}', ils)
    parts = [
        '<section class="cyx-tool" data-cyx-tool="net-yield" data-lang="%s" dir="rtl" data-rules="%s" data-pc-rules="%s" data-text="%s" data-example="%s">'
        % (lang, escape(json.dumps(rules, ensure_ascii=False)), escape(json.dumps(pc_rules, ensure_ascii=False)),
           escape(json.dumps(T, ensure_ascii=False)), escape(json.dumps(ex))),
        '<div class="cyx-tool__head"><h2 class="cyx-tool__title">%s</h2><p class="cyx-tool__lead">%s</p></div>' % (escape(T['title']), escape(T['lead'])),
        '<div class="cyx-panel">',
        '<div class="cyx-field cyx-field--wide"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div>' % (escape(T['f_city']), city_chips),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s</div></div>'
        % (escape(T['f_beds']), chip('beds', '1', T['c_beds_1'], ex['beds'] == '1'), chip('beds', '2', T['c_beds_2'], ex['beds'] == '2')),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s</div></div>'
        % (escape(T['f_deal']), chip('deal', 'resale', T['c_resale'], not ex['isNew']), chip('deal', 'new', T['c_new'], ex['isNew'])),
        '<div class="cyx-field"><label class="cyx-label" for="cyx-ny-price">%s</label><div class="cyx-money"><span>\u20AC</span><input id="cyx-ny-price" type="text" inputmode="numeric" autocomplete="off" value="{:,}"></div></div>'.replace('{:,}', '{:,}'.format(ex['price'])) % escape(T['f_price']),
        '<div class="cyx-field"><label class="cyx-label" for="cyx-ny-rent">%s</label><div class="cyx-money"><span>\u20AC</span><input id="cyx-ny-rent" type="text" inputmode="numeric" autocomplete="off" value="{:,}"></div></div>'.replace('{:,}', '{:,}'.format(ex['rent'])) % escape(T['f_rent']),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s%s</div></div>'
        % (escape(T['f_months']), chip('months', '12', '12', ex['months'] == 12), chip('months', '11', '11', ex['months'] == 11), chip('months', '10', '10', ex['months'] == 10)),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s</div></div>'
        % (escape(T['f_israel']), chip('israel', '15', T['c_israel_15'], ex['israelTrack']), chip('israel', 'none', T['c_israel_none'], not ex['israelTrack'])),
        '<div class="cyx-field cyx-field--wide"><label class="cyx-label" for="cyx-ny-expenses">%s</label><div class="cyx-money"><span>\u20AC</span><input id="cyx-ny-expenses" type="text" inputmode="numeric" autocomplete="off" value="%d"></div></div>'
        % (escape(T['f_expenses']), ex['expenses']),
        '</div>',
        '<div class="cyx-result" aria-live="polite"><div class="cyx-result__kicker">%s</div><bdi class="cyx-result__figure" data-out="yield">%s</bdi>'
        '<p class="cyx-result__line" data-out="monthly">%s</p><p class="cyx-result__line" data-out="gross">%s</p></div>'
        % (escape(T['kicker']), y, escape(monthly), escape(T['gross_line'].replace('{g}', pct(r['grossYield'])))),
        '<p class="cyx-example">%s</p>' % escape(T['preset_note']),
        '<div class="cyx-break-wrap"><table class="cyx-break"><thead><tr><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th></tr></thead><tbody>%s</tbody></table></div>'
        % (escape(T['th_item']), escape(T['th_amount']), escape(T['th_rule']), body),
        '<p class="cyx-source">%s</p>' % escape(T['source']),
        '<div class="cyx-next"><a class="cyx-cta" href="%s" target="_blank" rel="noopener">%s</a><span class="cyx-next__note">%s</span></div>'
        % (wa, escape(T['cta']), escape(T['cta_note'])),
        '</section>',
    ]
    return '\n'.join(parts)


def section_for(tool, lang, rules, T):
    if tool == 'purchase-cost':
        return purchase_cost_section(lang, rules, T)
    if tool == 'net-yield':
        pc = json.loads((HERE / 'purchase-cost' / 'rules.json').read_text(encoding='utf-8'))
        return net_yield_section(lang, rules, T, pc)
    if tool == 'bank-docs':
        import bank_section
        return bank_section.bank_docs_section(lang, rules, T, run_engine, HERE)
    if tool == 'vat5':
        import vat5_section
        return vat5_section.vat5_section(lang, rules, T, run_engine, HERE)
    raise SystemExit('unknown tool ' + tool)


ENGINES = {'purchase-cost': ['purchase-cost'], 'net-yield': ['purchase-cost', 'net-yield'], 'bank-docs': ['bank-docs'], 'vat5': ['vat5']}


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
    ap.add_argument('--after', type=int, default=2)
    a = ap.parse_args()
    tool_dir = HERE / a.tool
    rules = json.loads((tool_dir / 'rules.json').read_text(encoding='utf-8'))
    if a.ship and not rules.get('verified'):
        raise SystemExit('rules.json is not verified: refusing to build a shippable package')
    T = json.loads((tool_dir / f'text.{a.lang}.json').read_text(encoding='utf-8'))
    section = section_for(a.tool, a.lang, rules, T)
    out = Path(a.out)
    (out / 'cyx').mkdir(parents=True, exist_ok=True)
    shutil.copy(HERE / 'common.css', out / 'cyx' / 'common.css')
    for eng in ENGINES[a.tool]:
        shutil.copy(HERE / eng / 'engine.js', out / 'cyx' / ('engine-%s.js' % eng))
    shutil.copy(tool_dir / 'ui.js', out / 'cyx' / ('ui-%s.js' % a.tool))
    page = Path(a.copy).read_text(encoding='utf-8')
    page = inject_after_paragraph(page, section, a.after)
    head = FONTS + '<link rel="stylesheet" href="cyx/common.css">'
    page = page.replace('</head>', head + '</head>', 1)
    scripts = ''.join('<script src="cyx/engine-%s.js"></script>' % e for e in ENGINES[a.tool]) + '<script src="cyx/ui-%s.js"></script>' % a.tool
    page = page.replace('</body>', scripts + '</body>', 1)
    (out / f'{a.tool}.{a.lang}.html').write_text(page, encoding='utf-8')
    (out / f'{a.tool}.{a.lang}.section.html').write_text(section, encoding='utf-8')
    print('built', out / f'{a.tool}.{a.lang}.html')


if __name__ == '__main__':
    main()
