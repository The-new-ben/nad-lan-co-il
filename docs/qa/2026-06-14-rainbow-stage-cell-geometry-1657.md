# Rainbow v1.65.7 Stage-Cell Geometry QA

## Purpose

The owner rejected detached dots and floating markers. The buyer must feel that apartments are
embedded in the building/facade, not hovering in the air. This slice adds authorable stage-cell
geometry to `project_3d_units` so each apartment can render as a facade-like clickable rectangle.

## Visual Basis

The bundled facade asset is original concept art, not a copied developer render. It was steered by
public descriptions of Rainbow as a coastal Sde Dov resort project with a sculptural or spiral tower
and six boutique buildings:

- `https://rainbowtlv.com/`
- `https://sdedov.co.il/project/rainbow/`
- `https://www.israel-canada.co.il/projects/tel-aviv/rainbow`
- `https://ascendisraelproperties.com/rainbow.html`

## What Changed

- Preserved `stage_x` and `stage_w` in the unit sanitizer.
- Added `stage_x` and `stage_w` fields to the Hebrew unit builder in the `בחירת דירות
  אינטראקטיבית` metabox.
- Added a `points` field to that same builder so the owner can place true facade/elevation
  apartment polygons without hand-editing only the raw JSON.
- Added a one-shot Rainbow `v1657` showroom seed. If the live Rainbow post already ran the older
  `v1635` seed before facade `points` existed, this patch imports the updated unit-map only when
  the current units do not already contain facade points.
- Tightened the one-shot showroom payload contract so `points`, `stage_x` and `stage_w` are
  required per unit. The importer now refuses live writes until the site is at 1.65.7 and the
  facade-cell health markers are present.
- Tightened the live and visual QA scripts so they assert the facade-cell runtime and DOM
  (`.nlp3d-facade-cell` / `.nlp3d-facade-hit`) instead of passing on the old stage-pick fallback
  alone.
- Updated the stage renderer so authored `stage_x` controls the horizontal cell position.
- Updated cell width with `stage_w`, while keeping a minimum mobile-friendly hit size.
- Promoted facade/elevation `points` polygons to the primary selector when they exist.
- Keeps the stage-cell layer as a fallback only when no facade polygons are available.
- Enlarged the Rainbow prototype polygons from thin highlight bands into apartment-sized cells,
  with stronger availability colour, selected-state glow and label contrast.
- Added buyer-readable labels to the embedded facade cells, generated from the same CMS unit data
  (`floor` + `rooms`) and synced with the selected apartment state.
- Corrected the public mental model: the first visible path now says the buyer chooses an apartment
  on the facade. The 360 view remains secondary until a real apartment-level BIM/GLB exists.
- Added an admin facade-point helper in the project metabox. The operator can click four corners on
  the configured facade image and copy the generated polygon into the existing `points` field.
- When facade polygons exist and a placeholder GLB also loads, the facade selector stays primary
  and the GLB is hidden to avoid the "two towers / floating cells" visual collision.
- Changed the drag rule: clicking an apartment cell selects the unit; dragging empty building
  surface rotates the scene.
- Added Rainbow prototype `points`, `stage_x` and `stage_w` values to the source payload files.
- Replaced the darker generic facade demo with an original white/glass coastal tower concept that
  reads closer to Rainbow's public "spiral/sculptural tower + boutique buildings" positioning,
  while staying clearly illustrative and non-official.
- Added an architectural window/apartment-band layer to that original facade asset so the
  clickable cells sit on a believable tower skin instead of floating over a smooth illustration.

## Local Preview Proof

Preview file:
`docs/qa/previews/rainbow-facade-selector-1657.html`

Screenshots:

- `docs/qa/screenshots/rainbow-facade-selector-1657/chrome-desktop-1440-selected.png`
- `docs/qa/screenshots/rainbow-facade-selector-1657/chrome-mobile-390-selected.png`
- `docs/qa/screenshots/rainbow-facade-selector-1657/chrome-after-click-viewport.png`
- `docs/qa/screenshots/rainbow-facade-selector-1657/chrome-desktop-1440-new-facade.png`
- `docs/qa/screenshots/rainbow-facade-selector-1657/chrome-desktop-1440-architectural-facade.png`

Chrome interaction proof on the local preview:

- `cells = 6`
- selected before click: `unit-24-nw`
- clicked facade cell: `unit-31-se`
- selected after click: `unit-31-se`
- selected card after click: `דירת 5 חדרים, קומה 31`, `156 מ"ר`, `5 חד׳`
- `mojibake = false`
- `horizontal overflow = false` in the Chrome extension desktop viewport

## Chrome Gate

Run on the live Rainbow page after deploy:

1. Desktop 1440px: apartment selectors look like embedded apartment-sized facade/elevation cells,
   not dots, floating squares or thin decorative lines.
2. Mobile 390px: every cell remains easy to tap and does not create horizontal overflow.
   The visual cell must not collapse into a decorative line, and the transparent hit target must
   remain at least 44px by 44px.
3. Click/tap a cell once: the selected-apartment card updates with the correct unit.
4. Public copy leads with facade apartment selection. It must not start with "spin the model" or
   promise true 3D apartment picking before a per-apartment BIM/GLB exists.
5. Drag empty model surface: the building rotates.
6. Drag/click on a cell: it does not feel jammed; selection wins predictably.
7. Recommended unit pulses subtly, but no fake urgency copy appears.
8. Console has no page errors.
9. Healthcheck reports version `1.65.7`, `project_3d.stage_cell_geometry_v1657 = true` and
   `project_3d.facade_polygon_primary_v1657 = true`.
10. Healthcheck also reports `project_3d.facade_points_builder_v1657 = true` and
   `project_3d.facade_hides_placeholder_glb_v1657 = true`.
11. Healthcheck reports `project_3d.facade_cell_labels_v1657 = true`.
12. Healthcheck reports `project_3d.facade_point_helper_v1657 = true`.
13. Healthcheck reports `project_page_assembly.rainbow_showroom_v1657 = true` and
    `project_page_assembly.rainbow_units_have_facade_points = true`.
14. `node scripts/validate-project-showroom-payload.mjs --payload assets/projects/rainbow-tel-aviv/showroom-payload.json`
    reports `units_with_points = 6`.

## Factory Payload Gate

Local factory validation:

```powershell
node --check scripts/build-project-showroom-payload.mjs
node --check scripts/validate-project-showroom-payload.mjs
node --check scripts/import-project-showroom-payload.mjs
node --check scripts/qa-project-showroom-visual.mjs
node scripts/build-project-showroom-payload.mjs rainbow-tel-aviv > plugin-dist/_showroom-payload-check.json
node scripts/validate-project-showroom-payload.mjs --payload plugin-dist/_showroom-payload-check.json
node scripts/validate-project-showroom-payload.mjs --payload assets/projects/rainbow-tel-aviv/showroom-payload.json
```

The visual QA script now fails a deployed project if facade cells are only thin decorative lines,
if their transparent hit boxes fall below the 44px tap-target gate, or if public copy still leads
with spinning/3D wording before apartment-level BIM exists.

Both generated and committed payloads passed with `units = 6`, `units_with_points = 6`,
`drawings = 6` and no validation errors.

Live import dry-run on 2026-06-14 correctly refused to write because production was still
`1.65.5`, below the `1.65.7` facade-cell contract:

```json
{
  "live_version": "1.65.5",
  "required_version": "1.65.7",
  "version_ready": false,
  "route_marker_ready": true,
  "facade_cell_marker_ready": false
}
```

## Honest Boundary

This is a CMS-ready facade/stage-cell bridge. It is not yet a true BIM-level per-apartment mesh.
For exact geometry on the physical tower, the project needs one of:

- official BIM/GLB with separate apartment meshes,
- an official facade/elevation drawing traced into per-unit polygons,
- or a Blender-generated model where each apartment is exported as a named selectable mesh.

Until one of those exists, every public label must remain approximate and demonstrative.
