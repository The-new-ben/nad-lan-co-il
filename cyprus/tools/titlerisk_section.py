# -*- coding: utf-8 -*-
"""Server-rendered section of the title-deeds risk check (example computed by the same engine.js)."""
import json
import re
from html import escape

from bank_section import chip


def titlerisk_section(lang, R, T, run_engine, here):
    ex = dict(R['example'])
    r = run_engine(here / 'title-risk', ex, R, 'assess')
    fields = []
    for qd in R['questions']:
        label, answers = T['questions'][qd['id']]
        chips = ''.join(chip(qd['id'], k, answers[k], ex[qd['id']] == k) for k in qd['answers'])
        fields.append('<div class="cyx-field cyx-field--wide"><span class="cyx-label">%s</span><div class="cyx-chips" role="radiogroup">%s</div></div>' % (escape(label), chips))
    if r['flags']:
        flags = ''.join('<li class="cyx-check %s"><span class="cyx-check__why">%s</span></li>'
                        % ('cyx-check--no' if f['level'] == 'high' else 'cyx-check--warn', escape(T['flags'][f['id']])) for f in r['flags'])
    else:
        flags = '<li class="cyx-check cyx-check--ok">%s</li>' % escape(T['none'])
    lst = ''.join('<li>%s</li>' % escape(x) for x in r['lawyerList'])
    wa = 'https://wa.me/972525101555?text=' + re.sub(r'\s', '%20', T['wa_text'])
    parts = [
        '<section class="cyx-tool" data-cyx-tool="title-risk" data-lang="%s" dir="rtl" data-rules="%s" data-text="%s" data-example="%s">'
        % (lang, escape(json.dumps(R, ensure_ascii=False)), escape(json.dumps(T, ensure_ascii=False)), escape(json.dumps(ex))),
        '<div class="cyx-tool__head"><h2 class="cyx-tool__title">%s</h2><p class="cyx-tool__lead">%s</p></div>' % (escape(T['title']), escape(T['lead'])),
        '<div class="cyx-panel">%s</div>' % ''.join(fields),
        '<div class="cyx-result" aria-live="polite" data-level="%s"><div class="cyx-result__kicker">%s</div><p class="cyx-result__figure cyx-result__figure--text" data-out="level">%s</p></div>'
        % (r['level'], escape(T['kicker']), escape(T['levels'][r['level']])),
        '<div class="cyx-listwrap"><h3 class="cyx-list__title">%s</h3><ul class="cyx-checks" data-out="flags">%s</ul>' % (escape(T['h_flags']), flags),
        '<h3 class="cyx-list__title">%s</h3><p class="cyx-list__note">%s</p><ol class="cyx-lawyer" dir="ltr" lang="en" data-out="list">%s</ol></div>'
        % (escape(T['h_list']), escape(T['list_note']), lst),
        '<div class="cyx-next"><button type="button" class="cyx-chip" data-copy>%s</button><span class="cyx-next__note" data-out="copied" hidden>%s</span></div>'
        % (escape(T['copy']), escape(T['copied'])),
        '<p class="cyx-source">%s</p>' % escape(T['source']),
        '<div class="cyx-next"><a class="cyx-cta" href="%s" target="_blank" rel="noopener">%s</a><span class="cyx-next__note">%s</span></div>'
        % (wa, escape(T['cta']), escape(T['cta_note'])),
        '</section>',
    ]
    return '\n'.join(parts)
