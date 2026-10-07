# Rova 4 area map: design prototype (7.10.2026)

Not live. Nothing here was deployed, committed or sent to the site. Target: a band under the price list on
https://nad-lan.co.il/north-tel-aviv/rova-4/ (between "מחירים מבוקשים סביב הכיכר" / the price calculator and
"כיכר המדינה והמגדלים"), later on project pages.

Open `preview.html` straight from disk (Chrome). It needs the network only for the map tiles, the MapLibre script and
Google Fonts; every pin, card and line comes from the copy of `data.json` embedded in the page.

## What is in the folder

| file | what it is |
|---|---|
| `preview.html` | the band: kicker, H2, lead, six filters, the map (70vh desktop, 60svh phone), card, reset button, caption, a closed list of every project and address under the map |
| `data.json` | all data with source and retrieval time per item, plus `not_placed` (what was left out and why) |
| `geocode.py` | Nominatim geocoding of the renewal addresses, 1 request per second, cached in `raw/nominatim.json` |
| `fetch_osm.py` | one Overpass query for the Rova 4 box (daily life + the four boundary lines), saved to `raw/overpass.json` |
| `build_data.py` | builds `data.json` (and reads our own project pages once into `raw/projects.json`), then embeds a slim copy into `preview.html` |
| `shoot.py` | headless Chrome check (Playwright, `channel="chrome"`), screenshots into `shots/`, report in `shots/report.json` |
| `raw/` | the untouched answers from Nominatim, Overpass and our catalogue, as evidence |
| `shots/` | desktop 1366x900 and phone 390x844 screenshots, home view, renewal card, project card, top-down view, one-finger test |

Stack: MapLibre GL JS **5.24.0** pinned from cdnjs (published 23.4.2026; 6.x is ESM-only with a separate worker, so the
last 5.x UMD build was chosen), basemap OpenFreeMap **positron** recoloured to the Skin A tokens (paper, sand, sea,
deep, ink), 3D buildings as a `fill-extrusion` from the tiles' `render_height` / `render_min_height` (from zoom 13),
`@mapbox/mapbox-gl-rtl-text@0.3.0` for Hebrew labels. Camera: centre Kikar HaMedina (32.086758, 34.789776),
desktop zoom 15, pitch 55, bearing -18 (north up, slightly turned so the sea sits top left); phone zoom 14.2,
centre 32.0868, 34.7900.

## Counts per filter (7.10.2026)

| filter (visible name) | count | source |
|---|---|---|
| פרויקטים | 6 | our project pages |
| התחדשות עירונית | 15 placed (13 press rows + 2 of our renewal-compound pages), 1 not placed | facts.md R41 to R51, press-facts.md U1 to U12 and D1, our pages |
| בתי ספר וגנים | 11 (8 schools, 3 kindergartens) | OpenStreetMap |
| פארקים | 19 | OpenStreetMap (`leisure=park`) |
| קניות | 43 (21 cafés, 16 supermarkets, 6 pharmacies) | OpenStreetMap |
| תחבורה | 4 (light rail ארלוזורוב and שאול המלך, train station תל אביב סבידור מרכז, מסוף 2000) | OpenStreetMap |

Places dropped by `build_data.py`: 109 without a name (mostly small unnamed parks and kindergartens), 157 outside the
quarter line, 11 rail stop positions (the station node is kept). Transport within 250 m of the line is kept and its
card says "על גבול הרובע" (שאול המלך station, 114 m south of the line).

## Projects (position from our own pages, read 7.10.2026 08:34 to 08:35 UTC)

Candidates came from `https://nad-lan.co.il/wp-json/nadlan/v1/project-map` (962 projects) and were kept only when
inside the quarter line. Each card line is in the page's own words (meta description or facts box).

| pin | page | lat, lng | position from | card line |
|---|---|---|---|---|
| מגדלי כיכר המדינה | /projects/hamedina/ | 32.086758, 34.789776 | JSON-LD geo | 3 מגדלים בני 40, 40 ו-37 קומות · 453 דירות |
| DUO | /projects/duo-tel-aviv/ | 32.085658, 34.783027 | stage lat/lng in the page HTML (JSON-LD says 32.085698, 34.782856, about 17 m away) | 2 מגדלים בני 54 קומות · 668 דירות · אפריקה ישראל מגורים |
| H Infinity | /projects/h-infinity-somail-tel-aviv/ | 32.087284, 34.78272 | JSON-LD geo | מגדל מגורים ובניין בוטיק · כ-278 דירות · קבוצת חג'ג' |
| מגדלי YOO | /projects/yoo-tel-aviv/ | 32.090497, 34.7963 | JSON-LD geo | 2 מגדלים בני 37 ו-41 קומות · כ-300 דירות · קבוצת חבס |
| מגדלי אקירוב | /projects/akirov-towers/ | 32.090711, 34.793055 | JSON-LD geo | 3 מגדלים בני 32 קומות · כ-350 דירות · אלרוב |
| פארק בבלי | /projects/park-bavli/ | 32.092292, 34.798255 | JSON-LD geo | 4 מגדלים בני 46 קומות · כ-800 דירות · קבוצת תשובה ואלעד מגורים |

Left out on purpose: Rainbow, the Sde Dov projects, ToHa2, Einstein (outside the line); ten catalogue pages
(בבלי 299 units, הדר יוסף, כפר שלם, עמק ברכה and others) that all carry the same city-centre fallback point
32.0853, 34.781806, which is not a real position.

## Urban renewal: every geocoding result (OSM Nominatim, 7.10.2026 08:28 to 08:29 UTC)

Card fields (before, after, developer, stage) follow facts.md and the table on the live Rova 4 page. An unknown field is
omitted from the card, never printed as "לא פורסם".

| address | query sent | lat, lng | OSM object | OSM display name |
|---|---|---|---|---|
| זלוציסטי 4 | זלוציסטי 4, תל אביב-יפו | 32.083462, 34.793160 | node/2079071542 | 4, זלוציסטי, תל־אביב–יפו, הצפון החדש, הצפון החדש - סביבת ככר המדינה, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 6492903, ישראל |
| רמז 27 | דוד רמז 27, תל אביב-יפו | 32.089241, 34.786249 | node/2079027632 | 27, דוד רמז, תל־אביב–יפו, הצפון החדש, הצפון החדש - סביבת ככר המדינה, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 6296802, ישראל |
| ז'בוטינסקי 152 | ז'בוטינסקי 152, תל אביב-יפו | 32.085748, 34.793979 | node/2078993963 | 152, ז'בוטינסקי, תל־אביב–יפו, הצפון החדש, הצפון החדש - סביבת ככר המדינה, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 5268101, ישראל |
| בארי 36 (pin = midpoint of 36 and 56) | בארי 36, תל אביב-יפו | 32.082293, 34.789806 | node/2079041196 | 36, בארי, תל־אביב–יפו, הצפון החדש - החלק הדרומי, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 6492903, ישראל |
| בארי 56 | בארי 56, תל אביב-יפו | 32.082046, 34.791674 | node/2079194783 | 56, בארי, תל־אביב–יפו, הצפון החדש - החלק הדרומי, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 6492903, ישראל |
| ז'בוטינסקי 135 (pin = midpoint of 135 and 137) | ז'בוטינסקי 135, תל אביב-יפו | 32.086709, 34.791985 | node/2078986611 | 135, ז'בוטינסקי, תל־אביב–יפו, הצפון החדש, הצפון החדש - סביבת ככר המדינה, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 5268101, ישראל |
| ז'בוטינסקי 137 | ז'בוטינסקי 137, תל אביב-יפו | 32.086647, 34.792143 | way/149367031 | 137, ז'בוטינסקי, תל־אביב–יפו, הצפון החדש, הצפון החדש - סביבת ככר המדינה, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 5268101, ישראל |
| ז'בוטינסקי 133 | ז'בוטינסקי 133, תל אביב-יפו | 32.086720, 34.791724 | node/2078986280 | 133, ז'בוטינסקי, תל־אביב–יפו, הצפון החדש, הצפון החדש - סביבת ככר המדינה, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 5268101, ישראל |
| רמז 44 | דוד רמז 44, תל אביב-יפו | 32.090195, 34.786758 | node/2079183328 | 44, דוד רמז, תל־אביב–יפו, הצפון החדש, הצפון החדש - סביבת ככר המדינה, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 6296802, ישראל |
| רמז 42 | דוד רמז 42, תל אביב-יפו | 32.089978, 34.786731 | node/2079182457 | 42, דוד רמז, תל־אביב–יפו, הצפון החדש, הצפון החדש - סביבת ככר המדינה, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 6296802, ישראל |
| רמז 25 | דוד רמז 25, תל אביב-יפו | 32.090427, 34.786879 | node/2079022075 | 25, דוד רמז, תל־אביב–יפו, הצפון החדש, הצפון החדש - סביבת ככר המדינה, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 6296802, ישראל |
| ליסין 27 | ליסין 27, תל אביב-יפו | 32.085498, 34.793797 | way/149367201 | 27, ליסין, תל־אביב–יפו, הצפון החדש, הצפון החדש - סביבת ככר המדינה, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 5268101, ישראל |
| שרת 30 | משה שרת 30, תל אביב-יפו | 32.086872, 34.787700 | node/2079036017 | 30, משה שרת, תל־אביב–יפו, הצפון החדש, הצפון החדש - סביבת ככר המדינה, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 6296802, ישראל |
| זכרון יעקב 16 | זכרון יעקב 16, תל אביב-יפו | 32.083900, 34.791056 | node/2078994835 | 16, זכרון יעקב, תל־אביב–יפו, הצפון החדש, הצפון החדש - סביבת ככר המדינה, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 6492903, ישראל |
| חנקין 3 (Noga; number from press-facts D1) | חנקין 3, תל אביב-יפו | 32.089057, 34.789130 | node/2079033932 | 3, חנקין, תל־אביב–יפו, הצפון החדש, הצפון החדש - סביבת ככר המדינה, תל־אביב–יפו, נפת תל אביב, מחוז תל אביב, 6296802, ישראל |

Every result above matched the house number, and every one falls inside the quarter line (all in the official
statistical areas "הצפון החדש - סביבת ככר המדינה" or "הצפון החדש - החלק הדרומי").

Also on the renewal filter, from our own compound pages (position = the page's JSON-LD, origin of the point not stated,
so the card says "המיקום בקירוב"):
- מתחם ארלוזורוב, 32.084522, 34.783965: 57 → 248 units, plan 507-0634923, approved before execution, 2023 (data.gov.il register via the page).
- מתחם דפנה, 32.080866, 34.793167: plan תא/3885, approved in execution, 2015. **No unit line**: the page prints 1,434 units
  with 471 existing and 517 added, which do not add up. Worth a fix on that page.

### Could not place
- **רמז 22** (אנשי העיר, 32 units, committee approval): Nominatim returned the street only (way of דוד רמז), for both
  "דוד רמז 22" and "רמז 22". Left off the map; it stays in data.json under `not_placed`.
- **Kikar HaMedina towers in 3D**: the OSM building data in the tiles does not stand the three towers up yet. Checked
  in the rendered tiles at zoom 16.5: within about 200 m of the plaza centre nothing is taller than 41 m; the one 100 m
  building found (241 m south) is מגדל בית לסין (OSM way 965602855, `height=100`). So the plot is marked by the pin and
  a soft ring on the ground. Nothing was drawn by hand. Tile buildings do carry feature ids, so once OSM maps the towers
  they can be tinted sea blue by id.

## The quarter line

OSM has no boundary relation for Rova 4 in the box. The dashed line is built from the OSM geometry of the four lines
named in facts.md R1: אבן גבירול (west), נתיבי איילון (east, motorway ref 20), נחל ירקון (north), שדרות שאול המלך
(south); carriageways averaged, corners where the lines meet. It is labelled "גבולות הרובע, בקירוב" along the line and
in a fixed key in the corner of the map. A light veil softens the ground outside it.

## Design and copy checks

- Skin A tokens only (paper, surf, sand, ink, ink2, sea, seah, deep, line); Noto Serif Hebrew 600 for the H2, card titles
  and the main pin; Assistant for the rest; pills for every button and chip; no gradients, no em dash.
- Place colours were run through the dataviz validator against sa-paper with all pairs: lightness, chroma, colour-blind
  separation (worst ΔE 9.2) and normal-vision floor (16.3) pass; contrast is a warning for green and orange, relieved
  because every marker also carries a white line icon (cap, tree, bag, tram, house), the filters are a legend, and the
  card names the type. Projects are named pills; renewal is a square.
- Language gate: the blacklist from the language-dna skill finds 0 hits in the visible text and in the card strings
  (no "מפה אינטראקטיבית", no "שכבה", no "תלת ממד"). "פרויקטים" are never called "שלנו" (publisher, not broker).
- Card stays inside the screen: right side of the map on desktop (330 px), a bottom sheet on the phone. The chosen pin
  gets a sea ring; project labels that would collide fold to a dot (still tappable).
- Gestures: `cooperativeGestures` on. On the phone a one-finger swipe over the map scrolled the page (scrollY 0 → 84,
  the page end) and left the map centre unchanged; two fingers move the map. Hebrew hint: "שתי אצבעות להזזת המפה".
  Desktop zoom with Ctrl + wheel, buttons bottom left.
- OSM attribution is always visible (not compact): "OpenFreeMap © OpenMapTiles Data from OpenStreetMap"; the caption
  under the map reads exactly "מפה להמחשה. מיקומים לפי OpenStreetMap; פרויקטי התחדשות לפי פרסומים, עודכן 7.10.2026."

## Verification (headless Chrome, `python shoot.py`, last run 7.10.2026)

| check | 1366x900 | 390x844 (mobile, touch) |
|---|---|---|
| page errors / console errors / failed requests | 0 / 0 / 0 | 0 / 0 / 0 |
| map idle, load | yes, 4.7 s | yes, 3.8 s |
| 3D buildings rendered in view | 200 | 148 |
| renewal pin → card | opened (clicked the ז'בוטינסקי 152 spot, the icon on top is ליסין 27), inside the screen | זלוציסטי 4, inside the screen |
| project pin → card | מגדלי כיכר המדינה with "לעמוד הפרויקט", inside | DUO with "לעמוד הפרויקט", inside |
| reset button | back to zoom 15, card closed | back to zoom 14.2, card closed |
| fonts | Noto Serif Hebrew and Assistant loaded | same |

Evidence class: code (DOM and map state checks) plus eyes (the screenshots in `shots/` were looked at).

## Known limits

- Renewal pins very close together stack at the opening zoom (רמז 25, 42, 44 within about 50 m; ז'בוטינסקי 133 and
  135 to 137; ליסין 27 and ז'בוטינסקי 152). Zooming in separates them.
- Daily-life data is only as complete as OSM: few kindergartens carry names; one café entry is a restaurant by name
  ("restaurant poisson Ada") but OSM tags it as a café. "קניות" holds supermarkets, pharmacies and cafés.
- The public Overpass server timed out five times; the answer came from its sister instance z.overpass-api.de
  (08:33 UTC).
- OpenFreeMap's public tiles carry no SLA; for the live site consider a fallback style or self-hosted tiles.

## How it could plug into the site

1. **Shortcode** in the nadlan-config plugin: `[nadlan_area_map key="rova-4"]`. PHP reads
   `assets/area-maps/rova-4.json` (this `data.json`), prints the same section markup with the data inline in
   `<script type="application/json" id="nlam-data-rova-4">`, and server-renders the list under the map (project links
   and addresses), so crawlers and screen readers get it without JavaScript.
2. **Assets**: split the CSS (prefix `nlam-`) and the script out of `preview.html` into `assets/area-map/area-map.css`
   and `area-map.js`; ship MapLibre 5.24.0 and the RTL plugin from the plugin's own assets rather than a CDN.
   Initialise with an IntersectionObserver when the band nears the screen, so the about 1 MB script never weighs on
   the first view (the speed series, HAD-421). Show a still image of the home view when WebGL is missing.
3. **Data refresh** stays offline: `geocode.py` → `fetch_osm.py` → `build_data.py`, reviewed, then released with the
   runner like any asset. Visitors never call Overpass or Nominatim.
4. **Placement** on /north-tel-aviv/rova-4/: after the price list and calculator, before "כיכר המדינה והמגדלים", which
   keeps the content-first order (H1, answer, prices, then the map).
5. **Project pages**: the design system says one map per page, and project pages already carry the nlpjx area map
   (the beam is frozen). Putting this band there needs the owner's choice: replace that map's surroundings layer with
   this data, or link to the Rova 4 band instead. Not decided here.

## Site component (AreaMap, 7.10.2026, second round)

Code: `scripts/project-stage/area_map/` (nothing committed, nothing live).

| file | what it is |
|---|---|
| `render_map.py` | `html(d, sfx="")` section markup (prefix `nlam`, ids `nlam<sfx>`, data in `data-cfg`), `CSS` (every selector starts with `.nlam`, checked by `python render_map.py`), `JS` (one classic script; the only global is the guarded `window.nlamInit`) |
| `rova-4.json` | the page data, made by `make_data.py` from this folder's `data.json`: 6 projects, 15 renewal pins, 77 places, the quarter line; nothing on the catalogue's fake city-centre point |
| `build_preview.py` | writes `component-preview.html` here: the page above, the section at full width, the rest of the page, then the same section in a 390px phone frame (two instances, one page) |
| `test_area_map.py` | the load test; screenshots `shots/component-*.png`, report `shots/component-report.json` |

How it loads: the section prints a calm placeholder of the final height ("המפה נטענת", filters inactive). An
IntersectionObserver (rootMargin 300px) starts the load: MapLibre 5.24.0 CSS and JS from cdnjs with the cdnjs
sha512 SRI, then the OpenFreeMap style and tiles, then the RTL plugin (jsdelivr; cdnjs does not carry it). If the
library fails, WebGL is missing, the style errors, or 20 s pass, the section switches to `data-state="fail"`: the
frame and filters hide and the server-rendered list of every place opens, with a short note.

Sizes without MapLibre (Rova 4 data): markup 32,593 bytes (6,364 gzip; about 20 KB of it is the data in
`data-cfg`, the rest is the heading, filters and the list), CSS 15,647 (2,877 gzip), JS 16,729 (6,467 gzip).
Total 64,969 bytes, 15,588 gzip.

Load proof (`python test_area_map.py`, 12 of 12 pass): page loaded and idle for 3 s with zero requests to cdnjs,
OpenFreeMap or jsdelivr; the first such request (maplibre-gl.css) left 0.17 s after the scroll; the first section
reached `ready` with 6 project pins and 15 renewal pins drawn, frame height 630 px before and after (no jump); the
second section stayed waiting until scrolled to; the hero pin opened its card with "לעמוד הפרויקט"; in the 390px frame
a renewal pin (זלוציסטי 4) opened its card inside the screen; no duplicate ids; zero page and console errors; with
cdnjs blocked the list of places showed instead of the map, again with zero page errors.

Plugin hookup (not done): a shortcode `[nadlan_area_map key="rova-4"]` that prints `html()` from the JSON and enqueues
CSS and JS once per page (the script is safe to print twice). Place it under the Rova 4 price list.
