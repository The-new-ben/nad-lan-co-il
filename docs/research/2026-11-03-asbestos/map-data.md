# Public geographic data on asbestos in Israel - what really exists

Checked 3.11.2026, 17:45-18:40 UTC. Every count below was obtained by querying the live endpoint (ArcGIS REST `returnCountOnly` / statistics, data.gov.il CKAN `datastore_search`), not copied from a description. Nothing was written to any service.

## Bottom line

- **There is no national asbestos map in Israel.** MoEP told the Knesset (17.12.2023) that no mapping of asbestos stock or asbestos-cement roofs, with extent and location, had ever been done, and that a national mapping was being promoted for 2024. MoEP's 02.12.2025 implementation-report news says satellite-based mapping of asbestos roofs was done in the Gaza envelope and is "expected to be published as a layer on the government map site". **No such govmap layer was found on 3.11.2026.**
- **One real, public, queryable asbestos layer exists:** the Western Galilee friable-asbestos soil project sites, **348 points**, with locality, jurisdiction and clean-up status (ArcGIS REST, GeoJSON export works, no login).
- **One local roof-mapping layer exists** (Golan Heights extent, October 2017): **181 polygons tagged asbestos** out of 14,803 building polygons. Public, but its publisher is an ArcGIS organisation keyed `M-GOLAN` whose identity was not confirmed; treat as unofficial until the council confirms.
- Everything else is **tabular** (registry of 453 licence holders, 6 landfill sites, 8 labs, 255 local authorities -> 57 environmental units). These have locality names or addresses, not coordinates, so they can be mapped only by geocoding at locality level.

What we can honestly build: (1) a Western Galilee map of the 348 project sites with the official status legend; (2) a national "who is near me" map of licence holders and landfills aggregated by locality / district (geocoded by us, labelled as such); (3) a local-authority lookup (no geometry needed). We cannot honestly show "asbestos roofs near you" anywhere in Israel except the 2017 Golan layer, and that only after provenance is confirmed.

---

## 1. Western Galilee friable-asbestos soil project - site points (MoEP data)

| Item | Value |
|---|---|
| Endpoint | https://services8.arcgis.com/JcXY3lLZni6BK4El/arcgis/rest/services/asbestos/FeatureServer/0 |
| ArcGIS item | 4066e69c1aa94f40b247db671f8ab527 "פרויקט ניקוי קרקעות מאסבסט פריך בגליל המערבי", owner `sysdata` (the data.gov.il ArcGIS account), access public, accessInformation "המשרד להגנת הסביבה", licence "according to data.gov.il terms of use" |
| Created | 01.05.2018 (item metadata); data covers the 2011-2017 stage A project |
| Format | ArcGIS FeatureServer, point layer; `f=json` and **`f=geojson` both work**; outSR 4326 works; capabilities: Query only; maxRecordCount 2000 |
| **Feature count** | **348** (`where=1=1&returnCountOnly=true` -> `{"count":348}`) |
| Fields | OBJECTID, site_num (site number on the project map), yishuv (locality), X, Y (Israel TM Grid, EPSG 2039), shiput (jurisdiction), vaad_mkomi (local committee), link (per-site PDF map), legend (status) |
| By status (legend) | 234 "אתר שנוקה ולא ידוע על אסבסט שנותר בקרקע" · 101 "אתר שנוקה אך ידוע שנותר אסבסט תחת התשתיות" · 13 "אתר שידוע שיש בו אסבסט, טרם בוצע ניקוי" |
| By locality | Nahariya 122 (118 + 4 spelled נהריה) · Ben Ami 54 · Bustan HaGalil 35 · Betzet 28 · Liman 21 · Sa'ar 16 · Yechiam 16 · Kabri 16 · Kfar Rosh HaNikra 12 · Netiv HaShayara 8 · Mazra'a 7 · Evron 6 · Nes Ammim 6 · Ga'aton 1 |
| By jurisdiction | Mateh Asher 214 · Nahariya 128 · Mazra'a 6 |
| Downloadable without login | **Yes** via the REST endpoint. The data.gov.il catalogue copy (dataset `cleanasbestos`, XML resource) is **not**: the data.gov.il page returns 404 and the `e.data.gov.il` file redirects to a Google sign-in. |
| Caveats | Status is as of the 2018 layer; stage B (2022/2023-2026) results are not in it. The per-site PDF links point to the retired `www.sviva.gov.il` site and now redirect to the MoEP homepage (dead). MoEP's own text says stage A covered 342 sites; the layer has 348 points (some sites have sub-points, e.g. 218.2, 218.6, 218.8). |

Example request (GeoJSON, WGS84):
`https://services8.arcgis.com/JcXY3lLZni6BK4El/arcgis/rest/services/asbestos/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=geojson`

## 2. Asbestos roof mapping, Golan Heights extent (October 2017) - unofficial until confirmed

| Item | Value |
|---|---|
| Endpoint | https://services2.arcgis.com/jnlY5lLf3TzEtt6y/arcgis/rest/services/%D7%90%D7%A1%D7%91%D7%A1%D7%981/FeatureServer/0 (layer `ASBEST`, service description "מיפוי אסבסט") |
| Related items | Web map 9acab89ada5142f5a7a79f64602e9f98 "מיפוי גגות אסבסט- אוקטובר 2017"; web app 6bd77f27c1864cd9acb669ccd14257b8 "מיפוי גגות אסבסט" at m-golan.maps.arcgis.com (created 22.10.2017); owner `usvitaly88`, organisation urlKey `M-GOLAN` |
| Format | ArcGIS FeatureServer, polygons, EPSG 2039; maxRecordCount 1000 |
| **Feature count** | **14,803** polygons in total; **181** have field `גגות` = "אסבסט" (statistics query); summed footprint area of the 181 ≈ **61,500 m²** (footprint, not roof surface) |
| Extent | lon 35.65-35.84, lat 32.73-33.20 (Golan Heights) |
| Fields | OBJECTID, גגות (roof type), REMARKS, GlobalID, Shape__Area, Shape__Length |
| Downloadable without login | Yes (query). Note: the service also exposes editing capabilities publicly; we only read. |
| Caveats | Publisher identity not confirmed (likely a regional council GIS account, not MoEP); 2017 snapshot; no metadata on method. **Do not publish without the council's confirmation.** |

## 3. Registry of asbestos licence holders (MoEP) - tabular, locality level

| Item | Value |
|---|---|
| Source | data.gov.il dataset `asbest` "מרשם העוסקים באסבסט" (resource 512d916e-07f0-4774-b84a-3a989e45e7eb), also searchable at https://www.gov.il/he/Departments/DynamicCollectors/asbest_list |
| Format | CSV + CKAN datastore API (`/api/3/action/datastore_search?resource_id=...`) - works without login; the direct CSV download link is behind CloudFront and was blocked for scripts (403), the API is not |
| Updated | dataset modified 03.11.2026 (gov.il page: 25.01.2026) |
| **Records** | **453**: 168 asbestos-cement workers in charge, 115 asbestos-cement contractors, 109 surveyors, 30 friable workers in charge, 16 friable inspectors, 15 friable contractors |
| Fields | LicenseType, LicenseNumber, Name, Phone, AdditionalTelephone, Fax, Email, Address, Settlement, District, LicenseExpirationDate, DisciplinaryAspects, EmployerContractor, AdditionalTerms |
| Geography | District (Center 132, North 115, South 86, Haifa 44, Tel Aviv 37, Jerusalem 33, blank 6) and 157 distinct localities; **no coordinates** |
| Use | Map by locality centroid (we geocode; label "location = registered address locality, not service area"); filters by licence type; show licence expiry and disciplinary entries as published. Personal names and phones are public in the registry but our page should link out rather than republish personal details. |

## 4. Asbestos landfill and transfer sites (MoEP) - tabular, addresses

| Item | Value |
|---|---|
| Source | data.gov.il dataset `asbestoslandfills` "מטמנות אסבסט" (XLSX + datastore), modified 03.11.2026 |
| **Records** | **6**: 5 landfills + 1 transfer station (Milu'ot South / Western Galilee; Ef'e - Tamar area, cement + friable; Nimra - Eilot area; Shfeya at Tut quarries near Zichron Ya'akov; Haruvit near Sdot Micha, Road 383; Neot Hovav landfill 204, cement + friable) |
| Fields | LicenseNumber, EnvironmentalSite, ResponsiblePerson, SiteType, Address, PhoneNumber, FaxNumber, LicenseExpiryDate, DisciplinaryMeasures |
| Geography | text addresses only - 6 points can be placed by hand from the addresses (we would label them "approximate") |
| Older copy | dataset `asbest-waste-sites` (2020, 9 rows, several marked closed) - stale, do not use |

## 5. Asbestos laboratories (MoEP) - tabular

data.gov.il `asbestos-lab` (modified 03.11.2026): **8** licence rows (4 sampling, 2 analysis, 2 air-sample analysis only), addresses only. Older `asbestsamplinganalysis` (2024, 10 rows) is superseded.

## 6. Local authorities -> environmental units (MoEP) - directory, no geometry

| Item | Value |
|---|---|
| Source | https://www.gov.il/BlobFolder/generalpage/moked_hasviva/he/Emergency_cyber_environmental-units.xlsx (linked from the MoEP hotline page, updated 26.05.2026); downloads without login |
| **Rows** | **255 local authorities** mapped to **57 distinct environmental units** (105 via town associations for environmental quality, 71 regional units, 24 municipal units, 55 unclassified) |
| Fields | authority, MoEP district, unit name, unit type flags, manager name, manager phone, e-mail, unit phone, fax, website (132 rows), address |
| Use | "Type your city -> your environmental unit + MoEP district + hotline" lookup. Can be joined to official municipal boundaries if we want a choropleth (boundary source not checked in this research). |

## 7. Asbestos work permits dataset (MoEP) - not usable

data.gov.il `asbest-permit-03-2016` "היתרים לעבודות אסבסט": requests for permits Q2 2015 - Q1 2016 with area, asbestos type and quantities. The file is **not downloadable** (data.gov.il CloudFront 403; `e.data.gov.il` copy also blocked), datastore not active. Ten-year-old in any case. Aggregate permit numbers by year and district exist only as charts in the Knesset report of 17.7.2023 (see facts.json).

## 8. Other things checked

- **govmap.gov.il**: no asbestos layer found (search and MoEP statements). The Gaza-envelope satellite roof layer announced on 02.12.2025 was not found.
- **soil-remediation.co.il GIS dashboard** (managing company of the Western Galilee stage B): ArcGIS dashboard a98c58f61d5b435eb30a078e5f8256dc -> layer `EvenDerech_Sites` (112 polygons). It covers contaminated-land remediation sites in general (IDF camps, landfills, civil sites, coded Type 1/2/3 and Status 1-4 without published domains). **Not an asbestos layer**; do not use for asbestos.
- **Local roof surveys reported to the Knesset (17.12.2023)**: Sdot Negev RC mapped ~40,000 m² of asbestos roofs; Ashkelon received NIS 350,000 (2020 decision) for roof mapping. **Neither result was found published as data.**
- **Municipal rules with geography in text only**: Haifa requires surveys in TAMA 38 / urban-renewal buildings and in the Check Post, port, Hadar and downtown areas - an area list, not a GIS layer.
- **PDF maps**: the Western Galilee per-site PDF maps (old sviva.gov.il links) are dead; MoEP's project photo book 2011-2017 is a PDF (https://www.gov.il/blobFolder/reports/western_galilee_asbestos_removal/he/asbestos_western_galilee_asbestos_removal_photos_2011-2017.pdf), not a map dataset.

## Recommended map build (honest scope)

1. **Western Galilee layer** - 348 points from section 1, three-colour status legend exactly as MoEP worded it, locality filter, "data as of 2018 layer; stage B ongoing to 2026" note, link to MoEP and to the stage-B reporting site.
2. **"Who can do the work near me"** - registry (section 3) aggregated per locality and district, landfill and transfer sites (section 4) as six labelled points, labs (section 5).
3. **"Who do I call" lookup** - authority -> environmental unit (section 6) + MoEP hotline *6911 + local 106.
4. Optional, only after written confirmation from the publisher: the 2017 Golan roof layer (section 2) as a case study of what roof mapping looks like.
