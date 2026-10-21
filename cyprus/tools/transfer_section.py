# -*- coding: utf-8 -*-
"""Server-rendered section of the Israel-to-Cyprus transfer cost comparison (example computed by the same engine.js)."""
import json
import re
from html import escape

from bank_section import chip


def ils(n):
    return '⁦₪{:,}⁩'.format(int(n))


def pct(x):
    return '%.2f%%' % (round(x * 10000) / 100)


def transfer_section(lang, R, T, run_engine, here):
    ex = dict(R['example'])
    r = run_engine(here / 'transfer', ex, R, 'compare')
    rows = ''.join('<tr class="cyx-row%s"><th scope="row">%s</th>%s</tr>'
                   % (' cyx-row--total' if i == 0 else '', escape(x['name']),
                      ''.join('<td class="cyx-num"><bdi>%s</bdi></td>' % ils(x[k]) for k in ('total', 'transfer', 'conversion', 'incoming')))
                   for i, x in enumerate(r['rows']))
    cy = ''.join(chip('cy', c['id'], c['name'], c['id'] == ex['cy']) for c in R['cyprus'])
    notes = ''.join('<p class="cyx-list__note">%s</p>' % escape(n) for n in T['notes'])
    best = r['cheapest']
    wa = 'https://wa.me/972525101555?text=' + re.sub(r'\s', '%20', T['wa_text'])
    parts = [
        '<section class="cyx-tool" data-cyx-tool="transfer" data-lang="%s" dir="rtl" data-rules="%s" data-text="%s" data-example="%s">'
        % (lang, escape(json.dumps(R, ensure_ascii=False)), escape(json.dumps(T, ensure_ascii=False)), escape(json.dumps(ex))),
        '<div class="cyx-tool__head"><h2 class="cyx-tool__title">%s</h2><p class="cyx-tool__lead">%s</p></div>' % (escape(T['title']), escape(T['lead'])),
        '<div class="cyx-panel">',
        '<div class="cyx-field"><label class="cyx-label" for="cyx-tr-eur">%s</label><div class="cyx-money"><span>€</span><input id="cyx-tr-eur" type="text" inputmode="numeric" autocomplete="off" value="%s"></div></div>'
        % (escape(T['f_eur']), '{:,}'.format(ex['eur'])),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s</div></div>'
        % (escape(T['q_channel']), chip('channel', 'internet', T['c_internet'], ex['channel'] == 'internet'), chip('channel', 'branch', T['c_branch'], ex['channel'] == 'branch')),
        '<div class="cyx-field cyx-field--wide"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div>' % (escape(T['q_cy']), cy),
        '</div>',
        '<div class="cyx-result" aria-live="polite"><div class="cyx-result__kicker">%s</div><p class="cyx-result__figure cyx-result__figure--text" data-out="best">%s</p>'
        '<p class="cyx-result__line" data-out="cheap">%s</p><p class="cyx-result__line" data-out="spread">%s</p><p class="cyx-result__line" data-out="base">%s</p></div>'
        % (escape(T['kicker']), escape(best['name']),
           escape(T['cheap_line'].replace('{b}', best['name']).replace('{t}', ils(best['total'])).replace('{p}', pct(best['pct']))),
           escape(T['spread_line'].replace('{d}', ils(r['dearest']['total'] - best['total']))),
           escape(T['base_line'].replace('{s}', ils(r['ils'])))),
        '<div class="cyx-break-wrap"><table class="cyx-break cyx-break--wide"><thead><tr><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th></tr></thead><tbody>%s</tbody></table></div>'
        % (escape(T['th_bank']), escape(T['th_total']), escape(T['th_transfer']), escape(T['th_conversion']), escape(T['th_incoming']), rows),
        '<div class="cyx-listwrap">%s</div>' % notes,
        '<p class="cyx-source">%s</p>' % escape(T['source']),
        '<div class="cyx-next"><a class="cyx-cta" href="%s" target="_blank" rel="noopener">%s</a><span class="cyx-next__note">%s</span></div>'
        % (wa, escape(T['cta']), escape(T['cta_note'])),
        '</section>',
    ]
    return '\n'.join(parts)
