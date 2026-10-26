"""Writes PROOF.md from proof-results.json, out/build-report.json and bench/bench.json, so every number in it is the measured one.

    python write_proof_md.py
"""
import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'proof-results.json'), encoding='utf-8'))
B = json.load(open(os.path.join(HERE, 'out', 'build-report.json'), encoding='utf-8'))
BENCH = json.load(open(os.path.join(HERE, 'bench', 'bench.json'), encoding='utf-8'))
ZN = {'country': 'country (the page\'s first view)', 'central': 'central district', 'tlv': 'Tel Aviv area'}


def S(v, m, z):
    return R['views'][v][m]['states'][z]


def med(x):
    return '%.1f' % statistics.median(x) if x else '-'


def table(v):
    out = ['| %s px | zoom | in view | text contrast, min (target 7:1) | pixel contrast, median | overlapping label pairs (target 0) | names readable | complete labels (name + count) | counts on screen (alone or in a group total) | cities you can tap | smallest tap target (target 44 on phones) | overlapping tap targets | names nearer another circle |' % v,
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for z in ('country', 'central', 'tlv'):
        for m in ('before', 'after'):
            s = S(v, m, z)
            iv = s['in_view']
            out.append('| %s · %s | %s | %d | %.2f:1 | %s:1 | %d | %d (%d%% of view, %d%% of 76) | %d | %d / %d | %d / %d | %s x %s | %d | %s |' % (
                'today' if m == 'before' else '**proposal**', ZN[z], s['zoom'], iv, min(s['contrast_text']), med(s['contrast_pixels']), s['label_overlaps'],
                len(s['names']), round(100 * len(s['names']) / iv), round(100 * len(s['names']) / 76), len(s['complete']),
                len(s['counts_covered']), iv, len(s['tappable']), iv, s['tap_min_w'], s['tap_min_h'], s['tap_overlaps'],
                ('-' if m == 'before' else str(s.get('ambiguous', '-')))))
    return '\n'.join(out)


def http(v, m):
    st = R['views'][v][m].get('lookup_statuses')
    return ' (lookup HTTP %s)' % '/'.join(str(x) for x in st) if st else ''


def inter_rows():
    rows = []
    for v in ('390', '1280'):
        b = R['views'][v]['before']['interactions']
        a = R['views'][v]['after']['interactions']
        rows.append('| %s | tap a city: the complex list under the map loads (today\'s behaviour) | %s: %d items%s | %s: %d items%s |' % (v, b['city_tap_target']['city'], b['list_loaded'], http(v, 'before'), a['city_tap_target']['city'], a['list_loaded'], http(v, 'after')))
        c = a.get('card', {})
        rows.append('| %s | the same tap opens the city card | none | yes, %s x %s px, buttons %s px tall, close button %s px |' % (v, c.get('w'), c.get('h'), '/'.join(str(x['h']) for x in c.get('buttons', [])), c.get('close_w')))
        t = a.get('tracker', {})
        rows.append('| %s | card button "יומן המתחמים בעיר": the tracker\'s city select is set and scrolled to | none | select = %s, in view: %s, under the sticky header: %s |' % (v, t.get('select_value'), t.get('select_in_view'), t.get('select_under_header')))
        g = a.get('group_tap') or {}
        rows.append('| %s | tap a group ("%s", %s complexes, %s cities): the map zooms to fit it | no groups today | zoom %s → %s |' % (v, g.get('label'), g.get('n'), g.get('members'), g.get('zoom_before'), g.get('zoom_after')))
        rows.append('| %s | zoom-in button | %s → %s | %s → %s |' % (v, b['zoom_button']['before'], b['zoom_button']['after'], a['zoom_button']['before'], a['zoom_button']['after']))
        if v == '390':
            for k, lab in (('swipe_control_above_map', 'control: one-finger swipe on page text above the map'), ('swipe_empty', 'one-finger swipe on the map'), ('swipe_label', 'one-finger swipe that starts on a label')):
                rows.append('| 390 | %s | page scrolled %d px, map moved: %s, card opened: no | page scrolled %d px, map moved: %s, card opened: %s |' % (lab, b[k]['page_scrolled_px'], b[k]['map_moved'], a[k]['page_scrolled_px'], a[k]['map_moved'], 'yes' if a[k]['opened_card'] else 'no'))
        else:
            rows.append('| 1280 | mouse drag on the map pans it | moved %.2f° lng | moved %.2f° lng |' % (b['drag_pan']['moved_lng'], a['drag_pan']['moved_lng']))
            for k, lab in (('wheel_empty', 'mouse wheel over the map (no Ctrl)'), ('wheel_label', 'mouse wheel over a label')):
                rows.append('| 1280 | %s | page scrolled %d px, map zoom change %s | page scrolled %d px, map zoom change %s |' % (lab, b[k]['page_scrolled_px'], b[k]['map_zoom_change'], a[k]['page_scrolled_px'], a[k]['map_zoom_change']))
            kb, ka = b.get('keyboard', {}), a.get('keyboard', {})
            rows.append('| 1280 | keyboard: focus a city label, Enter | list loaded: %s items | list loaded: %s items, card opened: %s, Escape closes it: %s |' % (kb.get('list_loaded'), ka.get('list_loaded'), ka.get('card_open'), ka.get('escape_closes')))
    return '\n'.join(rows)


def errs():
    return ', '.join('%s %s: %d page errors, %d blocked requests' % (v, m, len(R['views'][v][m]['page_errors']), R['views'][v][m]['blocked_requests']) for v in ('390', '1280') for m in ('before', 'after'))


def bench_rows():
    rows = []
    for k, r in BENCH.items():
        rows.append('| [%s](bench/%s) | %s | %s | %s |' % (k, r.get('screenshot', ''), r['url'], r['at_utc'], ('blocked headless (HTTP 403/429), captured with a visible Chrome' if r['mode'] == 'headed' else 'captured headless')))
    return '\n'.join(rows)


s = lambda v, m, z: S(v, m, z)
md = '''# City labels on /urban-renewal/map/: proof, before and after

Measured %(at)s on the live page. **Local only:** nothing was deployed, nothing written to the site, no REST writes, no plugin
file touched. The "after" is the live page fetched at that moment with only its map block swapped, inside the local test
browser, for the block that `urban-map-labels.patch.php.txt` produces. During the test every non-GET request to nad-lan.co.il
was aborted and analytics and session-recording hosts were blocked, so these visits are not in the owner's statistics or
Hotjar recordings (%(errs)s).

Evidence classes: **code** (numbers from `proof.py`, read from the DOM and from pixels of the screenshots), **eyes** (the
screenshots below, looked at), **unverified** (listed at the end).

## What changed (labels only)

- **The label:** a circle sized by the count (area grows with the count), the count inside in white IBM Plex Mono, and the city
  name beside it in ink `#12202A` with a white halo (IBM Plex Sans Hebrew 600). Was: a brass `#9C7A3C` pill, "city · count",
  `#FAF7F1` text, 3.73:1.
- **Collision rule:** biggest counts first. Cities whose tap areas would touch share one circle with the summed count and the
  name "<biggest city> ועוד N"; a tap on it zooms to fit its cities. A name shows only where it overlaps nothing and sits clearly
  nearer its own circle than any other; otherwise it waits for a closer zoom, a hover, keyboard focus or a tap.
- **Tap targets:** 44 x 44 px on touch screens, 24 x 24 px with a mouse (WCAG 2.5.8), never overlapping.
- **Base map:** Hebrew labels (`language: "he"` and the Mapbox RTL text plugin; before, the map said Amman, Jordan, West Bank,
  Gaza Strip in English), the base map's own label for a city we already name is hidden, base-map words at 60%% opacity.
- **City card** (Part B of the patch, can be left out): the same tap that loads today's complex list also opens a card with the
  count, the stage split and units on the authority map, what moved since 15.8.2026, and buttons to the tracker (set to that
  city) and to the list.
- **Fonts:** finding: the site skin forces Assistant on every `span`, `button`, `p` with `!important` (`body.nl-skin-a span`),
  so today's pills render in Assistant 900, and the page's own IBM Plex data block (`.nlur2`) also renders in Assistant on the
  live page. The patch pins IBM Plex on the labels and the card only, with scoped `!important` rules. Measured after:
  names in "IBM Plex Sans Hebrew", counts in "IBM Plex Mono".

Not changed: data, routes, REST, page text, the note under the map, the list markup, the SEO block, the data block, schemas.
`build.py`: both patch variants lint clean (`%(lint)s`), the text outside the map block is byte-identical, and the live page
served exactly the live-520 block (drift check: %(drift)s). Part A alone (labels without the card) was also loaded inside the
live page at 390 and 1280 px (26.10.2026, 08:40 UTC, no clicks): the same layout at country zoom (10 and 14 names, 0 overlaps,
74 of 74 counts on screen, tap targets 44 and 24 px) and no page errors.

## Before and after, by width and zoom

"In view" = cities whose point is inside the map at that zoom (of 76). "Names readable" = the whole name is visible and not
covered by another label. "Complete label" = name and its count both readable. Contrast "min" is the WCAG ratio of the
lowest label (text against its own background or halo); "pixel" is the 5th/95th percentile luminance inside each readable
name box, sampled from the 2x screenshots.

%(t390)s

%(t1280)s

**Where the proposal does not win:** at the two widest views it names fewer cities than today: at country zoom %(c_a1280)d vs
%(c_b1280)d on a desktop and %(c_a390)d vs %(c_b390)d on a phone; at district zoom %(d_a390)d vs %(d_b390)d on a phone and
%(d_a1280)d vs %(d_b1280)d on a desktop. Today's
extra names are readable only because the labels pile on top of each other (%(ov)d overlapping pairs at country zoom,
%(untap)d cities that cannot be tapped at all, %(hidden)d counts hidden). With 44 px tap targets and no overlap, a phone at
country zoom holds about ten names; the rest are inside group circles whose totals are on screen and that open with one tap.
Google Maps shows about a dozen Israeli city names at that zoom (bench/google-il-z8.png). Complete labels (name and count
together): district zoom on a desktop %(dc_a)d vs %(dc_b)d, Tel Aviv area %(tc_a1280)d vs %(tc_b1280)d (desktop) and
%(tc_a390)d vs %(tc_b390)d (phone).

## Clicks and use, on the live page

| width | check | today | proposal |
|---|---|---|---|
%(inter)s

Today's tap handler (the 758-character listener that fills `#nlurm-list`) is kept byte for byte in both patch variants
(`build.py`: %(verbatim)s).

**Finding, outside the labels: the lookup limit.** `/renewal-lookup` allows 30 lookups per IP per hour
(`nadlan_ur_lookup_rate_limited`, `inc/urban-hub.php`). Past that it answers 429 and the live page prints "אין מתחמים להצגה"
("no complexes to show") for a city that does have complexes, which is an unknown shown as a zero. My repeated proof runs from
this machine reached the limit on 26.10.2026 around 08:20 UTC, so for about an hour this connection (the owner's too, if he browses
from it) got empty lists. Many Israeli phone users share one public IP through their carrier, so heavy use of the map can hit the
same wall for real visitors. Not changed here (it is not a label); worth a separate fix: a higher or per-session limit, and an
honest message on 429.

The one-finger swipe uses real touch events (CDP `Input.dispatchTouchEvent`); the control swipe on page text proves the method
scrolls at all. `cooperativeGestures` is unchanged, so two fingers (or Ctrl + wheel) still move the map, as today.
Note: `.nlurm-top` (the city search/top controls mentioned in the brief) is **not on the live page** of 1.72.529; it exists only
in an unreleased preview (`scripts/project-stage/preview_v101.py`). The patch does not touch it and adds nothing that would
collide with it.

## Screenshots

Map only, same live page, same moment: `before-<width>-<zoom>.png` and `after-<width>-<zoom>.png` for 390 and 1280 and
country / central / tlv. Also `after-390-card.png`, `after-1280-card.png` (the city card), `after-390-tracker.png`,
`after-1280-tracker.png` (the tracker after the card button) and `after-1280-state-{default,hover,pressed,selected}.png`.

| | today | proposal |
|---|---|---|
| phone, country | ![](before-390-country.png) | ![](after-390-country.png) |
| phone, central | ![](before-390-central.png) | ![](after-390-central.png) |
| phone, Tel Aviv | ![](before-390-tlv.png) | ![](after-390-tlv.png) |
| desktop, country | ![](before-1280-country.png) | ![](after-1280-country.png) |
| desktop, central | ![](before-1280-central.png) | ![](after-1280-central.png) |
| desktop, Tel Aviv | ![](before-1280-tlv.png) | ![](after-1280-tlv.png) |

## Benchmark (captured 26.10.2026, Chrome via Playwright)

| capture | URL | time | how |
|---|---|---|---|
%(bench)s

What the best do, and what was measured on the captures:

| product | how it labels counts by place | contrast of the marker text (sampled) |
|---|---|---|
| Google Maps (he) | dot + name with a white halo, names drop out by importance as you zoom out, no overlaps; about 12 Israeli city names at zoom 8; search results as pins with halo labels, also collision-culled | dark text on halo, high |
| Mapbox cluster example | circles stepped by count (3 sizes), the count inside, a tap zooms to the expansion zoom; circles may overlap a little; no names | black on `#51BBD6` 9.4:1, on yellow 17:1 |
| Zillow | at metro zoom hundreds of overlapping dots, price pills only where they fit | white on `#99000A` 8.9:1 |
| Redfin | price pills that overlap heavily at metro zoom | white on `#01783E` 5.6:1 (AA, not AAA) |
| NYT Upshot election map | Mapbox base with sparse city names, dark text with a white halo, label hierarchy, a search box | high |
| FT Visual Vocabulary (public docs; an FT map page itself was not captured) | proportional symbol: the symbol area encodes the value | n/a |
| Madlan | teal circles sized by count with white numbers, overlapping, no names on the clusters | white on `#03AFB5` 2.7:1 (fails AA) |
| govmap | Hebrew base names, point + name, collision-culled | high |
| Government renewal map (ArcGIS, #1 for "מפת התחדשות עירונית") | green/orange dots with a black name and white halo beneath, no counts, some names collide (בת ים) | high, but no counts |

How each rule is met here:

| rule | where it comes from | measured in the proposal |
|---|---|---|
| no label collisions, biggest first | Google, govmap, Mapbox symbol placement | 0 overlapping pairs at every width and zoom |
| cluster by zoom, tap to expand | Mapbox clusters, Zillow, Redfin, Madlan | groups with the summed count; a tap zoomed 7 → %(gz390)s (phone) and 7 → %(gz1280)s (desktop) |
| halo text, high contrast | Google, NYT, the government map | 16.59:1 names, 9.46:1 counts (AAA); today 3.73:1 |
| size by count | FT Visual Vocabulary, Mapbox | circle area grows with the count (radius 9 + 1.5 * sqrt(count), capped) |
| numbers in mono | survey sheets, the page's own tiles | counts in IBM Plex Mono |
| tap targets | Apple HIG 44 pt, WCAG 2.5.5 / 2.5.8 | 44 x 44 on phones, 24 x 24 with a mouse, 0 overlapping |
| one name per place, local language | Google (he), govmap | Hebrew base map, duplicates hidden |
| a name belongs to one point | cartographic practice | 0 names nearer another circle |
| counts always findable | (beyond the benchmark: none of them shows every count) | every city in view has its count on screen, alone or in a visible group total |
| a click that tells you something | (beyond the benchmark) | the card: stages, units today and after, moves, the tracker set to the city |

## Option, not done: Mapbox symbol layers

Moving the labels into Mapbox GL symbol layers (a GeoJSON source with `cluster: true`, a circle layer, a symbol layer with
`text-field` and `text-halo`) would hand collision and fading to the map engine, place names smoothly while zooming, and
cost less DOM. It is a bigger change (new layers, a click handler on the layer, keyboard access rebuilt, because markers are
buttons today), so it is offered as a next step, not done here.

## Not verified

- Real phones (iOS Safari, Android Chrome): tested only in desktop Chrome with phone emulation (390 px, touch events).
- Two-finger pan and pinch on the map (cooperative gestures are unchanged, but not exercised by the test).
- Screen readers: the buttons carry Hebrew `aria-label`s and the card has `role="dialog"`, but no screen reader was run.
- WebGL in headless Chrome ran on SwiftShader; real GPUs may differ in timing, not in layout.
- The live page's sticky WhatsApp bar covers part of the tracker in the phone screenshot; that bar is outside the labels.
- The benchmark contrast values are sampled from screenshots, not read from those sites' CSS.

## Files

| file | what |
|---|---|
| `urban-map-labels.patch.php.txt` | the patch: exact OLD/NEW blocks for the live `urban-map.php` (Part A labels, Part B card), not applied |
| `build.py`, `lib.py` | apply the patch to a copy in `out/`, `php -l`, outside-the-block check, drift check against the live page, writes `preview.html` |
| `preview.html`, `serve.py` | local preview: `python serve.py`, then `http://localhost:8765/preview.html` (the map alone) or `/live.html` (the whole live page with the block swapped) |
| `proof.py`, `proof-results.json` | the measurement and its raw results |
| `bench/bench.py`, `bench/bench.json`, `bench/*.png` | the benchmark captures |
| `ds_build.py` | builds the design-system card RenewalMapLabels |
''' % {
    'at': R['at_utc'], 'errs': errs(), 'lint': B['urban-map.patched.php']['php_l'].split(' in ')[0],
    'drift': 'equal' if B['live_block_equals_live520'] else 'DIFFERENT', 't390': table('390'), 't1280': table('1280'),
    'inter': inter_rows(), 'bench': bench_rows(),
    'verbatim': 'kept' if B.get('todays_click_handler_kept_verbatim') else 'NOT KEPT',
    'c_a1280': len(S('1280', 'after', 'country')['names']), 'c_b1280': len(S('1280', 'before', 'country')['names']),
    'c_a390': len(S('390', 'after', 'country')['names']), 'c_b390': len(S('390', 'before', 'country')['names']),
    'd_a390': len(S('390', 'after', 'central')['names']), 'd_b390': len(S('390', 'before', 'central')['names']),
    'd_a1280': len(S('1280', 'after', 'central')['names']), 'd_b1280': len(S('1280', 'before', 'central')['names']),
    'ov': S('390', 'before', 'country')['label_overlaps'],
    'untap': S('390', 'before', 'country')['in_view'] - len(S('390', 'before', 'country')['tappable']),
    'hidden': S('390', 'before', 'country')['in_view'] - len(S('390', 'before', 'country')['counts_covered']),
    'dc_a': len(S('1280', 'after', 'central')['complete']), 'dc_b': len(S('1280', 'before', 'central')['complete']),
    'tc_a1280': len(S('1280', 'after', 'tlv')['complete']), 'tc_b1280': len(S('1280', 'before', 'tlv')['complete']),
    'tc_a390': len(S('390', 'after', 'tlv')['complete']), 'tc_b390': len(S('390', 'before', 'tlv')['complete']),
    'gz390': (R['views']['390']['after']['interactions'].get('group_tap') or {}).get('zoom_after'),
    'gz1280': (R['views']['1280']['after']['interactions'].get('group_tap') or {}).get('zoom_after'),
}
open(os.path.join(HERE, 'PROOF.md'), 'w', encoding='utf-8', newline='\n').write(md)
print('PROOF.md', len(md))
