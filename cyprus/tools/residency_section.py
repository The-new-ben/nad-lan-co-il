# -*- coding: utf-8 -*-
"""Server-rendered section of the residency-by-investment checker (example computed by the same engine.js)."""
import json
import re
from html import escape

from bank_section import chip


def money(n):
    return '⁦€{:,}⁩'.format(int(n))


def yn(name, on, T):
    return chip(name, 'yes', T['c_yes'], on) + chip(name, 'no', T['c_no'], not on)


def residency_section(lang, R, T, run_engine, here):
    ex = dict(R['example'])
    r = run_engine(here / 'residency', ex, R, 'check')
    checks = []
    for c in r['checks']:
        why = ''
        if not c['pass']:
            gap = r['amountGap'] if c['key'] == 'amount' else r['incomeGap']
            why = '<span class="cyx-check__why">%s</span>' % escape(T['checks'][c['key']][1].replace('{g}', money(gap)))
        checks.append('<li class="cyx-check %s"><span class="cyx-check__label">%s</span>%s</li>'
                      % ('cyx-check--ok' if c['pass'] else 'cyx-check--no', escape(T['checks'][c['key']][0]), why))
    routes = ''.join(chip('route', k, v, k == ex['route']) for k, v in T['routes'].items())
    minors = ''.join(chip('minors', str(n), str(n), n == ex['minors']) for n in range(0, 5))
    adults = ''.join(chip('adults', str(n), str(n), n == ex['adults']) for n in range(0, 3))
    also = ''.join('<li class="cyx-list__item">%s</li>' % escape(x) for x in T['also'])
    wa = 'https://wa.me/972525101555?text=' + re.sub(r'\s', '%20', T['wa_text'])
    parts = [
        '<section class="cyx-tool" data-cyx-tool="residency" data-lang="%s" dir="rtl" data-rules="%s" data-text="%s" data-example="%s">'
        % (lang, escape(json.dumps(R, ensure_ascii=False)), escape(json.dumps(T, ensure_ascii=False)), escape(json.dumps(ex))),
        '<div class="cyx-tool__head"><h2 class="cyx-tool__title">%s</h2><p class="cyx-tool__lead">%s</p></div>' % (escape(T['title']), escape(T['lead'])),
        '<div class="cyx-panel">',
        '<div class="cyx-field cyx-field--wide"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div>' % (escape(T['q_route']), routes),
        '<div class="cyx-field"><label class="cyx-label" for="cyx-rs-amount">%s</label><div class="cyx-money"><span>€</span><input id="cyx-rs-amount" type="text" inputmode="numeric" autocomplete="off" value="%s"></div></div>'
        % (escape(T['f_amount']), '{:,}'.format(ex['amount'])),
        '<div class="cyx-field" data-field="first"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div>' % (escape(T['q_first']), yn('firstSale', ex['firstSale'], T)),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div>' % (escape(T['q_spouse']), yn('spouse', ex['spouse'], T)),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div>' % (escape(T['q_minors']), minors),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div>' % (escape(T['q_adults']), adults),
        '<div class="cyx-field"><label class="cyx-label" for="cyx-rs-income">%s</label><div class="cyx-money"><span>€</span><input id="cyx-rs-income" type="text" inputmode="numeric" autocomplete="off" value="%s"></div></div>'
        % (escape(T['f_income']), '{:,}'.format(ex['income'])),
        '<div class="cyx-field" data-field="abroad"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div>' % (escape(T['q_abroad']), yn('abroad', ex['abroad'], T)),
        '</div>',
        '<div class="cyx-result" aria-live="polite"><p class="cyx-result__figure cyx-result__figure--text" data-out="answer">%s</p>'
        '<p class="cyx-result__line" data-out="need">%s</p><p class="cyx-result__line" data-out="income">%s</p><p class="cyx-result__line" data-out="fees">%s</p></div>'
        % (escape(T['ok'] if r['ok'] else T['no']),
           escape(T['need_line'].replace('{n}', money(r['need'])).replace('{v}', T['vat_suffix'] if r['vatOnTop'] else '')),
           escape(T['income_line'].replace('{i}', money(r['incomeNeed']))),
           escape(T['fees_line'].replace('{f}', money(r['fees'])).replace('{p}', str(r['people'])))),
        '<div class="cyx-listwrap"><ul class="cyx-checks" data-out="checks">%s</ul>' % ''.join(checks),
        '<h3 class="cyx-list__title">%s</h3><ul class="cyx-list">%s</ul><p class="cyx-list__note">%s</p></div>' % (escape(T['also_title']), also, escape(T['pending'])),
        '<p class="cyx-source">%s</p>' % escape(T['source']),
        '<div class="cyx-next"><a class="cyx-cta" href="%s" target="_blank" rel="noopener">%s</a><span class="cyx-next__note">%s</span></div>'
        % (wa, escape(T['cta']), escape(T['cta_note'])),
        '</section>',
    ]
    return '\n'.join(parts)
