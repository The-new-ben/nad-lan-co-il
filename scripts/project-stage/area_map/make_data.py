# -*- coding: utf-8 -*-
"""rova-4.json for the AreaMap component, from the research file docs/design/area-map-3d/data.json (7.10.2026).

Keeps only what the page needs (positions, card lines, links, the quarter line, the view and the page words).
The evidence for every item (Nominatim queries and OSM names, Overpass retrieval time, page reads) stays in the
research file. Drops anything sitting on the catalogue's city-centre fallback point (32.0853, 34.781806): ten
catalogue pages carry it and it is not a real position.
python make_data.py"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'docs', 'design', 'area-map-3d', 'data.json'))
OUT = os.path.join(HERE, 'rova-4.json')
FALLBACK = (32.0853, 34.781806)


def fake(lat, lng):
    return abs(lat - FALLBACK[0]) < 1e-6 and abs(lng - FALLBACK[1]) < 1e-6


def r5(x):
    return round(float(x), 6)


def main():
    d = json.load(io.open(SRC, encoding='utf-8'))
    projects = [{
        'id': p['id'], 'name': p['name'], 'fact': p['fact'], 'dev': p.get('developer'), 'url': p['url'],
        'lat': r5(p['lat']), 'lng': r5(p['lng']), 'hero': bool(p.get('hero')),
    } for p in d['projects'] if not fake(p['lat'], p['lng'])]
    renewal = [{
        'id': r['id'], 'address': r['address'], 'before': r.get('before'), 'after': r.get('after'),
        'dev': r.get('developer'), 'stage': r.get('stage'), 'note': r.get('note'), 'url': r.get('url'),
        'lat': r5(r['lat']), 'lng': r5(r['lng']),
    } for r in d['renewal'] if not fake(r['lat'], r['lng'])]
    places = [[p['cat'], p['type'], p['name'], p.get('addr'), r5(p['lat']), r5(p['lng']), p.get('edge_m')]
              for p in d['places'] if not fake(p['lat'], p['lng'])]
    ring = [[round(x, 5), round(y, 5)] for x, y in d['boundary']['geometry']['coordinates'][0]]
    v = d['view']
    out = {
        'key': 'rova-4',
        'updated': '2026-10-07',
        'page': d['page'],
        'research': 'docs/design/area-map-3d/data.json (sources and retrieval time for every item)',
        'kicker': 'המיקום',
        'title': 'רובע 4 על המפה: הפרויקטים, ההתחדשות והשכונה',
        'lead': 'בין אבן גבירול לנתיבי איילון, ובין הירקון לשדרות שאול המלך: מגדלי המגורים סביב כיכר המדינה, '
                'הבניינים שעוברים התחדשות עירונית, ובתי הספר, הפארקים, בתי הקפה והרכבת הקלה של רובע 4.',
        'caption': 'מפה להמחשה. מיקומים לפי OpenStreetMap; פרויקטי התחדשות לפי פרסומים, עודכן 7.10.2026.',
        'view': {'center': v['center'], 'zoom': v['zoom'], 'pitch': v['pitch'], 'bearing': v['bearing'],
                 'phone': v['phone']},
        'facts': {'ארלוזורוב': 'הקו האדום פועל מאז אוגוסט 2023'},  # facts.md R31, shown on the light-rail stop's card
        'boundary': ring,
        'projects': projects,
        'renewal': renewal,
        'places': places,
    }
    assert not any(fake(p['lat'], p['lng']) for p in projects + renewal)
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print('wrote', OUT, 'projects', len(projects), 'renewal', len(renewal), 'places', len(places), 'ring', len(ring))


if __name__ == '__main__':
    main()
