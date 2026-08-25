#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""URL word-duplication audit for nad-lan.co.il (owner law 25.8.2026).

The owner's rule: Google is sensitive to the same word appearing twice in a
URL, and same-word URLs across the site invite cannibalization. This tool is
the standing "way to know":

  1. INTERNAL duplication - the same token twice inside ONE URL path
     (e.g. /mortgage-calculator/reverse-mortgage/ repeats "mortgage";
      /investment/apartments-for-investment/ repeats "investment").
     These almost always mark parent/child pages competing on one intent.
  2. CROSS-URL token pressure - how many distinct URLs share a money token
     (mortgage, investment, tel-aviv...). High counts = one word with many
     owners; every NEW URL must pick a token that is not already owned.

Default source: the LIVE sitemap index (post-purge truth). --csv <file> runs on
an inventory CSV with a `url` column instead. Read-only, no site changes.

Usage:
  python url_word_audit.py                 # live sitemaps, digest to stdout
  python url_word_audit.py --out audit.csv # full internal-duplication CSV
  python url_word_audit.py --token mortgage  # list every URL holding a token
"""
import argparse, csv, re, sys, urllib.parse, urllib.request
from collections import Counter, defaultdict

BASE = 'https://nad-lan.co.il'
STOP = {'', 'https', 'http', 'www', 'nad-lan', 'co', 'il', 'page', 'the', 'of', 'and',
        'a', 'b', 'c', 'en', 'fr', 'ru', 'ar', 'he'}
SECTIONS = {'projects', 'properties', 'professionals', 'city', 'cities', 'glossary',
            'global', 'tour', 'guides', 'sde-dov', 'investment'}


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'nadlan-url-audit'})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode('utf-8', 'replace')


def live_urls():
    idx = fetch(BASE + '/sitemap_index.xml')
    urls = []
    for sm in re.findall(r'<loc>([^<]+)</loc>', idx):
        try:
            urls += re.findall(r'<loc>([^<]+)</loc>', fetch(sm))
        except Exception as e:
            print('WARN could not fetch %s: %s' % (sm, e), file=sys.stderr)
    return urls


def tokens_of(url):
    path = urllib.parse.unquote(urllib.parse.urlsplit(url).path).lower()
    toks = [t for t in re.split(r'[/\-_.+ ]+', path) if t and t not in STOP and not t.isdigit()]
    return toks


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--csv', help='inventory CSV with a url column instead of live sitemaps')
    p.add_argument('--out', help='write full internal-duplication rows to CSV')
    p.add_argument('--token', help='list every URL containing this token')
    p.add_argument('--min-cross', type=int, default=8, help='min URL count to report a cross-URL token')
    a = p.parse_args()

    if a.csv:
        with open(a.csv, encoding='utf-8-sig') as f:
            urls = [row['url'] for row in csv.DictReader(f) if row.get('url')]
    else:
        urls = live_urls()
    print('urls analyzed: %d' % len(urls))

    internal = []           # (url, [dup tokens])
    cross = Counter()       # token -> distinct url count
    owners = defaultdict(list)
    for u in urls:
        toks = tokens_of(u)
        c = Counter(toks)
        dups = [t for t, n in c.items() if n > 1]
        if dups:
            internal.append((u, dups))
        for t in set(toks):
            cross[t] += 1
            if len(owners[t]) < 400:
                owners[t].append(u)

    if a.token:
        print('\n=== URLs holding token "%s" (%d) ===' % (a.token, cross.get(a.token, 0)))
        for u in owners.get(a.token, []):
            print('  ' + urllib.parse.unquote(u).replace(BASE, ''))
        return

    print('\n=== 1. INTERNAL duplication (same word twice in one URL) - %d URLs ===' % len(internal))
    for u, dups in sorted(internal, key=lambda x: -len(x[1])):
        print('  %s   <- repeats: %s' % (urllib.parse.unquote(u).replace(BASE, ''), ', '.join(dups)))

    print('\n=== 2. CROSS-URL token pressure (>= %d URLs share the token) ===' % a.min_cross)
    for t, n in cross.most_common():
        if n < a.min_cross: break
        if t in SECTIONS: continue
        print('  %-28s %4d URLs' % (t, n))

    if a.out:
        with open(a.out, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['url', 'duplicated_tokens'])
            for u, dups in internal:
                w.writerow([u, '|'.join(dups)])
        print('\nwrote %s' % a.out)


if __name__ == '__main__':
    main()
