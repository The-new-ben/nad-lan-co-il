# Kikar Hamedina, P9b: the inside of the towers ("דירה לדוגמה"), the plan

**30.9.2026, loop phase P9b, HAD-375.** Local only: no runner, no WordPress, no push. No `plugins/` product file was edited.
The prototype that proves this plan is in `interiors-proto/` (renders + README). The scripts are
`scripts/interior/kikar_world.py`, `kikar_interior.py` and `render_kikar_proto.py`.

The owner's bar (28.9.2026): the interiors must be "far higher quality" than Rainbow's styles and DUO's bare rooms.
This plan says what to show, how to derive it honestly, how to render it to that bar, and how it plugs into the world and
the page in 5 languages.

---

## 0. The decisions, in short

1. **Three example apartments, always labelled "דירה לדוגמה"**, each tied to a PUBLISHED size, never an invented one:
   - **A, 4 rooms, 140 m²**: the size of the three Globes deals (floors 38-39, 2.5.2025). One quarter of a floor.
   - **B, 5 rooms, 154 m² + 12 m² balcony**: the floor-35 ask (Sotheby's Israel). A quarter plus a corner.
   - **C, the penthouse, 258 m² + 57 m² outside**: the floor-39 ask (Sotheby's; Bizportal 19.4.2025). Half of a top floor.
   - The label names the source of the SIZE. The plan inside the walls is an illustration and the chip says so.
2. **The layout comes from the tower, not from imagination.** The glass line is the world's plate (the municipal footprint,
   the white curtain wall); four apartments a floor (453 / 117 floors = 3.9) make a quarter of about 150 m² gross, the
   size of the published 140 m² deals. Every room is on the glass; the core side holds the baths and storage.
3. **The twist is a selling feature, shown, not hidden.** Each floor turns 1.25°, so the same apartment faces a different
   bearing on every floor: tower C's "west" apartment faces 301.9° on floor 1, 265.6° on floor 30 and 253.1° on floor 40.
   The page shows it as a strip of the same window on floors 20, 30 and 38 (rendered in the prototype), and as
   **"your sunset day"**: the date the sun sets straight into your living room (computed below).
4. **The view out of every example window is the real city**, rendered from the world's data at the real height and
   bearing: every building at its surveyed height, the streets, the city's trees, the sea with the earth's curvature, the
   sun at the true hour. Three times: day, sunset, evening.
5. **Engine: Blender 5.2 Cycles, offline path tracing, on this machine** (no GPU: the integrated Radeon is not usable by
   Cycles here, so CPU). The output is the fleet's own format (equirectangular 360 + stills), opened by `tour.js`.
6. **Facilities are shown as they are published: "on one of the basement levels" (Ashtrom).** So the pool, gym and spa
   have NO windows and NO view in their renders, and carry "המקום להמחשה".
7. **Styles** are whole re-materialised renders of the same room (not overlays): "כמו במסירה", "עץ חם" (the prototype),
   "בהיר", "אבן". All procedural until the owner OKs downloading CC0 furniture (still open, FORGOTTEN row 27).
8. **Plugging in:** a button "היכנסו לדירה לדוגמה" in the world's Tower mode, next to "הנוף מהחלון", opens the tour on the
   chosen tower, floor band and facing; the page's 360 section (the fleet's `.nlat` card) gets Kikar's own `tour` words.
   `tour.js` needs a language option before fr/ru/ar (it is hard-coded RTL Hebrew today).
9. **One open fact changes every facing: the DIRECTION of the turn is not published** (world.json's model note; the world
   draws it counter-clockwise from above). With a clockwise turn, floor 30's sides would face 338°/68°/158°/248° instead of
   356°/86°/176°/266°. A west-facing example exists either way (one side is always within 45° of west), but the exact
   bearing, the per-floor strip and the sunset days depend on it. **Verify from a photo before release** (section 10).

---

## 1. What is real and what is an illustration

| Element | Status | Where it comes from |
|---|---|---|
| The tower's place, size and base orientation | **real** | the municipal building layer (GIS 513) via `hamedina/world.json` (C: centre 40.2 m E, 63.6 m N of the plot centre; side 32.6 m; base bearing 31.86°) |
| The turn, 1.25° a floor | **published** | Wikipedia, Mako 24.9.2026, Alum Eshet, WXG, MYS (conflict: 2.5° in one case study, logged in facts.md) |
| The turn's direction | **not published** | the world shows counter-clockwise; see decision 9 |
| Floor height 4.0 m (floor 30's slab at 116 m, the eye at 117.6 m) | **provisional** | 160 m / 40 floors (world.json model note) |
| The facade system | **published** | MYS: "a repetitive system of floor slabs and white curtain walls"; Alum Eshet: unitised floor-to-ceiling curtain wall, 300 mm aluminium/glass shading fins, insulated glass with built-in electric shading, full-height pivot windows with inner railings, 4,000 m of balcony railings |
| The fins every 1.5 m | illustration | the world's rhythm (the spacing is not published) |
| The plate's shape (a superellipse, n 4.5) | illustration | "circle-inspired", sized to the footprint; no floor plan is public |
| The view: buildings, heights, streets, trees, sea | **real** | world.json: 9,079 buildings within 2 km (city survey 2019), 1,433 streets, 685 green areas, 11,669 tree crowns (canopy 2024), the sea and the Yarkon (GIS 504) |
| The facades' textures, cars, roof clutter, waves, haze | illustration | procedural, to make the real geometry read as a lived-in city |
| The sun | **real** | the world's suncalc for 32.087°N, Israel's clock |
| The layout, room sizes, ceiling (3.05 m net), balcony, finishes, furniture | illustration | derived in section 3; the listings' "fishbone parquet, designer marble, VRF, high ceilings" are marketing claims and are used only as inspiration |

---

## 2. Which example apartments

| Example | Size on the label (sourced) | Where it sits in the illustration | Facing options | What the renders show |
|---|---|---|---|---|
| **A · 4 rooms** | 140 m², like the published deals on floors 38-39 (Globes 2.5.2025; the tower is not published) | one quarter of a floor: living-dining-kitchen on a flat side, the master bedroom in one corner, the second bedroom and the safe room (ממ"ד) in the other | the 4 sides of any floor (the plate is symmetric) | living (3 times), master bedroom, balcony, a 360 of the living room |
| **B · 5 rooms** | 154 m² + 12 m² balcony, like the floor-35 ask (Sotheby's Israel, south-east) | a quarter that takes the neighbouring corner | as A | living + balcony per side at floor 35 |
| **C · penthouse** | 258 m² + 57 m² outside (42 terrace + 15 balcony), like the floor-39 ask (Sotheby's; Bizportal) | half of the top floor, the terrace where the illustration's plate steps back (the set-back per floor is published but not quantified) | north-west-south, like the listing | living + terrace at sunset and evening |

**The label, everywhere (Hebrew master):**
- Chip: **"דירה לדוגמה"**.
- Line under the picture: **"דירה לדוגמה בגודל שפורסם בעסקאות: 4 חדרים, 140 מ״ר (גלובס, 2.5.2025). התכנון, הגמרים והריהוט להמחשה."**
- In the fold "מה בתמונה להמחשה" (small, not on the first line, per iron law 3 "unknown = omitted, never announced"):
  "תמהיל הדירות ותוכניות הקומה לא פורסמו. הנוף, הגובה והכיוון לפי נתוני העירייה והסיבוב שפורסם (1.25° לקומה)."

The coordinator asked for "the unit mix is not published" on the label. The site's law says an unknown is not announced
on the first line; the fold is where the world already keeps such notes. The chip and the line above are always visible.

---

## 3. How the layout is derived (honestly)

**The glass line.** world.js's plate for tower C: a superellipse (n 4.5) of 16.3 m half-size for the slab and 15.05 m for
the glass (the slab reaches 1.25 m beyond the glass). Area inside the glass: about 853 m².

**The core.** A "circular turning core built with slip forms" (Ashtrom; CivilEng). Its size is not published. The
illustration takes a 5.2 m radius (lifts, two stairs, shafts) and a 1.6 m lobby ring, so the depth on each side's axis is
8.25 m (15.05 - 6.8).

**Four apartments a floor.** 453 apartments over 117 floors (40 + 37 + 40) is 3.9 a floor. A quarter of the plate outside
the core ring is about 177 m² gross, which after walls and shafts is the published 140-150 m² (the deals: 140 m²; the
average: about 150 m², TheMarker 2021, Bizportal 2025).

**The balcony.** 4,000 m of balcony railings (Alum Eshet) over 453 apartments is about 8.8 m of railing each. On the slab's
1.25 m edge that is 8.8 x 1.25 = 11 m², close to the published "12 m² balcony" (floor 35). So the illustration's balcony
runs 8.8 m along the middle of the living room's side, under the slab above (a loggia), with a 1.1 m glass railing.
The world's towers draw the same railing on every side of every floor, and no fins in front of it.

**The rooms per facing (apartment A, any side).**
- **The flat middle of the side, about 9.6 m of glass:** living, dining and the kitchen behind them (the island
  parallel to the glass, the tall units on the back wall at 7.4 m). The balcony is in front.
- **The corner (the glass turns 45°):** the master bedroom, with the curved glass on two sides.
- **The other corner:** the second bedroom and the safe room (ממ"ד). Its window is a regulation blast window: the
  illustration keeps the curtain wall there, and the release must not show that room's window as floor-to-ceiling glass.
- **Toward the core:** the entrance hall, the baths, the dressing room, the laundry.

**What each side sees (bearings from the plot centre, `sight-landmarks.json`; floor 30 of tower C in brackets).**

| Side (floor 30) | Faces | What is in the window |
|---|---|---|
| west (265.6°) | the sea | the Old North to the sea, 2.1 km; the Herzliya Gymnasium; City Hall at 237.6° (to the left); the coast's hotels; the horizon at about 39 km |
| north-west corner (310.6°) | the port | the sea at 292.8°, Tel Aviv Port 314.5°, Reading lighthouse 327.3° and power station 333.6° |
| north (355.6°) | the park | the Sportek 355°, Ramat Aviv 11.5°, Tel Aviv University 26.8° |
| north-east corner (40.6°) | Park HaYarkon | Park HaYarkon (Ganei Yehoshua) 54.5° |
| east (85.6°) | Ramat Gan | the Ayalon 106°, Savidor station 109°, the Moshe Aviv tower 106° |
| south-east corner (130.6°) | the business district | the Ramat Gan towers, the Ayalon |
| south (175.6°) | Azrieli | Ichilov 177°, the Azrieli towers 170-173°, Azrieli Sarona 183°, the Kirya 188° |
| south-west corner (220.6°) | the city centre | Habima 213°, City Hall 238° |

(Tower C is the north-east tower, so its south and west windows also see towers B and A, 110-160 m away; the balcony
render shows tower A.)

**The twist, per floor (counter-clockwise, as the world draws it).**

| Tower C floor | Eye height | North side | East side | South side | West side |
|---|---|---|---|---|---|
| 1 | 1.6 m | 31.9° | 121.9° | 211.9° | 301.9° |
| 10 | 37.6 m | 20.6° | 110.6° | 200.6° | 290.6° |
| 20 | 77.6 m | 8.1° | 98.1° | 188.1° | 278.1° |
| 30 | 117.6 m | 355.6° | 85.6° | 175.6° | 265.6° |
| 35 | 137.6 m | 349.4° | 79.4° | 169.4° | 259.4° |
| 38 | 149.6 m | 345.6° | 75.6° | 165.6° | 255.6° |
| 40 | 157.6 m | 343.1° | 73.1° | 163.1° | 253.1° |

Tower A's floor 30 west side faces 262.4°; tower B's 263.4° (their base bearings are 28.65° and 29.63°).

**"Your sunset day" (a new feature this plan proposes).** Tel Aviv's sunset moves between 242.6° (December) and 298.7°
(June). The date the sun sets exactly on the axis of the west apartment's living room (tower C, computed with the world's
suncalc, ±0.5°):

| Floor | West side | The sun sets on the axis on |
|---|---|---|
| 5 | 296.9° | 29.5-2.6 and 10.7-14.7 (it stays near the axis for weeks around the solstice) |
| 10 | 290.6° | 6.5 and 5.8 |
| 20 | 278.1° | 5.4 and 6.9 |
| 25 | 271.9° | 23.3 and 20.9 |
| **30** | **265.6°** | **9.3 and 3.10** |
| 35 | 259.4° | 23.2 and 17.10 |
| 38 | 255.6° | 14.2 and 26.10 |
| 40 | 253.1° | 8.2 and 1.11 |

The prototype's sunset render is 21.9 at 17:36 (the sun at 262.8°, 12.7° high): three degrees left of the axis, which is
why the sun stands in the middle of the glass. The same computation works for every side and tower. Label: computed from
the sun's path and the published turn; the turn's direction is not published (decision 9).

---

## 4. The window view, from the world

- **Same data as the web world** (`hamedina/world.json`), so the view in the example apartment and the world's "הנוף
  מהחלון" agree: the camera stands at the real eye height (floor 30: the floor finish at 116.47 m; the camera 1.38 m above
  it) and looks along the real bearing of that side on that floor.
- **Everything real is in its place:** the buildings at their heights (0.1 m near, 0.5 m far), the street network at its
  widths, the canopy, the sea polygon with the breakwaters, the Yarkon, the square's park; towers A and B built floor by
  floor with the same twist, slabs, glass, fins and railings.
- **The sea to the horizon:** a curved surface (earth radius with refraction k 0.13), so the horizon dips about 0.33° below
  eye level at floor 30 and lies about 40 km out, as it does; the sea band is about 3° deep (2.1 km of city, then water).
- **The sky and the sun:** Blender's multiple-scattering sky at the true sun position, with coastal September air; the
  Sun lamp is CALIBRATED from the sky's own sun disc each render (radiance x solid angle), so colour and power match the
  hour (21.9, 17:36: warm, 43 units; 14:30: white, 54 units).
- **Aerial perspective:** every outside surface fades into the sky's own horizon colour in the direction it is seen
  (reach 6.5-7.5 km; 16 km for the sea), as the far city pales into the sky over Tel Aviv.
- **Three times:** day (21.9, 14:30), sunset (21.9, 17:36), evening (21.9, 19:06, the sun 6.33° below the horizon by the world's suncalc, corrected 1.10.2026 from 5.7°; the evening v2 render uses 19:00, 5.06° below: the
  blue hour, a share of the windows lit, the street glow).
- **The window pull.** Real-estate photography exposes the room and the view separately and blends them. The render does
  the same, physically inside Cycles: only what the camera sees THROUGH the curtain wall is darkened (x0.26 by day, x0.38
  at sunset, none in the evening); the light entering the room is untouched. So the room is exposed for itself and the
  view keeps its colour instead of burning white.
- **Two more photographic choices, both tonal, never content:** a gentle lens bloom in the compositor (only what is far
  brighter than white glows: the sun's disc, a lamp at night), and the sky's fill on diffuse surfaces taken 15% down and
  30% less blue than the sky one sees (in a city the shade is also lit by warm sunlit walls).

---

## 5. The facility rooms

Published: "a pool, a gym, a spa, treatment rooms and multi-purpose halls, on one of the basement levels" (Ashtrom); "lobby
with a security guard; sports club, spa and pool" (Sotheby's). What that means for the renders:
- **No windows, no view.** A basement pool is lit by its own light: a stone wall-washer, a light cove, the water's glow.
- **Rooms:** the pool (25 m lanes are not published: the illustration keeps a residents' pool, not a lap pool claim), the
  gym, the spa (a treatment room and a sauna), a multi-purpose hall, and the lobby (a high lobby is only a listing claim:
  "floor 4 is like 7"; the lobby height stays an illustration).
- **Scripts:** `kikar_facility.py` from `duo_facility.py`'s room kit, with the materials of `kikar_interior.py` (the same
  quality bar), each labelled "המקום להמחשה" and hung on the building walk (facilities.json `walk`: the lift's stops per
  tower, doors measured in the renders, like DUO's `aptStops`).

---

## 6. Design styles

The same room, re-materialised and re-rendered (never a flat overlay):
- **"כמו במסירה"** (as delivered): the finishes a developer delivers in Israel: porcelain, painted walls, the kitchen, no
  furniture. It sets expectations honestly.
- **"עץ חם"** (the prototype): herringbone oak, bouclé, travertine, honed white marble, walnut, brass.
- **"בהיר"**: whitened oak, linen, pale stone, sage.
- **"אבן"**: grey stone floor, dark oak, cognac leather, black steel.

The style switch in `tour.js` (the styles panel exists for Rainbow) keeps the direction and the place. Each style is one
more render per scene: plan the matrix accordingly (section 9).

---

## 7. The quality bar, and what reaches it

**The best off-plan and luxury sites of 2026, checked by web search on 30.9:**
- **R2U** renders "the actual sightline from each floor level", calibrated to elevation and the surrounding buildings, with
  a sun simulation and material swaps from the developer's finishing book; it claims 25-40% more pre-sale reservations
  when every unit is rendered, and a browser component that "loads in under 2 seconds"
  ([R2U, sightlines](https://r2u.io/en/blog/interactive-floor-plan-real-estate/),
  [R2U, pre-construction virtual tour](https://r2u.io/en/blog/pre-construction-virtual-tour-complete-guide/),
  [R2U, sunlight simulation](https://r2u.io/en/blog/sunlight-simulation-real-estate-sales/)).
- **Zillow SkyTour** (Gaussian splats from drone footage) and **Apartments.com / Matterport 3D Exteriors** show real,
  captured exteriors ([Zillow](https://www.zillow.com/news/take-home-listings-to-new-heights-with-skytour/),
  [Radiance Fields](https://radiancefields.com/zillow-adds-gaussian-splatting-support-with-skytour-unveiling)). A tower
  under construction cannot be captured inside yet.
- **Pre-rendered 360 tours** are path-traced (V-Ray, Corona, Lumion), a finite set of panoramas with hotspots, 2-6 weeks of
  studio work; **real-time Unreal / pixel streaming** adds free walking and time of day at a streaming cost
  ([archicgi](https://archicgi.com/3d-virtual-tours/), [Virtuelle](https://www.virtuelle.io/blog-posts/real-time-3d-tours-for-real-estate-pixel-streaming-vs-native-app)).
- **Luxury towers** market the view at sunrise, sunset and night (for example Aria Reserve Miami's east-west flow-through
  floors "to capture sunrise-to-sunset views") ([CondoBlackBook](https://www.condoblackbook.com/blog/what-new-luxury-miami-condos-will-be-completed-this-year)).
- **In Israel,** the 360 sample-apartment tours from renders are a standard studio product
  ([P360](https://www.p360.co.il/tour/setoru-teil/)), but none shows the real view per floor and facing of the tower.

**Our bar, per render (the checklist the prototype was iterated against):**
1. Path-traced light, the real sun and sky, contact shadows, no fake ambient.
2. A real view: the true city at the true height and bearing, the sea, haze; never a white-box city (the DUO and Rainbow
   views were white massing), never a stock photo.
3. Two-point perspective (level camera, straight verticals), eye 1.38-1.6 m, 80-90° lenses: how architects shoot.
4. Every edge rounded (bevels on every box, 5-segment upholstery), no perfect CG spheres or boxes.
5. Materials with micro detail: grain per plank and a tone per plank, bouclé loops, linen weave, stone pits and veins,
   brushed brass; roughness varies; nothing plastic.
6. Life, in restraint: a bowl of lemons, books, a folded throw, dense olive trees, sheers catching the light.
7. A restrained palette: the house's cream and ink; terracotta only as an accent.
8. The window pull (section 4) and AgX tone mapping, so neither the room nor the view is burned.
9. No bare room is shown as the default any more (the bare "as delivered" becomes a style, labelled).

**What the prototype reached:** see `interiors-proto/README.md` (quality notes, times, sizes). Short: the living room at
sunset and the corner bedroom read as premium photography; the balcony shot shows tower A turning, floor by floor, in the
real skyline. What is still below the bar: the near city is procedural texture on true geometry (at 100-300 m it reads
as a clean model, not a photo); the sofa and chairs are primitive-built (good silhouettes, no seams or wrinkles).

**What it would take to go further:**
1. **Real furniture and plants** (CC0 models, e.g. Poly Haven), with the owner's OK to download (FORGOTTEN row 27): the
   single biggest step for close-ups.
2. **A photographic city for the view:** Google Photorealistic 3D Tiles rendered once into the view plates (Q1 option b:
   a paid key and attribution; offline rendering of tiles must respect the terms) or a drone Gaussian splat (option c).
   Until then, per-building facade variety (balconies as geometry for the nearest 300 m) closes most of the gap.
3. **A GPU** (a rented cloud GPU or another machine): 10-20x faster, so 1,000+ renders become possible (section 9).
4. **Walking inside, continuous:** bake the lighting of each example apartment into a GLB (lightmaps) and walk it in
   three.js, the "continuous interior" of FORGOTTEN row 25. A later phase.

---

## 8. Engine options, checked on this machine

| Option | Quality | Cost | Verdict |
|---|---|---|---|
| **Blender 5.2 Cycles, offline** (installed: `C:\Program Files\Blender Foundation\Blender 5.2`) | path-traced, photographic | CPU only: Ryzen 7 7730U (8 cores / 16 threads), 13 GB RAM; the integrated Radeon is not offered to Cycles (HIP lists the CPU only) | **chosen**; the fleet's scripts already use it |
| three.js path tracer in the browser (three-gpu-pathtracer) | progressive, converges slowly | heavy on phones, minutes to converge | no, for a sales page |
| Baked lightmaps + three.js | good, walkable | a UV/bake pipeline per apartment, 5-15 MB per apartment | later, for continuous walking |
| Unreal pixel streaming | top | a streaming server per visitor | no (cost, latency, Israel hosting) |
| Gaussian splats | top for real places | needs the real place | only when a model apartment exists |

**Measured on this machine** (the prototype's final renders; details in the proto README): a 2K still at 160 samples
(adaptive, OIDN denoised) takes **7 to 23 minutes** (the balcony 7, the bedroom 13, the living room at sunset 18, in the
evening 23: interiors lit by lamps converge slowest); the 4096 x 2048 360 at 96 samples takes **43 minutes**; a scene
builds in 15-25 s (9,079 buildings, 14,587 cars, 11,669 trees, towers A-C floor by floor, the apartment).

---

## 9. The render matrix and the load budget

**The release set (tower C first, the tower the world opens on):**
- Example A on 3 floors (a low, a middle and a high band: 12, 24, 36) x 4 sides x the living 360 at the side's best hour
  (west and south: sunset; north and east: day) = 12 panoramas; plus the balcony and the bedroom stills for the west and
  north sides = 12 stills; plus the evening versions of the 4 floor-24 living rooms.
- Example B on floor 35 (the published south-east): living 360 + balcony. Example C on floor 39: living 360 + terrace, at
  sunset and evening.
- Facilities: pool, gym, spa, hall, lobby = 5 panoramas.
- Styles: 3 more styles x the 4 floor-24 living rooms = 12 panoramas.
- Total about 50 panoramas + 20 stills: on this CPU about 50 x 43 + 20 x 15 minutes = **about 41 hours**, four or five
  nights of background rendering, sequenced by `render_kikar_proto.py`'s pattern (it waits while another Blender runs).
  A rented GPU (Cycles on a current NVIDIA card is roughly 15-25 times this laptop's CPU) would do it in 2-3 hours.

**File sizes (measured on the prototype, JPG):** the 360 is 487 KB at 4096 x 2048 and 156 KB at 2048 x 1024 (the
furnished room compresses well at q82); its card 69 KB; the 2048 x 1152 stills 224-271 KB (q88); their 1200 px cards
80-100 KB. The budget per visitor action:
- Nothing interior loads with the page. The tour opens on a tap.
- The first picture is the 2048 x 1024 panorama (the `-2k.jpg`, 156 KB), then the 4096 one replaces it (487 KB); WebP
  or AVIF would save about 30-40% more.
- Stills: 1200 px cards (80-100 KB) in the page's gallery; the 2048 px originals (about 250 KB) only on a tap.
- A budget of **under 700 KB before the first view** and **under 3 MB per scene fully sharp**.

---

## 10. How it plugs in (the world, the page, 5 languages)

**The world's Tower mode** (`assets/project-stage/world/world.js`, `renderPanel()`, the row with "המגדל מבחוץ / הנוף
מהחלון"):
- When a tower, a floor and a facing are chosen, a third control appears under the facing row: **"היכנסו לדירה לדוגמה"**.
- It opens `tour.js` with the scenes of the nearest rendered floor band for that tower and facing (the chosen floor is
  kept separate from the scene's floor, and the tour says which floor the picture is from: the fleet's rule "the chosen
  unit is never the scene"), the times of day as a switch (**יום · שקיעה · ערב**), the places (living room, balcony,
  bedroom), the chip "דירה לדוגמה" and the sourced line.
- It sends `nl:example-apartment` { tower, floor, sceneFloor, facing, time } and sets `window.__nlpsPick.example = true`,
  so the WhatsApp line reads "דירה לדוגמה · מגדל C · קומה 30 · מערבה".
- The world stays frozen-safe: this is a panel button and an event; `engine.js` and the beam are not touched.

**The page** (`inc/project-stage.php`, `nadlan_ps_parts()`):
- The fleet's 360 section (`.nlat` card) with Kikar's own `tour` config: `dirs` words per side (the table in section 3),
  `facing`, `height`, `view_src`, `card_alt`, `card_title`. Without them Rainbow's words print (feature inventory, finding 5).
- The PHP hard-codes the floors 25/10/36 and the gate file `tour/living-25w-card.jpg`: make both config keys
  (`tour.floors`, `tour.gate`) in the build phase, or Kikar's files will not be found.
- File names in the fleet's pattern: `hamedina/tour/living-30w.jpg` (+ `-2k`, `-card`), `balcony-30w`, `bedroom-30nw`,
  and `-sunset` / `-evening` suffixes for the times (a new key; the tour's scene gets a `time`).
- `facilities.json` gets `tour` and `walk` for the basement rooms.

**`tour.js` needs a language option.** It sets `dir = 'rtl'` and `lang = 'he'` on its root today, so the fr/ru/ar pages
would show a Hebrew viewer. Add `o.lang` and the strings below.

**The words, in 5 languages (Hebrew is the master; each language page gets its cultural wording, not a literal one):**

| Key | עברית | English | Français | Русский | العربية |
|---|---|---|---|---|---|
| button | היכנסו לדירה לדוגמה | Step inside an example apartment | Visiter un appartement témoin | Зайти в пример квартиры | ادخلوا إلى شقة نموذجية |
| chip | דירה לדוגמה | Example apartment | Appartement témoin | Пример квартиры | شقة نموذجية |
| size line | דירה לדוגמה בגודל שפורסם בעסקאות: 4 חדרים, 140 מ״ר (גלובס, 2.5.2025) | An example at the size of the published deals: 4 rooms, 140 m² (Globes, 2.5.2025) | Un exemple à la taille des ventes publiées : 4 pièces, 140 m² (Globes, 2.5.2025) | Пример площадью как в опубликованных сделках: 4 комнаты, 140 м² (Globes, 2.5.2025) | مثال بمساحة الصفقات المنشورة: 4 غرف، 140 م² (غلوبس، 2.5.2025) |
| illustration | התכנון, הגמרים והריהוט להמחשה | The layout, finishes and furniture are illustrations | Plan, finitions et mobilier à titre d'illustration | Планировка, отделка и мебель условны | التصميم والتشطيبات والأثاث للتوضيح |
| times | יום · שקיעה · ערב | Day · Sunset · Evening | Jour · Coucher du soleil · Soir | День · Закат · Вечер | نهار · غروب · مساء |
| places | סלון · מרפסת · חדר השינה | Living room · Balcony · Bedroom | Séjour · Balcon · Chambre | Гостиная · Балкон · Спальня | الصالون · الشرفة · غرفة النوم |
| sunset day | השקיעה בציר הסלון: 3 באוקטובר | The sun sets on the living room's axis: 3 October | Le soleil se couche dans l'axe du séjour : 3 octobre | Солнце садится по оси гостиной: 3 октября | تغرب الشمس في محور الصالون: 3 أكتوبر |
| fold note | תמהיל הדירות ותוכניות הקומה לא פורסמו | The unit mix and floor plans are not published | La répartition des lots et les plans ne sont pas publiés | Состав квартир и планы этажей не опубликованы | لم تُنشر تشكيلة الشقق ومخططات الطوابق |

The Hebrew passes the language-DNA blacklist (no "סימולציה", "מודל", "טכנולוגיה", "פרוטוטייפ"). The Russian and
French need the Cyrillic font subset already on the P9 list.

---

## 11. What only the owner can decide, and what the coordinator should do next

**For the owner (in plain Hebrew, in the report):**
1. OK to download free (CC0) furniture and plant models? It is the biggest step up for close-ups (open since 28.9).
2. A cloud GPU for the full set (about 50 panoramas + 20 pictures, several nights on this laptop)? It costs money.
3. The penthouse example (C): OK to show a terrace as an illustration where the plate steps back?

**For the coordinator:**
1. **Verify the turn's direction** (clockwise or counter-clockwise seen from above) from a photo or the architect's
   drawings. It moves every facing, the view strip and the sunset days. Until then every such text says the direction is
   not published, as the world's fold already does.
2. **The ממ"ד window:** the second-bedroom corner must not show floor-to-ceiling glass in the release renders.
3. The build phase (after G1, Claude Design first): a design-system version for the "דירה לדוגמה" panel and the tour's
   time switch; then `tour.js` `lang`, the PHP `tour` keys, `kikar_facility.py`, the render matrix.
4. Consider the same interior pipeline for DUO and Rainbow: their 360s are the bare, white-massing renders the owner
   ruled "not looking good" on 28.9. The scripts here are the upgrade path (the world JSON is per project).
