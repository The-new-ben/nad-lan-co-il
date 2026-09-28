# Stage geometry: Dimri Yama, Ashira, DUO, H-Infinity

Run date: 28.9.2026. Prepared by an Opus 5.5 research agent. This is read-only research: nothing was deployed and no
plugin code was edited. Fable audits this before any stage is built on it.

Purpose: the data for 3D stages of four Tel Aviv projects, built like the Rainbow stage
(`plugins/nadlan-config/assets/project-stage/rainbow/stage.js`, lines 100-140: `LOT_OUTLINE`, `TOWER`, `BLOCKS`).

---

## 0. How to read this file

### 0.1 Evidence classes

| Label | Meaning |
|---|---|
| **OFFICIAL** | A Tel Aviv-Yafo municipal record (planning committee text, GIS layer, building permit), or a company's filing to the stock exchange. |
| **DEVELOPER** | The developer's own marketing page. It shows intent, not a binding plan. |
| **PRESS** | A news or portal article. |
| **COMPUTED** | Arithmetic or geometry on an OFFICIAL value. The method is stated. It is not a source claim. |
| **DRAWING** | Measured by us off a scanned drawing inside an official document, then fitted to the official GIS lot outline. The municipality warns that its scans are not to scale. Accuracy is about ±2-3 m. A stage may draw it, but the caption must say "illustration". |
| **TOUR ESTIMATE** | A value that exists only in our own tours or 3D models. No official source. Never shown as a fact. |

### 0.2 Coordinate frame (the same convention as Rainbow)

- **Origin:** the lot's centroid, computed from the lot polygon in the city's GIS layer 837 (see 0.3).
- **Local metres:** `e = (lng - lng0) * cos(lat0) * 111320`, `n = (lat - lat0) * 110574`. These are the constants in
  `scripts/project-stage/build_quarter_rainbow.py` and `rainbow_lot_layout.py`.
- **Turned with the lot:** `X = e`, `Z = -n`, `g = -GRID°`, then `x = X*cos g - Z*sin g`, `z = X*sin g + Z*cos g`.
  So **x = grid east** and **z = grid south**, exactly as in `rainbow_lot_layout.py`.
- **GRID per lot:** the bearing of the lot's long street edge, minus 90°.
  - Lots 107 and 101: edges at 101° / 281° / 11° / 191°, so GRID = 11°.
  - DUO (lots 111 + 112) and H-Infinity (lot 124): edges at 99-100° / 190°, so GRID = 10°.
  - Rainbow's code uses 10° for lot 111. The 1° difference is about 1.7 m over 100 m.
- **Method check:**
  - The same method on lot 111 returns Rainbow's origin exactly (32.103168, 34.784441), and it returns the vertices in
    `rainbow_lot_layout.py`.
  - `rainbow/city.json` already holds plates for lots 107 and 101, taken from the design-plan snapshot. They match the
    layer 837 outlines within about 1 m.

### 0.3 The municipal GIS layers used (public ArcGIS REST, read-only GET queries)

Base URL: `https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/<layer>/query`

| Layer | Name | What it gave |
|---|---|---|
| 837 | מגרשי ייעודי קרקע - מפורט | The lot polygons, lot numbers, block and parcel, registered and graphic areas, land use. |
| 528 | תוכניות בניין עיר | The design-plan records for each lot, with their document pages. |
| 772 | בקשות והיתרי בניה | Permits: units, floors, addresses, permit dates. |
| 513 | מבנים | Building footprints: DUO's two towers and H-Infinity's tower. |

Example query for lot 107:
`.../837/query?where=st_mispar_migrash_betaba='107' AND st_taba LIKE '%3001%'&outFields=*&returnGeometry=true&outSR=4326&f=json`

The outlines below are simplified from the raw polygons (Douglas-Peucker, 0.35 m tolerance). The raw polygons have 12 to 62
vertices.

---

## 1. Dimri Yama (Y.H. Dimri), lot 107, Eshkol, Sde Dov

### 1.1 Reference point

| Item | Value | Source |
|---|---|---|
| Lot centroid (the stage origin) | **32.104441, 34.784472** | COMPUTED from GIS 837 (oid_migrash 26781). It is identical to our page's `lat`/`lng` and to `docs/data/location-audit-2026-08-05.csv`. |
| Position in Rainbow's turned frame | x -21.6, z -139.1 m | COMPUTED. `quarter.json` holds the same point unturned: (2.9, -140.8). |
| Block / parcel / lot | Block 6634, GIS parcel 2613, lot 107 in plan תמ"ל/3001. Land use "מגורים, מסחר ותיירות" | OFFICIAL (GIS 837) |
| Area | 7,589.11 m² graphic, 7,578.03 m² registered. The design plan says "7.59 ד'" | OFFICIAL (GIS 837; design decision p.5) |

### 1.2 Lot outline (OFFICIAL, GIS 837)

Latitude and longitude, from the north-east corner going clockwise:
`(32.104665, 34.785101) (32.104147, 34.784987) (32.104098, 34.784953) (32.104071, 34.784910) (32.104057, 34.784860) (32.104058, 34.784807) (32.104214, 34.783847) (32.104846, 34.783989)`

In the stage frame (GRID 11°, metres):
`LOT_OUTLINE = [[53.5,-35.6],[53.9,22.6],[51.7,28.6],[48.4,32.3],[44.0,34.8],[39.1,35.6],[-53.1,35.9],[-53.3,-35.2]]`

- **Shape:** a rectangle about 107 m (grid east-west) by 71 m (grid north-south), with a rounded south-east corner.
  - North edge: 106.8 m at bearing 101°.
  - East edge: 58.2 m at 191°, then an arc of about 10 m radius.
  - South edge: 92.1 m at 281°.
  - West edge: 71.1 m at 11°.
- **Neighbours:** lot 107 is the southern half of planning unit 6 (lots 105 and 107, plus part of open space 608).
  - The unit is bounded by a street to the north ("רחוב מס' XXX"), Yaakov Apter St. to the south, Israel Galili St. to
    the east, and lot 608 to the west.
  - A strip of open space 608 separates lot 105 (north) from lot 107.
  - Source: design decision, p.1 (OFFICIAL).
- **Building lines:**
  - 3 m from the north and west edges, which face open space.
  - 0 m on the east and south, along the streets.
  - Buildings facing the open space step back a further 3-4 m.
  - The tower keeps about 5 m from the southern lot line so the sidewalk can be widened.
  - Buildings stand 12 m apart, not counting balconies.
  - Source: design decision, section 2.1(ד) (OFFICIAL).

### 1.3 Buildings

Sources:
- Tel Aviv local committee, meeting 23-0008ב, decision 11, **10.5.2023**, "תא/תעא/תמל3001(107) - מגרש 107 אשכול"
  (OFFICIAL): <https://www.tel-aviv.gov.il/Residents/Development/DocLib/%D7%93%D7%99%D7%95%D7%9F%20%D7%91%D7%A2%D7%99%D7%A6%D7%95%D7%91%20%D7%9E%D7%92%D7%A8%D7%A9%20107%20%D7%90%D7%A9%D7%9B%D7%95%D7%9C.pdf>
- The GIS record for this design plan (layer 528, id_taba 8210) shows it effective **30.6.2025**. Its final documents are
  scanned PDFs that this run did not read (see 1.6).

Four buildings: "מגדל בן 40, מגדלון בן 16 קומות ושני מבנים מרקמיים בני 9 קומות". Letters are as in the plan's key drawing (p.6).

| Id | Kind | Floors (OFFICIAL) | Floor heights and height (OFFICIAL) | Areas main / service, m² (OFFICIAL, p.7) | Footprint centre (x, z) | Footprint size (grid E-W x N-S) | Place on the lot |
|---|---|---|---|---|---|---|---|
| A | Tower | 40: ground floor (retail, lobbies, residents' shared areas) + 38 residential + a technical floor on the roof | Ground ≤7 m; typical 4 m; the top two residential floors ≤4.5 m (they include private pools); **at most 165 m above ground** | 23,700 / 8,000 | (-30.9, 18.2) DRAWING | 30.2 x 30.2 m, 907 m² DRAWING. Official tower coverage: **900 m² (12% of the lot)** | **South-west** (OFFICIAL: key plan; fire pad "between the tower and the hotel building" on the south sidewalk) |
| B | Textural (residential) | 9 | Ground ≤4.5 m (residential, no private yards); typical 3.5 m | 6,450 / 1,850 | (-16.3, -18.7) DRAWING | 61.6 x 18.9 m, about 1,155 m² DRAWING | **North**, a long bar from the west edge (OFFICIAL: key plan; called "the north-west textural building" in the text) |
| C | Mid-rise (מגדלון) | 16: ground floor (retail, a colonnade 5 m wide and 4.5 m high on the east street, lobbies, the ramp) + 15 residential | Ground ≤7 m; typical 3.5-4 m; the top two ≤4.5 m (private pools) | 8,000 / 2,530 | (37.4, -13.9) DRAWING | 21.8 x 28.6 m, about 621 m² DRAWING | **North-east corner** (OFFICIAL: "במגרש 107 המגדלון ממוקם בפינה הצפון מזרחית"). The basement ramp runs under it. |
| D | Textural (hotel + residential) | 9: ground floor (retail, hotel lobby, colonnade on the east and south) + 7 floors of homes and hotel + a 9th floor for residents' amenities with a pool | Ground ≤7 m; typical 3.5-4 m; the pool floor ≤5 m | 5,870 / 2,630 | (22.0, 24.1) DRAWING | 52.2 x 22.9 m, rounded south-east corner, about 1,146 m² DRAWING | **South-east** (OFFICIAL: key plan; "המבנה הדרום מזרחי (D)") |

- **Plan totals (OFFICIAL, p.6):**
  - Main areas 38,526 m² (as printed).
  - Above-ground service areas 17,314 m².
  - Balconies 6,832 m².
  - Basement coverage 6,450 m² (85% of the lot).
- **Heights not stated in the text, computed from the stated floor heights (COMPUTED):**
  - B: about 32.5 m (4.5 + 8 x 3.5).
  - C: about 61.5-68 m (7 + 13 x 3.5..4 + 2 x 4.5), plus a roof that is not stated.
  - D: about 36.5-40 m (7 + 7 x 3.5..4 + 5).
  - A: 7 + 36 x 4 + 2 x 4.5 = 160 m, plus the technical floor, within the 165 m cap.
- **Homes:**
  - **458** in total, with about **70 hotel rooms** and about **1,500 m² of retail**. Source: DEVELOPER/PRESS:
    [sdedov.co.il, 22.12.2025](https://sdedov.co.il/%D7%94%D7%97%D7%9C-%D7%9E-3-75-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%9F-%D7%A9%D7%A7%D7%9C%D7%99%D7%9D-%D7%93%D7%9E%D7%A8%D7%99-%D7%9E%D7%AA%D7%97%D7%99%D7%9C%D7%94-%D7%A9%D7%99%D7%95%D7%95%D7%A7-%D7%91/)
    ("שני מגדלים בני 39 ו-16 קומות, ושני מבנים מרקמיים בני 8-9 קומות"; "458 יחידות דיור, כ-70 חדרי מלון").
  - Homes per building: **not found**. The unit table in the decision PDF did not extract.
  - Parking at the 1:1 standard: 485 spaces (OFFICIAL, section 2.3).
- **The floor count:**
  - The plan counts 40 floors: ground + 38 residential + technical.
  - The developer and our page say 39, which is probably ground + 38.
  - Both describe the same 38 residential floors (COMPUTED reading).
- **The DRAWING method:**
  - Source image: the ground-floor development drawing on p.3 of the decision (image object 36, 585 x 818 px). Lot 107
    fills the lower part of that image.
  - We read the four lot corners off the image and fitted them by least squares to the GIS corners. The south-east corner
    was taken where the east and south edge lines meet. The largest fit residual is 0.1 m.
  - We then read each building's outline off the same image.
  - Check: A's fitted area (907 m²) matches the official tower coverage (900 m²).
  - A's ground floor is recessed about 5 m from the south lot line, as the text says. Its upper outline in the drawing
    reaches within about 1 m of the line. The polygon below takes a middle value.

Building outlines in the stage frame (DRAWING, illustration grade):
```
A [[-46.0,3.1],[-15.9,3.1],[-15.8,33.2],[-45.9,33.3]]
B [[-47.1,-28.0],[14.5,-28.1],[14.5,-9.4],[-47.1,-9.3]]
C [[26.5,-28.2],[48.3,-28.2],[48.3,0.3],[26.5,0.4]]
D [[-2.7,12.9],[48.4,12.8],[48.4,26.4],[43.8,33.9],[39.2,35.6],[-3.8,35.7]]
```
The same outlines in latitude and longitude:
- A `(32.104493,34.783987)(32.104442,34.784301)(32.104174,34.784240)(32.104225,34.783927)`
- B `(32.104772,34.784038)(32.104666,34.784680)(32.104500,34.784642)(32.104605,34.784001)`
- C `(32.104646,34.784805)(32.104609,34.785032)(32.104355,34.784975)(32.104393,34.784748)`
- D `(32.104331,34.784418)(32.104244,34.784950)(32.104123,34.784923)(32.104065,34.784860)(32.104057,34.784809)(32.104131,34.784361)`

Draft stage parameters in the Rainbow style:
- A: `y0 = 7` (ground floor ≤7 m), `fh = 4`, `floors = 38` residential, the top two 4.5 m, a technical floor above,
  `cap = 165 m`. All OFFICIAL.
- The plan fixes no tower shape. The ground drawing shows a near-square plan, and balconies may project up to 2 m
  (OFFICIAL, section 2.2).

### 1.4 Facilities and where they are

| Facility | Place | Source |
|---|---|---|
| Pools | "בריכות שחיה ימוקמו על גג מבנה המלון ... או בתת הקרקע מתחת למלון". Building D's 9th floor is the residents' amenity floor with a pool, shared with hotel guests. Its roof is "שטח משותף". | OFFICIAL (sections 2.1ב, 2.4ז) |
| Private pools | In the top two residential floors of the tower (A) and of the mid-rise (C) | OFFICIAL (2.1ב) |
| Marketed pools and wellness | "בריכת אינפיניטי בקומת הגג" (the building is not named), a spa, gyms, a chef's kitchen, shared workrooms. [sdedov.co.il/project/dimri-yama](https://sdedov.co.il/project/dimri-yama/) also lists an indoor half-Olympic pool, sauna, jacuzzi, a yoga studio, a library, a kids' room and a wine room, without places. | DEVELOPER/PRESS |
| Lobbies | Ground floors: residents' lobbies in each building; the **hotel lobby in D, entered from the south** through the colonnade and also from the courtyard. B's lobby is entered from the inner courtyard. | OFFICIAL (2.1א, "2.1 קומת הקרקע") |
| Retail | Ground floors of A, C and D. B's ground floor is homes. A colonnade 5 m deep and 4.5 m high runs along the east and south streets. | OFFICIAL |
| Courtyard | An inner courtyard. All 4,004 m² of open space is a 24-hour public easement, crossing to the neighbouring spaces. | OFFICIAL (3.1) |
| Parking | 4 basement levels plus a bicycle gallery in the upper basement. The upper basement is about 8 m high. The ramp enters from the new street on the east and is covered by C. | OFFICIAL (2.1ב, 2.3) |
| Conflict | One sentence says "כניסה ראשית לחניון תהיה מהפינה הצפון מערבית". The ramp text and the drawing put it on the east, under C. We treat the north-west sentence as an error. | OFFICIAL (internal conflict) |
| Fire pads | South sidewalk between A and D; east sidewalk between C and D; north, between B and C | OFFICIAL (2.3) |

### 1.5 Our own tours and models (TOUR ESTIMATE, not official)

| Where | What it says | Compared with the official record |
|---|---|---|
| `experience/sde-dov/index.html` (the same file as `plugins/nadlan-config/assets/tours/sde-dov-tour.html`) | `pos [-38, 0, -150]` in the tour's own stylized frame (shore x = -183, Levi Eshkol x = 470). It is not tied to real coordinates, so it cannot be converted. | Use 1.1 instead. |
| The model: `assets/engine/rich-v1/spec-dimri.json`, generating `rich-dimri-v2.glb`, which is byte-identical to `showroom-engine/models/dimri-rich.glb` (the page model) | **One** building, 30 x 30 m, 39 floors x 3.2 m, a 2-floor podium (57 x 51 m), 6% taper, `seafront: true` (it draws a sea plate). The fallback in the tour is the same. `TOWER_TOP` is 129 m, with a beacon at 128.6 m. | B, C and D are missing. The official tower is up to 165 m. The lot is not on the waterline: Rainbow's lot, 141 m further south, is 713 m from the water. |
| The tour card | "39 קומות מעל פודיום", "458 דירות", tag "קו ראשון לים" | 458 is supported by the developer. "First line to the sea" has no support. |

### 1.6 Not read in this run

The final design-plan documents on the GIS record (id_taba 8210):
- `https://gisn.tel-aviv.gov.il/taba_raster/tamal3001_107_HI.pdf` (11.4 MB)
- `.../tamal3001_107_NI.pdf` (174 MB)

They are scanned images, above the fetch limit. If Dimri changed the layout after the committee decision of 10.5.2023,
the change would be there.

---

## 2. Ashira (Avisror Moshe & Sons), lot 101, Eshkol, Sde Dov

### 2.1 Reference point

| Item | Value | Source |
|---|---|---|
| Lot centroid (the stage origin) | **32.105643, 34.787673** | COMPUTED from GIS 837 (oid_migrash 44368). It is identical to our page's `lat`/`lng`. |
| Position in Rainbow's turned frame | x 252.6, z -322.4 m | COMPUTED. `quarter.json` unturned: (304.8, -273.7). |
| Block / parcel / lot | Block 6634, GIS parcel 2609, lot 101 in plan תמ"ל/3001. Land use "מגורים ומסחר" | OFFICIAL (GIS 837) |
| Area | 7,425.76 m² graphic, 7,393.33 m² registered. The plan says "7.406 דונם" | OFFICIAL |

### 2.2 Lot outline (OFFICIAL, GIS 837)

Latitude and longitude, from the south-east corner going clockwise:
`(32.105156, 34.788187) (32.105298, 34.787308) (32.105957, 34.787185) (32.106124, 34.787174) (32.105980, 34.788071) (32.105825, 34.788078) (32.105544, 34.788110)`

In the stage frame (GRID 11°):
`LOT_OUTLINE = [[57.9,43.6],[-26.5,44.0],[-51.8,-25.2],[-56.3,-43.2],[29.8,-43.7],[33.7,-27.0],[42.5,2.9]]`

- **Shape:** a parallelogram about 86 m wide and 88 m deep. The east and west edges are not square to the north and south.
  - South edge: 84.4 m at 281°.
  - West edge: 73.7 m at 351°, then 18.5 m at 357°.
  - North edge: 86.1 m at 101°.
  - East edge, along Levi Eshkol: 17.1 + 31.2 + 43.6 m at 178°, 174° and 170°.
- **Neighbours:** Levi Eshkol St. to the east, road no. 14 (a new street) to the west, open space 601 to the north, and
  open space 606 to the south. Source: committee agenda, p.173 (OFFICIAL).
- **Building lines:** 0 m on Levi Eshkol, on road 14 and toward open space 606; 3 m toward open space 601.
  Source: agenda, p.180 (OFFICIAL).

### 2.3 Buildings

Source: the Tel Aviv local committee agenda for meeting 23-0007ב of **3.5.2023**, item 13, "מגרש 101 אשכול דיון בעיצוב
ארכיטקטוני", PDF pp.171-190 (OFFICIAL):
<https://www.tel-aviv.gov.il/Residents/Development/DocLib/%D7%A1%D7%93%D7%A8%20%D7%99%D7%95%D7%9D%2023-0007%20%D7%9E%D7%99%D7%95%D7%9D%203-5-2023.pdf>

- The committee's lot 107 decision records that the lot 101 plan was approved at this meeting.
- GIS layer 528 (id_taba 8209) shows the design plan effective **12.5.2024**.

Four buildings: "מגדל בן 35 קומות, מגדלון בן 16 קומות ושני מבנים מרקמיים בגובה 9 קומות", framing a shared courtyard with a
public easement.

| Id | Kind | Floors (OFFICIAL) | Heights (OFFICIAL) | Homes (OFFICIAL, p.181 table and p.176 scheme) | Areas main / service, m² | Footprint centre (x, z) | Footprint size | Place |
|---|---|---|---|---|---|---|---|---|
| S1 | Tower on a podium ("מסד מגדל 1-7") | 35 including the ground floor; the technical floors are not counted | Typical about 3.5 m; the top penthouse floors about 4.5 m; ground 7 m; roof about 9.5 m; **total about 137 m** (136 in the table) | **202** (32 small, 53 medium, 117 large) | 18,173 / 7,843 | Podium (-15.7, 21.5) DRAWING | Podium 38.4 x 34.2 m, about 1,135 m² DRAWING. Tower plate above the podium: **944 m² including balconies (12.7%)**, with a cap of 950 m² (OFFICIAL). Where the plate sits on the podium is not fixed in the text. | **South-west** |
| S2 | Textural | 9, including ground and technical | Typical about 3.5 m; the top floor about 4.5 m; ground about 4-7 m; roof about 5 m; **total about 38 m** | **65** | 4,459 / 1,208 | (34.2, 29.1) DRAWING | 37.7 x 26.0 m, about 675 m² (the ground floor behind the colonnade) DRAWING | **South-east** (Levi Eshkol and open space 606) |
| N1 | Textural + public building | 9, including ground and technical. Floors 1-3 are wide and cover the ramp; floors 4-8 are narrower and set back. | **About 38 m** | **57** | 4,114 / 1,153 | (-30.9, -28.7) DRAWING | 45.1 x 25.4 m, about 915 m² (the wide lower part) DRAWING | **North-west** |
| N2 | Mid-rise over a textural base | Floors 1-7 textural, floors 8-16 mid-rise, then a technical roof (16 including the ground floor) | Typical about 3.5 m; ground about 4-7 m; roof about 8 m; **total about 70 m** | **82** | 7,428 / 2,629 | (24.5, -19.8) DRAWING | L-shape, 35.0 x 44.3 m, about 940 m² DRAWING | **North-east** (Levi Eshkol and open space 601) |

- **Totals (OFFICIAL):**
  - 406 homes: 101 small, 101 medium, 204 large.
  - 202 homes in the tower and 204 in the textural buildings.
  - Main areas 34,176 m²; service 12,835.13 m²; balconies 5,571.29 m².
  - Building coverage up to 58%; basement coverage 6,286 m² (85%).
- **Balcony projections (OFFICIAL, p.182):** N1 1.2 m to the north; N2 1.8 m to the east; S2 1.25 m to the east;
  S1 1.2 m to the west.
- **The tower (OFFICIAL, p.179):** "כלל המרפסות פונות מערבה". Its east facade is split by a glazed lift facade. It has a
  wavy ("גלית") profile.
- **Height check (COMPUTED):** 7 + 32 x 3.5 + 2 x 4.5 + 9.5 = 137.5 m, which agrees with the stated 137 m.
- **The DRAWING method:**
  - Source image: the development drawing on agenda p.177 (732 x 741 px). The lot outline is drawn in blue.
  - We fitted its four corners to the GIS corners. The residual is 0.2 m.
  - The building outlines follow the key-plan shapes on p.178.
  - The ground floors of S1 and S2 stand about 4.5 m behind the south lot line, which matches the 5 m colonnade. Their
    upper floors may reach the line, since the building line is 0 there.

Building outlines in the stage frame (DRAWING, illustration grade):
```
S1 [[-37.2,5.4],[0.9,5.2],[1.2,39.3],[-27.3,39.4]]                       // podium; tower plate 944 m² somewhere above it
S2 [[30.6,13.3],[42.5,13.3],[42.6,23.6],[49.4,23.5],[53.5,39.0],[16.0,39.2],[15.8,23.7],[30.6,23.6]]
N1 [[-53.4,-39.7],[-8.5,-39.9],[-8.4,-23.2],[-23.2,-23.2],[-23.1,-14.6],[-45.9,-14.4]]
N2 [[6.3,-40.0],[30.8,-40.1],[41.3,4.1],[20.8,4.2],[20.7,-21.7],[6.4,-21.6]]
```
The same outlines in latitude and longitude:
- S1 `(32.105660,34.787275)(32.105595,34.787672)(32.105292,34.787605)(32.105340,34.787309)`
- S2 `(32.105472,34.787964)(32.105452,34.788089)(32.105360,34.788068)(32.105349,34.788139)(32.105204,34.788151)(32.105267,34.787759)(32.105405,34.787790)(32.105380,34.787944)`
- N1 `(32.106087,34.787197)(32.106012,34.787665)(32.105864,34.787633)(32.105889,34.787478)(32.105812,34.787462)(32.105850,34.787224)`
- N2 `(32.105987,34.787819)(32.105946,34.788074)(32.105536,34.788095)(32.105570,34.787881)(32.105800,34.787932)(32.105824,34.787783)`

Draft stage parameters for S1:
- `y0 = 7`, `fh = 3.5`, 34 floors above the ground floor, the top floors 4.5 m, a roof of about 9.5 m, `H ≈ 137 m`
  (OFFICIAL).
- Tower plate ≤950 m² (OFFICIAL).
- The plate's position on the podium is **illustration**. The renders on p.176 show the tower rising out of the middle of
  the podium mass, not flush with its edges.

### 2.4 Facilities and where they are

| Facility | Place | Source |
|---|---|---|
| Pool | **Underground**: "בתת הקרקע: בריכת שחיה, חדרים טכניים, חדרי כושר". An English courtyard of up to 60 m² and up to 2.5 m wide brings light to it. | OFFICIAL (pp.175, 183) |
| Marketed pool and wellness | "בריכה חצי אולימפית פנימית", a kids' pool, a jacuzzi, a spa (dry and wet sauna, a salt room), a lounge with a bar, a cinema, a kids' area. [ashirabyavisror.com](https://ashirabyavisror.com/presale/) | DEVELOPER |
| Residents' clubs | **Three**, on the ground floors of N2, S1 and S2 | OFFICIAL (p.184) |
| Lobbies | The eastern buildings (N2, S2) are entered from Levi Eshkol. The tower (S1) is entered from the shared courtyard. N1's homes are entered from the west (road 14) and its public building from the north. | OFFICIAL (p.183) |
| Retail | Ground floors. Commercial frontage and a colonnade face west and south. A 5 m colonnade runs along the whole south facade (S1, S2). Shops open mainly to Levi Eshkol and the new street. | OFFICIAL (pp.175, 178, 184) |
| Public building | N1's ground floor: a kindergarten with 2 classes plus community space, 500 m² in all, and a fenced, shaded yard of 250 m². Also 225 m² of service space underground with 4 parking spaces. | OFFICIAL (p.181) |
| Courtyard | In the middle of the lot, with a public easement crossing north-south and east-west | OFFICIAL (p.178) |
| Parking | Basements over 85% of the lot. The upper basement is at least about 6 m deep, basement -2 about 3.5 m, typical levels about 3 m. The ramp opens in N1's frontage, inside the building. The number of levels is not stated in the extracted text. | OFFICIAL (pp.180, 183) |
| Roofs | Technical rooms and equipment. The textural roofs are the "fifth facade" seen from the towers. | OFFICIAL (pp.175, 182) |

### 2.5 Our own tours and models (TOUR ESTIMATE)

| Where | What it says | Compared with the official record |
|---|---|---|
| Sde Dov tour | `pos [415, 0, -60]` in the stylized frame. It cannot be converted. | Use 2.1. |
| `spec-ashira.json`, generating `rich-ashira-v2.glb`, which is byte-identical to the page model `ashira-rich.glb` | Four boxes, all with 3.2 m floors: 26 x 26 m x 35 floors at (0, 0); 30 x 22 x 16 at (+40, -8); 26 x 18 x 8 at (-38, +14); 24 x 18 x 8 at (-34, -22). `TOWER_TOP` is 116 m. | The official tower stands **south-west**, not in the middle, and is about 137 m tall. The official textural buildings are one north-west and one **south-east**; the model puts both on the west. They have 9 floors (including ground and technical), not 8. |
| Tour header and card | "34F + 15F + boutique 7-8F", "35 / 16 / 8 / 8" | Official: 35 (including ground) / 16 / 9 / 9. The developer's "8" is probably ground + 7 residential. |

---

## 3. DUO Tel Aviv (Africa Israel Residences), lots 111 + 112, Somail South

### 3.1 Reference point

| Item | Value | Source |
|---|---|---|
| Site centroid (the stage origin): the area-weighted centroid of lots 111 and 112 | **32.085698, 34.782856** | COMPUTED from GIS 837 |
| Our page's `lat`/`lng` (live REST, 28.9.2026) | 32.0847, 34.7824 | **118 m off** the site centroid. See section 5. |
| The location audit's "corrected" point (5.8.2026) | 32.085775, 34.782221 | 60 m west of the site centroid, near lot 41. It was never applied to the page. |

### 3.2 The site and the lot outline

- **Permit site (OFFICIAL):** block/parcel **6213/1468**, **8,338 m²**. Source: licensing authority decision 1-25-0172,
  21.9.2025, request 25-0263:
  <https://www.tel-aviv.gov.il/Transparency/DocLib3/%D7%A4%D7%A8%D7%95%D7%98%D7%95%D7%A7%D7%95%D7%9C%20%D7%94%D7%97%D7%9C%D7%98%D7%95%D7%AA%20%D7%A8%D7%A9%D7%95%D7%AA%20%D7%A8%D7%99%D7%A9%D7%95%D7%99%201-25-0172.pdf>
- **Plan lots in GIS 837 (OFFICIAL):** plan 2988א, "מתחם סמל דרום", effective 2.7.2013.
  - Lot **111** = parcel 1471, 4,379 m² registered, in the north.
  - Lot **112** = parcel 1472, 3,959 m² registered, in the south.
  - Land use "מגורים, מסחר ומבנים ומוסדות ציבור".
  - 4,379 + 3,959 = **8,338 m²**, exactly the permit's site area. So parcel 1468 is the two lots together
    (COMPUTED match).
- **Boundaries (OFFICIAL, decision of 21.9.2025):** Arlozorov St. to the **south**, Ibn Gabirol St. to the **west**,
  the "Givat Hamoreh" public open space to the **north**, Ben Saruk St. to the **east**.
- **Addresses (OFFICIAL, permit layer):** Arlozorov 85, 87, 89; Ibn Gabirol 112א, 118; Ben Saruk 1, 3.

Outline of lots 111 and 112 together, in latitude and longitude, clockwise from the north-west corner:
`(32.086196,34.782503) (32.086064,34.783410) (32.085679,34.783332) (32.085686,34.783284) (32.085620,34.783270) (32.085304,34.783202) (32.085271,34.783190) (32.085242,34.783169) (32.085212,34.783128) (32.085201,34.783104) (32.085192,34.783054) (32.085193,34.783028) (32.085331,34.782329) (32.085744,34.782412)`

In the stage frame (GRID 10°):
`LOT_OUTLINE = [[-42.3,-48.5],[44.5,-49.0],[44.6,-5.8],[40.0,-5.7],[40.0,1.7],[39.7,37.2],[39.3,41.0],[37.9,44.5],[34.6,48.4],[32.6,50.0],[28.1,51.8],[25.7,52.1],[-41.9,48.6],[-42.1,2.2]]`

- **Shape:** about 87 m (grid east-west) by 101 m (north-south), with a rounded south-east corner at Arlozorov and Ben Saruk.
- The line between lot 111 (north) and lot 112 (south) is at z ≈ +2.

### 3.3 Buildings

- **Layout (OFFICIAL, decision of 21.9.2025):**
  - "בחלקו המזרחי של המגרש 2 מגדלי מגורים", so the two towers stand in the east part of the site.
  - "ובחלקו המערבי של המגרש 3 מבני מסחר, פיתוח שטח וחצר שקועה", so the west part holds three commercial buildings and a
    sunken courtyard.
- **Tower footprints (OFFICIAL):** city GIS layer 513, which already holds both towers, each marked with 53 floors. The
  ids and areas are in the table below.

| Id | Kind | Floors | Footprint (OFFICIAL, GIS 513) | Centre (x, z) | Size (grid E-W x N-S) | Place |
|---|---|---|---|---|---|---|
| North tower | Residential tower (lot 111) | **54, of them 50 residential**: Africa Israel's annual report and the full permit of 30.12.2021 (via the ledger below). GIS 513 marks 53. | oid 44499, 1,082 m². Latitude and longitude: `(32.0861028,34.7829518)(32.0860576,34.7832710)(32.0857453,34.7832045)(32.0857962,34.7828751)` | (16.1, -28.3), which is 32.085925, 34.783076 | 31.8 x 35.1 m | East half, north |
| South tower | Residential tower (lot 112) | 54 / 50 residential, as above | oid 42941, 918 m². Latitude and longitude: `(32.0855417,34.7828404)(32.0854923,34.7831789)(32.0852358,34.7831134)(32.0852869,34.7827869)` | (17.5, 31.5), which is 32.085390, 34.782980 | 32.5 x 29.0 m | East half, south |
| Lobby building | The main lobby connects the towers, with the pool on its roof | Ground floor about 7 m (DEVELOPER) | Not in GIS | Between the towers: the gap is **28 m** along the grid (COMPUTED) | Not known | Between the towers |
| Commercial buildings (3) | Retail, over up to 3 floors (the western commercial building: ground, 1, 2, 3 and a technical roof) | Named "מסחר מערבי / צפוני / דרומי" | Not in GIS | West half | Not known | West half, around a sunken patio with escalators |

- **Floor schedule (OFFICIAL, the changes approved on 21.9.2025):**
  - A residential gallery floor.
  - Residential floors 1 to 50.
  - Penthouse floors 48-50, with the private pools moved on 49-50.
  - Technical roof floors 51 and 52.
  - Basements 1 to 5. The basement 1 changes cover "חיבור לבניין העירייה" (a connection to the municipality building)
    and transformer niches "למנהרה" (for the tunnel).
- **Height: no official number found.**
  - The tour header's "about 200 m" is from a forum only.
  - GIS 513 stores `dsm_mean = 180` for both towers, with no documented meaning. Do not use it.
  - Typical floor height: not found.
- **Homes (OFFICIAL):** 668 in all (permit 20210784 of 29.12.2021, GIS 772), of which 510 are the partners' marketable
  pool (annual report).
- **Other areas (OFFICIAL, filings via the ledger):**
  - Commercial: 9,620 m² main area; about 13,000 m² gross.
  - Public building: 2,140 m² gross in the municipal agreement.
  - Yashar Architects: "1000 square meters of civic space with an independent entrance" in the **north-east corner**
    (ARCHITECT, [yashararch.com](https://yashararch.com/projects/duo/)).
- **Ledger:** `docs/content/wave1/duo-tel-aviv-content-package-2026-08-04/research-source-ledger-draft.md` (S02, S05,
  S06, S13).

### 3.4 Facilities and where they are

| Facility | Place | Source |
|---|---|---|
| Pool | An outdoor infinity pool "על גג מבנה הלובי בין שני מגדלי המגורים", plus a toddler pool | DEVELOPER ([duo-tlv.com/residential-towers](https://www.duo-tlv.com/residential-towers/)) |
| Pool (municipal) | "קומה 1 מגורים": the residents' amenities, the pool plaza's skylight, the toddler pool's position, and a shade pergola for the swimming pool. This fits a pool deck one level above the street. | OFFICIAL (decision 21.9.2025) |
| Private pools | Penthouse floors 49-50 | OFFICIAL (same decision) |
| Lobby | Ground floor about 7 m high, the main lobby joining both towers as an "internal street"; a lobby on every floor | DEVELOPER |
| Wellness, gym, club | A wellness complex with its own entrance straight from the lobby; a gym; a residents' club. The floor is not given. | DEVELOPER |
| Retail | Three commercial buildings in the west half, a sunken courtyard, and a multi-level commercial complex | OFFICIAL; ARCHITECT |
| Parking | 5 basement levels | OFFICIAL |

### 3.5 Our own tours and models (TOUR ESTIMATE)

| Where | What it says | Compared with the official record |
|---|---|---|
| `experience/somail/index.html` (the same file as `plugins/nadlan-config/assets/tours/somail-tour.html`) | `pos [170, 0, 80]` in a stylized frame: +Z north, Ibn Gabirol at x = 60, Arlozorov at z = 0, distances compressed about 15%. It cannot be converted. | Use 3.1. |
| `spec-duo.json`, generating `rich-duo-v2.glb`, which is byte-identical to the page model `duo-rich.glb` | Two towers of 30 x 30 m, 50 floors x 3.1 m, **side by side east-west** at x = -26 and x = +26; a 3-floor podium under one. | The real towers stand **one north of the other, both in the east half**, 28 m apart, with footprints of 1,082 and 918 m². |
| The tour's fallback | Two towers of 30 x 26 m, 54 floors x 2.9 m, at x = -42 and x = +42 | Same issue. |

---

## 4. H-Infinity (Hagag Group), lot 124, Somail North

### 4.1 Reference point

| Item | Value | Source |
|---|---|---|
| Lot centroid (the stage origin) | **32.087284, 34.782720** | COMPUTED from GIS 837 (lot 124, plan 2988ב) |
| Our page's `lat`/`lng` (post 6548) | 32.086, 34.7821, marked `conf: address-approx` | **154 m off**. See section 5. |
| Block / parcel | **6213 / 1493**, **3,167 m²** registered (3,031.71 m² graphic). Land use "מגורים, מסחר ומבנים ומוסדות ציבור". | OFFICIAL (GIS 837), and it matches Hagag's 2025 annual report, footnote 138: "מגרש בשטח כולל של 3,167 מ"ר הידוע כגוש 6213 חלקה 1493" |
| Street address on the permit | Ibn Gabirol 128 | OFFICIAL (GIS 772, request 20190089) |

### 4.2 Lot outline (OFFICIAL, GIS 837)

Latitude and longitude, from the north-west corner going clockwise:
`(32.087540, 34.782383) (32.087439, 34.783100) (32.087019, 34.783016) (32.087076, 34.782632) (32.087094, 34.782636) (32.087139, 34.782340) (32.087444, 34.782403) (32.087450, 34.782364)`

In the stage frame (GRID 10°):
`LOT_OUTLINE = [[-36.2,-22.4],[32.4,-23.1],[32.6,24.0],[-4.2,24.1],[-4.2,22.0],[-32.5,22.0],[-32.5,-12.3],[-36.2,-12.3]]`

- **Edges:**
  - North: 68.6 m at bearing 99°.
  - East: 47.1 m at 190°.
  - South: 36.8 + 28.3 m, with a 2.1 m jog.
  - West, on Ibn Gabirol: 34.3 + 10.1 m, with a 3.7 m jog.
- **The compound (OFFICIAL, Hagag report section 6.8.3.3.3):** Somail sits at Ibn Gabirol and Arlozorov, split into a
  south and a north compound. "הפרויקט מוקם בחלקו הצפוני". Each compound plans 2 towers of about 50 floors and 3 textural
  buildings of up to 8 floors.
- **Neighbours (OFFICIAL: GIS 837 and permits in GIS 772), useful as the stage's quarter:**
  - **North: lot 121.** Parcel 1490, 3,110 m². It is Hagag's own future "Somail 121" project, 80% held through a
    partnership (Hagag report). It sits at the Ibn Gabirol and Jabotinsky corner.
  - **East: lot 122.** Parcel 1491, Africa Israel's north tower. Permit 20240457 of 14.4.2024: 50 residential floors,
    226 homes, 330 parking spaces, a public building of 1,500 m². A 4/2026 request adds a roof pool at floor 50.
  - **East: lot 123.** Parcel 1492. Permit 20231349: a textural building of 8 floors including the ground floor, 31 homes,
    over 4 shared basement levels.
  - **South:** plan 4067, open space and public buildings. The new municipality tower stands there: GIS 513 oid 40141,
    25 floors, footprint 1,928 m².
  - **West:** Ibn Gabirol St.

### 4.3 Buildings

Hagag Group's annual report for 2025 (published 4.2026), section 6.8.3.3.3 (OFFICIAL, TASE filing):
<https://www.hagag-group.co.il/Uploads/2026/04/rln33jws7WiMM6.pdf>

It says: "ביום 22 בדצמבר 2021 התקבל היתר בניה וביום 9 בדצמבר 2024 התקבל היתר שינויים לפרויקט, המתירים הקמת **מגדל
מגורים בן 53 קומות** לצד **מבנה מרקמי בן 6 קומות מגורים מעל קומת מסחר**, ובהם סך כולל של **כ-278 יחידות דיור** וכ-267
מ"ר ברוטו שטח מסחרי."

- The planning table gives **278** homes and 29,425 m² of residential area.
- The city's permit layer holds the 2021 permit: permit 20210989 of 22.12.2021, request 20190089, Ibn Gabirol 128.
  It lists "קומה מסחרית עבור: מסחר, כמות קומות מגורים: 49, כמות יח"ד מבוקשות: 273", a gym and one shop on the ground
  floor, and 346 parking spaces. The 2024 change permit raised these to 53 floors and 278 homes.

| Id | Kind | Floors | Footprint | Centre (x, z) | Size | Place |
|---|---|---|---|---|---|---|
| Tower | Residential tower | **53** (OFFICIAL, amended permit of 9.12.2024). The 2021 permit had 49 residential floors plus a commercial floor. The developer's page says 52. | The permit-layer polygon 1, which is the same polygon as **GIS 513 oid 45729**: **623 m²**, a square of 25.4 x 25.1 m. Latitude and longitude: `(32.0871878,34.7826675)(32.0874062,34.7827108)(32.0873743,34.7829718)(32.0871501,34.7829332)` | (9.5, -1.2), which is 32.087279, 34.782821 | 25.6 x 25.3 m | East-centre of the lot |
| Low building | Textural: 6 residential floors over a commercial floor | 7 above ground (OFFICIAL). The developer says "בניין בוטיק בן 7 קומות". | The permit-layer polygon 2: **313 m²**, 13 x 27 m. Latitude and longitude: `(32.0872495,34.7823357)(32.0874874,34.7823657)(32.0874734,34.7824951)(32.0872340,34.7824534)` | (-30.0, -3.6), which is 32.087363, 34.782413 | 13.0 x 27.0 m | West edge, on Ibn Gabirol |

- **What the two polygons are:** both are attached to the H-Infinity permit (20210989) in the city's permit layer.
  - We read polygon 1 as the tower footprint (COMPUTED from its size). The buildings layer lists it as a building, with a
    DSM maximum of 78.6 m at the survey date, which suggests the structure was still rising. Its "floors" field is a
    placeholder (1).
  - We read polygon 2 as the low building, from its size and its position on the Ibn Gabirol shop frontage. No record
    names either role, so both roles are inferred.
  - The two centres are 39.6 m apart (COMPUTED).
- **Height: no official number found.** Hagag's page gives "לובי כניסה המתנשא לגובה של כ-10 מטרים". Floor heights: not
  found.
- **Status (OFFICIAL):**
  - The same report: "בניית הפרויקט נמצאת בעיצומה".
  - The permit layer lists permit 20210989 as "בניה חדשה מגדל מגורים מעל 20 קומות" at the stage "בבניה", with a
    works-start date field of 11.11.2025.

### 4.4 Facilities and where they are

| Facility | Place | Source |
|---|---|---|
| Lobby | Entrance lobby about 10 m high | DEVELOPER ([hagag-group.co.il](https://www.hagag-group.co.il/projects/ResidentProjects/h_infinity)) |
| Pool | "בריכת אינפיניטי מרשימה המשקיפה אל קו החוף". The floor is **not stated**. | DEVELOPER |
| Gym | On the ground floor (2021 permit: "בקומת הקרקע: אולם כניסה ... אחר: חדר כושר"). The developer says "מתקני כושר מתקדמים". | OFFICIAL / DEVELOPER |
| Residents' room, park | "חדר דיירים מפואר", "פארק לרווחת התושבים". Places are not stated. | DEVELOPER |
| Retail | About 267 m² gross, in the commercial floor under the low building (OFFICIAL). The 2021 permit also lists one shop on the tower's ground floor. | OFFICIAL |
| Roof | 2021 permit: exit rooms, machine rooms, air-conditioning plant, a pergola | OFFICIAL |
| Parking | 346 spaces (2021 permit). The number of basements is not stated. | OFFICIAL |

### 4.5 Our own tours and models (TOUR ESTIMATE)

| Where | What it says | Compared with the official record |
|---|---|---|
| Somail tour `NPROJECTS` entry `h-infinity` | `x 152, z 262` in the stylized frame. A tower of 25 x 23 m x 52 floors x 3.0 m (156 m). A "boutique" of 15 x 12 m x 7 floors, **26 m east and 10 m north** of the tower. `un: 200`. Card "52 + 7", "כ-200 דירות". | Official: 53 floors and about 278 homes. The likely low building is **west** of the tower, on Ibn Gabirol. |
| Page model `h-infinity.glb` (generator `docs/playbooks/glb-gen-h-infinity.py`) | Total height **187 m** (no source); 52 floors; a 2-floor podium, 5 m per floor; a 6 m crown; an elliptical plan of about 31 x 25 m narrowing to 28 x 23 m; a boutique of 7 floors x 3.3 m, an ellipse of 18 x 14 m placed **24 m east** of the tower | The height has no source, and the low building is on the wrong side. The real tower footprint is a 25 m square of 623 m². |
| Page meta (post 6548) | `num_floors 52`, `num_units 242` | Official: 53 and about 278 |

---

## 5. Findings on our own pages and tours (flagged, not fixed in this run)

1. **DUO page position.** `lat`/`lng` 32.0847, 34.7824 is 118 m from the site centroid (32.085698, 34.782856). The
   location audit of 5.8.2026 proposed 32.085775, 34.782221, but that point is itself 60 m west of the site, and it was
   never applied.
2. **H-Infinity page position and text.**
   - `lat`/`lng` 32.086, 34.7821 is 154 m from lot 124.
   - The page's text says "אבן גבירול ממזרח, ז'בוטינסקי מדרום ... ארלוזורוב מצפון". That is reversed: the municipal record
     has Ibn Gabirol on the west, Arlozorov on the south and Jabotinsky on the north.
   - The page's address "אבן גבירול פינת ז'בוטינסקי" is the corner of lot 121, Hagag's other lot. H-Infinity is lot 124,
     at Ibn Gabirol 128.
   - The page shows 52 floors and 242 homes. Hagag's 2025 filing gives 53 floors and about 278 homes.
3. **Somail tour.** H-Infinity has "52 + 7, about 200 homes", and the low building is on the east side. Both are out of
   date or wrong.
4. **DUO model.** The towers stand east-west, side by side. The real towers stand north-south, in the east half.
5. **Ashira model.** The tower is drawn in the middle, with both textural buildings on the west and 8 floors. The real
   tower is south-west, the textural buildings are north-west and south-east, and they have 9 floors including ground and
   technical.
6. **Dimri model and card.**
   - The model has a single building and a sea plate.
   - The card's "קו ראשון לים" has no support: the lot is about 0.7 km from the water.
   - Three of the four buildings are missing.
7. **Rainbow's lot outline.** The layer 837 outline of lot 111 has 8,669 m² and a rounded south-east corner. Rainbow's
   `LOT_OUTLINE` came from the design-plan snapshot (8,504 m²). The two outlines differ by a few metres at the corners.
   This is only for consistency if the stages share a frame.

---

## 6. Summary: what is solid and what is estimated

| Project | Solid (official record or filing) | Estimated or unknown |
|---|---|---|
| **Dimri Yama (lot 107)** | Reference point and lot outline (GIS 837). Block 6634. Boundaries and building lines. Four buildings with kinds, floors (40 / 16 / 9 / 9), floor heights, the tower's 165 m cap, the tower's 900 m² coverage. Each building's quadrant (tower south-west, mid-rise north-east, hotel building south-east, residential bar north). Areas per building. Pools on the hotel building's roof or under it. Private pools on the top floors. Hotel lobby from the south. Colonnades. 4 basements with the ramp under the mid-rise. | Exact footprints (DRAWING, ±2-3 m; the tower's area checks out against the official 900 m²). Heights of B, C and D (COMPUTED from floor heights). Homes per building (not found). 458 homes, about 70 hotel rooms and about 1,500 m² of retail are DEVELOPER/PRESS. The final 2025 plan was not read (scanned). |
| **Ashira (lot 101)** | Reference point and lot outline (GIS 837). Boundaries and building lines. Four buildings with quadrants (S1 tower south-west, S2 south-east, N1 north-west, N2 mid-rise north-east), floors, heights (about 137 / 38 / 38 / 70 m), homes per building (202 / 65 / 57 / 82), the tower plate ≤950 m² (944), balcony directions. Pool and gym underground. 3 residents' clubs. Kindergarten in N1. Ramp in N1. | Exact footprints (DRAWING, ±2-3 m). Where the tower plate sits on its podium (illustration). The number of basement levels. |
| **DUO (lots 111 + 112)** | Site 6213/1468, 8,338 m² = lots 111 + 112 (GIS 837). Boundaries. Both **tower footprints** (GIS 513: 1,082 and 918 m²). Towers in the east half, 3 commercial buildings and a sunken courtyard in the west half. 54 floors (50 residential), the floor schedule (penthouses 48-50, technical 51-52), 5 basements, 668 homes. | **Height and floor-to-floor height** (not found). The lobby building's outline and the commercial buildings' outlines (not in GIS). The pool's exact outline (DEVELOPER plus the municipal "floor 1"). |
| **H-Infinity (lot 124)** | Lot 6213/1493, 3,167 m², and its outline (GIS 837 plus the Hagag filing). 53 floors plus a low building of 6 residential floors over retail, about 278 homes, about 267 m² of retail (Hagag 2025 filing). The 2021 permit's data (49 residential floors, 273 homes, 346 parking spaces, gym on the ground floor). The neighbours' permits. | The **roles** of the two permit polygons (tower 623 m², low building 313 m²) are inferred from size and place. **Height** not found. The pool's floor is not stated. Floor heights are unknown. |

**Bottom line:**
- For all four projects, the lot outlines, reference points and floor counts are official.
- Building positions are official by quadrant and drawn to about ±2-3 m for the two Sde Dov lots.
- Building positions are exact for DUO's towers (city GIS) and inferred for H-Infinity.
- Only the heights of DUO and H-Infinity, and the tower plate's position on Ashira's podium, have no source. They must be
  labelled "illustration" if drawn.
