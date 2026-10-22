# -*- coding: utf-8 -*-
"""Build prices.json (+ helper tables for prices.md) for the Greece price list.
Run:  python -I -X utf8 build_prices.py
Inputs (all under this folder): raw/indomio/*.txt, raw/neighbourhoods/browser_capture_*.txt,
raw/regions/spi_q2_2026_deiktis-timon.txt, raw/xe_q3_2026.json, raw/agent_*.json,
../2026-10-22-greece/facts.json. No network access.
"""
import json, re, os, math

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw')
RETR = '2026-10-22'

# ----------------------------------------------------------------- sources
S = {
 'indomio': dict(provider='Indomio.gr', kind='asking', period='2026-09',
                 source_date='undated live page; reference month September 2026, yoy vs September 2025',
                 url='https://www.indomio.gr/en/agora-akiniton/'),
 'spit_q3': dict(provider='Spitogatos', kind='asking', period='2026-Q3', source_date='2026-10-22',
                 url='https://www.newmoney.gr/roh/palmos-oikonomias/oikonomia/spitogatos-pou-afxithikan-eos-305-ta-enikia-to-g-trimino-i-perioches-me-tis-megaliteres-anatimisis-pinakes/'),
 'spi_q2': dict(provider='Spitogatos SPI', kind='asking', period='2026-Q2',
                source_date='undated live page (still showing Q2 2026 on 2026-10-22)', url='https://www.spitogatos.gr/deiktis-timon'),
 'spit_q2_blog': dict(provider='Spitogatos', kind='asking', period='2026-Q2', source_date='2026-08-04',
                      url='https://www.spitogatos.gr/blog/pwliseis-enoikiaseis-katoikion-ellada-2o-trimino-2026'),
 'spit_isl': dict(provider='Spitogatos (islands report)', kind='asking', period='2026-Q2', source_date='2026-09-16',
                  url='https://www.spitogatos.gr/blog/ellinika-nisia-2o-trimino-2026-mzt-polisis-katoikion'),
 'spit_hol': dict(provider='Spitogatos (holiday homes report)', kind='asking, holiday homes', period='2026-Q2', source_date='2026-09-24',
                  url='https://www.spitogatos.gr/blog/times-exoxikon-katoikion-ellada-2o-trimino-2026'),
 'spit_ng': dict(provider='Spitogatos (North Greece report)', kind='asking', period='2026-Q1', source_date='2026-07-03',
                 url='https://www.spitogatos.gr/blog/agora-enoikiasi-katoikias-voreia-ellada-q1-2026-mzt-2022-2026'),
 'spit_thes': dict(provider='Spitogatos (Thessaly report)', kind='asking', period='2025-Q3', source_date='2025-11-28',
                   url='https://www.spitogatos.gr/blog/agora-akiniton-thessalia-aap-zitisi'),
 'spit_epir': dict(provider='Spitogatos (Epirus report)', kind='asking', period='2025-Q3', source_date='2025-12-31',
                   url='https://www.spitogatos.gr/blog/agora-katoikion-gis-ipeiro'),
 'spit_student': dict(provider='Spitogatos (student housing)', kind='asking, student-type small units only', period='2026-Q2',
                      source_date='2026-09-01', url='https://www.spitogatos.gr/blog/enoikia-foititika-spitia-2026-athina-thessaloniki-ypoloipi-ellada'),
 'xe': dict(provider='xe.gr (Chrysi Efkairia)', kind='asking; listing-weighted mean of 3 size bands computed by us', period='2026-Q3',
            source_date='undated live page (Q3 2026 vs Q3 2025)', url='https://www.xe.gr/property/times-akiniton'),
 'remax_rent': dict(provider='RE/MAX Greece', kind='closed lettings (not asking)', period='2026', source_date='2026-09-03',
                    url='https://www.protothema.gr/greece/article/1873382/o-hartis-enoikion-se-poies-periohes-ektoxeutikan-oi-times-oi-protathlites-se-athina-thessaloniki-kai-nisia/'),
 'remax_sale_ath': dict(provider='RE/MAX Greece', kind='completed sales (not asking)', period='2025', source_date='2026-05-15',
                        url='https://www.naftemporiki.gr/finance/economy/2110674/akinita-sto-37-i-mesi-ayxisi-ton-timon-polisis-to-2025-oi-akrivoteres-perioches-kai-ekeines-me-ti-megalyteri-anodo/'),
 'remax_sale_thes': dict(provider='RE/MAX Greece', kind='completed sales (not asking)', period='2025', source_date='2026-05-15',
                         url='https://www.typosthes.gr/oikonomia/429076_thessaloniki-oi-times-gia-spitia-ana-periohi-poy-kanei-pano-apo-6000-eyro-tm'),
 'numbeo': dict(provider='Numbeo (crowd-sourced)', kind='crowd-sourced estimate', period='rolling 12 months to 2026-10-22',
                source_date='2026-10-22', url='https://www.numbeo.com/cost-of-living/in/'),
 'ev': dict(provider='Engel & Völkers Market Report Greece 2026', kind='broker price range', period='2026', source_date='2026-05-15',
            url='https://www.newmoney.gr/roh/palmos-oikonomias/oikonomia/engel-volkers-se-dio-tachitites-i-agora-akiniton-stin-attiki-pou-i-times-bori-na-xeperasoun-ta-e20-000-t-m/'),
}

def src(key, **kw):
    d = dict(S[key]); d.update(kw); d['retrieved'] = RETR; return d

def num(s):
    s = s.strip()
    if s in ('-', ''): return None
    return float(s.replace(',', ''))

def pct(s):
    s = (s or '').strip().replace('%', '')
    if s in ('', '-'): return None
    return round(float(s) / 100, 4)

# ----------------------------------------------------------------- Indomio
IND = {}  # (path, name) -> dict

def ind_put(path, name, sale, syoy, rent, ryoy):
    IND[(path, name.strip())] = dict(sale=sale, sale_yoy=syoy, rent=rent, rent_yoy=ryoy,
                                     url='https://www.indomio.gr/en/agora-akiniton/' + path)

cap = open(os.path.join(RAW, 'indomio', 'indomio_capture_2026-10-22.txt'), encoding='utf-8').read()
for line in cap.splitlines():
    if line.startswith('Regions:'):
        for part in line[len('Regions:'):].split('|'):
            m = re.match(r'\s*(.+?) ([\d,]+)\(([+\-][\d.]+)\) ([\d.]+)\(([+\-][\d.]+)\)', part)
            if m:
                ind_put('', m.group(1), num(m.group(2)), pct(m.group(3)), num(m.group(4)), pct(m.group(5)))
    if line.startswith('{"u"'):
        d = json.loads(line)
        rows = d.get('rows') or d.get('rows (selected)') or []
        for r in rows:
            f = r.split('|')
            ind_put(d['u'], f[0], num(f[1]), pct(f[2]), num(f[3]), pct(f[4]) if len(f) > 4 else None)
        if d.get('top'):
            t = d['top']
            ind_put(d['u'], '__top__', num(t[0]), pct(t[1]), num(t[2]), pct(t[3]))
IND[('', 'Greece')] = dict(sale=2790.0, sale_yoy=0.0473, rent=10.68, rent_yoy=0.0379, url='https://www.indomio.gr/en/agora-akiniton/')

cap2 = open(os.path.join(RAW, 'neighbourhoods', 'browser_capture_indomio_spitogatos_2026-10-22.txt'), encoding='utf-8').read()
cur = None
for line in cap2.splitlines():
    m = re.match(r'https://www\.indomio\.gr/en/agora-akiniton/(\S*)', line)
    if m:
        cur = m.group(1); continue
    if line.startswith('SPITOGATOS'):
        cur = None
    if cur is None or not line.strip():
        continue
    for part in re.split(r'\|\||;', line):
        m = re.match(r'\s*(.+?) ([\d,]+)\(([+\-][\d.]+)%\) ([\d.]+)(?:\(([+\-][\d.]+)%\))?\s*$', part)
        if m:
            ind_put(cur, m.group(1), num(m.group(2)), pct(m.group(3)), num(m.group(4)), pct(m.group(5)))
# Athens "Kentro" zones (no yoy published in capture)
for z, s_, r_ in [('Akadimia', 5177, 19.51), ('Omonoia', 2698, 12.5), ('Psirri', 3859, 17.69), ('Sintagma', 6067, 17.67)]:
    ind_put('attiki/kentro/', z, float(s_), None, r_, None)

def ind(path, name):
    return IND.get((path, name))

# ----------------------------------------------------------------- Spitogatos SPI Q2 2026
SPI = {}
spitxt = open(os.path.join(RAW, 'regions', 'spi_q2_2026_deiktis-timon.txt'), encoding='utf-8').read()
sale_part = spitxt.split('SALE (EUR/m2):')[1].split('RENT (EUR/m2/month):')[0]
rent_part = spitxt.split('RENT (EUR/m2/month):')[1]
ALIAS = {'Athens Centre': 'Athens Centre', 'Athens North': 'Athens North', 'Athens South': 'Athens South',
         'Athens West': 'Athens West', 'Athens East': 'Athens East', 'Thess. municipality': 'Thessaloniki Municipality',
         'Thess. peripheral munis': 'Thessaloniki Suburbs', 'Θεσσαλονίκη - Υπόλ. Νομού': 'Thessaloniki Rest',
         'Αθήνα - Δυτικά Προάστια': 'Athens West', 'Ανατολικά': 'Athens East', 'Πειραιάς': 'Piraeus',
         'Προάστια Πειραιά': 'Piraeus suburbs', 'Υπόλοιπο Αττικής': 'Rest of Attica', 'Θεσσαλονίκη - Δήμος': 'Thessaloniki Municipality',
         'Περιφ/κοί δήμοι': 'Thessaloniki Suburbs', 'Υπόλ. Νομού': 'Thessaloniki Rest', 'Rest of Attica': 'Rest of Attica',
         'Piraeus suburbs': 'Piraeus suburbs', 'Piraeus': 'Piraeus'}
def spi_parse(part, metric):
    for chunk in re.split(r'[~|\n]', part):
        m = re.match(r'\s*(.+?) ([\d.]+) ([\d.]+) (-?[\d.]+)%?\s*$', chunk.strip().split(' (no rent')[0])
        if not m: continue
        nm = ALIAS.get(m.group(1).strip(), m.group(1).strip())
        SPI.setdefault(nm, {})[metric] = dict(prev=float(m.group(2)), value=float(m.group(3)), yoy=round(float(m.group(4)) / 100, 4))
spi_parse(sale_part, 'sale'); spi_parse(rent_part, 'rent')
# Q2 2026 Spitogatos blog text: rent for Athens Centre / North / South (SPI rows not captured)
for k, v in [('Athens Centre', 12.0), ('Athens North', 11.8), ('Athens South', 13.3)]:
    SPI.setdefault(k, {})['rent_blog'] = dict(value=v, yoy=None)

# ----------------------------------------------------------------- xe.gr Q3 2026 (computed weighted means)
XE = {}
xe = json.load(open(os.path.join(RAW, 'xe_q3_2026.json'), encoding='utf-8'))
for metric in ('sale', 'rent'):
    for area, rec in xe[metric].items():
        L, P = rec['listings'], rec['price']
        try:
            n25 = sum(L[b][0] for b in P); n26 = sum(L[b][1] for b in P)
            v25 = sum(P[b][0] * L[b][0] for b in P) / n25
            v26 = sum(P[b][1] * L[b][1] for b in P) / n26
        except Exception:
            continue
        XE.setdefault(area, {})[metric] = dict(value=round(v26, 2 if metric == 'rent' else 0), prev=round(v25, 2 if metric == 'rent' else 0),
                                               yoy=round(v26 / v25 - 1, 4), listings=int(n26),
                                               bands={b: P[b][1] for b in P})

# ----------------------------------------------------------------- Spitogatos Q3 2026 / Q2 2026 lists (press tables, notes-1.md)
SQ3 = {  # name: (sale, sale_yoy, rent, rent_yoy)
 'Athens South': (4257, None, 13.5, None), 'Cyclades': (4091, None, 12.2, None), 'Athens North': (3505, None, 12.0, None),
 'Lefkada RU': (3500, None, None, None), 'Chania RU': (3125, None, None, None), 'Athens Centre': (None, None, 12.2, None),
 'Piraeus': (None, None, 11.0, None), 'Kastoria': (577, None, None, None), 'Kozani': (667, None, None, None),
 'Florina': (690, None, None, None), 'Kilkis': (700, None, 4.8, None), 'Karditsa': (806, None, None, None),
 'Pella': (None, None, 5.0, None), 'Imathia': (None, None, 5.1, None), 'Grevena': (None, None, 5.1, None),
 'Thessaloniki Rest': (None, None, 5.6, None),
 'Vouliagmeni': (7442, None, 22.4, None), 'Voula': (6389, None, 17.5, None), 'Elliniko': (5849, None, None, None),
 'Glyfada': (5758, None, 17.1, None), 'Palaio Psychiko': (5603, None, 18.0, None), 'Kolonaki': (None, None, 18.0, None),
 'Varnavas': (1448, None, None, None), 'Agia Varvara': (1500, None, None, None), 'Acharnes': (1680, None, 8.3, None),
 'Perama': (1731, None, 7.9, None), 'Patisia': (1739, None, None, None), 'Kamatero': (None, None, 7.7, None),
 'Nea Filadelfeia': (2193, 0.234, None, None), 'Drosia': (3077, 0.229, None, None), 'Nea Penteli': (2574, 0.213, None, None),
 'Dafni': (3571, 0.196, None, None), 'Nea Ionia': (3012, 0.167, None, None),
 'Kaisariani': (None, None, 14.7, 0.257), 'Neo Psychiko': (None, None, 14.6, 0.218), 'Kentro Athinas': (None, None, 15.9, 0.191),
 'Neo Faliro': (None, None, 12.0, 0.182), 'Artemida': (None, None, 10.2, 0.169),
 'Kalamaria': (3243, None, None, None), 'Thessaloniki Centre': (3075, None, 12.0, None), 'Charilaou': (3000, None, None, None),
 'Pylaia': (2962, None, None, None), 'Toumba': (2870, None, None, None), 'Vardaris': (None, None, 12.5, 0.204),
 '40 Ekklisies': (None, None, 11.4, None), 'Ano Poli': (None, None, 10.7, None), 'Xirokrini': (None, 0.266, 10.7, None),
 'Mygdonia': (938, None, None, None), 'Kallithea Thess': (1000, None, None, None), 'Chortiatis': (1369, None, 5.4, None),
 'Oraiokastro': (None, 0.272, 5.6, None), 'Epanomi': (None, None, None, 0.305), 'Menemeni': (None, None, None, 0.226),
 'Pefka': (None, None, 5.6, None), 'Mikra': (None, None, 5.6, None),
}
SQ2 = {  # Spitogatos Q2 2026 blog (2026-08-04) Attica / Thessaloniki tables
 'Vouliagmeni': (7364, None, 22.0), 'Voula': (6250, None, 17.4), 'Elliniko': (5688, None, None), 'Glyfada': (5669, None, 16.5),
 'Palaio Psychiko': (5182, None, 17.4), 'Kolonaki': (None, None, 17.9), 'Drosia': (3094, 0.302, None), 'Dafni': (3500, 0.270, None),
 'Lykovrysi': (3918, 0.256, None), 'Tavros': (2800, 0.225, None), 'Nea Filadelfeia': (2128, 0.223, None),
 'Kalamaria': (3175, None, None), 'Thessaloniki Centre': (3056, None, 12.0), 'Pylaia': (2962, None, None), 'Charilaou': (2857, None, None),
 'Toumba': (2850, None, None), 'Vardaris': (None, None, 12.0), '40 Ekklisies': (None, None, 11.9), 'Xirokrini': (None, None, 10.8),
}
ISL = {  # Spitogatos islands Q2 2026 (sale EUR/m2)
 'Antiparos': 7600, 'Mykonos': 7059, 'Paros': 5263, 'Folegandros': 4746, 'Kythnos': 4583, 'Ios': 4167, 'Serifos': 4154,
 'Santorini': 4096, 'Sifnos': 3846, 'Naxos': 3846, 'Milos': 3695, 'Kea': 3333, 'Tinos': 3004, 'Sikinos': 2563, 'Syros': 2363,
 'Amorgos': 2143, 'Andros': 2051, 'Paxoi': 3846, 'Lefkada': 3302, 'Kefalonia': 2531, 'Ithaca': 2455, 'Corfu': 2417,
 'Zakynthos': 2300, 'Kythira': 2188, 'Skiathos': 3521, 'Alonnisos': 2667, 'Skyros': 2402, 'Skopelos': 2154,
 'Chania RU': 3102, 'Rethymno RU': 2202, 'Heraklion RU': 2200, 'Lasithi RU': 1944, 'Ikaria': 1846, 'Chios': 1533,
 'Lesvos': 1136, 'Samos': 1059, 'Patmos': 5000, 'Astypalaia': 4000, 'Kalymnos': 2759, 'Leros': 2422, 'Symi': 2157,
 'Kos': 2125, 'Rhodes': 2105, 'Aegean islands': 2941, 'Ionian islands': 2531, 'Crete': 2250,
}
HOL = {  # Spitogatos holiday homes Q2 2026 (sale EUR/m2, yoy from the table)
 'Kalamos (Attica)': (1615, 0.004), 'Artemida': (1862, -0.007), 'Keratea': (1875, -0.013), 'Marathon': (2013, -0.031),
 'Nea Makri': (2276, 0.051), 'Rafina': (2500, 0.021), 'Palaia Fokaia': (2556, 0.078), 'Porto Rafti': (2667, 0.151),
 'Anavyssos': (2941, -0.029), 'Saronida': (3200, -0.052), 'Eretria': (1635, 0.010), 'Aegina': (2692, 0.021), 'Poros': (3207, 0.078),
 'Spetses': (4615, 0.151), 'Nafplio': (2778, 0.111), 'Akrata': (1538, 0.017), 'Zacharo': (1200, -0.022), 'Loutraki': (2619, 0.200),
 'Xylokastro': (1700, 0.030), 'East Mani': (2727, 0.106), 'Oitylo': (1781, 0.079), 'Kalamata': (2892, 0.013), 'Koroni': (2250, 0.0),
 'Kyparissia': (1750, 0.029), 'Leuktro': (2292, -0.066), 'Methoni': (2273, -0.020), 'Galaxidi': (2394, -0.128),
 'Kallikrateia': (2513, 0.047), 'Kassandra': (2895, 0.045), 'Sithonia': (3000, 0.071), 'Nafpaktos': (1867, 0.173),
 'Syvota': (2795, 0.153), 'Kavala': (2286, 0.128), 'Agria': (1387, 0.028), 'Zagora': (1171, -0.024), 'Milies': (1644, 0.151),
 'Mouresi': (2134, 0.024),
}
NG = {  # Spitogatos North Greece Q1 2026 city values (sale, rent)
 'Alexandroupoli': (2000, 9.0), 'Kavala': (1993, 7.3), 'Komotini': (1300, 7.6), 'Xanthi': (1282, 7.3), 'Katerini': (1108, 6.2),
 'Serres': (1047, 6.6), 'Veria': (1000, 5.0), 'Drama': (1000, 5.8), 'Kozani': (838, 5.9),
}
STUDENT = {'Patras': (10.0, 0.0), 'Heraklion': (12.0, 0.12), 'Larissa': (10.0, 0.057), 'Volos': (10.0, 0.0), 'Ioannina': (10.0, 0.03),
           'Chania': (12.9, 0.047), 'Kalamata': (11.2, 0.071), 'Rhodes': (13.3, 0.166), 'Chalkida': (10.7, 0.071), 'Lamia': (6.8, 0.055)}
REMAX_RENT = {'Kolonaki': (14.0, 0.0), 'Koukaki': (9.7, None), 'Exarcheia': (9.8, None), 'Kypseli': (8.0, 0.143), 'Petralona': (10.4, 0.156),
              'Neos Kosmos': (10.6, 0.082), 'Vari-Varkiza': (13.0, 0.083), 'Panorama': (8.5, None), 'Thermi': (8.0, 0.143),
              'Peraia': (6.8, None), 'East Thessaloniki': (7.5, 0.042), 'West Thessaloniki': (6.1, 0.052)}
NUMBEO = {  # city: (centre sale, outside sale, 1-bed centre rent, yield centre, yield outside)
 'Athens': (3615.98, 2969.00, 661.18, 0.0394, 0.0418), 'Thessaloniki': (3302.71, 2522.35, 560.00, 0.0367, 0.0372),
 'Heraklion': (3196.67, 2337.14, 571.75, 0.0384, 0.0435), 'Patras': (1826.29, 1568.00, 435.33, 0.0496, 0.0493),
 'Chania': (3692.64, 3134.36, 564.29, 0.0337, 0.0332)}

# published yields
YPUB = {
 'spit_ind_q2': ('Spitogatos Insights indicative gross yield (asking rent / asking price), 2026-Q2', 'https://www.spitogatos.gr/deiktis-timon', 'undated live page'),
 'gpg': ('Global Property Guide (1-bedroom flat gross yield)', 'https://www.globalpropertyguide.com/europe/greece/rental-yields', 'page last update May 2026'),
 'spit_cap_2025': ('Spitogatos Data Report cap rate (asking), May 2025', 'https://www.newmoney.gr/roh/palmos-oikonomias/oikonomia/spitogatos-data-report-i-anerchomenes-perioches-gia-ependisis-se-katikies-i-perioches-me-tis-ipsiloteres-apodosis/', '2025-06-23'),
 'numbeo': ('Numbeo gross rental yield (city centre / outside)', 'https://www.numbeo.com/property-investment/in/', '2026-10-22'),
 'spit_ptr_2025': ('Spitogatos price-to-rent 2025 (12 / months of rent)', 'https://www.cnn.gr/oikonomia/chrima/story/525434/posa-enoikia-xreiazontai-gia-tin-agora-spitioy-ti-isxyei-gia-kathe-proastio-tis-attikis', '2026-03-25'),
 'gpg_city': ('Global Property Guide city average gross yield', 'https://www.globalpropertyguide.com/europe/greece/rental-yields', 'page last update May 2026'),
}
def yp(key, v, note=None):
    d = dict(value=v, provider=YPUB[key][0], source=YPUB[key][1], source_date=YPUB[key][2], retrieved=RETR)
    if note: d['note'] = note
    return d

# ----------------------------------------------------------------- policy tags
GV8, GV4 = 800000, 400000
STR_NOTE = 'new STR registrations frozen until 2026-12-31 (2027 extension planned in DBP 2027, not enacted)'

# ----------------------------------------------------------------- place registry
# fields: id, en, he, region, type, level, lat, lng, ind=(path,name), spi=name, xe=name, sq3, sq2, isl, hol, ng, other
P = []
def add(id, en, he, region, type, level, lat, lng, gv=None, border=False, strf=False, notes='', **src):
    P.append(dict(id=id, name_en=en, name_he=he, region=region, type=type, level=level, lat=lat, lng=lng,
                  gv=gv, border=border, strf=strf, notes=notes, src=src))

A = 'Attica'; CM = 'Central Macedonia'; EMT = 'East Macedonia & Thrace'; WM = 'West Macedonia'; EP = 'Epirus'
TH = 'Thessaly'; CG = 'Central Greece'; WG = 'Western Greece'; PE = 'Peloponnese'; IO = 'Ionian Islands'
NA = 'North Aegean'; SA = 'South Aegean'; CR = 'Crete'
KA = 'attiki/kentro-athinas-perifereia/'; IK = 'attiki/istoriko-kentro/'; NS = 'attiki/athina-notia-proastia-perifereia/'
VP = 'attiki/athina-voreia-proastia-perifereia/'; DP = 'attiki/athina-dytika-proastia-perifereia/'; AP = 'attiki/athina-anatolika-proastia-perifereia/'
YA = 'attiki/ypoloipo-attikis-perifereia/'; PI = 'attiki/peiraias-perifereia/'; PP = 'attiki/proastia-peiraia-perifereia/'
AR = 'attiki/nisia-argosaronikou-perifereia/'; TD = 'thessaloniki/thessaloniki-dimos-perifereia/'; TS = 'thessaloniki/thessaloniki-perif-koi-dimoi-perifereia/'

# --- 13 administrative regions
add('attica', 'Attica', 'אטיקה', A, 'region', 'admin_region', 38.00, 23.73, gv=GV8, ind=('', 'Attika'))
add('central-macedonia', 'Central Macedonia', 'מקדוניה המרכזית', CM, 'region', 'admin_region', 40.65, 23.10, gv='mixed',
    border='partial', notes='No provider publishes this administrative region as one figure; see Thessaloniki, Halkidiki, Serres, Pieria, Imathia, Pella, Kilkis entries.')
add('east-macedonia-thrace', 'East Macedonia & Thrace', 'מקדוניה המזרחית ותרקיה', EMT, 'region', 'admin_region', 41.10, 24.90, gv=GV4,
    border='partial', notes='No single published figure; Indomio "Thrace" grouping (Evros, Xanthi, Rodopi) is a separate entry; Kavala and Drama are in Indomio "Macedonia".')
add('west-macedonia', 'West Macedonia', 'מקדוניה המערבית', WM, 'region', 'admin_region', 40.30, 21.60, gv=GV4, border='partial',
    notes='No single published figure; see Kozani, Kastoria, Florina, Grevena.')
add('epirus', 'Epirus', 'אפירוס', EP, 'region', 'admin_region', 39.60, 20.80, gv=GV4, border='partial', ind=('', 'Epirus'))
add('thessaly', 'Thessaly', 'תסליה', TH, 'region', 'admin_region', 39.50, 22.30, gv=GV4, ind=('', 'Thessaly'),
    notes='Indomio Thessaly = Larissa, Magnesia, Trikala, Karditsa; the Sporades (administratively Thessaly) are counted by Indomio in Aegean Islands.')
add('central-greece', 'Central Greece (Sterea Ellada)', 'יוון המרכזית (סטריאה אלדה)', CG, 'region', 'admin_region', 38.70, 22.70, gv='mixed',
    ind=('', 'Central Greece'), notes='Indomio "Central Greece" also includes Aitoloakarnania (administratively Western Greece). Evia is an island (>3,100 inhabitants), so EUR 800k may apply there; mainland units EUR 400k.')
add('western-greece', 'Western Greece', 'יוון המערבית', WG, 'region', 'admin_region', 38.30, 21.60, gv=GV4,
    notes='No single published figure; see Achaia/Patras, Ilia, Aitoloakarnania.')
add('peloponnese', 'Peloponnese', 'פלופונס', PE, 'region', 'admin_region', 37.40, 22.30, gv=GV4, ind=('', 'Peloponnese'),
    notes='Indomio "Peloponnese" also includes Achaia and Ilia (administratively Western Greece).')
add('ionian-islands', 'Ionian Islands', 'האיים היוניים', IO, 'region', 'admin_region', 38.80, 20.40, gv='mixed', border='partial',
    ind=('', 'Ionian Islands'), isl='Ionian islands')
add('north-aegean', 'North Aegean', 'צפון הים האגאי', NA, 'region', 'admin_region', 38.90, 26.20, gv='mixed', border=True,
    notes='No single published figure; see Lesvos, Chios, Samos.')
add('south-aegean', 'South Aegean', 'דרום הים האגאי', SA, 'region', 'admin_region', 36.90, 25.80, gv='mixed', border='partial',
    notes='No single published figure; see Cyclades and Dodecanese.')
add('crete', 'Crete', 'כרתים', CR, 'region', 'admin_region', 35.25, 24.90, gv=GV8, ind=('', 'Crete'), isl='Crete')
# --- provider groupings
add('grp-macedonia', 'Macedonia excl. Thessaloniki (Indomio grouping)', 'מקדוניה ללא סלוניקי (קיבוץ של Indomio)', CM, 'region', 'provider_grouping', 40.70, 22.30,
    gv='mixed', border='partial', ind=('', 'Macedonia'), notes='Indomio grouping across Central, West and East Macedonia (not an administrative region).')
add('grp-thrace', 'Thrace (Evros, Xanthi, Rodopi)', 'תרקיה (אברוס, קסנתי, רודופי)', EMT, 'region', 'provider_grouping', 41.10, 25.40, gv=GV4, border=True, ind=('', 'Thrace'))
add('grp-aegean', 'Aegean islands (Indomio grouping)', 'איי הים האגאי (קיבוץ של Indomio)', SA, 'region', 'provider_grouping', 37.60, 25.80,
    gv='mixed', border='partial', ind=('', 'Aegean Islands'), isl='Aegean islands', notes='Cyclades, Dodecanese, Lesvos, Chios, Samos, Sporades.')

# --- regional units (prefectures)
RU = [
 ('ru-thessaloniki', 'Thessaloniki (regional unit)', 'מחוז סלוניקי', CM, 40.70, 23.05, GV8, False, ('', 'Thessaloniki'), None),
 ('ru-aitoloakarnania', 'Aitoloakarnania (Agrinio, Mesolongi)', 'אטוליה-אקרנניה', WG, 38.62, 21.41, GV4, False, ('sterea-ellada/', 'Aetolia & Acarnania'), 'Αιτωλοακαρνανία'),
 ('ru-argolida', 'Argolida (Nafplio, Porto Heli)', 'ארגוליס', PE, 37.62, 22.73, GV4, False, ('peloponnisos/', 'Argolis'), 'Αργολίδα'),
 ('ru-arkadia', 'Arkadia (Tripoli)', 'ארקדיה', PE, 37.51, 22.37, GV4, False, ('peloponnisos/', 'Arcadia'), 'Αρκαδία'),
 ('ru-arta', 'Arta', 'ארטה', EP, 39.16, 20.99, GV4, False, ('ipiros/', 'Arta Prefecture'), 'Ν. Άρτας'),
 ('ru-achaia', 'Achaia (Patras)', 'אכאיה', WG, 38.10, 21.90, GV4, False, ('peloponnisos/', 'Achaia'), 'Αχαΐα'),
 ('ru-viotia', 'Viotia (Livadeia, Thiva)', 'בויאוטיה', CG, 38.40, 23.00, GV4, False, ('sterea-ellada/', 'Boeotia'), 'Βοιωτία'),
 ('ru-grevena', 'Grevena', 'גרבנה', WM, 40.08, 21.43, GV4, False, ('macedonia/', 'Grevena Prefecture'), 'Γρεβενά'),
 ('ru-drama', 'Drama', 'מחוז דרמה', EMT, 41.20, 24.20, GV4, 'partial', ('macedonia/', 'Drama Prefecture'), 'Ν. Δράμας'),
 ('ru-dodecanese', 'Dodecanese', 'הדודקנסוס', SA, 36.60, 27.40, 'mixed', True, ('nisia-aigaiou/', 'Dodecanese'), 'Δωδεκάνησα'),
 ('ru-evros', 'Evros (Alexandroupoli)', 'אברוס', EMT, 41.10, 26.10, GV4, True, ('thraki/', 'Evros'), 'Έβρος'),
 ('ru-evia', 'Evia (Euboea)', 'אוויה', CG, 38.55, 23.80, 'mixed', 'partial', ('sterea-ellada/', 'Evia'), 'Εύβοια'),
 ('ru-evrytania', 'Evrytania (Karpenisi)', 'אבריטניה', CG, 38.91, 21.79, GV4, False, ('sterea-ellada/', 'Evrytania'), 'Ευρυτανία'),
 ('ru-ilia', 'Ilia (Pyrgos)', 'איליה', WG, 37.68, 21.44, GV4, False, ('peloponnisos/', 'Ilia'), 'Ηλεία'),
 ('ru-imathia', 'Imathia (Veria)', 'אימתיה', CM, 40.55, 22.25, GV4, False, ('macedonia/', 'Imathia'), 'Ημαθία'),
 ('ru-heraklion', 'Heraklion (regional unit, Crete)', 'מחוז הרקליון', CR, 35.20, 25.15, GV8, False, ('kriti/', 'Heraklion Prefecture'), 'Ν. Ηρακλείου'),
 ('ru-thesprotia', 'Thesprotia (Igoumenitsa, Syvota)', 'תספרוטיה', EP, 39.50, 20.30, GV4, True, ('ipiros/', 'Thesprotia'), 'Θεσπρωτία'),
 ('ru-ioannina', 'Ioannina (regional unit)', 'מחוז יואנינה', EP, 39.80, 20.70, GV4, 'partial', ('ipiros/', 'Ioannina Prefecture'), 'Ν. Ιωαννίνων'),
 ('ru-kavala', 'Kavala (regional unit, incl. Thassos)', 'מחוז קוואלה', EMT, 40.95, 24.30, 'mixed', False, ('macedonia/', 'Kavala Prefecture'), 'Ν. Καβάλας'),
 ('ru-karditsa', 'Karditsa', 'קרדיצה', TH, 39.36, 21.92, GV4, False, ('thessalia/', 'Karditsa Prefecture'), 'Ν. Καρδίτσας'),
 ('ru-kastoria', 'Kastoria', 'קסטוריה', WM, 40.52, 21.27, GV4, True, ('macedonia/', 'Kastoria Prefecture'), 'Ν. Καστοριάς'),
 ('ru-corfu', 'Corfu (regional unit, incl. Paxoi)', 'מחוז קורפו', IO, 39.55, 19.85, 'mixed', 'partial', ('nisia-ioniou/', 'Corfu Prefecture'), 'Ν. Κέρκυρας'),
 ('ru-kefalonia', 'Kefalonia (regional unit, incl. Ithaca)', 'מחוז קפלוניה', IO, 38.25, 20.55, 'mixed', False, ('nisia-ioniou/', 'Kefallinia Prefecture'), 'Ν. Κεφαλονιάς'),
 ('ru-kilkis', 'Kilkis', 'קילקיס', CM, 40.99, 22.87, GV4, True, ('macedonia/', 'Kilkis Prefecture'), 'Ν. Κιλκίς'),
 ('ru-kozani', 'Kozani (regional unit)', 'מחוז קוזאני', WM, 40.35, 21.75, GV4, False, ('macedonia/', 'Kozani Prefecture'), 'Ν. Κοζάνης'),
 ('ru-corinthia', 'Corinthia (Corinth, Loutraki)', 'קורינתיה', PE, 37.88, 22.65, GV4, False, ('peloponnisos/', 'Corinthia'), 'Κορινθία'),
 ('ru-cyclades', 'Cyclades', 'הקיקלאדים', SA, 37.10, 25.20, 'mixed', 'partial', ('nisia-aigaiou/', 'Cyclades'), 'Κυκλάδες'),
 ('ru-lakonia', 'Lakonia (Sparti, Monemvasia)', 'לקוניה', PE, 36.90, 22.60, GV4, False, ('peloponnisos/', 'Lakonia'), 'Λακωνία'),
 ('ru-larissa', 'Larissa (regional unit)', 'מחוז לריסה', TH, 39.70, 22.35, GV4, False, ('thessalia/', 'Larissa Prefecture'), 'Ν. Λάρισας'),
 ('ru-lasithi', 'Lasithi (Agios Nikolaos, Elounda)', 'לסיתי', CR, 35.10, 25.80, GV8, False, ('kriti/', 'Lasithi Prefecture'), 'Ν. Λασιθίου'),
 ('ru-magnesia', 'Magnesia (Volos, Pelion)', 'מגנסיה', TH, 39.30, 23.00, GV4, False, ('thessalia/', 'Magnesia'), 'Μαγνησία'),
 ('ru-messinia', 'Messinia (Kalamata, Pylos)', 'מסיניה', PE, 37.05, 21.85, GV4, False, ('peloponnisos/', 'Messinia'), 'Μεσσηνία'),
 ('ru-xanthi', 'Xanthi (regional unit)', 'מחוז קסנתי', EMT, 41.20, 24.95, GV4, True, ('thraki/', 'Xanthi Prefecture'), 'Ν. Ξάνθης'),
 ('ru-pella', 'Pella (Edessa, Giannitsa)', 'פלה', CM, 40.80, 22.05, GV4, 'partial', ('macedonia/', 'Pella Prefecture'), 'Πέλλα'),
 ('ru-pieria', 'Pieria (Katerini)', 'פיאריה', CM, 40.20, 22.55, GV4, False, ('macedonia/', 'Pieria Prefecture'), 'Ν. Πιερίας'),
 ('ru-preveza', 'Preveza (Parga)', 'פרבזה', EP, 39.10, 20.70, GV4, True, ('ipiros/', 'Preveza Prefecture'), 'Ν. Πρέβεζας'),
 ('ru-rethymno', 'Rethymno (regional unit, Crete)', 'מחוז רתימנו', CR, 35.25, 24.55, GV8, False, ('kriti/', 'Rethymno Prefecture'), 'Ν. Ρεθύμνου'),
 ('ru-rodopi', 'Rodopi (Komotini)', 'רודופי', EMT, 41.05, 25.50, GV4, True, ('thraki/', 'Rodopi Prefecture'), 'Ν. Ροδόπης'),
 ('ru-serres', 'Serres (regional unit)', 'מחוז סרס', CM, 41.10, 23.60, GV4, 'partial', ('macedonia/', 'Serres Prefecture'), 'Ν. Σέρρες'),
 ('ru-trikala', 'Trikala (regional unit, Meteora)', 'מחוז טריקלה', TH, 39.60, 21.70, GV4, False, ('thessalia/', 'Trikala Prefecture'), 'Ν. Τρικάλων'),
 ('ru-fthiotida', 'Fthiotida (Lamia)', 'פתיוטידה', CG, 38.85, 22.50, GV4, False, ('sterea-ellada/', 'Phthiotis'), 'Φθιώτιδα'),
 ('ru-florina', 'Florina', 'פלורינה', WM, 40.78, 21.41, GV4, True, ('macedonia/', 'Florina Prefecture'), 'Ν. Φλώρινας'),
 ('ru-fokida', 'Fokida (Amfissa, Galaxidi)', 'פוקידה', CG, 38.50, 22.35, GV4, False, ('sterea-ellada/', 'Fokida'), 'Φωκίδα'),
 ('ru-halkidiki', 'Halkidiki', 'חלקידיקי', CM, 40.30, 23.45, GV4, False, ('macedonia/', 'Chalkidiki'), 'Χαλκιδική'),
 ('ru-chania', 'Chania (regional unit, Crete)', 'מחוז חאניה', CR, 35.40, 23.90, GV8, False, ('kriti/', 'Chania Prefecture'), 'Ν. Χανίων'),
 ('ru-argosaronic', 'Argosaronic islands (Aegina, Hydra, Spetses, Poros, Salamina)', 'איי הים הסרוני', A, 37.60, 23.40, GV8, False, ('attiki/', 'Argosaronikos islands'), 'Νησιά Αργοσαρωνικού'),
 ('ru-sporades', 'Sporades (Skiathos, Skopelos, Alonnisos)', 'ספוראדס', TH, 39.15, 23.70, 'mixed', False, ('nisia-aigaiou/', 'Sporades'), 'Σποράδες'),
]
for r in RU:
    id_, en, he, reg, lat, lng, gv, bor, indk, spik = r
    extra = {}
    sq3 = {'ru-chania': 'Chania RU', 'ru-kastoria': 'Kastoria', 'ru-kozani': 'Kozani', 'ru-florina': 'Florina', 'ru-kilkis': 'Kilkis',
           'ru-karditsa': 'Karditsa', 'ru-pella': 'Pella', 'ru-imathia': 'Imathia', 'ru-grevena': 'Grevena', 'ru-cyclades': 'Cyclades'}.get(id_)
    isl = {'ru-heraklion': 'Heraklion RU', 'ru-chania': 'Chania RU', 'ru-rethymno': 'Rethymno RU', 'ru-lasithi': 'Lasithi RU'}.get(id_)
    notes = ''
    if id_ == 'ru-evia': notes = 'Evia island is above 3,100 inhabitants (EUR 800k likely applies on the island; verify); Skyros (border zone) is in this unit.'
    if id_ == 'ru-cyclades': notes = 'Border permit needed on Santorini (Thira) only. GV: Mykonos, Santorini and islands above 3,100 inhabitants EUR 800k; smaller islands EUR 400k.'
    if id_ == 'ru-corfu': notes = 'Border-zone list covers the Diapontia islands only (not Corfu main island).'
    if id_ == 'ru-kavala': notes = 'Thassos (island, >3,100 inhabitants) EUR 800k; mainland Kavala EUR 400k.'
    if id_ == 'ru-dodecanese': notes = 'Entire Dodecanese is a border zone (non-EU buyers need a permit).'
    add(id_, en, he, reg, 'region', 'regional_unit', lat, lng, gv=gv, border=bor, notes=notes, ind=indk, spi=spik, sq3=sq3, isl=isl)
# fix: Lefkada / Zakynthos / Lesvos / Samos / Chios RUs are represented by their island entries below (same geography)

# --- Attica sub-areas
SUB = [
 ('ath-centre', 'Athens Centre (Municipality of Athens)', 'מרכז אתונה (עיריית אתונה)', 37.985, 23.730, ('attiki/', 'Athens - Center'), 'Athens Centre', 'Αθήνα', 'Athens Centre', 'partial'),
 ('ath-north', 'Athens North suburbs', 'הפרברים הצפוניים של אתונה', 38.040, 23.800, ('attiki/', 'Athens - North'), 'Athens North', None, 'Athens North', False),
 ('ath-south', 'Athens South suburbs (Riviera)', 'הפרברים הדרומיים של אתונה (הריביירה)', 37.890, 23.740, ('attiki/', 'Athens - South'), 'Athens South', None, 'Athens South', False),
 ('ath-east', 'Athens East suburbs (Mesogeia)', 'הפרברים המזרחיים של אתונה', 37.960, 23.880, ('attiki/', 'Athens - East'), 'Athens East', None, None, False),
 ('ath-west', 'Athens West suburbs', 'הפרברים המערביים של אתונה', 38.020, 23.680, ('attiki/', 'Athens - West'), 'Athens West', None, None, False),
 ('piraeus', 'Piraeus (municipality)', 'פיראוס', 37.943, 23.647, ('attiki/', 'Piraeus'), 'Piraeus', 'Πειραιάς', 'Piraeus', False),
 ('piraeus-suburbs', 'Piraeus suburbs', 'פרברי פיראוס', 37.965, 23.630, ('attiki/', 'Piraeus suburbs'), 'Piraeus suburbs', None, None, False),
 ('rest-attica', 'Rest of Attica (East + West Attica)', 'שאר אטיקה (מזרח ומערב)', 37.950, 23.950, ('attiki/', 'Rest of Attica'), 'Rest of Attica', None, None, False),
]
for id_, en, he, lat, lng, indk, spik, xek, sq3k, strf in SUB:
    add(id_, en, he, A, 'area', 'sub_area', lat, lng, gv=GV8, strf=strf, ind=indk, spi=spik, xe=xek, sq3=sq3k,
        notes='STR freeze applies only in Athens municipal districts 1-3.' if strf == 'partial' else '')

# --- Athens neighbourhoods (Municipality of Athens)
NB = [
 ('kolonaki', 'Kolonaki - Lykavittos', 'קולונקי', 37.979, 23.743, KA, 'Kolonaki - Lykavittos', True, 'Kolonaki'),
 ('koukaki', 'Koukaki - Makrygianni', 'קוקאקי', 37.964, 23.725, KA, 'Koukaki - Makrygianni', True, 'Koukaki'),
 ('pagrati', 'Pangrati', 'פנגרטי', 37.968, 23.747, KA, 'Pagkrati', True, None),
 ('exarcheia', 'Exarcheia - Neapoli', 'אקסרכיה', 37.986, 23.735, KA, 'Exarchia - Neapoli', True, 'Exarcheia'),
 ('kypseli', 'Kypseli', 'קיפסלי', 38.002, 23.738, KA, 'Kipseli', False, 'Kypseli'),
 ('neos-kosmos', 'Neos Kosmos', 'נאוס קוסמוס', 37.958, 23.729, KA, 'Neos Kosmos', True, 'Neos Kosmos'),
 ('mets', 'Mets - Kallimarmaro', 'מטס', 37.967, 23.740, KA, 'Mets - Kalimarmaro', True, None),
 ('petralona', 'Petralona', 'פטרלונה', 37.969, 23.709, KA, 'Petralona', True, 'Petralona'),
 ('gazi', 'Gazi - Metaxourgeio - Votanikos', 'גאזי - מטקסורגיו', 37.979, 23.712, KA, 'Gazi - Metaxourgio - Votanikos', True, None),
 ('ilisia', 'Ilisia', 'איליסיה', 37.977, 23.762, KA, 'Ilisia', True, None),
 ('ampelokipoi', 'Ampelokipoi - Pentagon', 'אמפלוקיפי', 37.988, 23.758, KA, 'Ampelokipoi - Pentagon', False, None),
 ('patisia', 'Patisia', 'פטיסיה', 38.020, 23.733, KA, 'Patisia', False, None),
 ('gyzi', 'Gyzi - Pedion Areos', 'גיזי - פדיון אראוס', 37.997, 23.745, KA, 'Gizi - Pedion Areos', False, None),
 ('athens-historic', 'Athens Historic Centre', 'המרכז ההיסטורי של אתונה', 37.972, 23.727, KA, 'Athens Historic Center', True, None),
 ('athens-kentro', 'Athens commercial centre (Syntagma-Omonoia)', 'מרכז העסקים של אתונה (סינטגמה-אומוניה)', 37.981, 23.731, KA, 'Athens Center', True, None),
 ('plaka', 'Plaka', 'פלאקה', 37.9725, 23.730, IK, 'Plaka', True, None),
 ('thiseio', 'Thiseio', 'תיסיו', 37.977, 23.719, IK, 'Thiseio', True, None),
 ('monastiraki', 'Monastiraki', 'מונסטירקי', 37.976, 23.725, IK, 'Monastiraki', True, None),
 ('akropoli', 'Akropoli (Makrygianni side)', 'אקרופולי', 37.969, 23.728, IK, 'Akropoli', True, None),
 ('syntagma', 'Syntagma', 'סינטגמה', 37.9755, 23.735, 'attiki/kentro/', 'Sintagma', True, None),
 ('psyrri', 'Psyrri', 'פסירי', 37.978, 23.724, 'attiki/kentro/', 'Psirri', True, None),
]
for id_, en, he, lat, lng, path, nm, strf, rk in NB:
    add(id_, en, he, A, 'area', 'neighbourhood', lat, lng, gv=GV8, strf=strf, ind=(path, nm), remax_rent=rk,
        sq3={'kolonaki': 'Kolonaki', 'patisia': 'Patisia', 'athens-kentro': 'Kentro Athinas'}.get(id_),
        sq2={'kolonaki': 'Kolonaki'}.get(id_))

# --- Attica municipalities
MU = [
 # id, en, he, lat, lng, (path,name) or None, xe greek, sq3, sq2, hol
 ('glyfada', 'Glyfada', 'גליפדה', 37.865, 23.753, (NS, 'Glyfada'), 'Γλυφάδα', 'Glyfada', 'Glyfada', None),
 ('voula', 'Voula', 'וולה', 37.844, 23.774, (NS, 'Voula'), 'Βούλα', 'Voula', 'Voula', None),
 ('vouliagmeni', 'Vouliagmeni', 'ווליאגמני', 37.813, 23.781, (NS, 'Vouliagmeni'), None, 'Vouliagmeni', 'Vouliagmeni', None),
 ('vari-varkiza', 'Vari - Varkiza', 'וארי - ורקיזה', 37.825, 23.805, (NS, 'Vari - Varkiza'), 'Βάρη', None, None, None),
 ('alimos', 'Alimos', 'אלימוס', 37.910, 23.722, (NS, 'Alimos'), 'Άλιμος', None, None, None),
 ('palaio-faliro', 'Palaio Faliro', 'פליאו פלירו', 37.928, 23.700, (NS, 'Palaio Faliro'), 'Παλαιό Φάληρο', None, None, None),
 ('elliniko', 'Elliniko (Ellinikon)', 'אליניקו', 37.893, 23.747, (NS, 'Elliniko'), 'Ελληνικό', 'Elliniko', 'Elliniko', None),
 ('kallithea', 'Kallithea', 'קליתאה', 37.955, 23.702, (NS, 'Kallithea'), 'Καλλιθέα', None, None, None),
 ('nea-smyrni', 'Nea Smyrni', 'ניאה סמירני', 37.945, 23.713, (NS, 'Nea Smyrni'), 'Νέα Σμύρνη', None, None, None),
 ('agios-dimitrios', 'Agios Dimitrios', 'אגיוס דימיטריוס', 37.933, 23.733, (NS, 'Agios Dimitrios'), 'Αγ. Δημήτριος Αττικής', None, None, None),
 ('argyroupoli', 'Argyroupoli', 'ארגירופולי', 37.905, 23.749, (NS, 'Argyroupoli'), 'Αργυρούπολη', None, None, None),
 ('ilioupoli', 'Ilioupoli', 'איליופולי', 37.931, 23.760, (NS, 'Ilioupoli'), 'Ηλιούπολη', None, None, None),
 ('dafni', 'Dafni', 'דפני', 37.949, 23.737, (NS, 'Dafni'), 'Δάφνη Αττικής', 'Dafni', 'Dafni', None),
 ('vyronas', 'Vyronas', 'וירונס', 37.960, 23.753, (NS, 'Vironas'), 'Βύρωνας', None, None, None),
 ('zografou', 'Zografou', 'זוגרפו', 37.976, 23.769, (NS, 'Zografou'), 'Ζωγράφου', None, None, None),
 ('kaisariani', 'Kaisariani', 'קייסריאני', 37.967, 23.765, (NS, 'Kaisariani'), 'Καισαριανή', 'Kaisariani', None, None),
 ('kifisia', 'Kifisia', 'קיפיסיה', 38.074, 23.811, (VP, 'Kifissia'), 'Κηφισιά', None, None, None),
 ('marousi', 'Marousi', 'מרוסי', 38.050, 23.806, (VP, 'Marousi'), 'Μαρούσι', None, None, None),
 ('chalandri', 'Chalandri', 'חלנדרי', 38.021, 23.799, (VP, 'Chalandri'), 'Χαλάνδρι', None, None, None),
 ('palaio-psychiko', 'Palaio Psychiko', 'פליאו פסיכיקו', 38.013, 23.772, (VP, 'Paleo Psichiko'), None, 'Palaio Psychiko', 'Palaio Psychiko', None),
 ('neo-psychiko', 'Neo Psychiko', 'נאו פסיכיקו', 38.005, 23.773, (VP, 'Neo Psychiko'), None, 'Neo Psychiko', None, None),
 ('filothei', 'Filothei', 'פילותאי', 38.023, 23.784, (VP, 'Filothei'), None, None, None, None),
 ('ekali', 'Ekali', 'אקאלי', 38.101, 23.833, (VP, 'Ekali'), None, None, None, None),
 ('nea-erythraia', 'Nea Erythraia', 'ניאה אריתראה', 38.093, 23.818, (VP, 'Nea Erithraia'), 'Νέα Ερυθραία', None, None, None),
 ('agia-paraskevi', 'Agia Paraskevi', 'אגיה פרסקבי', 38.011, 23.820, None, 'Αγ. Παρασκευή', None, None, None),
 ('cholargos', 'Cholargos', 'חולרגוס', 38.002, 23.800, None, 'Χολαργός', None, None, None),
 ('vrilissia', 'Vrilissia', 'ורליסיה', 38.035, 23.830, None, 'Βριλήσσια', None, None, None),
 ('melissia', 'Melissia', 'מליסיה', 38.050, 23.833, None, 'Μελίσσια', None, None, None),
 ('gerakas', 'Gerakas', 'גרקס', 38.023, 23.856, (AP, 'Gerakas'), 'Γέρακας', None, None, None),
 ('pallini-attica', 'Pallini (Attica)', 'פליני (אטיקה)', 38.006, 23.880, (AP, 'Pallini (Attica)'), 'Παλλήνη', None, None, None),
 ('koropi', 'Koropi', 'קורופי', 37.900, 23.873, (AP, 'Koropi'), 'Κορωπί', None, None, None),
 ('glyka-nera', 'Glyka Nera', 'גליקה נרה', 37.993, 23.847, (AP, 'Glika Nera'), None, None, None, None),
 ('artemida', 'Artemida (Loutsa)', 'ארטמידה (לוצה)', 37.972, 24.004, (AP, 'Artemida (Loutsa)'), 'Άρτεμις', 'Artemida', None, 'Artemida'),
 ('marathon', 'Marathon', 'מרתון', 38.153, 23.962, (AP, 'Marathonas'), None, None, None, 'Marathon'),
 ('nea-makri', 'Nea Makri', 'ניאה מקרי', 38.087, 23.976, (AP, 'Nea Makri'), None, None, None, 'Nea Makri'),
 ('peristeri', 'Peristeri', 'פריסטרי', 38.015, 23.691, (DP, 'Peristeri'), 'Περιστέρι', None, None, None),
 ('aigaleo', 'Aigaleo', 'אגלאו', 37.992, 23.682, (DP, 'Aigaleo'), 'Αιγάλεω', None, None, None),
 ('galatsi', 'Galatsi', 'גלאצי', 38.017, 23.759, (DP, 'Galatsi'), 'Γαλάτσι', None, None, None),
 ('nea-ionia', 'Nea Ionia', 'ניאה יוניה', 38.037, 23.755, (DP, 'Nea Ionia'), 'Νέα Ιωνία', 'Nea Ionia', None, None),
 ('nea-filadelfeia', 'Nea Filadelfeia', 'ניאה פילדלפיה', 38.035, 23.738, (DP, 'Nea Philadelfia'), None, 'Nea Filadelfeia', 'Nea Filadelfeia', None),
 ('acharnes', 'Acharnes', 'אחרנס', 38.083, 23.735, (DP, 'Acharnes'), 'Αχαρνές', 'Acharnes', None, None),
 ('petroupoli', 'Petroupoli', 'פטרופולי', 38.041, 23.684, (DP, 'Petroupoli'), 'Πετρούπολη', None, None, None),
 ('ilion', 'Ilion', 'איליון', 38.033, 23.700, (DP, 'Ilion'), 'Ίλιον', None, None, None),
 ('chaidari', 'Chaidari', 'חיידרי', 38.012, 23.665, (DP, 'Chaidari'), 'Χαϊδάρι', None, None, None),
 ('agia-varvara', 'Agia Varvara', 'אגיה ורורה', 37.990, 23.659, (DP, 'Agia Varvara'), None, 'Agia Varvara', None, None),
 ('nikaia', 'Nikaia', 'ניקאיה', 37.966, 23.647, (PP, 'Nikaia'), 'Νίκαια', None, None, None),
 ('keratsini', 'Keratsini', 'קרצ\'יני', 37.962, 23.620, (PP, 'Keratsini'), 'Κερατσίνι', None, None, None),
 ('korydallos', 'Korydallos', 'קורידלוס', 37.984, 23.650, (PP, 'Koridallos'), 'Κορυδαλλός', None, None, None),
 ('moschato', 'Moschato', 'מוסחטו', 37.953, 23.680, (PP, 'Moschato'), 'Μοσχάτο', None, None, None),
 ('perama', 'Perama', 'פרמה', 37.965, 23.570, (PP, 'Perama'), None, 'Perama', None, None),
 ('kastella', 'Kastella - Passalimani (Piraeus)', 'קסטלה - פסלימני (פיראוס)', 37.938, 23.656, (PI, 'Kastella - Passalimani'), None, None, None, None),
 ('neo-faliro', 'Neo Faliro (Piraeus)', 'נאו פלירו (פיראוס)', 37.945, 23.665, (PI, 'Neo Faliro'), None, 'Neo Faliro', None, None),
 ('saronida', 'Saronida', 'סרונידה', 37.748, 23.915, (YA, 'Saronida'), 'Σαρωνίδα', None, None, 'Saronida'),
 ('anavyssos', 'Anavyssos', 'אנביסוס', 37.733, 23.947, (YA, 'Anavissos'), None, None, None, 'Anavyssos'),
 ('palaia-fokaia', 'Palaia Fokaia', 'פליאה פוקאיה', 37.720, 23.950, (YA, 'Palaia Fokaia'), None, None, None, 'Palaia Fokaia'),
 ('rafina', 'Rafina', 'רפינה', 38.022, 24.005, (YA, 'Rafina'), None, None, None, 'Rafina'),
 ('porto-rafti', 'Porto Rafti', 'פורטו רפטי', 37.884, 24.013, None, 'Πόρτο Ράφτη', None, None, 'Porto Rafti'),
 ('kalyvia', 'Kalyvia Thorikou', 'קליוויה תוריקו', 37.835, 23.933, (YA, 'Kalivia Thorikou'), 'Καλύβια Θορικού', None, None, None),
 ('markopoulo', 'Markopoulo Mesogaias', 'מרקופולו', 37.884, 23.930, (YA, 'Markopoulo'), None, None, None, None),
 ('lavrio', 'Lavrio', 'לבריו', 37.714, 24.056, (YA, 'Lavrio'), None, None, None, None),
 ('keratea', 'Keratea', 'קרטאה', 37.808, 23.977, (YA, 'Keratea'), None, None, None, 'Keratea'),
 ('megara', 'Megara', 'מגרה', 37.995, 23.344, (YA, 'Megara'), None, None, None, None),
 ('lagonisi', 'Lagonisi', 'לגוניסי', 37.786, 23.888, None, None, None, None, None),
]
for id_, en, he, lat, lng, indk, xek, sq3k, sq2k, holk in MU:
    add(id_, en, he, A, 'area', 'municipality', lat, lng, gv=GV8, ind=indk, xe=xek, sq3=sq3k, sq2=sq2k, hol=holk,
        remax_rent={'vari-varkiza': 'Vari-Varkiza'}.get(id_))

# --- Thessaloniki
TSL = [
 ('thess-municipality', 'Thessaloniki (municipality)', 'סלוניקי (העירייה)', 40.632, 22.950, 'sub_area', ('thessaloniki/', 'Thessaloniki - Municipality'), 'Thessaloniki Municipality', 'Θεσσαλονίκη', None, None, 'partial'),
 ('thess-suburbs', 'Thessaloniki suburbs', 'פרברי סלוניקי', 40.620, 22.990, 'sub_area', ('thessaloniki/', 'Thessaloniki - Suburbs'), 'Thessaloniki Suburbs', None, None, None, False),
 ('thess-rest', 'Rest of Thessaloniki prefecture', 'שאר מחוז סלוניקי', 40.700, 23.200, 'sub_area', ('thessaloniki/', 'Thessaloniki - Rest of Prefecture'), 'Thessaloniki Rest', None, 'Thessaloniki Rest', None, False),
 ('thess-centre', 'Thessaloniki Centre', 'מרכז סלוניקי', 40.633, 22.944, 'neighbourhood', (TD, 'Thessaloniki - Center'), None, None, 'Thessaloniki Centre', 'Thessaloniki Centre', True),
 ('ano-poli', 'Ano Poli', 'אנו פולי', 40.641, 22.955, 'neighbourhood', (TD, 'Ano Poli'), None, None, 'Ano Poli', None, False),
 ('toumba', 'Toumba', 'טומבה', 40.612, 22.970, 'neighbourhood', (TD, 'Toumpa'), None, None, 'Toumba', 'Toumba', False),
 ('charilaou', 'Charilaou', 'חרילאו', 40.600, 22.965, 'neighbourhood', (TD, 'Charilaou'), None, None, 'Charilaou', 'Charilaou', False),
 ('40-ekklisies', '40 Ekklisies - Evangelistria', '40 אקליסייס', 40.628, 22.960, 'neighbourhood', (TD, '40 Ekklisies - Evaggelistria'), None, None, '40 Ekklisies', '40 Ekklisies', False),
 ('nea-paralia', 'Analipsi - Botsari - Nea Paralia', 'אנאליפסי - נאה פרליה', 40.615, 22.955, 'neighbourhood', (TD, 'Analipsi - Mpotsari - Nea Paralia'), None, None, None, None, False),
 ('vardaris', 'Vardaris - Lachanokipoi', 'ורדריס', 40.643, 22.928, 'neighbourhood', (TD, 'Vardaris - Lahanokipi'), None, None, 'Vardaris', 'Vardaris', False),
 ('kalamaria', 'Kalamaria', 'קלמריה', 40.582, 22.950, 'municipality', (TS, 'Kalamaria'), None, 'Καλαμαριά', 'Kalamaria', 'Kalamaria', False),
 ('pylaia', 'Pylaia', 'פילאיה', 40.600, 22.987, 'municipality', (TS, 'Pylaia'), None, None, 'Pylaia', 'Pylaia', False),
 ('panorama', 'Panorama', 'פנורמה', 40.588, 23.031, 'municipality', (TS, 'Panorama'), None, None, None, None, False),
 ('thermi', 'Thermi', 'תרמי', 40.547, 23.019, 'municipality', (TS, 'Thermi'), None, None, None, None, False),
 ('peraia', 'Peraia (Thermaikos)', 'פראיה (תרמאיקוס)', 40.503, 22.927, 'municipality', (TS, 'Thermaikos'), None, None, None, None, False),
 ('neapoli-thess', 'Neapoli (Neapoli-Sykies)', 'ניאפולי', 40.655, 22.945, 'municipality', (TS, 'Neapoli'), None, None, None, None, False),
 ('sykies', 'Sykies (Neapoli-Sykies)', 'סיקייס', 40.649, 22.953, 'municipality', (TS, 'Sikies'), None, None, None, None, False),
 ('evosmos', 'Evosmos', 'אבוסמוס', 40.669, 22.908, 'municipality', (TS, 'Evosmos'), None, None, None, None, False),
 ('ampelokipoi-thess', 'Ampelokipoi (Thessaloniki)', 'אמפלוקיפי (סלוניקי)', 40.651, 22.923, 'municipality', (TS, 'Ampelokipoi'), None, None, None, None, False),
 ('menemeni', 'Menemeni', 'מנמני', 40.660, 22.902, 'municipality', (TS, 'Menemeni'), None, None, 'Menemeni', None, False),
 ('oraiokastro', 'Oraiokastro', 'אוראיוקסטרו', 40.730, 22.917, 'municipality', (TS, 'Oreokastro'), None, None, 'Oraiokastro', None, False),
 ('stavroupoli', 'Stavroupoli', 'סטברופולי', 40.668, 22.935, 'municipality', (TS, 'Stavroupoli'), None, None, None, None, False),
 ('epanomi', 'Epanomi', 'אפנומי', 40.427, 22.930, 'municipality', (TS, 'Epanomi'), None, None, 'Epanomi', None, False),
]
for id_, en, he, lat, lng, lvl, indk, spik, xek, sq3k, sq2k, strf in TSL:
    add(id_, en, he, CM, 'area', lvl, lat, lng, gv=GV8, strf=strf, ind=indk, spi=spik, xe=xek, sq3=sq3k, sq2=sq2k,
        remax_rent={'panorama': 'Panorama', 'thermi': 'Thermi', 'peraia': 'Peraia'}.get(id_),
        notes='STR freeze applies in the 1st Municipal Community (historic and commercial centre) only.' if strf == 'partial' else
              ('Peraia has no figure of its own; Indomio publishes it inside Thermaikos municipality.' if id_ == 'peraia' else ''))

# --- cities outside Attica / Thessaloniki
CT = [
 # id, en, he, region, lat, lng, (path,name), gv, border, extra keys
 ('patras', 'Patras', 'פטרה', WG, 38.2466, 21.7346, ('peloponnisos/achaia-perifereia/', 'Patra'), GV4, False, dict(xe='Πάτρα', student='Patras', numbeo='Patras')),
 ('heraklion', 'Heraklion (city)', 'הרקליון', CR, 35.3387, 25.1442, ('kriti/nomos-irakleiou-perifereia/', 'Heraclion Cretes'), GV8, False, dict(xe='Ηράκλειο, Κρήτη', student='Heraklion', numbeo='Heraklion')),
 ('chania', 'Chania (city)', 'חאניה', CR, 35.5138, 24.0180, ('kriti/nomos-chanion-perifereia/', 'Chania'), GV8, False, dict(student='Chania', numbeo='Chania')),
 ('rethymno', 'Rethymno (town)', 'רתימנו', CR, 35.3660, 24.4820, ('kriti/nomos-rethymnou-perifereia/', 'Rethimno'), GV8, False, {}),
 ('agios-nikolaos', 'Agios Nikolaos (incl. Elounda)', 'אגיוס ניקולאוס (כולל אלונדה)', CR, 35.1900, 25.7160, ('kriti/nomos-lasithiou-perifereia/', 'Agios Nikolaos'), GV8, False, {}),
 ('hersonissos', 'Hersonissos', 'חרסוניסוס', CR, 35.3160, 25.3900, ('kriti/nomos-irakleiou-perifereia/', 'Chersonisos'), GV8, False, {}),
 ('larissa', 'Larissa (city)', 'לריסה', TH, 39.6390, 22.4191, ('thessalia/nomos-larisas-perifereia/', 'Larisa'), GV4, False, dict(student='Larissa', thes=1598)),
 ('volos', 'Volos', 'וולוס', TH, 39.3622, 22.9420, ('thessalia/magnisia-perifereia/', 'Volos'), GV4, False, dict(student='Volos', thes=1577)),
 ('ioannina', 'Ioannina (city)', 'יואנינה', EP, 39.6650, 20.8537, ('ipiros/nomos-ioanninon-perifereia/', 'Ioannina'), GV4, 'check', dict(student='Ioannina', epir=(1739, 9.2))),
 ('kavala', 'Kavala (city)', 'קוואלה', EMT, 40.9376, 24.4129, ('macedonia/nomos-kavalas-perifereia/', 'Kavala'), GV4, False, dict(ng='Kavala', hol='Kavala')),
 ('kalamata', 'Kalamata', 'קלמטה', PE, 37.0389, 22.1142, ('peloponnisos/messinia-perifereia/', 'Kalamata'), GV4, False, dict(student='Kalamata', hol='Kalamata')),
 ('alexandroupoli', 'Alexandroupoli', 'אלכסנדרופוליס', EMT, 40.8457, 25.8740, ('thraki/evros-perifereia/', 'Alexandroupoli'), GV4, True, dict(ng='Alexandroupoli')),
 ('serres', 'Serres (city)', 'סרס', CM, 41.0856, 23.5484, ('macedonia/nomos-serron-perifereia/', 'Serres'), GV4, 'check', dict(ng='Serres')),
 ('chalkida', 'Chalkida', 'חלקיס', CG, 38.4636, 23.6024, ('sterea-ellada/evia-perifereia/', 'Chalkida'), 'check', False, dict(student='Chalkida')),
 ('corinth', 'Corinth (Korinthos)', 'קורינתוס', PE, 37.9386, 22.9322, ('peloponnisos/korinthia-perifereia/', 'Korinthos'), GV4, False, {}),
 ('loutraki', 'Loutraki - Perachora', 'לוטרקי', PE, 37.9750, 22.9770, ('peloponnisos/korinthia-perifereia/', 'Loutraki-Perachora'), GV4, False, dict(hol='Loutraki')),
 ('nafplio', 'Nafplio', 'נפפליו', PE, 37.5673, 22.8016, ('peloponnisos/argolida-perifereia/', 'Nafplio'), GV4, False, dict(hol='Nafplio')),
 ('lamia', 'Lamia', 'למיה', CG, 38.8990, 22.4340, ('sterea-ellada/fthiotida-perifereia/', 'Lamia'), GV4, False, dict(student='Lamia', cap=0.075)),
 ('komotini', 'Komotini', 'קומוטיני', EMT, 41.1220, 25.4060, None, GV4, True, dict(ng='Komotini', cap=0.081)),
 ('xanthi', 'Xanthi (city)', 'קסנתי', EMT, 41.1350, 24.8880, None, GV4, True, dict(ng='Xanthi')),
 ('katerini', 'Katerini', 'קטריני', CM, 40.2720, 22.5020, None, GV4, False, dict(ng='Katerini')),
 ('veria', 'Veria', 'ורויה', CM, 40.5240, 22.2020, None, GV4, False, dict(ng='Veria', cap=0.085)),
 ('drama', 'Drama (city)', 'דרמה', EMT, 41.1500, 24.1470, None, GV4, 'check', dict(ng='Drama', cap=0.081)),
 ('kozani', 'Kozani (city)', 'קוזאני', WM, 40.3010, 21.7890, None, GV4, False, dict(ng='Kozani', cap=0.093)),
 ('trikala', 'Trikala (city)', 'טריקלה', TH, 39.5550, 21.7680, None, GV4, False, dict(thes=1138)),
]
for id_, en, he, reg, lat, lng, indk, gv, bor, ex in CT:
    notes = ''
    if bor == 'check': notes = 'Lies in a regional unit only partly in the border zone; the city itself was not verified as inside or outside it.'
    if id_ == 'chalkida': notes = 'Chalkida is on Evia island (>3,100 inhabitants): EUR 800k likely applies; verify before relying on it.'
    if id_ == 'agios-nikolaos': notes = 'Elounda belongs to the Agios Nikolaos municipality; no Elounda-only price is published.'
    add(id_, en, he, reg, 'city', 'city', lat, lng, gv=gv, border=bor, notes=notes, ind=indk, **ex)

# --- islands
IS = [
 # id, en, he, region, lat, lng, (path,name), isl key, gv, border, extra
 ('rhodes', 'Rhodes', 'רודוס', SA, 36.4349, 28.2176, ('nisia-aigaiou/dodekanisa-perifereia/', 'Rhodes'), 'Rhodes', GV8, True, dict(student='Rhodes')),
 ('kos', 'Kos', 'קוס', SA, 36.8930, 27.2880, ('nisia-aigaiou/dodekanisa-perifereia/', 'Kos'), 'Kos', GV8, True, {}),
 ('patmos', 'Patmos', 'פטמוס', SA, 37.3230, 26.5450, ('nisia-aigaiou/dodekanisa-perifereia/', 'Patmos'), 'Patmos', 'check', True, {}),
 ('kalymnos', 'Kalymnos', 'קלימנוס', SA, 36.9500, 26.9830, ('nisia-aigaiou/dodekanisa-perifereia/', 'Kalimnos'), 'Kalymnos', GV8, True, {}),
 ('leros', 'Leros', 'לרוס', SA, 37.1500, 26.8500, ('nisia-aigaiou/dodekanisa-perifereia/', 'Leros'), 'Leros', GV8, True, {}),
 ('symi', 'Symi', 'סימי', SA, 36.6150, 27.8380, ('nisia-aigaiou/dodekanisa-perifereia/', 'Simi'), 'Symi', GV4, True, {}),
 ('karpathos', 'Karpathos', 'קרפתוס', SA, 35.5070, 27.2130, ('nisia-aigaiou/dodekanisa-perifereia/', 'Karpathos'), None, GV8, True, {}),
 ('astypalaia', 'Astypalaia', 'אסטיפליאה', SA, 36.5500, 26.3500, ('nisia-aigaiou/dodekanisa-perifereia/', 'Astypalea'), 'Astypalaia', GV4, True, {}),
 ('mykonos', 'Mykonos', 'מיקונוס', SA, 37.4467, 25.3289, ('nisia-aigaiou/kyklades-perifereia/', 'Mykonos'), 'Mykonos', GV8, False, {}),
 ('santorini', 'Santorini (Thira)', 'סנטוריני', SA, 36.4166, 25.4320, ('nisia-aigaiou/kyklades-perifereia/', 'Santorini'), 'Santorini', GV8, True, {}),
 ('paros', 'Paros', 'פארוס', SA, 37.0850, 25.1500, ('nisia-aigaiou/kyklades-perifereia/', 'Paros'), 'Paros', GV8, False, {}),
 ('antiparos', 'Antiparos', 'אנטיפארוס', SA, 37.0400, 25.0820, ('nisia-aigaiou/kyklades-perifereia/', 'Antiparos'), 'Antiparos', GV4, False, {}),
 ('naxos', 'Naxos', 'נקסוס', SA, 37.1036, 25.3766, ('nisia-aigaiou/kyklades-perifereia/', 'Naxos'), 'Naxos', GV8, False, {}),
 ('syros', 'Syros', 'סירוס', SA, 37.4440, 24.9420, ('nisia-aigaiou/kyklades-perifereia/', 'Syros'), 'Syros', GV8, False, {}),
 ('tinos', 'Tinos', 'טינוס', SA, 37.5380, 25.1630, ('nisia-aigaiou/kyklades-perifereia/', 'Tinos'), 'Tinos', GV8, False, {}),
 ('milos', 'Milos', 'מילוס', SA, 36.7250, 24.4460, ('nisia-aigaiou/kyklades-perifereia/', 'Milos'), 'Milos', GV8, False, {}),
 ('ios', 'Ios', 'איוס', SA, 36.7330, 25.2830, ('nisia-aigaiou/kyklades-perifereia/', 'Ios'), 'Ios', GV4, False, {}),
 ('sifnos', 'Sifnos', 'סיפנוס', SA, 36.9750, 24.7130, ('nisia-aigaiou/kyklades-perifereia/', 'Sifnos'), 'Sifnos', GV4, False, {}),
 ('folegandros', 'Folegandros', 'פולגנדרוס', SA, 36.6220, 24.9200, ('nisia-aigaiou/kyklades-perifereia/', 'Folegandros'), 'Folegandros', GV4, False, {}),
 ('serifos', 'Serifos', 'סריפוס', SA, 37.1520, 24.5050, ('nisia-aigaiou/kyklades-perifereia/', 'Serifos'), 'Serifos', GV4, False, {}),
 ('kea', 'Kea (Tzia)', 'קאה (צ\'יה)', SA, 37.6350, 24.3270, ('nisia-aigaiou/kyklades-perifereia/', 'Kea'), 'Kea', GV4, False, {}),
 ('kythnos', 'Kythnos', 'קיתנוס', SA, 37.4000, 24.4250, ('nisia-aigaiou/kyklades-perifereia/', 'Kythnos'), 'Kythnos', GV4, False, {}),
 ('andros', 'Andros', 'אנדרוס', SA, 37.8400, 24.9370, ('nisia-aigaiou/kyklades-perifereia/', 'Andros'), 'Andros', GV8, False, {}),
 ('amorgos', 'Amorgos', 'אמורגוס', SA, 36.8300, 25.9000, ('nisia-aigaiou/kyklades-perifereia/', 'Amorgos'), 'Amorgos', GV4, False, {}),
 ('corfu', 'Corfu', 'קורפו', IO, 39.6243, 19.9217, ('nisia-ioniou/nomos-kerkiras-perifereia/', 'Corfu'), 'Corfu', GV8, False, dict(cfnote=1)),
 ('paxoi', 'Paxoi', 'פקסוס', IO, 39.2000, 20.1830, ('nisia-ioniou/nomos-kerkiras-perifereia/', 'Paxoi'), 'Paxoi', GV4, False, {}),
 ('zakynthos', 'Zakynthos', 'זקינתוס', IO, 37.7870, 20.8990, ('nisia-ioniou/', 'Zante'), 'Zakynthos', GV8, False, dict(spi='Ζάκυνθος')),
 ('kefalonia', 'Kefalonia', 'קפלוניה', IO, 38.1750, 20.4900, ('nisia-ioniou/nomos-kefallonias-perifereia/', 'Kefalonia'), 'Kefalonia', GV8, False, {}),
 ('ithaca', 'Ithaca', 'איתקה', IO, 38.3660, 20.7180, ('nisia-ioniou/nomos-kefallonias-perifereia/', 'Ithaki'), 'Ithaca', 'check', False, {}),
 ('lefkada', 'Lefkada', 'לפקדה', IO, 38.8330, 20.7070, ('nisia-ioniou/nomos-lefkadas-perifereia/', 'Lefkada'), 'Lefkada', GV8, False, dict(spi='Ν. Λευκάδας', sq3='Lefkada RU')),
 ('meganisi', 'Meganisi', 'מגניסי', IO, 38.6550, 20.7660, ('nisia-ioniou/nomos-lefkadas-perifereia/', 'Meganisi'), None, GV4, False, {}),
 ('aegina', 'Aegina', 'אגינה', A, 37.7460, 23.4280, (AR, 'Aegina'), None, GV8, False, dict(hol='Aegina')),
 ('hydra', 'Hydra', 'הידרה', A, 37.3490, 23.4640, (AR, 'Hydra'), None, GV8, False, {}),
 ('spetses', 'Spetses', 'ספצס', A, 37.2620, 23.1590, (AR, 'Spetses'), None, GV8, False, dict(hol='Spetses')),
 ('poros', 'Poros', 'פורוס', A, 37.4990, 23.4540, (AR, 'Poros'), None, GV8, False, dict(hol='Poros')),
 ('salamina', 'Salamina', 'סלמינה', A, 37.9640, 23.4960, (AR, 'Salamina'), None, GV8, False, {}),
 ('skiathos', 'Skiathos', 'סקיאתוס', TH, 39.1620, 23.4900, ('nisia-aigaiou/sporades-perifereia/', 'Skiathos'), 'Skiathos', GV8, False, {}),
 ('skopelos', 'Skopelos', 'סקופלוס', TH, 39.1220, 23.7270, ('nisia-aigaiou/sporades-perifereia/', 'Skopelos'), 'Skopelos', GV8, False, {}),
 ('alonnisos', 'Alonnisos', 'אלוניסוס', TH, 39.1480, 23.8640, ('nisia-aigaiou/sporades-perifereia/', 'Alonnisos'), 'Alonnisos', GV4, False, {}),
 ('skyros', 'Skyros', 'סקירוס', CG, 38.9050, 24.5650, ('nisia-aigaiou/sporades-perifereia/', 'Skiros'), 'Skyros', GV4, True, {}),
 ('thassos', 'Thassos', 'תאסוס', EMT, 40.7790, 24.7090, ('macedonia/nomos-kavalas-perifereia/', 'Thasos'), None, GV8, False, {}),
 ('chios', 'Chios', 'כיוס', NA, 38.3680, 26.1360, ('nisia-aigaiou/', 'Chios Prefecture'), 'Chios', GV8, True, dict(spi='Ν. Χίου')),
 ('lesvos', 'Lesvos', 'לסבוס', NA, 39.1080, 26.5550, ('nisia-aigaiou/', 'Lesvos Prefecture'), 'Lesvos', GV8, True, dict(spi='Ν. Λέσβου')),
 ('samos', 'Samos', 'סאמוס', NA, 37.7570, 26.9770, ('nisia-aigaiou/', 'Samos Prefecture'), 'Samos', GV8, True, dict(spi='Ν. Σάμου', cap=0.084)),
 ('samothraki', 'Samothraki', 'סמותרקי', EMT, 40.4750, 25.5300, ('thraki/evros-perifereia/', 'Samothraki'), None, GV4, True, {}),
]
SMALL = {'patmos', 'ithaca'}
for id_, en, he, reg, lat, lng, indk, islk, gv, bor, ex in IS:
    notes = ''
    if gv == GV4: notes = 'Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it.'
    if id_ in SMALL: notes = 'Population close to the 3,100 threshold; golden-visa tier must be checked against the 2021 census.'
    if id_ == 'corfu': notes = 'Corfu main island is not on the border-zone list (the Diapontia islets are).'
    if id_ == 'rhodes': notes = 'Indomio "Rhodes" = Rhodes municipality (whole island).'
    if id_ in ('lesvos', 'chios', 'samos', 'zakynthos', 'lefkada'): notes = 'Island values = whole regional unit.'
    ex = dict(ex); ex.pop('cfnote', None)
    add(id_, en, he, reg, 'island', 'island', lat, lng, gv=gv, border=bor, notes=notes, ind=indk, isl=islk, **ex)

# --- coastal / resort areas
CO = [
 ('kassandra', 'Halkidiki - Kassandra (Kassandra unit)', 'חלקידיקי - קסנדרה', CM, 40.000, 23.450, ('macedonia/chalkidiki-perifereia/', 'Kassandra'), dict(hol='Kassandra')),
 ('kassandra-pallini', 'Halkidiki - Kassandra peninsula north (Pallini unit: Kallithea, Afytos)', 'חלקידיקי - צפון קסנדרה (פליני)', CM, 40.080, 23.430, ('macedonia/chalkidiki-perifereia/', 'Pallini'), {}),
 ('sithonia', 'Halkidiki - Sithonia', 'חלקידיקי - סיתוניה', CM, 40.150, 23.800, ('macedonia/chalkidiki-perifereia/', 'Sithonia'), dict(hol='Sithonia')),
 ('kallikrateia', 'Halkidiki - Kallikrateia', 'חלקידיקי - קליקרטיה', CM, 40.311, 23.064, ('macedonia/chalkidiki-perifereia/', 'Kallikrateia'), dict(hol='Kallikrateia')),
 ('nea-moudania', 'Halkidiki - Nea Moudania', 'חלקידיקי - ניאה מודניה', CM, 40.240, 23.285, ('macedonia/chalkidiki-perifereia/', 'Moudania'), {}),
 ('porto-heli', 'Porto Heli (Kranidi unit, Ermionida)', 'פורטו חלי', PE, 37.317, 23.146, ('peloponnisos/argolida-perifereia/', 'Kranidi'), {}),
 ('ermioni', 'Ermioni', 'ארמיוני', PE, 37.385, 23.247, ('peloponnisos/argolida-perifereia/', 'Ermioni'), {}),
 ('pylos', 'Pylos (Costa Navarino area)', 'פילוס (אזור קוסטה נבארינו)', PE, 36.913, 21.696, ('peloponnisos/messinia-perifereia/', 'Pilos'), {}),
 ('methoni', 'Methoni', 'מתוני', PE, 36.819, 21.705, ('peloponnisos/messinia-perifereia/', 'Methoni'), dict(hol='Methoni')),
 ('koroni', 'Koroni', 'קורוני', PE, 36.795, 21.957, ('peloponnisos/messinia-perifereia/', 'Koroni'), dict(hol='Koroni')),
 ('stoupa', 'Kardamyli - Stoupa (Lefktro unit, Mani)', 'קרדמילי - סטופה', PE, 36.850, 22.255, ('peloponnisos/messinia-perifereia/', 'Lefktros'), dict(hol='Leuktro')),
 ('xylokastro', 'Xylokastro', 'קסילוקסטרו', PE, 38.075, 22.630, ('peloponnisos/korinthia-perifereia/', 'Xilokastro'), dict(hol='Xylokastro')),
 ('pelion-mouresi', 'Pelion - Mouresi (Tsagarada)', 'פליון - מורסי (צגרדה)', TH, 39.390, 23.170, ('thessalia/magnisia-perifereia/', 'Mouresi'), dict(hol='Mouresi')),
 ('pelion-milies', 'Pelion - Milies', 'פליון - מיליס', TH, 39.329, 23.152, ('thessalia/magnisia-perifereia/', 'Milies'), dict(hol='Milies')),
 ('pelion-zagora', 'Pelion - Zagora', 'פליון - זגורה', TH, 39.447, 23.102, ('thessalia/magnisia-perifereia/', 'Zagora'), dict(hol='Zagora')),
 ('pelion-argalasti', 'Pelion - Argalasti (south Pelion)', 'פליון - ארגלסטי', TH, 39.226, 23.219, ('thessalia/magnisia-perifereia/', 'Argalasti'), {}),
 ('pelion-portaria', 'Pelion - Portaria', 'פליון - פורטריה', TH, 39.388, 22.996, ('thessalia/magnisia-perifereia/', 'Portaria'), {}),
 ('eretria', 'Evia - Eretria', 'אוויה - ארטריה', CG, 38.395, 23.793, ('sterea-ellada/evia-perifereia/', 'Eretria'), dict(hol='Eretria')),
 ('karystos', 'Evia - Karystos', 'אוויה - קריסטוס', CG, 38.015, 24.419, ('sterea-ellada/evia-perifereia/', 'Karistos'), {}),
 ('syvota', 'Syvota (Thesprotia)', 'סיבוטה', EP, 39.407, 20.238, None, dict(hol='Syvota')),
 ('nafpaktos', 'Nafpaktos', 'נאפקטוס', WG, 38.392, 21.828, None, dict(hol='Nafpaktos')),
]
for id_, en, he, reg, lat, lng, indk, ex in CO:
    gv = GV4; bor = True if id_ == 'syvota' else False
    note = ''
    if reg == CG: gv = 'check'; note = 'On Evia island (>3,100 inhabitants): EUR 800k likely applies; verify.'
    if id_.startswith('kassandra'): note = 'Kassandra municipality = Kassandra + Pallini units; Indomio publishes both separately.'
    if id_ == 'pylos': note = 'Engel & Völkers 2026 gives Pylos/Gialova 3,000-6,000 EUR/m2 (holiday homes, broker range).'
    if id_ == 'porto-heli': note = 'Porto Heli lies in the Kranidi municipal unit; Engel & Völkers 2026: 4,000-6,000, prime up to 12,000+.'
    add(id_, en, he, reg, 'area', 'resort_area', lat, lng, gv=gv, border=bor, notes=note, ind=indk, **ex)

# ----------------------------------------------------------------- resolve values
def ind_rec(key):
    if not key: return None
    path, name = key
    r = IND.get((path, name))
    if r is None and name == '__top__':
        return None
    return r

def rent_ok(sale, rent, ryoy):
    if rent is None: return False, None
    if rent < 4.0: return False, 'Indomio rent below 4 EUR/m2: implausible small-sample value, not used'
    if ryoy is not None and abs(ryoy) > 1.0: return False, 'Indomio rent yoy beyond +/-100%: small-sample value, not used'
    if sale and rent * 12 / sale < 0.02: return False, 'Indomio rent implies gross yield under 2%: seasonal/small-sample value, not used'
    return True, None

out = []
missing_ind = []
for p in P:
    s = p['src']
    sale_c, rent_c, ypub = [], [], []
    notes = [p['notes']] if p['notes'] else []
    # Indomio
    r = ind_rec(s.get('ind'))
    if s.get('ind') and r is None: missing_ind.append((p['id'], s.get('ind')))
    if r:
        u = r['url']
        if r['sale'] is not None:
            sale_c.append(dict(key='indomio', value=r['sale'], yoy=r['sale_yoy'], **src('indomio', url=u)))
        ok, why = rent_ok(r['sale'], r['rent'], r['rent_yoy'])
        if ok:
            rent_c.append(dict(key='indomio', value=r['rent'], yoy=r['rent_yoy'], **src('indomio', url=u)))
        elif r['rent'] is not None:
            notes.append(f"{why} (published {r['rent']} EUR/m2, yoy {r['rent_yoy']}).")
    # Spitogatos Q3 2026
    k = s.get('sq3')
    if k and k in SQ3:
        sv, sy, rv, ry = SQ3[k]
        if sv: sale_c.append(dict(key='spit_q3', value=float(sv), yoy=sy, **src('spit_q3')))
        if rv: rent_c.append(dict(key='spit_q3', value=float(rv), yoy=ry, **src('spit_q3')))
        if sv is None and sy is not None: notes.append(f'Spitogatos Q3 2026: sale asking price {sy*100:+.1f}% yoy (level not published).')
        if rv is None and ry is not None: notes.append(f'Spitogatos Q3 2026: rent {ry*100:+.1f}% yoy (level not published).')
    # Spitogatos SPI Q2 2026
    k = s.get('spi')
    if k and k in SPI:
        if 'sale' in SPI[k]:
            d = SPI[k]['sale']; sale_c.append(dict(key='spi_q2', value=d['value'], yoy=d['yoy'], prev_year=d['prev'], **src('spi_q2')))
        if 'rent' in SPI[k]:
            d = SPI[k]['rent']
            if k == 'Χαλκιδική':
                notes.append(f"Spitogatos SPI Q2 2026 rent {d['value']} (Q2 2025 {d['prev']}, {d['yoy']*100:+.1f}%) looks like small-sample volatility; not used.")
            else:
                rent_c.append(dict(key='spi_q2', value=d['value'], yoy=d['yoy'], prev_year=d['prev'], **src('spi_q2')))
        if 'rent_blog' in SPI[k]:
            rent_c.append(dict(key='spit_q2_blog', value=SPI[k]['rent_blog']['value'], yoy=None, **src('spit_q2_blog')))
    # Spitogatos Q2 blog lists
    k = s.get('sq2')
    if k and k in SQ2:
        sv, sy, rv = SQ2[k]
        if sv: sale_c.append(dict(key='spit_q2_blog', value=float(sv), yoy=sy, **src('spit_q2_blog')))
        if rv: rent_c.append(dict(key='spit_q2_blog', value=float(rv), yoy=None, **src('spit_q2_blog')))
    # xe.gr
    k = s.get('xe')
    if k and k in XE:
        if 'sale' in XE[k]:
            d = XE[k]['sale']; sale_c.append(dict(key='xe', value=d['value'], yoy=d['yoy'], prev_year=d['prev'], size_bands_2026=d['bands'], listings=d['listings'], **src('xe')))
        if 'rent' in XE[k]:
            d = XE[k]['rent']; rent_c.append(dict(key='xe', value=d['value'], yoy=d['yoy'], prev_year=d['prev'], size_bands_2026=d['bands'], listings=d['listings'], **src('xe')))
    # islands report
    k = s.get('isl')
    if k and k in ISL:
        sale_c.append(dict(key='spit_isl', value=float(ISL[k]), yoy=None, **src('spit_isl')))
    # holiday homes
    k = s.get('hol')
    if k and k in HOL:
        sale_c.append(dict(key='spit_hol', value=float(HOL[k][0]), yoy=HOL[k][1], **src('spit_hol')))
    # North Greece Q1 2026
    k = s.get('ng')
    if k and k in NG:
        sale_c.append(dict(key='spit_ng', value=float(NG[k][0]), yoy=None, **src('spit_ng')))
        rent_c.append(dict(key='spit_ng', value=float(NG[k][1]), yoy=None, **src('spit_ng')))
    if s.get('thes'):
        sale_c.append(dict(key='spit_thes', value=float(s['thes']), yoy=None, **src('spit_thes')))
    if s.get('epir'):
        sale_c.append(dict(key='spit_epir', value=float(s['epir'][0]), yoy=None, **src('spit_epir')))
        rent_c.append(dict(key='spit_epir', value=float(s['epir'][1]), yoy=None, **src('spit_epir')))
    k = s.get('student')
    if k and k in STUDENT:
        rent_c.append(dict(key='spit_student', value=STUDENT[k][0], yoy=STUDENT[k][1], **src('spit_student')))
    k = s.get('remax_rent')
    if k and k in REMAX_RENT:
        rent_c.append(dict(key='remax_rent', value=REMAX_RENT[k][0], yoy=REMAX_RENT[k][1], **src('remax_rent')))
    k = s.get('numbeo')
    if k and k in NUMBEO:
        nb = NUMBEO[k]
        sale_c.append(dict(key='numbeo', value=nb[0], yoy=None, note=f'city centre; outside centre {nb[1]}', **src('numbeo', url=f'https://www.numbeo.com/cost-of-living/in/{k}')))
        ypub.append(yp('numbeo', nb[3], note=f'outside centre {nb[4]}'))
    if s.get('cap'):
        ypub.append(yp('spit_cap_2025', s['cap']))
    # special cases
    if p['id'] == 'lagonisi':
        sale_c.append(dict(key='remax_sale_ath', value=2000.0, yoy=None, note='homes older than 5 years; new-build (<=5 years) 3,000', **src('remax_sale_ath')))
    if p['id'] == 'peraia':
        sale_c.append(dict(key='remax_sale_thes', value=1400.0, yoy=0.167, note='homes older than 5 years; new-build 2,000 (+8.1%)', **src('remax_sale_thes')))
    if p['id'] == 'ath-centre':
        sale_c.append(dict(key='numbeo', value=NUMBEO['Athens'][0], yoy=None, note=f"city centre; outside centre {NUMBEO['Athens'][1]}", **src('numbeo', url='https://www.numbeo.com/cost-of-living/in/Athens')))
        ypub.append(yp('numbeo', NUMBEO['Athens'][3], note=f"outside centre {NUMBEO['Athens'][4]}"))
    if p['id'] == 'thess-municipality':
        sale_c.append(dict(key='numbeo', value=NUMBEO['Thessaloniki'][0], yoy=None, note=f"city centre; outside centre {NUMBEO['Thessaloniki'][1]}", **src('numbeo', url='https://www.numbeo.com/cost-of-living/in/Thessaloniki')))
        ypub.append(yp('numbeo', NUMBEO['Thessaloniki'][3], note=f"outside centre {NUMBEO['Thessaloniki'][4]}"))
    # published yields
    PY = {
     'ath-centre': [('spit_ind_q2', 0.0577), ('spit_ptr_2025', 0.0566), ('gpg_city', 0.0552, 'Athens average')],
     'piraeus': [('spit_ind_q2', 0.0487), ('spit_ptr_2025', 0.0496)], 'piraeus-suburbs': [('spit_ptr_2025', 0.0498)],
     'kifisia': [('spit_ind_q2', 0.0417)], 'chalandri': [('spit_ind_q2', 0.0407)],
     'glyfada': [('spit_ind_q2', 0.0349), ('spit_ptr_2025', 0.0351)], 'ath-south': [('spit_ptr_2025', 0.0386)],
     'ath-north': [('spit_ptr_2025', 0.0417)], 'ath-west': [('spit_ptr_2025', 0.0504)], 'ath-east': [('spit_ptr_2025', 0.0469)],
     'evosmos': [('spit_ind_q2', 0.0452)], 'thermi': [('spit_ind_q2', 0.0406)], 'kalamaria': [('spit_ind_q2', 0.0378)],
     'thess-centre': [('spit_ind_q2', 0.0471), ('gpg', 0.0471)], 'toumba': [('spit_ind_q2', 0.0421), ('gpg', 0.0406)],
     'kolonaki': [('gpg', 0.0508, '1-bed; 2-bed 3.39%')], 'pagrati': [('gpg', 0.0467, '1-bed; 2-bed 3.92%')],
     'kypseli': [('gpg', 0.0611, '1-bed; 2-bed 4.80%')], 'neos-kosmos': [('gpg', 0.0488, '1-bed; 2-bed 4.25%')],
     'patisia': [('gpg', 0.0678, '1-bed; 2-bed 5.87%')], 'ano-poli': [('gpg', 0.0514, '1-bed; 2-bed 4.72%'), ('spit_cap_2025', 0.058)],
     'thess-municipality': [('gpg_city', 0.0419, 'Thessaloniki average')], 'patras': [('gpg_city', 0.0468)],
     'heraklion': [('gpg_city', 0.0425)], 'volos': [('gpg_city', 0.0420)], 'kavala': [('gpg_city', 0.0344)],
     'vardaris': [('spit_cap_2025', 0.059)], '40-ekklisies': [('spit_cap_2025', 0.054)], 'neapoli-thess': [('spit_cap_2025', 0.073)],
     'ampelokipoi-thess': [('spit_cap_2025', 0.067)], 'stavroupoli': [('spit_cap_2025', 0.066)], 'menemeni': [('spit_cap_2025', 0.055)],
     'sykies': [('spit_cap_2025', 0.053)], 'serres': [('spit_cap_2025', 0.076)],
    }
    for t in PY.get(p['id'], []):
        ypub.append(yp(t[0], t[1], t[2] if len(t) > 2 else None))

    # choose primary: Indomio first (one method, one month, widest coverage), then Spitogatos Q3, SPI Q2, xe, others
    order = ['indomio', 'spit_q3', 'spi_q2', 'spit_q2_blog', 'xe', 'spit_isl', 'spit_hol', 'spit_ng', 'spit_epir', 'spit_thes', 'remax_sale_ath', 'remax_sale_thes', 'numbeo']
    rorder = ['indomio', 'spit_q3', 'spi_q2', 'spit_q2_blog', 'xe', 'spit_ng', 'spit_epir', 'remax_rent', 'spit_student']
    def pick(c, order):
        for k in order:
            for x in c:
                if x['key'] == k: return x
        return None
    ps, pr = pick(sale_c, order), pick(rent_c, rorder)
    rec = dict(id=p['id'], name_en=p['name_en'], name_he=p['name_he'], region=p['region'], type=p['type'], level=p['level'],
               lat=p['lat'], lng=p['lng'], coords_note='approximate (town or area centre, set by hand)')
    def put(prefix, x):
        rec[f'{prefix}_eur_m2'] = x['value'] if x else None
        rec[f'{prefix}_period'] = x['period'] if x else None
        rec[f'{prefix}_yoy'] = x.get('yoy') if x else None
        rec[f'{prefix}_provider'] = x['provider'] if x else None
        rec[f'{prefix}_kind'] = x['kind'] if x else None
        rec[f'{prefix}_source'] = x['url'] if x else None
        rec[f'{prefix}_source_date'] = x['source_date'] if x else None
        rec[f'{prefix}_retrieved'] = RETR if x else None
    put('sale', ps)
    put('rent', pr)
    if rec['rent_eur_m2'] is not None:
        pass
    # yield: only when sale and rent come from the same provider and period
    if ps and pr and ps['key'] == pr['key']:
        rec['gross_yield'] = round(pr['value'] * 12 / ps['value'], 4)
        rec['yield_source'] = f"computed: {pr['provider']} asking rent x 12 / asking sale price, {pr['period']} (gross, before costs and vacancy)"
    else:
        rec['gross_yield'] = None
        rec['yield_source'] = None
    rec['yield_published'] = ypub
    rec['sale_alt'] = [dict((kk, vv) for kk, vv in x.items() if kk != 'key') for x in sale_c if x is not ps]
    rec['rent_alt'] = [dict((kk, vv) for kk, vv in x.items() if kk != 'key') for x in rent_c if x is not pr]
    rec['gv_tier'] = p['gv']
    rec['border_permit'] = p['border']
    rec['str_freeze'] = p['strf']
    if p['strf']:
        rec['str_freeze_note'] = STR_NOTE
    rec['notes'] = ' '.join(n for n in notes if n)
    out.append(rec)

# ----------------------------------------------------------------- other blocks
facts = json.load(open(os.path.join(BASE, '..', '2026-10-22-greece', 'facts.json'), encoding='utf-8'))
bog = facts['prices']['bog_index']
def annual(series):
    yrs = {}
    for k, v in series.items():
        y = k[:4]; yrs.setdefault(y, []).append(v)
    return {y: round(sum(v) / len(v), 2) for y, v in yrs.items() if len(v) == 4}

national = dict(
    indomio=dict(sale_eur_m2=2790, sale_yoy=0.0473, sale_prev_year=2664, rent_eur_m2=10.68, rent_yoy=0.0379, rent_prev_year=10.29,
                 sale_change_3y=0.143, sale_change_5y=0.385, rent_change_3y=0.135, rent_change_5y=0.439,
                 sale_low='2024-12: 2,526', **src('indomio')),
    spitogatos_q3_2026=dict(sale_yoy=0.057, sale_yoy_q3_2025=0.100, rent_yoy=0.0, rent_yoy_q3_2025=0.072,
                            attica=dict(sale_yoy=0.050, rent_yoy=0.050, sale_yoy_q3_2025=0.088, rent_yoy_q3_2025=0.048),
                            thessaloniki=dict(sale_yoy=0.067, rent_yoy=0.053, sale_yoy_q3_2025=0.110, rent_yoy_q3_2025=0.077),
                            note='levels for the whole country not published in the release', **src('spit_q3')),
    spitogatos_q2_2026=dict(sale_yoy=0.061, rent_yoy=0.013, attica_sale_yoy=0.053, thessaloniki_sale_yoy=0.077, rest_of_greece_sale_yoy=0.071,
                            **src('spi_q2')),
    bank_of_greece=dict(index_2026_q2=114.25, base='2007=100', yoy=bog['yoy_2026_q2'], kind='valuation-based apartment price index (all banks)',
                        source='facts.json (../2026-10-22-greece) from bankofgreece.gr', release='2026-09-15 (provisional)', next_release='Q3 2026 not yet published (usually late November)'),
)

price_by_type = dict(
    new_vs_old_bog=dict(yoy_2026_q2_new_up_to_5y=bog['yoy_2026_q2']['new_up_to_5y'], yoy_2026_q2_old=bog['yoy_2026_q2']['old'],
                        index_2026_q2_new=bog['quarterly_series_2016_2026']['whole_country_new']['2026-Q2'],
                        index_2026_q2_old=bog['quarterly_series_2016_2026']['whole_country_old']['2026-Q2'],
                        source='Bank of Greece apartment price index (via facts.json)'),
    new_vs_old_spitogatos_2025=dict(
        unit='EUR/m2 asking, year 2025', sale={
            'Athens Centre': dict(old=2250, new=4000), 'Athens East': dict(old=2077, new=3195), 'Athens North': dict(old=2800, new=4495),
            'Athens South': dict(old=3226, new=5122), 'Athens West': dict(old=1888, new=3333), 'Piraeus': dict(old=2364, new=3723),
            'Piraeus suburbs': dict(old=1856, new=3235), 'Thessaloniki municipality': dict(old=2455, new=3190), 'Thessaloniki suburbs': dict(old=1554, new=2667)},
        rent={
            'Athens Centre': dict(old=11.3, new=15.5), 'Athens East': dict(old=8.9, new=10.3), 'Athens North': dict(old=11.3, new=15.2),
            'Athens South': dict(old=12.6, new=18.8), 'Athens West': dict(old=8.7, new=11.5), 'Piraeus': dict(old=10.1, new=12.0),
            'Piraeus suburbs': dict(old=8.6, new=11.6), 'Thessaloniki municipality': dict(old=10.0, new=13.4), 'Thessaloniki suburbs': dict(old=7.5, new=9.7)},
        new_build_share_of_sale_stock_athens_municipality=0.07, new_build_share_of_rent_stock_athens_municipality=0.03,
        new_build_sale_stock_split_attica_2025={'South': 0.44, 'North': 0.22, 'Centre': 0.11, 'West': 0.10, 'East': 0.06, 'Piraeus suburbs': 0.03, 'Piraeus': 0.02},
        provider='Spitogatos', source='https://www.spitogatos.gr/blog/energeiaki-apodosi-etos-kataskevis-katoikies-times-enoikiasi-pwlisi',
        source_date='2026-03-31', retrieved=RETR, raw='raw/types/age_1.png, age_2.png, age_5.png'),
    energy_class_spitogatos_2025=dict(
        unit='EUR/m2 asking, 2025 (yoy in brackets)', sale={
            'Athens Centre': dict(high=3529, mid=2412, low=1915), 'Athens East': dict(high=2949, mid=2075, low=1949),
            'Athens North': dict(high=4286, mid=2787, low=2667), 'Athens South': dict(high=4925, mid=3238, low=2481),
            'Athens West': dict(high=3133, mid=1944, low=1584), 'Piraeus': dict(high=3450, mid=2526, low=2000),
            'Piraeus suburbs': dict(high=3130, mid=1964, low=1531), 'Thessaloniki municipality': dict(high=3000, mid=2500, low=2027),
            'Thessaloniki suburbs': dict(high=2460, mid=1585, low=1200)},
        rent={
            'Athens Centre': dict(high=12.6, mid=11.3, low=10.6), 'Athens East': dict(high=10.0, mid=8.8, low=8.8),
            'Athens North': dict(high=12.5, mid=11.0, low=10.9), 'Athens South': dict(high=15.6, mid=12.3, low=10.7),
            'Athens West': dict(high=9.6, mid=8.6, low=8.2), 'Piraeus': dict(high=11.5, mid=10.0, low=9.4),
            'Piraeus suburbs': dict(high=9.4, mid=8.6, low=7.8), 'Thessaloniki municipality': dict(high=11.0, mid=10.0, low=9.5),
            'Thessaloniki suburbs': dict(high=8.1, mid=7.4, low=7.0)},
        classes='high = A+, A, B+, B; mid and low as defined by Spitogatos',
        provider='Spitogatos', source='https://www.spitogatos.gr/blog/energeiaki-apodosi-etos-kataskevis-katoikies-times-enoikiasi-pwlisi',
        source_date='2026-03-31', retrieved=RETR, raw='raw/types/age_3.png, age_4.png'),
    new_vs_old_remax_transactions_2025=dict(
        unit='EUR/m2 completed sales 2025', rows={'East Thessaloniki': dict(old=1840, new=2800, old_yoy=0.031, new_yoy=0.023),
                                                 'West Thessaloniki': dict(old=1306, new=2107, old_yoy=0.037, new_yoy=0.045),
                                                 'Peraia': dict(old=1400, new=2000, old_yoy=0.167, new_yoy=0.081),
                                                 'Lagonisi': dict(old=2000, new=3000)},
        provider='RE/MAX Greece', sources=[S['remax_sale_thes']['url'], S['remax_sale_ath']['url']], source_date='2026-05-15', retrieved=RETR),
    size_bands_xe_q3_2026={k: dict(sale=v['sale']['bands'] if 'sale' in v else None, rent=v['rent']['bands'] if 'rent' in v else None) for k, v in XE.items()},
    size_bands_note='xe.gr Q3 2026 asking EUR/m2 by size: up to 80 m2 / 81-120 m2 / 121 m2+, 50 largest markets (Greek names). Source https://www.xe.gr/property/times-akiniton',
    apartment_vs_house=dict(note='No provider publishes EUR/m2 for apartments vs detached houses per area in 2026. AADE transfer-values registry 2025: 21,354 apartments worth EUR 2.25 bn and 4,278 houses worth EUR 451.11m were posted (a subset of all deals).',
                            source='https://www.in.gr/2026/01/13/economy/allaksan-xeria-akinita-42-dis-eyro-2025/', source_date='2026-01-13', retrieved=RETR),
)

spi_history = dict(
    note='No year-by-year Spitogatos SPI EUR/m2 series by region for 2016-2025 is published in open form (searched: press, Spitogatos blog, SPI page, Datawrapper chart behind the SPI page = demand map only). Official 10-year history = Bank of Greece index below.',
    bank_of_greece_annual_avg_2007eq100={name: annual(series) for name, series in bog['quarterly_series_2016_2026'].items()},
    bank_of_greece_2026_h1={name: dict(q1=series.get('2026-Q1'), q2=series.get('2026-Q2')) for name, series in bog['quarterly_series_2016_2026'].items()},
    bank_of_greece_change_2016q2_2026q2=bog['change_2016q2_to_2026q2'],
    bank_of_greece_source='facts.json (../2026-10-22-greece), Bank of Greece apartment price index, release 2026-09-15',
    ecb_resr_greece_annual_2025eq100=dict(values={'2014': 58.96, '2015': 55.98, '2016': 54.65, '2017': 54.10, '2018': 55.07, '2019': 59.05, '2020': 61.70,
                                                  '2021': 66.40, '2022': 74.32, '2023': 84.62, '2024': 92.36, '2025': 100.0},
                                          source='https://data-api.ecb.europa.eu/service/data/RESR/A.GR........?format=csvdata&startPeriod=2014',
                                          retrieved=RETR, raw='raw/market/ecb_RESR_A_GR.csv', note='ECB RESR series of the Bank of Greece flats index, rebased 2025=100 (revised)'),
    spitogatos_yoy_national=dict(values={'2025 (year)': 0.096, '2025-Q2': 0.097, '2025-Q3': 0.100, '2026-Q1': 0.079, '2026-Q2': 0.061, '2026-Q3': 0.057},
                                 sources=['https://www.in.gr/2026/01/13/economy/allaksan-xeria-akinita-42-dis-eyro-2025/', S['spi_q2']['url'], S['spit_q3']['url']], retrieved=RETR),
    spitogatos_attica_2025_yoy=dict(value=0.081, source='https://www.in.gr/2026/01/13/economy/allaksan-xeria-akinita-42-dis-eyro-2025/', source_date='2026-01-13'),
    spitogatos_islands_2021_vs_2026=dict(unit='EUR/m2 asking, Q2', values={'Aegean islands': dict(q2_2021=2071, q2_2026=2941), 'Ionian islands': dict(q2_2021=1719, q2_2026=2531),
                                                                            'Crete': dict(q2_2021=1500, q2_2026=2250)}, **src('spit_isl')),
    spitogatos_north_greece_2022_to_q1_2026=dict(unit='cumulative change in asking price', values={
        'Macedonia (excl. Thessaloniki) sale': 0.537, 'Macedonia rent': 0.155, 'Thrace sale': 0.383, 'Thrace rent': 0.328,
        'Alexandroupoli sale': 0.513, 'Alexandroupoli rent': 0.440, 'Kavala rent': 0.317, 'Komotini sale': 0.385, 'Komotini rent': 0.292,
        'Xanthi sale': 0.453, 'Xanthi rent': 0.212, 'Katerini sale': 0.233, 'Katerini rent': 0.332, 'Serres sale': 0.196, 'Serres rent': 0.310,
        'Veria sale': 0.255, 'Drama sale': 0.324, 'Kozani sale': 0.040}, **src('spit_ng')),
    spitogatos_regional_long_run=[dict(area='Thessaly', change=0.353, span='2019 to Q3 2025', value_2025=1273, **src('spit_thes')),
                                  dict(area='Epirus', value_2025=1538, yoy=0.073, rent_2025=8.9, rent_2019=6.1, **src('spit_epir')),
                                  dict(area='Peloponnese', change=0.307, span='2019-2024', source='https://www.newmoney.gr/wp-content/uploads/2025/03/Spitogatos-Data-Report_Πελοπόννησος-1-1.pdf', source_date='2025-03', retrieved=RETR)],
    indomio_multi_year=dict(national_sale_change=dict(y1=0.047, y3=0.143, y5=0.385, since_2020_start=0.483),
                            national_rent_change=dict(y1=0.038, y3=0.135, y5=0.439, since_2020_start=0.519), **src('indomio')),
    geoaxis_mykonos_typical_median=dict(values={'2017': 2141, '2026': 2969}, source='https://www.powergame.gr/akinita/1399097/fotia-oi-times-stis-polyteleis-exochikes-katoikies-eos-kai-30-000-evro-to-t-m-o-chartis-tis-agoras/', source_date='2026-08-05', retrieved=RETR),
)

transactions = dict(
    elstat_notarial_property_sales=dict(unit='notarial acts, all property types', values={'2014': 43443, '2015': 54631, '2016': 60540, '2017': 69826, '2018': 79532,
        '2019': 96662, '2020': 74769, '2021': 104746, '2022': 112283, '2023': 122123, '2024': 145765},
        sources=['https://www.taxheaven.gr/attachment/21838 (ELSTAT, 2024-11-27, years 2014-2023)',
                 'https://www.naftemporiki.gr/finance/economy/2037531/akinita-agorapolisies-se-pro-krisis-epipeda-kai-ektoxeysi-dekaetias-stoys-pleistiriasmoys/ (2025-11-23, year 2024)'],
        note='2025 not yet published by ELSTAT', retrieved=RETR),
    aade_transfer_declarations=[
        dict(period='2024', count=225000, value_eur=23.0e9, note='declarations (one per co-owner/right), all property types; ~EUR 1.5 bn mortgage-funded',
             source='https://www.newmoney.gr/roh/palmos-oikonomias/oikonomia/i-aade-xeskonizi-45-000-metavivasis-akiniton-sto-mikroskopio-ta-simvolea/', source_date='2025-05-16'),
        dict(period='2025', count=223000, value_eur=None, note='myPROPERTY sale declarations; transfer-tax revenue EUR 607.93m (2024: 656.49m)',
             source='https://www.tovima.gr/2026/03/05/finance/akinita-posa-allaksan-xeria-o-xartis-ton-xryson-metavivaseon/', source_date='2026-03-05'),
        dict(period='2025', count=None, value_eur=23.5e9, note='AADE total value of properties that changed hands (all types)',
             source='https://greekreporter.com/2026/07/20/foreign-investment-greece-real-estate-2019-2025/', source_date='2026-07-20'),
        dict(period='2026-H1', count=112320, value_eur=12.0e9, note='H1 2025: 108,228 declarations; avg value EUR 115k (H1 2025 110k); ~EUR 1.3 bn mortgage-funded; ~EUR 550m from foreign investors',
             source='https://www.powergame.gr/forologia/1385920/akinita-axias-12-dis-evro-allaxan-cheria-to-a-examino/', source_date='2026-07-13')],
    transfer_values_registry_2025=dict(properties=41743, value_eur=4.2e9, apartments=21354, apartments_value_eur=2.25e9, houses=4278, houses_value_eur=451.11e6,
        plots=6566, commercial=3394, parking=1958, avg_value_eur=100770, athens_city_sales=5816, athens_city_value_eur=626e6,
        note='only contracts posted to the registry (subset of the market); the URL slug "42" means 4.2 bn',
        source='https://www.in.gr/2026/01/13/economy/allaksan-xeria-akinita-42-dis-eyro-2025/', source_date='2026-01-13', retrieved=RETR),
    foreign_direct_investment_real_estate_eur_m=dict(values={'2019': 1449, '2021': 1176, '2022': 1975, '2023': 2130, '2024': 2750, '2025': 2050, '2026-Q1': 511.6},
        cumulative_2019_2025=12400, cumulative_2002_2018=3380,
        sources={'2019,2021,2022': 'https://www.tanea.gr/2023/03/18/economy/akinita-rekor-20etias-stis-ksenes-ependyseis-sta-2-dis-eyro-oi-eisroes-to-2022/',
                 '2023,2024': 'https://greekcitytimes.com/?p=507769', '2025,cumulative': 'https://greekreporter.com/2026/07/20/foreign-investment-greece-real-estate-2019-2025/',
                 '2026-Q1': 'https://www.powergame.gr/akinita/1375247/tte-me-chamiloteri-tachytita-i-koursa-ton-timon-akiniton-afxanontai-oi-xenes-ependyseis/'},
        note='Bank of Greece net FDI inflows into real estate (press-reported). 2020 narrow series not found. 2025 Jan-Sep: 1,465 (-23.9%).', retrieved=RETR),
    foreign_buyers=dict(
        share_of_value_2026_h1=dict(value=round(550 / 12000, 4), note='computed: ~EUR 550m foreign / EUR 12 bn total (AADE, H1 2026)', source='https://www.powergame.gr/forologia/1385920/akinita-axias-12-dis-evro-allaxan-cheria-to-a-examino/'),
        fdi_share_of_total_fdi_2025=dict(value=0.166, source='https://greekreporter.com/2026/07/20/foreign-investment-greece-real-estate-2019-2025/'),
        by_nationality=[dict(nationality='Turkey', year=2025, eur_m=214), dict(nationality='Turkey', year=2024, eur_m=293), dict(nationality='Turkey', year=2023, eur_m=107),
                        dict(nationality='Israel', year='2002-2022 cumulative', eur_m=253), dict(nationality='Hong Kong', year='2002-2022 cumulative', eur_m=1293),
                        dict(nationality='Germany', year='2002-2022 cumulative', eur_m=606), dict(nationality='China', year='2002-2022 cumulative', eur_m=524)],
        ranking_remax_2025='Attica and Thessaloniki: Israelis most active foreign buyers, then Turks, Lebanese, Chinese, Ukrainians; rest of Greece: Germans lead (RE/MAX Hellas, via alfavita.gr 2026-01-12)',
        golden_visa=dict(initial_applications={'2023': 8477, '2024': 9411}, permits_granted_2025=9479, applications_2026_jan_apr=1677, applications_2025_jan_apr=3507,
                         israel_approvals_9m_2025=544, israel_approvals_9m_2024=296),
        sources=['https://www.tovima.com/finance/greek-real-estate-continues-to-attract-turkish-capital/', 'https://www.tanea.gr/2023/03/18/economy/akinita-rekor-20etias-stis-ksenes-ependyseis-sta-2-dis-eyro-oi-eisroes-to-2022/',
                 'https://www.alfavita.gr/koinonia/502563_xenoi-ependytes-stin-ellada-israilinoi-kai-toyrkoi-protostatoyn-stis-agores', 'https://greekcitytimes.com/?p=507769',
                 'https://www.powergame.gr/akinita/1375247/tte-me-chamiloteri-tachytita-i-koursa-ton-timon-akiniton-afxanontai-oi-xenes-ependyseis/'],
        retrieved=RETR),
)

build_cost = dict(
    elstat_new_residential_input_cost_index=dict(period='2026-Q2', yoy=0.040, materials_yoy=0.043, labour_yoy=0.036, qoq=0.017, q1_2026_yoy=0.028,
        source='https://www.forin.gr/articles/article/91582/elstat-aukshsh-3-shmeiwse-o-genikos-deikths-timwn-ergwn-kataskeuhs-newn-katoikiwn-to-b-trimhno-efetos', source_date='2026-07-23'),
    elstat_new_residential_output_price_index=dict(period='2026-Q2', yoy=0.030, qoq=0.007, q1_2026_yoy=0.025, source='same as above'),
    eur_per_m2_press=dict(value_min=1900, note='"often 1,900 EUR/m2 or more" depending on quality; no named industry body; excludes land, VAT, permits and developer margin unless stated',
        period='2026-Q1', source='https://www.newmoney.gr/roh/palmos-oikonomias/oikonomia/ikodomi-rali-se-ergatika-ke-domika-ilika-nees-afxisis-sto-kostos-kataskevis-gia-katikies/', source_date='2026-05-07', confidence='low'),
    building_permits_may_2026=dict(permits=2669, permits_yoy=-0.008, floor_area_m2=585896, floor_area_yoy=0.046, rolling_12m_permits_yoy=0.09, rolling_12m_area_yoy=0.14,
        source='https://www.forin.gr/articles/article/92001/elstat-meiwsh-36-shmeiwse-o-ogkos-ths-idiwtikhs-oikodomikhs-drasthriothtas-to-maio-tou-2026', source_date='2026-08-28'),
    gaps='No TEE or PEDMEDE 2026 EUR/m2 construction-cost figure found; ELSTAT Q3 2026 index not yet released.',
    retrieved=RETR,
)

luxury = dict(
    note='Prime/luxury EUR/m2. Broker ranges (Engel & Völkers) and listing medians (GEOAXIS) are NOT comparable with the all-stock averages in places[].',
    rows=[
     dict(place='Mykonos', low=16790, high=30000, what='GEOAXIS luxury median asking / top listing (+4.94% yoy); typical home median 2,969', source='https://www.powergame.gr/akinita/1399097/fotia-oi-times-stis-polyteleis-exochikes-katoikies-eos-kai-30-000-evro-to-t-m-o-chartis-tis-agoras/', source_date='2026-08-05'),
     dict(place='Mykonos', low=7500, high=12000, what='Engel & Völkers 2026 holiday-home range', source='https://ered.gr/en/engel-volkers-geographic-breakdown-and-price-trends-in-the-second-home-market/', source_date='2026-06-05'),
     dict(place='Santorini', low=13943, high=25000, what='GEOAXIS luxury median asking / top listing (+4.90%); typical 2,363', source='https://www.powergame.gr/akinita/1399097/fotia-oi-times-stis-polyteleis-exochikes-katoikies-eos-kai-30-000-evro-to-t-m-o-chartis-tis-agoras/', source_date='2026-08-05'),
     dict(place='Santorini', low=4500, high=8000, what='Engel & Völkers 2026 range; Oia and Imerovigli caldera named as premium (no figure)', source='https://www.powergame.gr/akinita/1388720/exochikes-katoikies-o-chartis-ton-timon-se-aigaio-kai-ionio-pou-ependyoun-oi-xenoi/', source_date='2026-07-17'),
     dict(place='Paros', low=10026, high=20000, what='GEOAXIS luxury median asking / top listing (+5.55%); typical 2,384', source='https://www.powergame.gr/akinita/1399097/fotia-oi-times-stis-polyteleis-exochikes-katoikies-eos-kai-30-000-evro-to-t-m-o-chartis-tis-agoras/', source_date='2026-08-05'),
     dict(place='Paros', low=5500, high=10000, what='Engel & Völkers 2026 range', source='https://ered.gr/en/engel-volkers-geographic-breakdown-and-price-trends-in-the-second-home-market/', source_date='2026-06-05'),
     dict(place='Antiparos', low=6800, high=10200, what='Engel & Völkers 2026 range', source='https://ered.gr/en/engel-volkers-geographic-breakdown-and-price-trends-in-the-second-home-market/', source_date='2026-06-05'),
     dict(place='Kea', low=6549, high=16000, what='GEOAXIS luxury median / top listing; E&V 3,500-7,000', source='https://www.powergame.gr/akinita/1399097/fotia-oi-times-stis-polyteleis-exochikes-katoikies-eos-kai-30-000-evro-to-t-m-o-chartis-tis-agoras/', source_date='2026-08-05'),
     dict(place='Vouliagmeni (Athens Riviera)', low=8500, high=12000, what='Engel & Völkers 2026 average sale range; iconic seafront homes can exceed 20,000', source=S['ev']['url'], source_date='2026-05-15'),
     dict(place='Glyfada', low=5300, high=9000, what='Engel & Völkers 2026 range', source=S['ev']['url'], source_date='2026-05-15'),
     dict(place='Kolonaki', low=6086, high=None, what='Engel & Völkers 2026 average (Syntagma 5,638)', source=S['ev']['url'], source_date='2026-05-15'),
     dict(place='Palaio Psychiko / Filothei', low=None, high=10000, what='Engel & Völkers 2026: new-build up to 10,000', source=S['ev']['url'], source_date='2026-05-15'),
     dict(place='The Ellinikon - Riviera Tower', low=14036, high=None, what='average pre-sale price, 171 units, EUR 626m (AXIA data on Lamda)', source='https://www.powergame.gr/akinita/1092241/poso-polei-i-lamda-tis-polyteleis-katoikies-sto-elliniko/', source_date='2025-09-12'),
     dict(place='The Ellinikon - Cove Residences / Cove Villas / Park Rise', low=10048, high=11359, what='average pre-sale prices (AXIA)', source='https://www.powergame.gr/akinita/1092241/poso-polei-i-lamda-tis-polyteleis-katoikies-sto-elliniko/', source_date='2025-09-12'),
     dict(place='The Ellinikon - Little Athens (Mainstream)', low=7575, high=8873, what='average pre-sale prices (AXIA); overall Ellinikon 7,500-14,000', source='https://www.powergame.gr/akinita/1092241/poso-polei-i-lamda-tis-polyteleis-katoikies-sto-elliniko/', source_date='2025-09-12'),
     dict(place='Porto Heli / Kosta', low=4000, high=12000, what='Engel & Völkers 2026: 4,000-6,000, prime 12,000+', source='https://ered.gr/en/engel-volkers-geographic-breakdown-and-price-trends-in-the-second-home-market/', source_date='2026-06-05'),
     dict(place='Messinia - Pylos / Gialova (Costa Navarino area)', low=3000, high=6000, what='Engel & Völkers 2026 range (no resort-specific figure)', source='https://ered.gr/en/engel-volkers-geographic-breakdown-and-price-trends-in-the-second-home-market/', source_date='2026-06-05'),
     dict(place='Halkidiki (beachfront)', low=8000, high=14000, what='Engel & Völkers 2026 range', source='https://ered.gr/en/engel-volkers-geographic-breakdown-and-price-trends-in-the-second-home-market/', source_date='2026-06-05'),
     dict(place='Corfu', low=3200, high=3800, what='Engel & Völkers 2026; seafront mansions sometimes above 8,500', source='https://www.powergame.gr/akinita/1388720/exochikes-katoikies-o-chartis-ton-timon-se-aigaio-kai-ionio-pou-ependyoun-oi-xenoi/', source_date='2026-07-17'),
     dict(place='Hydra', low=5000, high=7500, what='Engel & Völkers 2026', source='https://www.powergame.gr/akinita/1388720/exochikes-katoikies-o-chartis-ton-timon-se-aigaio-kai-ionio-pou-ependyoun-oi-xenoi/', source_date='2026-07-17'),
     dict(place='Paxoi', low=4200, high=9500, what='Engel & Völkers 2026: 4,200-5,000, top villas above 9,500', source='https://www.powergame.gr/akinita/1388720/exochikes-katoikies-o-chartis-ton-timon-se-aigaio-kai-ionio-pou-ependyoun-oi-xenoi/', source_date='2026-07-17'),
     dict(place='Lefkada', low=3800, high=7500, what='Engel & Völkers 2026: 3,800-3,900, luxury up to 7,500', source='https://www.powergame.gr/akinita/1388720/exochikes-katoikies-o-chartis-ton-timon-se-aigaio-kai-ionio-pou-ependyoun-oi-xenoi/', source_date='2026-07-17'),
     dict(place='Kefalonia', low=3000, high=7500, what='Engel & Völkers 2026: 3,000-3,600, up to 7,500', source='https://www.powergame.gr/akinita/1388720/exochikes-katoikies-o-chartis-ton-timon-se-aigaio-kai-ionio-pou-ependyoun-oi-xenoi/', source_date='2026-07-17'),
     dict(place='Elounda (Crete)', low=None, high=None, what='no published EUR/m2 found; Indomio Agios Nikolaos municipality (incl. Elounda) 3,901 (Sep 2026)', source=None, source_date=None),
    ],
    highest_area_averages_sep_2026_indomio={k: v for k, v in [('Vouliagmeni', 7710), ('Mykonos', 7633), ('Antiparos', 7420), ('Hydra', 7188), ('Meganisi', 6303),
                                                              ('Voula', 6198), ('Plaka', 6116), ('Syntagma', 6067), ('Elliniko', 5745), ('Paros', 5656)]},
    retrieved=RETR,
)

numbeo = {c: dict(price_m2_centre=v[0], price_m2_outside=v[1], rent_1bed_centre_eur_month=v[2], gross_yield_centre=v[3], gross_yield_outside=v[4],
                  source=f'https://www.numbeo.com/cost-of-living/in/{c} and https://www.numbeo.com/property-investment/in/{c}', last_update='2026-10-22', retrieved=RETR,
                  note='crowd-sourced, small samples (Chania 17 contributors, Patras 20)') for c, v in NUMBEO.items()}

policy = dict(
    golden_visa=dict(thresholds=facts['golden_visa']['thresholds'], law=facts['golden_visa']['law'],
                     tag_rule='EUR 800k: Attica, Thessaloniki regional unit, Mykonos, Santorini, islands above 3,100 inhabitants; EUR 400k: elsewhere; "mixed" = unit spans both; "check" = population near the threshold or island status disputed (Evia)',
                     island_population_note='island populations used for tagging are approximate (2021 census, from general knowledge) and were not checked one by one'),
    border_permit=facts['border_zone_permit_non_eu'],
    str_freeze=facts['short_term_rental']['registration_freeze'],
)

result = dict(
    _meta=dict(title='Greece residential property price list (asking prices) for nad-lan.co.il', built=RETR, retrieved=RETR,
               method='Primary value per place = Indomio.gr September 2026 asking price (one provider, one month, widest coverage, sale + rent + yoy). '
                      'Where Indomio has no figure, the next source in this order: Spitogatos Q3 2026, Spitogatos SPI Q2 2026, Spitogatos Q2 2026 blog, xe.gr Q3 2026 (computed weighted mean), '
                      'Spitogatos islands / holiday-homes / regional reports, RE/MAX, Numbeo. All other values kept in sale_alt / rent_alt. '
                      'Asking prices are typically above transaction prices. gross_yield is computed only when sale and rent come from the same provider and month.',
               rent_filter='Indomio rents dropped as implausible when < 4 EUR/m2, yoy beyond +/-100%, or implying < 2% gross yield (seasonal islands, tiny samples).',
               yoy_units='fractions (0.047 = +4.7%)', companion='prices.md', builder='build_prices.py',
               raw='raw/ (indomio/, neighbourhoods/, regions/, market/, types/, numbeo/, xe_q3_2026.json, agent_*.json)'),
    national=national,
    places=out,
    spi_history=spi_history,
    transactions=transactions,
    build_cost=build_cost,
    luxury=luxury,
    price_by_type=price_by_type,
    numbeo_cities=numbeo,
    policy=policy,
)
json.dump(result, open(os.path.join(BASE, 'prices.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ----------------------------------------------------------------- checks printed for the builder
print('places', len(out))
print('with sale', sum(1 for r in out if r['sale_eur_m2']), 'with rent', sum(1 for r in out if r['rent_eur_m2']), 'with yield', sum(1 for r in out if r['gross_yield']))
print('missing indomio keys', missing_ind)
print('primary providers', {k: sum(1 for r in out if r['sale_provider'] == k) for k in set(r['sale_provider'] for r in out)})
print('no sale:', [r['id'] for r in out if not r['sale_eur_m2']])
