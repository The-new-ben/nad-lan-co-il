# Kikar Hamedina world: P4 design prototype (local only)

A standalone three.js page that builds the area around the Kikar Hamedina towers from the city's real data, and a set of
screenshots for the owner and the designer. It is a design reference for phase P4 of
`docs/loop/KIKAR-HAMEDINA-LOOP.md`, not the product: nothing here is deployed, nothing touches `plugins/`, and the
frozen `engine.js` was not read or copied.

- Built 30.9.2026. Rendered on the local GPU (AMD Radeon, Direct3D11 through ANGLE) in Chrome, via Playwright.
- The house DNA: cream paper `#FAF7F1`, ink `#1B1A17` edges, one gold `#9C7A3C` accent, hairline `#E2DCD0`. It reads as a white
  architectural model. The towers are in champagne-gold glass with white slabs, the park is a muted green and the water a soft blue.
  Terracotta is not used, because there is no money CTA on these frames.

## Files

| File | What it is |
|---|---|
| `kikar-world.html` | The page. It loads three.js 0.170.0 (pinned, jsDelivr) and the Assistant and Noto Serif Hebrew fonts (Google Fonts) at view time. |
| `world-data.js` | The world as one JS object (`window.KIKAR_WORLD`), written by `prep_world.py`. About 1.5 MB. |
| `prep_world.py` | Builds `world-data.js` from the research files, the cached city GIS pages and three more read-only city layers. |
| `shoot.py` | Takes the screenshots with Playwright (`channel="chrome"`). `--desktop`, `--mobile`, a view name, or `--study`. |

To open the page, double-click `kikar-world.html` (it works from `file://`). The URL controls it:

- `?view=`: `aerial`, `overview`, `street`, `c30west`, `a30north`, `shade`, `twist`, `study`.
- `&sun=`: `jun09`, `jun13`, `jun17`, `dec09`, `dec13`, `dec17`.
- Keys `1` to `8` switch the view. The six sun chips at the bottom left switch the sun and keep the camera. Drag to orbit.
- Provisional switches: `&twist=cw` flips the turn direction, `&bfloors=40` gives tower B the city's 40 floors,
  `&fh=4.2` changes the floor height, and `&pond=0` hides the illustrative pond.

## The screenshots

Desktop screenshots are 1440×900. Phone screenshots are 390×844 CSS px at device scale 2, which saves as a 780×1688 PNG.

| PNG | What it shows | Sun |
|---|---|---|
| `kikar-a-aerial-three-quarter-{desktop,mobile}.png` | (a) Three-quarter aerial from the south-east, looking north-west over the square, the ring, the three towers and the city to the sea, the port, Reading and the Yarkon. Pins, tower tags and far landmarks are shown. | 21 June 09:00 |
| `kikar-a2-overview-25-places-{desktop,mobile}.png` | Extra frame: a high oblique, north up, from Park HaYarkon to Ichilov and from the Green Line to Savidor/the Red Line. It shows the 25 pins in one frame, because two of them (Ichilov, Red Line) sit behind the hero camera. | 21 December 13:00 |
| `kikar-b-street-level-ring-{desktop,mobile}.png` | (b) Eye height 1.65 m on the outer sidewalk of the ה' באייר ring, north-west, next to the new school, looking south-east at C, B and A. This is the one arc of the ring with a clear line to all three towers and every tower at least 145 m away (checked against the 2024 tree canopies). It is a level camera with a shifted, very wide lens (about 107° horizontal on desktop), so the verticals stay vertical. | 21 June 17:00 |
| `kikar-c1-window-tower-C-floor30-west-{desktop,mobile}.png` | (c) From tower C, floor 30, looking west (bearing 270°) down the Jabotinsky axis to the sea 2.0 km away. The eye is 117.6 m high and 0.35 m inside the glass line of the turned floor-30 plate. | 21 June 09:00 |
| `kikar-c2-window-tower-A-floor30-north-{desktop,mobile}.png` | (c) From tower A, floor 30, looking north (0°) to Sportek, Park HaYarkon, Reading and Ramat Aviv. Tower C twists at the right edge. The eye is 117.6 m high. | 21 December 13:00 |
| `kikar-d-sun-shade-21dec-1300-{desktop,mobile}.png` | (d) Sun and shade on 21 December at 13:00 (sun 31.2° high, bearing 202°), seen from the east-south-east so the shadows run across the frame. The frame has real shadow-mapped shadows, the sun-path dome (21.6 and 21.12 arcs, the six positions, a ray to the current sun) and a gold dashed outline of each tower's ground shadow with its length: A 286 m, B 278 m, C 286 m. | 21 December 13:00 |
| `kikar-d2-sun-study-6-times-desktop.png` | Extra frame, 1440×1350: the same camera at all six times. June is on the right and December on the left; the rows are 09:00, 13:00 and 17:00. December 17:00 is after sunset (16:41), so it is lit as dusk. | all six |
| `kikar-e-towers-twist-closeup-{desktop,mobile}.png` | (e) The three towers from the north-west at mid-height. The floor slabs, the gold corner lines (the four plate corners joined floor to floor draw the spiral) and the gold marks at floors 10/20/30 (40 on A and C) are shown, with floor tags 20/30/40. | 21 June 17:00 |

### Sun positions used

The positions come from the suncalc formulas (Agafonkin), cross-checked against an independent Python port. Bearings are
clockwise from true north. Local time is Israel Daylight Time (UTC+3) in June and Israel Standard Time (UTC+2) in December.

| | 09:00 | 13:00 | 17:00 | sunset |
|---|---|---|---|---|
| 21 June | 85.3°, 40.5° high | 204.8°, 80.6° high | 278.6°, 33.3° high | 19:51 |
| 21 December | 140.5°, 22.7° high | 201.8°, 31.2° high | 245.1°, -4.5° (set) | 16:41 |

Shadow lengths of a 160 m tower measured on the model: 207 m (June 09), 46-48 m (June 13), 265 m (June 17), 403 m (December 09)
and 286 m (December 13).

## Data used (all real, all read-only)

The frame is x metres east and z metres south of the plot centre 32.086758, 34.789776, the frame of `city-blocks.json`
(three.js north = -z). It uses 111,320 m per degree on both axes, the convention of `build_places.py`, which stretches north-south
by about 0.4%.

| Layer | Source | In the model |
|---|---|---|
| Buildings within 700 m | `../city-blocks.json` (GIS 513: footprint, 2019 survey height, else roof-base, DSM, floors × 3.2 m) | 1,096 extruded blocks with ink edges; the civic buildings get a warmer cream |
| Buildings 700 m to 2 km | the same GIS 513 fetch, cached in `scripts/project-stage/_cache/kikar-area/gis-513-*.json` | 7,983 context blocks, simplified to 1 m, lighter edges |
| The three towers | `../city-blocks.json` plot towers (GIS 513 footprints) + `../facts.md` | See "Provisional" below |
| Plot lots | `../city-blocks.json` plot lots (plan 2500ב, GIS 837) | Residential lot as pale stone, private open space as a light green wash |
| Street axes to 1.6 km | cached GIS 507/508, the width classes of `build_area_kikar.py` | Flat ribbons; the ה' באייר ring has a gold hairline on its axis |
| Green areas to 2.2 km | GIS 503, fetched by `prep_world.py` | Muted green; the square's park (`ככר המדינה`) is slightly deeper |
| Water | GIS 504, fetched: the Mediterranean, the Yarkon, the Yarkon/Ayalon stream, the Yarkon park lake | Soft blue |
| Tree canopies 2024 to 900 m | GIS 574, fetched | 4,563 canopy polygons, 11,669 crowns (see "Provisional") |
| 25 pins | `../places.json` + `../kikar-stage/quarter.json` (school north, community centre south, per the city's 4.8.2021 decision) | Ink/gold dots with Hebrew tags: kind and walking minutes (Mapbox, from the plot centre) or opening note |
| Far landmarks | `../sight-landmarks.json` | Serif gold-edged tags with distance: sea, port, Reading, Sportek, Ramat Aviv, TAU, City Hall |
| Eye rule | `../eye-kikar-provisional.json` | (floor - 1) × 4.0 m + 1.6 m |

The 25 pins are: the Kikar Hamedina school, the community centre, the Purple Line Ichilov station (planned 2028), the Red Line
Arlozorov station (open since 18.8.2023), Savidor Center railway, the Green Line Arlozorov station (planned), Ichilov Hospital,
Park HaYarkon (nearest edge), Abraham Park, ZEST, the Kikar Hamedina bakery café, City Market, Gucci, Open, Lehem Erez, HaKe'ara,
Miele, Tollman's, Marinado, Victory, the Herzliya Hebrew Gymnasium, the Tel Aviv Theatre, the Weizman Centre, the Arlozorov 97
sports centre and the Anan kindergarten.

`prep_world.py` fetched three city layers once with plain GET: 503 (to 2.2 km), 504 (to 6 km) and 574 (to 900 m). They are
cached as `proto-*.json` in the git-ignored `scripts/project-stage/_cache/kikar-area/`. No secrets were used, and nothing was
written anywhere but this folder and that cache.

## Provisional and illustrative (read before using any number)

1. **Floor height 4.0 m**. This is the provisional value of `eye-kikar-provisional.json`, which is 160 m / 40 floors. No floor-to-floor
   height is published, and the high lobby ("floor 4 is like 7") is a listing claim that is not modelled.
2. **Eye heights**. (floor - 1) × 4.0 + 1.6, so floor 30 = 117.6 m. The eye stands on the plate's axis toward the view bearing,
   0.35 m inside the glass line. P5 replaces this with the stage's `floorHeight()` and `measure_eyes.py`.
3. **Tower B floor count**. B is modelled as 37 floors and 157 m (Hebrew Wikipedia / Ashtrom). The city's GIS 513 says 40 floors
   and 158.2 m (DSM mean). 37 × 4.0 m = 148 m of floors, so a 9 m roof crown reaches the published 157 m. The crown's form is an
   illustration. `&bfloors=40` shows the city's version.
4. **The floor-plate shape**. No official plan is public. Each plate is a rounded square the size of the municipal footprint (GIS 513:
   32.6-33.5 m sides, 1,063-1,120 m², about "1,000 m²" per Calcalist). It has 4.5 m corners, a 0.45 m white slab, and a slab edge
   1.25 m beyond the glass line. Floor 1 is aligned to the footprint (edges at about 29-32°). The MYS "set back from the floor
   below" is not quantified, so it is not modelled. The label on the frames is "geometry from the municipal footprint + the
   published twist".
5. **The twist**. The 1.25° per floor comes from Wikipedia, Mako, Alum Eshet and Ashtrom; RMD Kwikform says 2.5°, so it is a
   CONFLICT. This gives 48.75° over 40 floors, or 45° over 37. The **direction is not published**: the model turns
   counter-clockwise seen from above (`&twist=cw` flips it).
6. **Glass colour and mullions**. The champagne-gold tint and the 1.5 m white mullion rhythm are an illustration. The source says a
   white aluminium curtain wall with 300 mm fins (Alum Eshet).
7. **The park pond**. Its position and shape are an ILLUSTRATION: an amorphous 2,500 m² shape in the middle of the park, drawn with a
   dashed outline and tagged "מיקום וצורה להמחשה". No geometry is published. The 2015 plan text says "up to 3.5 dunam,
   amorphous", and the 2025 press says "ecological pond". `&pond=0` removes it.
8. **Trees**. The canopy footprints are the city's 2024 layer. Large merged canopies are filled with crowns on a jittered 7 m grid,
   and the crown heights are an illustration. The square itself shows few trees because it was a construction site in 2024. The
   planned three rows of boulevard trees are not drawn.
9. **Street widths** are drawing classes (5/10/20/24 m); the axes are the city's.
10. **Walking minutes** on the pins are Mapbox walking times from the plot centre (provisional in `places.json`), not per tower.
11. **School / community centre naming conflict**. GIS 513, OSM and layer 553 disagree. The pins follow the municipal decision of
    4.8.2021: the school is in the north of the public plot and the community centre in the south.
12. **Beyond 2 km** the ground is plain paper with haze. The window views see real buildings to about 2 km and the real sea polygon
    beyond that.

## Notes for the designer

- The look: a white model under a warm sun, soft shadows (hemisphere fill ≈ sun), ink edges fading into a paper fog, gold kept to
  the towers, the ring hairline and the sun diagram. The tags follow the site's card style: a cream pill, a hairline border and a
  Hebrew name with a grey meta line.
- Tags never cover the towers (tower rectangles are reserved). In the hero aerial the square's own shops therefore show as dots
  only, and the overview frame names all 25.
- The street view needs an ultra-wide shifted lens: from the ring the towers are only 145-225 m away and 157-160 m tall. Every other
  arc of the ring has a tower within about 105 m or is blocked by the 2024 street trees.
- Open points for P5:
  - one shared stage layer that can turn a floor (the twist is a per-floor transform here);
  - per-tower and per-floor bearings;
  - real floor heights;
  - an official floor plan, which would replace the rounded-square plate.

## Reproduce

```
python docs/research/2026-09-30-kikar-hamedina/prototype/prep_world.py      # world-data.js (network only on the first run)
python docs/research/2026-09-30-kikar-hamedina/prototype/shoot.py           # 14 PNGs (7 views x desktop/mobile)
python docs/research/2026-09-30-kikar-hamedina/prototype/shoot.py --study   # the six-time sun study sheet
```
