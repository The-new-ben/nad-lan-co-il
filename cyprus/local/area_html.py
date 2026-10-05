# -*- coding: utf-8 -*-
"""The "What is close to the homes" section of a project page, printed by the server in Hebrew and English.
Each project has a private area folder (cyprus-private/area-<date>/ or area-projects-<date>/<slug>/) with:
- places.geojson: OpenStreetMap and cy-prus.co.il atlas places with straight-line distance and walking minutes on the
  street network (made by cyprus/local/area/area_places.py);
- drive-osrm.json: road driving minutes without traffic (made by cyprus/local/area/area_spec.py);
- area-spec.json: which places the page shows, their Hebrew and English names and descriptions, the lead paragraph and
  the six key tiles. The spec holds words only: every number comes from the two data files, and a place that is
  missing from the data stops the build, so nothing on the page is typed by hand."""
import datetime, io, json
from html import escape

GROUPS = {'schools': ('בתי ספר וגנים', 'Schools and kindergartens'), 'errands': ('קניות וסידורים', 'Shopping and errands'),
          'health': ('בריאות', 'Health'), 'leisure': ('ים, פנאי ותרבות', 'Sea, leisure and culture'),
          'roads': ('כבישים, תחבורה ותעופה', 'Roads, buses and airports')}
MONTHS = {'he': ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'],
          'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']}

TEXT = {
    'he': {'eyebrow': 'הסביבה', 'title': 'מה קרוב לבתים',
           'm': 'מ׳', 'km': 'ק״מ', 'walk': 'דק׳ הליכה', 'drive': 'דק׳ נסיעה', 'about': 'כ־', 'road': 'בכביש',
           'from': 'מהמגרש', 'note': 'המרחקים נמדדו בקו אוויר {from}, ולמקומות הרחוקים לפי הדרך בכביש. זמני ההליכה מחושבים לפי רשת הרחובות בקצב רגיל על קרקע ישרה; ',
           'hilly': 'האזור גבעי, ובעלייה ההליכה ארוכה יותר. ',
           'note2': 'זמני הנסיעה הם לפי מסלול בכביש, בלי פקקים. המקורות: OpenStreetMap ומפת CY-PRUS, {month}.'},
    'en': {'eyebrow': 'The area', 'title': 'What is close to the homes',
           'm': 'm', 'km': 'km', 'walk': 'min walk', 'drive': 'min drive', 'about': '~', 'road': 'by road',
           'from': 'from the plot', 'note': 'Distances are straight lines {from}, and by road for the far places. Walking times follow the street network at a normal pace on flat ground; ',
           'hilly': 'the area is hilly, so uphill walks take longer. ',
           'note2': 'Driving times follow the road route, without traffic. Sources: OpenStreetMap and the CY-PRUS map, {month}.'},
}


def _find(features, cat, text):
    rows = [f['properties'] for f in features if f['properties'].get('category') == cat
            and text.lower() in ((f['properties'].get('name') or '') + ' ' + (f['properties'].get('name_local') or '')).lower()]
    if not rows:
        raise SystemExit(f'area_html: no place for {cat!r} / {text!r} in the data')
    return min(rows, key=lambda p: p['distance_m'])


def _find_ref(features, ref):
    for f in features:
        if f['properties'].get('source_ref') == ref:
            return f['properties']
    raise SystemExit(f'area_html: no place {ref!r} in the data')


def _place(features, item):
    return _find_ref(features, item['ref']) if 'ref' in item else _find(features, *item['find'])


def _dist(m, t):
    if m < 1000:
        return f'{int(round(m, -1))} {t["m"]}'
    return f'{m / 1000:.1f} {t["km"]}'


def _mins(x):
    return max(1, int(round(x)))


def _note(t, spec, generated):
    d = datetime.date.fromisoformat(generated)
    lang = 'he' if t is TEXT['he'] else 'en'
    month = f'{MONTHS[lang][d.month - 1]} {d.year}'
    origin = spec.get('from', {}).get(lang) or t['from']
    return t['note'].format(**{'from': origin}) + (t['hilly'] if spec.get('hilly', True) else '') + t['note2'].format(month=month)


def build(places_path, drive_path, spec_path):
    data = json.load(io.open(places_path, encoding='utf-8'))
    feats = data['features']
    drive = json.load(io.open(drive_path, encoding='utf-8'))['rows']
    spec = json.load(io.open(spec_path, encoding='utf-8'))
    if any('TODO' in spec['lead'][lang] for lang in TEXT):
        raise SystemExit(f'area_html: write the lead paragraph in {spec_path} first')
    out = {}
    for lang, t in TEXT.items():
        rtl = lang == 'he'
        resolved = []
        for item in spec['places']:
            name, desc = item[lang]
            url = ''
            if 'find' not in item and 'ref' not in item:
                r = drive[item['drive']]
                meas = f'{_mins(r["drive_min"])} {t["drive"]} · {round(r["road_km"])} {t["km"]} {t["road"]}'
            else:
                p = _place(feats, item)
                url = p.get('atlas_url') or ''
                if item['show'] == 'walk':
                    meas = f'{_dist(p["distance_m"], t)} · {_mins(p["walk_min"])} {t["walk"]}'
                else:
                    mins = drive[item['drive']]['drive_min'] if item.get('drive') else p['drive_min_est']
                    meas = f'{_dist(p["distance_m"], t)} · {t["about"]}{_mins(mins)} {t["drive"]}'
            resolved.append((item['group'], name, desc, meas, url))
        tiles = []
        for tile in spec['tiles']:
            if 'walk' in tile:
                p = _place(feats, {'find': tile['walk']} if isinstance(tile['walk'], list) else {'ref': tile['walk']})
                tiles.append((_mins(p['walk_min']), t['walk'], tile[lang]))
            else:
                tiles.append((_mins(drive[tile['drive']]['drive_min']), t['drive'], tile[lang]))
        h = [f'<section class="cyx-area" lang="{lang}" dir="{"rtl" if rtl else "ltr"}" aria-labelledby="cyx-area-h">',
             f'<p class="cyx-area-eyebrow">{escape(spec.get("eyebrow", {}).get(lang) or t["eyebrow"])}</p>'
             f'<h2 id="cyx-area-h">{escape(spec.get("title", {}).get(lang) or t["title"])}</h2>',
             f'<p class="cyx-area-lead">{escape(spec["lead"][lang])}</p>', '<ul class="cyx-area-keys">']
        for n, unit, label in tiles:
            h.append(f'<li><span class="cyx-area-n">{n}</span><span class="cyx-area-u">{escape(unit)}</span><span class="cyx-area-l">{escape(label)}</span></li>')
        h.append('</ul><div class="cyx-area-groups">')
        for g, (he_t, en_t) in GROUPS.items():
            rows = [r for r in resolved if r[0] == g]
            if not rows:
                continue
            h.append(f'<details class="cyx-area-g" open><summary><h3>{escape(he_t if rtl else en_t)}</h3>'
                     f'<span class="cyx-area-c">{len(rows)}</span></summary><ul>')
            for group, name, desc, meas, url in rows:
                nm = f'<a href="{escape(url)}">{escape(name)}</a>' if url.startswith('https://cy-prus.co.il/') else escape(name)
                h.append(f'<li><span class="cyx-area-name">{nm}</span><span class="cyx-area-desc">{escape(desc)}</span>'
                         f'<span class="cyx-area-meas">{escape(meas)}</span></li>')
            h.append('</ul></details>')
        h.append(f'</div><p class="cyx-area-note">{escape(_note(t, spec, data.get("generated", "2026-10-03")))}</p></section>')
        out[lang] = '\n'.join(h) + '\n'
    return out


AREA_CSS = (
    '.cyx-area{margin:36px 0 40px;padding:28px 24px 22px;background:var(--cy-surface,#FBF8F2);border:1px solid var(--cy-line,#E3DCCE);border-radius:8px;'
    'color:var(--cy-ink,#1B2833);font-family:var(--cy-font-body,"Assistant"),Arial,sans-serif}'
    '.cyx-area-eyebrow{margin:0;color:var(--cy-teal,#178076);font-size:13px;font-weight:700;letter-spacing:.04em}'
    'body .cyx-area h2{font-family:var(--cy-font-display,"Frank Ruhl Libre"),Georgia,serif;color:var(--cy-navy,#12293E);font-size:clamp(24px,3vw,31px);line-height:1.25;margin:4px 0 10px}'
    '.cyx-area-lead{max-width:760px;margin:0 0 22px;font-size:17px;line-height:1.75}'
    '.cyx-area-keys{list-style:none;margin:0 0 26px;padding:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px}'
    '.cyx-area-keys li{display:flex;flex-direction:column;gap:2px;padding:14px 12px;background:#fff;border:1px solid var(--cy-line,#E3DCCE);border-radius:6px}'
    '.cyx-area-n{font-family:var(--cy-font-display,"Frank Ruhl Libre"),Georgia,serif;font-size:34px;line-height:1;color:var(--cy-navy,#12293E);font-variant-numeric:tabular-nums}'
    '.cyx-area-u{font-size:13px;font-weight:700;color:var(--cy-teal,#178076)}'
    '.cyx-area-l{font-size:14px;line-height:1.4;color:var(--cy-muted,#5A6B76)}'
    '.cyx-area-groups{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px 32px}'
    'body .cyx-area h3{font-family:var(--cy-font-display,"Frank Ruhl Libre"),Georgia,serif;color:var(--cy-navy,#12293E);font-size:19px;margin:0}'
    '.cyx-area-g summary{display:flex;align-items:center;gap:10px;min-height:44px;padding:8px 0 4px;cursor:pointer;list-style:none}'
    '.cyx-area-g summary::-webkit-details-marker{display:none}'
    '.cyx-area-g summary::after{content:"";width:9px;height:9px;margin-inline-start:auto;border:solid var(--cy-teal,#178076);border-width:0 2px 2px 0;transform:rotate(45deg);transition:transform .2s}'
    '.cyx-area-g[open] summary::after{transform:rotate(-135deg)}'
    '.cyx-area-c{min-width:24px;padding:1px 7px;border-radius:12px;background:var(--cy-cream,#F4EFE6);color:var(--cy-muted,#5A6B76);font-size:13px;font-weight:700;text-align:center}'
    '.cyx-area-g summary:focus-visible{outline:2px solid var(--cy-teal,#178076);outline-offset:2px}'
    '.cyx-area-g ul{list-style:none;margin:0 0 10px;padding:0}'
    '.cyx-area-g li{display:grid;grid-template-columns:minmax(0,1fr) auto;column-gap:14px;padding:9px 0;border-bottom:1px solid var(--cy-line,#E3DCCE)}'
    '.cyx-area-name{font-weight:700;font-size:16px;line-height:1.4}'
    'body .cyx-area-name a{color:var(--cy-navy,#12293E);text-decoration:underline;text-decoration-color:var(--cy-teal-light,#2FA79A);text-underline-offset:4px}'
    'body .cyx-area-name a:hover{color:var(--cy-teal,#178076)}'
    '.cyx-area-desc{grid-column:1;font-size:14px;color:var(--cy-muted,#5A6B76);line-height:1.45}'
    '.cyx-area-meas{grid-column:2;grid-row:1/span 2;align-self:center;font-size:14.5px;white-space:nowrap;font-variant-numeric:tabular-nums;color:var(--cy-ink,#1B2833)}'
    '.cyx-area-note{margin:18px 0 0;font-size:13px;line-height:1.6;color:var(--cy-muted,#5A6B76)}'
    '@media(max-width:1100px){.cyx-area-keys{grid-template-columns:repeat(3,minmax(0,1fr))}}'
    '@media(max-width:700px){.cyx-area{padding:22px 14px 18px}.cyx-area-groups{grid-template-columns:1fr}'
    '.cyx-area-keys{grid-template-columns:repeat(2,minmax(0,1fr))}.cyx-area-n{font-size:30px}'
    '.cyx-area-g{border-bottom:1px solid var(--cy-line,#E3DCCE)}.cyx-area-g li:last-child{border-bottom:0}'
    '.cyx-area-g li{display:flex;flex-wrap:wrap;column-gap:10px;row-gap:1px;padding:9px 0}.cyx-area-name{flex-basis:100%}'
    '.cyx-area-meas{order:1;white-space:nowrap;color:var(--cy-teal,#178076);font-weight:700;font-size:14px}.cyx-area-desc{order:2}}'
)

# On phones only the first group starts open (the server prints them all open, so nothing is hidden without JavaScript).
AREA_JS = ("\n// The area list: on phones only the first group starts open.\n"
           "if(matchMedia('(max-width:700px)').matches)document.querySelectorAll('details.cyx-area-g').forEach((d,i)=>{if(i)d.open=false;});\n")
