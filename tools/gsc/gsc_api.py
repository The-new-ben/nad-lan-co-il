#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zero-dependency Google Search Console API client for nad-lan.co.il sessions.

Secrets: OAuth client + refresh token live OUTSIDE the repo at
  %USERPROFILE%\\Documents\\jus-tice-secrets\\gsc\\gsc-oauth-client.json
  %USERPROFILE%\\Documents\\jus-tice-secrets\\gsc\\gsc-token.json
(override with GSC_OAUTH_CLIENT_PATH / GSC_TOKEN_PATH). NEVER print, copy,
commit or ZIP those files. This script only ever prints API data.

Usage:
  python gsc_api.py sites
  python gsc_api.py sitemaps [--site sc-domain:nad-lan.co.il]
  python gsc_api.py query --start 2026-08-01 --end 2026-08-24 \
      [--dimensions query,page] [--limit 25000] [--out rows.csv] [--filter-page contains:/projects/]
  python gsc_api.py totals --days 7        # quick clicks/impressions summary

Scope note (2026-08-25): the stored token is webmasters.READONLY. Reading
(query/sites/sitemaps-list) works; sitemap SUBMIT needs the full webmasters
scope = a one-time interactive re-consent by the owner.
"""
import argparse, csv, datetime as dt, json, os, sys, urllib.parse, urllib.request

_SECRETS = os.path.join(os.path.expanduser('~'), 'Documents', 'jus-tice-secrets', 'gsc')
CLIENT = os.environ.get('GSC_OAUTH_CLIENT_PATH', os.path.join(_SECRETS, 'gsc-oauth-client.json'))
_FULL = os.path.join(_SECRETS, 'gsc-token-full.json')   # full webmasters scope (owner consent 25.8.2026)
TOKEN = os.environ.get('GSC_TOKEN_PATH',
    _FULL if os.path.exists(_FULL) else os.path.join(_SECRETS, 'gsc-token.json'))
DEFAULT_SITE = 'sc-domain:nad-lan.co.il'
API = 'https://www.googleapis.com/webmasters/v3'


def access_token():
    with open(CLIENT, encoding='utf-8') as f: c = json.load(f)
    conf = c.get('installed') or c.get('web') or c
    with open(TOKEN, encoding='utf-8') as f: t = json.load(f)
    refresh = t.get('refresh_token') or t.get('refreshToken')
    if not refresh:
        sys.exit('token file has no refresh_token - interactive re-auth needed')
    data = urllib.parse.urlencode({
        'client_id': conf['client_id'], 'client_secret': conf['client_secret'],
        'refresh_token': refresh, 'grant_type': 'refresh_token'}).encode()
    req = urllib.request.Request(t.get('token_uri', 'https://oauth2.googleapis.com/token'), data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            j = json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit('token refresh FAILED (%s): %s' % (e.code, e.read()[:300]))
    return j['access_token'], j.get('scope', ''), j.get('expires_in')


def call(tok, path, payload=None, method=None):
    req = urllib.request.Request(API + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        method=method or ('POST' if payload is not None else 'GET'),
        headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        sys.exit('API %s FAILED (%s): %s' % (path, e.code, e.read()[:300]))


def cmd_sites(tok):
    for s in call(tok, '/sites').get('siteEntry', []):
        print('%s\t%s' % (s.get('siteUrl'), s.get('permissionLevel')))


def cmd_sitemaps(tok, site):
    for s in call(tok, '/sites/%s/sitemaps' % urllib.parse.quote(site, safe='')).get('sitemap', []):
        print('%s\tlastSubmitted=%s\tlastDownloaded=%s\terrors=%s' % (
            s.get('path'), s.get('lastSubmitted'), s.get('lastDownloaded'), s.get('errors')))


def cmd_submit(tok, site, feedpath):
    """Submit (or resubmit) a sitemap - needs the FULL webmasters scope."""
    call(tok, '/sites/%s/sitemaps/%s' % (
        urllib.parse.quote(site, safe=''), urllib.parse.quote(feedpath, safe='')), method='PUT')
    print('submitted: %s' % feedpath)


def cmd_query(tok, site, start, end, dimensions, limit, out, filter_page):
    body = {'startDate': start, 'endDate': end, 'rowLimit': min(limit, 25000), 'startRow': 0,
            'dataState': 'final'}
    if dimensions: body['dimensions'] = dimensions
    if filter_page:
        op, _, val = filter_page.partition(':')
        body['dimensionFilterGroups'] = [{'filters': [
            {'dimension': 'page', 'operator': op, 'expression': val}]}]
    rows = []
    while True:
        resp = call(tok, '/sites/%s/searchAnalytics/query' % urllib.parse.quote(site, safe=''), body)
        got = resp.get('rows', [])
        rows.extend(got)
        if len(got) < body['rowLimit'] or len(rows) >= limit: break
        body['startRow'] = len(rows)
    if out:
        with open(out, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow((dimensions or []) + ['clicks', 'impressions', 'ctr', 'position'])
            for r in rows:
                w.writerow(list(r.get('keys', [])) + [r['clicks'], r['impressions'], r['ctr'], r['position']])
        print('wrote %d rows -> %s' % (len(rows), out))
    else:
        for r in rows[:50]:
            print('%s\t%s\t%s\t%.1f' % (' | '.join(r.get('keys', ['-'])), r['clicks'], r['impressions'], r['position']))
        if len(rows) > 50: print('... (%d rows total, use --out for full CSV)' % len(rows))


def cmd_totals(tok, site, days):
    end = dt.date.today() - dt.timedelta(days=3)          # final data lags ~2-3 days
    start = end - dt.timedelta(days=days - 1)
    resp = call(tok, '/sites/%s/searchAnalytics/query' % urllib.parse.quote(site, safe=''),
                {'startDate': start.isoformat(), 'endDate': end.isoformat(), 'rowLimit': 1})
    row = (resp.get('rows') or [{}])[0]
    print('range %s..%s  clicks=%s impressions=%s ctr=%.2f%% pos=%.1f' % (
        start, end, row.get('clicks', 0), row.get('impressions', 0),
        100 * row.get('ctr', 0), row.get('position', 0)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('cmd', choices=['sites', 'sitemaps', 'query', 'totals', 'submit-sitemap'])
    p.add_argument('--site', default=DEFAULT_SITE)
    p.add_argument('--feedpath', default='https://nad-lan.co.il/sitemap_index.xml')
    p.add_argument('--start'); p.add_argument('--end')
    p.add_argument('--dimensions', default='query,page')
    p.add_argument('--limit', type=int, default=25000)
    p.add_argument('--out'); p.add_argument('--filter-page')
    p.add_argument('--days', type=int, default=7)
    a = p.parse_args()
    tok, scope, ttl = access_token()
    print('# auth ok, scope=%s, ttl=%ss' % (scope, ttl), file=sys.stderr)
    if a.cmd == 'sites': cmd_sites(tok)
    elif a.cmd == 'sitemaps': cmd_sitemaps(tok, a.site)
    elif a.cmd == 'submit-sitemap': cmd_submit(tok, a.site, a.feedpath)
    elif a.cmd == 'totals': cmd_totals(tok, a.site, a.days)
    else:
        if not (a.start and a.end): sys.exit('query needs --start and --end (YYYY-MM-DD)')
        dims = [d for d in a.dimensions.split(',') if d]
        cmd_query(tok, a.site, a.start, a.end, dims, a.limit, a.out, a.filter_page)


if __name__ == '__main__':
    main()
