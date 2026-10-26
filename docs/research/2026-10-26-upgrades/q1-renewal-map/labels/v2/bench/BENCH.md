# Renewal map v2: competitors and world patterns (26.10.2026)

Captured with plain Chrome through Playwright (`bench2.py`, no stealth flags, no CAPTCHA solving), 26.10.2026 09:43 to 09:47 UTC,
at 1280 px and 390 px. A page that answered with a block or a challenge was recorded and left alone. Three captures from this
morning's first round (`v1-*.png`, 07:23 to 07:29 UTC, from `labels/bench/`) are reused where today's run was blocked; that round
used a visible Chrome with one automation flag switched off, and that is said wherever they are used.

| capture | what | status |
|---|---|---|
| `v1-madlan-tlv.png` | Madlan, for sale, Tel Aviv (map + list) | captured this morning (v1 round); today 403 in both modes (`madlan-map-*.png` is the block page) |
| `madlan-renewal-*.png` | madlan.co.il/urban-renewal | 404 (no such page) |
| `yad2-map-*.png` | Yad2, for sale map | blocked by a CAPTCHA (Radware Bot Manager); not solved, no notes on its map |
| `onmap-1280.png`, `onmap-390.png` | OnMap, buy, Ramat Gan | captured (headless) |
| `homeless-1280.png`, `homeless-390.png` | Homeless, for sale | captured (visible window); the board has no map; the phone capture came back blank |
| `govmap-1280.png`, `govmap-390.png` | govmap, Tel Aviv area | captured (headless) |
| `gov-renewal-1280.png`, `gov-renewal-390.png` | gov.il, the renewal authority's map topic page | captured; the map itself (ArcGIS) is `v1-gov-renewal-arcgis.png` |
| `v1-gov-renewal-arcgis.png` | the authority's renewal map (ArcGIS) | captured this morning (headless) |
| `airbnb-1280.png`, `airbnb-390.png` | Airbnb, Tel Aviv search | captured (headless) |
| `v1-zillow-nyc.png` | Zillow, New York | captured this morning (v1 round); today 403 |
| `v1-redfin-nyc.png` | Redfin, New York | captured this morning (v1 round); today blocked |
| `v1-google-il-z8.png` | Google Maps (Hebrew), Israel at zoom 8 | captured this morning (headless) |

## What each does well, and where it stops (from the captures)

| product | does well | stops short |
|---|---|---|
| **Madlan** (`v1-madlan-tlv.png`) | map and list side by side, list on the right (Hebrew reading order), sorting, "שכבות מידע" (layers), neighbourhood outline | the map marks are teal circles with a number only: no name, no meaning ("9318" of what?), circles overlap, white on `#03AFB5` samples at 2.7:1 (fails even AA) |
| **Yad2** | not captured (CAPTCHA) | |
| **OnMap** (`onmap-*.png`) | "מציג 269 מתוך 427 תוצאות": a count of what is in view; list cards synced to the map | about 270 identical blue dots that say nothing until clicked; on a phone the map is hidden behind a "מפה" button, list first |
| **Homeless** (`homeless-1280.png`) | city chips as shortcuts ("דירות למכירה ברמת גן") | no map on the board |
| **govmap** (`govmap-*.png`) | clean Hebrew base map, names placed without collisions, address and parcel search, layers, share | no renewal facts, no prices, nothing per city |
| **The authority's map** (`v1-gov-renewal-arcgis.png`, topic page `gov-renewal-1280.png`) | the only one with the real outline of every complex; search by address; city points with names | no counts, no stages, no prices on the map; names collide (בת ים); the topic page itself says it was last updated 01.09.2020 |
| **Airbnb** (`airbnb-*.png`) | the mark IS the information (a price pill); map and list in step; "מעל 1,000 בתים"; a pill that has no room shrinks to a blank mini pill | on a phone the pills pile on each other (`airbnb-390.png`: price pills piled over each other in one spot); the bottom sheet covers half the map |
| **Zillow** (`v1-zillow-nyc.png`) | "500 of 22,848 homes" (honest about what is drawn), price pills where they fit, filters as chips | at metro zoom hundreds of red dots that say nothing |
| **Redfin** (`v1-redfin-nyc.png`) | price pills | pills overlap heavily at metro zoom; white on `#01783E` samples at 5.6:1 (AA, not AAA) |
| **Google Maps** (`v1-google-il-z8.png`) | names ranked by importance, never overlapping, white halo; about 12 Israeli city names at zoom 8 | names only, no facts |

## The combined bar, and how v2 meets it

| bar (best of the field) | from | v2 |
|---|---|---|
| the mark carries the information | Airbnb, Zillow, Redfin | every tag: the city name plus the facts the chips choose (complexes and approved plans, a price range, homes added, what moved) and a strip of its stages |
| nothing overlaps, important first, names kept for the zoom | Google, govmap | tags placed by importance, never overlapping (measured in PROOF.md), name-only and dot steps for the rest |
| map and list in step, a count of what is in view | OnMap, Zillow, Airbnb, Madlan | panel beside the map ("ערים בתצוגה: N מתוך 79"), refreshed when the map moves; hover a row, the tag lights up |
| a phone view that keeps the map | Airbnb (sheet), not OnMap (map hidden) | a peek card at the bottom of the map, the full panel under it in the page flow; one finger still scrolls the page |
| search by address, name or plan | govmap, the authority's map | city, complex name or plan number, spelling folded (גבעתיים / גבעתים) |
| layers or filters | Madlan, Zillow | five chips that re-label the whole map |
| official renewal data per complex | the authority's map | every complex of the city with its stage at the authority, homes today and after, its last change and a link to its page and to "יומן המתחמים"; exact points are NOT drawn (the authority layer's reuse licence is unstated) |
| contrast | none of the Israeli competitors reaches AAA on its marks | AAA (7:1 and up) on every tag word and number |

**Beyond all of them together:** stage, price and momentum on the same tag; the sea as a label margin (crowded coastal cities float
their tags over the water with a thin line, a column no competitor uses); every number in the detail carries its source and date;
"מה זז" shows the complexes that moved, by name, on the map.
