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
  19:06: 6.33° below the horizon; corrected 1.10.2026 from the world's own suncalc, the first text said 5.7°). The Sun lamp is calibrated from the sky's own disc at that hour (orange and weaker at
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

## Evening v2 (1.10.2026)

The first evening picture (`living-evening.jpg`, 30.9) was rejected by the owner. It stays in this folder untouched; its
replacement is `living-evening-v2.jpg` (2048 x 1152) + `living-evening-v2-1200.jpg`. The comparison sheet
`evening-v2-contact.jpg` shows the old evening, the new one and the sunset hero side by side, and below them crops of the
2048 px frames at one scale (old towers, new towers, the new lamp and sofa).

### What was wrong, and what changed

| Rejected for | Fix |
|---|---|
| The far towers read as a checkerboard: half of every tower white squares, no floors, no structure | **Interior mapping** (below): every lit window is a room with a back wall, a ceiling, a floor and side walls, lit by its own lamp. Rooms 3.0 / 4.5 / 6.0 m wide on the towers' 1.5 m mullion grid, 2-3 rooms an apartment, lit in runs along a floor; glass towers keep a dark slab band between floors. About 27% of tower windows lit (30% of apartments x 82% of their rooms, + 3.5% single rooms), plus a dim glow in ~10% of the other rooms. Colour 2700-3800 K, a few cool-white rooms, ~7% TV-blue; ~36% of rooms with sheers drawn in from the sides, ~22% with blinds half down; brightness varies room by room |
| Bright dots across the sky (the ceiling downlights reflected in the glass) | **Light linking** (Cycles): every lamp and glowing surface of the apartment lights everything except the curtain-wall glass and the balcony railing glass. The glass still mirrors the lit room faintly, never a lamp. The sky is clean |
| A bright streak at the right (the linear pendant reflected in the glass) | Gone with the light linking; the pendant's own diffuser is softer (its own material, 1.6 instead of the bulbs' 6.0), so it reads as a brass bar with a warm line of light |
| A dim, muddy room; the grey sofa back a flat mass | The table lamp is visibly on (a translucent linen shade that glows, open below so the light pools on the table); the LED cove in the curtain pocket is now a real light (a 9.4 m strip, 60 W) that washes the sheers and the window frame; a soft fill from behind the camera (30 W, 3 x 1.6 m, invisible to the camera and kept out of the glass); a blue-hour white balance of 5,200 K; +0.2 EV. The camera moved slightly: 45 cm right, 15 cm forward, 7 cm higher (1.45 m), 3 deg more to the left, 78 deg instead of 82 deg, no tilt (the verticals stay straight; a lens shift frames it). It still looks out of the same window toward the sea (260.6 deg instead of 263.6 deg); the sofa takes less of the frame and the lamp, the lounge chair and the dining read |
| The city's low-rise | The same room model for the near low-rise (each window bay a room, 3 bays an apartment, about 38% lit), and the street lights at 0.20 instead of 0.10 |

**The time: 19:00 instead of 19:06** (same day, 21.9.2026). The world's own suncalc (`kikar_world.sun_at`) gives the sun
**5.06 deg below the horizon at 19:00** (bearing 274.0 deg). At 19:06 the same calculation gives **6.33 deg** below (the README
above said 5.7, a slip: the first evening render was made at 6.33), already past civil twilight: the afterglow over the sea is
gone and the lit room outshines the view. Six minutes earlier the western sky keeps its pink-violet band over the sea and
the room and the view balance by eye about 1:1. Previews at 18:54, 18:57, 19:00 and 19:06 were compared before choosing.

### The technique

Interior mapping, Joost van Dongen, "Interior Mapping: A new technique for rendering realistic buildings", CGI 2008:
https://www.proun-game.com/Oogst3D/CODING/InteriorMapping/InteriorMapping.pdf ; the idea as a three.js port:
https://github.com/codedgar/three-fenestra . Written as Cycles shader nodes (SVM, no OSL; `night_windows()` in
`kikar_world.py`): for each pixel of a window, the view ray (the shading point's incoming vector in the wall's frame: along
the wall, up, into the building) is intersected with the room's two side walls, its floor or ceiling and its back wall (3.2-6.2
m deep); the nearest hit is shaded by albedo (a pale or darker back wall, side walls, a white ceiling, a wooden floor) times
one lamp's light (a ceiling light or a standing lamp at a random place in the room, falling off with distance), then a
curtain or blind plane 20 cm behind the glass is tested along the same ray. It costs no geometry: the 9,079 buildings stay
one mesh. The result is depth and parallax: a lit back wall, a darker floor, a ceiling hot spot near a lamp, curtains.

### Real and illustration in v2

- **Real, unchanged:** the city (every building within 2 km at its surveyed height), the streets, the trees, the sea, the
  three towers, floor 30's height and facing, and the sun from the world's calculation (now at 19:00).
- **Illustration:** which windows are lit, the rooms behind them, their lamps, colours, curtains and blinds (random per
  building, floor and room; nothing is known about who is home); the street-light level; the apartment's lamps and their
  power; everything in the room, as before.
- **Photographic choices (tonal, like the window pull):** the lamps kept out of the glass's reflection (light linking: what a
  twilight photographer does by flagging or blending frames), the soft fill from behind the camera (like a bounce flash),
  the 5,200 K white balance, +0.2 EV.
- The day and sunset pictures do not use any of it: every v2 change sits behind the evening flag (`TOD["night"]` / `NIGHT`).
  Checked: a 320 x 180 day render and a 320 x 180 sunset render of the living room before and after the change have
  identical 16-bit pixels.

### Render

`python scripts/interior/render_kikar_proto.py living-evening-v2 160 96 12` (the shot `living_eve`, 12 of 16 threads):
2048 x 1152, 160 samples (adaptive, OIDN): **1,451 s (24 min)** on this laptop (the first evening: 1,354 s on 14 threads). 10 preview rounds before it (640 x 360 to 1024 x 576 at 24-32
samples, 1:1 crops of the towers, the city and the lamp at 48 samples, framing and time-of-day sheets).

### Verdict, honestly

**Close to the bar of `living-sunset.jpg`, not equal to it.** At the card size (1200 px) it reads as a premium blue-hour
photograph: a warm, lit room balanced with a blue sky and a lived-in city, the lamps visibly on, a clean sky, no streak,
and the towers read as buildings with floors and apartments, no longer a mosaic. What still falls short, looked at 1:1 on
the 2048 px frame:
- the lit windows are still procedural: at 3-8 px a floor the interior mapping's depth (back wall, ceiling hot spot,
  curtains) shows only on the nearest towers; farther away they are warm dashes on a regular grid;
- the tower bodies are dark silhouettes with a fine vertical pinstripe (the 1.5 m mullions on dark glass); the twin
  towers on the axis remain flat boxes (their data is height only, as noted above);
- the near low-rise city is a blue-grey mass with points of light; no street-lamp heads, no car lights, no lit signs;
- the lampshade's top is close to white; the sofa is still a large pale mass in the left foreground (now lit and textured,
  no longer muddy);
- one faint fleck (about 8 px, low contrast) in the sky of the right-hand panel: a reflection of a lit surface in the room,
  invisible at the card size;
- the sunset hero is carried by real light (the sun in the glass, its beams on the floor); the evening relies more on
  illustration (which windows are lit, the fill light), so it is by nature a step less "true".

What would close the rest: street lights as geometry along the surveyed streets (lamp heads and their pools), car light
trails on the main roads, and per-building facade data for the near towers; a GPU would allow 400+ samples.
