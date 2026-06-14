# Rainbow Tel Aviv Prototype Model Source Notes

This folder is an **illustrative prototype package** for the approved v1.63.0 model-viewer rail.
It is not official Rainbow BIM, not an official sale plan and not live inventory.

## Public Facts Used

- Official/marketing sources describe Rainbow as a Sde Dov coastal project by Israel Canada with six boutique buildings, a spiral / spiral-like residential tower, lagoon/resort positioning and coastal views.
- Developer/architect sources describe 6 boutique buildings and a 42-story spiral-designed tower; press/planning-style sources describe a 40-story tower, 6 additional 8-floor buildings and 459 units. The public page must keep that truth-first discrepancy disclosure.
- Sde Dov/Rainbow public materials mention pools, spa, fitness, cafe/workspaces, sea proximity and resort-style positioning.
- For the prototype only, `project_3d_avg_price_per_sqm` uses a public Madlan-style average of 76,000 NIS per sqm as an indicative calculation basis. It is not official stock, not an offer and not a commitment.

## Sources To Recheck Before Public Claims

- https://rainbow-telaviv.com/
- https://www.blk.co.il/rainbow
- https://www.israel-canada.co.il/projects/tel-aviv/rainbow
- https://sdedov.co.il/project/rainbow/
- https://sdedov.co.il/projects/
- https://sdedov.co.il/faq/
- https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx
- https://www.gov.il/he/pages/sdedov-pr-22072020
- https://timeout.co.il/%D7%A8%D7%95%D7%91%D7%A2-%D7%A9%D7%93%D7%94-%D7%93%D7%91-%D7%A4%D7%90%D7%A8%D7%A7%D7%99%D7%9D/
- https://www.madlan.co.il/projects/%D7%97%D7%9C%D7%A7%D7%94_15_%D7%A9%D7%93%D7%94_%D7%93%D7%91_%D7%AA%D7%9C_%D7%90%D7%91%D7%99%D7%91
- https://en.globes.co.il/en/article-eyal-waldman-buys-sde-dov-apartments-for-nis-50m-1001483936

## Environment Layer Sources

- Sde Dov information site project index: names the marketed projects used in
  `environment.json` (`Rainbow`, `DIMRI YAMA`, `GINDI VOGUE`, `ASHIRA BY AVISROR`,
  `FIRST BY HAGAG`, `זוהי`, `UTOPIA`).
- Tel Aviv municipality Sde Dov page: district scale, master-plan status, parks, transport,
  commerce/employment and public-services framing.
- Gov.il planning announcement: 16,000 homes and district-scale public/commercial/employment
  program.
- Time Out Tel Aviv parks report: public report on park design-plan approval for the coastal,
  runway and linear parks.

Do not turn nearby project names into exact map pins until their coordinates are verified from a
trusted map/source.

## Public Safety

- Label this model as illustrative until official developer material replaces it.
- The `plans/*.svg` files are original schematic showroom aids, not official sale plans.
- Do not present the demo units as available stock.
- Do not present exact prices unless the owner approves a public or licensed source.
- Any public estimate must carry the visible non-binding source note in `project_3d_price_source_note`.
- Keep `project_3d_video_url`, `project_3d_tour_url`, `project_3d_cesium_tiles_url`,
  and unit-level `interior_url`/`tour_url` empty until the owner or developer supplies
  approved material. Do not use fake tours, copied developer media, or stock interiors.
- Replace `project_model_glb` with an official BIM/GLB when Israel Canada or the project manager supplies one.

## Prototype Design Basis

- Tower massing: original 42-level spiral-inspired stack, based on public descriptions of a spiral-designed Rainbow tower. It is not traced from any render.
- Boutique ring: six 8-floor blocks around a central resort court, based on the public complex description.
- Resort layer: lagoon/pool court, roof amenity hints, landscape markers, coastal strip, promenade and park ribbons are schematic cues only.
- Context masses: low surrounding silhouettes suggest the future Sde Dov district scale, but are not exact neighboring project pins or approved 3D city data.
- Facade cues: champagne ribs and highlighted demo-unit bands are interaction/readability aids for the prototype spinner, not official sale elevations.
- No faces, no copied stock, no copied developer images, no official inventory claims.
