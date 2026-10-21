# -*- coding: utf-8 -*-
"""Server-rendered section of the Cyprus price list (example computed by the same engine.js; the full city table is printed)."""
import json
import re
from html import escape

from bank_section import chip


def eur(n):
    return '⁦€{:,}⁩'.format(int(n))


def sgn(y):
    return '⁦%s%s%%⁩' % ('+' if y > 0 else '', y)


def pricelist_section(lang, R, T, run_engine, here):
    ex = dict(R['example'])
    r = run_engine(here / 'price-list', ex, R, 'lookup')
    me = r['me']
    rows = ''.join('<tr class="cyx-row%s"><th scope="row">%s</th>%s</tr>'
                   % (' cyx-row--total' if x['id'] == ex['city'] else '', escape(T['cities'][x['id']]),
                      ''.join('<td class="cyx-num"><bdi>%s</bdi></td>' % v for v in (
                          eur(x['r']['median']), eur(x['r']['m2']) if x['r']['m2'] else '—', eur(x['r']['asking']),
                          sgn(x['r']['yoy']), '{:,}'.format(x['r']['contracts']))))
                   for x in r['table'])
    size = (T['size_line'].replace('{s}', str(ex['size'])).replace('{d}', eur(r['bySizeDeals'])).replace('{k}', eur(r['bySizeAsking']))
            if r['bySizeDeals'] else T['size_line_new'].replace('{s}', str(ex['size'])).replace('{k}', eur(r['bySizeAsking'])))
    cities = ''.join(chip('city', k, T['cities'][k], k == ex['city']) for k in R['cities'])
    wa = 'https://wa.me/972525101555?text=' + re.sub(r'\s', '%20', T['wa_text'])
    parts = [
        '<section class="cyx-tool" data-cyx-tool="price-list" data-lang="%s" dir="rtl" data-rules="%s" data-text="%s" data-example="%s">'
        % (lang, escape(json.dumps(R, ensure_ascii=False)), escape(json.dumps(T, ensure_ascii=False)), escape(json.dumps(ex))),
        '<div class="cyx-tool__head"><h2 class="cyx-tool__title">%s</h2><p class="cyx-tool__lead">%s</p></div>' % (escape(T['title']), escape(T['lead'])),
        '<div class="cyx-panel">',
        '<div class="cyx-field cyx-field--wide"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div>' % (escape(T['f_city']), cities),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s</div></div>'
        % (escape(T['f_type']), chip('type', 'apartment', T['c_apartment'], ex['type'] == 'apartment'), chip('type', 'house', T['c_house'], ex['type'] == 'house')),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s</div></div>'
        % (escape(T['f_deal']), chip('deal', 'resale', T['c_resale'], ex['deal'] == 'resale'), chip('deal', 'new', T['c_new'], ex['deal'] == 'new')),
        '<div class="cyx-field"><label class="cyx-label" for="cyx-pl-size">%s</label><input id="cyx-pl-size" class="cyx-input" type="text" inputmode="numeric" autocomplete="off" value="%d"></div>'
        % (escape(T['f_size']), ex['size']),
        '</div>',
        '<div class="cyx-result" aria-live="polite"><div class="cyx-result__kicker">%s</div><bdi class="cyx-result__figure" data-out="median">%s</bdi>'
        '<p class="cyx-result__line" data-out="m2">%s</p><p class="cyx-result__line" data-out="ask">%s</p><p class="cyx-result__line" data-out="yoy">%s</p>'
        '<p class="cyx-result__line" data-out="size">%s</p></div>'
        % (escape(T['kicker']), eur(me['median']), escape(T['m2_line'].replace('{m}', eur(me['m2']))), escape(T['ask_line'].replace('{a}', eur(me['asking']))),
           escape(T['yoy_line'].replace('{y}', sgn(me['yoy']))), escape(size)),
        '<p class="cyx-example">%s</p>' % escape(T['gap_note']),
        '<div class="cyx-break-wrap"><table class="cyx-break cyx-break--wide"><thead><tr><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th></tr></thead><tbody>%s</tbody></table></div>'
        % (escape(T['th_city']), escape(T['th_median']), escape(T['th_m2']), escape(T['th_ask']), escape(T['th_yoy']), escape(T['th_contracts']), rows),
        '<div class="cyx-listwrap"><p class="cyx-list__note">%s</p></div>'
        % escape(T['contracts_note'].replace('{n}', '{:,}'.format(R['contracts_total_2026'])).replace('{c}', str(R['contracts_change_total']))),
        '<p class="cyx-source">%s</p>' % escape(T['source']),
        '<div class="cyx-next"><a class="cyx-cta" href="%s" target="_blank" rel="noopener">%s</a><span class="cyx-next__note">%s</span></div>'
        % (wa, escape(T['cta']), escape(T['cta_note'])),
        '</section>',
    ]
    return '\n'.join(parts)
