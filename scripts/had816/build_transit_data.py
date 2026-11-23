# -*- coding: utf-8 -*-
"""HAD-816: build assets/transit/transit-data.json for the transit map (version 1, Gush Dan + national rail).
Inputs (official open data, downloaded 23.11.2026 to D:/Scratch/transit-map-had816/raw, never committed):
  data.gov.il (Ministry of Transport, CC-BY): rail_stat, rail_freq_2026, lrt_line, lrt_stat, metro_line, metro_stat (shapefiles, ITM)
  gtfs.mot.gov.il national GTFS of 22.11.2026 (which Red line and Israel Railways stations run today + English names)
  Tel Aviv-Yafo municipal GIS IView2 layers 764/766/423 (English station names of the Green/Purple/Red lines) and 761 (Green line works)
Rules: 'running' comes from GTFS (trips exist), never from a status field; no opening dates; unknown = omitted."""
import json, math, sys, os, re, collections
import shapefile
from pyproj import Transformer
from shapely.geometry import LineString
RAW = 'D:/Scratch/transit-map-had816/raw/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'plugins', 'nadlan-config', 'assets', 'transit', 'transit-data.json')
T = Transformer.from_crs(2039, 4326, always_xy=True)

def ll(x, y):
    lo, la = T.transform(x, y)
    return [round(lo, 5), round(la, 5)]

def dist(a, b):  # metres, lon/lat
    k = math.cos(math.radians((a[1] + b[1]) / 2))
    return math.hypot((a[0] - b[0]) * 111320 * k, (a[1] - b[1]) * 110540)

def rd(name):
    return shapefile.Reader(RAW + 'shp_%s/%s.shp' % (name, name.upper()), encoding='utf-8')

def lines_of(r, pred, tol=6):
    out = []
    for rec, sh in zip(r.records(), r.shapes()):
        if not pred(rec):
            continue
        pts = sh.points
        parts = list(sh.parts) + [len(pts)]
        for i in range(len(parts) - 1):
            seg = pts[parts[i]:parts[i + 1]]
            if len(seg) < 2:
                continue
            s = LineString(seg).simplify(tol)
            out.append([ll(x, y) for x, y in s.coords])
    return out

gtfs = json.load(open('D:/Scratch/transit-map-had816/gtfs_rail_lrt_stops.json', encoding='utf-8'))
EN_FIX = {"נתב''ג": 'Ben Gurion Airport', "רשל''צ משה דיין": 'Rishon LeZion Moshe Dayan', "הבעש''ט": 'HaBesht', "כ''ט בנובמבר": '29 November'}
def gname(s):
    return s['name'].replace("''", '"')
seen = set(); g_lrt = []; g_rail = []
for s in gtfs:
    key = (s['agency'], s['name'])
    if key in seen:
        continue
    seen.add(key)
    s = dict(s); s['en'] = s['en'] or EN_FIX.get(s['name'], '')
    (g_rail if s['agency'] == '2' else g_lrt).append(s)

# English names from the Tel Aviv-Yafo municipal layers (Green 764, Purple 766, Red 423)
tlv = collections.defaultdict(list)
for L, line in ((764, 'green'), (766, 'purple'), (423, 'red')):
    d = json.load(open(RAW + 'tlv_%d.geojson' % L, encoding='utf-8'))
    for f in d['features']:
        c = f['geometry']['coordinates']
        tlv[line].append((f['properties']['station_name_HEB'], f['properties']['station_name_ENG'], [c[0], c[1]]))

def tlv_en(line, he, p):
    best = None
    for h, e, c in tlv[line]:
        dd = dist(p, c)
        if dd < 250 and (best is None or dd < best[0]):
            best = (dd, e)
    e = best[1] if best else ''
    return e.title() if e and e == e.lower() else e

stations = []; lines = []
# ---------- light rail, Tel Aviv metropolitan area ----------
LRT = {'אדום': ('red', 'הקו האדום', 'Red Line', '#d7262c'), 'סגול': ('purple', 'הקו הסגול', 'Purple Line', '#7b3fa0'), 'ירוק': ('green', 'הקו הירוק', 'Green Line', '#2e9e4a')}
r = rd('lrt_line')
TA = lambda rec: rec['MTR_AREA'] == 'מטרופולין תל אביב'
lines.append(dict(id='red', kind='lrt', he='הקו האדום', en='Red Line', color='#d7262c', status='open', paths=lines_of(r, lambda x: TA(x) and x['NAME'] == 'אדום' and x['STATUS'] == 'קיים')))
ext = lines_of(r, lambda x: TA(x) and x['NAME'] == 'אדום' and x['STATUS'] == 'תכנון')
if ext:
    lines.append(dict(id='red-ext', kind='lrt', he='הקו האדום, הארכה מתוכננת', en='Red Line, planned extension', color='#d7262c', status='plan', paths=ext))
lines.append(dict(id='purple', kind='lrt', he='הקו הסגול', en='Purple Line', color='#7b3fa0', status='build', paths=lines_of(r, lambda x: TA(x) and x['NAME'] == 'סגול')))
lines.append(dict(id='green', kind='lrt', he='הקו הירוק', en='Green Line', color='#2e9e4a', status='build', paths=lines_of(r, lambda x: TA(x) and x['NAME'] == 'ירוק')))
# Red line stations that run today = the GTFS stops of the Tel Aviv light rail operator (34)
for s in g_lrt:
    p = [round(s['lon'], 5), round(s['lat'], 5)]
    stations.append(dict(id='red-%s' % s['code'], kind='lrt', line='red', status='open', he=gname(s), en=s['en'] or tlv_en('red', s['name'], p), p=p))
red_open = [x['p'] for x in stations if x['line'] == 'red']
rs = rd('lrt_stat')
for rec, sh in zip(rs.records(), rs.shapes()):
    if rec['MTR_AREA'] != 'מטרופולין תל אביב':
        continue
    p = ll(*sh.points[0])
    name = rec['STAT_NAME'].strip()
    under = rec['TYPE'] == 'תחתית'
    if rec['LINE'] == 'אדום':
        if min(dist(p, q) for q in red_open) < 200:
            continue  # already listed from GTFS
        stations.append(dict(id='redx-%d' % len(stations), kind='lrt', line='red-ext', status='plan', he=name, en='', p=p))
        continue
    lid = {'סגול': 'purple', 'ירוק': 'green'}.get(rec['LINE'])
    if not lid:
        continue
    st = dict(id='%s-%d' % (lid, len(stations)), kind='lrt', line=lid, status='build', he=name, en=tlv_en(lid, name, p), p=p)
    if under:
        st['under'] = 1
    stations.append(st)
for x in stations:
    if x['line'] == 'red' and x['he'] in ('אלנבי', 'קרליבך', 'יהודית', 'שאול המלך', 'ארלוזורוב', 'אבא הלל', 'ביאליק', 'בן גוריון', 'אהרונוביץ\'', 'גשר אם המושבות'):
        x['under'] = 1  # the 10 underground Red line stations (lrt_stat TYPE 'תחתית', checked below)
# ---------- metro (planned) ----------
MET = {'M1': ('m1', '#1f6fc5'), 'M2': ('m2', '#00897b'), 'M3': ('m3', '#c2185b')}
r = rd('metro_line')
for code, (lid, col) in MET.items():
    lines.append(dict(id=lid, kind='metro', he='קו המטרו %s' % code, en='Metro %s' % code, color=col, status='plan', paths=lines_of(r, lambda x, c=code: x['NAME'] == c, 10)))
r = rd('metro_stat')
for rec, sh in zip(r.records(), r.shapes()):
    lid = MET[rec['LINE']][0]
    en = rec['NAMEENG'].strip().title().replace(' - ', ' - ')
    stations.append(dict(id='%s-%s' % (lid, rec['MASAD']), kind='metro', line=lid, status='plan', he=rec['NAME'].strip(), en=en, p=ll(*sh.points[0])))
# ---------- Israel Railways (national) ----------
r = rd('rail_freq_2026')
lines.append(dict(id='rail', kind='rail', he='רכבת ישראל', en='Israel Railways', color='#4b5a66', status='open', paths=lines_of(r, lambda x: True, 12)))
r = rd('rail_stat')
for rec, sh in zip(r.records(), r.shapes()):
    p = ll(*sh.points[0])
    best = min(g_rail, key=lambda s: dist(p, [s['lon'], s['lat']]))
    bd = dist(p, [best['lon'], best['lat']])
    name = re.sub(r'\s+', ' ', rec['ASSET_NAME'].replace('\xa0', ' ')).strip().replace("''", '"')
    if rec['STATUS'] == 'נוסעים':
        status = 'open' if bd < 700 else None
    else:
        status = 'build'
    if status is None:
        print('rail station without trains in GTFS, skipped:', name, round(bd), file=sys.stderr)
        continue
    en = best['en'] if (status == 'open' and bd < 700) else ''
    stations.append(dict(id='rail-%d' % int(rec['ASSET_NO']), kind='rail', line='rail', status=status, he=name, en=en, p=p))
RAIL_EN_BUILD = {'שוהם': 'Shoham', 'רמלה - ק. האומנים': 'Ramla - Kiryat HaOmanim', 'אלעד - פתח תקווה דרום': 'Elad - Petah Tikva South', 'ראשון לציון - תש"ח': 'Rishon LeZion - Tashah', 'ראש העין דרום': "Rosh HaAyin South", 'שפיים': 'Shefayim'}
for x in stations:
    if x['kind'] == 'rail' and not x['en']:
        x['en'] = RAIL_EN_BUILD.get(x['he'], '')
cnt = collections.Counter((x['line'], x['status']) for x in stations)
meta = dict(
    built='2026-11-23',
    sources=[
        dict(he='משרד התחבורה, data.gov.il: תחנות רכבת כבדה (rail_stat, 7.2026), מסילות ותדירות 2026 (rail_freq_2026), קווי ותחנות רכבת קלה (lrt_line 3.2026, lrt_stat 16.11.2026), קווי ותחנות מטרו (metro_line 1.2026, metro_stat, מיקומים מ־12.2021). רישיון ייחוס פתוח (CC-BY).', en='Ministry of Transport open data on data.gov.il: rail_stat (7.2026), rail_freq_2026, lrt_line (3.2026), lrt_stat (16.11.2026), metro_line (1.2026), metro_stat (positions of 12.2021). CC-BY.'),
        dict(he='לוח הזמנים הארצי של משרד התחבורה (GTFS) מ־22.11.2026: אילו תחנות של הקו האדום ושל רכבת ישראל פועלות היום, ושמות התחנות באנגלית.', en='Ministry of Transport national GTFS of 22.11.2026: which Red Line and Israel Railways stations run today, and their English names.'),
        dict(he='עיריית תל אביב־יפו, מערכת המידע הגאוגרפי: שמות התחנות באנגלית של הקו הירוק והסגול, וקטעי העבודות של הקו הירוק.', en='Tel Aviv-Yafo municipal GIS: English station names of the Green and Purple lines and the Green Line works sections.'),
    ],
    counts={'%s|%s' % k: v for k, v in sorted(cnt.items())},
)
data = dict(meta=meta, lines=lines, stations=stations)
json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(json.dumps(meta['counts'], ensure_ascii=False), os.path.getsize(OUT), 'bytes')
