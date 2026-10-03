# -*- coding: utf-8 -*-
"""Second step for a project's "what is close" section (after area_places.py).
Usage: python area_spec.py --dir <private area folder> [--suggest]
- --suggest (or no area-spec.json yet): writes area-spec.suggested.json, a first choice of places from places.geojson
  (nearest named place per kind, in five groups) with plain Hebrew and English descriptions. A person reviews it, writes
  the lead paragraph (the build refuses a "TODO" lead) and saves it as area-spec.json.
- Always: asks the public OSRM router (OpenStreetMap roads, no traffic) for the driving minutes of every spec item that
  shows a drive time, and writes drive-osrm.json."""
import argparse, datetime, io, json, os, re, urllib.request

UA = {'User-Agent': 'cy-prus-area-research/1.1 (read-only, low volume)'}
FIXED = {  # far places that are not in places.geojson: (lon, lat)
    'airport_lca': ([33.6086, 34.8715], ['נמל התעופה לרנקה', 'נמל התעופה הראשי, טיסות ישירות לתל אביב'],
                    ['Larnaca Airport', 'the main airport, direct flights to Tel Aviv']),
    'airport_pfo': ([32.4880, 34.7110], ['נמל התעופה פאפוס', 'נמל התעופה במערב האי'], ['Paphos Airport', 'the airport in the west of the island']),
    'nicosia_centre': ([33.3613, 35.1706], ['מרכז ניקוסיה', 'הבירה'], ['Nicosia centre', 'the capital']),
}
DESC = {  # category -> (Hebrew, English) description
    'school': ('בית ספר', 'school'), 'kindergarten': ('גן ילדים', 'kindergarten'), 'supermarket': ('סופרמרקט', 'supermarket'),
    'pharmacy': ('בית מרקחת', 'pharmacy'), 'fuel': ('תחנת דלק', 'fuel station'), 'cafe': ('בית קפה', 'café'),
    'marketplace': ('שוק', 'market'), 'mall': ('קניון', 'shopping mall'), 'clinic': ('מרפאה', 'clinic'),
    'hospital': ('בית חולים', 'hospital'), 'playground': ('ציבורי', 'public'), 'place_of_worship': ('בית תפילה', 'place of worship'),
    'beach': ('חוף ים', 'beach'), 'marina': ('מרינה', 'marina'), 'attraction': ('אתר', 'sight'), 'gym': ('חדר כושר', 'gym'),
    'motorway_junction': ('הכביש המהיר לניקוסיה, ללרנקה ולפאפוס', 'the motorway to Nicosia, Larnaca and Paphos'),
    'bus_stop': ('התחנה הקרובה לבתים', 'the nearest stop to the homes'),
}
HE_NAMES = {  # well-known names -> Hebrew
    'Columbia Beach': 'חוף קולומביה', 'Dasoudi': 'חוף דסודי', 'Limassol Marina': 'המרינה של לימסול',
    'Limassol General Hospital': 'בית החולים הכללי של לימסול', 'Limassol Medieval Castle': 'הטירה והעיר העתיקה',
    'Germasogeia Farmers Market': 'שוק האיכרים של גרמסוגיה', 'Limassol Old Port': 'הנמל הישן של לימסול',
}
CHAINS = re.compile(r'sklavenitis|alphamega|lidl|metro|carrefour|papantoniou', re.I)
CHURCH = re.compile(r'church|ναός|ναος|agios|agia|saint|ekklisia|monast|μον', re.I)


def nearest(feats, cat, n=1, named=True, where=lambda p: True, taken=()):
    rows = [p for p in feats if p.get('category') == cat and (p.get('name') or not named) and where(p)
            and p['source_ref'] not in taken]
    return sorted(rows, key=lambda p: p['distance_m'])[:n]


def item(group, p, show=None, he=None, en=None):
    cat = p['category']
    name = p.get('name') or ''
    d_he, d_en = DESC.get(cat, (cat, cat))
    if cat == 'school' and p.get('operator_type') == 'private':
        d_he, d_en = 'בית ספר פרטי', 'private school'
    if cat == 'place_of_worship' and CHURCH.search(name + ' ' + (p.get('name_local') or '')):
        d_he, d_en = 'כנסייה', 'church'
    if cat == 'playground':
        he, en = he or 'גן שעשועים', en or 'Playground'
    if cat == 'bus_stop':
        he, en = he or 'תחנת אוטובוס', en or 'Bus stop'
    if show is None:
        show = 'walk' if p['walk_min'] <= 20 else 'drive'
    it = {'group': group, 'ref': p['source_ref'], 'he': [he or HE_NAMES.get(name, name), d_he], 'en': [en or name, d_en], 'show': show}
    if show != 'walk':
        it['drive'] = re.sub(r'\W+', '_', p['source_ref'])
    return it


def suggest(feats):
    taken, out = set(), []

    def add(group, rows, **kw):
        for p in rows:
            out.append(item(group, p, **kw))
            taken.add(p['source_ref'])
    add('schools', nearest(feats, 'school', 2, taken=taken))
    add('schools', nearest(feats, 'kindergarten', 1, taken=taken))
    add('schools', nearest(feats, 'school', 2, where=lambda p: p.get('international_or_english_hint'), taken=taken), show='drive')
    add('errands', nearest(feats, 'supermarket', 1, taken=taken), show='drive')
    add('errands', nearest(feats, 'supermarket', 1, where=lambda p: CHAINS.search((p.get('name') or '') + (p.get('brand') or '')), taken=taken), show='drive')
    for cat in ('pharmacy', 'fuel', 'cafe', 'marketplace', 'mall'):
        add('errands', nearest(feats, cat, 1, taken=taken), show='drive')
    add('health', nearest(feats, 'clinic', 1, taken=taken), show='drive')
    add('health', nearest(feats, 'hospital', 2, taken=taken), show='drive')
    add('health', nearest(feats, 'hospital', 1, where=lambda p: 'General Hospital' in (p.get('name') or ''), taken=taken), show='drive')
    add('leisure', nearest(feats, 'playground', 1, named=False, taken=taken), show='walk')
    add('leisure', nearest(feats, 'place_of_worship', 1, taken=taken))
    add('leisure', nearest(feats, 'beach', 2, taken=taken), show='drive')
    add('leisure', nearest(feats, 'marina', 1, where=lambda p: p.get('name') == 'Limassol Marina', taken=taken), show='drive')
    add('leisure', nearest(feats, 'attraction', 1, where=lambda p: 'Castle' in (p.get('name') or ''), taken=taken), show='drive')
    add('leisure', nearest(feats, 'gym', 1, taken=taken), show='drive')
    exits = []
    for p in nearest(feats, 'motorway_junction', 20, named=False):
        no = re.search(r'exit (\d+)', p.get('name') or '')
        if no and no.group(1) not in [e[0] for e in exits]:
            exits.append((no.group(1), p))
    add('roads', [p for _, p in exits[:2]], show='drive')
    add('roads', nearest(feats, 'bus_stop', 1, named=False, taken=taken), show='walk')
    for k, (_, he, en) in FIXED.items():
        out.append({'group': 'roads', 'he': he, 'en': en, 'show': 'far', 'drive': k})
    first = {g: next((i for i in out if i['group'] == g), None) for g in ('schools', 'leisure', 'errands', 'roads')}
    beach = next((i for i in out if i.get('ref') and 'beach' in i['en'][1]), None)
    junction = next((i for i in out if 'motorway' in i['en'][1]), None)
    market = next((i for i in out if i['en'][1] == 'supermarket'), None)
    marina = next((i for i in out if i['en'][0] == 'Limassol Marina'), None)
    tiles = [t for t in (
        beach and {'drive': beach['drive'], 'he': 'לחוף הים', 'en': 'to the beach'},
        junction and {'drive': junction['drive'], 'he': 'לכביש המהיר A1', 'en': 'to the A1 motorway'},
        first['schools'] and {'walk': first['schools']['ref'], 'he': 'לבית הספר הקרוב', 'en': 'to the nearest school'},
        market and {'drive': market['drive'], 'he': 'לסופרמרקט הקרוב', 'en': 'to the nearest supermarket'},
        marina and {'drive': marina['drive'], 'he': 'למרינה של לימסול', 'en': 'to Limassol Marina'},
        {'drive': 'airport_lca', 'he': 'לנמל התעופה לרנקה', 'en': 'to Larnaca Airport'}) if t]
    return {'what': 'SUGGESTED area section spec: review every place, write the lead, save as area-spec.json',
            'lead': {'he': 'TODO', 'en': 'TODO'}, 'hilly': True, 'tiles': tiles, 'places': out}


def osrm(origin, dests):
    keys = list(dests)
    coords = ';'.join(f'{c[0]:.6f},{c[1]:.6f}' for c in [origin] + [dests[k] for k in keys])
    url = f'https://router.project-osrm.org/table/v1/driving/{coords}?sources=0&annotations=duration,distance'
    r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
    if r.get('code') != 'Ok':
        raise SystemExit(f'area_spec: OSRM said {r.get("code")}')
    return {k: {'drive_min': round(r['durations'][0][i + 1] / 60, 1), 'road_km': round(r['distances'][0][i + 1] / 1000, 2),
                'lonlat': dests[k]} for i, k in enumerate(keys)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', required=True)
    ap.add_argument('--suggest', action='store_true')
    a = ap.parse_args()
    data = json.load(io.open(os.path.join(a.dir, 'places.geojson'), encoding='utf-8'))
    feats = [dict(f['properties'], _ll=f['geometry']['coordinates']) for f in data['features']]
    spec_path = os.path.join(a.dir, 'area-spec.json')
    if a.suggest or not os.path.exists(spec_path):
        spec = suggest(feats)
        path = os.path.join(a.dir, 'area-spec.suggested.json')
        io.open(path, 'w', encoding='utf-8', newline='\n').write(json.dumps(spec, ensure_ascii=False, indent=1))
        print('wrote', path, len(spec['places']), 'places')
    else:
        spec = json.load(io.open(spec_path, encoding='utf-8'))
    by_ref = {p['source_ref']: p for p in feats}
    dests = {}
    for it in spec['places'] + spec['tiles']:
        k = it.get('drive')
        if not k or k in dests:
            continue
        if k in FIXED:
            dests[k] = FIXED[k][0]
        elif 'ref' in it:
            dests[k] = by_ref[it['ref']]['_ll']
        elif 'find' in it:
            cat, text = it['find']
            rows = [p for p in feats if p['category'] == cat and text.lower() in ((p.get('name') or '') + ' ' + (p.get('name_local') or '')).lower()]
            dests[k] = min(rows, key=lambda p: p['distance_m'])['_ll']
    o = data['origin']
    rows = osrm([o['lon'], o['lat']], dests)
    io.open(os.path.join(a.dir, 'drive-osrm.json'), 'w', encoding='utf-8', newline='\n').write(json.dumps(
        {'source': 'OSRM demo server (router.project-osrm.org), OSM road network, no traffic', 'origin': 'the project point',
         'retrieved': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ'), 'rows': rows}, ensure_ascii=False, indent=1))
    print('drive rows', len(rows))


if __name__ == '__main__':
    main()
