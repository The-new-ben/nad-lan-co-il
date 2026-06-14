# Skill: Project 3D Model Pipeline

Use this skill when creating or upgrading a `nadlan_project` page into a premium 3D showroom with
real model assets, clickable units, and a CMS-repeatable data contract.

## Goal

Turn developer/project material into a web-safe showroom:

1. A real GLB model for the building.
2. Optional USDZ for iOS AR.
3. A lightweight poster image.
4. Per-unit hotspots mapped into the model.
5. Floor plans, drawings, media, surroundings and pricing context attached through CMS fields.
6. A fallback procedural/facade experience when official model material is missing.

## Source Hierarchy

Use the highest trust source available:

1. Official developer BIM / Revit / SketchUp / OBJ / FBX / GLB.
2. Official elevation/facade drawings and floor plans.
3. Official marketing render with owner/developer permission.
4. Original illustrative model created from public facts and clearly marked as illustrative.

Never copy paid-source photos, paid transaction tables, or licensed marketing renders into public
assets without explicit permission.

## Massing Now, Swap Later

When official BIM is not available but the owner needs a working showroom demo:

1. Create an original low-poly massing model from public facts and clearly label it illustrative.
2. Keep scale intuitive: 1 model unit = approximately 1 meter, origin at building-base center, Y up.
3. Model the product structure, not a fantasy render: tower, podium, boutique blocks, amenity court,
   roof crown, floor rhythm and window bands.
4. Avoid flat stacked-box placeholders. Even prototype massing must show the architectural idea:
   spiral/stepped form when sourced, facade rhythm, podium/lobby, roof amenity hints, surroundings
   and a first-glance residential read.
5. Keep the first GLB lightweight. Target under 4 MB for a massing model.
6. Store demo units with `source_note` and non-binding price/availability copy.
7. When official BIM/developer GLB arrives, optimize it and replace `project_model_glb` while keeping
   the same origin/scale where possible. If origin/scale changes, regenerate `hotspot_position`,
   `hotspot_normal`, and `camera_orbit`.

This "massing now, swap later" path is valid for a contractor demo, but the public page must never
present it as the official architectural model.

## Modeling Pipeline

Recommended path for a real project model:

1. Import source material into Blender.
2. Clean the scene: remove people, fake logos, hidden geometry and oversized textures.
3. Name meaningful objects: tower, podium, balcony bands, amenity deck, surroundings.
4. Add empty markers or helper points for unit hotspots.
5. Export GLB for web.
6. Export USDZ only when iOS AR is required.
7. Create a poster image at the exact stage ratio.
8. Optimize before upload.

Recommended optimization commands:

```bash
gltf-transform inspect project.glb
gltf-transform optimize project.glb project.optimized.glb --compress draco --texture-compress webp
gltf-transform inspect project.optimized.glb
```

Target budgets:

- Prototype poster used before first load: under 80 KB when committed to the repo.
- Poster uploaded to media/CDN for richer official model: under 350 KB.
- GLB first massing version: under 4 MB.
- GLB first official export: under 8 MB if possible.
- Hero-grade GLB: under 15 MB only when the model quality justifies it.
- Texture sizes: prefer 1024 or 2048, avoid 4096 unless visually necessary.

## CMS Fields

Project fields:

- `project_model_glb`: optimized GLB URL.
- `project_model_usdz`: optional USDZ URL.
- `project_model_poster`: lightweight poster URL.
- `project_3d_image`: optional facade/elevation fallback image.
- `project_3d_drawings_json`: approved drawings and floor plans.
- `project_3d_environment_json`: surroundings, transport, schools, parks and source-aware context.
- `project_3d_video_url`: developer-approved video.
- `project_3d_tour_url`: interior or apartment tour.
- `project_3d_cesium_tiles_url`: future approved 3D Tiles/environment layer.

Unit JSON fields:

- `id`
- `title`
- `floor`
- `rooms`
- `sqm`
- `dir`
- `status`
- `price` or `price_estimate`
- `price_note`
- `points` for SVG/facade fallback polygons
- `hotspot_position` for model-viewer hotspots
- `hotspot_normal` for model-viewer hotspots
- `camera_orbit` optional per-unit camera orbit
- `plan_url`
- `interior_url`
- `tour_url`
- `view_note`
- `source_note`

Media and tour rules:

- Create the fields even when no official media exists yet; empty slots are an honest CMS contract.
- Use only owner-approved `https://` URLs for video, tour, Cesium/3D Tiles, interior media and unit tours.
- Do not fill the slots with copied developer assets, stock interiors, AI-generated fake interiors, or
  unlicensed screenshots.
- Keep Mapbox/Cesium/3D Tiles lazy and user-opened. The project page must not spend paid map/tiles
  quota before a buyer requests the view layer.
- Each flagship asset folder should include `material-intake-template.json` mapping official
  model/video/tour/drawings/unit/environment materials to CMS fields, accepted formats, current
  status and public-use policy. This is the project-manager handoff document and the countrywide
  replication checklist.
- Each flagship asset folder should include `view-layer-config.json` for Mapbox-now / Cesium-ready
  views: project center, provider policy, cost controls, unit altitude/bearing records, overlay
  policy and QA requirements. The default state remains building-first; map/tiles are inspection
  tools opened by the buyer.

## Price Context

Buyers expect price context inside a showroom, but it must not turn a prototype into an invented
offer:

- Prefer project-level `project_3d_avg_price_per_sqm` plus `project_3d_price_source_note` when
  official apartment inventory is missing. The runtime can compute a non-binding unit estimate from
  sqm without claiming availability.
- Use per-unit `price_estimate` only when the owner approves the source and the visible note still
  says it is not an offer or commitment.
- Do not paste paid transaction rows, licensed tables, or exact availability into public CMS fields
  unless the owner has explicitly approved the source/license.
- Exact `price` is reserved for official developer inventory or a formally approved source.

## Hotspot Capture

For `<model-viewer>`, each unit hotspot needs model coordinates:

```json
{
  "id": "unit-2402",
  "title": "דירת 4 חדרים, קומה 24",
  "floor": 24,
  "hotspot_position": "1.2 24.8 -0.6",
  "hotspot_normal": "0 0 1",
  "camera_orbit": "35deg 66deg auto"
}
```

Capture hotspot points from Blender helpers, a model-viewer editor/export workflow, or a project
model annotation script. Store only coordinates, not private source files.

## Runtime Standard

- Render `<model-viewer>` only when `project_model_glb` exists.
- Keep procedural/facade fallback visible until the model loads.
- If the model errors, do not leave a blank stage.
- Model hotspots must call the same selected-unit flow as facade/SVG clicks.
- The lead payload must preserve the selected unit.
- Mapbox or Cesium environment views stay lazy and user-opened.
- Empty video/tour/Cesium slots should hide their controls or show a clear "material pending" state,
  never a broken button.

## QA Gate

Before shipping a project:

- Confirm no blank stage without GLB.
- Confirm no blank stage with a broken GLB.
- Confirm GLB loads and has camera controls.
- Confirm at least one hotspot selects the matching unit.
- Confirm keyboard/focus access to unit selection remains available.
- Confirm mobile has no horizontal overflow and no nested gray scrollbars.
- Confirm source notes/disclaimers distinguish official data from illustrative/demo data.
- Confirm video/tour/Cesium/unit-media URLs are empty or valid approved HTTPS links; malformed URLs fail.
- Confirm `material-intake-template.json` exists and records the official replacement path before
  calling a project clone-ready.
- Confirm `view-layer-config.json` exists, is user-opened/lazy for Mapbox and Cesium, and gives every
  unit a numeric altitude and bearing for view-from-apartment QA.
- Before live CMS wire-in, run the local model preview browser gate:
  `node scripts/check-rainbow-prototype-preview.mjs` (or the project-specific equivalent). It must
  prove the GLB loads at 1440px and 390px, hotspots exist, hotspot tap/click changes the unit
  readout, tap targets are at least 44px, drawings/environment/media slots render from the project
  JSON, Mapbox/Cesium view policy remains user-opened/lazy, and screenshots are captured.
- Confirm the local model preview screenshot shows `loaded:true` / actual GLB visible, not only the
  poster image.
- Confirm the page still has one H1 and the article body remains readable below the showroom.
- Confirm the page assembly/SEO gate passes before wiring the public GLB: transaction-led title,
  price-aware non-binding meta description, visible buyer phrasing, FAQ/schema meta and no raw
  code leak. A model is not enough if the page shell still reads unfinished.
- For Rainbow-style projects, the final proof should be one combined command such as
  `python scripts/check-rainbow-finish-line.py`: healthcheck prerequisites, page assembly,
  GLB readiness and real-browser DOM must pass together.

## Countrywide Replication

For every future project, create the asset folder with the scaffold helper first:

```powershell
python scripts\scaffold-project-showroom.py --project-slug <latin-slug> --project-name "<Project Name>" --post-id <project-id> --city "<city>" --lat <lat> --lng <lng>
```

That command creates the day-zero contract. It is intentionally not public-ready until model assets,
unit data, source notes and QA are filled. Every future project asset folder must then contain:

- `source-notes.md`
- `model.glb`
- `model.usdz` if needed
- `poster.png`
- `unit-map.json`
- `drawings.json`
- `environment.json`
- `material-intake-template.json`
- `view-layer-config.json`
- `qa.md`

The plugin should consume URLs and JSON only. Large raw modeling files should live outside the
plugin ZIP and outside the WordPress plugin repository unless explicitly approved.
