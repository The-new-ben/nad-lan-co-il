# Rainbow Prototype Model QA

## Generated Artifacts

- `model.glb`: original lightweight architectural massing of the Rainbow tower, boutique ring and central amenity court.
- `poster.png`: lightweight poster for `<model-viewer>` before the GLB reveals.
- `unit-map.json`: demo unit records with model-viewer hotspot coordinates.
- `project-meta-example.json`: copy/paste map for the CMS fields added in v1.63.0.
- `plans/*.svg`: original schematic unit/site plans for the prototype plan overlay.
- `drawings.json`: prototype drawing map plus slots for official elevation/floor/site drawings.
- `environment.json`: surroundings starter data to be replaced by the map/POI layer.

## Local Validation

Run:

```powershell
python scripts/generate-rainbow-prototype-model.py
node -e "const fs=require('fs'); const b=fs.readFileSync('assets/projects/rainbow-tel-aviv/model.glb'); console.log(b.subarray(0,4).toString(), b.readUInt32LE(4), b.readUInt32LE(8), b.length)"
```

Expected:

- Magic: `glTF`
- Version: `2`
- File size under 8 MB.
- `project_3d_units` JSON has `hotspot_position`, `hotspot_normal`, `camera_orbit` and `plan` for each demo unit.

## Browser Gate After v1.63.0 Is Installed

1. Upload `model.glb` and `poster.png` to WordPress Media or serve from GitHub raw/CDN.
2. Set `project_model_glb`, `project_model_poster`, `project_3d_units`, `project_3d_drawings_json` and `project_3d_environment_json` from `project-meta-example.json`.
3. Open `/projects/rainbow-tel-aviv/`.
4. Confirm the procedural fallback remains visible until the model loads.
5. Confirm the GLB becomes the stage, drag rotates the building, and each hotspot selects the matching unit.
6. Confirm the plan overlay opens the relevant schematic plan for each selected unit.
7. Confirm lead/compare/map actions still carry the selected unit.
8. Confirm mobile has no horizontal overflow and no nested gray scrollbars.

## Honest Boundary

This is a contractor-demo model package. It proves the CMS rail and interaction pattern; it is not a substitute for official developer BIM, official drawings, live inventory or binding price data.
