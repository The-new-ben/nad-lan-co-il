# sdplan: "כל מגרש ברובע שדה דב" (S1 moat, local build 26.10.2026)

Nothing here is in the plugin yet. When Ben says go, the release copies:

| from (this folder) | to |
|---|---|
| `tool/sdplan.js` | `plugins/nadlan-config/assets/instruments/tools/sdplan.js` |
| `data/sdplan.json` (44 KB) | `plugins/nadlan-config/assets/instruments/data/sdplan.json` |
| `tool/registry-snippet.php`, function `s1_sdplan_registry_entry()` | the `'sdplan' => array(...)` entry inside `nadlan_nli_tools()` in `inc/instruments.php` (next to `'urtrack'`) |
| `tool/registry-snippet.php`, function `s1_sdplan_summary()` | an `if ( 'sdplan' === $id ) { ... }` branch in `nadlan_nli_summary()` (next to the `'urtrack'` branch), with `$path = dirname( __DIR__ ) . '/assets/instruments/data/sdplan.json';` |
| `tool/test_sdplan.js` | `tools/instruments/test_sdplan.js` (fix the two data paths) |

Then the page writer (`write_s1_page.py`) adds `[nadlan_tool id="sdplan"]` and the new sections to page 4730. The writer refuses to
post while `tools/sdplan.js` or `data/sdplan.json` answer anything but 200 on the live plugin path.

## What it does
- Two views: **מגרש אחד** (one plot: the official stage, the Israel Land Authority tender with the winner as recorded, units, bids,
  winning bid, development cost and land + development per unit, the design plan date, the first permit request, the first permit,
  the start of works, the nearest green line station and the air distance to the waterline, our project page and the price its
  developer reported) and **כל המגרשים** (a compound or the whole district: counts by stage, a table sortable by stage, bids,
  land per unit, distance to a station or to the sea, filtered by use: for sale, rental, assisted living, hotels and employment).
- The map: each compound north-up (the district as a strip, sea on top, north on the right), every plot in the colour of its
  official stage, labels placed by priority without overlaps (the selected plot, the stations, project names, plot numbers).
  A tap or Enter on a plot opens that plot. Six presets (the district, Rainbow 111, FIRST 2270, GINDI VOGUE 2206, the open tender
  3204, the plots nearest a station).
- The stage ladder (latest official record): בתכנית → שווק במכרז → תכנית עיצוב אושרה → הוגשה בקשה להיתר → התקבל היתר → בבנייה.
  A request or works record older than the plot's own plan deposit or tender publication is dropped (one case: plot 2207).
- Honesty: no delivery or occupancy year anywhere; an open tender shows its closing date; a tender with no bids says so;
  distances are air distances from the plot's centre. No permit holder name is read into the data (the GIS layers carry them).

## Data (`../build_s1_data.py`, official files read 26.10.2026 09:55 to 10:09 UTC)
Tel Aviv-Yafo GIS layers 837 (plots), 528 (plans and design plans), 772 (permit requests and permits), 499 (construction sites),
764 (green line stations); Israel Land Authority tender files (MichrazDetailsApi, 19 tenders, 44 plot files); OpenStreetMap
coastline (ODbL); the published developer prices of `scripts/project-stage/price_guide/sde-dov-prices.json` (the /sde-dov/prices/
page owns them; the tool links there). Refresh: rerun the fetches in dna.md section 3, then `build_s1_data.py`, `render_static_map.js`,
`s1_build_sections.py`, the test, and a release.

## Checks
- `node tool/test_sdplan.js`: 34 won plot files, 9,316 units, 8 open, 2 no-bid recomputed from the tender records; every plot's
  tender equals the file; the stage ladder; whitelisted keys only; 179 runs (every plot, every list combination, every preset)
  with no error, no long dash, no banned word (incl. the soil words: the hub tool never touches that subject), svg text >= 12 px.
- `php tool/test_summary.php`: the no-script summary lints and prints 73 rows.
- `python shot_s1.py`: 390 and 1280 px, no console errors, no sideways scroll, H1 → answer → CTAs → hero, a tap on 2270 opens it.

## Registry entry (text, as it goes into `nadlan_nli_tools()`)
```php
/* S1 (HAD-601 loop, Sde Dov hub moat): "כל מגרש ברובע שדה דב"; sdplan.json from the Tel Aviv GIS (plots 837, plans and design plans 528, permits 772, construction sites 499, green line stations 764), the Israel Land Authority tender files and the OSM waterline (docs/research/2026-10-26-upgrades/s1-sde-dov/build_s1_data.py, 26.10.2026) */
'sdplan' => array(
	'name' => 'כל מגרש ברובע שדה דב: מי זכה בו, בכמה, ובאיזה שלב הוא היום', 'cat' => 'ReferenceApplication', 'kicker' => 'מגרש אחר מגרש · רובע שדה דב',
	'desc' => 'לכל אחד מ־73 המגרשים למגורים, למלונאות ולתעסוקה ברובע שדה דב: היעוד והשטח בתכנית, מכרז רשות מקרקעי ישראל (הזוכה כפי שנרשם, יחידות הדיור, מספר ההצעות, סכום הזכייה והוצאות הפיתוח, וקרקע ופיתוח ליחידת דיור), תכנית העיצוב האדריכלי ותאריך אישורה, בקשה להיתר, היתר ותחילת עבודות לפי העירייה, תחנת הקו הירוק הקרובה והמרחק מהים, ובפרויקט שבשיווק: המחיר שדווח. מפה של כל מתחם לפי השלב הרשמי, וטבלה שמסדרים לפי שלב, הצעות, מחיר קרקע ליחידה או מרחק.',
	'data' => array( 'sdplan.json' ),
	'related' => array( '/sde-dov/prices/' => 'מחירי דירות בשדה דב', '/sde-dov/eshkol/' => 'מתחם אשכול', '/sde-dov/merkaz/' => 'מתחם המרכז', '/sde-dov/tzafon/' => 'מתחם הצפון', '/sde-dov/transport/' => 'תחבורה והקו הירוק', '/purchase-tax-calculator/' => 'מחשבון מס רכישה' ),
),
```
All six related URLs answered 200 on 26.10.2026. "מחירי דירות בשדה דב" links only to its owner, /sde-dov/prices/ (keyword guard).

## No-script summary
`s1_sdplan_summary()` prints one paragraph (73 plots, the count at each stage, 9,316 units in the tenders, 7 open-tender plots, how the
stage is decided, "air distances", "no delivery date") and a 73-row table: plot, compound, project or winner, units, stage with its
date, nearest station with the distance. It reads the same `sdplan.json`, so the summary and the tool never disagree.

## Design (NadLan Instruments)
Ink `#12202A`, ink 2 `#3E4C58`, sea `#2F6F86`, deep `#1F4B5C`, line `#D3DCE2`, red `#C42550` only for a tender with no bids; the stage
ramp `#EEF2F5 → #CFE0E7 → #8DB4C3 → #4F8BA0 → #2F6F86 → #1F4B5C` (light paper to deep sea, one hue); sea fill `#E4EEF2`.
IBM Plex Sans Hebrew for words, IBM Plex Mono for plot numbers and amounts. Why it is not the default AI look: it is a survey
sheet (a municipal plot plan in one cold hue with mono plot numbers), with no cream, no gold, no gradients and no rounded card wall.
