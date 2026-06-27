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

When official material is still missing, a generated bitmap facade is allowed as a prototype only
when it is original, high quality, and explicitly labeled as illustrative in the CMS. It must be
stored in the project asset folder and wired through `project_3d_facade_images`, so the contractor
can replace only the URL later. Do not ship CSS/SVG grids or abstract rectangles as the facade.

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
  layers completely. They are legacy/prototype layers only, not silent recovery layers.
- No silent showroom fallbacks: if the GLB, facade image, tour, drawing or other showroom asset
  fails, show a visible failure state and log the defect. Do not silently reload the old tower,
  old facade or fake material as a substitute.
- If the GLB is a massing/prototype model and does not contain apartment-level meshes, do not place
  free-floating dots around it and pretend those are apartments. Keep the GLB as the premium
  rotating showroom object, and place a locked facade/elevation selector beside it. The facade
  selector is the precise apartment-picking surface until official BIM/GLB unit geometry exists.
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

Interior fields are part of the product contract, not optional decoration. A selected apartment
should be able to open its floor plan, interior render or 360 walkthrough when the asset exists.
For pre-construction projects without official interiors, generated prototype media is acceptable
only when clearly labeled as illustrative and replaceable.

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
- Keep a poster or explicit loading state visible until the model loads.
- If the model errors, show a clear visible model-error state. Do not resurrect the procedural
  tower or legacy facade as a hidden fallback.
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
6. Interior tour is the next buyer step after the selected-apartment card. Follow the
   Homes.com/Matterport pattern: floor plan, room media, 360 or walkthrough, dimensions, then CTA.

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

Initialize that folder with:

```bash
node scripts/init-project-showroom.mjs <project-slug> --post-id <post-id> --title "Project Name"
```

The initializer creates only safe placeholders and refuses to overwrite an existing folder unless
`--force` is passed. It is a scaffold, not publication proof. Replace the starter model, poster,
unit data, drawings, environment, price notes and source notes with sourced/developer-approved
material before importing anything into WordPress.

Before relying on the factory for a real project, run:

```bash
npm run qa:project-factory-smoke
```

This creates a temporary project folder, builds `showroom-payload.json`, validates it against the
schema, checks that the expected scaffold files exist, writes
`docs/qa/project-factory-smoke-report.json`, and removes the temporary folder. If this smoke test
is red, do not start the next Sde Dov project yet.

Before any project draft is imported or published, create a project publication manifest and run:

```bash
node scripts/build-project-hreflang-artifact.mjs --manifest <project-manifest> --out-json <hreflang-map> --out-html <hreflang-head>
node scripts/qa-project-hreflang-artifact.mjs --manifest <project-manifest> --map <hreflang-map> --html <hreflang-head> --out <hreflang-report> --strict
node scripts/qa-project-publication-readiness.mjs --manifest <project-manifest> --out <project-report> --strict
```

The hreflang artifact must remain preflight-only until every language URL is live and verified.
The publication gate must prove all language drafts are still draft-only, target `/projects/`, use
the real project asset folder, have Yoast fields, pass their content-depth reports and pass
screenshot QA. Ashira keeps `npm run qa:ashira-publication-readiness` as an alias, but the reusable
checkers are the manifest-driven scripts above.

The plugin should consume URLs and JSON only. Large raw modeling files should live outside the
plugin ZIP and outside the WordPress plugin repository unless explicitly approved.

## Rainbow v1.66.3 QA Lesson: Mobile Product Integrity

Mobile containment is a product requirement, not a CSS detail. The 390px and Edge-mobile gates must
measure the rendered showroom root before and after selecting an apartment. The selector fails if:

- the root is shifted outside the viewport even when the document has no horizontal scrollbar;
- the selected-apartment card collapses the model scene to a tiny strip;
- the card covers the apartment selector before the buyer understands what was selected;
- the first apartment tap does not leave a visible selected state and a readable next step.

When a JavaScript nudge variable exists, late CSS must not cancel it with `transform:none!important`.
If a selected-card mobile sheet is used, it must preserve the model scene height and expose only a
small collapsed handle until the buyer opens it.

Public product copy must stay buyer-facing. Do not publish back-office terms such as lead panel,
funnel, CRM, monetization, or paid placement. The visible page should say inquiry, selected
apartment, developer contact, availability check, and non-binding estimate.

## Buyer Copy Discipline

The model pipeline produces a buyer product, not a demo deck. Public text must describe what a
buyer can see, compare and ask about:

- apartment floor, rooms, sqm, view and orientation;
- available, checking, reserved or sold status;
- non-binding price estimate and source note;
- floor plan, interior media, view, surroundings and next inquiry step.

Do not let model, data or build terms leak into rendered pages. These words are documentation-only:
engine, template, prototype, CMS, SEO, CRM, lead, funnel, monetization, supplier, project manager,
מנוע, תבנית, אבטיפוס, פאנל, לידים.

If the public screen needs a placeholder for media not yet supplied, write it as a buyer promise:
`כאן יוצגו סיור פנים, וידאו או גלריית תמונות כאשר החומר המאושר זמין.`
Do not write `placeholder`, `מקום שמור`, `prototype`, or similar working language.

## Rainbow v1.66.4 QA Lesson: Showroom DNA

The reusable product pattern is two surfaces, close together:

- The rotating `model.glb` is the context surface. It gives the buyer the building massing,
  surrounding area, sun/orientation cues, and premium spatial impression.
- The fixed facade/elevation picker is the transaction surface. Apartment cells live on that
  facade, are color-coded by status, and open the selected-apartment card.

Do not try to make a massing GLB behave like a per-apartment sales model. True 360-degree
apartment picking requires a developer BIM/GLB where each apartment is its own mesh. Until that
asset exists, keep GLB rotation for context and use an adjacent facade/elevation picker for exact
apartment choice.

For every future project, the factory payload must include:

- `project_model_glb` and `project_model_poster` for the rotating context model.
- `project_3d_units` with `stage_x`, `stage_y`, `stage_w`, `stage_h`, status, rooms, sqm, view,
  floor, label, price estimate, and optional tour/plan URLs.
- `project_3d_environment_json` with project-relative context labels such as parks, coast,
  transit, schools, neighboring projects, or civic services. These labels must be local to the
  project; do not hard-code Rainbow/Sde Dov words into the runtime.
- `project_3d_tour_url`, `project_3d_drawings_json`, and per-unit `tour_url`/`interior_url`
  when a Matterport-style or Zillow/Homes.com-style interior tour is available.

The selected-apartment card must never permanently block the facade picker. It needs a close
control and must reopen when a new apartment is selected.

## Dimri Yama Theme-First Lesson: Selected Unit To Lead Funnel

For the next project, do not create a new plugin module just to render the showroom. Prefer a
theme block pattern or theme template part for presentation, and keep the plugin as the shared
data and REST rail.

Minimum reusable markup contract:

- Root wrapper: `data-nlps-showroom`, `data-nlps-project-title`, and `data-nlps-endpoint`.
- Unit cells: `data-nlps-unit`, `data-unit-id`, `data-building`, `data-title`, `data-status`,
  `data-rooms`, `data-sqm`, `data-floor`, `data-view`, and `data-note`.
- Selected card: `data-nlps-card` plus fields for title, status, rooms, sqm, floor, view, note,
  media panel, and a close button.
- Buyer form: `data-nlps-lead-form`, posting to `/nadlan/v1/lead` with the selected apartment
  context. It should support callback and non-binding purchase-check intents.

Public copy still says "פנייה", "דברו איתנו", and "בדיקת רכישה לא מחייבת". It must not leak
internal words such as lead, funnel, CRM, owner routing, automation, or monetization.

Publishing requirement: when owner routing matters, publish the page as a real `nadlan_project`
post or pass a valid `data-nlps-card-id`, so the shared lead endpoint can attribute the inquiry
to the selected project.

## Ashira V2 Clean Contract Lesson

If a project showroom becomes hard to reason about because previous slices stacked CSS and runtime
patches, freeze that path and create a clean contract instead of trying to rescue the cascade.

Ashira v2 uses:

- `.nlv2-showroom` as the only root;
- `.nlv2-*` classes only;
- `data-nlv2-*` runtime attributes only;
- a generated or official bitmap facade for apartment cells;
- a GLB/model-viewer context model beside the facade;
- a selected-apartment card below the scene, not floating over the facade;
- Chrome screenshot proof at desktop, tablet and mobile before merge.

Never mix `.nlps` or `.nlp3d` selectors into this v2 layer. If another project needs the same
standard, clone the v2 contract and replace the asset folder, payload and public copy.

Factory bridge rule: draft/apply scripts must recognize both the old `data-nlps-showroom` root and
the clean `data-nlv2-showroom` root. This is not permission to mix runtimes inside a page. It only
keeps the factory able to generate and dry-run v2 WordPress drafts while the WordPress import schema
still uses the existing `showroom-payload.json` v1 meta contract. When the plugin payload route is
versioned for v2, update the schema and scripts together in one verified slice.

For every v2 preview, run the local Chrome gate before a WordPress import:

```bash
node scripts/qa-showroom-v2-preview.mjs --preview docs/previews/<project>-showroom-v2-preview.html --out docs/qa/screenshots/<project>-v2-preview-factory-gate --strict
```

The report must be green at desktop, tablet, mobile and Edge-mobile widths. If the report catches
mojibake, old selector leakage, card/facade overlap, tap targets below 44px, missing model-viewer
registration, console errors or horizontal overflow, stop and fix the preview before touching the
CMS or live site.

Ashira v2 adds a second pre-import gate:

```bash
npm run qa:ashira-factory-readiness
```

Run it after the screenshot gate and before any WordPress import. It validates that the project
asset folder, `showroom-payload.json`, public strings and screenshot report are all ready for a
buyer-facing project page. The gate should fail if the page or payload talks about the build
system instead of the apartment: no public SEO/CMS/CRM/lead/engine/template/prototype/factory
language, no internal contractor pitch, no placeholder wording, and no mojibake.

The buyer-language test is part of the model pipeline because model data becomes public text:
unit titles, price notes, view notes, media labels and facade notices are all buyer copy once they
render on the page.

The same gate must compare visible facade cells with payload units. Never hardcode extra apartment
cells only in the preview. If a buyer can see or click an apartment, its unit id, status, floor,
rooms, sqm, view and estimate must live in `showroom-payload.json` so the CMS/import path can
recreate it.

After preview readiness, validate the WordPress draft payload before any CMS write:

```bash
npm run qa:ashira-draft-readiness
```

The draft payload is the bridge between the theme-first showroom pattern and WordPress. It must
stay `draft`, keep one H1, contain the supported showroom root, use buyer-facing title and Yoast
metadata, and expose the same unit ids as `showroom-payload.json`. A generated REST payload is not
safe to import until this gate is green and the apply script also passes in `--dry-run` mode.
