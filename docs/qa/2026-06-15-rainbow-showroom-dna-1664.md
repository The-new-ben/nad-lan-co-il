# Rainbow Showroom DNA v1.66.4 QA

## Scope

This slice keeps the rotating GLB/model-viewer rail and makes the adjacent fixed facade/elevation
the primary apartment selector. It does not change payments, lead routing, schema generation, or
the admin metabox contract.

## Product Decision

- GLB/model-viewer = context, rotation, sun/environment, premium impression.
- Fixed facade/elevation = apartment picking, status, price estimate, tours, contact action.
- True 360-degree apartment picking is deferred until the developer supplies a GLB/BIM where
  individual apartments are real meshes with IDs.

## Research Anchors

- Zillow Interactive Floor Plans: https://www.zillow.com/3d-home/floor-plans/  
  Lesson: buyers understand spaces better when tours and selectable plan positions are connected.
- Matterport on Homes.com: https://www.homes.com/solutions/matterport  
  Lesson: the tour/floor-plan layer should be an explorable sales surface, not just a media link.
- model-viewer annotations: https://modelviewer.dev/examples/annotations  
  Lesson: hotspots are supported, but meaningful apartment picking requires real model positions.
- Baymard product thumbnails: https://baymard.com/blog/always-use-thumbnails-additional-images  
  Lesson: anonymous dots are weak selectors; users need richer visual targets and labels.
- Zillow next-generation 3D tours: https://zillow.mediaroom.com/2021-02-17-Zillow-Launches-Next-Generation-3D-Tours  
  Lesson: the best UX feels like product shopping: view, choose, compare, then act.

## Changed

- Added `nadlan_p3d_showroom_dna_v1664_css()` as a final scoped override.
- Added informative facade cell labels: unit/line, floor, rooms and area.
- Added a dismiss button for the selected-apartment card; selecting a new unit reopens it.
- Added data-driven context pins from `project_3d_environment_json`.
- Added a lightweight sun arc visual inside the showroom stage.
- Added `rainbow-showroom-hero-v1664.jpg` as the Rainbow poster/social image.
- Added a one-shot poster/social seed marked by `project_page_assembly.rainbow_showroom_v1664`.
- Added health markers:
  - `project_3d.showroom_dna_v1664`
  - `project_3d.facade_picker_side_by_side_v1664`
  - `project_3d.stage_card_dismiss_v1664`
  - `project_3d.context_pins_v1664`
  - `project_3d.poster_social_v1664`

## Local Gate

- PASS: PHP 8.3.31 installed via winget and run from
  `C:\Users\pro\AppData\Local\Microsoft\WinGet\Packages\PHP.PHP.8.3_Microsoft.Winget.Source_8wekyb3d8bbwe\php.exe`.
- PASS: `php -l` on changed PHP files:
  - `plugins/nadlan-config/nadlan-config.php`
  - `plugins/nadlan-config/inc/project-3d.php`
  - `plugins/nadlan-config/inc/project-page-assembly.php`
  - `plugins/nadlan-config/inc/health.php`
- PASS: `node --check` on extracted `nadlan-p3d` inline JavaScript.
- PASS: `node scripts/validate-project-showroom-payload.mjs --payload assets/projects/rainbow-tel-aviv/showroom-payload.json`
  returned 17 meta fields, 6 units, 6 drawings, and zero errors.
- PASS: `python scripts/build-plugin-zip.py 1.66.4`.
- PASS: `python scripts/verify-plugin-release.py 1.66.4`.
- PASS: ZIP paths are rooted at `nadlan-config/` with zero backslashes.
- PASS: `node scripts/qa-project-factory-smoke.mjs` created, built, validated, checked, and
  cleaned up a temporary project showroom folder. Result: 5 passed, 0 failed,
  `factory_ready=true`.

## Live Gate After Deploy

1. Pull/sync server Git to the merge commit.
2. Update NadLan Config to 1.66.4.
3. Clear UPress cache.
4. Check `/wp-json/nadlan/v1/healthcheck`:
   - `version` is `1.66.4`.
   - `project_3d.showroom_dna_v1664` is `true`.
   - `project_page_assembly.rainbow_showroom_v1664` is `true`.
5. Hard refresh `/projects/rainbow-tel-aviv/`.
6. Chrome screenshots at 1440, 768, 390:
   - model and facade are close together;
   - facade cells are visible and informative;
   - click on available cell opens card;
   - close button hides card;
   - selecting another cell reopens card;
   - no horizontal overflow;
   - headings are centered above paragraph text;
   - no public words such as funnel, CRM, lead panel, or paid placement.

## Asset Note

The new poster is an original generated showroom concept image. It is an illustrative marketing
poster, not official BIM, not a real photograph, and not an official developer render.
