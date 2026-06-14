# Project 3D Sales Experience Skill

Use this when adding or improving an interactive real-estate project model on nad-lan.co.il.

## Standard

- Start with a fast, premium model that can ship without BIM: architectural massing, floor selection, unit selection, and clear inquiry flow.
- The model must be interactive, not a static image. Minimum interaction: drag-to-rotate, floor selection, unit selection, selected-unit facts, and a view/inside preview mode.
- Do not publish invented prices, availability, apartment numbers, or floorplans. If data is illustrative, label it clearly and render price as `לפי פנייה`.
- Keep all real interest capture inside the existing lead system. Do not create a second lead endpoint.
- Every unit-level CTA must include `card_id`, `unit`, `floor`, `rooms`, `sqm`, and a source marker so the owner can see which apartment created the lead.
- A theoretical purchase CTA is allowed only as a non-binding inquiry. It must say availability, price, and terms require human verification.
- Use dark blueprint, champagne linework, restrained glass, and architectural geometry. Avoid cartoon buildings, fake stock photos, fake people, and fantasy renders.
- Make mobile usable first: no horizontal overflow at 390px, 44px tap targets for model controls, and stacked forms.

## CMS Contract

Use the existing `nadlan_project` metadata:

- `project_3d_image`
- `project_3d_viewbox`
- `project_3d_units`
- `project_3d_demo`

Recommended unit JSON fields:

```json
{
  "id": "R-34-E",
  "title": "קו E",
  "floor": 34,
  "rooms": 5,
  "sqm": 158,
  "balcony": 22,
  "dir": "צפון מערב",
  "line": "E",
  "view": "ים, פארק ושדה דב",
  "price": 0,
  "status": "available",
  "plan": ""
}
```

`price: 0` means `לפי פנייה`. Only official owner/developer data should set a price.

## Long-Term Upgrade Path

- Phase 1: pseudo-3D tower picker in `inc/project-3d.php`.
- Phase 2: owner-approved elevation image and real unit inventory.
- Phase 3: traced polygons or GeoJSON per floor.
- Phase 4: compound map with Mapbox 3D buildings and project pins.
- Phase 5: real BIM/IFC/glTF/3D Tiles when the developer provides source files.

## Sde Dov To Countrywide Rollout

Treat Sde Dov as the first district template, not as a one-off.

For each district:

- Create one `nadlan_compound` term for the district or subdistrict.
- Assign every real project card to that compound.
- Require city, lat, lng, developer, project status, unit count when sourced, and official links.
- Enable the compound map only after token, term, and project pins are present.
- Add project-level 3D only where the card has `project_3d_demo=1` or real unit/elevation metadata.

For countrywide expansion:

- Start with high-value districts: Sde Dov, Park Hayam Bat Yam, Glilot, Pi Glilot, Bavli, Kikar Hamedina, Givat Amal, Ramat Hasharon west, Herzliya marina and business district, Jerusalem entrance district.
- Normalize every project into the same unit JSON contract so one renderer can power all projects.
- Keep official data provenance in the project body or references list.
- Never generate fake inventory to fill gaps. Use a premium illustrative model with clear demo labeling until official data arrives.

## Data Quality Levels

- `concept`: visual massing only, no official unit data. Price shows `לפי פנייה`.
- `traced`: owner-approved elevation/floor polygons, but availability not verified. Price shows `לפי פנייה`.
- `inventory`: verified unit fields from owner/developer, still non-binding unless contract process exists.
- `bim`: real BIM/IFC/glTF/3D Tiles source connected to project/unit data.

Only `inventory` and `bim` can show specific prices or availability.

## v1.60.0 — Fully interactive buyer layer (Claude)

What shipped on top of the v1.59.x picker (all inside `inc/project-3d.php`, same look/borders):

- **FIX**: floor strip rendered zero buttons since 1.59.0 (`[].slice.call(new Set(...))` returns
  `[]` — Set is not array-like). Floor navigation works now. Lesson: never spread a Set with
  `slice.call`; use an indexOf-dedupe or `Array.from`.
- **Live view-from-unit**: when `nadlan_mapbox_token` option is set AND the project has `lat`/`lng`
  meta, the "מבט מהדירה" panel lazy-loads Mapbox GL v3.14.0 and places a free camera at
  `ground_elevation + 4.0 + (floor-1) × floor_height + 1.55` meters, looking 900m along the
  facade bearing, with 3D building extrusions. Honest fallback (gradient + "יופעל כאשר מפתח
  המפות יוזן") when tokenless. Camera math documented in
  docs/2026-06-11-rainbow-research-and-inventions.md (strand 2).
- **Sun insight (אור ושמש tool)**: pure-JS solar position (SunCalc-core formulas, no API), direct
  sun windows for summer/winter solstice per facade bearing (±70° cone, >8° elevation, Israel
  clock). Validated against NOAA: TA solstice noon elevation 81.3° exact. Sun hours also appear
  in the comparison table.
- **Compare**: up to 3 units, chips tray + overlay table (floor/rooms/sqm/balcony/dir/view/sun/
  status), "בחר" from table selects the unit. Persisted in localStorage per project.
- **Lead wizard**: 2 steps with progress dots (contact → progression details), multi-select
  advisors checkboxes (lawyer/mortgage/inspection/designer) joined into the lead payload
  (`advisor`, plus full list in message). Research basis: multi-step forms convert ~37% better.
- **Plan lightbox**: image plans open in-overlay; PDFs in iframe; other URLs default.
- **Deal-step tracker**: after successful submit, "בחירה" (and "ליווי" if advisors chosen) are
  marked done; lead reference id shown when the REST response includes one.
- **Selection persistence**: last selected unit restored per visitor (localStorage).

### Replication playbook — onboarding the NEXT project (fill-in-the-details)

No code changes needed per project. Per-building checklist:

1. Create/locate the `nadlan_project` post. Set post meta:
   - `lat`, `lng` (decimal WGS84) — enables live view + sun insight.
   - `project_3d_floor_height_m` (default 3.05; luxury towers 3.1–3.3).
   - `project_3d_ground_elevation_m` (coastal TA ≈ 5–25; from Google Elevation or city GIS).
   - `developer_name`, `project_status`, `num_units`, `city`, `address`.
2. Facade: upload an ORIGINAL elevation render → set `project_3d_image` + `project_3d_viewbox`
   (e.g. `0 0 1000 1000`). Trace per-unit polygons in those viewBox coordinates.
3. Units: fill `project_3d_units` JSON (one object per sellable line/unit). Template:
   `docs/templates/project-3d-units-template.json`. Required: `id`, `floor`. Strongly
   recommended: `dir` (Hebrew compass words — drives camera bearing AND sun calc), `points`
   (facade polygon), `plan` (drawing URL → lightbox), `rooms`, `sqm`, `balcony`, `view`,
   `building`, `availability`, `status` (available|reserved|sold).
4. If no verified inventory yet: tick `project_3d_demo` — prices show "לפי פנייה" and the demo
   disclaimer renders. NEVER enter invented prices.
5. Flag: `nadlan_feature_project_3d` must be ON; Mapbox token once globally in NadLan Features.
6. Verify: healthcheck `project_3d` block shows `renderer: premium_tower_picker_v4`,
   `view_from_unit: mapbox_live` (or `awaiting_token`), `sun_insight/unit_compare/lead_wizard:
   true`. On the page: click a floor on the tower, click a facade polygon, open אור ושמש (real
   hours appear if lat/lng set), compare 2 units, run the 2-step form, confirm the lead arrives
   with unit/floor/advisors/camera params.

### Countrywide note
Everything above is data-driven from post meta — the Sde Dov content seeder (MISSION-CODEX-
CONTENT) can populate steps 1–3 for every compound project programmatically. The same template
serves any tower in Israel.

## v1.60.2 Flagship Clone Standard

Use this section as the repeatable standard for every future premium project page and every
building that later appears inside a compound map.

### Page Placement

- The interactive model belongs near the top of the project page, after a compact project heading
  and before the long article body. Do not bury it below thousands of words.
- Keep one short keyword-rich intro around the model so search engines understand the page:
  project name, city, district, developer, apartment selection, view from apartment, sun, unit
  comparison, and purchase guidance.
- Long-form article content stays below the model. Visitors must reach the interaction on first
  glance or within a very short scroll.

### Reusable Data Contract

Every cloned project must use the same post meta contract:

- `lat`, `lng`
- `project_3d_image`
- `project_3d_viewbox`
- `project_3d_units`
- `project_3d_floor_height_m`
- `project_3d_ground_elevation_m`
- `project_3d_demo`

Each unit object should be stable enough to sync with the future compound map:

- `id`: stable public-safe unit id.
- `building`: tower or boutique building name.
- `floor`: numeric floor.
- `line`: line/stack.
- `rooms`, `sqm`, `balcony`.
- `dir`: Hebrew compass direction, used for camera bearing and sun logic.
- `view`: human-readable view.
- `points`: SVG polygon points in `project_3d_viewbox` coordinates.
- `plan`: official or owner-approved drawing URL.
- `status`: `available`, `reserved`, or `sold`.
- `availability`, `market_note`, `source_note`.

Only verified owner/developer inventory may set a real `price`. Demo or researched-but-unverified
rows must use price 0 and display "price by inquiry" behavior.

### Compound Map Linkage

- The project page and the compound map must read from the same `nadlan_project` card and the same
  unit JSON. Do not maintain a separate map-only copy of inventory.
- Compound pins use project-level `lat` and `lng`; unit views use the same coordinates plus
  `floor_height_m`, `ground_elevation_m`, and unit direction.
- The future map can deep-link into a selected unit by URL state, for example:
  `/projects/project-slug/?unit=R-24-W`.
- A project should not be promoted in the map unless healthcheck confirms `project_3d.enabled`,
  `facade_polygons`, `lead_unit_payload`, and the current renderer.

### Public Copy Rules

- Public page copy must speak to buyers, investors, project owners, and advisors. Never mention
  internal terms such as prompt, SEO task, CRM, route, REST, lead endpoint, Claude, Codex, or plugin.
- CTAs must be clear and non-binding unless a real legal/purchase rail exists.
- Show uncertainty honestly: use "requires developer verification" language for price,
  availability, drawings, and purchase terms unless the source is official.

### Visual Standard

- Use dark blueprint, restrained champagne linework, glass panels, precise spacing, and large
  calm surfaces.
- No stock faces, no fake logos, no fantasy towers, no cartoon houses.
- Keep the map draggable and visible when token and coordinates exist. Non-fatal map style warnings
  must not hide the container.
- At 390px mobile, there must be no horizontal overflow, all controls must be 44px or larger, and
  the model, unit facts, comparison, and form must stack cleanly.

### Verification Before Replication

For every cloned project, verify:

- Healthcheck exposes the expected renderer and capability flags.
- Model appears before the long content body.
- Selecting a unit updates selected-unit facts, camera altitude, sun insight, compare tray, and lead
  payload.
- Owner/project request form uses the existing lead route with `source=project_3d_showcase`.
- No invented prices, drawings, apartment numbers, or availability appear publicly.

### Ecommerce Patterns To Reuse Carefully

- Use 360/product-spin behavior as an inspection affordance: the visitor should understand that
  the model can be rotated and explored.
- Keep a selected-unit dock visible, similar to a selected product state in premium commerce. It
  should show the current unit, status, and next step.
- Use guided progression rather than a fake cart. Until provider pricing, terms, invoices,
  cancellation language, and routing are real, interior design, legal, mortgage, and inspection
  services should remain advisor/package options inside the inquiry flow.
- Do not add a payment button for apartments or services unless the legal, billing, fulfillment,
  and owner/developer authorization rails are already implemented.

### WordPress Container Gate

- Do not rely only on selectors like `.entry-content > .nlp3d`. The project model can be inserted
  inside plugin profile wrappers, theme blocks, or shortcode containers. The final layout override
  must also target `.nlp3d.nlp3d-premium` directly.
- At desktop width, measure `.nlp3d`, `.nlp3d-shell`, `.nlp3d-stage-wrap`, `.nlp3d-console`,
  `.nlp3d-viewframe`, and `.nlp3d-view-map`. No child may have a negative x coordinate and the
  live view map must be in the main stage, not trapped inside the side console. Gate: the live
  `.nlp3d-view-map` should be at least 60% of the stage width when open.
- Mapbox warnings are not failures by themselves. A real failure is no `.mapboxgl-canvas`, a hidden
  `.nlp3d-view-map`, or an off-canvas map rectangle. If Mapbox cannot load, show an honest inline
  fallback while keeping unit selection, comparison, sun insight, and inquiry working.

### Clone And Translation Standard

- Treat the 3D module as a replicable product template for every large project. Data changes per
  project; the interaction model stays stable.
- Before scaling beyond Rainbow/Sde Dov, extract public UI labels into translation-ready strings or
  filters so Hebrew, English, French, and Russian pages can share one data contract.
- Do not hard-code project-specific marketing text into the 3D engine. Project copy belongs in the
  card body/meta; the engine renders labels, states, units, views, and actions.

### v1.60.4 App Selector Standard

- Default state must be the building selector, not the map. The buyer should immediately understand
  that the building is the product: drag/spin, choose floor, choose unit, then inspect.
- Mapbox/Cesium/Google views are high-value but cost-bearing. Lazy-init them only after a user asks
  for `מבט`; do not instantiate map objects on page load.
- Keep selected-unit state visible on the main stage, not only in a side rail. The stage card should
  show title, status, view, price/estimate state, and next actions.
- Avoid nested browser scrollbars inside the module. Panels may wrap or stack, but `.nlp3d-console`,
  `.nlp3d-units`, `.nlp3d-facts`, and `.nlp3d-tool-panel` must not look like embedded iframes.
- Floor plates should read as architecture: stable taper, visible active floor, unit markers, and
  keyboard/focus support. Avoid decorative random-width silhouettes.
- Pricing is optional and source-aware:
  - Official unit `price` may display as price.
  - Unit `price_estimate` or project `project_3d_avg_price_per_sqm` may display only as
    `אומדן` with a short non-binding note.
  - If no approved source exists, display `לפי פנייה`.
- Future authorized market data should map into the existing unit JSON or project-level average
  estimate fields. Do not publish paid-source transaction rows blindly or imply official developer
  availability without approval.

### v1.61.0 Premium Showroom Standard

- The interactive model belongs immediately after breadcrumbs and before the old static profile
  card. If the buyer must scroll through a hero image/profile card first, the page feels like a
  document rather than a showroom.
- Stage-first layout: the building selector is the first usable surface, with facts, filters and
  forms as supporting panels. SEO copy can follow the stage, but it must not push the interactive
  product below the fold.
- Use stable markers around the module: `<!-- nlp3d-start -->` and `<!-- nlp3d-end -->`. Content
  migration and future translation tooling must split by markers rather than guessing DOM order.
- Map labels must support RTL. Register the Mapbox RTL text plugin before creating the live map.
- Price estimates are allowed only as `אומדן` with a short source note. If the source is public
  market reporting, state the source/date class in the note and keep the value non-binding.
- WhatsApp is not a funnel by itself. A premium project page needs a secret-gated ingestion path
  that can turn WhatsApp messages or shortcuts into the same lead CPT and owner routing used by
  the site forms.
- Floating contact controls must respect safe-area insets, 44px tap targets, focus outlines and
  mobile viewport height. They must not cover the 3D stage, lead form or footer.
- After every merge: pull/sync the uPress/server Git copy first, then update or upload the
  WordPress plugin. Merging GitHub alone does not update production.

### v1.62.0 Product Showroom Contract

- Treat the building as the product, like a premium ecommerce configurator: the default state is a
  single full-stage selector, not a map, not a side panel and not a document body.
- Drag must rotate the model horizontally and tilt it vertically. Double tap / double click can zoom;
  explicit zoom buttons must exist for keyboard and accessibility.
- Clickable unit targets must be larger than the visible polygons. Use invisible SVG hit polygons or
  equivalent hit areas so users can press the apartment, not only a thin line.
- No nested visible scrollbars inside the showroom. If there is too much information, stack panels
  below the stage or split into clear cards. The module must feel like an app surface, not an iframe.
- CMS fields required for every future flagship project:
  - `project_3d_model_type` (`procedural`, `facade`, `sprite360`, `gltf`, `bim`),
  - `project_3d_video_url`,
  - `project_3d_tour_url`,
  - `project_3d_cesium_tiles_url`,
  - `project_3d_drawings_json`,
  - `project_3d_environment_json`,
  - per-unit `interior_url`, `tour_url`, `view_note`.
- CMS material fields are only useful if the buyer can act on them. Render approved drawings,
  tours, videos, surroundings and future city-view links as source-aware material cards inside the
  relevant showroom panel, with sanitized URLs and honest empty states.
- Data quality must be explicit. Procedural/demo geometry is allowed for a sales prototype, but the
  public copy must not imply it is official BIM, official floor plans or verified availability.
- Zillow-style parity for project pages means: unit picker, floor plans/drawings when provided,
  photos/video/tour slots, view/surroundings layer, source-aware price context, comparison and a
  lead path that preserves the selected unit.
- Cesium / Google Photorealistic 3D Tiles remains a lazy, user-opened view layer until cost and token
  governance are approved. Do not instantiate it on page load.

### v1.62.1 First-Screen Showroom Gate

- If a project has the 3D showroom, do not let the theme featured image become the first visual
  product impression. The interactive stage must appear before the long article body and before any
  static profile/featured-image treatment.
- The first visible showroom surface should be the building selector. Supporting SEO copy can sit
  directly below the stage, but it must not push the model out of view.
- Fixed WhatsApp, AI and accessibility controls must not overlap the 3D toolbar, selected-unit card,
  floor picker or lead form. On project showroom pages, move them away from the stage controls or
  collapse them.
- Bare WordPress article headings must be guarded on project pages: no floated headings, no
  pushed-right fragments, readable paragraph width, and tables centered/contained.
- Product-style drag means full-circle rotation. Do not clamp the model to a narrow facade angle.
  Preset buttons are useful, but free drag should normalize around 360 degrees and may add light
  release momentum.
- The healthcheck for a cloned flagship should expose a first-screen renderer marker and flags for
  static image suppression, cleared floating actions and full 360 rotation.

### v1.63.0 Real Model Rail

- The durable showroom path is not CSS art. When a project has a real model, render
  `<model-viewer>` from `project_model_glb` and keep the procedural/facade tower only as fallback.
- Add project-level CMS fields for `project_model_glb`, `project_model_usdz`, and
  `project_model_poster`. Keep large modeling source files outside the plugin ZIP.
- Add per-unit hotspot fields: `hotspot_position`, `hotspot_normal`, and optional `camera_orbit`.
  These fields let a buyer click the apartment on the real 3D model while preserving the existing
  selected-unit, comparison, inquiry and analytics flow.
- Never hide the fallback stage before the real model loads. If a GLB fails, the user must still be
  able to inspect units through the procedural/facade selector instead of seeing a blank dark box.
- Use poster/lazy loading for performance. If no poster is supplied, reveal the model automatically
  so the first impression does not feel dead.
- Model hotspots, facade polygons and floor plates must all converge into the same `selectUnit`
  state machine. Do not create a parallel lead payload or a second apartment state.
- Mapbox/Cesium/Google Photorealistic 3D Tiles remain the view/environment layer. They are not the
  building-product model and should stay user-opened unless cost governance changes.
- For the full modeling runbook, use `skills/skill-3d-model-pipeline.md` before creating the next
  project showroom.

### Live DOM Buyer-Action Gate

- A showroom is not verified merely because the markup exists. The browser gate must prove the
  buyer action loop: click or tap a model hotspot, facade polygon or unit target, then confirm the
  selected-unit title, stage card and active state update.
- When `--expect-glb` is used, require visible `<model-viewer>` dimensions, no model error class,
  and at least one model hotspot. If this fails, the page is still in fallback mode.
- Contact, AI, WhatsApp and call buttons must be checked geometrically against visible showroom
  controls. They may sit at a safe viewport edge, but they must not cover toolbar controls,
  hotspots, the selected-unit card, the live-view return button or form fields.
- Run the gate at desktop 1440px and mobile 390px. A pass at one size does not prove the other.
- Treat 44px tap target warnings as deploy blockers for the final showroom review, even if they are
  acceptable warnings while the fallback/prototype is still live.
