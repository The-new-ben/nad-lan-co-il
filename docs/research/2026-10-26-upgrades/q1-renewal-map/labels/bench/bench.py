"""Benchmark capture for the renewal-map label proposal (26.10.2026).

Opens each reference map in real Chrome (Playwright), waits for tiles,
saves a screenshot and a record (final URL, title, blocked or not).
Read-only: no clicks except declining a consent wall when one appears.

Run:  python bench.py            (headless)
      python bench.py --headed   (retry sites that block headless)
      python bench.py --only zillow,madlan --headed
"""
import json, sys, time, io, os
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

SITES = [
    # key, url, viewport, wait seconds, note
    ('google-tlv-z12', 'https://www.google.com/maps/@32.0750,34.8100,12z?hl=iw', (1280, 800), 9, 'Google Maps, Hebrew UI, Tel Aviv at city zoom'),
    ('google-il-z8', 'https://www.google.com/maps/@31.75,34.95,8z?hl=iw', (1280, 800), 9, 'Google Maps, Hebrew UI, country zoom'),
    ('google-search-z12', 'https://www.google.com/maps/search/%D7%A4%D7%99%D7%A0%D7%95%D7%99+%D7%91%D7%99%D7%A0%D7%95%D7%99/@32.0750,34.8100,12z?hl=iw', (1280, 800), 10, 'Google Maps search results as labelled pins'),
    ('google-tlv-390', 'https://www.google.com/maps/@32.0750,34.8100,12z?hl=iw', (390, 844), 9, 'Google Maps phone width'),
    ('mapbox-cluster', 'https://docs.mapbox.com/mapbox-gl-js/example/cluster/', (1280, 900), 9, 'Mapbox GL JS official cluster example'),
    ('mapbox-cluster-html', 'https://docs.mapbox.com/mapbox-gl-js/example/cluster-html/', (1280, 900), 9, 'Mapbox GL JS HTML clusters with custom properties'),
    ('redfin-nyc', 'https://www.redfin.com/city/30749/NY/New-York', (1280, 900), 10, 'Redfin map clusters and price tags'),
    ('zillow-nyc', 'https://www.zillow.com/new-york-ny/', (1280, 900), 10, 'Zillow map clusters and price tags'),
    ('nyt-election', 'https://www.nytimes.com/interactive/2021/upshot/2020-election-map.html', (1280, 900), 10, 'NYT Upshot detailed election map'),
    ('ft-visual-vocabulary', 'https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary', (1280, 900), 5, 'FT Visual Vocabulary (public): proportional symbol maps'),
    ('madlan-tlv', 'https://www.madlan.co.il/for-sale/%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91-%D7%99%D7%A4%D7%95-%D7%99%D7%A9%D7%A8%D7%90%D7%9C', (1280, 900), 10, 'Madlan for-sale map, Tel Aviv'),
    ('govmap', 'https://www.govmap.gov.il/?c=179000,663000&z=4', (1280, 900), 12, 'govmap.gov.il national map, Hebrew labels'),
    ('gov-renewal-arcgis', 'https://moch.maps.arcgis.com/apps/webappviewer/index.html?id=d6191754d18a4fd29ee2e2ca1d040759', (1280, 900), 14, 'Government Urban Renewal Authority map (ArcGIS), the #1 result for the query'),
]

BLOCK_WORDS = ['press & hold', 'captcha', 'are you a human', 'access denied', 'verify you are human', 'unusual traffic', 'blocked', 'px-captcha', 'אנא אמתו']


def decline_consent(page):
    for label in ['Reject all', 'דחייה של הכול', 'דחה הכל', 'Decline', 'Reject']:
        try:
            b = page.get_by_role('button', name=label)
            if b.count() > 0:
                b.first.click(timeout=2000)
                time.sleep(2)
                return label
        except Exception:
            pass
    return None


def main():
    headed = '--headed' in sys.argv
    only = None
    if '--only' in sys.argv:
        only = set(sys.argv[sys.argv.index('--only') + 1].split(','))
    rec_path = os.path.join(HERE, 'bench.json')
    recs = {}
    if os.path.exists(rec_path):
        recs = json.load(open(rec_path, encoding='utf-8'))
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME, headless=not headed, args=['--disable-blink-features=AutomationControlled'])
        for key, url, vp, wait, note in SITES:
            if only and key not in only:
                continue
            ctx = br.new_context(viewport={'width': vp[0], 'height': vp[1]}, locale='he-IL',
                                 device_scale_factor=1, is_mobile=vp[0] < 500, has_touch=vp[0] < 500,
                                 user_agent=None)
            page = ctx.new_page()
            r = {'key': key, 'url': url, 'note': note, 'viewport': vp, 'mode': 'headed' if headed else 'headless',
                 'at_utc': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
            try:
                resp = page.goto(url, wait_until='domcontentloaded', timeout=60000)
                r['status'] = resp.status if resp else None
                time.sleep(3)
                c = decline_consent(page)
                if c:
                    r['consent'] = 'declined via "%s"' % c
                time.sleep(wait)
                r['final_url'] = page.url
                r['title'] = page.title()
                txt = ''
                try:
                    txt = page.inner_text('body', timeout=5000)[:4000].lower()
                except Exception:
                    pass
                r['blocked'] = any(w in txt for w in BLOCK_WORDS) or (r.get('status') in (401, 403, 429))
                shot = os.path.join(HERE, key + '.png')
                page.screenshot(path=shot)
                r['screenshot'] = key + '.png'
            except Exception as e:
                r['error'] = str(e)[:300]
            print(json.dumps(r, ensure_ascii=False))
            recs[key] = r
            ctx.close()
        br.close()
    json.dump(recs, open(rec_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
