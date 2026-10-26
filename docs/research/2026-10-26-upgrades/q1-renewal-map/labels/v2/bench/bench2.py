"""Benchmark captures for the v2 map proposal (26.10.2026): Israeli competitors and world patterns, desktop and phone.

Plain Chrome through Playwright, no stealth flags, no CAPTCHA solving: a page that answers with a block or a challenge is
recorded as blocked (with the HTTP status) and left alone. Headless first; a blocked page gets one try in a visible window.

    python bench2.py            (writes <name>-<w>.png and bench2.json next to this file)
"""
import io
import json
import os
import sys
import time
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
SITES = [
    ('madlan-map', 'https://www.madlan.co.il/for-sale/%D7%A8%D7%9E%D7%AA-%D7%92%D7%9F-%D7%99%D7%A9%D7%A8%D7%90%D7%9C', 'Madlan, for sale, Ramat Gan (map + list)'),
    ('madlan-renewal', 'https://www.madlan.co.il/urban-renewal', 'Madlan, urban renewal hub'),
    ('yad2-map', 'https://www.yad2.co.il/realestate/forsale/map?city=8600', 'Yad2, for sale map, Ramat Gan'),
    ('onmap', 'https://www.onmap.co.il/homes/buy/c_32.068400,34.811400/t_32.110000,34.870000/b_32.030000,34.760000/z_14', 'OnMap, buy, Ramat Gan'),
    ('homeless', 'https://www.homeless.co.il/sale/', 'Homeless, for sale'),
    ('gov-renewal', 'https://www.gov.il/he/departments/topics/mapa-renewal', 'Government renewal authority, map topic page'),
    ('govmap', 'https://www.govmap.gov.il/?c=180000,663000&z=5', 'govmap, Tel Aviv area'),
    ('airbnb', 'https://www.airbnb.com/s/Tel-Aviv--Israel/homes', 'Airbnb, Tel Aviv search (map + list)'),
    ('zillow', 'https://www.zillow.com/new-york-ny/', 'Zillow, New York'),
    ('redfin', 'https://www.redfin.com/city/30749/NY/New-York', 'Redfin, New York'),
]
VIEWS = [(1280, 900, False), (390, 844, True)]
BLOCK_WORDS = ['captcha', 'are you a human', 'access denied', 'press & hold', 'verify you are human', 'unusual traffic', 'blocked', 'perimeterx', 'px-captcha', 'shieldsquare', 'אנחנו צריכים לוודא']


def shoot(br, name, url, w, h, mob):
    ctx = br.new_context(viewport={'width': w, 'height': h}, is_mobile=mob, has_touch=mob, device_scale_factor=1, locale='he-IL')
    pg = ctx.new_page()
    rec = {'url': url, 'w': w}
    try:
        resp = pg.goto(url, wait_until='domcontentloaded', timeout=45000)
        rec['status'] = resp.status if resp else None
        time.sleep(7)
        txt = (pg.evaluate("document.body ? document.body.innerText.slice(0, 4000) : ''") or '').lower()
        rec['title'] = pg.title()[:120]
        rec['blocked_words'] = [b for b in BLOCK_WORDS if b in txt]
        rec['blocked'] = bool(rec['blocked_words']) or (rec['status'] or 0) >= 400
        p = os.path.join(HERE, '%s-%d.png' % (name, w))
        pg.screenshot(path=p)
        rec['png'] = os.path.basename(p)
    except Exception as e:  # noqa: BLE001
        rec['error'] = str(e)[:200]
        rec['blocked'] = True
    ctx.close()
    return rec


def main():
    out = {'at_utc': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), 'how': 'Chrome via Playwright, no stealth flags, no CAPTCHA solving', 'sites': {}}
    only = set(sys.argv[1:])
    with sync_playwright() as p:
        hl = p.chromium.launch(executable_path=CHROME, headless=True)
        hd = None
        for name, url, label in SITES:
            if only and name not in only:
                continue
            for w, h, mob in VIEWS:
                r = shoot(hl, name, url, w, h, mob)
                r['mode'] = 'headless'
                if r.get('blocked'):
                    if hd is None:
                        hd = p.chromium.launch(executable_path=CHROME, headless=False)
                    r2 = shoot(hd, name, url, w, h, mob)
                    r2['mode'] = 'visible window'
                    r2['headless_first'] = {k: r.get(k) for k in ('status', 'blocked_words', 'error')}
                    r = r2
                r['label'] = label
                r['at_utc'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
                out['sites']['%s-%d' % (name, w)] = r
                print(name, w, r.get('mode'), r.get('status'), 'blocked' if r.get('blocked') else 'ok', r.get('blocked_words'), r.get('error', ''))
        hl.close()
        if hd:
            hd.close()
    prev = {}
    pj = os.path.join(HERE, 'bench2.json')
    if os.path.exists(pj) and only:
        prev = json.load(open(pj, encoding='utf-8')).get('sites', {})
    prev.update(out['sites'])
    out['sites'] = prev
    json.dump(out, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
