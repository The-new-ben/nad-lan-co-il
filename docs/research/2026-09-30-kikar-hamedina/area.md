# Kikar Hamedina, P2: the area (30.9.2026)

Research only, local. Nothing here is on the live site; the registry moves into `plugins/nadlan-config/assets/project-stage/kikar/` at release (P7).
Every line carries its source. "Not found" means we looked and no source gave it.

**Files in this folder**
- `places.json`: the place registry, same schema as `assets/project-stage/duo/places.json` (plus optional fields `info`, `lines`, `rides`, `line`, `opens`, `layer`).
- `city-blocks.json`: every building within 700 m with footprint and height (and its source), the notable towers within 2 km, the plot, the street axes, the green areas, the distance to each road.
- `sight-landmarks.json`: what a high floor may see, by direction, with coordinates. Visibility is not computed yet (P5).
- `eye-kikar-provisional.json`, `kikar-stage/quarter.json`, `kikar-stage/city.json`: the inputs `build_places.py` needs until the stage exists.
- Scripts: `build_area_kikar.py` (step 1), `scripts/project-stage/build_places.py kikar` (step 2), `enrich_places_kikar.py` (step 3).

## 1. The plot, located

**Plot centre: 32.086758, 34.789776.** It is the area-weighted centroid of plan 2500ב's lots that are not roads (lots 101, 201-208 and 303, 47,846 m² together), from the Tel Aviv-Yafo GIS lots layer 837. Cross-check: OpenStreetMap's construction area "פרויקט כיכר המדינה" (way 727196846) centres 11 m away (32.086854, 34.789805); OSM's point for the square itself (way 26260278) is 32.0868637, 34.7898471.

| Lot (plan 2500ב) | Use (as the layer names it) | Registered area |
|---|---|---|
| 101 | מגורים ד' | 28,380 m² |
| 201 | פרטי פתוח | 2,044 m² |
| 202 | פרטי פתוח | 94 m² |
| 203 | פרטי פתוח | 405 m² |
| 204 | פרטי פתוח | 599 m² |
| 205 | פרטי פתוח | 767 m² |
| 206 | פרטי פתוח | 550 m² |
| 207 | פרטי פתוח | 631 m² |
| 208 | פרטי פתוח | 166 m² |
| 303 | שטחים פתוחים ומבנים ומוסדות ציבור | 13,812 m² |
| 501 | דרך מאושרת | 14,870 m² |
| 502 | דרך מאושרת | 14,526 m² |

Source: [TLV GIS layer 837](https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/837), block (gush) 6213, read 30.9.2026. The towers stand on lot 101 (residential). Lot 303 (west) holds the new school and community centre.

**The plans** (TLV GIS layer 528):
- **2500**: ככר המדינה; status: בתוקף; in force from 2000-08-03. Documents: https://gisn.tel-aviv.gov.il/tabaot/docs.aspx?id_taba=727&st_taba=2500&mode=internet
- **2500א**: כיכר המדינה - המרת מסחר במגורים ושינוי בינוי; status: בתוקף; in force from 2013-06-24; 453 housing units, 59,175 m² housing, 6,000 m² public buildings. Documents: https://gisn.tel-aviv.gov.il/tabaot/docs.aspx?id_taba=6012&st_taba=2500א&mode=internet
- **2500ב**: כיכר המדינה שינוי הסדרי תנועה; status: בתוקף; in force from 2018-03-20. Documents: https://gisn.tel-aviv.gov.il/tabaot/docs.aspx?id_taba=6627&st_taba=2500ב&mode=internet

**The three towers** (TLV GIS buildings layer 513; names, floors and heights are the layer's own fields):

| Tower | Centre (lat, lng) | From the plot centre | Floors | Height | Height source |
|---|---|---|---|---|---|
| Tower A | 32.086160, 34.789337 | 78 m, bearing 212° | 40 | 160.0 m | DSM mean (dsm_mean) |
| Tower B | 32.086348, 34.790444 | 78 m, bearing 126° | 40 | 158.2 m | DSM mean (dsm_mean) |
| Tower C | 32.087330, 34.790202 | 75 m, bearing 32° | 40 | 160.0 m | DSM mean (dsm_mean) |

- Tower A is to the south-west, B to the south-east and C to the north-east. Each footprint is about 1,210-1,220 m², and OSM ways 1180213994-6 give the same three footprints.
- This agrees with Hebrew Wikipedia as quoted in `facts.md` (A and C the south and north towers, B the east tower).
- **Conflict for P1:** the city's layer gives tower B 40 floors and 158.2 m. Wikipedia and Ashtrom give 37 floors (157 m, and "37 - 40 floors" on [Ashtrom's page](https://www.ashtrom.co.il/en/projects/kikar-hamedina)). The city's construction-site record (below) lists a permit request for "2 more floors for building B". Which is final is not settled here.
- **The building-site record** (TLV GIS layer 499, file 61-1-2018-0391, read 30.9.2026): stage "גמר שלד" as of 2026-04-23; works started 2022-06-06; permits 20181007, 20220484, 20220688, 20220958, 20221436, 20241393, 20241394, 20251961, 20251962; addresses רחוב הא באייר מס' 45,  רחוב הא באייר מס' 65,  רחוב הא באייר מס' 25. The record's text lists 40 residential floors, 453 units, and a spa, pool (290 m³) and gym in the basements.

**The public buildings on lot 303** (the west of the square):
- The municipality's design plan 2500ב/1 (local committee decision 21-0018ב-3, 4.8.2021, [PDF](https://www.tel-aviv.gov.il/Residents/Development/DocLib/2500%D7%91-%D7%9B%D7%99%D7%9B%D7%A8%20%D7%94%D7%9E%D7%93%D7%99%D7%A0%D7%94%20%D7%9E%D7%91%D7%A0%D7%99%20%D7%A6%D7%99%D7%91%D7%95%D7%A8%20%D7%A2%D7%99%D7%A6%D7%95%D7%91.pdf)): the **north** building is an elementary school of 18 classes plus 6 special-education classes, with an underground sports hall; the **south** building is a community centre (4 floors, up to 7), which also serves the park. Address ה' באייר 75; plan area 13.8 dunam. The two buildings flank an open walk that continues Jabotinsky Street into the centre of the park.
- TLV GIS layer 513: the north building (oid 43143) has 5 floors, built 2026, no name; the south building (oid 43109) has 5 floors, built 2025, named "מרכז קהילתי".
- The 2026-27 schools layer (769) lists two schools at ה' באייר 75: "כיכר המדינה" (elementary, state) and "מאיר שלו - חט"ב" (middle school).
- **Conflict:** OSM names the north building "בית הספר כיכר המדינה" (way 1560991906) and the south one "תיכון עירוני כ"ה ע"ש מאיר שלו" (way 1560991907); the community layer (553) puts the community centre's point in the north building. We follow the municipal design plan and the buildings layer.

**The park and the lake on the plot:**
- Globes, 2.5.2022: "באמצע המתחם יוקם פארק ציבורי שיכלול גם אגם מלאכותי" ([Globes](https://www.globes.co.il/news/article.aspx?did=1001410751)); the same article: 15 dunam go to the municipality, including a new school.
- English Wikipedia: "a 10-acre public park, an artificial lake, green areas and pedestrian avenues" ([Kikar Hamedina](https://en.wikipedia.org/wiki/Kikar_Hamedina)).
- Ashtrom's English page does not say "lake"; it lists "ecological pools, running and cycling tracks, playgrounds, and a dog park" ([Ashtrom](https://www.ashtrom.co.il/en/projects/kikar-hamedina)).
- Size: the press conflicts: up to 3.5 dunam (TheMarker and Calcalist, 11.2015) against 8 dunam (Globes, 16.9.2017). See `facts.md` section 1.8 (P1), which also lists the park size conflicts (26 to about 50 dunam).
- **Not found:** the lake's outline and its place on the plot. The landscape plan (design plan 2500א) was not readable from a public source today. P5 must not draw a lake shape until it is found.

## 2. The square's character

- A round square ringed by the one-way street ה' באייר (OSM way 5118376, 128-147 m from the plot centre). Weizmann meets it from the south and Jabotinsky from the east (OSM; TLV GIS 507).
- The municipality's neighbourhood name is "הצפון החדש - סביבת ככר המדינה" (TLV GIS layer 511).
- English Wikipedia calls it "the epicenter of high international fashion in Tel Aviv", with luxury shops on the ground floors of the ring's residential buildings ([Wikipedia](https://en.wikipedia.org/wiki/Kikar_Hamedina)).
- **Shops on the ring, as the sources name them** (within 190 m of the plot centre, the ring's ground floors):
  - OpenStreetMap: Bamoss Square, City Market, DoDo, Flower Lab, Gucci, KISU, LA GARCONNIÉRE, Maison 24, Michal Outlet, Miele, Nuchi, Padani, Royal Diamonds, Royal Lux.
  - The city's business-licence data via findplace.co.il (TLV open data): Open, TOLLMAN'S, ZEST, א.קאשי, אורמן, בוטיק סנטרל, בייקרי כיכר המדינה, בית הבטיחות, גאט מקסימום, גלרית הזהב, הקערה, זריה וסימון, כרונו טיים, לחם ארז, מונסטון, מוקאיה שוקולד, מחסן לחנות פרחים לה רוז, מכירת תבלינים, מנימרקט כיכר המדינה, מעדני דניאל, מרינדו, מרקט אקספרס, נוצ'י סושי אנד,מחסן 15175, נוצי סושי אנד בר, נטו עיצוב מערכות - מרתף, נטו עיצוב מערכות - קרקע, נספרסו ישראל, פדני, רותי שוקולדים, רמות.
  - No other brand is named here: we name only what OSM or the city's data name.
- **Building all around the ring:** the city's building-site layer (499) has 16 other building-site files within 250 m of the plot centre (read 30.9.2026). Most are TAMA 38 / urban-renewal rebuilds of 7-9 floors (for example ז'בוטינסקי 133 and 135-137, משה שרת 60 and 66). The ring is being renewed while the towers rise.

## 3. The 30 most useful places

Walking minutes: Mapbox walking profile, from the ring road on the side facing the place (see section 9). Distance: straight line from the plot centre.

| Place | What | Walk (min) | Distance (m) | Source |
|---|---|---|---|---|
| כיכר המדינה | elementary school on the plot (ה' באייר 75) | 1 | 102 | TLV open data + TLV GIS |
| מאיר שלו - חט"ב | middle school, ה' באייר 75 | 1 | 102 | TLV open data (findplace) |
| מרכז קהילתי כיכר המדינה | community centre on the plot | 1 | 91 | TLV open data + TLV GIS |
| ענן | kindergarten, חברה חדשה 11 | 1 | 186 | TLV open data + OSM + TLV GIS |
| קרינה ורחל | daycare, משה שרת 11 | 1 | 229 | TLV open data + TLV GIS |
| גמנסיה הרצליה-חט"ב | Herzliya Hebrew Gymnasium, ז'בוטינסקי 106 | 4 | 406 | TLV open data + TLV GIS |
| אהבת ציון | elementary school, כהנשטם 16 | 3 | 370 | TLV open data + TLV GIS |
| כיכר המדינה/וייצמן | bus stop | 1 | 141 | TLV open data + OSM; lines on 8.9.2026: 3, 7, 14, 66, 89, 90 |
| כיכר המדינה/אריה עקיבא | bus stop | 1 | 141 | TLV open data + OSM; lines on 8.9.2026: 5, 7, 14, 66, 89 |
| דרך נמיר/ז'בוטינסקי | bus stop | 5 | 520 | GTFS; lines on 8.9.2026: 5, 40, 44, 47, 71, 72, 91, 116, 148, 149, 159, 171, 193, 248, 249, 270, 271, 272, 274, 282, 299, 347, 349, 450, 464, 474, 501, 506, 532, 600, 601, 602, 603, 605, 606, 607, 611, 623, 632, 633, 650 |
| תחנת איכילוב, הקו הסגול | Purple Line station, planned 2028 | 2 | 350 | TLV GIS (layer 766); planned, 2028 |
| תחנת אבן גבירול, הקו הסגול | Purple Line station, planned 2028 | 9 | 708 | TLV GIS (layer 766); planned, 2028 |
| תחנת ארלוזרוב, הקו האדום | Red Line station, running | 11 | 859 | OSM + TLV GIS; running since 18.8.2023 |
| תל אביב סבידור מרכז | Israel Railways station | 9 | 852 | OSM |
| סוראסקי-איכילוב | Ichilov hospital, ויצמן 6 | 9 | 845 | TLV GIS (layer 565) |
| כללית | Clalit clinic, בארי 27 | 4 | 424 | OSM + TLV GIS |
| סופר פארם ויצמן ת"א | pharmacy, ויצמן 53 | 1 | 215 | TLV GIS (layer 564) |
| City Market | supermarket | 1 | 152 | OSM |
| ויקטורי | supermarket | 1 | 211 | OSM |
| בייקרי כיכר המדינה | café | 1 | 158 | TLV open data (findplace) |
| לחם ארז | café | 1 | 158 | OSM |
| Training Room | gym | 1 | 152 | OSM |
| גן אברהם | park | 2 | 206 | OSM |
| חורשת ליסין | dog park, ליסין 20 | 4 | 400 | TLV open data + TLV GIS |
| פארק הירקון (גני יהושע), ליד בני דן | Park HaYarkon, nearest edge | 13 | 1,020 | OSM |
| ספורטק צפון | Sportek (in Park HaYarkon) | 22 | 1,262 | OSM |
| ארלוזורוב 97 - הקאנטרי הקהילתי במרכז | community country club | 5 | 444 | OSM + TLV GIS |
| תיאטרון בית החייל תל אביב | Beit Hahayal theatre, ויצמן 60 | 6 | 425 | TLV open data + TLV GIS |
| ספריית הגימנסיה הרצליה | library | 3 | 388 | OSM |
| מוזיאון תל אביב לאמנות | Tel Aviv Museum of Art | 14 | 1,070 | TLV GIS (layer 745) |

## 4. Transport

**Light rail and rail** (stations: TLV GIS layers 423 red, 764 green, 766 purple; OSM for Israel Railways):

| Station | Line | Status | Walk (min) | Distance (m) |
|---|---|---|---|---|
| תחנת איכילוב, הקו הסגול | Purple | planned, 2028 | 2 | 350 |
| תחנת אבן גבירול, הקו הסגול | Purple | planned, 2028 | 9 | 708 |
| תחנת ארלוזורוב, הקו הירוק | Green | planned, by 2030 (the Tel Aviv section) | 9 | 730 |
| תחנת תל אביב מרכז, הקו הסגול | Purple | planned, 2028 | 10 | 750 |
| תל אביב סבידור מרכז | Israel Railways | running | 9 | 852 |
| תחנת ארלוזרוב, הקו האדום | Red | running since 18.8.2023 | 11 | 859 |
| תחנת יהודה המכבי, הקו הירוק | Green | planned, by 2030 (the Tel Aviv section) | 11 | 961 |
| תחנת רבין, הקו הירוק | Green | planned, by 2030 (the Tel Aviv section) | 13 | 1,069 |
| תחנת שאול המלך, הקו האדום | Red | running since 18.8.2023 | 17 | 1,118 |
| אבא הלל | not in the city's layers (Ramat Gan; OSM station) | not found | 17 | 1,312 |
| אבא הלל | not in the city's layers (Ramat Gan; OSM station) | not found | 17 | 1,322 |
| תחנת דיזנגוף, הקו הסגול | Purple | planned, 2028 | 18 | 1,399 |

- **Red Line: running.** It opened on 18.8.2023 ([Wikipedia, Red Line](https://en.wikipedia.org/wiki/Red_Line_(Tel_Aviv_Light_Rail)); [Bloomberg, 18.8.2023](https://www.bloomberg.com/news/features/2023-08-18/tel-aviv-light-rail-opens-red-line-with-stops-from-bat-yam-to-petah-tikva)). The nearest station is the underground Arlozorov station, beside the Savidor Center railway station (both about 850 m east).
- **Purple Line: under construction, street level.** It runs along Arlozorov Street past the square (Hebrew Wikipedia: "ארלוזורוב, בן יהודה, אלנבי, העלייה, לוינסקי"; its Ichilov station is by Kikar Hamedina and the Sourasky Medical Center) ([he.wikipedia](https://he.wikipedia.org/wiki/%D7%93%D7%A0%D7%A7%D7%9C_%E2%80%93_%D7%94%D7%A7%D7%95_%D7%94%D7%A1%D7%92%D7%95%D7%9C)). Planned opening: July 2028 (the same article's infobox); "the opening in 2028" ([Railway Gazette, 18.6.2026](https://www.railwaygazette.com/light-rail/2026/06/18/tel-aviv-purple-line-light-rail-vehicles-deliveries-begin/)); mid-2028, as NTA and the Ministry of Transport set it on 18.2.2025 ([ynet](https://www.ynet.co.il/news/article/rykwppw5yx)). NTA's own page answered 403 to our reader, so we have not read it.
- **Green Line: under construction.** Its underground Arlozorov station is on Ibn Gabirol. The southern section (Rishon LeZion to Levinsky) is planned for the end of 2028, and the whole line during 2030 ([Calcalist, 18.2.2025](https://www.calcalist.co.il/local_news/article/h1bjfwg5kg)). So the Ibn Gabirol stations are not in the 2028 section.
- **Metro (planned):** line M1's planned route (TLV GIS layer 954) passes about 540 m east of the plot. Its stations and dates are not in the layer: not found.

**Buses.** The lines are those that stopped at each stop on Tuesday 8.9.2026, a normal weekday, from the Ministry of Transport's GTFS as archived by Open Bus Stride ([Hasadna API](https://open-bus-stride-api.hasadna.org.il/docs)). Stops are from TLV open data, OSM and GTFS.

| Stop | Walk (min) | Distance (m) | Lines (8.9.2026) | Rides that day |
|---|---|---|---|---|
| כיכר המדינה/וייצמן | 1 | 141 | 3, 7, 14, 66, 89, 90 | 477 |
| כיכר המדינה/אריה עקיבא | 1 | 141 | 5, 7, 14, 66, 89 | 516 |
| כיכר המדינה/ויצמן | 1 | 160 | 7, 14, 66, 89 | 358 |
| ז'בוטינסקי/דרך נמיר | 1 | 188 | 3, 90 | 121 |
| כיכר המדינה/ויצמן | 1 | 214 | 7, 14, 89 | 256 |
| ז'בוטינסקי/כיכר המדינה | 1 | 234 | 3, 5, 90 | 245 |
| ארלוזורוב/משה שרת | 4 | 348 | 61, 66, 90, 161 | 411 |
| גימנסיה הרצליה/רמז | 3 | 350 | 3 | 61 |
| גימנסיה הרצליה/ז'בוטינסקי | 3 | 377 | none in GTFS that day | - |
| ארלוזורוב/ויצמן | 4 | 380 | 28, 55, 59, 61, 161, 379 | 405 |
| ויצמן/בארי | 3 | 402 | 7, 14, 28, 55, 59, 89, 379 | 412 |
| בית החייל/ויצמן | 3 | 434 | 7, 14, 66, 89 | 358 |
| ארלוזורוב/בלוך | 5 | 440 | 61, 161 | 230 |
| גימנסיה הרצליה/ז'בוטינסקי | 4 | 466 | 3, 61, 66, 90 | 387 |
| ארלוזורוב/דרך נמיר | 6 | 514 | 28, 55, 59, 61, 161, 379 | 407 |
| דרך נמיר/ז'בוטינסקי | 5 | 520 | 5, 40, 44, 47, 71, 72, 91, 116, 148, 149, 159, 171, 193, 248, 249, 270, 271, 272, 274, 282, 299, 347, 349, 450, 464, 474, 501, 506, 532, 600, 601, 602, 603, 605, 606, 607, 611, 623, 632, 633, 650 | 1594 |
| ת. רכבת תל אביב - סבידור/דרך נמיר | 8 | 614 | 40, 44, 47, 58, 71, 72, 91, 101, 103, 104, 105, 107, 111, 116, 148, 149, 159, 171, 190, 193, 194, 200, 222, 248, 249, 253, 270, 271, 272, 274, 276, 282, 283, 299, 302, 304, 345, 347, 349, 375, 378, 450, 454, 458, 460, 462, 464, 474, 480, 500, 501, 506, 532, 575, 600, 601, 605, 606, 611, 615, 623, 632, 633, 635, 650, 704, 825, 826, 833, 836, 840, 843, 845, 846, 852, 910 | 2293 |
| תיכון חדש רבין/דרך נמיר | 8 | 653 | 3, 5, 11, 40, 44, 47, 71, 72, 90, 91, 107, 116, 124, 148, 149, 159, 171, 193, 248, 249, 253, 270, 271, 272, 274, 282, 283, 347, 349, 450, 464, 474, 501, 506, 532, 575, 600, 601, 603, 605, 606, 607, 611, 623, 635, 650, 833 | 1860 |
| ביה''ח איכילוב/ויצמן | 6 | 667 | 7, 14, 28, 55, 59, 89, 379, 811 | 568 |

- 53 different bus lines stop within 5 minutes' walk of the ring, and 95 within 10 minutes. The Namir / Jabotinsky stops and the Savidor terminal on Namir carry most of them.

**Main roads** (nearest point of each street axis, TLV GIS layers 507 and 508; "main" = the city's main-streets layer):

| Road | Distance (m) | Direction | Main street |
|---|---|---|---|
| הא באייר | 135 | NE (24°) | yes |
| ז'בוטינסקי | 136 | E (103°) | no |
| ויצמן | 139 | S (190°) | yes |
| ארלוזורוב | 349 | S (197°) | yes |
| פנקס דוד צבי | 474 | N (359°) | yes |
| נמיר מרדכי | 526 | E (100°) | yes |
| אבן גבירול | 718 | W (278°) | yes |
| יהודה המכבי | 783 | N (359°) | no |
| בגין מנחם | 880 | SE (155°) | yes |
| שאול המלך | 996 | S (166°) | yes |
| בני דן | 1,010 | N (350°) | no |
| רוקח ישראל | 1,361 | N (355°) | yes |
| דיזנגוף | 1,373 | W (281°) | yes |
| Ayalon Highway (Route 20) | 804 | E (106°) | motorway (OSM way/139744094) |

## 5. Parks and outdoors

- **Park HaYarkon** (OSM relation 16022802, officially "גני יהושע"): its nearest edge is about 1 km north, by Bnei Dan Street. The edge point is where the park's outline is nearest, not necessarily a gate: gates are not in our sources (not found).
- **The plot's own park and lake:** see section 1.

### Nearest green places

| Place | What | Walk (min) | Distance (m) | Source |
|---|---|---|---|---|
| גן אברהם | park | 2 | 206 | OSM |
| אברהם ברוך | גן, שרת משה 66 | 2 | 218 | TLV open data + TLV GIS |
| גן בילטמור | גן, בילטמור 12 | 2 | 261 | TLV open data + OSM + TLV GIS |
| פולק | גן, ויצמן 71 | 2 | 263 | TLV open data + OSM + TLV GIS |
| גן הגת | גן, חברה חדשה 4 | 2 | 277 | OSM + TLV GIS |
| כהן משה | גן, ויצמן 56 | 2 | 287 | TLV open data + TLV GIS |
| גן משה כהן | park | 2 | 291 | OSM |
| גן גרמניס | גן, תש"ח 2 | 2 | 301 | OSM + TLV GIS |
| רמז | גינה, רמז דוד 17 | 3 | 378 | OSM + TLV GIS |
| חורשת ליסין | גינת כלבים, ליסין 20 | 4 | 400 | TLV open data + TLV GIS |
| גן גורדון | גן, ארלוזורוב 170 | 4 | 412 | OSM + TLV GIS |
| פורר אליענה | גינה, הציונות 21 | 4 | 423 | TLV GIS (layer 696) |
| בילטמור | park, בילטמור 12 | 5 | 280 | TLV open data (findplace) |
| כורכר מחשוף רמז | park | 5 | 389 | TLV open data (findplace) |
| אהבת ציון | park | 5 | 460 | TLV open data (findplace) |

### Sport

| Place | What | Walk (min) | Distance (m) | Source |
|---|---|---|---|---|
| Training Room | gym, הא באייר 46 | 1 | 152 | OSM |
| ביה"ס יסודי תורה ב | מגרש כדורסל וקט רגל, חדרה 2 | 3 | 289 | TLV open data + TLV GIS |
| ביה"ס אהבת ציון | אולם ספורט, כהנשטיין 16 | 4 | 383 | TLV open data + TLV GIS |
| ביה"ס גמנסיה הרצליה | sport, ג'בוטינסקי 106 | 5 | 443 | TLV open data + OSM |
| ארלוזורוב 97 - הקאנטרי הקהילתי במרכז | אולם ספורט, ארלוזורוב 97 | 5 | 444 | OSM + TLV GIS |
| קאנטרי ארלוזורוב | מכון כושר, ארלוזורוב 97 | 5 | 449 | TLV GIS (layer 937) |
| חדר כושר הגימנסיה הרצליה | gym, ז'בוטינסקי 106 | 5 | 469 | OSM |
| מרכז ספורט חדש | אולם ספורט, דרך נמיר 81 | 6 | 532 | TLV open data + TLV GIS |
| ביה"ס עירוני ד' | מכון כושר, וייצמן | 6 | 687 | TLV open data + TLV GIS |
| ביה"ס עירוני ד' | sport, ויצמן 74 | 6 | 706 | TLV open data (findplace) |
| ביה"ס גמנסיה הרצליה | אולם ספורט, ז'בוטינסקי 106 | 7 | 381 | TLV open data + TLV GIS |
| פאלאס | מכון כושר, וויצמן 14 | 7 | 597 | TLV GIS (layer 937) |

## 6. Schools, kindergartens, daycare

The city's 2026-27 layers (769 schools, 768 kindergartens) and recognised daycares (624), with TLV open data and OSM. Registration zones are set by the city each year and are not asserted here.

### Schools

| Place | What | Walk (min) | Distance (m) | Source |
|---|---|---|---|---|
| כיכר המדינה | יסודי, ממלכתי, הא באייר 75 | 1 | 102 | TLV open data + TLV GIS |
| מאיר שלו - חט"ב | school, הא באייר 75 | 1 | 102 | TLV open data (findplace) |
| מכללת מישלב | college | 1 | 209 | OSM |
| יסודי התורה ב | יסודי, חרדי, חדרה 2 | 3 | 292 | TLV open data + TLV GIS |
| אהבת ציון | יסודי, ממלכתי, כהנשטם 16 | 3 | 370 | TLV open data + TLV GIS |
| גמנסיה הרצליה-חט"ב | על יסודי, ממלכתי, ז'בוטינסקי 106 | 4 | 406 | TLV open data + TLV GIS |
| גמנסיה הרצליה | school, ז'בוטינסקי 106 | 4 | 406 | TLV open data (findplace) |
| יואל גבע | school, ז'בוטינסקי 106 | 4 | 406 | TLV open data (findplace) |
| בית יעקוב | school, אהבת ציון 22 | 4 | 415 | TLV open data (findplace) |
| מוזיר | school, מוזר יעקב | 5 | 483 | TLV open data + OSM |
| ארנון | יסודי, ממלכתי, ילין דוד 11 | 5 | 509 | TLV open data + TLV GIS |
| הגימנסיה העברית הרצליה | school, ז'בוטינסקי 106 | 6 | 431 | OSM |
| בית הילד | יסודי, חרדי, אהבת ציון 22 | 6 | 441 | TLV open data + TLV GIS |
| יש. הרב עמיאל (הישוב החדש) | על יסודי, ממ"ד, פומבדיתא 13 | 6 | 543 | TLV GIS (layer 769) |

### Kindergartens and daycare

| Place | What | Walk (min) | Distance (m) | Source |
|---|---|---|---|---|
| ענן | גנים, ממלכתי, חברה חדשה 11 | 1 | 186 | TLV open data + OSM + TLV GIS |
| נשיאים | kindergarten, חברה חדשה 11 | 1 | 186 | TLV open data (findplace) |
| קרינה ורחל | מעון פרטי בנכס עירוני, משה שרת 11 | 1 | 229 | TLV open data + TLV GIS |
| גן חדרה 1 | גנים, חרדי, חדרה 2 | 3 | 292 | TLV open data + OSM + TLV GIS |
| גן חדרה 2 | kindergarten, חדרה 2 | 3 | 292 | TLV open data (findplace) |
| טבת | גנים, מיוחד, גלוסקין 3 | 4 | 345 | TLV open data + TLV GIS |
| לבנדר | kindergarten, גלוסקין 3 | 4 | 345 | TLV open data (findplace) |
| קינמון | גנים, ממלכתי, ליסין 22 | 4 | 437 | TLV open data + TLV GIS |
| לימונית | kindergarten, ליסין 22 | 4 | 437 | TLV open data (findplace) |
| קורנית | kindergarten, ליסין 22 | 4 | 437 | TLV open data (findplace) |
| ריחן | kindergarten, ליסין 22 | 4 | 437 | TLV open data (findplace) |
| נענע | kindergarten, ליסין 22 | 4 | 437 | TLV open data (findplace) |
| רוזמרין | kindergarten, ליסין 22 | 4 | 437 | TLV open data (findplace) |
| גן אהבת ציון 2 | גנים, חרדי, אהבת ציון 22 | 6 | 441 | TLV open data + TLV GIS |

## 7. Health

### Hospitals, clinics, pharmacies

Ichilov (Tel Aviv Sourasky Medical Center) is at ויצמן 6, about 0.7-0.85 km south: the city's medical layer (565) places its general, children's (Dana) and maternity (Lis) hospitals there, and OSM has the campus as "בי"ח איכילוב".

| Place | What | Walk (min) | Distance (m) | Source |
|---|---|---|---|---|
| סופר פארם ויצמן ת"א | בית מרקחת, ויצמן 53 | 1 | 215 | TLV GIS (layer 564) |
| גוד פארם | pharmacy | 2 | 326 | OSM |
| ברק | בית מרקחת, ז'בוטינסקי 109 | 3 | 372 | TLV open data + TLV GIS |
| כללית | כללית, בארי 27 | 4 | 424 | OSM + TLV GIS |
| בארי | בית מרקחת, בארי 27 | 4 | 433 | TLV GIS (layer 564) |
| שחר ברנדס | בית מרקחת, פנקס 27 | 6 | 583 | TLV open data + TLV GIS |
| מרפאות טופ איכיפוב | hospital | 7 | 592 | OSM |
| סופר פארם איכילוב | בית מרקחת, ויצמן 14 | 7 | 602 | TLV GIS (layer 564) |
| ניופרם בי"ח איכילוב | בית מרקחת, ויצמן 6 | 8 | 682 | TLV GIS (layer 564) |
| מגדל המאה | כללית, אבן גבירול 124 | 8 | 704 | TLV open data + TLV GIS |
| סופר פארם אבן גבירול | בית מרקחת, אבן גבירול 124 | 8 | 706 | TLV open data + OSM + TLV GIS |
| מרפאת עין טל ספטולב | מרפאה כירורגית, ברנדיס | 8 | 752 | TLV open data + TLV GIS |
| רבינוביץ | כללית, אריסטובול 2 | 8 | 765 | TLV open data + TLV GIS |
| כללית | clinic | 8 | 769 | OSM |
| יהודה המכבי | בית מרקחת, יהודה המכבי 42 | 8 | 795 | TLV open data + TLV GIS |
| פריים פארם יהודה המכבי | pharmacy, יהודה המכבי | 8 | 795 | TLV open data (findplace) |

## 8. Culture, community, food and shopping

### Culture and community

| Place | What | Walk (min) | Distance (m) | Source |
|---|---|---|---|---|
| מרכז קהילתי כיכר המדינה | מרכז קהילתי | 1 | 91 | TLV open data + TLV GIS |
| חנקין-גן פולק | community centre, חנקין-גן פולק 3 | 3 | 256 | TLV open data (findplace) |
| תיאטרון תל אביב | culture | 3 | 432 | OSM |
| אשכול גנים לסין (ככר התבלינים) | community centre, אשכול גנים לסין (ככר התבלינים) | 4 | 434 | TLV open data (findplace) |
| ארלוזורוב 97 | קאנטרי קהילתי, קאנטרי קהילתי, ארלוזורוב 97 | 5 | 453 | TLV GIS (layer 553) |
| אהבת ציון | community centre, אהבת ציון 7 | 5 | 473 | TLV open data (findplace) |
| תיאטרון בית החייל תל אביב | סטנדאפ, ויצמן 60 | 6 | 425 | TLV open data + TLV GIS |
| שבט דיזנגוף - תנועת הצופים העבריים בישראל | community centre, דוד רמז 7 | 6 | 435 | OSM |
| גימנסיה הרצליה | community centre, גימנסיה הרצליה | 6 | 437 | TLV open data (findplace) |
| מרכז ספורט חדש | מרכז ספורט, מרכז ספורט, דרך נמיר מרדכי 81 | 7 | 615 | TLV open data + TLV GIS |
| הקונסרבטוריון הישראלי למוסיקה | מוזיקה קלאסית, לואי מרשל 25 | 7 | 708 | TLV open data + TLV GIS |
| בית יד לבנים | מרכז קהילתי, מרכז קהילתי, פנקס דוד צבי 63 | 8 | 627 | TLV open data + TLV GIS |
| רייך לאזרחים ותיקים | מרכז קהילתי לאזרחים ותיקים, מרכז קהילתי, ארלוזורוב 106 | 9 | 719 | TLV GIS (layer 553) |
| אריסטובולוס | community centre, אריסטובולוס | 9 | 818 | TLV open data (findplace) |

### Synagogues (the city's layer 568)

| Place | What | Walk (min) | Distance (m) | Source |
|---|---|---|---|---|
| עבודת ישראל - קוז'ניץ | נוסח אשכנז, ויצמן 71 | 1 | 236 | TLV GIS (layer 568) |
| יסודי התורה | נוסח אשכנז, חדרה 2 | 3 | 293 | TLV GIS (layer 568) |
| משכן הכהנים | נוסח עדות המזרח, שד' הציונות 20 | 4 | 410 | TLV GIS (layer 568) |
| מגורים | נוסח אשכנז, קליי 7 | 6 | 501 | TLV GIS (layer 568) |
| סדיגורא | נוסח אשכנז, פנקס 41 | 6 | 502 | TLV GIS (layer 568) |
| ישיבת עמיאל - היישוב | נוסח אשכנז, פומבדיתא 13 | 6 | 543 | TLV GIS (layer 568) |
| בית הכנסת היכל יהודה | נוסח עדות המזרח, בן סרוק 13 | 7 | 602 | OSM + TLV GIS |
| בי"ח איכילוב בנין סוראסקי | נוסח כללי, ויצמן 6' | 7 | 681 | TLV GIS (layer 568) |

### Cafés and restaurants

| Place | What | Walk (min) | Distance (m) | Source |
|---|---|---|---|---|
| Open | restaurant, הא באייר | 1 | 149 | TLV open data (findplace) |
| נוצ'י סושי אנד,מחסן 15175 | restaurant, הא באייר | 1 | 150 | TLV open data (findplace) |
| נספרסו ישראל | café, הא באייר | 1 | 152 | TLV open data (findplace) |
| בייקרי כיכר המדינה | café, ויצמן | 1 | 158 | TLV open data (findplace) |
| לחם ארז | café | 1 | 158 | OSM |
| Nuchi | restaurant | 1 | 161 | OSM |
| נוצי סושי אנד בר | restaurant, תש"ח | 1 | 162 | TLV open data (findplace) |
| לחם ארז | restaurant, הא באייר | 2 | 152 | TLV open data + OSM |
| אסתריקה פיצה | restaurant, ז'בוטינסקי | 2 | 297 | TLV open data + OSM |
| אוסישקין גלידות תל אביב ב | restaurant, ז'בוטינסקי | 2 | 297 | TLV open data (findplace) |
| מיצלי | café | 2 | 312 | OSM |
| דלל | café, ז'בוטינסקי 110 | 2 | 329 | OSM |
| בייקפה | restaurant, רמז דוד | 3 | 329 | TLV open data (findplace) |
| בית לחם | café | 3 | 374 | OSM |

### Supermarkets

| Place | What | Walk (min) | Distance (m) | Source |
|---|---|---|---|---|
| ZEST | supermarket, הא באייר | 1 | 149 | TLV open data (findplace) |
| מוקאיה שוקולד | supermarket, הא באייר | 1 | 150 | TLV open data (findplace) |
| מנימרקט כיכר המדינה | supermarket, הא באייר | 1 | 150 | TLV open data (findplace) |
| City Market | supermarket | 1 | 152 | OSM |
| ויקטורי | supermarket | 1 | 211 | OSM |
| הקערה | supermarket, הא באייר | 2 | 154 | TLV open data (findplace) |
| ניו מרקט | supermarket | 2 | 315 | OSM |
| פ.א.ר פירות וירקות | supermarket, ז'בוטינסקי | 2 | 324 | TLV open data (findplace) |
| דלאל | supermarket, רמז דוד | 3 | 329 | TLV open data (findplace) |
| החנווני | supermarket, שרת משה | 5 | 434 | TLV open data (findplace) |
| מגה בעיר | supermarket, פנקס דוד צבי | 5 | 450 | TLV open data + OSM |
| פרי השחר | supermarket, מוזר יעקב | 5 | 482 | TLV open data (findplace) |

## 9. The place registry (`places.json`)

- **1245 places** within 1.5 km: education 158, outdoors 256, transport 39, food 314, essentials 353, health 43, community 82.
- All 1245 have a walking time: 182 within 5 minutes, 463 within 10, 843 within 15.
- Sources: OSM 483, TLV open data (findplace) 386, TLV GIS 142, TLV open data + TLV GIS 105, TLV open data + OSM 57, OSM + TLV GIS 36, TLV open data + OSM + TLV GIS 31, GTFS 5.
- How it was built:
  1. `build_places.py kikar`: findplace.co.il's frozen file (TLV open data + OSM, 27.8.2026), then OSM via Overpass, the nearest 14 bus stops, walking minutes, and the 5/10/15-minute areas.
  2. `enrich_places_kikar.py`:
     - the city's own layers for daily life (findplace's file stops at lat 32.0845, about 250 m south of the plot);
     - bus lines per stop, and the busiest stops the 14-stop cut left out (the Namir hub);
     - the light-rail stations with their line and status;
     - Park HaYarkon's nearest edge.
- **Walking start (provisional).** The plot is a closed building site inside the ring road, and Mapbox snaps its centre 122 m south onto the ring (checked 30.9.2026), which would add about 2 minutes to every walk north.
  - So each walk starts on the ring road, on the side facing the place.
  - The walking areas are the union of four Mapbox walking areas from the ring's N/E/S/W points.
  - From a tower's lobby to the ring add about one minute (the towers stand 75-78 m from the centre, the ring 128-147 m).
  - P5/P7 re-measure from the lobbies once their doors are known. The permit addresses are ה' באייר 25, 45 and 65 (TLV GIS 499).
- **Sight lines (provisional).** Each place's `sight` (street / roof / hidden on floors 10, 25 and 37) uses the plot centre as the view point, the formula eyes of `eye-kikar-provisional.json` (37.6 / 97.6 / 145.6 m), and the city's buildings within 700 m, with the three towers left out. P5 replaces it per tower with the stage's own eyes.
- Personal data: the city's school and kindergarten layers carry staff names and phones. None was copied; only the institution's name, kind and address.

## 10. The blocks around (`city-blocks.json`)

- **1102 buildings** within 700 m of the plot centre (TLV GIS layer 513, read 30.9.2026), each with its footprint (lat/lng and local metres), floors, year, height and the height's source.
  - Heights: DSM mean 23, survey 2019 1075, ESTIMATED: floors x 3.2 m 4.
  - Estimated heights (floors × 3.2 m) are labelled `ESTIMATED` in `h_src`.
  - Left out: antennas, bus shelters and temporary structures (95), and footprints under 10 m² (31).
- Also for the P5 world: 349 street axes (507/508) and 108 green areas (503), in the same frame; 334 named streets with their nearest distance (`roads_near`).
- The frame: x = metres east of the plot centre, z = metres south, no grid turn. It is the frame of `build_places.py`, so the sight lines read it directly.

**Notable towers within 2 km** (70 m and higher: 95 in the layer; the tallest with a name from the layer or OSM):

| Height | Floors | Name (source) | Address (OSM) | Distance (m) | Direction |
|---|---|---|---|---|---|
| 242.5 m (survey 2019) | 6 | no name in the sources | מנחם בגין 121 | 1,632 | S (183°) |
| 235.0 m (DSM mean) | 70 | no name in the sources | מנחם בגין 121 | 1,627 | S (183°) |
| 214.3 m (survey 2019) | 1 | no name in the sources | מנחם בגין 121 | 1,673 | S (183°) |
| 213.3 m (survey 2019) | 1 | עזריאלי שרונה (OSM) | מנחם בגין 121 | 1,671 | S (183°) |
| 197.3 m (survey 2019) | not found | no name in the sources | מנחם בגין 144ב | 1,102 | S (162°) |
| 187.3 m (survey 2019) | 1 | מתחם עזריאלי קומות מסחר (TLV GIS) | גשר "הקריה" | 1,375 | S (172°) |
| 185.8 m (survey 2019) | 3 | no name in the sources | טיילת איילון 156 | 986 | SE (144°) |
| 185.7 m (survey 2019) | 4 | מידטאון TLV מגורים (OSM) | מנחם בגין 144ד | 1,054 | S (160°) |
| 184.6 m (survey 2019) | 49 | מגדלי עזריאלי (TLV GIS) | גשר "הקריה" | 1,377 | S (173°) |
| 180.0 m (DSM mean) | 53 | no name in the sources | ארלוזורוב 83;89 | 659 | W (257°) |
| 180.0 m (DSM mean) | 53 | no name in the sources | not found | 639 | W (262°) |
| 171.0 m (survey 2019) | 50 | מגדל אלקטרה (OSM) | יגאל אלון 98 | 1,909 | S (168°) |
| 165.0 m (DSM mean) | 40 | no name in the sources | השלום 12 | 1,825 | S (160°) |
| 160.5 m (survey 2019) | 29 | מגדל קריית הממשלה (TLV GIS) | מנהרת אריה לובה אליאב 125 | 1,539 | S (181°) |
| 158.8 m (survey 2019) | 1 | no name in the sources | ניסים אלוני 6 | 712 | E (80°) |
| 157.4 m (survey 2019) | 1 | no name in the sources | טיילת איילון | 976 | SE (140°) |
| 154.7 m (survey 2019) | 42 | מגדלי עזריאלי (TLV GIS) | איילון דרום 136 | 1,382 | S (170°) |
| 154.4 m (survey 2019) | 44 | no name in the sources | אהרן מגד 6 | 1,098 | NE (53°) |
| 149.5 m (survey 2019) | 46 | מגדלי עזריאלי (TLV GIS) | גבעת התחמושת 132 | 1,451 | S (173°) |
| 145.0 m (survey 2019) | 40 | no name in the sources | דרך נמיר 19 | 720 | NE (55°) |

- Some records in the layer are parts of one building: a podium or a crown with its own height and "1" floor. The Azrieli Sarona site has four records between 213 and 242.5 m. Read these heights as the layer's, not as the tower's official height.
- The two 53-floor, 180 m (DSM) buildings at Arlozorov 83/89, 640-660 m west, are probably H Infinity (our page's lot 124 lies about 670 m west). The city's layer does not name them: unverified.

## 11. What the high floors may see (`sight-landmarks.json`)

Preparation only. Coordinates, distance and direction from the plot centre; **visibility is not computed** (P5 brings the towers' model and eye heights).

| Direction | Landmark | Distance (m) | Height (source) | Coordinates (source) |
|---|---|---|---|---|
| N (12°) | רמת אביב | 2,511 | not found | 32.10886, 34.79510 (OpenStreetMap (Nominatim), way/819845420 (רמת-אביב)) |
| NE (27°) | אוניברסיטת תל אביב | 3,192 | not found | 32.11236, 34.80501 (OpenStreetMap (Nominatim), relation/17483735 (אוניברסיטת תל אביב)) |
| NE (54°) | פארק הירקון (גני יהושע), מרכז | 3,122 | not found | 32.10303, 34.81673 (OpenStreetMap relation 16022802 (Nominatim)) |
| E (106°) | מגדל משה אביב (רמת גן) | 1,368 | not found | 32.08343, 34.80374 (OpenStreetMap (Nominatim), way/503512749 (מגדל משה אביב)) |
| E (106°) | נתיבי איילון (כביש 20), הנקודה הקרובה | 804 | not found | 32.08478, 34.79798 (OpenStreetMap way 139744094 (Overpass)) |
| E (109°) | תחנת רכבת תל אביב סבידור מרכז | 852 | not found | 32.08424, 34.79831 (OpenStreetMap (Nominatim), node/2930618402 (תל אביב סבידור מרכז)) |
| S (170°) | מגדלי עזריאלי (42 קומות) | 1,382 | 154.7 m (survey 2019 (gova_simplex_2019)) | 32.07454, 34.79236 (עיריית תל אביב-יפו, שכבת המבנים 513, oid 13824) |
| S (171°) | מרכז עזריאלי (שלושת המגדלים) | 1,358 | not found | 32.07470, 34.79197 (OpenStreetMap (Nominatim), way/32635200 (מרכז עזריאלי)) |
| S (173°) | מגדלי עזריאלי (46 קומות) | 1,451 | 149.5 m (survey 2019 (gova_simplex_2019)) | 32.07383, 34.79176 (עיריית תל אביב-יפו, שכבת המבנים 513, oid 13381) |
| S (173°) | מגדלי עזריאלי (49 קומות) | 1,377 | 184.6 m (survey 2019 (gova_simplex_2019)) | 32.07448, 34.79160 (עיריית תל אביב-יפו, שכבת המבנים 513, oid 13383) |
| S (177°) | בית החולים איכילוב (המרכז הרפואי תל אביב) | 711 | 72.9 m (עיריית תל אביב-יפו, שכבת המבנים 513, oid 37352, 6 קומות (survey 2019 (gova_simplex_2019))) | 32.08038, 34.79015 (OpenStreetMap (Nominatim), way/26599740 (בי"ח איכילוב)) |
| S (183°) | מגדל עזריאלי שרונה | 1,646 | 242.5 m (עיריית תל אביב-יפו, שכבת המבנים 513, oid 39126, 6 קומות (survey 2019 (gova_simplex_2019))) | 32.07199, 34.78889 (OpenStreetMap (Nominatim), way/509799257 (עזריאלי שרונה)) |
| S (188°) | מגדל מרגנית (הקריה) | 1,328 | not found | 32.07496, 34.78773 (OpenStreetMap (Nominatim), way/149520805 (מגדל מרגנית)) |
| SW (213°) | תיאטרון הבימה | 1,856 | not found | 32.07280, 34.77902 (OpenStreetMap (Nominatim), way/149522836 (הבימה)) |
| SW (238°) | בניין עיריית תל אביב-יפו (כיכר רבין) | 1,027 | not found | 32.08182, 34.78058 (OpenStreetMap (Nominatim), way/31786632 (עיריית תל אביב-יפו)) |
| NW (293°) | הים התיכון (חוף מציצים, קו המים) | 2,042 | not found | 32.09388, 34.76982 (עיריית תל אביב-יפו, שכבת החופים 579 (הקודקוד המערבי של פוליגון החוף)) |
| NW (314°) | נמל תל אביב | 1,887 | not found | 32.09865, 34.77552 (OpenStreetMap (Nominatim), way/803404214 (נמל תל-אביב)) |
| NW (327°) | מגדלור רידינג | 2,219 | not found | 32.10354, 34.77707 (OpenStreetMap (Nominatim), way/560065218 (מגדלור רידינג)) |
| NW (334°) | תחנת הכוח רידינג | 2,278 | not found | 32.10509, 34.77902 (OpenStreetMap (Nominatim), way/97714590 (תחנת רידינג)) |
| N (355°) | ספורטק | 1,278 | not found | 32.09819, 34.78861 (OpenStreetMap (Nominatim), way/34333834 (ספורטק צפון)) |

- The sea: the city's beach layer puts the coast between bearings 225° and 348° within 4.5 km. The nearest waterline point is at Metzitzim beach, about 2 km to the north-west.
- Heights of the Azrieli towers, Sarona and Ichilov are the city's layer's values for the building at OSM's point, not official figures.
- Marganit, City Hall and Habima have no building of the layer within 45 m of OSM's point: height not found. Moshe Aviv (Ramat Gan) is outside the city's layer.

## 12. Not found, open, and for later phases

- The lake's outline and place on the plot, and which size is final (P5 needs the landscape plan, design plan 2500א).
- Park HaYarkon's gates (only the nearest edge point is known).
- Where the towers' lobby doors are. The walking start is the ring road for now.
- Final floors and height of tower B (GIS 40 floors and 158.2 m against 37 floors and 157 m in Wikipedia and Ashtrom; the city's permit record mentions 2 added floors for building B).
- The official heights of the landmark towers (only the city's layer values are given).
- The metro M1 stations and dates.
- NTA's own Purple and Green Line pages (403 to our reader). The dates come from Wikipedia, Railway Gazette, ynet and Calcalist, quoting NTA and the Ministry of Transport.
- Registration zones for schools (the city publishes them yearly; not asserted).
- Visibility of every landmark and place per tower and floor (P5).

## 13. Sources (all read 30.9.2026 unless dated)

- Tel Aviv-Yafo municipality GIS, ArcGIS REST IView2 (https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer):
  - 513 buildings, 837 lots, 528 plans, 499 building sites;
  - 507/508 streets, 503 green areas, 511 neighbourhoods;
  - 423/764/766 light-rail stations, 954 metro lines, 956 bus stops, 579 beaches;
  - 769/768 schools and kindergartens 2026-27, 624 daycares;
  - 563/565/564/561/560 health, 553 community, 745 culture;
  - 937/938/939/943/936 sport, 696 playgrounds, 586 dog parks, 551 gardens, 568 synagogues.
- Tel Aviv-Yafo local planning committee, decision 21-0018ב-3 (4.8.2021), design plan 2500ב/1, public buildings at Kikar Hamedina (PDF, tel-aviv.gov.il).
- findplace.co.il frozen discovery file north-tlv-discovery-v2 (TLV open data + OSM, 27.8.2026, sha256 2909a0c2…).
- OpenStreetMap (ODbL, © OpenStreetMap contributors), via Overpass and Nominatim.
- Mapbox Directions and Isochrone APIs, walking profile, with the site's public token read from a live project page (not stored).
- Open Bus Stride (the Public Knowledge Workshop), GTFS of the Ministry of Transport, 8.9.2026.
- Globes 2.5.2022; Calcalist 28.11.2021 and 18.2.2025; ynet 18.2.2025; Railway Gazette 18.6.2026; Bloomberg 18.8.2023; Wikipedia (en: Kikar Hamedina, Red Line; he: the Purple Line); Ashtrom (en).
