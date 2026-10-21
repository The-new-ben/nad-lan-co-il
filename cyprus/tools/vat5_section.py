# -*- coding: utf-8 -*-
"""Server-rendered section of the 5% VAT eligibility checker (example computed by the same engine.js)."""
import json
import re
from html import escape

from bank_section import chip


def money(n):
    return '⁦€{:,}⁩'.format(int(n))


def vat5_section(lang, R, T, run_engine, here):
    ex = dict(R['example'])
    r = run_engine(here / 'vat5', ex, R, 'check')
    checks = []
    for c in r['checks']:
        cls = 'cyx-check--ok' if c['pass'] else ('cyx-check--warn' if c['soft'] else 'cyx-check--no')
        why = '' if (c['pass'] and not c['soft']) else '<span class="cyx-check__why">%s</span>' % escape(T['checks'][c['key']][1])
        checks.append('<li class="cyx-check %s"><span class="cyx-check__label">%s</span>%s</li>' % (cls, escape(T['checks'][c['key']][0]), why))
    wa = 'https://wa.me/972525101555?text=' + re.sub(r'\s', '%20', T['wa_text'])
    parts = [
        '<section class="cyx-tool" data-cyx-tool="vat5" data-lang="%s" dir="rtl" data-rules="%s" data-text="%s" data-example="%s">'
        % (lang, escape(json.dumps(R, ensure_ascii=False)), escape(json.dumps(T, ensure_ascii=False)), escape(json.dumps(ex))),
        '<div class="cyx-tool__head"><h2 class="cyx-tool__title">%s</h2><p class="cyx-tool__lead">%s</p></div>' % (escape(T['title']), escape(T['lead'])),
        '<div class="cyx-panel">',
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s</div></div>'
        % (escape(T['q_buyer']), chip('buyer', 'person', T['c_person'], True), chip('buyer', 'company', T['c_company'], False)),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s</div></div>'
        % (escape(T['q_home']), chip('home', 'main', T['c_main'], True), chip('home', 'holiday', T['c_holiday'], False)),
        '<div class="cyx-field"><label class="cyx-label" for="cyx-v5-price">%s</label><div class="cyx-money"><span>€</span><input id="cyx-v5-price" type="text" inputmode="numeric" autocomplete="off" value="%s"></div></div>'
        % (escape(T['f_price']), '{:,}'.format(ex['price'])),
        '<div class="cyx-field"><label class="cyx-label" for="cyx-v5-area">%s</label><input id="cyx-v5-area" class="cyx-input" type="text" inputmode="numeric" autocomplete="off" value="%d"></div>'
        % (escape(T['f_area']), ex['area']),
        '<div class="cyx-field cyx-field--wide"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s%s%s</div></div>'
        % (escape(T['q_family']), chip('family', 'none', T['c_none'], True), chip('family', 'disability', T['c_disability'], False),
           chip('family', 'kids4', T['c_kids4'], False), chip('family', 'kids5', T['c_kids5'], False)),
        '<div class="cyx-field cyx-field--wide"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s%s</div></div>'
        % (escape(T['q_timing']), chip('timing', 'before', T['c_before'], True), chip('timing', 'late', T['c_late'], False), chip('timing', 'over', T['c_over'], False)),
        '</div>',
        '<div class="cyx-result" aria-live="polite"><p class="cyx-result__figure cyx-result__figure--text" data-out="answer">%s</p>'
        '<p class="cyx-result__line" data-out="saving"%s>%s</p><p class="cyx-result__line" data-out="vat">%s</p>'
        '<p class="cyx-result__line" data-out="late" hidden>%s</p></div>'
        % (escape(T['yes'] if r['eligible'] else T['no']), '' if r['eligible'] else ' hidden',
           escape(T['saving'].replace('{s}', money(r['saving']))) if r['eligible'] else '',
           escape(T['vat_line'].replace('{v}', money(r['vat']))), escape(T['late_note'])),
        '<div class="cyx-listwrap"><ul class="cyx-checks" data-out="checks">%s</ul><p class="cyx-list__note" data-out="how">%s</p></div>'
        % (''.join(checks), escape(T['how'].replace('{m}', str(r['firstM2'])))),
        '<p class="cyx-source">%s</p>' % escape(T['source']),
        '<div class="cyx-next"><a class="cyx-cta" href="%s" target="_blank" rel="noopener">%s</a><span class="cyx-next__note">%s</span></div>'
        % (wa, escape(T['cta']), escape(T['cta_note'])),
        '</section>',
    ]
    return '\n'.join(parts)
