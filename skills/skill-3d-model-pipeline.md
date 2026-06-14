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
  status-colored dots with 44px+ invisible hit areas, hover/focus tooltip on desktop, selected-card
  details on mobile, and optional recommended pulse.
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
- `qa.md`

The plugin should consume URLs and JSON only. Large raw modeling files should live outside the
plugin ZIP and outside the WordPress plugin repository unless explicitly approved.

