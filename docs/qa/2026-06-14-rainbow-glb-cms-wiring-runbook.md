# Rainbow GLB CMS Wiring Runbook

Use this after PR #163 is merged. It turns the v1.63.0 model-viewer rail from "ready but no GLB"
into a visible 3D model on the live Rainbow Tel Aviv page.

## Preconditions

- Live plugin healthcheck reports `version: 1.63.0` or newer.
- Healthcheck reports `project_3d.model_viewer_ready: true`.
- For fully automated unit wiring, healthcheck reports `project_3d.unit_meta_rest: true`
  (v1.63.2 or newer). If not, use the metabox fallback for `project_3d_units`.
- PR #163 is merged to `main`.
- The UPress/server Git copy has been pulled or synced after the merge.
- Cache can be cleared after the write.

Do not wire the public page to an unreviewed draft asset unless it is an explicit temporary QA
decision.

## Files

After merge, the production asset URLs are:

- GLB:
  `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/assets/projects/rainbow-tel-aviv/model.glb`
- Poster:
  `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/assets/projects/rainbow-tel-aviv/poster.png`
- Prototype plans:
  `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/assets/projects/rainbow-tel-aviv/plans/`
- Metadata source:
  `assets/projects/rainbow-tel-aviv/project-meta-example.json`

If GitHub raw is too slow or blocked by cache policy, upload `model.glb` and `poster.png` to
WordPress Media or a CDN and use those URLs instead.

Do not leave the live card pointing at a draft branch raw URL. The readiness script fails
`raw.githubusercontent.com/The-new-ben/nad-lan-co-il/<branch>/...` URLs unless the ref is `main`,
because draft branches can be deleted after merge and would break the public model.

## WordPress Meta To Set

Rainbow post id: `4464`.

Set:

- `project_model_glb`: hosted GLB URL.
- `project_model_poster`: hosted poster URL.
- `project_model_usdz`: empty for now.
- `project_3d_model_type`: `gltf`.
- `project_3d_units`: JSON array from `project-meta-example.json`.
- `project_3d_drawings_json`: JSON array from `project-meta-example.json`.
- `project_3d_environment_json`: flattened JSON array generated from the rich environment object in
  `project-meta-example.json`.

Version boundary: v1.63.0 saves `project_3d_units` through the admin metabox only. v1.63.2 exposes
it safely through REST with `edit_post` auth and a unit sanitizer. The apply helper checks
healthcheck before writing units and falls back to printing the metabox value when the marker is
missing.

Keep all demo unit and drawing copy source-aware. Do not remove:

- "לפי פנייה"
- "אומדן"
- "לא הצעה ולא התחייבות"
- "לא BIM רשמי"
- "המחשה מקורית לא רשמית"

Those phrases are part of the legal/product honesty boundary.

## Generate The Payload

From the repo root:

```powershell
python scripts\prepare-rainbow-cms-payload.py --branch main
```

For a temporary branch QA URL before merge:

```powershell
python scripts\prepare-rainbow-cms-payload.py --branch codex/rainbow-prototype-model-1631
```

The script prints:

- the exact model URLs,
- the full `project_3d_units` JSON,
- the `project_3d_drawings_json` JSON,
- the flattened `project_3d_environment_json` JSON,
- a safe copy/paste checklist.

It does not write to WordPress.

The generator also defaults `project-meta-example.json` to `main` URLs. For a throwaway pre-merge
QA artifact only, set `RAINBOW_MODEL_REF=codex/rainbow-prototype-model-1631` before running
`scripts\generate-rainbow-prototype-model.py`; do not commit or publish branch-scoped URLs to the
live CMS payload.

## Optional REST Apply Helper

To write the REST-registered fields, use the dry-run-first helper:

```powershell
python scripts\apply-rainbow-cms-payload.py --branch main
```

Dry run prints the exact fields and the unit JSON. In apply mode, the helper checks the live
healthcheck before deciding whether to include `project_3d_units`.

To apply:

```powershell
$env:WP_BASE_URL='https://nad-lan.co.il'
$env:WP_USER='<wordpress-user>'
$env:WP_APP_PASSWORD='<application-password>'
python scripts\apply-rainbow-cms-payload.py --branch main --apply
```

The helper writes:

- `project_3d_model_type`
- `project_model_glb`
- `project_model_poster`
- `project_model_usdz`
- `project_3d_drawings_json`
- `project_3d_environment_json`
- `project_3d_units` only when healthcheck reports `project_3d.unit_meta_rest=true`

It does not print credentials. On older plugin versions it skips `project_3d_units` and prints the
metabox fallback instead of forcing a write that WordPress will reject or ignore.

## Readiness Check

Before merge or before CMS wire-in, run:

```powershell
python scripts\check-rainbow-showroom-readiness.py
```

Expected now: local assets pass, asset URLs are durable (`main` or custom hosted), demo units carry
non-binding price/source language, every unit has a plan URL, drawing material has linked URLs, live
`model_viewer_ready` passes, and `projects_with_glb` is a warning because the live Rainbow post is
not wired yet.

After merge and after the CMS fields are populated, run:

```powershell
python scripts\check-rainbow-showroom-readiness.py --expect-live-glb
```

Expected after wire-in: every check passes, including `projects_with_glb >= 1`.

## Live DOM / Visual Gate

Before and after CMS wire-in, run:

```powershell
node scripts\check-rainbow-live-dom.mjs --out docs\qa\screenshots-rainbow-live-dom-current
```

After GLB wire-in:

```powershell
node scripts\check-rainbow-live-dom.mjs --expect-glb --out docs\qa\screenshots-rainbow-live-dom-after-glb
```

This gate checks the rendered page at 1440px and 390px for:

- one H1,
- showroom presence,
- horizontal overflow,
- raw code leaks,
- visible PHP/JS error text,
- featured-image suppression,
- model-viewer/fallback state,
- visible showroom tap targets below 44px.

Current live pre-wire evidence is recorded in
`docs/qa/2026-06-14-rainbow-live-dom-current.md`.

## Browser QA After Wiring

Open:

`https://nad-lan.co.il/projects/rainbow-tel-aviv/?cb=<timestamp>`

Desktop 1440:

- The model stage shows the real `<model-viewer>` asset, not only the fallback tower.
- The poster appears before the model loads.
- Drag rotates the model.
- Zoom controls work.
- Hotspot click selects a unit and updates the selected-unit card.
- Surroundings/environment panel can read nearby-project, parks, mobility and services data.
- Lead form payload still includes card, unit, floor, sqm and inquiry context.
- No horizontal overflow.
- No raw code text visible.

Mobile 390:

- The model does not overflow the viewport.
- Touch drag rotates the model.
- Hotspots are still tappable.
- The selected-unit card stacks below/inside the stage without covering required controls.
- Contact/floating buttons do not cover the showroom controls or lead form.

Healthcheck after cache clear:

- `project_3d.projects_with_glb` should be at least `1`.

## Failure Handling

If the GLB fails to load:

1. Confirm the GLB URL returns HTTP 200 and `model/gltf-binary` or a browser-acceptable binary
   response.
2. Confirm the URL is reachable without authentication.
3. Confirm the model file size remains small enough for public delivery.
4. Confirm the fallback tower still appears. A blank stage is a failure.
5. If GitHub raw is blocked or slow, upload the GLB to Media/CDN and update `project_model_glb`.
6. Keep the schematic plan URLs until official plans arrive; once official plans are approved,
   replace the URLs but keep the same `plan` and `project_3d_drawings_json` fields so the buyer
   journey does not change.

## Replication To The Next Project

For each future project:

1. Create `assets/projects/<latin-slug>/`.
2. Generate or receive a model as `model.glb`.
3. Generate a `poster.png`.
4. Create `project-meta-example.json` with:
   - `project_model_glb`,
   - `project_model_poster`,
   - `project_model_usdz`,
   - `project_3d_units`,
   - `project_3d_drawings_json`.
5. Every unit must include:
   - stable `id`,
   - `title`,
   - `floor`,
   - `rooms`,
   - `sqm`,
   - `dir`,
   - `status`,
   - `hotspot_position`,
   - `hotspot_normal`,
   - `plan`,
   - optional `camera_orbit`,
   - `source_note`.
6. If official inventory is missing, show inquiry-only pricing and label the model illustrative.
7. Run the same 1440/390 browser QA before publishing.

This is the repeatable handoff from model asset to live CMS-driven showroom.
