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

## Runtime Display Rules

- Load `model-viewer` as an ES module with a `script_loader_tag` filter. A plain script tag breaks
  model-viewer 4.x because the browser sees `export` in a classic script.
- Use `reveal="auto"` and a poster image so the buyer sees the building without first clicking a
  blank frame.
- When the GLB `load` event fires, hide the procedural tower, facade, sea, runway and horizon
  layers completely. They are fallback layers only. If the GLB errors, show the fallback again.
- Start the camera close enough for apartment picking: narrow field of view, gentle auto-rotate,
  and a target near the occupied floors. Avoid fast spinning because it reads like a demo, not a
  sales showroom.
- Apartment selectors must read as apartment inventory before the user opens any side panel:
  use status-coded apartment cells/rectangles on the building wherever possible. Dots are only a
  fallback for very small geometry. Available, reserved, sold and recommended states are part of
  the model contract.

Unit JSON fields:

- `id`
- `title`
- `label`
- `floor`
- `rooms`
- `sqm`
- `dir`
- `status`
- `recommended`
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
- The `nadlan-model-viewer` script tag must render as `type="module"`. In WordPress this requires
  a `script_loader_tag` filter for that handle; `wp_script_add_data( $handle, 'type', 'module' )`
  alone is not a sufficient live gate on this site.
- In Chrome, `customElements.get('model-viewer')` must return a function before anyone claims that
  the GLB rail works.
- Use `reveal="auto"` and `loading="auto"` for near-top flagship showroom models, with a poster
  image so the stage is never blank while the GLB streams.
- Keep procedural/facade fallback visible until the model loads.
- If the model errors, do not leave a blank stage.
- Model hotspots must call the same selected-unit flow as facade/SVG clicks.
- Unit markers must be buyer-obvious without becoming text blobs on the model: use clean
  apartment cells/rectangles with 44px+ hit areas, status color, hover/focus tooltip on desktop,
  selected-card details on mobile, and optional recommended pulse.
- Those invisible hit areas must not block the primary product gesture. A tap on a unit marker
  selects it; a drag that starts on the same marker rotates the building and suppresses the
  accidental click at the end of the swipe.
- `recommended` is a CMS/business flag. It should identify units worth attention, not fake urgency.
- The lead payload must preserve the selected unit.
- Mapbox or Cesium environment views stay lazy and user-opened.

## Product Selector Standard

The apartment selector is the product hero, not a decoration.

1. The first visible order is intro, compact model, selected unit, CTA.
2. Availability is visible before copy: available, reserved and sold must have different marker
   colors.
3. Price may be official, estimated or hidden, but estimated values must say `אומדן` and
   `לא מחייב`.
4. On desktop, the selected-apartment card docks near the model. On mobile, it becomes a clear
   panel in the vertical flow.
5. Advanced tools such as sun, surroundings, Mapbox and Cesium are opened after the buyer selects
   a unit. Do not flood first view with every control.

## Selected Apartment Card Standard

The selected-apartment card is the buyer decision surface. It must not feel like a debug panel.

- Show buyer-facing tags from CMS data: recommended, availability/status, view and price-estimate
  context.
- Color the card status edge consistently with the marker status: available, reserved, sold.
- If the price is an estimate, the card must say it is an estimate and not binding.
- If the unit is reserved or sold, explain the next useful action without pretending it is available.
- The active marker should expose `aria-pressed="true"` so keyboard and assistive-tech users know
  which apartment is selected.
- Do not use internal words such as lead, funnel, CRM, supplier or monetization in public card copy.

## QA Gate

Before shipping a project:

- Confirm no blank stage without GLB.
- Confirm no blank stage with a broken GLB.
- Confirm GLB loads and has camera controls.
- Confirm the rendered model-viewer script tag includes `type="module"` and Chrome has no
  `Unexpected token 'export'` console error.
- Confirm at least one hotspot selects the matching unit.
- Confirm keyboard/focus access to unit selection remains available.
- Confirm mobile has no horizontal overflow and no nested gray scrollbars.
- Confirm source notes/disclaimers distinguish official data from illustrative/demo data.
- Confirm the page still has one H1 and the article body remains readable below the showroom.

## Apartment Cell Selector Standard

The buyer-facing selector must read as apartments on the building, not as abstract map pins.

The primary marker should be a facade-like cell:

- rectangular, aligned to the visible building/facade/model,
- status stripe: available green, reserved amber, sold grey,
- short label or floor/unit clue,
- optional recommended pulse only for owner-approved available units,
- hover/tap tooltip with floor, rooms, sqm, view and non-binding estimate,
- minimum 44px by 44px hit target on mobile.

Dots are permitted only as a fallback when no facade, floor plate, GLB hotspot or image geometry is
available. If the buyer cannot understand where the apartment sits in the building, the selector has
failed even if the click handler works.

Mobile rule: selected-apartment details must be a controlled sheet or inline card that stays visible
without shrinking the model scene. Never let a selected card collapse the 3D stage height or appear
off-screen.

## CMS Owner Rule

Do not make Classic Editor the long-term answer for finding showroom fields. It can be used as a
temporary owner comfort tool, but the durable standard is the plugin-owned
`בחירת דירות אינטראקטיבית` metabox, REST-writable project meta, and a plain owner manual. A field is
not considered usable until a non-technical owner can find it in the WordPress edit screen and a
buyer can see the rendered result on the public page.

The metabox must expose a plain unit builder above the raw `project_3d_units` JSON textarea. The
builder is the owner path for one-off edits: add or update a unit by id, floor, rooms, sqm, status,
view, estimate, plan URL and model hotspot vectors, then write the sanitized JSON back to the same
meta field. Raw JSON remains only for bulk import and developer/debug use.

The REST contract must match the metabox contract. Do not expose a field only in wp-admin if a
future project factory needs to write it. At minimum, REST-writable sanitized meta must include:
model/facade image, viewBox, floor height, ground elevation, average price estimate, price source
note, model type, GLB, USDZ, poster, video, tour, Cesium/3D Tiles seam, drawings JSON,
environment JSON, unit JSON and demo flag.

For one-shot project assembly, use the project showroom payload route instead of writing each field
manually. The canonical contract is:

- `GET /wp-json/nadlan/v1/project-showroom/<project_id>` to export the current payload.
- `POST /wp-json/nadlan/v1/project-showroom/<project_id>` with either flat fields or
  `{ "meta": { ... } }` to apply a project data file.
- The route must be authenticated and must require `current_user_can( 'edit_post', $project_id )`.
- The route must reuse the same sanitizers as the metabox and registered REST meta.
- Every project asset folder should have a generated `showroom-payload.json` built by
  `node scripts/build-project-showroom-payload.mjs <project-slug> --write`. This file is the
  single handoff from research/modeling into the CMS and must validate before WordPress import.
- Validate every payload with
  `node scripts/validate-project-showroom-payload.mjs --payload assets/projects/<slug>/showroom-payload.json`.
  The source of truth is `docs/templates/project-showroom-payload.schema.json`.
- Apply the payload with `scripts/import-project-showroom-payload.mjs` only after live healthcheck
  proves the plugin version and payload route marker are ready. The script must use environment
  variables for WordPress application-password auth and must not store secrets in the repo.
- After import, run `node scripts/qa-project-showroom-live.mjs --strict` against the public URL.
  A project is not factory-complete until healthcheck, public HTML, model-viewer module loading,
  hotspots, one H1, title/meta intent and payload API checks are green.

`project_3d_drawings_json` may be either a flat array of material items or an object with an
`items` array. `project_3d_environment_json` may be a flat array or a structured object with
`layers[].items[]`; the plugin must flatten it into safe buyer-facing cards and keep source labels.

## Countrywide Replication

For every future project, create a project asset folder containing:

- `source-notes.md`
- `model.glb`
- `model.usdz` if needed
- `poster.webp`
- `unit-map.json`
- `drawings.json`
- `environment.json`
- `showroom-payload.json`
- `qa.md`

The plugin should consume URLs and JSON only. Large raw modeling files should live outside the
plugin ZIP and outside the WordPress plugin repository unless explicitly approved.

