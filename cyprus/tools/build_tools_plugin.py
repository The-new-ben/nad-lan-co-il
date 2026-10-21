# -*- coding: utf-8 -*-
"""Packages the cy-prus-tools WordPress plugin: server-rendered tool sections, FAQ blocks, JSON-LD, assets and
self-hosted fonts, zipped with forward slashes (WordPress mis-extracts backslash paths).

  python build_tools_plugin.py --out <dir> [--ship]

--ship refuses to build while any tool's rules.json is not verified."""
import argparse
import json
import re
import shutil
import zipfile
from html import escape
from pathlib import Path

import build_tool

HERE = Path(__file__).resolve().parent
SITE = 'https://cy-prus.co.il'
REGISTRY = [
    {'id': 'purchase-cost', 'page_id': 114, 'path': '/guides/purchase-tax-cyprus-2026/', 'lang': 'he', 'after_paragraph': 2,
     'engines': ['purchase-cost']},
    {'id': 'net-yield', 'page_id': 53, 'path': '/guides/real-estate-investments-in-cyprus/', 'lang': 'he', 'after_paragraph': 3,
     'engines': ['purchase-cost', 'net-yield']},
    {'id': 'bank-docs', 'page_id': 51, 'path': '/guides/cyprus-bank-account-for-israelis/', 'lang': 'he', 'after_paragraph': 2,
     'engines': ['bank-docs']},
    {'id': 'vat5', 'page_id': 54, 'path': '/guides/vat-5-percent-first-home-cyprus/', 'lang': 'he', 'after_paragraph': 2,
     'engines': ['vat5']},
    {'id': 'residency', 'page_id': 52, 'path': '/guides/relocation-cyprus-israelis/', 'lang': 'he', 'after_paragraph': 2,
     'engines': ['residency']},
]


def version():
    m = re.search(r"define\( 'CYPT_VERSION', '([^']+)' \)", (HERE / 'plugin' / 'cy-prus-tools.php').read_text(encoding='utf-8'))
    head = re.search(r'\* Version: (\S+)', (HERE / 'plugin' / 'cy-prus-tools.php').read_text(encoding='utf-8'))
    assert m and head and m.group(1) == head.group(1), 'header Version and CYPT_VERSION differ'
    return m.group(1)


def faq_html(T):
    items = ''.join('<details class="cyx-faq__item"><summary>%s</summary><p>%s</p></details>' % (escape(f['q']), escape(f['a']))
                    for f in T['faq'])
    return ('<section class="cyx-faq" dir="rtl" aria-labelledby="cyx-faq-%s"><h2 id="cyx-faq-%s">%s</h2>%s</section>'
            % (T['slug'], T['slug'], escape(T['faq_title']), items))


def ld_json(T, url):
    graph = [
        {'@type': 'WebApplication', '@id': url + '#cyx-' + T['slug'], 'name': T['title'], 'url': url,
         'description': T['lead'], 'applicationCategory': 'FinanceApplication', 'operatingSystem': 'Any',
         'inLanguage': 'he', 'isAccessibleForFree': True,
         'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'EUR'}},
    ]
    if T.get('faq'):
        graph.append({'@type': 'FAQPage', '@id': url + '#cyx-faq-' + T['slug'],
                      'mainEntity': [{'@type': 'Question', 'name': f['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in T['faq']]})
    out = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
    assert '</' not in out
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--ship', action='store_true')
    a = ap.parse_args()
    ver = version()
    stage = Path(a.out) / ('stage-' + ver) / 'cy-prus-tools'
    if stage.exists():
        shutil.rmtree(stage)
    (stage / 'assets').mkdir(parents=True)
    (stage / 'fonts').mkdir()
    shutil.copy(HERE / 'plugin' / 'cy-prus-tools.php', stage / 'cy-prus-tools.php')
    for f in (HERE / 'fonts').glob('*.woff2'):
        shutil.copy(f, stage / 'fonts' / f.name)
    shutil.copy(HERE / 'fonts' / 'fonts.css', stage / 'assets' / 'fonts.css')
    styles = []
    for t in REGISTRY:
        tdir = HERE / t['id']
        rules = json.loads((tdir / 'rules.json').read_text(encoding='utf-8'))
        if a.ship and not rules.get('verified'):
            raise SystemExit(t['id'] + ': rules.json is not verified, refusing --ship')
        T = json.loads((tdir / ('text.%s.json' % t['lang'])).read_text(encoding='utf-8'))
        T.setdefault('slug', t['id'])
        out = stage / 'tools' / t['id']
        out.mkdir(parents=True)
        (out / ('section.%s.html' % t['lang'])).write_text(build_tool.section_for(t['id'], t['lang'], rules, T), encoding='utf-8')
        if T.get('faq'):
            (out / ('faq.%s.html' % t['lang'])).write_text(faq_html(T), encoding='utf-8')
        (out / ('ld.%s.json' % t['lang'])).write_text(ld_json(T, SITE + t['path']), encoding='utf-8')
        for eng in t['engines']:
            shutil.copy(HERE / eng / 'engine.js', stage / 'assets' / ('engine-%s.js' % eng))
        shutil.copy(tdir / 'ui.js', stage / 'assets' / ('ui-%s.js' % t['id']))
    styles.append((HERE / 'common.css').read_text(encoding='utf-8'))
    styles.append((HERE / 'faq.css').read_text(encoding='utf-8'))
    (stage / 'assets' / 'style.css').write_text('\n'.join(styles), encoding='utf-8')
    (stage / 'registry.json').write_text(json.dumps([{k: v for k, v in t.items() if k != 'path'} for t in REGISTRY], ensure_ascii=False, indent=1), encoding='utf-8')
    z = Path(a.out) / ('cy-prus-tools-%s%s.zip' % (ver, '' if a.ship else '-DRAFT'))
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(stage.rglob('*')):
            if f.is_file():
                zf.write(f, 'cy-prus-tools/' + f.relative_to(stage).as_posix())
    print('built', z, z.stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
