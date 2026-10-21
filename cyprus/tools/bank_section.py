# -*- coding: utf-8 -*-
"""Server-rendered section of the bank-documents wizard (the example answers, computed by the same engine.js)."""
import json
import re
from html import escape


def chip(name, value, label, on):
    return ('<button type="button" class="cyx-chip" role="radio" data-chip="%s" data-value="%s" aria-checked="%s">%s</button>'
            % (name, value, 'true' if on else 'false', escape(label)))


def output_html(r, T):
    h = []
    for g in r['groups']:
        h.append('<h3 class="cyx-list__title">%s</h3><ul class="cyx-list">' % escape(T['groups'][g['key']]))
        for it in g['items']:
            who = '<span class="cyx-list__who">%s</span>' % escape(it['who']) if it['who'] else ''
            h.append('<li class="cyx-list__item">%s%s</li>' % (escape(it['text']), who))
        h.append('</ul>')
    h.append('<h3 class="cyx-list__title">%s</h3><ul class="cyx-list">' % escape(T['h_channels']))
    for c in r['channels']:
        h.append('<li class="cyx-list__item"><strong>%s: </strong>%s</li>' % (escape(c['bank']), escape(c['text'])))
    h.append('</ul><h3 class="cyx-list__title">%s</h3>' % escape(T['h_fees']))
    rows = ''.join('<tr class="cyx-row"><th scope="row">%s</th><td class="cyx-rule">%s</td><td class="cyx-rule">%s</td><td class="cyx-num">%s</td></tr>'
                   % (escape(f['bank']), escape(f['open']), escape(f['keep']), escape(f['table'])) for f in r['fees'])
    h.append('<div class="cyx-break-wrap"><table class="cyx-break"><thead><tr><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th></tr></thead><tbody>%s</tbody></table></div>'
             % (escape(T['th_bank']), escape(T['th_open']), escape(T['th_keep']), escape(T['th_table']), rows))
    if r['basic']:
        h.append('<h3 class="cyx-list__title">%s</h3><p class="cyx-list__note">%s</p>' % (escape(T['h_basic']), escape(r['basic'])))
    for n in r['always']:
        h.append('<p class="cyx-list__note">%s</p>' % escape(n))
    return ''.join(h)


def bank_docs_section(lang, R, T, run_engine, here):
    ex = {'lives': 'israel', 'passport': 'il', 'purpose': 'property', 'funds': 'salary', 'hebrew': True}
    r = run_engine(here / 'bank-docs', ex, R, 'checklist')
    wa = 'https://wa.me/972525101555?text=' + re.sub(r'\s', '%20', T['wa_text'])
    purpose = ''.join(chip('purpose', k, v['label'], k == ex['purpose']) for k, v in R['purpose'].items())
    funds = ''.join(chip('funds', k, v['label'], k == ex['funds']) for k, v in R['source_of_funds'].items())
    parts = [
        '<section class="cyx-tool" data-cyx-tool="bank-docs" data-lang="%s" dir="rtl" data-rules="%s" data-text="%s" data-example="%s">'
        % (lang, escape(json.dumps(R, ensure_ascii=False)), escape(json.dumps(T, ensure_ascii=False)), escape(json.dumps(ex))),
        '<div class="cyx-tool__head"><h2 class="cyx-tool__title">%s</h2><p class="cyx-tool__lead">%s</p></div>' % (escape(T['title']), escape(T['lead'])),
        '<div class="cyx-panel">',
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s</div></div>'
        % (escape(T['q_lives']), chip('lives', 'israel', T['c_lives_israel'], True), chip('lives', 'cyprus', T['c_lives_cyprus'], False)),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s%s</div></div>'
        % (escape(T['q_passport']), chip('passport', 'il', T['c_passport_il'], True), chip('passport', 'eu', T['c_passport_eu'], False),
           chip('passport', 'us', T['c_passport_us'], False)),
        '<div class="cyx-field cyx-field--wide"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div>' % (escape(T['q_purpose']), purpose),
        '<div class="cyx-field cyx-field--wide"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div>' % (escape(T['q_funds']), funds),
        '<div class="cyx-field"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s%s</div></div>'
        % (escape(T['q_hebrew']), chip('hebrew', 'yes', T['c_hebrew_yes'], True), chip('hebrew', 'no', T['c_hebrew_no'], False)),
        '</div>',
        '<div class="cyx-result" aria-live="polite"><div class="cyx-result__kicker">%s</div><p class="cyx-result__figure cyx-result__figure--text" data-out="count">%s</p></div>'
        % (escape(T['kicker']), escape(T['count'].replace('{n}', str(r['count'])))),
        '<div class="cyx-listwrap" data-out="list">%s</div>' % output_html(r, T),
        '<div class="cyx-next"><button type="button" class="cyx-chip" data-copy>%s</button><span class="cyx-next__note" data-out="copied" hidden>%s</span></div>'
        % (escape(T['copy']), escape(T['copied'])),
        '<p class="cyx-source">%s</p>' % escape(T['source']),
        '<div class="cyx-next"><a class="cyx-cta" href="%s" target="_blank" rel="noopener">%s</a><span class="cyx-next__note">%s</span></div>'
        % (wa, escape(T['cta']), escape(T['cta_note'])),
        '</section>',
    ]
    return '\n'.join(parts)
