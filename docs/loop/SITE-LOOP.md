# The site loop: the whole of nad-lan.co.il at the highest level (started 24.9.2026 night)

**Owner's order (24.9.2026):** loop yourself toward the target, take responsibility for everything, never work a minute
without Claude Design, do it methodically, stop giving the owner homework. Not only Rainbow: DUO and the other projects,
then the home page and the whole site. The lower bar: Hauzd (https://olae-tower.hauzd.app/) for the building and the
apartment picker, and the EcoCity configurator (https://profshor.com/cfg/a39/l39a) for the inside of an apartment; above
Simplex, Zillow, Matterport and every other leader. Every project page is a whole information system around the project.

**How each loop turn works** (the prompt lives in the session's cron job; this file is its memory):
1. Read this board, `git log -5`, and the live health (`/wp-json/nadlan/v1/health`).
2. Collect finished outside work (the ChatGPT deep research below; background agents' reports).
3. Take the first item that is not done and not blocked. Do it end to end: Claude Design first (artifact
   L9Nqz7Viv7K3MYeZrBc9s8, publish a new version) → code → local harness and the GPU journey
   (`scripts/project-stage/pagejourney.py`) → runner dry run → release → the journey on the live site, desktop and phone,
   looked at → public-source audit before and after → commit and push → Linear comment (HAD-221 for Rainbow; Linear is at
   its free issue limit, so comment on existing issues) and a Notion row → a short Hebrew report with screenshots to the
   owner (SendUserFile).
4. Update this board: the item's state, evidence, and the next item. If something needs the owner, write it under
   "Waiting for the owner", move on, and mention it once in the report; never stop the loop for it.

**Laws that never bend:** CLAUDE.md iron laws; the recipe (`docs/research/2026-09-24-rainbow-run/unit-layer-and-recipes.md`
section 3: 13 rules, 30 rows, the unit-selection contract); no invented facts (unknown is omitted, illustrations are
labelled in the caption); EcoCity's content never comes back; no noindex or sitemap changes; the URL word law; secrets
only inside runners; every release through a runner with drift check, lint, backups, page checks and automatic rollback.

## Research in hand (docs/research/2026-09-24-rainbow-run/)
- `unit-layer-and-recipes.md`: the old engine's 6 demo units, its capabilities with file:line, the merged recipe, the
  Einstein prototype, the gap list, the proposal for units in the new stage.
- `rainbow-facts.md`: 480 approved (229 tower + 251 boutique), 459 per the developer; tower 39 floors in the lot's NE
  corner; 3-5 apartments per floor (developer, 7.2023); floor height 3.5-4.0 m; pools on two boutique roofs; average
  NIS/m² 75K (pre-sale) → 85.7K (2025), 81,782 cumulative through Q1 2026; 5 deals with a floor (Globes 11.2023).
- `worlds.md`: the Sde Dov and Somail tours (three.js, wrong positions) and the Google-tiles "earth" views (true, not
  cinematic, a 401 layer); the 12 Sde Dov and Einstein-axis projects; the find-place data (4,495 places) for a real quarter.
- `engine-journey.md`, `competitors.md`: the earlier maps.
- `hauzd-teardown.md` (the facade is the interface: per-unit hover, fly-to, card, plans rail, drone 360 column, walk; our edge: 6 MB vs 659 MB, SEO, data), `tech-stack.md` (pre-render what the buyer looks at, live only what they move through; Blender orbit frames with unit masks; Google 3D view at the floor; Blender 360 rooms; LiveKit).
- PRIVATE, never in this public repo: EcoCity configurator teardown and all competitor/Google screenshots are in C:/Users/777/nad-lan/_private-research/2026-09-24-rainbow-run/ (Hiway VR: one pre-rendered 6000x3000 360 per room per scheme; drone 360 per floor for the view).
- `deep-research-rainbow.md` (ChatGPT Pro deep research, collected 25.9): no public floor plans exist (so real apartments per
  floor cannot be drawn); 459 units (480 in the 2023 plan), six boutique buildings, the plan finally approved 17.1.2024;
  **275 of 459 sold** by the H1 2026 report (Globes 27.8.2026, re-checked); six deals tied to a floor (Globes 29.11.2023 from
  the Tax Authority, Bizportal 19.7.2023) and Waldman's high floor; Madlan's "670 deals" mixes nearby addresses; lot 306 to
  the west: up to 11 floors in the 2024 tender.

## The board

| # | Item | State | Evidence / notes |
|---|---|---|---|
| R1 | Rainbow facts fixed on the page and the stage | **done 24.9 (1.72.258)** | the stage: tower in lot 111's NE corner (its official outline from the Tel Aviv plans layer), 39 floors, 3.75 m, pools on two boutique roofs, turned 10° like the lot, shore 713 m; view and beam start at the tower (32.10354, 34.78466); demo units never feed public numbers (the "82-210 מ״ר" is gone); the page text: writer's notes removed, 459 (480 approved), NIS/m² 81,782 per the developer's reports. Next inside R2/R4: the lot's full real layout (150 x 75 m, long N-S) |
| R2 | Rainbow page to the recipe: hero with the two CTAs and the building in the first fold, the answer paragraph (names, developer, place, status, mix, sourced prices, keywords), six facts, progress, one FAQ with one FAQPage schema, the notice opening the article and the disclaimers last | **done 25.9 (1.72.259-260)** | DS v12-14. The first fold on 1440x900: text column (h1, lead, two buttons), the stage 716x660 and Meital's rail; on a phone the stage right after the buttons (eyes, live GPU journeys). One FAQ, one FAQPage (10 questions); one facts table and one progress band (the old ones are not printed there); the facts say 275 of 459 sold. The page's promises made true: the meta and social description, the social picture (the old showroom poster advertised unit picking), the article's description of the old engine, the byline date; the card gallery's three AI resort pictures (tower on the beach, a lagoon courtyard) taken off. Public source GREEN; the notice back at the article's opening (owner 29.8; 1.72.259 had lifted it and the audit caught it) |
| R3 | Rainbow apartments in the stage: floor + side arcs, the card, `?unit=`, the cone and the view per apartment. DS first | **done 25.9 (1.72.261)** | The owner ruled (a): example apartments with a direction, labelled. DS v15-16. Four per tower floor, one per side; the pick snaps, the arc is drawn, the card, view and caption say "דירה לדוגמה"; `?unit=24-n` opens it (live: floor 24 north, the view toward Tel Baruch, the beam north). With it, R8's core: ProjectDeals, seven sold apartments tied to a floor with the source on every row, tower rows open their floor; the floor card's line from sources. Linear HAD-286. Next inside R3 when data comes: real plans per apartment |
| R4 | Rainbow surroundings: the real Sde Dov quarter in the white-model style from the find-place data; our 11 projects clickable with a card and "what you see from Rainbow toward it"; facilities clickable | **part 1 done 25.9 (1.72.264-265)**; **R4b part A done 25.9 (1.72.266)**; **done 25.9 (1.72.264-268)** | DS v18-19 (QuarterPins). Live: our eight project pages around Rainbow at their true places as pale translucent volumes by their floors (Rainbow the one solid building), five places (the light rail station 511 m, the school 290 m, the park 186 m, the beach 839 m, the Yarkon estuary 802 m); a pin per item, hidden behind Rainbow's tower, faded by distance, never over another pin (pincheck.py: 8 of 24 steps overlapped on 264, none on 265); the card (developer, status, floors, units, distance and direction, the source; no prices of other projects) and "מה רואים מריינבו לכיוונו" (the exact bearing, the view says "קומה 25 · לכיוון זוהי"). Data: quarter.json from our pages and find-place (build_quarter_rainbow.py). Linear HAD-288. **R4b part A (1.72.266, DS v20 StageLot, Linear HAD-289):** Rainbow's lot from its official line (long north to south, 8,499 m² computed), the tower at its true point (it stood ~30 m off), six boutique buildings by the design plan's rules (8 m apart, 12 m from the tower, 5 m back in the west; places marked as illustration; scripts/project-stage/rainbow_lot_layout.py checks them), no quarter pin on the tower on screen, the poster again. **R4b part B (1.72.267, DS v21-22 StageCity, Linear HAD-290):** the 808 buildings standing today within ~1 km (TLV GIS layer 513, the city's surveyed heights) and the Sde Dov plan's 21 lots with approved design plans + the linear park, from city.json (build_city_rainbow.py); the generic fill only as the fallback; a source line under the stage. **R4c (1.72.268, DS v23, Linear HAD-291):** the honest form of the time machine. Only 2 of 9 pages give a completion year, so no year-by-year view (a guessed year is not shown); instead the legend under the stage by each page's status (קיים היום 808 / בבנייה 2 / בשיווק 5 / בשלב ההיתר 2), group colours on the masses and pins, a chip shows its group alone and frames it with the building's own label; Einstein's "אכלוס צפוי 2030" from its page. Left for later, not blocking: clickable existing buildings (floors, year are already in city.json), more places |
| R5 | Rainbow interior at EcoCity level: our own Blender renders (360 cube maps per room, material variants), a viewer, rooms bar, plan, "view" to the real outside | **done 25.9 (1.72.269-271)** | DS v24 ApartmentTour, Linear HAD-292. Live: the example apartment's living room with an open kitchen, our own Cycles 360° (scripts/interior/rainbow_interior.py, CPU ~12 min at 4096), floor 25 (eye 98.8 m), the curved glass facing true west, through it the city's buildings (city.json), the coast and the sea; always "דירה לדוגמה" + illustration caption (no public floor plans). The card after the view and the map; the full-screen viewer (tour.js: 2048 first, then 4096; grab-speed drag, pinch/wheel zoom, arrows, Esc, focus back). **Part 2 (1.72.270, DS v25, Linear HAD-293):** floor 25 in the four directions (north, east, south, west) with the page's own words for each, a direction bar, the viewer opens on the side picked on the stage, planned projects named in a view's caption (north looks straight at Dimri Yama's mass, 101 m). Render fixes: the camera sees 60 km (a new camera saw 1 km: the sky showed as a false sea inland), the ground reaches 40 km, far land hazes, the sea is water. **Part 3 (1.72.271, DS v26-28, Linear HAD-294):** the tower's balcony bands as the stage draws them in every render (the living rooms again) and the balcony in the four directions, a second switch (בסלון · במרפסת); every balcony caption gives the record's limit (tower balconies ≤2 m, no wrap-around, design plan 5.2023) — the stage's form vs the permit is HAD-295 (verify, then an owner decision). Left as background renders for any turn, not blocking: noon light, more heights (10, 38). Not done on purpose: finish "variants" and a floor plan (the developer publishes neither; ours would be invented) |
| R6 **next** | Rainbow cinematic pass: a detailed tower, sun and soft shadows, atmosphere, the opening flight, first picture < 4 s on a mid Android | todo | hauzd-teardown.md (coming) |
| R7 | Rainbow in five languages (the stage, cards and texts on -en/-fr/-ru/-ar) | todo | recipe row 29. Found 25.9: the English page's title mixes Hebrew and runs 102 characters ("Rainbow Tel Aviv | Coastal Resort Living in Sde Dov, תל אביב יפו - מחירים, דירות"); the quarter's cards are Hebrew only |
| R8 | Rainbow deals and prices section from sourced data (deep research, company reports) | **partly done 25.9 (1.72.261)** | ProjectDeals is live with the seven deals the press tied to a floor. Left: the Tax Authority's full list for the project (nadlan.gov.il gave no stable page; find the block/parcel key), a price range chip, the table in five languages |
| S1 | The skill `project-page-factory` (the recipe, the data intake, the DS pieces, the runners, the checks) so a project is cloned in minutes | todo | after R3 proves the unit layer; a first version sooner |
| D1 | DUO (Somail): the same recipe, its own stage, the Somail quarter | todo | after S1 |
| P1 | The other flagship projects, one by one: Dimri Yama, Ashira, UTOPIA, Einstein Tower, H-Infinity, SIX-8 | todo | after D1. Found 25.9: Zohi's page holds its developer as "לוינשטין, מבנה ואלייד נדלן" without the gershayim (the quarter's card already spells it "נדל״ן") |
| H1 | Home page redesign, DS first: a premium hero (our own cinematic render, no stock), the 3D projects up front, the portal sections kept | todo | owner: "the hero image is not premium" |
| X1 | Small defects found on the way (Linear HAD-287, a checklist) | **Rainbow part done 25.9 (1.72.262-263)**; the rest waits for the fleet items | Done: Hebrew place names in the view and the area map (with the right-to-left plugin), chips and popups without emoji, one map per page (the surroundings band's static map hidden), the Sde Dov tour box readable, the phone progress, the poster at the stage's aspect. Left, picked up with their pages: Dimri Yama's title (P1), Aurelia's coordinates (P1), /earth/ 401 and the Somail tour (D1), catalog-plus's surroundings wording ("תכנית ל'", "find-place", permit numbers), repo hygiene. Found 25.9 with R4 and fixed in 1.72.265: the accessibility button sat on the WhatsApp pill on the English, French and Russian pages (it followed the site's locale, now the page's language). Noted, not changed: in its corner the button still covers 2-3 letters of the bottom lines on a phone (a slim edge tab would cover less; the corner is the owner's ruling) |

## Waiting for the owner
- Nothing open. (25.9: the owner ruled example apartments with directions, labelled, and the accessibility button to the bottom corner; both live in 1.72.261.)

## Done in this loop
- 25.9 night: R5 part 3 (1.72.271: the balcony and the tower's bands in the renders, the place switch, the balcony-size note;
  DS v26-28; HAD-294; the balcony form vs the permit opened as HAD-295). R5 is done (1.72.269-271).
- 25.9 night: R5 part 2 (1.72.270: the four directions of floor 25, the direction bar; the false sea fixed; DS v25; HAD-293).
- 25.9 night: R5 part 1 (1.72.269: the example apartment from the inside, our own Cycles 360° on floor 25 facing the sea;
  the card and the full-screen viewer; DS v24 ApartmentTour; Linear HAD-292).
- 25.9 night: R4c (1.72.268: the quarter's legend under the stage in place of a year-by-year time machine; DS v23;
  Linear HAD-291). R4 is done (1.72.264-268).
- 25.9 night: R4b part B (1.72.267: the real city around Rainbow from the city's buildings layer and the plan's lots; the
  source line under the stage; DS v21-22 StageCity; Linear HAD-290).
- 25.9 night: R4b part A (1.72.266: Rainbow's lot from the record, the tower at its true point, the boutique buildings by the
  design plan's rules, no pin on the tower, the poster again; DS v20 StageLot; Linear HAD-289).
- 25.9 night: R4 part 1 (1.72.264 the quarter inside Rainbow's stage; 1.72.265 pins never overlap, the accessibility corner by
  the page's language; DS v18-19; Linear HAD-288). A lesson: several uncached page loads in a row gave four 502s for
  about 20 seconds (~01:50); leave a pause between uncached runs against the live site.
- 25.9 night: X1's Rainbow part (1.72.262-263: Hebrew map names, no emoji, one map, the tour box, the phone progress, the poster; DS v17).
- 25.9 night: R3 (1.72.261: example apartments, ProjectDeals, the accessibility button in the corner; DS v15-16; Linear HAD-286).
- 25.9 night: R2 (1.72.260 the first fold, 1.72.259 the page top to the recipe; the page text passes 2-4 and the search and
  social fields made true; the deep research collected). The recipe's row 6 corrected to the owner's 29.8 order.
- 24.9 night: R1 (1.72.258 + page text + NIS/m² meta). Research in: hauzd-teardown.md (85 screens), tech-stack.md.
- 24.9: 1.72.255-256 Rainbow page top (stage, view, beam, rail) and the shore at 713 m; 1.72.257 "המלצות" and the count;
  EcoCity's /tour/ecocity/ taken off (404, folder moved out of the web root).
