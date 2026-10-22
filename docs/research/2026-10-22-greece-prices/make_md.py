# -*- coding: utf-8 -*-
"""Render prices.md from prices.json.  Run: python -I -X utf8 make_md.py"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(BASE, 'prices.json'), encoding='utf-8'))
P = d['places']

AB = {'Indomio.gr': 'IND', 'Spitogatos': 'SQ3', 'Spitogatos SPI': 'SPI', 'xe.gr (Chrysi Efkairia)': 'XE',
      'Spitogatos (islands report)': 'ISL', 'Spitogatos (holiday homes report)': 'HOL', 'Spitogatos (North Greece report)': 'NG',
      'Spitogatos (Thessaly report)': 'THS', 'Spitogatos (Epirus report)': 'EPI', 'Spitogatos (student housing)': 'STU',
      'RE/MAX Greece': 'RMX', 'Numbeo (crowd-sourced)': 'NUM'}
def ab(x):
    if not x: return ''
    a = AB.get(x['provider'], x['provider'])
    if a == 'SQ3' and x.get('period') == '2026-Q2': a = 'SQ2'
    return a
def f0(v): return '' if v is None else f'{v:,.0f}'
def f2(v): return '' if v is None else f'{v:.2f}'.rstrip('0').rstrip('.') if v % 1 else f'{v:.0f}'
def pc(v): return '' if v is None else f'{v*100:+.1f}%'
def yl(v): return '' if v is None else f'{v*100:.1f}%'
def gv(v):
    if v == 800000: return '800k'
    if v == 400000: return '400k'
    return v or ''
def flag(v):
    if v is True: return 'yes'
    if v is False: return 'no'
    return v or ''

def table(rows):
    out = ['| Place | עברית | Sale €/m² | yoy | Rent €/m²/mo | yoy | Gross yield | Source (period) | Other sale values | GV | Border permit | STR freeze |',
           '|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|']
    for p in rows:
        prim = dict(provider=p['sale_provider'], period=p['sale_period']) if p['sale_provider'] else None
        src = f"{ab(prim)} {p['sale_period'] or ''}" if prim else 'not published'
        if p['rent_provider'] and p['rent_provider'] != p['sale_provider']:
            src += f"; rent {ab(dict(provider=p['rent_provider'], period=p['rent_period']))} {p['rent_period']}"
        alts = '; '.join(f"{ab(a)} {f0(a['value'])}" for a in p['sale_alt'])
        out.append(f"| {p['name_en']} | {p['name_he']} | {f0(p['sale_eur_m2'])} | {pc(p['sale_yoy'])} | {f2(p['rent_eur_m2']) if p['rent_eur_m2'] else ''} | {pc(p['rent_yoy'])} | {yl(p['gross_yield'])} | {src} | {alts} | {gv(p['gv_tier'])} | {flag(p['border_permit'])} | {flag(p['str_freeze'])} |")
    return '\n'.join(out)

L = []
w = L.append
w('# Greece property price list: asking prices by place (retrieved 22 October 2026)\n')
w('Companion of `prices.json` (built by `build_prices.py`, rendered by `make_md.py`). Every number has its provider, period and URL in the JSON; this page shows the short code.\n')
w('## How to read it\n')
w('- **Primary value = Indomio.gr, September 2026** (one provider, one month, sale + rent + yoy for almost every place: 248 of 263 priced places). Where Indomio has nothing, the next source is used (order: Spitogatos Q3 2026, Spitogatos SPI Q2 2026, Spitogatos Q2 blog, xe.gr Q3 2026, Spitogatos regional reports, RE/MAX, Numbeo). Other values stay in "Other sale values" and in `sale_alt` / `rent_alt`.')
w('- These are **asking prices** (listings). Deeds and bank valuations are lower; the Bank of Greece index is the official trend.')
w('- **Gross yield** = asking rent x 12 / asking sale price, same provider and month only. It is before costs, tax, vacancy and furnishing.')
w('- Indomio island rents below 4 €/m², with yoy beyond ±100%, or implying under 2% yield (Kos, Milos, Sifnos, Serifos, Kythnos, Skiathos, Skopelos, Methoni and others) are tiny seasonal samples and were **dropped**, not replaced.')
w('- **GV** = golden-visa minimum (800k: Attica, Thessaloniki regional unit, Mykonos, Santorini, islands over 3,100 inhabitants; 400k elsewhere; "mixed" = unit spans both; "check" = island population near 3,100 or Evia status unverified). **Border permit** = prior permit needed for non-EU buyers (Law 1892/1990); "partial" = only part of the unit; "check" = city not verified. **STR freeze** = no new short-term-rental registrations until 31 Dec 2026 (Athens districts 1-3, Thessaloniki 1st community).')
w('- Coordinates in the JSON are approximate (set by hand to the town or area centre).\n')
w('**Source codes:** IND = Indomio Sep 2026 (https://www.indomio.gr/en/agora-akiniton/), SQ3 = Spitogatos Q3 2026 press release 22.10.2026 (newmoney.gr / insider.gr), SPI = Spitogatos SPI Q2 2026 (https://www.spitogatos.gr/deiktis-timon), SQ2 = Spitogatos Q2 2026 blog 4.8.2026, XE = xe.gr Q3 2026 (https://www.xe.gr/property/times-akiniton, listing-weighted mean of 3 size bands computed by us), ISL = Spitogatos islands Q2 2026 (16.9.2026), HOL = Spitogatos holiday homes Q2 2026 (24.9.2026), NG = Spitogatos North Greece Q1 2026 (3.7.2026), THS / EPI = Spitogatos Thessaly / Epirus reports (Q3 2025), STU = Spitogatos student housing Q2 2026, RMX = RE/MAX (closed deals, not asking), NUM = Numbeo (crowd-sourced).\n')

n = d['national']
w('## Whole country\n')
w('| Measure | Value | Period | Source |\n|---|---|---|---|')
w(f"| Indomio asking sale | {n['indomio']['sale_eur_m2']:,} €/m² ({pc(n['indomio']['sale_yoy'])}; Sep 2025 {n['indomio']['sale_prev_year']:,}) | 2026-09 | IND |")
w(f"| Indomio asking rent | {n['indomio']['rent_eur_m2']} €/m²/month ({pc(n['indomio']['rent_yoy'])}) | 2026-09 | IND |")
w(f"| Indomio sale change 3 / 5 years | +14.3% / +38.5% | to 2026-09 | IND |")
w(f"| Spitogatos asking sale yoy | +5.7% (Q3 2025: +10.0%); Attica +5.0%, Thessaloniki +6.7% | 2026-Q3 | SQ3 |")
w(f"| Spitogatos asking rent yoy | 0.0% (Q3 2025: +7.2%); Attica +5.0%, Thessaloniki +5.3% | 2026-Q3 | SQ3 |")
w(f"| Spitogatos Q2 sale yoy | +6.1%; Attica +5.3%, Thessaloniki +7.7%, rest of Greece +7.1% | 2026-Q2 | SPI |")
w(f"| Bank of Greece apartment index | 114.25 (2007=100), +5.5% yoy; new +6.2%, old +5.0% | 2026-Q2 | BoG (facts.json) |\n")

groups = [
 ('Administrative regions and provider groupings', lambda p: p['level'] in ('admin_region', 'provider_grouping')),
 ('Regional units (prefectures)', lambda p: p['level'] == 'regional_unit'),
 ('Attica: sub-areas', lambda p: p['region'] == 'Attica' and p['level'] == 'sub_area'),
 ('Athens: neighbourhoods inside the Municipality of Athens', lambda p: p['region'] == 'Attica' and p['level'] == 'neighbourhood'),
 ('Attica: municipalities and Piraeus districts', lambda p: p['region'] == 'Attica' and p['level'] == 'municipality'),
 ('Thessaloniki: city, neighbourhoods and suburbs', lambda p: p['region'] == 'Central Macedonia' and p['level'] in ('sub_area', 'neighbourhood', 'municipality')),
 ('Cities', lambda p: p['type'] == 'city'),
 ('Islands', lambda p: p['type'] == 'island'),
 ('Resort and coastal areas (Halkidiki, Peloponnese coast, Pelion, Evia)', lambda p: p['level'] == 'resort_area'),
]
for title, fn in groups:
    rows = [p for p in P if fn(p)]
    rows.sort(key=lambda p: -(p['sale_eur_m2'] or 0))
    w(f'## {title} ({len(rows)})\n')
    w(table(rows) + '\n')
    notes = [(p['name_en'], p['notes']) for p in rows if p['notes']]
    if notes:
        w('Notes: ' + ' '.join(f'**{a}:** {b}' for a, b in notes) + '\n')

# rankings
priced = [p for p in P if p['sale_eur_m2']]
w('## Rankings (primary values)\n')
w('**10 most expensive places:** ' + '; '.join(f"{p['name_en']} {f0(p['sale_eur_m2'])}" for p in sorted(priced, key=lambda p: -p['sale_eur_m2'])[:10]) + '.\n')
w('**10 cheapest places:** ' + '; '.join(f"{p['name_en']} {f0(p['sale_eur_m2'])}" for p in sorted(priced, key=lambda p: p['sale_eur_m2'])[:10]) + '.\n')
w('**Biggest asking-price risers (yoy):** ' + '; '.join(f"{p['name_en']} {pc(p['sale_yoy'])}" for p in sorted([p for p in priced if p['sale_yoy'] is not None], key=lambda p: -p['sale_yoy'])[:15]) + '. Leros, Skyros, Milos and Samothraki are thin island samples.\n')
w('**Fallers:** ' + '; '.join(f"{p['name_en']} {pc(p['sale_yoy'])}" for p in sorted([p for p in priced if p['sale_yoy'] is not None], key=lambda p: p['sale_yoy'])[:8]) + '.\n')
yl_ = [p for p in priced if p['gross_yield'] and p['level'] not in ('admin_region', 'provider_grouping')]
w('**Highest computed gross yields:** ' + '; '.join(f"{p['name_en']} {yl(p['gross_yield'])}" for p in sorted(yl_, key=lambda p: -p['gross_yield'])[:10]) + '.\n')
w('**Lowest computed gross yields:** ' + '; '.join(f"{p['name_en']} {yl(p['gross_yield'])}" for p in sorted(yl_, key=lambda p: p['gross_yield'])[:10]) + '.\n')

# price by type
t = d['price_by_type']
w('## Price by type\n')
w(f"- **New vs old, Bank of Greece (Q2 2026):** new flats (up to 5 years) +{t['new_vs_old_bog']['yoy_2026_q2_new_up_to_5y']*100:.1f}% yoy, older +{t['new_vs_old_bog']['yoy_2026_q2_old']*100:.1f}%; index new {t['new_vs_old_bog']['index_2026_q2_new']:.1f} vs old {t['new_vs_old_bog']['index_2026_q2_old']:.1f} (2007=100).")
nv = t['new_vs_old_spitogatos_2025']
w(f"- **New vs older, Spitogatos asking 2025** (source {nv['source']}, 31.3.2026). New-builds were about 7% of homes for sale and 3% of rentals in the Municipality of Athens.\n")
w('| Area | Older sale €/m² | New sale €/m² | Premium | Older rent | New rent | Premium |\n|---|---:|---:|---:|---:|---:|---:|')
for k in nv['sale']:
    s, r = nv['sale'][k], nv['rent'][k]
    w(f"| {k} | {s['old']:,} | {s['new']:,} | {pc(s['new']/s['old']-1)} | {r['old']} | {r['new']} | {pc(r['new']/r['old']-1)} |")
ec = t['energy_class_spitogatos_2025']
w('\n**Energy class, Spitogatos asking 2025** (high = A+ to B):\n')
w('| Area | High sale | Mid sale | Low sale | High rent | Mid rent | Low rent |\n|---|---:|---:|---:|---:|---:|---:|')
for k in ec['sale']:
    s, r = ec['sale'][k], ec['rent'][k]
    w(f"| {k} | {s['high']:,} | {s['mid']:,} | {s['low']:,} | {r['high']} | {r['mid']} | {r['low']} |")
w('\n**Size bands, xe.gr Q3 2026 asking €/m²** (up to 80 m² / 81-120 m² / 121 m²+), selected markets:\n')
w('| Market | Sale ≤80 | Sale 81-120 | Sale 121+ | Rent ≤80 | Rent 81-120 | Rent 121+ |\n|---|---:|---:|---:|---:|---:|---:|')
for k, v in t['size_bands_xe_q3_2026'].items():
    s, r = v['sale'] or {}, v['rent'] or {}
    sv = list(s.values()); rv = list(r.values())
    if len(sv) == 3 and len(rv) == 3:
        w(f"| {k} | {sv[0]:,.0f} | {sv[1]:,.0f} | {sv[2]:,.0f} | {rv[0]} | {rv[1]} | {rv[2]} |")
w('\n- **Transactions, new vs older (RE/MAX closed sales 2025):** East Thessaloniki 1,840 vs 2,800; West Thessaloniki 1,306 vs 2,107; Peraia 1,400 vs 2,000; Lagonisi 2,000 vs 3,000 €/m².')
w(f"- **Apartment vs house:** {t['apartment_vs_house']['note']}\n")

# history
h = d['spi_history']
w('## Ten-year history\n')
w(h['note'] + '\n')
ba = h['bank_of_greece_annual_avg_2007eq100']
yrs = sorted(ba['whole_country_all'])
w('**Bank of Greece apartment price index, annual average (2007=100):**\n')
w('| Series | ' + ' | '.join(yrs) + ' | 2026-Q2 |\n|---|' + '---:|' * (len(yrs) + 1))
for k in ba:
    w(f"| {k} | " + ' | '.join(f"{ba[k].get(y, ''):.1f}" if ba[k].get(y) else '' for y in yrs) + f" | {h['bank_of_greece_2026_h1'][k]['q2']:.1f} |")
c = h['bank_of_greece_change_2016q2_2026q2']
w(f"\nChange Q2 2016 to Q2 2026: whole country {pc(c['whole_country'])}, Athens {pc(c['athens'])}, Thessaloniki {pc(c['thessaloniki'])}, other cities {pc(c['other_cities'])}, other areas {pc(c['other_areas'])}. Trough 2017-Q3; 2026-Q2 is a series high.\n")
w('- Spitogatos national asking-price yoy: 2025 year +9.6%; Q2 2025 +9.7%; Q3 2025 +10.0%; Q1 2026 +7.9%; Q2 2026 +6.1%; Q3 2026 +5.7%. Attica 2025 +8.1%.')
w('- Spitogatos islands Q2 2021 to Q2 2026: Aegean 2,071 to 2,941; Ionian 1,719 to 2,531; Crete 1,500 to 2,250 €/m².')
w('- Spitogatos North Greece 2022 to Q1 2026: Macedonia (excl. Thessaloniki) sale +53.7%, Thrace +38.3%, Alexandroupoli +51.3%, Xanthi +45.3%, Komotini +38.5%, Drama +32.4%, Veria +25.5%, Katerini +23.3%, Serres +19.6%, Kozani +4.0%.')
w('- Thessaly asking price +35.3% from 2019 to Q3 2025 (1,273 €/m²); Peloponnese +30.7% 2019-2024; Epirus 1,538 €/m² in 2025 (+7.3%), rent 6.1 (2019) to 8.9 €/m².')
w('- Indomio whole country: sale +14.3% in 3 years, +38.5% in 5 years, +48.3% since early 2020; rent +43.9% in 5 years.')
w('- GEOAXIS Mykonos typical holiday home: 2,141 (2017) to 2,969 €/m² (2026).\n')

tr = d['transactions']
w('## Market activity\n')
w('| Year | ELSTAT notarial property sales (all property types) |\n|---|---:|')
for y, v in tr['elstat_notarial_property_sales']['values'].items():
    w(f'| {y} | {v:,} |')
w('\n2025 not yet published by ELSTAT. Other measures (all property types):\n')
for x in tr['aade_transfer_declarations']:
    cnt = '' if x['count'] is None else '{:,} declarations; '.format(x['count'])
    val = '' if x['value_eur'] is None else 'EUR {:.1f} bn; '.format(x['value_eur'] / 1e9)
    w(f"- AADE {x['period']}: {cnt}{val}{x['note']} ({x['source']}, {x['source_date']}).")
r = tr['transfer_values_registry_2025']
w(f"- Transfer-values registry 2025: {r['properties']:,} properties, EUR 4.2 bn; {r['apartments']:,} apartments (EUR 2.25 bn), {r['houses']:,} houses (EUR 451m); Athens city {r['athens_city_sales']:,} sales (EUR 626m). Subset of the market ({r['source']}).")
fd = tr['foreign_direct_investment_real_estate_eur_m']
w('- Bank of Greece foreign direct investment into real estate (EUR m): ' + ', '.join(f'{k} {v:,}' for k, v in fd['values'].items()) + f"; 2019-2025 total {fd['cumulative_2019_2025']:,} (2002-2018: {fd['cumulative_2002_2018']:,}).")
fb = tr['foreign_buyers']
w(f"- Foreign buyers' share: about {fb['share_of_value_2026_h1']['value']*100:.1f}% of transaction value in H1 2026 (EUR 550m of 12 bn, computed); property was 16.6% of all FDI in 2025. No official share by count is published.")
w(f"- {fb['ranking_remax_2025']}. Turkish buyers: EUR 293m (2024), 214m (2025). Israel 2002-2022 cumulative: EUR 253m.")
w(f"- Golden visa: initial applications 8,477 (2023), 9,411 (2024); 9,479 permits granted in 2025; Jan-Apr 2026 applications 1,677 vs 3,507 a year earlier; Israeli approvals 544 in 9M 2025 vs 296.\n")

b = d['build_cost']
w('## Construction cost\n')
w(f"- ELSTAT input-cost index for new homes, Q2 2026: +4.0% yoy (materials +4.3%, labour +3.6%), +1.7% on the quarter; Q1 2026 +2.8% ({b['elstat_new_residential_input_cost_index']['source']}, 23.7.2026).")
w('- ELSTAT output-price index for new residential construction, Q2 2026: +3.0% yoy.')
w(f"- Euro per m² to build: press says \"often 1,900 €/m² or more\" depending on quality (newmoney.gr, 7.5.2026; no named industry body; low confidence).")
w('- Building permits May 2026: 2,669 (-0.8%), 585,896 m² (+4.6%); rolling 12 months permits +9%, floor area +14%.')
w(f"- Gap: {b['gaps']}\n")

lx = d['luxury']
w('## Luxury and prime\n')
w(lx['note'] + '\n')
w('| Place | Low €/m² | High €/m² | What | Source date |\n|---|---:|---:|---|---|')
for x in lx['rows']:
    w(f"| {x['place']} | {f0(x['low'])} | {f0(x['high'])} | {x['what']} | {x['source_date'] or ''} |")
w('\nHighest area averages in the list (Indomio Sep 2026): ' + '; '.join(f'{k} {v:,}' for k, v in lx['highest_area_averages_sep_2026_indomio'].items()) + '.\n')

w('## Numbeo city centre vs outside (crowd-sourced, low confidence)\n')
w('| City | Centre €/m² | Outside €/m² | 1-bed rent centre €/month | Yield centre | Yield outside |\n|---|---:|---:|---:|---:|---:|')
for k, v in d['numbeo_cities'].items():
    w(f"| {k} | {v['price_m2_centre']:,.0f} | {v['price_m2_outside']:,.0f} | {v['rent_1bed_centre_eur_month']:,.0f} | {yl(v['gross_yield_centre'])} | {yl(v['gross_yield_outside'])} |")
w('\nNumbeo has enough data only for these five Greek cities (last update 22.10.2026; Chania 17 and Patras 20 contributors).\n')

# conflicts
w('## Conflicts between sources (difference above 15% for sale, 20% for rent)\n')
w('Rule used: the map and tables use Indomio September 2026 everywhere it exists, so that places are compared on one method and one month. The second value is kept in the JSON and should be shown in the tooltip. A systematic pattern: Indomio is 15-30% above Spitogatos on the islands and in some regional units (different listing pools and averaging), close to Spitogatos in Athens and Thessaloniki.\n')
w('| Place | Used | Other value | Why the difference / what to do |\n|---|---|---|---|')
WHY = {
 'ru-heraklion': 'Spitogatos itself disagrees (SPI 1,917 vs islands report 2,200 for the same quarter). Use Indomio 2,150, which sits between them.',
 'ru-lasithi': 'Indomio 2,678 vs Spitogatos 1,944: Indomio sample weighted to Agios Nikolaos/Elounda listings. Show both.',
 'ru-corfu': 'Indomio 3,032 vs Spitogatos 2,417 (+25%). Different listing pools; show both, label Indomio as the map value.',
 'ath-centre': 'Numbeo 3,616 is crowd-sourced "city centre" (a narrower, pricier zone); Spitogatos 2,500 (Q2) and xe 3,029 bracket Indomio 2,844.',
 'peraia': 'RE/MAX 1,400 is completed sales of older homes in Peraia only; Indomio 2,352 is all asking listings in Thermaikos municipality.',
 'heraklion': 'xe 2,813 is a listing-weighted mean of size bands; Numbeo 3,197 is crowd-sourced. Indomio 2,351 used.',
 'kolonaki': 'RE/MAX 14.0 is closed lettings; asking rents (Indomio 18.83, Spitogatos 18.0) are higher. Expected gap.',
 'koukaki': 'RE/MAX 9.7 closed lettings vs Indomio 14.92 asking: Koukaki asking rents reflect short-let style listings; show both.',
 'paxoi': 'Indomio 5,495 vs Spitogatos 3,846: tiny island sample; treat as indicative.',
}
for p in priced:
    for a in p['sale_alt']:
        if a['value'] and abs(a['value'] / p['sale_eur_m2'] - 1) > 0.15:
            w(f"| {p['name_en']} (sale) | {ab(dict(provider=p['sale_provider'], period=p['sale_period']))} {f0(p['sale_eur_m2'])} | {ab(a)} {f0(a['value'])} ({a['period']}) | {WHY.get(p['id'], 'Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip.')} |")
    for a in p['rent_alt']:
        if p['rent_eur_m2'] and a['value'] and abs(a['value'] / p['rent_eur_m2'] - 1) > 0.20:
            why = WHY.get(p['id'])
            if not why:
                why = 'Student-housing rents are small units (higher €/m²); not comparable.' if a['provider'].endswith('(student housing)') else (
                      'Closed lettings (RE/MAX) run below asking rents.' if a['provider'] == 'RE/MAX Greece' else 'Different provider / quarter; keep Indomio for the map.')
            w(f"| {p['name_en']} (rent) | {ab(dict(provider=p['rent_provider'], period=p['rent_period']))} {f2(p['rent_eur_m2'])} | {ab(a)} {f2(a['value'])} ({a['period']}) | {why} |")
w('| Halkidiki (rent) | IND 12.38 | SPI 21.11 (Q2 2026; Q2 2025 32.14) | SPI value swings 34% in a year: small sample. Not used. |')
w('| Spitogatos holiday homes text vs table | table yoy used | Porto Rafti +14.7% (text) vs +15.1% (table); Palaia Fokaia +14.3% vs +7.8%; Poros ">20%" vs +7.8%; Spetses "+10%" vs +15.1% | The blog text and its own table disagree; table values kept. |')
w('| Lefkada (sale) | IND 3,816 | SQ3 3,500 (RU), SPI 3,302 (Q2) | Prices moved between Q2 and Q3; Spitogatos Q3 lists the regional unit at 3,500. |\n')

w('## Could not find\n')
for g in [
 'One published figure for six administrative regions: Central Macedonia, East Macedonia & Thrace, West Macedonia, Western Greece, North Aegean, South Aegean (providers publish regional units or their own groupings). Not computed, to avoid invented weights.',
 'Spitogatos Q3 2026 full tables per regional unit and per Athens/Thessaloniki sub-area: only top-5 / bottom-5 lists were released on 22.10.2026; the SPI page still shows Q2 2026.',
 'A year-by-year Spitogatos SPI €/m² series 2016-2025 by region (the official Bank of Greece index is used for history instead).',
 'Island rents for Kos, Milos, Sifnos, Serifos, Kythnos, Skiathos, Skopelos, Patmos, Antiparos, Ios, Folegandros, Amorgos, Paxoi, Ithaca, Meganisi, Hydra, Spetses, Symi, Karpathos, Astypalaia, Alonnisos, Skyros, Samothraki (no reliable long-let asking rent).',
 'Elounda-only, Oia-only, Ekali/Kifisia prime and north-east Corfu prime €/m²; Knight Frank / Savills / Sotheby\'s Greece price levels.',
 'Construction cost per m² from TEE or PEDMEDE for 2026 (only a press "1,900 €/m² or more" figure).',
 'Residential-only transaction counts for 2025 and a foreign-buyer share by number of deals; Bank of Greece FDI 2026 H1.',
 'Apartment vs detached-house €/m² per area; Bank of Greece and ELSTAT Q3 2026 releases (not yet published).',
 'Lagonisi asking price (only RE/MAX 2025 deals), Porto Rafti in Indomio (xe used), Komotini/Xanthi/Katerini/Veria/Drama/Kozani city-level Indomio figures (Spitogatos Q1 2026 used), Trikala city after Q3 2025.',
 'Golden-visa tags for small islands rely on approximate 2021 populations; Evia\'s treatment (island vs mainland) and whether Ioannina, Serres and Drama cities fall inside the partial border zone were not verified.',
]:
    w(f'- {g}')
w('\n## Evidence files\n')
w('- `raw/indomio/indomio_capture_2026-10-22.txt` and `raw/neighbourhoods/browser_capture_indomio_spitogatos_2026-10-22.txt` (Indomio pages read in the browser; the site blocks scripts).')
w('- `raw/regions/spi_q2_2026_deiktis-timon.txt` (Spitogatos SPI table), `raw/xe_q3_2026.json` (xe.gr parsed by `parse_xe.py`), `raw/notes-1.md` (Spitogatos Q3/Q2/islands/holiday tables), `raw/types/age_*.png` (new vs old, energy class), `raw/market/` (ELSTAT, BoG, AADE, luxury), `raw/numbeo/`, `raw/agent_regions.json`, `raw/agent_neigh.json`.')

open(os.path.join(BASE, 'prices.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('written', len(L), 'lines')
