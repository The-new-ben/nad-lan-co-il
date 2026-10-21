# -*- coding: utf-8 -*-
"""Server-rendered section of the off-plan payment schedule (example computed by the same engine.js)."""
import json
import re
from html import escape

from bank_section import chip


def eur(n):
    return '⁦€{:,}⁩'.format(int(n))


def ils(n):
    return '⁦₪{:,}⁩'.format(int(n))


def offplan_section(lang, R, T, run_engine, here):
    ex = dict(R['example'])
    r = run_engine(here / 'offplan', ex, R, 'schedule')
    body = ''
    for x in r['rows']:
        if not x['pct']:
            continue
        mark = x['stage'] == r['releaseAt']
        body += '<tr class="cyx-row%s"><th scope="row">%s</th>%s</tr>' % (
            ' cyx-row--total' if mark else '', escape(T['stages'][x['stage']]),
            ''.join('<td class="cyx-num"><bdi>%s</bdi></td>' % v for v in ('%d%%' % x['pct'], eur(x['eur']), ils(x['ils']), ils(x['ilsShock']))))
        if mark:
            body += '<tr class="cyx-row cyx-row--note"><td class="cyx-rule" colspan="5">%s</td></tr>' % escape(T['release'])
    pct_fields = ''.join(
        '<div class="cyx-field"><label class="cyx-label" for="cyx-op-p%d">%s (%%)</label><input id="cyx-op-p%d" class="cyx-input" data-pct="%d" type="text" inputmode="numeric" autocomplete="off" value="%d"></div>'
        % (i, escape(T['stages'][i]), i, i, p) for i, p in enumerate(ex['pcts']))
    plans = ''.join(chip('plan', k, T['plans'][k], k == ex['plan']) for k in R['plans'])
    rules = ''.join('<li class="cyx-list__item">%s</li>' % escape(x) for x in T['rules'])
    wa = 'https://wa.me/972525101555?text=' + re.sub(r'\s', '%20', T['wa_text'])
    parts = [
        '<section class="cyx-tool" data-cyx-tool="offplan" data-lang="%s" dir="rtl" data-rules="%s" data-text="%s" data-example="%s">'
        % (lang, escape(json.dumps(R, ensure_ascii=False)), escape(json.dumps(T, ensure_ascii=False)), escape(json.dumps(ex))),
        '<div class="cyx-tool__head"><h2 class="cyx-tool__title">%s</h2><p class="cyx-tool__lead">%s</p></div>' % (escape(T['title']), escape(T['lead'])),
        '<div class="cyx-panel">',
        '<div class="cyx-field"><label class="cyx-label" for="cyx-op-price">%s</label><div class="cyx-money"><span>€</span><input id="cyx-op-price" type="text" inputmode="numeric" autocomplete="off" value="%s"></div></div>'
        % (escape(T['f_price']), '{:,}'.format(ex['price'])),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s</div></div>'
        % (escape(T['q_vat']), chip('vat', 'standard', T['c_standard'], ex['vat'] == 'standard'), chip('vat', 'reduced', T['c_reduced'], ex['vat'] == 'reduced')),
        '<div class="cyx-field cyx-field--wide"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div><span class="cyx-list__note">%s</span></div>'
        % (escape(T['q_plan']), plans, escape(T['plan_note'])),
        pct_fields,
        '</div>',
        '<div class="cyx-result" aria-live="polite"><div class="cyx-result__kicker">%s</div><bdi class="cyx-result__figure" data-out="total">%s</bdi>'
        '<p class="cyx-result__line" data-out="ils">%s</p><p class="cyx-result__line" data-out="shock">%s</p></div>'
        % (escape(T['kicker']), eur(r['total']), escape(T['ils_line'].replace('{s}', ils(r['ils'])).replace('{d}', R['fx']['date'])),
           escape(T['shock_line'].replace('{s}', ils(r['ilsShock'])).replace('{x}', ils(r['ilsShock'] - r['ils'])))),
        '<p class="cyx-example" data-out="sum" hidden></p>',
        '<div class="cyx-break-wrap"><table class="cyx-break cyx-break--wide"><thead><tr><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th></tr></thead><tbody>%s</tbody></table></div>'
        % (escape(T['th_stage']), escape(T['th_pct']), escape(T['th_eur']), escape(T['th_ils']), escape(T['th_shock']), body),
        '<div class="cyx-listwrap"><h3 class="cyx-list__title">%s</h3><ul class="cyx-list">%s</ul></div>' % (escape(T['rules_title']), rules),
        '<p class="cyx-source">%s</p>' % escape(T['source']),
        '<div class="cyx-next"><a class="cyx-cta" href="%s" target="_blank" rel="noopener">%s</a><span class="cyx-next__note">%s</span></div>'
        % (wa, escape(T['cta']), escape(T['cta_note'])),
        '</section>',
    ]
    return '\n'.join(parts)
