# Climate lab: sun, wind and rain inside one apartment (HAD-803)

LIVE SINCE 22.11.2026 (Ben: "מאשר להעלות הכל") at https://nad-lan.co.il/tour/climate/ : a static folder under <site root>/tour/climate/,
linked from nowhere on the site and not in the sitemap (the noindex line was removed on 22.11.2026: indexing is Ben's decision only; indexing is never requested), no plugin file and no version bump. Uploaded with scripts/had801/tour_ship.py, 50 files
md5-verified. Rollback = rename or remove tour/climate/ on the server. The host rate-limits .glb and .json (429 after a burst), so
the page loads byte-identical .js twins (E-4A.json.js, models.json.js, *.glb.js). Nothing in the live designer, project pages, maps, the beam or
`assets/showroom-engine/engine.js` was touched. The lab runs on its own copy of the designer in `./designer/`.

Open it: serve the repo root (`python -m http.server 47961 --bind 127.0.0.1`) and open
`http://127.0.0.1:47961/docs/design-lab/climate-lab/` (`?card=rain` etc. opens on one answer). One-click for Ben:
`D:\00 מוכן להצגה\16 לפתוח את מעבדת השמש, הרוח והגשם במחשב הזה.bat`.

## History
- 22.11.2026 11:32-11:39: built by session local_645b8055 (package 2, apartment designer), which then froze on an approval card.
  Its exact files are kept untouched in `../climate-lab-backup-from-645b8055-2026-11-22/` (MANIFEST.md5 = fingerprints).
- 22.11.2026 evening: taken over and finished by a side session of local_abb2e8c1 (Opus 5.5):
  - fixed the walk camera going to NaN on the first frame (designer/space.js, lab copy only: negative first dt and a zero-length
    step to the spot you already stand on). The same latent line exists in the live
    `plugins/nadlan-config/assets/designer/space.js:404` - reported, not touched.
  - short answers with a picture behind each (pictures are taken from the 3D scene at load): sunset by month and room, sun in the
    living room (winter hours, depth, summer hours), a draft through the home, cooking smells in or out, rain on windows and balcony,
    which way the apartment faces and what it means day to day.
  - the sun disc in the sky at its real position; lower fill light so the sun patch on the floor reads; plan labels readable.
  - `__lab.film()`: a 54 s scripted walk used for the screen recording (D:\Media\Captures\climate-lab-had803\, asset AST-12100).

## Which apartment, and why not Rainbow
The brief asked for "a Rainbow apartment the designer already knows". The designer knows no Rainbow apartment: its plans are
Ashira E-3B, E-4A, E-5E, E-5F (redrawn from the published sales plans) and three example flats. Rainbow has only illustrative
schematic SVGs (`assets/projects/rainbow-tel-aviv/plans/`, marked "not an official sales plan"). Running sun hours on an invented
plan would be inventing facts, so the lab stays on Ashira E-4A (north arrow 11° from the sales plan). A Rainbow plan drops in the
moment a real sales plan is redrawn into the designer's JSON format.

## Data and sources
- Sun: NOAA solar position equations (gml.noaa.gov/grad/solcalc/calcdetails.html), full calculation per date, Israel time
  (summer time from the browser's time-zone table), site 32.10 N 34.785 E. Floor sampled every 40 cm, every 10 minutes.
  Shading: the apartment's own walls, window sills and heads, and the slab of the floor above (also over the balcony).
- Wind by season and hour: Israel Meteorological Service, aviation climate summary for Ben Gurion airport, observations
  1999-2009 (ims.gov.il ... climate_airport_ben_gurion.pdf). That station is about 16 km inland.
- Winter storm wind turning SW → W → NW: Berkovic and Alpert, Tel Aviv University, The Open Atmospheric Science Journal 2018,
  Beit Dagan station 1974-2012.

## Not real yet
- Neighbouring towers are not in the model: no shading by them and no blocking of the sunset.
- The sea and the city outside the window are an illustration.
- Wind is not from a coastal station yet (Tel Aviv coast / Hof Tel Aviv station data was not fetched); it is the airport summary.
- Wind and rain are an illustration of direction and path, not an engineering air-flow or driven-rain calculation.
- No Claude Design board was made in this takeover; the lab's own look (synoptic weather chart on an architect's sheet:
  sheet #F2F5F7, ink #0F2233, cobalt #1F5FA8, sun #FFC400, air #0B7285/#66C2D0, rain #3B4CC0; IBM Plex Sans Hebrew + IBM Plex
  Mono; square corners, no shadows) is the design to review. Not the default look: no cream, no brass, no Inter.
- Never checked on a real phone; phone width checked headless (390 px).
