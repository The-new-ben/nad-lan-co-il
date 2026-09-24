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
- ChatGPT Pro deep research on Rainbow's floors and deals: https://chatgpt.com/c/6ab58178-54f8-83eb-848d-1bb86a034149
  (started 24.9.2026 ~22:45). When done, save it as `deep-research-rainbow.md` and use it in items R3 and R8.

## The board

| # | Item | State | Evidence / notes |
|---|---|---|---|
| R1 | Rainbow facts fixed on the page and the stage | **done 24.9 (1.72.258)** | the stage: tower in lot 111's NE corner (its official outline from the Tel Aviv plans layer), 39 floors, 3.75 m, pools on two boutique roofs, turned 10° like the lot, shore 713 m; view and beam start at the tower (32.10354, 34.78466); demo units never feed public numbers (the "82-210 מ״ר" is gone); the page text: writer's notes removed, 459 (480 approved), NIS/m² 81,782 per the developer's reports. Next inside R2/R4: the lot's full real layout (150 x 75 m, long N-S) |
| R2 | Rainbow page to the recipe: hero with the two CTAs and the building in the first fold, the answer paragraph (names, developer, place, status, mix, sourced prices, keywords), six facts, progress, one FAQ with one FAQPage schema, the notice after the lead and the disclaimers last | todo | recipe rows 3-8, 25, 28 |
| R3 | Rainbow apartments in the stage: floor + side arcs (3-5 per floor), the unit card (floor, side in words, rooms and m² only where sourced, the illustrative plan), `?unit=`, the cone and the view per apartment, the lead with the unit id. DS first: UnitPicker, UnitCard | todo | unit-layer §6; waits for the deep research for real layouts, starts with honest side-arcs labelled "חלוקה משוערת להמחשה" |
| R4 | Rainbow surroundings: the real Sde Dov quarter in the white-model style from the find-place data; our 11 projects clickable with a card and "what you see from Rainbow toward it"; facilities clickable | todo | worlds.md §9 |
| R5 | Rainbow interior at EcoCity level: our own Blender renders (360 cube maps per room, material variants), a viewer, rooms bar, plan, "view" to the real outside | todo | ecocity-cfg-teardown.md (coming), tech-stack.md |
| R6 | Rainbow cinematic pass: a detailed tower, sun and soft shadows, atmosphere, the opening flight, first picture < 4 s on a mid Android | todo | hauzd-teardown.md (coming) |
| R7 | Rainbow in five languages (the stage, cards and texts on -en/-fr/-ru/-ar) | todo | recipe row 29 |
| R8 | Rainbow deals and prices section from sourced data (deep research, company reports) | todo | recipe row 21 |
| S1 | The skill `project-page-factory` (the recipe, the data intake, the DS pieces, the runners, the checks) so a project is cloned in minutes | todo | after R3 proves the unit layer; a first version sooner |
| D1 | DUO (Somail): the same recipe, its own stage, the Somail quarter | todo | after S1 |
| P1 | The other flagship projects, one by one: Dimri Yama, Ashira, UTOPIA, Einstein Tower, H-Infinity, SIX-8 | todo | after D1 |
| H1 | Home page redesign, DS first: a premium hero (our own cinematic render, no stock), the 3D projects up front, the portal sections kept | todo | owner: "the hero image is not premium" |
| X1 | Small defects found on the way: map chips with emoji; Aurelia shows "חסרות קואורדינטות למפה"; /earth/ clickable layer 401; Somail placeholder pins; tours' wrong positions; H-Infinity "coming soon" in the Somail tour | todo | worlds.md §9, engine-journey.md |

## Waiting for the owner
- Rainbow apartments' directions: labelled example apartments with directions (a), types without a stated direction (b, the
  default until he says), or wait for real data (c). unit-layer §6.6.

## Done in this loop
- 24.9 night: R1 (1.72.258 + page text + NIS/m² meta). Research in: hauzd-teardown.md (85 screens), tech-stack.md.
- 24.9: 1.72.255-256 Rainbow page top (stage, view, beam, rail) and the shore at 713 m; 1.72.257 "המלצות" and the count;
  EcoCity's /tour/ecocity/ taken off (404, folder moved out of the web root).
