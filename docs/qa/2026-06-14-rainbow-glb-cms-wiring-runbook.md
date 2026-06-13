# Rainbow GLB CMS Wiring Runbook

Use this after PR #163 is merged. It turns the v1.63.0 model-viewer rail from "ready but no GLB"
into a visible 3D model on the live Rainbow Tel Aviv page.

## Preconditions

- Live plugin healthcheck reports `version: 1.63.0`.
- Healthcheck reports `project_3d.model_viewer_ready: true`.
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
- Metadata source:
  `assets/projects/rainbow-tel-aviv/project-meta-example.json`

If GitHub raw is too slow or blocked by cache policy, upload `model.glb` and `poster.png` to
WordPress Media or a CDN and use those URLs instead.

## WordPress Meta To Set

Rainbow post id: `4464`.

Set:

- `project_model_glb`: hosted GLB URL.
- `project_model_poster`: hosted poster URL.
- `project_model_usdz`: empty for now.
- `project_3d_units`: JSON array from `project-meta-example.json`.
- `project_3d_drawings_json`: JSON array from `project-meta-example.json`.
- `project_3d_environment_json`: JSON object from `project-meta-example.json`.

Keep all demo unit copy source-aware. Do not remove:

- "לפי פנייה"
- "אומדן"
- "לא הצעה ולא התחייבות"
- "לא BIM רשמי"

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
- the `project_3d_environment_json` JSON,
- a safe copy/paste checklist.

It does not write to WordPress.

## Readiness Check

Before merge or before CMS wire-in, run:

```powershell
python scripts\check-rainbow-showroom-readiness.py
```

Expected now: local assets pass, live `model_viewer_ready` passes, and `projects_with_glb` is a
warning because the live Rainbow post is not wired yet.

After merge and after the CMS fields are populated, run:

```powershell
python scripts\check-rainbow-showroom-readiness.py --expect-live-glb
```

Expected after wire-in: every check passes, including `projects_with_glb >= 1`.

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
   - optional `camera_orbit`,
   - `source_note`.
6. If official inventory is missing, show inquiry-only pricing and label the model illustrative.
7. Run the same 1440/390 browser QA before publishing.

This is the repeatable handoff from model asset to live CMS-driven showroom.
