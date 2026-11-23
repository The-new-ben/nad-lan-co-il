# 07 - Exact sources of the transit map v1 (/transit/, /en/transit/), HAD-816

Downloaded 23.11.2026 to D:/Scratch/transit-map-had816/raw (not in git). Builder: scripts/had816/build_transit_data.py -> plugins/nadlan-config/assets/transit/transit-data.json.

| What | Source | Dataset date | Licence |
|---|---|---|---|
| Israel Railways stations (78: 72 passenger, 6 under construction) | https://data.gov.il/dataset/rail_stat (SHP, ITM) | YEARMONTH 202607, metadata 12.7.2026 | CC-BY |
| Rail tracks | https://data.gov.il/dataset/rail_freq_2026 (94 segments; frequency fields not shown) | 23.6.2026 | CC-BY |
| Light rail lines (TA: Red running, Red extension planned, Purple "ביצוע", Green "תכנון מפור" in the 2021 row) | https://data.gov.il/dataset/lrt_line | 22.3.2026 | CC-BY |
| Light rail stations (Purple 46, Green 61, Red extension 4) | https://data.gov.il/dataset/lrt_stat | 16.11.2026 | CC-BY |
| Metro lines M1 (north+south), M2, M3 | https://data.gov.il/dataset/metro_line | 8.1.2026 | CC-BY |
| Metro stations (109: M1 62, M2 22, M3 25), positions of 12.2021 | https://data.gov.il/dataset/metro_stat | 24.11.2024 | CC-BY |
| Which Red Line (34) and Israel Railways (70) stations run today + English names | https://gtfs.mot.gov.il/gtfsfiles/israel-public-transportation.zip (Last-Modified 22.11.2026 17:31 GMT, 139,351,097 bytes) | 22.11.2026 | MoT GTFS terms (exact wording not readable by agents: gov.il 403) |
| English names of Green / Purple stations; Green Line works sections (works 2020-2023 on several sections) | https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer layers 764, 766, 423, 761 | date_import 20.3.2025 | Tel Aviv-Yafo open data (credit) |
| Projects | plugins/nadlan-config/assets/deals/projects.json (site catalogue, 15.11.2026); city-centre placeholder points (shared by 3+ projects) left out; private sandbox pages left out | 15.11.2026 | ours |
| Base map | OpenFreeMap positron (OpenStreetMap), MapLibre GL 5.24.0 from cdnjs | live | ODbL / BSD |
| Address search | Photon (komoot, OpenStreetMap), only when the visitor searches an address | live | ODbL |

Decisions:
- "Running" = GTFS has trips (never the status field: lrt_stat still marks 28 running Red stations "מתוכננת").
- Two rail_stat passenger stations have no trains in the 22.11.2026 GTFS (ירושלים מלחה, ירושלים גן חיות התנ"כי): left off the map.
- Green Line shown "בבנייה": Tel Aviv-Yafo GIS lists executed works sections (e.g. גשר פנחס רוזן 9.2021-1.2023, ראול ולנברג 7.2021-7.2022); the national file row is from 2021.
- No opening date is shown. NTA's site (Cloudflare check) could not be read by this session; press dates in 01-TRANSPORT-DATA.md are not official sources.
- Walking minutes = straight line x 1.3 / 80 m per minute, labelled an estimate on the page.
