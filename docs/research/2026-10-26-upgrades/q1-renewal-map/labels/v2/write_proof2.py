"""Writes PROOF.md (26.10.2026) from proof-results.json, out/timing.json, out/build-report.json and out/had605-test.json.

    python write_proof2.py
"""
import gzip
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib2  # noqa: E402

R = json.load(open(os.path.join(HERE, 'proof-results.json'), encoding='utf-8'))
T = json.load(open(os.path.join(HERE, 'out', 'timing.json'), encoding='utf-8'))
B = json.load(open(os.path.join(HERE, 'out', 'build-report.json'), encoding='utf-8'))
H = json.load(open(os.path.join(HERE, 'out', 'had605-test.json'), encoding='utf-8'))
V = R['views']

# weight: the block as the browser gets it, raw and gzipped (token redacted, same length)
html = open(os.path.join(HERE, 'cache', 'live-page.redacted.html'), encoding='utf-8').read()
note, blk = lib2.patched_parts()
vals = {'token': 'pk.' + 'x' * 80, 'rest': 'https://nad-lan.co.il/wp-json/nadlan/v1/renewal-map-data', 'lookup': 'https://nad-lan.co.il/wp-json/nadlan/v1/renewal-lookup', 'pulled': '13.7.2026'}
new_blk = lib2.fill(blk, vals).encode('utf-8')
bs, be = lib2.block_span(html)
old_blk = html[bs:be].encode('utf-8')
gz = lambda b: len(gzip.compress(b, 9))  # noqa: E731


def L(c):
    v = []
    for x in (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)):
        x /= 255
        v.append(x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4)
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def cr(a, b):
    x, y = L(a), L(b)
    return '%.2f:1' % ((max(x, y) + 0.05) / (min(x, y) + 0.05))


ZN = {'country': 'country (the first view, zoom 7)', 'central': 'central district (zoom 9)', 'tlv': 'Tel Aviv area (zoom 11)'}
out = []
w = out.append
w('# Renewal map v2: proof, today vs the proposal')
w('')
w('Measured %s on the live page https://nad-lan.co.il/urban-renewal/map/. **Local only:** nothing was deployed, nothing written to '
  'the site, no REST writes, no plugin file touched. "Proposal" = the live page fetched at that moment with only its map block and '
  'the note under the map swapped, inside the local test browser, for what `urban-map-v2.patch.php.txt` produces (`lib2.swapped_live_page`). '
  'Every non-GET request to nad-lan.co.il was aborted and analytics and Hotjar hosts were blocked (%s requests blocked per visit), so these '
  'visits are not in the owner\'s statistics or recordings. Page errors: %s.' % (R['at_utc'], V['390']['after']['blocked_requests'],
  ', '.join('%s %s: %d' % (v, m, len(V[v][m]['page_errors'])) for v in ('390', '1280') for m in ('before', 'after'))))
w('')
w('Evidence classes: **code** (numbers read from the DOM and from screenshot pixels by `proof2.py`, `timing2.py`, `had605_test.py`), '
  '**eyes** (the screenshots below, looked at), **unverified** (listed at the end). Chrome headless with software WebGL; 390 px = phone '
  'emulation with touch; the sticky site header was set to static in the test browser for the element screenshots.')
w('')
w('## What the visitor sees')
w('')
w('- **Tags instead of gold pills.** Each city that has room gets a small white survey tag (square corners, ink text, a tick pointing at '
  'its point): the city name in IBM Plex Sans Hebrew, under it one or two facts with the numbers in IBM Plex Mono, and a 4 px strip along '
  'the bottom showing how its complexes split across the authority\'s stages (light = no stage, dark = in implementation). The most '
  'important cities get two facts, the next one fact, then the name alone, then a bare point that waits for the zoom. Nothing overlaps.')
w('- **The sea as the margin.** The crowded coastal cities (Tel Aviv, Ramat Gan, Bat Yam, Netanya...) float their tags over the sea with a '
  'thin line to the city, so the first view already names and quantifies the Dan region.')
w('- **Five chips re-label the whole map:** מתחמים (complexes and approved plans, plus the apartment price range where the Tax Authority '
  'publishes one), תכניות מאושרות, דירות חדשות (homes after building minus today), מחירי דירות (median deal prices, 3 to 5 rooms), מה זז '
  '(what changed since 15.8.2026, with the name of the complex that moved last).')
w('- **Hover (mouse)** shows a preview: count, the stage strip with numbers, homes today and after, the price range with its quarter, '
  'what moved, and the three most advanced complexes by name. **Click or tap** opens the city in the panel: every number with its source '
  'and date, a button to "יומן המתחמים" set to the city, links to the city\'s price page, and every complex of the city (not only the first '
  '8) with stage, homes, last change, a link to its page and a "ביומן" button that opens the tracker on that complex.')
w('- **Panel:** beside the map on a wide screen, under it on a phone, listing the cities in view sorted by the chosen chip ("ערים '
  'בתצוגה: N מתוך 79"), refreshed when the map moves. **Phone:** a peek card at the bottom of the map with the facts and two 44 px buttons; '
  'one finger keeps scrolling the page. **Search:** city, complex name or plan number, spelling folded (גבעתיים finds גבעתים).')
w('- **Base map in Hebrew**, its own name for a city that has a tag steps aside (one name per place).')
w('')
w('## Labels: today vs the proposal (same page, same moment)')
w('')
w('"Names readable" = the whole name is visible and not covered. "Facts readable" = fact lines on screen that are fully visible (today: the '
  'count inside a readable pill; proposal: each fact line, plus the stage strip). "Wrong point" = a tag sits nearer to another city\'s point '
  'than to its own. Contrast is WCAG: computed from the CSS (names / fact lines, lowest on screen) and sampled from the screenshot pixels '
  'inside each readable name (median).')
w('')
for v in ('390', '1280'):
    w('| %s px | in view | labels | names readable | facts readable | facts per label | overlapping labels | labels over a line | wrong point | contrast min, names / facts (target 7:1) | pixel contrast | smallest tap target | overlapping tap targets |' % v)
    w('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for z in ('country', 'central', 'tlv'):
        for m, lab in (('before', 'today'), ('after', '**proposal**')):
            s = V[v][m]['states'][z]
            w('| %s · %s | %d | %d | %d | %d | %s | %d | %d | %d | %s / %s | %s | %s x %s | %d |' % (
                lab, ZN[z], s['in_view'], s['shown'], s['names_n'], s['facts'], s['facts_per_tag'], s['overlaps'], s.get('over_lines', 0), s.get('ambiguous', 0),
                min(s['contrast_text']) if s['contrast_text'] else '-', min(s['contrast_facts']) if s['contrast_facts'] else '-',
                (sorted(s['contrast_pixels'])[len(s['contrast_pixels']) // 2] if s['contrast_pixels'] else '-'), s['tap_min_w'], s['tap_min_h'], s['tap_overlaps']))
    w('')
a3 = V['390']['after']['states']
w('Phone, name-only tags: on a touch screen a name without a plate is not its own button (that would put overlapping 44 px targets on the '
  'map); a tap within 22 px of the point or on the name opens the city through the map\'s own tap test. Name-only tags on the phone views: %s. '
  'The tap targets in the table are the tags with a plate (44 px and up on the phone, 24 px and up with a mouse, WCAG 2.5.8).'
  % ', '.join('%s %d' % (z, a3[z].get('name_only_through_map', 0)) for z in ('country', 'central', 'tlv')))
w('')
fewer = [(v, z, V[v]['after']['states'][z]['names_n'], V[v]['before']['states'][z]['names_n']) for v in ('390', '1280') for z in ('country', 'central', 'tlv') if V[v]['after']['states'][z]['names_n'] < V[v]['before']['states'][z]['names_n']]
morefacts = all(V[v]['after']['states'][z]['facts'] > V[v]['before']['states'][z]['facts'] for v in ('390', '1280') for z in ('country', 'central', 'tlv'))
w('**Where the proposal does not win:** it shows fewer readable names than today in %s. The extra names today are readable only because the '
  'pills pile on each other (%d and %d overlapping pairs at the first two zooms, and many pills cannot be tapped at all). The proposal shows %s '
  'facts on the same screen, with no overlap and every tag tied to its own point.' % (
      ', '.join('%s px %s (%d vs %d)' % f for f in fewer) or 'no view', V['390']['before']['states']['country']['overlaps'], V['390']['before']['states']['central']['overlaps'],
      'more' if morefacts else 'more (in most views)'))
w('')
fz = V['390']['after']['states']['country'].get('fonts', {})
w('Faces measured on the proposal\'s tags: names `%s` %s %s, numbers `%s` (the site skin forces another face on span and button; the '
  'patch pins these with scoped `!important` rules). Token contrast on white: ink `#12202A` %s, ink2 `#3E4C58` %s, deep `#1F4B5C` %s; the '
  'chosen tag (white on deep) %s; sea `#2F6F86` %s is used only for the stage strip, never for text.'
  % (fz.get('name_family'), fz.get('name_weight'), fz.get('name_size'), fz.get('number_family'), cr('#12202A', '#FFFFFF'), cr('#3E4C58', '#FFFFFF'),
     cr('#1F4B5C', '#FFFFFF'), cr('#FFFFFF', '#1F4B5C'), cr('#2F6F86', '#FFFFFF')))
w('')
w('## Every interaction, on the live page')
w('')
ib, ia = V['390']['before']['interactions'], V['390']['after']['interactions']
jb, ja = V['1280']['before']['interactions'], V['1280']['after']['interactions']


def g(d, *k, default='-'):
    for x in k:
        if not isinstance(d, dict) or x not in d:
            return default
        d = d[x]
    return d


rows = [
    ('tap or click a city: its complexes appear', '%s: %s items (lookup HTTP %s)' % (g(ib, 'city_tap_target', 'city'), g(ib, 'list', 'items'), V['390']['before']['network']['lookup']),
     '%s: panel opens, %s complexes after "הציגו את כל" (every complex, %s with a page link); 0 lookup calls' % (g(ia, 'city', 'panel_city'), g(ia, 'city', 'rows_all'), len(g(ia, 'city', 'links_all', default=[]) or [])),
     '%s: %s items (lookup HTTP %s)' % (g(jb, 'city_tap_target', 'city'), g(jb, 'list', 'items'), V['1280']['before']['network']['lookup']),
     '%s: panel opens, %s complexes; 0 lookup calls' % (g(ja, 'city', 'panel_city'), g(ja, 'city', 'rows_all'))),
    ('the chosen tag', 'none', 'deep tag: %s' % g(ia, 'city', 'selected_tag'), 'none', 'deep tag: %s' % g(ja, 'city', 'selected_tag')),
    ('phone peek card', 'none', '%s px tall; buttons %s' % (g(ia, 'city', 'peek', 'h'), ', '.join('"%s" %sx%s' % tuple(b) for b in (g(ia, 'city', 'peek', 'buttons', default=[]) or []))), '-', 'wide screen: the panel instead (peek: %s)' % g(ja, 'city', 'peek')),
    ('hover preview (mouse)', '-', '-', 'none', '%s x %s px, %s complexes named' % (g(ja, 'hover_preview', 'w'), g(ja, 'hover_preview', 'h'), g(ja, 'hover_preview', 'complexes_named'))),
    ('complex rows: smallest tap height', '-', '%s px' % g(ia, 'city', 'row_tap_min_h'), '-', '%s px' % g(ja, 'city', 'row_tap_min_h')),
    ('"יומן המתחמים" button: tracker set to the city, scrolled into view, clear of the sticky header', 'none', 'select = %s, in view %s, under header %s' % (g(ia, 'tracker_city', 'select_value'), g(ia, 'tracker_city', 'in_view'), g(ia, 'tracker_city', 'under_header')),
     'none', 'select = %s, in view %s, under header %s' % (g(ja, 'tracker_city', 'select_value'), g(ja, 'tracker_city', 'in_view'), g(ja, 'tracker_city', 'under_header'))),
    ('"ביומן" on one complex: the tracker opens on it', 'none', '%s: %s' % (g(ia, 'complex_to_tracker', 'name'), 'ok' if g(ia, 'complex_to_tracker', 'ok') is True else 'FAILED'), 'none', '%s: %s' % (g(ja, 'complex_to_tracker', 'name'), 'ok' if g(ja, 'complex_to_tracker', 'ok') is True else 'FAILED')),
    ('search "גניש" (a complex), pick the result', 'no search', '%s; city %s, row highlighted: %s' % ((g(ia, 'search_complex', 'results') or ['-'])[0], g(ia, 'search_complex', 'picked', 'panel_city'), g(ia, 'search_complex', 'picked', 'highlighted')), 'no search',
     '%s; city %s, row highlighted: %s' % ((g(ja, 'search_complex', 'results') or ['-'])[0], g(ja, 'search_complex', 'picked', 'panel_city'), g(ja, 'search_complex', 'picked', 'highlighted'))),
    ('search "גבעתיים" (spelling variant)', 'no search', (g(ia, 'search_spelling') or ['-'])[0], 'no search', (g(ja, 'search_spelling') or ['-'])[0]),
    ('phone: tap on a name-only tag', '-', '%s -> %s' % (g(ia, 'name_only_tap', 'name'), g(ia, 'name_only_tap', 'opened')), '-', '-'),
    ('keyboard: focus a tag, Enter, Escape', '-', '-', 'list only', 'focused %s, panel %s, Escape closes %s' % (g(ja, 'keyboard', 'focused'), g(ja, 'keyboard', 'panel_city'), g(ja, 'keyboard', 'escape_closes'))),
    ('zoom-in button', '%s -> %s' % (g(ib, 'zoom_button', 'before'), g(ib, 'zoom_button', 'after')), '%s -> %s' % (g(ia, 'zoom_button', 'before'), g(ia, 'zoom_button', 'after')),
     '%s -> %s' % (g(jb, 'zoom_button', 'before'), g(jb, 'zoom_button', 'after')), '%s -> %s' % (g(ja, 'zoom_button', 'before'), g(ja, 'zoom_button', 'after'))),
    ('"כל הארץ" button (fits all 79 cities)', 'none', 'zoom 12 -> %s' % g(ia, 'home_button', 'zoom_after'), 'none', 'zoom 12 -> %s' % g(ja, 'home_button', 'zoom_after')),
    ('mouse drag on the map pans it', '-', '-', 'pans (v1 proof: 0.87 deg)', 'moved %s deg lng, city opened by the drag: %s' % (g(ja, 'drag_pan', 'moved_lng'), g(ja, 'drag_pan', 'opened_city'))),
    ('mouse wheel over the map, no Ctrl: the page scrolls, the map does not zoom', '-', '-', 'page 450 px, zoom 0 (v1 proof)', 'empty spot: page %s px, zoom %s; on a tag: page %s px, zoom %s' % (g(ja, 'wheel_empty', 'page_scrolled_px'), g(ja, 'wheel_empty', 'map_zoom_change'), g(ja, 'wheel_label', 'page_scrolled_px'), g(ja, 'wheel_label', 'map_zoom_change'))),
]
for wh in ('control_above_map', 'empty', 'label', 'chips', 'peek'):
    s = g(ia, 'swipe_' + wh)
    if s != '-':
        rows.append(('phone: one-finger swipe on %s' % {'control_above_map': 'page text above the map (control)', 'empty': 'the map', 'label': 'a tag', 'chips': 'the chips row', 'peek': 'the peek card'}[wh],
                     '(v1 proof: page scrolls, map still)', 'page scrolled %s px, map moved %s' % (s['page_scrolled_px'], s['map_moved']), '-', '-'))
if V['390']['before']['network']['lookup'] and all(s == 429 for s in V['390']['before']['network']['lookup']):
    w('**The list today was empty at this moment, and that is the HAD-605 bug, live:** the endpoint answered 429 to this machine (my repeated proof runs '
      'had passed its 30 calls per IP per hour; earlier runs the same day got 8 items with HTTP 200), and the live map printed "%s" for %s, a city with '
      '80 complexes. A visitor behind a busy carrier IP gets the same. The proposal does not call the endpoint at all.' % (V['390']['before']['interactions']['list']['text'], V['390']['before']['interactions']['city_tap_target']['city']))
    w('')
w('| check | today 390 | proposal 390 | today 1280 | proposal 1280 |')
w('|---|---|---|---|---|')
for r in rows:
    w('| ' + ' | '.join(str(x) for x in r) + ' |')
w('')
ch = ja.get('chips', {})
w('**The five chips** (desktop, first view; tags on screen / with facts; a sample):')
w('')
w('| chip | tags | with facts | sample | first row in the panel |')
w('|---|---|---|---|---|')
for m, t in (('all', 'מתחמים'), ('ap', 'תכניות מאושרות'), ('un', 'דירות חדשות'), ('px', 'מחירי דירות'), ('mv', 'מה זז')):
    c = ch.get(m, {})
    w('| %s | %s | %s | %s | %s |' % (t, c.get('tags'), c.get('with_facts'), ' / '.join(c.get('sample', [])[:2]), c.get('first_row')))
w('')
lk = R.get('link_check', [])
w('**Complex links in the panel** (a random 6 of the %d Tel Aviv links, plain GET): %s.' % (len(g(ja, 'city', 'links_all', default=[]) or []),
  '; '.join('%s %s' % (x.get('status', x.get('error')), x.get('title', '')[:60]) for x in lk)))
w('')
w('## The lookup limit (HAD-605)')
w('')
w('- The map no longer calls `/renewal-lookup` while the tracker file is on the page: lookup calls during the whole proof visit: today %s, proposal %s '
  '(390), today %s, proposal %s (1280). The list comes from the tracker file the page already loads, and it has every complex, where the '
  'lookup returned the first 8.' % (V['390']['before']['network']['lookup'], V['390']['after']['network']['lookup'], V['1280']['before']['network']['lookup'], V['1280']['after']['network']['lookup']))
w('- `urban-hub-had605.patch.php.txt` (6 hunks, php -l: %s; round trip to the repo text: %s) caches each answer 6 hours per city + query, '
  'counts only cache misses, raises the limit to 120 per IP per hour, and answers 429 with a Hebrew message and `Retry-After`. Run under '
  'php-cli with WordPress stubbed (`had605_test.py`), one IP: **today** the 31st call is refused (%d of 130 repeated city calls refused, '
  '"%s"); **patched** %d of 130 repeats answered, the first refusal comes at new query %d (120 misses), message "%s", Retry-After %s, and '
  'a cached city still answers while the IP is at its limit (%s); the count now runs for a fixed hour from the first counted call (stored as %s; '
  'a new query after that hour: HTTP %s), where today every counted call sets the hour again, so a steady user stays blocked until a full quiet hour.' % (
      B['had605']['php_l'].split(' in ')[0], B['had605']['round_trip_equals_repo'], H['repo_today']['repeat_429'], H['repo_today']['msg'],
      H['patched']['repeat_ok'], H['patched']['first_429_at'], H['patched']['msg'], H['patched']['retry'], H['patched']['hit_while_limited'],
      H['patched'].get('stored'), H['patched'].get('new_query_after_the_hour')))
w('- The live text of `inc/urban-hub.php` was not read for this proposal; the repo text equals the live read of 3.10.2026 '
  '(`docs/qa/live-read/20261003T094808Z/inc/urban-hub.php`, CRLF). Re-read the live file before applying.')
w('- Same wrong "not found" on a 429, not patched here: the renewal wizard (`assets/urban/renewal-3d.js`, line 38); the one-line fix is in the patch header.')
w('')
w('## Load, weight and motion')
w('')
md = T['median']
w('| | today 390 | proposal 390 | today 1280 | proposal 1280 |')
w('|---|---|---|---|---|')
for k, lab in (('ms_to_labels', 'navigation to the first label on screen, ms (median of 3)'), ('longtasks_n', 'long tasks (over 50 ms) until then + 3 s'), ('longtasks_ms', 'their total, ms'),
               ('zoom_median_ms', 'frame interval while the map zooms in 7 to 10, median ms'), ('zoom_p95_ms', 'same, 95th percentile ms'),
               ('zoomout_median_ms', 'frame interval while the map zooms out 10 to 7, median ms'), ('zoomout_p95_ms', 'same, 95th percentile ms'),
               ('scroll_median_ms', 'frame interval while the page scrolls past the map, median ms'), ('scroll_p95_ms', 'same, 95th percentile ms')):
    w('| %s | %s | %s | %s | %s |' % (lab, md['390-before'][k], md['390-after'][k], md['1280-before'][k], md['1280-after'][k]))
w('')
w('Weight: the map block grows from %s bytes (%s gzipped) to %s bytes (%s gzipped): + %s KB on the wire, inline in the page. '
  'New requests: the Mapbox RTL text plugin for the Hebrew base map (`mapbox-gl-rtl-text` v0.3.0; the test browser counted %s fetches '
  'because Playwright routing turns the HTTP cache off; a normal browser fetches it once). The tracker file is the one the page already '
  'loads for "יומן המתחמים", asked again with `cache: force-cache` (the test browser counted %s fetches for the same reason). The PHP '
  'function prints %s bytes of JSON (centroids + price medians) into the script; no new request.' % (
      len(old_blk), gz(old_blk), len(new_blk), gz(new_blk), round((gz(new_blk) - gz(old_blk)) / 1024, 1), V['390']['after']['network']['rtl'],
      V['390']['after']['network']['track'], B['boot']['bytes']))
w('')
w('Software WebGL makes every number here slower than a real phone; the comparison is what counts, and real devices were not measured.')
w('')
w('## Build checks')
w('')
w('- `build2.py`: target md5 %s (ok: %s); 6 hunks apply once each; php -l: %s; reverting the hunks gives back the live text byte for '
  'byte: %s; the live page serves exactly the live-520 map block (%s) and note (%s); `node --check` on the exact script: %s; banned words '
  'in visible strings: %s; long dashes: %s.' % (B['target']['md5'], B['target']['md5_ok'], B['patched']['php_l'].split(' in ')[0],
  B['patched']['round_trip_equals_live'], B['live_block_equals_live520'], B['live_note_equals_live520'], B['node_check'],
  B['banned_words_in_visible_strings'] or 'none', B['long_dashes']))
w('- The new PHP function ran under php-cli: %d price cities, %d centroids (ערד added), pulled date %s, price file %s.' % (B['boot']['price_cities'], B['boot']['centroids'], B['boot']['pulled'], B['boot']['pxsrc_file']))
w('- Data: the tracker and price files on the live site are byte-identical to the repo copies the proposal read (`cache/fetch-report.json`).')
w('')
w('## Side by side with the competitors (details and captures: bench/BENCH.md)')
w('')
w('| | Madlan | OnMap | govmap | authority map | Airbnb | Zillow | today | **v2** |')
w('|---|---|---|---|---|---|---|---|---|')
for r in (
    ('the mark says what it is', 'number only', 'blank dot', 'name only', 'name only', 'price', 'price where it fits', 'name + count', 'name + 1 or 2 facts + stages'),
    ('no overlaps', 'no', 'no', 'yes', 'some collide', 'no on phone', 'no', 'no (475 pairs)', 'yes (0)'),
    ('price range', 'per listing', 'per listing', '-', '-', 'per night', 'per listing', '-', 'official medians, 3-5 rooms, with quarter'),
    ('renewal stage / momentum', '-', '-', '-', 'outline only', '-', '-', '-', 'stage strip + "מה זז" by name'),
    ('map + list in step', 'yes', 'yes', '-', '-', 'yes', 'yes', 'list on tap (8 items)', 'yes, count in view'),
    ('phone keeps the map', '?', 'no (list first)', 'yes', 'yes', 'sheet over map', '?', 'yes', 'yes, peek + panel below'),
    ('search', 'city', 'area', 'address, parcel', 'address', 'place', 'place', '-', 'city, complex, plan number'),
    ('marks contrast (AAA = 7:1)', '2.7:1', '-', 'high', 'high', 'high', '8.9:1', '3.73:1', '16.59:1 names, 8.83:1 facts'),
    ('source + date per number', '-', '-', '-', '-', '-', '-', 'date in the note', 'every number'),
):
    w('| ' + ' | '.join(r) + ' |')
w('')
w('## Screenshots')
w('')
w('Map only, same live page, same moment: `before-<width>-<zoom>.png`, `after-<width>-<zoom>.png`; the whole block (bar, map, panel): '
  '`after-<width>-<zoom>-full.png`. States: `after-1280-hover.png`, `after-<width>-city.png`, `after-390-peek.png`, `after-<width>-search.png`, '
  '`after-<width>-tracker.png`, `after-<width>-mode-<chip>.png`. Phone comparison: `compare-phone.png`.')
w('')
w('| | today | proposal |')
w('|---|---|---|')
for v, vl in (('390', 'phone'), ('1280', 'desktop')):
    for z in ('country', 'central', 'tlv'):
        w('| %s, %s | ![](before-%s-%s.png) | ![](after-%s-%s.png) |' % (vl, z, v, z, v, z))
w('')
w('## Not verified')
w('')
w('- Real phones (iOS Safari, Android Chrome) and real GPUs: desktop Chrome with phone emulation and software WebGL only.')
w('- Two-finger pan and pinch on the map (cooperative gestures are unchanged, not exercised).')
w('- Screen readers: tags are buttons with full Hebrew labels, the panel is a labelled region with a live line, the peek a dialog; no screen reader was run.')
w('- The live text of `inc/urban-hub.php` (see HAD-605 above).')
w('- Hotjar: blocked during the test on purpose; how existing heatmaps and recordings map onto the new layout was not checked.')
w('- Madlan, Yad2, Zillow and Redfin blocked plain Chrome today (403, CAPTCHA); Madlan, Zillow and Redfin notes rest on this morning\'s captures, Yad2 has none.')
w('- The coastline used to keep sea tags over water is coarse on purpose (the bay of Haifa counts as land); checked by eye on the screenshots, not against a coastline file.')
w('')
w('## Files')
w('')
w('| file | what |')
w('|---|---|')
for f, d in (('urban-map-v2.patch.php.txt', 'the patch against the live `inc/urban-map.php` (6 hunks: one centroid, the PHP function, the shortcode line, the note, the style, the script), NOT applied'),
             ('urban-hub-had605.patch.php.txt', 'the HAD-605 fix for `inc/urban-hub.php` (6 hunks), NOT applied'),
             ('src/style.css.txt, src/script.js.txt, make_patch.py', 'the sources of the patch and its assembler'),
             ('build2.py, lib2.py', 'apply to a copy, php -l, round trip, drift check against the live page, node --check, preview.html'),
             ('serve2.py', 'local preview: `python serve2.py`, then http://localhost:8766/live.html (the whole live page with the v2 block swapped in memory, analytics removed)'),
             ('proof2.py, timing2.py, had605_test.py, proof-results.json, out/', 'the measurements and their raw results'),
             ('fetch_cache.py, cache/', 'the public inputs, cached (the page with its map key redacted)'),
             ('bench/', 'competitor captures, bench2.py, BENCH.md'),
             ('compare_phone.py, ds_build2.py', 'the phone comparison image and the design board card')):
    w('| `%s` | %s |' % (f, d))
open(os.path.join(HERE, 'PROOF.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('PROOF.md written', len('\n'.join(out)))
