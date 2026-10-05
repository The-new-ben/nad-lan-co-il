# -*- coding: utf-8 -*-
"""Polite stdlib crawler for nad-lan.co.il (HAD-435, read-only).
BFS from the home page (link depth), then sitemap URLs never reached by links (orphans).
Records status, redirects, title, meta description, h1s, canonical, robots, hreflang, lang,
word counts, JSON-LD types and internal outlinks with anchors. 4 workers, no redirect following
inside a fetch (chains are walked explicitly)."""
import csv, json, re, sys, time, threading, urllib.request, urllib.parse, urllib.error, html
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor

OUT = sys.argv[1] if len(sys.argv) > 1 else None
SITEMAP_CSV = sys.argv[2] if len(sys.argv) > 2 else None
WORKERS = 4
HOSTS = {'nad-lan.co.il', 'www.nad-lan.co.il'}
UA = 'Mozilla/5.0 (compatible; nadlan-seo-audit/1.0; HAD-435 owner audit)'
SKIP_EXT = re.compile(r'\.(jpe?g|png|gif|webp|avif|svg|pdf|mp4|webm|mp3|zip|xml|js|css|ico|glb|gltf|json|txt|woff2?|ttf|vtt|csv|docx?|xlsx?)$', re.I)
SKIP_PATH = re.compile(r'^/(wp-admin|wp-json|wp-content|wp-includes|wp-login|feed|cart|checkout|my-account|xmlrpc)', re.I)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def norm(u):
    s = urllib.parse.urlsplit(u)
    host = (s.hostname or '').lower()
    path = s.path or '/'
    # canonical form: https, host as-is, decoded-then-quoted path
    path = urllib.parse.quote(urllib.parse.unquote(path), safe="/%:@!$&'()*+,;=-._~")
    return urllib.parse.urlunsplit(('https', host, path, s.query, ''))


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None; self._in_title = False
        self.metas = {}; self.canon = []; self.hreflang = []; self.lang = None
        self.h1 = []; self._h1 = None; self.h2 = 0
        self.links = []; self._a = None
        self.skip = 0; self.chrome = 0
        self.words_all = 0; self.words_main = 0
        self.jsonld = []; self._ld = None
        self.stack = []

    def handle_starttag(self, tag, attrs):
        a = dict((k, v or '') for k, v in attrs)
        if tag == 'html': self.lang = a.get('lang')
        if tag in ('script', 'style', 'noscript', 'svg', 'template'):
            if tag == 'script' and 'ld+json' in a.get('type', ''): self._ld = []
            self.skip += 1; self.stack.append(tag); return
        if tag in ('header', 'footer', 'nav') or 'site-header' in a.get('class', '') or 'site-footer' in a.get('class', ''):
            if tag in ('header', 'footer', 'nav'): self.chrome += 1; self.stack.append('chrome:' + tag)
        if tag == 'title' and self.title is None: self._in_title = True; self.title = ''
        elif tag == 'meta':
            n = (a.get('name') or a.get('property') or '').lower()
            if n in ('description', 'robots', 'og:title', 'googlebot'): self.metas[n] = a.get('content', '')
        elif tag == 'link':
            rel = a.get('rel', '').lower()
            if rel == 'canonical': self.canon.append(a.get('href', ''))
            if rel == 'alternate' and a.get('hreflang'): self.hreflang.append((a['hreflang'], a.get('href', '')))
        elif tag == 'h1': self._h1 = ''
        elif tag == 'h2': self.h2 += 1
        elif tag == 'a' and a.get('href'):
            self._a = [a['href'], '', a.get('rel', '')]

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript', 'svg', 'template'):
            if self.skip: self.skip -= 1
            if tag == 'script' and self._ld is not None:
                self.jsonld.append(''.join(self._ld)); self._ld = None
            return
        if tag in ('header', 'footer', 'nav') and self.chrome: self.chrome -= 1
        if tag == 'title': self._in_title = False
        elif tag == 'h1' and self._h1 is not None: self.h1.append(' '.join(self._h1.split())); self._h1 = None
        elif tag == 'a' and self._a is not None:
            self._a[1] = ' '.join(self._a[1].split())[:80]; self.links.append(tuple(self._a)); self._a = None

    def handle_data(self, d):
        if self._ld is not None: self._ld.append(d); return
        if self.skip: return
        if self._in_title: self.title += d
        if self._h1 is not None: self._h1 += d
        if self._a is not None: self._a[1] += d
        n = len(d.split())
        self.words_all += n
        if not self.chrome: self.words_main += n


def fetch1(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html'})
    t = time.time()
    try:
        r = OPENER.open(req, timeout=40)
        code = r.getcode(); hdr = r.headers; body = r.read(4_000_000)
    except urllib.error.HTTPError as e:
        code = e.code; hdr = e.headers; body = e.read(2_000_000) if code < 300 or code >= 400 else b''
    except Exception as e:
        return {'status': -1, 'error': str(e)[:200], 'ms': int(1000 * (time.time() - t))}
    return {'status': code, 'hdr': hdr, 'body': body, 'ms': int(1000 * (time.time() - t))}


def crawl_one(url):
    rec = {'url': url, 'chain': []}
    cur = url
    for hop in range(6):
        r = fetch1(cur)
        time.sleep(0.15)
        if r['status'] in (301, 302, 303, 307, 308):
            loc = urllib.parse.urljoin(cur, r['hdr'].get('Location', ''))
            rec['chain'].append([cur, r['status']])
            cur = loc
            if urllib.parse.urlsplit(cur).hostname not in HOSTS: break
            continue
        break
    rec['status'] = r['status'] if not rec['chain'] else rec['chain'][0][1]
    rec['final_url'] = cur; rec['final_status'] = r['status']; rec['ms'] = r.get('ms')
    if r.get('error'): rec['error'] = r['error']
    if rec['chain']:
        # record the redirect but do not parse the target here (target gets its own record)
        return rec
    hdr = r.get('hdr')
    if hdr is None: return rec
    ct = hdr.get('Content-Type', '')
    rec['ct'] = ct; rec['xrobots'] = hdr.get('X-Robots-Tag', '')
    rec['bytes'] = len(r.get('body') or b'')
    if 'html' not in ct or not r.get('body'): return rec
    p = P()
    try:
        p.feed(r['body'].decode('utf-8', 'replace'))
    except Exception as e:
        rec['parse_error'] = str(e)[:120]
    rec.update({
        'title': (p.title or '').strip(), 'desc': p.metas.get('description'), 'robots': p.metas.get('robots', ''),
        'canonical': p.canon, 'hreflang': p.hreflang, 'lang': p.lang, 'h1': p.h1, 'h2': p.h2,
        'words_all': p.words_all, 'words_main': p.words_main,
        'ld_types': sorted(set(re.findall(r'"@type"\s*:\s*"([^"]+)"', ' '.join(p.jsonld))))[:20],
    })
    links = {}
    for href, anchor, rel in p.links:
        if href.startswith(('mailto:', 'tel:', 'javascript:', '#', 'whatsapp:', 'sms:')): continue
        absu = urllib.parse.urljoin(url, href)
        s = urllib.parse.urlsplit(absu)
        if s.hostname not in HOSTS: continue
        key = (absu.split('#')[0], 'nofollow' in rel)
        if key not in links: links[key] = anchor
    rec['links'] = [[k[0], a, int(k[1])] for k, a in links.items()]
    return rec


def crawlable(u):
    s = urllib.parse.urlsplit(u)
    if s.hostname not in HOSTS: return False
    if s.query: return False
    if SKIP_EXT.search(s.path) or SKIP_PATH.search(s.path): return False
    return True


def main():
    sm = [norm(r['url']) for r in csv.DictReader(open(SITEMAP_CSV, encoding='utf-8'))]
    seen = {}
    out = open(OUT, 'w', encoding='utf-8')
    lock = threading.Lock()
    level = [norm('https://nad-lan.co.il/')]
    seen[level[0]] = 0
    depth = 0
    total = 0
    pool = ThreadPoolExecutor(WORKERS)

    def run(batch, d, phase):
        nonlocal total
        nxt = []
        for rec in pool.map(crawl_one, batch):
            rec['depth'] = d; rec['phase'] = phase
            targets = []
            if rec.get('chain'):
                targets.append(norm(rec['final_url']))
            for l in rec.get('links', []):
                targets.append(norm(l[0]))
            for t in targets:
                if crawlable(t) and t not in seen:
                    seen[t] = (d + 1) if d is not None else None
                    nxt.append(t)
            with lock:
                out.write(json.dumps(rec, ensure_ascii=False) + '\n'); total += 1
        out.flush()
        print('phase=%s depth=%s fetched=%d total=%d next=%d' % (phase, d, len(batch), total, len(nxt)), flush=True)
        return nxt

    while level and total < 9000:
        level = run(level, depth, 'links')
        depth += 1
    orph = [u for u in dict.fromkeys(sm) if u not in seen]
    for u in orph: seen[u] = None
    print('sitemap urls not reached by links:', len(orph), flush=True)
    level = orph
    while level and total < 12000:
        level = run(level, None, 'sitemap-only')
    out.close()
    print('DONE', total)


if __name__ == '__main__':
    main()
