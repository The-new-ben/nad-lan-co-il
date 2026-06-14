# Project Page Premium Showroom Runbook

Use this skill when turning a real-estate project page into a flagship, replicable project showroom
for NadLan. The target is a buyer-ready, investor-search-ready, contractor-demo-ready page, not a
plain WordPress article.

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

## C. 3D And Buyer Interaction

1. Default view is the building selector, not the map.
2. The buyer can drag or tap angle controls to rotate/spin.
3. Clickable floors/units update the selected-unit card, facts, compare tray, sun insight and lead
   payload.
4. Map view is user-opened and lazy-loaded to control Mapbox costs.
5. Register Mapbox RTL text plugin before creating a map with Hebrew labels.
6. Drawings, floor plans and real inventory are optional CMS fields. If absent, show a clear request
   path instead of faking a plan.
7. Price can be:
   - official unit price,
   - explicit unit estimate,
   - project average per sqm estimate,
   - or `לפי פנייה`.
   Anything estimated must say `אומדן` and `לא מחייב`.

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

The default model can be schematic, but the user experience must still feel like a product
showroom: building-first, drag to rotate/tilt, visible zoom controls, large unit hit areas, no
nested scrollbars and source-aware price/availability wording.

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

## G. Model Asset Wire-In

When the model-viewer rail is live but `projects_with_glb` is still `0`, the next step is not a
plugin rebuild. It is CMS wiring.

For Rainbow, use:

- `docs/qa/2026-06-14-rainbow-glb-cms-wiring-runbook.md`
- `scripts/prepare-rainbow-cms-payload.py`

For future projects, create the same asset folder and payload helper pattern:

1. `assets/projects/<slug>/model.glb`
2. `assets/projects/<slug>/poster.png`
3. `assets/projects/<slug>/project-meta-example.json`
4. A QA/runbook doc that lists the exact post id, model URLs, unit JSON, healthcheck proof and
   browser QA gates.

Do not wire a public page to a draft branch asset unless the owner explicitly approves a temporary
QA pass. After merge, use `main` raw URLs, WordPress Media URLs or a CDN, then clear cache and
verify healthcheck `project_3d.projects_with_glb >= 1`.

Use the shared readiness checker for every future asset folder:

```powershell
python scripts\check-rainbow-showroom-readiness.py --project-slug <latin-slug> --skip-live
```

Despite the historical Rainbow filename, the checker validates any `assets/projects/<latin-slug>/`
folder that follows the same contract. GitHub raw URLs from this repo must point to `main`; custom
WordPress Media/CDN HTTPS URLs are acceptable and should be verified with `--check-remote-assets`
before public CMS wiring.

The shared apply helper follows the same future-project pattern:

```powershell
python scripts\apply-rainbow-cms-payload.py --project-slug <latin-slug> --post-id <project-id> --branch main
```

In `--apply` mode, it must prove the live plugin stack is ready before asking for WordPress
credentials. Do not bypass that preflight for a final public page.

After writing, the helper must verify the REST response, not only trust that the request succeeded:
exact GLB/poster/model values, drawing/environment counts, and, when unit REST support is live, unit
count plus unit ids. A mismatch means the project is not CMS-wired yet.

## Page Assembly And SEO Gate

A project showroom is not finished when the 3D model works. The page also needs a premium indexed
content shell with one visible H1, guide assembly, transactional title/meta, FAQ schema, price/schema
disclaimers and enough buyer-language depth.

For Rainbow, run:

```powershell
python scripts\check-rainbow-page-assembly.py --strict
```

The checker validates the public page, healthcheck assembly flags, JSON-LD, visible word count,
transactional keyword counts, title/meta direction and public rendering leaks. Future cloned projects
should get the same checker generalized to their slug and post id before launch.
