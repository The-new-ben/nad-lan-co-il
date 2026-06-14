# Rainbow Prototype Model QA

## Generated Artifacts

- `model.glb`: original lightweight architectural massing of the Rainbow tower, boutique ring and central amenity court.
- `poster.png`: lightweight poster for `<model-viewer>` before the GLB reveals.
- `unit-map.json`: demo unit records with model-viewer hotspot coordinates.
- `project-meta-example.json`: CMS payload map for the model fields in v1.63.0 and the REST unit
  write gate added in the follow-up v1.63.2 stack.
- `plans/*.svg`: original schematic unit/site plans for the prototype plan overlay.
- `drawings.json`: prototype drawing map plus slots for official elevation/floor/site drawings.
- `environment.json`: surroundings starter data to be replaced by the map/POI layer.
- `material-intake-template.json`: contractor/developer handoff checklist mapping each official
  material to its CMS field, accepted formats and public-use policy.
- `view-layer-config.json`: Mapbox-now / Cesium-ready view-from-apartment contract with
  camera formulas, per-unit altitude/bearing, overlays and cost controls.
- Media/tour slots: `project_3d_video_url`, `project_3d_tour_url`,
  `project_3d_cesium_tiles_url`, and per-unit `interior_url`/`tour_url` are present
  but intentionally blank until official or owner-approved material is supplied.

## Local Validation

Run:

```powershell
python scripts/generate-rainbow-prototype-model.py
node -e "const fs=require('fs'); const b=fs.readFileSync('assets/projects/rainbow-tel-aviv/model.glb'); console.log(b.subarray(0,4).toString(), b.readUInt32LE(4), b.readUInt32LE(8), b.length)"
```

Expected:

- Magic: `glTF`
- Version: `2`
- `model.glb` under 4 MB for the prototype massing.
- `poster.png` under 80 KB for a repo-committed lightweight poster.
- `project_3d_units` JSON has `hotspot_position`, `hotspot_normal`, `camera_orbit` and `plan` for each demo unit.
- Each unit has empty `interior_url` and `tour_url` keys so the CMS contract is ready
  for approved unit media without changing the data shape later.
- `material-intake-template.json` lists at least eight handoff slots and keeps prototype material
  separate from official/developer-approved material.
- `view-layer-config.json` keeps the default state building-first, defines user-opened map/tiles
  behavior, and gives each unit a derived altitude and bearing for view-from-apartment QA.

## Browser Gate After The Full v1.63.4 Stack Is Installed

1. Merge/deploy the full stack: v1.63.1 tap targets, v1.63.2 unit REST wiring,
   v1.63.3 contact-rail containment and v1.63.4 page assembly/SEO.
2. Pull/sync the UPress server Git copy, update/upload the plugin, clear cache and verify healthcheck.
3. Upload `model.glb` and `poster.png` to WordPress Media or serve from GitHub raw/CDN.
4. Set `project_model_glb`, `project_model_poster`, `project_3d_units`, `project_3d_drawings_json` and `project_3d_environment_json` from `project-meta-example.json`.
5. Open `/projects/rainbow-tel-aviv/`.
6. Confirm the procedural fallback remains visible until the model loads.
7. Confirm the GLB becomes the stage, drag rotates the building, and each hotspot selects the matching unit.
8. Confirm the plan overlay opens the relevant schematic plan for each selected unit.
9. Confirm lead/compare/map actions still carry the selected unit.
10. Confirm mobile has no horizontal overflow, no nested gray scrollbars, and no showroom tap target below 44px.

## Honest Boundary

This is a contractor-demo model package. It proves the CMS rail and interaction pattern; it is not a substitute for official developer BIM, official drawings, live inventory or binding price data.
