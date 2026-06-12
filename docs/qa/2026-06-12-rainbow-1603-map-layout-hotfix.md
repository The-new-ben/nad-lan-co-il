# Rainbow 1.60.3 Map And Layout Hotfix QA

## Live failure reproduced before fix

- URL: `https://nad-lan.co.il/projects/rainbow-tel-aviv/?cb=1602-browser`
- Healthcheck before fix: `version=1.60.2`, `project_3d.view_from_unit=mapbox_live`, `compound_map.token_present=true`.
- Browser measurement showed the module existed but the view-from-apartment panel was trapped in
  the narrow buyer console:
  - `.nlp3d` width: about `920px`
  - `.nlp3d-viewframe` left: negative/off-column in the live audit
  - `.nlp3d-view-map` width: about `282-285px`
- Root cause: the final 1.60.2 wide layout targeted `.entry-content > .nlp3d` and
  `.wp-block-post-content > .nlp3d`, but the live Rainbow module is inserted inside the plugin
  profile body, so those rules did not own the layout. The deeper product issue was that a
  282px side panel can never be the main 3D experience.

## Fix

- Added a final stability CSS layer targeting `.nlp3d.nlp3d-premium` directly.
- The view-from-apartment mode now opens inside the main `.nlp3d-stage-wrap`, over the model,
  instead of rendering in the narrow side console.
- Kept the 1.60.1 Mapbox behavior: no cooperative gestures, NavigationControl is present, the
  live view auto-opens when token + coordinates exist, and camera altitude/bearing recompute on
  unit change.
- Added a return-to-model button, stage-level containment, and stronger tower cues: podium, crown,
  edge highlights, and brighter window rhythm.
- Fixed a separate reviews inline-script syntax issue by moving the review form JavaScript to
  `wp_add_inline_script`; the content-rendered block no longer emits a raw script that WordPress
  can texturize into invalid JavaScript.

## Local checks

- `node` syntax check for `nadlan_p3d_inline_js`: PASS.
- `node` syntax check for the reviews inline script: PASS.
- `php -l`: not run locally because this Windows workspace does not have `php` installed. Must be
  executed by the deploy gate.

## Post-deploy acceptance

- `/wp-json/nadlan/v1/healthcheck` returns `version=1.60.3` and
  `project_3d.layout_contained=true`, `project_3d.stage_live_view=true`.
- Rainbow page returns HTTP 200.
- Browser console has no `Invalid or unexpected token` from the reviews script.
- At 390px and 1440px:
  - no horizontal overflow,
  - `.nlp3d-stage-viewframe` x is not negative,
  - `.nlp3d-view-map` is inside the main stage and width is at least 60% of the stage,
  - Mapbox canvas is visible in the main stage when the token works,
  - fallback text is visible if Mapbox fails.

## Next Slice, Not In This Hotfix

- Premium floating action dock for AI / WhatsApp / call should be v1.61.0 after research and
  accessibility testing. Do not mix it into 1.60.3.
- Before cloning the module across Sde Dov/countrywide, move all project-3D labels into
  translation-ready/filterable strings so English, French, and Russian versions can share the
  same data model without rewriting UI logic.
