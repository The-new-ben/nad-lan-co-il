#!/usr/bin/env python3
"""
Create DRAFT nadlan_property posts from this package through the WordPress REST API.

Safety
- Dry run by default: prints the preflight report and what would be sent. Add --apply to write.
- Every request forces status=draft. The script has no publish path.
- Authenticate with a WordPress Application Password for an administrator account
  (Users > Profile > Application Passwords). Never use the login password.

Usage (from the package root)
  export WP_URL=https://nad-lan.co.il
  export WP_USER=<admin username>
  export WP_APP_PASSWORD='xxxx xxxx xxxx xxxx xxxx xxxx'
  python3 scripts/create_drafts.py --only L10 --lang he            # dry run, one listing
  python3 scripts/create_drafts.py --only L10 --lang he --apply    # create one draft
  python3 scripts/create_drafts.py --lang both --apply             # all listings, both languages
  python3 scripts/create_drafts.py --broker --lang he               # dry run, broker page (WordPress page, not the listing post type)
  python3 scripts/create_drafts.py --broker --lang both --apply     # broker page drafts in both languages

Output
- data/import-map.json: {"L10-he": 1234, ...} so reruns update instead of duplicating (--update).
"""
import argparse, base64, json, os, sys, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, 'data', 'import-map.json')

def req(method, path, body=None, params=None):
    url = os.environ['WP_URL'].rstrip('/') + '/wp-json' + path
    if params:
        url += '?' + urllib.parse.urlencode(params)
    tok = base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={'Authorization': 'Basic ' + tok, 'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode() or 'null')
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or 'null')

def preflight():
    rep = {'ok': True, 'notes': []}
    st, t = req('GET', '/wp/v2/types/nadlan_property', params={'context': 'edit'})
    if st != 200:
        rep['ok'] = False; rep['notes'].append(f'post type lookup failed: HTTP {st} {t}')
        return rep, None, set()
    base = t.get('rest_base') or 'nadlan_property'
    st, u = req('GET', '/wp/v2/users/me', params={'context': 'edit'})
    caps = (u or {}).get('capabilities', {}) if st == 200 else {}
    if not caps.get('unfiltered_html'):
        rep['ok'] = False; rep['notes'].append('user lacks unfiltered_html: radio tabs, SVG and JSON-LD would be stripped. Use an administrator on a single site, or the meta-render fallback in HANDOFF section 4B.')
    st, o = req('OPTIONS', f'/wp/v2/{base}')
    props = (((o or {}).get('schema') or {}).get('properties') or {})
    meta_keys = set(((props.get('meta') or {}).get('properties') or {}).keys())
    rep['notes'].append(f'rest_base={base}; REST meta keys: {sorted(meta_keys)}')
    return rep, base, meta_keys

def term_ids(names):
    ids, missing = [], []
    for n in names:
        st, res = req('GET', '/wp/v2/nadlan_city', params={'search': n, 'per_page': 20})
        hit = [x['id'] for x in (res or []) if isinstance(x, dict) and x.get('name') == n]
        (ids if hit else missing).append(hit[0] if hit else n)
    return ids, missing

def broker_pages(a):
    langs = ['he', 'en'] if a.lang == 'both' else [a.lang]
    st, u = req('GET', '/wp/v2/users/me', params={'context': 'edit'})
    caps = (u or {}).get('capabilities', {}) if st == 200 else {}
    print(json.dumps({'user_ok': st == 200, 'unfiltered_html': bool(caps.get('unfiltered_html'))}, indent=1))
    if not caps.get('unfiltered_html') and a.apply:
        sys.exit('user lacks unfiltered_html: the filter inputs and SVG would be stripped; stop and read HANDOFF section 12')
    imap = json.load(open(MAP)) if os.path.exists(MAP) else {}
    for lang in langs:
        p = json.load(open(os.path.join(ROOT, 'broker', f'wp-page-{lang}.json')))
        assert p['status'] == 'draft'
        content = open(os.path.join(ROOT, 'broker', p['content_file']), encoding='utf-8').read()
        st, parents = req('GET', '/wp/v2/pages', params={'slug': p['parent_slug'], 'context': 'edit', 'status': 'publish,draft,private'})
        parent = parents[0]['id'] if st == 200 and parents else None
        body = {'status': 'draft', 'title': p['title'], 'slug': p['slug'], 'content': content, 'excerpt': p['excerpt']}
        if parent:
            body['parent'] = parent
        key = f'broker-{lang}'
        print(f"\n{key}: title={p['title']!r} slug={p['slug']} parent_page={'id ' + str(parent) if parent else 'not found (' + p['parent_slug'] + '), page stays top-level'} content={len(content)} chars")
        if not a.apply:
            continue
        if key in imap and not a.update:
            print(f'  exists as page {imap[key]}; pass --update to overwrite the draft')
            continue
        path = f'/wp/v2/pages/{imap[key]}' if (key in imap and a.update) else '/wp/v2/pages'
        st, res = req('POST', path, body)
        if st not in (200, 201):
            print(f'  FAILED HTTP {st}: {json.dumps(res, ensure_ascii=False)[:400]}')
            continue
        imap[key] = res['id']
        print(f"  draft page id {res['id']}  status={res.get('status')}  link={res.get('link')}")
        st2, chk = req('GET', f"/wp/v2/pages/{res['id']}", params={'context': 'edit'})
        raw = ((chk or {}).get('content') or {}).get('raw', '')
        for marker in ('type="radio"', '<svg', 'nlb-lcard'):
            if marker not in raw:
                print(f'  WARNING: {marker} missing after save (kses filtering?)')
        print(f"  Yoast: set title and description from broker/seo-broker.json (wp post meta update {res['id']} _yoast_wpseo_title '...')")
        json.dump(imap, open(MAP, 'w'), indent=1)
    print('\ndone; drafts only')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default='')
    ap.add_argument('--lang', default='both', choices=['he', 'en', 'both'])
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--update', action='store_true')
    ap.add_argument('--broker', action='store_true', help='create the broker profile page drafts instead of listings')
    a = ap.parse_args()
    for k in ('WP_URL', 'WP_USER', 'WP_APP_PASSWORD'):
        if not os.environ.get(k):
            sys.exit(f'missing environment variable {k}')
    if a.broker:
        return broker_pages(a)
    idx = json.load(open(os.path.join(ROOT, 'data', 'listings.json')))['listings']
    only = set(x.strip() for x in a.only.split(',') if x.strip())
    langs = ['he', 'en'] if a.lang == 'both' else [a.lang]
    rep, base, meta_keys = preflight()
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    if not rep['ok'] and a.apply:
        sys.exit('preflight failed; fix the notes above before --apply')
    imap = json.load(open(MAP)) if os.path.exists(MAP) else {}
    for it in idx:
        if only and it['id'] not in only:
            continue
        for lang in langs:
            p = json.load(open(os.path.join(ROOT, 'listings', it['id'], f'wp-{lang}.json')))
            assert p['status'] == 'draft'
            content = open(os.path.join(ROOT, 'listings', it['id'], p['content_file']), encoding='utf-8').read()
            meta = {k: v for k, v in p['meta'].items() if v is not None and (not meta_keys or k in meta_keys)}
            dropped = sorted(k for k, v in p['meta'].items() if v is not None and meta_keys and k not in meta_keys)
            yoast = {k: v for k, v in p['yoast_meta'].items() if k in meta_keys}
            meta.update(yoast)
            ids, missing = term_ids(p['terms']['nadlan_city']) if base else ([], p['terms']['nadlan_city'])
            body = {'status': 'draft', 'title': p['title'], 'slug': p['slug'], 'content': content, 'excerpt': p['excerpt'], 'meta': meta}
            if ids:
                body['nadlan_city'] = ids
            key = f"{it['id']}-{lang}"
            print(f"\n{key}: title={p['title']!r} slug={p['slug']} content={len(content)} chars meta={len(meta)} dropped={dropped} missing_terms={missing} yoast_via_rest={bool(yoast)}")
            if not a.apply:
                continue
            if key in imap and not a.update:
                print(f'  exists as post {imap[key]}; pass --update to overwrite the draft')
                continue
            path = f'/wp/v2/{base}/{imap[key]}' if (key in imap and a.update) else f'/wp/v2/{base}'
            st, res = req('POST', path, body)
            if st not in (200, 201):
                print(f'  FAILED HTTP {st}: {json.dumps(res, ensure_ascii=False)[:400]}')
                continue
            imap[key] = res['id']
            saved = (res.get('content') or {}).get('raw') or ''
            print(f"  draft id {res['id']}  status={res.get('status')}  link={res.get('link')}")
            st2, chk = req('GET', f"/wp/v2/{base}/{res['id']}", params={'context': 'edit'})
            raw = ((chk or {}).get('content') or {}).get('raw', '')
            for marker in ('type="radio"', '<svg', '<details', 'application/ld+json'):
                if marker not in raw:
                    print(f'  WARNING: {marker} missing after save (kses filtering?)')
            if not yoast:
                print(f"  Yoast fields not REST-writable; run: wp post meta update {res['id']} _yoast_wpseo_title '...'; see seo.json")
            json.dump(imap, open(MAP, 'w'), indent=1)
    print('\ndone; drafts only')

if __name__ == '__main__':
    main()
