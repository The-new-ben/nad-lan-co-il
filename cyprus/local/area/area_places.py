# -*- coding: utf-8 -*-
"""Everyday places around one project point, with distances: the data behind a project page's "what is close" section.
Usage: python area_places.py --lat 34.72086 --lon 33.063781 --out <private area folder> [--refresh]
Writes <out>/places.geojson. Raw downloads are kept in <out>/_cache (delete them, or pass --refresh, to fetch again).
Sources, all public and read-only: OpenStreetMap through the Overpass API (ODbL) and the cy-prus.co.il atlas REST API.
- distance_m: straight line from the point;
- walk_m / walk_min: shortest path on the OSM street network (motorways excluded) at 80 m a minute, flat ground;
  beyond the downloaded streets: straight line x 1.3;
- drive_min_est: 1 minute + straight line x 1.35 at 35 km/h, a rough fallback (area_spec.py adds real road minutes).
The folder is private: it holds the project's exact point."""
import argparse, datetime, heapq, json, math, os, re, time, urllib.parse, urllib.request

UA = {'User-Agent': 'cy-prus-area-research/1.1 (read-only, low volume)'}
OVERPASS = ('https://overpass-api.de/api/interpreter', 'https://overpass.kumi.systems/api/interpreter')
NEAR_M, FAR_M, ATLAS_M = 2600, 12000, 1500


def hav(a, b, c, d):
    p = math.pi / 180
    x = math.sin((c - a) * p / 2) ** 2 + math.cos(a * p) * math.cos(c * p) * math.sin((d - b) * p / 2) ** 2
    return 2 * 6371008.8 * math.asin(math.sqrt(x))


def overpass(q, path, refresh):
    if os.path.exists(path) and not refresh:
        return json.load(open(path, encoding='utf-8'))
    data = urllib.parse.urlencode({'data': q}).encode('utf-8')
    last = None
    for ep in OVERPASS:
        for _ in range(2):
            try:
                with urllib.request.urlopen(urllib.request.Request(ep, data=data, headers=UA), timeout=300) as r:
                    j = json.loads(r.read().decode('utf-8'))
                json.dump(j, open(path, 'w', encoding='utf-8'), ensure_ascii=False)
                return j
            except Exception as e:  # noqa: BLE001 (try the next mirror)
                last = e
                time.sleep(15)
    raise SystemExit(f'area_places: Overpass failed: {last}')


def atlas(bbox, path, refresh):
    if os.path.exists(path) and not refresh:
        return json.load(open(path, encoding='utf-8'))
    feats, off = [], 0
    while True:
        url = ('https://cy-prus.co.il/wp-json/cyprus-atlas/v1/places?' +
               urllib.parse.urlencode({'bbox': ','.join(f'{v:.6f}' for v in bbox), 'limit': 200, 'offset': off}))
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
            page = json.loads(r.read().decode('utf-8'))['features']
        feats += page
        if len(page) < 200:
            break
        off += 200
    j = {'type': 'FeatureCollection', 'features': feats}
    json.dump(j, open(path, 'w', encoding='utf-8'), ensure_ascii=False)
    return j


def queries(lat, lon):
    c = f'{lat},{lon}'
    bb = f'{lat - 0.035},{lon - 0.04},{lat + 0.035},{lon + 0.04}'
    roads = f'[out:json][timeout:180];(way["highway"]({bb}););out geom tags;'
    near = (f'[out:json][timeout:180];(\n'
            f' nwr(around:{NEAR_M},{c})["amenity"~"^(cafe|restaurant|fast_food|bar|pub|ice_cream|school|kindergarten|childcare|college|university|clinic|doctors|dentist|hospital|pharmacy|bank|atm|bus_station|fuel|post_office|place_of_worship|library|community_centre|police|fire_station|veterinary|marketplace|townhall|language_school|music_school|driving_school|bureau_de_change|social_facility|nursing_home|arts_centre|cinema|theatre)$"];\n'
            f' nwr(around:{NEAR_M},{c})["shop"~"^(supermarket|convenience|bakery|mall|department_store|greengrocer|butcher|pastry|deli|chemist|kiosk|seafood|beverages|wine|alcohol|confectionery|frozen_food|coffee|tea|chocolate|dairy|farm|spices|health_food|hairdresser|beauty|optician|hardware|doityourself|florist|pet|books|electronics|clothes|furniture|variety_store|garden_centre)$"];\n'
            f' nwr(around:{NEAR_M},{c})["leisure"~"^(park|playground|fitness_centre|sports_centre|stadium|pitch|dog_park|garden|track|sports_hall)$"];\n'
            f' nwr(around:{NEAR_M},{c})["office"~"^(lawyer|notary|estate_agent|accountant|architect|tax_advisor|insurance|financial|property_management|surveyor|engineer)$"];\n'
            f' nwr(around:{NEAR_M},{c})["healthcare"];\n'
            f' nwr(around:{NEAR_M},{c})["highway"="bus_stop"];\n'
            f' nwr(around:{NEAR_M},{c})["tourism"~"^(hotel|apartment|museum|attraction|viewpoint|guest_house)$"];\n'
            f' nwr(around:{NEAR_M},{c})["historic"];\n'
            f' nwr(around:{NEAR_M},{c})["landuse"~"^(retail|recreation_ground)$"]["name"];\n'
            f');out center tags;')
    far = (f'[out:json][timeout:180];(\n'
           f' node(around:9000,{c})["highway"="motorway_junction"];\n'
           f' nwr(around:10000,{c})["natural"="beach"];\n'
           f' nwr(around:10000,{c})["leisure"="beach_resort"];\n'
           f' nwr(around:10000,{c})["shop"~"^(mall|department_store)$"];\n'
           f' nwr(around:10000,{c})["amenity"~"^(school|college|university|kindergarten)$"];\n'
           f' nwr(around:10000,{c})["amenity"="hospital"];\n'
           f' nwr(around:10000,{c})["healthcare"="hospital"];\n'
           f' nwr(around:10000,{c})["leisure"~"^(marina|golf_course|water_park)$"];\n'
           f' nwr(around:10000,{c})["shop"="supermarket"]["brand"];\n'
           f' nwr(around:10000,{c})["tourism"~"^(museum|attraction|zoo|theme_park)$"]["name"];\n'
           f');out center tags;')
    return roads, near, far


NOWALK = {'motorway', 'motorway_link', 'trunk', 'trunk_link', 'proposed', 'construction', 'raceway', 'bus_guideway',
          'abandoned', 'platform', 'corridor', 'elevator'}
INTL = re.compile(r'(international|english|british|american|academy|grammar|foley|heritage|logos|pascal|russian|'
                  r'montessori|igcse|anglo|french|lyc[eé]e|deutsche|german school)', re.I)
# Limassol A1 junctions named from their exit signs (OSM node id -> name); others fall back to their OSM tags.
JUNCTIONS = {'54247925': 'A1 exit 25: Linopetra, Agios Athanasios, Industrial Zone', '54247169': 'A1 exit 25: Agios Athanasios, Linopetra',
             '21253233': 'A1 exit 26: Mesa Geitonia, Agios Athanasios', '21253230': 'A1 exit 24: Germasogeia, Limassol (E127)',
             '148988397': 'A1 exit 26: Agios Athanasios, Mesa Geitonia (F131)', '145883900': 'A1 exit 27: Agia Fylaxi, Agros, Town Centre'}
FAR_KEEP = {'motorway_junction', 'beach', 'mall', 'hospital', 'school', 'kindergarten', 'college', 'supermarket', 'marina',
            'golf_course', 'water_park', 'attraction'}


def classify(t):
    a = t.get('amenity'); s = t.get('shop'); l = t.get('leisure'); o = t.get('office'); h = t.get('highway')
    hc = t.get('healthcare'); n = t.get('natural'); tr = t.get('tourism')
    if h == 'motorway_junction': return 'motorway_junction', 'transport'
    if h == 'bus_stop' or a == 'bus_station': return 'bus_stop', 'transport'
    if n == 'beach' or l == 'beach_resort': return 'beach', 'outdoors'
    if a == 'cafe': return 'cafe', 'food'
    if a == 'restaurant': return 'restaurant', 'food'
    if a == 'fast_food': return 'fast_food', 'food'
    if a in ('bar', 'pub'): return 'bar', 'food'
    if a == 'ice_cream': return 'ice_cream', 'food'
    if s == 'supermarket': return 'supermarket', 'groceries'
    if s in ('convenience', 'kiosk'): return 'convenience', 'groceries'
    if s in ('bakery', 'pastry', 'confectionery', 'chocolate'): return 'bakery', 'groceries'
    if s in ('butcher', 'greengrocer', 'deli', 'seafood', 'beverages', 'wine', 'alcohol', 'dairy', 'farm', 'spices',
             'health_food', 'frozen_food', 'coffee', 'tea'): return 'food_shop', 'groceries'
    if a == 'school': return 'school', 'education'
    if a in ('kindergarten', 'childcare'): return 'kindergarten', 'education'
    if a in ('college', 'university', 'language_school', 'music_school', 'driving_school'): return 'college', 'education'
    if a == 'hospital' or hc == 'hospital': return 'hospital', 'health'
    if a == 'pharmacy' or hc == 'pharmacy' or s == 'chemist': return 'pharmacy', 'health'
    if a == 'dentist' or hc == 'dentist': return 'dentist', 'health'
    if a in ('clinic', 'doctors') or hc: return 'clinic', 'health'
    if a == 'veterinary': return 'veterinary', 'services'
    if l in ('park', 'garden'): return 'park', 'outdoors'
    if l == 'playground': return 'playground', 'outdoors'
    if l == 'dog_park': return 'dog_park', 'outdoors'
    if l == 'fitness_centre': return 'gym', 'sport'
    if l in ('sports_centre', 'stadium', 'sports_hall', 'track'): return 'sports_centre', 'sport'
    if l == 'pitch': return 'pitch', 'sport'
    if s in ('mall', 'department_store'): return 'mall', 'shopping'
    if a == 'bank': return 'bank', 'services'
    if a == 'atm': return 'atm', 'services'
    if a in ('post_office', 'bureau_de_change'): return a, 'services'
    if o == 'estate_agent': return 'estate_agent', 'professionals'
    if o in ('lawyer', 'notary'): return o, 'professionals'
    if o: return 'office_' + o, 'professionals'
    if a == 'place_of_worship': return 'place_of_worship', 'community'
    if a in ('library', 'community_centre', 'townhall', 'police', 'fire_station', 'social_facility', 'nursing_home',
             'arts_centre', 'cinema', 'theatre', 'marketplace'): return a, 'community'
    if a == 'fuel': return 'fuel', 'services'
    if tr in ('hotel', 'apartment', 'guest_house'): return 'hotel', 'tourism'
    if tr in ('museum', 'attraction', 'viewpoint', 'zoo', 'theme_park') or t.get('historic'): return 'attraction', 'culture'
    if l in ('marina', 'golf_course', 'water_park'): return l, 'outdoors'
    if t.get('landuse') == 'retail': return 'retail_area', 'shopping'
    if t.get('landuse') == 'recreation_ground': return 'recreation_ground', 'outdoors'
    if s: return 'shop', 'shopping'
    return 'other', 'other'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lat', type=float, required=True)
    ap.add_argument('--lon', type=float, required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--refresh', action='store_true')
    a = ap.parse_args()
    C = (a.lat, a.lon)
    cache = os.path.join(a.out, '_cache')
    os.makedirs(cache, exist_ok=True)
    q_roads, q_near, q_far = queries(*C)
    roads = overpass(q_roads, os.path.join(cache, 'roads.json'), a.refresh)
    near = overpass(q_near, os.path.join(cache, 'near.json'), a.refresh)
    far = overpass(q_far, os.path.join(cache, 'far.json'), a.refresh)
    dlat, dlon = ATLAS_M / 111000, ATLAS_M / (111000 * math.cos(math.radians(C[0])))
    at = atlas((C[1] - dlon, C[0] - dlat, C[1] + dlon, C[0] + dlat), os.path.join(cache, 'atlas.json'), a.refresh)

    # ---------- the walking graph ----------
    def key(p):
        return (round(p['lat'], 7), round(p['lon'], 7))
    G = {}
    for e in roads['elements']:
        t = e.get('tags', {})
        if 'highway' not in t or t['highway'] in NOWALK or t.get('access') in ('private', 'no') or t.get('foot') == 'no':
            continue
        g = e['geometry']
        for i in range(len(g) - 1):
            p, q = key(g[i]), key(g[i + 1])
            w = hav(p[0], p[1], q[0], q[1])
            G.setdefault(p, []).append((q, w))
            G.setdefault(q, []).append((p, w))
    cell = 0.002
    idx = {}
    for n in G:
        idx.setdefault((int(n[0] / cell), int(n[1] / cell)), []).append(n)

    def snap(lat, lon, maxd=250):
        best = None
        ci, cj = int(lat / cell), int(lon / cell)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for n in idx.get((ci + di, cj + dj), []):
                    d = hav(lat, lon, n[0], n[1])
                    if best is None or d < best[0]:
                        best = (d, n)
        return best if best and best[0] <= maxd else None
    s0 = snap(*C)
    if not s0:
        raise SystemExit('area_places: no street within 250 m of the point')
    dist = {s0[1]: 0.0}
    pq = [(0.0, s0[1])]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, 1e18):
            continue
        if d > 6000:
            break
        for v, w in G[u]:
            nd = d + w
            if nd < dist.get(v, 1e18):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    def walk(lat, lon, straight):
        s = snap(lat, lon)
        if s and s[1] in dist:
            return round(dist[s[1]] + s[0] + s0[0]), 'osm_network'
        return round(straight * 1.3), 'straight_x1.3'

    def drive_est(straight):
        return max(1, round(1 + straight * 1.35 / (35000 / 60)))

    # ---------- OSM places ----------
    feats = {}

    def add(src, maxd, keep=lambda c: True):
        ts = src.get('osm3s', {}).get('timestamp_osm_base')
        for e in src['elements']:
            t = e.get('tags', {})
            if 'lat' in e:
                la, lo = e['lat'], e['lon']
            elif 'center' in e:
                la, lo = e['center']['lat'], e['center']['lon']
            else:
                continue
            st = hav(C[0], C[1], la, lo)
            cat, grp = classify(t)
            if st > maxd or cat == 'other' or not keep(cat):
                continue
            if cat in ('pitch', 'park', 'playground', 'sports_centre') and t.get('access') in ('private', 'no'):
                continue
            fid = f"osm:{e['type']}/{e['id']}"
            if fid in feats:
                continue
            name = t.get('name:en') or t.get('name') or None
            props = dict(name=name, name_local=t.get('name') if t.get('name') and t.get('name') != name else None,
                         category=cat, group=grp, source='OpenStreetMap via Overpass API', source_ref=fid, osm_timestamp=ts,
                         licence='ODbL-1.0, (c) OpenStreetMap contributors', distance_m=round(st))
            wm, basis = walk(la, lo, st)
            props.update(walk_m=wm, walk_basis=basis, walk_min=round(wm / 80), drive_min_est=drive_est(st))
            if cat in ('school', 'kindergarten', 'college'):
                props['international_or_english_hint'] = bool(INTL.search(' '.join(
                    [t.get('name', ''), t.get('name:en', ''), t.get('operator', '')])))
            if cat == 'motorway_junction':
                props['name'] = JUNCTIONS.get(str(e['id'])) or ' '.join(
                    x for x in ('A1 exit ' + t['ref'] if t.get('ref') else 'A1 junction', t.get('name') or t.get('exit_to') or '') if x)
            for kk in ('ref', 'operator', 'operator:type', 'brand', 'website'):
                if kk in t:
                    props[kk.replace(':', '_')] = t[kk]
            feats[fid] = {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [round(lo, 6), round(la, 6)]},
                          'properties': props}
    add(near, NEAR_M)
    add(far, FAR_M, lambda c: c in FAR_KEEP)

    # ---------- atlas places (merged into the OSM place when it is the same one) ----------
    def norm(s):
        return re.sub(r'\W+', '', (s or '').lower())
    osm = list(feats.values())
    for f in at['features']:
        p = f['properties']
        lo, la = f['geometry']['coordinates']
        st = hav(C[0], C[1], la, lo)
        if st > ATLAS_M:
            continue
        match = None
        if p['kind'] != 'street':
            for o in osm:
                ol, oa = o['geometry']['coordinates']
                if hav(la, lo, oa, ol) < 40 and (norm(p['name']) in (norm(o['properties']['name']), norm(o['properties'].get('name_local')))
                                                  or p.get('subtype') == o['properties']['category']):
                    match = o
                    break
        if match:
            match['properties'].update(atlas_id=p['id'], atlas_url=p['url'])
            continue
        if p['kind'] in ('project',):
            continue
        wm, basis = walk(la, lo, st)
        cat = 'street' if p['kind'] == 'street' else (p.get('subtype') or p['kind'])
        feats['atlas:' + str(p['id'])] = {
            'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [round(lo, 6), round(la, 6)]},
            'properties': dict(name=p['name'], category=cat, group='street' if p['kind'] == 'street' else p['kind'],
                               atlas_kind=p['kind'], atlas_subtype=p.get('subtype'), source='cy-prus.co.il atlas REST',
                               source_ref='atlas:' + str(p['id']), atlas_id=p['id'], atlas_url=p['url'], licence=p.get('licence'),
                               distance_m=round(st), walk_m=wm, walk_basis=basis, walk_min=round(wm / 80), drive_min_est=drive_est(st))}

    fc = {'type': 'FeatureCollection', 'name': os.path.basename(os.path.normpath(a.out)),
          'origin': {'lat': C[0], 'lon': C[1], 'what': 'the project point; INTERNAL'},
          'generated': datetime.date.today().isoformat(),
          'notes': ['distance_m = straight line from the point', 'walk_min = OSM street network at 80 m/min, flat ground',
                    'drive_min_est = 1 + straight x 1.35 at 35 km/h (fallback only)',
                    f'OSM everyday places within {NEAR_M} m, far categories within {FAR_M} m; atlas places within {ATLAS_M} m',
                    'OSM base timestamp (roads): ' + str(roads.get('osm3s', {}).get('timestamp_osm_base'))],
          'features': sorted(feats.values(), key=lambda f: f['properties']['distance_m'])}
    json.dump(fc, open(os.path.join(a.out, 'places.geojson'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    from collections import Counter
    print('places', len(fc['features']), 'snap m', round(s0[0]), dict(Counter(f['properties']['group'] for f in fc['features'])))


if __name__ == '__main__':
    main()
