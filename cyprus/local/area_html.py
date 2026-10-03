# -*- coding: utf-8 -*-
"""The "What is close to the homes" section of a project page, printed by the server in Hebrew and English.
Every number comes from the private area research (cyprus-private/area-20261003): places.geojson (OpenStreetMap and the
cy-prus.co.il atlas, with straight-line distance and walking minutes on the street network) and drive-osrm.json (road
driving minutes without traffic). This file holds only the choice of places and the words around them; a place that
is missing from the data stops the build, so nothing on the page is typed by hand."""
import io, json
from html import escape

# (group, data match, Hebrew name, Hebrew description, English name, English description, how to show the distance)
# match = (category, text in the OSM name) or ('osrm', key) for places outside the OSM file; show = walk | drive
PLACES = [
    ('schools', ('school', 'Agios Athanasios High School'), 'גימנסיו אגיוס אתנסיוס', 'חטיבת ביניים ציבורית',
     'Agios Athanasios Gymnasio', 'public lower-secondary school', 'walk'),
    ('schools', ('school', 'B Dimotiko Scholeio'), 'בית הספר היסודי ב׳ של אגיוס אתנסיוס', 'יסודי ציבורי',
     "Agios Athanasios B' Primary School", 'public primary school', 'walk'),
    ('schools', ('school', "Foley's School"), "Foley's School", 'בית ספר פרטי', "Foley's School", 'private school', 'walk'),
    ('schools', ('kindergarten', 'Mario Lego'), 'Mario Lego', 'גן ילדים', 'Mario Lego', 'kindergarten', 'walk'),
    ('schools', ('kindergarten', 'Regional Public and Community Nursery Agiou Athanasiou'), 'הגן הציבורי האזורי של אגיוס אתנסיוס', 'גן ציבורי',
     'Agios Athanasios regional public nursery', 'public nursery', 'walk'),
    ('schools', ('school', 'The Grammar School'), 'The Grammar School', 'בית ספר פרטי', 'The Grammar School', 'private school', 'drive'),
    ('schools', ('school', 'American Academy Private School'), 'American Academy Limassol', 'בית ספר פרטי',
     'American Academy Limassol', 'private school', 'drive'),

    ('errands', ('supermarket', 'Discount Supermarket'), 'Discount Supermarket', 'סופרמרקט', 'Discount Supermarket', 'supermarket', 'drive'),
    ('errands', ('supermarket', 'Sklavenitis'), 'Sklavenitis', 'רשת סופרמרקטים', 'Sklavenitis', 'supermarket chain', 'drive'),
    ('errands', ('pharmacy', 'Laiko Pharmacy No 4'), 'Laiko Pharmacy', 'בית מרקחת', 'Laiko Pharmacy', 'pharmacy', 'drive'),
    ('errands', ('fuel', 'Esso'), 'Esso', 'תחנת דלק', 'Esso', 'fuel station', 'drive'),
    ('errands', ('cafe', 'La Croissanterie'), 'La Croissanterie', 'בית קפה ומאפה', 'La Croissanterie', 'café and bakery', 'drive'),
    ('errands', ('marketplace', 'Germasogeia Farmers Market'), 'שוק האיכרים של גרמסוגיה', 'שוק איכרים',
     'Germasogeia Farmers Market', 'farmers market', 'drive'),
    ('errands', ('mall', 'My Mall'), 'My Mall', 'קניון', 'My Mall', 'shopping mall', 'drive'),

    ('health', ('clinic', 'Lytras'), 'Dr. Lytras', 'רופא משפחה במערכת הבריאות הציבורית (GESY)', 'Dr. Lytras', 'GP in the public health system (GESY)', 'drive'),
    ('health', ('hospital', 'German Oncology Centre'), 'German Oncology Centre', 'מרכז אונקולוגי, לא חדר מיון כללי',
     'German Oncology Centre', 'cancer centre, not a general emergency room', 'drive'),
    ('health', ('hospital', 'Mediterranean Hospital of Cyprus'), 'Mediterranean Hospital of Cyprus', 'בית חולים פרטי',
     'Mediterranean Hospital of Cyprus', 'private hospital', 'drive'),
    ('health', ('hospital', 'Limassol General Hospital'), 'בית החולים הכללי של לימסול', 'בית חולים ציבורי',
     'Limassol General Hospital', 'public hospital', 'drive'),

    ('leisure', ('playground', ''), 'גן שעשועים ופארק קטן', 'ציבורי, ברחוב הסמוך', 'Playground and small park', 'public, on the next street', 'walk'),
    ('leisure', ('place_of_worship', 'Αγίου Αθανασίου και Αγίας Μαρίνας'), 'כנסיית אגיוס אתנסיוס ואגיה מרינה', 'כנסיית השכונה',
     'Church of Agios Athanasios and Agia Marina', 'the neighbourhood church', 'walk'),
    ('leisure', ('monastery', 'μοναστήρι'), 'מנזר ספלגיוטיסה', 'אתר היסטורי', 'Sfalagiotissa Monastery', 'historic site', 'drive'),
    ('leisure', ('beach', 'Columbia Beach'), 'חוף קולומביה', 'רצועת החופים של גרמסוגיה', 'Columbia Beach', 'the Germasogeia beach strip', 'drive'),
    ('leisure', ('beach', 'Dasoudi'), 'חוף דסודי', 'חוף ציבורי', 'Dasoudi Beach', 'public beach', 'drive'),
    ('leisure', ('marina', 'Limassol Marina'), 'המרינה של לימסול', 'מרינה, מסעדות וטיילת', 'Limassol Marina', 'marina, restaurants and promenade', 'drive'),
    ('leisure', ('attraction', 'Limassol Medieval Castle'), 'הטירה והעיר העתיקה', 'מרכז לימסול ההיסטורי', 'The castle and the old town', 'historic Limassol centre', 'drive'),
    ('leisure', ('gym', 'BioFitness'), 'BioFitness', 'חדר כושר', 'BioFitness', 'gym', 'drive'),

    ('roads', ('motorway_junction', 'exit 24'), 'כביש A1, מחלף 24 (גרמסוגיה)', 'הכביש המהיר לניקוסיה, ללרנקה ולפאפוס',
     'A1, exit 24 (Germasogeia)', 'the motorway to Nicosia, Larnaca and Paphos', 'drive'),
    ('roads', ('motorway_junction', 'exit 25: Linopetra, Agios Athanasios, Industrial Zone'), 'כביש A1, מחלף 25 (אגיוס אתנסיוס)', 'המחלף הקרוב בקו אוויר',
     'A1, exit 25 (Agios Athanasios)', 'the nearest junction in a straight line', 'drive'),
    ('roads', ('bus_stop', 'Agios Athanasios Cemetery 1'), 'תחנת אוטובוס', 'התחנה הקרובה לבתים', 'Bus stop', 'the nearest stop to the homes', 'walk'),
    ('roads', ('osrm', 'airport_lca'), 'נמל התעופה לרנקה', 'נמל התעופה הראשי, טיסות ישירות לתל אביב', 'Larnaca Airport', 'the main airport, direct flights to Tel Aviv', 'far'),
    ('roads', ('osrm', 'airport_pfo'), 'נמל התעופה פאפוס', 'נמל התעופה במערב האי', 'Paphos Airport', 'the airport in the west of the island', 'far'),
    ('roads', ('osrm', 'nicosia_centre'), 'מרכז ניקוסיה', 'הבירה', 'Nicosia centre', 'the capital', 'far'),
]
# the place keys of drive-osrm.json, per data match (road minutes without traffic)
OSRM = {'Agios Athanasios High School': None, "Foley's School": 'school_foleys', 'The Grammar School': 'school_grammar',
        'American Academy Private School': 'school_american', 'Discount Supermarket': 'super_discount', 'Sklavenitis': 'super_sklavenitis',
        'Laiko Pharmacy No 4': 'pharmacy_laiko', 'Germasogeia Farmers Market': 'farmers_market', 'My Mall': 'mall_mymall',
        'Lytras': 'gp_lytras', 'German Oncology Centre': 'oncology', 'Mediterranean Hospital of Cyprus': 'hosp_mediterranean',
        'Limassol General Hospital': 'hosp_general', 'Columbia Beach': 'beach_columbia', 'Dasoudi': 'beach_dasoudi',
        'Limassol Marina': 'marina', 'Limassol Medieval Castle': 'castle', 'exit 24': 'a1_exit24',
        'exit 25: Linopetra, Agios Athanasios, Industrial Zone': 'a1_exit25'}

GROUPS = {'schools': ('בתי ספר וגנים', 'Schools and kindergartens'), 'errands': ('קניות וסידורים', 'Shopping and errands'),
          'health': ('בריאות', 'Health'), 'leisure': ('ים, פנאי ותרבות', 'Sea, leisure and culture'),
          'roads': ('כבישים, תחבורה ותעופה', 'Roads, buses and airports')}

TEXT = {
    'he': {'eyebrow': 'הסביבה', 'title': 'מה קרוב לבתים',
           'lead': 'הבתים נמצאים בחלק העליון של אגיוס אתנסיוס, ברחוב מגורים שקט בגובה של כ־120 מטר מעל פני הים. '
                   'בית ספר, גן שעשועים וכנסיית השכונה נמצאים במרחק הליכה, והסופרמרקט, חוף הים והכביש המהיר במרחק נסיעה קצרה. '
                   'לסידורים היומיומיים כאן נוסעים ברכב.',
           'm': 'מ׳', 'km': 'ק״מ', 'walk': 'דק׳ הליכה', 'drive': 'דק׳ נסיעה', 'about': 'כ־', 'road': 'בכביש',
           'keys': [('beach_columbia', 'לחוף הים בגרמסוגיה'), ('a1_exit24', 'לכביש המהיר A1'), ('walk:Agios Athanasios High School', 'לחטיבת הביניים הציבורית'),
                    ('super_discount', 'לסופרמרקט הקרוב'), ('marina', 'למרינה של לימסול'), ('airport_lca', 'לנמל התעופה לרנקה')],
           'note': 'המרחקים נמדדו בקו אוויר מהמגרש, ולמקומות הרחוקים לפי הדרך בכביש. זמני ההליכה מחושבים לפי רשת הרחובות בקצב רגיל על קרקע ישרה; '
                   'האזור גבעי, ובעלייה ההליכה ארוכה יותר. זמני הנסיעה הם לפי מסלול בכביש, בלי פקקים. '
                   'המקורות: OpenStreetMap ומפת CY-PRUS, אוקטובר 2026.'},
    'en': {'eyebrow': 'The area', 'title': 'What is close to the homes',
           'lead': 'The homes are in upper Agios Athanasios, on a quiet residential street about 120 metres above sea level. '
                   'A school, a playground and the neighbourhood church are within walking distance; the supermarket, the beach and the motorway are a short drive. '
                   'Day-to-day errands here are done by car.',
           'm': 'm', 'km': 'km', 'walk': 'min walk', 'drive': 'min drive', 'about': '~', 'road': 'by road',
           'keys': [('beach_columbia', 'to the Germasogeia beaches'), ('a1_exit24', 'to the A1 motorway'), ('walk:Agios Athanasios High School', 'to the public gymnasio'),
                    ('super_discount', 'to the nearest supermarket'), ('marina', 'to Limassol Marina'), ('airport_lca', 'to Larnaca Airport')],
           'note': 'Distances are straight lines from the plot, and by road for the far places. Walking times follow the street network at a normal pace on flat ground; '
                   'the area is hilly, so uphill walks take longer. Driving times follow the road route, without traffic. '
                   'Sources: OpenStreetMap and the CY-PRUS map, October 2026.'},
}


def _find(features, cat, text):
    rows = [f['properties'] for f in features if f['properties'].get('category') == cat
            and text.lower() in ((f['properties'].get('name') or '') + ' ' + (f['properties'].get('name_local') or '')).lower()]
    if not rows:
        raise SystemExit(f'area_html: no place for {cat!r} / {text!r} in the data')
    return min(rows, key=lambda p: p['distance_m'])


def _dist(m, t):
    if m < 1000:
        return f'{int(round(m, -1))} {t["m"]}'
    return f'{m / 1000:.1f} {t["km"]}'


def _mins(x):
    return max(1, int(round(x)))


def build(places_path, drive_path):
    feats = json.load(io.open(places_path, encoding='utf-8'))['features']
    drive = json.load(io.open(drive_path, encoding='utf-8'))['rows']
    out = {}
    for lang, t in TEXT.items():
        rtl = lang == 'he'
        resolved = []
        for group, (cat, text), he_n, he_d, en_n, en_d, show in PLACES:
            name, desc = (he_n, he_d) if rtl else (en_n, en_d)
            url = ''
            if cat == 'osrm':
                r = drive[text]
                meas = f'{_mins(r["drive_min"])} {t["drive"]} · {round(r["road_km"])} {t["km"]} {t["road"]}'
            else:
                p = _find(feats, cat, text)
                url = p.get('atlas_url') or ''
                key = OSRM.get(text)
                if show == 'walk':
                    meas = f'{_dist(p["distance_m"], t)} · {_mins(p["walk_min"])} {t["walk"]}'
                else:
                    mins = drive[key]['drive_min'] if key else p['drive_min_est']
                    meas = f'{_dist(p["distance_m"], t)} · {t["about"]}{_mins(mins)} {t["drive"]}'
            resolved.append((group, name, desc, meas, url))
        tiles = []
        for key, label in t['keys']:
            if key.startswith('walk:'):
                p = _find(feats, 'school', key[5:])
                tiles.append((_mins(p['walk_min']), t['walk'], label))
            else:
                tiles.append((_mins(drive[key]['drive_min']), t['drive'], label))
        h = [f'<section class="cyx-area" lang="{lang}" dir="{"rtl" if rtl else "ltr"}" aria-labelledby="cyx-area-h">',
             f'<p class="cyx-area-eyebrow">{escape(t["eyebrow"])}</p><h2 id="cyx-area-h">{escape(t["title"])}</h2>',
             f'<p class="cyx-area-lead">{escape(t["lead"])}</p>', '<ul class="cyx-area-keys">']
        for n, unit, label in tiles:
            h.append(f'<li><span class="cyx-area-n">{n}</span><span class="cyx-area-u">{escape(unit)}</span><span class="cyx-area-l">{escape(label)}</span></li>')
        h.append('</ul><div class="cyx-area-groups">')
        for g, (he_t, en_t) in GROUPS.items():
            rows = [r for r in resolved if r[0] == g]
            h.append(f'<details class="cyx-area-g" open><summary><h3>{escape(he_t if rtl else en_t)}</h3>'
                     f'<span class="cyx-area-c">{len(rows)}</span></summary><ul>')
            for group, name, desc, meas, url in rows:
                nm = f'<a href="{escape(url)}">{escape(name)}</a>' if url.startswith('https://cy-prus.co.il/') else escape(name)
                h.append(f'<li><span class="cyx-area-name">{nm}</span><span class="cyx-area-desc">{escape(desc)}</span>'
                         f'<span class="cyx-area-meas">{escape(meas)}</span></li>')
            h.append('</ul></details>')
        h.append(f'</div><p class="cyx-area-note">{escape(t["note"])}</p></section>')
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
