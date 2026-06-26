# Project Page Premium Showroom Runbook

Use this skill when turning a real-estate project page into a flagship, replicable project showroom
for NadLan. The target is a buyer-ready, investor-search-ready, contractor-demo-ready page, not a
plain WordPress article.

Before starting, read `skills/goal-discipline-anti-drift.md`. One project must move through one
verified slice at a time: target, proof, smallest step, Chrome evidence, then next step. Do not
open a second feature/PR/deploy path while the current proof is unresolved.

## A. Source And Intent Research

1. Search Hebrew and English SERP for the project name, developer, neighborhood and price intent.
2. Open the official project site, developer page, compound/city page, Madlan/Yad2 if permitted,
   and news sources that report sales or construction milestones.
3. Record only public or licensed facts: developer, units, floors, amenities, status, notable
   public sales, price per sqm ranges, transport, parks and risks.
4. If numbers conflict, show the conflict. Example: developer marketing count vs municipal permit
   count. Truth-first is part of the NadLan brand.
5. Do not publish paid-source rows or subscription-only data until the owner approves the license
   and public wording.
6. Before writing the short intro above the model, read the first organic result snippets and
   extract the language users and competitors already recognize. For Rainbow this means:
   `Rainbow Tel Aviv`, `ריינבו תל אביב`, `שדה דב`, `ישראל קנדה`, `דירות`, `מחיר`, `זמינות`,
   `ריזורט מגורים`, `קרוב לים`, and amenities language. Use those naturally, not as a keyword
   list.

## B. Page Assembly

1. One URL only, under `/projects/<latin-slug>/`.
2. Keep one visible H1.
3. Place the interactive model immediately after breadcrumbs and before the old static profile card.
4. Wrap the model with `<!-- nlp3d-start -->` and `<!-- nlp3d-end -->`.
5. Add a concise source-backed content block with:
   - buyer summary,
   - price/availability disclaimer,
   - project facts,
   - FAQ visible in the body.
6. Seed schema meta before `wp_head`, never on `the_content` render:
   - `amenities`,
   - `official_site_url`,
   - `price_range`,
   - `price_min`,
   - `price_max`,
   - `project_faq_json`.
7. Transactional project SEO must be verified separately from the 3D module:
   - public title leads with buyer language such as `דירות למכירה` and `מחירים`,
   - meta description mentions price only as sourced or non-binding,
   - visible body contains natural buyer phrases, not keyword stuffing,
   - run the project page assembly checker when one exists.
8. If a one-shot content seed already ran, never re-run the old seed. Add a new dated/numbered
   idempotent option for the delta, for example `nadlan_<project>_seo_vXXXX`.

## B2. Child Theme Versus Plugin Boundary

1. Put reusable data contracts, meta registration, sanitization, REST endpoints, lead/WhatsApp
   routing, model-viewer runtime loading and importer/validator scripts in the plugin.
2. Put project page hierarchy, breadcrumbs, showroom placement, article heading alignment,
   paragraph width, visual wrappers and responsive layout CSS in the child theme when possible.
3. Do not ship a plugin ZIP for a one-page visual alignment issue if a child-theme template/CSS
   layer can solve it more safely.
4. Heavy project media such as GLB, poster, facade, drawings and tours belong in Media Library,
   CDN, or project asset URLs during prototype. Do not bloat the plugin ZIP with per-project media.

## C. 3D And Buyer Interaction

1. Default view is the building selector, not the map.
2. The buyer can drag or tap angle controls to rotate/spin.
3. Clickable floors/units update the selected-unit card, facts, compare tray, sun insight and lead
   payload.
4. Apartment markers must be obvious without explanation: the default visual target is an
   apartment cell/rectangle on the building, not an abstract dot. It needs a 44px+ target,
   color-coded availability, label, hover/tap info and optional recommended pulse.
5. The selected-apartment card is the hero after a click: title, status, view, non-binding price
   estimate and actions for details, view and developer contact.
   The card must also include buyer tags, a short next-step note, status-color edge treatment and
   estimate wording when prices are not official.
6. Map view is user-opened and lazy-loaded to control Mapbox costs.
7. Register Mapbox RTL text plugin before creating a map with Hebrew labels.
8. Drawings, floor plans and real inventory are optional CMS fields. If absent, show a clear request
   path instead of faking a plan.
9. Price can be:
   - official unit price,
   - explicit unit estimate,
   - project average per sqm estimate,
   - or `לפי פנייה`.
   Anything estimated must say `אומדן` and `לא מחייב`.
10. If a real GLB is loaded, the fallback procedural tower must disappear. Seeing both the old tower
    and the GLB together is a hard visual failure. A model error must show a visible error state,
    not silently bring back the old tower or old facade.
11. If the GLB is not apartment-level BIM, keep it as the rotating product object and add a static
    facade/elevation selector beside it for apartment picking. This is not a downgrade: it is the
    honest product architecture until every apartment exists as its own GLB mesh. The buyer clicks
    cells embedded in the facade, not dots floating around the 3D object.
12. The model should open close enough for unit selection and rotate slowly. Fast spin, wide camera
    and tiny markers make the experience feel like a technical demo instead of a buyer showroom.
13. If no official facade/elevation render exists yet, create an original high-quality bitmap
    prototype and label it as illustrative. Wire it only through `project_3d_facade_images`; do not
    revive fake CSS/SVG grids, and do not overwrite an existing official contractor-supplied facade.
    The upgrade path must stay field-only: replace the prototype URL with the official render later.

## C2. Product Showroom Fields

Every flagship project page must expose the following before it is considered clone-ready:

1. `project_3d_model_type` for the model source quality (`procedural`, `facade`, `sprite360`,
   `gltf`, `bim`).
2. `project_3d_video_url` for developer sales video or meeting recording.
3. `project_3d_tour_url` for a 3D/interior walkthrough when supplied.
4. `project_3d_cesium_tiles_url` as the future photorealistic 3D city-view seam.
5. `project_3d_drawings_json` for approved plans, elevations and site drawings.
6. `project_3d_environment_json` for nearby projects, schools, parks, transit and public services.
7. Per-unit `interior_url`, `tour_url` and `view_note`.

Material fields are not complete until they appear in the buyer UI:

- drawing items must surface in the plan/drawing panel,
- video and tour URLs must surface in the media panel,
- environment items must surface in the surroundings panel,
- future Cesium/3D city-view URLs must be exposed as a ready seam in the view panel,
- nested material URLs must be sanitized before rendering as links.

Interior journey rule: after a buyer selects an apartment, the product must offer a clear path to
step inside the apartment when media exists. The sequence is selected apartment card, floor plan,
interior render or room carousel, 360/Matterport/Marzipano tour if supplied, video if supplied, and
request-full-plan/contact CTA. If official assets are missing, generated prototype media is allowed
only with an illustrative/non-binding label. Do not present generated interiors as official
developer material.

The default model can be schematic, but the user experience must still feel like a product
showroom: building-first, drag to rotate/tilt, visible zoom controls, large unit hit areas, no
nested scrollbars and source-aware price/availability wording.

Per-unit fields required for a buyer-ready selector:

1. `label` for short marker/tool-tip copy.
2. `status` in `available`, `reserved`, `sold`, controlling marker color.
3. `recommended` boolean for owner-approved featured units.
4. `price_estimate` plus source note when an approximate price is shown.
5. `hotspot_position` and `hotspot_normal` for GLB hotspots.

Marker design rule: the model surface should read as apartment inventory. Use facade-like
rectangles/cells with status color and subtle window rhythm as the default. Use dots only as a
last-resort fallback when the actual model geometry is too dense or the viewport is too small. The
full details belong in the selected-apartment card, especially on mobile.

Apartment-cell rule: if a buyer says "these are just dots", the design failed. The visual target is
closer to a product configurator plus a tower sales plan: visible apartment rectangles on the
building, each with availability color and a large invisible touch zone. The cell should answer
"where is this apartment in the building?" before the tooltip or side panel opens.

Gesture rule: the same large hit area must support both buyer actions. A tap selects the apartment,
but a drag that starts on the marker rotates the building. Never exclude the unit hit area from the
model drag path.

Selected-card rule: once a unit is selected, the card must answer the buyer's first four questions:
is it available, what is the approximate price context, what view/direction does it have, and what
is the next step. The language must be public and buyer-facing, never internal operations wording.

## D. Lead And WhatsApp Funnel

1. Every CTA must enter the same lead CPT and routing rails.
2. Site forms use `/nadlan/v1/lead`.
3. WhatsApp messages should use a secret-gated bridge such as `/nadlan/v1/wa-lead`; never rely on a
   click-to-chat link as the only funnel.
4. Always send `card_id` when known. If unknown, route to admin fallback and log attribution gap.
5. Lead payload should preserve unit, floor, sqm, building, timeline, budget, advisor and
   non-binding purchase intent.

## E. Browser QA Gate

Check real Chrome or Playwright at:

- 390px mobile,
- 760px tablet,
- 1440px desktop.

Pass criteria:

- no horizontal overflow,
- no raw JavaScript text visible,
- no page errors,
- 44px tap targets,
- building selector is visible quickly,
- drag changes model angle,
- unit click updates facts and card,
- view button opens map only on demand,
- Hebrew map labels are not reversed,
- floating buttons do not cover forms or footer,
- schema contains visible FAQ-aligned data.

## F. Deployment Reminder

After a PR is merged:

1. Pull/sync the uPress/server Git copy.
2. Trigger or upload the WordPress plugin update.
3. Hard refresh the page.
4. Check `/wp-json/nadlan/v1/healthcheck` for the new version and feature blocks.

GitHub merge alone does not update production.

## G. Rainbow Template v1 Gate

Before using Rainbow as the template for another project, the page must pass the small-product gate,
not only the content gate:

1. The 390px mobile view keeps the entire showroom inside the viewport before and after unit
   selection.
2. The selected-apartment card does not collapse the model scene, hide the building, or cover the
   first-choice action.
3. Apartment markers read as apartments on a building. Dots are acceptable only as a temporary
   fallback before a facade image, apartment-cell overlay, or real per-unit GLB is available.
4. The first public paragraph and all public labels use buyer language only. Never publish internal
   words such as lead panel, funnel, CRM, monetization or paid placement.
5. The healthcheck exposes any one-shot content cleanup marker, because a production DB seed is not
   proven until the live endpoint reports that it ran.
6. The final proof is a Chrome screenshot and a visual QA report. Saved fields, imported JSON and
   ZIP integrity are necessary, but not sufficient.

## H. 2026-06-14 Rainbow GLB Finish-Line Addendum

For any project page that uses a GLB/model-viewer showroom, the live gate is buyer-rendered Chrome,
not saved meta fields.

Required runtime proof:

1. The rendered `nadlan-model-viewer` script tag includes `type="module"`. In WordPress, enforce it
   with a `script_loader_tag` filter for that handle.
2. Chrome console returns a function for `customElements.get('model-viewer')`.
3. The `<model-viewer>` element uses `reveal="auto"` and `loading="auto"` with a poster, so the
   building appears without a first click and without a blank frame.
4. The public page has no `Unexpected token 'export'`, no raw `class=`, no visible JavaScript/HTML
   fragments, no horizontal overflow, and one H1.
5. The first paragraph above the model names the project, location, developer and non-binding
   price/availability rule before generic showroom language.

Material JSON standard:

1. `project_3d_drawings_json` may be a flat item array or an object with an `items` array.
2. `project_3d_environment_json` may be a flat array or a sourced object with `layers[].items[]`.
3. The runtime must flatten structured environment layers into safe buyer-facing cards.
4. Illustrative relative positions are not survey pins and must not be displayed as exact map data.

Owner manual standard:

1. Every flagship project ships `docs/owner-manual-project-showroom.md`.
2. The manual must explain where the `בחירת דירות אינטראקטיבית` metabox lives in WordPress.
3. The manual must list the exact fields for GLB, poster, USDZ, unit JSON, drawings, surroundings,
   video, tours, Cesium/3D Tiles seam and price notes.
4. The owner path must use a simple unit-builder UI before raw JSON. Raw `project_3d_units` remains
   for import/debug, not for normal contractor edits.
5. Classic Editor is only a temporary visibility aid. The durable fix is a clear plugin-owned
   metabox/sidebar plus REST-writable fields.
6. GitHub merge, plugin update, and field save are not final proof. The buyer-facing page and
   Chrome screenshots are the proof.

## I. Showroom DNA For Cloned Project Pages

Use the same hierarchy for every project page:

1. Short SEO intro above the showroom: project name, neighborhood, developer, non-binding price or
   availability rule, and "choose an apartment" intent.
2. Rotating 3D model beside the facade picker on desktop. On mobile, stack them tightly: model
   first, facade picker immediately below, then selected apartment card.
3. Fixed facade/elevation apartment cells are the primary selector. The cells should show useful
   labels, not anonymous dots.
4. Status colors are stable: available = green, reserved/checking = amber, sold/unavailable = red.
   Recommended/high-demand units may pulse only when they are available.
5. The selected-apartment card contains price estimate, rooms, sqm, floor, view, status, and three
   buyer actions: full details, view from apartment, and contact the developer.
6. The card must have a dismiss button and must not hide the facade permanently.
7. The environment layer is project-relative. For Sde Dov it may show sea/coast/Reading/nearby
   projects; for Ramat Aviv it should show that neighborhood's parks, roads, schools and transit.

This is the factory standard: one model, one facade/unit map, one environment file, one poster, one
SEO/content pack. Do not create a new plugin feature for each project unless the reusable payload
contract cannot express it.

## J. Inventory Semantics v1.66.9

The facade picker is the buyer's inventory surface. It must answer "can I ask about this apartment?"
before the buyer opens the card:

1. Available cells are green and may pulse only when recommended.
2. Reserved/checking cells are amber and still selectable for follow-up.
3. Sold/unavailable cells are red, lower-emphasis, and not selectable.
4. Non-available cell labels should include the status text inside the cell where space allows.
5. The same status must be mirrored in the selected-apartment card edge color and status chip.

## K. Hierarchy Standard v1.67.0

For the clone-ready project showroom, keep the visible hierarchy stable:

1. A real project media image or poster appears above the showroom and before the short SEO intro.
2. The rotating GLB/model-viewer is context only unless the asset is true per-apartment BIM.
3. The fixed facade/elevation is the primary apartment picker. Hide old floating model squares and model-viewer hotspots when the facade picker is present.
4. The selected-apartment card docks below the scene on desktop, tablet and mobile. It must never permanently cover the model, facade, cells or lead form.
5. On mobile, stack tightly: media image, intro, model, facade, selected card, then article.
6. Article H2/H3 headings must share the same reading column as the paragraphs. Do not let theme-side headings drift to the far right while paragraphs sit in the center.
7. Clone this as one layout contract for every project: poster, short intro, rotating context model, fixed inventory facade, selected-apartment card, structured article.

## L. Interior Journey Contract

The model/facade selector is not the end of the buyer journey. It is the door into the apartment.
Use the engine documented in `docs/design/2026-06-19-project-showroom-engine-interior-journey.md`.

Minimum for a prototype:

1. Every selectable unit may include `plan_url`, `interior_url`, `tour_url` and `view_note`.
2. The selected-apartment card must expose "view from apartment" and "inside the apartment" when
   those fields exist.
3. Project-level `project_3d_tour_url` and `project_3d_video_url` are fallbacks when a unit-specific
   tour does not exist.
4. Prototype interiors must be marked illustrative until contractor-approved assets arrive.
5. The lead payload must keep the selected unit id/title/floor/rooms/sqm/status so the contractor
   knows which apartment the buyer explored.

## M. Clean V2 Reset Rule

When a project page has accumulated stacked showroom CSS, do not add another override layer. Start a
clean v2 contract:

1. Use a new root such as `.nlv2-showroom` and only `.nlv2-*` selectors.
2. Use only `data-nlv2-*` attributes for the new runtime.
3. Do not add `.nlps`, `.nlp3d`, old compatibility selectors, or `!important` patches to v2.
4. Enqueue old and new assets by content marker:
   - old pages with `data-nlps-showroom` load old assets only;
   - v2 pages with `data-nlv2-showroom` load v2 assets only.
5. Keep the rotating GLB as the context surface until official per-apartment BIM exists.
6. Keep the facade/elevation image as the apartment-picking surface.
7. Prove v2 with screenshots at 1440, 768 and 390 before any live import.
8. Factory scripts must accept both `data-nlps-showroom` and `data-nlv2-showroom` roots while
   pages transition from the old runtime to the clean v2 runtime. V2 page markup uses only
   `data-nlv2-*`, but `showroom-payload.json` can still use the existing import schema until the
   plugin-side payload API is deliberately versioned.

The Ashira clean v2 proof lives in
`docs/qa/2026-06-26-ashira-v2-clean-preview.md`.

Before importing any v2 preview into WordPress, run the reusable Chrome preview gate:

```bash
node scripts/qa-showroom-v2-preview.mjs --preview docs/previews/<project>-showroom-v2-preview.html --out docs/qa/screenshots/<project>-v2-preview-factory-gate --strict
```

This gate must capture desktop, tablet, mobile and Edge-mobile screenshots, then prove no
horizontal overflow, one H1, model-viewer registration, visible Hebrew, no mojibake, no public
internal wording, no old `.nlps` / `.nlp3d` roots, apartment cells with 44px+ tap targets, and no
selected-card overlap over the facade.

## N. Buyer-Language Rule

Public project pages speak to buyers only. They do not explain our business model, CMS, SEO plan,
lead routing, template system, engine, strategy or contractor sales pitch.

Before publishing or previewing a project surface, ask: would a buyer care about this sentence
while choosing an apartment? If not, move it to docs or admin.

Buyer-facing wording should answer:

1. Which apartments or projects can I compare?
2. What floor, rooms, sqm, view and direction are shown?
3. What is the price context, and is it an estimate?
4. What plans, photos, video, interior tour or view are available?
5. What do I do next if I want to check availability?

Forbidden public wording includes:

- SEO, CMS, CRM, lead, engine, template, prototype, funnel, monetization, paid placement;
- פאנל, מנוע, תבנית, לידים, מוניטיזציה;
- project manager, supplier or contractor language when it is speaking about our service rather
  than helping the buyer choose an apartment.

Allowed public wording includes:

- דירה, קומה, חדרים, שטח, נוף, כיוון, מחיר, אומדן לא מחייב, זמינות, תוכנית, סיור, תמונות,
  בדיקת רכישה לא מחייבת, דברו עם היזם.

Every screenshot QA must include a visible-copy scan. A page can look premium and still fail if it
talks to us instead of to the buyer.
