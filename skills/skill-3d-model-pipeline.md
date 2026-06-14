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
4. Keep the first GLB lightweight. Target under 4 MB for a massing model.
5. Store demo units with `source_note` and non-binding price/availability copy.
6. When official BIM/developer GLB arrives, optimize it and replace `project_model_glb` while keeping
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

- Poster: under 350 KB.
- GLB first version: under 8 MB if possible.
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

## QA Gate

Before shipping a project:

- Confirm no blank stage without GLB.
- Confirm no blank stage with a broken GLB.
- Confirm GLB loads and has camera controls.
- Confirm at least one hotspot selects the matching unit.
- Confirm keyboard/focus access to unit selection remains available.
- Confirm mobile has no horizontal overflow and no nested gray scrollbars.
- Confirm source notes/disclaimers distinguish official data from illustrative/demo data.
- Confirm the page still has one H1 and the article body remains readable below the showroom.
- Confirm the page assembly/SEO gate passes before wiring the public GLB: transaction-led title,
  price-aware non-binding meta description, visible buyer phrasing, FAQ/schema meta and no raw
  code leak. A model is not enough if the page shell still reads unfinished.

## Countrywide Replication

For every future project, create a project asset folder containing:

- `source-notes.md`
- `model.glb`
- `model.usdz` if needed
- `poster.webp`
- `unit-map.json`
- `drawings.json`
- `environment.json`
- `qa.md`

The plugin should consume URLs and JSON only. Large raw modeling files should live outside the
plugin ZIP and outside the WordPress plugin repository unless explicitly approved.
