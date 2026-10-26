"""Shared helpers for the renewal-map labels proposal (26.10.2026). Read-only toward the live site.

- parse/apply the patch file (urban-map-labels.patch.php.txt) to a COPY of the live urban-map.php
- read the live page (GET only) and find its map block (the <style> + <script> the shortcode prints)
- fill a PHP block's echo tags with the values the live page itself carries (token, REST URLs)
- swap the live block for the patched one inside the live HTML, in memory (for the local browser only)

The public map token lives only in memory: never printed, never written to disk.
"""
import hashlib
import os
import re
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
LIVE_PHP = os.path.join(REPO, 'scripts', 'project-stage', 'live-520', 'urban-map.php')
LIVE_PHP_MD5 = '3864aca919d7e07fed60e49c606e74af'
PATCH = os.path.join(HERE, 'urban-map-labels.patch.php.txt')
TRACK_JSON = os.path.join(REPO, 'plugins', 'nadlan-config', 'assets', 'instruments', 'data', 'renewal-track.json')
LIVE_URL = 'https://nad-lan.co.il/urban-renewal/map/'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'

TOKEN_PHP = '<?php echo esc_js( $token ); ?>'
REST_PHP = '<?php echo $rest; // phpcs:ignore ?>'
LOOKUP_PHP = "<?php echo esc_url( rest_url( 'nadlan/v1/renewal-lookup' ) ); // phpcs:ignore ?>"
BLOCK_START = '<style>\n#nlurm-map{'


def md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()


def parse_patch(path=PATCH):
    txt = open(path, encoding='utf-8').read()
    hunks = []
    for m in re.finditer(r'^=== (.+?) ===\n--- OLD\n(.*?)\n--- NEW\n(.*?)\n=== END$', txt, re.S | re.M):
        hunks.append({'name': m.group(1), 'old': m.group(2), 'new': m.group(3)})
    return hunks


def apply(src, hunks):
    for h in hunks:
        n = src.count(h['old'])
        if n != 1:
            raise SystemExit('hunk "%s": OLD text found %d times (must be exactly once)' % (h['name'], n))
        src = src.replace(h['old'], h['new'], 1)
    return src


def extract_block(text):
    s = text.find(BLOCK_START)
    if s < 0:
        raise SystemExit('map block not found')
    e = text.find('</script>', s) + len('</script>')
    return s, e, text[s:e]


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'replace')


def live_values(live_block):
    tok = re.search(r'mapboxgl\.accessToken="(pk\.[^"]+)"', live_block)
    rest = re.search(r'fetch\("(https://[^"]+/renewal-map-data)"\)', live_block)
    look = re.search(r'fetch\("(https://[^"]+/renewal-lookup)\?city=', live_block)
    if not (tok and rest and look):
        raise SystemExit('live block values not found (token / REST / lookup)')
    return {'token': tok.group(1), 'rest': rest.group(1), 'lookup': look.group(1)}


def fill(block_php, vals):
    out = block_php.replace(TOKEN_PHP, vals['token']).replace(REST_PHP, vals['rest']).replace(LOOKUP_PHP, vals['lookup'])
    if '<?php' in out:
        raise SystemExit('unfilled PHP tag left in the block')
    return out


def live_token():
    _, _, blk = extract_block(fetch(LIVE_URL))
    return live_values(blk)['token']


def token_js():
    return 'window.NLURM_TOKEN="' + live_token() + '";'


def patched_block(parts='AB'):
    if md5(LIVE_PHP) != LIVE_PHP_MD5:
        raise SystemExit('live-520/urban-map.php changed (md5); re-check the patch target')
    hunks = [h for h in parse_patch() if h['name'][0] in parts]
    src = apply(open(LIVE_PHP, encoding='utf-8').read(), hunks)
    return extract_block(src)[2]


def swapped_live_page(live_html=None, parts='AB'):
    """The live page HTML with its map block replaced by the patched block (in memory)."""
    html = live_html if live_html is not None else fetch(LIVE_URL)
    s, e, blk = extract_block(html)
    new = fill(patched_block(parts), live_values(blk))
    return html[:s] + new + html[e:]
