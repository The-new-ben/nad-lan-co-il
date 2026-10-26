"""Shared helpers for the renewal-map v2 proposal (26.10.2026). Read-only toward the live site.

- parse/apply urban-map-v2.patch.php.txt to a COPY of the live urban-map.php (scripts/project-stage/live-520/urban-map.php)
- run the new PHP function (nadlan_ur_map_v2_boot) under php-cli with WordPress stubs, to get the exact JSON the page would print
- read the live page (GET only), find its note and its map block, and swap both for the patched ones, in memory, for the local
  test browser only (lib2.swapped_live_page)

The public map token lives only in memory: never printed, never written to disk.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..', '..'))
LIVE_PHP = os.path.join(REPO, 'scripts', 'project-stage', 'live-520', 'urban-map.php')
LIVE_PHP_MD5 = '3864aca919d7e07fed60e49c606e74af'
PATCH = os.path.join(HERE, 'urban-map-v2.patch.php.txt')
DATA = os.path.join(REPO, 'plugins', 'nadlan-config', 'assets', 'instruments', 'data')
TRACK_JSON = os.path.join(DATA, 'renewal-track.json')
PHP = r'C:\Users\777\tools\php-8.3\php.exe'
OUT = os.path.join(HERE, 'out')
LIVE_URL = 'https://nad-lan.co.il/urban-renewal/map/'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'

TOKEN_PHP = '<?php echo esc_js( $token ); ?>'
REST_PHP = '<?php echo $rest; // phpcs:ignore ?>'
LOOKUP_PHP = "<?php echo esc_url( rest_url( 'nadlan/v1/renewal-lookup' ) ); // phpcs:ignore ?>"
V2_PHP = '<?php echo $v2; // phpcs:ignore ?>'
PULLED_PHP = "<?php echo esc_html( function_exists( 'nadlan_ur_source_pulled' ) ? nadlan_ur_source_pulled() : '13.7.2026' ); ?>"
STARTS = ['<style>\n#nlurm-map{', '<style>\n/* renewal map v2']


def md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()


def parse_patch(path=PATCH):
    txt = open(path, encoding='utf-8').read()
    return [{'name': m.group(1), 'old': m.group(2), 'new': m.group(3)}
            for m in re.finditer(r'^=== (.+?) ===\n--- OLD\n(.*?)\n--- NEW\n(.*?)\n=== END$', txt, re.S | re.M)]


def apply(src, hunks):
    for h in hunks:
        n = src.count(h['old'])
        if n != 1:
            raise SystemExit('hunk "%s": OLD text found %d times (must be exactly once)' % (h['name'], n))
        src = src.replace(h['old'], h['new'], 1)
    return src


def revert(src, hunks):
    for h in reversed(hunks):
        if src.count(h['new']) != 1:
            raise SystemExit('revert "%s": NEW text found %d times' % (h['name'], src.count(h['new'])))
        src = src.replace(h['new'], h['old'], 1)
    return src


def block_span(text):
    s = -1
    for st in STARTS:
        s = text.find(st)
        if s > -1:
            break
    if s < 0:
        raise SystemExit('map block not found')
    e = text.find('</script>', s) + len('</script>')
    return s, e


def note_span(text):
    s = text.find('<p class="nlurm-note">')
    if s < 0:
        raise SystemExit('note not found')
    return s, text.find('</p>', s) + len('</p>')


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'replace')


def live_values(html):
    s, e = block_span(html)
    blk = html[s:e]
    tok = re.search(r'mapboxgl\.accessToken="(pk\.[^"]+)"', blk)
    rest = re.search(r'fetch\("(https://[^"]+/renewal-map-data)"\)', blk)
    look = re.search(r'fetch\("(https://[^"]+/renewal-lookup)\?city=', blk)
    ns, ne = note_span(html)
    pulled = re.search(r'נמשך ב-([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4})', html[ns:ne])
    if not (tok and rest and look and pulled):
        raise SystemExit('live values not found (token / REST / lookup / pulled date)')
    return {'token': tok.group(1), 'rest': rest.group(1), 'lookup': look.group(1), 'pulled': pulled.group(1)}


def patched_php():
    if md5(LIVE_PHP) != LIVE_PHP_MD5:
        raise SystemExit('live-520/urban-map.php changed (md5); re-check the patch target')
    return apply(open(LIVE_PHP, encoding='utf-8').read(), parse_patch())


_BOOT = {}


def boot_json(php_src=None):
    """Run nadlan_ur_map_v2_boot() from the patched file under php-cli (WordPress stubbed), with the repo's value.json."""
    if 'v' in _BOOT:
        return _BOOT['v']
    root = os.path.join(OUT, 'php')
    os.makedirs(os.path.join(root, 'inc'), exist_ok=True)
    os.makedirs(os.path.join(root, 'assets', 'instruments', 'data'), exist_ok=True)
    open(os.path.join(root, 'inc', 'urban-map.php'), 'w', encoding='utf-8', newline='\n').write(php_src or patched_php())
    shutil.copyfile(os.path.join(DATA, 'value.json'), os.path.join(root, 'assets', 'instruments', 'data', 'value.json'))
    stub = ("<?php\ndefine('ABSPATH', __DIR__);\nfunction add_filter(){}\nfunction add_action(){}\nfunction add_shortcode(){}\n"
            "function apply_filters($t, $v){ return $v; }\nfunction wp_json_encode($d, $o = 0){ return json_encode($d, $o); }\n"
            "require __DIR__ . '/inc/urban-map.php';\necho nadlan_ur_map_v2_boot();\n")
    open(os.path.join(root, 'stub.php'), 'w', encoding='utf-8', newline='\n').write(stub)
    r = subprocess.run([PHP, os.path.join(root, 'stub.php')], capture_output=True)
    out = r.stdout.decode('utf-8')
    if r.returncode != 0 or not out.startswith('{'):
        raise SystemExit('php boot failed: ' + (r.stderr.decode('utf-8', 'replace') + out)[:400])
    json.loads(out)
    _BOOT['v'] = out
    return out


def fill(text, vals):
    out = (text.replace(TOKEN_PHP, vals['token']).replace(REST_PHP, vals['rest']).replace(LOOKUP_PHP, vals['lookup'])
           .replace(V2_PHP, boot_json()).replace(PULLED_PHP, vals['pulled']))
    if '<?php' in out:
        raise SystemExit('unfilled PHP tag left: ' + out[out.find('<?php'):out.find('<?php') + 80])
    return out


def patched_parts():
    src = patched_php()
    ns, ne = note_span(src)
    bs, be = block_span(src)
    return src[ns:ne], src[bs:be]


def swapped_live_page(html=None):
    """The live page HTML with its note and map block replaced by the patched ones (in memory)."""
    html = html if html is not None else fetch(LIVE_URL)
    vals = live_values(html)
    note, blk = patched_parts()
    bs, be = block_span(html)
    html = html[:bs] + fill(blk, vals) + html[be:]
    ns, ne = note_span(html)
    return html[:ns] + fill(note, vals) + html[ne:]
