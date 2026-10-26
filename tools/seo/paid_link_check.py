"""Paid-link check for nad-lan.co.il (read-only; it only downloads public pages).

Rules (inc/ad-safety.php): every outbound link inside a paid surface is rel="sponsored ...", every paid card
shows "ממומן" or "פרסומת", a paid profile shows its label, and a page carries at most N paid cards.
Paid surfaces: elements with data-paid="1", plus (for pages released before the attribute) the existing
markers: a professional card that holds the "ממומן" chip (.nlprc-spon) and a placement aside (.nlpl).

Usage: python tools/seo/paid_link_check.py URL [URL ...] [--cap 3]
Exit code 1 when any FAIL is found.
"""
import argparse
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser

HOST = 'nad-lan.co.il'


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # (tag, is_paid_root, kind)
        self.paid_depth = 0
        self.roots = []          # dicts: kind, links, text
        self.label_found = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = ' ' + (a.get('class') or '') + ' '
        kind = ''
        if a.get('data-paid') == '1':
            kind = 'data-paid'
        elif ' nlpl ' in cls:
            kind = 'placement'
        elif ' nlprc ' in cls:
            kind = 'procard?'
        if ' nlad-label ' in cls:
            self.label_found = True
        is_root = bool(kind) and self.paid_depth == 0
        if tag in ('br', 'img', 'input', 'meta', 'link', 'hr', 'source'):
            return
        self.stack.append((tag, is_root, kind))
        if is_root:
            self.paid_depth = 1
            self.roots.append({'kind': kind, 'cls': cls.strip()[:60], 'links': [], 'text': ''})
        elif self.paid_depth:
            self.paid_depth += 1
        if self.paid_depth and tag == 'a' and a.get('href'):
            self.roots[-1]['links'].append((a.get('href'), a.get('rel') or ''))

    def handle_endtag(self, tag):
        while self.stack:
            t, is_root, _ = self.stack.pop()
            if self.paid_depth:
                self.paid_depth -= 1
            if t == tag:
                break

    def handle_data(self, d):
        if self.paid_depth and self.roots:
            self.roots[-1]['text'] += d


def external(href):
    u = urllib.parse.urlparse(href)
    if u.scheme in ('tel', 'mailto', 'javascript', ''):
        return False
    return bool(u.netloc) and not u.netloc.endswith(HOST)


def check(url, cap):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (paid_link_check)'})
    html = urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'replace')
    s = Scan()
    s.feed(html)
    out, fails = [], 0
    roots = []
    for r in s.roots:
        if r['kind'] == 'procard?':
            if 'ממומן' not in r['text']:
                continue  # an unpaid professional card
            r['kind'] = 'procard'
        roots.append(r)
    cards = [r for r in roots if r['kind'] in ('procard', 'placement') or 'nlprc' in r['cls'] or 'nlpl' in r['cls']]
    for r in roots:
        for href, rel in r['links']:
            if external(href) and 'sponsored' not in rel.split():
                fails += 1
                out.append(f'FAIL  {r["kind"]}: outbound link without rel=sponsored: {href[:70]} rel="{rel}"')
        if (r in cards) and not ('ממומן' in r['text'] or 'פרסומת' in r['text']):
            fails += 1
            out.append(f'FAIL  {r["kind"]}: paid card without a visible "ממומן"/"פרסומת" label')
        if 'nlpe' in r['cls'] and not s.label_found:
            fails += 1
            out.append('FAIL  paid profile without the "פרופיל ממומן" label')
    if len(cards) > cap:
        fails += 1
        out.append(f'FAIL  {len(cards)} paid cards on the page (cap {cap})')
    out.append(f'INFO  paid surfaces: {len(roots)} (cards {len(cards)})')
    return fails, out


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('urls', nargs='+')
    ap.add_argument('--cap', type=int, default=3)
    a = ap.parse_args()
    total = 0
    for u in a.urls:
        try:
            f, lines = check(u, a.cap)
        except Exception as e:  # noqa: BLE001 - report and continue
            f, lines = 1, [f'FAIL  could not read the page: {e}']
        total += f
        print(u)
        for line in lines:
            print('  ' + line)
    print('RESULT:', 'FAIL' if total else 'OK')
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
