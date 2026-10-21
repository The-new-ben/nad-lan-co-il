# -*- coding: utf-8 -*-
"""Server-rendered section of the Israel-Cyprus tax map (sale example computed by the same engine.js; every card printed)."""
import json
import re
from html import escape

from bank_section import chip


def money(n):
    return '⁦€{:,}⁩'.format(int(n))


def yn(name, on, T):
    return chip(name, 'yes', T['c_yes'], on) + chip(name, 'no', T['c_no'], not on)


def taxmap_section(lang, R, T, run_engine, here):
    ex = dict(R['example'])
    r = run_engine(here / 'tax-map', ex, R, 'sale')
    events = ''.join(chip('event', k, v, k == 'sale') for k, v in T['events'].items())
    rows = [('cy', r['cyTax'], False), ('fee', r['fee'], False), ('il', r['ilNet'], False), ('total', r['total'], True)]
    body = ''.join('<tr class="cyx-row%s"><th scope="row">%s</th><td class="cyx-num"><bdi data-row="%s">%s</bdi></td><td class="cyx-rule">%s</td></tr>'
                   % (' cyx-row--total' if s else '', escape(T['rows'][k][0]), k, money(v), escape(T['rows'][k][1])) for k, v, s in rows)
    cards = ''
    for ev, pair in T['cards'].items():
        cards += ('<div class="cyx-cards" data-event="%s">' % ev) + ''.join(
            '<div class="cyx-card"><h3 class="cyx-list__title">%s</h3><p>%s</p></div>' % (escape(h), escape(p)) for h, p in pair) + '</div>'
    wa = 'https://wa.me/972525101555?text=' + re.sub(r'\s', '%20', T['wa_text'])

    def money_field(key, label):
        return ('<div class="cyx-field"><label class="cyx-label" for="cyx-tm-%s">%s</label><div class="cyx-money"><span>€</span>'
                '<input id="cyx-tm-%s" type="text" inputmode="numeric" autocomplete="off" value="%s"></div></div>' % (key, escape(label), key, '{:,}'.format(ex[key])))

    parts = [
        '<section class="cyx-tool" data-cyx-tool="tax-map" data-lang="%s" dir="rtl" data-rules="%s" data-text="%s" data-example="%s">'
        % (lang, escape(json.dumps(R, ensure_ascii=False)), escape(json.dumps(T, ensure_ascii=False)), escape(json.dumps(ex))),
        '<div class="cyx-tool__head"><h2 class="cyx-tool__title">%s</h2><p class="cyx-tool__lead">%s</p></div>' % (escape(T['title']), escape(T['lead'])),
        '<div class="cyx-panel"><div class="cyx-field cyx-field--wide"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div></div>'
        % (escape(T['q_event']), events),
        '<div data-event="sale">',
        '<div class="cyx-panel">%s%s%s' % (money_field('buy', T['f_buy']), money_field('sell', T['f_sell']), money_field('costs', T['f_costs'])),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div>' % (escape(T['q_main']), yn('main', ex['main'], T)),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div></div>' % (escape(T['q_used']), yn('used', ex['used'], T)),
        '<div class="cyx-result" aria-live="polite"><div class="cyx-result__kicker">%s</div><bdi class="cyx-result__figure" data-out="total">%s</bdi>'
        '<p class="cyx-result__line" data-out="net">%s</p><p class="cyx-result__line" data-out="gain">%s</p></div>'
        % (escape(T['kicker']), money(r['total']), escape(T['net_line'].replace('{n}', money(r['net']))),
           escape(T['gain_line'].replace('{g}', money(r['gain'])).replace('{e}', money(r['exemption'])))),
        '<div class="cyx-break-wrap"><table class="cyx-break"><thead><tr><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th></tr></thead><tbody>%s</tbody></table></div>'
        % (escape(T['th_item']), escape(T['th_amount']), escape(T['th_rule']), body),
        '</div>',
        '<div class="cyx-listwrap">%s</div>' % cards,
        '<p class="cyx-source">%s</p>' % escape(T['source']),
        '<div class="cyx-next"><a class="cyx-cta" href="%s" target="_blank" rel="noopener">%s</a><span class="cyx-next__note">%s</span></div>'
        % (wa, escape(T['cta']), escape(T['cta_note'])),
        '</section>',
    ]
    return '\n'.join(parts)
