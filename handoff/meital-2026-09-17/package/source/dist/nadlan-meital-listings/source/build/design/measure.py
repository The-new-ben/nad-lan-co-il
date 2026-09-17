import asyncio, json, os, re, subprocess, sys
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(HERE)) + '/'
PROJ = BASE + 'canvas/project/'
PREV = BASE + 'canvas_preview/'
os.makedirs(PREV, exist_ok=True)
SIZES = {'Main.dc.html': 1440, 'English.dc.html': 1440, 'Mobile.dc.html': 390, 'MobileFirst.dc.html': 390, 'ListingCard.dc.html': 1440,
         'BusinessCardFront.dc.html': 1050, 'BusinessCardBack.dc.html': 1050, 'ShareImage.dc.html': 1080}

def to_plain(src):
    helmet = re.search(r'<helmet>(.*?)</helmet>', src, re.S).group(1)
    body = re.search(r'</helmet>(.*?)</x-dc>', src, re.S).group(1)
    body = re.sub(r'<sc-if[^>]*>', '', body).replace('</sc-if>', '')
    def hole(m):
        k = m.group(1).strip()
        mm = re.match(r'pills\.(\w+)\.(\w+)', k)
        if mm:
            on = mm.group(1) == 'all'
            return {'bg': '#14212B' if on else 'transparent', 'fg': '#F7F6F2' if on else '#14212B', 'bd': '#14212B' if on else '#E3E1DA', 'pressed': 'true' if on else 'false', 'pick': ''}[mm.group(2)]
        return ''
    body = re.sub(r'\{\{(.*?)\}\}', hole, body)
    lang = re.search(r'<html lang="(\w+)" dir="(\w+)"', src)
    extra = '<style>.hi, .chips, .lcard h3 { height: auto !important; }</style>' if os.environ.get('AUTOH') == '1' else ''
    return f'<!doctype html><html lang="{lang.group(1)}" dir="{lang.group(2)}"><head><meta charset="utf-8">{helmet}{extra}</head><body>{body}</body></html>'

async def measure(files, shots=False):
    out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for f in files:
            w = SIZES[f]
            html = to_plain(open(PROJ + f).read())
            path = PREV + f.replace('.dc.html', '.html')
            open(path, 'w').write(html)
            pg = await b.new_page(viewport={'width': w, 'height': 900}, device_scale_factor=1)
            await pg.goto('file://' + path)
            await pg.evaluate('document.fonts.ready')
            await pg.wait_for_timeout(800)
            r = await pg.evaluate('''() => {
              const root = document.getElementById('root');
              const hi = [...document.querySelectorAll('.hi')].map(e => e.scrollHeight);
              const chips = [...document.querySelectorAll('.chips')].map(e => e.scrollHeight);
              const titles = [...document.querySelectorAll('.lcard h3')].map(e => [e.closest('article').querySelector('span[style*="letter-spacing: 0.06em"]')?.textContent, e.getBoundingClientRect().height, parseFloat(getComputedStyle(e).lineHeight)]);
              const over = [];
              for (const el of root.querySelectorAll('*')) {
                if (el.closest('svg') ) continue;
                const cs = getComputedStyle(el);
                if ((el.scrollWidth > el.clientWidth + 1) && cs.overflow !== 'visible' && el.clientWidth > 0) over.push(['x', el.tagName, (el.textContent||'').trim().slice(0, 40), el.scrollWidth, el.clientWidth]);
                if ((el.scrollHeight > el.clientHeight + 1) && el.clientHeight > 0 && (el.style.height && el.style.height !== 'auto') && !el.id) over.push(['y', el.tagName, (el.className||''), (el.textContent||'').trim().slice(0, 40), el.scrollHeight, el.clientHeight]);
              }
              const fonts = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight);
              return { h: root.scrollHeight, hi, chips, titles, over: over.slice(0, 30), fonts: [...new Set(fonts)].slice(0, 20), docW: document.documentElement.scrollWidth };
            }''')
            out[f] = r
            if shots:
                await pg.screenshot(path=PREV + f.replace('.dc.html', '.png'), full_page=True)
            await pg.close()
        await b.close()
    return out

if __name__ == '__main__':
    shots = '--shots' in sys.argv
    files = [a for a in sys.argv[1:] if a.endswith('.dc.html')] or list(SIZES)
    res = asyncio.run(measure(files, shots))
    for f, r in res.items():
        print(f, 'h=', r['h'], 'docW=', r['docW'], 'hi max=', max(r['hi']) if r['hi'] else None, 'chips max=', max(r['chips']) if r['chips'] else None)
        for o in r['over']:
            print('   OVER', o)
    json.dump(res, open(PREV + 'measure.json', 'w'), ensure_ascii=False, indent=1)
    print('fonts:', res[files[0]]['fonts'])
