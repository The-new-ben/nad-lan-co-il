# Environmental-hazards map: public data inventory (Israel)

Research date: 3.11.2026 (all counts queried live that day, never copied from descriptions).
Scope: public, no-login data only. Nothing was signed into, no captcha, nothing written to any service.
Raw downloads: `docs/research/2026-11-03-hazards/layers/` (26 files, all under 25 MB, treated as data only).

## Two access facts that shape everything

1. **data.gov.il: only the CKAN datastore API is open.** `https://data.gov.il/api/3/action/datastore_search?resource_id=<id>&limit=10000&offset=N`
   works with no login (send a `User-Agent`, e.g. `datagov-external-client`). The direct file links on `e.data.gov.il/.../download/...`
   now 302-redirect to a Google sign-in (checked 3.11.2026 on the airport-noise ZIP and the PRTR CSV). So any resource that is not
   "datastore active" (ZIP, GDB, XML) is effectively behind a login. `datastore_search_sql` returns 404 (disabled).
2. **govmap.gov.il needs a token.** `https://www.govmap.gov.il/api/layers-catalog/catalog` -> `{"error":"access denied"}`;
   `.../api/search-service/autocomplete` -> 403; `ags.govmap.gov.il` refused the connection. Govmap layers and its geocoder are not
   usable without a registered govmap API key. We did not request one.

**Coordinates:** almost every Israeli government table is in **ITM, EPSG:2039** (X about 130,000-285,000, Y about 378,000-800,000;
verified per file below). Convert to WGS84 with proj4js using the standard EPSG:2039 string:
`+proj=tmerc +lat_0=31.7343936111111 +lon_0=35.2045169444444 +k=1.0000067 +x_0=219529.584 +y_0=626907.39 +ellps=GRS80 +towgs84=-24.0024,-17.1032,-17.8444,-0.33077,-1.85269,1.66969,5.4248 +units=m +no_defs`.

---

## 1. Cellular antennas and broadcast transmitters

### 1a. Active cellular antenna sites (MoEP non-ionizing radiation dept.) - USABLE NOW
- **What:** every licensed active cellular site with its radiation permit and the worst-point result as a percent of the health threshold.
- **Publisher:** Ministry of Environmental Protection (המשרד להגנת הסביבה). Dataset `antennaactive` ("אנטנות סלולריות פעילות").
- **Endpoint:** `https://data.gov.il/api/3/action/datastore_search?resource_id=8935c8e5-ec77-421f-af86-d970583195f8`
- **No login:** yes (datastore API). **Format:** CSV/JSON. **CRS:** ITM EPSG:2039 (`X_ITM`,`Y_ITM`).
- **Count (queried):** 8,531 rows; 8,525 with valid ITM, 6 without.
- **Fields:** ID, חברה, מס' אתר, עיר, כתובת האתר, רשות מקומית, תחום שיפוט, X_ITM, Y_ITM, סוג אתר, תאריך היתר הקמה, תאריך היתר הפעלה,
  בדיקה תקופתית אחרונה, היתר קרינה, עוצמה מרבית תיאורטית בµW לסמר, תוצאה מירבית ב% ביחס לסף הבריאות, תאור נקודה בה התקבלה תוצאה מירבית,
  קובץ הקמה, קובץ הפעלה (PDF links on documents.sviva.gov.il), טכנולוגיית שידור.
- **Updated:** resource last_modified 2026-11-03 (refreshed daily or close to it).
- **Content facts:** operators PHI (Hot+Partner) 2,983, Pelephone 2,821, Cellcom 2,727. Site types: ground mast 3,351, small indoor 1,597,
  rooftop mast 1,537, "עוקץ" 979, wireless access 839, disguised 226. Radiation permit: 8,525 yes, 6 no.
  Max result vs health threshold: median 2.95%, max 29.96%, zero sites above 50%. Last periodic check: 4,786 in 2026, 1,672 in 2025, 73 blank.
- **Caveats:** the % is the operator's measured or computed worst point at check time, not continuous exposure. "רשות מקומית" is not
  normalised (554 raw names: "עירית תל אביב", "תל אביב -יפו", "תל אביב יפו" ...). Indoor small cells are mapped at building address.
- **File:** `layers/moep_cell_antennas_active.csv` (3.4 MB).
- **Mirror:** ArcGIS Online `https://services8.arcgis.com/JcXY3lLZni6BK4El/arcgis/rest/services/אנטנות_סלולריות_פעילות/FeatureServer/4`
  (owner "sysdata", description "המשרד להגנת הסביבה"), `returnCountOnly` = 8,475, last edit 2026-09-09, EPSG:2039. Older than data.gov.il; use data.gov.il.

### 1b. Antennas pending construction permit - USABLE NOW
- MoEP `antenna_hakama` ("אנטנות סלולריות בהקמה"). Endpoint `resource_id=ff398c7e-c522-4ee8-a53a-312b188a573d`. No login.
- 305 rows, all "היתר הקמה", applications dated 2025-10-15 to 2026-10-11. ITM (`X_ITM`,`Y_ITM`), all 305 valid.
- Fields: ID, תאריך הגשת הבקשה, מס' סימוכין, חברה, סוג היתר, מספר האתר, ישוב, כתובת + תאור, סוג המוקד, X_ITM, Y_ITM, תחום שיפוט. Updated 2026-11-03.
- Caveat: an application, not a built antenna. Show as "planned". File `layers/moep_cell_antennas_pending.csv`.

### 1c. Broadcast transmitters (radio/TV, מתקני שידור) - NOT USABLE (no official open layer)
- data.gov.il search "מתקני שידור" = 0, "סלולר" = 0. No MoEP open layer of broadcast sites found.
- Proxy: OSM masts/towers (see 2f) = 359 features, incomplete, no power or radiation data.
- Related, not a map: `557` "בעלי היתר לביצוע מדידות קרינה בלתי מייננת" (list of licensed measurers, 2023).

---

## 2. Electricity: high-voltage lines, substations, power plants, transformer rooms

No official open IEC (חברת החשמל) layer found on data.gov.il ("חשמל" search = 1 unrelated hit). Govmap infrastructure layers need a token.

### 2a. OSM power lines - USABLE NOW (with attribution)
- **Endpoint:** Overpass `https://overpass-api.de/api/interpreter`, query `area["ISO3166-1"="IL"][admin_level=2]->.il; way["power"="line"](area.il); out geom;`
- No login. GeoJSON (built from Overpass JSON), WGS84 EPSG:4326. OSM base 2026-11-03T20:00Z. Licence ODbL, attribution "© OpenStreetMap contributors".
- **Count:** `out count` = 1,923 ways. voltage tag: 161 kV 1,523, 400 kV 328, 115 kV 5, untagged 67. (`power=minor_line` = 2,229 more ways, not downloaded.)
- bbox lon 34.35-35.82, lat 29.53-33.23. Operator tag empty on all ways.
- **Caveats:** crowd-mapped; transmission network looks well covered, distribution (22 kV and below) is not. Underground cables mostly absent.
- File `layers/osm_power_lines.geojson` (0.8 MB).

### 2b. OSM substations - USABLE NOW
- `nwr["power"="substation"]` count = 258 (255 ways, 3 nodes). voltage: 161 kV 188, 161/25 kV 15, 400/161 kV 9, 400 kV 9, untagged 36.
- File `layers/osm_power_substations.geojson` (258 features).

### 2c. OSM power plants - USABLE NOW
- `nwr["power"="plant"]` count = 257 (232 ways, 25 relations). Converted 232 (the 25 relations had no closed outer ring in the output; re-fetch with `out center` if needed).
- plant:source: solar 196, gas 24, hydro 3, coal 2, coal;gas 1, diesel 1, gas;diesel 1. File `layers/osm_power_plants.geojson`.

### 2d. Transformer rooms (חדרי שנאים) - NOT USABLE
- OSM `node["power"="transformer"]` = 388 nodes nationally. Israel has many thousands of transformer rooms; this is a tiny fraction.
- No official open layer. Do not map them; say so.

### 2e. Third-party mirror of IEC extra-high-voltage circuits - USABLE WITH WORK (licence)
- `https://services2.arcgis.com/N9O4H6cqPBna0bEx/arcgis/rest/services/קווי_מתח_עליון/FeatureServer/1453` (owner AvivGIS6, a planning firm).
- Service text: "עודכן ממערכת NIS יוני 2023". `returnCountOnly` = 94 polylines, EPSG:2039, last edit 2024-02-06.
- Fields: FID, CIRCUITNAM, VOLTAGE, REMARK, Shape_Leng, סוג, NAME. Type: 161 overhead 87, 161 underground 6, 400 overhead 1.
- Covers the north only (circuit names Kinarot, Hula, Katzrin, Kiryat Shmona...). Provenance IEC NIS via a private firm; licence unknown.
  Use only to cross-check OSM, not for public display without permission. File `layers/aviv_iec_ehv_lines_2023.geojson`.
- Same owner's `תמא_10_ג_13שכבות_שימושי_קרקע/FeatureServer` layers 6-7 are an OSM re-export (1,589 lines, 182 energy polygons): no added value.

### 2f. OSM communication masts/towers (proxy for transmitters) - USABLE WITH WORK
- `man_made=mast` 258, `tower:type=communication` 253, `communication:mobile_phone=yes` 113; union downloaded = 359 features.
- Mix includes 57 lighting masts. Filter to `tower:type=communication`. File `layers/osm_comm_masts_towers.geojson`.
- OSM `power=tower` (pylons) = 13,714 nodes, not downloaded (lines are enough).

---

## 3. Industry, PRTR, hazardous materials

### 3a. PRTR facility list (מפל"ס - רשימת מפעלים) - USABLE NOW
- MoEP `maflasmultiannualforzover`. Endpoint `resource_id=7ad8ddc7-87f4-45f9-84e4-d7f972662153`. No login. ITM.
- **Count:** 7,810 facility-year rows, 801 distinct environmental sites, reporting years 2012-2025 (2025: 566). 7,769 rows with coordinates.
- Key fields: ShemTaagidShutfut, SugPeilutAtarSvivati (activity code, e.g. "53 - תפעול מטמנות..."), AnafAtarSvivati (sector), TchumPeilutAtarSvivati,
  MisparAtarSvivati, ShemAtarSvivatiMenifa, address fields, YeshuvAtarSvivatiMenifa, RashutMekomitAtarSvivati, NekudatTsiunX/Y..., URL.
- Updated 2026-09-16. Caveat: 13 rows have a date string in ShnatDivuach (source quirk). Covers only facilities above PRTR thresholds.
- File `layers/moep_prtr_facilities.csv` (6.5 MB).

### 3b. PRTR releases (מפל"ס - נתונים רב שנתיים) - USABLE NOW (2025 subset saved)
- MoEP `maflasmultiannual`. Endpoint `resource_id=87c88ab8-3076-4422-a8fb-27bc57ce4b76`. No login. ITM.
- **Count:** 173,461 rows (all years). Saved year 2025 only: filter `filters={"ShnatDivuach":"2025"}` -> 13,371 rows, 566 facilities, 14.1 MB.
- 2025 by medium: air 6,936, sewage 3,572, sea 1,058, soil 924, water source 881. Top pollutants: ammonia, VOCs, PM2.5, PM10, NOx.
- Fields include SugPlita (medium), MezahemBeplitaHeb/Eng, KodMezahem, KamutPlita, KamutPlitaBeTeunot, NechonutNekudatTsiun
  (13,324 "נ.צ בתחום", 47 "נ.צ מחוץ לתחום"), coordinates. Updated 2026-09-16.
- **Full multi-year file is too large to keep here:** page `datastore_search` with `limit=10000&offset=N` over 173,461 rows
  (the e.data.gov.il CSV link is login-walled). File `layers/moep_prtr_releases_2025.csv`.

### 3c. MoEP facilities register (מפעלים) - USABLE WITH WORK
- `factory`. Endpoint `resource_id=88d1883c-3b7a-4580-9be9-6d54659666c3`. No login. ITM.
- 26,179 rows, 17,919 distinct site ids. **Only 13,449 rows have coordinates inside the ITM range; 12,730 are blank or out of range.**
- Fields: Shem_Atar_Svivati, Mispar_Atar, Mispar_Mezahe, Machoz, Yeshuv, mehute_Atar (activity, e.g. "2397 ייצור בטון"), Rashut_Mekomit, Nekudat_Tsiun_X/Y.
- Updated 2026-11-03. Caveat: includes small businesses (bakeries, garages); needs a category filter. Max X 285000 / Y 798667 also
  appears in the contaminated-land file: check for placeholder coordinates before mapping. File `layers/moep_factories.csv`.

### 3d. Permits: business-licence approvals, toxins (רעלים), X-ray, radioactive - USABLE WITH WORK (no coordinates)
- `licences_per_missions_facilities`. Endpoint `resource_id=e9ecedbd-8f93-437e-9a2f-4ff908daf210`. No login.
- 27,260 rows: אישור המשרד לרישיון עסק 26,218; רנטגן 606; קרינה רדיואקטיבית 401; **רעלים 35** (32 plants, all valid to 2026+).
- Fields: Yishuv_Name, Start_Date, End_Date, Heter_Num, Heter_Name, MifalName, Machoz_Name, SugHeter. **No coordinates**: join by plant name
  and locality to 3a/3c (fuzzy). 1,032 rows valid to 2026 or later. Updated 2026-11-03.
- Caveat: 35 toxins permits is far below the real number of היתרי רעלים in Israel; this file is not the full toxins register.
- File `layers/moep_permits_licences.csv`.

### 3e. Seveso-type major-hazard sites - NOT USABLE
- Israel has no published Seveso-style register. Closest proxies: PRTR (3a/3b), the 35 toxins permits (3d), stack sampling (3f).

### 3f. Stack sampling sites (מאגר זיהום אוויר מארובות) - USABLE WITH WORK (stale)
- `digumi_arubut`, `resource_id=d8b6d9dd-12b3-4f79-b900-5e171debdf51`. 564 rows, ITM, all valid. Fields MIFALKEY, MIFAL, YISHUV, RASHUTMEKO, MACHOZ, X, Y, hyperlink.
- Last modified 2020-09-03. File `layers/moep_stack_sampling_2020.csv`. (Related `svivaniturmifal` "פליטות ממפעלים" exists, not inspected.)

### 3g. Industrial zones (Ministry of Economy) - USABLE WITH WORK
- `industrial-zones-info`, `resource_id=30af8da4-7586-4b00-ac88-c5ee75251632`. 32 rows with `geom` WKT POLYGON in ITM.
- Only zones the Ministry of Economy manages, not all industrial land. Updated 2026-11-03. File `layers/economy_industrial_zones.csv`.
- Better national coverage: OSM `landuse=industrial` count 1,139 (1,124 converted) -> `layers/osm_industrial_landuse.geojson`.
- MoEP `industrialareas` ("אזורי תעשייה הנדרשים בביצוע סקר קרקע") is XML on e.data.gov.il: login-walled, not usable.

### 3h. Contaminated land (קרקעות מזוהמות) - USABLE NOW (with careful wording)
- `contaminatedterrains`, `resource_id=cbb2ed28-310d-4389-a1ec-64bb538fc090`. 3,829 rows, ITM, all with coordinates.
- legend: "היתכנות לזיהום קרקע" 3,614; (חסר) 80; "בחקירה/ בשיקום" 68; "סיים שיקום או אין סיכון" 67. Fields name, address, X, Y, gush, helka, legend,
  matzav, peeilut, date, sug, stat_gas, stat_zih, drisha, d_begin, d_end, link. Updated 2026-11-03.
- Caveat: 94% are "potential" (suspected by past land use), not confirmed contamination. Must be labelled that way. File `layers/moep_contaminated_land.csv`.

---

## 4. Air quality

### 4a. Monitoring stations - USABLE NOW (locations only)
- MoEP `air-stations`, CSV `resource_id=782cfb94-ebbd-4f41-aba2-80c298457a58` (XLSX twin 9e6daaea...). No login. ITM.
- 159 stations (158 with coordinates). Operators: MoEP 34, IEC 24, Sharon-Carmel towns association 21, Haifa association 16, Ashkelon 12, Neot Hovav 10...
  Types: Background 120, Traffic 16, Industrial 11, Mobile 10. Fields include מזהמי אוויר, פרמטרים מטאורולוגיים, שנת הקמה, כתובת, X, Y.
- Last modified **2024-04-01** (station list may be out of date). File `layers/moep_air_stations.csv`.

### 4b. Latest measured values - NOT USABLE (no open API found)
- `https://air.sviva.gov.il/` is a live Envista web app (HTML 200). Its data calls are internal; `api/...GetStations`-style guesses returned 404
  and no documented public API was found.
- **The old public API host `api.svivaaqm.net` now serves a domain-for-sale parking page. Never call it** (anyone who buys it could serve fake data).

### 4c. Air-pollution forecast by region - USABLE WITH WORK
- `cf-output` ("תחזית חצי-יומית למזהמי אוויר"), `resource_id=a976089d-e8e5-4013-8f3d-777b8551c684`. 17 rows (regions such as "באר שבע רבתי"),
  fields air_quality, fill_color, morning/noon/evening. Updated 2026-11-03. No geometry: region names only (needs a region polygon join).
- File `layers/moep_air_forecast_regions.csv`. No national air-pollution grid (concentration raster) was found as open data.

---

## 5. Noise

- **Airport noise contours** (MoEP `ap`, "חשיפה לרעש משדות תעופה", `ap7.gdb.zip`, resource last modified 2021-05-13): the file is only on
  e.data.gov.il -> **Google sign-in redirect**. NOT USABLE without logging in. Israel Airports Authority publishes noise maps as documents, not open geometry.
- **Roads and rail noise:** no open national or municipal noise-map geometry found (data.gov.il "רעש" returns only the legal-limits table `noise-duration` and the airport ZIP).
- **Proxy, USABLE NOW (distance only, never dB):** OSM `railway=rail` 2,272 ways -> `layers/osm_railways.geojson`; OSM `aeroway=aerodrome` 45 -> `layers/osm_aerodromes.geojson`;
  OSM `highway~motorway|trunk` 7,553 ways (not saved; fetch with `way["highway"~"^(motorway|trunk)$"](area.il); out geom;` on Overpass).

---

## 6. Fuel, gas and pipelines, landfills, sewage plants, Haifa Bay

- **Fuel stations (Ministry of Energy) - USABLE NOW.** `gas-station`, `resource_id=5537a0ef-3eeb-449c-90c8-51e27564f0cb`. 1,255 rows, ITM X/Y plus WGS84
  (`נ.צ. אורך`, `נ.צ. רוחב`, 1,253 filled). Fields מס_מינהל_הדלק, חברה, שם_תחנה, כתובת, רשות_מקומית. Updated 2026-01-19. File `layers/energy_fuel_stations.csv`.
  (Also `fuelstationbynumber` XLSX 2026-08-06, not saved; OSM `amenity=fuel` = 1,036; Beer Sheva municipal list `gas-stations-br7`.)
- **Gas and fuel pipelines (קו צינור) - NOT USABLE.** OSM `man_made=pipeline` = 106 ways, of which substance gas 1, water 10, untagged 95.
  INGL natural-gas transmission and EAPC/Katsa oil lines are not open data. File `layers/osm_pipelines.geojson` kept for reference only.
- **Landfills - USABLE WITH WORK.** MoEP `matmenot-psolet-mixed` 11 and `matmenot-binyan` 13 (names and ids only, no coordinates, 2024-07-22);
  `asbestoslandfills` 6 (addresses, no coordinates). Locations come from PRTR activity 53 ("תפעול מטמנות") in 3a and from OSM `landuse=landfill` = 35.
  Files `moep_landfills_mixed.csv`, `moep_landfills_construction.csv`, `moep_asbestos_sites.csv`, `osm_landfills.geojson`.
- **Sewage treatment plants (מט"ש) - USABLE WITH WORK.** MoEP `matash` = 80 rows of annual-report links (2015), no coordinates.
  OSM `man_made=wastewater_plant` = 91 (89 converted) -> `layers/osm_wastewater_plants.geojson`. PRTR sector "פסולת ושפכים" adds plants with coordinates.
- **Haifa Bay industrial zone:** no dedicated open layer. Build it from PRTR (3a/3b), air stations (Haifa association), contaminated land, OSM industrial landuse.

---

## 7. Seismic hazard and flood zones

- **Seismic (Geological Survey PGA / IS 413 zonation) - NOT USABLE.** No reachable GSI ArcGIS REST (`gis.gsi.gov.il`, `geo.gsi.gov.il` do not answer;
  `gsi.gov.il/arcgis/...` redirects to the web site). No open geometry found on data.gov.il or ArcGIS Online. The map exists as a document.
- **Flood zones - NOT USABLE.** No national flood-hazard layer found. ArcGIS Online `FinalHatzafaAreas_January2018` (SPNI, 42 polygons, EPSG:2039)
  is a planning-comments layer, not a flood-risk map. MAPI sea-level-rise scenarios on data.gov.il are ZIPs on e.data.gov.il (login-walled).

## 8. Radon - NOT USABLE
- data.gov.il `radon` ("סקר ראדון") points to `https://ims.data.gov.il/sites/default/files/RADON.XML`: the host no longer resolves (DNS failure, 3.11.2026).
- Only lists of licensed radon testers and labs exist (`radon-practitioners`, `radon-lab-practitioners`): not a hazard map.

## 9. govmap.gov.il
- Honest answer: **govmap layers and the govmap geocoder are not queryable without a token** (access denied / 403 / connection refused, see top).
  If the owner wants govmap layers (IEC lines, flood, etc.), a govmap API key must be registered under his name; we did not do that.

---

## Locality-level aggregates
- No ready-made "per locality" hazard tables were found on data.gov.il.
- We can compute them: antennas per local authority from 1a. Raw "רשות מקומית" has 554 spellings; a naive clean-up gives 439, still with duplicates
  ("תל אביב" 325 vs "תל אביב יפו" 547). Top after clean-up: Jerusalem 671, Tel Aviv-Yafo 547 (+325), Haifa 337, Petah Tikva 247, Rishon LeZion 226,
  Ramat Gan 204, Beer Sheva 202, Holon 152, Netanya 149. Correct method: spatial join of the points to official municipal boundaries, not the name field.
- The same spatial join gives PRTR facilities, contaminated-land sites and fuel stations per locality.

## Geocoding (address -> coordinates, whole of Israel, no paid key)
- **OSM Nominatim** (`https://nominatim.openstreetmap.org/search?format=jsonv2&countrycodes=il&q=...`): works in Hebrew. Tested "הרצל 10, ראשון לציון" ->
  building, 31.97133, 34.80582; structured "10 שדרות רוטשילד / תל אביב" -> 32.06272, 34.77019; reverse works. **Usage policy:** max 1 request/second,
  an identifying User-Agent, no autocomplete-as-you-type, no bulk jobs, results must be cached, ODbL attribution. Fine for low traffic with a server-side cache;
  for real traffic self-host Nominatim or Photon on the Geofabrik "israel-and-palestine" extract.
- **Photon (komoot)** (`https://photon.komoot.io/api/?q=...&bbox=34.2,29.4,35.9,33.4`): same hit for the same address (OSM data), GeoJSON out; fair-use public
  instance, no SLA. Good fallback and good for typeahead only if self-hosted.
- **govmap geocoder:** token required (403). Not usable now.
- Recommendation: geocode on our server, cache every result, throttle to 1/s to Nominatim, fall back to Photon, then convert nothing (both return WGS84).

---

## Bottom line

**We can honestly map today (official, refreshed, with coordinates):** active cellular antennas with their radiation-permit result (8,531),
pending antenna permits (305), PRTR facilities and their 2025 releases (566 facilities in 2025, 801 sites since 2012), contaminated-land sites (3,829,
mostly "potential"), fuel stations (1,255), air-monitoring station locations (159, list dated 2024). From OpenStreetMap with attribution:
high-voltage lines (1,923 ways, 161/400 kV), substations (258), power plants (257), railways, airfields, industrial land, sewage plants, landfills.

**We can map with work:** MoEP factories (half lack coordinates), toxins/radioactive/X-ray permits (no coordinates, join by name), industrial zones (32 only),
air-pollution forecast (regions only), landfills and sewage plants (official lists without coordinates; locations from PRTR and OSM).

**We cannot map today:** broadcast transmitters with radiation data, transformer rooms, distribution lines, gas and fuel pipelines, live air-quality values,
any air-pollution grid, airport noise contours (login wall), road and rail noise in decibels, seismic acceleration, flood zones, radon, and every govmap layer (token).

**What the map must say about missing data (on the map itself, not only in a footnote):**
- Hebrew line for the UI: "אין סימון במפה לא אומר שאין מפגע. המפה מציגה רק מה שמפורסם במאגרים פתוחים; חלק מהמפגעים (חדרי שנאים, צנרת גז, רעש, ראדון) לא מפורסמים בכלל."
- Every layer shows its source and its data date ("נכון ל-..."), and OSM layers say they are community-mapped and may be incomplete.
- Contaminated land must say "חשד לזיהום לפי שימוש קרקע בעבר" for the "היתכנות" class, never "קרקע מזוהמת".
- Antenna results are shown as the published "% of the health threshold at the worst point", never as a safety verdict.
- Distances only, never invented exposure numbers (no dB, no µW where the source gives none).

| Layer | Publisher | Count (queried 3.11.2026) | Usable |
|---|---|---|---|
| Active cellular antennas + radiation % | MoEP (data.gov.il) | 8,531 | Now |
| Antennas pending construction permit | MoEP (data.gov.il) | 305 | Now |
| Broadcast transmitters | none open | 0 | No |
| Comm masts/towers (proxy) | OSM | 359 | With work |
| High-voltage lines | OSM | 1,923 ways | Now (attribution) |
| EHV circuits (north, NIS 2023) | AvivGIS6 on ArcGIS Online | 94 | With work (licence) |
| Substations | OSM | 258 | Now |
| Power plants | OSM | 257 | Now |
| Transformer rooms | OSM only | 388 (tiny fraction) | No |
| PRTR facility list 2012-2025 | MoEP (data.gov.il) | 7,810 rows / 801 sites | Now |
| PRTR releases (all years / 2025) | MoEP (data.gov.il) | 173,461 / 13,371 | Now |
| Facilities register | MoEP (data.gov.il) | 26,179 (13,449 with XY) | With work |
| Permits incl. toxins (35), radioactive (401), X-ray (606) | MoEP (data.gov.il) | 27,260 | With work (no XY) |
| Stack sampling sites | MoEP (data.gov.il) | 564 (2020) | With work |
| Industrial zones | Ministry of Economy (data.gov.il) | 32 | With work |
| Industrial land use | OSM | 1,139 | Now |
| Contaminated land | MoEP (data.gov.il) | 3,829 | Now (careful wording) |
| Air-monitoring stations | MoEP (data.gov.il) | 159 | Now (locations) |
| Live air-quality values | MoEP air.sviva.gov.il | n/a | No (no open API) |
| Air-pollution forecast regions | MoEP (data.gov.il) | 17 | With work |
| Airport noise contours | MoEP (data.gov.il ZIP) | not countable (login wall) | No |
| Railways / airfields (noise proxy) | OSM | 2,272 / 45 | Now (distance only) |
| Motorways/trunk roads (noise proxy) | OSM | 7,553 ways | Now (fetch on demand) |
| Fuel stations | Ministry of Energy (data.gov.il) | 1,255 | Now |
| Pipelines | OSM | 106 (1 tagged gas) | No |
| Landfills | MoEP lists 11+13+6 / OSM | 30 (no XY) / 35 | With work |
| Sewage treatment plants | MoEP list 80 (no XY) / OSM | 80 / 91 | With work |
| Seismic PGA | Geological Survey | none found | No |
| Flood zones | none open | none found | No |
| Radon | MoEP / data.gov.il | host dead | No |
| govmap layers + geocoder | govmap | token required | No |
| Geocoding | OSM Nominatim / Photon | tested OK | Now (1 req/s, cache) |
