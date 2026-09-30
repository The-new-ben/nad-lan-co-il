# Kikar Hamedina P9b prototype: "דירה לדוגמה", tower C, floor 30, facing west

**30.9.2026, local only.** One example apartment (4 rooms, the size of the published 140 m² deals, Globes 2.5.2025)
inside tower C on floor 30, facing the sea, rendered with Blender 5.2 Cycles on this laptop. The plan it proves is
`../interiors-plan.md`. Every picture here is an illustration and must carry "דירה לדוגמה" wherever it is shown.

## The files

| File | What | Size |
|---|---|---|
| `living-sunset.jpg` (2048 x 1152) + `-1200.jpg` | **the hero**: the living room on 21.9 at 17:36, looking straight out (263.6°), the sun in the glass | 224 KB / 81 KB |
| `living-day.jpg` + `-1200.jpg` | the living room at 14:30, from the hall's corner, three-quarters (the art, the console, the sofa, the dining) | see the log below |
| `living-evening.jpg` + `-1200.jpg` | the living room at 19:06 (the blue hour), the lamps on, the city lit | see the log below |
| `bedroom-day.jpg` + `-1200.jpg` | the corner bedroom at 14:30: the curved glass, the sea, Park HaYarkon's green to the north-west | 244 KB / 90 KB |
| `balcony-sunset.jpg` + `-1200.jpg` | on the balcony at 17:36, looking at tower A (212°) turning floor by floor, and the city | 271 KB / 100 KB |
| `living360-sunset.jpg` (4096 x 2048), `-2k.jpg`, `-card.jpg` | the living room as a 360 equirectangular panorama, centre = the glass, cut by `cut_tour.py` exactly like the fleet's tour pictures | 487 KB / 156 KB / 69 KB |
| `twist-floor20.jpg`, `twist-floor30.jpg`, `twist-floor38.jpg` (1280 x 720) | the same window of the same apartment on floors 20, 30 and 38 (facing 278.1°, 265.6°, 255.6°): the view turns with the tower | about 150 KB each |
| `plan-floor30-towerC.png` | the floor diagram: the plate, the core, the four quarters, the rooms, the balcony, the fins, the cameras | |

Scripts (all in `scripts/interior/`): `kikar_world.py` (the city, the three towers, the sky and the sun, the outside
materials), `kikar_interior.py` (the apartment, the finishes, the furniture, the lights, the cameras; preview mode
`KH_CAMS`), `render_kikar_proto.py` (this set), `kikar_plan_diagram.py` (the diagram). Raw 16-bit PNGs and the ~60
preview renders and contact sheets stay in `scripts/interior/_renders/kikar/` (not committed).

## What is REAL in these pictures

- **The view:** every building within 2 km of the plot at its surveyed height (`hamedina/world.json`: 9,079 buildings
  from the municipal layer and the 2019 survey), the streets at their width class, the city's 2024 tree canopy (11,669
  crowns), the sea polygon with its breakwaters, the Yarkon. The sea is a curved surface (the horizon about 40 km out,
  0.33° below eye level). The coast is 2.1 km away at this bearing.
- **The height:** floor 30: the slab at 116.0 m, the floor finish at 116.47 m, the camera 1.38 m above it (117.85 m).
  The world's window view uses an eye of 117.6 m; the difference does not show. The 4.0 m floor height is the world's
  provisional value (160 m / 40 floors; floor heights are not published).
- **The facing:** floor 30's plate turned 29 x 1.25° from the base footprint's 31.86°, so the west side faces 265.6°.
  **Caveat:** the turn's DIRECTION is not published; like the world, the render turns counter-clockwise seen from above.
  With a clockwise turn the same side would face about 338°, and another side about 248°.
- **The facade system:** white slabs 0.45 m thick, reaching 1.25 m beyond the glass (the world's numbers); floor-to-ceiling
  glass; white aluminium fins 300 mm deep (Alum Eshet); a full-height pivot window with an inner railing (Alum Eshet;
  visible left of the balcony and in the bedroom); a balcony railing (Alum Eshet: 4,000 m of them). Towers A and B stand
  where the municipal layer puts them, floor by floor with the same turn, 110-160 m away.
- **The sun:** the world's suncalc for 21.9.2026, Israel daylight time (14:30: 226.8°, 48.5° high; 17:36: 262.8°, 12.7°;
  19:06: 5.7° below the horizon). The Sun lamp is calibrated from the sky's own disc at that hour (orange and weaker at
  sunset). On that day the sun sets 3° from this living room's axis; the exact alignment for floor 30 falls on 9.3 and
  3.10 (the plan's "sunset day" table).

## What is an ILLUSTRATION

- The layout (one quarter of the floor; the core's size is not published), the room sizes, the 3.05 m ceiling, the
  balcony's 8.8 x 1.25 m (derived from the railing length, section 3 of the plan).
- Every finish and piece of furniture: herringbone oak, bouclé, travertine, honed marble, walnut, oak veneer, brass,
  linen, the olive trees, the lemons. Built from primitives and procedural materials; nothing was downloaded.
- In the city: the facades' textures (plaster tones, windows, shutters, recessed balconies), the cars, the roof clutter,
  the tree shapes, the waves, the haze, the fins' 1.5 m spacing.
- Three photographic choices, tonal only: the window pull (the view through the glass x0.26 by day, x0.38 at sunset, x0.15
  for the three-quarter day shot with +0.8 EV on the room; none in the evening), a gentle lens bloom (only what is far
  brighter than white: the sun's disc, lamps), and the sky's fill on diffuse surfaces 15% weaker and 30% less blue than
  the sky one sees.

## How it was made, and how it was iterated

`python scripts/interior/render_kikar_proto.py all 160 96 14`: 2K stills at up to 160 samples (adaptive, OIDN), the 360 at
96, AgX base contrast, 14 of 16 CPU threads (AMD Ryzen 7 7730U, 13 GB; the integrated Radeon is not offered to Cycles).

Looked at critically after every round (9 preview rounds, ~60 renders, contact sheets), and fixed:
1. a blown-out exposure, the view burned white: the window pull and AgX;
2. a white-massing city (the old DUO/Rainbow look): plaster tones, windows with reveals, recessed balconies, roller
   shutters, roof heaters and air conditioners, parked cars, the canopy, the haze toward the sky's own horizon colour;
3. an invisible sea: a darker, rougher sea with its own haze reach, on a curved surface;
4. "marshmallow" upholstery: tailored 5-segment cushions with piping, a real back frame, sewn pillows with pinched seams;
5. sparse "bonsai" olives: 5,000-9,000 leaves on three levels of branches;
6. wavy "zebra" bands in the parquet: fine grain along each plank and a tone per plank;
7. blotchy fabric that read as marble; a black balcony-door pull standing in the middle of the view;
8. a camera inside the core wall (the first plan's core was too big: now 5.2 m + a 1.6 m lobby ring, 8.25 m of depth);
9. **white ground and blue "water" patches between the buildings:** the boolean that cuts the sea out of the land left
   an empty first material slot, so the whole ground rendered with Blender's default white; found by ray-casting the
   patches, fixed in `build_ground` (every final was re-rendered after it);
10. evening windows as a coarse mosaic of white panes: dimmer, warmer, lit in runs along a floor; the downlights'
    reflections in the glass softened.

## Quality reached, honestly

- **At the owner's bar:** the living room at sunset, the corner bedroom and the balcony read as premium real-estate
  photography: warm, real light, a real view with the sea and the true skyline, nothing plastic. The 360 is a furnished,
  sunlit room with the kitchen, the dining and the view, not a bare box.
- **Still below the bar, and what closes it:**
  - close-ups of furniture: primitive-built pieces have good silhouettes but no seams, stitching or natural wrinkles;
    CC0 models (Poly Haven), with the owner's OK to download, close this;
  - the near city (100-300 m) reads as a clean, true model, not a photograph; balconies as geometry for the nearest
    blocks, or Google's photoreal tiles (a paid key, the owner's Q1) would close it;
  - the evening's lit towers are still a pattern, not apartments; a lit-window model per floor band would help;
  - the twin towers on the axis are flat boxes (their facade data is height only).
- **Speed:** 7-23 minutes a still and 43 minutes a 360 on this laptop; the full set of the plan needs a GPU or several
  nights.

## Timings and sizes on this machine (render_kikar_proto.log, 30.9)

| Item | Resolution | Samples | Time |
|---|---|---|---|
| living-sunset | 2048 x 1152 | 160 | 1,056 s |
| bedroom-day | 2048 x 1152 | 160 | 761 s |
| balcony-sunset | 2048 x 1152 | 160 | 420 s |
| living-day | 2048 x 1152 | 160 | TIME-DAY |
| living-evening | 2048 x 1152 | 160 | TIME-EVE |
| living360-sunset | 4096 x 2048 | 96 | 2,600 s |
| twist-floor20/30/38 | 1280 x 720 | 48 | 70-73 s each |
