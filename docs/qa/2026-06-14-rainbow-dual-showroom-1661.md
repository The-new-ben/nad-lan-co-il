# Rainbow v1.66.1 Dual Showroom Selector

## Goal

Keep the Rainbow GLB as the premium rotating showroom object, and add a static facade/elevation
selector beside it so apartment selection happens on visible apartment cells embedded in the
building face, not on floating dots.

## Honest Boundary

True 360-degree rotation with every apartment clickable on every side requires an official
apartment-level BIM/GLB where each unit is its own mesh or selection surface. The current Rainbow
model is a prototype/massing model, so the honest production architecture is:

- GLB/model-viewer: emotional premium 3D object, rotation and context.
- Facade/elevation selector: precise buyer apartment picking with status colors and selected card.

This matches the researched apartment-selector pattern from Parallel Select, DIGBY, Zillow floor
plans and model-viewer hotspot guidance.

## Code Changes

- `project-3d.php`
  - Creates the facade selector even when `<model-viewer>` exists.
  - Adds `is-dual-showroom` when a GLB is present and `is-facade-select` when no GLB is present.
  - Uses `stage_x`, `stage_y`, `stage_w`, and `stage_h` for facade cell placement.
  - Keeps model-viewer native drag controls from fighting the facade-cell click surface.
  - Adds health flags:
    - `dual_showroom_v1661`
    - `embedded_selector_with_glb_v1661`
    - `stage_xywh_fields_v1661`

- `scripts/qa-project-showroom-visual.mjs`
  - Counts `.nlp3d-cell` apartment cells as primary picks.
  - Fails when a model exists but embedded facade cells are missing.
  - Checks that clicking a visible cell marks a selected unit.

## Manual QA Gate

Run after deploying the plugin:

```bash
curl -s https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck
```

Expected:

- `version` is `1.66.1`.
- `project_3d.model_viewer_ready` is `true`.
- `project_3d.dual_showroom_v1661` is `true`.
- `project_3d.embedded_selector_with_glb_v1661` is `true`.
- `project_3d.stage_xywh_fields_v1661` is `true`.

Then run:

```bash
node scripts/qa-project-showroom-visual.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv --out docs/qa/screenshots/rainbow-dual-showroom-1661 --strict
```

Pass criteria:

- Desktop, tablet and mobile show both the GLB/model and apartment cells.
- The apartment cells sit on the facade/elevation selector, not floating in empty space.
- A clicked available cell becomes selected and opens/updates the selected-apartment card.
- No horizontal overflow.
- One visible H1.
- No console/page errors.
- No public copy leaks internal terms.

