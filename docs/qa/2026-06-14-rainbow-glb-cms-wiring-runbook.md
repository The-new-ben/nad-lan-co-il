# Rainbow GLB CMS Wiring Runbook

Use this after PR #163 is merged. It turns the v1.63.0 model-viewer rail from "ready but no GLB"
into a visible 3D model on the live Rainbow Tel Aviv page.

## Preconditions

- Live plugin healthcheck reports `version: 1.63.4` or newer.
- Healthcheck reports `project_3d.model_viewer_ready: true`.
- Healthcheck reports `project_3d.unit_meta_rest: true` (v1.63.2 or newer).
- Healthcheck reports `project_3d.floating_action_rail_v1633: true`.
- Healthcheck reports `project_page_assembly.rainbow_seo_v1634: true`.
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
For GitHub raw URLs on `main`, the readiness script also checks that the corresponding local file
exists in the repo, so a typo in a GLB/poster/plan/drawing URL is caught before it becomes a public
404.

## WordPress Meta To Set

Rainbow post id: `4464`.

Set:

- `project_model_glb`: hosted GLB URL.
- `project_model_poster`: hosted poster URL.
- `project_model_usdz`: empty for now.
- `project_3d_model_type`: `gltf`.
- `project_3d_video_url`: empty until an approved developer/project video is supplied.
- `project_3d_tour_url`: empty until an approved virtual tour is supplied.
- `project_3d_cesium_tiles_url`: empty until an approved Cesium/3D Tiles environment is supplied.
- `project_3d_avg_price_per_sqm`: optional, sourced indicative average used only for non-binding
  estimates.
- `project_3d_price_source_note`: visible source/disclaimer for any computed estimate.
- `project_3d_units`: JSON array from `project-meta-example.json`.
- `project_3d_drawings_json`: JSON array from `project-meta-example.json`.
- `project_3d_environment_json`: flattened JSON array generated from the rich environment object in
  `project-meta-example.json`.

Version boundary: v1.63.0 can show the model-viewer rail, but public GLB wiring should wait for
the full v1.63.4 stack. v1.63.2 exposes `project_3d_units` safely through REST with `edit_post`
auth and a unit sanitizer; v1.63.3 clears the floating contact rail; v1.63.4 closes the page
assembly/title/meta gate. The apply helper checks all of those healthcheck markers before writing.

Keep all demo unit and drawing copy source-aware. Do not remove:

- "לפי פנייה"
- "אומדן"
- "לא הצעה ולא התחייבות"
- "לא BIM רשמי"
- "המחשה מקורית לא רשמית"

Those phrases are part of the legal/product honesty boundary.

The current prototype uses `project_3d_avg_price_per_sqm = 76000` as an indicative calculation basis
from public Madlan-style average price-per-sqm context. It is not official sale inventory. Do not
paste paid transaction rows, exact apartment availability or exact public prices unless the owner has
approved the source/license and the visible note still says the estimate is not an offer or
commitment.

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
- the empty official media/tour/Cesium slots,
- the `material-intake-template.json` handoff list for the project manager/developer,
- the `view-layer-config.json` Mapbox/Cesium view-from-apartment contract,
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

If the plugin update is still propagating or cache is being cleared, use the safe wait mode:

```powershell
python scripts\apply-rainbow-cms-payload.py --branch main --apply --wait-ready --wait-timeout 900 --poll-seconds 20
```

This polls healthcheck before reading WordPress credentials into a write request. It still refuses
to write unless the same v1.63.4 stack markers are live.

The apply helper also enforces the plugin-stack preflight before asking for credentials. It refuses
to write unless live healthcheck proves:

- plugin version at least `1.63.4`,
- `project_3d.model_viewer_ready=true`,
- `project_3d.unit_meta_rest=true`,
- `project_3d.floating_action_rail_v1633=true`,
- `project_page_assembly.rainbow_seo_v1634=true`.

For a future project using the same asset contract:

```powershell
python scripts\apply-rainbow-cms-payload.py --project-slug <latin-slug> --post-id <project-id> --branch main
```

Only use `--skip-plugin-stack-check` for an explicit temporary QA fallback. Do not use it for the
final public showroom wire-in.

After a REST write, the helper performs a strict returned-meta verification. It fails with exit `5`
if WordPress does not return the expected GLB/poster values, drawing count, environment count or,
when `project_3d.unit_meta_rest=true`, the expected unit count and unit ids. Do not treat a write as
complete if this verification fails.

Safety guard: `--apply` refuses to write any `raw.githubusercontent.com/The-new-ben/nad-lan-co-il/<branch>/...`
asset URL unless the ref is `main`. This prevents a public Rainbow page from depending on a
temporary PR branch that may be deleted after merge. If an operator intentionally wants a temporary
pre-merge QA write, the explicit override is:

```powershell
python scripts\apply-rainbow-cms-payload.py --branch codex/rainbow-prototype-model-1631 --apply --allow-branch-assets
```

Do not leave that override state on the live page. Replace it with `main`, WordPress Media, or CDN
URLs before public review.

The helper writes:

- `project_3d_model_type`
- `project_model_glb`
- `project_model_poster`
- `project_model_usdz`
- `project_3d_video_url`
- `project_3d_tour_url`
- `project_3d_cesium_tiles_url`
- `project_3d_avg_price_per_sqm`
- `project_3d_price_source_note`
- `project_3d_drawings_json`
- `project_3d_environment_json`
- `project_3d_units` only when healthcheck reports the full v1.63.4 stack is live

It does not print credentials. On older plugin versions it refuses `--apply` before writing; use
dry-run output only for review until the plugin stack is actually deployed.

The helper also refuses any payload that looks text-corrupted before credentials or writes are used.
It checks for replacement characters, C1 mojibake controls and an unexpectedly low Hebrew-character
count in the public showroom payload. If this fails, regenerate the JSON from source instead of
copying terminal output that may have been damaged by a Windows code-page view.

## One-Command Operator Sequence

After PR #163 and the required plugin stack are merged, use the orchestrator to avoid applying the
CMS payload out of order:

```powershell
python scripts\project-showroom-go-live.py --project-slug rainbow-tel-aviv --post-id 4464
```

This is read-only by default. It runs the deploy-sequence preflight, remote asset/signature checks
and CMS payload dry run, then stops before any WordPress write.

To apply and immediately run the finish-line gate:

```powershell
$env:WP_BASE_URL='https://nad-lan.co.il'
$env:WP_USER='<wordpress-user>'
$env:WP_APP_PASSWORD='<application-password>'
python scripts\project-showroom-go-live.py --project-slug rainbow-tel-aviv --post-id 4464 --apply --wait-ready
```

For the current incomplete live state, the negative-control proof is:

```powershell
python scripts\project-showroom-go-live.py --expect-incomplete
```

That command should pass only while the live stack is incomplete. Once the stack is merged and
deployed, it should stop passing, and the normal preflight/apply path above becomes the correct gate.
The deploy-sequence checker is squash-aware: it accepts either branch ancestry or the expected
marker/file on `origin/main`, because GitHub squash merges do not leave the feature branch commit as
a direct ancestor of main.
For future projects, pass the project slug and that project's asset branch:

```powershell
python scripts\project-showroom-go-live.py --project-slug <latin-slug> --post-id <project-id> --asset-branch origin/codex/<project-asset-branch>
```

The checker then looks for `assets/projects/<latin-slug>/model.glb` on `origin/main` instead of the
Rainbow path, while keeping the same shared plugin-stack markers.
When `--fetch` is used, the checker runs `git fetch origin --prune`, not a main-only fetch, because
the diagnosis depends on the latest remote refs for the stacked plugin branches and the project
asset branch.

## Readiness Check

Before merge or before CMS wire-in, run:

```powershell
python scripts\check-rainbow-showroom-readiness.py
```

Expected now: local assets pass, asset URLs are durable (`main` or custom hosted), demo units carry
non-binding price/source language, every unit has a plan URL plus empty `interior_url` and
`tour_url` slots, drawing material has linked URLs, project-level video/tour/Cesium fields are
present, public JSON files pass the UTF-8/Hebrew text-sanity check, live `model_viewer_ready`
passes, and `projects_with_glb` is a warning because the live Rainbow post is not wired yet.
Any `main` raw URL in the payload must also resolve to a local committed file.

Empty media/tour/Cesium slots are intentional. Fill them only with approved `https://` URLs:

- official project video or a licensed sales video,
- owner-approved Matterport/virtual-tour style link,
- approved Cesium 3D Tiles / Google Photorealistic 3D Tiles view layer,
- unit-level official interior media or a licensed virtual tour.

Do not use copied developer media, stock interiors, fake tours or unlicensed screenshots. The
readiness gate warns on empty slots but fails malformed or non-HTTPS URLs.

## Contractor / Developer Material Handoff

The asset folder includes `material-intake-template.json`. Use it as the handoff checklist when the
project manager or developer supplies official material. It maps every requested asset to the CMS
field it powers:

- official BIM/GLB or convertible source model,
- official poster/still frame,
- project sales video,
- virtual tour,
- Cesium/3D Tiles view layer,
- approved drawings and floor plans,
- unit inventory and availability feed,
- unit interior media and unit tour links,
- surroundings/project pins.

The file also records the public-use rule for each item. Keep a slot empty until the source and
rights are approved. Empty slots are a valid state; fake media is not.

## View Layer Contract

The asset folder includes `view-layer-config.json`. This is the repeatable contract for the
apartment-view layer:

- Mapbox is the current live provider and must stay `user_open_only`.
- Cesium/3D Tiles is a ready seam, but `project_3d_cesium_tiles_url` stays empty until approved
  token/cost governance and public-use rights exist.
- Camera altitude is derived from `ground_elevation_m + 4.0 + (floor - 1) * floor_height_m + 1.55`.
- Unit bearing comes from the unit direction and is stored per unit for QA.
- Environment overlays are source-aware: verified pins can be clickable, unverified projects remain
  cards until coordinates are approved.
- The default first view remains the building selector, not map or tiles.

To prove the remote files on this PR branch before merge without changing the durable CMS payload,
run:

```powershell
python scripts\check-rainbow-showroom-readiness.py --skip-live --check-remote-assets --remote-ref codex/rainbow-prototype-model-1631
```

## Local Prototype Browser Gate

Before the GLB is wired into the live CMS, prove the committed model package in a real browser:

```powershell
node scripts\check-rainbow-prototype-preview.mjs
```

The command serves the repo locally, opens `docs/previews/rainbow-model-viewer-prototype.html` in
headless Chrome or Edge, and checks desktop 1440px plus mobile 390px:

- one H1 and RTL document,
- no horizontal overflow,
- `<model-viewer>` custom element defined,
- GLB loaded/revealed,
- six hotspots present,
- visible hotspot targets at least 44px,
- hotspot click updates the readout,
- drawings and plans panel renders from `drawings.json`,
- surroundings panel renders from `environment.json`,
- media/view slots render from `project-meta-example.json` and remain honest when pending,
- view-layer policy is user-opened/lazy according to `view-layer-config.json`,
- no browser errors or visible fatal text.

Current evidence:

- `docs/qa/screenshots-rainbow-prototype-preview/prototype-desktop-1440.png`
- `docs/qa/screenshots-rainbow-prototype-preview/prototype-mobile-390.png`
- `docs/qa/screenshots-rainbow-prototype-preview/rainbow-prototype-preview-report.json`

`--remote-ref` changes only what the checker fetches for QA. It does not change the payload file and
must not be used as a live CMS URL strategy.

After the plugin stack is deployed through v1.63.4 and before applying the Rainbow CMS payload, run:

```powershell
python scripts\check-rainbow-deploy-sequence.py
python scripts\check-rainbow-showroom-readiness.py --require-plugin-stack
```

The deploy-sequence checker shows exactly whether the blocker is an unmerged branch, an outdated
live plugin, a missing healthcheck marker, or `projects_with_glb=0`. Then the readiness checker must
pass:

- live plugin version at least `1.63.4`,
- `project_3d.unit_meta_rest=true` from v1.63.2,
- `project_3d.floating_action_rail_v1633=true` from v1.63.3,
- `project_3d.model_viewer_ready=true` from v1.63.0,
- `project_page_assembly.rainbow_seo_v1634=true` from v1.63.4.

If this fails, stop and finish the plugin deploy sequence first. Do not apply the CMS payload to an
older plugin, because unit JSON may not write through REST, the floating contact rail may still cover
the showroom controls, or the page may still fail the flagship SEO/title/meta gate.

After PR #163 is merged to `main`, but before applying the CMS payload, run the remote URL gate:

```powershell
python scripts\check-rainbow-showroom-readiness.py --check-remote-assets
```

This fetches the GLB, poster, schematic plan and drawing URLs and verifies the file signatures
before any public CMS write depends on them.

After merge and after the CMS fields are populated, run:

```powershell
python scripts\check-rainbow-showroom-readiness.py --require-plugin-stack --check-remote-assets --expect-live-glb
```

Expected after wire-in: every check passes, including `projects_with_glb >= 1`.

For the final combined gate, run:

```powershell
python scripts\check-rainbow-finish-line.py
```

This command fails unless the live healthcheck proves v1.63.4+, the page assembly checker passes,
the GLB is wired (`projects_with_glb >= 1`), and the real browser DOM gate passes with
`<model-viewer>` visible plus clickable drawings, surroundings and media panels.

## Live DOM / Visual Gate

Before and after CMS wire-in, run:

```powershell
node scripts\check-rainbow-live-dom.mjs --out docs\qa\screenshots-rainbow-live-dom-current
```

After GLB wire-in:

```powershell
node scripts\check-rainbow-live-dom.mjs --expect-glb --expect-materials --out docs\qa\screenshots-rainbow-live-dom-after-glb
```

This gate checks the rendered page at 1440px and 390px for:

- one H1,
- showroom presence,
- horizontal overflow,
- raw code leaks,
- visible PHP/JS error text,
- featured-image suppression,
- model-viewer/fallback state,
- visible showroom tap targets below 44px,
- model-viewer hotspot presence when `--expect-glb` is used,
- real product interaction: a browser-level drag over `<model-viewer>` changes the camera orbit,
- buyer action: tapping a hotspot/facade/unit target updates the selected-unit title, stage card and
  active state,
- material action: after selecting a unit, the drawing, surroundings and media tools are reachable;
  when `--expect-materials` is used, drawings must render linked cards and surroundings must render
  several source-aware cards,
- fixed WhatsApp/AI/contact widgets do not overlap visible showroom controls.

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

1. Create the contract scaffold:

```powershell
python scripts\scaffold-project-showroom.py --project-slug <latin-slug> --project-name "<Project Name>" --post-id <project-id> --city "<city>" --lat <lat> --lng <lng>
```

2. Generate or receive a model as `model.glb`.
3. Generate a `poster.png`.
4. Fill `project-meta-example.json` with:
   - `project_model_glb`,
   - `project_model_poster`,
   - `project_model_usdz`,
   - `project_3d_units`,
   - `project_3d_drawings_json`,
   - `project_3d_video_url`,
   - `project_3d_tour_url`,
   - `project_3d_cesium_tiles_url`.
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

Before applying to WordPress, print the copy/paste payload and review the model/media URLs:

```powershell
python scripts\prepare-rainbow-cms-payload.py --project-slug <latin-slug> --post-id <project-id> --branch main
```

The readiness checker defaults to Rainbow. For the next project, keep the same asset contract and
pass the project slug:

```powershell
python scripts\check-rainbow-showroom-readiness.py --project-slug <latin-slug> --skip-live
```

If the project uses WordPress Media or a CDN for plans/drawings instead of GitHub raw URLs, HTTPS
URLs are valid. When `--check-remote-assets` is used, the checker fetches those hosted files and
validates their signatures. GitHub raw URLs from this repository must still point to `main` before a
public CMS write.

This is the repeatable handoff from model asset to live CMS-driven showroom.
